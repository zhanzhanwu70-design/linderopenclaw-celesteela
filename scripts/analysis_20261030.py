import json,collections
def grp(n):
    N=n.lower()
    if "team rocket" in N: return '火箭隊系'
    if any(k in N for k in ["altaria","igglybuff","chingling","happiny"]): return '七夕青鳥系'
    if any(k in N for k in ["magnezone","miraidon","dedenne","heliolisk","manectric","zeraora","rotom","jolteon","bellibolt","electrode","zapdos","meowstic","raikou","indeedee","pikachu"]): return '電系'
    if any(k in N for k in ["suicune","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi","palafin","blissey","chien-pao","greninja"]): return '水系'
    if any(k in N for k in ["hoopa","absol","zoroark","darkrai","sableye","giratina","banette","weezing","nihilego","gengar","hydreigon","mismagius","hatterene","alcremie","slowking","tyranitar"]): return '暗/超能'
    if any(k in N for k in ["sceptile","buzzwole","pheromosa","venomoth","beautifly","dustox","beedrill","ledian","volcarona","exeggutor","venusaur","abomasnow","torterra","lilligant","serperior","celebi","lurantis","bonsly","cherubi","chikorita","treecko","scizor","revavroom","exeggutor"]): return '草/蟲系'
    if any(k in N for k in ["vespiquen","shuckle","heracross","arceus","registeel","metagross","perrserker","magneton","farfetch","starmie","tentacruel","armaldo","mawile","steelix","skarmory","lycanroc"]): return '鋼/蟲/格鬥'
    if any(k in N for k in ["dragonite","salamence","flygon","dragonair","garchomp","goomy","haxorus","goodra","drampa","latios","noivern","archaludon","duraludon","baxcalibur","tyranitar","bagon","shelgon","rayquaza","dragonite"]): return '龍/地面'
    if any(k in N for k in ["lucario","blaziken","charizard","moltres","entei","typhlosion","incineroar","landorus","heatmor","skeledirge","hitmon","medicham","gallade","machamp","annihilape","primeape","infernape","hitmontop","aegislash","gholdengo","meloetta","tsareena","decidueye","meowscarada","chesnaught","mewtwo"]): return '格鬥/火系'
    if any(k in N for k in ["gardevoir","diancie","mimikyu","indeedee","eevee","togekiss","miltank","wigglytuff","leafeon","flareon","sylveon","audino","pichu","orchid","snorlax","tauros","carbink"]): return '超能/一般系'
    return '其他'
def build(rows,label,minq=0.20):
    rr=[r for r in rows if r['share']>=minq]
    G=collections.defaultdict(lambda:[0.0,0,0])
    for r in rr:
        g=grp(r['name']); G[g][0]+=r['share']; G[g][1]+=r['w']; G[g][2]+=r['n']
    out=[]
    for g,(s,w,t) in G.items():
        out.append({'group':g,'share':round(s,2),'awr':round((w+12)/(t+25)*100,2),'n':t})
    out.sort(key=lambda x:-x['share'])
    print(f'=== {label} (rows={len(rr)}) ===')
    for x in out: print(f"{x['group']:14} {x['share']:>7.2f}% {x['awr']:>7.2f}%  N={x['n']}")
    return out
Y=json.load(open('memory/ptcgp_meta_20261029.json'))
T=json.load(open('memory/ptcgp_meta_20261030_b4a.json'))
build(Y,'B4a branch 10-29')
build(T,'B4a branch 10-30')
YC=json.load(open('memory/ptcgp_meta_20261029_comb.json'))
TC=json.load(open('memory/ptcgp_meta_20261030_b4a_comb.json'))
build(YC,'B4a comb 10-29')
build(TC,'B4a comb 10-30')
C1=json.load(open('memory/ptcgp_meta_20261030_c1.json'))
print('\n=== C1 branch top 40 ===')
for r in C1[:40]: print(f"{r['name'][:52]:54} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']}")
