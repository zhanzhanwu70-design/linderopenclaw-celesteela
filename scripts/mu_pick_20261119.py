#!/usr/bin/env python3
"""2026-11-19 抽取指定對位（合併口徑加權）。"""
import json, collections

M = json.load(open('memory/mu_matrix_20261119_c1.json', encoding='utf-8'))
M18 = json.load(open('memory/mu_matrix_20261118_c1.json', encoding='utf-8'))
EB = json.load(open('memory/ptcgp_meta_20261119_std.json', encoding='utf-8'))['rows']


def branches(comb):
    cands = [r['name'] for r in EB if r['name'] == comb or r['name'].startswith(comb + ' ')]
    return cands or [comb]


def opp_names(comb):
    return set([comb]) | set(branches(comb))


def agg_row(matrix, comb, opp_comb):
    tot = 0; acc = 0.0
    keys = opp_names(opp_comb)
    for rn in branches(comb):
        d = matrix.get(rn, {})
        for k, (w, n) in d.items():
            if k in keys:
                acc += w * n; tot += n
    return [round(acc / tot, 1), tot] if tot else None


PAIRS = [
    ('Magnezone','Vespiquen ex'),('Magnezone','Hoopa ex'),('Magnezone','Mega Altaria ex'),
    ('Magnezone','Mega Greninja ex'),('Magnezone','Suicune ex'),('Magnezone','Mega Lucario ex'),
    ('Magnezone','Hydreigon'),('Magnezone','Umbreon'),('Magnezone','Mega Charizard Y ex'),
    ('Hydreigon','Vespiquen ex'),('Hydreigon','Magnezone'),('Hydreigon','Mega Altaria ex'),
    ('Hydreigon','Hoopa ex'),('Hydreigon','Umbreon'),('Hydreigon','Mega Charizard Y ex'),
    ('Vespiquen ex','Hoopa ex'),('Vespiquen ex','Suicune ex'),('Vespiquen ex','Mega Altaria ex'),
    ('Vespiquen ex','Mega Mewtwo X ex'),('Vespiquen ex','Mega Lucario ex'),
    ('Hoopa ex','Mega Altaria ex'),('Hoopa ex','Suicune ex'),('Hoopa ex','Mega Charizard Y ex'),
    ('Hoopa ex','Mega Mewtwo X ex'),('Hoopa ex','Mega Lucario ex'),('Hoopa ex','Mega Greninja ex'),
    ('Mega Altaria ex','Mega Lucario ex'),('Mega Altaria ex','Mega Mewtwo X ex'),
    ('Mega Altaria ex','Umbreon'),('Mega Altaria ex','Mega Charizard Y ex'),
    ('Mega Altaria ex','Suicune ex'),('Mega Altaria ex','Mega Greninja ex'),
    ('Suicune ex','Mega Greninja ex'),('Suicune ex','Mega Altaria ex'),('Suicune ex','Mega Charizard Y ex'),
    ('Mega Charizard Y ex','Hoopa ex'),('Mega Charizard Y ex','Mega Altaria ex'),
    ('Mega Charizard Y ex','Mega Lucario ex'),('Mega Charizard Y ex','Suicune ex'),
    ('Mega Charizard Y ex','Mega Greninja ex'),('Mega Charizard Y ex','Mega Mewtwo X ex'),
    ('Mega Mewtwo X ex','Mega Altaria ex'),('Mega Mewtwo X ex','Hoopa ex'),
    ('Mega Mewtwo X ex','Magnezone'),('Mega Mewtwo X ex','Vespiquen ex'),
    ('Umbreon','Mega Altaria ex'),('Umbreon','Magnezone'),('Umbreon','Suicune ex'),
    ('Umbreon','Mega Greninja ex'),('Umbreon','Mega Mewtwo X ex'),('Umbreon','Hoopa ex'),
    ('Mega Greninja ex','Suicune ex'),('Mega Greninja ex','Magnezone'),('Mega Greninja ex','Mega Manectric ex'),
    ('Mega Lucario ex','Mega Altaria ex'),('Mega Lucario ex','Magnezone'),('Mega Lucario ex','Hoopa ex'),
]
for a,b in PAIRS:
    cur = agg_row(M, a, b)
    rv = agg_row(M, b, a)
    p = agg_row(M18, a, b)
    cs = f"{cur[0]:>5.1f}% N={cur[1]:>4}" if cur else '   --    '
    rs = f"{rv[0]:>5.1f}% N={rv[1]:>4}" if rv else '   --    '
    ps = f"昨 {p[0]:>5.1f}% N={p[1]:>4}" if p else ''
    print(f"{a:24} vs {b:24}: {cs}  | 反向 {b:24}->{a:20}: {rs}  | {ps}")
