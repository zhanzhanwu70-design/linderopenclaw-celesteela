from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/reflections.md')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'

block = r'''
## 2026-11-10 正式驗證 PRED_20261108（檢查日 2026-11-10） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **環境狀態**：C1 Standard 47 錦標賽／5,982 玩家／18,550 對局（昨 43／5,559／17,380，**+4 錦標賽／+423 玩家／+1,170 對局**）；分支 **529 條**／合併 **172 條**（昨 506／168），全環境加權 AWR **48.93%**（昨 48.96%）。**單日僅 +1,170 對局（+6.7%），屬低增量日**；B4a 頁面仍**凍結**於 210／15,008／38,924（自 10-28 起連續十四天）。Standard 與 set=C1 頁逐 slug 一致。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（自爆磁怪合併 AWR ≥56.5%）：❌ **未命中**。同名合併 55.28→**54.97%**（主分支 55.03%），單日 −0.31pt，距門檻 1.53pt。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（水君 ex 合併 AWR <50.5%）：❌ **未命中**。51.31→**51.47%**，反向 +0.16pt，距門檻 0.97pt。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（超級七夕青鳥 ex 合併份額 ≥7.0%）：✅ **命中**。7.27→**7.29%** 守住 7% 以上；但 AWR 53.72→**53.30%**，仍屬靶心磨損。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **結果：1/3。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 核心反省 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
1. **低增量日不要設遠距離 AWR 型條件**：今日全環境 AWR 48.96→48.93%（−0.03pt）幾乎凍結，個體 AWR 只在 ±0.3pt 內移動；PRED_20261108 的 A、B 距離門檻分別是 1.22pt 與 0.81pt，本來就走不到。→ **新規則：單日對局增量 <1,500（低增量日）時，AWR 型條件距離超過 0.5pt 即判定「本檢查日不可能命中」，不再列入「逼近中」；當日應改用份額型條件，或把門檻設在 0.3pt 以內。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
2. **「份額與 AWR 雙升」是曝光的代價，不是趨勢**：超級路卡利歐 ex 11-09 +1.86／+3.08 → 11-10 **+0.57／−0.96**；超級噴火龍 Y ex 11-09 +0.80／+0.71 → 11-10 +0.17／**−0.11**。兩個樣本都在雙升隔天回吐 AWR。→ **新規則：雙升支線一律標記「T+1 觀察」，不可把單日雙升延伸成趨勢型預測條件；目前僅 2 例，暫列「待驗證」。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
3. **「份額門檻守住」與「突破」要分開記帳**：七夕青鳥 7.27→7.29% 只是守住 7.0%，報告與 predictions 都應寫「守住」而非「突破」，否則命中率統計會灌水。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 流程教訓 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **對位「壓／輸」的數字來源必須寫清楚**：Limitless matchups 頁每一列的數值是「被檢視的那副牌」自己對該對手的勝率。因此「A 壓 B p%」取自 A 自己那一列，「A 輸 B p%」取自 B 那一列（＝A 輸的比率），同一對會出現兩個不同數字（自爆磁怪對路卡利歐：自己列 35.8%、對手列 60.4%）。覆核今日報告時抓到昨日「蜂女王 ex 輸自爆磁怪 8.3%」把自己的勝率誤標成敗率（正確為輸 91.7%），而「路卡利歐 輸自爆磁怪 33.3%」方向正確但來源是對手列。→ **新規則：每個對位數字都必須由 `scripts/verify_mu_YYYYMMDD.py` 依「壓＝自己列、輸＝對手列」自動覆核通過才可輸出，且數字旁一律註明自身勝率。今日 54 條敘述全數通過。**<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- `scripts/parse_20261110.py` 以同一支 parser 重解析 11-05～11-10 raw，跨日口徑一致；`scripts/verify_mu_20261110.py` 為本次新增的對位自動覆核腳本，應每日沿用。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 今日新發現 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
1. **三首惡龍是新的低曝光高效率樞紐**：AWR 53.46→53.57→54.81→**55.24%** 登頂，份額卻是 2.69→2.59→2.55→**2.52%** 連三降；壓騎拉帝納 ex 74.1%（N=27）、蜂女王 ex 64.7%（N=34）、超級噴火龍 Y ex 58.9%（N=56），輸胡帕 ex 65.2%（N=46）、水君 ex 53.3%（N=45）。正是 11-07 訂的「先找 AWR 榜上位但份額還低的牌組」規則的新樣本。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
2. **超級路卡利歐 ex 一天之內由真轉強翻成靶心**：份額 2.85→4.71→**5.28%（+2.43pt）**，AWR 50.13→53.21→**52.25%（−0.96pt）**；格鬥／草／鋼系族群 AWR 49.94→49.62% 同向下行。它壓蜂女王 70.6%、自爆磁怪 60.4%、水君 59.6%、胡帕 56.1%，但輸超級七夕青鳥 59.3%、超級噴火龍 Y ex 50.5%，份額越跑越快、強度越掉越快。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
3. **兩種「人氣王退坑」要分開**：忍蛙系份額五連降 9.77→**8.38%** 且 AWR 44.79→**43.57%** 同步下滑（真退坑，低於大盤 5.36pt，全線被壓）；月亮伊布份額五連降 11.25→**9.88%** 但 AWR 48.63% 持平（純份額外流，強度未崩）。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
4. **C1 新包拖累差距連兩日停滯**：2.68→2.73→2.96→**2.95pt**，含新卡份額 54.09→**53.44%** 反而回落、AWR 47.28→47.25% 幾乎不動，擴充包仍未轉正。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
5. **超級蜥蜴王 ex 是穩健上升線**：份額 1.91→2.62→2.68→2.99→**3.16%**（五連升），AWR 守住 51.08%；壓月亮伊布 72.2%（N=36）、胡帕 ex 65.5%（N=29）、騎拉帝納 ex 62.9%（N=35），輸雷電獸 73.3%（N=30）、水君 59.0%（N=78）。草系壓兩支黑暗系有效，是對位驅動而非人氣驅動。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
6. **環境已無新突襲線**：合併頁無任何新列突破 0.3%，分支口徑也無份額 ≥0.15% 的新進榜，擴張全由既有核心分支完成。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### PRED_20261109 內檢（正式檢查日 2026-11-11） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（超級路卡利歐 ex 合併 AWR ≥52.0%）：⚠️ **仍成立但只剩 0.25pt 緩衝**。53.21→**52.25%**，單日 −0.96pt，動能已翻負。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（自爆磁怪合併份額 ≥3.8%）：⏳ **逼近中**。3.02→**3.33%**，距門檻 0.47pt；動能 +0.97→+0.31pt，標記「動能衰退觀察」。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（C1 新舊卡 AWR 差距 ≥3.5pt）：⏳ **逼近中但停滯**。2.96→**2.95pt**。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 內檢結果：仍成立 1、逼近中 2；正式命中率仍以 2026-11-11 檢查日為準。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

## 2026-11-10 新預測 PRED_20261110（檢查日 2026-11-12） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境A（0.35）超級路卡利歐 ex 合併 AWR **<52.0%**：今日 52.25%，距離 0.25pt（AWR 帶 0.1～0.5pt 內）；方向 50.13→53.21→**52.25%**，單日動能 **−0.96pt** 為全環境最強負動能；族群（格鬥／草／鋼系 AWR 49.94→49.62%）同向下行 → AWR 型條件不降級。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境B（0.30）自爆磁怪合併份額 **≥3.8%**：今日 3.33%，距離 0.47pt（份額帶 0.3～0.8pt 內）；方向 2.05→3.02→**3.33%** 連兩日上升，但動能 +0.97→+0.31pt 衰減，**標記「動能衰退觀察」**；AWR 同步守住 54.97%。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 情境C（0.25）超級甲賀忍蛙 ex 合併份額 **<8.0%**：今日 8.38%，距離 0.38pt（份額帶 0.3～0.8pt 內）；方向 9.77→9.30→8.97→8.72→**8.38%** 五連降，動能 −0.35pt 穩定，AWR 同步下滑 → 真退坑延續型。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 最大機率：A。信心：中。三條皆單條件方向型且距離落在指標帶內；A 動能最強但屬反轉型（與 PRED_20261109 的 A 互為鏡像），B 動能衰減、C 為既有趨勢延伸。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
'''

t = P.read_text(encoding='utf-8')
if 'PRED_20261110' in t:
    print('already present, skip')
else:
    if not t.endswith('\n'):
        t += '\n'
    P.write_text(t + block.strip('\n') + '\n', encoding='utf-8')
    print('reflections appended')
