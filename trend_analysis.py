"""Auditable descriptive trends for World Bank Bangladesh secondary education.

Run from repository root: py -3.15 trend_analysis.py
No third-party packages. Missing years are never interpolated.
"""
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

DATA = Path('data/raw/worldbank_bgd_secondary.csv')
OUT = Path('outputs')
INDICATORS = {
    'SE.SEC.ENRR': 'Secondary gross enrolment (%)',
    'SE.SEC.TCHR': 'Secondary teachers (number)',
    'SE.SEC.TCHR.FE.ZS': 'Female secondary teachers (%)',
    'SE.SEC.ENRL': 'Secondary pupils (number)',
}


def analyze(path: Path = DATA) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f'CSV not found: {path}. Run py -3.15 run.py fetch-worldbank first.')
    series = defaultdict(dict)
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        required = {'indicator_code', 'country', 'year', 'value'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f'Missing CSV columns: {sorted(required - set(reader.fieldnames or []))}')
        for line_no, row in enumerate(reader, 2):
            code = row['indicator_code'].strip()
            if code not in INDICATORS:
                continue
            if row['country'].strip() != 'Bangladesh':
                raise ValueError(f'Line {line_no}: unexpected country')
            try:
                year = int(row['year'])
                value = float(row['value'])
            except (TypeError, ValueError) as exc:
                raise ValueError(f'Line {line_no}: invalid year/value') from exc
            if not math.isfinite(value) or value < 0:
                raise ValueError(f'Line {line_no}: invalid measurement')
            if code.endswith('.ZS') and value > 100:
                raise ValueError(f'Line {line_no}: percentage exceeds 100')
            if code in ('SE.SEC.TCHR', 'SE.SEC.ENRL') and value <= 0:
                raise ValueError(f'Line {line_no}: count cannot be zero')
            if year in series[code]:
                raise ValueError(f'Duplicate indicator-year: {code}/{year}')
            series[code][year] = value

    trends = {}
    for code, name in INDICATORS.items():
        observations = sorted(series[code].items())
        if not observations:
            trends[code] = {'name': name, 'records': 0}
            continue
        first_year, first_value = observations[0]
        last_year, last_value = observations[-1]
        delta = last_value - first_value
        trends[code] = {
            'name': name,
            'records': len(observations),
            'first_observation': {'year': first_year, 'value': first_value},
            'last_observation': {'year': last_year, 'value': last_value},
            'absolute_change': delta,
            'relative_change_percent': (delta / first_value * 100) if first_value else None,
            'missing_years': sorted(set(range(first_year, last_year + 1)) - set(series[code])),
            'minimum': {'year': min(observations, key=lambda x: x[1])[0], 'value': min(v for _, v in observations)},
            'maximum': {'year': max(observations, key=lambda x: x[1])[0], 'value': max(v for _, v in observations)},
        }

    shared_years = sorted(set(series['SE.SEC.ENRL']) & set(series['SE.SEC.TCHR']))
    ratio = [
        {'year': year, 'pupils': series['SE.SEC.ENRL'][year],
         'teachers': series['SE.SEC.TCHR'][year],
         'pupils_per_teacher': series['SE.SEC.ENRL'][year] / series['SE.SEC.TCHR'][year]}
        for year in shared_years
    ]
    return {
        'source': str(path),
        'country': 'Bangladesh',
        'method': 'Descriptive, available-case analysis; no interpolation, imputation or causal inference',
        'indicator_trends': trends,
        'pupil_teacher_ratio': {
            'definition': 'Secondary pupils divided by secondary teachers in the same reported year; descriptive proxy, not classroom size',
            'shared_years_count': len(ratio),
            'first': ratio[0] if ratio else None,
            'last': ratio[-1] if ratio else None,
            'observations': ratio,
        },
        'limitations': [
            'World Bank national aggregates are not measures of teacher philosophy or digital literacy.',
            'Indicator changes may reflect coverage, definitions or reporting differences.',
            'Gross enrolment ratios may exceed 100; do not equate them with net enrolment.',
            'Missing years are excluded rather than estimated.',
            'The pupil-teacher ratio is not a measure of class size or teaching quality.',
        ],
    }


def main() -> None:
    report = analyze()
    OUT.mkdir(parents=True, exist_ok=True)
    destination = OUT / 'worldbank_trends.json'
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    csv_path = OUT / 'pupil_teacher_ratio.csv'
    with csv_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['year', 'pupils', 'teachers', 'pupils_per_teacher'])
        writer.writeheader()
        writer.writerows(report['pupil_teacher_ratio']['observations'])
    for code, item in report['indicator_trends'].items():
        if not item['records']:
            print(f'{code}: no observations')
            continue
        first, last = item['first_observation'], item['last_observation']
        print(f"{code}: {item['records']} records; {first['year']}={first['value']:.3f}, "
              f"{last['year']}={last['value']:.3f}; missing years={len(item['missing_years'])}")
    print(f"Paired pupil/teacher years: {report['pupil_teacher_ratio']['shared_years_count']}")
    print(f'Reports saved: {destination} and {csv_path}')


if __name__ == '__main__':
    main()
