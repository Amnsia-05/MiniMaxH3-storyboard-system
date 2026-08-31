---
name: h3-dialogue-voice
description: 海螺 H3 视频提示词中「对白 / 语速 / 声音三层 / 口型同步 / 旁白」的写法规范，含 <d> 标签规则、说话人 ID、语速换算表、可复制模板。触发词：H3对白、H3语速、H3台词容量、H3旁白、H3口型同步、H3声音、H3说话人。
agent_created: true
---

# H3 对白 / 语速 / 声音三层 / 口型同步 / 旁白 写法规范

> 本 skill 只解决一件事：**在 MiniMax 海螺 H3 的提示词里，声音这部分怎么写才不翻车。**
> 镜头、运镜、时间戳、资产一致性见 `minimax-h3-storyboard`；本文件是它的**声音侧下钻**。
>
> **写作纪律**：标注 **【官方原文】** 的条目逐字摘自 MiniMax 官方 `base-en.txt` / `ref-en.txt` / 官方 API 文档 / 官方模型卡，不得改写；**【业界】** 为可查第三方实测与投放样本；**【推断】** 为本项目推导；**【待验证】** 为未经实测确认、必须自行跑一次再写进 SOP 的条目。**严禁编造数据，不确定的一律标【待验证】并给实测方法。**

---

## 0. 三十秒速查（贴墙用）

```text
对白     The woman with a low, steady voice (S1) says: <d>[Chinese] 我早就知道了。</d>
        ↑身份/ID/动作/语气在标签外          ↑标签内只有：语言标签 + 原话，逐字不译

旁白     The man (S1) says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d>
        while his lips remain completely closed.          ← 这两句必须成对，漏后半句必穿帮

跨镜     <scenetrans> 打在两处连接点 + 明写 continues seamlessly across the cut
截断     <cutoff> 打在视频结尾被打断处

声音三层  ① integrated_multimodal_description = 角色听得见的（对白、剧情内音乐、演唱）
        ② overall_soundscape      = 环境音/物理动作音/非语言人声（1–4 句，禁重复对白）
        ③ non_diegetic_music      = 只有观众听得见的配乐（1–3 句，只写乐器/速度/节奏/动态）

判别口诀   问一句"画面里的人能不能听见这个声音"
语速      T ≈ 字数 ÷ 3.15   ｜   15s：写作 38 字 / 定稿 ≤45 / 硬红线 47（详见 §3.7）
口型      一镜一个说话人：If two people need to talk, cut between them.
```

**一句话原则**：H3 **原生出声、与画面同一次推理生成**，所以声音不是后期补的，而是**提示词直接决定**的。写错一处，整条片子直接废。

---

## 1. 对白标签 `<d>`：`</d>`（最容易写错的一处）

### 1.1 官方原文

> **【官方原文】**
> `Place the speaker's identifying phrase, ID, action, and delivery outside <d>. Inside <d>, include only the language tag and the actual user-provided spoken content. Preserve every original word and punctuation mark verbatim; do not translate or rewrite them.`

拆成四条硬性动作：

| # | 规则 | 官方用词 |
|---|---|---|
| 1 | 说话人**识别短语**、**ID**、**动作**、**语气（delivery）** 全部放 `<d>` **外面** | identifying phrase, ID, action, and delivery |
| 2 | `<d>` **里面**只放两样东西：**语言标签** + **用户提供的原话** | only the language tag and the actual spoken content |
| 3 | 逐字保留**每一个词和每一个标点** | Preserve every original word and punctuation mark verbatim |
| 4 | **不翻译、不改写** | do not translate or rewrite them |

> **只有 `<d>` 标签里的东西会被念出来。**（"Only what sits inside the tag is spoken, so stage directions never get read aloud."）所以写进去的任何描述性文字都会被当成台词念出来——这是 `<d>` 规则最要命的一条。

### 1.2 结构模板（可直接复制）

```text
<说话人识别短语> (<ID>) <动作/语气动词>: <d>[<语言标签>] <原话></d>
```

### 1.3 正反例对照（逐条）

**✅ 正确（官方例句，逐字）**

```text
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
```

中：声音轻、带气声的年轻女人 (S1) 说：`<d>[English] I get off at the next station.</d>`
中：两个孩子 (S1,S2) 一起喊：`<d>[English] Wait for us!</d>`

```text
The woman with a low, steady voice at a measured pace (S1) says: <d>[Chinese] 陈总，这份合同我一个字都不会改。</d>
```

中：语速平稳、声音低沉的女人 (S1) 说：`<d>[Chinese] 陈总，这份合同我一个字都不会改。</d>`

**❌ 错误 1：缺 `<d>` 标签** —— 台词会被当成画面描述，可能不发声或变成画面内文字

```text
❌ The young woman (S1) says: [English] I get off at the next station.
✅ The young woman (S1) says: <d>[English] I get off at the next station.</d>
```

**❌ 错误 2：身份/语气写进标签里** —— 描述会被**念出来**

```text
❌ <d>[English] The young woman with a breathy voice says: I get off at the next station.</d>
✅ The young woman with a breathy voice (S1) says: <d>[English] I get off at the next station.</d>
```

**❌ 错误 3：把台词翻译成提示词语言** —— 违反 `do not translate`

```text
❌ The woman (S1) says: <d>[Chinese] 我下一站下车。</d>   ← 原文是英文却翻成了中文
✅ The woman (S1) says: <d>[English] I get off at the next station.</d>
```

**❌ 错误 4：改标点 / 加省略号 / 加语气词**

```text
❌ <d>[Chinese] 我早就知道了……</d>      ← 原稿无省略号，擅自加
✅ <d>[Chinese] 我早就知道了。</d>
```

**❌ 错误 5：标签内写舞台提示**

```text
❌ <d>[Chinese] （冷笑）你觉得我会信吗？</d>
✅ She lets out a short cold laugh, then the woman (S1) says: <d>[Chinese] 你觉得我会信吗？</d>
```

**❌ 错误 6：`<d>` 未闭合 / 大小写写成 `<D>`**

```text
❌ ...says: <D>[Chinese] 站住。
✅ ...says: <d>[Chinese] 站住。</d>
```

### 1.4 语言标签的写法

H3 **稳定支持 11 种语言**（官方模型卡）：

`Arabic` / `Chinese` / `English` / `French` / `German` / `Italian` / `Japanese` / `Korean` / `Portuguese` / `Russian` / `Spanish`

| 语言 | 标签写法 | 例句 |
|---|---|---|
| 中文 | `[Chinese]` | `<d>[Chinese] 我早就知道了。</d>` |
| 英文 | `[English]` | `<d>[English] I get off at the next station.</d>` |
| 日文 | `[Japanese]` | `<d>[Japanese] もう帰る時間だ。</d>` |
| 韩文 | `[Korean]` | `<d>[Korean] 이제 그만하자.</d>` |
| 阿拉伯语 | `[Arabic]` | `<d>[Arabic] سأغادر الآن.</d>` |

- 标签**首字母大写**，方括号，紧贴 `<d>` 之后，后接一个空格。
- **11 种之外**的语言（如泰语、越南语、粤语、方言）**不在官方稳定支持清单内**，属【待验证】。实测方法见 §9.5。

### 1.5 ⚠️ 双引号：存在官方口径冲突，默认不加【待验证·未定论】

**两条官方来源说法相反，本节如实并列，不做单边裁剪。**

**证据一 · 官方 `base-en.txt`**：对白例句**无双引号**（`The two children (S1,S2) shout together, <d>[English] Wait for us!</d>`）；双引号被官方**专属定义**给画面内可见文字（`Place any banner, sign, label, subtitle, or neon text that is actually visible on screen in English double quotation marks`），例句 `A red neon sign reading "营业中" glows above the doorway.`

**证据二 · MiniMax × ComfyUI 官方直播**（出处 `防翻车限制词库_H3版.md` 第 97 行）：*把输入音频作为 reference 的同时，在提示词里用引号写出角色要说的台词，并放进对应镜头的描述中——两者并用可显著提升对白稳定性与一致性。*

**无法确认三点**（标【待验证】）：① 直播技巧是否与 `<d>` 并用，官方未说明；② 原话以"配 reference 音频"开头，**可能仅限该场景，直接当作通用规则推广不成立**；③ 成文文档权威高于口头演示，但后者可能反映更新的工程实践。

| 场景 | 写法 | 强度 |
|---|---|---|
| 默认 / 无 reference 音频 | `<d>[Chinese] 我早就知道了。</d>` 不加引号 | ✅ 默认遵守 |
| 画面内可见文字 | `A red neon sign reading "营业中"` 必须加引号 | ✅ 强制 |
| 若采用直播技巧（配 reference 音频时） | 引号写在**镜头描述**里，**不写进 `<d>` 内** | 🔶 可选 |
| `<d>` 内叠加引号 | `<d>[Chinese] "我早就知道了。"</d>` | ⚠️ 不推荐 |

**不推荐理由**：两套语义共用一组符号，台词与招牌可能被混同。**但这是推论，不是实测结论**——故标【待验证】。

> **旧判定已修正**：项目内叠加引号的写法，此前判为"无官方支持的错误"，现改为**出处可考（源自直播技巧）、适用范围不明（`<d>` 内未经官方确认）**。
> **实测（各 5 条，同 seed/duration/画面描述）**：A 组无引号、B 组 `<d>` 内加引号，比对 B 组是否出现台词被渲染成画面内文字、两组发音清晰度。**补 C 组**：配 reference 音频时引号写在镜头描述层，与 A 组比对对白稳定性；**C 组显著更优则证明技巧成立且应落在描述层**。结果回填本节。

---

## 2. 说话人 ID 系统

### 2.1 编号规则【官方原文】

> `stable IDs such as (S1) and (S2)`
> `A speaker keeps the same ID across shots; characters who never vocalize receive no speaker ID.`
> 齐声：官方例句写作 `(S1,S2)`

| 规则 | 说明 |
|---|---|
| 格式 | `(S1)` `(S2)` `(S3)` …，**大写 S + 阿拉伯数字，圆括号** |
| 齐声 | `(S1,S2)` —— **逗号无空格** |
| **跨镜头 ID 不变** | 同一说话人在 Shot 1 / Shot 2 / Shot 3 里始终是同一个 ID |
| **跨段落 / 跨集 ID 不变** | 主角在第 1 集是 (S1)，第 20 集也必须是 (S1) |
| **不出声的角色不给 ID** | 群演、路人、只做表情的角色一律不编号 |
| 编号起点 | 永远是 `S1`，从 1 连续递增，不跳号 |

### 2.2 ID 与角色卡的绑定（工程做法）

角色卡里固定一行，**全剧不改**：

```markdown
### 声音
- 说话人 ID：(S1)　← 全剧恒定，跨镜跨集不重编号
- 音色 pitch/timbre：low, steady（低沉、稳定）
- 语速 speaking rate：measured（平稳）
- 口音 accent：无
- 首次出场身份句（英文，逐字复用）：
  The woman with a low, steady voice at a measured pace (S1)
```

**一旦分配，全剧任何提示词里都逐字复制这一句**，不做同义替换。

### 2.3 首次出场：视觉 + 听觉双维建身份【官方原文】

> 首次出场需从视觉 + 听觉两维交代：`character type, age, gender, whether the person is on-screen, pitch, timbre, speaking rate, or accent`

八个维度不用写全，但**听觉维度至少命中 2 个**（推荐 pitch + timbre，或 timbre + speaking rate）：

| 维度 | 官方英文 | 可选词（可直接挑） |
|---|---|---|
| 角色类型 | character type | `the young woman` / `the middle-aged man` / `the teenage boy` |
| 年龄 | age | `28-year-old` / `in his sixties` |
| 性别 | gender | `woman` / `man` / `girl` / `boy` |
| 是否在画内 | whether the person is on-screen | `on-screen` / `off-screen` / `speaking from off-frame right` |
| 音高 | pitch | `low` / `high` / `deep` / `soft` |
| 音色 | timbre | `raspy` / `breathy` / `husky` / `warm` / `nasal` / `clear` / `gravelly` |
| 语速 | speaking rate | `at a measured pace` / `rapid-fire` / `unhurried` / `halting` |
| 口音 | accent | `with a faint northern accent` / `with a slight British accent` |

**✅ 首次出场身份句（可复制）**

```text
The 28-year-old woman with a low, steady voice at a measured pace (S1)
中：声音低沉稳定、语速平稳的 28 岁女人 (S1)

The middle-aged man with a calm, slightly raspy voice (S1)
中：声音平静、略带沙哑的中年男人 (S1)   ← 官方例句用词

The teenage boy with a high, breathless voice (S2)
中：声音偏高、带着喘息感的少年 (S2)
```

**❌ 反例**

```text
❌ A woman says: <d>[Chinese] 我早就知道了。</d>
   ← 无 ID、无听觉维度、无识别短语。模型不知道这是谁，下一段换个人说就串音。

❌ The woman (S1) says: <d>[Chinese] 我早就知道了。</d> ... [Shot 2] ... the woman (S2) says: ...
   ← 同一人换了 ID，这是「说话人串音」的头号根因。

❌ An old man stands by the window. (S2) ...（他全程没说话）
   ← 不出声的角色给了 ID，占用编号且可能诱导模型让他出声。
```

### 2.4 ID 复用与"沉寂后重现"

角色在多段之后再次出场时，**不要重新建身份句**（会覆盖已有音色记忆），只做**ID 回指**：

```text
[Shot 2] At 00:05.000, the camera cuts to the same 28-year-old woman (S1), who says: <d>[Chinese] 你还是没变。</d>
中：镜头切到同一个 28 岁女人 (S1)，她说：`<d>[Chinese] 你还是没变。</d>`
```

> **判定口诀**：**身份句只在首次出场写一次；之后永远只写 `the same ... (S1)`。**

---

## 3. 语速体系

### 3.1 一个必须先接受的事实

> **H3 原生生成音频并与画面同一次推理，自带唇形同步。语速不再是"可配置参数"，而是"模型的输出行为"。**
> 因此本章所有表格是**时长校验表**，不是配置表——用来判断写好的台词能不能塞进既定镜长，以及留多少余量。

### 3.2 语速档位表【业界】

| 档位 | 字/分 | 字/秒 V | 适用场景 |
|---|---|---|---|
| 慢速（情感 / 悬疑铺垫） | 180–220 | **3.0–3.7** | 悬念制造、情绪独白、旁白 |
| 中速（通用口播） | 260–280 | **4.3–4.7** | 短剧对白默认档 |
| 快速（冲突爆发） | 340 | **5.7** | 争吵、爽点爆发句 |
| **AI 配音工程基准** | 270 | **4.5** | 流水线通用校验值【工程取值】 |

【业界】2026 年一线投放样本（400+ 条）：**4.3–4.8 字/秒完播率最优**；**低于 3.5 字/秒前 3 秒易被划走**。

### 3.3 换算公式

```text
镜头/段落时长   T = 台词字数 W ÷ 语速 V ÷ 台词占用率 ρ
台词字数上限   W_max = T × V × ρ

代入 V = 4.5、ρ = 0.70  →  简化式：T ≈ W ÷ 3.15      W_max ≈ T × 3.15
```

- `ρ = 0.70`：台词只占镜头时长的 70%，剩下 30% 留给停顿、换气、画面呼吸与起落白。【业界】建议台词不超过容量 80%。
- 例：35 字台词 → `T = 35 ÷ 3.15 ≈ 11.1 秒` → 主镜给 11 秒或 12 秒。

### 3.4 各时长台词容量对照表（ρ=0.70，V=4.5，**四舍五入**）

| 镜长 T | 台词字数上限 | 对应分镜范式 | 备注 |
|---|---|---|---|
| 2.0s | **6 字** | 衔接镜（入镜 / 出镜） | 建议**无台词**，纯音效更稳 |
| 3.0s | **9 字** | 四镜快切 / 短反应镜 | |
| 3.5s | **11 字** | 四镜对话 | |
| 4.0s | **13 字** | 四镜对话 / 快切 | |
| **5.0s** | **16 字** | 三镜标准（默认） | 单句上限参考值 |
| 7.0s | **22 字** | 三镜重主镜 | |
| 7.5s | **24 字** | 双镜长对白 | ⚠️ 仅台词确实需要时用 |
| 10.0s | **32 字** | 三镜重主镜 / 双镜 | |
| **11.0s** | **35 字** | **三镜主镜（B 镜）默认** | |
| **15.0s** | **47 字** | 单镜 / 单元总量 | **硬上限** |

> **衔接镜口径**：本表 2.0s → **6 字**（2.0 × 3.15 = 6.3）；主模板 §4.3 给 **≤7 字**（对应 2.2s）。差异只在舍入方向，**取小者按 6 字执行，更稳妥是衔接镜无台词**。本表 5.0s→16、7.5s→24、11.0s→35 与主模板完全对得上，可互查。

### 3.5 不同语速下的 15 秒容量

| 语速 V | 满容量（ρ=1.0） | 建议上限（ρ=0.70） | 备注 |
|---|---|---|---|
| 3.5 | 52 字 | **36 字** | 情感独白段 |
| 4.0 | 60 字 | **42 字** | |
| **4.5** | 67 字 | **47 字** | **推荐默认，计算值** |
| 4.8 | 72 字 | **50 字** | 冲突爆发段硬上限 |
| 5.7 | 85 字 | **60 字** | 仅争吵使用，可懂度风险高 |

### 3.6 官方口径交叉验证

> **⚠️ 勘误（旧推导已作废）**：曾把官方"10 秒片段 20–25 词"反推为 `25 ÷ 2.5 = 10s → 10 × 4.5 = 45 字`，称其"独立收敛到 45"。**这是量纲错误**：该式的 45 字是 **10 秒 / ρ=1.0**，47 字是 **15 秒 / ρ=0.70**，不可比——§3.4 表 10.0s 对应 **32 字**已直接证伪。**两者撞在一起是 15vs10、0.70vs1.0 恰好抵消的巧合，不是互相印证。** 已与 `h3-antibug-check` 同步撤下。

**正确推导**（统一到 15 秒 / ρ=0.70；1 英文词 ≈ 1.8 汉字，由 4.5 字/秒 ÷ 2.5 词/秒 得）：

| 路径 | 计算 | 结果 |
|---|---|---|
| **① 时长公式（本项目）** | 15s × 4.5 字/秒 × ρ 0.70 | **47 字** |
| **② 官方天花板速率** | 2.5 词/秒 ≡ 4.5 字/秒 → 15 × 4.5 × 0.70 | **47 字** |
| **③ 官方舒适速率** | 舒适值 20 词/10s = 2.0 词/秒 ≡ 3.6 字/秒 → 15 × 3.6 × 0.70 | **38 字** |
| **③b 等价算法** | 47 字 × 官方舒适/天花板比 (20/25 = 0.80) | **38 字** |

**官方口径能独立支撑的只有两个数：天花板 47 字、舒适值 38 字。** 45 无独立推导，只是 47 减约 4% 的安全边，**不得对外宣称 45 有官方依据**。

> **官方原文（已核实所指是"被念出的台词容量"，不是提示词描述长度）**：
> *"Only what sits inside the tag is spoken, so stage directions never get read aloud. Around twenty words fit comfortably in a clip, about ten to a line; pack in more and the delivery rushes, then slurs."*
> *"A 10-second clip fits maybe 20-25 spoken words total if you want anything else to happen."*

**推论**：20 英文词是**舒适值**、25 词是天花板，**二者都是 10 秒片段的数字**，引用前须先换算到目标时长与 ρ。折算到 15 秒：舒适 38 字、天花板 47 字。

### 3.7 三档口径定稿（照这个写）—— 不单值化

| 口径 | 数值 | 角色 | 依据 |
|---|---|---|---|
| **写作目标** | **38 字 / 15s**（区间 30–40） | 正常照这个写 | ✅ 官方推导值（§3.6 ③：舒适速率 2.0 词/秒 ≡ 3.6 字/秒） |
| **工程定稿 / 常规判据** | **≤ 45 字 / 15s** | **结构检查按这条判** | 🔶 安全边，非推导值（47 减约 4%） |
| **硬红线 / 例外批准上限** | **47 字 / 15s** | 超过必返工，无例外 | ✅ 官方推导值（§3.6 ①②） |
| **单句上限** | **≤ 18 字（硬）/ 12–15（建议）** | 逐句检查 | 官方"about ten to a line"折算。**"句"＝换气单元，断点 `，。！？；`**（§4.1 规则 3） |

**三档为什么不合并**：

- **47 不冗余**：它是"剧情硬要求塞 46 字时"唯一的上界参照。只留 45 会让该场景要么无脑放行、要么无脑返工。
- **45 的理由是工程性的，不是数学性的**：模型实际语速不可控，说过快会含糊、过慢会被结尾截断。**安全边的正当性来自风险，不来自公式**。
- **38 才是推导值**：官方舒适速率折算而来，是"为什么建议 30–40"的真正出处。

> **46 字怎么判**：不算"破例免检"，而是**需人工确认**——负责人确认该句无法再压缩并在分镜表备注写明理由。"破例"易被理解成免检，不要用。

### 3.8 不同情绪的语速选择

| 情绪 / 场景 | 选 V | 怎么写 delivery（放 `<d>` 外，官方允许位） | 20 字台词需时 |
|---|---|---|---|
| 悬念制造 / 情绪独白 | 3.0–3.7 | `says slowly` / `says after a long pause` / `in a low, unhurried murmur` | ~5.7s |
| 回忆旁白 / 抒情 | 3.5–4.0 | `says in a soft, reflective voice` | ~5.3s |
| 日常对白（默认） | 4.3–4.7 | `says evenly` / `replies`（不写速度词，交给默认） | ~4.4s |
| 说明 / 推进信息 | 4.5 | `says at a measured pace` | ~4.4s |
| 焦急 / 赶时间 | 5.0–5.7 | `says in a rushed, breathless voice` | ~3.8s |
| 争吵 / 爆发 / 爽点 | 5.7 | `snaps` / `says through clenched teeth` / `cuts in sharply` | ~3.5s |

```text
✅ 慢速：She pauses, then the woman (S1) says slowly: <d>[Chinese] 我数到三，你再想想。</d>
中：她停顿一下，然后女人 (S1) 缓慢地说：`<d>[Chinese] 我数到三，你再想想。</d>`

✅ 快速：She snaps, the woman (S1) cutting in sharply: <d>[Chinese] 闭嘴。现在就走。</d>
中：她猛地打断，女人 (S1) 厉声说：`<d>[Chinese] 闭嘴。现在就走。</d>`

❌ 错误：把速度指令写进标签里（会被念出来）
<d>[Chinese] （快速）闭嘴。现在就走。</d>
```

> **【待验证】** delivery 副词对 H3 实际输出语速的**引导强度**未量化。实测方法：同一句 20 字台词，分别挂 `says slowly` / `says` / `says in a rushed, breathless voice`，各生成 5 条，用音频软件量出实际发音时长，算出真实 V 值，**回填 §3.2 表**。

### 3.9 字幕（后期叠加，不在提示词里）

【业界】单行 **12–15 字**；断句对齐换气点；**字幕比语音早 0.2s 结束**。字幕一律后期叠，不写进 H3 提示词。

---

## 4. 台词写作规范

### 4.1 六条硬规则

| # | 规则 | 理由 |
|---|---|---|
| 1 | **口语化**，写"能说出口的话" | 书面语念出来僵硬，且吃掉字数 |
| 2 | **一句一个信息点** | 15 秒单元只有 1 个信息点或 1 个情绪转折，二者不可兼得。**信息点＝可单独删除的最小语义单元（事实／决定／指控／问题）；判定法：能拆成几句各自成立的话，就有几个信息点** |
| 3 | **断句对齐换气点** | 断点 `，。！？；`；段内 12–15 字（同字幕单行），硬上限 18 字 |
| 4 | **字数按 §3.4 表卡死** | 超了就是塞不进 |
| 5 | **画面能说的，台词就别说** | 台词与画面重复 = 双倍占时，零信息增量 |
| 6 | **台词逐字锁定后不改** | 改词会改变时长，口型节奏对不上 |

### 4.2 台词与画面的分工

> **核心原则：信息用台词，转折用画面；或反过来。不要都压在台词上。**

| 承载方式 | 适合 | 不适合 |
|---|---|---|
| **台词** | 事实、数字、名字、决定、威胁、指令 | 心理活动、情绪、氛围 |
| **画面** | 情绪转折、心理外化、关系、环境 | 抽象概念、前史、因果 |

```text
❌ 全压台词（3 个信息点挤一句，情绪全用台词说，画面无事可做）：
<d>[Chinese] 我很伤心很难过，我觉得你背叛了我，我们结束吧。</d>   （26 字，**未超容量**）

✅ 台词给事实、画面给情绪：
She keeps her head down; her jaw tightens, then the woman (S1) says: <d>[Chinese] 我们结束吧。</d>
中：她低着头，下颌绷紧，然后女人 (S1) 说：`<d>[Chinese] 我们结束吧。</d>`   （6 字）
```

### 4.3 跨镜台词拆分（15 秒 3 镜模板）

| 镜 | 时长 | 台词配额 | 写法 |
|---|---|---|---|
| A 入镜 | 2.0s | **0–6 字，建议 0** | 无台词，纯环境音 + 动作，让观众入戏 |
| B 主镜 | 10–11s | **30–35 字** | 台词主场 |
| C 出镜 | 2–3s | **0–9 字，建议 0** | 无台词，留白 + 配乐收尾 |

**分配检查**：`A(0) + B(35) + C(0) = 35 字 ≤ 45` ✅

### 4.4 拆分长台词的三种手法

**手法一：砍**（首选）

```text
原：其实我早就知道你那天晚上去了哪里，只是我一直没有说而已。（29 字）
砍：<d>[Chinese] 那天晚上，你去了哪儿。</d>   （12 字）
```

**手法二：拆到两镜（用 `<scenetrans>`，见 §6）**

```text
[Shot 1] ... says: <d>[Chinese] 那天晚上你去了哪儿，<scenetrans></d>
[Shot 2] At 00:08.000, ... her line continues seamlessly across the cut, <d>[Chinese] <scenetrans> 别告诉我你在加班。</d>
```

**手法三：转成画面**

```text
原：<d>[Chinese] 我恨你。</d>
转：She turns her back on him and walks out of frame, her lips pressed into a thin line.
中：她背过身走出画面，嘴唇抿成一条直线。
```

### 4.5 台词字数自检（写完后必做）

```text
1. 数单元内所有 <d> 标签里的汉字 + 标点总数
2. ≤ 45 → 通过；46–47 → 警告，改词或拆镜；> 47 → 硬失败，必须拆
3. 数单句最长的一句：> 18 字 → 断句
4. 数每个说话人的总字数，按 §3.4 表校验所在镜长是否够
```

---

## 5. 画外音与旁白

### 5.1 官方原文（两句必须成对）

> **【官方原文】**
> `For voiceover, use the exact phrase "says in an off-screen voiceover". Immediately after every voiceover <d> block, state that the corresponding on-screen character's lips remain closed:`
>
> `The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.`

两条不可拆：

| 组成 | 官方原文 | 不可替换 |
|---|---|---|
| 前半句 | `says in an off-screen voiceover` | 官方要求 `use the exact phrase`，**不得换成 `narrates` / `says in a voiceover` / `voices over`** |
| 后半句 | `while his lips remain completely closed.` | 官方原句，逐字复制；人称按角色改 `his` / `her` / `their` |

> **漏掉后半句 = 画面里的人跟着动嘴，口型与旁白打架，这是 H3 旁白的头号穿帮。**

### 5.2 可直接复制的模板

```text
The <识别短语> (S1) says in an off-screen voiceover: <d>[Chinese] <旁白内容></d> while <his/her/their> lips remain completely closed.
```

**中文旁白**

```text
The man (S1) says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d> while his lips remain completely closed.
中：男人 (S1) 以画外音旁白说：`<d>[Chinese] 我还记得那条路。</d>`，画面中他的嘴唇完全闭合。
```

```text
The 28-year-old woman (S1) says in an off-screen voiceover: <d>[Chinese] 那是二〇一九年的冬天，雪下了一整夜。</d> while her lips remain completely closed.
中：28 岁的女人 (S1) 以画外音旁白说：`<d>[Chinese] 那是二〇一九年的冬天，雪下了一整夜。</d>`，画面中她的嘴唇完全闭合。
```

**英文旁白**

```text
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```

### 5.3 三种适用场景

| 场景 | 画内角色在做什么 | 写法要点 |
|---|---|---|
| **回忆旁白** | 看着照片 / 望向窗外 / 静坐 | 旁白 + `lips remain completely closed` + 画面只做微表情 |
| **上帝视角解说** | 角色在画面里行动但不出声 | 旁白者可**不在画面中**，见 §5.4 |
| **内心独白** | 角色特写，无口型动作 | 同上，画面只给眼神与呼吸。⚠️ **大特写（2–3s）时"眼神"须写保持态**：`her gaze holds level, she blinks once`——**禁用 `gaze drifts`**（`h3-expression-psych` §4.3.2，中高风险） |

### 5.4 ⚠️ 旁白者不在画面里时怎么写

官方例句里的 `while his lips remain completely closed` 前提是「旁白者在画面里」。若旁白者是**纯画外叙述者**（画面里根本没有他），应改写为**画外声明 + 画内所有人不出声**：

```text
An unseen narrator with a low, unhurried voice (S1) says in an off-screen voiceover: <d>[Chinese] 那年冬天，没有人再提起他的名字。</d> On screen, the woman sits by the window; her lips remain completely closed throughout.
中：一个声音低沉从容、不可见的叙述者 (S1) 以画外音旁白说：`<d>[Chinese] 那年冬天，没有人再提起他的名字。</d>` 画面中，女人坐在窗边，全程嘴唇完全闭合。
```

> **【推断】** 官方原文只给了"旁白者在画面里"的例句。纯画外叙述者的写法是本项目按官方规则外推的，标 **【待验证】**。实测方法：各生成 5 条，看画面里是否出现"不该出现的嘴部动作"或"是否凭空多出一个人"。

### 5.5 旁白与台词的字数

**旁白同样占用语速容量。** 15 秒单元内「台词 + 旁白」总字数一起卡 §3.7 的 45 字。旁白多用 3.0–3.7 字/秒慢速档（情感铺垫），同样字数需**更长时长**：

| 旁白字数 | 慢速 3.5 字/秒 | 中速 4.5 字/秒 |
|---|---|---|
| 20 字 | 8.2s | 6.3s |
| 30 字 | 12.2s | 9.5s |
| 35 字 | 14.3s | 11.1s |

### 5.6 正反例

```text
✅ 正确（两句成对、官方原句、标签规范）
The man (S1) says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d> while his lips remain completely closed.

❌ 错误 1：漏掉后半句 → 画内人跟着动嘴
The man (S1) says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d>

❌ 错误 2：把官方短语换掉
The man (S1) narrates: <d>[Chinese] 我还记得那条路。</d> while his lips remain closed.

❌ 错误 3：后半句语义弱化
... while he does not speak.        ← 应写 lips remain completely closed（官方原句）

❌ 错误 4：把"画外音"写进 <d> 里（会被念出来）
<d>[Chinese] （画外音）我还记得那条路。</d>
```

---

## 6. 跨镜连续台词与截断

### 6.1 官方原文

> **【官方原文】**
> `When the same line of dialogue or lyrics crosses a cut, use <scenetrans> at the connecting points in both parts and explicitly state that the audio continues across the cut. Use <cutoff> when speech is truncated by the end of the video.`

连续性措辞（官方列出四选一）：
`continues seamlessly across the cut` / `continues uninterrupted into the next shot` / `carries over from the previous shot` / `remains audible across the transition`

### 6.2 `<scenetrans>` 三条硬规则

| # | 规则 |
|---|---|
| 1 | **两处连接点都要标** —— 前半句结尾标一次，后半句开头标一次 |
| 2 | **必须明写音频跨切点连续** —— 四选一措辞，不可省略 |
| 3 | 说话人 **ID 必须相同** |

### 6.3 可直接复制的模板

```text
【Shot 1 结尾】
... the woman (S1) says: <d>[Chinese] 我从来没想过 <scenetrans></d>

【Shot 2 开头】
[Shot 2] At 00:05.000, ... her sentence continues seamlessly across the cut, <d>[Chinese] <scenetrans> 你会回来。</d>
```

**完整英文版**

```text
... and says: <d>[English] I never thought <scenetrans></d>
[Shot 2] At 00:05.000, ... her sentence continues seamlessly across the cut, <d>[English] <scenetrans> that you would come back.</d>
```

### 6.4 `<cutoff>` 用法

用于**视频结束时话还没说完**（被片尾截断），制造"话没说完"的钩子：

```text
... the woman (S1) says: <d>[Chinese] 其实我早就知 <cutoff></d>
中：……女人 (S1) 说：`<d>[Chinese] 其实我早就知 <cutoff></d>`（话被片尾截断）
```

| 标记 | 触发条件 | 位置 |
|---|---|---|
| `<scenetrans>` | 一句台词**跨两个镜头** | 两处连接点各一次 |
| `<cutoff>` | 台词被**视频结尾**截断 | 句尾，一次 |

### 6.5 与叙事卡点的配合

`【业界】台词卡点`：**在关键词之前切断**，下一段承接补全。

```text
Shot 3 结尾：<d>[Chinese] 其实我早就知——<cutoff></d>
下一段 Shot 1：<d>[Chinese] <scenetrans> 道你那天去了哪儿。</d>
```

### 6.6 正反例

```text
✅ 正确（两处都标 + 明写连续 + ID 一致）
[Shot 1] ... the woman (S1) says: <d>[Chinese] 我从来没想过 <scenetrans></d>
[Shot 2] At 00:05.000, ... her line continues seamlessly across the cut, <d>[Chinese] <scenetrans> 你会回来。</d>

❌ 错误 1：只标一处
[Shot 1] ... says: <d>[Chinese] 我从来没想过 <scenetrans></d>
[Shot 2] At 00:05.000, ... <d>[Chinese] 你会回来。</d>     ← 后半段没标

❌ 错误 2：没写连续措辞
[Shot 1] ... says: <d>[Chinese] 我从来没想过 <scenetrans></d>
[Shot 2] At 00:05.000, ... <d>[Chinese] <scenetrans> 你会回来。</d>   ← 缺 continues seamlessly across the cut

❌ 错误 3：跨切点换了 ID
[Shot 1] ... (S1) says: <d>[Chinese] 我从来没想过 <scenetrans></d>
[Shot 2] At 00:05.000, ... (S2) says: <d>[Chinese] <scenetrans> 你会回来。</d>   ← 串音

❌ 错误 4：把 scenetrans 写成 scenetransition / scene-trans
```

> **【待验证】** `<cutoff>` 的触发是"视频结尾截断"还是"任意中断"，官方原文表述为 `truncated by the end of the video`，字面指视频结尾。若在片中就想让话被打断，**建议改用画面事件打断**（如 `a door slams and cuts her off`），而非依赖 `<cutoff>`。实测方法：把 `<cutoff>` 放在 Shot 1 结尾（非视频结尾）生成 5 条，看是否被正确截断。

---

## 7. 声音三层详解

### 7.1 三层定义与分工【官方原文】

| 层 | 字段 | 官方定义 | 句数 | N/A 条件 |
|---|---|---|---|---|
| **① 剧情内** | `integrated_multimodal_description` | "Describes visuals, actions, shots, speakers, dialogue, singing, and **diegetic** audio along the timeline." | 无上限 | 不可 N/A |
| **② 音景** | `overall_soundscape` | "Summarizes **ambient sound, physical action sounds, and non-verbal human sounds** across the entire video." | **1–4 句** | "Use N/A **only when the user explicitly requests complete silence** throughout the video." |
| **③ 配乐** | `non_diegetic_music` | "Describes background music that **the characters cannot hear and only the audience can hear**." | **1–3 句** | "Use N/A when there is no non-diegetic music." |

### 7.2 判别口诀（唯一需要记住的一条）

> **问一句：画面里的人能不能听见这个声音？**
>
> - **能听见** → ① `integrated_multimodal_description`（对白、演唱、角色听得到的音乐、角色制造的动响）
> - **不直接属于某个角色的物理动作** → ② `overall_soundscape`（环境音、脚步、门、雨、布料、呼吸、非语言人声）
> - **只有观众能听见** → ③ `non_diegetic_music`

### 7.3 判定表（遇到具体声音查这里）

| 声音 | 去哪一层 | 理由 |
|---|---|---|
| 角色说台词 | ①（`<d>` 内） | 官方：dialogue 属 multimodal description |
| 角色唱歌 | ①（`<d>` 内，lyrics 同规则） | "Singing ... should not be repeated here [soundscape]" |
| 收音机 / 电视 / 手机外放的音乐 | **①** | 【官方原文】"radio, television, or phone music **audible to the characters are diegetic events** and should appear in the multimodal description." |
| 角色自己弹的钢琴 | ① | 角色听得到 |
| 街道车流 / 雨声 / 风声 | ② | 环境音 |
| 脚步声、开门声、纸张摩擦、布料声 | ② | 物理动作音 |
| 呼吸、叹气、啜泣、哼声、笑 | ② | "non-verbal human sounds" |
| 心跳、耳鸣 | ② | 非语言人声【推断】 |
| 只有观众听到的弦乐配乐 | ③ | 官方定义 |
| 片尾主题曲（角色听不到） | ③ | 官方定义 |
| **场内广播 / PA 喊话** | **①** | 角色听得到 → diegetic【推断】 |

### 7.4 ② `overall_soundscape` 写法

**三条禁止**（官方原文）：

> `Dialogue, singing, and diegetic music already belong in the multimodal description and should not be repeated here.`

| 禁止 | 说明 |
|---|---|
| ❌ 重复对白 | 不要在音景里复述 `<d>` 里的任何一句话 |
| ❌ 重复演唱 | 歌词只在 `<d>` 里 |
| ❌ 写剧情内音乐 | 角色听得到的音乐属 ① |

**✅ 正例（可复制）**

```text
overall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery. The doorbell rings once, followed by light footsteps and the crisp sound of bread being sliced.
中：木制卷帘在安静的街道上拉开，店里托盘轻轻碰撞。门铃响了一次，随后是轻脚步声与切开面包的清脆声。
```

```text
overall_soundscape: Quiet meeting-room tone, one soft press of palms against the tabletop, the friction of paper being lifted, two steady footfalls, and trench-coat fabric shifting with each step.
中：安静的会议室底噪，一次手掌轻按桌面，纸张被拿起的摩擦声，两记平稳的脚步，风衣布料随步伐摆动的声音。
```

```text
overall_soundscape: Coat fabric shifting, one slow breath released, the faint creak of floorboards under shifting weight.
中：外套布料摩擦，一次缓慢的呼气，地板在重心转移下发出轻微吱呀声。
```

**❌ 反例**

```text
❌ overall_soundscape: She says she will not change the contract, and the cello music plays sadly while they argue.
   ← 重复了对白（"she says..."）+ 剧情解释（"while they argue"）+ 情绪词（sadly），三重违规。

❌ overall_soundscape: The radio plays a jazz song.
   ← 若角色听得到收音机，这是 diegetic，必须写回 ①。

❌ overall_soundscape: N/A
   ← 全片并非静音，滥用 N/A（官方：N/A 仅当用户明确要求全片静音）。
```

### 7.5 ③ `non_diegetic_music` 写法

> **【官方原文】** `Focus on instrumentation, speed, rhythm, and dynamic changes; do not use abstract mood words or explain the emotional function of the score.`

**只写四样**：`instrumentation`（乐器）／ `speed`（速度）／ `rhythm`（节奏）／ `dynamic changes`（动态变化）。
**禁写**：抽象情绪词、配乐的情感功能解释。

**✅ 正例（官方例句，逐字）**

```text
non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
中：一段柔和的原声吉他音型，中速，加入稀疏的低音提琴音符，结尾轻微淡出。
```

```text
non_diegetic_music: A single sustained cello note at a slow tempo, entering halfway and swelling gently to the end of the shot.
中：一个持续的大提琴长音，慢速，在中段进入，轻柔渐强至镜头结束。
```

```text
non_diegetic_music: Sparse low strings at a very slow tempo, entering after she finishes speaking and fading out over the final second.
中：稀疏的低音弦乐，极慢速，在她讲完后进入，最后一秒淡出。
```

**❌ 反例（逐条）**

```text
❌ non_diegetic_music: Sad music that makes the audience cry.
   ← 抽象情绪词 + 情感功能解释，官方明确禁止。

❌ non_diegetic_music: A tense, heartbreaking, epic orchestral score full of sorrow and hope.
   ← 三个抽象情绪词。

❌ non_diegetic_music: Music playing from the radio on the table.
   ← 角色听得到 → diegetic，必须写回 ①。

❌ non_diegetic_music:          ← 留空
   ← 官方要求无配乐时写 N/A，不留空。
```

### 7.6 ⚠️ 项目内的一处写法冲突

| 来源 | 无配乐写法 | 判定 |
|---|---|---|
| **官方 `base-en.txt`** | `non_diegetic_music: N/A`（"Use N/A when there is no non-diegetic music."） | ✅ **以此为准** |
| `MiniMaxH3-小说转分镜-完整模板.md` 模块九示例 | `non_diegetic_music: no music` | ⚠️ 项目示例，**建议统一为 N/A** |
| `防翻车限制词库_H3版.md` §1.5 | `no music`（"明确写出，不要留空"） | ⚠️ 同上 |

**建议：无配乐一律写 `N/A`（官方原文口径），不要留空。`no music` 也不建议——它可能被引擎理解为"要生成一段名为无音乐的静音"，属【待验证】。**

### 7.7 完整的三字段声音骨架（可复制）

```text
integrated_multimodal_description: [Shot 1] <画面描述> The <识别短语> (S1) says: <d>[Chinese] <台词></d> <角色听得到的声音，如：the radio on the shelf plays a faint jazz tune>
[Shot 2] At 00:SS.mmm, ...

overall_soundscape: <1–4 句：环境音 + 物理动作音 + 非语言人声，不重复对白>

non_diegetic_music: <1–3 句：乐器 + 速度 + 节奏 + 动态，无情绪词>  或  N/A
```

---

## 8. 配乐写法（细化为可执行的词库）

### 8.1 四个维度词库（照着挑，不要临场造）

| 维度 | 可用词 |
|---|---|
| **乐器 instrumentation** | `solo piano` `acoustic-guitar pattern` `sustained cello note` `low strings` `sparse upright-bass notes` `brushed drums` `muted trumpet` `synth pad` `harp arpeggio` `tremolo strings` `woodwind` `choir pad` |
| **速度 speed / tempo** | `at a very slow tempo` `at a moderate tempo` `at a brisk tempo` `accelerating` `decelerating` |
| **节奏 rhythm** | `sparse` `steady eighth-note pulse` `syncopated` `repeating two-bar pattern` `lilting` `driving` `staccato` |
| **动态 dynamic changes** | `entering halfway` `swelling gently` `fading out over the final second` `a gentle fade at the end` `cutting cleanly on the final beat` `a gradual crescendo` `suddenly dropping to silence` |

### 8.2 组合公式

```text
<乐器> + <速度> + <节奏> + <动态变化起点> + <动态变化终点>
```

**五条可复制范例**

```text
① non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
中：柔和的原声吉他音型，中速，加入稀疏的低音提琴音符，结尾轻微淡出。

② non_diegetic_music: A single sustained cello note at a slow tempo, entering halfway and swelling gently to the end of the shot.
中：单个持续的大提琴长音，慢速，中段进入，轻柔渐强至镜头结束。

③ non_diegetic_music: Sparse low strings at a very slow tempo, entering after she finishes speaking and fading out over the final second.
中：稀疏的低音弦乐，极慢速，在她讲完后进入，最后一秒淡出。

④ non_diegetic_music: A steady eighth-note pulse on brushed drums at a brisk tempo, with a syncopated bass line, cutting cleanly on the final beat.
中：刷鼓上稳定的八分音符律动，轻快速度，配切分低音线，在最后一拍干净收住。

⑤ non_diegetic_music: N/A
中：无配乐。
```

### 8.3 ⛔ 情绪词黑名单（写了就是违规）

`sad` `happy` `tense` `romantic` `heartbreaking` `epic` `triumphant` `melancholic` `hopeful` `sorrowful` `uplifting` `scary` `nostalgic` `emotional` `moving` `touching` `thrilling` `mysterious`

以及**任何解释情感功能的句式**：
`that makes the audience cry` / `to build tension` / `to convey her loneliness`

**替换法**：想表达"悲伤" → 写 `a solo cello at a very slow tempo, with long sustained notes fading into silence`（乐器 + 速度 + 动态）。把情绪翻译成**声学参数**。

### 8.4 情绪 → 声学参数转换表（想写情绪时查这张表）

| 你想要的效果 | ❌ 不能这么写 | ✅ 改成声学参数 | 中文说明 |
|---|---|---|---|
| 悲伤 / 失落 | `sad music` | `A solo cello at a very slow tempo, long sustained notes fading into silence` | 独奏大提琴，极慢，长音淡入静默 |
| 紧张 / 危险 | `tense music` | `Tremolo low strings at a brisk tempo with a steady eighth-note pulse, gradually accelerating` | 低音弦乐震音，轻快，八分音符律动，逐渐加速 |
| 甜蜜 / 心动 | `romantic music` | `A light harp arpeggio at a moderate tempo with a lilting rhythm and a gentle fade` | 轻盈竖琴琶音，中速，摇曳节奏，轻微淡出 |
| 燃 / 爽点 | `epic triumphant music` | `Full brass and low strings at a fast tempo with a driving rhythm and a sudden crescendo on the final beat` | 全铜管与低音弦乐，快速，推进感节奏，末拍突强 |
| 孤独 / 空旷 | `lonely music` | `A single sustained piano note with wide gaps between sparse low chords` | 单个钢琴长音，稀疏低音和弦间留出大段空白 |
| 恐惧 / 惊悚 | `scary music` | `High sustained string harmonics at a very slow tempo with irregular staccato accents` | 高音弦乐泛音持续音，极慢，不规则断奏重音 |
| 怀旧 / 回忆 | `nostalgic music` | `A soft acoustic-guitar pattern at a slow tempo with a repeating two-bar figure` | 柔和的原声吉他音型，慢速，两小节循环 |
| 释然 / 和解 | `hopeful music` | `A warm synth pad swelling gradually, joined by sparse upright-bass notes at a moderate tempo` | 温暖的合成器铺底缓慢渐强，加入稀疏低音提琴音符，中速 |
| 压抑 / 憋屈 | `melancholic music` | `Muted trumpet over a sustained low drone, very slow tempo, no rhythmic pulse` | 弱音小号叠在持续低音上，极慢，无节奏律动 |
| 平静 / 日常 | `calm music` | `No non-diegetic music` → 写 `N/A` | 无配乐，直接写 N/A |

> **替换心法**：情绪是**结果**，声学参数是**原因**。写原因，让观众自己得出结果。

### 8.5 按段落功能选配乐（15 秒 3 镜）

| 段落功能 | 配乐策略 | 可复制写法 |
|---|---|---|
| A 入镜（2s） | 通常**不进配乐**，留环境音 | `non_diegetic_music: N/A` |
| B 主镜（10–11s） | 配乐主体；**进在人声之后**，避免盖词 | `entering after she finishes speaking` |
| C 出镜（2–3s） | 收尾动态：淡出 / 干净收住 / 突停 | `fading out over the final second` / `cutting cleanly on the final beat` |

```text
【主镜有台词时的标准动态】
non_diegetic_music: Sparse low strings at a very slow tempo, entering after she finishes speaking and fading out over the final second.
中：稀疏的低音弦乐，极慢速，在她讲完后进入，最后一秒淡出。
```

> **为什么配乐要在人声之后进**：H3 的配乐与对白同一次推理生成，两者会争夺同一段音频。**配乐进点写在人声之后，是让对白保住清晰度的最省事手段。**【推断·待验证】——实测方法：同一条提示词，A 组配乐 `entering at the start`，B 组 `entering after she finishes speaking`，各 5 条，盲听对白清晰度打分。

### 8.6 正面/负面完整对照

```text
❌ 全违规
non_diegetic_music: A tense, heartbreaking orchestral score that makes the audience feel her loneliness as she walks away.

✅ 改写后（同样意图，全部转成声学参数）
non_diegetic_music: A solo cello at a very slow tempo with long sustained notes, joined by a faint high string harmonic, fading into silence over the last two seconds.
中：独奏大提琴，极慢速，长持续音，加入微弱的高音弦乐泛音，最后两秒淡入静默。
```

```text
❌ 违规（情绪词 + 情感功能解释 + 重复对白）
non_diegetic_music: Sad music that makes the audience cry while she says goodbye.

✅ 改写后
non_diegetic_music: A solo piano at a very slow tempo with sparse low chords, entering after she speaks and fading into silence before the cut.
中：独奏钢琴，极慢速，稀疏低音和弦，在她说话后进入，在切点前淡入静默。
```

---

## 9. 口型同步与语种串台

### 9.1 为什么这是 H3 的新增高风险项

H3 **原生生成音频**（32 kHz 立体声，与画面同一次推理产出，自带唇形同步，稳定支持 11 种语言）。因此翻车形态从"口型对不上"变成了：

| 翻车形态 | 表现 | 根因 |
|---|---|---|
| **说错话** | 念出的不是 `<d>` 里的词 | 台词没放 `<d>` 里 / 标签未闭合 |
| **说错人** | 声音是另一个人的 | 说话人 ID 跨镜变了 / 一镜两人说话 |
| **说错语言** | 中文台词念成英文发音 | 语言标签缺失或与内容不符 |
| **嘴在动但没声 / 有声但嘴不动** | 画外音穿帮 | 漏 `while his lips remain completely closed.` |

> **风险类型码 `V`（语音与说话人）** —— H3 新增，凡"有台词、跨镜说话、画外音、多角色对话"的分镜一律打此码。

### 9.2 一镜一个说话人（最重要的防串音规则）

> **官方原话**：*"The single most reliable trick for clean lip sync. If two people need to talk, cut between them."*

**规则：同一镜内不得让两人先后说话。要两人对话，就切成两个镜头。**

> 这是「对话段采用 4 镜方案」的直接原因：A 说 → 切 → B 说 → 切 → A 反应 → 切 → B 反应。

**✅ 正例**

```text
[Shot 1] A medium shot frames the man (S2); he says: <d>[Chinese] 你迟到了十分钟。</d>
[Shot 2] At 00:04.000, the camera cuts to the woman (S1), who answers without looking up: <d>[Chinese] 我知道。</d>
中：[镜 1] 中景，男人 (S2)，他说：`<d>[Chinese] 你迟到了十分钟。</d>`
    [镜 2] 00:04.000 切到女人 (S1)，她没抬头就回答：`<d>[Chinese] 我知道。</d>`
```

**❌ 反例**

```text
❌ [Shot 1] The man (S2) says: <d>[Chinese] 你迟到了。</d> Then the woman (S1) replies: <d>[Chinese] 我知道。</d>
   ← 一镜内两个说话人，唇形同步可靠性显著下降。
```

### 9.3 语种串台的四道防线

| 防线 | 做法 | 说明 |
|---|---|---|
| 1 | **语言标签必写** `[Chinese]` / `[English]` | 官方要求 `<d>` 内第一个元素就是语言标签 |
| 2 | **身份/语气一律放 `<d>` 外** | 官方原文：identifying phrase, ID, action, delivery 全在外面 |
| 3 | **台词逐字不译** | `do not translate or rewrite them` |
| 4 | **说话人描述用英文、台词用原语言** | 提示词骨架英文，只有 `<d>` 内是原语种 |

**✅ 正确**

```text
The 28-year-old woman with a low, steady voice (S1) says: <d>[Chinese] 陈总，这份合同我一个字都不会改。</d>
中：声音低沉平稳的 28 岁女人 (S1) 说：`<d>[Chinese] 陈总，这份合同我一个字都不会改。</d>`
```

**❌ 三语种串台错误**

```text
❌ 语言标签与实际内容不符
   <d>[English] 陈总，这份合同我一个字都不会改。</d>     ← 标 English 却是中文

❌ 缺语言标签
   <d>陈总，这份合同我一个字都不会改。</d>

❌ 身份描述用了中文导致语种混杂
   那个女人 (S1) 说: <d>[Chinese] 我早就知道了。</d>      ← 提示词骨架应保持英文
```

### 9.4 口型同步的加强技巧

> **【H3】官方对白稳定性技巧**（MiniMax × ComfyUI 官方直播）：把输入音频作为 reference 的**同时**，在提示词里**写出角色要说的台词并放进对应镜头的描述中**——两者并用可显著提升对白稳定性与一致性。

前置条件：走 **Ref2VA（全能参考）** 模式，用 `<Audio N>` 作音色参考：

```text
subject_definitions:
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).

retention_analysis:
<Audio 1>: reference - the target speaker follows <Audio 1>'s voice timbre and measured delivery without copying the original signal.

detailed_description:
[Shot 1] ... <Subject 1> (S1) says: <d>[Chinese] 我早就知道了。</d>
```

> ⚠️ **图生视频与全能参考互斥** —— `first_frame`/`last_frame` 与 `reference_*` 不可同时出现。要用音色参考，就必须放弃首尾帧。
> ⚠️ 仅参考音色/节奏时，**"do not carry the original dialogue from the reference audio into the target video"**（官方原文）——不要把参考音频里的原台词带进目标视频。

### 9.5 【待验证】清单与实测方法

| # | 待验证项 | 实测方法 |
|---|---|---|
| 1 | 模型**实际中文语速** V 值 | 用 20 / 35 / 45 字三档台词各生成 5 条，量实际发音时长，`V = 字数 ÷ 时长`，回填 §3.2 |
| 2 | 11 种语言各自的**可懂度** | 每种语言同一句台词各生成 5 条，母语者盲听打分（1–5） |
| 3 | 11 种之外的语言（粤语 / 泰语 / 方言）是否可用 | 各 5 条，听是否为目标语言发音 |
| 4 | delivery 副词对语速的**引导强度** | 见 §3.8 |
| 5 | `<d>` 内叠加英文双引号是否有副作用 | 见 §1.5 |
| 6 | `no music` vs `N/A` 的差异 | 各 5 条，听是否真的无配乐 |
| 7 | 纯画外叙述者写法 | 见 §5.4 |
| 8 | `<cutoff>` 在片中（非片尾）是否生效 | 见 §6.6 |
| 9 | `dialogue replacement` 后画面是否**逐帧不变** | 官方表述是"未指定元素保持不变"，**不是**"逐帧不变"。交付前必跑一次：编辑前后逐帧对比，确认画面像素级一致 |
| 10 | 齐声 `(S1,S2)` 的**可懂度** | 见 §10.3 |

### 9.6 台词改错了怎么办：`dialogue replacement`

**H3 支持 in-context 视频编辑，其中包含 `dialogue replacement`（对白替换）**，官方明确"未指定的镜头元素保持原样"。即：**改一句台词 ≠ 重生成整个镜头。**

**判断口诀：改「说什么」→ 用编辑；改「怎么演」或「演多久」→ 重生成。**

| 情况 | 用哪个 | 理由 |
|---|---|---|
| 只改**用词 / 语序**，表演、构图、运镜都满意 | ✅ **dialogue replacement** | 画面保留，成本最低 |
| 改词后**时长变了**（字数差 > 20%） | ❌ **重生成** | 口型节奏与新时长不匹配 |
| 改词导致**情绪 / 表演需要变**（平静 → 愤怒） | ❌ **重生成** | 表情属"指定改动范围"之外，硬改会僵 |
| **语种切换**（中文版 → 英文版） | ✅ **优先 dialogue replacement** | 官方列出的典型用例（regional adaptations） |
| 画面本身有缺陷（手部崩、穿模） | ❌ **重生成**（先抬采样步数到 6–8） | 编辑模式不改未指定区域。**抬步数前先做生成前内容检查**（景别/强度/节拍）——设计错误抬步数无效，只会得到"高清版的错误" |
| 只换**音色**（换配音演员） | ✅ **dialogue replacement** + 换音频参考 | 用 `reference` 标记指向新音色 |

**三条限制（必须写清）**：

1. 这是**视频编辑模式**（需上传源片作参考），**不是"只重生音轨"的参数开关**；走 `reference_*` 通道，因此**与 `first_frame`/`last_frame` 互斥**。
2. **画面是否逐帧 100% 不变，未经独立实测**（见 §9.5 #9）。
3. 对白稳定性另有官方技巧：输入音频作 reference **同时**在提示词里写出台词（见 §9.4）。

> **流程结论**：**不设「台词定稿后的 Audio Lock 变更审批」环节**——那是给创作者增加无谓负担，按常规流程写即可。

---

## 10. 多人对白与群戏

### 10.1 三种形态与写法

| 形态 | 写法 | 关键约束 |
|---|---|---|
| **交替说话** | 切成两个镜头，一镜一人 | 官方："If two people need to talk, cut between them." |
| **齐声** | `(S1,S2)` + `together` | 官方例句用词 |
| **打断 / 抢话** | 切成两镜 + 措辞明写打断 | 【推断·待验证】 |
| **群杂 / 环境人声** | 不放 `<d>`，放 `overall_soundscape` | 非语言人声或听不清的人声 |

### 10.2 交替说话（推荐做法）

```text
[Shot 1] A medium shot frames the man at frame right (S2), who says without turning: <d>[Chinese] 你还是来了。</d>
[Shot 2] At 00:04.500, the camera cuts to the woman at frame left (S1); she answers evenly: <d>[Chinese] 我说过我会来。</d>
中：[镜 1] 中景，男人在画面右侧 (S2)，没有回头地说：`<d>[Chinese] 你还是来了。</d>`
    [镜 2] 00:04.500 切到画面左侧的女人 (S1)；她平静地回答：`<d>[Chinese] 我说过我会来。</d>`
```

**方位写法要点**（与 180° 轴线一致）：用**绝对画面位置** `at frame left` / `at frame right`，**不要写"她的左边"**（有歧义）。有关轴线与 [AXIS] 块见 `minimax-h3-storyboard`。

### 10.3 齐声（官方例句）

```text
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
中：两个孩子 (S1,S2) 一起喊道：`<d>[English] Wait for us!</d>`
```

```text
The crowd of neighbours (S1,S2,S3) chants together, <d>[Chinese] 不行！不行！</d>
中：一群邻居 (S1,S2,S3) 齐声喊：`<d>[Chinese] 不行！不行！</d>`
```

- **写法**：`(S1,S2)` —— **逗号后无空格**。
- **动词**：`shout together` / `say in unison` / `chant together`。
- **⚠️ 可懂度风险**：多人同念时清晰度下降。**【待验证】**（§9.5 #10）。实测方法：齐声 2 人 / 3 人 / 5 人各生成 5 条，盲听能否听清每个词。**建议齐声只用于短句（≤ 8 字）或口号，承载关键信息的一律单人说。**

### 10.4 打断 / 抢话

```text
[Shot 1] ... the woman (S1) says: <d>[Chinese] 你听我解释，那天我——<cutoff></d>
[Shot 2] At 00:06.000, the camera cuts to the man (S2), who cuts her off mid-sentence: <d>[Chinese] 我不听。</d>
中：[镜 1] ……女人 (S1) 说：`<d>[Chinese] 你听我解释，那天我——<cutoff></d>`
    [镜 2] 00:06.000 切到男人 (S2)，他在她说到一半时打断：`<d>[Chinese] 我不听。</d>`
```

可用措辞：`cuts her off mid-sentence` / `interrupts before she finishes` / `talks over her`
配合标记：前半句用 `<cutoff>` 或 `<scenetrans>`，后半句明写打断动作。

> **【推断·待验证】** 官方原文只给 `<cutoff>` 的定义是"被视频结尾截断"。片中打断用 `<cutoff>` 是本项目外推（见 §9.5 #8）。

### 10.5 群杂 / 环境人声（不进 `<d>`）

```text
overall_soundscape: A low murmur of conversation from the neighbouring tables, cutlery against plates, and one burst of laughter from off-frame right.
中：邻桌传来的低声交谈，餐具碰盘的声音，画外右侧传来一阵笑声。
```

> 听不清的源词写 `[unclear]`，**不要猜**（官方 Ref2VA 规则）。

### 10.6 正反例

```text
✅ 正确（切镜一人一句 + ID 稳定 + 绝对方位）
[Shot 1] ... the man at frame right (S2) says: <d>[Chinese] 你还是来了。</d>
[Shot 2] At 00:04.500, the camera cuts to the woman at frame left (S1), who answers: <d>[Chinese] 我说过我会来。</d>

✅ 正确（齐声）
The two children (S1,S2) shout together, <d>[Chinese] 等等我们！</d>

❌ 错误 1：一镜两人先后说话
[Shot 1] ... (S1) says: <d>[Chinese] 你来了。</d> Then (S2) replies: <d>[Chinese] 我来了。</d>

❌ 错误 2：齐声写成两个标签
The two children (S1) (S2) shout together, <d>[Chinese] 等等我们！</d>     ← 应为 (S1,S2)

❌ 错误 3：群杂写进 <d>（会被逐个念出来，且字数爆表）
<d>[Chinese] 大家都在喊着什么。</d>

❌ 错误 4：不出声的群演也给了 ID
A waiter crosses the background (S4).     ← 他没说话，不该有 ID
```

---

## 11. 检查清单 + 正反例速查表

### 11.1 提交前 20 条（逐条打勾）

**对白标签 `<d>`**

- [ ] 1. 每一句台词都在 `<d>` … `</d>` 之间，标签闭合、小写
- [ ] 2. `<d>` 内**只有**语言标签 + 原话，无身份、无动作、无语气、无舞台提示
- [ ] 3. 语言标签**首字母大写**且在 11 种官方语言内
- [ ] 4. 台词**逐字保留**，标点未改、未翻译、未加省略号
- [ ] 5. `<d>` 内**未**叠加英文双引号（默认不加；存在官方口径冲突，见 §1.5）

**说话人**

- [ ] 6. 所有出声角色都有稳定 ID `(S1)` `(S2)`…
- [ ] 7. **跨镜、跨段、跨集 ID 一致**（同一人不换号）
- [ ] 8. 不出声的角色**没有** ID
- [ ] 9. 首次出场从**视觉 + 听觉**两维建了身份（听觉至少 2 维）
- [ ] 10. 齐声写 `(S1,S2)`，逗号无空格

**语速与字数**

- [ ] 11. 单元总台词 **≤ 45 字**（计算硬上限 47）
- [ ] 12. 每镜台词字数 ≤ §3.4 表对应镜长上限
- [ ] 13. 单句 ≤ 18 字，建议 12–15 字
- [ ] 14. 入镜 / 出镜**无台词或 ≤ 7–9 字**

**旁白与跨镜**

- [ ] 15. 每个 voiceover `<d>` 后**紧跟** `while his/her/their lips remain completely closed.`
- [ ] 16. 用了官方原句 `says in an off-screen voiceover`，未替换成 narrates 等
- [ ] 17. 跨镜连续台词两处都标 `<scenetrans>` + 写了四选一连续措辞
- [ ] 18. 视频结尾截断用 `<cutoff>`

**声音三层**

- [ ] 19. `overall_soundscape` 1–4 句，**未重复对白 / 演唱 / 剧情内音乐**；非全片静音就没写 N/A
- [ ] 20. `non_diegetic_music` 1–3 句，**只写乐器 / 速度 / 节奏 / 动态**，无情绪词；无配乐写 `N/A`

### 11.2 补充 5 条（跨节）

- [ ] 21. 角色听得到的音乐（radio / TV / 手机外放 / 现场演奏）已写回 `integrated_multimodal_description`
- [ ] 22. **一镜一个说话人**（两人对话已切成两镜）
- [ ] 23. 台词与画面**不重复同一信息**
- [ ] 24. 全提示词 ≤ 7000 字符（1 汉字 = 1 字符）
- [ ] 25. 分镜表 `风险类型` 已打 **`V`** 码，且有备选方案

### 11.3 正反例速查表（一页看完）

| # | ❌ 错误写法 | ✅ 正确写法 | 违反的规则 |
|---|---|---|---|
| 1 | `The woman (S1) says: [Chinese] 我早就知道了。` | `The woman (S1) says: <d>[Chinese] 我早就知道了。</d>` | 缺 `<d>` 标签，台词不会被念出 |
| 2 | `<d>[Chinese] 那个女人低声说：我早就知道了。</d>` | `The woman with a low voice (S1) says: <d>[Chinese] 我早就知道了。</d>` | 身份/语气进了标签，会被念出来 |
| 3 | `<d>[English] 我早就知道了。</d>` | `<d>[Chinese] 我早就知道了。</d>` | 语言标签与内容不符 → 语种串台 |
| 4 | `<d>[Chinese] 我早就知道了……</d>` | `<d>[Chinese] 我早就知道了。</d>` | 改了标点，违反 verbatim |
| 5 | 第 1 镜 `(S1)`，第 3 镜同一个 `(S2)` | 全程 `(S1)` | ID 跨镜变了 → **说话人串音** |
| 6 | 路人甲乙丙也编了 `(S3)` `(S4)` | 不出声不给 ID | "characters who never vocalize receive no speaker ID" |
| 7 | `[Shot 1] (S1) 说一句，(S2) 回一句` | 切成两镜，一镜一人 | "If two people need to talk, cut between them." |
| 8 | `...says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d>` | 句尾补 `while his lips remain completely closed.` | 旁白两句必须成对 |
| 9 | `The man (S1) narrates: <d>[Chinese] ...</d>` | `says in an off-screen voiceover` | 官方要求 `use the exact phrase` |
| 10 | 只在 Shot 1 结尾标 `<scenetrans>` | 两处连接点都标 + 写连续措辞 | "at the connecting points in **both** parts" |
| 11 | `overall_soundscape: She says she won't change the contract.` | 改为环境音与动作音 | 音景不得重复对白 |
| 12 | `overall_soundscape: The radio plays a jazz song.` | 移进 `integrated_multimodal_description` | 角色听得到 → diegetic |
| 13 | `non_diegetic_music: Sad, heartbreaking music.` | `A solo cello at a very slow tempo, fading into silence.` | 禁写抽象情绪词 |
| 14 | `non_diegetic_music:` （留空） | `non_diegetic_music: N/A` | 无配乐写 N/A |
| 15 | `overall_soundscape: N/A`（全片并非静音） | 写实际环境音 | N/A 仅当用户明确要求全片静音 |
| 16 | 主镜 11 秒塞 48 字台词 | 拆镜或砍到 ≤ 35 字 | 超 §3.4 容量表 |
| 17 | `<d>[Chinese] （冷笑）你觉得我会信吗？</d>` | `She lets out a short cold laugh, then says: <d>[Chinese] 你觉得我会信吗？</d>` | 舞台提示进了标签 |
| 18 | `The two children (S1) (S2) shout together` | `The two children (S1,S2) shout together` | 齐声格式 |
| 19 | `<d>[Chinese] 大家都在喊着什么。</d>` | 群杂写进 `overall_soundscape`，不放 `<d>` | `<d>` 内只放一句确定的原话 |
| 20 | `A waiter crosses the background (S4).` | `A waiter crosses the background.` | 不出声不给 ID |

### 11.4 生成后看片检查（声音侧）

| 检查项 | 通过标准 | 不通过时的处置 |
|---|---|---|
| **念的是不是这句话** | 逐字对上 `<d>` 内容 | 检查标签是否闭合、是否有多余内容进标签 |
| **是不是这个人在说** | 音色与前几镜/前几集一致 | 检查 ID 是否跨镜变化 |
| **是不是这个语种** | 发音属于 `[Chinese]` 等标签语言 | 检查语言标签 |
| **嘴型对不对** | 说话时嘴动；不说话时嘴闭 | 旁白漏后半句 / 一镜两人说话 |
| **有没有说完** | 结尾没被突兀截断（除非故意 `<cutoff>`） | 减字数或加时长 |
| **听不听得清** | 语速不急促、不拖沓 | 回填 §3.2 的 V 值，重算字数 |
| **配乐有没有抢戏** | 配乐不盖过人声 | 改动态描写（降低进入音量 / 提前淡出） |
| **环境音有没有盖人声** | 对白清晰 | 精简 `overall_soundscape` 句数 |

---

## 12. 可复制片段库（直接抄）

### 12.1 单人对白 · 中文

```text
The 28-year-old woman with a low, steady voice at a measured pace (S1) says: <d>[Chinese] 陈总，这份合同我一个字都不会改。要么重签，要么法庭见。</d>
```

### 12.2 单人对白 · 简短（≤ 8 字）

```text
The man (S2) says without looking up: <d>[Chinese] 我知道。</d>
```

### 12.3 首次出场 + 对白（视听双维）

```text
[Shot 1] Live-action, cinematic. A medium shot frames a 34-year-old man in a grey wool coat, his short black hair brushed back, a faint scar across his left eyebrow. The man with a deep, slightly gravelly voice at an unhurried pace (S2) says: <d>[Chinese] 十年了，你一点都没变。</d>
```

### 12.4 旁白（成对）

```text
The man (S1) says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d> while his lips remain completely closed.
```

### 12.5 跨镜连续（两处）

```text
[Shot 1] ... the woman (S1) says: <d>[Chinese] 我从来没想过 <scenetrans></d>
[Shot 2] At 00:05.000, the camera cuts to a close-up of her hands; her sentence continues seamlessly across the cut, <d>[Chinese] <scenetrans> 你会回来。</d>
```

### 12.6 结尾截断

```text
... the woman (S1) says: <d>[Chinese] 其实我早就知 <cutoff></d>
```

### 12.7 双人交替（切镜）

```text
[Shot 1] A medium shot frames the man at frame right (S2), who says without turning: <d>[Chinese] 你还是来了。</d>
[Shot 2] At 00:04.500, the camera cuts to the woman at frame left (S1), who answers evenly: <d>[Chinese] 我说过我会来。</d>
```

### 12.8 齐声

```text
The two children (S1,S2) shout together, <d>[Chinese] 等等我们！</d>
```

### 12.9 完整三字段（无台词镜）

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic, 35mm lens. A medium close-up frames her standing at the right third of frame, body angled three-quarters to camera, both arms hanging at her sides. First her gaze drops to the letter on the desk, then her right hand lifts and presses once flat against the paper, then her fingers curl and she picks the letter up. She stays silent; her lips remain closed. The paper bends slightly at one corner; dust drifts through the warm lamp light. The camera pushes in with small amplitude at slow speed from a medium close-up to a close-up. By the end of the shot she holds the letter in both hands, her knuckles slightly pale, her gaze fixed on the paper. Do not show any legible text on the paper.

overall_soundscape: Paper sliding across wood, a single slow inhalation, the low hum of the desk lamp, distant wind against the window.

non_diegetic_music: A single sustained cello note at a slow tempo, entering halfway and swelling gently to the end of the shot.
```

### 12.10 完整三字段（有台词 + diegetic 音乐）

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic. A medium two-shot frames a narrow noodle bar at night, steam rising behind the counter. The radio on the shelf behind them plays a faint jazz tune that both of them can hear. The 40-year-old woman with a warm, slightly nasal voice (S1) says: <d>[Chinese] 最后一班地铁，十一点二十。</d> [Shot 2] At 00:06.000, the camera cuts to a close-up of the man at frame right (S2), who nods once and says: <d>[Chinese] 来得及。</d>

overall_soundscape: Broth bubbling on the stove, chopsticks tapping against a ceramic bowl, the low hum of the extractor fan, and two sets of footsteps outside on wet pavement.

non_diegetic_music: N/A
```

> 注意：收音机的爵士乐**角色听得到**，所以写在 `integrated_multimodal_description` 里，不写进 `non_diegetic_music`。这正是 §7.3 的判定。

---

## 13. 与其他 skill / 文档的分工

| 内容 | 去哪 |
|---|---|
| 集数拆解、分镜节奏、运镜、时间戳、资产一致性、检查清单总表 | `minimax-h3-storyboard` |
| **对白、语速、说话人、旁白、声音三层、口型同步** | **本 skill** |
| 官方来源与硬参数完整表 | `MiniMax-H3-官方提示词规范调研报告.md` |
| 翻车类型与风险码 `V` | `防翻车限制词库_H3版.md` §1 |
| 语速公式与单镜容量表 | `MiniMaxH3-小说转分镜-完整模板.md` 模块四 |

**参考来源（官方，可直接写进交付物）**：

- `https://github.com/MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/base-en.txt`（T2VA / I2VA / FL2VA / L2VA）
- `https://github.com/MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/ref-en.txt`（Full-Reference / Ref2VA）
- `https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir`（官方 API 文档：7000 字符、4–15 秒、24 FPS）
- `https://huggingface.co/MiniMaxAI/MiniMax-H3`（官方模型卡：32 kHz 立体声、11 种语言）

---

## 附：【待验证】清单唯一入口 = §9.5

**样片阶段必须跑完并回填。** 全部 10 项见 **§9.5**，此处不复制——两份清单长期必然漂移。

> **回填规则**：每跑完一项，把结论改写入对应章节，并删除【待验证】标记、改为【实测·YYYY-MM-DD】。**没跑过的，永远保留【待验证】。**
