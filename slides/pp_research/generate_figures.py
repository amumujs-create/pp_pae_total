#!/usr/bin/env python3
"""High-contrast, data-first figures for a ~12-slide SAAR briefing."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.colors import LinearSegmentedColormap

OUT = Path("/Users/baghyeongbae/Desktop/연구/ppt/pp/_build/figs")
OUT.mkdir(parents=True, exist_ok=True)

# High-contrast restrained palette (not washed out)
INK = "#111111"
MUTED = "#555555"
RULE = "#D0D0D0"
SOFT = "#F2F2F0"
WHITE = "#FFFFFF"
TEAL = "#0A5C5C"
NAVY = "#1A3355"
RED = "#9B1C1C"
GREY = "#8A8A8A"
OK = "#1F6B4A"

DPI = 300

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
        "font.family": "AppleGothic",
        "axes.unicode_minus": False,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "savefig.dpi": DPI,
        "axes.linewidth": 1.0,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "font.size": 11,
    }
)


def save(fig, name: str):
    # Fixed size save — avoid tight-crop blur when stretched in PPT
    fig.savefig(OUT / name, dpi=DPI, bbox_inches="tight", pad_inches=0.18, facecolor=WHITE)
    plt.close(fig)
    print("wrote", name)


def spines(ax, grid=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK, labelsize=10)
    if grid:
        ax.yaxis.grid(True, color=RULE, lw=0.7, zorder=0)
        ax.set_axisbelow(True)


def title(ax, text, size=13):
    ax.set_title(text, loc="left", color=INK, fontsize=size, fontweight="bold", pad=10)


# ── 1 Cover diagram / route ───────────────────────────────────────────────────

def fig_route():
    """Premium decision-route diagram — high contrast, restrained, sharp."""
    fig, ax = plt.subplots(figsize=(12.2, 5.4))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    # subtle top wash
    ax.add_patch(Rectangle((0, 4.85), 12.2, 0.55, facecolor=SOFT, edgecolor="none", zorder=0))

    ax.text(0.45, 5.15, "Assumption-Aware Extrapolation", color=TEAL, fontsize=11,
            fontweight="bold", va="center")
    ax.text(0.45, 4.55, "밖을 지탱하는 것은 데이터가 아니라 가정이다",
            color=INK, fontsize=15, fontweight="bold", va="center")

    def card(x, y, w, h, *, fc=WHITE, ec=INK, lw=1.5, accent=None):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.012,rounding_size=0.06",
            facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2,
        ))
        if accent is not None:
            ax.add_patch(Rectangle((x, y), 0.1, h, facecolor=accent, edgecolor="none", zorder=3))

    # input row — three pills
    pills = [("관측", 2.4), ("경계", 5.35), ("도메인 지식", 8.3)]
    for label, x in pills:
        ax.add_patch(FancyBboxPatch(
            (x, 3.55), 2.0, 0.55,
            boxstyle="round,pad=0.01,rounding_size=0.28",
            facecolor=WHITE, edgecolor=INK, linewidth=1.3, zorder=2,
        ))
        ax.text(x + 1.0, 3.825, label, ha="center", va="center", color=INK, fontsize=12, fontweight="bold")
    for x in [3.4, 6.35, 9.3]:
        ax.plot([x, 6.1], [3.55, 3.15], color=RULE, lw=1.2, zorder=1)

    card(3.35, 2.25, 5.5, 0.85, fc=NAVY, ec=NAVY, lw=0)
    ax.text(6.1, 2.675, "후보식이 정당화되는가?", ha="center", va="center",
            color=WHITE, fontsize=14, fontweight="bold", zorder=4)

    ax.annotate("", xy=(2.7, 1.95), xytext=(4.6, 2.25),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.8, mutation_scale=14))
    ax.annotate("", xy=(9.5, 1.95), xytext=(7.6, 2.25),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=14))
    ax.text(3.55, 2.05, "YES", color=TEAL, fontsize=10, fontweight="bold", ha="center")
    ax.text(8.65, 2.05, "NO", color=RED, fontsize=10, fontweight="bold", ha="center")

    card(0.55, 0.55, 5.0, 1.25, ec=TEAL, lw=1.6, accent=TEAL)
    ax.text(1.0, 1.45, "PAE", color=TEAL, fontsize=16, fontweight="bold", zorder=4)
    ax.text(2.05, 1.48, "equation-aware", color=MUTED, fontsize=10, zorder=4)
    ax.text(1.0, 1.05, "허용된 식 + 제한 NN", color=INK, fontsize=12, zorder=4)
    ax.text(1.0, 0.72, "다음 논문", color=MUTED, fontsize=11, zorder=4)

    card(6.65, 0.55, 5.0, 1.25, fc="#F0F7F6", ec=TEAL, lw=2.2, accent=TEAL)
    ax.text(7.1, 1.45, "SAAR", color=TEAL, fontsize=16, fontweight="bold", zorder=4)
    ax.text(8.35, 1.48, "equation-free", color=MUTED, fontsize=10, zorder=4)
    ax.add_patch(FancyBboxPatch(
        (10.35, 1.32), 1.05, 0.32,
        boxstyle="round,pad=0.01,rounding_size=0.08",
        facecolor=TEAL, edgecolor="none", zorder=4,
    ))
    ax.text(10.875, 1.48, "TODAY", ha="center", va="center", color=WHITE, fontsize=9, fontweight="bold", zorder=5)
    ax.text(7.1, 1.05, "동결 affine + dual-scale residual", color=INK, fontsize=12, zorder=4)
    ax.text(7.1, 0.72, "이번 발표 · 논문 1편", color=MUTED, fontsize=11, zorder=4)

    ax.plot([3.05, 6.1], [0.55, 0.28], color=RULE, lw=1.1, zorder=1)
    ax.plot([9.15, 6.1], [0.55, 0.28], color=RULE, lw=1.1, zorder=1)
    ax.text(6.1, 0.12, "Assurance   믿기  ·  보류  ·  거절     →     박사논문에서 두 경로 통합",
            ha="center", va="center", color=MUTED, fontsize=10.5)

    save(fig, "research_route.png")


def fig_nn_vs_saar():
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    x = np.linspace(0, 8, 400)
    b = 4.0
    true = 0.88 - 0.07 * x
    nn = np.where(x <= b, true, true[x.searchsorted(b)] + 0.02 * (x - b) + 0.045 * (x - b) ** 2)
    saar = np.where(x <= b, true, true[x.searchsorted(b)] - 0.055 * (x - b) + 0.008 * np.tanh(x - b))

    ax.axvspan(0, b, color="#E8EEED", zorder=0)
    ax.axvline(b, color=INK, ls=":", lw=1.2)
    ax.text(b + 0.08, 0.97, "support 경계", color=INK, fontsize=10, fontweight="bold")

    ax.plot(x[x <= b], true[x <= b], color=TEAL, lw=2.6, label="관측 궤적")
    ax.plot(x[x >= b], true[x >= b], color=TEAL, lw=2.0, ls="--", label="가능한 참 연장")
    ax.plot(x[x >= b], nn[x >= b], color=RED, lw=2.6, label="제약 없는 NN")
    ax.plot(x[x >= b], saar[x >= b], color=NAVY, lw=2.8, label="SAAR")

    ax.set_xlim(0, 8)
    ax.set_ylim(0.25, 1.05)
    ax.set_xlabel("열화 좌표 / support 거리", color=INK, fontsize=11)
    ax.set_ylabel("예측", color=INK, fontsize=11)
    spines(ax, grid=True)
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    title(ax, "문제: support 밖에서 NN은 폭주하고, SAAR는 affine 추세를 지킨다")
    save(fig, "nn_vs_saar_curves.png")


# ── 3 Method equation panel ───────────────────────────────────────────────────

def fig_equation():
    fig, ax = plt.subplots(figsize=(11.8, 4.8))
    ax.set_xlim(0, 11.8)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    ax.add_patch(Rectangle((0.35, 3.15), 11.1, 1.2, facecolor=SOFT, edgecolor=INK, lw=1.4))
    ax.text(5.9, 3.95, r"$\hat{y}=m\cdot\mathrm{softplus}\!\left(\ell(z)+c_\theta(z)\right)$",
            ha="center", va="center", fontsize=20, color=INK)
    ax.text(5.9, 3.4, r"$c_\theta=w\,B_L\tanh r_\theta+(1-w)\,B_H\tanh(r_\theta/B_H)$"
            r"   ·   $B_L{=}2,\;B_H{=}6$",
            ha="center", va="center", fontsize=13, color=MUTED)

    terms = [
        (0.35, r"$m$", "경계 / 스케일", TEAL),
        (3.2, r"$\ell(z)$", "동결 affine\n기본 추세", NAVY),
        (6.05, r"$c_\theta$", "dual-scale\n제한 residual", TEAL),
        (8.9, r"$w(d)$", "support 거리\ngate", RED),
    ]
    for x, t, b, col in terms:
        ax.add_patch(Rectangle((x, 0.45), 2.55, 2.4, facecolor=WHITE, edgecolor=col, lw=1.8))
        ax.text(x + 1.27, 2.35, t, ha="center", color=col, fontsize=16, fontweight="bold")
        ax.text(x + 1.27, 1.35, b, ha="center", color=INK, fontsize=12)

    title(ax, "방법: SAAR — Support-Aware Affine–Residual")
    save(fig, "pp_equation_panel.png")


# ── 4 Main results: bars + table ──────────────────────────────────────────────

def fig_main_results():
    """Bars only — numeric table lives in PPT as a native table."""
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    models = {
        "고정 경계": FIXED,
        "무제한": UNBOUNDED,
        "거리보정": DISTANCE,
        "SAAR": SAAR,
    }
    colors = [GREY, "#A8A8A8", "#6E6E6E", TEAL]
    x = np.arange(len(DATASETS))
    w = 0.18
    for i, (name, vals) in enumerate(models.items()):
        off = (i - 1.5) * w
        bars = ax.bar(x + off, vals, w, color=colors[i], edgecolor=WHITE, linewidth=0.6, label=name, zorder=2)
        for b, v in zip(bars, vals):
            ax.text(
                b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.2f}",
                ha="center", va="bottom", fontsize=8,
                color=TEAL if name == "SAAR" else INK,
                fontweight="bold" if name == "SAAR" else "normal",
            )
    ax.set_xticks(x)
    ax.set_xticklabels(DATASETS, fontsize=12, fontweight="bold")
    ax.set_ylabel(r"$R^2$ (5-run mean)", color=INK)
    ax.set_ylim(0, 1.12)
    spines(ax)
    ax.legend(frameon=False, ncol=4, loc="upper center", fontsize=10, bbox_to_anchor=(0.5, 1.02))
    title(ax, "주 결과 — 개발 3데이터 (막대)")
    save(fig, "results_panel.png")


# ── 5 Ablation slope + tradeoff ───────────────────────────────────────────────

def fig_ablation_panel():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.0), gridspec_kw={"wspace": 0.32})

    # slope
    for i, (name, a, b) in enumerate(zip(DATASETS, FIXED, SAAR)):
        ax1.plot([i, i], [a, b], color=RULE, lw=2.2, zorder=1)
        ax1.scatter([i], [a], s=70, color=GREY, zorder=3, label="고정 경계" if i == 0 else None)
        ax1.scatter([i], [b], s=90, color=TEAL, zorder=3, label="SAAR" if i == 0 else None)
        d = b - a
        ax1.text(i, max(a, b) + 0.04, f"{d:+.2f}", ha="center", color=TEAL if d > 0 else RED, fontsize=11, fontweight="bold")
    ax1.set_xticks(range(3))
    ax1.set_xticklabels(DATASETS, fontweight="bold")
    ax1.set_ylabel(r"$R^2$")
    ax1.set_ylim(0.35, 1.08)
    spines(ax1)
    ax1.legend(frameon=False, loc="lower right")
    title(ax1, "고정 경계 → SAAR")

    # tradeoff scatter
    pts = [
        ("고정 경계", FIXED.mean(), FIXED.min(), GREY),
        ("무제한", UNBOUNDED.mean(), UNBOUNDED.min(), "#A0A0A0"),
        ("전체 적응", FULL.mean(), FULL.min(), "#707070"),
        ("거리보정", DISTANCE.mean(), DISTANCE.min(), NAVY),
        ("SAAR", SAAR.mean(), SAAR.min(), TEAL),
    ]
    for name, m, mn, col in pts:
        ax2.scatter([m], [mn], s=140 if name == "SAAR" else 90, color=col, zorder=3, edgecolors=INK, linewidths=0.6)
        ax2.text(m + 0.008, mn + 0.012, name, color=col if name == "SAAR" else INK, fontsize=9, fontweight="bold" if name == "SAAR" else "normal")
    ax2.set_xlabel(r"평균 $R^2$")
    ax2.set_ylabel(r"최저 $R^2$")
    ax2.set_xlim(0.70, 0.88)
    ax2.set_ylim(0.40, 0.80)
    spines(ax2)
    title(ax2, "평균–최저 tradeoff")
    save(fig, "ablation_panel.png")


# ── 6 Competitor heatmap + bars (TabPFN included as a peer) ───────────────────

def fig_competitor():
    """One figure: heatmap of all algorithms including TabPFN, plus grouped bars."""
    fig = plt.figure(figsize=(12.2, 6.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.35, 1.0], hspace=0.38)
    ax = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    show = np.clip(COMP, -0.5, 1.0)
    cmap = LinearSegmentedColormap.from_list("rg", ["#9B1C1C", "#F2F2F0", "#0A5C5C"])
    im = ax.imshow(show, aspect="auto", cmap=cmap, vmin=-0.35, vmax=1.0)
    ax.set_xticks(range(len(COMP_ALG)))
    ax.set_yticks(range(len(COMP_DS)))
    ax.set_xticklabels(COMP_ALG, fontsize=10, fontweight="bold")
    ax.set_yticklabels(COMP_DS, fontsize=10, fontweight="bold")
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    # highlight TabPFN column header
    for j, name in enumerate(COMP_ALG):
        if name == "TabPFN":
            ax.get_xticklabels()[j].set_color(NAVY)
    for i in range(len(COMP_DS)):
        for j in range(len(COMP_ALG)):
            v = COMP[i, j]
            txt = f"{v:.2f}" if abs(v) < 1.5 else f"{v:.1f}"
            bold = j == 0 or j == len(COMP_ALG) - 1 or (v == np.nanmax(COMP[i]) and v > 0)
            ax.text(
                j, i, txt, ha="center", va="center", fontsize=8,
                color=WHITE if abs(show[i, j]) > 0.55 else INK,
                fontweight="bold" if bold else "normal",
            )
    cbar = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.015)
    cbar.set_label(r"$R^2$", color=INK)
    cbar.ax.tick_params(labelsize=8, colors=INK)
    for sp in ax.spines.values():
        sp.set_color(INK)
        sp.set_linewidth(1.0)
    title(ax, "비교 — 양의 8곳 × 전 알고리즘 (SAAR · … · TabPFN 동일 표)")

    # grouped bars: SAAR + strong baselines + TabPFN together
    key = ["SAAR", "V-REx", "GroupDRO", "LinRBF", "Engression", "TabPFN"]
    key_idx = [COMP_ALG.index(k) for k in key]
    colors = [TEAL, GREY, "#6E6E6E", NAVY, "#A0A0A0", "#C45C26"]
    x = np.arange(len(COMP_DS))
    w = 0.13
    for ki, (name, j) in enumerate(zip(key, key_idx)):
        vals = np.clip(COMP[:, j], -0.35, None)
        ax2.bar(x + (ki - 2.5) * w, vals, w, label=name, color=colors[ki], edgecolor=WHITE, linewidth=0.4)
    ax2.axhline(0, color=INK, lw=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(COMP_DS, fontsize=9, fontweight="bold")
    ax2.set_ylabel(r"$R^2$")
    ax2.set_ylim(-0.4, 1.15)
    spines(ax2)
    ax2.legend(frameon=False, ncol=6, loc="upper center", fontsize=8, bbox_to_anchor=(0.5, 1.18))
    title(ax2, "같은 수치 · 막대 요약 (TabPFN 포함)")

    save(fig, "competitor_bars.png")


# ── 7 SAAR vs TabPFN bars (kept for study PDF optional) ───────────────────────

def fig_vs_tabpfn():
    fig, ax = plt.subplots(figsize=(11.8, 5.0))
    pp = COMP[:, 0]
    pfn = COMP[:, -1]
    x = np.arange(len(COMP_DS))
    w = 0.38
    ax.bar(x - w / 2, pp, w, color=TEAL, label="SAAR", edgecolor=WHITE)
    ax.bar(x + w / 2, np.clip(pfn, -1.0, None), w, color="#C45C26", label="TabPFN", edgecolor=WHITE)
    for i, (a, b) in enumerate(zip(pp, pfn)):
        ax.text(i - w / 2, a + 0.03, f"{a:.2f}", ha="center", fontsize=8, color=INK, fontweight="bold")
        ypos = max(min(b, 1.0), -1.0)
        ax.text(i + w / 2, ypos + 0.03 if ypos > -0.9 else -0.95, f"{b:.2f}", ha="center", fontsize=8, color="#C45C26")
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(COMP_DS, fontsize=10, fontweight="bold")
    ax.set_ylabel(r"$R^2$")
    ax.set_ylim(-1.15, 1.2)
    spines(ax)
    ax.legend(frameon=False, loc="upper right")
    title(ax, "SAAR vs TabPFN (동일 표의 두 열)")
    save(fig, "pp_vs_tabpfn.png")


# ── 8 Robustness: bootstrap + MICH ────────────────────────────────────────────

def fig_robustness():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8), gridspec_kw={"wspace": 0.3})

    y = np.arange(len(BOOT))
    ax1.axvline(0, color=RED, lw=1.2, ls="--")
    for i, (name, m, lo, hi) in enumerate(BOOT):
        ax1.plot([lo, hi], [i, i], color=TEAL, lw=5, solid_capstyle="round")
        ax1.scatter([m], [i], s=55, color=INK, zorder=3)
        ax1.text(hi + 1.0, i, f"{m:.1f}  [{lo:.1f}, {hi:.1f}]", va="center", fontsize=9, color=MUTED)
    ax1.set_yticks(y)
    ax1.set_yticklabels([b[0] for b in BOOT], fontweight="bold")
    ax1.set_xlabel("unit RMSE 변화 (후-전)  ·  95% CI")
    ax1.invert_yaxis()
    spines(ax1, grid=False)
    ax1.xaxis.grid(True, color=RULE, lw=0.7)
    title(ax1, "Bootstrap CI (0 아래 = 일관 개선)")

    colors = [TEAL if v >= 0.6 else NAVY for v in MICH_R]
    bars = ax2.bar([str(u) for u in MICH_U], MICH_R, color=colors, edgecolor=WHITE)
    ax2.axhline(0.751, color=INK, ls="--", lw=1.2, label="pooled 0.751")
    for b, v in zip(bars, MICH_R):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}", ha="center", fontsize=8.5, color=INK)
    ax2.set_ylabel(r"within-unit $R^2$")
    ax2.set_xlabel("MICH test unit")
    ax2.set_ylim(0, 1.15)
    spines(ax2)
    ax2.legend(frameon=False, loc="upper left")
    title(ax2, "MICH 8/8 unit 양의 $R^2$")
    save(fig, "robustness_panel.png")


# ── 9 Failures table ──────────────────────────────────────────────────────────

def fig_failures():
    fig, ax = plt.subplots(figsize=(11.8, 4.6))
    ax.axis("off")
    headers = ["설정", "기본 PP $R^2$", "해석", "조치"]
    rows = [
        ["MICH (기본)", "-1.522", "관계 이동 · 보정 꺼짐", "경계+dual-scale → 0.751"],
        ["XJTU", "-1.229", "val/test 이동 반대", "거절 / 옮기지 않음"],
        ["FEMTO", "-1.378", "끝점 희소 · 채널 이슈", "설계 미성숙 · 보류"],
        ["NASA milling", "-4.826", "메커니즘 전이 · unit 극소", "사전 Fail / ABSTAIN"],
    ]
    tbl = ax.table(cellText=rows, colLabels=headers, loc="center", cellLoc="left", colLoc="center", bbox=[0.02, 0.12, 0.96, 0.78])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    widths = [0.18, 0.16, 0.34, 0.32]
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(RULE)
        cell.set_linewidth(0.9)
        cell.set_height(0.16)
        if r == 0:
            cell.set_facecolor(INK)
            cell.set_text_props(color=WHITE, fontweight="bold", fontsize=11)
        else:
            cell.set_facecolor(SOFT if r % 2 == 0 else WHITE)
            cell.set_text_props(color=INK if c != 1 else RED, fontweight="bold" if c == 1 else "normal")
        cell.set_width(widths[c])
    title(ax, "실패 설정 (표) — 숨기지 않고 거절 근거로 사용")
    save(fig, "fail_cases.png")


# ── 10 Status / limits + dual path ────────────────────────────────────────────

def fig_status_limits():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8), gridspec_kw={"wspace": 0.25})
    for a in (ax1, ax2):
        a.set_xlim(0, 10)
        a.set_ylim(0, 10)
        a.axis("off")

    # left KPIs
    ax1.text(0.2, 9.2, "주장하는 것", color=TEAL, fontsize=12, fontweight="bold")
    kpis = [("Sunwoda", "0.934"), ("RWTH", "0.842"), ("MICH", "0.751")]
    for i, (n, v) in enumerate(kpis):
        x = 0.4 + i * 3.1
        ax1.add_patch(Rectangle((x, 5.2), 2.8, 3.4, facecolor=WHITE, edgecolor=TEAL, lw=1.8))
        ax1.text(x + 1.4, 7.8, n, ha="center", color=MUTED, fontsize=11, fontweight="bold")
        ax1.text(x + 1.4, 6.5, v, ha="center", color=TEAL, fontsize=26, fontweight="bold")
        ax1.text(x + 1.4, 5.6, r"$R^2$", ha="center", color=MUTED, fontsize=10)
    ax1.text(0.2, 4.2, "·  연속 열화 · unit-disjoint · hull-out", color=INK, fontsize=11)
    ax1.text(0.2, 3.3, "·  고정 affine + dual-scale residual", color=INK, fontsize=11)
    ax1.text(0.2, 2.4, "·  경계 위반 0 (해당 설정)", color=INK, fontsize=11)
    ax1.text(0.2, 1.3, "분야 타깃: Q1–Q2 (RESS / MSSP / IEEE)", color=MUTED, fontsize=10)
    title(ax1, "개발 주표")

    ax2.text(0.2, 9.2, "아직 주장하지 않는 것", color=RED, fontsize=12, fontweight="bold")
    limits = [
        ("Zn / Na", "사후 개발 점수 — untouched 확증 아님"),
        ("XJTU · FEMTO", "교차도메인 우월성 전 · 감사/복구 중"),
        ("PAE", "식 라우팅 실험 없음 · 결과 표와 분리"),
        ("만능 SOTA", "모든 OOD / tabular 외삽 1등 아님"),
    ]
    for i, (h, b) in enumerate(limits):
        y = 7.6 - i * 1.7
        ax2.add_patch(Rectangle((0.2, y - 0.35), 9.4, 1.4, facecolor=SOFT if i % 2 == 0 else WHITE, edgecolor=RULE, lw=1.0))
        ax2.text(0.5, y + 0.55, h, color=INK, fontsize=12, fontweight="bold")
        ax2.text(0.5, y + 0.05, b, color=MUTED, fontsize=11)
    title(ax2, "경계")
    save(fig, "status_compact.png")


def fig_dual_path():
    fig, ax = plt.subplots(figsize=(11.8, 4.4))
    ax.set_xlim(0, 11.8)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    # SAAR
    ax.add_patch(Rectangle((0.35, 0.5), 5.3, 3.4, facecolor=WHITE, edgecolor=TEAL, lw=2.0))
    ax.text(3.0, 3.45, "SAAR  ·  equation-free", ha="center", color=TEAL, fontsize=14, fontweight="bold")
    for i, t in enumerate(["명시적 도메인 식 없음", "동결 affine + dual-scale residual", "이번 발표 / 논문 1의 주결과"]):
        ax.text(0.7, 2.6 - i * 0.65, "–  " + t, color=INK, fontsize=12)
    # PAE
    ax.add_patch(Rectangle((6.15, 0.5), 5.3, 3.4, facecolor=WHITE, edgecolor=NAVY, lw=2.0))
    ax.text(8.8, 3.45, "PAE  ·  equation-aware", ha="center", color=NAVY, fontsize=14, fontweight="bold")
    for i, t in enumerate(["후보식 검증 후 식+제한 NN", "이득 없으면 끔 / SAAR로 fallback", "다음 논문 — 이번 표와 분리"]):
        ax.text(6.5, 2.6 - i * 0.65, "–  " + t, color=INK, fontsize=12)
    title(ax, "이중 경로 — 같은 외삽, 다른 입력")
    save(fig, "pp_vs_pae_split.png")


def fig_summary_kpis():
    """Cover-adjacent one-liner numbers with tiny bars."""
    fig, ax = plt.subplots(figsize=(11.5, 3.6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    ax.text(0.3, 3.15, "SAAR  ·  equation-free safeguard", color=TEAL, fontsize=12, fontweight="bold")
    ax.text(0.3, 2.7, r"$\hat y = m\,\mathrm{softplus}(\ell + c_\theta)$", color=INK, fontsize=14)

    # mini bars
    axb = fig.add_axes([0.08, 0.18, 0.55, 0.42])
    axb.bar(DATASETS, SAAR, color=TEAL, width=0.55, edgecolor=WHITE)
    for i, v in enumerate(SAAR):
        axb.text(i, v + 0.02, f"{v:.3f}", ha="center", fontsize=11, fontweight="bold", color=INK)
    axb.set_ylim(0, 1.15)
    axb.set_ylabel(r"$R^2$")
    spines(axb)

    ax.text(7.4, 2.3, "평균  0.842", color=INK, fontsize=16, fontweight="bold")
    ax.text(7.4, 1.7, "최저  0.751 (MICH)", color=TEAL, fontsize=14, fontweight="bold")
    ax.text(7.4, 1.1, "만능 SOTA 주장 없음", color=MUTED, fontsize=12)
    ax.text(7.4, 0.55, "PAE 결과는 이번 표에 없음", color=MUTED, fontsize=12)
    title(ax, "지금 결론")
    save(fig, "summary_executive.png")


def main():
    fig_route()
    fig_nn_vs_saar()
    fig_equation()
    fig_main_results()
    fig_ablation_panel()
    fig_competitor()
    fig_vs_tabpfn()
    fig_robustness()
    fig_failures()
    fig_status_limits()
    fig_dual_path()
    fig_summary_kpis()
    print("done", OUT)


if __name__ == "__main__":
    main()
