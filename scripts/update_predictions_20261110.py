import json
import shutil
from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/predictions.json')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'
shutil.copy(P, str(P) + '.bak_20261110')
preds = json.loads(P.read_text(encoding='utf-8'))

for item in preds:
    if item.get('id') == 'PRED_20261108':
        item['verification'] = {
            'date': '2026-11-10',
            'check_date': '2026-11-10',
            'interim': False,
            'source': 'Limitless TCG Live 2026-11-10 20:05 (UTC+8), C1 Standard 47 錦標賽／5,982 玩家／18,550 對局, 529 分支／172 合併；同一支 parser 重解析 11-05～11-10 raw',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '自爆磁怪合併 AWR ≥56.5%',
                    'result': 'miss',
                    'actual': '同名合併 54.97%（主分支 55.03%）；昨 55.28%，單日 −0.31pt，距門檻 1.53pt。'
                },
                {
                    'scenario': 'B',
                    'predicted': '水君 ex 合併 AWR <50.5%',
                    'result': 'miss',
                    'actual': '51.47%（昨 51.31%）；反向 +0.16pt，距門檻 0.97pt。'
                },
                {
                    'scenario': 'C',
                    'predicted': '超級七夕青鳥 ex 合併份額 ≥7.0%',
                    'result': 'hit',
                    'actual': '7.29%（昨 7.27%）；守住 7% 以上，但 AWR 53.72→53.30% 呈靶心磨損。'
                }
            ],
            'score': '1/3',
            'conclusion': f'正式命中 1/3。兩條 AWR 型條件全數落空，唯一命中的份額型條件也只是「守住」而非突破。根因是今日為低增量日（單日 +1,170 對局，+6.7%；全環境 AWR 48.96→48.93%），個體 AWR 幾乎凍結，距離門檻 0.8～1.2pt 的 AWR 條件在這種環境下本來就走不到。{MARK}'
        }
        item['reflection'] = f'反省重點：①**低增量日必須改用「份額型」或近距離 AWR 型條件**：今日證明距離 >0.8pt 的 AWR 條件在低增量日等於不可能命中，之後在增量 <1,500 對局的日子應直接改設份額型條件。②**份額門檻「守住」與「突破」要分開記帳**：七夕青鳥 7.27→7.29% 只是守住 7%，不能寫成突破。③自爆磁怪 54.97% 仍在 AWR 前二、份額續升到 3.33%，它的強度並未崩，只是今日沒有加速。{MARK}'

    if item.get('id') == 'PRED_20261109':
        item['interim_check'] = {
            'date': '2026-11-10',
            'check_date': '2026-11-11',
            'source': 'Limitless TCG Live 2026-11-10 20:05 (UTC+8), C1 Standard 47 錦標賽／5,982 玩家／18,550 對局',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '超級路卡利歐 ex 合併 AWR ≥52.0%',
                    'result': 'still_true_but_fragile',
                    'actual': '52.25%（昨 53.21%），仍 ≥52.0% 但只剩 0.25pt 緩衝，單日 −0.96pt，動能已翻負。'
                },
                {
                    'scenario': 'B',
                    'predicted': '自爆磁怪合併份額 ≥3.8%',
                    'result': 'approaching',
                    'actual': '3.33%（昨 3.02%），距門檻 0.47pt；動能由 +0.97pt 衰減到 +0.31pt（約前日的 32%，尚未觸及 25% 衰退門檻）。'
                },
                {
                    'scenario': 'C',
                    'predicted': 'C1 新舊卡 AWR 差距 ≥3.5pt',
                    'result': 'approaching_but_stalled',
                    'actual': '2.95pt（昨 2.96pt），單日幾乎沒動；含新卡份額 54.09→53.44%、AWR 47.28→47.25%。'
                }
            ],
            'score': '內檢：仍成立 1（緩衝僅 0.25pt）、逼近中 2；正式命中率仍以 2026-11-11 檢查日為準',
            'conclusion': f'PRED_20261109 的 A 條件已從「安全」變成「脆弱」：超級路卡利歐 ex 由雙升轉為份額升、AWR 跌的靶心型，52.25% 只比門檻高 0.25pt。B 仍在軌道上但動能衰減。C 停滯。{MARK}'
        }

new = {
    'id': 'PRED_20261110',
    'date': '2026-11-10',
    'session': '晚間 20:05（C1 第十三日）',
    'set': 'C1 Day 13',
    'source': 'Limitless TCG Live 2026-11-10 20:05 (UTC+8), C1 Standard 47 錦標賽／5,982 玩家／18,550 對局, 529 分支／172 合併；同一支 parser 重解析 11-05～11-10 raw；對位取自 24 張牌組 matchups 頁並經 scripts/verify_mu_20261110.py 覆核',
    'environment_summary': 'C1 第十三日，單日增加 4 場錦標賽／423 玩家／1,170 對局（低增量日，+6.7%），環境加權 AWR 48.96→48.93%。合併份額前五：超級噴火龍 Y ex 11.52%／49.05%、月亮伊布 9.88%／48.63%、超級甲賀忍蛙 ex 8.38%／43.57%、水君 ex 8.17%／51.47%、超級七夕青鳥 ex 7.29%／53.30%。AWR 前五：三首惡龍 55.24%、自爆磁怪 54.97%、蜂女王 ex 54.80%、胡帕 ex 53.79%、超級七夕青鳥 ex 53.30%。最大結構變化：超級路卡利歐 ex 從昨日的「份額與 AWR 雙升」翻成份額 +0.57pt／AWR −0.96pt 的靶心型；三首惡龍以份額 2.52%、AWR 55.24% 登頂。C1 含新卡 53.44%／47.25%，不含新卡 68.87%／50.20%，差距 2.95pt（連兩日停滯）。' + MARK,
    'predictions': [
        {
            'scenario': 'A',
            'name': '超級路卡利歐 ex 合併 AWR <52.0%',
            'probability': 0.35,
            'description': '超級路卡利歐 ex 合併 AWR **<52.0%**（今日 52.25%，距離 0.25pt，AWR 帶 0.1～0.5pt 內，是最容易被觸發的一段）。方向 50.13→53.21→**52.25%**，單日動能 **−0.96pt** 為全環境最強負動能；族群（格鬥／草／鋼系 AWR 49.94→49.62%）同向下行，AWR 型條件不降級。屬「靶心化續行」型單條件。'
        },
        {
            'scenario': 'B',
            'name': '自爆磁怪合併份額 ≥3.8%',
            'probability': 0.30,
            'description': '自爆磁怪合併份額 **≥3.8%**（今日 3.33%，距離 0.47pt，份額帶 0.3～0.8pt 內）。方向 2.05→3.02→**3.33%** 連兩日上升，但動能 +0.97→+0.31pt 明顯衰減（約前日的 32%，尚未觸及 25% 衰退門檻），**標記「動能衰退觀察」**；AWR 同步守住 54.97%。'
        },
        {
            'scenario': 'C',
            'name': '超級甲賀忍蛙 ex 合併份額 <8.0%',
            'probability': 0.25,
            'description': '超級甲賀忍蛙 ex 合併份額 **<8.0%**（今日 8.38%，距離 0.38pt，份額帶 0.3～0.8pt 內）。方向 9.77→9.30→8.97→8.72→**8.38%** 五連降，動能 −0.35pt 穩定，AWR 44.79→**43.57%** 同步下滑，真退坑延續型單條件。'
        }
    ],
    'most_likely': 'A',
    'confidence': 'medium',
    'check_date': '2026-11-12',
    'verification': None,
    'reflection': None
}

if not any(p.get('id') == 'PRED_20261110' for p in preds):
    preds.append(new)

P.write_text(json.dumps(preds, ensure_ascii=False, indent=2), encoding='utf-8')
print('predictions:', len(preds), '| last id:', preds[-1]['id'])
