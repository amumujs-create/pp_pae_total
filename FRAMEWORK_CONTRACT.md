# Framework contract

## Inputs

Each task declares an observation contract:

- available covariates and their temporal order;
- target and boundary labels that are available at training and deployment time;
- unit, domain, and operating-condition metadata;
- known qualitative constraints such as sign or monotonic direction;
- known quantitative laws, if any;
- definition of extrapolation support and the target deployment shift.

No component may use a test label, future unavailable state, or a prior inferred from the held-out target labels.

## Prior ladder

| Level | Prior | Executor | Required evidence |
|---|---|---|---|
| 0 | None | prior-off neural predictor plus UQ/abstention | no defensible structure |
| 1 | Boundary, range, history, support distance | PP | observable endpoint/range/history and a declared extrapolation axis |
| 2 | Qualitative structure | constrained model | defensible direction/order/decomposition |
| 3 | Quantitative equation or dynamics | equation/physics residual hybrid | externally justified law and observable quantities |

## Output contract

Every prediction returns:

- point prediction;
- selected prior level and executor;
- support-distance or applicability signal;
- uncertainty or validation-derived risk signal;
- predict/abstain decision when the assurance policy is enabled.

## Falsification tests

The integrated framework succeeds only if it can show all of the following:

1. A stronger prior helps when it is correct.
2. A wrong prior can harm performance.
3. PAE detects insufficient evidence and selects a weaker or prior-off route often enough to limit that harm.
4. The assurance signal is associated with error or selective risk on untouched units/conditions.
