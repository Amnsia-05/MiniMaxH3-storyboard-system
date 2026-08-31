#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H3 提示词体系 · 跨文件硬规则自查脚本

用途：把「硬规则」写成可执行判定式，扫描全文例句，找出"正面范例违反本文规则"的地方。
背景：2026-08-30 skill-expression 连抓两轮，每轮都以为扫干净了，第二轮又出 3 处。
      结论是光靠人读一定漏，必须脚本化。

用法：
    python audit_rules.py                  # 扫默认文件集
    python audit_rules.py <文件1> <文件2>  # 扫指定文件

输出：[疑似违规] / [正例需审] / [豁免]
      - 匹配位置前若出现 ❌ / 禁止 / 反例 / 错 等标记，判为"反例"，豁免
      - 其余标 [疑似违规] 或 [正例需审]，需人工判定

扩展：在 RULES 里加规则即可，每条 = (名称, 正则, 豁免关键词列表)
"""

import re
import sys
import pathlib
import glob

# ---- 反例上下文标记：出现这些即视为"这里是在举反例"，豁免 ----
ANTI_MARKS = ["❌", "✗", "禁", "反例", "错误", "不推荐", "避免", "别写", "勿", "避免用"]

# ---- 已知合法例外（白名单片段） ----
WHITELIST = [
    "while his lips remain completely closed",   # 官方画外音成对句，描述持续状态
    "while her lips remain completely closed",
    "while their lips remain completely closed",
]

# ---- 硬规则集 ----
RULES = [
    (
        "R1_while并联主体动作",
        # while + 两个动作性动词（人/身体部位做主语）
        r"\b(?:she|he|they|her|his|the \w+)\b[^.\n]{0,60}?\bwhile\b[^.\n]{0,80}?\b\w+ing\b",
        [],
    ),
    (
        "R2_裸名词否定_中文",
        r"(?:画面内?|画面任意位置)?[^，。；\n]{0,12}不(?:出现|显示)[^，。；\n]{0,16}",
        [],
    ),
    # R3 分四个子模式：大小写 + 名词否定 + 否定句形式
    # （2026-08-30 h3-antibug 自查漏扫 4 处的教训：只扫小写 no [a-z]，
    #   漏了句首大写 No X、以及 does not X 这类否定句形式）
    (
        "R3a_裸名词否定_小写no",
        r"\bno\s+(?:text|letters?|numbers?|logos?|watermarks?|subtitles?|captions?|extra|deformed|mutated|six|pouring|smoking|splashing)\b[^.\n]{0,40}",
        [],
    ),
    (
        "R3b_裸名词否定_句首大写No",
        r"(?:^|[.\s])No\s+(?:text|letters?|numbers?|logos?|watermarks?|subtitles?|captions?|extra|new|deformed|mutated|six|pouring|smoking|splashing|duplicated|melting)\b[^.\n]{0,60}",
        [],
    ),
    # 注意：只扫 does/should/will not，不扫 "Do not"。
    # 因为 "Do not ..." 是本体系**唯一允许**的否定收边句式（每条提示词最多 1 句），
    # 扫它会产生大量噪音。真正可疑的是正文里的描述性否定（如 `the table does not deform`）。
    (
        "R3c_描述性否定_does not / should not",
        r"\b(?:does|should|will)\s+not\s+\w+",
        [],
    ),
    (
        "R3d_否定_not+名词",
        r"\bnot\s+(?:text|letters?|numbers?|logos?|watermarks?|extra|deformed|mutated|six)\b",
        [],
    ),
    (
        "R4_台词内双引号",
        r"<d>\s*\[[^\]]+\]\s*[\"“”]",
        [],
    ),
    (
        "R5_无配乐写no music",
        r"non_diegetic_music\s*:\s*no music",
        [],
    ),
    (
        "R6_Hailuo23旧规格",
        r"(?<!7)2000\s*字符|6\s*[–\-]\s*10\s*秒|全系不生成音频|不生成音频",
        [],
    ),
]

DEFAULT_FILES = (
    sorted(glob.glob("C:/Users/Amnesia/.workbuddy/skills/h3-*/SKILL.md"))
    + ["C:/Users/Amnesia/.workbuddy/skills/minimax-h3-storyboard/SKILL.md"]
    + ["MiniMaxH3-小说转分镜-完整模板.md"]
)


def is_anti_context(line: str) -> bool:
    """
    整行是否有反例标记。
    2026-08-30 教训：原来只看匹配位置前 60 字符，表格行里 ❌ 在行首（>60 字符外）会漏判。
    改为整行判断——表格的一行通常只有一种性质，整行判定的误判代价可接受。
    """
    return any(m in line for m in ANTI_MARKS)


def is_explanatory(line: str) -> bool:
    """说明性/教学性文字（非可复制示例），通常含这些特征"""
    return any(k in line for k in ["判定", "说明", "为什么", "原理", "机制", "注：", "注:", "【", "见 §", "见主模板"])


def is_checklist(line: str) -> bool:
    """
    检查清单条目（□ / - [ ]）—— 清单里常出现"Do not"是**引用规则**，
    不是提示词里的实际句子。2026-08-30 误报过一次。
    """
    s = line.lstrip()
    return s.startswith("□") or s.startswith("- [") or s.startswith("* [")


def scan_do_not_blocks(text: str) -> list:
    """
    块级检查：每个代码块内的 `Do not` 是否超过 1 句。
    本体系硬规则是「每条提示词最多 1 句 Do not」，所以按代码块计数才有意义。
    """
    lines = text.split("\n")
    out = []
    in_block = False
    start = 0
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if not in_block:
                in_block = True
                start = i
            else:
                # 只统计"提示词正文"行：排除清单条目与说明性文字
                body_lines = [
                    ln for ln in lines[start:i]
                    if not is_checklist(ln) and not is_explanatory(ln)
                ]
                # 按 [Shot N] 分段计数——规则是"每镜 1 句"，不是"每块 1 句"。
                # 一个三镜示例块本就该有 3 句 Do not。2026-08-30 修正。
                segs, cur = [], []
                for ln in body_lines:
                    if re.search(r"\[Shot\s*\d+\]", ln) and cur:
                        segs.append("\n".join(cur))
                        cur = [ln]
                    else:
                        cur.append(ln)
                if cur:
                    segs.append("\n".join(cur))
                for off, seg in enumerate(segs):
                    n = len(re.findall(r"\bDo\s+not\b", seg))
                    if n > 1:
                        out.append((start, f"第 {off+1} 段含 {n} 句 Do not"))
                in_block = False
    return out


def scan(path: str) -> int:
    p = pathlib.Path(path)
    if not p.exists():
        return 0
    text = p.read_text(encoding="utf-8")
    lines = text.split("\n")
    name = p.parent.name if p.parent.name.startswith("h3-") or "storyboard" in p.parent.name else p.name

    total = 0
    for rule_name, pat, _ in RULES:
        rx = re.compile(pat, re.I)
        hits = []
        for ln, line in enumerate(lines, 1):
            for m in rx.finditer(line):
                seg = line[m.start():m.end()]
                if any(w.lower() in seg.lower() for w in WHITELIST):
                    continue
                if is_anti_context(line):
                    continue
                if is_checklist(line):
                    continue
                if is_explanatory(line):
                    continue
                hits.append((ln, seg.strip()))
        if hits:
            print(f"\n### {name} · {rule_name}  ({len(hits)})")
            for ln, seg in hits[:8]:
                print(f"  {ln:5d}  {seg[:150]}")
            if len(hits) > 8:
                print(f"  ... 另有 {len(hits)-8} 处")
            total += len(hits)

    blocks = scan_do_not_blocks(text)
    if blocks:
        print(f"\n### {name} · R3e_同一代码块内 Do not 超过 1 句  ({len(blocks)})")
        for ln, n in blocks[:8]:
            print(f"  代码块起始行 {ln:5d}  {n}  ← 每段应为 1 句")
        total += len(blocks)
    return total


def main():
    files = sys.argv[1:] or DEFAULT_FILES
    grand = 0
    for f in files:
        grand += scan(f)
    print(f"\n===== 疑似命中总数: {grand} =====")
    print("说明：[疑似]需人工判定；已自动豁免反例上下文与白名单。")


if __name__ == "__main__":
    main()
