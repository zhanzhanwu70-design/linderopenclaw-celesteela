import re,json
def parse(path):
    h=open(path).read()
    out=[]
    for m in re.finditer(r'<tr[^>]+data-share="([^"]+)"[^>]*data-winrate="([^"]+)"[^>]*>(.*?)</tr>',h,re.DOTALL):
        share=float(m.group(1)); row=m.group(3)
        tds=re.findall(r'<td[^>]*>(.*?)</td>',row,re.DOTALL)
        if len(tds)<6: continue
        nm=re.search(r'<a href="/decks/([^"?]+)[^"]*"[^>]*>([^<]+)</a>',tds[2])
        if not nm: continue
        slug,name=nm.group(1),nm.group(2).strip()
        rec=re.sub(r'<[^>]+>','',tds[5]).strip()
        parts=[int(x) for x in re.findall(r'\d+',rec)] if '-' in rec else [0,0,0]
        w,los,t=parts[0],parts[1],parts[2]
        tot=w+los+t
        awr=round((w+12)/(tot+25)*100,2) if tot else 0
        out.append({'name':name,'slug':slug,'share':round(share*100,4),'w':w,'l':los,'d':t,'n':tot,'awr':awr})
    return out
for src,dst in [('memory/ptcgp_raw_20261031_b4a.html','memory/ptcgp_meta_20261031_b4a.json'),
                ('memory/ptcgp_raw_20261031_b4a_comb.html','memory/ptcgp_meta_20261031_b4a_comb.json'),
                ('memory/ptcgp_raw_20261031_c1_comb.html','memory/ptcgp_meta_20261031_c1_comb.json'),
                ('memory/ptcgp_raw_20261030.html','memory/ptcgp_meta_20261031_c1.json')]:
    d=parse(src); json.dump(d,open(dst,'w'),ensure_ascii=False,indent=1); print(dst,len(d))
