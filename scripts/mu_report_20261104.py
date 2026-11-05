import json
D=json.load(open('ptcgp_deck_dictionary.json'))
dn=D['deck_names']; cn=D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n
M=json.load(open('memory/mu_matrix_20261104_c1.json'))
prev=json.load(open('memory/mu_matrix_20261103_c1.json'))
def show(key, minN=8, top=10):
    if key not in M: 
        print(f'!! {key} not found'); return
    d=M[key]
    print(f'=== {zh(key)} ({key}) ===')
    rows=[(o,w,m) for o,(w,m) in d.items() if m>=minN]
    rows.sort(key=lambda x:-x[1])
    for o,w,m in rows[:top]:
        p=prev.get(key,{}).get(o)
        ex=f' (昨 {p[0]:.1f}%/{p[1]})' if p else ''
        print(f'   vs {zh(o)[:30]:32} {w:>5.1f}%  N={m}{ex}')
for k in ['Mega Altaria ex','Hoopa ex','Suicune ex','Umbreon','Mega Greninja ex','Mega Manectric ex','Vespiquen ex','Hydreigon','Mega Charizard Y ex','Giratina ex']:
    show(k)
    print()
