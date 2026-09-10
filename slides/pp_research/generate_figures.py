#!/usr/bin/env python3
"""Journal-style DATA charts only for PP-X briefing.

No boxed diagrams / fake infographics — only plots from numbers.
Style: white bg, light grid, no top/right spines, colorblind-safe
(Okabe–Ito blue/orange), sans-serif, panel labels, 300 dpi + PDF.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

OUT = Path("/Users/baghyeongbae/Desktop/연구/ppt/pp/_build/figs")
OUT.mkdir(parents=True, exist_ok=True)

# Colorblind-safe (Okabe–Ito); avoid red–green
INK = "#222222"
MUTED = "#666666"
GRID = "#E8E8E8"
WHITE = "#FFFFFF"
BLUE = "#0072B2"
ORANGE = "#E69F00"
SKY = "#56B4E9"
GREY = "#999999"
DARK = "#333333"

DATASETS = ["Sunwoda", "RWTH", "MICH"]
DUAL = np.array([0.934, 0.842, 0.751])  # joint dual-scale executor, not the whole PP-X
FIXED = np.array([0.939, 0.878, 0.468])
UNBOUNDED = np.array([0.718, 0.788, 0.759])
DISTANCE = np.array([0.894, 0.800, 0.736])
FULL = np.array([0.719, 0.738, 0.746])

# 1D strict-extrapolation nine only. NaN = not run on that split.
COMP_DS = ["HUST", "Sunwoda", "N-CMAPSS", "Virkler", "RWTH", "MATRb2", "MICH", "NASA", "MATR19"]
COMP_ALG = ["PP-X", "V-REx", "GroupDRO", "Monotone", "LinRBF", "Engression", "GP", "TabPFN"]
NAN = np.nan
COMP = np.array(
    [
        [0.958, 0.809, 0.934, 0.822, 0.710, 0.878, -0.320, 0.218],
        [0.939, -0.240, -0.295, -0.048, 0.838, 0.619, -1.598, -0.886],
        [0.937, 0.883, 0.880, 0.892, 0.819, 0.932, 0.804, 0.934],
        [0.888, 0.583, 0.554, 0.565, 0.805, 0.552, 0.539, 0.621],
        [0.878, 0.645, 0.602, -0.005, 0.385, 0.526, -0.474, -2.175],
        [0.862, 0.850, 0.777, 0.674, -0.781, 0.739, 0.213, 0.618],
        [0.751, -0.750, -0.750, -0.743, -2.729, -1.580, -2.247, -1.860],
        [0.584, 0.285, 0.286, 0.283, 0.550, 0.549, 0.438, -0.691],
        [0.466, 0.044, 0.272, 0.018, -2.639, -0.726, -2.461, 0.202],
    ],
    dtype=float,
)

MICH_U = [25, 26, 27, 28, 29, 30, 31, 32]
MICH_R = [0.789, 0.609, 0.813, 0.761, 0.657, 0.722, 0.496, 0.957]

# unit log-RMSE ratio vs stored comparison; JOURNAL_EVIDENCE_COMPLETE_KO.md
UNIT_LOG = [
    ("Sunwoda", 0.458, 0.323, 0.625, 9, 9),
    ("MATRb2", 1.109, 0.762, 1.434, 9, 9),
    ("N-CMAPSS", 0.684, 0.257, 1.130, 3, 3),
    ("RWTH", 0.510, 0.138, 0.778, 7, 8),
    ("MICH", 0.232, -0.004, 0.521, 6, 8),
    ("HUST", 0.222, -0.106, 0.548, 10, 16),
    ("Virkler", 0.162, -0.681, 0.864, 8, 10),
    ("NASA", 0.113, -0.177, 0.450, 2, 4),
    ("MATR2019", 0.053, -0.085, 0.181, 6, 10),
]

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "AppleGothic"],
        "axes.unicode_minus": False,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "axes.linewidth": 1.0,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
    }
)


def save(fig, name: str, also_pdf: bool = True):
    fig.savefig(OUT / name, dpi=300, bbox_inches="tight", pad_inches=0.12)
    if also_pdf:
        pdf_name = name.replace(".png", ".pdf")
        fig.savefig(OUT / pdf_name, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("wrote", name)


def journal_ax(ax, grid="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)
    if grid == "y":
        ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0)
    elif grid == "x":
        ax.xaxis.grid(True, color=GRID, lw=0.6, zorder=0)
    elif grid == "both":
        ax.grid(True, color=GRID, lw=0.6, zorder=0)
    ax.set_axisbelow(True)


def panel_label(ax, lab, x=-0.08, y=1.06):
    ax.text(x, y, lab, transform=ax.transAxes, fontsize=12, fontweight="bold", color=INK, va="bottom")


# ── 1 Mechanism curves (illustrative, but plotted as a figure) ────────────────

def fig_nn_vs_saar():
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    x = np.linspace(0, 8, 400)
    b = 4.0
    true = 0.88 - 0.07 * x
    nn = np.where(x <= b, true, true[np.searchsorted(x, b)] + 0.02 * (x - b) + 0.045 * (x - b) ** 2)
    saar = np.where(x <= b, true, true[np.searchsorted(x, b)] - 0.055 * (x - b) + 0.008 * np.tanh(x - b))

    ax.axvspan(0, b, color="#F3F3F3", zorder=0)
    ax.axvline(b, color=MUTED, ls=":", lw=1.2)
    ax.text(b + 0.1, 0.98, "support boundary", color=MUTED, fontsize=8)

    ax.plot(x[x <= b], true[x <= b], color=DARK, lw=1.8, label="Observed")
    ax.plot(x[x >= b], true[x >= b], color=DARK, lw=1.5, ls="--", label="Plausible true")
    ax.plot(x[x >= b], nn[x >= b], color=ORANGE, lw=1.8, ls="-.", label="Unconstrained NN")
    ax.plot(x[x >= b], saar[x >= b], color=BLUE, lw=2.0, label="PP-X core")

    ax.set_xlim(0, 8)
    ax.set_ylim(0.25, 1.05)
    ax.set_xlabel("Degradation coordinate / support distance", color=INK, fontsize=9)
    ax.set_ylabel("Prediction", color=INK, fontsize=9)
    journal_ax(ax, "y")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("OOS behavior: NN vs PP-X", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "nn_vs_saar_curves.png")


# ── 2 Main development results ───────────────────────────────────────────────

def fig_main_results():
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    models = {
        "Fixed bound": FIXED,
        "Unbounded": UNBOUNDED,
        "Distance": DISTANCE,
        "Dual-scale": DUAL,
    }
    colors = [GREY, "#BBBBBB", SKY, BLUE]
    hatches = ["", "//", "..", ""]
    x = np.arange(len(DATASETS))
    w = 0.18
    for i, (name, vals) in enumerate(models.items()):
        off = (i - 1.5) * w
        bars = ax.bar(
            x + off, vals, w, color=colors[i], edgecolor=INK, linewidth=0.6,
            label=name, hatch=hatches[i], zorder=2,
        )
        for b, v in zip(bars, vals):
            ax.text(
                b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}",
                ha="center", va="bottom", fontsize=7, color=INK,
                fontweight="bold" if name == "Dual-scale" else "normal",
            )
    ax.set_xticks(x)
    ax.set_xticklabels(DATASETS, fontsize=9)
    ax.set_ylabel(r"$R^2$ (5-run mean)", fontsize=9, color=INK)
    ax.set_ylim(0, 1.15)
    journal_ax(ax)
    ax.legend(frameon=False, ncol=4, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, 1.14))
    ax.set_title("Development results (3 datasets)", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "results_panel.png")


# ── 3 Ablation ───────────────────────────────────────────────────────────────

def fig_ablation_panel():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 5.4), gridspec_kw={"wspace": 0.32})

    for i, (a, b) in enumerate(zip(FIXED, DUAL)):
        ax1.plot([i, i], [a, b], color="#CCCCCC", lw=2.0, zorder=1)
        ax1.scatter([i], [a], s=110, color=GREY, edgecolors=INK, linewidths=0.8, zorder=3)
        ax1.scatter([i], [b], s=140, color=BLUE, edgecolors=INK, linewidths=0.8, zorder=3)
        d = b - a
        ax1.text(
            i,
            max(a, b) + 0.045,
            f"{d:+.3f}",
            ha="center",
            color=BLUE if d > 0 else ORANGE,
            fontsize=13,
            fontweight="bold",
        )
    ax1.scatter([], [], s=110, color=GREY, edgecolors=INK, label="Fixed bound")
    ax1.scatter([], [], s=140, color=BLUE, edgecolors=INK, label="Dual-scale")
    ax1.set_xticks(range(3))
    ax1.set_xticklabels(DATASETS, fontsize=13, fontweight="bold")
    ax1.set_ylabel(r"$R^2$", fontsize=13)
    ax1.set_ylim(0.38, 1.10)
    ax1.tick_params(labelsize=12)
    journal_ax(ax1)
    ax1.legend(frameon=False, fontsize=12, loc="lower right")
    panel_label(ax1, "(a)")
    ax1.set_title("Fixed bound → dual-scale", loc="left", fontsize=14, color=INK, fontweight="bold")

    pts = [
        ("Fixed bound", FIXED.mean(), FIXED.min(), GREY, 110),
        ("Unbounded", UNBOUNDED.mean(), UNBOUNDED.min(), "#BBBBBB", 95),
        ("Full adapt.", FULL.mean(), FULL.min(), SKY, 95),
        ("Distance", DISTANCE.mean(), DISTANCE.min(), ORANGE, 95),
        ("Dual-scale", DUAL.mean(), DUAL.min(), BLUE, 150),
    ]
    for name, m, mn, col, sz in pts:
        ax2.scatter([m], [mn], s=sz, color=col, edgecolors=INK, linewidths=0.8, zorder=3, label=name)
    ax2.annotate(
        "Dual-scale\nmean 0.84 · min 0.75",
        xy=(DUAL.mean(), DUAL.min()),
        xytext=(0.845, 0.62),
        fontsize=11,
        color=BLUE,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2),
        ha="left",
    )
    ax2.annotate(
        "Fixed bound\nmin 0.47 (MICH)",
        xy=(FIXED.mean(), FIXED.min()),
        xytext=(0.695, 0.42),
        fontsize=11,
        color=MUTED,
        arrowprops=dict(arrowstyle="->", color=GREY, lw=1.1),
        ha="left",
    )
    ax2.set_xlabel(r"Mean $R^2$  (Sun · RWTH · MICH)", fontsize=12)
    ax2.set_ylabel(r"Min $R^2$", fontsize=13)
    ax2.set_xlim(0.68, 0.92)
    ax2.set_ylim(0.38, 0.86)
    ax2.tick_params(labelsize=11)
    journal_ax(ax2, "both")
    ax2.legend(frameon=False, fontsize=11, loc="upper left", markerscale=0.9)
    panel_label(ax2, "(b)")
    ax2.set_title("Mean–min tradeoff", loc="left", fontsize=14, color=INK, fontweight="bold")
    save(fig, "ablation_panel.png")


# ── 4 Competitors ────────────────────────────────────────────────────────────

def fig_competitor():
    cmap = LinearSegmentedColormap.from_list("cb", ["#C45C00", "#FFFFFF", "#005A8C"], N=256)
    show = np.clip(np.where(np.isnan(COMP), 0.0, COMP), -0.5, 1.0)
    # two-line bottom labels: name + rank/score so headers never collide
    col_meta = [
        ("PP-X", "1  ·  0.81", BLUE),
        ("V-REx", "3  ·  0.35", DARK),
        ("GroupDRO", "2  ·  0.36", ORANGE),
        ("Monotone", "", MUTED),
        ("LinRBF", "", MUTED),
        ("Engression", "", MUTED),
        ("GP", "", MUTED),
        ("TabPFN", "", MUTED),
    ]
    fig, (ax_a, ax_b) = plt.subplots(
        1, 2, figsize=(14.6, 7.0), gridspec_kw={"width_ratios": [1.42, 1.0], "wspace": 0.24}
    )

    im = ax_a.imshow(show, aspect="auto", cmap=cmap, vmin=-0.4, vmax=1.0)
    ax_a.set_xticks(np.arange(-0.5, len(COMP_ALG), 1), minor=True)
    ax_a.set_yticks(np.arange(-0.5, len(COMP_DS), 1), minor=True)
    ax_a.grid(which="minor", color="white", linestyle="-", linewidth=1.4)
    ax_a.tick_params(which="minor", bottom=False, left=False)
    ax_a.set_xticks([])
    ax_a.set_yticks(range(len(COMP_DS)))
    ax_a.set_yticklabels(COMP_DS, fontsize=12, fontweight="bold")
    ax_a.tick_params(top=False, bottom=False, labeltop=False, labelbottom=False, length=0, colors=INK)
    for i in range(len(COMP_DS)):
        for j in range(len(COMP_ALG)):
            v = COMP[i, j]
            if np.isnan(v):
                ax_a.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color="#EEEEEE", zorder=2))
                ax_a.text(j, i, "—", ha="center", va="center", fontsize=13, color=MUTED, fontweight="bold", zorder=3)
                continue
            txt = f"{v:.2f}"
            strong = abs(show[i, j]) > 0.45
            tc = "white" if strong else INK
            ax_a.text(j, i, txt, ha="center", va="center", fontsize=12, color=tc, fontweight="bold", zorder=3)
    for j, (name, rank, col) in enumerate(col_meta):
        ax_a.text(
            j,
            8.72,
            name,
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
            color=INK,
            clip_on=False,
        )
        if rank:
            ax_a.text(
                j,
                9.18,
                rank,
                ha="center",
                va="top",
                fontsize=9,
                fontweight="bold",
                color=col,
                clip_on=False,
            )
            ax_a.text(
                j,
                -0.72,
                rank.split("·")[0].strip(),
                ha="center",
                va="center",
                fontsize=10,
                color="white",
                fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.22", facecolor=col, edgecolor="none"),
                clip_on=False,
            )
    for sp in ax_a.spines.values():
        sp.set_color(INK)
        sp.set_linewidth(1.2)
    cbar = fig.colorbar(im, ax=ax_a, fraction=0.04, pad=0.02)
    cbar.set_label(r"$R^2$ (pooled)", fontsize=11)
    cbar.ax.tick_params(labelsize=10)
    panel_label(ax_a, "(a)", x=-0.07, y=1.12)
    ax_a.set_title("Heatmap of pooled $R^2$", loc="left", fontsize=13, color=INK, pad=22, fontweight="bold")

    rng = np.random.default_rng(0)
    y = np.arange(len(COMP_DS))
    for j, name in enumerate(COMP_ALG):
        if name == "PP-X":
            continue
        vals = COMP[:, j]
        mask = ~np.isnan(vals)
        jit = rng.uniform(-0.12, 0.12, size=int(mask.sum()))
        ax_b.scatter(vals[mask], y[mask] + jit, s=48, color="#8A8A8A", alpha=0.95, edgecolors=INK, linewidths=0.4, zorder=2)
    ax_b.scatter(COMP[:, 0], y, s=150, color=BLUE, edgecolors=INK, linewidths=1.0, zorder=4)
    tab = COMP[:, -1]
    tmask = ~np.isnan(tab)
    ax_b.scatter(tab[tmask], y[tmask], s=110, facecolors="none", edgecolors=ORANGE, linewidths=2.2, zorder=3)
    ax_b.axvline(0, color=INK, lw=1.2, ls="--", zorder=1)
    ax_b.set_yticks(y)
    ax_b.set_yticklabels(COMP_DS, fontsize=12, fontweight="bold")
    ax_b.set_xlabel(r"$R^2$ (pooled)", fontsize=12)
    ax_b.set_xlim(-2.8, 1.18)
    journal_ax(ax_b, "x")
    ax_b.tick_params(labelsize=11)
    ax_b.invert_yaxis()
    ax_b.legend(
        handles=[
            Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markeredgecolor=INK, markersize=11, label="PP-X  (1)"),
            Line2D([0], [0], marker="o", color="w", markerfacecolor="none", markeredgecolor=ORANGE, markersize=10, markeredgewidth=2.0, label="TabPFN"),
            Line2D([0], [0], marker="o", color="w", markerfacecolor="#8A8A8A", markeredgecolor=INK, markersize=7, label="Others"),
        ],
        frameon=False,
        loc="lower right",
        fontsize=11,
    )
    panel_label(ax_b, "(b)", x=-0.10, y=1.12)
    ax_b.set_title("Where PP-X sits among methods", loc="left", fontsize=13, color=INK, pad=22, fontweight="bold")
    fig.suptitle(r"Extrapolation $R^2$ on nine 1D-strict datasets", fontsize=14, fontweight="bold", color=INK, y=1.02)
    fig.text(
        0.08,
        -0.04,
        "Rank 1–3 (circled):  PP-X  0.81     GroupDRO  0.36     V-REx  0.35     (next: Engression 0.28)\n"
        "Rank = mean pooled $R^2$ on all nine 1D-strict splits.  Robust = # of 9 with $R^2>0$  (PP-X 9/9; GroupDRO and V-REx 7/9).\n"
        "MICH TabPFN = local v3 CPU, seeds 42–46, 1,000-row cap, same 202-row split (ensemble $R^2=-1.86$).",
        fontsize=11,
        color=INK,
        ha="left",
        va="top",
        linespacing=1.45,
    )

    fig.subplots_adjust(bottom=0.16, top=0.86, left=0.06, right=0.98)
    fig.savefig(OUT / "competitor_bars.png", dpi=400, bbox_inches="tight", pad_inches=0.32)
    fig.savefig(OUT / "competitor_journal.pdf", bbox_inches="tight", pad_inches=0.22)
    fig.savefig(OUT / "competitor_journal.svg", bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)
    print("wrote competitor_bars.png (+ pdf/svg)")


# ── 5 Robustness ─────────────────────────────────────────────────────────────

def fig_robustness():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 4.2), gridspec_kw={"wspace": 0.32})

    y = np.arange(len(UNIT_LOG))
    ax1.axvline(0, color=ORANGE, lw=1.2, ls="--")
    for i, (name, m, lo, hi, _w, _n) in enumerate(UNIT_LOG):
        col = BLUE if lo > 0 else GREY
        ax1.plot([lo, hi], [i, i], color=col, lw=2.0, solid_capstyle="round")
        ax1.scatter([m], [i], s=36, color=INK, zorder=3)
        ax1.text(hi + 0.04, i, f"{m:.2f}", va="center", fontsize=7, color=MUTED)
    ax1.set_yticks(y)
    ax1.set_yticklabels([b[0] for b in UNIT_LOG], fontsize=8)
    ax1.set_xlabel(r"Unit log-RMSE ratio  (PP better if $>0$), 95% CI", fontsize=8)
    ax1.set_xlim(-0.9, 1.7)
    ax1.invert_yaxis()
    journal_ax(ax1, "x")
    panel_label(ax1, "(a)")
    ax1.set_title("Nine-dataset unit bootstrap", loc="left", fontsize=9, color=INK)

    ax2.bar([str(u) for u in MICH_U], MICH_R, color=BLUE, edgecolor=INK, linewidth=0.5, width=0.7)
    ax2.axhline(0.751, color=ORANGE, ls="--", lw=1.3, label="pooled 0.751")
    for i, v in enumerate(MICH_R):
        ax2.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=7, color=INK)
    ax2.set_ylabel(r"Within-unit $R^2$", fontsize=9)
    ax2.set_xlabel("MICH test unit", fontsize=9)
    ax2.set_ylim(0, 1.15)
    journal_ax(ax2)
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    panel_label(ax2, "(b)")
    ax2.set_title("MICH: 8/8 units with positive $R^2$", loc="left", fontsize=9, color=INK)
    save(fig, "robustness_panel.png")


# ── 6 KPI mini bars (optional for summary slide) ─────────────────────────────

def fig_summary_bars():
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    ax.bar(DATASETS, DUAL, color=BLUE, edgecolor=INK, linewidth=0.6, width=0.55)
    for i, v in enumerate(DUAL):
        ax.text(i, v + 0.02, f"{v:.3f}", ha="center", fontsize=9, color=INK, fontweight="bold")
    ax.set_ylim(0, 1.15)
    ax.set_ylabel(r"$R^2$ (5-run mean)", fontsize=9)
    journal_ax(ax)
    ax.set_title("Dual-scale executor on development trio", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "summary_bars.png")


def fig_ppx_portfolio():
    names = [
        "HUST",
        "Sunwoda",
        "N-CMAPSS",
        "Virkler",
        "RWTH",
        "MATR batch2",
        "MICH",
        "NASA PCoE",
        "MATR 2019",
    ]
    vals = [0.958, 0.939, 0.937, 0.888, 0.878, 0.862, 0.751, 0.584, 0.466]
    execs = [
        "transport",
        "fixed BQ",
        "multiscale",
        "gated residual",
        "fixed BQ",
        "decay+transport",
        "dual-scale",
        "multiscale",
        "cal. latent",
    ]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    y = np.arange(len(names))
    ax.barh(y, vals, color=BLUE, edgecolor=INK, lw=0.5, height=0.62)
    for i, (v, e) in enumerate(zip(vals, execs)):
        ax.text(v + 0.015, i, f"{v:.3f}   {e}", va="center", fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel(r"PP-X v1.0 pooled $R^2$", fontsize=9)
    ax.set_xlim(0, 1.28)
    ax.invert_yaxis()
    journal_ax(ax, "x")
    ax.set_title("PP-X on nine 1D-strict datasets (evidence-selected executor)", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "ppx_portfolio.png")


# ── 7 Component ΔR² ──────────────────────────────────────────────────────────

def fig_component_delta():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.6), gridspec_kw={"wspace": 0.28, "width_ratios": [1, 1.35]})
    labs1 = ["Sunwoda", "RWTH", "MICH"]
    res = [0.658, 0.219, 3.811]
    ax1.axhline(0, color=INK, lw=0.8)
    ax1.bar(labs1, res, color=BLUE, edgecolor=INK, lw=0.5, width=0.55)
    for i, v in enumerate(res):
        ax1.text(i, v + 0.08, f"{v:+.2f}", ha="center", fontsize=8, color=INK, fontweight="bold")
    ax1.set_ylabel(r"$\Delta R^2$", fontsize=9)
    ax1.set_ylim(0, 4.4)
    journal_ax(ax1)
    panel_label(ax1, "(a)")
    ax1.set_title("Nonlinear residual", loc="left", fontsize=9, color=INK)

    labs2 = [
        "Freeze\nSun",
        "Freeze\nMICH",
        "Bound\nSun",
        "Bound\nMICH",
        "Dual-sc.\nMICH",
        "History\nRWTH",
        "History\nMICH",
        "Transp.\nMATRb2",
    ]
    vals2 = [0.039, 0.149, 0.221, -0.291, 0.283, 1.256, -0.247, 0.187]
    cols2 = [BLUE if v >= 0 else ORANGE for v in vals2]
    x = np.arange(len(vals2))
    ax2.axhline(0, color=INK, lw=0.8)
    ax2.bar(x, vals2, color=cols2, edgecolor=INK, lw=0.5, width=0.7)
    for i, v in enumerate(vals2):
        ax2.text(i, v + (0.06 if v >= 0 else -0.14), f"{v:+.2f}", ha="center", fontsize=6.5, color=INK)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labs2, fontsize=7)
    ax2.set_ylabel(r"$\Delta R^2$", fontsize=9)
    ax2.set_ylim(-0.5, 1.5)
    journal_ax(ax2)
    panel_label(ax2, "(b)")
    ax2.set_title("Conditional modules", loc="left", fontsize=9, color=INK)
    save(fig, "ablation_delta.png")


def fig_matched_arms():
    fig, ax = plt.subplots(figsize=(10.2, 5.0))
    arms = ["Direct\nNN", "Soft\nbdry", "Trainable\nhard-bdry", "Affine\nonly", "Unbounded", "Fixed BQ"]
    sun = [-1.352, -3.107, 0.900, 0.281, 0.718, 0.939]
    rw = [0.633, 0.483, 0.855, 0.659, 0.788, 0.878]
    mi = [0.684, -0.057, 0.319, -3.343, 0.759, 0.468]
    floor = -0.95
    sun_p = [max(v, floor) for v in sun]
    mi_p = [max(v, floor) for v in mi]
    x = np.arange(len(arms))
    w = 0.24
    ax.bar(x - w, sun_p, w, color=GREY, edgecolor=INK, lw=0.6, label="Sunwoda")
    ax.bar(x, rw, w, color=SKY, edgecolor=INK, lw=0.6, label="RWTH")
    ax.bar(x + w, mi_p, w, color=BLUE, edgecolor=INK, lw=0.6, label="MICH")
    ax.axhline(0, color=INK, lw=1.0)
    box = dict(boxstyle="round,pad=0.28", facecolor=WHITE, edgecolor=INK, linewidth=1.0)
    for xpos, val, lab in (
        (0 - w, sun[0], "Sun  −1.35"),
        (1 - w, sun[1], "Sun  −3.11"),
        (3 + w, mi[3], "MICH  −3.34"),
    ):
        ax.annotate(
            lab,
            xy=(xpos, floor),
            xytext=(xpos, -0.55),
            ha="center",
            va="center",
            fontsize=11,
            color=INK,
            fontweight="bold",
            bbox=box,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.0),
        )
    ax.set_xticks(x)
    ax.set_xticklabels(arms, fontsize=11)
    ax.set_ylabel(r"Ensemble $R^2$", fontsize=12)
    ax.set_ylim(-1.08, 1.18)
    ax.tick_params(labelsize=11)
    journal_ax(ax)
    ax.legend(frameon=False, ncol=3, fontsize=12, loc="upper left")
    ax.set_title("Matched 6-arm ablation (ensemble $R^2$)", loc="left", fontsize=14, color=INK, fontweight="bold")
    save(fig, "ablation_arms.png")


def fig_matr_2x2():
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    z = np.array([[0.674, 0.820], [0.675, 0.862]])
    cmap = LinearSegmentedColormap.from_list("b", ["#F4F4F4", BLUE])
    im = ax.imshow(z, cmap=cmap, vmin=0.60, vmax=0.90)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Transport off", "Transport on"], fontsize=8)
    ax.set_yticklabels(["Decay off", "Decay on"], fontsize=8)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{z[i, j]:.3f}", ha="center", va="center", fontsize=12, color=INK, fontweight="bold")
    ax.set_title("MATRb2  ·  decay × transport", loc="left", fontsize=10, color=INK, fontweight="bold")
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=7)
    cbar.set_label(r"Ensemble $R^2$", fontsize=8)
    save(fig, "ablation_matr.png")


def fig_history_ablation():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    labs = ["Margin only", "Margin hist.", "Margin+cycle", "Full rate hist."]
    sun = [0.590, 0.550, 0.777, 0.939]
    rw = [-0.378, -0.197, -0.251, 0.878]
    mi = [0.672, 0.715, 0.702, 0.468]
    x = np.arange(len(labs))
    w = 0.24
    ax.bar(x - w, sun, w, color=GREY, edgecolor=INK, lw=0.4, label="Sunwoda")
    ax.bar(x, rw, w, color=SKY, edgecolor=INK, lw=0.4, label="RWTH")
    ax.bar(x + w, mi, w, color=BLUE, edgecolor=INK, lw=0.4, label="MICH")
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=8)
    ax.set_ylabel(r"Ensemble $R^2$", fontsize=9)
    ax.set_ylim(-0.55, 1.15)
    journal_ax(ax)
    ax.legend(frameon=False, ncol=3, fontsize=8)
    ax.set_title("Causal history ablation", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "ablation_history.png")


def fig_gate_audit():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), gridspec_kw={"wspace": 0.32})
    cats = ["Improve", "Hold", "Worsen"]
    vals = [3, 10, 0]
    cols = [BLUE, GREY, ORANGE]
    ax1.bar(cats, vals, color=cols, edgecolor=INK, lw=0.5, width=0.55)
    for i, v in enumerate(vals):
        ax1.text(i, v + 0.25, str(v), ha="center", fontsize=11, fontweight="bold", color=INK)
    ax1.set_ylabel("Settings (n = 13)", fontsize=9)
    ax1.set_ylim(0, 12)
    journal_ax(ax1)
    panel_label(ax1, "(a)")
    ax1.set_title("Evidence gate audit", loc="left", fontsize=9, color=INK)

    # consensus binomial
    votes = ["4/5", "5/5"]
    pvals = [0.1875, 0.03125]
    ax2.bar(votes, pvals, color=[ORANGE, BLUE], edgecolor=INK, lw=0.5, width=0.5)
    ax2.axhline(0.05, color=INK, ls="--", lw=1.2, label=r"$\alpha=0.05$")
    ax2.text(0, 0.20, "reject", ha="center", fontsize=8, color=ORANGE)
    ax2.text(1, 0.045, "accept", ha="center", va="bottom", fontsize=8, color=BLUE)
    ax2.set_ylabel("One-sided binomial p", fontsize=9)
    ax2.set_ylim(0, 0.25)
    journal_ax(ax2)
    ax2.legend(frameon=False, fontsize=8)
    panel_label(ax2, "(b)")
    ax2.set_title("Seed consensus rule", loc="left", fontsize=9, color=INK)
    save(fig, "stats_gate.png")


def fig_v11_gate_ablation():
    source = Path(
        "/Users/baghyeongbae/Desktop/연구/pp-extrapolation/"
        "results/stanford_ppx_v11_gate_ablation/results.json"
    )
    data = json.loads(source.read_text())["arms"]
    names = ["Prior\nalways-on", "v1.1\nval gate", "Matched\nMLP"]
    keys = ["prior_always_on", "v11_validation_gate", "matched_mlp_fallback"]
    r2 = [data[key]["test"]["pooled"]["r2"] for key in keys]
    rmse = [data[key]["test"]["pooled"]["rmse"] for key in keys]
    colors = [ORANGE, BLUE, GREY]

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4))
    x = np.arange(3)
    axes[0].bar(x, r2, color=colors, edgecolor=INK, linewidth=0.6)
    axes[0].axhline(0, color=INK, linewidth=0.9)
    axes[0].set_xticks(x, names)
    axes[0].set_ylabel(r"Test pooled $R^2$")
    axes[0].set_ylim(0, 0.13)
    for i, value in enumerate(r2):
        axes[0].text(i, value + 0.004, f"{value:.3f}", ha="center",
                     fontsize=9, fontweight="bold")
    axes[0].set_title("Prediction outcome", loc="left", fontsize=11,
                      fontweight="bold")
    journal_ax(axes[0], "y")
    panel_label(axes[0], "(a)")

    axes[1].bar(x, rmse, color=colors, edgecolor=INK, linewidth=0.6)
    axes[1].set_xticks(x, names)
    axes[1].set_ylabel("Test RMSE (cycles)")
    axes[1].set_ylim(76, 82)
    for i, value in enumerate(rmse):
        axes[1].text(i, value + 0.12, f"{value:.2f}", ha="center",
                     fontsize=9, fontweight="bold")
    axes[1].set_title("Error magnitude", loc="left", fontsize=11,
                      fontweight="bold")
    journal_ax(axes[1], "y")
    panel_label(axes[1], "(b)")
    fig.suptitle(
        "PP-X v1.1 safety-gate ablation — Stanford post-test development",
        fontsize=12, fontweight="bold", y=1.03,
    )
    fig.tight_layout()
    save(fig, "v11_gate_ablation.png")


def fig_v11_complete_trust():
    source = Path(
        "/Users/baghyeongbae/Desktop/연구/pp-extrapolation/"
        "results/ppx_v11_complete_structure_ablation/results.json"
    )
    cohorts = json.loads(source.read_text())["cohorts"]
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.45))
    for ax, (name, cohort), unit in zip(
        axes, cohorts.items(), ("cycles", "days")
    ):
        trust = np.array([row["trust"] for row in cohort["trust_dose"]])
        validation = np.array([
            row["validation"]["pooled"]["r2"] for row in cohort["trust_dose"]
        ])
        test = np.array([
            row["test"]["pooled"]["r2"] for row in cohort["trust_dose"]
        ])
        ax.plot(trust, validation, "o-", color=BLUE, lw=2, label="Validation")
        ax.plot(trust, test, "s--", color=ORANGE, lw=2, label="Test (audit only)")
        ax.axvline(0, color=GREY, lw=0.8)
        ax.set_xlabel("Fixed affine trust")
        ax.set_ylabel(r"Pooled $R^2$")
        ax.set_title(f"{name} · target in {unit}", loc="left",
                     fontsize=11, fontweight="bold")
        journal_ax(ax, "both")
        ax.legend(frameon=False, fontsize=8)
    panel_label(axes[0], "(a)")
    panel_label(axes[1], "(b)")
    fig.suptitle(
        "PP-X v1.1 trust-dose ablation · architecture selected on validation",
        fontsize=12, fontweight="bold", y=1.03,
    )
    fig.tight_layout()
    save(fig, "v11_complete_trust.png")


def fig_v11_complete_gate_seed():
    source = Path(
        "/Users/baghyeongbae/Desktop/연구/pp-extrapolation/"
        "results/ppx_v11_complete_structure_ablation/results.json"
    )
    cohorts = json.loads(source.read_text())["cohorts"]
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.45))
    names = list(cohorts)
    x = np.arange(len(names))
    width = 0.35
    fallback, always = [], []
    for cohort in cohorts.values():
        fallback.append(cohort["gate_2x2"]["margin_1_bootstrap_1"]
                        ["test"]["pooled"]["r2"])
        always.append(cohort["gate_2x2"]["margin_0_bootstrap_0"]
                      ["test"]["pooled"]["r2"])
    axes[0].bar(x - width / 2, always, width, color=ORANGE,
                edgecolor=INK, label="No gate · prior on")
    axes[0].bar(x + width / 2, fallback, width, color=BLUE,
                edgecolor=INK, label="Full v1.1 gate")
    axes[0].set_xticks(x, ["Stanford", "ISU 250 mAh"])
    axes[0].set_ylabel(r"Test pooled $R^2$")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].set_title("Gate 2×2 endpoints", loc="left",
                      fontsize=11, fontweight="bold")
    journal_ax(axes[0], "y")
    panel_label(axes[0], "(a)")

    positions, values, labels, colors = [], [], [], []
    position = 0
    for name, cohort in cohorts.items():
        indexed = {row["key"]: row for row in cohort["grid_rows"]}
        for label, key, color in (
            ("MLP", cohort["fallback"], BLUE),
            ("Prior", cohort["always_on"], ORANGE),
        ):
            positions.append(position)
            values.append([row["r2"] for row in indexed[key]["test_seed_metrics"]])
            labels.append(f"{name}\n{label}")
            colors.append(color)
            position += 1
        position += 0.45
    box = axes[1].boxplot(values, positions=positions, widths=0.55,
                          patch_artist=True, showmeans=True)
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    axes[1].axhline(0, color=INK, ls="--", lw=0.9)
    axes[1].set_xticks(positions, labels)
    axes[1].set_ylabel(r"Per-seed test $R^2$")
    axes[1].set_title("Five-seed stability", loc="left",
                      fontsize=11, fontweight="bold")
    journal_ax(axes[1], "y")
    panel_label(axes[1], "(b)")
    fig.suptitle(
        "PP-X v1.1 gate cost and seed stability",
        fontsize=12, fontweight="bold", y=1.03,
    )
    fig.tight_layout()
    save(fig, "v11_complete_gate_seed.png")


def fig_support_envelope():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    d = np.linspace(0, 4, 240)
    w = 1 / (1 + np.exp((d - 1.2) / 0.35))
    env = w * 2 + (1 - w) * 6
    ax.plot(d, env, color=BLUE, lw=2.0, label="Allowed residual envelope")
    ax.axvline(1.2, color=ORANGE, ls="--", lw=1.3)
    ax.text(1.28, 5.7, r"$\tau$", color=ORANGE, fontsize=11, fontweight="bold")
    ax.fill_between(d, 0, env, where=d <= 1.2, color=BLUE, alpha=0.12)
    ax.fill_between(d, 0, env, where=d >= 1.2, color=ORANGE, alpha=0.12)
    ax.text(0.25, 2.35, r"$B_L=2$", color=BLUE, fontsize=10, fontweight="bold")
    ax.text(2.55, 5.15, r"$B_H=6$", color=ORANGE, fontsize=10, fontweight="bold")
    ax.set_xlabel("Normalized support distance", fontsize=9)
    ax.set_ylabel("Residual bound", fontsize=9)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 6.8)
    journal_ax(ax)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.set_title("Support-adaptive dual-scale envelope", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "support_envelope.png")


def fig_extrapolation_cut():
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    h = np.linspace(1.15, 0.72, 220)
    rul = (h - 0.80) / 0.35 * 400
    cut = 1.05
    ax.plot(h, rul, color=INK, lw=1.8)
    ax.axvline(cut, color=ORANGE, ls="--", lw=1.4)
    ax.axvspan(cut, 1.16, color=BLUE, alpha=0.10)
    ax.axvspan(0.70, cut, color=ORANGE, alpha=0.10)
    ax.text(1.105, 380, "Train\nhealth still seen", ha="center", va="top", fontsize=9, color=BLUE, fontweight="bold")
    ax.text(0.88, 380, "Val / test\nbeyond train range", ha="center", va="top", fontsize=9, color=ORANGE, fontweight="bold")
    ax.text(cut - 0.012, 50, "train min.\nhealth", color=ORANGE, fontsize=8, fontweight="bold", ha="right")
    ax.set_xlim(1.16, 0.70)
    ax.set_ylim(0, 420)
    ax.set_xlabel("Health / capacity   (right = more degraded, later in life)", fontsize=9)
    ax.set_ylabel("Remaining life (RUL)", fontsize=9)
    journal_ax(ax)
    ax.set_title("Score only the tail beyond the train support", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "extrapolation_cut.png")


def fig_hull_numbers():
    names = [
        "MATR2019",
        "Sunwoda",
        "MICH",
        "RWTH",
        "NASA batt.",
        "MATR b2",
        "Virkler",
        "HUST",
        "N-CMAPSS",
    ]
    dist = [5.554, 4.421, 3.426, 2.870, 2.005, 1.898, 1.623, 1.608, 0.228]
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    y = np.arange(len(names))
    colors = [ORANGE if v < 0.5 else BLUE for v in dist]
    ax.barh(y, dist, color=colors, edgecolor=INK, lw=0.5, height=0.62)
    for i, v in enumerate(dist):
        ax.text(v + 0.08, i, f"{v:.2f} SD", va="center", fontsize=8, color=INK)
    ax.axvline(1.0, color=MUTED, ls=":", lw=1.0)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Median hull distance (train SD)", fontsize=9)
    ax.set_xlim(0, 6.8)
    ax.invert_yaxis()
    journal_ax(ax, "x")
    ax.set_title("1D ordered-coordinate hull distance  (not full feature-space)", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "hull_distance.png")


def fig_ppx_core():
    """One predictor in three steps: prior, clip residual, add."""
    fig = plt.figure(figsize=(8.6, 4.55))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.28, 0.40], hspace=0.52, wspace=0.42)

    z = np.linspace(0.0, 8.0, 400)
    y_prior = 1.15 - 0.11 * z
    r_of_z = 0.55 * (z - 3.2)
    b = 2.0
    corr = b * np.tanh(r_of_z / b)
    y_clip = np.clip(y_prior + corr, 0.0, None)
    y_free = y_prior + r_of_z

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.plot(z, y_prior, color=BLUE, lw=2.2)
    ax0.set_xlabel(r"coordinate $z$", fontsize=8)
    ax0.set_ylabel("prediction", fontsize=8)
    ax0.set_xlim(0, 8)
    ax0.set_ylim(-1.2, 3.4)
    ax0.text(0.35, 1.22, r"$y_{\mathrm{prior}}(z)$", color=BLUE, fontsize=8)
    journal_ax(ax0)
    panel_label(ax0, "(a)")
    ax0.set_title("1  Frozen prior", loc="left", fontsize=9, color=INK)

    r = np.linspace(-8.0, 8.0, 400)
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.plot(r, r, color=GREY, lw=1.4, ls="--", label="raw $r$")
    ax1.plot(r, b * np.tanh(r / b), color=BLUE, lw=2.1, label=r"$b\,\tanh(r/b)$")
    ax1.axhline(b, color=ORANGE, ls=":", lw=1.2)
    ax1.axhline(-b, color=ORANGE, ls=":", lw=1.2)
    ax1.text(5.4, b + 0.28, r"$+b$", color=ORANGE, fontsize=9, fontweight="bold")
    ax1.text(5.4, -b - 0.58, r"$-b$", color=ORANGE, fontsize=9, fontweight="bold")
    ax1.set_xlabel(r"raw residual $r(z)$", fontsize=8)
    ax1.set_ylabel("allowed correction", fontsize=8)
    ax1.set_xlim(-8, 8)
    ax1.set_ylim(-4.2, 4.2)
    journal_ax(ax1)
    ax1.legend(frameon=False, fontsize=7.2, loc="upper left")
    panel_label(ax1, "(b)")
    ax1.set_title("2  Clip the residual", loc="left", fontsize=9, color=INK)

    ax2 = fig.add_subplot(gs[0, 2])
    ax2.fill_between(z, y_prior - b, y_prior + b, color=BLUE, alpha=0.10, label=r"$y_{\mathrm{prior}}\pm b$")
    ax2.plot(z, y_prior, color=GREY, lw=1.5, ls="--", label=r"$y_{\mathrm{prior}}$")
    ax2.plot(z, y_free, color=GREY, lw=1.3, ls=":", label="prior + raw $r$")
    ax2.plot(z, y_clip, color=BLUE, lw=2.2, label=r"$\hat y$ before $D$")
    ax2.set_xlabel(r"coordinate $z$", fontsize=8)
    ax2.set_ylabel("prediction", fontsize=8)
    ax2.set_xlim(0, 8)
    ax2.set_ylim(-1.2, 3.4)
    journal_ax(ax2)
    ax2.legend(frameon=False, fontsize=6.8, loc="upper right")
    panel_label(ax2, "(c)")
    ax2.set_title("3  Add to the prior", loc="left", fontsize=9, color=INK)

    ax3 = fig.add_subplot(gs[1, :])
    ax3.axis("off")
    ax3.text(
        0.5,
        0.58,
        r"$\hat{y}=D\left\{\,y_{\mathrm{prior}}+b(z)\,\tanh\left[r(z)/b(z)\right]\,\right\}$",
        ha="center",
        va="center",
        fontsize=16,
        color=INK,
    )
    ax3.text(
        0.5,
        0.08,
        r"one model, three steps    ·    $y_{\mathrm{prior}}$: frozen affine tail    ·    $r$: source NN    ·    $b$: clip    ·    $D$: domain contract",
        ha="center",
        va="center",
        fontsize=8,
        color=MUTED,
    )
    save(fig, "ppx_core.png")


def fig_unit_wins():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.6), gridspec_kw={"wspace": 0.34})

    labs = ["vs Direct NN", "vs Soft-bdry", "vs Affine only", "vs Trainable", "vs Unbounded"]
    wins = [17, 24, 25, 20, 14]
    pvals = [0.0028, 1.13e-6, 5.96e-8, 0.071, 0.578]
    colors = [BLUE if p < 0.05 else ORANGE for p in pvals]
    ax1.barh(labs[::-1], wins[::-1], color=colors[::-1], edgecolor=INK, lw=0.5, height=0.55)
    ax1.axvline(12.5, color=MUTED, ls=":", lw=1.0)
    for i, (w, p) in enumerate(zip(wins[::-1], pvals[::-1])):
        ax1.text(w + 0.3, i, f"{w}/25   p={p:.3g}", va="center", fontsize=8, color=INK)
    ax1.set_xlim(0, 34)
    ax1.set_xlabel("Units won (Sun·RWTH·MICH, n=25)", fontsize=8)
    journal_ax(ax1, "x")
    panel_label(ax1, "(a)")
    ax1.set_title("Wilcoxon vs matched arms", loc="left", fontsize=9, color=INK)

    names = [r[0] for r in UNIT_LOG]
    won = [r[4] / r[5] for r in UNIT_LOG]
    cols = [BLUE if r[4] == r[5] else SKY for r in UNIT_LOG]
    y = np.arange(len(names))
    ax2.barh(y, won, color=cols, edgecolor=INK, lw=0.45, height=0.62)
    for i, r in enumerate(UNIT_LOG):
        ax2.text(won[i] + 0.02, i, f"{r[4]}/{r[5]}", va="center", fontsize=7, color=INK)
    ax2.set_yticks(y)
    ax2.set_yticklabels(names, fontsize=8)
    ax2.set_xlim(0, 1.28)
    ax2.set_xlabel("Unit win rate vs stored comparison", fontsize=8)
    ax2.invert_yaxis()
    journal_ax(ax2, "x")
    panel_label(ax2, "(b)")
    ax2.set_title(r"Nine datasets: 60/77 units  ·  sign $p=0.0039$", loc="left", fontsize=9, color=INK)
    save(fig, "stats_wilcoxon.png")


def main():
    fig_nn_vs_saar()
    fig_main_results()
    fig_ablation_panel()
    fig_competitor()
    fig_robustness()
    fig_summary_bars()
    fig_ppx_portfolio()
    fig_ppx_core()
    fig_extrapolation_cut()
    fig_hull_numbers()
    fig_component_delta()
    fig_matched_arms()
    fig_history_ablation()
    fig_matr_2x2()
    fig_gate_audit()
    fig_v11_gate_ablation()
    fig_v11_complete_trust()
    fig_v11_complete_gate_seed()
    fig_support_envelope()
    fig_unit_wins()
    print("done — data charts only:", OUT)


if __name__ == "__main__":
    main()
