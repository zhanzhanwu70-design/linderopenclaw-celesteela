import json,collections,sys
rows=json.load(open('memory/ptcgp_meta_20261024.json'))
rows=[r for r in rows if r['share']>=0.20]
def grp(n):
    N=n.lower()
    if "team rocket" in N: return '火箭隊系'
    if "altaria" in N or "igglybuff" in N or "chingling" in N or "happiny" in N: return '七夕青鳥系'
    if any(k in N for k in ["magnezone","miraidon","dedenne","heliolisk","manectric","zeraora","rotom","jolteon","bellibolt","electrode","zapdos","meowstic","raikou","indeedee"]): return '電系'
    if any(k in N for k in ["suicune","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi","palafin","blissey"]): return '水系'
    if any(k in N for k in ["hoopa","absol","zoroark","greninja","darkrai","sableye","giratina","banette","weezing","nihilego","gengar","hydreigon","mismagius","hatterene","alcremie"]): return '暗/超能'
    if any(k in N for k in ["sceptile","buzzwole","pheromosa","venomoth","beautifly","dustox","beedrill","ledian","volcarona","exeggutor","venusaur","abomasnow","torterra","lilligant","serperior","celebi","lurantis","bonsly","cherubi","chikorita","treecko","scizor","revavroom"]): return '草/蟲系'
    if any(k in N for k in ["vespiquen","shuckle","heracross","arceus","registeel","metagross","perrserker","magneton","farfetch","starmie","tentacruel","armaldo","mawile","steelix","skarmory"]): return '鋼/蟲系'
    if any(k in N for k in ["dragonite","salamence","flygon","dragonair","garchomp","goomy","haxorus","goodra","drampa","latios","noivern","archaludon","duraludon","baxcalibur","tyranitar","bagon","shelgon"]): return '龍/地面'
    if any(k in N for k in ["lucario","blaziken","charizard","moltres","entei","typhlosion","incineroar","landorus","heatmor","skeledirge","hitmon","medicham","gallade","machamp","annihilape","primeape","infernape","hitmontop","aegislash","gholdengo","meloetta","tsareena","decidueye","meowscarada","chesnaught"]): return '格鬥/火系'
    if any(k in N for k in ["gardevoir","diancie","mimikyu","indeedee","eevee","togekiss","miltank","wigglytuff","leafeon","flareon","sylveon","audino","pichu","orchid","snorlax","tauros"]): return '超能/一般系'
    return '其他'
def build(rows,label):
    G=collections.defaultdict(lambda:[0.0,0,0,0])
    for r in rows:
        g=grp(r['name']); G[g][0]+=r['share']; G[g][1]+=r['w']; G[g][2]+=r['d']; G[g][3]+=r['l']
    out=[]
    for g,(s,w,d,l) in G.items():
        t=w+d+l; out.append({'group':g,'share':round(s,2),'awr':round((w+12)/(t+25)*100,2),'n':t})
    out.sort(key=lambda x:-x['awr'])
    print(f'=== {label} (branches={len(rows)}) ===')
    for x in out: print(f'{x["group"]:16} {x["share"]:>7.2f}% {x["awr"]:>7.2f}%  N={x["n"]}')
    return out
o=build(rows,'2026-10-24 top50+')
json.dump(o,open('memory/groups_20261024.json','w'),ensure_ascii=False,indent=1)
