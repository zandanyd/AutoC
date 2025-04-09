import torch
import json
import os
import joblib
from transformers import BertTokenizer
from typing import List, Optional



class TramClassifierExtractor:
    def __init__(self, article_content: str, model_path: str, threshold: float = 0.2, keywords: List[str] = [], qna: Optional[List[dict]] = None,):
        self.article_content = article_content
        self.model_path = model_path
        self.threshold = threshold
        self.keywords = keywords
        self.qna = qna or []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = torch.jit.load(os.path.join(model_path, "model_scripted.pt")).to(self.device)
        self.model.eval()
        self.mlb = joblib.load(os.path.join(model_path, "label_binarizer.pkl"))

        self.mitre_map = self._load_mitre_map()

    def _load_mitre_map(self):
        json_path = os.path.join(self.model_path, "enterprise-attack.json")
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
        text = self.article_content
        chunks = []
        if len(self.tokenizer.encode(text, add_special_tokens=False)) > 512:
            chunks = self._split_text_into_chunks(text)
            len_chunks = len(chunks)
            print(len_chunks)
       
        else:
            chunks = [text]

        if self.keywords:
            keyword_text = " ".join(self.keywords)
            chunks.append(keyword_text)  

        # Add QnA answers as separate chunks
        for item in self.qna:
            answer = item.get("answer", "").strip()
            if answer:
                if len(self.tokenizer.encode(answer, add_special_tokens=False)) > 512:
                    chunks.extend(self._split_text_into_chunks(answer))
                else:
                    chunks.append(answer)
    
        all_preds = set()
        for chunk in chunks:
            inputs = self.tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                logits = self.model(inputs["input_ids"], inputs.get("attention_mask"), inputs.get("token_type_ids"))
                probs = torch.sigmoid(logits).cpu().numpy()
                preds = (probs > self.threshold).astype(int)
                labels = list(self.mlb.inverse_transform(preds)[0])
                all_preds.update(labels)

        # Enrich the technique IDs with metadata
        enriched_techniques = self.enrich_ids_with_metadata(list(all_preds))
        return enriched_techniques
    
    def _split_text_into_chunks(self, text, max_tokens=512, stride=256):
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        for i in range(0, len(tokens), stride):
            chunk = tokens[i:i + max_tokens]
            if chunk:
                chunks.append(self.tokenizer.decode(chunk))
            if i + max_tokens >= len(tokens):
                break
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
