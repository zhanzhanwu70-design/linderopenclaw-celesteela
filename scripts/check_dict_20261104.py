import json
D=json.load(open('ptcgp_deck_dictionary.json'))
dn=D['deck_names']; cn=D['card_names']
rows_b=json.load(open('memory/ptcgp_meta_20261104_std.json'))['rows']
rows_c=json.load(open('memory/ptcgp_meta_20261104_std_comb.json'))['rows']
miss_b=[r['name'] for r in rows_b if r['name'] not in dn and r['name'] not in cn]
miss_c=[r['name'] for r in rows_c if r['name'] not in dn and r['name'] not in cn]
print('branch rows', len(rows_b), 'missing', len(set(miss_b)))
for n in sorted(set(miss_b)): print('  B:', n)
print('comb rows', len(rows_c), 'missing', len(set(miss_c)))
for n in sorted(set(miss_c)): print('  C:', n)
print('dict version', D.get('metadata'))
print('deck_names', len(dn), 'card_names', len(cn))
