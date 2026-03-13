#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from typing import Optional


PREFIXES = [
    "把这段",
    "把这篇",
    "帮我把",
    "帮我写",
    "整理成",
    "写成",
    "生成",
    "请把",
]


def load_text(text: Optional[str], file: Optional[str]) -> str:
    if file:
        return Path(file).expanduser().read_text(encoding="utf-8")
    return text or ""


def clean_line(line: str) -> str:
    line = line.strip().strip('#').strip()
    line = re.sub(r'[`*_>~-]+', '', line)
    for prefix in PREFIXES:
        if line.startswith(prefix):
            line = line[len(prefix):].strip()
    line = line.replace("Bear 笔记", "").replace("Bear note", "")
    line = re.sub(r'\s+', ' ', line).strip(' ，。；：:,-')
    return line


def suggest(text: str) -> str:
    lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
    if not lines:
        return "未命名笔记"

    first = lines[0]

    if len(first) <= 24 and not any(x in first for x in ["今天", "这段", "这篇"]):
        return first

    for line in lines[1:6]:
        if 4 <= len(line) <= 24 and not line.startswith(("今天", "这次", "这是")):
            return line

    first = re.sub(r'^(关于|对于)', '', first).strip()
    if len(first) > 24:
        first = first[:24].rstrip() + "…"
    return first or "未命名笔记"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--file")
    args = ap.parse_args()
    print(suggest(load_text(args.text, args.file)))

if __name__ == "__main__":
    main()
