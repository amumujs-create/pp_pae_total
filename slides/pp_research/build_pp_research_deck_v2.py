#!/usr/bin/env python3
"""~12-slide SAAR briefing — sharp data figures, minimal chrome."""

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
    "ink": RGBColor(0x11, 0x11, 0x11),
    "muted": RGBColor(0x55, 0x55, 0x55),
    "rule": RGBColor(0xD0, 0xD0, 0xD0),
    "teal": RGBColor(0x0A, 0x5C, 0x5C),
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
    for i, line in enumerate(str(text).split("\n")):
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
        sh.line.width = Pt(1)
    return sh


def pic(slide, name, left, top, width, height):
    path = FIGS / name
    if not path.exists():
        add_text(slide, left, top + 40, width, 30, f"missing: {name}", 14, C["muted"], True)
        return False
    slide.shapes.add_picture(str(path), px(left), px(top), px(width), px(height))
    return True


def head(slide, title, sub=""):
    rect(slide, 0, 0, 1280, 4, C["teal"])
    add_text(slide, 48, 22, 1180, 34, title, 22, C["ink"], True)
    if sub:
        add_text(slide, 48, 56, 1180, 20, sub, 12, C["muted"])


def foot(slide, n, total=12):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, px(48), px(680), px(1232), px(680))
    line.line.color.rgb = C["rule"]
    line.line.width = Pt(0.75)
    add_text(slide, 48, 686, 800, 14, "SPS Lab  ·  Assumption-Aware Extrapolation  ·  SAAR", 9, C["muted"])
    add_text(slide, 1100, 684, 100, 16, f"{n}/{total}", 10, C["muted"], True, "right")


def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C["white"]
    bg.line.fill.background()
    return s


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    n = 0
    TOTAL = 12

    def p():
        nonlocal n
        n += 1
        return n

    # 1 Cover
    s = blank(prs)
    for sh in list(s.shapes):
        sh._element.getparent().remove(sh._element)
    bg = s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C["white"]
    bg.line.fill.background()
    frame = s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, px(40), px(32), px(1200), px(656))
    frame.fill.background()
    frame.line.color.rgb = RGBColor(0x22, 0x22, 0x22)
    frame.line.width = Pt(1.25)
    logo = ASSETS / "sps_lab_logo.png"
    if logo.exists():
        s.shapes.add_picture(str(logo), px(860), px(58), px(320), px(64))
    add_text(s, 100, 240, 1080, 48, "가정 인식형 외삽", 36, C["ink"], True, "center")
    add_text(s, 100, 300, 1080, 28, "Assumption-Aware Extrapolation", 16, C["muted"], False, "center")
    add_text(s, 100, 360, 1080, 28, "식 없는 경로  ·  SAAR", 16, C["teal"], True, "center")
    add_text(s, 100, 460, 1080, 24, "Smart Production Systems Lab.  ·  박사과정 박형배", 14, C["ink"], False, "center")
    add_text(s, 100, 510, 1080, 22, "2026.09.09", 13, C["muted"], False, "center")
    p()

    # 2 Route
    s = blank(prs)
    head(s, "연구 루트", "외삽을 범용화하고, 식 유무로 경로만 가른다")
    pic(s, "research_route.png", 40, 90, 1200, 540)
    foot(s, p(), TOTAL)

    # 3 Problem
    s = blank(prs)
    head(s, "문제", "support 밖에서는 데이터가 아니라 가정이 방향을 정한다")
    pic(s, "nn_vs_saar_curves.png", 50, 90, 1180, 540)
    foot(s, p(), TOTAL)

    # 4 Method
    s = blank(prs)
    head(s, "방법 — SAAR", "동결 affine + dual-scale residual  ·  equation-free")
    pic(s, "pp_equation_panel.png", 40, 90, 1200, 520)
    foot(s, p(), TOTAL)

    # 5 Now conclusion (KPI)
    s = blank(prs)
    head(s, "지금 결론", "개발 3배터리 주표")
    pic(s, "summary_executive.png", 40, 100, 1200, 500)
    foot(s, p(), TOTAL)

    # 6 Main results table+bars
    s = blank(prs)
    head(s, "주 결과", "같은 구조 · Sunwoda / RWTH / MICH")
    pic(s, "results_panel.png", 30, 85, 1220, 550)
    foot(s, p(), TOTAL)

    # 7 Ablation
    s = blank(prs)
    head(s, "Ablation", "고정 경계 → SAAR 이동  ·  평균–최저 tradeoff")
    pic(s, "ablation_panel.png", 30, 85, 1220, 550)
    foot(s, p(), TOTAL)

    # 8 Competitors
    s = blank(prs)
    head(s, "비교", "양의 8곳 × 알고리즘 $R^2$")
    pic(s, "competitor_bars.png", 30, 80, 1220, 560)
    foot(s, p(), TOTAL)

    # 9 vs TabPFN
    s = blank(prs)
    head(s, "SAAR vs TabPFN", "표 수치 기반 막대 비교")
    pic(s, "pp_vs_tabpfn.png", 40, 90, 1200, 540)
    foot(s, p(), TOTAL)

    # 10 Robustness
    s = blank(prs)
    head(s, "안정성", "bootstrap CI  ·  MICH unit $R^2$")
    pic(s, "robustness_panel.png", 30, 90, 1220, 530)
    foot(s, p(), TOTAL)

    # 11 Failures + limits
    s = blank(prs)
    head(s, "실패 · 경계", "표로 남긴 한계  ·  주장 / 비주장")
    pic(s, "fail_cases.png", 30, 85, 620, 520)
    pic(s, "status_compact.png", 660, 85, 560, 520)
    foot(s, p(), TOTAL)

    # 12 Dual path + takeaway
    s = blank(prs)
    head(s, "경로와 한 줄", "PAE / SAAR  ·  오늘 가져갈 말")
    pic(s, "pp_vs_pae_split.png", 40, 85, 1200, 380)
    add_text(s, 56, 490, 1160, 28, "1  밖을 지탱하는 것은 가정이지만, 식만 넣으면 답이 아니다.", 14, C["ink"])
    add_text(s, 56, 530, 1160, 28, "2  식이 없으면 SAAR — 동결 affine + 제한 residual.  주표 0.934 / 0.842 / 0.751.", 14, C["ink"])
    add_text(s, 56, 570, 1160, 28, "3  실패·Zn·PAE는 한계/후속. 만능 SOTA를 주장하지 않는다.", 14, C["ink"])
    foot(s, p(), TOTAL)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print(f"Saved {OUT} ({n} slides)")


if __name__ == "__main__":
    build()
