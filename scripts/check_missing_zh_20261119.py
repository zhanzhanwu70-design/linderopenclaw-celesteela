#!/usr/bin/env python3
"""2026-11-19 檢查分支/合併口徑缺翻譯（deck_names 未命中即視為缺）。"""
import json

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']

def zh(n):
    if n in dn: return dn[n]
    if n in cn: return cn[n]
    return None

for tag, path in [
    ('合併', 'memory/ptcgp_meta_20261119_std_comb.json'),
    ('分支', 'memory/ptcgp_meta_20261119_std.json'),
]:
    rows = json.load(open(path))['rows']
    miss = [r for r in rows if zh(r['name']) is None]
    print(f'=== {tag} 共 {len(rows)} 列，缺翻譯 {len(miss)} ===')
    for r in miss:
        print(f"  {r['share']:>6.2f}%  {r['name']}")
    print()
