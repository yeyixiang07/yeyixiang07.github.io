#!/usr/bin/env python3
"""生成 projects.qmd：从 GitHub 拉取置顶（Pinned）仓库。

数据来源优先级：
1. GraphQL pinnedItems（需要 token：环境变量 GH_TOKEN / GITHUB_TOKEN，或本机已登录的 gh）；
2. 拉不到置顶时，回退到最近更新的公开仓库（并在页面上说明）；
3. 都失败时保持原文件不变，构建继续。

本地用法：
    python scripts/fetch_projects.py
"""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
import urllib.request

LOGIN = "yeyixiang07"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "projects.qmd")

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          url
          stargazerCount
          updatedAt
          isPrivate
          primaryLanguage { name color }
        }
      }
    }
  }
}
"""


def get_token() -> str | None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token.strip()
    try:
        out = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        )
        return out.stdout.strip() or None
    except Exception:
        return None


def fetch_pinned(token: str) -> list[dict]:
    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": LOGIN}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "yeyixiang-blog-projects-sync",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.load(resp)
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    nodes = data["data"]["user"]["pinnedItems"]["nodes"] or []
    return [n for n in nodes if n and not n.get("isPrivate")]


def fetch_recent(token: str | None) -> list[dict]:
    url = f"https://api.github.com/users/{LOGIN}/repos?sort=updated&per_page=6"
    headers = {"User-Agent": "yeyixiang-blog-projects-sync"}
    if token:
        headers["Authorization"] = f"bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as resp:
        repos = json.load(resp)
    return [
        {
            "name": r["name"],
            "description": r.get("description") or "",
            "url": r["html_url"],
            "stargazerCount": r.get("stargazers_count") or 0,
            "updatedAt": r.get("updated_at") or "",
            "primaryLanguage": {"name": r.get("language") or "", "color": None},
        }
        for r in repos
    ]


def card(repo: dict) -> str:
    name = html.escape(repo.get("name") or "")
    url = html.escape(repo.get("url") or "#")
    desc = (repo.get("description") or "").strip()
    stars = repo.get("stargazerCount") or 0
    updated = (repo.get("updatedAt") or "")[:10]
    lang = repo.get("primaryLanguage") or {}
    lang_name = (lang.get("name") or "").strip()
    lang_color = lang.get("color") or "#8b949e"

    desc_html = f'\n    <p class="project-desc">{html.escape(desc)}</p>' if desc else ""
    lang_html = (
        f'\n    <span class="project-meta-item"><span class="lang-dot" '
        f'style="background:{html.escape(lang_color)}"></span>{html.escape(lang_name)}</span>'
        if lang_name
        else ""
    )
    updated_html = (
        f'\n    <span class="project-meta-item">更新于 {html.escape(updated)}</span>'
        if updated
        else ""
    )
    return f"""  <a class="project-card" href="{url}">
    <div class="project-name"><span>{name}</span><span class="project-stars">★ {stars}</span></div>{desc_html}
    <div class="project-meta">{lang_html}{updated_html}
    </div>
  </a>"""


def render(repos: list[dict], mode: str) -> str:
    if mode == "pinned":
        intro = "以下是我在 GitHub 上置顶（Pinned）的仓库。"
    elif mode == "recent":
        intro = (
            "我还没有在 GitHub 上置顶仓库，下面是最近更新的公开仓库；"
            "在 GitHub 主页置顶仓库后，这个页面会自动切换为置顶项目。"
        )
    else:
        intro = "还没有可展示的公开仓库。"

    if repos:
        grid = '<div class="project-grid">\n' + "\n".join(card(r) for r in repos) + "\n</div>"
    else:
        grid = '<p class="project-empty">暂无项目。</p>'

    return f"""---
title: 项目
description: GitHub 置顶项目
toc: false
---

这里同步自我 GitHub 上的置顶（Pinned）仓库。{intro}

```{{=html}}
{grid}
```

::: {{.callout-note}}
完整仓库列表见 [GitHub 主页](https://github.com/{LOGIN}?tab=repositories)。
:::
"""


def main() -> int:
    token = get_token()
    repos: list[dict] = []
    mode = "none"

    if token:
        try:
            repos = fetch_pinned(token)
            print(f"pinned: GraphQL ok, fetched {len(repos)} pinned repositories")
            if repos:
                mode = "pinned"
        except Exception as exc:  # noqa: BLE001
            print(f"warn: pinned query failed: {exc}", file=sys.stderr)

        if not repos:
            try:
                repos = fetch_recent(token)
                if repos:
                    mode = "recent"
                    print(f"recent: fetched {len(repos)} public repositories")
            except Exception as exc:  # noqa: BLE001
                print(f"warn: recent repos query failed: {exc}", file=sys.stderr)
    else:
        print("warn: no GitHub token available", file=sys.stderr)

    if not repos and mode == "none":
        print("no repositories fetched; leaving projects.qmd unchanged")
        return 0

    content = render(repos, mode)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print(f"wrote {OUT} (mode={mode}, count={len(repos)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
