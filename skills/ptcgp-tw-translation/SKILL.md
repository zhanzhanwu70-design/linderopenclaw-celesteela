---
name: "ptcgp-tw-translation"
description: "查 PTCGP 台版卡包/卡片中文名、更新翻譯字典時用。新擴充發布或翻譯錯誤被指出時觸發。"
---

# PTCGP 台灣繁體中文翻譯字典維護

## 觸發條件
- 新擴充發布（PTCG Pocket 約每 1–1.5 個月推一個擴充包）
- 使用者要求「查官方翻譯」「查台灣版本」「更新字典」
- 卡包或卡片名稱翻譯錯誤被指出

## 來源
- 英文卡包名與代碼：Limitless TCG Pocket，或 GitHub `flibustier/pokemon-tcg-pocket-database`
- 台版中文名：Pokemon Hubs（pokemonhubs.com）、Bahamut（forum.gamer.com.tw）PTCGP 哈啦板
- 搜尋範本：`PTCG Pocket [English Name] 卡包名 繁體中文`

## 步驟

1. 讀 `ptcgp_deck_dictionary.json` 取得既有對照與 B 代碼，避免重複鍵或漏改。
2. 確認新擴充的英文名與代碼後，用 `web_search` 對 Pokemon Hubs 與 Bahamut 各查一次台版中文名；兩個來源出現相同名稱才算確認。查不到時改搜 Bahamut 全文或 Reddit r/PTCGP 中文討論。
3. 更新 `ptcgp_deck_dictionary.json`：`set_names` 用英文鍵、`set_short_names` 用 B 代碼鍵、`card_names` 用英文卡片名鍵。

```json
{
  "set_names": { "Mega Rising": "超級堀起" },
  "set_short_names": { "B1": "超級堀起" },
  "card_names": { "<English Pack Name>": "<台版中文>" }
}
```

4. 逐字核對易錯字：`堀`（非 `崛`）、`帕底亞`（非 `帕底`）、`紅蓮`（非 `深紅`）、`天空主宰`（非 `天空之主`）。字典與官方不一致時以官方為準修正。
5. 驗證：`python3 scripts/ptcgp_meta.py -d <deck_key>` 顯示新名稱，且 grep 字典確認新對照已寫入。

## 回報
簡短確認說明 + 對照表，標記修正項。

## 依賴
- `ptcgp_deck_dictionary.json`
- `scripts/ptcgp_meta.py`
- `web_search`
