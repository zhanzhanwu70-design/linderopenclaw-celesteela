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

### 卡圖工作區
- 卡圖目錄: `cards/`（18個系列，共3033張）
- 卡圖下載: `scripts/download_limitless.sh`（從 Limitless TCG 網站）
- 卡號格式: `{SET}_{NUM}.webp`，例如 `A1_001.webp`, `B2a_042.webp`

### 卡片資料庫
- 完整資料: `memory/ptcgp_cards_full.json`（2916張卡的完整資料）
- 欄位: name, type, hp, weakness, retreat, attacks
- 查詢方式: `node -e "const d=require('./memory/ptcgp_cards_full.json'); console.log(d['A1_001'])"`
- 卡圖路徑: `cards/{SET}/{SET}_{NUM}.webp`

### 卡牌查詢 Skill
- Skill 路徑: `skills/ptcgp-card-lookup/`
- 編號→名稱: `skills/ptcgp-card-lookup/number_to_name.json`
- 名稱→編號: `skills/ptcgp-card-lookup/name_to_numbers.json`

### OCR 流程（建議）
1. OCR 辨識卡名（英文）
2. 用 `name_to_numbers.json` 找出所有同名卡版本
3. 若需確認版本，再跑影像辨識
4. 用編號精準查詢資料庫

### 卡圖對應表（2026-03-27 更新）
| 系列 | 目錄 | 卡數 |
|------|------|------|
| A1 Genetic Apex | cards/A1/ | 286 |
| A1a Mythical Island | cards/A1a/ | 86 |
| A2 Space-Time Smackdown | cards/A2/ | 207 |
| A2a Triumphant Light | cards/A2a/ | 96 |
| A2b Shining Revelry | cards/A2b/ | 111 |
| A3 Celestial Guardians | cards/A3/ | 239 |
| A3a Extradimensional Crisis | cards/A3a/ | 103 |
| A3b Eevee Grove | cards/A3b/ | 107 |
| A4 Wisdom of Sea and Sky | cards/A4/ | 241 |
| A4a Secluded Springs | cards/A4a/ | 105 |
| A4b Deluxe Pack ex | cards/A4b/ | 379 |
| B1 Mega Rising | cards/B1/ | 331 |
| B1a Crimson Blaze | cards/B1a/ | 103 |
| B2 Fantastical Parade | cards/B2/ | 234 |
| B2a Paldean Wonders | cards/B2a/ | 131 |
| B2b Mega Shine | cards/B2b/ | 117 |
| P-A Promo-A | cards/P-A/ | 117 |
| P-B Promo-B | cards/P-B/ | 40 |

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
