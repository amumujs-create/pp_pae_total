#!/usr/bin/env python3
"""Detailed study PDF for the PP-X paper-main method."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

ROOT = Path("/Users/baghyeongbae/Desktop/연구")
FIGS = ROOT / "ppt/pp/_build/figs"
OUT = ROOT / "pp_pae_total/output/PP_PPX_Study_Detailed.pdf"

FONT = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
pdfmetrics.registerFont(TTFont("AppleGothic", FONT))

INK = HexColor("#111111")
MUTED = HexColor("#555555")
TEAL = HexColor("#0A5C5C")
NAVY = HexColor("#1A3355")
RULE = HexColor("#D0D0D0")
SOFT = HexColor("#F2F2F0")
RED = HexColor("#9B1C1C")

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm


def styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(name="CoverTitle", fontName="AppleGothic", fontSize=26, leading=34, textColor=INK, alignment=TA_CENTER, spaceAfter=8))
    ss.add(ParagraphStyle(name="CoverSub", fontName="AppleGothic", fontSize=12, leading=18, textColor=MUTED, alignment=TA_CENTER, spaceAfter=6))
    ss.add(ParagraphStyle(name="H1", fontName="AppleGothic", fontSize=16, leading=22, textColor=TEAL, spaceBefore=4, spaceAfter=8))
    ss.add(ParagraphStyle(name="H2", fontName="AppleGothic", fontSize=12, leading=17, textColor=NAVY, spaceBefore=10, spaceAfter=5))
    ss.add(ParagraphStyle(name="Body", fontName="AppleGothic", fontSize=10, leading=15, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6))
    ss.add(ParagraphStyle(name="BulletKo", fontName="AppleGothic", fontSize=10, leading=14, textColor=INK, leftIndent=8, spaceAfter=2))
    ss.add(ParagraphStyle(name="Caption", fontName="AppleGothic", fontSize=8.5, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceBefore=3, spaceAfter=10))
    ss.add(ParagraphStyle(name="Small", fontName="AppleGothic", fontSize=8.5, leading=12, textColor=MUTED, spaceAfter=3))
    ss.add(ParagraphStyle(name="Footer", fontName="AppleGothic", fontSize=8, leading=10, textColor=MUTED, alignment=TA_CENTER))
    ss.add(ParagraphStyle(name="Eq", fontName="AppleGothic", fontSize=11, leading=16, textColor=INK, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8))
    return ss


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(2)
    canvas.line(MARGIN, PAGE_H - 10 * mm, PAGE_W - MARGIN, PAGE_H - 10 * mm)
    canvas.setFont("AppleGothic", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 10 * mm, "SPS Lab  ·  PP-X paper main  ·  frozen method v1")
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def fig(name: str, width=170 * mm, max_h=95 * mm):
    path = FIGS / name
    if not path.exists():
        return Paragraph(f"[missing figure: {name}]", styles()["Small"])
    img = Image(str(path))
    img.hAlign = "CENTER"
    # scale preserving aspect
    iw, ih = img.imageWidth, img.imageHeight
    scale = min(width / iw, max_h / ih)
    img.drawWidth = iw * scale
    img.drawHeight = ih * scale
    return img


def bullets(items, style):
    return [Paragraph(f"·  {t}", style) for t in items]


def data_table(headers, rows, col_widths=None):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, hAlign="CENTER")
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "AppleGothic"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    # highlight the final PP-X/core row
    if len(rows) >= 1 and ("PP-X" in str(rows[-1][0]) or "SAAR" in str(rows[-1][0])):
        style_cmds += [
            ("BACKGROUND", (0, -1), (-1, -1), HexColor("#DCEBEB")),
            ("TEXTCOLOR", (0, -1), (-1, -1), TEAL),
            ("FONTNAME", (0, -1), (-1, -1), "AppleGothic"),
        ]
    t.setStyle(TableStyle(style_cmds))
    return t


def build():
    S = styles()
    story = []

    # ── Cover ──
    story.append(Spacer(1, 35 * mm))
    story.append(Paragraph("가정 인식형 외삽", S["CoverTitle"]))
    story.append(Paragraph("Assumption-Aware Extrapolation", S["CoverSub"]))
    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width="60%", thickness=1.2, color=TEAL, spaceBefore=2, spaceAfter=8, hAlign="CENTER"))
    story.append(Paragraph("상세 공부 노트  ·  PP-X paper main", S["CoverSub"]))
    story.append(Paragraph("validation-approved prior-residual framework  ·  frozen method v1", S["CoverSub"]))
    story.append(Spacer(1, 18 * mm))
    story.append(Paragraph("Smart Production Systems Lab.", S["CoverSub"]))
    story.append(Paragraph("박사과정 박진서  ·  2026.09.11", S["CoverSub"]))
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph(
        "이 PDF는 PP-X 브리핑의 <b>상세 공부 버전</b>이다. "
        "문제 정의 · 방법 · 프로토콜 · 표 수치 · 한계 · 원문 연결을 한곳에 모았다.",
        S["Body"],
    ))
    story.append(PageBreak())

    # ── 1 Program ──
    story.append(Paragraph("1. 프로그램 한 줄", S["H1"]))
    story.append(Paragraph(
        "목표는 외삽을 <b>범용화</b>하는 것이다. 식 유무는 문제를 둘로 쪼개는 것이 아니라, "
        "같은 외삽 목표 안에서 <b>가정 강도에 따라 경로를 고르는 조건</b>이다.",
        S["Body"],
    ))
    story.extend(bullets([
        "paper main → <b>PP-X</b>: validation-approved prior-residual framework",
        "SAAR = historical alias / core architecture; PP-X 전체와 동의어가 아님",
        "prior reject → 사전 고정 fallback 또는 abstention",
        "PAE = future program; paper main이 아님",
    ], S["BulletKo"]))
    story.append(Spacer(1, 4 * mm))
    story.append(fig("research_route.png", 170 * mm, 88 * mm))
    story.append(Paragraph("그림 1. 연구 루트 — 현재 paper main은 PP-X, PAE는 future program", S["Caption"]))
    story.append(PageBreak())

    # ── Modeling intent / contributions / positioning ──
    story.append(Paragraph("2. 모델링 의도와 research gap", S["H1"]))
    story.append(Paragraph(
        "<b>PP-X treats extrapolation as test-independent approval/rejection of structural assumptions.</b> "
        "즉, test sample별로 모델을 고르는 문제가 아니라 배포 전에 구조 가정의 사용 권한을 승인하거나 거절하는 문제다.",
        S["Body"],
    ))
    story.extend(bullets([
        "<b>Declare</b> typed contract: state, strict tail, units, prior, fallback을 선언",
        "<b>Learn</b> source-supported residual around a frozen prior",
        "<b>Approve</b> or decline with physical-unit evidence",
        "<b>Decline</b> 시 exact frozen fallback 또는 abstention",
    ], S["BulletKo"]))
    story.append(Paragraph("Research gap", S["H2"]))
    story.append(Paragraph(
        "개별 affine+NN, hard boundary, gate의 최초성이 아니라 "
        "<b>typed admissibility + prior-centered residual authority + predeployment unit-risk approval/fallback</b>의 결합이 novelty다.",
        S["Body"],
    ))
    story.append(PageBreak())

    story.append(Paragraph("3. 본 연구의 기여와 evidence mapping", S["H1"]))
    story.append(data_table(
        ["기여", "핵심 증거", "반례 / 한계"],
        [
            ["Typed contract + conditional execution", "common backbone 6/12; RMSE-only 7/12 (FA 4); unit-risk 8/12 (FA 2, FR 2)", "RWTH dual-scale 악화; MICH fixed-bound 악화"],
            ["Prior-preserving residual", "25 units: direct 17/25 p=.0028; soft 24/25; affine 25/25; bound 0/17,645", "frozen/trainable p=.071; bounded/unbounded p=.578 미확증"],
            ["Approval / fallback", "Sun +.221; MICH +.283; HUST +.128; MATRb2 +.187; DS03 route PASS", "DS03 .8818 < Engression .9013"],
        ],
        col_widths=[45 * mm, 70 * mm, 43 * mm],
    ))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Novelty positioning", S["H2"]))
    story.append(data_table(
        ["계열", "PP-X와의 차이"],
        [
            ["PINN", "완전식이 필수 아님; typed partial prior를 승인·거절"],
            ["prior-residual hybrid", "frozen prior 중심 residual authority + unit-risk approval"],
            ["MoE", "sample-wise test routing 없음; predeployment executor/fallback 동결"],
            ["Engression", "generic distribution보다 approved structural tail 보존"],
            ["V-REx", "source-domain risk invariance가 아니라 state-level strict-tail + prior authority"],
        ],
        col_widths=[45 * mm, 110 * mm],
    ))
    story.append(Paragraph(
        "최초 hybrid/PINN, literature 또는 universal SOTA, safety guarantee는 주장하지 않는다.",
        S["Small"],
    ))
    story.append(PageBreak())

    story.append(Paragraph("4. Claim–evidence–limitation과 투고 전략", S["H1"]))
    story.append(data_table(
        ["Tier", "Evidence", "Limitation"],
        [
            ["A Mixed strongest same-split retrospective", "9/9; p=.00390625; 77 units; equal-dataset geometric RMSE −33.8%; hierarchical CI 15.8–48.6%", "comparator budget heterogeneous; paired comparator와 pooled strongest 일부 다름"],
            ["B Uniformly tuned equal-budget retrospective", "9×8 baselines×30 candidates×5 refit; 8/9; p=.0391; Virkler −.002", "30은 방법별 후보예산; 전체 구조개발 횟수 아님; 5 seeds는 독립 표본 아님"],
            ["C DS03 prospective truth test", "fallback .8818; basic .832; multiscale .869; Engression .9013", "route PASS, predictive superiority FAIL; CRT/GCIE rejected"],
        ],
        col_widths=[45 * mm, 65 * mm, 48 * mm],
    ))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "<b>투고 bottleneck: 독립 prospective predictive superiority 1개 추가 필요.</b> "
        "그 전에는 retrospective breadth와 route-selection validity만 주장하며 세 tier를 pooled evidence로 합치지 않는다.",
        S["Body"],
    ))
    story.append(PageBreak())

    # ── 2 Problem ──
    story.append(Paragraph("5. 왜 외삽이 어려운가", S["H1"]))
    story.append(Paragraph(
        "학습 support 안에서는 여러 함수가 비슷하게 맞는다. "
        "밖에서는 데이터가 방향을 정해주지 못하고, <b>가정이 예측을 가른다</b>. "
        "제약이 없는 NN은 support 밖에서 폭주하기 쉽고, "
        "물리식을 세게 넣으면 그 식이 틀릴 때 오히려 위험하다.",
        S["Body"],
    ))
    story.append(fig("nn_vs_ppx_curves.png", 170 * mm, 85 * mm))
    story.append(Paragraph("그림 2. support 경계 밖: 제약 없는 NN vs PP-X core", S["Caption"]))
    story.append(Paragraph("PP-X가 하는 일", S["H2"]))
    story.extend(bullets([
        "기본 추세(동결 affine)를 밖으로 연장한다",
        "NN residual은 <b>유한 상한</b> 안에서만 보정한다",
        "support에서 멀수록 보정 비중을 줄인다 (dual-scale / gate)",
        "계약이 안 맞으면 숫자를 내지 않고 거절할 수 있게 설계한다",
    ], S["BulletKo"]))
    story.append(PageBreak())

    # ── 3 Method ──
    story.append(Paragraph("6. 방법 — Algorithm 1: Declare–Learn–Approve–Decline", S["H1"]))
    story.append(Paragraph(
        "<b>PP-X</b>는 prior-residual candidate를 validation evidence로 승인하고, "
        "지원되는 executor만 실행하며, prior가 거절되면 fallback 또는 abstention하는 "
        "paper-main top-level framework다. test sample별 routing은 없고 test는 frozen forward만 수행한다. "
        "SAAR는 historical alias / core architecture다.",
        S["Body"],
    ))
    story.append(Paragraph("ŷ = m · softplus( ℓ(z) + cθ(z) )", S["Eq"]))
    story.append(Paragraph(
        "cθ = w · BL tanh(rθ) + (1−w) · BH tanh(rθ/BH) ,  BL=2 , BH=6",
        S["Eq"],
    ))
    story.append(fig("pp_equation_panel.png", 170 * mm, 72 * mm))
    story.append(Paragraph("그림 3. PP-X historical core 식과 항의 역할", S["Caption"]))
    story.append(Paragraph("항 해석", S["H2"]))
    story.extend(bullets([
        "m : 경계/스케일 (관측 가능한 health 경계가 있을 때 quotient 확장 가능; 과거 BQ-SAAR/BQ-PP label)",
        "ℓ(z) : 동결 affine — 밖으로도 폭주하지 않는 기본 추세",
        "cθ : dual-scale residual — 가까우면 세밀(BL), 멀면 유한 포화(BH)",
        "w(d) : support 거리 gate — 멀수록 NN 보정 감쇠",
    ], S["BulletKo"]))
    if (FIGS / "support_adaptive.png").exists():
        story.append(fig("support_adaptive.png", 140 * mm, 70 * mm))
        story.append(Paragraph("그림 4. support-adaptive residual envelope", S["Caption"]))
    story.append(PageBreak())

    # ── 4 Scope / protocol ──
    story.append(Paragraph("4. 문제 범위와 검증 프로토콜", S["H1"]))
    story.append(Paragraph("In scope", S["H2"]))
    story.extend(bullets([
        "연속 열화의 남은수명(RUL) 또는 동등 잔여량",
        "unit(개체) 분리 평가 — 같은 셀/시편/엔진이 train·val·test에 동시 등장 금지",
        "사전 좌표의 train convex hull 밖(hull-out)만 점수",
        "validation-approved prior-residual 실행 (PP-X)",
    ], S["BulletKo"]))
    story.append(Paragraph("Out of scope", S["H2"]))
    story.extend(bullets([
        "임의 tabular 만능 외삽 / 모든 OOD 1등 주장",
        "도메인 물리식 발견·주입 (그건 PAE)",
        "같은 개체 단순 미래예측만으로 ‘외삽 성공’ 주장",
        "test 라벨을 보고 prior·구조를 다시 고르기",
    ], S["BulletKo"]))
    if (FIGS / "dataset_split.png").exists():
        story.append(fig("dataset_split.png", 170 * mm, 70 * mm))
        story.append(Paragraph("그림 5. 공통 스플릿: 계약 → unit 분리 → train support → hull-out → val-only 선택", S["Caption"]))
    if (FIGS / "protocol_flow.png").exists():
        story.append(fig("protocol_flow.png", 170 * mm, 55 * mm))
        story.append(Paragraph("그림 6. 검증 흐름 — test 정답은 모델 고를 때 보지 않는다", S["Caption"]))
    story.append(PageBreak())

    # ── 5 Main results ──
    story.append(Paragraph("5. 역사적 core 결과 (개발 3데이터)", S["H1"]))
    story.append(Paragraph(
        "논문 주표는 Sunwoda / RWTH / MICH에 같은 구조·설정을 공동 적용한 개발 결과다. "
        "확증 cohort는 별도. Zn·베어링은 한계/확장으로 분리한다.",
        S["Body"],
    ))
    story.append(fig("results_panel.png", 175 * mm, 82 * mm))
    story.append(Paragraph("그림 7. historical SAAR core가 평균·최저를 같이 올린 개발 결과", S["Caption"]))
    story.append(data_table(
        ["모형", "Sunwoda", "RWTH", "MICH", "평균", "최고", "최저"],
        [
            ["고정 경계형", "0.939", "0.878", "0.468", "0.762", "0.939", "0.468"],
            ["보정 제한 없음", "0.718", "0.788", "0.759", "0.755", "0.788", "0.718"],
            ["전체 적응형", "0.719", "0.738", "0.746", "0.734", "0.746", "0.719"],
            ["거리 기반 보정", "0.894", "0.800", "0.736", "0.810", "0.894", "0.736"],
            ["SAAR (historical core)", "0.934", "0.842", "0.751", "0.842", "0.934", "0.751"],
        ],
        col_widths=[28 * mm, 20 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm],
    ))
    story.append(Paragraph(
        "해석: 이 표는 historical core mechanism evidence다. 최고점은 고정 경계형(0.939)과 비슷하고 최저는 0.751로 회복한다.",
        S["Small"],
    ))
    story.append(PageBreak())

    # ── 6 Ablation ──
    story.append(Paragraph("6. Ablation — 무엇이 성능을 만드나", S["H1"]))
    story.append(fig("ablation_panel.png", 175 * mm, 78 * mm))
    story.append(Paragraph("그림 8. 고정 경계→historical SAAR core 이동 · 평균–최저 tradeoff", S["Caption"]))
    story.append(data_table(
        ["Arm", "Sunwoda", "RWTH", "MICH"],
        [
            ["Direct NN (구조 없음)", "-1.35", "0.63", "0.68"],
            ["Affine only", "0.28", "0.66", "-3.34"],
            ["Trainable hard-boundary", "0.90", "0.86", "0.32"],
            ["Frozen + unbounded", "0.72", "0.79", "0.76"],
            ["BQ bounded (고정)", "0.94", "0.88", "0.47"],
            ["SAAR dual-scale (legacy)", "0.93", "0.84", "0.75"],
        ],
        col_widths=[45 * mm, 30 * mm, 30 * mm, 30 * mm],
    ))
    story.append(Spacer(1, 3 * mm))
    story.extend(bullets([
        "핵심: frozen affine + nonlinear residual (둘 다 필요)",
        "고정 bound는 Sun/RWTH↑, MICH↓ → dual-scale이 worst-domain 회복",
        "‘모든 부품이 모든 데이터에서 항상 이긴다’가 아니라 regime별 승인",
    ], S["BulletKo"]))
    story.append(PageBreak())

    # ── 7 Competitors ──
    story.append(Paragraph("7. 9-setting retrospective portfolio 비교", S["H1"]))
    story.append(Paragraph(
        "알고리즘: PP-X, V-REx, GroupDRO, Monotone, LinRBF, Engression, GP, TabPFN. "
        "이 포트폴리오는 retrospective concept-aligned evidence이며 prospective 확증으로 읽지 않는다. "
        "9/9, 양측 p=.0039는 이질적 strongest same-split comparison이다.",
        S["Body"],
    ))
    story.append(fig("competitor_bars.png", 175 * mm, 110 * mm))
    story.append(Paragraph("그림 9. heatmap + 막대 요약 (TabPFN 포함)", S["Caption"]))
    story.append(PageBreak())

    # ── 8 Prospective / final boundary ──
    story.append(Paragraph("8. 동일예산 retrospective와 DS03 prospective 경계", S["H1"]))
    story.append(Paragraph(
        "사전에 고정한 동일예산 protocol은 <b>9 settings × 8 baselines × 30 candidates × 5 refit</b>이다. "
        "PP-X는 8/9에서 우세했고 양측 sign p=.0391이었다. Virkler는 −0.002로 승리에 포함하지 않는다.",
        S["Body"],
    ))
    story.append(data_table(
        ["항목", "PP-X / 개발안", "비교 / 결과", "판정"],
        [
            ["Equal-budget retrospective", "8/9", "p=.0391 · Virkler −0.002", "동일예산 우세 방향"],
            ["DS03", "frozen fallback .8818", "Engression .9013", "route PASS · superiority FAIL"],
            ["CCMR v2.2", "trajectory-domain", "executor only", "PP-X main 아님"],
            ["CRT", "DS03 .8851", "< Engression .9013", "rejected"],
            ["GCIE", ".8850 · nested .8727", "< Engression .9013", "rejected"],
        ],
        col_widths=[31 * mm, 43 * mm, 45 * mm, 43 * mm],
    ))
    story.append(Spacer(1, 5 * mm))
    story.extend(bullets([
        "PP-X = paper-main top-level framework; frozen method v1",
        "SAAR = historical alias / core architecture",
        "CRT와 GCIE는 Algorithm 1 미포함",
        "prior reject 시 frozen fallback 또는 abstention",
        "N-CMAPSS 0.937 portfolio split과 DS03는 서로 다른 split·비교",
    ], S["BulletKo"]))
    story.append(PageBreak())

    # ── 9 Robustness ──
    story.append(Paragraph("9. 안정성 · 유닛 효과", S["H1"]))
    story.append(fig("robustness_panel.png", 175 * mm, 78 * mm))
    story.append(Paragraph("그림 11. Bootstrap CI · MICH unit R²", S["Caption"]))
    story.extend(bullets([
        "HUST / RWTH / MATR2019: unit RMSE 변화의 95% CI가 모두 0 아래 → 긴 시계열 몇 개의 착시가 아님",
        "MICH: 8/8 unit 양의 R², pooled 0.751 (unit 31도 0.496으로 회복)",
        "도메인 수가 적어 ‘모든 분야에서 유의’라고 쓰면 안 된다",
    ], S["BulletKo"]))
    story.append(PageBreak())

    # ── 10 Failures ──
    story.append(Paragraph("10. 실패 설정 — 거절이 정직한 답", S["H1"]))
    story.append(fig("fail_cases.png", 170 * mm, 70 * mm))
    story.append(Paragraph("그림 12. 실패 표", S["Caption"]))
    story.append(data_table(
        ["설정", "기본 PP R²", "해석", "조치"],
        [
            ["MICH (기본)", "-1.522", "관계 이동", "경계+dual-scale → 0.751"],
            ["XJTU", "-1.229", "val/test 이동 반대", "거절 / 옮기지 않음"],
            ["FEMTO", "-1.378", "끝점 희소", "설계 미성숙 · 보류"],
            ["NASA milling", "-4.826", "메커니즘 전이", "사전 Fail / ABSTAIN"],
        ],
        col_widths=[32 * mm, 28 * mm, 40 * mm, 48 * mm],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(fig("status_compact.png", 170 * mm, 72 * mm))
    story.append(Paragraph("그림 13. 주장하는 것 / 아직 주장하지 않는 것", S["Caption"]))
    story.append(PageBreak())

    # ── 11 PAE ──
    story.append(Paragraph("11. PAE future program과의 경계", S["H1"]))
    story.append(fig("pp_vs_pae_split.png", 170 * mm, 70 * mm))
    story.append(Paragraph("그림 14. PP-X vs PAE — PP-X가 paper main, PAE는 future program", S["Caption"]))
    if (FIGS / "pae_equation_nn.png").exists():
        story.append(fig("pae_equation_nn.png", 170 * mm, 75 * mm))
        story.append(Paragraph("그림 15. PAE = 허용된 식 + 제한 NN (후속)", S["Caption"]))
    story.extend(bullets([
        "PAE는 future program — 이번 PP-X paper-main 결과 표와 분리",
        "식이 이득 없으면 PP-X / fallback / abstention으로 가는 그림이 목표",
        "저널 현실 본선: 분야 Q1–Q2 (RESS / MSSP / IEEE 계열)",
    ], S["BulletKo"]))
    story.append(PageBreak())

    # ── 12 Applicability (study) ──
    story.append(Paragraph("12. 조건 적합도 (허가증, 성적표 아님)", S["H1"]))
    story.append(Paragraph(
        "밖의 R²를 미리 맞춰 맞힐 수는 없다. "
        "할 수 있는 것은 test 라벨 없이 <b>이 가정으로 말해도 되는가</b>를 검사하는 것이다.",
        S["Body"],
    ))
    story.append(data_table(
        ["검사", "통과 조건", "실패하면"],
        [
            ["① 문제", "안 본 개체 + 학습 밖 RUL", "같은 개체 미래 / 랜덤 split"],
            ["② 계약", "prior에 필요한 관측 존재", "없는 경계·방향 강제"],
            ["③ Val", "검증 끝단에서 이미 도움", "test만 보고 채택"],
            ["④ 안정", "거리·seed 허용", "너무 멀거나 재학습 붕괴"],
            ["⑤ 호환", "val→test 이동 유사", "방향 반대·관계 급변"],
            ["⑥ 메커니즘", "재료·고장·센서 의미 동일", "다른 현상을 같은 모델에"],
        ],
        col_widths=[22 * mm, 70 * mm, 55 * mm],
    ))
    story.append(Spacer(1, 3 * mm))
    story.extend(bullets([
        "Pass → 예측 + 거리·불확실성 함께 제시",
        "Weak → 보정 축소 / identity 유지",
        "Fail → ABSTAIN (숫자를 내지 않음)",
    ], S["BulletKo"]))
    story.append(PageBreak())

    # ── 13 Reading list ──
    story.append(Paragraph("13. 원문 읽는 순서", S["H1"]))
    story.append(Paragraph("브리핑 → 실험 원문 → 문헌조사", S["Body"]))
    files = [
        ("① 프로그램", "ASSUMPTION_AWARE_EXTRAPOLATION_PROGRAM_KO.md"),
        ("② 문제·분할", "MODEL_AND_SPLIT_KO.md"),
        ("③ 최종 결과", "UNIFIED_SUPPORT_GATED_PP_RESULTS_KO.md"),
        ("④ 경계형", "BOUNDARY_QUOTIENT_PP_RESULTS_KO.md"),
        ("⑤ Ablation", "FINAL_PP_COMPONENT_ABLATION_RESULTS_KO.md"),
        ("⑥ 경쟁", "ALL_DATASET_EXTRAPOLATION_COMPETITORS_KO.md"),
        ("⑦ 통계", "STATISTICAL_NOVELTY_EVIDENCE_KO.md"),
        ("⑧ 적합도", "APPLICABILITY_NOVELTY_LIMITS_KO.md"),
        ("⑨ 노벨티", "NOVELTY_LITERATURE_AUDIT_KO.md / PP_FIRST_PUBLICATION_CLAIMS_KO.md"),
        ("⑩ 명칭", "slides/pp_research/PPX_NAMING.md"),
    ]
    story.append(data_table(
        ["단계", "파일"],
        [[a, b] for a, b in files],
        col_widths=[28 * mm, 130 * mm],
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("한 줄로 다시", S["H2"]))
    story.extend(bullets([
        "밖을 지탱하는 것은 데이터가 아니라 가정이다. 식만 넣으면 답이 아니다.",
        "PP-X는 validation-approved prior-residual framework다.",
        "동일예산 retrospective benchmark 8/9, p=.0391; DS03 prospective predictive-superiority FAIL.",
        "CCMR는 executor only, CRT/GCIE는 rejected, prior reject 시 fallback/abstention.",
        "PAE는 future program. 만능 SOTA를 주장하지 않는다.",
    ], S["BulletKo"]))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(
        "브리핑 덱: pp_pae_total/output/PP_Research_Detailed_v2.pptx<br/>"
        "본 공부 PDF: pp_pae_total/output/PP_PPX_Study_Detailed.pdf",
        S["Small"],
    ))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="PP-X Study — Assumption-Aware Extrapolation",
        author="박진서 / SPS Lab",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("Saved", OUT)


if __name__ == "__main__":
    build()
