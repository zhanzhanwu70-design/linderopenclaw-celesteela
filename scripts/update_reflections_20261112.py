from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/reflections.md')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'

block = r'''
## 2026-11-12 正式驗證 PRED_20261110（檢查日 2026-11-12） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **環境狀態**：C1 Standard 53 錦標賽／6,711 玩家／20,618 對局（昨 50／6,413／19,770，**+3 錦標賽／+298 玩家／+848 對局／+4.29%**）；分支 **568 條**／合併 **181 條**（昨 552／178），全環境加權 AWR **48.89%**（昨 48.91%）。**連續第三個低增量日**（<1,000 對局）。B4a 頁面仍**凍結**於 210／15,008／38,924（自 10-28 起連續十六天）。Standard 與 set=C1 頁逐 slug 一致。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（超級路卡利歐 ex 合併 AWR <52.0%）：✅ **命中**。51.71→**51.62%**，連兩日低於門檻；份額 5.41→5.27% 轉跌，族群（格鬥／草／鋼系 AWR 49.38%）同向，靶心效應第四日。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（自爆磁怪合併份額 ≥3.8%）：❌ **未命中**。3.54→**3.59%**，動能 +0.97→+0.31→+0.21→**+0.05pt** 逐日衰減到幾近停滯。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（超級甲賀忍蛙 ex 合併份額 <8.0%）：✅ **命中**。7.94→**7.73%**，七連降延續，AWR 43.47→43.49% 持平。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **結果：2/3。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 核心反省（新增三條規則） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
1. **擴張型條件必須在「設定當天」就檢查動能是否進入衰退期**。B（自爆磁怪份額 ≥3.8%）的門檻距離 0.47pt 落在份額帶內、預計天數也算得出來，但動能在四天內衰減 95%（+0.97→+0.31→+0.21→+0.05pt）——**設定當天看到的 +0.31pt 動能，其實已是衰退期的尾聲**。→ **新規則：擴張型條件（門檻高於當前值）設定時，必須同時寫出「動能的三日變化率」；若動能連兩日衰減 >30%，該條件的機率上限壓到 0.30 以下，且不得作為「最大機率」。**本條使今日 PRED_20261112 的 A（超夢 X 份額擴張）機率上限定在 0.35，且必須用第二個獨立指標（N 佔全環境比重）交叉確認。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
2. **「近兩日已用（牌組, 指標）」必須逐條比對，不能靠記憶**。PRED_20261111 違反了 11-11 自己訂的「同一牌組同一指標不得連續兩日使用」規則——忍蛙份額 11-10 用 <8.0%、11-11 又用 <7.5%。**這是規則落地第二次失敗**（第一次是 11-03 的門檻距離規則，11-04 又重寫一次）。→ **新規則：每次設定預測前，先把近兩日已用的（牌組, 指標）配對列出來逐條排除，並寫進預測腳本的註解。**本日 PRED_20261112 已排除：忍蛙份額、蜂女王 AWR、水君份額、路卡利歐 AWR、自爆磁怪份額。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
3. **低增量日的單日份額跳動，必須用「N 佔全環境比重」驗證真實性**。今日 +848 對局下，超級超夢 X ex 單日份額 +0.48pt（全環境最大）。若只看份額，低增量日的單場錦標賽就能製造假突破。驗證方式：**看該牌的 N 佔全環境 N 的比重是否同步上升**——超夢X 3.62%→3.77%→**4.19%**，比例正常 → 判為真實擴張。→ **新規則：低增量日（<1,000 對局）任何單日份額跳動 >0.4pt 者，必須做 N 佔比驗證，未通過者一律視為單場噪音。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 流程教訓 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **`scripts/verify_mu_20261112.py` 再次攔下方向錯誤**：今日草稿把「蜂女王 ex 壓超級路卡利歐 ex 70.5%」寫反（實際是路卡利歐壓蜂女王 70.5%），並把「A 輸 B」的數值誤用成 100−A 的勝率。正確口徑是「A 輸 B p%」＝ **B 那一列的勝率**（平局會讓兩列之和小於 100%）。**今日 5 條敘述被抓出錯誤，修正後 55 條全數通過。** → 對位敘述必須在寫報告前就由覆核腳本產生，不可手寫後再驗。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **字典補譯 27 條，全部由既有官方卡名分段組合**（`scripts/fill_missing_zh_20261112.py`），無即興機翻；deck_names 730→757，version 4.12，缺翻譯歸零。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 低增量日對位網凍結可量化：55 條主要對線僅 **4 條**移動 >1.5pt。→ **對位追查門檻自今日起改為 |Δ|≥1.5pt**（11-11 訂的是 AWR 跳動 ≥1.0pt 才追查對位）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 今日新發現 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
1. **超級超夢 X ex 是全環境唯一的「份額升、強度跌」背離**：份額 4.13→4.26→**4.74%**（單日 +0.48pt），AWR 47.94→48.31→**47.38%**（單日 −0.93pt）。N 佔比 3.62%→**4.19%** 同步上升 → 真實擴張。**「份額加速 = 環境靶心」規則的最新樣本**（11-10 的規則原型是路卡利歐 ex 的 +1.86／+3.08 → 次日反轉）。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
2. **份額王超級噴火龍 Y ex 正在強化對位，這是自爆磁怪份額動能歸零的直接原因**：壓自爆磁怪 52.5→**54.5%**（N 122→134）、壓三首惡龍 41.7→**43.5%**（N 60→62）、壓月亮伊布 47.9→**48.9%**（N 213→225）；輸水君 25.3→**25.8%**、輸胡帕 42.1→**41.1%**。**→ 新觀察：AWR 冠軍的份額天花板，不只由自己的剋星決定，還要看「份額王的對位面是否在強化」。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
3. **水君 ex 是環境中唯一對份額王有 70% 壓制力的牌組**：壓超級噴火龍 Y ex **70.3%**（N=236）、忍蛙 68.7%、月亮伊布 67.2%、蜥蜴王 57.5%；但輸蜂女王 69.9%、胡帕 41.8%。水君份額三連降到 7.88%、AWR 卻升到 51.71%（全環境第六）——**它是被低估的反制核心，不是退坑牌組**。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
4. **兩種退坑必須分開標籤**：忍蛙系七連降到 7.73%、AWR 43.49%（低於大盤 5.40pt），但同家族普通忍蛙線回補，**家族合計只由 12.81% 降到 12.38%**；相對地，**超能系族群七連降到 10.51% 且族群 AWR 48.23% 低於大盤 48.89%**（沒有人接手）→ 真退坑。**判準：族群合併 AWR 是否高於大盤，分辨「真退坑」與「份額外流」。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
5. **C1 新包拖累差距擴大到 3.23pt**（2.96→3.06→**3.23**，單日 +0.17pt 為 11-09 以來最大），含新卡份額 52.21→51.91% 續降、AWR 47.03% 微跌 → 擴充包仍未轉正。**「新卡 vs 舊卡差距擴大」已連三日照 11-05 訂的「連兩日收斂且每日 ≥0.3pt」反向收斂** → 該條件已可判定為 C1 換包期結構性落後，不再列入「觀察待轉」。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
6. **厚度稅把份額推向薄血牌組**：130–160HP 份額升至 **41.92%**（AWR 50.74%），210+HP 20.97%（47.46%）。240HP 超級快龍 ex 36.15%、240HP 超級班基拉斯 ex 42.49% 是極端值；150HP 自爆磁怪 55.07%、140HP 蜂女王 ex 54.26% 是技能與對位蓋過厚度的例外。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
7. **環境已連續第二日無新突襲線**：合併頁無新列突破 0.15%，分支口徑無份額 ≥0.15% 新進榜；退出前 40 的只有「三首惡龍 超級勾魂眼ex」（昨 0.45%）與「超級妙蛙花ex 妙蛙花」（昨 0.42%）。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### PRED_20261111 內檢（正式檢查日 2026-11-13） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（蜂女王 ex 合併 AWR <54.0%）：⏳ **逼近中**。54.59→**54.26%**，距門檻僅 **0.26pt**；四連降，動能 −0.21→−0.33pt 反而略升。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（超級甲賀忍蛙 ex 合併份額 <7.5%）：⏳ **逼近中**。7.94→**7.73%**，距門檻 **0.23pt**；動能 −0.44→−0.21pt 略減；同家族普通忍蛙線仍小幅回補。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（水君 ex 合併份額 <7.5%）：⏳ **逼近中**。7.95→**7.88%**，距門檻 **0.38pt**；動能 −0.22→−0.07pt 趨緩最明顯；AWR 反升 51.47→51.71%，屬純份額外流。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 內檢結果：逼近中 3、已破 0；正式命中率仍以 2026-11-13 檢查日為準。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

## 2026-11-12 新預測 PRED_20261112（檢查日 2026-11-14） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（0.35）超級超夢 X ex 合併份額 **≥5.1%**：今日 4.74%，距離 0.36pt（份額帶 0.3～0.8pt 內）；預計天數 0.36 ÷ 0.185（四日均動能）≈ **1.9 天**；方向 4.00→4.12→4.13→4.26→**4.74%** 五連升，單日 +0.48pt 為全環境最大，N 佔全環境比重 3.62→3.77→**4.19%** 同向上升（依 11-12 新規則通過真實性驗證）。**擴張型門檻歷史命中率偏低，且動能未進入衰退期，故機率上限定在 0.35。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（0.30）超級雷電獸 ex 合併 AWR **<50.0%**：今日 50.56%，距離 0.56pt（AWR 帶 0.5～1.5pt 內）；預計天數 0.56 ÷ 0.275（近兩日動能）≈ **2.0 天**；方向 52.76→51.22→51.11→50.71→**50.56%** 四連降，份額 4.02→4.18→3.99→**3.86%** 同步四連降 → 真退坑型（份額與強度同跌，非純外流）。族群（電系 AWR 49.66%）仍高於大盤，屬族群內部分化，AWR 型條件不降級。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（0.25）超能系族群合併份額 **<10.2%**：今日 10.51%，距離 0.31pt（份額帶下緣）；預計天數 0.31 ÷ 0.183（近三日動能）≈ **1.7 天**；方向 12.39→…→10.88→10.62→**10.51%** 七連降，族群 AWR **48.23%** 低於大盤 48.89% 且未回升 → 真退坑而非純份額外流。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 最大機率：A。信心：中。三條皆為單條件方向型，距離落在對應指標帶內、預計天數 ≤2 天，且（牌組, 指標）組合皆未在近兩日使用過。本日為連續第三個低增量日，擴張／崩壞型條件的實現率偏低，整體信心維持中。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
'''

s = P.read_text(encoding='utf-8')
if '## 2026-11-12 正式驗證 PRED_20261110' in s:
    print('already present, skip')
else:
    s = s.rstrip() + '\n' + block
    P.write_text(s, encoding='utf-8')
    print('reflections.md updated, len =', len(s))
