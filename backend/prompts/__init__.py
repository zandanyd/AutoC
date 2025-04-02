import yaml


def get_prompts():
    prompts = {}
    with open("backend/prompts/extract_qna.yaml") as f:
        prompts["qna"] = yaml.safe_load(f)

    with open("backend/prompts/extract_iocs.yaml") as f:
        prompts["iocs"] = yaml.safe_load(f)

    return prompts
