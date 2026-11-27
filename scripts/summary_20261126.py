#!/usr/bin/env python3
"""2026-11-26 PTCGP Meta 摘要：合併頁同名加總、調整後勝率、多日比較、新舊卡與進榜變化。"""
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


SUF = {'20261126': '.json', '20261125': '.json', '20261124': '.json', '20261123': '.json', '20261122': '.json'}


def load(day, combined=True):
    kind = 'std_comb' if combined else 'std'
    data = json.load(open(f'memory/ptcgp_meta_{day}_{kind}{SUF[day]}', encoding='utf-8'))
    return data['header'], agg_rows(data['rows']) if combined else data['rows']


H, T = load('20261126', True)
_, TB = load('20261126', False)
H1, Y = load('20261125', True)
_, YB = load('20261125', False)
H2, Y2 = load('20261124', True)
H3, Y3 = load('20261123', True)
H4, Y4 = load('20261122', True)


def index(rows):
    return {r['name']: r for r in rows}


IT, IY, IY2, IY3, IY4 = index(T), index(Y), index(Y2), index(Y3), index(Y4)

print('### 環境')
print(H, 'branch_rows', len(TB), 'combined_rows', len(T), 'merged_groups', len(IT))
print('11-25', H1, '| 11-24', H2, '| 11-23', H3, '| 11-22', H4)
print(f"增量 tournaments {H['tournaments']-H1['tournaments']:+d} players {H['players']-H1['players']:+d} matches {H['matches']-H1['matches']:+d} ({(H['matches']/H1['matches']-1)*100:+.2f}%)")

print('\n### 合併份額前 30')
for i, r in enumerate(T[:30], 1):
    y = IY.get(r['name'])
    d = f"Δshare {r['share']-y['share']:+.4f}pt Δawr {r['awr']-y['awr']:+.4f}pt" if y else 'NEW'
    print(f"{i:2}. {zh(r['name'])[:30]:32} {r['share']:8.4f}% AWR {r['awr']:8.4f}% 副 {r['decks']:4} N {r['n']:5} {r['w']}-{r['l']}-{r['d']} | {d}")

print('\n### AWR 前 30（合併口徑，N>=100）')
for i, r in enumerate(sorted([x for x in T if x['n'] >= 100], key=lambda x: -x['awr'])[:30], 1):
    y = IY.get(r['name'])
    print(f"{i:2}. {zh(r['name'])[:30]:32} AWR {r['awr']:8.4f}% 份額 {r['share']:7.4f}% N {r['n']:5} | 昨 {y['awr'] if y else 0:8.4f}% | Δ {(r['awr']-y['awr']) if y else 0:+8.4f}pt")

print('\n### 最差 20（N>=50）')
for r in sorted([x for x in T if x['n'] >= 50], key=lambda x: x['awr'])[:20]:
    print(f"  {zh(r['name'])[:32]:34} {r['awr']:8.4f}% 份額 {r['share']:7.4f}% N={r['n']}")

print('\n### 五日關鍵趨勢（合併同名加總）')
keys = ['Mega Charizard Y ex', 'Umbreon', 'Mega Altaria ex', 'Suicune ex', 'Mega Greninja ex',
        'Hoopa ex', 'Mega Lucario ex', 'Mega Mewtwo X ex', 'Vespiquen ex', 'Magnezone',
        'Giratina ex', 'Mega Manectric ex', 'Mega Sceptile ex', 'Hydreigon', 'Pikachu ex',
        'Chien Pao ex', 'Greninja ex', 'Greninja', 'Mega Skarmory ex', 'Mega Blaziken ex',
        'Lopunny', 'Miraidon ex', 'Alolan Exeggutor ex', 'Dragonair', 'Mega Dragonite ex',
        'Absol ex', 'Mega Bouffalant ex', 'Pidgeot ex', 'Arceus ex', 'Rampardos ex',
        'Mega Rayquaza ex', 'Zapdos ex', 'Eevee', 'Mega Banette ex', 'Latias ex',
        'Dedenne ex', 'Mega Mewtwo Y ex', 'Dondozo ex', 'Electivire', 'Mismagius',
        'Mega Treecko', 'Sableye ex', 'Wigglytuff ex', 'Ambipom', 'Whiscash',
        'Mega Tyranitar ex', 'Mega Buzzwole ex', 'Latios ex', 'Arcanine ex', 'Mega Gardevoir ex']
for name in keys:
    t, y, y2, y3, y4 = IT.get(name), IY.get(name), IY2.get(name), IY3.get(name), IY4.get(name)

    def fmt(r):
        return f"{r['share']:7.4f}%/{r['awr']:8.4f}% N={r['n']:5}" if r else ' -- '
    print(f"{zh(name)[:30]:32} 今 {fmt(t)} | 昨 {fmt(y)} | 前 {fmt(y2)} | 前2 {fmt(y3)} | 前3 {fmt(y4)}")

print('\n### 分支口徑前 45')
for i, r in enumerate(TB[:45], 1):
    print(f"{i:2}. {zh(r['name'])[:34]:36} {r['share']:7.4f}% AWR {r['awr']:8.4f}% N {r['n']:5} {r['w']}-{r['l']}-{r['d']}")

print('\n### 分支 AWR 前 15（N>=100）')
for i, r in enumerate(sorted([x for x in TB if x['n'] >= 100], key=lambda x: -x['awr'])[:15], 1):
    print(f"{i:2}. {zh(r['name'])[:34]:36} AWR {r['awr']:8.4f}% 份額 {r['share']:7.4f}% N {r['n']:5}")

cards = json.load(open('memory/ptcgp_cards_full.json', encoding='utf-8'))
C1N = {c.get('name') for k, c in cards.items() if k.startswith('C1_') and c.get('name')}


def has_c1(name):
    n = name.replace('’', "'")
    return any(n.startswith(c.replace('’', "'")) or n.startswith(c.replace('’', "'").replace(' ex', 'ex')) for c in C1N)


print('\n### 新舊卡差距（合併口徑）')
for label, rows in [('11-22', Y4), ('11-23', Y3), ('11-24', Y2), ('11-25', Y), ('11-26', T)]:
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

print('\n### 合併頁新名稱與退出前 40')
old_names = set(IY)
for r in T:
    if r['name'] not in old_names:
        print(' 新', zh(r['name'])[:32], f"{r['share']:.4f}%/{r['awr']:.4f}% N={r['n']} 副{r['decks']}")
cur40 = {r['name'] for r in T[:40]}
for r in Y[:40]:
    if r['name'] not in cur40:
        print(' 退', zh(r['name'])[:32], f"昨 {r['share']:.4f}%/{r['awr']:.4f}%")

print('\n### 分支前 40 進榜/退出')
prev40 = {x['name'] for x in YB[:40]}
for r in TB[:40]:
    if r['name'] not in prev40:
        print(' 新', zh(r['name'])[:34], f"{r['share']:.4f}%/{r['awr']:.4f}% N={r['n']}")
cur40b = {r['name'] for r in TB[:40]}
for r in YB[:40]:
    if r['name'] not in cur40b:
        print(' 退', zh(r['name'])[:34], f"昨 {r['share']:.4f}%/{r['awr']:.4f}%")

print('\n### 環境總副牌')
for label, rows in [('11-22', Y4), ('11-23', Y3), ('11-24', Y2), ('11-25', Y), ('11-26', T)]:
    print(f"  {label}: 總副牌 {sum(r['decks'] for r in rows)}  組數 {len(rows)}")

prev_decks = {r['name']: r['decks'] for r in Y}
inc = [(r['name'], r['decks'] - prev_decks.get(r['name'], 0)) for r in T]
inc.sort(key=lambda x: -x[1])
print('  今日副牌增加前 20:', [(zh(n)[:16], d) for n, d in inc[:20]])
print('  今日副牌減少:', [(zh(n)[:16], d) for n, d in inc if d < 0])
print('  持平組數:', sum(1 for n, d in inc if d == 0), ' 增加組數:', sum(1 for n, d in inc if d > 0), ' 減少組數:', sum(1 for n, d in inc if d < 0))

tot_decks_delta = sum(r['decks'] for r in T) - sum(r['decks'] for r in Y)
print('  總增量:', tot_decks_delta)
pos = sum(d for n, d in inc if d > 0)
print('  吸收集中度 (正吸收/總增量):', f"{pos/tot_decks_delta*100:.2f}%" if tot_decks_delta else 'n/a')

print('\n### 全環境')
w = sum(r['w'] for r in T)
n = sum(r['n'] for r in T)
wy = sum(r['w'] for r in Y)
ny = sum(r['n'] for r in Y)
print(f"AWR {(w+12)/(n+25)*100:.4f}% N={n} | 昨 {(wy+12)/(ny+25)*100:.4f}% N={ny} | Δ{((w+12)/(n+25)-(wy+12)/(ny+25))*100:+.4f}pt")

print('\n### 缺翻譯檢查（合併頁 + 分支頁）')
allrows = T + TB
miss = sorted({r['name'] for r in allrows if r['name'] not in DN and r['name'] not in CN})
print('  缺翻譯數:', len(miss))
for m in miss[:40]:
    print('   -', m)
