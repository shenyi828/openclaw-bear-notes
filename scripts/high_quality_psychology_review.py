#!/usr/bin/env python3
from pathlib import Path
from typing import Dict, List
import re

WORKSPACE = Path('/Users/yizhitan/.openclaw/workspace')
PSY_DIR = WORKSPACE / 'vector-test/data/bear/psychology'

BATCHES: List[List[str]] = [
    ['基础心理学','认知心理学','发展心理学','生物心理学','教育心理学','精神分析（Psychoanalysis）'],
    ['社会心理学','临床与咨询心理学','建构主义（Constructivism）','心理学','行为主义（Behaviorism）','人本主义（Humanism）'],
]

BODY_LINKS: Dict[str, List[str]] = {
    '基础心理学': ['元认知能力','认知负荷理论与信息单元','选择性注意（Selective Attention）','过滤器理论（Filter Theory）','鸡尾酒会效应（Cocktail Party Effect）','赫布法则（Hebb\'s Rule）'],
    '认知心理学': ['达克效应','认知闭合（Cognitive Closure）','认知负荷理论与信息单元','认知经济性','选择性注意（Selective Attention）','鸡尾酒会效应（Cocktail Party Effect）'],
    '发展心理学': ['边界感','特定恐惧症'],
    '生物心理学': ['赫布法则（Hebb\'s Rule）','神经心理学与生物心理学的差异'],
    '教育心理学': ['建构主义（Constructivism）','元认知能力','认知负荷理论与信息单元'],
    '精神分析（Psychoanalysis）': ['房树人','心理投射游戏','词语联想'],
    '行为主义（Behaviorism）': ['阿希从众实验','米尔格拉姆服从实验'],
    '人本主义（Humanism）': ['边界感','边界感（增强版）'],
}

RELATED_DESC: Dict[str, str] = {
    '元认知能力': '帮助理解个体如何监控、调整与优化自己的思维过程。',
    '认知负荷理论与信息单元': '说明信息复杂度与工作记忆容量如何共同影响学习和理解。',
    '选择性注意（Selective Attention）': '展示注意资源如何优先投向目标信息。',
    '过滤器理论（Filter Theory）': '解释信息为什么会在进入更深加工前被筛选。',
    '鸡尾酒会效应（Cocktail Party Effect）': '是选择性注意在复杂环境中的经典现象。',
    '赫布法则（Hebb\'s Rule）': '从神经连接层面解释学习与记忆形成的基础机制。',
    '达克效应': '帮助理解能力评估偏差与错误自信的形成。',
    '认知闭合（Cognitive Closure）': '说明人为何会急于摆脱不确定并快速下判断。',
    '认知经济性': '帮助理解高效判断背后也可能伴随的系统性偏差。',
    '边界感': '连接发展、自我区分与关系互动中的责任边界问题。',
    '特定恐惧症': '提供一个具体临床困扰案例来连接发展与干预视角。',
    '神经心理学与生物心理学的差异': '帮助厘清两个相近领域的研究重心与方法差别。',
    '建构主义（Constructivism）': '提供教育场景下“知识如何形成”的核心理论支点。',
    '房树人': '作为投射性测验例子，帮助理解无意识材料的外显方式。',
    '心理投射游戏': '展示投射机制如何在较自由的表达任务中出现。',
    '词语联想': '是精神分析与潜在联想结构相关的经典切入口。',
    '阿希从众实验': '展示群体压力如何改变个体判断。',
    '米尔格拉姆服从实验': '展示权威命令如何影响服从行为。',
    '边界感（增强版）': '从更结构化角度展开边界感与主体性的关系。',
}


def protect_existing(text: str):
    protected = {}
    def repl(match):
        key = f'__P{len(protected)}__'
        protected[key] = match.group(0)
        return key
    text = re.sub(r'\[\[[^\]]+\]\]', repl, text)
    return text, protected


def restore(text: str, protected: Dict[str, str]) -> str:
    for k, v in protected.items():
        text = text.replace(k, v)
    return text


def add_body_links(text: str, title: str, links: List[str]) -> str:
    text, protected = protect_existing(text)
    for link in sorted(links, key=len, reverse=True):
        if link == title:
            continue
        plain = re.sub(r'（.*?）', '', link)
        for candidate in [link, plain]:
            if not candidate or candidate == title:
                continue
            text = re.sub(rf'(?<!\[\[){re.escape(candidate)}(?!\]\])', f'[[{link}]]', text)
    return restore(text, protected)


def replace_related_block(text: str, links: List[str]) -> str:
    marker = '\n## 关联笔记\n'
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + '\n'
    lines = ['## 关联笔记', '']
    for link in links:
        desc = RELATED_DESC[link]
        lines.append(f'- [[{link}]]：{desc}')
    return text.rstrip() + '\n\n' + '\n'.join(lines) + '\n'


def process_note(title: str) -> None:
    path = PSY_DIR / f'{title}.md'
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
    links = [l for l in BODY_LINKS.get(title, []) if l in RELATED_DESC]
    text = add_body_links(text, title, links)
    if links:
        text = replace_related_block(text, links)
    path.write_text(text, encoding='utf-8')


def main() -> None:
    for batch in BATCHES:
        for title in batch:
            process_note(title)
    print('OK')

if __name__ == '__main__':
    main()
