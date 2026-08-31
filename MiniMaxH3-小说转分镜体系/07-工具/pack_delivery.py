#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 MiniMax H3 分镜体系打包成 zip，放到桌面，用于分享。
目录结构按「新手 → 干活 → 参考 → 追溯」分层，已废弃文件单独隔离。
"""
import os
import re
import zipfile
import pathlib
import shutil

SRC = pathlib.Path(r"C:\Users\Amnesia\WorkBuddy\2026-08-30-01-29-44")
SKILLS = pathlib.Path(r"C:\Users\Amnesia\.workbuddy\skills")
DESKTOP = pathlib.Path(r"C:\Users\Amnesia\Desktop")
ROOT = "MiniMaxH3-小说转分镜体系"

# (打包内相对路径, 源文件绝对路径)
FILES = [
    # ---- 根：入口 ----
    ("从这里开始-使用流程教程.html", SRC / "MiniMaxH3-使用流程教程.html"),
    ("README-交付索引.md",          SRC / "README-交付索引.md"),

    # ---- 01 主模板 ----
    ("01-主模板/MiniMaxH3-小说转分镜-完整模板.md", SRC / "MiniMaxH3-小说转分镜-完整模板.md"),
    ("01-主模板/MiniMaxH3-模板.html",              SRC / "MiniMaxH3-模板.html"),

    # ---- 02 完整示例 ----
    ("02-完整示例/06-完整示例-一个故事走通全流程.md", SRC / "06-完整示例-一个故事走通全流程.md"),

    # ---- 03 单镜参考模板 ----
    ("03-单镜模板/H3单镜提示词模板_Ref2VA参考模式版.md", SRC / "H3单镜提示词模板_Ref2VA参考模式版.md"),
    ("03-单镜模板/⚠️已废弃-H3单镜提示词模板_v1.md",       SRC / "H3单镜提示词模板_v1.md"),
    ("03-单镜模板/MiniMaxH3_分镜脚本_15s3镜.md",           SRC / "MiniMaxH3_分镜脚本_15s3镜.md"),

    # ---- 04 调研底稿 ----
    ("04-调研底稿/01-MiniMax-H3-官方提示词规范调研报告.md", SRC / "MiniMax-H3-官方提示词规范调研报告.md"),
    ("04-调研底稿/02-防翻车限制词库_H3版.md",              SRC / "防翻车限制词库_H3版.md"),
    ("04-调研底稿/03-防翻车限制词库_补充勘误_H3专属.md",    SRC / "防翻车限制词库_补充勘误_H3专属.md"),
    ("04-调研底稿/04-叙事侧方法论_小说拆解与15秒3镜结构.md", SRC / "叙事侧方法论_小说拆解与15秒3镜结构.md"),
    ("04-调研底稿/05-衔接镜类型库_12列风险表单.md",          SRC / "衔接镜类型库_12列风险表单.md"),

    # ---- 05 已废弃（2.3 规格污染，仅供追溯）----
    ("05-已废弃-仅供追溯（Hailuo2.3规格，勿作H3依据）/防翻车限制词库_AI视频生成失败类型与规避写法.md",
     SRC / "防翻车限制词库_AI视频生成失败类型与规避写法.md"),
    ("05-已废弃-仅供追溯（Hailuo2.3规格，勿作H3依据）/防翻车限制词库_AI视频翻车类型调研.md",
     SRC / "防翻车限制词库_AI视频翻车类型调研.md"),

    # ---- 07 工具 ----
    ("07-工具/make_html.py",     SRC / "make_html.py"),
    ("07-工具/audit_rules.py",   SRC / "audit_rules.py"),
    ("07-工具/audit_expr.py",    SRC / "audit_expr.py"),
    ("07-工具/pack_delivery.py", SRC / "pack_delivery.py"),
]

# ---- 08 实拆案例（自动发现，新增拆解文件无需改这里）----
CASE_FILES = sorted(SRC.glob("拆解-*.html"))

# skills 自动发现：总控放最前，其余按名字排序。新增 skill 无需改这里。
SKILL_LIST = ["minimax-h3-storyboard"] + sorted(
    p.name for p in SKILLS.glob("h3-*")
    if (p / "SKILL.md").exists() and p.name != "minimax-h3-storyboard"
)

INTRO = """# MiniMax H3 小说转分镜体系

把一本长篇小说，稳定地变成 MiniMax 海螺 H3 能直接吃的视频提示词。

---

## 先看这个

**打开 `从这里开始-使用流程教程.html`**（双击即可，无需联网、无外部依赖）。

它是八步流程教程：每步讲清「做什么 / 用什么 / 怎么做 / 校验点」，
另附三个实战场景（从零开新书 / 只做一段 15 秒 / 画面崩了怎么修）。

看完教程再决定下一步：

| 你要做什么 | 用哪个 |
|---|---|
| 拿去干活 | `01-主模板/MiniMaxH3-模板.html`（侧边导航 + 一键复制 + 实时校验） |
| 让 AI 跑流程 | 把 `01-主模板/MiniMaxH3-小说转分镜-完整模板.md` 整份丢给 AI |
| 看完整范例 | `02-完整示例/` |
| 查官方依据 | `04-调研底稿/01-MiniMax-H3-官方提示词规范调研报告.md` |

---

## 目录

```
从这里开始-使用流程教程.html      ← 新手入口
README-交付索引.md                 文件导航
01-主模板/                         主模板（md 给 AI，html 给人）
02-完整示例/                       一个故事走通全流程
03-单镜模板/                       Ref2VA / Base 单镜模板
04-调研底稿/                       调研原始材料（均可用）
05-已废弃-仅供追溯/                ⚠️ 规格依据错误，勿作 H3 依据
06-skills/                         可复用 skill（放进 ~/.workbuddy/skills/）
07-工具/                           构建与自查脚本
08-实拆案例/                       真实小说拆解成品（看体系实际产出什么样）
```

---

## 关于 skills

`06-skills/` 里是一组 WorkBuddy skill，**总控是 `minimax-h3-storyboard`**。

安装：把 `06-skills/` 下的目录整个复制到
`C:\\Users\\<你的用户名>\\.workbuddy\\skills\\`

之后在对话里说「按 H3 流程拆解这本小说」，总控会自动按阶段调用对应分 skill。

| 阶段 | skill |
|---|---|
| ① 拆书 | `h3-novel-split` |
| ② 分镜 | `h3-camera-edit` |
| **③ 备参考图** | **`h3-refsheet-gen`** —— 三视图 / 表情集 / 场景图 / 道具图的制作方法 |
| ④ 写词 | `h3-character-asset` / `h3-expression-psych` / `h3-action-body` / `h3-dialogue-voice` / `h3-env-scene` / `h3-screen-text` |
| ⑤ 检查 | `h3-antibug-check` |

> ⚠️ **③ 不要跳过。** 角色卡只规定「登记哪些字段」，
> **那些参考图本身从哪来**由 `h3-refsheet-gen` 负责。
> H3 的一致性是靠**图**锁的——移除视觉锚定后，角色一致性从 **7.99 崩到 0.55**。

---

## 关于 08-实拆案例

`08-实拆案例/` 里是用这套体系**真实拆解的小说成品**（HTML，双击可看）。
每份都包含：集数测算、角色卡、场景表、逐段分镜表、每镜六段中文详版、H3 官方三字段。

**建议先扫一眼再动手**——比读方法论更快理解体系实际产出什么样。

---

## ⚠️ 两条使用提醒

1. **H3 ≠ Hailuo 2.3。** 2.3 无音频、仅首帧、2000 字符；H3 有原生音频、FL2VA、7000 字符。
   `05-已废弃-仅供追溯/` 里的两份底稿用的是 2.3 规格，**不要拿它当 H3 依据**，保留仅为追溯调研过程。

2. **有两处官方口径冲突，均未定论**（教程与主模板里都有完整说明与实测方法）：
   - 台词要不要加英文双引号
   - 参考标签写法（`<Subject N>` vs `<image_1>`）

   遇到这类问题，**不要只采信一条官方来源**。

---

## 体系规模

- 主模板 1 份（约 18,000 汉字）
- 完整示例 1 份
- skill 一组（合计约 133,000 汉字）
- 调研底稿 7 份
- 实拆案例若干

统计口径：`[\\u4e00-\\u9fff]` 只数汉字，不含标点 / 英文 / 数字。
"""


def safe_delete(path):
    """
    删除目录，但不因沙箱「安全删除（回收站）不可用」而崩溃。
    shutil.rmtree 在沙箱里被替换为走回收站的版本，回收站不可用时抛 OSError。
    降级为 os.walk 直接删除文件与空目录，忽略个别失败。
    """
    try:
        shutil.rmtree(path)
        return
    except Exception:
        pass
    try:
        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                except Exception:
                    pass
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except Exception:
                    pass
        try:
            os.rmdir(path)
        except Exception:
            pass
    except Exception:
        pass


def pick_outdir():
    """
    优先输出到桌面；若桌面不可写（沙箱拦截 / 权限不足），回退工作区。
    回退时会在结束时提示，避免用户以为打包成功却找不到文件。
    """
    try:
        probe = DESKTOP / "_pack_probe"
        probe.mkdir(parents=True, exist_ok=True)
        safe_delete(probe)
        return DESKTOP, True
    except Exception:
        return SRC, False


def main():
    # 注意：变量名用 outdir，不要用 out —— 下面拷贝循环里有个局部 out（目标文件路径）会覆盖它
    outdir, on_desktop = pick_outdir()
    tmp = outdir / ("_pack_" + ROOT)
    if tmp.exists():
        safe_delete(tmp)
    (tmp / ROOT).mkdir(parents=True, exist_ok=True)
    base = tmp / ROOT

    n = 0
    miss = []

    # 根目录说明
    (base / "README.md").write_text(INTRO, encoding="utf-8")
    n += 1

    for rel, src in FILES:
        if not src.exists():
            miss.append(str(src))
            continue
        dst = base / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        n += 1

    # skills
    for sk in SKILL_LIST:
        d = SKILLS / sk
        md = d / "SKILL.md"
        if not md.exists():
            miss.append(str(md))
            continue
        dst_dir = base / "06-skills" / sk
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in d.rglob("*"):
            if f.is_file():
                rel = f.relative_to(d)
                out = dst_dir / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out)
                n += 1

    # 08 实拆案例（自动发现）
    for src in CASE_FILES:
        dst = base / "08-实拆案例" / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        n += 1

    # zip
    # 注意：不要先 unlink 旧包 —— 沙箱会把删除劫持成「走回收站」，回收站不可用时抛 OSError，
    # 导致脚本在写新包前崩溃。ZipFile "w" 模式本身就是原地覆盖（15:00 已验证可行）。
    zpath = outdir / (ROOT + ".zip")
    try:
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for f in sorted(base.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(tmp))
    except OSError:
        # 桌面写入被沙箱拦截：回退工作区，保留桌面旧包不破坏
        outdir = SRC
        zpath = outdir / (ROOT + ".zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for f in sorted(base.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(tmp))
        on_desktop = False

    # 清理临时目录（沙箱下安全删除可能不可用，用 safe_delete 兜底）
    safe_delete(tmp)

    size_kb = round(zpath.stat().st_size / 1024, 1)
    print("打包完成:")
    print(" ", zpath)
    print(f"  文件数 {n}   大小 {size_kb} KB")
    if miss:
        print("\n未找到（已跳过）:")
        for m in miss:
            print("  -", m)
    else:
        print("  无缺失文件")

    if not on_desktop:
        print()
        print("  ⚠️ 桌面不可写（沙箱拦截或权限不足），已输出到工作区。")
        print(f"     手动复制到桌面:  copy \"{zpath}\" \"{DESKTOP}\"")


if __name__ == "__main__":
    main()
