import json, requests, os, time, re

HDR = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

rows = json.load(open('memory/ptcgp_meta_20261105_std.json'))['rows']
top = sorted(rows, key=lambda z: -z['share'])[:24]

outdir = 'memory/matchups_20261105'
os.makedirs(outdir, exist_ok=True)

ok = 0
for r in top:
    slug = r['slug']
    url = f'https://play.limitlesstcg.com/decks/{slug}/matchups/?game=POCKET&format=standard&set=C1'
    path = os.path.join(outdir, slug + '.html')
    try:
        resp = requests.get(url, headers=HDR, timeout=45)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(resp.text)
        ok += 1
        print(f'{slug:60} {resp.status_code} {len(resp.text):>7}')
    except Exception as e:
        print(f'{slug:60} FAIL {e}')
    time.sleep(1.2)
print('fetched', ok, '/', len(top))
