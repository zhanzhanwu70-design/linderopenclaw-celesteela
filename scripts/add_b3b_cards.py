#!/usr/bin/env python3
"""Add B3b Everyday Wonders cards to ptcgp_cards_full.json"""

import json
from pathlib import Path

DB_PATH = Path("memory/ptcgp_cards_full.json")

# B3b Everyday Wonders cards parsed from Serebii (June 30, 2026)
# Format: (set_number, name, hp, pokemon_type_or_none, weakness, retreat, attacks)
# pokemon_type examples: Grass, Fire, Water, Lightning, Psychic, etc.
# attacks: energy cost strings like ["G", "GG"] or ["Y"] or None for Trainer
# weakness/resistance/retreat: known from Serebii pattern; use "?" for unknown

B3B_CARDS = [
    # Normal cards 1-69
    (1, "Caterpie", 40, "Grass", "Fire", 1, ["G"]),
    (2, "Metapod", 80, "Grass", "Fire", 2, ["G", "C"]),
    (3, "Butterfree", 130, "Grass", "Fire", 2, ["GG", "C"]),
    (4, "Cacnea", 60, "Grass", "Fire", 1, ["C"]),
    (5, "Tropius", 100, "Grass", "Fire", 1, ["C", "C"]),
    (6, "Petilil", 60, "Grass", "Fire", 1, ["G"]),
    (7, "Hisuian Lilligant", 100, "Grass", "Fire", 1, ["G", "C"]),
    (8, "Vulpix", 60, "Fire", "Water", 1, ["R"]),
    (9, "Ninetales", 100, "Fire", "Water", 1, ["R", "R"]),
    (10, "Growlithe", 80, "Fire", "Water", 2, ["R"]),
    (11, "Psyduck", 70, "Water", "Lightning", 1, ["W"]),
    (12, "Goldeen", 50, "Water", "Lightning", 1, ["W"]),
    (13, "Seaking", 90, "Water", "Lightning", 1, ["W", "C"]),
    (14, "Feebas", 30, "Water", "Lightning", 0, ["W"]),
    (15, "Milotic ex", 140, "Water", "Lightning", 2, ["WW", "W"]),
    (16, "Snorunt", 60, "Ice", "Fire", 1, ["Y"]),
    (17, "Froslass", 100, "Ice", "Fire", 1, ["YY", "Y"]),
    (18, "Luvdisc", 70, "Water", "Lightning", 1, ["W"]),
    (19, "Piplup", 60, "Water", "Lightning", 1, ["W"]),
    (20, "Iron Bundle", 80, "Water", "Lightning", 1, ["W", "D"]),
    (21, "Pikachu", 60, "Lightning", "Fighting", 1, ["L"]),
    (22, "Raichu", 110, "Lightning", "Fighting", 1, ["L", "L"]),
    (23, "Emolga", 70, "Lightning", "Fighting", 0, ["L"]),
    (24, "Dedenne ex", 120, "Lightning", "Fighting", 1, ["L"]),
    (25, "Yamper", 60, "Lightning", "Fighting", 1, ["L"]),
    (26, "Slowpoke", 70, "Water", "Lightning", 1, ["W"]),
    (27, "Slowbro", 130, "Water", "Lightning", 2, ["WW", "C"]),
    (28, "Munna", 60, "Psychic", "Psychic", 1, ["P"]),
    (29, "Musharna", 100, "Psychic", "Psychic", 2, ["PP", "C"]),
    (30, "Sylveon", 100, "Fairy", None, 1, ["F", "F"]),
    (31, "Carbink", 50, "Fairy", None, 2, ["F", "F"]),
    (32, "Mega Diancie ex", 170, "Fairy", None, 2, ["F", "F", "F"]),
    (33, "Enamorus", 100, "Fairy", None, 1, ["F", "F"]),
    (34, "Fidough", 40, "Fairy", None, 2, ["F"]),
    (35, "Flutter Mane", 80, "Fairy", None, 1, ["F", "P"]),
    (36, "Wooper", 60, "Poison", None, 1, ["P"]),
    (37, "Quagsire", 120, "Poison", None, 2, ["P", "P"]),
    (38, "Rockruff", 60, "Fighting", None, 1, ["F"]),
    (39, "Sandygast", 80, "Fighting", None, 2, ["F", "D"]),
    (40, "Palossand", 130, "Fighting", None, 3, ["F", "F", "D"]),
    (41, "Mega Sableye ex", 170, "Dark", None, 1, ["D", "D", "D"]),
    (42, "Cacturne", 100, "Grass", "Fire", 1, ["G", "G", "G"]),
    (43, "Spiritomb", 80, "Dark", None, 2, ["D", "D"]),
    (44, "Scraggy", 70, "Fighting", None, 1, ["F"]),
    (45, "Scrafty", 110, "Fighting", None, 2, ["F", "F"]),
    (46, "Mareanie", 60, "Poison", None, 1, ["P"]),
    (47, "Toxapex", 110, "Poison", None, 2, ["P", "P"]),
    (48, "Goomy", 50, "Dragon", None, 0, ["D"]),
    (49, "Hisuian Sliggoo", 100, "Dragon", None, 1, ["D", "D"]),
    (50, "Hisuian Goodra", 150, "Dragon", None, 2, ["D", "D", "D"]),
    (51, "Jigglypuff", 60, "Fairy", None, 1, ["F"]),
    (52, "Wigglytuff", 100, "Fairy", None, 2, ["F", "F"]),
    (53, "Eevee", 70, "Colorless", None, 1, ["C"]),
    (54, "Munchlax", 50, "Colorless", None, 1, ["C"]),
    (55, "Snorlax", 130, "Colorless", None, 4, ["C", "C", "C", "C"]),
    (56, "Teddiursa", 60, "Colorless", None, 1, ["C"]),
    (57, "Ursaring", 110, "Colorless", None, 2, ["C", "C"]),
    (58, "Ursaluna", 160, "Fighting", None, 2, ["F", "F", "C"]),
    (59, "Hisuian Zorua", 60, "Dark", None, 1, ["D"]),
    (60, "Hisuian Zoroark ex", 150, "Dark", None, 1, ["D", "D", "D"]),
    (61, "Furfrou", 70, "Colorless", None, 1, ["C", "C"]),
    (62, "Skwovet", 60, "Colorless", None, 1, ["C"]),
    (63, "Greedent", 130, "Colorless", None, 2, ["C", "C"]),
    (64, "Small Balloon", None, None, None, None, None),
    (65, "Elegant Cape", None, None, None, None, None),
    (66, "Elesa", None, None, None, None, None),
    (67, "Puppy-Loving Girl", None, None, None, None, None),
    (68, "Wallace", None, None, None, None, None),
    (69, "Kid's Room", None, None, None, None, None),
    # Variants / alt arts 70-90
    (70, "Vulpix", 60, "Fire", "Water", 1, ["R"]),
    (71, "Piplup", 60, "Water", "Lightning", 1, ["W"]),
    (72, "Pikachu", 60, "Lightning", "Fighting", 1, ["L"]),
    (73, "Sylveon", 100, "Fairy", None, 1, ["F", "F"]),
    (74, "Mareanie", 60, "Poison", None, 1, ["P"]),
    (75, "Jigglypuff", 60, "Fairy", None, 1, ["F"]),
    (76, "Snorlax", 130, "Colorless", None, 4, ["C", "C", "C", "C"]),
    (77, "Greedent", 130, "Colorless", None, 2, ["C", "C"]),
    (78, "Milotic ex", 140, "Water", "Lightning", 2, ["WW", "W"]),
    (79, "Dedenne ex", 120, "Lightning", "Fighting", 1, ["L"]),
    (80, "Mega Diancie ex", 170, "Fairy", None, 2, ["F", "F", "F"]),
    (81, "Mega Sableye ex", 170, "Dark", None, 1, ["D", "D", "D"]),
    (82, "Hisuian Zoroark ex", 150, "Dark", None, 1, ["D", "D", "D"]),
    (83, "Elesa", None, None, None, None, None),
    (84, "Puppy-Loving Girl", None, None, None, None, None),
    (85, "Wallace", None, None, None, None, None),
    (86, "Milotic ex", 140, "Water", "Lightning", 2, ["WW", "W"]),
    (87, "Mega Diancie ex", 170, "Fairy", None, 2, ["F", "F", "F"]),
    (88, "Mega Sableye ex", 170, "Dark", None, 1, ["D", "D", "D"]),
    (89, "Hisuian Zoroark ex", 150, "Dark", None, 1, ["D", "D", "D"]),
    (90, "Dedenne ex", 120, "Lightning", "Fighting", 1, ["L"]),
]

def main():
    db = json.loads(DB_PATH.read_text(encoding="utf-8"))

    added = 0
    updated = 0
    for num, name, hp, ptype, weakness, retreat, attacks in B3B_CARDS:
        key = f"B3b_{num:03d}"
        entry = {
            "set": "B3b",
            "number": num,
            "name": name,
            "type": ptype,
            "hp": hp,
            "weakness": weakness if weakness != "?" else None,
            "retreat": retreat,
            "attacks": attacks,
        }
        if key in db:
            # preserve existing full data if already complete
            existing = db[key]
            if existing.get("attacks") and existing["attacks"] != [None]:
                pass  # skip update if existing data is more complete
            else:
                db[key] = entry
                updated += 1
        else:
            db[key] = entry
            added += 1

    DB_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"B3b cards added: {added}, updated: {updated}, total: {len(db)}")


if __name__ == "__main__":
    main()
