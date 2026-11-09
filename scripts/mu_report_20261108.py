import json
D=json.load(open('ptcgp_deck_dictionary.json'))
dn=D['deck_names']; cn=D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n
M=json.load(open('memory/mu_matrix_20261108_c1.json'))
FOCUS=['Vespiquen ex Shuckle ex','Mega Altaria ex Espeon','Magnezone Miraidon ex','Hoopa ex Mega Absol ex',
 'Hydreigon Mega Absol ex','Suicune ex Baxcalibur','Mega Charizard Y ex Entei ex','Mega Greninja ex Greninja ex',
 'Mega Manectric ex Heliolisk','Umbreon Hydreigon','Giratina ex Dragonair','Mega Lucario ex Lucario',
 'Mega Sceptile ex Greninja','Mega Mewtwo X ex Mew ex','Alolan Exeggutor ex Ribombee','Mega Greninja ex Suicune ex']
for f in FOCUS:
    if f not in M:
        print('== MISSING', f); continue
    print('==', zh(f))
    d=M[f]
    for o,(w,n) in sorted(d.items(), key=lambda x:-x[1][1])[:10]:
        print(f'   {zh(o)[:26]:28} {w:>5.1f}%  N={n}')
    print()
