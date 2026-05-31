#!/bin/bash
# PTCGP 中英翻譯每日更新 cron script
# 每日台北時間 08:00 執行
# 用途：抓取最新卡牌中英對照，更新 ptcgp_deck_dictionary.json

WORKSPACE="/home/node/.openclaw/workspace-celesteela"
DICT_PATH="${WORKSPACE}/ptcgp_deck_dictionary.json"
CARDS_PATH="${WORKSPACE}/memory/ptcgp_cards_full.json"
LOG_FILE="${WORKSPACE}/memory/translation_update.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 開始 PTCGP 翻譯更新" >> "$LOG_FILE"

cd "$WORKSPACE" || exit 1

# 嘗試從 Limitless TCG 抓取 B3a 卡名對照
# 如果失敗則跳過（只更新已知的部分）
node -e "
const https = require('https');
const fs = require('fs');

const CARDS_PATH = '${WORKSPACE}/memory/ptcgp_cards_full.json';
const DICT_PATH = '${WORKSPACE}/ptcgp_deck_dictionary.json';

const cards = JSON.parse(fs.readFileSync(CARDS_PATH, 'utf8'));
const dict = JSON.parse(fs.readFileSync(DICT_PATH, 'utf8'));

if (!dict.card_names) dict.card_names = {};

async function fetchPage(set, num) {
  return new Promise((resolve) => {
    setTimeout(() => {
      try {
        const req = https.get({
          hostname: 'Limitlesstcg.com',
          path: '/pokemon-tcg-pocket/cards/' + set + '/' + num,
          headers: { 'User-Agent': 'Mozilla/5.0' },
          timeout: 8000
        }, (res) => {
          let data = '';
          res.on('data', c => data += c);
          res.on('end', () => {
            // Try to extract Chinese from page title or meta
            const titleMatch = data.match(/<title>([^<]+)/);
            const cnMatch = data.match(/data-cn[=:][\"']([^\"']+)[\"']/i);
            const ogMatch = data.match(/og:title[^\"]+\"([^\"]+)/i);
            
            let name = null;
            if (cnMatch) name = cnMatch[1];
            else if (ogMatch) name = ogMatch[1].split('•')[0].trim();
            else if (titleMatch) name = titleMatch[1].split('•')[0].trim();
            
            resolve(name);
          });
        });
        req.on('error', () => resolve(null));
        req.on('timeout', () => { req.destroy(); resolve(null); });
      } catch(e) { resolve(null); }
    }, 300);
  });
}

async function update() {
  const sets = ['B3a'];
  let updated = 0;
  let errors = 0;
  
  for (const set of sets) {
    // Get B3a card count
    const count = Object.keys(cards).filter(k => k.startsWith(set + '_')).length;
    
    for (let num = 1; num <= count; num++) {
      const padded = String(num).padStart(3, '0');
      const cardId = set + '_' + padded;
      const card = cards[cardId];
      if (!card) continue;
      if (dict.card_names[card.name]) continue;
      
      const name = await fetchPage(set, num);
      if (name && name !== card.name) {
        dict.card_names[card.name] = name;
        updated++;
        console.log('Update:', card.name, '->', name);
      } else {
        errors++;
      }
    }
  }
  
  dict.last_updated = new Date().toISOString().split('T')[0];
  fs.writeFileSync(DICT_PATH, JSON.stringify(dict, null, 2));
  console.log('Updated:', updated, 'errors:', errors);
  return { updated, errors };
}

update().catch(e => { console.error('Error:', e.message); process.exit(1); });
" 2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 更新完成" >> "$LOG_FILE"