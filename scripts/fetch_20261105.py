#!/usr/bin/env python3
"""2026-11-05 Limitless TCG 抓取（不使用 curl，用 requests）"""
import requests, os, time

HDR = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

targets = [
    ('memory/ptcgp_raw_20261105_std.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard'),
    ('memory/ptcgp_raw_20261105_std_comb.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&combine=1'),
    ('memory/ptcgp_raw_20261105_C1.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&set=C1'),
    ('memory/ptcgp_raw_20261105_C1_comb.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&set=C1&combine=1'),
    ('memory/ptcgp_raw_20261105_B4a.html', 'https://play.limitlesstcg.com/decks?game=pocket&format=standard&set=B4a'),
]

for path, url in targets:
    try:
        r = requests.get(url, headers=HDR, timeout=45)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f'{path}  HTTP {r.status_code}  {len(r.text)} bytes')
    except Exception as e:
        print(f'{path}  FAIL: {e}')
    time.sleep(1.5)
