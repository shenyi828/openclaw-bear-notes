#!/usr/bin/env python3
import re
from pathlib import Path
from typing import Dict, List, Tuple

WORKSPACE = Path('/Users/yizhitan/.openclaw/workspace')
PSY_DIR = WORKSPACE / 'vector-test/data/bear/psychology'
MANUAL_DIR = WORKSPACE / 'vector-test/data/manual'

CATEGORY_MAP: Dict[str, List[str]] = {
    '心理学': ['基础心理学','发展心理学','社会心理学','认知心理学','生物心理学','临床与咨询心理学','进化心理学','健康心理学','工业与组织心理学','环境心理学','跨文化心理学','神经心理学','实验心理学','教育心理学'],
    '基础心理学': ['元认知能力','认知负荷理论与信息单元','认知经济性','选择性注意（Selective Attention）','过滤器理论（Filter Theory）','鸡尾酒会效应（Cocktail Party Effect）','赫布法则（Hebb\'s Rule）','人类记忆类型深入解析','人类学习效率与技能掌握能力的多维解析'],
    '社会心理学': ['归因偏差（Attribution Bias）','社会促进效应','阿希从众实验','米尔格拉姆服从实验','斯坦福监狱实验','认知失调理论','认知失调理论在生活与商业中的实际案例','情绪勒索（Emotional Blackmail）','情感责任外包','关系中的隐性控制','暗黑三联征（Dark Triad）'],
    '发展心理学': ['边界感','边界感（增强版）','特定恐惧症'],
    '认知心理学': ['达克效应','认知闭合（Cognitive Closure）','过度分析瘫痪（Analysis Paralysis）','过度调整自我认知','自我矛盾理论','词语联想'],
    '行为主义（Behaviorism）': ['阿希从众实验','米尔格拉姆服从实验'],
    '人本主义（Humanism）': ['边界感','边界感（增强版）'],
    '精神分析（Psychoanalysis）': ['房树人','心理投射游戏','词语联想'],
}

DESC: Dict[str, str] = {
    '基础心理学': '心理学的基础层，负责承接感知、记忆、学习、思维、情绪等基本心理机制。',
    '发展心理学': '聚焦个体在不同生命阶段中的变化，并连接依恋、认同、发展任务等主题。',
    '社会心理学': '聚焦个体如何在关系、群体与规范中形成判断、态度与行为。',
    '认知心理学': '聚焦注意、记忆、推理、决策与语言等内部信息加工过程。',
    '生物心理学': '研究神经系统、生理机制与心理活动之间的关系。',
    '临床与咨询心理学': '连接诊断、干预、治疗与心理支持的实践应用分支。',
    '进化心理学': '从适应与自然选择角度解释心理与行为倾向。',
    '健康心理学': '研究压力、习惯、行为与身心健康之间的互动。',
    '工业与组织心理学': '将心理学用于工作、团队、领导与组织效能场景。',
    '环境心理学': '关注空间、噪音、自然与建成环境对人的影响。',
    '跨文化心理学': '比较不同文化背景下心理规律的差异与共性。',
    '神经心理学': '关注脑损伤、神经系统变化与认知行为功能的对应关系。',
    '实验心理学': '通过实验方法研究心理机制，为其他分支提供方法论支持。',
    '教育心理学': '研究学习、教学与学生发展中的心理机制。',
    '元认知能力': '对自己思维过程进行觉察、监控和调节的能力。',
    '认知负荷理论与信息单元': '解释工作记忆容量有限时，信息复杂度如何影响学习效果。',
    '认知经济性': '说明人类如何以较低认知成本快速形成判断，也因此容易产生偏差。',
    '选择性注意（Selective Attention）': '说明有限注意资源如何优先处理与目标相关的信息。',
    '过滤器理论（Filter Theory）': '提出注意系统会像过滤器一样筛选信息进入进一步加工。',
    '鸡尾酒会效应（Cocktail Party Effect）': '说明人在嘈杂环境中仍能锁定关键刺激，如自己的名字。',
    '赫布法则（Hebb\'s Rule）': '概括学习与神经连接增强之间的经典关系。',
    '人类记忆类型深入解析': '系统梳理不同记忆系统及其分工方式。',
    '人类学习效率与技能掌握能力的多维解析': '从练习结构、反馈质量和认知资源看学习效率。',
    '归因偏差（Attribution Bias）': '解释人们为何会系统性高估内因、低估情境因素。',
    '社会促进效应': '说明他人在场会改变个体表现水平。',
    '阿希从众实验': '经典展示群体压力如何扭曲个体判断。',
    '米尔格拉姆服从实验': '经典展示权威命令如何提高服从。',
    '斯坦福监狱实验': '显示情境与角色如何迅速塑造行为。',
    '认知失调理论': '解释人在态度与行为冲突时如何调整认知以缓解不适。',
    '认知失调理论在生活与商业中的实际案例': '把认知失调放进真实决策和商业情境中理解。',
    '情绪勒索（Emotional Blackmail）': '讨论关系中如何借由恐惧、内疚和责任压力实现隐性操控。',
    '情感责任外包': '描述一个人把自己的情绪稳定任务转移给关系另一方。',
    '关系中的隐性控制': '讨论没有明确命令却仍然发生控制的关系结构。',
    '暗黑三联征（Dark Triad）': '概括三种高操控性人格特质。',
    '边界感': '说明个体如何区分自我与他人、责任与侵入。',
    '边界感（增强版）': '从关系结构和主体性角度进一步展开边界感。',
    '特定恐惧症': '描述对特定对象或情境的持续强烈恐惧。',
    '达克效应': '解释能力不足者为何更容易高估自己。',
    '认知闭合（Cognitive Closure）': '解释人们为何急于摆脱不确定感并快速下结论。',
    '过度分析瘫痪（Analysis Paralysis）': '描述权衡过多导致行动停滞的状态。',
    '过度调整自我认知': '说明个体如何在外界反馈下不断扭曲自我判断。',
    '自我矛盾理论': '研究不同自我表征不一致时带来的紧张感。',
    '词语联想': '通过联想内容观察潜在认知与情绪连接。',
    '房树人': '投射性绘画测验之一，可辅助观察心理状态。',
    '心理投射游戏': '通过模糊刺激与解释方式观察投射过程。',
}

SKIP_MANUAL = {'Bear-标签与目录规范','Bear-知识库与协作方法论','今日复盘｜Bear × 小安 × 向量库打通全过程','心理学目录-待追加段落','心理学目录-新增链接片段','心理学目录-更新稿','心理学目录-漏项补全清单','情绪勒索（Emotional Blackmail）-优化稿','边界感（格式增强版）'}


def canonical_manual_title(path: Path) -> str:
    title = path.stem
    if title.endswith('-优化稿'):
        title = title[:-4]
    return title


def collect_notes() -> Dict[str, Path]:
    notes: Dict[str, Path] = {}
    for p in PSY_DIR.glob('*.md'):
        notes[p.stem] = p
    preferred = {
        '情绪勒索（Emotional Blackmail）': MANUAL_DIR / '情绪勒索（Emotional Blackmail）-优化稿.md',
        '边界感': MANUAL_DIR / '边界感（增强版）.md',
        '心理学目录': MANUAL_DIR / '心理学目录-更新稿.md',
        '情感责任外包': MANUAL_DIR / '情感责任外包.md',
        '关系中的隐性控制': MANUAL_DIR / '关系中的隐性控制.md',
    }
    for t, p in preferred.items():
        if p.exists():
            notes[t] = p
    return notes


def strip_old_related_block(text: str) -> str:
    marker = '\n## 关联笔记\n'
    if marker in text:
        return text.split(marker, 1)[0].rstrip() + '\n'
    return text.rstrip() + '\n'


def build_related_block(title: str, links: List[str]) -> str:
    if not links:
        return ''
    lines = ['## 关联笔记', '']
    for link in links:
        desc = DESC.get(link, '与本篇相关，建议结合定义、机制、案例与应用一起理解。')
        lines.append(f'- [[{link}]]：{desc}')
    return '\n'.join(lines) + '\n'


def append_related(path: Path, title: str, links: List[str]) -> None:
    text = path.read_text(encoding='utf-8')
    text = strip_old_related_block(text)
    text = text.rstrip() + '\n\n' + build_related_block(title, links)
    path.write_text(text, encoding='utf-8')


def main() -> None:
    notes = collect_notes()
    for title, links in CATEGORY_MAP.items():
        if title in notes:
            append_related(notes[title], title, [x for x in links if x in notes])

if __name__ == '__main__':
    main()
