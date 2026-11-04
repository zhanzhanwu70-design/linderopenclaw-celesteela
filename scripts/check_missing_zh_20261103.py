import json, re

d = json.load(open('ptcgp_deck_dictionary.json'))
dn = d.get('deck_names', {})

for f in ['memory/ptcgp_meta_20261103_std.json', 'memory/ptcgp_meta_20261103_std_comb.json']:
    rows = json.load(open(f))['rows']
    miss = []
    for r in rows:
        n = r['name']
        if n not in dn and n.lower() not in {k.lower() for k in dn}:
            miss.append((n, r['share'], r['awr'], r['n']))
    print(f, 'rows=', len(rows), 'missing=', len(miss))
    for m in sorted(miss, key=lambda z: -z[1]):
        print('   MISSING:', m)
