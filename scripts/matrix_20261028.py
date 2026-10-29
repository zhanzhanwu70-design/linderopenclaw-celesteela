import json
SUBJ={
 'Mega Altaria ex Espeon':'七夕青鳥',
 'Mega Lucario ex Lucario':'路卡利歐',
 'Butterfree Mega Sceptile ex':'蜥蜴王',
 'Suicune ex Baxcalibur':'水君',
 'Vespiquen ex Shuckle ex':'蜂女王',
 'Dragonair Mega Rayquaza ex':'哈克龍',
 'Magnezone Miraidon ex':'自爆磁怪',
 'Hoopa ex Mega Absol ex':'胡帕',
 'Hydreigon Mega Absol ex':'三頭龍',
 'Mega Blaziken ex':'火焰雞',
 'Dedenne ex Indeedee ex':'好壞電龍',
 'Mega Charizard Y ex Entei ex':'噴火龍Y',
 'Mega Sharpedo ex Gyarados':'巨牙鯊',
 'Mega Manectric ex Heliolisk':'雷電獸',
 'Milotic ex Eevee ex':'Milotic',
 'Mega Gardevoir ex Mega Diancie ex':'沙奈朵',
}
def opp(n):
    for k,v in SUBJ.items():
        if k.lower()==n.lower(): return v
    return None
T=json.load(open('memory/mu_matrix_20261028.json'))
Y=json.load(open('memory/mu_matrix_20261026.json'))
rows=[]
for s,d in T.items():
    if s not in SUBJ: continue
    a=SUBJ[s]
    r={'a':a}
    for on,(w,m) in d.items():
        o=opp(on)
        if o: r[o]=(w,m)
    rows.append(r)
order=['七夕青鳥','路卡利歐','蜥蜴王','水君','蜂女王','哈克龍','自爆磁怪','胡帕','三頭龍','火焰雞','好壞電龍','噴火龍Y']
cols=order
print('| | '+' | '.join(cols)+' |')
print('|'+'---|'*(len(cols)+1))
for r in sorted(rows,key=lambda x:order.index(x['a']) if x['a'] in order else 99):
    cells=[]
    for c in cols:
        if c==r['a']: cells.append('—')
        elif c in r: 
            w,m=r[c]; cells.append(f'{w:.1f}' + ('' if m>=25 else '*'))
        else: cells.append('·')
    print(f"| {r['a']} | "+' | '.join(cells)+' |')
print('\n* = N<25')
# deltas vs yesterday
print('\n=== Δ vs 10-26 (|Δ|>=0.5pt, N>=25 both) ===')
Ym={}
for s,d in Y.items():
    if s in SUBJ: Ym[SUBJ[s]]={opp(on):(w,m) for on,(w,m) in d.items() if opp(on)}
for r in rows:
    for c in cols:
        if c==r['a'] or c not in r: continue
        if c in Ym.get(r['a'],{}):
            yw,ym=Ym[r['a']][c]; tw,tm=r[c]
            if ym>=25 and tm>=25 and abs(tw-yw)>=0.5:
                print(f'{r["a"]:8} vs {c:8} {yw:>5.1f} -> {tw:>5.1f}  (N {ym}->{tm})')
