# MiniMax H3（Hailuo 03）官方提示词规范调研报告

> **核心突破**：找到了 MiniMax **官方**提示词指南原文（不是镜像、不是转述）。
> 官方仓库 `MiniMax-AI/MiniMax-H3` 内置 prompt-writing skill，含两份指南：
> - `skills/h3-prompt-writing/references/base-en.txt` — **T2VA/I2VA/FL2VA/L2VA**
> - `skills/h3-prompt-writing/references/ref-en.txt` — **Full-Reference (Ref2VA)**
>
> 下文标注 **【官方原文】** 的条目均逐字摘自这两份文件。

| 来源 | URL | 性质 |
|---|---|---|
| **A** | `https://github.com/MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/base-en.txt` | **官方原文** |
| **B** | `https://github.com/MiniMax-AI/MiniMax-H3` → `skills/h3-prompt-writing/references/ref-en.txt` | **官方原文** |
| **C** | `https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir` | **官方 API 文档** |
| **D** | `https://huggingface.co/MiniMaxAI/MiniMax-H3` | **官方模型卡** |
| **E** | `https://docs.comfy.org/tutorials/video/minimax/minimax-h3` | ComfyUI 官方文档 |
| **F** | `https://minimaxh3.co/prompt-guide` | **第三方镜像**（自述 "This page follows the two official MiniMax H3 prompt guides"，非 MiniMax 自有域名） |
| **G** | `https://platform.minimaxi.com/document/guides_video_generation` | 官方开放平台（页面返回 500，经搜索缓存取证） |

---

## 1. 四种任务类型与「指令首行」

### 1.1 定义【官方原文 · A】

```text
- T2VA: Builds a complete audiovisual timeline from text.
- I2VA: T2VA body + first-frame instruction + a visual path that develops forward from the first frame.
- FL2VA: T2VA body + first-and-last-frame instruction + a continuous path from the first frame to the last frame.
- L2VA: T2VA body + last-frame instruction + a path that converges from a plausible preceding state to the last frame.
```

### 1.2 指令首行模板【官方原文 · A】

> **T2VA 不需要指令首行。** 原文：**"T2VA has no image-alignment instruction and begins directly with the three core fields."**

**I2VA（固定模板，原文标注 "always uses"）**
```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

**FL2VA（固定模板，"always uses"）**
```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

**L2VA（固定模板，"always uses"）**
```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

【官方原文 · A】占位符与位置规则：
```text
Here, `N` is the index of the actual final shot, and `S.SS` is the effective video duration
formatted to exactly two decimal places. The instruction must be the first line of the final
prompt, followed by one blank line before the core fields.
```

⚠️ **易错点（官方内部不一致，照抄即可）**：FL2VA 用裸 `Picture 1`（**无尖括号**）+ `(from Shot 1)`；L2VA 用 `<Picture 1>`（**有尖括号**）+ `(from [Shot N])`。两份都按官方原文照抄，不要统一。
⚠️ 第三方镜像 F 的版本（`For the target video, at 0.00 seconds, <Picture 1> from [Shot 1] is fully referenced.`）与官方 A **有出入，以 A 为准**。

---

## 2. 三个核心字段

字段拼写与顺序【官方原文 · A】：

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

| 字段 | 官方定义【A】 | 句数限制【A】 | N/A 条件【A】 |
|---|---|---|---|
| `integrated_multimodal_description` | "Describes visuals, actions, shots, speakers, dialogue, singing, and diegetic audio along the timeline." | 无上限 | 不可 N/A |
| `overall_soundscape` | "Summarizes ambient sound, physical action sounds, and non-verbal human sounds across the entire video." | **1–4 句** | "Use N/A only when the user explicitly requests complete silence throughout the video." |
| `non_diegetic_music` | "Describes background music that the characters cannot hear and only the audience can hear." | **1–3 句** | "Use N/A when there is no non-diegetic music." |

句数原文【A】：
```text
Use 1–4 English sentences in one continuous paragraph to summarize the ambient sound...
Use 1–3 English sentences to describe background music...
```

禁止内容【A】：
```text
Dialogue, singing, and diegetic music already belong in the multimodal description and should not be repeated here [overall_soundscape].
...Focus on instrumentation, speed, rhythm, and dynamic changes; do not use abstract mood words or explain the emotional function of the score.
Singing, instruments, radio, television, or phone music audible to the characters are diegetic events and should appear in the multimodal description.
```

---

## 3. 镜头时间戳（三处格式不同，已分别确认）

| 位置 | 官方格式 | 官方原文 |
|---|---|---|
| **[Shot 1]** | **不加时间戳** | "Do not add a timestamp to the first shot." |
| 后续镜头 | `[Shot N] At MM:SS.mmm, ...` **三位小数** | "begin each one with a strictly increasing cut time that falls within the video duration" |
| 指令首行锚点 | `S.SS` **两位小数，无 MM: 前缀** | "`S.SS` is the effective video duration formatted to exactly two decimal places" |

官方例句【A】：`[Shot 2] At 00:03.500, the camera cuts to...`
第三方镜像 F 的最终检查清单（**第三方转述**，但与 A 一致）：
```text
S.SS uses exactly two decimal places, and [Shot N] is the actual final shot index.
[Shot 1] has no timestamp. Every later cut time is strictly increasing and remains inside the requested duration.
```

切换动词【A】：`the camera cuts to` / `the shot cuts to` / `the shot transitions to` / `the shot changes to` / `the shot switches to`；用户明确要求时可用 `cross-dissolve`、`fade`、`wipe`。

**核心红线**："A cut should introduce new information about the subject, space, state, viewpoint, or time. If only the distance or a slight angle needs to change, prefer camera motion."

---

## 4. 运镜官方术语表

【官方原文 · A 完整表格】

| Dimension | Available Expression | Description |
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
| Amplitude | `with small amplitude` | Small-range change |
| Amplitude | `with large amplitude` | Large-range change |
| Speed | `at slow speed` | Slow movement |
| Speed | `at fast speed` | Fast movement |

**搭配规则**【A】：三维顺序 = **motion type → amplitude → speed**；"Add amplitude and speed only when they are meaningful; medium amplitude and normal speed are usually omitted."

官方例句【A】：
```text
The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.
The camera pans right with large amplitude at fast speed, revealing the open doorway.
The camera holds a static shot as the runner exits the frame.
```
> "Camera motion should be written as a natural English action within the shot, rather than stacked as separate labels at the end of a sentence."

---

## 5. 说话人与对白

【官方原文 · A】

- **编号规则**：`stable IDs such as (S1) and (S2)`；齐声用 `(S1,S2)`；"A speaker keeps the same ID across shots; characters who never vocalize receive no speaker ID."
- **首次出场**需从视觉+听觉两维建立身份：`character type, age, gender, whether the person is on-screen, pitch, timbre, speaking rate, or accent`。
- **标签结构**：`Place the speaker's identifying phrase, ID, action, and delivery outside <d>. Inside <d>, include only the language tag and the actual user-provided spoken content. Preserve every original word and punctuation mark verbatim; do not translate or rewrite them.`

```text
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
```

- **画外音旁白**（固定搭配，两句话必须成对出现）：
```text
For voiceover, use the exact phrase `says in an off-screen voiceover`. Immediately after every
voiceover <d> block, state that the corresponding on-screen character's lips remain closed:

The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```
> **「嘴唇保持闭合」官方原句 = `while his lips remain completely closed.`**

- **跨剪辑连续对话 / 结尾截断**：
```text
When the same line of dialogue or lyrics crosses a cut, use <scenetrans> at the connecting points
in both parts and explicitly state that the audio continues across the cut. Use <cutoff> when
speech is truncated by the end of the video. Continuity may be expressed with `continues
seamlessly across the cut`, `continues uninterrupted into the next shot`, `carries over from the
previous shot`, or `remains audible across the transition`.
```

---

## 6. 画面内可见文字

【官方原文 · A】
```text
Place any banner, sign, label, subtitle, or neon text that is actually visible on screen in English
double quotation marks. Preserve the original text and punctuation verbatim, without translation.

A red neon sign reading "营业中" glows above the doorway.
```
→ 确认：**英文双引号包裹**，**逐字保留不翻译**（官方示例直接保留了中文原文）。

---

## 7. 全参考模式（Ref2VA / Full-Reference）

### 7.1 六部分结构【官方原文 · B】

| Section | Purpose |
|---|---|
| `subject_definitions` | Defines referenced content and its reference labels |
| `summary` | Summarizes the task type, target video, and main reference relationships |
| `retention_analysis` | Describes how referenced content is preserved, transferred, or reused |
| `detailed_description` | Describes visuals, actions, shots, sound, and dialogue in playback order |
| `overall_soundscape` | Summarizes ambience and physical sounds |
| `non_diegetic_music` | Describes background music audible only to the audience |

### 7.2 ✅ 四种参考标签的**确切语法**【官方原文 · B】

> **不是 `<asset-1>` / `<subject-1>` / `<image-1>`。官方写法是首字母大写 + 空格 + 数字：**

| Label | 官方含义 |
|---|---|
| `<Subject N>` | Visible content abstracted from reference assets that can be reused or modified in the target video |
| `<Picture N>` | A reference image used as a concrete target frame or shot-planning anchor |
| `<Video N>` | A reference video that provides an editing source, continuation starting point, or whole-video temporal structure |
| `<Audio N>` | An audio signal that is copied or referenced |

官方例句【B】：
```text
<Subject 1> is the young woman in <Picture 1>, with long dark hair, a blue cardigan, and a thin silver necklace.
<Subject 1> is the woman whose appearance comes from <Picture 1> and whose walking motion comes from <Video 1>.
<Picture 2> is the first frame of [Shot 1], showing a woman seated beside a café window.
<Picture 3> is a storyboard reference for [Shot 1] and [Shot 2], defining their viewpoint, subject placement, and shot order.
<Video 1> is the source video for the target video edit.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
```

标签复用【B】："Once a reference label is assigned to a piece of content, it keeps the same meaning across `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, and the audio sections."
独立编号【B】："`Video N` and `Audio N` are numbered independently... The same reference video may therefore correspond to `<Video 1>` and `<Audio 2>`."

### 7.3 retention_analysis 关系标记【官方原文 · B，"fixed English values"】

**视觉**（`<Subject N>` / `<Picture N>` / `<Video N>`）：

| Relationship marker | Meaning |
|---|---|
| `fully_preserved` | The defined role of the referenced content is fully preserved |
| `partially_preserved` | The referenced content is still used, but some defined characteristics are changed or only partially retained |
| `attribute_transfer` | Referenced characteristics are transferred to a different identifiable target subject |
| `weak_reference` | Only broad similarity in style, category, composition, or atmosphere is retained |

**音频**（`<Audio N>`）：

| Relationship marker | Meaning |
|---|---|
| `fully_copy` | The complete source audio serves as the target video's complete final audio track |
| `partially_copy` | Only part of the timeline or selected audio layers are copied, or other sounds are added, removed, or replaced after copying |
| `reference` | The signal is not copied directly; only timbre, rhythm, music style, dialogue content, or sound texture is referenced |
| `weak_reference` | Only broad similarity in category or atmosphere is retained |

官方条目格式【B】：
```text
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
<Picture 2> ([Shot 1] first frame): fully_preserved - ...
<Video 1> (cut and pacing structure): weak_reference - ...
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track.
<Audio 2>: reference - the target speaker follows <Audio 2>'s voice timbre and measured delivery without copying the original signal.
```

### 7.4 summary 任务类型前缀【官方原文 · B】

```text
[reference generation] ...
[video editing + reference generation + audio reuse] ...
```
六种：`keyframe completion` / `reference generation` / `video editing` / `video continuation` / `audio reuse` / `audio reference`。多类型用 ` + ` 连接且不重复。
> 编辑任务固定开头：`The target video is an edited version of <Video 1>.`
> "Do not introduce new reference labels in this section."

### 7.5 与 Base 模式的格式差异【官方原文 · B】

| Dimension | T2VA | Full-reference mode |
|---|---|---|
| Main field | `integrated_multimodal_description` | `detailed_description` |
| Style opening | Written after `[Shot 1]` | **Established in one or two English sentences before `[Shot 1]`** |
| Reference information | Does not use full-reference labels | Inserts `<Subject N>`, `<Picture N>`, `<Video N>`, `<Audio N>` |
| Audio relationships | Describes the target video's own sound | Cites `<Audio N>` and states whether the signal is copied or referenced |

**字数**【B】："For generation tasks, `detailed_description` is normally 350-500 English words."（非硬配额，对白密集时以完整对白时间线优先）

**说话人组合写法**【B】：
```text
<Subject 2> (S1) turns toward the woman and says, <d>[English] Last summer, I went to my grandfather's house. He talked about you.</d>
```
> "Do not write `(Sx)` in `retention_analysis`."

---

## 8. 硬性参数

### 8.1 提示词上限【官方原文 · C】✅ 权威定论

```text
Text prompt, required: every scenario must include one non-empty `text` describing the desired
video. Length is counted by characters, with a maximum of 7000 characters per `text`.
```
→ **7000 是字符（characters），不是 token。中文按字符计数（1 个汉字 = 1 字符）。**
中国区文档 G 佐证：「提示词字数上限 不超过 7000 字符」。

### 8.2 时长 / 帧率 / 分辨率 / 画幅【官方 C + D】

| 项 | 官方值 | 来源 |
|---|---|---|
| Duration | **Required, integer. Available values: 4-15**（枚举 `4,5,6,7,8,9,10,11,12,13,14,15`） | **C 官方** |
| FPS | **24 FPS** | **D 官方** |
| Resolution | 短边默认 768 像素；`768p` / `2K` 两档（2K 经 H3-Regenerate-2K） | **D 官方** |
| Aspect ratio | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` | **C 官方** |
| Audio | 32 kHz stereo | **D 官方** |
| 对白语言 | 稳定支持 11 种：Arabic, Chinese, English, French, German, Italian, Japanese, Korean, Portuguese, Russian, Spanish | **D 官方** |

**ratio 分模式行为**【官方 C】：
- **t2va**：`ratio` **必填且不能为 adaptive**，只能取 6 个具体值。
- **i2va**：画幅由输入图决定，**恒为 adaptive**，传其他值不报错但被忽略。
- **r2va**：可选，默认 `adaptive`，也可显式指定。

⚠️ **时长口径不一致（重要）**：官方 API（C）与官方模型卡（D）为 **4–15 秒**；但 **ComfyUI 官方文档（E）与 diffusers 文档写 5–15 秒**（本地权重帧数网格 `17k+5` → 合法帧数 `5, 22, 39...`）。**API 走 4–15，本地部署走 5–15**。

### 8.3 参考素材上限【官方 C + D】

| 类型 | 数量 | 时长 | 单文件 | 格式 / 其他 |
|---|---|---|---|---|
| Image | first_frame ≤ 1、last_frame ≤ 1、**reference_image ≤ 9** | — | ≤ 30 MB | JPG/JPEG/PNG/WEBP/HEIC/HEIF；宽高 [256, 5760] px；宽高比 [0.4, 2.5] |
| Video | **≤ 3** | 单段 [2, 15] s，**总 ≤ 15 s** | ≤ 50 MB | MP4/MOV；H.264/AVC、H.265/HEVC；帧率 [23.976, 60] |
| Audio | **≤ 3**，**不能单独输入**，须配图或视频 | 单段 [2, 15] s，**总 ≤ 15 s** | ≤ 15 MB | WAV/MP3 |
| **混合总上限** | **12 个文件** | | 请求体 ≤ 64 MB | 图生视频与全能参考**互斥**，不可混用 |

### 8.4 本地部署画布【官方 E】
原生 `768px` 短边，16:9 下为 `1344x768`；分辨率取整到 **32 的倍数**；`1.0` Megapixel 档会得到 `1376x768`，**超出 768x1344 面积上限，须跳过**。

---

## 9. 官方避坑清单

> ⚠️ **重要声明**：官方 base-en.txt / ref-en.txt **没有**一份成文的「红线清单」。下列 **(A)(B)(C)** 是从官方原文中逐条摘出的 `do not / should not / only when` 硬性规则；**(F)** 标记的段落来自第三方镜像 minimaxh3.co 的 "Final output checklist"，与官方内容一致但**属第三方转述，未找到官方原文对应段落，存疑**。

**(A) 结构与时间戳**
- "Do not add a timestamp to the first shot."
- 后续镜头切点必须 "strictly increasing" 且 "falls within the video duration"。
- 小幅取景变化用 camera motion，**不要切镜头**。

**(A)(B) 音频三层不得混写**
- `overall_soundscape` 不得重复对白/演唱/剧情内音乐。
- `non_diegetic_music` "do not use abstract mood words or explain the emotional function of the score"。
- "Write complete dialogue and lyrics only inside `<d>` in `detailed_description`; do not repeat them in these two sections."

**(A) 对白**
- `<d>` 内只放语言标签与原话；身份/动作/语气一律放外面。
- "do not translate or rewrite them."
- 不出声的角色不给 ID；同一说话人跨镜头 ID 不变。

**(B) 参考模式**
- "Do not introduce new reference labels in this section [summary]."
- "Do not write `(Sx)` in `retention_analysis`."
- "An ordinary reference video does not create `<Audio N>` merely because the file contains sound."
- 仅用于定义角色/场景/服装/风格的图片**不建**独立 `<Picture N>`，应引在 `<Subject N>` 定义里。
- "Do not treat newly added actions, backgrounds, or plot events in the target video as losses of reference fidelity."
- "Avoid reducing the description to a plot summary or a list of reference relationships."
- 听不清的源词写 `[unclear]`，不要猜。
- 仅参考音色/节奏时，"do not carry the original dialogue from the reference audio into the target video"。

**(C) API 层**
- 每个请求必须含一个非空 `text` 项，否则参数错误。
- **图生视频与全能参考互斥**（`first_frame`/`last_frame` 与 `reference_*` 不可同时出现）。
- **音频不能单独提交**。

**(F) 第三方转述的最终检查清单（存疑，但与官方一致，可作自查表）**
```text
- The correct image-alignment instruction is the first line when required, followed by one blank line. T2VA has no alignment line.
- S.SS uses exactly two decimal places, and [Shot N] is the actual final shot index.
- [Shot 1] has no timestamp. Every later cut time is strictly increasing and remains inside the requested duration.
- Every cut introduces new subject, space, state, viewpoint, or time information. Minor reframing uses camera motion instead.
- Speaker IDs stay stable across shots. Non-speaking characters do not receive an ID.
- Each <d> block contains only the language tag and exact spoken words. Visible text stays in double quotation marks.
- overall_soundscape contains ambience and physical sounds, not repeated dialogue, singing, or on-screen music.
- non_diegetic_music describes instrumentation, tempo, rhythm, and dynamics, or uses N/A for no audience-only score.
```

**(第三方) 内容审核错误码** — 来源 atlascloud.ai，**第三方转述，存疑**：`1026` 输入命中审核、`1027` 输出命中审核、`1042` 文本含隐藏/非法字符（从 Notion/Word 复制粘贴常见）、`2013` 参数非法。

---

## 10. 加分项

### 10.1 ✅ 官方完整示例（T2VA）【官方原文 · A】
```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a baker opening the shutters of a small street bakery before sunrise. The camera pushes in with small amplitude at slow speed as the middle-aged baker with a calm, slightly raspy voice (S1) places a fresh loaf on the wooden counter and says: <d>[English] First batch of the morning.</d> [Shot 2] At 00:05.000, the camera cuts to a close-up of steam rising from the sliced bread while the baker's final words carry over from the previous shot.

overall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery. The doorbell rings once, followed by light footsteps and the crisp sound of bread being sliced.

non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
```

### 10.2 ✅ 官方 Full-Reference 三镜头完整示例【官方原文 · B】
（含 `[Shot 1]/[Shot 2]/[Shot 3]`、四种标签、retention 标记，见 B 文件 Section 7 "Complete Example"，因长度此处从略，建议直接取原文）

### 10.3 ✅ FL2VA 单镜头默认【官方原文 · A】
```text
FL2VA generally favors a single shot so the model can interpolate continuously from the first
frame to the last frame. Use multiple shots only when they are explicitly specified. The last
frame must be reached by the final `[Shot N]` at the end of the video.
```
推荐叙事结构【A】：**first-frame state → observable intermediate changes → progressively narrowing differences → last-frame state**

### 10.4 ✅ 角色一致性 / 参考帧锁定官方写法

- **I2VA**【A】："Character identity, clothing, colors, key objects, and spatial relationships should remain consistent." 官方示例锁定句：
```text
...the young woman shown in <Picture 1> remains beside the rain-covered train window, preserving her appearance, clothing, seat position, and the carriage layout.
```
- **Ref2VA**【B】：把不可漂移的特征写进 `subject_definitions` + `retention_analysis` 的特征清单，如
```text
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the Samoyed's thick white fur, pointed ears, dark nose, and curved tail are retained.
```
- **多素材组合单主体**【B】：`<Subject 1> is the woman whose appearance comes from <Picture 1> and whose walking motion comes from <Video 1>.`
- 天然帧锚点写法【B】：`the shot begins from <Picture 1>` / `the shot's keyframe corresponds to <Picture 2>` / `the shot ends on <Picture 3>`

### 10.5 ⭐ 强烈建议：用官方 H3-Context-IR 当「提示词编译器」

官方 C 有一条独立接口 `POST /v2/h3_context_ir`，把自然语言需求**自动改写成规范的 H3 结构化提示词**，成功后从 `content.prompt` 取回。官方响应示例中返回的正是标准三字段格式：
```json
"content": { "prompt": "integrated_multimodal_description: [Shot 1] Cinematic, wide shot with a slow push in on a female captain standing center frame...\noverall_soundscape: Deep, resonant low-frequency thrumming of ship engines...\nnon_diegetic_music: Symphonic orchestral score, beginning with a slow, rising brass and string crescendo..." }
```
→ 模板体系可先用 H3-Context-IR 做**基线校验器**：把自研模板输出喂进去，对比官方改写结果，反向校准模板。这是最快验证模板正确性的手段。

另：ComfyUI 官方节点支持 `embedding:` 语法（E），内置 10 个官方 LoRA 风格 embedding，如 `minimaxh3_bullet_time`、`minimaxh3_four_seasons`、`minimaxh3_truman_show` 等。

---

## 附录：一句话速查

```text
[指令首行（T2VA 无）]  ← I2VA/FL2VA 用 S.SS 两位小数
<空一行>
integrated_multimodal_description: [Shot 1] <style>, <composition>, ...  ← Shot 1 无时间戳
                                    [Shot 2] At 00:SS.mmm, ...          ← 三位小数
overall_soundscape: 1–4 句，环境音/动作音/非语言人声；N/A 仅当全程静音
non_diegetic_music: 1–3 句，乐器/速度/节奏/动态；无配乐写 N/A
对白: <d>[English] ...</d>｜旁白: says in an off-screen voiceover ... while his lips remain completely closed.
跨切: <scenetrans>｜截断: <cutoff>｜可见文字: "英文双引号原文"
运镜: <type> with small|large amplitude at slow|fast speed（中等可省）
Ref2VA 六段: subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music
标签: <Subject N> <Picture N> <Video N> <Audio N>
上限: 7000 字符（按字符计）｜duration 4–15 整数｜24 FPS｜768p/2K｜9 图 + 3 视频 + 3 音频 ≤ 12 文件
```
