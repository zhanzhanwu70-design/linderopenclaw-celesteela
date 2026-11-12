#!/usr/bin/env python3
"""2026-11-11 對位數字覆核。

口徑：Limitless matchups 頁每一列的數值＝「被檢視的那副牌」自己對該對手的勝率。
因此：
  「A 壓 B p%」→ 必須等於 A 自己那一列對 B 的 win%（N 為該列對局數）。
  「A 輸 B p%」→ 必須等於 B 那一列對 A 的 win%（即 A 輸的比率，N 相同）。
"""
import json
import sys

M = json.load(open('memory/mu_matrix_20261111_c1.json'))

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
    ('自爆磁怪', '蜂女王 ex', '壓', 92.3, 65),
    ('自爆磁怪', '超級甲賀忍蛙 ex', '壓', 73.7, 38),
    ('自爆磁怪', '胡帕 ex', '壓', 60.3, 68),
    ('自爆磁怪', '水君 ex', '壓', 55.4, 65),
    ('自爆磁怪', '超級噴火龍 Y ex', '壓', 45.1, 122),
    ('自爆磁怪', '超級路卡利歐 ex', '輸', 56.9, 65),
    ('自爆磁怪', '月亮伊布', '輸', 61.0, 59),
    ('自爆磁怪', '超級七夕青鳥 ex', '輸', 53.7, 54),
    ('蜂女王 ex', '胡帕 ex', '壓', 75.3, 150),
    ('蜂女王 ex', '水君 ex', '壓', 69.9, 143),
    ('蜂女王 ex', '月亮伊布', '壓', 65.7, 67),
    ('蜂女王 ex', '超級甲賀忍蛙 ex', '壓', 75.6, 41),
    ('蜂女王 ex', '超級七夕青鳥 ex', '壓', 54.1, 61),
    ('蜂女王 ex', '自爆磁怪', '輸', 92.3, 65),
    ('蜂女王 ex', '超級路卡利歐 ex', '輸', 70.2, 121),
    ('三首惡龍', '騎拉帝納 ex', '壓', 75.0, 28),
    ('三首惡龍', '蜂女王 ex', '壓', 64.7, 34),
    ('三首惡龍', '超級噴火龍 Y ex', '壓', 56.7, 60),
    ('三首惡龍', '胡帕 ex', '輸', 65.2, 46),
    ('三首惡龍', '水君 ex', '輸', 55.3, 47),
    ('胡帕 ex', '超級七夕青鳥 ex', '壓', 66.0, 97),
    ('胡帕 ex', '超級雷電獸 ex', '壓', 71.6, 67),
    ('胡帕 ex', '騎拉帝納 ex', '壓', 77.0, 61),
    ('胡帕 ex', '超級超夢 X ex', '壓', 77.6, 58),
    ('胡帕 ex', '超級噴火龍 Y ex', '壓', 54.6, 183),
    ('胡帕 ex', '蜂女王 ex', '輸', 75.3, 150),
    ('胡帕 ex', '水君 ex', '輸', 39.0, 141),
    ('超級七夕青鳥 ex', '月亮伊布', '壓', 69.9, 73),
    ('超級七夕青鳥 ex', '超級路卡利歐 ex', '壓', 61.2, 67),
    ('超級七夕青鳥 ex', '水君 ex', '壓', 54.2, 107),
    ('超級七夕青鳥 ex', '超級噴火龍 Y ex', '壓', 55.6, 117),
    ('超級七夕青鳥 ex', '胡帕 ex', '輸', 66.0, 97),
    ('超級七夕青鳥 ex', '自爆磁怪', '輸', 42.6, 54),
    ('超級路卡利歐 ex', '蜂女王 ex', '壓', 70.2, 121),
    ('超級路卡利歐 ex', '水君 ex', '壓', 60.0, 115),
    ('超級路卡利歐 ex', '胡帕 ex', '壓', 54.3, 105),
    ('超級路卡利歐 ex', '自爆磁怪', '壓', 56.9, 65),
    ('超級路卡利歐 ex', '騎拉帝納 ex', '壓', 65.1, 43),
    ('超級路卡利歐 ex', '超級七夕青鳥 ex', '輸', 61.2, 67),
    ('超級路卡利歐 ex', '超級噴火龍 Y ex', '輸', 49.6, 121),
    ('水君 ex', '超級噴火龍 Y ex', '壓', 70.5, 217),
    ('水君 ex', '月亮伊布', '壓', 66.9, 133),
    ('水君 ex', '超級甲賀忍蛙 ex', '壓', 68.3, 82),
    ('水君 ex', '超級蜥蜴王 ex', '壓', 57.5, 80),
    ('水君 ex', '蜂女王 ex', '輸', 69.9, 143),
    ('水君 ex', '胡帕 ex', '輸', 58.9, 141),
    ('超級甲賀忍蛙 ex', '超級七夕青鳥 ex', '壓', 59.6, 57),
    ('超級甲賀忍蛙 ex', '月亮伊布', '壓', 58.7, 92),
    ('超級甲賀忍蛙 ex', '水君 ex', '輸', 68.3, 82),
    ('超級甲賀忍蛙 ex', '自爆磁怪', '輸', 73.7, 38),
    ('超級甲賀忍蛙 ex', '蜂女王 ex', '輸', 75.6, 41),
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

# 互補性檢查（同一 N 下兩列 win% 合計應接近 100 減平局率）
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
