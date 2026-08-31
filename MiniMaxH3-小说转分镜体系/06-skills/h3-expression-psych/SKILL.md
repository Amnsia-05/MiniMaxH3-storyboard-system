---
name: h3-expression-psych
description: 海螺 H3 视频提示词中「表情 / 眼睛动作 / 心理外化」的写法。心理不可见，必须转成可见的肌肉动作；含情绪→动作对照库、眼神写法、微表情模板。触发词：H3表情、H3眼神、H3心理描写、H3情绪、H3微表情、H3面部特写。
agent_created: true
---

# H3 表情 / 眼睛动作 / 心理外化

**一句话方法论**：心理不可见，必须外化成可见动作。

本 skill 是 `minimax-h3-storyboard` 流水线的**表演层补充**，专门解决「小说里的心理描写，在 H3 提示词里该怎么写」。

---

## 0. 怎么用这份 skill

| 你要干什么 | 跳到 |
|---|---|
| 小说里写「她很愤怒」，不知道怎么转成提示词 | §3 情绪对照库 → 查「愤怒」 |
| 想写眼神、眨眼、看向画外 | §4 眼睛动作专章 |
| 只有 2 秒，能塞几个表情变化？ | §5 微表情与短镜头 |
| 表情和台词对不上 | §6 三元一致性校验 |
| 想拍大特写 | §7 先看风险，再决定景别 |
| 已经生成了，脸崩了 / 表情突变 | §9 常见翻车与规避 |
| 提交前最后过一遍 | §10 检查清单 |

### 0.1 与主模板的关系

| 文件 | 关系 |
|---|---|
| `MiniMaxH3-小说转分镜-完整模板.md` | **上游主模板**。模块六 §6.4-B「表演要素」是本 skill 的依据；模块九 §9.3/§9.4 是范例 |
| `防翻车限制词库_H3版.md` | 术语与否定句口径以它为准 |
| `衔接镜类型库_12列风险表单.md` | **#4 眼神/面部反应镜**的风险评级，本 skill §4、§7 直接引用 |

**术语一致性**：本 skill 全部沿用主模板的「景别 / 运镜 / 锁定块 / 收边 / 三镜 A-B-C / 时长校验」等术语，不另立名词。

### 0.2 可信度标注

| 标记 | 含义 |
|---|---|
| 【官方】 | MiniMax 官方仓库 / API 文档 / 模型卡原文 |
| 【主模板】 | 主模板已定稿条款 |
| 【业界】 | 通用影视表演 / 面部动作编码（FACS / Ekman）常识，非 H3 特有 |
| 【推断】 | 由已知机制推导，无公开量化基准 |
| 【待验证】 | **H3 上无实测数据**。本文给出实测方法，不要当既成事实用 |

> **铁律**：情绪→肌肉的对应关系属【业界】（FACS 体系），**H3 是否忠实复现某个具体动作属【待验证】**。凡标【待验证】的项，**不得承载叙事信息**——观众认不出来也不影响剧情，才可以写。

---

## 1. 方法论基石：为什么心理不能直写

### 1.1 模型没有"内心"这个概念

H3 的输入是文本，输出是像素。它能建立的是**「文字 → 可见像素统计」**的映射，不是**「文字 → 角色内心 → 表情」**的推理链。

写 `she is heartbroken`，模型只能去训练数据里找"标注为 heartbroken 的画面"的统计特征——而这个特征在不同样本里可能是哭、是发呆、是笑。**你给的是一个类别，模型返回的是一个采样。**

写 `her lower lip pushes out and trembles, her inner brows lift`，你给的是**一组确定的像素目标**，模型的采样空间被压缩了。

> **判断标准**：能不能被摄像机拍到？拍不到的一律改写。

### 1.2 心理外化的四条路径

| 路径 | 写什么 | 示例 | 可靠度 |
|---|---|---|---|
| **① 面部**（主力） | 眉、眼、鼻、唇、下颌、颈部的**肌肉变化** | `her jaw tightens, her eyebrows draw together` | 高 |
| **② 肢体**（辅助，且常被低估） | 肩、手、呼吸、姿态 | `her shoulders drop away from her ears, she lets out a long breath` | **高**（比面部更抗崩） |
| **③ 道具 / 接触物** | 角色对物件的动作 | `her thumb picks at her cuticle`, `her fingers tighten on the cup` | 中（避开精细持物） |
| **④ 环境**（仅辅助） | 光影、风、发丝、衣摆 | `dust drifts through the warm lamp light`, `the hem of her coat sways once` | 中（只做氛围，不承载信息） |

**四条路径的优先级**：① ② 是主力，③ ④ 是辅助。

> ⚠️ **环境不能替代外化。** 「天在下雨」不能说明人物难过——观众能读出的是氛围呼应，不是心理。**心理外化必须落在①②③上。**
>
> 在 H3 官方格式里，④ 落在 `integrated_multimodal_description` 的**环境反应段**（主模板 §6.1 段④），它是画面的一部分，不是情绪的替身。

### 1.3 反例大表：抽象词 → 可见动作

| ❌ 不能写（不可见 / 是类别不是画面） | ✅ 改写（可见） |
|---|---|
| she is heartbroken | `her inner brows lift, her lower lip pushes out and trembles` |
| she looks angry | `her brows draw together and lower, her jaw tightens` |
| he is nervous | `he swallows hard, his fingers pick at the seam of his sleeve` |
| she feels guilty | `her gaze drops to her hands, her thumb picks at her cuticle` |
| he is pretending to be calm | `his smile stays on his mouth and never reaches his eyes` |
| she is thinking | `her gaze goes flat and unfocused, her fingers stop moving` |
| he is lying | `his eyes slide away from hers and stay away, he swallows once` |
| she is relieved | `her shoulders drop away from her ears, she breathes out slowly` |
| he is heartless | `his face holds perfectly still, his gaze passes straight through her` |
| she is determined | `her jaw tightens, her gaze locks onto a fixed point ahead` |
| he is shocked | `his brows fly up, his jaw drops open` |
| she is hesitant | `she catches her lower lip between her teeth, her gaze flickers to the door` |

**禁用情绪名词清单**（主模板 §6.4-B 已定「写可见的肌肉变化，不写情绪名词」）：

```
sad / angry / afraid / happy / nervous / guilty / jealous / proud / relieved /
disappointed / excited / calm / heartbroken / determined / suspicious / disgusted /
contemptuous / numb / smug / awkward  ← 一律不写
```

### 1.4 一条可直接复制的外化流程

```
① 从小说里抽出心理句        例：「她心虚了」
        ↓
② 问：这个状态在脸上/身上能看到什么？   答：视线躲开、眨眼变多、手指有动作
        ↓
③ 拆到具体区域              眼（视线落点）+ 眼（眨眼）+ 手（抠指甲）
        ↓
④ 用 then 串起来，给每个动作一个终点
        ↓
⑤ 写成提示词：her gaze drops to her hands and stays there, then her blink rate
   picks up, then her thumb begins to pick at her cuticle
```

---

## 2. 表情写法规范

### 2.1 核心规范

> 【主模板 §6.4-B】**表情：写可见的肌肉变化，不写情绪名词。**
> ✅ `her eyebrows draw together, her jaw tightens`
> ❌ `she looks sad`

**三条细则**：

1. **写动作，不写状态。** ✅ `her jaw tightens`（过程） ❌ `her jaw is tight`（状态，模型容易忽略）
2. **给终点。** ✅ `her chin lifts until her gaze is level with the lens` ❌ `her chin lifts`
3. **一镜内同一区域的动作不超过 2 个。** 写「眉蹙 → 眉松开 → 眉再蹙」在短镜里会变成抖动

### 2.2 面部区域分解与动词库

这是本 skill 的核心词表。**选 1–2 个区域、每个区域 1 个动词**即可构成一句可用的表情描述。

| 区域 | 英文写法（可直接复制） | 中文 |
|---|---|---|
| **眉** | `her eyebrows draw together` | 眉头靠拢 |
| | `her brows lower` | 眉毛下压 |
| | `her inner brows lift` | 眉内侧上提 |
| | `the outer ends of her brows droop` | 眉尾下垂 |
| | `one eyebrow arches` | 单侧眉毛上扬 |
| | `her eyebrows flash up and settle` | 眉闪（快速上扬再落下）【业界：greeting signal】 |
| | `her brow unknots and settles level` | 眉头松开、展平 |
| | `vertical lines form between her brows` | 眉间竖纹出现 |
| **眼 / 眼睑** | `her upper lids lift` | 上睑抬起 |
| | `her lids lower` | 眼睑下垂 |
| | `her eyes narrow to slits` | 眯成缝 |
| | `her eyes open wide` | 眼睛睁大 |
| | `her eyes squeeze shut` | 紧闭双眼 |
| | `she blinks once` | 眨一次眼 |
| | `her eyes close for a full second and reopen` | 闭眼一秒再睁开 |
| | `she holds her eyes open without blinking` | 睁着眼不眨 |
| | `her gaze goes flat and unfocused` | 目光失焦 |
| | `her gaze locks onto a fixed point` | 目光锁定一个点 |
| **鼻** | `her nostrils flare` | 鼻翼张大 |
| | `her nose wrinkles` | 鼻根皱起 |
| | `the bridge of her nose creases` | 鼻梁出现横纹 |
| **唇 / 口** | `her lips press into a thin line` | 抿成一条线 |
| | `her lips part` | 双唇微张 |
| | `one corner of her mouth lifts` | 单侧嘴角上提 |
| | `the corners of her mouth pull down` | 嘴角下拉 |
| | `her lips stretch horizontally` | 唇横向拉开 |
| | `her upper lip curls up` | 上唇上翻 |
| | `her lower lip pushes out` | 下唇外推 |
| | `her lower lip trembles` | 下唇颤抖 |
| | `she catches her lower lip between her teeth` | 咬住下唇 |
| **下颌 / 下巴** | `her jaw tightens` | 下颌收紧 |
| | `her jaw sets` | 牙关扣住 |
| | `her jaw clenches, the muscle at her jaw angle bulges` | 咬紧，咬肌隆起 |
| | `her jaw unclenches` | 下颌松开 |
| | `her chin lifts` | 下巴抬起 |
| | `her chin drops to her chest` | 下巴垂到胸前 |
| | `her lower jaw trembles once` | 下颌颤一下 |
| **颊 / 额** | `her cheeks lift and push her lower lids up` | 脸颊上提、顶起下眼睑 |
| | `creases fan out from the corners of her eyes` | 眼角鱼尾纹张开 |
| | `her forehead creases into horizontal lines` | 额头出现横纹 |
| | `her forehead smooths out` | 额头展平 |
| **颈 / 喉** | `she swallows once` | 吞咽一次 |
| | `her throat works as she swallows repeatedly` | 喉结反复滚动 |
| | `the tendons in her neck stand out` | 颈部青筋凸起 |
| | `her head bows forward` | 头向前低垂 |
| **呼吸 / 肩** | `she draws one long slow breath` | 长吸一口气 |
| | `a sharp intake of breath` | 倒抽一口气 |
| | `she breathes out slowly through parted lips` | 从微张的唇间缓缓呼气 |
| | `her breath comes short and shallow` | 呼吸短促 |
| | `her shoulders drop away from her ears` | 肩膀从耳侧沉下 |
| | `her shoulders ride up and stay up` | 肩耸起并保持 |
| | `her shoulders slump` | 双肩塌陷 |

### 2.3 正反例对照

| ❌ 错 | 为什么错 | ✅ 对 |
|---|---|---|
| `she looks angry` | 情绪名词，是类别不是画面 | `her brows draw together and lower, her jaw tightens` |
| `a sad expression` | 抽象名词，模型采样空间过大 | `the corners of her mouth pull down, her lower lip trembles` |
| `her face shows determination` | 心理名词 | `her jaw tightens, her gaze locks onto a fixed point ahead` |
| `she smiles sadly` | 「sadly」是副词情绪 | `her mouth curves up while her eyes stay flat and unfocused` |
| `emotion crosses her face` | 没有任何可见信息 | `first her brows lift, then her jaw tightens, then her gaze drops` |
| `she cries` | 「哭」是过程，短镜装不下；且结果不可控 | `her eyes are already glistening, a single tear runs down her right cheek` |
| `her expression changes` | 无具体变化 | `her jaw unclenches and her lips part` |
| `she looks at him with hatred` | 情绪名词 | `her eyes narrow to slits, her upper lip curls up on one side` |
| `he is expressionless` | 否定式状态（且易被忽略） | `his face holds perfectly still, his mouth is a flat line` |
| `her eyes widen in shock` | 「in shock」是情绪 | `her brows fly up, her eyes open wide, her jaw drops open` |

> **一条容易漏的**：`she smiles` 只有嘴动，模型常生成"只动嘴不动眼"的僵笑。
> **真笑要写眼睛参与**【业界：Duchenne smile】：`her cheeks lift and push her lower lids up, creases fan out from the corners of her eyes, then her mouth curves up`。
> **假笑则反之**：`her mouth curves up while her eyes stay flat`。

---

## 3. 情绪 → 写法对照库（核心）

**用法**：查情绪 → 取「中」档描述串 → 按上下文微调 → 用 `then` 接进动作链。

**强度梯度用法**：
- **弱** = 内心已有、外表刚露头 → 用于 A 入镜、2 秒衔接镜
- **中** = 标准档 → 用于 B 主镜
- **强** = 完全释放 → 用于段落情绪最高点、C 出镜卡点

---

### 3.1 愤怒 Anger

**可见特征**：眉内侧下压并靠拢（眉间竖纹）→ 上睑抬起、下睑紧绷、目光锁定 → 鼻翼张大 → 唇抿紧成线或张开露齿 → 咬肌隆起 → 颈部肌肉绷紧。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her brows draw slightly closer, her lips press into a thin line, her jaw sets` |
| 中 | `her eyebrows draw together and lower, her jaw tightens, her nostrils flare slightly, her lips press into a hard line` |
| 强 | `her brows crash down and inward with deep vertical lines between them, her nostrils flare wide, her jaw clenches until the muscle at her jaw angle bulges, her lips part over set teeth, the tendons in her neck stand out` |

**中文**：弱＝眉头微拢、抿唇、牙关扣住／中＝眉头下压靠拢、下颌收紧、鼻翼微张、唇抿成硬线／强＝眉头狠狠压下、眉间竖纹深陷、鼻翼大张、咬肌隆起、唇间露齿、颈部青筋凸起

---

### 3.2 恐惧 Fear

**可见特征**：眉内侧**上提**并聚拢（与愤怒的"下压"相反，这是最关键的区分）→ 上睑大幅抬起、虹膜上方露白 → 唇横向拉开、嘴角后拉 → 下颌下垂。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her eyebrows lift slightly at the inner ends, her lips part, her breath catches once` |
| 中 | `her inner brows lift and draw together, her upper lids rise until a thin line of white shows above the iris, her lips stretch horizontally, her jaw drops slightly` |
| 强 | `her brows shoot up and together, her eyes open wide with white visible above the iris, her lips pull back horizontally, her jaw hangs open, her breath comes short and shallow` |

**中文**：弱＝眉内侧微提、双唇微张、呼吸一顿／中＝眉内侧上提聚拢、上睑抬起露出虹膜上方一线眼白、唇横向拉开、下颌微垂／强＝眉毛猛地上提聚拢、眼睛大睁四周露白、唇向后拉、下颌全开、呼吸短促

---

### 3.3 悲伤 Sadness

**可见特征**：眉内侧上提 + 眉尾下垂（形成"八字"）→ 上睑下垂、目光下移失焦 → 嘴角下拉 → 下唇外推并颤抖 → 吞咽（喉结上下）。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her gaze lowers, the corners of her mouth turn down slightly, she swallows once` |
| 中 | `her inner brows lift while the outer ends droop, her upper eyelids lower, the corners of her mouth pull down, her lower lip pushes out and trembles` |
| 强 | `her brows form a steep inverted V with the inner ends raised high, her upper lids sink, her eyes glisten and overflow, her mouth draws down hard at both corners, her lower lip quivers, she swallows against the lump in her throat` |

**中文**：弱＝目光下垂、嘴角微撇、吞咽一次／中＝眉内侧上提而眉尾下垂、上睑下垂、嘴角下拉、下唇外推颤抖／强＝眉呈倒八字、上睑沉重、泪光溢出、嘴角用力下拉、下唇颤抖、强忍着吞咽

---

### 3.4 震惊 Surprise / Shock

**可见特征**：眉**整体**大幅上提（横向拉平，额头横纹）→ 上睑抬起、眼白露出 → 下颌下垂、嘴呈 O 形 → 伴随身体微后倾或吸气。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her eyebrows lift, her lips part slightly, she draws a short breath` |
| 中 | `her brows fly up into horizontal lines across her forehead, her eyes widen, her jaw drops and her mouth opens into a small O` |
| 强 | `her eyebrows shoot high and her forehead creases into deep horizontal lines, her eyes open to their limit, her jaw drops open, her whole body pulls back a fraction, a sharp intake of breath` |

**中文**：弱＝眉毛上提、双唇微张、短吸一口气／中＝眉毛扬起、额头出现横纹、眼睛睁大、下颌垂下嘴微张成 O／强＝眉毛高高扬起额头深横纹、眼睛睁到极限、下颌全开、身体微微后缩、倒抽一口气

---

### 3.5 厌恶 Disgust

**可见特征**：鼻根皱起（鼻梁横纹）→ 上唇大幅上提、鼻翼两侧成深沟 → 下唇上推 → 头微微转向一侧。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her nose wrinkles slightly, her upper lip lifts on one side` |
| 中 | `her nose wrinkles and the bridge creases, her upper lip curls up, her cheeks push the lower lids up` |
| 强 | `her nose wrinkles hard, her upper lip curls high and her lower lip pushes up to meet it, deep grooves form beside her nostrils, she turns her head slightly away` |

**中文**：弱＝鼻子微皱、单侧上唇上提／中＝鼻根皱起鼻梁横纹、上唇上翻、脸颊顶起下眼睑／强＝鼻子狠狠皱起、上下唇对挤、鼻翼两侧深沟、头微微转开

---

### 3.6 轻蔑 Contempt

**可见特征**：**单侧**嘴角上提（不对称是标志性特征）→ 鼻翼微皱 → 下巴微抬、头略后仰 → 眼睑半垂、自上而下看人。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `one corner of her mouth lifts slightly, her chin tilts up a degree` |
| 中 | `one corner of her mouth lifts into a half-smile while the other stays flat, her nose creases faintly, her chin lifts and she looks down the line of her nose` |
| 强 | `one side of her mouth curls high in a one-sided sneer, her head tilts back, her eyelids lower to half-mast as she looks down the length of her nose at him` |

**中文**：弱＝单侧嘴角微提、下巴微抬／中＝单侧嘴角上扬另一侧保持平直、鼻子微皱、抬下巴俯视／强＝单侧嘴角高高撇起成冷笑、头后仰、眼睑半垂居高临下地看

---

### 3.7 怀疑 Suspicion / Doubt

**可见特征**：单侧眉毛上扬（不对称）→ 眯眼 → 头部微侧倾 → 视线扫视目标而非锁定 → 单侧嘴角压平。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `one eyebrow lifts a little, her head tilts slightly` |
| 中 | `one eyebrow arches while the other stays level, her brow furrows lightly, her eyes narrow, her head tilts to one side` |
| 强 | `one eyebrow shoots up, her eyes narrow to slits, her gaze flicks over him from head to foot and back, her head cocks hard to one side, one corner of her mouth presses flat` |

**中文**：弱＝单侧眉毛微扬、头微偏／中＝单侧眉毛弓起另一侧不动、眉头轻蹙、眼睛眯起、头侧向一边／强＝单侧眉毛猛扬、眯成缝、目光上下扫视、头大幅侧倾、单侧嘴角压平

---

### 3.8 犹豫 Hesitation

**可见特征**：咬下唇或抿唇 → 视线在两处之间来回 → 吞咽 → 手指停在半空 → 眉头微蹙但**不聚拢**（与愤怒区分）。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `she bites the inside of her lower lip, her gaze drops and returns` |
| 中 | `she catches her lower lip between her teeth, her brow furrows without drawing together, her gaze flickers between the door and the letter, she swallows once` |
| 强 | `she presses her lips together then releases them, her breath comes short, her gaze darts between the two and cannot settle, her jaw works once before she speaks` |

**中文**：弱＝轻咬下唇内侧、目光落下又抬起／中＝咬住下唇、眉头微蹙但不聚拢、目光在门与信之间游移、吞咽一次／强＝抿唇又松开、呼吸短促、目光在两处之间无法落定、开口前下颌动了一下

---

### 3.9 决绝 Resolve

**两版写法**，按叙事语境选：

**A 版「压眉版」**——忍痛下定决心（主模板 §9.3 用的就是这一版：`her jaw tightens and her eyebrows draw together, then her chin lifts and her gaze rises to a fixed point beyond the lens`）

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her brows draw together, her jaw tightens, her gaze stops moving` |
| 中 | `her jaw tightens and her eyebrows draw together, then her chin lifts and her gaze rises to a fixed point` |
| 强 | `her brows lock down together, her jaw clenches hard, her chin lifts until her eyes are level, her gaze fixes on a point straight ahead and holds there` |

**B 版「展眉版」**——想通后下定决心（眉头松开是"看开了"的信号）

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her brow smooths out, her jaw sets, her gaze holds one point` |
| 中 | `her brow unknots and settles level, her jaw tightens, her lips press into a flat line, her gaze locks onto a fixed point ahead` |
| 强 | `the furrow leaves her brow entirely, her jaw clenches, she draws one long slow breath and holds it, her eyes fix on a single point, unblinking` |

**中文**：A 弱＝眉头聚拢、下颌收紧、目光停住／A 中＝下颌收紧眉头靠拢，接着下巴抬起视线升至一个固定点／A 强＝眉头锁死、咬紧牙关、下巴抬到眼平、视线钉死在正前方不动摇／B 弱＝眉头展平、牙关扣住、目光落定／B 中＝眉头松开持平、下颌收紧、唇压成平线、目光锁定前方一点／B 强＝眉间皱纹完全消失、咬紧、长吸一口气屏住、双眼定在一点上不眨

---

### 3.10 心虚 Guilty conscience

**可见特征**：视线刻意躲开特定目标 → 眨眼频率上升 → 手指无意识小动作（抠指甲、摸鼻侧）→ 舔唇 → 肩微缩。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her gaze slides away and returns, she blinks once more than needed` |
| 中 | `her gaze drops to her hands and stays there, her blink rate picks up, her thumb picks at her cuticle, she licks her lower lip` |
| 强 | `her head turns from side to side, her gaze sweeping everywhere except the other person's face, she blinks rapidly, her hand goes up to touch the side of her nose, her lips go dry and she licks them twice, her shoulders draw up around her ears` |

**中文**：弱＝视线滑开又回来、多眨了一次／中＝目光垂到手上不动、眨眼变快、拇指抠指甲、舔下唇／强＝目光避开对方面孔到处乱飘、快速眨眼、手抬起来摸鼻侧、唇干连舔两次、肩缩向耳朵

> **心虚 vs 紧张 的区分**：紧张**没有回避对象**（只是身体反应）；心虚**回避一个特定的目标**（人、物、话题）。写的时候必须把这个目标写出来——`her gaze avoids the envelope on the desk`。

---

### 3.11 愧疚 Guilt / Remorse

**可见特征**：眉内侧上提（与悲伤同区）→ 眼睑下垂、抬不起眼 → 嘴角下拉并颤抖 → 头部低垂 → 手捂嘴或捂脸。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her gaze drops to the floor, her mouth turns down at the corners, she is still for a moment` |
| 中 | `her inner brows lift, her eyelids lower, she cannot raise her eyes, the corners of her mouth pull down and tremble, she swallows` |
| 强 | `her head bows, her brows pull up into a knot of distress, her eyes fill and her lower lip quivers, her hand comes up to cover her mouth, her shoulders fold forward` |

**中文**：弱＝目光垂向地面、嘴角下撇、静止片刻／中＝眉内侧上提、眼睑下垂抬不起眼、嘴角下拉颤抖、吞咽／强＝头低垂、眉毛拧成痛苦的一团、眼眶充盈下唇颤抖、手抬起来捂住嘴、双肩向前合拢

---

### 3.12 隐忍 Suppression

**可见特征**：咬肌隆起但**嘴闭合** → 深呼吸并屏住 → 吞咽压制喉部动作 → 眼睑下垂遮住眼神 → 手指握拳或抓紧。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `she presses her lips together, holds one slow breath, and lets it out` |
| 中 | `her lips press into a thin white line, her jaw sets hard, she draws one deep breath through her nose and holds it, her eyelids lower to hide her eyes` |
| 强 | `her teeth clamp down until the muscle at her jaw angle bulges, her nostrils flare with a held breath, her fingers curl into a fist and stop there, her eyes stay fixed and dry, unblinking` |

**中文**：弱＝抿唇、屏一息、缓缓吐出／中＝唇抿成白色细线、牙关扣紧、用鼻子深吸一口气屏住、眼睑垂下藏住眼神／强＝牙关咬紧到咬肌隆起、鼻翼随屏息张大、手指攥拳停住、双眼干涩定住不眨

> **隐忍是 H3 上性价比最高的情绪**：动作幅度小、跨帧稳定，不容易崩五官。想不出怎么写时，先试隐忍。

---

### 3.13 嫉妒 Envy / Jealousy

**可见特征**：**嘴在笑、眼不参与**（假笑）→ 眯眼 → 视线紧盯目标不放 → 下颌在笑容下收紧 → 单侧眉毛微抽。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her smile stays on her mouth and never reaches her eyes, her gaze lingers` |
| 中 | `her mouth smiles but her eyes stay flat and cold, her lids narrow slightly, her gaze follows the other woman across the room and stays locked on her` |
| 强 | `her lips stretch into a tight smile that leaves her eyes dead, her eyes narrow to slits, her jaw tightens under the smile, one eyebrow twitches up and she looks away too fast` |

**中文**：弱＝笑容只停在嘴上、不到眼底、目光滞留／中＝嘴在笑而眼睛平淡发冷、眼睑微眯、目光跟着对方穿过房间不放／强＝唇绷出紧笑而眼神死寂、眯成缝、笑容之下下颌收紧、单侧眉毛抽动、过快地把视线移开

---

### 3.14 贪婪 Avarice / Greed

**可见特征**：视线锁定目标物、不眨眼 → 舔唇或咬唇 → 头前伸、身体前倾 → 手指微屈成预备抓握 → 呼吸加深。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her gaze fixes on the object and holds, she wets her lips once` |
| 中 | `her eyes lock onto the object and she stops blinking, she licks her lips, she leans forward a fraction` |
| 强 | `her gaze locks on the object and stays on it, she licks her lips and then bites the lower one, her head pushes forward and her fingers curl into a half-grip` |

**中文**：弱＝目光钉在物件上、舔一次唇／中＝双眼锁住物件不再眨眼、舔唇、身体微微前倾／强＝目光锁死不离开、舔唇后又咬住下唇、头部前伸、手指微屈成半抓握

> ⚠️ **【待验证】** 不要写 `her pupils dilate`（瞳孔放大）。瞳仁在 768p 下像素极小，H3 是否忠实响应未实测。**实测方法**：单镜 5 秒，同一提示词只改瞳孔描述，生成 10 条，统计瞳孔直径差异是否稳定。**未实测前不得承载叙事信息。**

---

### 3.15 释然 Relief

**可见特征**：肩膀下沉（**最可靠的标志**）→ 眉间纹消失 → 一次**长**呼气 → 闭眼一秒再睁开 → 单侧嘴角微扬。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her shoulders drop, she lets out a long breath` |
| 中 | `her shoulders drop away from her ears, the lines between her brows smooth out, she breathes out slowly through parted lips` |
| 强 | `her whole shoulder line drops several inches, her brow releases completely, her eyes close for a full second and reopen, a long breath leaves her and one corner of her mouth curves up` |

**中文**：弱＝肩膀沉下、长呼一口气／中＝肩膀从耳侧落下、眉间纹展平、从微张的唇间缓缓吐气／强＝整条肩线下沉数寸、眉头完全松开、闭眼整整一秒再睁开、长长吐气、单侧嘴角微扬

---

### 3.16 失望 Disappointment

**可见特征**：肩膀塌陷 → 上睑下垂、目光失焦 → 嘴角下拉 → **短促**的一次呼气（与释然的"长呼气"相反）→ 头部微摇。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her gaze drops, the corners of her mouth turn down, a short breath leaves her` |
| 中 | `her shoulders slump, her upper eyelids lower, her gaze goes flat and unfocused, the corners of her mouth pull down, she exhales once, short and hard` |
| 强 | `her shoulders collapse, her head bows forward, her eyes lose their focus entirely, her mouth draws down at both corners, she gives one small shake of her head` |

**中文**：弱＝目光下垂、嘴角下撇、短呼一口气／中＝双肩塌陷、上睑下垂、目光平淡失焦、嘴角下拉、短促地呼一口气／强＝肩膀垮掉、头向前低、目光完全失去焦点、嘴角用力下拉、轻轻摇一下头

> **释然 vs 失望**：两者都沉肩。**区别在呼气长度与嘴角方向**——释然＝长呼气＋嘴角上扬；失望＝短呼气＋嘴角下拉。这个对比可以在一个段落里前后脚使用，信息密度很高。

---

### 3.17 期待 Anticipation

**可见特征**：眉外侧上提 → 睁眼、目光前视 → 唇微张（呼吸准备）→ 身体前倾 → 呼吸变浅变快 → 手指轻颤。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her eyebrows lift a little, her lips part, she leans forward slightly` |
| 中 | `her outer brows lift, her eyes widen and look ahead, her lips part, her breathing quickens, she leans forward` |
| 强 | `her brows ride high, her eyes open wide and fix on the doorway, her lips part and her breath comes fast and shallow, her whole body tips forward, her fingers drum once against her thigh` |

**中文**：弱＝眉毛微提、双唇微张、身体微微前倾／中＝眉外侧上提、睁大眼睛向前看、唇微张、呼吸加快、身体前倾／强＝眉毛高挑、双眼大睁钉在门口、唇张呼吸又浅又快、整个身体前倾、手指在大腿上敲了一下

---

### 3.18 紧张 Nervousness

**可见特征**：吞咽频繁 → 舔唇 → 眨眼变快 → 下颌轻颤 → 手指小动作（搓、捏、抠）→ 呼吸变浅 → 肩微耸。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `she swallows once, her fingers still` |
| 中 | `she swallows hard, her blink rate rises, her fingers pick at the seam of her sleeve, her breath comes shallow` |
| 强 | `her throat works as she swallows repeatedly, her lips dry and she licks them, her lower jaw trembles once, her fingers twist together in her lap, her shoulders ride up and stay up` |

**中文**：弱＝吞咽一次、手指停住／中＝用力吞咽、眨眼变快、手指抠袖口缝线、呼吸变浅／强＝喉结反复滚动、唇干舔唇、下颌颤一下、手指在膝上绞在一起、肩耸起并保持

---

### 3.19 放松 Relaxation

**可见特征**：下颌松开（上下齿分离、唇微开）→ 额头与眉间纹消失 → 眼睑半垂 → 肩膀下沉并后展 → 呼吸变慢变深。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her jaw unclenches, her lips part` |
| 中 | `her jaw releases and her lips part slightly, the lines across her forehead smooth away, her shoulders drop and settle back` |
| 强 | `her whole face lets go — her jaw hangs loose, her lids drop to half-mast, her forehead smooths entirely, her shoulders sink and her breath slows to a long slow tide` |

**中文**：弱＝下颌松开、双唇微开／中＝下颌释放唇微张、额头横纹展平、肩膀沉下并向后放平／强＝整张脸松开——下颌松弛、眼睑半垂、额头完全展平、肩膀下沉、呼吸慢下来成悠长潮汐

---

### 3.20 傲慢 Arrogance / Pride

**可见特征**：下巴抬起（自上而下看人）→ 眼睑半垂 → 单侧嘴角微提（比轻蔑更放松）→ 肩背挺直、胸腔打开 → 长时间不眨眼。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her chin lifts a degree, her shoulders settle back` |
| 中 | `her chin lifts, her eyelids drop to half-mast, her shoulders draw back and her chest opens, she looks down the line of her nose` |
| 强 | `her chin comes up until she is looking down her nose, her lids hang at half-mast, her back straightens and her chest lifts, she holds his gaze without a single blink` |

**中文**：弱＝下巴微抬、肩向后放平／中＝下巴抬起、眼睑半垂、肩后展胸腔打开、沿鼻梁线向下看人／强＝下巴抬到俯视角度、眼睑半垂、背挺直胸廓抬起、直视对方一次都不眨

---

### 3.21 讨好 Ingratiation

**可见特征**：**眉闪**（眉毛快速上扬再落下）【业界：greeting signal】→ 大幅且**对称**的真笑（眼睛参与，眼角出现纹路）→ 点头 → 头部微倾 → 视线频繁接触后快速移开 → 身体前倾。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her eyebrows flash up and settle, a small smile appears, she nods once` |
| 中 | `her brows flash up and fall, a quick symmetrical smile crinkles the corners of her eyes, she nods twice, her head tilts to one side` |
| 强 | `her eyebrows shoot up and hold, a wide smile pulls her cheeks up and creases the skin beside both eyes, she nods repeatedly, her body leans forward, her gaze flicks to his face and away and back again` |

**中文**：弱＝眉快速上扬后落定、出现浅笑、点一次头／中＝眉毛一闪即落、快速对称的笑让眼角起皱、点两次头、头侧向一边／强＝眉毛高扬并保持、大笑把脸颊顶起两侧眼角起皱、连连点头、身体前倾、目光在他脸上落下又移开又回来

---

### 3.22 麻木 Numbness / Apathy

**可见特征**：面部全部区域静止 → 眼睑半垂或全睁但**不聚焦** → 无吞咽、无眨眼节律变化 → 嘴角保持中性平线 → 目光**穿过**目标而非落在其上。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her face settles into a blank mask, her gaze drifts past him` |
| 中 | `her face holds perfectly still, her eyelids hang at half-mast, her gaze passes through him without landing, no swallow, no blink` |
| 强 | `her face is completely empty — her lids hang low, her mouth is a flat line, her eyes look straight through the person in front of her and register nothing, she holds her eyes open, unblinking, for the entire shot` |

**中文**：弱＝脸定格成空白面具、目光从他身上飘过／中＝脸完全静止、眼睑半垂、目光穿过他而不停留、不吞咽、不眨眼／强＝整张脸全空——眼睑低垂、嘴是一条平线、目光直直穿过面前的人什么都没接收、整镜不眨眼

> **麻木是 H3 上最安全的表情**（变化量最小）。适用场景：① 大特写镜头 ② 高风险段落 ③ 需要稳住身份时。

---

### 3.23 崩溃 Breakdown

**可见特征**：面部**自上而下依次失守**——眉头先拧 → 眼睑紧闭挤压 → 鼻根皱起 → 嘴张开变形；伴随呼吸失控（抽气）、肩部抖动、头部下埋。**顺序感是关键**，不要同时写。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `her brow contracts, she presses her lips together and holds, her breath catches once` |
| 中 | `first her brows knot, then her eyes squeeze shut and the skin around them creases, then her mouth opens in a silent shape, her shoulders begin to shake, one sharp gasp escapes` |
| 强 | `her face folds in on itself — her brows knot hard, her eyes clench shut, her nose wrinkles, her mouth opens and works without sound, her shoulders heave, her head drops forward into her hands` |

**中文**：弱＝眉头收紧、抿唇屏住、呼吸一顿／中＝先眉头打结，再双眼紧闭眼周起皱，再嘴张开成无声形状，双肩开始发抖，一声抽气漏出／强＝脸向内塌陷——眉头死拧、双眼紧闭、鼻根皱起、嘴张开无声地动、双肩起伏、头向前埋进双手

> ⚠️ **崩溃是崩脸高风险项**（全脸大幅形变）。**只放在中近景及以上**，禁止放在大特写。见 §7。

---

### 3.24 狂喜 Elation / Euphoria

**可见特征**：**眼睛参与的真笑**（脸颊上提、顶起下眼睑、眼角鱼尾纹张开）→ 嘴大幅张开、嘴角上提 → 眉毛上提 → 伴随向上的动作（跳、举手、仰头）。

| 强度 | 英文描述串 |
|---|---|
| 弱 | `a real smile reaches her eyes, the corners crinkle, her cheeks lift` |
| 中 | `her cheeks lift high and push her lower lids up, deep creases fan out from the corners of her eyes, her mouth opens wide, her brows lift` |
| 强 | `her whole face opens up — her cheeks lift until her eyes half-close into creased arcs, her mouth opens wide and her head tips back, her brows fly up, she cannot keep still` |

**中文**：弱＝真笑到达眼底、眼角起皱、脸颊上提／中＝脸颊高高顶起下眼睑、眼角鱼尾纹张开、嘴大张、眉毛上提／强＝整张脸舒展开——脸颊上顶到眼睛半闭成带皱的弧、嘴大张头后仰、眉毛飞扬、整个人静不下来

---

### 3.25 情绪库使用速查（跨情绪对照）

> ⚠️ **用情绪库前必读的三条口径**——缺一条就会踩本文其他章节的硬规则：
>
> 1. **中 / 强档是「完整面部配置」，不是「一个节拍」。** 强档常同时列到 4 个区域（如 §3.3 悲伤：眉 + 上眼睑 + 嘴角 + 下唇）。**不要整段丢进一个节拍**，须按 §5.3 拆成多拍，**每拍 ≤2 区**（§5.3 规则 3）。
> 2. **强档里的大幅形变禁大特写。** 崩溃（§3.23）、狂喜（§3.24）、愤怒爆发（§3.1 强）属大幅形变，**大特写必崩**，改中近景（§7.1 / §9.3）。
> 3. **例句默认按中小景别写。** 凡含视线方向变化的，大特写下改为 `gaze held level, one slow blink`（§4.3.2）。

| 想写 | 别用情绪词，用这个最小写法 |
|---|---|
| 「强装镇定」 | `her face holds perfectly still while her fingers pick at the seam of her sleeve` |
| 「强颜欢笑」 | `her mouth curves up while her eyes stay flat and unfocused` |
| 「由惊转怒」 | `first her brows fly up, then they crash down and inward, then her jaw tightens` |
| 「由怒转绝望」 | `first her jaw clenches, then it releases, then her shoulders collapse and her gaze goes flat` |
| 「忍了很久终于说出口」 | `her lips press into a thin white line, then she draws one deep breath, then her jaw unclenches and she speaks` |
| 「被戳中心事」 | `her gaze locks for a moment, then her blink rate picks up, then she looks down` |
| 「认出某人」 | `first her brows lift, then her eyes widen, then her lips part and her breath catches` |
| 「话到嘴边又咽回去」 | `her lips part, then she presses them together, then she swallows once` |
| 「不敢相信」 | `her brows draw together and lift at the same time, her head tilts slightly, her gaze stays on his face` |
| 「嘴上服软心不甘」 | `one corner of her mouth lifts while her jaw stays tight` |

---

## 4. 眼睛动作专章

> 【主模板 §6.4-B】**眼睛动作：单独指定，这是情绪的第一载体。**
> 范例：`she blinks once, then slowly raises her chin, then her gaze lifts to a fixed point beyond the lens`

**为什么眼睛要单独写**：面部所有区域里，眼部的像素占比与对比度最高，是模型最容易"看见"的部分。一次眨眼就能让一个静止镜头活过来。

### 4.1 眨眼 Blink

| 写法 | 用途 | 风险 |
|---|---|---|
| `she blinks once` | 最稳。**几乎任何镜头都能加** | 低 |
| `she blinks slowly` | 疲惫、放松、麻木 | 低 |
| `her eyes close for a full second and reopen` | 释然、隐忍、绝望 | 低中 |
| `she holds her eyes open without blinking` | 紧张、傲慢、锁定目标 | 低中 |
| `she blinks rapidly` | 心虚、紧张 | 中 |
| `her blink rate picks up` | 心虚（不写具体次数，写"变快"） | 中 |

**写法要点**：

1. **写次数，不写频率** —— `she blinks once` ✅ ／ `she blinks at 20 blinks per minute` ❌（模型没有时间计量）
2. **`blinks once` 是万金油** —— 任何需要"让静止的脸活起来"的镜头，加一句 `she blinks once` 都不会错
3. 【待验证】`she blinks three times` 这类**多次眨眼** H3 是否稳定复现次数。**实测方法**：同一提示词只改眨眼次数，各生成 10 条，统计实际次数分布。**未实测前不要靠眨眼次数传递信息。**

> **不眨眼的妙用**：`she holds her eyes open, unblinking, for the entire shot` 能制造极强的压迫感，且**跨帧极其稳定**（静态 = 低风险）。是大特写的好搭档。

### 4.2 眼睛稳定器句（复制即用）

来自 `衔接镜类型库_12列风险表单.md` #4 眼神镜的已验证写法：

```
both eyes open and symmetrical, pupils centered and equal size, steady gaze, no eye movement
```

**用法**：放在大特写 / 面部特写镜头的**正向状态描述之后**，作为正向锚定。它是「占据描述位」的稳定器，不是表演指令。

### 4.3 视线方向 Gaze direction

| 想表达 | 英文写法 | 风险 |
|---|---|---|
| 视线落定在某物 | `her gaze rests on the letter in her hands` | 低 |
| 视线垂下 | `her gaze drops to her hands and stays there` | 低中 |
| 视线抬起 | `her chin lifts and her gaze rises to a fixed point` | 中 |
| 视线保持平视 | `her gaze holds level` | **低** |
| 看向画外 | `her gaze rests on a point beyond the lens` | 中 |
| 看向画外（指定边） | `toward a point off-frame right` | 中 |
| 视线穿过对方 | `her gaze passes through him without landing` | 低中 |
| 视线追随 | `her head turns to follow him, her gaze stays on him` | 中 |
| **纯眼球转动** | ~~`her eyes move to the left`~~ | **高，禁用** |

#### 4.3.1 关键技巧：用「头 / 下巴」带动视线，不要写「眼球转动」

> **主模板 §9.3 的范例就是这么做的**：`her chin lifts and her gaze rises to a fixed point beyond the lens` —— 视线变化由**下巴抬起**承载，而不是写"眼球向上转"。

| ❌ 高风险 | ✅ 推荐 |
|---|---|
| `her eyes move to the left` | `she turns her head slightly to frame left, her gaze follows` |
| `her eyes dart around` | `her head turns from side to side, her gaze sweeping the room` |
| `her gaze rises` | `her chin lifts and her gaze rises to a fixed point` |
| `she rolls her eyes` | `she tips her head back and looks down the line of her nose` |

**为什么**：头 / 下巴是一个**大尺度的刚体运动**，模型容易生成；眼球是**小尺度的局部形变**，模型容易生成歪斜或不对称。

⚠️ **两个必须同时遵守的限定**（缺一个就翻车）：

1. **用画面方位，不用角色左右**（§4.3.3）——`frame left` 不是 `her left`。上表首行曾写作 `to the left`，与 §4.3.3 自相矛盾，已修正。
2. **大特写禁用本表**（§4.3.2）——本表所有替换项都**含视线方向变化**，只适用于**中近景 / 近景**。大特写（2–3 秒）应写 `gaze held level, one slow blink`，**不要套用本表**。

#### 4.3.2 ⚠️ 视线方向变化是高风险指令

> 来源：`衔接镜类型库_12列风险表单.md` #4 眼神/面部反应镜（风险 `I`+`B`，**中高**，处置＝规避）：
> 「① **不写眼神方向变化**（"抬眼看向画外"是高风险指令），改为 `gaze held level, one slow blink`；② 加 `both eyes open and symmetrical, pupils centered and equal size, steady gaze, no eye movement`；③ **大特写不承载情绪转折表演**，情绪转折放中近景，大特写只做静态凝视」

**与主模板 §9.3 的范例如何统一**？两者不冲突，区别在**景别与时长**：

| 条件 | 能不能写视线方向变化 |
|---|---|
| **大特写**（衔接镜 #4，2–3 秒） | ❌ **不能**。写 `gaze held level, one slow blink` |
| **中近景 / 近景**（B 主镜，≥3 秒，情绪转折） | ✅ **可以**，且主模板 §9.3 的 C 出镜正是这么写的（3.0s，特写（眼）） |
| 任何景别 | 优先用「头/下巴带动」而非「眼球转动」 |

**判断口诀**：**大特写静止，中小景别才动；动就动头，别只动眼。**

> ⚠️ **本条规则在本 skill 内优先级最高**：情绪库 §3、画外音 §6.1 等其他章节里的例句**默认按中小景别写**，其中凡含**视线方向变化**的（如 §3.22 麻木的 `her gaze drifts past him`、§6.1 的 `her gaze drifts`），**一旦镜头是大特写，一律替换为 `gaze held level, one slow blink`**。
> 这不是两处规则冲突，而是**同一条规则在不同景别下的两个取值**——例句给的是中小景别取值，大特写取值以本节为准。

#### 4.3.3 用画面方位，不用角色左右

> 【主模板 §6.4-C】**用画面方位表述，不用角色的左右。**
> ✅ `on the left third of frame` ❌ `on her left`

```
✅ her gaze rests on a point off-frame right
❌ she looks to her right
```

**理由**：「她的右边」有歧义（是她的右手边还是画面右边？），是左右翻转翻车的常见根因。

⚠️ **跨请求（跨生成）的左右方位一致属硬阻断**（主模板 §8.3）。若下一段要靠"她看向画外右侧"来接，**必须**把两段放进同一次请求，或用 FL2VA 把上段尾帧作下段首帧，或后期水平镜像。

#### ⚠️ 这条规则的边界：管「构图与跨镜一致性」，不管「单镜内的身体部位」

| 场景 | 写法 | 判定 |
|---|---|---|
| 人物/物体在画面里的位置 | ✅ `on the left third of frame` ❌ `on her left` | **用画面方位** |
| 视线朝向、镜头间要接的方位 | ✅ `toward a point off-frame right` ❌ `she looks to her right` | **用画面方位** |
| **单镜头内的身体部位** | ✅ `a single tear runs down her right cheek`、`her hair falls back over her left shoulder` | **用角色左右**，这是自然写法，不违规 |

**唯一例外**：若人物锁定块里有**不对称面部特征**（疤、痣、单边耳环），其左右**必须与锁定块逐字一致**——此时它不再是"单镜内的身体部位"，而是跨镜身份锚点，受 §8.3 硬阻断约束。

### 4.4 泪光与眼泪

**核心技巧**：泪光要写成**已存在的状态**，不要写成**生成过程**。

| ❌ 高风险 | ✅ 推荐 |
|---|---|
| `she starts to cry` | `her eyes are already glistening` |
| `tears form in her eyes` | `her eyes glisten, no tears fall` |
| `she begins to sob` | `a single tear runs down her right cheek` |
| `her eyes fill with tears` | `her eyes are brimmed and still` |

**为什么**：「从无到有」是一个需要较长时间的**过程**，2–3 秒的镜头装不下，模型会在中间帧生成半成型的眼泪或扭曲的眼部。**写成"已经是"，模型只需维持一个状态。**

**可靠写法清单**：

```
her eyes glisten but no tears fall
a single tear runs down her right cheek
her eyes are brimmed and still
her eyes are red-rimmed, her lashes wet
```

> 【待验证】`a tear runs down her cheek`（单滴泪水的轨迹）在 H3 上的可信度未实测。**实测方法**：5 秒中近景，只改这一句，生成 10 条，看泪痕位置是否稳定在脸颊上（而非穿过眼睛或消失）。**未实测前不承载叙事信息。**

### 4.5 对视与回避

| 情境 | 写法 |
|---|---|
| 直视对方 | `her gaze holds his` |
| 对视后移开 | `her gaze holds his for a moment, then slides away` |
| 回避特定人 | `her eyes slide away from his face and stay away` |
| 回避特定物 | `her gaze avoids the envelope on the desk` |
| 不敢抬眼 | `her eyelids lower, she cannot raise her eyes` |
| 视线穿过对方 | `her gaze passes straight through him` |
| 偷看 | `her gaze flicks to his face and away again` |

### 4.6 眼神在衔接镜中的用法（类型库 #4）

| 项目 | 规格 |
|---|---|
| 类型 | #4 眼神 / 面部反应镜 |
| 适用情境 | 反转瞬间、情绪转折 |
| 景别 | **大特写（眼）**（叙事侧另有「中近景」的建议，见下） |
| 运镜 | 极缓推（Push In，small amplitude / slow speed） |
| 对齐方式 | **视线匹配**：人物看向画外 → 下镜即其所见 |
| 风险 | `I`（身份漂移）+ `B`（肢体结构），**中高** |
| 处置 | **规避** |
| 备选方案 | 大特写**只承载静态凝视**（眨眼 / 微转头 / 平视保持）。**禁止用大特写演情绪转折**，反转瞬间改中近景。避开「缓缓抬眼看向画外」 |

**可直接复制的眼神镜模板（静态版，安全）**：

```
A large close-up frames her face centred in frame, her gaze held level.
Both eyes open and symmetrical, pupils centred and equal size.
First she blinks once, then her jaw tightens, then her gaze stays fixed straight ahead.
Her hair falls back over her left shoulder; the key light holds steady on her cheek.
The camera pushes in with small amplitude at slow speed.
By the end of the shot her gaze is still level, unblinking.
```

**可直接复制的眼神镜模板（转折版，中近景，≥3 秒）**：

```
[Shot 3] At 00:12.000, the shot switches to a medium close-up of the same woman's face
in three-quarter view, filling the right two thirds of frame. First her gaze drops to the
letter, then she blinks once, then her jaw tightens and her eyebrows draw together, then
her chin lifts and her gaze rises to a fixed point beyond the lens. Both eyes open and
symmetrical, pupils centred and equal size. Her hair slides off her shoulder with the turn,
and the window light forms a steady highlight band across her cheekbone. The camera holds
a static shot. By the end of the shot her gaze rests on a point off-frame right, level and
unblinking. Do not change her facial identity.
```

---

## 5. 微表情与短镜头

### 5.1 一个镜头能装多少表情变化

**经验规则**（【推断】，基于"变化越快越多、跨帧不一致风险越高"这一通用规律）：

> **一个镜头内，同时变化的面部区域不超过 2 个；串行变化的节拍数按时长决定。**

| 时长 | 可承载节拍数 | 说明 |
|---|---|---|
| **1.5s**（硬下限） | **1 个** | 只够一个动作。例：`she blinks once` |
| **2.0–3.0s** | **2 个** | 一个眼睑动作 + 一个口部动作，或一次头部动作 + 一次眼睑动作 |
| **≥3.0s**（承载信息镜） | **3 个** | **`First ... then ... finally ...`** 的完整三段 |
| **≥5.0s** | 3 个 + 1 个收尾状态 | 情绪转折的标准配置 |

> **为什么情绪转折要 ≥3 秒**：情绪转折的本质是**状态的改变**，至少需要「起始态 → 变化 → 终态」三个节拍。2 秒装不下三段，硬塞的结果是突变或中间帧扭曲。

### 5.2 微表情的时序写法

**用 `First ... then ... finally ...` 串联，禁用 `while`。**

> 【主模板 §6.4-B / 防翻车词库 §5】**用 `then` 串联动作，禁用 `while` 并发。**
> 【防翻车词库 §补充勘误】"Without them the model has to guess whether your three described events happen in sequence or simultaneously, and it **usually picks simultaneously**."

| 模板 | 适用 |
|---|---|
| `First A, then B.` | 2.0–3.0s |
| `First A, then B, then C.` | ≥3.0s |
| `First A, then B, finally C.` | ≥5.0s，强调终点 |

**写表情时序的三条规则**：

1. **按面部区域从上到下排**：眉 → 眼 → 鼻 → 唇 → 下颌 → 颈/肩。符合真实肌肉扩散方向，生成更自然
2. **每个节拍给明确终点**：`then her jaw tightens` → `then her jaw tightens until the muscle at her jaw angle bulges`
3. **一拍内最多 2 个区域，且用 `and` 不用 `while`**：

| 写法 | 判定 |
|---|---|
| ❌ `her brows draw together while her jaw tightens` | **`while` 显式标记并发**，模型会真的同时做两件事 → 崩 |
| ✅ `first her brows draw together, then her jaw tightens` | 拆成两拍（推荐） |
| ✅ `then her jaw tightens and her eyebrows draw together` | **合并为一拍，`and` 并联，上限 2 区**（模板 D 第三拍即此写法） |
| ❌ 3 个及以上区域用 `and` 串联 | 全脸同时抖，必须砍到 2 区 |

> ⚠️ **禁用的是 `while` 这个并发标记，不是"两个区域"这件事**。措辞若写成"不要写两个区域同时变"，会与本文模板 D 自相矛盾——模板 D 的第三拍正是两个区域 `and` 并联。

**「主体动作」vs「次级运动」的判定**——这是 `while` / `as` 禁用的**唯一判据**，必须能判别：

| 判据 | 主体动作（❌ 禁 `while`） | 次级运动 / 瞬时事件（✅ 可并行） |
|---|---|---|
| **要不要模型构造身体结构** | **要**——需摆姿势、转重心、动手、走位 | **不要**——眨眼、呼吸、吞咽、发丝、衣摆、声光、热气 |
| 例 | ❌ `She sips while waving`、❌ `He stands up while speaking` | ✅ `As she speaks, she blinks once`、✅ `Her coat sways as she walks` |

> **口诀**（口径与 `h3-action-body` §1.3 一致）：**要摆姿势的 = 主体动作；不摆姿势的 = 次级运动。**
> ⚠️ 面部微动作（眨眼、吞咽、嘴角微动）**归次级运动**——它们不争夺解剖结构资源，因此 `As she speaks, she blinks once` 合法。

### 5.3 可直接复制的微表情模板

**模板 A：2 秒「一个念头闪过」**

```
First she blinks once, then her jaw tightens.
```

**模板 B：3 秒「由听到、到反应」**

```
First her brows lift, then her gaze drops to her hands, then her lips press into a thin line.
```

**模板 C：3 秒「忍住」**

```
First her lips press into a thin white line, then she draws one deep breath through her nose
and holds it, then her eyelids lower to hide her eyes.
```

**模板 D：5 秒「决定」（主模板 §9.3 同款结构）**

```
First her gaze drops to the letter, then she blinks once, then her jaw tightens and her
eyebrows draw together, then her chin lifts and her gaze rises to a fixed point beyond the lens.
```

**模板 E：2 秒「强装无事」**

```
Her face holds perfectly still, her gaze held level; she blinks once.
```

**模板 F：3 秒「被戳中心事」**

```
First her gaze locks for a moment, then her blink rate picks up, then her gaze drops to her
hands and stays there.
```

### 5.4 短镜头里不该写什么

| ❌ 别在 ≤3 秒的镜头里写 | 原因 |
|---|---|
| 完整的"从无到有"过程（哭出来、笑出来、眼泪形成） | 过程需要时间，短镜会生成半成型状态 |
| 3 个以上面部区域同时变化 | 模型会"平均"成抖动 |
| 情绪的**两次**转折（先笑后哭） | 至少需 5 秒，且崩脸风险高 |
| 快速连续的表情切换 | 跨帧跳变 |
| `her expression changes` | 无信息，且诱导随机变化 |

---

## 6. 表情与动作 / 台词的配合

### 6.1 三元一致性校验

一个镜头里，**表情 / 肢体动作 / 台词**三者必须指向同一个状态。任何一个不一致，观众立刻出戏。

| 校验项 | 检查什么 | 不一致的后果 |
|---|---|---|
| **表情 ↔ 台词** | 说了台词 → 嘴部必须有动作；没说 → `her lips remain closed` | 说话时嘴不动 / 不说话时嘴乱动 |
| **表情 ↔ 语气** | 语气描述（`<d>` 标签外）与表情一致 | 内容是狠话、表情在笑 |
| **表情 ↔ 肢体** | 面部与肩/手/呼吸同向 | 脸在笑、手在攥拳，读出精神分裂 |

> **表情 ↔ 肢体的具体对照**（哪一档表情该配什么肩/手/重心）属动作侧内容，见 `h3-action-body` §10.1 **三元一致性校验表**（在该节第 16 条之后），此处不重复维护。
> **不一致时的处置优先级：改动作，不要改表情**——表情是情绪的第一载体，优先级更高。
| **表情 ↔ 画外音** | 画外音时**画面人物必须闭嘴** | 口型与旁白打架 |

**台词侧的官方写法**（【官方】base-en.txt）：

```
Place the speaker's identifying phrase, ID, action, and delivery outside <d>.
Inside <d>, include only the language tag and the actual user-provided spoken content.
```

```
✅ The woman with a low, steady voice at a measured pace (S1) says: <d>[Chinese] 陈总，这份合同我一个字都不会改。</d>
❌ (S1) says angrily: <d>[Chinese] 我很生气</d>
```

**关键**：语气词（`with a low, steady voice`、`at a measured pace`）**在 `<d>` 外面**，它和表情描述同属"表演层"，**两者必须一致**。

| 表情 | 配套的语气写法（放 `<d>` 外） |
|---|---|
| 隐忍 | `with a tight, controlled voice at a slow pace` |
| 愤怒（压制） | `with a low, hard voice, each word separated` |
| 愤怒（爆发） | `in a raised voice at a fast pace` |
| 心虚 | `with a hesitant, breathy voice, trailing off` |
| 决绝 | `with a level, unhurried voice` |
| 讨好 | `in a bright, quick voice` |

**画外音的强制写法**（【官方】原文）：

```
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d>
while his lips remain completely closed.
```

> 画外音时，画面中的人物**不能说话**，所以表情要写成"沉默的表演"。**按景别分两种写法**：
>
> | 景别 | 写法 |
> |---|---|
> | **中近景 / 近景**（回忆旁白：看着照片、望向窗外） | `her lips remain closed, her gaze drifts, her fingers stop moving` |
> | **大特写**（内心独白：角色特写） | `her lips remain closed, her gaze holds level, she blinks once`（**不写 `gaze drifts`**，见 §4.3.2） |

### 6.2 表情抢戏 vs 表情不足

| 问题 | 症状 | 修正 |
|---|---|---|
| **表情抢戏** | 台词很平，脸却在大哭；观众只看到"演"，看不到"事" | 降一个强度档（强 → 中），或把表情挪到肢体（沉肩、停手） |
| **表情不足** | 说了"我恨你"，脸毫无变化 | 补一个最小表情：`her jaw tightens` 或 `one corner of her mouth presses flat` |
| **表情与景别不匹配** | 中景里写 `her lower lip trembles`（拍不到） | 见 §7.1 景别承载量表 |
| **表情没有时间演** | 3 秒里塞了 4 个节拍 | 砍到 2–3 个，见 §5.1 |

**修正口诀**：**抢戏就降档或挪到身上，不足就补一个下颌动作。**

> `her jaw tightens` 是"表情不足"的万能补丁——幅度小、任何景别都成立、不抢戏。

### 6.3 表情与对白的时序排布

**不要在同一时刻给表情和台词。** 观众需要时间分别接收。

| 排布 | 写法 | 效果 |
|---|---|---|
| **先表情后台词**（推荐） | `First her jaw tightens and her eyebrows draw together, then she says: <d>...</d>` | 观众先读到情绪，再听到内容 |
| **先台词后表情**（反转常用） | `She says: <d>...</d>, then her smile stays on her mouth while her eyes go flat` | 台词后的表情是"真实反应" |
| **台词中插入一次眨眼** | `As she speaks, she blinks once` | 让说话的脸活起来（用 `as she speaks` 是允许的，因为它不是两个动作并发） |

> ⚠️ `As she speaks, she blinks once` 中的 `as` **不属于禁用范围**。禁的是 `while` 把两个**主体动作**并联（如 `She sips while waving`）。眨眼是次级运动，可以并行。
> 「主体动作 / 次级运动」怎么分 → **见 §5.3 的判定表**（口诀：要摆姿势的 = 主体动作）。

---

## 7. 面部特写的技术要点

### 7.1 景别承载量表

**经验规则**（【推断】，基于"像素占比越大、形变越明显"）：

| 景别 | 英文 | 能看清什么 | 能承载的表情强度 |
|---|---|---|---|
| 远景 / 全景 | Wide / Full | 只有肢体与姿态 | 只能靠**肢体**（沉肩、停步、握拳） |
| 中景 | Medium | 头肩姿态、大幅度表情 | 弱–中；`her shoulders slump` ✅ ／ `her lower lip trembles` ❌ |
| **中近景** | **Medium Close-Up** | 完整表情 | **中–强。情绪转折的最佳景别** |
| 近景 / 特写 | Close-Up | 眉眼口全部细节 | 中；避免大幅形变 |
| **大特写** | **Large / Extreme Close-Up** | 只有眼睛或局部 | **只做静态凝视**（眨眼 / 平视 / 微转头）。**禁止情绪转折** |

> 【衔接镜类型库 #4】**大特写不承载情绪转折表演，情绪转折放中近景。**

**判断口诀**：**转折去中近景，凝视去大特写。**

### 7.2 大特写的三类风险

| 风险 | 表现 | 规避 |
|---|---|---|
| **皮肤细节失控** | 毛孔、斑点、纹路逐帧生长变化；出现原角色没有的痣 | 锁定块写 `natural skin texture, no moles or marks on the face`；加 `skin texture remains identical from the first frame to the last` |
| **五官不对称 / 崩脸** | 两眼大小不一、嘴歪、鼻梁歪斜、面部比例中途变化 | 加稳定器句 `both eyes open and symmetrical, pupils centred and equal size`；避免大幅表情 |
| **身份漂移** | 大特写下"不像同一个人" | 走参考图（I2VA / FL2VA / Ref2VA）；**Verbatim Rule** 描述串逐字复制 |

**大特写的必备三件套**：

```
① 稳定器句：both eyes open and symmetrical, pupils centred and equal size, steady gaze
② 静态表演：her gaze held level, she blinks once（不写大幅表情）
③ 收边：Do not change her facial identity.（每镜最多 1 句，前面必须有正向描述）
```

### 7.3 光位与面部表现力

> **前提**：光位由**共用锁定块**统一规定，三镜逐字一致（主模板 §6.3）。
> 【防翻车词库 §7】**光照方向全程单一主光，主光换边身份就会晃。**

**光位不是"美容选项"，它是身份一致性的一部分。** 在任何镜头里改光位，都会连带影响身份稳定。

| 光位 | 英文写法 | 面部效果【业界】 | H3 风险【推断】 |
|---|---|---|---|
| 前侧光 45° | `a single soft key light from the upper right front` | 立体、自然，最通用 | 低（主模板锁定块用的就是这一档） |
| 侧光 | `a key light from camera left, raking across her face` | 明暗对比强，显硬朗、藏一半脸 | 中（半张脸在暗部，细节易糊） |
| 逆光 / 轮廓光 | `backlit, a rim light separates her from the background` | 边缘发亮，脸部偏暗 | 中高（脸部细节不足，身份易漂） |
| 底光 | `a cool glow from below lights her chin` | 阴森、诡异 | 高（非自然光照，模型生成不稳定） |
| 顶光 | `a hard light from directly above` | 眼窝阴影，压抑 | 中（眼窝阴影可能吃掉眼部动作） |

**可直接复制的光位差异写法**（主模板 §6.1 段⑥要求"写本镜与锁定块的差异，无差异就写一致"）：

```
✅ Lighting matches the lock block exactly.
✅ Lighting matches the lock block exactly, with the window light remaining the only source.
❌ dramatic lighting, moody atmosphere（情绪词，且无光位信息）
```

**与表情配合的一条实用建议**：**表情的动作区域，要落在有光的一侧。**

```
✅ a single soft key light from the upper right front; her jaw tightens and the muscle
   bulges in the light
❌ 光从左侧来，却写右侧下颌的动作（暗部里看不出）
```

### 7.4 大特写的次级运动（防恐怖谷）

**静态大特写 + 无次级运动 = 恐怖谷。** 必须给一处微小的"活气"：

| 次级运动 | 写法 |
|---|---|
| 眨眼（首选） | `she blinks once` |
| 呼吸 | `her shoulders rise and fall once with a slow breath` |
| 发丝 | `a strand of hair shifts across her temple` |
| 光影 | `the window light holds a steady bright patch across her cheekbone` |
| 衣摆 | `the collar of her coat shifts slightly` |

> **注意**：次级运动要**恒定**，不要写变化。`the light holds steady` ✅ ／ `the light flickers` ❌（闪烁是翻车项）。

---

## 8. 年龄 / 性别 / 性格的表情差异

> ⚠️ 本节是**表演设计选择**，不是生理断言。同一情绪在不同角色身上幅度不同，这是**角色设定**，不是男女老少的刻板印象。

### 8.1 年龄

| 年龄段 | 幅度 | 持续时间 | 转换速度 | 写法要点 |
|---|---|---|---|---|
| **儿童** | 大 | 短 | 快 | 表情切换快、全身参与（不只是脸）。`her whole face scrunches up, then it clears all at once` |
| **青年** | 中 | 中 | 中 | 本 skill §3 默认档 |
| **中老年** | 小 | 长 | 慢 | 靠**眼周与口周的纹路**承载，不靠肌肉幅度 |

**老年角色的正确写法**：

```
✅ the lines around her eyes deepen, her eyelids lower, her mouth holds a flat line
✅ her cheeks hollow slightly as her jaw sets
❌ she looks old / an elderly expression
```

> **原理**：年龄的视觉信号是**纹路与皮肤松弛**，不是"表情幅度小"。写纹路变化比写"幅度小"有效得多。

### 8.2 性格（这是本节最有用的一节）

**同一个角色，全剧的表情幅度必须一致。** 这是角色一致性的一部分，不是可有可无的风格。

| 表演基线 | 特征 | 幅度 | 速度 | 示例 |
|---|---|---|---|---|
| **外放型** | 情绪写在脸上，藏不住 | 大 | 快 | `her whole face opens up — brows fly up, mouth opens wide` |
| **内敛型** | 情绪压在眼与下颌，嘴不动 | 小 | 慢 | `her jaw tightens, her eyelids lower; her mouth stays still` |
| **控制型** | 只在独处时露出，有人时归零 | 两档切换 | 突兀 | `first her face holds perfectly still, then, alone, her brows knot and her shoulders drop` |
| **表演型** | 表情是工具，可随意切换 | 大但不真 | 快 | `her mouth curves up while her eyes stay flat` |

**必须写进角色卡**（主模板 §5.1 已有此字段）：

```markdown
### 外观
- 标志性表情：（写死 1 条英文描述串，全剧复用）
  > 例：`her jaw tightens and her eyelids lower; her mouth stays still`
### 行为锚点
- 专属小动作：（推眼镜 / 捏衣角 / 抿唇）
```

> **「标志性表情」是角色的表情基线**——它决定了这个角色在 §3 对照库里默认取哪一档。**内敛型角色永远取「弱」或「中」，只有崩溃时才取「强」。** 这条不写进角色卡，同一角色在不同集里会演成两个人。

### 8.3 性别

**不要按性别套模板。** 性别不决定表情幅度，**角色设定**才决定。

需要写的只有一条：**该角色的表演基线**（见 §8.2），进角色卡，与性别无关。

> **一个反例**：写「女性角色必须温婉含蓄」会让所有女性角色演成同一个人。**正确的做法是给每个角色一条独立的标志性表情描述串。**

### 8.4 表情基线与参考图

**主模板 §5.1 角色卡已有字段**：

```markdown
### 参考图集
- 正面定妆图：IMG__　侧面：IMG__　全身：IMG__　**表情集：IMG__ / IMG__**
```

**建议**：给每个主要角色出 **2 张表情参考图**（一张中性、一张该角色的标志性表情），在需要强表情的段落走 I2VA 首帧。

> 【推断，需实测】表情参考图对表情一致性的提升幅度未量化。**实测方法**：同一提示词，一组用中性定妆图作首帧、一组用表情图作首帧，各生成 10 条，盲评表情到位率。

---

## 9. 常见翻车与规避

### 9.1 表情突变（跨帧跳变）

| 症状 | 脸在两帧之间突然从 A 状态跳到 B 状态，中间没有过渡 |
|---|---|
| 成因 | 写了"状态"没写"过程"；或节拍数超出时长承载量 |
| 规避 | ① 写过程动词（`tightens` 而非 `is tight`）② 用 `First ... then ...` 明序 ③ 按 §5.1 控制节拍数 ④ 每个节拍给终点 |

### 9.2 恐怖谷

| 症状 | 大特写下脸"像人但不是人"：皮肤过于光滑、眼神空洞、微动作缺失 |
|---|---|
| 成因 | 静态 + 无次级运动 + 过度写实的皮肤 |
| 规避 | ① 加一次眨眼 `she blinks once` ② 加次级运动（呼吸 / 发丝 / 衣领）③ 加 `natural skin texture, light film grain` ④ **降景别到中近景** |

### 9.3 五官扭曲（崩脸）

| 症状 | 嘴歪、两眼不对称、鼻梁歪斜、面部比例中途变化 |
|---|---|
| 成因 | 大特写 + 大幅表情（尤其"崩溃"档） |
| 规避 | ① **大幅表情绝不放大特写**（改中近景）② 加稳定器句 `both eyes open and symmetrical, pupils centred and equal size` ③ 用「隐忍」替代「崩溃」④ 走参考图锁脸 |

### 9.4 情绪与台词不符

| 症状 | 说"我没事"，脸在哭；或说狠话，脸在笑（非有意为之） |
|---|---|
| 成因 | 表情描述与 `<d>` 外的语气描述分头写的，没有对齐 |
| 规避 | 跑 §6.1 三元一致性校验；语气词与表情**同一段写、一起审** |

### 9.5 表情与光位矛盾

| 症状 | 表情动作落在暗部，看不出来；或光位一变，脸也变了 |
|---|---|
| 成因 | 光位改了但锁定块没改；或没考虑光位与动作区域的关系 |
| 规避 | ① 光位严格走锁定块，三镜逐字一致 ② 表情动作区域落在有光的一侧 ③ 单一主光，不换边 |

### 9.6 「从无到有」的过程类表情

| 症状 | 眼泪形成到一半卡住；笑容展开到一半扭曲 |
|---|---|
| 成因 | 过程需要时间，短镜装不下 |
| 规避 | **写成"已经是"，不写"变成"**（见 §4.4） |

### 9.7 ⚠️ 最容易误判的一条：采样步数（NFE）伪翻车

> 【主模板 §8.4】**很多看起来像"提示词写错了"的问题，其实是采样步数太低。**
> 官方口径：*"人物动作散架或音画对不上时，第一件该怀疑的是步数太低，不是 prompt 写错。"*

| 场景 | 步数 |
|---|---|
| 试拍 / 快速验证 | 4 步 |
| 出片 | **6–8 步** |

**表情崩了的返工顺序**：

```
【第 0 步 · 零成本，读提示词就能查，不用生成】设计校验
  大特写里写了情绪转折？2 秒镜里塞了 3 拍以上？一个镜里 3 个面部区域同时变？
    ↓ 是 → 这是设计错误，抬步数只会得到「高清版的错误」。先改设计。
    ↓ 不是
① 采样步数是不是 4？→ 抬到 6–8，重生成一次
    ↓ 还是崩
② 崩脸 / 恐怖谷 / 五官扭曲？→ 按 §9.2 / §9.3 降景别、降强度、加稳定器句
    ↓ 不是
③ 最后才改提示词（砍节拍、换强度档）
```

**为什么第 0 步排在抬步数之前**：主模板 §8.4 的「先怀疑步数」说的是**生成后看片阶段**；而设计校验属**生成前内容检查**（§8.2），本来就排在前面，而且**零成本**——不用生成、不用等。

**哪些表情崩坏抬步数救不了**（这张表决定首查项）：

| 症状 | 根因 | 首查项 | 抬步数有用吗 |
|---|---|---|---|
| 大特写下五官扭曲 / 崩脸 | 大特写承载了情绪转折（**设计错误**） | **改景别到中近景**（§7.1） | ❌ 无效，只会崩得更清晰 |
| 2 秒镜里表情跳变 | 节拍数超承载量（§5.1） | **砍到 2 拍，或加时长** | ❌ 无效 |
| 全脸同时抖 | 一拍内 3 个以上面部区域同时变 | **砍到 2 区**（§5.3 规则 3） | ❌ 无效 |
| 视线没落点 / 眼神游移 | 一个镜里出现多个注视锚点 | **只留一个落点**（§4.3） | ❌ 无效 |
| 眨眼抽搐 / 高频眨眼 | 一个镜里写了 2 次以上眨眼 | **砍到 1 次**（§4.1） | ❌ 无效 |
| **恐怖谷（静态僵脸）** | 缺次级运动（§7.4） | **加眨眼 / 呼吸 / 发丝** | ⚠️ **可能更糟**【推断】 |
| 五官不对称 / 大小眼 | 概率性 | 稳定器句 + 参考图（§7.2） | ✅ 有用 |
| 皮肤细节逐帧生长 | 概率性纹理漂移 | 锁定块加 `skin texture remains identical from the first frame to the last` | ✅ 有用 |
| 脸「不像本人」 | 身份漂移 | 光位不换边 + 锁定块逐字一致 + 参考图 | ✅ 部分有用 |

> **本表的边界**：本表只回答「这一类崩坏该不该抬步数」。**表情类设计错误的完整逐条处置见 §9.1–9.6**（突变 / 恐怖谷 / 崩脸 / 与台词不符 / 与光位矛盾 / 过程类表情），本表不重复。若你引用本表做首查项，**请连 §9.1–9.6 一起引用**。

> ⚠️ **恐怖谷是唯一一项「抬步数可能让它更糟」的**【推断】：步数越高，皮肤细节越清晰，一张**完全静止、无眨眼无呼吸**的脸就越显假。
> **实测方法**：同一张静态大特写，4 步与 8 步各生成 5 条，盲评「像不像活人」。若 8 步评分更低，则该项不适用「先抬步数」。
> **未实测前的处置**：静态大特写**先加 `she blinks once`**，再考虑抬步数。

> **步数一直是 4 却反复改表情描述，是纯浪费**——你改的每一版都是在低质量采样下评估的，结论不可靠。**但设计错误也一样：先确认不是设计错误，再抬步数。**

### 9.8 其他规避速查

| 翻车 | 规避 |
|---|---|
| 说话时嘴不动 | 有台词 → 必须写口部动作；无台词 → `her lips remain closed` |
| 画外音时人物跟着动嘴 | 用官方成对写法：`says in an off-screen voiceover ... while his lips remain completely closed.` |
| 大特写下"不像本人" | 走参考图；描述串 Verbatim Rule 逐字复制；`Do not change her facial identity.` |
| 表情把身份带漂了 | 单一主光不换边；锁定块逐字一致；降低表情强度 |
| 眨眼不对称/单眼眨 | 加稳定器 `both eyes open and symmetrical`；写 `she blinks once` 不写 `she winks` |
| 眼泪位置乱跑 | 改静态写法 `her eyes glisten but no tears fall`（见 §4.4，【待验证】） |
| 情绪转折没演出来 | 检查是不是景别太小（中景拍不到唇部动作）或时长不够（<3 秒） |

---

## 10. 检查清单与速查表

### 10.1 表情描写提交前 10 条

```
□ 1. 没有情绪名词（sad / angry / guilty / determined ... 一个都没有）
□ 2. 每个表情都写成了可见动作，且是「过程动词」（tightens 不是 is tight）
□ 3. 每个动作都有明确终点（until / to a fixed point / and stays there）
□ 4. 用 First ... then ... finally 串联，无 while
□ 5. 一个镜头内同时变化的面部区域 ≤ 2 个
□ 6. 节拍数符合时长承载量（1.5s→1 / 2–3s→2 / ≥3s→3）
□ 7. 大特写没有承载情绪转折（只做静态凝视）；情绪转折在 ≥3 秒的中近景
□ 8. 视线方向变化由「头 / 下巴」承载，没写纯眼球转动；用的是画面方位不是角色左右
□ 9. 表情 / 肢体 / 台词（含 <d> 外的语气词）三者一致；无台词处写了 lips remain closed
□ 10. 大特写 / 面部特写已加稳定器句：both eyes open and symmetrical, pupils centred and equal size
```

### 10.2 景别 / 时长 / 表情强度 决策表

| 条件 | 景别 | 时长 | 表情强度 | 可写内容 |
|---|---|---|---|---|
| 大特写，衔接镜 #4 | **Large Close-Up** | 2–3s | **静态** | 眨眼 1 次、平视保持、微转头。**不写转折、不写视线方向变化** |
| 特写，情绪转折 | Close-Up | ≥3s | 中 | 眉 + 眼 + 下颌，2–3 节拍 |
| **中近景，情绪转折**（推荐） | **Medium Close-Up** | **≥3s，建议 5s+** | **中–强** | 完整三段式 `First ... then ... finally ...` |
| 中景，常规 | Medium | 任意 | 弱–中 | 主要靠肩 / 手 / 呼吸，面部只写大幅变化 |
| 全景 / 远景 | Wide / Full | 任意 | — | **只写肢体**：沉肩、停步、转身、握拳 |

### 10.3 正反例速查表（一页版）

| ❌ 不要写 | 原因 | ✅ 改写 |
|---|---|---|
| `she looks angry` | 情绪名词 | `her brows draw together and lower, her jaw tightens` |
| `tears form in her eyes` | 从无到有的过程 | `her eyes are already glistening, no tears fall` |
| `her eyes move to the left` | 纯眼球转动 + 角色左右 | `she turns her head slightly to frame left, her gaze follows`（中小景别；**大特写改 `gaze held level, one slow blink`**） |
| `her eyes widen in shock` | 情绪副词 | `her brows fly up, her eyes open wide, her jaw drops open` |
| 大特写里写 `her face folds in on itself` | 大幅形变 + 大特写 = 崩脸 | 改中近景；或降为 `her jaw tightens, her eyes close for a full second` |
| 2 秒镜里写 4 个节拍 | 超出承载量 | 砍到 2 个 |
| `she smiles while her jaw tightens` | while 并发 | `first her mouth curves up, then her jaw tightens` |
| `she looks to her right` | 角色左右，有歧义 | `toward a point off-frame right` |
| 说台词却不写嘴部动作 | 三元不一致 | 补 `her lips part and she speaks` |
| 画外音却让人物张嘴 | 口型打架 | `... while his lips remain completely closed.` |
| `her pupils dilate` | 【待验证】，不可靠 | 删掉；改用 `her eyes open wide` 或 `her gaze locks on` |
| `dramatic emotional lighting` | 情绪词 + 无光位信息 | `a single soft key light from the upper right front` |

### 10.4 万能补丁句（任何镜头都能加）

```
让静止的脸活起来：      she blinks once
表情不够，最低成本补强：  her jaw tightens
需要情绪但不想要风险：    her shoulders drop away from her ears, she lets out a long breath
大特写防崩：            both eyes open and symmetrical, pupils centred and equal size,
                       steady gaze
收边（每镜最多 1 句）：   Do not change her facial identity.
```

---

## 附：本 skill 的【待验证】清单（可测，测完回填）

| # | 待验证项 | 实测方法 | 验证前怎么处理 |
|---|---|---|---|
| 1 | H3 是否忠实响应**眨眼次数**（`blinks once` vs `blinks three times`） | 单镜 5 秒，只改眨眼次数，各生成 10 条，统计实际次数分布 | 只写 `blinks once`，不靠次数传信息 |
| 2 | **瞳孔放大 / 缩小**（`pupils dilate`）是否可控 | 同一提示词只改瞳孔描述，生成 10 条，量瞳孔相对直径 | 不写；改用睁眼 / 眯眼 |
| 3 | **单滴泪水的轨迹**（`a tear runs down her cheek`）是否稳定 | 5 秒中近景，生成 10 条，看泪痕位置是否稳定在脸颊 | 用静态 `her eyes glisten but no tears fall` |
| 4 | **情绪强度档**（弱/中/强）在 H3 上是否呈现可分辨的梯度 | 同一情绪三档各生成 5 条，三人盲评排序 | 默认取「中」档；关键处用肢体动作补强 |
| 5 | **表情参考图**对表情一致性的提升幅度 | 中性定妆图 vs 表情图作首帧，各 10 条，盲评到位率 | 至少保留中性定妆图作首帧 |
| 6 | **H3 对具体面部区域词汇**（如 `inner brows`、`masseter`）的理解精度 | 同一情绪用「区域精确词」vs「通用词」各 10 条，盲评差异 | 优先用本 skill §2.2 动词库的写法 |

> **测试通用规范**：每次只改一处，改完全量重测（主模板 §10.3）。同一提示词固定种子，只变待测项。
