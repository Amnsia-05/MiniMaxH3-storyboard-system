> # ⚠️ 本文件已被取代，规格依据错误，请勿作为 H3 依据使用
>
> **问题**：本文件的核心硬约束取自 **Hailuo 2.3**（MiniMax 前代云端模型），**不是 MiniMax H3**。
> 两者差异极大，以下四条已被官方原文推翻：
>
> | 项 | 本文件写的（2.3） | **H3 实际** |
> |---|---|---|
> | 提示词上限 | 2,000 字符 | **7,000 字符** |
> | 音频 | 不生成 | **原生立体声，与画面同次推理生成** |
> | 首尾帧 | 仅首帧单图，无尾帧 | **FL2VA / L2VA 均支持** |
> | 参考素材 | 单图 | **9 图 + 3 视频 + 3 音频 ≤ 12 文件** |
>
> **连带失效的结论**：
> - ~~「口型/对白语种属硬阻断，只能后期 Wav2Lip」~~ → H3 原生出声带唇形同步，**语种串台反而是真实高频翻车项**
> - ~~「跨镜身份一致是模型硬限制，只能靠首帧单图」~~ → H3 有 omni-reference，一件资产锁一样
> - ~~「1200–2500 汉字必然丢指令」~~ → 那是 2.3 的甜点区；H3 官方提供带时间戳的多镜结构化字段
> - ~~「H3 不支持否定句」~~ → 证据冲突，另见官方证据说明
> - 文中「Hailuo 2.3 支持 6s / 10s」→ H3 为 **4–15 秒整数**（API）
>
> **现行版本见**：`防翻车限制词库_H3版.md` 与 `防翻车限制词库_补充勘误_H3专属.md`
> **官方原文依据见**：`MiniMax-H3-官方提示词规范调研报告.md`
>
> 本文件保留仅作**调研过程记录**，其中的翻车类型分类与部分规避写法（与模型版本无关的通用部分）仍有参考价值。
>
> ---

# AI 视频生成防翻车限制词库
### —— 面向「小说 → 15 秒 3 镜 → 海螺 H3 提示词」工业级模板

> 证据分级：【官】官方/权威文档 · 【业】业界多来源一致的实测经验 · 【推】机制推断，无实测数字 · ✗ **硬阻断**：提示词解决不了，必须靠参考图/后期/换工具。客户零容忍编造，凡无公开数据支撑处均已标注。

---

## 0. 前置结论：负向提示词在 H3 上是否有效

**结论：H3（按 Hailuo 2.3 系列）没有负向提示词字段，所有限制必须写成正向描述。**

- 【官】fal.ai 的 Kling V3 Pro vs Hailuo 2.3 Pro 参数对照表：Hailuo 2.3 Pro 的 `Negative prompt` 一栏为 **"Not available"**（Kling 为 Supported）。
- 【官】国内聚合 API 文档列出 Hailuo 2.3 不支持的参数：`negative_prompt`、`image_tail`（首尾帧）、`size`、`fps`、`aspect_ratio`。
- 【官】Hailuo 2.3 官方 API：提示词上限 **2,000 字符**；支持 15 个方括号运镜指令；**仅支持单张首帧，无尾帧**。

**关于"只写'不要六指'反而会激活该概念"——这个说法mechanism上不成立，但经验上常常是真的，且对 H3 无意义：**

- 在真正的 CFG 架构 + 独立负向字段下，负向词是"远离该向量"，**没有机制会让它把概念画出来**（【官】CFG 原理：负向提示是第三组条件，输出被拉离它）。
- 但实测中常见"越禁越出"：Kling 用户实测把 `cars` 写进负向栏，结果**车出现得更多**（【业】ageofllms）。业内解释是：模型只是把一种不想要的效果换成了另一种；且**过长的负向清单会稀释引导力**——"avoid 预算"被几十个模糊概念摊薄，真正要禁的那两个反而不生效（【业】ai-tldr）。
- 而 H3 根本没有负向字段，把"不要六指"写进主提示词时模型**必须先编码"六指"这个 token 才能理解否定**，注意力反而被导向它。

**因此本词库统一采用「正向替代」策略——只写"是什么"，不写"不是什么"。** 这也是跨模型最安全的写法（写"空无一人的街道"而不是"没有车"）。

### 全局硬阻断清单（提示词做不到，别承诺客户）

| 项 | 替代手段 |
|---|---|
| 可读文字（招牌/短信/字幕/表盘数字） | 干净底板 + 后期贴图 |
| 跨生成的左右方位一致 | 后期水平镜像翻转 |
| 跨生成的 180° 轴线 / 正反打朝向 | 同镜内完成，或后期镜像 |
| 拉远揭示镜（无尾帧时身体凭空生成） | 改剪辑：局部镜 → 硬切 → 全景镜 |
| 小物件纯文本复现（耳环/纹身） | 必须走 I2VA 参考图 |

---

## 1. 手部异常（六指/断指/融合/穿模）

**成因**：手部占画面像素极小，姿势组合极多，训练样本中大量被遮挡，交叉注意力难以把各部位映射到正确位置；视频还叠加跨帧指骨数量变化。

**规避写法（原理）**：① 提高像素占比（特写而非全身）；② 消灭手指分离需求（握拳、叠放、插兜、背手）；③ **消灭"精细持物"**——手与细长物体的接触是最难的一类；④ 用"无接触传递"替代"递交"（【业】Versely 实测：`hands her the cup` 的失败率显著高于 `slides the cup across the table toward her`，*"Contact-free transfers sidestep the hardest hand problem"*）。

**可直接复制的词句**
```
正面（优先用这些）：
Her hands hang naturally at her sides, fingers gently curled and held together, thumbs resting along the seams of her trousers.
He rests a closed fist on the table, fingers curled inward, knuckles visible.
Her hand lies flat against the fabric of her skirt, palm down, five fingers held together, natural finger proportions.
Both hands are tucked into her coat pockets; no fingers are visible.
He holds a large ceramic mug with both hands, fingers wrapped fully around the body of the mug.
Close-up from the wrist up, the hand fills more than half the frame, five fingers, natural proportions, clean edges.

兜底约束句（写在动作描述之后）：
five fingers on each hand, natural finger length and spacing, clean separation between fingers,
hands fully visible in frame, no objects passing between the fingers.

中文等价：
双手自然下垂贴于裤缝，手指自然弯曲并拢，拇指沿裤缝贴合。
右手握拳置于桌面，四指内收，指节清晰可见。
手掌平覆在裙摆布料上，掌心向下，五指并拢，手指比例自然。
双手插在外套口袋中，画面中不露出手指。
```
> 风险分级：握拳（中）＜ 捏衣角（高）＜ **签字/持笔/插钥匙（极高，建议直接改动作）**。

---

## 2. 肢体与人体结构（多余肢体/关节反折/人数增减）

**成因**：模型没有骨骼与关节自由度约束，只学了"看起来合理"的像素统计；人物数量在跨帧状态跟踪中极易漂移。

**规避写法**：① 用 `then` 串联动作，**禁用 `while`**（【业】Versely：`She sips while waving while walking` 会破坏 anatomy，`She picks up the cup, then takes a sip` 则干净）；② 每个动作给**明确终点**（有界动作）；③ 多人时**第一句就拉开外观差异**，且每人只给一个动作（*"two men in suits" 这种对称描述会诱导融合*）；④ 人数写死并前置。

```
Exactly ONE person in frame, a single subject, no additional figures anywhere in the shot.
She lowers the folder onto the desk, then straightens her back, then turns to face the window.
A tall man in a red apron (left of frame) and a short woman in a denim jacket (right of frame);
the man folds his arms, then the woman takes one step forward.
Both arms hang at his sides throughout; both shoulders remain level and square to camera;
his neck stays straight, no head tilt beyond a slight downward glance.
Slow, single, bounded movement; no rapid limb motion; no jumping, no spinning.

中文等价：
画面中严格只有一名人物，画面任何位置不出现第二个人形。
她把文件夹放到桌上，然后挺直后背，然后转向窗户。
画面左侧是一名穿红围裙的高个男子，右侧是一名穿牛仔外套的矮个女子；男子双臂交叉，随后女子向前迈一步。
全程双臂垂于体侧，双肩保持水平正对镜头，脖颈挺直。
```

---

## 3. 镜头不流畅 / 不连贯（跳切/速度突变/主体漂移/末帧抖动）

**成因**：每条独立生成，模型无跨生成记忆；叠加运镜时模型会"平均"多个指令，产生混乱漂移。

**规避写法**：① **一条镜只给一个运镜**（*"Stacking 'pan then zoom then tilt' is the fastest way to get a confused drift."*）；② **运镜句必须放提示词第一句**——Hailuo 对靠前 token 权重更高；③ 用官方方括号指令而非自然语言（【官】Hailuo 2.3 支持 `[Truck left/right] [Pan left/right] [Push in] [Pull out] [Pedestal up/down] [Tilt up/down] [Zoom in/out] [Shake] [Tracking shot] [Static shot]`，同一括号内最多 3 个＝同时执行，写在不同位置＝顺序执行）；④ **提示词超过约 100 词后开始丢指令，最先丢的就是运镜句**（【业】Versely）。

```
Locked-off camera on a tripod, one single continuous camera move at a constant speed from start to finish,
no acceleration, no deceleration, no direction reversal, no camera shake, no jitter, no stutter,
no frame flicker, stable exposure throughout.

[Truck right] — the camera moves continuously from left to right in one unbroken move,
maintaining the same speed and the same direction, never pausing and never reversing.

The camera settles and holds completely still for the final second,
ending on a stable held frame with no drift.

A single slow push-in at a constant rate, no zoom, no handheld wobble,
the subject stays centered in frame throughout.

中文等价：
三脚架固定机位，全程仅一次匀速运镜，无加减速、无方向反转、无抖动、无闪烁，曝光全程稳定。
[Truck right] 镜头自左向右连续横移，速度与方向始终不变，不中断不回头。
镜头在最后一秒完全停稳，结束于无漂移的稳定静止帧。
单次缓慢匀速推近，无变焦、无手持晃动，主体全程居中。
```
> 跨镜头方向对齐四规则：① 上下两段**必须用同一个 token**（都用 `[Truck right]`，不要一段 `pan right` 一段 `move rightward`）；② 方向句置首；③ 给两段一个共同物理参照物（"结束于深色墙面充满画面" → "从深色墙面继续向右进入"）；④ **左右一致属硬阻断，跨生成只能靠后期镜像。**

---

## 4. 身份漂移（脸/服装/发型/年龄变化）

**成因**：每个镜头是独立任务，模型没有长期记忆；文字描述天然不精确，模型每次重新"猜"。

**规避写法**：① **Verbatim Rule——角色描述串逐字复制、一字不改**（【业】Veo 3 实测：完整复述 vs 简化改写，一致性差异可达 40%）；② 描述串只写**可见且稳定**的特征，120 字左右；③ **首帧参考图是决定变量**：移除视觉锚定后一致性得分从 **7.99 崩到 0.55**（【官】arXiv 2512.16954）；④ 只锁 **1–2 个**不可变配饰，锁多了反而互相干扰（【业】Elser AI）；⑤ 光照方向**全程单一主光**，主光换边身份就会晃。

```
The same woman appears in every shot: 28 years old, shoulder-length straight black hair in a low ponytail,
dark brown eyes, straight nose, soft round chin. She wears an unbranded ivory cotton T-shirt and
dark-wash straight-leg jeans. Her appearance does not change at any point: same hair, same face,
same clothing, same age, same body type, from the first frame to the last.
A single soft key light from camera left throughout; no change in hair colour, no change of outfit,
no accessories added or removed.

中文等价：
同一名女性贯穿全部镜头：28 岁，齐肩黑色直发低马尾，深棕色眼睛，鼻梁挺直，下巴圆润，
身穿无标识的米白色纯棉 T 恤与深蓝色直筒牛仔裤。从第一帧到最后一帧，发型、五官、服装、
年龄、体型完全不变，不添加也不减少任何配饰。全程单一柔和主光，来自镜头左侧。
```

---

## 5. 语言与文字错误（乱码招牌/字幕/短信/口型不同步）

**成因**：文字符号被当作像素图案处理，模型未学字符结构规则；数字顺序与字形尤其不可靠。

**规避写法（Clean-Plate Rule）**：**任何不能错的文字都不要在模型内生成。** 生成干净底板，文字在时间线上后期贴（【业】Versely）。理由不只是准确率——后期图层**逐帧像素完全一致**，而模型内的文字会漂移、会变字形。

```
干净底板（推荐，几乎万能）：
A plain unbranded shopfront with a blank signboard, no text, no letters, no numbers,
no logo, no watermark, no subtitles, no captions, no UI elements anywhere in frame.
A smartphone with a dark screen; the screen emits a soft cool-white glow onto her face. No visible text on the screen.

退而求其次（必须出字时，只满足这一个条件才可用）：
A single large word, flat and facing the camera directly, held for under three seconds,
on a still surface with a locked-off camera.

中文等价：
无任何品牌标识的店面，招牌空白，画面中不出现任何文字、字母、数字、标识、水印或字幕。
手机屏幕为暗屏，屏幕在她脸上投下柔和的冷白色光，屏幕上看不到任何文字。
（必须出字时）单个大号单词，正对镜头平铺，停留不足三秒，承载面静止且机位锁死。
```
> **口型与台词不同步**：Hailuo 2.3 不生成音频（【官】），口型无从对齐。属**硬阻断**——用 Wav2Lip 类工具在后期生成唇形，或干脆把对白段处理成画外音/背影/遮挡，回避口型。语种串台同理，AI 生成画面里不要出现任何可读文字，就不会串台。

---

## 6. 物理与空间违和（穿透/重力/液体/布料/左右翻转）

**成因**：结构性缺陷——模型学的是"物理的外观"不是"物理的逻辑"；ICML 2025（字节 Seed × 清华）结论：*"scaling alone is insufficient for video generation models to uncover fundamental physical laws"*（【官】Kang et al. 2025）。

**规避写法**：① **回避动态物理**，改拍静态结果（*"Person pouring water into glass"* 会浮空/分流/越界；改 *"a filled glass of water on the table, the bottle held nearby"*）；② 命名次级运动，否则模型只给你一个静态道具（*"Naming the secondary motion gets you secondary motion"*）；③ 复杂物理（水/布料/人群）不要用 Fast 档。

```
A filled glass of water stands on the table; the bottle rests beside it. No pouring.
Her coat whips in the wind, steam curls off the mug, the hem of her skirt sways with each step.
He sets the box down heavily onto the table; the table does not deform; the box stays rigid.
Two people stand two arm's lengths apart, and this distance stays constant for the whole shot.
The glass remains solid and rigid, its contents stay inside it, no object passes through another.

中文等价：
桌上放着一只已倒好水的玻璃杯，瓶子放在杯旁。全程不做倒水动作。
她的外套在风中翻飞，杯口热气袅袅上升，裙摆随步伐摆动。
他把纸箱重重放到桌上，桌面无形变，纸箱保持刚性。
两人相距约两臂之遥，该距离在全镜头内保持不变。
玻璃杯保持完整刚性，杯中液体始终在杯内，任何物体不发生相互穿透。
```
> 小尺度精细交互（钥匙插锁孔、手指点按拨号盘）与机械约束（车门从铰链侧开）**属硬阻断**——模型没有 3D 朝向跟踪与刚体约束（【业】Nano Banana 用户实测归纳的四类失效）。规避：**不要给小尺度交互点特写**。

---

## 7. 道具与资产丢失（耳环/手表/手机/眼镜忽有忽无、左右手互换）

**成因**：像素占比低 → 注意力不足；叠加视频模型"跨帧状态跟踪弱"（VGI-Bench 归纳的三大失效模式之一 Object/state inconsistency：物体会消失、变形或重置到早前状态）。【业】Morphic 的伪影综述明确记录："objects such as glasses or jewelry disappearing and reappearing between frames... tattoos or skin marks may vanish across frames"。

**规避写法**：① **绑定位置 + 绑定不变量**（"戴在左耳垂，全程不摘下"）；② 颜色/材质对比拉满；③ 减少头部/肢体大幅运动；④ **小物件是后期最容易补画的元素之一**（面积小、跟踪容易），生成失败就后期贴。

```
She wears a single small silver hoop earring on her LEFT earlobe; it remains on her left earlobe
for the entire shot, unchanged in size, shape and position, and is never removed or replaced.
He wears a silver wristwatch on his LEFT wrist, the watch face turned toward his palm;
the watch stays on the same wrist throughout, unchanged.
She holds the phone in her RIGHT hand and does not switch hands at any point.

中文等价：
她左耳垂佩戴一只银色小圆环耳环，该耳环在整个镜头中始终在左耳垂上，大小、形状、位置不变，
不会被摘下或替换。
他左腕佩戴银色手表，表盘朝掌心，手表全程在同一只手腕上，外观不变。
她用右手握持手机，全程不换手。
```

---

## 8. 多镜头生成特有问题（风格/光照不统一、节奏错位、起手动作重复）

**成因**：三次独立生成，无共享状态；提示词微改会导致风格漂移（Cause B/C：过多竞争性约束 + 没有 lock block）。

**规避写法**：① **Lock Block（锁定块）**——风格串、角色串、光位串做成模板常量，每镜原样复制粘贴，禁止临场改写；② 光位/色温写成一个固定句子，三镜共用；③ 后一镜的动作**起点必须区别于前一镜的起点**（前一镜结尾是"手已放下"，后一镜就从"转身"开始，避免重复起手）；④ 前一镜最后一帧截图作为后一镜首帧参考图。

```
[STYLE LOCK — copy verbatim into every shot]
Handheld-feeling but steady, 35mm lens, shallow depth of field, muted teal-and-amber grade,
natural skin texture, no stylisation, no filter, consistent colour temperature, consistent contrast.
[LIGHT LOCK] A single soft key light from camera left at 45°, cool ambient fill, no practical lamps in frame.
[SHOT 3 STARTS FROM A NEW POSE] She is already standing with her back to the door; she begins by
turning her head slightly — this shot does not repeat the reaching motion from the previous shot.

中文等价：
［风格锁——每镜逐字复制］手持感但稳定，35mm 镜头，浅景深，青绿与琥珀色调，自然皮肤质感，
无风格化、无滤镜，色温与反差全程一致。
［光位锁］单一柔和主光位于镜头左侧 45°，冷色环境补光，画面内无光源灯具。
［第 3 镜从新姿态起手］她已背对门站立，以微微转头开始；本镜不重复上一镜的伸手动作。
```

---

## 9. 【重点】手机屏幕内容处理

**成因**：屏幕内容是"小面积 + 高密度文字 + 高频变化"三者叠加，是全部翻车类型的**交集**，因此是风险最高的一类。

**业界通用做法：不要生成屏幕内容，生成"屏幕的光"，内容后期合成。** 这条能把它从"高风险"直接降到"低风险"。

| 方案 | 风险 | 适用 |
|---|---|---|
| A. 屏幕背对镜头（只拍手机背面/侧边） | **低** | 只需表达"他在看手机" |
| B. 暗屏 + 冷白光映脸 | **低** | 需要观众知道"他在看消息"，但不需要看清内容 |
| C. 首帧用真实截图（I2VA），镜头只做微动 | **中** | 必须看到内容，且可以接受极短时长 |
| D. 后期屏幕替换（跟踪+角点+调色匹配） | **低**（但要工时） | 交付级要求 |
| E. 直接生成可读短信 | **高，不采用** | — |

```
方案 A（最稳）：
He holds his phone with the BACK of the phone facing the camera; only the matte black back panel
and his fingers are visible. A thin rim of cool white light escapes around the phone's edge.
方案 B（推荐默认）：
She looks down at her phone. The screen is not visible to camera; only its cool white glow
lights the underside of her face and her chin from below. No text visible anywhere.
方案 C（必须用真实内容时）：
Using the uploaded screenshot as the starting frame: keep every word, icon and colour exactly
as shown; the camera performs one slow push-in only; no new elements, no redesigned layout,
no distorted text, no duplicated cards, no melting geometry, no random text.

中文等价：
A：他以手机背面朝向镜头握持，只见哑光黑色背板与手指，手机边缘漏出一圈冷白色光。
B：她低头看手机，镜头看不到屏幕，只有屏幕的冷白光从下方照亮她的下巴与脸的下半部，
画面任意位置不出现文字。
C：以上传的截图为起始帧：保持每一个字、图标与颜色与截图完全一致；镜头只做一次缓慢推近；
不得新增元素、不得重排布局、不得出现字形扭曲、重复卡片、融化变形或随机文字。
```

---

## 10. 【重点】小物件（耳环/手表/戒指/手机壳）一致性锁定

**核心判断**：决定成败的**不是物件类别，而是三个变量**——① 是否有参考图 ② 是否在运动中 ③ 同时锁了几个。

**【官】硬证据**：移除视觉锚定后一致性得分 **7.99 → 0.55**（arXiv 2512.16954）。即：**纯文本描述小物件 ≈ 放弃**，必须走 I2VA 参考图。

**【业】业界对策一致**：*"We favor simple silhouettes, solid colors, and notable but minimal anchors (a red jacket, a silver pendant)"*（CrePal）——大面积、纯色、少量锚点。Elser AI 明确要求 **one or two immutable accessories**，并给出约束写法 *"do not remove the red hairpin"*。

**写法模板（四要素：颜色 + 材质 + 固定位置 + 不变量声明）**
```
[ASSET LOCK — paste verbatim] A small matte-gold signet ring on her RIGHT ring finger
(worn on the right hand, not the left). The ring stays on the same finger for the entire shot,
unchanged in size, colour and shape; it is never removed, never duplicated, never changes hand.
[LIMIT] Lock exactly two signature accessories per character. Do not add any others.

中文等价：
［资产锁——逐字粘贴］她右手无名指佩戴一枚哑光金色印章戒指（戴在右手，非左手）。
该戒指在整个镜头中始终在同一根手指上，大小、颜色、形状不变，不会被摘下、不会重复出现、
不会换手。
［限制］每个角色最多锁定两件标志性配饰，不得再增加。
```

**风险排序（【推】，含机制解释）**：
**义肢（最高·建议禁用或仅静态中远景）＞ 纹身（高）＞ 耳环/戒指（中高）＞ 手表/手机（中）＞ 大面积衣物/围巾（低）**

> 义肢必须单列最高档：它不只是"小物件"，会改变**肢体轮廓与关节结构**，易被渲染成正常肢体或与身体融合，属"肢体结构崩坏"而非"物件丢失"。
>
> ⚠️ **没有公开的量化基准**。我未找到任何来源给出"耳环复现成功率 = X%"。网上"某模型珠宝保真度优异"类说法均出自聚合站/营销软文，无方法论、无测试集，**判定为不可引用**。建议自建测试（≥20 次，且必须在真实运动条件下测，静止画面测出的成功率无意义），并登记业界现成指标 **Prop Persistence Rate (PPR) / Wardrobe Lock Rate (WLR)**，目标 ≥80%（storytool.io）。

---

## 11. 【重点】长提示词的组织方法

### ⚠️ 必须先纠正一个前提

**1200–2500 汉字的单镜提示词，在海螺 2.3 上大概率会丢指令，不建议使用。**

- 【业】Versely 实测：Hailuo 2.3 最佳区间 **40–70 词**（英文）；**低于 25 词**模型自行脑补细节；**超过 100 词开始丢指令，最先丢运镜句，然后丢动作的后半段**。
- 【官】Hailuo 2.3 提示词上限 2,000 字符（能写进去 ≠ 会被执行）。
- 【业】注意力分布规律：**开头与结尾权重高，中段被弱化**；80–150 词时已开始出现优先级分化，150 词以上出现明显折损（getvidzy）。

### 正确解法：不是"把 2000 字组织好"，而是"把静态信息从提示词里搬走，交给参考图"

**静态信息（角色外观、服装、场景、画风、光位、小物件）→ 全部进参考图 + 资产库的固定描述串，用 I2VA 承载。提示词里只留三样：动作、运镜、约束。** 这样单镜提示词自然落到 40–70 词区间，且参考图还顺带解决了身份漂移与小物件丢失（第 4、7、10 节）。

### 若确需长提示词：分层 + 前后同述

**优先级排序（严格按此顺序写）**
```
第 1 层（最前，权重最高）：运镜 + 景别        → [Truck right] / Medium close-up
第 2 层：主体 + 人数（写死）                  → Exactly one woman, 28, ...
第 3 层：动作（用 then 串联，给终点）          → She ..., then ..., then ...
第 4 层：环境 + 光位（一个主光，一个方向）      → A single soft key light from camera left
第 5 层：约束句（每条一行，动宾结构）          → five fingers / the ring stays on the same finger
第 6 层（最后，权重次高）：复述第 1 层与第 5 层的关键项
```
**防"信息埋没"三条**：① 关键约束**绝不放在中段**；② **尾部再复述一次**最重要的 1–2 条（首尾双写，利用首尾权重高的特性）；③ 每条约束**独立成句、动宾结构**，不要塞进长定语从句里被稀释。

**中英文混排的取舍**：Hailuo 系对中文自然语言理解良好，但**官方显式运镜指令（`[Truck right]` 等 15 个）只有英文形式**且官方明确"显式指令比自然语言更准"。建议：**运镜与关键约束用英文方括号/短句，其余用中文**，不要把中文长句再翻译一遍（重复描述等于增加竞争性约束）。

---

## 附：通用限制词串（H3 无负向字段，以下均为正向句，按需挑 3–5 条，不要全贴）

```
Exactly one person in frame; no additional figures, no crowd, no background people.
Five fingers on each hand, natural finger proportions, clean separation between fingers.
The subject's face, hair, clothing and accessories remain identical from the first frame to the last.
A single continuous camera move at constant speed; no shake, no jitter, no stutter, no flicker.
Stable exposure and consistent colour temperature throughout; lighting direction never changes.
No text, no letters, no numbers, no logos, no watermarks, no subtitles anywhere in frame.
No object passes through another; rigid objects stay rigid; liquids stay inside their containers.
Single subject, uncluttered background, minimal environment, soft bokeh, clean edges.
```

> **使用纪律**：挑 3–5 条与当前镜头强相关的即可。**堆满清单会稀释引导力**——这与负向清单越写越长反而失效是同一个道理（【业】ai-tldr）。

---

## 主要来源

- fal.ai — Kling V3 Pro vs Hailuo 2.3 Pro 参数对照（Negative prompt / Start-end image / Multi-shot 均 Not available）
- MiniMax Hailuo 2.3 官方 API 文档（2,000 字符上限、15 个方括号运镜指令、仅单张首帧）
- Versely — Hailuo 2.3 Prompting Guide（40–70 词区间、早 token 优先、`then` vs `while`、无接触传递）
- Versely — On-screen text in generated video（Clean-Plate Rule）
- Scenario / APIXO / 极客智坊 — Hailuo 2.3 能力边界（无尾帧、无负向字段）
- Kang et al., ICML 2025（字节 Seed × 清华）— *How Far is Video Generation from World Model: A Physical Law Perspective*
- VGI-Bench（arXiv 2608.19583）— 视频生成三大失效模式
- arXiv 2512.16954 — 视觉锚定消融：7.99 → 0.55
- CrePal / Elser AI / storytool.io — 角色一致性与资产锁定实践、PPR/WLR 指标
- Morphic 伪影综述（经 humantext.pro 验证）— 珠宝/眼镜/纹身跨帧消失
- ageofllms Kling Prompt Guide — 负向提示词实测失效记录
- is4.ai — AI 视频 2025 年八大局限（手部、物理、时序）
