---
name: h3-screen-text
description: 海螺 H3 视频提示词中「手机屏幕 / 短信 / 角色看手机视频 / 画面内文字 / 招牌字幕」的处理方案。含干净底板+后期贴图、不可辨认声明、参考图锚定三档方案与可复制模板。触发词：H3手机屏、H3短信、H3屏幕内容、H3看手机、H3画面文字、H3招牌、H3字幕乱码。
agent_created: true
---

# H3 屏幕与画面内文字处理规范

> 本 skill 只解决一件事：**当分镜里出现"手机屏 / 短信 / 角色看手机 / 招牌 / 字幕 / 文件文字"时，H3 的提示词该怎么写、哪些必须交给后期。**
> 它服从主模板（`MiniMaxH3-小说转分镜-完整模板.md`）的全部术语与硬约束，不另立标准；覆盖主模板 §6.4-E、§8.3 与 `防翻车限制词库_H3版.md` §8、§12。

## 0. 先记住这四句话

| # | 结论 | 依据 |
|---|---|---|
| 1 | **交付级的可读文字一律后期合成。** H3 文字能力强于同类，但实测判定仍是：*"Reference mode holds an existing label far better than text-to-video invents one, but **neither is safe for anything a client will read closely**. Composite text in post."* | 【H3·实测转述】 |
| 2 | **把「不可辨认」主动写进提示词**，模型就不再去赌字形，观众也读不出错字 —— 比硬写短信原文稳一个量级。 | 【工艺】 |
| 3 | **观众要的是情绪，不是像素。** 拍"屏幕打在脸上的光"，别拍"屏幕里的字"。 | 【工艺】 |
| 4 | 屏幕内容 = **文字 + UI + 动态刷新** 三重叠加，是全部翻车类型的交集。分镜表里打风险码时，它永远是 `T`。 | 【工艺】 |

### 0.1 本 skill 使用的证据分级

**【H3】** 官方规格　|　**【工艺】** 模型无关的通用规律　|　**【推】** 机制推断，无实测数字　|　**【待验证】** 无法确证，文末附实测方法　|　**✗ 硬阻断** 提示词解决不了，须靠参考输入 / 后期 / 换方案

**铁律**：① 严禁编造数字与官方原文，无法确证的标【待验证】并给实测方法；② 提示词模板、官方术语、例句**保留英文原文**，中文只作解释；③ 本 skill 全部方案的目标是**降低发生率或把风险搬出生成环节**，不是消除。

---

# §1 为什么屏幕内容是最高危区域

## 1.1 三重叠加的失效机制

普通翻车项通常是单一成因（手部位数、肢体结构、物理碰撞）。**屏幕内容是唯一一个同时踩中四个失效通道的元素**：

| 失效通道 | 具体表现 | 为什么在屏幕上必然发生 |
|---|---|---|
| **① 文字** | 字形崩坏、少笔画、多笔画、中英混排、逐帧抖动 | 模型把文字当**像素图案**学，没有字形结构规则。§8.3 硬阻断清单原文：*"模型把文字当像素图案，无字形结构规则"* |
| **② UI 结构** | 气泡错位、列表项重复、图标融化、卡片数量逐帧变化 | UI 是**大量小尺度刚体的精确排布**，模型无栅格约束、无对齐约束 |
| **③ 动态刷新** | 内容在无人操作时自己变、滚动条乱跳、进度条回退 | 视频的跨帧状态跟踪本身弱，叠加"屏幕内容应该变化"的先验，模型会**主动制造它以为该有的变化** |
| **④ 承载面极不稳定** | 手机晃动、手指遮挡、反光、透视变化 | 手机是小物件 + 手持 → 同时命中「小物件资产丢失」与「手部异常」两个通道 |

> **这四项是相乘不是相加。** 招牌只踩 ①，文件只踩 ①④，手机屏四项全中。所以屏幕内容的失败率是所有画面元素里最高的。

## 1.2 小字为什么必死：量化失效机制

**保守方给出的机制（是本 skill 采纳的判据）**：

> *"Keep on-screen text large and high-contrast. **Small text is the first casualty of 8-bit quantization.**"*

**关键推论：这条失效机制与分辨率无关。** 8-bit 量化发生在**每个颜色通道的编码精度**上，上 2K 只是增加像素数量，不增加每个像素的阶数。

> ⚠️ **因此：即使上 2K，屏幕小字也不降级，仍按高风险处理。** 乐观方（*"at 1440p fine detail stops being suggestion and becomes information"*）只有断言、无测试集；保守方给了具体机制。**从严处置。**

## 1.3 一个反直觉的事实：官方"能写文字"≠"文字可用"

【H3】官方确实给了精确的文本写法：

```text
Place any banner, sign, label, subtitle, or neon text that is actually visible on screen in English
double quotation marks. Preserve the original text and punctuation verbatim, without translation.

A red neon sign reading "营业中" glows above the doorway.
```

**这条规则的正确读法**：它是**"当文字必须出现时"的正确写法**，不是"模型能稳定渲染文字"的保证。官方自己在别处把文字列为**脆弱细节（fragile detail）**，建议与运动分开判断。

→ **决策含义**：官方规则解决的是"写法的规范性"，不解决"渲染的可靠性"。规范性照做，可靠性靠后期。两者不冲突，是两条独立的工作流。

## 1.4 失效成本：为什么屏幕崩了特别贵

手部崩可以裁掉、可以换镜；**屏幕崩是整条信息载体报废**——都市题材里"短信内容""监控画面""转账金额"往往是本段唯一信息点（主模板 §3.1：B 主镜承载本段唯一信息点）；字幕崩则直接不可交付。

→ **所以屏幕类镜头的处置动作默认填 `后置`（生成时不解决，交给后期），而不是 `重生成`。**（主模板 §8.6 处置四级枚举）

---

# §2 三档方案详解（A / B / C）

## 2.0 决策树（先走这个，再选模板）

```
分镜里出现手机屏
   │
   ├─ 观众需要【读出】屏幕上的字吗？
   │     │
   │     ├─ 需要（金额/名字/罪名/证据）───────────► A 档（推荐）
   │     │                                    或 C 档（短视频、可接受漂移）
   │     │
   │     └─ 不需要，只要有"在看手机"这件事 ─────► B 档（最实用、成本最低）
   │
   └─ 屏幕根本不需要被看到？
         └─ 只拍屏幕的光 / 只拍手机背板 ────────► B 档变体 B0（零风险）
```

## 2.1 三档横向对比

| | **A 干净底板 + 后期贴图** | **B 主动认领不可辨认** | **C 参考图锚定** |
|---|---|---|---|
| **风险** | 低（★推荐） | 低（★最实用） | 中 |
| **核心做法** | 生成时屏幕是**无内容的纯色面**，后期 corner pin 贴内容 | 把"不可辨认"写进提示词 | 图像模型做正确 UI 静帧 → 参考图传入 → 提示词只写"内容不变" |
| **屏幕内容** | 后期决定，像素级稳定、可改字、可换语种 | 永久不可读 | 首帧正确，中段可能漂移 |
| **后期** | 必须（角点跟踪 + 混合模式 + 光影匹配） | 不需要 | 通常需要（漂移处修补） |
| **生成成本** | 正常 | **最低**（无需额外资产、无需多条挑选） | 高（需做 UI 图 + 多跑几条挑） |
| **适用** | 交付级、对客、长剧集 | 过场、氛围、情绪镜、短视频 | 短视频、非对客、首帧即信息点 |
| **主模板定性** | `后置` | `降级` | `降级` + `后置` |

---

### 2.1b 三档成本对比（合并）

| 项 | A 干净底板+后期 | B 不可辨认 | C 参考图锚定 |
|---|---|---|---|
| 生成成本 | 1×（正常） | **1×（最低）** | **2–4×**（需多条挑选；C2 还占 1 个参考图槽位） |
| 资产制作 | 需做 UI 设计稿 | 无 | 需先用图像模型做正确 UI 静帧 |
| 后期成本 | **2–3×**（相对普通镜） | **0** | 1–2×（漂移修补） |
| 参考图费用【H3】 | — | — | 前 5 张免费，**第 6 张起 $0.04/张**；视频参考按时长计费（最贵）；音频参考免费 |
| 失败模式 | 单调可修（跟踪漂了重跟，不导致重生成） | 偶发"仍出了可读乱码" → 换种子重跑 1–2 条 | **二值**：首帧对就可用，首帧错则整条废 |
| 规模化建议 | **长剧集必选**（UI 稿可复用全剧，改字/换语种零成本） | 过场/氛围镜首选 | 屏幕镜 < 3 个时可考虑；超过 10 个则 A 档边际成本更低 |

> 【推】"2–3×"是相对工时经验估计，无公开基准，建议台账记 10 镜后校准。【待验证】C 档漂移临界点（2s/3s/5s）无公开数据，实测方法见 §附 C。

---

## 2.2 A 档：干净底板 + 后期贴图

### 适用
- **观众必须读出屏幕内容**（短信正文、转账金额、聊天对象名、监控时间码）
- 对客交付 / 长剧集 / 需要改字、换语种
- 屏幕需要在镜头里持续 3 秒以上

### 关键设计点：底板要"发光"，不是"全黑"

主模板与防翻车库的原始写法是 `blank dark screen`（纯黑屏）。**但当角色正在看手机时，纯黑屏在叙事上是矛盾的**（黑屏 = 灭屏 = 没在看）。

→ **A 档拆成两个变体**：

| 变体 | 用途 | 屏幕状态 | 后期贴法 |
|---|---|---|---|
| **A1 亮屏纯色** | 角色正在看 | 屏幕发**均匀的冷白光**，无任何界面 | 贴图层用 **Screen / Add** 混合，直接压在发光面上 |
| **A2 灭屏纯黑** | 刚锁屏 / 还没点亮 / 放下手机 | 屏幕全黑不发光 | 贴图层用 **Screen**（黑底上 Screen 等于直接替换），最简单 |

### A1 完整提示词模板（复制可用）

```text
She holds the phone in her RIGHT hand, the screen angled up toward her face and
turned away from the camera. The screen is lit and its entire surface is a single
uniform cool-white field; the only thing visible on the glass is a thin soft-edged
reflection of the ceiling light. The cool white light
from the screen falls on the underside of her chin, her lower cheeks and the collar
of her coat, lifting them slightly against the dim room. Her thumb rests along the lower
edge of the phone and stays there. Do not let the brightness of the screen change at
any point in the shot.
```

**中文对照**：她右手握着手机，屏幕上仰朝向她的脸、背对镜头。屏幕亮着，**整个屏面是一片均匀的冷白光**，玻璃上唯一可见的东西是一小块柔和边缘的天花板灯反光。冷白光落在她的下巴底面、下半张脸和外套领口上，把这几处微微提亮。她的拇指搭在手机下边缘并停在那里。屏幕亮度在整镜中任何时刻都不改变。

### A2 提示词模板（复制可用）

```text
She lowers the phone into her lap; the screen is black and unlit, the glass showing
only a faint reflection of the window. Her face falls back into the warm
key light, which is now the only light touching her. Do not let the screen light up at
any point in the shot.
```

**中文对照**：她把手机放到腿上，屏幕全黑不发光，玻璃上只映出窗户的一丝反光；她的脸重新落回暖色主光之中，此刻这盏灯是唯一照到她的光源。屏幕在整镜中任何时刻都不亮起。

### A 档后期流程

完整 9 步见 **§8**。这里只记三步核心与最容易翻车的一环：

| 步 | 动作 | 要点 |
|---|---|---|
| 1 | **平面跟踪 → Corner Pin** | 跟屏幕**四角**而非手机轮廓；被手指遮挡时走**内缩安全区** |
| 2 | **混合模式** | A1 用 `Screen`/`Add`（屏幕是发光体）；A2 用 `Screen`（黑底等效替换） |
| 3 | **光影匹配** | 保留反射层（贴图上方的 `Screen` 层，5–15%）+ 冷色 spill + shutter blur |

> ⚠️ **最常穿帮的是第 3 步里的运动模糊**：贴图是静止渲染的，不加 shutter blur 就有"贴纸感"。详见 §8.2 ⑥。


---

## 2.3 B 档：主动认领「不可辨认」（★ 最实用）

### 适用
- 只需表达"她在看手机 / 收到消息 / 在刷视频"，**内容不重要**
- 过场镜、衔接镜、氛围镜（主模板 §3.5 类型库 #3 道具特写、#4 反应镜）
- 时间紧、预算紧、不想做后期

### 核心原理（为什么这招有效）

> **模型在"要不要赌字形"上有选择权。** 你不提屏幕内容 → 它按训练先验**默认补一套像界面的图案**（最坏结果：观众看出那是字，读出来是错的）。你主动声明"不可辨认" → 它明确放弃字形，改用模糊和反光糊过去。**模型不再赌，观众也读不出错。**

**关键区别**：`不可辨认` ≠ `没有内容`。前者是"那里有东西，只是看不清"（叙事成立），后者是"屏幕坏了"（叙事穿帮）。

### B 档三句核心句（任选其一，也可叠加）

| 变体 | 英文原句 | 中文 | 适用 |
|---|---|---|---|
| **B1 运动模糊** | `The screen content is softened by motion blur and reflection, illegible.` | 屏幕内容被运动模糊与反光柔化，不可辨认 | 手在动 / 镜头在推 / 通用首选 |
| **B2 反光糊化** | `The glass of the screen catches a bright reflection of the window; the content underneath is washed out and unreadable.` | 屏幕玻璃映出窗户的明亮反光，底下的内容被冲淡、无法阅读 | 静态手持、室内靠窗 |
| **B3 角度 + 距离** | `The screen is seen at a steep oblique angle from two steps away, its content reduced to unreadable smears of light and colour.` | 屏幕以陡斜的角度从两步外被看到，内容退化成无法辨认的光色斑块 | 中景、镜头离屏幕远 |

**B 档的一个硬边界**：声明"不可辨认"之后，**绝不能再给屏幕特写**。一旦景别近到观众能看清，"不可辨认"就变成了穿帮（观众能看到那是模糊的一团，而不是有内容）。

→ **B 档的景别下限：中近景（waist-up 及以上），禁止大特写。**

### B 档完整提示词模板（复制可用）

```text
A medium shot frames her seated on the sofa, looking down at the phone she holds in
both hands. The screen is turned up toward her face and away from the camera; its
content is softened by motion blur and reflection, illegible. The cool white light
from the screen lights the underside of her face from below, while the warm floor
lamp on the right remains the single key light. She blinks once, then her eyebrows
draw together slightly, then her thumb stops moving. The camera pushes in with small
amplitude at slow speed to a close-up of her face, not of the phone. By the end of the
shot her gaze is still lowered, the cool light on her chin is unchanged, and the screen
content is still illegible.
```

**中文对照**：中景，她坐在沙发上，低头看着双手捧着的手机。屏幕上仰朝向她的脸、背对镜头，内容被运动模糊与反光柔化，不可辨认。冷白光从下方照亮她的下半张脸，右侧暖色落地灯仍是唯一主光。她眨眼一次，然后眉毛微微收紧，然后拇指停住。镜头小幅慢速推近到她的**脸部**特写（不是手机）。到本镜结束她的视线仍低垂，下巴上的冷光不变，屏幕内容仍然不可辨认。

### B0 变体：连屏幕都不给（零风险）

**适用场景**：只需要"他在看手机"这个信息，且手机在远景或作为身份符号。

| 变体 | 英文原句 | 中文 |
|---|---|---|
| **B0-1 背板朝镜头** | `He holds the phone with the BACK of the phone facing the camera; only the matte black back panel and his fingers are visible. A thin rim of cool white light escapes around the phone's edge.` | 他以手机背面朝向镜头握持，只见哑光黑色背板与手指，手机边缘漏出一圈冷白色光 |
| **B0-2 只拍光不拍机** | `The screen is not visible to camera; only its cool white glow lights the underside of her face and her chin from below.` | 镜头看不到屏幕，只有屏幕的冷白光从下方照亮她的脸的下半部与下巴 |
| **B0-3 拍口袋/桌面** | `The phone lies face-down on the table beside her hand, its screen pressed flat against the tabletop and its matte black back panel the only part on show.` | 手机正面朝下放在她手边的桌上，屏幕平贴桌面，只有哑光黑色背板露在外面 |

> **B0 是唯一真正零风险的写法**——画面里根本不存在需要渲染的文字区域。在能用 B0 的地方优先用 B0。

### B 档后期流程
**不需要后期。** 这是 B 档最大的成本优势。仅需常规调色。


---

## 2.4 C 档：参考图锚定

### 适用
- 短视频、非对客内容、可接受中段漂移
- **首帧就是信息点**（开场即"屏幕上写着XXX"）
- 已经有一张做好的正确 UI 图（图像模型生成，或真实设计稿）

### 前置硬约束（必读）

> **【H3】图生视频与全能参考互斥** —— `first_frame` / `last_frame` 与 `reference_*` **不可同时出现在同一次请求中。**

→ C 档有**两条互斥的实现路径**，必须先二选一：

| | **C1 走 FL2VA（首尾帧）** | **C2 走 Ref2VA（全能参考）** |
|---|---|---|
| 输入 | 1–2 张图（首帧 = UI 静帧） | ≤9 图 + ≤3 视频 + ≤3 音频 |
| 能否同时锁角色/场景 | **不能**（只有 2 张图，要留给屏幕） | **能**（屏幕占 1 张，其余锁脸/服装/场景） |
| 提示词锚定 | 指令首行 + `<Picture 1>` | `subject_definitions` + `retention_analysis` |
| 官方默认 | **FL2VA 默认单镜**（*"FL2VA generally favors a single shot"*） | 支持多镜 |
| 适用 | 单镜屏幕特写（2–3s） | 屏幕镜需要和其他镜同段生成 |
| 风险 | 身份/场景一致性下降（放弃 9 图资产锁） | **不能精确控制首帧构图** |

> ⚠️ **C1 与"角色看手机"天然冲突**：C1 把 2 张图全给了屏幕，角色身份就失去视觉锚定。**所以 C1 只适合"只有手机、没有人"的道具特写镜**（主模板 §3.5 类型库 #3）。

### C1 模板（FL2VA，单镜屏幕特写）

**完整可提交的模板见 附 B.2（含中文对照）。** 这里只记三条要点：

1. 指令首行按官方 FL2VA **固定模板**写：`Picture 1` **无尖括号**、`(from Shot 1)` **无方括号**、`S.SS` **两位小数**；官方自身两处不一致，照抄即可，不要自作主张统一成 I2VA/L2VA 的写法。
2. `The screen content remains unchanged throughout.` 必须写在**镜内开头**（关键约束不埋中段，主模板 §6.5），不能写在末尾。
3. 用**正向枚举**锁死内容（`the same three bubbles, the same sender name, the same timestamp, the same colours and the same positions`）；**不要**成串列举失败产物（如 `no duplicated cards, no melting geometry`），那会把失败产物本身送进条件分布。需要收边时**只加 1 句 B 类** `Do not let the screen change at any point in the shot.`（见 §7.8.1）。

### C2 模板（Ref2VA，屏幕作为一个独立资产）

```text
subject_definitions:
<Picture 4> is the phone UI screen, a flat-on shot of the message thread, used as the
exact on-screen content reference.
<Subject 1> is the young woman from <Picture 1>, with shoulder-length straight black hair.
<Picture 5> is the location and its light direction.

retention_analysis:
<Picture 4>: fully_preserved - the message thread on the phone screen keeps the exact
same three bubbles, sender name, timestamp, colours and layout.
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - her facial identity,
hairstyle, clothing and the phone in her right hand are unchanged.
<Picture 5>: attribute_transfer - only the colour grade and light direction are adopted
from it; the room, the furniture and every prop come from the other references.

summary:
[reference generation] ...

detailed_description:
[Shot 1] ...
```

**要点**：
- 屏幕 UI 是一张**具体的目标帧** → 用 `<Picture N>`（官方定义：*"A reference image used as a concrete target frame or shot-planning anchor"*）。
- 若屏幕必须**像素级不变** → `fully_preserved`；若屏幕会被看到透视/倾斜/部分被手指遮挡（角色握着时几乎必然）→ 改 `partially_preserved`，否则模型会为了"保留"而把屏幕强行摆正，姿态随之崩坏。【推】
- 风格/场景图**必须** `attribute_transfer`，误用 `fully_preserved` 会把参考图里的物体也搬进画面。

### C 档后期流程

| 情况 | 做法 |
|---|---|
| 首帧正确、中段漂移 | 逐段修补：漂移段用 A 档的平面跟踪 + 贴图盖掉 |
| 出现重复卡片 / 融化 | **救不回来**，重跑或改 B 档 |
| 文字错字 | **救不回来**，改 A 档 |


---

## 2.5 三档与分镜表字段的对应

在主模板 §附 2 的分镜表字段里，屏幕镜按此填写：

| 字段 | A 档 | B 档 | C 档 |
|---|---|---|---|
| `风险类型` | `T` | `T` | `T` |
| `风险等级` | 低 | 低 | 中 |
| `处置动作` | **后置** | **降级** | **降级 + 后置** |
| `备选方案` | 降级为 B 档 | 降级为 B0（不给屏幕） | 降级为 A 档 |
| `是否单请求多镜` | 是 | 是 | C1 填「否」（FL2VA 默认单镜） |
| `采样步数` | 6–8（出片） | 6–8 | 6–8 |

> **采样步数纪律**：屏幕出问题，先怀疑步数。*"人物动作散架或音画对不上时，第一件该怀疑的是步数太低，不是 prompt 写错。"* 试拍 4 步、出片 6–8 步。**步数是 4 时判定的"这个镜头做不了"结论无效。**

---

# §3 B 档「不可辨认」专章

> 这是本 skill 里**性价比最高的一节**。绝大多数手机镜，用 B 档就够了。

## 3.1 为什么"主动认领不可辨认"比"什么都不说"好

| 写法 | 模型的行为 | 观众看到 | 判定 |
|---|---|---|---|
| **什么都不提**（`She looks at her phone.`） | 按先验自动补一套界面 | 能看出是字，读出来是错的 | ❌ **最差** |
| **硬写短信原文**（`a message reading "今晚八点老地方"`） | 逐字去赌，输面大 | 错字、缺笔画、语种混杂 | ❌ 差 |
| **只写"没有文字"**（`no text on the screen`） | 可能理解成屏幕是关的/坏的 | 屏幕黑着，但她明明在看 | ⚠️ 穿帮 |
| **主动认领不可辨认**（`illegible`） | 明确放弃字形，改用模糊/反光填 | 知道那里有内容，看不清 | ✅ **最优** |

## 3.2 变体库（12 句，直接复制）

### 3.2.1 运动模糊类

| # | 英文原句 | 中文 |
|---|---|---|
| 1 | `The screen content is softened by motion blur and reflection, illegible.` | 屏幕内容被运动模糊与反光柔化，不可辨认 |
| 2 | `As her hand trembles slightly, the screen content smears into unreadable streaks of light.` | 手微微颤动，屏幕内容被拖成无法阅读的光条 |
| 3 | `The phone is in constant slight motion, so the screen never resolves into anything readable.` | 手机始终轻微移动，屏幕内容始终无法清晰成像 |

### 3.2.2 反光 / 曝光类

| # | 英文原句 | 中文 |
|---|---|---|
| 4 | `The glass of the screen catches a bright reflection of the window; the content underneath is washed out and unreadable.` | 屏幕玻璃映出窗户反光，底下的内容被冲淡、无法阅读 |
| 5 | `A hard specular highlight runs across the screen, hiding everything beneath it.` | 一道强烈的高光横贯屏幕，遮住底下的一切 |
| 6 | `The screen is blown out by its own brightness at this angle, showing only a white glare.` | 从这个角度看屏幕被自身亮度过曝，只见一片白色眩光 |

### 3.2.3 角度 / 距离类

| # | 英文原句 | 中文 |
|---|---|---|
| 7 | `The screen is seen at a steep oblique angle from two steps away, its content reduced to unreadable smears of light and colour.` | 屏幕在两步外以陡斜角度呈现，内容退化成无法辨认的光色斑块 |
| 8 | `The phone is held low and far, and the screen is only ever seen edge-on.` | 手机拿得又低又远，屏幕始终只以侧边示人 |
| 9 | `The screen faces away from the camera at all times; the camera sees only the back of the phone.` | 屏幕全程背对镜头，镜头只看到手机背面 |

### 3.2.4 遮挡 / 焦外类

| # | 英文原句 | 中文 |
|---|---|---|
| 10 | `Her thumb and the edge of her sleeve cover most of the screen; nothing readable remains visible.` | 拇指和袖口遮住大部分屏幕，看不到任何可读内容 |
| 11 | `The phone stays in the soft foreground blur, its content never comes into focus.` | 手机始终在前景柔焦中，内容从未合焦 |
| 12 | `Shot from behind her shoulder, the screen is a small bright rectangle far from the lens, its details beyond resolution.` | 从她肩后拍摄，屏幕只是远离镜头的一个小亮矩形，细节超出分辨能力 |

## 3.3 B 档的适用边界（三条硬线）

| 边界 | 规则 | 违反后果 |
|---|---|---|
| **景别下限** | 最近到**中近景（waist-up）**。**禁止**屏幕大特写 | 观众能看清"那是模糊的一团"，穿帮 |
| **时长上限** | 单镜 ≤ 5 秒。更长的静止"模糊屏"会让人出戏 | 观众开始疑惑"为什么一直看不清" |
| **信息承载** | **B 档屏幕绝不承载叙事信息**。信息必须由**对白/旁白/下一个镜头**给出 | 信息丢失 |

> ⚠️ **最重要的一条**：如果这条路走不通（观众必须读到内容），**不要试图把 B 档"写得更清楚一点"**——那是 C 档的活，而且 C 档也不保险。**直接上 A 档。**

## 3.4 B 档的信息替代方案：把视觉信息搬到听觉

**H3 原生生成语音与唇形同步**（这是 H3 相对前代的能力变化）。这意味着：**原本要靠"屏幕上的字"传达的信息，可以改由角色念出来。**

| 原设计 | 改成 |
|---|---|
| 她看着屏幕上的分手短信 | 她看着手机，然后**念出**那句话：`<d>[Chinese] 他说，我们到此为止。</d>` |
| 他盯着转账金额 | 他盯着手机，喉结滚动，然后低声：`<d>[Chinese] 五十万……他真的转了。</d>` |
| 看监控画面认出凶手 | 她看着屏幕，瞳孔收缩，然后：`<d>[Chinese] 我认识那件外套。</d>` |

**优势**：
1. 对白是 H3 原生出声，**100% 准确**，不存在字形崩坏
2. 观众获得的情绪强度**更高**（听到人说 vs 看到字）
3. 完全不需要后期

**写法**（官方对白规范：说话人描述与表达方式放**标签外**，只有**语言标签 + 台词**放**里面**）：

```text
Her gaze stays on the screen; the cool light on her chin flickers once, then she says
in a flat, empty voice (S1): <d>[Chinese] 他说，我们到此为止。</d>
```

**中文对照**：她的视线停留在屏幕上，下巴上的冷光闪了一下，然后她用平淡空洞的声音说：「他说，我们到此为止。」

> **这是本 skill 最推荐的信息传达路径。** 能用对白替代的屏幕文字，一律替代。

---

# §4 角色看手机的分镜设计

## 4.1 景别选择（一张表定死）

| 景别 | 屏幕像素占比 | 推荐档 | 判定 |
|---|---|---|---|
| **大特写（只拍屏幕）** | > 60% | — | ❌ **禁止**。小尺度精确对准是硬阻断（§9） |
| **特写（屏 + 半张脸）** | 25–40% | C | ⚠️ 高风险，仅短视频 |
| **中近景（waist-up）** | 8–15% | **B** | ✅ **推荐区间**。够近到看出在看手机，够远到内容不可辨 |
| **中景（全身坐姿）** | 3–8% | B / B0 | ✅ 最稳，但情绪弱 |
| **远景 / 全景** | < 3% | B0 | ✅ 零风险，只能表达"有人在玩手机" |

> **主模板 §3.2.1**：道具 / 手机屏特写建议 **2–3 秒**，静态为主、微动即可。**B 档屏幕镜控制在 2–3 秒**，是时长与风险的最佳平衡点。

## 4.2 光位：屏幕冷白光打脸的写法

### 4.2.1 与主模板「单一主光」原则的冲突与解法

主模板 §7（身份漂移）的锁定原则要求**光照方向全程单一主光，主光换边身份就会晃**。

**手机屏是第二个光源，会不会破坏一致性？** 解法：**把手机光声明为"局部补光 / 实用光源"，而不是主光。**

```text
[LIGHT] A single warm key light from camera right at 45° remains the main light for the
entire shot. The phone screen adds a secondary cool-white fill on the underside of her
face only; this secondary light never becomes the key light, never moves to the other
side of her face, and never changes colour temperature.
```

**中文对照**：来自镜头右侧 45° 的单一暖色主光在整镜中始终是主光。手机屏幕只在她脸的下半部增加一层冷白色补光；这层补光永远不会变成主光，不会移到她脸的另一侧，色温也全程不变。

### 4.2.2 冷白光打脸的写法库

| # | 英文原句 | 中文 |
|---|---|---|
| 1 | `The cool white light from the screen lights her face from below, sharpening the line of her jaw and leaving the upper half of her face in the warm ambient dark.` | 屏幕的冷白光从下方照亮她的脸，勾出下颌线，上半张脸留在暖色环境暗部中 |
| 2 | `A soft cool-white glow from the screen falls on the underside of her chin, her lower lip and the open collar of her coat.` | 屏幕的柔和冷白光落在下巴底面、下唇与外套敞开的领口上 |
| 3 | `The screen light picks out the wet edge of her lower eyelid and the pale skin under her eyes.` | 屏幕光勾出下眼睑的湿润边缘与眼下的苍白皮肤 |
| 4 | `Her face is split: warm amber above from the lamp, cool white below from the phone.` | 她的脸被分成两半：上方是落地灯的暖琥珀色，下方是手机的冷白色 |
| 5 | `As she tilts the phone, the cool light slides across her cheek and settles on her collarbone.` | 她倾斜手机时，冷光扫过脸颊，最后落在锁骨上 |

> **第 4 句是最好用的一句**：一句话同时交代了两个光源的位置关系、色温差、以及"主光仍是灯不是手机"，直接消解 §4.2.1 的冲突。

## 4.3 视线落点

**写可见的肌肉变化，不写情绪名词**（主模板 §6.4-B：✅ `her eyebrows draw together` / ❌ `she looks sad`）。

| 情绪 | 英文原句 | 中文 |
|---|---|---|
| **专注** | `Her gaze drops to a fixed point just below the lens; her eyelids lower halfway and do not blink for the rest of the shot.` | 她的视线落在镜头正下方的某个固定点，眼睑半垂，本镜余下时间不再眨眼 |
| **不安** | `Her eyes dart left and right in small quick movements, then stop dead; her jaw tightens.` | 她的眼珠小幅快速左右游移，然后骤然停住，下颌收紧 |
| **震惊** | `Her eyebrows lift, her lips part slightly, and her gaze freezes on the screen; she does not blink.` | 她的眉毛抬起，嘴唇微张，视线凝固在屏幕上，不眨眼 |
| **心虚** | `Her gaze drops away from the screen to her own hands; her thumbnail picks at the cuticle of her index finger.` | 她的视线从屏幕移开落到自己手上，拇指指甲抠着食指的甲缘 |
| **看完收尾** | `She blinks once, then slowly raises her chin, then her gaze lifts to a fixed point beyond the lens.` | 她眨了一次眼，然后缓缓抬起下巴，然后视线抬向镜头之外的某个固定点 |

> ⚠️ **不要用角色左右描述方位**（主模板 §6.4-C：*"她的左边"有歧义*）。视线方向一律用**画面方位**：`below the lens` / `beyond the lens` / `toward frame right`。

## 4.4 手部握持姿态（三档降级）

握持手机属**精细持物**。防翻车 §4：*"消灭精细持物"* 是手部规避三原则之一；风险分级为 **握手（中）＜ 捏衣角（高）＜ 签字/持笔/插钥匙（极高）**。

→ **握持手机定级：中高。** 按此三档降级：

| 档 | 姿态 | 英文原句 | 中文 | 风险 |
|---|---|---|---|---|
| **H1（首选）** | **不握持** —— 手机平放桌面/腿上，手搭在旁边 | `The phone lies flat on the table; her right hand rests beside it, palm down, five fingers held together, not gripping it.` | 手机平放在桌上，她的右手搭在旁边，掌心向下，五指并拢，没有握住它 | 低 |
| **H2（次选）** | **双手捧握** —— 手指包住机身，无精细动作 | `She holds the phone with both hands, fingers wrapped fully around the body of the phone, thumbs resting along the two lower edges.` | 她用双手握着手机，手指完全包住机身，两根拇指搭在下方两条边上 | 中 |
| **H3（避免）** | **单手握持 + 拇指操作** | `She holds the phone in one hand, her thumb moving across the screen.` | 她单手握着手机，拇指在屏幕上移动 | **高** ❌ |

**H3 为什么必须避免**：它同时命中三个通道 —— ① 精细持物（手部）② 指尖与屏幕的精确对位（§9 硬阻断）③ 屏幕内容必须可见（§1）。**三项相乘，几乎必崩。**

**H2 的正面锚定收边句**（按主模板 §6.4-F：正向锚定 + 末尾最多一句 `Do not`）：

```text
Both hands hold the phone, fingers wrapped fully around its body, five fingers on each
hand, natural finger length and spacing, clean separation between fingers, both thumbs
resting along the lower edges of the phone; this hand shape holds unchanged from the
first frame to the last.
```

**中文对照**：双手握持手机，手指完全包住机身，每只手五指，手指长度与间距自然，指间分离清晰，两根拇指搭在手机下方边缘。这个手型从第一帧到最后一帧保持不变。

## 4.5 一个完整的「她收到短信」15 秒 3 镜骨架（B 档）

| 镜 | 时长 | 景别 | 屏幕 | 内容 |
|---|---|---|---|---|
| **A 入镜** | 2.0s | 中景，她坐在沙发上 | B0-3（手机面朝下放在腿上，不发光） | 建立空间与暖色主光 |
| **B 主镜** | 11.0s | 中近景 → 缓推到脸部特写 | B1（运动模糊 + 反光，不可辨认） | 她拿起手机、点亮、看完、念出台词 |
| **C 出镜** | 2.0s | 特写（她的眼睛，非手机） | 不在画面内 | 瞳孔收缩，冷光在下眼睑上闪一下 |

> **C 镜为什么拍眼睛不拍屏幕**：主模板 §3.5 类型库 #4「眼神 / 面部反应镜」—— *"视线匹配：人物看向画外 → 下镜即其所见"*。但在这里，**"其所见"是屏幕内容 = 高危**。所以反过来：**不上屏幕，只上反应**。观众从她的眼睛里读到一切。

---

# §5 角色看手机中的视频画面

> 这一节解决的是：**角色在刷视频 / 看监控 / 看直播回放**这类"屏幕内容本身是动态影像"的场景。

## 5.1 核心原则：拍「屏幕的光」，不拍「屏幕的内容」

**观众真正在读的信息是：她看到了什么反应。** 屏幕里的像素不承载信息，屏幕打在她脸上的光才承载信息。

| 拍什么 | 观众得到 | 风险 |
|---|---|---|
| 屏幕内容（像素） | 一段糊掉的小视频，看不清在演什么 | 极高 |
| **屏幕的光（明暗/色相的调制）** | "她在看一个会变化的东西"，以及她的情绪 | 极低 |

## 5.2 把"内容变化"外化成"光的调制"

**技巧：不在提示词里描述视频内容，只描述它投在角色脸上的光的时序变化。**

| 屏幕里在放什么 | 英文原句（只写光） | 中文 |
|---|---|---|
| 普通亮度变化 | `The cool light on her face breathes — brightening for about two seconds, then dimming, then brightening again.` | 她脸上的冷光在呼吸——亮约两秒，然后变暗，然后再亮起来 |
| 切换到更暗的场景 | `The light on her face dims sharply, as though the video she is watching has cut to a night scene.` | 她脸上的光骤然变暗，仿佛她正在看的视频切到了夜景 |
| 爆炸/闪光 | `A single hard white flash washes across her face and is gone; the room behind her does not change.` | 一道强烈的白光扫过她的脸随即消失，她身后的房间没有变化 |
| 火光 / 暖色画面 | `The light on her face shifts from cool white to a warm flickering orange, then back to cool white.` | 她脸上的光从冷白转为温暖跳动的橙色，然后又回到冷白 |
| 视频结束 / 灭屏 | `The cool light on her face fades out over about one second and does not return; her face falls back into the warm ambient dark.` | 她脸上的冷光在约一秒内淡出且不再回来，她的脸重新沉入暖色环境暗部 |
| 快速剪辑的内容 | `The light on her face stutters in quick irregular pulses, too fast to read as anything but flicker.` | 她脸上的光以快速不规则的脉冲跳动，快到只能读作闪烁 |

> **最后一句是这类镜头的万能兜底**：`flicker` / `pulses` 天然要求"看不清内容"，与 B 档的 `illegible` 完美兼容。

## 5.3 屏幕光随画面变化的分时写法（带时间锚点）

在单镜内用自然英文句写时序（**不要**用时间戳——时间戳是镜头切换用的，不是镜内节拍用的）：

```text
She holds the phone with both hands, the screen turned up toward her face and away from
the camera; its content is softened by motion blur and reflection, illegible. At first
the cool light on her face is steady. Then it brightens suddenly and holds, and her
eyebrows lift. Then it dims in three quick steps, and her mouth presses into a thin
line. The camera pushes in with small amplitude at slow speed to a close-up of her face.
By the end of the shot the cool light on her chin is dimmer than when it started.
```

**中文对照**：她用双手握着手机，屏幕上仰朝向她的脸、背对镜头，屏幕内容被运动模糊与反光柔化，不可辨认。起初她脸上的冷光是稳定的。然后它骤然变亮并保持，眉毛抬起。然后它分三步快速变暗，嘴抿成一条细线。镜头以小幅慢速推近到她的脸部特写。到本镜结束时，她下巴上的冷光比开始时更暗。

## 5.4 ⚠️ 声音层：手机外放是 diegetic，必须写回画面字段

**这是一个高频错误。**

【H3】官方原文（禁止内容条款）：

> *"Singing, instruments, radio, television, or **phone music audible to the characters** are diegetic events and should appear in the multimodal description."*

→ **角色能听到的手机声音 = diegetic = 写进 `integrated_multimodal_description`，不能写进 `non_diegetic_music`。**

| 情况 | 字段 | 写法 |
|---|---|---|
| 手机外放（角色和观众都听得到） | `integrated_multimodal_description` | `A tinny, compressed stream of dialogue and music plays from the phone's small speaker, too small and too far to make out any words.` |
| 角色戴耳机（观众听不到） | 不写声音，只写光 | `She wears earbuds; all the sound stays inside her ears. Only the light on her face changes.` |
| 手机震动 | `overall_soundscape` | `A phone buzzes once against the wooden tabletop, then goes quiet.` |
| 收到短信的提示音 | `integrated_multimodal_description` 或 `overall_soundscape` | `A short two-note chime comes from the phone.` |

**中文对照**：
- 手机小喇叭里传出单薄、压缩过的对白与音乐声，音量太小、距离太远，听不清任何词句。
- 她戴着耳机，全部声音都留在她耳朵里，只有她脸上的光在变化。
- 手机在木质桌面上震动了一次，然后归于安静。
- 手机传出一声短促的两个音的提示音。

> ⚠️ **不要在 `overall_soundscape` 里重复对白与剧情内音乐**【H3】：*"Dialogue, singing, and diegetic music already belong in the multimodal description and should not be repeated here."*

## 5.5 「看监控 / 看证据视频」的特殊处理

这类场景的信息密度最高，也最容易翻车。

**推荐结构（三镜，把信息从屏幕搬到脸和声音）**：

| 镜 | 屏幕 | 信息载体 |
|---|---|---|
| A（2s） | 屏幕亮起，内容不可辨认，只有光 | 建立"她开始看" |
| B（11s） | 光的调制（变暗 → 闪一下 → 稳定） | **她的脸**：瞳孔收缩 → 呼吸停 → 手指收紧 |
| C（2s） | 不在画面 | 她说出结论：`<d>[Chinese] 是他。</d>` |

> **不要设计"镜头推近到屏幕让观众看到监控画面"这一镜。** 这是把全段信息押在最高危的元素上。观众不需要看到监控里的人——**她认出来了，就够了。**

---

# §6 手机作为道具的资产锁定

## 6.1 资产锁定四要素（主模板 §6.4-E）

```
[ASSET LOCK] 一件 <材质+颜色> 的 <物件>，位于 <精确位置>，
全帧可见，从第一帧到最后一帧位置、大小、颜色完全不变。
```

**手机的资产锁（复制可用，全剧逐字复用）**：

```text
[PHONE ASSET LOCK — paste verbatim] A matte-black slab-style smartphone with rounded
corners and a plain, unbranded, unmarked back panel. She holds it in her
RIGHT hand and does not switch hands at any point. The phone stays the same size,
colour and shape from the first frame to the last; it is never duplicated, never
changes hand, and never leaves her hand.
```

**中文对照**：［手机资产锁——逐字粘贴］一部哑光黑色、圆角直板智能手机，背板是**素面、无品牌标识、无标记**的。她用右手握持，全程不换手。手机从第一帧到最后一帧大小、颜色、形状不变，不会重复出现、不会换手、不会离手。

> **为什么写 `a plain, unbranded, unmarked back panel` 而不是 `no visible brand logo`**：① 品牌 logo 是**图形 + 文字**，会命中 §1 的文字失效通道；② 避免品牌识别问题；③ 换集换戏时手机型号不会漂移。**这一项是必须的，不是可选的。**
> ⚠️ **必须用正向锚定的说法，不能写 `no visible brand logo`** —— 后者是裸名词否定，主模板 §6.4-F 判为 ❌ 禁用（名词本身进条件分布，反向激活）。详见 §7.8。

## 6.2 朝向锁定：正反面翻转是已知高发项

主模板 §8.3 硬阻断清单原文：

> | **手机正反面翻转** | 已知高发 | 参考图锚定 + 多条挑选 + 后期 |

**四层防御**：

| 层 | 做法 | 说明 |
|---|---|---|
| **1. 开场即终态** | 让手机**在开场就已经在手里**，且姿态就是全镜姿态 | ❌ 不要写 `she takes the phone out of her pocket, then...` —— 掏取是精细交互 + 状态突变，双重高风险 |
| **2. 参考图锚定** | 单独做一张"手握手机、屏幕上仰朝脸"的姿态参考图 | 占主模板 §2 的 9 图分配中的**槽位 6（关键道具特写）**或**槽位 7（手部姿态参考）** |
| **3. [PHONE-POSE] 锁定块** | 每镜逐字复制一段朝向描述 | 见下方模板 |
| **4. 多条挑选 + 后期** | 跑 3–4 条挑不翻的；实在没有就后期只保留不翻的帧段 | 最后一道防线 |

### [PHONE-POSE] 锁定块模板（复制可用）

```text
[PHONE-POSE — copy verbatim into every shot] The phone is held in her RIGHT hand at
about chest height, tilted roughly thirty degrees, with the SCREEN facing her face and
the BACK of the phone facing the camera at all times. The camera never sees the screen
surface directly; it sees only the back panel, the right edge, and the cool light
spilling around the phone's edges. The phone does not rotate, does not flip, and does
not turn over at any point in the shot.
```

**中文对照**：［手机姿态——每镜逐字复制］手机被她右手握在约胸口高度，倾斜约三十度，屏幕**始终**朝向她的脸，手机**背面**始终朝向镜头。镜头从不直接看到屏幕表面，只看到背板、右侧边缘，以及从手机边缘溢出的冷光。手机在本镜任何时刻都不旋转、不翻面、不翻转。

> **为什么写"倾斜约三十度"**：给一个**可度量的角度**比写"稍微倾斜"稳。主模板 §6.4-C 的同一原则：给可度量的距离并声明"全程不变"。

### 参考图锚定（Ref2VA 写法）

```
subject_definitions:
<Picture 6> is the exact pose reference: her right hand holding the matte-black
smartphone, screen tilted up toward her face, back of the phone toward the camera.

retention_analysis:
<Picture 6> (appears in [Shot 1], [Shot 2]): partially_preserved - the hand-and-phone
pose, the grip, the tilt angle and which side of the phone faces the camera are kept
exactly; only the size of the phone in frame changes with the shot size.
```

**中文对照**：`<Picture 6>` 是精确姿态参考：她右手握着哑光黑色智能手机，屏幕上仰朝脸，背面朝镜头。保留分析：手与手机的姿态、握法、倾角、哪一面朝镜头被精确保留；只有手机在画面中的大小随景别变化。

> 【推】这里用 `partially_preserved` 而不是 `fully_preserved`：`fully_preserved` 要求"定义的角色被完整保留"，会把景别变化也算作保真度损失，导致模型强行维持同样大小（与推镜冲突）。**只在"屏幕内容像素级不变"这一项上用 `fully_preserved`。**

## 6.3 型号一致性：全剧统一描述串

**把手机描述串做成模板常量，禁止临场改写、禁止同义替换**（主模板 §5.3 描述串锁）。

```text
[PHONE DESCRIPTION STRING — never rewrite]
a matte-black slab-style smartphone with rounded corners, a plain, unbranded,
unmarked back panel
```

| ❌ 常见错误 | 后果 |
|---|---|
| 第 1 集写 `a black smartphone`，第 5 集写 `a dark phone` | 同义替换 → 手机外观漂移 |
| 一集写 `matte black`，一集写 `glossy black` | 材质翻转 → 明显穿帮 |
| 加了 `with a clear case` 又忘了写进后续 | 手机壳忽有忽无 |

## 6.4 一镜内小物件上限

**【工艺】一镜内要稳住的小物件 ≤ 2 件。** 同时写耳环 + 项链 + 戒指 + 手机 + 手表，几乎必然丢 1–2 件。

→ **如果本镜的手机承载叙事信息（比如"她正在看那条短信"），手机的优先级高于耳环戒指。** 把耳环戒指从该镜的描述里**删掉**（不是弱化，是删除），让出注意力预算。

## 6.5 三条硬规则回顾（主模板 §6.4-E 原文）

1. **不要在提示词里写短信原文** —— 写了必乱码
2. **不要用极端特写怼屏幕** —— 小尺度精确对准是已知高发失败
3. **手机正反面翻转是已知高发项** —— 参考图锚定 + 多条挑选 + 后期

---

# §7 画面内其他文字：招牌 / 路牌 / 门牌 / 字幕 / 文件 / 信封

## 7.1 官方规则（先照做）

【H3】官方原文：

```text
Place any banner, sign, label, subtitle, or neon text that is actually visible on screen
in English double quotation marks. Preserve the original text and punctuation verbatim,
without translation.

A red neon sign reading "营业中" glows above the doorway.
```

**三个执行要点**：

| 要点 | 说明 |
|---|---|
| **英文双引号** | 用 `"` 包裹，不是中文引号 `“”`，不是书名号 |
| **逐字保留** | 原文是什么就写什么，**包括中文**。官方示例直接保留了 `营业中` |
| **不翻译** | 不要写 `a sign saying it is open`，要写 `a sign reading "营业中"` |

> **这条规则解决"写法规范"，不解决"渲染可靠"。** 引号写法是**必须出字时**的正确写法，不是"可以放心出字"的许可。

## 7.2 何时该出现文字：决策表

| 判断条件 | 结论 |
|---|---|
| 观众需要**读出**这段文字（店名、门牌号、文件内容、金额） | ❌ **不交给模型**。走后期（§8） |
| 只需要"有字的感觉"（背景街景、霓虹氛围） | ✅ **干净底板**，或形状暗示（见 §7.3） |
| 是**单个大词 / 短词**，能正对镜头、承载面静止、机位锁死 | ⚠️ **可试官方引号写法**，但需 ≥3 条候选 + 逐帧验收 + 后期兜底 |
| 是**字幕 / 对白字幕条** | ❌ **绝对不生成**。字幕是交付层，后期挂 |
| 是**品牌 logo** | ❌ 不生成（文字通道 + 品牌问题） |
| 是**手写体**（信、便签、信封） | ⚠️ 见 §7.5 |

## 7.3 「有字的感觉」但不出现真字：三种替代

| 方法 | 英文原句 | 中文 |
|---|---|---|
| **干净底板**（首选） | `A plain unbranded shopfront whose signboard is a blank pale rectangle; the shopfront, the window and the pavement show only colour, material and reflection.` | 无品牌标识的店面，招牌是一块空白的浅色长方形；店面、橱窗与人行道只呈现颜色、材质与反光 |
| **只给光不给字** | `A rectangle of warm neon light glows above the doorway, its surface out of focus and its edge soft.` | 门洞上方有一块暖色霓虹光板在发亮，表面处于焦外，边缘柔和 |
| **只给笔画节奏** | `A sign hangs above the door, its painted surface weathered and out of focus; the marks on it resolve into abstract strokes, not readable characters.` | 门上挂着一块招牌，漆面风化且处于焦外，上面的痕迹退化为抽象笔画，不是可读的字 |

> **第三句最适合都市夜景**：观众会读出"那是一块有字的招牌"，但不会去读内容。

## 7.4 必须出字时的四条硬条件（同时满足才可试）

| # | 条件 | 不满足的后果 |
|---|---|---|
| 1 | **单个大词 / 极短词**（≤ 2 个词，或单个汉字词） | 词一多，错一个整块就废 |
| 2 | **正对镜头**（square to the lens，无透视变形） | 斜角会让字形被重新采样，必然糊 |
| 3 | **承载面静止 + 机位锁死**（Static Shot） | 任何相对运动都会让字形逐帧抖动 |
| 4 | **停留不超过 3 秒** | 时间越长，累积漂移越多 |

**写法模板（四条件同时写入）**：

```text
A blue neon sign reading "OPEN ALL NIGHT" hangs flat and square to the lens above the
entrance; the sign does not move and the camera holds a static shot. The letters are
large, high-contrast and evenly lit, filling the upper third of the frame. The shot
holds for under three seconds.
```

**中文对照**：一块写着 "OPEN ALL NIGHT" 的蓝色霓虹招牌平正地悬在入口上方，正对镜头；招牌不动，镜头保持固定。字母大而高对比，受光均匀，占据画面上三分之一。本镜停留不足三秒。

> ⚠️ **即使四条全满足，也必须跑 ≥3 条并逐帧验收。** 这不是"稳了"，是"值得一试"。

## 7.5 文件 / 信件 / 信封：把视觉信息搬到听觉

**文件与信件是最容易踩坑的一类** —— 它们的文字**通常就是信息点本身**。

| 场景 | 错误做法 | 正确做法 |
|---|---|---|
| 她读一封分手信 | 特写信纸上的字 | **特写她的脸** + 她**念出**信里的话（§3.4） |
| 他看到合同上的金额 | 特写数字 | 他的手指停在某一行 → 抬头 → `<d>[Chinese] 三百万。</d>` |
| 信封上的地址 | 特写地址 | `A cream envelope held close to the lens; the handwriting on it is out of focus and illegible.` |
| 一份文件需要被识别 | 特写文件抬头 | 只拍**抬头之外的部分**（签名区、印章、页边的手指），抬头交给后期贴 |

**信封 / 手写的"不可辨认"写法库**：

| # | 英文原句 | 中文 |
|---|---|---|
| 1 | `The letter is covered in dense handwriting seen from too far to read, the lines reduced to grey texture.` | 信纸上写满致密的手写字迹，距离远到无法阅读，字行退化成灰色纹理 |
| 2 | `A fountain pen rests across the page; the written lines beneath it are softened by the shallow depth of field, unreadable.` | 一支钢笔横放在纸页上，下面的字行被浅景深柔化，无法阅读 |
| 3 | `The document's header is cropped out of frame at the top; only the lower half of the page and her thumb holding its edge are visible.` | 文件抬头被裁在画面上方之外，只有纸页下半部和她捏着边缘的拇指可见 |

> **第 3 句是文件类镜头的通用解**：让关键信息**自然地出画**，而不是"在画里但看不清"。出画是构图决策，观众不会追问；在画里看不清，观众会盯着看。

## 7.6 招牌 / 路牌 / 门牌：分级处置表

| 元素 | 是否承载信息 | 处置 | 英文原句 |
|---|---|---|---|
| **街景背景招牌** | 否 | 干净底板 / 只给光不给字 | `The street behind her is lined with unbranded shopfronts whose signboards are blank, wet with rain and reflecting the traffic lights.` |
| **店名（需要被认出）** | 是 | **后期贴图** | 生成时：`A plain shopfront with a blank rectangular signboard above the door, evenly lit, square to the lens, the camera holding a static shot.` |
| **路牌** | 可能 | 干净底板；需要时后期 | `A blank green road sign stands at the corner, its face catching the streetlight.` |
| **门牌号** | 是（往往是关键线索） | **后期贴图**，或改由对白说出 | 生成时：`A small blank brass plate is mounted beside the door; it is too far from the lens for any marking on it to resolve.` |
| **电梯楼层数字** | 是 | 后期；或只拍跳变的光 | `The floor indicator above the door is a small out-of-focus rectangle of red light; the digits on it never resolve into readable numbers.` |
| **霓虹招牌（氛围）** | 否 | 只给光不给字 / 官方引号（若必须） | `A red neon tube traces an abstract loop pattern above the doorway.` |

**中文对照**：① 她身后的街道两侧是无品牌标识的店面，招牌是空白的，被雨打湿，映着红绿灯的光。②（店名需被认出时）门洞上方一块空白的长方形招牌板，受光均匀、正对镜头、机位固定。③ 街角立着一块空白的绿色路牌，牌面反着路灯的光。④ 门边一块空白的黄铜小牌，离镜头太远。⑤ 门上方的楼层指示器只是一个焦外的红色小矩形。⑥ 门洞上方一圈红色霓虹灯管勾出抽象的环形图案。

## 7.7 字幕：绝对不生成

| 类型 | 处理 |
|---|---|
| 对白字幕 | **后期挂**。H3 原生出声，字幕按成片规格在剪辑阶段挂 |
| 标题字幕 / 集名字幕 | **后期挂** |
| 画面内的"手机短信字幕条"（把短信内容做成字幕条打在画面上） | ✅ **推荐替代** —— 见下方 |

> 💡 **把"屏幕内容"改成"画面字幕条"，是本 skill 最省事的一招。**
> 原本要在手机屏上渲染的短信，改成**打在画面下方的字幕条**（后期挂），手机本身走 B 档（不可辨认）。
> 观众读到的信息完全一样，风险从"最高"降到"零"。**都市题材里大量"收到短信"的镜头都可以这样处理。**

## 7.8 「无文字」的正向锚定写法（不要用裸名词否定串）

主模板 §6.4-F 的判定表：

| 写法 | 判定 |
|---|---|
| 裸名词否定 `no six fingers` / `no text, no letters` | ❌ **禁用** —— 名词本身进条件分布，反向激活 |
| 裸否定句 `do not generate six fingers` | ⚠️ 弱 —— 模型要先构想再否定 |
| **正向锚定** | ✅ 最强 —— 占据描述位，畸形解无处安放 |
| **正向锚定 + 末尾最多 1 句 B 类 `Do not`** | ✅ **H3 最优** —— 结构限收边位置，内容限 B 类（§7.8.1） |

→ **本 skill 全篇的屏幕与文字描述，一律用最后一档。** 已按此标准自查并修完全部模板（原稿中 13 处裸名词/裸否定句已改正，见 §10.1 检查项 11）。

### 7.8.1 正向锚定串（推荐，全篇通用）

| 版本 | 写法 | 判定 |
|---|---|---|
| 主模板附 1 原版 | `No text, no letters, no numbers, no logos, no watermarks, no subtitles anywhere in frame.` | ⚠️ 成串裸名词否定 |
| **升级版（推荐）** | `Every surface in frame that could carry lettering — <列举> — is a plain, unmarked surface showing only colour, material and reflection, and every one of them holds that way from the first frame to the last.` | ✅ **纯正向锚定（含时长维度）** |

**原理**：正向句把"该是什么"钉死，模型就没有"要不要写字"的抉择空间。

> ⚠️ **收边 `Do not` 的内容限 B 类**（team-lead 裁定）：只能写**变化 / 时长 / 运动**
> （`holds steady` / `does not change` / `does not move`）；**A 类**（能指给人看的具体
> 元素，`letters` / `numbers` / `logos` / `extra fingers`）**一律改正向**，不得写进
> `Do not`。**混合句就低不就高** —— 一句里含 A 类成分，整句判 A 类；**开放量词
> `anything` 按 A 类判**。确无正向写法时按【待验证】申报实测，不默认豁免。

### 7.8.2 ⚠️ `<列举>` 必须按场景改写（不能全剧套一串）

**列举画面里不存在的物件本身就是一种激活风险** —— 在病房里列 `the envelope`、在车里列 `the signboard`，等于把无关物件喂进条件分布。**规则：每个场景只列它画面里真实存在的 2–3 个表面。**

| 场景 | `<列举>` 取值 |
|---|---|
| 客厅 / 书房 | `the book spines, the envelope, the framed print` |
| 车内 | `the dashboard, the instrument panel, the door trim` |
| 街景 | `the signboard, the shopfront window, the road sign` |
| 办公室 / 会议室 | `the folder, the whiteboard, the name plate` |
| 病房 | `the bed rail, the bedside cabinet, the monitor casing` |
| **含手机屏的镜** | 必须把 `the phone screen` 排进列举的第一位 |

> 这条口径由 `h3-env-scene` 提出、本 skill 采纳。**光照走正向锚定不占额度；本串收尾用正向（`holds that way...`），不写 `Do not`（见 §7.8.1）。**

> ⚠️ **转写层不得退回否定句。** 中文正向串（如"素面无标记"）转英文时极易被译回 `No text` / `no letters`。**中英两版都要正向写**，转写时不得简化成否定。

### 7.8.3 正向锚定关键词表（与 `h3-env-scene` 合并版，全队共用）

| 层级 | 正向锚定词 | 适用维度 |
|---|---|---|
| **物件级** | `blank` / `plain` / `unmarked` / `unbranded` / `a single uniform ___ field` | 表面、招牌、屏幕、信封、背板 |
| **状态级** | `holds steady` / `the only ___ is the one named above` / `falls into shadow` | 光照、运动、暗部、时长 |

> 物件级由 `h3-screen-text` 归纳，状态级由 `h3-env-scene` 归纳。两套互补，建议全队统一引用本表。

**物件级这五个词能替代绝大多数"没有文字"的否定句：**

| ❌ 别写 | ✅ 写 |
|---|---|
| `a signboard with no letters` | `a blank signboard` |
| `a phone with no visible logo` | `a plain, unbranded back panel` |
| `the screen with no interface on it` | `the screen is a single uniform cool-white field` |
| `the envelope with no address` | `a blank cream envelope` |
| `no other light source is visible` | 见 `h3-env-scene`：夜景用 `the rest of the frame falls into shadow with no detail`，日景用 `all the light in the room comes from this one source` |

---

# §8 后期合成工作流

> 这一节是 A 档的落地手册。**B 档不需要后期，可跳过。**

## 8.1 完整流程图

```
生成（A1 亮屏纯色 / A2 灭屏纯黑）
  ↓
① 平面跟踪（跟屏幕四角，走内缩安全区）
  ↓
② Corner Pin 贴 UI 设计稿
  ↓
③ 混合模式（Screen / Add）
  ↓
④ 反射层单独抠出，叠在贴图上方（5–15%）
  ↓
⑤ 光溢出 spill（冷色，遮罩 + 大羽化）
  ↓
⑥ 运动模糊（shutter blur，180° 快门角 ≈ 1/48s）
  ↓
⑦ 手指遮挡层（roto，手指压在贴图上方）
  ↓
⑧ 内容动效（气泡逐条出现 / 滚动 / 进度条）
  ↓
⑨ 验收：抽 5 帧看角点是否漂
```

## 8.2 逐步骤要点

| 步 | 动作 | 要点 |
|---|---|---|
| ① | **平面跟踪** | 跟**屏幕四角**而非手机轮廓（手机有厚度，跟轮廓会跟着透视抖）；跟踪区内**向内缩 5–10%** 避开周期性的手指遮挡；**反光是干扰不是特征**（会随镜头游走），改用听筒/边框内沿当特征点。**A2 黑屏无特征点 → 改跟手机外框**，再内缩到屏幕区 |
| ② | **贴图源** | **用 UI 设计稿，不用真机截图** —— 真机截图带状态栏（与剧情时间对不上）和无关通知，改字换语种要重做。用 Figma/PS 出图，导出带透明通道的 PNG |
| ③ | **混合模式** | **A1 亮屏**用 `Screen` / `Add`（线性减淡，屏幕是发光体，内容是"加上去的光"不是"盖上去的纸"）；**A2 黑屏**用 `Screen`（黑底等效替换）。❌ 不用 `Normal`（丢自发光感）/ `Multiply`（黑底上全黑） |
| ④ | **反射层** | 原素材的屏幕反光**不要擦掉**，单独抠出叠在贴图**上方**，`Screen` 模式，强度 **5–15%**。真实内容是"透过玻璃看到的"、反光在更前，贴图压在反光上就会显出"内容在玻璃外面"的贴纸感 |
| ⑤ | **光溢出 spill** | 遮罩区 = 下巴底面 / 下脸颊 / 衣领 / 握持手指内侧 / 手机边框；颜色取屏幕主色（通常冷白 `#DCE6F0` 附近，贴暖色画面则跟随）；强度取原素材 spill **±10%**（大改就与生成光影脱节）。**若贴的内容有明暗变化，spill 必须跟着变** —— 把 UI 稿亮度做成曲线驱动 spill 层 opacity |
| ⑥ | **运动模糊** ← **最常穿帮** | 贴图是静止渲染的，不加模糊就是"贴纸感"。手机静止＋镜头缓推 → 轻微运动模糊；手机跟手动 → 用跟踪数据反算**矢量模糊**；快速甩动 → **改分镜**（几乎做不干净）。参数：180° 快门角 @ 24 FPS ≈ 1/48s（H3 输出即 24 FPS） |
| ⑦ | **手指遮挡层** | 把手指 roto 抠出压在贴图**上层**（H2 双手捧握时拇指压屏幕下缘）；手指边缘要有 spill 否则显黑；阴影层压在贴图上、手指层下 |
| ⑧ | **内容动效** | **静止贴图 = 死图**。短信 → 气泡逐条出现（停 0.5s 再出下一条）；刷视频 → 换动态素材 + 进度条；列表 → 极缓滚动。**兜底**：任何贴图都加一道缓慢下移的 shimmer 高光，观众就会认为"那是块亮着的屏幕" |

> 【推】"5–15%""±10%"是经验值，无公开基准。**以原素材 spill 为基准眼校，不要凭空设定。**

### ⑨ 验收

```
□ 抽 5 帧（首、25%、50%、75%、末）看角点是否漂
□ 反光层是否始终在贴图上层
□ 手指遮挡层是否正确遮挡
□ spill 强度是否与新内容亮度匹配
□ 运动模糊是否与原素材边缘一致
□ 快速播放一遍，看有没有"跳动"（角点抖的征兆）
□ 静帧定格 3 秒，看贴图是否明显"太清晰"（缺少模糊的征兆）
```

## 8.3 与原视频的光影一致性：三大检查点

| 检查点 | 看什么 | 不一致的表现 |
|---|---|---|
| **色温** | 屏幕内容主色 vs 脸上 spill 的颜色 | 贴了暖黄视频、spill 还是冷白 → 一眼假 |
| **亮度量级** | 屏幕相对亮度 vs spill 强度 | 屏幕很亮但脸上没光 → 光"没照出来" |
| **时域同步** | 屏幕明暗变化 vs spill 变化 | 屏幕闪了一下、脸上的光没闪 → 穿帮 |

> **时域同步最容易被漏，也最致命。** 观众对"光和时间不同步"的敏感度远高于对"亮度差一点"的敏感度。

---

# §9 小尺度精细交互的硬阻断

## 9.1 定义与判定

主模板 §8.3 硬阻断清单原文：

> | **小尺度精确对准**（钥匙插锁、指尖对位） | 无 3D 朝向跟踪与刚体约束 | 避开极端特写 + 多条挑选 |

**判定口诀**：**只要"两个刚体的相对位置必须精确"，就是硬阻断。**

| 是硬阻断 | 不是硬阻断（可放宽） |
|---|---|
| 指尖点在某个具体图标上 | 手指搭在屏幕边缘（无目标） |
| 键盘上敲出具体的字 | 手放在键盘上（不敲） |
| 手机摄像头对准二维码 | 举着手机朝向某个方向 |
| 钥匙插进锁孔 | 手握在门把上（已插入状态） |
| 拨号盘拨出具体号码 | 拇指在屏幕下方（不接触） |

## 9.2 为什么提示词解决不了

模型**没有 3D 朝向跟踪与刚体约束**，学的是"合理外观的像素统计"，不是"物理的因果逻辑"。ICML 2025（字节 Seed × 清华）：*"scaling alone is insufficient for video generation models to uncover fundamental physical laws"*（Kang et al. 2025）。

→ **这不是提示词写得不够好的问题，是模型类别的结构性缺陷。改一百版提示词都是浪费。**

## 9.3 替代动作表（直接照抄）

| 想要的动作 | ❌ 原设计 | ✅ 替代（按推荐度排序） |
|---|---|---|
| **打字发短信** | `She types a message on her phone.` | ① 她已经打完了，拇指停在屏幕上方，然后放下手机<br>② 手机平放桌上，她的食指轻触一下屏幕，然后收回<br>③ **最好**：她盯着屏幕念出台词（§3.4），不拍打字 |
| **解锁手机** | `She unlocks her phone with her thumb.` | 手机**开场就已经亮着**（开场即终态，§6.2） |
| **滑动刷视频** | `She swipes up to the next video.` | 中景，不给手部特写；**用屏幕光的跳变暗示"切了下一条"**（§5.2） |
| **扫码支付** | `She scans the QR code with her phone.` | ① 她举着手机对着柜台，然后点头，收起手机<br>② 后期贴二维码 + 对勾（A 档） |
| **接电话** | `She slides to answer the call.` | 手机**已经在耳边**（开场即终态）；或：她看着响铃的手机，然后说 `<d>[Chinese] 喂？</d>` |
| **看时间** | `She taps the screen to check the time.` | 她抬起手腕看表（手表比手机稳，且表盘数字可后期）；或她念出 `<d>[Chinese] 十一点四十。</d>` |
| **拍照** | `She presses the shutter button.` | 她举着手机对着前方，机身轻微一顿（快门已按下的**结果态**），然后放下 |

**"开场即终态"是本节的通用解**：把"完成一个交互"改成"呈现交互已经完成的状态"。前者要求模型模拟物理过程，后者只要求模型画一个静态姿势。

**替代动作的英文写法示例**：

```text
She is already holding the lit phone in both hands, her thumb resting along the lower
edge of the screen and not moving. She is not typing, not swiping and not tapping;
her hands hold the phone still for the entire shot.
```

**中文对照**：她已经用双手握着亮着的手机，拇指搭在屏幕下缘且不动。她全程**只是握着**——不打字、不滑动、不点按；她的手在整镜中稳稳地托着手机。

## 9.4 硬阻断的处置

分镜表里 `处置动作` 字段填 **`硬阻断`** 时，**`备选方案` 强制非空**（主模板 §附 2）。

> **遇到这几类，第一反应应该是改分镜，不是改提示词。** 把"钥匙插进锁孔"改成"手已经握在门把上"，一秒钟解决问题；硬写提示词，十次也过不了。

---

# §10 检查清单 + 正反例速查表

## 10.1 提交前检查（屏幕 / 文字专项，12 条）

```
□ 1. 屏幕镜选了档位吗？（A / B / C / B0）没选就默认是 B
□ 2. 提示词里【没有】短信正文 / 招牌文字 / 文件内容？
      （唯一例外：§7.4 四条硬条件全满足 + 官方英文双引号）
□ 3. 屏幕镜的景别是否 ≥ 中近景？（禁止大特写怼屏幕）
□ 4. 是否显式声明了"不可辨认"或"干净底板"？（不能什么都不说）
□ 5. 手机光是否被声明为【次级补光】，主光方向未变？
□ 6. 是否有 [PHONE-POSE] 锁定块，且三镜逐字复制？
□ 7. 是否有 [PHONE ASSET LOCK]，且用的是「plain, unbranded, unmarked back panel」
      正向说法（不是 `no visible brand logo`）？
□ 8. 手机外放的声音写进了 integrated_multimodal_description 吗？（不是 non_diegetic_music）
□ 9. 一镜内需要稳住的小物件 ≤ 2 件吗？
□ 10. 每镜最多 1 句 Do not，且该句之前有正向描述？
□ 11. 屏幕/文字用的是正向锚定（blank / plain / unmarked / unbranded / a single uniform
      ___ field），没有成串裸名词否定？（见 §7.8）
□ 12. 若写了收边 `Do not`，内容是 **B 类**（变化 / 时长 / 运动）而非 A 类？（§7.8.1）
```

## 10.2 生成后看片检查（屏幕专项，8 条）

```
□ 1. 逐帧看屏幕：有没有冒出乱码 / 错字 / 中英混杂？
□ 2. 屏幕内容有没有【自己变化】？（无人操作时自己刷新 = 高危信号）
□ 3. UI 结构有没有重复卡片 / 融化 / 气泡错位？
□ 4. 手机有没有【翻面】？（正反面翻转已知高发）
□ 5. 手机有没有换手？型号有没有变？
□ 6. 屏幕的冷光是不是打在脸的【下半部】？（打在上半部 = 光位错）
□ 7. 屏幕光与 spill 的变化是否【同步】？
□ 8. 步数是不是 6–8？（是 4 就先抬步数重跑，别急着改提示词）
```

## 10.3 正反例速查表（核心 20 条）

### A. 屏幕内容

| # | ❌ 反例 | 为什么错 | ✅ 正例 |
|---|---|---|---|
| 1 | `She reads a message saying "今晚八点老地方".` | 硬写短信原文，必乱码 | `The screen content is softened by motion blur and reflection, illegible.` |
| 2 | `She looks at her phone.` | 什么都不说 = 模型自动补界面 | `She looks at her phone; the screen is turned away from the camera and its content is illegible.` |
| 3 | `The screen is black.`（但她明明在看） | 灭屏与"在看"矛盾 | `The screen shows a single uniform cool-white field across its entire surface.` |
| 4 | `Extreme close-up of the phone screen showing the message.` | 小尺度精确对准 = 硬阻断 | `A medium shot frames her holding the phone; the screen is seen at an oblique angle, unreadable.` |
| 5 | `No text on the screen.` | 观众会觉得屏幕坏了 | `The screen is a plain lit surface showing only colour and reflection.` |
| 6 | `The screen shows a WeChat conversation.` | 品牌 App 界面 = 文字 + UI + 版权三重问题 | `The screen shows an unreadable interface softened by motion blur.` |
| 7 | `The camera pushes in to reveal the message.` | 推近到屏幕 = 内容必然要成像 | `The camera pushes in to a close-up of her face, not of the phone.` |
| 8 | `She types the reply, then sends it.` | 精细交互硬阻断 | `She is already holding the lit phone; her thumb rests along the lower edge and does not move.` |

### B. 手机作为道具

| # | ❌ 反例 | 为什么错 | ✅ 正例 |
|---|---|---|---|
| 9 | `a black smartphone` | 描述太泛，跨集会漂移 | `a matte-black slab-style smartphone with rounded corners and a plain, unbranded, unmarked back panel` |
| 10 | `She holds the phone.` | 没锁哪只手，会换手 | `She holds the phone in her RIGHT hand and does not switch hands at any point.` |
| 11 | `She takes the phone out of her pocket, then holds it up.` | 掏取 = 精细交互 + 状态突变 | `She is already holding the phone in her right hand at about chest height.` |
| 12 | `The phone is tilted slightly.` | "稍微"不可度量 | `The phone is tilted roughly thirty degrees, screen facing her face, back facing the camera throughout.` |
| 13 | 写了耳环 + 戒指 + 手机 + 手表 | 一镜小物件 >2 件，必丢 | 只保留手机，其余从该镜描述中删除 |

### C. 光位与视线

| # | ❌ 反例 | 为什么错 | ✅ 正例 |
|---|---|---|---|
| 14 | `The phone lights her face.` | 没说从哪打，模型会乱给 | `The cool white light from the screen lights the underside of her face from below.` |
| 15 | 只写屏幕光，不提主光 | 与"单一主光"冲突，身份会晃 | `A single warm key light from camera right remains the main light; the phone adds a secondary cool fill below only.` |
| 16 | `She looks sad at the message.` | 情绪名词，不可渲染 | `Her eyebrows draw together, then her jaw tightens, then her gaze freezes.` |
| 17 | `She looks to her left at the phone.` | 角色左右有歧义 | `Her gaze drops to a fixed point just below the lens.` |

### D. 画面内文字

| # | ❌ 反例 | 为什么错 | ✅ 正例 |
|---|---|---|---|
| 18 | `A shop sign saying it is open for business.` | 模糊表述，官方明令禁止 | `A red neon sign reading "营业中" glows above the doorway.`（或：干净底板） |
| 19 | `A neon sign reading "Grand Opening — 50% Off Everything This Weekend Only".` | 词太多，错一个整块废 | 长文案一律后期；生成时只给 `a blank signboard` |
| 20 | 让 H3 生成对白字幕 | 字幕是交付层，且文字高风险 | H3 原生出声，字幕后期挂 |

## 10.4 一页纸速查卡

```text
┌─────────────────────────────────────────────────────────────┐
│  H3 屏幕与文字 · 一页纸                                      │
├─────────────────────────────────────────────────────────────┤
│ 默认档位        B 档（主动认领不可辨认）                      │
│ 零风险档位      B0（不给屏幕，只给光 / 只给背板）             │
│ 交付级必须      A 档（干净底板 + 后期 corner pin）            │
│ 能用对白替代的  一律替代（H3 原生出声，100% 准确）            │
│ 字幕           永远后期挂                                    │
├─────────────────────────────────────────────────────────────┤
│ 三条硬规则                                                   │
│  1. 不在提示词里写短信原文                                   │
│  2. 不用极端特写怼屏幕                                       │
│  3. 手机正反面翻转 = 已知高发，参考图锚定 + 多条挑 + 后期      │
├─────────────────────────────────────────────────────────────┤
│ 拍手机 = 拍光，不是拍像素                                    │
│  · 冷白光打脸的下半部                                        │
│  · 主光仍是那盏灯（手机光只是次级补光）                       │
│  · 内容变化 → 外化成光的调制（flicker / dim / flash）         │
│  · 观众要的是情绪，不是像素                                   │
├─────────────────────────────────────────────────────────────┤
│ 手机外放 = diegetic → 写进 integrated_multimodal_description  │
│ 屏幕崩了先抬采样步数（4 → 6–8），再改提示词                   │
└─────────────────────────────────────────────────────────────┘
```

---

# 附 A：完整 15 秒 3 镜示例（B 档 + 对白替代）

**场景**：深夜，她独自在家收到一条短信。本段信息点 = 她被甩了。

## 附 A.1 分镜表

| 镜 | 时长 | 景别 | 屏幕档位 | 运镜 | 内容 |
|---|---|---|---|---|---|
| A | 2.0s | 中景 | B0-3（手机面朝下放腿上，不发光） | Static Shot | 建立空间、暖色主光 |
| B | 11.0s | 中近景 → 缓推到脸部特写 | **B1（illegible）** | Push In small/slow | 拿起手机、点亮、看完、念出台词 |
| C | 2.0s | 特写（眼睛） | 不在画面 | Static Shot | 瞳孔收缩，冷光在下眼睑闪一下 |

## 附 A.2 H3 官方格式提示词（可直接提交）

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium shot frames a 28-year-old woman seated alone on a low grey fabric sofa in a dim living room at night, a warm floor lamp glowing on the right of frame as the only key light. She sits still, both hands resting flat on her thighs, a matte-black slab-style smartphone with rounded corners and a plain unbranded back panel lying face-down on her lap. A single soft warm key light from camera right at 45 degrees; the phone screen is dark and unlit. [Shot 2] At 00:02.000, the camera cuts to a medium close-up as she picks the phone up with both hands, fingers wrapped fully around its body, five fingers on each hand, natural finger length and spacing. The screen is turned up toward her face and away from the camera; its content is softened by motion blur and reflection, illegible. The screen now adds a secondary cool-white fill that lights the underside of her chin, her lower lip and her collar from below; the warm key light from camera right remains the main light and does not change direction. Her gaze drops to a fixed point just below the lens. The cool light on her face holds steady, then dims sharply in three quick steps; her eyebrows draw together, then her jaw tightens, then her mouth presses into a thin line. She says in a flat, empty voice (S1): <d>[Chinese] 他说，我们到此为止。</d> The camera pushes in with small amplitude at slow speed to a close-up of her face, not of the phone. [Shot 3] At 00:13.000, the camera cuts to a static extreme close-up of her eyes; her pupils contract slightly and the cool white light catches the wet edge of her lower eyelid, then holds; the screen content stays illegible throughout.

overall_soundscape: A quiet room at night with the faint hum of a refrigerator somewhere beyond frame. Fabric rustles softly as she shifts on the sofa. Her breathing is slow and audible, then stops for a moment.

non_diegetic_music: A single sustained cello note at a slow tempo, entering at the midpoint and fading out on the final beat.
```

**中文对照（要点）**：

> - **镜 1（无时间戳）**：实拍电影感，中景，28 岁女性独自坐在昏暗客厅的矮灰色布艺沙发上，画面右侧一盏暖色落地灯是唯一主光。她静坐不动，双手平放大腿，腿上正面朝下放着一部哑光黑色、圆角直板、素面无标识的智能手机。单一柔和暖色主光来自镜头右侧 45°；手机屏是暗的、不发光。
> - **镜 2（00:02.000）**：切中近景，她双手拿起手机，手指完全包住机身，每只手五指，长度间距自然。屏幕上仰朝脸、背对镜头，内容被运动模糊与反光柔化，**不可辨认**。屏幕此时增加一层冷白补光，从下方照亮下巴底面、下唇与领口；来自镜头右侧的暖色主光仍是主光，方向不变。她的视线落在镜头正下方的固定点。脸上的冷光先稳定，然后分三步快速变暗；眉毛收紧，下颌绷紧，嘴抿成细线。她用平淡空洞的声音说：「他说，我们到此为止。」镜头小幅慢速推近到她的**脸部**特写（不是手机）。
> - **镜 3（00:13.000）**：切静态眼部大特写，瞳孔微微收缩，冷白光勾出下眼睑的湿润边缘，然后保持。任何时刻都不要让屏幕内容变得可读。
- **音景**：夜晚安静的房间，画外有冰箱微弱嗡鸣；她在沙发上挪动时布料轻响；呼吸缓慢可闻，然后停顿一瞬。
- **配乐**：一个持续的大提琴长音，慢速，中点进入，最后一拍淡出。

## 附 A.3 为什么这样写（自查）

| 检查项 | 满足方式 |
|---|---|
| 无短信原文 | ✅ 全程未写短信内容，信息由 `<d>` 对白承载 |
| 景别 ≥ 中近景 | ✅ 最近到「中近景 → 脸部特写」，无屏幕特写 |
| 主动声明不可辨认 | ✅ `softened by motion blur and reflection, illegible` |
| 手机光是次级补光 | ✅ 显式声明 `the warm key light ... remains the main light and does not change direction` |
| 主光单一 | ✅ 全程 `camera right at 45°` |
| 手机资产锁 | ✅ 完整描述串，且用正向说法 `plain, unbranded, unmarked back panel` |
| 手部三档降级 | ✅ 走 H2 双手捧握，非 H3 单手操作 |
| 开场即终态 | ✅ 镜 1 手机已在腿上；镜 2 是"拿起"，不是"掏出" |
| 每镜最多 1 句 Do not | ✅ 仅末镜 1 句，B 类，且前面有正向描述 |
| 对白标签 | ✅ `<d>[Chinese] ...</d>`，说话人描述 `(S1)` 在标签外 |
| 时间戳 | ✅ Shot 1 无、Shot 2/3 有且递增、落在 15 秒内 |
| non_diegetic_music | ✅ 非 N/A，只写乐器/速度/动态，无情绪词 |
| 时长校验 | ✅ 2 + 11 + 2 = 15；每镜 ≥ 2.0s 设计下限 |

---

# 附 B：A 档与 C 档的最小可用片段

## 附 B.1 A 档（单镜 3 秒，纯屏幕特写，供后期贴图）

```text
integrated_multimodal_description: [Shot 1] Live-action, a static close-up holds a matte-black slab-style smartphone with rounded corners and a plain unbranded back panel, held flat in a still hand with five fingers visible below the frame edge. The screen fills most of the frame, square to the lens, and is lit as a single uniform cool-white field across its entire surface. The glass carries a soft-edged reflection of a window in the upper left. The phone stays still and the camera holds a static shot; the cool field of the screen holds steady in brightness. Do not let the screen change at any point in the shot.

overall_soundscape: A quiet indoor ambience with a faint low room tone; whatever the phone
plays is inaudible at this distance.

non_diegetic_music: N/A
```

> **中文要点**：静态特写，手机被一只静止的手平举正对镜头；**整个屏面亮成一片均匀冷白光场**，玻璃上只有一块柔和的窗户反光。手机不动、机位不动、冷光场亮度全程不变。末尾一句 `Do not` 收边。
> **后期时**：这一镜的屏幕是**均匀发光面**，corner pin 贴 UI 稿后用 `Screen` 混合，是 A 档里最容易做干净的一种。（这是 §2.2 A1 模板的"纯屏幕特写"变体。）

## 附 B.2 C 档（FL2VA 单镜 3 秒，参考图锚定）

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 3.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, a static close-up fills the frame with the screen of a matte-black smartphone held flat and square to the lens, its dark bezel visible on all four sides and a dim out-of-focus room behind it. The screen content remains unchanged throughout: the same layout, the same three message bubbles, the same sender name, the same timestamp, the same colours and the same positions. The only motion is a faint shimmer moving slowly down the glass and the very slight tremor of the hand holding the phone. The camera holds a static shot. By the end of the shot the screen is identical to the first frame. Do not let the screen
change at any point in the shot.

overall_soundscape: A faint room tone that holds steady from the first frame to the last.

non_diegetic_music: N/A
```

> **中文要点**：指令首行按官方 FL2VA 固定模板（`Picture 1` 无尖括号、`(from Shot 1)` 无方括号、`S.SS` 两位小数）。正文：静态特写，画面被正对镜头平举的手机屏幕填满，深色边框四边可见。**屏幕内容全程不变**——同样的布局、三个气泡、发件人名字、时间戳、颜色与位置。唯一的运动是玻璃上缓缓下移的一道微光与握持手的轻微颤动。镜头固定，末帧与首帧一致，末尾一句 `Do not` 收边。

> ⚠️ **C 档注意**：`The screen content remains unchanged throughout.` 必须在**镜内开头**（关键约束不埋中段，主模板 §6.5）。

---

# 附 C：【待验证】清单与实测方法

> **本 skill 中下列结论无法从公开资料确证，标注【待验证】。下列实测方法均可在 1–2 小时内跑完，建议量产前做完。**

| # | 待验证命题 | 为什么不确定 | 实测方法 | 采纳阈值（建议） |
|---|---|---|---|---|
| 1 | **B 档"不可辨认"的实际成功率** | 无公开测试集；"模型还是出了可读乱码"的发生率未知 | 固定同一条 B 档提示词，跑 **20 次**（步数 6–8），统计「出现可读乱码」与「被判为屏幕坏了」的比例 | 可读乱码 ≤ 10% 可量产 |
| 2 | **C 档在不同时长下的漂移临界点**（2s / 3s / 5s） | 官方只保证"保留程度"，无时长-漂移数据 | 同一 UI 参考图，分别生成 2s / 3s / 5s，各 10 条；逐帧抽 5 帧，人工判「内容是否仍可辨认且未重排」 | 找出成功率 ≥ 80% 的最大时长 |
| 3 | **A 档后期工时的实际倍率**（本文估 2–3×） | 经验估计，无基准 | 台账记录 10 个屏幕镜的实际后期分钟数，与同难度非屏幕镜对比 | 校准倍率，重估 A/B 档的成本分界 |
| 4 | **`fully_preserved` vs `partially_preserved` 对握持手机姿态的影响** | 官方只给了四个标记的**定义**，未给"姿态 vs 像素"的选择指引 | 同一镜分别用两种标记各跑 10 条，统计「手机姿态崩 / 屏幕被强行摆正」的比例 | 取崩坏率低者 |
| 5 | **2K 是否改善屏幕小字** | 乐观方断言 vs 8-bit 量化机制，两方均无 H3 实测 | 同一条含 12pt 等效小字的提示词，768p 与 2K 各跑 10 条，逐帧判读 | — |
| 6 | **采样步数对屏幕质量的影响曲线** | 官方直播只给了 4 / 6–8 的粗分档，无屏幕专项 | 同一提示词在 4 / 6 / 8 步各跑 10 条，统计屏幕乱码率 | 若 8 步显著优于 6 步，屏幕镜单独提步数 |
| 7 | **"只给光不给字"招牌写法能否稳定生效** | 该写法为本 skill 构造，未经实测 | 跑 20 次，统计「仍出现可读字形」的比例 | ≤ 15% 可量产 |
| 8 | **手机正反面翻转的发生率与参考图锚定的改善幅度** | 官方/三方只说"已知高发"，无数字 | A 组无参考图、B 组有 `<Picture N>` 姿态参考，各 20 条，统计翻转率 | 改善 ≥ 30 个百分点才值得占一个参考图槽 |

**通用实测纪律**（照抄自 `防翻车限制词库_H3版.md` §10）：① **必须在真实运动条件下测**（静止画面测出的成功率无意义）；② **样本量 ≥ 20 次**；③ 固定其他变量，只改被测项；④ 登记自建指标 `Screen Legibility Rate (SLR)` =「屏幕内容符合预期且未出现可辨错字」的比例，目标 ≥ 80%；⑤ **步数不达 6–8 的失败结论无效**，必须重测。

---

# 附 D：来源与交叉引用

## 本 skill 依据的文件

| 文件 | 使用部分 |
|---|---|
| `MiniMaxH3-小说转分镜-完整模板.md` | §3.1 三镜分工、§3.2.1 时长、§3.5 类型库、§5.2 资产表、§6.4-E 手机屏与资产 / F 限制词、§6.5 信息埋没、§7 官方格式、§8.3 硬阻断清单、§8.6 处置四级、§附 2 风险字段 |
| `MiniMax-H3-官方提示词规范调研报告.md` | §2 三核心字段、§3 时间戳、§4 运镜术语、§5 说话人与对白、§6 画面内可见文字、§7 Ref2VA、§8 硬性参数、§9 避坑清单 |
| `防翻车限制词库_H3版.md` | §1 对白与音频、§2 资产锁定、§3 否定句稳妥口径、§4 手部、§8 文字与屏幕、§9 物理与空间、§10 道具资产、§11 多镜结构、§12 手机屏幕、§14 采样步数 |
| `防翻车限制词库_补充勘误_H3专属.md` | §四 硬阻断重判、§5.2 手机屏幕三档、§6.1 180° 轴线 |

## 官方原文出处

- `https://github.com/MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/base-en.txt`（T2VA / I2VA / FL2VA / L2VA）
- `https://github.com/MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/ref-en.txt`（Full-Reference / Ref2VA）
- `https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir`（官方 API 文档）
- `https://huggingface.co/MiniMaxAI/MiniMax-H3`（官方模型卡）

> **协作提示**：§4.4 的 H1/H2/H3 手部降级档与 `h3-action-body` 共用分级原则；**握持手机定级「中高」**。冲突时以 `h3-action-body` 为准。