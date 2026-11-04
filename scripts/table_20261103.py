import json

def load(p):
    return json.load(open(p))['rows'], json.load(open(p))['header']

r3, h3 = load('memory/ptcgp_meta_20261103_std_comb.json')
r2, h2 = load('memory/ptcgp_meta_20261102_std_comb_re.json')

print('=== 11-03 combined 份額前 15 ===')
for x in sorted(r3, key=lambda z: -z['share'])[:15]:
    print(f"{x['name'][:58]:60} {x['share']:>6.2f}%  AWR {x['awr']:>6.2f}%  raw {x['raw_wr']:>6.2f}%  N={x['n']:>5}  {x['w']}-{x['l']}-{x['d']}")

print()
print('=== 11-03 combined AWR 前 15 (N>=80) ===')
for x in sorted([z for z in r3 if z['n'] >= 80], key=lambda z: -z['awr'])[:15]:
    print(f"{x['name'][:58]:60} {x['share']:>6.2f}%  AWR {x['awr']:>6.2f}%  raw {x['raw_wr']:>6.2f}%  N={x['n']:>5}")

print()
print('=== 對比 11-02（份額前 15） ===')
for x in sorted(r2, key=lambda z: -z['share'])[:15]:
    print(f"{x['name'][:58]:60} {x['share']:>6.2f}%  AWR {x['awr']:>6.2f}%  N={x['n']:>5}")

m3 = {x['name']: x for x in r3}
m2 = {x['name']: x for x in r2}
print()
print('=== 合併份額變化（11-03 vs 11-02, 兩邊都有的） ===')
for n in sorted(set(m3) & set(m2), key=lambda n: -abs(m3[n]['share'] - m2[n]['share']))[:30]:
    a, b = m2[n], m3[n]
    print(f"{n[:58]:60} {a['share']:>6.2f}% -> {b['share']:>6.2f}% ({b['share']-a['share']:+.2f}pt)  AWR {a['awr']:>6.2f} -> {b['awr']:>6.2f} ({b['awr']-a['awr']:+.2f}pt)  N {a['n']}->{b['n']}")

print()
print('=== 11-03 新進榜（不在 11-02 合併榜） ===')
for n in sorted(set(m3) - set(m2), key=lambda n: -m3[n]['share'])[:20]:
    x = m3[n]
    print(f"{n[:58]:60} {x['share']:>6.2f}%  AWR {x['awr']:>6.2f}%  N={x['n']}")
