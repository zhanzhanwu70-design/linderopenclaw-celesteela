import json
Y={r['name']:r for r in json.load(open('memory/ptcgp_meta_20261026.json'))}
T={r['name']:r for r in json.load(open('memory/ptcgp_meta_20261027.json'))}
mv=[]
for n,r in T.items():
    o=Y.get(n)
    if not o: continue
    if r['n']>=250:
        mv.append((r['awr']-o['awr'],n,o['awr'],r['awr'],o['share'],r['share'],r['n']))
mv.sort()
print('=== DOWN (N>=250) ===')
for d,n,ya,ta,ys,ts,nn in mv[:12]:
    print(f'{n[:45]:47} {ys:>5.2f}->{ts:>5.2f}%  AWR {ya:>5.2f}->{ta:>5.2f} ({d:+.2f}) N={nn}')
print('=== UP (N>=250) ===')
for d,n,ya,ta,ys,ts,nn in mv[-12:][::-1]:
    print(f'{n[:45]:47} {ys:>5.2f}->{ts:>5.2f}%  AWR {ya:>5.2f}->{ta:>5.2f} ({d:+.2f}) N={nn}')
print('\n=== NEW entries (not in 10-26) ===')
for n,r in T.items():
    if n not in Y and r['n']>=30: print(f"{n[:50]:52} {r['share']:>5.2f}% {r['awr']:>5.2f}% N={r['n']}")
print('\n=== Top AWR among share>=0.5, N>=300 (top) ===')
c=[r for r in T.values() if r['share']>=0.5 and r['n']>=300]
c.sort(key=lambda x:-x['awr'])
for r in c[:18]: print(f"{r['name'][:45]:47} {r['share']:>5.2f}% {r['awr']:>5.2f}% N={r['n']}")
print('\n=== Worst ===')
for r in c[-10:]: print(f"{r['name'][:45]:47} {r['share']:>5.2f}% {r['awr']:>5.2f}% N={r['n']}")
