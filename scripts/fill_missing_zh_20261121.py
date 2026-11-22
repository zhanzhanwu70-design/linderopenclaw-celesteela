#!/usr/bin/env python3
"""2026-11-20 補齊 Limitless 新出現牌組名；以既有官方卡名字典分段翻譯。
新增卡名 'Mega Mewtwo Y ex'（Promo-C #2）依既有官方名 'Mega Mewtwo X ex' 之同構規則補為「超級超夢Yex」。"""
import collections
import functools
import json

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
cn = D['card_names']
dn = D['deck_names']

# 手動別名：Limitless 合併頁會把 "Team Rocket's Articuno ex" 寫成無撇號的 "Team Rockets Articuno ex"，
# 沿用既有官方卡名 "Team Rocket’s Articuno ex" => 火箭隊的 急凍鳥ex 的同構寫法。
ALIAS = {
    'Team Rockets Articuno ex': '火箭隊的 急凍鳥ex',
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
for f in ['memory/ptcgp_meta_20261121_std.json', 'memory/ptcgp_meta_20261121_std_comb.json']:
    for r in json.load(open(f, encoding='utf-8'))['rows']:
        n = r['name']
        if n not in dn and n not in cn:
            missing.add(n)

added = []
for n in sorted(missing):
    if n in ALIAS:
        dn[n] = ALIAS[n]
        added.append((n, ALIAS[n]))
        continue
    options = segment(n)
    if not options:
        raise RuntimeError(f'cannot translate: {n}')
    parts = min(options, key=lambda x: (len(x), sum(len(k) for k in x)))
    zh = ' '.join(cn[k] for k in parts)
    dn[n] = zh
    added.append((n, zh))

D['metadata']['deck_names_count'] = len(dn)
D['metadata']['card_names_count'] = len(cn)
D['metadata']['version'] = '4.21'
D['metadata']['last_updated'] = '2026-11-20'
D['last_updated'] = '2026-11-20'
json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('added:', len(added))
for n, zh in added:
    print('  ', n, '=>', zh)
print('deck_names:', len(dn), 'card_names:', len(cn))
