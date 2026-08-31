# MiniMax H3 分镜脚本｜15 秒 · 3 镜头 · 衔接段

> 用途：3D 次世代漫剧的**转场 / 氛围段**，承接上一段 15 秒、引出下一段 15 秒
> 模型：MiniMax H3（海螺 H3 / Hailuo 03）　画幅：16:9　时长：15s（3 × 5s）　风格：3D 次世代动漫

---

## 一、镜头总表

| # | 时间码 | 时长 | 景别 | 运镜（官方术语） | 镜头功能 |
|---|---|---|---|---|---|
| 1 | 00:00–00:05 | 5s | 特写 → 大全景 | Pull Out with large amplitude at slow speed + Tilt Down | **入场衔接**：接上一段尾帧，从细节拉出，建立空间 |
| 2 | 00:05–00:10 | 5s | 全景 | Static Shot（靠元素运动） | **主体空镜**：过渡空间的核心意象，情绪停留 |
| 3 | 00:10–00:15 | 5s | 全景 → 中景 | Push In with large amplitude at slow speed | **出场衔接**：收束到可接下一帧的构图，钉住下一段首帧 |

**节奏逻辑**：一点（细节）→ 一线（空间纵深）→ 一面（出口） 。全程无人物、无对白，纯环境与运镜推进，方便前后任意剧情段插入。

---

## 二、逐镜详解【中文版（人类看）】

### 镜头 1｜00:00–00:05｜入场衔接
- **画面**：黄昏高空悬浮回廊。开场是一颗雨珠沿镀铬扶手滑落的特写，镜头大幅缓慢拉出，回廊全长没入雾气，再轻微下摇，露出下方天际线与渐变晚霞。
- **光影**：体积光束扫过湿滑地面，浮尘在光柱中飘移。
- **衔接动作**：首帧 = **上一段视频的最后一帧**（FL2VA 锁定）。
- **注意**：拉出幅度要大，确保第 5 秒的构图能直接对上镜头 2 的开场。

### 镜头 2｜00:05–00:10｜主体空镜
- **画面**：回廊纵深全景，机身固定。风穿过廊道，浮空光粒横向飘过，远处一列悬浮列车划破天际，光带在地面拖出长影。
- **光影**：暖色夕照与冷色阴影对撞，画面明暗分区清晰。
- **注意**：机身不动，全靠画面内元素运动制造"活着"的感觉——这是空镜不呆的关键。

### 镜头 3｜00:10–00:15｜出场衔接
- **画面**：镜头沿廊道大幅缓慢推进，终点是尽头那道亮着灯的门洞。推近过程中构图逐渐收拢，最终停在门洞剪影上，门内溢出强光。
- **衔接动作**：尾帧 = **下一段视频的第一帧**（FL2VA 锁定）。
- **注意**：末帧必须是高对比、低细节的剪影构图——细节越少，接下一帧越不容易穿帮。

---

## 三、可直接粘贴的 H3 提示词【H3版（H3看）】

### 方案 A（推荐）｜分三条生成，衔接帧精确可控

> 镜头 1、3 用 **FL2VA**（首尾帧），镜头 2 用 **T2VA**。生成后按 0–5–10–15 秒拼接。

#### ▸ 镜头 1 — FL2VA（5s）

```
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 5.00-second mark of the target video.

integrated_multimodal_description:
[Shot 1] Next-generation 3D anime style, cinematic, 16:9. The shot begins on a close-up of a single raindrop sliding down the chrome handrail of a floating sky corridor at dusk. The camera pulls out with large amplitude at slow speed, revealing the full length of the empty corridor receding into pale haze, then tilts down slightly to show the distant city skyline glowing beneath a gradient sunset sky. Volumetric light shafts sweep slowly across the wet floor, and floating dust motes drift through the beams. Begins with the raindrop in sharp macro focus, transitions into a wide establishing frame as the corridor opens into empty sky. No characters are present.

overall_soundscape:
A faint water drop lands on metal, then a low wind moves through the open corridor. Distant city hum rises under soft air movement.

non_diegetic_music:
A single sustained cello note with sparse ambient synth pads at a slow tempo, gradually swelling and holding through the final second.
```

#### ▸ 镜头 2 — T2VA（5s）

```
integrated_multimodal_description:
[Shot 1] Next-generation 3D anime style, cinematic, 16:9. A wide static shot frames the empty length of a floating sky corridor at dusk, the camera holding perfectly still. Wind moves through the corridor, drifting glowing particles horizontally across the frame. In the far distance a suspended maglev train crosses the sunset sky, leaving a slow light trail that draws a long reflection across the wet floor. Warm sunset light collides with cool blue shadow, splitting the frame into clear zones of light and dark. No characters are present.

overall_soundscape:
A steady breeze passes through the corridor with faint metallic resonance from the railings. A distant low rumble of the far-off train, soft and delayed.

non_diegetic_music:
Sparse piano notes at a slow tempo over a sustained string pad, minimal and even-paced, no percussion.
```

#### ▸ 镜头 3 — FL2VA（5s）

```
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 5.00-second mark of the target video.

integrated_multimodal_description:
[Shot 1] Next-generation 3D anime style, cinematic, 16:9. The camera pushes in with large amplitude at slow speed along the empty sky corridor, moving toward a lit doorway at the far end. As it advances, the composition narrows and the surrounding corridor falls into deep silhouette. The shot culminates on the doorway as a bright warm light spills out from inside, the frame reduced to a high-contrast silhouette with minimal interior detail. No characters are present.

overall_soundscape:
Wind rises gently as the camera advances, floor panels creaking faintly under nothing. A soft low hum of light grows as the doorway approaches.

non_diegetic_music:
A low sustained drone builds slowly under a single high sustained violin note, reaching full intensity and cutting cleanly at the final frame.
```

---

### 方案 B｜一条 15 秒 T2VA 一次出三镜

> 只用在你**不需要**精确锁首尾帧、只想快速看整体节奏时。

```
integrated_multimodal_description:
[Shot 1] Next-generation 3D anime style, cinematic, 16:9. The shot begins on a close-up of a single raindrop sliding down the chrome handrail of a floating sky corridor at dusk. The camera pulls out with large amplitude at slow speed, revealing the full length of the empty corridor receding into pale haze, then tilts down slightly to show the distant city skyline glowing beneath a gradient sunset sky. Volumetric light shafts sweep slowly across the wet floor and floating dust motes drift through the beams. No characters are present.

[Shot 2] At 00:05.000, the camera cuts to a wide static shot along the same empty corridor, the camera holding perfectly still. Wind drifts glowing particles horizontally across the frame while a suspended maglev train crosses the distant sunset sky, its light trail drawing a long reflection across the wet floor. Warm sunset light collides with cool blue shadow across the frame. No characters are present.

[Shot 3] At 00:10.000, the camera cuts to a view pushing in with large amplitude at slow speed along the corridor toward a lit doorway at the far end. The composition narrows and the corridor falls into deep silhouette, culminating on the doorway as bright warm light spills out, leaving a high-contrast silhouette with minimal interior detail. No characters are present.

overall_soundscape:
A water drop lands on metal, then wind moves continuously through the open corridor throughout. Distant city hum and a delayed low rumble from a far-off train, with a soft low hum of light rising near the end.

non_diegetic_music:
A sustained cello note with sparse ambient synth pads at a slow tempo, joined by sparse piano notes in the middle section, building to a low drone and a single high sustained violin note that cuts cleanly at the final frame.
```

---

## 四、衔接实施要点

1. **锁帧素材准备**：从「上一段 15s」导出最后一帧 → 作为镜头 1 的 Picture 1；从「下一段 15s」导出第一帧 → 作为镜头 3 的 Picture 2。
2. **镜头 1 的 Picture 2 / 镜头 3 的 Picture 1**：用镜头 2 的首尾帧，保证中间不跳。
3. **时间码必须严格递增**：`At 00:05.000` → `At 00:10.000`，第一个镜头**不加**时间戳。
4. **拼接**：三条 5s 视频硬切即可，别加转场特效——H3 生成的节奏已经对齐。
5. **一致性**：三条用同一批参考图（回廊、扶手材质、色板）能显著减少风格漂移。

---

## 五、需要你替换的占位项 ⚠️

以下是我按「3D 次世代漫剧」的通用理解拟的**默认场景**，不是从你的实际剧本里来的，请按需替换：

| 占位 | 当前默认值 | 需你确认 |
|---|---|---|
| 场景 | 黄昏·高空悬浮回廊 | 你的漫剧实际转场空间 |
| 核心意象 | 雨珠 / 光粒 / 悬浮列车 | 与主线呼应的道具 |
| 色彩 | 暖夕照 vs 冷蓝阴影 | 你的剧集色板 |
| 镜头 3 终点 | 亮着灯的门洞 | 下一段的真实开场画面 |
| 配乐 | 大提琴 + 钢琴 + 弦乐 pad | 你的 BGM 风格 |

告诉我这五项，我把提示词改成你剧本里的实际内容。

---

## 六、官方避坑检查表

- [ ] 指令首行在**第一行**，之后空一行（T2VA 不需要）
- [ ] 时间码格式 `00:SS.SSS`，不是 `5s` / `第5秒`
- [ ] 第一个镜头**没有**时间戳
- [ ] 运镜写成自然英文句子，不堆标签：`pulls out with large amplitude at slow speed`
- [ ] 每个镜头只有一个主运镜，不叠加互相打架的运动
- [ ] 配乐只写乐器 / 速度 / 节奏 / 动态，不写「史诗感」这类情绪词
- [ ] 音景不重复对话与配乐内容
- [ ] 无对白时不要硬加说话人标签
