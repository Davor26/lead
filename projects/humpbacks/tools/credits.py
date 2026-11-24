"""credits.txt: one line per clip actually used (provider | title | URL | licence)."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1]
plan = json.load(open(P/'artifacts/plan.json'))
noaa = json.load(open(P/'assets/footage/noaa_meta.json'))
wm = json.load(open('/home/user/lead/projects/orcas/assets/footage/commons_meta.json'))
wm.update(json.load(open(P/'assets/footage/commons_meta.json')))
used = []
for n in sorted(plan, key=int):
    for s in plan[n]['shots']:
        if s['src'] not in used and not s['src'].startswith(('G:', 'BLACK')): used.append(s['src'])
lines = []
for k in used:
    if k.startswith('noaa_'):
        v = noaa[k[5:]]; lines.append(f"NOAA Fisheries | {v['title'].split(' - ')[0]} | {v['page_url']} | Public domain (U.S. Government work; credit: NOAA Fisheries)")
    elif k.startswith('wm_'):
        v = wm[k + '.webm']
        lines.append(f"Wikimedia Commons | {v['title']} — {v['author'].split(' Assessment')[0].strip() or 'see file page'} | {v['page_url']} | {v['licence']}")
music = json.load(open(P/'assets/music/music_meta_all.json'))
mp = json.load(open(P/'artifacts/music_plan.json'))
used_m = []
for seg in mp['segments']:
    if seg[0] not in used_m: used_m.append(seg[0])
out = ["WHY HUMPBACK WHALES SAVE OTHER ANIMALS FROM ORCAS — Naturexplore", '', 'FOOTAGE (provider | title | URL | licence)'] + lines
out += ['', 'MUSIC'] + [f"{music[m]['provider']} | \"{music[m]['title']}\" — {music[m]['author']} | {music[m]['page_url']} | {music[m]['licence']}" for m in used_m]
out += ['', 'NARRATION', 'Piper TTS (rhasspy/piper, MIT) | voice en_GB-cori-high | https://huggingface.co/rhasspy/piper-voices | trained on LibriVox recordings (public domain)',
        '', 'MAP DATA', 'Natural Earth via world-atlas | land 50m / 10m | https://github.com/topojson/world-atlas | Public domain',
        '', 'GRAPHICS', 'Diagrams, maps, text cards and silhouettes (including the rescue scenes): original artwork made for this film (Naturexplore).',
        '', 'SCIENCE', 'Pitman, R.L. et al. (2017). Humpback whales interfering when mammal-eating killer whales attack other species. Marine Mammal Science 33(1): 7–58.', '']
(P.parents[1]/'output/humpbacks/credits.txt').write_text('\n'.join(out), encoding='utf-8')
print(len(lines), 'visual sources;', len(used_m), 'music tracks')
