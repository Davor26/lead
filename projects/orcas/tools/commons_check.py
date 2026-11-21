import re, subprocess, json, sys, time, html, urllib.parse
from pathlib import Path
P = Path(__file__).resolve().parents[1]
out = P/'artifacts/search/commons_meta.json'
meta = json.load(open(out)) if out.exists() else {}
UA = 'NaturexploreDocBot/1.0 (documentary research; github.com/Davor26/lead)'
def field(h, lab):
    i = h.find('>'+lab+'<')
    if i < 0: return ''
    s = re.sub(r'<[^>]+>', ' ', h[i+len(lab)+2:i+1500]); s = re.sub(r'\s+', ' ', html.unescape(s)).strip()
    return re.split(r' (Author|Source|Date|Licensing|Permission|Camera location|Other versions) ', s)[0][:200]
for t in sys.argv[1:]:
    if t in meta and meta[t].get('v') == 2: continue
    u = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(t)
    h = subprocess.run(['curl','-sL','-m','40','-A',UA,u],capture_output=True,text=True).stdout
    if len(h) < 20000: print('FAILED', t, len(h)); time.sleep(5); continue
    lic = sorted(set(m.upper().replace('/', ' ').strip() for m in re.findall(r'creativecommons\.org/licenses/((?:by|by-sa|by-nc[a-z-]*)/[0-9.]+)', h)))
    lic = ['CC ' + l for l in lic]
    if re.search(r'public domain|PD-USGov|PD-self|PD-old', h, re.I) and re.search(r'licensetpl|This file is in the public domain|is in the public domain', h): lic.append('Public domain')
    tr = sorted(set(re.findall(r'https://upload\.wikimedia\.org/wikipedia/commons/transcoded/[^"\s<>]+?\.(\d{3,4})p\.(?:vp9\.webm|webm)', h)), key=int)
    best = None
    if tr:
        top = tr[-1]
        best = re.search(r'https://upload\.wikimedia\.org/wikipedia/commons/transcoded/[^"\s<>]+?\.' + top + r'p\.(?:vp9\.webm|webm)', h).group(0)
    orig = re.search(r'https://upload\.wikimedia\.org/wikipedia/commons/[0-9a-f]/[0-9a-f]{2}/[^"\'\s<>]+\.(?:webm|ogv|mpg|mpeg)', h)
    meta[t] = {'v': 2, 'page_url': u, 'licence': lic, 'transcodes': tr, 'best': best, 'orig': orig.group(0) if orig else None,
               'author': field(h, 'Author'), 'source': field(h, 'Source'), 'description': field(h, 'Description')}
    print(t[5:70], '|', lic, '|', tr[-1:] , '|', meta[t]['author'][:40], flush=True)
    json.dump(meta, open(out,'w'), indent=1)
    time.sleep(1.5)
