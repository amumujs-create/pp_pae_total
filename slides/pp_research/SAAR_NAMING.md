# 명칭 대응: SAAR ↔ PP-X core

> 이 파일명은 참조 안정성을 위해 유지한다. 정식 paper-main 명칭은 **PP-X**이며,
> canonical 규칙은 `PPX_NAMING.md`에 있다.

**역사적 이름:** Support-Aware Affine–Residual Network (**SAAR**)

**현재 의미:**
SAAR는 관측 support를 고려해 동결 affine 추세 위에 제한 residual을 더하는
**역사적 alias / core architecture**다. 최종 PP-X 전체, paper main, 또는 모든 executor의
동의어가 아니다.

과거 문서의 `adaptive dual-scale PP`, `dual-scale BQ-PP`, `final adaptive dual-scale PP`
표기는 해당 실험 행과 artifact를 가리키는 역사적 label로 보존한다. 이를 소급해 PP-X로
바꾸지 않는다.

**역사적 core 식:**

\[
\hat y = m\,\operatorname{softplus}\big[\ell(z)+c_\theta(z)\big]
\]

\[
c_\theta(z)=w(z)\,B_L\tanh r_\theta(z)
+[1-w(z)]\,B_H\tanh\!\left(\frac{r_\theta(z)}{B_H}\right)
\]

**경계 모듈:** EOL health 경계가 관측될 때의 quotient 확장은 과거 artifact에서
**BQ-SAAR** 또는 **BQ-PP**로 기록될 수 있다.

**쓰지 말 것:**
- “SAAR = 논문” 또는 “SAAR = 최종 PP-X 전체”
- “CCMR = 메인” (CCMR v2.2는 trajectory-domain executor only)
- SAAR를 PAE와 혼동하는 표현 (PAE는 future program)
- “prior-free” (PP-X는 validation-approved prior-residual framework)

**원문 수치 표기:**  
`UNIFIED_SUPPORT_GATED_PP_RESULTS_KO.md`의 **최종 adaptive dual-scale PP** 행은
SAAR core의 역사적 결과다. 9-setting portfolio는 retrospective concept-aligned evidence이며
최종 PP-X의 prospective superiority 증거로 읽지 않는다.

**최종 경계:** PP-X가 top-level이다. CCMR v2.2는 trajectory-domain executor only이고,
CRT/GCIE는 rejected이며 Algorithm 1에 포함되지 않는다. DS03는 route-selection PASS지만
frozen PP-X fallback R² 0.8818 < Engression 0.9013이므로 predictive-superiority FAIL이다.
prior reject 시 fallback 또는 abstention으로 간다.

갱신일: 2026-09-11
