import json
def load(p,n=50):
    rs=json.load(open(p)); rs.sort(key=lambda x:-x['share']); return rs[:n]
Y=load('memory/ptcgp_meta_20261028.json'); T=load('memory/ptcgp_meta_20261029.json')
def agg(rs,f):
    sel=[r for r in rs if f(r['name'].lower())]
    sh=sum(r['share'] for r in sel); w=sum(r['w'] for r in sel); t=sum(r['w']+r['l']+r['d'] for r in sel)
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
print(f'{"群組":18}{"昨日份額":>10}{"今日份額":>10}{"Δ":>8}{"昨日AWR":>10}{"今日AWR":>10}{"Δ":>8}{"N":>8}')
res=[]
for lab,f in G:
    ys,ya,yn=agg(Y,f); ts,ta,tn=agg(T,f)
    res.append({'group':lab,'y_share':ys,'t_share':ts,'d_share':round(ts-ys,2),'y_awr':ya,'t_awr':ta,'d_awr':round(ta-ya,2),'n':tn})
    print(f'{lab:18}{ys:>9.2f}%{ts:>9.2f}%{ts-ys:>+8.2f}{ya:>9.2f}%{ta:>9.2f}%{ta-ya:>+8.2f}{tn:>8}')
json.dump(res,open('memory/group_table_20261029.json','w'),ensure_ascii=False,indent=1)

print('\n=== 單體 Top25 昨日 vs 今日 ===')
ym={r['name']:r for r in Y}; tm={r['name']:r for r in T}
for r in T[:25]:
    o=ym.get(r['name'])
    if o: print(f"{r['name'][:38]:40} share {o['share']:>5.2f}->{r['share']:>5.2f}  awr {o['awr']:>5.2f}->{r['awr']:>5.2f}")
    else: print(f"{r['name'][:38]:40} share NEW {r['share']:>5.2f} awr {r['awr']:>5.2f}")
print('\n--- 掉出前50 ---')
for r in Y:
    if r['name'] not in {x['name'] for x in T[:50]}:
        print(f"{r['name'][:45]:47} share {r['share']:>5.2f} awr {r['awr']:>5.2f}")
