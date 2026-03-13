#!/usr/bin/env python3
import argparse
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

WORKSPACE = Path('/Users/yizhitan/.openclaw/workspace')
MANUAL_DIR = WORKSPACE / 'vector-test/data/manual'
BEAR_DIR = WORKSPACE / 'vector-test/data/bear/psychology'
DEFAULT_VAULT = Path('/Users/yizhitan/Documents/ObsidianVaults/our-obsidian-notes')
DEFAULT_TARGET = DEFAULT_VAULT / '博闻强记/心理学'

MANUAL_PREFERRED = {
    '边界感': '边界感（增强版）.md',
    '情绪勒索（Emotional Blackmail）': '情绪勒索（Emotional Blackmail）-优化稿.md',
    '心理学目录': '心理学目录-更新稿.md',
}

SKIP_MANUAL = {
    'Bear-标签与目录规范',
    'Bear-知识库与协作方法论',
    '今日复盘｜Bear × 小安 × 向量库打通全过程',
    '心理学目录-待追加段落',
    '心理学目录-新增链接片段',
    '心理学目录-更新稿',
    '心理学目录-漏项补全清单',
    '情绪勒索（Emotional Blackmail）-优化稿',
    '边界感（格式增强版）',
}


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def normalize_title_from_path(path: Path) -> str:
    stem = path.stem
    if stem.endswith('-优化稿'):
        stem = stem[:-4]
    return stem


def ensure_frontmatter(title: str, body: str) -> str:
    if body.startswith('---\n'):
        return body
    tags = ['博闻强记/心理学']
    fm = [
        '---',
        f'title: "{title}"',
        'tags:',
    ]
    fm.extend([f'  - "{t}"' for t in tags])
    fm.append('source: "bear-sync"')
    fm.append('---\n')
    return '\n'.join(fm) + body


def collect_sources() -> Dict[str, Path]:
    chosen: Dict[str, Path] = {}

    for p in sorted(BEAR_DIR.glob('*.md')):
        chosen[normalize_title_from_path(p)] = p

    for canonical, fname in MANUAL_PREFERRED.items():
        p = MANUAL_DIR / fname
        if p.exists():
            chosen[canonical] = p

    for p in sorted(MANUAL_DIR.glob('*.md')):
        title = normalize_title_from_path(p)
        if title in SKIP_MANUAL:
            continue
        if title not in chosen:
            chosen[title] = p

    return chosen


def sync(vault: Path, target: Path) -> Tuple[int, int, List[str]]:
    target.mkdir(parents=True, exist_ok=True)
    chosen = collect_sources()
    created = 0
    updated = 0
    names = []

    for title, src in sorted(chosen.items()):
        dst = target / f'{title}.md'
        body = read_text(src)
        content = ensure_frontmatter(title, body)
        if not dst.exists():
            dst.write_text(content, encoding='utf-8')
            created += 1
        else:
            old = read_text(dst)
            if old != content:
                dst.write_text(content, encoding='utf-8')
                updated += 1
        names.append(title)
    return created, updated, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', default=str(DEFAULT_VAULT))
    ap.add_argument('--target-dir', default=str(DEFAULT_TARGET))
    args = ap.parse_args()

    vault = Path(args.vault).expanduser()
    target = Path(args.target_dir).expanduser()
    created, updated, names = sync(vault, target)
    print(f'vault={vault}')
    print(f'target={target}')
    print(f'created={created}')
    print(f'updated={updated}')
    print('synced_titles=')
    for n in names:
        print(n)

if __name__ == '__main__':
    main()
