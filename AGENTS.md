# AGENTS.md

本仓库是 **Ye Yixiang 的学术博客**：Quarto 静态站点，GitHub Actions 构建并发布到 GitHub Pages。
任何 AI/自动化代理在修改本仓库前，先读本文件，按这里的约定操作。

- 线上站点：`https://yeyixiang07.github.io`
- 仓库：`https://github.com/yeyixiang07/yeyixiang07.github.io`
- 本地仓库：`C:\Users\yeyix\Documents\GitHub\yeyixiang07.github.io`
- 发布方式：push 到 `main` → `.github/workflows/deploy.yml` → GitHub Pages

---

## 1. 目录结构

```text
.
├── _quarto.yml                 # 站点配置（导航、主题、字体、搜索）
├── _styles/zh.scss             # 中文排版与项目卡片样式
├── index.qmd / about.qmd       # 首页 / 关于
├── projects.qmd                # 项目页（脚本生成，勿手改）
├── scripts/
│   ├── fetch_projects.py       # 同步 GitHub 置顶仓库 → projects.qmd
│   └── make_figures.py         # 生成本文两张概念图（SVG + PNG）
├── blog/
│   ├── index.qmd               # 文章列表（分页、分类、RSS）
│   └── posts/
│       └── YYYY-MM-DD-slug/    # 每篇文章一个目录（目录名 = URL，发布后不要改）
│           ├── index.qmd
│           ├── refs.bib        # 本文参考文献
│           ├── ieee.csl        # 本文使用的 CSL（英文 IEEE）
│           └── figures/        # 本文图片（SVG 为主，PNG 备用）
└── .github/workflows/deploy.yml
```

不要提交 `_site/`、`.quarto/`、`.tools/`、系统临时文件。

---

## 2. 新建一篇文章

1. 新建目录：`blog/posts/YYYY-MM-DD-slug/`（slug 用英文短横线；**发布后不要改目录名**，否则 URL 会变）。
2. 复制/新建 `index.qmd`，front matter 至少包含：

```yaml
---
title: "文章标题"
description: "一句话摘要（用于列表页与搜索索引）"
date: 2026-11-05
categories: [Coding Agent, LLM]
tags: [对话噪声, 鲁棒性]
bibliography: refs.bib
csl: ieee.csl
---
```

3. 写正文；结构为 `## 1 标题`、`### 1.1 子标题`。
4. 在正文第一段之前写摘要与关键词（见 §3）。
5. 需要引用时，在 `refs.bib` 加条目，正文用 `[@key]`（见 §6）。
6. 文末加作者与版权（见 §5）。
7. 本地渲染检查（见 §7），确认无误后 commit + push（见 §8）。

---

## 3. 摘要与关键词（每篇必写）

放在 front matter 之后、正文 `## 1` 之前：

```markdown
## 摘要

（150–200 字：问题、方法/框架、主要结论、边界，一段话写完。）

**关键词**：关键词 1；关键词 2；关键词 3；关键词 4；关键词 5
```

要求：摘要不写“本文将……”式空话，直接说问题、做法、结论；关键词 3–6 个，用中文分号分隔。

---

## 4. 图表、公式、示例的编号规范

### 4.1 图

- 图片放文章目录的 `figures/`，优先 SVG（文字已转路径），PNG 作备用。
- 用 Markdown 图片 + `#fig-*` 标签，**不要在标题/图注里手写“图 1：”**，Quarto 会自动编号；手写会渲染成“图 图 1”。

```markdown
![图注内容（不写“图 1：”）](figures/fig1-framework.svg){#fig-framework width=100% fig-alt="替代文本"}
```

- 正文引用：`@fig-framework`（**不要写“图 @fig-framework”**，否则出现“图 图 1”）。
- 图片必须给 `fig-alt`；图注末尾可标注“概念图/假设图，非实验数据”。

### 4.2 表

- 用 pipe table，caption 写在表格之后、空一行，加 `#tbl-*`：

```markdown
| 列 1 | 列 2 |
|---|---|
| a | b |

: 表注内容 {#tbl-example}
```

- 正文引用：`@tbl-example`（不要手写“表 1”）。
- 表注不要以“表 1：”开头。

### 4.3 公式

- 行内 `$...$`，独立公式 `$$ ... $$`，需要编号时在结束 `$$` 后加 `{#eq-*}`：

```markdown
$$
E = mc^2
$$ {#eq-einstein}

由 @eq-einstein 可知……
```

- 正文引用：`@eq-einstein`（不要写“式 @eq-…”）。

### 4.4 示例（论文式 listing）

用加粗编号标题 + `text` 代码框 + 斜体分析；代码框前后必须有空行，否则会粘进上一段：

```markdown
**例 1｜示例标题**

```text
用户：……
Agent：……
```

*一段斜体分析，说明这个例子对应哪条机制/哪个结论。*
```

- 示例编号手动维护；如果在正文引用“例 1”，确保编号一致。
- 不要把示例标题拼在段落末尾（会渲染成“…，例 1｜…”）；标题必须独占一行。

---

## 5. 作者与版权（每篇文末）

```markdown
## 作者与版权

**作者**：Ye Yixiang（四川大学计算机科学与技术）  
**邮箱**：[yeyixiang@stu.scu.edu.cn](mailto:yeyixiang@stu.scu.edu.cn)  
**版权**：© 2026 Ye Yixiang。本文版权归作者所有，转载请注明作者与原文链接。
```

---

## 6. 参考文献

- 每篇文章目录下自带 `refs.bib` 与 `ieee.csl`（英文 IEEE 格式；`ieee.csl` 已做中文 locale 覆盖，不要随意删改）。
- 正文用 `[@key]`；多条用 `[@a; @b]`；引用只出现在表格单元格里也照常。
- **只引用可核验的文献**：arXiv 编号、DOI、会议/期刊信息必须真实；不要编造引用，也不要把无法核实的数字写成结论。
- 新增 bib 条目后重新渲染；检查没有 `[?]` 未解析引用；未被正文引用的条目建议删除（citeproc 不会渲染它）。
- 数字必须来自原文：引用具体百分比/降幅时，先核对论文摘要或正文。

---

## 7. 本地渲染与预览

Quarto 便携版（本机）：

```powershell
cd "C:\Users\yeyix\Documents\GitHub\yeyixiang07.github.io"
C:\Users\yeyix\Documents\GitHub\.tools\quarto\bin\quarto.exe render
```

预览（会占用 4321 端口）：

```powershell
C:\Users\yeyix\Documents\GitHub\.tools\quarto\bin\quarto.exe preview --port 4321 --no-browser
```

- 预览是独立进程；如果端口被占用，先结束旧的 `quarto.exe` 再启动。
- `quarto render` 前最好先停掉预览，避免 `_site` 文件竞争导致 `rename ... NotFound`；报错时删掉 `_site` 重渲染即可。
- 渲染产物在 `_site/`，已被 `.gitignore` 忽略，不要提交。

---

## 8. 发布

```powershell
git add -A
git commit -m "post: 文章标题"
git push
```

推送后：

1. 到 GitHub Actions 看 `Render and Deploy` 是否通过（约 1–3 分钟）。
2. 打开线上文章页，确认图、公式、表、示例、参考文献、摘要、作者版权都正常。
3. 检查 `/blog/index.xml`（RSS）与 `/sitemap.xml` 是否包含新文章。

站点设置：`Settings → Pages → Source = GitHub Actions`。

---

## 9. 发布前检查清单

- [ ] `quarto render` 无报错；
- [ ] 页面里没有 `[?]`（未解析引用）；
- [ ] 图/表/式/例编号连续，正文引用与编号一致；
- [ ] 没有出现“图 图 1”“表 表 1”这类重复前缀；
- [ ] 图片路径正确（`figures/...`），SVG/PNG 都在仓库里；
- [ ] `refs.bib` 中没有未被引用的条目（或确认保留）；
- [ ] 摘要 150–200 字，关键词 3–6 个；
- [ ] 文末作者、邮箱、版权齐全；
- [ ] 手机宽度下宽表/图不溢出；暗色模式下可读；
- [ ] 没有提交 `_site/`、`.quarto/`、`.tools/`。

---

## 10. 内容与写作约定

- 语气：学术博客，论证优先，少用“首先/其次/最后”式套话；结论标注证据强度。
- 区分**直接证据、跨域外推、待检验假设**；不要把自己的推断写成文献结论。
- 术语首次出现给英文（如“上下文卷吸（contextual entrainment）”）。
- 不做没有依据的“首次/填补空白”声明；用“据本文检索”限定。
- 作者信息固定为 Ye Yixiang（四川大学计算机科学与技术），邮箱 `yeyixiang@stu.scu.edu.cn`。

---

## 11. 项目页与图生成脚本

- `projects.qmd` 由 `scripts/fetch_projects.py` 生成，**不要手改**；GitHub Actions 每天 03:00 UTC 自动同步置顶仓库。
- 文章配图由 `scripts/make_figures.py` 生成（matplotlib；需要本机安装 matplotlib）。改图后运行：

```powershell
python scripts\make_figures.py
```

脚本会覆盖 `figures/fig1-framework.{svg,png}` 与 `figures/fig2-risk-matrix.{svg,png}`，然后重新渲染文章。
