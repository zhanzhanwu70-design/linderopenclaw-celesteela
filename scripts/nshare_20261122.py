#!/usr/bin/env python3
"""2026-11-22 N 佔全環境比重（合併口徑，同名加總）11-19～11-22 趨勢。"""
import collections
import json


def agg(rows):
    out = collections.defaultdict(lambda: {'share': 0.0, 'w': 0, 'l': 0, 'd': 0, 'n': 0, 'decks': 0})
    for r in rows:
        a = out[r['name']]
        for k in ('share', 'w', 'l', 'd', 'n', 'decks'):
            a[k] += r[k]
    res = []
    for name, a in out.items():
        a = dict(a)
        a['name'] = name
        a['awr'] = (a['w'] + 12) / (a['n'] + 25) * 100 if a['n'] else 0.0
        res.append(a)
    res.sort(key=lambda r: -r['share'])
    return res


def load(day):
    suf = '.json' if day == '20261122' else '_re2.json'
    d = json.load(open(f'memory/ptcgp_meta_{day}_std_comb{suf}', encoding='utf-8'))
    return d['header'], agg(d['rows'])


days = ['20261119', '20261120', '20261121', '20261122']
data = {}
for d in days:
    h, rows = load(d)
    tot = sum(r['n'] for r in rows)
    data[d] = (rows, {r['name']: r['n'] / tot * 100 for r in rows}, tot)
    print(d, h, 'N=', tot, 'AWR=%.4f' % ((sum(r['w'] for r in rows) + 12) / (tot + 25) * 100))

names = ['Mega Altaria ex', 'Hoopa ex', 'Magnezone', 'Mega Greninja ex', 'Umbreon',
         'Mega Charizard Y ex', 'Suicune ex', 'Vespiquen ex', 'Mega Lucario ex', 'Giratina ex',
         'Mega Mewtwo X ex', 'Mega Manectric ex', 'Chien Pao ex', 'Mega Sceptile ex',
         'Mega Skarmory ex', 'Hydreigon', 'Greninja', 'Greninja ex', 'Arceus ex',
         'Mega Dragonite ex', 'Absol ex', 'Pidgeot ex', 'Alolan Exeggutor ex', 'Dragonair',
         'Mega Bouffalant ex', 'Lopunny', 'Pikachu ex', 'Miraidon ex', 'Rampardos ex',
         'Zapdos ex', 'Eevee', 'Latias ex', 'Sylveon', 'Dedenne ex', 'Mega Mewtwo Y ex']
print()
for n in names:
    line = []
    for d in days:
        rows, ns, tot = data[d]
        r = [x for x in rows if x['name'] == n]
        if r:
            line.append(f"{d[4:6]}-{d[6:8]} N佔 {ns[n]:6.4f}% 份額 {r[0]['share']:7.4f}% AWR {r[0]['awr']:7.4f}% N={r[0]['n']:5}")
        else:
            line.append(f"{d[4:6]}-{d[6:8]} --")
    print(f"{n:22} | " + " | ".join(line))

print('\n### 今日份額變動分布（合併口徑，同名加總）噪音量化')
rows_t, ns_t, tot_t = data['20261122']
rows_y, ns_y, tot_y = data['20261121']
deltas = []
for r in rows_t:
    y = [x for x in rows_y if x['name'] == r['name']]
    if y and r['n'] >= 200:
        deltas.append((r['share'] - y[0]['share'], r['name'], r['share'], r['n']))
deltas.sort()
vals = [d[0] for d in deltas]
import statistics
print(f"  可比牌組數 N>=200: {len(vals)}  最大上升 {vals[-1]:+.4f}pt  最大下降 {vals[0]:+.4f}pt  中位 {statistics.median(vals):+.4f}pt  平均 {statistics.mean(vals):+.4f}pt  標準差 {statistics.pstdev(vals):.4f}pt")
print('  上升前 8：')
for d in deltas[-8:][::-1]:
    print(f"    {d[1][:34]:36} {d[0]:+.4f}pt  份額 {d[2]:.4f}% N={d[3]}")
print('  下降前 8：')
for d in deltas[:8]:
    print(f"    {d[1][:34]:36} {d[0]:+.4f}pt  份額 {d[2]:.4f}% N={d[3]}")
