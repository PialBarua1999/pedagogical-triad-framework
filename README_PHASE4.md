# Phase 4 — Psychometric Diagnostics (Research Prototype)

**Pedagogical Triad Framework | Bangladesh Secondary Education | Python 3.15-compatible syntax**

This optional add-on uses the exact Phase 3 survey schema: `response_id,division,setting,school_type,data_status,ph1..ph4,dl1..dl4,eq1..eq4`. It requires **only the Python standard library**. It does **not** change `run.py` or your existing Phase 1–3 code.

> **Academic integrity:** These diagnostics are **not a validated psychological instrument**, a clinical assessment, or a test of student outcomes. Results from the bundled synthetic demonstration must never be presented as observed results from Bangladeshi teachers. Synthetic and field data cannot be pooled.

## Install (Git Bash and VS Code)

Extract this ZIP and copy the following into your *existing project root* (same folder as `run.py`):

```
psychometric_analysis.py
README_PHASE4.md
docs/PSYCHOMETRIC_VALIDATION_PROTOCOL.md
tests/test_psychometric_analysis.py
```

Do **not** replace your existing `tests/` or `docs/` directories—merge them. Your existing `data/demo/synthetic_teacher_survey.csv` remains in place.

From your project root, run:

```bash
py -3.15 psychometric_analysis.py --input data/demo/synthetic_teacher_survey.csv --output outputs/psychometric_diagnostics.json
py -3.15 -m json.tool outputs/psychometric_diagnostics.json
py -3.15 -m unittest discover -s tests -v
```

The first command creates a **synthetic demonstration report**, not field validation. The existing tests should still run; this add-on adds 6 more tests. On a repository that previously had 10 tests, expect 16 total if the installed files match the supplied versions.

## Outputs and statistical interpretation

- **Cronbach's alpha**: conventional covariance-based internal consistency, calculated separately for the 4 items in each of the 3 proposed subscales. Alpha can be negative and does not establish unidimensionality.
- **One-factor omega total (approximation)**: computed using a Pearson-correlation principal-axis one-factor model per subscale. This is a **provisional standardized-item estimate**, not ordinal omega, and has **no confidence interval**.
- **Corrected item-total correlations**: each item correlated with the sum of the other three items in the same subscale.
- **Scale correlations and HTMT-like diagnostics**: association and exploratory discriminant-evidence indicators, **not** standalone proof of construct validity. HTMT here uses absolute Pearson correlations, not polychoric correlations.
- **Exploratory factor analysis**: unrotated principal-axis extraction of **three** common factors, then *orthogonal varimax* for descriptive loadings. Factors are **assumed**, not selected through parallel analysis. Correlated psychological constructs may make orthogonal rotation inappropriate. No inferential fit index or uncertainty estimate is provided. Calculated only when there are at least 5 cases per item and all items have nonzero variance.
- **Data safeguards**: all item responses must be 1–5 integers; duplicate response IDs, missing context columns, and mixed `data_status` cause explicit failure. Report contains **aggregates**, not individual data.

## Fieldwork and validity decision

Read `docs/PSYCHOMETRIC_VALIDATION_PROTOCOL.md` **before fieldwork**. For credible journal-grade evidence, obtain approvals and strengthen the analysis with a documented sampling plan, expert review, cognitive interviews, ordinal factor analysis, appropriate sample size, independent CFA, robust model fit and group invariance where justified. Pure-Python calculations here are preliminary diagnostics; they are not substitutes for those analyses.

Keep **all identifiable and participant-level field data out of this public GitHub repository**. Prefer encrypted institutional storage and local analysis. If you analyze field data, place the input file outside the repository and write reports to a private folder. See data governance in the protocol.

## GitHub publication

```bash
git add psychometric_analysis.py README_PHASE4.md docs/PSYCHOMETRIC_VALIDATION_PROTOCOL.md tests/test_psychometric_analysis.py
git commit -m "feat: add Phase 4 exploratory psychometric diagnostics"
git push origin main
```

Keep generated exploratory reports local unless labelled *synthetic demonstration*, audited for disclosure risks and explicitly suitable for public release. Avoid `git add .` when fieldwork files exist.
