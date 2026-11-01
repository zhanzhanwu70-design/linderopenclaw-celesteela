#!/usr/bin/env python3
"""只補齊目前缺少的官方台版卡名（不動其他既有條目）。"""
import json, re, requests, time
from pathlib import Path

WS = Path("/home/amr/.openclaw/workspace-celesteela")
DICT = WS / "ptcgp_deck_dictionary.json"
CARDS = WS / "memory/ptcgp_cards_full.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

WANT = {
    "Dragalge", "Gourgeist", "Guzzlord", "Rampardos", "Dusknoir", "Mega Pidgeot ex",
    "Mantyke", "Mega Skarmory ex", "Miltank", "Simisear", "Tapu Koko ex", "Arceus ex",
    "Wigglytuff ex", "Mega Charizard X ex", "Mega Gengar ex", "Charizard X ex",
    "Team Rocket's Moltres ex", "Dragalge ex", "Guzzlord ex", "Tapu Koko",
}

cards = json.loads(CARDS.read_text(encoding="utf-8"))
d = json.loads(DICT.read_text(encoding="utf-8"))
cn = d.setdefault("card_names", {})

# 找每張卡所在的 set + number
targets = []
for key, card in sorted(cards.items()):
    if card.get("name") in WANT:
        targets.append((card["name"], key.split("_")[0], card["number"]))

by_set = {}
for name, s, n in targets:
    by_set.setdefault(s, []).append((name, n))

session = requests.Session()
session.headers.update(HEADERS)

added = []
for s, items in sorted(by_set.items()):
    url = f"https://tcgpocket.centropkmn.com/zh_TW/{s.lower()}"
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
        html = r.content.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"{s}: fetch failed: {e}")
        continue
    tiles = {int(n): zh for n, zh in re.findall(rf'href="/zh_TW/{s.lower()}/(\d+)-[a-z0-9\-]+"[^>]*?aria-label="#\d+ ([^"]+)"', html)}
    print(f"{s}: {len(tiles)} tiles")
    for name, n in items:
        zh = tiles.get(n)
        if zh:
            if name not in cn:
                cn[name] = zh
                added.append((name, zh))
            else:
                print(f"  keep existing: {name} = {cn[name]} (official {zh})")
        else:
            print(f"  {s} #{n} {name}: not found in tiles")

d["last_updated"] = time.strftime("%Y-%m-%d")
d.setdefault("metadata", {})["last_updated"] = d["last_updated"]
DICT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("added:", added)
print("card_names count:", len(cn))
