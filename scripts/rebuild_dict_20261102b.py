#!/usr/bin/env python3
"""2026-11-02（二次）：修正分段邏輯 —— 排除 card_names 內的「複合牌組名」，
以官方卡名重新組出今日所有牌組名。"""
import json
from pathlib import Path

WS = Path("/home/amr/.openclaw/workspace-celesteela")
D = json.loads((WS / "ptcgp_deck_dictionary.json").read_text(encoding="utf-8"))
cards = json.loads((WS / "memory/ptcgp_cards_full.json").read_text(encoding="utf-8"))
num2zh = json.loads((WS / "memory/official_zh_map.json").read_text(encoding="utf-8"))
cn = D["card_names"]; dn = D["deck_names"]

def norm(s): return s.replace("\u2019", "'").replace("\u2018", "'")

# 官方卡名對照（DB 卡名 -> 官方台版名）
en2zh = {}
for k, c in cards.items():
    if k in num2zh and c.get("name"):
        en2zh.setdefault(c["name"], num2zh[k])

# 基本卡名候選：DB 卡名 + 字典中「非複合」卡名
base = set(en2zh.keys()) | set(cn.keys())

def segmentable(key, cands):
    """key 能否被切成 2 個以上候選卡名（排除自身）"""
    rest = norm(key); n = 0
    while rest:
        hit = None
        for c in cands:
            if c == norm(key):
                continue
            if rest == c or rest.startswith(c + " "):
                hit = c; break
        if not hit: return n >= 2
        rest = rest[len(hit):].strip(); n += 1
    return n >= 2

cands_all = sorted({norm(n) for n in base}, key=len, reverse=True)
composite = {norm(k) for k in cn if segmentable(k, cands_all)}
cands = [c for c in cands_all if c not in composite]
print(f"卡名候選 {len(cands)} 條，排除複合牌組名 {len(composite)} 條")

zh_map = {norm(k): v for k, v in cn.items()}
for en, zh in en2zh.items():
    zh_map[norm(en)] = zh

def translate(nm):
    rest = norm(nm); out = []
    while rest:
        for c in cands:
            if rest == c or rest.startswith(c + " "):
                out.append(zh_map.get(c) or c)
                rest = rest[len(c):].strip()
                break
        else:
            return None
    return " ".join(out)

meta = json.loads((WS / "memory/ptcgp_meta_20261102_std.json").read_text(encoding="utf-8"))
meta_c = json.loads((WS / "memory/ptcgp_meta_20261102_std_comb.json").read_text(encoding="utf-8"))
names = sorted({r["name"] for r in meta["rows"]} | {r["name"] for r in meta_c["rows"]})

changed = 0; still = []
for nm in names:
    t = translate(nm)
    if t:
        if dn.get(nm) != t:
            dn[nm] = t; changed += 1
    else:
        still.append(nm)

D["metadata"]["last_updated"] = "2026-11-02"
D["metadata"]["version"] = "4.3"
D["metadata"]["official_zh_aligned"] = "2026-11-02（tcgpocket.centropkmn.com/zh_TW 全 22 系列）"
(WS / "ptcgp_deck_dictionary.json").write_text(json.dumps(D, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"deck_names 更新 {changed} 條（共 {len(dn)}）；仍缺 {len(still)}")
for m in still: print("  MISS:", m)
for k in ["Miraidon ex Magnezone", "Umbreon", "Mega Greninja ex", "Charizard ex Charizard", "Mega Altaria ex Galarian Cursola"]:
    print(" ", k, "->", dn.get(k))
