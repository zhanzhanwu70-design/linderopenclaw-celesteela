#!/usr/bin/env python3
"""2026-11-17 分析：合併口徑需對同名列做加總（Limitless 合併頁會因跨 set 同名拆列）。"""
import json, collections

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n


def agg_rows(rows):
    A = collections.defaultdict(lambda: [0.0, 0, 0, 0, set()])
    for r in rows:
        a = A[r['name']]
        a[0] += r['share']; a[1] += r['w']; a[2] += r['l']; a[3] += r['n']
        a[4].add(r['slug'])
    out = []
    for k, (s, w, l, n, slugs) in A.items():
        out.append({'name': k, 'share': round(s, 4), 'w': w, 'l': l, 'd': n - w - l, 'n': n,
                    'awr': round((w + 12) / (n + 25) * 100, 2) if n else 0,
                    'raw_wr': round(w / n * 100, 2) if n else 0,
                    'decks': sum(1 for _ in slugs), 'slugs': sorted(slugs)})
    out.sort(key=lambda x: -x['share'])
    return out


def grp(n):
    N = n.lower()
    if "team rocket" in N or "slowking" in N or "raticate" in N or "weezing" in N: return '火箭隊系'
    if any(k in N for k in ["greninja","suicune","baxcalibur","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi","palafin","blissey","chien-pao","blastoise","whiscash","clodsire","furfret","jellicent"]): return '水系'
    if any(k in N for k in ["magnezone","miraidon","dedenne","heliolisk","manectric","zeraora","rotom","jolteon","bellibolt","electrode","zapdos","meowstic","raikou","indeedee","pikachu","pachirisu","pawmot","oricorio","dialga","palkia","articuno","meltan","morpeko","togekiss","ampharos","houndoom"]): return '電系'
    if any(k in N for k in ["umbreon","espeon","leafeon","eevee","glaceon","sylveon","flareon","vaporeon","meowth","mimikyu","alcremie","meloetta","ditto"]): return '超能系'
    if any(k in N for k in ["charizard","moltres","entei","typhlosion","incineroar","landorus","heatmor","skeledirge","blaziken","fuecoco","gardevoir","mewtwo","mew","miltank","tauros","audino","carbink","wobbbufett","armarouge","ceruledge","armaldo","dondozo","tinkaton","scovillain","tsareena","decidueye","meowscarada","chesnaught","squawkabilly","feebas","annihilape","castform"]): return '火/超能系'
    if any(k in N for k in ["altaria","igglybuff","chingling","happiny","duraludon","dragonite","salamence","flygon","dragonair","garchomp","goomy","haxorus","goodra","drampa","latios","noivern","archaludon","bagon","shelgon","rayquaza","hydreigon","tyranitar","giratina","zoroark","absol","darkrai","sableye","banette","nihilego","gengar","mismagius","hatterene","hoopa","grimmsnarl","guzzlord","dragalge","dragapult","alolan exeggutor","latias"]): return '龍/惡系'
    if any(k in N for k in ["lucario","hitmon","medicham","gallade","machamp","annihilape","primeape","infernape","hitmontop","aegislash","gholdengo","excadrill","mienfoo","toxicroak","scrafty","sceptile","buzzwole","pheromosa","venomoth","beautifly","dustox","beedrill","ledian","volcarona","exeggutor","venusaur","abomasnow","torterra","lilligant","serperior","celebi","lurantis","bonsly","cherubi","chikorita","treecko","scizor","revavroom","ribombee","skarmory","mawile","clodsire","steelix","magcargo","forretress","klinklang","aggron","miltank","audino","medicham"]): return '格鬥/草/鋼系'
    if any(k in N for k in ["pidgeot","swellow","talonflame","staraptor","farfetch","rufflet","fletchling","pidgey","tornadus","landorus"]): return '飛行系'
    if any(k in N for k in ["azumarill","lopunny","raboot","pawmot","wigglytuff","clefairy","clefable","tinkaton","sylveon","miltank","tauros","blissey","chansey","snorlax","ambipom","eevee","galvantula"]): return '一般/妖精系'
    return '其他'


def build(rows, label):
    G = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rows:
        g = grp(r['name']); G[g][0] += r['share']; G[g][1] += r['w']; G[g][2] += r['n']
    out = []
    for g, (s, w, t) in G.items():
        out.append({'group': g, 'share': round(s, 2), 'awr': round((w + 12) / (t + 25) * 100, 2) if t else 0, 'n': t})
    out.sort(key=lambda x: -x['share'])
    print(f'=== {label} ===')
    for x in out: print(f"{x['group']:14} {x['share']:>7.2f}% {x['awr']:>7.2f}%  N={x['n']}")
    return out


T = json.load(open('memory/ptcgp_meta_20261117_std_comb.json'))
TB = json.load(open('memory/ptcgp_meta_20261117_std.json'))
Y = json.load(open('memory/ptcgp_meta_20261116_std_comb_re.json'))
YB = json.load(open('memory/ptcgp_meta_20261116_std_re.json'))
Y3 = json.load(open('memory/ptcgp_meta_20261115_std_comb_re.json'))

E = agg_rows(T['rows']); EB = agg_rows(TB['rows'])
Y_A = agg_rows(Y['rows']); Y3_A = agg_rows(Y3['rows'])
p = {r['name']: r for r in Y_A}
p3 = {r['name']: r for r in Y3_A}

print('### 今日合併 Top 25（已對同名加總）vs 昨')
for r in E[:25]:
    o = p.get(r['name'])
    if o:
        print(f"{zh(r['name'])[:28]:30} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4} | 昨 {o['share']:>5.2f}%/{o['awr']:>5.2f}% Δ{r['share']-o['share']:+.2f}pt/Δ{r['awr']-o['awr']:+.2f}pt")
    else:
        print(f"{zh(r['name'])[:28]:30} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4} | NEW")
print()
print('### 今日合併 AWR 前 15（N>=100）')
for r in sorted([x for x in E if x['n'] >= 100], key=lambda x: -x['awr'])[:15]:
    o = p.get(r['name'])
    print(f"{zh(r['name'])[:28]:30} {r['awr']:>6.2f}% 份額 {r['share']:>5.2f}% N={r['n']:>4}  昨 {o['awr'] if o else 0:>5.2f}%  Δ{(r['awr']-o['awr']) if o else 0:+.2f}")
print()
build(EB, '族群 分支口徑'); print(); build(E, '族群 合併口徑')
print()
print('### 陷阱：份額前 30 中 AWR < 48%')
for r in E[:30]:
    if r['awr'] < 48: print(f"{zh(r['name'])[:28]:30} 份額 {r['share']:>5.2f}% AWR {r['awr']:>6.2f}% N={r['n']}")
print()
print('### 分支口徑 Top 25 今日 vs 昨（未加總，分支頁本身無同名）')
B = {r['slug']: r for r in json.load(open('memory/ptcgp_meta_20261116_std_re.json'))['rows']}
for r in TB['rows'][:25]:
    o = B.get(r['slug'])
    ex = f" | 昨 {o['share']:>5.2f}%/{o['awr']:>5.2f}% Δ{r['share']-o['share']:+.2f}/{r['awr']-o['awr']:+.2f}" if o else ' | 新進榜'
    print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4}{ex}")
print()
print('### 分支 AWR 前 12（N>=100）')
for r in sorted([x for x in TB['rows'] if x['n'] >= 100], key=lambda x: -x['awr'])[:12]:
    print(f"{zh(r['name'])[:30]:32} {r['awr']:>6.2f}% 份額 {r['share']:>5.2f}% N={r['n']}")
print()
print('### 關鍵牌組三日趨勢（合併，已加總）')
for k in ['Mega Charizard Y ex', 'Umbreon', 'Mega Altaria ex', 'Suicune ex', 'Mega Greninja ex',
          'Hoopa ex', 'Mega Lucario ex', 'Mega Mewtwo X ex', 'Vespiquen ex', 'Magnezone',
          'Giratina ex', 'Mega Manectric ex', 'Mega Sceptile ex', 'Hydreigon', 'Pikachu ex',
          'Mega Tyranitar ex', 'Lopunny', 'Miraidon ex', 'Alolan Exeggutor ex', 'Dragonair',
          'Mega Dragonite ex', 'Mega Skarmory ex', 'Mega Blaziken ex']:
    t = next((r for r in E if r['name'] == k), None)
    y = p.get(k); y3 = p3.get(k)
    def f(r): return f"{r['share']:>5.2f}%/{r['awr']:>5.2f}%" if r else '   --    '
    d1 = f"{t['share']-y['share']:+.2f}/{t['awr']-y['awr']:+.2f}" if (t and y) else '  --  '
    print(f"{zh(k)[:26]:28} 今日 {f(t)}  昨 {f(y)}  前 {f(y3)}  Δ{d1}")
print()
w = sum(r['w'] for r in E); n = sum(r['n'] for r in E)
wY = sum(r['w'] for r in Y_A); nY = sum(r['n'] for r in Y_A)
print(f'全環境加權 AWR（合併口徑）= {(w+12)/(n+25)*100:.2f}%  N={n}   (昨 {(wY+12)/(nY+25)*100:.2f}%)')
