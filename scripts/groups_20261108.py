import json, collections

D = json.load(open('ptcgp_deck_dictionary.json'))
def zh(n): return D['deck_names'].get(n) or D['card_names'].get(n) or n

def grp(n):
    N = n.lower()
    if "team rocket" in N or "slowking" in N or "raticate" in N or "weezing" in N: return '火箭隊系'
    if any(k in N for k in ["greninja","suicune","baxcalibur","milotic","gyarados","sharpedo","vaporeon","wailord","swanna","pyukumuku","wishiwashi","palafin","blissey","chien-pao","blastoise","whiscash","clodsire","furfret"]): return '水系'
    if any(k in N for k in ["magnezone","miraidon","dedenne","heliolisk","manectric","zeraora","rotom","jolteon","bellibolt","electrode","zapdos","meowstic","raikou","indeedee","pikachu","pachirisu","pawmot","oricorio","dialga","palkia","articuno","meltan","morpeko","togekiss"]): return '電系'
    if any(k in N for k in ["umbreon","espeon","leafeon","eevee","glaceon","sylveon","flareon","vaporeon","meowth"]): return '超能系'
    if any(k in N for k in ["charizard","moltres","entei","typhlosion","incineroar","landorus","heatmor","skeledirge","blaziken","fuecoco","gardevoir","mimikyu","meloetta","alcremie","tinkaton","sandslash","simisear","charcadet","centiskorch","scovillain","tsareena","decidueye","meowscarada","chesnaught","mewtwo","mew","miltank","tauros","audino","carbink","wobbbufett"]): return '火/超能系'
    if any(k in N for k in ["altaria","igglybuff","chingling","happiny","duraludon","dragonite","salamence","flygon","dragonair","garchomp","goomy","haxorus","goodra","drampa","latios","noivern","archaludon","bagon","shelgon","rayquaza","hydreigon","tyranitar","giratina","zoroark","absol","darkrai","sableye","banette","nihilego","gengar","mismagius","hatterene","hoopa","grimmsnarl","guzzlord","dragalge"]): return '龍/惡系'
    if any(k in N for k in ["lucario","hitmon","medicham","gallade","machamp","annihilape","primeape","infernape","hitmontop","aegislash","gholdengo","excadrill","mienfoo","toxicroak","scrafty","sceptile","buzzwole","pheromosa","venomoth","beautifly","dustox","beedrill","ledian","volcarona","exeggutor","venusaur","abomasnow","torterra","lilligant","serperior","celebi","lurantis","bonsly","cherubi","chikorita","treecko","scizor","revavroom","ribombee","bellibolt","dragapult","iron","steelix","skarmory","mawile"]): return '格鬥/草/鋼系'
    if any(k in N for k in ["pidgeot","swellow","talonflame","staraptor","farfetch","rufflet","fletchling"]): return '飛行系'
    if any(k in N for k in ["azumarill","lopunny","raboot","pawmot","wigglytuff","clefairy","clefable","tinkaton","sylveon","miltank","tauros"]): return '一般/妖精系'
    return '其他'

def groups(path):
    rows = json.load(open(path))['rows']
    G = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rows:
        g = grp(r['name']); G[g][0] += r['share']; G[g][1] += r['w']; G[g][2] += r['n']
    out = {}
    for g, (s, w, t) in G.items():
        out[g] = {'share': round(s, 2), 'awr': round((w+12)/(t+25)*100, 2) if t else 0, 'n': t}
    return out

days = [('20261105','memory/ptcgp_meta_20261105_std_comb_re.json'),
        ('20261106','memory/ptcgp_meta_20261106_std_comb_re.json'),
        ('20261107','memory/ptcgp_meta_20261107_std_comb_re.json'),
        ('20261108','memory/ptcgp_meta_20261108_std_comb.json')]
G = {d: groups(p) for d, p in days}
names = sorted({g for d in G for g in G[d]}, key=lambda g: -G['20261108'][g]['share'])
print('族群'.ljust(14) + '  '.join(f'{d[4:]:>22}' for d, _ in days))
for g in names:
    cells = []
    for d, _ in days:
        x = G[d].get(g)
        cells.append(f"{x['share']:.2f}%/{x['awr']:.2f}%" if x else "--")
    print(f'{g:14} ' + '  '.join(f'{c:>22}' for c in cells))

print()
print('### 新卡 vs 舊卡（合併口徑）')
cards = json.load(open('memory/ptcgp_cards_full.json'))
C1N = set(c.get('name') for k, c in cards.items() if k.startswith('C1_') and c.get('name'))
def has_c1(nm):
    n = nm.replace("’", "'")
    for c in C1N:
        c2 = c.replace("’", "'")
        if n.startswith(c2) or n.startswith(c2.replace(' ex', 'ex')): return True
    return False
for d, p in days:
    rows = json.load(open(p))['rows']
    a = [r for r in rows if has_c1(r['name'])]; b = [r for r in rows if not has_c1(r['name'])]
    res = []
    for tag, g in (('含新卡', a), ('不含新卡', b)):
        s = sum(r['share'] for r in g); w = sum(r['w'] for r in g); n = sum(r['n'] for r in g)
        res.append(f"{tag} {s:.2f}%/{(w+12)/(n+25)*100:.2f}%")
    gap = (sum(r['w'] for r in b)+12)/(sum(r['n'] for r in b)+25)*100 - (sum(r['w'] for r in a)+12)/(sum(r['n'] for r in a)+25)*100
    print(f"{d}: " + ' | '.join(res) + f" | 差距 {gap:.2f}pt")

print()
print('### 分支口徑新進榜（今日 vs 11-07，份額 >= 0.2%）')
y = {r['slug']: r for r in json.load(open('memory/ptcgp_meta_20261107_std_re.json'))['rows']}
for r in json.load(open('memory/ptcgp_meta_20261108_std.json'))['rows']:
    if r['slug'] not in y and r['share'] >= 0.2:
        print(f"  新 {zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']}")
print('### 分支口徑退出前 40 的牌組')
t40 = {r['slug'] for r in json.load(open('memory/ptcgp_meta_20261108_std.json'))['rows'][:40]}
y40 = {r['slug'] for r in json.load(open('memory/ptcgp_meta_20261107_std_re.json'))['rows'][:40]}
for s in y40 - t40:
    r = [x for x in json.load(open('memory/ptcgp_meta_20261107_std_re.json'))['rows'] if x['slug'] == s][0]
    print(f"  退 {zh(r['name'])[:30]:32} 昨 {r['share']:>6.2f}% {r['awr']:>6.2f}%")

print()
print('### 最差榜（合併口徑，N>=50）')
rows = json.load(open('memory/ptcgp_meta_20261108_std_comb.json'))['rows']
for r in sorted([x for x in rows if x['n']>=50], key=lambda x:x['awr'])[:12]:
    print(f"  {zh(r['name'])[:28]:30} {r['awr']:>6.2f}% 份額 {r['share']:>5.2f}% N={r['n']}")

print()
print('### Standard vs set=C1 一致性')
s = json.load(open('memory/ptcgp_meta_20261108_std.json'))['rows']
c = json.load(open('memory/ptcgp_meta_20261108_C1.json'))['rows']
print('  std rows', len(s), 'C1 rows', len(c), 'slug set equal:', {x['slug'] for x in s}=={x['slug'] for x in c})
