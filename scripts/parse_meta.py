#!/usr/bin/env python3
import json
import re
import subprocess

# Fetch the page
result = subprocess.run(
    ['curl', '-s', 'https://play.limitlesstcg.com/decks?game=POCKET&format=standard'],
    capture_output=True, text=True
)
html = result.stdout

# Extract deck data using regex
pattern = r'<tr[^>]*data-share="([^"]+)"[^>]*data-winrate="([^"]+)"[^>]*>.*?<td>(\d+)</td>.*?<a[^>]*>([^<]+)</a>.*?<td class="landscape-only">(\d+)</td>.*?<td[^>]*>([0-9.-]+%)</td>'
matches = re.findall(pattern, html, re.DOTALL)

# Prior for Bayesian adjustment (from existing config)
prior_games = 25
prior_wins = 12

decks = []
for i, match in enumerate(matches[:50]):
    data_share, data_winrate, rank, name, sample_str, usage = match
    
    # Convert sample size
    sample = int(sample_str)
    
    # Calculate win rate from sample and data-winrate
    raw_winrate = float(data_winrate)
    wins = int(raw_winrate * sample)
    losses = sample - wins
    draws = 0  # Not directly available
    
    # Calculate adjusted win rate (Bayesian)
    adjusted_wins = wins + prior_wins
    adjusted_games = sample + prior_games
    adjusted_winrate = adjusted_wins / adjusted_games
    
    usage_pct = float(data_share) * 100
    
    deck = {
        "rank": int(rank),
        "name": name.strip(),
        "pokemon": [],
        "usage_rate": f"{usage_pct:.2f}%",
        "win_rate": f"{raw_winrate * 100:.2f}%",
        "record": f"{wins} - {losses} - {draws}",
        "adjusted_win_rate": f"{adjusted_winrate * 100:.2f}%",
        "sample_size": sample
    }
    decks.append(deck)

# Calculate analysis
# Get top 5 by adjusted win rate (with minimum sample size of 20)
strong_decks = sorted(
    [d for d in decks if d["sample_size"] >= 20],
    key=lambda x: float(x["adjusted_win_rate"].replace("%", "")),
    reverse=True
)[:5]

strong_deck_names = [
    f"{d['name']}(调整后{d['adjusted_win_rate']}%/原始{d['win_rate']}%)"
    for d in strong_decks
]

analysis = {
    "trends": [],
    "strong_decks": strong_deck_names,
    "meta_insight": f"调整后最强牌组: {strong_decks[0]['name']} (调整后胜率{strong_decks[0]['adjusted_win_rate']}, 原始{strong_decks[0]['win_rate']}, 样本{strong_decks[0]['sample_size']}场)" if strong_decks else "数据不足",
    "settings": {
        "prior_games": prior_games,
        "prior_wins": prior_wins,
        "prior_win_rate": f"{prior_wins/prior_games*100:.0f}%"
    },
    "filtered_count": len([d for d in decks if d["sample_size"] >= 20])
}

# Create output
output = {
    "update_time": "2026-03-10 12:13",
    "top_decks": decks,
    "analysis": analysis
}

# Save JSON
with open('/home/node/.openclaw/workspace/memory/ptcgp_meta.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Updated {len(decks)} decks")
