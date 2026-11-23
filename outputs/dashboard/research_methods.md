# Research dashboard — methods and limitations

Built UTC: 2026-11-23T19:45:11.037063+00:00

## Sources
- World Bank Bangladesh secondary education indicators, from `data/raw/worldbank_bgd_secondary.csv`, retrieved by Phase 1 API script; exact source URLs and retrieval dates reside in the source CSV.
- Country-level audit: `outputs/worldbank_data_quality.json`; trends: `outputs/worldbank_trends.json`.
- Teacher survey: Phase 4 *aggregate diagnostics*, status **synthetic**, n=120. This is **NOT VALIDATED**.

## Processing
- Present all valid observed years, with discontinuities at missing calendar years; no interpolation or imputation.
- Relative change and absolute change describe first vs last **observed** year, not fitted trends.
- Pupil–teacher ratio requires same-year pupil and teacher counts and is not class size.
- Survey scales have four ordinal 1–5 items each; current omega is an exploratory one-factor Pearson-based estimate, not ordinal omega.
- Data classes are displayed separately; no merges, correlation across ecological and individual records, or causal claims.

## Limitations and validity safeguards
- World Bank indicators do not operationalize philosophy or digital literacy, and do not alone establish educational equity.
- Synthetic results are software demonstrations, not empirical psychological evidence.
- A field label alone does not prove informed consent, ethics approval, representativeness, or measurement validity.
- Teacher-level content validity, response processes, factor structure, invariance and independent validation remain future research tasks.
- No participant-level survey rows should be committed to a public GitHub repository.
