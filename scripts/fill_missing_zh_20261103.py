import json, io

PATH = 'ptcgp_deck_dictionary.json'
with open(PATH, encoding='utf-8') as f:
    d = json.load(f)

ADD = {
    'Mega Lucario ex Hitmonchan ex': '超級路卡利歐 ex 快拳郎ex',
    'Blastoise Lapras': '水箭龜 拉普拉斯',
    'Mega Sharpedo ex Blastoise': '超級巨牙鯊ex 水箭龜',
    'Mega Blastoise ex Blastoise': '超級水箭龜ex 水箭龜',
    'Milotic ex Igglybuff': '美納斯ex 寶寶丁',
    'Paldean Clodsire Whiscash': '帕底亞 土王 鯰魚王',
    'Solgaleo ex Ferrothorn': '索爾迦雷歐ex 堅果啞鈴',
    'Mega Sharpedo ex Mega Gyarados ex': '超級巨牙鯊ex 超級暴鯉龍ex',
    'Dedenne ex Sylveon': '咚咚鼠ex 仙子伊布',
    'Mega Sceptile ex Leafeon ex': '超級蜥蜴王ex 葉伊布ex',
    'Gardevoir Giratina ex': '沙奈朵 騎拉帝納ex',
    'Pikachu ex Happiny': '皮卡丘ex 小福蛋',
    'Alolan Exeggutor ex Tsareena': '阿羅拉 椰蛋樹ex 甜冷美后',
    'Pawmot Ditto': '巴布土撥 百變怪',
    'Teal Mask Ogerpon ex Pidgeot': '厄鬼椪 碧草面具ex 大比鳥',
    'Mega Gyarados ex Dusknoir': '超級暴鯉龍ex 黑夜魔靈',
    'Dedenne ex Pikachu ex': '咚咚鼠ex 皮卡丘ex',
    'Mega Greninja ex Dustox': '超級甲賀忍蛙ex 毒粉蛾',
    'Vespiquen ex Teal Mask Ogerpon ex': '蜂女王ex 厄鬼椪 碧草面具ex',
    'Mega Dragonite ex Suicune ex': '超級快龍ex 水君ex',
    'Ho-Oh ex Snorlax ex': '鳳王ex 卡比獸ex',
    'Flutter Mane ex Gengar': '振翼髮ex 耿鬼',
    'Mega Tyranitar ex Chingling': '超級班基拉斯ex 鈴鐺響',
    'Rotom ex Mime Jr.': '洛托姆ex 魔尼尼',
    'Mega Sharpedo ex Milotic ex': '超級巨牙鯊ex 美納斯ex',
    'Gengar Nihilego': '耿鬼 虛吾伊德',
    'Teal Mask Ogerpon ex': '厄鬼椪 碧草面具ex',
    'Flutter Mane ex': '振翼髮ex',
}

added = 0
for k, v in ADD.items():
    if k not in d['deck_names']:
        d['deck_names'][k] = v
        added += 1

d['metadata']['last_updated'] = '2026-11-03'
d['metadata']['version'] = '4.4'
d['metadata']['deck_names_count'] = len(d['deck_names'])

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('added', added, 'total deck_names', len(d['deck_names']))
