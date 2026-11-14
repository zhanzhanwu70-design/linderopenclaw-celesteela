#!/usr/bin/env python3
"""2026-11-13 合併口徑彙總：同名牌組合併、份額榜、AWR 榜、三日變化。"""
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
    '11-09': 'memory/ptcgp_meta_20261109_std_comb_re.json',
    '11-10': 'memory/ptcgp_meta_20261110_std_comb_re.json',
    '11-11': 'memory/ptcgp_meta_20261111_std_comb_re.json',
    '11-12': 'memory/ptcgp_meta_20261112_std_comb_re.json',
    '11-13': 'memory/ptcgp_meta_20261113_std_comb.json',
}
A = {d: agg(p) for d, p in FILES.items()}
T = A['11-13']; Y = A['11-12']; Y2 = A['11-11']

# 全環境加權 AWR
for d in FILES:
    w = sum(o['w'] for o in A[d].values()); n = sum(o['n'] for o in A[d].values())
    print(f"全環境 AWR {d}: {(w+12)/(n+25)*100:.2f}%  N={n}  branches={len(json.load(open(FILES[d]))['rows'])}  merged={len(A[d])}")
print()

print('### 合併份額前五（同名合併）')
for k, o in sorted(T.items(), key=lambda kv: -kv[1]['share'])[:8]:
    print(f"{k:24} 份額 {o['share']:>6.2f}%  牌組數 {o['decks']:>4}  AWR {o['awr']:>6.2f}%  {o['w']}-{o['l']}-{o['d']}  N={o['n']}")
print('\n### AWR 前十（N>=100，同名合併）')
for k, o in sorted([(k, o) for k, o in T.items() if o['n'] >= 100], key=lambda kv: -kv[1]['awr'])[:12]:
    print(f"{k:24} AWR {o['awr']:>6.2f}%  份額 {o['share']:>6.2f}%  牌組數 {o['decks']:>4}  {o['w']}-{o['l']}-{o['d']}  N={o['n']}")
print('\n### 主要牌組軌跡（份額/AWR/N）')
names = ['超級噴火龍Yex', '月亮伊布', '超級甲賀忍蛙ex', '水君ex', '超級七夕青鳥ex', '胡帕ex', '蜂女王ex', '騎拉帝納ex', '超級路卡利歐 ex', '自爆磁怪', '三首惡龍', '超級雷電獸ex', '超級蜥蜴王ex', '密勒頓ex', '超級超夢Xex', '超級阿勃梭魯ex', '咚咚鼠', '皮卡丘ex']
for k in names:
    print(k, end=': ')
    for d in FILES:
        o = A[d].get(k)
        print(f"{d} {o['share']:.2f}/{o['awr']:.2f}/{o['n']}" if o else f'{d} --', end=' | ')
    print()
print('\n### 今日 vs 11-12 變化（同名牌合併，N>=100）')
rows = []
for k, o in T.items():
    y = Y.get(k)
    if not y or o['n'] < 100 or y['n'] < 100:
        continue
    rows.append((k, o['share'] - y['share'], o['awr'] - y['awr'], o['n'], o['share'], o['awr'], y['share'], y['awr']))
print('  份額升幅前 10：')
for r in sorted(rows, key=lambda x: -x[1])[:10]:
    print(f"    {r[0]:24} 份額 {r[6]:>5.2f}%→{r[4]:>5.2f}% ({r[1]:+.2f}pt)  AWR {r[7]:.2f}→{r[5]:.2f}% ({r[2]:+.2f}pt) N={r[3]}")
print('  AWR 升幅前 10：')
for r in sorted(rows, key=lambda x: -x[2])[:10]:
    print(f"    {r[0]:24} AWR {r[7]:.2f}%→{r[5]:.2f}% ({r[2]:+.2f}pt)  份額 {r[6]:.2f}→{r[4]:.2f}% ({r[1]:+.2f}pt) N={r[3]}")
print('  AWR 降幅前 10：')
for r in sorted(rows, key=lambda x: x[2])[:10]:
    print(f"    {r[0]:24} AWR {r[7]:.2f}%→{r[5]:.2f}% ({r[2]:+.2f}pt)  份額 {r[6]:.2f}→{r[4]:.2f}% ({r[1]:+.2f}pt) N={r[3]}")
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
print('\n### 今日新進榜合併項（份額 >=0.15%）')
prev = set(Y.keys())
for k, o in sorted(T.items(), key=lambda kv: -kv[1]['share']):
    if k not in prev and o['share'] >= 0.15:
        print(f"  新進 {k:28} 份額 {o['share']:.2f}% AWR {o['awr']:.2f}% N={o['n']}")
print('\n### 退出合併榜（11-12 有份額 >=0.15%，今日低於）')
for k, o in sorted(Y.items(), key=lambda kv: -kv[1]['share']):
    t = T.get(k)
    if o['share'] >= 0.15 and (not t or t['share'] < 0.15):
        print(f"  退出 {k:28} 昨份額 {o['share']:.2f}% AWR {o['awr']:.2f}%")
print('\n### N 佔全環境比重（前 25 名）')
tot_n = sum(o['n'] for o in T.values())
for k, o in sorted(T.items(), key=lambda kv: -kv[1]['share'])[:25]:
    print(f"  {k:26} 份額 {o['share']:>6.2f}%  N {o['n']:>6}  N佔比 {o['n']/tot_n*100:>6.2f}%  AWR {o['awr']:.2f}%")
print('\n### 最差榜（合併口徑，N>=50）')
for k, o in sorted([(k, o) for k, o in T.items() if o['n'] >= 50], key=lambda kv: kv[1]['awr'])[:15]:
    print(f"  {k:26} AWR {o['awr']:.2f}%  份額 {o['share']:.2f}%  N={o['n']}  {o['w']}-{o['l']}-{o['d']}")
print('\n### 陷阱（份額 >=1.2% 且 AWR < 大盤-3pt）')
big = (sum(o['w'] for o in T.values())+12)/(sum(o['n'] for o in T.values())+25)*100
for k, o in sorted(T.items(), key=lambda kv: -kv[1]['share']):
    if o['share'] >= 1.2 and o['awr'] < big - 3 and o['n'] >= 100:
        print(f"  {k:26} 份額 {o['share']:.2f}%  AWR {o['awr']:.2f}% (大盤 {big:.2f}, 差 {o['awr']-big:+.2f}pt)  N={o['n']}")
