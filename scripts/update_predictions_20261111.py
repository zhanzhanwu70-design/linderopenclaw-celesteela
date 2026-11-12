#!/usr/bin/env python3
"""2026-11-11 更新 predictions.json：補 PRED_20261109 驗證、PRED_20261110 內檢、新增 PRED_20261111。"""
import json
import shutil

P = 'memory/meta_predictions/predictions.json'
shutil.copy(P, 'memory/meta_predictions/predictions.json.bak_20261111')

d = json.load(open(P))

# --- 1. PRED_20261109 正式驗證（檢查日 2026-11-11） ---
for e in d:
    if e['id'] == 'PRED_20261109':
        e['verification'] = {
            'date': '2026-11-11',
            'result': 'all_miss',
            'actual': (
                '情境A: 超級路卡利歐 ex 合併 AWR 51.71%（門檻 ≥52.0%，反向 −0.54pt，距門檻 0.29pt）；'
                '情境B: 自爆磁怪合併份額 3.54%（門檻 ≥3.8%，距 0.26pt，動能 +0.97→+0.31→+0.21pt 逐日衰減）；'
                '情境C: C1 新舊卡 AWR 差距 3.06pt（門檻 ≥3.5pt，距 0.44pt，前一日幾乎停滯於 2.95pt）。'
            ),
            'lesson': (
                '三條失敗原因各不相同：A 是方向反轉（份額升、AWR 跌的靶心型），B 是動能衰減＋距離不足，'
                'C 是擴張停滯。帶狀距離規則只保證門檻有鑑別力、不會被雜訊觸發，保證不了趨勢會持續。'
                '→ 新規則：設定門檻時必須同時寫出「距離 ÷ 單日動能＝預計天數」，檢查日為兩天後者預計天數需 ≤2 天。'
            ),
        }
        e['reflection'] = (
            '0/3 全滅。教訓一：門檻距離需做「可達成性檢查」（距離 ÷ 單日動能 ≤ 2 天）。'
            '教訓二：同一牌組同一指標不得連續兩日下修門檻，否則命中率會被灌水；趨勢延伸型必須改指標或換族群。'
            '教訓三：雙升支線的同升幅度小時，隔日回吐機率更高（自爆磁怪今日 +0.21／+0.57 即為此型）。'
            '教訓四：退坑要分「族群退坑」與「版本內轉移」——忍蛙家族合計只降 0.16pt，其餘是 Mega 版搬到普通版。'
        )

# --- 2. PRED_20261110 內檢（正式檢查日 2026-11-12） ---
for e in d:
    if e['id'] == 'PRED_20261110':
        e['interim_check'] = {
            'date': '2026-11-11',
            'check_date': '2026-11-12',
            'source': 'Limitless TCG Live 2026-11-11 20:05 (UTC+8), C1 Standard 50 錦標賽／6,413 玩家／19,770 對局',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '超級路卡利歐 ex 合併 AWR <52.0%',
                    'result': 'broken_early',
                    'actual': '51.71%（昨 52.25%），已破門檻；份額續升 5.28→5.41%、AWR −0.54pt，靶心效應第三日。',
                },
                {
                    'scenario': 'B',
                    'predicted': '自爆磁怪合併份額 ≥3.8%',
                    'result': 'approaching_but_momentum_fading',
                    'actual': '3.54%（昨 3.33%），距門檻 0.26pt；動能 +0.31→+0.21pt（約前日 68%，尚未觸及 25% 衰退門檻）。',
                },
                {
                    'scenario': 'C',
                    'predicted': '超級甲賀忍蛙 ex 合併份額 <8.0%',
                    'result': 'broken_early',
                    'actual': '7.94%（昨 8.38%），已破門檻；份額六連降，AWR 43.57→43.47% 同步下滑，真退坑第六日。',
                },
            ],
            'score': '內檢：已破 2、逼近中 1；正式命中率仍以 2026-11-12 檢查日為準',
            'conclusion': (
                'PRED_20261110 的 A、C 已提前破；B 逼近中但動能持續衰減。'
                '依 11-10 訂的規則，同一牌組同一指標不得連續兩日下修門檻，'
                '因此 PRED_20261111 不再對路卡利歐 AWR 設定 <51.0% 的門檻，改列為觀察項。'
            ),
        }

# --- 3. 新增 PRED_20261111 ---
if not any(e['id'] == 'PRED_20261111' for e in d):
    d.append({
        'id': 'PRED_20261111',
        'date': '2026-11-11',
        'session': '晚間 20:05（C1 第十四日）',
        'set': 'C1 Day 14',
        'source': (
            'Limitless TCG Live 2026-11-11 20:05 (UTC+8), C1 Standard 50 錦標賽／6,413 玩家／19,770 對局, '
            '552 分支／178 合併；同一支 parser 重解析 11-05～11-11 raw；'
            '對位取自 24 張牌組 matchups 頁並經 scripts/verify_mu_20261111.py 覆核 55 條全數通過'
        ),
        'environment_summary': (
            'C1 第十四日，單日增加 3 場錦標賽／431 玩家／1,220 對局（連續第二個低增量日，+6.6%），'
            '環境加權 AWR 48.93→48.91%。合併份額前五：超級噴火龍 Y ex 11.40%／49.22%、月亮伊布 9.65%／48.38%、'
            '水君 ex 7.95%／51.47%、超級甲賀忍蛙 ex 7.94%／43.47%、超級七夕青鳥 ex 7.19%／53.51%。'
            'AWR 前五：自爆磁怪 55.54%、蜂女王 ex 54.59%、三首惡龍 54.36%、胡帕 ex 53.74%、超級七夕青鳥 ex 53.51%。'
            '最大結構變化：自爆磁怪以份額僅 3.54% 登頂 AWR；蜂女王 ex 擴張後退潮三連降；'
            '超級路卡利歐 ex 靶心效應第三日（份額 +0.13pt／AWR −0.54pt）；'
            '忍蛙系真退坑第六日但同家族普通忍蛙線反彈（家族合計僅降 0.16pt）。'
            'C1 含新卡 52.21%／47.14%，不含新卡 68.61%／50.20%，差距 3.06pt（再擴大 0.11pt）。'
        ),
        'predictions': [
            {
                'scenario': 'A',
                'name': '蜂女王 ex 合併 AWR <54.0%',
                'probability': 0.35,
                'description': (
                    '蜂女王 ex 合併 AWR **<54.0%**（今日 54.59%，距離 0.59pt，AWR 帶 0.5～1.5pt 內）。'
                    '預計天數 0.59 ÷ 0.21 ≈ 2.8 天（略超兩天，機率已下修）。'
                    '方向 55.01→54.80→**54.59%** 三連降，動能 −0.21pt；'
                    '族群（龍／惡系 AWR 50.58→50.56%）同向微降，AWR 型條件不降級。擴張後退潮型單條件。'
                ),
            },
            {
                'scenario': 'B',
                'name': '超級甲賀忍蛙 ex 合併份額 <7.5%',
                'probability': 0.30,
                'description': (
                    '超級甲賀忍蛙 ex 合併份額 **<7.5%**（今日 7.94%，距離 0.44pt，份額帶 0.3～0.8pt 內）。'
                    '預計天數 0.44 ÷ 0.44 ≈ 1 天。方向 8.72→8.38→**7.94%** 六連降，動能 −0.44pt 穩定，'
                    'AWR 43.57→43.47% 同步下滑，真退坑延續型單條件。'
                    '**機率下修理由：同家族普通忍蛙線「甲賀忍蛙 ex」單日反彈 +0.21pt，家族合計只降 0.16pt，'
                    '退坑有一部分只是版本內轉移。**'
                ),
            },
            {
                'scenario': 'C',
                'name': '水君 ex 合併份額 <7.5%',
                'probability': 0.25,
                'description': (
                    '水君 ex 合併份額 **<7.5%**（今日 7.95%，距離 0.45pt，份額帶 0.3～0.8pt 內）。'
                    '預計天數 0.45 ÷ 0.22 ≈ 2 天。方向 8.29→8.17→**7.95%** 兩連降，動能 −0.22pt；'
                    'AWR 持平 51.47%，屬純份額外流（水系族群 AWR 47.35→47.38% 同步微升，AWR 型條件不降級）。'
                ),
            },
        ],
        'most_likely': 'A',
        'confidence': 'medium',
        'check_date': '2026-11-13',
        'verification': None,
        'reflection': None,
    })

json.dump(d, open(P, 'w'), ensure_ascii=False, indent=1)
print('predictions.json 更新完成，共', len(d), '筆')
for e in d[-3:]:
    print(' ', e['id'], '| check_date', e.get('check_date'), '| verification', bool(e.get('verification')),
          '| interim', bool(e.get('interim_check')))
