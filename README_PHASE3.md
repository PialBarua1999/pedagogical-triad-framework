# Phase 3 add-on | Pedagogical Triad Framework

**Purpose:** Provides 12 original provisional bilingual item pairs, a Bangla/English consent template, validation roadmap, input CSV header and a zero-dependency structural audit script. **These items are not a validated instrument.** This add-on does not collect data and should not be used with teachers before ethics approval, expert review and translation checks.

## Installation into your EXISTING GitHub repository

Copy `survey_check.py`, `docs/`, `data/` and `tests/test_survey_check.py` from this add-on into your existing project root, **merging folders; do not delete existing files**. In Git Bash in repository root:

```bash
py -3.15 survey_check.py --input data/demo/synthetic_teacher_survey.csv --output outputs/survey_schema_audit.json
py -3.15 -m unittest discover -s tests -v
```

Expected on the bundled existing synthetic demo: `Records reviewed: 120; schema valid: True; errors: 0`. This expectation is based on the original repo's 120-row schema, but recheck locally. To audit later approved *private* field data, use `--input "C:/private_research/teacher_survey.csv"` and keep CSV outside the public repo. Validation only tests structure; it does not certify participant consent, reliability or validity.

**Existing compatibility:** Uses the existing codes `ph1–ph4`, `dl1–dl4`, `eq1–eq4` and input columns. The existing 120 synthetic observations were generated for older demonstration items; **do not retrospectively interpret those fabricated responses as answers to these new bilingual items**. They are for software schema tests only.

### Commit the new public files

```bash
git add survey_check.py README_PHASE3.md docs/CONSENT_FORM_BILINGUAL.md docs/MEASUREMENT_AND_VALIDATION_PLAN.md docs/QUESTIONNAIRE_BILINGUAL.md data/teacher_survey_items_bilingual.csv data/field_survey_blank_template.csv tests/test_survey_check.py
git commit -m "feat: add bilingual teacher survey and ethics-first measurement protocol"
git push origin main
```

See `docs/MEASUREMENT_AND_VALIDATION_PLAN.md` for research limits and source credits.
