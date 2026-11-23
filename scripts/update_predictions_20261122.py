#!/usr/bin/env python3
"""2026-11-22 更新 predictions.json：驗證 PRED_20261121、新增 PRED_20261122。"""
import collections
import json

P = 'memory/meta_predictions/predictions.json'
D = json.load(open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

# 1) 驗證 PRED_20261121
for p in D:
    if p['id'] == 'PRED_20261121':
        p['verification'] = collections.OrderedDict([
            ('date', '2026-11-22'),
            ('result', 'miss'),
            ('score', '0/3'),
            ('detail', [
                'A 超級甲賀忍蛙 ex 合併份額 <6.30% → 6.3960% ❌（昨 6.4154%，Δ−0.0194pt，方向正確但幅度不足，距門檻 0.0960pt）',
                'B 胡帕 ex 合併份額 ≥8.10% → 7.9245% ❌（昨 7.9094%，Δ+0.0151pt，方向正確但幅度不足 24 倍，距門檻 0.1755pt）',
                'C 月亮伊布 合併份額 <8.20% → 8.3820% ❌（昨 8.3684%，Δ+0.0136pt，方向反轉，距門檻 0.1820pt）',
            ]),
            ('cause', '失敗主因不是方向而是檢查日增量只有 +62 對局：可比牌組（N≥200）單日份額變動上限僅 +0.0350pt（自爆磁怪）／−0.0294pt（噴火龍 Y），標準差 0.0123pt，三條門檻距離為噪音帶的 3～6 倍。副牌層級驗算：環境總副牌 +54 副且 0 組減少 → A 需淨減約 9.7 副、C 需淨減約 14.6 副（兩條結構性不可能）；B 需吸收 +21.9 副（＝全環境新增的 40.6% 集中度），實際僅 +4 副（7.4%）。'),
            ('lesson', '「門檻可達性取決於檢查日預估增量」規則的第二次驗證，且這次是硬性結構不可能而非機率問題。固定 0.05pt 的噪音門檻不足，必須改用可計算的副牌濃度模型。'),
        ])
        p['reflection'] = '0/3。三條的方向判斷有兩條是對的（忍蛙續降、胡帕續升），但門檻距離全部遠大於當日噪音帶。根因是設定門檻時把「檢查日會有正常量級增量」當成前提（11-21 是 +1,753 的最大增量日，隔天就掉到 +62）。修正方向：門檻必須以副牌數為單位換算可行性，而不是以份額點數搭配經驗噪音帶。'

# 2) 新增 PRED_20261122
new = collections.OrderedDict([
    ('id', 'PRED_20261122'),
    ('date', '2026-11-22'),
    ('session', '晚間 20:05（C1 第二十五日） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
    ('set', 'C1 Day 25'),
    ('source', 'Limitless TCG 即時資料 2026-11-22 20:05（UTC+8），C1 標準賽制 92 錦標賽／10,272 玩家／31,272 對局（+2 場／+31 人／+62 對局／+0.20%，本系列最小增量日），719 分支／199 合併列（同名加總後 183 組，新增 2 個噪音名稱）；同一支 parser 重解析 11-19～11-22 raw；對位取自前 24 張牌組對位頁＋咚咚鼠愛管侍線並經 scripts/verify_mu_20261122.py 覆核 89 條全數通過（合併 74＋分支 13＋古劍豹 2）；字典補 4 條牌組名（deck_names 873→877，version 4.22） <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
    ('environment_summary', 'C1 第二十五日，單日增加 2 場錦標賽／31 玩家／62 對局（+0.20%，本系列有紀錄以來最小增量日；Sunday 20:05 快照大量當日賽事未入庫），全環境加權 AWR 48.9888%（+0.0028pt，N=61,979）。環境總副牌 12,663→12,717（+54 副），181 組中 28 組新增、153 組持平、0 組減少 → 份額下降只能靠分母稀釋，單日份額變動上限被壓到 ±0.035pt。合併份額前五：超級噴火龍 Y ex 12.9576%／50.2163%、超級七夕青鳥 ex 9.9591%／53.5383%、月亮伊布 8.3820%／48.3998%、胡帕 ex 7.9245%／53.2685%、水君 ex 7.6227%／51.5081%。AWR 前五：自爆磁怪 54.1513%、三首惡龍 53.7868%、超級七夕青鳥 ex 53.5383%、胡帕 ex 53.2685%、蜂女王 ex 52.9789%。最大結構變化：超級七夕青鳥 ex 五連升擴張正式中止（動能 +0.2858→−0.0204pt 轉負、AWR 持平、族群微跌）；自爆磁怪份額六連升但 AWR 兩連跌且電系族群同步微跌，11-14 三要素首次齊備、靶心雛形成立；胡帕 ex 份額九連升但擴張速度驟降（+0.3607→+0.0151pt）、AWR 續跌；超級路卡利歐 ex 退坑結構瓦解（份額三連升＋AWR 反彈＋族群反彈）；超級甲賀忍蛙 ex 副牌 +0 而份額仍跌 0.0194pt，為最乾淨的純稀釋觀測；超級蜥蜴王 ex 三連降且吸收濃度降至 0%，同為純份額外流。C1 新舊卡差距 3.2149→3.1952pt，連兩日擴大後首次收斂 0.0197pt。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
    ('predictions', [
        collections.OrderedDict([
            ('scenario', 'A'),
            ('name', '自爆磁怪 合併 AWR <53.60% <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
            ('probability', 0.30),
            ('description', '自爆磁怪 合併 AWR **<53.60%**（今日 54.1513%，距離 0.5513pt）。本輪唯一合規的 AWR 型條件：依 11-19 低增量日規則，AWR 型距離須 ≥0.4pt 且全輪最多一條。結構：份額 4.2395→4.3003→4.5308→**4.5658%** 六連升、N 佔比 3.9045% 同步升、AWR 54.6710→54.2317→**54.1513%** 兩連跌、電系族群 AWR 49.7916→**49.7717%** 同步微跌 → **11-14 三要素（份額升／AWR 跌／族群跌）今日首次齊備，靶心雛形成立**。預計 0.5513 ÷ 兩日平均動能 0.2599 ≈ **2.1 天**，正好對上檢查日。風險：N=2,420 的 AWR 單日標準誤約 1.0%，0.55pt 仍在噪音內；族群確認偏弱（僅 −0.0199pt）。**停止條件：若 11-23／11-24 份額動能重新放大，依 11-21 規則機率壓到 0.25。** <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
        ]),
        collections.OrderedDict([
            ('scenario', 'B'),
            ('name', '三首惡龍 合併份額 ≥2.80% <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
            ('probability', 0.33),
            ('description', '三首惡龍 合併份額 **≥2.80%**（今日 2.6967%，距離 0.1033pt）。份額 2.5856→2.6091→2.6755→**2.6967%** 四連升；AWR 53.7868%（全環境第 2）；副牌 247→253→274→**277**（+6／+21／+3，吸收濃度 2.73%／2.97%／5.56%）。可行性（副牌濃度模型，T1＝13,437）：需吸收 dD = **+26.9 副** ＝ 全環境 +720 副新增的 **3.73%**，略高於歷史中位 2.97%、遠低於歷史最高 5.56% → **可行但無安全餘裕**。AWR 同步走強 +0.0544pt，但龍／惡系族群 AWR 微跌 −0.0071pt（擴張發生在族群強度略降的背景下，品質有雜音）。風險：近門檻型依 11-13 規則要求「動能衰減 <30%」，今日衰減 68.1%（+0.0664→+0.0212pt）**在舊規則下會被降級**；本輪改以濃度模型判定為可行，機率因此壓到 0.33 而非更高。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
        ]),
        collections.OrderedDict([
            ('scenario', 'C'),
            ('name', '超級蜥蜴王 ex 合併份額 <2.55% <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
            ('probability', 0.28),
            ('description', '超級蜥蜴王 ex 合併份額 **<2.55%**（今日 2.6382%，距離 0.0882pt）。份額 2.7217→2.7122→2.6462→**2.6382%** 三連降、N 佔比 2.1911% 同步三降、AWR 49.5300% 持平（本來就低於大盤 0.46pt，無崩潰可跌）→ **純份額外流**。副牌 260→263→271→**271**（+3／+8／+0，吸收濃度 1.36%／1.13%／0%），持續低於環境增速。可行性：門檻對應 dD ≤ **+5.7 副**（吸收濃度 ≤0.79%，略低於歷史中位 1.13%）→ **可行**；若 dD=0，份額將落在 2.4967%，直接命中。對位未惡化（壓胡帕 57.2%、壓月亮伊布 63.5%；輸噴火龍 Y 40.2%、輸忍蛙 41.5%）→ 不是版本淘汰，是人氣遷移。風險：11-21 曾單日 +8 副，若 11-23／11-24 拿到 6 副以上新增即失效。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
        ]),
    ]),
    ('most_likely', 'B'),
    ('confidence', 'medium-low'),
    ('check_date', '2026-11-24'),
    ('verification', None),
    ('reflection', None),
    ('excluded_strongest_signal', '超級七夕青鳥 ex 合併份額 <9.80%（擴張中止後的回落）。今日 9.9591%，距離 0.1591pt；份額五連升後動能轉負（+0.2858→**−0.0204pt**）、AWR 完全持平、龍／惡系族群 AWR −0.0071pt。可行性極高：門檻對應 dD ≤ **+40.9 副** ＝ 全環境新增的 5.68%，而七夕青鳥歷史吸收濃度為 11.58%（11-21：+82 副／+708）／10.45%（11-20：+23／+220）／1.85%（11-22：+1／+54），中位 10.45% 遠高於所需 → **在舊規則下這會是本輪最強訊號**。但（超級七夕青鳥 ex, 份額）已於 PRED_20261120 使用、（超級七夕青鳥 ex, AWR）已於 PRED_20261118 使用，落在去重規則內故排除。代價：本輪少了一條可行性極高、方向明確的份額回落訊號。 <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'),
])

# 取代同 id（若已存在）
D = [p for p in D if p['id'] != 'PRED_20261122']
D.append(new)

json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('predictions total:', len(D), '| last:', D[-1]['id'], D[-1]['most_likely'], D[-1]['check_date'])
for p in D:
    if p['id'] == 'PRED_20261121':
        print('PRED_20261121 verification:', p['verification']['result'], p['verification']['score'])
