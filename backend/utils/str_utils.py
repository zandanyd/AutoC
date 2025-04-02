import re


def is_md5(s: str) -> bool:
    return bool(re.fullmatch(r"^[a-fA-F0-9]{32}$", s))


def is_sha256(s: str) -> bool:
    return bool(re.fullmatch(r"[a-fA-F0-9]{64}", s))


if __name__ == "__main__":
    print("md5: ", is_md5("471d596dad7ca027a44b21f3c3a2a0d9"))
    print("sha256: ", is_sha256("471d596dad7ca027a44b21f3c3a2a0d9"))
