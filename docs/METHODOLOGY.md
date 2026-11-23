# Research protocol: Pedagogical Triad Framework

## Proposed design
Sequential explanatory mixed methods: (1) review published national indicators and document policy context; (2) secure ethics approval, pilot and field-test teacher-level survey; (3) purposive interviews/classroom observation to contextualize the quantitative findings. A cross-sectional survey supports descriptive association **not** causal inference.

## Constructs and conceptual anchors
- **Educational philosophy**: pragmatic/constructivist, learner-centred, critical-reflective classroom orientations. Self-report does not measure philosophical sophistication alone.
- **Digital literacy**: pedagogical integration and judgment, not hardware ownership or an unvalidated ability score. Align instrument development with UNESCO ICT Competency Framework for Teachers and DigCompEdu after permission and contextual adaptation.
- **Educational equity**: teachers' self-reported inclusive practices, accessibility, fair learning opportunities and responsive support. Must distinguish this *proxy* from objective student equity outcomes.

## Minimal draft item bank (NOT validated)
Administer 1 = strongly disagree to 5 = strongly agree, after expert review and Bangla translation/back translation.

| Code | Draft English item |
|---|---|
| ph1 | I connect lessons with learners' lived experiences. |
| ph2 | I invite learners to explain their reasoning. |
| ph3 | I adapt teaching in response to learner feedback. |
| ph4 | I reflect on how my beliefs influence instruction. |
| dl1 | I evaluate the reliability of digital teaching resources. |
| dl2 | I select digital tools based on learning goals. |
| dl3 | I support learners to use digital tools safely. |
| dl4 | I can adapt instruction when connectivity is limited. |
| eq1 | I provide multiple ways to participate in lessons. |
| eq2 | I check whose voices are missing from discussions. |
| eq3 | I adapt materials for students with differing access needs. |
| eq4 | I seek support when barriers to participation arise. |

**Instrument warning:** Draft items are original research starting points. Cronbach alpha alone does not establish construct validity. For publishable work, use cognitive interviewing, expert content validity, pilot testing, EFA/CFA on appropriately sized independent samples, measurement invariance if subgroup comparisons are claimed, and classroom/learner data where warranted.

## Sampling and ethics
Define target population and school sampling frame with BANBEIS or institutional approval. Stratify by school governance, division, and urban/rural context as feasible; document exclusions, clustering, nonresponse and weighting decisions. Recruit teachers voluntarily. Seek recognized university IRB/ethics approval and participating school permissions before collection. Avoid collecting names, exact school addresses, phone numbers, student data or identifying free text; protect confidential school codes off-repository. Store consent records separately and use encrypted storage. Never commit raw sensitive field files to GitHub.

## Data integration
- National WDI indicators are **country-year aggregates**, not teacher-level measurements.
- School-level BANBEIS tables must not be merged to individual teacher responses without approved matching keys and appropriate statistical models.
- OECD benchmarks require explicit definitions, coverage and country comparability notes; not interchangeable with Bangladesh observations.
- UCI/Kaggle/Google Dataset Search are discovery sources, not authority or proof of validity; verify original provider, methodology, rights, license and construct alignment before import.
- NAEM/B.Ed/IER/BRAC IED/BOU/NCTB provide theory, training and curriculum context where verifiable publications are located—not interchangeable datasets.
- DPE NSA is **primary** assessment, so cannot be described as observed secondary achievement.

## Quantitative plan beyond the MVP
Pre-register hypotheses, primary outcome and multiplicity rules. Include cluster-robust models or hierarchical models when school clustering is present, explicit confounder adjustment and missingness sensitivity analyses. Report confidence intervals, effect sizes and survey design limitations. Avoid treating correlation as causal evidence, ranking teachers, clinical labels, or using results for punitive appraisal.

## MVP boundaries
Current CLI calculates means, SD, alpha and Pearson r to prove data pipeline functionality on *synthetic* records. These are demo statistics, not Bangladesh empirical findings. No causal model, factor validation, hypothesis tests, or quality claims are inferred from demo outputs.
