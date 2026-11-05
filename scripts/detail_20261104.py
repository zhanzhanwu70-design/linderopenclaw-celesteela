import json, collections, re

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n

def load(p): return json.load(open(p))

def fam(rows, keys):
    """所有 name 含任一 key 的分支加總（份額加總、勝場加總、N 加總）"""
    out=[]
    for r in rows:
        if any(k.lower() in r['name'].lower() for k in keys):
            out.append(r)
    s=sum(r['share'] for r in out); w=sum(r['w'] for r in out); n=sum(r['n'] for r in out)
    return {'share':round(s,2),'awr':round((w+12)/(n+25)*100,2) if n else 0,'n':n,'rows':out}

days = {
 '11-02': ('memory/ptcgp_meta_20261102_std_comb_re.json','memory/ptcgp_meta_20261102_std_re.json'),
 '11-03': ('memory/ptcgp_meta_20261103_std_comb_re.json','memory/ptcgp_meta_20261103_std_re.json'),
 '11-04': ('memory/ptcgp_meta_20261104_std_comb.json','memory/ptcgp_meta_20261104_std.json'),
}

FAMS = {
 '忍蛙系':['greninja'],
 '月亮伊布系':['umbreon'],
 '七夕青鳥系':['altaria'],
 '水君系':['suicune'],
 '胡帕系':['hoopa'],
 '雷電獸系':['raikou'],
 '三首惡龍':['hydreigon'],
 '龍/惡系':['giratina','hydreigon','dragonite','salamence','flygon','haaxorus','goodra','drampa','latios','noivern','archaludon','bagon','shelgon','rayquaza','tyranitar','zoroark','absol','darkrai','sableye','banette','nihilego','gengar','mismagius','hatterene','grimmsnarl','guzzlord','dragalge'],
 '水系':['greninja','suicune','baxcalibur','milotic','gyarados','sharpedo','vaporeon','wailord','swanna','pyukumuku','wishiwashi','palafin','blissey','chien-pao','blastoise','whiscash','clodsire','furfret'],
 '電系':['magnezone','miraidon','dedenne','heliolisk','manectric','zeraora','rotom','jolteon','bellibolt','electrode','zapdos','meowstic','raikou','indeedee','pikachu','pachirisu','pawmot','oricorio','dialga','palkia','articuno','meltan','morpeko','togekiss'],
 '超能系':['umbreon','espeon','leafeon','eevee','glaceon','sylveon','flareon','meowth'],
 '火/超能系':['charizard','moltres','entei','typhlosion','incineroar','landorus','heatmor','skeledirge','blaziken','fuecoco','gardevoir','mimikyu','meloetta','alcremie','tinkaton','sandslash','simisear','charcadet','centiskorch','scovillain','tsareena','decidueye','meowscarada','chesnaught','mewtwo','mew','miltank','tauros','audino','carbink','wobbbufett'],
 '格鬥/草/鋼系':['lucario','hitmon','medicham','gallade','machamp','annihilape','primeape','infernape','hitmontop','aegislash','gholdengo','excadrill','mienfoo','toxicroak','scrafty','sceptile','buzzwole','pheromosa','venomoth','beautifly','dustox','beedrill','ledian','volcarona','exeggutor','venusaur','abomasnow','torterra','lilligant','serperior','celebi','lurantis','bonsly','cherubi','chikorita','treecko','scizor','revavroom','ribombee','bellibolt','dragapult','iron','steelix','skarmory','mawile'],
}

print('### 族群三日趨勢（分支口徑）')
for name, keys in FAMS.items():
    line=[]
    for d,(cp,bp) in days.items():
        rows = load(bp)['rows']
        f = fam(rows, keys)
        line.append(f"{d} {f['share']:>6.2f}%/{f['awr']:>6.2f}%")
    print(f"{name:14} " + ' | '.join(line))

print()
print('### 族群三日趨勢（合併口徑）')
for name, keys in FAMS.items():
    line=[]
    for d,(cp,bp) in days.items():
        rows = load(cp)['rows']
        f = fam(rows, keys)
        line.append(f"{d} {f['share']:>6.2f}%/{f['awr']:>6.2f}%")
    print(f"{name:14} " + ' | '.join(line))

print()
print('### 11-04 合併口徑 全表（份額>=0.5%）')
rows=load('memory/ptcgp_meta_20261104_std_comb.json')['rows']
for r in rows:
    if r['share']>=0.5:
        print(f"{zh(r['name'])[:34]:36} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4}  slug={r['slug']}")
