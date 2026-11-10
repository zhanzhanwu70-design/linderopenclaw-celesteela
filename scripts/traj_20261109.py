import json, collections
D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n

def agg(path):
    G = collections.defaultdict(lambda: {'share':0.0,'w':0,'n':0,'awr':0})
    for r in json.load(open(path))['rows']:
        k = zh(r['name'])
        G[k]['share'] += r['share']; G[k]['w'] += r['w']; G[k]['n'] += r['n']
    for k, v in G.items():
        v['awr'] = round((v['w']+12)/(v['n']+25)*100, 2) if v['n'] else 0
    return G

FILES = {
 '11-06':'memory/ptcgp_meta_20261106_std_comb_re.json',
 '11-07':'memory/ptcgp_meta_20261107_std_comb_re.json',
 '11-08':'memory/ptcgp_meta_20261108_std_comb_re.json',
 '11-09':'memory/ptcgp_meta_20261109_std_comb.json',
}
days = list(FILES)
comb = {d: agg(FILES[d]) for d in days}

names = ['超級噴火龍Yex','月亮伊布','超級甲賀忍蛙ex','水君ex','超級七夕青鳥ex','胡帕ex','騎拉帝納ex','甲賀忍蛙ex','超級雷電獸ex','超級超夢Xex','蜂女王ex','超級路卡利歐 ex','三首惡龍','自爆磁怪','阿羅拉 椰蛋樹ex','密勒頓ex','超級班基拉斯ex','超級快龍ex','帕底亞 土王','雷公ex','長耳兔','瑪力露麗','哈克龍','超級蜥蜴王ex','皮卡丘ex','咚咚鼠ex','大比鳥']
print('### 合併口徑 四日軌跡（份額 / AWR / N）')
print('牌組'.ljust(20) + '  '.join(f'{d:>22}' for d in days))
for nm in names:
    row = []
    for d in days:
        r = comb[d].get(nm)
        row.append(f"{r['share']:.2f}/{r['awr']:.2f}/{r['n']}" if r else "  --  ")
    print(f'{nm[:18]:20} ' + '  '.join(f'{x:>22}' for x in row))

print()
print('### 全環境加權 AWR（合併口徑）')
for d in days:
    rows = json.load(open(FILES[d]))['rows']
    w = sum(r['w'] for r in rows); n = sum(r['n'] for r in rows)
    print(f"{d}: {(w+12)/(n+25)*100:.2f}%  N={n}")

print()
print('### 合併口徑 份額 / AWR 變動幅度前 15（vs 11-08）')
p = comb['11-08']; c = comb['11-09']
moves=[]
for k,v in c.items():
    o=p.get(k)
    if o and o['n']>=100 and v['n']>=100:
        moves.append((v['share']-o['share'], v['awr']-o['awr'], k, v, o))
for ds,da,k,v,o in sorted(moves, key=lambda x:-abs(x[0]))[:15]:
    print(f"{k[:22]:24} 份額 {o['share']:>5.2f}->{v['share']:>5.2f} ({ds:+.2f})  AWR {o['awr']:>5.2f}->{v['awr']:>5.2f} ({da:+.2f}) N={v['n']}")
print()
print('### AWR 變動前 12（份額 >=1.0%，N>=150）')
moves2=[(da,ds,k,v,o) for ds,da,k,v,o in moves if v['share']>=1.0 and v['n']>=150]
for da,ds,k,v,o in sorted(moves2, key=lambda x:-x[0])[:12]:
    print(f"{k[:22]:24} AWR {o['awr']:>5.2f}->{v['awr']:>5.2f} ({da:+.2f})  份額 {o['share']:>5.2f}->{v['share']:>5.2f} ({ds:+.2f}) N={v['n']}")
