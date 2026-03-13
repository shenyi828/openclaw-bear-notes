#!/usr/bin/env python3
from pathlib import Path
from typing import Dict, List
import re

ROOT = Path('/Users/yizhitan/.openclaw/workspace/vector-test/data/bear/psychology')

MAJOR_HUBS: Dict[str, List[str]] = {
    '心理学': ['基础心理学','发展心理学','社会心理学','认知心理学','生物心理学','临床与咨询心理学','进化心理学','健康心理学','工业与组织心理学','环境心理学','跨文化心理学','神经心理学','实验心理学','教育心理学','联结主义（Connectionism）','结构主义（Structuralism）','功能主义（Functionalism）','存在主义（Existentialism）','行为主义（Behaviorism）','人本主义（Humanism）','精神分析（Psychoanalysis）','建构主义（Constructivism）'],
    '基础心理学': ['认知心理学','实验心理学','生物心理学','教育心理学','联结主义（Connectionism）','功能主义（Functionalism）'],
    '发展心理学': ['教育心理学','社会心理学','临床与咨询心理学','人本主义（Humanism）','精神分析（Psychoanalysis）'],
    '社会心理学': ['临床与咨询心理学','认知心理学','进化心理学','行为主义（Behaviorism）','人本主义（Humanism）'],
    '认知心理学': ['基础心理学','实验心理学','生物心理学','教育心理学','联结主义（Connectionism）','建构主义（Constructivism）'],
    '生物心理学': ['神经心理学','基础心理学','认知心理学','实验心理学','进化心理学'],
    '临床与咨询心理学': ['精神分析（Psychoanalysis）','人本主义（Humanism）','行为主义（Behaviorism）','发展心理学','社会心理学'],
    '进化心理学': ['社会心理学','生物心理学','基础心理学','功能主义（Functionalism）'],
    '健康心理学': ['临床与咨询心理学','生物心理学','社会心理学'],
    '工业与组织心理学': ['社会心理学','认知心理学','健康心理学'],
    '环境心理学': ['社会心理学','健康心理学','跨文化心理学'],
    '跨文化心理学': ['社会心理学','发展心理学','环境心理学'],
    '神经心理学': ['生物心理学','认知心理学','临床与咨询心理学'],
    '实验心理学': ['基础心理学','认知心理学','生物心理学','社会心理学'],
    '教育心理学': ['发展心理学','认知心理学','建构主义（Constructivism）','基础心理学','人本主义（Humanism）'],
    '联结主义（Connectionism）': ['认知心理学','基础心理学','生物心理学','建构主义（Constructivism）'],
    '结构主义（Structuralism）': ['功能主义（Functionalism）','行为主义（Behaviorism）','心理学'],
    '功能主义（Functionalism）': ['结构主义（Structuralism）','行为主义（Behaviorism）','进化心理学','教育心理学'],
    '存在主义（Existentialism）': ['人本主义（Humanism）','精神分析（Psychoanalysis）','临床与咨询心理学'],
    '行为主义（Behaviorism）': ['功能主义（Functionalism）','认知心理学','教育心理学','临床与咨询心理学'],
    '人本主义（Humanism）': ['存在主义（Existentialism）','临床与咨询心理学','教育心理学','精神分析（Psychoanalysis）'],
    '精神分析（Psychoanalysis）': ['人本主义（Humanism）','存在主义（Existentialism）','临床与咨询心理学','发展心理学'],
    '建构主义（Constructivism）': ['教育心理学','认知心理学','联结主义（Connectionism）','人本主义（Humanism）'],
}

DESC: Dict[str, str] = {
    '心理学': '整个知识库的总枢纽，用来统摄主要学科分支与核心流派。',
    '基础心理学': '承接感知、记忆、学习、思维与情绪等基本心理机制。',
    '发展心理学': '关注个体在不同生命阶段中的变化与发展任务。',
    '社会心理学': '研究个体如何在关系、群体与规范中形成判断与行为。',
    '认知心理学': '研究注意、记忆、推理、语言与决策等信息加工过程。',
    '生物心理学': '从神经、生理和遗传层面解释心理活动的基础。',
    '临床与咨询心理学': '把评估、理解、干预与支持放进现实困扰中处理的实践枢纽。',
    '进化心理学': '从适应与自然选择角度解释心理与行为倾向。',
    '健康心理学': '连接心理状态、行为习惯与身体健康结果。',
    '工业与组织心理学': '把心理学应用到工作、团队与组织效率场景。',
    '环境心理学': '研究空间与环境条件如何塑造人的感受与行为。',
    '跨文化心理学': '比较不同文化背景下心理规律的差异与共性。',
    '神经心理学': '关注脑损伤、神经系统变化与认知行为功能之间的对应。',
    '实验心理学': '通过实验设计与控制变量研究心理机制。',
    '教育心理学': '研究学习、教学与学生发展中的心理机制。',
    '联结主义（Connectionism）': '借由神经网络式模型解释认知表征与学习过程。',
    '结构主义（Structuralism）': '强调从结构层面理解意识、文化或知识系统。',
    '功能主义（Functionalism）': '关注心理活动的功能及其适应环境的作用。',
    '存在主义（Existentialism）': '围绕自由、责任、荒谬与意义展开对人的理解。',
    '行为主义（Behaviorism）': '强调可观察行为及其强化、惩罚与条件作用机制。',
    '人本主义（Humanism）': '强调人的主体性、潜能与自我实现。',
    '精神分析（Psychoanalysis）': '通过无意识、冲突与人格结构理解心理活动。',
    '建构主义（Constructivism）': '强调知识并非被动接收，而是在互动中主动建构。',
}


def protect(text: str):
    protected = {}
    def repl(m):
        k = f'__P{len(protected)}__'
        protected[k] = m.group(0)
        return k
    text = re.sub(r'\[\[[^\]]+\]\]', repl, text)
    return text, protected


def restore(text: str, protected):
    for k, v in protected.items():
        text = text.replace(k, v)
    return text


def add_in_body_links(text: str, title: str, links: List[str]) -> str:
    text, protected = protect(text)
    for link in sorted(links, key=len, reverse=True):
        if link == title:
            continue
        plain = re.sub(r'（.*?）', '', link)
        for candidate in [link, plain]:
            if not candidate or candidate == title:
                continue
            text = re.sub(rf'(?<!\[\[){re.escape(candidate)}(?!\]\])', f'[[{link}]]', text)
    return restore(text, protected)


def replace_related(text: str, links: List[str]) -> str:
    marker = '\n## 关联笔记\n'
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + '\n'
    lines = ['## 关联笔记', '']
    for link in links:
        lines.append(f'- [[{link}]]：{DESC[link]}')
    return text.rstrip() + '\n\n' + '\n'.join(lines) + '\n'


def process(title: str, links: List[str]) -> None:
    path = ROOT / f'{title}.md'
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
    links = [x for x in links if (ROOT / f'{x}.md').exists() and x in DESC]
    text = add_in_body_links(text, title, links)
    text = replace_related(text, links)
    path.write_text(text, encoding='utf-8')


def main():
    for title, links in MAJOR_HUBS.items():
        process(title, links)
    print('OK')

if __name__ == '__main__':
    main()
