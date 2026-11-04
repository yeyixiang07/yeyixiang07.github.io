# -*- coding: utf-8 -*-
"""Generate the two conceptual figures for the dialogue-noise article.

Fig 1: noise -> mechanisms -> capabilities -> governance framework.
Fig 2: task x noise-type risk hypothesis matrix (qualitative, not measured).

Run:  python scripts/make_figures.py
Outputs SVG (text as paths) + PNG (300 dpi) into the post's figures/ folder.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Patch

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "path"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "blog" / "posts" / "2026-11-04-dialogue-noise-coding-agents" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#263238"
LINE = "#546E7A"
GRID = "#ECEFF1"
HDR = "#37474F"


def box(ax, x, y, w, h, text, fc, ec, fs=9.0, weight="normal", tc=INK, ls="-"):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.06",
        linewidth=1.0, edgecolor=ec, facecolor=fc, linestyle=ls, zorder=2,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, fontweight=weight, zorder=3, linespacing=1.4)


def header(ax, x, y, w, h, text):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.06",
        linewidth=0, facecolor=HDR, zorder=2,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=11, color="white", fontweight="bold", zorder=3)


def arrow(ax, p1, p2, dashed=False, rad=0.0, color=LINE, lw=1.2):
    arr = FancyArrowPatch(
        p1, p2, arrowstyle="-|>", mutation_scale=9,
        linewidth=lw, color=color, zorder=3,
        linestyle=(0, (4, 3)) if dashed else "-",
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=0, shrinkB=0,
    )
    ax.add_patch(arr)


def figure_framework():
    fig, ax = plt.subplots(figsize=(12.4, 6.1))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(1.05, 7.15)
    ax.axis("off")
    fig.patch.set_facecolor("#FBFAF7")
    ax.set_facecolor("#FBFAF7")

    header(ax, 0.30, 6.55, 2.55, 0.45, "输入噪声")
    header(ax, 3.20, 6.55, 2.55, 0.45, "作用机制")
    header(ax, 6.10, 6.55, 2.45, 0.45, "受影响能力")
    header(ax, 9.15, 6.55, 2.85, 0.45, "治理层")

    # 输入噪声
    box(ax, 0.35, 4.75, 2.45, 1.05,
        "表面噪声\n填充词 · 符号 · 闲聊", "#E8F0FE", "#90A4AE")
    box(ax, 0.35, 3.20, 2.45, 1.30,
        "语义噪声\n无信息抱怨 · 含信息抱怨\n情绪施压 · 元对话", "#FBE9E7", "#BCAAA4")

    # 机制
    mech = [
        (5.70, "注意力汇与\n位置效应"),
        (4.92, "上下文卷吸\n（entrainment）"),
        (4.14, "语义重合"),
        (3.36, "指令层级竞争"),
        (2.58, "多轮累积\n（constraint drift）"),
    ]
    for y, label in mech:
        box(ax, 3.25, y, 2.45, 0.58, label, "#E3F2FD", "#90A4AE", fs=8.8)

    # 能力
    caps = [
        (5.70, "代码补全"),
        (4.72, "重构"),
        (3.74, "单元测试生成"),
        (2.76, "调试与\n多步工具调用"),
    ]
    for y, label in caps:
        box(ax, 6.15, y, 2.35, 0.70, label, "#F5F5F5", "#B0BEC5", fs=9.2)

    # 治理
    gov = [
        (5.70, "意图抽取 /\n缺陷报告"),
        (4.92, "上下文压缩"),
        (4.14, "解码锚定\n（SPA）"),
        (3.36, "工作流与接口"),
        (2.58, "噪声对齐训练"),
    ]
    for y, label in gov:
        box(ax, 9.20, y, 2.75, 0.58, label, "#E8F5E9", "#A5D6A7", fs=8.8)

    # 噪声 -> 机制（实线：有证据；虚线：假设）
    arrow(ax, (2.80, 5.50), (3.25, 5.99), dashed=False)
    arrow(ax, (2.80, 4.40), (3.25, 5.21), dashed=False, rad=-0.06)
    arrow(ax, (2.80, 4.15), (3.25, 4.43), dashed=False)
    arrow(ax, (2.80, 3.90), (3.25, 3.65), dashed=False)
    arrow(ax, (2.80, 3.55), (3.25, 2.87), dashed=True, rad=0.08)

    # 机制 -> 能力（虚线：任务层映射是假设）
    arrow(ax, (5.70, 5.99), (6.15, 6.05), dashed=True)
    arrow(ax, (5.70, 5.21), (6.15, 5.07), dashed=True, rad=-0.10)
    arrow(ax, (5.70, 4.43), (6.15, 5.07), dashed=True, rad=0.05)
    arrow(ax, (5.70, 4.43), (6.15, 4.09), dashed=True, rad=-0.05)
    arrow(ax, (5.70, 3.65), (6.15, 3.11), dashed=True, rad=0.08)
    arrow(ax, (5.70, 2.87), (6.15, 3.11), dashed=True, rad=-0.08)

    # 治理 -> 能力（相邻列，虚线：设计提议）
    arrow(ax, (9.20, 5.99), (8.50, 6.05), dashed=True)
    arrow(ax, (9.20, 5.21), (8.50, 5.07), dashed=True)
    arrow(ax, (9.20, 4.43), (8.50, 4.09), dashed=True, rad=0.05)
    arrow(ax, (9.20, 3.65), (8.50, 3.11), dashed=True, rad=0.05)
    arrow(ax, (9.20, 2.87), (8.50, 3.11), dashed=True, rad=-0.05)

    # 图例
    ax.plot([0.35, 0.95], [1.55, 1.55], color=LINE, lw=1.4)
    ax.text(1.05, 1.55, "有直接或较强间接证据的路径", va="center", fontsize=8.5, color=INK)
    ax.plot([0.35, 0.95], [1.25, 1.25], color=LINE, lw=1.4, linestyle=(0, (4, 3)))
    ax.text(1.05, 1.25, "待检验假设 / 设计提议", va="center", fontsize=8.5, color=INK)

    fig.tight_layout(pad=0.2)
    for ext in ("svg", "png"):
        path = OUT / f"fig1-framework.{ext}"
        fig.savefig(path, format=ext, bbox_inches="tight", pad_inches=0.06,
                    dpi=300, facecolor=fig.get_facecolor())
        print("saved", path)
    plt.close(fig)


def figure_risk_matrix():
    tasks = ["代码补全", "重构", "单元测试生成", "调试与\n多步工具调用"]
    noises = ["填充词", "符号", "闲聊", "无信息\n抱怨", "含信息\n抱怨", "情绪施压", "元对话"]
    # 1=低, 2=中, 3=高, 4=最高, 0=双面（可能有益）
    values = [
        [1, 2, 1, 2, 2, 2, 2],
        [1, 1, 1, 3, 3, 3, 3],
        [1, 1, 1, 2, 0, 2, 2],
        [2, 2, 1, 3, 3, 4, 3],
    ]
    fills = {0: "#FFE0B2", 1: "#DCEDC8", 2: "#FFF3C4", 3: "#FFCC80", 4: "#E64A19"}
    labels = {0: "双面", 1: "低", 2: "中", 3: "高", 4: "最高"}
    tcolors = {0: "#5D4037", 1: "#33691E", 2: "#795548", 3: "#6D4C41", 4: "white"}

    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 4.9)
    ax.axis("off")
    fig.patch.set_facecolor("#FBFAF7")
    ax.set_facecolor("#FBFAF7")

    left = 2.05
    colw = 0.72
    top = 3.52
    rowh = 0.60

    # 顶部两层表头：表面噪声 / 语义噪声
    ax.add_patch(Rectangle((left, 4.28), colw * 3, 0.30, facecolor="#E3F2FD",
                           edgecolor="white", linewidth=1))
    ax.add_patch(Rectangle((left + colw * 3, 4.28), colw * 4, 0.30, facecolor="#FBE9E7",
                           edgecolor="white", linewidth=1))
    ax.text(left + colw * 1.5, 4.43, "表面噪声", ha="center", va="center",
            fontsize=9.5, color=INK, fontweight="bold")
    ax.text(left + colw * 5.0, 4.43, "语义噪声", ha="center", va="center",
            fontsize=9.5, color=INK, fontweight="bold")

    # 列标签
    for j, n in enumerate(noises):
        ax.text(left + colw * (j + 0.5), 4.06, n, ha="center", va="center",
                fontsize=8.4, color=INK, linespacing=1.2)

    # 行标签 + 单元格
    for i, task in enumerate(tasks):
        y = top - rowh * (i + 1)
        ax.text(left - 0.12, y + rowh / 2, task, ha="right", va="center",
                fontsize=9.2, color=INK, linespacing=1.25)
        for j in range(len(noises)):
            v = values[i][j]
            x = left + colw * j
            ax.add_patch(Rectangle((x, y), colw, rowh, facecolor=fills[v],
                                   edgecolor="white", linewidth=1.2))
            if v == 0:
                ax.add_patch(Rectangle((x, y), colw, rowh, facecolor="none",
                                       edgecolor="#8D6E63", linewidth=0, hatch="///"))
            ax.text(x + colw / 2, y + rowh / 2, labels[v], ha="center", va="center",
                    fontsize=9.0, color=tcolors[v], fontweight="bold")

    # 图例
    legend_y = 0.62
    items = [(1, "低"), (2, "中"), (3, "高"), (4, "最高")]
    start = 0.30
    for k, (v, name) in enumerate(items):
        x = start + k * 1.05
        ax.add_patch(Rectangle((x, legend_y), 0.42, 0.22, facecolor=fills[v],
                               edgecolor="white", linewidth=1))
        ax.text(x + 0.50, legend_y + 0.11, name, va="center", fontsize=8.2, color=INK)
    x = start + 4 * 1.05
    ax.add_patch(Rectangle((x, legend_y), 0.42, 0.22, facecolor=fills[0],
                           edgecolor="white", linewidth=1, hatch="///"))
    ax.text(x + 0.50, legend_y + 0.11, "双面（可能有益）", va="center", fontsize=8.2, color=INK)

    fig.tight_layout(pad=0.2)
    for ext in ("svg", "png"):
        path = OUT / f"fig2-risk-matrix.{ext}"
        fig.savefig(path, format=ext, bbox_inches="tight", pad_inches=0.06,
                    dpi=300, facecolor=fig.get_facecolor())
        print("saved", path)
    plt.close(fig)


if __name__ == "__main__":
    figure_framework()
    figure_risk_matrix()
