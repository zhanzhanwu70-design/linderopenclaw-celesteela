const dict = require('../ptcgp_deck_dictionary.json');
const metaData = require('../memory/ptcgp_meta_latest.json');
const decks = metaData.decks;

const trans = (en) => dict.deck_names[en] || en;

const top10 = decks.slice(0, 10);
const top10wr = [...decks].sort((a,b) => parseFloat(b.adjusted_wr) - parseFloat(a.adjusted_wr)).slice(0, 10);

// Format top 10 by usage with correct emoji
const usageEmojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'];
const usageLines = top10.map((d, i) => {
  const emoji = usageEmojis[i];
  const cn = trans(d.name);
  return `${emoji} ${cn} — ${d.share_pct} (W: ${d.win_rate})`;
}).join('\n');

// Format top 10 by adjusted WR
const wrEmojis = ['🟢','🟢','🟢','🟢','🟢','🟢','🟢','🔴','🔴','🔴'];
const wrLines = top10wr.slice(0,10).map((d, i) => {
  const rank = i + 1;
  const arrow = i < 7 ? '🟢' : '🔴';
  const cn = trans(d.name);
  return `${arrow} #${rank} ${cn} — **${d.adjusted_wr}**`;
}).join('\n');

// Changes from last analysis
const changes = [];
const prev = [
  {name: 'Suicune ex Baxcalibur', share: 13.29, wr: 50.27},
  {name: 'Mega Altaria ex Greninja', share: 11.46, wr: 51.33},
  {name: 'Magnezone Bellibolt ex', share: 8.37, wr: 51.58},
  {name: 'Bellibolt ex Zeraora', share: 6.54, wr: 51.14},
  {name: 'Greninja Mega Absol ex', share: 5.97, wr: 51.77},
  {name: 'Mega Altaria ex Gourgeist', share: 5.79, wr: 53.14},
  {name: 'Hydreigon Mega Absol ex', share: 5.53, wr: 50.94},
];

top10.slice(0,7).forEach((d, i) => {
  const p = prev[i];
  const shareDiff = parseFloat(d.share_pct) - p.share;
  const wrDiff = parseFloat(d.win_rate) - p.wr;
  if (Math.abs(shareDiff) > 0.1 || Math.abs(wrDiff) > 0.3) {
    const arrow = shareDiff > 0 ? '📈' : '📉';
    changes.push(`${arrow} ${trans(d.name)}: 使用率 ${shareDiff > 0 ? '+' : ''}${shareDiff.toFixed(2)}%`);
  }
});

const changeText = changes.length > 0 ? changes.join(' | ') : '相較上次變化不大';

const date = metaData.date || '2026-03-27';

const msg = `**📊 PTCGP Meta Report | ${date} | Standard B2a**

**🔥 使用率 Top 10**

${usageLines}

**⚡ 調整後勝率排名 (Bayesian: (W+12)/(Total+25))**

${wrLines}

---
_數據來源: Limitless TCG | 調整後勝率公式: (勝場+12)/(總場+25)_

**📈 趨勢追蹤:**
${changeText}

**分析重點:**
- 水君 ex 戟脊龍 使用率仍居首，但調整後勝率中等
- 超級七夕青鳥 ex 構築多變，勝率最高(55.02%)
- 電肚蛙體系（電肚蛙 ex、自爆磁怪）仍是meta核心
- 低勝率牌組（魔幻假面喵、長耳兔）建議觀望`;

console.log(msg);
