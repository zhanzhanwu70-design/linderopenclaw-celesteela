import json
from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/ptcgp_deck_dictionary.json')
d = json.loads(P.read_text(encoding='utf-8'))
ADD = {
    'Armarouge ex Ceruledge': '紅蓮鎧騎ex 蒼炎刃鬼',
    'Blastoise Chien-Pao ex': '水箭龜 古劍豹ex',
    'Chien Pao ex': '古劍豹ex',
    'Chien-Pao ex Baxcalibur': '古劍豹ex 戟脊龍',
    'Decidueye ex Decidueye': '狙射樹梟ex 狙射樹梟',
    'Decidueye ex Greninja': '狙射樹梟ex 甲賀忍蛙',
    'Fuecoco ex Armarouge ex': '呆火鱷ex 紅蓮鎧騎ex',
    'Fuecoco ex Charizard': '呆火鱷ex 噴火龍',
    'Giratina ex Guzzlord ex': '騎拉帝納ex 惡食大王ex',
    'Greninja Wigglytuff ex': '甲賀忍蛙 胖可丁ex',
    'Koraidon ex Great Tusk': '故勒頓ex 雄偉牙',
    'Magnezone Lugia ex': '自爆磁怪 洛奇亞ex',
    'Mega Absol ex Umbreon ex': '超級阿勃梭魯ex 月亮伊布ex',
    'Mega Altaria ex Frogadier': '超級七夕青鳥ex 呱頭蛙',
    'Mega Diancie ex Wigglytuff': '超級蒂安希ex 胖可丁',
    'Mega Gallade ex Lycanroc ex': '超級艾路雷朵ex 鬃岩狼人ex',
    'Mega Kangaskhan ex Happiny': '超級袋獸ex 小福蛋',
    'Mega Lucario ex Happiny': '超級路卡利歐ex 小福蛋',
    'Mega Sableye ex Hydreigon': '超級勾魂眼ex 三首惡龍',
    'Mega Sceptile ex Butterfree': '超級蜥蜴王ex 巴大蝶',
    'Mega Sceptile ex Vespiquen': '超級蜥蜴王ex 蜂女王',
    'Mega Steelix ex Sylveon': '超級大鋼蛇ex 仙子伊布',
    'Mega Tyranitar ex Goomy': '超級班基拉斯ex 黏黏寶',
    'Mega Tyranitar ex Wynaut': '超級班基拉斯ex 小果然',
    'Meowscarada Teal Mask Ogerpon ex': '魔幻假面喵 厄鬼椪 碧草面具ex',
    'Pidgeot ex Pidgeot': '大比鳥ex 大比鳥',
    'Primeape Paldean Clodsire': '火爆猴 帕底亞 土王',
    'Solgaleo ex Entei ex': '索爾迦雷歐ex 炎帝ex',
    'Sylveon ex Eevee ex': '仙子伊布ex 伊布ex',
    "Team Rocket's Weezing ex Hydreigon": '火箭隊的雙彈瓦斯 三首惡龍',
    'Vaporeon ex Mega Greninja ex': '水精靈ex 超級甲賀忍蛙ex',
    'Wigglytuff Darkrai': '胖可丁 達克萊伊',
}
added = 0
for k, v in ADD.items():
    if k not in d['deck_names']:
        d['deck_names'][k] = v
        added += 1
d['metadata']['last_updated'] = '2026-11-05'
d['metadata']['version'] = '4.6'
d['metadata']['deck_names_count'] = len(d['deck_names'])
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('added', added, 'total deck_names', len(d['deck_names']))
