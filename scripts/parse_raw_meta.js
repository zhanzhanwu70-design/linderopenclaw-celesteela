const cheerio = require('cheerio');
const fs = require('fs');
const html = fs.readFileSync('memory/ptcgp_raw_latest.html', 'utf8');
const $ = cheerio.load(html);
const rows = $('table.meta tr');
const decks = [];
rows.each((i, row) => {
  if (i === 0) return;
  const cells = $(row).find('td');
  if (cells.length < 5) return;
  const rank = $(cells[0]).text().trim();
  const name = $(cells[2]).find('a').text().trim();
  const usage = $(cells[4]).text().trim();
  const winRate = $(cells[cells.length-1]).text().trim();
  const record = cells.length > 5 ? $(cells[cells.length-2]).text().trim() : '';
  const share = $(row).attr('data-share') || '';
  if (name && usage !== 'N/A') {
    decks.push({ rank, name, usage, winRate, record, share });
  }
});
// Sort by share descending, take top 20
decks.sort((a, b) => parseFloat(b.share) - parseFloat(a.share));
const top20 = decks.slice(0, 20);
console.log(JSON.stringify(top20, null, 2));
