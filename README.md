# Ye Yixiang's Blog

个人博客源码：Quarto + GitHub Pages。

## 写一篇新文章

1. 新建目录 `blog/posts/YYYY-MM-DD-slug/`（slug 用英文和短横线，发布后不要改路径）；
2. 新建 `index.qmd`，开头写 front matter：

```yaml
---
title: "文章标题"
description: "一句话摘要，显示在列表页和搜索结果里"
date: 2026-11-04
categories: [GraphRAG]
tags: [知识图谱, LLM]
---
```

3. 正文用 Markdown 写，公式用 LaTeX 语法：
   - 行内公式：`$E = mc^2$`
   - 独立公式：`$$ ... $$`
   - 编号公式：`$$ ... $$ {#eq-name}`，正文用 `@eq-name` 引用
4. 提交并推送：

```bash
git add -A
git commit -m "post: 文章标题"
git push
```

推送后 GitHub Actions 自动渲染并发布，通常 1–2 分钟生效。

## 本地预览

安装 [Quarto](https://quarto.org/docs/get-started/) 后，在本目录运行：

```bash
quarto preview     # 实时预览
quarto render      # 全量渲染到 _site/
```

## 部署说明

- 站点地址：`https://yeyixiang07.github.io`
- 仓库：`https://github.com/yeyixiang07/yeyixiang07.github.io`
- 仓库设置：**Settings → Pages → Source = GitHub Actions**
- 工作流：`.github/workflows/deploy.yml`

## 目录

| 路径 | 说明 |
|---|---|
| `_quarto.yml` | 站点配置（导航、主题、搜索、字体） |
| `_styles/zh.scss` | 中文排版与字体 |
| `blog/index.qmd` | 文章列表（分页、分类、RSS） |
| `blog/posts/` | 所有文章 |
| `index.qmd` / `about.qmd` | 首页 / 关于 |
