/**
 * PTCGP 卡牌中英對照字典更新腳本
 * 功能：抓取 Limitless TCG Pocket 卡牌資料，更新卡名翻譯
 * 
 * 使用方式：
 *   node scripts/update_card_translations.js [set]
 *   
 * 不帶參數：更新所有系列（1181張卡）
 * 帶參數：只更新指定系列，例如 node scripts/update_card_translations.js B3a
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const WORKSPACE = '/home/node/.openclaw/workspace-celesteela';
const DICT_PATH = `${WORKSPACE}/ptcgp_deck_dictionary.json`;
const CARDS_PATH = `${WORKSPACE}/memory/ptcgp_cards_full.json`;

const SETS = ['A1', 'A1a', 'A2', 'A2a', 'A2b', 'A3', 'A3a', 'A3b', 'A4', 'A4a', 'A4b',
              'B1', 'B1a', 'B2', 'B2a', 'B2b', 'B3a', 'P-A', 'P-B'];

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; PTCGP-Bot/1.0)',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Accept': 'application/json, text/html'
      },
      timeout: 15000
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
  });
}

function extractChineseName(html) {
  // Try to find Chinese name in page
  // Pattern 1: <title>Surskit • Paradox Drive (B3a) #1 – Limitless TCG Pocket</title>
  // Pattern 2: data-name attributes, data-cn attributes
  const titleMatch = html.match(/<title>([^<]+)\s+•/);
  if (titleMatch) return titleMatch[1].trim();
  
  // Try JSON-LD
  const jsonMatch = html.match(/"name"\s*:\s*"([^"]+)"/);
  if (jsonMatch) return jsonMatch[1];
  
  // Try meta
  const ogMatch = html.match(/og:title[^>]*content="([^"]+)"/i);
  if (ogMatch) return ogMatch[1].split('•')[0].trim();
  
  return null;
}

function extractCardNumber(html) {
  // Try to get internal card identifier
  const numMatch = html.match(/card\/([A-Z0-9]+)_(\d+)/i);
  if (numMatch) return numMatch[1] + '_' + numMatch[2];
  
  // Try data attributes
  const dataMatch = html.match(/"set"\s*:\s*"([^"]+)".*?"number"\s*:\s*(\d+)/s);
  if (dataMatch) return dataMatch[1] + '_' + dataMatch[2];
  
  return null;
}

async function fetchChineseName(set, number) {
  const url = `https://Limitless.tcgpocket.com/cards/${set}/${number}`;
  try {
    const html = await fetchUrl(url);
    const name = extractChineseName(html);
    const cardId = extractCardNumber(html);
    return { cardId, name, url };
  } catch (e) {
    return { cardId: `${set}_${number}`, name: null, error: e.message };
  }
}

async function getSetCardCount(set) {
  try {
    const url = `https://Limitless.tcgpocket.com/cards/${set}`;
    const html = await fetchUrl(url);
    // Find total cards count from pagination
    const countMatch = html.match(/(\d+)\s*cards?/i);
    if (countMatch) return parseInt(countMatch[1]);
    
    // Try to find pagination info
    const pageMatch = html.match(/Showing\s+(\d+)-(\d+)\s+of\s+(\d+)/i);
    if (pageMatch) return parseInt(pageMatch[3]);
    
    // Try JSON API
    const apiUrl = `https://Limitless.tcgpocket.com/api/sets/${set}/cards`;
    const json = await fetchUrl(apiUrl).catch(() => null);
    if (json) {
      const data = JSON.parse(json);
      if (Array.isArray(data)) return data.length;
    }
  } catch (e) {}
  return 100; // fallback
}

async function updateTranslations(targetSet = null) {
  const sets = targetSet ? [targetSet] : SETS;
  const cards = JSON.parse(fs.readFileSync(CARDS_PATH, 'utf8'));
  const dict = JSON.parse(fs.readFileSync(DICT_PATH, 'utf8'));
  
  // Initialize card_names if not exists
  if (!dict.card_names) dict.card_names = {};
  
  let updated = 0;
  let errors = 0;
  
  for (const set of sets) {
    console.log(`\nProcessing set: ${set}`);
    
    // Get set card count
    const count = await getSetCardCount(set);
    console.log(`  Total cards: ${count}`);
    
    for (let num = 1; num <= count; num++) {
      const cardId = `${set}_${String(num).padStart(3, '0')}`;
      const card = cards[cardId];
      
      if (!card) {
        // Try without padding
        const card2 = cards[`${set}_${num}`];
        if (!card2) continue;
      }
      
      // Skip if already has Chinese in dict
      if (dict.card_names[card.name]) continue;
      
      // Rate limit: 1 request per 500ms
      await new Promise(r => setTimeout(r, 500));
      
      const result = await fetchChineseName(set, num);
      
      if (result.name && result.name !== card.name) {
        dict.card_names[card.name] = result.name;
        updated++;
        console.log(`  ${cardId}: ${card.name} -> ${result.name}`);
      } else if (result.name === null) {
        errors++;
        console.log(`  ${cardId}: (no Chinese name found)`);
      }
    }
  }
  
  // Save updated dict
  dict.last_updated = new Date().toISOString().split('T')[0];
  fs.writeFileSync(DICT_PATH, JSON.stringify(dict, null, 2));
  
  console.log(`\nDone. Updated: ${updated}, Errors: ${errors}`);
  console.log(`Dict saved to: ${DICT_PATH}`);
}

// Run from command line
const targetSet = process.argv[2] || null;
updateTranslations(targetSet).catch(console.error);