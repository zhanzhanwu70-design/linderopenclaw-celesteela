import requests
from bs4 import BeautifulSoup
import json
import re

def fetch_meta():
    url = "https://play.limitlesstcg.com/decks?game=POCKET"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find deck cards
        deck_cards = soup.find_all('div', class_='deck-card')
        
        decks = []
        for i, card in enumerate(deck_cards[:50]):
            try:
                name_elem = card.find('a')
                stats_elem = card.find_all('span')
                
                name = name_elem.text.strip() if name_elem else "Unknown"
                
                # Extract stats from text
                card_text = card.get_text()
                
                # Parse usage rate
                usage_match = re.search(r'([\d.]+)%', card_text)
                usage = usage_match.group(1) + "%" if usage_match else "0%"
                
                # Parse win rate
                win_match = re.search(r'([\d.]+)%.*?(\d+)\s*-\s*(\d+)', card_text)
                if win_match:
                    win_rate = win_match.group(1) + "%"
                    wins = int(win_match.group(2))
                    losses = int(win_match.group(3))
                    record = f"{wins} - {losses}"
                else:
                    win_rate = "0%"
                    record = "0 - 0"
                
                # Calculate adjusted win rate (Bayesian smoothing)
                prior_games = 25
                prior_wins = 12
                if wins + losses > 0:
                    adjusted = (wins + prior_wins) / (wins + losses + prior_games)
                    adjusted_win_rate = f"{adjusted*100:.2f}%"
                else:
                    adjusted_win_rate = "0%"
                
                deck = {
                    "rank": i + 1,
                    "name": name,
                    "usage_rate": usage,
                    "win_rate": win_rate,
                    "record": record,
                    "adjusted_win_rate": adjusted_win_rate,
                    "sample_size": wins + losses
                }
                decks.append(deck)
                
            except Exception as e:
                continue
        
        # Save to file
        result = {
            "update_time": "2026-03-14 12:00",
            "top_decks": decks
        }
        
        with open('/home/node/.openclaw/workspace/memory/ptcgp_meta.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {len(decks)} decks")
        return decks
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    fetch_meta()
