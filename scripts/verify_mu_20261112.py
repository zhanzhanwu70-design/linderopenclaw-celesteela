#!/usr/bin/env python3
"""2026-11-12 對位數字覆核。

口徑：Limitless matchups 頁每一列的數值＝「被檢視的那副牌」自己對該對手的勝率。
  「A 壓 B p%」→ A 自己那一列對 B 的 win%（N 為該列對局數）。
  「A 輸 B p%」→ B 那一列對 A 的 win%（N 相同）。
"""
import json
import sys

M = json.load(open('memory/mu_matrix_20261112_c1.json'))

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

# (主體, 對手, 方向, 報告數值, N)
CLAIMS = [
    ('自爆磁怪', '蜂女王 ex', '壓', 91.5, 71),
    ('自爆磁怪', '超級甲賀忍蛙 ex', '壓', 74.4, 39),
    ('自爆磁怪', '胡帕 ex', '壓', 59.2, 71),
    ('自爆磁怪', '水君 ex', '壓', 54.3, 70),
    ('自爆磁怪', '超級噴火龍 Y ex', '壓', 43.3, 134),
    ('自爆磁怪', '超級路卡利歐 ex', '壓', 40.9, 66),
    ('自爆磁怪', '月亮伊布', '壓', 39.7, 63),
    ('自爆磁怪', '超級七夕青鳥 ex', '壓', 42.9, 56),
    ('自爆磁怪', '騎拉帝納 ex', '壓', 60.5, 38),
    ('自爆磁怪', '超級蜥蜴王 ex', '壓', 47.2, 36),
    ('蜂女王 ex', '胡帕 ex', '壓', 75.5, 151),
    ('蜂女王 ex', '水君 ex', '壓', 69.9, 143),
    ('蜂女王 ex', '月亮伊布', '壓', 65.2, 69),
    ('蜂女王 ex', '超級甲賀忍蛙 ex', '壓', 74.4, 43),
    ('蜂女王 ex', '超級七夕青鳥 ex', '壓', 54.1, 61),
    ('蜂女王 ex', '超級路卡利歐 ex', '輸', 70.5, 122),
    ('蜂女王 ex', '自爆磁怪', '輸', 91.5, 71),
    ('水君 ex', '超級噴火龍 Y ex', '壓', 70.3, 236),
    ('水君 ex', '月亮伊布', '壓', 67.2, 134),
    ('水君 ex', '超級甲賀忍蛙 ex', '壓', 68.7, 83),
    ('水君 ex', '超級蜥蜴王 ex', '壓', 57.5, 80),
    ('水君 ex', '蜂女王 ex', '輸', 69.9, 143),
    ('水君 ex', '胡帕 ex', '輸', 58.2, 146),
    ('超級七夕青鳥 ex', '月亮伊布', '壓', 70.3, 74),
    ('超級七夕青鳥 ex', '超級路卡利歐 ex', '壓', 61.8, 68),
    ('超級七夕青鳥 ex', '水君 ex', '壓', 54.1, 109),
    ('超級七夕青鳥 ex', '超級噴火龍 Y ex', '壓', 56.3, 126),
    ('超級七夕青鳥 ex', '胡帕 ex', '輸', 66.0, 100),
    ('超級路卡利歐 ex', '蜂女王 ex', '壓', 70.5, 122),
    ('超級路卡利歐 ex', '水君 ex', '壓', 60.2, 118),
    ('超級路卡利歐 ex', '胡帕 ex', '壓', 53.3, 107),
    ('超級路卡利歐 ex', '自爆磁怪', '壓', 56.1, 66),
    ('超級路卡利歐 ex', '騎拉帝納 ex', '壓', 65.1, 43),
    ('超級路卡利歐 ex', '超級七夕青鳥 ex', '輸', 61.8, 68),
    ('超級路卡利歐 ex', '超級噴火龍 Y ex', '輸', 50.0, 130),
    ('胡帕 ex', '超級七夕青鳥 ex', '壓', 66.0, 100),
    ('胡帕 ex', '超級雷電獸 ex', '壓', 71.0, 69),
    ('胡帕 ex', '騎拉帝納 ex', '壓', 77.0, 61),
    ('胡帕 ex', '超級超夢 X ex', '壓', 77.6, 58),
    ('胡帕 ex', '超級噴火龍 Y ex', '壓', 55.7, 192),
    ('胡帕 ex', '水君 ex', '壓', 58.2, 146),
    ('超級甲賀忍蛙 ex', '超級七夕青鳥 ex', '壓', 59.6, 57),
    ('超級甲賀忍蛙 ex', '月亮伊布', '壓', 58.1, 93),
    ('超級甲賀忍蛙 ex', '水君 ex', '輸', 68.7, 83),
    ('超級甲賀忍蛙 ex', '自爆磁怪', '輸', 74.4, 39),
    ('超級甲賀忍蛙 ex', '蜂女王 ex', '輸', 74.4, 43),
    ('三首惡龍', '蜂女王 ex', '壓', 64.7, 34),
    ('三首惡龍', '騎拉帝納 ex', '壓', 75.0, 28),
    ('三首惡龍', '超級噴火龍 Y ex', '壓', 54.8, 62),
    ('三首惡龍', '胡帕 ex', '輸', 66.0, 47),
    ('三首惡龍', '水君 ex', '輸', 54.2, 48),
    ('超級蜥蜴王 ex', '月亮伊布', '壓', 72.5, 40),
    ('超級蜥蜴王 ex', '騎拉帝納 ex', '壓', 60.5, 38),
    ('超級蜥蜴王 ex', '蜂女王 ex', '壓', 55.6, 36),
    ('超級蜥蜴王 ex', '超級雷電獸 ex', '輸', 73.3, 30),
]

bad = 0
for me, opp, direction, claim, n in CLAIMS:
    me_row, op_row = NAME2ROW[me], NAME2ROW[opp]
    if direction == '壓':
        entry = M.get(me_row, {}).get(op_row)
        if not entry:
            print(f'✗ {me} vs {opp}: 自己那一列找不到對手')
            bad += 1
            continue
        w, m = entry
        if m != n:
            print(f'✗ {me} 壓 {opp}: N 不符（報告 {n} / 實際 {m}）')
            bad += 1
        elif abs(w - claim) > 0.05:
            print(f'✗ {me} 壓 {opp}: 報告 {claim}% / 自己列 {w}%')
            bad += 1
    else:
        entry = M.get(op_row, {}).get(me_row)
        if not entry:
            print(f'✗ {me} vs {opp}: 對手那一列找不到對手')
            bad += 1
            continue
        w, m = entry
        if m != n:
            print(f'✗ {me} 輸 {opp}: N 不符（報告 {n} / 實際 {m}）')
            bad += 1
        elif abs(w - claim) > 0.05:
            print(f'✗ {me} 輸 {opp}: 報告 {claim}% / 對手列 {w}%')
            bad += 1

for me, opp, direction, claim, n in CLAIMS:
    me_row, op_row = NAME2ROW[me], NAME2ROW[opp]
    a = M.get(me_row, {}).get(op_row)
    b = M.get(op_row, {}).get(me_row)
    if a and b and a[1] == b[1]:
        tot = a[0] + b[0]
        if tot > 100.2 or tot < 96:
            print(f'! {me} vs {opp}: 兩列 win% 合計 {tot:.1f}%（N={a[1]}）')

print(f'\n覆核 {len(CLAIMS)} 條對位敘述，錯誤 {bad} 條')
sys.exit(1 if bad else 0)
