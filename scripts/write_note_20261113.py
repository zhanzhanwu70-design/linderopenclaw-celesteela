from pathlib import Path

ROOT = Path('/home/amr/.openclaw/workspace-celesteela')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'


def marked(text):
    lines = []
    for line in text.strip('\n').splitlines():
        lines.append((line + ' ' + MARK) if line.strip() else '')
    return '\n'.join(lines).rstrip() + '\n'


note = r'''
---

# 2026-11-13 PTCGP Meta 每日摘要（晚間 20:05，C1 第十六日） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 資料狀態 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- C1 Standard：57 錦標賽／7,091 玩家／21,598 對局，較 11-12 增加 4 場／380 人／**980 對局（+4.75%）**；分支 583 條、合併 182 條（昨 568／181）；全環境加權 AWR 48.89%（持平）。Standard 與 set=C1 頁逐 slug 一致；B4a 頁仍凍結於 210／15,008／38,924（連續十七天）。**連續第四個低增量日**（<1,000 對局）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 合併份額前五 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 超級噴火龍 Y ex 11.92%／49.72%／845 副／2147-2058-112 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 月亮伊布 9.59%／48.37%／680 副／1655-1699-67 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 水君 ex 7.91%／51.73%／561 副／1495-1321-72 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 超級甲賀忍蛙 ex 7.63%／43.52%／541 副／1089-1358-58 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 超級七夕青鳥 ex 7.25%／53.93%／514 副／1561-1232-99 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 調整後勝率前五（合併口徑，N≥100） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 自爆磁怪 54.69%／3.65%／259 副／758-594-31（主分支「自爆磁怪 密勒頓ex」54.94%／3.55%） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 蜂女王 ex 54.26%／4.91%／348 副／1025-833-28（主分支「蜂女王ex 壺壺ex」54.46%／4.85%） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 三首惡龍 54.14%／2.48%／176 副／505-410-15（主分支「三首惡龍 超級阿勃梭魯ex」54.24%／1.99%） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 超級七夕青鳥 ex 53.93%／7.25%／514 副／1561-1232-99（主分支「超級七夕青鳥ex 太陽伊布」54.99%／3.67%） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 胡帕 ex 53.43%／6.75%／479 副／1413-1159-70（主分支「胡帕ex 超級阿勃梭魯ex」53.55%／5.54%） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

*第六名水君 ex 51.73%（7.91%，N=2,888）、第七名超級阿勃梭魯 ex 51.60%、第八名超級路卡利歐 ex 51.54%、第九名咚咚鼠 ex 50.88%、第十名密勒頓 ex 50.77%。* <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 三日變化（11-11 → 11-12 → 11-13） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級七夕青鳥 ex 是今日唯一「份額與強度同步回升」的主流線**：份額 7.19→7.05→**7.25%**（三連降後反彈），AWR 53.51→53.83→**53.93%**（四連升）。反彈由「超級七夕青鳥ex 甲賀忍蛙」分支帶動（2.88→**3.14%**／**53.97%**），太陽伊布分支反而微降（3.74→3.67%／54.99%）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級噴火龍 Y ex 份額與強度同升、創全環境最大單日份額增幅**：份額 11.40→11.52→**11.92%（+0.40pt）**，AWR 49.22→49.50→**49.72%**；N 佔比 9.02→9.31→**10.08%** 同向上升 → 判定真實擴張。但仍低於大盤 0.83pt——份額王不是強度王。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **自爆磁怪 AWR 五連冠但兩連跌，冠軍差距收斂到 0.43pt**：AWR 55.54→55.02→**54.69%**；份額 3.54→3.59→**3.65%**（動能 +0.05→**+0.06pt** 首次重新加速）。下跌非對位崩壞——對噴火龍 Y +0.8pt、對路卡利歐 +1.1pt、對蜥蜴王 +1.4pt 都改善，唯一大跌是對騎拉帝納 ex（60.5→**57.5%**）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **胡帕 ex 是今日唯一「份額與強度雙跌」的主流線**：份額 6.92→6.87→**6.75%**，AWR 53.74→53.68→**53.43%**，退守第五。對位根因：對噴火龍 Y ex 55.7→**54.0%**、對水君 ex 58.2→**57.0%** 兩線同時退潮。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級超夢 X ex 的擴張是「弱分支擴張」**：合併份額 4.26→4.74→**4.78%**（動能 +0.48→**+0.04pt** 幾近歸零），AWR 48.31→47.38→**47.33%**。拆分支：強線「超級超夢Xex 夢幻ex」3.26→**3.16%**／48.45% 縮水，弱線「超級超夢Xex 超級蒂安希ex」0.82→**0.94%**／45.88% 獨撐份額；N 佔比 4.19→**4.14%** 微降。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **忍蛙系真退坑第八日，但家族合計幾乎不動**：超級甲賀忍蛙 ex 份額 7.94→7.73→**7.63%**（八連降）、AWR 43.47→43.49→**43.52%**；純忍蛙線「甲賀忍蛙 ex」3.96→**3.98%**、「甲賀忍蛙」0.69→**0.76%**。**家族合計 12.65→12.38→12.37%**，退坑幾乎全部只是版本內轉移（主分支「超級甲賀忍蛙ex 甲賀忍蛙ex」4.83→**4.82%**、「甲賀忍蛙ex 超級甲賀忍蛙ex」3.31→**3.36%** 反而回補）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級路卡利歐 ex 靶心效應第五日**：份額 5.41→5.27→**5.26%**，AWR 51.71→51.62→**51.54%** 續跌；族群（格鬥／草／鋼系 AWR 49.38→**49.12%**）同向下行，確認非族群拖累。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級雷電獸 ex 份額與強度背離首度翻正**：份額 3.86→**3.91%**（終止四連降）、AWR 50.56→**50.39%**（續跌）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **蜂女王 ex 退潮止步**：份額 4.92→**4.91%**、AWR 54.26→**54.26%** 持平；族群（龍／惡系 50.57→**50.67%**）同向上升。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **騎拉帝納 ex 份額四連降**：5.16→4.96→**4.84%**，AWR 49.33→49.22→**49.41%** 回升。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **哈克龍是今日 AWR 升幅第一**（48.10→**50.12%，+2.02pt**），但 N 僅 392，屬小樣本噪音級別，僅列觀察。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級盔甲鳥 ex 是新冒出的人氣陷阱**：份額 0.46→**0.59%**、AWR 45.98→**44.00%（−1.98pt）**，份額與強度反向。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **沒有新突襲線**：合併頁無新列突破 0.15%，分支口徑亦無份額 ≥0.15% 新進榜；退出前 40 的只有「超級甲賀忍蛙ex 甲賀忍蛙」（昨 0.48%）與「超級妙蛙花ex 妙蛙花」（昨 0.43%）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 對位變化（|Δ|≥1.5pt） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **55 條主要對線中只有 5 條移動超過 1.5pt**（可比 54 條）：自爆磁怪 vs 騎拉帝納 ex 60.5→57.5%（−3.0pt，N 38→40）、超級七夕青鳥 ex vs 月亮伊布 70.3→68.4%（−1.9pt，N 74→76）、胡帕 ex vs 超級噴火龍 Y ex 55.7→54.0%（−1.7pt，N 192→200）、超級蜥蜴王 ex vs 騎拉帝納 ex 60.5→59.0%（−1.5pt）、超級蜥蜴王 ex vs 蜂女王 ex 55.6→54.1%（−1.5pt）。大樣本對線（N≥150）只有胡帕 vs 噴火龍 Y 一條移動。**對位網在第四個低增量日仍然凍結。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 另：全表最大單日變化為三首惡龍 vs 超級雷電獸 ex 55.6→**61.9%（+6.3pt，N 18→21）**，兩列合計 106.3%，屬對局樣本替換造成的跳動，僅列觀察。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 新卡／規則影響 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 含 C1 新卡 **51.76%／47.02%**（N=17,986），不含新卡 **68.68%／50.24%**（N=24,862），AWR 差距 3.06→3.23→**3.22pt（單日 −0.01pt，為 11-09 以來首次收斂）**；含新卡份額 51.91→**51.76%** 續降、AWR 47.03→**47.02%** 微跌，擴充包仍未轉正。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 3 點 KO 下 HP 分桶：130–160HP **50.65%**（份額 41.80%）＞ 170–200HP 48.77%（37.12%）＞ 210+HP 47.57%（21.22%）＞ ≤120HP 47.06%（18.52%）。六天口徑一致，厚度稅持續把份額推向薄血節奏牌組；240HP 超級快龍 ex 35.57%、240HP 超級班基拉斯 ex 42.38% 是極端值。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 陷阱牌組 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級甲賀忍蛙 ex**：份額第四 7.63%，AWR 43.52%，低於大盤 **5.37pt**；輸水君 ex **68.2%**（N=88，自身 31.8%）、輸自爆磁怪 **75.6%**（N=39→41，自身 24.4%）、輸蜂女王 ex **73.9%**（N=46，自身 26.1%）。人氣與效率錯配最大標本，八連降未止。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級超夢 X ex 4.78%／47.33%**（低品質擴張）、**甲賀忍蛙 ex 3.98%／48.21%**、**皮卡丘 ex 2.69%／43.96%**、**阿羅拉 椰蛋樹 ex 1.54%／45.98%**、**長耳兔 1.21%／46.67%**、**超級盔甲鳥 ex 0.59%／44.00%**。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **超級班基拉斯 ex 1.73%／42.38%**、**超級快龍 ex 1.13%／35.57%（全環境最差）**、**大比鳥 0.99%／39.77%**、**雷公 ex 0.76%／42.80%**、**超級沙奈朵 ex 0.47%／42.86%**、**帕底亞 土王 0.87%／43.05%**。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- **火箭隊系 0.62%／40.57%**（AWR 三連升但份額仍近零）；**飛行系族群 1.38%／38.97%** 仍為最差族群。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 預測驗證 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- PRED_20261111（正式檢查日 2026-11-13）→ **0/3**：A 蜂女王 ex AWR 54.26%（<54.0% ❌，動能歸零）、B 忍蛙份額 7.63%（<7.5% ❌，動能腰斬 −0.21→−0.10pt）、C 水君 ex 份額 7.91%（<7.5% ❌，方向反轉 −0.07→+0.03pt）。三條同時失敗，失敗模式一致：**門檻設定時的動能是單日快照，兩天後動能已反轉或歸零**。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- PRED_20261112 內檢（正式檢查日 2026-11-14，尚未到期）：A 超夢份額 4.78%（≥5.1% ❌，動能 +0.48→+0.04pt 崩潰、擴張全由弱分支貢獻、N 佔比微降）、B 雷電獸 AWR 50.39%（<50.0% ❌，距 0.39pt，預計 2.3 天）、C 超能系族群份額 10.48%（<10.2% ❌，動能 −0.11→−0.03pt 停滯，預計 9.3 天）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 反省（新增三條規則）：①**內檢時每條條件必須寫出「當日動能值」與「動能衰減率」，衰減 >50% 或方向反轉者直接降級為「本檢查日不可能命中」，不再標記「逼近中」**（11-12 內檢只比距離、放過動能資訊）；②**份額擴張型條件在設定與驗證時都要列出主分支 vs 次分支的份額與 AWR 對照，擴張只發生在 AWR 低於合併值的分支即判定「低品質擴張」**；③**門檻距離須設在「動能衰減後預估天數 ≤1.5 天」，否則寧可放寬距離也不要設在 0.1～0.3pt 一步之遙的位置**。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

### 新預測 PRED_20261113（檢查日 2026-11-15） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- A（0.45）自爆磁怪 合併 AWR **<54.5%**（今日 54.69%，距離 0.19pt，AWR 帶下緣；動能 −0.52→−0.33pt 衰減 37% 仍在門檻內；預計 0.19÷0.33≈0.6 天；主分支同步 55.30→54.94%，且份額動能反向上升 +0.05→+0.06pt，屬靶心型初期）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- B（0.30）騎拉帝納 ex 合併份額 **<4.6%**（今日 4.84%，距離 0.24pt，份額型；四連降 5.16→4.96→4.84%，動能 −0.20→−0.12pt 衰減 40% 仍在門檻內；預計 0.24÷0.14≈1.7 天）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- C（0.25）胡帕 ex 合併 AWR **<53.0%**（今日 53.43%，距離 0.43pt，AWR 帶內 ≤0.5pt；兩連跌 53.74→53.68→53.43%，動能 −0.06→−0.25pt 反向放大；對位根因已定位；預計 0.43÷0.25≈1.7 天）。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
- 最大機率：A。信心：中。三條皆為單條件方向型延續，距離落在對應指標帶內、動能衰減率未超過 50%、預計天數 ≤2 天，且（牌組, 指標）組合皆未在近兩日使用過（近兩日已用：超夢份額、雷電獸 AWR、超能系族群份額、蜂女王 AWR、忍蛙份額、水君份額）。本日為連續第四個低增量日，AWR 型條件實現率偏低，信心維持中。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->

完整報告：`memory/ptcgp_meta_discord_20261113.md`。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->
'''

p = ROOT / 'memory/2026-11-13.md'
existing = p.read_text(encoding='utf-8')
if not existing.endswith('\n'):
    existing += '\n'
# 補上既有 heartbeat 段落的專案標記（只加標記，不改內容）
lines = []
for line in existing.splitlines():
    if line.strip() and MARK not in line:
        lines.append(line + ' ' + MARK)
    else:
        lines.append(line)
existing = '\n'.join(lines) + '\n'
p.write_text(existing + note.lstrip('\n'), encoding='utf-8')
print('wrote', p, len(p.read_text(encoding='utf-8').splitlines()), 'lines')
