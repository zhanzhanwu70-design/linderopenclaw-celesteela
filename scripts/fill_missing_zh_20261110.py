#!/usr/bin/env python3
"""2026-11-10 補齊 Limitless 新出現牌組名；以既有官方卡名字典分段翻譯 + 手動對照表。"""
import collections
import functools
import json

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P), object_pairs_hook=collections.OrderedDict)
cn = D['card_names']
dn = D['deck_names']

MANUAL = {
    'Hisuian Goodra Mantyke': '洗翠 黏美龍 小球飛魚',
    'Hoopa ex Decidueye ex': '胡帕ex 狙射樹梟ex',
    'Hoopa ex Umbreon ex': '胡帕ex 月亮伊布ex',
    'Koraidon ex Furfrou': '故勒頓ex 多麗米亞',
    # B3 #113 Single Strike Urshifu，官方繁中名「一擊流 熊拳士」
    'Lucario Single Strike Urshifu': '路卡利歐 一擊流 熊拳士',
    'Malamar Mega Absol ex': '烏賊王 超級阿勃梭魯ex',
    'Mega Altaria ex Oricorio': '超級七夕青鳥ex 花舞鳥',
    'Mega Charizard X ex Skeledirge': '超級噴火龍Xex 骨紋巨聲鱷',
    "Mega Gallade ex Team Rocket's Raticate ex": '超級艾路雷朵ex 火箭隊的拉達ex',
    'Mega Kangaskhan ex Greninja': '超級袋獸ex 甲賀忍蛙',
    'Mega Lucario ex Mega Blaziken ex': '超級路卡利歐ex 超級火焰雞ex',
    'Mega Mewtwo X ex Minior': '超級超夢Xex 小隕星',
    "Mega Pidgeot ex Team Rocket's Raticate ex": '超級大比鳥ex 火箭隊的拉達ex',
    'Mega Sceptile ex Furfrou': '超級蜥蜴王ex 多麗米亞',
    'Mega Tyranitar ex Minior': '超級班基拉斯ex 小隕星',
    'Mimikyu ex Gardevoir': '謎擬Ｑex 沙奈朵',
    "Team Rocket's Electrode Heliolisk": '火箭隊的頑皮彈 光電傘蜥',
    "Team Rocket's Weezing ex Alolan Muk": '火箭隊的雙彈瓦斯ex 阿羅拉 臭臭泥',
    'Team Rockets Electrode': '火箭隊的頑皮彈',
}

keys = sorted(cn, key=len, reverse=True)


@functools.lru_cache(maxsize=None)
def segment(s):
    if not s:
        return ((),)
    out = []
    for k in keys:
        if s.startswith(k + ' ') or s == k:
            for rest in segment(s[len(k):].lstrip()):
                out.append((k,) + rest)
    return tuple(out)


missing = set()
for f in ['memory/ptcgp_meta_20261110_std.json', 'memory/ptcgp_meta_20261110_std_comb.json']:
    for r in json.load(open(f))['rows']:
        n = r['name']
        if n not in dn and n not in cn:
            missing.add(n)

added = []
for n in sorted(missing):
    if n in MANUAL:
        zh = MANUAL[n]
    else:
        options = segment(n)
        if not options:
            raise RuntimeError(f'cannot translate: {n}')
        parts = min(options, key=lambda x: (len(x), sum(len(k) for k in x)))
        zh = ' '.join(cn[k] for k in parts)
    dn[n] = zh
    added.append((n, zh))

D['metadata']['deck_names_count'] = len(dn)
D['metadata']['version'] = '4.11'
D['metadata']['last_updated'] = '2026-11-10'
D['last_updated'] = '2026-11-10'
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)

print('added:', len(added))
for n, zh in added:
    print('  ', n, '=>', zh)
print('deck_names:', len(dn))
