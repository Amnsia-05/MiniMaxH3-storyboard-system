---
name: h3-env-scene
description: 海螺 H3 视频提示词中「环境 / 场景 / 光影 / 天气 / 空间关系」的写法规范与可复制模板。触发词：H3环境描写、H3场景提示词、H3光影、H3空间距离、场景一致性、室内外景描写、H3天气。
agent_created: true
---

# 海螺 H3 · 环境 / 场景 / 光影 / 天气 / 空间关系 提示词写法

本 skill 只解决一个问题：**一段 H3 提示词里，"人在哪儿、光从哪来、天怎么样、谁站在哪个位置" 这些句子该怎么写**。

---

## 0. 定位、上游与铁律

### 0.1 本 skill 管什么 / 不管什么

| 管 | 不管 |
|---|---|
| 环境可见物件的写法 | 角色外观与服装（→ 角色卡、主模板模块五） |
| 室内 / 室外场景描述串库 | 对白与说话人（→ 主模板 §7.6，`<d>` 规范） |
| 光影系统（方向 / 色温 / 光质 / 光比） | 运镜术语表（→ 主模板 §7.5） |
| 天气与大气（雨 / 雪 / 雾 / 风 / 逆光 / 丁达尔） | 分镜时长校验（→ 主模板模块三 §3.2） |
| 空间关系与人物距离 | 台词容量换算（→ 主模板模块四） |
| 跨镜 / 跨段 / 跨集场景一致性 | 参考模式六段结构（→ 主模板 §7.8） |
| `overall_soundscape` 的环境音部分 | 采样步数与返工 SOP（→ 主模板 §8.4） |

**本 skill 是主模板的"环境层插件"**，不取代主模板。冲突时以主模板为准。

### 0.2 执行前必读（每次都要读，不要凭记忆写）

| 文件 | 路径 | 读什么 |
|---|---|---|
| 主模板 | `C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44\MiniMaxH3-小说转分镜-完整模板.md` | 模块五 §5.5 场景表、模块六 §6.3 锁定块、§6.4 空间要素、模块七官方格式 |
| 官方规范调研 | `C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44\MiniMax-H3-官方提示词规范调研报告.md` | 三核心字段、时间戳、运镜术语、红线清单 |
| 防翻车词库 | `C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44\防翻车限制词库_H3版.md` | §9 物理与空间、§13 多镜头一致性、§2 资产锁定 |
| 叙事侧方法论 | `C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44\叙事侧方法论_小说拆解与15秒3镜结构.md` | §2.3 衔接镜类型库、§2.4 匹配三锚点、§3 分镜表字段 |

### 0.3 三条铁律

1. **不编造。** 查不到出处的数字一律标【待验证】并附实测方法。宁可写"没数据，你自己测 10 次"，也不给一个看起来合理的假数字。
2. **英文原文保留。** H3 提示词正文、场景串、官方术语一律英文原文；中文只作解释与对照，**不要把中文段再翻译一遍塞进提示词**（重复描述 = 竞争性约束，见防翻车词库 §11.5）。
3. **可执行优先。** 表格 > 模板 > 可复制例句 > 论述。

### 0.4 证据标注（沿用主模板 §0.2，不另发明）

| 标记 | 含义 |
|---|---|
| 【官方】 | MiniMax H3 官方文档 / 模型卡 / 官方 GitHub 仓库原文 |
| 【业界】 | 影视摄影与 AI 视频的公开行业通行做法 |
| 【推断】 | 由通用原理推导，**未经大规模实测** |
| 【工程取值】 | 本流水线人为设定的常数，可按你的实测覆盖 |
| 【待验证】 | 无公开数据，需你自己跑实测，**本 skill 一律给实测方法不给数字** |

### 0.5 H3 硬约束速查（与本 skill 直接相关的部分）

全部为【官方】，出处为主模板 §7.11 与官方调研报告 §8。

| # | 约束 | 值 |
|---|---|---|
| 1 | 提示词上限 | **7000 字符**（按字符计，1 汉字 = 1 字符，非 token） |
| 2 | 三核心字段固定顺序 | `integrated_multimodal_description` → `overall_soundscape` → `non_diegetic_music`，**不可调换** |
| 3 | `overall_soundscape` | **1–4 句英文**，一段连续段落；N/A 仅当用户明确要求全片静音 |
| 4 | `non_diegetic_music` | **1–3 句英文**；只写乐器 / 速度 / 节奏 / 动态，**禁止情绪词** |
| 5 | 第一镜时间戳 | **永远不加**；后续 `At 00:SS.mmm`（**三位小数**）；指令首行 `S.SS`（**两位小数**） |
| 6 | 运镜 | **一镜一个主运镜**，官方术语 + `with small\|large amplitude at slow\|fast speed` |
| 7 | 否定句 | 每镜**最多 1 句 `Do not ...`**，置末尾、前有正向描述。**重复正向的删，补充正向未覆盖的留**（见 §1.6） |
| 8 | 可见文字 | 英文双引号包裹，逐字保留不翻译 |
| 9 | 图生视频与全能参考互斥 | `first_frame`/`last_frame` 与 `reference_*` 不可同时出现 |
| 10 | 采样步数 | 试拍 4 步，出片 **6–8 步**（【三方·官方直播转述】，数值为社区共识） |

### 0.6 环境描写在提示词里的位置

主模板 §6.5 的优先级排序规定：**第 4 层：环境 + 光位（一个主光，一个方向）**。

含义有两层：

- 环境的**权重低于**运镜、主体、动作 → 不要把场景描写铺在最前面抢注意力
- 但环境是**跨镜一致性的地基** → 它必须**外置到场景卡**（§7），三镜逐字复制，而不是每镜临场重写

> **一句话**：环境不抢镜头的权重，但必须抢"一致性"的权重。

---

## 1. 环境描写基本原则

### 1.1 唯一原则：写可见物件，不写氛围词

模型不渲染"氛围"，它渲染"物体 + 光"。写 `a cozy living room`，模型只能从训练分布里随机采样一个客厅；写 `a low grey fabric sofa, a blank off-white wall, a floor lamp at the right of frame`，模型才有确定解。

**判定口诀：这句话能不能被画出来？画不出来就不是提示词，是剧本。**

### 1.2 正例 / 反例对照表（12 组，逐条可直接改用）

| # | ❌ 氛围词 / 抽象词 | 为什么不行 | ✅ 可见写法（英文原文） | 中文对照 |
|---|---|---|---|---|
| 1 | `a cozy living room` | cozy 不可渲染 | `a low grey fabric sofa against a blank off-white wall, a floor lamp with a warm-white shade at the right of frame, a dark wood coffee table in front of the sofa` | 靠墙放一张低矮的灰色布艺沙发，墙面留白呈米白色，画面右侧一盏暖白灯罩落地灯，沙发前一张深色木质茶几 |
| 2 | `an eerie corridor` | eerie 是观感不是物体 | `a narrow corridor with pale green wall tiles, a row of ceiling lights along its length, the last ceiling light is dark, a pale linoleum floor` | 狭窄走廊，墙面为浅绿色瓷砖，一整排顶灯沿走廊排列，最后一盏顶灯是熄灭的，地面为浅色塑胶地板 |
| 3 | `a luxurious office` | 奢华是评价 | `a dark walnut desk, a low bookcase against the left wall, a brass desk lamp at the left of frame, a floor-to-ceiling window behind the desk` | 一张深胡桃木书桌，左墙一排矮书柜，画面左侧一盏黄铜台灯，书桌后方一整面落地窗 |
| 4 | `a romantic restaurant` | 浪漫靠光不靠词 | `a small dining room with six round tables, a candle in a glass holder at the centre of the nearest table, warm amber light pooling on the tabletop, the far end of the room falling into shadow` | 小餐厅内六张圆桌，最近一张桌中央一只玻璃烛台蜡烛，暖琥珀色光在桌面聚成一滩，房间远端没入暗部 |
| 5 | `a tense atmosphere` | 气氛完全不可渲染 | 拆成可见项：`two people stand two arm's lengths apart and this distance stays constant for the whole shot; neither of them blinks; the only movement is her thumb picking at her cuticle` | 两人相距约两臂之遥，该距离在全镜头内保持不变；两人都不眨眼；唯一的动作是她用拇指抠自己的甲缘 |
| 6 | `a messy room` | messy 无边界 | `three cardboard boxes stacked against the right wall, papers spread flat across the table, an overturned chair lying on its side near the door` | 右墙边叠着三个纸箱，纸张平摊在桌面上，门边一把椅子侧翻在地 |
| 7 | `a high-tech laboratory` | 概念词会触发随机布景 | `a row of white benchtops, a glass-fronted cabinet along the back wall, a blue-lit panel mounted on the back wall, a steel stool beside the nearest benchtop` | 一排白色实验台，后墙一排玻璃门储物柜，后墙上嵌一块泛蓝光的面板，最近的实验台旁一张钢制圆凳 |
| 8 | `a beautiful sunset` | 美不可渲染 | `the sun sits just above the horizon at the left of frame; the sky grades from amber near the sun to deep blue at the top of frame; a thin band of cloud crosses the sun` | 太阳位于画面左侧、紧贴地平线上方；天空由近日处的琥珀色渐变到画面顶部的深蓝；一道薄云横穿太阳 |
| 9 | `a quiet street` | 安静是听觉不是视觉 | 加可见载体 —— **正向描述"空"，不说"没有人"**：`an empty two-lane street, cars parked along both kerbs, a single street lamp at the right of frame, a sheet of paper tumbling along the gutter` | 空无一人的双向两车道街道，两侧路边停满车辆，画面右侧一盏路灯，一张纸沿水沟翻滚而过 |
| 10 | `a cold winter day` | 冷是体感 | `a layer of untouched snow covers the pavement, thin white vapour rises with each breath, bare tree branches along the kerb, a pale grey sky filling the top third of frame` | 人行道覆着一层无人踩过的雪，每次呼吸升起一缕白色水汽，路边是光秃的树枝，画面上三分之一为浅灰色天空 |
| 11 | `a grand hall` | 宏伟无尺寸 | 尺寸化：`a hall roughly fifteen metres deep, two rows of columns along each wall, a polished stone floor reflecting the ceiling lights` | 大厅纵深约十五米，两侧墙各两排列柱，抛光的石材地面映出顶灯 |
| 12 | `she looks sad` | 情绪不可直接写 | 外化：`her shoulders drop, her gaze stays on the floor, the key light leaves her eyes in shadow, her lower lip presses flat` | 她双肩下沉，视线停留在地面，主光让她的眼部处于阴影中，下唇被压平 |

### 1.3 环境串四件套（每个场景必含，顺序固定）

```
① 空间边界    → 墙 / 窗 / 地面 / 天空，告诉模型"盒子多大"
② 3–5 件物件  → 可数名词，材质 + 颜色 + 画面位置
③ 单一主光    → 一个光源，一个方向，一个色温
④ 次级运动    → 至少 1 个，必须显式命名（见 §5.1）
```

**填空模板（英文，可直接复制改变量）**

```
<空间边界>. <物件1>, <物件2>, <物件3>. A single <soft|hard> key light from
<方向>, <色温>, <次级运动>.
```

**完整例句 ×3**

> 例句 A · 室内夜景
> `A small living room with a blank off-white wall behind the sofa, a low grey fabric sofa, a dark wood coffee table, and a floor lamp at the right of frame. A single soft key light from the upper right of frame at 45°, warm amber. Fine dust drifts slowly through the lamp light; the lampshade does not move.`
> 一间小客厅，沙发背后是留白的米白墙面，一张低矮灰色布艺沙发，一张深色木质茶几，画面右侧一盏落地灯。单一柔和主光自画面右上方 45° 打来，暖琥珀色。细微尘埃在灯光中缓慢飘移；灯罩不动。

> 例句 B · 室外日景
> `A two-lane street with parked cars along both kerbs, a row of bare plane trees on the left pavement, and a low concrete wall on the right. A single hard key light from the upper left of frame, neutral daylight. The tree branches sway in a light breeze; a sheet of newspaper tumbles along the gutter.`
> 双向两车道街道，两侧路边停满车，左侧人行道一排光秃的法国梧桐，右侧一道矮混凝土墙。单一硬主光自画面左上方打来，中性日光。树枝在微风中摇动；一张报纸在水沟边翻滚。

> 例句 C · 室外夜景
> `A wet alley between two brick walls, a green dumpster against the left wall, a fire escape on the right wall, and a single wall-mounted lamp above the far doorway. A single hard key light from the far end of the alley, cool white. Rain falls steadily and evenly; the puddle surface ripples with each drop.`
> 两堵砖墙之间的湿漉小巷，左墙边一只绿色垃圾箱，右墙一道消防梯，远端门洞上方一盏壁灯。单一硬主光自小巷远端打来，冷白色。雨稳定均匀地落下；每滴雨都在水洼表面激起涟漪。

### 1.4 数量纪律

| 项 | 建议值 | 依据 |
|---|---|---|
| 场景串内可见物件数 | **3–5 件** | 【工程取值】 |
| 上限 | **7 件** | 【推断】超过后模型开始丢物件 |
| 一镜内需"稳住"的小物件 | **≤ 2 件** | 主模板 §6.4 E（角色资产）；场景固定物同理【推断】 |
| 场景串长度 | **60–120 英文词** | 【工程取值】，含主光与次级运动 |

> 【待验证】"物件数 > 7 就开始丢"这个阈值没有公开数据支撑。
> **实测方法**：写 5 个版本（3 / 5 / 7 / 9 / 12 件物件），每个版本同一提示词生成 10 次，人工统计"全部物件都在位"的比例。把你自己的拐点填回上表，覆盖本 skill 的默认值。

### 1.5 场景串 与 画风串 的分工（不要混写）

| | 场景串 | 画风串（主模板 §6.3） |
|---|---|---|
| 管 | 空间边界、物件、光源方向、色温、天气 | 镜头、景深、色调、颗粒、皮肤质感 |
| 改的频率 | 换场景才改 | 全剧不改 |
| 例句 | `a low grey fabric sofa, a blank off-white wall, a floor lamp at the right of frame` | `Live-action, cinematic, 35mm lens, shallow depth of field, muted teal-and-amber grade, natural skin texture` |

**为什么要分开**：两者写在同一段里，做 Verbatim 逐字复制时极易手滑改错一处，而**改一处就可能触发漂移**（主模板 §6.3：实测一致性差异可达 40%）。

---

### 1.6 环境侧的否定句配额（每镜 1 句：冗余的删，补充的留）

主模板 §6.4-F：**每镜最多 1 句 `Do not`**，置末尾、前有正向描述。分级：裸名词否定 ❌ 禁用（名词进条件分布，反向激活）｜完整否定句 ⚠️ 弱｜**正向锚定 ✅ 最强**（占据描述位，畸形解无处安放）。

**⚠️ 废止写法**：`No other light source...`（弱档，吃额度）／`...with no detail`（`detail` 判 A 类）。

**存量判定 A/B 类**（`h3-antibug` §1.3，【推断·待验证】）：A 类 = 能指给人看的 → ❌ 一律改正向；B 类 = 只能靠变化察觉的 → ⚠️ 单个可留，不得成串。**但 do not 取舍看冗余性，不看 A/B。**

> 🔑 **判据是冗余性**：**重复正向已说过的 do not = 纯风险零收益，删掉**（尤其重复 A 类名词时）；**补充正向没覆盖到的 = 保留**，优先留给 B 类帧间属性（flicker / drift / shift）。
> ⚠️ **别写成"A 类一律不得进 do not"** —— 会误删补充型句子（Morphed 41 条实测里有效的那句否定，针对的正是 A 类问题）。**冗余的才删，补充的才留。**

**替换成正向锚定，按光型二选一**

| 光型 | 收边句 |
|---|---|
| 夜景 / 局部照明 | `The rest of the frame falls into shadow, reading as one soft unbroken darkness.` |
| 日景 / 整体照明 | `All the light in the room comes from this one source.` |

> 中文：画面其余部分没入暗部，连成一整片柔和的暗。／室内全部光线都来自这一处光源。
> 原理：写满"主光打在哪 + 暗部长什么样"，第二盏灯无处安放。

**无文字走正向锚定，不占额度**（正向串已能堵死）。按本场景可能承载文字的表面列举 2–3 个，不要全剧套同一串：

```text
Every surface in frame that could carry lettering — <列举本场景 2–3 个表面> — is a plain,
unmarked surface showing only colour, material and reflection.
```

> 中文：画面内每一个可能承载文字的表面——<列举>——都是素面无标记的，只呈现颜色、材质与反光。
> 列举参考：客厅 / 书房 `the book spines, the envelope, the framed print`；车内 `the dashboard, the instrument panel, the door trim`；街景 `the signboard, the shopfront window, the road sign`。引自 `h3-screen-text` §7.8；招牌 / 门牌 / 霓虹的处置见其 §7.6。
> **那 1 句留给"补充型"**（正向说不掉的才写）。环境侧补充型 = 帧间变化：`Do not let the light level change at any point.`（曝光漂移无法静态描述）。

---

## 2. 室内场景库（8 类）

**使用方式**：复制"描述串"整段，填进锁定块的"场景与光位串"位置（主模板 §6.3），三镜逐字复制。变量部分用 `< >` 标出，替换时**只改变量，不改骨架**。

每类统一给：描述串（英文原文）· 中文对照 · 主光与色温 · 声景基线 · 翻车点。

---

### 2.1 客厅（夜，落地灯单一光源）

```text
A small living room at night. Behind the sofa, a blank off-white wall. A low grey fabric
sofa occupies the lower half of frame. A dark wood coffee table stands in front of the sofa,
its surface clear except for <one object>. At the right of frame, a floor lamp with a warm-white
fabric shade. A single soft key light from the upper right of frame at 45°, warm amber, falling
from the lamp onto the sofa and the near edge of the table. The rest of the room falls into
shadow, reading as one soft unbroken darkness. Fine dust drifts slowly through the cone of lamp light; the lampshade
does not move. The rest of the frame falls into shadow, reading as one soft unbroken darkness.
```

> 室内客厅，夜景。沙发背后是一面留白的米白墙面。一张低矮的灰色布艺沙发占据画面下半部。沙发前一张深色木质茶几，桌面除 `<一件物件>` 外空无一物。画面右侧一盏暖白色布艺灯罩落地灯。单一柔和主光自画面右上方 45° 打来，暖琥珀色，从灯落到沙发与茶几近端边缘。房间其余部分没入暗部，连成一整片柔和的暗。细微尘埃在灯光的锥形光束中缓慢飘移；灯罩不动。画面其余部分没入暗部，连成一整片柔和的暗。

- **主光**：`upper right of frame at 45°` · **色温**：`warm amber` · **光质**：`soft`
- **声景基线**：`The low hum of a refrigerator from off-frame, floorboards creaking once under shifting weight, fabric shifting as the subject settles into the sofa.`
- **翻车点**：① 不给正向光位锚定，模型常自作主张在背景加一盏顶灯 → 出现双主光（收边句见 §1.6）；② 茶几上写"放了手机和杯子"会触发小物件丢失，只留 1 件。

---

### 2.2 老宅书房（夜，台灯局部照明）

```text
An old study at night. Floor-to-ceiling bookshelves fill the left wall, their spines dark and
unreadable. A dark wooden writing desk sits at the centre of frame, papers spread flat across
its surface. A brass desk lamp with a green glass shade stands at the left of the desk. A single
soft key light from the upper left of frame, warm amber, pooling on the desktop and leaving the
shelves in near-darkness. The window at the back of frame is a flat black rectangle with no
detail behind it. Dust drifts slowly through the cone of lamp light; a single sheet of paper
lifts at one corner and settles again. The rest of the frame falls into shadow, reading as one soft unbroken darkness.
```

> 老宅书房，夜景。左墙整面到顶书架，书脊深暗、不可辨认。一张深色木质书桌位于画面中央，纸张平摊在桌面。书桌左侧一盏黄铜绿玻璃罩台灯。单一柔和主光自画面左上方打来，暖琥珀色，在桌面聚成一滩光，书架几乎全黑。画面后方的窗户是一块纯黑矩形，窗后是一整片均匀的暗。尘埃在灯光的锥形光束中缓慢飘移；一张纸的一角被掀起又落回。画面其余部分没入暗部，连成一整片柔和的暗。

- **主光**：`upper left of frame` · **色温**：`warm amber` · **光质**：`soft`
- **声景基线**：`A low ambient room tone, the soft rustle of paper, the faint tick of a clock from off-frame, floorboards creaking once.`
- **翻车点**：① 书架书脊是**文字类高风险**，必须写 `unreadable`，否则出现乱码书名；② 窗户必须写死 `a flat black rectangle`，否则模型会在窗外造一个随机夜景。
- **注**：这是主模板 §5.5 场景表里的示例场景（`SC_03 老宅书房`），主光 `左前上方`、色温 `暖黄` 与之对应。

---

### 2.3 开放式办公室（日，窗光为主光）

```text
An open-plan office during the day. A row of desks with low grey dividers runs from the left of
frame toward the back. A floor-to-ceiling window fills the right half of frame, its glass showing
only an out-of-focus pale grey sky. A single soft key light from the
right of frame through the window, neutral daylight. The ceiling lights are off. A thin curtain
beside the window breathes in and out; papers on the nearest desk stay flat and still. All the light in the room comes from this one source.
```

> 开放式办公室，日景。一排带浅灰色隔板的办公桌自画面左侧向后延伸。一整面落地窗占据画面右半部，玻璃上只有虚化的浅灰天空，看不到任何建筑。单一柔和主光自画面右侧穿过窗户打来，中性日光。顶灯全部关闭。窗边一层薄窗帘一鼓一收地呼吸；最近一张桌上的纸张平摊不动。室内全部光线都来自这一处光源。

- **主光**：`from the right of frame through the window` · **色温**：`neutral daylight` · **光质**：`soft`
- **声景基线**：`Distant keyboard clatter, a low ventilation hum, the muffled sound of a door closing somewhere off-frame.`
- **翻车点**：① 窗外是最容易失控的地方，必须写死 `out-of-focus pale grey sky`，否则模型会生成整座城市（焦外已承载"不可辨认"，不用再加 `no visible buildings` 这类尾巴）；② 办公室人多的写法见 §6.3。

---

### 2.4 会议室（日/夜，顶灯 + 长桌）

```text
A meeting room. A long dark oval table occupies the centre of frame, its surface clear except
for <one object>. Six identical grey chairs are evenly spaced along both sides, all of them
empty. Behind the table, a blank pale grey wall with a single wall-mounted display; the display
is switched off and shows a flat black panel showing only a uniform dark surface. A single soft key light from
directly above, neutral white. Dust drifts slowly through the light; the chair nearest the camera
does not move. All the light in the room comes from this one source.
```

> 会议室。一张深色椭圆长桌占据画面中央，桌面除 `<一件物件>` 外空无一物。六把相同的灰色椅子沿两侧等距排开，全部空置。桌子后方是一面浅灰素墙，墙上嵌一块显示屏；屏幕关闭，是一块只有均匀暗色表面的面板。单一柔和主光自正上方打来，中性白光。尘埃在光中缓慢飘移；最靠近镜头的椅子不动。室内全部光线都来自这一处光源。

- **主光**：`directly above` · **色温**：`neutral white` · **光质**：`soft`
- **声景基线**：`A low ventilation hum, the scrape of a chair leg on the floor, a single sheet of paper sliding across the table surface.`
- **翻车点**：① 屏幕是**文字类高风险**，必须写 `switched off and shows a flat black panel showing only a uniform dark surface`；② 空椅子是背景人物乱入的高发载体（见 §9.3），写死 `all of them empty`。

---

### 2.5 病房（日，晨光斜射）

```text
A hospital room during the day. A single bed with white linen stands at the left of frame, its
head against the back wall. A metal rail runs along both sides of the bed. A bedside cabinet
with a closed top sits beside the bed. At the right of frame, a window with horizontal blinds;
the blinds are half closed. A single soft key light from the right of frame through the blinds,
warm daylight, casting a set of parallel light bands across the bed and the floor. The dust in
the light bands drifts slowly; the blinds do not move. All the light in the room comes from this one source.
```

> 病房，日景。一张铺白色床品的单人床位于画面左侧，床头靠后墙。床两侧各有一道金属护栏。床边一只顶盖合上的床头柜。画面右侧一扇带横向百叶的窗；百叶半闭。单一柔和主光自画面右侧穿过百叶打来，暖色日光，在床面与地面投下一组平行的光带。光带中的尘埃缓慢飘移；百叶不动。室内全部光线都来自这一处光源。

- **主光**：`from the right of frame through the blinds` · **色温**：`warm daylight` · **光质**：`soft`
- **声景基线**：`The steady beep of a monitor off-frame, a distant trolley rolling past the door, soft footsteps on vinyl flooring.`
- **翻车点**：① 平行光带是**图案类高风险**，横移镜头时极易闪烁 → 此场景建议 `Static Shot` 或 `Push In`；② 医疗设备上的数字与读数属文字类，写 `off-frame` 交给声音层。

---

### 2.6 车内（夜，行驶中）

```text
The interior of a moving car at night. The dashboard occupies the lower third of frame, its
surface dark with a faint amber glow from the instrument panel. The windscreen fills the upper
half of frame; beyond it, street lights pass as soft amber streaks. Two
front seats; the passenger seat is empty. A single soft key light from below, cool amber from
the instrument panel. The cabin shakes with a small, steady vibration; the passing light streaks
move continuously from right to left at a constant rate. Every surface in the cabin that could
carry lettering — the dashboard, the instrument panel, the door trim — is a plain, unmarked
surface showing only colour, material and reflection.
```

> 行驶中的汽车内景，夜。仪表台占据画面下三分之一，表面呈暗色，仪表盘透出微弱琥珀光。挡风玻璃占据画面上半部；玻璃外，路灯化作柔和的琥珀色光条掠过，无任何可读细节。两个前排座位；副驾空置。单一柔和主光自下方打来，来自仪表盘的冷琥珀光。车厢持续轻微震动；掠过的光条以恒定速率自右向左连续移动。车厢内每一个可能承载文字的表面——仪表台、仪表盘、车门内饰板——都是素面无标记的，只呈现颜色、材质与反光。

- **主光**：`from below, cool amber from the instrument panel` · **色温**：`cool amber` · **光质**：`soft`
- **声景基线**：`A low engine hum, tyre noise on wet asphalt, the soft click of the indicator, faint muffled traffic from outside.`
- **翻车点**：① 车外**必须写"无可读细节"**，否则模型会去生成随机的车流与行人；② 光条方向（right to left）要与前后段落的**运动方向锚点**一致（主模板 §3.6），跨段时不得反向。

---

### 2.7 走廊（夜，顶灯序列）

```text
A long corridor at night. Pale green wall tiles cover both walls. A row of ceiling lights runs
from the near end of frame to the far end; the third light from the camera is dark. A pale
linoleum floor reflects the lights in a soft vertical smear. A closed door sits at the far end
of the corridor, centred in frame. A single soft key light from directly above, cool white. Dust
drifts slowly through the light; the reflections on the floor hold steady and do not flicker.
The rest of the frame falls into shadow, reading as one soft unbroken darkness.
```

> 长走廊，夜。两侧墙面贴浅绿色瓷砖。一整排顶灯自画面近端排向远端；自镜头数第三盏灯是熄灭的。浅色塑胶地板把灯光反射成柔和的竖向拖影。走廊远端一扇关着的门，位于画面正中。单一柔和主光自正上方打来，冷白光。尘埃在光中缓慢飘移；地面反射保持稳定、不闪烁。画面其余部分没入暗部，连成一整片柔和的暗。

- **主光**：`directly above` · **色温**：`cool white` · **光质**：`soft`
- **声景基线**：`A low fluorescent hum, the soft echo of footsteps on hard flooring, a distant door closing.`
- **翻车点**：① 顶灯闪烁是硬阻断级高风险 → 用"有一盏是灭的"替代"有盏在闪"，静态比动态稳；② 反射拖影在横移时极易闪，写 `hold steady and do not flicker`；③ 这是长运镜（Truck）的经典场景，跨请求拆分见主模板 §3.4。

---

### 2.8 咖啡馆 / 小店（日，窗边座位）

```text
The interior of a small café during the day. A wooden counter runs along the left wall, its
surface clear. Round wooden tables with bentwood chairs fill the middle of frame; all the
chairs are empty except the one nearest the window. At the right of frame, a large shop window
showing only an out-of-focus pale grey street. A single soft key light
from the right of frame through the window, neutral daylight. Steam rises steadily from a cup
on the nearest table; a thin curtain at the window breathes in and out. All the light in the room comes from this one source.
```

> 小咖啡馆内景，日。一道木质吧台沿左墙延伸，台面空置。圆木桌与曲木椅填满画面中段；除最靠窗的一把外，所有椅子空置。画面右侧一扇大橱窗，窗外只有虚化的浅灰色街道，无可读细节。单一柔和主光自画面右侧穿过橱窗打来，中性日光。最近一张桌上的杯子持续升起热气；窗边薄帘一鼓一收。室内全部光线都来自这一处光源。

- **主光**：`from the right of frame through the window` · **色温**：`neutral daylight` · **光质**：`soft`
- **声景基线**：`The low hiss of a steam wand, cups clinking on saucers, muffled conversation from off-frame, the chime of the door.`
- **翻车点**：① 空椅子 + 模糊对话 = 背景人物乱入双高发，椅子写死 `all empty except one`；② 热气是**必须命名的次级运动**，不写就得到一个完全静止的杯子。

---

## 3. 室外场景库（8 类）

**使用方式同 §2。** 室外场景比室内多两个必写项：**天空**（顶部三分之一写死）与**地面材质**（决定倒影与接触阴影）。

---

### 3.1 城市街道（日）

```text
A two-lane city street during the day. Parked cars line both kerbs. A row of bare plane trees
runs along the left pavement. A low concrete wall runs along the right pavement. Beyond the
buildings, a pale grey sky fills the top third of frame, its tone even from edge to edge. A single soft key
light from the upper left of frame, neutral daylight. The tree branches sway in a light breeze;
a sheet of paper tumbles along the gutter from right to left. The only movement in frame is the one named above.
```

> 城市双向两车道街道，日景。两侧路边停满车辆。左侧人行道一排光秃的法国梧桐。右侧人行道一道矮混凝土墙。建筑之外，浅灰色天空占据画面上三分之一，看不到太阳。单一柔和主光自画面左上方打来，中性日光。树枝在微风中摇动；一张报纸自右向左沿水沟翻滚。画面内唯一的运动就是上面写到的那一处。

- **主光**：`upper left of frame` · **色温**：`neutral daylight` · **光质**：`soft`
- **声景基线**：`Distant traffic, a light breeze through bare branches, the occasional car passing off-frame.`
- **翻车点**：① 天空不写死就会出现随机太阳 → 双主光；② 街上的"空"要**正向写死**（`an empty street, cars parked along both kerbs`），**不要**写 `No moving figures` —— 那是否定句，属 ⚠️ 弱档且占掉唯一 1 句 `Do not` 配额（见 §1.6）。

---

### 3.2 雨夜街道（雨 + 路灯光斑）

```text
A city street on a rainy night. Rain falls steadily and evenly across the whole frame. Wet
asphalt covers the ground and reflects the light. A single street lamp stands at the right of
frame, its light forming a soft amber cone in the rain. Parked cars line the left kerb, their
roofs beaded with water. The sky at the top of frame is a flat dark grey. A single
hard key light from the upper right of frame, warm amber, coming from the street lamp. Rain
streaks fall continuously at a constant density; the puddle surface ripples with each drop; the
lamp cone does not move. The only movement in frame is the one named above.
```

> 雨夜城市街道。雨稳定均匀地落满整个画面。地面为湿沥青并反射灯光。画面右侧一盏路灯，它的光在雨中形成一个柔和的琥珀色光锥。左侧路边停满车辆，车顶布满水珠。画面顶部的天空是一块色调均匀的深灰。单一硬主光自画面右上方打来，暖琥珀色，来自路灯。雨丝以恒定密度连续坠落；每一滴都在水洼表面激起涟漪；灯光锥不动。画面内唯一的运动就是上面写到的那一处。

- **主光**：`upper right of frame, warm amber, from the street lamp` · **色温**：`warm amber` · **光质**：`hard`
- **声景基线**：`Steady rainfall on asphalt and car roofs, water splashing underfoot, distant muffled traffic, a low roll of thunder far away.`
- **翻车点**：① 雨的密度**必须写 `steady and even` / `constant density`**，不写则雨量忽大忽小（见 §5.3）；② 雨夜 + 硬光 + 湿反射三者叠加是**画面闪烁的最高危组合**，量产前先试拍。③ 若画面出现霓虹招牌，属文字类高风险 —— 不出字时写 `a red neon sign` 只给光不给字，要出字走主模板 §7.7 四条硬条件，具体处置见 `h3-screen-text` §7.6

---

### 3.3 雪地 / 雪夜

```text
An open snowfield at night. A layer of untouched snow covers the ground, its surface unbroken. Bare
tree trunks stand at the left and right edges of frame. A low wooden fence runs across the middle
distance. The sky at the top of frame is a flat pale grey, slightly brighter than the snow. A
single soft key light from directly above, cool white, diffused by cloud. Snow falls slowly and
steadily at a constant density; fine powder lifts off the surface in a thin drifting sheet. The only movement in frame is the one named above.
```

> 开阔雪原，夜。地面覆着一层无人踩过的雪，没有脚印。画面左右边缘各立着一棵光秃的树干。中景横着一道矮木栅栏。画面顶部的天空是一块比雪略亮的浅灰。单一柔和主光自正上方打来，冷白光，被云层散射。雪以恒定密度缓慢而稳定地飘落；细雪从地面被掀起，形成一层漂移的薄纱。画面内唯一的运动就是上面写到的那一处。

- **主光**：`directly above, diffused by cloud` · **色温**：`cool white` · **光质**：`soft`
- **声景基线**：`A low wind across open ground, snow crunching underfoot, a distant muffled rumble.`
- **翻车点**：① 雪地是**高亮度大面积**，最容易触发曝光漂移 → 画风串里的 `stable exposure` 不可省；② 脚印一旦出现就跨镜不一致 → 正向写死"未被踩过"：`a layer of untouched snow, its surface unbroken`（`unbroken` 已承载，不要再加 `no footprints`）。

---

### 3.4 天台（夜，城市灯海）

```text
A rooftop at night. A low concrete parapet runs across the foreground, its top edge at the lower
quarter of frame. Behind it, the rooftop surface is flat grey concrete with a single ventilation
unit at the left. Beyond the parapet, a city skyline fills the upper two thirds of frame; the
buildings are small and out of focus, their windows forming a dense field of tiny warm points. A
ventilation pipe crosses the foreground at the right. A single soft key light from below the
frame, warm amber, coming from the city and lighting the parapet from beneath. The distant window
points hold steady and do not flicker; a thin cable sways slowly in the wind. The only movement in frame is the one named above.
```

> 天台，夜。一道矮混凝土女儿墙横贯前景，其顶边位于画面下四分之一处。墙后，天台地面是平整的灰色混凝土，左侧一台通风机组。女儿墙之外，城市天际线填满画面上三分之二；建筑很小且虚化，窗户形成一片密集的暖色小光点。画面右侧一根通风管横过前景。单一柔和主光自画面下方打来，暖琥珀色，来自城市并从下方照亮女儿墙。远处窗格光点保持稳定、不闪烁；一根细缆在风中缓慢摆动。画面内唯一的运动就是上面写到的那一处。

- **主光**：`from below the frame, warm amber, from the city` · **色温**：`warm amber` · **光质**：`soft`
- **声景基线**：`A low steady wind, distant muffled traffic from far below, the hum of a ventilation unit nearby.`
- **翻车点**：① 密集小光点是**闪烁高发**，必须写 `hold steady and do not flicker`；② 天际线是**坠落 / 危险动作高风险场景**，能不靠近边缘就不靠近，改拍"背靠女儿墙"。

---

### 3.5 校园（日，操场 / 教学楼走廊）

```text
A school corridor during the day. Pale green wall tiles cover the lower half of both walls;
above them, a row of windows on the left lets daylight in. A row of closed classroom doors runs
along the right wall, all of them shut. A pale grey linoleum floor runs from the near end of
frame to the far end, its surface reflecting the windows in a soft vertical smear. A single soft
key light from the left of frame through the windows, neutral daylight. Dust drifts slowly
through the light; the floor reflections hold steady and do not flicker. The only movement in frame is the one named above.
```

> 教学楼走廊，日。两侧墙面下半部贴浅绿色瓷砖；其上，左侧一排窗透进日光。右墙一排关着的教室门，全部关闭。浅灰塑胶地板自画面近端延伸到远端，表面把窗户反射成柔和的竖向拖影。单一柔和主光自画面左侧穿过窗户打来，中性日光。尘埃在光中缓慢飘移；地面反射保持稳定、不闪烁。画面内唯一的运动就是上面写到的那一处。

- **主光**：`from the left of frame through the windows` · **色温**：`neutral daylight` · **光质**：`soft`
- **声景基线**：`A distant school bell, muffled voices from behind closed doors, footsteps on hard flooring.`
- **翻车点**：① 门牌号是文字类高风险 → 写 `all of them shut` 不写门牌；② 若需要"走廊里有人"，参考 §6.3 拉开差异，不要用 `a group of students`（对称描述会诱导人物融合）。

---

### 3.6 地下停车场（夜，顶灯 + 柱网）

```text
An underground car park at night. A grid of square concrete pillars runs from the near end of
frame toward the back. Parked cars fill the bays on both sides, all of them stationary and empty.
A row of ceiling tubes runs along the ceiling, spaced evenly. The floor is painted grey concrete,
marked with pale yellow parking lines. A single soft key light from directly above, cool white.
One ceiling tube near the far end is dark. Dust drifts slowly through the light; the parked cars
do not move. The only movement in frame is the one named above.
```

> 地下停车场，夜。一排方形混凝土柱自画面近端排向后方。两侧车位停满车辆，全部静止且无人。天花板上一排顶灯管，间距均匀。地面是刷灰漆的混凝土，画着浅黄色停车线。单一柔和主光自正上方打来，冷白光。远端有一根灯管是灭的。尘埃在光中缓慢飘移；停着的车不动。画面内唯一的运动就是上面写到的那一处。

- **主光**：`directly above` · **色温**：`cool white` · **光质**：`soft`
- **声景基线**：`A low fluorescent hum, the distant echo of an engine starting, footsteps with a hard echo, a metal door closing somewhere off-frame.`
- **翻车点**：① 车辆是**结构高风险物件**（刚体 + 复杂几何），只作背景、不作前景、不给车标；② 柱网是很好的**空间深度锚点**，跨镜复用同一描述串能显著提升一致性。

---

### 3.7 窄巷（夜，单光源纵深）

```text
A narrow alley at night between two brick walls. A green metal dumpster stands against the left
wall. A fire escape runs up the right wall, its platform casting a hard shadow. A single
wall-mounted lamp sits above the doorway at the far end of the alley, centred in frame. Wet
patches on the ground catch the light. The sky above the alley is a narrow dark blue strip. A
single hard key light from the far end of the alley, cool white, coming from the wall lamp and
throwing long shadows toward the camera. The light holds steady and does not flicker; a thin
trail of water runs along the gutter at the left. The only movement in frame is the one named above.
```

> 两堵砖墙之间的窄巷，夜。左墙边一只绿色金属垃圾箱。右墙一道消防梯向上延伸，其平台投下硬阴影。小巷远端门洞上方一盏壁灯，位于画面正中。地上的水洼映着灯光。小巷上方的天空是一条狭窄的深蓝。单一硬主光自小巷远端打来，冷白光，来自壁灯并把长影投向镜头。灯光保持稳定、不闪烁；一道细水流沿左侧水沟流淌。画面内唯一的运动就是上面写到的那一处。

- **主光**：`from the far end of the alley, cool white` · **色温**：`cool white` · **光质**：`hard`
- **声景基线**：`Water dripping somewhere out of sight, a distant siren, the hollow echo of footsteps between the two walls.`
- **翻车点**：① 这是**纵深推镜（Push In）的理想场景**——单一光源在远端，天然引导视线；② 反光与阴影是**身份漂移高发**（脸一半在影里），若主角要在此说话，改 `soft` 光质。

---

### 3.8 江边 / 码头（黄昏，逆光）

```text
A riverside quay at dusk. A concrete quay edge runs across the lower third of frame. Beyond it,
a wide stretch of water fills the middle of frame, its surface broken by small slow ripples. On
the far bank, a low line of dark buildings sits against the sky. The sun is a soft bright disc
just above the horizon at the left of frame. The sky grades from amber near the sun to deep blue
at the top of frame. A single soft key light from the left of frame, low and horizontal, warm
amber, backlighting everything in frame. The water surface ripples continuously; a length of rope
hanging from a bollard sways slowly. The only movement in frame is the one named above.
```

> 江边码头，黄昏。一道混凝土码头边缘横贯画面下三分之一。其外，一片开阔水面填满画面中段，水面被细小的慢波打破。对岸，一排低矮的深色建筑贴着天空。太阳是画面左侧紧贴地平线上方的一个柔和亮盘。天空由近日处的琥珀色渐变到画面顶部的深蓝。单一柔和主光自画面左侧打来，低位且近水平，暖琥珀色，为画面内一切逆光。水面持续起波纹；系船柱上一截垂下的缆绳缓慢摆动。画面内唯一的运动就是上面写到的那一处。

- **主光**：`from the left of frame, low and horizontal, backlighting` · **色温**：`warm amber` · **光质**：`soft`
- **声景基线**：`Water lapping against the concrete, a distant boat horn, gulls calling, a light wind across open water.`
- **翻车点**：① **逆光会让脸进入剪影**，若该镜需要看清表情，加 `a faint cool fill from camera right` 作为唯一补光（仍守住"单一主光 + 一个补光"）；② 水面波纹是**高闪烁风险**，量产前先试拍 3 条。

---

## 4. 光影系统

### 4.1 H3 没有光照字段 —— 光照写在哪

【官方】H3 的三核心字段里**没有**独立的光照字段。光照描述写在 `integrated_multimodal_description` 内，与主体、动作同一句群；且按主模板 §6.5 的优先级，它落在**第 4 层**（环境 + 光位）。

**写法**：不要单独起一段 `[LIGHTING] ...`，直接嵌进场景串的第三件套（见 §1.3）。

### 4.2 单一主光原则（硬）

主模板 §6.3 场景与光位串原文：**"画面右侧有一盏落地灯作为唯一可见光源，单一柔和主光自画面右前方 45° 打来"**。

防翻车词库 §13 的 `[LIGHT LOCK]`：`A single soft key light from camera left at 45°, cool ambient fill with all light sources kept off-screen.`

**两条约束**：

| 约束 | 写法 |
|---|---|
| 主光**只有一个**，一个方向 | `A single soft key light from the upper right of frame at 45°, warm amber.` |
| 画面内**不出现**灯具本体（除非它是叙事物件） | `The rest of the frame falls into shadow, reading as one soft unbroken darkness.` |

**为什么**：多主光 = 多组方向矛盾的阴影，模型会在几组解之间摇摆，结果是**脸和场景一起漂移**。主模板 §5.5 明确："主光源方向与色温必须记录——这是匹配剪辑「色彩锚点」的取值来源。上下段要衔接，光源方向就不能乱变。"

> 【推断】这条原则的机制解释（多主光 → 多维解空间 → 采样摇摆）没有公开实测支撑。但它同时被主模板、防翻车词库、官方 Ref2VA 示例三方各自独立采用，**按执行即可**。
> 【待验证】"单一主光比双主光的一致性提升多少"无数字。
> **实测方法**：同一场景串写两版（1 主光 vs 1 主光 + 1 补光），各生成 10 次，三镜一组，盲评"三镜光照方向是否一致"，统计通过率。

### 4.3 方向词表（**用画面方位，不用角色左右**）

主模板 §6.4 C 明确：**"用画面方位表述，不用角色的左右"**——"她的左边"有歧义（是她的左手边还是画面左边？），是左右翻转翻车的常见根因。

| 中文 | 英文原文（可直接复制） | 适用 |
|---|---|---|
| 镜头左侧 | `from camera left` | 最通用，与摄影术语一致 |
| 镜头右侧 | `from camera right` | 同上 |
| 画面左侧 | `from the left of frame` | 强调画面坐标 |
| 画面右侧 | `from the right of frame` | 同上 |
| 画面左上方 45° | `from the upper left of frame at 45°` | 最常用主光位 |
| 画面右上方 45° | `from the upper right of frame at 45°` | 同上 |
| 正上方 | `from directly above` | 顶灯、阴天 |
| 下方（底光） | `from below` | ⚠️ 会改变脸的观感，慎用 |
| 从背后（逆光） | `from directly behind the subject, backlighting` | 剪影、黄昏 |
| 从窗户来 | `from the right of frame through the window` | 室内日景 |
| 从画面远端来 | `from the far end of the corridor` | 走廊、窄巷 |

### 4.3.1 光位常量串（跨段色彩锚点的可复制模板）

场景卡「光照」组落地成一串，**上下段、跨段、跨集逐字复制**。三段式：**主光方向 + 色温 + 暗部落向**（暗部落向是对光位的二次编码，比只写方向更稳）。

```text
【光位常量块 · 全剧逐字复用】
A single soft key light from the upper front left at 45°, warm amber, holding steady on her
cheek, the shadow side falling to the lower right. The rest of the frame falls into shadow, reading as one soft unbroken darkness.
```

> 中文对照：单一柔和主光自左前上方 45° 打来，暖琥珀色，稳定地落在她脸颊上，暗部落在右下方。画面其余部分没入暗部，连成一整片柔和的暗。

| 段 | 取值 | 备注 |
|---|---|---|
| 主光方向 | `from the upper front left at 45°` | 见 §4.3，用画面方位不用角色左右 |
| 色温 | `warm amber` | 见 §4.4；**K 值只作团队沟通语言，不进提示词** |
| 光质 | `soft` / `hard` / `diffused by cloud` | |
| 暗部落向 | `the shadow side falling to the lower right` | 【推断】二次编码，强化明暗结构 |
| 收边 | `The rest of the frame falls into shadow, reading as one soft unbroken darkness.` | 守住单一主光 |

> ⚠️ **与 `h3-camera-edit` §8.2 的口径统一**：**色彩锚点取的就是这一串**。若在别处看到 `colour temperature 3200K` 的写法，替换为 `warm amber` —— K 值虽是【业界】摄影标准，但模型对数字 token 的响应度未获官方确认（§4.4）。

### 4.4 色温与光质

| 中文 | 英文原文 | 常见场景 |
|---|---|---|
| 暖琥珀（灯光 / 黄昏） | `warm amber` | 室内夜景、黄昏、烛光 |
| 暖白（柔光灯） | `warm white` | 室内柔光、台灯 |
| 暖色日光 | `warm daylight` | 清晨 / 傍晚 |
| 中性日光 | `neutral daylight` | 白天室外、窗光 |
| 中性白（顶灯） | `neutral white` | 办公室、会议室 |
| 冷白（荧光 / 月光） | `cool white` | 走廊、车库、医院 |
| 冷蓝（夜 / 阴） | `cool blue` | 夜晚室外、雪夜、阴天 |
| 深红（霓虹 / 警示） | `deep red` | 霓虹、暗房 |

**光质**：

| 中文 | 英文原文 | 视觉特征 |
|---|---|---|
| 柔和 | `soft` | 阴影边缘模糊，过渡长 |
| 硬 | `hard` | 阴影边缘锐利，对比强 |
| 被云层散射 | `diffused by cloud` | 无明确方向阴影 |

> ⚠️ **关于 K 值（3200K / 5600K）**：这些是【业界】摄影标准数值，本身正确；但**模型对数字 token 的响应度没有官方确认**【待验证】。
> **建议**：提示词里以文字描述为主（`warm amber`），K 值只作为团队内部的沟通语言与场景卡备注，**不要**作为唯一判据写进提示词。
> **实测方法**：同一场景生成 10 次，5 次写 `3200K`、5 次写 `warm amber`，三方盲评两组内部的一致性得分。若差异不显著，就永久改用文字描述。

### 4.5 光比（主光 : 补光）

【业界】影视摄影的常规光比档位：

| 档 | 比值 | 视觉 | 英文写法 |
|---|---|---|---|
| 平光 | 2:1 | 阴影浅，细节全留 | `a faint fill from camera right, the shadow side retains full detail` |
| 常规 | 4:1 | 有明暗面，阴影有细节 | `a soft fill from camera right, the shadow side holds visible detail` |
| 硬光 | 8:1 | 阴影几乎全黑 | `the shadow side falls into near-darkness, the key light the only source touching her` |

> 【待验证】光比的**数字比值**（2:1 / 4:1 / 8:1）模型是否响应，无公开数据。
> **建议**：**写视觉结果，不写比值数字**。上表右列的写法即为可直接复制的形式。

### 4.6 光照与身份一致性的关系（重要）

**机制【推断】**：人脸的明暗分布是身份的**强视觉特征**。主光换边 = 明暗分布反转 = 模型眼中的"另一张脸"。

防翻车词库 §7 原文：**"光照方向全程单一主光，主光换边身份就会晃。"**

**执行规则**：

| 场景 | 规则 |
|---|---|
| 同一次请求的三镜 | 主光方向、色温、光质**逐字相同** |
| 同一段落内的三镜 | 同上；第六段（光影风格）写 `Lighting matches the lock block exactly.` |
| 跨段（不同请求） | 主光方向**不得改变**；改段不改光 |
| 必须改光（如日夜转换） | 这是**转场事件**，要用一个空镜承载（见 §9.1），不要在人物镜里悄悄改 |

### 4.7 日夜景差异

| 维度 | 日景 | 夜景 |
|---|---|---|
| 光源性质 | 单一大光源（太阳 / 天空 / 窗） | 多个小光源，但**只能指定一个主光** |
| 对比 | 低–中对比，暗部有细节 | 高对比，暗部吞细节 |
| 必写项 | 天空 + 地面 | **唯一可见光源** + 正向锚定收边（见 §1.6） |
| 背景 | 可虚化但要有内容 | 直接写"没入暗部"最稳 |
| 色温 | `neutral daylight` / `warm daylight` | `warm amber` / `cool white` / `cool blue` |

**夜景三条**：

1. **明确写"唯一可见光源"** —— `a floor lamp at the right of frame` 是唯一一盏，就写 `The rest of the frame falls into shadow, reading as one soft unbroken darkness.`
2. **背景压暗，不要写"背景可见很多细节"** —— 夜景背景细节越多，漂移与杂乱的概率越高。写 `The rest of the room falls into shadow, reading as one soft unbroken darkness.`
3. **光源数量写死** —— `a single street lamp`、`a row of ceiling lights`（并说明有几盏是灭的）。

### 4.8 完整例句 ×3（日 / 夜 / 逆光）

> **日景**
> `A single soft key light from the upper left of frame, neutral daylight, filtering through the canopy and casting a set of soft dappled patches on the path.`
> 单一柔和主光自画面左上方打来，中性日光，穿过树冠并在小径上投下一组柔和的斑驳光斑。

> **夜景**
> `A single soft key light from the upper right of frame at 45°, warm amber, falling from the lamp onto the sofa and the near edge of the table. The rest of the room falls into shadow, reading as one soft unbroken darkness. The rest of the frame falls into shadow, reading as one soft unbroken darkness.`
> 中文对照见 §4.3.1 光位常量串（同一串，不重复译）。

> **逆光**
> `A single soft key light from the left of frame, low and horizontal, warm amber, backlighting everything in frame, with a faint cool fill from camera right so the subject's face holds visible detail.`
> 单一柔和主光自画面左侧打来，低位且近水平，暖琥珀色，为画面内一切逆光；画面右侧一抹极弱的冷色补光，使人物的脸保住可见细节。

---

## 5. 天气与大气

### 5.1 铁律：次级运动必须命名

防翻车词库 §9 原文：**"命名次级运动才能得到次级运动"**——不命名，模型只给你一个静态道具。

**次级运动** = 环境中不由主体驱动的、持续发生的小运动：衣摆、发丝、热气、尘埃、雨丝、雪片、水面波纹、树叶、光斑。

**每个场景串至少要命名 1 个次级运动**（§1.3 四件套第 ④ 项）。

```
❌ 只有静态道具：A café with a cup on the table.
✅ 命名了次级运动：Steam rises steadily from a cup on the nearest table;
   a thin curtain at the window breathes in and out.
```

### 5.2 六种天气 / 大气的写法

#### (1) 雨 Rain

```text
Rain falls steadily and evenly across the whole frame. Rain streaks fall continuously at a
constant density; the puddle surface ripples with each drop; water runs along the gutter at the
left. The wet asphalt reflects the street lamp in a soft vertical smear that holds steady.
```

> 雨稳定均匀地落满整个画面。雨丝以恒定密度连续坠落；每一滴都在水洼表面激起涟漪；水沿左侧水沟流淌。湿沥青把路灯光反射成柔和的竖向拖影，保持稳定。

- **声景**：`Steady rainfall on asphalt and car roofs, water splashing underfoot, distant muffled traffic.`
- **必须命名的三个次级运动**：雨丝本身、水洼涟漪、地面径流。三个都写，雨才"活"。
- **翻车点**：不写 `steady and even` / `constant density` → 雨量忽大忽小（见 §5.3）。

#### (2) 雪 Snow

```text
Snow falls slowly and steadily at a constant density; fine powder lifts off the surface in a
thin drifting sheet. The falling flakes keep the same size and the same density from the first
frame to the last.
```

> 雪以恒定密度缓慢而稳定地飘落；细雪从地面被掀起，形成一层漂移的薄纱。从第一帧到最后一帧，飘落的雪花保持同样的大小与同样的密度。

- **声景**：`A low wind across open ground, snow crunching underfoot, a distant muffled rumble.`
- **翻车点**：雪花密度是最容易漂的量，必须写 `constant density` + `same size`。

#### (3) 雾 / 霾 Fog / Haze

```text
A thin layer of fog sits at knee height across the middle distance, its top edge soft and level.
The fog holds a constant density and drifts slowly from left to right. The far end of the street
fades into an even grey beyond which nothing is rendered.
```

> 一层薄雾齐膝高，铺在中景处，其顶边柔和而齐平。雾保持恒定密度，缓慢自左向右漂移。街道远端淡入灰色，其外看不到任何细节。

- **声景**：`A muffled, dampened room tone; distant sounds arrive softened and indistinct; water dripping nearby.`
- **翻车点**：雾是**最好的深度分层工具**（远景被吃掉 = 背景不乱），但它同时也是**曝光漂移源** → 画风串的 `stable exposure` 不可省。

#### (4) 风 Wind

```text
A steady breeze moves through frame from right to left. The tree branches sway continuously in
one direction; the hem of her coat lifts and settles; a sheet of paper tumbles along the gutter
from right to left.
```

> 稳定的微风自右向左穿过画面。树枝持续朝一个方向摇动；她的外套下摆被掀起又落回；一张报纸自右向左沿水沟翻滚。

- **声景**：`Wind moving through branches, the dry rustle of paper, fabric flapping softly.`
- **翻车点**：① **风的方向必须写死并与运动方向锚点一致**（主模板 §3.6：上段出口方向 = 下段入口方向，严禁反向）；② 布料大幅飘动是高风险（防翻车词库 §9），写 `lifts and settles` 这类**有界**动作，不要写 `whips violently`。

#### (5) 逆光 Backlight

```text
The sun sits just above the horizon at the left of frame. A single soft key light from the left
of frame, low and horizontal, warm amber, backlighting everything in frame. A faint cool fill
from camera right keeps the subject's face in visible detail. A thin bright rim runs along the
subject's right shoulder and the edge of her hair.
```

> 太阳位于画面左侧、紧贴地平线上方。单一柔和主光自画面左侧打来，低位且近水平，暖琥珀色，为画面内一切逆光。画面右侧一抹极弱的冷色补光，使人物的脸保住可见细节。一道细而亮的轮廓光沿着人物的右肩与发丝边缘。

- **声景**：`A low warm wind, distant birds, the faint hiss of long grass.`
- **翻车点**：纯逆光 = 脸全黑；必须加**一个补光**（仍守住单一主光原则：一主一补，不要再加第三个）。

#### (6) 丁达尔 / 光柱 Tyndall / God rays

```text
A shaft of warm light enters from the upper left of frame and falls diagonally across the room,
its edges clearly defined. Fine dust drifts slowly and continuously inside the shaft; the shaft
itself does not move. Outside the shaft, the room falls into soft shadow.
```

> 一束暖光自画面左上方射入，斜斜落过房间，其边缘清晰可辨。细微尘埃在光束内缓慢而连续地飘移；光束本身不动。光束之外，房间没入柔和的阴影。

- **声景**：`A low, still room tone; a single floorboard creaking; faint dust settling.`
- **翻车点**：① 光柱边缘是**形态高风险**，横移时会抖 → 优先用 `Static Shot` 或 `Push In`；② 尘埃是必须命名的次级运动，不写则光柱里空无一物，显得"贴上去的"。

### 5.3 天气一致性（跨镜三件套）

大气类的量（雨量、雪量、雾浓度、风强）**天生会漂**。防翻车词库与叙事侧方法论 §2.3 #10 给出的写法是**密度声明**：

| 项 | 必写的英文原文 |
|---|---|
| 密度恒定 | `at a constant density` / `holds a constant density` |
| 尺寸恒定 | `the falling flakes keep the same size` |
| 不闪烁 | `holds steady and does not flicker` |
| 首尾一致 | `from the first frame to the last` |

**完整串（可直接附加到任何天气场景串末尾）**：

```text
The <rain|snow|fog> holds a constant density and the same particle size from the first frame to
the last; it does not start or stop mid-shot and it does not flicker.
```

> `<雨|雪|雾>` 从第一帧到最后一帧保持恒定密度与相同的颗粒大小；它不在镜头中途开始或停止，也不闪烁。

---

## 6. 空间关系与距离

### 6.1 用画面方位，不用角色左右

主模板 §6.4 C 原文：**"用画面方位表述，不用角色的左右"**；⚠️ 注释：**"'她的左边'有歧义（是她的左手边还是画面左边？），是左右翻转翻车的常见根因。"**

| 中文 | 英文原文 | 说明 |
|---|---|---|
| 画面左三分之一 | `at the left third of frame` | 主体位置最常用 |
| 画面右三分之一 | `at the right third of frame` | 同上 |
| 画面正中 | `centred in frame` / `at the centre of frame` | |
| 画面左四分之一 | `in the left quarter of frame` | 前景遮挡常用 |
| 画面右四分之一 | `in the right quarter of frame` | 同上 |
| 前景 | `in the foreground` | 需配合占比 |
| 中景 | `in the middle distance` / `in the mid-ground` | |
| 背景 | `in the background` | 通常加 `out of focus` |
| 画面上三分之一 | `at the top third of frame` | 天空 |
| 画面下三分之一 | `at the lower third of frame` | 地面、桌面 |
| 画面左边缘 | `at the left edge of frame` | 半个身位入画 |

```
❌  on her left                      （她的左边 —— 歧义）
✅  at the left third of frame       （画面左三分之一 —— 唯一解）

❌  the man standing next to him     （"旁边"无距离）
✅  the man stands at the right third of frame, one arm's length from her
```

### 6.2 可度量距离声明

主模板 §6.4 C 原文示例：`two people stand two arm's lengths apart, and this distance stays constant for the whole shot`

**三段式**：`<数值/身体尺度> + <方位> + <恒定性声明>`

| 中文 | 英文原文 | 适用 |
|---|---|---|
| 约一臂之遥 | `one arm's length apart` | 近距离对峙 |
| 约两臂之遥 | `two arm's lengths apart` | 常规对话距离 |
| 约一米 | `about one metre apart` | 需要精确时 |
| 约两步远 | `about two paces apart` | 中距离 |
| 并肩，肩距约一拳 | `side by side, about a hand's width between their shoulders` | 同行 |
| 相距半个房间 | `across half the width of the room from each other` | 大空间 |

**恒定性声明（必写）**：

```text
... and this distance stays constant for the whole shot.
... and neither of them moves closer or further away.
... and the gap between them does not change from the first frame to the last.
```

> ……且该距离在全镜头内保持不变。
> ……且两人都不靠近或远离。
> ……且两人之间的间距从第一帧到最后一帧不发生变化。

> 【推断】"距离声明能降低模型把两人拉到一起的概率"这个机制无公开实测数字。
> 【待验证】实测方法：同一双人场景生成 10 次，5 次带距离声明、5 次不带，量末帧两人间距的方差。把你自己的结果填回。

### 6.3 多人站位（拉开差异是第一原则）

主模板 §6.4 A 原文：**"反例必崩：`two men in suits` —— 对称描述会诱导人物融合。必须拉开差异。"**

**公式**：

```
<人物A：外观差异 + 画面位置>（一个动作）and <人物B：外观差异 + 画面位置>（一个动作）;
<距离声明 + 恒定性声明>.
```

**正例**：

```text
A tall man in a red apron at the left third of frame and a short woman in a denim jacket at the
right third of frame; they stand two arm's lengths apart and this distance stays constant for the
whole shot. The man folds his arms, then the woman takes one step forward.
```

> 一名穿红围裙的高个男人位于画面左三分之一，一名穿牛仔外套的矮个女人位于画面右三分之一；两人相距约两臂之遥，该距离在全镜头内保持不变。男人抱起双臂，然后女人向前迈一步。

**反例与修正**：

| ❌ | 为什么崩 | ✅ |
|---|---|---|
| `two men in suits` | 对称描述 → 融合 | `a tall man in a dark suit at the left third of frame and a shorter man in a grey suit at the right third of frame` |
| `a group of students` | 数量与外观都不可控 | `three students at the far end of the corridor, out of focus` |
| `people in the background` | 会生成清晰人脸并乱入 | `blurred passersby in the background, out of focus` |
| `two people talking` | 违反"一镜一个说话人"（防翻车词库 §1.4） | 切成两镜，或用一镜一人的正反打（叙事侧 §2.3 #11） |

**多人配置纪律**：

| 项 | 值 | 依据 |
|---|---|---|
| 一镜内**有名有姓**的人物 | **≤ 2 人** | 【推断】 |
| 一镜内说话的人 | **1 人** | 防翻车词库 §1.4 官方原文 |
| 背景人群 | 写到 `out of focus` 为止 —— 焦外已承载"不可辨认"，**不再加否定尾巴**；不给数量以外的细节 | 主模板 §6.4 A |
| 每人动作数 | **1 个**（多人时） | 主模板 §6.4 A |

### 6.4 前中后景三层

【推断】把画面切成三层，是让场景串"有层次且不打架"的最简单方法。三层各有职责，**不是平均分配注意力**。

| 层 | 画面占比 | 职责 | 英文写法 | 中文 |
|---|---|---|---|---|
| **前景** | **≤ 1/4** | 遮挡、剪影、制造纵深 | `a dark out-of-focus silhouette occupies the left quarter of frame, its edge clean and its surface one even dark tone from the subject` | 一团虚化的暗色剪影占据画面左四分之一，色调均匀，与主体之间有干净的边缘分离 |
| **中景** | 主体所在 | 承载叙事 | `the subject stands at the right third of frame, body angled three-quarters to camera` | 主体位于画面右三分之一，身体与镜头成四分之三角 |
| **后景** | 剩余 | 提供环境，虚化 | `the background is a soft out-of-focus blur` | 背景是一片柔和的虚化 |

**执行规则**：

1. **前景占比必须 ≤ 1/4** —— 叙事侧 §2.3 #8 原文：**"前景占比压到 ≤1/4（1/3 时粘连概率明显上升）"**
2. **前景做成色调均匀的暗剪影** —— 有纹理的前景在横移时必闪（叙事侧 §2.3 #5）
3. **后景越虚越安全** —— `out of focus` 是背景人物乱入与文字乱码的双重解药

### 6.5 完整例句 ×2

> **双人室内**
> `A tall man in a dark suit at the left third of frame and a shorter woman in a grey coat at the right third of frame; they stand two arm's lengths apart and this distance stays constant for the whole shot. A dark out-of-focus silhouette occupies the lower left quarter of frame. Behind them, a blank off-white wall falls into a soft blur. A single soft key light from the upper right of frame at 45°, warm amber.`
> 一名穿深色西装的高个男人位于画面左三分之一，一名穿灰色外套的较矮女人位于画面右三分之一；两人相距约两臂之遥，该距离在全镜头内保持不变。一团虚化的暗色剪影占据画面左下四分之一。他们身后，一面留白的米白墙面淡入柔和的虚化。单一柔和主光自画面右上方 45° 打来，暖琥珀色。

> **单人室外（含前景 + 三层）**
> `The subject stands at the right third of frame, body angled three-quarters to camera, both arms hanging at her sides. In the foreground, the out-of-focus edge of a concrete parapet crosses the lower quarter of frame. In the background, a city skyline fills the upper two thirds of frame, small and out of focus, its windows a dense field of tiny warm points. A single soft key light from below the frame, warm amber.`
> 主体位于画面右三分之一，身体与镜头成四分之三角，双臂垂在身侧。前景中，混凝土女儿墙的虚化边缘横过画面下四分之一。背景中，城市天际线填满画面上三分之二，很小且虚化，窗户是一片密集的暖色小光点。单一柔和主光自画面下方打来，暖琥珀色。

---

## 7. 场景一致性

### 7.1 场景卡（外置环境，全剧复用）

主模板 §5.5 给了最小字段集：**场景ID / 名称 / 环境描述串（固定）/ 主光源方向 / 色温 / 参考图ID / 出现集段**。本 skill 在其基础上补充环境层专属字段，**不改动原有字段**。

```markdown
## SC__ 《场景名》

### 基础（沿用主模板 §5.5）
- 场景ID：SC__　　名称：
- 出现集段：E__、E__、E__

### 环境描述串（固定，40–80 词，全剧逐字复用，禁止同义改写）
> <英文描述串，见 §2 / §3 场景库，只改 <变量>>

### 光照（本 skill 新增）
- 主光源方向：　　　　（如：upper right of frame at 45°）
- 色温：　　　　　　　（如：warm amber）
- 光质：　　　　　　　（soft / hard / diffused by cloud）
- 补光：　　　　　　　（无 / 一个，方向 + 强度）
- 画面内灯具本体：　　（无 / 有，作为叙事物件）

### 空间（本 skill 新增）
- 空间边界：　　　　　（墙 / 窗 / 地面 / 天空，各一句）
- 可见物件清单：　　　（3–5 件，逐件登记）
- 前 / 中 / 后景：　　（各一句）
- 人物站位模板：　　　（主体位置 + 距离声明）

### 大气与次级运动（本 skill 新增）
- 天气：　　　　　　　（晴 / 雨 / 雪 / 雾 / 风 / 逆光 / 丁达尔）
- 密度声明：　　　　　（constant density / same size / held steady）
- 次级运动：　　　　　（≥1 个，必须命名）

### 声景基线（本 skill 新增）
- overall_soundscape 模板句（1–4 句，全剧复用）：
> <英文 1–4 句>

### 资产
- 场景空镜参考图 ID：IMG__（= Ref2VA 的 <Picture 4> 槽位，见 §7.5）
- 保留强度：fully_preserved（承载场景识别）/ attribute_transfer（纯风格）
```

### 7.2 与「色彩锚点」的关系

主模板 §3.6 三锚点【推断】：

| 锚点 | 内容 | **本 skill 的取值来源** |
|---|---|---|
| **色彩锚点** | 上下段复用同一光位 / 色温描述串 | **场景卡的「光照」组**——主光方向 + 色温 + 光质，逐字复制 |
| 运动方向锚点 | 上段出口方向 = 下段入口方向，严禁反向 | 场景卡的「次级运动」组（风、雨、水流、光条方向） |
| 构图锚点 | 末帧主体位置 ≈ 首帧主体位置 | 场景卡的「空间」组——人物站位模板 |

> ⚠️ **三者共用同一张场景卡。** 这就是为什么场景卡要"外置"：三锚点的值不能靠分镜师临场回忆，必须查表。

**跨段复用的最小操作**：

```
上一段 C 出镜的末帧光照  →  下一段 A 入镜的开场光照
   直接复制场景卡「光照」组的四行，一个词都不改
```

### 7.3 三级一致性（段内 / 跨段 / 跨集）

| 级别 | 谁来保证 | 场景层要做什么 |
|---|---|---|
| **段内（同一次请求的三镜）** | **模型架构自带**（共享上下文，同一次推理） | 三镜复制同一份场景串；第六段写 `Lighting matches the lock block exactly.` |
| **跨段（不同请求）** | 人工锚点工程（三锚点）+ FL2VA 首尾帧 | 场景卡查表；光源方向**不得改变**；次级运动方向**与运动方向锚点对齐** |
| **跨集** | 场景卡 + 参考图锁 | 场景串全剧不改；场景空镜参考图全程不换图 |

> 主模板 §3.2 明确指出：**单次请求出三镜时，若第 2 镜崩了，重生成会把第 1、3 镜一起重新采样**。所以段内一致性虽然由模型保证，**返修时仍需要场景卡兜底**（走 T2 单镜重生成，场景串从卡里复制）。

### 7.4 场景串的逐字复用纪律（Verbatim Rule）

主模板 §6.3 铁律：**"一个字都不改。改一个词就可能触发身份漂移（Verbatim Rule，实测一致性差异可达 40%）。"**

| 情形 | 正确做法 | 错误做法 |
|---|---|---|
| 觉得场景串写得不好 | **全剧统一改**，改完所有出现集段一起替换 | 只改当前这一处 |
| 换了个更贴切的同义词 | ❌ 不改。同义替换 = 触发漂移 | `sofa` → `couch` |
| 需要加一件物件 | 全员同步加，并重跑该场景的复现测试 | 只在这一镜加 |
| 段落之间要"有点变化" | **变化交给运镜与景别，不交给场景串** | 改一个形容词来"区分" |

### 7.5 参考图槽位：场景空镜锁在哪

防翻车词库 §2 的 9 图分配表**槽位 4 = 场景空镜（含光源方向）**，标为 ✅ 必填。

| 槽位 | 用途 | 与场景卡的关系 |
|---|---|---|
| 1–3 | 角色正面 / 侧面 / 全身 | — |
| **4** | **场景空镜（含光源方向）** | **= 场景卡的「场景空镜参考图 ID」** |
| 5 | 画风 / 调色参考 | 对应画风串，不是场景串 |
| 6–9 | 道具 / 手部 / 第二角色 / 备用 | — |

> ⚠️ **图生视频与全能参考互斥**（【官方】）。走 Ref2VA 就有槽位 4，走 FL2VA 就没有——**FL2VA 时场景只能靠描述串锁**。这是选模式时的真实代价，见防翻车词库 §15。

**Ref2VA 模式下的场景锁定写法**（可直接复制）：

```text
<Picture 4> is the location reference for [Shot 1] and [Shot 2], defining the room layout, the
position of the furniture and the direction of the key light.
```

> `<Picture 4>` 是 `[Shot 1]` 与 `[Shot 2]` 的场景参考，定义房间布局、家具位置与主光方向。

```text
retention_analysis:
<Picture 4> (appears in [Shot 1], [Shot 2]): fully_preserved - the room layout, the position of
the sofa and the floor lamp, and the direction of the key light are unchanged.
```

> 保留分析：`<Picture 4>`（出现在 `[Shot 1]`、`[Shot 2]`）：完全保留 —— 房间布局、沙发与落地灯的位置、以及主光方向均不变化。

> **铁律（防翻车词库 §2.1）**：**承载识别的资产一律 `fully_preserved`；纯风格/氛围一律 `attribute_transfer`。** 场景空镜承载的是"这是哪个地方"，所以用 `fully_preserved`。

---

## 8. 环境音与物理音（`overall_soundscape`）

### 8.1 官方口径

【官方】`overall_soundscape`：**"Summarizes ambient sound, physical action sounds, and non-verbal human sounds across the entire video."** **1–4 句英文，写成一段连续段落。**

【官方】禁止内容：**"Dialogue, singing, and diegetic music already belong in the multimodal description and should not be repeated here."**

【官方】N/A 条件：**"Use N/A only when the user explicitly requests complete silence throughout the video."**

### 8.2 该写什么 / 不该写什么

| ✅ 该写（`overall_soundscape`） | ❌ 不该写 |
|---|---|
| 环境底噪（room tone、风、雨、车流、荧光灯嗡鸣） | 对白（已在 `<d>` 里） |
| 物理动作音（脚步、门响、纸张、杯碟、水花） | 演唱 / 歌词（已在主字段） |
| 非语言人声（呼吸、抽气、咳嗽、笑声、脚步声） | 剧情内音乐（画内收音机 / 手机 / 电视的音乐，属 diegetic → 主字段） |
| 天气声（雨、雪、雷、水） | 配乐（→ `non_diegetic_music`） |
| 场景机制声（霓虹管嗡鸣、通风管、电梯） | 情绪词（"悲伤的音乐"→ 违归；见 §8.4） |

### 8.3 判别问句

防翻车词库 §1.5 原文：**"问一句'画面里的人能不能听见这个声音'"**

```
画面里的人能听见  → integrated_multimodal_description 或 overall_soundscape
只有观众能听见    → non_diegetic_music
```

**边界情形**：

| 声音 | 归属 | 理由 |
|---|---|---|
| 角色自己说台词 | `<d>` 内（主字段） | 官方：只写在 `<d>` 里 |
| 角色哼歌 | 主字段（`singing`） | 官方明确列为例外 |
| 画内收音机放的歌 | 主字段（diegetic music） | 官方："Singing, instruments, radio, television, or phone music audible to the characters are diegetic events" |
| 脚步声、门响、布料摩擦 | `overall_soundscape` | 物理动作音 |
| 环境底噪（雨、风、荧光灯） | `overall_soundscape` | 环境音 |
| 紧张感的弦乐 | `non_diegetic_music` | 只有观众能听见 |

### 8.4 写法公式

```
<环境底噪> + <1–2 个物理动作音> + （可选）<1 个非语言人声>
```

**三档，按长度选**：

```text
【1 句 · 精简】
Steady rainfall on asphalt and car roofs, water splashing underfoot.

【2–3 句 · 标准】
Steady rainfall on asphalt and car roofs, water splashing underfoot. A low hum comes from the
neon sign above the doorway. Distant traffic passes muffled and indistinct.

【4 句 · 上限】
A low ambient room tone with a faint fluorescent hum. Paper slides across a wooden surface and
a chair leg scrapes once against the floor. Outside, distant traffic passes at uneven intervals.
A single slow breath is released close to the microphone.
```

> 【1 句】雨点持续打在沥青与车顶上，脚下踩出水花。
> 【2–3 句】同上，加：门洞上方的霓虹招牌发出低沉的嗡鸣；远处车声经过，含混而难辨。
> 【4 句】低沉的室内底噪，夹杂微弱的荧光灯嗡鸣。纸张在木质表面上滑动，一只椅腿在地面上刮擦了一下。室外，远处的车流以不规则的间隔经过。靠近话筒处，一次缓慢的呼气被释放出来。

> ⚠️ **不要超 4 句**【官方】。场景声音很多时，挑 **1 个底噪 + 2 个动作音**，不要罗列。

### 8.5 与 §2 / §3 场景库配套的声景基线（17 条速查）

| 场景 | `overall_soundscape` 基线句（可直接复制） |
|---|---|
| 客厅（夜） | `A low refrigerator hum from off-frame, floorboards creaking once under shifting weight, fabric shifting as the subject settles into the sofa.` |
| 老宅书房（夜） | `A low ambient room tone, the soft rustle of paper, the faint tick of a clock from off-frame, floorboards creaking once.` |
| 开放式办公室（日） | `Distant keyboard clatter, a low ventilation hum, the muffled sound of a door closing somewhere off-frame.` |
| 会议室 | `A low ventilation hum, the scrape of a chair leg on the floor, a single sheet of paper sliding across the table surface.` |
| 病房（日） | `The steady beep of a monitor off-frame, a distant trolley rolling past the door, soft footsteps on vinyl flooring.` |
| 车内（夜·行驶） | `A low engine hum, tyre noise on wet asphalt, the soft click of the indicator, faint muffled traffic from outside.` |
| 走廊（夜） | `A low fluorescent hum, the soft echo of footsteps on hard flooring, a distant door closing.` |
| 咖啡馆（日） | `The low hiss of a steam wand, cups clinking on saucers, muffled conversation from off-frame, the chime of the door.` |
| 楼梯间 / 车库（夜） | `Footsteps echoing on concrete, a faint metallic ring from the handrail, a distant door slamming.` |
| 城市街道（日） | `Distant traffic, a light breeze through bare branches, the occasional car passing off-frame.` |
| 雨夜街道 | `Steady rainfall on asphalt and car roofs, water splashing underfoot, distant muffled traffic, a low roll of thunder far away.` |
| 雪地 / 雪夜 | `A low wind across open ground, snow crunching underfoot, a distant muffled rumble.` |
| 天台（夜） | `A low steady wind, distant muffled traffic from far below, the hum of a ventilation unit nearby.` |
| 校园（日） | `A distant school bell, muffled voices from behind closed doors, footsteps on hard flooring.` |
| 地下停车场（夜） | `A low fluorescent hum, the distant echo of an engine starting, footsteps with a hard echo, a metal door closing somewhere off-frame.` |
| 窄巷（夜） | `Water dripping somewhere out of sight, a distant siren, the hollow echo of footsteps between the two walls.` |
| 江边 / 码头（黄昏） | `Water lapping against the concrete, a distant boat horn, gulls calling, a light wind across open water.` |

**雾 / 逆光 / 丁达尔的补充声景**：

| 大气 | 声景句 |
|---|---|
| 雾 | `A muffled, dampened room tone; distant sounds arrive softened and indistinct; water dripping nearby.` |
| 逆光（黄昏） | `A low warm wind, distant birds, the faint hiss of long grass.` |
| 丁达尔（静室） | `A low, still room tone; a single floorboard creaking; faint dust settling.` |

### 8.6 `non_diegetic_music` 的环境侧注意（一句话）

【官方】`non_diegetic_music` **只写乐器、速度、节奏、动态变化，禁止抽象情绪词**。它**不归环境层管**，但提交时要一起检查，且**必须非空**（无配乐写 `N/A` 或 `no music`，见主模板 §6.6 第 8 条）。

```
❌  A sad and emotional piano piece that conveys her loneliness.
✅  A single sustained cello note at a slow tempo, entering halfway and swelling gently to the end.
```

---

## 9. 常见翻车与规避

### 9.1 场景突变（同一段落内背景换了地方）

| 项 | 内容 |
|---|---|
| **症状** | 三镜里的背景墙、家具、窗外景色不一致；第二镜突然换了个房间 |
| **根因** | ① 场景串三镜不一致（被"临场改了一个词"）；② 环境物件太少，模型自由发挥；③ 切镜引入了新空间但没写清楚 |
| **规避写法** | `The same room continues from the previous shot: the same blank off-white wall behind the sofa, the same low grey fabric sofa, the same floor lamp at the right of frame, the same key light from the upper right.` |
| **中文** | 同一个房间延续自上一镜：沙发背后同样是那面留白的米白墙，同样是那张低矮灰色布艺沙发，同样是画面右侧那盏落地灯，同样来自右上方的那束主光。 |
| **兜底** | 走 T2 单镜重生成，用 FL2VA 首尾帧钳住两侧（主模板 §3.2.3） |

### 9.2 光源漂移（主光方向在镜间换边）

| 项 | 内容 |
|---|---|
| **症状** | 第一镜光从左边来，第二镜从右边来；人脸明暗反转，看着像换了个人 |
| **根因** | 场景卡没建，或建了没查；不同人写不同镜 |
| **规避写法** | 每镜第六段（光影风格）统一写 `Lighting matches the lock block exactly.`；场景卡的「光照」组四行逐字复制 |
| **中文** | 光照与锁定块完全一致。 |
| **兜底** | 后期统一调色可缓解部分，但**明暗结构反转无法后期修** → 只能重生成 |

### 9.3 背景人物乱入

| 项 | 内容 |
|---|---|
| **症状** | 明明写了两个人，背景里长出第三个人的清晰脸；空椅子坐了人 |
| **根因** | 环境里存在"人形载体"（椅子、门、走廊尽头）且未声明空置 |
| **规避写法（三句，按需组合）** | `The only movement in frame is the one named above.`<br>`All the chairs are empty.`<br>`Passersby in the background are out of focus, their faces soft blurs of skin tone.` |
| **中文** | 画面内唯一的运动就是上面写到的那一处。／所有椅子都是空的。／背景中的路人处于焦外，面孔是柔和的肤色模糊。 |
| **为什么用正向不用否定** | 主模板 §6.4 F：裸名词否定（`no extra people`）会把名词本身送进条件分布、反向激活。**正向锚定 + 末尾一句 do not 收边**是 H3 最优写法 |
| ⚠️ **已废止的旧写法** | `No moving figures anywhere in frame.` —— 曾在场景串出现 9 次，属**完整否定句（⚠️ 弱档）且占掉唯一 1 句 `Do not` 配额**。改为上面第一句：既然已命名次级运动，就**占满了"运动描述位"**，额外人形无处安放 |

### 9.4 天气不一致（雨量忽大忽小 / 雪停了又下）

| 项 | 内容 |
|---|---|
| **症状** | 同一镜里雨量变化；跨镜时雪停了；雾浓度突变 |
| **根因** | 颗粒类大气是模型最难维持连续性的量之一 |
| **规避写法** | 见 §5.3 的密度声明三件套：`at a constant density` + `the same particle size` + `from the first frame to the last` + `does not start or stop mid-shot` |
| **中文** | 密度恒定 + 颗粒尺寸不变 + 首尾一致 + 不在中途开始或停止 |
| **兜底** | 把天气从"行进中"改成"已停"（`Rain has stopped; the ground is wet`），静态结果远比动态过程稳（防翻车词库 §9 原则①） |

### 9.5 物件数量失控

| 项 | 内容 |
|---|---|
| **症状** | 写了 8 件物件，只出现 4 件，且每次生成丢的还不一样 |
| **根因** | 物件互相竞争注意力 |
| **规避** | 压到 **3–5 件**（§1.4）；需要更多细节时，用**背景虚化**暗示而不是逐件列举 |
| **实测方法** | 见 §1.4 的五版本测试 |

### 9.6 窗外 / 镜面反射穿帮

| 项 | 内容 |
|---|---|
| **症状** | 室内日景，窗外长出随机城市；镜子里映出不存在的人 |
| **根因** | 窗与镜是"通向另一个空间的洞"，模型会填满它 |
| **规避写法** | 窗户：`the window is a flat black rectangle behind it`（夜）<br>窗户：`its glass showing only an out-of-focus pale grey sky`（日）<br>镜面：**能不写就不写**；必须写则 `the mirror is angled away from camera and shows only the blank wall` |
| **中文** | 窗户是一块纯黑的矩形，窗后是一整片均匀的暗。／玻璃上只有虚化的浅灰色天空，看不到任何建筑。／镜子背对镜头，只映出那面素墙。 |

### 9.7 地面接触阴影缺失（人物"飘"在地上）

| 项 | 内容 |
|---|---|
| **症状** | 人物像贴纸浮在地面上，没有接触阴影 |
| **根因** | 只写了主光，没写地面与接触关系 |
| **规避写法** | `A soft contact shadow sits directly beneath her feet on the floor.` |
| **中文** | 她脚下的地面上，正下方有一片柔和的接触阴影。 |

### 9.8 内外景光比不一致（窗边人物脸过暗）

| 项 | 内容 |
|---|---|
| **症状** | 窗很亮，人物脸全黑；或反之，人物正常但窗外过曝 |
| **根因** | 室外亮度远高于室内，模型难同时保住两端 |
| **规避** | ① 室外部分写 `out-of-focus ...`（降低它的细节需求）；② 给人物一个补光（仍守住"一主一补"）；③ 实在不行，把机位改为**背窗**（窗在人物身后成为背景） |

### 9.9 长运镜 / 大摇摄必须配简背景（环境侧配合项）

> 由 `h3-camera-edit` 提出，环境侧必须配合执行，**这是长运镜最常见的失效形态**。

| 项 | 内容 |
|---|---|
| **症状** | 长横移 / 大摇摄时，背景出现摩尔纹、闪烁、图案"沸腾" |
| **根因** | 背景持续流过画面时，任何**细密重复图案**都会在采样中产生干涉 |
| **规避写法** | `simple background, minimal environment, soft bokeh, plain surfaces and smooth gradients throughout` |
| **中文** | 简洁背景、最小环境、柔和散景，通篇为素面与平滑渐变。 |
| **环境侧配合** | 排到长运镜时，从 §2 / §3 场景库**换掉**含重复图案的场景，见下表 |

**重复图案场景替换表**（长运镜 / 大摇摄时生效）

| 高危场景（含重复图案） | 替换为 |
|---|---|
| 走廊（顶灯序列 + 瓷砖缝） | 窄巷（单光源纵深，砖墙虚化） |
| 病房（百叶光带） | 客厅（素墙 + 单一落地灯） |
| 地下车库（柱网 + 车位线） | 江边码头（开阔水面，无重复结构） |
| 会议室（椅阵） | 老宅书房（书架虚化，无重复结构） |
| 雨夜街道（雨丝 + 湿路反光） | 雪地（均匀低对比，无图案） |

**时间流逝镜**（衔接镜 #10）同属环境语义，见 `h3-camera-edit`：砍掉一切可读时间信息（"时钟指向 3 点"属文字类崩坏，与招牌乱码同源），改抽象时间感 —— 用光的明度与色温渐变桥接。

> ⚠️ 该节原例句结尾的 `no visible clock face, no numbers, no text` 是**裸名词否定串**，按主模板 §6.4-F ❌ 禁用。**用 §1.6 的正向串替代**：`The walls and the floor are plain, unmarked surfaces showing only colour, material and the slow change of the light.`

### 9.10 环境类自建实测方法（三条，量产前各跑一遍）

> 环境层没有任何公开的量化基准。**不要引用网上任何"某模型场景保真度 XX%"的说法**——那些出自聚合站/营销软文，无方法论、无可复现测试集（防翻车词库 §10 已判定不可引用）。

| 测试 | 做法 | 指标（本 skill 命名【工程取值】） | 目标 |
|---|---|---|---|
| **场景复现测试** | 同一场景串 + 同一参考图，生成 **10 次**（必须在有运镜/有动作的条件下测，静态测无意义） | **SPR（Scene Persistence Rate）** = 全部登记物件都在位的比例 | ≥ 80% |
| **光源方向测试** | 同一场景串，只改主光方向（左 / 右 / 上），各 10 次，盲评三镜光照一致性 | **LCR（Lighting Consistency Rate）** | ≥ 80% |
| **大气密度测试** | 同一天气场景串，加 / 不加密度声明各 10 次，逐帧看雨量/雪量是否恒定 | **ADR（Atmosphere Density Rate）** | ≥ 70% |

**处置规则**（沿用防翻车词库 §5.4 的分级逻辑）：

| 成功率 | 处置 |
|---|---|
| ≥ 90% | 可承载叙事信息，正常使用 |
| 70% – 90% | 可出现，但**不得承载叙事信息** |
| < 70% | **砍掉或替换**（如把"靠窗外的城市天际线识别地点"改成"靠室内那盏红色落地灯识别地点"） |

**设计原则（与环境层直接相关）**：

- 把"这是哪个地方"的识别，设计在**大面积、高对比、位置固定**的物件上。一面红墙 > 桌上的一个小摆件。
- 环境物件若承载叙事信息，**必须出参考图**（防翻车词库 §5.2：`是否出参考图` 是主判据，非加分项）。
- **不要边拍边测。** 高价值场景量产前全测一遍。

---

## 10. 检查清单 + 正反例速查

### 10.1 提交前检查清单（环境层，12 条，可勾选）

```
□ 1.  场景串来自场景卡，是复制粘贴，不是临场重写
□ 2.  三镜的场景串与「光照」组四行逐字一致（做字符串比对，不是人眼看）
□ 3.  场景串含四件套：空间边界 / 3–5 件物件 / 单一主光 / ≥1 个次级运动
□ 4.  没有氛围词与抽象词（cozy / eerie / luxurious / sad / tense 一个都没有）
□ 5.  主光只有一个，有方向、有色温、有光质
□ 6.  光照收边用了正向锚定（夜/日二选一，见 §1.6），没写 "No other light source"
□ 7.  位置用画面方位（frame left / right third），没有 "on her left" 这类角色左右
□ 8.  多人时：人数写死、外观拉开差异、每人一个动作、距离有量化声明 + 恒定性声明
□ 9.  前景占比 ≤ 1/4，前景是一片色调均匀的暗剪影
□ 10. 后景写了 "out of focus"（焦外已承载"不可辨认"，不再加否定尾巴）
□ 11. 窗 / 镜 / 屏幕等"通向别处的洞"已写死内容或写死为空
□ 12. 天气类写了密度声明三件套（constant density / same size / 首尾一致）
```

### 10.2 生成后看片检查清单（环境层，8 条）

```
□ 1.  三镜背景是不是同一个地方（墙、家具、窗外）
□ 2.  三镜主光方向是否一致（看鼻影、眼下阴影的位置）
□ 3.  色温有没有中途变（看白平衡）
□ 4.  背景有没有莫名多出人形，空椅子有没有坐人
□ 5.  登记的环境物件是不是都在位，有没有多出未登记的物件
□ 6.  雨/雪/雾的密度是否恒定，有没有中途停或变大
□ 7.  次级运动有没有出现（热气 / 尘埃 / 树动 / 水波），画面是不是"死"的
□ 8.  人物脚下有没有接触阴影，有没有"飘"在地上
```

### 10.3 正反例速查表（一张表看完）

| 维度 | ❌ 反例 | ✅ 正例 |
|---|---|---|
| 氛围 vs 物件 | `a cozy living room` | `a low grey fabric sofa, a blank off-white wall, a floor lamp at the right of frame` |
| 情绪 | `she looks sad` | `her shoulders drop, her gaze stays on the floor, her lower lip presses flat` |
| 位置 | `on her left` | `at the left third of frame` |
| 距离 | `they stand nearby` | `they stand two arm's lengths apart and this distance stays constant for the whole shot` |
| 多人 | `two men in suits` | `a tall man in a dark suit at the left third of frame and a shorter man in a grey suit at the right third of frame` |
| 背景人群 | `people in the background` | `blurred passersby in the background, out of focus` |
| 光源 | `soft lighting, warm` | `A single soft key light from the upper right of frame at 45°, warm amber.` |
| 多光源 | `lit by a lamp and a window` | `A single soft key light from the upper right at 45°, warm amber. The rest of the frame falls into shadow, reading as one soft unbroken darkness.` |
| 色温数值 | `3200K` | `warm amber`（K 值只作团队沟通语言，见 §4.4） |
| 光比 | `4:1 lighting ratio` | `a soft fill from camera right, the shadow side holds visible detail` |
| 天气 | `it is raining` | `Rain falls steadily and evenly across the whole frame; rain streaks fall continuously at a constant density; the puddle surface ripples with each drop.` |
| 风 | `a windy day` | `A steady breeze moves through frame from right to left; the tree branches sway continuously in one direction.` |
| 次级运动 | 不写 | `Steam rises steadily from the cup; a thin curtain breathes in and out.` |
| 窗外 | 不写 | `its glass showing only an out-of-focus pale grey sky` |
| 接触阴影 | 不写 | `A soft contact shadow sits directly beneath her feet on the floor.` |
| 前景 | `a plant in the foreground` | `a dark out-of-focus silhouette occupies the left quarter of frame, its edge clean and its surface one even dark tone` |
| 否定写法 | `No extra people, no six fingers.` | 正向锚定铺到底；do not 只写正向没覆盖到的（见 §1.6） |
| 场景变更 | 每镜重写场景 | 场景卡外置 + 三镜逐字复制 |
| 声景 | `a tense atmosphere with dramatic music` | `overall_soundscape: A low ambient room tone, the soft rustle of paper, a distant door closing.`<br>`non_diegetic_music: A single sustained cello note at a slow tempo, entering halfway.` |

### 10.4 最小可复制集（赶时间就抄这四段）

```text
【场景串骨架】
<空间边界>. <物件1>, <物件2>, <物件3>. A single <soft|hard> key light from <方向>, <色温>.
<次级运动>. The rest of the frame falls into shadow, reading as one soft unbroken darkness.

【光照串】
A single soft key light from the upper right of frame at 45°, warm amber. The rest of the frame falls into shadow, reading as one soft unbroken darkness.

【站位串 · 双人】
A tall man in a dark suit at the left third of frame and a shorter woman in a grey coat at the
right third of frame; they stand two arm's lengths apart and this distance stays constant for the
whole shot.

【密度声明 · 天气】
The rain holds a constant density and the same particle size from the first frame to the last;
it does not start or stop mid-shot and it does not flicker.
```

> 中文对照见 §1.3（场景串骨架）、§4.3.1（光照串）、§6.2（站位串）、§5.3（密度声明）。此处不重复，避免两份译文将来改一处漏一处。

---

## 附录 A：本 skill 的【待验证】清单（跑完实测请回填）

| # | 待验证项 | 实测方法 | 你的结果 |
|---|---|---|---|
| 1 | 场景串物件数上限（默认 7 件） | §1.4 五版本测试 | ___ |
| 2 | 模型对 K 值（`3200K`）的响应度 | §4.4 A/B 十次盲评 | ___ |
| 3 | 光比数字（2:1 / 4:1 / 8:1）是否响应 | §4.5 | ___ |
| 4 | 距离声明对"两人被拉到一起"的抑制效果 | §6.2 对照十次测量方差 | ___ |
| 5 | 单一主光 vs 主光+补光的一致性差异 | §4.2 | ___ |
| 6 | SPR（场景复现率） | §9.9 | ___ |
| 7 | LCR（光照一致率） | §9.9 | ___ |
| 8 | ADR（大气密度率） | §9.9 | ___ |

> **本 skill 中所有阈值（3–5 件物件 ≤7、SPR ≥80%、前景 ≤1/4、一镜 ≤2 个有名人物）均为【工程取值】或【推断】**，不是官方数据。跑完实测后请用你的结果覆盖，并在团队内同步。

## 附录 B：与其他 skill / 文档的接口

| 你要做的事 | 去哪 |
|---|---|
| 写整条 H3 提示词（三字段、时间戳、对白标签） | 主模板模块六 + 模块七 |
| 写角色外观 / 服装 / 小物件 | 主模板模块五（角色卡与资产表） |
| 选运镜术语 | 主模板 §7.5（官方术语表） |
| 排 15 秒 3 镜时长 | 主模板 §3.2 |
| 跨段锚点工程 | 主模板 §3.6（匹配三锚点）+ 本 skill §7.2 |
| 参考图怎么分配 | 防翻车词库 §2 + 本 skill §7.5 |
| 画面崩了先干什么 | 主模板 §8.4 —— **先抬采样步数到 6–8，再改提示词** |
| 写环境音 | 本 skill §8 |

