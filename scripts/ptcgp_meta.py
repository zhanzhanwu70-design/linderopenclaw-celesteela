#!/usr/bin/env python3
"""
PTCGP Meta & Card List Generator
自動抓取 Limitless TCG Meta 資料，生成翻譯表格與卡表
"""

import json
import re
import sys
import argparse
from datetime import datetime

# ========== 設定區 ==========
DICT_PATH = "ptcgp_deck_dictionary.json"
META_CACHE = "memory/ptcgp_meta_cache.json"

AWR_OFFSET_WINS = 12
AWR_OFFSET_TOTAL = 25

# ========== 載入字典 ==========
def load_dict():
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def translate(name, dd):
    """查詢字典，翻譯卡牌/牌組名稱"""
    card_names = dd.get("card_names", {})
    # 精確匹配
    if name in card_names:
        return card_names[name]
    # 模糊匹配（忽略大小寫）
    name_lower = name.lower()
    for k, v in card_names.items():
        if k.lower() == name_lower:
            return v
    return name  # 查不到就回傳原文

# ========== AWR 計算 ==========
def calc_awr(w, l, t):
    """計算調整後勝率 (Adjusted Win Rate)"""
    total = w + l + t
    if total == 0:
        return 0.0
    return (w + AWR_OFFSET_WINS) / (total + AWR_OFFSET_TOTAL) * 100

def raw_wr(w, l, t):
    """原始勝率"""
    total = w + l + t
    if total == 0:
        return 0.0
    return w / total * 100

# ========== 解析 Limitless HTML ==========
def parse_limitless_html(html):
    """
    解析 Limitless TCG 的 decks page HTML
    回傳: [(牌組名, 使用率, W, L, T), ...]
    """
    results = []
    # 匹配模式: 名稱 /decks/xxx ... W-L-T / 分數
    pattern = r'<a[^>]+href="/decks/[^"]+"[^>]*>([^<]+)</a></td><td[^>]*>([0-9.,]+)%</td><td[^>]*>\[([0-9]+)\s*-\s*([0-9]+)\s*-\s*([0-9]+)\]</td><td[^>]*>'
    matches = re.findall(pattern, html)
    for name, share, w, l, t in matches:
        name = name.strip()
        share = float(share.replace(",", ""))
        results.append({
            "name": name,
            "usage": share,
            "w": int(w),
            "l": int(l),
            "t": int(t)
        })
    return results

# ========== 從快取讀取 ==========
def load_meta_cache(set_code="B4"):
    cache_path = META_CACHE.replace(".json", f"_{set_code}.json")
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def save_meta_cache(data, set_code="B4"):
    import os
    os.makedirs("memory", exist_ok=True)
    cache_path = META_CACHE.replace(".json", f"_{set_code}.json")
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== 抓取網頁 ==========
def fetch_limitless(url):
    """用 curl 抓取 Limitless TCG 頁面"""
    import subprocess
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", url],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout
    except Exception as e:
        print(f"[ERROR] curl failed: {e}", file=sys.stderr)
        return None

# ========== Meta 表格生成 ==========
def generate_meta_table(decks, dd, top_n=20):
    """
    生成 Meta 排名表格
    """
    # 計算總使用率
    total_usage = sum(d["usage"] for d in decks)

    # 計算 AWR 並排序
    for d in decks:
        d["total"] = d["w"] + d["l"] + d["t"]
        d["awr"] = calc_awr(d["w"], d["l"], d["t"])
        d["raw_wr"] = raw_wr(d["w"], d["l"], d["t"])
        d["share"] = d["usage"] / total_usage * 100
        d["zh"] = translate(d["name"], dd)

    decks.sort(key=lambda x: x["awr"], reverse=True)

    # 輸出
    lines = []
    lines.append("=" * 90)
    lines.append(f"{'Rank':<5} {'牌組':<35} {'AWR%':>8} {'Raw%':>7} {'樣本':>7} {'使用率%':>8} {'W-L-T'}")
    lines.append("=" * 90)
    for i, d in enumerate(decks[:top_n], 1):
        lines.append(
            f"{i:<5} {d['zh']:<35} {d['awr']:>7.2f}% {d['raw_wr']:>6.1f}% "
            f"{d['total']:>6d}  {d['share']:>7.2f}%  {d['w']}-{d['l']}-{d['t']}"
        )
    lines.append("=" * 90)
    return "\n".join(lines)

# ========== 強度分級 ==========
def generate_tier(decks, dd, top_n=20):
    """生成強度分級報告"""
    tier_lines = []
    tier_lines.append("\n【強度分級】\n")

    # 分級
    if len(decks) >= 1:
        top_awr = decks[0]["awr"]

        t0 = [d for d in decks if d["awr"] >= top_awr - 1.0]
        t1 = [d for d in decks if top_awr - 1.0 > d["awr"] >= 51.0]
        t2 = [d for d in decks if 51.0 > d["awr"] >= 48.0]
        t3 = [d for d in decks if d["awr"] < 48.0]

        def fmt(d):
            return f"{d['zh']} ({d['awr']:.2f}%)"

        if t0:
            tier_lines.append(f"T0: {', '.join(fmt(d) for d in t0[:5])}")
        if t1:
            tier_lines.append(f"T1: {', '.join(fmt(d) for d in t1[:8])}")
        if t2:
            tier_lines.append(f"T2: {', '.join(fmt(d) for d in t2[:8])}")
        if t3:
            tier_lines.append(f"T3: {', '.join(fmt(d) for d in t3[:5])}")

    return "\n".join(tier_lines)

# ========== 卡表翻譯查詢 ==========
def translate_card_list(cards, dd):
    """
    翻譯卡表（卡片名稱列表）
    cards: [("CardName", count), ...]
    """
    lines = []
    for name, count in cards:
        zh = translate(name, dd)
        lines.append(f"  {zh:<30} ×{count}")
    return "\n".join(lines)

# ========== 內建牌組卡表資料庫 ==========
DECK_DATABASES = {
    "vespiquen_ex_shuckle_ex": {
        "name": "Vespiquen ex Shuckle ex",
        "zh": "蜂女王 ex 壺壺 ex",
        "pokemon": [
            ("Vespiquen", 1),
            ("Shuckle ex", 2),
            ("Teal Mask Ogerpon ex", 1),
            ("Combee", 2),
            ("Vespiquen ex", 2),
        ],
        "trainer": [
            ("Cyrus", 1),
            ("Leaf Cape", 2),
            ("Copycat", 2),
            ("Field Blower", 2),
            ("Fragrant Forest", 2),
            ("X Speed", 1),
            ("Professor's Research", 2),
        ],
        "energy": [("Grass Energy", 4)],
        "packs": {
            "A2": [("Vespiquen", 1), ("Cyrus", 1)],
            "A3": [("Leaf Cape", 2)],
            "A4": [("Shuckle ex", 2)],
            "B1": [("Copycat", 2)],
            "A2b": [("Teal Mask Ogerpon ex", 1)],
            "B3": [("Field Blower", 2), ("Fragrant Forest", 2)],
            "B4": [("Combee", 2), ("Vespiquen ex", 2)],
            "P-A": [("X Speed", 1), ("Professor's Research", 2)],
        }
    },
    "hoopa_ex_mega_absol_ex": {
        "name": "Hoopa ex Mega Absol ex",
        "zh": "胡帕 ex 超級阿勃梭魯 ex",
        "pokemon": [
            ("Hoopa ex", 2),
            ("Mega Absol ex", 2),
            ("Hydreigon", 2),
        ],
        "trainer": [
            ("Professor's Research", 4),
            ("Copycat", 2),
            ("Pokemon Center Ladies", 2),
        ],
        "energy": [
            ("Dark Energy", 4),
        ],
        "packs": {}
    }
}

# ========== 主程式 ==========
def main():
    parser = argparse.ArgumentParser(description="PTCGP Meta 表格生成器")
    parser.add_argument("--set", "-s", default="B4", help="擴展代碼 (預設 B4)")
    parser.add_argument("--top", "-n", type=int, default=20, help="顯示前N名 (預設 20)")
    parser.add_argument("--url", "-u", default=None, help="自訂 Limitless URL")
    parser.add_argument("--deck", "-d", default=None, help="顯示牌組卡表 (如 vespiquen_ex_shuckle_ex)")
    parser.add_argument("--cache", action="store_true", help="使用快取資料")
    args = parser.parse_args()

    dd = load_dict()

    # 牌組卡表模式
    if args.deck:
        deck_key = args.deck.lower()
        if deck_key in DECK_DATABASES:
            deck = DECK_DATABASES[deck_key]
            print(f"\n{'=' * 50}")
            print(f"牌組: {deck['zh']}")
            print(f"{'=' * 50}")

            print("\n【寶可夢】")
            print(translate_card_list(deck["pokemon"], dd))

            if deck["trainer"]:
                print("\n【訓練家】")
                print(translate_card_list(deck["trainer"], dd))

            if deck["energy"]:
                print("\n【能量】")
                print(translate_card_list(deck["energy"], dd))

            if deck["packs"]:
                print("\n【所需卡包】")
                for pack, cards in deck["packs"].items():
                    zh_cards = ", ".join(f"{translate(c[0], dd)} ×{c[1]}" for c in cards)
                    print(f"  {pack}: {zh_cards}")
        else:
            print(f"[ERROR] 找不到牌組: {args.deck}")
            print(f"可用牌組: {', '.join(DECK_DATABASES.keys())}")
        return

    # Meta 表格模式
    if args.cache:
        data = load_meta_cache(args.set)
        if data:
            decks = data
        else:
            print("[ERROR] 無快取資料，請先不用 --cache 抓取")
            return
    else:
        url = args.url or f"https://play.limitlesstcg.com/decks?game=pocket&set={args.set}"
        print(f"[INFO] 抓取: {url}", file=sys.stderr)
        html = fetch_limitless(url)
        if not html:
            print("[ERROR] 無法取得網頁內容", file=sys.stderr)
            return
        decks = parse_limitless_html(html)
        if not decks:
            print("[WARNING] 無法解析 HTML，可能需要登入或 JS 載入", file=sys.stderr)
            return
        save_meta_cache(decks, args.set)

    print(f"[INFO] 共取得 {len(decks)} 個牌組", file=sys.stderr)
    print()
    print(f"📊 PTCGP {args.set} Meta — {datetime.now().strftime('%Y-%m-%d')}")
    print()
    print(generate_meta_table(decks, dd, top_n=args.top))
    print(generate_tier(decks, dd, top_n=args.top))

if __name__ == "__main__":
    main()
