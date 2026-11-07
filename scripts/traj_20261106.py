import json, collections

D = json.load(open('ptcgp_deck_dictionary.json'))
dn = D['deck_names']; cn = D['card_names']
def zh(n): return dn.get(n) or cn.get(n) or n

def agg(path):
    """依牌組名合併同名列（同名不同 set）"""
    G = collections.defaultdict(lambda: {'share':0.0,'w':0,'n':0,'awr':0})
    for r in json.load(open(path))['rows']:
        k = zh(r['name'])
        G[k]['share'] += r['share']; G[k]['w'] += r['w']; G[k]['n'] += r['n']
    for k, v in G.items():
        v['awr'] = round((v['w']+12)/(v['n']+25)*100, 2) if v['n'] else 0
    return G

days = ['20261103','20261104','20261105','20261106']
comb = {d: agg(f'memory/ptcgp_meta_{d}_std_comb_re.json') for d in days[:3]}
comb['20261106'] = agg('memory/ptcgp_meta_20261106_std_comb.json')

names = ['月亮伊布','超級甲賀忍蛙ex','超級噴火龍Yex','水君ex','超級七夕青鳥ex','胡帕ex','騎拉帝納ex','甲賀忍蛙ex','超級超夢Xex','超級雷電獸ex','皮卡丘ex','三首惡龍','超級路卡利歐 ex','阿羅拉 椰蛋樹ex','蜂女王ex','超級蜥蜴王ex','密勒頓ex','自爆磁怪','超級班基拉斯ex','超級快龍ex','帕底亞 土王','雷公ex','長耳兔','瑪力露麗','月亮伊布ex']
print('### 合併口徑 四日軌跡（份額 / AWR / N）')
print('牌組'.ljust(20) + '  '.join(f'{d[4:]:>22}' for d in days))
for nm in names:
    row = []
    for d in days:
        r = comb[d].get(nm)
        row.append(f"{r['share']:.2f}/{r['awr']:.2f}/{r['n']}" if r else "  --  ")
    print(f"{nm[:18]:20} " + '  '.join(f'{x:>22}' for x in row))

print()
print('### 全環境加權 AWR（合併口徑）')
for d in days:
    rows = json.load(open(f"memory/ptcgp_meta_{d}_std_comb_re.json" if d!='20261106' else "memory/ptcgp_meta_20261106_std_comb.json"))['rows']
    w = sum(r['w'] for r in rows); n = sum(r['n'] for r in rows)
    print(f"{d}: {(w+12)/(n+25)*100:.2f}%  N={n}")
