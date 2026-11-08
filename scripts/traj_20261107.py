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
 '20261104':'memory/ptcgp_meta_20261104_std_comb_re.json',
 '20261105':'memory/ptcgp_meta_20261105_std_comb_re.json',
 '20261106':'memory/ptcgp_meta_20261106_std_comb.json',
 '20261107':'memory/ptcgp_meta_20261107_std_comb.json',
}
days = list(FILES)
comb = {d: agg(FILES[d]) for d in days}

names = ['超級噴火龍Yex','月亮伊布','超級甲賀忍蛙ex','水君ex','超級七夕青鳥ex','胡帕ex','騎拉帝納ex','甲賀忍蛙ex','超級雷電獸ex','超級超夢Xex','皮卡丘ex','蜂女王ex','超級路卡利歐 ex','三首惡龍','超級蜥蜴王ex','阿羅拉 椰蛋樹ex','密勒頓ex','自爆磁怪','超級班基拉斯ex','超級快龍ex','帕底亞 土王','雷公ex','長耳兔','瑪力露麗','哈克龍','月亮伊布ex','超級火焰雞ex']
print('### 合併口徑 四日軌跡（份額 / AWR / N）')
print('牌組'.ljust(20) + '  '.join(f'{d[4:]:>22}' for d in days))
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
