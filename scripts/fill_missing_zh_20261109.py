#!/usr/bin/env python3
"""2026-11-09 補齊 Limitless 新出現牌組名；以既有官方卡名字典分段翻譯。"""
import collections
import functools
import json

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P), object_pairs_hook=collections.OrderedDict)
cn = D['card_names']
dn = D['deck_names']

# 字典中只有基底卡名時，依同一官方命名規則補足；既有牌組翻譯亦可交叉驗證。
MANUAL = {
    'Mega Houndoom ex': '超級黑魯加ex',
    'Mega Medicham ex': '超級恰雷姆ex',
    'Inteleon': '狙射樹梟',
    'Inteleon Pyukumuku': '狙射樹梟 拳海參',
    'Mega Medicham ex Mega Mewtwo X ex': '超級恰雷姆ex 超級超夢Xex',
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
for f in ['memory/ptcgp_meta_20261109_std.json', 'memory/ptcgp_meta_20261109_std_comb.json']:
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
        # 優先選用最多卡名、能完整覆蓋原名且最短的一段。
        parts = min(options, key=lambda x: (len(x), sum(len(k) for k in x)))
        zh = ' '.join(cn[k] for k in parts)
    dn[n] = zh
    added.append((n, zh))

D['metadata']['deck_names_count'] = len(dn)
D['metadata']['version'] = '4.10'
D['metadata']['last_updated'] = '2026-11-09'
D['last_updated'] = '2026-11-09'
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)

print('added:', len(added))
for n, zh in added:
    print('  ', n, '=>', zh)
print('deck_names:', len(dn))
