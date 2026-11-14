import json

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

T = json.load(open('memory/mu_matrix_20261113_c1.json'))
Y = json.load(open('memory/mu_matrix_20261112_c1.json'))


def get(M, me, opp):
    e = M.get(NAME2ROW[me], {}).get(NAME2ROW[opp])
    return (e[0], e[1]) if e else (None, None)


pairs = []
for me in NAME2ROW:
    for opp in NAME2ROW:
        if me == opp: continue
        t, tn = get(T, me, opp)
        y, yn = get(Y, me, opp)
        if t is None or y is None: continue
        pairs.append((me, opp, y, yn, t, tn))

print('### 對位變化（|Δ|≥1.5pt，自身列口徑）')
ch = [p for p in pairs if abs(p[4]-p[2]) >= 1.5]
ch.sort(key=lambda p: -abs(p[4]-p[2]))
for me, opp, y, yn, t, tn in ch:
    print(f"  {me:18} vs {opp:18} {y:>5.1f}%→{t:>5.1f}% ({t-y:+.1f}pt)  N {yn}→{tn}")
print(f'  合計 {len(ch)} 條 / 共 {len(pairs)} 條')

print('\n### 主要線對位現況（今日）')
key = [
    ('自爆磁怪', '蜂女王 ex'), ('自爆磁怪', '超級甲賀忍蛙 ex'), ('自爆磁怪', '胡帕 ex'),
    ('自爆磁怪', '水君 ex'), ('自爆磁怪', '超級噴火龍 Y ex'), ('自爆磁怪', '超級路卡利歐 ex'),
    ('自爆磁怪', '月亮伊布'), ('自爆磁怪', '超級七夕青鳥 ex'), ('自爆磁怪', '騎拉帝納 ex'),
    ('自爆磁怪', '超級蜥蜴王 ex'), ('自爆磁怪', '超級超夢 X ex'),
    ('蜂女王 ex', '胡帕 ex'), ('蜂女王 ex', '水君 ex'), ('蜂女王 ex', '月亮伊布'),
    ('蜂女王 ex', '超級甲賀忍蛙 ex'), ('蜂女王 ex', '超級七夕青鳥 ex'),
    ('水君 ex', '超級噴火龍 Y ex'), ('水君 ex', '月亮伊布'), ('水君 ex', '超級甲賀忍蛙 ex'),
    ('水君 ex', '超級蜥蜴王 ex'), ('水君 ex', '蜂女王 ex'), ('水君 ex', '胡帕 ex'),
    ('超級七夕青鳥 ex', '月亮伊布'), ('超級七夕青鳥 ex', '超級路卡利歐 ex'),
    ('超級七夕青鳥 ex', '水君 ex'), ('超級七夕青鳥 ex', '超級噴火龍 Y ex'), ('超級七夕青鳥 ex', '胡帕 ex'),
    ('超級路卡利歐 ex', '蜂女王 ex'), ('超級路卡利歐 ex', '水君 ex'), ('超級路卡利歐 ex', '胡帕 ex'),
    ('超級路卡利歐 ex', '自爆磁怪'), ('超級路卡利歐 ex', '騎拉帝納 ex'),
    ('超級路卡利歐 ex', '超級七夕青鳥 ex'), ('超級路卡利歐 ex', '超級噴火龍 Y ex'),
    ('胡帕 ex', '超級七夕青鳥 ex'), ('胡帕 ex', '超級雷電獸 ex'), ('胡帕 ex', '騎拉帝納 ex'),
    ('胡帕 ex', '超級超夢 X ex'), ('胡帕 ex', '超級噴火龍 Y ex'), ('胡帕 ex', '水君 ex'),
    ('超級甲賀忍蛙 ex', '超級七夕青鳥 ex'), ('超級甲賀忍蛙 ex', '月亮伊布'),
    ('三首惡龍', '蜂女王 ex'), ('三首惡龍', '騎拉帝納 ex'), ('三首惡龍', '超級噴火龍 Y ex'),
    ('三首惡龍', '胡帕 ex'), ('三首惡龍', '水君 ex'),
    ('超級蜥蜴王 ex', '月亮伊布'), ('超級蜥蜴王 ex', '騎拉帝納 ex'),
    ('超級蜥蜴王 ex', '蜂女王 ex'), ('超級蜥蜴王 ex', '超級雷電獸 ex'),
    ('超級超夢 X ex', '胡帕 ex'), ('超級超夢 X ex', '水君 ex'), ('超級超夢 X ex', '超級七夕青鳥 ex'),
    ('超級雷電獸 ex', '蜂女王 ex'), ('超級雷電獸 ex', '胡帕 ex'), ('超級雷電獸 ex', '水君 ex'),
    ('超級噴火龍 Y ex', '自爆磁怪'), ('超級噴火龍 Y ex', '三首惡龍'), ('超級噴火龍 Y ex', '月亮伊布'),
    ('超級噴火龍 Y ex', '水君 ex'), ('超級噴火龍 Y ex', '胡帕 ex'), ('超級噴火龍 Y ex', '超級七夕青鳥 ex'),
    ('騎拉帝納 ex', '胡帕 ex'), ('騎拉帝納 ex', '三首惡龍'), ('騎拉帝納 ex', '蜂女王 ex'),
]
for me, opp in key:
    t, tn = get(T, me, opp); y, yn = get(Y, me, opp)
    if t is None:
        print(f"  {me} vs {opp}: 缺"); continue
    print(f"  {me:18} vs {opp:18} 今日 {t:>5.1f}% (N={tn})   昨 {y if y is None else format(y,'.1f'):>6} (N={yn})   Δ {t-y:+.1f}pt" if y is not None else f"  {me} vs {opp}: 今日 {t}% N={tn}")
