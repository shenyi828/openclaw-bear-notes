#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Optional


def load_text(text: Optional[str], file: Optional[str]) -> str:
    if file:
        return Path(file).expanduser().read_text(encoding="utf-8")
    return text or ""


def suggest(text: str) -> str:
    lines = [line.strip('# ').strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "未命名笔记"
    first = lines[0]
    if len(first) <= 30:
        return first
    return first[:30].rstrip() + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--file")
    args = ap.parse_args()
    print(suggest(load_text(args.text, args.file)))

if __name__ == "__main__":
    main()
