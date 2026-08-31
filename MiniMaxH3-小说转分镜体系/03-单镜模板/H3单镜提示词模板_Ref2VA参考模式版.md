# H3 提示词模板 · Ref2VA 全能参考模式版
### 面向「15 秒 3 镜」AI 漫剧 · 官方六段式结构

> **与 `H3单镜提示词模板_v1.md` 的关系**：v1 是 **Base 四段式**（T2VA / FL2VA，无参考文件或仅 1–2 张首尾帧）。本文件是 **Ref2VA 六段式**（omni-reference，最多 12 个参考文件）。
> **客户锁资产走的是 omni-reference，因此本文件为主力模板，v1 退为 FL2VA 专用场景使用。**

---

## ⚠️ 使用前必读：参考标签有两种官方来源，写法冲突，未定论

**本文件正文已统一转换为 `ref-en.txt` 写法**（首字母大写 + 空格 + 数字）。

**但存在第二条官方来源，两者不一致，且都自称官方：**

| 来源 | 写法 | 性质 |
|---|---|---|
| **本文件所用** —— `MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/ref-en.txt` | `<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>` | MiniMax 自有 GitHub 组织的**提示词写作专用指南** |
| MiniMax 官方开源公告的 API 脚本 | `<image_1>` / `<video_1>` / `<audio_1>`（小写 + 下划线 + 数字） | 开源公告中的 API 示例脚本 |

**采用 `ref-en.txt` 的理由**：它出自 MiniMax 自有仓库的**提示词写作专用指南**，与"怎么写提示词"直接对口；公告脚本里的写法面向 API 调用示例，语境可能不同。

**⚠️ 转换说明**：本文件原用小写下划线式，已**机械转换**为官方指南式，规则是
`<image_N>` → `<Subject N>`、`<video_N>` → `<Video N>`、`<audio_N>` → `<Audio N>`。

> 经逐条核对，原文件中 `<image_N>` 的用法**全部是"定妆图 / 物件参考 / 出现在哪些镜"**，
> **无一例用作首帧或分镜锚点**，因此统一转 `<Subject N>` 语义正确。

**若你新增用法，要按语义选**：
- `<Subject N>` —— 从参考素材抽象出来的**可复用可见内容**（人、物、画风）
- `<Picture N>` —— 用作**具体目标帧或分镜锚点**的参考图（如"本镜首帧"）
- `<Video N>` / `<Audio N>` —— 参考视频 / 参考音频，**两者独立编号**

**同一份提示词内绝不能混用两套写法。**

**【待验证】两条官方口径谁为准，未定论。** 实测方法：同一份素材与提示词，分别用两套写法各生成 5 次，比对① 模型是否按标签锁定对应素材 ② 锁定准确率有无差异 ③ 是否出现标签未被解析（模型把标签当普通文本生成出来）。
**若你实测出结论，请回填到本文件与主模板模块七。**

---

## 0. 证据标注与来源

| 标记 | 含义 |
|---|---|
| **【官】** | MiniMax 官方原文（开放平台文档 / 官方开源公告中的真实 API 脚本 / HuggingFace 官方 `VIDEO_PROMPT_WRITING_GUIDE`） |
| **【官·转述】** | 官方约束，但由 team-lead 从 API 文档转述、h3-official-research 核实，**我未直接验证原始文档** |
| **【三方】** | 第三方实测/整理，可追溯但非官方 |
| **【推断】** | 机制推断，无实测数据 |

---

## 0.5 双版本产出约定（每镜必带两份提示词）

本模板是 **【H3版（H3看）】** 的写法规范。但**写分镜时，每镜必须同时产出两份、成对出现**——一份给人看，一份给 H3 看：

| 版本 | 给谁看 | 语言 | 形态 | 由谁产出 |
|---|---|---|---|---|
| **【中文版（人类看）】** | 人（你审、改、确认、沟通意图） | 纯中文自然语言 | 按「主体/动作/对白/环境/运镜/光影」顺序写的白话稿 | 模块六中文详版 |
| **【H3版（H3看）】** | 模型（H3 实际吃进去的） | 官方六段式英文 | 本模板的 `subject_definitions` → `detailed_description` | 模块七转译 |

**三条硬规则**：

1. **两份描述同一镜**，H3版由中文版转写而来，**不是两套独立创作**——改中文版要同步 H3版，反之亦然，不能各写各的（避免两边漂移）。
2. **中文版是源头、H3版是终点**：先写中文版把控细节与剧情，再转写成 H3版；不要先写英文再"翻译"成中文。
3. **分镜脚本里两者相邻放置**：推荐上方「【中文版（人类看）】」、下方「【H3版（H3看）】」，各用标题标注，方便一眼对照。

> 范式成品：`MiniMaxH3_分镜脚本_15s3镜.md` 的「二、逐镜详解」即中文版、「三、可直接粘贴的 H3 提示词」即 H3版，两者一一对应。

### 0.5.1 一镜双版对照示例（以 Shot 1 为例）

**【中文版（人类看）】**

> 中景。蒋筱筱坐在沙发左下三分之一处，身体朝镜头偏 45°。双手在胸前捧着那封米白色信封。
> 几缕头发在静止空气里轻晃；然后她低头看信，拇指沿信封边缘滑一下。
> 她不说话，嘴唇闭着。落地灯暖光稳在脸颊，信封在风衣上投下淡影。
> 镜头小幅缓慢推近，从中景到中近景。光位与场景锁定块一致。
> 结尾她仍低头、信仍在双手，构图收在胸以上。信封上不出现任何文字。

**【H3版（H3看）】**（完整六段见 §8，此处取 `detailed_description` 段作对照）

```text
[Shot 1] A medium shot frames <Subject 1> seated on the sofa in the lower-left third of frame,
  body angled three-quarters to camera, the off-white envelope from <Subject 6> held in both
  hands at chest height. A few loose strands of her hair shift in the still air, then she
  lowers her chin and looks down at the envelope, then her thumbs slide once along its edge.
  She does not speak; her lips remain closed. The warm floor-lamp light holds steady on her
  cheek; the envelope casts a soft shadow on her coat. The camera pushes in with small
  amplitude at slow speed from a medium shot to a medium close-up. Lighting follows <Subject 5>.
  By the end of the shot she is still looking down, envelope still in both hands, framed
  chest-up. Do not show any text on the envelope.
```

> 对照要点：中文版「几缕头发在静止空气里轻晃；然后她低头看信」↔ H3版 `A few loose strands ... shift ... then she lowers her chin`；**时序词 `then` 是两边都保留的骨架**，转写时不能丢。

---

## 1. ⚠️ 前置决策：Ref2VA 与 FL2VA **互斥**，必须先二选一

**【官·转述】图生视频与全能参考互斥**：`first_frame` / `last_frame` 与 `reference_*` **不可同时出现在同一次请求中**。

→ **走 Ref2VA 就没有首尾帧；走 FL2VA 就不能用 9 张参考图。**

| 维度 | **Ref2VA（本模板）** | **FL2VA（用 v1 模板）** |
|---|---|---|
| 参考文件 | 最多 12 个（图 ≤9 / 视频 ≤3 / 音频 ≤3） | 仅 1–2 张图（首帧 + 尾帧） |
| 首尾帧控制 | ❌ 无 | ✅ 可精确控制首帧与尾帧构图 |
| 一致性手段 | 每资产独立锁定 + 保留强度标记 | 描述串 + 2 张图 |
| 成本 | 前 5 图免费，第 6 图起 $0.04/张；视频按时长计费；音频免费 | 无额外参考费用 |
| **适用** | **角色多、资产多、跨镜一致性优先** | **需要精确首尾构图的镜型** |

### 决策规则（分镜师照此判断）

```
本段落是否含有「必须精确控制尾帧构图」的镜型？
   │
   ├─ 是 → 走 FL2VA（用 v1 模板）
   │       触发镜型：
   │         · #7 局部→整体揭示镜（需尾帧锁终点构图）
   │         · #6 同构图匹配镜（需首帧锁构图）
   │         · 任何"终点构图必须由我指定"的镜头
   │       ⚠️ 代价：放弃 9 图资产锁，一致性退化为"2 张图 + 描述串"
   │
   └─ 否 → 走 Ref2VA（用本模板）  ← 默认路径
           典型段落：对白段、情绪段、过肩段、手部特写段
           衔接靠：构图描述 + 时间戳 + 后期
```

> ### ⚠️ 一个真实的设计冲突，请分镜阶段就规避
> **同一段落内不能混用 Ref2VA 与 FL2VA。**
> 若某一段落里既有需要 9 图锁资产的镜，又有一个 #7 揭示镜（需尾帧），**该段必须整体走 FL2VA**，从而**放弃 9 图资产锁**，身份漂移风险随之上升。
> **建议**：把 #7 揭示镜**单独拆成一次 FL2VA 请求**生成，其余镜走 Ref2VA，最后在剪辑台拼接。这样两种能力都不浪费。
> 代价：接缝处需人工对齐（走的正是 T2 降级梯的逻辑）。

---

## 2. 六段结构总览与字数预算

| # | 字段 | 作用 | 字数预算（汉字） | 必填 |
|---|---|---|---|---|
| ① | `subject_definitions` | 逐一点名每个参考文件**是什么** | 100–180（每个文件 15–25 字） | ✅ |
| ② | `summary` | 一段话说清整体任务 | 60–120（含任务类型标签） | ✅ |
| ③ | `retention_analysis` | **逐个文件指定保留强度 + 保留什么** | 180–320（每个文件 30–50 字） | ✅ |
| ④ | `detailed_description` | 主时间轴：画面 + 动作 + 对白 + 画内音 | **每镜 250–400，三镜合计 750–1200** | ✅ |
| ⑤ | `overall_soundscape` | 环境音、物理音、非语言人声 | 60–150 | ✅ |
| ⑥ | `non_diegetic_music` | 仅观众可听的配乐，或 `N/A` | 20–60 | ✅ |
| | **全套合计** | | **1170–2030** | |

> **【三方】官方参考值（非硬配额）**：复杂场景 `detailed_description` 建议 **350–450 英文词**，简单单镜 **150–250 英文词**。40 词的提示词会让模型自行填空，正是随意写法的短板。（来源：bottlerocket / inreels 整理，trace back to MiniMax docs，**非官方硬配额**）
> 三镜段落因含三个镜，总量高于单镜参考值属正常。

---

## 3. 段① `subject_definitions` —— 逐一点名每个文件

**写法**：`<文件ID> is <它是什么>`。**不要只写文件名**，要说清它在画面里的角色。
**占位符格式**（本文件正文所用，小写 + 下划线 + 序号）：`<Subject 1>` / `<Video 1>` / `<Audio 1>` / `<Audio 2>`。

> ⚠️ **这不是唯一官方写法，且与 `ref-en.txt` 冲突**。官方提示词指南用的是 `<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>`。
> **建议改用后者**，替换映射见文首「使用前必读」。保留本套仅为与开源公告脚本对照。

```
subject_definitions:
<Subject 1> is the 28-year-old woman's front-facing character sheet: oval face, shoulder-length
  straight black hair, dark brown almond eyes, natural skin texture.
<Subject 2> is her left three-quarter view.
<Subject 3> is her full-body reference, showing the ivory T-shirt, khaki trench coat,
  straight-leg jeans and white canvas shoes.
<Subject 4> is the 35-year-old man's front-facing character sheet.
<Subject 5> is the location empty plate, showing the sofa, the blank wall and the floor lamp
  on the right that provides the only light source.
<Subject 6> is the off-white envelope, exact product reference.
<Subject 7> is the colour-grade and art-style reference.
<Subject 8> is the hand-pose reference: both hands resting flat, fingers held together.
<Video 1> is the camera-movement reference: a slow small-amplitude push-in.
<Video 2> is the editing-rhythm reference: three cuts, roughly five seconds each.
<Audio 1> is the woman's speaking voice, timbre reference.
<Audio 2> is the man's speaking voice, timbre reference.
```
> **【官】参考文件硬限制**：图片 ≤9 张；视频 ≤3 段（单段 2–15s，**合计 ≤15s**）；音频 ≤3 段（单段 2–15s，**合计 ≤15s**，**且必须配图片或视频，不能单独输入**）；**混合总上限 12 个文件**。

---

## 4. 段② `summary` —— 任务类型标签 + 一段话

**【官】官方示例在 summary 开头用了方括号任务类型标签**：`[video editing + audio reference + audio reuse]`。标签后接一段自然语言，说清：目标视频是什么、谁在画面里、发生什么改动、音频怎么处理。

```
summary:
[reference-to-video + audio reference] The target video is a 15-second three-shot dialogue
scene in a night-time living room. <Subject 1>, wearing the trench coat from <Subject 3>, sits on
the sofa holding the envelope from <Subject 6>, then hands it to <Subject 4>. The visual style and
colour grade follow <Subject 7>. The camera language follows <Video 1> and the cutting rhythm
follows <Video 2>. The woman's voice references <Audio 1> and the man's voice references <Audio 2>.
```

---

## 5. 段③ `retention_analysis` —— **本模板的核心**

### 5.1 官方条目格式

```
<文件ID> (<出现在哪些镜 / 扮演什么角色>): <保留强度标记> - <具体保留的内容，用英文写>
```
官方真实条目（摘自 MiniMax 官方开源公告的 API 脚本；⚠️ 注意：该脚本所用标签写法与 `ref-en.txt` 不一致，见文首「使用前必读」）：
```
<Subject 1> (appears in [Shot 1]): fully_preserved - the man retains his identity, wavy blonde
    hair, pink suit, white shirt, accessories, and the black lamb he holds, with his mouth
    newly animated to speak.
<Video 1> (source video editing): fully_preserved - the original camera framing, warm golden
    hour lighting, grassy hill setting, and background white lambs are maintained while the
    central character is edited.
<Audio 1>: partially_copy - the atmospheric background music from <Audio 1> is reused in the
    target video, mixed beneath the newly added spoken dialogue.
<Audio 2>: reference - the target audio references the male voice timbre from <Audio 2> to
    generate <Subject 1>'s spoken dialogue.
```

### 5.2 六个保留强度标记 · 选择决策表

| 标记 | 含义 | **什么时候用** | 典型资产 |
|---|---|---|---|
| **`fully_preserved`** | **完全保留**：身份、特征、道具全部不变 | **承载身份识别、观众会认的东西** | 脸、发型、核心服装、关键道具（戒指/耳环/信封）、场景光位 |
| **`partially_preserved`** | 部分保留：主体不变，细节可随情境微调 | 允许随表演变化的 | 外套的开合/褶皱、发型的松散度、妆的浓淡 |
| **`attribute_transfer`** | **只迁移属性**：风格、材质、色彩、质感，**不搬物体** | **纯风格类参考** | 画风参考、调色参考、材质参考、颗粒感 |
| **`weak_reference`** | 弱参考，仅作倾向 | 只提供方向、不做约束 | 氛围板、构图倾向、光影感觉 |
| **`partially_copy`** | 部分复制（音频轨复用） | 要复用已有音轨 | 复用已有 BGM、环境音 |
| **`reference`** | 参考（音频：音色/音轨） | 要参考但不复制 | 角色音色参考 |

### 5.3 客户视角的实用规则（背诵版）

```
脸 / 发型 / 核心服装 / 关键道具  →  fully_preserved
画风 / 调色 / 材质              →  attribute_transfer
氛围板 / 构图倾向               →  weak_reference
音色 / BGM                      →  reference / partially_copy
```

> **【官】官方原句**：*"A marker of `fully_preserved` on a face is what keeps it the same face all the way through."*
>
> ⚠️ **最容易犯的错**：把**画风参考图误用 `fully_preserved`**。后果是模型会把那张参考图里的**物体也搬进画面**（官方对 `attribute_transfer` 的定义就是"只迁移属性、不搬物体"）。画风图一律 `attribute_transfer`。

### 5.4 本模板示例的 retention 写法

```
retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - she retains her exact facial
    identity, oval face, shoulder-length straight black hair, dark brown almond eyes, skin
    texture and age throughout, with only her mouth newly animated to speak.
<Subject 2> (appears in [Shot 1]): fully_preserved - the three-quarter view is used only to
    confirm facial geometry; no objects are taken from it.
<Subject 3> (appears in [Shot 1], [Shot 2]): fully_preserved - the ivory T-shirt, khaki trench
    coat, straight-leg jeans and white canvas shoes remain unchanged in every shot.
<Subject 4> (appears in [Shot 2], [Shot 3]): fully_preserved - the man retains his identity,
    short cropped hair, grey wool coat and age throughout.
<Subject 5> (appears in [Shot 1], [Shot 2], [Shot 3]): partially_preserved - the sofa, blank
    wall and floor lamp position and the warm key-light direction from camera right are
    maintained; small props may vary.
<Subject 6> (appears in [Shot 2]): fully_preserved - the off-white envelope keeps its exact
    size, colour and shape, and is never duplicated or replaced.
<Subject 7>: attribute_transfer - only the muted teal-and-amber grade, contrast curve and film
    grain are adopted; no objects or subjects are taken from this image.
<Subject 8> (appears in [Shot 2]): attribute_transfer - only the hand pose is adopted
    (both hands flat, five fingers held together, natural proportions).
<Video 1>: attribute_transfer - only the camera-movement language is adopted (slow
    small-amplitude push-in); no visual content is taken from it.
<Video 2>: attribute_transfer - only the cutting rhythm is adopted (three cuts, roughly
    five seconds each).
<Audio 1>: reference - the target audio references the woman's voice timbre.
<Audio 2>: reference - the target audio references the man's voice timbre.
```

---

## 6. 段④ `detailed_description` —— 主时间轴

### 6.1 ⚠️ 风格开场位置：与 Base 模式不同

| 模式 | 风格串位置 |
|---|---|
| **Base（v1 模板）** | 写在 `[Shot 1]` **之后** |
| **Full-Reference（本模板）** | 在 `[Shot 1]` **之前**，用 **1–2 句英文**先建立 |

**【官】官方示例佐证**：
```
detailed_description:
The target video is in realistic photographic style.
[Shot 1] The shot begins from the source <Video 1>, showing <Subject 1>, a young man with ...
```
→ 风格句 `The target video is in realistic photographic style.` 位于 `[Shot 1]` **之前**。

### 6.2 每镜六段顺序（沿用 v1，映射官方 11 要素）

| 段 | 名称 | 预算（汉字） |
|---|---|---|
| ① | subject 主体与开场构图 | 50–80 |
| ② | 时序动作节拍（**用「然后」串联，禁用「同时」**） | 50–90 |
| ③ | 对白（`说话人描述 + 语气` 在标签**外**；`(S1)` + `[语言]` + 台词在 `<d>` 标签**内**；台词**不加英文双引号**） | 30–80 |
| ④ | 环境反应（次级运动：发丝/衣摆/光影/热气） | 20–40 |
| ⑤ | 运镜（**只用官方术语，一镜一个**） | 30–50 |
| ⑥ | 光影风格（只写与本段差异） | 20–40 |
| ⑦ | 收尾状态 | 30–60 |
| — | 收边（**最多 1 句 `Do not ...`**，且前面必须先有正向描述） | ≤25 |

### 6.3 时间戳规则

```
[Shot 1] ...                                  ← 第一镜不加时间戳
[Shot 2] At 00:05.000, the camera cuts to ... ← 之后每镜必须带
[Shot 3] At 00:10.500, the shot switches to ...
```
- Shot 1 不带时间戳；之后每镜**必须带、必须递增、必须落在请求时长内**
- 实测切点精度 **±0.12 秒**（软引导，非硬约束）
- **不要指定精确帧数或 FPS**——时机由模型控制
- 每镜最短 **1.5 秒**（硬下限）；设计取 **2 秒**；承载信息镜 **≥3 秒**

---

## 7. 段⑤⑥ 声音层

```
overall_soundscape:
夜间的安静客厅底噪，纸张摩擦声，布料摩擦声，她一次缓慢的吸气，
落地灯极轻微的电流声。

non_diegetic_music:
低频弦乐，极慢速度，在第二镜推起、第三镜结束前淡出。
（无配乐时明确写：no music；不要留空）
```
**判别规则**：问"画面里的人能不能听见"——能 → `overall_soundscape`；只有观众能听见 → `non_diegetic_music`。

---

## 8. 完整填好的示例（15 秒 3 镜 · 12 文件分配示范）

> **本示例即一份【H3版（H3看）】完整稿。** 与其配对的【中文版（人类看）】由模块六中文详版产出，
> 一镜双版的写法与对照见 §0.5。

**参考文件分配：8 图 + 2 视频 + 2 音频 = 12**（用满混合上限）

| 槽位 | 内容 | 保留强度 |
|---|---|---|
| image_1 | 女主正面定妆 | `fully_preserved` |
| image_2 | 女主左侧 45° | `fully_preserved` |
| image_3 | 女主全身（服装鞋） | `fully_preserved` |
| image_4 | 男主正面定妆 | `fully_preserved` |
| image_5 | 场景空镜（含光位） | `partially_preserved` |
| image_6 | 道具：米白色信封 | `fully_preserved` |
| image_7 | 画风调色参考 | `attribute_transfer` |
| image_8 | 手部姿态参考 | `attribute_transfer` |
| video_1 | 镜头运动参考（缓推） | `attribute_transfer` |
| video_2 | 剪辑节奏参考（三切） | `attribute_transfer` |
| audio_1 | 女主音色 | `reference` |
| audio_2 | 男主音色 | `reference` |

> **注意**：本例走 Ref2VA，**因此没有首帧/尾帧**（字段互斥）。三镜衔接靠构图描述 + 时间戳 + 后期。

```
subject_definitions:
<Subject 1> is the 28-year-old woman's front-facing character sheet: oval face, shoulder-length
  straight black hair, dark brown almond eyes, natural skin texture.
<Subject 2> is her left three-quarter view.
<Subject 3> is her full-body reference, showing the ivory T-shirt, khaki trench coat,
  straight-leg jeans and white canvas shoes.
<Subject 4> is the 35-year-old man's front-facing character sheet: square jaw, short cropped
  hair, grey wool coat.
<Subject 5> is the location empty plate: a light grey fabric sofa, a blank wall, and a floor
  lamp on the right that is the only light source.
<Subject 6> is the off-white envelope, exact product reference.
<Subject 7> is the colour-grade and art-style reference.
<Subject 8> is the hand-pose reference: both hands resting flat, five fingers held together.
<Video 1> is the camera-movement reference: a slow small-amplitude push-in.
<Video 2> is the editing-rhythm reference: three cuts, roughly five seconds each.
<Audio 1> is the woman's speaking voice, timbre reference.
<Audio 2> is the man's speaking voice, timbre reference.

summary:
[reference-to-video + audio reference] The target video is a 15-second three-shot scene in a
night-time living room. <Subject 1> sits on the sofa holding the envelope from <Subject 6>, reads
it, then hands it to <Subject 4> and looks up at him. The visual style and grade follow
<Subject 7>. The camera language follows <Video 1> and the cutting rhythm follows <Video 2>.
The woman's voice references <Audio 1> and the man's voice references <Audio 2>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - she retains her exact facial
    identity, oval face, shoulder-length straight black hair, dark brown almond eyes, skin
    texture and age throughout, with only her mouth newly animated to speak.
<Subject 2> (appears in [Shot 1]): fully_preserved - used only to confirm facial geometry;
    no objects are taken from it.
<Subject 3> (appears in [Shot 1], [Shot 2]): fully_preserved - the ivory T-shirt, khaki trench
    coat, straight-leg jeans and white canvas shoes remain unchanged in every shot.
<Subject 4> (appears in [Shot 2], [Shot 3]): fully_preserved - the man retains his identity,
    short cropped hair, grey wool coat and age throughout.
<Subject 5> (appears in [Shot 1], [Shot 2], [Shot 3]): partially_preserved - the sofa, blank
    wall and floor lamp position and the warm key-light direction from camera right are
    maintained; small props may vary.
<Subject 6> (appears in [Shot 2]): fully_preserved - the off-white envelope keeps its exact
    size, colour and shape, and is never duplicated or replaced.
<Subject 7>: attribute_transfer - only the muted teal-and-amber grade, contrast curve and film
    grain are adopted; no objects or subjects are taken from this image.
<Subject 8> (appears in [Shot 2]): attribute_transfer - only the hand pose is adopted (both
    hands flat, five fingers held together, natural proportions).
<Video 1>: attribute_transfer - only the camera-movement language is adopted.
<Video 2>: attribute_transfer - only the cutting rhythm is adopted.
<Audio 1>: reference - the target audio references the woman's voice timbre.
<Audio 2>: reference - the target audio references the man's voice timbre.

detailed_description:
Live-action, cinematic and photorealistic, in the muted teal-and-amber grade of <Subject 7>.

[Shot 1] A medium shot frames <Subject 1> seated on the sofa in the lower-left third of frame,
  body angled three-quarters to camera, the off-white envelope from <Subject 6> held in both
  hands at chest height. A few loose strands of her hair shift in the still air, then she
  lowers her chin and looks down at the envelope, then her thumbs slide once along its edge.
  She does not speak; her lips remain closed. The warm floor-lamp light holds steady on her
  cheek; the envelope casts a soft shadow on her coat. The camera pushes in with small
  amplitude at slow speed from a medium shot to a medium close-up. Lighting follows <Subject 5>.
  By the end of the shot she is still looking down, envelope still in both hands, framed
  chest-up. Do not show any text on the envelope.

[Shot 2] At 00:05.000, the camera cuts to a close-up of both hands and the envelope. A tight
  close-up fills the frame with her hands and the off-white envelope, held in the flat
  five-finger pose of <Subject 8>. Her grip tightens slightly, then both hands turn the envelope
  over, then they extend it forward out of the top of frame. She does not speak. The coat
  fabric creases softly at the wrist; a thin shadow falls across the envelope's edge. The
  camera holds a static shot. Lighting follows <Subject 5>. By the end of the shot the envelope
  has left the frame and her hands are still raised, fingers held together. Do not add extra
  fingers or distort the hands.

[Shot 3] At 00:10.500, the shot switches to a medium two-shot. <Subject 1> sits on the left of
  frame looking up, <Subject 4> stands on the right holding the envelope. She blinks once, then
  slowly raises her chin, then her gaze lifts to a fixed point on him and holds there. The
  woman with a quiet, breathy voice (S1) says: [Chinese] "你早就知道了。" He does not answer;
  his lips remain closed. Her hair falls back over her shoulder; the warm key light stays
  steady on both faces. The camera holds a static shot, then pushes in with small amplitude at
  slow speed over the final second. Lighting follows <Subject 5>. By the end of the shot she is
  holding a steady gaze on him and he is looking down at the envelope, both unchanged in
  position. Do not change either character's facial identity.

overall_soundscape:
夜间的安静客厅底噪，纸张摩擦声，信封翻面声，布料摩擦声，她一次缓慢的吸气，
落地灯极轻微的电流声。

non_diegetic_music:
低频弦乐，极慢速度，在第二镜推起、第三镜结束前淡出。
```

**字数校验**：subject_definitions ≈ 150；summary ≈ 90；retention_analysis ≈ 300；detailed_description ≈ 950（三镜）；overall_soundscape ≈ 55；non_diegetic_music ≈ 25。**全套 ≈ 1,570 汉字**，落在 1170–2030 区间 ✅。

---

## 9. 提交前校验清单（11 条）

| # | 校验项 | 不通过则 |
|---|---|---|
| 1 | **未同时出现 `first_frame`/`last_frame` 与 `reference_*`**（字段互斥） | 二选一，重选模式 |
| 2 | 参考文件总数 ≤12；图 ≤9；视频 ≤3（合计 ≤15s）；音频 ≤3（合计 ≤15s 且配有图或视频） | 删参考 |
| 3 | 风格句在 `[Shot 1]` **之前**（1–2 句英文） | 移到前面 |
| 4 | 每个参考文件在 `subject_definitions` **都被点名** | 补 |
| 5 | 每个参考文件在 `retention_analysis` **都有条目** | 补 |
| 6 | **画风/调色参考用的是 `attribute_transfer`，不是 `fully_preserved`** | 改标记 |
| 7 | 时间戳递增、落在时长内；Shot 1 无时间戳 | 改时间戳 |
| 8 | 每镜最短 ≥1.5s（设计取 ≥2s） | 改切分 |
| 9 | 每镜最多 1 句 `Do not ...`，且前面有正向描述 | 删到 1 句 |
| 10 | 有台词处：`(S1)` 跨镜不重编号、`[语言]` 标签存在、台词在英文双引号内、描述在标签外、**一镜一个说话人** | 补标签 |
| 11 | `non_diegetic_music` 非空（无配乐写 `no music`） | 补 |

---

## 10. 已知冲突与注意事项

1. **Ref2VA 无首尾帧** → 若段落含 #7 揭示镜或 #6 同构图匹配镜，见 §1 的拆段方案。
2. **音频参考不能单独输入**【官】，必须配图片或视频。
3. **成本**【官】：2K $0.13/秒（15 秒 ≈ $1.95）；**前 5 张参考图免费，第 6 张起 $0.04/张**；**视频参考按时长计费，是最贵的一项**；**音频参考免费**。量产时优先用图片 + 音频，视频参考只留给"必须复刻某段镜头运动"的场合。
4. **采样步数**：试拍 4 步、出片 6–8 步。人物散架或音画不同步时**先抬步数，不要先改提示词**。
5. **本模板的 `detailed_description` 未使用首尾帧**——三镜衔接依赖构图描述 + 时间戳 + 后期，请在剪辑台预留对齐工时。
