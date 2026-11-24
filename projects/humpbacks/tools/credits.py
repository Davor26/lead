"""credits.txt: one line per clip actually used (provider | title | URL | licence)."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1]
plan = json.load(open(P/'artifacts/plan.json'))
usgs = json.load(open(P/'assets/footage/usgs_meta.json'))
mk = json.load(open(P/'assets/footage/mixkit_meta.json'))
noaa = json.load(open('/home/user/lead/projects/orcas/assets/footage/noaa_meta.json'))
mk_orca = json.load(open('/home/user/lead/projects/orcas/assets/footage/mixkit_meta.json'))
used = []
for n in sorted(plan, key=int):
    for s in plan[n]['shots']:
        if s['src'] not in used and not s['src'].startswith(('G:', 'BLACK')): used.append(s['src'])
lines = []
for k in used:
    if k.startswith('IMG:'):
        lines.append(f"AI-generated image (muapi / Imagen 4 Fast), original for Naturexplore | {k[4:]} | — | Original work for Naturexplore")
    elif k.startswith('usgs_'):
        v = usgs[k + '.mp4']; lines.append(f"USGS | {v['title'].split(' | ')[0]} | {v['page_url']} | {v['licence']}")
    elif k.startswith('noaa_'):
        v = noaa[k[5:]]; lines.append(f"NOAA Fisheries | {v['title'].split(' - ')[0]} | {v['page_url']} | Public domain (U.S. Government work; credit: NOAA Fisheries)")
    elif k.startswith('mk_'):
        v = mk.get(k + '.mp4') or mk_orca.get(k + '.mp4')
        lines.append(f"Mixkit | {v['title'].capitalize()} | {v['page_url']} | Mixkit Stock Video Free License ({v.get('resolution', '1080')}p source)")
music = json.load(open(P/'assets/music/music_meta_all.json'))
mp = json.load(open(P/'artifacts/music_plan.json'))
used_m = []
for seg in mp['segments']:
    if seg[0] not in used_m: used_m.append(seg[0])
out = ["WHY POLAR BEARS THROW ROCKS AT WALRUSES — Naturexplore", '', 'FOOTAGE AND IMAGES (provider | title | URL | licence)'] + lines
out += ['', 'MUSIC'] + [f"{music[m]['provider']} | \"{music[m]['title']}\" — {music[m]['author']} | {music[m]['page_url']} | {music[m]['licence']}" for m in used_m]
out += ['', 'NARRATION', 'Piper TTS (rhasspy/piper, MIT) | voice en_GB-cori-high | https://huggingface.co/rhasspy/piper-voices | trained on LibriVox recordings (public domain)',
        '', 'MAP DATA', 'Natural Earth via world-atlas | land 50m / 10m | https://github.com/topojson/world-atlas | Public domain',
        '', 'GRAPHICS', 'Diagrams, maps, text cards and silhouettes: original artwork made for this film (Naturexplore).', '']
(P.parents[1]/'output/walrus/credits.txt').write_text('\n'.join(out), encoding='utf-8')
print(len(lines), 'visual sources;', len(used_m), 'music tracks')
