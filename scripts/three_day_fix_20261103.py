import json, collections

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']
def zh(n): return dn.get(n) or n

def agg_by_name(rows):
    out = {}
    for r in rows:
        k = r['name']
        if k not in out:
            out[k] = {'name': k, 'share': 0.0, 'w': 0, 'l': 0, 'd': 0, 'n': 0}
        o = out[k]
        o['share'] += r['share']; o['w'] += r['w']; o['l'] += r['l']; o['d'] += r['d']; o['n'] += r['n']
    for o in out.values():
        o['awr'] = round((o['w'] + 12) / (o['n'] + 25) * 100, 2) if o['n'] else 0
        o['share'] = round(o['share'], 4)
    return out

DAYS = [
    ('11-01', 'memory/ptcgp_meta_20261101_std_comb_re.json'),
    ('11-02', 'memory/ptcgp_meta_20261102_std_comb_re.json'),
    ('11-03', 'memory/ptcgp_meta_20261103_std_comb.json'),
]
names = ['Umbreon', 'Mega Greninja ex', 'Mega Charizard Y ex', 'Giratina ex', 'Suicune ex',
         'Mega Altaria ex', 'Mega Mewtwo X ex', 'Greninja ex', 'Pikachu ex', 'Hoopa ex',
         'Mega Manectric ex', 'Hydreigon', 'Alolan Exeggutor ex', 'Miraidon ex', 'Mega Dragonite ex',
         'Vespiquen ex', 'Magnezone', 'Lopunny']
data = {tag: json.load(open(f)) for tag, f in DAYS}
agg = {tag: agg_by_name(d['rows']) for tag, d in data.items()}

print(f"{'牌組':22} {'11-01':>18} {'11-02':>18} {'11-03':>18} {'Δ份額':>8} {'ΔAWR':>7}")
for n in names:
    cells = []
    for tag, _ in DAYS:
        r = agg[tag].get(n)
        cells.append(f"{r['share']:.2f}/{r['awr']:.2f}({r['n']})" if r else '-')
    a = agg['11-02'].get(n); b = agg['11-03'].get(n)
    ds = f"{b['share']-a['share']:+.2f}" if a and b else '-'
    da = f"{b['awr']-a['awr']:+.2f}" if a and b else '-'
    print(f"{zh(n)[:20]:22} {cells[0]:>18} {cells[1]:>18} {cells[2]:>18} {ds:>8} {da:>7}")

print('\n=== 合併口徑重複名合併後 Top 20（11-03） ===')
for r in sorted(agg['11-03'].values(), key=lambda x: -x['share'])[:20]:
    print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']}")
