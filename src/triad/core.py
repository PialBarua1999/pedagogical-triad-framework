"""Standard-library-only, explicitly descriptive research utilities."""
from __future__ import annotations
import csv
import html
import json
import math
import statistics
from collections import Counter
from pathlib import Path

ITEMS = {
    "philosophy": ["ph1", "ph2", "ph3", "ph4"],
    "digital_literacy": ["dl1", "dl2", "dl3", "dl4"],
    "equity": ["eq1", "eq2", "eq3", "eq4"],
}
GROUPS = ["division", "setting", "school_type"]
FIELDS = ["response_id", "division", "setting", "school_type", "data_status"] + sum(ITEMS.values(), [])


def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = set(FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
        return list(reader)


def validate(rows):
    errors=[]
    ids=set()
    for n, row in enumerate(rows, 2):
        rid=row["response_id"].strip()
        if not rid or rid in ids: errors.append(f"Line {n}: empty/duplicate response_id")
        ids.add(rid)
        if row["data_status"] not in ("synthetic", "field_unverified", "field_verified"):
            errors.append(f"Line {n}: invalid data_status")
        for group in GROUPS:
            if not row[group].strip(): errors.append(f"Line {n}: empty {group}")
        for item in sum(ITEMS.values(), []):
            try:
                x=int(row[item])
                if not 1 <= x <= 5: raise ValueError
            except (ValueError,TypeError): errors.append(f"Line {n}: {item} must be integer 1..5")
    if not rows: errors.append("CSV contains no rows")
    if errors: raise ValueError("\n".join(errors[:40]))
    statuses={r["data_status"] for r in rows}
    if len(statuses)>1: raise ValueError("Do not mix synthetic and real or differently verified responses in one run")
    return statuses.pop()


def mean(xs): return round(statistics.mean(xs), 3) if xs else None


def alpha(rows, keys):
    """Cronbach alpha, descriptive only; not proof of construct validity."""
    if len(rows)<3: return None
    columns=[[int(r[k]) for r in rows] for k in keys]
    variances=[statistics.variance(c) for c in columns]
    totals=[sum(int(r[k]) for k in keys) for r in rows]
    vt=statistics.variance(totals)
    if vt==0: return None
    k=len(keys)
    return round((k/(k-1)) * (1-sum(variances)/vt),3)


def pearson(x,y):
    if len(x)<3: return None
    mx=statistics.mean(x);my=statistics.mean(y)
    a=sum((v-mx)*(w-my) for v,w in zip(x,y))
    b=math.sqrt(sum((v-mx)**2 for v in x)*sum((w-my)**2 for w in y))
    return round(a/b,3) if b else None


def summarize(rows,status):
    scores={name:[statistics.mean(int(r[k]) for k in keys) for r in rows]
            for name,keys in ITEMS.items()}
    result={"data_status": status, "n":len(rows),
            "disclaimer":"Descriptive associations only; not causal evidence, nationally representative estimates, or validated psychological diagnosis.",
            "scales":{name:{"mean":mean(vals),"std_dev":round(statistics.stdev(vals),3) if len(vals)>1 else None,
                            "cronbach_alpha":alpha(rows,ITEMS[name])} for name,vals in scores.items()},
            "correlations":{}, "subgroups":{},"coverage":{}}
    keys=list(scores)
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            result["correlations"][f"{keys[i]}__{keys[j]}"]=pearson(scores[keys[i]],scores[keys[j]])
    for group in GROUPS:
        result["coverage"][group]=dict(sorted(Counter(r[group] for r in rows).items()))
        result["subgroups"][group]={}
        for level in sorted(set(r[group] for r in rows)):
            selected=[i for i,r in enumerate(rows) if r[group]==level]
            result["subgroups"][group][level]={"n":len(selected),
                "mean_scores":{k:mean([v[i] for i in selected]) for k,v in scores.items()}}
    return result


def html_report(result):
    esc=lambda v: html.escape(str(v))
    scales=''.join(f'<tr><td>{esc(k)}</td><td>{esc(v["mean"])}</td><td>{esc(v["std_dev"])}</td><td>{esc(v["cronbach_alpha"])}</td></tr>' for k,v in result['scales'].items())
    corr=''.join(f'<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>' for k,v in result['correlations'].items())
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pedagogical Triad | Research Report</title><style>body{{font:16px/1.6 system-ui;max-width:1000px;margin:50px auto;padding:0 20px;color:#16263c}}h1{{color:#123b59}}.notice{{background:#fff3df;padding:18px;border-left:5px solid #d68c20}}table{{border-collapse:collapse;width:100%;margin:18px 0}}th,td{{padding:10px;border-bottom:1px solid #dce4ea;text-align:left}}th{{background:#edf4f8}}small{{color:#486177}}</style></head><body><h1>The Pedagogical Triad Framework</h1><p>Bangladesh secondary education — descriptive prototype report</p><div class="notice"><b>DATA STATUS: {esc(result['data_status']).upper()}</b><p>{esc(result['disclaimer'])}</p></div><h2>Participants: {result['n']}</h2><h2>Scale summaries</h2><table><tr><th>Construct</th><th>Mean (1–5)</th><th>SD</th><th>Alpha</th></tr>{scales}</table><h2>Exploratory Pearson correlations</h2><table><tr><th>Pair</th><th>r</th></tr>{corr}</table><h2>Coverage</h2><pre>{esc(json.dumps(result['coverage'],ensure_ascii=False,indent=2))}</pre><small>Self-report item averages are provisional. Do not interpret as validated latent factors. This report does not establish causation.</small></body></html>"""
