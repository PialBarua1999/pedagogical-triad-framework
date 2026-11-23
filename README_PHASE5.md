# Phase 5 — Integrated Research Dashboard

**The Pedagogical Triad Framework: Integrating Educational Philosophy, Teachers’ Digital Literacy, and Educational Equity in Secondary Education in Bangladesh**

**Status:** Research-software prototype (not a validated psychological instrument). **Runtime:** Python 3.15-compatible syntax; Python standard library only. **Design:** Responsive standalone HTML, entirely offline, with inline SVG (no CDN, tracking scripts or API keys).

## Scope and scientific safeguards

This package visualizes four **real national-level World Bank** education indicators separately from **teacher-survey psychometric diagnostics**. The supplied demonstration survey is **synthetic**. The two sources are not pooled. The dashboard exports only statistical aggregates from the psychometric report, **never respondent-level survey records**. National indicators are contextual statistics, not measurements of individual educational philosophy, teacher digital literacy, or educational equity; correlations do not demonstrate causality.

The Phase 4 omega is a *one-factor Pearson-based exploratory approximation*, and its EFA is preliminary. No synthetic reliability coefficient, HTMT-like measure, or factor loading establishes instrument validity. If `dataset_status` is `field`, the dashboard prominently warns that provenance and ethical approval have not been independently verified.

## Install into an existing repository (Git Bash + VS Code)

Copy the following files from the Phase 5 ZIP to the **existing repository root**, beside `run.py`, preserving subfolders:

```text
dashboard.py
README_PHASE5.md
docs/DASHBOARD_RESEARCH_PROTOCOL.md
tests/test_dashboard.py
```

**Do not nest the add-on folder in the project.** Merge `docs/` and `tests/`, never overwrite earlier material. The dashboard expects these previously generated files:

```text
data/raw/worldbank_bgd_secondary.csv
outputs/worldbank_data_quality.json
outputs/worldbank_trends.json
outputs/pupil_teacher_ratio.csv
outputs/psychometric_diagnostics.json
```

If any are missing or stale, from repository root run:

```bash
py -3.15 run.py fetch-worldbank
py -3.15 data_quality.py
py -3.15 trend_analysis.py
py -3.15 psychometric_analysis.py --input data/demo/synthetic_teacher_survey.csv --output outputs/psychometric_diagnostics.json
```

The World Bank API fetch needs internet; **building the dashboard does not**. Your previously downloaded and audited datasets can be used without refetching.

### Build the dashboard

```bash
py -3.15 dashboard.py build
```

Open its home page in Windows using Git Bash:

```bash
explorer.exe "$(cygpath -w "$PWD/outputs/dashboard/index.html")"
```

Alternatively open `outputs/dashboard/index.html` through File Explorer. No web server or installation required.

### Run all tests

```bash
py -3.15 -m unittest discover -s tests -v
```

Five additional Phase 5 tests are included. In a repository with the previous 16 tests, expect **21 tests** (unless other changes have been made).

## Research report exports

All saved under `outputs/dashboard/` and available as local links inside the dashboard:

- `index.html` — standalone responsive HTML dashboard with SVG trend charts
- `worldbank_indicator_summary.csv` — first/last observations, coverage, count, gaps
- `research_summary.json` — provenance & aggregated research summary
- `research_methods.md` — study methods, definitions, caveats and limitations
- `worldbank_data_quality.json` — copy of national data audit
- `worldbank_trends.json` — copy of national trend analysis
- `pupil_teacher_ratio.csv` — copy of same-year descriptive ratio
- `psychometric_diagnostics.json` — copy of aggregate-only psychometric report

**Important:** Download links in `index.html` may show a file preview on certain browsers opened via `file://`; use Save As if needed. The exports are deliberately static snapshots; rerun `dashboard.py build` after updating data. No guessed data points, estimates for missing years, or respondent-level exports are created.

## Data ethics & GitHub

The existing project may ignore `outputs/` and `data/raw/`; keep that protection. Do **not** commit any identifiable teacher/student data or raw field responses. Publish only vetted, anonymized aggregate results under research approval when appropriate. If sharing generated dashboards, remove sensitive/inappropriate small-group results and add documented provenance and clear synthetic labels.

Stage **only source files**:

```bash
git add dashboard.py README_PHASE5.md docs/DASHBOARD_RESEARCH_PROTOCOL.md tests/test_dashboard.py
git commit -m "feat: add Phase 5 evidence-aware research dashboard"
git push origin main
```

Do not use `git add .` if private surveys or downloaded archives are in the repository.

## Troubleshooting

- `can't open file dashboard.py`: check that `dashboard.py` is beside `run.py` (`ls -l dashboard.py`).
- `Missing ...`: regenerate prior reports, then rerun the dashboard build.
- `Stale trend report`: run `py -3.15 trend_analysis.py` to regenerate matching audit/trend reports.
- `World Bank audit record count differs`: run `py -3.15 data_quality.py` against the matching source CSV.
- `NOT VALIDATED`: intentional research-integrity check; do not remove or misrepresent it.
- Browser not opening: double-click `outputs/dashboard/index.html` in Explorer.

## Limitations and roadmap

This is a descriptive dashboard. It does not provide ordinal CFA, longitudinal statistical inference, psychometric measurement invariance, ethics approval, or causal estimates. Future research needs expert review, cognitive interviews, pilot and field recruitment, documented data governance, independent validation and appropriate CFA before making instrument claims.
