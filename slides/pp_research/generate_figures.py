#!/usr/bin/env python3
"""Generate research figures for Assumption-Aware Extrapolation (SAAR / PP deck)."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUT = Path("/Users/baghyeongbae/Desktop/연구/ppt/pp/_build/figs")
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update(
    {
        "font.family": "AppleGothic",
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
        "savefig.dpi": 200,
    }
)

# Design system
INK = "#0B1F33"
NAVY = "#153E75"
CRIMSON = "#9B1B30"
TEAL = "#0F766E"
BLUE = "#1D4ED8"
ORANGE = "#C2410C"
GOLD = "#B45309"
RED = "#B91C1C"
GREEN = "#166534"
GREY = "#64748B"
LINE = "#CBD5E1"
PALE = "#F8FAFC"
WASH = "#EEF6FF"
SOFT_TEAL = "#ECFDF5"
SOFT_ORANGE = "#FFF7ED"

DPI = 200
PAD = 0.12
ROUND = 0.12


def save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=PAD)
    plt.close(fig)
    print("wrote", path)


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for sp in ax.spines.values():
        sp.set_color(LINE)
    ax.tick_params(colors=GREY)


def title_left(ax, text: str, size: int = 13, pad: int = 8):
    ax.set_title(text, color=INK, fontsize=size, pad=pad, loc="left", fontweight="bold")


def soft_card(
    ax,
    x,
    y,
    w,
    h,
    *,
    facecolor="white",
    edgecolor=LINE,
    lw=2.0,
    shadow=True,
    zorder=2,
):
    if shadow:
        ax.add_patch(
            FancyBboxPatch(
                (x + 0.04, y - 0.04),
                w,
                h,
                boxstyle=f"round,pad=0.02,rounding_size={ROUND}",
                facecolor=GREY,
                edgecolor="none",
                alpha=0.12,
                zorder=zorder - 1,
            )
        )
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.02,rounding_size={ROUND}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def header_band(ax, x, y, w, h, text, color, text_color="white", size=12):
    ax.add_patch(Rectangle((x, y + h - 0.38), w, 0.38, facecolor=color, edgecolor="none", zorder=5))
    ax.text(x + w / 2, y + h - 0.19, text, ha="center", va="center", color=text_color, fontsize=size, fontweight="bold", zorder=6)


def arrow_h(ax, x0, y0, x1, color=GREY, lw=2.0):
    ax.annotate("", xy=(x1, y0), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color=color, lw=lw))


def draw_table(ax, headers, rows, col_xs, col_ws, *, y0=3.5, row_h=0.42, header_color=NAVY, highlight_row=None, highlight_color=SOFT_TEAL):
    ax.set_xlim(0, max(col_xs[-1] + col_ws[-1], 10))
    ax.set_ylim(0, y0 + 0.8)
    ax.axis("off")
    for i, h in enumerate(headers):
        ax.text(col_xs[i], y0, h, ha="left", va="center", color=header_color, fontsize=11, fontweight="bold")
    for ri, row in enumerate(rows):
        y = y0 - (ri + 1) * row_h
        bg = highlight_color if ri == highlight_row else (PALE if ri % 2 else "white")
        edge = TEAL if ri == highlight_row else LINE
        lw = 2.2 if ri == highlight_row else 1.0
        ax.add_patch(Rectangle((col_xs[0] - 0.08, y - row_h / 2 + 0.04), col_xs[-1] + col_ws[-1] - col_xs[0] + 0.16, row_h - 0.06, facecolor=bg, edgecolor=edge, linewidth=lw, zorder=0))
        for i, val in enumerate(row):
            bold = ri == highlight_row or i == 0
            col = TEAL if ri == highlight_row and i > 0 else INK
            ax.text(col_xs[i], y, str(val), ha="left", va="center", color=col, fontsize=10.5, fontweight="bold" if bold else "normal")


def card_grid_2x2(ax, items, x0=0.35, y0=0.35, w=5.2, h=1.85, gap_x=0.25, gap_y=0.25):
    for i, (tag, title, body, col) in enumerate(items):
        c, r = i % 2, i // 2
        x = x0 + c * (w + gap_x)
        y = y0 + (1 - r) * (h + gap_y)
        soft_card(ax, x, y, w, h, facecolor="white", edgecolor=col, lw=2.2)
        ax.add_patch(Rectangle((x, y + h - 0.42), w, 0.42, facecolor=col, edgecolor="none", zorder=5))
        ax.text(x + 0.18, y + h - 0.21, tag, ha="left", va="center", color="white", fontsize=12, fontweight="bold", zorder=6)
        ax.text(x + 0.95, y + h - 0.21, title, ha="left", va="center", color="white", fontsize=12, fontweight="bold", zorder=6)
        ax.text(x + 0.22, y + h - 0.7, body, ha="left", va="top", color=INK, fontsize=11, linespacing=1.4, zorder=6)


# ── Existing figures (upgraded) ──────────────────────────────────────────────


def fig_motivation():
    fig, ax = plt.subplots(figsize=(11.2, 4.2))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    ax.plot([0.8, 10.4], [1.4, 1.4], color=NAVY, lw=2.2)
    ax.plot([0.8, 0.8], [1.4, 3.5], color=NAVY, lw=2.2)
    ax.text(0.35, 2.5, "예측", rotation=90, va="center", color=GREY, fontsize=11)
    ax.text(9.7, 1.05, "열화 좌표 / 시간", color=GREY, fontsize=11)

    xs_in = np.linspace(1.0, 5.2, 40)
    y_true = 3.2 - 0.22 * (xs_in - 1) ** 1.15
    ax.plot(xs_in, y_true, color=BLUE, lw=3, label="관측 궤적")
    ax.scatter(xs_in[::5], y_true[::5], color=BLUE, s=28, zorder=3)

    ax.axvline(5.2, color=RED, lw=2, ls="--")
    ax.text(5.3, 3.55, "학습 support 끝", color=RED, fontsize=11, fontweight="bold")

    xs_out = np.linspace(5.2, 10.0, 50)
    futures = [
        (3.2 - 0.22 * (5.2 - 1) ** 1.15 - 0.18 * (xs_out - 5.2), TEAL, "가능한 미래 A"),
        (3.2 - 0.22 * (5.2 - 1) ** 1.15 - 0.05 * (xs_out - 5.2) - 0.03 * (xs_out - 5.2) ** 1.4, ORANGE, "가능한 미래 B"),
        (3.2 - 0.22 * (5.2 - 1) ** 1.15 + 0.12 * (xs_out - 5.2) - 0.04 * (xs_out - 5.2) ** 1.2, CRIMSON, "NN 폭주 경로"),
    ]
    for y, c, lab in futures:
        ax.plot(xs_out, y, color=c, lw=2.4, alpha=0.95)
        ax.text(9.15, y[-1], lab, color=c, fontsize=10, va="center")

    ax.fill_between([0.8, 5.2], 0.6, 3.7, color=WASH, alpha=0.85, zorder=0)
    ax.text(2.4, 0.85, "관측 가능 구간 (여러 함수가 비슷하게 맞음)", color=NAVY, fontsize=11)
    ax.text(6.6, 0.85, "밖 = 가정이 방향을 결정", color=CRIMSON, fontsize=11, fontweight="bold")
    title_left(ax, "모티베이션: support 밖에서는 데이터만으로 함수가 정해지지 않는다")
    save(fig, "motivation_futures.png")


def fig_prior_ladder():
    fig, ax = plt.subplots(figsize=(10.8, 4.6))
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    levels = [
        (0.4, "0", "구조 지식 없음", "일반 예측 + 거절", GREY),
        (3.0, "1", "경계·이력", "SAAR / PP (TODAY)", TEAL),
        (5.6, "2", "방향·부호", "제약 신경망", BLUE),
        (8.2, "3", "수식·물리", "PAE (식+NN)", ORANGE),
    ]
    for x, lv, name, exe, col in levels:
        soft_card(ax, x, 1.2, 2.2, 2.4, facecolor=PALE, edgecolor=col, lw=2.5)
        ax.add_patch(Circle((x + 1.1, 3.05), 0.28, facecolor=col, edgecolor="none"))
        ax.text(x + 1.1, 3.05, lv, ha="center", va="center", color="white", fontsize=14, fontweight="bold")
        ax.text(x + 1.1, 2.35, name, ha="center", va="center", color=INK, fontsize=13, fontweight="bold")
        ax.text(x + 1.1, 1.7, exe, ha="center", va="center", color=GREY, fontsize=11)
        if x < 8:
            arrow_h(ax, x + 2.2, 2.4, x + 2.45)
    soft_card(ax, 2.95, 1.1, 2.3, 2.6, facecolor="none", edgecolor=TEAL, lw=3)
    ax.patches[-1].set_linestyle("--")
    ax.text(0.4, 0.45, "강함 →", color=GREY, fontsize=11)
    ax.text(9.4, 0.45, "← 강한 prior", color=GREY, fontsize=11, ha="right")
    title_left(ax, "Prior ladder — PAE(식) vs SAAR(식 없는 안전장치)", size=12)
    save(fig, "prior_ladder.png")


def fig_pp_core_idea():
    fig, ax = plt.subplots(figsize=(11.4, 5.0))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    soft_card(ax, 0.35, 1.55, 3.6, 2.9, facecolor=WASH, edgecolor=TEAL, lw=2.2)
    ax.text(2.15, 4.15, "관측된 train 구간", ha="center", color=TEAL, fontsize=13, fontweight="bold")
    rng = np.random.default_rng(0)
    xs = rng.uniform(0.7, 3.5, 18)
    ys = rng.uniform(1.9, 3.6, 18)
    ax.scatter(xs, ys, s=55, color=TEAL, zorder=3, edgecolors="white", linewidths=0.6)

    ax.plot([4.15, 4.15], [1.55, 4.45], color=CRIMSON, lw=2.5)
    arrow_h(ax, 4.25, 3.0, 10.9)
    ax.text(7.5, 4.25, "관측되지 않은 외삽 구간", ha="center", color=CRIMSON, fontsize=13, fontweight="bold")

    soft_card(ax, 4.5, 3.15, 6.4, 0.85, facecolor="white", edgecolor=RED, lw=1.8)
    ax.text(7.7, 3.57, "일반 NN:  자유롭게 연장  →  불안정·폭주 가능", ha="center", va="center", color=RED, fontsize=12, fontweight="bold")

    soft_card(ax, 4.5, 1.75, 6.4, 1.15, facecolor=SOFT_TEAL, edgecolor=TEAL, lw=2.2)
    ax.text(7.7, 2.55, "SAAR:  안정적 추세(affine)를 기본으로,", ha="center", va="center", color=TEAL, fontsize=12, fontweight="bold")
    ax.text(7.7, 2.05, "dual-scale residual은 제한된 보정만", ha="center", va="center", color=INK, fontsize=12)

    soft_card(ax, 0.35, 0.3, 10.7, 0.95, facecolor=PALE, edgecolor=LINE)
    ax.text(5.7, 0.78, "가정 인식형 외삽: NN 자유도를 줄이고,\n데이터가 지지하는 추세를 중심으로 예측을 보정한다.", ha="center", va="center", color=INK, fontsize=13, fontweight="bold")
    title_left(ax, "SAAR — Support-Aware Affine–Residual (식 없는 경로)")
    save(fig, "pp_core_idea.png")


def fig_pp_architecture():
    fig, ax = plt.subplots(figsize=(11.4, 5.35))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 5.35)
    ax.axis("off")

    soft_card(ax, 3.55, 4.35, 4.3, 0.7, facecolor=WASH, edgecolor=BLUE, lw=2)
    ax.text(5.7, 4.7, "history / health / rate / time", ha="center", va="center", color=BLUE, fontsize=13, fontweight="bold")

    soft_card(ax, 1.0, 2.55, 3.8, 1.35, facecolor=SOFT_ORANGE, edgecolor=ORANGE, lw=2.4)
    ax.text(2.9, 3.55, "Frozen Affine Path", ha="center", color=ORANGE, fontsize=14, fontweight="bold")
    ax.text(2.9, 3.0, "stable trend\nglobal extrapolation path", ha="center", color=INK, fontsize=11)

    soft_card(ax, 6.6, 2.55, 3.8, 1.35, facecolor=SOFT_TEAL, edgecolor=TEAL, lw=2.4)
    ax.text(8.5, 3.55, "Dual-Scale Residual SAAR", ha="center", color=TEAL, fontsize=14, fontweight="bold")
    ax.text(8.5, 3.0, "local nonlinear correction\nhistory-driven · B_L=2, B_H=6", ha="center", color=INK, fontsize=11)

    ax.annotate("", xy=(2.9, 3.9), xytext=(4.8, 4.35), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.8))
    ax.annotate("", xy=(8.5, 3.9), xytext=(6.6, 4.35), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.8))

    soft_card(ax, 2.4, 1.45, 6.6, 0.75, facecolor="white", edgecolor=NAVY, lw=2.2)
    ax.text(5.7, 1.82, "Support-Distance Gate  +  bounded dual-scale residual", ha="center", va="center", color=NAVY, fontsize=13, fontweight="bold")
    ax.annotate("", xy=(2.9, 2.2), xytext=(2.9, 2.55), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.6))
    ax.annotate("", xy=(8.5, 2.2), xytext=(8.5, 2.55), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.6))

    soft_card(ax, 3.9, 0.55, 3.6, 0.6, facecolor=NAVY, edgecolor="none")
    ax.text(5.7, 0.85, "RUL prediction", ha="center", va="center", color="white", fontsize=13, fontweight="bold")
    ax.annotate("", xy=(5.7, 1.15), xytext=(5.7, 1.45), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.6))

    title_left(ax, "SAAR 구조: Frozen Affine · Dual-Scale Residual · Support Gate → RUL")
    save(fig, "pp_architecture.png")


def fig_pp_equation_panel():
    fig, ax = plt.subplots(figsize=(11.4, 4.8))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    soft_card(ax, 0.4, 3.35, 10.6, 1.15, facecolor=WASH, edgecolor=TEAL, lw=2)
    ax.text(5.7, 4.05, r"$\hat{y} = m \cdot \mathrm{softplus}(\ell(z) + c_\theta(z))$", ha="center", va="center", color=INK, fontsize=17, fontweight="bold")
    ax.text(5.7, 3.55, r"$c_\theta = w\,B_L\tanh(r) + (1-w)\,B_H\tanh(r/B_H)$  ·  $B_L{=}2,\; B_H{=}6$", ha="center", va="center", color=NAVY, fontsize=12)

    terms = [
        (0.4, r"$\ell(z)$", "동결 affine\n기본 추세\n(폭주 방지)", ORANGE),
        (3.15, r"$c_\theta(z)$", "dual-scale\nresidual\n(제한 보정)", TEAL),
        (5.9, r"$B_L,B_H$", "가까우면 $B_L$\n멀면 $B_H$\n포화 상한", NAVY),
        (8.65, r"$w(d)$", "support\n거리 감쇠\ngate", CRIMSON),
    ]
    for x, ttitle, body, col in terms:
        soft_card(ax, x, 0.45, 2.5, 2.55, facecolor="white", edgecolor=col, lw=2.2)
        ax.add_patch(Rectangle((x, 2.6), 2.5, 0.4, facecolor=col, edgecolor="none"))
        ax.text(x + 1.25, 2.8, ttitle, ha="center", va="center", color="white", fontsize=13, fontweight="bold")
        ax.text(x + 1.25, 1.35, body, ha="center", va="center", color=INK, fontsize=12)
    title_left(ax, "SAAR 핵심식 — softplus affine + dual-scale residual")
    save(fig, "pp_equation_panel.png")


def fig_pp_shared_vs_data():
    fig, ax = plt.subplots(figsize=(11.4, 4.8))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    rows = [
        (3.55, "공용 외삽 prior", "Frozen affine path\ndual-scale SAAR residual\nsupport-distance gate", TEAL, "모든 데이터셋에\n같은 외삽 구조"),
        (2.05, "데이터별 학습", "affine 계수\nresidual NN\nbound · gate 강도", ORANGE, "추세와 residual만\n새로 맞춤"),
        (0.55, "도메인별 입력 표현", "배터리: capacity·rate·cycle\n기계: 센서 health·time history", NAVY, "식은 주입하지 않음\n관측 표현만 다름"),
    ]
    soft_card(ax, 0.35, 0.35, 10.7, 4.15, facecolor=PALE, edgecolor=LINE, lw=1, shadow=False)
    for y, title, body, col, note in rows:
        soft_card(ax, 0.55, y, 2.6, 1.25, facecolor=col, edgecolor=col, lw=0, shadow=False)
        ax.text(1.85, y + 0.62, title, ha="center", va="center", color="white", fontsize=13, fontweight="bold")
        ax.text(5.5, y + 0.62, body, ha="center", va="center", color=INK, fontsize=12)
        ax.text(9.5, y + 0.62, note, ha="center", va="center", color=GREY, fontsize=11)
    title_left(ax, "Assumption-Aware Extrapolation — 공용 vs 데이터별")
    save(fig, "pp_shared_vs_data.png")


def fig_support_adaptive():
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    d = np.linspace(0, 4, 200)
    w = 1 - (1 / (1 + np.exp(-(d - 1.2) / 0.35))) * (1 - 0.4)
    bound = w * 2 + (1 - w) * 6
    ax.plot(d, bound, color=TEAL, lw=3.2, label="허용 residual 상한")
    ax.axvline(1.2, color=ORANGE, ls="--", lw=1.8)
    ax.text(1.28, 5.55, "전환점 τ", color=ORANGE, fontsize=11, fontweight="bold")
    ax.fill_between(d, 0, bound, where=d <= 1.2, color=TEAL, alpha=0.12)
    ax.fill_between(d, 0, bound, where=d >= 1.2, color=ORANGE, alpha=0.10)
    ax.text(0.35, 2.6, "local\n$B_L=2$", color=TEAL, fontsize=12, fontweight="bold")
    ax.text(2.5, 4.7, "broad\n$B_H=6$", color=ORANGE, fontsize=12, fontweight="bold")
    ax.set_xlabel("support 거리 (정규화)", color=GREY)
    ax.set_ylabel("residual envelope", color=GREY)
    ax.set_ylim(0, 6.8)
    ax.set_xlim(0, 4)
    style_axes(ax)
    title_left(ax, "Support-adaptive dual-scale: 가까우면 세밀, 멀면 유한 포화")
    ax.legend(frameon=False, loc="lower right")
    save(fig, "support_adaptive.png")


def fig_main_results():
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    datasets = ["Sunwoda", "RWTH", "MICH"]
    models = {
        "고정 경계형": [0.939, 0.878, 0.468],
        "보정 제한 없음": [0.718, 0.788, 0.759],
        "거리 기반 보정": [0.894, 0.800, 0.736],
        "SAAR (최종)": [0.934, 0.842, 0.751],
    }
    colors = [GREY, BLUE, ORANGE, TEAL]
    x = np.arange(len(datasets))
    width = 0.18
    for i, (name, vals) in enumerate(models.items()):
        ax.bar(x + (i - 1.5) * width, vals, width, label=name, color=colors[i], edgecolor="white")
        for xi, v in zip(x + (i - 1.5) * width, vals):
            ax.text(xi, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=8, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=12)
    ax.set_ylabel("설명력 R² (5회 평균)", color=GREY)
    ax.set_ylim(0, 1.15)
    ax.axhline(0, color=LINE, lw=1)
    style_axes(ax)
    ax.legend(frameon=False, ncol=2, fontsize=9, loc="upper right")
    title_left(ax, "Ablation — SAAR가 평균과 어려운 MICH를 같이 올림", size=12)
    save(fig, "main_ablation_bars.png")


def fig_competitor():
    datasets = ["HUST", "Virkler", "NASA", "Sunwoda", "RWTH", "MATR19", "MATRb2", "NCMAPSS"]
    algos = ["SAAR", "V-REx", "GroupDRO", "Monotone", "LinRBF", "Engression", "GP", "TabPFN"]
    mat = np.array(
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
    show = np.clip(mat, -0.5, 1.0)

    fig, ax = plt.subplots(figsize=(11.4, 5.0))
    im = ax.imshow(show, aspect="auto", cmap="RdYlGn", vmin=-0.3, vmax=1.0)
    ax.set_xticks(np.arange(len(algos)))
    ax.set_yticks(np.arange(len(datasets)))
    ax.set_xticklabels(algos, fontsize=10)
    ax.set_yticklabels(datasets, fontsize=11)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    for i in range(len(datasets)):
        for j in range(len(algos)):
            v = mat[i, j]
            txt = f"{v:.2f}" if v > -1.5 else f"{v:.1f}"
            bold = j == 0 or (v == np.nanmax(mat[i]) and v > 0)
            ax.text(j, i, txt, ha="center", va="center", color=INK if abs(show[i, j]) < 0.85 else "white", fontsize=8.5, fontweight="bold" if bold else "normal")
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("설명력 R²", color=GREY)
    cbar.ax.tick_params(labelsize=9)
    title_left(ax, "잘 된 8곳 · 알고리즘별 R² (TabPFN 전체 반영)", size=13, pad=18)
    fig.text(0.08, 0.01, "TabPFN: HUST/Virkler/NASA·C-MAPSS계=동일예산 · Sunwoda/RWTH/MATRb2=고정 test·train≤1000 · MATR19 보조 · NCMAPSS 단일 seed", color=GREY, fontsize=8)
    save(fig, "competitor_bars.png")

    fig2, ax2 = plt.subplots(figsize=(11.2, 4.8))
    key = ["SAAR", "V-REx", "GroupDRO", "LinRBF", "Engression", "TabPFN"]
    key_idx = [algos.index(k) for k in key]
    colors = [TEAL, ORANGE, BLUE, NAVY, GREY, CRIMSON]
    x = np.arange(len(datasets))
    w = 0.13
    for ki, (name, j) in enumerate(zip(key, key_idx)):
        vals = mat[:, j]
        plot_vals = np.clip(vals, -0.25, None)
        ax2.bar(x + (ki - 2.5) * w, plot_vals, w, label=name, color=colors[ki], edgecolor="white")
    ax2.axhline(0, color=LINE, lw=1)
    ax2.set_xticks(x)
    ax2.set_xticklabels(datasets, fontsize=10)
    ax2.set_ylabel("설명력 R²", color=GREY)
    ax2.set_ylim(-0.3, 1.15)
    style_axes(ax2)
    ax2.legend(frameon=False, ncol=6, loc="upper center", fontsize=8)
    title_left(ax2, "주요 알고리즘 막대 비교 (TabPFN 포함)", size=12)
    save(fig2, "competitor_algo_bars.png")

    fig3, ax3 = plt.subplots(figsize=(10.6, 4.6))
    pp = mat[:, 0]
    pfn = mat[:, -1]
    x = np.arange(len(datasets))
    w = 0.36
    ax3.bar(x - w / 2, pp, w, color=TEAL, label="SAAR", edgecolor="white")
    ax3.bar(x + w / 2, np.clip(pfn, -1.0, None), w, color=CRIMSON, label="TabPFN", edgecolor="white")
    for i, (a, b) in enumerate(zip(pp, pfn)):
        ax3.text(i - w / 2, a + 0.02, f"{a:.2f}", ha="center", fontsize=8, color=INK)
        ypos = max(b, -1.0) + 0.02 if b > -1.0 else -0.92
        ax3.text(i + w / 2, ypos, f"{b:.2f}", ha="center", fontsize=8, color=CRIMSON)
    ax3.axhline(0, color=LINE, lw=1)
    ax3.set_xticks(x)
    ax3.set_xticklabels(datasets, fontsize=10)
    ax3.set_ylabel("설명력 R²", color=GREY)
    ax3.set_ylim(-1.1, 1.2)
    style_axes(ax3)
    ax3.legend(frameon=False, loc="upper right")
    title_left(ax3, "SAAR vs TabPFN (8곳 전체)", size=13)
    fig3.text(0.12, 0.02, "보조 비교: TabPFN은 train 행 상한·일부 단일 seed 조건이 포함됨", color=GREY, fontsize=9)
    save(fig3, "pp_vs_tabpfn.png")


def fig_fail_success_map():
    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    points = [
        (0.9, 0.85, "HUST", TEAL), (0.75, 0.78, "Virkler", TEAL), (0.55, 0.55, "NASA", TEAL),
        (0.8, 0.7, "Sunwoda", TEAL), (0.7, 0.65, "RWTH", TEAL), (0.5, 0.45, "MATR2019", ORANGE),
        (0.78, 0.72, "MATR b2", TEAL), (0.88, 0.82, "N-CMAPSS", TEAL),
        (0.2, 0.15, "MICH*", RED), (0.18, 0.2, "XJTU", RED), (0.15, 0.12, "FEMTO", RED), (0.12, 0.08, "Milling", RED),
    ]
    ax.axhline(0.5, color=LINE, ls=":", lw=1)
    ax.axvline(0.5, color=LINE, ls=":", lw=1)
    ax.fill_between([0.5, 1], 0.5, 1, color=TEAL, alpha=0.08)
    ax.fill_between([0, 0.5], 0, 0.5, color=RED, alpha=0.08)
    for x, y, name, c in points:
        ax.scatter([x], [y], s=120, color=c, edgecolors="white", linewidths=1.2, zorder=3)
        ax.text(x + 0.02, y + 0.03, name, color=c, fontsize=9, fontweight="bold")
    ax.text(0.72, 0.92, "성공 영역", color=TEAL, fontsize=12, fontweight="bold")
    ax.text(0.08, 0.42, "실패/기권 영역", color=RED, fontsize=12, fontweight="bold")
    ax.text(0.55, 0.08, "경계·보정 필요", color=ORANGE, fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("적용 조건 적합도 (개념축)", color=GREY)
    ax.set_ylabel("외삽 성능 (개념축)", color=GREY)
    title_left(ax, "실험 지형: 성공·경계·실패를 같은 지도에 (*기본 SAAR 기준)", size=12)
    style_axes(ax)
    save(fig, "experiment_map.png")


def fig_bootstrap():
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    names = ["HUST", "RWTH", "MATR2019"]
    means = [-25.19, -23.27, -10.63]
    lo = [-34.38, -41.79, -15.67]
    hi = [-14.54, -8.94, -6.37]
    y = np.arange(len(names))
    ax.axvline(0, color=RED, lw=1.5, ls="--")
    for i, (m, l, h) in enumerate(zip(means, lo, hi)):
        ax.plot([l, h], [i, i], color=TEAL, lw=4, solid_capstyle="round")
        ax.scatter([m], [i], color=NAVY, s=70, zorder=3)
        ax.text(h + 1.2, i, f"{m:.1f}  [{l:.1f}, {h:.1f}]", va="center", color=GREY, fontsize=10)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=12)
    ax.set_xlabel("unit RMSE 변화 (보정 후 − 전) · 95% bootstrap CI", color=GREY)
    title_left(ax, "Unit-level paired bootstrap: CI가 0 아래 = 일관된 개선", size=12)
    style_axes(ax)
    ax.invert_yaxis()
    save(fig, "bootstrap_ci.png")


def fig_pp_pae_flow():
    fig, ax = plt.subplots(figsize=(11.2, 4.8))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    stages = [
        (0.35, "분기", "외삽 문제", "후보식·관측 계약만 본다\n데이터셋 이름으로\n경로를 고르지 않음", GREY),
        (3.9, "식이 있을 때", "PAE", "식 = 뼈대\nNN = 부족분(제한 보정)\n실패 시 끔 / SAAR로", ORANGE),
        (7.45, "식이 없을 때", "SAAR / PP", "equation-free safeguard\n계약상 약한 bundle만\n기계적으로 켠다", TEAL),
    ]
    for x, title, tag, body, col in stages:
        soft_card(ax, x, 1.35, 3.1, 2.7, facecolor="white", edgecolor=col, lw=2.5)
        header_band(ax, x, 1.35, 3.1, 2.7, title, col)
        ax.text(x + 1.55, 3.25, tag, ha="center", color=col, fontsize=12, fontweight="bold")
        ax.text(x + 1.55, 2.15, body, ha="center", va="center", color=INK, fontsize=11)
    for x in [3.45, 7.0]:
        arrow_h(ax, x, 2.7, x + 0.35)
    soft_card(ax, 0.35, 0.25, 10.5, 0.85, facecolor=WASH, edgecolor=LINE)
    ax.text(5.6, 0.68, "Assumption-Aware Extrapolation  ·  PAE(식+NN)  ·  SAAR(식 없음)", ha="center", va="center", color=INK, fontsize=12, fontweight="bold")
    title_left(ax, "문제 계약 → 후보식 유무로 분기 → PAE / SAAR")
    save(fig, "pp_pae_flow.png")


def fig_pae_equation_nn():
    fig, ax = plt.subplots(figsize=(11.4, 5.2))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    soft_card(ax, 0.25, 0.35, 10.9, 4.5, facecolor=PALE, edgecolor=LINE, lw=1.2, shadow=False)
    nodes = [
        (0.45, 2.55, 1.85, 1.7, "① 후보식", "문헌 · LLM\n물리·경험식", ORANGE),
        (2.55, 2.55, 1.85, 1.7, "② 검증", "변수·단위\ntrain-only", CRIMSON),
        (4.65, 2.55, 2.55, 1.7, "③ 조립", "식 뼈대 + NN 부족분\n보정은 제한", NAVY),
        (7.5, 2.55, 1.7, 1.7, "④ 판정", "이득 있음?\non / off", TEAL),
        (9.5, 2.55, 1.55, 1.7, "⑤ 출력", "예측\n또는 거절", BLUE),
    ]
    for x, y, w, h, title, body, col in nodes:
        soft_card(ax, x, y, w, h, facecolor="white", edgecolor=col, lw=2.2)
        header_band(ax, x, y, w, h, title, col, size=12)
        ax.text(x + w / 2, y + 0.65, body, ha="center", va="center", color=INK, fontsize=11)
    for x in [2.3, 4.4, 7.2, 9.2]:
        arrow_h(ax, x, 3.4, x + 0.2)
    soft_card(ax, 0.55, 0.55, 4.7, 1.7, facecolor="white", edgecolor=ORANGE, lw=2)
    ax.text(2.9, 1.95, "식 (뼈대)", ha="center", color=ORANGE, fontsize=12, fontweight="bold")
    ax.text(2.9, 1.25, "방향 · 경계 · 관계\n검증된 항만 고정", ha="center", color=INK, fontsize=11)
    soft_card(ax, 5.55, 0.55, 5.2, 1.7, facecolor="white", edgecolor=TEAL, lw=2)
    ax.text(8.15, 1.95, "NN (부족분)", ha="center", color=TEAL, fontsize=12, fontweight="bold")
    ax.text(8.15, 1.25, "미지 파라미터 · 잔차 · 노이즈\n식 위에 제한적으로 학습", ha="center", color=INK, fontsize=11)
    ax.text(5.4, 1.7, "+", ha="center", color=NAVY, fontsize=16, fontweight="bold")
    title_left(ax, "PAE = 허용된 식 + 제한된 NN 보정 (equation-aware path)", size=13, pad=4)
    save(fig, "pae_equation_nn.png")


def fig_pp_vs_pae_split():
    fig, ax = plt.subplots(figsize=(11.4, 4.6))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    soft_card(ax, 0.3, 0.4, 5.2, 3.8, facecolor="white", edgecolor=TEAL, lw=2.8)
    ax.add_patch(Rectangle((0.3, 3.7), 5.2, 0.5, facecolor=TEAL, edgecolor="none"))
    ax.text(2.9, 3.95, "SAAR / PP  ·  equation-free safeguard", ha="center", va="center", color="white", fontsize=13, fontweight="bold")
    ax.text(2.9, 3.15, "명시적 도메인 식 없음", ha="center", color=INK, fontsize=13, fontweight="bold")
    for i, t in enumerate([
        "일반 구조 bias만 (affine · dual-scale · gate)",
        "계약 → 고정 rule로 weak bundle 기계적 활성",
        "중심 질문: 식 없이 외삽 형태를 어떻게 통제할까",
    ]):
        ax.text(0.65, 2.45 - i * 0.55, "·  " + t, ha="left", color=GREY, fontsize=11)

    soft_card(ax, 5.9, 0.4, 5.2, 3.8, facecolor="white", edgecolor=ORANGE, lw=2.8)
    ax.add_patch(Rectangle((5.9, 3.7), 5.2, 0.5, facecolor=ORANGE, edgecolor="none"))
    ax.text(8.5, 3.95, "PAE  ·  equation prior + NN", ha="center", va="center", color="white", fontsize=13, fontweight="bold")
    ax.text(8.5, 3.15, "후보식 검증 후 식+NN 조립", ha="center", color=INK, fontsize=13, fontweight="bold")
    for i, t in enumerate([
        "식 = 뼈대, NN = 부족분(제한 보정)",
        "이득 없으면 식 끔 · SAAR/거절로 fallback",
        "중심 질문: 어떤 식을 어떻게 넣을까",
    ]):
        ax.text(6.25, 2.45 - i * 0.55, "·  " + t, ha="left", color=GREY, fontsize=11)

    title_left(ax, "Dual path — PAE(식) vs SAAR(식 없음)")
    save(fig, "pp_vs_pae_split.png")


def fig_dataset_split():
    fig, ax = plt.subplots(figsize=(11.4, 4.8))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    steps = [
        (0.3, "① 계약 고정", "경계·unit·시간축\n인과 입력·외삽 좌표", ORANGE),
        (2.55, "② unit 분리", "같은 개체가\ntrain/val/test에\n동시에 안 들어감", TEAL),
        (4.8, "③ train support", "학습 unit의\n관측 범위 안만 사용", BLUE),
        (7.05, "④ hull-out만", "val/test는\n사전 좌표가\ntrain hull 밖인 행", CRIMSON),
        (9.3, "⑤ 선택·보고", "val만으로 설정\ntest R² 한 번 개봉", NAVY),
    ]
    for x, t, b, c in steps:
        soft_card(ax, x, 1.35, 1.95, 2.7, facecolor="white", edgecolor=c, lw=2.2)
        header_band(ax, x, 1.35, 1.95, 2.7, t, c, size=11)
        ax.text(x + 0.975, 2.4, b, ha="center", va="center", color=INK, fontsize=10)
        if x < 9:
            arrow_h(ax, x + 1.95, 2.7, x + 2.15)
    soft_card(ax, 0.3, 0.25, 10.8, 0.85, facecolor=WASH, edgecolor=LINE)
    ax.text(5.7, 0.68, "스케일·정규화는 train만  ·  seed 42–46  ·  주 지표: raw pooled R²", ha="center", va="center", color=INK, fontsize=12, fontweight="bold")
    title_left(ax, "공통 스플릿: 개체 분리 + 학습 support 밖(끝단)만 평가")
    save(fig, "dataset_split.png")


def fig_dataset_landscape():
    fig, ax = plt.subplots(figsize=(11.4, 4.9))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.9)
    ax.axis("off")
    blocks = [
        (0.3, 2.55, 5.3, 2.0, "잘 되는 축", TEAL,
         "열화 좌표 끝단 · 처음 보는 unit\n경계·방향이 맞고 val/test 이동이 비슷\nHUST · Virkler · NASA · Sunwoda\nRWTH · MATR · N-CMAPSS"),
        (5.9, 2.55, 5.2, 2.0, "안 되는 / 거절이 맞음", CRIMSON,
         "관계·메커니즘이 바뀜\n끝점 1개·유닛 너무 적음\nXJTU · FEMTO · milling\n기본 MICH → dual-scale로 회복"),
        (0.3, 0.35, 10.8, 1.9, "추론 대상 (공통)", NAVY,
         "주 타깃 = 남은수명(RUL) 또는 동등한 잔여량\n"
         "입력 = 인과적으로 관측 가능한 건강/부하/이력 요약 (미래·test 라벨 통계 금지)\n"
         "판정 = pooled R² + unit coverage + seed 안정성 + 경계 위반 0"),
    ]
    for x, y, w, h, title, col, body in blocks:
        soft_card(ax, x, y, w, h, facecolor="white", edgecolor=col, lw=2.4)
        ax.add_patch(Rectangle((x, y + h - 0.42), w, 0.42, facecolor=col, edgecolor="none"))
        ax.text(x + w / 2, y + h - 0.21, title, ha="center", va="center", color="white", fontsize=13, fontweight="bold")
        ax.text(x + w / 2, y + (h - 0.42) / 2, body, ha="center", va="center", color=INK, fontsize=11)
    title_left(ax, "데이터셋 지도 — 무엇을 맞히고, 언제 점수가 의미 있나")
    save(fig, "dataset_landscape.png")


def fig_mich_units():
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    units = [25, 26, 27, 28, 29, 30, 31, 32]
    r2 = [0.789, 0.609, 0.813, 0.761, 0.657, 0.722, 0.496, 0.957]
    colors = [TEAL if v >= 0.6 else ORANGE for v in r2]
    bars = ax.bar([str(u) for u in units], r2, color=colors, edgecolor="white")
    ax.axhline(0, color=LINE, lw=1)
    ax.axhline(0.751, color=NAVY, ls="--", lw=1.5, label="pooled 0.751")
    for b, v in zip(bars, r2):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}", ha="center", fontsize=9, color=INK)
    ax.set_ylabel("within-unit R²", color=GREY)
    ax.set_xlabel("MICH test unit", color=GREY)
    ax.set_ylim(0, 1.15)
    ax.legend(frameon=False)
    style_axes(ax)
    title_left(ax, "MICH: 8/8 unit 양의 R² (unit 31 복구 0.496)", size=12)
    save(fig, "mich_units.png")


def fig_protocol():
    fig, ax = plt.subplots(figsize=(10.8, 3.6))
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    steps = [
        (0.3, "① 나누기", "다른 개체끼리\n진짜 바깥만 테스트", ORANGE),
        (2.9, "② 고르기", "검증 구간만으로\n설정 결정", TEAL),
        (5.5, "③ 학습", "여러 번 재학습\n기본 경향은 고정", BLUE),
        (8.1, "④ 보고", "점수·안정성\n경계 위반 여부", NAVY),
    ]
    for x, t, b, c in steps:
        soft_card(ax, x, 0.7, 2.3, 2.2, facecolor="white", edgecolor=c, lw=2)
        ax.text(x + 1.15, 2.4, t, ha="center", color=c, fontsize=14, fontweight="bold")
        ax.text(x + 1.15, 1.5, b, ha="center", color=INK, fontsize=12)
        if x < 8:
            arrow_h(ax, x + 2.3, 1.8, x + 2.55, color=LINE)
    ax.text(5.4, 0.25, "테스트 정답은 모델 고를 때 보지 않는다", ha="center", color=CRIMSON, fontsize=11, fontweight="bold")
    title_left(ax, "검증 흐름 — Assumption-Aware Extrapolation protocol")
    save(fig, "protocol_flow.png")


def fig_research_route():
    fig, ax = plt.subplots(figsize=(12.2, 5.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    def box(x, y, w, h, facecolor, edge, text, tw=11, tc=INK, bold=False):
        soft_card(ax, x, y, w, h, facecolor=facecolor, edgecolor=edge, lw=1.8, shadow=False)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=tw, color=tc, fontweight="bold" if bold else "normal", linespacing=1.35)

    box(0.4, 4.55, 11.2, 0.65, WASH, LINE,
        "MOTIVATION  ·  밖을 지탱하는 것은 데이터가 아니라 가정이다.  식을 무조건 넣지도, NN에만 맡기지도 않겠다.")
    box(0.4, 3.85, 11.2, 0.55, PALE, NAVY,
        "OBSERVATIONS  ·  연속 열화 · unit 분리 · hull-out 평가 · val-only 선택")
    box(3.7, 2.85, 4.6, 0.7, NAVY, NAVY, "관측 · 경계 · 도메인 지식", tw=13, tc="white", bold=True)
    ax.annotate("", xy=(6, 2.65), xytext=(6, 2.85), arrowprops=dict(arrowstyle="->", color=LINE, lw=2))
    box(2.8, 1.85, 6.4, 0.7, CRIMSON, CRIMSON, "후보식이 정당화되는가?", tw=14, tc="white", bold=True)

    ax.annotate("", xy=(2.6, 1.45), xytext=(4.2, 1.85), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.2))
    ax.annotate("", xy=(9.4, 1.45), xytext=(7.8, 1.85), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.2))
    ax.text(3.0, 1.55, "YES", color=ORANGE, fontsize=11, fontweight="bold", ha="center")
    ax.text(8.8, 1.55, "NO", color=TEAL, fontsize=11, fontweight="bold", ha="center")

    box(0.35, 0.35, 5.0, 1.05, SOFT_ORANGE, ORANGE,
        "PAE  ·  equation-aware path\n허용된 식 + 제한 NN   ·   다음 논문", tw=12)
    box(6.65, 0.35, 5.0, 1.05, SOFT_TEAL, TEAL,
        "SAAR / PP  ·  equation-free (TODAY)\n가정 인식형 외삽 안전장치", tw=12, bold=True)

    ax.annotate("", xy=(6, 0.15), xytext=(2.85, 0.35), arrowprops=dict(arrowstyle="->", color=LINE, lw=1.6))
    ax.annotate("", xy=(6, 0.15), xytext=(9.15, 0.35), arrowprops=dict(arrowstyle="->", color=LINE, lw=1.6))
    box(2.2, 0.0, 7.6, 0.38, PALE, NAVY,
        "Assurance  ·  믿기 / 보류 / 거절까지 연결  ·  박사논문에서 두 경로를 한 프레임으로", tw=10, tc=NAVY)

    title_left(ax, "가정 인식형 외삽의 통합 루트 — Motivation → PAE / SAAR → Assurance", size=12, pad=4)
    save(fig, "research_route.png")


# ── New figures (replace PPT tables/cards) ───────────────────────────────────


def fig_status_update():
    fig, ax = plt.subplots(figsize=(11.2, 4.8))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    items = [
        ("유지", "SAAR / dual-scale BQ", "Sunwoda·RWTH·MICH\n0.934 / 0.842 / 0.751\n논문 1편의 주 executor", TEAL),
        ("확장", "Na / Zn-ion", "BQ만으로는 Zn untouched 실패 →\nRBF-regime·refit으로 개발 점수 회복", BLUE),
        ("교차", "XJTU · FEMTO · Milling", "구조 복구·입력 감사 단계\n통합 우월성 주장 전 아님", ORANGE),
        ("경계", "PAE / 저널", "결과 표는 PP만 · PAE 라우팅 실험 없음\n분야 Q1–Q2가 현실 본선", NAVY),
    ]
    card_grid_2x2(ax, items, x0=0.35, y0=0.35, w=5.2, h=1.85)
    title_left(ax, "최신 업데이트 (2026-09) — 유지 · 확장 · 교차 · 경계")
    save(fig, "status_update.png")


def fig_zn_ion_pathway():
    fig, ax = plt.subplots(figsize=(11.4, 4.6))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    steps = [
        ("1", "BQ fail", "untouched Zn\n실패 (≈ −0.38)", RED),
        ("2", "RBF-regime", "장수명 memory\n+ BQ 혼합", ORANGE),
        ("3", "α / refit", "강한 shrinkage +\nfull-dev refit", BLUE),
        ("4", "개발 점수", "Zn ≈ 0.91\nNa ≈ 0.82", TEAL),
    ]
    for i, (sn, sh, sb, scol) in enumerate(steps):
        x = 0.5 + i * 2.75
        soft_card(ax, x, 1.8, 2.45, 1.85, facecolor="white", edgecolor=scol, lw=2.2)
        ax.add_patch(Rectangle((x, 3.15), 2.45, 0.5, facecolor=scol, edgecolor="none"))
        ax.text(x + 0.2, 3.4, sn, ha="left", va="center", color="white", fontsize=16, fontweight="bold")
        ax.text(x + 0.55, 3.4, sh, ha="left", va="center", color="white", fontsize=13, fontweight="bold")
        ax.text(x + 0.2, 2.45, sb, ha="left", va="center", color=INK, fontsize=12)
        if i < 3:
            arrow_h(ax, x + 2.45, 2.7, x + 2.68)
    soft_card(ax, 0.35, 0.25, 10.75, 1.25, facecolor=WASH, edgecolor=LINE)
    ax.text(5.7, 0.88,
            "주의  ·  0.91/0.82는 사후 개발 결과 — 새 untouched 확증 아님\n"
            "개선 축: ridge shrinkage + validation 포함 refit  ·  RBF+BQ는 margin=0 미보장",
            ha="center", va="center", color=INK, fontsize=11)
    title_left(ax, "Zn-ion 경로 — BQ fail → RBF-regime → α/refit → 개발 점수")
    save(fig, "zn_ion_pathway.png")


def fig_score_attribution():
    fig, ax = plt.subplots(figsize=(11.4, 4.6))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    cards = [
        ("구조", "SAAR dual-scale로\nMICH 최저점 회복\n(고정 bound 0.468→0.751)\n\nZn lifetime 경로로\nBQ 단독 실패 보완", TEAL),
        ("계약·조율", "α=1000 affine shrinkage\nfull-development refit\n(같은 epoch로 val prefix 포함)\n\n같은 refit을 MLP에도\n줘야 공정 비교", ORANGE),
        ("아직 분리 안 됨", "RBF memory 정보량 vs\nNN residual 기여\n\n공정 NN 대조·nested\nunit CV·표본 수", RED),
    ]
    for i, (h, b, col) in enumerate(cards):
        x = 0.35 + i * 3.75
        soft_card(ax, x, 0.55, 3.45, 3.35, facecolor="white", edgecolor=col, lw=2.4)
        ax.add_patch(Rectangle((x, 3.52), 3.45, 0.38, facecolor=col, edgecolor="none"))
        ax.text(x + 1.72, 3.71, h, ha="center", va="center", color="white", fontsize=14, fontweight="bold")
        ax.text(x + 1.72, 1.85, b, ha="center", va="center", color=INK, fontsize=11, linespacing=1.35)
    title_left(ax, "점수가 오른 이유 — 구조 / 계약·조율 / 아직 분리 안 됨")
    save(fig, "score_attribution.png")


def fig_cross_domain_status():
    fig, ax = plt.subplots(figsize=(11.4, 4.2))
    headers = ["도메인", "상태", "핵심 수치/사실", "주장"]
    rows = [
        ["XJTU", "개발 개선", "progress+scale transport ≈ 0.257\n(기존 Ridge −0.84)", "post-test 개발. 독립 확증 아님"],
        ["FEMTO", "판정 보류/실패", "잘못된 진동 채널 발견\n교정 후 PP 구조들 채택 실패", "우월 실패가 아니라 설계 미성숙"],
        ["Milling", "감사", "일부 양수 점수는 수식 보정\nNN 경로 꺼진 경우 있음", "NN 기여와 보정 기여 분리 필요"],
        ["정보 한계", "이론", "비슷한 prefix + 다른 Z면\n어떤 f(H)도 한계", "안 보이는 lifetime을 복원하지 않음"],
    ]
    draw_table(ax, headers, rows, [0.4, 1.6, 3.0, 7.2], [1.1, 1.3, 4.0, 3.5], y0=3.6, row_h=0.55)
    title_left(ax, "교차 도메인 현황 — XJTU · FEMTO · Milling · 정보한계")
    save(fig, "cross_domain_status.png")


def fig_ablation_overview():
    fig, ax = plt.subplots(figsize=(11.4, 4.6))
    headers = ["기능", "제거하면", "켠 효과(요지)", "해석"]
    rows = [
        ["NN residual", "affine only", "MICH −3.3→0.47 등", "직선만으로는 부족"],
        ["Affine freeze", "trainable 경계NN", "세 데이터 모두 ↑", "NN이 tail 덮는 것 억제"],
        ["Residual bound", "unbounded", "Sun/RWTH ↑, MICH ↓", "조건부 — dual-scale로 보완"],
        ["Dual-scale", "고정 bound", "MICH 0.47→0.75", "이질 regime에서 용량 확대"],
        ["Rate history", "margin만", "Sun/RWTH 큰 ↑", "MICH는 단순 history가 유리한 반례"],
        ["Transport/gate", "always-on", "HUST·MATRb2 ↑", "증거 없으면 모듈 거절"],
    ]
    draw_table(ax, headers, rows, [0.4, 2.0, 3.7, 6.5], [1.5, 1.6, 2.6, 4.0], y0=4.0, row_h=0.48)
    title_left(ax, "Ablation overview — NN residual · Affine freeze · Dual-scale · Gate")
    save(fig, "ablation_overview.png")


def fig_gate_effect():
    fig, ax = plt.subplots(figsize=(11.2, 4.2))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    cards = [
        ("방식", "같은 split·같은 모델에서\n① 게이트 끔 (always-on)\n② 게이트 켬 (val 증거 있을 때만)\n차이를 비교", TEAL),
        ("결과", "13개 설정 감사:\n개선 3 · 유지 10 · 악화 0\n항상 켜면 Virkler 등 악화\n(−5.37→−6.56)", ORANGE),
        ("해석", "게이트는 평균 R²를\n직접 올리는 부품보다\n틀린 모듈을 막아\n기본 SAAR를 지키는 역할", NAVY),
    ]
    for i, (h, b, col) in enumerate(cards):
        x = 0.35 + i * 3.65
        soft_card(ax, x, 0.55, 3.35, 3.0, facecolor="white", edgecolor=col, lw=2.4)
        ax.add_patch(Rectangle((x, 3.17), 3.35, 0.38, facecolor=col, edgecolor="none"))
        ax.text(x + 1.67, 3.36, h, ha="center", va="center", color="white", fontsize=14, fontweight="bold")
        ax.text(x + 1.67, 1.75, b, ha="center", va="center", color=INK, fontsize=11, linespacing=1.35)
    title_left(ax, "Gate effect — 개선 3 · 유지 10 · 악화 0")
    save(fig, "gate_effect.png")


def fig_applicability_why():
    fig, ax = plt.subplots(figsize=(11.2, 4.2))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    cards = [
        ("할 수 없는 것", "테스트 정답을 보기 전에\n‘이번엔 R²가 몇이다’를\n맞춰 맞히는 일", RED),
        ("할 수 있는 것", "관측만으로 검사:\n이 문제에 SAAR를\n써도 되는가?\n안 되면 숫자를 내지 않기", TEAL),
        ("최종 출력", "예측 숫자\n+\n적용 가능 증명\n+\n거리·불확실성", NAVY),
    ]
    for i, (h, b, col) in enumerate(cards):
        x = 0.35 + i * 3.65
        soft_card(ax, x, 0.55, 3.35, 3.0, facecolor="white", edgecolor=col, lw=2.4)
        ax.add_patch(Rectangle((x, 3.17), 3.35, 0.38, facecolor=col, edgecolor="none"))
        ax.text(x + 1.67, 3.36, h, ha="center", va="center", color="white", fontsize=13, fontweight="bold")
        ax.text(x + 1.67, 1.75, b, ha="center", va="center", color=INK, fontsize=11, linespacing=1.35)
    title_left(ax, "조건 적합도 — 할 수 없는 것 / 할 수 있는 것 / 최종 출력")
    save(fig, "applicability_why.png")


def fig_applicability_checks():
    fig, ax = plt.subplots(figsize=(11.4, 5.0))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    checks = [
        ("① 문제 타입", "무엇을", "안 본 개체의\n학습 밖 남은수명인가?", "왜", "랜덤 미래예측과\n문제가 다르기 때문", TEAL),
        ("② 관측 계약", "무엇을", "경계·이력·방향이\n실제로 보이는가?", "왜", "없는 prior를 켜면\n가정이 거짓이 됨", ORANGE),
        ("③ Val 기술", "무엇을", "검증 끝단에서\n이미 도움이 되나?", "왜", "test 보기 전에\n실력 증거를 남김", BLUE),
        ("④ 거리·안정", "무엇을", "너무 멀거나\n재학습이 흔들리나?", "왜", "멀수록 가정 의존↑\n불안정하면 위험", NAVY),
        ("⑤ 경로 호환", "무엇을", "검증→시험 방향이\n비슷한가?", "왜", "반대면 보정을\n옮기면 안 됨", CRIMSON),
        ("⑥ 메커니즘", "무엇을", "재료·고장·센서\n의미가 같은가?", "왜", "다르면 모델이\n다른 현상을 봄", GREEN),
    ]
    for i, (title, a, av, b, bv, col) in enumerate(checks):
        x = 0.35 + (i % 3) * 3.75
        y = 0.35 + (1 - i // 3) * 2.35
        soft_card(ax, x, y, 3.45, 2.15, facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(Rectangle((x, y + 1.77), 3.45, 0.38, facecolor=col, edgecolor="none"))
        ax.text(x + 0.15, y + 1.96, title, ha="left", va="center", color="white", fontsize=12, fontweight="bold")
        ax.text(x + 0.15, y + 1.35, a, ha="left", color=col, fontsize=11, fontweight="bold")
        ax.text(x + 0.65, y + 1.25, av, ha="left", color=INK, fontsize=10.5)
        ax.text(x + 0.15, y + 0.55, b, ha="left", color=GREY, fontsize=11, fontweight="bold")
        ax.text(x + 0.65, y + 0.45, bv, ha="left", color=GREY, fontsize=10.5)
    title_left(ax, "조건 적합도 6가지 검사 — 2×3 grid")
    save(fig, "applicability_checks.png")


def fig_fit_decision():
    fig, ax = plt.subplots(figsize=(11.2, 4.6))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    steps = [
        ("Pass", "써도 된다", "6항이 대체로 통과\nval에서 실력도 확인", "→ SAAR 예측을 보고\n거리·불확실성과 함께 제시", TEAL),
        ("Weak", "조심해서", "문제는 맞지만\n거리 큼·증거 얇음", "→ 보정 줄이거나\n직선(identity)만 유지", ORANGE),
        ("Fail", "쓰지 않는다", "메커니즘이 다르거나\nval에서 이미 실패", "→ ABSTAIN\n숫자를 내지 않음", RED),
    ]
    for i, (tag, sub, mid, out, col) in enumerate(steps):
        x = 0.35 + i * 3.65
        soft_card(ax, x, 0.55, 3.35, 3.5, facecolor="white", edgecolor=col, lw=2.8)
        ax.add_patch(Rectangle((x, 3.67), 3.35, 0.55, facecolor=col, edgecolor="none"))
        ax.text(x + 1.67, 3.95, tag, ha="center", va="center", color="white", fontsize=18, fontweight="bold")
        ax.text(x + 1.67, 3.55, sub, ha="center", va="center", color="white", fontsize=11, fontweight="bold")
        ax.text(x + 1.67, 2.55, mid, ha="center", va="center", color=INK, fontsize=12)
        ax.text(x + 1.67, 1.15, out, ha="center", va="center", color=col, fontsize=12, fontweight="bold")
    title_left(ax, "적합도 판정 — Pass / Weak / Fail")
    save(fig, "fit_decision.png")


def fig_ablation_numbers():
    fig, ax = plt.subplots(figsize=(11.0, 4.4))
    headers = ["Arm", "Sunwoda", "RWTH", "MICH"]
    rows = [
        ["Direct NN (구조 없음)", "−1.35", "0.63", "0.68"],
        ["Affine only", "0.28", "0.66", "−3.34"],
        ["Trainable hard-boundary", "0.90", "0.86", "0.32"],
        ["Frozen + unbounded", "0.72", "0.79", "0.76"],
        ["BQ bounded (고정)", "0.94", "0.88", "0.47"],
        ["최종 dual-scale SAAR", "0.93", "0.84", "0.75"],
    ]
    draw_table(ax, headers, rows, [0.5, 3.8, 5.5, 7.2], [3.1, 1.5, 1.5, 1.5], y0=3.8, row_h=0.45, highlight_row=5)
    title_left(ax, "Ablation 수치 (matched arms) — 최종 dual-scale SAAR highlight")
    save(fig, "ablation_numbers.png")


def fig_dataset_catalog():
    fig, ax = plt.subplots(figsize=(11.4, 5.0))
    headers = ["데이터", "도메인", "추론", "스플릿·외삽", "결과 요지"]
    rows = [
        ["HUST", "배터리", "RUL", "안 본 프로토콜의\n깊은 미래/끝단", "잘 됨 · 0.96"],
        ["Virkler", "균열", "잔여 수명", "안 본 시편의\n균열 성장 끝단", "잘 됨 · 0.89"],
        ["NASA bat.", "배터리", "RUL", "건강도 끝단\n(LOBO 집계)", "잘 됨 · 0.58"],
        ["Sunwoda", "배터리", "RUL", "안 본 셀\n늦은 health", "잘 됨 · 0.87"],
        ["RWTH", "배터리", "RUL", "안 본 셀\n늦은 health", "잘 됨 · 0.74"],
        ["MICH", "배터리", "RUL", "안 본 셀\n새 regime", "통합 후 0.75"],
        ["MATR19/b2", "배터리", "RUL", "안 본 셀\n먼/가까운 꼬리", "보정 후 양수"],
        ["N-CMAPSS", "엔진", "RUL", "안 본 엔진\n× 고부하 × 만기", "잘 됨 · 0.94"],
    ]
    draw_table(ax, headers, rows, [0.4, 1.5, 2.5, 3.5, 6.8], [1.0, 0.9, 0.9, 3.1, 3.5], y0=4.5, row_h=0.42)
    ax.text(0.4, 0.15, "실패 축(별도): XJTU · FEMTO · NASA milling", color=CRIMSON, fontsize=10, fontweight="bold")
    title_left(ax, "Dataset catalog — HUST … N-CMAPSS")
    save(fig, "dataset_catalog.png")


def fig_applicability_checklist():
    fig, ax = plt.subplots(figsize=(11.4, 4.6))
    headers = ["검사", "통과 조건 (쉬운 말)", "실패하면"]
    rows = [
        ["① 문제", "안 본 개체 + 학습 밖 RUL인가?", "같은 개체 미래만 / 랜덤 split"],
        ["② 계약", "쓰는 prior에 필요한 관측이 있나?", "없는 경계·방향 강제"],
        ["③ Val", "검증 끝단에서 이미 도움이 되나?", "test만 보고 채택"],
        ["④ 안정", "거리·seed가 허용 범위인가?", "너무 멀거나 재학습 붕괴"],
        ["⑤ 호환", "검증→시험 이동이 비슷한가?", "방향 반대·관계 급변"],
        ["⑥ 메커니즘", "재료·고장·센서 의미가 같은가?", "다른 현상을 같은 모델에"],
    ]
    draw_table(ax, headers, rows, [0.4, 1.8, 6.5], [1.3, 4.5, 4.0], y0=4.0, row_h=0.48)
    title_left(ax, "Applicability checklist — Pass / Weak / Fail 판정 근거")
    save(fig, "applicability_checklist.png")


def fig_unified_model_table():
    fig, ax = plt.subplots(figsize=(11.4, 4.2))
    headers = ["모형", "Sunwoda", "RWTH", "MICH", "평균", "최고", "최저"]
    rows = [
        ["고정 경계형", "0.939", "0.878", "0.468", "0.762", "0.939", "0.468"],
        ["보정 제한 없음", "0.718", "0.788", "0.759", "0.755", "0.788", "0.718"],
        ["전체 적응형", "0.719", "0.738", "0.746", "0.734", "0.746", "0.719"],
        ["거리 기반 보정", "0.894", "0.800", "0.736", "0.810", "0.894", "0.736"],
        ["SAAR (최종)", "0.934", "0.842", "0.751", "0.842", "0.934", "0.751"],
    ]
    draw_table(ax, headers, rows, [0.35, 2.5, 3.6, 4.7, 5.8, 6.9, 8.0], [2.0, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95], y0=3.6, row_h=0.45, highlight_row=4)
    title_left(ax, "통합 모델 비교 — SAAR highlight (개발 3데이터)")
    save(fig, "unified_model_table.png")


def fig_fail_cases():
    fig, ax = plt.subplots(figsize=(11.2, 4.4))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    fails = [
        ("MICH (기본 PP)", "−1.522", "보정이 거의 안 켜짐\n형태/관계 실패\n→ dual-scale로 회복", RED),
        ("XJTU", "−1.229", "검증과 테스트의\n이동 방향이 반대\n→ 옮기지 않는 게 맞음", ORANGE),
        ("FEMTO", "−1.378", "베어링당 끝점 1개\n유닛 점수 정의 어려움", BLUE),
        ("NASA milling", "−4.826", "검증 유닛이 너무 적음\n나눔 자체가 불안정", NAVY),
    ]
    for i, (h, v, b, col) in enumerate(fails):
        x = 0.35 + i * 2.75
        soft_card(ax, x, 0.45, 2.55, 3.35, facecolor="white", edgecolor=col, lw=2.2)
        ax.add_patch(Rectangle((x, 3.42), 2.55, 0.38, facecolor=col, edgecolor="none"))
        ax.text(x + 1.27, 3.61, h, ha="center", va="center", color="white", fontsize=12, fontweight="bold")
        ax.text(x + 1.27, 2.85, v, ha="center", va="center", color=col, fontsize=22, fontweight="bold")
        ax.text(x + 1.27, 1.55, b, ha="center", va="center", color=GREY, fontsize=10.5, linespacing=1.35)
    title_left(ax, "Fail cases — MICH base · XJTU · FEMTO · Milling")
    save(fig, "fail_cases.png")


def fig_stats_evidence():
    fig, ax = plt.subplots(figsize=(11.2, 4.6))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    soft_card(ax, 0.35, 0.45, 5.2, 3.55, facecolor=SOFT_TEAL, edgecolor=TEAL, lw=2.2)
    ax.text(2.95, 3.65, "재학습 합의 규칙", ha="center", color=TEAL, fontsize=14, fontweight="bold")
    ax.text(2.95, 2.55, "보정 채택을 5번 재학습 투표로 봄\n5/5일 때만 승인 (단측 p=0.031)\n4/5는 거절\n\n주의: 물리 반복실험이 아니라\n초기화 안정성 검정", ha="center", va="center", color=INK, fontsize=11, linespacing=1.35)

    soft_card(ax, 5.75, 0.45, 5.1, 3.55, facecolor=WASH, edgecolor=BLUE, lw=2.2)
    ax.text(8.3, 3.65, "Unit paired bootstrap (20,000회)", ha="center", color=BLUE, fontsize=14, fontweight="bold")
    names = ["HUST", "RWTH", "MATR2019"]
    means = [-25.19, -23.27, -10.63]
    lo = [-34.38, -41.79, -15.67]
    hi = [-14.54, -8.94, -6.37]
    for i, (n, m, l, h) in enumerate(zip(names, means, lo, hi)):
        y = 2.85 - i * 0.75
        ax.plot([6.2 + (l + 40) / 80 * 3.8, 6.2 + (h + 40) / 80 * 3.8], [y, y], color=TEAL, lw=3.5, solid_capstyle="round", transform=ax.transData)
        ax.scatter([6.2 + (m + 40) / 80 * 3.8], [y], color=NAVY, s=50, zorder=3)
        ax.text(6.05, y, n, ha="right", va="center", color=GREY, fontsize=10)
        ax.text(10.5, y, f"{m:.1f}  [{l:.1f}, {h:.1f}]", ha="right", va="center", color=INK, fontsize=9)
    ax.text(8.3, 0.75, "세 곳 모두 CI < 0  ·  7곳 중 개선3 유지4 악화0", ha="center", color=CRIMSON, fontsize=10, fontweight="bold")

    title_left(ax, "Stats evidence — consensus + bootstrap CI")
    save(fig, "stats_evidence.png")


def fig_claim_boundary():
    fig, ax = plt.subplots(figsize=(11.2, 4.4))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    soft_card(ax, 0.35, 0.45, 5.2, 3.55, facecolor=SOFT_TEAL, edgecolor=TEAL, lw=2.4)
    ax.text(2.95, 3.65, "기여 (Claim)", ha="center", color=TEAL, fontsize=14, fontweight="bold")
    bullets = [
        "1) 개체 분리 + 범위 밖 RUL 문제 정의",
        "2) Frozen affine + dual-scale SAAR",
        "3) 검증으로만 승인하는 보정·gate",
        "4) 실패·거절까지 포함한 실험 지도",
    ]
    for i, t in enumerate(bullets):
        ax.text(0.65, 3.0 - i * 0.55, "·  " + t, ha="left", color=INK, fontsize=11)

    soft_card(ax, 5.75, 0.45, 5.1, 3.55, facecolor="#FEF2F2", edgecolor=RED, lw=2.4)
    ax.text(8.3, 3.65, "비기여 (Do NOT claim)", ha="center", color=RED, fontsize=14, fontweight="bold")
    bullets2 = [
        "최초 물리–신경망 혼합",
        "최초 affine+residual",
        "최초 범위 밖 평가",
        "모든 도메인 1등 · prior-free",
    ]
    for i, t in enumerate(bullets2):
        ax.text(6.05, 3.0 - i * 0.55, "·  " + t, ha="left", color=INK, fontsize=11)

    title_left(ax, "Claim boundary — 기여 vs 비기여")
    save(fig, "claim_boundary.png")


def fig_method_saar_detail():
    fig, ax = plt.subplots(figsize=(11.4, 4.8))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    soft_card(ax, 0.35, 2.55, 10.7, 1.55, facecolor=WASH, edgecolor=TEAL, lw=2)
    ax.text(5.7, 3.65, r"$\hat{y} = m \cdot \mathrm{softplus}(\ell(z) + c_\theta(z))$", ha="center", color=INK, fontsize=16, fontweight="bold")
    ax.text(5.7, 3.15, r"$c_\theta = w\,B_L\tanh(r) + (1-w)\,B_H\tanh(r/B_H)$  ·  Support-Distance Gate $w(d)$", ha="center", color=NAVY, fontsize=11)

    left = [
        "ℓ(z): 동결 affine — 관측 밖 폭주 방지",
        "c_θ: dual-scale residual (B_L=2, B_H=6)",
        "w(d): support 거리 감쇠 gate",
        "공용: affine + bounded residual + gate",
        "데이터별: 계수·NN·bound·gate 강도만 학습",
    ]
    right = [
        "배터리 열화식 사전 주입 아님",
        "도메인별은 입력 표현만 다름",
        "재학습 seed 42–46 (5회)",
        "검증 MSE로 설정·조기종료",
        "경계·보정 위반: 0/17,645",
    ]
    for i, t in enumerate(left):
        y = 2.15 - i * 0.38
        ax.add_patch(Rectangle((0.55, y - 0.06), 0.12, 0.12, facecolor=TEAL, edgecolor="none"))
        ax.text(0.8, y, t, ha="left", va="center", color=INK, fontsize=10.5)
    for i, t in enumerate(right):
        y = 2.15 - i * 0.38
        ax.add_patch(Rectangle((5.95, y - 0.06), 0.12, 0.12, facecolor=ORANGE, edgecolor="none"))
        ax.text(6.2, y, t, ha="left", va="center", color=INK, fontsize=10.5)

    title_left(ax, "SAAR method detail — Support-Aware Affine–Residual")
    save(fig, "method_saar_detail.png")


def fig_summary_executive():
    fig, ax = plt.subplots(figsize=(11.4, 5.0))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    soft_card(ax, 0.3, 3.85, 10.8, 0.85, facecolor=SOFT_TEAL, edgecolor=TEAL, lw=2.0)
    ax.text(5.7, 4.45, "EQUATION-FREE  ·  SAAR", ha="center", color=TEAL, fontsize=12, fontweight="bold", zorder=5)
    ax.text(
        5.7, 4.05,
        "식 없는 외삽 안전장치  ·  Frozen Affine + Dual-Scale Residual  ·  PAE는 이번 주결과 아님",
        ha="center", color=INK, fontsize=12, zorder=5,
    )

    kpis = [("Sunwoda", "0.934", "최고", TEAL), ("RWTH", "0.842", "중간", BLUE), ("MICH", "0.751", "최저 회복", ORANGE)]
    for i, (name, val, note, col) in enumerate(kpis):
        x = 0.4 + i * 3.7
        soft_card(ax, x, 2.15, 3.45, 1.5, facecolor="white", edgecolor=col, lw=2.6)
        ax.text(x + 1.72, 3.3, name, ha="center", color=GREY, fontsize=13, fontweight="bold", zorder=5)
        ax.text(x + 1.72, 2.75, val, ha="center", color=col, fontsize=32, fontweight="bold", zorder=5)
        ax.text(x + 1.72, 2.35, f"R²  ·  {note}", ha="center", color=GREY, fontsize=11, zorder=5)

    bits = [
        (0.4, "한 줄 식", r"$\hat y = m\,\mathrm{softplus}(\ell+c_\theta)$", NAVY),
        (4.1, "주장 범위", "연속 열화 · 경계 prior\n만능 SOTA 아님", ORANGE),
        (7.8, "아직", "Zn·베어링 = 한계\n분야 Q1–Q2 본선", CRIMSON),
    ]
    for x, h, b, col in bits:
        soft_card(ax, x, 0.55, 3.4, 1.4, facecolor="white", edgecolor=col, lw=2.0)
        ax.add_patch(Rectangle((x, 1.55), 3.4, 0.4, facecolor=col, edgecolor="none", zorder=5))
        ax.text(x + 1.7, 1.75, h, ha="center", va="center", color="white", fontsize=12, fontweight="bold", zorder=6)
        ax.text(x + 1.7, 1.0, b, ha="center", va="center", color=INK, fontsize=12, zorder=6)

    soft_card(ax, 0.3, 0.08, 10.8, 0.35, facecolor=NAVY, edgecolor="none", shadow=False)
    ax.text(
        5.7, 0.25,
        "Assumption-Aware Extrapolation  ·  SAAR = Support-Aware Affine–Residual",
        ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=5,
    )
    title_left(ax, "SAAR Executive Summary — 식 없는 경로의 지금 결론")
    save(fig, "summary_executive.png")


def main():
    # Existing deck figures
    fig_motivation()
    fig_prior_ladder()
    fig_pp_core_idea()
    fig_pp_architecture()
    fig_pp_equation_panel()
    fig_pp_shared_vs_data()
    fig_support_adaptive()
    fig_main_results()
    fig_competitor()
    fig_fail_success_map()
    fig_bootstrap()
    fig_pp_pae_flow()
    fig_pae_equation_nn()
    fig_pp_vs_pae_split()
    fig_dataset_split()
    fig_dataset_landscape()
    fig_mich_units()
    fig_protocol()
    fig_research_route()
    # New table/card replacements
    fig_status_update()
    fig_zn_ion_pathway()
    fig_score_attribution()
    fig_cross_domain_status()
    fig_ablation_overview()
    fig_gate_effect()
    fig_applicability_why()
    fig_applicability_checks()
    fig_fit_decision()
    fig_ablation_numbers()
    fig_dataset_catalog()
    fig_applicability_checklist()
    fig_unified_model_table()
    fig_fail_cases()
    fig_stats_evidence()
    fig_claim_boundary()
    fig_method_saar_detail()
    fig_summary_executive()
    print("done", OUT)


if __name__ == "__main__":
    main()
