#!/usr/bin/env python3
"""2026-11-16 對位重點抽取 + 與 11-15 對比。
口徑：每列數值＝被檢視的那副牌自己對該對手的勝率（禁止 100 − 自身勝率 反推）。
合併口徑＝該合併牌組所有分支列依對局數加權合併。"""
import json, collections

M = json.load(open('memory/mu_matrix_20261116_c1.json', encoding='utf-8'))
M15 = json.load(open('memory/mu_matrix_20261115_c1.json', encoding='utf-8'))
EB = json.load(open('memory/ptcgp_meta_20261116_std.json', encoding='utf-8'))['rows']
E = json.load(open('memory/ptcgp_meta_20261116_std_comb.json', encoding='utf-8'))['rows']

# 合併名 -> 分支列（分支頁列名以合併名 + ' ' 開頭）
BR = collections.defaultdict(list)
for r in EB:
    BR[r['name']].append(r['name'])


def branches(comb):
    cands = [r['name'] for r in EB if r['name'] == comb or r['name'].startswith(comb + ' ')]
    return cands or [comb]


def opp_names(comb):
    """對手合併名在對位頁上可能以合併名或分支名出現 → 展開成比對用的鍵集合。"""
    out = set([comb])
    out |= set(branches(comb))
    return out


def agg_row(matrix, comb, opp_comb):
    """在 matrix 中把 comb 的所有分支列對 opp_comb 的對局加權合併。"""
    tot = 0; acc = 0.0
    keys = opp_names(opp_comb)
    for rn in branches(comb):
        d = matrix.get(rn, {})
        for k, (w, n) in d.items():
            if k in keys:
                acc += w * n; tot += n
    return [round(acc / tot, 1), tot] if tot else None


def fmt(v, p):
    if v is None: return '   --    '
    s = f"{v[0]:>5.1f}% N={v[1]:>4}"
    if p is not None and p[1] >= 20:
        s += f" (昨 {p[0]:>5.1f}% N={p[1]:>4}, Δ{v[0]-p[0]:+.1f})"
    return s


def show(a, b):
    va = agg_row(M, a, b); vb = agg_row(M, b, a)
    pa = agg_row(M15, a, b); pb = agg_row(M15, b, a)
    print(f"  {a:22} vs {b:22}: {fmt(va,pa)}  |  反向 {b}→{a}: {fmt(vb,pb)}")


PAIRS = [
    ('Magnezone', 'Mega Altaria ex'), ('Magnezone', 'Mega Lucario ex'), ('Magnezone', 'Mega Charizard Y ex'),
    ('Magnezone', 'Suicune ex'), ('Magnezone', 'Vespiquen ex'), ('Magnezone', 'Hoopa ex'),
    ('Magnezone', 'Mega Greninja ex'), ('Magnezone', 'Hydreigon'), ('Magnezone', 'Umbreon'),
    ('Mega Altaria ex', 'Mega Lucario ex'), ('Mega Altaria ex', 'Hoopa ex'),
    ('Mega Altaria ex', 'Mega Greninja ex'), ('Mega Altaria ex', 'Suicune ex'),
    ('Mega Altaria ex', 'Mega Charizard Y ex'), ('Mega Altaria ex', 'Magnezone'),
    ('Mega Altaria ex', 'Vespiquen ex'), ('Mega Altaria ex', 'Umbreon'),
    ('Mega Greninja ex', 'Vespiquen ex'), ('Mega Greninja ex', 'Magnezone'),
    ('Mega Greninja ex', 'Mega Manectric ex'), ('Mega Greninja ex', 'Suicune ex'),
    ('Mega Greninja ex', 'Umbreon'), ('Mega Greninja ex', 'Mega Altaria ex'),
    ('Mega Lucario ex', 'Mega Charizard Y ex'), ('Mega Lucario ex', 'Magnezone'),
    ('Mega Lucario ex', 'Mega Altaria ex'), ('Mega Lucario ex', 'Hoopa ex'),
    ('Hoopa ex', 'Mega Charizard Y ex'), ('Hoopa ex', 'Suicune ex'),
    ('Hoopa ex', 'Vespiquen ex'), ('Hoopa ex', 'Mega Lucario ex'), ('Hoopa ex', 'Mega Altaria ex'),
    ('Vespiquen ex', 'Magnezone'), ('Vespiquen ex', 'Hoopa ex'), ('Vespiquen ex', 'Mega Altaria ex'),
    ('Mega Charizard Y ex', 'Magnezone'), ('Mega Charizard Y ex', 'Mega Lucario ex'),
    ('Mega Charizard Y ex', 'Mega Altaria ex'),
    ('Suicune ex', 'Mega Greninja ex'), ('Suicune ex', 'Hoopa ex'), ('Suicune ex', 'Mega Altaria ex'),
    ('Mega Mewtwo X ex', 'Hoopa ex'), ('Mega Mewtwo X ex', 'Mega Altaria ex'),
    ('Mega Sceptile ex', 'Mega Manectric ex'), ('Mega Sceptile ex', 'Mega Charizard Y ex'),
    ('Pikachu ex', 'Magnezone'), ('Pikachu ex', 'Hoopa ex'), ('Pikachu ex', 'Mega Altaria ex'),
    ('Umbreon', 'Mega Altaria ex'), ('Umbreon', 'Mega Greninja ex'),
]
print('### 今日重點對位（合併口徑加權合併）')
for a, b in PAIRS:
    show(a, b)

print()
print('### 各重點牌組的關鍵劣勢線（合併口徑，N>=25）')
for me in ['Magnezone', 'Mega Altaria ex', 'Vespiquen ex', 'Hoopa ex', 'Mega Greninja ex',
           'Mega Charizard Y ex', 'Suicune ex', 'Mega Lucario ex']:
    aggmap = collections.defaultdict(lambda: [0.0, 0])
    for rn in branches(me):
        for o, (w, n) in M.get(rn, {}).items():
            aggmap[o][0] += w * n; aggmap[o][1] += n
    print(f'-- {me}')
    for o, (acc, n) in sorted(aggmap.items(), key=lambda x: x[1][0] / x[1][1])[:7]:
        if n >= 25:
            p = agg_row(M15, me, o)
            extra = f" (昨 {p[0]:.1f}% N={p[1]})" if p else ''
            print(f'     vs {o[:44]:46} {acc/n:>5.1f}% N={n}{extra}')
