#!/usr/bin/env python3
"""2026-11-18 對位數字覆核：每列數值為被檢視牌組自身勝率；不得用 100−自身勝率反推。"""
import json

M = json.load(open('memory/mu_matrix_20261118_c1.json', encoding='utf-8'))
Y = json.load(open('memory/mu_matrix_20261117_c1.json', encoding='utf-8'))

# 說明, A 列, B 列, 期望方向（win=大於50%，lose=小於50%）
CLAIMS = [
    ('水君壓噴火龍 Y', 'Suicune ex Baxcalibur', 'Mega Charizard Y ex Entei ex', 'win'),
    ('水君壓月亮伊布', 'Suicune ex Baxcalibur', 'Umbreon Hydreigon', 'win'),
    ('水君輸蜂女王', 'Suicune ex Baxcalibur', 'Vespiquen ex Shuckle ex', 'lose'),
    ('水君輸胡帕', 'Suicune ex Baxcalibur', 'Hoopa ex Mega Absol ex', 'lose'),
    ('蜂女王壓胡帕', 'Vespiquen ex Shuckle ex', 'Hoopa ex Mega Absol ex', 'win'),
    ('蜂女王壓水君', 'Vespiquen ex Shuckle ex', 'Suicune ex Baxcalibur', 'win'),
    ('路卡利歐壓蜂女王', 'Mega Lucario ex Lucario', 'Vespiquen ex Shuckle ex', 'win'),
    ('蜂女王輸自爆磁怪', 'Vespiquen ex Shuckle ex', 'Magnezone Miraidon ex', 'lose'),
    ('胡帕壓七夕青鳥忍蛙線', 'Hoopa ex Mega Absol ex', 'Mega Altaria ex Greninja', 'win'),
    ('胡帕壓七夕青鳥太陽伊布線', 'Hoopa ex Mega Absol ex', 'Mega Altaria ex Espeon', 'win'),
    ('胡帕輸蜂女王', 'Hoopa ex Mega Absol ex', 'Vespiquen ex Shuckle ex', 'lose'),
    ('胡帕壓水君', 'Hoopa ex Mega Absol ex', 'Suicune ex Baxcalibur', 'win'),
    ('自爆磁怪壓蜂女王', 'Magnezone Miraidon ex', 'Vespiquen ex Shuckle ex', 'win'),
    ('自爆磁怪壓胡帕', 'Magnezone Miraidon ex', 'Hoopa ex Mega Absol ex', 'win'),
    ('自爆磁怪輸七夕青鳥忍蛙線', 'Magnezone Miraidon ex', 'Mega Altaria ex Greninja', 'lose'),
    ('自爆磁怪輸月亮伊布', 'Magnezone Miraidon ex', 'Umbreon Hydreigon', 'lose'),
    ('七夕青鳥忍蛙線壓路卡利歐', 'Mega Altaria ex Greninja', 'Mega Lucario ex Lucario', 'win'),
    ('七夕青鳥忍蛙線壓月亮伊布', 'Mega Altaria ex Greninja', 'Umbreon Hydreigon', 'win'),
    ('七夕青鳥忍蛙線輸胡帕', 'Mega Altaria ex Greninja', 'Hoopa ex Mega Absol ex', 'lose'),
    ('七夕青鳥忍蛙線壓超夢強線', 'Mega Altaria ex Greninja', 'Mega Mewtwo X ex Mew ex', 'win'),
    ('七夕青鳥太陽伊布線壓路卡利歐', 'Mega Altaria ex Espeon', 'Mega Lucario ex Lucario', 'win'),
    ('七夕青鳥太陽伊布線壓月亮伊布', 'Mega Altaria ex Espeon', 'Umbreon Hydreigon', 'win'),
    ('七夕青鳥太陽伊布線輸胡帕', 'Mega Altaria ex Espeon', 'Hoopa ex Mega Absol ex', 'lose'),
    ('路卡利歐壓蜂女王', 'Mega Lucario ex Lucario', 'Vespiquen ex Shuckle ex', 'win'),
    ('路卡利歐壓水君', 'Mega Lucario ex Lucario', 'Suicune ex Baxcalibur', 'win'),
    ('路卡利歐輸七夕青鳥忍蛙線', 'Mega Lucario ex Lucario', 'Mega Altaria ex Greninja', 'lose'),
    ('忍蛙輸水君', 'Mega Greninja ex Greninja ex', 'Suicune ex Baxcalibur', 'lose'),
    ('忍蛙輸胡帕', 'Mega Greninja ex Greninja ex', 'Hoopa ex Mega Absol ex', 'lose'),
    ('忍蛙輸自爆磁怪', 'Mega Greninja ex Greninja ex', 'Magnezone Miraidon ex', 'lose'),
    ('忍蛙壓七夕青鳥忍蛙線', 'Mega Greninja ex Greninja ex', 'Mega Altaria ex Greninja', 'win'),
    ('蜥蜴王壓胡帕', 'Mega Sceptile ex Greninja', 'Hoopa ex Mega Absol ex', 'win'),
    ('蜥蜴王壓月亮伊布', 'Mega Sceptile ex Greninja', 'Umbreon Hydreigon', 'win'),
    ('蜥蜴王輸超級甲賀忍蛙', 'Mega Sceptile ex Greninja', 'Mega Greninja ex Greninja ex', 'lose'),
    ('超夢強線輸七夕青鳥忍蛙線', 'Mega Mewtwo X ex Mew ex', 'Mega Altaria ex Greninja', 'lose'),
    ('超夢強線輸胡帕', 'Mega Mewtwo X ex Mew ex', 'Hoopa ex Mega Absol ex', 'lose'),
    ('超夢強線壓蜂女王', 'Mega Mewtwo X ex Mew ex', 'Vespiquen ex Shuckle ex', 'win'),
    ('月亮伊布輸水君', 'Umbreon Hydreigon', 'Suicune ex Baxcalibur', 'lose'),
    ('月亮伊布輸七夕青鳥忍蛙線', 'Umbreon Hydreigon', 'Mega Altaria ex Greninja', 'lose'),
    ('月亮伊布輸胡帕', 'Umbreon Hydreigon', 'Hoopa ex Mega Absol ex', 'lose'),
    ('月亮伊布贏自爆磁怪', 'Umbreon Hydreigon', 'Magnezone Miraidon ex', 'win'),
    ('月亮伊布輸超級甲賀忍蛙', 'Umbreon Hydreigon', 'Mega Greninja ex Greninja ex', 'lose'),
    ('噴火龍 Y 輸水君', 'Mega Charizard Y ex Entei ex', 'Suicune ex Baxcalibur', 'lose'),
    ('噴火龍 Y 輸胡帕', 'Mega Charizard Y ex Entei ex', 'Hoopa ex Mega Absol ex', 'lose'),
    ('噴火龍 Y 輸七夕青鳥忍蛙線', 'Mega Charizard Y ex Entei ex', 'Mega Altaria ex Greninja', 'lose'),
    ('三首惡龍壓蜂女王', 'Hydreigon Mega Absol ex', 'Vespiquen ex Shuckle ex', 'win'),
    ('三首惡龍壓自爆磁怪', 'Hydreigon Mega Absol ex', 'Magnezone Miraidon ex', 'win'),
    ('三首惡龍輸七夕青鳥忍蛙線', 'Hydreigon Mega Absol ex', 'Mega Altaria ex Greninja', 'lose'),
    ('三首惡龍輸胡帕', 'Hydreigon Mega Absol ex', 'Hoopa ex Mega Absol ex', 'lose'),
]

err = 0
nmis = 0
print(f'共 {len(CLAIMS)} 條對位敘述')
for desc, a, b, direction in CLAIMS:
    va = M.get(a, {}).get(b)
    vb = M.get(b, {}).get(a)
    if va is None or vb is None:
        print(f'  ✗ 無資料: {desc}')
        err += 1
        continue
    ok = (va[0] >= 50) if direction == 'win' else (va[0] < 50)
    if not ok:
        err += 1
    if va[1] != vb[1]:
        nmis += 1
    old = Y.get(a, {}).get(b)
    delta = f'  Δ{va[0]-old[0]:+.1f}pt' if old else ''
    print(f"  {'✓' if ok else '✗'} {desc:28} A列 {va[0]:>5.1f}% N={va[1]:>4} | B列 {vb[0]:>5.1f}% N={vb[1]:>4}{delta}")

print(f'\n方向錯誤數：{err}/{len(CLAIMS)}')
print(f'N 不一致數：{nmis}/{len(CLAIMS)}')
if err or nmis:
    raise SystemExit(1)
