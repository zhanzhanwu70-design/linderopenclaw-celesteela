import json
import shutil
from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/predictions.json')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'
shutil.copy(P, str(P) + '.bak_20261109')
preds = json.loads(P.read_text(encoding='utf-8'))

for item in preds:
    if item.get('id') == 'PRED_20261107':
        item['verification'] = {
            'date': '2026-11-09',
            'check_date': '2026-11-09',
            'interim': False,
            'source': 'Limitless TCG Live 2026-11-09 20:05 (UTC+8), C1 Standard 43 錦標賽／5,559 玩家／17,380 對局, 506 分支／168 合併；同一支 parser 重解析 11-04～11-09 raw',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '超級甲賀忍蛙 ex 合併份額 <8.8%',
                    'result': 'hit',
                    'actual': '8.72%（11-08 為 8.97%、11-07 為 9.30%）；份額四連降，且 AWR 44.35→44.22→43.65% 同步下滑，確認是真退坑。'
                },
                {
                    'scenario': 'B',
                    'predicted': '超級噴火龍 Y ex 合併 AWR <47.5%',
                    'result': 'miss',
                    'actual': '49.16%（11-08 為 48.34%、11-07 為 48.17%）；單日反彈 +0.82pt，四連降中斷，距門檻 1.66pt。'
                },
                {
                    'scenario': 'C',
                    'predicted': '蜂女王 ex 合併份額 ≥4.0%',
                    'result': 'hit',
                    'actual': '5.23%（11-08 為 3.46%、11-07 為 3.39%）；單日 +1.78pt，但 AWR 56.81→55.01% 同步下滑，屬擴張中的靶心效應。'
                }
            ],
            'score': '2/3',
            'conclusion': f'正式命中 2/3。份額型條件全中，唯一失手的噴火龍 AWR 條件因單日反轉而未破。11-08 的「蜂女王份額動能衰退」判斷在今日 +3,725 對局的大樣本更新中被推翻，顯示**大增量日不能用前一日動能衰減直接判定條件失效**。{MARK}'
        }
        item['reflection'] = f'反省重點：①**動能衰減判準必須納入樣本增量**：蜂女王份額 11-08 僅 +0.07pt，但 11-09 在 +3,725 對局後單日 +1.78pt；往後遇到大增量日，至少改看兩日累計方向，不以單日動能直接降級。②**擴張不等於轉強**：蜂女王份額達標但 AWR −1.80pt，應描述為「擴張中的靶心效應」，不可只看份額門檻宣告強度上升。③忍蛙系是唯一「份額跌＋AWR 跌」的真退坑，噴火龍則在門檻前反彈；兩者同為人氣王，判定仍須拆開。{MARK}'

    if item.get('id') == 'PRED_20261108':
        item['interim_check'] = {
            'date': '2026-11-09',
            'check_date': '2026-11-10',
            'source': 'Limitless TCG Live 2026-11-09 20:05 (UTC+8), C1 Standard 43 錦標賽／5,559 玩家／17,380 對局',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '自爆磁怪合併 AWR ≥56.5%',
                    'result': 'not_approaching',
                    'actual': '同名合併 55.28%（主分支 55.35%）；昨 55.16%／主分支 55.28%，僅 +0.12pt，距門檻 1.22pt。'
                },
                {
                    'scenario': 'B',
                    'predicted': '水君 ex 合併 AWR <50.5%',
                    'result': 'not_approaching',
                    'actual': '51.31%（昨 51.38%）；僅 −0.07pt，動能幾乎停滯，距門檻 0.81pt。'
                },
                {
                    'scenario': 'C',
                    'predicted': '超級七夕青鳥 ex 合併份額 ≥7.0%',
                    'result': 'hit_early',
                    'actual': '7.27%（昨 6.59%）；份額三連升，門檻已提前突破，但 AWR 54.55→53.72% 呈靶心磨損。'
                }
            ],
            'score': '內檢：提前命中 1、未逼近 2；正式命中率仍以 2026-11-10 檢查日為準',
            'conclusion': f'內檢顯示 PRED_20261108 的 C 已提前命中；A、B 距離門檻仍大。A 的自爆磁怪仍守在 AWR 前列但未加速，B 的水君 ex AWR 動能近乎停滯。{MARK}'
        }

new = {
    'id': 'PRED_20261109',
    'date': '2026-11-09',
    'session': '晚間 20:05（C1 第十二日）',
    'set': 'C1 Day 12',
    'source': 'Limitless TCG Live 2026-11-09 20:05 (UTC+8), C1 Standard 43 錦標賽／5,559 玩家／17,380 對局, 506 分支／168 合併；同一支 parser 重解析 11-04～11-09 raw；對位取自 24 張牌組 matchups 頁',
    'environment_summary': 'C1 第十二日，單日增加 5 場錦標賽／933 玩家／3,725 對局，環境加權 AWR 48.78→48.96%。合併份額前五：超級噴火龍 Y ex 11.35%／49.16%、月亮伊布 10.04%／48.63%、超級甲賀忍蛙 ex 8.72%／43.65%、水君 ex 8.29%／51.31%、超級七夕青鳥 ex 7.27%／53.72%。AWR 前五：自爆磁怪 55.28%、蜂女王 ex 55.01%、三首惡龍 54.81%、超級七夕青鳥 ex 53.72%、胡帕 ex 53.68%。最大結構變化：超級路卡利歐 ex 份額 +1.86pt／AWR +3.08pt，為罕見「份額與強度同升」；蜂女王 ex 份額 +1.78pt／AWR −1.80pt，屬擴張中的靶心效應。C1 含新卡 54.09%／47.28%，不含新卡 68.20%／50.24%，差距 2.96pt（再擴大 0.23pt）。' + MARK,
    'predictions': [
        {
            'scenario': 'A',
            'name': '超級路卡利歐 ex 合併 AWR ≥52.0%',
            'probability': 0.35,
            'description': '超級路卡利歐 ex 合併 AWR **≥52.0%**（今日 53.21%，距離 1.21pt，AWR 帶 0.5～1.5pt 內）。方向 50.00→50.13→**53.21%** 連兩日上升，動能 +3.08pt 達標；N=1,392，且格鬥／草／鋼系族群 AWR 48.41→49.94% 同向上升。屬守住型單條件。'
        },
        {
            'scenario': 'B',
            'name': '自爆磁怪合併份額 ≥3.8%',
            'probability': 0.30,
            'description': '自爆磁怪合併份額 **≥3.8%**（今日 3.02%，距離 0.78pt，份額帶 0.3～0.8pt 內）。方向 1.96→2.05→**3.02%** 連兩日上升，動能 +0.97pt 達標；AWR 53.81→55.16→**55.28%** 同步守住，符合「AWR 先登頂、份額才跟上」路徑。'
        },
        {
            'scenario': 'C',
            'name': 'C1 新舊卡 AWR 差距 ≥3.5pt',
            'probability': 0.25,
            'description': 'C1 新舊卡 AWR 差距 **≥3.5pt**（今日 2.96pt，距離 0.54pt，差距帶 0.5～1.0pt 內）。方向 2.68→2.73→**2.96pt** 連兩日擴大，且含新卡份額 52.25→54.09%、AWR 47.27→47.28% 幾乎不動，擴充包拖累仍在。'
        }
    ],
    'most_likely': 'A',
    'confidence': 'medium',
    'check_date': '2026-11-11',
    'verification': None,
    'reflection': None
}

if not any(p.get('id') == 'PRED_20261109' for p in preds):
    preds.append(new)

P.write_text(json.dumps(preds, ensure_ascii=False, indent=2), encoding='utf-8')
print('predictions:', len(preds), '| last id:', preds[-1]['id'])
