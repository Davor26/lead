import json, subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
idx = json.load(open(P/'artifacts/search/mixkit_index.json'))
log = P/'assets/footage/mixkit_meta.json'
meta = json.load(open(log)) if log.exists() else {}
for i in sys.argv[1:]:
    fn = f'mk_{i}.mp4'
    if fn in meta: continue
    out = P/'assets/footage/raw'/fn
    for res in ('1080', '720'):
        r = subprocess.run(['curl','-s','-m','300','-A','Mozilla/5.0','-e','https://mixkit.co/','-o',str(out),'-w','%{http_code}',
                            f'https://assets.mixkit.co/videos/{i}/{i}-{res}.mp4'],capture_output=True,text=True).stdout
        if r == '200': break
    v = idx.get(i, {})
    meta[fn] = {'provider': 'Mixkit', 'title': v.get('title', i), 'page_url': v.get('page_url', f'https://mixkit.co/free-stock-video/{i}/'),
                'download_url': f'https://assets.mixkit.co/videos/{i}/{i}-{res}.mp4', 'resolution': res,
                'licence': 'Mixkit Stock Video Free License (free for commercial use, no attribution required)'}
    json.dump(meta, open(log,'w'), indent=1)
    print(r, res, fn, v.get('title','')[:50], flush=True)
