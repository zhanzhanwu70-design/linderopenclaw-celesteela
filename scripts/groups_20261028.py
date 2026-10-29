import json,collections
def grp(n):
    N=n.lower()
    if "team rocket" in N: return '火箭隊系'
    if any(k in N for k in ["altaria","igglybuff","chingling","happiny"]): return '七夕青鳥系'
    if any(k in N for k in ["magnezone","miraidon","dedenne","heliolisk","manectric","zeraora","rotom","jolteon","bellibolt","electrode","zapdos","meowstic","raikou","indeedee"]): return '電系'
    if any(k in N for k in ["suicune","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi","palafin","blissey","chien-pao"]): return '水系'
    if any(k in N for k in ["hoopa","absol","zoroark","greninja","darkrai","sableye","giratina","banette","weezing","nihilego","gengar","hydreigon","mismagius","hatterene","alcremie","slowking"]): return '暗/超能'
    if any(k in N for k in ["sceptile","buzzwole","pheromosa","venomoth","beautifly","dustox","beedrill","ledian","volcarona","exeggutor","venusaur","abomasnow","torterra","lilligant","serperior","celebi","lurantis","bonsly","cherubi","chikorita","treecko","scizor","revavroom"]): return '草/蟲系'
    if any(k in N for k in ["vespiquen","shuckle","heracross","arceus","registeel","metagross","perrserker","magneton","farfetch","starmie","tentacruel","armaldo","mawile","steelix","skarmory"]): return '鋼/蟲系'
    if any(k in N for k in ["dragonite","salamence","flygon","dragonair","garchomp","goomy","haxorus","goodra","drampa","latios","noivern","archaludon","duraludon","baxcalibur","tyranitar","bagon","shelgon","rayquaza"]): return '龍/地面'
    if any(k in N for k in ["lucario","blaziken","charizard","moltres","entei","typhlosion","incineroar","landorus","heatmor","skeledirge","hitmon","medicham","gallade","machamp","annihilape","primeape","infernape","hitmontop","aegislash","gholdengo","meloetta","tsareena","decidueye","meowscarada","chesnaught"]): return '格鬥/火系'
    if any(k in N for k in ["gardevoir","diancie","mimikyu","indeedee","eevee","togekiss","miltank","wigglytuff","leafeon","flareon","sylveon","audino","pichu","orchid","snorlax","tauros","carbink"]): return '超能/一般系'
    return '其他'
def build(path,label,minq=0.20):
    rows=[r for r in json.load(open(path)) if r['share']>=minq]
    G=collections.defaultdict(lambda:[0.0,0,0])
    for r in rows:
        g=grp(r['name']); G[g][0]+=r['share']; G[g][1]+=r['w']; G[g][2]+=r['w']+r['l']+r['d']
    out=[]
    for g,(s,w,t) in G.items():
        out.append({'group':g,'share':round(s,2),'awr':round((w+12)/(t+25)*100,2),'n':t})
    out.sort(key=lambda x:-x['awr'])
    print(f'=== {label} (n={len(rows)}) ===')
    for x in out: print(f"{x['group']:14} {x['share']:>7.2f}% {x['awr']:>7.2f}%  N={x['n']}")
    return out
b=build('memory/ptcgp_meta_20261028.json','branch 10-27')
c=build('memory/ptcgp_meta_20261028_comb.json','combine 10-27')
# yesterday for comparison
by=build('memory/ptcgp_meta_20261026.json','branch 10-26')
cy=build('memory/ptcgp_meta_20261026_comb.json','combine 10-26')
print('\n=== 電系雙雄 / 特定合併口徑 ===')
for path,lab in [('memory/ptcgp_meta_20261026_comb.json','10-26'),('memory/ptcgp_meta_20261028_comb.json','10-27')]:
    rs=json.load(open(path))
    def agg(f):
        sel=[r for r in rs if f(r['name'].lower())]
        sh=sum(r['share'] for r in sel); w=sum(r['w'] for r in sel); t=sum(r['w']+r['l']+r['d'] for r in sel)
        return round(sh,2),round((w+12)/(t+25)*100,2),t
    dz=agg(lambda n:'magnezone' in n or 'dedenne' in n)
    print(lab,'電系雙雄(磁怪+好壞電龍) %.2f%% / %.2f%% N=%d'%dz)
    for nm,f in [('電系全部',lambda n:any(k in n for k in ['magnezone','miraidon','dedenne','heliolisk','manectric','zeraora','rotom','indeedee','bellibolt','jolteon','electrode','zapdos','meowstic','raikou'])),
                 ('七夕青鳥',lambda n:'altaria' in n),('路卡利歐',lambda n:'lucario' in n),
                 ('胡帕',lambda n:'hoopa' in n),('蜂女王',lambda n:'vespiquen' in n),
                 ('三頭龍',lambda n:'hydreigon' in n),('巨牙鯊',lambda n:'sharpedo' in n),
                 ('火箭隊系',lambda n:'team rocket' in n),('拉達',lambda n:'raticate' in n),
                 ('烈咬陸鯊',lambda n:'garchomp' in n),('沙奈朵',lambda n:'gardevoir' in n),
                 ('火焰雞',lambda n:'blaziken' in n),('水君',lambda n:'suicune' in n),('哈克龍',lambda n:'dragonair' in n),
                 ('哈克龍系(rayquaza)',lambda n:'dragonair' in n or 'rayquaza' in n)]:
        s,a,t=agg(f); print(f'   {nm:20} {s:>6.2f}% {a:>6.2f}% N={t}')
