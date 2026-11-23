# Phase 4 Psychometric Evidence Plan — pre-registration draft

**Working title:** The Pedagogical Triad Framework: Integrating Educational Philosophy, Teachers' Digital Literacy, and Educational Equity in Secondary Education in Bangladesh.

## 1. What this project does — and does not — measure

The three hypothesised constructs are (a) *reflective/dialogic learner-centred teaching orientation* (`ph1–ph4`), (b) *self-reported digital pedagogical practices* (`dl1–dl4`), and (c) *self-reported inclusive/equity-sensitive practices* (`eq1–eq4`). The four items per block are project-authored and preliminary. They do not measure a teacher's full philosophy, objectively tested digital competence, educational equity outcomes, developmental diagnosis or school effectiveness.

All 12 responses are ordered Likert categories (1–5). The Phase 4 script applies **Pearson/covariance diagnostics for demonstration and initial screening**; ordinal/polychoric factor models are recommended for final empirical interpretation. The script assumes one factor in each four-item reliability block and three in the pooled 12-item EFA; neither assumption is empirically confirmed.

## 2. Ethical and linguistic safeguards (before recruitment)

- Secure ethics approval and permission from the relevant education authorities, schools and institutional review mechanisms **before recruiting anyone**.
- Obtain freely given informed consent; ensure voluntariness, withdrawal procedures, minimal burden and no impact on employment or appraisal.
- Arrange independent Bangla/English review, reconciliation, back-translation as justified, and **teacher cognitive interviews** to identify ambiguities, local terminology, social desirability and differential interpretation.
- Do not collect student information or unnecessary sensitive identifiers; protect school/participant identity. Keep consent records separate from survey responses.

## 3. Content and response-process validity

Recruit subject-matter experts across educational psychology, teacher education, digital pedagogy, equity/inclusion and measurement. Record each expert's item relevance, clarity, local appropriateness and critique. Document **item-level and scale-level CVI where appropriate**, and revisions. An expert rating is evidence to be interpreted, not a ceremonial approval or an automatic validity pass.

Conduct cognitive interviews across diverse school contexts. Preserve a versioned item history and rationale for all edits. Pre-register what was changed after the pilot rather than claiming the initial wording was validated.

## 4. Sampling and design

Use a defensible sampling frame and record school-level clusters, school setting (urban/rural), division, school type, invitation counts, participation, exclusions and missingness. National representativeness requires probability-based or otherwise justified sampling, not a large convenience sample. The example pilot size of roughly 30–50 is for feasibility only; a separate, substantially larger sample will normally be needed for stable factor models. Justify effective sample size considering design effects from school clustering, number of factors, communality, precision and missingness. Plan EFA and independent-sample CFA where feasible. No universal sample-size threshold certifies validity.

## 5. Pre-analysis and measurement reporting

1. Verify response IDs, consent/provenance and segregation of `synthetic`, `field_unverified`, `field_verified`; do not rely on the `field_verified` label as independent proof of approval.
2. Describe each item: ordered-category frequencies, ceiling/floor effects, item missingness, zero variance, nonresponse and selection processes. Explain exclusions and disclose denominators.
3. Examine corrected item-total correlations, Cronbach's alpha as a supplement, McDonald's omega with justified ordinal factor model and uncertainty (e.g. bootstrap confidence intervals where defensible). Reliability is score- and population-dependent.
4. Perform **ordinal/polychoric EFA**, selecting the number of factors using parallel analysis, theory and interpretability; oblique rotation is often more appropriate than varimax when the constructs are correlated. Evaluate weak loadings and cross-loadings without mechanically deleting substantive content.
5. Confirm the proposed 3-factor measurement model on a held-out sample with **CFA for ordered categorical data** using an appropriate robust estimator (e.g. WLSMV), reporting parameter estimates, standard errors, residuals and fit indices with transparent caveats. Do not assert CFA has been performed by this project.
6. Examine convergent and discriminant evidence, including theoretical relationships, external criteria and carefully interpreted HTMT. A low HTMT alone does not validate constructs, and no universal threshold should replace theory.
7. If adequately powered, assess **measurement invariance** across relevant school settings and teacher subgroups; avoid evaluating tiny groups that risk participant disclosure.
8. Account for teachers nested within schools using cluster-robust or hierarchical approaches if analyzing explanatory relationships. Analyze self-report/common-method bias through design and triangulation; neither structural correlations nor the national World Bank series establish causality.

## 6. Reporting standards

Report uncertainty, exclusions, data provenance, preregistered versus exploratory analyses, recruitment limitations, item changes, missing data methods and substantive limitations. **Avoid made-up p-values and unverified psychometric results.** Avoid claims that World Bank country-level education statistics establish teacher-level psychological correlations.

## 7. Public repo privacy policy

Never upload raw teacher-level responses, personal identifiers, precise school IDs, private consent forms or protected participant metadata. Keep field data in access-controlled storage and use synthetic examples for public continuous integration. Examine generated reports for accidental disclosure prior to publication.

## Reference orientation

- AERA, APA, NCME (2014). *Standards for Educational and Psychological Testing.* https://www.testingstandards.net/ (foundational validity framework)
- UNESCO (2018). *ICT Competency Framework for Teachers*, version 3. https://www.unesco.org/en/articles/unesco-ict-competency-framework-teachers
- Redecker (2017). *European Framework for the Digital Competence of Educators: DigCompEdu.* https://doi.org/10.2760/159770

These sources inform methodology only. **No endorsement or pre-existing scale validation is claimed.**
