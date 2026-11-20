#!/usr/bin/env python3
"""2026-11-19 補齊缺漏的 B3 系列（工作區說明有 B3，但本地卡庫缺失）。"""
import json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
import requests
sys.path.insert(0, 'scripts')
from fetch_c1_cards import parse

SET='B3'; BASE=f'https://pocket.limitlesstcg.com/cards/{SET}'
OUT='memory/ptcgp_cards_full.json'
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
s=requests.Session(); s.headers.update(H)
html=s.get(BASE,timeout=30).text
nums=sorted({int(x) for x in re.findall(rf"{SET}_(\d+)_EN_SM", html)})
print('B3 cards on Limitless:',len(nums),'max',max(nums) if nums else 0,flush=True)
def fetch(n):
    for a in range(3):
        try:
            r=s.get(f'{BASE}/{n}',timeout=25)
            if r.status_code==200: return parse(r.text,n)
        except Exception: pass
        time.sleep(0.8*(a+1))
    return None
cards=[]
with ThreadPoolExecutor(max_workers=8) as ex:
    for c in ex.map(fetch, nums):
        if c: cards.append(c)
cards.sort(key=lambda c:c['number'])
print('fetched',len(cards))
db=json.load(open(OUT,encoding='utf-8'))
added=0
for c in cards:
    k=f"{SET}_{c['number']:03d}"
    if k in db: continue
    c=dict(c); c['set']=SET; db[k]=c; added+=1
json.dump(db,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('added',added,'total',len(db))
