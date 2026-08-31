---
name: h3-antibug-check
description: 海螺 H3 提示词的防翻车限制词库与漏洞检查体系。含否定句正确写法、采样步数伪翻车识别、硬阻断清单、三类必查漏洞、处置四级枚举、提交前自检清单。触发词：H3防翻车、H3限制词、H3漏洞检查、H3多手指、H3镜头不流畅、H3语言错误、H3返工、H3采样步数。
agent_created: true
---

# H3 防翻车限制词库 · 漏洞检查 · 硬阻断识别

> 定位：流水线**第 6 步**（提示词写完、提交生成之前），以及与第 7 步（生成后看片）之间的双向闸门。
> 配套主模板：`MiniMaxH3-小说转分镜-完整模板.md` **模块八**。本文是模块八的执行细则与例句库。

## 用法

```
写完一段 15 秒 3 镜提示词
  ↓
① 跑 §13.1 结构检查（9 条，可脚本化）  ← 不过不许提交
  ↓
② 跑 §13.2 内容检查（9 类翻车，人工对照）
  ↓
③ 提交生成（出片步数 6–8）
  ↓
④ 跑 §13.3 看片清单（9 条）
  ↓
⑤ 有问题 → 先走 §2 步数 SOP，再走 §12 处置四级枚举
```

## 证据分级（本文严格执行）

| 标记 | 含义 |
|---|---|
| **【H3】** | MiniMax H3 官方规格（开放平台 API 文档 / GitHub `MiniMax-AI/MiniMax-H3` 内置 prompt-writing skill / HuggingFace 官方模型卡） |
| **【官·转述】** | 官方口径但经第三方或团队转述，未直接核对原文 |
| **【工艺】** | 模型无关的通用工艺规律，多代模型上均成立 |
| **【2.3】** | 仅在 Hailuo 2.3 上验证过，H3 上未确认，套用需谨慎 |
| **【推】** | 机制推断，无公开实测数字 |
| **【待验证】** | 无可靠出处，**必须实测后才能写进客户交付物** |
| **✗ 硬阻断** | 提示词解决不了，必须靠参考输入 / 后期 / 改分镜 |

> **铁律：不给"成功率 X%"这类假数字。** 网上"某模型珠宝保真度优异""加限制词后 X% 不崩"之类说法，来源多为聚合站与营销软文，无方法论、无测试集，**一律判定为不可引用**。

## H3 硬约束速查（本文所有检查项的判定基准）

| 项 | 官方值 |
|---|---|
| 提示词上限 | **7,000 字符**（按字符计，1 汉字 = 1 字符） |
| 时长 | API **4–15 秒整数**；本地部署 5–15 秒 |
| 帧率 / 分辨率 | 24 FPS；`768p` / `2K` |
| 音频 | 原生立体声 32 kHz，与画面同一次推理生成；对白 11 语言含中文 |
| 参考素材 | 图 ≤9、视频 ≤3、音频 ≤3，混合 **≤12 文件**；音频**不能单独输入** |
| 三核心字段 | 固定顺序 `integrated_multimodal_description` → `overall_soundscape` → `non_diegetic_music` |
| 时间戳 | Shot 1 **不加**；后续 `At 00:SS.mmm`（三位小数）；指令首行锚点 `S.SS`（两位小数） |
| 对白 | 必须包在 `<d>...</d>` 内；标签内只放语言标签 + 原话 |
| 运镜 | **一镜一个运镜**；术语 + `with small/large amplitude` + `at slow/fast speed` |
| 模式互斥 | `first_frame`/`last_frame` 与 `reference_*` **不可同时出现** |
| FL2VA | 官方默认**单镜**，多镜需显式指定 |
| 每镜时长 | **硬下限 1.5 秒**，设计下限 2.0 秒，承载信息镜 ≥3.0 秒 |
| 负面提示词 | **未见 H3 官方 `negative_prompt` 参数**【待验证】——现有"无负向字段"的证据均出自 Hailuo 2.3，未获 H3 官方确认。处置口径见 §1.1（**不依赖该结论是否成立**） |

---

## 1. 否定句的正确写法（先读这一节，全篇基础）

### 1.1 裁定表（两套证据冲突后的稳妥结论）

| 写法 | 判定 | 机制 |
|---|---|---|
| 裸名词否定 `no six fingers, no extra limbs` | ❌ **禁用** | 名词本身进入条件分布，**反向激活**。arXiv:2508.10931（VSF）原文：*"a prompt like 'a scientist that is not wearing glasses' will usually generate a scientist with glasses, **even more frequently than a plain 'a scientist'**"* |
| 裸否定句 `do not generate six fingers` | ⚠️ 弱 | 模型必须先构想"六指"这个解，再否定它 |
| **正向锚定** `five fingers on each hand, fingers gently curved and held together` | ✅ **最强** | 直接占据描述位，畸形解无处安放 |
| **正向锚定 + 末尾一句 `Do not` 收边** | ✅ **H3 最优** | 正向给解，`do not` 只负责收边界 |

**为什么保留一句 `Do not`**：Flashloop 模型卡把 *"Reliable instruction following, including explicit negatives"* 列为 H3 特性；Morphed 41 条实测称 *"Adding one negative constraint per reference generation was the cheapest reliability fix in the whole set."* 无否约束时冒出的问题正是 extra people / extra products / **invented background text**。
**为什么不能多写**：H3 是否提供 `negative_prompt` 独立通道**未经官方确认**【待验证】——现有证据来自 Hailuo 2.3（fal.ai 参数对照表记 "Negative prompt: Not available"），**不排除 H3 有变化**。
但无论该字段存在与否，**否定句都要与正向句竞争同一段注意力预算**（若字段存在，长负向清单同样会稀释引导力）。堆满清单 = 把"avoid 预算"摊薄给几十个模糊概念，真正要禁的那条反而不生效。
→ 因此本节的三条硬规则在**两种假设下都成立，不依赖该结论**。

### 1.2 三条硬规则

```
1. 每条提示词最多 1 句 Do not ...
2. 该句置于该镜末尾
3. 该句之前必须先有对应的正向状态描述
4. 禁止成串裸名词否定（no X, no Y, no Z...）
5. 手部问题优先正向锚定；如需收边，`Do not` 句必须置于正向锚定之后，
   且不得写成裸名词否定（`no six fingers`）或无前置的否定句（`do not generate six fingers`）
```

> ⚠️ **第 5 条已修正**。旧表述「绝不写含 six fingers / extra fingers 字样的句子」**与 §1.4 正例冲突**，
> 已导致有 skill 据此废止「正向锚定 + 一句 `Do not` 收边」这一合法档位。
> **从严点在"有没有正向锚定前置"，不在"能不能提 extra fingers"**：
> - ❌ `do not generate six fingers`（无前置）/ `no six fingers`（裸名词否定）→ 反向激活
> - ✅ `five fingers on each hand... Do not add extra fingers.`（正向锚定占住描述位后收边）
>   ⚠️ 但按 §1.3 冗余性判据此句属**冗余**，最优选 `Do not change the number of fingers at any point.`
> 依据：Morphed 实测 *"Adding one negative constraint per reference generation was the cheapest reliability fix in the whole set."*

### 1.3 裸名词否定的 A/B 两级判定线【推断 · 本项目裁定】

**§1.2 第 4 条只说了"禁止成串"，但单个裸名词否定怎么判，需要一个分镜师能自己判的标准。**

```
按【名词性质】分两级：

A 类 · 具体可视内容 —— 画面里能被指认出来的元素
   fingers / figures / people / crowd / text / letters / numbers / logos /
   watermark / subtitles / patterns / texture / detail / clock face / lamps /
   accessories / outfit / hair colour / interface elements
   → ❌ 一律改正向，无例外。不成串也不行。

B 类 · 纯物理或时间属性 —— 不是可渲染的内容，只是帧间/时间上的性质
   drift / shake / jitter / stutter / flicker / acceleration / deceleration /
   eye movement / distortion / wobble
   → ⚠️ 允许单个存在，但必须同时满足三条：
      ① 一镜内最多 1 处，不得成串
      ② 前面已有正向描述
      ③ 与 `Do not` 句【合并计 1 处额度】（一镜内否定表达总共只有 1 处）

判定口诀（修正版）：**模型能把它渲染出来的是 A 类，只是物理/时间属性的是 B 类。**

成串一律违规：不论 A/B，≥2 个并列无谓语名词短语即违规（独立于上面分级）。
```

**机制依据**【推断】：反向激活的强度取决于名词在**视觉条件分布中的表征强度**。
`text`、`finger` 是模型可独立生成的对象，激活后易泄漏到输出；`drift`、`flicker` 不是可渲染内容、只是帧间变化属性，表征弥散，反向激活弱。
→ 该分级**从 VSF 机制外推**，非官方原文，标【推断·待验证】。

> ⚠️ **适用范围**：A/B 分级【只管裸名词否定】；`Do not` 句按下面的**冗余性判据**。
> **两者共用一个额度**：一镜内 `Do not` 句 + 裸名词否定**合计 ≤1 处**。
>
> **🔑 `Do not` 句的冗余性判据**（回答"A 类名词能不能写进 do not"）：
> **不看 A/B 类，看【这句 do not 是否重复正向已说过的内容】。**
> - **重复正向** → **冗余，删掉**。尤其当它重复 A 类名词时，是**纯风险（反向激活）零收益（正向已说）**
>   例：`... a plain unmarked surface ... Do not draw any letters, numbers or logos.` → 删掉 do not
> - **补充正向未覆盖的** → 保留，**优先留给 B 类帧间属性**（正向难以静态描述的东西）
>   例：`Do not change the brightness of the screen at any point.`
>
> **这调和了两条证据**：Morphed"一句否定有效"指**补充**；VSF"反向激活"指**重复/无前置**。
> ⚠️【推断·待验证】——找不到正向写法时报【待验证】实测，不默认豁免。
>
> **开放量词按 A 类**：`anything` / `any content` / `any object` 出现在否定句里 → **A 类**。
> 理由：外延**包含 A 类可视元素且无法在生成时限定范围**，等同于把这些元素全部点名激活。
> 处置：不是删整句，而是**改为正向**（"保持原样/不额外添加"正向都能说清）。
> 例：`Do not add anything on the screen.` → `the screen content stays exactly as first shown`
>
> **⚠️ 本限制【同时适用于中文详版与英文终稿】**，不得以"中文没有 `no X` 形态"为由豁免——
> 中文"不要/无/不出现 + A 类名词"同样是裸名词否定。
> **传导风险**：中文层放行 → 转录英文时被译回 A 类 do not → 英文层违规。
>
> **辅助判据**（A/B 拿不准时）：**单帧可见 → A 类；只有连续播放才察觉 → B 类。**

> **🔍 自查指令**：全文搜 `no `/`No `/`never `/`Do not`/`does not`/`not `/`avoid `，逐条判定。
> 重点查：①「可整句复制」的句库 ②标准声明句 ③指导性文字。**违规几乎都在那里**（12/12、3/4、2/2）。
> 另注意**同文件重复块**：改一处，要确认别处没有同类写法。
> **凡是写"额度给谁"的句子，都必须同时写"能装什么"** —— 只写前半句＝教人把 A 类塞进那唯一一个坑位。

> **⚠️ 口诀修正（原口诀判不了动作类）**：原口诀"能指给人看 A / 靠变化察觉 B"判不了 `pouring`（两类都像）。
> 修正为**"模型能不能把它渲染出来"** → 动作类（`pouring`/`smoking`/`walking`/`jumping`/`spinning`/`splashing`）**一律 A 类**。
> ✅ 不改变任何已有判定（`texture`/`detail`/`fill`/`sun` 仍 A，`eye movement`/`drift`/`flicker` 仍 B），只是把标准说准了。

> ⚠️ **B 类"可留"是【容忍存量】，不是【推荐写法】。**
> 凡新写提示词一律优先正向——**不必先判 A/B，先问"有没有同样清楚的正向写法"；有就用**（此判据优先于 A/B 分级）。

**改写对照**

| A 类（一律改正向） | 正向写法 |
|---|---|
| `no additional figures, no crowd, no background people` | `Exactly one person in frame, a single subject alone in the shot` |
| `no shake, no jitter, no stutter, no flicker` | `the motion smooth and even throughout` |
| `no text, no letters, no numbers, no logos` | `plain unmarked surfaces showing only colour and material` |
| `no repeating fine patterns` / `no texture` / `no detail` | `plain surfaces and smooth gradients throughout` |
| `no practical lamps in frame` | `the only light sources are off-screen` |
| `no change in hair colour, no change of outfit` | `hair colour and outfit remain identical throughout` |
| `no fingers are visible` | `both hands tucked into her coat pockets, hands fully hidden from view` |

| B 类（单个可留） | 示例 |
|---|---|
| `no drift` | `ending on a stable held frame with no drift` ✅ |
| `no eye movement` | `her gaze held steady, no eye movement` ✅ |

**⚠️ 与硬阻断清单的边界**：裸名词否定**属提示词可修**（改正向即可），**不属 §11 硬阻断**。
不要在硬阻断清单里找它，也不要因为它去改分镜。

### 1.4 正反例对照

```
✅ 最优（先正向后否定，do not 补充正向未覆盖的帧间属性）
Her hands rest flat on the table, fingers held together, five fingers on each hand,
natural proportions. Do not change the number of fingers at any point.

✅ 正确（纯正向锚定，零否定）
Both hands hang naturally at her sides, fingers gently curled and held together,
thumbs resting along the seams of her trousers.

❌ 错误（只有否定、无正向锚定）
Do not make six fingers. Do not deform hands. Do not show extra limbs.

❌ 错误（成串裸名词否定 —— 把"不要的东西"列给模型当购物清单）
no six fingers, no extra limbs, no deformed hands, no watermark, no text, no blur

❌ 错误（否定句在句首，且前面无正向锚定）
Do not add other people. A woman stands by the window.

❌ 错误（两句 Do not）
... Do not add extra fingers. Do not change the lighting.
```

### 1.4 一句话改写口诀

> **把"不要 X"改写成"是 Y"。** 写不出 Y，说明这个镜头本身就应该改设计（走 §12 的"规避"）。

| 想禁的 | 改写成 |
|---|---|
| 不要六指 | `five fingers on each hand, natural finger proportions, clean separation between fingers` |
| 不要多出人 | `Exactly one person in frame, a single subject` |
| 不要镜头抖 | `A single continuous camera move at constant speed` |
| 不要穿模 | `Rigid objects stay rigid and keep their own volume; liquids stay inside their containers` |
| 不要冒出乱码字 | `All surfaces in frame stay plain and unmarked, showing only colour and material`（正向锚定 + 唯一保留的一句 `Do not add invented background text.`） |
| 不要换脸 | `The subject's face, hair, clothing and accessories remain identical from the first frame to the last` |

---

## 2. ⚠️ 采样步数（NFE）伪翻车 —— 最重要的一节

> **证据等级：【三方·官方直播转述】。**
> 核心规则源自 MiniMax 官方与 ComfyUI 的联合直播及社区实测归纳（中文技术媒体转述）。**未找到 MiniMax 书面文档中的对应原文**；数值区间（4 / 6–8）为社区共识而非官方硬指标。
> → 若要写进客户交付物，**先按 §2.5 的方法自测一遍**。

### 2.1 定义

**有一大类"翻车"，提示词完全没问题，是采样步数不够。**

| 场景 | 步数 |
|---|---|
| 试拍 / 找构图 / 快速验证方向 | **4 步** |
| **出片 / 送审 / 交付** | **6–8 步** |

**官方口径原文**：
> *"如果你发现人物动作开始'散架'或者音画对不上，**第一件该怀疑的事就是步数压太低了，而不是 prompt 写错了**。"*

### 2.2 伪翻车 vs 真问题：识别表

| 现象 | 先怀疑步数 | 还是直接判为提示词/设计问题 |
|---|---|---|
| 人物动作"散架"、关节处断裂 | ✅ **先抬步数** | — |
| 音画对不上（口型/音效错位） | ✅ **先抬步数** | — |
| 动作不连贯、中间帧跳变 | ✅ **先抬步数** | — |
| 手指数目错 | 一次抬步数 + 换种子 | 反复出现 → 走 §3 三档降级 |
| 画面里冒出乱码文字 | 一次换种子 | 反复出现 → 属硬阻断，走 §11 |
| 身份在跨镜间漂移 | — | ✅ 属 §6，走参考图/锁定块 |
| 物体穿模、液体溢出 | — | ✅ 属 §8，改设计 |
| 跨生成左右方位反了 | — | ✅ **硬阻断**，§11 |

**判据**：**概率性**（同一条提示词，几次生成有时崩有时不崩）→ 优先怀疑步数/种子；**确定性**（每次都崩，崩得一模一样）→ 是设计或提示词问题。

### 2.3 ⭐ 返工 SOP（必须替换原有流程）

```
画面崩了
  ↓
① 抬采样步数：4 → 6–8，同一条提示词重跑一次        ← 先做这个，90% 的情况到此为止
  ↓ 仍不合格
② 换种子，重生成 2–3 条，从中挑最好的一条          ← 概率性崩坏在这一步解决
  ↓ 仍不合格
③ 检查参考文件的保留强度标记（Ref2VA 模式，见 §9.3）
   —— 承载身份的资产是否都标了 fully_preserved
  ↓ 仍不合格
④ 对照 §11 硬阻断清单：是不是踩了硬阻断？
   是 → 不要改提示词，直接改分镜（规避/降级/后置，见 §12）
  ↓ 不是硬阻断
⑤ 最后才微调提示词（一次只改一处，改完回到 ① 重跑）
```

> **❌ 禁止：步数一直是 4，却反复改提示词。**
> 这是纯浪费——你改的每一版都是在低质量采样下评估的，结论不可靠，而且会误判成"这个镜头做不了"，白白砍掉本来能拍的戏。

### 2.4 分镜表必须加一列

| 列 | 控件 | 枚举值 | 规则 |
|---|---|---|---|
| `采样步数` | 单选 | **4（试拍）** / **6–8（出片）** | 每条生成记录必填；**送审与交付的一律 6–8** |

**这一列的作用**：让伪翻车可追溯。若某镜被判为失败但步数是 4，**该失败结论无效，必须重测**。

### 2.5 【待验证】自测方法（写进客户 SOP 前先跑）

1. 选 1 条含中等幅度肢体动作 + 1 句对白的提示词（这类最容易暴露步数不足）
2. 固定 seed，分别在 4 / 6 / 8 步各生成 1 条，共 3 条
3. 换 3 个不同 seed，重复第 2 步，共 9 条
4. 盲评（不看参数）打分：动作连贯性 / 音画同步 / 结构正确，各 1–5 分
5. **结论只在"同 seed 下 4 步明显低于 6–8 步、且 6 与 8 差异不显著"时才支持本文口径**

> 未做这一步之前，把 4 / 6–8 当作**社区经验值**使用，不要当作官方承诺。

---

## 3. 手部防崩：三档降级 + 无接触传递 + 风险分级

### 3.1 成因【工艺】

手部像素占比极小、姿势组合极多、训练样本中大量被遮挡，跨注意力难以把各部位映射到正确位置；视频还叠加**跨帧指骨数量变化**。

### 3.2 四条规避原则

```
① 提高像素占比（特写 > 全身；手占画面 ≥1/2）
② 消灭手指分离需求（握拳、叠放、插兜、背手）
③ 消灭"精细持物"（签字、持笔、插钥匙 —— 直接换动作）
④ 用无接触传递替代递交
```

**④ 的原理【2.3 实测，机制通用】**：
> `hands her the cup`（手递手）的失败率**显著高于** `slides the cup across the table toward her`（沿桌面推过去）。
> 原因：递接要求两只手在同一空间点精确对准并保持接触，是 §11 的"小尺度精确对准"硬阻断。

### 3.3 三档降级表（手部镜头必须在此表内选一档）

| 档 | 动作 | 风险 | 写法 |
|---|---|---|---|
| **A 档（首选）** | 手不可见 | 无 | `Both hands are tucked into her coat pockets, hands fully hidden from view.` |
| **A 档** | 手可见但不分离 | 低 | `Her hands hang naturally at her sides, fingers gently curled and held together, thumbs resting along the seams of her trousers.` |
| **A 档** | 握拳 | **中** | `He rests a closed fist on the table, fingers curled inward, knuckles visible.` |
| **B 档** | 手掌平覆 / 整体包裹 | **中** | `Her hand lies flat against the fabric of her skirt, palm down, five fingers held together, natural finger proportions.`<br>`He holds a large ceramic mug with both hands, fingers wrapped fully around the body of the mug.` |
| **B 档** | 手部特写（占画面 ≥1/2） | **中** | `Close-up from the wrist up, the hand fills more than half the frame, five fingers, natural proportions, clean edges.` |
| **C 档** | 捏衣角 | **高** | 改 B 档：`her palm rests flat on the fabric of her skirt, palm down, five fingers held together` |
| **✗ 禁用** | **签字 / 持笔 / 插钥匙 / 拨号盘** | **极高** | **换动作**：签字 → 合上文件、盖印章、放下笔；插钥匙 → 手已经握在门把上 |

### 3.4 兜底约束句（正向锚定，可直接复制）

```
Five fingers on each hand, natural finger length and spacing, clean separation between fingers,
hands fully visible in frame.
中文：双手各五指，手指长度与间距自然，指间分离干净，双手完整在画面内。
```

> **绝不写**：`no six fingers` / `do not generate extra fingers` / `no mutated hands`。

### 3.5 手部风险分级（用于分镜表 `风险等级` 列）

| 动作 | 等级 | 处置 |
|---|---|---|
| 手在口袋/画外/背手 | 低 | 直接拍 |
| 自然下垂并拢 | 低 | 直接拍 |
| 握拳 | 中 | 直接拍，出片步数 6–8 |
| 手掌平覆、整体包裹持物 | 中 | 直接拍，手部占画面 ≥1/3 |
| 捏衣角、捻小物件 | 高 | **降级**为平覆 |
| 签字 / 持笔 / 插钥匙 / 指尖点按 | **极高** | **规避**，换动作 |
| 手递手交接物品 | 高 | **规避**，改无接触传递 |

---

## 4. 肢体结构与人数控制

### 4.1 成因【工艺】

模型无骨骼与关节自由度约束，只学了"看起来合理"的像素统计；人数在跨帧状态跟踪中易漂移。

### 4.2 四条规避原则

```
① 用 then 串联动作，禁用 while 并发
② 每个动作给明确终点（有界动作）
③ 多人时第一句就拉开外观差异，每人只给一个动作
④ 人数写死并前置
```

**① 的依据【2.3 实测，机制通用】**：`She sips while waving while walking` 会破坏 anatomy；`She picks up the cup, then takes a sip` 则干净。
**③ 的反例必崩**：`two men in suits` —— 对称描述会诱导人物**融合**。必须拉开差异。

### 4.3 可直接复制的写法

```
人数写死：
Exactly ONE person in frame, a single subject alone in the shot.
中文：画面中严格只有一名人物，任何位置不出现第二个人形。

then 串联：
She lowers the folder onto the desk, then straightens her back, then turns to face the window.
中文：她把文件夹放到桌上，然后挺直后背，然后转向窗户。

多人拉开差异 + 每人一个动作：
A tall man in a red apron (left of frame) and a short woman in a denim jacket (right of frame);
the man folds his arms, then the woman takes one step forward.

静态姿态锚定：
Both arms hang at his sides throughout; both shoulders remain level and square to camera;
his neck stays straight, the head held level with only a slight downward glance.

有界动作：
The movement stays slow, single and bounded: one continuous action, the limbs moving at an even pace,
the feet staying on the ground throughout.
```

### 4.4 肢体检查清单

```
□ 动作全部用 then / first...then...finally 串联，无 while、无"同时"
□ 每个动作有明确终点（不是"一直在动"）
□ 人数在第一句写死，且是具体数字（ONE / TWO），不是"几个人"
□ 若人数 ≥2，每人的外观差异在第一句内拉开（高/矮、服色、位置）
□ 若人数 ≥2，每人只给一个动作
□ 无跳跃、旋转、快速挥动
□ 无"双手同时做不同精细动作"
□ 关节朝向已声明（arms hang at sides / shoulders level / neck straight）
```

---

## 5. 镜头流畅性

### 5.1 官方运镜术语表【H3】

| 想要的效果 | 官方写法 |
|---|---|
| 物理靠近 / 远离 | `Push In` / `Pull Out` |
| 改变焦距 | `Zoom In` / `Zoom Out` |
| 原地水平旋转 / 整机身横移 | `Pan Left/Right` / `Truck Left/Right` |
| 垂直旋转 / 整机身升降 | `Tilt Up/Down` / `Pedestal Up/Down` |
| 环绕 / 跟随 / 固定 / 主观视角 | `Arc Shot` / `Tracking Shot` / `Static Shot` / `POV` |
| 不稳定感 / 地平线旋转 | `Shake Slightly`、`Shake Strongly` / `Roll Clockwise`、`Roll Counterclockwise` |

**三维顺序**：motion type → amplitude → speed。中等幅度与正常速度**省略不写**（留给模型反而更稳）。

### 5.2 四条规避原则

```
① 一镜只给一个运镜（不要在同一 3 秒内叠加环绕 + 变焦 + 升降 + 手持）
② 幅度与速度只在必要时加，不要机械地每条都加
③ 运镜写在当前镜之内，不要把所有运镜关键词堆在提示词末尾
④ 运镜句写在该镜开头（运镜句前置）
```

**① 的官方/实测依据**：*"One camera move per clip is not a stylistic preference, it is the operating limit."* 三个以上运镜会被**平均成漂移**。

### 5.3 可直接复制的写法

```
The camera pushes in with small amplitude at slow speed from a medium shot to a close-up.
The camera pulls out with large amplitude at slow speed while pedestaling upward with small
amplitude at slow speed.                       ← 例外：同向可组合，反向不可
It travels directly backward along the same optical axis. The camera does not orbit,
truck sideways, or use a digital zoom.
The camera holds a static shot.
中文：镜头以小幅慢速从近景推近至特写。／镜头大幅慢速拉远，同时小幅慢速升高。
      镜头沿同一光轴直线后退；不环绕、不横移、不使用数字变焦。／镜头保持固定。
```

### 5.4 时间连接词（性价比最高的一次改写）

**实测原文**：
> *"Without them the model has to guess whether your three described events happen in sequence or simultaneously, and it **usually picks simultaneously**, which is what produces the mushy, everything-at-once clips."*

**做法**：用 `First ..., then ..., as ..., finally ...` 显式给 beat 顺序。**仅加 4 个词，是整份实测里性价比最高的一次改写。**

```
❌ She picks up the cup and sips and looks out the window.
✅ First she picks up the cup, then she takes one sip, then she turns her head toward the window.
```

### 5.5 跨镜方向对齐四规则【工艺】

```
① 上下两镜必须用同一个运镜术语（都用 Truck right，不要一段 pan、一段 move）
② 方向句写在当前镜开头
③ 给两镜一个共同物理参照物（"结束于深色墙面充满画面" → "从深色墙面继续向右进入"）
④ 跨请求左右一致仍是硬阻断，只能后期镜像——除非把三镜放进同一次请求
```

### 5.6 镜头流畅检查清单

```
□ 每镜只有 1 个运镜术语，且术语在官方表内
□ 未叠加反向运镜（push in + pull out 不可同镜）
□ 运镜句在该镜开头，不是堆在段末
□ 幅度/速度只在必要时写，未机械堆砌
□ 动作 beat 用了 First / then / as / finally 等时间连接词
□ 相邻镜共用同一运镜术语（或共用一个物理参照物）
□ 时间戳：Shot 1 无时间戳；后续严格递增；格式为 00:SS.mmm（三位小数）
□ 时间戳全部落在请求时长内
□ 每次切镜都引入新信息（主体/空间/状态/视角/时间）；只有距离或角度变化 → 改用运镜，不切镜
□ 末帧状态已显式声明（供下一段接）
```

### 5.7 时间戳精度与剪辑冗余【三方·实测】

**实测数据**：切点落点误差 **±0.12 秒**。
> *"In our testing the cuts landed within 0.12 seconds of the mark, while the same brief written as plain prose held a single framing for all 15 seconds."*

→ **时间戳是软引导，不是硬约束。** 分镜表「时长」列应标为**目标值 ±0.15s**，不是保证值。

**⚠️ 容易搞错的一条：误差不跨段累积。**
总时长由请求固定（如 15 秒）。若 cut1 晚 0.12 秒，shot1 变成 5.12 秒、剩余变成 9.88 秒——**切点偏移只是在段内重新分配，段的总长不变**。

```
✅ 正确：每段留 0.2 秒剪辑冗余（固定值）
❌ 错误：10 个段落留 10 × 0.2 = 2 秒冗余 → 过度预留，浪费时长
```

**另注**：**不要指定精确帧数或 FPS** —— 时机由模型控制。

---

## 6. 身份漂移与光照稳定

### 6.1 成因【工艺】

每次生成是独立任务，无长期记忆；文字描述不精确时，模型每次重新"猜"。

### 6.2 H3 的正确解法：把身份外置到参考图

```
图 1  角色正面定妆（脸 + 发型 + 妆容）
图 2  角色侧面 / 45°
图 3  角色全身（体型 + 服装 + 鞋）
图 4  场景空镜（含光源方向）
图 5  画风 / 调色参考
```

> 走 Ref2VA 就没有首尾帧，走 FL2VA 就不能用 9 张参考图（**模式互斥**）。同一段内不能混用。

### 6.3 可勾选的身份锁定清单

```
□ 角色描述串在每一镜逐字复制，一字未改（Verbatim Rule）
□ 描述串含可辨识的具象特征（脸型/发长/发色/瞳色/鼻型/下巴），不含"英俊""漂亮"这类抽象词
□ 服装写到颜色 + 材质 + 款式，且声明"全程不增减任何配饰"
□ 主光源方向写死（如 from camera left at 45°），且每一镜都写
□ 只有 1 个主光源；画面内尽量无可见灯具（practical lamps）
□ 只锁 1–2 个不可变配饰（锁多了互相干扰）
□ 画风串三镜共用，逐字一致
□ 已声明不变性收尾句
```

### 6.4 可直接复制的写法

```
The same woman appears in every shot: 28 years old, shoulder-length straight black hair in a low
ponytail, dark brown eyes, straight nose, soft round chin. She wears an unbranded ivory cotton
T-shirt and dark-wash straight-leg jeans. Her appearance does not change at any point: same hair,
same face, same clothing, same age, same body type, from the first frame to the last.
A single soft key light from camera left throughout; her hair colour, outfit and every accessory
stay identical from the first frame to the last, the same earrings and the same watch in the same
positions throughout.

中文：同一名女性贯穿全部镜头：28 岁，齐肩黑色直发低马尾，深棕色眼睛，鼻梁挺直，下巴圆润，
身穿无标识的米白色纯棉 T 恤与深蓝色直筒牛仔裤。从第一帧到最后一帧，发型、五官、服装、年龄、
体型完全不变。全程单一柔和主光，来自镜头左侧。

[STYLE LOCK — copy verbatim into every shot]
Live-action, cinematic and photorealistic, 35mm lens, shallow depth of field, muted teal-and-amber
grade, natural skin texture, a straight photographic look without stylisation,
consistent colour temperature, consistent contrast.
[LIGHT LOCK] A single soft key light from camera left at 45°, cool ambient fill,
all light sources kept off-screen.
```

> **⚠️ 主光一旦换边，身份就会晃。** 光照方向是身份一致性的隐藏变量，优先级等同于脸部描述。

---

## 7. 语言与文字（H3 新增高风险区）

> H3 **原生生成语音**，所以翻车形态从"口型对不上"变成"**说错话 / 说错人 / 说错语言**"。这是 H3 相对前代的新增高风险项。

### 7.1 台词量上限

**【H3】官方原文（已核实所指为被念出的台词，不是描述长度）**：
> *"Only what sits inside the tag is spoken, so stage directions never get read aloud. Around twenty words fit comfortably in a clip, about ten to a line; pack in more and the delivery rushes, then slurs."*

**官方语速基准**：自然语速约 **2.5 词/秒**；*"A 10-second clip fits maybe 20-25 spoken words total if you want anything else to happen."*

| 口径 | 数值 | 用途 |
|---|---|---|
| 绝对红线 | **47 汉字 / 15 秒** | 理论天花板，超过必含糊。**有官方推导支撑**（见下方四条路径） |
| **执行线** | **≤45 汉字 / 15 秒** | **工程安全边，非推导值**。**结构检查按这条判** |
| 建议写作区间 | **30–40 汉字 / 15 秒** | 舒适区。**有官方推导支撑：官方舒适值折算 = 38 字** |
| 主镜 | ≤35 汉字 | — |
| 衔接镜 | ≤6 汉字（宽松上限 7） | **建议干脆无台词**（见下方口径说明） |

> ⛔ **不要把 45 说成官方推导值 —— 对外宣称 45 有官方依据属虚假置信。**
> 45 是 47 减约 4% 的工程安全边，正当性来自"模型实际语速不可控"，**不是物理边界，也对应不上官方任何数字**。

---

#### ⚠️ 勘误：以下旧推导已作废（量纲错误）

> **旧版作废声明**：本小节曾写过「25 词 ÷ 2.5 = 10s → × 4.5 = 45 字（对应执行线）」「20 词 ÷ 2.5 = 8s → × 4.5 ≈ 36 字」。
> **这两行有量纲错误，已删除，不要引用。**
>
> **错在哪**：
> 官方原句是 *"A 10-second clip fits maybe 20-25 spoken words"* —— 所以它推出的是 **10 秒片段 / ρ=1.0** 的容量。
> 而本表其他数值都是 **15 秒 / ρ=0.70** 的容量。**两者量纲不同，不能混用。**
>
> **自证矛盾**：本文 §7.1 衔接镜一行用 `2.0s × 3.15 字/秒`（= 4.5 × 0.70）算出 6.3 字；旧推导说 10 秒能装 45 字（= 10 × 4.5 × 1.0），**与自身的 ρ=0.70 口径直接打架**。
>
> **为什么数字会"撞上"——是巧合，不是印证**：
> ```
> 47 = 15 × 4.5 × 0.70      ← 15 秒 / 占用率 0.70
> 45 = 10 × 4.5 × 1.0       ← 10 秒 / 占用率 1.00
> ```
> 两个式子有 **15 vs 10**、**0.70 vs 1.0** 两处不同（15 × 0.70 = 10.5 ≈ 10 × 1.0），**恰好部分抵消**。
> → 因此**不得**用"两条独立路径收敛到相邻数值"来论证 45 或 47 的合理性。**该论证已撤。**
>
> *（本勘误由 `h3-dialogue-voice` 交叉检查发现并同步。）*

---

#### 正确的四条路径【统一到 15 秒 / ρ=0.70 / 1 英文词 ≈ 1.8 汉字】

换算基准：4.5 字/秒 ÷ 2.5 词/秒 = **1.8 汉字/英文词**

| 路径 | 计算 | 结果 |
|---|---|---|
| ① 时长公式 | 15 × 4.5 × 0.70 | **47 字** |
| ② 官方天花板速率 | 官方 25 词/10s = 2.5 词/秒 ≡ 4.5 字/秒 → 15 × 4.5 × 0.70 | **47 字** |
| ③ 官方舒适速率 | 官方 20 词/10s = **2.0 词/秒** ≡ **3.6 字/秒** → 15 × 3.6 × 0.70 | **37.8 ≈ 38 字** |
| ③b 等价算法 | 47 × 官方舒适/天花板比 (20/25 = 0.80) | **37.6 ≈ 38 字** |

**结论**：
- **47 字** = 理论天花板，① 与 ② 两条路径同解，互为印证，**这条成立**。
- **38 字** = 官方舒适值折算，落在「建议 30–40」区间内 → **建议写作区间这次有官方依据了**。
- **45 字** = **无独立推导**，仅 47 减约 4% 的工程安全边。

**单句上限**【推】：官方 *"about ten to a line"* → 10 英文词 ÷ 2.5 词/秒 = **4 秒** → 4 × 4.5 字/秒 = **18 字硬上限**；建议 **12–15 字**（与字幕单行 12–15 字自洽）。
> 注：单句内部不存在"留给别的动作"的问题，故此处 **ρ=1.0**（4 秒全被这句占满）是**正确的隐含假设**，与上述量纲错误的情形不同。

**衔接镜 6 字 vs 7 字**：2.0s × 3.15 字/秒（= 4.5 × 0.70）≈ **6.3 字** → 取小者 **6 字**；主模板模块八给的是 **≤7 字**（对应 2.2s）。差异只在舍入方向，**不影响结论**。
→ **统一口径：衔接镜建议无台词**；必须有台词时按 **≤6 字** 执行（取小者），模块八的 ≤7 作为宽松上限仍成立。

**另两条**：
- **一镜一个说话人**（*"The single most reliable trick for clean lip sync. If two people need to talk, cut between them."*）
  → 两人对话**必须切成两镜**，不是在一镜内让两人先后说。
- 唇形同步支持 **11 语言**：阿拉伯语、中文、英语、法语、德语、意大利语、日语、韩语、葡萄牙语、俄语、西班牙语。
  （**【待验证】** 11 语言之外是否可用、各语言可懂度差异，需实测；未测前不要给客户承诺。）

### 7.2 `<d>` 标签规范【H3 官方】

```
结构：说话人识别语 + ID + 动作 + 语气  放在 <d> 外
     语言标签 + 原话                  放在 <d> 内

The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
中文示例：<d>[Chinese] 我早就知道了。</d>
```

**官方红线**：
- `<d>` 内**只放**语言标签与逐字原话；身份/动作/语气一律放外面
- **do not translate or rewrite them**（不翻译、不改写）
- 不出声的角色**不给 ID**
- 同一说话人**跨镜 ID 不变**，切换镜头后不得重新编号
- **`<d>` 内默认不加英文双引号**（⚠️ 非绝对禁令，**官方存在冲突证据**，见下）

#### `<d>` 内要不要加双引号：官方证据冲突，按「默认不加」执行

**⚠️ 这不是已定论的禁律。官方两处证据互相冲突，实测前不作绝对判定。**

**证据 A —— 支持不加（文本文档口径）**
- 官方对双引号的定义原文：*"Place any banner, sign, label, subtitle, or neon text that is actually visible on screen in English double quotation marks."*，示例为 `A red neon sign reading "营业中" glows above the doorway.`
- 官方对白例句逐字为 `The young woman ... (S1) says: <d>[English] I get off at the next station.</d>`，**无任何双引号**。

**证据 B —— 支持加（官方直播口径，与 A 冲突）**
- 出处：`防翻车限制词库_H3版.md` **第 97 行**记录的 **MiniMax × ComfyUI 官方直播**建议，原文大意：
  > 把输入音频作为 reference 的同时，在提示词里**用引号写出角色要说的台词，并放进对应镜头的描述中** —— 两者并用可显著提升对白稳定性与一致性。

**三条无法确认（这是冲突无法当场判定的原因）**：
1. **直播技巧是否可与 `<d>` 并用** —— 官方**未说明**。直播讲的是"放进镜头描述"，未提 `<d>` 标签。
2. **原话以"把输入音频作为 reference 的同时"开头** —— 该技巧**可能仅限"配 reference 音频"这一场景**，未必是通用写法。
3. **效力层级** —— 成文文档（`base-en.txt`）权威性高于口头演示；**但直播可能反映更新的工程实践**，不能简单以"成文优先"压掉。

**当前处置（按 team-lead 裁决软化，原绝对禁令已撤销）**：
1. **默认不加** —— 沿用证据 A（文本文档示例逐字可核；直播口径为转述且场景限定不明）
2. **冲突必须披露** —— 若下游采用加引号写法，**不得声称"官方禁止"**，须说明两条证据并存
3. **列为待验证** —— 未实测前，两种写法都不判定为错误

**新增：一档可选写法（采用直播技巧时）**
```
配 reference 音频时，可采用直播技巧 —— 但引号写在「镜头描述层」，不写进 <d> 内：

the woman stands by the window, her line "我早就知道了" delivered flatly,
her breath fogging the glass. <d>[Chinese] 我早就知道了。</d>
                              ↑ 台词在 <d> 内；描述层的引号写法按直播技巧保留

⚠️ 此写法【推断·待验证】：直播只说"放进镜头描述"，未说可与 <d> 并用。
```

**风险提示（仍成立，但属推论）**：在 `<d>` 里套双引号，等于把"要念出来的台词"和"要渲染出来的招牌"用同一组符号标记，**可能**诱导模型把台词渲染成画面里的字。
→ **注意：这是推论，不是实测结论。**

> **【待验证】实测方法**（A/B/C 三组，各 5 条）：
> - **A 组**：`<d>[Chinese] 我早就知道了。</d>`（`<d>` 内无引号）← 当前默认
> - **B 组**：`<d>[Chinese] "我早就知道了。"</d>`（`<d>` 内加引号）
> - **C 组**：配 reference 音频，引号写在**镜头描述层**、`<d>` 内不加（直播技巧的原样落法）
>
> **判据**：
> - B 组 vs A 组 → 看 B 组是否出现台词被渲染为画面内文字
> - **C 组 vs A 组 → 看对白稳定性/一致性是否显著提升；C 组显著更优，则证明直播技巧成立，且应落在描述层而非 `<d>` 内**
>
> *（C 组设计由 `h3-dialogue-voice` 补充。）*

> ⚠️ **上游已清理**：旧版 `防翻车限制词库_H3版.md` §1.1、`叙事侧方法论`（336/451 行）、`Ref2VA模板`（218 行）、`v1模板` 中的 `<d>[Chinese] "..."</d>` 写法已由 team-lead 全部清理（共 5 处）。
> **该写法的原判定"无官方原文支持，已作废"已撤销** —— 现确认该写法**很可能就出自上述官方直播**，属「**出处可考 + 适用范围不明**」（写进 `<d>` 内未经官方确认），**不是"无官方支持的错误"**。

### 7.3 说话人 ID 与串音

```
✅ 正确（跨镜复用 ID，不重新编号；说话人切换靠切镜完成，不是一镜内两人先后说）
[Shot 1] ... the woman ... (S1) says: <d>[English] I get off at the next station.</d>
[Shot 2] At 00:05.000, the camera cuts to the man ... (S2) replies: <d>[English] Then we leave now.</d>
                       ↑ 切镜后才换人 —— 这是「一镜一个说话人」的正确实现方式

❌ 错误（换镜重新编号 → 声音串台）
[Shot 1] [Character A: Mom] ...
[Shot 2] [Mother] ...            ← 角色标签前后不一致，是声音串台/张冠李戴的已知根因

❌ 错误（一镜内两人先后说话，违反「一镜一个说话人」）
[Shot 1] the woman (S1) says <d>[English] ...</d>, then the man (S2) replies <d>[English] ...</d>
          → 官方：*"If two people need to talk, cut between them."* 必须切成两镜
```

### 7.4 画外音（必须成对出现）

**【H3】官方规则**：画外音必须显式声明口型闭合，否则模型会在"谁在说"上产生歧义（画面里的人会跟着动嘴，口型与旁白打架）。

```
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d>
while his lips remain completely closed.
```

> **「嘴唇保持闭合」官方原句 = `while his lips remain completely closed.`** 整句照抄，不要改写；人称可按需改为 `her` / `their`。

**纯画外叙述者（旁白者不在画面内）**【推断·待验证】
官方只给了"旁白者在画面里"的例句。旁白者不在画面里时，按下式外推：

```
An unseen narrator with a low, unhurried voice (S1) says in an off-screen voiceover:
<d>[English] I still remember that road.</d> On screen, the woman sits by the window;
her lips remain completely closed throughout.
```

> 实测方法：A 组用官方在画面内的句式、B 组用上式，各 5 条，比对是否出现"画面内人物跟着动嘴"或"旁白音色被赋予画面内人物"。未测前，优先用官方原始句式。

### 7.5 跨剪辑连续对白 / 结尾截断【H3 官方】

| 情况 | 写法 |
|---|---|
| 同一句台词跨切点 | 在两段连接处都用 `<scenetrans>`，并显式声明 `continues seamlessly across the cut` |
| 台词被片尾截断 | 用 `<cutoff>` |
| 连续性表达可选词 | `continues uninterrupted into the next shot` / `carries over from the previous shot` / `remains audible across the transition` |

> ⚠️ **`<cutoff>` 的官方定义边界**：官方原文是 *"Use `<cutoff>` when speech is truncated by the end of the video"*，字面指**视频结尾**截断。
> **片中打断**（A 说到一半被 B 抢话）用 `<cutoff>` 属**本项目外推**，标【推断·待验证】。
> 稳妥替代写法：**用画面事件打断**，不用标签 —— `a door slams and cuts her off`。
> 实测方法：A 组片中打断用 `<cutoff>`、B 组用画面事件句，各 5 条，比对是否真的在指定位置收声。

### 7.6 画面内可见文字【H3 官方】

**规则**：必须出现的可见文本放进**英文双引号**，**逐字保留不翻译**；文本要**大、高对比、静态承载面、短时长**。

```
A red neon sign reading "营业中" glows above the doorway.
A blue neon sign reading "OPEN ALL NIGHT" flickers above the entrance.
（❌ 不要写 the sign says something about being open）
```

> ⚠️ **双引号的符号分工（与 §7.2 联动）**：
> **英文双引号 = 画面内可见文字的标记，`<d>` 对白默认不用。**（⚠️ 非绝对禁令，官方证据冲突，见 §7.2）
> 两套语义共用一组符号，混用**可能**让模型分不清"要念出来"和"要渲染出来"：
> ```
> ✅ 默认对白：<d>[Chinese] 我早就知道了。</d>          ← 无双引号（默认写法）
> ✅ 可见文字：A red neon sign reading "营业中"         ← 有双引号（官方明确要求）
> ⚠️ 不推荐：<d>[Chinese] "我早就知道了。"</d>           ← 可能把台词渲染成画面内的字
>            ↑ 【未实测，不判为错误】。不推荐的理由是「推论」，不是实测结论；
>              官方直播口径支持加引号（但指的是描述层），冲突详情见 §7.2
> ```

**但评级维持「高风险」，不因 2K 降级**。两方说法冲突：

| 立场 | 原文 | 判断 |
|---|---|---|
| 乐观 | *"Small text stays legible... at 1440p fine detail stops being suggestion and becomes information"* | 单一来源，无测试集 |
| **保守（采纳）** | ***"Keep on-screen text large and high-contrast. Small text is the first casualty of 8-bit quantization."*** | **给出了失效机制**（8-bit 量化），与已知量化损失原理一致 |

→ **从严处置：能不出字就不出字。**

**分级处置表**

| 场景 | 处置 | 写法 |
|---|---|---|
| 文字**不需要**被看清 | **首选：干净底板 + 后期贴图** | `A plain unbranded shopfront with a blank signboard, every surface in frame staying plain and unmarked, showing only colour and material.` |
| 手机屏内容 | **干净底板 + 冷白光映脸** | `A smartphone with a dark screen showing only a uniform dark surface; the screen emits a soft cool-white glow onto her face.` |
| 屏幕"有那么回事"即可 | **主动声明不可辨认** | `the screen content is softened by motion blur and reflection, illegible` |
| 文字**必须**精确出现 | **引号逐字 + 静态承载面 + 短时长** | `A blue neon sign reading "OPEN ALL NIGHT" flickers above the entrance.` |

> **"不可辨认"这一招的原理**：把 illegible 写进提示词，模型不再去赌字形，观众也读不出错字。**比硬写短信原文稳一个量级。**

### 7.7 手机屏幕三档（客户点名项）

| 档 | 做法 | 适用 | 写法 |
|---|---|---|---|
| **A 推荐** | 干净底板 + 后期 corner pin 贴图 | 内容必须读得出 | `she holds a phone with a blank dark screen showing only a uniform dark surface; a soft cool-white glow from the screen lights her face from below.` |
| **B 次选** | 主动声明不可辨认 | 只需"有那么回事" | `the screen content is softened by motion blur and reflection, illegible` |
| **C 冒险** | 先用图像模型做带正确文字的 UI 静帧 → 作参考图传入 → 提示词只写"内容不变" | 短镜头可接受 | `The screen content remains unchanged throughout.` |

> **⚠️ A 档旧写法已修正**：原为 `... No text visible anywhere.`。`text` 属 **A 类裸名词否定**
> （反向激活正好诱发 invented background text），且原标注"零风险"与判定相反。已改正向。
> 主模板 §6.4-E 同问题**已报 team-lead 裁定**，其答复前以本文为准。

**三条硬坑**：
1. **不要在提示词里写短信正文**，写了必乱码
2. **不要用极端特写怼屏幕**
3. **手机正反面翻转是已知高发项**（参考图锚定 + 多条挑选 + 后期）

### 7.8 语言与文字检查清单

```
□ 本段台词总量 ≤45 汉字（绝对红线 47，建议 30–40）；主镜 ≤35；衔接镜 ≤6（建议无台词）
□ 单句台词 ≤18 汉字（建议 12–15）
□ 一镜只有 1 个说话人；两人对话必须切成两镜
□ 每处对白都在 <d>...</d> 内
□ <d> 内只有语言标签 + 逐字原话，无身份/动作/语气
□ <d> 内**默认未加**英文双引号；如已加 → 属官方证据冲突项，**不判错**，但需知悉风险（见 §7.2）
□ <d> 内的台词未被翻译或改写
□ 说话人 ID (S1)/(S2) 跨镜稳定，未重新编号
□ 不出声的角色未被分配 ID
□ 画外音后紧跟 while his/her/their lips remain completely closed.
□ 跨切连续对白用了 <scenetrans>；视频结尾截断用了 <cutoff>
□ 画面内可见文字用英文双引号包裹，逐字未译
□ 未在提示词里写短信正文 / 未用极端特写怼屏幕
□ 不需要读出的文字已改为干净底板，或已主动声明 illegible
□ overall_soundscape 内未重复对白/演唱/剧情内音乐
□ non_diegetic_music 为 `N/A` 或 1–3 句声学参数描述（**禁止留空**），且未用抽象情绪词
```

> **为什么无配乐只写 `N/A`，不写 `no music`**：官方原文只有 *"Use N/A when there is no non-diegetic music."*【H3】。
> `no music` 的写法出自主模板模块九示例与旧版词库，**不是官方口径**；且存在被引擎理解为"生成一段名为无音乐的静音"的风险。
> **【待验证】实测方法**：同一条提示词，A 组写 `N/A`、B 组写 `no music`，各 5 条，比对是否存在静音轨异常或底噪差异。
> → 统一口径：**无配乐写 `N/A`；不留空、不写 `no music`。** 判空逻辑不变。

> **【推断·待验证】配乐进点建议写在人声之后**：H3 的配乐与对白在**同一次推理**中生成，会争同一段音频。
> 成本极低，建议在 `non_diegetic_music` 里显式写入场时机，如 `entering after she finishes speaking`。
> 实测方法：同一条含对白的提示词，A 组不写进点、B 组写 `entering after she finishes speaking`，各 5 条，盲评对白可懂度。

### 7.9 改台词：走编辑还是重生成？

H3 支持 in-context `dialogue replacement`（对白替换），官方明确"未指定的镜头元素保持原样"。

| 情况 | 用哪个 | 理由 |
|---|---|---|
| 只改**用词/语序**，表演、构图、运镜都满意 | ✅ **dialogue replacement** | 画面保留，成本最低 |
| 改台词后**时长变了**（字数差 >20%） | ❌ **重生成** | 口型节奏与新时长不匹配 |
| 改台词导致**情绪/表演需要变** | ❌ **重生成** | 表情在"指定改动范围"之外 |
| **语种切换**（中文版 → 英文版） | ✅ **优先 dialogue replacement** | 官方列出的典型用例（regional adaptations） |
| 画面本身有缺陷（手部崩、穿模） | ❌ **重生成**（先按 §2 抬步数） | 编辑模式不改未指定区域 |
| 只换**音色** | ✅ **dialogue replacement** + 换音频参考 | 用 `reference` 标记指向新音色 |

> **判断口诀**：**改"说什么" → 用编辑；改"怎么演"或"演多久" → 重生成。**
> **【待验证】**：画面是否逐帧 100% 不变，未经独立实测。官方表述是"未指定元素保持不变"，不是"其他部分逐帧不变"。交付级项目**先跑一次验证**再写进 SOP。

---

## 8. 物理与空间违和

### 8.1 成因：结构性缺陷

ICML 2025（字节 Seed × 清华，Kang et al.）结论：
> *"scaling alone is insufficient for video generation models to uncover fundamental physical laws."*

→ 模型学的是**物理的外观**，不是**物理的逻辑**；它在抄训练样本，不是在推理。

### 8.2 三条规避原则

```
① 回避动态物理，改拍静态结果
② 命名次级运动，否则模型只给你一个静态道具
③ 空间距离写死并声明"全程不变"
```

**① 示例**：`Person pouring water into glass` 会浮空/分流/越界 → 改成 `A filled glass of water stands on the table, the water already settled and still, the bottle resting beside it.`
（⚠️ 旧版写 `No pouring.` —— `pouring` 属**动作类 A 类**（模型能渲染出倒水动作），已改正向。）
**② 的依据**：外套翻飞、热气上升、裙摆摆动这类次级运动**必须显式写出来**才会出现。

### 8.3 可直接复制的写法

> ⚠️ **本块【逐条挑用，不要整段复制】。**
> 下面的句子各自合规，但**一镜内否定表达（`No pouring.` / `does not deform` 这类也算）合计 ≤1 处**。
> 整段复制会一次带入多处否定，直接违反 §15 的 A8。

```
A filled glass of water stands on the table, the water already settled and still, the bottle resting beside it.
Her coat whips in the wind, steam curls off the mug, the hem of her skirt sways with each step.
He sets the box down heavily onto the table; the table and the box both hold their shape on impact.
Two people stand two arm's lengths apart, and this distance stays constant for the whole shot.
The glass remains solid and rigid, its contents stay inside it, every object keeping its own volume.

中文：桌上放着一只已倒好水的玻璃杯，瓶子放在杯旁，全程不做倒水动作。
      她的外套在风中翻飞，杯口热气袅袅上升，裙摆随步伐摆动。
      他把纸箱重重放到桌上，桌面无形变，纸箱保持刚性。
      两人相距约两臂之遥，该距离在全镜头内保持不变。
```

### 8.4 物理检查清单

```
□ 无倒水、倒酒、泼洒等液体转移动作（已改为静态结果）
□ 无碰撞、无物体被撞飞、无跌落
□ 无大幅布料飘动（可做小幅摆动，且已显式命名）
□ 物体间距离已量化并声明"全程不变"
□ 无物体穿过另一物体
□ 刚性物体声明了 stays rigid
□ 次级运动已显式命名（衣摆/热气/头发/光影）
□ 空间方位用画面方位（frame left / on the left third of frame），不用"她的左边"
```

> ⚠️ **用画面方位，不用角色左右**："她的左边"有歧义（是她的左手边还是画面左边？），是左右翻转翻车的常见根因。

---

## 9. 道具与资产丢失

### 9.1 成因【工艺】

像素占比低 → 注意力不足；叠加"跨帧状态跟踪弱"。业界伪影综述明确记录：
> *"objects such as glasses or jewelry disappearing and reappearing between frames... tattoos or skin marks may vanish across frames."*

### 9.2 四要素锁定法（颜色 + 材质 + 固定位置 + 不变量声明）

```
[ASSET LOCK — paste verbatim] A small matte-gold signet ring on her RIGHT ring finger
(worn on the right hand, not the left). The ring stays on the same finger for the entire shot,
unchanged in size, colour and shape; it is never removed, never duplicated, never changes hand.
[LIMIT] Lock exactly two signature accessories per character. Do not add any others.

She wears a single small silver hoop earring on her LEFT earlobe; it remains on her left earlobe
for the entire shot, unchanged in size, shape and position, and is never removed or replaced.
She holds the phone in her RIGHT hand and does not switch hands at any point.

中文：［资产锁——逐字粘贴］她右手无名指佩戴一枚哑光金色印章戒指（戴在右手，非左手）。
该戒指在整个镜头中始终在同一根手指上，大小、颜色、形状不变，不会被摘下、不会重复出现、
不会换手。［限制］每个角色最多锁定两件标志性配饰。
```

### 9.3 三条硬规则 + Ref2VA 保留强度

```
1. 一镜内要稳住的小物件 ≤ 2 件（同时写耳环+项链+戒指+手链+发卡，几乎必然丢 1–2 件）
2. 每镜重复，逐字不改
3. 必须走参考图（纯文本描述小物件 ≈ 放弃）
```

**Ref2VA 下的正确工具：`retention_analysis` 保留强度标记【H3 官方】**

| 标记 | 含义 | 用于 |
|---|---|---|
| `fully_preserved` | 完全保留：身份、特征、道具全部不变 | **脸、发型、核心服装、关键道具——必须用这个** |
| `partially_preserved` | 部分保留 | 允许随情境微调的资产（外套开合、发型松散度） |
| `attribute_transfer` | 只迁移属性：风格、材质、颜色、质感 | 画风参考、调色参考、材质参考 |
| `weak_reference` | 弱参考，仅作倾向 | 氛围板、构图倾向 |

**官方原文**：*"A marker of `fully_preserved` on a face is what keeps it the same face all the way through."*

> **规则**：承载身份识别的资产一律 `fully_preserved`；纯风格/氛围一律 `attribute_transfer`。
> **风格参考若误用 `fully_preserved`，模型会把参考图里的物体也搬进画面。**

**两条实测习惯（值得照抄）**：
- **用文字复述参考图里已有的身份细节**（`Match Image 1's jawline and hair length`）—— 纸面上是冗余，实测稳定得多
- **一资产一职责**：`Use Image 1 for the subject's face and hair. Use Image 2 for wardrobe. Use Image 3 for the watch on her left wrist only.`

### 9.4 风险排序【推，含机制解释】

| 资产 | 等级 | 机制 |
|---|---|---|
| **义肢** | **最高 · 建议禁用或仅静态中远景** | 不只是"小物件"，会改变**肢体轮廓与关节结构**，易被渲染成正常肢体或与身体融合，属"肢体结构崩坏"而非"物件丢失" |
| 纹身 | 高 | 贴在皮肤上，随形变而形变 |
| 耳环 / 戒指 | 中高 | 像素极小 |
| 手表 / 手机 | 中 | 有明确承载面，可贴肤声明 |
| 大面积衣物 / 围巾 | 低 | 像素占比高 |

> **⚠️ 无公开量化基准**：未找到任何来源给出"耳环复现成功率 = X%"。
> **【待验证】自建测试方法**：≥20 次，**必须在真实运动条件下测**（静止画面测出的成功率无意义）。登记业界指标 **Prop Persistence Rate (PPR) / Wardrobe Lock Rate (WLR)**，建议目标 **≥80%**（此目标值为团队自设管理指标，非官方数据）。

### 9.5 道具检查清单

```
□ 一镜内需稳住的小物件 ≤ 2 件
□ 每件小物件都写了四要素：颜色 + 材质 + 固定位置 + 不变量声明
□ 高风险资产（纹身/义肢/耳环/戒指）已占参考图槽位
□ Ref2VA 模式下，承载身份的资产标了 fully_preserved
□ 风格/调色参考标的是 attribute_transfer，不是 fully_preserved
□ 左右手/左右耳已用大写 RIGHT / LEFT 写死
□ 已声明"不换手 / 不被摘下 / 不重复出现"
□ 义肢场景已降级为静态中远景，或已改剧本
```

---

## 10. 多镜一致性

### 10.1 成因【工艺】

多次独立生成无共享状态；提示词微改会导致风格漂移。

### 10.2 H3 的第一解法：三镜放进同一次请求

15 秒 3 镜**正好落在 H3 官方支持的单请求多镜区间内**。

| 时长 | 官方建议镜数 |
|---|---|
| 4–5 秒 | 1 镜 |
| 6–8 秒 | 1–2 镜 |
| 9–12 秒 | 2–3 镜 |
| **13–15 秒** | **2–4 镜** |

→ 三镜同请求 ⇒ 共享上下文 ⇒ **跨请求的"左右方位"与"180° 轴线"两项硬阻断自动解除**。

### 10.3 若必须拆成多次生成：锁定块 + 链式首尾帧

```
[STYLE LOCK — copy verbatim into every shot]
Live-action, cinematic and photorealistic, 35mm lens, shallow depth of field, muted teal-and-amber
grade, natural skin texture, a straight photographic look without stylisation,
consistent colour temperature, consistent contrast.
[LIGHT LOCK] A single soft key light from camera left at 45°, cool ambient fill,
all light sources kept off-screen.
[SHOT 3 STARTS FROM A NEW POSE] She is already standing with her back to the door; she begins by
turning her head slightly — this shot does not repeat the reaching motion from the previous shot.
```

**链式首尾帧**：生成镜 1 → 取最后一帧 → 作为镜 2 首帧，依此类推。H3 的 FL2VA（首帧 + 尾帧双锁）正好服务这个。

### 10.4 180° 轴线：写「画面」不写「规则名」

> **写 `respecting the 180-degree rule` 几乎无效** —— 那是行规名字，不是画面描述。
> **固定 seed 也救不了** —— seed 用于复现结果，不跨提示词承载空间约定。

```
[AXIS] The woman stands at frame left, angled toward frame right.
The man stands at frame right, angled toward frame left.
The window is behind them on the far side of the room.
The camera stays on the near side of the desk throughout.
```

三个要点：
1. **用绝对画面位置**（frame left / frame right），不要用"她的左边"
2. 加一个**不动的背景锚点**（窗户/门/墙）—— 锚点比人物描述可靠
3. **方向、朝向、行进方向三者会一起翻，必须一起写**

### 10.5 通用连续性 5 自查（每镜过一遍）

| # | 项 | 查什么 |
|---|---|---|
| 1 | 人物连续 | 服化道 / 五官 / 肢体数 |
| 2 | 方向连续 | 不左右翻转 |
| 3 | 动作连续 | 有先后承接，不瞬移 |
| 4 | 空间连续 | 守轴线 |
| 5 | 光线连续 | 光源角度 / 色温 / 明暗统一 |

### 10.6 风险类型 9 码（分镜表 `风险类型` 列下拉）

| 码 | 名称 | 触发特征 |
|---|---|---|
| `H` | 手部异常 | 手部入画、持物、精细手势 |
| `B` | 肢体与人体结构 | 全身入镜、大幅度肢体动作、人数 >1 |
| `M` | 镜头运动 | 任何非固定运镜、多段运镜组合 |
| `I` | 身份漂移 | 人脸清晰、换景、跨镜复用角色 |
| `T` | 文字与屏幕 | 招牌 / 字幕 / 手机屏 / 表盘数字 |
| `P` | 物理与空间 | 液体、布料、碰撞、穿模、空间距离 |
| `A` | 小物件资产丢失 | 耳环 / 戒指 / 手表 / 眼镜 / 纹身 / 义肢出场 |
| `X` | 跨镜头一致性 | 风格、光照、节奏、左右方位、动作重复 |
| `V` | 语音与说话人（H3 新增） | 有台词、跨镜说话、画外音、多角色对话、语种串台 |

**三类必查漏洞 → 9 码映射**

| 用户说的 | 覆盖的码 | 对应本文 |
|---|---|---|
| **人物结构类**（多手指、多余肢体、关节反折、人数、身份漂移） | `H` `B` `I` `A` | §3 §4 §6 §9 |
| **镜头流畅类**（运镜数量、运镜位置、时间连接词、并发动作、帧间漂移、末帧抖动） | `M` `X` | §5 §10 |
| **语言与文字类**（`<d>` 标签、说话人 ID、语种串台、画面文字乱码、口型同步） | `V` `T` | §7 |

---

## 11. ⛔ 硬阻断清单（提示词解决不了，别浪费时间）

> **这些问题的正确答案是"绕开"，不是"写好提示词"。**
> 遇到这几类，**第一反应应该是改分镜**。把"钥匙插进锁孔"改成"手已经握在门把上"，一秒钟解决问题；硬写提示词，十次也过不了。

### 11.1 主表

| # | 问题 | 为什么解决不了 | 唯一可行方案 |
|---|---|---|---|
| 1 | **屏幕 / 招牌 / 字幕的可读文字** | 模型把文字当像素图案，无字形结构规则；小字是 8-bit 量化的第一受害者 | **干净底板 + 后期贴图**；或主动声明 `illegible` |
| 2 | **跨生成的左右方位一致** | 每次生成为独立采样，无空间状态传递 | **后期水平镜像翻转**；或改为单请求内多镜 |
| 3 | **跨生成的 180° 轴线 / 正反打朝向** | 同上；模型没有轴线概念 | **同一次请求内完成正反打**；或后期镜像 |
| 4 | **拉远揭示镜**（无尾帧时） | 身体会凭空生成 | **改剪辑：局部镜 → 硬切 → 全景镜**；或局部作首帧、全景构图作尾帧（FL2VA），拉远段 ≤3 秒且 ≤该镜时长 50% |
| 5 | **小物件纯文本复现**（耳环 / 纹身） | 像素占比低，无持续状态跟踪 | **必须走参考图**（I2VA / Ref2VA），一资产一职责 |
| 6 | **物理接触 / 碰撞 / 液体 / 布料** | 结构性缺陷（ICML 2025 Kang et al.：模型抄训练样本而非推理物理） | **改写剧本避开**，或实拍 / 3D |
| 7 | **小尺度精确对准**（钥匙插锁、指尖点按拨号盘、车门从铰链侧开） | 无 3D 朝向跟踪与刚体约束 | **不给交互点特写** + 多条挑选 |
| 8 | **手机正反面翻转** | 已知高发项 | **参考图锚定** + 多条挑选 + 后期 |

### 11.2 分级：单次请求内可解除的两项

| 问题 | 单请求多镜（三镜同一次生成） | 跨请求（三镜分别生成） |
|---|---|---|
| #2 跨生成左右方位 | ✅ **自动解除**（共享上下文） | ✗ 硬阻断 → 后期镜像 |
| #3 跨生成 180° 轴线 / 正反打 | ✅ **降级为后置**（用 [AXIS] 块 + 同请求时间戳切镜） | ✗ 硬阻断 → 后期镜像 |
| #1 #4 #5 #6 #7 #8 | ✗ 仍是硬阻断 | ✗ 仍是硬阻断 |

→ **因此分镜表必须有一列 `是否单请求多镜`（是/否）**，填"是"时 #2 #3 自动由硬阻断降为"后置"。

### 11.3 硬阻断的识别口诀

```
出现下面任一特征，立刻停止改提示词：
  ✗ 同一条提示词重跑 3 次（步数已 6–8、换过种子），每次都崩，且崩法一致
  ✗ 崩的是"精确性"而非"概率性"（文字错字、左右反了、钥匙没插进锁孔）
  ✗ 你能清晰说出"正确的画面长什么样"，但模型每次都差一点点
  → 这是硬阻断，改分镜。
```

---

## 12. 处置四级枚举 + 决策流程

### 12.1 四级定义

| 级别 | 做法 | 适用 | 示例 |
|---|---|---|---|
| **规避** | 改分镜 / 改动作，从源头绕开 | 硬阻断清单里的项、极高风险动作 | 签字特写 → 合上文件；钥匙插锁 → 手已握在门把上 |
| **降级** | 镜头保留，但不承载关键叙事信息 | 中高风险但必须保留的镜头 | 手机屏只发冷白光、内容后期贴；捏衣角 → 手掌平覆布料 |
| **后置** | 生成时不解决，交给后期 | 文字、屏幕、方位、调色 | 屏幕内容后期 corner pin；跨请求左右方位后期镜像；三镜色温统一 |
| **重生成** | 抬步数 / 换种子 / 微调提示词 | 概率性崩坏，且不在硬阻断清单内 | 手部崩 → 抬步数到 6–8 → 换种子挑 2–3 条 |

**必填规则**：`备选方案` 恒必填，且必须是"**另一个能拍的镜头**"，**不得填"重试""调提示词"**。

### 12.2 决策流程（按顺序走，不要跳）

```
发现问题
  ↓
【判 1】是概率性的还是确定性的？
  ├─ 概率性（几次生成有时崩有时不崩）→ 重生成（先抬步数 4→6–8，再换种子 2–3 条）
  └─ 确定性（每次都崩，崩法一致）↓
【判 2】在 §11 硬阻断清单里吗？
  ├─ 是 → 规避（改分镜）；规避不了则降级；再不行则后置
  └─ 否 ↓
【判 3】这个信息的丢失会伤到叙事吗？
  ├─ 会 → 规避 / 降级（把信息挪到别的镜或别的手段承载）
  └─ 不会 ↓
【判 4】后期能补吗？
  ├─ 能 → 后置
  └─ 不能 ↓
【判 5】微调提示词（一次只改一处），改完回到判 1 重跑
```

### 12.3 四条选择的优先级理由

```
规避 > 降级 > 后置 > 重生成 > （最后才是）微调提示词
```

- **规避最省**：改一个动作描述，重生成风险归零
- **降级次之**：信息挪走，镜头保住
- **后置最贵**：要工时，但结果最可控（像素级稳定、可改字、可换语种）
- **重生成是概率游戏**：只在你判断"这确实是概率性崩坏"时才划算
- **微调提示词代价最高**：改一处就要重跑一轮，且在低步数下评估的结论不可靠

### 12.4 分镜表必须字段

| 列 | 控件 | 枚举值 | 规则 |
|---|---|---|---|
| `风险类型` | 单选下拉 | §10.6 的 9 码 | — |
| `风险等级` | 单选下拉 | 高 / 中 / 低 | — |
| `处置动作` | 单选下拉 | 规避 / 降级 / 后置 / 硬阻断 | — |
| `备选方案` | 文本 | — | **必填**，写降级后的具体镜头描述 |
| `是否单请求多镜` | 单选下拉 | 是 / 否 | 填"是"时，`X` 类的左右方位与 180° 轴线自动由硬阻断降为后置 |
| `采样步数` | 单选下拉 | 4（试拍）/ 6–8（出片） | 送审与交付一律 6–8 |

---

## 13. 三层检查体系

> 检查分三层：**提交前**查结构（可自动化）、**生成前**查内容（人工对照）、**生成后**看片。
> **不要把所有问题都拖到看片阶段** —— 那时候返工成本已经翻倍了。

### 13.1 第一层：结构检查（提交前，可自动化）

这 9 条可以做成脚本校验，**不过不许提交**：

```
□ 1. 三镜时长和 = 15.0s，且都是 0.5s 网格
□ 2. 每镜 ≥ 1.5s（硬下限），建议 ≥ 2.0s（设计下限）
□ 3. 承载信息镜 ≥ 3.0s
□ 4. 悬殊比 ≤ 2.5（量产）；≤ 5.5（试验，已知合法但重生成代价高）
□ 5. 本段台词 ≤45 汉字（绝对红线 47，建议 30–40）；主镜 ≤35；衔接镜 ≤6（建议无台词）；单句 ≤18
□ 6. 三镜共用锁定块逐字一致（做字符串比对，不是人眼看）
□ 7. 每镜只有 1 个运镜术语，且在官方术语表内
□ 8. 每镜最多 1 句 Do not，且该句不是裸名词否定
□ 9. 3 个镜头每一个都填了「备选方案」，无空缺
```

**补充 4 条（结构层同样可自动化）**

```
□ 10. Shot 1 不带时间戳；后续时间戳严格递增，格式 00:SS.mmm（三位小数）
□ 11. 全部时间戳落在请求时长内
□ 12. 三核心字段齐全且顺序正确：
      integrated_multimodal_description → overall_soundscape → non_diegetic_music
□ 13. non_diegetic_music 为 `N/A` 或 1–3 句声学参数描述（**禁止留空，不写 no music**）
```

### 13.2 第二层：内容检查（生成前，人工对照 9 类翻车）

| # | 翻车类型 | 检查什么 | 通过标准 |
|---|---|---|---|
| 1 | **手部异常** | 有没有精细持物（签字/持笔/插钥匙）？手部姿态写死了吗？ | 危险动作已改掉，或已用 §3.3 三档降级 |
| 2 | **肢体结构** | 有没有"同时"？人数写死了吗？多人外观拉开差异了吗？ | 全用「然后」串联；人数第一句写死 |
| 3 | **镜头流畅** | 每镜只有一个运镜吗？运镜句在句首吗？有时间连接词吗？ | 单运镜 + 运镜句前置 + `First/then/finally` |
| 4 | **身份漂移** | 锁定块是复制粘贴的吗？主光源方向写了吗？ | 逐字复制；单一主光 + 固定方向 |
| 5 | **语言文字** | 有没有在提示词里写短信原文/招牌文字？`<d>` 内外分工对吗？`<d>` 里是否加了双引号？说话人 ID 跨镜稳定吗？ | 已改成干净底板或 `illegible`；`<d>` 内默认无双引号（加了不判错，属冲突项）；`(S1)` 未重编号 |
| 6 | **物理空间** | 有没有倒水/碰撞/布料大幅飘动？距离写死了吗？ | 危险物理已改写；距离有量化声明 |
| 7 | **道具资产** | 一镜内需稳住的小物件 ≤2 件吗？有参考图槽位吗？ | 符合；且高风险资产走参考图 |
| 8 | **多镜一致** | 风格串/光位串三镜共用吗？说话人 ID 跨镜稳定吗？ | 共用；`(S1)` 未重编号 |
| 9 | **硬阻断** | 有没有踩 §11 清单？ | 踩了 → 已改分镜，不是改提示词 |
| 10 | **否定句写法**（§1.3） | 有无成串裸名词否定？单个裸名词否定是 A 类还是 B 类？否定表达总数超 1 处了吗？ | 无成串；A 类（能指给人看）已全改正向；`Do not` 句 + 裸名词否定**合并 ≤1 处** |

### 13.3 第三层：生成后检查（看片清单）

```
□ 1. 手部：逐帧看是不是五指、有没有融合 / 穿模
□ 2. 脸：三镜对比，是不是同一个人（发型 / 五官 / 年龄）
□ 3. 服装：颜色有没有中途变
□ 4. 小物件：耳环 / 戒指 / 手表在不在，左右有没有换手
□ 5. 光照：三镜主光方向是否一致
□ 6. 运镜：有没有方向反转、速度突变、末帧抖动
□ 7. 口型：对白与口型对不对得上；语种有没有串台；说话人有没有串音
□ 8. 文字：画面里有没有冒出乱码文字（invented background text）
□ 9. 收尾帧：最后一帧是不是稳定的（供下一段接）
```

**补充 5 条（H3 专属）**

```
□ 10. 对白：听到的台词与 <d> 内原文是否逐字一致（有无漏字/改词/加词）
□ 11. 画外音：画面里的人有没有跟着动嘴（应在旁白时 lips remain closed）
□ 12. 声音分层：环境音/配乐有没有拟人声或漏配乐（N/A 处是否真的无配乐）
□ 13. 台词未被渲染成画面内的字（<d> 内加双引号时重点观察，见 §7.2）
□ 14. 语速自然：台词没有被"赶"出来（rushed / slurred），即未超 §7.1 容量
```

---

## 14. 通用限制词串与使用纪律

### 14.1 词串（H3 版 · 正向锚定 + 最多一句 `Do not` 收边）

```
Exactly one person in frame, a single subject alone in the shot.
Five fingers on each hand, natural finger proportions, clean separation between fingers.
The subject's face, hair, clothing and accessories remain identical from the first frame to the last.
A single continuous camera move at constant speed, the motion smooth and even throughout.
Stable exposure and consistent colour temperature throughout; lighting direction never changes.
Rigid objects stay rigid; liquids stay inside their containers.
Single subject, uncluttered background, minimal environment, soft bokeh, clean edges.
─────────────────────────────
（收边，最多挑 1 句）Do not add other people, extra limbs, or invented background text.
```

> ⚠️ **本词串已按 §1.3 清理**。旧版此处有成串裸名词否定
> （`no additional figures, no crowd...` / `no shake, no jitter, no stutter, no flicker`），已全改正向。
> 从旧资料抄到带 `no ...` 串的词串**不要直接用**，按 §1.3 改写。

**中文对照（挂在锁定块里）**

```
单镜一镜到底，只做一个运镜，机位稳定，无晃动。画面内只有一个人，双手各五指，
手指自然弯曲并拢，关节自然。从第一帧到最后一帧，面部、发型、服装颜色与全部饰品
保持一致。光照方向、色温与色调全程恒定。画面内不出现文字，手机屏幕保持纯黑。
```

### 14.2 使用纪律（五条）

```
1. 挑 3–5 条与当前镜强相关的正向句即可 —— 不要 8 条全贴
2. 末尾最多 1 句 Do not，且前面必须有对应的正向描述
3. 堆满清单会稀释引导力 —— 真正要禁的那一条反而不生效
4. 这段约 55 英文词，已接近甜点区上沿，不要再叠加
5. 预期是「降低发生率」，不是「消除」—— 不要因为加了限制词就跳过看片检查
```

### 14.3 挑选规则（当前镜该挑哪 3–5 条）

| 当前镜特征 | 必挑 |
|---|---|
| 单人、有脸 | `Exactly one person in frame` + `face, hair, clothing remain identical` + `Stable exposure` |
| 多人 | 加 `the group stays at a fixed number throughout, the same people in the same positions`（**不挑** `Exactly one person`） |
| 手部入画 | 加 `Five fingers on each hand...` |
| 有运镜 | 加 `A single continuous camera move at constant speed` |
| 有液体/容器 | 加 `Rigid objects stay rigid; liquids stay inside their containers` |
| 有招牌/屏幕 | 加正向锚定 `every surface in frame staying plain and unmarked, showing only colour and material`，末尾一句 `Do not add invented background text.`（⚠️ 不要写 `No text...` —— 它是 A 类裸名词否定，不是正向锚定） |
| 无以上特征（空镜） | 只挑 `Single subject, uncluttered background` + `Stable exposure` |

---

## 15. 完整自检清单（按提交顺序排列，可勾选）

> **用法**：每写完一段 15 秒 3 镜提示词，从上到下过一遍。**任何一条不过，不许提交。**

### A. 提交前 · 结构（可脚本化，13 条）

```
□ A1  三镜时长和 = 15.0s，且都是 0.5s 网格
□ A2  每镜 ≥ 1.5s（硬下限），且 ≥ 2.0s（设计下限）
□ A3  承载信息镜 ≥ 3.0s
□ A4  悬殊比 ≤ 2.5（量产）/ ≤ 5.5（试验）
□ A5  本段台词 ≤45 汉字（建议 30–40）；主镜 ≤35；衔接镜 ≤6（建议无台词）；单句 ≤18
□ A6  三镜共用锁定块逐字一致（字符串比对）
□ A7  每镜只有 1 个运镜术语，且在官方术语表内
□ A8  每镜否定表达 ≤1 处（`Do not` 句 + 裸名词否定**合并计**），且该句不是裸名词否定
□ A8b 无成串裸名词否定（≥2 个并列无谓语名词短语即违规）
□ A8c 单个裸名词否定须为 B 类（只能靠变化察觉）；A 类（能指给人看）已改正向 —— 见 §1.3
□ A9  3 个镜头每一个都填了「备选方案」，无空缺
□ A10 Shot 1 不带时间戳；后续严格递增，格式 00:SS.mmm
□ A11 全部时间戳落在请求时长内
□ A12 三核心字段齐全且顺序正确
□ A13 non_diegetic_music 为 `N/A` 或 1–3 句声学参数描述（禁止留空，不写 no music）
```

### B. 提交前 · 内容（人工对照，9 类）

```
□ B1  手部：无签字/持笔/插钥匙；手部姿态已写死；已用三档降级
□ B2  肢体：无"同时"/while；人数第一句写死；多人外观已拉开差异；每人一个动作
□ B3  镜头：单运镜；运镜句前置；有 First/then/finally 时间连接词
□ B4  身份：锁定块复制粘贴未改写；主光方向与色温已写死；配饰 ≤2 件
□ B5  语言：<d> 内外分工正确（标签内只有语言标签+原话）；说话人 ID 跨镜未重编号
□ B5b 语言：<d> 内**默认未加**双引号；已加者**不判错**，属官方证据冲突项（见 §7.2）
□ B5c 语言：单句台词 ≤18 字；一镜一个说话人（两人对话已切两镜）
□ B5d 语言：画外音后紧跟 while his/her/their lips remain completely closed.
□ B6  文字：未在提示词写短信正文；招牌文字已改干净底板或声明 illegible
□ B7  物理：无倒水/碰撞/大幅布料；空间距离已量化并声明不变
□ B8  道具：小物件 ≤2 件；高风险资产已占参考图槽位；Ref2VA 已标 fully_preserved
□ B9  一致：风格串/光位串三镜共用；说话人 ID 跨镜稳定
□ B10 硬阻断：已对照 §11 清单；踩中的已改分镜而非改提示词
```

### C. 提交前 · 参数（3 条）

```
□ C1  采样步数 = 6–8（出片）；试拍才用 4
□ C2  提示词总长 ≤ 7000 字符（含中文，1 汉字 = 1 字符）
□ C3  Ref2VA 与 FL2VA 未混用（first_frame/last_frame 与 reference_* 未同时出现）
```

### D. 生成后 · 看片（14 条）

```
□ D1  手部：逐帧确认五指，无融合 / 穿模
□ D2  脸：三镜对比是同一人（发型 / 五官 / 年龄）
□ D3  服装：颜色未中途变化
□ D4  小物件：耳环 / 戒指 / 手表在，未换手
□ D5  光照：三镜主光方向一致
□ D6  运镜：无方向反转、速度突变、末帧抖动
□ D7  口型：对白与口型对得上；语种未串台；说话人未串音
□ D8  文字：画面内无乱码冒出（invented background text）
□ D9  收尾帧：最后一帧稳定，可供下一段接
□ D10 对白：听到的与 <d> 内原文逐字一致
□ D11 画外音：旁白时画面内的人未动嘴
□ D12 声音分层：环境音/配乐无异常，N/A 处确实无配乐
□ D13 台词未被渲染成画面内的字（<d> 内若加了双引号，此条必看）
□ D14 语速自然：台词未被 rushed / slurred（未超 §7.1 容量）
```

### E. 返工判定（4 条，出问题后按序走）

```
□ E1  已先抬步数到 6–8，同提示词重跑一次
□ E2  仍不合格 → 已换种子重生成 2–3 条并挑选
□ E3  仍不合格 → 已检查 Ref2VA 保留强度标记（Ref2VA 模式下）
□ E4  仍不合格 → 已对照 §11 硬阻断清单；是硬阻断则改分镜，否则才微调提示词
```

---

## 附：三句口诀

```
1. 负面写法：把"不要 X"改写成"是 Y"；写不出 Y 就改分镜。
2. 返工顺序：抬步数 → 换种子 → 查保留强度 → 查硬阻断 → 最后才改词。
3. 硬阻断：改"精确性"问题要绕开，改"概率性"问题要重生成。
```

## 附：本文待实测项汇总（写入客户交付物前必须完成）

| # | 待验证内容 | 实测方法 | 出处 |
|---|---|---|---|
| 1 | 采样步数 4 / 6–8 的实际分界（§2.5） | 同 seed 下 4/6/8 各 3 条共 9 条，盲评动作连贯性 / 音画同步 / 结构正确 | 本文 |
| 2 | 小物件复现率（§9.4） | ≥20 次，**真实运动条件下**，登记 PPR / WLR | 本文 |
| 3 | `dialogue replacement` 画面是否逐帧不变（§7.9） | 跑一次编辑模式，逐帧比对未指定区域 | 本文 |
| 4 | 2K 全精度下小字可读性（§7.6） | 同一招牌文案在 768p / 2K 各生成 10 条，统计可读率 | 本文 |
| 5 | 时间戳 ±0.12 秒精度在本项目提示词长度下的复现性（§5.7） | 10 段生成，量测实际切点与标注切点的偏差 | 本文 |
| 6 | **`<d>` 内加英文双引号是否导致台词被渲染成画面文字**（§7.2）**——官方证据冲突，优先级最高** | A/B 各 5 条：A `<d>[Chinese] 我早就知道了。</d>` vs B `<d>[Chinese] "我早就知道了。"</d>`，比对 B 组是否出现画面内文字 | **skill-voice** |
| 7 | **`no music` 与 `N/A` 是否等价**（§7.8） | 同一提示词 A 组 `N/A`、B 组 `no music`，各 5 条，比对静音轨异常与底噪 | **skill-voice** |
| 8 | **纯画外叙述者（旁白者不在画面内）写法**（§7.4） | A 组官方在画面内句式、B 组外推句式，各 5 条，比对是否出现画面内人物动嘴或音色错配 | **skill-voice** |
| 9 | **`<cutoff>` 在片中打断是否生效**（§7.5） | A 组片中打断用 `<cutoff>`、B 组用画面事件句（`a door slams and cuts her off`），各 5 条，比对收声位置 | **skill-voice** |
| 10 | **配乐进点写在人声之后是否提升对白可懂度**（§7.8） | A 组不写进点、B 组写 `entering after she finishes speaking`，各 5 条，盲评对白可懂度 | **skill-voice** |
| 11 | 模型实际中文语速（是否等于 4.5 字/秒） | 固定 20 字台词，测实际发音时长，反推字/秒，回填 §7.1 | **skill-voice** |
| 12 | 11 语言可懂度 / 11 语言之外是否可用（§7.1） | 每语言 5 条固定台词，盲评可懂度；再试 2 种语言外语种 | **skill-voice** |
| 13 | 齐声 `(S1,S2)` 的可懂度（§7.2） | 齐声台词 5 条，盲评是否听得出是两人同时说 | **skill-voice** |
| 14 | **H3 是否存在 `negative_prompt` 独立通道**（§0、§1.1）**——现有"无该字段"证据出自 Hailuo 2.3，非 H3 官方** | 在所用接口/平台提交一个带 `negative_prompt` 的请求，观察是**报错 / 被忽略 / 生效**三种结果中的哪一种；或直接查该平台 H3 的参数表 | **team-lead** |

> 第 6–13 项的实测方法与判据由 **skill-voice** 在 `h3-dialogue-voice` 中给出，本文直接引用以保持两份 skill 口径一致。
> ⚠️ **第 14 项与第 6 项同属"来源错配"风险**：本项目多份调研曾把 Hailuo 2.3 的规格当作 H3 使用。**凡引用外部参数表/对照表，须先确认其针对的型号是 H3 而非 2.3。**
> **共同原则：未实测前，上述项一律不得写进客户交付物。**
