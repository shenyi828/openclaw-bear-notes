#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path
from typing import Optional


def read_note(file_path: Optional[str], body: Optional[str]) -> str:
    if file_path:
        return Path(file_path).expanduser().read_text(encoding="utf-8")
    return body or ""


def escape_applescript(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def build_script(title: str, note: str) -> str:
    title_esc = escape_applescript(title)
    note_esc = escape_applescript(note)
    return f'''
tell application "Bear" to activate

tell application "System Events"
    keystroke "f" using command down
    delay 0.3
    keystroke "{title_esc}"
    delay 0.8
    key code 36
    delay 0.8
    keystroke "a" using {{command down}}
    delay 0.2
    key code 124 using {{command down}}
    delay 0.2
    keystroke return
    keystroke "{note_esc}"
end tell
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--body")
    ap.add_argument("--file")
    args = ap.parse_args()

    note = read_note(args.file, args.body)
    script = build_script(args.title, note)
    subprocess.run(["osascript", "-e", script], check=True)
    print("OK")

if __name__ == "__main__":
    main()
