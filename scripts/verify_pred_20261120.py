#!/usr/bin/env python3
"""2026-11-20 預測驗證：PRED_20261118（正式檢查日 2026-11-20）＋PRED_20261119（提前內檢）。"""
import collections
import json

D = json.load(open('ptcgp_deck_dictionary.json', encoding='utf-8'))
DN = D['deck_names']


def zh(n):
    return DN.get(n) or n


def agg(rows):
    out = collections.defaultdict(lambda: {'share': 0.0, 'w': 0, 'l': 0, 'd': 0, 'n': 0, 'decks': 0})
    for r in rows:
        a = out[r['name']]
        a['share'] += r['share']; a['w'] += r['w']; a['l'] += r['l']; a['d'] += r['d']
        a['n'] += r['n']; a['decks'] += r['decks']
    res = []
    for name, a in out.items():
        a = dict(a); a['name'] = name
        a['awr'] = (a['w'] + 12) / (a['n'] + 25) * 100 if a['n'] else 0.0
        res.append(a)
    res.sort(key=lambda r: -r['share'])
    return res


def load(day):
    suf = '.json' if day == '20261120' else '_re.json'
    d = json.load(open(f'memory/ptcgp_meta_{day}_std_comb{suf}', encoding='utf-8'))
    return d['header'], agg(d['rows'])


H4, T4 = load('20261120')
H3, T3 = load('20261119')
H2, T2 = load('20261118')
H1, T1 = load('20261117')
I4, I3, I2, I1 = ({r['name']: r for r in x} for x in (T4, T3, T2, T1))

print('### 環境')
print('11-20', H4, '| 11-19', H3, '| 11-18', H2, '| 11-17', H1)
print(f"增量 tournaments {H4['tournaments']-H3['tournaments']:+d} players {H4['players']-H3['players']:+d} matches {H4['matches']-H3['matches']:+d} ({(H4['matches']/H3['matches']-1)*100:+.2f}%)")
w = sum(r['w'] for r in T4); n = sum(r['n'] for r in T4)
print(f"全環境 AWR {(w+12)/(n+25)*100:.4f}% N={n}")

print('\n### PRED_20261118 正式驗證（檢查日 2026-11-20）')
print('A 超級七夕青鳥 ex 合併 AWR <53.0%')
for lbl, I in [('11-17', I1), ('11-18', I2), ('11-19', I3), ('11-20', I4)]:
    r = I['Mega Altaria ex']
    print(f"   {lbl}: AWR {r['awr']:.4f}% 份額 {r['share']:.4f}% N={r['n']} raw {r['w']}/{r['n']}")
print('B 月亮伊布合併份額 <8.60%')
for lbl, I in [('11-17', I1), ('11-18', I2), ('11-19', I3), ('11-20', I4)]:
    r = I['Umbreon']
    print(f"   {lbl}: 份額 {r['share']:.4f}% AWR {r['awr']:.4f}% N={r['n']}")
print('C 超級蜥蜴王 ex 合併 AWR <49.60%')
for lbl, I in [('11-17', I1), ('11-18', I2), ('11-19', I3), ('11-20', I4)]:
    r = I['Mega Sceptile ex']
    print(f"   {lbl}: AWR {r['awr']:.4f}% 份額 {r['share']:.4f}% N={r['n']} raw {r['w']}/{r['n']}")

print('\n### PRED_20261119 提前內檢（檢查日 2026-11-21）')
print('A 超級路卡利歐 ex 合併 AWR <50.00%')
for lbl, I in [('11-16', None), ('11-17', I1), ('11-18', I2), ('11-19', I3), ('11-20', I4)]:
    if I is None: continue
    r = I['Mega Lucario ex']
    print(f"   {lbl}: AWR {r['awr']:.4f}% 份額 {r['share']:.4f}% N={r['n']} raw {r['w']}/{r['n']}")
print('B 超級雷電獸 ex 合併份額 <3.40%')
for lbl, I in [('11-17', I1), ('11-18', I2), ('11-19', I3), ('11-20', I4)]:
    r = I['Mega Manectric ex']
    print(f"   {lbl}: 份額 {r['share']:.4f}% AWR {r['awr']:.4f}% N={r['n']}")
print('C 騎拉帝納 ex 合併份額 <4.20%')
for lbl, I in [('11-17', I1), ('11-18', I2), ('11-19', I3), ('11-20', I4)]:
    r = I['Giratina ex']
    print(f"   {lbl}: 份額 {r['share']:.4f}% AWR {r['awr']:.4f}% N={r['n']}")

print('\n### N 佔比（份額／全環境份額總和 123.28 比例，合併頁口徑）')
tot = sum(r['share'] for r in T4)
tot3 = sum(r['share'] for r in T3)
for name in ['Mega Charizard Y ex', 'Mega Altaria ex', 'Umbreon', 'Suicune ex', 'Hoopa ex',
             'Mega Greninja ex', 'Mega Lucario ex', 'Mega Mewtwo X ex', 'Vespiquen ex', 'Magnezone',
             'Giratina ex', 'Mega Manectric ex', 'Mega Sceptile ex', 'Hydreigon', 'Mega Skarmory ex',
             'Mega Greninja ex']:
    r4 = I4.get(name); r3 = I3.get(name)
    if r4 and r3:
        n4 = r4['share'] / tot * 100; n3 = r3['share'] / tot3 * 100
        print(f"  {zh(name)[:22]:24} N佔比 {n3:7.4f}% -> {n4:7.4f}%  Δ{n4-n3:+.4f}pt")
