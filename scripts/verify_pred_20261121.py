#!/usr/bin/env python3
"""2026-11-21 PRED_20261120 正式驗證 + 新預測動能計算。"""
import collections, json

def agg(path):
    out = collections.defaultdict(lambda: {'share':0.0,'w':0,'l':0,'d':0,'n':0,'decks':0})
    for r in json.load(open(path, encoding='utf-8'))['rows']:
        a = out[r['name']]
        for k in ('share','w','l','d','n','decks'): a[k] += r[k]
    res = []
    for n,a in out.items():
        a=dict(a); a['name']=n
        a['awr'] = (a['w']+12)/(a['n']+25)*100 if a['n'] else 0
        a['raw'] = a['w']/a['n']*100 if a['n'] else 0
        res.append(a)
    res.sort(key=lambda r:-r['share'])
    return res

DAYS = ['20261118','20261119','20261120','20261121']
D = {}
for d in DAYS:
    suf = '.json' if d=='20261121' else '_re.json'
    D[d] = agg(f'memory/ptcgp_meta_{d}_std_comb{suf}')

def get(day, name):
    for r in D[day]:
        if r['name']==name: return r
    return None

print('=== PRED_20261120 正式驗證（檢查日 2026-11-21）===')
A = get('20261121','Mega Altaria ex'); Ay = get('20261120','Mega Altaria ex')
print(f"A 超級七夕青鳥ex 合併份額 >=9.85%: 今 {A['share']:.4f}% (昨 {Ay['share']:.4f}%) raw {A['share']:.4f} >= 9.85 -> {'HIT' if A['share']>=9.85 else 'MISS'}")
B = get('20261121','Magnezone'); By = get('20261120','Magnezone')
print(f"B 自爆磁怪 合併份額 >=4.42%: 今 {B['share']:.4f}% (昨 {By['share']:.4f}%) raw {B['share']:.4f} >= 4.42 -> {'HIT' if B['share']>=4.42 else 'MISS'}")
C = get('20261121','Hoopa ex'); Cy = get('20261120','Hoopa ex')
print(f"C 胡帕ex 合併AWR <53.00%: 今 {C['awr']:.4f}% (昨 {Cy['awr']:.4f}%) raw {C['w']}/{C['n']} -> {'HIT' if C['awr']<53.0 else 'MISS'}")

print()
print('=== 四日趨勢表（合併同名加總）===')
KEYS = ['Mega Charizard Y ex','Mega Altaria ex','Umbreon','Hoopa ex','Suicune ex',
        'Mega Greninja ex','Mega Lucario ex','Magnezone','Mega Mewtwo X ex','Vespiquen ex',
        'Giratina ex','Mega Manectric ex','Greninja ex','Chien Pao ex','Mega Sceptile ex',
        'Hydreigon','Pikachu ex','Mega Skarmory ex','Lopunny','Mega Dragonite ex',
        'Greninja','Alolan Exeggutor ex','Dragonair','Miraidon ex','Lopunny','Dondozo ex',
        'Mega Mewtwo Y ex','Arceus ex','Absol ex','Mega Bouffalant ex','Zapdos ex','Latias ex']
for n in KEYS:
    vals = [get(d,n) for d in DAYS]
    if not any(vals): continue
    def f(r): return f"{r['share']:7.4f}%/{r['awr']:8.4f}%" if r else '  --  /  --   '
    mom = []
    for i in range(1,4):
        a,b = vals[i-1], vals[i]
        mom.append(f"{(b['share']-a['share']):+.4f}" if a and b else '  --  ')
    print(f"{n[:26]:28} " + " | ".join(f(v) for v in vals) + " | 動能 " + " ".join(mom))

print()
print('=== 咚咚鼠ex / 巴大蝶 / 其他 movers ===')
for n in ['Dondozo ex','Mega Gardevoir ex','Butterfree','Mega Blaziken ex','Absol ex','Bisharp ex','Arceus ex']:
    for d in DAYS:
        r = get(d,n)
        if r: print(f"  {n:22} {d[4:6]}-{d[6:8]} {r['share']:7.4f}%/{r['awr']:8.4f}% N={r['n']}")
    print()
