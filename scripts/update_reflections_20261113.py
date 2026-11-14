from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/reflections.md')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'

block = r'''
## 2026-11-13 正式驗證 PRED_20261111（檢查日 2026-11-13） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **環境狀態**：C1 Standard 57 錦標賽／7,091 玩家／21,598 對局（昨 53／6,711／20,618，**+4 錦標賽／+380 玩家／+980 對局／+4.75%**）；分支 **583 條**／合併 **182 條**（昨 568／181），全環境加權 AWR **48.89%**（持平）。**連續第四個低增量日**（<1,000 對局）。B4a 頁面仍**凍結**於 210／15,008／38,924（自 10-28 起連續十七天）。Standard 與 set=C1 頁逐 slug 一致。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（蜂女王 ex 合併 AWR <54.0%）：❌ **未命中**。54.59→54.26→**54.26%**，距門檻 0.26pt；動能 −0.21→−0.33→**0.00pt 歸零**。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（超級甲賀忍蛙 ex 合併份額 <7.5%）：❌ **未命中**。7.94→7.73→**7.63%**，距門檻 0.13pt；動能 −0.44→−0.21→**−0.10pt 腰斬**。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（水君 ex 合併份額 <7.5%）：❌ **未命中**。7.95→7.88→**7.91%**，距門檻 0.41pt；動能 −0.22→−0.07→**+0.03pt 方向反轉**，AWR 反而升到 51.73%。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **結果：0/3 全滅。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 核心反省（新增三條規則） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
1. **內檢必須比對「動能」，不能只比對「距離」**。三條條件的距離（0.26／0.13／0.41pt）全在低增量日的 0.5pt 允許帶內，11-12 的內檢因此把三條都標成「逼近中」——但當時動能已經分別是「略升／腰斬／趨緩」，等於把三條即將失效的條件都標成健康。**「逼近」不等於「會到」：動能是決定性變數，距離只是必要條件。** → **新規則：內檢時每條條件必須寫出「當日動能值」與「動能衰減率（今日 ÷ 前日）」；衰減 >50%、衰減後預估天數 >檢查期、或方向反轉者，直接降級為「本檢查日不可能命中」，不得標記「逼近中」。** 這是規則落地第三次失敗（前兩次：11-03 門檻距離規則、11-11 同指標連用規則），也是同一套框架連續第二次近乎全滅。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
2. **份額擴張型條件必須拆到分支層驗證「擴張品質」**。PRED_20261112 的 A（超級超夢 X ex 份額 ≥5.1%）在 11-12 用 N 佔比驗證通過（3.62→3.77→4.19%），今日卻被拆分支推翻：合併份額 4.74→4.78%（動能 +0.48→**+0.04pt**，衰減 92%），N 佔比 4.19→**4.14%** 微降，且**強線「超級超夢Xex 夢幻ex」3.26→3.16%／48.45% 反而縮水，份額全由弱線「超級超夢Xex 超級蒂安希ex」0.82→0.94%／45.88% 獨撐**。→ **新規則：份額擴張型條件在「設定」與「驗證」兩端都要列出主分支 vs 次分支的份額與 AWR 對照；若擴張只發生在 AWR 低於合併值的分支，判定為「低品質擴張」，門檻不得再上調，且該條件機率上限壓到 0.30 以下。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
3. **門檻距離要設在「動能衰減後的預估天數 ≤1.5 天」，而不是卡在一步之遙**。三條失敗條件的距離分別是 0.26／0.13／0.41pt——都屬於「差一口氣」的位置，一旦動能反轉就整個作廢；而 11-12 命中的兩條（路卡利歐 AWR、忍蛙份額）距離分別是 0.62pt 與 0.21pt，前者是「已經站在門檻另一邊」、後者是「四連降的強延續型」。→ **新規則：門檻設定時，若預估天數 >1.5 天，寧可把距離放寬到 0.4～0.6pt 的方向型，也不要設 0.1～0.3pt 的近門檻型；近門檻型必須搭配「動能衰減 <30%」與「同一指標連續 ≥3 日同向」兩個額外條件才可使用。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 流程教訓 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **`scripts/verify_mu_20261113.py` 攔下 10 條方向錯誤**：今日草稿把「路卡利歐 ex 輸 噴火龍 Y ex」誤填成自己的勝率 47.4%（實際對手列 50.4%）、把「胡帕 ex 輸 噴火龍 Y ex」誤標成輸（實際胡帕 54.0% 是贏）、把「噴火龍 Y ex 壓 自爆磁怪」寫成 44.1%（實際是噴火龍自己那列 53.8%）、把「騎拉帝納 ex 輸 蜂女王 ex」寫成 63.9%（實際騎拉帝納是贏 63.9%）。**修正後 76 條全數通過。** → 延續 11-12 的結論：對位敘述必須由覆核腳本產生方向，不可手寫。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **字典補譯 9 條**（`scripts/fill_missing_zh_20261113.py`），全部由既有官方卡名分段組合、無即興機翻；deck_names 757→766，version 4.13，缺翻譯歸零。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 低增量日對位網凍結再度量化：55 條主要對線僅 **5 條**移動 >1.5pt（昨 4 條），且大樣本對線（N≥150）只有胡帕 vs 噴火龍 Y 一條移動（−1.7pt）→ 對位追查門檻 |Δ|≥1.5pt 繼續有效。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 今日新發現 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
1. **超級七夕青鳥 ex 是今日唯一「份額與強度同步回升」的主流線**：份額 7.19→7.05→**7.25%**（三連降後反彈），AWR 53.51→53.83→**53.93%**（四連升）。**反彈由「超級七夕青鳥ex 甲賀忍蛙」分支帶動（2.88→3.14%／53.97%），太陽伊布分支反而微降（3.74→3.67%／54.99%）** → **分支層的分化比合併層更有資訊量：合併值上升不代表所有分支都變好。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
2. **自爆磁怪是「AWR 冠軍 + 份額動能重新加速」的靶心型初期**：AWR 55.54→55.02→**54.69%** 兩連跌（冠軍差距收斂到 0.43pt），但份額 3.59→**3.65%**、動能 +0.05→**+0.06pt** 轉為加速。與超級路卡利歐 ex 的五日樣本（「份額先衝、AWR 後跌」）同構，是 11-10 那條規則的早期指徵。**→ 新觀察：靶心效應的預警順序是「份額動能先轉正、AWR 後續跌」，只看 AWR 會晚一步。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
3. **份額王超級噴火龍 Y ex 的對位面持續擴張，今日同時壓住兩條高 AWR 線**：壓自爆磁怪 53.8%（N=143，自身 43.3→44.1%）、壓三首惡龍 54.4%（N=68）、壓超級甲賀忍蛙 ex 51.9%（N=135）；輸水君 ex 69.9%（N=249）。**→ 延伸 11-12 的規則：AWR 冠軍的份額天花板不只由自己的剋星決定，還要看份額王的對位面是否在強化；今日自爆磁怪與三首惡龍的 AWR 同跌，直接對應噴火龍 Y 的對位強化。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
4. **「份額外流」與「退坑」的判準再次得到驗證，但這次要加分支層**：忍蛙系超級線份額八連降到 7.63%、AWR 43.52%（低於大盤 5.37pt），但**家族合計僅由 12.38% 降到 12.37%**，且「甲賀忍蛙ex 超級甲賀忍蛙ex」主分支 3.31→**3.36%** 反而回補 → 退坑幾乎全是版本內轉移。相對地，**胡帕 ex 是今日唯一「份額與強度雙跌」的主流線**（6.87→6.75%、53.68→53.43%），且對位根因明確（對噴火龍 Y 55.7→54.0%、對水君 58.2→57.0%）→ 這才是真退坑。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
5. **C1 新包拖累差距首次收斂**：3.06→3.23→**3.22pt**（單日 −0.01pt，11-09 以來首次逆轉），含新卡份額 51.91→**51.76%** 續降、AWR 47.03→**47.02%** 微跌。**仍遠未達成 11-05 訂的「連兩日收斂且每日 ≥0.3pt」，但方向首次逆轉，繼續觀察不變。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
6. **厚度稅連續第六天成立**：130–160HP 份額 41.80%（AWR 50.65%）＞ 170–200HP 37.12%（48.77%）＞ 210+HP 21.22%（47.57%）＞ ≤120HP 18.52%（47.06%）。240HP 超級快龍 ex 35.57%、240HP 超級班基拉斯 ex 42.38% 是極端值；150HP 自爆磁怪 54.69%、140HP 蜂女王 ex 54.26% 是技能與對位蓋過厚度的例外。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
7. **環境已連續第三日無新突襲線**：合併頁無新列突破 0.15%，分支口徑無份額 ≥0.15% 新進榜；退出前 40 的只有「超級甲賀忍蛙ex 甲賀忍蛙」（昨 0.48%）與「超級妙蛙花ex 妙蛙花」（昨 0.43%）。**擴張全由既有核心分支完成 → 沒有新軸在醞釀，環境仍在既有結構內重分配。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
8. **小樣本 AWR 暴動必須標註 N**：哈克龍 48.10→**50.12%（+2.02pt，全環境最大）**但 N 僅 392；超級盔甲鳥 ex 份額 +0.13pt 而 AWR −1.98pt、N 200。→ 這類變動只列觀察，不進預測。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### PRED_20261112 內檢（正式檢查日 2026-11-14） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（超級超夢 X ex 合併份額 ≥5.1%）：❌ **動能失效**。4.74→**4.78%**，距門檻 0.32pt；動能 +0.48→**+0.04pt 衰減 92%**；N 佔比 4.19→4.14% 微降；拆分支確認為**低品質擴張**（強線夢幻ex 3.26→3.16%，弱線蒂安希ex 0.82→0.94%／45.88%）。依 11-13 新規則直接降級為「本檢查日不可能命中」。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（超級雷電獸 ex 合併 AWR <50.0%）：⏳ **逼近中**。50.56→**50.39%**，距門檻 0.39pt；動能 −0.15→−0.17pt 穩定；預計 0.39÷0.17≈**2.3 天**，略超出檢查日。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（超能系族群合併份額 <10.2%）：❌ **動能失效**。10.51→**10.48%**，距門檻 0.28pt；動能 −0.11→**−0.03pt 衰減 73%**；預計 0.28÷0.03≈9.3 天，本檢查日不可能命中。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 內檢結果：逼近中 1、動能失效 2；正式命中率仍以 2026-11-14 檢查日為準。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

## 2026-11-13 新預測 PRED_20261113（檢查日 2026-11-15） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（0.45）自爆磁怪 合併 AWR **<54.5%**：今日 54.69%，距離 0.19pt（AWR 帶下緣，≤0.5pt 符合低增量日規則）；方向 55.54→55.02→**54.69%** 兩連跌，動能 −0.52→**−0.33pt（衰減 37%，門檻內）**；預計天數 0.19 ÷ 0.33 ≈ **0.6 天**。主分支「自爆磁怪 密勒頓ex」同步 55.30→54.94%；同時份額動能反向上升（+0.05→+0.06pt），屬靶心型初期。**風險：N=1,383 的 AWR 仍有 ±0.3pt 級噪音，門檻只差 0.19pt，可能被噪音推回。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（0.30）騎拉帝納 ex 合併份額 **<4.6%**：今日 4.84%，距離 0.24pt（份額型，低增量日友善）；四連降 5.16→4.96→**4.84%**，動能 −0.20→**−0.12pt（衰減 40%，門檻內）**；預計天數 0.24 ÷ 0.14 ≈ **1.7 天**。主分支「騎拉帝納ex 哈克龍」4.38→4.27%／49.81%。**風險：AWR 同步回升（49.22→49.41%），若份額止跌而強度續升，條件會失敗。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（0.25）胡帕 ex 合併 AWR **<53.0%**：今日 53.43%，距離 0.43pt（AWR 帶內 ≤0.5pt）；兩連跌 53.74→53.68→**53.43%**，動能 −0.06→**−0.25pt（反向放大，門檻內）**；預計天數 0.43 ÷ 0.25 ≈ **1.7 天**。主分支「胡帕ex 超級阿勃梭魯ex」53.87→53.55% 同步下滑；對位根因已定位（對噴火龍 Y 55.7→54.0%、對水君 58.2→57.0%）。**風險：胡帕反制面仍寬（壓超夢 77.6%、騎拉帝納 77.0%、雷電獸 71.4%），對手若不反擊可能止跌。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 最大機率：A。信心：中。三條皆為單條件方向型延續，距離落在對應指標帶內、**動能衰減率皆未超過 50%（A 37%、B 40%、C 反向放大）**、預計天數 ≤2 天，且（牌組, 指標）組合皆未在近兩日使用過（近兩日已用：超夢份額、雷電獸 AWR、超能系族群份額、蜂女王 AWR、忍蛙份額、水君份額）。本日為連續第四個低增量日，AWR 型條件實現率偏低，整體信心維持中。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
'''

s = P.read_text(encoding='utf-8')
if '## 2026-11-13 正式驗證 PRED_20261111' in s:
    print('already present, skip')
else:
    s = s.rstrip() + '\n' + block
    P.write_text(s, encoding='utf-8')
    print('reflections.md updated,', len(s.splitlines()), 'lines')
