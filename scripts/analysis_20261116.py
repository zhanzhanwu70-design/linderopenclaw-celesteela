#!/usr/bin/env python3
"""2026-11-16 PTCGP Meta 分析。"""
import json, collections

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n


def grp(n):
    N = n.lower()
    if "team rocket" in N or "slowking" in N or "raticate" in N or "weezing" in N: return '火箭隊系'
    if any(k in N for k in ["greninja","suicune","baxcalibur","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi","palafin","blissey","chien-pao","blastoise","whiscash","clodsire","furfret","jellicent","wishiwashi","palafin","squawkabilly","feebas","milotic","kingdra","goomy"]): return '水系'
    if any(k in N for k in ["magnezone","miraidon","dedenne","heliolisk","manectric","zeraora","rotom","jolteon","bellibolt","electrode","zapdos","meowstic","raikou","indeedee","pikachu","pachirisu","pawmot","oricorio","dialga","palkia","articuno","meltan","morpeko","togekiss","ampharos","houndoom","bellibolt","electivire","plusle","minior","voltorb"]): return '電系'
    if any(k in N for k in ["umbreon","espeon","leafeon","eevee","glaceon","sylveon","flareon","vaporeon","meowth","mimikyu","alcremie","meloetta","indeedee","mrrime","morpeko","mimikyu","ditto"]): return '超能系'
    if any(k in N for k in ["charizard","moltres","entei","typhlosion","incineroar","landorus","heatmor","skeledirge","blaziken","fuecoco","gardevoir","mewtwo","mew","miltank","tauros","audino","carbink","wobbbufett","armarouge","ceruledge","armaldo","dondozo","tinkaton","palafin","scovillain","tsareena","decidueye","meowscarada","chesnaught","archaludon","squawkabilly","feebas","annihilape"]): return '火/超能系'
    if any(k in N for k in ["altaria","igglybuff","chingling","happiny","duraludon","dragonite","salamence","flygon","dragonair","garchomp","goomy","haxorus","goodra","drampa","latios","noivern","archaludon","bagon","shelgon","rayquaza","hydreigon","tyranitar","giratina","zoroark","absol","darkrai","sableye","banette","nihilego","gengar","mismagius","hatterene","hoopa","grimmsnarl","guzzlord","dragalge","dragapult","dragonite","alolan exeggutor","milotic","latias","latios","tinkaton","duraludon"]): return '龍/惡系'
    if any(k in N for k in ["lucario","hitmon","medicham","gallade","machamp","annihilape","primeape","infernape","hitmontop","aegislash","gholdengo","excadrill","mienfoo","toxicroak","scrafty","sceptile","buzzwole","pheromosa","venomoth","beautifly","dustox","beedrill","ledian","volcarona","exeggutor","venusaur","abomasnow","torterra","lilligant","serperior","celebi","lurantis","bonsly","cherubi","chikorita","treecko","scizor","revavroom","ribombee","skarmory","mawile","clodsire","miltank","audino","medicham","aggron","steelix","magcargo","forretress","klinklang","lairon","sandslash","simisear","charjabug","vikavolt","beedrill","wormadam","burmy"]): return '格鬥/草/鋼系'
    if any(k in N for k in ["pidgeot","swellow","talonflame","staraptor","farfetch","rufflet","fletchling","pidgey","talonflame","staraptor","tornadus","landorus"]): return '飛行系'
    if any(k in N for k in ["azumarill","lopunny","raboot","pawmot","wigglytuff","clefairy","clefable","tinkaton","sylveon","miltank","tauros","blissey","chansey","snorlax","miltank","audino","girafarig","eevee"]): return '一般/妖精系'
    return '其他'


def build(rows, label, minq=0.0):
    rr = [r for r in rows if r['share'] >= minq]
    G = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rr:
        g = grp(r['name']); G[g][0] += r['share']; G[g][1] += r['w']; G[g][2] += r['n']
    out = []
    for g, (s, w, t) in G.items():
        out.append({'group': g, 'share': round(s, 2), 'awr': round((w + 12) / (t + 25) * 100, 2) if t else 0, 'n': t})
    out.sort(key=lambda x: -x['share'])
    print(f'=== {label} (rows={len(rr)}) ===')
    for x in out: print(f"{x['group']:14} {x['share']:>7.2f}% {x['awr']:>7.2f}%  N={x['n']}")
    return out


T = json.load(open('memory/ptcgp_meta_20261116_std_comb.json'))
TB = json.load(open('memory/ptcgp_meta_20261116_std.json'))
E = T['rows']; EB = TB['rows']
Y = json.load(open('memory/ptcgp_meta_20261115_std_comb_re.json'))
YB = json.load(open('memory/ptcgp_meta_20261115_std_re.json'))
Y3 = json.load(open('memory/ptcgp_meta_20261114_std_comb_re.json'))
p = {r['slug']: r for r in Y['rows']}
pb = {r['slug']: r for r in YB['rows']}
p3 = {r['slug']: r for r in Y3['rows']}

print('### 今日合併 Top 25 vs 昨（份額）')
for r in E[:25]:
    o = p.get(r['slug'])
    if o:
        print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4} | 昨 {o['share']:>5.2f}%/{o['awr']:>5.2f}% Δ{r['share']-o['share']:+.2f}pt/Δ{r['awr']-o['awr']:+.2f}pt")
    else:
        print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4} | NEW")
print()
print('### 今日合併 AWR 前 15（N>=100）')
for r in sorted([x for x in E if x['n'] >= 100], key=lambda x: -x['awr'])[:15]:
    print(f"{zh(r['name'])[:30]:32} {r['awr']:>6.2f}%  份額 {r['share']:>5.2f}% N={r['n']}  昨 {p[r['slug']]['awr'] if r['slug'] in p else 0:>5.2f}%")
print()
build(EB, '族群 分支口徑'); print(); build(E, '族群 合併口徑')
print()

cards = json.load(open('memory/ptcgp_cards_full.json'))
C1N = set(c.get('name') for k, c in cards.items() if k.startswith('C1_') and c.get('name'))


def has_c1(nm):
    n = nm.replace("’", "'")
    for c in C1N:
        c2 = c.replace("’", "'")
        if n.startswith(c2) or n.startswith(c2.replace(' ex', 'ex')): return True
    return False


for label, rows in [('合併', E), ('分支', EB)]:
    a = [r for r in rows if has_c1(r['name'])]; b = [r for r in rows if not has_c1(r['name'])]
    for tag, g in (('含C1新卡', a), ('不含新卡', b)):
        s = sum(r['share'] for r in g); w = sum(r['w'] for r in g); n = sum(r['n'] for r in g)
        print(f"{label} {tag}: 份額 {s:.2f}% / AWR {(w+12)/(n+25)*100:.2f}% / N={n}")
print()
print('### 陷阱：份額前 30 中 AWR < 48%')
for r in E[:30]:
    if r['awr'] < 48: print(f"{zh(r['name'])[:30]:32} 份額 {r['share']:>5.2f}% AWR {r['awr']:>6.2f}% N={r['n']}")
print()
print('### 分支口徑 Top 25 今日 vs 昨')
for r in EB[:25]:
    o = pb.get(r['slug'])
    ex = f" | 昨 {o['share']:>5.2f}%/{o['awr']:>5.2f}% Δ{r['share']-o['share']:+.2f}/{r['awr']-o['awr']:+.2f}" if o else ' | 新進榜'
    print(f"{zh(r['name'])[:32]:34} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4}{ex}")
print()
print('### 分支 AWR 前 12（N>=100）')
for r in sorted([x for x in EB if x['n'] >= 100], key=lambda x: -x['awr'])[:12]:
    print(f"{zh(r['name'])[:32]:34} {r['awr']:>6.2f}% 份額 {r['share']:>5.2f}% N={r['n']}")
print()
print('### 新進榜（合併口徑，份額>=0.15%）')
for r in E:
    if r['slug'] not in p and r['share'] >= 0.15:
        print(f"{zh(r['name'])[:32]:34} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']}")
print()
print('### 退出合併前 40（昨在今不在）')
for r in Y['rows'][:40]:
    if r['slug'] not in {x['slug'] for x in E[:40]}:
        print(f"{zh(r['name'])[:32]:34} 昨 {r['share']:>5.2f}%/{r['awr']:>5.2f}%")
print()
w = sum(r['w'] for r in E); n = sum(r['n'] for r in E)
wY = sum(r['w'] for r in Y['rows']); nY = sum(r['n'] for r in Y['rows'])
print(f'全環境加權 AWR（合併口徑）= {(w+12)/(n+25)*100:.2f}%  N={n}   (昨 {(wY+12)/(nY+25)*100:.2f}%)')
print()
print('### 關鍵牌組三日趨勢（合併）')
KEYS = ['Mega Charizard Y ex', 'Umbreon', 'Mega Altaria ex', 'Suicune ex', 'Mega Greninja ex',
        'Hoopa ex', 'Mega Lucario ex', 'Mega Mewtwo X ex', 'Vespiquen ex', 'Magnezone',
        'Giratina ex', 'Greninja ex', 'Mega Manectric ex', 'Mega Sceptile ex', 'Hydreigon',
        'Pikachu ex', 'Mega Tyranitar ex', 'Lopunny', 'Miraidon ex', 'Alolan Exeggutor ex',
        'Dragonair', 'Mega Dragonite ex', 'Mega Skarmory ex', 'Mega Blaziken ex', 'Mega Audino ex',
        'Mega Gallade ex', 'Mega Latios ex', 'Mega Gyarados ex', 'Mega Pidgeot ex']
for k in KEYS:
    t = next((r for r in E if r['name'] == k), None)
    y = next((r for r in Y['rows'] if r['name'] == k), None)
    y3 = next((r for r in Y3['rows'] if r['name'] == k), None)
    def f(r): return f"{r['share']:>5.2f}%/{r['awr']:>5.2f}%" if r else '   --   '
    d1 = f"{t['share']-y['share']:+.2f}/{t['awr']-y['awr']:+.2f}" if (t and y) else '  --  '
    print(f"{zh(k)[:28]:30} 今日 {f(t)}  昨 {f(y)}  前日 {f(y3)}  Δ{d1}")
print()
print('### HP 分桶（分支口徑，N>=30）')
import re
HPB = collections.defaultdict(lambda: [0.0, 0, 0])
for r in EB:
    m = re.search(r'([A-Z]\d[a-z]?_\d+)', r['slug'])
    hp = None
    if r['slug']:
        # 從卡庫抓 HP 不可靠，改用 deck slug 對應的第一張卡
        pass
    HPB['skip'][0] += 0
# 用卡庫對 deck name 前段推 HP
name2hp = {}
for k, c in cards.items():
    if c.get('name') and c.get('hp'):
        name2hp.setdefault(c['name'], c['hp'])
for r in EB:
    if r['n'] < 30: continue
    hp = None
    for nm, h in name2hp.items():
        if r['name'].startswith(nm):
            hp = max(hp or 0, h)
    if hp is None: continue
    b = '≤120' if hp <= 120 else ('130-160' if hp <= 160 else ('170-200' if hp <= 200 else '210+'))
    HPB[b][0] += r['share']; HPB[b][1] += r['w']; HPB[b][2] += r['n']
for b, (s, w, t) in sorted(HPB.items(), key=lambda kv: -(kv[1][1] + 12) / (kv[1][2] + 25)):
    print(f"{b:>8}  份額 {s:>6.2f}%  AWR {(w+12)/(t+25)*100:>6.2f}%  N={t}")
