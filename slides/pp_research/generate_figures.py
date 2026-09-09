#!/usr/bin/env python3
"""Journal-style DATA charts only for SAAR briefing.

No boxed diagrams / fake infographics — only plots from numbers.
Style: white bg, light grid, no top/right spines, colorblind-safe
(Okabe–Ito blue/orange), sans-serif, panel labels, 300 dpi + PDF.
"""

from __future__ import annotations

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
SAAR = np.array([0.934, 0.842, 0.751])
FIXED = np.array([0.939, 0.878, 0.468])
UNBOUNDED = np.array([0.718, 0.788, 0.759])
DISTANCE = np.array([0.894, 0.800, 0.736])
FULL = np.array([0.719, 0.738, 0.746])

COMP_DS = ["HUST", "Virkler", "NASA", "Sunwoda", "RWTH", "MATR19", "MATRb2", "NCMAPSS"]
COMP_ALG = ["SAAR", "V-REx", "GroupDRO", "Monotone", "LinRBF", "Engression", "GP", "TabPFN"]
COMP = np.array(
    [
        [0.958, 0.809, 0.934, 0.822, 0.710, 0.878, -0.320, 0.218],
        [0.888, 0.583, 0.554, 0.565, 0.805, 0.552, 0.539, 0.621],
        [0.584, 0.285, 0.286, 0.283, 0.550, 0.549, 0.438, -0.691],
        [0.865, -0.240, -0.295, -0.048, 0.838, 0.619, -1.598, -0.886],
        [0.743, 0.645, 0.602, -0.005, 0.385, 0.526, -0.474, -2.175],
        [0.466, 0.044, 0.272, 0.018, -2.639, -0.726, -2.461, 0.202],
        [0.862, 0.850, 0.777, 0.674, -0.781, 0.739, 0.213, 0.618],
        [0.937, 0.883, 0.880, 0.892, 0.819, 0.932, 0.804, 0.934],
    ],
    dtype=float,
)

MICH_U = [25, 26, 27, 28, 29, 30, 31, 32]
MICH_R = [0.789, 0.609, 0.813, 0.761, 0.657, 0.722, 0.496, 0.957]
BOOT = [("HUST", -25.19, -34.38, -14.54), ("RWTH", -23.27, -41.79, -8.94), ("MATR2019", -10.63, -15.67, -6.37)]

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
    ax.plot(x[x >= b], saar[x >= b], color=BLUE, lw=2.0, label="SAAR")

    ax.set_xlim(0, 8)
    ax.set_ylim(0.25, 1.05)
    ax.set_xlabel("Degradation coordinate / support distance", color=INK, fontsize=9)
    ax.set_ylabel("Prediction", color=INK, fontsize=9)
    journal_ax(ax, "y")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("OOS behavior: NN vs SAAR", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "nn_vs_saar_curves.png")


# ── 2 Main development results ───────────────────────────────────────────────

def fig_main_results():
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    models = {
        "Fixed bound": FIXED,
        "Unbounded": UNBOUNDED,
        "Distance": DISTANCE,
        "SAAR": SAAR,
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
                fontweight="bold" if name == "SAAR" else "normal",
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.6), gridspec_kw={"wspace": 0.35})

    for i, (a, b) in enumerate(zip(FIXED, SAAR)):
        ax1.plot([i, i], [a, b], color=GRID, lw=1.5, zorder=1)
        ax1.scatter([i], [a], s=55, color=GREY, edgecolors=INK, linewidths=0.5, zorder=3)
        ax1.scatter([i], [b], s=70, color=BLUE, edgecolors=INK, linewidths=0.5, zorder=3)
        d = b - a
        ax1.text(i, max(a, b) + 0.04, f"{d:+.2f}", ha="center", color=BLUE if d > 0 else ORANGE, fontsize=8, fontweight="bold")
    ax1.scatter([], [], s=55, color=GREY, edgecolors=INK, label="Fixed bound")
    ax1.scatter([], [], s=70, color=BLUE, edgecolors=INK, label="SAAR")
    ax1.set_xticks(range(3))
    ax1.set_xticklabels(DATASETS, fontsize=9)
    ax1.set_ylabel(r"$R^2$", fontsize=9)
    ax1.set_ylim(0.35, 1.08)
    journal_ax(ax1)
    ax1.legend(frameon=False, fontsize=7.5, loc="lower right")
    panel_label(ax1, "(a)")
    ax1.set_title("Fixed bound → SAAR", loc="left", fontsize=9, color=INK)

    pts = [
        ("Fixed", FIXED.mean(), FIXED.min(), GREY),
        ("Unbounded", UNBOUNDED.mean(), UNBOUNDED.min(), "#BBBBBB"),
        ("Full adapt.", FULL.mean(), FULL.min(), SKY),
        ("Distance", DISTANCE.mean(), DISTANCE.min(), ORANGE),
        ("SAAR", SAAR.mean(), SAAR.min(), BLUE),
    ]
    for name, m, mn, col in pts:
        ax2.scatter([m], [mn], s=90 if name == "SAAR" else 55, color=col, edgecolors=INK, linewidths=0.6, zorder=3)
        ax2.text(m + 0.006, mn + 0.012, name, color=INK, fontsize=7, fontweight="bold" if name == "SAAR" else "normal")
    ax2.set_xlabel(r"Mean $R^2$", fontsize=9)
    ax2.set_ylabel(r"Min $R^2$", fontsize=9)
    ax2.set_xlim(0.70, 0.88)
    ax2.set_ylim(0.40, 0.80)
    journal_ax(ax2, "both")
    panel_label(ax2, "(b)")
    ax2.set_title("Mean–min tradeoff", loc="left", fontsize=9, color=INK)
    save(fig, "ablation_panel.png")


# ── 4 Competitors ────────────────────────────────────────────────────────────

def fig_competitor():
    cmap = LinearSegmentedColormap.from_list("cb", [ORANGE, WHITE, BLUE], N=256)
    show = np.clip(COMP, -0.5, 1.0)
    fig, (ax_a, ax_b) = plt.subplots(
        1, 2, figsize=(11.2, 4.6), gridspec_kw={"width_ratios": [1.35, 1.0], "wspace": 0.28}
    )

    im = ax_a.imshow(show, aspect="auto", cmap=cmap, vmin=-0.4, vmax=1.0)
    ax_a.set_xticks(range(len(COMP_ALG)))
    ax_a.set_yticks(range(len(COMP_DS)))
    ax_a.set_xticklabels(COMP_ALG, fontsize=8)
    ax_a.set_yticklabels(COMP_DS, fontsize=9)
    ax_a.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False, length=0)
    for i in range(len(COMP_DS)):
        for j in range(len(COMP_ALG)):
            v = COMP[i, j]
            txt = f"{v:.2f}" if abs(v) < 1.5 else f"{v:.1f}"
            tc = "white" if abs(show[i, j]) > 0.55 else INK
            ax_a.text(j, i, txt, ha="center", va="center", fontsize=6.5, color=tc, fontweight="bold" if j == 0 else "normal")
    for sp in ax_a.spines.values():
        sp.set_color(INK)
        sp.set_linewidth(0.8)
    cbar = fig.colorbar(im, ax=ax_a, fraction=0.035, pad=0.02)
    cbar.set_label(r"$R^2$ (pooled)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    panel_label(ax_a, "(a)", x=-0.06, y=1.12)
    ax_a.set_title("Heatmap of pooled $R^2$", loc="left", fontsize=10, color=INK, pad=18)

    rng = np.random.default_rng(0)
    y = np.arange(len(COMP_DS))
    for j, name in enumerate(COMP_ALG):
        if name == "SAAR":
            continue
        jit = rng.uniform(-0.14, 0.14, size=len(COMP_DS))
        ax_b.scatter(COMP[:, j], y + jit, s=26, color="#B0B0B0", alpha=0.9, edgecolors="none", zorder=2)
    ax_b.scatter(COMP[:, 0], y, s=85, color=BLUE, edgecolors=INK, linewidths=0.7, zorder=4)
    ax_b.scatter(COMP[:, -1], y, s=65, facecolors="none", edgecolors=ORANGE, linewidths=1.6, zorder=3)
    ax_b.axvline(0, color=MUTED, lw=1.0, ls="--", zorder=1)
    ax_b.set_yticks(y)
    ax_b.set_yticklabels(COMP_DS, fontsize=9)
    ax_b.set_xlabel(r"$R^2$ (pooled)", fontsize=9)
    ax_b.set_xlim(-2.8, 1.15)
    journal_ax(ax_b, "x")
    ax_b.invert_yaxis()
    ax_b.legend(
        handles=[
            Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markeredgecolor=INK, markersize=8, label="SAAR"),
            Line2D([0], [0], marker="o", color="w", markerfacecolor="none", markeredgecolor=ORANGE, markersize=7, markeredgewidth=1.5, label="TabPFN"),
            Line2D([0], [0], marker="o", color="w", markerfacecolor="#B0B0B0", markersize=5, label="Others"),
        ],
        frameon=False,
        loc="lower right",
        fontsize=8,
    )
    panel_label(ax_b, "(b)", x=-0.08, y=1.05)
    ax_b.set_title("Where SAAR sits among methods", loc="left", fontsize=10, color=INK, pad=8)
    fig.suptitle("Extrapolation $R^2$ on eight positive datasets", fontsize=11, fontweight="bold", color=INK, y=1.02)

    fig.savefig(OUT / "competitor_bars.png", dpi=300, bbox_inches="tight", pad_inches=0.12)
    fig.savefig(OUT / "competitor_journal.pdf", bbox_inches="tight", pad_inches=0.12)
    fig.savefig(OUT / "competitor_journal.svg", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("wrote competitor_bars.png (+ pdf/svg)")


# ── 5 Robustness ─────────────────────────────────────────────────────────────

def fig_robustness():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.5), gridspec_kw={"wspace": 0.32})

    y = np.arange(len(BOOT))
    ax1.axvline(0, color=ORANGE, lw=1.2, ls="--")
    for i, (name, m, lo, hi) in enumerate(BOOT):
        ax1.plot([lo, hi], [i, i], color=BLUE, lw=2.2, solid_capstyle="round")
        ax1.scatter([m], [i], s=40, color=INK, zorder=3)
        ax1.text(hi + 1.0, i, f"{m:.1f}", va="center", fontsize=8, color=MUTED)
    ax1.set_yticks(y)
    ax1.set_yticklabels([b[0] for b in BOOT], fontsize=9)
    ax1.set_xlabel(r"Unit RMSE change (after − before), 95% CI", fontsize=8)
    ax1.invert_yaxis()
    journal_ax(ax1, "x")
    panel_label(ax1, "(a)")
    ax1.set_title("Bootstrap CI (below 0 = consistent gain)", loc="left", fontsize=9, color=INK)

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
    ax.bar(DATASETS, SAAR, color=BLUE, edgecolor=INK, linewidth=0.6, width=0.55)
    for i, v in enumerate(SAAR):
        ax.text(i, v + 0.02, f"{v:.3f}", ha="center", fontsize=9, color=INK, fontweight="bold")
    ax.set_ylim(0, 1.15)
    ax.set_ylabel(r"$R^2$ (5-run mean)", fontsize=9)
    journal_ax(ax)
    ax.set_title("SAAR on development trio", loc="left", fontsize=10, color=INK, fontweight="bold")
    save(fig, "summary_bars.png")


def main():
    fig_nn_vs_saar()
    fig_main_results()
    fig_ablation_panel()
    fig_competitor()
    fig_robustness()
    fig_summary_bars()
    print("done — data charts only:", OUT)


if __name__ == "__main__":
    main()
