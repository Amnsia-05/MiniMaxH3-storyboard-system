---
name: h3-action-body
description: 海螺 H3 视频提示词中「动作 / 肢体 / 手部 / 姿态 / 空间距离」的控制方法，含防多指、防关节反折、防人物融合的可复制模板。触发词：H3动作描写、H3肢体、H3手部防崩、H3姿态、H3空间距离、动作时序、H3多指问题。
agent_created: true
---

# H3 动作 / 肢体 / 手部 / 姿态 / 空间距离 控制手册

> **本 skill 只管一件事**：把「人怎么动、手怎么放、身体摆什么姿势、两人隔多远」写成 H3 吃得下去、且不崩坏的句子。
> 这是 AI 视频崩坏率最高的一块。**画面崩了先按 §9 排查采样步数，再回来改词。**

---

## 0. 定位、证据分级与上游文件

### 0.1 本 skill 与主模板的分工

| 文件 | 管什么 | 与本 skill 的关系 |
|---|---|---|
| `MiniMaxH3-小说转分镜-完整模板.md` | 全流程（拆集 → 分镜 → 提示词 → 检查 → 交付） | **母模板**，术语/字段/锁定块以它为准 |
| `MiniMax-H3-官方提示词规范调研报告.md` | H3 官方格式（三字段、时间戳、运镜术语、`<d>` 标签） | 格式依据，本 skill 不重复 |
| `防翻车限制词库_H3版.md` | 9 类翻车的规避写法 | §4 手部、§5 肢体、§9 物理 母章节；本 skill 是专项展开 |
| `叙事侧方法论_小说拆解与15秒3镜结构.md` | 15 秒 3 镜结构、衔接类型、走位方向 | 结构依据 |

**绝对路径**：`C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44\`

> ⚠️ **补齐母模板一处悬空引用**：§3.3A 引用了「§4.5 压缩式动作写法」，但模块四只有 §4.1–4.3，**§4.5 不存在**。本 skill §1.6 即该节内容，可回填。

### 0.2 证据分级（严格执行，客户对编造零容忍）

| 标记 | 含义 |
|---|---|
| **【H3】** | MiniMax H3 官方规格 / 官方提示词写作指南（`MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/`）/ 官方 API 文档 |
| **【工艺】** | 模型无关的通用工艺规律，在多代模型上均成立 |
| **【2.3】** | 仅在 Hailuo 2.3 上验证过，**未在 H3 上确认**，套用需谨慎 |
| **【推】** | 机制推断，无公开实测数字支撑 |
| **【待验证】** | 无法确证，本 skill 已给出实测方法 |
| **✗ 硬阻断** | 提示词解决不了，必须改分镜 / 走参考图 / 后期 |

**凡本 skill 中未标注来源的量化数字，一律视为【待验证】或【推】，不得当作官方数据引用。**

### 0.3 H3 硬约束备忘（影响动作写法的部分）

| 项 | 值 | 对动作写法的直接影响 |
|---|---|---|
| 提示词上限 | **7,000 字符**（1 汉字 = 1 字符） | 动作段预算充足，不用为省字砍时序连接词 |
| 时长 | **4–15 秒整数**（API）；本地 **5–15 秒** | 长动作必须跨段拆分（§1.6） |
| 单镜硬下限 | **1.5 秒**；承载信息镜 **≥3 秒** | 短镜内不能塞多拍动作 |
| 帧率 | **24 FPS**（不要指定 FPS 或精确帧数） | 动作节奏靠描述，不靠帧数 |
| 运镜 | **一镜一个** | 见 §7 |
| 图生视频 ↔ 全能参考 | **互斥** | 手部参考图走 Ref2VA 就没首尾帧；走 FL2VA 就不能用 9 图资产锁 |

---

## 1. 动作时序的底层规则

### 1.1 为什么「同时」是头号杀手

模型**没有骨骼、没有关节自由度、没有刚体约束**，它学的是"看起来合理的像素统计"。当你写两个并行动作时，模型不会调度两条运动链，而是把两个动作**平均**成一个不存在的中间姿态——结果就是解剖撕裂、多肢体、手部分叉。

> 【2.3·机制通用】Hailuo 指南原文：并行三动作会破坏 anatomy。
> 【工艺】官方实测归纳：*"Without them the model has to guess whether your three described events happen in sequence or simultaneously, and it **usually picks simultaneously**, which is what produces the mushy, everything-at-once clips."*

→ **核心认知：不写时序连接词，模型默认按「同时」理解。所以"什么都不写" ≠ 中性，而是等于写了一个 `while`。**

### 1.2 `then` vs `while` 对照表

| # | ❌ 崩坏写法 | 崩在哪 | ✅ 正确写法 |
|---|---|---|---|
| 1 | `She sips while waving while walking.` | 三链并行，躯干与手臂互相拉扯 | `She picks up the cup, then takes a sip, then takes one step forward.` |
| 2 | `He turns his head while opening the door.` | 头与手臂争夺注意力，颈部易反折 | `He turns his head toward the door, then reaches for the handle, then pushes it open.` |
| 3 | `She walks toward the window as her hair blows and her coat flutters.` | 若写进主动作链会并行；**衣摆发丝属次级运动，应另起一句**（见 §2.5） | 主链：`She walks to the window, then stops, then rests one hand on the sill.` 次链另起：`Her coat sways with each step; a few strands of hair lift in the draft.` |
| 4 | `He stands up while speaking.` | 重心转移 + 口型，两端都崩，且音频会糊 | `He rises fully to standing, then pauses, then says: <d>[Chinese] …</d>` |
| 5 | `Two people talk at the same time.` | 说话人串音 + 口型崩 | **一镜一个说话人**（官方：*"If two people need to talk, cut between them."*）。同镜双人对话 → 只让一人出声 |
| 6 | `She picks up the pen and signs the document at the same time as looking up.` | 高危手部动作 + 并行 | 改动作：见 §3.7 风险表 |
| 7 | `He hands her the cup while she reaches for it.` | **交接是最难的手部问题**，还并行 | `He slides the cup across the table toward her, then withdraws his hand below the frame line. She closes her fingers around the mug.`（两拍，无接触，见 §3.6） |

**判断口诀：一个句子里出现两个动词，除非它们天然是一个动作的起止（如 `picks up ... and sets down`），否则一律拆成 `then` 序列。**

### 1.3 时间连接词：4 个词的最高杠杆

> 【工艺·实测】*"用 `First ..., then ..., then ..., finally ...` 显式给 beat 顺序。**仅加 4 个词，是整份实测里性价比最高的一次改写。**"*

**标准写法（直接套）**

```
First <动作 A，有终点>, then <动作 B，有终点>, then <动作 C，有终点>, finally <收尾状态>.
```

```
First her gaze drops to the letter on the desk, then her right hand lifts and presses once
flat against the paper, then her fingers curl and she picks the letter up.
中：她先垂下视线看向桌上的信，然后右手抬起、平按在纸上一次，然后手指收拢、把信拿起。
```

**`while` / `as` 的边界**（与 `h3-expression-psych` 已对齐，两边口径一致）

禁 `while` 的**真正理由**不是这个词本身，而是它把**两个主体动作**并联，模型只能把两条运动链平均成一个不存在的姿态。

> 【工艺·原文依据】*"Without them the model has to guess whether your described events happen in sequence or simultaneously, and it **usually picks simultaneously**, which is what produces the mushy, everything-at-once clips."*（防翻车词库·补充勘误）

**判定规则：看并联的两样东西是不是「两个都需要模型构造解剖结构的主体动作」。**

| 情形 | 判定 | 例 |
|---|---|---|
| 主体动作 **+** 另一个主体动作 | ❌ **禁**（等同 `while`） | ❌ `She sips while waving while walking.` → ✅ `She picks up the cup, then takes a sip, then takes one step forward.`<br>❌ `She walks as she talks.` → ✅ `She walks two steps, then stops, then speaks.` |
| 主体动作 **+** 次级运动 / 瞬时事件（眨眼、呼吸、发丝、衣摆、一声响、一道光） | ✅ **允许** | ✅ `As she speaks, she blinks once.`<br>✅ `First she rises, then she turns, as a floorboard creaks under her weight.` |
| 主体动作 **+** 面部微动作（眨眼、吞咽、嘴角微动） | ✅ **允许**（不争夺解剖资源） | ✅ `She holds the letter steady as her jaw tightens.` |

→ **判定口诀：`as` 后接"不用模型构造身体结构的东西"（眨眼、呼吸、发丝、衣摆、环境声光）就可以；接"另一个要摆姿势、转重心、动手的动作"就不行。**

> ⚠️ **与 `h3-expression-psych` 统一口径**：**`As she speaks, she blinks once` 不属禁用范围**——这是让静止的脸活起来的主力写法，大特写可放心用。
> ⚠️ **唯一官方例外**：画外音必须写 `... says in an off-screen voiceover: <d>...</d> **while his lips remain completely closed.**`（【H3】官方原句）。这里的 `while` 是官方固定搭配，**照抄，不要改成 `then`**。

### 1.4 有界动作：每个动作必须有终点

**无界动作**（`she waves` / `he moves his arm` / `she keeps looking`）没有终止条件，模型会在剩余时长里让动作**无限延续或原地抖动**——这是"末帧抖动"和"后半段空转"的直接成因。

**有界动作三要素**：**起点 → 路径（可选） → 终点（必写）**

| 要素 | 写法 | 例 |
|---|---|---|
| 起点 | 开场姿态（见 §5.3） | `both arms hanging at her sides` |
| 路径 | 方向 + 幅度（可量化最好） | `her right hand lifts to chest height` |
| **终点** | **明确的接触点 / 姿态 / 位置** | `and presses flat against the paper` |

| ❌ 无界 | ✅ 有界 |
|---|---|
| `She reaches toward the shelf.` | `She reaches forward and rests her fingertips on the edge of the shelf.` |
| `He turns around.` | `He turns 90 degrees to face the window and stops there.` |
| `She lowers her hand.` | `She lowers her hand until it rests flat on the tabletop.` |
| `He walks away.` | `He takes three steps toward the doorway and stops just inside it.` |
| `She looks down.` | `Her gaze drops to her hands and holds there.` |

**终点三选一（按可靠性排序）**：① **物理接触点**（`until it rests flat on the tabletop`）② **角度/距离量化**（`rotates about 45 degrees`）③ **明确姿态**（`ends with both arms hanging at her sides`）。

### 1.5 动作数量上限

**统一口径：节拍数 = 动作数 = 表情变化数。完整时长—节拍对照表见 `h3-expression-psych` §5.1（权威版在那边，避免两处维护）；本 skill 只保留下面两条执行细则。**

**两条硬规则**
1. **节拍数上限 = 3，与镜头多长无关。** 超过 3 个动作 → 拆镜，不要塞第 4 个节拍。（10 秒主镜也不是 4 拍，而是 3 拍 + 更长的收尾状态。母模板 §9.3 的 10 秒 B 主镜正是 3 拍 + 收尾。）
   - 参考区间：1.5s → 1 拍；2–3s → 2 拍；≥3s → 3 拍；≥5s → 3 拍 + 1 个收尾状态（**收尾状态不是第 4 拍**，它是段⑦的末帧声明 `By the end of the shot...`，不新增动作）。
2. **并行动作数恒为 0**（次级运动不计入，见 §1.3）。

**叠加约束**（来自 `h3-expression-psych`，叠加非替代）：同时变化的面部区域 **≤2 个**（眉/眼/鼻/唇/下颌/颈肩 六区）——三区同时变会被平均成抖动。表情拍最多带 2 区变化，肢体拍不受限。

> 【待验证】本表节拍数为【推】，基于"每个动作需 1.5–3 秒才立得住"与"并行会崩"两条已知规律推导，**无 H3 官方量化基准**。
> **实测方法**：固定一条 10 秒主镜（同一提示词、同一种子、8 步），分别写 2 / 3 / 4 / 5 个串联动作各生成 10 条，逐帧统计"最后一个动作是否完成"与"肢体是否崩坏"，找崩坏率开始陡升的点。

### 1.6 压缩式动作写法（补齐母模板 §4.5 悬空引用）

**适用场景**：为裁切而生成的镜头——**生成 4 秒，只用前 1.5–2 秒**（衔接"哭完、说完狠话、被扇完"等镜头）。动作均匀铺满则裁后断在半路，动作太快则剩余时长空转抖动。

**解法：动作前置 + 余韵兜底**

```
[动作段] First <短动作 A>，then <短动作 B>，then <收尾小动作>。  ← 三条全在前 1.5–2s
[余韵段] She holds that position, <唯一的次级运动：一次呼吸 / 一次眨眼 / 衣摆落定>,
         and nothing else changes for the remainder of the shot.   ← 后半段主动"锁死"
```

```
First her chin lifts, then her jaw tightens, then her gaze rises to a fixed point beyond
the lens. She holds that gaze; her breathing slows; nothing else changes for the remainder
of the shot.
中：她先抬起下巴，然后咬紧牙关，然后视线抬向镜头外一个固定点。她保持这个凝视，
呼吸放缓，在本镜剩余时间画面内没有其他变化。
```

**三条规则**：① 动作**全部写进前三拍**，每拍一个瞬时/有界小动作；② **`nothing else changes for the remainder of the shot` 必须写**——主动声明"后半段不许有新动作"，压住空转抖动；③ 余韵段**只留一个次级运动**（呼吸 / 眨眼 / 衣摆 / 发丝），多一个就变成并行。

> 【推】基于「动作第一帧就做完 → 后半段空转抖动」反向设计，**未做 A/B 实测**（见附 1 #2）。

### 1.7 动作段禁用词与替换表

| ❌ 禁用 | 为什么 | ✅ 替换 |
|---|---|---|
| `while`（连接两个**主体动作**） | 强制并行，两条运动链被平均 | `then` |
| `at the same time` / `simultaneously`（连接两个主体动作） | 同上 | 拆成 `then` 序列 |
| `as`（后接另一个**主体动作**） | 同上 | 拆句；或改接次级运动 / 瞬时事件 |
| `her eyes move to the left` / 纯眼球转动 | 眼球是局部形变，无刚体约束，高风险 | 抬头看：`her chin lifts and her gaze rises to a fixed point`<br>横移视线：`she turns her head slightly to frame right, her gaze follows`<br>⚠️ **两句仅限中小景别；大特写禁写视线变化**，改 `gaze held level, one slow blink`（`h3-expression-psych` §4.3.2）<br>⚠️ 用**画面方位**不用角色左右（`frame right` 不是 `her right`，§6.4-C）<br>**口诀：大特写静止，中小景别才动；动就动头，别只动眼。** |
| `keeps -ing` / `continues to -ing`（后接肢体动作） | 无界，会抖 | 给接触点：`until it rests on ...` |
| `slowly`（单独使用，无终点） | 慢但无终止 → 半途而废 | `slowly, until her palm lies flat on the desk` |
| `waves` / `gestures` / `moves around` | 抽象动词，模型自由发挥度最高 | 拆成有界：抬手 → 停在某个位置 |
| `interacts with` / `touches` | 无接触点定义 | 写明接触面：`rests her palm flat against the wooden surface` |
| `looking sad / angry / determined` | 情绪不可见（心理外化，见 §2.3） | 写肌肉变化：`her jaw tightens, her eyebrows draw together` |

> ✅ **`while` / `as` 不禁用的情形**（见 §1.3 判定表）：后接**次级运动或瞬时事件**时可用——`As she speaks, she blinks once.` / `Her coat sways as she walks.` 这两类**不属禁用范围**。
> ⚠️ **唯一官方例外**：画外音必须写 `... says in an off-screen voiceover: <d>...</d> **while his lips remain completely closed.**`（【H3】官方原句）。这里的 `while` 是官方固定搭配，**照抄，不要改成 `then`**。

---

## 2. 动作库（30+ 标准化写法）

> **使用方式**：表格里的"标准英文写法"可**整句复制**进 `integrated_multimodal_description` 的动作段。
> **风险等级**沿用母模板 §5.2 口径（高 / 中 / 低），对应 `风险类型` 码：`H` 手部、`B` 肢体、`P` 物理。

### 2.1 位移动作（Locomotion）

**模板句式**
```
First she <起始姿态>, then she <位移，含步数/方向/终点>, then she <停住并稳定重心>.
```

| # | 动作 | 标准英文写法 | 中文 | 风险 |
|---|---|---|---|---|
| 1 | 站起 | `She pushes up from the chair, then straightens her legs, then rises fully to standing and settles her weight.` | 她从椅子上撑起，然后伸直双腿，然后完全站起并稳住重心。 | 中（重心转移） |
| 2 | 坐下 | `She steps back until her calves touch the chair, then lowers herself, then sits upright with both feet flat on the floor.` | 她后退到小腿碰到椅子，然后坐下，然后坐直、双脚平放地面。 | 中 |
| 3 | 迈步 / 走出画 | `She takes three steps toward the doorway, then stops just inside it.` | 她朝门口走三步，然后停在门内。 | 中 |
| 4 | 转身 | `She turns 90 degrees to her right, then stops with her shoulders square to the window.` | 她向右转 90 度，然后停下、双肩正对窗户。 | 低 |
| 5 | 后退 | `She takes two steps backward, then stops when her back meets the wall.` | 她后退两步，然后背碰到墙时停住。 | 中（有接触点，反而是加分项） |
| 6 | 走近 | `She walks forward until she stands one arm's length from the desk, then stops.` | 她向前走，直到距桌子一臂之遥，然后停下。 | 中 |
| 7 | 穿过门口 | `She walks through the doorway and exits the frame on the right; the frame holds empty for the last beat.` | 她穿过门口、从画面右侧出画；末拍画面留空。 | 中 |
| 8 | 上台阶 | `She lifts one foot onto the first step, then brings the other up beside it, then stands still.` | 她一只脚踏上第一级台阶，然后另一只脚并上，然后站定。 | **高**（多段重心转移） |
| 9 | 停下 | `She slows, then comes to a full stop with both feet planted shoulder-width apart.` | 她放慢，然后完全停住，双脚与肩同宽踩实。 | 低 |
| 10 | 跪下 / 蹲下 | `She bends at the knees and lowers herself until one knee touches the floor, then she holds that position.` | 她屈膝下蹲，直到一侧膝盖触地，然后保持该姿势。 | **高** |

> ⚠️ **#8 上台阶与 #10 跪蹲属高危**——多关节连续重心转移是解剖崩坏重灾区。
> **降级**：改拍**结果态**（`She is already standing on the second step, one hand resting on the railing.`）或改拍**局部**（只拍脚：`A close-up frames her shoes on the first two steps.`）。

### 2.2 手持动作（Hand-held Object）

**模板句式**
```
First her <左/右> hand <起点>, then it <路径>, then <接触点/终点>.
```

| # | 动作 | 标准英文写法 | 中文 | 风险 |
|---|---|---|---|---|
| 11 | 拿起（大物） | `She closes both hands around the mug, then lifts it clear of the table, then holds it steady at chest height.` | 她双手握住杯子，然后把它端离桌面，然后在胸前端稳。 | 中 |
| 12 | 放下 | `She lowers the folder until it lies flat on the desk, then slides her hand away and lets it rest at her side.` | 她把文件夹下放至平躺桌面，然后把手抽开、垂回身侧。 | 中 |
| 13 | 推过去（无接触传递） | `He slides the cup across the table toward her, then withdraws his hand below the frame line.` | 他把杯子沿桌面推向她，然后把手撤到画面下沿之外。 | **低**（替代"递"） |
| 14 | 握持（静置） | `Both hands are wrapped around a large ceramic mug, fingers fully hidden behind the mug.` | 双手环握一只大陶瓷杯，手指完全被杯身遮住。 | **低** |
| 15 | 翻页 | `Her right hand turns the corner of the page over, then flattens it against the book.` | 她右手把页角翻过，然后把它抚平在书上。 | **高**（精细持物） |
| 16 | 掀开布/盖 | `She lifts one corner of the cloth, then folds it back onto itself, then lays her hand flat beside it.` | 她掀起布的一角，然后把它翻折回去，然后把手平放在旁边。 | 中 |
| 17 | 拉开抽屉 | `She closes her hand around the drawer pull, then draws the drawer open halfway, then lets go.` | 她握住抽屉把手，然后把抽屉拉出一半，然后松手。 | **高**（机械约束） |
| 18 | 举杯到嘴边（不喝） | `She raises the mug until the rim touches her lower lip, then holds it there.` | 她把杯子举到杯沿触到下唇，然后停住。 | **高**（接触点过小） |
| 19 | 收进衣袋 | `She slips the folded paper into her coat pocket, then lets her hand hang naturally at her side.` | 她把折好的纸塞进外套口袋，然后让手自然垂在身侧。 | 中 |
| 20 | 按住（替代"按按钮/打字"） | `Her hand is already resting flat on the wooden surface; her fingers stay still.` | 她的手已经平放在木质表面上；手指保持不动。 | **低**（改动作的结果态） |

> ⚠️ **#15 翻页、#17 抽屉、#18 举杯到唇** 的共同问题是**接触面小或存在机械约束**。
> **降级**：一律改拍**已完成态**（`The page is already turned.`、`The drawer stands half open.`、`The mug is already set down beside her.`）。

### 2.3 表情联动动作（Facial / Emotional）

> **铁律：写可见的肌肉变化，不写情绪名词。** 心理必须外化（母模板 §6.4 B）。

**模板句式**
```
First <眉/眼部>, then <唇/口部>, then <下颌>, then <头部/视线终点>.
```

**三条共享规则（与 `h3-expression-psych` 对齐，两边同口径）**

| # | 规则 | 说明 | 反例 |
|---|---|---|---|
| **A** | **表情链按面部区域从上到下排**：眉 → 眼 → 鼻 → 唇 → 下颌 → 颈/肩 | 符合肌肉扩散方向，更自然 | ❌ `first her jaw tightens, then her brows draw together` |
| **B** | **同时变化的面部区域 ≤ 2 个**：2 区用 `and` 或拆成两拍，**但 `while` 仍然禁** | 三区同时变会被平均成抖动 | ✅ `then her jaw tightens and her eyebrows draw together`<br>❌ `brows draw together while jaw tightens`——**禁的是 `while` 这个并发标记，不是"两区并列"本身**<br>❌ 眉蹙 + 下颌收紧 + 唇抿紧（3 区） |
| **C** | **视线变化用头 / 下巴承载，不写纯眼球转动** | 头部转动是大尺度刚体运动，比眼球局部形变稳（同 §2.1 转身/抬头逻辑） | ❌ `her eyes move to the left`（高风险） |

| # | 动作 | 标准英文写法 | 中文 | 情绪对应 |
|---|---|---|---|---|
| 21 | 抬眼 | `She blinks once, then her chin lifts, then her gaze rises to a fixed point beyond the lens.` | 她眨一次眼，然后抬起下巴，然后视线抬向镜头外一个固定点。 | 下定决心 / 挑衅 |
| 22 | 低头 | `Her gaze drops to her hands, then her chin lowers toward her chest, then she holds there.` | 她视线垂到手上，然后下巴向胸口低下，然后保持。 | 心虚 / 回避 |
| 23 | 皱眉 | `Her eyebrows draw together, then a vertical crease forms between them, then her jaw tightens.` | 她双眉靠拢，然后眉间出现一道竖纹，然后咬紧牙关。 | 困惑 / 愤怒 |
| 24 | 咬唇 | `Her lower lip disappears briefly between her teeth, then her mouth closes and her jaw sets.` | 她的下唇被牙齿轻轻咬住片刻，然后嘴合上、下颌绷紧。 | 忍耐 / 紧张 |
| 25 | 吞咽 | `Her throat moves once as she swallows, then her shoulders drop by a fraction.` | 她吞咽时喉部动了一下，然后肩膀微微下沉。 | 压抑 / 认命 |
| 26 | 冷笑 | `Her eyes narrow a little, then the corners of her mouth lift slightly, then she turns her head and looks away.` | 她的眼睛微眯，然后嘴角微微上扬，然后她转过头移开视线。 | 冷笑 / 讥讽 |
| 27 | 深呼吸 | `Her shoulders rise on a slow inhalation, then fall, then she goes still.` | 她随一次缓慢吸气而耸肩，然后落下，然后静止。 | 平复 / 蓄势 |
| 28 | 转头看向画外 | `She turns her head to frame right, then holds her gaze on something off-screen.` | 她把头转向画面右侧，然后视线停在画外某处。 | 接下镜（视线匹配） |
| 29 | 肩膀下沉 | `Her shoulders drop, then her arms settle closer to her sides, then she is still.` | 她双肩下沉，然后手臂更贴近身侧，然后静止。 | 泄气 / 放松 |
| 30 | 后仰 / 缩回 | `Her head draws back a few centimetres, then her chin lowers slightly, then she holds the pose.` | 她的头后缩几厘米，然后下巴微低，然后保持该姿势。 | 惊惧 / 防备 |

> ⚠️ **大特写只承载静态凝视**（`衔接镜类型库` #4：禁止用大特写演情绪转折）。反转瞬间改**中近景**。

### 2.4 交互动作（Interaction）

**模板句式**
```
First <A 的动作，有终点>, then <B 的动作，有终点>.  ← A、B 必须分拍，绝不并行
```

| # | 动作 | 标准英文写法 | 中文 | 风险 | 降级方案 |
|---|---|---|---|---|---|
| 31 | 无接触传递 | `He sets the envelope on the table, then slides it across the surface toward her, then withdraws his hand.` | 他把信封放在桌上，然后沿桌面推向她，然后把手撤回。 | **低** | — |
| 32 | 指向（泛指） | `She raises one arm and points toward the far end of the room, then lowers it.` | 她抬起一只手臂指向房间另一端，然后放下。 | 中 | 指向**大方向**，不要指向具体小物件 |
| 33 | 敲门 | `He closes his hand into a fist, then knocks twice on the door panel, then lowers his arm.` | 他握拳，然后在门板上敲两下，然后放下手臂。 | 中 | 只拍背影 + 只出声音也可 |
| 34 | 推门 | `He pushes the door open about thirty degrees, then steps through, then the door swings shut behind him.` | 他把门推开约 30 度，然后走进去，然后门在他身后关上。 | 中 | ⚠️ **不要写"从铰链侧开"**（硬阻断） |
| 35 | 举杯示意（替代握手） | `He raises his glass to chest height and holds it there; she nods once.` | 他把杯子举到胸高并停住；她点一次头。 | **低** | 替代"握手" |
| 36 | 递文件（结果态） | `The folder is already lying on the desk between them; both hands rest flat on the surface.` | 文件夹已经摊在他们之间的桌面上；双方双手平放在桌面。 | **低** | 替代"递交"全过程 |
| 37 | 挡住 / 拦下 | `She steps sideways until she stands between him and the doorway, then stops.` | 她侧移一步，直到站在他与门口之间，然后停住。 | 中 | 用**站位**代替肢体接触 |
| 38 | 拉住（→ 改为拉住大物） | `She closes both hands around the strap of the bag and holds it against her chest.` | 她双手攥住包的带子，把它抱在胸前。 | **高**（人物间接触） | 人物肢体接触**优先改成站位或道具中介** |
| 39 | 拍肩 / 拥抱 | ⛔ **硬阻断** | — | **极高** | 改：两人**并肩站立**、**隔桌对视**、或只拍**两只手各自平放**（不同框接触） |

> ⛔ **人物之间的物理接触（握手、拥抱、拍肩、搀扶、打斗）属高危至硬阻断**，模型无接触约束，会渲染成融合或穿模。**替代：用空间关系表达亲密/冲突**——距离、站位、朝向、视线（§6.3）。

### 2.5 微动作与次级运动（Micro-motion / Secondary Motion）

> 【工艺·关键】**命名次级运动才能得到次级运动**。不写，模型只给你一个静态道具。

**模板句式（必须另起一句，不并入主动作链；或用 `as` 直接挂在主体动作上）**
```
<主动作链，then 串联>. Meanwhile, <次级运动 1>; <次级运动 2>.
<主体动作>, as <次级运动>.     ← 见 §1.3，这个 as 不禁用
```
> ⚠️ `Meanwhile` / `as` 只能接**次级运动与瞬时事件**（衣摆、发丝，及眨眼、呼吸、吞咽等面部/身体微动作，与 `h3-expression-psych` 对齐）；**绝不接两个主体动作**（`She walks as she talks` 仍禁）。次级运动不计入 §1.5 节拍数，但不要堆过 2 条。

| #（41–46） | 微动作 | 标准英文写法 | 中文 | 用途 |
|---|---|---|---|---|
| 41 | 呼吸起伏 | `Her shoulders rise and fall once with a slow breath.` | 她的肩膀随一次缓慢呼吸起伏。 | 证明"活着"，防僵 |
| 42 | 发丝飘动 | `A few strands of hair lift and settle at her temple.` | 几缕发丝在她的太阳穴处扬起又落下。 | 补自然感 |
| 43 | 衣摆摆动 | `The hem of her coat sways once with the movement and settles.` | 她的外套下摆随动作摆动一次后落定。 | 位移后必加 |
| 44 | 重心转移 | `Her weight settles onto her back foot; her shoulders level out.` | 她的重心落到后脚上；双肩恢复水平。 | 位移动作的收尾 |
| 45 | 手指静置 | `Her fingers stay gently curled and held together throughout.` | 她的手指全程保持自然弯曲并拢。 | 手部锚定（见 §3.4） |
| 46 | 眨眼 | `She blinks once, slowly.` | 她缓慢地眨一次眼。 | 衔接镜最低成本动作；**静态大特写防恐怖谷必加**（§9.3） |

> 环境类微动作（热气 / 灰尘 / 光影流动）归 `h3-env-scene` §1.3、§4，本表只收人物身上的次级运动。

---

## 3. 手部专章（最重要）

### 3.1 为什么手是崩坏之王

| 成因 | 说明 | 推导出的对策 |
|---|---|---|
| **像素占比极小** | 中景全身里手只占几百像素，跨注意力难以把各部位映射到正确位置 | **提高占比** → 手部特写反而比中景全身稳（反直觉但已被实测确认） |
| **姿态组合极多** | 27 个自由度，训练分布长尾 | **消灭手指分离需求** → 握拳、叠放、插兜、背手 |
| **训练样本大量被遮挡** | 数据里手常被物体/其他手挡住 | **主动遮挡** → 让物体挡住手指 |
| **视频叠加跨帧变化** | 指骨数量会在帧间变化 | **减少手在画面里的运动量** → 静置 > 移动 |

### 3.2 三档降级决策树

```
这个镜头必须出现手吗？
│
├─ 不必须 → 【档 ①】手出画 / 被遮挡   ← 最稳，优先选
│           写法：改景别、改构图、用物体挡、插兜、背手
│
├─ 必须出现，但可以不动
│   └─ 手里需要拿东西吗？
│       ├─ 不需要 → 【档 ②】静置 + 明确静态姿态   ← 次稳
│       │           写法：正向锚定句库（§3.4）
│       └─ 需要   → 东西够大吗？
│                   ├─ 够大（杯/碗/书/包/文件夹）→ 【档 ③】大物体握持
│                   └─ 太小（笔/钥匙/针/硬币）  → ⛔ 改动作（§3.7 极高风险档）
│
└─ 必须出现，且必须动 → 先看 §3.7 风险表
                        ├─ 低 / 中风险 → 写有界动作 + 手部锚定句
                        └─ 高 / 极高风险 → 改动作或改拍结果态（§8.3）
```

### 3.3 档 ①：手出画 / 被遮挡（6 个可直接复制的句式）

```
① both hands tucked fully into her coat pockets, the hand shapes hidden beneath the fabric
   中：双手完全插在外套口袋中，手的轮廓藏在衣料之下

② framed from the waist up; both hands are below the frame line
   中：取景自腰部以上，双手位于画面下沿之外

③ her hands rest behind her back, hidden from camera
   中：她的双手背在身后，镜头看不到

④ both hands wrapped around a large ceramic mug, fingers fully hidden behind the mug
   中：双手环握一只大陶瓷杯，手指完全被杯身遮住

⑤ her hands are covered by the wool blanket drawn up to her chest
   中：她的手被拉到胸前的羊毛毯盖住

⑥ a close-up frames only her forearms resting on the table; her hands are cropped at the
   bottom edge of frame
   中：特写只拍她搁在桌上的小臂，双手在画面下边缘被裁掉
```

> 💡 **档 ① 的进阶用法：先出画，后入画。** 需要手部动作时，让手**从画面外进入并完成动作**，动作完成后**立刻撤回画外**——把高风险窗口压到最短。
> `His right hand enters the frame from the lower edge, sets the key on the table, then withdraws below the frame line.`（中：他的右手从画面下沿进入，把钥匙放在桌上，然后撤回画外。）

### 3.4 档 ②：静置 + 明确静态姿态（正向锚定句库）

> **核心原理**：用正向描述**占据描述位**，畸形解就无处安放。这比任何否定句都强。

**基础锚定串（逐字复制，不要用同义词替换）**

```
Her hands hang naturally at her sides, fingers gently curled and held together, thumbs resting
along the seams of her trousers, five fingers on each hand, natural finger proportions, holding
this exact pose throughout the shot.
中：她的双手自然下垂贴于身侧，手指自然弯曲并拢，拇指沿裤缝贴合，每只手五根手指，
手指比例自然，本镜全程保持这一姿势。
```

**变体句式（按姿态选一条）**

| 姿态 | 英文写法 | 中文 |
|---|---|---|
| 平放桌面（掌心向下） | `Her hands lie flat on the table, palms down, five fingers held together, fingers fully visible and cleanly separated.` | 她的双手平放在桌上，掌心向下，五指并拢，手指完整可见、彼此分明。 |
| 交叠置于膝上 | `Her hands rest folded in her lap, the left hand laid over the right, fingers relaxed and held together.` | 她的双手交叠放在膝上，左手搭在右手上，手指放松并拢。 |
| 握拳撑在桌面 | `He rests a closed fist on the table, fingers curled inward, knuckles visible, the fist unmoving.` | 他把一只握紧的拳放在桌上，四指内收，指节清晰可见，拳头保持不动。 |
| 平覆在布料上 | `Her hand lies flat against the fabric of her skirt, palm down, five fingers held together.` | 她的手平覆在裙摆布料上，掌心向下，五指并拢。 |
| 单手扶在固定物上 | `One hand rests flat against the doorframe at shoulder height, fingers spread naturally against the wood.` | 一只手平扶在门框上、与肩同高，手指自然地贴住木面。 |
| 双手捧物（大物） | `She holds the book open with both hands, thumbs resting along the inner edges, the other fingers hidden behind the covers.` | 她双手把书捧开，拇指压在内缘，其余手指被书封遮住。 |

**手部锚定三件套**（任何手部入画的镜头都至少带一套）
1. **数量**：`five fingers on each hand`
2. **形态**：`fingers gently curled and held together` / `clean separation between fingers`
3. **持续性**：`holding this exact pose throughout the shot`

### 3.5 档 ③：大物体握持

**为什么大物体更稳**：手指被物体挡住 → **手指分离需求归零**。物体越大，挡得越多。

| 握持对象 | 写法 | 遮挡程度 |
|---|---|---|
| 大陶瓷杯 | `Both hands are wrapped around a large ceramic mug, fingers fully hidden behind the mug.` | ★★★★★ |
| 硬皮书 | `She holds the hardcover book against her chest with both hands, fingers hidden behind the covers.` | ★★★★★ |
| 文件夹 / 纸箱 | `He carries the box with both hands, fingers curled under the bottom edge, only the backs of his hands visible.` | ★★★★ |
| 玻璃杯（中） | `Her right hand closes around the glass, fingers wrapped fully around the body of the glass.` | ★★★ |
| 帆布袋带子 | `Both hands close around the strap of the canvas bag, held together against her chest.` | ★★★★ |

> ⚠️ **握持 + 移动 = 风险叠加**。需要移动时，物体要**更大、更贴近身体**：
> `She carries the box against her chest with both hands, elbows tucked against her sides.`（比端着杯子走动稳得多）

### 3.6 无接触传递（用"推"替代"递"）

> 【2.3 实测·机制通用】官方指南原文：*"Contact-free transfers sidestep the hardest hand problem."*
> `hands her the cup` 的失败率显著高于 `slides the cup across the table toward her`。

| ❌ 接触传递 | ✅ 无接触传递 | 中文 |
|---|---|---|
| `He hands her the letter.` | `He sets the letter on the table, then slides it across the surface toward her, then withdraws his hand.` | 他把信放在桌上，然后沿桌面推向她，然后把手撤回。 |
| `She passes him the keys.` | `She places the keys on the counter and pushes them a short distance toward his side; her hand then rests flat on the counter.` | 她把钥匙放在台面上，朝他那侧推近一小段；然后她的手平放在台面上。 |
| `He gives her the ring.` | `The small velvet box is already open on the table between them; her right hand closes around its lid.` | 那只小绒盒已经摊开放在两人之间的桌上；她的右手合上盒盖。 |
| `She takes the cup from his hand.` | `The cup is already standing on the table in front of her; she closes both hands around it and lifts it.` | 杯子已经摆在她面前的桌上；她双手握住并端起。 |
| `They shake hands.` | `They stand one arm's length apart and nod once to each other; both pairs of hands remain at their sides.` | 他们相距一臂，互相点头一次；双方的双手都垂在身侧。 |

**三拍结构（无接触传递的标准写法）**
```
① A 把物放到中介面上（有接触点：桌面/台面/柜台）
② A 沿面推向 B 的方向（有界：推到某处停）
③ A 的手撤回（出画或静置）→ 下一拍才轮到 B 的手
```

### 3.7 手部风险分级表（细化版）

| 等级 | 动作 | 崩坏形态 | 处置 |
|---|---|---|---|
| **低** | 双手插兜 / 背手 / 手出画 / 握大物静置 / 双手交叠静置 / 手掌平放桌面 | 几乎不崩 | 直接用 |
| **中低** | 握拳（静止）/ 手掌平覆布料 / 手扶门框、椅背、栏杆等固定物 | 偶发指节异常 | 直接用 + 带锚定句 |
| **中** | 举杯到胸高（不喝）/ 翻书页 / 拉开抽屉 / 掀开盒盖 / 关门 | 手指数量漂移、物体变形 | 用**有界动作 + 结果态兜底**；准备备选方案 |
| **中高** | **捏衣角 / 捻发梢 / 抠手指 / 摩挲物件表面** | 手指融合、指尖消失、手指穿进布料 | **降级：改"手掌平覆布料，掌心向下，五指并拢"** |
| **高** | 递接物品（任何接触式）/ 举起小物件到眼前 / 打字 / 敲键盘 | 手物分离、物品漂浮 | 改无接触传递（§3.6）或改结果态 |
| **极高** | **签字 / 持笔写字 / 插钥匙进锁孔 / 扣纽扣 / 系鞋带 / 用筷子 / 拨号** | 手指数量崩、笔消失、笔尖与纸面不接触、钥匙穿模 | ⛔ **建议直接改动作**（§8.3） |
| **✗ 硬阻断** | 小尺度精确对准（指尖点按、钥匙对孔）/ 机械约束（车门从铰链侧开、门把手旋转） | 无 3D 朝向跟踪与刚体约束 | **不给交互点特写**；改拍结果态 |

> 母模板原表：握拳（中）＜ 捏衣角（高）＜ 签字/持笔/插钥匙（极高，建议直接改动作）。本表在它基础上补齐了中间档与硬阻断档。

### 3.8 景别与手部的配合（反直觉但重要）

**手部特写比中景全身稳。** 原因是像素占比。

| 景别 | 手占画面 | 稳定性 | 用法 |
|---|---|---|---|
| **大特写（手占 ≥1/2 画面）** | 极大 | ★★★★ | **需要手部动作时的首选**，不是最后手段 |
| 特写（胸以上） | 大 | ★★★ | 手在胸前动作可用 |
| 中近景（腰以上） | 中 | ★★ | 手需静置或握大物 |
| 中景（全身） | 小 | ★ | ⚠️ **最容易崩手**，双手应出画或插兜 |
| 全景 / 远景 | 极小 | — | 手部细节不可辨，反而不崩（因为看不出） |

**手部特写标准写法**（衔接镜类型库 #2）
```
A large close-up frames her hands from the wrist up, filling more than half the frame: five
fingers on each hand, natural finger length and spacing, clean separation between fingers,
clean edges against the background. First her fingers close slowly around the folded letter,
then she lifts it clear of the desk, then she holds it steady.
中：大特写从手腕以上拍她的双手，占画面一半以上：每只手五根手指，手指长度与间距自然，
指间分明，与背景边缘干净。她先缓慢地握住折好的信，然后把它端离桌面，然后端稳。
```

**四条硬规则**：
1. 手占画面 **≥1/2**；
2. 背景**极简**（虚化纯色 / 单一材质表面），减少边缘歧义；
3. **一镜只做一个手部动作**；
4. 必带**数量 + 形态 + 持续性**三件套锚定句。

### 3.9 绝对禁写的否定句

> 【工艺】VLM 解析否定会失败（arXiv:2508.10931 反向激活效应）：**"不要六指"里的"六指"会作为名词进入条件分布，反而把六指激活。**

| ❌ 绝对禁写 | 为什么 | ✅ 改写成 |
|---|---|---|
| `no six fingers` / `not six fingers` | 裸名词否定，反向激活 | `five fingers on each hand` |
| `do not generate extra fingers` | 模型要先构想"extra fingers"再否定 | `five fingers on each hand, natural finger proportions` |
| `no deformed hands` / `no mutated hands` | 同上 | `fingers gently curled and held together, natural joints` |
| `no extra limbs` / `no extra arms` | 同上 | `exactly one person in frame, two arms, both hanging at her sides` |
| `hands must not be fused` | 同上 | `clean separation between fingers` |
| `avoid six fingers, deformed hands, extra limbs, malformed fingers, mutated hands...` | **成串否定清单**会稀释引导力，真正要禁的那条反而不生效 | 挑 **1 句** `Do not ...` 放末尾，前面必须已有正向描述 |

**ⓐ 默认方案（纯正向，推荐）**
```
Her hands rest flat on the table, fingers held together, five fingers on each hand,
natural finger proportions, clean separation between fingers, holding this exact pose
throughout the shot.
中：她的双手平放在桌上，手指并拢，每只手五根手指，手指比例自然，指间分明，
本镜全程保持这一姿势。
```

**ⓑ 正向锚定 + 一句 `Do not` 收边（有效）**
```
Her hands rest flat on the table, fingers held together, five fingers on each hand,
natural proportions. Do not let the hand shape change or the fingers separate during the shot.
中：她的双手平放在桌上，手指并拢，每只手五根手指，比例自然。本镜全程手形不变、手指不分开。
```
> **适用条件**：`Do not` 句必须置于正向锚定**之后**，占用每镜唯一 1 句 `Do not` 的额度，且**内容限 B 类**（变化 / 时长 / 运动）。上例的 `change` / `separate` 是变化，属 B 类；写成 `Do not add extra fingers` 则属 A 类，违规。

**结构与内容分开写**（`h3-antibug` §1.3 最终口径）

| 层 | 规则 |
|---|---|
| **结构** | 正向锚定 + 末尾**最多 1 句** `Do not`，该句前**必须有正向状态描述** |
| **内容** | 该 `Do not` **只写 B 类**（变化/时长/运动：`does not move` / `holds steady`）；**A 类**（可视元素：`letters` / `logos` / `extra fingers`）**一律改正向** |

**配套三条**：① **混合句就低不就高**——含 A 类成分则整句判 A 类；② **开放量词按 A 类判**——`Do not add anything` 的 `anything` 是开放集合；③ **【待验证】**——机制推演（arXiv:2508.10931），非 H3 实测，纯正向写不出可申报例外。

> → **手部否定句合法写法只有一种**：正向锚定前置 + 末尾 1 句 **B 类** `Do not`（即 ⓑ）；A 类手部名词**零档位**。
> → **B 类 `Do not` 不冗余**：正向句描述静态外观，`Do not` 约束"全程不变"，是前者未覆盖的维度；A 类才冗余。
> → 此口径**闭合了 4 次提请裁决的母文件冲突**（词库 §3 vs 主模板 §6.4-F，**以后者为准**）。

---

## 4. 肢体结构与人数控制

### 4.1 人数写死并前置

> 【工艺】人数在跨帧状态跟踪中易漂移——模型会在背景里"长出"第二个人。

**写法铁律**：**人数写在该镜第一句**，且用**绝对数字**（不用 "a man"、"some people"）。

| 人数 | 标准声明句 |
|---|---|
| 1 | `Exactly ONE person in frame: a single subject, held for the entire shot.` |
| 2 | `Exactly TWO people in frame, and the count stays at two for the entire shot.` |
| 3 | `Exactly THREE people in frame; the number stays fixed from the first frame to the last.` |
| 群演 | `Blurred passersby in the soft-focus background, their faces left soft and indistinct.` ⚠️ **不要给数量以外的细节** |

> ⚠️ 官方原句原为 `..., no additional figures anywhere in the shot.` 形式，按 A 类裁定线已改正向；`Exactly N` 已锁人数，后半句冗余。

> ⚠️ **群演写法**：只写 `blurred passersby in the background`，**不要**写 `five people walking behind her`——给了具体数字，模型会去数，数错了就是穿帮；写"虚化的背景人群"，观众不会去数。

### 4.2 多人时第一句就拉开外观差异

> 【工艺·已知根因】**对称描述会诱导人物融合**（把两个人渲染成一个有两颗头的身体，或身体互相穿插）。

❌ **反例（必崩）**
```
two men in suits
two women standing in the room
a man and a woman talking
three people in dark clothes
```
共同点：**类别相同 + 描述对称 + 无空间分离**。

✅ **正例（母模板标准写法）**
```
A tall man in a red apron (left third of frame) and a short woman in a denim jacket
(right third of frame); the man folds his arms, then the woman takes one step forward.
中：一名穿红色围裙的高个男人（画面左三分之一）与一名穿牛仔外套的矮个女人
（画面右三分之一）；男人抱起双臂，然后女人向前迈一步。
```

**差异维度清单（至少拉开 3 项）**

| 维度 | 差异示例 | 优先级 |
|---|---|---|
| **画面位置** | `left third of frame` vs `right third of frame` | ★★★★★ **必写** |
| **身高体型** | `a tall broad-shouldered man` vs `a short slight woman` | ★★★★★ **必写** |
| **服装颜色（高对比）** | `a red apron` vs `a denim jacket` | ★★★★★ **必写** |
| 发型发色 | `close-cropped grey hair` vs `shoulder-length black hair` | ★★★★ |
| 年龄 | `a man in his sixties` vs `a woman in her twenties` | ★★★ |
| 朝向 | `angled toward frame right` vs `angled toward frame left` | ★★★ |
| 姿态 | `standing` vs `seated` | ★★★ |

**三人及以上的站位模板**
```
Exactly THREE people in frame. On the left third, a tall older man in a charcoal overcoat,
standing. At centre, a shorter woman in a mustard-yellow sweater, seated. On the right third,
a teenage boy in a blue hoodie, leaning against the wall. The frame holds exactly these
three people.
中：画面中严格三人。左三分之一为一名穿炭灰色大衣的高个年长男性，站立；中间为一名穿
芥末黄毛衣的矮个女性，坐着；右三分之一为一名穿蓝色连帽衫的少年，倚墙，画面保持这三人。
```

### 4.3 关节状态声明句

> 【工艺】模型无骨骼约束，肘/膝/肩/颈是反折高发部位。

**通用句（可整句复制）**
```
Both arms hang at his sides throughout; both shoulders remain level and square to camera;
his elbows keep a soft natural bend at his sides; his neck stays aligned with his spine;
his head stays level, lowered only enough for a slight downward glance.
中：他的双臂全程垂在身侧；双肩保持水平并正对镜头；肘部在身侧保持自然的柔和弯曲；
颈部与脊柱对齐；头部保持水平，只低到足以形成轻微下视。
```

| 部位 | 声明句 | 中文 |
|---|---|---|
| 肩 | `both shoulders remain level and square to camera` | 双肩保持水平并正对镜头 |
| 肘 | `both elbows keep a soft natural bend` | 双肘保持自然的柔和弯曲 |
| 腕 | `her wrists stay straight, in line with her forearms` | 她的手腕保持平直，与前臂成一线 |
| 膝 | `both knees point forward, in line with her feet` | 双膝朝前，与双脚同向 |
| 颈 | `his neck stays aligned with his spine, chin level` | 他的颈部与脊柱对齐，下巴水平 |
| 躯干 | `her torso stays upright, her waist facing forward` | 她的躯干保持直立，腰腹正朝前方 |
| 整体 | `natural human anatomy, natural joint articulation, exactly two arms and two legs` | 自然人体解剖，自然关节活动，两条手臂两条腿 |

**运动类声明句**
```
Slow, single, bounded movement; the motion stays smooth and continuous; her feet stay in
contact with the ground; her direction stays constant.
中：缓慢、单一、有界的运动；动作保持平滑连贯；双脚保持与地面接触；方向保持恒定。
```

### 4.4 多人时的动作分配规则

| 规则 | 说明 | 例 |
|---|---|---|
| **一镜一人一动作** | 同一时间只有一个人主动 | `the man folds his arms, then the woman takes one step forward` |
| **用 `then` 隔开两人的动作** | 绝不写 `while the other...` | ✅ `..., then the woman ...` ❌ `... while the woman ...` |
| **被动方写结果态** | 另一人保持静态姿态 | `the man remains perfectly still, both hands at his sides` |
| **两人同时动 = 拆镜** | 无法避免时切成两镜 | Shot 1 拍 A，Shot 2 拍 B |

### 4.5 融合 / 漂移反例 → 正例速改表

| ❌ 反例 | 崩在哪 | ✅ 改成 |
|---|---|---|
| `two men in suits` | 类别相同 + 描述对称 + 无空间分离 | `a tall man in a charcoal suit at frame left and a shorter man in a light grey suit at frame right` |
| `a man and a woman talking` | 无外观差异、无位置 | `Exactly TWO people in frame: a man in his sixties in a dark wool coat at frame left, a woman in her twenties in a mustard sweater at frame right.` |
| `three people standing in the room` | 人数未写死、无差异、无位置 | `Exactly THREE people in frame: ...`（见 §4.2 三人站位模板） |
| `the group moves closer` | 群体主体 + 复数同时动作 = 融合温床 | `She takes one step forward; the others remain perfectly still.` |
| `a crowd of people` | 数量不可控 | `blurred passersby in the soft-focus background, their faces left soft and indistinct` |
| `everyone turns to look at her` | 多人同一动作 | `Only the man at frame left turns his head; the others keep their gaze forward.` |

### 4.6 双人镜完整示例（可直接复制）

```
Exactly TWO people in frame, and the count stays at two for the entire shot. On the left third, a tall
man in his sixties in a dark wool overcoat, standing with his weight evenly distributed,
both hands at his sides. On the right third, a shorter woman in her twenties in a
mustard-yellow sweater, seated upright, both hands folded in her lap. They remain one
arm's length apart, and this distance stays constant for the whole shot.

First the man folds his arms, then the woman lifts her chin, then she holds her gaze on him.
Both shoulders stay level; neither figure moves from their position. The camera holds a
static shot. By the end of the shot both are still in the same positions, framed from the
waist up. The frame holds exactly these two people for its full duration.

中：画面中严格只有这两人，全程保持两人。左三分之一为一名六十多岁、穿深色羊毛大衣的
高个男性，站立，重心均匀分布，双手垂于身侧。右三分之一为一名二十多岁、穿芥末黄毛衣的
矮个女性，端坐，双手交叠放在膝上。两人相距一臂之遥，该距离全程不变。

男人先抱起双臂，然后女人抬起下巴，然后她保持对他的凝视。双方双肩保持水平；两人都不离开
各自的位置。镜头保持固定。到本镜结束时两人仍在原位置，取景自腰部以上。画面任意位置
不要出现第三个人。
```

---

## 5. 姿态与静态锁定

### 5.1 五种基础姿态的标准描述串

> **用法**：整串复制进该镜的段①（开场构图），或段⑦（收尾状态）。
> **每个姿态串都自带重心与支撑面**——这两项是模型判断"人是否站得住"的线索。

| 姿态 | 标准描述串（EN） | 中文 |
|---|---|---|
| **站** | `She stands with her feet shoulder-width apart, her weight evenly distributed on both feet, both arms hanging naturally at her sides, her shoulders level, her torso upright.` | 她双脚与肩同宽站立，重心均匀分布在双脚上，双臂自然垂于身侧，双肩水平，躯干直立。 |
| **坐** | `She sits upright on the chair with her back straight, both feet flat on the floor, her knees together, both hands resting folded in her lap.` | 她在椅上坐直，背部挺直，双脚平放地面，双膝并拢，双手交叠放在膝上。 |
| **倚** | `He leans back against the wall with his shoulders and upper back in contact with it, his weight carried by the wall, one knee slightly bent, both arms hanging at his sides.` | 他背靠墙后仰，双肩与上背贴住墙面，重心由墙承担，一侧膝盖微屈，双臂垂于身侧。 |
| **蹲** | `She crouches with both feet flat on the floor, her knees bent to roughly 90 degrees, her weight forward over her toes, one hand resting on the floor for support.` | 她蹲下，双脚平踩地面，双膝屈至约 90 度，重心前移到脚趾上方，一只手撑地辅助。 |
| **卧** | `She lies on her back on the bed, her head resting on the pillow, her arms straight alongside her body, her legs extended and slightly apart.` | 她仰卧在床上，头枕在枕头上，双臂伸直置于身体两侧，双腿伸展并微微分开。 |

**变体补充**

| 姿态 | 描述串（EN） | 中文 |
|---|---|---|
| 站（重心偏移） | `She stands with her weight on her back foot, her front foot slightly forward, one hand resting on the back of the chair for support.` | 她重心落在后脚，前脚略向前，一只手扶在椅背上支撑。 |
| 坐（前倾） | `She sits leaning forward, her forearms resting on the table, her shoulders raised slightly toward her ears.` | 她坐着前倾，小臂搁在桌上，双肩向耳朵方向微微抬起。 |
| 倚（单侧） | `He stands with one shoulder against the doorframe, his weight on one leg, the other leg relaxed.` | 他单肩抵着门框站立，重心在一条腿上，另一条腿放松。 |
| 半起（动作延续） | `She is held mid-rise, knees bent at roughly 120 degrees, torso leaning forward, the motion deliberately unfinished.` | 她停在半起的姿势，双膝屈至约 120 度，躯干前倾，动作故意未完成。 |

### 5.2 重心与支撑面

> 【推】模型不会推理物理，但**你写了重心与支撑面，它就有了可复用的画面先验**。这是"减伤"不是"根治"。

**必写的三项**

| 项 | 写法 | 例 |
|---|---|---|
| **支撑面** | 明确写出与地面/家具的**接触部位** | `both feet flat on the floor` / `her back against the wall` / `one hand resting on the floor` |
| **重心位置** | 明确写出重量落在哪 | `her weight evenly distributed on both feet` / `her weight on her back foot` |
| **辅助支撑**（可选） | 加一个接触点，显著提高稳定感 | `one hand resting on the back of the chair for support` |

**支撑面越多越稳**（单脚 < 双脚 < 双脚 + 一个扶手）。设计动作时，**主动加一个支撑点**是成本最低的稳定性提升手段。

**接触加固句**（让物体与人体"焊"在一起，防漂浮、防穿模）
```
The chair legs stay in full contact with the floor; her shoes rest flat on the surface;
every object keeps its own solid volume; rigid objects stay rigid.
中：椅腿与地面保持完全接触；她的鞋平踩在地面上；每个物体都保持各自完整的实体体积；刚性物体保持刚性。
```

### 5.3 姿态锁定三件套

任何有明确姿态要求的镜头，三段都要写（**开场 → 保持 → 收尾**），缺一段就容易被中途改姿态。

```
① 开场姿态：A medium shot frames her <姿态串>，...
② 保持句：  She holds this position; <唯一的次级运动>, and nothing else changes.
⑦ 收尾状态：By the end of the shot she is still <同一姿态串>, <最终构图>.
```

```
A medium shot frames her seated upright at the desk, both forearms resting on the surface,
her hands folded. She holds this position; her breathing lifts her shoulders slightly, and
nothing else changes. By the end of the shot she is still seated in the same posture, framed
from the waist up, her gaze lowered to the papers.
中：中景拍她端坐在桌前，两条小臂搁在桌面上，双手交叠。她保持这个姿势；呼吸让她的
肩膀微微起伏，画面内没有其他变化。到本镜结束时她仍以同一姿势坐着，取景自腰部以上，
视线低垂看向文件。
```

### 5.4 姿态参数量化（为动作延续衔接服务）

> 母模板 §3.3 动作延续衔接法要求：**姿态参数必须可量化和复述，下一段要能逐字抄回这个数字。**

| 参数 | 写法 | 用于 |
|---|---|---|
| 关节角度 | `knees bent at roughly 120 degrees` / `knees bent to roughly 90 degrees` | 半起、蹲 |
| 旋转角度 | `her shoulders rotated about 45 degrees` / `she turns 90 degrees to her right` | 转身、半转 |
| 距离 | `one arm's length` / `two steps back` / `until her calves touch the chair` | 走位、坐下 |
| 高度 | `lifts to chest height` / `raises it until the rim is level with her chin` | 持物 |
| 倾角 | `torso leaning forward about 30 degrees` | 前倾、半起 |

**动作延续三件套写法**（跨段接力）
```
【上一段 C 出镜】... the turn deliberately unfinished, her shoulders rotated about 45 degrees.
【下一段 A 入镜】... already mid-turn, shoulders rotated about 45 degrees — resuming exactly
                  the pose held at the end of the previous shot.
```
> **参数必须逐字抄回**，改一个数字衔接就断了。

---

## 6. 空间距离与走位

### 6.1 可度量距离声明

> 【工艺·已知翻车】距离不一致（两人忽远忽近）是物理空间类的主要翻车形态。

**规则**：距离要**可度量**（用身体单位或物件单位，不要用米——模型对米没有视觉先验）。

| 单位 | 写法 | 中文 | 适用 |
|---|---|---|---|
| **臂长** | `one arm's length apart` / `two arm's lengths apart` | 一臂之遥 / 两臂之遥 | 两人站立距离 |
| **步数** | `two steps apart` / `three steps behind him` | 相隔两步 / 在他身后三步 | 前后距离 |
| **参照物** | `the width of the table between them` / `a chair's width apart` | 隔着一张桌子 / 相隔一把椅子的宽度 | 有家具时（更可靠） |
| **接触** | `their shoulders are almost touching` / `standing back to back` | 肩膀几乎相碰 / 背对背站立 | 极近距离（比写"拥抱"稳） |
| **画面位置** | `left third of frame` / `right third of frame` | 画面左/右三分之一 | ⭐ **最可靠**，优先用 |

> ⭐ **最佳实践：用画面位置代替物理距离。** `On the left third of frame... / On the right third of frame...` 比 `one metre apart` 可控得多——模型直接按构图安排，不需要推断尺度。

**距离恒定声明句（多人镜必带）**
```
Two people stand two arm's lengths apart, and this distance stays constant for the whole shot.
中：两人相距约两臂之遥，该距离在全镜头内保持不变。
```

### 6.2 用画面方位，不用角色左右

> ⚠️ **母模板明确警告**：「她的左边」有歧义（是她的左手边还是画面左边？），是左右翻转翻车的常见根因。

| ❌ 错误 | ✅ 正确 |
|---|---|
| `he stands on her left` | `he stands on the left third of frame` |
| `the lamp is to his right` | `the lamp stands at the right edge of frame` |
| `she turns to her left` | `she turns toward frame left` |
| `the door is behind them` | `the door is at the back of the frame, on the far side of the room` |

> ⚠️ **本规则只管构图与跨镜一致性，不管单镜内身体部位**：`his right hand` / `her left knee` / `a single tear runs down her right cheek` 用角色左右即可，**改成 `frame right hand` 属过度纠正**。
> **唯一例外**：锁定块含不对称面部特征（疤、痣、单边耳环）时，左右须与锁定块逐字一致——那是跨镜身份锚点（见 `h3-character`）。

**【AXIS】块（跨请求时每镜逐字复制）**
```
[AXIS] The woman stands at frame left, angled toward frame right.
The man stands at frame right, angled toward frame left.
The window is behind them on the far side of the room.
The camera stays on the near side of the desk throughout.
中：女人站在画面左侧，朝向画面右侧。男人站在画面右侧，朝向画面左侧。
窗户在他们身后、房间远端。机位全程停在桌子的近侧。
```
**三个要点**：① 用绝对画面位置；② 加一个**不动的背景锚点**（窗/门/墙），锚点比人物描述可靠；③ **方向、朝向、行进方向三者会一起翻，必须一起写**。

> ⚠️ **固定 seed 救不了左右翻转**——seed 用于复现结果，不跨提示词承载空间约定。

### 6.3 多人站位模板

| 人数 | 关系 | 站位模板（EN） | 中文 |
|---|---|---|---|
| 2 | **对面对峙** | `They stand facing each other across the table, she at frame left and he at frame right, roughly one table's width apart.` | 他们隔着桌子面对面站立，她在画面左、他在画面右，相隔约一张桌子的宽度。 |
| 2 | **并肩** | `They stand side by side at the centre of frame, shoulders almost touching, both facing camera.` | 他们并排站在画面中央，肩膀几乎相碰，都朝向镜头。 |
| 2 | **前后** | `She stands at frame centre; he stands two steps behind her and slightly to frame right, his face partly obscured by her shoulder.` | 她站在画面中央；他站在她身后两步、略偏画面右，脸被她的肩部部分遮住。 |
| 2 | **过肩** | `An over-the-shoulder shot frames her at the centre; the back of his head and one shoulder occupy the lower-left quarter of frame as a dark, untextured silhouette, cleanly separated from her edge.` | 过肩镜头把她放在中央；他的后脑与一侧肩部占据画面左下四分之一，呈无纹理的暗色剪影，与她的轮廓干净分离。 |
| 3 | **三角** | `Three people form a loose triangle: the older man at frame left, the woman at frame centre slightly forward, the boy at frame right and further back.` | 三人构成一个松散三角形：年长男性在画面左，女性在画面中央略微靠前，男孩在画面右且更靠后。 |

> ⚠️ **过肩前景压到 1/4 以下并做成纯暗剪影**（衔接镜类型库 #8）。前景带纹理必闪。

### 6.4 走位路径写法

> 规则：**单一方向、单一路径、有终点。** 折线走位（先左后右）在 H3 上极易崩。

**模板**
```
She walks in a single straight line from <起点画面位置> to <终点画面位置>, then stops.
```

| 走位 | 写法（EN） | 中文 |
|---|---|---|
| 横穿画面 | `She walks in a single straight line from frame left to frame right, then exits the frame.` | 她沿单一从画面左到右的直线走过，然后出画。 |
| 走向镜头 | `She walks directly toward the camera, then stops when she fills the frame from the waist up.` | 她径直走向镜头，然后在占满腰部以上画面时停下。 |
| 背离镜头 | `She walks away from the camera along a straight path, growing smaller, until she reaches the far doorway.` | 她沿直线背离镜头走远、身形变小，直到抵达远处的门口。 |
| 绕行（⚠️） | ⛔ `She walks around the table, then behind him.` | 折线 + 遮挡关系变更，**高危** → 改为：**只拍一段**（`She walks from frame left to the near edge of the table, then stops.`） |
| 穿过遮挡物 | `He walks past the camera from frame right to frame left; his shoulder briefly fills the frame before he clears it.` | 他从画面右向左经过镜头；他的肩膀短暂占满画面，然后让开。 |

**运动方向锚点四条（跨段走位必守）**
1. **两段必须用同一个运镜/方向 token**（都用 `Truck right`，不要一段 `pan` 一段 `move`）；
2. **方向句写在该镜开头**，不要埋在场景描述之后；
3. **给两段一个共同物理参照物**（上段末"深色墙面充满画面" → 下段首"从深色墙面继续向右进入"）；
4. **上段出口方向 = 下段入口方向，严禁反向**。

### 6.5 避免穿模：接触声明句

```
Every object keeps its own solid volume; rigid objects stay rigid; liquids stay inside their
containers; every object in contact with a surface stays in contact for the entire shot.
中：每个物体都保持各自完整的实体体积；刚性物体保持刚性；液体留在容器内；每个与表面
接触的物体在整个镜头内保持接触。
```

| 场景 | 声明句 | 中文 |
|---|---|---|
| 人物与家具 | `She stays fully seated; her back remains in contact with the chair back.` | 她保持完全坐姿；背部始终贴着椅背。 |
| 物体与桌面 | `The mug remains on the table, its base in full contact with the surface.` | 杯子留在桌上，杯底与桌面完全接触。 |
| 两人之间 | `The space between them stays open and constant throughout.` | 两人之间的空间全程保持敞开且恒定。 |
| 门与框 | `The door swings within its frame and stays attached to its hinges.` | 门在门框内摆动并保持与铰链连接。 |

---

## 7. 动作与运镜的配合

### 7.1 一镜一运镜（官方硬规则）

> 【H3 相关·实测】*"One camera move per clip is not a stylistic preference, it is the operating limit."*

**三个以上运镜会被模型"平均"成混乱漂移。**

**官方术语表（保留英文原文）**

| 效果 | 官方写法 |
|---|---|
| 物理靠近 / 远离 | `Push In` / `Pull Out` |
| 改变焦距 | `Zoom In` / `Zoom Out` |
| 原地水平旋转 / 整机横移 | `Pan Left` / `Pan Right` / `Truck Left` / `Truck Right` |
| 垂直旋转 / 整机升降 | `Tilt Up` / `Tilt Down` / `Pedestal Up` / `Pedestal Down` |
| 环绕 / 跟随 / 固定 / 主观 | `Arc Shot` / `Tracking Shot` / `Static Shot` / `POV` |
| 抖动 / 滚转 | `Shake Slightly` / `Shake Strongly` / `Roll Clockwise` / `Roll Counterclockwise` |

**搭配顺序**：**motion type → amplitude → speed**，写成自然英文句，不堆标签。
```
✅ The camera pushes in with small amplitude at slow speed from a medium shot to a close-up.
❌ Push in. Small. Slow. Close-up.
```
> 【H3】*"Add amplitude and speed only when they are meaningful; medium amplitude and normal speed are usually omitted."* —— 中等幅度与正常速度**省略不写**，留给模型反而更稳。

### 7.2 动作幅度 ↔ 运镜幅度 匹配表

| 动作幅度 | 推荐运镜 | 幅度 / 速度 | 理由 |
|---|---|---|---|
| **微动作**（眨眼、呼吸、视线移动） | `Static Shot` | 不写 | 主体几乎不动，固定机位最稳；加运镜反而引入漂移 |
| **小动作**（手放到桌面、低头、转头） | `Push In` / `Pull Out` | `with small amplitude at slow speed` | 小推近强化注意点 |
| **中动作**（站起、坐下、转身 90°） | `Static Shot` 或 `Push In` | `with small amplitude at slow speed` | ⚠️ **重心转移类动作不要加横移/环绕**，双重运动必崩 |
| **走位**（走 2–3 步） | `Tracking Shot` / `Truck Left/Right` | `at slow speed` | 跟随方向必须与走位方向一致 |
| **揭示**（局部 → 整体） | `Pull Out` | `with large amplitude at slow speed` | 拉远段 **≤3 秒且 ≤该镜时长 50%**（衔接镜类型库 #7） |
| **对话 / 反应** | `Static Shot` | 不写 | 一镜一说话人 + 固定机位 = 最稳组合 |

> ⚠️ **核心禁忌：动作与运镜同时大幅变化。** `She stands up while the camera arcs around her` 是典型的双高危叠加——重心转移 + 视角连续变化，两个不确定源相乘。
> **改法**：① 先站起（固定机位），② 再环绕（人已站定）。分两镜，或把环绕改成小幅推近。

### 7.3 常见组合模板（可直接复制）

```
【模板 A · 静止 + 小动作】
The camera holds a static shot. First her gaze drops to the letter, then her right hand lifts
and presses once flat against the paper, then her fingers curl and she picks the letter up.
中：镜头保持固定。她先垂下视线看向信，然后右手抬起、平按在纸上一次，然后手指收拢、
把信拿起。

【模板 B · 小推近 + 情绪递进】
The camera pushes in with small amplitude at slow speed from a medium close-up to a close-up.
First she blinks once, then her jaw tightens and her eyebrows draw together, then her chin
lifts and her gaze rises to a fixed point beyond the lens.
中：镜头以小幅慢速从中近景推近至特写。她先眨一次眼，然后咬紧牙关、双眉靠拢，然后
抬起下巴、视线抬向镜头外一个固定点。

【模板 C · 跟拍 + 走位】
The camera tracks with her at slow speed as she walks in a single straight line from frame
left to frame centre, then stops when she reaches the desk.
中：镜头以慢速跟随她，她沿单一从画面左到画面中央的直线行走，然后在抵达书桌时停下。

【模板 D · 拉远揭示（慎用）】
The camera pulls out with large amplitude at slow speed, revealing the full room. She remains
seated and perfectly still throughout the move.
中：镜头大幅慢速拉远，揭示整个房间。在整个运镜过程中她保持坐姿、完全静止。
   ↑ 关键：运镜期间主体必须静止，否则双重运动
```

### 7.4 运镜句的位置

> 【工艺】模型对靠前 token 权重更高。**运镜句写在该镜靠前的位置**，不要埋在中段或堆在末尾。
> 【H3】*"Camera motion should be written as a natural English action within the shot, rather than stacked as separate labels at the end of a sentence."*

**优先级排序（严格按此写）**
```
第 1 层（最前）：运镜 + 景别
第 2 层：主体 + 人数（写死）
第 3 层：动作（then 串联，给终点）
第 4 层：环境 + 光位
第 5 层：约束句（每条一行）
第 6 层（最后）：复述第 1 层与第 5 层的关键项（首尾双写）
```

---

## 8. 高难度动作的降级方案

### 8.1 动作类硬阻断清单（提示词解决不了）

| # | 项 | 为什么 | 唯一可行方案 |
|---|---|---|---|
| 1 | **小尺度精确对准**（钥匙插锁、指尖点按、纽扣对扣眼） | 无 3D 朝向跟踪与刚体约束 | **不给交互点特写**；改拍结果态（钥匙已在锁孔里 / 门已开） |
| 2 | **机械约束**（车门从铰链侧开、门把手旋转、拉链拉动） | 模型不理解铰链与转轴 | 改拍**开到一半的结果态**；或只出声音 |
| 3 | **人物间物理接触**（握手、拥抱、搀扶、打斗、推搡） | 无接触约束，手臂会融合/穿模 | 用**空间关系**替代（距离/站位/朝向/视线）；或只拍局部 |
| 4 | **液体动态**（倒水、酒液晃动、泼洒） | 结构性缺陷（ICML 2025：模型抄训练样本而非推理物理） | 改拍**静态结果**：`a glass of water already full on the table, the bottle at rest beside it.` |
| 5 | **跨请求的左右方位一致** | 每次生成为独立采样，无空间状态传递 | 放进**同一次请求**（首选）；或后期水平镜像 |
| 6 | **跨请求的 180° 轴线 / 正反打朝向** | 模型没有轴线概念 | 同一次请求内完成；或后期镜像 |
| 7 | **布料大幅动态**（脱外套、系围巾、裙摆翻飞） | 布料解算不可靠 | 改拍**已穿好/已脱下**的结果态；或只让衣摆小幅摆动一次 |

> **遇到这几类，第一反应是改分镜，不是改提示词。**

### 8.2 降级决策树

```
遇到一个动作
  ↓
① 它在 §8.1 硬阻断清单里吗？
   ├─ 是 → ⛔ 改分镜（换一个能拍的镜头表达同样的叙事信息）
   └─ 否 → ②
  ↓
② 它在 §3.7 的「高 / 极高」档吗？
   ├─ 是 → 优先【规避】：换成另一个动作（见 §8.3 对照表）
   │        不能换 → 【降级】：改拍结果态，且该镜不承载关键叙事信息
   └─ 否 → ③
  ↓
③ 按本 skill 的标准写法写：then 串联 + 有界终点 + 手部/关节锚定句
  ↓
④ 生成后崩了？→ 走 §9 返工 SOP，不要直接改词
```

**处置四值**（母模板 §8.6）
| 值 | 含义 | 例 |
|---|---|---|
| **规避** | 改分镜 / 改动作，从源头绕开 | 签字特写 → 合上文件 |
| **降级** | 镜头保留，但不承载关键叙事信息 | 手机屏只发冷白光，不留内容 |
| **后置** | 生成时不解决，交给后期 | 屏幕内容后期贴、左右方位后期镜像 |
| **重生成** | 抬步数 / 换种子 / 微调提示词 | 概率性崩坏，且不在硬阻断清单内 |

### 8.3 高危动作 → 替代动作 对照表

| # | 高危动作 | 崩坏形态 | ✅ 替代动作（可直接复制） |
|---|---|---|---|
| 1 | 签字 / 持笔写字 | 笔消失、手指数量崩、笔尖离纸 | `She closes the folder and lays her hand flat on the cover.`<br>她合上文件夹，把手平放在封面上。 |
| 2 | 插钥匙开锁 | 钥匙穿模、对不准孔 | `The key is already in the lock; her hand closes around it and turns.` → 更稳：`The door stands ajar; she pushes it open with her shoulder.` |
| 3 | 倒水 | 水流浮空、分流、越界 | `A glass of water already full stands on the table, the bottle at rest beside it.` |
| 4 | 递接物品 | 手物分离、物品漂浮 | `He sets it on the table, then slides it across the surface toward her, then withdraws his hand.` |
| 5 | 握手 | 手臂融合、手指穿模 | `They stand one arm's length apart and nod once; both pairs of hands remain at their sides.` |
| 6 | 拥抱 / 拍肩 | 肢体融合 | `She steps closer until she stands half a step from him, then stops; they remain facing each other without touching.` |
| 7 | 打斗 / 推搡 | 严重解剖崩坏 | **只拍局部**：`A close-up frames two pairs of shoes on the floor, one pair stepping back.`；或只拍**反应**（旁观者的脸） |
| 8 | 脱外套 / 系围巾 | 布料解算崩 | 结果态：`She is already standing with her coat over her arm.` |
| 9 | 用筷子 / 吃饭 | 手部 + 食物双重崩 | `She sets the chopsticks down beside the bowl, then rests both hands in her lap.` |
| 10 | 打字 / 敲键盘 | 手指数量崩、手与键盘不接触 | 只出声音：`Her hands rest flat on the desk on either side of the keyboard; the sound of typing continues.` |
| 11 | 扣纽扣 / 系鞋带 | 手指与物体不接触 | 结果态：`Her coat is already buttoned; she lowers her hands to her sides.` |
| 12 | 抽烟 / 点烟 | 手部 + 火 + 烟三重崩 | 结果态：`A lit cigarette rests in the ashtray, a thin thread of smoke rising from it.` |
| 13 | 上台阶 / 下楼梯 | **重心转移 + 上下台阶叠加**——肢体崩坏高发组合 | 结果态：`She is already standing on the landing, one hand resting on the railing.`（**改拍"已站在平台上"的静态中景**，规避整段风险；场景串见 §8.4） |
| 14 | 骑车 / 跑步 | 全身快速运动 | 静态替代：`She stands beside the bicycle, one hand on the handlebar, perfectly still.` |
| 15 | 镜子里的反射动作 | 镜像 + 双重人物 | ⚠️ **慎用**；改拍**过肩**或**正面特写** |

### 8.4 楼梯 / 车辆（由 `h3-env-scene` 转入，归口本 skill）

楼梯属肢体高风险场景（§8.3 #13）。确需楼梯镜时用下面这串，人物**只作静态站位**：

```text
A concrete stairwell at night. Grey painted concrete walls on both sides. A single flight of
concrete steps descends from the upper left of frame toward the camera. A metal handrail runs
along the left wall. A bare ceiling light hangs at the top of the flight.
```

**车辆**同族风险：只作背景、不作前景、不给车标。

---

## 9. 采样步数与返工 SOP

### 9.1 伪翻车识别（最容易误判的一条）

> 【三方·官方直播转述】*"如果你发现人物动作开始'散架'或者音画对不上，**第一件该怀疑的事就是步数压太低了，而不是 prompt 写错了**。"*
> ⚠️ 数值区间（4 / 6–8）为**社区共识而非官方硬指标**；核心规则源自 MiniMax 官方与 ComfyUI 联合直播的社区转述，**未找到 MiniMax 书面文档中的对应原文**。

**这类"翻车"的特征是：提示词没问题，是采样步数不够。**

| 场景 | 步数 |
|---|---|
| 试拍 / 找构图 | **4 步**（只看方向，不要求质量） |
| 出片 / 送审 / 交付 | **6–8 步** |

### 9.2 返工 SOP（六步，顺序不可颠倒）

```
画面崩了（肢体散架 / 音画不同步 / 动作不连贯 / 手部异常）
  ↓
⓪ 生成前内容检查：照 §10.1 的 17 条过一遍提示词
     （零成本——读一遍即可，不用生成、不用等）
     ← 拦下"设计错误"类崩坏；这类抬步数救不了，只会得到高清版的错误（见 §9.3）
  ↓ 确认无设计错误
① 抬采样步数：4 → 6–8，重跑同一条提示词        ← 先做这个，不要先改词
  ↓ 仍不合格
② 检查参考文件的保留强度标记（retention_analysis 的 fully_preserved 等）
  ↓ 仍不合格
③ 换种子重跑（同一提示词、同一批参考文件）
  ↓ 仍不合格
④ 才动提示词：按 §3.7 / §8.3 降级动作
  ↓ 仍不合格
⑤ 改镜头设计（走 §8.2 的「规避」，换一个能拍的镜头）
```

> **⓪ 为何排在 ① 前**：主模板 §8.4「先怀疑步数」说的是**生成后看片阶段**；景别 / 强度 / 节拍数校验属**生成前内容检查**（§8.2），本就排在前且零成本。阶段错配，非冲突。
> ❌ **禁止**：步数一直是 4，却反复改提示词。**这是纯浪费**——你在低质量采样下评估每一版提示词，结论不可靠，还会把"这个镜头做不了"的错误结论写进分镜表。

### 9.3 崩坏类型 → 首查项 对照表

**⓪ 组：设计错误 —— 抬步数救不了，只会得到「高清版的错误」**

| 看到的崩坏 | 根因 | 首查项（⓪ 步） | 抬步数有用吗 |
|---|---|---|---|
| 大特写下五官扭曲 / 崩脸 | 大特写承载了情绪转折（设计错误） | **改景别到中近景**（§2.3） | ❌ **只崩得更清晰** |
| 2 秒镜里表情跳变 | 节拍数超承载量（§1.5） | **砍到 2 拍，或加时长** | ❌ 无效 |
| 全脸同时抖 | 3 个以上面部区域同时变（§2.3 规则 B） | **砍到 2 区** | ❌ 无效 |
| 两个动作糊成一团 | `while`/`as` 误接两个主体动作（§1.3） | **拆成 `then` 序列** | ❌ 无效 |
| 后半段空转抖动 | 动作无终点（§1.4） | **加接触点** / 用 §1.6 压缩式写法 | ❌ 无效 |
| 穿模 / 物体漂浮 | 在 §8.1 硬阻断清单里 | **⑤ 改分镜** | ❌ 无效 |

**① 组：概率性崩坏 —— 抬步数有效**

| 看到的崩坏 | 第一嫌疑 | 处置 |
|---|---|---|
| 全身"散架"、关节反折、肢体数量异常 | **步数太低** | ① 抬步数 |
| 音画不同步、动作不连贯 | **步数太低** | ① 抬步数 |
| 手部多指 / 融合 | 步数 → 手部动作风险等级 | ① 抬步数 → ④ 按 §3.7 降级 |
| 人物融合 | 对称描述 / 无空间分离 | ④ 拉外观差异 + 加画面位置 |
| 距离忽远忽近 | 缺距离恒定声明 | ④ 加 `this distance stays constant` |
| 末帧抖动 | 运镜收尾无声明 | ④ 加 `The camera settles and holds completely still for the final second, ending on a stable held frame with no drift.` |
| **五官不对称 / 大小眼 / 皮肤纹理逐帧生长 / 脸不像本人 / 视线没落点 / 眨眼抽搐** | 概率性或设计性表情崩坏 | **见 `h3-expression-psych` §9.7（判定表）+ §9.1–9.6（逐条处置）**，此处不重复维护 |

**⚠️ 唯一例外：恐怖谷（静态僵脸）不适用「先抬步数」**

| 症状 | 根因 | 处置 | 抬步数有用吗 |
|---|---|---|---|
| 恐怖谷 / 静态僵脸（脸完全不动、无眨眼无呼吸） | **缺次级运动**（§2.5） | **先加 `she blinks once` / 呼吸 / 发丝，再考虑抬步数** | ⚠️ **可能更糟** |

> 【推断，未实测】恐怖谷是唯一**抬步数可能更糟**的一项——步数越高皮肤越清晰，完全静止无眨眼无呼吸的脸越显假（实测见附 1 #8）。

> 【推】本表的"第一嫌疑"排序基于"步数是全局质量开关，其他都是局部因素"这一机制推断，**无公开量化基准**；⓪ 组的"抬步数无效"判定由 skill-expression 提供并已对齐。

### 9.4 分镜表字段

| 列 | 控件 | 枚举值 | 规则 |
|---|---|---|---|
| `采样步数` | 单选 | **4（试拍）** / **6–8（出片）** | 每条生成记录必填；**送审/交付一律 6–8** |
| `风险类型` | 单选 | `H` 手部 / `B` 肢体 / `P` 物理空间 等 9 码 | 见母模板附 2 |
| `风险等级` | 单选 | 高 / 中 / 低 | 高的镜头优先安排试拍 |
| `处置动作` | 单选 | 规避 / 降级 / 后置 / 硬阻断 | 填"硬阻断"时 `备选方案` 强制非空 |
| `备选方案` | 文本 | **必填** | 必须是"另一个能拍的镜头"，不得填"重试""调提示词" |

> **`采样步数` 列的作用**：让"伪翻车"可追溯。**如果某镜被判为失败但步数是 4，该失败结论无效，必须重测。**

---

## 10. 检查清单与正反例速查表

### 10.1 提交前检查（动作类，17 条）

```
□  1. 主体动作用 then 串联；while / as 只接次级运动，不接第二个主体动作（§1.3）
□  2. 每个动作都有接触点 / 角度 / 姿态终点（无界动作已清零）
□  3. 有 First ... then ... finally ... 时序连接词（只加 4 个词，性价比最高）
□  4. 节拍数 ≤3（与时长无关；≥5s = 3 拍 + 收尾状态，不是 4 拍）（§1.5）
□  5. 手部：走了三档降级决策树（出画 > 静置 > 大物握持）（§3.2）
□  6. 手部入画都带了"数量 + 形态 + 持续性"三件套锚定句（§3.4）
□  7. 提示词无任何含 six fingers / extra fingers / mutated 字样的句子（§3.9）
□  8. 人数在镜首写死（Exactly ONE / TWO / THREE person in frame）（§4.1）
□  9. 多人时外观差异 ≥3 项，且每人都写明画面位置（§4.2）
□ 10. 距离声明可度量（臂长 / 步数 / 画面位置），且有"全程不变"句（§6.1）
□ 11. 每镜只有 1 个官方运镜术语，且动作幅度与运镜幅度匹配（§7.2）
□ 12. 姿态写了开场 → 保持 → 收尾三件套，带重心与支撑面（§5.2 / §5.3）
□ 13. 表情链从上到下：眉 → 眼 → 鼻 → 唇 → 下颌 → 颈肩（§2.3 规则 A）
□ 14. 同时变化的面部区域 ≤2 个（§2.3 规则 B）
□ 15. 视线由头 / 下巴承载，没写纯眼球转动；**大特写没写视线变化**（§2.3 规则 C）
□ 16. 【三元一致性】表情 / 肢体 / 台词指向同一状态（见下方校验表）
□ 17. 每镜最多 1 句 Do not，置末尾，前面有正向描述，**且只能装 B 类**
```

**三元一致性校验表**（与 `h3-expression-psych` §6.1 共用，动作侧负责最右列）

| 表情 | 肢体动作应指向同一状态 | ❌ 不一致（观众读出精神分裂） |
|---|---|---|
| `jaw tightens, brows draw together`（愤怒 / 忍耐） | 攥拳、手撑桌面、身体前倾、肩部绷紧 | 手指放松交叠、身体后仰、肩膀下沉 |
| `chin lifts, gaze rises`（下定决心 / 挑衅） | 站直、肩展开、手离开支撑面 | 缩肩、低头含胸（尽管脸在抬） |
| `gaze drops, chin lowers`（心虚 / 回避） | 肩内收、手插兜、身体后缩 | 双臂张开、挺胸 |
| `shoulders drop, arms settle`（泄气 / 放松） | 手垂落、重心下沉、支撑面增大 | 攥拳、肌肉紧绷 |
| `eyes narrow, mouth corners lift`（冷笑） | 头部转向一侧、肩膀单侧抬起 | 双手捧物于胸前（示弱） |

> **校验口诀**：**脸在笑、手在攥拳 = 精神分裂。** 不一致时**改动作不改表情**（表情是情绪第一载体，优先级更高）。

### 10.2 看片检查（动作类，11 条）

```
□ 1. 手：逐帧看是不是五指、有没有融合 / 穿模 / 多指
□ 2. 关节：肘 / 膝 / 腕有没有反折
□ 3. 人数：全程是不是同一个人（没有被"长出"第二个人）
□ 4. 距离：两人间距有没有忽远忽近
□ 5. 动作：then 序列有没有真的按顺序发生（还是糊成一团）
□ 6. 终点：最后一个动作有没有走完（还是断在半路）
□ 7. 支撑：脚有没有踩在地面上、椅子有没有浮空
□ 8. 收尾帧：最后一帧是否稳定（供下一段接）
□ 9. 节拍：3 个节拍有没有都走完（第 3 拍没走完 = 超载）
□ 10. 三元一致性：表情 / 肢体 / 台词指向同一状态（脸在笑手在攥拳 = 精神分裂）
□ 11. 若以上任一项崩 → 先跑 §9.2 的 ⓪ 步，再查采样步数是不是 4
```

### 10.3 正反例速查总表

| 维度 | ❌ 反例 | ✅ 正例 |
|---|---|---|
| 时序 | `She sips while waving while walking.` | `She picks up the cup, then takes a sip, then takes one step forward.` |
| **次级运动并行（不禁）** | `She walks two steps, then stops, then speaks.`（丢了自然感） | `She walks two steps as her coat sways once and settles, then stops, then speaks.`<br>`As she speaks, she blinks once.`（面部微动作同理，大特写主力写法） |
| 时序连接词 | `She looks at the letter, tears it open, reads it.` | `First she looks at the letter, then she tears it open, then her gaze moves across the page.` |
| 动作终点 | `She reaches toward the shelf.` | `She reaches forward and rests her fingertips on the edge of the shelf.` |
| 手部传递 | `He hands her the cup.` | `He slides the cup across the table toward her, then withdraws his hand below the frame line.` |
| 手部锚定 | `Do not make six fingers.` | `Her hands rest flat on the table, five fingers on each hand, fingers held together, natural proportions.` |
| 人数 | `a man and a woman talking` | `Exactly TWO people in frame: a tall man in a red apron at frame left and a short woman in a denim jacket at frame right.` |
| 对称描述 | `two men in suits` | `a tall man in a red apron and a short woman in a denim jacket` |
| 关节声明 | （不写） | `Both arms hang at his sides throughout; both shoulders remain level; his elbows keep a soft natural bend.` |
| 距离 | `they stand close together` | `They stand one arm's length apart, and this distance stays constant for the whole shot.` |
| 左右 | `he stands on her left` | `he stands on the left third of frame` |
| 姿态 | `she sits there` | `She sits upright with her back straight, both feet flat on the floor, both hands folded in her lap.` |
| 支撑 | `she stands` | `She stands with her feet shoulder-width apart, her weight evenly distributed on both feet.` |
| 穿模 | （不写） | `Every object keeps its own solid volume; rigid objects stay rigid; her shoes rest flat on the floor.` |
| 运镜组合 | `The camera arcs around her while she stands up.` | `She rises fully to standing, then the camera begins a slow arc.`（或分两镜） |
| 运镜数量 | `Push in, then pan right, then tilt up.` | `The camera pushes in with small amplitude at slow speed.`（只留一个） |
| 液体 | `She pours water into the glass.` | `A glass of water already full stands on the table, the bottle at rest beside it.` |
| 次级运动 | （不写） | `Her coat sways once with the movement and settles; steam curls off the mug.` |
| 情绪外化 | `she looks determined` | `her jaw tightens, her eyebrows draw together, then her chin lifts` |
| 视线（纯眼球） | `her eyes move to the left` | `her chin lifts and her gaze rises to a fixed point beyond the lens` |
| 三元一致 | 脸在笑 + 手在攥拳 | 表情 / 肢体 / 台词指向同一状态（见 §10.1 校验表） |
| 走位 | `She walks around the table, then behind him.` | `She walks in a single straight line from frame left to the near edge of the table, then stops.` |

### 10.4 一键粘贴：动作段模板

```
【单镜动作段 · 通用模板】

<人数声明>；<画面位置>；<开场姿态串（§5.1）>
First <动作 A，有界终点>, then <动作 B，有界终点>, then <动作 C，有界终点>.
<次级运动句：衣摆 / 发丝 / 呼吸，只留 1–2 个>
The camera <官方运镜术语> with <small/large> amplitude at <slow/fast> speed.
<手部锚定句 / 关节声明句 / 距离恒定句，挑 3–5 条与当前镜强相关的>
By the end of the shot, <最终人物状态> + <最终构图>.
Do not <最多一句，且只能是 B 类：drift / flicker / shake / jitter 等靠变化察觉的词>.
   ⚠️ A 类（可视元素）写进 `Do not` 同样违规，一律改正向（§3.9）。

─────────────────────────────
【填好的例子】

Exactly ONE person in frame; at the right third of frame; she stands with her feet
shoulder-width apart, her weight evenly distributed, both arms hanging at her sides.
First her gaze drops to the letter on the desk, then her right hand lifts and presses once
flat against the paper, then her fingers curl and she picks the letter up. Her coat sways
once with the movement and settles; her breathing slows.
The camera pushes in with small amplitude at slow speed from a medium close-up to a close-up.
Both hands hold the letter steady, five fingers on each hand, natural proportions; both
shoulders stay level; her shoes remain flat on the floor. By the end of the shot she holds
the letter in both hands, framed from the chest up, her gaze fixed on the paper.
The letter shows an even blank surface.
```

---

## 附 1：待验证清单与实测方法

本 skill 中以下条目**无公开量化基准**，标注为【待验证】或【推】。**不要当作官方数据引用。**

| # | 待验证项 | 取值 | 实测方法（简式） |
|---|---|---|---|
| 1 | 节拍数上限 = 3（§1.5，同 `h3-expression-psych` §5.1） | 1.5s→1、2–3s→2、≥3s→3、≥5s→3+收尾 | 10 秒主镜，2/3/4/5 拍各 20 条，统计末动作完成率与崩坏率，找陡升点 |
| 2 | 压缩式动作写法（§1.6） | 动作前置 + `nothing else changes` 兜底 | 4 秒镜压缩式 vs 均匀铺开各 20 条，裁到 2 秒比动作完整性与末 1 秒抖动率 |
| 3 | 采样步数 4 / 6–8 | 试拍 4、出片 6–8 | 同一提示词 4/5/6/7/8 步各 20 条，逐帧统计崩坏率与音画同步率 |
| 4 | 手部三档降级的相对稳定性 | 出画 > 静置 > 大物握持 | 三档各 20 条，统计"手部可见异常"帧占比。建议指标 **HAFR**，目标 <2% |
| 5 | 人体接触动作崩坏率 | 判为硬阻断 | 各 20 条，统计"完全无穿模且无融合"成功率；若 >70% 可降为"高" |
| 6 | 重心/支撑面声明句减伤幅度 | 判为有效减伤 | 同一站姿镜，带/不带支撑面描述各 20 条，统计"脚部离地/浮空"帧占比 |
| 7 | `as` 接次级运动是否安全（§1.3） | 判为允许 | 同一镜，`as she speaks, she blinks once` vs 拆 `then` 各 15 条，比崩坏率与自然感 |
| 8 | 恐怖谷不适用「先抬步数」（§9.3） | 静态大特写先加眨眼 | 同一静态大特写，4 步与 8 步各 5 条，盲评"像不像活人" |
| 9 | A/B 类否定分级（§3.9） | 结构 1 句 Do not + 内容限 B 类 | 机制推演（arXiv:2508.10931），**非 H3 实测**。同一镜，纯正向 vs 正向+B类Do not 各 20 条，比崩坏率 |

**通用测试规范**：① **必须在真实运动条件下测**——静止画面测出的成功率无意义；② 每组 **≥20 次**；③ 记录**种子与步数**，否则不可复现；④ 逐帧看，只看首末帧会漏掉中间帧的指骨数量变化。

---

## 附 2：与主模板的术语对照（保持一致性）

| 概念 | 本 skill | 母模板 / 词库 | 状态 |
|---|---|---|---|
| 风险类型码 | `H` 手部 / `B` 肢体 / `P` 物理空间 | 9 码体系 | ✅ 沿用 |
| 处置四值 | 规避 / 降级 / 后置 / 硬阻断 | `处置动作` 枚举 | ✅ 沿用 |
| 手部三档降级 | ① 出画/遮挡 ② 静置 ③ 大物握持 | §4 四条规避原则 | ✅ 一致（本 skill 细化为决策树） |
| 手部风险分级 | 低→中低→中→中高→高→极高→硬阻断（7 档） | 握拳中 / 捏衣角高 / 签字极高 | ✅ 母表的细化扩展 |
| 姿态参数量化 | 角度 / 距离 / 高度 / 倾角 | §3.3.4 铁律 1 | ✅ 沿用 |
| 采样步数 | 试拍 4 / 出片 6–8 | §8.4、§14 | ✅ 沿用 |
| 压缩式动作写法 | §1.6 | §3.3A 引用了 §4.5 | ⚠️ **§4.5 缺失，本 skill 已补齐** |
| 时间连接词 | First/then/then/finally | 补充勘误 §3.1 | ✅ 沿用 |
| 无接触传递 | §3.6 | 词库 §4 ④ | ✅ 沿用 |
| 返工 SOP | §9.2 六步（⓪ 生成前检查 → ① 抬步数 → …） | §8.4 只说"先怀疑步数" | ✅ 沿用并补 ⓪ 步 |

**与 `h3-expression-psych` 的 8 条对齐口径**（表体只在彼处维护，此处留指针）

| 概念 | 本 skill | 对方 |
|---|---|---|
| `as` / `while`：禁两主体动作并联，接次级运动允许 | §1.3、§1.7 | 细化 |
| 节拍数上限 **≤3** | §1.5 | §5.1 |
| 同时变化的面部区域 **≤2** | §2.3-B | 采纳 |
| 表情链从上到下 眉→眼→鼻→唇→下颌→颈肩 | §2.3-A | 采纳 |
| 视线由头/下巴承载 | §2.3-C、§1.7 | §4.3.1 |
| 大特写禁写视线变化（改 `gaze held level`） | §1.7 | §4.3.2 |
| 三元一致性（本 skill 出"肢体"列） | §10.1 | §6.1 |
| ⓪ 生成前检查优先于抬步数；恐怖谷例外 | §9.2、§9.3 | §9.1–9.7 |

---

## 附 3：一句话速查

```text
动作：then 串联｜while/as 只接次级运动，不接第二个主体动作（As she speaks, she blinks ✅）
      ｜必须写 First...then...finally｜每动作给接触点做终点
      ｜节拍数 ≤3（与时长无关）｜并行动作数 = 0
表情：链条从上到下 眉→眼→鼻→唇→下颌→颈肩｜同时变化面部区域 ≤2｜视线由头/下巴承载
      ｜大特写不写视线变化，改 gaze held level｜三元一致：表情/肢体/台词 同状态
手部：出画 > 静置 > 大物握持｜无接触传递（推，不递）｜锚定三件套 = 数量+形态+持续性
      ｜禁写 six/extra fingers｜手部特写比中景全身稳（手占画面 ≥1/2）
肢体：人数镜首写死｜多人拉开 ≥3 项差异 + 各给画面位置｜关节声明句｜一人一动作
姿态：站/坐/倚/蹲/卧 各一串｜重心 + 支撑面｜开场 → 保持 → 收尾 三件套写全
距离：臂长/步数/画面位置，优先画面位置｜加"全程不变"｜用画面方位不用角色左右
走位：单一方向、单一路径、有终点｜上段出口方向 = 下段入口方向，严禁反向
运镜：一镜一个术语｜动作大幅时运镜静止｜运镜句前置｜中等幅度速度省略
降级：硬阻断 7 项 → 改分镜｜高危 → §8.3 换动作｜楼梯/车辆见 §8.4
返工：⓪ 生成前检查（零成本）→ ① 抬步数 4→6-8 → ② 保留强度 → ③ 换种子
      → ④ 才改词 → ⑤ 改镜头设计｜⚠️ 恐怖谷例外：先加眨眼，别急着抬步数
否定：可视元素一律改正向｜手部否定句零档位（§3.9）
```
