#!/usr/bin/env python3
"""2026-11-22 抓取前 24 名牌組 matchups 頁。"""
import json
import os
import time
import requests

HDR = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

rows = json.load(open('memory/ptcgp_meta_20261122_std.json'))['rows']
top = sorted(rows, key=lambda z: -z['share'])[:24]
outdir = 'memory/matchups_20261122'
os.makedirs(outdir, exist_ok=True)

failed = []
for r in top:
    slug = r['slug']
    url = f'https://play.limitlesstcg.com/decks/{slug}/matchups/?game=POCKET&format=standard&set=C1'
    path = os.path.join(outdir, slug + '.html')
    try:
        resp = requests.get(url, headers=HDR, timeout=45)
        if resp.status_code != 200:
            failed.append((slug, f'HTTP {resp.status_code}'))
            continue
        with open(path, 'w', encoding='utf-8') as f:
            f.write(resp.text)
        print(f'{slug:60} {resp.status_code} {len(resp.text):>7}')
    except Exception as e:
        failed.append((slug, str(e)))
        print(f'{slug:60} FAIL {e}')
    time.sleep(1.0)

print('fetched', len(top) - len(failed), '/', len(top))
if failed:
    raise SystemExit('matchup fetch failed: ' + repr(failed))
