# SKILL.md - 寶可夢 TCG Pocket Meta 分析技能

## 觸發條件
當用戶要求分析寶可夢 TCG Pocket Meta、查詢強勢牌組、或需要每日 Meta 更新時使用此技能。

## 資料來源
- 主要來源: `https://play.limitlesstcg.com/decks?game=POCKET`
- 格式: Standard, Set B2a

## 分析方法

### 1. 使用率排名 (Top 10 by Usage)
直接取用 deck count 最高的前 10 名。

### 2. 調整後勝率排名 (Top 10 by Adjusted Win Rate)
使用 Bayesian 調整公式，避免樣本過小導致的偏差。

### 📐 調整後勝率公式

| 參數 | 值 |
|------|-----|
| 預設場次 (prior_games) | 25 場 |
| 預設勝場 (prior_wins) | 12 場 |
| 預設勝率 (prior_wr) | 48% |

**公式:**
```
調整後勝率 = (勝場 + 12) / (總場 + 25)
```

### 3. 資料解析
從 Limitless 取得的原始資料格式：
- 排名
- 牌組名稱
- 牌組數量 (deck_count)
- 佔有率 (share %)
- 戰績 (wins-losses-draws)
- 原始勝率 (win %)

## 牌組名稱翻譯對照

> ⚠️ **重要**: 字典檔案位於 `ptcgp_deck_dictionary.json`，分析時優先從該檔案讀取翻譯。

分析時將英文牌組名翻譯為中文：

| 英文名稱 | 中文翻譯 |
|----------|----------|
| Suicune ex Baxcalibur | 水君 ex 喇叭芽 ex |
| Mega Altaria ex Greninja | 超級七夕青鳥 ex 忍者龍 ex |
| Magnezone Bellibolt ex | 自爆磁怪 電肚蛙 ex |
| Bellibolt ex Zeraora | 電肚蛙 ex 索爾迦雷歐 |
| Greninja Mega Absol ex | 忍者龍 超級太陽伊貝 ex |
| Hydreigon Mega Absol ex | 三首惡龍 超級太陽伊貝 ex |
| Mega Altaria ex Gourgeist | 超級七夕青鳥 ex 南瓜精 |
| Mega Altaria ex Chingling | 超級七夕青鳥 ex 鈴鐺響 |
| Meowscarada ex Meowscarada | 魔幻假面喵 ex |
| Mega Lopunny ex Annihilape | 超級長耳兔 ex 棄世猴 ex |
| Mega Charizard Y ex Entei ex | 超級噴火龍 Y ex 炎帝 ex |
| Gourgeist Houndstone | 南瓜精 腫頭龍 |
| Suicune ex Greninja ex | 水君 ex 忍者龍 ex |
| Alolan Ninetales ex Baxcalibur | 阿羅拉九尾 ex 喇叭芽 ex |
| Bellibolt ex Magnezone | 電肚蛙 ex 自爆磁怪 |
| Mega Altaria ex | 超級七夕青鳥 ex |
| Magnezone Oricorio | 自爆磁怪 舞天使 |
| Mega Gardevoir ex Meloetta | 超級沙奈朵 ex 美錄梅塔 |
| Gholdengo ex Dialga ex | 銀阿爾宙斯 ex 帝牙盧卡 ex |
| Gholdengo ex Orthworm | 銀阿爾宙斯 ex 幾何雪絨蛾 |
| Greninja Oricorio | 忍者龍 舞天使 |
| Leafeon ex Teal Mask Ogerpon ex | 葉伊布 ex 偽裝外套 omatato ex |
| Mega Blaziken ex Heatmor | 超級火焰雞 ex 熔蟻獸 |
| Melmetal ex Melmetal | 瑪機利馬 ex |
| Giratina ex Darkrai ex | 騎拉帝納 ex 暗裂導師 ex |
| Mimikyu ex Greninja | 謎擬 Q ex 忍者龍 |
| Mega Absol ex Darkrai ex | 超級太陽伊貝 ex 暗裂導師 ex |

## 輸出格式

### Discord 格式 (無表格，用 bullet list)

所有輸出皆使用中文，包含：
- 標題、分類、使用說明皆為中文
- 牌組名稱使用上方翻譯對照表
- 數據說明（場次、戰績、勝率）皆為中文

```
📊 **寶可夢 TCG Pocket 環境分析** | {日期}

**🔥 使用率前十名**
1. [中文牌組名] - {deck_count} 牌組 (佔有率 {share}%)
2. ...

**⚡ 調整後勝率前十名** (Bayesian 公式)
1. [中文牌組名] - {adj_wr}% (原始: {raw_wr}%) | 戰績 {w}-{l}-{d}
2. ...

📐 調整公式: (勝場 + 12) / (總場 + 25)
📖 說明: 小樣本牌組會向 48% 收斂，樣本越大越接近原始勝率
🔗 資料來源: play.limitlesstcg.com
```

## 執行步驟

1. **抓取資料**: 使用 web_fetch 取得 `https://play.limitlesstcg.com/decks?game=POCKET`
2. **解析 HTML**: 擷取各牌組的 deck_count、wins、losses、draws
3. **翻譯牌組名**: 依上方對照表將英文名轉為中文
4. **計算調整後勝率**: 使用 Bayesian 公式
5. **排序輸出**: 分別排出使用率和調整後勝率各 Top 10
6. **格式化輸出**: 轉為 Discord 相容中文格式

## 注意事項
- Discord 不支援 Markdown 表格，用 bullet list 代替
- 調整後勝率可消除小樣本牌組的偏差
- 牌組翻譯以上方對照表為準，若有未收錄牌組請使用英文原名
- 輸出時加入視覺化分隔線提昇可讀性

## 範例輸出

```
📊 **寶可夢 TCG Pocket 環境分析** | 2026-03-21

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 使用率前十名
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. 水君 ex 喇叭芽 ex - 1635 牌組 (13.22%)
 2. 超級七夕青鳥 ex 忍者龍 ex - 1433 牌組 (11.59%)
 3. 自爆磁怪 電肚蛙 ex - 1076 牌組 (8.70%)
 4. 電肚蛙 ex 索爾迦雷歐 - 783 牌組 (6.33%)
 5. 忍者龍 超級太陽伊貝 ex - 737 牌組 (5.96%)
 6. 三首惡龍 超級太陽伊貝 ex - 693 牌組 (5.60%)
 7. 超級七夕青鳥 ex 南瓜精 - 652 牌組 (5.27%)
 8. 超級七夕青鳥 ex 鈴鐺響 - 233 牌組 (1.88%)
 9. 魔幻假面喵 ex - 209 牌組 (1.69%)
10. 超級長耳兔 ex 棄世猴 ex - 194 牌組 (1.57%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ 調整後勝率前十名 (Bayesian 公式)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 公式: (勝場 + 12) / (總場 + 25)

 1. 超級七夕青鳥 ex 南瓜精 - 53.57% (原始: 53.61%) | 1961-1581-116
 2. 忍者龍 超級太陽伊貝 ex - 51.94% (原始: 51.97%) | 2114-1862-92
 3. 自爆磁怪 電肚蛙 ex - 51.72% (原始: 51.74%) | 3158-2789-157
 4. 超級七夕青鳥 ex 忍者龍 ex - 51.39% (原始: 51.40%) | 4110-3684-202
 5. 三首惡龍 超級太陽伊貝 ex - 50.92% (原始: 50.94%) | 1961-1807-82
 6. 電肚蛙 ex 索爾迦雷歐 - 50.90% (原始: 50.92%) | 2134-1954-103
 7. 水君 ex 喇叭芽 ex - 50.25% (原始: 50.25%) | 4480-4248-187
 8. 超級七夕青鳥 ex 鈴鐺響 - 50.12% (原始: 50.16%) | 615-571-40
 9. 超級長耳兔 ex 棄世猴 ex - 42.89% (原始: 42.75%) | 401-529-8
10. 魔幻假面喵 ex - 42.23% (原始: 42.08%) | 401-543-9

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 分析筆記
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 使用率冠軍: 水君 ex 喇叭芽 ex 獨佔 13.22% 市場
• 勝率冠軍: 超級七夕青鳥 ex 南瓜精 調整後 53.57%
• 電系強勢: 自爆磁怪 / 電肚蛙 組合統治環境
• 超級七夕青鳥: 在多個組合中出現，是目前最泛用的超級進化
```
