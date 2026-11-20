#!/usr/bin/env python3
"""N 佔全環境比重（合併口徑）11-16～11-19 趨勢。"""
import collections, json

def agg(rows):
    out = collections.defaultdict(lambda: {'share':0.0,'w':0,'l':0,'d':0,'n':0,'decks':0})
    for r in rows:
        a = out[r['name']]
        for k in ('share','w','l','d','n','decks'):
            a[k] += r[k]
    res=[]
    for name,a in out.items():
        a=dict(a); a['name']=name
        a['awr']=(a['w']+12)/(a['n']+25)*100 if a['n'] else 0.0
        res.append(a)
    res.sort(key=lambda r:-r['share'])
    return res

def load(day):
    suf = '.json' if day=='20261119' else '_re.json'
    d=json.load(open(f'memory/ptcgp_meta_{day}_std_comb{suf}',encoding='utf-8'))
    return d['header'], agg(d['rows'])

days=['20261116','20261117','20261118','20261119']
data={}
for d in days:
    h,rows=load(d)
    tot=sum(r['n'] for r in rows)
    data[d]=(h,rows,{r['name']:r['n']/tot*100 for r in rows},tot)
    print(d,h,'N=',tot,'AWR=%.4f'%((sum(r['w'] for r in rows)+12)/(tot+25)*100))

names=['Mega Altaria ex','Hoopa ex','Magnezone','Mega Greninja ex','Umbreon','Mega Charizard Y ex',
 'Suicune ex','Vespiquen ex','Mega Lucario ex','Giratina ex','Mega Mewtwo X ex','Mega Manectric ex',
 'Chien Pao ex','Mega Sceptile ex','Mega Skarmory ex','Hydreigon','Greninja','Greninja ex','Arceus ex',
 'Mega Dragonite ex','Absol ex','Pidgeot ex','Alolan Exeggutor ex','Dragonair','Mega Bouffalant ex',
 'Lopunny','Pikachu ex','Miraidon ex','Rampardos ex','Zapdos ex','Eevee','Ancient Mew ex','Lugia ex',
 'Latias ex','Dialga ex','Sylveon','Weezing','Klefki','Mew ex','Snorlax','Alolan Ninetales ex']
print()
for n in names:
    line=[]
    for d in days:
        rows=data[d][1]
        r=next((x for x in rows if x['name']==n), None)
        ns=data[d][2].get(n)
        line.append(f"{r['share']:7.4f}%/{r['awr']:8.4f}%/N{r['n']:5}/{ns:6.3f}%" if r else ' -- ')
    print(f"{n[:28]:30} " + ' | '.join(line))
