#!/usr/bin/env python3
"""2026-11-23 解析 matchups 矩陣 + 陷阱牌組對位報告。"""
import glob
import json
import re

M = {}
for f in sorted(glob.glob('memory/matchups_20261125/*.html')):
    h = open(f, encoding='utf-8').read()
    t = re.search(r'<title>([^<]*?) - C1 Standard - Matchups', h)
    if not t:
        print('skip', f)
        continue
    me = t.group(1).strip()
    d = {}
    for tr in re.findall(r'<tr ([^>]*)>', h):
        nm = re.search(r'data-name="([^"]+)"', tr)
        mm = re.search(r'data-matches="(\d+)"', tr)
        wr = re.search(r'data-winrate="([\d.]+)"', tr)
        if nm and mm and wr:
            m = int(mm.group(1))
            w = round(float(wr.group(1)) * 100, 1)
            if nm.group(1) not in d or m > d[nm.group(1)][1]:
                d[nm.group(1)] = [w, m]
    M[me] = d

json.dump(M, open('memory/mu_matrix_20261125_c1.json', 'w'), ensure_ascii=False, indent=1)
print('decks', len(M), 'rows', sum(len(v) for v in M.values()))
for k, v in M.items():
    print('==', k, len(v))
    for o, (w, m) in sorted(v.items(), key=lambda x: -x[1][1])[:8]:
        print(f'   {o[:50]:52} {w:>5.1f}%  N={m}')
