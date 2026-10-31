#!/usr/bin/env python3
"""Apply official zh_TW names (from game assets) to the PTCGP dictionary + log corrections."""

import json
from pathlib import Path

WS = Path("/home/amr/.openclaw/workspace-celesteela")
DICT = WS / "ptcgp_deck_dictionary.json"
CARDS = WS / "memory/ptcgp_cards_full.json"
ZH = WS / "memory/c1_zh_map.json"

cards = json.loads(CARDS.read_text(encoding="utf-8"))
zh = json.loads(ZH.read_text(encoding="utf-8"))
d = json.loads(DICT.read_text(encoding="utf-8"))
d.setdefault("card_names", {})
d.setdefault("corrections", [])
d.setdefault("set_names", {})
d.setdefault("set_short_names", {})

d["set_names"]["Dual Fusion"] = "雙元融合"
d["set_short_names"]["C1"] = "雙元融合"

added, changed = [], []
for key, card in sorted(cards.items()):
    if not key.startswith("C1_"):
        continue
    name = card.get("name")
    zh_name = zh.get(name)
    if not name or not zh_name:
        continue
    old = d["card_names"].get(name)
    if old is None:
        d["card_names"][name] = zh_name
        added.append((name, zh_name))
    elif old != zh_name:
        d["card_names"][name] = zh_name
        changed.append((name, old, zh_name))
        d["corrections"].append({
            "date": "2026-10-31",
            "english": name,
            "correction": f"依 C1「雙元融合」台版官方卡名修正為「{zh_name}」（原「{old}」）。",
        })

d["last_updated"] = "2026-10-31"
d.setdefault("metadata", {})
d["metadata"]["version"] = "3.8"
d["metadata"]["last_updated"] = "2026-10-31"
d["metadata"]["c1_dual_fusion_cards"] = 217
DICT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"added={len(added)} corrected={len(changed)} total card_names={len(d['card_names'])}")
for n, o, z in changed[:80]:
    print(f"  {n}: {o} -> {z}")

c1_names = sorted({cards[k]["name"] for k in cards if k.startswith("C1_") and cards[k].get("name")})
missing = [n for n in c1_names if n not in d["card_names"]]
print(f"C1 unique={len(c1_names)} missing={missing}")
