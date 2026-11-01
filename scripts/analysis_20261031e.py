import json, collections

d0 = json.load(open('ptcgp_deck_dictionary.json'))
dn = d0['deck_names']; cn = d0['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n

def grp(n):
    N = n.lower()
    if "team rocket" in N or "slowking" in N or "raticate" in N or "weezing" in N: return '火箭隊系'
    if any(k in N for k in ["greninja", "suicune", "baxcalibur", "milotic", "gyarados", "sharpedo", "vaporeon", "wailord", "swanna", "pyukumuku", "wishiwashi", "palafin", "blissey", "chien-pao", "blastoise", "whiscash", "clodsire", "furfret"]): return '水系'
    if any(k in N for k in ["magnezone", "miraidon", "dedenne", "heliolisk", "manectric", "zeraora", "rotom", "jolteon", "bellibolt", "electrode", "zapdos", "meowstic", "raikou", "indeedee", "pikachu", "pachirisu", "pawmot", "oricorio", "dialga", "palkia", "articuno", "meltan", "morpeko", "togekiss"]): return '電系'
    if any(k in N for k in ["umbreon", "espeon", "leafeon", "eevee", "glaceon", "sylveon", "flareon", "jolteon", "vaporeon", "meowth"]): return '超能系'
    if any(k in N for k in ["charizard", "moltres", "entei", "typhlosion", "incineroar", "landorus", "heatmor", "skeledirge", "blaziken", "fuecoco", "gardevoir", "mimikyu", "meloetta", "alcremie", "tinkaton", "sandslash", "simisear", "charcadet", "centiskorch", "scovillain", "tsareena", "decidueye", "meowscarada", "chesnaught", "mewtwo", "mew", "miltank", "tauros", "audino", "carbink", "wobbbufett", "blissey"]): return '火/超能系'
    if any(k in N for k in ["altaria", "igglybuff", "chingling", "happiny", "duraludon", "dragonite", "salamence", "flygon", "dragonair", "garchomp", "goomy", "haxorus", "goodra", "drampa", "latios", "noivern", "archaludon", "bagon", "shelgon", "rayquaza", "hydreigon", "tyranitar", "giratina", "dialga", "palkia", "zoroark", "absol", "darkrai", "sableye", "banette", "weezing", "nihilego", "gengar", "mismagius", "hatterene", "slowking", "hoopa", "darkrai", "grimmsnarl", "morpeko", "guzzlord", "dragalge", "tyranitar"]): return '龍/惡系'
    if any(k in N for k in ["lucario", "hitmon", "medicham", "gallade", "machamp", "annihilape", "primeape", "infernape", "hitmontop", "aegislash", "gholdengo", "excadrill", "mienfoo", "toxicroak", "scrafty", "lucario", "sceptile", "buzzwole", "pheromosa", "venomoth", "beautifly", "dustox", "beedrill", "ledian", "volcarona", "exeggutor", "venusaur", "abomasnow", "torterra", "lilligant", "serperior", "celebi", "lurantis", "bonsly", "cherubi", "chikorita", "treecko", "scizor", "revavroom", "ribombee", "volcarona", "bellibolt", "sceptile", "dragapult", "iron", "steelix", "skarmory", "mawile", "archaludon", "duraludon"]): return '格鬥/草/鋼系'
    if any(k in N for k in ["pidgeot", "swellow", "talonflame", "staraptor", "farfetch", "rufflet", "fletchling"]): return '飛行系'
    if any(k in N for k in ["azumarill", "lopunny", "raboot", "pawmot", "blissey", "wigglytuff", "clefairy", "clefable", "tinkaton", "sylveon", "miltank", "tauros"]): return '一般/妖精系'
    return '其他'

def build(rows, label, minq=0.15):
    rr = [r for r in rows if r['share'] >= minq]
    G = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rr:
        g = grp(r['name']); G[g][0] += r['share']; G[g][1] += r['w']; G[g][2] += r['n']
    out = []
    for g, (s, w, t) in G.items():
        out.append({'group': g, 'share': round(s, 2), 'awr': round((w + 12) / (t + 25) * 100, 2), 'n': t})
    out.sort(key=lambda x: -x['share'])
    print(f'=== {label} (rows={len(rr)}) ===')
    for x in out: print(f"{x['group']:14} {x['share']:>7.2f}% {x['awr']:>7.2f}%  N={x['n']}")
    return out

E = json.load(open('memory/ptcgp_meta_20261031e_c1_comb.json'))
EB = json.load(open('memory/ptcgp_meta_20261031e_c1.json'))
M = json.load(open('memory/ptcgp_meta_20261031_c1_comb.json'))
MB = json.load(open('memory/ptcgp_meta_20261031_c1.json'))

print('### 晚間（20:05）C1 合併 Top 20 vs 早間（05:45）')
mb = {r['slug']: r for r in M}
for r in E[:20]:
    o = mb.get(r['slug'])
    print(f"{zh(r['name'])[:26]:28} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4}  | 早 {o['share']:.2f}%/{o['awr']:.2f}%  Δ{r['share']-o['share']:+.2f}pt / Δ{r['awr']-o['awr']:+.2f}pt" if o else f"{zh(r['name'])} NEW")

print()
build(EB, 'C1 分支口徑 族群')
print()
build(E, 'C1 合併口徑 族群')
print()

# 含 C1 新卡 vs 不含
C1_NAMES = set()
cards = json.load(open('memory/ptcgp_cards_full.json'))
for k, c in cards.items():
    if k.startswith('C1_'): C1_NAMES.add(c.get('name'))
def has_c1(deckname):
    toks = [t for t in deckname.split(' ') if t]
    # 用已知的 C1 卡名做前綴比對
    for cn_ in C1_NAMES:
        if cn_ and deckname.startswith(cn_): return True
    return False
for label, rows in [('合併', E), ('分支', EB)]:
    a = [r for r in rows if has_c1(r['name'])]
    b = [r for r in rows if not has_c1(r['name'])]
    for tag, g in (('含C1新卡', a), ('不含新卡', b)):
        s = sum(r['share'] for r in g); w = sum(r['w'] for r in g); n = sum(r['n'] for r in g)
        awr = round((w + 12) / (n + 25) * 100, 2) if n else 0
        print(f'{label} {tag}: 份額 {s:.2f}% / AWR {awr:.2f}% / N={n}')

print()
print('### 分支口徑 Top 18（晚間）')
mbb = {r['slug']: r for r in MB}
for r in EB[:18]:
    o = mbb.get(r['slug'])
    extra = f"  | 早 {o['share']:.2f}%/{o['awr']:.2f}% Δ{r['share']-o['share']:+.2f}/{r['awr']-o['awr']:+.2f}" if o else '  | 新進榜'
    print(f"{zh(r['name'])[:34]:36} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4}{extra}")

print()
print('### 分支口徑 Top 早間（對照）')
for r in MB[:18]:
    print(f"{zh(r['name'])[:34]:36} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4}")
