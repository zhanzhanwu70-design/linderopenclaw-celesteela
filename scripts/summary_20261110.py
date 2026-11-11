#!/usr/bin/env python3
"""2026-11-10 合併口徑彙總：同名牌組合併、份額榜、AWR 榜、五日變化。"""
import collections
import json

D = json.load(open('ptcgp_deck_dictionary.json'))
DN = D['deck_names']; CN = D['card_names']


def zh(n):
    return DN.get(n) or CN.get(n) or n


def agg(path):
    out = collections.OrderedDict()
    for r in json.load(open(path))['rows']:
        k = zh(r['name'])
        o = out.setdefault(k, {'share': 0.0, 'decks': 0, 'w': 0, 'l': 0, 'd': 0, 'n': 0, 'slugs': []})
        for f in ('share', 'decks', 'w', 'l', 'd', 'n'):
            o[f] += r[f]
        o['slugs'].append(r['slug'])
    for o in out.values():
        o['share'] = round(o['share'], 4)
        o['awr'] = round((o['w'] + 12) / (o['n'] + 25) * 100, 2) if o['n'] else 0
    return out


FILES = {
    '11-06': 'memory/ptcgp_meta_20261106_std_comb_re.json',
    '11-07': 'memory/ptcgp_meta_20261107_std_comb_re.json',
    '11-08': 'memory/ptcgp_meta_20261108_std_comb_re.json',
    '11-09': 'memory/ptcgp_meta_20261109_std_comb.json',
    '11-10': 'memory/ptcgp_meta_20261110_std_comb.json',
}
A = {d: agg(p) for d, p in FILES.items()}
T = A['11-10']; Y = A['11-09']

print('### 合併份額前五（同名合併）')
for k, o in sorted(T.items(), key=lambda kv: -kv[1]['share'])[:5]:
    print(f"{k:24} 份額 {o['share']:>6.2f}%  牌組數 {o['decks']:>4}  AWR {o['awr']:>6.2f}%  {o['w']}-{o['l']}-{o['d']}  N={o['n']}")
print('\n### AWR 前五（N>=100，同名合併）')
for k, o in sorted([(k, o) for k, o in T.items() if o['n'] >= 100], key=lambda kv: -kv[1]['awr'])[:8]:
    print(f"{k:24} AWR {o['awr']:>6.2f}%  份額 {o['share']:>6.2f}%  牌組數 {o['decks']:>4}  {o['w']}-{o['l']}-{o['d']}  N={o['n']}")
print('\n### 主要牌組五日軌跡（份額/AWR/N）')
names = ['超級噴火龍Yex', '月亮伊布', '超級甲賀忍蛙ex', '水君ex', '超級七夕青鳥ex', '胡帕ex', '蜂女王ex', '騎拉帝納ex', '超級路卡利歐 ex', '自爆磁怪', '三首惡龍', '超級雷電獸ex', '超級蜥蜴王ex']
for k in names:
    print(k, end=': ')
    for d in FILES:
        o = A[d].get(k)
        print(f"{d} {o['share']:.2f}/{o['awr']:.2f}/{o['n']}" if o else f'{d} --', end=' | ')
    print()
print('\n### 今日 vs 11-09 變化（同名牌合併，N>=100）')
rows = []
for k, o in T.items():
    y = Y.get(k)
    if not y or o['n'] < 100 or y['n'] < 100:
        continue
    rows.append((k, o['share'] - y['share'], o['awr'] - y['awr'], o['n'], o['share'], o['awr'], y['share'], y['awr']))
print('  份額升幅前 10：')
for r in sorted(rows, key=lambda x: -x[1])[:10]:
    print(f"    {r[0]:24} 份額 {r[7]:>5.2f}%→{r[4]:>5.2f}% ({r[1]:+.2f}pt)  AWR {r[7+0-1]:.2f}→{r[5]:.2f}% ({r[2]:+.2f}pt) N={r[3]}")
print('  AWR 升幅前 10：')
for r in sorted(rows, key=lambda x: -x[2])[:10]:
    print(f"    {r[0]:24} AWR {r[7]:.2f}%→{r[5]:.2f}% ({r[2]:+.2f}pt)  份額 {r[7]:.2f}→{r[4]:.2f}% ({r[1]:+.2f}pt) N={r[3]}")
print('  AWR 降幅前 10：')
for r in sorted(rows, key=lambda x: x[2])[:10]:
    print(f"    {r[0]:24} AWR {r[7]:.2f}%→{r[5]:.2f}% ({r[2]:+.2f}pt)  份額 {r[7]:.2f}→{r[4]:.2f}% ({r[1]:+.2f}pt) N={r[3]}")
print('\n### 份額與 AWR 同升／同降（門檻：份額 ±0.3pt、AWR ±0.5pt）')
for k, o in T.items():
    y = Y.get(k)
    if not y or o['n'] < 100 or y['n'] < 100:
        continue
    ds = o['share'] - y['share']; da = o['awr'] - y['awr']
    if ds >= 0.3 and da >= 0.5:
        print(f"  同升 {k:24} 份額 {ds:+.2f}pt AWR {da:+.2f}pt N={o['n']}")
    if ds <= -0.3 and da <= -0.5:
        print(f"  同降 {k:24} 份額 {ds:+.2f}pt AWR {da:+.2f}pt N={o['n']}")
