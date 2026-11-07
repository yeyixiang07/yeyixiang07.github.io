"""Generate all figures for the KGC route comparison post.

Run
---
python figures/make_figures.py

Outputs (PNG, 220 dpi)
---------------------
fig1_lineage.png        技术路线谱系，按干预位置分层
fig2_allocation.png     上下文开销随邻居规模的增长，含 SSQR 常数线
fig3_generalization.png 跨数据集排名的稳定性
fig4_ns_backbone.png    负采样策略在三种 backbone 下的偏差
fig5_ablation.png       消融效应量，区分表示侧与训练侧
fig6_propagation.png    四阶段误差类型矩阵
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

import data as D

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

INK = "#2B2B2B"
MUTED = "#6E6E6E"
C_SINGLE = "#5B7C99"
C_MULTI = "#C08A5E"
C_NEG = "#7A8B6F"
C_OURS = "#8C3A3A"
GRID = "#DCDCDC"


def _save(fig, name: str) -> None:
    fig.savefig(os.path.join(HERE, name), dpi=220, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ 图 1
def fig_lineage() -> None:
    lanes = [
        ("推理时决策", 3, [
            ("PoG", 2024, 0.0, 0.30),
        ]),
        ("文本化与参数内化", 2, [
            ("KG-BERT", 2019, 0.0, 0.30),
            ("KGT5", 2022, 0.0, 0.30),
            ("KG-LLM", 2023, 0.0, -0.36),
            ("SSQR", 2025, 0.0, 0.30),
        ]),
        ("负采样与训练信号", 1, [
            ("KBGAN", 2018, 0.0, -0.42),
            ("NSCaching", 2019, 0.0, 0.42),
            ("SANS", 2020, 0.0, -0.42),
            ("DHNS", 2025, 0.0, 0.30),
        ]),
        ("打分函数与嵌入", 0, [
            ("TransE", 2013, 0.0, 0.30),
            ("DistMult", 2015, 0.0, 0.30),
            ("ComplEx", 2016, 0.0, -0.34),
            ("ConvE", 2018, 0.0, 0.30),
            ("RotatE", 2019, 0.0, -0.34),
        ]),
    ]
    anchors = {"PoG", "SSQR", "DHNS", "KG-LLM"}

    fig, ax = plt.subplots(figsize=(7.8, 4.1))
    for name, y, items in lanes:
        ax.axhline(y, color=GRID, linewidth=1.0, zorder=0)
        ax.text(2011.6, y, name, ha="right", va="center", fontsize=9.5,
                color=MUTED)
        for label, year, dx, dy in items:
            hero = label in anchors
            ax.scatter(year, y, s=78 if hero else 42,
                       color=C_OURS if hero else "#9AA5AD",
                       edgecolor="white", linewidth=1.2,
                       zorder=3)
            ax.annotate(label, (year, y), xytext=(year + dx, y + dy),
                        ha="center", va="center", fontsize=8.2,
                        color=INK if hero else MUTED,
                        fontweight="bold" if hero else "normal")

    ax.set_xlim(2011.2, 2026.6)
    ax.set_ylim(-0.7, 3.7)
    ax.set_yticks([])
    ax.set_xticks(range(2013, 2026, 2))
    ax.set_xlabel("发表年份", fontsize=10)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="x", labelsize=9)

    handles = [
        Line2D([], [], marker="o", linestyle="", markersize=8, color=C_OURS,
               label="本文讨论的四篇"),
        Line2D([], [], marker="o", linestyle="", markersize=6, color="#9AA5AD",
               label="背景方法"),
    ]
    ax.legend(handles=handles, frameon=False, fontsize=9, loc="upper left",
              bbox_to_anchor=(0.0, 1.06), ncol=2)
    _save(fig, "fig1_lineage.png")


# ------------------------------------------------------------------ 图 2
def fig_allocation() -> None:
    x = D.SSQR_PROMPT["x"]
    y = D.SSQR_PROMPT["mean_token"]
    labels = D.SSQR_PROMPT["labels"]

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.plot(x, y, marker="o", color=C_SINGLE, linewidth=1.8, markersize=7,
            label="常规提示（邻居展开）", zorder=3)
    ax.plot([6, 200], [16, 16], color=C_OURS, linewidth=1.8, linestyle="--",
            label="SSQR，每实体 16 token", zorder=3)

    for xi, yi, lab in zip(x, y, labels):
        if "FB15k" in lab:
            dx, dy, ha = -9, 7, "right"
        else:
            dx, dy, ha = 9, 5, "left"
        ax.annotate(f"{lab}\n{yi:,.0f} token".replace(",", " "),
                    (xi, yi), xytext=(dx, dy), textcoords="offset points",
                    ha=ha, va="bottom", fontsize=8.4, color=INK)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(6, 220)
    ax.set_ylim(10, 6000)
    ax.set_xlabel("每实体平均邻居数（对数）", fontsize=10)
    ax.set_ylabel("每实体消耗 token（对数）", fontsize=10)
    ax.grid(True, which="major", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)

    ax.text(8.5, 4200, "斜率约 1，开销随邻居数线性增长", fontsize=8.6,
            color=MUTED)
    ax.annotate("DHNS 不进入上下文\n（0 token）", (15, 34), fontsize=8.4,
                color=C_OURS, ha="center",
                bbox=dict(boxstyle="round,pad=0.32", facecolor="#F6EDED",
                          edgecolor="none"))
    ax.legend(frameon=False, fontsize=9, loc="center right",
              bbox_to_anchor=(0.98, 0.52))
    _save(fig, "fig2_allocation.png")


# ------------------------------------------------------------------ 图 3
def fig_generalization() -> None:
    groups = [
        ("单模态", D.DHNS_MAIN["single"], C_SINGLE, "o"),
        ("多模态", D.DHNS_MAIN["multi"], C_MULTI, "s"),
        ("负采样", D.DHNS_MAIN["neg"], C_NEG, "^"),
    ]
    ours = D.DHNS_MAIN["ours"]["DHNS"]
    di = {"DB15K": 0, "MKG-W": 1, "MKG-Y": 2}

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.9))
    for ax, ref, tgt, title in (
        (axes[0], "DB15K", "MKG-W", "（a）MKG-W 对 DB15K"),
        (axes[1], "DB15K", "MKG-Y", "（b）MKG-Y 对 DB15K"),
    ):
        ax.plot([18, 42], [18, 42], color=GRID, linewidth=1.2, linestyle="--",
                zorder=0)
        for _, table, color, marker in groups:
            xs = [v[di[ref]] for v in table.values()]
            ys = [v[di[tgt]] for v in table.values()]
            ax.scatter(xs, ys, s=46, color=color, marker=marker,
                       edgecolor="white", linewidth=0.8, zorder=2)
        ax.scatter(ours[di[ref]], ours[di[tgt]], s=150, color=C_OURS,
                   marker="*", edgecolor="white", linewidth=0.9, zorder=4)
        ax.annotate("DHNS", (ours[di[ref]], ours[di[tgt]]),
                    xytext=(-9, 8), textcoords="offset points",
                    fontsize=9, color=C_OURS, fontweight="bold")

        xs_all, ys_all = [], []
        for _, table, _, _ in groups:
            xs_all += [v[di[ref]] for v in table.values()]
            ys_all += [v[di[tgt]] for v in table.values()]
        r = np.corrcoef(xs_all, ys_all)[0, 1]
        ax.set_title(title, fontsize=10, color=INK, pad=8)
        ax.text(0.04, 0.94, f"$r = {r:.2f}$", transform=ax.transAxes,
                fontsize=9, color=MUTED, va="top")
        ax.set_xlabel(f"{ref} MRR", fontsize=9.5)
        ax.set_ylabel(f"{tgt} MRR", fontsize=9.5)
        ax.tick_params(labelsize=8.5)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)

    handles = [Patch(color=c, label=n) for n, _, c, _ in groups]
    handles.append(Line2D([], [], marker="*", linestyle="", markersize=11,
                          color=C_OURS, label="DHNS"))
    fig.legend(handles=handles, frameon=False, fontsize=9, ncol=4,
               loc="lower center", bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout(w_pad=2.0)
    _save(fig, "fig3_generalization.png")


# ------------------------------------------------------------------ 图 4
def fig_ns_backbone() -> None:
    names = D.DHNS_NS["rows"]
    cols = D.DHNS_NS["columns"]
    vals = np.array([[np.nan if v is None else v for v in row]
                     for row in D.DHNS_NS["values"]], dtype=float)
    best = np.nanmax(vals[:-1], axis=0, keepdims=True)
    delta = vals - best

    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    im = ax.imshow(delta, cmap="RdBu", vmin=-11, vmax=7, aspect="auto")

    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            if np.isnan(vals[i, j]):
                ax.text(j, i, "n/r", ha="center", va="center", fontsize=7.2,
                        color="#B0B0B0")
                continue
            d = delta[i, j]
            color = "white" if abs(d) > 5.5 else INK
            ax.text(j, i, f"{d:+.1f}", ha="center", va="center", fontsize=7.8,
                    color=color)

    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(["" for _ in cols])
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.tick_params(length=0)
    for x in (2.5, 5.5):
        ax.axvline(x, color="white", linewidth=2.4)

    for center, label in ((1, "TransE"), (4, "DistMult"), (7.5, "RotatE")):
        ax.text(center, -0.85, label, ha="center", va="bottom", fontsize=9.5,
                color=INK)
    for j, (_, ds) in enumerate(cols):
        ax.text(j, len(names) - 0.35, ds, ha="center", va="top", fontsize=8,
                color=MUTED, rotation=0)

    cb = fig.colorbar(im, ax=ax, pad=0.015, fraction=0.03)
    cb.set_label("相对最强基线的 ΔMRR", fontsize=8.4)
    cb.ax.tick_params(labelsize=8)
    for side in ("left", "right", "top", "bottom"):
        ax.spines[side].set_visible(False)
    _save(fig, "fig4_ns_backbone.png")


# ------------------------------------------------------------------ 图 5
def fig_ablation() -> None:
    sets = D.DHNS_ABLATION["datasets"]
    full = np.array(D.DHNS_ABLATION["full"])

    fig, ax = plt.subplots(figsize=(7.8, 3.9))
    h = 0.26
    colors = {"DB15K": "#3F5D7D", "MKG-W": "#C08A5E", "MKG-Y": "#7A8B6F"}

    ypos = []
    ylabels = []
    y = 0.0
    for label, v in (D.DHNS_ABLATION["branch_heg"]
                     + D.DHNS_ABLATION["branch_train"]):
        drop = (full - np.array(v)) / np.array(v) * 100.0
        ypos.append(y)
        ylabels.append(label)
        for k, ds in enumerate(sets):
            ax.barh(y + (1 - k) * h, drop[k], height=h, color=colors[ds],
                    edgecolor="white", linewidth=0.6)
            ax.text(drop[k] + 0.45, y + (1 - k) * h, f"{drop[k]:.1f}",
                    va="center", fontsize=7.8, color=INK)
        y += 1.0
        if label == "w/o MHLD":
            y += 0.45

    ax.set_yticks(ypos)
    ax.set_yticklabels(ylabels, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlabel("移除该项后的相对降幅（%），以移除后的模型为分母", fontsize=10)
    ax.set_xlim(0, 33)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)

    ax.text(32.6, -1.05, "MMC 与 MHLD 为 DiffHEG 的子模块，各行均与完整模型比较",
            ha="right", fontsize=8.2, color=MUTED)

    handles = [Patch(color=c, label=d) for d, c in colors.items()]
    ax.legend(handles=handles, frameon=False, fontsize=9, ncol=1,
              loc="lower right", bbox_to_anchor=(1.0, 0.02))
    _save(fig, "fig5_ablation.png")


# ------------------------------------------------------------------ 图 6
def fig_propagation() -> None:
    rows = ["KG-LLM", "SSQR", "PoG", "DHNS"]
    cols = ["表示", "选择", "推理", "监督"]
    grid = [
        [("描述改写", "unobs"), ("候选截断", "obs"), ("生成匹配", "obs"), ("", "none")],
        [("量化损失", "unobs"), ("", "none"), ("", "none"), ("", "none")],
        [("", "none"), ("剪枝假阴性", "obs"), ("答案抽取", "obs"), ("", "none")],
        [("", "none"), ("", "none"), ("", "none"), ("分布偏移", "unobs")],
    ]

    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    for i, row in enumerate(grid):
        for j, (text, state) in enumerate(row):
            y = len(rows) - 1 - i
            face = {"obs": "#E3A16F", "unobs": "#8C3A3A", "none": "#F4F4F4"}[state]
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor=face,
                                   edgecolor="white", linewidth=2.0))
            if text:
                color = "white" if state == "unobs" else INK
                ax.text(j + 0.5, y + 0.5, text, ha="center", va="center",
                        fontsize=9.2, color=color)

    ax.set_xlim(0, len(cols))
    ax.set_ylim(0, len(rows))
    ax.set_xticks([j + 0.5 for j in range(len(cols))])
    ax.set_xticklabels(cols, fontsize=10)
    ax.set_yticks([len(rows) - 1 - i + 0.5 for i in range(len(rows))])
    ax.set_yticklabels(rows, fontsize=10)
    ax.xaxis.tick_top()
    for side in ("left", "right", "bottom", "top"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)

    handles = [
        Rectangle((0, 0), 1, 1, facecolor="#E3A16F", edgecolor="white"),
        Rectangle((0, 0), 1, 1, facecolor="#8C3A3A", edgecolor="white"),
        Rectangle((0, 0), 1, 1, facecolor="#F4F4F4", edgecolor="white"),
    ]
    ax.legend(handles, ["有对应指标", "无对应指标", "该阶段未引入新误差"],
              loc="upper center", bbox_to_anchor=(0.5, -0.02),
              ncol=3, frameon=False, fontsize=9)

    fig.tight_layout()
    _save(fig, "fig6_propagation.png")


# ------------------------------------------------------------------ 图 7
def fig_ssqr_corpus() -> None:
    labels = ["移除结构分支", "移除语义分支"]
    fb = D.SSQR_ABLATION["w/o GCN"][1], D.SSQR_ABLATION["w/o semantics"][1]
    wn = D.SSQR_ABLATION["w/o GCN"][0], D.SSQR_ABLATION["w/o semantics"][0]

    x = range(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    bars_fb = ax.bar([i - width / 2 for i in x], fb, width,
                     color="#3F5D7D", label="FB15k-237")
    bars_wn = ax.bar([i + width / 2 for i in x], wn, width,
                     color="#C08A5E", label="WN18RR")

    for bars, vals in ((bars_fb, fb), (bars_wn, wn)):
        for rect, v in zip(bars, vals):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 0.35,
                    f"{v:.2f}".rstrip("0").rstrip("."),
                    ha="center", va="bottom", fontsize=9.5, color=INK)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=10.5)
    ax.set_ylabel("MRR 相对降幅（%）", fontsize=10.5)
    ax.set_ylim(0, 17.5)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    ax.tick_params(axis="y", labelsize=9)

    fig.tight_layout()
    _save(fig, "fig7_ssqr_corpus.png")


# ------------------------------------------------------------------ 框架图
if __name__ == "__main__":
    fig_lineage()
    fig_allocation()
    fig_generalization()
    fig_ns_backbone()
    fig_ablation()
    fig_propagation()
    fig_ssqr_corpus()
    print("done")
