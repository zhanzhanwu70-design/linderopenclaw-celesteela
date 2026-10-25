import json
def load(p,n=50):
    rs=json.load(open(p)); rs.sort(key=lambda x:-x['share']); return rs[:n]
Y=load('memory/ptcgp_meta_20261023.json'); T=load('memory/ptcgp_meta_20261024.json')
def agg(rs,f):
    sel=[r for r in rs if f(r['name'].lower())]
    sh=sum(r['share'] for r in sel); w=sum(r['w'] for r in sel)
    t=sum(r['w']+r['l']+r.get('t',r.get('d',0)) for r in sel)
    return round(sh,2),round((w+12)/(t+25)*100,2),t,len(sel)
ELEC=lambda n: any(k in n for k in ['magnezone','miraidon','manectric','heliolisk','rotom','zeraora','bellibolt','dedenne','indeedee'])
EPURE=lambda n: any(k in n for k in ['magnezone','miraidon','manectric','heliolisk','rotom','zeraora','bellibolt'])
print('電系合計(分支口徑, 含好壞電龍) Y:',agg(Y,ELEC),' T:',agg(T,ELEC))
print('電系純 Y:',agg(Y,EPURE),' T:',agg(T,EPURE))
print('路卡利歐 Y:',agg(Y,lambda n:'lucario' in n),' T:',agg(T,lambda n:'lucario' in n))
print('火箭隊 Y:',agg(Y,lambda n:'team rocket' in n),' T:',agg(T,lambda n:'team rocket' in n))
print('七夕青鳥 Y:',agg(Y,lambda n:'altaria' in n or 'igglybuff' in n or 'chingling' in n),' T:',agg(T,lambda n:'altaria' in n or 'igglybuff' in n or 'chingling' in n))
print('胡帕 Y:',agg(Y,lambda n:'hoopa' in n),' T:',agg(T,lambda n:'hoopa' in n))
print('蜂女王 Y:',agg(Y,lambda n:'vespiquen' in n),' T:',agg(T,lambda n:'vespiquen' in n))
print('火焰雞 Y:',agg(Y,lambda n:'blaziken' in n),' T:',agg(T,lambda n:'blaziken' in n))
print('水系 Y:',agg(Y,lambda n:any(k in n for k in ['suicune','milotic','gyarados','sharpedo','vaporeon'])),' T:',agg(T,lambda n:any(k in n for k in ['suicune','milotic','gyarados','sharpedo','vaporeon'])))
print('巨牙鯊 Y:',agg(Y,lambda n:'sharpedo' in n),' T:',agg(T,lambda n:'sharpedo' in n))
print('沙奈朵 Y:',agg(Y,lambda n:'gardevoir' in n),' T:',agg(T,lambda n:'gardevoir' in n))
print('蜥蜴王 Y:',agg(Y,lambda n:'sceptile' in n),' T:',agg(T,lambda n:'sceptile' in n))
print('哈克龍 Y:',agg(Y,lambda n:'dragonair' in n),' T:',agg(T,lambda n:'dragonair' in n))
print()
print('=== 合併口徑 combine=1 ===')
C=json.load(open('memory/ptcgp_meta_20261024_comb.json'))
for f,lab in [(lambda n:any(k in n for k in ['magnezone','miraidon','manectric','dedenne','indeedee']),'電系含好壞電龍'),(lambda n:any(k in n for k in ['magnezone','miraidon','manectric']),'電系(磁怪/密勒頓/雷電獸)'),(lambda n:'altaria' in n,'七夕青鳥'),(lambda n:'lucario' in n,'路卡利歐'),(lambda n:'team rocket' in n,'火箭隊'),(lambda n:'raticate' in n,'拉達'),(lambda n:'vespiquen' in n,'蜂女王'),(lambda n:'hoopa' in n,'胡帕'),(lambda n:'blaziken' in n,'火焰雞'),(lambda n:any(k in n for k in ['suicune','milotic','sharpedo']),'水系')]:
    print(f'{lab:18}',agg(C,f))
