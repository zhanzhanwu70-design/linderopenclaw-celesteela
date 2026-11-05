import re, json

def parse(path):
    h = open(path).read()
    out = []
    for m in re.finditer(r'<tr[^>]+data-share="([^"]+)"[^>]*data-winrate="([^"]+)"[^>]*>(.*?)</tr>', h, re.DOTALL):
        share = float(m.group(1)); row = m.group(3)
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(tds) < 6: continue
        nm = re.search(r'<a href="/decks/([^"?]+)[^"]*"[^>]*>([^<]+)</a>', tds[2])
        if not nm: continue
        slug, name = nm.group(1), nm.group(2).strip()
        rec = re.sub(r'<[^>]+>', '', tds[5]).strip()
        parts = [int(x) for x in re.findall(r'\d+', rec)] if '-' in rec else [0, 0, 0]
        w, los, t = parts[0], parts[1], parts[2]
        tot = w + los + t
        awr = round((w + 12) / (tot + 25) * 100, 2) if tot else 0
        raw = round(w / tot * 100, 2) if tot else 0
        out.append({'name': name, 'slug': slug, 'share': round(share * 100, 4),
                    'w': w, 'l': los, 'd': t, 'n': tot, 'awr': awr, 'raw_wr': raw})
    return out

def header(path):
    h = open(path).read()
    m = re.search(r'<p>(\d+)\s+tournaments,\s+(\d+)\s+players,.*?(\d+)\s+matches', h, re.DOTALL)
    if m: return {'tournaments': int(m.group(1)), 'players': int(m.group(2)), 'matches': int(m.group(3))}
    return {}

for src, dst in [
    ('memory/ptcgp_raw_20261105_std.html', 'memory/ptcgp_meta_20261105_std.json'),
    ('memory/ptcgp_raw_20261105_std_comb.html', 'memory/ptcgp_meta_20261105_std_comb.json'),
    ('memory/ptcgp_raw_20261105_C1.html', 'memory/ptcgp_meta_20261105_C1.json'),
    ('memory/ptcgp_raw_20261105_C1_comb.html', 'memory/ptcgp_meta_20261105_C1_comb.json'),
    ('memory/ptcgp_raw_20261104_std.html', 'memory/ptcgp_meta_20261104_std_re.json'),
    ('memory/ptcgp_raw_20261104_std_comb.html', 'memory/ptcgp_meta_20261104_std_comb_re.json'),
    ('memory/ptcgp_raw_20261103_std.html', 'memory/ptcgp_meta_20261103_std_re.json'),
    ('memory/ptcgp_raw_20261103_std_comb.html', 'memory/ptcgp_meta_20261103_std_comb_re.json'),
    ('memory/ptcgp_raw_20261102_std.html', 'memory/ptcgp_meta_20261102_std_re.json'),
    ('memory/ptcgp_raw_20261102_std_comb.html', 'memory/ptcgp_meta_20261102_std_comb_re.json'),
    ('memory/ptcgp_raw_20261105_B4a.html', 'memory/ptcgp_meta_20261105_B4a.json'),
]:
    d = parse(src)
    hd = header(src)
    json.dump({'header': hd, 'rows': d}, open(dst, 'w'), ensure_ascii=False, indent=1)
    print(dst, len(d), 'rows  total_share=%.2f' % sum(x['share'] for x in d), hd)
