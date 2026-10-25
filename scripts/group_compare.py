import json,collections
def grp(n):
    N=n.lower()
    if "team rocket" in N: return '火箭隊系'
    if "altaria" in N or "igglybuff" in N or "chingling" in N or "happiny" in N: return '七夕青鳥系'
    if any(k in N for k in ["magnezone","miraidon","manectric","heliolisk","rotom","zeraora","bellibolt"]): return '電系(純)'
    if any(k in N for k in ["dedenne","indeedee"]): return '好壞電龍/愛管仕'
    if any(k in N for k in ["suicune","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi"]): return '水系'
    if any(k in N for k in ["hoopa","absol","zoroark","greninja","darkrai","sableye","giratina","banette","weezing","nihilego","gengar","hydreigon","mismagius","hatterene"]): return '暗/超能'
    if any(k in N for k in ["sceptile","beautifly","dustox","venusaur","buzzwole","pheromosa","scizor","revavroom","exeggutor","volcarona","abomasnow","torterra"]): return '草/蟲系'
    if any(k in N for k in ["vespiquen","shuckle","heracross"]): return '蜂女王系'
    if any(k in N for k in ["dragonair","dragonite","flygon","garchomp","salamence","baxcalibur","tyranitar"]): return '龍/地面'
    if any(k in N for k in ["lucario","blaziken","charizard","moltres","entei","typhlosion","incineroar","heatmor","skeledirge","hitmon","medicham","gallade","machamp","annihilape","aegislash","gholdengo","meloetta","meowscarada","chesnaught"]): return '格鬥/火系'
    if any(k in N for k in ["gardevoir","diancie","mimikyu","eevee","togekiss","snorlax","tauros","leafeon","flareon","sylveon","audino","pichu"]): return '超能/一般系'
    return '其他'
def agg(rows,f):
    sel=[r for r in rows if f(r['name'].lower())]
    sh=sum(r['share'] for r in sel); w=sum(r['w'] for r in sel); t=sum(r['w']+r['l']+r.get('t',r.get('d',0)) for r in sel)
    return round(sh,2),round((w+12)/(t+25)*100,2),t
def load(p,n=50):
    rs=json.load(open(p)); rs.sort(key=lambda x:-x['share']); return rs[:n]
groups={
 '電系(純)':lambda n: any(k in n for k in ['magnezone','miraidon','manectric','heliolisk','rotom','zeraora','bellibolt']),
 '好壞電龍/愛管仕':lambda n: any(k in n for k in ['dedenne','indeedee']),
 '水系':lambda n: any(k in n for k in ['suicune','milotic','gyarados','sharpedo','vaporeon','wailord','swanna','pyukumuku','wishiwashi']),
 '七夕青鳥系':lambda n: 'altaria' in n or 'igglybuff' in n or 'chingling' in n,
 '暗/超能':lambda n: any(k in n for k in ['hoopa','absol','zoroark','greninja','darkrai','sableye','giratina','banette','weezing','nihilego','gengar','hydreigon','mismagius','hatterene']),
 '草/蟲系':lambda n: any(k in n for k in ['sceptile','beautifly','dustox','venusaur','buzzwole','pheromosa','scizor','revavroom','exeggutor','volcarona']),
 '蜂女王系':lambda n: any(k in n for k in ['vespiquen','shuckle','heracross']),
 '龍/地面':lambda n: any(k in n for k in ['dragonair','dragonite','flygon','garchomp','salamence','baxcalibur','tyranitar']),
 '格鬥/火系':lambda n: any(k in n for k in ['lucario','blaziken','charizard','moltres','entei','typhlosion','incineroar','heatmor','skeledirge','hitmon','medicham','gallade','machamp','annihilape','aegislash','gholdengo','meloetta','meowscarada','chesnaught']),
 '超能/一般系':lambda n: any(k in n for k in ['gardevoir','diancie','mimikyu','eevee','togekiss','snorlax','tauros','leafeon','flareon','sylveon','audino','pichu']),
 '火箭隊系':lambda n: 'team rocket' in n,
}
Y=load('memory/ptcgp_meta_20261023.json'); T=load('memory/ptcgp_meta_20261024.json')
print(f'{"群組":18}{"昨日份額":>10}{"今日份額":>10}{"Δ":>7}  {"昨日AWR":>8}{"今日AWR":>9}{"Δ":>7}  {"N":>7}')
res=[]
for g,f in groups.items():
    ys,ya,yn=agg(Y,f); ts,ta,tn=agg(T,f)
    res.append((g,ys,ts,ya,ta,tn))
    print(f'{g:18}{ys:>9.2f}%{ts:>9.2f}%{ts-ys:>+7.2f}  {ya:>7.2f}%{ta:>8.2f}%{ta-ya:>+7.2f}  {tn:>7}')
json.dump(res,open('memory/group_compare_20261024.json','w'),ensure_ascii=False,indent=1)
