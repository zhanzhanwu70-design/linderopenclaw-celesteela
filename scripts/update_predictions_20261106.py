import json
from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/predictions.json')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'
preds = json.loads(P.read_text(encoding='utf-8'))

for item in preds:
    if item.get('id') == 'PRED_20261105':
        item['verification'] = {
            'date': '2026-11-06',
            'check_date': '2026-11-07',
            'interim': True,
            'source': 'Limitless TCG Live 2026-11-06 20:05 (UTC+8), C1 Standard 31 錦標賽／3,714 玩家／10,319 對局, 383 分支／144 合併',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '月亮伊布合併份額 <11.0%',
                    'result': 'pending',
                    'actual': '11.23%（11-05 為 11.56%，−0.33pt）；距門檻 0.23pt，逼近中，正式判定待 2026-11-07。'
                },
                {
                    'scenario': 'B',
                    'predicted': '超級甲賀忍蛙 ex 合併份額 <9.7%',
                    'result': 'pending',
                    'actual': '9.77%（11-05 為 10.17%，−0.40pt）；距門檻 0.07pt，逼近中，正式判定待 2026-11-07。'
                },
                {
                    'scenario': 'C',
                    'predicted': '格鬥／草／鋼系族群合併份額 ≥9.0%',
                    'result': 'miss',
                    'actual': '8.45%（11-05 為 8.25%，+0.20pt）；距門檻 0.55pt，動能 +0.20pt 剛好達標但幅度不足。'
                }
            ],
            'score': '內檢 0/3（已破 0、逼近中 2、未逼近 1）；正式命中率以 2026-11-07 檢查日為準',
            'conclusion': f'檢查日前一天，A、B 兩條都只剩 0.23pt／0.07pt 的距離，方向與動能皆符合規則，判定幾乎確定會在檢查日翻成；C 距離 0.55pt 屬「未逼近」。新增「內檢三級狀態」規則：已破／逼近中（<0.3pt 且動能未衰）／未逼近（>0.5pt）。{MARK}'
        }
        item['reflection'] = f'內檢 0/3，但不可視為失敗：A、B 為逼近中，C 為未逼近，正式判定留待 11-07。補充兩條可複用規律：①差距「收斂」本身不是訊號，收斂速度才是——新舊卡差距 2.92→2.74pt（−0.18pt）不足 11-04 那次（−0.59pt）的三分之一，擴充包轉正應改看「差距連兩日收斂且每日收斂 ≥0.3pt」或「新卡 AWR 單日回升 ≥0.5pt」；②族群需新增「份額平＋AWR 跌＝觀望期（資金停滯）」分支，與「份額跌＋AWR 跌＝真退坑」區分，電系今日正屬前者（雷電獸 −0.60pt、密勒頓 −0.63pt、自爆磁怪 −0.72pt，份額幾乎不動）。{MARK}'

new = {
    'id': 'PRED_20261106',
    'date': '2026-11-06',
    'session': '晚間 20:05（C1 第九日）',
    'set': 'C1 Day 9',
    'source': 'Limitless TCG Live 2026-11-06 20:05 (UTC+8), C1 Standard 31 錦標賽／3,714 玩家／10,319 對局, 383 分支／144 合併；同一支 parser 重解析 11-03／11-04／11-05 raw；對位取自 24 張牌組 matchups 頁',
    'environment_summary': 'C1 第九日，對局增量自 +1,716 收斂至 +492。合併份額前五：超級噴火龍 Y ex 9.91%（升至第二）、月亮伊布 11.23%／49.41%（兩日 −1.08pt、AWR 幾乎不動）、超級甲賀忍蛙 ex 9.77%／44.79%（兩日 −0.80pt）、水君 ex 6.00%／53.43%（份額四連升且 AWR 回升）、超級七夕青鳥 ex 5.41%／54.40%（份額三連升、AWR 三日 −0.78pt）。AWR 前五：胡帕 ex 54.96%（取代七夕青鳥登頂，差距僅 0.56pt）、超級七夕青鳥 ex 54.40%、蜂女王 ex 54.35%、三首惡龍 53.91%、水君 ex 53.43%。對位樞紐轉移：蜂女王 ex 份額僅 2.07% 卻壓忍蛙 85.7%、壓水君 74.4%、壓月亮伊布 68.2%、壓胡帕 53.1%；胡帕首次出現明確剋星（輸超級超夢 X ex 26.1%，N=23，列觀察名單）。C1 含新卡族群 52.53%／47.20%，不含新卡 55.22%／49.94%，差距 2.74pt（收斂 0.18pt，不足以判定轉正）。族群：龍／惡系 25.44%／50.58%、格鬥／草／鋼系 8.45%／48.48%（唯一份額與強度同升）、水系 22.78%／47.67%、電系 13.09%／48.42%（份額平、強度跌＝觀望期）。3 點 KO 規則下 240HP 超級快龍 ex／超級班基拉斯 ex 仍僅 38.87%／40.07%。' + MARK,
    'predictions': [
        {
            'scenario': 'A',
            'name': '超級甲賀忍蛙 ex 份額跌破 9.4%',
            'probability': 0.35,
            'description': '超級甲賀忍蛙 ex 合併份額 **<9.4%**（今日 9.77%，門檻距離 0.37pt，份額帶 0.3～0.8pt 內；方向 10.57→10.17→9.77% 連兩日下降，動能 −0.40pt 達標）。若命中，代表人氣王陷阱的份額外流進入第五日，且今日 AWR 44.79%（四天最高）會正式確認「崩解只剩份額面」。'
        },
        {
            'scenario': 'B',
            'name': '月亮伊布份額跌破 10.8%',
            'probability': 0.35,
            'description': '月亮伊布合併份額 **<10.8%**（今日 11.23%，門檻距離 0.43pt，份額帶內；方向 12.31→11.56→11.23% 連兩日下降，動能 −0.33pt 達標）。AWR 三日 49.43→49.41→49.41% 幾乎不動，若份額續跌而 AWR 不跟跌，則正式確認其已由「人氣王靶心」轉為純份額外流。'
        },
        {
            'scenario': 'C',
            'name': '超級雷電獸 ex AWR 跌破 51.5%',
            'probability': 0.30,
            'description': '超級雷電獸 ex 合併 AWR **<51.5%**（今日 52.25%，門檻距離 0.75pt，AWR 帶 0.5～1.5pt 內；方向 53.72→52.85→52.25% 連兩日下降，動能 −0.60pt 達標）。電系三線（雷電獸 −0.60、密勒頓 −0.63、自爆磁怪 −0.72）同步下滑且族群份額幾乎不動，若雷電獸跌破 51.5%，即確認電系進入「觀望期」（資金停滯）而非退坑潮。'
        }
    ],
    'most_likely': 'A（與 B 並列 0.35）',
    'confidence': 'low-medium',
    'check_date': '2026-11-08',
    'verification': None,
    'reflection': None
}

if not any(p.get('id') == 'PRED_20261106' for p in preds):
    preds.append(new)

P.write_text(json.dumps(preds, ensure_ascii=False, indent=2), encoding='utf-8')
print('predictions:', len(preds), '| last id:', preds[-1]['id'])
