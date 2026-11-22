import re, subprocess, json, html, sys
H = ['-A', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36', '-H', 'Accept-Language: en-US,en;q=0.9']
meta = {}
for slug in sys.argv[1:]:
    u = 'https://www.usgs.gov/media/videos/' + slug
    h = subprocess.run(['curl', '-sL', '-m', '40'] + H + [u], capture_output=True, text=True).stdout
    mp4 = sorted(set(re.findall(r'https?://[^"\'\s<>]+\.mp4', h)))
    yt = sorted(set(re.findall(r'youtube(?:-nocookie)?\.com/embed/([\w-]{11})', h)))
    title = re.search(r'<title>([^<|]+)', h)
    desc = re.search(r'<meta name="description" content="([^"]*)"', h)
    meta[slug] = {'page_url': u, 'title': html.unescape(title.group(1)).strip() if title else slug, 'mp4': mp4, 'youtube': yt,
                  'description': html.unescape(desc.group(1))[:300] if desc else '', 'pd': 'public domain' in h.lower()}
    print(slug, '| mp4:', mp4[:2], '| yt:', yt, '| PD-mentioned:', meta[slug]['pd'])
json.dump(meta, open('artifacts/search/usgs_meta.json', 'w'), indent=1)
