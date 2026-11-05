import json
from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/predictions.json')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'
preds = json.loads(P.read_text(encoding='utf-8'))

for item in preds:
    if item.get('id') == 'PRED_20261103':
        item['verification'] = {
            'date': '2026-11-05',
            'check_date': '2026-11-05',
            'source': 'Limitless TCG Live 2026-11-05 20:05 (UTC+8), C1 Standard 28 錦標賽／3,529 玩家／9,827 對局, 371 分支／138 合併',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '月亮伊布合併 AWR 跌破 47.5%',
                    'result': 'miss',
                    'actual': '49.41%（11-04 為 49.43%，僅 −0.02pt）；AWR 已連兩日近乎停滯，距門檻 1.91pt。'
                },
                {
                    'scenario': 'B',
                    'predicted': '水君 ex 合併份額突破 6.0%',
                    'result': 'miss',
                    'actual': '5.87%（11-04 為 5.29%，距門檻 0.13pt）；份額續升但 AWR −0.74pt，擴張未帶來強度。'
                },
                {
                    'scenario': 'C',
                    'predicted': 'C1 新舊卡 AWR 差距擴大到 ≥5.0pt',
                    'result': 'miss',
                    'actual': '2.91pt（11-04 為 2.85pt，僅擴大 0.06pt）；距門檻 2.09pt。'
                }
            ],
            'score': '0/3 命中',
            'conclusion': f'三條全滅。A 的下行動能已停、B 的份額動能不足且強度反向、C 的差距僅微幅擴大；舊式遠距門檻再次缺乏鑑別力。{MARK}'
        }
        item['reflection'] = f'正式驗證仍為 0/3。A 的門檻距離超出 AWR 實際波動帶；B 距門檻僅 0.13pt，屬追逐噪音；C 的差距雖反轉向上，但單日只擴大 0.06pt，遠不足以支撐 5pt 目標。後續只採用單條件、連續兩日同方向且距離落在指標帶內的情境。{MARK}'
    elif item.get('id') == 'PRED_20261104':
        item['verification'] = {
            'date': '2026-11-05',
            'check_date': '2026-11-05',
            'source': 'Limitless TCG Live 2026-11-05 20:05 (UTC+8), C1 Standard 28 錦標賽／3,529 玩家／9,827 對局, 371 分支／138 合併',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '含 C1 新卡族群 AWR ≥48.2%',
                    'result': 'miss',
                    'actual': '47.16%（11-04 為 47.19%，−0.03pt）；新舊卡差距 2.85→2.91pt，僅反向擴大 0.06pt。'
                },
                {
                    'scenario': 'B',
                    'predicted': '超級甲賀忍蛙 ex 合併份額 <10.2%',
                    'result': 'hit',
                    'actual': '10.17%（11-04 為 10.57%，−0.40pt）；份額三連降，AWR 44.62→44.75% 小幅回升。'
                },
                {
                    'scenario': 'C',
                    'predicted': '格鬥／草／鋼系族群合併 AWR ≥49.5%',
                    'result': 'miss',
                    'actual': '48.07%（11-04 為 48.10%，−0.03pt）；族群份額反而由 6.68% 升至 8.25%。'
                }
            ],
            'score': '1/3 命中',
            'conclusion': f'僅份額崩解型 B 命中。新包 AWR 沒有止穩；格鬥／草／鋼系是「份額升、強度平」，不能誤判為族群強度反攻。{MARK}'
        }
        item['reflection'] = f'B 證明「單條件份額下行＋連續兩日同方向」仍有效。A 失敗的關鍵不是距離，而是把「份額下降」誤當成「強度即將回升」的充分證據；新卡份額 53.99→53.33%、AWR 47.19→47.16%、差距 2.85→2.91pt，顯示拖累只是停滯。C 的族群份額已 +1.57pt，但 AWR −0.03pt；資金遷入不等於強度提升。{MARK}'

new_item = {
    'id': 'PRED_20261105',
    'date': '2026-11-05',
    'session': '晚間 20:05（C1 第八日）',
    'set': 'C1 Day 8',
    'source': 'Limitless TCG Live 2026-11-05 20:05 (UTC+8), C1 Standard 28 錦標賽／3,529 玩家／9,827 對局, 371 分支／138 合併；同一支 parser 重解析 11-03／11-04 raw；對位取自 24 張牌組 matchups 頁',
    'environment_summary': f'C1 第八日。合併份額前三：月亮伊布 11.56%／49.41%（兩日 −1.41pt、AWR 近乎持平）、超級甲賀忍蛙 ex 10.17%／44.75%（兩日 −0.84pt）、超級噴火龍 Y ex 9.97%／48.90%（兩日 −1.00pt）。AWR 前五：超級七夕青鳥 ex 55.07%、胡帕 ex 55.04%、蜂女王 ex 54.41%、三首惡龍 53.63%、水君 ex 53.12%。資金向舊卡高效率線遷移：七夕青鳥、胡帕、水君、蜂女王、超級蜥蜴王、超級路卡利歐及雷電獸份額皆上升；水君、七夕青鳥、胡帕的 AWR 則小跌。C1 含新卡族群 53.33%／47.16%，不含新卡 54.83%／50.07%，差距 2.91pt，未止穩。族群：龍／惡系 25.28%／50.62%（兩日 +2.00pt／−0.46pt）、格鬥／草／鋼系 8.25%／48.07%（兩日 +2.15pt／+1.25pt）。3 點 KO 規則下 240HP 超級快龍 ex／超級班基拉斯 ex 仍僅 39.06%／39.57%，200HP 超級甲賀忍蛙 ex 44.75%。{MARK}',
    'predictions': [
        {
            'scenario': 'A',
            'name': '月亮伊布份額跌破 11%',
            'probability': 0.35,
            'description': '月亮伊布合併份額 **<11.0%**（今日 11.56%，門檻距離 0.56pt，份額帶內；方向：12.97→12.31→11.56% 連兩日下降）。今日 AWR 49.43→49.41% 近乎不動，若份額續跌而 AWR 不跟跌，將確認它已從「人氣王靶心」轉為單純份額外流，份額與強度正式脫鉤。'
        },
        {
            'scenario': 'B',
            'name': '忍蛙系份額跌破 9.7%',
            'probability': 0.35,
            'description': '超級甲賀忍蛙 ex 合併份額 **<9.7%**（今日 10.17%，門檻距離 0.47pt，份額帶內；方向：11.01→10.57→10.17% 連兩日下降）。今日 AWR 44.62→44.75% 小幅回升，若只跌份額不跌強度，將再次驗證「崩解只剩份額面」。'
        },
        {
            'scenario': 'C',
            'name': '格鬥／草／鋼系份額突破 9%',
            'probability': 0.30,
            'description': '格鬥／草／鋼系族群合併份額 **≥9.0%**（今日 8.25%，門檻距離 0.75pt，份額帶內；方向：6.10→6.68→8.25% 連兩日上升）。不再以 AWR 作第二條件，因今日族群 AWR 48.13→48.07% 近乎持平，資金遷入尚未轉成強度。'
        }
    ],
    'most_likely': 'A（與 B 並列 0.35）',
    'confidence': 'low-medium',
    'check_date': '2026-11-07',
    'verification': None,
    'reflection': None
}

# 避免重跑時重複追加
preds = [x for x in preds if x.get('id') != 'PRED_20261105']
preds.append(new_item)
P.write_text(json.dumps(preds, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('updated', len(preds), 'predictions; latest', preds[-1]['id'])
