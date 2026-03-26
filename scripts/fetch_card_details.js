const https = require('https');
const fs = require('fs');

const SETS = ['A1', 'A1a', 'A2', 'A2a', 'A2b', 'A3', 'A3a', 'A3b', 'A4', 'A4a', 'A4b', 
              'B1', 'B1a', 'B2', 'B2a', 'P-A', 'P-B'];

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {
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
    }).on('error', reject);
  });
}

function parseCardData(html, setCode, cardNum) {
  const card = {
    set: setCode,
    number: cardNum,
    name: '',
    type: '',
    hp: 0,
    weakness: '',
    retreat: 0,
    attacks: []
  };

  // Extract from title section
  const start = html.indexOf('card-text-title');
  if (start === -1) return card;
  
  const section = html.substring(start, start + 800);
  
  // Extract name - it's between > and < in card-text-name
  const nameMatch = section.match(/card-text-name[^>]*><a[^>]*>([^<]+)</);
  if (nameMatch) card.name = nameMatch[1].trim();
  
  // Find type and HP: look for pattern "- Type - XX HP"
  const typeHpPattern = section.match(/- ([A-Za-z]+)\s*- (\d+)\s*HP/);
  if (typeHpPattern) {
    card.type = typeHpPattern[1].trim();
    card.hp = parseInt(typeHpPattern[2]);
  }

  // Extract weakness
  const weakMatch = html.match(/Weakness:\s*([A-Za-z]+)/);
  if (weakMatch) card.weakness = weakMatch[1].trim();

  // Extract retreat
  const retreatMatch = html.match(/Retreat:\s*(\d+)/);
  if (retreatMatch) card.retreat = parseInt(retreatMatch[1]);

  // Extract attacks - look for energy symbols and damage
  const energyMatches = section.match(/ptcg-symbol[^>]*>([^<]+)/g);
  if (energyMatches) {
    card.attacks = energyMatches.slice(0, 4).map(e => {
      const m = e.match(/>([^<]+)/);
      return m ? m[1].trim() : '';
    }).filter(e => e.length > 0 && e.length < 5);
  }

  // Extract damages
  const damageMatches = section.match(/Damage:\s*(\d+)/g);
  if (damageMatches) {
    card.damages = damageMatches.map(d => parseInt(d.match(/\d+/)[0]));
  }

  return card;
}

async function getCardCount(setCode) {
  const html = await fetchUrl(`https://pocket.limitlesstcg.com/cards/${setCode}`);
  const regex = new RegExp(setCode + '_([0-9]+)_EN_SM', 'g');
  const matches = html.match(regex) || [];
  const nums = matches.map(m => parseInt(m.split('_')[1]));
  return nums.length > 0 ? Math.max(...nums) : 0;
}

async function fetchCardDetail(setCode, cardNum) {
  const url = `https://pocket.limitlesstcg.com/cards/${setCode}/${cardNum}`;
  try {
    const html = await fetchUrl(url);
    return parseCardData(html, setCode, cardNum);
  } catch (e) {
    return null;
  }
}

async function fetchSetDetails(setCode) {
  console.log(`Fetching ${setCode}...`);
  const total = await getCardCount(setCode);
  
  const cards = [];
  for (let i = 1; i <= total; i += 25) {
    const batch = [];
    for (let j = i; j <= Math.min(i + 24, total); j++) {
      batch.push(fetchCardDetail(setCode, j));
    }
    const results = await Promise.all(batch);
    cards.push(...results.filter(r => r !== null));
    await new Promise(r => setTimeout(r, 100));
    
    if (i % 100 === 0 || i + 24 >= total) {
      console.log(`  ${i}-${Math.min(i+24, total)}/${total}`);
    }
  }
  
  console.log(`  Got ${cards.length} cards`);
  return cards;
}

async function main() {
  const allCards = {};
  
  for (const setCode of SETS) {
    const cards = await fetchSetDetails(setCode);
    for (const card of cards) {
      const key = `${setCode}_${String(card.number).padStart(3, '0')}`;
      allCards[key] = card;
    }
    await new Promise(r => setTimeout(r, 400));
  }
  
  // Save to file
  fs.mkdirSync('memory', { recursive: true });
  fs.writeFileSync('memory/ptcgp_cards_full.json', JSON.stringify(allCards, null, 2), 'utf8');
  
  // Stats
  const typeCount = {};
  const totalHP = {};
  
  for (const [key, card] of Object.entries(allCards)) {
    if (card.type) typeCount[card.type] = (typeCount[card.type] || 0) + 1;
  }
  
  console.log('\n=== Summary ===');
  console.log(`Total: ${Object.keys(allCards).length} cards`);
  console.log('By type:', typeCount);
  console.log('\nSaved to memory/ptcgp_cards_full.json');
}

main().catch(console.error);
