# Question Plan & Acceptance Checklist

n = number of members (2 or 3); total number of questions = 2 × n.
Each member owns two questions. At least one question is answered with ML.

| ID | Owner | Specific question | Stakeholder / decision | Non-ML criteria D1–D6 or ML | Status |
|---|---|---|---|---|---|
| Q1 | [Name] | [TODO] | [TODO] | [D?, D?] | Proposed |
| Q2 | [Name] | [TODO] | [TODO] | [D?, D?] | Proposed |
| Q3 | [Name] | [TODO] | [TODO] | [D?, D?] | Proposed |
| Q4 | [Name] | [TODO] | [TODO] | [D?, D?] | Proposed |
<!-- Add Q5 and Q6 when n=3 -->

## Verify coverage
- [ ] At least 1 ML question.
- [ ] Each non-ML question meets >=2 relevant D criteria.
- [ ] Non-ML questions together cover >=4 of D1–D6.
- [ ] Each question explains motivation, stakeholder and informed decision.
- [ ] Each question includes preprocessing description, row-count checks, method rationale, >=2 labelled plots, quantified answer and limitations.

## D1–D6 overview
- D1: merge tables / sources and verify join cardinality, missing keys and row counts.
- D2: reshape / resample / rolling / lag / time comparison.
- D3: justified derived variables.
- D4: check confounders using subgroups or adjustments.
- D5: uncertainty (confidence intervals, tests, effect sizes).
- D6: robustness to reasonable analytical assumptions.

## ML checklist
- [ ] Explain prediction task, user and prediction-time features; list excluded leakage features.
- [ ] Split correctly (time-based or group-based when required).
- [ ] Compare trivial baseline with >=2 ML models; preprocess within sklearn Pipeline.
- [ ] Tune using cross-validation on train only; hold out test until final evaluation.
- [ ] Justify metrics; analyze failure cases; interpret model; answer question, not only report score.
