# Long-Term Memory

## PTCGP Meta 輸出規範（2026-10-31 Linder 指示）
- Meta 分析一律只輸出推薦結果前五名，依調整後勝率 (勝場+12)/(總場+25) 排序。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 單次輸出總字數控制在 500 字內，超長就刪到合格；不用表格、不列第六名以後。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- Meta 對外輸出改為每三天彙整一次（Job `6ddc8b4c-6963-4c68-9f01-5773722fbd76`，每 72 小時）；每日分析仍照跑，但只寫本地筆記（Job `09c7940b-c32b-4336-928f-6f158947147d`，每日 20:05 Asia/Taipei，delivery=none）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 每日筆記寫入 `memory/YYYY-MM-DD.md` 與 `memory/ptcgp_meta_discord_YYYYMMDD.md`；每日排程不得再用 curl／message 發 Discord。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

## PTCGP Meta 分析流程規則（累積教訓，長期有效）
- **跨日比較前必須用同一支 parser 重新解析當日 raw HTML**，並比對 row 數 + 錦標賽／對局數確認口徑；不可直接沿用前次留下的 JSON 快取（檔名與 raw 不同步會誤用舊快照）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **新分支的第一份 AWR 不能當定論**：需 N≥1500 且連續 2 日同方向、族群合併值同方向確認，才視為真實反轉；否則視為噪音。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **預測判定線**：靜止期與換包期都改用「崩解型／守住型」雙條件判定線，不要設「份額擴張門檻」型情境（已連續多日全滅）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **追蹤主力時必須同時列出同核心的所有分支版本**，否則會低估擴張幅度（自爆磁怪 → 密勒頓分支；忍蛙 → 水君／甲賀忍蛙／反制三分支）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **換包後必須同時維護新舊兩個 set 的頁面並在數字旁標註出自哪一頁**；舊頁凍結要寫「凍結」不可寫成「延續」。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **份額第一 = 環境靶心**：牌組被三方以上對位同時圍剿時會快速崩解，判讀崩壞原因要看對位結構而非只看勝率。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **門檻需距當前值至少 1.5pt**，否則門檻落在噪音帶內、連續多日擦邊不破；雙條件情境改為「任一條件成立＝方向成立、兩者皆成立＝情境命中」，避免雙條件互相稀釋。同一族群不同方向不可併在同一情境。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **族群分類函式 grp() 不可自行增刪關鍵字**：跨日比較前須與前一日腳本逐字對齊，否則族群份額／AWR 不可比。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **對位頁為牌組分支級 URL**（如 `giratina-ex-c1-dragonair-b4`），用原型 slug 抓會得到 title 為 `undefined` 的空白殼頁；抓對位必須用分支表 slug。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **牌組名翻譯以官方台版卡名為準**：來源 tcgpocket.centropkmn.com/zh_TW/{SET}（遊戲內台版官方名，2026-11-02 已對齊全部 22 系列）。字典需嚴格區分 card_names（單卡）與 deck_names（牌組）；自動組譯時要把「可被切成 2 張以上卡名」的複合項排除，否則會把整個牌組名當一張卡。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **每日並列追蹤「新卡份額占比」與「新舊卡 AWR 差距」**：差距擴大代表擴充包進入衰退期，是比族群 AWR 波動更早的環境轉向訊號（2026-11-02 差距由 0.28pt 擴大到 2.89pt）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

## Heartbeat 機制（2026-11-03 確認）
- 本機 heartbeat 由 OpenClaw 原生 cron 承載：`heartbeat:celesteela`（Job `46242a4c-915b-4f97-9163-5fd924f1f81e`，每 30 分鐘，payload=`{"kind":"heartbeat"}`），狀態用 scratch 傳遞（`openclaw cron scratch <id>`）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **不存在** `~/.openclaw/task-queue/heartbeat_check.py` 這套舊機制，2026-08-23 起每天回報「heartbeat 缺失」是誤判，不要再報。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- Poll 判準：scratch=`HEARTBEAT_OK` → 無待辦回 `NO_REPLY`；只有 `HEARTBEAT_FAIL` 才需處理任務。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

## Auto Video Processing
- Linder 明確要求：看到 YouTube PTCGP 影片 URL 一律直接處理，不再等詢問
- 處理流程：下載 → 截圖分析 → 寫 wiki → 回報 Discord
- Whisper API 配額不足時用 frame analysis 截圖代替

## Promoted From Short-Term Memory (2026-07-16)

<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:10:10 -->
- B3b 新系列動態（持續更新）: **B3b 牌組記錄**： [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:10-10]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:11:14 -->
- B3b 新系列動態（持續更新）: `0P4b_X1PSlY`：超級蒂安希 ex + 超級沙奈朵 ex + 美洛耶塔（新超屬最強打手）; `9Mib7l9drKU`：美納斯 ex + 達克萊伊 + 寶寶丁（睡眠惡系混合）; `RwfcoHgrirM`：阿塞蘿拉 + 咚咚鼠 ex（新Combo，「訊息差」打法）; `BzilAomFpZs`：超級蜥蜴王 ex + 甲賀忍蛙 — 四座冠軍 59%勝率（Cool Kid Aura） [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:11-14]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:15:15 -->
- B3b 新系列動態（持續更新）: `oSmWPVnfuSU`：超級暴鯉龍 ex — 全進化 ALL-IN 牌組（Cool Kid Aura） [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:15-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:19:22 -->
- 翻譯字典更新（2026-07-03）: | 原文 | 翻譯 | 備註 | |------|------|------| | Mega Sableye ex | 超級勾魂眼 ex | 新增 | | Mega Sableye | 超級勾魂眼 | 新增 | [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:19-22]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:23:25 -->
- 翻譯字典更新（2026-07-03）: | Dedenne | 咚咚鼠 | 修正（之前誤翻為「dd」）| | Dedenne ex | 咚咚鼠 ex | 修正（之前誤翻為「電擊蟲 ex」）| | Milotic | 美納斯 | 新增 | [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:23-25]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:27:27 -->
- 翻譯字典更新（2026-07-03）: Mega Gardevoir ex（超級沙奈朵ex）和 Mega Diancie ex（超級蒂安希ex）早已記錄。 [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:27-27]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:5:5 -->
- B3b 新系列動態（持續更新）: **惡系上升趨勢確認（已驗證）**： [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:6:8 -->
- B3b 新系列動態（持續更新）: `Y3nt8oHuZKE`：B3b 首個錦標賽冠軍，勾魂眼 + 惡系; `9x9BzxnTZs`：百人比賽 TOP 1，超級勾魂眼 ex + 甲賀忍蛙 + 達克萊伊 ex; 惡系連續兩個影片奪冠，B3b 新卡（超級勾魂眼 ex）帶動迴歸 [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:6-8]

## Promoted From Short-Term Memory (2026-07-17)

<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:10:10 -->
- 今日處理記錄: **翻譯字典更新：** [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-12.md:10-10]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:11:11 -->
- 今日處理記錄: `Mandibuzz` → `禿鷹娜` ✅（之前誤翻為 `md`） [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-12.md:11-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:15:15 -->
- 重要修正：惡系崛起預測錯誤: **之前預測（2026-07-03）**：「惡系上升趨勢確認，超級勾魂眼 ex 帶動惡系迴歸」 [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-12.md:15-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:17:17 -->
- 重要修正：惡系崛起預測錯誤: **實際 Meta（2026-07-11）**： [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-12.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:18:21 -->
- 重要修正：惡系崛起預測錯誤: 超級勾魂眼 ex + Greninja：AWR 47.01%，使用率 11.7% → 陷阱確認; 超級勾魂眼 ex + 達克萊伊 ex：AWR 46.12%; 三眼奪魂 + 巨翅鳥：AWR 48.66%; 惡系全軍覆沒，預測完全錯誤 [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-12.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:23:23 -->
- 重要修正：惡系崛起預測錯誤: **原因分析**：錦標賽奪冠（影片）與整體 Meta 表現是不同維度，樣本偏差。 [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-12.md:23-23]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:6:7 -->
- 今日處理記錄: `L7ZU_dqrypk`：禿鷹娜 + 甲賀忍蛙 — 冷門狙擊牌組（Cool Kid Aura）; 「比樹梟還快」可能是針對草系的反制 [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-12.md:6-7]

## Promoted From Short-Term Memory (2026-07-18)

<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:5:5 -->
- 今日處理記錄: **YouTube 影片處理：** [score=0.818 recalls=0 avg=0.620 source=memory/2026-07-12.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:10:13 -->
- 今日 Meta 分析（2026-07-13 已發布）: 超級七夕青鳥 + 太陽伊布 52.48%; 超級蜥蜴王 ex + 忍蛙 52.37%; 美納斯 ex + 獅烈颚 ex 52.29%; 愛管仕 ex + 騎拉帝納 51.96% [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-13.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:14:15 -->
- 今日 Meta 分析（2026-07-13 已發布）: 超級雷電獸 ex + 傑拉 51.40%; 超級路卡利歐 ex 51.20% [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-13.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:17:17 -->
- 今日 Meta 分析（2026-07-13 已發布）: **強度分級：** [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-13.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:18:21 -->
- 今日 Meta 分析（2026-07-13 已發布）: T0：佐羅克+阿博梭魯 / 密樂頓 / 水君+戟脊龍（53%+）; T1：火焰雞 / 七夕青鳥 / 蜥蜴王 / 美納斯+獅烈颚 / 愛管仕（51-53%）; T1.5：雷電獸 / 路卡利歐 / 三眼奪魂+勾魂眼（50-52%）; T2：巴大蝶+蜥蜴王（48.77%） [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-13.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:22:22 -->
- 今日 Meta 分析（2026-07-13 已發布）: 陷阱：Greninja+超級勾魂眼 ex（47.48%，使用率12.5%） [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-13.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:24:24 -->
- 今日 Meta 分析（2026-07-13 已發布）: **Cron 故障原因：** MiniMax API 短暫過載（overloaded），7次連續錯誤，非程式碼問題。 [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-13.md:24-24]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:6:9 -->
- 今日 Meta 分析（2026-07-13 已發布）: 佐羅克 ex + 阿博梭魯 ex 53.44% 🌟 新AWR王; 密樂頓 ex + 自爆磁怪 53.15%（使用率 18.1%）; 水君 ex + 戟脊龍 53.05%; 超級火焰雞 ex + 忍蛙 52.82% [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-13.md:6-9]

## Promoted From Short-Term Memory (2026-07-19)

<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:5:5 -->
- 今日 Meta 分析（2026-07-13 已發布）: **AWR 前10：** [score=0.818 recalls=0 avg=0.620 source=memory/2026-07-13.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:10:13 -->
- 昨日 Meta 分析（2026-07-13 已發布）: 超級七夕青鳥 + 太陽伊布 52.48%; 超級蜥蜴王 ex + 忍蛙 52.37%; 美納斯 ex + 獅烈颚 ex 52.29%; 愛管仕 ex + 騎拉帝納 51.96% [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-14.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:14:15 -->
- 昨日 Meta 分析（2026-07-13 已發布）: 超級雷電獸 ex + 傑拉 51.40%; 超級路卡利歐 ex 51.20% [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-14.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:17:17 -->
- 昨日 Meta 分析（2026-07-13 已發布）: **強度分級：** [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-14.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:18:21 -->
- 昨日 Meta 分析（2026-07-13 已發布）: T0：佐羅克+阿博梭魯 / 密樂頓 / 水君+戟脊龍（53%+）; T1：火焰雞 / 七夕青鳥 / 蜥蜴王 / 美納斯+獅烈颚 / 愛管仕（51-53%）; T1.5：雷電獸 / 路卡利歐 / 三眼奪魂+勾魂眼（50-52%）; T2：巴大蝶+蜥蜴王（48.77%） [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-14.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:22:22 -->
- 昨日 Meta 分析（2026-07-13 已發布）: 陷阱：Greninja+超級勾魂眼 ex（47.48%，使用率12.5%） [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-14.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:24:24 -->
- 昨日 Meta 分析（2026-07-13 已發布）: **Cron 故障原因：** MiniMax API 短暫過載（overloaded），7次連續錯誤，非程式碼問題。 [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-14.md:24-24]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:6:9 -->
- 昨日 Meta 分析（2026-07-13 已發布）: 佐羅克 ex + 阿博梭魯 ex 53.44% 🌟 新AWR王; 密樂頓 ex + 自爆磁怪 53.15%（使用率 18.1%）; 水君 ex + 戟脊龍 53.05%; 超級火焰雞 ex + 忍蛙 52.82% [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-14.md:6-9]

## Promoted From Short-Term Memory (2026-07-20)

<!-- openclaw-memory-promotion:memory:memory/2026-07-15.md:14:15 -->
- 今日 Meta 分析（2026-07-15 已發布）: 美納斯 ex + 獅烈颚 ex 51.42%; 超級路卡利歐 ex 51.39% [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-15.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-15.md:17:17 -->
- 今日 Meta 分析（2026-07-15 已發布）: **強度分級：** [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-15.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-15.md:18:21 -->
- 今日 Meta 分析（2026-07-15 已發布）: T0：佐羅克+阿博梭魯 / 火焰雞 / 密樂頓（53%+）; T1：蜥蜴王 / 七夕青鳥 / 水君+戟脊龍 / 雷電獸（52%）; T1.5：愛管仕 / 美納斯+獅烈颚 / 路卡利歐（51-52%）; T2：三眼奪魂+勾魂眼 / 巴大蝶+蜥蜴王（48-49%） [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-15.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-07-15.md:10:13 -->
- 今日 Meta 分析（2026-07-15 已發布）: 超級七夕青鳥 + 太陽伊布 52.46%; 水君 ex + 戟脊龍 52.45% ↓ 跌破; 超級雷電獸 ex + 傑拉 52.01%; 愛管仕 ex + 騎拉帝納 51.77% [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-15.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-07-15.md:22:22 -->
- 今日 Meta 分析（2026-07-15 已發布）: 陷阱：Greninja+超級勾魂眼 ex（47.16%，使用率 12.8%） [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-15.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:5:5 -->
- 昨日 Meta 分析（2026-07-13 已發布）: **AWR 前10：** [score=0.818 recalls=0 avg=0.620 source=memory/2026-07-14.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-15.md:24:24 -->
- 今日 Meta 分析（2026-07-15 已發布）: **關鍵變化：** [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-15.md:24-24]
<!-- openclaw-memory-promotion:memory:memory/2026-07-15.md:6:9 -->
- 今日 Meta 分析（2026-07-15 已發布）: 佐羅克 ex + 阿博梭魯 ex 53.71% ↑↑ 大回升; 超級火焰雞 ex + 忍蛙 53.20% ↑↑ 新AWR王！; 密樂頓 ex + 自爆磁怪 52.97%; 超級蜥蜴王 ex + 忍蛙 52.59% [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-15.md:6-9]
