# PP-X canonical naming

## 정식 정의

**PP-X**는 paper-main top-level framework다. 정당화된 prior-residual candidate를
validation evidence로 승인하고, 지원되는 executor만 선택하며, prior가 거절되면
frozen fallback 또는 abstention으로 전환한다.

권장 한 줄 표기:

> PP-X: validation-approved prior-residual framework with fallback/abstention.

최종 방법 버전은 **frozen method v1**로 표기한다. 개발 과정의 v1.0/v1.1은 역사적
mechanism/stress-test를 설명할 때만 사용하며 최종 paper method 이름으로 쓰지 않는다.

## 구성 경계

- **SAAR**: historical alias / core architecture. PP-X 전체와 동의어가 아니다.
- **CCMR v2.2**: trajectory-domain executor only. 메인 모델이 아니다.
- **CRT**: DS03 R² 0.8851로 Engression 0.9013보다 낮아 rejected.
- **GCIE**: R² 0.8850, nested 0.8727로 rejected.
- **CRT / GCIE**: Algorithm 1에 포함하지 않는다.
- **PAE**: future research program. 현재 paper main이 아니다.

## 증거 해석

- 기존 9-setting portfolio는 **retrospective concept-aligned evidence**다.
- 9/9, 양측 p=.0039는 이질적인 데이터별 strongest same-split comparison의 sign test다.
- 동일예산 retrospective benchmark:
  9 settings × 8 baselines × 30 candidates × 5 refit.
- 동일예산 결과: PP-X 8/9, 양측 p=.0391; Virkler 차이 −0.002.
- DS03: frozen PP-X fallback R² 0.8818, Engression R² 0.9013.
  route-selection PASS지만 predictive-superiority FAIL이다.
- N-CMAPSS 0.937은 기존 portfolio split 결과이며 DS03와 동일한 split/비교가 아니다.

## artifact 표기 원칙

기존 파일명과 과거 결과명은 참조 안정성과 사실 보존을 위해 rename하지 않는다.
생성 당시 SAAR, BQ-PP, adaptive dual-scale PP 등으로 기록된 artifact label은 소급해
PP-X로 바꾸지 않는다. 단, 현재 방법의 주체와 설명 문구는 PP-X로 통일한다.

저자: **박진서**

갱신일: 2026-09-11
