import json, shutil
from pathlib import Path

P = Path('/home/amr/.openclaw/workspace-celesteela/memory/meta_predictions/predictions.json')
MARK = '<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-celesteela -->'
shutil.copy(P, str(P) + '.bak_20261108')
preds = json.loads(P.read_text(encoding='utf-8'))

for item in preds:
    if item.get('id') == 'PRED_20261106':
        item['verification'] = {
            'date': '2026-11-08',
            'check_date': '2026-11-08',
            'interim': False,
            'source': 'Limitless TCG Live 2026-11-08 20:05 (UTC+8), C1 Standard 38 錦標賽／4,626 玩家／13,655 對局, 441 分支／151 合併；同一支 parser 重解析 11-04～11-08 raw',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '超級甲賀忍蛙 ex 合併份額 <9.4%',
                    'result': 'hit',
                    'actual': '8.97%（11-07 為 9.30%、11-06 為 9.77%）；份額三連降且 AWR 同步跟跌（44.79→44.35→44.22%），確認是真退坑而非靶心效應。'
                },
                {
                    'scenario': 'B',
                    'predicted': '月亮伊布合併份額 <10.8%',
                    'result': 'hit',
                    'actual': '10.31%（11-07 為 10.55%、11-06 為 11.23%）；但今日 AWR 反彈 +0.11pt（48.71→48.82%），屬純份額外流，與忍蛙系的「連人帶強度一起走」不同。'
                },
                {
                    'scenario': 'C',
                    'predicted': '超級雷電獸 ex 合併 AWR <51.5%',
                    'result': 'miss',
                    'actual': '52.76%（11-07 為 52.51%、11-06 為 52.25%）；反向 +0.51pt，距門檻 1.26pt。電系族群整體轉強（族群 AWR 49.37→49.64%，自爆磁怪單日 +1.35pt）。'
                }
            ],
            'score': '2/3',
            'conclusion': f'兩條「份額單條件」全中，唯一的「AWR 單條件」因族群整體轉強而失敗。規則組合（單條件方向型＋門檻落在指標帶內＋方向連兩日一致＋動能 ≥0.2pt/日）在**份額型**條件上仍是有效判準；在**族群整體轉強**的背景下，單一分支的 AWR 條件會被族群趨勢壓過，因此 AWR 型條件必須先檢查族群方向。{MARK}'
        }
        item['reflection'] = f'反省重點：①**份額型與 AWR 型條件要分流**——PRED_20261106 的 AWR 條件之所以失敗，不是因為雷電獸本身沒訊號，而是「電系族群整體轉強」把個體拉了回來；往後設定 AWR 型條件前，先確認族群 AWR 方向與個體方向是否同向，同向才給高機率。②同一族群的兩支人氣王走勢可以相反：忍蛙系份額與 AWR 同步下滑（真退坑），月亮伊布份額跌但 AWR 彈（純份額外流）——**描述崩解必須同時報 AWR 是否跟跌**（沿用 11-07 規律）。③11-07 報告的「騎拉帝納壓自爆磁怪 71.4%」方向寫反（實際是自爆磁怪壓騎拉帝納），已更正；對位數字一律取自該牌組自己的 matchups row。{MARK}'

    if item.get('id') == 'PRED_20261107':
        item['interim_check'] = {
            'date': '2026-11-08',
            'check_date': '2026-11-09',
            'source': 'Limitless TCG Live 2026-11-08 20:05 (UTC+8), C1 Standard 38 錦標賽／4,626 玩家／13,655 對局',
            'results': [
                {
                    'scenario': 'A',
                    'predicted': '超級甲賀忍蛙 ex 合併份額 <8.8%',
                    'result': 'approaching',
                    'actual': '8.97%（昨 9.30%）；動能 −0.33pt、方向三連降，距門檻僅 0.17pt，若維持動能明日將命中。'
                },
                {
                    'scenario': 'B',
                    'predicted': '超級噴火龍 Y ex 合併 AWR <47.5%',
                    'result': 'not_approaching',
                    'actual': '48.34%（昨 48.17%）；反向 +0.17pt，四連降中斷，距門檻 0.84pt。'
                },
                {
                    'scenario': 'C',
                    'predicted': '蜂女王 ex 合併份額 ≥4.0%',
                    'result': 'approaching_but_momentum_fading',
                    'actual': '3.46%（昨 3.39%）；動能自 +1.31pt 掉到 +0.07pt，距門檻 0.54pt。'
                }
            ],
            'score': '內檢：逼近中 2、未逼近 1；正式命中率以 2026-11-09 檢查日為準',
            'conclusion': f'內檢顯示昨日的規則組合並非無敵：**動能衰減會讓條件失效**（蜂女王份額 +1.31→+0.07pt）。新增判準：當條件的單日動能跌至歷史平均動能的 25% 以下，標記為「動能衰退」，機率下調一級。{MARK}'
        }

new = {
    'id': 'PRED_20261108',
    'date': '2026-11-08',
    'session': '晚間 20:05（C1 第十一日）',
    'set': 'C1 Day 11',
    'source': 'Limitless TCG Live 2026-11-08 20:05 (UTC+8), C1 Standard 38 錦標賽／4,626 玩家／13,655 對局, 441 分支／151 合併；同一支 parser 重解析 11-04～11-08 raw；對位取自 24 張牌組 matchups 頁',
    'environment_summary': 'C1 第十一日，對局增量自 +2,811 收斂回 +525。合併份額前五：超級噴火龍 Y ex 10.72%／48.34%、月亮伊布 10.31%／48.82%、超級甲賀忍蛙 ex 8.97%／44.22%（份額三連降且 AWR 跟跌＝真退坑）、水君 ex 7.44%／51.38%（份額平而 AWR −0.65pt＝靶心）、超級七夕青鳥 ex 6.59%／54.55%。AWR 前五：蜂女王 ex 56.81%（連兩日登頂）、自爆磁怪 55.28%（單日 +1.35pt 躍居第二、份額僅 2.03%）、超級七夕青鳥 ex 54.55%、胡帕 ex 53.83%、三首惡龍 53.57%。族群：龍／惡系 27.95%／50.65%（四連升）、電系 13.77%／49.64%（唯一強度上升）、超能系 11.37%／48.93%、水系 23.09%／47.08%（唯一雙跌）。C1 含新卡 52.25%／47.27%，不含新卡 61.31%／50.01%，差距 2.73pt（連三日收斂後首次回頭 +0.05pt，擴充包仍未轉正）。3 點 KO 規則下 210+HP 桶 46.78% 仍是全環境最差（修正本地卡庫 HP 缺值後的口徑）。' + MARK,
    'predictions': [
        {
            'scenario': 'A',
            'name': '自爆磁怪合併 AWR ≥56.5%',
            'probability': 0.35,
            'description': '自爆磁怪合併 AWR **≥56.5%**（今日 55.28%，門檻距離 1.22pt，AWR 帶 0.5～1.5pt 內；方向 53.81→**55.28%** 連兩日上升，動能 +1.35pt 達標）。份額僅 2.03% 卻是全環境 AWR 第二，符合 11-07 訂的「反制樞紐擴張順序：AWR 先登頂、份額才跟上」路徑；若命中，即為下一個擴張點。'
        },
        {
            'scenario': 'B',
            'name': '水君 ex 合併 AWR <50.5%',
            'probability': 0.30,
            'description': '水君 ex 合併 AWR **<50.5%**（今日 51.38%，門檻距離 0.88pt，AWR 帶內；方向 53.43→52.03→**51.38%** 連三降，動能 −0.65pt 達標）。份額停在 7.44% 無處可退，且被蜂女王（輸 24.7%）、七夕青鳥（輸 36.8%）、胡帕（輸 37.6%）三方夾擊，靶心效應第四日。'
        },
        {
            'scenario': 'C',
            'name': '超級七夕青鳥 ex 合併份額 ≥7.0%',
            'probability': 0.25,
            'description': '超級七夕青鳥 ex 合併份額 **≥7.0%**（今日 6.59%，門檻距離 0.41pt，份額帶 0.3～0.8pt 內；方向 5.41→6.37→**6.59%** 三連升，動能 +0.22pt 剛好達標，AWR 同步守住 54.55%）。**動能僅 +0.22pt，為三條中最脆弱，若延續 11-07 蜂女王的動能衰減路徑則易失效。**'
        }
    ],
    'most_likely': 'A',
    'confidence': 'medium',
    'check_date': '2026-11-10',
    'verification': None,
    'reflection': None
}

if not any(p.get('id') == 'PRED_20261108' for p in preds):
    preds.append(new)

P.write_text(json.dumps(preds, ensure_ascii=False, indent=2), encoding='utf-8')
print('predictions:', len(preds), '| last id:', preds[-1]['id'])
