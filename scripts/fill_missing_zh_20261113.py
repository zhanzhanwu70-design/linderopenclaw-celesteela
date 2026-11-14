#!/usr/bin/env python3
"""2026-11-12 補齊 Limitless 新出現牌組名；以既有官方卡名字典分段翻譯。"""
import collections
import functools
import json

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P), object_pairs_hook=collections.OrderedDict)
cn = D['card_names']
dn = D['deck_names']

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
for f in ['memory/ptcgp_meta_20261113_std.json', 'memory/ptcgp_meta_20261113_std_comb.json']:
    for r in json.load(open(f))['rows']:
        n = r['name']
        if n not in dn and n not in cn:
            missing.add(n)

added = []
for n in sorted(missing):
    options = segment(n)
    if not options:
        raise RuntimeError(f'cannot translate: {n}')
    parts = min(options, key=lambda x: (len(x), sum(len(k) for k in x)))
    zh = ' '.join(cn[k] for k in parts)
    dn[n] = zh
    added.append((n, zh))

D['metadata']['deck_names_count'] = len(dn)
D['metadata']['version'] = '4.13'
D['metadata']['last_updated'] = '2026-11-13'
D['last_updated'] = '2026-11-13'
json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)

print('added:', len(added))
for n, zh in added:
    print('  ', n, '=>', zh)
print('deck_names:', len(dn))
