---
name: h3-refsheet-gen
description: 为海螺 H3 的 Ref2VA 全能参考制作「人物三视图 / 表情集 / 场景图 / 道具图」参考素材。含 image2 / 豆包 实操（均支持中文提示词）、3D 次世代动漫风格 token、图与描述串互为镜像原则、9 图分配策略、验收测试法。触发词：三视图、人物设定图、角色参考图、场景图、参考素材制作、H3参考图、image2、豆包、中文提示词、全能参考、次世代动漫风格、去头版三视图、九宫格场景板、九机位 contact sheet。
agent_created: true
---

# h3-refsheet-gen · H3 参考素材制作

> **本 skill 补的是整套体系缺失的一环**：角色卡与场景卡只规定了"要登记哪些字段"，
> 却没说**那些参考图本身从哪来**。而 H3 的一致性是靠图锁的——
> 移除视觉锚定后，角色一致性从 **7.99 崩到 0.55**（arXiv 2512.16954）。
>
> **没有参考图，锁定块描述串写得再精确也是空中楼阁。**

## 0. 三十秒速查

| 要什么 | 生成什么 | 关键要求 |
|---|---|---|
| **锁角色** | 三视图（正/侧/背）+ 表情集 + 局部特写 | 白底、平光、中性站姿、可辨识剪影 |
| **锁场景** | 空镜（**无人物**）+ 光位标注 | 光位方向写进场景卡；画面内无文字 |
| **锁道具** | 单物体特写，纯色底 | 一图一物，不要拼贴 |
| **定首帧** | 带环境的完成画面 | 与提示词的构图描述一致 |

**一句铁律**：参考图是**给模型读的技术文档**，不是给人欣赏的插画。
好不好看不重要，**能不能被稳定提取特征**才重要。

---

## 1. 先分清两种图，别做错方向

这是最容易混淆、也最容易白做的一步。

| | **参考图**（Ref2VA / 全能参考） | **首帧图**（I2VA / FL2VA） |
|---|---|---|
| **作用** | 锁特征：告诉模型"这个人长什么样" | 定构图：告诉模型"第一帧画面是什么" |
| **内容** | 白底三视图、表情集、道具特写 | **带环境的完成画面**，含人物、构图、光影 |
| **要不要背景** | **不要**，纯色或白底 | **必须要有** |
| **要不要人物** | 场景图**不要有人**；角色图只要一个人 | 有 |
| **H3 字段** | `reference_image`（≤9 张） | `first_frame` / `last_frame`（各 1 张） |
| **互斥** | ⚠️ **两类不可同时提交**（官方 API 硬约束） | 同左 |

> ⚠️ **API 硬约束**：`first_frame`/`last_frame` 与 `reference_*` **不可同时出现**。
> 你要么走「首尾帧定构图」，要么走「全能参考锁特征」，**二选一**。

**你用「全能参考」→ 走参考图路线 → 本节做白底三视图。**

**什么时候改用首帧路线**：当某个镜头的**构图**比**人物一致性**更关键时
（如开场大全景、复杂多人调度）。此时要出的是带环境的完成画面。

---

## 2. 图 ↔ 描述串：互为镜像原则（本体系特有）

> 这是通用绘画教程不会讲、但对 H3 至关重要的一条。

**模型同时收到两路信号：图像特征 + 文字描述。两者必须说同一件事。**

| 情形 | 后果 | 处置 |
|---|---|---|
| 图上有，描述串没写 | 模型可能不提取该特征（文字权重更高时） | **补进描述串** |
| 描述串写了，图上没有 | 模型凭空想象 → 身份漂移 | **改图，或删掉该描述** |
| 图上与描述串矛盾 | 收到冲突信号，两边都不稳 | **必须消除，二选一改** |

**验收动作**（每张参考图都要过一遍）：

```
把锁定块描述串逐句念出来，对照图上找：
  □ 每句描述在图上都能指出来 → 通过
  □ 图上每个显著特征都在描述串里 → 通过
  □ 有矛盾项 → 改图或改描述串，不能留
```

**为什么这条比"画得好看"重要**：描述串是**逐字复制**的（Verbatim Rule），
图是**每次生成都重新采样**的。两者不一致时，模型会在两套信号间摇摆，
表现就是"脸忽大忽小、发色忽深忽浅"这类**渐进式漂移**——最难排查的一种。

---

## 3. 人物三视图

### 3.1 为什么三视图难，以及怎么破

**难点**：一张图里多个视角，模型倾向于画出"三个相似的人"而不是"一个人的三个面"。

**四个必写要素**（缺一个就散）：

| 要素 | 写法 | 为什么 |
|---|---|---|
| **一致性声明** | `consistent` / `same character` **重复多次** | 最重要的 tag。不写就出三个人 |
| **布局指令** | `arranged left to right`、`clean spacing between each view` | 模型不懂制表规范，必须明确说 |
| **背景中性** | `plain white background`、`flat even lighting, no dramatic shadows` | 消除环境对特征提取的干扰 |
| **姿态中性** | `full body standing pose`、`relaxed stance`、`neutral expression` | 动态姿态会扭曲比例，让三个视角对不上 |

### 3.2 可直接复制的模板（3D 次世代动漫风）

**正面 + 45° + 侧面 三视图**：

```
masterpiece, best quality, character design turnaround sheet,
same character shown in three views arranged left to right,
front view, three-quarter view, side profile view,
1girl, 26 years old, oval face, round eyes, slightly upturned nose tip,
straight bangs above the eyebrows, shoulder-length dark brown hair with outward-flipped ends,
pale even skin, slim build, 165cm,
wearing a cream white knit cardigan over a light inner top, light grey lounge trousers,
consistent facial features and proportions across all three views,
consistent outfit detail and colour across all three views,
full body standing pose in each view, relaxed stance, arms at sides, neutral expression,
plain white background, flat even lighting, no dramatic shadows,
clean spacing between each view, character design reference sheet,
next-gen 3D anime rendering, thick painted CG texture, delicate material rendering,
soft volumetric light, cinematic depth of field, 8K, ultra detailed,
clear readable silhouette, limited palette of three colours
```

**负面**（SD 系有独立负向字段，可以用）：

```
different characters, inconsistent design, inconsistent proportions,
busy background, text, watermark, logo, signature,
extra limbs, extra fingers, bad anatomy, deformed hands,
plastic texture, 3d render look, excessive bloom, rainbow colouring,
multiple people, crowd
```

### 3.3 四个视角各自的验收点

| 视角 | 必须看得清什么 | 常见失败 |
|---|---|---|
| **正面** | 五官、发型轮廓、服装前襟、身高比例 | 两眼不对称、发际线错乱 |
| **45°（3/4）** | 鼻梁侧面、脸型厚度、肩线 | 最容易崩——五官会"转不过去" |
| **侧面** | 鼻梁与下巴的侧影、后脑勺发量、背部服装 | 侧脸与正脸不是同一个人 |
| **背面** | 发型背面结构、服装接缝、配饰位置 | 常被忽略，但**是真正的照妖镜** |

> **背面是一致性的终极测试**。如果背面的发型、服装接缝、配饰位置都对得上，
> 说明模型真的理解了这个角色的三维结构，而不是在画三张相似的正脸。

### 3.4 姿态控制（进阶，强烈建议）

纯文生图经常失败。用 **OpenPose / ControlNet** 强制三个视角的姿态：

```
做法：若你的生图平台支持 ControlNet / 垫图（如 ComfyUI 类工作流），
      画/找一张「三个站姿骨架」的 OpenPose 图（正面、45°、侧面），
      作为姿态控制输入，权重 0.8–1.0，
      提示词里再写一遍三个视角的描述。
```

**为什么有效**：文生图时模型要同时"想"姿态和内容，容易顾此失彼。
给了骨架，姿态这条归一，模型只需专注把**同一个人**填到三个位置。

### 3.5 表情集

**做法**：固定 seed、固定提示词，**只改情绪 token**。

```
共用前缀（不变）：
1girl, <角色四段锚定>, front view, head and shoulders portrait,
plain white background, flat even lighting, next-gen 3D anime rendering...

只改这一处：
  neutral expression
  / gentle smile, eyes slightly curved
  / brows drawn together, jaw tightened          ← 写肌肉变化，不写"angry"
  / eyes widened, lips slightly parted           ← 写"睁大"，不写"surprised"
  / lashes lowered, gaze dropped to the side
  / corners of the mouth pressed down, chin raised
```

⚠️ **与 `h3-expression-psych` 的口径一致**：情绪要写成**可见的肌肉变化**，
不写情绪名词（不写 `angry`，写 `brows drawn together`）。
参考图这么写，提示词也这么写，两边才对得上（互为镜像原则）。

### 3.6 表情集完整模板（6 格）

**做法**：提示词只改情绪短语，**其余一字不动**，seed 固定，批量出 6 张。

```
【共用前缀 — 六张完全一致，不要改】
masterpiece, best quality, character expression sheet,
1girl, 26 years old, oval face, round eyes, slightly upturned nose tip,
straight bangs above the eyebrows, shoulder-length dark brown hair with outward-flipped ends,
pale even skin, wearing a cream white knit cardigan,
head and shoulders portrait, front view, facing camera,
plain white background, flat even lighting, no dramatic shadows,
next-gen 3D anime rendering, thick painted CG texture, delicate material rendering,
cinematic depth of field, 8K, ultra detailed,
【只改这一处 ↓】

① neutral, lips closed, gaze level with camera
② eyes slightly narrowed, corners of the mouth lifted, cheeks raised
③ brows drawn together, jaw tightened, lips pressed flat
④ lashes lowered, gaze dropped to the lower right, mouth slightly open
⑤ eyes widened, brows raised, lips parted
⑥ brows raised at the inner ends, corners of the mouth pulled down, chin raised
```

**六格对应的情绪**（供你对照剧情选用）：

| 格 | 可见变化 | 对应情绪 |
|---|---|---|
| ① | 唇闭合，视线平视 | 中性/基线 |
| ② | 眼微眯、嘴角上提、颧骨抬起 | 愉悦 |
| ③ | 眉头内收、下颌收紧、唇压平 | 隐忍/压抑的怒 |
| ④ | 睫毛低垂、视线下移、唇微张 | 心虚/闪躲 |
| ⑤ | 眼睁大、眉上抬、唇分开 | 震惊 |
| ⑥ | 眉头内侧上抬、嘴角下压、下巴抬起 | 委屈/强撑 |

> ⚠️ **不要写情绪名词进提示词**（不写 `angry`/`sad`）。
> 情绪名词在不同模型里映射不一致，肌肉变化则是确定的几何描述。
> 这是 `h3-expression-psych` 的核心主张，参考图必须同口径。

**验收**：六张并排，**遮住下面半张脸，只凭眼睛能认出是同一个人吗**？
认不出就重出——说明五官在不同表情下发生了漂移。

---

### 3.7 人物三视图（去头版 · 9:16 竖向）——防面部混乱变体

> 与 §3.2 的「正/45°/侧 拼贴」互补。当你反复遇到
> **「三视图里三个脸不是同一张脸」「发色/五官在三个视角飘」**时，改用这版：
> 把**面部特写**单独放画面顶部，**三视图区域只画颈部以下的身体**（不露头），
> 从源头消除「三个头互相污染」的问题。

**结构**：上方约 1/3 为面部特写（正面 + 轻微 3/4 补充）；
下方约 1/2 为 0°正面 / 90°侧面 / 180°背面，仅颈部以下、不露头；底部仅角色名（中文）。

**⚠️ 取舍**：去头版的三视图区**看不到后脑勺发量**（被头部挡掉了）。
若「背面发型结构」对一致性很关键（见 §3.3 背面是照妖镜），
保留 §3.2 正/45°/侧 + 单独出一张背面图，不要用去头版。

**中文提示词（可直接复制）**：

```
3D动漫写实人物角色设计展示板，非真人、原创虚构角色，完整角色资产介绍图，竖向构图，统一角色比例与身份特征。上方为角色面部特写，展示清晰五官结构、眼睛细节、发丝层次、皮肤材质、面部妆容、唇妆、眼妆、眉形、睫毛和微妙表情；下方为角色全身三视图，依次展示0°正面、90°侧面、180°背面，仅展示颈部以下的完整身体，不展现头部与面部（防止面部细节混乱），站立姿态自然，双臂自然垂落，脚部完整可见，三视图比例一致，视线水平，无遮挡，无透视变形。角色设定：原创3D动漫写实人物，年轻成年人，气质高级、时尚、精致，面部具有动漫美型特征，同时保留真实人体结构和自然比例。发型为【发型描述】，发色为【发色】，瞳色为【瞳色】，肤色为【肤色】，面部妆容为【妆容描述】。服装为【服装风格】风，包含【服装清单，逗号分隔】，突出服装剪裁、层次结构、面料质感与穿搭逻辑。服装材质包括高级织物、皮革、金属配件、半透明材质和细致刺绣，呈现真实的物理反射、褶皱、磨损细节与高级定制服装质感。角色身材修长匀称，采用标准9头身成年角色比例，头部、颈部、肩宽、躯干、腰臀、手臂与腿部比例自然协调，腿部线条修长但符合真实人体骨骼与肌肉结构。角色身体完整置于画面内（三视图仅颈部以下、不绘制头部与面部），三视图整体比例缩小、完整入画，头顶、双手、脚部均不被裁切，画面四周留出充足留白，站姿端正自然，避免夸张身材比例、幼态比例或过度纤细的肢体表现。采用高级CG动漫材质，虚幻引擎5风格渲染，PBR物理材质，真实全局光照，柔和轮廓光，细腻皮肤散射，清晰毛发材质，精致眼球湿润反射，高质量布料纹理，金属与皮革反射准确，电影级灯光，干净中性背景，角色资产展示板构图，专业角色设计稿，游戏角色制作标准，超高细节，8K质感，锐利清晰，统一光照，统一色彩，正面、侧面、背面信息明确。画面布局：上方占画面约三分之一，为面部特写区域，展示正面面部与轻微三分之二角度补充视图；下方占画面约二分之一，为三张横向排列的身体视图（仅颈部以下，不展现头部与面部，防止面部细节混乱），三视图整体适当缩小、完整入画，从左至右明确标注0°正面、90°侧面、180°背面；底部仅展示角色名称（中文），简洁、规整、可读，不遮挡角色。画面固定为9:16竖向比例，高分辨率角色设计展示板，所有角色视图大小协调、边界整齐，画面留白充足。角色名称：【角色名】 角色身份：【身份描述】 年龄设定：成年角色 整体气质：【气质】 主色调：【主色】 辅助色：【辅色】 服装关键词：【服装关键词】 妆容关键词：【妆容关键词】 配饰关键词：【配饰关键词】 背景颜色：【背景色】 镜头与渲染：专业角色资产展示摄影，50mm镜头，正交式三视图辅助构图，电影级CG渲染，Unreal Engine 5风格，细节优先。底部仅保留角色名称中文标签，其余一律不展示中文或其他文字，保持画面简洁；标签使用简洁专业的无衬线字体，字距正常、对比度清晰、排版整齐，不遮挡角色主体。负面提示词：真人照片，真实人物，现实人物肖像，名人脸，已有IP角色，版权角色，儿童，未成年角色，低龄化身体比例，儿童比例，幼态比例，非9头身比例，夸张大头身比例，过度细长四肢，三视图不一致，脸型变化，发型变化，服装变化，颜色变化，正侧背角度错误，背面出现正脸，侧面出现双眼，身体缺失，头顶裁切，脚部裁切，手部裁切，画面边缘裁切，手指错误，三视图区域出现头部、面部、五官，多余头部，脖颈断裂，头部虚影，多余手指，多余肢体，肢体扭曲，关节错位，比例失衡，透视变形，姿势夸张，动作姿态，遮挡，重复人物，模糊，低清晰度，噪点，过度磨皮，塑料皮肤，廉价材质，错误布料褶皱，材质混乱，过度反光，曝光过度，阴影过重，背景杂乱，复杂场景，多余文字标签，多余中文文字，除角色名称外的其他文字，角色身份标签，服装标签，妆容标签，配色标签，文字乱码，中文乱码，英文乱码，伪文字，无意义文字，错别字，模糊文字，难以辨识的字体，重叠文字，变形文字，文字遮挡角色，错误中文标签，排版错乱，字符缺失，低分辨率文字，错误标签，水印，边框裁切，画面比例错误，非9:16画幅，横向构图，构图拥挤，画面分裂，风格不统一。
```

**英文 image 版（给生图模型的精简版，可选）**：

```
3D anime realistic character design sheet, original fictional character, vertical 9:16 layout. Top third: detailed facial close-up (eyes, hair strands, skin, makeup). Bottom two-thirds: full-body turnaround of 【角色英文描述】— 0° front, 90° side, 180° back, showing ONLY the body below the neck, NO head or face in the three-view area (to avoid facial confusion). Natural standing pose, arms relaxed, feet fully visible, consistent proportions across views, no perspective distortion. 【服装英文清单】. Standard 9-head adult proportion, slim and tall, complete body in frame, hands and feet not cropped. High-end CG materials, Unreal Engine 5 render, PBR physical materials, realistic global illumination, soft rim light, subtle skin scattering, detailed fabric texture, cinematic lighting, clean neutral background (【背景色英文】), character asset board. Bottom shows the character name in Chinese ONLY, no other text or labels, clean and minimal. Negative prompt: photoreal photo, real person, celebrity face, existing IP, child, underage, chibi proportions, distorted limbs, extra fingers, inconsistent three views, head/face appearing in the three-view area, extra head, broken neck, head ghost, wrong perspective, text garbled, watermark, non-9:16, busy background.
```

**快速填表清单（替换占位符用）**：

| 字段 | 示例（以女主蒋筱筱为例） |
|---|---|
| 角色名 | 蒋筱筱 |
| 身份 | 救了顾时安一命的女主，清纯钢琴生 |
| 发型/发色 | 微卷栗色长发，披肩 / 栗色 |
| 瞳色/肤色 | 琥珀棕 / 暖白 |
| 妆容 | 淡妆素净：浅粉唇、几乎无眼影 |
| 服装清单 | 浅蓝色针织开衫＋白色吊带、白色及膝连衣裙、浅色平底单鞋、无配饰 |
| 气质 | 清纯、温柔 |
| 主色/辅色 | 浅蓝 / 白 |
| 背景色 | 米白 |

**常见翻车规避**：

1. **不露头是硬约束**：三视图区域负面词必须含「三视图区域出现头部、面部、五官 / 多余头部 / 脖颈断裂 / 头部虚影」。
2. **比例一致性**：三视图须同一角色比例，正面/侧面/背面信息明确，防止角度错乱。
3. **完整入画**：头顶、双手、脚部不得被裁切，四周留白充足。
4. **方向锁定**：若角色有固定光向（如全片光向恒右→左），在提示词补一句「Light from the right」保持一致，防镜像翻车。

---

## 4. 3D 次世代动漫风格（你指定的画风）

### 4.1 风格 token 库

| 类别 | 英文 token | 中文释义 |
|---|---|---|
| **质感** | `next-gen 3D anime rendering`、`thick painted CG texture`、`delicate material rendering`、`visible brush strokes` | 次世代 3D 动漫渲染、厚涂 CG 质感、细腻材质塑造、可见笔触 |
| **光影** | `soft volumetric light`、`cinematic depth of field`、`ray tracing`、`rim lighting`、`dappled sunlight` | 柔和体积光、电影级景深、光追、边缘光、斑驳日光 |
| **画质** | `8K`、`ultra detailed`、`high contrast shadow`、`colorful` | — |
| **剪影** | `clear readable silhouette`、`limited palette of three colours` | 可辨识剪影、三色限制 |

**对标参考**：《原神》《永劫无间》一类**厚涂 CG + 次世代渲染**的美术风格。
（注意：这是**风格描述**，不是要你生成具体 IP 角色——直接写 IP 角色名涉及版权风险。）

### 4.2 ⚠️ 「塑料感」三件套（本画风最常见的翻车）

| 症状 | 原因 | 加什么 |
|---|---|---|
| 过度光滑，像塑料娃娃 | 高光过曝 + 假景深叠加 | 负向加 `plastic texture`、`3d render look`、`excessive bloom`；正向加 `hand-painted feel`、`visible brush strokes` |
| 配色花，没有主色 | 颜色超过三种 | `limited palette of three colours`、`no rainbow coloring` |
| 剪影认不出职业 | 配饰堆太满挡住轮廓 | `no cluttered accessories blocking silhouette` |

### 4.3 三轮微调法（一次跑十张挑三张）

```
第一轮：查剪影 —— 把图缩小到看不清细节，还能认出这个角色的身份/职业吗？
        不能 → inpaint 重画配饰
第二轮：查配色 —— 局部颜色是否超过三色？
        超了 → 压到三色以内
第三轮：查塑料感 —— 有没有过度光滑的局部？
        有 → inpaint 重画，加 hand-painted feel
```

> **出片率预期**：原画感出片率本来就不高，**跑十张挑三张**是常态。
> 死磕一张反复改，不如批量跑再筛。

### 4.4 题材变体（在次世代 3D 动漫基础上换装换景）

| 题材 | 追加 token | 换掉什么 |
|---|---|---|
| **现代都市** | `modern urban setting`、`contemporary fashion`、`city backdrop` | 服装用现实款，场景用公寓/街道/办公室 |
| **古风仙侠** | `ancient chinese costume`、`flowing hanfu layers`、`ink-wash distant mountains`、`oriental classical features` | 服装换汉服，场景换宫殿/山水/竹林 |
| **未来科幻** | `sci-fi setting`、`metallic surfaces`、`holographic light`、`neon accents`、`techwear` | 材质加金属与全息，场景换舱内/都市废墟 |
| **校园青春** | `school uniform`、`daylight classroom`、`soft pastel grading`、`youthful features` | 服装换校服，色调偏柔和 |
| **暗黑奇幻** | `dark fantasy`、`chiaroscuro`、`gothic architecture`、`desaturated palette with deep reds` | 光比拉大，色调压暗 |

**统一保留的底色 token**（不随题材变）：
```
next-gen 3D anime rendering, thick painted CG texture, delicate material rendering,
soft volumetric light, cinematic depth of field, 8K, ultra detailed,
clear readable silhouette, limited palette of three colours
```

> **为什么底子不变**：题材变了但渲染底子不变，全剧画风才统一。
> 换题材只换服装与场景 token，**渲染 token 一个字都不改**。

---

## 5. 场景图

### 5.1 场景图与角色图的关键差异

| | 角色三视图 | 场景图 |
|---|---|---|
| 人物 | 一个人，站中间 | **绝对不要有人** |
| 背景 | 纯白 | 这就是主体 |
| 光位 | 平光无影 | **明确单一主光，方向要记下来** |
| 用途 | 锁角色特征 | 锁场景特征 + 提供「色彩锚点」 |

### 5.2 为什么场景图必须「无人」

两条理由：

1. **作为参考图时，人物会污染特征提取**——模型可能把场景里那个路人当成角色
2. **作为色彩锚点时，需要纯粹的光位信息**——有人的话，主体注意力被抢走

```
场景图提示词必须写：
  empty room, no people, no characters, no figures
```

### 5.3 场景空镜模板（室内）

```
masterpiece, best quality, environment concept art, wide shot,
modern urban apartment living room at night, empty room, no people,
a light grey fabric sofa on the left, an open kitchen island on the right,
a low wooden coffee table in the centre,
single warm ceiling light from the upper front right, warm colour temperature,
soft shadows falling to the lower left,
background kept simple and uncluttered, all surfaces that could carry
lettering are plain and unmarked, showing only colour, material and reflection,
next-gen 3D anime rendering, thick painted CG texture, cinematic depth of field,
soft volumetric light, 8K, ultra detailed, clear spatial layering
```

**负面**：

```
people, person, figure, character, crowd, silhouette of a person,
text, letters, numbers, logo, watermark, signage,
cluttered, messy, distorted perspective, warped architecture
```

### 5.4 ⚠️ 光位必须标注（这是场景卡的核心字段）

**每张场景图出图后，立刻在场景卡里记录**：

```
主光源方向：画面右前上方
色温：暖 3200K
阴影方向：落向左下方
```

**为什么必须记**：这是 §匹配剪辑「**色彩锚点**」的唯一取值来源。
上下两段要衔接，光源方向就不能变。图出了不记，后面写提示词时只能凭记忆猜，
猜错就是光照漂移——而光照一变，脸就跟着晃（光照是一致性的一半功力）。

**验证技巧**：把图拿远看，问自己"光从哪边来"。答不上来就说明这张图光照混乱，
**重出**——光照混乱的图当参考图，会把混乱带进视频。

### 5.5 室外场景追加要素

| 要素 | 必写内容 |
|---|---|
| 时间 | `at night` / `golden hour` / `overcast midday` |
| 大气 | `light fog` / `clear air` / `rain-slicked ground` |
| 次级运动 | `leaves moving in the wind`、`dust drifting through the light beam` |
| 天际线 | `distant city skyline`、`open sky` |

> **次级运动必须命名**：不写，模型就给你一张静态照片。
> 虽然在参考图里它不动，但命名过的特征更容易被 H3 提取时保留。

---

### 5.6 场景库（可直接复制，10 类）

> 每类都按「无人 + 单一主光 + 无文字」三原则写好，替换方括号内容即可。

**① 现代公寓客厅（夜）**
```
environment concept art, wide shot, modern apartment living room at night,
empty room, no people, a light grey fabric sofa on the left of frame,
a low wooden coffee table in the centre, an open kitchen island on the right,
single warm ceiling light from the upper front right, soft shadows falling to the lower left,
all surfaces that could carry lettering are plain and unmarked,
next-gen 3D anime rendering, thick painted CG texture, soft volumetric light,
cinematic depth of field, 8K, ultra detailed
```

**② 豪门餐厅（日）**
```
environment concept art, wide shot, grand mansion dining room in daylight,
empty room, no people, a long dark wood dining table running across the frame,
a crystal pendant lamp above the table, tall windows on the left,
single key light from the large window at the front left, neutral colour temperature,
warm pendant glow as a secondary accent, all surfaces plain and unmarked,
next-gen 3D anime rendering, thick painted CG texture, 8K, ultra detailed
```

**③ 豪门厨房（日）**
```
environment concept art, medium wide shot, large mansion kitchen in daylight,
empty room, no people, a deep stone sink beneath a wide window,
dark wood cabinetry, a marble island in the centre, a single orange on the counter,
single key light from the large window at the front left,
all surfaces that could carry lettering are plain and unmarked,
next-gen 3D anime rendering, thick painted CG texture, 8K, ultra detailed
```

**④ 车内（夜）**
```
environment concept art, interior view, car cabin at night, empty, no people,
dark leather interior, dashboard glowing with cool blue light at the front of frame,
windscreen showing moving city light streaks outside,
single cool key light from the dashboard, deep shadows in the rear,
next-gen 3D anime rendering, thick painted CG texture, 8K, ultra detailed
```

**⑤ 卧室（夜）**
```
environment concept art, wide shot, bedroom at night, empty room, no people,
a bed with light grey bedding on the right, a bedside lamp glowing warm on the left,
a curtained window at the back, single warm key light from the bedside lamp on the left,
all surfaces plain and unmarked, next-gen 3D anime rendering,
thick painted CG texture, soft volumetric light, 8K, ultra detailed
```

**⑥ 办公室 / 会议室（日）**
```
environment concept art, wide shot, modern office meeting room in daylight,
empty room, no people, a long white conference table, grey fabric chairs,
floor-to-ceiling windows on the right, single neutral key light from the windows at the right,
all surfaces that could carry lettering are plain and unmarked,
next-gen 3D anime rendering, thick painted CG texture, 8K, ultra detailed
```

**⑦ 城市街道（夜·雨后）**
```
environment concept art, wide shot, city street at night after rain,
empty street, no people, wet asphalt reflecting neon, closed shopfronts on both sides,
a single cool street lamp at the upper left, distant warm window glow,
light fog at ground level, all signage blank and unmarked,
next-gen 3D anime rendering, thick painted CG texture, cinematic depth of field, 8K
```

**⑧ 海边（日·高对比）**
```
environment concept art, wide establishing shot, coastline in bright daylight,
empty beach, no people, pale sand, clear turquoise water, distant rock formations,
strong overhead sunlight, bright reflection off the water, high contrast,
next-gen 3D anime rendering, thick painted CG texture, 8K, ultra detailed
```

**⑨ 雨夜街道（近景）**
```
environment concept art, medium shot, rain-slicked alley at night,
empty alley, no people, wet brick walls, a single warm lamp above a door on the right,
rain falling in visible streaks, puddles reflecting the lamp light,
no signage, no readable text, next-gen 3D anime rendering,
thick painted CG texture, cinematic depth of field, 8K
```

**⑩ 医院 / 病房（日）**
```
environment concept art, wide shot, hospital room in daylight, empty room, no people,
a single bed with white bedding, a bedside cabinet, a window with sheer curtains on the left,
single soft key light from the window at the left, cool white colour temperature,
all surfaces plain and unmarked, next-gen 3D anime rendering,
thick painted CG texture, 8K, ultra detailed
```

> **统一负面**：
> `people, person, figure, character, crowd, silhouette of a person, text, letters,
> numbers, logo, watermark, signage, cluttered, messy, distorted perspective, warped architecture`

---

### 5.7 场景九宫格（3×3 同一空间多机位）——高效锁空间一致性

> 与 §5.6 的「单张空镜」互补。九宫格是**同一物理空间、同一套建筑/家具/光线**，
> 由摄影机移动到 9 个位置拍出的 contact sheet。**一次生成拿 9 个空间锚点**，
> 且因为同源生成，9 张之间的空间关系天然一致——这是它最大的价值。
>
> **代价**：每格分辨率低，只作「空间关系锚点」；细节与精确光位仍靠 §5.6 单张场景图补。
> **需要输入**：先有一张 §5.6 的单场景图作为参考，再令模型「以这张为唯一空间依据」生成九宫格。
> **H3 额度账**：九宫格算 **1 张参考图**，却给出 9 个机位锚点，是 9 图预算里的性价比之王。

**一、场景基础设定**

- 场景类型：【客厅 / 办公室 / 教室 / 餐厅 / 商店 / 医院 / 街道 / 工厂等】
- 空间风格：【现代现实主义 / 中式 / 日式 / 工业风 / 科幻 / 古典等】
- 主要材质：【墙面材质】、【地面材质】、【家具材质】、【核心装饰材质】

**核心空间锚点**（必须严格保持位置关系）：A 区域 / B 区域 / C 区域 / 左侧（固定物）/ 右侧（固定物）/ 前方 / 后方 / 中央（主要家具）。
> 所有家具、门窗、墙体、柱体、楼梯、柜体、设备、灯具和主要装饰物的位置与参考图完全一致。
> **摄影机可以移动，环境不允许改变。**

**二、九宫格机位**

| # | 机位 | 高度/角度 | 焦段 |
|---|---|---|---|
| ① | 全局高位俯视（空间地图） | 45°—65° 向下 | 24mm |
| ② | 正面广角主视角（入口/正面） | 约 1.5m | 24—28mm |
| ③ | 左前方 45° | — | 28mm |
| ④ | 右前方 45°（补右侧关系） | — | 28mm |
| ⑤ | 核心电影主机位（人眼高度） | 1.4—1.6m | 28—35mm |
| ⑥ | 反打（⑤ 的对面，验证同空间） | — | 35mm |
| ⑦ | 场景内部向外（前景门框/桌角作参照） | — | 28mm |
| ⑧ | 侧面横向空间（看排列距离） | — | 35mm |
| ⑨ | 低机位/特殊高度（儿童/坐姿视线） | 0.8—1m | 35mm |

**三、统一摄影条件**（九张必须一致）：时间、天气、主光方向、色温；灯具开启状态、太阳方向、阴影方向、窗外天气、道具状态全部一致。

**四、一致性强化词（直接复制进提示词）**：

```
same exact environment, same exact architecture, same floor plan, same room geometry, same spatial topology,
same doors, same windows, same walls, same columns, same ceiling, same flooring,
identical furniture placement, identical furniture dimensions, same props, same decorations, same materials, same lighting fixtures,
camera moves only, environment does not change,
nine cameras photographing one physical location,
physically consistent 3D environment, architecturally coherent, accurate scale, accurate depth, realistic perspective,
spatial continuity, production design continuity, film set continuity, reverse-angle consistency, 180-degree camera continuity,
same time of day, same lighting direction, same weather, same color temperature.
```

**五、画面风格**：

```
cinematic realistic environment, photorealistic, realistic architectural photography, cinematic production design, 35mm film look, natural perspective, realistic material texture, physically correct lighting, natural shadows, high detail, realistic proportions, professional film location scouting photography
```

要求像影视剧正式勘景用的 **Scene Reference Board / Environment Bible / Location Contact Sheet**——不是室内设计效果图。

**六、九宫格输出要求**：

```
3×3 contact sheet, nine different camera views of exactly the same environment,
统一画幅, 统一色彩, 统一曝光, 细窄分隔线, 不要文字, 不要编号, 不要人物, 不要水印
```

**七、负面提示词**：

```
different rooms, different locations, different architecture, redesigned environment, random furniture changes, moving furniture, different doors, different windows, new windows, missing windows, extra doors, missing walls, changing wall positions, changing room size, different floor plan, different ceiling, different flooring, different decorations,
random props, duplicate furniture, floating objects, warped furniture, warped walls, curved architecture, impossible geometry, incorrect perspective, AI architecture errors,
fisheye, extreme wide angle distortion, exaggerated perspective,
different lighting, different time, different weather, different sunlight direction,
豪宅化, 场景随机扩建, 空间比例变化, 家具位置随机变化, 门窗随机增加, 不同装修风格, 九张独立设计图, 样板间效果图
```

> **最重要要求**：九宫格必须像摄影师带着同一台摄影机，在一个真实存在的场景里连续移动九次拍摄。
> `Camera moves only. Environment does not change.`

---

## 6. 道具图

**原则**：一图一物，纯色底，多角度可选。

```
masterpiece, best quality, item reference sheet,
a single matte gold signet ring, plain light grey background,
front view and three-quarter view arranged left to right,
flat even lighting, product photography style,
next-gen 3D anime rendering, delicate material rendering, 8K, ultra detailed
```

**负面**：`multiple objects`、`person`、`hand`、`text`、`logo`、`watermark`

> ⚠️ **不要画上手**。手部是 AI 最高危区域，画上去大概率崩，
> 崩了的手会污染整张参考图。要表达"戴在手上"，交给 H3 生成时处理。

---

### 6.1 高风险资产图专章（耳环 / 手表 / 伤疤 / 纹身）

按 `h3-character-asset` §9 的风险排序，**小面积身体标记与随身小物件复现成功率最低**。
它们是"纯文本 ≈ 放弃"的资产——**必须给单独的参考图**。

| 资产 | 参考图怎么拍 | 关键 |
|---|---|---|
| **耳环** | 单只耳环特写 + 一张「戴在耳垂上」的侧脸局部 | 必须能看清**戴在哪只耳朵** |
| **手表** | 手表平放特写 + 一张「戴在手腕上，表盘朝向明确」的局部 | 表盘朝向要固定（朝掌心/朝外） |
| **伤疤** | 位置特写（如手背、脸颊），**纯色底、平光、无阴影遮挡** | 尺寸与颜色要能准确辨认 |
| **纹身** | 单独平铺特写（图案本身）+ 一张「在身体某部位」的局部 | 图案复杂会被简化，尽量设计简单 |
| **戒指** | 平放特写 + 「戴在某根手指」的手部局部 | ⚠️ 手部局部**必须检查手指数量** |

**统一的拍法四要素**：

```
① 纯色底（浅灰最佳，不与肤色混淆）
② 平光，无强阴影
③ 一图一物，不拼贴
④ 给出尺寸参照（旁边放手/硬币等常见物，让模型理解比例）
```

**⚠️ 唯一例外：手不入图**

> 上面说「戴在手腕上」需要手，但这与 §11 的「崩手会污染参考图」冲突。
>
> **处置顺序**：
> 1. 优先用**不带手**的方式表达位置（如耳环用侧脸局部，不画手）
> 2. 必须带手时，**逐张检查手指数量与形态**，崩了就重出
> 3. 实在出不来干净的手 → **只给物件平放图**，位置交给提示词描述

### 6.2 先有图，后写卡：反推描述串

有时流程是反的——先出了一张满意的图，再补角色卡。**顺序反过来容易出错**。

**反推四步**：

```
1. 逐项「读图」：把图上能看清的特征全部列出来
   脸型 / 发型发色 / 瞳色 / 肤色 / 五官 / 体型 / 服装 / 配饰 / 随身道具

2. 逐项「翻译成词」：每个特征写成 2–4 个英文 token
   例：圆眼、过眉齐刘海、发尾外翘 → round eyes, straight bangs above the eyebrows,
       shoulder-length dark brown hair with outward-flipped ends

3. 组成四段锚定：发色发型 / 瞳色 / 服装款式 / 配饰（每段独立短语，不写成长句）

4. 反向校验：把描述串盖住，只看图，再念一遍描述串，看有没有多写或漏写
```

**反推时最常见的错误**：

| 错误 | 后果 | 正确做法 |
|---|---|---|
| 把图上的**光影效果**当成角色特征写进描述串 | 换场景后特征对不上 | 只写**固有属性**（发色、瞳色），不写光照造成的颜色变化 |
| 把**一次性姿态**当成特征 | 后续镜头被姿态锁死 | 只写静态属性，姿态留给分镜 |
| 图上有但懒得写 | 该特征不被提取 | 图上有的**全部**写进描述串 |
| 图上没有但想加 | 凭空想象 → 漂移 | 补图，或删掉该描述 |

---

## 7. 9 张参考图怎么分配（H3 特有）

H3 上限：**9 图 + 3 视频 + 3 音频 ≤ 12 文件**，单图 ≤ 30MB，
宽高 [256, 5760]px，宽高比 [0.4, 2.5]。

### 7.1 单人场景（推荐分配）

| # | 内容 | 锁定什么 |
|---|---|---|
| 1 | 角色三视图（正/45°/侧，**拼在一张**） | 脸型、发型、体型、服装 |
| 2 | 角色背面图 | 背面结构（一致性照妖镜） |
| 3 | 表情集（4–6 个） | 表情基线 |
| 4 | 局部特写：脸 + 眼 | 五官精度 |
| 5 | 局部特写：随身资产（耳环/手表/伤疤） | 高风险小物件 |
| 6 | 场景空镜（主场景） | 环境 + 光位 |
| 7 | 场景空镜（第二场景） | 环境 + 光位 |
| 8 | 关键道具 | 道具特征 |
| 9 | 画风参考（调色/质感样板） | 风格锁定 |

### 7.2 双人场景（如需要锁两个相似角色）

| # | 内容 | 说明 |
|---|---|---|
| 1–4 | 角色 A：三视图 / 背面 / 表情 / 局部 | |
| 5–8 | 角色 B：同上 | |
| 9 | 场景空镜 | ⚠️ **双人时场景只剩 1 张** |

**相似角色（如兄弟/双胞胎）的特别处理**：

> 两个相似角色**不要放在同一张图里**生成——模型会把他们画成同一个人。
> 分开各出一套三视图，让差异在**独立生成**中被强化。
> 差异做在发色、服装色系、表情基线（见 §8）。

### 7.3 拼贴 vs 分图

| 方式 | 优点 | 缺点 | 适用 |
|---|---|---|---|
| **拼贴**（三视图一张） | 省额度；模型能看到三个视角的关系 | 单视角分辨率低 | 9 图不够用时 |
| **分图**（每个视角一张） | 单视角精度高 | 占 3 个额度 | 主角，一致性要求极高 |

**建议**：**主角分图，配角拼贴**。

---

## 8. 相似角色的差异化（本体系实战难点）

当剧情要求两个角色"长得像"时（如认错人、兄弟），**剧情要求像、技术要求可辨**。

**差异必须做在非五官维度**——五官保持相似满足剧情，其他维度拉开供模型区分：

| 维度 | 权重 | 做法 |
|---|---|---|
| **发色** | **最高** | 一人纯黑、一人深棕带栗。大面积、高对比、最稳 |
| 服装色系 | 高 | 一冷（深灰/黑/炭蓝）一暖（暖米/杏/浅驼） |
| 表情基线 | 中 | 一人面无表情、一人常带笑 |
| 身形 | 中 | 身高、肩宽、体态拉开 |
| 随身道具 | 中 | 给其中一人一个稳定的可见道具 |

**验收（结对校验）**：

```
把两张参考图并排，遮掉名字，问自己：
  □ 能一眼认出谁是谁吗？
  □ 认不出 → 加大发色与服装色系的对比，不要靠提示词硬扛
```

⚠️ **这个测试在量产前必须做**。两个人各自测 20 次，统计互换率，
互换率 >10% 就加大差异。详见 `h3-character-asset` §12。

---

## 9. 生图工具实操（image2 / 豆包）

### 9.1 工具与提示词语言

本体系的参考图用 **image2** 与 **豆包** 生成。两个平台都**支持中文提示词**，
所以提示词可直接用中文写——本 skill 的 §3.7（去头版三视图）、§5.7（场景九宫格）
已经是完整中文版；其余英文 token 版保留作国际模型通用参考，效果等价。

> **中文优先原则**：既然你的工具支持中文，优先用中文写提示词。
> 中文描述「发色/瞳色/服装/材质」比英文 token 更不易歧义，也更好和角色卡字段对齐
> （角色卡本来就是中文填的，图与描述串互为镜像，语言统一更不容易出错）。

⚠️ **平台参数不写死**：image2 / 豆包 的具体生成参数（步数、采样器、高清修复方式）
以各自界面为准，本体系未逐一实测，不写固定数值。**唯一要守住的是「参数锁」**——
选定一组参数后全剧不换，改一处即全量重测（见 `h3-character-asset` §11）。

### 9.2 出图规格与参数

**H3 对参考图的硬约束（必须落地，与工具无关）**：

- 单图 ≤ **30MB**
- 宽高 **[256, 5760]px**
- 宽高比 **[0.4, 2.5]**

常见可用比例：角色竖版 768×1024（0.75）、场景横版 1216×832（1.46）均 ✅。
出图后确认落在上述区间内，否则 H3 拒收。

**生成参数（平台界面为准）**：image2 / 豆包 的步数、采样器、高清修复强度在各平台界面设置，
本体系未做实测，不写死具体数值。固定一组你自己的参数后**全剧不换**即可——
这是「参数锁」（`h3-character-asset` §11）三锁之一，改一处即全量重测。

### 9.3 模型/LoRA 选择原则（不给硬推荐）

> **我不推荐具体模型名**——模型迭代快，且我未做你的画风实测，
> 给"某某最好"是不负责任的。给**选择方法**：

```
1. 先定风格模型：在平台模型库搜「3D」「厚涂」「二次元」类底模/风格，
   看样图是否符合你要的「次世代厚涂 CG」质感
2. 再叠风格 LoRA（若平台支持）：权重 0.6–0.8，看是否更接近目标
3. 固定组合：选定后记进你的资产表，全剧不换
4. 验证：用同一组参数生成同一角色 10 次，看能否稳定复现
```

**关键不是选到"最好"的模型，而是选定后就不再换。**
参数锁是一致性三锁之一（见 `h3-character-asset` §11）——
改一处即全量重测。

### 9.4 角色 LoRA 训练（若平台支持，是固定角色的终局方案）

当某个角色要贯穿几十集时，训练专属 LoRA 是**最稳**的方案
（前提：你的生图平台提供角色 LoRA / 垫图微调能力）：

```
素材要求：
  □ 10–30 张
  □ 多角度（正/侧/背/45°）
  □ 服装一致（或明确分版本）
  □ 光照一致，背景干净
  □ 清晰度高、无水印、无文字
训练参数（参考）：15–20 轮
```

⚠️ **素材质量 >> 素材数量**。30 张风格混乱的图，不如 12 张风格统一的图。

### 9.5 常见翻车与修复表

| 症状 | 根因 | 修复 |
|---|---|---|
| **三个视角像三个人** | 缺一致性声明 | 提示词里 `consistent` / `same character` **重复 3 次以上**，每个特征后都跟一句 |
| 三个视角重叠或乱排 | 缺布局指令 | 补 `arranged left to right`、`clean spacing between each view` |
| 一个站立一个动起来 | 缺姿态指令 | 补 `full body standing pose in each view`、`relaxed stance` |
| **发色在不同图里深浅不一** | 服装/发色描述不够具体 | 用「材质 + 色相 + 明度」三词锁定，如 `jet black`、`chestnut-tinted dark brown` |
| 侧面像另一个人 | 侧脸特征没写 | 补 `side profile, nose bridge and chin clearly defined` |
| 背面发型崩 | 背面未单独描述 | 单独出一张背面图，或补 `back view, hair structure visible from behind` |
| **出图带文字/水印** | 底模自带或 LoRA 带 | 负面加 `text, watermark, logo, signature`；仍不行就换底模 |
| 高清修复后变脸 | 重绘强度太高 | 降到 **0.25–0.35**；超过 0.5 会改脸 |
| 画面过于光滑像塑料 | 高光过曝 | 负向加 `plastic texture, 3d render look, excessive bloom`；正向加 `hand-painted feel` |
| 参考图里冒出第二个人 | 负面词不够 | 负向加 `multiple people, crowd, two girls, duplicate` |
| 手崩了 | 手部入镜 | **裁掉手或重出**；参考图崩手会污染后续生成 |
| 场景图里有人影 | 未明确排除 | 正向写 `empty room, no people`，负向写 `person, figure, silhouette of a person` |

---

## 10. 参考图在 H3 提示词里怎么引用

做完图，还要在提示词里引用它。这里与 `h3-character-asset` §10 衔接。

### 10.1 四个标签的语义分工（官方 `ref-en.txt`）

| 标签 | 用途 | 例子 |
|---|---|---|
| `<Subject N>` | 从素材抽象出的**可复用可见内容**（人、物、画风） | 定妆图、角色三视图 |
| `<Picture N>` | 用作**具体目标帧或分镜锚点**的图 | 首帧、分镜参考 |
| `<Video N>` | 参考视频 | 运镜/剪辑节奏 |
| `<Audio N>` | 参考音频 | 音色、BGM |

> ⚠️ **存在第二条官方口径**：MiniMax 开源公告的 API 脚本用 `<image_1>/<video_1>/<audio_1>`。
> **本体系采用 `ref-en.txt` 这套**（出自官方提示词写作专用指南）。
> **同一份提示词内不可混用。**
> 冲突详情与实测方法见 `H3单镜提示词模板_Ref2VA参考模式版.md` 文首。

### 10.2 分配示例

```
subject_definitions:
<Subject 1> is the 26-year-old woman in <Picture 1>, with straight bangs,
shoulder-length dark brown hair, round eyes, wearing a cream white knit cardigan.
<Subject 2> is the empty apartment interior shown in <Picture 6>, including the
grey sofa, the kitchen island, and the warm ceiling light from the upper front right.
<Picture 5> is a close-up reference for the silver hoop earring on her left earlobe.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - ...
<Subject 2> ([Shot 1] background): partially_preserved - ...
<Picture 5> (asset reference): fully_preserved - ...
```

**保留强度怎么选**：

| 标记 | 何时用 |
|---|---|
| `fully_preserved` | 脸、发型、核心服装、关键道具——**必用** |
| `partially_preserved` | 允许随情境微调的（如背景细节） |
| `attribute_transfer` | 只迁移风格/材质/色彩（画风参考图） |
| `weak_reference` | 氛围板，只作倾向 |

### 10.3 图文配比的经验规律

| 情况 | 图上有的 | 文字要写 |
|---|---|---|
| 大面积、高对比特征（发色、服装色） | ✅ 图上已明确 | **仍要写**——冗余但更稳 |
| 小物件（耳环、戒指） | ✅ 单独特写图 | **仍要写** + 接触阴影句 |
| 图上没有但剧情需要 | ❌ | 写，但**预期会漂移**，优先补图 |

> **关键习惯**：**用文字复述参考图里已有的身份细节**。
> 冗余，但比只给图或只写文字稳定得多。

### 10.4 完整示例：带参考图的 Ref2VA 六段式

> 这是「参考图 → 提示词」的完整闭环，可直接改内容复用。
> 假设已备好：`<Picture 1>` 角色三视图、`<Picture 2>` 背面图、`<Picture 3>` 资产特写、`<Picture 4>` 场景空镜。

```text
subject_definitions:
<Picture 1> is the character design turnaround sheet for the 26-year-old woman,
showing her from the front, three-quarter and side views against a plain white background.
<Subject 1> is the woman in <Picture 1>: oval face, round eyes, slightly upturned nose tip,
straight bangs above the eyebrows, shoulder-length dark brown hair with outward-flipped ends,
pale even skin, slim build, wearing a cream white knit cardigan over a light inner top
and light grey lounge trousers.
<Picture 2> is the back view of <Subject 1>, showing the hair structure from behind
and the seams of the cardigan.
<Picture 3> is a close-up reference for the small silver hoop earring
worn on <Subject 1>'s left earlobe.
<Picture 4> is the empty apartment interior: a light grey fabric sofa on the left,
a low wooden coffee table in the centre, an open kitchen island on the right,
and a single warm ceiling light from the upper front right.
<Subject 2> is the empty apartment interior shown in <Picture 4>.

summary:
[reference generation] A 15-second three-shot sequence in which <Subject 1> sits in
<Subject 2> at night, receives a message on her phone, and looks up.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - her face shape,
hair colour and style, eye shape, and cardigan remain identical across all three shots.
<Picture 3> (asset reference): fully_preserved - the silver hoop earring stays on her
left earlobe, unchanged in size, shape and position.
<Subject 2> (appears in [Shot 1], [Shot 3]): partially_preserved - the furniture layout
and the warm key light from the upper front right are retained; background detail may vary.

detailed_description:
[Shot 1] Next-generation 3D anime rendering. A medium shot frames <Subject 1> seated on
the sofa in the lower-left third of frame, body angled three-quarters to camera, both feet
on the floor, phone held in her right hand at chest height. A few loose strands of hair
shift in the still air, then she lowers her chin and looks down at the phone, then her
thumb moves once across the screen. She does not speak. The phone's cool white glow lights
the underside of her chin and jaw; the ceiling light casts a steady warm pool on the wall
beside her. The camera holds a static shot. Lighting matches <Picture 4> exactly.
By the end of the shot she is still looking down, phone still in her right hand.
Do not let the screen content become legible at any point in the shot.

[Shot 2] At 00:02.000, the camera cuts to a close-up of her hands and the phone, still in
the same cardigan. Her grip tightens slightly, then her right thumb stops moving, then both
hands lower a few centimetres into her lap. She does not speak. A thin rim of cool white
light escapes around the phone's edge; the knit fabric of the cardigan creases softly at
the wrist. The camera holds a static shot.
By the end of the shot the phone rests in her lap, both hands still holding it, fingers
held together. Do not let the number of fingers change at any point in the shot.

[Shot 3] At 00:13.000, the shot switches to a large close-up of her face, the sofa and
ceiling light still visible behind her. She blinks once, then slowly raises her chin, then
her gaze lifts to a fixed point beyond the lens and holds there. She does not speak.
Her hair falls back over her shoulder; the warm key light holds steady on her cheek.
The camera holds a static shot. Lighting matches <Picture 4> exactly.
By the end of the shot she is holding a steady gaze off-camera, expression unchanged.
Do not let the lighting direction shift at any point in the shot.

overall_soundscape: Quiet night-time living room tone, one soft screen-tap, knit fabric
shifting, one slow inhalation, a faint electrical hum from the ceiling light.

non_diegetic_music: Sparse low strings at a slow tempo, entering in shot 2 and fading out
over the final hold.
```

**这个示例里值得注意的几处**：

| 处 | 为什么这么写 |
|---|---|
| `<Subject 1>` 与 `<Picture 1>` 分开定义 | 图是素材，**Subject 是从图里抽象出来的可复用内容** |
| `Lighting matches <Picture 4> exactly` | **用参考图当光照锚点**——这是场景图最重要的用途 |
| 每镜收边都是 B 类 | `legible` / `number of fingers change` / `lighting direction shift`——都是"帧间不变"，非重复正向 |
| 描述串复述了图上的特征 | 互为镜像原则：图有、文也有，冗余但稳 |
| `<Picture 3>` 单独标 `fully_preserved` | 高风险小物件单独一张图 + 最强保留标记 |

---

## 11. 反面清单：什么图不能当 H3 参考图

| 类型 | 为什么不行 | 处置 |
|---|---|---|
| **带文字/水印/logo** | 模型会把文字当特征学习，导致画面内冒出乱码 | 重出或后期抹除 |
| **多人合影** | 模型不知道该锁谁 | 裁成单人，或分开出图 |
| **极端角度**（仰拍/俯拍/大透视） | 特征提取会带上透视畸变 | 改用平视标准角度 |
| **光照混乱**（多光源/强逆光/硬阴影） | 光照信息污染，脸会随光变 | 重出，用平光 |
| **背景杂乱** | 背景特征被一起学进去 | 抠图换纯色底 |
| **分辨率过低**（<256px 或糊） | 达不到特征提取精度 | 高清修复 |
| **画风与成片不一致** | 风格信号冲突 | 全剧统一画风参数 |
| **手部入镜且是崩的** | 崩手会被当成"正常手部特征"学进去 | **裁掉手，或重出** |

> ⚠️ 最后一条特别重要：**参考图里崩掉的手，会被模型当成正确的手去学**。
> 参考图只要出现手部，就必须逐张检查手指数量与形态。

---

## 12. 验收测试：怎么确认参考图能用

**不要直接拿去量产。先跑这个测试。**

### 12.1 角色图验收（≥10 次）

```
用同一组参考图 + 同一段提示词，生成 10 次，每次换种子。
逐条检查：
  □ 脸型/五官：10 次里几次是同一个人？
  □ 发色：有没有忽深忽浅？
  □ 服装：颜色、款式一致吗？
  □ 随身资产：耳环/手表在吗？左右换边了吗？
判定：
  ≥ 9/10 稳定 → 可用
  7–8/10     → 可出镜，但不得承载叙事信息
  < 7/10     → 重做参考图（通常是图的信息不够纯）
```

### 12.2 场景图验收

```
  □ 光照方向：10 次一致吗？
  □ 场景结构：家具/建筑位置稳定吗？
  □ 有没有冒出多余人影？
```

### 12.3 相似角色专项（必须做）

```
两个角色各生成 20 次，统计：
  □ 互换率（把 A 画成 B 或反之）
  □ 融合率（画成第三个人）
判定：
  互换/融合率 ≤ 10% → 可用
  > 10%            → 加大发色与服装色系对比，重出图
```

### 12.4 与描述串的镜像复核（回到 §2）

```
念一遍锁定块描述串，逐句在图上指认。
有一句指不出来 → 改图或改描述串。
```

---

## 13. 完整工作流（从角色卡到可用参考图）

```
1. 填角色卡                     → h3-character-asset §2
   └ 输出：四段锚定（发色发型 / 瞳色 / 服装款式 / 配饰）

2. 写三视图提示词               → 本 skill §3.2
   └ 四段锚定 + 一致性声明 + 布局 + 白底平光 + 中性姿态 + 风格 token

3. 批量生成                      → image2 / 豆包，一次跑 10 张
   └ 参数：以你平台界面为准（固定一组不换）；角色竖版约 768×1024，场景横版约 1216×832

4. 三轮微调筛选                  → 本 skill §4.3
   └ 剪影 → 配色 → 塑料感

5. 高清修复                      → 重绘强度 0.25–0.35（不要高，会改脸）

6. 反面清单过一遍                → 本 skill §11
   └ 重点：有没有文字、有没有崩手、光照是否纯净

7. 镜像复核                      → 本 skill §2
   └ 描述串 ↔ 图，逐句对照

8. 场景图重复 2–7 步             → 本 skill §5
   └ 出图后**立刻**把光位方向记进场景卡

9. 分配 9 图额度                 → 本 skill §7

10. 验收测试                     → 本 skill §12
    └ 角色 ≥10 次 / 相似角色各 20 次

11. 写进 Ref2VA 提示词            → h3-character-asset §10
    └ <Subject N> / <Picture N> + retention_analysis 标记

12. 锁定，全剧不再更换
```

### 13.1 批量生产：一部剧几十个角色怎么高效做

**分层投入**——不是每个角色都值得做全套：

| 层级 | 角色类型 | 参考图投入 | 说明 |
|---|---|---|---|
| **T0** | 男女主（贯穿全剧） | **全套**：三视图 + 背面 + 表情集 + 局部 + 资产图 | 值得训练 LoRA |
| **T1** | 重要配角（出现 ≥5 集） | 三视图 + 一张场景/服装图 | 拼贴一张，省额度 |
| **T2** | 功能配角（2–4 集） | 一张三视图拼贴 | 够用即可 |
| **T3** | 一次性角色 / 路人 | **不制作** | 提示词里写"虚化处理"，不锁 |

**判断标准**：这个角色**会不会被观众记住脸**？
会 → 至少 T1。不会 → 不投入，把额度留给主角。

### 13.2 参考图的版本管理

**什么时候该重出图**：

| 触发 | 处置 |
|---|---|
| 角色**换装**（进入新篇章/新场景） | 出新版本的服装图，**服装版本 ID 同步更新** |
| 角色有**状态变化**（受伤、变装、年龄变化） | 出对应状态的图，建新的资产 ID |
| 场景**换了**（从公寓搬到公司） | 出新场景图，**光位重新记录** |
| 原图发现有**崩手/文字/水印** | 立即重出，不要将就 |
| 验收测试**未达标** | 加大差异重出 |

**⚠️ 版本管理铁律**：

> **换了图，描述串必须同步改。**
> 图与描述串互为镜像（§2），改一边不改另一边 = 主动制造冲突信号。
>
> 用**变更日志**记录每次改动：
> ```
> | 日期 | 改了什么 | 同步改了什么 |
> |---|---|---|
> | 08-30 | CH_01 服装换为浅杏风衣 | 角色卡 OUT_A→OUT_B；三视图重出；锁定块服装串已改 |
> ```

### 13.3 画风统一性验证（多角色时必做）

不同角色分批出图，画风容易漂移。**全剧画风必须一致**：

```
验证方法：
把所有角色的参考图并排放在一起，检查：
  □ 渲染质感一致吗（厚涂笔触的粗细、材质表现）？
  □ 色彩饱和度一致吗？
  □ 光影对比度一致吗？
  □ 面部结构与比例是同一套审美吗？

不一致 → 回到同一个底模 + 同一组 LoRA 权重重出不达标的那几个
```

> **根因通常是参数不同**：不同批次用了不同底模、不同 LoRA 权重、不同 CFG。
> **固定参数组合，全剧不换**——这是「参数锁」（`h3-character-asset` §11）。

---

## 14. 与其他 skill 的分工

| skill | 管什么 |
|---|---|
| **`h3-refsheet-gen`（本 skill）** | **参考图怎么制作**（三视图/表情集/场景图/道具图）+ image2/豆包 实操（支持中文提示词）+ 验收测试 |
| `h3-character-asset` | 角色卡字段、资产锁定四要素、Ref2VA 提示词写法、一致性三锁 |
| `h3-env-scene` | 场景描述串写法、光影系统、色彩锚点 |
| `h3-expression-psych` | 表情写法（情绪→肌肉变化），参考图表情集要与它口径一致 |
| `h3-antibug-check` | 提示词漏洞检查、采样步数伪翻车 |

**上下游关系**：

```
h3-character-asset（定义角色字段）
        ↓
h3-refsheet-gen（把字段变成图）     ← 本 skill
        ↓
h3-character-asset §10（把图写进 Ref2VA 提示词）
        ↓
h3-antibug-check（检查）
```

---

## 15. 待验证清单

| # | 待验证项 | 实测方法 | 样本 |
|---|---|---|---|
| 1 | 三视图拼贴 vs 分图，哪个锁定更准 | 同一角色，两种各生成 10 次，比对一致性 | 20 |
| 2 | 背面图是否显著提升跨镜一致性 | 有/无背面图各 10 次 | 20 |
| 3 | 参考图带手部是否污染手部生成 | 有手/无手参考图各 10 次，数手指 | 20 |
| 4 | 场景图光位标注对色彩锚点的实际帮助 | 标注一致 vs 不一致各 10 次，比对光照漂移 | 20 |
| 5 | 相似角色发色差异的最小可辨阈值 | 逐步缩小发色差异，找失效点 | 30 |
| 6 | 3D 次世代风格 token 在不同底模上的稳定性 | 同提示词换 3 个底模各 10 次 | 30 |
| 7 | image2/豆包 参数（步数/采样器等）对特征提取的影响 | 固定角色，扫参数网格 | 30 |

---

## 16. 一句话速查

```
参考图是技术文档，不是插画。
三视图四要素：一致性声明 + 布局 + 白底平光 + 中性姿态。
背面图是照妖镜。
场景图必须无人，光位必须记进场景卡。
图与描述串互为镜像，矛盾项必改其一。
崩掉的手会污染参考图——手不入参考图。
相似角色：差异做在发色/服装色系，不做在五官。
出图后先测 10 次再量产。
```
