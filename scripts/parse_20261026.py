import re,json,sys
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
        out.append({'name':name,'slug':slug,'share':round(share*100,4),'w':w,'l':t,'d':los,'n':tot,'awr':awr})
    return out
branch=parse('/tmp/meta_20261026.html')
comb=parse('/tmp/meta_20261026_comb.html')
json.dump(branch,open('memory/ptcgp_meta_20261026.json','w'),ensure_ascii=False,indent=1)
json.dump(comb,open('memory/ptcgp_meta_20261026_comb.json','w'),ensure_ascii=False,indent=1)
print('branch',len(branch),'comb',len(comb))
print(branch[0])
