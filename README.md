# bear-notes

A Bear.app note-writing skill for OpenClaw that turns conversations into structured long-term notes.

它的目标不是“临时写一段文本”，而是把聊天内容稳定沉淀成：
- 正式 Markdown 笔记
- Bear 中可维护的长期笔记
- 可继续检索、追加、导出的知识资产

> Status: public beta / early release

## 当前能力

- 将正文和标签格式化为 Bear 可接受内容
- 生成本地 Markdown 副本
- 通过 AppleScript 调起 Bear 新建笔记
- 通过 UI 自动化向已有 Bear 笔记追加内容（实验性，受系统语言/界面变化影响）
- 支持常见模板：概念卡、方法论、SOP、会议纪要、复盘
- 保留标签治理、双链克制、标题去重等规则

## 目录结构

- `SKILL.md`：触发和执行规则
- `scripts/`：可执行脚本
- `references/`：规则和升级思路
- `examples/`：示例 prompts
- `config.example.json`：可复制成你自己的配置

## 推荐用法

用户说：
- 把这段整理成 Bear 笔记
- 存到知识库
- 追加到已有 Bear 笔记
- 帮我写一篇心理学笔记并同步到 Bear

代理应优先：
1. 生成正式 Markdown
2. 判断标签和模板
3. 先写入 Bear，作为用户首要验收面
4. 再同步本地副本 / Obsidian / 其他检索层
5. 告知路径与状态

## 可执行脚本

### 1. 新建 Bear 笔记

```bash
./scripts/create_bear_note.py \
  --title "认知重评" \
  --tag "博闻强记/心理学" \
  --file /path/to/note.md
```

### 2. 生成本地 Markdown 笔记

```bash
./scripts/render_note.py \
  --title "认知重评" \
  --template concept \
  --tag "博闻强记/心理学" \
  --body-file /path/to/body.md \
  --out /path/to/output.md
```

### 3. 追加到已有 Bear 笔记（实验性）

```bash
./scripts/append_bear_note.py \
  --title "认知重评" \
  --file /path/to/appendix.md
```

> 说明：该能力当前依赖 Bear 前台界面与 macOS UI 自动化，系统语言、输入法、窗口焦点变化都可能影响稳定性。

### 4. 初步判断该新建还是追加

```bash
./scripts/decide_note_action.py --text "把这段会议纪要整理成 Bear 笔记"
```

### 5. 从正文粗略建议标题

```bash
./scripts/suggest_title.py --file /path/to/body.md
```

### 6. 主入口：自动建议标题 / 标签 / 新建或追加

```bash
./scripts/create_or_append_note.py \
  --file /path/to/body.md \
  --print-only
```

- 默认会：
  - 粗略建议标题（已做一版中文指令清洗）
  - 粗略推荐标签
  - 判断是 `create` 还是 `append`
  - 先渲染正式 Markdown
- 若不加 `--print-only`，会进一步尝试写入 Bear。

## Obsidian sync

A one-way psychology-note sync is now available:

```bash
./scripts/sync_psychology_to_obsidian.py
```

Default target:

```text
/Users/yizhitan/Documents/ObsidianVaults/our-obsidian-notes/博闻强记/心理学/
```

Current behavior:
- prefers optimized notes from `vector-test/data/manual/`
- falls back to Bear-exported psychology notes from `vector-test/data/bear/psychology/`
- keeps sync one-way into Obsidian
- writes files as Markdown compatible with Obsidian wikilinks
- can be paired with `autofill_psychology_index.py` to reduce missing index entries

### Related maintenance scripts

```bash
./scripts/autofill_psychology_index.py
./scripts/enrich_psychology_index_descriptions.py
./scripts/link_psychology_notes.py
./scripts/clean_obsidian_to_psychology_only.sh
```

### Psychology note structure

Recommended hierarchy:
- `心理学目录` = level 1 index
- stable domain/school/hub notes (学科 / 主义 / 流派) = level 2 hubs
- specific concepts / experiments / mechanisms / cases = child notes mounted under one or more hubs

Recommended note ending:

```md
## 关联笔记

- [[相关笔记A]]：一句说明它为什么和本篇相关
- [[相关笔记B]]：一句说明它提供了什么补充视角
```

Recommended default workflow after psychology note changes:
1. inspect the note body carefully
2. add meaningful in-body wikilinks for existing related notes
3. refresh the ending `## 关联笔记` block with concrete descriptions
4. write/update in Bear first for user review
5. update hub/index links if needed
6. run one-way sync into Obsidian
7. refresh local/vector source layers if applicable

Quality bar:
- do not settle for only end-of-note links
- do not use vague fallback descriptions in `## 关联笔记`
- prefer slower, batch-based review over low-quality bulk rewrites

## Installation

### For OpenClaw-style local skills

Clone or copy this repository into a local skills directory that your agent runtime can read.

Typical example:

```bash
git clone https://github.com/shenyi828/openclaw-bear-notes.git
```

Then place `bear-notes/` where your local agent runtime expects custom skills, or merge the folder into an existing `skills/` directory.

### For local development only

If you already have a local skill workspace, you do **not** need to download it again from GitHub just to keep using it. The GitHub repo is mainly the public source-of-truth for sharing and versioning.

## Requirements

This project currently assumes:

- macOS
- Bear.app installed
- `osascript` available
- an agent/runtime that can read `SKILL.md` and run local scripts

Experimental append support additionally depends on Bear front-end UI automation, so behavior may vary with:

- system language
- input method
- window focus
- UI layout changes

## Positioning vs official Bear skills

This repository is **not** trying to replace an official Bear integration.

Its focus is different:

- turn conversations into structured long-term notes
- keep a local Markdown backup
- enforce sane tag rules
- encourage controlled linking and note hygiene
- support a repeatable personal knowledge workflow

So a better mental model is:

> official Bear skills may expose Bear capabilities,
> while `bear-notes` tries to package a long-term Bear writing workflow.

## Open-source publishing notes

建议把个人路径、私有标签树、自动化细节做成配置项，不要硬编码在公共版里。

适合公开的：
- 触发逻辑
- 笔记模板
- 标签治理原则
- 执行脚本接口

更适合私有配置的：
- 默认标签树
- 本地 Bear 工作习惯
- 向量库路径
- 个人目录命名

## License

MIT.
