# Long-Term Memory


## Auto Video Processing
- Linder 明確要求：看到 YouTube PTCGP 影片 URL 一律直接處理，不再等詢問
- 處理流程：下載 → 截圖分析 → 寫 wiki → 回報 Discord
- Whisper API 配額不足時用 frame analysis 截圖代替

## Promoted From Short-Term Memory (2026-06-24)

<!-- openclaw-memory-promotion:memory:memory/2026-03-21.md:1:32 -->
- # 2026-03-21 Daily Log ## 00:03 UTC - Rowlet Keep-Alive / Meta Update Cron - Cron keep-alive test fired at 00:03 UTC - Attempted daily Pokemon TCG Pocket meta update per HEARTBEAT.md - Issues encountered: - External sites (pokemoncard.io, tcgplayer, etc.) blocked or returned no content - No Discord webhook URL configured in workspace - Result: Could not fetch live meta data or post to Discord ## 00:30 UTC - Workspace Review & Updates - Linder added files to workspace - reviewed and integrated - Updates made: 1. **IDENTITY.md** - Filled with identity (Celesteela, 寶可夢助手) 2.... [score=0.849 recalls=5 avg=1.000 source=memory/2026-03-21.md:1-32]

## Promoted From Short-Term Memory (2026-06-27)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:34:36 -->
- Open TODOs: [ ] 等待下場大型錦標賽驗證最新 Meta 預測; [ ] Whisper API 配額恢復後正常流程; [ ] 新收到 Shorts URL 需持續追蹤 [score=0.857 recalls=0 avg=0.620 source=memory/2026-06-23.md:34-36]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:12:14 -->
- 最新 Meta 資料: 來源：Limitless TCG; 最新分析：2026-06-17（`memory/ptcgp_meta_discord_20260615.md`）; 基準：2026-06-17 12:12 UTC，樣本 963（七夕青鳥） [score=0.822 recalls=0 avg=0.620 source=memory/2026-06-23.md:12-14]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:25:27 -->
- Whisper API 狀態: 配額仍耗盡（insufficient_quota）; Frame analysis 已成為主要備援方案; ffmpeg 在部分環境不可用（`0rH9XkVtlNA` 案例） [score=0.822 recalls=0 avg=0.620 source=memory/2026-06-23.md:25-27]

## Promoted From Short-Term Memory (2026-06-28)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:18:21 -->
- 處理的 YouTube 影片（本週）: | Video ID | 頻道 | 牌組 | 方法 | |----------|------|------|------| | t1H6aoqQLSc | Cool Kid Aura | 振翼髮ex + 超級沙奈朵ex 控制 | 截圖分析 | | 0rH9XkVtlNA | Hey Game Plus | 超級路卡利歐ex + 甲賀忍蛙（240人TOP1） | 標題分析（無ffmpeg）| [score=0.893 recalls=0 avg=0.620 source=memory/2026-06-23.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:22:22 -->
- 處理的 YouTube 影片（本週）: | 05X5WLpQ6mo | 安放送局 | 轟鳴月 + 索爾迦雷歐 ex | 截圖分析 | [score=0.893 recalls=0 avg=0.620 source=memory/2026-06-23.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:30:31 -->
- 翻譯字典: 進度：723/1181 張待翻譯; Cron Job ID：`72a0c6ef-3762-4ec5-b529-0cc1d9c585eb`（每日 08:00） [score=0.893 recalls=0 avg=0.620 source=memory/2026-06-23.md:30-31]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:6:9 -->
- 預測驗證記錄: **6/15 → 6/16 → 6/17**：情境 A（水君＋戟脊龍）連續三天命中; 水君 AWR：6/16=52.01%、6/17=51.91%——最穩健效率首選; 電系陷阱規律持續：密勒頓ex系合計 11% 使用率，AWR 49.14%; 睡眠青鳥：南瓜精分支（51.54%）穩定優於太陽伊布（50.71%） [score=0.861 recalls=0 avg=0.620 source=memory/2026-06-23.md:6-9]

## Promoted From Short-Term Memory (2026-07-07)

<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:15:17 -->
- 自動處理原則（確認）: 用戶明確要求：看到 YouTube URL 直接處理，不需詢問; 流程：下載 → 截圖分析 → wiki → 回報 Discord; Whisper 配額不足時用 frame analysis（ffmpeg 截幀 + 視覺分析） [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:15-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:20:22 -->
- 下載環境: yt-dlp：`/tmp/yt-dlp`; 下載腳本：`/home/node/.openclaw/workspace-celesteela/scripts/download_yt.sh`; Video workspace：`/home/node/.openclaw/workspace-celesteela/video3/` [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:20-22]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:25:26 -->
- Whisper API 狀態: 仍為配額不足（insufficient_quota）; Local Whisper 未安裝 [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:25-26]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:29:30 -->
- 翻譯字典: 進度：723/1181 張待翻譯（需確認最新進度）; Cron Job ID：`72a0c6ef-3762-4ec5-b529-0cc1d9c585eb`（每日 08:00） [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:29-30]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:33:36 -->
- 預測系統狀態: 效率基準：水君ex + 戟脊龍ex（~52% AWR）; 電系陷阱：密勒頓ex系合計 11% 使用率，AWR 49%; 睡眠青鳥：南瓜精分支（51.54%）> 太陽伊布分支（50.71%）; 最新驗證：6/17 情境 A（水君）命中 [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:33-36]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:39:42 -->
- 強度評估標準: | 等級 | AWR | 範例 | |------|-----|------| | T0 | > 52% + 高使用率 | 水君 + 戟脊龍 | | T1 | > 51% + 3-5% 使用率 | 火焰雞 + 忍蛙 | [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:39-42]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:4:6 -->
- B3b 新系列（2026-06-30 更新）: 卡圖已下載至 `cards/B3b/`; 新卡 90 張已加入 DB（`memory/ptcgp_cards_full.json`）; 牌組字典翻譯需同步更新 [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:43:44 -->
- 強度評估標準: | T1.5 | 50-51% | 七夕青鳥（50.7%）| | 陷阱 | 高使用率 + < 50% AWR | 密勒頓ex | [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:43-44]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:47:50 -->
- Open TODOs: [ ] 等待下場大型錦標賽驗證最新 Meta 預測; [ ] Whisper API 配額恢復後正常流程; [ ] B3b 新卡翻譯同步; [ ] yt-dlp 環境修復（目前不可用） [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:47-50]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:9:12 -->
- 處理的 YouTube 影片（本對話）: | Video ID | 頻道 | 牌組 | 方法 | |----------|------|------|------| | 0P4b_X1PSlY | 未知 | 超級蒂安希ex + 超級沙奈朵ex + 美洛耶塔 | 標題分析（yt-dlp 不可用）| | 9Mib7l9drKU | 未知 | 美納斯ex + 達克萊伊 + 寶寶丁（睡眠） | 標題分析（yt-dlp 不可用）| [score=0.806 recalls=0 avg=0.620 source=memory/2026-07-02.md:9-12]

## Promoted From Short-Term Memory (2026-07-08)

<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:11:12 -->
- B3b 新系列動態（重要）: `0P4b_X1PSlY`：超級蒂安希 ex + 超級沙奈朵 ex + 美洛耶塔（新超屬最強打手）; `9Mib7l9drKU`：美納斯 ex + 達克萊伊 + 寶寶丁（睡眠惡系混合） [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-03.md:11-12]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:5:5 -->
- B3b 新系列動態（重要）: **惡系上升趨勢確認**： [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-03.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:6:8 -->
- B3b 新系列動態（重要）: `Y3nt8oHuZKE`：B3b 首個錦標賽冠軍，勾魂眼 + 惡系; `9x9BzxnTZs`：百人比賽 TOP 1，超級勾魂眼 ex + 甲賀忍蛙 + 達克萊伊 ex; 惡系連續兩個影片奪冠，B3b 新卡（超級勾魂眼 ex）帶動迴歸 [score=0.852 recalls=0 avg=0.620 source=memory/2026-07-03.md:6-8]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:15:17 -->
- 自動處理原則（確認）: 用戶明確要求：看到 YouTube URL 直接處理，不需詢問; 流程：下載 → 截圖分析 → wiki → 回報 Discord; Whisper 配額不足時用標題分析 [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-03.md:15-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:20:21 -->
- 下載環境: yt-dlp：`/tmp/yt-dlp`（目前標題分析代替實際下載）; Video workspace：`/home/node/.openclaw/workspace-celesteela/video3/` [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-03.md:20-21]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:24:25 -->
- Whisper API 狀態: 仍為配額不足（insufficient_quota）; Local Whisper 未安裝 [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-03.md:24-25]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:28:29 -->
- 翻譯字典: 進度：待確認（應已有 cron job 持續更新）; Cron Job ID：`72a0c6ef-3762-4ec5-b529-0cc1d9c585eb`（每日 08:00） [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-03.md:28-29]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:32:35 -->
- 預測系統狀態: 效率基準：水君ex + 戟脊龍ex（~52% AWR）; 電系陷阱：密勒頓ex系合計 11% 使用率，AWR 49%; 睡眠青鳥：南瓜精分支（51.54%）> 太陽伊布分支（50.71%）; 最新驗證：6/17 情境 A（水君）命中 [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-03.md:32-35]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:38:41 -->
- 強度評估標準: | 等級 | AWR | 範例 | |------|-----|------| | T0 | > 52% + 高使用率 | 水君 + 戟脊龍 | | T1 | > 51% + 3-5% 使用率 | 火焰雞 + 忍蛙 | [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-03.md:38-41]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:42:43 -->
- 強度評估標準: | T1.5 | 50-51% | 七夕青鳥（50.7%）| | 陷阱 | 高使用率 + < 50% AWR | 密勒頓ex | [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-03.md:42-43]

## Promoted From Short-Term Memory (2026-07-09)

<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:46:49 -->
- Open TODOs: [ ] B3b Meta 分析（需要及時更新）; [ ] 惡系牌組強度追蹤; [ ] Whisper API 配額恢復後正常流程; [ ] 翻譯字典進度確認 [score=0.845 recalls=0 avg=0.620 source=memory/2026-07-03.md:46-49]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:10:10 -->
- B3b 新系列動態（重要）: **其他 B3b 牌組**： [score=0.835 recalls=0 avg=0.620 source=memory/2026-07-03.md:10-10]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05.md:10:10 -->
- B3b 新系列動態（2026-07-03 重要更新）: **其他 B3b 牌組**： [score=0.803 recalls=0 avg=0.620 source=memory/2026-07-05.md:10-10]
