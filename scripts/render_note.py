#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import List, Optional

TEMPLATES = {
    "concept": ["定义", "机制", "表现", "应用", "风险与局限", "总结"],
    "method": ["目标", "为什么", "步骤", "注意事项", "总结"],
    "meeting": ["背景", "关键信息", "结论", "待办"],
    "review": ["发生了什么", "问题", "原因", "修正", "结论"],
}

def normalize_tag(tag: str) -> str:
    tag = tag.strip()
    if not tag:
        return ""
    return tag if tag.startswith("#") else f"#{tag}"


def strip_duplicate_h1_and_tags(title: str, body: str, tags: List[str]) -> str:
    lines = body.splitlines()
    clean_tag_set = {normalize_tag(t) for t in tags if t.strip()}

    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        first = lines[i].strip().lstrip('#').strip()
        if first == title.strip():
            lines = lines[:i] + lines[i+1:]

    cleaned = []
    for line in lines:
        s = line.strip()
        if s in clean_tag_set:
            continue
        cleaned.append(line)

    while cleaned and not cleaned[0].strip():
        cleaned = cleaned[1:]
    return "\n".join(cleaned).strip()


def build_content(title: str, tags: List[str], body: str, template: Optional[str]) -> str:
    lines = [f"# {title}", ""]
    clean_tags = [normalize_tag(t) for t in tags if t.strip()]
    if clean_tags:
        lines.extend(clean_tags)
        lines.append("")
    if body.strip():
        cleaned_body = strip_duplicate_h1_and_tags(title, body, tags)
        lines.append(cleaned_body)
    elif template and template in TEMPLATES:
        for section in TEMPLATES[template]:
            lines.append(f"## {section}")
            lines.append("")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--body")
    ap.add_argument("--body-file")
    ap.add_argument("--template", choices=sorted(TEMPLATES.keys()))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    body = args.body or ""
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")

    content = build_content(args.title, args.tag, body, args.template)
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()
