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
3. 保存本地副本
4. 写入 Bear
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
