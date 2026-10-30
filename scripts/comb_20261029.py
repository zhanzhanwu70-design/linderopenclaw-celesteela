import json
def agg(rs,f):
    sel=[r for r in rs if f(r['name'].lower())]
    sh=sum(r['share'] for r in sel); w=sum(r['w'] for r in sel); t=sum(r['w']+r['l']+r['d'] for r in sel)
    return round(sh,2),round((w+12)/(t+25)*100,2),t
L=[('電系雙雄(磁怪+好壞電龍)',lambda n:'magnezone' in n or 'dedenne' in n),
   ('電系全部',lambda n:any(k in n for k in ['magnezone','miraidon','dedenne','heliolisk','manectric','zeraora','rotom','indeedee','bellibolt','jolteon','electrode','zapdos','meowstic','raikou'])),
   ('七夕青鳥',lambda n:'altaria' in n),('路卡利歐',lambda n:'lucario' in n),
   ('胡帕',lambda n:'hoopa' in n),('蜂女王',lambda n:'vespiquen' in n),
   ('三頭龍',lambda n:'hydreigon' in n),('巨牙鯊',lambda n:'sharpedo' in n),
   ('火箭隊系',lambda n:'team rocket' in n),('拉達',lambda n:'raticate' in n),
   ('烈咬陸鯊',lambda n:'garchomp' in n),('沙奈朵',lambda n:'gardevoir' in n),
   ('火焰雞',lambda n:'blaziken' in n),('水君',lambda n:'suicune' in n),('哈克龍',lambda n:'dragonair' in n),
   ('哈克龍系(含rayquaza)',lambda n:'dragonair' in n or 'rayquaza' in n),
   ('雷電獸',lambda n:'manectric' in n),('Milotic',lambda n:'milotic' in n),
   ('自爆磁怪',lambda n:'magnezone' in n),('好壞電龍',lambda n:'dedenne' in n),
   ('噴火龍Y',lambda n:'charizard' in n),('蜥蜴王',lambda n:'sceptile' in n)]
for path,lab in [('memory/ptcgp_meta_20261028_comb.json','10-28'),('memory/ptcgp_meta_20261029_comb.json','10-29')]:
    rs=json.load(open(path)); print('===',lab,'comb',len(rs))
    for nm,f in L:
        s,a,t=agg(rs,f); print(f'   {nm:22} {s:>6.2f}% {a:>6.2f}% N={t}')
