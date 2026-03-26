#!/usr/bin/env python3
"""Fetch card data from Limitless TCG efficiently using concurrent requests."""

import asyncio
import aiohttp
import json
import re
from pathlib import Path

SETS = ['A1', 'A1a', 'A2', 'A2a', 'A2b', 'A3', 'A3a', 'A3b', 'A4', 'A4a', 'A4b', 
        'B1', 'B1a', 'B2', 'B2a', 'P-A', 'P-B']

async def fetch_card(session, set_code, card_num):
    """Fetch single card data."""
    url = f"https://pocket.limitlesstcg.com/cards/{set_code}/{card_num}"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                text = await resp.text()
                # Extract name from title
                match = re.search(r'<title>([^•]+)', text)
                name = match.group(1).strip() if match else f"Unknown_{card_num}"
                return {'number': card_num, 'name': name, 'set': set_code}
    except Exception as e:
        print(f"Error fetching {set_code}/{card_num}: {e}")
    return None

async def fetch_set(set_code, max_cards=500):
    """Fetch all cards in a set."""
    print(f"Fetching {set_code}...")
    
    # First get total cards
    async with aiohttp.ClientSession() as session:
        url = f"https://pocket.limitlesstcg.com/cards/{set_code}"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            text = await resp.text()
            cards = re.findall(rf'{set_code}_(\d+)_EN_SM', text)
            if not cards:
                print(f"No cards found for {set_code}")
                return []
            total = len(cards)
            max_num = max(int(c) for c in cards)
            print(f"  Found {max_num} cards")
            
    # Fetch all cards concurrently (limit to 50 parallel)
    semaphore = asyncio.Semaphore(30)
    
    async def fetch_with_sem(session, num):
        async with semaphore:
            await asyncio.sleep(0.05)  # Rate limiting
            return await fetch_card(session, set_code, num)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_sem(session, i) for i in range(1, max_num + 1)]
        results = await asyncio.gather(*tasks)
        
    cards = [r for r in results if r]
    print(f"  Got {len(cards)} cards")
    return cards

async def main():
    all_cards = {}
    for set_code in SETS:
        cards = await fetch_set(set_code)
        all_cards[set_code] = cards
        await asyncio.sleep(1)  # Delay between sets
    
    # Save to file
    output = {}
    for set_code, cards in all_cards.items():
        for card in cards:
            key = f"{set_code}_{card['number']:03d}"
            output[key] = {'name': card['name'], 'set': set_code, 'number': card['number']}
    
    Path('memory').mkdir(exist_ok=True)
    with open('memory/ptcgp_card_names.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal cards saved: {len(output)}")
    print("Saved to memory/ptcgp_card_names.json")

if __name__ == '__main__':
    asyncio.run(main())
