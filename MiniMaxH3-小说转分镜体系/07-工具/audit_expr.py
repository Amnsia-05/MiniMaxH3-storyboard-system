import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# 用法: python audit_expr.py <SKILL.md 路径>
# 作用: 扫描全文例句，找出"违反了本文其他章节硬规则"的写法
#       （主结论改了、散落在别处的旧例句/旧措辞没跟着改）
# 复用: 改 BODY 白名单 + pats 正则，换成你自己 skill 的硬规则
#
# 极性判定（由 skill-voice 提出改进）:
#   旧版只看"匹配位置之前的同一行"有没有 ❌ —— 但代码块里 ❌/✅ 常独立成行，
#   导致真正的反例被误判成正例。新版维护"最近一次极性标记"向下沿用 HOLD 行。
#   注意: 沿用只是【降级为待扫一眼】，不是静默丢弃，避免漏掉真违规。

HOLD = 6

p = sys.argv[1] if len(sys.argv) > 1 else r'C:/Users/Amnesia/.workbuddy/skills/h3-expression-psych/SKILL.md'
lines = open(p, encoding='utf-8').read().split('\n')

BODY = re.compile(
    r'\b(cheek|cheeks|hand|hands|wrist|wrists|shoulder|shoulders|knee|knees|ear|ears|'
    r'eye|eyes|arm|arms|leg|legs|foot|feet|ankle|ankles|elbow|elbows|hip|hips|palm|palms|'
    r'finger|fingers|thumb|thumbs|collar|lapel|pocket|pockets|sleeve|sleeves|temple|temples|'
    r'jaw|side|brow|brows|nostril|nostrils)\b', re.I)

pats = {
    'A_视线方向变化': r'\bgaze (drifts|rises|drops|moves|shifts|falls|lifts|sweeps|travels|wanders)|gaze (to|toward|towards|across|past|down|up)\b|\blooks (away|down|up|toward|towards)\b|\bglances?\b|\bturns? her head\b',
    # 注意: 不含 widen —— 睁大眼是眼睑开合，不是眼球转动，且 `eyes open wide` 是本文推荐写法
    'B_纯眼球转动': r'\b(her|his) eyes (move|dart|roll|shift|flick)|\brolls (her|his) eyes\b|\bpupils? dilate',
    'C_角色左右': r'\b(her|his) (left|right)\b',
    'D_过程类表情': r'\btears? form|\bbegins? to (cry|sob|weep|tremble|shake)|\bstarts? to (cry|sob|weep)|\bpupils? dilate|\bher face folds\b',
    'E_情绪名词副词': r'\b(angry|sad|shocked|furiously|happily|nervously|afraid|scared|emotional|dramatic emotional)\b',
    'F_while_as并发': r'\bwhile \b|,\s*as (she|he)\b',
    'G_从无到有': r'\btears? (form|well|gather|appear|spring)|\bbegins? to\b|\bstarts? to\b',
}

last_mark, last_mark_line = None, -HOLD * 2

def polarity(i, pos):
    """返回 True=反例(可豁免), False=正例(需审)"""
    seg = lines[i - 1][:pos] if pos else lines[i - 1]
    if '❌' in seg:
        return True, '行内'
    if '✅' in seg:
        return False, ''
    if last_mark is not None and (i - last_mark_line) <= HOLD:
        return last_mark, f'沿用{i - last_mark_line}行前'
    return False, ''

hits, exempt = [], []
for i, ln in enumerate(lines, 1):
    if '❌' in ln:
        last_mark, last_mark_line = True, i
    elif '✅' in ln:
        last_mark, last_mark_line = False, i

    if '`' not in ln and '"' not in ln:
        continue
    for name, pat in pats.items():
        m = re.search(pat, ln, re.I)
        if not m:
            continue
        if name == 'C_角色左右' and BODY.search(ln[m.end():m.end() + 40]):
            continue
        neg, why = polarity(i, m.start())
        row = (i, name, why, ln.strip()[:175])
        (exempt if neg else hits).append(row)
        break

def dump(rows, title):
    print(f'\n########## {title}  ({len(rows)}) ##########')
    for name in pats:
        sub = [r for r in rows if r[1] == name]
        if not sub:
            continue
        print(f'\n===== {name}  ({len(sub)}) =====')
        for i, nm, why, ln in sub:
            tag = f'<{why}>' if why else ''
            print(f'{i}\t{tag}\t{ln}')

dump(hits, '需人工审（正例/无标记）')
dump(exempt, '自动豁免（反例）——仅列计数，建议扫一眼确认未被误豁免')

print(f'\n---- 合计: 需审 {len(hits)} / 豁免 {len(exempt)} ----')
