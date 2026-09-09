#!/usr/bin/env python3
"""SAAR briefing — data charts (PNG) + native PPT text/tables only.

No boxed diagram images. Journal-style plots from numbers only.
"""

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
    "ink": RGBColor(0x22, 0x22, 0x22),
    "muted": RGBColor(0x66, 0x66, 0x66),
    "rule": RGBColor(0xE8, 0xE8, 0xE8),
    "blue": RGBColor(0x00, 0x72, 0xB2),
    "orange": RGBColor(0xE6, 0x9F, 0x00),
    "soft": RGBColor(0xF5, 0xF5, 0xF5),
    "soft_blue": RGBColor(0xE8, 0xF1, 0xF8),
    "white": RGBColor(0xFF, 0xFF, 0xFF),
    "red": RGBColor(0x9B, 0x1C, 0x1C),
}


def set_run(run, size=18, color=None, bold=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "Arial"
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
        sh.line.width = Pt(1.25)
    return sh


def pic(slide, name, left, top, width, height):
    path = FIGS / name
    if not path.exists():
        add_text(slide, left, top + 20, width, 24, f"missing: {name}", 12, C["muted"])
        return False
    slide.shapes.add_picture(str(path), px(left), px(top), px(width), px(height))
    return True


def add_table(slide, left, top, width, height, headers, rows, *, font_size=11, highlight_last=False, red_cols=None):
    red_cols = red_cols or set()
    table = slide.shapes.add_table(1 + len(rows), len(headers), px(left), px(top), px(width), px(height)).table
    for j in range(len(headers)):
        table.columns[j].width = px(width / len(headers))

    def cell(r, c, text, *, fill=None, color=None, bold=False, align="center"):
        cl = table.cell(r, c)
        cl.text = ""
        p = cl.text_frame.paragraphs[0]
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER}[align]
        run = p.add_run()
        run.text = str(text)
        set_run(run, size=font_size, color=color or C["ink"], bold=bold)
        cl.vertical_anchor = MSO_ANCHOR.MIDDLE
        if fill is not None:
            cl.fill.solid()
            cl.fill.fore_color.rgb = fill
        else:
            cl.fill.background()

    for j, h in enumerate(headers):
        cell(0, j, h, fill=C["ink"], color=C["white"], bold=True)
    for i, row in enumerate(rows):
        last = highlight_last and i == len(rows) - 1
        bg = C["soft_blue"] if last else (C["soft"] if i % 2 else C["white"])
        for j, val in enumerate(row):
            col = C["blue"] if last else (C["red"] if j in red_cols else C["ink"])
            cell(i + 1, j, val, fill=bg, color=col, bold=last or j in red_cols or j == 0, align="left" if j == 0 else "center")
    return table


def head(slide, title, sub=""):
    rect(slide, 0, 0, 1280, 3, C["blue"])
    add_text(slide, 48, 22, 1180, 32, title, 22, C["ink"], True)
    if sub:
        add_text(slide, 48, 54, 1180, 20, sub, 12, C["muted"])


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
    add_text(s, 100, 240, 1080, 48, "가정 인식형 외삽", 34, C["ink"], True, "center")
    add_text(s, 100, 300, 1080, 28, "Assumption-Aware Extrapolation", 16, C["muted"], False, "center")
    add_text(s, 100, 360, 1080, 28, "식 없는 경로  ·  SAAR", 16, C["blue"], True, "center")
    add_text(s, 100, 460, 1080, 24, "Smart Production Systems Lab.  ·  박사과정 박형배", 14, C["ink"], False, "center")
    add_text(s, 100, 510, 1080, 22, "2026.09.09", 13, C["muted"], False, "center")
    p()

    # 2 Route — PPT text only (no diagram image)
    s = blank(prs)
    head(s, "연구 루트", "외삽을 범용화하고, 식 유무로 경로만 가른다")
    add_text(s, 48, 100, 1180, 28, "밖을 지탱하는 것은 데이터가 아니라 가정이다.", 16, C["ink"], True)
    add_text(s, 48, 145, 1180, 24, "입력: 관측  ·  경계  ·  도메인 지식", 14, C["muted"])
    add_text(s, 48, 190, 1180, 24, "분기: 후보식이 정당화되는가?", 15, C["ink"], True)
    add_table(
        s,
        48,
        240,
        1184,
        220,
        ["분기", "경로", "내용", "단계"],
        [
            ["YES", "PAE", "허용된 식 + 제한 NN", "다음 논문"],
            ["NO", "SAAR", "동결 affine + dual-scale residual", "이번 발표 / 논문 1"],
        ],
        font_size=13,
        highlight_last=True,
    )
    add_text(s, 48, 500, 1180, 40, "Assurance: 믿기 / 보류 / 거절  →  박사논문에서 두 경로 통합", 14, C["muted"])
    foot(s, p(), TOTAL)

    # 3 Problem — data-style curve only
    s = blank(prs)
    head(s, "문제", "support 밖에서는 가정이 예측을 가른다")
    pic(s, "nn_vs_saar_curves.png", 80, 95, 1100, 520)
    foot(s, p(), TOTAL)

    # 4 Method — PPT text (no boxed figure)
    s = blank(prs)
    head(s, "방법 — SAAR", "equation-free  ·  Support-Aware Affine–Residual")
    add_text(s, 48, 110, 1180, 36, "ŷ = m · softplus( ℓ(z) + cθ(z) )", 20, C["ink"], True, "center")
    add_text(
        s,
        48,
        160,
        1180,
        28,
        "cθ = w·B_L tanh(rθ) + (1−w)·B_H tanh(rθ/B_H)   ·   B_L=2, B_H=6",
        14,
        C["muted"],
        False,
        "center",
    )
    add_table(
        s,
        80,
        230,
        1120,
        320,
        ["항", "역할"],
        [
            ["m", "경계 / 스케일"],
            ["ℓ(z)", "동결 affine — 밖으로도 폭주하지 않는 기본 추세"],
            ["cθ", "dual-scale residual — 가까우면 세밀, 멀면 유한 포화"],
            ["w(d)", "support 거리 gate — 멀수록 NN 보정 감쇠"],
        ],
        font_size=14,
    )
    foot(s, p(), TOTAL)

    # 5 KPI — bars + table
    s = blank(prs)
    head(s, "지금 결론", "개발 3배터리 주표")
    pic(s, "summary_bars.png", 60, 110, 620, 420)
    add_table(
        s,
        720,
        160,
        500,
        280,
        ["Dataset", "R²"],
        [["Sunwoda", "0.934"], ["RWTH", "0.842"], ["MICH", "0.751"], ["Mean", "0.842"]],
        font_size=16,
        highlight_last=True,
    )
    add_text(s, 720, 470, 500, 50, "만능 SOTA 아님  ·  PAE는 이번 표에 없음", 12, C["muted"])
    foot(s, p(), TOTAL)

    # 6 Main results
    s = blank(prs)
    head(s, "주 결과", "같은 구조 · Sunwoda / RWTH / MICH")
    pic(s, "results_panel.png", 40, 95, 700, 480)
    add_table(
        s,
        760,
        130,
        470,
        300,
        ["Model", "Sun", "RWTH", "MICH", "Mean", "Min"],
        [
            ["Fixed", "0.939", "0.878", "0.468", "0.762", "0.468"],
            ["Unbounded", "0.718", "0.788", "0.759", "0.755", "0.718"],
            ["Distance", "0.894", "0.800", "0.736", "0.810", "0.736"],
            ["SAAR", "0.934", "0.842", "0.751", "0.842", "0.751"],
        ],
        font_size=11,
        highlight_last=True,
    )
    add_text(s, 760, 460, 470, 40, "최저(MICH)를 살린 tradeoff", 12, C["muted"])
    foot(s, p(), TOTAL)

    # 7 Ablation
    s = blank(prs)
    head(s, "Ablation", "(a) Fixed→SAAR  ·  (b) mean–min tradeoff")
    pic(s, "ablation_panel.png", 50, 95, 1180, 520)
    foot(s, p(), TOTAL)

    # 8 Competitors
    s = blank(prs)
    head(s, "비교", "(a) heatmap  ·  (b) SAAR vs TabPFN vs others")
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
    )
    foot(s, p(), TOTAL)

    # 9 Robustness
    s = blank(prs)
    head(s, "안정성", "(a) bootstrap CI  ·  (b) MICH unit R²")
    pic(s, "robustness_panel.png", 50, 100, 1180, 500)
    foot(s, p(), TOTAL)

    # 10 Failures — tables only
    s = blank(prs)
    head(s, "실패 · 경계", "표로 남긴 한계")
    add_table(
        s,
        48,
        110,
        1184,
        230,
        ["Setting", "Base PP R²", "Interpretation", "Action"],
        [
            ["MICH (base)", "-1.522", "관계 이동 · 보정 꺼짐", "경계+dual-scale → 0.751"],
            ["XJTU", "-1.229", "val/test 이동 반대", "거절 / 옮기지 않음"],
            ["FEMTO", "-1.378", "끝점 희소 · 채널 이슈", "설계 미성숙 · 보류"],
            ["NASA milling", "-4.826", "메커니즘 전이 · unit 극소", "사전 Fail / ABSTAIN"],
        ],
        font_size=12,
        red_cols={1},
    )
    add_table(
        s,
        48,
        380,
        580,
        220,
        ["Claim", "Detail"],
        [
            ["Main scores", "0.934 / 0.842 / 0.751"],
            ["Scope", "연속 열화 · unit-disjoint · hull-out"],
            ["Method", "frozen affine + dual-scale residual"],
            ["Venue", "분야 Q1–Q2"],
        ],
        font_size=12,
    )
    add_table(
        s,
        660,
        380,
        572,
        220,
        ["Not claimed", "Detail"],
        [
            ["Zn / Na", "사후 개발 — untouched 확증 아님"],
            ["Cross-domain", "XJTU · FEMTO 우월성 전"],
            ["PAE", "식 라우팅 실험 없음"],
            ["Universal SOTA", "모든 OOD 1등 아님"],
        ],
        font_size=12,
    )
    foot(s, p(), TOTAL)

    # 11 Dual path — PPT table (no photo boxes) + takeaway
    s = blank(prs)
    head(s, "경로와 한 줄", "같은 외삽, 다른 입력")
    add_table(
        s,
        48,
        110,
        1184,
        280,
        ["", "SAAR (equation-free)", "PAE (equation-aware)"],
        [
            ["입력", "명시적 도메인 식 없음", "후보식 검증 후 사용"],
            ["구조", "동결 affine + dual-scale residual", "식 + 제한 NN"],
            ["실패 시", "거절 / identity", "끔 → SAAR fallback"],
            ["단계", "이번 발표 · 논문 1 주결과", "다음 논문 · 이번 표와 분리"],
        ],
        font_size=13,
    )
    add_text(s, 48, 440, 1180, 28, "1  밖을 지탱하는 것은 가정이지만, 식만 넣으면 답이 아니다.", 15, C["ink"])
    add_text(s, 48, 490, 1180, 28, "2  식이 없으면 SAAR.  주표 0.934 / 0.842 / 0.751.", 15, C["ink"])
    add_text(s, 48, 540, 1180, 28, "3  실패·Zn·PAE는 한계/후속. 만능 SOTA를 주장하지 않는다.", 15, C["ink"])
    foot(s, p(), TOTAL)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print(f"Saved {OUT} ({n} slides)")


if __name__ == "__main__":
    build()
