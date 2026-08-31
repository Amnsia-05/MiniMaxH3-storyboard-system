---
name: h3-camera-edit
description: 海螺 H3 视频提示词中「运镜控制 / 剪辑技巧 / 衔接镜头」的写法。含官方运镜术语表、时间戳规则、15秒3镜切分方案、衔接镜类型库、动作延续衔接法、匹配剪辑三锚点。触发词：H3运镜、H3剪辑、H3衔接镜、H3分镜切分、H3时间戳、匹配剪辑、H3长镜头、H3转场。
agent_created: true
---

# H3 运镜 · 剪辑 · 衔接镜

MiniMax 海螺 H3（Hailuo 03）视频提示词中**运镜、剪辑、衔接**三件事的写法规范。

配套 skill：`minimax-h3-storyboard`（小说 → 剧集 → 15 秒 3 镜全流程）。本 skill 是它的**模块三深水区**——当分镜已经拆好、要写运镜句/切镜/段间衔接时，用这一份。

## 0. 使用说明

### 0.1 可信度标注（全文通用）

| 标记 | 含义 |
|---|---|
| 【官方原文】 | 逐字摘自 MiniMax 官方仓库 `MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/base-en.txt` / `ref-en.txt`，或官方 API 文档。**可直接照抄，不要改写** |
| 【官方实测】 | 官方发布或官方引用的实测数据 |
| 【三方实测】 | 第三方发布的实测数据，趋势可信，数值未必精确 |
| 【推断】 | 由已知机制推导，无公开量化基准。可用，但别当硬约束 |
| 【待验证】 | 来源存疑或未实测。**文末给实测方法** |
| 【工艺】 | 从业者经验总结，非官方 |

### 0.2 三条前置硬约束（与运镜/剪辑直接相关）

| 约束 | 值 | 后果 |
|---|---|---|
| 提示词上限 | **7000 字符**（按字符计，1 汉字 = 1 字符）【官方原文 · API】 | 三镜全套 1100–1850 汉字，仅用掉 26%，运镜句不缺预算 |
| 单次时长 | **4–15 秒整数**（API）／本地部署 5–15 秒【官方原文 · API / 模型卡】 | ⚠️ **单独重生成一个 2 秒的衔接镜是不可能的**——最小 4 秒，生成后裁切 |
| 三核心字段顺序 | `integrated_multimodal_description` → `overall_soundscape` → `non_diegetic_music`，**不可调换**【官方原文】 | 运镜句写在 `integrated_multimodal_description` 内 |

### 0.3 一句话速查卡

```text
运镜句：The camera <type> with <small|large> amplitude at <slow|fast> speed <朝向/目标>.
        顺序固定 = 类型 → 幅度 → 速度；中等幅度/正常速度省略不写
        一镜只给 1 个运镜；运镜句写在镜内靠前位置；不要句末堆标签

时间戳：[Shot 1] 无时间戳
        [Shot N] At MM:SS.mmm, the camera cuts to ...（三位小数，严格递增，落在时长内）
        指令首行锚点用 S.SS（两位小数，无 MM: 前缀）——三处格式不同，别混

切镜红线：只改距离或微角度 → 用运镜，不要切镜
          切镜必须引入新信息（主体 / 空间 / 状态 / 视角 / 时间，至少变一项）

15秒3镜：A 入镜（接上段）/ B 主镜（叙事主力）/ C 出镜（接下段）
          硬下限 1.5s｜设计下限 2.0s｜承载信息镜 ≥3.0s｜悬殊比建议 ≤2.5
          A 向后看（匹配上段尾帧），C 向前看（匹配下段首帧）

衔接三宝：动作延续衔接法（动作跨段拆开，衔接镜承载未完成态）
          匹配剪辑三锚点（色彩 / 运动方向 / 构图）
          衔接镜类型库 10 种

硬阻断：跨生成左右方位一致、跨生成 180°轴线/正反打、拉远揭示镜（无尾帧）
        —— 提示词解决不了，改分镜或后期镜像
```

---

## 1. 运镜官方术语表全解

### 1.1 官方表格逐字摘录【官方原文】

| Dimension | Available Expression | Description（官方原文） |
|---|---|---|
| Motion type | `Zoom In / Zoom Out` | The focal length changes while the camera body remains stationary |
| Motion type | `Push In / Pull Out` | The camera moves forward / backward |
| Motion type | `Pan Left / Pan Right` | The camera remains in place while the lens pivots horizontally |
| Motion type | `Truck Left / Truck Right` | The camera translates horizontally |
| Motion type | `Tilt Up / Tilt Down` | The camera remains in place while the lens pivots vertically |
| Motion type | `Pedestal Up / Pedestal Down` | The entire camera moves upward / downward |
| Motion type | `Arc Shot` | The camera moves in an arc around the subject |
| Motion type | `Tracking Shot` | The camera follows a moving subject |
| Motion type | `Static Shot` | The camera position and lens remain still |
| Motion type | `Shake Slightly / Shake Strongly` | Slight / strong camera shake |
| Motion type | `POV` | The subject's point of view |
| Motion type | `Roll Clockwise / Roll Counterclockwise` | The camera rolls clockwise / counterclockwise around the lens axis |
| Amplitude | `with small amplitude` / `with large amplitude` | Small-range / large-range change |
| Speed | `at slow speed` / `at fast speed` | Slow / fast movement |

**官方语句法**【官方原文】：

> "Camera motion should be written as a natural English action within the shot, rather than stacked as separate labels at the end of a sentence."

**官方例句**【官方原文】：

```text
The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.
The camera pans right with large amplitude at fast speed, revealing the open doorway.
The camera holds a static shot as the runner exits the frame.
```

### 1.2 逐条全解（例句 / 场景 / 误用）

---

#### ① `Zoom In` / `Zoom Out` 变焦

- **官方释义**：焦距变化，机身不动（The focal length changes while the camera body remains stationary）
- **中文**：拧镜头变焦，透视关系**不变**，背景压缩感变化
- **例句**：
  ```text
  The camera zooms in with small amplitude at slow speed, tightening from a medium shot to a
  close-up of her face while the background compression increases slightly.
  ```
  中文：镜头小幅慢速变焦推近，从中景收紧到她的脸部特写，背景压缩感略微增强。
- **适用场景**：需要"看出去更近"但不改变透视；模拟监控/新闻素材质感；配合 Static Shot 做低成本的"准推镜"
- **常见误用**：把它当 `Push In` 用。二者视觉差异明显——`Zoom In` 背景与人物的相对大小**不变**，`Push In` 会"穿过"空间。**H3 上 `Zoom` 更容易触发背景畸变**（透视被强行拉伸），推近优先用 `Push In`

---

#### ② `Push In` / `Pull Out` 深度位移

- **官方释义**：摄像机前移 / 后退（The camera moves forward / backward）
- **中文**：真推真拉，透视改变，人物与背景产生相对位移
- **例句**：
  ```text
  The camera pushes in with small amplitude at slow speed from a medium close-up to a close-up
  of her hands folded on the desk.
  ```
  中文：镜头小幅慢速推近，从中近景推到她交叠在桌上的双手特写。
- **适用场景**：**15 秒段落里最好用的一档**。情绪加压（`Push In`）、段落收尾与信息揭示（`Pull Out`）；也是"小幅取景变化"的首选——官方说这种情况**不要切镜，用运镜**
- **常见误用**：
  - 幅度写 `large` 又写 `slow`：长距离慢推是累计漂移重灾区，末帧构图常失控
  - `Pull Out` 拉到全身却不给尾帧：见 §10 硬阻断「拉远揭示镜」

---

#### ③ `Pan Left` / `Pan Right` 摇摄

- **官方释义**：机身不动，镜头水平转（The camera remains in place while the lens pivots horizontally）
- **中文**：原地摇，视点不动、朝向变
- **例句**：
  ```text
  The camera pans right with large amplitude at fast speed, revealing the open doorway at the
  far end of the corridor.
  ```
  中文：镜头大幅快速右摇，揭示走廊尽头敞开的门。
- **适用场景**：同一空间内的视线引导、揭示画外信息；**运动方向锚点**最好用的一类（方向直观、模型不易搞反）
- **常见误用**：`large amplitude` + 有纹理的背景（书架、砖墙、百叶窗）→ 横向纹理蠕动/闪烁。**大摇必须配简背景**：`simple background, minimal environment, soft bokeh`

---

#### ④ `Truck Left` / `Truck Right` 横移

- **官方释义**：摄像机水平横移（The camera translates horizontally）
- **中文**：整机平移，产生视差（前景与背景相对滑动）
- **例句**：
  ```text
  The camera trucks right with large amplitude at slow speed along the corridor, passing two
  closed doorways before the lit doorway at the far end comes into view.
  ```
  中文：镜头大幅慢速沿走廊右移，掠过两扇关着的门，尽头亮着灯的门进入视野。
- **适用场景**：展示空间纵深、跟随侧移的人物、超长运镜（见 §9）
- **常见误用**：与 `Pan` 混用导致**跨段方向对不上**。若上段写 `pan right`、下段写 `truck right`，模型走出的速度与幅度不同，接缝必顿（见 §8 运动方向锚点）

---

#### ⑤ `Tilt Up` / `Tilt Down` 俯仰摇

- **官方释义**：机身不动，镜头垂直转（The camera remains in place while the lens pivots vertically）
- **中文**：原地上下摇
- **例句**：
  ```text
  The camera tilts up with small amplitude at slow speed from his shoes to his face, holding on
  his eyes for the last second.
  ```
  中文：镜头小幅慢速上摇，从他的鞋摇到他的脸，最后一秒停在眼睛上。
- **适用场景**：人物出场（脚 → 头）、建筑/高大物体、从细节拉回整体
- **常见误用**：`Tilt Up` 到完整人脸属"揭示"，若在短镜内摇过全身，**中段身体比例畸变**概率明显上升。要么缩短摇的范围，要么改硬切两镜

---

#### ⑥ `Pedestal Up` / `Pedestal Down` 升降

- **官方释义**：整机升降（The entire camera moves upward / downward）
- **中文**：整机上下平移，视点变、朝向不变
- **例句**：
  ```text
  The camera pedestals down with small amplitude at slow speed from eye level to the tabletop,
  settling on the overturned cup.
  ```
  中文：镜头小幅慢速下降，从视平线降到桌面高度，停在翻倒的杯子上。
- **适用场景**：从站立降到桌面/地面道具、从桌面升到人物；场景建立的开头与结尾
- **常见误用**：与 `Tilt` 混用。`Pedestal down` 到桌面时，桌沿与背景的相对关系会滑动（视差），`Tilt down` 不会。**跨段衔接时两者不能互换**

---

#### ⑦ `Arc Shot` 环绕

- **官方释义**：绕主体弧线运动（The camera moves in an arc around the subject）
- **中文**：绕着主体转
- **例句**：
  ```text
  The camera arcs slowly around her with small amplitude at slow speed, travelling from her
  left profile to a three-quarter view, the background sliding smoothly behind her.
  ```
  中文：镜头小幅慢速绕她弧线运动，从她的左侧面转到四分之三侧，背景在她身后平滑滑过。
- **适用场景**：情绪高点、人物定格、展示角色与环境的空间关系
- **常见误用**：`large amplitude` 环绕 = **崩坏率最高的一档**。绕过大角度时模型要连续重建人物背面/侧面，脸与服装最容易漂；且背景滑过整个 360° 必然出现纹理闪烁。**环绕幅度一律压到 small，时长 ≤6 秒**（见 §9.3）

---

#### ⑧ `Tracking Shot` 跟拍

- **官方释义**：跟拍移动主体（The camera follows a moving subject）
- **中文**：镜头跟着走动的主体移动
- **例句**：
  ```text
  The camera tracks her with small amplitude at slow speed as she walks along the corridor,
  keeping her centred in frame at a constant distance.
  ```
  中文：她沿走廊行走时，镜头小幅慢速跟拍，以恒定距离把她保持在画面中央。
- **适用场景**：行走、奔跑、车辆移动；交代"从 A 到 B"的空间转移
- **常见误用**：主体 + 背景双重漂移。跟拍时背景持续流过，是纹理闪烁与背景畸变的高发区。**跟拍必须配简背景**，且时长 ≤6 秒（见 §9.3）

---

#### ⑨ `Static Shot` 固定

- **官方释义**：机位与镜头都不动（The camera position and lens remain still）
- **中文**：完全不动
- **例句**：
  ```text
  The camera holds a static shot as the runner exits the frame.
  ```
  中文：镜头保持固定，跑步者走出画面。
- **适用场景**：**衔接镜的默认选择**。A 入镜与 C 出镜大多是 1.5–3 秒的短镜，短镜内做运镜既看不出效果又增加崩坏面；固定机位可占满 15 秒不漂移
- **常见误用**：把 `Static Shot` 写成 "no camera movement" 这类否定句。官方给的是**正向术语** `holds a static shot`，直接用它

---

#### ⑩ `Shake Slightly` / `Shake Strongly` 抖动

- **官方释义**：轻微 / 强烈抖动（Slight / strong camera shake）
- **中文**：手持感 / 剧烈晃动
- **例句**：
  ```text
  The camera shakes slightly throughout the shot, a handheld tremor holding the same small
  amplitude from start to finish, the frame otherwise holding the same framing.
  ```
  中文：镜头全程轻微抖动，手持震颤幅度从头到尾不变，画面其他方面保持同一构图。
- **适用场景**：手持纪实感、紧张、打斗、爆炸余波
- **常见误用**：抖动与另一运镜叠加（"推镜 + 抖动"）→ 抖动会被平均成整体漂移，画面糊。要用抖动就**单独用**，并加"幅度不增大"的约束

---

#### ⑪ `POV` 主观视角

- **官方释义**：主体视角（The subject's point of view）
- **中文**：第一人称视角
- **例句**：
  ```text
  The camera holds her POV with small amplitude at slow speed as the door handle turns and the
  door swings inward.
  ```
  中文：镜头小幅慢速保持她的主观视角，门把手转动，门向内打开。
- **适用场景**：代入、惊吓、信息揭示（"她看见了什么"）；也是 §6 类型库 #4 眼神反应镜的标准下一段
- **常见误用**：POV 里出现主体自己的脸/身体。写 POV 时**画面内不得出现该主体**，前景可以有手/门框，但脸不许入画

---

#### ⑫ `Roll Clockwise` / `Roll Counterclockwise` 滚转

- **官方释义**：绕镜头轴滚转（The camera rolls clockwise / counterclockwise around the lens axis）
- **中文**：地平线旋转（荷兰角的动态版）
- **例句**：
  ```text
  The camera rolls clockwise with small amplitude at slow speed, the horizon tilting no more
  than ten degrees and stopping there, the rotation held well short of a full turn.
  ```
  中文：镜头小幅慢速顺时针滚转，地平线倾斜不超过十度即停住，远未转满一圈。
- **适用场景**：失衡、醉酒、眩晕、现实崩塌的瞬间
- **常见误用**：不给角度上限 → 模型可能转成整圈，画面彻底失控。**必须写死幅度上限**（`no more than ten degrees`）

---

### 1.3 方括号运镜 token（⚠️【待验证】）

部分资料提到 H3 支持 15 个方括号运镜指令：

```text
[Truck left] [Truck right] [Pan left] [Pan right] [Push in] [Pull out] [Pedestal up]
[Pedestal down] [Tilt up] [Tilt down] [Zoom in] [Zoom out] [Shake] [Tracking shot] [Static shot]
```

并称"同一括号内最多 3 个 = 同时执行；写在提示词不同位置 = 顺序执行"。

> ⚠️ **【待验证】** 这套 token **未出现在 H3 官方 `base-en.txt` / `ref-en.txt` 中**，疑似来自海螺 02 或第三方转述。官方明确给出的是**自然英文动作句**（§1.1 的 12 条术语 + 例句）。
>
> **处置**：默认用**官方自然语句式**。方括号 token 仅在自然语句式失效时做 A/B 测试，不要作为主力写法。
>
> **实测方法**：同一段描述写两版（自然句 vs 方括号 token），同种子各生成 3 条，对比运镜是否执行、方向是否一致、是否出现画面漂移。若方括号版无优势，弃用。

---

## 2. 运镜三参数的搭配规则与决策表

### 2.1 官方搭配规则【官方原文】

**顺序 = motion type → amplitude → speed**

> "Add amplitude and speed only when they are meaningful; medium amplitude and normal speed are usually omitted."

**完整句式**：

```text
The camera <motion type> with <amplitude> at <speed> <方向 / 起点→终点 / 目标>.
```

| 段 | 内容 | 可选值 | 是否可省 |
|---|---|---|---|
| 1 运动类型 | motion type | §1.1 的 12 类 | **不可省**（不写运镜等于让模型自由发挥） |
| 2 幅度 | amplitude | `with small amplitude` / `with large amplitude` | **可省**，中等幅度省略 |
| 3 速度 | speed | `at slow speed` / `at fast speed` | **可省**，正常速度省略 |
| 4 方向/目标 | 起点 → 终点 或 朝向 | 自然语言 | 建议写，**不写则运镜无落点** |

### 2.2 什么时候该写、什么时候该省

| 情况 | 写法 | 例子 |
|---|---|---|
| 想让它慢、想让它小 | **写** `with small amplitude at slow speed` | 情绪推近、衔接镜内的微调 |
| 想让它快、想让它大 | **写** `with large amplitude at fast speed` | 揭示、转场、紧张段落 |
| 中等幅度 + 正常速度 | **全省**，只写类型 | `The camera pushes in toward the letter.` |
| 只有一档有意义（如只想要慢，幅度无所谓） | **只写那一档** | `The camera trucks right at slow speed along the corridor.` |

> **为什么"只写一档"合法**：官方的省略规则是"没有意义就不写"，不是"要写就两档都写"。只写 `at slow speed` 是常见且合规的写法。

### 2.3 幅度 / 速度选择决策表

| 叙事目的 | 推荐类型 | 幅度 | 速度 | 建议时长 | 备注 |
|---|---|---|---|---|---|
| 情绪加压、聚焦内心 | `Push In` | `small` | `slow` | 3–8s | 最稳的一档，首选 |
| 信息揭示、交代环境 | `Pull Out` | `small` | `slow` | 3–6s | 拉到全身需尾帧（见 §10） |
| 段落开场建立空间 | `Pedestal Down` 或 `Truck Right` | `large` | `slow` | 4–6s | 配简背景 |
| 视线引导、揭示画外 | `Pan Left/Right` | `small` | `slow` | 2–4s | 大幅需简背景 |
| 人物出场（脚→头） | `Tilt Up` | `small` | `slow` | 3–5s | 跨全身比例易畸变 |
| 高潮定格、空间关系 | `Arc Shot` | **`small`** | `slow` | ≤6s | 大幅环绕崩坏率最高 |
| 行走转移 | `Tracking Shot` | `small` | `slow` | ≤6s | 主体 + 背景双重漂移 |
| 衔接镜（A/C） | **`Static Shot`** | — | — | 1.5–3s | 短镜内运镜看不出效果 |
| 紧张、打斗、纪实 | `Shake Slightly` | — | — | 2–5s | 单独用，不与运镜叠加 |
| 代入、惊吓 | `POV` | `small` | `slow` | 2–4s | 主体不得入画 |
| 失衡、眩晕 | `Roll Clockwise/CCW` | `small` | `slow` | 1.5–3s | 必须写死角度上限 |
| 转场、快速揭示 | `Pan` / `Truck` | `large` | `fast` | 1.5–3s | 短促大幅，配简背景 |

### 2.4 组合写法（两个运镜同时执行）

官方未禁止组合，官方例句里就有两个运镜并行的写法：

```text
The camera pulls out with large amplitude at slow speed while pedestaling upward with small
amplitude at slow speed.
```
中文：镜头大幅慢速拉远，同时小幅慢速升高。

**组合规则**【推断，与官方例句一致】：

| 规则 | 说明 |
|---|---|
| 上限 | **一镜最多 2 个运镜**。3 个以上必被平均成漂移（见 §3.2） |
| 句法 | 用 `while` 连接，第二个运镜**重复完整三参数结构**（`... while pedestaling upward with small amplitude at slow speed`），不要简写成 `while pedestaling up` |
| 主次 | 第一个是主运镜，第二个是修饰。把主要信息放在第一个 |
| 配套 | 组合运镜建议配一句稳定器（见 §3.4） |

---

## 3. 一镜一运镜原则

### 3.1 官方与工艺两条口径

- **官方口径**【官方原文】：运镜要写成"镜内的自然英文动作"，不是句末堆标签；幅度/速度只在有意义时加
- **工艺口径**【工艺】：**一镜只给一个主运镜**；模块三分镜表的「运镜」字段也写死"单镜最多 2 个组合运镜"

### 3.2 运镜堆叠为什么会变成漂移

**机制**【推断】：视频模型把运镜指令当作一个**条件分布**参与采样。多个运镜指令同时出现时，模型不会"依次执行"，而是取各指令在潜空间方向的**加权平均**——三个不同方向的运动平均之后，得到的既不是环绕也不是推近，而是一个没有明确方向的缓慢位移。

**可观察的失效形态**：

| 输入 | 常见输出 |
|---|---|
| `arc shot` + `push in` + `pedestal up` | 画面缓慢斜向漂，主体偏离构图中心，背景纹理呼吸 |
| `push in` + `zoom in` | 透视与焦距互相打架，人物面部出现"膨胀—收缩"的呼吸感 |
| `tracking shot` + `shake slightly` | 抖动被平均成整体模糊，主体边缘发糊 |
| 三个以上运镜 | 末帧构图与描述完全不相关 |

### 3.3 硬规则

| # | 规则 | 违反后果 |
|---|---|---|
| 1 | 一镜只给 **1 个主运镜**，最多 2 个（用 `while` 连接） | 3+ 平均成漂移 |
| 2 | 运镜**写成句子**，写在镜内，不写在提示词末尾统一声明 | 官方明确要求"不要句末堆标签" |
| 3 | 否定句限制运镜时，**每镜最多 1 句 `Do not ...`**，且前面必须先有正向描述 | 纯否定会让模型无所适从 |
| 4 | 不用运镜时也要**明说** `The camera holds a static shot.` | 不写 = 模型自由发挥，可能自己动 |

### 3.4 运镜句前置（位置纪律）

**原理**【工艺，多来源一致】：模型对**靠前** token 的权重更高。把运镜埋在长描述中段，它第一个丢的就是运镜。

**写法规则**：

| 位置 | 放什么 |
|---|---|
| 镜内最前 | 景别 + 主体 + 构图（①段） |
| **紧随其后（②段前）或紧跟①段** | **运镜句** |
| 中段 | 时序动作节拍、对白 |
| 末尾 | 收尾状态 `By the end of the shot ...` + 最多一句 `Do not ...` |

**推荐句位**（两种都对，二选一并全片统一）：

```text
【A：运镜紧跟构图】
A medium close-up frames her at the right third of frame. The camera pushes in with small
amplitude at slow speed toward her face. First her gaze drops to the letter...

【B：运镜写进构图句】
A medium close-up frames her at the right third of frame, and the camera pushes in with small
amplitude at slow speed as she ...
```

> ⚠️ 与模块六「六段结构」（①构图 ②动作 ③对白 ④环境 ⑤运镜 ⑥光影 ⑦收尾）**不矛盾**：模块六的 ⑤ 是**中文详版**的填写顺序（给人看、给 AI 转译用）；转译成 H3 官方格式时，把运镜句**提到靠前**。转译不是翻译，是换结构。

### 3.5 运镜稳定器句式（可直接复制）【工艺】

官方未给出"稳定器"，以下是从业者实测有效的附加约束句。**挑一句**加在运镜句之后即可，**不要全加**——四句内容有重叠，全加会稀释主体描述。

```text
【通用】Locked-off camera on a tripod, a single continuous camera move at a constant speed from
start to finish, the speed held even, the motion smooth, exposure held steady throughout.

【末帧稳定】The camera settles and holds completely still for the final second, ending on a
stable held frame, the framing held fixed.

【方向连续性】The camera moves continuously from left to right in one unbroken move, holding the
same speed and the same direction from the first frame to the last.

【纵深推拉】A single slow push-in at a constant rate, the camera body level and fixed in place,
the subject staying centred in frame throughout.
```

> ❌ **旧版七个 `no` 串成一排**（`no acceleration, no deceleration, no direction reversal, no camera shake, no jitter, no stutter, no frame flicker`），属**成串**违规。逐个看这些都是 **B 类**（物理/时间属性，见 §11.1 A8b），**违规的是"成串"，不是"用了 no"**。这是【工艺】时代传下来的写法，实测"有效"很可能来自**同时写进去的正向部分**（`constant speed`、`single continuous move`）。

---

## 4. 剪辑规范

### 4.1 时间戳三处格式（翻车高发区）

**三处格式不同，混用是最常见错误。**

| # | 位置 | 格式 | 位数 | 官方原文 |
|---|---|---|---|---|
| 1 | **`[Shot 1]`** | **不加时间戳** | — | "Do not add a timestamp to the first shot." |
| 2 | **后续镜头** `[Shot N]` | `At MM:SS.mmm, ...` | **三位小数**，带 `MM:` 前缀 | "begin each one with a strictly increasing cut time that falls within the video duration" |
| 3 | **指令首行锚点**（I2VA/FL2VA/L2VA） | `S.SS` | **两位小数，无 `MM:` 前缀** | "`S.SS` is the effective video duration formatted to exactly two decimal places" |

**正确示例**：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the
0.00-second mark of the target video; Picture 2 (from Shot 3) aligns with the 15.00-second mark
of the target video.

integrated_multimodal_description:
[Shot 1] Live-action, cinematic, a medium shot frames her beside the dark wooden desk ...
[Shot 2] At 00:05.000, the camera cuts to a close-up of the letter in her hands ...
[Shot 3] At 00:11.500, the shot transitions to a large close-up of her face ...
```

**易混点速查**：

| 错误写法 | 正确写法 | 原因 |
|---|---|---|
| `[Shot 1] At 00:00.000, ...` | `[Shot 1] ...` | 首镜永远不加时间戳 |
| `[Shot 2] At 00:05.00, ...` | `[Shot 2] At 00:05.000, ...` | 后续镜三位小数 |
| `... aligns with the 15.000-second mark` | `... aligns with the 15.00-second mark` | 指令首行两位小数 |
| `[Shot 3] At 00:16.000, ...`（15 秒视频） | 改到 `00:11.500` | 必须"落在视频时长内" |
| `[Shot 3] At 00:05.000`（与 Shot 2 相同） | 改到 `00:09.000` | 必须"严格递增" |

### 4.2 切换动词【官方原文】

**默认硬切**，用以下五种之一：

```text
the camera cuts to ...
the shot cuts to ...
the shot transitions to ...
the shot changes to ...
the shot switches to ...
```

**软转场**（`cross-dissolve` / `fade` / `wipe`）——**只在用户明确要求时使用**，否则默认硬切：

```text
[Shot 2] At 00:05.000, the shot cross-dissolves to a close-up of the same letter, ten years later.
[Shot 3] At 00:11.000, the shot fades to a wide view of the empty room.
```

> ⚠️ 软转场在 AI 生成上**额外不稳定**：叠化要求模型在两帧之间做半透明混合，容易出现"重影脸"。**AI 漫剧默认全部硬切**，软转场交给后期剪辑软件做。

### 4.3 核心红线：切镜必须引入新信息【官方原文】

> "A cut should introduce new information about the subject, space, state, viewpoint, or time. If only the distance or a slight angle needs to change, prefer camera motion."

**五个"新"——至少变一项**：

| 维度 | 含义 | 例子 |
|---|---|---|
| **subject** 主体 | 画面里的主角/对象换了 | 她的脸 → 她手里的信 |
| **space** 空间 | 换了地方，或揭示了新的空间关系 | 书房中景 → 走廊全景 |
| **state** 状态 | 同一主体的状态变了 | 站着的她 → 坐下的她 |
| **viewpoint** 视角 | 观察角度/视点变了 | 客观中景 → 她的 POV |
| **time** 时间 | 时间跳跃 | 白天 → 夜晚；现在 → 十年前 |

**判定流程**：

```
问：这个切镜引入了「主体/空间/状态/视角/时间」里的一项新信息吗？
├─ 是 → 可以切
└─ 否 → 只是想换个距离或微调角度
        └─ 改用运镜：Push In / Pull Out / Pan / Tilt
```

**正例 / 反例**：

```text
✅ 可以切（新主体 + 新空间）
[Shot 1] ... a medium shot frames her standing by the desk ...
[Shot 2] At 00:05.000, the camera cuts to a large close-up of the wedding ring on the desk ...

❌ 不该切（只是想更近一点）
[Shot 1] ... a medium shot frames her standing by the desk ...
[Shot 2] At 00:05.000, the camera cuts to a close-up of her standing by the desk ...

✅ 改为运镜
[Shot 1] ... a medium shot frames her standing by the desk, and the camera pushes in with small
amplitude at slow speed to a close-up of her face ...
```

中文对照（❌ 那例）：第 1 镜中景拍她站在书桌旁，第 2 镜还是中景里站着的她——只是近了点，**不该切**，改推镜。

> **为什么这条红线在 AI 上特别重要**：切镜 = 模型重新采样一次。每多一次采样，就多一次身份漂移、光照跳变、服装错乱的机会。能用一个推镜解决的，绝不要切成两个镜头。

### 4.4 切点密度与镜数预算

| 项 | 值 | 性质 | 来源 |
|---|---|---|---|
| 切点密度 | **约每 3 秒一切**（"Budget roughly one cut per 3 seconds"） | 建议 | 【官方实测】 |
| 镜数代价 | "More shots = more chances for visual inconsistency between cuts" | 官方提示 | 【官方原文】 |
| 15 秒建议镜数 | **2–4 镜** | 建议 | 【推断】 |
| 13–15 秒 | 2–4 镜 | 建议 | 【推断】 |
| 9–12 秒 | 2–3 镜 | 建议 | 【推断】 |
| 6–8 秒 | 1–2 镜 | 建议 | 【推断】 |
| 4–5 秒 | 1 镜 | 建议 | 【推断】 |

> ⭐ **15 秒 3 镜正好落在 H3 官方支持的单请求多镜区间内**，且切点密度（每 5 秒一切）接近官方建议的每 3 秒一切。

### 4.5 时间戳精度【三方实测】

| 项 | 值 |
|---|---|
| 切点落点误差 | **±0.12 秒**（*"In our testing the cuts landed within 0.12 seconds of the mark, while the same brief written as plain prose held a single framing for all 15 seconds."*） |
| 性质 | **软引导**，不是硬约束 |
| 总时长 | 由请求参数固定，**不受误差影响** |
| 误差是否跨段累积 | **否**（切点偏移只在段内重新分配） |

> **剪辑冗余按「每段 0.2 秒」留即可，不按段数累加。** 10 段仍留 0.2 秒，不是 2 秒。
> 反例（错误）：10 段 × 0.2 = 2 秒冗余 → 过度预留，浪费时长。

> ⚠️ **不要在提示词里指定精确帧数或 FPS**——时机由模型控制。分镜表的时间码是**规划值**，不进提示词。

### 4.6 跨剪辑连续对白 / 结尾截断【官方原文】

> "When the same line of dialogue or lyrics crosses a cut, use `<scenetrans>` at the connecting points in both parts and explicitly state that the audio continues across the cut. Use `<cutoff>` when speech is truncated by the end of the video."

| 场景 | 标记 | 配用措辞 |
|---|---|---|
| 一句台词跨两个镜头 | `<scenetrans>` | `continues seamlessly across the cut` / `continues uninterrupted into the next shot` / `carries over from the previous shot` / `remains audible across the transition` |
| 视频结尾时话没说完 | `<cutoff>` | — |

```text
[Shot 1] ... and says: <d>[Chinese] 我从来没想过<scenetrans></d>
[Shot 2] At 00:05.000, ... her sentence continues seamlessly across the cut, <d>[Chinese]<scenetrans> 你会回来。</d>
```

---

## 5. 15 秒 3 镜切分

### 5.1 A / B / C 三镜的正确分工

**不要把 3 个镜头理解成「1 个主镜 + 2 个陪衬」。** 三个镜头功能完全不同：

| | 名称 | 时长 | 职责 | 设计要点 |
|---|---|---|---|---|
| **A** | **入镜**（接上段） | 1.5–2.5s | 确立时空、承接情绪、给出"入口" | 延续上一段的色调与光源方向 |
| **B** | **主镜** | 10.5–12s | 叙事主力，承载本段唯一信息点或情绪转折 | 全段资源集中在这里 |
| **C** | **出镜**（接下段） | 1.5–2.5s | 卡点、留白、交棒 | 是下一段的"预告片" |

**A 和 C 不能套同一个模板**：

- **A 向后看** —— 它的构图和色调要**匹配上一段的尾帧**
- **C 向前看** —— 它的构图和动作方向要**匹配下一段的首帧**
- 两者方向相反，提示词写法自然不同

**A / C 的写法选择规则**：

| 情境 | 选哪种 | 理由 |
|---|---|---|
| 承接人物情绪（哭完、说完狠话、被扇完） | **生成法**：动作压缩在前 1.5–2s，后段留余韵，后期裁切 | 需要人物反应，空镜接不住情绪 |
| 纯时空转场（换场景、换时间） | **空镜法**：空镜 / 道具特写 | 无人物全身，裁到 1–2s 几乎无损 |
| 危险动作（打斗、坠落、肢体冲突） | **空镜法** 优先 | 短镜头最容易崩手崩脸，能避则避 |
| 手机屏 / 短信内容转场 | **道具特写** | 屏幕内容靠后期合成更稳 |

> **判断口诀：有人脸 → 生成法；无人脸 → 空镜法。**

### 5.2 时间分配：先定衔接类型，再定秒数

**不要一刀切规定"衔接镜就是 2 秒"。** 正确顺序：**先决定这个衔接镜要干什么，再决定它该多长。**

| 衔接镜要承担的任务 | 建议时长 | 理由 | 类型库 |
|---|---|---|---|
| **动作延续**（承接/交出一个未完成的动作） | **2–3s** | 只需建立"中间态"，不需要动作走完 | 见 §7 |
| 空镜 / 环境氛围过渡 | **2–3s** | 无动作，只需色调与光位对齐 | #1 |
| 道具 / 手机屏特写 | **2–3s** | 静态为主，微动即可 | #3 |
| 眼神 / 面部反应镜 | **2–3s** | 一次眨眼、一次转头就够 | #4 |
| 局部 → 整体揭示 | **4–5s** | 需要走完一段拉镜 | #7 |
| **超长运镜衔接**（⚠️ 高难度） | **4–5s** | 需要完整走完一段运镜 | 见 §9 |

> **规律：任务越"轻"，衔接镜越短。** 只需"摆出一个状态"的，2–3 秒够；需要"走完一段运动"的，4–5 秒起步。

### 5.3 时长校验规则（可直接写成公式）

> ✅ **更正**：先前一度认为「各镜必须均衡、不支持 11/2/2」——**这是错的**。官方**没有**"均衡"这条约束，真实约束是**每镜最短时长**。

| 项 | 数值 | 性质 | 来源 / 官方原文 |
|---|---|---|---|
| **单镜硬下限** | **1.5s** | **硬约束** | "Shorter than 1.5s doesn't give the model enough frames"【官方原文】 |
| 建议区间 | **2–5s** | 建议 | 【官方实测】多来源一致 |
| **承载信息镜** | **≥3s** | 建议 | "each shot needs at least 3 seconds to establish anything meaningful"【官方原文】 |
| **设计下限** | **2.0s** | 建议 | 【推断】不要用硬下限做设计值 |
| **悬殊上限** | **最长镜 ≤ 最短镜 × 2.5** | 建议 | 【推断】由 2–5s 推荐区间导出 |
| 切点密度 | 约每 3s 一切 | 建议 | 【官方实测】 |
| 镜数代价 | 镜越多，跨镜不一致风险越高 | 官方提示 | 【官方原文】 |

```text
① 硬下限：  每镜 ≥ 1.5s          （低于即不可生成，直接报错）
② 设计下限：每镜 ≥ 2.0s          （日常建议，留安全余量，告警）
③ 信息下限：承载信息镜 ≥ 3.0s    （要交代东西的镜头才适用，告警）
④ 悬殊上限：最长镜 ≤ 最短镜 × 2.5（超过则告警，考虑拆请求）
⑤ 求和：    A + B + C = 15.0s    （必须精确，取 0.5s 网格）
```

### 5.4 五套时间分配范式

| 范式 | A 入镜 | B 主镜 | C 出镜 | 适用场景 | 悬殊比 |
|---|---|---|---|---|---|
| **均衡**（默认推荐） | 5.0s | 5.0s | 5.0s | 官方最稳，重生成代价最小 | 1.0 |
| **主优** | 4.5s | 6.0s | 4.5s | 主镜需多承载一点 | 1.33 |
| **快切** | 4.0s | 7.0s | 4.0s | 对话密集、爽点段 | 1.75 |
| **重尾** | 4.0s | 6.5s | 4.5s | 集尾卡点段，C 需留白 | 1.63 |
| **主镜优先** | 2.0s | 11.0s | 2.0s | 严格贴合"短衔接镜"规格 | **5.5** ⚠️ |

**硬约束**：时长取 **0.5s 网格**；三者之和 **= 15.0s**；每镜 ≥ 1.5s（硬）、建议 ≥ 2.0s；承载信息镜 ≥ 3.0s；悬殊比建议 ≤ 2.5。

**切分方案判定表**：

| 切分 | 判定 | 说明 |
|---|---|---|
| 5 / 5 / 5 | ✅ 安全 | 最均衡，跨镜一致性最好 |
| 4.5 / 6 / 4.5 | ✅ 安全 | 推荐档，主镜保留优势 |
| 3 / 9 / 3 | ✅ 合法（悬殊比 3.0） | 超出 2.5 建议值，需评估 |
| **2 / 11 / 2** | ✅ **合法**（满足硬下限） | 悬殊比 5.5；两个 2s 镜低于"承载信息"的 3s 线，只适合当纯衔接镜 |

**五套范式怎么选**：

| 情况 | 选哪套 | 理由 |
|---|---|---|
| 常规段落，无特殊要求 | **均衡 5/5/5** 或 **主优 4.5/6/4.5** | 重生成代价最小，量产最稳 |
| 衔接镜只是"摆一个状态"（动作延续 / 空镜 / 道具特写） | **主镜优先 2/11/2** | 衔接镜任务轻，2 秒够用；崩了走 T2 单镜重生成 |
| 衔接镜需要"走完一段运动"（超长运镜 / 局部揭示） | **主优 4.5/6/4.5** | 这类任务 2 秒不够，必须给到 4 秒以上 |
| 量产阶段、要控制成本 | 悬殊比 ≤2.5 的任一档 | 避免重生成连坐 |
| 试验阶段、单次出片 | 可放宽到主镜优先 | 崩了大不了整条重来 |

> **口诀：衔接镜任务轻 → 可以短；任务重 → 必须长；量产 → 悬殊比压在 2.5 以内。**

### 5.5 悬殊切分的真实代价：重生成连坐

既然 11/2/2 合法，为什么仍建议均衡？**真正的问题出在重生成环节**：

> 单次请求出三镜时，**若第 2 镜崩了，重生成会把第 1、3 镜一起重新采样**——可能修好一个、弄坏两个。**在量产阶段这是成本事故。**

**三级降级梯**：

| 级别 | 做法 | 适用 | 依赖 |
|---|---|---|---|
| **T1** | 单次请求出多镜（2–4 镜），时间戳切分 | 首次生成，**默认起点** | — |
| **T2** | 单镜重生成，用 **FL2VA 首尾帧**钳住两侧 | 三镜中 ≤2 镜不合格 | **完全依赖 FL2VA** |
| **T3** | 全拆成独立请求，FL2VA 串联 | T2 反复失败、或需精确控制 | — |

> ⚠️ **T2 是这套降级梯的关键**，它完全依赖 FL2VA 可用。若某天 FL2VA 不可用，降级梯就只剩 T1 ↔ T3 两极，成本会显著上升。

**T2 的操作要点**：

```
失败镜首帧 = 前镜尾帧（截帧）；失败镜尾帧 = 后镜首帧（截帧）；用 FL2VA 钳死两端，中间交给模型插值
```

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the
0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 4.00-second mark
of the target video.

integrated_multimodal_description:
[Shot 1] ...（该镜完整提示词，自成一体）...
```

> ⚠️ **API 时长下限是 4 秒**：重生成一个"2 秒的衔接镜"时，**必须请求 4 秒再裁切**，不能请求 2 秒。

**T1 的前置要求（否则降级梯失效）**：

> T1 生成时，**每一镜的提示词必须自成一体**——完整写出角色、服装、环境、光线、画风，不得依赖"共享上下文"省略。一旦走 T2，该镜要被单独抽出重生成，缺字段会直接崩。**禁止为省 token 让后两镜依赖前文。**

### 5.6 FL2VA 默认单镜【官方原文】

> "FL2VA generally favors a single shot so the model can interpolate continuously from the first frame to the last frame. Use multiple shots only when they are explicitly specified. The last frame must be reached by the final `[Shot N]` at the end of the video."

**含义**：用首尾帧模式（FL2VA）时，**默认写成单镜**。要写多镜必须显式指定（即写清楚时间戳与切镜）。

**FL2VA 推荐叙事结构**【官方原文】：

```text
first-frame state → observable intermediate changes → progressively narrowing differences → last-frame state
首帧状态 → 可观察的中间变化 → 逐步收窄的差异 → 尾帧状态
```

**对衔接镜的直接应用**：A 入镜与 C 出镜大多是"承接/交出一个中间状态"，天然是单镜 + 首尾帧的场景——**A 入镜的首帧 = 上一段尾帧，C 出镜的尾帧 = 下一段首帧**。这正是动作延续衔接法（§7）的实现基础。

---

## 6. 衔接镜类型库 10 种

> 评级口径：`单次请求内` = 三镜放同一次生成（T1 默认）；`跨请求` = 三镜独立生成（T3）。
> 风险码：`H`手部 `B`肢体 `M`运镜 `I`身份 `T`文字 `P`物理 `A`小物件 `X`跨镜一致性 `V`语音。
> 本表为**技术侧评级定稿**（`衔接镜类型库_12列风险表单.md`），与主模板模块三 3.5 冲突时以本表为准。

### 6.1 主表

| # | 类型 | 适用情境 | 景别 | 运镜 | 与前后段对齐方式 | 风险码 | 单次请求内 | 跨请求 | 处置 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 空镜 / 环境氛围镜 | 段落首、时空切换 | 远景 / 全景 | 缓推或固定 | 延续前段色调与光源方向；下段主镜从此处"推入" | `M` | 低 | 低 | 后置 |
| 2 | 手部特写 | 握拳、捏衣角、倒酒 | 大特写 | 微推 | **动作顺接**：上段起势 → 本镜完成 → 下段接续 | `H` | **高** | **高** | **规避** |
| 3 | 道具特写 | 信、戒指、手机屏、刀 | 大特写 | 固定 / 微环绕 | **图形匹配**：手机屏内容 = 下段信息载体 | `T`+`A` | 中高 | **高** | **降级** |
| 4 | 眼神 / 面部反应镜 | 情绪转折 | **中近景** | 极缓推 | **视线匹配**：视线保持平视，不做方向变化 | `I`+`B` | 中高 | 中高 | **规避** |
| 5 | 遮挡黑场 | 段落尾、时间跳跃 | 中景 / 特写 | 横移穿过遮挡物 | 遮挡物从左入 → 全黑 → 下段从右出，**运动方向连续** | `P`+`X` | 低中 | 低中 | 后置 |
| 6 | 同构图匹配镜 | 时空转换、蒙太奇 | 与前后主镜同景别 | 同向推 / 摇 / 环绕 | 复用同一构图描述串，或直接给同一张构图参考图 | `X` | **中** | 中 | 后置 |
| 7 | 局部 → 整体揭示镜 | 升级、震惊、身份曝光 | 脚 / 背影 / 局部 → 全景 | 缓拉 | 拉镜终点构图 = 下段主镜起点构图 | `B` | **中** | 中高 | 后置 |
| 8 | 过肩 / 前景虚化镜 | 对话、偷听、偷拍 | 中近景，前景 **≤1/4** | 轻微手持感 | 正反打遵循 **180° 轴线 / 30° 原则** | `P`+`X` | **中** | **高** | **规避** |
| 9 | 声音先导镜 | 转折前 | 任意 | 固定 | 本镜画面 = 下段声音源（门铃响 → 切门） | — | 低 | 低 | 无 |
| 10 | 时间流逝镜 | 省略、转场 | 空镜（**无表盘 / 无数字**） | 固定 | 用明度 / 色温渐变桥接上下段 | `T` | 中（含表盘数字 → **高**） | 中 | **降级** |
| **11** | **正反打**（补充） | 双人对白、对峙、试探 | 中近景双人交替 | 固定或微推 | 180° 轴线；A 看画左 → B 看画右 | `X`+`B` | **中** | **硬阻断** | **规避** |

**风险排序（高→低）**：手部特写(签字) → 正反打(跨请求) / 手机屏小字 / 戒指 → 眼神大特写 → 揭示镜 / 过肩 / 时间流逝镜 / 同构图匹配镜 → 遮挡黑场 → 空镜 / 声音先导。

### 6.2 逐型写法（含可直接复制的例句）

---

#### #1 空镜 / 环境氛围镜　风险：低 / 低

- **适用**：段落首、时空切换、情绪留白
- **景别**：远景 / 全景　**运镜**：缓推或固定
- **对齐方式**：延续前段色调与光源方向；下段主镜从此处"推入"
- **写法要点**：背景元素越少越好
- **英文例句**：
  ```text
  [Shot 1] A wide shot frames the empty corridor at dawn, dust drifting through a single shaft
  of warm light from the left. Simple background, minimal environment, soft bokeh. The camera
  pushes in with small amplitude at slow speed toward the far doorway.
  ```
  中文：全景拍黎明的空走廊，尘埃在左侧一道暖光里飘浮。背景简洁、环境最少、柔和虚化。镜头小幅慢速向尽头的门推近。
- **备选方案**：背景压到最少（`simple background, minimal environment, soft bokeh`）；缓推若背景蠕动 → 改固定机位 + 后期缓缩放

---

#### #2 手部特写　风险：**高 / 高**

- **适用**：握拳、捏衣角、倒酒（**签字 / 持笔 / 插钥匙 → 直接换动作**）
- **景别**：大特写　**运镜**：微推
- **对齐方式**：**动作顺接**：上段起势 → 本镜完成 → 下段接续
- **手势风险排序**：握拳（中）＜ 捏衣角（高）＜ **签字 / 持笔（极高）**
- **三档降级**：握拳（可留）／捏衣角 → 改"手掌平覆布料，掌心向下，五指并拢"／**签字·持笔·插钥匙 → 直接换动作**（合上文件、盖印章、放下笔）
- **兜底写法**：手占画面 ≥1/2
- **英文例句（握拳，可留）**：
  ```text
  [Shot 2] At 00:05.000, the camera cuts to a large close-up of a closed fist resting on the
  dark wooden table, all five fingers curled inward into the palm, the knuckles forming one even
  row, the thumb folded across the front, shot from the wrist up, hand fully in frame, natural
  finger proportions. The camera holds a static shot.
  ```
  中文：第 2 镜在 5.000 秒切到搁在深色木桌上的握拳大特写，五根手指向内收拢进掌心，指节排成整齐一列，拇指扣在前面，从手腕以上取景，手完整入画，手指比例自然。镜头保持固定。
- **英文例句（捏衣角 → 降级为平覆）**：
  ```text
  ... her hand rests flat against the fabric, palm down, fingers together.
  ```
  中文：她的手平覆在布料上，掌心向下，五指并拢。

---

#### #3 道具特写　风险：中高 / **高**

- **适用**：信、戒指、手机屏、刀
- **景别**：大特写　**运镜**：固定 / 微环绕
- **对齐方式**：**图形匹配**：手机屏内容 = 下段信息载体
- **写法要点**：
  - **手机屏 → 只出冷白光映脸，内容后期贴**（小字是 8-bit 量化的第一受害者，未实测前不赌）
  - 戒指 / 刀 / 信件 → 走参考图，**并在提示词中对该参考图标注 `fully_preserved`**
- **英文例句（手机屏，降级写法）**：
  ```text
  [Shot 2] At 00:05.000, the shot cuts to a close-up of her face from the chest up, the phone
  held just below frame; the screen casts cold white light onto her face, the screen showing only
  a uniform dark surface.
  ```
  中文：切到她胸部以上的脸部特写，手机握在画面下缘之外；屏幕在她脸上投下冷白光，屏幕只呈现一片均匀的暗色表面。
- **英文例句（戒指，参考图锚定）**：
  ```text
  ... the same ring, staying on the same finger unchanged in size, shape and position for the
  entire shot.
  ```
  中文：同一枚戒指，全程在同一根手指上，大小、形状、位置完全不变。

---

#### #4 眼神 / 面部反应镜　风险：中高 / 中高

- **适用**：情绪转折、反转瞬间
- **景别**：**中近景**（不是大特写）　**运镜**：极缓推
- **对齐方式**：**视线匹配**：视线保持平视，不做方向变化；人物看向画外 → 下镜即其所见
- **写法要点**：
  - **不写眼神方向变化**（"抬眼看向画外"是高风险指令）
  - **大特写不承载情绪转折表演**——情绪转折放中近景，大特写只做静态凝视
- **英文例句**：
  ```text
  [Shot 3] At 00:11.500, the shot transitions to a medium close-up of her face, gaze held level,
  one slow blink, both eyes open and symmetrical, pupils centred and equal size, steady gaze,
  no eye movement. The camera pushes in with small amplitude at slow speed.
  ```
  中文：切到她的中近景，视线保持平视，缓慢眨眼一次，双眼睁开且对称，瞳孔居中且等大，凝视稳定，眼球不转动。镜头小幅慢速推近。

---

#### #5 遮挡黑场　风险：低中 / 低中

- **适用**：段落尾、时间跳跃、跨时空硬接
- **景别**：中景 / 特写　**运镜**：横移穿过遮挡物
- **对齐方式**：遮挡物从左入 → 全黑 → 下段从右出，**运动方向连续**
- **写法要点**：
  - 遮挡物用**纯色 / 剪影平面**，禁用带纹理物体（横移时必闪）
  - **不要指望模型给出真正全黑帧**——生成时留冗余，剪辑时挑最暗的 0.3–0.5s 用
- **英文例句**：
  ```text
  [Shot 3] At 00:12.000, a solid dark silhouette sweeps across the frame from left to right,
  fully covering the lens, flat black, the surface reading as one even unbroken field, clean
  straight edge. The camera holds a static shot as the frame goes fully dark.
  ```
  中文：一个纯暗剪影从左向右扫过画面，完全遮住镜头，纯黑、表面是一整片均匀无断裂的暗场、边缘干净平直。画面全黑时镜头保持固定。

---

#### #6 同构图匹配镜　风险：**中 / 中**

- **适用**：时空转换、蒙太奇
- **景别**：与前后主镜同景别　**运镜**：同向推 / 摇 / 环绕
- **对齐方式**：上下段主体在画面同一位置、同向运动
- **写法要点**：**FL2VA 可用** —— 上下镜共用同一张构图参考图作首帧 / 尾帧，或复用同一构图描述串
- **必填备选方案**：同构图不保证同主体位置
- **英文例句**：
  ```text
  [Shot 2] At 00:05.000, the shot changes to the same composition, same framing, same subject
  position in frame, same lighting direction — the same woman seated at the right third of frame,
  now in a different room, a decade later.
  ```
  中文：切到完全相同的构图、相同的取景、主体在画面中的相同位置、相同的光照方向——同一个女人坐在画面右三分之一处，但换了房间，十年之后。
- **⚠️ 为什么不给"低风险"**：即便在单次请求内共享上下文，"同构图"仍要求模型在两个不同场景里复现**同一构图与主体位置**——身份/风格共享了，但**构图不共享**。且官方明确提醒 "More shots = more chances for visual inconsistency between cuts"。**备选方案照填。**

---

#### #7 局部 → 整体揭示镜　风险：**中 / 中高**（原硬阻断，FL2VA 解禁）

- **适用**：升级、震惊、身份曝光
- **景别**：脚 / 背影 / 局部 → 全景　**运镜**：缓拉
- **对齐方式**：拉镜终点构图 = 下段主镜起点构图
- **解禁条件（双重，缺一不可）**：
  - **首帧给局部构图图、尾帧给全景构图图**（两图须先渲出，属"首尾帧构图图"资产）
  - **拉远段 ≤3 秒** **且** **≤该镜时长的 50%**（真正决定插值难度的是相对比例，不是绝对值：3s 在 5s 镜里占 60%，在 12s 镜里只占 25%）
  - **高 stakes 揭示（身份曝光、关键反转）仍走硬切**，不赌单次插值
- **失效模式**：从"终点崩"变为"**中段畸变**"——模型在已知两端之间插值，但**插值路径不受控**，中段仍可能出现身体比例畸变【推断，H3 上无公开实测数据】
- **英文例句**：
  ```text
  [Shot 2] At 00:05.000, the camera begins a single continuous pull-out at a constant rate,
  starting from the polished black shoes and rising to a full wide shot of the man standing in
  the doorway; the subject's body remains fully visible and proportionally correct throughout
  the move.
  ```
  中文：第 2 镜开始一次恒定速率的连续拉远，从锃亮的黑皮鞋起幅，升到那个男人站在门口的完整全景；整个运动过程中主体的身体始终完整可见且比例正确。

---

#### #8 过肩 / 前景虚化镜　风险：**中 / 高**

- **适用**：对话、偷听、偷拍
- **景别**：中近景，前景 **≤1/4**（1/3 时粘连概率明显上升）　**运镜**：轻微手持感
- **对齐方式**：正反打遵循 **180° 轴线 / 30° 原则**
- **写法要点**：前景压到 1/4 以下并做成**纯暗剪影**，与主体边缘干净分离
- **英文例句**：
  ```text
  [Shot 2] At 00:05.000, the camera cuts to a medium close-up of her, a dark out-of-focus
  silhouette occupying the left quarter of frame, reading as one solid unbroken shape, clean
  edge separation from the subject. The camera shakes slightly, a handheld tremor holding its
  small amplitude.
  ```
  中文：切到她的中近景，一个暗色虚化剪影占据画面左侧四分之一，呈一整块实心无断裂的形状，与主体边缘干净分离。镜头轻微抖动，是手持的轻微震颤且幅度不增大。

---

#### #9 声音先导镜　风险：低 / 低

- **适用**：转折前（J-cut 的画面侧）
- **景别**：任意　**运镜**：固定
- **对齐方式**：本镜画面 = 下段声音源（门铃响 → 切门）
- **说明**：纯剪辑层 J-cut / L-cut，**无生成风险**
- **英文例句**：
  ```text
  [Shot 3] At 00:12.000, the shot switches to a close-up of the doorbell button, and a single
  chime rings out; the chime continues uninterrupted into the next shot.
  ```

---

#### #10 时间流逝镜　风险：中（含表盘数字 → **高**）

- **适用**：省略、转场
- **景别**：空镜（**无表盘 / 无数字**）　**运镜**：固定
- **对齐方式**：用明度 / 色温渐变桥接上下段
- **写法要点**：**砍掉一切可读时间信息**（"时钟指向 3 点"属文字类崩坏，与招牌乱码同源）；降级为抽象时间感；粒子类加"密度恒定、无闪烁"
- **英文例句**：
  ```text
  [Shot 3] At 00:12.000, the shot cuts to a wide shot of the window, the light gradually
  shifting from warm amber to cool blue, the shadows lengthening across the floor. The walls and
  the floor are plain, unmarked surfaces showing only colour, material and the slow change of
  the light. The dust drifts at a constant density, evenly spread, its brightness held steady.
  Do not draw any letters, numbers, logos or captions anywhere in frame.
  ```
  中文：切到窗户的全景，光线逐渐从暖琥珀色转为冷蓝色，影子在地板上拉长。墙面与地板是素净无标记的表面，只呈现颜色、材质与光线的缓慢变化。尘埃以恒定密度飘浮、分布均匀、亮度保持稳定。画面内任何位置都不要画出字母、数字、标志或字幕。

> ❌ **禁用写法**：`no visible clock face, no numbers, no text` 这类**成串裸名词否定**，按主模板 §6.4-F 是 ❌ **禁用**：名词进条件分布，会**反向激活**。上面例句用**正向锚定 + 末尾 1 句 `Do not` 收边**，即主模板判定的 **H3 最优档**。粒子类同理：`no flicker` 改正向 `its brightness held steady`。

---

#### #11 正反打（补充）　风险：**中（单次请求内） / 硬阻断（跨请求）**

- **适用**：双人对白、对峙、试探——**短剧里占比最高的场景类型**
- **景别**：中近景双人交替　**运镜**：固定或微推
- **对齐方式**：180° 轴线；A 看画左 → B 看画右；两条交替出现
- **实现方式与评级**：

| 实现方式 | 评级 | 说明 |
|---|---|---|
| 单人过肩同框，不切 | 中 | 共享上下文，最稳 |
| **单次请求内用时间戳切两镜** | **中** | 180° 轴线自动成立，**推荐** |
| 跨请求分两次生成 | **硬阻断** | 提示词保不住轴线，只能后期水平镜像 |

- **约束**：**一镜一个说话人**（*"If two people need to talk, cut between them"*），两人对话必须切镜，不可在同一镜内让两人先后说话
- **对话段推荐范式**：**4 镜 4.0 / 3.5 / 4.0 / 3.5**（A 说 / B 说 / A 说 / 反应），每镜 ≥3s、切点 ≈3.5s 贴合密度建议
- **英文例句（单次请求内两镜）**：
  ```text
  [Shot 2] At 00:04.000, the camera cuts to a medium close-up of the man on the left, looking
  frame right, and he says: <d>[Chinese] 你早就知道了。</d>
  [Shot 3] At 00:07.500, the shot cuts to a medium close-up of the woman on the right, looking
  frame left, and she says: <d>[Chinese] 是。</d>
  ```
  中文：切到画面左侧男人的中近景，他朝画面右方看，说"你早就知道了。"／切到画面右侧女人的中近景，她朝画面左方看，说"是。"
- **⚠️ 分镜表须写死此约束**：否则分镜师会反复用提示词去对齐朝向与左右位置，是纯浪费。

---

## 7. 动作延续衔接法（实战核心）

> 这是使用者在实战中总结的模式，本节把它规范化。**这是所有衔接手法里最有效、也最应该优先使用的一档。**

### 7.1 原理

一个完整动作**跨段落拆开执行**，衔接镜承载的是**动作的未完成态**：

```text
上一段 C 出镜           本段 A 入镜             本段 B 主镜
"站起一半"      ────→   从"站起一半"接上  ────→   完成站起，迈步
（动作中断）            （承接中间态）            （动作完成）
```

**为什么这么做有效**：

| # | 理由 |
|---|---|
| 1 | **天然掩盖剪辑点** —— 观众的注意力跟着动作走，不会注意到切镜 |
| 2 | **符合 H3 的能力边界** —— 长动作容易崩（尤其站起、转身这类重心转移），拆成两段后每段都短，崩坏率大幅下降 |
| 3 | **衔接镜有了实质内容** —— 它不是空转的过渡，而是动作链的一环，观众感知为"连续"而非"切了" |

### 7.2 三段写法模板

#### ① 上一段的 C 出镜（交出未完成动作）

```text
② 她双手撑住扶手，然后重心前移、身体抬起约三分之一，然后停在这个半起的姿势。
⑦ By the end of the shot she is held mid-rise, knees bent at roughly 120 degrees,
   torso leaning forward, the motion deliberately unfinished.
```

**关键点**：**明确写"动作未完成"**（`deliberately unfinished` / `held mid-rise`），并给出**具体的中间姿态**（膝盖角度、身体倾角），让下一段能精确接上。

#### ② 本段的 A 入镜（承接中间态）

```text
① A medium shot frames her already mid-rise, knees bent at roughly 120 degrees,
   torso leaning forward — resuming exactly the pose held at the end of the previous shot.
② She continues straightening her legs, then rises fully to standing, then settles her weight.
```

**关键点**：用 `already mid-rise` / `resuming exactly the pose` 声明**这是延续而非新动作**，并把上一段 C 出镜的姿态参数**原样抄过来**。

#### ③ 本段的 C 出镜（交出下一个未完成动作）

```text
⑦ By the end of the shot she has begun to turn toward the door, her shoulders rotated
   about 45 degrees, the turn deliberately unfinished.
```

### 7.3 可直接复制的英文句式库

| 用途 | 英文句式 | 中文 |
|---|---|---|
| 声明延续 | `already mid-rise, ... — resuming exactly the pose held at the end of the previous shot` | 已经处于半起状态……精确承接上一段尾镜所保持的姿态 |
| 声明延续（通用） | `continuing the motion from the previous shot without restarting it` | 延续上一段的运动，不重新开始 |
| 交出未完成 | `the motion deliberately unfinished` | 动作刻意未完成 |
| 交出未完成（通用） | `held at the midpoint of the movement, the motion still in progress` | 停在动作的中点，运动仍在进行中 |
| 姿态量化 | `knees bent at roughly 120 degrees` | 膝盖弯曲约 120 度 |
| 姿态量化 | `shoulders rotated about 45 degrees` | 肩膀旋转约 45 度 |
| 姿态量化 | `her hand raised to shoulder height, palm open` | 手抬到肩高，掌心张开 |
| 姿态量化 | `the door open by a hand's width` | 门开了一掌宽 |
| 时间顺序 | `First ... then ... then ...` | 首先……然后……然后……（**禁用 "同时"**） |
| 禁止重来 | `Do not repeat the reaching motion from the previous shot.` | 不要重复上一段的伸手动作 |

### 7.4 可延续的动作清单

| 动作 | 拆分方式 | 崩坏风险 | 姿态参数建议 |
|---|---|---|---|
| 站起 / 坐下 | 半起 → 完全站起 | 中（重心转移） | `knees bent at roughly 120 degrees` |
| 转身 | 转 45° → 转完 | 低 | `shoulders rotated about 45 degrees` |
| 伸手取物 | 手伸出一半 → 触到并拿起 | 中（手部） | `arm extended halfway, fingertips 20 cm from the letter` |
| 抬头 / 低头 | 抬到一半 → 抬到位 | 低 | `chin lifted halfway, gaze at the middle of the door` |
| 迈步 | 抬脚 → 落地 | 中 | `right foot lifted, knee at 90 degrees` |
| 开门 | 门开一线 → 门全开 | 中 | `the door open by a hand's width` |
| 穿衣 / 脱外套 | 穿上一袖 → 穿好 | **高**（布料） | ⚠️ **不推荐**，布料是结构性缺陷 |

> **优先用前四行**（站起/坐下、转身、伸手、抬头低头）——风险低且姿态好量化。布料类（穿衣/脱外套）风险高，能避则避。

### 7.5 三条铁律

| # | 铁律 | 说明 | 反例 |
|---|---|---|---|
| **1** | **姿态参数必须可量化和复述** | 写「膝盖约 120 度」，不写「半蹲着」。下一段要能**逐字抄回这个数字** | ❌ `half-crouching`　✅ `knees bent at roughly 120 degrees` |
| **2** | **衔接动作只用简单、单向、慢速的** | 复杂动作（跳跃、快速转身、布料大幅飘动）在短镜头里崩坏率极高 | ❌ `she spins around quickly`　✅ `she rotates her shoulders about 45 degrees at a steady pace` |
| **3** | **上下两段用同一套姿态参数** | 这是 §8「构图锚点」在动作维度的延伸。参数一旦改，衔接就断了 | 上段写 120 度、下段写 135 度 → 接缝必跳 |

### 7.6 完整段落示例（含三镜提示词）

**段落设定**：`E01-S03《她决定起身》`，与上一段衔接：动作延续（上一段 C 出镜停在"半起"）；与下一段衔接：动作延续（本段 C 出镜停在"转身 45°"）。

**分镜表**：

| 镜 | 时间码 | 时长 | 景别 | 运镜 | 生成方式 | 风险 | 备选方案 |
|---|---|---|---|---|---|---|---|
| A 入镜 | 00:00–00:02 | 2.0s | 中景 | `Static Shot` | FL2VA | 中 | 改空镜：书桌上的信 |
| B 主镜 | 00:02–00:12 | 10.0s | 中近景 → 近景 | `Push In` small/slow | T2VA | 高 | 拆成两镜各 5s |
| C 出镜 | 00:12–00:15 | 3.0s | 特写（眼） | `Static Shot` | FL2VA | 低 | 改手部特写 |

**校验**：2 + 10 + 3 = 15.0s ✅　台词 12 字 ≤ 47 ✅　每镜有备选 ✅
**悬殊比**：10 ÷ 2 = 5.0（超出建议值 2.5）——衔接镜任务轻（摆状态），可接受；崩了走 T2 单镜重生成。

**A 入镜（FL2VA，2s）**：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the
0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 2.00-second mark
of the target video.

integrated_multimodal_description:
[Shot 1] Live-action, cinematic, 35mm lens. A medium shot frames the same 28-year-old woman
already mid-rise beside the dark wooden desk, knees bent at roughly 120 degrees, torso leaning
forward, both palms flat on the desk surface — resuming exactly the pose held at the end of the
previous shot. First her shoulders settle, then she continues straightening her legs, then she
rises fully to standing. Her coat falls back into place, the desk lamp's warm pool of light
widens across the papers as she gains height. The camera holds a static shot. Lighting matches
the lock block exactly. By the end of the shot she stands fully upright, hands at her sides,
framed from the waist up. Do not repeat the reaching motion from the previous shot.

overall_soundscape: Coat fabric shifting, one slow breath released, the faint creak of floorboards under shifting weight.

non_diegetic_music: N/A
```

**C 出镜（FL2VA，3s）**：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the
0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 3.00-second mark
of the target video.

integrated_multimodal_description:
[Shot 1] Live-action, cinematic. A large close-up frames her face centred in frame, her gaze
still lowered to the letter. First she blinks once, then her jaw tightens and her eyebrows draw
together, then her chin lifts and her gaze rises to a fixed point beyond the lens. Her hair
falls back over her left shoulder; the warm key light holds steady on her cheek. The camera
holds a static shot. By the end of the shot she has begun to turn toward the door, her shoulders
rotated about 45 degrees, the turn deliberately unfinished. Do not change her facial identity.

overall_soundscape: A single sharp intake of breath, paper crumpling slightly in her grip.

non_diegetic_music: The sustained cello note cuts cleanly on the final beat.
```

**下一段 A 入镜该怎么写**（接力 45° 转身）：

```text
[Shot 1] A medium shot frames her already mid-turn toward the door, shoulders rotated about
45 degrees — resuming exactly the pose held at the end of the previous shot. First her hips
follow her shoulders, then she completes the turn to face the door, then she takes one step
forward. The camera trucks right with small amplitude at slow speed.
```

---

## 8. 匹配剪辑三锚点

【业界】匹配剪辑分三类：图形匹配、动作匹配、声音匹配。

| 类型 | AI 可行度 | 原因 | 提示词写法要点 |
|---|---|---|---|
| **图形匹配** | **高** | 可用首尾帧（I2VA / FL2VA）锁定形状、颜色、位置 | 两段复用同一构图描述串，例如「圆形主体居中占画面 1/3，右侧暖色边缘光」；或直接给同一张构图参考图 |
| **动作匹配** | **中** | 方向可控，**速度与幅度不可精确控制** | 只写「慢速、单一、单向」动作 |
| **声音匹配** | **高**（属后期） | 与生成无关，剪辑阶段做 J-cut / L-cut | 上段尾部音效提前 0.3s 入，或延续至下段 |

### 8.1 三锚点【推断】

| 锚点 | 含义 | 怎么写 |
|---|---|---|
| **① 色彩锚点** | 上下段复用**同一光位**常量串 | 从场景卡「光照」组取五行（方向/色温/光质/暗部落向/收边），两段逐字复用 |
| **② 运动方向锚点** | 上段出口方向 = 下段入口方向，**严禁反向** | 两段用**同一个运镜 token**，方向句写在该镜开头 |
| **③ 构图锚点** | 末帧主体位置 ≈ 首帧主体位置 | 两段复用同一构图描述串，或用 FL2VA 把上段尾帧当下段首帧 |

### 8.2 色彩锚点

**取值来源**：场景卡的「光照」组五行（主光方向 / 色温 / 光质 / 暗部落向 / 收边）。**上下段要衔接，光源方向就不能乱变。**
→ 光位串的**设定**归 `h3-env-scene`；本节只管**跨段怎么转录**。

**写法**：把光位描述串做成**常量块**，两段逐字复用。

```text
【光位常量块 · 全剧逐字复用】
A single soft key light from the upper front left at 45°, warm amber, holding steady on her
cheek, the shadow side falling to the lower right. The rest of the frame falls into shadow,
every surface there reading as one even unbroken field.
```

**日景版**（整体照明、无强暗部的场景，末句换成）：`All the light in the room comes from this one source.`

**跨段转录**：上段 C 出镜与下段 A 入镜**逐字复用上面这一整串**。

**五段拆解**（场景卡「光照」组五行 → 转录进提示词的顺序）：

| 段 | 英文写法 | 中文 |
|---|---|---|
| 主光方向 | `from the upper front left at 45°` | 自左前上方 45° |
| 色温 | `warm amber` | 暖琥珀色 |
| 光质 | `soft` / `hard` / `diffused by cloud` | 柔和 / 硬光 / 云层漫射 |
| 暗部落向 | `the shadow side falling to the lower right` | 暗部落在右下方 |
| 收边 | `The rest of the frame falls into shadow, every surface there reading as one even unbroken field.` | 画面其余落入暗部，表面均匀无断裂 |

> **三条写法纪律** ① **方向词用画面方位，绝不用角色左右**（`on her left` 有歧义，是翻转翻车的常见根因）——用 `upper front left` / `camera left`。② **收边句用正向、且不含 `no detail`**：`No other light source...` 是完整否定句，⚠️ **弱**且吃掉每镜唯一一句 `Do not` 的配额；`detail` 是 A 类（见 §11.1 A8b）。③ **K 值不进提示词**：`3200K` / `5600K` 只作团队沟通语言，提示词用文字（`warm amber` / `cool white` / `neutral daylight`），响应度【待验证】。完整规则见 `h3-env-scene` §1.6 / §4.3.1。

> **⚠️ 跨段对齐用 `same` 复述**：下段写 `the same warm key light...`，**不要**写 `Do not change the light direction.` —— 三锚点全是正向写法，**天然不占 `Do not` 配额**。

> **为什么是硬要求**：**主光换边，身份就会晃**。光照方向全程保持单一主光。

### 8.3 运动方向锚点（四条硬规则）

| # | 规则 | 反例 |
|---|---|---|
| **1** | **两段必须用同一个运镜 token**。上段末用 `truck right`，下段首也必须是 `truck right` | ❌ 一段 `pan right`、一段 `move rightward`、一段 `camera drifts right` —— 会走出不同速度与幅度，是"粗匹配也匹配不上"的**主因** |
| **2** | **方向句写在该镜描述的开头**，不要埋在场景描述之后 | ❌ `...the corridor stretches behind her, and the camera moves right.` |
| **3** | **给两段一个共同物理参照物** | 见下方例句 |
| **4** | **严禁反向**。上段向右收尾，下段就必须从向右开始 | ❌ 上段 `truck right` 收尾、下段 `truck left` 开场 |

**共同物理参照物写法**：

```text
【上段 C 出镜收尾】
... the camera continues right until a dark wooden door panel fills the entire frame.

【下段 A 入镜开场】
The shot opens on the same dark wooden door panel filling the frame, then the camera continues
moving right past it.
```

中文对照：镜头继续右移，直到一扇深色木门板充满画面。／镜头从同一扇充满画面的门板开始，继续向右移过它。

**方向连续性完整例句**：

```text
[Shot 1] ... The camera trucks right with large amplitude at slow speed along the corridor.
[Shot 2] At 00:05.000, the camera continues the same truck right with large amplitude at slow
speed, now passing the second doorway.
[Shot 3] At 00:10.000, the same truck right decelerates and settles on the lit doorway at the
far end.
```

中文：镜头沿走廊大幅慢速右移。／第 2 镜继续**同一个**大幅慢速右移，掠过第二道门。／**同一个**右移减速，停在尽头亮着灯的门口。

> `continues the same truck right` 这句是灵魂——它告诉模型这是**同一个运动的延续**，不是新镜头。

### 8.4 构图锚点

**写法**：两段复用同一构图描述串，或用 FL2VA 把上段尾帧当下段首帧。

```text
【上段 C 出镜末帧描述】
By the end of the shot she is framed at the right third of frame, her shoulder occupying the
right edge, the dark doorway filling the left two thirds.

【下段 A 入镜首帧描述】
A medium shot frames her at the right third of frame, her shoulder occupying the right edge, the
dark doorway filling the left two thirds.
```

**更可靠的做法**：**用 FL2VA 直接把上段尾帧作为下段首帧**，比描述串对齐更可靠。

> 🟢 **锚点工程的作用范围已大幅缩小**：段内三镜由模型共享上下文自动维持，**三锚点只在「段与段之间」（跨请求）才需要人工写**。三锚点从"每三段做一次"降为"每 15 秒做一次"，工作量约降为 1/3。

### 8.5 粗匹配原则

> ⚠️ **不要追求像素级匹配。** AI 生成是概率性的，匹配做到"**形状 / 色彩 / 方向**"级别即可。**追求像素级必然返工。**

| 维度 | 追求到什么程度 | 不追求什么 |
|---|---|---|
| 色彩 | 同一光位方向、同一色温档位 | 精确 RGB 值、完全一致的曝光 |
| 运动方向 | 同一运镜 token、同一方向 | 精确速度、精确幅度 |
| 构图 | 主体在画面的同一分区（左 1/3 / 居中 / 右 1/3） | 精确到像素的主体位置 |
| 姿态 | 同一个量化参数（120 度 / 45 度） | 精确到度的关节角度 |

---

## 9. 超长运镜与长镜头

> 所有衔接里最难的一档。

### 9.1 为什么难

| 难点 | 原因 |
|---|---|
| **运镜参数跨请求无法精确对齐** | 速度、幅度、方向在两次生成中会有偏差，接起来必然"顿一下" |
| **长镜头本身是崩坏重灾区** | 生成时间越长，累计漂移越大，末帧构图可能与描述相去甚远 |
| **单次生成有 15 秒上限** | 超长运镜装不进一条请求，必须拆 |
| **末帧不可控** | 除非用 L2VA 锁尾帧，否则长运镜的终点是随机的 |

### 9.2 四条策略（按优先级）

#### 策略一（首选）：塞进单条请求，不跨请求

长运镜最忌讳拆。如果总时长 ≤15 秒，**一定要放在同一条请求里**，用多镜时间戳切成 2–3 段，让模型共享上下文。

```text
[Shot 1] The camera begins a slow truck right along the corridor with large amplitude at slow
speed, passing the first doorway ...
[Shot 2] At 00:05.000, the camera continues the same truck right with large amplitude at slow
speed, now passing the second doorway ...
[Shot 3] At 00:10.000, the same truck right decelerates and settles on the lit doorway at the
far end.
```

**关键**：**三镜用同一个运镜术语 + 同一个方向 + 同一个速度描述，逐字复用**。

#### 策略二：拆段 + 共同物理参照物

必须跨请求时，给两段一个**共同的具体物体**作为接缝（写法见 §8.3）。

#### 策略三：统一运镜三参数

| 参数 | 要求 |
|---|---|
| 运动类型 | 上下段**必须用同一个 token**（都用 `truck right`，不要一段 `pan right` 一段 `move rightward`） |
| 方向 | **严禁反向**。上段向右收尾，下段就必须从向右开始 |
| 幅度 / 速度 | **逐字复用** `with large amplitude at slow speed`，不要一段写一段不写 |

#### 策略四（兜底）：用遮挡黑场回避

实在接不上，就用**遮挡物横移穿过**制造黑场（类型库 #5），避开硬接。**不要试图通过调提示词把两段硬凑——那是在跟概率较劲。**

### 9.3 各运镜类型的时长上限建议

| 镜头类型 | 建议单次生成时长 | 说明 |
|---|---|---|
| 缓推 / 缓拉（`Push In` / `Pull Out`） | **≤ 8s** | 超过后末帧构图漂移明显 |
| 横移 / 升降（`Truck` / `Pedestal`） | **≤ 6s** | 位移越大，累计漂移越大 |
| 环绕（`Arc Shot`） | **≤ 6s** | 角度累计误差最明显 |
| 跟拍（`Tracking Shot`） | **≤ 6s** | 主体 + 背景双重漂移 |
| 摇摄（`Pan` / `Tilt`） | **≤ 5s** | 大幅摇摄配简背景可适当延长 |
| 固定机位（`Static Shot`） | **≤ 15s** | 无运镜，可占满 |

> ⚠️ **上表全为【推断】**，基于"生成时长越长累计漂移越大"这一通用规律，**无公开量化基准**。实测方法见 §11.4 第 2 项。

### 9.4 长镜头的配套写法

```text
【匀速约束】
... at a constant rate from start to finish, the speed held even and unchanging throughout.

【末帧锁定】
... and the camera settles and holds completely still for the final second, ending on a stable
held frame with no drift.

【背景简化（长运镜必加）】
... simple background, minimal environment, soft bokeh, plain surfaces and smooth gradients
throughout.
```

> **❌ 旧版已弃用**：`no acceleration, no deceleration`（**成串**违规）、`no repeating fine patterns`（**A 类**，写了等于先让模型构想出图案）。分级见 §11.1 A8b；末帧锁定的 `no drift` 是 B 类单个，**可留**。⚠️ `h3-env-scene` §9.9 曾逐字收录含 `no` 的旧版，**以本节正向版为准**。

> **背景简化为什么必加**：长运镜里背景持续流过整个画面，任何细密重复图案（砖墙、百叶窗、书架、栅栏）都会产生**摩尔纹与闪烁**——这是长运镜最常见的失效形态。

**含重复图案的场景怎么换**：见 `h3-env-scene` §9.9 对照表（走廊→窄巷、病房→客厅、地下车库→江边码头、会议室→老宅书房、雨夜街道→雪地），**这边不复制**。即便同请求生成，走廊顶灯序列照样闪——**换场景比改提示词有效**。

### 9.5 硬阻断提醒

长运镜**一旦跨请求**，§10 的「跨生成左右方位一致」与「180° 轴线」两项**重新进入风险区**——出路见 §10.1。

---

## 10. 硬阻断项

> 遇到这几类，**第一反应应该是改分镜，不是改提示词**——答案是绕开，不是写好。

| 问题 | 为什么解决不了 | 唯一可行方案 |
|---|---|---|
| **跨生成的左右方位一致** | 每次生成为独立采样，无空间状态传递 | 后期水平镜像翻转 |
| **跨生成的 180° 轴线 / 正反打朝向** | 同上 | **同一次请求内完成正反打**，或后期镜像 |
| **拉远揭示镜**（无尾帧时） | 身体会凭空生成 | 改剪辑：局部镜 → 硬切 → 全景镜；或用 FL2VA 给尾帧（此时降为中风险，见 #7） |
| **屏幕 / 招牌 / 字幕文字正确** | 模型把文字当像素图案，无字形结构规则 | 干净底板 + 后期贴图 |
| **小物件纯文本复现**（耳环 / 纹身） | 像素占比低，无持续状态跟踪 | 必须走参考图（I2VA / Ref2VA） |
| **物理接触 / 碰撞 / 液体 / 布料** | 结构性缺陷 | 改写剧本避开，或实拍 / 3D |
| **小尺度精确对准**（钥匙插锁、指尖对位） | 无 3D 朝向跟踪与刚体约束 | 避开极端特写 + 多条挑选 |
| **手机正反面翻转** | 已知高发 | 参考图锚定 + 多条挑选 + 后期 |

> 把"钥匙插进锁孔"改成"手已经握在门把上"，一秒钟解决问题；硬写提示词，十次也过不了。

### 10.1 正反打：为什么"单次请求内"就解禁

同一次请求的多镜**共享上下文**，模型自动维持方位与 180° 轴线；两次独立请求之间**无状态传递**。

**跨请求时的三条出路**：① **合并进同一次请求**（首选，评级降为「中」）；② **用 FL2VA 把上段尾帧作为下段首帧**；③ **后期水平镜像翻转**。

### 10.2 最容易误判的一条：采样步数（NFE）伪翻车

> 很多看起来像"运镜写错了"的问题，其实是**采样步数太低**。
> 官方口径：*"人物动作散架或音画对不上时，第一件该怀疑的是步数太低，不是 prompt 写错。"*
> 步数档位（试拍 4 步 / 出片 6–8 步）与完整处置见 `h3-antibug-check`，这里只留运镜侧的排查顺序。

**运镜出问题时的排查顺序**：

```
1. 先加步数到 6–8 步重跑一次（最常见的原因）
2. 再查运镜是否堆叠（3+ 个运镜 → 减到 1 个）
3. 再查运镜是否写在镜内靠前位置
4. 再查幅度/速度是否过大（large amplitude 长距离 → 改 small）
5. 最后才考虑改运镜类型或改分镜
```

---

## 11. 检查清单与正反例速查表

### 11.1 提交前检查清单

#### A. 运镜（8 条）

| # | 检查项 | 判定 |
|---|---|---|
| A1 | 每个镜都写了运镜？（不用运镜也要写 `The camera holds a static shot.`） | 不写 = 模型自由发挥 |
| A2 | 一镜是否只给 1 个主运镜（最多 2 个，用 `while` 连接）？ | 3+ = 必漂移 |
| A3 | 运镜术语是否取自 §1.1 官方表？ | 自造词 = 不可控 |
| A4 | 参数顺序是否为 `类型 → 幅度 → 速度`？ | 顺序错 = 权重错 |
| A5 | 中等幅度 / 正常速度是否已省略？ | 官方要求省略 |
| A6 | 运镜句是否写成**自然英文句子**、且写在**镜内靠前**？ | 句末堆标签 = 违反官方要求 |
| A7 | 是否给了运镜落点（起点→终点 或 朝向）？ | 不写 = 运镜无目标 |
| A8 | 每镜**否定表达 ≤1 处**（`Do not` 句 + 裸名词否定**合并计**），且在末尾、前面有正向描述？ | 纯否定 = 模型无所适从 |
| A8b | 无**成串**裸名词否定；单个裸名词否定须为 **B 类**？ | A 类（能指给人看的）一律改正向 |

#### B. 剪辑（8 条）

| # | 检查项 | 判定 |
|---|---|---|
| B1 | `[Shot 1]` **没有**时间戳？ | 官方硬要求 |
| B2 | 后续镜头是否 `At MM:SS.mmm`（**三位小数**）？ | 两位 = 格式错 |
| B3 | 切点是否**严格递增**、且都**落在请求时长内**？ | 官方硬要求 |
| B4 | 指令首行锚点是否用 `S.SS`（**两位小数，无 MM: 前缀**）？ | 三位 = 格式错 |
| B5 | 切换动词是否取自官方五种（`cuts to` / `transitions to` / `changes to` / `switches to`）？ | 自造 = 可能不触发 |
| B6 | 软转场（dissolve/fade/wipe）是否**用户明确要求**？否则改硬切 | 默认硬切 |
| B7 | **每次切镜都引入了「主体/空间/状态/视角/时间」的新信息**？ | 只是改距离 → 改运镜 |
| B8 | 一句台词跨两镜时是否用了 `<scenetrans>` + 连续性措辞？ | 官方要求 |

#### C. 切分与衔接（8 条）

| # | 检查项 | 判定 |
|---|---|---|
| C1 | A + B + C 是否 **= 15.0s** 且取 0.5s 网格？ | 必须精确 |
| C2 | 每镜是否 ≥ 1.5s（硬下限）、建议 ≥ 2.0s？ | <1.5 = 不可生成 |
| C3 | 承载信息的镜是否 ≥ 3.0s？ | <3 = 立不住内容 |
| C4 | 悬殊比是否 ≤ 2.5？（超出需评估，量产需压住） | 2/11/2 = 5.5，走 T2 兜底 |
| C5 | 衔接镜任务"轻"还是"重"？轻 → 2–3s；重（揭示/长运镜）→ 4–5s | 见 §5.2 |
| C6 | **每一镜的提示词是否自成一体**（不依赖前文）？ | 否则 T2 降级梯失效 |
| C7 | 三镜是否都填了**备选方案**？ | 必填，不得写"重试" |
| C8 | 单独重生成短镜时是否请求了 **≥4 秒**（API 下限）再裁切？ | 请求 2s = 参数错误 |

#### D. 衔接手法（6 条）

| # | 检查项 | 判定 |
|---|---|---|
| D1 | 优先用**动作延续衔接法**？ | 最有效的一档 |
| D2 | 姿态参数是否**可量化**（120 度 / 45 度）且上下段**逐字一致**？ | 见 §7.5 三条铁律 |
| D3 | 衔接动作是否**简单、单向、慢速**？ | 复杂动作 = 高崩坏 |
| D4 | 上下段是否**逐字复用同一光位常量串**（色彩锚点，见 §8.2），且用**画面方位**而非角色左右？ | 主光换边 = 身份晃；`her left` 有歧义 = 翻转翻车根因 |
| D5 | 上下段是否用**同一个运镜 token**、方向**不反向**（运动方向锚点）？ | 同义改写 = 匹配不上 |
| D6 | 末帧主体位置 ≈ 下段首帧主体位置（构图锚点）？ | 粗匹配即可，别追像素级 |

> **A8b 否定表达分级（完整版见 `h3-antibug-check` §1.3）。口诀：模型能把它渲染出来的是 A 类，只是物理/时间属性的是 B 类。**
> **A 类 · 可被渲染的内容**（`fingers` / `text` / `numbers` / `logos` / `patterns` / `texture` / `detail`，**含动作类** `pouring` / `smoking` / `walking`）→ ❌ **一律改正向，不成串也不行**。
> **B 类 · 物理/时间属性**（`drift` / `shake` / `jitter` / `flicker` / `acceleration` / `eye movement`）→ ⚠️ 允许**单个**，须满足：一镜最多 1 处、前有正向描述、与 `Do not` 句**合并计 1 处额度**。
> **成串一律违规**：不论 A/B，≥2 个并列无谓语名词短语即违规（独立硬规则）。依据为反向激活机制外推的【推断】：A 类可独立生成，易泄漏；B 类只是帧间变化。
> ⚠️ **扫描查四种形式**：`no X` / `No X` / `does not X` / `never X`。`never grows larger` 这类**嵌入式否定同样计入 A8 的 1 处额度**。

### 11.2 正反例速查表

#### 运镜

| ❌ 反例 | ✅ 正例 | 原因 |
|---|---|---|
| `Push in. Small. Slow. Letter.` | `The camera pushes in with small amplitude at slow speed toward the folded letter.` | 官方：不要句末堆标签 |
| `The camera moves closer to her face.` | `The camera pushes in with small amplitude at slow speed toward her face.` | 必须用官方术语 |
| `zooms in and pushes in and tilts up` | 只留 1 个：`pushes in with small amplitude at slow speed` | 3 个运镜 = 平均成漂移 |
| 场景中段写 `...and the camera slowly pushes in...` | 运镜句紧随构图句，写在镜内靠前 | 靠前 token 权重更高 |
| （不写运镜）／`No camera movement at all.` | `The camera holds a static shot.` | 不写 = 模型自由发挥；用正向术语而非否定 |
| `large amplitude ... from a wide shot to a big close-up` | `small amplitude ... from a medium shot to a close-up` | 长距离慢推 = 末帧失控 |
| `arcs around her with large amplitude` | `arcs slowly around her with small amplitude at slow speed` | 大幅环绕崩坏率最高 |

#### 剪辑

| ❌ 反例 | ✅ 正例 | 原因 |
|---|---|---|
| `[Shot 1] At 00:00.000, ...` | `[Shot 1] ...` | 首镜不加时间戳 |
| `[Shot 2] At 00:05.00, ...` | `[Shot 2] At 00:05.000, ...` | 三位小数 |
| `[Shot 3] At 00:05.000`（同 Shot 2） | `[Shot 3] At 00:09.000` | 必须严格递增 |
| `[Shot 3] At 00:16.000`（15 秒视频） | `[Shot 3] At 00:11.500` | 必须落在时长内 |
| `[Shot 2] At 00:05.000, the shot dissolves to ...`（用户未要求） | `... the camera cuts to ...` | 默认硬切 |
| 中景她 → 切 → 近景她（同一姿势同一位置） | 改成一句推镜 `pushes in ... to a close-up` | 只改距离 → 用运镜 |
| 一句台词跨两镜，无标记 | 用 `<scenetrans>` + `continues seamlessly across the cut` | 官方要求 |

#### 切分与衔接

| ❌ 反例 | ✅ 正例 | 原因 |
|---|---|---|
| 1.0s / 13.0s / 1.0s | 2.0s / 11.0s / 2.0s | 硬下限 1.5s |
| 衔接镜 2.0s 承载关键反转 | 关键反转放 B 主镜；或给衔接镜 4–5s | 承载信息镜 ≥3s |
| 第 2 镜提示词写"同上"、"她"、"那张桌子" | 第 2 镜完整重写角色/环境/光线/画风 | 保留 T2 逃生通道 |
| 单独重生成 2s 衔接镜，请求 duration=2 | 请求 duration=4，生成后裁切 | API 下限 4 秒 |
| `she half-crouches` | `knees bent at roughly 120 degrees` | 姿态必须可量化 |
| 上段 120 度、下段 135 度 | 上下段都写 `120 degrees` | 参数一改，衔接就断 |
| 上段 `truck right` 收尾 → 下段 `pan right` 开场 | 下段写 `continues the same truck right` | 必须同一 token、同方向 |
| 上段向右收尾 → 下段向左开场 | 下段从向右开始 | 严禁反向 |
| 上段左前上方光 → 下段右前上方光 | 两段都写 `from the upper front left at 45°, warm amber` | 主光换边 = 身份晃 |
| 提示词里写 `colour temperature 3200K` | 写 `warm amber`（K 值不进提示词，见 §8.2） | 数字色温 token 响应度【待验证】 |
| 正反打跨请求分两次生成，靠提示词对齐朝向 | 合并进同一次请求，或后期镜像 | 硬阻断 |
| 拉远揭示镜不给尾帧 | 给尾帧构图图（FL2VA），或改硬切 | 无尾帧 = 身体凭空生成 |
| `non_diegetic_music: no music` | `non_diegetic_music: N/A` | 官方只有 `Use N/A when there is no non-diegetic music.`；`no music` 出自主模板九示例，**非官方口径** |
| 一镜里同时写 `No pouring.` 与 `does not deform` | 二选一，或都改正向 | 否定表达**合并计** ≤1 处 |

### 11.3 与其他 skill 的分工

| skill | 管什么 |
|---|---|
| `minimax-h3-storyboard` | 小说 → 集数 → 大纲 → 15 秒 3 镜分镜表 → 中文详版 → 官方格式转译 → 漏洞检查 |
| **`h3-camera-edit`（本 skill）** | 分镜表里的**运镜、切镜时间戳、段与段的接法** |
| `h3-*`（其余配套 skill） | 角色一致性、对白与声音、表演与动作、环境与光照、避坑词库 |

**配套文件**（需要更细的原文时回查，均在 `C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44\`）：

| 文件 | 用途 |
|---|---|
| `MiniMaxH3-小说转分镜-完整模板.md` | 主模板，**模块三**（15 秒 3 镜）、模块七（官方格式转译） |
| `MiniMax-H3-官方提示词规范调研报告.md` | 官方原文逐条摘录 |
| `衔接镜类型库_12列风险表单.md` | 衔接镜 12 列定稿表单 |
| `防翻车限制词库_H3版.md` | 翻车类型与规避写法 |
| `叙事侧方法论_小说拆解与15秒3镜结构.md` | 叙事侧时间分配范式与评级 |

### 11.4 待验证清单与实测方法

| # | 待验证项 | 实测方法 |
|---|---|---|
| 1 | 15 个方括号运镜 token（`[Truck right]` 等）是否生效、是否优于自然语句式 | 同一描述写两版（自然句 vs 方括号 token），同种子各生成 3 条，对比运镜是否执行、方向是否一致 |
| 2 | §9.3 各运镜类型的时长上限 | 走廊横移场景，请求 4/6/8/10/12/15s 六档，固定种子，检查末帧构图是否仍在描述范围内；找到失控那一档，减 2 秒作上限 |
| 3 | 悬殊比 2.5 这个阈值是否合理 | 用 5/5/5、4.5/6/4.5、2/11/2 各生成 10 条，统计三镜崩坏率与重生成连坐损失 |
| 4 | #7 揭示镜"中段畸变"在 H3 上的实际发生率 | 给首尾帧构图图，拉远段取 2s/3s/4s，各生成 5 条，逐帧检查中段身体比例 |
| 5 | 稳定器句式（§3.5）增益；**正向版是否优于含 `no` 串的旧版** | 三版（不加 / 旧版含 `no` 串 / 正向版）各生成 5 条，对比漂移、抖动与背景闪烁 |
| 6 | 时间戳 ±0.12 秒在中文提示词下是否成立 | 中文描述 + 三镜时间戳生成 10 条，逐条测量实际切点，统计偏差分布 |
| 7 | A/B 分级（§11.1 A8b）中 B 类词是否真的反向激活更弱 | `no flicker`（B）与 `no repeating patterns`（A）各生成 10 条，对比该类内容是否被"想出来" |
