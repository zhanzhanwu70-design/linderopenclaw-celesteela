const fs=require('fs'), cheerio=require('cheerio');
const dict=require('../ptcgp_deck_dictionary.json');
const trans=n=>dict.deck_names[n]||n;
const html=fs.readFileSync('memory/ptcgp_raw_latest.html','utf8');
const $=cheerio.load(html);
const summary=$('p').filter((i,e)=>$(e).text().includes('tournaments')&&$(e).text().includes('matches')).first().text().trim();
let decks=[];
$('table.meta tr[data-share]').each((i,tr)=>{
 const t=$(tr).find('td'); const name=$(t[2]).text().trim().replace(/\s+/g,' '); if(!name) return;
 const rank=parseInt($(t[0]).text().trim(),10); const count=parseInt($(t[3]).text().trim(),10); const share=$(t[4]).text().trim();
 const record=$(t[5]).text().trim().replace(/\s+/g,' '); const win_rate=$(t[6]).text().trim();
 const m=record.match(/(\d+)\s*-\s*(\d+)\s*-\s*(\d+)/); if(!m) return;
 const wins=+m[1], losses=+m[2], ties=+m[3], total=wins+losses+ties;
 const adjusted=((wins+12)/(total+25))*100;
 decks.push({rank,name,name_zh:trans(name),count,share,record,wins,losses,ties,total,win_rate,adjusted_win_rate:adjusted.toFixed(2)+'%', adjusted});
});
const top5=decks.slice(0,5);
const adjTop=decks.filter(d=>d.total>=100).sort((a,b)=>b.adjusted-a.adjusted).slice(0,8);
const prevShare={
 'Hydreigon Mega Absol ex':8.28,'Mega Blaziken ex Castform Sunny Form':6.78,'Mega Lucario ex Igglybuff':6.50,'Zoroark ex Mega Absol ex':5.82,'Mega Altaria ex Gourgeist':5.53,'Magnezone ex Magnezone':5.50,'Mega Altaria ex Greninja':3.91
};
const trendNames=['Hydreigon Mega Absol ex','Mega Blaziken ex Castform Sunny Form','Mega Lucario ex Igglybuff','Zoroark ex Mega Absol ex','Mega Altaria ex Gourgeist','Magnezone ex Magnezone','Mega Altaria ex Greninja'];
function diffLine(n){const d=decks.find(x=>x.name===n); if(!d) return null; const now=parseFloat(d.share), prev=prevShare[n]; const diff=now-prev; const arrow=diff>=0?'📈':'📉'; return `${arrow} ${trans(n)}：${prev.toFixed(2)}% → ${d.share}（${diff>=0?'+':''}${diff.toFixed(2)}）`;}
const report=`📊 **PTCGP Meta 分析（B3 Pulsing Aura）** | 2026-05-17

資料來源：Limitless TCG 即時頁面｜${summary || '資料摘要不可得'}
公式：調整後勝率 = **(勝場 + 12) / (總場 + 25)**；平手納入總場。勝率榜只列 **樣本≥100場**。

━━━━━━━━━━━━━━━━━━━━━━
**🎯 使用率 Top 5**
${top5.map((d,i)=>`${i+1}. **${d.name_zh}** — ${d.share}｜${d.record}｜原始 ${d.win_rate}｜調整 ${d.adjusted_win_rate}`).join('\n')}

━━━━━━━━━━━━━━━━━━━━━━
**⚡ 調整後勝率 Top（樣本≥100）**
${adjTop.slice(0,6).map((d,i)=>`${i+1}. **${d.name_zh}** — 調整 ${d.adjusted_win_rate}｜${d.record}｜樣本 ${d.total}`).join('\n')}

━━━━━━━━━━━━━━━━━━━━━━
**📈 環境變化**（對照 05-14 報告）
${trendNames.map(diffLine).filter(Boolean).join('\n')}

━━━━━━━━━━━━━━━━━━━━━━
**🔎 新動向 / 讀牌重點**
- **使用率前段全面小幅回落**：Top 1 從 8.28% 降到 7.94%，環境繼續分散，沒有單一霸權牌組。
- **超級雷電獸 ex 傑拉奧拉**：樣本已到 768 場，調整勝率 **55.61%**，不是偶然；電系進攻節奏目前很乾淨。
- **甲賀忍蛙 騎拉帝納 ex**：調整勝率 **55.90%** 但樣本 136，數字漂亮，可信度還沒完全成形。先列觀察，不急著神化。
- **Mega 火焰雞 ex 漂浮泡泡**：使用率仍第2，但調整勝率 **48.95%**。熱門不等於好用，這點很基本。
- **Mega 七夕青鳥體系**：南瓜精 / 甲賀忍蛙 / 寶寶丁三線都有高於平均表現，是目前最穩定的上分骨架。

━━━━━━━━━━━━━━━━━━━━━━
**🏆 推薦排序**
1. **超級雷電獸 ex 傑拉奧拉** — 高調整勝率 + 樣本足夠，值得優先測。
2. **超級七夕青鳥 ex 南瓜精 / 甲賀忍蛙** — 使用率高、勝率穩，風險最低。
3. **自爆磁怪 ex 自爆磁怪** — 樣本 3311、調整 51.53%，不是爆發型，但穩。
4. **超級路卡利歐 ex 寶寶丁** — Top 3 使用率，調整 50.64%，可用但沒有想像中壓制。

_註：Limitless 頁面已成功更新；舊 fetch 腳本解析欄位有誤，本次以 HTML table 重新解析。_`;
fs.writeFileSync('memory/ptcgp_meta_parsed_20260517.json', JSON.stringify({date:'2026-05-17',set:'B3',summary,decks},null,2));
fs.writeFileSync('memory/ptcgp_meta_discord_20260517.md', report);
fs.writeFileSync('memory/ptcgp_meta_discord_latest.md', report);
fs.writeFileSync('memory/ptcgp_meta_latest.json', JSON.stringify({date:'2026-05-17',set:'B3',summary,decks},null,2));
console.log(report);
console.error('\nlength', report.length, 'decks', decks.length);
