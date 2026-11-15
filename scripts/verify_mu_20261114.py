#!/usr/bin/env python3
"""2026-11-14 對位數字覆核。

口徑：Limitless matchups 頁每一列的數值＝「被檢視的那副牌」自己對該對手的勝率。
  「A 壓 B p%」→ A 自己那一列對 B 的 win%（N 為該列對局數）。
  「A 輸 B p%」→ B 那一列對 A 的 win%（N 相同）。
"""
import json
import sys

M = json.load(open('memory/mu_matrix_20261114_c1.json', encoding='utf-8'))

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

CLAIMS = [
    ('自爆磁怪', '蜂女王 ex', '壓', 91.6, 83),
    ('自爆磁怪', '超級甲賀忍蛙 ex', '壓', 74.4, 43),
    ('自爆磁怪', '胡帕 ex', '壓', 56.2, 89),
    ('自爆磁怪', '水君 ex', '壓', 55.4, 83),
    ('自爆磁怪', '騎拉帝納 ex', '壓', 57.8, 45),
    ('自爆磁怪', '超級噴火龍 Y ex', '壓', 46.2, 169),
    ('自爆磁怪', '超級路卡利歐 ex', '壓', 42.7, 82),
    ('自爆磁怪', '月亮伊布', '壓', 42.1, 76),
    ('自爆磁怪', '超級七夕青鳥 ex', '壓', 39.7, 63),
    ('自爆磁怪', '超級噴火龍 Y ex', '輸', 52.1, 169),
    ('自爆磁怪', '超級路卡利歐 ex', '輸', 54.9, 82),
    ('自爆磁怪', '月亮伊布', '輸', 56.6, 76),
    ('自爆磁怪', '超級七夕青鳥 ex', '輸', 57.1, 63),
    ('三首惡龍', '自爆磁怪', '壓', 69.2, 26),

    ('三首惡龍', '騎拉帝納 ex', '壓', 75.9, 29),
    ('三首惡龍', '蜂女王 ex', '壓', 61.5, 39),
    ('三首惡龍', '超級噴火龍 Y ex', '壓', 53.9, 76),
    ('三首惡龍', '超級甲賀忍蛙 ex', '壓', 48.5, 33),
    ('三首惡龍', '水君 ex', '壓', 43.6, 55),
    ('三首惡龍', '胡帕 ex', '輸', 63.0, 54),
    ('三首惡龍', '超級雷電獸 ex', '輸', 36.4, 22),

    ('蜂女王 ex', '胡帕 ex', '壓', 72.8, 169),
    ('蜂女王 ex', '超級甲賀忍蛙 ex', '壓', 76.0, 50),
    ('蜂女王 ex', '水君 ex', '壓', 69.4, 160),
    ('蜂女王 ex', '月亮伊布', '壓', 68.8, 80),
    ('蜂女王 ex', '超級七夕青鳥 ex', '壓', 54.5, 66),
    ('蜂女王 ex', '超級雷電獸 ex', '壓', 54.7, 64),
    ('蜂女王 ex', '自爆磁怪', '輸', 91.6, 83),
    ('蜂女王 ex', '超級路卡利歐 ex', '輸', 66.9, 142),

    ('超級七夕青鳥 ex', '月亮伊布', '壓', 67.1, 85),
    ('超級七夕青鳥 ex', '超級路卡利歐 ex', '壓', 60.0, 85),
    ('超級七夕青鳥 ex', '自爆磁怪', '壓', 57.1, 63),
    ('超級七夕青鳥 ex', '超級噴火龍 Y ex', '壓', 56.8, 162),
    ('超級七夕青鳥 ex', '水君 ex', '壓', 52.9, 121),
    ('超級七夕青鳥 ex', '胡帕 ex', '輸', 65.8, 111),
    ('超級七夕青鳥 ex', '超級甲賀忍蛙 ex', '輸', 60.3, 63),

    ('胡帕 ex', '騎拉帝納 ex', '壓', 78.5, 65),
    ('胡帕 ex', '超級七夕青鳥 ex', '壓', 65.8, 111),
    ('胡帕 ex', '超級雷電獸 ex', '壓', 72.0, 75),
    ('胡帕 ex', '水君 ex', '壓', 57.1, 161),
    ('胡帕 ex', '超級噴火龍 Y ex', '壓', 55.1, 227),
    ('胡帕 ex', '蜂女王 ex', '輸', 72.8, 169),
    ('胡帕 ex', '超級超夢 X ex', '壓', 73.4, 64),

    ('超級噴火龍 Y ex', '超級路卡利歐 ex', '壓', 55.9, 179),
    ('超級路卡利歐 ex', '超級噴火龍 Y ex', '輸', 55.9, 179),
    ('超級超夢 X ex', '胡帕 ex', '壓', 26.6, 64),
    ('超級蜥蜴王 ex', '月亮伊布', '壓', 69.8, 43),
    ('超級蜥蜴王 ex', '胡帕 ex', '壓', 65.9, 41),
    ('超級蜥蜴王 ex', '超級雷電獸 ex', '輸', 75.0, 32),
    ('超級蜥蜴王 ex', '超級噴火龍 Y ex', '輸', 56.4, 110),

    ('超級甲賀忍蛙 ex', '水君 ex', '壓', 28.4, 95),
    ('超級甲賀忍蛙 ex', '自爆磁怪', '壓', 25.6, 43),
    ('超級甲賀忍蛙 ex', '蜂女王 ex', '壓', 22.0, 50),
    ('超級甲賀忍蛙 ex', '胡帕 ex', '壓', 42.7, 82),
    ('超級甲賀忍蛙 ex', '水君 ex', '輸', 67.4, 95),
    ('超級甲賀忍蛙 ex', '自爆磁怪', '輸', 74.4, 43),
    ('超級甲賀忍蛙 ex', '蜂女王 ex', '輸', 76.0, 50),
    ('超級甲賀忍蛙 ex', '胡帕 ex', '輸', 54.9, 82),
    ('自爆磁怪', '超級超夢 X ex', '壓', 51.4, 37),
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

print(f'\n覆核 {len(CLAIMS)} 條對位敘述，錯誤 {bad} 條')
sys.exit(1 if bad else 0)
