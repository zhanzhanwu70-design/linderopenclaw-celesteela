#!/usr/bin/env python3
"""Fetch C1 (Dual Fusion) card data from pocket.limitlesstcg.com -> memory/ptcgp_cards_c1.json"""

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

SET = "C1"
BASE = f"https://pocket.limitlesstcg.com/cards/{SET}"
OUT = Path("memory/ptcgp_cards_c1.json")

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", s).strip()


def fetch_card(num, session, retries=3):
    url = f"{BASE}/{num}"
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=20)
            if r.status_code == 200:
                return parse(html=r.text, num=num)
        except Exception:
            pass
        time.sleep(1.2 * (attempt + 1))
    return {"set": SET, "number": num, "name": "", "type": "", "hp": 0, "weakness": "", "retreat": 0, "attacks": []}


def parse(html, num):
    card = {
        "set": SET,
        "number": num,
        "name": "",
        "type": "",
        "hp": 0,
        "weakness": "",
        "retreat": 0,
        "attacks": [],
    }

    m = re.search(r'<span class="card-text-name"><a[^>]*>([^<]+)</a>', html)
    if m:
        card["name"] = m.group(1).strip()

    # title: - Grass   - 70 HP
    t = re.search(r'card-text-title">(.*?)</p>', html, re.S)
    if t:
        seg = t.group(1)
        mt = re.search(r"-\s*([A-Za-z]+)\s*-\s*(\d+)\s*HP", seg)
        if mt:
            card["type"] = mt.group(1).strip()
            card["hp"] = int(mt.group(2))

    # subtype: Pokemon - Basic / Stage 1 / Trainer - Item
    st = re.search(r'class="card-text-type">(.*?)</p>', html, re.S)
    if st:
        seg = clean(st.group(1))
        card["stage"] = seg

    # attacks
    attacks = []
    for blk in re.findall(r'<div class="card-text-attack">(.*?)</div>', html, re.S):
        info = re.search(r'class="card-text-attack-info">(.*?)</p>', blk, re.S)
        eff = re.search(r'class="card-text-attack-effect">(.*?)</p>', blk, re.S)
        cost = ""
        name = ""
        dmg = None
        if info:
            seg = info.group(1)
            cs = re.search(r'<span class="ptcg-symbol">([^<]*)</span>', seg)
            if cs:
                cost = cs.group(1).strip()
            rest = re.sub(r'<span class="ptcg-symbol">[^<]*</span>', " ", seg)
            rest = clean(rest)
            md = re.search(r"(\d+)\s*$", rest)
            if md:
                dmg = int(md.group(1))
                rest = rest[: md.start()].strip()
            name = rest
        attacks.append({
            "cost": cost,
            "name": name,
            "damage": dmg,
            "effect": clean(eff.group(1)) if eff else "",
        })
    if attacks:
        card["attacks"] = attacks
        card["attack_costs"] = [a["cost"] for a in attacks]

    # ability
    ab = re.search(r'<div class="card-text-ability">(.*?)</div>', html, re.S)
    if ab:
        seg = ab.group(1)
        nm = re.search(r'class="card-text-ability-info">(.*?)</p>', seg, re.S)
        ef = re.search(r'class="card-text-ability-effect">(.*?)</p>', seg, re.S)
        card["ability"] = clean(nm.group(1)).replace("Ability:", "").strip() if nm else ""
        card["ability_effect"] = clean(ef.group(1)) if ef else ""

    wrr = re.search(r'class="card-text-wrr">(.*?)</p>', html, re.S)
    if wrr:
        seg = wrr.group(1)
        mw = re.search(r"Weakness:\s*([A-Za-z]+)", seg)
        mr = re.search(r"Retreat:\s*(\d+)", seg)
        if mw:
            card["weakness"] = mw.group(1).strip()
        if mr:
            card["retreat"] = int(mr.group(1))

    # trainer/other card type e.g. "Trainer - Item"
    if not card["type"] and "card-text-type" in html:
        seg = clean(re.search(r'class="card-text-type">(.*?)</p>', html, re.S).group(1))
        if "Trainer" in seg:
            card["type"] = "Trainer"
    return card


def main():
    sess = requests.Session()
    sess.headers.update(HEADERS)

    # set page -> count
    html = sess.get(BASE, timeout=30).text
    nums = sorted({int(x) for x in re.findall(rf"{SET}_(\d+)_EN_SM", html)})
    print(f"set page cards: {len(nums)} (max {max(nums) if nums else 0})", flush=True)
    targets = list(range(1, (max(nums) if nums else 0) + 1))

    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch_card, n, sess): n for n in targets}
        done = 0
        for f in futs:
            pass
        from concurrent.futures import as_completed
        for f in as_completed(futs):
            c = f.result()
            results.append(c)
            done += 1
            if done % 20 == 0:
                print(f"  {done}/{len(targets)}", flush=True)

    results.sort(key=lambda c: c["number"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    named = sum(1 for c in results if c["name"])
    with_att = sum(1 for c in results if c.get("attacks"))
    print(f"saved {len(results)} cards to {OUT} | named={named} with_attacks={with_att}")
    miss = [c["number"] for c in results if not c["name"]]
    if miss:
        print("missing names:", miss)


if __name__ == "__main__":
    main()
