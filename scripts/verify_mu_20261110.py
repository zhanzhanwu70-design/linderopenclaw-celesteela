#!/usr/bin/env python3
"""2026-11-10 對位數字覆核。

口徑：Limitless matchups 頁每一列的數值＝「被檢視的那副牌」自己對該對手的勝率。
因此：
  「A 壓 B p%」→ 必須等於 A 自己那一列對 B 的 win%。
  「A 輸 B p%」→ 必須等於 B 那一列對 A 的 win%（即 A 輸的比率）。
兩列在同一 N 下應互補（win_A + win_B + 平局 = 100）。
"""
import json
import sys

M = json.load(open('memory/mu_matrix_20261110_c1.json'))

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
}

# (主體, 對手, 方向, 報告數值, N)
CLAIMS = [
    ('自爆磁怪', '蜂女王 ex', '壓', 91.8, 61),
    ('自爆磁怪', '超級甲賀忍蛙 ex', '壓', 72.2, 36),
    ('自爆磁怪', '胡帕 ex', '壓', 59.0, 61),
    ('自爆磁怪', '水君 ex', '壓', 58.3, 60),
    ('自爆磁怪', '超級路卡利歐 ex', '輸', 60.4, 53),
    ('自爆磁怪', '月亮伊布', '輸', 62.5, 48),
    ('自爆磁怪', '超級七夕青鳥 ex', '輸', 57.1, 49),
    ('蜂女王 ex', '胡帕 ex', '壓', 75.7, 148),
    ('蜂女王 ex', '水君 ex', '壓', 69.7, 142),
    ('蜂女王 ex', '超級甲賀忍蛙 ex', '壓', 75.6, 41),
    ('蜂女王 ex', '超級七夕青鳥 ex', '壓', 55.0, 60),
    ('蜂女王 ex', '自爆磁怪', '輸', 91.8, 61),
    ('蜂女王 ex', '超級路卡利歐 ex', '輸', 70.6, 119),
    ('胡帕 ex', '超級噴火龍 Y ex', '壓', 56.4, 172),
    ('胡帕 ex', '超級七夕青鳥 ex', '壓', 65.6, 93),
    ('胡帕 ex', '超級雷電獸 ex', '壓', 71.2, 66),
    ('胡帕 ex', '騎拉帝納 ex', '壓', 76.7, 60),
    ('胡帕 ex', '蜂女王 ex', '輸', 75.7, 148),
    ('三首惡龍', '騎拉帝納 ex', '壓', 74.1, 27),
    ('三首惡龍', '蜂女王 ex', '壓', 64.7, 34),
    ('三首惡龍', '超級噴火龍 Y ex', '壓', 58.9, 56),
    ('三首惡龍', '胡帕 ex', '輸', 65.2, 46),
    ('三首惡龍', '水君 ex', '輸', 53.3, 45),
    ('超級路卡利歐 ex', '蜂女王 ex', '壓', 70.6, 119),
    ('超級路卡利歐 ex', '自爆磁怪', '壓', 60.4, 53),
    ('超級路卡利歐 ex', '水君 ex', '壓', 59.6, 109),
    ('超級路卡利歐 ex', '胡帕 ex', '壓', 56.1, 98),
    ('超級路卡利歐 ex', '月亮伊布', '壓', 52.0, 50),
    ('超級路卡利歐 ex', '超級七夕青鳥 ex', '輸', 59.3, 59),
    ('超級路卡利歐 ex', '超級噴火龍 Y ex', '輸', 50.5, 109),
    ('超級七夕青鳥 ex', '月亮伊布', '壓', 71.4, 70),
    ('超級七夕青鳥 ex', '超級路卡利歐 ex', '壓', 59.3, 59),
    ('超級七夕青鳥 ex', '水君 ex', '壓', 55.9, 102),
    ('超級七夕青鳥 ex', '超級噴火龍 Y ex', '壓', 56.1, 107),
    ('超級七夕青鳥 ex', '胡帕 ex', '輸', 65.6, 93),
    ('超級七夕青鳥 ex', '超級甲賀忍蛙 ex', '輸', 59.6, 57),
    ('水君 ex', '超級噴火龍 Y ex', '壓', 71.2, 208),
    ('水君 ex', '超級甲賀忍蛙 ex', '壓', 68.3, 82),
    ('水君 ex', '月亮伊布', '壓', 68.0, 128),
    ('水君 ex', '蜂女王 ex', '輸', 69.7, 142),
    ('水君 ex', '胡帕 ex', '輸', 59.3, 135),
    ('水君 ex', '超級路卡利歐 ex', '輸', 59.6, 109),
    ('超級甲賀忍蛙 ex', '水君 ex', '輸', 68.3, 82),
    ('超級甲賀忍蛙 ex', '自爆磁怪', '輸', 72.2, 36),
    ('超級甲賀忍蛙 ex', '蜂女王 ex', '輸', 75.6, 41),
    ('超級甲賀忍蛙 ex', '超級雷電獸 ex', '輸', 66.7, 57),
    ('超級甲賀忍蛙 ex', '超級七夕青鳥 ex', '壓', 59.6, 57),
    ('超級蜥蜴王 ex', '月亮伊布', '壓', 72.2, 36),
    ('超級蜥蜴王 ex', '胡帕 ex', '壓', 65.5, 29),
    ('超級蜥蜴王 ex', '騎拉帝納 ex', '壓', 62.9, 35),
    ('超級蜥蜴王 ex', '蜂女王 ex', '壓', 55.6, 36),
    ('超級蜥蜴王 ex', '超級雷電獸 ex', '輸', 73.3, 30),
    ('超級蜥蜴王 ex', '水君 ex', '輸', 59.0, 78),
    ('超級蜥蜴王 ex', '超級噴火龍 Y ex', '輸', 58.8, 85),
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

# 互補性檢查
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
