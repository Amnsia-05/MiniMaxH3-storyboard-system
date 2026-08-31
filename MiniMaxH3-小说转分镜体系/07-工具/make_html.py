# -*- coding: utf-8 -*-
"""
把主模板 md 编译成人类阅读版 HTML。
设计要点：用占位符替换而非 f-string，彻底避开 JS/CSS 花括号的转义问题。
产出：侧边定位导航 + 顶部定位 chips + 一键复制 + 官方格式速取卡 + 三个实时校验器。
"""
import re, html, pathlib, json, markdown

ROOT = pathlib.Path(r"C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44")
SRC = ROOT / "MiniMaxH3-小说转分镜-完整模板.md"
OUT = ROOT / "MiniMaxH3-模板.html"

md_text = SRC.read_text(encoding="utf-8")

# ---------- 1. md -> html ----------
body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "sane_lists"],
)

# ---------- 2. 标题加锚点 + 收集目录 ----------
toc = []
_seen = {}


def slugify(text):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text).strip("-").lower() or "sec"
    n = _seen.get(s, 0)
    _seen[s] = n + 1
    return s if n == 0 else f"{s}-{n}"


def heading_repl(m):
    level = int(m.group(1))          # ← 之前错写成 len()，导致标题全变 h1
    plain = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
    sid = slugify(plain)
    if level in (2, 3):
        toc.append((level, plain, sid))
    return f'<h{level} id="{sid}">{m.group(2)}</h{level}>'


body = re.sub(r"<h([1-6])>(.*?)</h\1>", heading_repl, body, flags=re.S)

# ---------- 3. 代码块加复制按钮 ----------
def pre_repl(m):
    esc = html.escape(m.group(1))
    return (
        '<div class="codewrap">'
        '<button class="copybtn" type="button">复制</button>'
        f"<pre><code>{esc}</code></pre>"
        f'<textarea class="rawcode" hidden>{esc}</textarea>'
        "</div>"
    )


body = re.sub(r"<pre><code>(.*?)</code></pre>", pre_repl, body, flags=re.S)

# ---------- 4. 侧边导航 + 顶部定位 chips ----------
nav, chips = [], []
for level, title, sid in toc:
    esc = html.escape(title)
    if level == 2:
        nav.append(f'<a class="toc-h2" href="#{sid}" data-t="{sid}">{esc}</a>')
        chips.append(f'<a class="chip" href="#{sid}" data-t="{sid}">{esc}</a>')
    else:
        nav.append(f'<a class="toc-h3" href="#{sid}" data-t="{sid}">{esc}</a>')
nav_html = "\n".join(nav)
chips_html = "\n".join(chips)

# ---------- 5. 官方格式速取卡 ----------
SNIPPETS = [
    ("指令首行 · I2VA",
     "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced."),
    ("指令首行 · FL2VA",
     "How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video."),
    ("指令首行 · L2VA",
     "How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video."),
    ("三核心字段骨架",
     "integrated_multimodal_description: [Shot 1] <风格>, <景别> frames <主体> at <画面位置>.\n"
     "[Shot 2] At 00:05.000, the camera cuts to ...\n"
     "[Shot 3] At 00:10.500, the shot switches to ...\n\n"
     "overall_soundscape: <1-4 句：环境音 / 物理音 / 非语言人声>\n\n"
     "non_diegetic_music: <1-3 句：乐器 / 速度 / 节奏；无配乐写 N/A>"),
    ("对白标签（<d> 不可省）",
     'The young woman with a quiet, breathy voice (S1) says: <d>[Chinese] 我早就知道了。</d>'),
    ("画外音旁白（两句成对）",
     'The man (S1) says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d> while his lips remain completely closed.'),
    ("跨镜连续台词 <scenetrans>",
     '...and says: <d>[Chinese] 我从来没想过 <scenetrans></d>\n\n'
     'At 00:05.000, ... her sentence continues seamlessly across the cut, <d>[Chinese] <scenetrans> 你会回来。</d>'),
    ("运镜公式",
     "The camera pushes in with small amplitude at slow speed toward the folded letter in her hands."),
    ("资产锁定四要素",
     "A small matte-gold signet ring on her RIGHT ring finger (worn on the right hand, not the left). "
     "The ring stays on the same finger for the entire shot, unchanged in size, colour and shape; "
     "it is never removed, never duplicated, never changes hand."),
    ("手机屏 · 干净底板（推荐）",
     "She holds a phone whose screen is a single uniform dark field; the only thing on the glass is a faint "
     "reflection of her face, and a soft cool-white glow from the screen lights her face from below."),
    ("手机屏 · 不可辨认（最实用）",
     "The screen content is softened by motion blur and reflection, illegible."),
    ("全局收尾约束",
     "Single continuous take, one camera move, locked-off framing, no camera shake. Exactly one person in frame, "
     "with two hands, five fingers on each hand, fingers gently curved and held together, natural joints. "
     "Her face, hairstyle, clothing color and every accessory stay identical from the first frame to the last. "
     "The lighting direction, color temperature and grade remain constant throughout. "
     "Every surface that could carry text is blank, plain and unmarked, showing only colour, material and reflection; "
     "the phone screen is a single uniform black field.\n"
     "Do not let anything on the screen animate, shift or change at any point in the shot."),
]

snips = []
for i, (title, code) in enumerate(SNIPPETS):
    snips.append(
        '<div class="snip">'
        f'<div class="snip-h"><span>{html.escape(title)}</span>'
        f'<button class="copybtn" type="button" data-snip="{i}">复制</button></div>'
        f'<pre><code>{html.escape(code)}</code></pre>'
        f'<textarea class="rawcode" hidden>{html.escape(code)}</textarea>'
        "</div>"
    )
snips_html = "\n".join(snips)

# ---------- 6. 工作区插入模板 ----------
TPL = {
    "t2va": (
        "integrated_multimodal_description: [Shot 1] <风格>, <景别> frames <主体> at <画面位置>，<朝向>，<开场姿态>.\n"
        "First <微小自然运动>, then <动作1，有明确终点>, then <动作2，有明确终点>.\n"
        "[可选对白] <说话人外观描述> with <音色与语气> (S1) says: <d>[Chinese] <逐字台词></d>\n"
        "<次级运动：发丝 / 衣摆 / 热气 / 光影>.\n"
        "The camera <官方运镜术语> with <small|large> amplitude at <slow|fast> speed <起点→终点>.\n"
        "By the end of the shot, <最终状态> + <最终构图>.\n"
        "Do not <最多一句否定收边>.\n\n"
        "[Shot 2] At 00:05.000, the camera cuts to ...\n"
        "[Shot 3] At 00:10.000, the shot switches to ...\n\n"
        "overall_soundscape: <1-4 句：环境音 / 物理动作音 / 非语言人声>\n\n"
        "non_diegetic_music: <1-3 句：乐器 / 速度 / 节奏 / 动态；无配乐写 N/A>"
    ),
    "i2va": (
        "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\n"
        "integrated_multimodal_description: [Shot 1] ..."
    ),
    "fl2va": (
        "How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the "
        "0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.\n\n"
        "integrated_multimodal_description: [Shot 1] ..."
    ),
    "l2va": (
        "How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the "
        "S.SS-second mark of the target video.\n\n"
        "integrated_multimodal_description: [Shot 1] ..."
    ),
    "lock": (
        "──── 共用锁定块（三镜逐字复制，禁止改写）────\n"
        "【角色身份串】同一名女性贯穿全部三镜：28 岁，鹅蛋脸，齐肩黑色直发发尾微内扣，深色眉毛，"
        "深棕色杏仁形眼睛，鼻梁挺直，唇形偏薄，下巴圆润，肤质自然，面部无任何痣或纹身。\n"
        "【服装与资产串】身穿米白色无标识圆领纯棉 T 恤，外搭深卡其色长款风衣，下身深蓝色直筒牛仔裤，"
        "白色低帮帆布鞋。左耳垂佩戴一只银色小圆环耳环，始终在左耳垂上，大小形状不变。全程不增加、不减少任何配饰。\n"
        "【场景与光位串】室内客厅，夜景。唯一光源为画面右侧落地灯，单一柔和主光自右前方 45° 打来，色温偏暖；"
        "背景简洁；画面内所有可能承载文字的表面都是素面、无标记的，只呈现颜色、材质与反光。\n"
        "【画风串】实拍电影感，写实风格，35mm 镜头，浅景深，青绿与琥珀色调，中等反差，自然皮肤质感，"
        "轻微胶片颗粒，无风格化滤镜，色温与反差在三镜内完全一致。\n"
        "───────────────────────────────────────────"
    ),
    "six": (
        "① <景别> frames <主体> at <画面位置>，<朝向>，<开场姿态>。\n"
        "② <微小自然运动>，然后<动作 1，有明确终点>，然后<动作 2，有明确终点>。\n"
        "③ <说话人外观描述> with <音色与语气> (S1) says: <d>[Chinese] <逐字台词></d>\n"
        "④ <次级运动：发丝 / 衣摆 / 光影 / 热气>；<画内物理音>。\n"
        "⑤ The camera <官方运镜术语> with <small|large> amplitude at <slow|fast> speed，<起点→终点>。\n"
        "⑥ <本镜光位差异，无差异则写\"光位与共用锁定块一致\">。\n"
        "⑦ By the end of the shot, <最终人物状态> + <最终构图>。\n"
        "   Do not <最多一句否定收边>。"
    ),
    "limit": (
        "Single continuous take, one camera move, locked-off framing, no camera shake. Exactly one person in frame, "
        "with two hands, five fingers on each hand, fingers gently curved and held together, natural joints. "
        "Her face, hairstyle, clothing color and every accessory stay identical from the first frame to the last. "
        "The lighting direction, color temperature and grade remain constant throughout. "
        "Every surface that could carry text is blank, plain and unmarked, showing only colour, material and "
        "reflection; the phone screen is a single uniform black field.\n"
        "Do not let anything on the screen animate, shift or change at any point in the shot."
    ),
}
tpl_js = "const TPL = " + json.dumps(TPL, ensure_ascii=False) + ";"

# ---------- 7. 页面骨架（占位符替换，不用 f-string） ----------
PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MiniMax H3 小说转分镜 · 完整模板</title>
<style>
:root{
  --bg:#0F0E0E; --bg2:#161514; --panel:rgba(255,255,255,0.045);
  --line:rgba(255,255,255,0.10); --line2:rgba(255,255,255,0.20);
  --tx:#F2F2F2; --tx2:#A8A8A8; --tx3:#727272;
  --gold:#E8C268; --ok:#7DD9A6; --warn:#E8C268; --bad:#E07866; --blue:#8FC0F0;
  --mono:"JetBrains Mono","Cascadia Mono","SFMono-Regular",Consolas,monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--bg);color:var(--tx);
  font:15px/1.78 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;}
a{color:var(--gold);text-decoration:none}

/* ---- 顶栏 ---- */
#bar{position:sticky;top:0;z-index:60;background:rgba(15,14,14,.94);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line)}
#barIn{max-width:1600px;margin:0 auto;padding:11px 22px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.brand{font-weight:700;font-size:14.5px;white-space:nowrap}
.brand em{font-style:normal;color:var(--gold)}
#chips{display:flex;gap:6px;flex-wrap:wrap;flex:1;min-width:0}
.chip{font-size:11.5px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;
  color:var(--tx2);background:var(--panel);white-space:nowrap;transition:.15s}
.chip:hover{border-color:var(--line2);color:var(--tx)}
.chip.on{border-color:var(--gold);color:var(--gold);background:rgba(232,194,104,.10)}

/* ---- 布局 ---- */
.wrap{max-width:1600px;margin:0 auto;display:grid;grid-template-columns:280px 1fr;align-items:start}
#side{position:sticky;top:52px;height:calc(100vh - 52px);overflow-y:auto;
  border-right:1px solid var(--line);padding:18px 10px 70px 18px}
#side .st{font-size:10.5px;letter-spacing:.18em;color:var(--tx3);margin:0 0 10px;font-weight:600}
.toc-h2{display:block;padding:6px 10px;margin:1px 0;font-size:13.5px;color:var(--tx);border-radius:5px;line-height:1.5}
.toc-h3{display:block;padding:4px 10px 4px 24px;font-size:12.5px;color:var(--tx2);border-radius:5px;line-height:1.5}
#side a:hover{background:var(--panel);color:var(--gold)}
#side a.on{background:rgba(232,194,104,.10);color:var(--gold)}
main{padding:26px 34px 140px;min-width:0}

/* ---- 按钮 ---- */
.btn{font-size:12px;padding:6px 12px;border:1px solid var(--line2);border-radius:6px;
  background:transparent;color:var(--tx);cursor:pointer;font-family:inherit;transition:.15s}
.btn:hover{background:var(--panel)}
.btn.gold{background:var(--gold);color:#1a1405;border-color:var(--gold);font-weight:600}
.btn.gold:hover{opacity:.86;color:#1a1405}

/* ---- 工具区 ---- */
.tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px;margin-bottom:30px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:16px}
.card h3{margin:0 0 4px;font-size:14.5px}
.card .hint{margin:0 0 12px;font-size:11.5px;color:var(--tx3);line-height:1.65}
.row{display:flex;gap:8px;align-items:center;margin-bottom:8px;flex-wrap:wrap}
.row label{font-size:12px;color:var(--tx2);min-width:46px}
input[type=number],input[type=text]{background:var(--bg);border:1px solid var(--line2);color:var(--tx);
  border-radius:6px;padding:5px 9px;font-size:13px;font-family:var(--mono);width:78px}
.out{margin-top:9px;font-size:12px;font-family:var(--mono);line-height:1.95;padding:9px 11px;
  border-radius:6px;background:var(--bg);border:1px solid var(--line)}
.out .g{color:var(--ok)} .out .w{color:var(--warn)} .out .b{color:var(--bad)} .out .n{color:var(--tx2)}

/* ---- 提示词工作区 ---- */
#lab{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:18px;margin-bottom:30px}
#lab h3{margin:0 0 4px;font-size:15px}
#lab .sub{margin:0 0 13px;font-size:11.5px;color:var(--tx3);line-height:1.65}
#prompt{width:100%;min-height:230px;background:#0a0a0a;color:#DCDCDC;border:1px solid var(--line);
  border-radius:8px;padding:13px;font:12.5px/1.7 var(--mono);resize:vertical}
#prompt:focus{outline:none;border-color:var(--gold)}
.meter{display:flex;align-items:center;gap:12px;margin-top:11px;flex-wrap:wrap}
.bar{flex:1 1 200px;height:6px;background:rgba(255,255,255,.09);border-radius:3px;overflow:hidden;min-width:160px}
.bar i{display:block;height:100%;width:0;background:var(--ok);transition:.2s}
.stats{font:12px/1.5 var(--mono);color:var(--tx2);white-space:nowrap}
.stats b{color:var(--tx)}
.zone{font-size:11.5px;margin-top:8px;color:var(--tx3)}
.zone.ok{color:var(--ok)} .zone.warn{color:var(--warn)} .zone.bad{color:var(--bad)}

/* ---- 速取卡 ---- */
.snips{display:grid;grid-template-columns:repeat(auto-fit,minmax(370px,1fr));gap:12px;margin-bottom:30px}
.snip{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;position:relative}
.snip-h{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 12px;
  border-bottom:1px solid var(--line);background:rgba(255,255,255,.03)}
.snip-h span{font-size:12.5px;font-weight:600}
.snip pre{margin:0;padding:12px;overflow-x:auto;background:transparent}
.snip code{font:12px/1.65 var(--mono);color:var(--blue);white-space:pre-wrap;word-break:break-word}

/* ---- 正文 ---- */
h1{font-size:29px;margin:6px 0 16px;scroll-margin-top:72px}
h2{font-size:21px;margin:46px 0 15px;padding-top:20px;border-top:1px solid var(--line);scroll-margin-top:72px}
h3{font-size:16.5px;margin:30px 0 10px;color:var(--gold);scroll-margin-top:72px}
h4{font-size:14.5px;margin:20px 0 8px;scroll-margin-top:72px}
p{margin:10px 0}
ul,ol{padding-left:22px} li{margin:5px 0}
blockquote{margin:14px 0;padding:11px 17px;border-left:3px solid var(--gold);
  background:var(--panel);color:var(--tx2);border-radius:0 8px 8px 0}
blockquote p{margin:5px 0}
hr{border:0;border-top:1px solid var(--line);margin:36px 0}
strong{color:#fff;font-weight:600}
code{background:rgba(255,255,255,.07);padding:2px 6px;border-radius:4px;font:12.5px/1.6 var(--mono);color:var(--gold)}
table{border-collapse:collapse;width:100%;margin:15px 0;font-size:13.5px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
th{background:var(--panel);font-weight:600;white-space:nowrap}
tbody tr:hover{background:rgba(255,255,255,.025)}

/* ---- 代码块 ---- */
.codewrap{position:relative;margin:15px 0}
pre{background:#0a0a0a;border:1px solid var(--line);border-radius:9px;padding:15px;overflow-x:auto;margin:0}
pre code{background:none;padding:0;color:#D6D6D6;font:12.5px/1.68 var(--mono)}
.copybtn{background:rgba(255,255,255,.09);color:var(--tx2);border:1px solid var(--line2);
  border-radius:6px;padding:3px 11px;font-size:11.5px;cursor:pointer;font-family:inherit;transition:.15s}
.copybtn:hover{background:var(--gold);color:#1a1405;border-color:var(--gold)}
.copybtn.done{background:var(--ok);color:#08281a;border-color:var(--ok)}
.codewrap>.copybtn{position:absolute;top:8px;right:8px;z-index:2}

#topbtn{position:fixed;right:22px;bottom:22px;width:40px;height:40px;border-radius:50%;
  background:var(--panel);border:1px solid var(--line2);color:var(--tx2);cursor:pointer;
  font-size:16px;display:none;align-items:center;justify-content:center}
#topbtn:hover{border-color:var(--gold);color:var(--gold)}
::-webkit-scrollbar{height:8px;width:8px}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.13);border-radius:4px}
@media(max-width:960px){
  .wrap{grid-template-columns:1fr}
  #side{display:none}
  main{padding:20px 18px 100px}
}
</style>
</head>
<body>

<div id="bar"><div id="barIn">
  <span class="brand">MiniMax <em>H3</em> · 小说转分镜模板</span>
  <div id="chips">__CHIPS__</div>
  <button class="btn" id="copyAll">复制全文</button>
</div></div>

<div class="wrap">
<nav id="side"><p class="st">目录 / CONTENTS</p>__NAV__</nav>

<main>
  <div class="tools">
    <div class="card">
      <h3>⏱ 时长校验</h3>
      <p class="hint">15 秒 3 镜的硬性校验：总和、硬下限、设计下限、信息镜、悬殊比。</p>
      <div class="row"><label>A 入镜</label><input type="number" id="tA" value="5" step="0.5" min="0"></div>
      <div class="row"><label>B 主镜</label><input type="number" id="tB" value="5" step="0.5" min="0"></div>
      <div class="row"><label>C 出镜</label><input type="number" id="tC" value="5" step="0.5" min="0"></div>
      <div class="out" id="tout"></div>
    </div>

    <div class="card">
      <h3>🎬 台词容量换算</h3>
      <p class="hint">语速 V=4.5 字/秒，占用率 ρ=0.70 → T ≈ 字数 ÷ 3.15（见模块四）。</p>
      <div class="row"><label>字数</label><input type="number" id="wNum" value="47" step="1" min="0"></div>
      <div class="row"><label>秒数</label><input type="number" id="wSec" value="15" step="0.5" min="0"></div>
      <div class="out" id="wout"></div>
    </div>

    <div class="card">
      <h3>📐 悬殊比参考</h3>
      <p class="hint">最长镜 ÷ 最短镜。建议 ≤2.5；超过则需评估重生成代价（§3.2.3）。</p>
      <div class="out" id="rout"></div>
    </div>
  </div>

  <section id="lab">
    <h3>⚡ H3 提示词工作区</h3>
    <p class="sub">点下方按钮插入模板 → 实时校验字数 → 一键复制，直接喂给海螺 H3。</p>
    <div class="row" style="margin-bottom:12px">
      <button class="btn" data-ins="t2va">T2VA 骨架</button>
      <button class="btn" data-ins="i2va">I2VA 首行</button>
      <button class="btn" data-ins="fl2va">FL2VA 首行</button>
      <button class="btn" data-ins="l2va">L2VA 首行</button>
      <button class="btn" data-ins="lock">共用锁定块</button>
      <button class="btn" data-ins="six">单镜六段</button>
      <button class="btn" data-ins="limit">限制词串</button>
    </div>
    <textarea id="prompt" placeholder="点上方按钮插入模板，或直接在此编辑…"></textarea>
    <div class="meter">
      <div class="bar"><i id="pbar"></i></div>
      <span class="stats" id="pstat">0 汉字</span>
      <button class="btn" id="clr">清空</button>
      <button class="btn gold" id="cp">一键复制</button>
    </div>
    <div class="zone" id="pzone"></div>
  </section>

  <h3 style="margin-top:34px">📋 官方格式速取卡（一键复制）</h3>
  <div class="snips">__SNIPS__</div>

__BODY__
</main>
</div>

<button id="topbtn" title="回到顶部">↑</button>

<script>
__TPLJS__

function cpText(t, btn){
  var done=function(){ if(btn){ var o=btn.textContent; btn.textContent='已复制';
    btn.classList.add('done'); setTimeout(function(){btn.textContent=o; btn.classList.remove('done');},1400);} };
  if(navigator.clipboard && window.isSecureContext){
    navigator.clipboard.writeText(t).then(done).catch(function(){fb(t,done);});
  } else fb(t,done);
}
function fb(t,done){
  var a=document.createElement('textarea'); a.value=t; a.style.position='fixed'; a.style.opacity='0';
  document.body.appendChild(a); a.select();
  try{ document.execCommand('copy'); done(); }catch(e){ alert('复制失败，请手动选择'); }
  document.body.removeChild(a);
}

document.addEventListener('click', function(e){
  var b=e.target.closest('.copybtn'); if(!b) return;
  var host = b.closest('.codewrap') || b.closest('.snip');
  var raw = host && host.querySelector('.rawcode');
  cpText(raw ? raw.value : (host ? host.querySelector('code').innerText : ''), b);
});

/* ---- 时长校验 ---- */
var tA=document.getElementById('tA'),tB=document.getElementById('tB'),tC=document.getElementById('tC');
var tout=document.getElementById('tout'), rout=document.getElementById('rout');
function chkT(){
  var v=[parseFloat(tA.value)||0, parseFloat(tB.value)||0, parseFloat(tC.value)||0];
  var s=v[0]+v[1]+v[2], mn=Math.min.apply(null,v), mx=Math.max.apply(null,v);
  var ratio = mn>0 ? (mx/mn) : 0;
  var L=[];
  L.push(Math.abs(s-15)<1e-9
    ? '<span class="g">✓ 总时长 '+s.toFixed(1)+'s = 15.0s</span>'
    : '<span class="b">✗ 总时长 '+s.toFixed(1)+'s ≠ 15.0s（差 '+(15-s).toFixed(1)+'s）</span>');
  L.push(v.every(function(x){return x>=1.5;})
    ? '<span class="g">✓ 每镜 ≥ 1.5s（硬下限）</span>'
    : '<span class="b">✗ 有镜头低于 1.5s 硬下限</span>');
  L.push(v.every(function(x){return x>=2;})
    ? '<span class="g">✓ 每镜 ≥ 2.0s（设计下限）</span>'
    : '<span class="w">△ 有镜头低于 2.0s 设计下限</span>');
  L.push(v[1]>=3
    ? '<span class="g">✓ 主镜 '+v[1]+'s ≥ 3.0s（信息镜）</span>'
    : '<span class="b">✗ 主镜 '+v[1]+'s < 3.0s，装不下信息</span>');
  var grid=v.every(function(x){return Math.abs(x*2-Math.round(x*2))<1e-9;});
  L.push(grid ? '<span class="g">✓ 符合 0.5s 网格</span>' : '<span class="w">△ 建议取 0.5s 网格</span>');
  tout.innerHTML=L.join('<br>');
  var rc = ratio<=2.5 ? 'g' : (ratio<=5.5 ? 'w' : 'b');
  var rt = ratio<=2.5 ? '量产安全' : (ratio<=5.5 ? '合法但重生成代价高' : '极端悬殊，务必先试拍');
  rout.innerHTML = mn>0
    ? '<span class="'+rc+'">悬殊比 '+ratio.toFixed(2)+' — '+rt+'</span><br>'
      + '<span class="n">最长 '+mx+'s ÷ 最短 '+mn+'s</span>'
    : '<span class="n">填入时长后显示</span>';
}
[tA,tB,tC].forEach(function(x){ x.addEventListener('input',chkT); });

/* ---- 台词容量换算 ---- */
var wNum=document.getElementById('wNum'), wSec=document.getElementById('wSec'), wout=document.getElementById('wout');
function chkW(){
  var w=parseFloat(wNum.value)||0, s=parseFloat(wSec.value)||0;
  var need = w/3.15, cap = s*3.15;
  var L=[];
  L.push('<span class="n">'+w+' 字 → 约 '+need.toFixed(1)+'s</span>');
  L.push('<span class="n">'+s+'s → 上限 '+Math.floor(cap)+' 字</span>');
  if(s>0){
    if(w<=cap) L.push('<span class="g">✓ 装得下</span>');
    else L.push('<span class="b">✗ 超出 '+(w-cap).toFixed(0)+' 字，语速会崩</span>');
    if(s<=2 && w>7) L.push('<span class="w">△ 衔接镜建议 ≤7 字或无台词</span>');
    if(s<=2 && w<=7) L.push('<span class="g">✓ 符合衔接镜容量</span>');
  }
  wout.innerHTML=L.join('<br>');
}
[wNum,wSec].forEach(function(x){ x.addEventListener('input',chkW); });

/* ---- 提示词工作区 ---- */
var ta=document.getElementById('prompt');
var pbar=document.getElementById('pbar'), pstat=document.getElementById('pstat'), pzone=document.getElementById('pzone');
function upd(){
  var v=ta.value, chars=v.length, han=(v.match(/[\u4e00-\u9fff]/g)||[]).length;
  pbar.style.width=Math.min(100, chars/7000*100)+'%';
  pbar.style.background = han>2500 ? 'var(--bad)' : ((han>0 && han<1200) ? 'var(--warn)' : 'var(--ok)');
  pstat.innerHTML = han.toLocaleString()+' 汉字 · '+chars.toLocaleString()+'/7000 字符';
  var m='', c='';
  if(han===0){ m='开始输入后显示校验结果'; }
  else if(han<1200){ m='⚠ 偏短（'+han+' 汉字）：低于 1200，模型可能自行脑补细节'; c='warn'; }
  else if(han<=1800){ m='✅ 甜点区（'+han+' 汉字）：长度合适'; c='ok'; }
  else if(han<=2500){ m='⚠ 偏长（'+han+' 汉字）：可用，但关键指令别埋在中段'; c='warn'; }
  else { m='❌ 超长（'+han+' 汉字）：超出安全上限 2500，建议拆镜或把静态信息移到参考图'; c='bad'; }
  if(chars>7000){ m='❌ 超出 H3 硬上限 7000 字符，必须删减'; c='bad'; }
  pzone.textContent=m; pzone.className='zone '+c;
}
ta.addEventListener('input',upd);

Array.prototype.forEach.call(document.querySelectorAll('[data-ins]'), function(b){
  b.onclick=function(){
    var t=TPL[b.getAttribute('data-ins')];
    ta.value = ta.value ? ta.value.replace(/\s*$/,'')+'\n\n'+t : t;
    ta.scrollTop=ta.scrollHeight; upd(); ta.focus();
  };
});
document.getElementById('clr').onclick=function(){ if(confirm('清空工作区？')){ ta.value=''; upd(); } };
document.getElementById('cp').onclick=function(e){ cpText(ta.value, e.target); };

document.getElementById('copyAll').onclick=function(e){
  var out=[], ns=document.querySelectorAll('main h1,main h2,main h3,main p,main li,main pre code,main td,main th');
  for(var i=0;i<ns.length;i++){
    var n=ns[i], tag=n.tagName.toLowerCase();
    if(tag==='code'){ out.push(n.innerText); }
    else if(tag==='h1'){ out.push('\n# '+n.innerText); }
    else if(tag==='h2'){ out.push('\n## '+n.innerText); }
    else if(tag==='h3'){ out.push('\n### '+n.innerText); }
    else { out.push(n.innerText); }
  }
  cpText(document.title+'\n'+out.join('\n'), e.target);
};

/* ---- 滚动高亮 + 回顶 ---- */
var tb=document.getElementById('topbtn');
window.addEventListener('scroll',function(){ tb.style.display = window.scrollY>600 ? 'flex' : 'none'; });
tb.onclick=function(){ window.scrollTo({top:0,behavior:'smooth'}); };

var links=[].slice.call(document.querySelectorAll('#side a'));
var all=[].slice.call(document.querySelectorAll('#chips a'));
function mark(id){
  links.concat(all).forEach(function(a){ a.classList.toggle('on', a.getAttribute('data-t')===id); });
}
var obs=new IntersectionObserver(function(es){
  es.forEach(function(en){ if(en.isIntersecting) mark(en.target.id); });
},{rootMargin:'-8% 0px -78% 0px'});
[].slice.call(document.querySelectorAll('main h2,main h3')).forEach(function(h){ if(h.id) obs.observe(h); });

chkT(); chkW(); upd();
</script>
</body>
</html>
"""

PAGE = (
    PAGE.replace("__CHIPS__", chips_html)
        .replace("__NAV__", nav_html)
        .replace("__SNIPS__", snips_html)
        .replace("__BODY__", body)
        .replace("__TPLJS__", tpl_js)
)

OUT.write_text(PAGE, encoding="utf-8")
print("已生成:", OUT)
print("大小(KB):", round(OUT.stat().st_size / 1024, 1))
print("目录条目:", len(nav), " 定位chip:", len(chips), " 速取卡:", len(SNIPPETS))
