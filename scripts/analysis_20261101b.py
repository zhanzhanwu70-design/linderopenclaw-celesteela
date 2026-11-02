import json, collections
D=json.load(open('ptcgp_deck_dictionary.json'))
dn=D['deck_names']; cn=D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n
def grp(n):
    N=n.lower()
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
def build(rows,label,minq=0.15):
    rr=[r for r in rows if r['share']>=minq]
    G=collections.defaultdict(lambda:[0.0,0,0])
    for r in rr:
        g=grp(r['name']); G[g][0]+=r['share']; G[g][1]+=r['w']; G[g][2]+=r['n']
    out=[]
    for g,(s,w,t) in G.items():
        out.append({'group':g,'share':round(s,2),'awr':round((w+12)/(t+25)*100,2) if t else 0,'n':t})
    out.sort(key=lambda x:-x['share']); return out

E=json.load(open('memory/ptcgp_meta_20261101_c1_comb.json'))
EB=json.load(open('memory/ptcgp_meta_20261101_c1.json'))
P=json.load(open('memory/ptcgp_meta_20261031e_c1_comb.json'))
PB=json.load(open('memory/ptcgp_meta_20261031e_c1.json'))

print('### 族群 合併口徑 今日 vs 昨')
gt=build(E,'今'); gp=build(P,'昨')
pm={x['group']:x for x in gp}
for x in gt:
    o=pm.get(x['group'])
    print(f"{x['group']:12} {x['share']:>6.2f}% {x['awr']:>6.2f}% N={x['n']:>5} | 昨 {o['share']:>6.2f}% {o['awr']:>6.2f}% N={o['n']:>5} Δ{x['share']-o['share']:+.2f}pt/Δ{x['awr']-o['awr']:+.2f}pt" if o else f"{x['group']} NEW")
print()
print('### 族群 分支口徑 今日 vs 昨')
gt=build(EB,'今'); gp=build(PB,'昨'); pm={x['group']:x for x in gp}
for x in gt:
    o=pm.get(x['group'])
    print(f"{x['group']:12} {x['share']:>6.2f}% {x['awr']:>6.2f}% N={x['n']:>5} | 昨 {o['share']:>6.2f}% {o['awr']:>6.2f}% N={o['n']:>5} Δ{x['share']-o['share']:+.2f}pt/Δ{x['awr']-o['awr']:+.2f}pt" if o else f"{x['group']} NEW")
print()
# 前50 進榜/退榜
rt={r['slug']:r for r in E}; rp={r['slug']:r for r in P}
top_now=[r['slug'] for r in E[:50]]; top_prev=[r['slug'] for r in P[:50]]
print('### 合併前 50 新進榜:', [zh(rt[s]['name']) for s in top_now if s not in top_prev])
print('### 合併前 50 退榜:', [zh(rp[s]['name']) for s in top_prev if s not in top_now])
print()
# 忍蛙系/電系/月亮伊布系 明細
def fam(rows, keys):
    out=[]
    for r in rows:
        if any(k in r['name'].lower() for k in keys): out.append(r)
    s=sum(x['share'] for x in out); w=sum(x['w'] for x in out); n=sum(x['n'] for x in out)
    return out, round(s,2), round((w+12)/(n+25)*100,2), n
for lab,keys in [('忍蛙系(mega greninja)',['mega greninja ex']),('甲賀忍蛙ex系',['greninja ex mega greninja','greninja ex ']),('月亮伊布系',['umbreon']),('電系',['magnezone','miraidon','manectric','raikou','dedenne','articuno','pikachu','electrode','zapdos','bellibolt','rotom','zeraora','indeedee','meltan','morpeko','pachirisu','togekiss','heliolisk']),('騎拉帝納系',['giratina ex']),('胡帕系',['hoopa']),('超級超夢X',['mega mewtwo x']),('七夕青鳥系',['mega altaria']),('噴火龍Y',['mega charizard y'])]:
    for tag,rows in [('今',E),('昨',P)]:
        lst,s,a,n = fam(rows,keys)
        print(f"{lab:26} {tag} 份額 {s:>6.2f}% AWR {a:>6.2f}% N={n} rows={len(lst)}")
    print()
