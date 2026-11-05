import json
from pathlib import Path
P = Path('/home/amr/.openclaw/workspace-celesteela/ptcgp_deck_dictionary.json')
d = json.loads(P.read_text(encoding='utf-8'))
ADD = {
    'Alolan Exeggutor ex Cleffa': '阿羅拉 椰蛋樹ex 皮寶寶',
    'Dedenne ex Jolteon ex': '咚咚鼠ex 雷伊布ex',
    'Entei ex Charizard': '炎帝ex 噴火龍',
    'Fuecoco ex Skeledirge': '呆火鱷ex 骨紋巨聲龍',
    'Greninja Mega Mewtwo X ex': '甲賀忍蛙 超級超夢Xex',
    'Greninja Samurott': '甲賀忍蛙 大劍鬼',
    'Lunala Mega Mewtwo X ex': '露奈雅拉 超級超夢Xex',
    'Mega Dragonite ex Umbreon': '超級快龍ex 月亮伊布',
    'Mega Gallade ex Gallade': '超級艾路雷朵ex 艾路雷朵ex',
    'Mega Mewtwo X ex Indeedee ex': '超級超夢Xex 愛管侍ex',
    'Mega Sceptile ex Teal Mask Ogerpon ex': '超級蜥蜴王ex 厄鬼椪 碧草面具ex',
    'Palossand Paldean Clodsire': '噬沙堡爺 帕底亞 土王',
    'Pikachu ex Mega Manectric ex': '皮卡丘ex 超級雷電獸ex',
}
added = 0
for k, v in ADD.items():
    if k not in d['deck_names']:
        d['deck_names'][k] = v; added += 1
d['metadata']['last_updated'] = '2026-11-04'
d['metadata']['version'] = '4.5'
d['metadata']['deck_names_count'] = len(d['deck_names'])
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('added', added, 'total deck_names', len(d['deck_names']))
