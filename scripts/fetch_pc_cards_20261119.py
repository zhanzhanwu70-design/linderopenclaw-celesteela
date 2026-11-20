#!/usr/bin/env python3
"""2026-11-19 抓取並補入新系列 Promo-C (P-C) 卡牌到 memory/ptcgp_cards_full.json。
P-C #2 = Mega Mewtwo Y ex（170HP），今日首次出現在 Limitless 牌組列表。"""
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.insert(0, 'scripts')
from fetch_c1_cards import parse  # noqa: E402  重用既有解析器

SET = 'P-C'
BASE = f'https://pocket.limitlesstcg.com/cards/{SET}'
OUT = 'memory/ptcgp_cards_full.json'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
TOTAL = 13


def fetch(num, sess):
    url = f'{BASE}/{num}'
    for attempt in range(3):
        try:
            r = sess.get(url, timeout=25)
            if r.status_code == 200:
                return parse(r.text, num)
        except Exception:
            pass
        time.sleep(1.0 * (attempt + 1))
    return None


sess = requests.Session()
sess.headers.update(HEADERS)

cards = []
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(fetch, n, sess): n for n in range(1, TOTAL + 1)}
    for f in futs:
        c = f.result()
        if c:
            cards.append(c)
        else:
            print('  MISS', futs[f], file=sys.stderr)
cards.sort(key=lambda c: c['number'])
print('fetched', len(cards), '/', TOTAL)
for c in cards:
    print(f"  P-C_{c['number']:03d}  {c['name']:28} {c.get('type',''):22} HP={c.get('hp',0)}")

db = json.load(open(OUT, encoding='utf-8'))
added = []
for c in cards:
    key = f"{SET}_{c['number']:03d}"
    if key in db:
        continue
    c = dict(c)
    c['set'] = SET
    db[key] = c
    added.append(key)

json.dump(db, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('added to DB:', len(added), added)
print('total cards:', len(db))
