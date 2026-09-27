---
name: "ptcgp-tw-translation"
description: "PTCGP 台灣繁體中文卡包名稱翻譯字典維護。新擴充發布或翻譯錯誤被指出時用。"
---

# PTCGP 台灣繁體中文翻譯字典維護

## 觸發條件
- 新擴充發布時（PTCG Pocket 約每 1-1.5 月推一個擴充包）
- 用戶要求「查官方翻譯」、「查台灣版本」、「更新字典」
- 卡包或卡片名稱翻譯錯誤被指出時

## 核心權威來源
1. **Pokemon Hubs**（pokemonhubs.com）— 台港最大寶可夢繁中資訊站，最權威
2. **Bahamut 巴哈姆特**（forum.gamer.com.tw）— 台灣最大電玩社群 PTCGP 哈啦板

搜尋範本：`PTCG Pocket [English Name] 卡包名 繁體中文`

## 標準作業流程

### 1. 確認擴充代碼與英文名
   - 從 Limitless TCG Pocket 或 GitHub flibustier/pokemon-tcg-pocket-database 取得英文名稱

### 2. 多源驗證台版名稱
   - 用 `web_search` 對 Pokemon Hubs + Bahamut 各查一次
   - 兩個來源都出現相同中文名才算確認
   - 找不到時：試搜 Bahamut 全文、Reddit r/PTCGP 中文討論

### 3. 更新字典 `ptcgp_deck_dictionary.json`
   必須新增/更新兩個區塊：

```json
{
  "set_names": {
    "Mega Rising": "超級堀起"
  },
  "set_short_names": {
    "B1": "超級堀起"
  },
  "card_names": {
    "<English Pack Name>": "<台版中文>"
  }
}
```

`set_names` 用英文鍵，`set_short_names` 用 B 代碼鍵。

### 4. 常見誤譯陷阱
- `堀`（不是 `崛`）— B1 Mega Rising 官方用字
- `帕底亞`（不是 `帕底`）— B2a Paldean Wonders
- `紅蓮`（不是 `深紅`）— B1a Crimson Blaze
- `天空主宰`（不是 `天空之主`）— B4 Ruler of the Skies

### 5. 驗證步驟
   - 執行 `python3 scripts/ptcgp_meta.py -d <deck_key>` 確認翻譯正確
   - 用 grep 確認字典中已包含新對照

## 已知 B 系列台版字典（已建）
```
B1   Mega Rising         → 超級堀起
B1a  Crimson Blaze       → 紅蓮烈焰
B2   Fantastical Parade  → 幻夢遊行
B2a  Paldean Wonders     → 帕底亞驚奇
B2b  Mega Shine          → 超級異彩
B3   Pulsing Aura        → 波導奏動
B3a  Paradox Drive       → 進擊悖謬
B3b  Everyday Wonders    → 奇跡日常
B4   Ruler of the Skies  → 天空主宰
B4a  Team Rocket's Ambition → 火箭隊的野心
```

## 輸出回報格式
簡短確認 + 對照表，標記修正項。

## 工具依賴
- `ptcgp_deck_dictionary.json`
- `web_search`
- `scripts/ptcgp_meta.py`（驗證用）
