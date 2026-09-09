#!/usr/bin/env python3
"""Generate minimal research figures for Assumption-Aware Extrapolation (SAAR / PP deck)."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path("/Users/baghyeongbae/Desktop/연구/ppt/pp/_build/figs")
OUT.mkdir(parents=True, exist_ok=True)

# ── Design system ─────────────────────────────────────────────────────────────
INK = "#1C1C1C"
MUTED = "#6A6A6A"
RULE = "#E6E6E6"
SOFT = "#F4F4F2"
WHITE = "#FFFFFF"
ACCENT = "#0F5C5C"
ACCENT2 = "#1F3A5F"
WARN = "#8B2E2E"
OK = "#2F6B4F"

DPI = 220
PAD = 0.1

DATASETS = ["Sunwoda", "RWTH", "MICH"]
SAAR = [0.934, 0.842, 0.751]
FIXED = [0.939, 0.878, 0.468]
UNBOUNDED = [0.718, 0.788, 0.759]
DISTANCE = [0.894, 0.800, 0.736]
FULL_ADAPT = [0.719, 0.738, 0.746]

DEV_MODELS = {
    "고정 경계형": FIXED,
    "보정 제한 없음": UNBOUNDED,
    "전체 적응형": FULL_ADAPT,
    "거리 기반 보정": DISTANCE,
    "SAAR": SAAR,
}

COMPETITOR_DATASETS = ["HUST", "Virkler", "NASA", "Sunwoda", "RWTH", "MATR19", "MATRb2", "NCMAPSS"]
COMPETITOR_ALGOS = ["SAAR", "V-REx", "GroupDRO", "Monotone", "LinRBF", "Engression", "GP", "TabPFN"]
COMPETITOR_MAT = np.array(
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

MICH_UNITS = [25, 26, 27, 28, 29, 30, 31, 32]
MICH_R2 = [0.789, 0.609, 0.813, 0.761, 0.657, 0.722, 0.496, 0.957]

BOOT_NAMES = ["HUST", "RWTH", "MATR2019"]
BOOT_MEANS = [-25.19, -23.27, -10.63]
BOOT_LO = [-34.38, -41.79, -15.67]
BOOT_HI = [-14.54, -8.94, -6.37]

mpl.rcParams.update(
    {
        "font.family": "AppleGothic",
        "axes.unicode_minus": False,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "savefig.bbox": "tight",
        "savefig.dpi": DPI,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "grid.linewidth": 0.4,
    }
)


def save(fig, name: str) -> None:
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=PAD)
    plt.close(fig)
    print("wrote", path)


def style_axes(ax, grid: bool = True) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=9)
    if grid:
        ax.grid(True, axis="y", color=RULE, alpha=0.3, linestyle="-")
        ax.set_axisbelow(True)


def title_left(ax, text: str, size: int = 10, pad: int = 6) -> None:
    ax.set_title(text, color=INK, fontsize=size, pad=pad, loc="left", fontweight="bold")


def thin_box(ax, x, y, w, h, *, fc=WHITE, ec=RULE, lw=0.8, zorder=1):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="square,pad=0",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def arrow_h(ax, x0, y0, x1, color=MUTED, lw=0.8):
    ax.annotate("", xy=(x1, y0), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))


def arrow_v(ax, x0, y0, y1, color=MUTED, lw=0.8):
    ax.annotate("", xy=(x0, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))


# ── Existing deck figures (minimal) ───────────────────────────────────────────

def fig_motivation():
    fig, ax = plt.subplots(figsize=(10, 3.8))
    xs_in = np.linspace(0, 4.2, 60)
    y0 = 0.82
    slope = -0.055
    y_true = y0 + slope * xs_in
    xs_out = np.linspace(4.2, 8.5, 60)
    d = xs_out - 4.2

    ax.plot(xs_in, y_true, color=ACCENT, lw=1.4, label="관측 궤적")
    ax.scatter(xs_in[::8], y_true[::8], s=14, color=ACCENT, zorder=3)

    ax.axvline(4.2, color=WARN, lw=0.8, ls="--")
    ax.text(4.25, 0.98, "support 경계", color=WARN, fontsize=8)

    ax.plot(xs_out, y0 + slope * 4.2 - 0.04 * d, color=MUTED, lw=1.0, ls="--", label="가능한 미래 A")
    ax.plot(xs_out, y0 + slope * 4.2 - 0.02 * d - 0.008 * d ** 1.3, color=MUTED, lw=1.0, ls=":", label="가능한 미래 B")
    ax.plot(xs_out, y0 + slope * 4.2 + 0.06 * d + 0.015 * d ** 1.2, color=WARN, lw=1.2, label="NN 폭주")

    ax.axvspan(0, 4.2, color=SOFT, alpha=0.5, zorder=0)
    ax.text(1.5, 0.15, "관측 구간 — 여러 함수가 비슷", color=MUTED, fontsize=8)
    ax.text(5.5, 0.15, "밖 — 가정이 방향 결정", color=INK, fontsize=8)

    ax.set_xlabel("열화 좌표 / 시간", color=MUTED, fontsize=9)
    ax.set_ylabel("예측", color=MUTED, fontsize=9)
    ax.set_xlim(-0.2, 8.8)
    ax.set_ylim(0.05, 1.05)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    title_left(ax, "모티베이션: support 밖에서는 데이터만으로 함수가 정해지지 않음")
    save(fig, "motivation_futures.png")


def fig_prior_ladder():
    fig, ax = plt.subplots(figsize=(10, 2.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.4)
    ax.axis("off")

    steps = [
        ("0", "구조 지식 없음", "일반 예측 + 거절"),
        ("1", "경계·이력", "SAAR / PP (현재)"),
        ("2", "방향·부호", "제약 신경망"),
        ("3", "수식·물리", "PAE (식+NN)"),
    ]
    ax.plot([0.6, 9.4], [1.2, 1.2], color=RULE, lw=1.0, zorder=0)
    for i, (num, name, exe) in enumerate(steps):
        x = 0.5 + i * 2.4
        ax.scatter([x], [1.2], s=40, color=ACCENT if i == 1 else MUTED, zorder=2, edgecolors=WHITE, linewidths=0.5)
        ax.text(x, 1.45, num, ha="center", color=ACCENT if i == 1 else INK, fontsize=9, fontweight="bold")
        ax.text(x, 0.85, name, ha="center", color=INK, fontsize=8, fontweight="bold")
        ax.text(x, 0.45, exe, ha="center", color=MUTED, fontsize=7.5)
    ax.text(0.3, 0.1, "약함", color=MUTED, fontsize=7)
    ax.text(9.5, 0.1, "강한 prior", color=MUTED, fontsize=7, ha="right")
    title_left(ax, "Prior ladder — PAE(식) vs SAAR(식 없는 안전장치)")
    save(fig, "prior_ladder.png")


def fig_pp_core_idea():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    thin_box(ax, 0.3, 1.0, 3.2, 1.8, fc=SOFT)
    ax.text(1.9, 2.55, "train support", ha="center", color=INK, fontsize=9, fontweight="bold")
    rng = np.random.default_rng(0)
    ax.scatter(rng.uniform(0.5, 3.3, 14), rng.uniform(1.2, 2.2, 14), s=18, color=ACCENT, zorder=3)

    ax.plot([3.6, 3.6], [0.8, 2.9], color=WARN, lw=0.8, ls="--")
    ax.text(3.65, 2.95, "support 끝", color=WARN, fontsize=8)

    thin_box(ax, 4.0, 2.0, 5.5, 0.7, fc=WHITE, ec=WARN)
    ax.text(6.75, 2.35, "일반 NN: 자유 연장 → 폭주 가능", ha="center", color=WARN, fontsize=8.5)

    thin_box(ax, 4.0, 1.0, 5.5, 0.8, fc=WHITE, ec=ACCENT)
    ax.text(6.75, 1.55, "SAAR: affine 기본 + 제한 residual 보정", ha="center", color=ACCENT, fontsize=8.5)
    ax.text(6.75, 1.15, "Assumption-Aware Extrapolation", ha="center", color=MUTED, fontsize=7.5)

    arrow_h(ax, 3.55, 1.5, 3.95)
    title_left(ax, "SAAR — Support-Aware Affine–Residual (식 없는 경로)")
    save(fig, "pp_core_idea.png")


def fig_pp_architecture():
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.6)
    ax.axis("off")

    thin_box(ax, 3.0, 2.85, 4.0, 0.45, fc=SOFT)
    ax.text(5.0, 3.08, "history · health · rate · time", ha="center", color=INK, fontsize=8.5)

    thin_box(ax, 0.8, 1.5, 3.5, 0.9, fc=WHITE)
    ax.text(2.55, 2.15, "Frozen Affine Path", ha="center", color=INK, fontsize=9, fontweight="bold")
    ax.text(2.55, 1.75, "stable trend", ha="center", color=MUTED, fontsize=7.5)

    thin_box(ax, 5.7, 1.5, 3.5, 0.9, fc=WHITE)
    ax.text(7.45, 2.15, "Dual-Scale Residual", ha="center", color=ACCENT, fontsize=9, fontweight="bold")
    ax.text(7.45, 1.75, "B_L=2, B_H=6", ha="center", color=MUTED, fontsize=7.5)

    arrow_v(ax, 2.55, 2.4, 2.45)
    arrow_v(ax, 7.45, 2.4, 2.45)
    thin_box(ax, 2.5, 0.55, 5.0, 0.55, fc=SOFT)
    ax.text(5.0, 0.82, "Support-Distance Gate + bounded residual", ha="center", color=INK, fontsize=8.5)
    arrow_v(ax, 5.0, 1.1, 1.5)
    ax.text(5.0, 0.25, "RUL 예측", ha="center", color=ACCENT, fontsize=9, fontweight="bold")

    title_left(ax, "SAAR 구조: Frozen Affine · Dual-Scale Residual · Support Gate")
    save(fig, "pp_architecture.png")


def fig_pp_equation_panel():
    fig, ax = plt.subplots(figsize=(10, 3.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.0)
    ax.axis("off")

    thin_box(ax, 0.4, 2.0, 9.2, 0.7, fc=SOFT)
    ax.text(5.0, 2.45, r"$\hat{y} = m \cdot \mathrm{softplus}(\ell(z) + c_\theta(z))$",
            ha="center", color=INK, fontsize=13, fontweight="bold")
    ax.text(5.0, 2.05,
            r"$c_\theta = w\,B_L\tanh(r) + (1-w)\,B_H\tanh(r/B_H)$  ·  $B_L{=}2,\; B_H{=}6$",
            ha="center", color=MUTED, fontsize=8.5)

    terms = [
        (0.4, r"$\ell(z)$", "동결 affine\n기본 추세"),
        (2.8, r"$c_\theta(z)$", "dual-scale\nresidual"),
        (5.2, r"$B_L,B_H$", "거리별\n포화 상한"),
        (7.6, r"$w(d)$", "support\n거리 gate"),
    ]
    for x, t, b in terms:
        thin_box(ax, x, 0.35, 2.0, 1.4, fc=WHITE)
        ax.text(x + 1.0, 1.45, t, ha="center", color=ACCENT, fontsize=10, fontweight="bold")
        ax.text(x + 1.0, 0.85, b, ha="center", color=MUTED, fontsize=7.5, linespacing=1.3)

    title_left(ax, "SAAR 핵심식 — softplus affine + dual-scale residual")
    save(fig, "pp_equation_panel.png")


def fig_support_adaptive():
    fig, ax = plt.subplots(figsize=(8, 3.2))
    d = np.linspace(0, 4, 200)
    w = 1 - (1 / (1 + np.exp(-(d - 1.2) / 0.35))) * (1 - 0.4)
    bound = w * 2 + (1 - w) * 6
    ax.plot(d, bound, color=ACCENT, lw=1.2)
    ax.axvline(1.2, color=MUTED, ls="--", lw=0.7)
    ax.text(1.3, 5.8, "τ", color=MUTED, fontsize=8)
    ax.text(0.3, 2.2, "$B_L$=2", color=MUTED, fontsize=8)
    ax.text(2.8, 5.2, "$B_H$=6", color=MUTED, fontsize=8)
    ax.set_xlabel("support 거리 (정규화)", color=MUTED, fontsize=9)
    ax.set_ylabel("residual envelope", color=MUTED, fontsize=9)
    ax.set_ylim(0, 6.5)
    ax.set_xlim(0, 4)
    style_axes(ax)
    title_left(ax, "Support-adaptive dual-scale: 가까우면 세밀, 멀면 유한 포화")
    save(fig, "support_adaptive.png")


def fig_protocol():
    fig, ax = plt.subplots(figsize=(10, 2.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.2)
    ax.axis("off")

    steps = ["① 나누기", "② 고르기", "③ 학습", "④ 보고"]
    bodies = [
        "개체 분리\nhull-out만",
        "val만으로\n설정 결정",
        "seed 42–46\n5회 재학습",
        "R²·안정성\n경계 위반 0",
    ]
    for i, (t, b) in enumerate(zip(steps, bodies)):
        x = 0.3 + i * 2.4
        thin_box(ax, x, 0.5, 2.0, 1.3, fc=WHITE if i % 2 else SOFT)
        ax.text(x + 1.0, 1.55, t, ha="center", color=INK, fontsize=9, fontweight="bold")
        ax.text(x + 1.0, 0.95, b, ha="center", color=MUTED, fontsize=7.5, linespacing=1.3)
        if i < 3:
            arrow_h(ax, x + 2.0, 1.15, x + 2.25)
    ax.text(5.0, 0.15, "test 라벨은 모델 선택에 사용하지 않음", ha="center", color=WARN, fontsize=8)
    title_left(ax, "검증 흐름 — Assumption-Aware Extrapolation protocol")
    save(fig, "protocol_flow.png")


def _grouped_bars(ax, models: dict, *, highlight: str | None = None, show_values: bool = True):
    names = list(models.keys())
    x = np.arange(len(DATASETS))
    n = len(names)
    width = 0.75 / n
    colors = [MUTED] * n
    if highlight and highlight in names:
        colors[names.index(highlight)] = ACCENT
    for i, (name, vals) in enumerate(models.items()):
        offset = (i - (n - 1) / 2) * width
        bars = ax.bar(x + offset, vals, width, label=name, color=colors[i], edgecolor=WHITE, linewidth=0.3)
        if show_values:
            for b, v in zip(bars, vals):
                ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.2f}",
                        ha="center", va="bottom", fontsize=6.5, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(DATASETS, fontsize=9)
    ax.set_ylabel("설명력 R²", color=MUTED, fontsize=9)
    ax.set_ylim(0, 1.12)
    ax.axhline(0, color=RULE, lw=0.5)
    style_axes(ax)


def fig_main_results():
    fig, ax = plt.subplots(figsize=(9, 3.6))
    _grouped_bars(ax, DEV_MODELS, highlight="SAAR")
    ax.legend(frameon=False, fontsize=7, ncol=3, loc="upper right")
    title_left(ax, "Ablation — SAAR가 평균과 MICH 최저를 함께 개선")
    save(fig, "main_ablation_bars.png")


def fig_ablation_numbers():
    fig, ax = plt.subplots(figsize=(10, 4.0))
    arms = {
        "Direct NN": [-1.35, 0.63, 0.68],
        "Affine only": [0.28, 0.66, -3.34],
        "Trainable bound": [0.90, 0.86, 0.32],
        "Frozen unbound": [0.72, 0.79, 0.76],
        "고정 bound": FIXED,
        "SAAR": SAAR,
    }
    x = np.arange(len(DATASETS))
    n = len(arms)
    width = 0.8 / n
    for i, (name, vals) in enumerate(arms.items()):
        offset = (i - (n - 1) / 2) * width
        col = ACCENT if name == "SAAR" else MUTED
        plot_vals = [max(v, -0.5) for v in vals]
        bars = ax.bar(x + offset, plot_vals, width, label=name, color=col, edgecolor=WHITE, linewidth=0.3, alpha=0.95 if name == "SAAR" else 0.7)
        for b, v in zip(bars, vals):
            ypos = max(v, -0.45) + 0.03 if v >= 0 else max(v, -0.45) - 0.08
            ax.text(b.get_x() + b.get_width() / 2, ypos, f"{v:.2f}", ha="center", fontsize=5.5, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(DATASETS, fontsize=9)
    ax.set_ylabel("R²", color=MUTED, fontsize=9)
    ax.set_ylim(-0.55, 1.12)
    ax.axhline(0, color=RULE, lw=0.5)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=6, ncol=3, loc="upper right")
    title_left(ax, "Ablation 수치 — matched arms (SAAR 강조)")
    save(fig, "ablation_numbers.png")


def fig_competitor():
    show = np.clip(COMPETITOR_MAT, -0.5, 1.0)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "minimal", [(1, 1, 1), (0.94, 0.94, 0.94), (0.06, 0.36, 0.36)], N=256
    )
    im = ax.imshow(show, aspect="auto", cmap=cmap, vmin=-0.3, vmax=1.0)
    ax.set_xticks(np.arange(len(COMPETITOR_ALGOS)))
    ax.set_yticks(np.arange(len(COMPETITOR_DATASETS)))
    ax.set_xticklabels(COMPETITOR_ALGOS, fontsize=8)
    ax.set_yticklabels(COMPETITOR_DATASETS, fontsize=8)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i in range(len(COMPETITOR_DATASETS)):
        for j in range(len(COMPETITOR_ALGOS)):
            v = COMPETITOR_MAT[i, j]
            txt = f"{v:.2f}" if v > -1.5 else f"{v:.1f}"
            fw = "bold" if j == 0 else "normal"
            tc = INK if abs(show[i, j]) < 0.75 else WHITE
            ax.text(j, i, txt, ha="center", va="center", color=tc, fontsize=7, fontweight=fw)
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.ax.tick_params(labelsize=7, colors=MUTED)
    cbar.outline.set_linewidth(0.4)
    title_left(ax, "8 데이터셋 × 알고리즘 R² (TabPFN 포함)", size=9, pad=14)
    fig.text(0.08, 0.01, "TabPFN: 예산·split 조건은 데이터셋별 상이", color=MUTED, fontsize=6.5)
    save(fig, "competitor_bars.png")

    fig2, ax2 = plt.subplots(figsize=(10, 3.8))
    key = ["SAAR", "V-REx", "GroupDRO", "LinRBF", "Engression", "TabPFN"]
    key_idx = [COMPETITOR_ALGOS.index(k) for k in key]
    x = np.arange(len(COMPETITOR_DATASETS))
    w = 0.12
    for ki, (name, j) in enumerate(zip(key, key_idx)):
        vals = COMPETITOR_MAT[:, j]
        plot_vals = np.clip(vals, -0.25, None)
        col = ACCENT if name == "SAAR" else MUTED
        ax2.bar(x + (ki - 2.5) * w, plot_vals, w, label=name, color=col, edgecolor=WHITE, linewidth=0.3, alpha=0.95 if name == "SAAR" else 0.65)
    ax2.axhline(0, color=RULE, lw=0.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(COMPETITOR_DATASETS, fontsize=8)
    ax2.set_ylabel("R²", color=MUTED, fontsize=9)
    ax2.set_ylim(-0.3, 1.1)
    style_axes(ax2)
    ax2.legend(frameon=False, ncol=6, fontsize=6.5, loc="upper center")
    title_left(ax2, "주요 알고리즘 막대 비교")
    save(fig2, "competitor_algo_bars.png")

    fig3, ax3 = plt.subplots(figsize=(9, 3.6))
    pp = COMPETITOR_MAT[:, 0]
    pfn = COMPETITOR_MAT[:, -1]
    x = np.arange(len(COMPETITOR_DATASETS))
    bw = 0.32
    ax3.bar(x - bw / 2, pp, bw, color=ACCENT, label="SAAR", edgecolor=WHITE, linewidth=0.3)
    ax3.bar(x + bw / 2, np.clip(pfn, -1.0, None), bw, color=MUTED, label="TabPFN", edgecolor=WHITE, linewidth=0.3)
    for i, (a, b) in enumerate(zip(pp, pfn)):
        ax3.text(i - bw / 2, a + 0.02, f"{a:.2f}", ha="center", fontsize=6.5, color=INK)
        ypos = max(b, -1.0) + 0.02 if b > -1.0 else -0.92
        ax3.text(i + bw / 2, ypos, f"{b:.2f}", ha="center", fontsize=6.5, color=MUTED)
    ax3.axhline(0, color=RULE, lw=0.5)
    ax3.set_xticks(x)
    ax3.set_xticklabels(COMPETITOR_DATASETS, fontsize=8)
    ax3.set_ylabel("R²", color=MUTED, fontsize=9)
    ax3.set_ylim(-1.1, 1.15)
    style_axes(ax3)
    ax3.legend(frameon=False, fontsize=8, loc="upper right")
    title_left(ax3, "SAAR vs TabPFN")
    save(fig3, "pp_vs_tabpfn.png")


def fig_experiment_map():
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    points = [
        (0.9, 0.85, "HUST"), (0.75, 0.78, "Virkler"), (0.55, 0.55, "NASA"),
        (0.8, 0.7, "Sunwoda"), (0.7, 0.65, "RWTH"), (0.5, 0.45, "MATR2019"),
        (0.78, 0.72, "MATR b2"), (0.88, 0.82, "N-CMAPSS"),
        (0.2, 0.15, "MICH*"), (0.18, 0.2, "XJTU"), (0.15, 0.12, "FEMTO"), (0.12, 0.08, "Milling"),
    ]
    ax.axhline(0.5, color=RULE, ls=":", lw=0.6)
    ax.axvline(0.5, color=RULE, ls=":", lw=0.6)
    for x, y, name in points:
        col = ACCENT if y >= 0.5 and x >= 0.5 else (WARN if y < 0.5 else MUTED)
        ax.scatter([x], [y], s=45, color=col, edgecolors=RULE, linewidths=0.5, zorder=3)
        ax.text(x + 0.02, y + 0.025, name, color=col, fontsize=7)
    ax.text(0.72, 0.92, "성공", color=ACCENT, fontsize=8)
    ax.text(0.08, 0.42, "실패/기권", color=WARN, fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("적용 조건 적합도", color=MUTED, fontsize=9)
    ax.set_ylabel("외삽 성능", color=MUTED, fontsize=9)
    style_axes(ax, grid=False)
    title_left(ax, "실험 지형: 성공 · 경계 · 실패 (*기본 SAAR 기준)")
    save(fig, "experiment_map.png")


def fig_bootstrap():
    fig, ax = plt.subplots(figsize=(8, 3.0))
    y = np.arange(len(BOOT_NAMES))
    ax.axvline(0, color=WARN, lw=0.7, ls="--")
    for i, (m, lo, hi) in enumerate(zip(BOOT_MEANS, BOOT_LO, BOOT_HI)):
        ax.plot([lo, hi], [i, i], color=ACCENT, lw=1.8, solid_capstyle="butt")
        ax.scatter([m], [i], color=ACCENT2, s=28, zorder=3, edgecolors=WHITE, linewidths=0.4)
        ax.text(hi + 1.5, i, f"{m:.1f}  [{lo:.1f}, {hi:.1f}]", va="center", color=MUTED, fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels(BOOT_NAMES, fontsize=9)
    ax.set_xlabel("unit RMSE 변화 (보정 후 − 전) · 95% bootstrap CI", color=MUTED, fontsize=8)
    style_axes(ax, grid=False)
    ax.invert_yaxis()
    title_left(ax, "Unit-level paired bootstrap — CI < 0 이면 일관 개선")
    save(fig, "bootstrap_ci.png")


def fig_mich_units():
    fig, ax = plt.subplots(figsize=(8, 3.2))
    colors = [ACCENT if v >= 0.6 else MUTED for v in MICH_R2]
    bars = ax.bar([str(u) for u in MICH_UNITS], MICH_R2, color=colors, edgecolor=WHITE, linewidth=0.3)
    ax.axhline(0.751, color=ACCENT2, ls="--", lw=0.7, label="pooled 0.751")
    for b, v in zip(bars, MICH_R2):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}", ha="center", fontsize=7, color=INK)
    ax.set_ylabel("within-unit R²", color=MUTED, fontsize=9)
    ax.set_xlabel("MICH test unit", color=MUTED, fontsize=9)
    ax.set_ylim(0, 1.1)
    ax.legend(frameon=False, fontsize=8)
    style_axes(ax)
    title_left(ax, "MICH: 8/8 unit 양의 R² (unit 31 = 0.496)")
    save(fig, "mich_units.png")


def fig_pp_pae_flow():
    fig, ax = plt.subplots(figsize=(10, 2.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.6)
    ax.axis("off")

    stages = [
        (0.3, "외삽 문제", "후보식·관측\n계약만 본다"),
        (3.5, "식 있음 → PAE", "식=뼈대\nNN=제한 보정"),
        (6.8, "식 없음 → SAAR", "equation-free\nsafeguard"),
    ]
    for x, t, b in stages:
        thin_box(ax, x, 0.7, 2.8, 1.4, fc=SOFT if "SAAR" in t else WHITE)
        ax.text(x + 1.4, 1.75, t, ha="center", color=ACCENT if "SAAR" in t else INK, fontsize=8.5, fontweight="bold")
        ax.text(x + 1.4, 1.15, b, ha="center", color=MUTED, fontsize=7.5, linespacing=1.3)
    arrow_h(ax, 3.1, 1.4, 3.45)
    arrow_h(ax, 6.4, 1.4, 6.75)
    ax.text(5.0, 0.25, "Assumption-Aware Extrapolation · PAE / SAAR dual path", ha="center", color=MUTED, fontsize=8)
    title_left(ax, "문제 계약 → 후보식 유무로 분기")
    save(fig, "pp_pae_flow.png")


def fig_pae_equation_nn():
    fig, ax = plt.subplots(figsize=(10, 2.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.8)
    ax.axis("off")

    nodes = [
        (0.2, "① 후보식"), (2.0, "② 검증"), (3.8, "③ 조립"),
        (5.8, "④ 판정"), (7.6, "⑤ 출력"),
    ]
    for x, t in nodes:
        thin_box(ax, x, 1.0, 1.5, 0.9, fc=WHITE)
        ax.text(x + 0.75, 1.45, t, ha="center", color=INK, fontsize=8, fontweight="bold")
    for x in [1.7, 3.5, 5.5, 7.3]:
        arrow_h(ax, x, 1.45, x + 0.25)

    thin_box(ax, 0.4, 0.2, 4.2, 0.65, fc=SOFT)
    ax.text(2.5, 0.52, "식 (뼈대): 방향·경계·관계", ha="center", color=INK, fontsize=8)
    thin_box(ax, 5.4, 0.2, 4.2, 0.65, fc=SOFT)
    ax.text(7.5, 0.52, "NN (부족분): 제한 보정", ha="center", color=ACCENT, fontsize=8)
    title_left(ax, "PAE = 허용된 식 + 제한된 NN 보정")
    save(fig, "pae_equation_nn.png")


def fig_pp_vs_pae_split():
    fig, ax = plt.subplots(figsize=(10, 3.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.0)
    ax.axis("off")

    thin_box(ax, 0.3, 0.4, 4.5, 2.3, fc=WHITE)
    ax.text(2.55, 2.45, "SAAR / PP", ha="center", color=ACCENT, fontsize=10, fontweight="bold")
    ax.text(2.55, 2.1, "equation-free safeguard", ha="center", color=MUTED, fontsize=8)
    for i, t in enumerate([
        "affine · dual-scale · gate",
        "약한 bundle을 계약상 기계적 활성",
        "식 없이 외삽 형태 통제",
    ]):
        ax.text(0.55, 1.65 - i * 0.4, "· " + t, color=INK, fontsize=8)

    thin_box(ax, 5.2, 0.4, 4.5, 2.3, fc=WHITE)
    ax.text(7.45, 2.45, "PAE", ha="center", color=ACCENT2, fontsize=10, fontweight="bold")
    ax.text(7.45, 2.1, "equation prior + NN", ha="center", color=MUTED, fontsize=8)
    for i, t in enumerate([
        "식=뼈대, NN=부족분",
        "이득 없으면 off · SAAR fallback",
        "어떤 식을 어떻게 넣을까",
    ]):
        ax.text(5.45, 1.65 - i * 0.4, "· " + t, color=INK, fontsize=8)

    title_left(ax, "Dual path — PAE(식) vs SAAR(식 없음)")
    save(fig, "pp_vs_pae_split.png")


def fig_dataset_split():
    fig, ax = plt.subplots(figsize=(10, 2.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.4)
    ax.axis("off")

    steps = [
        ("① 계약", "경계·unit·시간축"),
        ("② 분리", "unit disjoint"),
        ("③ support", "train 범위"),
        ("④ hull-out", "밖만 평가"),
        ("⑤ 보고", "val→test 1회"),
    ]
    for i, (t, b) in enumerate(steps):
        x = 0.2 + i * 1.9
        thin_box(ax, x, 0.55, 1.6, 1.2, fc=SOFT if i % 2 else WHITE)
        ax.text(x + 0.8, 1.45, t, ha="center", color=INK, fontsize=8, fontweight="bold")
        ax.text(x + 0.8, 0.95, b, ha="center", color=MUTED, fontsize=7)
        if i < 4:
            arrow_h(ax, x + 1.6, 1.15, x + 1.75)
    ax.text(5.0, 0.15, "정규화 train-only · seed 42–46 · raw pooled R²", ha="center", color=MUTED, fontsize=7.5)
    title_left(ax, "공통 스플릿: 개체 분리 + support 밖(끝단)만 평가")
    save(fig, "dataset_split.png")


def fig_fail_cases():
    fig, ax = plt.subplots(figsize=(9, 2.2))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 2.2)
    ax.axis("off")

    fails = [
        ("MICH (기본)", "−1.52", "dual-scale 회복"),
        ("XJTU", "−1.23", "이동 방향 반대"),
        ("FEMTO", "−1.38", "끝점 1개"),
        ("Milling", "−4.83", "val unit 부족"),
    ]
    for i, (h, v, b) in enumerate(fails):
        x = 0.2 + i * 2.2
        thin_box(ax, x, 0.35, 2.0, 1.5, fc=WHITE)
        ax.text(x + 1.0, 1.55, h, ha="center", color=INK, fontsize=8, fontweight="bold")
        ax.text(x + 1.0, 1.05, v, ha="center", color=WARN, fontsize=14, fontweight="bold")
        ax.text(x + 1.0, 0.65, b, ha="center", color=MUTED, fontsize=7)
    title_left(ax, "Fail cases — 거절·회복이 맞는 경우")
    save(fig, "fail_cases.png")


def fig_unified_model_table():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    headers = ["모형", "Sun", "RWTH", "MICH", "평균", "최저"]
    rows = []
    for name, vals in DEV_MODELS.items():
        rows.append([name, *[f"{v:.3f}" for v in vals], f"{np.mean(vals):.3f}", f"{min(vals):.3f}"])
    y0 = 2.6
    rh = 0.38
    for i, h in enumerate(headers):
        ax.text(0.3 + i * 1.55, y0, h, color=MUTED, fontsize=8, fontweight="bold")
    ax.plot([0.2, 9.5], [y0 - 0.15, y0 - 0.15], color=RULE, lw=0.6)
    for ri, row in enumerate(rows):
        y = y0 - (ri + 1) * rh
        hl = row[0] == "SAAR"
        if hl:
            ax.add_patch(Rectangle((0.2, y - rh / 2 + 0.05), 9.3, rh - 0.08, facecolor=SOFT, edgecolor=RULE, linewidth=0.5))
        for i, val in enumerate(row):
            col = ACCENT if hl and i > 0 else INK
            fw = "bold" if hl else "normal"
            ax.text(0.3 + i * 1.55, y, val, color=col, fontsize=8, fontweight=fw)
    title_left(ax, "통합 모델 비교 — 개발 3데이터")
    save(fig, "unified_model_table.png")


def fig_unified_tradeoff():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for name, vals in DEV_MODELS.items():
        mean_v = np.mean(vals)
        min_v = min(vals)
        hl = name == "SAAR"
        ax.scatter(mean_v, min_v, s=60 if hl else 35, color=ACCENT if hl else MUTED,
                   edgecolors=WHITE, linewidths=0.5, zorder=3 if hl else 2)
        ax.annotate(name, (mean_v, min_v), textcoords="offset points", xytext=(4, 4),
                    fontsize=7, color=ACCENT if hl else MUTED)
    ax.set_xlabel("평균 R²", color=MUTED, fontsize=9)
    ax.set_ylabel("최저 R² (MICH)", color=MUTED, fontsize=9)
    ax.set_xlim(0.72, 0.88)
    ax.set_ylim(0.42, 0.78)
    style_axes(ax)
    title_left(ax, "모델 trade-off: 평균 vs 최저 (SAAR = 균형)")
    save(fig, "unified_tradeoff.png")


def fig_research_route():
    fig, ax = plt.subplots(figsize=(10, 4.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    thin_box(ax, 0.3, 3.2, 9.4, 0.55, fc=SOFT)
    ax.text(5.0, 3.48, "밖을 지탱하는 것은 데이터가 아니라 가정", ha="center", color=INK, fontsize=8.5)

    thin_box(ax, 0.3, 2.45, 9.4, 0.45, fc=WHITE)
    ax.text(5.0, 2.68, "관측 · unit 분리 · hull-out · val-only 선택", ha="center", color=MUTED, fontsize=8)

    ax.text(5.0, 2.15, "후보식이 정당화되는가?", ha="center", color=INK, fontsize=9, fontweight="bold")
    arrow_v(ax, 5.0, 2.0, 1.85)

    thin_box(ax, 0.5, 0.9, 4.0, 0.85, fc=WHITE)
    ax.text(2.5, 1.55, "YES → PAE", ha="center", color=ACCENT2, fontsize=9, fontweight="bold")
    ax.text(2.5, 1.15, "식 + 제한 NN · 다음 논문", ha="center", color=MUTED, fontsize=7.5)

    thin_box(ax, 5.5, 0.9, 4.0, 0.85, fc=SOFT)
    ax.text(7.5, 1.55, "NO → SAAR (현재)", ha="center", color=ACCENT, fontsize=9, fontweight="bold")
    ax.text(7.5, 1.15, "equation-free safeguard", ha="center", color=MUTED, fontsize=7.5)

    ax.annotate("", xy=(2.5, 1.85), xytext=(4.2, 2.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))
    ax.annotate("", xy=(7.5, 1.85), xytext=(5.8, 2.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))
    ax.text(3.2, 1.95, "YES", color=MUTED, fontsize=7)
    ax.text(6.5, 1.95, "NO", color=MUTED, fontsize=7)

    ax.text(5.0, 0.35, "Assurance: 믿기 / 보류 / 거절 → 박사논문 통합 프레임", ha="center", color=MUTED, fontsize=7.5)
    title_left(ax, "가정 인식형 외삽 — Motivation → PAE / SAAR → Assurance")
    save(fig, "research_route.png")


def fig_summary_executive():
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.4)
    ax.axis("off")

    ax.text(5.0, 3.05, "SAAR — equation-free Assumption-Aware Extrapolation",
            ha="center", color=INK, fontsize=9, fontweight="bold")
    ax.text(5.0, 2.7, "Frozen Affine + Dual-Scale Residual · PAE는 이번 주결과 아님",
            ha="center", color=MUTED, fontsize=8)

    for i, (name, val) in enumerate(zip(DATASETS, SAAR)):
        x = 0.5 + i * 3.1
        ax.text(x + 1.2, 2.15, name, ha="center", color=MUTED, fontsize=8)
        ax.text(x + 1.2, 1.65, f"{val:.3f}", ha="center", color=ACCENT, fontsize=22, fontweight="bold")
        ax.text(x + 1.2, 1.25, "R²", ha="center", color=MUTED, fontsize=7)

    ax.plot([0.4, 9.6], [0.95, 0.95], color=RULE, lw=0.5)
    bits = [
        (0.4, r"$\hat y = m\,\mathrm{softplus}(\ell+c_\theta)$"),
        (3.5, "연속 열화 · 경계 prior · 만능 SOTA 아님"),
        (7.0, "Zn·베어링 한계 · Q1–Q2 본선"),
    ]
    for x, t in bits:
        ax.text(x, 0.55, t, color=INK if x < 1 else MUTED, fontsize=7.5)

    title_left(ax, "Executive summary — SAAR 현재 결론")
    save(fig, "summary_executive.png")


# ── New explanatory figures ───────────────────────────────────────────────────

def fig_nn_vs_saar_curves():
    fig, ax = plt.subplots(figsize=(9, 3.6))
    xs_in = np.linspace(0, 4, 80)
    xs_out = np.linspace(4, 8, 80)
    y_base = 0.85 - 0.06 * xs_in
    y_end = 0.85 - 0.06 * 4

    ax.plot(xs_in, y_base, color=ACCENT, lw=1.2, label="true (slow fade)")
    ax.plot(xs_out, y_end - 0.035 * (xs_out - 4), color=ACCENT, lw=1.2, ls="--")

    nn_out = y_end + 0.04 * (xs_out - 4) + 0.012 * (xs_out - 4) ** 2
    ax.plot(xs_out, nn_out, color=WARN, lw=1.2, label="unconstrained NN")

    saar_out = y_end - 0.03 * (xs_out - 4) + 0.008 * np.tanh((xs_out - 4) / 1.5)
    ax.plot(xs_out, saar_out, color=ACCENT2, lw=1.2, ls="-.", label="SAAR")

    ax.axvline(4, color=MUTED, lw=0.7, ls=":")
    ax.text(4.05, 0.98, "support 경계", color=MUTED, fontsize=7.5)
    ax.axvspan(0, 4, color=SOFT, alpha=0.4, zorder=0)

    ax.set_xlabel("support distance / time", color=MUTED, fontsize=9)
    ax.set_ylabel("prediction", color=MUTED, fontsize=9)
    ax.set_xlim(-0.2, 8.2)
    ax.set_ylim(0.2, 1.05)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    title_left(ax, "NN vs SAAR: support 밖에서 affine 유지 + 작은 residual")
    save(fig, "nn_vs_saar_curves.png")


def fig_ablation_slope():
    fig, ax = plt.subplots(figsize=(8, 3.6))
    x = np.arange(len(DATASETS))
    for i, ds in enumerate(DATASETS):
        ax.plot([i - 0.12, i + 0.12], [FIXED[i], SAAR[i]], color=RULE, lw=1.0, zorder=1)
        ax.scatter(i - 0.12, FIXED[i], s=40, color=MUTED, zorder=2, edgecolors=WHITE, linewidths=0.4)
        ax.scatter(i + 0.12, SAAR[i], s=50, color=ACCENT, zorder=3, edgecolors=WHITE, linewidths=0.4)
        delta = SAAR[i] - FIXED[i]
        sign = "+" if delta >= 0 else ""
        ax.text(i, max(FIXED[i], SAAR[i]) + 0.04, f"{sign}{delta:.2f}", ha="center", fontsize=7, color=ACCENT if delta > 0 else WARN)
    ax.set_xticks(x)
    ax.set_xticklabels(DATASETS, fontsize=9)
    ax.set_ylabel("R²", color=MUTED, fontsize=9)
    ax.set_ylim(0.35, 1.05)
    style_axes(ax)
    ax.text(0.02, 0.98, "○ 고정 bound", transform=ax.transAxes, color=MUTED, fontsize=7, va="top")
    ax.text(0.02, 0.90, "● SAAR", transform=ax.transAxes, color=ACCENT, fontsize=7, va="top")
    title_left(ax, "Ablation slope: 고정 bound → SAAR 이동")
    save(fig, "ablation_slope.png")


def fig_model_tradeoff():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for name, vals in DEV_MODELS.items():
        mean_v = np.mean(vals)
        min_v = min(vals)
        hl = name == "SAAR"
        ax.scatter(mean_v, min_v, s=70 if hl else 35, color=ACCENT if hl else MUTED,
                   edgecolors=WHITE, linewidths=0.5, zorder=3 if hl else 2)
        ax.annotate(name, (mean_v, min_v), textcoords="offset points", xytext=(5, 3),
                    fontsize=7.5, color=ACCENT if hl else MUTED, fontweight="bold" if hl else "normal")
    ax.set_xlabel("mean R²", color=MUTED, fontsize=9)
    ax.set_ylabel("min R²", color=MUTED, fontsize=9)
    ax.set_xlim(0.72, 0.88)
    ax.set_ylim(0.42, 0.78)
    style_axes(ax)
    title_left(ax, "개발 5모형 trade-off — SAAR 강조")
    save(fig, "model_tradeoff.png")


def fig_roadmap_line():
    fig, ax = plt.subplots(figsize=(10, 1.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.8)
    ax.axis("off")

    ax.plot([0.8, 9.2], [0.9, 0.9], color=RULE, lw=1.0)
    milestones = [
        (1.2, "NOW", "SAAR / PP", ACCENT),
        (4.5, "NEXT", "PAE", ACCENT2),
        (8.0, "PhD", "Assurance", MUTED),
    ]
    for x, tag, label, col in milestones:
        ax.scatter([x], [0.9], s=50, color=col, zorder=2, edgecolors=WHITE, linewidths=0.5)
        ax.text(x, 1.25, tag, ha="center", color=MUTED, fontsize=7)
        ax.text(x, 0.45, label, ha="center", color=col, fontsize=9, fontweight="bold")
    title_left(ax, "로드맵 — SAAR → PAE → Assurance")
    save(fig, "roadmap_line.png")


def fig_scope_inout():
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    thin_box(ax, 0.4, 0.4, 3.8, 2.4, fc=WHITE)
    ax.text(2.3, 2.55, "In scope", ha="center", color=OK, fontsize=9, fontweight="bold")
    for i, t in enumerate([
        "안 본 unit RUL 외삽",
        "Frozen affine + bounded residual",
        "val-only 승인 · gate",
        "실패·거절 포함 보고",
    ]):
        ax.text(0.65, 2.1 - i * 0.45, "· " + t, color=INK, fontsize=8)

    thin_box(ax, 4.8, 0.4, 3.8, 2.4, fc=WHITE)
    ax.text(6.7, 2.55, "Out of scope", ha="center", color=WARN, fontsize=9, fontweight="bold")
    for i, t in enumerate([
        "prior-free / 만능 SOTA",
        "test 라벨로 모델 선택",
        "모든 도메인 1등 주장",
        "PAE 결과 (이번 deck)",
    ]):
        ax.text(5.05, 2.1 - i * 0.45, "· " + t, color=MUTED, fontsize=8)

    title_left(ax, "Scope — 포함 / 제외")
    save(fig, "scope_inout.png")


def fig_results_panel():
    fig, ax = plt.subplots(figsize=(9, 3.8))
    _grouped_bars(ax, DEV_MODELS, highlight="SAAR", show_values=True)
    ax.legend(frameon=False, fontsize=6.5, ncol=3, loc="upper right")
    ax.text(0.98, 0.08, "SAAR mean R² = 0.842", transform=ax.transAxes, ha="right",
            color=ACCENT, fontsize=9, fontweight="bold")
    title_left(ax, "주요 결과 — 3데이터셋 grouped bars")
    save(fig, "results_panel.png")


def fig_limits_strip():
    fig, ax = plt.subplots(figsize=(10, 1.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.6)
    ax.axis("off")

    thin_box(ax, 0.3, 0.35, 4.5, 0.9, fc=SOFT)
    ax.text(0.5, 1.05, "Claim", color=OK, fontsize=8, fontweight="bold")
    ax.text(2.55, 0.8, "가정 인식 외삽 · SAAR 구조 · val 승인 · 실험 지도", ha="center", color=INK, fontsize=7.5)

    thin_box(ax, 5.2, 0.35, 4.5, 0.9, fc=WHITE)
    ax.text(5.4, 1.05, "Do NOT claim", color=WARN, fontsize=8, fontweight="bold")
    ax.text(7.45, 0.8, "최초·만능 · 모든 도메인 1등 · prior-free", ha="center", color=MUTED, fontsize=7.5)

    title_left(ax, "주장 경계")
    save(fig, "limits_strip.png")


def fig_status_compact():
    fig, ax = plt.subplots(figsize=(10, 2.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.4)
    ax.axis("off")

    thin_box(ax, 0.3, 0.4, 4.2, 1.7, fc=SOFT)
    ax.text(2.4, 1.75, "KPI (SAAR R²)", ha="center", color=INK, fontsize=8, fontweight="bold")
    for i, (ds, v) in enumerate(zip(DATASETS, SAAR)):
        ax.text(0.6, 1.35 - i * 0.35, f"{ds}", color=MUTED, fontsize=8)
        ax.text(3.8, 1.35 - i * 0.35, f"{v:.3f}", color=ACCENT, fontsize=9, fontweight="bold", ha="right")

    thin_box(ax, 5.0, 0.4, 4.7, 1.7, fc=WHITE)
    ax.text(7.35, 1.75, "한계 (3줄)", ha="center", color=INK, fontsize=8, fontweight="bold")
    limits = [
        "Zn untouched: BQ 단독 실패 → refit 개발점수",
        "XJTU·FEMTO·Milling: 통합 우월 주장 전",
        "PAE 라우팅 실험 없음 · Q1–Q2 본선",
    ]
    for i, t in enumerate(limits):
        ax.text(5.25, 1.35 - i * 0.35, "· " + t, color=MUTED, fontsize=7.5)

    title_left(ax, "Status — KPI + 한계 (compact)")
    save(fig, "status_compact.png")


def main():
    # Core deck figures
    fig_motivation()
    fig_prior_ladder()
    fig_pp_core_idea()
    fig_pp_architecture()
    fig_pp_equation_panel()
    fig_support_adaptive()
    fig_protocol()
    fig_main_results()
    fig_ablation_numbers()
    fig_competitor()
    fig_experiment_map()
    fig_bootstrap()
    fig_mich_units()
    fig_pp_pae_flow()
    fig_pae_equation_nn()
    fig_pp_vs_pae_split()
    fig_dataset_split()
    fig_fail_cases()
    fig_unified_model_table()
    fig_unified_tradeoff()
    fig_research_route()
    fig_summary_executive()
    # New explanatory figures
    fig_nn_vs_saar_curves()
    fig_ablation_slope()
    fig_model_tradeoff()
    fig_roadmap_line()
    fig_scope_inout()
    fig_results_panel()
    fig_limits_strip()
    fig_status_compact()

    n = len(list(OUT.glob("*.png")))
    print("done", OUT, f"({n} PNG files)")


if __name__ == "__main__":
    main()
