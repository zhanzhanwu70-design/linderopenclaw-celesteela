#!/usr/bin/env python3
"""2026-11-23 族群 AWR、新舊卡差距、HP 分桶、N 佔比與份額噪音量化。"""
import collections
import json
import re
import statistics

D = json.load(open('ptcgp_deck_dictionary.json', encoding='utf-8'))
cn = D['card_names']
dn = D['deck_names']
cards = json.load(open('memory/ptcgp_cards_full.json', encoding='utf-8'))


def zh(n):
    return dn.get(n) or cn.get(n) or n


def agg(rows):
    out = collections.defaultdict(lambda: {'share': 0.0, 'w': 0, 'l': 0, 'd': 0, 'n': 0, 'decks': 0})
    for r in rows:
        a = out[r['name']]
        for k in ('share', 'w', 'l', 'd', 'n', 'decks'):
            a[k] += r[k]
    res = []
    for name, a in out.items():
        a = dict(a)
        a['name'] = name
        a['awr'] = (a['w'] + 12) / (a['n'] + 25) * 100 if a['n'] else 0.0
        a['raw_wr'] = a['w'] / a['n'] * 100 if a['n'] else 0.0
        res.append(a)
    res.sort(key=lambda r: -r['share'])
    return res


SUF = {'20261124': '.json', '20261123': '.json', '20261122': '.json', '20261121': '_re2.json',
       '20261120': '_re2.json'}
DAYS = ['20261120', '20261121', '20261122', '20261123', '20261124']
LAB = {d: d[4:6] + '-' + d[6:8] for d in DAYS}

DATA = {}
for d in DAYS:
    j = json.load(open(f'memory/ptcgp_meta_{d}_std_comb{SUF[d]}', encoding='utf-8'))
    DATA[d] = (j['header'], agg(j['rows']))


def grp(n):
    N = n.lower()
    if "team rocket" in N or "slowking" in N or "raticate" in N or "weezing" in N:
        return '火箭隊系'
    if any(k in N for k in ["greninja", "suicune", "baxcalibur", "milotic", "gyarados", "sharpedo", "vaporeon", "wailord", "swanna", "pyukumuku", "wishiwashi", "palafin", "blissey", "chien-pao", "blastoise", "whiscash", "clodsire", "furfret"]):
        return '水系'
    if any(k in N for k in ["magnezone", "miraidon", "dedenne", "heliolisk", "manectric", "zeraora", "rotom", "jolteon", "bellibolt", "electrode", "zapdos", "meowstic", "raikou", "indeedee", "pikachu", "pachirisu", "pawmot", "oricorio", "dialga", "palkia", "articuno", "meltan", "morpeko", "togekiss", "electivire"]):
        return '電系'
    if any(k in N for k in ["umbreon", "espeon", "leafeon", "eevee", "glaceon", "sylveon", "flareon", "meowth"]):
        return '超能系'
    if any(k in N for k in ["charizard", "moltres", "entei", "typhlosion", "incineroar", "landorus", "heatmor", "skeledirge", "blaziken", "fuecoco", "gardevoir", "mimikyu", "meloetta", "alcremie", "tinkaton", "sandslash", "simisear", "charcadet", "centiskorch", "scovillain", "tsareena", "decidueye", "meowscarada", "chesnaught", "mewtwo", "mew", "miltank", "tauros", "audino", "carbink", "wobbbufett"]):
        return '火/超能系'
    if any(k in N for k in ["altaria", "igglybuff", "chingling", "happiny", "duraludon", "dragonite", "salamence", "flygon", "dragonair", "garchomp", "goomy", "haxorus", "goodra", "drampa", "latios", "noivern", "archaludon", "bagon", "shelgon", "rayquaza", "hydreigon", "tyranitar", "giratina", "zoroark", "absol", "darkrai", "sableye", "banette", "nihilego", "gengar", "mismagius", "hatterene", "hoopa", "grimmsnarl", "guzzlord", "dragalge"]):
        return '龍/惡系'
    if any(k in N for k in ["lucario", "hitmon", "medicham", "gallade", "machamp", "annihilape", "primeape", "infernape", "hitmontop", "aegislash", "gholdengo", "excadrill", "mienfoo", "toxicroak", "scrafty", "sceptile", "buzzwole", "pheromosa", "venomoth", "beautifly", "dustox", "beedrill", "ledian", "volcarona", "exeggutor", "venusaur", "abomasnow", "torterra", "lilligant", "serperior", "celebi", "lurantis", "bonsly", "cherubi", "chikorita", "treecko", "scizor", "revavroom", "ribombee", "dragapult", "iron", "steelix", "skarmory", "mawile"]):
        return '格鬥/草/鋼系'
    if any(k in N for k in ["pidgeot", "swellow", "talonflame", "staraptor", "farfetch", "rufflet", "fletchling"]):
        return '飛行系'
    if any(k in N for k in ["azumarill", "lopunny", "raboot", "pawmot", "wigglytuff", "clefairy", "clefable", "tinkaton", "sylveon", "miltank", "tauros"]):
        return '一般/妖精系'
    return '其他'


print('### 族群 AWR（合併口徑）')
G = {}
for d in DAYS:
    _, rows = DATA[d]
    gg = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rows:
        g = grp(r['name'])
        gg[g][0] += r['share']
        gg[g][1] += r['w']
        gg[g][2] += r['n']
    G[d] = {g: {'share': round(s, 4), 'awr': round((w + 12) / (t + 25) * 100, 4) if t else 0, 'n': t}
            for g, (s, w, t) in gg.items()}
names = sorted({g for d in DAYS for g in G[d]}, key=lambda g: -G['20261124'][g]['share'])
for g in names:
    cells = [f"{G[d].get(g, {}).get('share', 0):.4f}%/{G[d].get(g, {}).get('awr', 0):.4f}%" for d in DAYS]
    print(f'{g:14} ' + '  '.join(f'{c:>19}' for c in cells))

print('\n### 新舊卡差距')
C1N = set(c.get('name') for k, c in cards.items() if k.startswith('C1_') and c.get('name'))


def has_c1(nm):
    n = nm.replace('’', "'")
    for c in C1N:
        c2 = c.replace('’', "'")
        if n.startswith(c2) or n.startswith(c2.replace(' ex', 'ex')):
            return True
    return False


for d in DAYS:
    _, rows = DATA[d]
    a = [r for r in rows if has_c1(r['name'])]
    b = [r for r in rows if not has_c1(r['name'])]

    def stat(g):
        s = sum(r['share'] for r in g)
        w = sum(r['w'] for r in g)
        n = sum(r['n'] for r in g)
        return s, (w + 12) / (n + 25) * 100 if n else 0, n
    sa, aa, na = stat(a)
    sb, ab, nb = stat(b)
    print(f"{LAB[d]}: 含新卡 {sa:.4f}%/{aa:.4f}% N={na} | 不含 {sb:.4f}%/{ab:.4f}% N={nb} | 差距 {ab-aa:.4f}pt")

print('\n### N 佔比（合併口徑）')
NAMES = ['Mega Altaria ex', 'Hoopa ex', 'Magnezone', 'Mega Greninja ex', 'Umbreon',
         'Mega Charizard Y ex', 'Suicune ex', 'Vespiquen ex', 'Mega Lucario ex', 'Giratina ex',
         'Mega Mewtwo X ex', 'Mega Manectric ex', 'Chien Pao ex', 'Mega Sceptile ex',
         'Mega Skarmory ex', 'Hydreigon', 'Greninja', 'Greninja ex', 'Arceus ex',
         'Mega Dragonite ex', 'Absol ex', 'Pidgeot ex', 'Alolan Exeggutor ex', 'Dragonair',
         'Mega Bouffalant ex', 'Lopunny', 'Pikachu ex', 'Miraidon ex', 'Rampardos ex',
         'Zapdos ex', 'Eevee', 'Latias ex', 'Sylveon', 'Dedenne ex', 'Mega Mewtwo Y ex',
         'Butterfree', 'Entei ex', 'Milotic ex']
TOT = {d: sum(r['n'] for r in DATA[d][1]) for d in DAYS}
for n in NAMES:
    cells = []
    for d in DAYS:
        rows = DATA[d][1]
        r = [x for x in rows if x['name'] == n]
        if r:
            cells.append(f"{r[0]['n']/TOT[d]*100:6.4f}%/{r[0]['share']:7.4f}%/{r[0]['awr']:7.4f}%")
        else:
            cells.append('   --      ')
    print(f"{n:22} | " + " | ".join(cells))

print('\n### 今日份額變動分布（合併口徑，同名加總，N>=200）')
rt = DATA['20261124'][1]
ry = DATA['20261123'][1]
ymap = {r['name']: r for r in ry}
deltas = [(r['share'] - ymap[r['name']]['share'], r['name'], r['share'], r['n'])
          for r in rt if r['name'] in ymap and r['n'] >= 200]
deltas.sort()
vals = [d[0] for d in deltas]
print(f"  可比牌組數 N>=200: {len(vals)}  最大上升 {vals[-1]:+.4f}pt  最大下降 {vals[0]:+.4f}pt  中位 {statistics.median(vals):+.4f}pt  平均 {statistics.mean(vals):+.4f}pt  標準差 {statistics.pstdev(vals):.4f}pt")
print('  上升前 10：')
for d in deltas[-10:][::-1]:
    print(f"    {d[1][:36]:38} {d[0]:+.4f}pt  份額 {d[2]:.4f}% N={d[3]}")
print('  下降前 10：')
for d in deltas[:10]:
    print(f"    {d[1][:36]:38} {d[0]:+.4f}pt  份額 {d[2]:.4f}% N={d[3]}")

print('\n### HP 分桶（合併口徑）')
rev = {}
for en, z in cn.items():
    rev.setdefault(z, en)
hp = collections.defaultdict(list)
for k, c in cards.items():
    if c.get('name') and isinstance(c.get('hp'), int) and c.get('hp') > 0:
        hp[c['name']].append(c['hp'])
HP_OVERRIDE = {'超級路卡利歐 ex': 190}


def find_hp(en, z):
    if z in HP_OVERRIDE:
        return HP_OVERRIDE[z]
    if en in hp:
        return max(hp[en])
    if en and en.replace(' ex', '') in hp:
        return max(hp[en.replace(' ex', '')])
    norm = lambda s: re.sub(r'\s+', '', s)
    for cand_en, cand_zh in cn.items():
        if norm(cand_zh) == norm(z) and cand_en in hp:
            return max(hp[cand_en])
    return None


def bucket(h):
    if h is None:
        return '未知'
    if h <= 120:
        return '≤120HP'
    if h <= 160:
        return '130-160HP'
    if h <= 200:
        return '170-200HP'
    return '210+HP'


for d in DAYS:
    rows = DATA[d][1]
    G2 = collections.defaultdict(lambda: [0.0, 0, 0])
    miss = []
    for r in rows:
        z = zh(r['name'])
        h = find_hp(rev.get(z), z)
        if h is None:
            miss.append((z, r['share']))
            continue
        b = bucket(h)
        G2[b][0] += r['share']
        G2[b][1] += r['w']
        G2[b][2] += r['n']
    out = [(b, s, (w + 12) / (n + 25) * 100, n) for b, (s, w, n) in G2.items() if b != '未知' and n >= 30]
    print(f'  {LAB[d]}: ' + ' | '.join(f'{b} {s:.2f}%/{a:.2f}%(N={n})' for b, s, a, n in sorted(out, key=lambda x: -x[2])))
    if miss:
        print('    HP未知:', [(m[0], round(m[1], 2)) for m in sorted(miss, key=lambda x: -x[1])[:5]])

print('\n### 個別牌組 HP 對照（合併口徑，份額前 24）')
for r in DATA['20261124'][1][:24]:
    z = zh(r['name'])
    h = find_hp(rev.get(z), z)
    print(f"{z[:28]:30} HP={str(h):>5}  份額 {r['share']:>6.2f}%  AWR {r['awr']:>6.2f}%  N={r['n']}")

print('\n### 環境總副牌 / 吸收濃度')
TOTD = {d: sum(r['decks'] for r in DATA[d][1]) for d in DAYS}
for i, d in enumerate(DAYS):
    prev = DAYS[i - 1] if i else None
    delta = TOTD[d] - TOTD[prev] if prev else 0
    print(f'  {LAB[d]}: 總副牌 {TOTD[d]}  ΔT {delta:+d}')
print('  今日吸收副牌前 12（組）與占全環境新增比例：')
prevd = {r['name']: r['decks'] for r in DATA['20261123'][1]}
deltaT = TOTD['20261123'] - TOTD['20261122']
inc = sorted(((r['name'], r['decks'] - prevd.get(r['name'], 0)) for r in DATA['20261124'][1]), key=lambda x: -x[1])
for n, d in inc[:12]:
    print(f"    {zh(n)[:24]:26} {d:+5d} 副  吸收濃度 {d/deltaT*100:5.2f}%")
