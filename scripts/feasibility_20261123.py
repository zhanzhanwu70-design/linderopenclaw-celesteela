#!/usr/bin/env python3
"""2026-11-23 份額條件可行性（副牌濃度模型）+ K 值校準 + 吸收濃度歷史。"""
import collections
import json
import statistics

SUF = {'20261123': '.json', '20261122': '.json', '20261121': '_re2.json',
       '20261120': '_re2.json', '20261119': '_re2.json'}
DAYS = ['20261119', '20261120', '20261121', '20261122', '20261123']


def agg(path):
    out = collections.defaultdict(lambda: {'share': 0.0, 'w': 0, 'l': 0, 'd': 0, 'n': 0, 'decks': 0})
    for r in json.load(open(path, encoding='utf-8'))['rows']:
        a = out[r['name']]
        for k in ('share', 'w', 'l', 'd', 'n', 'decks'):
            a[k] += r[k]
    res = []
    for n, a in out.items():
        a = dict(a)
        a['name'] = n
        a['awr'] = (a['w'] + 12) / (a['n'] + 25) * 100 if a['n'] else 0
        res.append(a)
    res.sort(key=lambda r: -r['share'])
    return res


AGG = {d: agg(f'memory/ptcgp_meta_{d}_std_comb{SUF[d]}') for d in DAYS}
T = {d: sum(r['decks'] for r in AGG[d]) for d in DAYS}
IDX = {d: {r['name']: r for r in AGG[d]} for d in DAYS}

print('### K 值校準（share% = K × 100 × D / T）')
for d in ['20261123', '20261122']:
    ks = []
    for r in AGG[d]:
        if r['decks'] >= 20 and r['n'] >= 200:
            ks.append(r['share'] / (100.0 * r['decks'] / T[d]))
    print(f"  {d}: T={T[d]}  K 中位 {statistics.median(ks):.4f}  平均 {statistics.mean(ks):.4f}  標準差 {statistics.pstdev(ks):.4f}  (n={len(ks)})")

K = 1.2457

print('\n### 單日吸收濃度歷史（占全環境當日新增副牌的比例）')
for i in range(1, len(DAYS)):
    d, p = DAYS[i], DAYS[i - 1]
    dT = T[d] - T[p]
    print(f"  {d}: ΔT={dT:+d}")
    conc = []
    for r in AGG[d]:
        if r['name'] in IDX[p] and r['decks'] >= 50:
            dv = r['decks'] - IDX[p][r['name']]['decks']
            if dT:
                conc.append((r['name'], dv, dv / dT * 100))
    conc.sort(key=lambda x: -x[2])
    for n, dv, c in conc[:6]:
        print(f"     {n[:26]:28} {dv:+4d} 副  濃度 {c:5.2f}%")
    med = statistics.median([c for n, dv, c in conc if dv > 0]) if any(c > 0 for n, dv, c in conc) else 0
    print(f"     （正吸收者濃度中位 {med:.2f}%）")

print('\n### 目標牌組吸收濃度歷史')
for nm in ['Mega Charizard Y ex', 'Mega Altaria ex', 'Hoopa ex', 'Umbreon', 'Suicune ex',
           'Mega Greninja ex', 'Mega Lucario ex', 'Vespiquen ex', 'Magnezone', 'Giratina ex',
           'Hydreigon', 'Mega Sceptile ex', 'Dedenne ex', 'Chien Pao ex', 'Mega Manectric ex',
           'Butterfree', 'Entei ex', 'Milotic ex', 'Mega Mewtwo X ex', 'Pikachu ex']:
    line = []
    for i in range(1, len(DAYS)):
        d, p = DAYS[i], DAYS[i - 1]
        dT = T[d] - T[p]
        cur = IDX[d].get(nm)
        prv = IDX[p].get(nm)
        if cur and prv and dT:
            dv = cur['decks'] - prv['decks']
            line.append(f"{d[4:6]}-{d[6:8]} {dv:+4d}副/{dv/dT*100:5.2f}%")
    cur = IDX['20261123'].get(nm)
    print(f"  {nm[:24]:26} D={cur['decks'] if cur else '-':>4} 份額 {cur['share'] if cur else 0:7.4f}% | " + ' | '.join(line))

print('\n### 檢查日增量情境（11-23 → 11-25 兩日）')
T0 = T['20261123']
SCEN = [('保守', 1200, 520), ('中央', 2200, 1000), ('積極', 3200, 1420)]
for lab, dm, dl in SCEN:
    print(f'  {lab}: 對局 +{dm}  副牌 +{dl}  T1={T0+dl}  稀釋 {T0/(T0+dl)*100:.4f}%')


def show(name, target, dl, kind='share'):
    r = IDX['20261123'][name]
    T1 = T0 + dl
    if kind == 'share':
        D1 = target / 100 * T1 / K
        dd = D1 - r['decks']
        s0 = K * 100 * r['decks'] / T1
        print(f"  {name[:24]:26} 門檻 {target:6.2f}%  現值 {r['share']:7.4f}%  距離 {target-r['share']:+.4f}pt"
              f" | 需副牌 {dd:+7.1f}（ΔT={dl} 的 {dd/dl*100 if dl else 0:5.2f}%）| dD=0 時份額 {s0:7.4f}%")
    else:
        se = (r['awr'] / 100 * (1 - r['awr'] / 100) / r['n']) ** 0.5 * 100
        print(f"  {name[:24]:26} 門檻 AWR {target:6.2f}%  現值 {r['awr']:7.4f}%  距離 {target-r['awr']:+.4f}pt  N={r['n']} 1σ={se:.2f}pt")


CANDS = [
    ('Vespiquen ex', [5.45, 5.55, 5.65], 'share'),
    ('Mega Lucario ex', [6.10, 6.20, 6.30], 'share'),
    ('Dedenne ex', [1.28, 1.32, 1.35], 'share'),
    ('Chien Pao ex', [1.28, 1.32, 1.35], 'share'),
    ('Mega Manectric ex', [3.15, 3.10, 3.05], 'share'),
    ('Giratina ex', [4.10, 4.05, 4.00], 'share'),
    ('Mega Altaria ex', [10.30, 10.40, 10.50], 'share'),
    ('Mega Altaria ex', [53.80, 53.90, 54.00], 'AWR'),
    ('Vespiquen ex', [52.70, 52.50, 52.30], 'AWR'),
    ('Mega Manectric ex', [50.10, 49.90, 49.70], 'AWR'),
    ('Mega Sceptile ex', [49.20, 49.00, 48.80], 'AWR'),
    ('Chien Pao ex', [47.50, 47.20, 47.00], 'AWR'),
    ('Milotic ex', [0.95, 1.00, 1.05], 'share'),
    ('Entei ex', [0.80, 0.85, 0.90], 'share'),
]
for lab, dm, dl in SCEN:
    print(f'\n=== 情境：{lab}（副牌 +{dl}）===')
    for name, targets, kind in CANDS:
        for tg in targets:
            show(name, tg, dl, kind)
        print()
