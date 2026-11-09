import json, collections

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P), object_pairs_hook=collections.OrderedDict)

NEW = {
    'Flareon ex Charizard': '火伊布ex 噴火龍',
    'Haxorus Goomy': '雙斧戰龍 黏黏寶',
    'Serperior Teal Mask Ogerpon ex': '君主蛇 厄鬼椪 碧草面具ex',
    'Vaporeon ex Eevee ex': '水精靈 ex 伊布ex',
    "Team Rocket's Slowking ex Sylveon ex": '火箭隊的呆呆王 ex 仙子伊布ex',
    'Dragonair Drampa': '哈克龍 老翁龍',
    'Sylveon ex Mega Mewtwo X ex': '仙子伊布ex 超級超夢Xex',
    'Crobat ex Mega Sableye ex': '叉字蝠ex 超級勾魂眼ex',
    'Decidueye ex Heliolisk': '狙射樹梟ex 光電傘蜥',
    'Lugia ex Ho-Oh ex': '洛奇亞ex 鳳王ex',
    'Sylveon ex Mega Medicham ex': '仙子伊布ex 超級恰雷姆ex',
    'Indeedee ex Gengar ex': '愛管侍ex 耿鬼ex',
    'Mew ex Aegislash': '夢幻ex 堅盾劍怪',
    'Lycanroc ex Mega Mewtwo X ex': '鬃岩狼人ex 超級超夢Xex',
    'Arceus ex Tyranitar': '阿爾宙斯ex 班基拉斯',
    'Mega Gallade ex Minior': '超級艾路雷朵ex 小隕星',
    'Milotic ex Blastoise': '美納斯ex 水箭龜',
    'Blastoise Palkia ex': '水箭龜 帕路奇亞ex',
}

added = []
for k, v in NEW.items():
    if k not in D['deck_names']:
        D['deck_names'][k] = v
        added.append((k, v))

D['metadata']['deck_names_count'] = len(D['deck_names'])
D['metadata']['version'] = '4.9'
D['metadata']['last_updated'] = '2026-11-08'
D['last_updated'] = '2026-11-08'

json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
print('deck_names:', len(D['deck_names']))
for a in added:
    print('  新增', a)

miss = []
for f in ['memory/ptcgp_meta_20261108_std.json', 'memory/ptcgp_meta_20261108_std_comb.json']:
    for r in json.load(open(f))['rows']:
        if r['name'] not in D['deck_names'] and r['name'] not in D['card_names']:
            miss.append(r['name'])
print('仍缺翻譯:', miss)
