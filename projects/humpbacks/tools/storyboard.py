import json, subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(P/'tools')); from build import srcfile
pl = json.load(open(P/'artifacts/plan.json')); D = P/'artifacts/story/src'; D.mkdir(parents=True, exist_ok=True)
tiles = []
for n in sorted(pl, key=int):
    for k, s in enumerate(pl[n]['shots']):
        if s['src'].startswith(('G:', 'BLACK', 'IMG:')): continue
        src, tin = (s['fx']['left'] if s['src'] == 'SPLIT' else (s['src'], s['in']))
        mid = tin + s.get('src_len', 3) / 2
        o = D/f'b{int(n):03d}_{k}.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{mid:.2f}', '-i', str(srcfile(src)), '-frames:v', '1', '-vf',
                        f"scale=320:180,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{n}.{k} {src[:12]}':x=3:y=3:fontsize=15:fontcolor=yellow:box=1:boxcolor=black", '-y', str(o)])
        tiles.append(o)
for i in range(0, len(tiles), 40):
    grp = tiles[i:i+40]
    while len(grp) < 40: grp.append(grp[-1])
    args = sum([['-i', str(t)] for t in grp], [])
    lay = '|'.join(f'{(j%8)*320}_{(j//8)*180}' for j in range(40))
    subprocess.run(['ffmpeg', '-v', 'error'] + args + ['-filter_complex', f'xstack=inputs=40:layout={lay}', '-y', str(P/f'artifacts/story/board_{i//40}.jpg')])
print(len(tiles))
