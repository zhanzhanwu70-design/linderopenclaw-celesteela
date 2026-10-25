import json
Y=json.load(open('memory/mu_matrix_20261024.json')); T=json.load(open('memory/mu_matrix_20261025.json'))
names=sorted(T.keys(), key=lambda n: -max(v[0] for v in T[n].values()))
def g(M,a,b):
    v=M.get(a,{}).get(b)
    return v
print('主體 | 對手 | 今日勝率 | N | 昨日勝率 | Δ')
rows=[]
for a in names:
    for b,(w,n) in sorted(T[a].items(), key=lambda x:-x[1][0]):
        if a==b: continue
        if n<25: continue
        yv=g(Y,a,b); y=f"{yv[0]:.1f}({yv[1]})" if yv else '·'
        d=f"{w-yv[0]:+.1f}" if yv else '·'
        rows.append((a,b,w,n,y,d))
for r in rows: print(f'{r[0][:26]:28} {r[1][:24]:26} {r[2]:>5.1f} {r[3]:>5}  {r[4]:>10} {r[5]:>6}')
