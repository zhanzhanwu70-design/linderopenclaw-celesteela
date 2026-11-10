import json, collections, sys, re
D=json.load(open('ptcgp_deck_dictionary.json'))
cn=D['card_names']; dn=D['deck_names']
cards=json.load(open('memory/ptcgp_cards_full.json'))
rev={}
for en,zh in cn.items():
    rev.setdefault(zh,en)
hp=collections.defaultdict(list)
for k,c in cards.items():
    if c.get('name') and isinstance(c.get('hp'),int) and c.get('hp')>0:
        hp[c['name']].append(c['hp'])

HP_OVERRIDE = {
    # B3 官方卡表 #081（tcgpocket.centropkmn.com）確認為 190HP；本地完整卡庫缺 B3 資料。
    '超級路卡利歐 ex': 190,
}

def find_hp(en, zh):
    if zh in HP_OVERRIDE: return HP_OVERRIDE[zh]
    if en in hp: return max(hp[en])
    if en and en.replace(' ex','') in hp: return max(hp[en.replace(' ex','')])
    norm = lambda s: re.sub(r'\s+', '', s)
    for cand_en, cand_zh in cn.items():
        if norm(cand_zh)==norm(zh) and cand_en in hp: return max(hp[cand_en])
    return None

def bucket(h):
    if h is None: return '未知'
    if h<=120: return '≤120HP'
    if h<=160: return '130-160HP'
    if h<=200: return '170-200HP'
    return '210+HP'

def run(path,label):
    rows=json.load(open(path))['rows']
    G=collections.defaultdict(lambda:[0.0,0,0]); miss=[]
    for r in rows:
        z=dn.get(r['name']) or cn.get(r['name']) or r['name']
        en=rev.get(z); h=find_hp(en,z)
        if h is None:
            miss.append((z,r['share'])); continue
        b=bucket(h); G[b][0]+=r['share']; G[b][1]+=r['w']; G[b][2]+=r['n']
    print(f'=== {label} HP 分桶（合併牌組 N>=30）===')
    out=[]
    for b,(s,w,n) in G.items():
        if b=='未知' or n<30: continue
        out.append((b,s,(w+12)/(n+25)*100,n))
    for b,s,a,n in sorted(out,key=lambda x:-x[2]):
        print(f'{b:12} 份額 {s:>6.2f}%  AWR {a:>6.2f}%  N={n}')
    if miss: print('  HP未知:', [(m[0],round(m[1],2)) for m in sorted(miss,key=lambda x:-x[1])[:6]])
    print()
    return G

for d,label in [('20261106','11-06'),('20261107','11-07'),('20261108','11-08'),('20261109','11-09')]:
    p=f'memory/ptcgp_meta_{d}_std_comb.json'
    if d=='20261106': p='memory/ptcgp_meta_20261106_std_comb_re.json'
    if d=='20261107': p='memory/ptcgp_meta_20261107_std_comb_re.json'
    if d=='20261108': p='memory/ptcgp_meta_20261108_std_comb_re.json'
    run(p,label)

print('### 個別牌組 HP 對照（合併口徑，份額前 24）')
rows=json.load(open('memory/ptcgp_meta_20261109_std_comb.json'))['rows']
for r in rows[:24]:
    z=dn.get(r['name']) or cn.get(r['name']) or r['name']
    en=rev.get(z); h=find_hp(en,z)
    print(f"{z[:26]:28} HP={str(h):>5}  份額 {r['share']:>5.2f}%  AWR {r['awr']:>6.2f}%  N={r['n']}")
