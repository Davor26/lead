import re, subprocess, json, sys, urllib.parse
from pathlib import Path
P = Path(__file__).resolve().parents[1]
out = P/'artifacts/search/mixkit_index.json'
idx = json.load(open(out)) if out.exists() else {}
for q in sys.argv[1:]:
    slugq = q.replace(' ', '-')
    for page in (1, 2):
        u = f'https://mixkit.co/free-stock-video/discover/{slugq}/' + (f'?page={page}' if page > 1 else '')
        h = subprocess.run(['curl','-sL','-m','30','-A','Mozilla/5.0',u],capture_output=True,text=True).stdout
        items = sorted(set(re.findall(r'/free-stock-video/([a-z0-9-]+)-(\d{3,6})/', h)))
        for s, i in items:
            idx.setdefault(i, {'title': s.replace('-', ' '), 'page_url': f'https://mixkit.co/free-stock-video/{s}-{i}/', 'queries': []})
            if q not in idx[i]['queries']: idx[i]['queries'].append(q)
        if not items: break
json.dump(idx, open(out,'w'), indent=0)
for q in sys.argv[1:]:
    print('##', q)
    for i, v in idx.items():
        if q in v['queries']: print(' ', i, v['title'])
