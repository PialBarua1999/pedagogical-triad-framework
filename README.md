# The Pedagogical Triad Framework
### Integrating Educational Philosophy, Teachers' Digital Literacy, and Educational Equity in Secondary Education in Bangladesh

[![Python 3.15](https://img.shields.io/badge/Python-3.15.2-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3152/) ![Dependencies](https://img.shields.io/badge/runtime_dependencies-none-157f3b) ![Status](https://img.shields.io/badge/status-research_prototype-cc8a13) ![Ethics](https://img.shields.io/badge/data-synthetic_demo_only-8a3dbf)

> **Research integrity first:** This repository separates (a) verifiable public country-level indicators, (b) wholly **synthetic** survey examples, and (c) future ethics-approved field observations. Its example findings are **not empirical observations about teachers in Bangladesh**.

## Purpose and contribution

This open, reproducible research prototype explores a *proposed* three-construct conceptual framework for Bangladesh's secondary education system. It combines a source-audited national indicator retrieval system with a small local survey analysis pipeline. It is designed to support later instrument validation and educational/developmental-psychology research, not to diagnose educators, assess children clinically or claim nationally representative effects.

**Main research question:** How are teachers' philosophical orientations, pedagogical digital literacy and inclusive practice perceptions associated, accounting for school context and equity constraints?

**RQs:** (RQ1) What conceptual and policy links connect the triad? (RQ2) Can context-specific teacher instruments be developed and psychometrically validated? (RQ3) After ethical field collection, what associations remain after adjustment for school characteristics? (RQ4) How do access barriers shape teachers' perceived capacity to teach inclusively?

## Run in Visual Studio Code (Windows 10/11)

Requirements: Python **3.15.2**, VS Code, Microsoft Python extension, internet **only for optional WDI download**. No pip packages required.

```powershell
# Open this directory in VS Code and select Python 3.15.2 interpreter.
py -3.15 --version
py -3.15 run.py validate
py -3.15 run.py analyze
py -3.15 -m unittest discover -s tests -v
py -3.15 run.py fetch-worldbank
```

If `py -3.15` is not recognized, use `python` with your selected Python 3.15.2 interpreter:

```powershell
python --version
python run.py analyze
python -m unittest discover -s tests -v
```

Then open **`outputs/triad_report.html`** in your browser. JSON result: `outputs/triad_summary.json`. World Bank CSV (if API is reachable): `data/raw/worldbank_bgd_secondary.csv`. API failures are recorded in `data/raw/fetch_log.json`; the program never substitutes fake values.

> No dependency installation is required; avoid blindly adding Python 3.15-incompatible third-party packages. The code targets the 3.15 standard library. It has been tested in the build environment (the build host may use a different minor Python version); 3.15.2-specific execution should be verified locally.

## Repository map

```text
pedagogical-triad-framework/
├── README.md                  # You are here
├── run.py                     # VS Code-friendly CLI
├── src/triad/                 # Validation, scoring, reporting, WDI ingestion
├── data/demo/                 # 120 clearly labeled synthetic teacher records
├── data/teacher_survey_template.csv
├── data/raw/                  # Downloaded WDI and PRIVATE field inputs (gitignored)
├── outputs/                   # Reports (gitignored)
├── docs/METHODOLOGY.md        # Draft instrument, psychometrics and ethics
├── docs/DATA_SOURCES.csv      # Source provenance catalogue
├── docs/GITHUB_GUIDE.md       # GitHub publishing guide
├── tests/                     # Offline automatic validation tests
├── .github/workflows/         # Standard-library CI
└── .vscode/                   # VS Code task
```

## Use authentic survey observations responsibly

1. Get institutional ethics approval and school consent first. Confirm copyright and permitted reuse for external materials.
2. Copy the CSV **template** to a private folder **outside this repository**; do not put identifiable field data in a public Git repository.
3. Enter 12 item responses (integer 1–5); assign pseudonymous `response_id`, `division`, `setting`, `school_type`, and `data_status=field_unverified` or `field_verified` **only after documented verification**.
4. Run: `python run.py analyze --input "C:\private_research\teacher_survey.csv" --output "C:\private_research\results"`.
5. The code rejects missing, noninteger, out-of-range, duplicate and mixed-status records. It does **not** certify sampling quality, content validity, consent, representativeness or reliability of a survey design.

### Draft item map

| Scale | Item codes | Interpretation |
|---|---|---|
| Educational philosophy | ph1–ph4 | reflective, learner-centred instructional orientation (draft) |
| Pedagogical digital literacy | dl1–dl4 | critical instructional technology judgments (draft) |
| Inclusive educational practice | eq1–eq4 | self-reported inclusive action (draft) |

Each scale is the arithmetic mean of four 5-point items. Data are strictly **provisional** until the items are culturally reviewed, translated, piloted and psychometrically validated. See [methodology](docs/METHODOLOGY.md).

## Data provenance

| Dataset type | Current handling | What it may substantiate |
|---|---|---|
| World Bank WDI: BGD secondary enrolment, teacher counts and female teacher share | Actual values fetched at runtime with original indicator ID, year, URL, UTC retrieval timestamp | Country-level descriptive trends only |
| BANBEIS education statistics and ICT training research | Source catalogued for literature review/manual extraction | Bangladesh secondary-school context |
| NCTB, NAEM, MoE, IER, BRAC IED, BOU | Source discovery, conceptual/policy triangulation | Curriculum, teacher education, policy and theory |
| BBS, UNICEF, UNESCO, OECD | Contextual and external comparisons with explicit limitations | Equity and benchmark narratives |
| DPE primary National Student Assessment | Primary-level comparator **only** | Never treated as secondary outcomes |
| Kaggle, UCI, Google Dataset Search | Search directories; no automatic import | Not evidence until independently verified |
| Synthetic demo CSV | Generated expressly to run and test this software | **No real-world conclusion whatsoever** |

Detailed catalog: [`docs/DATA_SOURCES.csv`](docs/DATA_SOURCES.csv).

**Important:** None of the public sources above are automatically interpreted as measurements of all three teacher-level constructs. A spurious merge between public national aggregates and individual teachers would risk ecological fallacy. This repository intentionally does **not** do it.

## Methods and limitations

Present outputs: scale means, standard deviations, Cronbach's alpha (descriptive), Pearson correlations and subgroup summaries. All demo values are manufactured. No confidence intervals, significance testing, factor analysis, causal claims, weighted national estimates or survey-based behavioral conclusions are implemented. Alpha may be undefined when total-score variance is zero; subgroup means with small `n` are shown for illustration only and not suitable for comparative inference.

Proposed complete research methodology includes ethics review, pilot with cognitive interviews, expert content-validity screening, psychometric assessment, school-stratified sampling, multilevel modeling where warranted, and supplementary interviews/observations. See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Reproducibility and transparency

- **No fabricated published research data.** Missing API observations are skipped, not invented or interpolated.
- **No personal identifiers.** Never commit student or teacher identity, school contact details, raw consent forms or passwords.
- **No diagnostic usage.** Educational/developmental psychology constructs are studied as exploratory practice orientations, not disorders or performance verdicts.
- **No implicit institutional endorsement.** Referencing BANBEIS, the Ministry of Education, NAEM, universities, NGOs or WDI does not signify affiliation, support or approval.
- **No presumed reuse license.** Third-party tables and survey instruments retain original ownership and rights; verify each license before redistributing. This repository code is MIT-licensed; external data are not.

## Citation and scholarly attribution

If building on the framework, cite the repository version/commit and each **original data provider and report edition**; a citation to a search directory is not a data citation. Add an author, ORCID, institution (only if genuine), and final research publication DOI after these are confirmed. Suggested conceptual starting points: UNESCO ICT Competency Framework for Teachers (2018), European Commission DigCompEdu (2017), SDG 4 education equity metadata, and relevant Bangladesh national reports. These are reading leads, not falsely claimed adopted validated instruments.

## Contributing

Contributions for transparent Bangla instrument adaptation, code review, accurate official statistics and reproducibility tests are welcome. Propose a documented change with verifiable citations, consent/licensing checks and a corresponding test. **Never submit private teacher/student data in issues or pull requests.**

## License

MIT for code and original documentation. Public datasets and external documents are **not** relicensed by this repository. See [LICENSE](LICENSE).
