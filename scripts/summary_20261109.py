#!/usr/bin/env python3
"""2026-11-09 合併口徑彙總：同名牌組合併、份額榜、AWR 榜、三日變化。"""
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
}
A = {d: agg(p) for d, p in FILES.items()}
T = A['11-09']; Y = A['11-08']

print('### 合併份額前五（同名合併）')
for k, o in sorted(T.items(), key=lambda kv: -kv[1]['share'])[:5]:
    print(f"{k:24} 份額 {o['share']:>6.2f}%  牌組數 {o['decks']:>4}  AWR {o['awr']:>6.2f}%  {o['w']}-{o['l']}-{o['d']}  N={o['n']}")
print('\n### AWR 前五（N>=100，同名合併）')
for k, o in sorted([(k, o) for k, o in T.items() if o['n'] >= 100], key=lambda kv: -kv[1]['awr'])[:5]:
    print(f"{k:24} AWR {o['awr']:>6.2f}%  份額 {o['share']:>6.2f}%  牌組數 {o['decks']:>4}  {o['w']}-{o['l']}-{o['d']}  N={o['n']}")
print('\n### 主要牌組四日軌跡')
names = ['超級噴火龍Yex','月亮伊布','超級甲賀忍蛙ex','水君ex','超級七夕青鳥ex','胡帕ex','蜂女王ex','騎拉帝納ex','超級路卡利歐 ex','自爆磁怪','三首惡龍','超級雷電獸ex']
for k in names:
    print(k, end=': ')
    for d in FILES:
        o = A[d].get(k)
        print(f"{d} {o['share']:.2f}/{o['awr']:.2f}/{o['n']}" if o else f'{d} --', end=' | ')
    print()
print('\n### 份額與 AWR 同升／同降（N>=100）')
for k, o in T.items():
    y = Y.get(k)
    if not y or o['n'] < 100 or y['n'] < 100: continue
    ds = o['share'] - y['share']; da = o['awr'] - y['awr']
    if ds >= 0.4 and da >= 0.5:
        print(f"  同升 {k:24} 份額 {ds:+.2f}pt AWR {da:+.2f}pt N={o['n']}")
    if ds <= -0.4 and da <= -0.5:
        print(f"  同降 {k:24} 份額 {ds:+.2f}pt AWR {da:+.2f}pt N={o['n']}")
