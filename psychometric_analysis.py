#!/usr/bin/env python3
"""Pedagogical Triad Phase 4: transparent exploratory psychometric diagnostics.

Python >=3.10 standard library only. No personal-level outputs.
Exploratory Pearson principal-axis factoring is NOT ordinal EFA/CFA validation.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

ITEMS = {"ph": [f"ph{i}" for i in range(1, 5)],
         "dl": [f"dl{i}" for i in range(1, 5)],
         "eq": [f"eq{i}" for i in range(1, 5)]}
ALL = [x for group in ITEMS.values() for x in group]
REQUIRED = ["response_id", "division", "setting", "school_type", "data_status"] + ALL
STATUSES = {"synthetic", "field_unverified", "field_verified"}


def mean(x):
    return sum(x) / len(x) if x else None


def variance(x):
    return sum((a - mean(x)) ** 2 for a in x) / (len(x) - 1) if len(x) > 1 else None


def corr(x, y):
    if len(x) != len(y) or len(x) < 3:
        return None
    mx, my = mean(x), mean(y)
    xx = sum((v-mx)**2 for v in x)
    yy = sum((v-my)**2 for v in y)
    if xx < 1e-12 or yy < 1e-12:
        return None
    return max(-1.0, min(1.0, sum((a-mx)*(b-my) for a, b in zip(x,y))/math.sqrt(xx*yy)))


def alpha(columns):
    n = len(columns)
    if n < 2 or not columns or len(columns[0]) < 3:
        return None
    item_vars = [variance(c) for c in columns]
    totals = [sum(values) for values in zip(*columns)]
    total_var = variance(totals)
    if not total_var or any(v is None for v in item_vars):
        return None
    return n / (n-1) * (1-sum(item_vars)/total_var)


def identity(n):
    return [[float(i == j) for j in range(n)] for i in range(n)]


def eigen_symmetric(a, max_iterations=3000, tol=1e-11):
    """Pure-Python Jacobi eigendecomposition of a real symmetric matrix."""
    n = len(a)
    m = [row[:] for row in a]
    v = identity(n)
    for _ in range(max_iterations):
        p, q = max(((i,j) for i in range(n) for j in range(i+1,n)),
                   key=lambda ij: abs(m[ij[0]][ij[1]]), default=(0,0))
        if p == q or abs(m[p][q]) < tol:
            break
        angle = .5 * math.atan2(2*m[p][q], m[q][q]-m[p][p])
        c, s = math.cos(angle), math.sin(angle)
        # similarity transform with rotating columns p,q
        for i in range(n):
            if i not in (p,q):
                aip, aiq = m[i][p], m[i][q]
                m[i][p] = m[p][i] = c*aip-s*aiq
                m[i][q] = m[q][i] = s*aip+c*aiq
        app, aqq, apq = m[p][p], m[q][q], m[p][q]
        m[p][p] = c*c*app + s*s*aqq-2*c*s*apq
        m[q][q] = s*s*app + c*c*aqq+2*c*s*apq
        m[p][q] = m[q][p] = 0.0
        for i in range(n):
            vip, viq = v[i][p], v[i][q]
            v[i][p] = c*vip-s*viq
            v[i][q] = s*vip+c*viq
    pairs = sorted(((m[j][j], [v[i][j] for i in range(n)]) for j in range(n)),
                   key=lambda z: z[0], reverse=True)
    return [x[0] for x in pairs], [x[1] for x in pairs]


def loadings_paf(r, factors, iterations=60):
    """Exploratory principal-axis common-factor solution (unrotated)."""
    n = len(r)
    if factors < 1 or factors >= n:
        raise ValueError('Factors must be between 1 and n_items-1')
    h = [max(.05, min(.95, max(r[i][j]*r[i][j] for j in range(n) if j != i))) for i in range(n)]
    for _ in range(iterations):
        reduced = [[h[i] if i == j else r[i][j] for j in range(n)] for i in range(n)]
        eig, vec = eigen_symmetric(reduced)
        if eig[factors-1] <= 0:
            return None
        load = [[vec[k][i]*math.sqrt(eig[i]) for i in range(factors)] for k in range(n)]
        new_h = [max(.01, min(.99, sum(v*v for v in row))) for row in load]
        if max(abs(x-y) for x,y in zip(h,new_h)) < 1e-6:
            return load
        h = new_h
    return load


def rotate_varimax(load, iterations=150, tol=1e-8):
    """Orthogonal varimax; exploratory only."""
    n, k = len(load), len(load[0])
    a = [row[:] for row in load]
    for _ in range(iterations):
        biggest = 0.0
        for p in range(k):
            for q in range(p+1,k):
                u = [a[i][p]**2-a[i][q]**2 for i in range(n)]
                v = [2*a[i][p]*a[i][q] for i in range(n)]
                A = sum(x*x-y*y for x,y in zip(u,v))-(sum(u)**2-sum(v)**2)/n
                B = 2*(sum(x*y for x,y in zip(u,v))-sum(u)*sum(v)/n)
                theta = .25*math.atan2(B,A)
                biggest = max(biggest, abs(theta))
                c,s = math.cos(theta),math.sin(theta)
                for i in range(n):
                    x,y = a[i][p],a[i][q]
                    a[i][p],a[i][q] = c*x+s*y,-s*x+c*y
        if biggest < tol:
            break
    return a


def correlation_matrix(cols):
    r = [[corr(x,y) for y in cols] for x in cols]
    if any(z is None for row in r for z in row):
        return None
    return r


def one_factor_omega(cols):
    """Approximate omega total under single common-factor model and standardized items."""
    r = correlation_matrix(cols)
    if r is None:
        return None
    loading = loadings_paf(r, 1)
    if loading is None:
        return None
    l = [row[0] for row in loading]
    signal = sum(l)**2
    error = sum(max(.01, 1-x*x) for x in l)
    return signal/(signal+error) if signal+error else None


def htmt(group_a, group_b):
    cross = [abs(corr(a,b)) for a in group_a for b in group_b]
    own_a = [abs(corr(group_a[i],group_a[j])) for i in range(len(group_a)) for j in range(i+1,len(group_a))]
    own_b = [abs(corr(group_b[i],group_b[j])) for i in range(len(group_b)) for j in range(i+1,len(group_b))]
    if any(v is None for v in cross+own_a+own_b):
        return None
    denom = math.sqrt(mean(own_a)*mean(own_b))
    return mean(cross)/denom if denom > 1e-12 else None


def safe_round(v):
    return None if v is None or not math.isfinite(v) else round(v, 5)


def read_responses(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader = csv.DictReader(f)
        names = reader.fieldnames or []
        missing = sorted(set(REQUIRED)-set(names))
        if missing:
            raise ValueError('Missing required columns: '+', '.join(missing))
        rows, seen, statuses = [], set(), set()
        for line, row in enumerate(reader, 2):
            rid = (row.get('response_id') or '').strip()
            if not rid or rid in seen:
                raise ValueError(f'Line {line}: blank or duplicate response_id')
            seen.add(rid)
            if any(not (row.get(c) or '').strip() for c in ('division','setting','school_type')):
                raise ValueError(f'Line {line}: missing contextual column')
            status = (row.get('data_status') or '').strip()
            if status not in STATUSES:
                raise ValueError(f'Line {line}: invalid data_status')
            statuses.add(status)
            for item in ALL:
                raw = (row.get(item) or '').strip()
                if raw not in ('1','2','3','4','5'):
                    raise ValueError(f'Line {line}: {item} must be an integer 1-5')
            rows.append({k:int(row[k]) for k in ALL})
        if not rows:
            raise ValueError('No responses')
        if len(statuses) != 1:
            raise ValueError('Mixed data_status: keep synthetic and field datasets separate')
        return rows, next(iter(statuses))


def analyze(rows, status):
    n = len(rows)
    cols = {item:[row[item] for row in rows] for item in ALL}
    warnings = []
    if n < 100:
        warnings.append('N<100: factor structure especially unstable; use only exploratory diagnostics.')
    if n < 5*len(ALL):
        warnings.append('Less than five observations per item; factor analysis withheld.')
    sub = {}
    means = {}
    for group, items in ITEMS.items():
        c = [cols[item] for item in items]
        scores = [sum(row[item] for item in items)/len(items) for row in rows]
        means[group] = scores
        item_total = {}
        for item in items:
            other = [sum(row[x] for x in items if x != item) for row in rows]
            item_total[item] = safe_round(corr(cols[item], other))
        sub[group] = {'items': items, 'mean_of_person_means':safe_round(mean(scores)),
                      'sd_of_person_means':safe_round(math.sqrt(variance(scores))) if variance(scores) is not None else None,
                      'cronbach_alpha':safe_round(alpha(c)),
                      'omega_total_one_factor_approx':safe_round(one_factor_omega(c)),
                      'corrected_item_total_correlations':item_total,
                      'constant_items':[item for item in items if (variance(cols[item]) or 0)<1e-12]}
        av, ov = sub[group]['cronbach_alpha'], sub[group]['omega_total_one_factor_approx']
        if av is not None and ov is not None and abs(av-ov) > .20:
            warnings.append(f'{group}: alpha and approximate omega disagree strongly; inspect factor-model fit and item structure before interpreting reliability.')
        if sub[group]['constant_items']:
            warnings.append(f'{group}: constant item(s); related reliability values may be undefined.')
        if sub[group]['cronbach_alpha'] is not None and sub[group]['cronbach_alpha'] < 0:
            warnings.append(f'{group}: negative alpha; examine coding/dimensionality.')
    pairs = {}
    for a,b in [('ph','dl'),('ph','eq'),('dl','eq')]:
        pairs[f'{a}_{b}']={'scale_mean_pearson_r':safe_round(corr(means[a],means[b])),
                           'htmt_exploratory':safe_round(htmt([cols[i] for i in ITEMS[a]], [cols[i] for i in ITEMS[b]]))}
    factor = {'performed':False, 'method':'Exploratory Pearson-correlation principal-axis factoring with orthogonal varimax; NOT polychoric EFA or CFA',
              'factor_count':3, 'loadings':None, 'limitations':'No model-fit test, no uncertainty intervals, no invariance analysis.'}
    if n >= 5*len(ALL):
        r = correlation_matrix([cols[x] for x in ALL])
        if r is None:
            warnings.append('EFA withheld: at least one item has zero variance.')
        else:
            unrotated = loadings_paf(r,3)
            if unrotated is None:
                warnings.append('EFA withheld: insufficient positive eigenvalues for requested common factors.')
            else:
                load = rotate_varimax(unrotated)
                factor['performed'] = True
                factor['loadings'] = {item:[safe_round(x) for x in line] for item,line in zip(ALL,load)}
    if status == 'synthetic':
        warnings.insert(0,'SYNTHETIC DEMONSTRATION ONLY: no empirical reliability, validity or population claims.')
    else:
        warnings.insert(0,'Field-status label is self-reported metadata; consent, approval and sample provenance have NOT been independently verified.')
    return {'dataset_status':status,'n':n,'item_scale':'Ordinal agreement 1-5; complete cases only',
            'descriptive_reliability':sub,'exploratory_construct_relationships':pairs,
            'exploratory_factor_analysis':factor,
            'validity_decision':'NOT VALIDATED — evidence requires content/response-process review, independent field data, ordinal EFA and confirmatory testing.',
            'warnings':warnings}


def main(argv=None):
    parser=argparse.ArgumentParser(description='Exploratory Phase 4 analysis; no additional Python packages')
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=Path('outputs/psychometric_diagnostics.json'))
    args=parser.parse_args(argv)
    try:
        rows,status=read_responses(args.input)
        report=analyze(rows,status)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    except (ValueError,OSError,UnicodeError) as exc:
        print(f'Validation/error: {exc}')
        return 2
    print(f'Analyzed {report["n"]} {status} responses; report: {args.output}')
    print('Factor analysis performed:',report['exploratory_factor_analysis']['performed'])
    print('VALIDITY STATUS: NOT VALIDATED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
