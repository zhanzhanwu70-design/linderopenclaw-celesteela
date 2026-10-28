import json
def load(p,n=60):
    rs=json.load(open(p)); rs.sort(key=lambda x:-x['share']); return rs[:n]
for p,lab in [('memory/ptcgp_meta_20261026_comb.json','10-26'),('memory/ptcgp_meta_20261027_comb.json','10-27')]:
    rs=load(p)
    print(f'== {lab} combine ==')
    for r in rs[:30]:
        print(f"{r['name'][:45]:47} {r['share']:>6.2f}% {r['awr']:>6.2f}% N={r['n']}")
