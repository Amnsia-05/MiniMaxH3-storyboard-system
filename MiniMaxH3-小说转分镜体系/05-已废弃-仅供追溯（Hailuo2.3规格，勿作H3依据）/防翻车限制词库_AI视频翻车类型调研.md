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

# AI 视频生成「防翻车限制词库」调研报告

> 面向：小说 → 15 秒 3 镜分镜 → 海螺 H3 视频提示词工业模板
> 证据分级：**A**＝官方文档｜**B**＝可查第三方技术文档/学术论文｜**C**＝一线实操博客/社区共识（弱证据，已逐条标注）
> 原则：宁可写「这个解决不了」，不给假方案。

---

## 0. 前置结论：负向提示词在 H3 上有没有用（客户点名争议）

**事实层（B 级）**
- Hailuo 2.3 / 2.3 Fast 的 API **不提供 `negative_prompt` 字段**。第三方接入文档（geekai.co 的 MiniMax-Hailuo-2.3 页）把 `negative_prompt` 与 `with_audio / size / quality / aspect_ratio / fps / image_tail` 并列为「不支持参数」。fal.ai 的 Kling V3 Pro vs Hailuo 2.3 Pro 对照表同样标注：Hailuo 侧 "Negative prompt: Not available"，Kling 侧 "Supported"。
- Hailuo API 的 prompt 上限为 **2000 字符**；Hailuo 2.3 图生视频**只支持首帧单图**，`image_tail`（首尾帧）不支持（Hailuo 02 支持）。
- Hailuo 全系**不生成音频**。

**关于「不要六指反而激活六指」——有依据，但要分场景说**
1. **写在正向提示词里：基本成立。** 提示词工程文档（picassoia）原文："The model does not parse negation in plain English. Writing 'no extra fingers' in your positive prompt is largely ignored." 即否定词被弱化，而 "extra / fingers" 这些词本身进入了条件分布。
2. **写在真正的负向字段里（Kling/SD 系）：有效，但是概率推离而非硬保证。** 有实操记录（ageofllms 的 Kling Prompt Guide）报告把 "cars" 放进负向字段后「毫无效果，某些情况下反而出现更多车」，且负向提示词「从未能解决 disfigurement」。另一份文档（ai-tldr）给出机制解释：负向提示只对模型有强内部表征的概念（blurry、watermark、extra fingers）稳定生效；60 词的通用负向列表会**稀释转向力**，短而准的负向列表胜过长而全的。
3. **H3 上的唯一路线**：把「不要 X」改写成**正向等价 + 状态锁定**，用占据描述位的方式挤掉畸形解空间。例：把「不要六指」改成「双手自然下垂贴于裤缝，十指自然弯曲并拢，每只手五根手指」。

**实操裁定**：H3 提示词里禁止出现成串的 "不要……不要……"。最多保留 3–5 条硬约束，且必须写成正向状态句。

---

## 1. 手部异常（六指/多指/断指/融合/穿模）

**成因**：手在画面中像素占比小、姿态组合极多、训练覆盖不足；Hailuo 2.3 官方向指南把「手部交接物体」列为最高危动作。

**规避**：三档降级 —— ① 让手出画或被遮挡；② 让手静置并给出明确静态姿态；③ 用「无接触传递」替代「递/接」。注意反直觉的一点：**手部特写比中景全身稳**（像素占比越大越稳）。

**可直接复制**
- 出画/遮挡：`both hands tucked in coat pockets, fingers not visible`｜中：双手插在大衣口袋里，画面中看不到手指
- **静置锁定（客户要的正向写法）**：`her arms hang naturally at her sides, fingers gently curled and held together, five fingers on each hand, holding this exact pose throughout the shot`｜中：她双臂自然下垂贴于裤缝，双手手指自然弯曲并拢，每只手五根手指，全程保持这一姿势不变
- 大物体握持（比空手稳）：`both hands wrapped around a large ceramic mug, fingers fully hidden behind the mug`
- **无接触传递**（B 级，指南原文推荐）：用 `slides the cup across the table toward her` 替掉 `hands her the cup` —— "Contact-free transfers sidestep the hardest hand problem."
- 景别降级：`medium shot framed from the waist up, hands below the frame line`
- 负向（**仅对 Kling/SD 系负向字段有效，H3 不要指望**）：`extra fingers, fused fingers, missing fingers, mutated hands, six fingers, deformed hands, malformed limbs`

---

## 2. 肢体与人体结构（多余肢体/关节反折/人数失控）

**成因**：模型没有骨架与关节约束；并行多动作 + 对称描述 → 人物融合、解剖撕裂。

**规避**：人数写死 + 单人单动作 + 用「然后」排序而非「同时」并行（Hailuo 2.3 指南明确：并行三动作会破坏 anatomy）；对称描述（如 "two men in suits"）会诱导人物融合。

**可直接复制**
- `exactly one person in frame. She sets the cup down, then turns around — one action at a time, never simultaneously`｜中：画面中只有一个人。她先放下杯子，然后转身，一次只做一个动作
- `arms straight at the elbows, both shoulders level, head aligned with the spine, no extra limbs`｜中：双臂肘部伸直不外翻，双肩齐平，头部与脊柱对齐，无多余肢体
- 双人区分的正例（B 级原文）：`a tall man in a red apron and a short woman in a denim jacket`；反例：`two men in suits`

---

## 3. 镜头不流畅（跳切/运镜突变/主体漂移/结尾抖动）

**成因**：运镜指令堆叠被平均化 → 混乱漂移；动作在第一帧就做完 → 后半段空转抖动。

**规避**：**一个镜头只给一条运镜指令**；Hailuo 对靠前 token 权重更高，**运镜句必须前置**；给动作一个有终点的边界；给镜头加一个「前摇」拍子。

**可直接复制**
- 前置运镜（B 级原文："a leading 'Static tripod shot:' is obeyed far more often than a trailing one"）：`Static tripod shot: she looks at the letter, then slowly tears it open.`｜中：固定机位三脚架镜头：她先看着信停顿一秒，然后才慢慢撕开
- 单运镜白名单：`slow push-in` / `orbit around` / `tracking shot` / `static tripod shot`；**反例（必崩）**：`pan then zoom then tilt`
- `locked-off camera, no camera shake, no zoom, no cut, single continuous take`｜中：机位锁死，无晃动、无变焦、无剪辑，一镜到底
- 官方方括号指令（Hailuo 2.3 支持 15 个，同一括号内最多 3 个并发）：`[Static shot] [Push in] [Pull out] [Pan left/right] [Tilt up/down] [Truck left/right] [Pedestal up/down] [Zoom in/out] [Shake] [Tracking shot]`

---

## 4. 身份漂移（脸变/服装变色/发型变/年龄变）

**成因**：模型无长期记忆，每次生成为独立任务；误差逐帧累积。

**规避（关键：提示词只能减缓，不能根治）**。真正的解法是视觉锚定 —— arXiv 2512.16954 的消融实验：去掉 I2I 种子帧锚定后，角色一致性分数从 **7.99 崩到 0.55**。Veo 3 侧一线数据：每个镜头**逐字复制**完整角色描述（Verbatim Rule），一致性差异可达 40%。

**可直接复制**
- **角色锁定块（三镜逐字复制，一个字不改）**：`the same person throughout, identical face in every frame: 28-year-old East Asian woman, long straight black hair in a low ponytail, dark brown eyes, slightly thick eyebrows, small nose, rounded chin, small mole at the left brow tail; wearing a white crew-neck cotton T-shirt (slightly loose), dark blue slim jeans (cuffed), white canvas shoes.`
- 中：同一人物，全程同一张脸：28 岁东亚女性，黑色长直发扎低马尾，深棕色眼睛，眉毛略粗，鼻梁小巧，圆下巴，左眉尾一颗小痣。身穿白色圆领纯棉 T 恤（微宽松）、深蓝修身牛仔裤（裤脚挽起）、白色帆布鞋。
- `face unchanged from the first frame to the last, same hairstyle, same clothing color, no outfit change, no aging, no makeup change`
- 光照稳定（一致性的一半来自光照）：`single soft key light from camera left, color temperature locked at 5600K, no lighting change during the shot`
- **硬约束承认**：跨镜头严格身份一致，纯提示词做不到。必须首帧/参考图锚定（Chain Continuity：主镜头第一帧 → 所有镜头从同一帧衍生）。Hailuo 2.3 只有**首帧单图**，无主体参考、无多参考图、无首尾帧 —— 这是模型硬限制，不是写法问题。

---

## 5. 语言与文字错误（乱码招牌/字幕/短信/口型/语种）

**成因**：模型把文字当像素图案，没有字形与字符结构规则。Hailuo 2.3 被明确定位为「不是排版模型」。

**规避**：采用 **clean-plate rule（干净底板 + 后期贴图）**，不要在模型里生成任何必须正确的文字。

**可直接复制**
- `a smartphone with a dark blank screen, no text visible anywhere in frame, no signage, no subtitles, no watermark, no letters`｜中：一部屏幕纯黑的手机；画面任何位置不出现文字、招牌、字幕、水印、字母
- 唯一值得冒险的画面内文字（B 级）：单个大词、正对镜头、3 秒内、静止表面；或本就不需要被读懂的背景招牌。
- **口型与台词同步 / 对白语种：Hailuo 不生成音频轨，因此不可能靠提示词解决。** 必须后期（Wav2Lip 类唇形同步 + 配音）。"语种串台"在无音频模型中不存在；若要口播，全部走后期。

---

## 6. 物理与空间违和（穿透/重力/液体布料/距离不一致/左右翻转）

**成因**：结构性缺陷。Kang et al., ICML 2025（ByteDance/清华）《How Far is Video Generation from World Model》：模型遇到陌生场景不是推理物理，而是**抄最接近的训练样本**，只看颜色与尺寸等表层线索，结论原文 "scaling alone is insufficient"。VGI-Bench（arXiv 2608.19583）补充：即使给「oracle prompt」把正确解法完整写清楚，提升也很有限。

**规避**：能避就避，避不开就后期/实拍/3D。提示词只做减伤。

**可直接复制**
- 改写而非硬刚：`pouring water into a glass` → `a filled glass of water resting on the table, a pitcher beside it`｜中：「往杯子里倒水」→「装满水的玻璃杯静置在桌上，旁边放着一只水壶」
- 弱约束词：`physically plausible motion, obeys gravity, objects rest fully on the table surface, solid contact, no floating objects, no interpenetration, no sudden disappearance`
- **次级运动必须命名**（Hailuo 有效；不命名就得到静态道具）：`her coat whips in the wind, steam curls off the mug, water sloshes over the rim`
- 朝向/左右翻转（已知高发，社区报告集中在手机正反面翻转、钥匙对不准锁孔、车门从铰链侧打开）：`the phone's front screen faces the camera at all times and never flips to the back panel`｜中：手机正面屏幕全程朝向镜头，任何时刻不翻转为背面。更可靠的做法：**避开小尺度对准的极端特写 + 用参考图锚定朝向 + 多条里挑一条**。

---

## 7. 道具与资产丢失（耳环/手表/手机/眼镜忽有忽无、左右手调换）

**成因**：小物件像素占比低，模型无持续状态跟踪。VGI-Bench 把 "object/state inconsistency"（物体消失、变形、回退到早先状态）列为主要失败模式。

**规避**：减少数量 + 提高对比度 + 每镜重复 + 位置写死 + 补一句接触阴影。

**可直接复制**
- `a small silver hoop earring on her left ear, present in every frame, never removed, never switching ears`｜中：左耳垂一只银色小圆环耳环，全帧可见，不摘下、不换到另一只耳朵
- `a slim silver watch on her left wrist, watch face on the outer side, position fixed throughout the shot`｜中：左手腕一只银色细带手表，表盘朝向手背外侧，全程位置不变
- **接触加固**（写了阴影更不容易消失）：`the watch sits flush against her wrist skin, casting a small shadow on the skin beneath it`
- `no jewelry appears or disappears, no prop swaps hands, no object changes position between frames`
- 数量原则（B 级）：饰品「少而重」，一个高对比锚点（红色外套、银色吊坠）比一堆细节更能锁住一致性；复杂花纹与反光材质帧间变异率最高。同时写「耳环+项链+戒指+手链+发卡」几乎必然丢 1–2 件。

---

## 8. 多镜头生成的特有问题（风格光照不统一/节奏错位/重复起手动作）

**成因**：每个镜头独立采样，无共享状态；动作默认从静止起手，导致后一镜重复前一镜的起手动作。

**规避**：共享锁定块 + 明确「续接」而非「重启」。

**可直接复制**
- 三镜共用同一段「角色锁定块 + 风格锁定块 + 光照锁定块」，**逐字复制，一字不改**。
- 起始状态续接：`continuing from the previous shot: the phone is already raised to her chest, her eyes still on the screen; this shot only performs a slow push-in`｜中：（承接上一镜）她已把手机举到胸前，视线仍落在屏幕上；本镜只做缓慢推近
- 防重复起手：`no repeated setup motion, the action begins mid-gesture, entering the shot already in motion`｜中：不重复起手动作，镜头开始时人物已在动作进行中
- 光照统一：`same lighting setup and color grade as the previous shot: soft key from camera left, 5600K, muted teal grade`
- **时间码无效**：模型不解析「第 2 秒」「持续 5 秒」这类秒数，节奏只能靠剪辑实现。（Hailuo 2.3 支持 6s / 10s，1080p 仅 6s；15 秒 3 镜建议 5+5+5 或 6+6+3 拼接。）
- **硬约束承认**：跨镜头光照与风格的完全一致，纯提示词做不到，必须靠共享首帧/参考图 + 后期统一调色。

---

## 9. 手机屏幕内容处理（客户重点）

**成因**：屏幕 = 文字 + UI + 动态刷新三重叠加，是当前模型最不稳的区域。

**业界通用做法（B 级，多来源一致）：不在模型里生成屏幕内容。** 三档方案：

**方案 A（推荐，零风险）—— 干净底板 + 后期屏幕替换**
- 生成时：`she holds a phone with a blank dark screen; a soft cool-white glow from the screen lights her face from below. No text, no UI, no icons visible on the screen.`｜中：她握着一部屏幕纯黑的手机；屏幕发出冷白光，从下方打亮她的脸。屏幕上不出现任何文字、图标或界面。
- 后期：剪辑软件做屏幕替换（平面跟踪 / corner pin），把聊天记录贴图合成上去。像素级稳定、可改字、可换语言。

**方案 B（次选，画面里「有那么回事」但不需可读）—— 目前最实用的降要求写法**
- `the phone screen casts a cool white glow onto her face; the screen content is softened by motion blur and reflection, illegible`｜中：手机屏幕发出冷白微光映在她脸上，屏幕内容被运动模糊与反光柔化，**不可辨认**
- 原理：把「不可辨认」写进提示词，模型就不再去赌字形，观众也读不出错字。

**方案 C（必须读得出时）**：先用图像模型生成一张带正确文字的静态手机界面图，作为**首帧**上传做图生视频，提示词只写「屏幕内容保持不变 + 轻微手指滑动」。即便如此文字仍会漂移，短视频可接受，长镜头不行。

**明确三个坑**：① 不要在提示词里写短信原文，写了必乱码；② 不要用极端特写怼屏幕；③ 手机正反面翻转是已知高发项（见第 6 节）。

---

## 10. 小物件一致性锁定写法（客户重点）

三条原则：**每镜重复逐字不改**（同第 4 节 Verbatim Rule）｜**位置 + 材质颜色 + 对比度三件套**｜**一个镜头内必须稳住的小物件不超过 2 件**。

**可直接复制的模板**
- `WARDROBE LOCK: [item], [material+color], worn on [exact side/position], visible in every frame, unchanged in position, size, and color from the first frame to the last.`
- 中模板：服化道锁定：银色圆环耳环，左耳垂，全帧可见；从第一帧到最后一帧，位置、大小、颜色完全不变。
- `no jewelry appears or disappears, no prop swaps hands, no object changes position between frames`｜中：饰品不会忽有忽无，道具不会左右手调换，物件不会在帧间改变位置
- 接触句（对抗"消失"最有效的一句）：`the watch sits flush against her wrist skin, casting a small shadow on the skin beneath it`

---

## 11. 长提示词的组织方法

**先说一个与「1200–2500 汉字」设想冲突的坏消息（B 级，需官方交叉验证）**
Hailuo 系列的实测甜点区是 **40–70 个英文词**（约合中文 80–150 字）。versely《Hailuo 2.3 Prompting Guide》原文："Under 25 words, the model invents details you didn't ask for... Over 100, instructions start dropping — usually the camera line first, then the second half of the action." 也就是说，**单条提示词写到 1200–2500 汉字，模型几乎必然丢指令，而且最先丢的正是运镜**。（MiniMax 官方只公布 2000 字符上限，未公布甜点区；以上为第三方实测。）

**推荐结构：不写一条长提示词，写「一个三段式模板 + 三条短提示词」**
- 单条控制在 **150–300 汉字**，三段：
  1. **【锁定块】**（放最前，约占 1/3 篇幅）：角色 + 服化道 + 场景光照。三镜逐字复制。
  2. **【动作块】**（约 1/3）：一个动词，有起点有终点，用「然后」不用「同时」。
  3. **【运镜 + 收尾约束】**：运镜句**前置到句首**，约束句置尾。
- 若必须写长：**关键指令放最前和最后，次要信息放中间**（长上下文首尾注意力高于中部，lost-in-the-middle 现象）。
- 减字技巧（Seedance 侧实测，可迁移）：合并同质描述 —— 「深蓝制服 + 银警徽 + 黑对讲机」替掉三句话；删冗余标点与空格可省 8–12% 字符；超过 30 字的环境描写外置为参考图/参考素材，提示词里只写引用。
- 优先级排序：**角色/物件锁定 > 单一动作 > 运镜 > 风格 > 情绪**。风格词与情绪词最容易挤掉前面的硬约束，务必最短。

---

## 12. 明确「提示词解决不了」的清单（对客户零编造）

| 问题 | 现状 | 唯一可行方案 |
|---|---|---|
| 屏幕/招牌/字幕文字正确 | 无模型能保证帧间稳定 | 干净底板 + 后期贴图 |
| 口型与台词同步、对白语种 | Hailuo 不生成音频 | 后期唇形同步 + 配音 |
| 跨镜头角色身份严格一致 | 提示词仅减缓（实测约 +40%），不根治 | 首帧/参考图锚定（Hailuo 2.3 仅首帧单图，无主体参考、无首尾帧） |
| 物理接触/碰撞/液体/布料 | 结构性缺陷（ICML 2025 论文结论） | 改写剧本避开 + 实拍/3D + 后期 |
| 小尺度精确对准（钥匙插锁、指尖对位） | 高失败率 | 避开极端特写 + 多条挑选 |
| 手机正反面翻转 | 已知高发 | 参考图锚定 + 多条挑选 + 后期 |
| 长提示词（>100 英文词）不丢指令 | 做不到 | 拆镜、拆段、锁定块复用 |

---

## 13. 给 H3 模板的「全局限制词尾缀」（可直接复制）

**EN（约 70 词，挂在每条提示词末尾）**
> Single continuous take, locked-off camera, no cuts, no zoom, no camera shake. Exactly one person in frame, no extra people, no extra limbs, five fingers on each hand, natural joints. Face, hairstyle, clothing color and all accessories remain identical from the first frame to the last. No text, no letters, no subtitles, no watermark, no logo anywhere in frame; screens stay blank. Stable lighting, consistent white balance, consistent color grade. No scene change, no object disappearing, no prop swapping hands.

**中（挂在每个镜头的锁定块里）**
> 单镜一镜到底，机位固定，无剪辑、无变焦、无晃动。画面内只有一个人，无多余人物、无多余肢体，每只手五根手指，关节自然。从第一帧到最后一帧，面部、发型、服装颜色、全部饰品保持一致。画面任何位置不出现文字、字母、字幕、水印、标识；屏幕保持纯黑。光照稳定，白平衡与色调前后一致。无场景切换，无物件消失，无道具左右手调换。

**使用注意**
- 这段尾缀本身约 70 个英文词，已站在 Hailuo 甜点区上沿，**不要再加**，加了就互相挤兑。
- H3 若无负向字段，这段起的是**正向约束 + 状态锁定**作用，不是 CFG 推离 —— 预期是「降低发生率」，不是「消除」。

---

## 附：证据来源与分级

**A（官方）**：MiniMax 开放平台 API 文档 —— prompt 上限 2000 字符、15 个方括号运镜指令、Hailuo 2.3 图生视频仅首帧、不生成音频。（最终以 h3-official-research 的官方核对为准。）

**B（可查第三方 / 学术）**
- fal.ai 模型对照表：Hailuo 2.3 无 negative_prompt、无首尾帧、无音频、无 CFG 调节
- geekai.co 接入文档：`negative_prompt` 列为不支持参数
- versely.studio《Hailuo 2.3 Prompting Guide》：40–70 词甜点区、靠前 token 权重更高、无接触传递、非排版模型、复杂物理用 Standard 档
- versely.studio《On-screen text in generated video》：clean-plate rule、可生成/不可生成文字的边界
- arXiv 2512.16954：视觉锚定消融实验 7.99 → 0.55
- Kang et al., ICML 2025《How Far is Video Generation from World Model: A Physical Law Perspective》
- arXiv 2608.19583 VGI-Bench：oracle prompting 提升有限；object/state inconsistency
- pikaais.com 故障排查表：闪烁、身份漂移、手部、文字、运镜的逐条对策

**C（一线经验，弱证据，已在正文标注）**：Kling 负向提示词「无效或反效果」的实操记录；Nano Banana 手机正反面翻转等空间错误的用户报告；Veo 3 Verbatim Rule 的 40% 一致性差异。

**已被我剔除、未采用的来源**：若干中文站点流传的「MiniMax 超长提示词注入 `[EXP:V-SPATIO-TEMPORAL:E17-E24]` 专家路由符」「chunk_size=32768 / enable_chunking=True」等写法，无法在任何官方文档中验证，判定为编造，不予采用。
