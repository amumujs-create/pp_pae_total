# 첫 번째 논문 검토 기록

## 현재 결정

- **첫 번째 논문 대상:** PP-X
- **상태:** 투고 전 검토 대상
- **방법 버전:** frozen method v1
- **저자:** 박진서
- **기록일:** 2026-09-11

PP-X는 현재 연구 프로그램에서 첫 번째 독립 논문으로 검토한다. 논문의 중심은
개별 신경망 부품의 최초성이 아니라, 외삽에 사용할 구조 가정을 사전에 선언하고,
검증자료가 지지하는 prior-residual executor만 승인하며, 근거가 부족하면 미리 정한
fallback을 사용하거나 예측을 보류하는 절차다.

## 검토 중인 핵심 기여

1. 외삽에 허용할 state, tail, unit, prior, fallback을 typed contract로 선언한다.
2. frozen prior 주변에서 residual의 수정 범위를 제한한다.
3. test label을 사용하지 않고 physical-unit validation evidence로 executor를 승인하거나 거절한다.
4. 승인 실패 시 실행할 fallback 또는 abstention을 배포 전에 고정한다.

논문에서는 이를 다음과 같이 제한해 표현한다.

> PP-X formalizes a reproducible procedure for declaring, learning, approving,
> and declining structural assumptions in strict regression extrapolation.

## 현재 증거

- mixed strongest same-split retrospective: 9/9, exact two-sided p=.00390625
- uniformly tuned equal-budget retrospective: 8/9, p=.0391
- DS03 prospective: route-selection PASS
- DS03 predictive superiority: FAIL
  - PP-X fallback R²=.8818
  - Engression R²=.9013

9/9 결과와 8/9 결과는 서로 다른 evidence tier이므로 하나의 검정처럼 합치지 않는다.
DS03 결과 역시 retrospective 결과와 합산하지 않는다.

## 투고 전 검토 사항

PP-X의 방법론적 기여는 논문화할 수 있으나, 아래 항목을 검토한 뒤 첫 번째 논문
투고안을 확정한다.

1. Extrapolation Validation, extrapolation-aware inference, Engression,
   prior-residual learning, selective regression과의 차이를 관련연구 표에서 명확히 한다.
2. 개별 요소의 최초성이나 universal SOTA를 주장하지 않는다.
3. 가능하면 독립 prospective cohort에서 예측 우월성을 추가 검증한다.
4. 추가 prospective 결과가 없으면 retrospective breadth와 route-selection validity로
   주장을 제한한다.
5. 비교모델의 정보 계약, 탐색예산, split, 평가 단위를 동일하게 보고한다.

## 연구 프로그램 내 위치

- **PP-X:** 첫 번째 논문 검토 대상
- **CCMR v2.2:** PP-X가 조건부로 사용할 수 있는 trajectory-domain executor
- **PAE:** prior compilation과 multi-route selection을 다루는 후속 연구
- **CRT / GCIE:** 현재 PP-X Algorithm 1에서 제외

이 문서는 연구 우선순위를 기록한 것이며, 저널 투고 확정이나 acceptance 가능성을
보장하는 문서가 아니다.
