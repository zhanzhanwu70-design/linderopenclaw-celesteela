import fetch from 'node-fetch';
import * as cheerio from 'cheerio';
import { writeFileSync } from 'fs';

async function fetchMeta() {
  const url = "https://play.limitlesstcg.com/decks?game=POCKET";
  
  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      timeout: 30000
    });
    
    const html = await response.text();
    const $ = cheerio.load(html);
    
    const decks = [];
    
    // Try multiple selectors for Limitless
    const deckSelectors = [
      '.deck-card',
      '[class*="deck"]',
      '.tournament-deck',
      'article',
      '.card'
    ];
    
    // Look for deck entries - try to find any ranked list
    const allElements = $('*');
    let deckCount = 0;
    
    // Try finding by text patterns - deck names usually contain "ex" or specific patterns
    $('a[href*="deck"]').each((i, el) => {
      if (deckCount >= 20) return;
      const name = $(el).text().trim();
      const parent = $(el).parent();
      const grandparent = parent.parent();
      const container = grandparent.parent();
      const text = container.text();
      
      if (name && name.length > 3 && name.length < 60) {
        // Extract percentages
        const usageMatch = text.match(/([\d.]+)%/);
        const usage = usageMatch ? usageMatch[1] + '%' : 'N/A';
        
        // Extract win/loss
        const recordMatch = text.match(/(\d+)\s*-\s*(\d+)/);
        let wins = 0, losses = 0, winRate = 'N/A';
        if (recordMatch) {
          wins = parseInt(recordMatch[1]);
          losses = parseInt(recordMatch[2]);
          const total = wins + losses;
          if (total > 0) winRate = ((wins / total) * 100).toFixed(2) + '%';
        }
        
        // Bayesian adjusted
        let adjWinRate = 'N/A';
        if (wins + losses > 0) {
          const priorGames = 25, priorWins = 12;
          adjWinRate = ((wins + priorWins) / (wins + losses + priorGames) * 100).toFixed(2) + '%';
        }
        
        // Check if it's a Pocket deck (has ex, Mega, etc.)
        if (name.includes('ex') || name.includes('Mega') || name.includes('Pika') || name.length < 30) {
          decks.push({
            rank: deckCount + 1,
            name,
            usage_rate: usage,
            win_rate: winRate,
            record: `${wins} - ${losses}`,
            adjusted_win_rate: adjWinRate,
            sample_size: wins + losses
          });
          deckCount++;
        }
      }
    });
    
    // Fallback: try to get from JSON data embedded in page
    if (decks.length === 0) {
      const scriptMatch = html.match(/window\.__INITIAL_STATE__\s*=\s*({.+?});/s);
      const jsonMatch = html.match(/type="application\/json">(.+?)</);
      
      if (jsonMatch) {
        try {
          const data = JSON.parse(jsonMatch[1]);
          // Try to extract deck data
          console.log('Found JSON data in page');
        } catch (e) {}
      }
    }
    
    // Save raw HTML for debugging
    const workspacePath = '/home/node/.openclaw/workspace-celesteela';
    writeFileSync(`${workspacePath}/memory/ptcgp_raw_latest.html`, html);
    
    const result = {
      update_time: new Date().toISOString(),
      top_decks: decks
    };
    
    writeFileSync(`${workspacePath}/memory/ptcgp_meta_latest.json`, JSON.stringify(result, null, 2));
    
    console.log(`Found ${decks.length} decks`);
    console.log(JSON.stringify(decks.slice(0, 5), null, 2));
    
    return decks;
    
  } catch (e) {
    console.error('Error:', e.message);
    return [];
  }
}

fetchMeta();
