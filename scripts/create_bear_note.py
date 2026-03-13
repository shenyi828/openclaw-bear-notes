#!/usr/bin/env python3
import argparse
import subprocess
import urllib.parse
from pathlib import Path
from typing import List, Optional


def normalize_tag(tag: str) -> str:
    return tag.strip().lstrip("#")


def read_note(file_path: Optional[str], body: Optional[str]) -> str:
    if file_path:
        return Path(file_path).expanduser().read_text(encoding="utf-8")
    return body or ""


def strip_leading_h1_and_tags(title: str, note: str, tags: List[str]) -> str:
    lines = note.splitlines()
    tag_set = {f'#{normalize_tag(t)}' for t in tags if t.strip()}

    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        first = lines[i].strip()
        if first.lstrip('#').strip() == title.strip():
            lines = lines[:i] + lines[i+1:]

    cleaned = []
    for line in lines:
        if line.strip() in tag_set:
            continue
        cleaned.append(line)

    while cleaned and not cleaned[0].strip():
        cleaned = cleaned[1:]
    return '\n'.join(cleaned).strip()


def encode_part(text: str) -> str:
    return urllib.parse.quote(text, safe="")


def build_url(title: str, note: str, tags: List[str]) -> str:
    tag_list = [normalize_tag(t) for t in tags if t.strip()]
    clean_note = strip_leading_h1_and_tags(title, note, tags)
    return (
        "bear://x-callback-url/create?title="
        + encode_part(title)
        + "&text="
        + encode_part(clean_note)
        + "&tags="
        + encode_part(",".join(tag_list))
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--body")
    ap.add_argument("--file")
    args = ap.parse_args()

    note = read_note(args.file, args.body)
    url = build_url(args.title, note, args.tag)
    subprocess.run(["open", url], check=True)
    print("OK")

if __name__ == "__main__":
    main()
