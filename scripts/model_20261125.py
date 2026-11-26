#!/usr/bin/env python3
"""2026-11-25 副牌濃度模型：檢查日 11-27 份額門檻可行性 + AWR 門檻所需原始勝率。
口徑：
・share% = K × (D / T) × 100，K = 今日實測（41 支 N>=200 可比牌組）。
・所需吸收 dD = D1 − D0，D1 = S/K × T1；吸收濃度 = dD / ΔT。
・r = 吸收濃度 ÷ 該牌組歷史正吸收濃度中位。
・壓力測試：零吸收 → 份額 = K×D0/T1；最大吸收（歷史單日最大 ×2）→ 份額 = K×(D0+2dmax)/T1。
"""
import collections
import json
import statistics

K = 1.2466
T0 = 14213          # 今日總副牌
SCEN = {'保守': 518, '中央': 678, '積極': 838}   # 檢查日 11-27 預估副牌增量
HOLD = {'保守': 14731, '中央': 14891, '積極': 15051}

# 歷史吸收濃度（由 11-10～11-25 實測，%）
HIST = {
    'Entei ex': [0.19, 3.02, 1.34, 0.61, 0.50, 0.62, 0.63, 0.73, 0.00, 0.87, 1.36, 1.27, 0.00, 1.81, 3.82, 5.64],
    'Hoopa ex': [5.01, 4.87, 5.70, 3.64, 5.71, 6.34, 5.50, 11.72, 9.13, 10.76, 8.18, 11.02, 7.41, 10.27, 9.16, 9.60],
    'Hydreigon': [1.73, 2.09, 1.34, 2.43, 2.00, 2.32, 2.54, 2.20, 2.83, 1.45, 2.73, 2.97, 5.56, 2.60, 5.34, 4.18],
    'Mega Greninja ex': [3.08, 1.86, 3.36, 4.45, 3.81, 3.55, 1.90, 2.20, 3.48, 1.74, 2.27, 1.84, 0.00, 2.60, 3.82, 2.51],
    '超級七夕青鳥 ex': [6.17, 5.80, 4.03, 8.30, 8.52, 14.37, 14.38, 16.85, 13.70, 13.95, 10.45, 11.58, 1.85, 9.71, 9.16, 11.27],
    '咚咚鼠 ex': [0.77, 0.93, 0.34, 0.61, 0.30, 1.08, 0.85, 1.10, 0.65, 2.62, 1.82, 1.41, 3.70, 2.60, 4.58, 3.13],
    '水君 ex': [5.39, 4.87, 6.38, 6.48, 5.91, 5.87, 6.13, 4.40, 4.35, 5.81, 5.00, 4.24, 5.56, 6.21, 3.05, 3.34],
}


def agg(path):
    rows = json.load(open(path, encoding='utf-8'))['rows']
    out = collections.defaultdict(lambda: {'share': 0.0, 'decks': 0, 'n': 0, 'w': 0})
    for r in rows:
        a = out[r['name']]
        for k in ('share', 'decks', 'n', 'w'):
            a[k] += r[k]
    res = []
    for k, v in out.items():
        v = dict(v)
        v['name'] = k
        v['awr'] = (v['w'] + 12) / (v['n'] + 25) * 100 if v['n'] else 0
        v['raw'] = v['w'] / v['n'] * 100 if v['n'] else 0
        res.append(v)
    return res


T = agg('memory/ptcgp_meta_20261125_std_comb.json')
IDX = {r['name']: r for r in T}
ENV_N = sum(r['n'] for r in T)
ENV_W = sum(r['w'] for r in T)
print(f"全環境 AWR {(ENV_W+12)/(ENV_N+25)*100:.4f}% N={ENV_N} 總副牌 {sum(r['decks'] for r in T)}")


DAYS = ['202611%02d' % i for i in range(10, 26)]


def hist_decks(name):
    vals = []
    for i in range(1, len(DAYS)):
        a, b = DAYS[i - 1], DAYS[i]
        dT = sum(x['decks'] for x in agg(f'memory/ptcgp_meta_{a}_std_comb.json')) and None
        rows_b = agg(f'memory/ptcgp_meta_{b}_std_comb.json')
        rows_a = agg(f'memory/ptcgp_meta_{a}_std_comb.json')
        TB = sum(x['decks'] for x in rows_b)
        TA = sum(x['decks'] for x in rows_a)
        rb = [x for x in rows_b if x['name'] == name]
        ra = [x for x in rows_a if x['name'] == name]
        if rb and ra and TB > TA:
            vals.append(rb[0]['decks'] - ra[0]['decks'])
    return vals


def model(name, threshold, up=True, hist_key=None):
    r = IDX[name]
    D0 = r['decks']
    med = statistics.median([x for x in HIST[hist_key or name] if x > 0])
    dv = hist_decks(name)
    dmax = max(dv) if dv else 0
    print(f"\n== {name}  現值 {r['share']:.4f}%／D={D0}／AWR {r['awr']:.4f}%／N={r['n']}")
    print(f"   門檻 {threshold:.4f}%  距離 {abs(threshold - r['share']):.4f}pt  歷史正吸收中位 {med:.2f}%  單日最大 {dmax:.2f}%")
    for lab in ('保守', '中央', '積極'):
        T1 = HOLD[lab]
        D1 = threshold / 100 / K * T1
        dD = D1 - D0
        conc = dD / SCEN[lab] * 100
        zero = K * D0 / T1 * 100
        mx = K * (D0 + 2 * dmax) / T1 * 100
        print(f"   [{lab}] T1={T1} D1={D1:.1f} dD={dD:+.1f} 濃度={conc:5.2f}% r={conc/med:.2f} | 零吸收 {zero:.4f}% | 最大吸收(+{dmax}×2) {mx:.4f}% | 歷史單日最大吸收 {dmax:+d} 副")


model('Hydreigon', 2.90)          # 參考用（份額型本輪不採用）
model('Entei ex', 1.05)
model('Hoopa ex', 8.60)
model('Mega Greninja ex', 5.98)   # 下降型（份額 < 門檻）
model('Mega Greninja ex', 6.00, up=False)

print('\n### AWR 門檻所需原始勝率（檢查日 11-27）')
for nm, thr in [('Hydreigon', 54.80), ('Hydreigon', 54.50), ('Mega Greninja ex', 43.00), ('Mega Greninja ex', 43.30)]:
    r = IDX[nm]
    N1 = r['n'] + 1552 * (r['n'] / ENV_N)
    needW = thr / 100 * (N1 + 25) - 12
    print(f"  {nm:20} 門檻 {thr:.2f}%：N {r['n']} → N1≈{N1:.0f}，需原始勝率 {needW/N1*100:.2f}%（今日 {r['raw']:.2f}%，需 {needW/N1*100-r['raw']:+.2f}pt）")
