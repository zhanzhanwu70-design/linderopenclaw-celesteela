#!/usr/bin/env python3
"""
PTCGP Card Text Energy Parser
Parses energy costs from card text field
"""

import re
import json
import sys

# Energy type mapping
ENERGY_MAP = {
    'R': 'fire',
    'D': 'darkness',
    'W': 'water',
    'G': 'grass',
    'L': 'lightning',
    'M': 'metal',
    'F': 'fighting',
    'P': 'psychic',
    'C': 'colorless'
}

def parse_energy_from_text(text, attack_name):
    """
    Extract energy cost from card text for a given attack name.
    
    The text format in "Card text:" section is:
    "... ENERGY_SEQ AttackName damage | effect..."
    e.g., "DDD DDD Hyper Ray 130 Discard..."
    
    Returns list of energy codes, e.g., ['D', 'D', 'D', 'D', 'D', 'D']
    """
    if not attack_name or not text:
        return []
    
    # Find the Card text section (after "| Card text:")
    card_text_idx = text.find('| Card text:')
    if card_text_idx == -1:
        # Fallback to full text but find LAST occurrence
        search_text = text
    else:
        # Search only in Card text section
        search_text = text[card_text_idx:]
    
    # Find the LAST occurrence of attack_name (in case it appears multiple times)
    idx = search_text.rfind(attack_name)
    if idx == -1:
        return []
    
    # Get the portion before the attack name
    before_attack = search_text[:idx].strip()
    
    # The energy sequence is the last space-separated token(s) right before attack name
    # Energy sequences look like "DDD", "DDD DDD", "RCC RCC", etc.
    # They consist ONLY of R, D, W, G, L, M, F, P, C and spaces
    
    # Split and get just the last 2 tokens (most energy sequences are 1-2 tokens)
    words = before_attack.split()
    if not words:
        return []
    
    # Check last 2 words - energy sequences should be pure energy codes
    energies = []
    for word in reversed(words[-2:]):
        # Remove spaces to check for energy codes
        cleaned = word.strip()
        # If word is ONLY energy letters (possibly with spaces), use it
        if re.match(r'^[RDWGLMFPC ]+$', cleaned):
            word_energies = re.findall(r'[RDWGLMFPC]', cleaned)
            energies = word_energies + energies
        elif energies:
            # We already found energies and hit a non-energy word
            break
    
    return energies

def parse_attack_cost(text, attack_name):
    """
    Full parser: extract energy cost and attack info from text.
    Returns dict with attack_name, cost (list), damage (str), effect (str or None)
    """
    import re
    
    # Find the Card text section
    card_text_idx = text.find('| Card text:')
    if card_text_idx != -1:
        search_text = text[card_text_idx:]
    else:
        search_text = text
    
    # Find the LAST occurrence of attack_name
    idx = search_text.rfind(attack_name)
    if idx == -1:
        return None
    
    # Extract energy sequence
    energies = parse_energy_from_text(text, attack_name)
    
    # Find damage number after attack name
    rest = search_text[idx:]
    # Pattern: AttackName DAMAGE or AttackName DAMAGE+
    m = re.search(r'\d+\+?\s', rest[len(attack_name):])
    damage = m.group().strip().rstrip('+') if m else None
    
    # Find effect if present (after damage)
    if m:
        effect_start = idx + len(attack_name) + len(m.group())
        effect_text = search_text[effect_start:].split('|')[0].strip()
        if effect_text.startswith('effect:'):
            effect_text = effect_text[7:].strip()
        elif effect_text.startswith('Card text:'):
            effect_text = None
        else:
            effect_text = None
    else:
        effect_text = None
    
    return {
        'attack_name': attack_name,
        'cost': energies,
        'damage': damage,
        'effect': effect_text
    }

if __name__ == '__main__':
    # Test with Hydreigon
    test_text = "ID: B1-157 | Name: Hydreigon | Category: pokemon | Type: darkness | HP: 150 | Stage: stage_2 | Evolves from: Zweilous | Weakness: grass | Retreat: 2 | Attack 1: Hyper Ray | cost: none | 130 damage | effect: Discard all Energy from this Pokémon. | Card text: Ability: Roar in Unison Once during your turn, you may take 2 [ Darkness D ] Energy from your Energy Zone and attach it to this Pokémon. If you do, do 30 damage to this Pokémon. DDD DDD Hyper Ray 130 Discard all Energy from this Pokémon. | Tags: darkness, stage_2 | Set: Mega Rising (B1) #157"
    
    result = parse_attack_cost(test_text, 'Hyper Ray')
    print("Hydreigon - Hyper Ray:")
    print(json.dumps(result, indent=2))
    
    # Test with Armarouge ex
    test_text2 = "ID: B2a-020 | Name: Armarouge ex | Category: pokemon | Type: fire | HP: 140 | Stage: stage_1 | Evolves from: Charcadet | Weakness: water | Retreat: 2 | Attack 1: Armor Cannon | cost: none | 120 damage | effect: Discard a [ R ] Energy from this Pokémo | Card text: RCC RCC Armor Cannon 120 Discard a [ R ] Energy from this Pokémon. | Tags: fire, stage_1 | Set: Paldean Wonders (B2a) #20"
    
    result2 = parse_attack_cost(test_text2, 'Armor Cannon')
    print("\nArmarouge ex - Armor Cannon:")
    print(json.dumps(result2, indent=2))
    
    # Test with Charmander (should have cost from structured field)
    test_text3 = "ID: A2b-008 | Name: Charmander | Category: pokemon | Type: fire | HP: 60 | Stage: basic | Weakness: water | Retreat: 1 | Attack 1: Combustion | cost: R | 20 damage | Tags: basic, fire | Set: Shining Revelry (A2b) #8"
    
    result3 = parse_attack_cost(test_text3, 'Combustion')
    print("\nCharmander - Combustion:")
    print(json.dumps(result3, indent=2))