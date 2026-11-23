#!/usr/bin/env python3
"""2026-11-22 份額條件可行性計算（以副牌數為單位；K 由實測校準）。"""
import collections
import json

K = 1.2380  # share% = K * 100 * D / T


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


T = json.load(open('memory/ptcgp_meta_20261122_std_comb.json', encoding='utf-8'))['rows']
T0 = sum(r['decks'] for r in T)
D = {r['name']: r for r in agg('memory/ptcgp_meta_20261122_std_comb.json')}
D21 = {r['name']: r for r in agg('memory/ptcgp_meta_20261121_std_comb_re2.json')}
D20 = {r['name']: r for r in agg('memory/ptcgp_meta_20261120_std_comb_re2.json')}
D19 = {r['name']: r for r in agg('memory/ptcgp_meta_20261119_std_comb_re2.json')}
N0 = sum(r['n'] for r in agg('memory/ptcgp_meta_20261122_std_comb.json'))

print(f'環境基準：總副牌 T0={T0}  總對局 N={N0}')
print('K 校準抽查：')
for nm in ['Mega Greninja ex', 'Magnezone', 'Mega Charizard Y ex', 'Umbreon']:
    r = D[nm]
    print(f"  {nm:24} 實測 share {r['share']:8.4f}%  模型 {K*100*r['decks']/T0:8.4f}%")

print()
print('=== 檢查日增量情境（11-22 → 11-24 兩日累計）===')
scen = [('保守', 1200, 480), ('中央', 1800, 720), ('積極', 2800, 1120)]
for lab, dm, dl in scen:
    print(f'  {lab}: 對局 +{dm}  副牌 +{dl}  → T1={T0+dl}  稀釋因子 {T0/(T0+dl)*100:.4f}%')


def need(name, target, dl, mode):
    """回傳達到目標份額所需的副牌增減量（正=需吸收）。"""
    r = D[name]
    T1 = T0 + dl
    D1 = target / 100 * T1 / K
    return D1 - r['decks'], D1


def show(name, target, dl, tag=''):
    r = D[name]
    T1 = T0 + dl
    D1 = target / 100 * T1 / K
    dd = D1 - r['decks']
    # dD=0 時的份額
    s0 = K * 100 * r['decks'] / T1
    print(f"  {name[:26]:28} 門檻 {target:6.2f}%  現值 {r['share']:7.4f}%  距離 {target-r['share']:+.4f}pt"
          f" | 需吸收副牌 {dd:+7.1f} 副（環境 +{dl} 的 {abs(dd)/dl*100 if dl else 0:5.1f}%）"
          f" | dD=0 時份額 {s0:7.4f}%")


CANDS = [
    ('Magnezone', [54.00, 53.80, 53.60, 53.40], 'AWR'),
    ('Hydreigon', [2.80, 2.85, 2.90], 'share'),
    ('Dedenne ex', [1.10, 1.12, 1.15], 'share'),
    ('Mega Sceptile ex', [2.60, 2.55, 2.50], 'share'),
    ('Vespiquen ex', [52.90, 52.70, 52.50], 'AWR'),
    ('Mega Manectric ex', [50.30, 50.20, 50.00], 'AWR'),
    ('Miraidon ex', [51.00, 51.20], 'AWR'),
    ('Butterfree', [0.80, 0.85, 0.90], 'share'),
    ('Lopunny', [1.58, 1.60, 1.65], 'share'),
    ('Chien Pao ex', [1.15, 1.20], 'share'),
    ('Mega Lucario ex', [5.90, 6.00], 'share'),
    ('Mega Mewtwo X ex', [48.50, 48.80], 'AWR'),
    ('Giratina ex', [49.50, 49.40], 'AWR'),
]

for lab, dm, dl in scen:
    print(f'\n=== 增量情境：{lab}（副牌 +{dl}）===')
    for name, targets, kind in CANDS:
        for tg in targets:
            if kind == 'share':
                show(name, tg, dl)
            else:
                r = D[name]
                print(f"  {name[:26]:28} 門檻 AWR {tg:6.2f}%  現值 {r['awr']:7.4f}%  距離 {tg-r['awr']:+.4f}pt  (N={r['n']})")
        print()
