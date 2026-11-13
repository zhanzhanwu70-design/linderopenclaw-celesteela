#!/bin/bash
# PTCGP 中英翻譯每日更新 cron script
# 每日台北時間 08:00 執行
# 抓官方台版（zh_TW）卡名 → 更新 ptcgp_deck_dictionary.json
# 資料來源：tcgpocket.centropkmn.com/zh_TW/{SET}（遊戲內台版官方卡名）

WORKSPACE="/home/amr/.openclaw/workspace-celesteela"
LOG_FILE="${WORKSPACE}/memory/translation_update.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 開始 PTCGP 翻譯更新" >> "$LOG_FILE"

cd "$WORKSPACE" || exit 1
python3 scripts/update_translations.py 2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 更新完成" >> "$LOG_FILE"
