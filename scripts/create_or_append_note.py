#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from decide_note_action import decide
from suggest_title import suggest
from recommend_tags import recommend


def load_text(text: Optional[str], file: Optional[str]) -> str:
    if file:
        return Path(file).expanduser().read_text(encoding="utf-8")
    return text or ""


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--file")
    ap.add_argument("--title")
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--force-action", choices=["create", "append"])
    ap.add_argument("--print-only", action="store_true")
    args = ap.parse_args()

    text = load_text(args.text, args.file)
    if not text.strip():
        raise SystemExit("No note content provided.")

    title = args.title or suggest(text)
    decision = decide(text)
    action = args.force_action or decision["action"]
    tags = list(args.tag)
    auto_tags = recommend(text)
    for tag in auto_tags:
        if tag not in tags:
            tags.append(tag)

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(text)
        temp_body = tmp.name

    rendered = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    rendered.close()

    template = decision.get("template") or "method"
    run([
        "python3", "scripts/render_note.py",
        "--title", title,
        "--template", template,
        "--body-file", temp_body,
        "--out", rendered.name,
        *sum([["--tag", t] for t in tags], []),
    ])

    print(f"action={action}")
    print(f"title={title}")
    print(f"template={template}")
    print(f"tags={','.join(tags)}")
    print(f"rendered={rendered.name}")

    if args.print_only:
        print(Path(rendered.name).read_text(encoding="utf-8"))
        return

    if action == "append":
        run(["python3", "scripts/append_bear_note.py", "--title", title, "--file", rendered.name])
    else:
        create_cmd = ["python3", "scripts/create_bear_note.py", "--title", title, "--file", rendered.name]
        for tag in tags:
            create_cmd.extend(["--tag", tag])
        run(create_cmd)


if __name__ == "__main__":
    main()
