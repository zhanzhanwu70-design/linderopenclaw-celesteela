#!/usr/bin/env python3
"""2026-11-20 對位數字覆核。
口徑：每一列的數值＝被檢視的那副牌自己對該對手的勝率。
・A 壓 B p% → 取自 A 自己那一列。
・A 輸 B p% → 取自 B 那一列（＝A 輸的比率）；平局會讓兩列之和小於 100%，禁止用 100−自身勝率 反推。
・合併口徑只併入顯著分支（分支 N>=50），並以對局數加權。
"""
import json

M = json.load(open('memory/mu_matrix_20261120_c1.json', encoding='utf-8'))
Y = json.load(open('memory/mu_matrix_20261119_c1.json', encoding='utf-8'))
EB = json.load(open('memory/ptcgp_meta_20261120_std.json', encoding='utf-8'))['rows']
EB18 = json.load(open('memory/ptcgp_meta_20261119_std_re.json', encoding='utf-8'))['rows']
MIN_N = 50


def sig_branches(comb, rows=EB):
    cands = [r for r in rows if r['name'] == comb or r['name'].startswith(comb + ' ')]
    return [r['name'] for r in cands if r['n'] >= MIN_N] or [comb]


def merged(comb_a, comb_b, matrix=M, rows=EB):
    opp_keys = set(sig_branches(comb_b, rows))
    tot = 0
    acc = 0.0
    for rn in sig_branches(comb_a, rows):
        for k, (w, n) in matrix.get(rn, {}).items():
            if k in opp_keys:
                acc += w * n
                tot += n
    return (round(acc / tot, 1), tot) if tot else None


# ---- 合併口徑敘述：說明, A, B, 期望方向 ----
MERGED_CLAIMS = [
    ('自爆磁怪壓蜂女王', 'Magnezone', 'Vespiquen ex', 'win'),
    ('自爆磁怪壓胡帕', 'Magnezone', 'Hoopa ex', 'win'),
    ('自爆磁怪壓超級甲賀忍蛙', 'Magnezone', 'Mega Greninja ex', 'win'),
    ('自爆磁怪壓水君', 'Magnezone', 'Suicune ex', 'win'),
    ('自爆磁怪輸超級七夕青鳥', 'Magnezone', 'Mega Altaria ex', 'lose'),
    ('自爆磁怪輸三首惡龍', 'Magnezone', 'Hydreigon', 'lose'),
    ('自爆磁怪輸超級路卡利歐', 'Magnezone', 'Mega Lucario ex', 'lose'),
    ('自爆磁怪輸月亮伊布', 'Magnezone', 'Umbreon', 'lose'),
    ('自爆磁怪輸超級噴火龍Y', 'Magnezone', 'Mega Charizard Y ex', 'lose'),
    ('三首惡龍壓蜂女王', 'Hydreigon', 'Vespiquen ex', 'win'),
    ('三首惡龍壓自爆磁怪', 'Hydreigon', 'Magnezone', 'win'),
    ('三首惡龍輸超級七夕青鳥', 'Hydreigon', 'Mega Altaria ex', 'lose'),
    ('三首惡龍輸胡帕', 'Hydreigon', 'Hoopa ex', 'lose'),
    ('三首惡龍輸月亮伊布', 'Hydreigon', 'Umbreon', 'lose'),
    ('三首惡龍勝超級噴火龍Y', 'Hydreigon', 'Mega Charizard Y ex', 'win'),
    ('蜂女王壓胡帕', 'Vespiquen ex', 'Hoopa ex', 'win'),
    ('蜂女王壓水君', 'Vespiquen ex', 'Suicune ex', 'win'),
    ('蜂女王輸自爆磁怪', 'Vespiquen ex', 'Magnezone', 'lose'),
    ('蜂女王輸超級路卡利歐', 'Vespiquen ex', 'Mega Lucario ex', 'lose'),
    ('蜂女王輸超級超夢X', 'Vespiquen ex', 'Mega Mewtwo X ex', 'lose'),
    ('胡帕壓超級七夕青鳥', 'Hoopa ex', 'Mega Altaria ex', 'win'),
    ('胡帕壓水君', 'Hoopa ex', 'Suicune ex', 'win'),
    ('胡帕壓超級噴火龍Y', 'Hoopa ex', 'Mega Charizard Y ex', 'win'),
    ('胡帕壓超級超夢X', 'Hoopa ex', 'Mega Mewtwo X ex', 'win'),
    ('胡帕輸蜂女王', 'Hoopa ex', 'Vespiquen ex', 'lose'),
    ('胡帕輸超級路卡利歐', 'Hoopa ex', 'Mega Lucario ex', 'lose'),
    ('胡帕勝超級甲賀忍蛙', 'Hoopa ex', 'Mega Greninja ex', 'win'),
    ('七夕青鳥壓超級路卡利歐', 'Mega Altaria ex', 'Mega Lucario ex', 'win'),
    ('七夕青鳥壓超級超夢X', 'Mega Altaria ex', 'Mega Mewtwo X ex', 'win'),
    ('七夕青鳥壓月亮伊布', 'Mega Altaria ex', 'Umbreon', 'win'),
    ('七夕青鳥輸胡帕', 'Mega Altaria ex', 'Hoopa ex', 'lose'),
    ('七夕青鳥壓水君', 'Mega Altaria ex', 'Suicune ex', 'win'),
    ('七夕青鳥輸超級甲賀忍蛙', 'Mega Altaria ex', 'Mega Greninja ex', 'lose'),
    ('七夕青鳥勝超級噴火龍Y', 'Mega Altaria ex', 'Mega Charizard Y ex', 'win'),
    ('水君壓超級甲賀忍蛙', 'Suicune ex', 'Mega Greninja ex', 'win'),
    ('水君壓超級噴火龍Y', 'Suicune ex', 'Mega Charizard Y ex', 'win'),
    ('水君輸蜂女王', 'Suicune ex', 'Vespiquen ex', 'lose'),
    ('水君輸超級七夕青鳥', 'Suicune ex', 'Mega Altaria ex', 'lose'),
    ('水君輸胡帕', 'Suicune ex', 'Hoopa ex', 'lose'),
    ('水君輸自爆磁怪', 'Suicune ex', 'Magnezone', 'lose'),
    ('噴火龍Y輸水君', 'Mega Charizard Y ex', 'Suicune ex', 'lose'),
    ('噴火龍Y輸胡帕', 'Mega Charizard Y ex', 'Hoopa ex', 'lose'),
    ('噴火龍Y輸七夕青鳥', 'Mega Charizard Y ex', 'Mega Altaria ex', 'lose'),
    ('噴火龍Y壓路卡利歐', 'Mega Charizard Y ex', 'Mega Lucario ex', 'win'),
    ('噴火龍Y壓超夢X', 'Mega Charizard Y ex', 'Mega Mewtwo X ex', 'win'),
    ('月亮伊布輸七夕青鳥', 'Umbreon', 'Mega Altaria ex', 'lose'),
    ('月亮伊布輸水君', 'Umbreon', 'Suicune ex', 'lose'),
    ('月亮伊布輸胡帕', 'Umbreon', 'Hoopa ex', 'lose'),
    ('月亮伊布贏自爆磁怪', 'Umbreon', 'Magnezone', 'win'),
    ('月亮伊布壓超夢X', 'Umbreon', 'Mega Mewtwo X ex', 'win'),
    ('超夢X輸七夕青鳥', 'Mega Mewtwo X ex', 'Mega Altaria ex', 'lose'),
    ('超夢X輸胡帕', 'Mega Mewtwo X ex', 'Hoopa ex', 'lose'),
    ('超夢X壓蜂女王', 'Mega Mewtwo X ex', 'Vespiquen ex', 'win'),
    ('路卡利歐輸七夕青鳥', 'Mega Lucario ex', 'Mega Altaria ex', 'lose'),
    ('路卡利歐壓自爆磁怪', 'Mega Lucario ex', 'Magnezone', 'win'),
    ('路卡利歐壓蜂女王', 'Mega Lucario ex', 'Vespiquen ex', 'win'),
    ('路卡利歐勝胡帕', 'Mega Lucario ex', 'Hoopa ex', 'win'),
    ('忍蛙輸水君', 'Mega Greninja ex', 'Suicune ex', 'lose'),
    ('忍蛙輸自爆磁怪', 'Mega Greninja ex', 'Magnezone', 'lose'),
    ('忍蛙輸胡帕', 'Mega Greninja ex', 'Hoopa ex', 'lose'),
    ('忍蛙壓七夕青鳥', 'Mega Greninja ex', 'Mega Altaria ex', 'win'),
    ('忍蛙輸雷電獸', 'Mega Greninja ex', 'Mega Manectric ex', 'lose'),
    ('蜥蜴王輸水君', 'Mega Sceptile ex', 'Suicune ex', 'lose'),
    ('蜥蜴王輸自爆磁怪', 'Mega Sceptile ex', 'Magnezone', 'lose'),
    ('蜥蜴王勝胡帕', 'Mega Sceptile ex', 'Hoopa ex', 'win'),
    ('皮卡丘輸胡帕', 'Pikachu ex', 'Hoopa ex', 'lose'),
    ('皮卡丘贏自爆磁怪', 'Pikachu ex', 'Magnezone', 'win'),
]

# ---- 分支行敘述：說明, A 列, B 列, 期望方向 ----
BRANCH_CLAIMS = [
    ('自爆磁怪勝七夕青鳥忍蛙線', 'Magnezone Miraidon ex', 'Mega Altaria ex Greninja', 'win'),
    ('自爆磁怪輸七夕青鳥太陽伊布線', 'Magnezone Miraidon ex', 'Mega Altaria ex Espeon', 'lose'),
    ('七夕青鳥忍蛙線壓路卡利歐', 'Mega Altaria ex Greninja', 'Mega Lucario ex Lucario', 'win'),
    ('七夕青鳥忍蛙線壓超夢強線', 'Mega Altaria ex Greninja', 'Mega Mewtwo X ex Mew ex', 'win'),
    ('七夕青鳥忍蛙線壓月亮伊布', 'Mega Altaria ex Greninja', 'Umbreon Hydreigon', 'win'),
    ('七夕青鳥忍蛙線輸胡帕', 'Mega Altaria ex Greninja', 'Hoopa ex Mega Absol ex', 'lose'),
    ('七夕青鳥忍蛙線壓水君', 'Mega Altaria ex Greninja', 'Suicune ex Baxcalibur', 'win'),
    ('七夕青鳥忍蛙線輸超級甲賀忍蛙', 'Mega Altaria ex Greninja', 'Mega Greninja ex Greninja ex', 'lose'),
    ('七夕青鳥忍蛙線勝超級噴火龍Y', 'Mega Altaria ex Greninja', 'Mega Charizard Y ex Entei ex', 'win'),
    ('七夕青鳥太陽伊布線壓路卡利歐', 'Mega Altaria ex Espeon', 'Mega Lucario ex Lucario', 'win'),
    ('七夕青鳥太陽伊布線壓超夢強線', 'Mega Altaria ex Espeon', 'Mega Mewtwo X ex Mew ex', 'win'),
    ('七夕青鳥太陽伊布線壓月亮伊布', 'Mega Altaria ex Espeon', 'Umbreon Hydreigon', 'win'),
    ('七夕青鳥太陽伊布線輸胡帕', 'Mega Altaria ex Espeon', 'Hoopa ex Mega Absol ex', 'lose'),
    ('七夕青鳥太陽伊布線壓水君', 'Mega Altaria ex Espeon', 'Suicune ex Baxcalibur', 'win'),
    ('七夕青鳥太陽伊布線輸超級甲賀忍蛙', 'Mega Altaria ex Espeon', 'Mega Greninja ex Greninja ex', 'lose'),
    ('七夕青鳥太陽伊布線勝超級噴火龍Y', 'Mega Altaria ex Espeon', 'Mega Charizard Y ex Entei ex', 'win'),
    ('忍蛙線輸水君', 'Mega Greninja ex Greninja ex', 'Suicune ex Baxcalibur', 'lose'),
    ('忍蛙線輸自爆磁怪', 'Mega Greninja ex Greninja ex', 'Magnezone Miraidon ex', 'lose'),
    ('忍蛙線輸胡帕', 'Mega Greninja ex Greninja ex', 'Hoopa ex Mega Absol ex', 'lose'),
    ('忍蛙線壓七夕青鳥忍蛙線', 'Mega Greninja ex Greninja ex', 'Mega Altaria ex Greninja', 'win'),
    ('忍蛙線輸雷電獸', 'Mega Greninja ex Greninja ex', 'Mega Manectric ex Heliolisk', 'lose'),
    ('路卡利歐輸七夕青鳥忍蛙線', 'Mega Lucario ex Lucario', 'Mega Altaria ex Greninja', 'lose'),
    ('路卡利歐輸七夕青鳥太陽伊布線', 'Mega Lucario ex Lucario', 'Mega Altaria ex Espeon', 'lose'),
    ('路卡利歐壓自爆磁怪', 'Mega Lucario ex Lucario', 'Magnezone Miraidon ex', 'win'),
    ('路卡利歐壓蜂女王', 'Mega Lucario ex Lucario', 'Vespiquen ex Shuckle ex', 'win'),
    ('路卡利歐勝胡帕', 'Mega Lucario ex Lucario', 'Hoopa ex Mega Absol ex', 'win'),
    ('超夢強線輸七夕青鳥忍蛙線', 'Mega Mewtwo X ex Mew ex', 'Mega Altaria ex Greninja', 'lose'),
    ('超夢強線輸胡帕', 'Mega Mewtwo X ex Mew ex', 'Hoopa ex Mega Absol ex', 'lose'),
    ('超夢強線壓蜂女王', 'Mega Mewtwo X ex Mew ex', 'Vespiquen ex Shuckle ex', 'win'),
    ('超夢強線輸自爆磁怪', 'Mega Mewtwo X ex Mew ex', 'Magnezone Miraidon ex', 'lose'),
    ('蜂女王輸自爆磁怪', 'Vespiquen ex Shuckle ex', 'Magnezone Miraidon ex', 'lose'),
    ('蜂女王輸路卡利歐', 'Vespiquen ex Shuckle ex', 'Mega Lucario ex Lucario', 'lose'),
    ('蜂女王壓胡帕', 'Vespiquen ex Shuckle ex', 'Hoopa ex Mega Absol ex', 'win'),
    ('蜂女王壓水君', 'Vespiquen ex Shuckle ex', 'Suicune ex Baxcalibur', 'win'),
    ('胡帕壓七夕青鳥忍蛙線', 'Hoopa ex Mega Absol ex', 'Mega Altaria ex Greninja', 'win'),
    ('胡帕壓七夕青鳥太陽伊布線', 'Hoopa ex Mega Absol ex', 'Mega Altaria ex Espeon', 'win'),
    ('胡帕輸蜂女王', 'Hoopa ex Mega Absol ex', 'Vespiquen ex Shuckle ex', 'lose'),
    ('胡帕輸路卡利歐', 'Hoopa ex Mega Absol ex', 'Mega Lucario ex Lucario', 'lose'),
    ('胡帕壓水君', 'Hoopa ex Mega Absol ex', 'Suicune ex Baxcalibur', 'win'),
    ('胡帕壓噴火龍Y', 'Hoopa ex Mega Absol ex', 'Mega Charizard Y ex Entei ex', 'win'),
    ('胡帕壓超級甲賀忍蛙', 'Hoopa ex Mega Absol ex', 'Mega Greninja ex Greninja ex', 'win'),
    ('水君壓忍蛙', 'Suicune ex Baxcalibur', 'Mega Greninja ex Greninja ex', 'win'),
    ('水君壓噴火龍Y', 'Suicune ex Baxcalibur', 'Mega Charizard Y ex Entei ex', 'win'),
    ('水君輸七夕青鳥忍蛙線', 'Suicune ex Baxcalibur', 'Mega Altaria ex Greninja', 'lose'),
    ('水君輸七夕青鳥太陽伊布線', 'Suicune ex Baxcalibur', 'Mega Altaria ex Espeon', 'lose'),
    ('水君輸胡帕', 'Suicune ex Baxcalibur', 'Hoopa ex Mega Absol ex', 'lose'),
    ('水君輸自爆磁怪', 'Suicune ex Baxcalibur', 'Magnezone Miraidon ex', 'lose'),
    ('噴火龍Y輸水君', 'Mega Charizard Y ex Entei ex', 'Suicune ex Baxcalibur', 'lose'),
    ('噴火龍Y輸胡帕', 'Mega Charizard Y ex Entei ex', 'Hoopa ex Mega Absol ex', 'lose'),
    ('噴火龍Y輸七夕青鳥忍蛙線', 'Mega Charizard Y ex Entei ex', 'Mega Altaria ex Greninja', 'lose'),
    ('噴火龍Y壓路卡利歐', 'Mega Charizard Y ex Entei ex', 'Mega Lucario ex Lucario', 'win'),
    ('噴火龍Y輸超夢強線', 'Mega Charizard Y ex Entei ex', 'Mega Mewtwo X ex Mew ex', 'lose'),
    ('噴火龍Y壓超夢蒂安希線', 'Mega Charizard Y ex Entei ex', 'Mega Mewtwo X ex Mega Diancie ex', 'win'),
    ('月亮伊布輸七夕青鳥', 'Umbreon Hydreigon', 'Mega Altaria ex Greninja', 'lose'),
    ('月亮伊布輸水君', 'Umbreon Hydreigon', 'Suicune ex Baxcalibur', 'lose'),
    ('月亮伊布輸胡帕', 'Umbreon Hydreigon', 'Hoopa ex Mega Absol ex', 'lose'),
    ('月亮伊布贏自爆磁怪', 'Umbreon Hydreigon', 'Magnezone Miraidon ex', 'win'),
    ('三首惡龍壓自爆磁怪', 'Hydreigon Mega Absol ex', 'Magnezone Miraidon ex', 'win'),
    ('三首惡龍輸七夕青鳥', 'Hydreigon Mega Absol ex', 'Mega Altaria ex Greninja', 'lose'),
    ('三首惡龍輸胡帕', 'Hydreigon Mega Absol ex', 'Hoopa ex Mega Absol ex', 'lose'),
    ('三首惡龍勝噴火龍Y', 'Hydreigon Mega Absol ex', 'Mega Charizard Y ex Entei ex', 'win'),
    ('古劍豹壓噴火龍Y', 'Chien-Pao ex Baxcalibur', 'Mega Charizard Y ex Entei ex', 'win'),
    ('古劍豹輸七夕青鳥', 'Chien-Pao ex Baxcalibur', 'Mega Altaria ex Greninja', 'lose'),
    ('古劍豹輸胡帕', 'Chien-Pao ex Baxcalibur', 'Hoopa ex Mega Absol ex', 'lose'),
    ('古劍豹壓水君', 'Chien-Pao ex Baxcalibur', 'Suicune ex Baxcalibur', 'win'),
    ('皮卡丘輸胡帕', 'Pikachu ex Pawmot', 'Hoopa ex Mega Absol ex', 'lose'),
    ('皮卡丘勝自爆磁怪', 'Pikachu ex Pawmot', 'Magnezone Miraidon ex', 'win'),
    ('蜥蜴王勝胡帕', 'Mega Sceptile ex Greninja', 'Hoopa ex Mega Absol ex', 'win'),
    ('蜥蜴王輸水君', 'Mega Sceptile ex Greninja', 'Suicune ex Baxcalibur', 'lose'),
    ('蜥蜴王輸自爆磁怪', 'Mega Sceptile ex Greninja', 'Magnezone Miraidon ex', 'lose'),
]

err = 0
print(f'=== 合併口徑：{len(MERGED_CLAIMS)} 條 ===')
for desc, a, b, direction in MERGED_CLAIMS:
    va = merged(a, b)
    vb = merged(b, a)
    if va is None or vb is None:
        print(f'  ✗ 無資料: {desc}')
        err += 1
        continue
    ok = (va[0] >= 50) if direction == 'win' else (va[0] < 50)
    if not ok:
        err += 1
    p = merged(a, b, Y, EB18)
    delta = f'  Δ{va[0]-p[0]:+.1f}pt' if p else ''
    print(f"  {'✓' if ok else '✗'} {desc:24} A列 {va[0]:>5.1f}% N={va[1]:>4} | B列 {vb[0]:>5.1f}% N={vb[1]:>4}{delta}")

print(f'\n=== 分支行：{len(BRANCH_CLAIMS)} 條 ===')
for desc, a, b, direction in BRANCH_CLAIMS:
    va = M.get(a, {}).get(b)
    vb = M.get(b, {}).get(a)
    if va is None or vb is None:
        print(f'  ✗ 無資料: {desc}')
        err += 1
        continue
    ok = (va[0] >= 50) if direction == 'win' else (va[0] < 50)
    if not ok:
        err += 1
    print(f"  {'✓' if ok else '✗'} {desc:26} A列 {va[0]:>5.1f}% N={va[1]:>4} | B列 {vb[0]:>5.1f}% N={vb[1]:>4}")

print(f'\n錯誤 {err} 條')
