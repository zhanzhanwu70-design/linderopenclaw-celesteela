#!/usr/bin/env node
/**
 * PTCGP Meta 分析腳本
 * 從 Limitless TCG 取得資料，計算調整後勝率
 */

import { writeFileSync } from 'fs';

// Bayesian prior 參數
const PRIOR_WINS = 12;
const PRIOR_GAMES = 25;

/**
 * 計算 Bayesian 調整後勝率
 * 調整後勝率 = (勝場 + 12) / (總場 + 25)
 */
function calcAdjustedWR(wins, losses, draws = 0) {
    const total = wins + losses + draws;
    if (total === 0) return null;
    return (wins + PRIOR_WINS) / (total + PRIOR_GAMES);
}

/**
 * 解析 Limitless HTML 表格
 */
function parseLimitlessHTML(html) {
    const decks = [];
    
    // 使用正規表達式解析每一行
    // 格式: rank [name](link) deck_count share% [record] [wr%]
    const rowPattern = /(\d+)\[([^\]]+)\]\([^\)]+\)(\d+)([\d.]+)%\[(\d+)\s*-\s*(\d+)(?:\s*-\s*(\d+))?\]\[([\d.]+)%\]/g;
    
    let match;
    while ((match = rowPattern.exec(html)) !== null) {
        const rank = parseInt(match[1]);
        const name = match[2];
        const deckCount = parseInt(match[3]);
        const share = parseFloat(match[4]);
        const wins = parseInt(match[5]);
        const losses = parseInt(match[6]);
        const draws = match[7] ? parseInt(match[7]) : 0;
        const rawWR = parseFloat(match[8]);
        
        const total = wins + losses + draws;
        const adjWR = calcAdjustedWR(wins, losses, draws);
        
        decks.push({
            rank,
            name,
            deckCount,
            share,
            wins,
            losses,
            draws,
            total,
            rawWR,
            adjWR: adjWR !== null ? (adjWR * 100).toFixed(2) + '%' : 'N/A'
        });
    }
    
    return decks;
}

// 測試解析 (用已知的 HTML 結構)
const testHTML = `
1[Suicune ex Baxcalibur](/decks/suicune-ex-a4a-baxcalibur-b2a?game=POCKET)163513.22%[4480 - 4248 - 187]50.25%
2[Mega Altaria ex Greninja](/decks/mega-altaria-ex-b1-greninja-a1?game=POCKET)143311.59%[4110 - 3684 - 202]51.40%
3[Magnezone Bellibolt ex](/decks/magnezone-b1a-bellibolt-ex-b2a?game=POCKET)10768.70%[3158 - 2789 - 157]51.74%
`;

const decks = parseLimitlessHTML(testHTML);
console.log('Parsed decks:', JSON.stringify(decks, null, 2));

// 測試計算
console.log('\n--- Bayesian Adjustment Test ---');
console.log('Suicune ex: (4480 + 12) / (8915 + 25) =', (4480 + 12) / (8915 + 25));
console.log('Expected raw: 50.25%, Adjusted should be closer to 48%');
