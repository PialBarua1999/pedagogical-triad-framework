"""CLI. Run with python -m triad from repo root (PYTHONPATH=src)."""
import argparse
import json
from pathlib import Path
from .core import load_csv,validate,summarize,html_report
from .worldbank import fetch

def main():
    p=argparse.ArgumentParser(description="Pedagogical Triad educational research CLI")
    p.add_argument("command",choices=["analyze","fetch-worldbank","validate"])
    p.add_argument("--input",default="data/demo/synthetic_teacher_survey.csv")
    p.add_argument("--output",default="outputs")
    args=p.parse_args()
    if args.command=="fetch-worldbank":
        n,failures=fetch(Path("data/raw"))
        print(f"Downloaded {n} non-missing World Bank records; failures: {len(failures)}. See data/raw/fetch_log.json")
        if not n: raise SystemExit("No data retrieved. Check internet/API; no invented fallback data.")
        return
    rows=load_csv(Path(args.input));status=validate(rows)
    print(f"Validated {len(rows)} records; status: {status}")
    if args.command=="validate":return
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    result=summarize(rows,status)
    (output/"triad_summary.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    (output/"triad_report.html").write_text(html_report(result),encoding="utf-8")
    print(f"Created {output/'triad_summary.json'} and {output/'triad_report.html'}")
if __name__=="__main__":main()
