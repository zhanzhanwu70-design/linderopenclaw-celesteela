#!/usr/bin/env python3
"""
PTCGP Meta 分析 - 計算調整後勝率
公式: 調整後勝率 = (勝場 + 12) / (總場 + 25)
"""

PRIOR_WINS = 12
PRIOR_GAMES = 25

decks_raw = [
    (1, "Suicune ex Baxcalibur", 1635, 13.22, 4480, 4248, 187, 50.25),
    (2, "Mega Altaria ex Greninja", 1433, 11.59, 4110, 3684, 202, 51.40),
    (3, "Magnezone Bellibolt ex", 1076, 8.70, 3158, 2789, 157, 51.74),
    (4, "Bellibolt ex Zeraora", 783, 6.33, 2134, 1954, 103, 50.92),
    (5, "Greninja Mega Absol ex", 737, 5.96, 2114, 1862, 92, 51.97),
    (6, "Hydreigon Mega Absol ex", 693, 5.60, 1961, 1807, 82, 50.94),
    (7, "Mega Altaria ex Gourgeist", 652, 5.27, 1961, 1581, 116, 53.61),
    (8, "Mega Altaria ex Chingling", 233, 1.88, 615, 571, 40, 50.16),
    (9, "Meowscarada ex Meowscarada", 209, 1.69, 401, 543, 9, 42.08),
    (10, "Mega Lopunny ex Annihilape", 194, 1.57, 401, 529, 8, 42.75),
]

def calc_adj_wr(wins, losses, draws=0):
    total = wins + losses + draws
    return (wins + PRIOR_WINS) / (total + PRIOR_GAMES) * 100

print("=" * 60)
print("Pokemon TCG Pocket Meta 分析 | 2026-03-21")
print("=" * 60)

print("\n🔥 使用率 Top 10")
print("-" * 50)
for rank, name, count, share, w, l, d, raw_wr in decks_raw[:10]:
    print(f"{rank:2}. {name}")
    print(f"    牌組數: {count} | 佔有率: {share}%")

print("\n⚡ 調整後勝率 Top 10 (Bayesian 公式)")
print("-" * 50)
print("公式: (勝場 + 12) / (總場 + 25)")
print()

# 計算並排序
decks_with_adj = []
for rank, name, count, share, w, l, d, raw_wr in decks_raw:
    total = w + l + d
    adj_wr = calc_adj_wr(w, l, d)
    decks_with_adj.append((adj_wr, name, raw_wr, w, l, d, total))

# 依調整後勝率排序 (高到低)
decks_sorted = sorted(decks_with_adj, key=lambda x: x[0], reverse=True)

for i, (adj_wr, name, raw_wr, w, l, d, total) in enumerate(decks_sorted[:10], 1):
    print(f"{i:2}. {name}")
    print(f"    調整後: {adj_wr:.2f}% (原始: {raw_wr:.2f}%)")
    print(f"    戰績: {w}-{l}-{d} (共{total}場)")
