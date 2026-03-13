#!/usr/bin/env python3
import argparse
from pathlib import Path

KEYWORDS = {
    "心理": "博闻强记/心理学",
    "情绪": "博闻强记/心理学",
    "认知": "博闻强记/心理学",
    "AI": "博闻强记/AI",
    "向量库": "向量库",
    "方法论": "方法论",
    "会议": "工作/会议纪要",
    "复盘": "方法论",
    "小说": "小说",
}


def recommend(text: str) -> list[str]:
    found = []
    for k, v in KEYWORDS.items():
        if k.lower() in text.lower() and v not in found:
            found.append(v)
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--file")
    args = ap.parse_args()
    text = args.text or ""
    if args.file:
        text = Path(args.file).expanduser().read_text(encoding="utf-8")
    for tag in recommend(text):
        print(tag)

if __name__ == "__main__":
    main()
