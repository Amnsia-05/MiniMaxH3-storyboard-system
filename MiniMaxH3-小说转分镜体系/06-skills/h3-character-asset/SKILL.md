---
name: h3-character-asset
description: 海螺 H3 视频提示词中「人物分层 / 外貌 / 皮肤 / 伤口 / 服装 / 人物资产锁定」的写法，解决跨镜跨集人物一致性漂移。含角色卡模板、资产锁定四要素、Ref2VA 保留强度标记。触发词：H3角色一致性、H3人物描写、H3资产锁定、H3服装、H3伤口、H3耳环手表、角色卡、H3身份漂移。
agent_created: true
---

# MiniMax H3 · 人物与资产一致性提示词写法

> 面向「长篇小说 → 15 秒 3 镜 → 海螺 H3 提示词」工业化流水线。
> 本文只解决一件事：**让同一个人在第 1 集和第 60 集长得一样，让同一件耳环在第 3 镜还在左耳垂上。**

---

## 0. 边界、证据约定与硬约束

### 0.1 本 skill 管什么 / 不管什么

| 本 skill 管 | 不管（交给其他 skill） |
|---|---|
| 人物分层、外貌、皮肤、伤口、服装 | 动作 / 表情 / 运镜 / 分镜切分 |
| 随身资产（耳环 / 戒指 / 手表 / 义肢 / 纹身）锁定 | 场景环境、光位、色温、画风串 |
| 角色卡、资产表、服装版本 ID | 对白、音色、`(S1)` 编号、声音三字段 |
| Ref2VA 中**人物与资产**相关的参考图分配与保留强度 | — |

### 0.2 证据分级（全文通用，与主模板一致）
| 标记 | 含义 | 使用原则 |
|---|---|---|
| 【官方】 | MiniMax H3 官方仓库 skill 原文 / 官方 API 文档 / 官方模型卡 | 可当硬规范 |
| 【业界】 | 公开论文或通行工艺（不限 H3） | 可用，但别当 H3 专属基准 |
| 【推断】 | 机制推断，无大规模实测 | 小样本校准后再量产 |
| 【待验证】 | 必须自己跑实测 | 本文给出测试方法 |
| 【工程取值】 | 流水线人为设定的常数 | 用你的实测值覆盖 |

> **零编造纪律**：本文**不给任何"某物件复现成功率 = X%"的数字**——这类数据没有公开基准（§12.1）。凡查不到出处的，一律标注【待验证】并给出实测方法。
### 0.3 H3 硬约束（只列与人物/资产相关的部分）【官方】

| 约束 | 值 | 对本文的影响 |
|---|---|---|
| 提示词上限 | **7000 字符**（按字符计，1 汉字 = 1 字符） | 角色串 + 资产串要做预算，见 §9.9 |
| 单次时长 | **4–15 秒整数**（API）；本地 5–15 秒 | 15 秒 3 镜在单请求内，是资产锁定的最大红利 |
| 帧率 | 24 FPS | 15 秒 = 360 帧，误差逐帧累积 |
| 参考素材 | 图 ≤9、视频 ≤3、音频 ≤3，**混合 ≤12 文件**，请求体 ≤64 MB | 9 图怎么分配见 §10.5 |
| **图生视频与全能参考互斥** | `first_frame`/`last_frame` 与 `reference_*` **不可同时出现** | **人物锁定方案的二选一，见 §10.1** |
| 三核心字段 | `integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`（顺序固定） | Ref2VA 下主字段换为 `detailed_description`，见 §10.3 |
| 时间戳 | 第一镜不加，后续 `At 00:SS.mmm`（三位小数） | 见 §10.3 |
| 对白 | 必须 `<d>...</d>` | 人物描述放标签**外** |
| 运镜 | 一镜一个 | 与资产无关，但会挤占提示词预算 |

### 0.4 一条总原则

**一致性 = 参考图锁 × 描述串锁 × 参数锁**，三者是乘法关系，任何一项为 0，结果就是 0（详见 §11）。

---

## 1. 人物一致性为什么难

### 1.1 三个根因

| 根因 | 机制 | 后果 |
|---|---|---|
| **无长期记忆** | 每次请求是一次独立推理，模型不保留上一次的状态 | 第 2 集不认识第 1 集的主角 |
| **每次生成都是重新采样** | 同一段描述串，两次采样落在潜在空间的不同位置 | 同一条提示词，两次出片脸就不同 |
| **误差逐帧累积** | 24 FPS × 15s = **360 帧**；每帧的微小偏差不被回拉，只会单向漂移 | 耳环可能第 5 秒消失、第 9 秒长回右耳 |

### 1.2 三个放大项

1. **改描述串**——同义替换、临场润色、删一个形容词，都可能让采样落点整体偏移。
2. **换光位**——主光从右边换到左边，脸部明暗结构变了，观感上就是"换了个人"。
3. **切镜**——每一次切镜等于重新采样一次，3 镜 = 3 次漂移机会。

### 1.3 两条可用的量化参照（**以及它们不能怎么用**）

| 参照 | 数字 | 出处与性质 | **不能怎么用** |
|---|---|---|---|
| 视觉锚定消融 | 移除视觉锚定后角色一致性得分 **7.99 → 0.55** | 【业界·单篇论文】arXiv 2512.16954，该论文自定指标下的得分 | ❌ 不能外推为"H3 的耳环保真度 = X%"；❌ 不能当作通用基准；✅ 只能说明量级与方向——**没有视觉锚定时，纯文本描述小物件约等于放弃** |
| Verbatim Rule | 完整复述 vs 简化改写，一致性差异**可达 40%** | 【工艺】实践者实测归纳，测试集与方法未公开 | ❌ 不是受控实验基准；✅ 只能说明"逐字复用"这件事的量级足够大，**值得为它放弃临场润色** |

> ⚠️ 这两条都**不是**"复现成功率"，也都不是 H3 专属。任何"某模型珠宝保真度优异"类说法都来自聚合站或营销软文，无方法论、无测试集，**不可引用**。

### 1.4 由根因推出的四条对策

| 对策 | 对应根因 | 落在本文 |
|---|---|---|
| 把身份**外置**到参考图，不靠描述写长 | 无长期记忆 + 重新采样 | §10 |
| 描述串做成**模板常量**，逐字复用 | 改描述串 | §3.4、§11.2 |
| 光位、色温**全剧单一**，记进场景表 | 换光位 | §11.3 |
| 3 镜放进**同一次请求**，共享上下文 | 切镜 | §10.1 |

---

## 2. 角色卡模板

角色卡是整条流水线的一致性地基。**不做这一步，第 3 集的主角会长得跟第 1 集不一样，返工量以集数为指数增长。**

### 2.1 完整字段清单（12 组）

| # | 字段组 | 必填 | 说明 |
|---|---|---|---|
| 1 | 基础信息 | ✅ | 年龄（**具体数字**）、性别、身份、与其他角色关系 |
| 2 | 外观逐项写死 | ✅ | 脸型 / 发型发色 / 瞳色 / 肤色 / 五官 / 体型 / 标志性表情 / 稳定皮肤标记 |
| 3 | 固定穿搭 + **服装版本 ID** | ✅ | 换装即换 ID，见 §8 |
| 4 | 随身资产清单 | ✅ | 逐件登记，含四要素锁定串，见 §9 |
| 5 | 身体标记与伤口 | 按需 | 痣 / 胎记 / 疤 / 义肢，见 §6、§7 |
| 6 | 行为锚点 | ✅ | 专属小动作、口头禅、称呼习惯 |
| 7 | 声音 | ✅ | `voice_id`、语速 V、情绪基线、（S1）编号 |
| 8 | 画风串 | ✅ | 全剧逐字复用，禁止临场改写 |
| 9 | 参考图集 | ✅ | 9 图分配表，见 §10.5 |
| 10 | **提示词常量串** | ✅ | 英文 identity string，80–150 字，token 级不变 |
| 11 | 光照约定 | ✅ | 主光方向与色温（与场景表对齐） |
| 12 | **变更日志** | ✅ | 每次改动记一行，见 §11.5 |

### 2.2 空白模板（可直接复制）
```markdown
## CH__ 《角色名 / 代称》

### 基础
- 年龄（写数字）：　　性别：　　身份：
- 与其他角色关系：

### 外观（逐项写死，禁止"英俊""漂亮"这类抽象词）
- 脸型：　　发型 / 发色：　　瞳色：　　肤色 / 肤质：
- 五官特征（**必须有一项可辨识的独有特征**）：
- 体型：　　标志性表情：
- 稳定皮肤标记（痣 / 雀斑 / 胎记；没有就写"无"）：
- 伤口 / 身体标记（含义肢 / 纹身；没有就写"无"）：

### 固定穿搭
- 上装：　　下装：　　鞋：　　外套：
- **服装版本 ID**：CH___OUT___
- 服装不变量声明（见 §8.4）：

### 随身资产（每角色 ≤2 件标志性配饰，见 §9.5）
| 资产ID | 名称 | 四要素锁定串（固定不变） | 出现集段 | 参考图ID | 风险等级 |
|---|---|---|---|---|---|

### 行为锚点
- 专属小动作（推眼镜 / 捏衣角 / 抿唇）：
- 口头禅 / 称呼习惯：

### 画风
- 统一画风标签串（**逐字复用**）：

### 声音
- voice_id：　　语速 V：　　情绪基线：　　说话人 ID：(S__)

### 光照约定
- 主光方向：　　色温：　　是否允许画内出现灯具：

### 参考图集（9 图分配，见 §10.5）
| 槽位 | 内容 | 保留强度 |
|---|---|---|

### 提示词常量串（英文，token 级不变，直接复制）
> （80–150 字英文，见 §3）

### 变更日志
| 日期 | 改了什么 | 影响集段 | 是否全量重测 |
|---|---|---|---|
```

### 2.3 填好的范例 · 主角 CH_01

> 本范例与主模板模块六 §6.3「共用锁定块」**完全对齐**，可直接与主模板配套使用。

```markdown
## CH_01 《沈昭》— 主角

### 基础
- 年龄：28　　性别：女　　身份：私人律师事务所调查员
- 关系：与 CH_02 陆行舟为对手关系（表面合作）

### 外观（逐项写死）
- 脸型：鹅蛋脸
- 发型 / 发色：齐肩黑色直发，发尾微内扣，中分，无刘海
- 瞳色：深棕色
- 肤色 / 肤质：偏白，自然皮肤质感，可见毛孔，无磨皮
- 五官：深色眉毛，杏仁形眼睛，鼻梁挺直，唇形偏薄，下巴圆润
- **独有特征**：右眉尾一道 1.5cm 浅白色旧疤（见 §7.5，版本 SCAR_A）
- 体型：165cm 左右，偏瘦，肩线窄
- 标志性表情：抿唇 + 下巴微收（思考时）
- 稳定皮肤标记：左侧锁骨上方一颗直径约 2mm 深褐色痣
- 伤口 / 身体标记：右眉尾旧疤 SCAR_A；无义肢、无纹身

### 固定穿搭
- 上装：米白色无标识圆领纯棉 T 恤
- 外套：深卡其色长款风衣（敞开穿，不系腰带）
- 下装：深蓝色直筒牛仔裤
- 鞋：白色低帮帆布鞋
- **服装版本 ID**：CH_01_OUT_A
- 服装不变量声明：整套服装在全剧维持同一配色、同一材质、同一件数；风衣全程保持敞开、腰带垂落两侧的状态。

### 随身资产（每角色最多 2 件，见 §9.5）
| 资产ID | 名称 | 四要素锁定串（英文，逐字复用） | 集段 | 图ID | 风险 |
|---|---|---|---|---|---|
| AS_07 | 银色小圆环耳环 | `a single small silver hoop earring on her LEFT earlobe, staying on that earlobe for the entire shot, unchanged in size, shape and position` | 全剧 | IMG_06 | 中高 |
| AS_08 | 哑光金色印章戒指 | `a small matte-gold signet ring on her RIGHT ring finger, staying on that same finger for the entire shot, unchanged in size, colour and shape` | 全剧 | IMG_06 | 中高 |

> 完整的四要素锁定串与接触阴影句见 §9.7，量产前按 §12 测 PPR。

### 行为锚点
- 专属小动作：思考时用拇指指腹反复摩挲戒指的戒面
- 口头禅 / 称呼习惯：称对方全名，不叫昵称；句尾极少用语气词

### 画风
- 实拍电影感，写实风格，35mm 镜头，浅景深，背景轻微虚化，青绿与琥珀色调，
  中等反差，自然皮肤质感，轻微胶片颗粒，无风格化滤镜，色温与反差在三镜内完全一致。

### 声音
- voice_id：VOX_SHEN_01　　语速 V：4.5　　情绪基线：克制、偏低　　说话人 ID：(S1)

### 光照约定
- 主光方向：画面右前方 45°（与 SC_01 客厅夜景一致）
- 色温：暖（约 3200K）　　画内灯具：允许出现一盏落地灯（唯一可见光源）

### 参考图集（9 图分配，Ref2VA 模式）
| 槽位 | 内容 | 保留强度 |
|---|---|---|
| IMG_01 | 正面定妆（脸 + 发型 + 妆容，含右眉疤） | `fully_preserved` |
| IMG_02 | 左侧 45° | `fully_preserved` |
| IMG_03 | 全身（体型 + CH_01_OUT_A + 鞋） | `fully_preserved` |
| IMG_04 | 锁骨痣特写 | `fully_preserved` |
| IMG_05 | 场景空镜（含落地灯光位） | `partially_preserved` |
| IMG_06 | 耳环 + 戒指特写（**同一张图内并置**） | `fully_preserved` |
| IMG_07 | 画风 / 调色参考 | `attribute_transfer` |
| IMG_08 | 手部姿态参考（五指并拢平放） | `attribute_transfer` |
| IMG_09 | 备用：情绪表情参考 | `weak_reference` |

### 提示词常量串（英文，token 级不变，直接复制）
The same woman appears in every shot: 28 years old, oval face, shoulder-length straight
black hair with slightly inward-curled ends, centre-parted, forehead fully visible, dark brown
almond-shaped eyes, dark eyebrows, a straight nose bridge, thin lips, a rounded chin, pale skin
with natural visible texture and visible pores, a 1.5cm pale healed scar at the outer end of her
right eyebrow, and a 2mm dark brown mole just above her left collarbone. She wears an unbranded
ivory round-neck cotton T-shirt, a dark khaki long trench coat worn open without the belt,
dark-wash straight-leg jeans and white low-top canvas shoes. A single small silver hoop earring
sits on her left earlobe and a small matte-gold signet ring sits on her right ring finger, both
staying in place for the entire shot. Her appearance remains identical throughout: same face,
same hair, same clothing, same age, same body type, same accessories, from the first frame to
the last.

### 变更日志
| 日期 | 改了什么 | 影响集段 | 是否全量重测 |
|---|---|---|---|
| — | 初版 | 全剧 | — |
```

### 2.4 填好的范例 · 配角 CH_02（**重点看差异是怎么拉开的**）

```markdown
## CH_02 《陆行舟》— 配角（对手）

### 基础
- 年龄：35　　性别：男　　身份：某集团法务总监

### 外观（与 CH_01 四维全拉开，见 §4.3）
- 脸型：方下颌，颧骨明显
- 发型 / 发色：黑色寸头（约 1cm），无分发
- 瞳色：深褐色（近黑）
- 肤色 / 肤质：偏深的小麦色，皮肤偏油光，鼻翼两侧毛孔明显
- 五官：浓直眉，细长眼，高鼻梁，薄唇，下颌线硬
- **独有特征**：右侧下颌角一道 4cm 斜向旧疤（SCAR_B）
- 体型：185cm 左右，宽肩，体格厚实
- 标志性表情：下颌微抬，说话时右侧嘴角先动

### 固定穿搭
- 上装：白色衬衫（第一颗扣敞开，不打领带）
- 外套：炭灰色羊毛大衣（**合穿，扣上**）
- 下装：黑色西裤　　鞋：黑色皮鞋
- **服装版本 ID**：CH_02_OUT_A
- 服装不变量声明：大衣全程保持扣合状态，从第一帧到最后一帧系扣不变；衬衫领口维持敞开一颗扣的状态。

### 随身资产（配角 1 件，见 §4.3）
| 资产ID | 名称 | 四要素锁定串 | 风险等级 |
|---|---|---|---|
| AS_11 | 钢制机械表 | `a stainless-steel mechanical watch on his LEFT wrist, the face turned inward toward his palm; it stays on the same wrist for the entire shot, unchanged in size and colour` | 中 |

### 提示词常量串（英文，token 级不变）
The same man appears in every shot: 35 years old, square jaw with prominent cheekbones, black
hair cropped to about one centimetre, deep brown eyes, thick straight eyebrows, narrow eyes, a
high nose bridge, thin lips, a hard jawline, tan skin with a slightly oily sheen, and a 4cm
diagonal pale scar on the right side of his jaw. He is tall and broad-shouldered. He wears a
white shirt with the top button open and the collar spread flat, a charcoal grey wool coat worn
buttoned up, black trousers and black leather shoes. A stainless-steel mechanical watch sits on
his left wrist with its face turned inward, staying on that wrist for the entire shot. His
appearance remains identical throughout: same face, same hair, same clothing, same age, same
body type, from the first frame to the last.
```

> **差异核对**：CH_01（女/28/165cm/偏瘦/偏白/齐肩长发/暖色系风衣）vs CH_02（男/35/185cm/宽肩/小麦色/寸头/冷灰系大衣）——**性别、年龄、身高、体格、肤色、发型、服装色系七项全拉开**，模型不可能把两人混成一个。

---

## 3. 角色身份串写法

### 3.1 三条筛选规则：只写「可见 + 稳定 + 独有」

写进身份串的每一个词，必须同时满足：

| 规则 | 说明 | 反例 |
|---|---|---|
| **可见** | 镜头拍得到、且在当前景别下分辨得出 | ❌ 中景里写"瞳色"——远景根本看不见 |
| **稳定** | 不随情绪、时间、剧情变化 | ❌ "她今天涂了红唇"——下一集不涂就漂 |
| **必有一项独有** | 全剧只有这个角色有的特征 | ❌ 两个角色都是"黑色长发" |

> **独有特征（signature）是身份串的灵魂**：一道疤、一颗位置特殊的痣、一只特定的耳环、一件固定的外套、一个反常的发色。没有它，模型只能靠概率猜。

### 3.2 甜点长度：中文 100–140 汉字 ≈ 英文 50–70 词
| 长度 | 风险 | 判定 |
|---|---|---|
| < 60 汉字 / < 30 词 | 模型自由填空，脸随机 | ❌ 太短 |
| **100–140 汉字 / 50–70 词** | 信息足够，不稀释后续指令 | ✅ **甜点区** |
| > 250 汉字 / > 120 词 | 挤占动作与运镜的注意力预算 | ❌ 太长 |

> 【推断】该区间由「40–70 英文词甜点区」这一业界通行说法 + 主模板 120 汉字锁定块实践共同推出，**未在 H3 上做受控实验**。建议按 §12 的方法自测 3 组长度各 10 次，用你自己的数据定档。
### 3.3 身份串六段顺序模板（顺序即权重，不要调换）

```
① 同一性声明 + 年龄
② 脸型
③ 发型发色
④ 眉眼 + 鼻唇
⑤ 肤质 + 稳定皮肤标记
⑥ 独有特征
⑦ 服装（可单独成串，见 §8）
⑧ 不变量总声明
```

**中文模板（人工审校用）**
```
同一名<性别>贯穿全部镜头：<数字>岁，<脸型>，<发型发色>，<瞳色>，<眉形>，<眼形>，
<鼻形>，<唇形>，<下颌/下巴>，<肤色肤质>，<独有特征>。身穿<服装版本 ID 的内容>。
从第一帧到最后一帧，脸、发型、服装、年龄、体型、配饰完全不变。
```

**英文模板（进模型，逐字复用）**
```
The same <man/woman> appears in every shot: <age> years old, <face shape>, <hair length +
texture + colour>, <eye colour> <eye shape> eyes, <eyebrow>, <nose>, <lips>, <chin/jaw>,
<skin tone + texture>, <signature feature>. <He/She> wears <outfit>. <His/Her> appearance does
not change at any point: same face, same hair, same clothing, same age, same body type,
same accessories, from the first frame to the last.
```

### 3.4 逐字复用纪律（Verbatim Rule）

> 实测：完整复述 vs 简化改写，一致性差异**可达 40%**【工艺，测试集与方法未公开，只当量级参考】。

```
✅ 正确：把常量串存成一个文件/一个变量，每次复制粘贴
❌ 错误：这次写 "shoulder-length straight black hair"，下次写 "black hair to her shoulders"
❌ 错误：这次写 "dark brown eyes"，下次写 "deep brown eyes"
❌ 错误：为了省字数删掉 "from the first frame to the last" 这句不变量声明
```

**执行细则**：① 常量串存成**单一事实源**（一个 md 文件或表格单元格），所有镜头从那里复制；
② **禁止同义替换、禁止润色、禁止按镜头裁剪**，哪怕觉得写得不好也要**全剧统一改**（见 §11.5）；
③ 三镜共用的锁定块用**字符串比对**验证逐字一致，不要人眼看；④ 改一个词 = 全量重测，不是"改完接着拍"。

### 3.5 身份串常见错误对照

| # | ❌ 错误写法 | 问题 | ✅ 正确写法 |
|---|---|---|---|
| 1 | `a beautiful woman` / `a young man` | 抽象词 + 区间，模型自由填空 | `28 years old, oval face, dark brown almond-shaped eyes` |
| 2 | `she looks worried` | 情绪不可见，不是身份 | `her eyebrows draw together, her jaw tightens`（属表演，不进身份串） |
| 3 | `wearing casual clothes` | "casual" 无具体指向 | `an ivory cotton T-shirt and dark-wash straight-leg jeans` |
| 4 | `with a scar` | 无位置、无大小、无颜色 | `a 1.5cm pale healed scar at the outer end of her right eyebrow` |
| 5 | 三处分别写 `black hair` / `dark hair` / `raven hair` | 同义替换 = 三次不同采样 | 三处全部 `straight black hair` |
| 6 | 身份串里写 `standing by the window` | 位置属分镜，会锁死后续调度 | 位置写在分镜段① |

---

## 4. 人物分层：主角 / 配角 / 路人的不同写法

### 4.1 三层的描述预算

| 层级 | 中文预算 | 英文预算 | 进锁定块 | 参考图槽位 |
|---|---|---|---|---|
| **主角** | 80–150 汉字（身份串）+ 30–60（服装串） | 50–80 词 | ✅ 三镜逐字复制 | 3–5 张 |
| **配角** | 25–50 汉字（一次性差异描述） | 15–30 词 | ⚠️ 仅当跨镜出现才进 | 1–2 张 |
| **路人** | **0–15 汉字**（能不写就不写） | ≤8 词 | ❌ | 0 张 |

> 底层逻辑：**提示词的注意力预算有限**。给路人多写 20 个字，主角的脸就少 20 个字的权重。

### 4.2 主角：完整身份串 + 服装串，进锁定块

```
【锁定块 · 三镜逐字复制】
The same woman appears in every shot: 28 years old, oval face, shoulder-length straight black
hair with slightly inward-curled ends, dark brown almond-shaped eyes, straight nose bridge, thin
lips, rounded chin, pale skin with natural visible texture, a 1.5cm pale healed scar at the outer
end of her right eyebrow. She wears an unbranded ivory round-neck cotton T-shirt, a dark khaki
long trench coat worn open, dark-wash straight-leg jeans and white low-top canvas shoes.
```
```
同一名女性贯穿全部镜头：28岁，鹅蛋脸，齐肩黑色直发发尾微内扣，深棕色杏仁形眼睛，鼻梁挺直，
唇形偏薄，下巴圆润，偏白肤色带自然可见质感，右眉尾一道1.5厘米浅白色旧疤。身穿无标识米白色
圆领纯棉T恤，深卡其色长款风衣（敞开），深蓝色直筒牛仔裤，白色低帮帆布鞋。
```

### 4.3 配角：四维差异表（**至少拉开 2 维，建议 4 维全拉开**）

| 差异维度 | 取值建议 | 示例 |
|---|---|---|
| **性别 / 年龄** | 差值 ≥7 岁 | 28 女 vs 35 男 |
| **身高 / 体格** | 差值 ≥15cm 或体格相反 | 165cm 偏瘦 vs 185cm 宽肩 |
| **发型 / 发色** | 长度或颜色不同 | 齐肩黑长直 vs 黑色寸头 |
| **服装色系** | 冷暖对立 | 暖卡其 vs 冷炭灰 |

```
✅ 正确（差异拉开，每人只给一个动作）
A tall man in a charcoal wool coat buttoned up (left of frame) and a shorter woman in a dark
khaki trench coat worn open (right of frame); the man folds his arms, then the woman takes one
step forward.

❌ 必崩（对称描述会诱导人物融合）
two men in suits
```

> **"对称描述"是多人场景的头号杀手。** 两个人的描述越对称，模型越倾向于把他们渲染成同一个人的两个副本，或者在运动中互相"吸收"。

### 4.4 配角的三条硬规则

① **每人只给一个动作**——两个动作 = 两套姿态在有限注意力里互相竞争。
② **用画面方位定位，不用角色左右**——✅ `left of frame` ❌ `on her left`（"她的左边"是左手边还是画面左边？这是左右翻转翻车的常见根因）。
③ **不出声的配角不给 `(S1)` 编号**【官方】——"characters who never vocalize receive no speaker ID"。

### 4.5 路人：虚化 + 数量 + 不给细节

```
✅ 正确
blurred passersby in the background, their faces out of focus and unreadable, their gaze
    directed away from the camera

✅ 正确（需要指定人数时）
exactly three blurred figures crossing in the deep background, out of focus

❌ 错误（给了细节 = 给了漂移机会）
three people in the background, one in a red jacket, one wearing glasses, one talking on a phone
```

**路人处理原则**：① 能不写就不写——画面里没有路人，就不会有路人漂移；② 必须有时写**虚化 + 数量 + 无五官**三件套；
③ **绝不给路人脸部、服装、动作细节**；④ 路人不进锁定块、不占参考图槽位。

### 4.6 人数写死，且写在第一句

```
✅ Exactly ONE person in frame, a single subject; the rest of the frame is filled by the room.
   中文：画面中严格只有一名人物，其余画面由场景本身填满。

✅ Exactly TWO people in frame: <Subject 1> on the left, <Subject 2> on the right.

❌ a woman sitting on the sofa          ← 没写死人数，背景可能长出第三个人
```

> 人数漂移是跨帧状态跟踪弱的直接后果。**人数声明必须前置到该镜第一句**，放在动作描述之前。

---

## 5. 外貌细节描述串库

> 用法：从下表每行挑**一个** token 拼进 §3.3 的六段模板，**同类别只挑一个，不要叠加**。
> 稳定性评级是针对「跨镜复现」的主观分级【推断】，量产前按 §12 校准。

### 5.1 脸型

| 中文 | 英文 token | 稳定性 | 备注 |
|---|---|---|---|
| 鹅蛋脸 | `oval face` | 高 | 最稳，推荐默认 |
| 圆脸 | `round face` | 高 | |
| 方脸 / 方下颌 | `square jaw` | **高** | 轮廓强，远景也认得出 |
| 长脸 | `long face` | 中 | |
| 心形脸 | `heart-shaped face` | 中 | |
| 菱形脸 | `diamond-shaped face` | 低 | 易与其他元素混淆 |
| 瓜子脸 | `small pointed chin, narrow face` | 低 | **不要直译成 `melon-seed face`** |

```
✅ a 28-year-old woman with an oval face and a rounded chin
   28 岁女性，鹅蛋脸，下巴圆润
❌ a woman with a beautiful face shape       ← 抽象
❌ melon-seed face                            ← 直译，模型无此概念
```

### 5.2 发型发色（**顺序：长度 → 质地 → 发色 → 分发/扎法**）

| 类别 | 英文 token | 稳定性 | 备注 |
|---|---|---|---|
| 长度 | `cropped hair`（寸头）/ `short hair` / `chin-length` / `shoulder-length` / `long hair past the shoulders` / `waist-length` | **高** | 最稳的发型特征 |
| 质地 | `straight` / `wavy` / `curly` / `coily` | **中高** | `straight` 最稳，`wavy` 运动中易变 |
| 发色 | `black` / `dark brown` / `chestnut brown` / `auburn` / `blonde` / `ash grey` / `dyed ash-blue` | **高**（纯色）/ **中**（渐变） | 避免 `ombre`、`highlighted` |
| 分发 | `centre-parted` / `side-parted` / `forehead fully visible`（无刘海）/ `blunt fringe` | 中 | 中远景下不可见 |
| 扎法 | `in a low ponytail` / `in a low bun` / `tucked behind her left ear` | 中 | 写了扎法，**全剧不能散下来** |

```
✅ shoulder-length straight black hair, centre-parted, with slightly inward-curled ends, tucked
   behind her left ear
   齐肩黑色直发，中分，发尾微内扣，别在左耳后

✅ black hair cropped to about one centimetre（配角 CH_02）

❌ nice hairstyle / elegant hair          ← 抽象
❌ hair that changes with the wind        ← 引入了不可控变量
❌ 这次写 shoulder-length，下一次镜头写 long hair   ← Verbatim Rule 违反
```

### 5.3 瞳色（**最易失效的一项**）

| 英文 token | 稳定性 | 备注 |
|---|---|---|
| `dark brown eyes` / `deep brown eyes` | 中 | 深色瞳在暗光下与黑色瞳不可分 |
| `black eyes` | 中 | |
| `light brown eyes` / `hazel eyes` | 低 | 中远景下几乎不可见 |
| `blue eyes` / `green eyes` / `grey eyes` | **低**（亚洲面孔）/ 中（其他） | 与肤色、发色组合冲突时会被模型"修正" |
| `heterochromia`（异色瞳） | **极低** | 两眼不同色属结构性高风险，建议禁用 |

```
✅ dark brown almond-shaped eyes         ← 眼形 + 瞳色一起写，眼形更稳
   深棕色杏仁形眼睛

❌ eyes that look sad                     ← 情绪，不是外貌
❌ one blue eye and one brown eye         ← 异色瞳，禁
```

### 5.4 五官

| 部位 | 英文 token | 稳定性 |
|---|---|---|
| 眉 | `thick straight eyebrows` / `thin arched eyebrows` / `dark eyebrows` | **中高**（浓直眉 > 细弯眉） |
| 眼形 | `almond-shaped` / `narrow` / `round` / `deep-set` / `monolid` eyes | **高** |
| 鼻 | `a straight` / `a high` / `a slightly upturned` / `a broad` nose bridge | **中高** |
| 唇 | `thin lips` / `full lips` / `a defined cupid's bow` | 中 |
| 下颌/下巴 | `a rounded chin` / `a pointed chin` / `a hard jawline` / `a square jaw` | **高** |

```
✅ thick straight eyebrows, narrow eyes, a high nose bridge, thin lips, a hard jawline
   浓直眉，细长眼，高鼻梁，薄唇，下颌线硬

❌ delicate features / regular features        ← 中文"五官端正"直译，模型无对应
```

### 5.5 体型

| 维度 | 英文 token | 稳定性 |
|---|---|---|
| 身高 | `about 165 cm tall` / `tall (around 185 cm)` / `short` | **高**（写具体数字） |
| 体格 | `slim` / `lean and wiry` / `broad-shouldered` / `heavyset` / `muscular` | 中高 |
| 肩线 | `narrow` / `broad` / `sloped` shoulders | 中高 |
| 站姿 | `standing upright` / `slightly stooped` | 中（属表演，非身份） |

```
✅ 165 cm tall, slim, with narrow shoulders
   165 厘米左右，偏瘦，肩线窄

✅ tall and broad-shouldered, around 185 cm

❌ a good figure / nice body            ← 抽象 + 会被模型自由解释
❌ of medium height                     ← "中等"是区间，两次采样可差 15cm
```

### 5.6 年龄表达

> **一律写数字。** `young` / `middle-aged` / `elderly` 是区间，两次采样可能差 15 岁。

```
✅ 28 years old / 28 岁
✅ a man in his early sixties        ← 若必须模糊，用 decade 限定
❌ a young woman
❌ middle-aged man
```

### 5.7 组装公式与自检

```
[同一性声明] The same <woman/man> appears in every shot:
[年龄]      28 years old,
[脸型]      oval face,
[发型]      shoulder-length straight black hair with slightly inward-curled ends, centre-parted,
[眉眼]      dark eyebrows, dark brown almond-shaped eyes,
[鼻唇]      a straight nose bridge, thin lips,
[下颌]      a rounded chin,
[肤质]      pale skin with natural visible texture,
[独有特征]  a 1.5cm pale healed scar at the outer end of her right eyebrow.
[服装]      She wears ...
[不变量]    Her appearance remains identical throughout: same face, same hair, same clothing,
            same age, same body type, same accessories, from the first frame to the last.
```

> 组装自检（5 条）：① 每类只挑 1 个 token；② 无抽象形容词；③ 至少一项独有特征；
> ④ 长度落在 50–80 英文词 / 100–140 汉字；⑤ 与角色卡常量串逐字一致。

---

## 6. 皮肤描写

### 6.1 三个维度

| 维度 | 写什么 | 例子 |
|---|---|---|
| **肤色** | 具体的色相 + 明暗，不用比喻 | `pale` / `light` / `tan` / `olive` / `deep brown` |
| **质感** | 可见的表面状态 | `natural visible texture, visible pores, matte finish` |
| **稳定标记** | 痣 / 雀斑 / 胎记（见 §6.3） | `a 2mm dark brown mole just above her left collarbone` |

### 6.2 会失效的描述（**禁用清单**）

| ❌ 禁用 | 为什么失效 | ✅ 替换成 |
|---|---|---|
| `porcelain skin` | 比喻，指向"白 + 光滑 + 无瑕"三个不确定维度 | `pale skin with a matte finish` |
| `flawless skin` | 抽象，且会被理解为"无任何标记"，与你要写的痣冲突 | `natural skin texture with visible pores` |
| `glowing skin` / `radiant skin` | 指向打光而非皮肤，会把"皮肤"变成"光照"变量 | `soft even skin tone` |
| `ethereal` / `dewy` / `luminous` | 风格词，会带动整个画风漂移 | 删掉 |
| `smooth skin` | 与"自然质感"冲突，且易触发磨皮 | `natural visible texture, visible pores` |
| `fair-skinned beauty` | 评价词，不是描述 | `light skin, cool undertone` |

```
✅ pale skin with natural visible texture, visible pores and a matte finish
   偏白肤色，自然可见质感，可见毛孔，哑光质感

✅ tan skin with a slightly oily sheen, visible pores beside the nostrils（配角 CH_02）

❌ porcelain, flawless, glowing skin
```

### 6.3 稳定标记：痣 / 雀斑 / 胎记

**四要素写法（与资产锁定同构，见 §9.1）**：`位置 + 尺寸 + 颜色 + 形状`

| 标记类型 | 英文 token | 风险 | 备注 |
|---|---|---|---|
| **痣（单颗）** | `a 2mm dark brown mole just above her left collarbone` | **中高** | 太小就会消失；**直径 ≥3mm 才考虑承载叙事** |
| **痣（唇/眉边）** | `a small dark mole at the left corner of her mouth` | 中 | 位置在五官附近，注意力相对较高 |
| **雀斑（成片）** | `light freckles scattered across the bridge of her nose and both cheeks` | **中** | 成片反而比单颗稳（面积大），但边界易随光照变化 |
| **胎记** | `a 3cm pale pink birthmark on the left side of her neck` | **中** | 面积较大，是三类里最稳的 |
| **白癜风 / 大片色差** | `a pale patch of skin on her right temple` | 低 | 面积大、对比强 |

```
✅ 痣：a 2mm dark brown mole just above her left collarbone, unchanged in size, colour and
       position throughout
   左侧锁骨上方一颗直径约 2 毫米的深褐色痣，全程大小、颜色、位置不变

✅ 雀斑：light freckles scattered across the bridge of her nose and both cheeks, unchanged
         in density throughout

✅ 胎记：a 3cm pale pink birthmark on the left side of her neck, unchanged throughout

❌ a mole somewhere on her face        ← 位置不确定 = 每次随机长
❌ beauty mark                          ← 文化专有词，位置不确定
❌ 这集写 a mole above her collarbone，下集写 a mole on her chest   ← 位置换 = 换人
```

### 6.4 皮肤标记与光照的关系（**常被忽略**）

| 现象 | 原因 | 处置 |
|---|---|---|
| 痣在暖光下变浅、冷光下变深 | 皮肤标记是**色差**，随白平衡变化 | 该角色色温与场景表锁死（§11.3） |
| 雀斑在侧逆光下消失 | 对比度被压平 | 需雀斑出镜的镜头，主光走正面 45°，不要侧逆 |
| 痣在特写清晰、中景消失 | 像素占比随景别下降 | 承载叙事的痣只在特写里承担识别，中景交给发型/服装 |

### 6.5 妆容（**可变项，处理规则特殊**）

① 能不写就不写——写了妆，模型每次给的浓淡都不同；② 必须写时，连同浓淡一起写死并声明全程不变；
③ 剧情需要妆容变化（哭花妆、卸妆）→ 按 §8.3 的逻辑给妆容建版本 ID：`CH_01_MAKEUP_A` / `CH_01_MAKEUP_B`。

```
✅ minimal natural makeup: bare eyelids, muted rose lip colour, a matte finish,
   unchanged throughout
   极淡自然妆：眼睑保持素净，哑光玫瑰色唇，全程不变

❌ she wears makeup                    ← 浓淡随机
❌ heavy smoky eye makeup              ← 复杂 + 与"自然质感"画风冲突
```

### 6.6 皮肤描写自检

> ① 肤色写具体色相，不用比喻词；② 质感写"自然质感 + 无磨皮"；③ 稳定标记给了位置 + 尺寸 + 颜色 + 不变量声明；
> ④ 承载叙事的标记面积够大（≥3mm 或 ≥3cm）；⑤ 妆容要么不写，要么连浓淡一起写死；⑥ 色温已与场景表对齐。

---

## 7. 伤口与身体标记

### 7.1 四要素写法（位置 + 尺寸 + 颜色 + 阶段）

```
[位置] at the outer end of her right eyebrow     右眉尾
[尺寸] 1.5cm long, about 2mm wide                长 1.5 厘米，宽约 2 毫米
[颜色] pale, slightly lighter than the surrounding skin   浅白色，略浅于周围皮肤
[阶段] a healed scar                             已愈合的疤
```

**完整例句**
```
✅ a 1.5cm pale healed scar at the outer end of her right eyebrow, unchanged in size, colour
   and position throughout
   右眉尾一道长 1.5 厘米的浅白色旧疤，全程大小、颜色、位置不变

✅ a 4cm diagonal pale scar on the right side of his jaw（配角 CH_02）

❌ she has a scar on her face      ← 无位置、无尺寸、无颜色、无阶段
❌ a wound                          ← "wound" 是开放性伤口，与疤（scar）是两回事
```

### 7.2 阶段词汇表（**阶段错了就不是同一个伤**）

| 阶段 | 英文 token | 颜色 | 风险 |
|---|---|---|---|
| 新伤出血 | `a fresh bleeding cut` | `bright red` | **极高**（液体 + 颜色随时间变化） |
| 结痂 / 愈合中 | `a scabbed cut` / `a healing cut` / `a pink healing scar` | `dark red-brown` / `pink` | **高**（颜色处于变化中） |
| **已愈合 / 陈旧疤** | `a healed scar` / `an old scar` / `a faded scar` | `pale, slightly shiny` | **中高**（颜色稳定，但面积小） |
| 增生疤（疤痕疙瘩） | `a raised keloid scar` | `pink, raised` | **高**（立体结构） |
| 淤青 | `a bruise` | `purple-blue fading to yellow-green` | **高**（颜色随天数变） |
| 包扎 | `a bandaged wound` / `a white gauze pad taped on her forearm` | — | **中**（绷带面积大，比疤稳） |

```
✅ 稳定选择：healed scar（已愈合的浅白疤）——颜色不变、不出血、不变化
⚠️ 慎选：healing cut（愈合中）——"愈合中"意味着颜色在变，模型会理解为可以变换颜色
❌ 禁用：fresh bleeding cut（除非这一镜就是受伤瞬间，且只出现一镜）
```

### 7.3 为什么伤口是高风险资产

| 原因 | 说明 |
|---|---|
| **面积小** | 1.5cm 的疤在 768p 的中景里只有几十像素，注意力权重极低 |
| **色值与皮肤接近** | 浅白色疤 vs 偏白皮肤，对比度低，容易被"磨皮"掉 |
| **随景别消失** | 特写里清晰，中景里可能被模型判定为"噪点"而抹除 |
| **形状易变** | "斜向"作为方向描述是软引导，模型可能给成横向 |
| **与光照耦合** | 侧逆光下疤的明暗反转，观感上就是"疤没了"或"疤变深了" |

> ⚠️ **若这道疤承载叙事信息**（比如"这道疤是身份证据"），**必须走参考图，不能只靠文字**。参见 §9.6 风险排序表与 §10 参考图分配。

### 7.4 伤口的三种锁定方案（按可靠性排序）

| 档 | 方案 | 做法 | 适用 |
|---|---|---|---|
| **A 推荐** | **参考图锁定** | 一张疤部特写，Ref2VA 里标 `fully_preserved`，并在 `retention_analysis` 明确保留内容 | 疤承载叙事信息 |
| **B 次选** | **描述串 + 不变量声明 + 接触阴影句** | 四要素写全 + `unchanged in size, colour and position throughout` + 一句接触/投影描述 | 疤只是人物设定，不承载叙事 |
| **C 降级** | **换成大面积标记** | 把"1.5cm 的眉疤"改成"左颈一块 3cm 胎记"或"左手背一条 8cm 长疤" | 测出复现率不达标时（§12.6） |

**方案 A 的 `retention_analysis` 写法**
```
<Picture 4> (appears in [Shot 1], [Shot 3]): fully_preserved - the 1.5cm pale healed scar at
    the outer end of her right eyebrow keeps its exact length, colour and position, staying
    visible and identical in every frame from the first to the last.
```

### 7.5 伤口要"变化"时：每阶段一个版本 ID

剧中伤口常需呈现"受伤 → 结痂 → 愈合"的过程。做法是**把它当成服装版本一样管理**：

| 版本 ID | 阶段 | 描述串（逐字复用） | 出现集段 |
|---|---|---|---|
| `CH_01_SCAR_A` | 已愈合旧疤 | `a 1.5cm pale healed scar at the outer end of her right eyebrow` | E01–E11, E20+ |
| `CH_01_SCAR_B` | 结痂期 | `a 1.5cm dark red-brown scab at the outer end of her right eyebrow` | E12–E15 |
| `CH_01_SCAR_C` | 愈合中 | `a 1.5cm pink healing scar at the outer end of her right eyebrow` | E16–E19 |

```
规则：
1. 一个阶段 = 一个 ID = 一段独立描述串，集段之间不混用
2. 同一集内不得同时出现两个版本
3. 换版本 = 换参考图，并把新图登记进参考图集
4. 版本切换点记进变更日志（§11.5）
```

### 7.6 义肢：为什么单列最高风险
> 【推断】风险排序：**义肢（最高）＞ 纹身 ＞ 耳环/戒指 ＞ 手表/手机 ＞ 大面积衣物/围巾（最低）**

**义肢单列最高档，原因不是"物件太小"，而是失效机制完全不同**：耳环失效是**物件丢失**（只有那一个小区域受影响）；义肢失效是**肢体结构崩坏**——整条肢体的轮廓与关节结构错乱，手部动作、袖口、与他人的空间关系全部连带失效。模型缺少"手臂应该长什么样"的形态约束。

```
❌ 禁止：剧情里给主要角色装义肢并期待跨镜稳定复现
⚠️ 若必须有：
   · 只拍静态中远景（不特写、不拍末端、不做手部动作）
   · 义肢必须走参考图且标 fully_preserved
   · 参考图里要有真人穿戴该义肢的全身照（不是义肢单品图）
   · 量产前按 §12 测 ≥20 次，成功率不达标就改剧本
✅ 推荐替代：把"义肢"换成不破坏轮廓的标记——长袖遮住 + 一个明显的外部物件（拐杖 / 手套 / 护具），
   或干脆改成"左手活动不便"的表演设计（不依赖视觉结构）
```
### 7.7 纹身（次高风险）

```
风险原因：图案复杂 + 面积中等 + 位于皮肤上会随肢体形变——模型要同时解对"位置、图案、形变"三件事
```

```
✅ 可行（简单、大、高对比、位置平坦）
a solid black tribal band about 4cm wide around his left upper arm, unchanged in shape,
size and position throughout

⚠️ 勉强（中等复杂）
a small black outline of an anchor on the inside of her left forearm, about 5cm tall

❌ 禁用（复杂图案 + 文字 + 彩色渐变）
a full-colour Japanese-style sleeve tattoo with koi, waves and kanji characters

❌ 禁用（会随皮肤形变且面积小）
a small script tattoo on her ribs, reading "breathe"
肋骨处一行写着 "breathe" 的小字纹身   ← 文字 + 小面积 + 曲面，三重高风险
```

### 7.8 伤口与身体标记自检

> ① 四要素写全；② 阶段词选颜色稳定的（healed / old / faded）；③ 有不变量声明；
> ④ 承载叙事 → 走了参考图 + `fully_preserved`；⑤ 多阶段 → 每阶段一个版本 ID；
> ⑥ 义肢已按 §7.6 评估；⑦ 纹身图案简单、面积大、位置平坦；⑧ 已按 §12 测过并记录。

---

## 8. 服装系统

### 8.1 为什么需要服装版本 ID

服装是**面积最大的身份标识**，也是最稳定的一致性抓手（比耳环稳一个数量级）。但它有个陷阱：

> **同一段描述串，如果角色在剧里换过装，模型会把两套衣服的特征混在一起**——第 5 集的风衣可能长出第 12 集大衣的领子。

**解法**：给每套衣服一个 ID，描述串跟 ID 走，不与角色本体混写。

### 8.2 ID 命名规则

```
CH_<角色号>_OUT_<版本字母>
CH_01_OUT_A      主角沈昭 · 第 1 套（米白T恤 + 深卡其风衣 + 深蓝牛仔 + 白帆布鞋）
CH_01_OUT_B      主角沈昭 · 第 2 套（黑色高领毛衣 + 灰色西装外套 + 黑色西裤）
CH_02_OUT_A      配角陆行舟 · 第 1 套（白衬衫 + 炭灰大衣 + 黑西裤 + 黑皮鞋）
```

配套的身体标记、妆容也用同样的命名空间：
```
CH_01_SCAR_A / CH_01_SCAR_B      伤口版本
CH_01_MAKEUP_A / CH_01_MAKEUP_B  妆容版本
CH_01_HAIR_A / CH_01_HAIR_B      发型版本（扎起 / 散下）
```

### 8.3 「换装即换 ID」判定表

| 变化 | 算不算换装 | 处置 |
|---|---|---|
| 换上衣 / 换颜色 / 换材质 | ✅ 算 | 新建 OUT 版本（颜色最敏感） |
| 外套脱下 / 穿上 | ✅ 算 | 新建 OUT 版本（层数变了） |
| 衣服脏了 / 湿了 / 破了 | ✅ 算 | 新建 OUT 版本（`a rain-soaked version of CH_01_OUT_A`） |
| 外套敞开 ↔ 扣上、袖子挽起、换鞋 | ⚠️ 边界 | 同一版本内用状态句区分：`worn open` / `buttoned up` / `sleeves rolled`，**不换 ID** |
| 换配饰（摘掉耳环） | ❌ 不算服装 | 走资产表（§9），并明写"该镜不戴耳环" |

```
✅ 正确：CH_01_OUT_A → CH_01_OUT_B 之间，提示词里完整替换整段服装串
❌ 错误：把两套衣服的描述串同时留在锁定块里，让模型自己选
❌ 错误：同一集内 A 版本和 B 版本的串混着用
```

### 8.4 服装描述串五要素公式
`[颜色] + [材质] + [版型/细节] + [层次与穿着方式] + [不变量声明]`

| 要素 | 作用 | token 示例 |
|---|---|---|
| **颜色** | 最敏感，必须具体到色相 | `ivory` / `dark khaki` / `charcoal grey` / `dark-wash indigo` |
| **材质** | 决定反光度 | `cotton` / `wool` / `denim` / `matte` |
| **版型/细节** | 拉开与其他服装的距离 | `round-neck` / `long-line` / `straight-leg` / `low-top` |
| **层次与穿着方式** | 防止"有时穿有时不穿" | `worn open without the belt` / `buttoned up` |
| **不变量声明** | 防止中途换色换件 | `unchanged in colour, material and number of layers throughout` |

```
✅ She wears an unbranded ivory round-neck cotton T-shirt, a dark khaki long-line trench coat
   worn open without the belt, dark-wash straight-leg jeans and white low-top canvas shoes.
   The outfit is unchanged in colour, material and number of layers from the first frame to
   the last, the coat staying open and on her shoulders the whole time.
❌ She wears casual clothes.        ← 抽象
❌ a white top and dark pants        ← 白得哪种白？深得哪种深？
❌ She is wearing a trench coat.     ← 没写里面穿什么，模型逐帧自由发挥
```
### 8.5 服装属性稳定性分级

| 属性 | 稳定性 | 说明 | 建议 |
|---|---|---|---|
| **颜色（纯色）** | **高** | 最好抓的特征 | 优先把身份信息压在颜色上 |
| **大面积色块对比** | **高** | 如"黑大衣 + 白衬衫"领口三角区 | 极稳，推荐 |
| **材质（哑光）** | **中高** | `matte` / `cotton` / `wool` | 推荐 |
| **材质（反光）** | 低 | `silk` / `satin` / `leather` / `sequin` 随光照剧变 | 避开，或锁死光位 |
| **版型** | 中 | 随体型姿态变化 | 写 `straight-leg`、`fitted` 等具体词 |
| **图案（格子/条纹）** | **低** | 间距与对齐在运动中必崩 | **禁用** |
| **纯色无标识** | **高** | `unbranded` / `plain` / `solid-coloured` | 推荐，兼避文字风险 |
| **品牌 / 字母** | **极低** | 文字渲染不可靠 | **禁用** |
| **层数** | 中高 | 离散量，模型好抓 | 明确写层数 |

```
✅ 高稳定组合（推荐作为角色主穿搭）
   · 纯色 + 哑光材质 + 无标识 + 明确的领口对比
   · 例：charcoal grey wool coat + white shirt with the top button open

❌ 低稳定组合（禁止）
   · 格子衬衫 / 条纹毛衣 / 印花连衣裙 / 带字母的卫衣 / 亮片礼服 / 丝绸反光面料
```

### 8.6 服装表模板 + 填好的范例

```markdown
| 版本ID | 角色 | 上装 | 外套 | 下装 | 鞋 | 出现集段 | 参考图ID | 风险 |
|---|---|---|---|---|---|---|---|---|
```

**填好的范例**

| 版本ID | 角色 | 上装 | 外套 | 下装 | 鞋 | 层数 | 出现集段 | 参考图ID | 风险 |
|---|---|---|---|---|---|---|---|---|---|
| `CH_01_OUT_A` | CH_01 | 米白无标识圆领纯棉 T 恤 | 深卡其长款风衣（敞开、不系腰带） | 深蓝直筒牛仔裤 | 白色低帮帆布鞋 | E01–E60 | IMG_03 | 低 |
| `CH_01_OUT_B` | CH_01 | 黑色高领毛衣 | 灰色单排扣西装外套（扣上） | 黑色直筒西裤 | 黑色短靴 | E25–E29 | IMG_10 | 低 |
| `CH_02_OUT_A` | CH_02 | 白衬衫（第一颗扣敞开、无领带） | 炭灰羊毛大衣（扣上） | 黑色西裤 | 黑色皮鞋 | E01–E60 | IMG_12 | 低 |

### 8.7 易翻车的服装动作

| 动作 | 风险 | 替代写法 |
|---|---|---|
| 脱 / 穿外套 | **高**（布料形变 + 层数变化） | 外套一开始就是脱下/穿好的状态，镜头不拍过程 |
| 系扣 / 解扣 / 系腰带 | **高**（手部精细动作 + 状态变化） | `the coat is already buttoned` / `worn open throughout` / `worn without the belt` |
| 围巾 / 大摆裙随风摆动 | **高**（布料物理是结构性缺陷） | `the scarf hangs still against her chest`；`the hem sways once, then settles`（一次、有终点） |
| 挽袖子 | 中 | 一开始就挽好，`with both sleeves already rolled to the forearm` |

```
✅ The coat is already off, staying draped over the back of the chair for the entire shot.
   外套已经脱下，全程搭在椅背上。

❌ She takes off her coat and hangs it up.
```

### 8.8 服装描写自检

> ① 五要素齐全；② 纯色 + 哑光 + 无标识，无格子/条纹/印花/字母；③ 每版本有 ID，集段不混用；
> ④ 状态（敞开/扣上/挽袖）用状态句写死；⑤ 镜头内无穿脱、系扣动作；⑥ 服装表已登记、参考图已分配。

---

## 9. 资产锁定：四要素 + 接触阴影句

### 9.1 资产锁定四要素

> **颜色 + 材质 + 固定位置 + 不变量声明**，四者缺一不可。

| 要素 | 作用 | 缺失后果 |
|---|---|---|
| **颜色** | 提供最强对比信号 | 模型随机给色，逐帧变 |
| **材质** | 决定反光度与轮廓 | 银色被渲染成金色、哑光被渲染成亮面 |
| **固定位置** | 把物件绑在一个稳定坐标上 | 耳环从左耳跑到右耳，戒指换手 |
| **不变量声明** | 明确告诉模型"这个东西不许变" | 模型默认所有东西都可以随剧情变化 |

### 9.2 不变量声明的「五不变」——**一律正向写**

> ⚠️ **禁用 `never removed` / `never duplicated` / `never changes hand`。** 锁定块逐镜复制，
> 而团队规则是**每镜否定表达 ≤1 处**（`Do not` 与裸名词否定合并计，`h3-antibug-check` §1.3
> / 主模板 §6.4-F）。锁定块里 1 处否定 = **全剧每一镜的额度都在这一个块上用光**，
> 任何一镜都再加不了 `Do not` 收边。

| 语义 | ❌ 禁用 | ✅ 正向写法 |
|---|---|---|
| 不被摘下 | `never removed` | `staying on her right ring finger for the entire shot` |
| 不重复出现 | `never duplicated` | `a single ring, worn on one finger only` |
| 不换手 / 换边 | `never changes hand` / `never switches ear` | `staying on the same hand from the first frame to the last` |
| 不变大小 | `never changes size` | `unchanged in size` |
| 不变颜色 | `never changes colour` | `unchanged in colour` |

> 💡 **唯一例外：左右方位消歧。** `... (worn on the right hand, not the left)` 里的 `not the left`
> 属方位消歧（主模板 §6.4-C 要求），**保留，不计入额度**。

### 9.3 接触阴影句（对抗"消失"最有效的补充）

> 【推断】这是全部技巧里性价比最高的一条。

**原理**：模型判断"某个区域有没有东西"，依赖该区域与周围的**像素差异**。悬空描述的小物件会被当噪点抹掉；写了它**投下的阴影 / 与皮肤的接触压痕**，等于在画面里留了一个"这里必须有东西"的位置证据。

```
✅ 有接触阴影句
A small matte-gold signet ring on her RIGHT ring finger (worn on the right hand, not the left).
The ring stays on that same finger for the entire shot, a single ring worn on one finger only,
unchanged in size, colour and shape. A thin soft shadow falls across the skin at the base of the
ring where it meets her finger.

❌ 无接触阴影句
She wears a gold ring.
```

**接触阴影句的其他写法**：

| 物件 | 接触阴影句 |
|---|---|
| 耳环 | `the earring casts a small soft shadow on her neck below the left earlobe`<br>耳环在她左耳垂下方的颈部投下一小块柔和阴影 |
| 戒指 | `a thin soft shadow falls across the skin at the base of the ring where it meets her finger`<br>戒指与手指相接的根部，皮肤上落着一道细薄的柔和阴影 |
| 手表 | `the watch case presses a shallow dent into her wrist, with a soft shadow along its lower edge`<br>表壳在手腕上压出一道浅痕，下缘带一道柔和阴影 |
| 项链 | `the pendant rests against her collarbone and casts a small oval shadow on her skin`<br>吊坠贴在锁骨上，在皮肤上投下一小块椭圆形阴影 |
| 眼镜 | `the frame rests on the bridge of her nose, leaving two small contact shadows on her cheeks`<br>镜架架在鼻梁上，在双颊留下两小块接触阴影 |
| 义肢 | `the socket edge meets her sleeve with a visible seam and a soft shadow beneath it`<br>接受腔边缘与袖口相接处有一道可见接缝，下方一道柔和阴影 |

### 9.4 一镜内需稳住的小物件 ≤ 2 件（硬规则）

> 同时写耳环 + 项链 + 戒指 + 手链 + 发卡，**几乎必然丢 1–2 件**。

| 一镜内小物件数 | 预期结果 |
|---|---|
| 1 件 | 最稳 |
| **2 件** | ✅ **上限，推荐配置** |
| 3 件 | 大概率丢 1 件 |
| ≥4 件 | 必然丢 1–2 件，且可能互相"合并"（耳环跑到项链上） |

**执行方法**：给角色登记 3–4 件配饰没关系，但**每个镜头只挑 1–2 件写进提示词**，其余的在该镜不写（并接受它们可能不出现）。

```
✅ 本镜只锁 2 件
[ASSET LOCK] Lock exactly two signature accessories in this shot: the silver hoop earring on
her left earlobe, and the matte-gold signet ring on her right ring finger. Both remain unchanged
for the entire shot. No other jewellery is visible.

❌ 一镜锁 5 件
She wears a silver hoop earring on her left earlobe, a thin silver necklace with a small
pendant, a matte-gold signet ring on her right ring finger, a beaded bracelet on her left wrist,
and a metal hair clip above her right ear.
```

### 9.5 每个角色最多锁定 1–2 件标志性配饰（全剧维度）

```
规则：
· 每个角色的"标志性配饰"配额 = 2 件（全剧固定，进角色卡常量串）
· 锁多了会互相干扰——模型在有限注意力里分配权重，5 件配饰 = 每件只有 20% 的权重
· 其余配饰可以作为"临时道具"出现，但不进常量串，且不承载叙事信息
```

| 角色 | 标志性配饰（2 件） | 临时配饰（不进常量串） |
|---|---|---|
| CH_01 沈昭 | 左耳银圆环耳环 / 右手无名指哑光金印章戒指 | 手提包、围巾（按镜登记） |
| CH_02 陆行舟 | 左腕钢制机械表 | 公文包、领带（按镜登记） |

### 9.6 资产风险排序表

> 【推断】本表基于机制推断与小样本实践，**不是量化基准**，量产前按 §12 校准。

| 排名 | 资产 | 风险 | 失效形态 | 处置 |
|---|---|---|---|---|
| 1 | **义肢** | **最高** | 肢体轮廓与关节结构崩坏，非"物件丢失" | **建议禁用**，或仅静态中远景 + 参考图（§7.6） |
| 2 | **纹身** | 高 | 图案变形、位置漂移、随肌肉形变 | 简单纯色大图案 + 参考图 |
| 3 | **耳环 / 戒指** | 中高 | 消失、左右互换、数量重复 | 四要素 + 接触阴影句 + 参考图 |
| 4 | **手表 / 手机** | 中 | 换手、表盘乱码、正反面翻转 | 声明"全程固定在同一只手上"；屏幕走干净底板 |
| 5 | **眼镜** | 中 | 镜片反光变化、忽有忽无 | 接触阴影句（鼻梁两点）效果好 |
| 6 | **小面积伤口 / 疤** | 中高 | 被"磨皮"掉、位置漂移 | 见 §7.4 |
| 8 | **大面积衣物 / 围巾** | **低** | 最稳 | **优先把身份识别压在这一档** |
| 9 | **帽子 / 包** | 中低 | 面积较大，相对稳 | 可作身份标识备选 |

> **设计原则（最重要的一条）**：把"身份标识"设计在**大面积、高对比、位置固定**的特征上。**红围巾 > 耳环**——能用服装颜色解决的识别问题，不要用耳环解决。

### 9.7 资产锁模板（可直接复制）

**英文（进模型）**
```
[ASSET LOCK — paste verbatim] A single small silver hoop earring on her LEFT earlobe (on the
left ear, not the right). The earring stays on that earlobe for the entire shot, one earring on
one ear only, unchanged in size, shape, colour and position. A small soft shadow falls on her
neck just below the earring. A small matte-gold signet ring on her RIGHT ring finger (worn on
the right hand, not the left). The ring stays on that same finger for the entire shot, one ring
on one finger only, unchanged in size, colour and shape. A thin soft shadow falls across the
skin at the base of the ring where it meets her finger. [LIMIT] Exactly two accessories are
locked in this shot: the earring and the ring, and nothing else on her hands or ears.
```

**中文（人工审校用）**
```
［资产锁——逐字粘贴］她左耳垂佩戴一只银色小圆环耳环（在左耳，非右耳）。该耳环在整个镜头中
始终佩戴在左耳垂上，仅此一只，大小、形状、颜色、位置保持不变。耳环正下方的颈部落着一小块
柔和阴影。她右手无名指佩戴一枚哑光金色印章戒指（戴在右手，非左手）。该戒指在整个镜头中
始终戴在同一根手指上，仅此一枚，大小、颜色、形状保持不变。戒指与手指相接的根部，皮肤上
落着一道细薄的柔和阴影。［限制］本镜恰好锁定两件配饰：耳环与戒指，她的耳部与手部仅此两件。
```

### 9.8 人物资产表模板 + 填好的范例

```markdown
| 资产ID | 名称 | 所属角色 | 类别 | 四要素锁定串（固定不变） | 出现集段 | 参考图ID | 保留强度 | 风险等级 | 实测 PPR |
|---|---|---|---|---|---|---|---|---|---|
```

**填好的范例**（接触阴影句见 §9.3，此处省略）

| 资产ID | 名称 | 角色 | 类别 | 四要素锁定串 | 集段 | 图ID | 保留强度 | 风险 | PPR |
|---|---|---|---|---|---|---|---|---|---|
| AS_07 | 银色小圆环耳环 | CH_01 | 随身佩戴 | `a single small silver hoop earring on her LEFT earlobe, one earring on one ear only, staying on that earlobe for the entire shot, unchanged in size, shape, colour and position` | 全剧 | IMG_06 | `fully_preserved` | 中高 | 待测 |
| AS_08 | 哑光金印章戒指 | CH_01 | 随身佩戴 | `a small matte-gold signet ring on her RIGHT ring finger, one ring on one finger only, staying on that finger for the entire shot, unchanged in size, colour and shape` | 全剧 | IMG_06 | `fully_preserved` | 中高 | 待测 |
| AS_11 | 钢制机械表 | CH_02 | 随身佩戴 | `a stainless-steel mechanical watch on his LEFT wrist, face turned inward; unchanged in size and colour` | 全剧 | IMG_12 | `fully_preserved` | 中 | 待测 |
| AS_14 | 右眉尾旧疤 | CH_01 | 身体标记 | `a 1.5cm pale healed scar at the outer end of her right eyebrow; unchanged in size, colour and position` | 全剧 | IMG_04 | `fully_preserved` | 中高 | 待测 |

**类别枚举**（与主模板 §5.2 一致）：随身佩戴 / 道具 / 场景固定物 / 身体标记（伤疤、纹身）/ 特效

### 9.9 人物与资产的字数预算（**7000 字符总量下**）
**预算**：主角身份串 80–150 + 服装串 30–60 + 每件资产锁串 40–70（均进锁定块，**三镜只计 1 次**）+ 配角 25–50（每人 1×）。全套含场景、画风、六段指令、声音层，约 **1100–1850（Base）／ 1450–2470（Ref2VA）汉字**。

> 7000 字符上限对人物与资产非常宽裕（仅用掉约 20–35%）。**不要为怕超限而删减身份串或资产锁串**——这是一致性的全部本钱，先砍别的。
### 9.10 资产锁定自检

> ① 四要素齐全；② 每件配了接触阴影句；③ 本镜小物件 ≤2 件；④ 每角色标志性配饰 ≤2 件（全剧）；
> ⑤ 左右写成 `on the LEFT ... (on the left, not the right)`；⑥ 高风险资产走了参考图 + `fully_preserved`；
> ⑦ 资产串各镜逐字一致（字符串比对）；⑧ 资产表已登记、实测 PPR 已填或标待测。

---

## 10. Ref2VA 参考模式：人物与资产的正确锁定方式

### 10.1 前置决策：与图生视频互斥（**必须先二选一**）

> 【官方】`first_frame` / `last_frame` 与 `reference_*` **不可同时出现在同一次请求中**。

**决策规则**：本段落是否需要「精确控制首帧或尾帧构图」？
- **是** → 走 FL2VA（触发镜型：#7 揭示镜需尾帧、#6 同构图匹配镜需首帧）。代价：放弃 9 图资产锁，一致性退化为「2 张图 + 描述串」；补偿办法见 §9.7、§10.8。
- **否** → 走 **Ref2VA**（默认路径）：9 图 + 3 视频 + 3 音频，脸 / 侧面 / 全身 / 标记 / 资产各占独立槽位。

| 维度 | Ref2VA | FL2VA |
|---|---|---|
| 参考文件 | ≤12（图 ≤9 / 视频 ≤3 / 音频 ≤3） | 1–2 张图 |
| 人物锁定手段 | 每资产独立锁定 + 保留强度标记 | 描述串 + 2 张图 |
| 首尾帧控制 | ❌ | ✅ |
| **适合** | **人物多、资产多、跨镜一致性优先** | 需精确首尾构图的镜型 |

> ⚠️ **同一段落内不能混用。** 若某段既有需 9 图锁资产的镜、又有一个 #7 揭示镜，**该段必须整体走 FL2VA 并放弃 9 图资产锁**。
> **建议解法**：把 #7 揭示镜**单独拆成一次 FL2VA 请求**，其余镜走 Ref2VA，最后在剪辑台拼接。

### 10.2 四个参考标签的确切语法【官方】

> ⚠️ **不是** `<asset-1>` / `<subject-1>` / `<image-1>`。官方写法是**首字母大写 + 空格 + 数字**：

| 标签 | 官方含义 |
|---|---|
| `<Subject N>` | Visible content abstracted from reference assets that can be reused or modified in the target video |
| `<Picture N>` | A reference image used as a concrete target frame or shot-planning anchor |
| `<Video N>` | A reference video that provides an editing source, continuation starting point, or whole-video temporal structure |
| `<Audio N>` | An audio signal that is copied or referenced |

**官方例句**【官方】
```
<Subject 1> is the young woman in <Picture 1>, with long dark hair, a blue cardigan, and a thin
    silver necklace.
<Subject 1> is the woman whose appearance comes from <Picture 1> and whose walking motion comes
    from <Video 1>.
<Picture 2> is the first frame of [Shot 1], showing a woman seated beside a café window.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
```

> ⚠️ **写法差异（重要，需自查）**：官方 `ref-en.txt` 用的是 `<Picture N>` / `<Subject N>`；
> 而本流水线的 `H3单镜提示词模板_Ref2VA参考模式版.md` 示例里用的是 `<image_1>` / `<video_1>` / `<audio_1>`。
> **两者并存，官方口径以 `<Picture N>` 为准。** 若你的工程已沿用 `<image_1>` 且出片正常，可继续；
> 若要严格对齐官方，请全局替换。**API 是否对两种写法等价，未找到官方说明**【待验证】——
> 实测方法：同一提示词分别用两种写法各生成 5 次，对比人物一致性得分。
>
> **冲突对侧是 MiniMax 官方开源公告 API 脚本**（`<image_1>`，小写 + 下划线 + 序号），与 `ref-en.txt` 同属官方但口径不一。
> 采用 `ref-en.txt` 的理由：它出自 MiniMax 自有 GitHub 组织的**提示词写作专用指南**，与"怎么写提示词"直接对口；
> 公告脚本面向 API 调用示例，语境可能不同。**完整对照与替换映射见 `H3单镜提示词模板_Ref2VA参考模式版.md` 文首。**

### 10.3 六段结构与字数预算【官方】

| # | 字段 | 人物/资产相关的作用 | 预算 |
|---|---|---|---|
| ① | `subject_definitions` | 逐一点名每个参考文件**是什么**（哪张是脸、哪张是耳环） | 100–180 |
| ② | `summary` | 任务类型标签 + 一段话总览 | 60–120 |
| ③ | `retention_analysis` | **逐个文件指定保留强度 + 保留什么** ← 核心 | 180–320 |
| ④ | `detailed_description` | 主时间轴（风格串写在 `[Shot 1]` **之前**） | 每镜 250–400 |
| ⑤ | `overall_soundscape` | 环境音 | 60–150 |
| ⑥ | `non_diegetic_music` | 配乐或 `N/A` | 20–60 |

> 【官方】"For generation tasks, `detailed_description` is normally 350-500 English words."（非硬配额）

### 10.4 retention 保留强度标记决策表【官方 · "fixed English values"】

**视觉**（用于 `<Subject N>` / `<Picture N>` / `<Video N>`）

| 标记 | 官方含义 | **人物/资产场景下什么时候用** | 典型对象 |
|---|---|---|---|
| **`fully_preserved`** | 被引用内容的定义角色被完整保留 | **承载身份识别、观众会认的东西，一律用它** | 脸、发型、核心服装、关键道具（戒指/耳环/疤）、场景光位 |
| `partially_preserved` | 仍被使用，但部分定义特征被改变或只部分保留 | 允许随情境微调的 | 场景空镜（小道具可变）、外套的褶皱、发型松散度 |
| **`attribute_transfer`** | 引用特征被转移到另一个可识别的目标主体上 | **纯风格类参考，一律用它** | 画风参考、调色参考、材质参考、手部姿态参考、镜头运动参考 |
| `weak_reference` | 仅在风格、类别、构图或氛围上保持宽泛相似 | 只提供方向、不做约束 | 氛围板、情绪表情参考、构图倾向 |

**音频**（用于 `<Audio N>`）

| 标记 | 官方含义 | 人物/资产场景 |
|---|---|---|
| `fully_copy` | 完整源音频作为目标视频的完整最终音轨 | 复用整条 BGM |
| `partially_copy` | 只复制部分时间线或选定音层，或复制后有增删改 | 复用 BGM 并压低混音 |
| **`reference`** | 不直接复制信号，只参考音色、节奏、曲风、对白内容或声音质感 | **角色音色参考（最常用）** |
| `weak_reference` | 仅在类别或氛围上保持宽泛相似 | 氛围倾向 |

**官方条目格式**【官方】
```
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
<Picture 2> ([Shot 1] first frame): fully_preserved - ...
<Video 1> (cut and pacing structure): weak_reference - ...
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track.
<Audio 2>: reference - the target speaker follows <Audio 2>'s voice timbre and measured delivery
    without copying the original signal.
```

**背诵版规则**
```
脸 / 发型 / 核心服装 / 关键道具 / 身体标记  →  fully_preserved
场景空镜（小道具可变的）                    →  partially_preserved
画风 / 调色 / 材质 / 手部姿态 / 镜头运动    →  attribute_transfer
氛围板 / 情绪表情 / 构图倾向                →  weak_reference
音色 / BGM                                  →  reference / partially_copy
```

> ⚠️ **最容易犯的错**：把**画风参考图误用 `fully_preserved`**。后果是模型会把那张参考图里的**物体也搬进画面**（官方对 `attribute_transfer` 的定义就是"只迁移属性、不搬物体"）。**画风图一律 `attribute_transfer`。**

### 10.5 人物资产的 9 图分配表（推荐配置）

| 槽位 | 内容 | 保留强度 | 必填 | 说明 |
|---|---|---|---|---|
| 1 | 角色正面定妆（脸 + 发型 + 妆容 + 标记） | `fully_preserved` | ✅ | 锁脸的主锚点 |
| 2 | 角色侧面 / 45° | `fully_preserved` | ✅ | 锁面部几何，防正面像换人 |
| 3 | 角色全身（体型 + 服装版本 + 鞋） | `fully_preserved` | ✅ | 锁服装与体型 |
| 4 | 身体标记特写（疤 / 痣 / 胎记） | `fully_preserved` | 按需 | 承载叙事的标记必占一槽 |
| 5 | **随身资产特写**（耳环 + 戒指并置或分两张） | `fully_preserved` | 按需 | **一件资产锁一样东西** |
| 6 | 场景空镜（含光源方向） | `partially_preserved` | ✅ | 锁光位 |
| 7 | 画风 / 调色参考 | `attribute_transfer` | ✅ | **绝不能用 `fully_preserved`** |
| 8–9 | 手部姿态 / 第二角色 / 情绪表情 | `attribute_transfer` / `fully_preserved` / `weak_reference` | 按需 | 只迁移姿态或备用 |

> 💡 **成本提示**【官方】：前 5 张参考图免费，第 6 张起计费；视频参考按时长计费（最贵）；音频参考免费。**量产时优先用图片 + 音频，视频参考只留给"必须复刻某段镜头运动"的场合。**

### 10.6 完整人物锁定示例（Ref2VA，15 秒 3 镜）

```
subject_definitions:
<Picture 1> is <Subject 1>'s front-facing character sheet: a 28-year-old woman, oval face,
    shoulder-length straight black hair with slightly inward-curled ends, dark brown
    almond-shaped eyes, pale skin with natural visible texture, and a 1.5cm pale healed scar at
    the outer end of her right eyebrow.
<Picture 2> is <Subject 1>'s left three-quarter view.
<Picture 3> is <Subject 1>'s full-body reference, showing the ivory round-neck cotton T-shirt,
    the dark khaki long trench coat worn open, dark-wash straight-leg jeans and white low-top
    canvas shoes (costume version CH_01_OUT_A).
<Picture 4> is a close-up of the 1.5cm pale healed scar at the outer end of her right eyebrow.
<Picture 5> is the exact product reference for her two accessories: a single small silver hoop
    earring and a small matte-gold signet ring, photographed side by side.
<Picture 6> is the location empty plate: a light grey fabric sofa, a blank wall, and a floor
    lamp on the right that is the only light source.
<Picture 7> is the colour-grade and art-style reference.
<Picture 8> is the hand-pose reference: both hands resting flat, five fingers held together.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] The target video is a 15-second three-shot scene in a
night-time living room. <Subject 1> sits on the sofa, reads a letter, then looks up toward the
door. The visual style and colour grade follow <Picture 7>. The woman's voice references
<Audio 1>.

retention_analysis:
<Picture 1> (appears in [Shot 1], [Shot 3]): fully_preserved - she retains her exact facial
    identity, oval face, hair length and colour, eye shape, skin texture, age, and the 1.5cm
    pale healed scar at the outer end of her right eyebrow throughout, with only her mouth newly
    animated to speak.
<Picture 2> (appears in [Shot 1]): fully_preserved - the three-quarter view contributes only
    facial geometry.
<Picture 3> (appears in [Shot 1], [Shot 2]): fully_preserved - the ivory T-shirt, dark khaki
    trench coat worn open without the belt, dark-wash jeans and white canvas shoes remain
    unchanged in every shot, the coat staying open and on her shoulders throughout.
<Picture 4> (appears in [Shot 1], [Shot 3]): fully_preserved - the scar keeps its exact length,
    colour and position, staying visible and identical in every frame.
<Picture 5> (appears in [Shot 1], [Shot 2]): fully_preserved - exactly two accessories are
    locked: the small silver hoop earring stays on her LEFT earlobe and the small matte-gold
    signet ring stays on her RIGHT ring finger, each one keeping its size, colour and side
    from the first frame to the last.
<Picture 6> (appears in [Shot 1], [Shot 2], [Shot 3]): partially_preserved - the sofa, blank
    wall and floor-lamp position and the warm key-light direction from camera right are
    maintained; small props may vary.
<Picture 7>: attribute_transfer - only the muted teal-and-amber grade, contrast curve and film
    grain are adopted from this image.
<Picture 8> (appears in [Shot 2]): attribute_transfer - only the hand pose is adopted (both
    hands flat, five fingers held together, natural proportions).
<Audio 1>: reference - the target audio references the woman's voice timbre.

detailed_description:
Live-action, cinematic and photorealistic, in the muted teal-and-amber grade of <Picture 7>.

[Shot 1] A medium shot frames <Subject 1> seated on the sofa in the lower-left third of frame,
body angled three-quarters to camera, both hands resting flat in the pose of <Picture 8>. A few
loose strands of her hair shift in the still air, then she lowers her chin, then her thumbs
slide once along the edge of the letter. She stays silent with her lips closed. The warm
floor-lamp light holds steady on her cheek; the earring casts a small soft shadow on her neck
and the ring casts a thin shadow at the base of her right ring finger. The camera pushes in with
small amplitude at slow speed from a medium shot to a medium close-up. Lighting follows
<Picture 6>. By the end of the shot she is still looking down, framed chest-up, the sheet of
paper a blank surface marked only by folds and shadow.

[Shot 2] At 00:05.000, the camera cuts to a close-up of her right hand; the matte-gold signet
ring fills the upper-right of frame and stays on her right ring finger throughout. Her fingers
curl once, then the hand lowers to her lap, then it settles. The ring's soft contact shadow
stays visible on her skin. The camera holds a static shot. Lighting follows <Picture 6>. By the
end of the shot her right hand rests in her lap, five fingers held together in natural
proportions, the ring still visible.

[Shot 3] At 00:10.000, the shot switches to a medium close-up of <Subject 1> from the front.
She blinks once, then slowly raises her chin, then her gaze lifts to a fixed point beyond the
lens. The woman with a quiet, breathy voice (S1) says: <d>[Chinese] 我早就知道了。</d> Her
hair falls back over her left shoulder; the warm key light stays steady on her cheek and both
accessories remain visible. The camera holds a static shot. Lighting follows <Picture 6>. By the
end of the shot she holds a steady gaze beyond the lens, her face, costume and both accessories
identical to <Picture 1>.

overall_soundscape: A quiet night-time room tone, paper sliding against fabric, one slow
inhalation, the faint hum of a floor lamp.

non_diegetic_music: A single sustained cello note at a slow tempo, entering at the second shot
and fading out before the end.
```

> **本例要点回顾**：脸占 2 槽（正 + 45°）、服装占 1 槽、疤占 1 槽、两件配饰占 1 槽；
> 画风与手部姿态走 `attribute_transfer`；三镜都在正文里重复了接触阴影句与不变量声明。
> **整体约 1,900 汉字，仅用掉 7000 字符上限的 27%。**
>
> ✅ **本例全文零否定**：`retention_analysis` 与三镜正文只做正向锚定，无一句 `Do not` / `never` / `no X`。
> **每镜那 1 处否定额度因此完整保留**，留给该镜独有的一次性风险。逐镜复制的块，一处否定就是全剧代价。

### 10.7 Ref2VA 人物锁定的七条铁律【官方】

| # | 规则 |
|---|---|
| 1 | 标签一旦分配，全文六部分保持同一含义，中途不得重新定义 |
| 2 | **`retention_analysis` 里不得写 `(Sx)`** |
| 3 | 仅用于定义角色 / 场景 / 服装 / 风格的图片**不建**独立 `<Picture N>`，应引在 `<Subject N>` 定义里 |
| 4 | 参考视频带声音，不自动等于有了 `<Audio N>` |
| 5 | 新增的动作、背景、情节**不算**保真度损失，不要写进 `retention_analysis` 里去"补救" |
| 6 | 不要把描述简化成剧情摘要或参考关系清单 |
| 7 | `summary` 段**不得引入新的参考标签** |

### 10.8 Base 模式的备用方案（走 FL2VA 时）

无 `retention_analysis` 可用时，人物锁定退化为「描述串 + 2 张图」。此时**必须**做三件事：

```
① 把身份串、服装串、资产锁串写成完整锁定块，三镜逐字复制（见主模板 §6.3）
② 官方提供的角色一致性锁定句【官方】：
   ...the young woman shown in <Picture 1> remains beside the rain-covered train window,
   preserving her appearance, clothing, seat position, and the carriage layout.
③ 首尾帧各选一张：首帧用正面定妆、尾帧用同一套服装的全身照，
   并让两帧的光位一致（否则插值过程会"换脸"）
```

> 💡 **出稿后建议过一次 H3-Context-IR**（`POST /v2/h3_context_ir`）做 diff：把锁定块喂进去，取回 `content.prompt`
> 与你写的对照。若官方改写结果与锁定块差异显著，说明描述串可能没被模型按预期解析（详见主模板 §7.12）。

---

## 11. 一致性三锁

### 11.1 参考图锁
**定义**：同一角色 / 同一资产，全程复用**同一组**参考图，不换图、不补图、不用"差不多"的图。

| 规则 | 说明 |
|---|---|
| 一角色一组图 | 正面 / 45° / 全身三张是底线 |
| 换装必换全身图 | 服装版本 ID 变了，全身参考图同步换 |
| 图要"干净" | 纯色背景、单一光源、五官无遮挡、无文字水印 |
| 不混用不同画风的图 | 一张写实定妆 + 一张插画风 = 模型在两种风格间摇摆 |
| 用 ID 引用 | 登记进角色卡（`IMG_01`），不用文件名 |

```
✅ IMG_01 固定为 CH_01 正面定妆，全剧不换
❌ 第 12 集换了一张更像的定妆图     ← 这不是修 bug，是制造 bug
❌ 用剧集截图当下一集的参考图       ← 截图带场景光与运镜模糊，会污染锁定
```
### 11.2 描述串锁
**定义**：角色与资产的描述串做成**模板常量**，禁止临场改写、禁止同义替换。

执行三件事：① **单一事实源**——常量串存在一处（角色卡 / 资产表 / 常量文件），所有提示词从那里复制；
② **字符串比对**——三镜锁定块用 diff 工具验证逐字一致，不靠人眼；③ **变更日志**——改动必记。

**变更日志模板**

| 日期 | 对象 | 改前 | 改后 | 影响集段 | 全量重测 |
|---|---|---|---|---|---|
| — | `CH_01_OUT_A` | `dark khaki trench coat` | `dark khaki long-line trench coat` | E01–E60 | ✅ 是 |

### 11.3 参数锁

| 参数 | 锁定要求 | 为什么 |
|---|---|---|
| 种子 | 同角色相关镜头尽量用同一组种子 | 保证可复现 |
| 画幅 `ratio` | 全剧固定一档；`t2va` 必填且不能 `adaptive`【官方】 | 画幅变化改变构图与像素占比 |
| 分辨率 | 全剧固定 768p 或 2K，不混用 | 2K 经 H3-Regenerate-2K 得到，细节分布不同 |
| 采样步数 | 试拍 4 步、**出片 6–8 步**，记进分镜表 | 见 §11.4 |
| **主光方向与色温** | 记进场景表，全剧单一主光 | **主光换边，脸就跟着晃**——光照稳定是一致性的一半功力 |
| 画风串 | 全剧逐字复用 | 画风漂了，人物看起来就是另一个人 |

### 11.4 采样步数：先排除"伪翻车"
很多看起来像"提示词写错了"的问题，其实是采样步数太低。**返工顺序必须改成**：

```
① 抬采样步数（4 → 6–8）重跑同一条提示词        ← 先做这个
② 仍不合格 → 查硬阻断清单（§13.5）→ 改分镜绕开
③ 仍不合格 → 检查参考文件的保留强度标记（§10.4）
④ 仍不合格 → 才动提示词
```

> ❌ **禁止**：步数一直是 4，却反复改提示词。你改的每一版都是在低质量采样下评估的，结论不可靠。
### 11.5 变更控制：全剧统一改，不要只改一处
① **一次只改一处，改完全量重测**——同时改身份串和运镜，崩了不知道是谁的锅。
② 改了常量串 → 所有引用它的集段全部重新生成，不是"改完接着往下拍"。
③ 改之前先问：这是修 bug 还是为了"更好看"？**为"更好看"改常量串是最贵的返工**；能靠后期（调色 / 镜像）解决的，不动常量串。
④ E01 的常量串一旦通过验收就冻结，后续集数只引用、不修改。

> 三锁的具体勾选项并入 §13.1 提交前检查清单（㉘–㉜），此处不重复。

---

## 12. 资产复现测试法

### 12.1 为什么必须自测：**没有公开基准**
> ⚠️ **未找到任何公开来源给出"耳环复现成功率 = X%"这类数据。**
> 网上"某模型珠宝保真度优异"类说法均出自聚合站或营销软文，**无方法论、无测试集，不可引用**。

因此：① 不要相信任何外部的成功率数字；② 不要把 5 次观察当成成功率（样本量不足）；③ **必须自建测试**——用你自己的角色、参考图、画风串。测试对象只选**承载叙事信息**的资产。
### 12.2 测试设计

| 要素 | 要求 | 为什么 |
|---|---|---|
| **次数** | **≥ 20 次** | 低于 20 次，置信区间宽到没有决策价值 |
| **条件** | **必须在真实运动条件下测** | **静止画面测出的成功率没有意义**——见 §12.4 |
| 提示词 / 参考图 | 完全相同（只换种子） | 隔离变量 |
| 步数 | **6–8 步**（出片档） | 4 步测出的结论不可用 |
| 时长 / 景别 | 与量产一致（15s）；覆盖该资产实际出现的景别 | 时长越长漂移越大；特写下稳不代表中景下稳 |

**测试对象优先级**：只测**承载叙事信息**的资产（观众必须认出来才能看懂剧情的物件）。装饰性资产不必测。

### 12.3 两个自测指标
> 【工程取值】这两个指标名在本流水线中作为自测口径使用；**未找到公开的标准化定义与行业基准值**，阈值 80% 是工程取值，可用你自己的数据覆盖。

| 指标 | 全称 | 定义 |
|---|---|---|
| **PPR** | Prop Persistence Rate（道具持续率） | 该物件在**整条视频每一帧**都存在的生成次数占比 |
| **WLR** | Wardrobe Lock Rate（服装锁定率） | 整套服装在**每一帧**保持颜色、材质、层数不变的生成次数占比 |

```
PPR = （物件全程存在的生成次数 ÷ 总生成次数）× 100%
WLR = （服装全程未变的生成次数 ÷ 总生成次数）× 100%
目标：≥ 80%【工程取值】
```
**怎么判"全程存在"**：不必真看 360 帧，**抽查 6 个采样点**——第 1 帧、25%、50%、75%、末帧，外加动作幅度最大的一帧。**任一帧**物件消失 / 变形 / 换边即判失败。
### 12.4 为什么静止画面测出的成功率没有意义
| 静帧条件 | 真实运动条件 |
|---|---|
| 模型只需解一次构图 | 模型要在 360 帧里持续维护同一状态 |
| 无运动模糊、无遮挡 | 头部转动 → 耳环被头发遮挡后**能否长回来**才是关键 |
| 无注意力竞争 | 动作、运镜、环境都在抢注意力预算 |
| 结果：**虚高** | 结果：**才是真实值** |

> **耳环最常见的失效不是"一开始没有"，而是"转头后没长回来"。** 这种失效只在运动条件下暴露。
### 12.5 测试记录表模板

| 资产ID | 名称 | 次数 | 提示词版本 | 参考图ID | 步数 | 景别 | 通过次数 | **PPR** | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| AS_07 | 银色耳环 | 20 | v1.2 | IMG_05 | 8 | 中近景 + 转头 | \_\_ | \_\_% | \_\_ |
| AS_08 | 金色戒指 | 20 | v1.2 | IMG_05 | 8 | 手部特写 | \_\_ | \_\_% | \_\_ |
| — | `CH_01_OUT_A` 整套装 | 20 | v1.2 | IMG_03 | 8 | 全身 + 走动 | \_\_ | \_\_%（WLR） | \_\_ |

### 12.6 处置规则

| 实测成功率 | 处置 | 具体做法 |
|---|---|---|
| **≥ 90%** | ✅ **可承载叙事信息** | 正常使用，可让观众靠它认人（"凶手戴着金戒指"） |
| **80% – 90%** | ⚠️ 可承载，**但要有冗余** | 同一次识别给两个证据（戒指 + 疤同时入画），一个丢了另一个还在 |
| **70% – 90%** | ⚠️ **不得承载叙事信息** | 可出现、可增真实感，但**观众认不出也不影响剧情** |
| **< 70%** | ❌ **砍掉或替换** | 换更低风险的特征：耳环识别 → 红围巾识别；眉疤识别 → 颈部胎记识别 |

> **目标线**【工程取值】：**≥ 80%**。低于 80% 的资产进入"替换"评估流程。

### 12.7 什么时候必须重测

| 触发事件 | 是否重测 |
|---|---|
| 量产开始前 | ✅ 必测 |
| 换 H3 模型版本 / API 供应商 / 画风串 / 分辨率档（768p ↔ 2K） | ✅ 全量重测 |
| 换参考图 / 改角色常量串 | ✅ 重测该资产 |
| 只改动作 / 运镜 / 台词 | ❌ 可不重测 |

### 12.8 成本提示
20 次 × 15 秒 × 2K ≈ $39（按 $0.13/秒估算【官方】），约等于一次中等返工成本的 1/10。**测比不测便宜，边拍边测最贵。**
## 13. 检查清单 + 正反例速查表

### 13.1 提交前检查清单（32 条）

**人物分层**：① 主角身份串 80–150 汉字 / 50–80 英文词，进锁定块；② 配角 25–50 汉字且至少拉开 2 维差异；③ 配角每人只给一个动作；④ 路人只写"虚化 + 数量 + 无五官"；⑤ 人数写死且在该镜第一句。

**外貌皮肤**：⑥ 无抽象形容词；⑦ 至少一项独有特征；⑧ 年龄写数字；⑨ 瞳色在景别下可见才写；⑩ 稳定标记给位置 + 尺寸 + 颜色 + 不变量声明。

**伤口标记**：⑪ 四要素齐全；⑫ 阶段词选颜色稳定的（healed / old / faded）；⑬ 多阶段每阶段一个版本 ID；⑭ 义肢已按 §7.6 评估或已替换设计。

**服装资产**：⑮ 服装五要素齐全；⑯ 纯色 + 哑光 + 无标识；⑰ 版本 ID 正确、集段不混用；⑱ 镜头内无穿脱/系扣动作；⑲ 资产四要素 + 接触阴影句；⑳ 本镜小物件 ≤2 件（§9.1–§9.5）。

**逐字一致 + 正向**（字符串比对，不用人眼）：㉑ 三镜锁定串逐字一致；㉒ 与角色卡常量串逐字一致；㉓ 锁定块零否定、每镜否定 ≤1 处（方位消歧除外，§9.2）。

**Ref2VA**：㉔ 未同现 `first_frame`/`last_frame` 与 `reference_*`；㉕ 每个参考文件两段都被点名；㉖ 脸/发型/服装/关键道具 = `fully_preserved`，画风/调色/材质 = `attribute_transfer`；㉗ `retention_analysis` 里没有 `(Sx)`。

**参数流程**：㉘ 参考图未换、ID 一致；㉙ 主光与色温同场景表；㉚ 出片步数 6–8；㉛ 高价值资产已测 ≥20 次并登记 PPR/WLR；㉜ 改了常量串已记日志并安排全量重测。
### 13.2 生成后看片清单（人物与资产专项，8 条）

```
□ 1. 脸：三镜对比是不是同一个人（发型 / 五官 / 年龄 / 独有特征）；疤、痣、胎记每镜都在且没漂位
□ 2. 服装：颜色、材质、层数三镜一致；外套开合状态没变
□ 3. 小物件：耳环 / 戒指 / 手表在不在、有没有换边；**接触阴影在不在**（阴影消失往往先于物件消失）
□ 4. 光照：三镜主光方向一致（换边 = 换人观感）
□ 5. 人数与路人：有没有多出/少掉一个人；路人有没有从虚化变清晰、从 3 个变 5 个
```

### 13.3 正反例速查表

| # | 项目 | ❌ 反例 | ✅ 正例 | 原因 |
|---|---|---|---|---|
| 1 | 身份声明 / 年龄 | `a beautiful woman`；`a young man` | `a 28-year-old woman with an oval face`；`a 35-year-old man` | 抽象词自由填空；"young" 是区间 |
| 2 | 发型 / 瞳色 | `nice hair`；`eyes that look sad` | `shoulder-length straight black hair, centre-parted`；`dark brown almond-shaped eyes` | 长度最好抓；情绪不是外貌 |
| 3 | 肤色 / 妆容 | `porcelain skin`；`she wears makeup` | `pale skin with natural visible texture`；`minimal natural makeup, unchanged throughout` | 比喻无确定指向；浓淡必须写死 |
| 4 | 痣 | `a mole somewhere on her face` | `a 2mm dark brown mole just above her left collarbone` | 位置不确定 = 随机长 |
| 5 | 伤口 | `she has a scar`；`a healing cut` | `a 1.5cm pale healed scar at the outer end of her right eyebrow`；`a healed scar` | 四要素；愈合中 = 颜色在变 |
| 6 | 义肢 / 纹身 | `she has a prosthetic left forearm`；`a full-colour sleeve tattoo with koi and kanji` | 换成"长袖遮住 + 手套"或仅静态中远景；`a solid black band about 4cm wide around his left upper arm` | 结构崩坏非物件丢失；复杂度决定风险 |
| 7 | 锁定块里的否定句 | `never removed, never duplicated, never changes hand` | `staying on that same finger for the entire shot, one ring on one finger only` | 逐镜复制，1 处否定吃光全剧每镜的额度（§9.2） |
| 8 | 服装 | `casual clothes` | `an unbranded ivory cotton T-shirt and dark-wash straight-leg jeans` | 抽象 |
| 9 | 材质 / 图案 | `a silk dress`；`a plaid shirt` | `a matte cotton dress`；`a plain charcoal shirt` | 反光随光变；格子/条纹运动中必崩 |
| 10 | 层数 / 穿着方式 | `a coat`（没写里面）；`a trench coat` | `a white shirt under a charcoal wool coat`；`a trench coat worn open without the belt` | 不写内层 = 自由发挥；不写穿法 = 中途扣上 |
| 11 | 服装动作 | `she takes off her coat` | `her coat is already off, draped over the chair` | 布料 + 层数 + 手部三重风险 |
| 12 | 配饰数量 / 位置 | 一镜写耳环+项链+戒指+手链+发卡；`she wears an earring` | 一镜只锁 2 件；`a single small silver hoop earring on her LEFT earlobe (on the left ear, not the right)` | 注意力预算有限；防左右互换 |
| 13 | 接触阴影 / 不变量 | `she wears a gold ring` | `a thin soft shadow falls across the skin at the base of the ring`；`staying on that same finger for the entire shot, one ring on one finger only` | 阴影是位置证据；模型默认东西可以变 |
| 14 | 逐字复用 | `black hair` / `dark hair` / `raven hair` 混用 | 三处全部 `straight black hair` | Verbatim Rule |
| 15 | 双人描述 | `two men in suits` | `a tall man in a charcoal coat (left of frame) and a shorter woman in a khaki trench coat (right of frame)` | 对称描述诱导融合 |
| 16 | 方位 / 人数 / 路人 | `on her left`；`a woman sitting on the sofa`；`three people in the background, one in a red jacket` | `on the left third of frame`；`Exactly ONE person in frame`；`exactly three blurred figures, out of focus` | 有歧义 / 会漂移 / 给了细节（§4.4–§4.6） |
| 17 | 保留强度 / 标签 / 换图 | 画风图用 `fully_preserved`；`retention_analysis` 写 `(S1)`；`<image-1>`；中途换定妆图 | 画风图用 `attribute_transfer`；不写 `(Sx)`；`<Picture 1>` / `<Subject 1>`；全剧固定 IMG_01 | 见 §10.2、§10.4、§10.7、§11.1 |

### 13.4 故障 → 处置对照表
| 现象 | 最先怀疑 | 处置 |
|---|---|---|
| 三镜脸不一样 | 步数 4 / 锁定块被改写 / 光位换了 | 抬步数 → 字符串比对 → 查光位 |
| 耳环转头后没长回来 | 头发遮挡后状态未恢复 | 加参考图；改发型（别到耳后）；换更大耳饰 |
| 戒指换手 / 长出两只耳环 | 位置写成 `her right`；缺"仅此一只"的正向不变量声明 | 改 `on her RIGHT ring finger (worn on the right hand, not the left)`；补 `one ring on one finger only, staying on that finger for the entire shot` |
| 疤不见了 | 面积太小 / 被磨皮 / 侧逆光 | 换大面积标记 → 正面 45° 主光 → 走参考图 |
| 服装颜色中途变 | 服装串没进锁定块 / 步数 4 | 服装串并进锁定块逐字复制 → 抬步数 |
| 两人越来越像 / 第 12 集与第 1 集不一样 | 描述对称；参考图或常量串中途被改 | 按 §4.3 四维表拉开；查变更日志 → 回滚 → 全量重测 |

### 13.5 人物与资产相关的硬阻断清单（提示词解决不了，改分镜绕开）

| 问题 | 为什么解决不了 | 绕开方案 |
|---|---|---|
| **小物件纯文本复现**（耳环 / 纹身 / 疤） | 像素占比低、无持续状态跟踪 | **必须走参考图**（I2VA / Ref2VA）；或换成大面积标记 |
| **跨请求的左右方位 / 180° 轴线 / 正反打朝向** | 每次生成为独立采样，无空间状态传递 | 后期水平镜像；或把三镜放进**同一次请求** |
| **物理接触 / 碰撞 / 液体 / 布料大幅飘动** | 结构性缺陷（ICML 2025：模型抄训练样本而非推理物理） | 改写剧本避开 |
| **小尺度精确对准**（戴耳环、系扣、指尖对位） | 无 3D 朝向跟踪与刚体约束 | 避开极端特写 |
| **义肢的结构性稳定** | 属"肢体轮廓与关节结构"问题 | 改剧本；或仅静态中远景 |

> **遇到这几类，第一反应是改分镜，不是改提示词**——把"她摘下耳环递给他"改成"耳环已经在桌上"，一秒解决；硬写提示词，十次也过不了。另：纹身与服装上**不要写字母**（§7.7、§8.5）。

### 13.6 处置四级枚举（与主模板 §8.6 一致）

按序选，别一上来就重写提示词：**规避**（把"摘耳环"改成"耳环已在桌上"）→ **降级**（戒指保留但不作身份证据）→
**后置**（跨请求左右方位后期镜像）→ **重生成**（概率性崩坏时抬步数 / 换种子）。

---

## 14. 参考来源

| 标记 | 来源 | 性质 |
|---|---|---|
| 【官方】A / B | `github.com/MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/base-en.txt`、`ref-en.txt` | MiniMax 官方仓库 |
| 【官方】C | `platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir` | 官方 API 文档 |
| 【官方】D | `huggingface.co/MiniMaxAI/MiniMax-H3` | 官方模型卡 |
| 【官方】E | `docs.comfy.org/tutorials/video/minimax/minimax-h3` | ComfyUI 官方文档 |
| 【业界】 | arXiv 2512.16954（视觉锚定消融实验） | 单篇论文，自定指标 |
| 【工艺】/ 内部 | `防翻车限制词库_H3版.md` §7、§10；主模板模块五 / 六 / 七；`H3单镜提示词模板_Ref2VA参考模式版.md` | 本流水线内部 |

> **引用纪律**：对外交付只引用 A–E（MiniMax 自有域名与仓库）。引 arXiv 2512.16954 时必须说明"自定指标、非 H3 专属"。**任何"复现成功率 X%"的说法一律不引用、不传播。**

---

## 15. 一句话速查

```text
身份串：The same <woman> appears in every shot: <age>, <face>, <hair>, <brows+eyes>, <nose+lips>,
        <chin>, <skin>, <signature>. She wears <outfit>. Her appearance remains identical throughout.
四要素：颜色 + 材质 + 固定位置 + 不变量声明（正向写：staying in place / one only / unchanged）
接触阴影：A thin soft shadow falls across the skin at the base of the ring.
锁定块：100% 正向，零否定——逐镜复制，1 处否定吃光全剧每镜的额度（§9.2）
一镜小物件 ≤2 件；每角色标志性配饰 ≤2 件
风险：义肢 ＞ 纹身 ＞ 耳环/戒指 ＞ 手表/手机 ＞ 大面积衣物/围巾
保留强度：脸/发型/服装/关键道具 → fully_preserved；画风/调色/材质 → attribute_transfer
标签：<Subject N> <Picture N> <Video N> <Audio N>（首字母大写 + 空格 + 数字）
三锁：参考图锁 × 描述串锁 × 参数锁（乘法关系）
测试：≥20 次、真实运动条件、6–8 步、PPR/WLR、目标 ≥80%
处置：≥90% 可承载叙事｜70–90% 不得承载｜<70% 砍掉或替换
返工：抬步数 → 查硬阻断 → 查保留强度 → 最后才改提示词
```