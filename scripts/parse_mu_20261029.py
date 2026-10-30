import re,glob,json
M={}
for f in sorted(glob.glob('memory/matchups_20261029/*.html')):
    h=open(f).read()
    t=re.search(r'<title>([^<]*?) - B4a Standard - Matchups',h)
    if not t: continue
    me=t.group(1).strip()
    d={}
    for tr in re.findall(r'<tr ([^>]*)>',h):
        nm=re.search(r'data-name="([^"]+)"',tr); mm=re.search(r'data-matches="(\d+)"',tr); wr=re.search(r'data-winrate="([\d.]+)"',tr)
        if nm and mm and wr:
            m=int(mm.group(1)); w=round(float(wr.group(1))*100,1)
            # keep the row with the largest match count for each opponent
            if nm.group(1) not in d or m>d[nm.group(1)][1]:
                d[nm.group(1)]=[w,m]
    M[me]=d
json.dump(M,open('memory/mu_matrix_20261029.json','w'),ensure_ascii=False,indent=1)
print('subjects',len(M))
