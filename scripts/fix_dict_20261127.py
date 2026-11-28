#!/usr/bin/env python3
"""2026-11-27 字典維護：修補既有損壞條目 + 補齊今日新出現牌組名。

損壞條目成因：先前自動分段翻譯把部分卡名誤切（例如把 'Chandelure' 切出 'Chandel' + '...'），
產生 '伽勒爾搖籃 ab' / '野蠻 roc ab' / '幻achines ex' / '叉字蝠 異 Uop ab' 這類含拉丁雜訊的假譯名。
本輪改成「顯式對照表 + 以 card_names 為唯一真值來源」重建，不再依賴自動分段。
"""
import collections
import json
import re

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
cn = D['card_names']
dn = D['deck_names']

# ---- 1. 修補 card_names 中鍵值顛倒的條目 ----
CARD_FIX = {
    'Toxtricity': '電音魔',
    'Toxtricity ex': '電音魔 ex',
}
card_fixed = []
for en, zh in CARD_FIX.items():
    if en in cn and cn[en] != zh:
        old = cn.pop(en)
        card_fixed.append((en, old, zh))
    if en not in cn:
        cn[en] = zh
        card_fixed.append((en, '(新增)', zh))
# 移除舊的顛倒鍵
for k in ['電音魔', '電音魔 ex']:
    if k in cn and cn[k].startswith('Toxtricity'):
        old = cn.pop(k)
        card_fixed.append((k, old, '(已移除倒置鍵)'))

# ---- 2. 修補 deck_names 中已存在的損壞譯名 ----
DECK_FIX = {
    'Mimikyu ex': '謎擬Qex',
    'Mimikyu ex Greninja': '謎擬Qex 甲賀忍蛙',
    'Lunala ex Mimikyu ex': '璐妮雅ex 謎擬Qex',
    'Giratina ex Mimikyu ex': '騎拉帝納ex 謎擬Qex',
    'Jumpluff ex Galarian Cursola': '口呆花ex 伽勒爾 魔靈珊瑚',
    'Armarouge ex Skeledirge': '紅蓮鎧騎ex 骨紋巨聲鱷',
    'Armarouge ex Indeedee ex': '紅蓮鎧騎ex 愛管侍ex',
    'Chandelure Persian': '水晶燈火靈 貓老大',
    'Crobat ex Nihilego': '叉字蝠ex 虛吾伊德',
    'Mega Lopunny ex Elekid': '超級長耳兔ex 電擊怪',
    'Buzzwole ex Pheromosa': '爆肌蚊ex 費洛美螂',
    'Buzzwole ex Celesteela': '爆肌蚊ex 鐵火輝夜',
    'Giratina ex Indeedee ex': '騎拉帝納ex 愛管侍ex',
    'Crobat ex Darkrai ex': '叉字蝠ex 達克萊伊ex',
    'Baxcalibur Palkia ex': '戟脊龍 帕路奇亞ex',
}
deck_fixed = []
for en, zh in DECK_FIX.items():
    if en in dn and dn[en] != zh:
        deck_fixed.append((en, dn[en], zh))
    dn[en] = zh

# ---- 3. 補齊今日新出現名稱：以 card_names 逐段精確比對，不做模糊切分 ----
def translate(name):
    """把 'Hoopa ex Mandibuzz' 這種以空白分隔的卡名組合翻成中文；必須全部命中。"""
    parts = name.split(' ')
    out = []
    i = 0
    while i < len(parts):
        hit = None
        for j in range(len(parts), i, -1):
            cand = ' '.join(parts[i:j])
            if cand in cn:
                hit = (cand, cn[cand])
                break
        if hit is None:
            return None
        out.append(hit[1])
        i += len(hit[0].split(' '))
    return ' '.join(out)


missing = set()
for f in ['memory/ptcgp_meta_20261127_std.json', 'memory/ptcgp_meta_20261127_std_comb.json']:
    for r in json.load(open(f, encoding='utf-8'))['rows']:
        n = r['name']
        if n not in dn and n not in cn:
            missing.add(n)

added = []
for n in sorted(missing):
    zh = translate(n)
    if zh is None:
        raise RuntimeError(f'cannot translate (no clean segmentation): {n}')
    dn[n] = zh
    added.append((n, zh))

# ---- 4. 一致性掃描：值中仍含非白名拉丁雜訊者列出（僅報告，不自動改） ----
LATIN_OK = {'ex', 'Ex', 'EX', 'V', 'VSTAR', 'X', 'Y', 'Q'}
residue = []
for k, v in dn.items():
    toks = [t for t in re.findall(r'[A-Za-z]+', v)]
    weird = [t for t in toks if t not in LATIN_OK]
    if weird:
        residue.append((k, v, weird))

D['metadata']['deck_names_count'] = len(dn)
D['metadata']['card_names_count'] = len(cn)
D['metadata']['version'] = '4.27'
D['metadata']['last_updated'] = '2026-11-27'
D['last_updated'] = '2026-11-27'
json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('card_fixed', len(card_fixed))
for a, b, c in card_fixed:
    print('  CARD', repr(a), repr(b), '->', repr(c))
print('deck_fixed', len(deck_fixed))
for a, b, c in deck_fixed:
    print('  DECK', repr(a), repr(b), '->', repr(c))
print('added', len(added), 'deck_names', len(dn), 'card_names', len(cn))
for a, b in added:
    print('  NEW', repr(a), '->', repr(b))
print('殘留拉丁雜訊條目:', len(residue))
for k, v, w in residue[:20]:
    print('  RESIDUE', repr(k), '->', repr(v), w)
