#!/usr/bin/env python3
import re
from pathlib import Path

ROOTS = [
    Path('/Users/yizhitan/.openclaw/workspace/vector-test/data/bear/psychology'),
    Path('/Users/yizhitan/.openclaw/workspace/vector-test/data/manual'),
]

SKIP = {
    'Bear-标签与目录规范',
    'Bear-知识库与协作方法论',
    '今日复盘｜Bear × 小安 × 向量库打通全过程',
    '心理学目录-待追加段落',
    '心理学目录-新增链接片段',
    '心理学目录-漏项补全清单',
}

def canonical_title(path: Path) -> str:
    title = path.stem
    if title.endswith('-优化稿'):
        title = title[:-4]
    return title

def normalize(path: Path) -> bool:
    title = canonical_title(path)
    if title in SKIP:
        return False
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    while lines and not lines[0].strip():
        lines.pop(0)

    consumed = 0
    while consumed < len(lines):
        s = lines[consumed].strip()
        if not s:
            consumed += 1
            continue
        if s.startswith('#'):
            body_title = s.lstrip('#').strip()
            if body_title == title:
                consumed += 1
                continue
        if s == '#博闻强记/心理学':
            consumed += 1
            continue
        break

    body = '\n'.join(lines[consumed:]).lstrip('\n')
    new = f'# {title}\n\n#博闻强记/心理学\n\n{body}'.rstrip() + '\n'
    changed = new != text
    if changed:
        path.write_text(new, encoding='utf-8')
    return changed

changed = 0
for root in ROOTS:
    for p in root.glob('*.md'):
        if normalize(p):
            changed += 1
print(changed)
