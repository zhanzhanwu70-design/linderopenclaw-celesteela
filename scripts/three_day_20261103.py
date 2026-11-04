import json, collections

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']
def zh(n): return dn.get(n) or n

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

cards = json.load(open('memory/ptcgp_cards_full.json'))
C1N = set(c.get('name') for k, c in cards.items() if k.startswith('C1_') and c.get('name'))
def has_c1(nm):
    n = nm.replace("’", "'")
    for c in C1N:
        c2 = c.replace("’", "'")
        if n.startswith(c2) or n.startswith(c2.replace(' ex', 'ex')): return True
    return False

DAYS = [
    ('11-01', 'memory/ptcgp_meta_20261101_std_comb_re.json'),
    ('11-02', 'memory/ptcgp_meta_20261102_std_comb_re.json'),
    ('11-03', 'memory/ptcgp_meta_20261103_std_comb.json'),
]
data = {}
for tag, f in DAYS:
    d = json.load(open(f)); data[tag] = d
    print(f"{tag} header={d['header']}")

print('\n=== 三日族群（合併口徑） ===')
for tag, d in data.items():
    G = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in d['rows']:
        g = grp(r['name']); G[g][0] += r['share']; G[g][1] += r['w']; G[g][2] += r['n']
    line = []
    for g, (s, w, t) in sorted(G.items(), key=lambda x: -x[1][0]):
        line.append(f"{g} {s:.2f}%/{(w+12)/(t+25)*100:.2f}%")
    print(tag, ' | '.join(line))

print('\n=== 三日 新舊卡 AWR 差距（合併口徑） ===')
for tag, d in data.items():
    a = [r for r in d['rows'] if has_c1(r['name'])]
    b = [r for r in d['rows'] if not has_c1(r['name'])]
    def agg(g):
        s = sum(r['share'] for r in g); w = sum(r['w'] for r in g); n = sum(r['n'] for r in g)
        return s, (w + 12) / (n + 25) * 100, n
    sa, awa, na = agg(a); sb, awb, nb = agg(b)
    print(f"{tag}: 含新卡 {sa:.2f}%/{awa:.2f}% (N={na})  不含新卡 {sb:.2f}%/{awb:.2f}% (N={nb})  差距 {awb-awa:+.2f}pt")

print('\n=== 三日 主要牌組變化（合併口徑） ===')
m = {tag: {r['name']: r for r in d['rows']} for tag, d in data.items()}
names = ['Umbreon', 'Mega Greninja ex', 'Mega Charizard Y ex', 'Giratina ex', 'Suicune ex',
         'Mega Altaria ex', 'Mega Mewtwo X ex', 'Greninja ex', 'Pikachu ex', 'Hoopa ex',
         'Mega Manectric ex', 'Hydreigon', 'Alolan Exeggutor ex', 'Miraidon ex', 'Mega Dragonite ex']
print(f"{'牌組':22} {'11-01':>16} {'11-02':>16} {'11-03':>16}")
for n in names:
    cells = []
    for tag, _ in DAYS:
        r = m[tag].get(n)
        cells.append(f"{r['share']:.2f}/{r['awr']:.2f}" if r else '-')
    print(f"{zh(n)[:20]:22} {cells[0]:>16} {cells[1]:>16} {cells[2]:>16}")

print('\n=== 三日 前五份額變化 ===')
for tag, d in data.items():
    top = sorted(d['rows'], key=lambda r: -r['share'])[:5]
    print(tag, ' | '.join(f"{zh(r['name'])} {r['share']:.2f}%/{r['awr']:.2f}%" for r in top))

print('\n=== 三日 AWR 前五（N>=100） ===')
for tag, d in data.items():
    top = sorted([r for r in d['rows'] if r['n'] >= 100], key=lambda r: -r['awr'])[:5]
    print(tag, ' | '.join(f"{zh(r['name'])} {r['awr']:.2f}%({r['share']:.2f}%)" for r in top))
