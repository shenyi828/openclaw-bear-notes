#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from typing import List, Optional


def normalize_tag(tag: str) -> str:
    tag = tag.strip().lstrip("#")
    return tag


def read_note(file_path: Optional[str], body: Optional[str]) -> str:
    if file_path:
        return Path(file_path).expanduser().read_text(encoding="utf-8")
    return body or ""


def escape_js(s: str) -> str:
    return json.dumps(s)


def build_bear_url(title: str, note: str, tags: List[str]) -> str:
    title_js = escape_js(title)
    note_js = escape_js(note)
    tag_list = [normalize_tag(t) for t in tags if t.strip()]
    tags_js = escape_js(",".join(tag_list))
    script = f'''set theTitle to {title_js}
set theNote to {note_js}
set theTags to {tags_js}
set encodedTitle to do shell script "python3 - <<'PY'\nimport urllib.parse,sys\nprint(urllib.parse.quote(sys.stdin.read(), safe=''))\nPY" input theTitle
set encodedNote to do shell script "python3 - <<'PY'\nimport urllib.parse,sys\nprint(urllib.parse.quote(sys.stdin.read(), safe=''))\nPY" input theNote
set encodedTags to do shell script "python3 - <<'PY'\nimport urllib.parse,sys\nprint(urllib.parse.quote(sys.stdin.read(), safe=''))\nPY" input theTags
set theURL to "bear://x-callback-url/create?title=" & encodedTitle & "&text=" & encodedNote & "&tags=" & encodedTags
open location theURL'''
    return script


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--body")
    ap.add_argument("--file")
    args = ap.parse_args()

    note = read_note(args.file, args.body)
    script = build_bear_url(args.title, note, args.tag)
    subprocess.run(["osascript", "-e", script], check=True)
    print("OK")

if __name__ == "__main__":
    main()
