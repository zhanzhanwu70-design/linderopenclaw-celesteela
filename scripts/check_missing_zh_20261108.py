import json
D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']
rows = json.load(open('memory/ptcgp_meta_20261108_std_comb.json'))['rows']
miss = []
for r in rows:
    n = r['name']
    if n not in dn and n not in cn:
        miss.append((n, r['share'], r['awr'], r['n'], r['slug']))
miss.sort(key=lambda x: -x[1])
print('缺翻譯數:', len(miss))
for m in miss:
    print(f'  {m[0][:60]:62} {m[1]:>6.2f}% {m[2]:>6.2f}% N={m[3]}  slug={m[4]}')
print()
print('dict version:', D.get('version'), 'deck_names:', len(dn), 'card_names:', len(cn))
