# PP 공부용 부록 색인

발표 고정본(단일): `pp_pae_total/output/PP_Research_Detailed_v2.pptx`  
갱신: 2026-09 — PP-X paper-main 경계, 동일예산 prospective, DS03·최종 모델 판정 추가
※ `ppt/pp/` · `pp-extrapolation/slides/`에 PPTX 복사본을 두지 않음

## 명칭

- **PP-X** = paper-main top-level framework
- **SAAR** = historical alias / core architecture
- **CCMR v2.2** = trajectory-domain executor only
- **CRT / GCIE** = rejected; Algorithm 1 미포함
- **PAE** = future program; paper main이 아님
- 상세: `PPX_NAMING.md` · `SAAR_NAMING.md`

## 권장 공부 순서

1. `ppt/외삽자료/extrapolation-papers/외삽_문헌조사_통합.pptx`
2. PPT 본문 A–B (문제·PP-X prior-residual core)
3. PPT 본문 C: retrospective 9-setting portfolio → 동일예산 prospective → DS03 경계
4. PPT 본문 D: 최종 PP-X / CCMR / CRT / GCIE 경계 · PAE future program · 요약
5. 아래 md 원문

## 부록에서 보는 것

| 슬라이드 주제 | 내용 |
|---|---|
| PP-X 연구 바운더리 | unit-disjoint out-of-support RUL / validation-approved prior-residual |
| 외삽 범위 규칙 | 계약→unit분리→hull-out→val-only |
| 조건 적합도 | 6항 검사 · Pass/Weak/Fail |
| 9-setting portfolio | retrospective concept-aligned evidence; 확증 cohort 아님 |
| 동일예산 prospective | 9 settings×8 baselines×30 candidates×5 refit; PP-X 8/9, p=.0391 |
| DS03 | frozen PP-X fallback .8818 < Engression .9013; route PASS / superiority FAIL |
| 최종 경계 | PP-X top-level · CCMR executor only · CRT/GCIE rejected |
| Zn-ion 경로 | BQ 실패 → RBF-regime → shrinkage/refit (개발) |
| 교차 도메인 | XJTU 0.257 개발 · FEMTO 판정 보류 · Milling 감사 |

## 핵심 원문 (pp-extrapolation/)

| 주제 | 파일 |
|---|---|
| 역사적 SAAR core 결과 | `UNIFIED_DUAL_SCALE_PP_IMPROVEMENT_KO.md` |
| PP-X canonical naming | `slides/pp_research/PPX_NAMING.md` |
| 정보·주장 한계 | `PP_INFORMATION_LIMITS_AND_CLAIMS_KO.md` |
| Zn 경로·진단 | `ZNION_*`, `PP_NEXT_MODEL_HANDOFF_DIAGNOSIS_KO.md` |
| 전체 개선 인계 | `PP_TOTAL_IMPROVEMENT_HANDOFF_KO.md` |
| 교차 복구 | `STRUCTURAL_RECOVERY_V3_RESULTS_KO.md`, `MODELING_IMPROVEMENT_REAUDIT_KO.md` |
| 투고 권리 | `PP_FIRST_PUBLICATION_CLAIMS_KO.md` |
| 프로그램 | `ASSUMPTION_AWARE_EXTRAPOLATION_PROGRAM_KO.md` |

## 실패·미접촉·한계

- Zn untouched BQ 실패 → 개발 개선과 확증을 분리할 것
- FEMTO: 잘못된 채널/캐시 → 교정 후에도 PP 채택 실패 (우월 실패로 단정 금지)
- XJTU 0.257: post-test 개발, 독립 확증 아님
- 보편 LODO pre-gate 실패
- CRT DS03 .8851 < Engression .9013
- GCIE .8850, nested .8727로 rejected
- prior reject 시 fallback/abstention; CRT/GCIE는 Algorithm 1 미포함
- N-CMAPSS 0.937은 portfolio split이며 DS03와 다른 비교

## 문헌 폴더

- `ppt/외삽자료/extrapolation-papers/INDEX.md`
