import json
def load(p,n=50):
    rs=json.load(open(p)); rs.sort(key=lambda x:-x['share']); return rs[:n]
Y=load('memory/ptcgp_meta_20261023.json'); T=load('memory/ptcgp_meta_20261024.json')
def agg(rs,f):
    sel=[r for r in rs if f(r['name'].lower())]
    sh=sum(r['share'] for r in sel); w=sum(r['w'] for r in sel); t=sum(r['w']+r['l']+r.get('t',r.get('d',0)) for r in sel)
    return round(sh,2),round((w+12)/(t+25)*100,2),t
G=[
 ('七夕青鳥系', lambda n:'altaria' in n or 'igglybuff' in n or 'chingling' in n),
 ('電系(含好壞電龍)', lambda n: any(k in n for k in ['magnezone','miraidon','manectric','heliolisk','rotom','zeraora','bellibolt','dedenne','indeedee'])),
 ('水系', lambda n: any(k in n for k in ['suicune','milotic','gyarados','sharpedo','vaporeon'])),
 ('暗/超能', lambda n: any(k in n for k in ['hoopa','absol','zoroark','greninja','darkrai','sableye','giratina','banette','weezing','nihilego','gengar','hydreigon','mismagius','hatterene'])),
 ('草/蟲系', lambda n: any(k in n for k in ['sceptile','beautifly','dustox','venusaur','buzzwole','pheromosa','scizor','revavroom','exeggutor','volcarona'])),
 ('路卡利歐系', lambda n:'lucario' in n),
 ('龍/地面', lambda n: any(k in n for k in ['dragonair','dragonite','flygon','garchomp','salamence','baxcalibur','tyranitar'])),
 ('火焰雞系', lambda n:'blaziken' in n),
 ('蜂女王系', lambda n:'vespiquen' in n),
 ('火箭隊系', lambda n:'team rocket' in n),
]
print(f'{"群組":16}{"昨日份額":>10}{"今日份額":>10}{"Δ":>7}{"昨日AWR":>10}{"今日AWR":>10}{"Δ":>7}{"N":>7}')
res=[]
for lab,f in G:
    ys,ya,yn=agg(Y,f); ts,ta,tn=agg(T,f)
    res.append((lab,ys,ts,ya,ta,tn))
    print(f'{lab:16}{ys:>9.2f}%{ts:>9.2f}%{ts-ys:>+7.2f}{ya:>9.2f}%{ta:>9.2f}%{ta-ya:>+7.2f}{tn:>7}')
json.dump(res,open('memory/group_table_20261024.json','w'),ensure_ascii=False,indent=1)
