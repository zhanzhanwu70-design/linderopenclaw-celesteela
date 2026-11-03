#!/usr/bin/env python3
"""2026-11-02：以官方台版卡名重建字典（card_names 對齊 + 補齊牌組名）

官方來源：tcgpocket.centropkmn.com/zh_TW/{SET}（遊戲內台版官方卡名）
"""
import json, re, collections
from pathlib import Path

WS = Path("/home/amr/.openclaw/workspace-celesteela")
DICT = WS / "ptcgp_deck_dictionary.json"
cards = json.loads((WS / "memory/ptcgp_cards_full.json").read_text(encoding="utf-8"))
num2zh = json.loads((WS / "memory/official_zh_map.json").read_text(encoding="utf-8"))
D = json.loads(DICT.read_text(encoding="utf-8"))
cn = D["card_names"]; dn = D["deck_names"]

# 1) 官方名覆蓋（英文名 -> 官方台版名）
en2zh = {}
for k, c in cards.items():
    if k in num2zh and c.get("name"):
        en2zh.setdefault(c["name"], num2zh[k])
updated = []
for en, zh in en2zh.items():
    if en in cn and cn[en] != zh:
        updated.append((en, cn[en], zh)); cn[en] = zh
print(f"card_names 以官方名覆蓋 {len(updated)} 條；總數 {len(cn)}")

# 2) 牌組名分段：候選 = DB 卡名 ∪ 字典卡名（正規化彎引號）
def norm(s):
    return s.replace("\u2019", "'").replace("\u2018", "'")

card_list = sorted({norm(n) for n in en2zh.keys()} | {norm(n) for n in cn.keys()}, key=len, reverse=True)
zh_map = {norm(k): v for k, v in cn.items()}

meta = json.loads((WS / "memory/ptcgp_meta_20261102_std.json").read_text(encoding="utf-8"))
meta_c = json.loads((WS / "memory/ptcgp_meta_20261102_std_comb.json").read_text(encoding="utf-8"))
names = sorted({r["name"] for r in meta["rows"]} | {r["name"] for r in meta_c["rows"]})

def translate(nm):
    rest = norm(nm); out = []
    while rest:
        for c in card_list:
            if rest == c or rest.startswith(c + " "):
                out.append(zh_map.get(c) or en2zh.get(c) or c)
                rest = rest[len(c):].strip()
                break
        else:
            return None
    return " ".join(out)

added = 0; still = []
for nm in names:
    t = translate(nm)
    if t:
        if dn.get(nm) != t:
            dn[nm] = t; added += 1
    else:
        still.append(nm)

D["metadata"]["last_updated"] = "2026-11-02"
D["metadata"]["version"] = "4.2"
D["metadata"]["official_zh_aligned"] = "2026-11-02（tcgpocket.centropkmn.com/zh_TW 全 22 系列）"
DICT.write_text(json.dumps(D, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"deck_names 更新 {added} 條（共 {len(dn)}）；仍缺 {len(still)}")
for m in still: print("  MISS:", m)
