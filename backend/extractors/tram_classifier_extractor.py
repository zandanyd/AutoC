import torch
import json
import joblib
from transformers import BertTokenizer
from typing import List, Optional
from huggingface_hub import hf_hub_download
import blingfire
from collections import defaultdict

class mitreClassifierExtractor:
    def __init__(
        self,
        article_content: str,
        model_repo: str = "dvir056/mitre_ttp",
        threshold: float = 0.3,
        keywords: List[str] = [],
        qna: Optional[List[dict]] = None,
    ):
        self.article_content = article_content
        self.threshold = threshold
        self.keywords = keywords
        self.qna = qna or []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # === Load model, tokenizer, label binarizer from Hugging Face ===
        self.model_path = model_repo
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)

        scripted_model_path = hf_hub_download(repo_id=model_repo, filename="model_scripted.pt")
        self.model = torch.jit.load(scripted_model_path).to(self.device)
        self.model.eval()

        label_binarizer_path = hf_hub_download(repo_id=model_repo, filename="label_binarizer.pkl")
        self.mlb = joblib.load(label_binarizer_path)

        mitre_json_path = hf_hub_download(repo_id=model_repo, filename="enterprise-attack.json")
        self.mitre_map = self._load_mitre_map(mitre_json_path)

    def _load_mitre_map(self, json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        mapping = {}
        for obj in data["objects"]:
            if obj.get("type") == "attack-pattern":
                for ref in obj.get("external_references", []):
                    if ref.get("source_name") == "mitre-attack" and "external_id" in ref:
                        mapping[ref["external_id"]] = {
                            "name": obj.get("name", "Unknown"),
                            "url": ref.get("url", "")
                        }
        return mapping

    def classify(self):
        chunks = []

        # 1. Split article
        if len(self.tokenizer.encode(self.article_content, add_special_tokens=False)) > 512:
            chunks = self._split_text_into_chunks(self.article_content)
        else:
            chunks = [self.article_content]

        # 2. Add keywords
        if self.keywords:
            keyword_text = " ".join(self.keywords)
            chunks.append(keyword_text)

        # 3. Add QnA answers
        for item in self.qna:
            answer = item.get("answer", "").strip()
            if answer:
                if len(self.tokenizer.encode(answer, add_special_tokens=False)) > 512:
                    chunks.extend(self._split_text_into_chunks(answer))
                else:
                    chunks.append(answer)

        # 4. Predict
        all_preds = {}
        for chunk in chunks:
            inputs = self.tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                logits = self.model(inputs["input_ids"], inputs.get("attention_mask"), inputs.get("token_type_ids"))
                probs = torch.sigmoid(logits).cpu().numpy()[0]

            for idx, prob in enumerate(probs):
                if prob > self.threshold:
                    label = self.mlb.classes_[idx]
                    all_preds[label] = all_preds.get(label, 0) + prob

        # Sort by descending probability
        sorted_preds = sorted(all_preds.items(), key=lambda x: x[1], reverse=True)
        sorted_labels = [tid for tid, _ in sorted_preds]
        return self.enrich_ids_with_metadata(sorted_labels)

    def _split_text_into_chunks(self, text, max_tokens=512, stride=256):
        sentences = blingfire.text_to_sentences(text).split('\n')

        chunks = []
        current_chunk = ""
        for sentence in sentences:
            tentative = f"{current_chunk} {sentence}".strip() if current_chunk else sentence
            token_count = len(self.tokenizer.encode(tentative, add_special_tokens=False))

            if token_count <= max_tokens:
                current_chunk = tentative
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def enrich_ids_with_metadata(self, technique_ids):
        results = []
        for tid in technique_ids:
            info = self.mitre_map.get(tid, {"name": "Unknown Technique", "url": ""})
            results.append({
                "id": tid,
                "name": info["name"],
                "url": info["url"]
            })
        return results
