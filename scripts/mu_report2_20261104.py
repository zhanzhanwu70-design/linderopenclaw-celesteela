import json
D=json.load(open('ptcgp_deck_dictionary.json'))
dn=D['deck_names']; cn=D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n
M=json.load(open('memory/mu_matrix_20261104_c1.json'))
prev=json.load(open('memory/mu_matrix_20261103_c1.json'))
def show(key, minN=6, top=8):
    if key not in M:
        print(f'!! {key}'); return
    d=M[key]
    print(f'=== {zh(key) or key} ===')
    rows=[(o,w,m) for o,(w,m) in d.items() if m>=minN]
    rows.sort(key=lambda x:-x[1])
    for o,w,m in rows[:top]:
        p=prev.get(key,{}).get(o)
        ex=f'  (昨 {p[0]:.1f}%/N={p[1]})' if p else ''
        print(f'   vs {(zh(o) or o)[:28]:30} {w:>5.1f}%  N={m}{ex}')
for k in ['Mega Altaria ex Greninja','Umbreon Hydreigon','Suicune ex Baxcalibur','Hoopa ex Mega Absol ex','Mega Greninja ex Greninja ex','Mega Greninja ex Suicune ex','Mega Manectric ex Heliolisk','Vespiquen ex Shuckle ex','Hydreigon Mega Absol ex','Mega Charizard Y ex Entei ex','Giratina ex Dragonair','Mega Mewtwo X ex Mew ex','Pikachu ex Pawmot','Raikou ex Pawmot','Mega Lucario ex Lucario','Magnezone Miraidon ex']:
    show(k); print()
