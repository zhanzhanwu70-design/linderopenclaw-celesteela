#!/usr/bin/env python3
"""Add B3b Everyday Wonders card translations to ptcgp_deck_dictionary.json"""

import json
from pathlib import Path

DICT_PATH = Path("ptcgp_deck_dictionary.json")

B3B_TRANSLATIONS = {
    # Pokémon
    "Caterpie": "綠毛蟲",
    "Metapod": "鐵甲蛹",
    "Butterfree": "巴大蝶",
    "Cacnea": "刺球仙人掌",
    "Tropius": "熱帶龍",
    "Petilil": "百合根",
    "Hisuian Lilligant": "洗翠葉伊貝",
    "Vulpix": "六尾",
    "Ninetales": "九尾",
    "Growlithe": "卡蒂狗",
    "Psyduck": "可達鴨",
    "Goldeen": "角金魚",
    "Seaking": "金魚王",
    "Feebas": "醜醜魚",
    "Milotic ex": "美納斯 ex",
    "Snorunt": "雪童子",
    "Froslass": "雪妖女",
    "Luvdisc": "愛心魚",
    "Piplup": "波加曼",
    "Iron Bundle": "鐵包袱",
    "Pikachu": "皮卡丘",
    "Raichu": "雷丘",
    "Emolga": "電龍",
    "Dedenne ex": "電擊蟲 ex",
    "Yamper": "啪嚓小子",
    "Slowpoke": "呆呆獸",
    "Slowbro": "呆殼獸",
    "Munna": "夢夢蝕",
    "Musharna": "夢夢",
    "Sylveon": "仙子伊貝",
    "Carbink": "鑰圈兒",
    "Mega Diancie ex": "超級蒂安希 ex",
    "Enamorus": "願望獸",
    "Fidough": "狗包",
    "Flutter Mane": "迷擬Q",
    "Wooper": "烏培",
    "Quagsire": "骸腕龍",
    "Rockruff": "岩狗狗",
    "Sandygast": "沙堡",
    "Palossand": "沙駱駝",
    "Mega Sableye ex": "超級論謀天狗 ex",
    "Cacturne": "刺客仙人掌",
    "Spiritomb": "鬼盆栽",
    "Scraggy": "泡沫蛙",
    "Scrafty": "鱗甲蛙",
    "Mareanie": "小嘴蝸",
    "Toxapex": "有毒殼",
    "Goomy": "黏黏龍",
    "Hisuian Sliggoo": "洗翠黏黏龍",
    "Hisuian Goodra": "洗翠黏黏龍 ex",
    "Jigglypuff": "胖丁",
    "Wigglytuff": "胖可丁",
    "Eevee": "伊布",
    "Munchlax": "漢佐馬",
    "Snorlax": "卡比獸",
    "Teddiursa": "爆音怪",
    "Ursaring": "格拉西亞",
    "Ursaluna": "爆炸頭水牛",
    "Hisuian Zorua": "洗翠索羅亞",
    "Hisuian Zoroark ex": "洗翠索羅亞克 ex",
    "Furfrou": "披觸獸",
    "Skwovet": "野蠻鱸魚",
    "Greedent": "藏飽魚",
    # Trainers
    "Small Balloon": "小氣球",
    "Elegant Cape": "優雅披風",
    "Elesa": "艾莉絲",
    "Puppy-Loving Girl": "調皮女孩",
    "Wallace": "楓葉",
    "Kids Room": "兒童間",
    # Aliases for variant naming
    "Kids Room": "兒童間",
}

def main():
    d = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    cards = d.setdefault("card_names", {})

    added = 0
    for name, zh in B3B_TRANSLATIONS.items():
        if name not in cards or cards[name] in (None, "", name, "dd"):
            cards[name] = zh
            added += 1
        else:
            print(f"  [skip] {name} already has translation: {cards[name]}")

    DICT_PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added/fixed {added} translations")


if __name__ == "__main__":
    main()
