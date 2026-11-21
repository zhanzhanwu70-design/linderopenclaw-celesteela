#!/usr/bin/env python3
"""2026-11-19 對位「乾淨合併」：只併入顯著分支（分支 N>=50），並列出構成分支。
A 壓 B p% 取自 A 自己那一列；A 輸 B p% 取自 B 那一列（= A 輸的比率）。"""
import json, collections

M = json.load(open('memory/mu_matrix_20261120_c1.json', encoding='utf-8'))
M18 = json.load(open('memory/mu_matrix_20261119_c1.json', encoding='utf-8'))
EB = json.load(open('memory/ptcgp_meta_20261120_std.json', encoding='utf-8'))['rows']
EB18 = json.load(open('memory/ptcgp_meta_20261119_std.json', encoding='utf-8'))['rows']
MIN_N = 50


def sig_branches(comb, rows=EB):
    cands = [r for r in rows if r['name'] == comb or r['name'].startswith(comb + ' ')]
    return [r['name'] for r in cands if r['n'] >= MIN_N] or [comb]


def merged(comb_a, comb_b, matrix=M, rows=EB):
    """comb_a 對 comb_b 的加權勝率（只併顯著分支）。"""
    opp_keys = set(sig_branches(comb_b, rows))
    tot = 0; acc = 0.0
    for rn in sig_branches(comb_a, rows):
        d = matrix.get(rn, {})
        for k, (w, n) in d.items():
            if k in opp_keys:
                acc += w * n; tot += n
    return (round(acc / tot, 1), tot) if tot else None


def merged_reverse(comb_a, comb_b):
    """comb_b 那一列的合併值 = comb_a 輸 comb_b 的比率。"""
    return merged(comb_b, comb_a)


PAIRS = [
    ('Magnezone','Vespiquen ex'),('Magnezone','Hoopa ex'),('Magnezone','Mega Altaria ex'),
    ('Magnezone','Mega Greninja ex'),('Magnezone','Suicune ex'),('Magnezone','Mega Lucario ex'),
    ('Magnezone','Hydreigon'),('Magnezone','Umbreon'),('Magnezone','Mega Charizard Y ex'),
    ('Hydreigon','Vespiquen ex'),('Hydreigon','Magnezone'),('Hydreigon','Mega Altaria ex'),
    ('Hydreigon','Hoopa ex'),('Hydreigon','Umbreon'),('Hydreigon','Mega Charizard Y ex'),
    ('Vespiquen ex','Hoopa ex'),('Vespiquen ex','Suicune ex'),('Vespiquen ex','Mega Altaria ex'),
    ('Vespiquen ex','Mega Mewtwo X ex'),('Vespiquen ex','Mega Lucario ex'),('Vespiquen ex','Magnezone'),
    ('Hoopa ex','Mega Altaria ex'),('Hoopa ex','Suicune ex'),('Hoopa ex','Mega Charizard Y ex'),
    ('Hoopa ex','Mega Mewtwo X ex'),('Hoopa ex','Mega Lucario ex'),('Hoopa ex','Mega Greninja ex'),
    ('Mega Altaria ex','Mega Lucario ex'),('Mega Altaria ex','Mega Mewtwo X ex'),
    ('Mega Altaria ex','Umbreon'),('Mega Altaria ex','Mega Charizard Y ex'),
    ('Mega Altaria ex','Suicune ex'),('Mega Altaria ex','Mega Greninja ex'),
    ('Mega Altaria ex','Vespiquen ex'),('Mega Altaria ex','Magnezone'),('Mega Altaria ex','Hoopa ex'),
    ('Suicune ex','Mega Greninja ex'),('Suicune ex','Mega Altaria ex'),('Suicune ex','Mega Charizard Y ex'),
    ('Suicune ex','Hoopa ex'),('Suicune ex','Magnezone'),('Suicune ex','Vespiquen ex'),
    ('Mega Charizard Y ex','Hoopa ex'),('Mega Charizard Y ex','Mega Altaria ex'),
    ('Mega Charizard Y ex','Mega Lucario ex'),('Mega Charizard Y ex','Suicune ex'),
    ('Mega Charizard Y ex','Mega Greninja ex'),('Mega Charizard Y ex','Mega Mewtwo X ex'),
    ('Mega Mewtwo X ex','Mega Altaria ex'),('Mega Mewtwo X ex','Hoopa ex'),
    ('Mega Mewtwo X ex','Magnezone'),('Mega Mewtwo X ex','Vespiquen ex'),
    ('Umbreon','Mega Altaria ex'),('Umbreon','Magnezone'),('Umbreon','Suicune ex'),
    ('Umbreon','Mega Greninja ex'),('Umbreon','Mega Mewtwo X ex'),('Umbreon','Hoopa ex'),
    ('Mega Greninja ex','Suicune ex'),('Mega Greninja ex','Magnezone'),('Mega Greninja ex','Mega Manectric ex'),
    ('Mega Greninja ex','Mega Altaria ex'),('Mega Greninja ex','Hoopa ex'),
    ('Mega Lucario ex','Mega Altaria ex'),('Mega Lucario ex','Magnezone'),('Mega Lucario ex','Hoopa ex'),
    ('Mega Lucario ex','Vespiquen ex'),
]
for a, b in PAIRS:
    cur = merged(a, b); rv = merged_reverse(a, b); p = merged(a, b, M18, EB18)
    cs = f"{cur[0]:>5.1f}% N={cur[1]:>4}" if cur else '   --    '
    rs = f"{rv[0]:>5.1f}% N={rv[1]:>4}" if rv else '   --    '
    ps = f"昨 {p[0]:>5.1f}% N={p[1]:>4}" if p else ''
    print(f"{a:22} vs {b:22}: {cs} | 反向 {b:22}->{a:20}: {rs} | {ps}")

print('\n### 顯著分支清單')
for comb in ['Mega Altaria ex','Mega Greninja ex','Umbreon','Mega Mewtwo X ex','Hoopa ex',
             'Vespiquen ex','Magnezone','Hydreigon','Suicune ex','Mega Charizard Y ex',
             'Mega Lucario ex','Chien Pao ex','Pikachu ex','Lopunny','Greninja']:
    print(f"  {comb:24} -> {sig_branches(comb)}")
