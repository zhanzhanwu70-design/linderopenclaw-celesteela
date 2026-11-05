import json
D=json.load(open('ptcgp_deck_dictionary.json'))
dn=D['deck_names']; cn=D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n
T=json.load(open('memory/ptcgp_meta_20261104_std_comb.json'))
Y=json.load(open('memory/ptcgp_meta_20261103_std_comb_re.json'))
Y2=json.load(open('memory/ptcgp_meta_20261102_std_comb_re.json'))
E=T['rows']; p={r['slug']:r for r in Y['rows']}; p2={r['slug']:r for r in Y2['rows']}
print('### 合併口徑 Top 45（含三日）')
for i,r in enumerate(E[:45],1):
    o=p.get(r['slug']); o2=p2.get(r['slug'])
    s1=f"{o['share']:>6.2f}%/{o['awr']:>6.2f}" if o else '   NEW    '
    s2=f"{o2['share']:>6.2f}%/{o2['awr']:>6.2f}" if o2 else '   -     '
    print(f"{i:>2}. {zh(r['name'])[:30]:32} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']:>4} | 11-03 {s1} | 11-02 {s2}")
print()
print('### AWR 變動最大（合併，N>=100，兩日都有）')
mv=[]
for r in E:
    o=p.get(r['slug'])
    if o and r['n']>=100 and o['n']>=100:
        mv.append((r['awr']-o['awr'], r, o))
mv.sort(key=lambda x:-abs(x[0]))
for d,r,o in mv[:12]:
    print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {o['awr']:>6.2f}% -> {r['awr']:>6.2f}%  Δ{d:+.2f}pt  N={r['n']}")
print('  --- 跌幅 ---')
for d,r,o in mv[-8:]:
    print(f"{zh(r['name'])[:30]:32} {r['share']:>6.2f}% {o['awr']:>6.2f}% -> {r['awr']:>6.2f}%  Δ{d:+.2f}pt  N={r['n']}")
print()
print('### 份額變動最大（合併）')
mv2=[]
for r in E:
    o=p.get(r['slug'])
    if o: mv2.append((r['share']-o['share'], r, o))
mv2.sort(key=lambda x:-x[0])
for d,r,o in mv2[:8]:
    print(f"↑ {zh(r['name'])[:30]:32} {o['share']:>6.2f}% -> {r['share']:>6.2f}%  Δ{d:+.2f}pt  AWR {o['awr']:.2f}->{r['awr']:.2f}")
for d,r,o in mv2[-8:]:
    print(f"↓ {zh(r['name'])[:30]:32} {o['share']:>6.2f}% -> {r['share']:>6.2f}%  Δ{d:+.2f}pt  AWR {o['awr']:.2f}->{r['awr']:.2f}")
