"""credits.txt: one line per clip actually used in the edit (provider | title | URL | licence)."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1]
plan = json.load(open(P/'artifacts/plan.json'))
noaa = json.load(open(P/'assets/footage/noaa_meta.json'))
mk = json.load(open(P/'assets/footage/mixkit_meta.json'))
wm = json.load(open(P/'assets/footage/commons_meta.json'))
used = []
for n in sorted(plan, key=int):
    for s in plan[n]['shots']:
        srcs = [s['fx']['left'][0], s['fx']['right'][0]] if s['src'] == 'SPLIT' else [s['src']]
        for x in srcs:
            if x not in used and not x.startswith(('G:', 'BLACK')): used.append(x)
used.append('mk_48090_thumb')  # thumbnail background frame
lines = []
for k in used:
    if k.startswith('noaa_'):
        v = noaa[k[5:]]
        lines.append(f"NOAA Fisheries | {v['title'].split(' - ')[0]} | {v['page_url']} | Public domain (U.S. Government work; credit: NOAA Fisheries)")
    elif k.startswith('mk_'):
        kk = k.replace('_thumb', '')
        v = mk[kk + '.mp4']; note = ' (thumbnail background)' if k.endswith('_thumb') else ''
        lines.append(f"Mixkit | {v['title'].capitalize()}{note} | {v['page_url']} | Mixkit Stock Video Free License")
    elif k.startswith('wm_'):
        v = wm[k + '.webm']
        lines.append(f"Wikimedia Commons | {v['title']} — {v['author'] or 'see file page'} | {v['page_url']} | {v['licence']}")
music = json.load(open(P/'assets/music/music_meta_all.json'))
mp = json.load(open(P/'artifacts/music_plan.json'))
used_m = []
for seg in mp['segments']:
    if seg[0] not in used_m: used_m.append(seg[0])
out = ['WHY ORCAS DON\'T KILL HUMANS — Naturexplore', '', 'FOOTAGE (provider | title | URL | licence)'] + lines
out += ['', 'MUSIC'] + [f"{music[m]['provider']} | \"{music[m]['title']}\" — {music[m]['author']} | {music[m]['page_url']} | {music[m]['licence']}" for m in used_m]
out += ['', 'NARRATION', 'Piper TTS (rhasspy/piper, MIT) | voice en_GB-cori-high | https://huggingface.co/rhasspy/piper-voices | trained on LibriVox recordings (public domain)',
        '', 'MAP DATA', 'Natural Earth via world-atlas | land 50m / 10m | https://github.com/topojson/world-atlas | Public domain',
        '', 'GRAPHICS', 'Diagrams, maps, text cards and silhouettes: original artwork made for this film (Naturexplore).', '']
(P.parents[1]/'output/orcas/credits.txt').write_text('\n'.join(out), encoding='utf-8')
print(len(lines), 'clips;', len(used_m), 'music tracks')
