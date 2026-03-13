#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Optional

KEYWORDS_APPEND = ["追加", "补充", "续写", "更新", "append", "update"]
KEYWORDS_MEETING = ["会议", "纪要", "meeting"]
KEYWORDS_REVIEW = ["复盘", "review"]
KEYWORDS_PSY = ["心理", "情绪", "认知"]


def load_text(text: Optional[str], file: Optional[str]) -> str:
    if file:
        return Path(file).expanduser().read_text(encoding="utf-8")
    return text or ""


def decide(text: str) -> dict:
    lower = text.lower()
    if any(k in text for k in KEYWORDS_APPEND) or any(k in lower for k in KEYWORDS_APPEND):
        return {"action": "append", "template": None, "reason": "matched append/update intent"}
    if any(k in text for k in KEYWORDS_MEETING) or any(k in lower for k in KEYWORDS_MEETING):
        return {"action": "create", "template": "meeting", "reason": "matched meeting intent"}
    if any(k in text for k in KEYWORDS_REVIEW) or any(k in lower for k in KEYWORDS_REVIEW):
        return {"action": "create", "template": "review", "reason": "matched review intent"}
    if any(k in text for k in KEYWORDS_PSY) or any(k in lower for k in KEYWORDS_PSY):
        return {"action": "create", "template": "concept", "reason": "matched psychology intent"}
    return {"action": "create", "template": "method", "reason": "fallback default"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--file")
    args = ap.parse_args()
    text = load_text(args.text, args.file)
    result = decide(text)
    print(result["action"])
    if result["template"]:
        print(result["template"])
    print(result["reason"])

if __name__ == "__main__":
    main()
