---
name: "ptcgp-meta-reporting"
description: "PTCGP Meta 報告發布與排程調整：前五名、500 字內、每日筆記加三日彙整。"
---

# PTCGP Meta 報告輸出與發布

## 觸發條件
- 使用者要求「meta 分析」「環境分析」「推前五名」「meta 報告」
- 調整 Meta 分析的輸出格式、字數上限或發送頻率
- Meta 報告要發到 Discord，或既有 Meta 排程漏發／重複發

## 輸出契約（所有對外 Meta 輸出）

1. 只列推薦結果前五名，依調整後勝率排序。
2. 總字數 ≤ 500 字（含標點），超長就刪到剛好合格。
3. 全繁體中文；牌組名取自 `ptcgp_deck_dictionary.json`，禁英文名、禁即興機翻。
4. 不用表格；不列第六名以後；不貼長篇分析。
5. 最後補 1–2 句環境結論與 1 句建議。
6. 完整數據、變化與新卡／規則影響寫進本地筆記，不塞進貼文。

## 步驟

1. 讀既有規範與字典：讀 `AGENTS.md` 的「Meta 分析輸出格式」段與 `ptcgp_deck_dictionary.json`；缺翻譯先補字典再輸出。完成條件：成稿裡沒有英文牌組名。

2. 抓數並算 AWR：抓 `https://play.limitlesstcg.com/decks?game=pocket&format=standard`（需要時加 `&set=XXXX` 或 `&combine=1`），以 `(勝場 + 12) / (總場 + 25)` 算調整後勝率，排出使用率前五與 AWR 前五。完成條件：兩份前五都帶數字與樣本數。

3. 依「輸出契約」成稿：貼文只含前五名、結論與建議，並檢查字數 ≤ 500。完成條件：草稿字數達標。

4. 排程拆成「每日記錄」與「對外彙整」兩個 job：
   - 每日 job（cron `5 20 * * *`, tz `Asia/Taipei`）：只把完整結果寫入 `memory/YYYY-MM-DD.md` 與 `memory/ptcgp_meta_discord_YYYYMMDD.md`，delivery 設 `none`，不發 Discord；prompt 內禁止 curl／message 發送。
   - 彙整 job（`--every 72h`）：讀最近三份 `memory/ptcgp_meta_discord_*.md`，照輸出契約產出貼文，用 announce delivery 送目標 Discord 頻道。
   完成條件：`openclaw cron get <id>` 顯示每日 job delivery=none、彙整 job delivery=announce。

5. 不把 curl 直送 Discord webhook 當主要發送路徑：Discord 單則上限 2000 字元，超過回 HTTP 400；而 webhook delivery 會把 job 最終回覆再送一次，造成重複貼文。讓 job 回覆本身成為唯一貼文。完成條件：job prompt 裡沒有 curl 發送步驟。

6. 驗證：`openclaw cron list --json` 核對 schedule／delivery／payload，再 `openclaw cron run <id>` 手動跑一次彙整 job。完成條件：Discord 收到一則 ≤500 字貼文且沒有第二則。

## 診斷漏發／重複發

用 `openclaw automations runs --id <jobId>` 看 deliveryError：
- HTTP 400 → 貼文超過 Discord 2000 字元，改用 announce delivery 並收斂輸出。
- rate_limit → 模型端失敗，job 需設 fallback，否則整份報告遺失。
- 兩則以上 → 同時存在 webhook 與 announce 兩條發送路徑，刪掉 curl 那條。

## 注意
- 每日 job 至少要設定模型 fallback：過往單一模型在尖峰時回 429，造成整份每日報告遺失。
- 每日筆記是唯一正式紀錄；彙整 job 只讀筆記、不重新抓資料，避免與每日 job 互相覆蓋。
- 每日 job 的最終回覆只寫一句完成摘要（例：`已完成 YYYY-MM-DD Meta 分析，筆記：memory/YYYY-MM-DD.md`），不貼報告。
