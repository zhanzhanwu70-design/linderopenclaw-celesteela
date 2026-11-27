#!/usr/bin/env python3
"""2026-11-23 Limitless TCG 抓取（不使用 curl，用 requests）。"""
import os
import time
import requests

HDR = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

targets = [
    ('memory/ptcgp_raw_20261126_std.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard'),
    ('memory/ptcgp_raw_20261126_std_comb.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&combine=1'),
    ('memory/ptcgp_raw_20261126_C1.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&set=C1'),
    ('memory/ptcgp_raw_20261126_C1_comb.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&set=C1&combine=1'),
    ('memory/ptcgp_raw_20261126_B4a.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&set=B4a'),
]

failed = []
for path, url in targets:
    try:
        r = requests.get(url, headers=HDR, timeout=45)
        if r.status_code != 200:
            failed.append((path, f'HTTP {r.status_code}'))
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f'{path}  HTTP {r.status_code}  {len(r.text)} bytes')
    except Exception as e:
        failed.append((path, str(e)))
        print(f'{path}  FAIL: {e}')
    time.sleep(1.5)

if failed:
    raise SystemExit('fetch failed: ' + repr(failed))
