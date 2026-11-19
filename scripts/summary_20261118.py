#!/usr/bin/env python3
"""2026-11-18 PTCGP Meta 摘要：合併頁同名加總、調整後勝率、三日比較、新舊卡與進榜變化。"""
import collections
import json

D = json.load(open('ptcgp_deck_dictionary.json', encoding='utf-8'))
DN = D['deck_names']
CN = D['card_names']


def zh(n):
    return DN.get(n) or CN.get(n) or n


def agg_rows(rows):
    out = collections.defaultdict(lambda: {'share': 0.0, 'w': 0, 'l': 0, 'd': 0, 'n': 0, 'decks': 0, 'slugs': []})
    for r in rows:
        a = out[r['name']]
        a['share'] += r['share']
        a['w'] += r['w']
        a['l'] += r['l']
        a['d'] += r['d']
        a['n'] += r['n']
        a['decks'] += r['decks']
        a['slugs'].append(r['slug'])
    result = []
    for name, a in out.items():
        a = dict(a)
        a['name'] = name
        a['awr'] = (a['w'] + 12) / (a['n'] + 25) * 100 if a['n'] else 0.0
        a['raw_wr'] = a['w'] / a['n'] * 100 if a['n'] else 0.0
        result.append(a)
    result.sort(key=lambda r: -r['share'])
    return result


def load(day, combined=True):
    kind = 'std_comb' if combined else 'std'
    suffix = '.json' if day == '20261118' else '_re.json'
    data = json.load(open(f'memory/ptcgp_meta_{day}_{kind}{suffix}', encoding='utf-8'))
    return data['header'], agg_rows(data['rows']) if combined else data['rows']


def index(rows):
    return {r['name']: r for r in rows}


H, T = load('20261118', True)
_, TB = load('20261118', False)
H1, Y = load('20261117', True)
H2, Y2 = load('20261116', True)
H3, Y3 = load('20261115', True)
IT, IY, IY2, IY3 = index(T), index(Y), index(Y2), index(Y3)

print('### 環境')
print(H, 'branch_rows', len(TB), 'combined_rows', len(T))
print('前一日', H1, '前二日', H2, '前三日', H3)
print(f"增量 tournaments {H['tournaments']-H1['tournaments']:+d} players {H['players']-H1['players']:+d} matches {H['matches']-H1['matches']:+d} ({(H['matches']/H1['matches']-1)*100:+.2f}%)")

print('\n### 合併份額前 20')
for i, r in enumerate(T[:20], 1):
    y = IY.get(r['name'])
    d = f"Δshare {r['share']-y['share']:+.4f}pt Δawr {r['awr']-y['awr']:+.4f}pt" if y else 'NEW'
    print(f"{i:2}. {zh(r['name'])[:30]:32} {r['share']:8.4f}% AWR {r['awr']:8.4f}% 副 {r['decks']:4} N {r['n']:5} {r['w']}-{r['l']}-{r['d']} | {d}")

print('\n### AWR 前 20（合併口徑，N>=100）')
for i, r in enumerate(sorted([x for x in T if x['n'] >= 100], key=lambda x: -x['awr'])[:20], 1):
    y = IY.get(r['name'])
    print(f"{i:2}. {zh(r['name'])[:30]:32} AWR {r['awr']:8.4f}% 份額 {r['share']:7.4f}% N {r['n']:5} | 昨 {y['awr'] if y else 0:8.4f}%")

print('\n### 最差 20（N>=50）')
for r in sorted([x for x in T if x['n'] >= 50], key=lambda x: x['awr'])[:20]:
    print(f"  {zh(r['name'])[:32]:34} {r['awr']:8.4f}% 份額 {r['share']:7.4f}% N={r['n']}")

print('\n### 四日關鍵趨勢（合併同名加總）')
keys = ['Mega Charizard Y ex', 'Umbreon', 'Mega Altaria ex', 'Suicune ex', 'Mega Greninja ex',
        'Hoopa ex', 'Mega Lucario ex', 'Mega Mewtwo X ex', 'Vespiquen ex', 'Magnezone',
        'Giratina ex', 'Mega Manectric ex', 'Mega Sceptile ex', 'Hydreigon', 'Pikachu ex',
        'Chien Pao ex', 'Greninja ex', 'Greninja', 'Mega Skarmory ex', 'Mega Blaziken ex',
        'Lopunny', 'Miraidon ex', 'Alolan Exeggutor ex', 'Dragonair', 'Mega Dragonite ex',
        'Absol ex', 'Mega Bouffalant ex', 'Pidgeot ex', 'Arceus ex', 'Rampardos ex']
for name in keys:
    t, y, y2, y3 = IT.get(name), IY.get(name), IY2.get(name), IY3.get(name)
    def fmt(r): return f"{r['share']:7.4f}%/{r['awr']:8.4f}% N={r['n']}" if r else ' -- '
    print(f"{zh(name)[:30]:32} 今 {fmt(t)} | 昨 {fmt(y)} | 前 {fmt(y2)} | 前3 {fmt(y3)}")

print('\n### 分支口徑前 30')
for i, r in enumerate(TB[:30], 1):
    print(f"{i:2}. {zh(r['name'])[:34]:36} {r['share']:7.4f}% AWR {r['awr']:8.4f}% N {r['n']:5} {r['w']}-{r['l']}-{r['d']}")

print('\n### 分支 AWR 前 15（N>=100）')
for i, r in enumerate(sorted([x for x in TB if x['n'] >= 100], key=lambda x: -x['awr'])[:15], 1):
    print(f"{i:2}. {zh(r['name'])[:34]:36} AWR {r['awr']:8.4f}% 份額 {r['share']:7.4f}% N {r['n']:5}")

# 新舊卡
cards = json.load(open('memory/ptcgp_cards_full.json', encoding='utf-8'))
C1N = {c.get('name') for k, c in cards.items() if k.startswith('C1_') and c.get('name')}


def has_c1(name):
    n = name.replace('’', "'")
    return any(n.startswith(c.replace('’', "'")) or n.startswith(c.replace('’', "'").replace(' ex', 'ex')) for c in C1N)


print('\n### 新舊卡差距（合併口徑）')
for label, rows in [('11-15', Y3), ('11-16', Y2), ('11-17', Y), ('11-18', T)]:
    a = [r for r in rows if has_c1(r['name'])]
    b = [r for r in rows if not has_c1(r['name'])]

    def stat(g):
        s = sum(r['share'] for r in g)
        w = sum(r['w'] for r in g)
        n = sum(r['n'] for r in g)
        return s, (w + 12) / (n + 25) * 100 if n else 0, n

    sa, aa, na = stat(a)
    sb, ab, nb = stat(b)
    print(f"{label}: 含新卡 {sa:.4f}%/{aa:.4f}% N={na} | 不含 {sb:.4f}%/{ab:.4f}% N={nb} | 差距 {ab-aa:.4f}pt")

print('\n### 合併頁新進榜（份額 >=0.15%）與退出前 40')
old_names = set(IY)
for r in T:
    if r['name'] not in old_names and r['share'] >= 0.15:
        print(' 新', zh(r['name'])[:32], f"{r['share']:.4f}%/{r['awr']:.4f}% N={r['n']}")
cur40 = {r['name'] for r in T[:40]}
for r in Y[:40]:
    if r['name'] not in cur40:
        print(' 退', zh(r['name'])[:32], f"昨 {r['share']:.4f}%/{r['awr']:.4f}%")

print('\n### 全環境')
w = sum(r['w'] for r in T)
n = sum(r['n'] for r in T)
wy = sum(r['w'] for r in Y)
ny = sum(r['n'] for r in Y)
print(f"AWR {(w+12)/(n+25)*100:.4f}% N={n} | 昨 {(wy+12)/(ny+25)*100:.4f}% N={ny} | Δ{((w+12)/(n+25)-(wy+12)/(ny+25))*100:+.4f}pt")
