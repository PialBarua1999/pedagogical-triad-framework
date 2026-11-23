# Phase 5 — Dashboard Research and Publication Protocol

## Evidence strata

1. **World Bank BGD aggregate indicators:** real public national statistics. Fetch dates and indicator endpoints are recorded in the downloaded CSV. Incompleteness across years is a property of the retrieved series and does not imply zero educational activity.
2. **Synthetic teacher demonstration:** 120 computer-generated item-level responses are for coding checks and UI demonstration only. Never interpret simulated correlations, factor structure or reliability as teacher characteristics.
3. **Future field data:** teacher-survey ethics approval, explicit informed consent, sampling documentation, secure access controls and formal psychometric validation must precede substantive claims.

## Interpretation guardrails

- Gross secondary enrolment is not net enrolment; a GER can exceed 100% in principle.
- Pupil-to-teacher ratio is same-year pupil count divided by same-year teacher count, not actual class size or workload.
- Female teacher share is an indicator of workforce composition, not sufficient evidence of equal opportunity, safety or inclusion.
- An available-case trend with year gaps is descriptive; do not silently interpolate absent values or imply causal effects.
- The Phase 4 software uses Pearson covariance/correlation with ordinal responses. Cronbach's alpha and one-factor approximate omega have assumptions and do not prove unidimensionality or validity.
- Exploratory HTMT-like ratios and principal-axis factoring are not substitutes for independent ordinal CFA, model fit assessment or invariance testing.

## Quality gates for public output

- Re-run data quality and trend scripts whenever the raw World Bank CSV changes; dashboard refuses inconsistent record counts/coverage.
- Preserve data status labels, source attributions, definitions, timestamps and caveats in published visualizations.
- Never publish identifiable respondent-level data or small-group summaries that facilitate reidentification.
- Review data confidentiality, consent language, legal/ethical permissions and institutional repository policies before publishing field results.
- Add a reproducible release tag and research methods note to any publicly shared dashboard snapshot.

## Recommended advanced analysis (not implemented here)

Pre-register hypotheses; document sampling/power strategy; content validity review; translation/back-translation; cognitive interviews; pilot testing; ordinal reliability with uncertainty; exploratory/confirmatory factor analysis on independent groups, fit indices, discriminant/convergent evidence, invariance where justified, and bias/sensitivity analyses.
