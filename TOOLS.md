# TOOLS.md - Local Notes

## 寶可夢 TCG Pocket 工作區

### Meta 資料
- Meta 來源: `memory/ptcgp_meta.json` (Limitless TCG, B2a set)
- 牌組分析: `memory/ptcgp_meta_discord_*.md`
- 最新 raw: `memory/ptcgp_raw_latest.html`

### 牌組展示
- 牌組 HTML 模板: `deck_magnezone.html`
- 輸出目錄: 可產生靜態 HTML 供 Discord 分享

### Scripts
- `scripts/fetch_meta.mjs` - 抓取 Limitless Meta (需 Node.js + cheerio)
- `scripts/parse_meta.py` - 解析 Meta 資料
- `scripts/download_yt.sh` - 下載 YouTube 影片
- `scripts/analyze_meta.py` - 計算調整後勝率
- `scripts/generate_deck_html.mjs` - 產生牌組 HTML

### Discord Webhook
- Webhook 設定: `webhook_config.json`
- 發送位置: Channel 1338836482420510764

### 技術環境
- ffmpeg: `/home/node/.local/bin/ffmpeg`
- yt-dlp: `/tmp/yt-dlp`
- Video workspace: `video/`, `video2/`, `video3/`

### YouTube 影片下載
```bash
# 單部下載
./scripts/download_yt.sh "https://www.youtube.com/watch?v=..."

# 手動下載 (720p)
/tmp/yt-dlp -f "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]" \
    -o "%(title)s.%(ext)s" "URL"
```

### 牌組卡片資料
- 卡片 JSON: `memory/ptcgp_cards.json`
- 錦標賽記錄: `memory/ptcgp_tournaments.md`
- 牌組字典: `ptcgp_deck_dictionary.json`

### 翻譯字典
- 位置: `ptcgp_deck_dictionary.json`
- 用於 Meta 分析時翻譯牌組名
- 有新翻譯可直接編輯更新
