import re, json, subprocess, html, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
idx = json.load(open(P/'artifacts/search/noaa_index.json'))
want = sys.argv[1:]
log = P/'assets/footage/noaa_meta.json'
meta = json.load(open(log)) if log.exists() else {}
for vid, link in idx.items():
    slug = html.unescape(link).split('?')[0].split('/')[-1]
    if not any(w == slug for w in want) or vid in meta: continue
    url = 'https://videos.fisheries.noaa.gov' + html.unescape(link).split('?')[0]
    h = subprocess.run(['curl','-sL','-m','40','-A','Mozilla/5.0',url],capture_output=True,text=True).stdout
    mp4s = [html.unescape(m) for m in re.findall(r'https://fastly-signed[^"\' ]+\.mp4[^"\' ]*', h)]
    desc = re.search(r'<meta name="description" content="([^"]*)"', h)
    title = re.search(r'<title>([^<]*)', h)
    if not mp4s: print('NO MP4', slug); continue
    out = P/f'assets/footage/raw/noaa_{vid}.mp4'
    r = subprocess.run(['curl','-s','-m','600','-o',str(out),'-w','%{http_code}',mp4s[0]],capture_output=True,text=True).stdout
    meta[vid] = {'file': out.name, 'slug': slug, 'page_url': url, 'title': html.unescape(title.group(1)).strip() if title else slug,
                 'description': html.unescape(desc.group(1)) if desc else '', 'provider': 'NOAA Fisheries',
                 'licence': 'Public domain (U.S. federal government work, NOAA Fisheries)'}
    json.dump(meta, open(log,'w'), indent=1)
    print(r, slug, flush=True)
