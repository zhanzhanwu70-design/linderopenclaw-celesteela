# SKILL.md - PTCGP 卡牌查詢

## 概述
透過卡牌編號或名稱快速查詢 PTCGP 卡牌資料。

## 資料位置
- **卡圖目錄**: `/home/node/.openclaw/workspace-celesteela/cards/`
- **完整資料庫**: `/home/node/.openclaw/workspace-celesteela/memory/ptcgp_cards_full.json`
- **編號→名稱**: `skills/ptcgp-card-lookup/number_to_name.json`
- **名稱→編號**: `skills/ptcgp-card-lookup/name_to_numbers.json`

## 卡牌編號格式
```
{SET}_{NUM}.webp

例如：
- A1_001.webp = Bulbasaur (Genetic Apex #1)
- B2a_042.webp = Bellibolt ex (Paldean Wonders #42)
- P-A_001.webp = Potion (Promo-A #1)
```

## 系列代碼對照
| 代碼 | 系列名稱 |
|------|----------|
| A1 | Genetic Apex |
| A1a | Mythical Island |
| A2 | Space-Time Smackdown |
| A2a | Triumphant Light |
| A2b | Shining Revelry |
| A3 | Celestial Guardians |
| A3a | Extradimensional Crisis |
| A3b | Eevee Grove |
| A4 | Wisdom of Sea and Sky |
| A4a | Secluded Springs |
| A4b | Deluxe Pack ex |
| B1 | Mega Rising |
| B1a | Crimson Blaze |
| B2 | Fantastical Parade |
| B2a | Paldean Wonders |
| P-A | Promo-A |
| P-B | Promo-B |

## 使用方式

### 1. Node.js 查詢
```javascript
const cards = require('/home/node/.openclaw/workspace-celesteela/memory/ptcgp_cards_full.json');
const num2name = require('/home/node/.openclaw/workspace-celesteela/skills/ptcgp-card-lookup/number_to_name.json');
const name2nums = require('/home/node/.openclaw/workspace-celesteela/skills/ptcgp-card-lookup/name_to_numbers.json');

// 查詢特定編號
const card = cards['A1_042'];

// 查詢編號對應名稱
const name = num2name['A1']['42'];

// 查詢某張卡的所有版本
const versions = name2nums['Charizard']; // ['A1_035', 'B1a_013', 'B1a_091']
```

### 2. 命令列查詢
```bash
node -e "const d=require('./memory/ptcgp_cards_full.json'); console.log(JSON.stringify(d['A1_042'], null, 2))"
```

## 資料庫欄位
每張卡的資料：
- `name`: 英文名稱
- `set`: 系列代碼
- `number`: 編號
- `type`: 能量屬性（Grass, Fire, Water, Lightning, Psychic, Fighting, Darkness, Metal, Dragon, Colorless）
- `hp`: HP 值
- `weakness`: 弱點屬性
- `retreat`: 退場能量
- `attacks`: 攻擊所需能量（陣列）

## 卡圖路徑
```
cards/{SET}/{SET}_{NUM}.webp

例如：cards/A1/A1_001.webp
```

## OCR 流程建議
1. 先用 OCR 辨識卡名（英文）
2. 用 name_to_numbers.json 找出所有同名卡版本
3. 再用影像辨識確認正確版本（同一張卡可能有不同插圖/閃卡）
4. 用編號精準查詢資料庫

## 總卡數
- 卡圖：2921 張
- 資料庫：2916 筆
- 獨立卡名：1125 種
