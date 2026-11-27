#!/usr/bin/env python3
"""2026-11-26 模型參數：K 值、份額噪音帶、檢查日增量估計、T1、門檻可行性。"""
import collections
import json
import statistics

SUF = {'20261126': '.json', '20261125': '.json', '20261124': '.json', '20261123': '.json',
       '20261122': '.json', '20261121': '_re2.json', '20261120': '_re2.json',
       '20261119': '_re2.json', '20261118': '_re2.json', '20261117': '_re2.json',
       '20261116': '_re2.json', '20261115': '_re2.json', '20261114': '_re2.json',
       '20261113': '_re2.json', '20261112': '_re2.json', '20261111': '_re2.json',
       '20261110': '_re2.json'}


def agg(path):
    rows = json.load(open(path, encoding='utf-8'))['rows']
    out = collections.defaultdict(lambda: {'share': 0.0, 'decks': 0, 'n': 0, 'w': 0})
    for r in rows:
        a = out[r['name']]
        for k in ('share', 'decks', 'n', 'w'):
            a[k] += r[k]
    res = []
    for k, v in out.items():
        v = dict(v)
        v['name'] = k
        v['awr'] = (v['w'] + 12) / (v['n'] + 25) * 100 if v['n'] else 0
        v['raw'] = v['w'] / v['n'] * 100 if v['n'] else 0
        res.append(v)
    return res


def load(day):
    j = json.load(open(f'memory/ptcgp_meta_{day}_std_comb{SUF[day]}', encoding='utf-8'))
    return j['header'], agg(f'memory/ptcgp_meta_{day}_std_comb{SUF[day]}')


H, T = load('20261126')
HY, Y = load('20261125')
TOTD = sum(r['decks'] for r in T)
TOTD_Y = sum(r['decks'] for r in Y)
ENV_N = sum(r['n'] for r in T)
print(f"今日 T0={TOTD} 昨日 T0={TOTD_Y} 增量 {TOTD-TOTD_Y:+d}  環境 N={ENV_N}  AWR {(sum(r['w'] for r in T)+12)/(ENV_N+25)*100:.4f}%")

# ---- K 值（N>=200 可比牌組）----
ks = []
for r in T:
    if r['n'] >= 200 and r['decks'] > 0:
        ks.append(r['share'] / (r['decks'] / TOTD * 100))
print(f"K 值（可比 {len(ks)} 支）：中位 {statistics.median(ks):.4f} 平均 {statistics.mean(ks):.4f} 標準差 {statistics.pstdev(ks):.4f} min {min(ks):.4f} max {max(ks):.4f}")
K = statistics.median(ks)

# ---- 份額噪音帶 ----
ymap = {r['name']: r for r in Y}
deltas = [(r['share'] - ymap[r['name']]['share'], r['name'], r['share'], r['n'])
          for r in T if r['name'] in ymap and r['n'] >= 200]
vals = [d[0] for d in deltas]
print(f"份額噪音帶：可比 {len(vals)} 最大上升 {max(vals):+.4f}pt 最大下降 {min(vals):+.4f}pt 中位 {statistics.median(vals):+.4f}pt 標準差 {statistics.pstdev(vals):.4f}pt")

# ---- 檢查日（11-27）增量估計：歷史 weekday 差 ----
import datetime
hist = []
for d in sorted(SUF):
    try:
        h, rows = load(d)
    except Exception:
        continue
    hist.append((d, h['matches'], sum(r['decks'] for r in rows), h['tournaments'], h['players']))
print('\n日期 對局 副牌 (與前一日差)')
prev = None
byday = {}
for d, m, dk, t, p in hist:
    byday[d] = (m, dk)
for d in sorted(byday):
    dt = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:8]))
    if prev:
        pd_ = prev[0]
        pm, pdk = byday[pd_]
        m, dk = byday[d]
        print(f"  {d} ({dt.strftime('%a')}) 對局 {m} Δ{m-pm:+5d}  副牌 {dk} Δ{dk-pdk:+5d}   (前一日 {pd_} {dt.fromordinal(dt.toordinal()-1).strftime('%a')})")
    prev = (d,)

# Thu->Fri 歷史差
import re
pairs = []
for d in sorted(byday):
    dt = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:8]))
    pd_ = datetime.date.fromordinal(dt.toordinal() - 1)
    pdk_key = pd_.strftime('%Y%m%d')
    if pdk_key in byday:
        if dt.weekday() == 4 and pd_.weekday() == 3:   # Fri after Thu
            pairs.append((d, byday[d][0] - byday[pdk_key][0], byday[d][1] - byday[pdk_key][1]))
print('\n近三週 Thu→Fri 對局／副牌 差：')
for p in pairs:
    print('  ', p)
if pairs:
    dm = statistics.median([p[1] for p in pairs])
    dd = statistics.median([p[2] for p in pairs])
    print(f'  中位：對局 {dm:+.0f}  副牌 {dd:+.0f}')
