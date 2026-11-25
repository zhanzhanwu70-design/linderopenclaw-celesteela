#!/usr/bin/env python3
"""2026-11-23 對位分析：合併口徑（只併入 N>=50 顯著分支，對局數加權）。
口徑：
・A 壓 B p% → 取自 A 自己那一列（合併後）。
・A 輸 B p% → 取自 B 自己那一列（＝A 輸的比率）。
・平局會讓兩列之和小於 100%，禁止用 100−自身勝率 反推。
"""
import json
import re

M = json.load(open('memory/mu_matrix_20261124_c1.json', encoding='utf-8'))
EB = json.load(open('memory/ptcgp_meta_20261124_std.json', encoding='utf-8'))['rows']
MIN_N = 50


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


EB_NORM = {norm(r['name']): r['name'] for r in EB}


def resolve_matrix_key(name):
    if name in M:
        return name
    n = norm(name)
    for k in M:
        if norm(k) == n:
            return k
    return None


def sig_branches(comb, rows=EB):
    cands = [r for r in rows if r['name'] == comb or r['name'].startswith(comb + ' ')]
    return [r['name'] for r in cands if r['n'] >= MIN_N] or [comb]


def merged(comb_a, comb_b, matrix=M, rows=EB):
    opp_keys = set(sig_branches(comb_b, rows))
    tot = 0
    acc = 0.0
    for rn in sig_branches(comb_a, rows):
        mk = resolve_matrix_key(rn)
        if not mk:
            continue
        for k, (w, n) in matrix.get(mk, {}).items():
            if k in opp_keys:
                acc += w * n
                tot += n
    return (round(acc / tot, 1), tot) if tot else None


def wr_against(me, opp):
    return merged(me, opp)


def loses_to(me, opp):
    return merged(opp, me)


# 中文牌組 → 合併頁英文名
ZH2EN = {
    '自爆磁怪': 'Magnezone',
    '超級甲賀忍蛙 ex': 'Mega Greninja ex',
    '月亮伊布': 'Umbreon',
    '超級超夢 X ex': 'Mega Mewtwo X ex',
    '超級路卡利歐 ex': 'Mega Lucario ex',
    '超級蜥蜴王 ex': 'Mega Sceptile ex',
    '古劍豹 ex': 'Chien-Pao ex',
    '長耳兔': 'Lopunny',
    '超級噴火龍 Y ex': 'Mega Charizard Y ex',
    '胡帕 ex': 'Hoopa ex',
    '蜂女王 ex': 'Vespiquen ex',
    '三首惡龍': 'Hydreigon',
    '水君 ex': 'Suicune ex',
    '咚咚鼠 ex': 'Dedenne ex',
    '超級雷電獸 ex': 'Mega Manectric ex',
    '騎拉帝納 ex': 'Giratina ex',
    '超級盔甲鳥 ex': 'Mega Skarmory ex',
    '皮卡丘 ex': 'Pikachu ex',
    '超級班基拉斯 ex': 'Mega Bouffalant ex',
    '超級快龍 ex': 'Mega Dragonite ex',
    '超級七夕青鳥 ex': 'Mega Altaria ex',
    '超級蒂安希 ex': 'Mega Diancie ex',
    '超級大鋼蛇 ex': 'Mega Steelix ex',
}

TARGETS = [
    ('自爆磁怪', ['蜂女王 ex', '胡帕 ex', '超級甲賀忍蛙 ex', '水君 ex', '超級七夕青鳥 ex', '三首惡龍', '超級路卡利歐 ex', '月亮伊布', '超級噴火龍 Y ex', '超級超夢 X ex', '古劍豹 ex', '超級蜥蜴王 ex']),
    ('超級甲賀忍蛙 ex', ['水君 ex', '自爆磁怪', '蜂女王 ex', '超級雷電獸 ex', '超級七夕青鳥 ex', '胡帕 ex', '超級路卡利歐 ex']),
    ('月亮伊布', ['水君 ex', '超級七夕青鳥 ex', '胡帕 ex', '自爆磁怪', '超級超夢 X ex', '三首惡龍']),
    ('超級超夢 X ex', ['超級七夕青鳥 ex', '胡帕 ex', '蜂女王 ex', '水君 ex', '超級路卡利歐 ex']),
    ('超級路卡利歐 ex', ['超級七夕青鳥 ex', '超級噴火龍 Y ex', '蜂女王 ex', '水君 ex', '自爆磁怪', '胡帕 ex']),
    ('超級蜥蜴王 ex', ['超級噴火龍 Y ex', '超級甲賀忍蛙 ex', '胡帕 ex', '月亮伊布']),
    ('古劍豹 ex', ['超級七夕青鳥 ex', '蜂女王 ex', '胡帕 ex', '水君 ex', '自爆磁怪']),
    ('長耳兔', ['超級七夕青鳥 ex', '蜂女王 ex', '水君 ex', '胡帕 ex']),
    ('超級噴火龍 Y ex', ['超級七夕青鳥 ex', '胡帕 ex', '水君 ex', '自爆磁怪', '蜂女王 ex', '超級路卡利歐 ex']),
    ('胡帕 ex', ['超級七夕青鳥 ex', '水君 ex', '自爆磁怪', '超級甲賀忍蛙 ex', '蜂女王 ex', '三首惡龍']),
    ('蜂女王 ex', ['胡帕 ex', '水君 ex', '超級甲賀忍蛙 ex', '自爆磁怪', '超級路卡利歐 ex', '超級超夢 X ex']),
    ('三首惡龍', ['自爆磁怪', '蜂女王 ex', '超級七夕青鳥 ex', '胡帕 ex', '月亮伊布', '超級噴火龍 Y ex']),
    ('水君 ex', ['超級甲賀忍蛙 ex', '自爆磁怪', '超級七夕青鳥 ex', '胡帕 ex', '蜂女王 ex', '超級盔甲鳥 ex', '超級超夢 X ex', '超級路卡利歐 ex']),
    ('咚咚鼠 ex', ['蜂女王 ex', '自爆磁怪', '超級雷電獸 ex', '胡帕 ex']),
    ('超級雷電獸 ex', ['水君 ex', '超級七夕青鳥 ex', '自爆磁怪', '胡帕 ex']),
    ('騎拉帝納 ex', ['自爆磁怪', '超級七夕青鳥 ex', '胡帕 ex', '水君 ex']),
    ('超級盔甲鳥 ex', ['超級噴火龍 Y ex', '水君 ex', '蜂女王 ex']),
    ('皮卡丘 ex', ['自爆磁怪', '超級七夕青鳥 ex', '蜂女王 ex', '水君 ex']),
    ('超級班基拉斯 ex', ['自爆磁怪', '超級七夕青鳥 ex', '蜂女王 ex', '水君 ex']),
    ('超級快龍 ex', ['超級七夕青鳥 ex', '水君 ex', '蜂女王 ex']),
    ('超級七夕青鳥 ex', ['自爆磁怪', '胡帕 ex', '水君 ex', '蜂女王 ex', '超級路卡利歐 ex', '超級甲賀忍蛙 ex', '超級噴火龍 Y ex']),
]

print('### 對位報告（合併口徑；「壓」= 自身勝率，「輸」= 對方那一列對我的勝率）')
OUT = {}
for me, opps in TARGETS:
    en_me = ZH2EN.get(me, me)
    print(f'\n== {me}  [{en_me}]')
    OUT[me] = {}
    for o in opps:
        en_o = ZH2EN.get(o, o)
        a = wr_against(en_me, en_o)
        b = loses_to(en_me, en_o)
        sa = f'壓 {a[0]:.1f}%(N={a[1]})' if a else '壓 --'
        sb = f'輸 {b[0]:.1f}%(N={b[1]})' if b else '輸 --'
        print(f'   vs {o[:24]:26} {sa:18} {sb}')
        OUT[me][o] = {'win': a, 'lose': b}

json.dump(OUT, open('memory/mu_report_20261124.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
