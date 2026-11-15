#!/usr/bin/env python3
"""2026-11-14 更新 predictions.json：PRED_20261112 正式驗證、PRED_20261113 內檢、新增 PRED_20261114。"""
import json
import shutil

P = 'memory/meta_predictions/predictions.json'
shutil.copy(P, 'memory/meta_predictions/predictions.json.bak_20261114')
d = json.load(open(P, encoding='utf-8'))
MARK = ' <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'

for e in d:
    if e['id'] == 'PRED_20261112':
        e['verification'] = {
            'date': '2026-11-14',
            'check_date': '2026-11-14',
            'interim': False,
            'source': 'Limitless TCG Live 2026-11-14 20:05 (UTC+8), C1 Standard 63 錦標賽／7,789 玩家／24,154 對局, 612 分支／185 合併；同一支 parser 重解析 11-05～11-14 raw' + MARK,
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '超級超夢 X ex 合併份額 ≥5.1%',
                    'result': 'hit',
                    'actual': '4.78→5.16%（+0.38pt）；N 佔比 4.14→4.37% 同向上升。拆分支：強線「超級超夢Xex 夢幻ex」3.16→3.02%／48.65%，弱線「超級超夢Xex 超級蒂安希ex」0.94→1.37%／46.86%；兩線 AWR 均改善，但份額仍主要由弱線貢獻。'
                },
                {
                    'scenario': 'B',
                    'predicted': '超級雷電獸 ex 合併 AWR <50.0%',
                    'result': 'miss',
                    'actual': '50.39→50.00%（735-706-28，N=1,469）；原始調整後勝率為 747/1494=50.0000%，精確等於門檻。因條件為嚴格 <50.0%，不算命中。'
                },
                {
                    'scenario': 'C',
                    'predicted': '超能系族群合併份額 <10.2%',
                    'result': 'miss',
                    'actual': '10.48→10.36%，距門檻 0.16pt；兩日僅降 0.12pt，族群份額黏性高。族群 AWR 48.21→48.12%，仍低於大盤 48.95%。'
                },
            ],
            'score': '1/3',
            'conclusion': '正式命中 1/3。A 的份額門檻命中，但「低品質擴張」標籤只描述當日份額來源，今日兩線 AWR 已同步改善；B 因精確等於嚴格門檻而失手；C 再次證實族群份額比個體份額黏。' + MARK,
        }
        e['reflection'] = (
            '1/3。新增三條規則：①門檻驗證必須使用未四捨五入比例，顯示值只供人讀；'
            '②低品質擴張不可當永久標籤，每日重測主分支與次分支 AWR；'
            '③族群份額型條件若連兩日單日降幅 <0.15pt，門檻須距當前值至少 0.4pt，否則改看族群 AWR。'
            '另修正 11-13 規則：靶心型必須同時滿足份額升、AWR 跌、族群 AWR 跌；單看份額動能只能列觀察。' + MARK
        )

for e in d:
    if e['id'] == 'PRED_20261113':
        e['interim_check'] = {
            'date': '2026-11-14',
            'check_date': '2026-11-15',
            'source': 'Limitless TCG Live 2026-11-14 20:05 (UTC+8), C1 Standard 63 錦標賽／7,789 玩家／24,154 對局' + MARK,
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '自爆磁怪合併 AWR <54.5%',
                    'result': 'failing',
                    'actual': '54.69→55.24%（+0.55pt），方向反轉；昨預測的靶心型初期未成立。自身勝率對噴火龍 Y 43.3→46.2%、對路卡利歐 40.9→42.7%、對月亮伊布 39.7→42.1% 同步改善。'
                },
                {
                    'scenario': 'B',
                    'predicted': '騎拉帝納 ex 合併份額 <4.6%',
                    'result': 'approaching',
                    'actual': '4.84→4.69%，距門檻 0.09pt；動能 -0.12→-0.15pt，方向連續、速度改善。預計 0.09÷0.15≈0.6 天，11-15 命中機率高。'
                },
                {
                    'scenario': 'C',
                    'predicted': '胡帕 ex 合併 AWR <53.0%',
                    'result': 'failing',
                    'actual': '53.43→53.49%，方向反轉；動能 -0.25→+0.06pt。對超級超夢 X ex 仍壓 73.4%，但對蜂女王線被磨。'
                },
            ],
            'score': '內檢：逼近中 1、方向反轉 2；正式命中率仍以 2026-11-15 檢查日為準',
            'conclusion': '依 11-13 規則，A 與 C 因方向反轉降級為「本檢查日不可能命中」；B 動能改善且距門檻僅 0.09pt，是唯一可達成型。' + MARK,
        }

if not any(e['id'] == 'PRED_20261114' for e in d):
    d.append({
        'id': 'PRED_20261114',
        'date': '2026-11-14',
        'session': '晚間 20:05（C1 第十七日）',
        'set': 'C1 Day 17',
        'source': (
            'Limitless TCG Live 2026-11-14 20:05 (UTC+8), C1 Standard 63 錦標賽／7,789 玩家／24,154 對局, '
            '612 分支／185 合併；同一支 parser 重解析 11-05～11-14 raw；'
            '對位取自 24 張牌組 matchups 頁並經 scripts/verify_mu_20261114.py 覆核 59 條全數通過；'
            '字典補 25 條牌組名（deck_names 766→791，version 4.14）' + MARK
        ),
        'environment_summary': (
            'C1 第十七日，單日增加 6 場錦標賽／698 玩家／2,556 對局（+11.83%），結束連續四個低增量日；'
            '環境加權 AWR 48.89→48.95%。合併份額前五：超級噴火龍 Y ex 12.45%／49.73%、'
            '月亮伊布 9.51%／48.30%、水君 ex 7.96%／51.34%、超級七夕青鳥 ex 7.69%／54.05%、'
            '超級甲賀忍蛙 ex 7.43%／43.79%。AWR 前五：自爆磁怪 55.24%、三首惡龍 54.15%、'
            '蜂女王 ex 54.08%、超級七夕青鳥 ex 54.05%、胡帕 ex 53.49%。'
            '最大結構變化：自爆磁怪 AWR +0.55pt／份額 +0.19pt 反彈；'
            '超級路卡利歐 ex 份額 +0.50pt／AWR -0.55pt，噴火龍 Y 55.9%（N=179）確認靶心根因；'
            '超級七夕青鳥 ex 連兩日份額與 AWR 雙升；超級超夢 X ex 份額命中 5.1% 但仍由弱線擴張；'
            '忍蛙系份額九連降、家族合計降至 12.16%。C1 新舊卡差距 3.22→3.10pt，出現首個可靠轉正訊號。' + MARK
        ),
        'predictions': [
            {
                'scenario': 'A',
                'name': '自爆磁怪合併份額 ≥4.0%',
                'probability': 0.40,
                'description': (
                    '自爆磁怪合併份額 **≥4.0%**（今日 3.84%，距離 0.16pt）。方向 3.59→3.65→**3.84%**，'
                    '動能 +0.06→**+0.19pt** 加速；N 佔比 3.23→3.36% 同向上升，AWR 54.69→**55.24%** 同步走強。'
                    '預計天數 0.16÷0.19≈0.8 天。這是「高強度擴張」而非弱線獨撐；'
                    '風險是擴張型門檻歷史命中率偏低，且主分支已到 3.75%，若對位回彈可能停住。' + MARK
                ),
            },
            {
                'scenario': 'B',
                'name': '超級七夕青鳥 ex 合併份額 ≥8.0%',
                'probability': 0.30,
                'description': (
                    '超級七夕青鳥 ex 合併份額 **≥8.0%**（今日 7.69%，距離 0.31pt）。方向 7.05→7.25→**7.69%**，'
                    '動能 +0.20→**+0.44pt** 加速；N 佔比 6.75→6.99% 同向上升，兩大分支份額皆增。'
                    '預計天數 0.31÷0.44≈0.7 天。機率壓到 0.30：擴張型門檻歷史命中率偏低，'
                    '且太陽伊布線 AWR 54.99→54.74% 與合併方向不完全一致。' + MARK
                ),
            },
            {
                'scenario': 'C',
                'name': '超級蜥蜴王 ex 合併份額 <2.80%',
                'probability': 0.30,
                'description': (
                    '超級蜥蜴王 ex 合併份額 **<2.80%**（今日 2.91%，距離 0.11pt）。方向 3.05→3.02→**2.91%** 三連降，'
                    '動能 -0.03→**-0.10pt** 加速；AWR 50.62→50.58% 持平，屬純份額外流。預計天數 0.11÷0.10≈1.1 天。'
                    '對位壓力來自電系：超級雷電獸 ex 對蜥蜴王 75.0%（N=32），另有噴火龍 Y ex 56.4%（N=110）。'
                    '近門檻條件已滿足：同一指標連三日同向、動能未衰減反而放大。' + MARK
                ),
            },
        ],
        'most_likely': 'A',
        'confidence': 'medium',
        'check_date': '2026-11-16',
        'verification': None,
        'reflection': None,
    })

json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('predictions.json 更新完成，共', len(d), '筆')
for e in d[-3:]:
    print(' ', e['id'], '| check_date', e.get('check_date'), '| verification', bool(e.get('verification')), '| interim', bool(e.get('interim_check')))
