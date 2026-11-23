"""Offline Phase 5 research dashboard. Standard library only; Python 3.15 compatible.

Run at project root: py -3.15 dashboard.py build
Real national aggregates and synthetic/field survey diagnostics are NOT pooled.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import math
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

LABELS = {
    'SE.SEC.ENRR': ('Gross secondary enrolment', '%'),
    'SE.SEC.TCHR': ('Secondary teachers', 'teachers'),
    'SE.SEC.TCHR.FE.ZS': ('Female secondary teachers', '%'),
    'SE.SEC.ENRL': ('Secondary pupils', 'pupils'),
}
SCALES = {'ph': 'Educational philosophy', 'dl': 'Teachers’ digital literacy', 'eq': 'Educational equity'}


def read_json(path: Path):
    with path.open(encoding='utf-8-sig') as f:
        return json.load(f)


def load_inputs(data_file: Path, quality_file: Path, trends_file: Path, psych_file: Path):
    """Validate input provenance/consistency; never consume participant-level survey CSV."""
    for f in (data_file, quality_file, trends_file, psych_file):
        if not f.is_file():
            raise FileNotFoundError(f'Missing {f}; run Phase 2/4 analyses first (see README_PHASE5.md).')
    quality, trends, psych = read_json(quality_file), read_json(trends_file), read_json(psych_file)
    series = defaultdict(dict)
    with data_file.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        required = {'indicator_code', 'country', 'year', 'value'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('World Bank CSV is missing required headers')
        count = 0
        for row in reader:
            code = row['indicator_code'].strip()
            if code not in LABELS or row['country'].strip() != 'Bangladesh':
                raise ValueError('Unexpected indicator or country in World Bank CSV')
            year = int(row['year'])
            value = float(row['value'])
            if not math.isfinite(value) or value < 0:
                raise ValueError('World Bank CSV contains an invalid value')
            if code == 'SE.SEC.TCHR.FE.ZS' and value > 100:
                raise ValueError('Female teacher share exceeds 100%')
            if year in series[code]:
                raise ValueError(f'Duplicate country-indicator-year: {code}/{year}')
            series[code][year] = value
            count += 1
    if count == 0 or count != quality.get('rows') or count != quality.get('valid_numeric_rows'):
        raise ValueError('World Bank audit record count differs from CSV: rerun data_quality.py')
    if quality.get('invalid_rows') or quality.get('duplicate_indicator_country_year') or quality.get('missing_cell_counts'):
        raise ValueError('World Bank quality audit reports invalid, missing, or duplicate data')
    if set(series) != set(LABELS):
        raise ValueError('One or more World Bank indicators missing')
    for code, values in series.items():
        qa = quality.get('indicators', {}).get(code, {})
        t = trends.get('indicator_trends', {}).get(code, {})
        if qa.get('records') != len(values) or t.get('records') != len(values):
            raise ValueError(f'Inconsistent indicator counts: {code}')
        if sorted(values)[0] != t.get('first_observation', {}).get('year') or sorted(values)[-1] != t.get('last_observation', {}).get('year'):
            raise ValueError(f'Stale trend report for {code}; rerun trend_analysis.py')
    if trends.get('country') != 'Bangladesh':
        raise ValueError('Trend report must refer to Bangladesh')
    status = psych.get('dataset_status')
    if status not in {'synthetic', 'field'}:
        raise ValueError('Psychometric status must be a single synthetic or field dataset')
    if psych.get('validity_decision', '').upper().find('NOT VALIDATED') < 0:
        raise ValueError('Psychometric report must prominently declare NOT VALIDATED')
    if not isinstance(psych.get('n'), int) or psych['n'] <= 0:
        raise ValueError('Invalid survey record count')
    for scale in SCALES:
        if scale not in psych.get('descriptive_reliability', {}):
            raise ValueError(f'Missing psychometric scale {scale}')
    return series, quality, trends, psych


def fmt(value, digits=2):
    return '—' if value is None else f'{value:,.{digits}f}'


def svg_line(code, observations):
    """Missing calendar years produce visible breaks; never interpolate."""
    obs = sorted(observations.items())
    width, height, left, right, top, bottom = 860, 220, 54, 17, 18, 32
    min_year, max_year = obs[0][0], obs[-1][0]
    lo = min(v for _, v in obs)
    hi = max(v for _, v in obs)
    pad = (hi - lo) * .12 or 1.0
    lo, hi = max(0, lo - pad), hi + pad
    x = lambda yr: left + (yr - min_year) / max(1, max_year - min_year) * (width - left - right)
    y = lambda val: top + (hi - val) / (hi - lo) * (height - top - bottom)
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(LABELS[code][0])} values over observed years; gaps are not joined" xmlns="http://www.w3.org/2000/svg">']
    for k in range(3):
        val = lo + k * (hi - lo) / 2
        yy = y(val)
        parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="#dce5ed" stroke-dasharray="3,5"/><text x="{left-7}" y="{yy+4:.1f}" text-anchor="end" font-size="10" fill="#526478">{html.escape(f"{val:,.0f}")}</text>')
    groups, group = [], []
    for year, val in obs:
        if group and year != group[-1][0] + 1:
            groups.append(group)
            group = []
        group.append((year, val))
    if group:
        groups.append(group)
    for g in groups:
        pts = ' '.join(f'{x(yr):.1f},{y(v):.1f}' for yr, v in g)
        if len(g) > 1:
            parts.append(f'<polyline points="{pts}" fill="none" stroke="#146b91" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>')
    for year, val in obs:
        parts.append(f'<circle cx="{x(year):.1f}" cy="{y(val):.1f}" r="3.0" fill="#146b91"><title>{year}: {val:,.3f}</title></circle>')
    parts.append(f'<text x="{left}" y="{height-7}" font-size="12" fill="#526478">{min_year}</text><text x="{width-right}" y="{height-7}" text-anchor="end" font-size="12" fill="#526478">{max_year}</text></svg>')
    return ''.join(parts)


def build_content(series, quality, trends, psych):
    status = psych['dataset_status']
    status_title = 'SYNTHETIC DEMONSTRATION' if status == 'synthetic' else 'FIELD-STATUS DATA — UNVERIFIED PROVENANCE'
    status_note = ('These are simulated teacher responses; estimates are not empirical findings.' if status == 'synthetic'
                   else 'The field label is self-reported; consent, sampling, approvals and provenance have not been independently verified.')
    cards = []
    table = []
    csv_rows = []
    for code, (label, unit) in LABELS.items():
        vals = series[code]
        start, end = min(vals), max(vals)
        qa = quality['indicators'][code]
        suffix = '%' if unit == '%' else ''
        change = vals[end] - vals[start]
        heading = html.escape(label)
        svg = svg_line(code, vals)
        cards.append(f'<section class="panel"><div class="panel-head"><h3>{heading}</h3><span class="tag real">WORLD BANK · REAL AGGREGATE</span></div><div class="stat">{fmt(vals[end])}{suffix}<small> · {end}</small></div><p class="muted">{start}: {fmt(vals[start])}{suffix} · Change: {fmt(change)} {"percentage points" if unit == "%" else unit} · {len(vals)} observed years · {len(qa["years_missing_within_range"])} gaps</p>{svg}<p class="note">Individual dots are observed records; lines stop at missing years. No imputation.</p></section>')
        table.append(f'<tr><td>{html.escape(code)}</td><td>{html.escape(label)}</td><td>{len(vals)}</td><td>{start}–{end}</td><td>{len(qa["years_missing_within_range"])}</td><td>{fmt(vals[start])}</td><td>{fmt(vals[end])}</td></tr>')
        csv_rows.append({'indicator_code':code, 'indicator':label, 'observations':len(vals), 'first_year':start, 'first_value':vals[start], 'last_year':end, 'last_value':vals[end], 'change':change, 'missing_years':len(qa['years_missing_within_range'])})
    reliab = []
    for key, label in SCALES.items():
        scale = psych['descriptive_reliability'][key]
        alpha = scale.get('cronbach_alpha')
        omega = scale.get('omega_total_one_factor_approx')
        reliab.append(f'<tr><td>{html.escape(label)}</td><td>{fmt(alpha, 3)}</td><td>{fmt(omega, 3)}</td><td>{fmt(scale.get("mean_of_person_means"), 2)}</td></tr>')
    ratio = trends.get('pupil_teacher_ratio', {})
    n_pair = ratio.get('shared_years_count')
    corr = psych.get('exploratory_construct_relationships', {})
    corrs = []
    for k, label in [('ph_dl','Philosophy ↔ Digital literacy'),('ph_eq','Philosophy ↔ Equity'),('dl_eq','Digital literacy ↔ Equity')]:
        c = corr.get(k, {})
        corrs.append(f'<tr><td>{html.escape(label)}</td><td>{fmt(c.get("scale_mean_pearson_r"),3)}</td><td>{fmt(c.get("htmt_exploratory"),3)}</td></tr>')
    factor = psych.get('exploratory_factor_analysis', {})
    efa_note = 'Exploratory Pearson-based factor loadings available in psychometric report' if factor.get('performed') else 'EFA not performed / withheld; consult psychometric report'
    warnings = ''.join(f'<li>{html.escape(str(w))}</li>' for w in psych.get('warnings', []))
    body = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pedagogical Triad | Integrated Research Dashboard</title>
<style>
:root{{--ink:#183049;--sub:#586b80;--border:#dbe4ed;--bg:#f5f8fc;--accent:#146b91;--warn:#8a4918}}
*{{box-sizing:border-box}}body{{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;background:var(--bg);color:var(--ink);margin:0;line-height:1.5}}header{{background:#10283f;color:white;padding:32px max(22px,calc((100vw - 1180px)/2))}}header h1{{margin:.25rem 0;font-size:clamp(24px,3vw,38px)}}header p{{color:#d4e3f0;margin:0}}main{{max-width:1180px;margin:auto;padding:24px}}h2{{margin-top:35px}}h3{{margin:0;font-size:18px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:17px}}.panel,.banner{{background:white;border:1px solid var(--border);border-radius:12px;padding:19px;margin-bottom:14px}}.panel-head{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}}.tag{{font-size:10px;letter-spacing:.07em;font-weight:750;border-radius:5px;padding:5px 7px;white-space:nowrap}}.real{{background:#e1f2f7;color:#075f76}}.synthetic{{background:#fff0d8;color:#85480e}}.stat{{font-size:28px;font-weight:750;margin-top:8px}}.stat small{{font-size:14px;font-weight:400;color:var(--sub)}}.muted,.note{{color:var(--sub)}}.note{{font-size:12px}}.banner{{border-left:5px solid #d28d39}}.warning{{background:#fff7eb}}.tablewrap{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{padding:10px 12px;border-bottom:1px solid var(--border);text-align:left}}th{{font-size:12px;text-transform:uppercase;color:var(--sub);letter-spacing:.04em}}.links a{{display:inline-block;margin:4px 8px 5px 0;padding:8px 12px;border:1px solid #aac8dc;border-radius:8px;text-decoration:none;color:#07587d;background:white}}svg{{width:100%;height:auto}}footer{{padding:25px;text-align:center;color:var(--sub);font-size:13px}}@media(max-width:450px){{.grid{{grid-template-columns:1fr}}main{{padding:12px}}}}
</style></head><body><header><h1>The Pedagogical Triad Framework</h1><p>Bangladesh Secondary Education · Evidence-aware, offline research dashboard · National context vs teacher survey kept separate</p></header><main>
<section class="banner warning"><strong>Interpretation boundary:</strong> World Bank indicators are real, country-level education aggregates. Teacher responses below are <strong>{html.escape(status_title)}</strong>. {html.escape(status_note)} The instrument is <strong>NOT VALIDATED</strong>. There is no data pooling or causal interpretation.</section>
<section class="panel"><h2>Data provenance & quality</h2><p><span class="tag real">WORLD BANK · REAL AGGREGATE</span> {quality['rows']} records · {quality['valid_numeric_rows']} numeric rows · {len(quality.get('invalid_rows', []))} invalid rows · {len(quality.get('duplicate_indicator_country_year', []))} duplicate keys.</p><p><span class="tag synthetic">{html.escape(status_title)}</span> {psych['n']} survey responses · 12 ordinal items · preliminary psychometric diagnostics only.</p><p class="note">Counts refer to data loaded at build time, not a live connection. The source CSV should be re-fetched and re-audited when updating this dashboard.</p></section>
<h2>1 · World Bank secondary education trends</h2><div class="grid">{''.join(cards)}</div>
<section class="panel"><h3>Indicator audit</h3><div class="tablewrap"><table><thead><tr><th>Code</th><th>Indicator</th><th>N</th><th>Period</th><th>Missing years</th><th>First</th><th>Last</th></tr></thead><tbody>{''.join(table)}</tbody></table></div><p class="note">Gross enrolment is not net enrolment. All changes use each indicator's first and last observed years.</p></section>
<section class="panel"><h3>Pupil–teacher ratio</h3><p>Calculated from pupil and teacher totals only for matching years. Matching years in report: <strong>{html.escape(str(n_pair))}</strong>.</p><p class="note">A national count ratio is not a direct estimate of class size, teacher workload, student learning, or educational equity.</p></section>
<h2>2 · Teacher survey: {html.escape(status_title)}</h2><section class="banner warning"><strong>NOT VALIDATED · {html.escape(status)}</strong><p>{html.escape(status_note)} Alpha and approximate omega describe software output; neither establishes construct validity or population representativeness.</p></section>
<section class="panel"><h3>Exploratory reliability diagnostics</h3><div class="tablewrap"><table><thead><tr><th>Proposed scale</th><th>Cronbach's α</th><th>Approx. omega total</th><th>Mean score (1–5)</th></tr></thead><tbody>{''.join(reliab)}</tbody></table></div><p class="note">One-factor Pearson-based omega is a provisional approximation, not ordinal omega. Null values indicate undefined / withheld estimates.</p></section>
<section class="panel"><h3>Exploratory construct relationships</h3><div class="tablewrap"><table><thead><tr><th>Scales</th><th>Pearson r</th><th>Exploratory HTMT-like value</th></tr></thead><tbody>{''.join(corrs)}</tbody></table></div><p class="note">Correlation does not imply causation. HTMT-like output is not an independent validity decision.</p><p>{html.escape(efa_note)}.</p></section>
<section class="panel"><h3>Methodological warnings</h3><ul>{warnings}</ul></section>
<h2>3 · Download research exports</h2><section class="panel"><div class="links"><a href="worldbank_indicator_summary.csv" download>Indicator summary CSV</a><a href="research_summary.json" download>Research summary JSON</a><a href="research_methods.md" download>Methods & limitations MD</a><a href="psychometric_diagnostics.json" download>Psychometric diagnostics JSON</a><a href="worldbank_trends.json" download>World Bank trend report JSON</a><a href="worldbank_data_quality.json" download>World Bank audit JSON</a><a href="pupil_teacher_ratio.csv" download>Pupil–teacher ratio CSV</a></div><p class="note">Download links refer to files generated in the same output folder. In some browsers, local-file downloads open a preview: use Save As.</p></section>
</main><footer>Pedagogical Triad Framework · Evidence-aware research prototype · This dashboard is not a peer-reviewed validation study.</footer></body></html>'''
    return body, csv_rows


def build(root: Path, out: Path):
    root = root.resolve()
    out = out.resolve()
    series, qa, trends, psych = load_inputs(root/'data/raw/worldbank_bgd_secondary.csv', root/'outputs/worldbank_data_quality.json', root/'outputs/worldbank_trends.json', root/'outputs/psychometric_diagnostics.json')
    out.mkdir(parents=True, exist_ok=True)
    page, rows = build_content(series, qa, trends, psych)
    (out/'index.html').write_text(page, encoding='utf-8')
    with (out/'worldbank_indicator_summary.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    created = datetime.now(timezone.utc).isoformat()
    summary = {'generated_utc':created,'dashboard_status':'RESEARCH PROTOTYPE — NOT VALIDATED',
               'worldbank':{'source':'World Bank API country BGD; source URLs in raw CSV', 'records':qa['rows'], 'indicators':rows},
               'teacher_survey':{'dataset_status':psych['dataset_status'], 'n':psych['n'], 'validity_decision':psych['validity_decision'],
                                 'aggregate_diagnostics_only':True},
               'separation_note':'No teacher-level survey data or synthetic rows are exported; no dataset is pooled with national aggregates.'}
    (out/'research_summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False)+'\n',encoding='utf-8')
    methods = f'''# Research dashboard — methods and limitations\n\nBuilt UTC: {created}\n\n## Sources\n- World Bank Bangladesh secondary education indicators, from `data/raw/worldbank_bgd_secondary.csv`, retrieved by Phase 1 API script; exact source URLs and retrieval dates reside in the source CSV.\n- Country-level audit: `outputs/worldbank_data_quality.json`; trends: `outputs/worldbank_trends.json`.\n- Teacher survey: Phase 4 *aggregate diagnostics*, status **{psych['dataset_status']}**, n={psych['n']}. This is **NOT VALIDATED**.\n\n## Processing\n- Present all valid observed years, with discontinuities at missing calendar years; no interpolation or imputation.\n- Relative change and absolute change describe first vs last **observed** year, not fitted trends.\n- Pupil–teacher ratio requires same-year pupil and teacher counts and is not class size.\n- Survey scales have four ordinal 1–5 items each; current omega is an exploratory one-factor Pearson-based estimate, not ordinal omega.\n- Data classes are displayed separately; no merges, correlation across ecological and individual records, or causal claims.\n\n## Limitations and validity safeguards\n- World Bank indicators do not operationalize philosophy or digital literacy, and do not alone establish educational equity.\n- Synthetic results are software demonstrations, not empirical psychological evidence.\n- A field label alone does not prove informed consent, ethics approval, representativeness, or measurement validity.\n- Teacher-level content validity, response processes, factor structure, invariance and independent validation remain future research tasks.\n- No participant-level survey rows should be committed to a public GitHub repository.\n'''
    (out/'research_methods.md').write_text(methods,encoding='utf-8')
    for name in ('psychometric_diagnostics.json','worldbank_trends.json','worldbank_data_quality.json','pupil_teacher_ratio.csv'):
        f = root/'outputs'/name
        if f.is_file():
            if f.resolve() != (out/name).resolve():
                shutil.copy2(f, out/name)
        elif name == 'pupil_teacher_ratio.csv':
            raise FileNotFoundError(f'Missing {f}; run py -3.15 trend_analysis.py first')
    return out/'index.html', qa['rows'], psych['n'], psych['dataset_status']


def main(argv=None):
    parser = argparse.ArgumentParser(description='Build offline Phase 5 dashboard (no external packages).')
    parser.add_argument('action', nargs='?', choices=['build'], default='build')
    parser.add_argument('--root', type=Path, default=Path('.'), help='Existing Pedagogical Triad repository root')
    parser.add_argument('--output', type=Path, default=Path('outputs/dashboard'), help='Dashboard output folder')
    args = parser.parse_args(argv)
    try:
        dest, n_wb, n_survey, status = build(args.root, args.output)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(2, f'Build failed: {exc}\n')
    print(f'Dashboard created: {dest}')
    print(f'World Bank: {n_wb} audited national-aggregate records; survey: {n_survey} {status} responses (aggregated diagnostics only).')
    print('VALIDITY: NOT VALIDATED. No data pooling or imputation.')


if __name__ == '__main__':
    main()
