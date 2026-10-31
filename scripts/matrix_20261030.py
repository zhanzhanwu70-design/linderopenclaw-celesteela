import json
M=json.load(open('memory/mu_matrix_20261030_c1.json'))
SUBJ={
 'Mega Greninja ex Greninja ex':'超級甲賀忍蛙(忍蛙)',
 'Mega Greninja ex Suicune ex':'超級甲賀忍蛙(水君)',
 'Greninja ex Mega Greninja ex':'忍蛙(反制甲賀忍蛙)',
 'Mega Charizard Y ex Entei ex':'噴火龍Y(炎帝)',
 'Pikachu ex Pawmot':'皮卡丘(帕)",
 'Mega Mewtwo X ex Mew ex':'超級超夢X(夢幻)',
 'Mega Altaria ex Espeon':'七夕青鳥',
 'Mega Lucario ex Lucario':'路卡利歐',
 'Mega Manectric ex Heliolisk':'雷電獸',
 'Miraidon ex Magnezone':'未來牌(磁怪)',
 'Magnezone Miraidon ex':'磁怪(未來牌)',
 'Giratina ex Dragonair':'騎拉帝納(哈克龍)',
 'Alolan Exeggutor ex Ribombee':'椰蛋樹(蜜蜂)',
 'Umbreon Hydreigon':'月亮伊布(三頭龍)',
 'Mega Dragonite ex Dragonite':'超級快龍',
 'Azumarill Lopunny':'阿羅拉椰蛋樹(長耳兔)',
 'Vespiquen ex Shuckle ex':'蜂女王',
 'Mega Blaziken ex':'火焰雞',
 'Hoopa ex Mega Absol ex':'胡帕',
}
def opp(n):
    for k,v in SUBJ.items():
        if k.lower()==n.lower(): return v
    return None
rows=[]
for s,d in M.items():
    if s not in SUBJ: continue
    r={'a':SUBJ[s]}
    for on,(w,m) in d.items():
        o=opp(on)
        if o and o!=r['a']: r[o]=(w,m)
    rows.append(r)
cols=[v for v in SUBJ.values()]
seen=set(); cols=[c for c in cols if not (c in seen or seen.add(c))]
print('| | '+' | '.join(cols)+' |')
print('|'+'---|'*(len(cols)+1))
for r in sorted(rows,key=lambda x:cols.index(x['a']) if x['a'] in cols else 99):
    cells=[]
    for c in cols:
        if c==r['a']: cells.append('—')
        elif c in r:
            w,m=r[c]; cells.append(f'{w:.0f}'+('*' if m<8 else ''))
        else: cells.append('·')
    print(f"| {r['a']} | "+' | '.join(cells)+' |')
print('\n* = N<8')
