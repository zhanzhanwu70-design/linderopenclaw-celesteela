#!/usr/bin/env python3
"""PTCG 中英對照每日更新：抓官方 zh_TW 卡名 -> ptcgp_deck_dictionary.json

資料來源：tcgpocket.centropkmn.com/zh_TW/{SET}（卡圖檔名/aria-label 為遊戲內台版官方名稱）
用法：python3 scripts/update_translations.py [SET ...]   # 不帶參數 = 自動取最新系列
"""

import json
import re
import sys
import time
from pathlib import Path

import requests

WS = Path("/home/amr/.openclaw/workspace-celesteela")
DICT = WS / "ptcgp_deck_dictionary.json"
CARDS = WS / "memory/ptcgp_cards_full.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

# 官方台版系列名（由 Pokemon Hubs + 巴哈姆特交叉確認）
SET_ZH = {
    "A1": "Genetic Apex", "A1a": "Mythical Island", "A2": "Space-Time Smackdown",
    "A2a": "Triumphant Light", "A2b": "Shining Revelry", "A3": "Celestial Guardians",
    "A3a": "Extradimensional Crisis", "A3b": "Eevee Grove", "A4": "Wisdom of Sea and Sky",
    "A4a": "Secluded Springs", "A4b": "Deluxe Pack ex", "B1": "Mega Rising",
    "B1a": "Crimson Blaze", "B2": "Fantastical Parade", "B2a": "Paldean Wonders",
    "B2b": "Mega Shine", "B3": "Pulsing Aura", "B3a": "Paradox Drive",
    "B3b": "Everyday Wonders", "B4": "Ruler of Skies", "B4a": "Team Rocket's Ambition",
    "C1": "Dual Fusion",
}


def set_slug(set_code):
    """C1 -> c1dualfusion000-dual-fusion (pokemongohub 形式)；centropkmn 用 /zh_TW/{code} 直接即可"""
    return set_code.lower()


def fetch_zh_tiles(set_code, session):
    url = f"https://tcgpocket.centropkmn.com/zh_TW/{set_slug(set_code)}"
    r = session.get(url, timeout=30)
    r.raise_for_status()
    # requests 會猜 ISO-8859-1 → 中文會變亂碼，強制 utf-8 解碼
    html = r.content.decode("utf-8", errors="replace")
    tiles = re.findall(rf'href="/zh_TW/{set_slug(set_code)}/(\d+)-[a-z0-9\-]+"[^>]*?aria-label="#\d+ ([^"]+)"', html)
    return {int(n): zh for n, zh in tiles}


def main():
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    d = json.loads(DICT.read_text(encoding="utf-8"))
    d.setdefault("card_names", {})
    d.setdefault("corrections", [])

    args = sys.argv[1:]
    if args:
        sets = args
    else:
        # 自動取 DB 中「尚未有台版譯名」的最新系列
        have = {k.split("_")[0] for k in cards if k.startswith(("B", "C", "A"))}
        missing = []
        for s in sorted(have):
            names = {cards[f"{s}_{i:03d}"]["name"] for i in range(1, 400) if f"{s}_{i:03d}" in cards}
            names = {n for n in names if n and n not in d["card_names"]}
            if names:
                missing.append((s, len(names)))
        sets = [missing[-1][0]] if missing else []
        print("auto-detected sets needing translation:", missing)

    if not sets:
        print("nothing to do")
        return

    session = requests.Session()
    session.headers.update(HEADERS)
    added = corrected = 0

    for set_code in sets:
        try:
            by_num = fetch_zh_tiles(set_code, session)
        except Exception as e:
            print(f"{set_code}: fetch failed: {e}")
            continue
        print(f"{set_code}: {len(by_num)} tiles fetched")

        for key, card in sorted(cards.items()):
            if not key.startswith(set_code + "_"):
                continue
            name = card.get("name")
            zh = by_num.get(card["number"])
            if not name or not zh:
                continue
            old = d["card_names"].get(name)
            if old is None:
                d["card_names"][name] = zh
                added += 1
            elif old != zh:
                d["card_names"][name] = zh
                corrected += 1
                d["corrections"].append({
                    "date": time.strftime("%Y-%m-%d"),
                    "english": name,
                    "correction": f"依 {set_code} 官方台版卡名修正為「{zh}」（原「{old}」）。",
                })

        # 擴充包中文名
        en_name = SET_ZH.get(set_code)
        if en_name:
            zh_pack = fetch_pack_zh(set_code, session)
            if zh_pack:
                d.setdefault("set_names", {})[en_name] = zh_pack
                d.setdefault("set_short_names", {})[set_code] = zh_pack
                print(f"  set name: {en_name} -> {zh_pack}")

    d["last_updated"] = time.strftime("%Y-%m-%d")
    d.setdefault("metadata", {})["last_updated"] = d["last_updated"]
    DICT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"done: added={added} corrected={corrected} card_names={len(d['card_names'])}")


def fetch_pack_zh(set_code, session):
    """從 centropkmn 頁面標題取得擴充包中文名（若無則回傳 None）"""
    try:
        resp = session.get(f"https://tcgpocket.centropkmn.com/zh_TW/{set_slug(set_code)}", timeout=30)
        html = resp.content.decode("utf-8", errors="replace")
    except Exception:
        return None
    m = re.search(r"<title>([^<]+)</title>", html)
    if not m:
        return None
    t = m.group(1)
    zh = re.search(r"[\u4e00-\u9fff]{2,8}", t)
    return zh.group(0) if zh else None


if __name__ == "__main__":
    main()
