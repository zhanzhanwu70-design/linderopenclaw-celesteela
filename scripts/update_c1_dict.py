#!/usr/bin/env python3
"""Update translation dictionary + card lookup indexes with C1 (Dual Fusion) data."""

import json
from pathlib import Path

WS = Path("/home/amr/.openclaw/workspace-celesteela")
SKILL = Path("/home/amr/.openclaw/skills/ptcgp-card-lookup")

DICT = WS / "ptcgp_deck_dictionary.json"
CARDS = WS / "memory/ptcgp_cards_full.json"
ZH_MAP = WS / "memory/c1_zh_map.json"

cards = json.loads(CARDS.read_text(encoding="utf-8"))
zh = json.loads(ZH_MAP.read_text(encoding="utf-8"))
dict_ = json.loads(DICT.read_text(encoding="utf-8"))

dict_.setdefault("card_names", {})
dict_.setdefault("set_names", {})
dict_.setdefault("set_short_names", {})

# 1. set names (Pokemon Hubs + Bahamut: 雙元融合)
dict_["set_names"]["Dual Fusion"] = "雙元融合"
dict_["set_short_names"]["C1"] = "雙元融合"

# 2. card names for C1 cards (official zh_TW asset names)
added = replaced = 0
for key, card in cards.items():
    if not key.startswith("C1_"):
        continue
    name = card.get("name")
    if not name:
        continue
    zh_name = zh.get(name)
    if not zh_name:
        continue
    if name in dict_["card_names"]:
        if dict_["card_names"][name] != zh_name:
            print(f"  ! differs: {name}: {dict_['card_names'][name]} -> {zh_name}")
            replaced += 1
    else:
        dict_["card_names"][name] = zh_name
        added += 1

dict_["last_updated"] = "2026-10-31"
DICT.write_text(json.dumps(dict_, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"card_names: added={added} differs={replaced} total={len(dict_['card_names'])}")

# 3. card lookup indexes
num2name = json.loads((SKILL / "number_to_name.json").read_text(encoding="utf-8"))
name2nums = json.loads((SKILL / "name_to_numbers.json").read_text(encoding="utf-8"))

c1_map = {}
for key, card in sorted(cards.items()):
    if not key.startswith("C1_"):
        continue
    num = str(card["number"])
    c1_map[num] = card["name"]
    name2nums.setdefault(card["name"], [])
    if key not in name2nums[card["name"]]:
        name2nums[card["name"]].append(key)
num2name["C1"] = c1_map

(SKILL / "number_to_name.json").write_text(json.dumps(num2name, ensure_ascii=False, indent=2), encoding="utf-8")
(SKILL / "name_to_numbers.json").write_text(json.dumps(name2nums, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"number_to_name sets={len(num2name)} C1 entries={len(c1_map)} | name_to_numbers={len(name2nums)}")

# 4. report untranslated C1 names
c1_names = sorted({cards[k]["name"] for k in cards if k.startswith("C1_") and cards[k].get("name")})
missing = [n for n in c1_names if n not in dict_["card_names"]]
print(f"C1 unique names={len(c1_names)} still missing zh={len(missing)}: {missing}")
