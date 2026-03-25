# SKILL.md - 寶可夢 TCG Pocket 卡圖下載研究

## 研究目標
從 No哥的寶可夢 TCG Pocket 卡牌圖鑒網站下載所有卡圖。
- 網站: https://sites.google.com/view/noge-pokemontcgpocket-zh/%E5%8D%A1%E7%89%8C%E5%9C%96%E9%91%92
- 預期數量: 2000+ 張卡圖

## 研究過程

### 1. web_fetch / curl
- Google Sites 使用 JavaScript 動態載入內容
- curl 無法取得動態載入的卡片資料

### 2. Google Apps Script API
- Script ID: `AKfycbwnbRITmPw5aATj_uLiXthChxotkbv1dQgrMCR9PSk6gLdhZYubuU0tEwxsVkBMfMxr`
- 使用 IFRAME_SANDBOX 模式，需 JS 執行
- 無法從外部取得卡片 JSON 資料

### 3. Google Photos 圖片格式
- URL: `https://lh3.googleusercontent.com/d/{img_id}`
- 每張卡圖有獨立 img_id
- 無法枚舉所有 ID

## 結論

**目前無法自動下載。**

需 JS 執行或瀏覽器自動化（Puppeteer）。

## 工作流程整合

### 手動下載流程
1. 手動瀏覽網站
2. 將圖片放入 `cards/manual/` 目錄
3. 讓我分析特定卡圖

### 腳本位置
- 下載腳本: `scripts/download_cards.js`（需 Puppeteer）
- 卡圖目錄: `cards/`
- 手動下載: `cards/manual/`

## 環境限制
- 無 root 權限 → 無法 apt-get 安裝依賴
- 無 Chrome/Chromium → Puppeteer 無法運行
- 環境缺少 libnss3, libnspr4 等

## 待解決
- 需要 Chrome/Chromium 環境
- 或詢問 No哥 是否有開源儲存庫
