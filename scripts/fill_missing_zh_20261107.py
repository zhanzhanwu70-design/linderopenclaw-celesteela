import json, collections

P = 'ptcgp_deck_dictionary.json'
D = json.load(open(P), object_pairs_hook=collections.OrderedDict)

NEW = {
    'Alolan Exeggutor ex Meowscarada ex': '阿羅拉 椰蛋樹ex 魔幻假面喵ex',
    "Decidueye ex Team Rocket's Electrode": '狙射樹梟ex 火箭隊的頑皮彈',
    'Dragonair Haxorus': '哈克龍 雙斧戰龍',
    'Espeon Igglybuff': '太陽伊布 寶寶丁',
    'Greninja Mega Scizor ex': '甲賀忍蛙 超級巨鉗螳螂ex',
    'Ho-Oh ex Lugia ex': '鳳王ex 洛奇亞ex',
    'Indeedee ex Mega Mewtwo X ex': '愛管侍ex 超級超夢Xex',
    'Jolteon ex Pikachu ex': '雷伊布ex 皮卡丘ex',
    'Koraidon ex Palossand': '故勒頓ex 噬沙堡爺',
    'Mega Absol ex Hoopa ex': '超級阿勃梭魯ex 胡帕ex',
    'Mega Diancie ex Indeedee ex': '超級蒂安希ex 愛管侍ex',
    'Mega Gengar ex Umbreon ex': '超級耿鬼ex 月亮伊布ex',
    'Mega Gyarados ex Jellicent': '超級暴鯉龍ex 胖嘟嘟',
    'Mega Lucario ex Passimian ex': '超級路卡利歐 ex 投擲猴ex',
    'Mega Manectric ex Pikachu ex': '超級雷電獸ex 皮卡丘ex',
    'Mega Mewtwo X ex Greninja': '超級超夢Xex 甲賀忍蛙',
    'Mega Mewtwo X ex Mega Gardevoir ex': '超級超夢Xex 超級沙奈朵ex',
    'Mega Sceptile ex Chingling': '超級蜥蜴王ex 鈴鐺響',
    'Mega Sceptile ex Venusaur': '超級蜥蜴王ex 妙蛙花',
    'Mega Tyranitar ex Budew': '超級班基拉斯ex 芽〔官方中文名待確認〕',
    'Milotic ex Suicune ex': '美納斯ex 水君ex',
    "Mimikyu ex Team Rocket's Weezing ex": '謎擬Ｑex 火箭隊的雙彈瓦斯 ex',
    'Pawmot Raikou ex': '巴布土撥 雷公ex',
    'Revavroom Mega Skarmory ex': '普隆隆姆 超級盔甲鳥ex',
    'Rotom ex Oricorio': '洛托姆ex 花舞鳥',
    'Umbreon Galarian Obstagoon': '月亮伊布 伽勒爾 堵攔熊',
    'Umbreon Porygon-Z': '月亮伊布 多邊獸Ｚ',
    'Umbreon ex Mega Absol ex': '月亮伊布ex 超級阿勃梭魯ex',
    'Wigglytuff Igglybuff': '胖可丁 寶寶丁',
    'Wigglytuff ex Igglybuff': '胖可丁ex 寶寶丁',
    'Wigglytuff ex Wigglytuff': '胖可丁ex 胖可丁',
}

added = []
for k, v in NEW.items():
    if k not in D['deck_names']:
        D['deck_names'][k] = v
        added.append((k, v))

D['metadata']['deck_names_count'] = len(D['deck_names'])
D['metadata']['version'] = '4.8'
D['metadata']['last_updated'] = '2026-11-07'
D['last_updated'] = '2026-11-07'

json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
print('deck_names:', len(D['deck_names']))
for a in added:
    print('  新增', a)

miss = []
for f in ['memory/ptcgp_meta_20261107_std.json', 'memory/ptcgp_meta_20261107_std_comb.json']:
    for r in json.load(open(f))['rows']:
        if r['name'] not in D['deck_names'] and r['name'] not in D['card_names']:
            miss.append(r['name'])
print('仍缺翻譯:', miss)
