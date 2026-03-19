# 🦅 LinderOpenClaw

> 基於 OpenClaw 的多 Agent 協作系統 — 讓 AI 團隊分工合作，自動完成研究、開發、部署、測試與資安審計。

---

## 🤖 Agent 團隊

<div align="center">

| Agent | 名稱 | 角色定位 | 核心职责 |
|:-----:|:----:|:--------:|:---------|
| 🗼 Celesteela | 鐵火輝夜 | 主控 Agent | 任務調派、流程協調 |
| 🔥 Charizard | 噴火龍 | 軟體實作 | Plugin / Hook 開發 |
| 👻 Gengar | 耿鬼 | 測試回饋 | 任務驗證、測試覆蓋 |
| 🦉 Rowlet | 木木梟 | 研究理論 | 方案設計、技術調研 |
| 🌙 RoaringMoon | 轟鳴月 | 資安研究 | 滲透測試、威脅分析 |
| 🧱 MrMime | 魔牆人偶 | 安裝部署 | 安全監控、DevOps |

</div>

---

## 📋 Agent 合作框架

### 工作流程

```
Linder 下任務
     │
     ▼
┌─────────┐    研究理論     ┌─────────┐    軟體實作     ┌─────────┐
│  木木梟  │ ──────────────▶│  噴火龍  │ ──────────────▶│ 魔牆人偶 │
│  Rowlet  │                │ Charizard│                │ MrMime  │
└─────────┘                └─────────┘                └─────────┘
     ▲                                                        │
     │         資安研究                  測試回饋             │
┌─────────┐ ◀───────────────────────────────────────────────┘
│ 轟鳴月   │
│RoaringMoon│
└─────────┘
     │
     ▼
┌─────────┐
│  耿鬼    │
│  Gengar  │
└─────────┘
```

> 🔄 流程支援迴圈迭代：依需求，耿鬼可再次觸發各環節優化。

### 溝通機制

- **`sessions_send`** — Agent 之間直接溝通，精準傳遞意圖
- **智慧理解原則** — 理解目的後適當回應，**有價值才轉達**
- **嚴禁隨意廣播** — 不主動將 Agent 間對話轉發到 Discord 頻道

### 轉發判斷標準

```
✅ 轉發：最終成果、需人類確認事項、重要通知
❌ 不轉發：中間討論、技術細節、純內部協作訊息
```

---

## 🛠️ Skill 技能列表

### 🔒 安全監控

| Skill | 功能說明 |
|:------|:---------|
| `openclaw-monitor` | 即時監控 OpenClaw 運作狀態，發送異常通知 |
| `openclaw-runtime-monitor` | 檔案系統、憑證存取、異常行為即時偵測 |
| `openclaw-security` | 安全防護手冊，威脅模型與緩解措施 |
| `openclaw-security-scanner` | Tool 執行前惡意程式掃描 |
| `skill-guard` | Skill 惡意內容審查，過濾危險指令 |
| `prompt-injection-defense` | Prompt 注入攻擊偵測與防禦 |

### 🖼️ 圖片處理

| Skill | 功能說明 |
|:------|:---------|
| `image-attendant` | 圖片分析、分類、歸檔與整理 |
| `smart-ocr` | 文字辨識（支援 100+ 語言） |
| `ocr-handwriting` | 手寫文字 OCR，適合箱子標籤辨識 |
| `photo-archive` | 照片歸檔，自動擷取條碼與手寫文字 |

### 🎬 影片處理

| Skill | 功能說明 |
|:------|:---------|
| `video-frame-analyzer` | 影片截圖（1 FPS）並分析內容 |
| `youtube-downloader` | YouTube 影片下載與音訊提取 |

---

## 📁 專案結構

```
.
├── AGENTS.md          # Agent 角色定義
├── SECURITY.md        # 安全防護設定
├── SOUL.md            # Agent 靈魂與人格設定
├── HEARTBEAT.md       # 每日自動化任務
├── memory/            # 知識庫與 Meta 資料
├── skills/            # 自定義 Skills
└── scripts/           # 輔助腳本
```

---

## ⚙️ 快速開始

```bash
# 查看 OpenClaw 狀態
openclaw status

# 查看 Gateway 狀態
openclaw gateway status

# 重啟 Gateway
openclaw gateway restart
```

---

## 🔗 相關連結

- 📘 [OpenClaw 文件](https://docs.openclaw.ai)
- 🐙 [GitHub 原始碼](https://github.com/openclaw/openclaw)
- 💬 [Discord 社群](https://discord.com/invite/clawd)
- 🐾 [Skill 市集 ClaWHub](https://clawhub.com)

---

<div align="center">

**Built with 🐾 OpenClaw · Powered by Agent Team**

</div>
