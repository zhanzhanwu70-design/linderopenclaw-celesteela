#!/usr/bin/env python3
"""補齊缺漏的官方台版卡名 + 牌組名（2026-11-02 C1 環境新增 67 條牌組名）

來源：tcgpocket.centropkmn.com/zh_TW/{SET}（遊戲內台版官方卡名）
"""
import json, re, sys, time
from pathlib import Path
import requests

WS = Path("/home/amr/.openclaw/workspace-celesteela")
DICT = WS / "ptcgp_deck_dictionary.json"
CARDS = WS / "memory/ptcgp_cards_full.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

SETS = ["A1", "A1a", "A2", "A2a", "A2b", "A3", "A3a", "A3b", "A4", "A4a", "A4b",
        "B1", "B1a", "B2", "B2a", "B2b", "B3", "B3a", "B3b", "B4", "B4a", "C1"]


def fetch_set(set_code, session):
    url = f"https://tcgpocket.centropkmn.com/zh_TW/{set_code.lower()}"
    r = session.get(url, timeout=40)
    r.raise_for_status()
    html = r.content.decode("utf-8", errors="replace")
    tiles = re.findall(rf'href="/zh_TW/{set_code.lower()}/(\d+)-[a-z0-9\-]+"[^>]*?aria-label="#\d+ ([^"]+)"', html)
    return {int(n): zh for n, zh in tiles}


def main():
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    d = json.loads(DICT.read_text(encoding="utf-8"))
    cn = d.setdefault("card_names", {})
    dn = d.setdefault("deck_names", {})

    # 需要補的英文卡名
    need_cards = sys.argv[1:] or []
    s = requests.Session(); s.headers.update(HEADERS)

    # 建立 SET_NUM -> zh
    num2zh = {}
    for sc in SETS:
        try:
            m = fetch_set(sc, s)
        except Exception as e:
            print(f"  !! {sc} 抓取失敗: {e}")
            continue
        for n, zh in m.items():
            num2zh[f"{sc}_{n:03d}"] = zh
        print(f"  {sc}: {len(m)} 張")
        time.sleep(0.4)

    # 英文名 -> 官方台版名
    en2zh = {}
    for k, c in cards.items():
        if k in num2zh:
            en2zh.setdefault(c.get("name"), num2zh[k])

    added_cards = 0
    for en, zh in en2zh.items():
        if en and zh and en not in cn:
            cn[en] = zh
            added_cards += 1
    print(f"card_names 新增 {added_cards} 條（共 {len(cn)}）")

    # 牌組名：拆成卡名並翻譯
    meta = json.loads((WS / "memory/ptcgp_meta_20261102_std.json").read_text(encoding="utf-8"))
    rows = meta["rows"]
    names = sorted({r["name"] for r in rows})
    card_list = sorted(en2zh.keys(), key=len, reverse=True)

    def translate_deck(nm):
        rest = nm
        out = []
        while rest:
            for c in card_list:
                if rest.startswith(c + " ") or rest == c:
                    out.append(cn.get(c) or en2zh.get(c) or c)
                    rest = rest[len(c):].strip()
                    break
            else:
                return None
        return " ".join(out)

    added = 0
    still = []
    for nm in names:
        if nm in dn:
            continue
        t = translate_deck(nm)
        if t:
            dn[nm] = t
            added += 1
        else:
            still.append(nm)

    d["metadata"]["last_updated"] = "2026-11-02"
    d["metadata"]["version"] = "4.1"
    DICT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"deck_names 新增 {added} 條（共 {len(dn)}）；仍缺 {len(still)}")
    for m in still:
        print("  MISS:", m)


if __name__ == "__main__":
    main()
