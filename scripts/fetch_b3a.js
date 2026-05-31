// Fetch B3a (Paradox Drive) card data
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const SET_CODE = 'B3a';
const OUTPUT_FILE = 'memory/ptcgp_cards_full.json';

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    const req = protocol.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' },
      timeout: 20000
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
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

async function getCardCount(setCode) {
  const url = `https://pocket.limitlesstcg.com/cards/${setCode}`;
  const html = await fetchUrl(url);
  const regex = new RegExp(setCode + '_([0-9]+)_EN_SM', 'g');
  const matches = html.match(regex) || [];
  const nums = matches.map(m => parseInt(m.split('_')[1]));
  return nums.length > 0 ? Math.max(...nums) : 0;
}

async function getCardInfo(setCode, cardNum) {
  const url = `https://pocket.limitlesstcg.com/cards/${setCode}/${cardNum}`;
  try {
    const html = await fetchUrl(url);
    const titleMatch = html.match(/<title>([^•]+)/);
    const name = titleMatch ? titleMatch[1].trim() : `Unknown_${cardNum}`;
    const typeMatch = html.match(/Type[^>]*>([^<]+)</);
    const hpMatch = html.match(/HP[^>]*>([^<]+)</);
    const weaknessMatch = html.match(/Weakness[^>]*>([^<]+)</);
    const retreatMatch = html.match(/Retreat[^>]*>([^<]+)</);
    const attacksMatch = html.match(/Cost[^>]*>([^<]+)</g);
    return {
      number: cardNum,
      name,
      set: setCode,
      type: typeMatch ? typeMatch[1].trim() : '',
      hp: hpMatch ? hpMatch[1].trim() : '',
      weakness: weaknessMatch ? weaknessMatch[1].trim() : '',
      retreat: retreatMatch ? retreatMatch[1].trim() : '',
      attacks: attacksMatch ? attacksMatch.map(m => m.match(/>([^<]+)</)[1].trim()) : []
    };
  } catch (e) {
    return null;
  }
}

async function main() {
  console.log(`Fetching ${SET_CODE}...`);
  const total = await getCardCount(SET_CODE);
  console.log(`  Found ${total} cards`);

  if (total === 0) { console.log('No cards found'); return; }

  const cards = [];
  for (let i = 1; i <= total; i += 25) {
    const batch = [];
    for (let j = i; j <= Math.min(i + 24, total); j++) {
      batch.push(getCardInfo(SET_CODE, j));
    }
    const results = await Promise.all(batch);
    cards.push(...results.filter(r => r !== null));
    await new Promise(r => setTimeout(r, 200));
    console.log(`  ${Math.min(i + 24, total)}/${total}`);
  }

  console.log(`  Got ${cards.length} cards`);

  // Load existing DB
  let existing = {};
  if (fs.existsSync(OUTPUT_FILE)) {
    existing = JSON.parse(fs.readFileSync(OUTPUT_FILE, 'utf8'));
    console.log(` Existing DB: ${Object.keys(existing).length} cards`);
  }

  // Merge B3a cards
  for (const card of cards) {
    const key = `${SET_CODE}_${String(card.number).padStart(3, '0')}`;
    existing[key] = {
      name: card.name,
      set: card.set,
      number: card.number,
      type: card.type,
      hp: card.hp,
      weakness: card.weakness,
      retreat: card.retreat,
      attacks: card.attacks
    };
  }

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(existing, null, 2), 'utf8');
  console.log(`Total cards: ${Object.keys(existing).length}`);
  console.log(`Updated ${OUTPUT_FILE}`);
}

main().catch(console.error);
