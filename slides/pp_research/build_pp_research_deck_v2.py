#!/usr/bin/env python3
"""11-slide SAAR briefing — charts as PNG, tables as native PPT tables."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
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
    "soft": RGBColor(0xF2, 0xF2, 0xF0),
    "soft_teal": RGBColor(0xDC, 0xEB, 0xEB),
    "red": RGBColor(0x9B, 0x1C, 0x1C),
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


def add_table(
    slide,
    left,
    top,
    width,
    height,
    headers,
    rows,
    *,
    font_size=12,
    highlight_last=False,
    red_cols=None,
):
    """Native PowerPoint table — not a raster image."""
    red_cols = red_cols or set()
    nrows = 1 + len(rows)
    ncols = len(headers)
    table = slide.shapes.add_table(nrows, ncols, px(left), px(top), px(width), px(height)).table

    # equal-ish widths; first col a bit wider if text-heavy
    for j in range(ncols):
        table.columns[j].width = px(width / ncols)

    def fill_cell(cell, text, *, fill=None, color=None, bold=False, size=None, align="center"):
        cell.text = ""
        p = cell.text_frame.paragraphs[0]
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
        run = p.add_run()
        run.text = str(text)
        set_run(run, size=size or font_size, color=color or C["ink"], bold=bold)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        if fill is not None:
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
        else:
            cell.fill.background()

    for j, h in enumerate(headers):
        fill_cell(table.cell(0, j), h, fill=C["ink"], color=C["white"], bold=True, size=font_size)

    for i, row in enumerate(rows):
        last = highlight_last and i == len(rows) - 1
        bg = C["soft_teal"] if last else (C["soft"] if i % 2 else C["white"])
        for j, val in enumerate(row):
            col = C["teal"] if last else (C["red"] if j in red_cols else C["ink"])
            fill_cell(
                table.cell(i + 1, j),
                val,
                fill=bg,
                color=col,
                bold=last or j in red_cols or j == 0,
                size=font_size,
                align="left" if j in (0, 2, 3) and ncols >= 4 else "center",
            )
    return table


def head(slide, title, sub=""):
    rect(slide, 0, 0, 1280, 4, C["teal"])
    add_text(slide, 48, 22, 1180, 34, title, 22, C["ink"], True)
    if sub:
        add_text(slide, 48, 56, 1180, 20, sub, 12, C["muted"])


def foot(slide, n, total=11):
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
    TOTAL = 11

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

    # 2 Route (diagram)
    s = blank(prs)
    head(s, "연구 루트", "외삽을 범용화하고, 식 유무로 경로만 가른다")
    pic(s, "research_route.png", 40, 90, 1200, 540)
    foot(s, p(), TOTAL)

    # 3 Problem (chart)
    s = blank(prs)
    head(s, "문제", "support 밖에서는 데이터가 아니라 가정이 방향을 정한다")
    pic(s, "nn_vs_saar_curves.png", 50, 90, 1180, 540)
    foot(s, p(), TOTAL)

    # 4 Method (diagram)
    s = blank(prs)
    head(s, "방법 — SAAR", "동결 affine + dual-scale residual  ·  equation-free")
    pic(s, "pp_equation_panel.png", 40, 90, 1200, 520)
    foot(s, p(), TOTAL)

    # 5 KPI — native table + small chart
    s = blank(prs)
    head(s, "지금 결론", "개발 3배터리 주표")
    pic(s, "summary_executive.png", 40, 95, 700, 420)
    add_table(
        s,
        760,
        160,
        460,
        280,
        ["데이터", "R²"],
        [["Sunwoda", "0.934"], ["RWTH", "0.842"], ["MICH", "0.751"], ["평균", "0.842"]],
        font_size=14,
        highlight_last=True,
    )
    add_text(s, 760, 460, 460, 60, "만능 SOTA 아님  ·  PAE 결과는 이번 표에 없음", 12, C["muted"])
    foot(s, p(), TOTAL)

    # 6 Main results — chart + native table
    s = blank(prs)
    head(s, "주 결과", "같은 구조 · Sunwoda / RWTH / MICH")
    pic(s, "results_panel.png", 30, 90, 720, 480)
    add_table(
        s,
        760,
        120,
        470,
        320,
        ["모형", "Sun", "RWTH", "MICH", "평균", "최저"],
        [
            ["고정 경계", "0.939", "0.878", "0.468", "0.762", "0.468"],
            ["무제한", "0.718", "0.788", "0.759", "0.755", "0.718"],
            ["거리보정", "0.894", "0.800", "0.736", "0.810", "0.736"],
            ["SAAR", "0.934", "0.842", "0.751", "0.842", "0.751"],
        ],
        font_size=11,
        highlight_last=True,
    )
    add_text(s, 760, 460, 470, 50, "최저(MICH)를 살린 tradeoff  ·  확증 cohort 별도", 11, C["muted"])
    foot(s, p(), TOTAL)

    # 7 Ablation (charts)
    s = blank(prs)
    head(s, "Ablation", "고정 경계 → SAAR 이동  ·  평균–최저 tradeoff")
    pic(s, "ablation_panel.png", 30, 85, 1220, 550)
    foot(s, p(), TOTAL)

    # 8 Competitors — journal figure + native number table
    s = blank(prs)
    head(s, "비교", "(a) heatmap  ·  (b) SAAR vs TabPFN vs others  ·  아래는 동일 수치 표")
    pic(s, "competitor_bars.png", 40, 82, 1180, 360)
    add_table(
        s,
        40,
        455,
        1200,
        200,
        ["Dataset", "SAAR", "V-REx", "G-DRO", "Mono", "LinRBF", "Engr.", "GP", "TabPFN"],
        [
            ["HUST", "0.958", "0.809", "0.934", "0.822", "0.710", "0.878", "-0.32", "0.218"],
            ["Virkler", "0.888", "0.583", "0.554", "0.565", "0.805", "0.552", "0.54", "0.621"],
            ["NASA", "0.584", "0.285", "0.286", "0.283", "0.550", "0.549", "0.44", "-0.69"],
            ["Sunwoda", "0.865", "-0.24", "-0.30", "-0.05", "0.838", "0.619", "-1.60", "-0.89"],
            ["RWTH", "0.743", "0.645", "0.602", "-0.01", "0.385", "0.526", "-0.47", "-2.18"],
            ["MATR19", "0.466", "0.044", "0.272", "0.018", "-2.64", "-0.73", "-2.46", "0.202"],
            ["MATRb2", "0.862", "0.850", "0.777", "0.674", "-0.78", "0.739", "0.21", "0.618"],
            ["NCMAPSS", "0.937", "0.883", "0.880", "0.892", "0.819", "0.932", "0.80", "0.934"],
        ],
        font_size=9,
        highlight_last=False,
    )
    foot(s, p(), TOTAL)

    # 9 Robustness (charts)
    s = blank(prs)
    head(s, "안정성", "bootstrap CI  ·  MICH unit R²")
    pic(s, "robustness_panel.png", 30, 90, 1220, 530)
    foot(s, p(), TOTAL)

    # 10 Failures + limits — native tables only
    s = blank(prs)
    head(s, "실패 · 경계", "표로 남긴 한계  ·  주장 / 비주장")
    add_text(s, 48, 90, 600, 24, "실패 설정", 14, C["ink"], True)
    add_table(
        s,
        48,
        120,
        1184,
        240,
        ["설정", "기본 PP R²", "해석", "조치"],
        [
            ["MICH (기본)", "-1.522", "관계 이동 · 보정 꺼짐", "경계 + dual-scale → 0.751"],
            ["XJTU", "-1.229", "val/test 이동 반대", "거절 / 옮기지 않음"],
            ["FEMTO", "-1.378", "끝점 희소 · 채널 이슈", "설계 미성숙 · 보류"],
            ["NASA milling", "-4.826", "메커니즘 전이 · unit 극소", "사전 Fail / ABSTAIN"],
        ],
        font_size=12,
        red_cols={1},
    )
    add_text(s, 48, 390, 560, 24, "주장하는 것", 13, C["teal"], True)
    add_table(
        s,
        48,
        420,
        560,
        200,
        ["항목", "내용"],
        [
            ["주표", "0.934 / 0.842 / 0.751"],
            ["범위", "연속 열화 · unit-disjoint · hull-out"],
            ["방법", "동결 affine + dual-scale residual"],
            ["타깃", "분야 Q1–Q2"],
        ],
        font_size=11,
    )
    add_text(s, 640, 390, 560, 24, "아직 주장하지 않는 것", 13, C["red"], True)
    add_table(
        s,
        640,
        420,
        592,
        200,
        ["항목", "내용"],
        [
            ["Zn / Na", "사후 개발 — untouched 확증 아님"],
            ["교차도메인", "XJTU · FEMTO 우월성 전"],
            ["PAE", "식 라우팅 실험 없음 · 표 분리"],
            ["만능 SOTA", "모든 OOD 1등 아님"],
        ],
        font_size=11,
    )
    foot(s, p(), TOTAL)

    # 11 Dual path + takeaway
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
