import json, collections

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n

def grp(n):
    N = n.lower()
    if "team rocket" in N or "slowking" in N or "raticate" in N or "weezing" in N: return '火箭隊系'
    if any(k in N for k in ["greninja","suicune","baxcalibur","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi","palafin","blissey","chien-pao","blastoise","whiscash","clodsire","furfret"]): return '水系'
    if any(k in N for k in ["magnezone","miraidon","dedenne","heliolisk","manectric","zeraora","rotom","jolteon","bellibolt","electrode","zapdos","meowstic","raikou","indeedee","pikachu","pachirisu","pawmot","oricorio","dialga","palkia","articuno","meltan","morpeko","togekiss"]): return '電系'
    if any(k in N for k in ["umbreon","espeon","leafeon","eevee","glaceon","sylveon","flareon","vaporeon","meowth"]): return '超能系'
    if any(k in N for k in ["charizard","moltres","entei","typhlosion","incineroar","landorus","heatmor","skeledirge","blaziken","fuecoco","gardevoir","mimikyu","meloetta","alcremie","tinkaton","sandslash","simisear","charcadet","centiskorch","scovillain","tsareena","decidueye","meowscarada","chesnaught","mewtwo","mew","miltank","tauros","audino","carbink","wobbbufett"]): return '火/超能系'
    if any(k in N for k in ["altaria","igglybuff","chingling","happiny","duraludon","dragonite","salamence","flygon","dragonair","garchomp","goomy","haxorus","goodra","drampa","latios","noivern","archaludon","bagon","shelgon","rayquaza","hydreigon","tyranitar","giratina","zoroark","absol","darkrai","sableye","banette","nihilego","gengar","mismagius","hatterene","hoopa","grimmsnarl","guzzlord","dragalge","tyranitar"]): return '龍/惡系'
    if any(k in N for k in ["lucario","hitmon","medicham","gallade","machamp","annihilape","primeape","infernape","hitmontop","aegislash","gholdengo","excadrill","mienfoo","toxicroak","scrafty","sceptile","buzzwole","pheromosa","venomoth","beautifly","dustox","beedrill","ledian","volcarona","exeggutor","venusaur","abomasnow","torterra","lilligant","serperior","celebi","lurantis","bonsly","cherubi","chikorita","treecko","scizor","revavroom","ribombee","bellibolt","dragapult","iron","steelix","skarmory","mawile"]): return '格鬥/草/鋼系'
    if any(k in N for k in ["pidgeot","swellow","talonflame","staraptor","farfetch","rufflet","fletchling"]): return '飛行系'
    if any(k in N for k in ["azumarill","lopunny","raboot","pawmot","wigglytuff","clefairy","clefable","tinkaton","sylveon","miltank","tauros"]): return '一般/妖精系'
    return '其他'

def build(rows, label, minq=0.0):
    rr=[r for r in rows if r['share']>=minq]
    G=collections.defaultdict(lambda:[0.0,0,0])
    for r in rr:
        g=grp(r['name']); G[g][0]+=r['share']; G[g][1]+=r['w']; G[g][2]+=r['n']
    out=[]
    for g,(s,w,t) in G.items():
        out.append({'group':g,'share':round(s,2),'awr':round((w+12)/(t+25)*100,2) if t else 0,'n':t})
    out.sort(key=lambda x:-x['share'])
    print(f'=== {label} (rows={len(rr)}) ===')
    for x in out: print(f"{x['group']:14} {x['share']:>7.2f}% {x['awr']:>7.2f}%  N={x['n']}")
    return out

T=json.load(open('memory/ptcgp_meta_20261103_std_comb.json'))
TB=json.load(open('memory/ptcgp_meta_20261103_std.json'))
E=T['rows']; EB=TB['rows']
Y=json.load(open('memory/ptcgp_meta_20261102_std_comb_re.json'))
YB=json.load(open('memory/ptcgp_meta_20261102_std_re.json'))
p={r['slug']:r for r in Y['rows']}
pb={r['slug']:r for r in YB['rows']}

print('### 今日合併 Top 25 vs 昨')
for r in E[:25]:
    o=p.get(r['slug'])
    if o: print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4} | 昨 {o['share']:>5.2f}%/{o['awr']:>5.2f}% Δ{r['share']-o['share']:+.2f}pt/Δ{r['awr']-o['awr']:+.2f}pt")
    else: print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4} | NEW")
print()
print('### 今日合併 AWR 前 15（N>=100）')
for r in sorted([x for x in E if x['n']>=100], key=lambda x:-x['awr'])[:15]:
    print(f"{zh(r['name'])[:30]:32} {r['awr']:>6.2f}% 份額 {r['share']:>5.2f}% N={r['n']}")
print()
build(EB,'族群 分支口徑'); print(); build(E,'族群 合併口徑')
print()
cards=json.load(open('memory/ptcgp_cards_full.json'))
C1N=set(c.get('name') for k,c in cards.items() if k.startswith('C1_') and c.get('name'))
def has_c1(nm):
    n=nm.replace("’","'")
    for c in C1N:
        c2=c.replace("’","'")
        if n.startswith(c2) or n.startswith(c2.replace(' ex','ex')): return True
    return False
for label,rows in [('合併',E),('分支',EB)]:
    a=[r for r in rows if has_c1(r['name'])]; b=[r for r in rows if not has_c1(r['name'])]
    for tag,g in (('含C1新卡',a),('不含新卡',b)):
        s=sum(r['share'] for r in g); w=sum(r['w'] for r in g); n=sum(r['n'] for r in g)
        print(f"{label} {tag}: 份額 {s:.2f}% / AWR {(w+12)/(n+25)*100:.2f}% / N={n}")
print()
print('### 陷阱：份額前 30 中 AWR < 48%')
for r in E[:30]:
    if r['awr']<48: print(f"{zh(r['name'])[:30]:32} 份額 {r['share']:>5.2f}% AWR {r['awr']:>6.2f}% N={r['n']}")
print()
print('### 分支口徑 Top 20 今日 vs 昨')
for r in EB[:20]:
    o=pb.get(r['slug'])
    ex=f" | 昨 {o['share']:>5.2f}%/{o['awr']:>5.2f}% Δ{r['share']-o['share']:+.2f}/{r['awr']-o['awr']:+.2f}" if o else ' | 新進榜'
    print(f"{zh(r['name'])[:32]:34} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4}{ex}")
print()
print('### 分支 AWR 前 12（N>=100）')
for r in sorted([x for x in EB if x['n']>=100], key=lambda x:-x['awr'])[:12]:
    print(f"{zh(r['name'])[:32]:34} {r['awr']:>6.2f}% 份額 {r['share']:>5.2f}% N={r['n']}")
print()
print('### 新進榜（合併口徑，份額>=0.3%）')
for r in E:
    if r['slug'] not in p and r['share']>=0.3:
        print(f"{zh(r['name'])[:32]:34} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']}")
print()
w=sum(r['w'] for r in E); n=sum(r['n'] for r in E)
print(f'全環境加權 AWR（合併口徑）= {(w+12)/(n+25)*100:.2f}%  N={n}')
print()
print('### 高 HP 對照（3 點 KO 規則）')
for r in E[:20]:
    print(f"{zh(r['name'])[:32]:34} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']}")
