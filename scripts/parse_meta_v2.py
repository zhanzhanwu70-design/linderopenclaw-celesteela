#!/usr/bin/env python3
import re
import json
from datetime import datetime

with open('memory/ptcgp_raw_latest.html', 'r') as f:
    html = f.read()

# Find ALL rows with data-share
row_pattern = r'<tr[^>]+data-share="([^"]+)"[^>]+data-winrate="([^"]+)"[^>]*>(.*?)</tr>'
rows = re.findall(row_pattern, html, re.DOTALL)

decks = []
for share_str, winrate_str, row_content in rows:
    share = float(share_str)
    try:
        winrate = float(winrate_str) if winrate_str != 'null' else 0
    except:
        winrate = 0
    
    if share < 0.005:  # Skip below 0.5%
        continue
    
    # Extract all tds
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row_content)
    
    if len(tds) < 5:
        continue
    
    # td[0] = rank, td[2] = deck name, td[3] = count, td[4] = share%, td[5] = record, td[6] = win%
    rank_str = re.sub(r'<[^>]+>', '', tds[0]).strip()
    try:
        rank = int(rank_str)
    except:
        rank = 0
    
    # Deck name
    name_match = re.search(r'<a href="/decks/[^"]+">([^<]+)</a>', tds[2])
    name = name_match.group(1) if name_match else '?'
    
    # Count
    try:
        count = int(re.sub(r'<[^>]+>', '', tds[3]).strip())
    except:
        count = 0
    
    # Share (already have as float)
    share_pct = re.sub(r'<[^>]+>', '', tds[4]).strip()
    
    # Record
    record_text = re.sub(r'<[^>]+>', '', tds[5]).strip() if len(tds) > 5 else '?'
    
    # Win rate from display
    wr_display = re.sub(r'<[^>]+>', '', tds[6]).strip() if len(tds) > 6 else f'{winrate*100:.2f}'
    
    # Parse record
    adj_wr = 0
    w, d, l, total = 0, 0, 0, 0
    if record_text != '?' and '-' in record_text:
        parts = record_text.split('-')
        if len(parts) == 3:
            try:
                w = int(parts[0].strip())
                d = int(parts[1].strip())
                l = int(parts[2].strip())
                total = w + d + l
                adj_wr = (w + 12) / (total + 25) if total > 0 else 0
            except:
                pass
    
    decks.append({
        'rank': rank,
        'name': name,
        'count': count,
        'share': share,
        'share_pct': share_pct,
        'win_rate': wr_display,
        'adjusted_wr': f'{adj_wr*100:.2f}%',
        'record': record_text,
        'w': w, 'd': d, 'l': l, 'total': total
    })

# Sort by share descending
decks.sort(key=lambda x: x['share'], reverse=True)

# Save to file
output = {
    'date': datetime.utcnow().strftime('%Y-%m-%d'),
    'source': 'Limitless TCG (B2a Paldean Wonders)',
    'decks': decks[:30]
}
with open('memory/ptcgp_meta_latest.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(json.dumps(decks[:20], indent=2, ensure_ascii=False))
