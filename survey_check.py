#!/usr/bin/env python3
"""Offline survey schema checker. No field data or responses are printed."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ITEMS = [f"{stem}{n}" for stem in ("ph", "dl", "eq") for n in range(1,5)]
REQUIRED = ["response_id", "division", "setting", "school_type", "data_status"] + ITEMS
STATUS = {"synthetic", "field_unverified", "field_verified"}


def audit(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        missing_columns = sorted(set(REQUIRED) - set(columns))
        if missing_columns:
            raise ValueError("Missing required columns: " + ", ".join(missing_columns))
        errors, seen, counts, statuses = [], set(), Counter(), set()
        count = 0
        for row_num, row in enumerate(reader, start=2):
            count += 1
            rid = (row.get("response_id") or "").strip()
            if not rid or rid in seen:
                errors.append(f"Row {row_num}: blank or repeated response_id")
            seen.add(rid)
            for column in ("division", "setting", "school_type"):
                if not (row.get(column) or "").strip():
                    errors.append(f"Row {row_num}: missing {column}")
            status = (row.get("data_status") or "").strip()
            statuses.add(status)
            if status not in STATUS:
                errors.append(f"Row {row_num}: invalid data_status")
            counts[status] += 1
            for item in ITEMS:
                value = (row.get(item) or "").strip()
                if value not in {"1", "2", "3", "4", "5"}:
                    errors.append(f"Row {row_num}: {item} is not 1–5")
            if len(errors) >= 100:
                break
    if len(statuses) > 1:
        errors.append("Mixed data_status values; analyze datasets separately")
    if not count:
        errors.append("No survey responses")
    return {"file": path.name, "rows_reviewed": count, "status_counts": dict(counts),
            "schema_valid": not errors, "errors": errors,
            "interpretation": "Structure only. Does not establish ethics, sampling validity or psychometric validity."}


def main() -> int:
    parser = argparse.ArgumentParser(description="Teacher survey offline structural audit")
    parser.add_argument("--input", required=True, type=Path, help="CSV path (do not commit personal field data)")
    parser.add_argument("--output", type=Path, help="Optional local JSON audit path")
    args = parser.parse_args()
    try:
        result = audit(args.input)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Input error: {exc}")
        return 2
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Records reviewed: {result['rows_reviewed']}; schema valid: {result['schema_valid']}; errors: {len(result['errors'])}")
    for error in result["errors"][:10]:
        print("-", error)
    return 0 if result['schema_valid'] else 1


if __name__ == "__main__":
    raise SystemExit(main())
