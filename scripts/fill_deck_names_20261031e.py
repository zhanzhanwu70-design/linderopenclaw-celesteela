import json, re, sys

d = json.load(open('ptcgp_deck_dictionary.json'))
dn = d['deck_names']; cn = d['card_names']

E = json.load(open('memory/ptcgp_meta_20261031e_c1.json'))
EC = json.load(open('memory/ptcgp_meta_20261031e_c1_comb.json'))
allnames = sorted({r['name'] for r in E} | {r['name'] for r in EC})

# 可拆解的單卡名（用於 greedy 切分）
tokmap = {}
for k, v in cn.items():
    tokmap.setdefault(k, v)
for k, v in dn.items():
    tokmap.setdefault(k, v)

keys = sorted(tokmap.keys(), key=len, reverse=True)

def split(name):
    out = []
    i = 0
    rest = name
    while rest:
        for k in keys:
            if rest.startswith(k + ' ') or rest == k:
                out.append(k)
                rest = rest[len(k):].lstrip()
                break
        else:
            out.append(None)
            rest = rest.split(' ', 1)[1] if ' ' in rest else ''
    return out

missing = []
for n in allnames:
    if dn.get(n) or cn.get(n):
        continue
    parts = split(n)
    bad = [p for p in parts if p is None]
    if bad:
        missing.append((n, parts))
    else:
        zh = ' '.join(tokmap[p] for p in parts)
        dn[n] = zh

print('== 無法完整切分的（需人工）==')
for n, parts in missing:
    print(' -', n, '->', parts)

print()
print('== 已補翻譯 ==')
for n in allnames:
    if n in dn and dn[n] not in ('—', None):
        pass
json.dump(d, open('ptcgp_deck_dictionary.json', 'w'), ensure_ascii=False, indent=2)
print('done')
