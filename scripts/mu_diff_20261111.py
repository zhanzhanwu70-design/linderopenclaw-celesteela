#!/usr/bin/env python3
"""2026-11-11 對位矩陣比較：11-10 vs 11-11，找結構變化。"""
import json

A = json.load(open('memory/mu_matrix_20261110_c1.json'))
B = json.load(open('memory/mu_matrix_20261111_c1.json'))

NAME2ROW = {
    '自爆磁怪': 'Magnezone Miraidon ex',
    '蜂女王 ex': 'Vespiquen ex Shuckle ex',
    '胡帕 ex': 'Hoopa ex Mega Absol ex',
    '三首惡龍': 'Hydreigon Mega Absol ex',
    '超級路卡利歐 ex': 'Mega Lucario ex Lucario',
    '水君 ex': 'Suicune ex Baxcalibur',
    '超級七夕青鳥 ex': 'Mega Altaria ex Espeon',
    '超級噴火龍 Y ex': 'Mega Charizard Y ex Entei ex',
    '超級甲賀忍蛙 ex': 'Mega Greninja ex Greninja ex',
    '超級蜥蜴王 ex': 'Mega Sceptile ex Greninja',
    '超級雷電獸 ex': 'Mega Manectric ex Heliolisk',
    '月亮伊布': 'Umbreon Hydreigon',
    '騎拉帝納 ex': 'Giratina ex Dragonair',
    '超級超夢 X ex': 'Mega Mewtwo X ex Mew ex',
}

KEYS = list(NAME2ROW)

print('### 對位變動（|Δ|>=3.0pt 且 N>=25）')
for me in KEYS:
    rm = NAME2ROW[me]
    rowB = B.get(rm, {})
    rowA = A.get(rm, {})
    for opp, (wB, nB) in rowB.items():
        if opp == rm or nB < 25:
            continue
        if opp in rowA and rowA[opp][1] == nB:
            d = wB - rowA[opp][0]
            if abs(d) >= 3.0:
                onm = next((k for k, v in NAME2ROW.items() if v == opp), opp)
                print(f'  {me} vs {onm}: {rowA[opp][0]:.1f}% → {wB:.1f}%  ({d:+.1f}pt) N={nB}')
        else:
            print(f'  [新對線] {me} vs {opp}: {wB:.1f}%  N={nB}')

print('\n### 各主體今日主要對線（自己列，勝率）')
for me in KEYS:
    rm = NAME2ROW[me]
    rowB = B.get(rm, {})
    if not rowB:
        continue
    print(f'== {me}')
    for opp, (w, n) in sorted(rowB.items(), key=lambda x: -x[1][1])[:8]:
        if opp == rm:
            continue
        onm = next((k for k, v in NAME2ROW.items() if v == opp), opp)
        print(f'   vs {onm:18} {w:>5.1f}%  N={n}')
