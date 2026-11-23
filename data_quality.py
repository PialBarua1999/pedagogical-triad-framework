"""Audit World Bank Bangladesh secondary education CSV without third-party packages.

Run from the repository root: py -3.15 data_quality.py
"""
import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

SOURCE = Path('data/raw/worldbank_bgd_secondary.csv')
OUTPUT = Path('outputs/worldbank_data_quality.json')
EXPECTED_COLUMNS = {'indicator_code', 'indicator', 'country', 'year', 'value', 'source_url', 'retrieved_utc'}
PERCENT_INDICATORS = {'SE.SEC.TCHR.FE.ZS'}  # GER may legitimately exceed 100%.
NONNEGATIVE_INDICATORS = {'SE.SEC.ENRR', 'SE.SEC.TCHR', 'SE.SEC.ENRL'}


def audit(source=SOURCE):
    with source.open('r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not EXPECTED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError(f'Missing required CSV columns: {sorted(EXPECTED_COLUMNS - set(reader.fieldnames or []))}')
        rows = list(reader)

    codes = defaultdict(list)
    seen = Counter()
    invalid = []
    missing = Counter()
    valid = 0
    countries = Counter()
    for line, row in enumerate(rows, start=2):
        code = (row['indicator_code'] or '').strip()
        country = (row['country'] or '').strip()
        countries[country] += 1
        for key in EXPECTED_COLUMNS:
            if not (row.get(key) or '').strip():
                missing[key] += 1
        try:
            year = int(row['year'])
            value = float(row['value'])
            if not math.isfinite(value):
                raise ValueError('non-finite value')
            if not 1900 <= year <= datetime.now(timezone.utc).year:
                raise ValueError('year outside plausible range')
            if code in PERCENT_INDICATORS and not 0 <= value <= 100:
                raise ValueError('percentage outside 0–100')
            if code in NONNEGATIVE_INDICATORS and value < 0:
                raise ValueError('negative count or gross enrolment')
        except (ValueError, TypeError) as exc:
            invalid.append({'line': line, 'reason': str(exc)})
            continue
        valid += 1
        seen[(code, country, year)] += 1
        codes[code].append({'year': year, 'value': value, 'label': row['indicator']})

    duplicate_keys = [{'indicator_code': code, 'country': country, 'year': year, 'count': count}
                      for (code, country, year), count in sorted(seen.items()) if count > 1]
    indicators = {}
    for code, records in sorted(codes.items()):
        years = sorted({r['year'] for r in records})
        indicators[code] = {
            'name': records[0]['label'],
            'records': len(records),
            'start_year': years[0],
            'end_year': years[-1],
            'years_missing_within_range': sorted(set(range(years[0], years[-1] + 1)) - set(years)),
            'minimum_value': min(r['value'] for r in records),
            'maximum_value': max(r['value'] for r in records),
        }
    return {
        'source': str(source), 'rows': len(rows), 'valid_numeric_rows': valid,
        'missing_cell_counts': dict(missing), 'invalid_rows': invalid,
        'duplicate_indicator_country_year': duplicate_keys,
        'countries': dict(countries), 'indicators': indicators,
        'interpretation_note': 'Country-level aggregates cannot validate teacher-level psychological constructs or causal effects.',
    }


if __name__ == '__main__':
    if not SOURCE.is_file():
        raise SystemExit(f'Input not found: {SOURCE}. Run this script from your repository root.')
    report = audit()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Rows: {report['rows']} | Valid: {report['valid_numeric_rows']} | Invalid: {len(report['invalid_rows'])}")
    print(f"Missing cells: {report['missing_cell_counts']} | Duplicate keys: {len(report['duplicate_indicator_country_year'])}")
    print(f"Countries: {report['countries']}")
    for code, item in report['indicators'].items():
        print(f"{code}: {item['records']} records, {item['start_year']}–{item['end_year']}, gaps={len(item['years_missing_within_range'])}")
    print(f'Report saved: {OUTPUT}')
