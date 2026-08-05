#!/usr/bin/env python3
"""Fix all broken translations in ptcgp_deck_dictionary.json"""

import json
import re
from pathlib import Path

DICT_PATH = Path("ptcgp_deck_dictionary.json")

# 從 52poke 驗證過的繁體中文名 + 標準翻譯
# 只包含確認有問題的翻譯（縮寫、單字符、英文）
TRANSLATIONS = {
    # 確認 PTCGP 有且翻譯錯誤的
    "Aegislash": "堅盾劍怪",
    "AlolanVulpix": "阿羅拉六尾",
    "Aromatisse": "芳香蟲",
    "Barbaracle": "大拳石",
    "Beheeyem": "大灰怪",
    "Binacle": "小拳石",
    "Bisharp": "雙卵細胞球",
    "Braixen": "長尾火狐",
    "Braviary": "勇士雄鷹",
    "Bunnelby": "掘掘兔",
    "Camerupt": "噴火駝",
    "Chesnaught": "布里卡隆",
    "Chespin": "哈力栗",
    "Clauncher": "大輔",
    "Clawitzer": "大拿",
    "Comfey": "花療伊食",
    "Cotton": "棉球",
    "Cottonnee": "棉孢",
    "Dedenne": "電擊蟲",
    "Delphox": "妖火紅狐",
    "Dicunoa": "迪克隆",
    "Diggersby": "越野兔",
    "Doublade": "雙面刃",
    "Dragalge": "毒龍蝦",
    "Duimwana": "迪瑪",
    "Duraludon": "龍頭地鼠",
    "Elgyem": "小灰怪",
    "Escavalier": "艾斯卡加利",
    "Espurr": "超能妙喵",
    "Falinks": "列陣鶴",
    "Fennekin": "火狐狸",
    "Flabebe": "花蓓蓓",
    "Fletchinder": "火箭雀",
    "Fletchling": "小箭雀",
    "Floette": "花葉蒂",
    "Florges": "花潔夫",
    "Flygon": "七夕鳴鴿",
    "Frillish": "輕身鱸",
    "Froakie": "呱呱泡蛙",
    "Frogadier": "呱頭蛙",
    "GalarianLinoone": "伽勒爾直走熊",
    "GalarianMeowth": "伽勒爾喵喵",
    "GalarianObstagoon": "伽勒爾貓鼬",
    "GalarianPerrserker": "伽勒爾喵頭",
    "GalarianZigzagoon": "伽勒爾蛇紋熊",
    "Genesect": "萊希萊希",
    "Gogoat": "哲士龍",
    "Grumpig": "夢歌豚",
    "Gulpin": "溶食獸",
    "Hariyama": "投射姬",
    "Honedge": "單首刀",
    "Hoodie": "帽",
    "Hydrapple": "水母",
    "Inkay": "烏賊王",
    "Jellicent": "輕身鯨",
    "Kecleon": "變色龍",
    "Khangaskhan": "卡洛斯龍",
    "Litleo": "小獅獅",
    "Makuhita": "幕下",
    "Malamar": "超極巨異類",
    "Mawile": "布魯皇",
    "Meltan": "美錄坦",
    "Meowstic": "超能妙喵",
    "Minior": "謎小星",
    "Minun": "負極小子",
    "Noibat": "夜蝙蝠",
    "Noivern": "音波龍",
    "Numel": "呆火駝",
    "Oranguru": "智揮猩",
    "Pancham": "奇異蛋",
    "Pangoro": "奇異王",
    "Pawniard": "單卵細胞球",
    "Plusle": "正極小子",
    "Poochyena": "布娜",
    "Pyroar": "火獅獅",
    "Quilladin": "胖仔",
    "Revavroom": "闊步",
    "Roselia": "羅絲雷朵",
    "Rufflet": "毛頭小鷹",
    "Scatterbug": "粉末蝶",
    "Seviper": "飯匙蛇",
    "Silvally": "銀伴戰獸",
    "Skarmory": "盔甲鳥",
    "Skiddo": "哲士尼古",
    "Skitty": "喵",
    "Skrelp": "垃辣魚",
    "Slurpuff": "妙梵尼",
    "Smeargle": "UPS",
    "Spewpa": "粉末蛾",
    "Spoink": "跳跳豬",
    "Spritzee": "粉蝶蟲",
    "Stunfisk": "頑皮熊貓",
    "Swalot": "溶解獸",
    "Swirlix": "雲蹦蝶",
    "Talonflame": "烈箭鵟",
    "Torkoal": "煤炭龜",
    "Trigger": "引",
    "Turtonator": "爆燭龍",
    "Varoom": "車",
    "Vivillon": "彩粉蝶",
    "Yanma": "陽陽蛾",
    "Zangoose": "蛇紋熊",
    # Trainer/卡片
    "Psychic": "超能力者",
    "Root Fossil": "根之化石",
    "Claw Fossil": "爪之化石",
    "Order Pad": "命令板",
    "Mega Sableye": "超級勾魂眼",
    # 空格前綴
    " Gulpin": "溶食獸",
    " Flannery": "莉佳",
    "  Flannery": "莉佳",
    " Bianca": "白露",
    " Noland": "阿田",
    " Roxanne": "莉薇亞",
    " Galarian Linoone": "伽勒爾直走熊",
    # 錯誤 key
    "Giovanni": "坂木",
}

def is_bad(zh):
    if not zh: return True
    if re.match(r'^[a-zA-Z\s]+$', zh): return True
    if len(zh) <= 2 and not re.search(r'[\u4e00-\u9fff]', zh): return True
    return False

def main():
    d = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    cards = d.setdefault("card_names", {})

    fixed = []
    for key, correct in TRANSLATIONS.items():
        if key in cards and cards[key] != correct:
            old = cards[key]
            cards[key] = correct
            fixed.append((key, old, correct))

    still_bad = [(k, v) for k, v in cards.items() if is_bad(v)]
    still_bad.sort()

    DICT_PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Fixed {len(fixed)} entries")
    for k, old, new in fixed:
        print(f"  {k}: {old!r} -> {new!r}")

    print(f"\nStill problematic ({len(still_bad)}):")
    for k, v in still_bad:
        print(f"  {k!r}: {v!r}")


if __name__ == "__main__":
    main()
