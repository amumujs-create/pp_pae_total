#!/usr/bin/env python3
"""Compact PP / SAAR briefing — graph-first, minimal chrome."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

OUT = Path("/Users/baghyeongbae/Desktop/연구/pp_pae_total/output/PP_Research_Detailed_v2.pptx")
ASSETS = Path("/Users/baghyeongbae/Desktop/연구/ppt/pp/_build")
FIGS = ASSETS / "figs"

W, H = 12192000, 6858000
PX = 9525


def px(n: float) -> int:
    return int(n * PX)


C = {
    "ink": RGBColor(0x1C, 0x1C, 0x1C),
    "muted": RGBColor(0x6A, 0x6A, 0x6A),
    "rule": RGBColor(0xE6, 0xE6, 0xE6),
    "soft": RGBColor(0xF4, 0xF4, 0xF2),
    "accent": RGBColor(0x0F, 0x5C, 0x5C),
    "navy": RGBColor(0x1F, 0x3A, 0x5F),
    "warn": RGBColor(0x8B, 0x2E, 0x2E),
    "white": RGBColor(0xFF, 0xFF, 0xFF),
}


def set_run(run, size=18, color=None, bold=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "AppleGothic"
    run.font.color.rgb = color or C["ink"]
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        from lxml import etree

        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", "AppleGothic")


def add_text(slide, left, top, width, height, text, size=18, color=None, bold=False, align="left"):
    box = slide.shapes.add_textbox(px(left), px(top), px(width), px(height))
    tf = box.text_frame
    tf.word_wrap = True
    lines = str(text).split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
        run = p.add_run()
        run.text = line
        set_run(run, size=size, color=color or C["ink"], bold=bold)
    return box


def rect(slide, left, top, width, height, fill=None, line=None):
    sh = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, px(left), px(top), px(width), px(height))
    sh.line.fill.background()
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is not None:
        sh.line.color.rgb = line
        sh.line.width = Pt(0.75)
    return sh


def pic(slide, name, left, top, width, height):
    path = FIGS / name
    if path.exists():
        slide.shapes.add_picture(str(path), px(left), px(top), px(width), px(height))
        return True
    add_text(slide, left, top + 40, width, 40, f"[missing] {name}", 14, C["warn"], True)
    return False


def head(slide, title, sub=""):
    """Minimal header: thin accent bar + title + optional one-line sub."""
    rect(slide, 0, 0, 1280, 3, C["accent"])
    add_text(slide, 56, 28, 1100, 36, title, 22, C["ink"], True)
    if sub:
        add_text(slide, 56, 64, 1100, 22, sub, 12, C["muted"])


def foot(slide, n):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, px(56), px(678), px(1224), px(678))
    line.line.color.rgb = C["rule"]
    line.line.width = Pt(0.75)
    add_text(slide, 56, 684, 700, 14, "SPS Lab  ·  Assumption-Aware Extrapolation", 9, C["muted"])
    add_text(slide, 1140, 682, 60, 16, f"{n:02d}", 10, C["muted"], True, "right")


def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C["white"]
    bg.line.fill.background()
    return s


def fig_slide(prs, n_fn, title, fig, sub="", note="", fig_box=(40, 100, 1200, 520)):
    s = blank(prs)
    head(s, title, sub)
    l, t, w, h = fig_box
    pic(s, fig, l, t, w, h)
    if note:
        add_text(s, 56, 640, 1100, 28, note, 11, C["muted"])
    foot(s, n_fn())
    return s


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    n = 0

    def p():
        nonlocal n
        n += 1
        return n

    # ── 01 Cover ──────────────────────────────────────────────
    s = blank(prs)
    for sh in list(s.shapes):
        sh._element.getparent().remove(sh._element)
    bg = s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C["white"]
    bg.line.fill.background()
    frame = s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, px(36), px(28), px(1208), px(664))
    frame.fill.background()
    frame.line.color.rgb = RGBColor(0x33, 0x33, 0x33)
    frame.line.width = Pt(1)
    logo = ASSETS / "sps_lab_logo.png"
    if logo.exists():
        s.shapes.add_picture(str(logo), px(860), px(56), px(340), px(68))
    add_text(s, 120, 250, 1040, 48, "가정 인식형 외삽", 34, C["ink"], True, "center")
    add_text(s, 120, 310, 1040, 28, "Assumption-Aware Extrapolation", 16, C["muted"], False, "center")
    add_text(s, 120, 370, 1040, 28, "식 없는 경로  ·  SAAR", 15, C["accent"], True, "center")
    add_text(s, 120, 470, 1040, 24, "Smart Production Systems Lab.  ·  박사과정 박형배", 14, C["ink"], False, "center")
    add_text(s, 120, 520, 1040, 22, "2026.09.09", 13, C["muted"], False, "center")
    p()

    # ── 02 Route ──────────────────────────────────────────────
    fig_slide(
        prs, p,
        "연구 루트",
        "research_route.png",
        "외삽을 범용화하고, 식 유무로 경로만 가른다",
        fig_box=(50, 95, 1180, 540),
    )

    # ── 03 Executive ──────────────────────────────────────────
    fig_slide(
        prs, p,
        "지금 결론",
        "summary_executive.png",
        "SAAR  ·  Sunwoda 0.934  ·  RWTH 0.842  ·  MICH 0.751",
        fig_box=(40, 100, 1200, 520),
    )

    # ── 04 Motivation ─────────────────────────────────────────
    fig_slide(
        prs, p,
        "왜 외삽이 어려운가",
        "motivation_futures.png",
        "support 안에서는 여러 함수가 맞고, 밖에서는 가정이 방향을 정한다",
        fig_box=(40, 100, 1200, 500),
    )

    # ── 05 NN vs SAAR (key graph) ──────────────────────────────
    fig_slide(
        prs, p,
        "핵심: NN은 밖으로 튀고, SAAR는 추세를 지킨다",
        "nn_vs_saar_curves.png",
        "동결 affine + 제한 residual",
        fig_box=(80, 100, 1120, 520),
    )

    # ── 06 Scope ──────────────────────────────────────────────
    fig_slide(
        prs, p,
        "연구 범위",
        "scope_inout.png",
        "unit 분리 · hull-out RUL  ·  식 없는 구조 prior",
        fig_box=(60, 100, 1160, 520),
    )

    # ── 07 Roadmap ────────────────────────────────────────────
    fig_slide(
        prs, p,
        "지금 / 다음 / 통합",
        "roadmap_line.png",
        "지금은 SAAR(PP). PAE와 Assurance는 이어질 경로.",
        fig_box=(40, 160, 1200, 400),
    )

    # ── 08 Equation ───────────────────────────────────────────
    fig_slide(
        prs, p,
        "SAAR 식",
        "pp_equation_panel.png",
        r"ŷ = m · softplus(ℓ + cθ)  ·  dual-scale residual",
        fig_box=(40, 100, 1200, 500),
    )

    # ── 09 Architecture + gate (two figs feel) ────────────────
    s = blank(prs)
    head(s, "구조", "Frozen Affine  ·  Dual-Scale Residual  ·  Support Gate")
    pic(s, "pp_architecture.png", 40, 95, 620, 500)
    pic(s, "support_adaptive.png", 680, 120, 540, 450)
    foot(s, p())

    # ── 10 Protocol ───────────────────────────────────────────
    fig_slide(
        prs, p,
        "검증",
        "protocol_flow.png",
        "unit 분리 · hull-out · val-only 선택 · test는 한 번만",
        fig_box=(40, 130, 1200, 420),
    )

    # ── 11 Main results ───────────────────────────────────────
    fig_slide(
        prs, p,
        "주 결과",
        "results_panel.png",
        "개발 3데이터  ·  최저점(MICH)을 살린 tradeoff",
        fig_box=(40, 100, 1200, 520),
    )

    # ── 12 Ablation movement ──────────────────────────────────
    s = blank(prs)
    head(s, "무엇이 움직였나", "고정 경계 → SAAR  ·  평균 vs 최저")
    pic(s, "ablation_slope.png", 30, 100, 620, 500)
    pic(s, "model_tradeoff.png", 660, 100, 560, 500)
    foot(s, p())

    # ── 13 Competitors ────────────────────────────────────────
    fig_slide(
        prs, p,
        "비교 — 잘 된 8곳",
        "competitor_bars.png",
        "행=데이터  ·  열=알고리즘  ·  SAAR 열 강조",
        fig_box=(40, 95, 1200, 520),
    )

    # ── 14 SAAR vs TabPFN ──────────────────────────────────────
    fig_slide(
        prs, p,
        "SAAR vs TabPFN",
        "pp_vs_tabpfn.png",
        "보조 비교(train 상한). MATRb2만으로 우위 주장하지 않음.",
        fig_box=(40, 100, 1200, 500),
    )

    # ── 15 Where it works ─────────────────────────────────────
    fig_slide(
        prs, p,
        "되는 곳 / 안 되는 곳",
        "experiment_map.png",
        fig_box=(80, 100, 1120, 520),
    )

    # ── 16 Stats + MICH ───────────────────────────────────────
    s = blank(prs)
    head(s, "안정성 · 유닛", "bootstrap CI  ·  MICH 8/8 양수")
    pic(s, "bootstrap_ci.png", 30, 105, 600, 480)
    pic(s, "mich_units.png", 650, 105, 570, 480)
    foot(s, p())

    # ── 17 Status / limits ────────────────────────────────────
    s = blank(prs)
    head(s, "한계와 경계", "확증이 아닌 것 · 아직 주장하지 않는 것")
    pic(s, "status_compact.png", 40, 100, 700, 480)
    pic(s, "limits_strip.png", 760, 180, 460, 320)
    foot(s, p())

    # ── 18 Failures ───────────────────────────────────────────
    fig_slide(
        prs, p,
        "실패도 남긴다",
        "fail_cases.png",
        "거절이 정직한 답이 되는 경우",
        fig_box=(40, 110, 1200, 500),
    )

    # ── 19 Dual path contrast ─────────────────────────────────
    fig_slide(
        prs, p,
        "PAE / SAAR",
        "pp_vs_pae_split.png",
        "같은 외삽, 다른 입력 — 식 있음 / 식 없음",
        fig_box=(40, 100, 1200, 500),
    )

    # ── 20 Takeaway ───────────────────────────────────────────
    s = blank(prs)
    head(s, "가져갈 말")
    lines = [
        ("1", "밖을 지탱하는 것은 데이터가 아니라 가정이다."),
        ("2", "식이 없으면 SAAR: 동결 affine + 제한 residual."),
        ("3", "주 결과 0.934 / 0.842 / 0.751 — 최저점을 살린 tradeoff."),
        ("4", "Zn·베어링·PAE는 한계/후속. 만능 SOTA를 주장하지 않는다."),
    ]
    for i, (num, t) in enumerate(lines):
        y = 130 + i * 100
        add_text(s, 70, y, 40, 36, num, 22, C["accent"], True)
        add_text(s, 120, y + 4, 1050, 40, t, 18, C["ink"])
    foot(s, p())

    # ── Appendix ──────────────────────────────────────────────
    s = blank(prs)
    add_text(s, 70, 280, 1100, 50, "APPENDIX", 36, C["ink"], True, "center")
    add_text(s, 70, 350, 1100, 30, "스플릿 · 방법 상세 · 원문 연결", 16, C["muted"], False, "center")
    foot(s, p())

    fig_slide(prs, p, "공통 스플릿", "dataset_split.png", fig_box=(40, 100, 1200, 500))
    fig_slide(prs, p, "방법 상세", "pp_equation_panel.png", "공용 구조 · 데이터별은 계수·NN만", fig_box=(40, 100, 1200, 500))
    fig_slide(prs, p, "Ablation 수치", "ablation_numbers.png", fig_box=(40, 100, 1200, 520))
    fig_slide(prs, p, "알고리즘 막대", "competitor_algo_bars.png", fig_box=(40, 100, 1200, 520))
    fig_slide(prs, p, "PAE 경로 (후속)", "pae_equation_nn.png", "식 뼈대 + 제한 NN", fig_box=(40, 100, 1200, 500))

    # file index — short
    s = blank(prs)
    head(s, "원문")
    files = [
        "MODEL_AND_SPLIT_KO.md",
        "UNIFIED_SUPPORT_GATED_PP_RESULTS_KO.md",
        "FINAL_PP_COMPONENT_ABLATION_RESULTS_KO.md",
        "ALL_DATASET_EXTRAPOLATION_COMPETITORS_KO.md",
        "STATISTICAL_NOVELTY_EVIDENCE_KO.md",
        "APPLICABILITY_NOVELTY_LIMITS_KO.md",
    ]
    for i, f in enumerate(files):
        add_text(s, 80, 120 + i * 70, 1100, 36, f"·  {f}", 16, C["ink"])
    foot(s, p())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print(f"Saved {OUT} ({n} slides)")
    print("Figures:", sorted(p.name for p in FIGS.glob("*.png") if p.stat().st_mtime))


if __name__ == "__main__":
    build()
