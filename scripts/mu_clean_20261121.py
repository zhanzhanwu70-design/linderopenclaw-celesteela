#!/usr/bin/env python3
"""2026-11-21 對位「乾淨合併」：只併入顯著分支（分支 N>=50）。"""
import json, collections

M = json.load(open('memory/mu_matrix_20261121_c1.json', encoding='utf-8'))
M20 = json.load(open('memory/mu_matrix_20261120_c1.json', encoding='utf-8'))
EB = json.load(open('memory/ptcgp_meta_20261121_std.json', encoding='utf-8'))['rows']
EB20 = json.load(open('memory/ptcgp_meta_20261120_std_re.json', encoding='utf-8'))['rows']
MIN_N = 50


def sig_branches(comb, rows=EB):
    cands = [r for r in rows if r['name'] == comb or r['name'].startswith(comb + ' ')]
    return [r['name'] for r in cands if r['n'] >= MIN_N] or [comb]


def merged(comb_a, comb_b, matrix=M, rows=EB):
    opp_keys = set(sig_branches(comb_b, rows))
    tot = 0; acc = 0.0
    for rn in sig_branches(comb_a, rows):
        d = matrix.get(rn, {})
        for k, (w, n) in d.items():
            if k in opp_keys:
                acc += w * n; tot += n
    return (round(acc / tot, 1), tot) if tot else None


def merged_reverse(comb_a, comb_b, matrix=M, rows=EB):
    return merged(comb_b, comb_a, matrix, rows)


PAIRS = []
KEYS = ['Magnezone','Hydreigon','Vespiquen ex','Hoopa ex','Mega Altaria ex','Suicune ex',
        'Mega Charizard Y ex','Mega Lucario ex','Mega Greninja ex','Mega Mewtwo X ex',
        'Umbreon','Mega Manectric ex','Greninja ex','Mega Sceptile ex','Mega Skarmory ex',
        'Pikachu ex','Lopunny','Chien Pao ex','Mega Mewtwo Y ex','Dondozo ex','Arceus ex']
for a in KEYS:
    for b in KEYS:
        if a != b:
            PAIRS.append((a, b))

for a, b in PAIRS:
    cur = merged(a, b); rv = merged_reverse(a, b); p = merged(a, b, M20, EB20)
    if not cur and not rv:
        continue
    cs = f"{cur[0]:>5.1f}% N={cur[1]:>4}" if cur else '   --    '
    rs = f"{rv[0]:>5.1f}% N={rv[1]:>4}" if rv else '   --    '
    ps = f"昨 {p[0]:>5.1f}% N={p[1]:>4}" if p else ''
    print(f"{a:22} vs {b:22}: {cs} | 反向 {b:22}->{a:20}: {rs} | {ps}")

print('\n### 顯著分支清單')
for comb in KEYS:
    print(f"  {comb:24} -> {sig_branches(comb)}")
