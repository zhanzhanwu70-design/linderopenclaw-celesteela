#!/usr/bin/env python3
"""
分析 cards 目錄中的卡圖
分析目錄中的所有圖片，輸出卡牌資訊
"""

import os
import json
from pathlib import Path

CARDS_DIR = Path(__file__).parent.parent / "cards" / "manual"

def list_cards():
    """列出所有卡圖"""
    if not CARDS_DIR.exists():
        print(f"目錄不存在: {CARDS_DIR}")
        return []
    
    cards = []
    for f in CARDS_DIR.iterdir():
        if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            cards.append({
                'filename': f.name,
                'path': str(f),
                'size': f.stat().st_size
            })
    
    print(f"找到 {len(cards)} 張卡圖")
    for card in cards:
        print(f"  - {card['filename']} ({card['size']/1024:.1f} KB)")
    
    return cards

if __name__ == "__main__":
    list_cards()
