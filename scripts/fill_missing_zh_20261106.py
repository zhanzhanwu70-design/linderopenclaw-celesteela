import json, collections

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P), object_pairs_hook=collections.OrderedDict)

NEW = {
    'Alolan Exeggutor ex Decidueye ex': '阿羅拉 椰蛋樹ex 狙射樹梟ex',
    'Mega Metagross ex Orthworm': '超級巨金怪ex 拖拖蚓',
    'Charizard Cleffa': '噴火龍 皮寶寶',
    'Paldean Clodsire Mime Jr.': '帕底亞 土王 魔尼尼',
    'Mega Charizard X ex Charizard': '超級噴火龍Xex 噴火龍',
    'Mewtwo ex Mew ex': '超夢ex 夢幻ex',
    'Mega Metagross ex Metagross': '超級巨金怪ex 巨金怪',
}

added = []
for k, v in NEW.items():
    if k not in D['deck_names']:
        D['deck_names'][k] = v
        added.append((k, v))

D['metadata']['deck_names_count'] = len(D['deck_names'])
D['metadata']['version'] = '4.7'
D['metadata']['last_updated'] = '2026-11-06'
D['last_updated'] = '2026-11-06'

json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
print('deck_names:', len(D['deck_names']))
for a in added: print('  新增', a)

# 驗證：今日所有列都翻譯得到
miss = []
for f in ['memory/ptcgp_meta_20261106_std.json', 'memory/ptcgp_meta_20261106_std_comb.json']:
    for r in json.load(open(f))['rows']:
        if r['name'] not in D['deck_names'] and r['name'] not in D['card_names']:
            miss.append(r['name'])
print('仍缺翻譯:', miss)
