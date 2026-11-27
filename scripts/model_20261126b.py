#!/usr/bin/env python3
"""2026-11-26 模型：PRED_20261126（檢查日 2026-11-28）門檻可行性 + 歷史吸收濃度（全部由資料算出）。"""
import collections
import json
import os
import statistics

DAYS = ['202611%02d' % d for d in range(9, 27)]
SUF = {}
for d in DAYS:
    for s in ['', '_re2', '_re']:
        p = f'memory/ptcgp_meta_{d}_std_comb{s}.json'
        if os.path.exists(p):
            SUF[d] = s
            break


def agg(day):
    j = json.load(open(f'memory/ptcgp_meta_{day}_std_comb{SUF[day]}.json', encoding='utf-8'))
    out = collections.defaultdict(lambda: {'share': 0.0, 'decks': 0, 'n': 0, 'w': 0})
    for r in j['rows']:
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
    return j['header'], res


HIST = {}
HEAD = {}
TOTD = {}
for d in DAYS:
    HEAD[d], rows = agg(d)
    HIST[d] = {r['name']: r for r in rows}
    TOTD[d] = sum(r['decks'] for r in rows)

T0 = TOTD['20261126']
print(f"今日總副牌 T0={T0}  昨日={TOTD['20261125']}  ΔT={T0-TOTD['20261125']:+d}")
ENV_N = sum(r['n'] for r in HIST['20261126'].values() if r['name'] != '__tot__')
ENV_W = sum(r['w'] for r in HIST['20261126'].values() if r['name'] != '__tot__')
print(f"環境 N={ENV_N} AWR {(ENV_W+12)/(ENV_N+25)*100:.4f}%")

# K
ks = [r['share'] / (r['decks'] / T0 * 100) for r in HIST['20261126'].values()
      if r['name'] != '__tot__' and r['n'] >= 200 and r['decks'] > 0]
K = statistics.median(ks)
print(f"K={K:.4f}（{len(ks)} 支可比）")

# 檢查日 11-28 增量（Thu→Fri→Sat，兩日）
import datetime
byday = {}
for d in DAYS:
    byday[d] = (HEAD[d]['matches'], TOTD[d])


def wd_pairs(a, b):
    """回傳所有 weekday(a)->weekday(b) 的差值"""
    out = []
    for i in range(1, len(DAYS)):
        p, c = DAYS[i - 1], DAYS[i]
        dt = datetime.date(int(c[:4]), int(c[4:6]), int(c[6:8]))
        pdt = datetime.date.fromordinal(dt.toordinal() - 1)
        if dt.weekday() == b and pdt.weekday() == a:
            out.append((c, byday[c][0] - byday[p][0], byday[c][1] - byday[p][1]))
    return out


tf = wd_pairs(3, 4)   # Thu->Fri
fs = wd_pairs(4, 5)   # Fri->Sat
print('\nThu→Fri:', tf)
print('Fri→Sat:', fs)
dm = statistics.median([x[1] for x in tf]) + statistics.median([x[1] for x in fs])
dd = statistics.median([x[2] for x in tf]) + statistics.median([x[2] for x in fs])
print(f"兩日合計估計：對局 {dm:+.0f}  副牌 {dd:+.0f}")
print(f"  區間（各自 min/max 組合）對局 {min(x[1] for x in tf)+min(x[1] for x in fs):+.0f} ~ {max(x[1] for x in tf)+max(x[1] for x in fs):+.0f}")
print(f"  區間 副牌 {min(x[2] for x in tf)+min(x[2] for x in fs):+.0f} ~ {max(x[2] for x in tf)+max(x[2] for x in fs):+.0f}")
T1 = T0 + dd
print(f"T1 = {T0} + {dd:+.0f} = {T1}")


def series(name):
    """回傳該牌組的 (share, awr, decks) 歷史與單日吸收濃度"""
    sh, aw, dk, conc = [], [], [], []
    for i in range(1, len(DAYS)):
        p, c = DAYS[i - 1], DAYS[i]
        rb, ra = HIST[c].get(name), HIST[p].get(name)
        if not rb or not ra:
            continue
        dT = TOTD[c] - TOTD[p]
        sh.append((c, rb['share'], rb['awr'], rb['n'], rb['decks']))
        aw.append((c, rb['awr']))
        dk.append((c, rb['decks']))
        if dT > 0:
            conc.append((c, (rb['decks'] - ra['decks']) / dT * 100, rb['decks'] - ra['decks']))
    return sh, conc


def model(name, thr, kind='share', up=True):
    r = HIST['20261126'].get(name)
    if not r:
        print(f'!! {name} 不存在')
        return
    sh, conc = series(name)
    pos = [x[1] for x in conc if x[1] > 0]
    med = statistics.median(pos) if pos else 0
    dmax = max((x[2] for x in conc), default=0)
    print(f"\n== {name}  現值 份額 {r['share']:.4f}%／AWR {r['awr']:.4f}%／副 {r['decks']}／N {r['n']}")
    print(f"   歷史單日最大吸收 {dmax:+d} 副   歷史正吸收濃度中位 {med:.2f}%")
    print(f"   近 8 日份額: " + ' → '.join(f"{x[1]:.4f}" for x in sh[-8:]))
    print(f"   近 8 日 AWR:  " + ' → '.join(f"{x[2]:.4f}" for x in sh[-8:]))
    print(f"   近 8 日吸收濃度(%): " + ' → '.join(f"{x[1]:.2f}" for x in conc[-8:]))
    if kind == 'share':
        dist = abs(thr - r['share'])
        print(f"   門檻 {thr:.4f}%  距離 {dist:.4f}pt")
        for lab, dt_ in [('保守', min(x[2] for x in tf) + min(x[2] for x in fs)),
                         ('中央', dd),
                         ('積極', max(x[2] for x in tf) + max(x[2] for x in fs))]:
            TT = T0 + dt_
            D1 = thr / 100 / K * TT
            dD = D1 - r['decks']
            cn_ = dD / dt_ * 100 if dt_ else 0
            zero = K * r['decks'] / TT * 100
            mx = K * (r['decks'] + 2 * dmax) / TT * 100
            print(f"   [{lab}] ΔT={dt_:+.0f} T1={TT:.0f} 需吸收 {dD:+.1f} 副  濃度 {cn_:5.2f}%  r={cn_/med if med else 0:.2f}"
                  f" | 零吸收 {zero:.4f}% | 最大吸收(+{dmax}×2) {mx:.4f}%")
    else:
        dist = abs(thr - r['awr'])
        print(f"   AWR 門檻 {thr:.4f}%  距離 {dist:.4f}pt")
        band = [x[2] for x in sh[-5:]]
        print(f"   近 5 日 AWR 帶 {min(band):.4f}~{max(band):.4f}%  半寬 {(max(band)-min(band))/2:.4f}pt")
        for lab, dm_ in [('保守', min(x[1] for x in tf) + min(x[1] for x in fs)),
                         ('中央', dm),
                         ('積極', max(x[1] for x in tf) + max(x[1] for x in fs))]:
            N1 = r['n'] + dm_ * (r['n'] / ENV_N)
            needW = thr / 100 * (N1 + 25) - 12
            print(f"   [{lab}] Δ對局 {dm_:+.0f} N1≈{N1:.0f}  需原始勝率 {needW/N1*100:.2f}%（今日 {r['raw']:.2f}%，需 {needW/N1*100-r['raw']:+.2f}pt）")


if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        kind, name, thr = line.split('|')
        model(name.strip(), float(thr), kind.strip())
