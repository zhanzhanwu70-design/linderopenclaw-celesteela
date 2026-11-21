#!/usr/bin/env python3
"""2026-11-20 更新 predictions.json：
1) PRED_20261118 正式驗證（檢查日 2026-11-20）→ 2/3
2) PRED_20261119 提前內檢（正式檢查日 2026-11-21）
3) 新增 PRED_20261120（檢查日 2026-11-22）
"""
import collections
import json

P = 'memory/meta_predictions/predictions.json'
D = json.load(open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
byid = {p['id']: p for p in D}
PROJ = ' <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'

# ---------- 1) PRED_20261118 正式驗證 ----------
p = byid['PRED_20261118']
p['verification'] = collections.OrderedDict([
    ('date', '2026-11-20'),
    ('check_date', '2026-11-20'),
    ('interim', False),
    ('source', 'Limitless TCG 即時資料 2026-11-20 20:05（UTC+8），C1 標準賽制 86 錦標賽／9,697 玩家／29,457 對局，694 分支／197 合併列（同名加總後 181 組）；同一支 parser 重解析 11-17～11-20 raw' + PROJ),
    ('results', [
        collections.OrderedDict([
            ('scenario', 'A'),
            ('predicted', '超級七夕青鳥 ex 合併 AWR <53.0%' + PROJ),
            ('result', 'miss'),
            ('actual', '53.2538→**53.3902%**（raw 2681/5019），距門檻 0.3902pt；AWR 今日反彈 +0.1363pt，方向與預測相反。份額 9.5991→9.6937%、N 佔比 8.5401→8.5965% 續升，龍／惡系族群 AWR 50.9178→50.9267% 亦升 → 靶心訊號被打斷，僅列真擴張。' + PROJ),
        ]),
        collections.OrderedDict([
            ('scenario', 'B'),
            ('predicted', '月亮伊布合併份額 <8.60%' + PROJ),
            ('result', 'hit'),
            ('actual', '8.6151→**8.5696%**（raw 8.5696 < 8.60）；N 佔比 7.1679→7.1150% 連降，AWR 48.4484→48.4087% 微跌，屬純份額外流。' + PROJ),
        ]),
        collections.OrderedDict([
            ('scenario', 'C'),
            ('predicted', '超級蜥蜴王 ex 合併 AWR <49.60%' + PROJ),
            ('result', 'hit'),
            ('actual', '49.7390→**49.4440%**（raw 655/1324）；動能 −0.1858→−0.2950pt 再度放大，格鬥／草／鋼系族群 AWR 48.0489→47.9601% 同步下跌，族群確認成立。' + PROJ),
        ]),
    ]),
    ('score', '2/3'),
    ('conclusion', '正式命中 2/3。B 的純份額外流與 C 的「強度退潮＋族群同步下跌」命中；A 的 AWR 型條件在低訊號日反彈後無法挽回。' + PROJ),
])
p['reflection'] = ('2/3。新增兩條教訓：①AWR 型條件若族群方向未同步下跌，單靠自身 AWR 續跌不足以成立——A 今日份額、N 佔比、AWR、族群四項全部與「退潮」相反，'
                    '應在 11-18 設定當天就因「族群 AWR 回升」而壓低機率。②「份額升＋AWR 跌」的靶心雛形要同時追蹤族群 AWR 才算完整；'
                    '今日胡帕 ex 已是此結構（份額六連升、AWR 轉跌），但族群未跌，只能寫成觀察級。' + PROJ)

# ---------- 2) PRED_20261119 提前內檢 ----------
p = byid['PRED_20261119']
p['interim_check'] = collections.OrderedDict([
    ('date', '2026-11-20'),
    ('check_date', '2026-11-21'),
    ('source', 'Limitless TCG 即時資料 2026-11-20 20:05（UTC+8），C1 標準賽制 86 錦標賽／9,697 玩家／29,457 對局（+378 對局／+1.30%，近兩週最小增量日）' + PROJ),
    ('results', [
        collections.OrderedDict([
            ('scenario', 'A'),
            ('predicted', '超級路卡利歐 ex 合併 AWR <50.00%' + PROJ),
            ('result', 'invalid_momentum_decayed'),
            ('actual', '50.1913→**50.1893%**（raw 1314/2617），動能 −0.3169→**−0.0020pt，衰減 99.4%**，距門檻 0.1893pt → 依 11-13 規則降級為「本檢查日不可能命中」。同時份額 5.6527→5.6719% 反彈 +0.0192pt、N 佔比 4.4912→4.4824% 微降，昨判的「真退坑」結構瓦解。' + PROJ),
        ]),
        collections.OrderedDict([
            ('scenario', 'B'),
            ('predicted', '超級雷電獸 ex 合併份額 <3.40%' + PROJ),
            ('result', 'invalid_direction_reversed'),
            ('actual', '3.4439→**3.4444%**，+0.0005pt 轉正，四連降中止，距門檻由 0.0439pt 擴到 0.0444pt。N 佔比 2.8085→2.7919% 續降、AWR 50.5474→50.4532% 微跌，電系族群 AWR 49.6985→49.7248% 反而上升。' + PROJ),
        ]),
        collections.OrderedDict([
            ('scenario', 'C'),
            ('predicted', '騎拉帝納 ex 合併份額 <4.20%' + PROJ),
            ('result', 'approaching_momentum_exhausted'),
            ('actual', '4.2814→**4.2694%**，距門檻 0.0694pt；動能 −0.0660→**−0.0120pt（衰減 81.8%）**，N 佔比 3.6065→3.5866% 續降，接近但動力耗盡。' + PROJ),
        ]),
    ]),
    ('score', '內檢：動能失效 1、方向反轉 1、逼近但動力耗盡 1；正式命中率仍以 2026-11-21 為準' + PROJ),
    ('conclusion', '本輪三條全部無法在檢查日成立：最大機率 B 首日即反轉，A 的動能衰減 99.4%，C 動能衰減 81.8%。' + PROJ),
])

# ---------- 3) 新增 PRED_20261120 ----------
new = collections.OrderedDict([
    ('id', 'PRED_20261120'),
    ('date', '2026-11-20'),
    ('session', '晚間 20:05（C1 第二十三日）' + PROJ),
    ('set', 'C1 Day 23'),
    ('source', 'Limitless TCG 即時資料 2026-11-20 20:05（UTC+8），C1 標準賽制 86 錦標賽／9,697 玩家／29,457 對局（+2 場／+144 人／+378 對局／+1.30%，近兩週最小增量日），694 分支／197 合併列（同名加總後 181 組）；同一支 parser 重解析 11-17～11-20 raw；對位取自前 32 張牌組對位頁並經 scripts/verify_mu_20261120.py 覆核 137 條全數通過（合併 67＋分支 70）；字典補 6 條牌組名（deck_names 851→857，version 4.20）' + PROJ),
    ('environment_summary', 'C1 第二十三日，單日增加 2 場錦標賽／144 玩家／378 對局（+1.30%，近兩週最小增量日），全環境加權 AWR 48.9719%（+0.0080pt）。合併份額前五：超級噴火龍 Y ex 12.8390%／50.1567%、超級七夕青鳥 ex 9.6937%／53.3902%、月亮伊布 8.5696%／48.4087%、水君 ex 7.7344%／51.4883%、胡帕 ex 7.5487%／53.2795%。AWR 前五：自爆磁怪 54.6710%、三首惡龍 53.8287%、蜂女王 ex 53.5686%、超級七夕青鳥 ex 53.3902%、胡帕 ex 53.2795%。最大結構變化：自爆磁怪份額、N 佔比、AWR、電系族群四項同升，為今日最乾淨的擴張線；超級七夕青鳥 ex 份額四連升但 AWR 反彈 +0.1363pt、族群同步回升，靶心訊號被打斷；胡帕 ex 份額六連升而 AWR 轉跌，出現靶心初期雛形但族群未確認；超級路卡利歐 ex 退坑動能衰減 99.4% 熄火；超級蜥蜴王 ex AWR 四連跌且族群五跌。C1 新舊卡差距 3.0127→3.0599pt 反向擴大，連兩日收斂趨勢中止。' + PROJ),
    ('predictions', [
        collections.OrderedDict([
            ('scenario', 'A'),
            ('name', '超級七夕青鳥 ex 合併份額 ≥9.85%' + PROJ),
            ('probability', 0.4),
            ('description', '超級七夕青鳥 ex 合併份額 **≥9.85%**（今日 9.6937%，距離 0.1563pt）。方向 8.8837→9.1300→9.4211→9.5991→**9.6937%**，連四升；動能 +0.2911→+0.1780→**+0.0946pt**（衰減 46.8%，接近但仍在 50% 門檻內）；N 佔比 8.5401→**8.5965%** 同向上升，AWR 53.2538→**53.3902%** 同步走強 → 擴張三要素（動能未衰減、N 佔比同升、AWR 走強）齊備。門檻＝當前值＋1.65 個單日動能（落在 1.5～2.5 倍區間），預計 0.1563÷0.0946≈**1.65 天**（以最近兩日最小動能計）。風險：動能已連兩日衰減，噴火龍 Y 在 12.85～12.90 觸頂停住的前例可能重演；**停止條件：單日動能轉負即失效**。' + PROJ),
        ]),
        collections.OrderedDict([
            ('scenario', 'B'),
            ('name', '自爆磁怪 合併份額 ≥4.42%' + PROJ),
            ('probability', 0.35),
            ('description', '自爆磁怪 合併份額 **≥4.42%**（今日 4.3003%，距離 0.1197pt）。方向 4.1739→4.2395→**4.3003%**，連三升；動能 +0.0280→+0.0656→**+0.0608pt**（衰減 7.3%，遠低於 30% 門檻）；N 佔比 3.5464→3.6464→**3.6791%** 同向上升，AWR 54.5364→54.5839→**54.6710%** 同步走強且為全環境冠軍，電系族群 AWR 49.5847→49.6985→**49.7248%** 亦升 → 擴張三要素＋族群確認，結構品質高於 A。門檻＝當前值＋1.97 個單日動能（落在 1.5～2.5 倍區間），預計 0.1197÷0.0608≈**1.97 天**。風險：未加滿 11-18 規則要求的 0.15pt 安全餘裕（等效僅約 0.06pt），機率因此壓到 0.35；電系族群內搬份額效應一旦停止即失效。' + PROJ),
        ]),
        collections.OrderedDict([
            ('scenario', 'C'),
            ('name', '胡帕 ex 合併 AWR <53.00%' + PROJ),
            ('probability', 0.3),
            ('description', '胡帕 ex 合併 AWR **<53.00%**（今日 53.2795%，距離 0.2795pt）。方向 53.6361→53.3406→53.3951→**53.2795%**，今日動能 −0.1155pt 續跌；以最近兩日最小動能估算 0.2795÷0.1155≈**2.4 天**。同時份額 7.3395→7.4741→**7.5487%**（六連升）、N 佔比 6.5468→6.7012→**6.7467%** 同升 → 「份額升＋AWR 跌」的靶心初期三要素中的兩項成立。風險：龍／惡系族群 AWR 50.9178→**50.9267%** 今日微升、方向與預期不一致 → 依 11-19 規則機率上限壓到 0.30 且不得列為最大機率；低增量日（+378）AWR 噪音 ±0.25pt 會吃掉 0.28pt 的差距。' + PROJ),
        ]),
    ]),
    ('most_likely', 'A'),
    ('confidence', 'medium'),
    ('check_date', '2026-11-22'),
    ('verification', None),
    ('reflection', None),
])
D.append(new)

json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('predictions:', len(D))
print('last id:', D[-1]['id'])
print('PRED_20261118 score:', byid['PRED_20261118']['verification']['score'])
print('PRED_20261119 interim:', byid['PRED_20261119']['interim_check']['score'])
