const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const SETS = ['A1', 'A1a', 'A2', 'A2a', 'A2b', 'A3', 'A3a', 'A3b', 'A4', 'A4a', 'A4b', 
              'B1', 'B1a', 'B2', 'B2a', 'P-A', 'P-B'];

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    const req = protocol.get(url, { 
      headers: { 'User-Agent': 'Mozilla/5.0' },
      timeout: 15000
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        fetchUrl(res.headers.location).then(resolve).catch(reject);
        return;
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
  });
}

async function getCardCount(setCode) {
  const url = `https://pocket.limitlesstcg.com/cards/${setCode}`;
  const html = await fetchUrl(url);
  // Match patterns like A1_001_EN_SM, B2a_042_EN_SM, etc.
  const regex = new RegExp(setCode + '_([0-9]+)_EN_SM', 'g');
  const matches = html.match(regex) || [];
  const nums = matches.map(m => parseInt(m.split('_')[1]));
  return nums.length > 0 ? Math.max(...nums) : 0;
}

async function getCardInfo(setCode, cardNum) {
  const url = `https://pocket.limitlesstcg.com/cards/${setCode}/${cardNum}`;
  try {
    const html = await fetchUrl(url);
    const match = html.match(/<title>([^•]+)/);
    const name = match ? match[1].trim() : `Unknown_${cardNum}`;
    return { number: cardNum, name, set: setCode };
  } catch (e) {
    return null;
  }
}

async function fetchSet(setCode) {
  console.log(`Fetching ${setCode}...`);
  const total = await getCardCount(setCode);
  console.log(`  Found ${total} cards`);
  
  if (total === 0) return [];
  
  const cards = [];
  // Process in batches
  for (let i = 1; i <= total; i += 20) {
    const batch = [];
    for (let j = i; j <= Math.min(i + 19, total); j++) {
      batch.push(getCardInfo(setCode, j));
    }
    const results = await Promise.all(batch);
    cards.push(...results.filter(r => r !== null));
    await new Promise(r => setTimeout(r, 100)); // Rate limiting
    if (i % 100 === 0 || i + 19 > total) console.log(`  ${setCode}: ${i}-${Math.min(i+19, total)}/${total}`);
  }
  
  console.log(`  Got ${cards.length} cards`);
  return cards;
}

async function main() {
  const allCards = {};
  
  for (const setCode of SETS) {
    const cards = await fetchSet(setCode);
    for (const card of cards) {
      const key = `${setCode}_${String(card.number).padStart(3, '0')}`;
      allCards[key] = { name: card.name, set: setCode, number: card.number };
    }
    await new Promise(r => setTimeout(r, 500));
  }
  
  // Save to file
  fs.mkdirSync('memory', { recursive: true });
  fs.writeFileSync('memory/ptcgp_card_names.json', JSON.stringify(allCards, null, 2), 'utf8');
  
  console.log(`\nTotal cards saved: ${Object.keys(allCards).length}`);
  console.log('Saved to memory/ptcgp_card_names.json');
}

main().catch(console.error);
