import json

E = json.load(open('memory/ptcgp_meta_20261031e_c1_comb.json'))
M = json.load(open('memory/ptcgp_meta_20261031m_c1_comb.json'))   # 05:45 抓取
M2 = json.load(open('memory/ptcgp_meta_20261031_stdcomb.json'))   # 05:40 抓取(同一份)
mb = {r['slug']: r for r in M}

print('=== C1 合併口徑：份額 Top 20（20:05 抓取）===')
print(f"{'牌組':46} {'份額':>7} {'AWR':>7} {'N':>5}  {'早份額':>7} {'Δ份額':>7} {'早AWR':>7} {'ΔAWR':>7}")
for r in E[:20]:
    o = mb.get(r['slug'])
    if o:
        print(f"{r['name'][:44]:46} {r['share']:>6.2f}% {r['awr']:>6.2f}% {r['n']:>5}  {o['share']:>6.2f}% {r['share']-o['share']:>+6.2f} {o['awr']:>6.2f}% {r['awr']-o['awr']:>+6.2f}")
    else:
        print(f"{r['name'][:44]:46} {r['share']:>6.2f}% {r['awr']:>6.2f}% {r['n']:>5}  {'—':>7} {'新進榜':>7}")

print()
print('=== AWR Top 15（合併口徑，N>=40）===')
cand = [r for r in E if r['n'] >= 40]
cand.sort(key=lambda x: -x['awr'])
for r in cand[:15]:
    o = mb.get(r['slug'])
    da = f"{r['awr']-o['awr']:+.2f}" if o else '  新'
    ds = f"{r['share']-o['share']:+.2f}" if o else '  新'
    print(f"{r['name'][:44]:46} {r['share']:>6.2f}% {r['awr']:>6.2f}% {r['n']:>5}  Δ份額{ds} ΔAWR{da}")

print()
print('=== AWR Top 12（合併口徑，全樣本，含小樣本）===')
for r in sorted(E, key=lambda x: -x['awr'])[:12]:
    o = mb.get(r['slug'])
    da = f"{r['awr']-o['awr']:+.2f}" if o else '  新'
    print(f"{r['name'][:44]:46} {r['share']:>6.2f}% {r['awr']:>6.2f}% {r['n']:>5}  ΔAWR{da}")

print()
print('=== 份額下跌最多 Top 12 ===')
deltas = []
for r in E:
    o = mb.get(r['slug'])
    if o:
        deltas.append((r['share'] - o['share'], r, o))
for d, r, o in sorted(deltas, key=lambda x: (x[0], x[1]['name']))[:12]:
    print(f"{r['name'][:44]:46} {o['share']:>6.2f}% -> {r['share']:>6.2f}% ({d:+.2f})  AWR {o['awr']:.2f}->{r['awr']:.2f}  N={r['n']}")

print()
print('=== 份額上升最多 Top 12 ===')
for d, r, o in sorted(deltas, key=lambda x: (-x[0], x[1]['name']))[:12]:
    print(f"{r['name'][:44]:46} {o['share']:>6.2f}% -> {r['share']:>6.2f}% ({d:+.2f})  AWR {o['awr']:.2f}->{r['awr']:.2f}  N={r['n']}")

print()
print('=== 早間榜中消失的合併條目 ===')
en = {r['slug'] for r in E}
for r in M:
    if r['slug'] not in en:
        print(f"  {r['name'][:50]:52} 早 {r['share']:.2f}% AWR {r['awr']:.2f}% N={r['n']}")
