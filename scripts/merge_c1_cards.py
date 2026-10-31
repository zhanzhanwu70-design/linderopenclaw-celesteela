#!/usr/bin/env python3
"""Merge C1 (Dual Fusion) card data into memory/ptcgp_cards_full.json"""

import json
from pathlib import Path

DB = Path("memory/ptcgp_cards_full.json")
SRC = Path("memory/ptcgp_cards_c1.json")

db = json.loads(DB.read_text(encoding="utf-8"))
cards = json.loads(SRC.read_text(encoding="utf-8"))

added = updated = 0
for c in cards:
    key = f"C1_{c['number']:03d}"
    entry = {
        "set": "C1",
        "number": c["number"],
        "name": c["name"],
        "type": c["type"] if c["type"] else "",
        "hp": c["hp"],
        "weakness": c["weakness"],
        "retreat": c["retreat"],
        "attacks": c.get("attack_costs", []),
    }
    if c.get("stage"):
        entry["stage"] = c["stage"]
    if c.get("ability"):
        entry["ability"] = c["ability"]
        if c.get("ability_effect"):
            entry["ability_effect"] = c["ability_effect"]
    if c.get("attacks"):
        entry["attack_details"] = c["attacks"]
    if key in db:
        db[key] = entry
        updated += 1
    else:
        db[key] = entry
        added += 1

DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"C1 merged: added={added} updated={updated} total={len(db)}")

# stats
pk = [v for k, v in db.items() if k.startswith("C1_") and v.get("type")]
tr = [v for k, v in db.items() if k.startswith("C1_") and not v.get("type")]
print(f"C1 pokemon={len(pk)} trainer={len(tr)}")
noattack = [v["name"] for v in pk if not v.get("attacks")]
print("pokemon without attacks:", noattack)
