#!/usr/bin/env python3
"""2026-11-22 對位數字覆核。
口徑：每一列的數值＝被檢視的那副牌自己對該對手的勝率。
・A 壓 B p% → 取自 A 自己那一列。
・A 輸 B p% → 取自 B 自己那一列（＝A 輸的比率）；平局會讓兩列之和小於 100%，禁止用 100−自身勝率 反推。
・合併口徑只併入顯著分支（分支 N>=50），並以對局數加權。
"""
import json

M = json.load(open('memory/mu_matrix_20261122_c1.json', encoding='utf-8'))
Y = json.load(open('memory/mu_matrix_20261121_c1.json', encoding='utf-8'))
EB = json.load(open('memory/ptcgp_meta_20261122_std.json', encoding='utf-8'))['rows']
EBY = json.load(open('memory/ptcgp_meta_20261121_std_re2.json', encoding='utf-8'))['rows']
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


MERGED_CLAIMS = [
    ('自爆磁怪壓蜂女王', 'Magnezone', 'Vespiquen ex', 'win'),
    ('自爆磁怪壓胡帕', 'Magnezone', 'Hoopa ex', 'win'),
    ('自爆磁怪壓超級甲賀忍蛙', 'Magnezone', 'Mega Greninja ex', 'win'),
    ('自爆磁怪壓水君', 'Magnezone', 'Suicune ex', 'win'),
    ('自爆磁怪輸超級七夕青鳥', 'Magnezone', 'Mega Altaria ex', 'lose'),
    ('自爆磁怪輸三首惡龍', 'Magnezone', 'Hydreigon', 'lose'),
    ('自爆磁怪輸超級路卡利歐', 'Magnezone', 'Mega Lucario ex', 'lose'),
    ('自爆磁怪輸月亮伊布', 'Magnezone', 'Umbreon', 'lose'),
    ('自爆磁怪輸噴火龍Y', 'Magnezone', 'Mega Charizard Y ex', 'lose'),
    ('三首惡龍壓自爆磁怪', 'Hydreigon', 'Magnezone', 'win'),
    ('三首惡龍壓蜂女王', 'Hydreigon', 'Vespiquen ex', 'win'),
    ('三首惡龍輸超級七夕青鳥', 'Hydreigon', 'Mega Altaria ex', 'lose'),
    ('三首惡龍輸胡帕', 'Hydreigon', 'Hoopa ex', 'lose'),
    ('三首惡龍輸月亮伊布', 'Hydreigon', 'Umbreon', 'lose'),
    ('三首惡龍勝超級噴火龍Y', 'Hydreigon', 'Mega Charizard Y ex', 'win'),
    ('蜂女王壓胡帕', 'Vespiquen ex', 'Hoopa ex', 'win'),
    ('蜂女王壓水君', 'Vespiquen ex', 'Suicune ex', 'win'),
    ('蜂女王壓超級甲賀忍蛙', 'Vespiquen ex', 'Mega Greninja ex', 'win'),
    ('蜂女王輸自爆磁怪', 'Vespiquen ex', 'Magnezone', 'lose'),
    ('蜂女王輸超級路卡利歐', 'Vespiquen ex', 'Mega Lucario ex', 'lose'),
    ('蜂女王輸超級超夢X', 'Vespiquen ex', 'Mega Mewtwo X ex', 'lose'),
    ('蜂女王輸噴火龍Y', 'Vespiquen ex', 'Mega Charizard Y ex', 'lose'),
    ('胡帕壓超級七夕青鳥', 'Hoopa ex', 'Mega Altaria ex', 'win'),
    ('胡帕壓水君', 'Hoopa ex', 'Suicune ex', 'win'),
    ('胡帕壓超級噴火龍Y', 'Hoopa ex', 'Mega Charizard Y ex', 'win'),
    ('胡帕壓超級超夢X', 'Hoopa ex', 'Mega Mewtwo X ex', 'win'),
    ('胡帕勝超級甲賀忍蛙', 'Hoopa ex', 'Mega Greninja ex', 'win'),
    ('胡帕輸蜂女王', 'Hoopa ex', 'Vespiquen ex', 'lose'),
    ('胡帕輸超級路卡利歐', 'Hoopa ex', 'Mega Lucario ex', 'lose'),
    ('七夕青鳥壓超級路卡利歐', 'Mega Altaria ex', 'Mega Lucario ex', 'win'),
    ('七夕青鳥壓超級超夢X', 'Mega Altaria ex', 'Mega Mewtwo X ex', 'win'),
    ('七夕青鳥壓月亮伊布', 'Mega Altaria ex', 'Umbreon', 'win'),
    ('七夕青鳥壓水君', 'Mega Altaria ex', 'Suicune ex', 'win'),
    ('七夕青鳥輸胡帕', 'Mega Altaria ex', 'Hoopa ex', 'lose'),
    ('七夕青鳥輸超級甲賀忍蛙', 'Mega Altaria ex', 'Mega Greninja ex', 'lose'),
    ('七夕青鳥勝噴火龍Y', 'Mega Altaria ex', 'Mega Charizard Y ex', 'win'),
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
    ('月亮伊布輸水君', 'Umbreon', 'Suicune ex', 'lose'),
    ('月亮伊布輸七夕青鳥', 'Umbreon', 'Mega Altaria ex', 'lose'),
    ('月亮伊布輸胡帕', 'Umbreon', 'Hoopa ex', 'lose'),
    ('月亮伊布壓自爆磁怪', 'Umbreon', 'Magnezone', 'win'),
    ('月亮伊布壓超級超夢X', 'Umbreon', 'Mega Mewtwo X ex', 'win'),
    ('超級甲賀忍蛙輸水君', 'Mega Greninja ex', 'Suicune ex', 'lose'),
    ('超級甲賀忍蛙輸自爆磁怪', 'Mega Greninja ex', 'Magnezone', 'lose'),
    ('超級甲賀忍蛙輸蜂女王', 'Mega Greninja ex', 'Vespiquen ex', 'lose'),
    ('超級甲賀忍蛙壓七夕青鳥', 'Mega Greninja ex', 'Mega Altaria ex', 'win'),
    ('超級甲賀忍蛙輸胡帕', 'Mega Greninja ex', 'Hoopa ex', 'lose'),
    ('超級甲賀忍蛙輸雷電獸', 'Mega Greninja ex', 'Mega Manectric ex', 'lose'),
    ('超級甲賀忍蛙輸路卡利歐', 'Mega Greninja ex', 'Mega Lucario ex', 'lose'),
    ('超級路卡利歐壓蜂女王', 'Mega Lucario ex', 'Vespiquen ex', 'win'),
    ('超級路卡利歐壓水君', 'Mega Lucario ex', 'Suicune ex', 'win'),
    ('超級路卡利歐輸超夢X', 'Mega Lucario ex', 'Mega Mewtwo X ex', 'lose'),
    ('超級路卡利歐勝胡帕', 'Mega Lucario ex', 'Hoopa ex', 'win'),
    ('超級路卡利歐輸七夕青鳥', 'Mega Lucario ex', 'Mega Altaria ex', 'lose'),
    ('超級路卡利歐壓自爆磁怪', 'Mega Lucario ex', 'Magnezone', 'win'),
    ('超級路卡利歐輸噴火龍Y', 'Mega Lucario ex', 'Mega Charizard Y ex', 'lose'),
    ('超級超夢X輸胡帕', 'Mega Mewtwo X ex', 'Hoopa ex', 'lose'),
    ('超級超夢X輸七夕青鳥', 'Mega Mewtwo X ex', 'Mega Altaria ex', 'lose'),
    ('超級超夢X壓蜂女王', 'Mega Mewtwo X ex', 'Vespiquen ex', 'win'),
    ('超級蜥蜴王輸噴火龍Y', 'Mega Sceptile ex', 'Mega Charizard Y ex', 'lose'),
    ('超級蜥蜴王輸超級甲賀忍蛙', 'Mega Sceptile ex', 'Mega Greninja ex', 'lose'),
    ('超級蜥蜴王壓胡帕', 'Mega Sceptile ex', 'Hoopa ex', 'win'),
    ('超級蜥蜴王壓月亮伊布', 'Mega Sceptile ex', 'Umbreon', 'win'),
    ('咚咚鼠壓蜂女王', 'Dedenne ex', 'Vespiquen ex', 'win'),
    ('咚咚鼠輸自爆磁怪', 'Dedenne ex', 'Magnezone', 'lose'),
    ('咚咚鼠輸雷電獸', 'Dedenne ex', 'Mega Manectric ex', 'lose'),
]

BRANCH_CLAIMS = [
    ('胡帕壓七夕青鳥-超級阿勃梭魯線', 'Hoopa ex Mega Absol ex', 'Mega Altaria ex Espeon', 'win'),
    ('胡帕壓七夕青鳥-忍蛙線', 'Hoopa ex Mega Absol ex', 'Mega Altaria ex Greninja', 'win'),
    ('七夕青鳥太陽伊布線輸胡帕', 'Mega Altaria ex Espeon', 'Hoopa ex Mega Absol ex', 'lose'),
    ('七夕青鳥忍蛙線輸胡帕', 'Mega Altaria ex Greninja', 'Hoopa ex Mega Absol ex', 'lose'),
    ('自爆磁怪密勒頓線壓蜂女王', 'Magnezone Miraidon ex', 'Vespiquen ex Shuckle ex', 'win'),
    ('自爆磁怪密勒頓線壓七夕青鳥忍蛙線', 'Magnezone Miraidon ex', 'Mega Altaria ex Greninja', 'win'),
    ('自爆磁怪密勒頓線輸七夕青鳥太陽線', 'Magnezone Miraidon ex', 'Mega Altaria ex Espeon', 'lose'),
    ('三首惡龍阿勃梭魯線壓自爆磁怪', 'Hydreigon Mega Absol ex', 'Magnezone Miraidon ex', 'win'),
    ('三首惡龍阿勃梭魯線輸七夕青鳥', 'Hydreigon Mega Absol ex', 'Mega Altaria ex Greninja', 'lose'),
    ('蜂女王壺壺線輸自爆磁怪', 'Vespiquen ex Shuckle ex', 'Magnezone Miraidon ex', 'lose'),
    ('蜂女王壺壺線壓胡帕', 'Vespiquen ex Shuckle ex', 'Hoopa ex Mega Absol ex', 'win'),
    ('咚咚鼠愛管侍線壓蜂女王', 'Dedenne ex Indeedee ex', 'Vespiquen ex Shuckle ex', 'win'),
    ('咚咚鼠愛管侍線輸自爆磁怪', 'Dedenne ex Indeedee ex', 'Magnezone Miraidon ex', 'lose'),
]

fail = 0
for name, a, b, d in MERGED_CLAIMS:
    own = merged(a, b)
    opp = merged(b, a)
    y = merged(a, b, Y, EBY)
    if not own or not opp:
        print(f'  MISSING {name}: own={own} opp={opp}')
        fail += 1
        continue
    ok = (own[0] > opp[0]) if d == 'win' else (own[0] < opp[0])
    tag = 'OK ' if ok else 'FAIL'
    if not ok:
        fail += 1
    print(f'  {tag} {name:34} A側 {own[0]:>5.1f}% N={own[1]:>4} | B側 {opp[0]:>5.1f}% N={opp[1]:>4} | 昨 {y[0] if y else 0:>5.1f}% N={y[1] if y else 0:>4}')

print()
for name, a, b, d in BRANCH_CLAIMS:
    ra = M.get(a, {}).get(b)
    rb = M.get(b, {}).get(a)
    if not ra or not rb:
        print(f'  MISSING {name}: {ra} {rb}')
        fail += 1
        continue
    ok = (ra[0] > rb[0]) if d == 'win' else (ra[0] < rb[0])
    tag = 'OK ' if ok else 'FAIL'
    if not ok:
        fail += 1
    print(f'  {tag} {name:34} {a[:26]:28} {ra[0]:>5.1f}% N={ra[1]:>4} | 反向 {rb[0]:>5.1f}% N={rb[1]:>4}')

print()
print('### 古劍豹（分支層級）')
for opp, d in [('Mega Altaria ex Greninja', 'lose'), ('Mega Altaria ex Espeon', 'lose'),
               ('Vespiquen ex Shuckle ex', 'lose'), ('Mega Charizard Y ex Entei ex', 'win'),
               ('Hoopa ex Mega Absol ex', 'lose'), ('Suicune ex Baxcalibur', 'win')]:
    ra = M.get('Chien-Pao ex Baxcalibur', {}).get(opp)
    rb = M.get(opp, {}).get('Chien-Pao ex Baxcalibur')
    if not ra or not rb:
        print(f'  MISSING vs {opp}: {ra} {rb}')
        fail += 1
        continue
    ok = (ra[0] > rb[0]) if d == 'win' else (ra[0] < rb[0])
    if not ok:
        fail += 1
    print(f'  {"OK " if ok else "FAIL"} 古劍豹 vs {opp:28} {ra[0]:>5.1f}% N={ra[1]:>4} | 反向 {rb[0]:>5.1f}% N={rb[1]:>4}')

print()
print('分支/合併 條數：', len(MERGED_CLAIMS) + len(BRANCH_CLAIMS), '失敗：', fail)
