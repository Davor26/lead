"""Build: plan (durations, cut points, reuse audit, graphics jobs) and render beat clips / chapter chunks.
usage: python3 tools/build.py plan | gfxjobs | shots [beat...] | beats | chunks"""
import json, sys, subprocess, os, math
from pathlib import Path
from collections import defaultdict
P = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(P/'tools'))
from edl import EDL, OVERLAYS, CHAPTER_CARDS
FPS = 30
TL = json.load(open(P/'artifacts/timeline.json'))
BEATS = {b['beat']: b for b in TL['beats']}
RAW = P/'assets/footage/raw'
NORM = P/'assets/footage/norm'; NORM.mkdir(parents=True, exist_ok=True)
GOUT = P/'graphics/out'; GOUT.mkdir(parents=True, exist_ok=True)
BOUT = P/'renders/beats'; BOUT.mkdir(parents=True, exist_ok=True)
F = lambda t: int(round(t * FPS))

def srcfile(k):
    for ext in ('.mp4', '.webm'):
        if (RAW/(k+ext)).exists(): return RAW/(k+ext)
    raise FileNotFoundError(k)
def scenes(k):
    f = P/'artifacts/scenes'/(k+'.txt')
    if not f.exists(): return None, []
    L = f.read_text().split('\n'); dur = float(L[0].split()[1])
    return dur, [float(x) for x in L[1:] if x.strip()]

def beat_frames(b):
    """(visible frames, black frames) for a beat; frame-accurate on the global timeline."""
    st = F(b['visual_start']); en = F(b['segment_end'])
    vis_end = F(b['black_start']) if b['black_start'] else en
    return vis_end - st, en - vis_end

def plan():
    out = {}
    for n, b in BEATS.items():
        vis, blk = beat_frames(b)
        shots = EDL[n]
        fixed = sum(F(s[3]['d']) for s in shots if 'd' in s[3])
        wsum = sum(s[2] for s in shots if 'd' not in s[3])
        rest = vis - fixed; acc = 0; lst = []
        flex = [i for i, s in enumerate(shots) if 'd' not in s[3]]
        for i, (src, tin, w, fx) in enumerate(shots):
            if 'd' in fx: nf = F(fx['d'])
            elif i == flex[-1]: nf = rest - acc
            else: nf = int(round(rest * w / wsum)); acc += nf
            lst.append({'src': src, 'in': tin, 'frames': nf, 'fx': fx})
        # adjust in-points to stay inside one camera shot
        for s in lst:
            if s['src'].startswith(('G:', 'BLACK', 'SPLIT', 'IMG:')): continue
            dur, cuts = scenes(s['src'])
            need = s['frames'] / FPS / s['fx'].get('slow', 1.0)
            if dur is None: continue
            tin = min(s['in'], max(0, dur - need - 0.2))
            bounds = [0.0] + cuts + [dur]
            for a, z in zip(bounds, bounds[1:]):
                if a <= tin < z:
                    if tin + need <= z - 0.05: break
                    if z - a - 0.1 >= need:            # fits inside this shot: shift the window
                        tin = max(a + 0.05, z - 0.05 - need)
                    else:                               # shot too short: slow it (max 1.6x) or accept the cut
                        avail = z - tin - 0.05
                        if avail > 0 and need / avail <= 1.6 / s['fx'].get('slow', 1.0):
                            s['fx'] = dict(s['fx'], slow=round(s['fx'].get('slow', 1.0) * need / avail + 0.01, 3))
                            need = s['frames'] / FPS / s['fx']['slow']
                        else:
                            s['warn'] = f'crosses cut at {z:.2f}'
                    break
            s['in'] = round(tin, 3); s['src_len'] = round(need, 3)
        out[n] = {'vis': vis, 'black': blk, 'shots': lst, 'overlay': OVERLAYS.get(n)}
    json.dump(out, open(P/'artifacts/plan.json', 'w'), indent=1)
    # reuse audit: every source second may appear at most twice
    use = defaultdict(list)
    for n, bp in out.items():
        for s in bp['shots']:
            if s['src'].startswith('IMG:'): use[('IMG', s['src'])].append((n, 0, 1)); continue
            if s['src'].startswith(('G:', 'BLACK')):
                if s['src'].startswith('G:'): use[(s['src'], json.dumps(s['fx'].get('p', {})))].append((n, 0, 1))
                continue
            parts = [s['fx']['left'], s['fx']['right']] if s['src'] == 'SPLIT' else [(s['src'], s['in'])]
            for src, tin in parts:
                ln = s.get('src_len', s['frames'] / FPS)
                use[src].append((n, tin, tin + ln))
    bad = []
    for k, iv in use.items():
        if isinstance(k, tuple):
            if len(iv) > 2: bad.append((k, iv))
            continue
        pts = sorted({x for a in iv for x in a[1:]})
        for a, z in zip(pts, pts[1:]):
            m = (a + z) / 2; c = [i for i in iv if i[1] <= m < i[2]]
            if len(c) > 2: bad.append((k, c)); break
    warns = [(n, s['src'], s['warn']) for n, bp in out.items() for s in bp['shots'] if 'warn' in s]
    print('reuse violations:', bad if bad else 'none'); print('cut warnings:', warns if warns else 'none')
    print('sources:', len([k for k in use if not isinstance(k, tuple)]), 'graphics uses:', sum(len(v) for k, v in use.items() if isinstance(k, tuple)))
    return out

def gfx_jobs():
    pl = json.load(open(P/'artifacts/plan.json')); jobs = []; seen = set()
    for n, bp in pl.items():
        for k, s in enumerate(bp['shots']):
            if not s['src'].startswith('G:'): continue
            if s['fx'].get('reuse'): continue
            name = s['src'][2:]; d = s['frames'] / FPS
            if name == 'carving': d += 2.0     # tail used for the dissolve into beat 79
            jobs.append({'name': name, 'dur': round(d, 4), 'params': s['fx'].get('p', {}), 'out': str(GOUT/f'b{int(n):03d}_{name}.mp4')})
        if bp['overlay']:
            name, p, off = bp['overlay']
            jobs.append({'name': name, 'dur': round(bp['vis'] / FPS - off, 4), 'params': p, 'out': str(GOUT/f'b{int(n):03d}_ov_{name}.mov')})
    for c in TL['chapters']:
        if c['type'] != 'card': continue
        ci = c['chapter_index']; kick, title = CHAPTER_CARDS[ci]
        kick = f'CHAPTER {kick}' if kick.isdigit() else kick
        jobs.append({'name': 'chapter', 'dur': round((F(c['end']) - F(c['start'])) / FPS, 4), 'params': {'kicker': kick, 'title': title}, 'out': str(GOUT/f'card_{ci:02d}.mp4')})
    json.dump(jobs, open(P/'graphics/jobs.json', 'w'), indent=1)
    # split into 3 balanced lists for parallel rendering
    jobs.sort(key=lambda j: -j['dur']); parts = [[], [], []]; tot = [0, 0, 0]
    for j in jobs: i = tot.index(min(tot)); parts[i].append(j); tot[i] += j['dur']
    for i, p in enumerate(parts): json.dump(p, open(P/f'graphics/jobs_{i}.json', 'w'))
    print(len(jobs), 'graphics jobs', [round(x) for x in tot])

GRADE = {
 'cool': 'eq=contrast=1.04:saturation=0.85,colorbalance=bs=0.05:bm=0.03',
 'dark': 'eq=brightness=-0.07:contrast=1.08:saturation=0.8,colorbalance=bs=0.06:bm=0.04',
 'night': 'eq=brightness=-0.2:contrast=1.1:saturation=0.45,colorbalance=bs=0.12:bm=0.08:rs=-0.05',
 'dusk': 'colorbalance=rs=0.14:gs=0.03:bs=-0.12:rm=0.08:bm=-0.06,eq=saturation=1.1:brightness=-0.04',
 'grey': 'eq=saturation=0.55:contrast=0.98',
 'warm': 'colorbalance=rs=0.06:bs=-0.05:rm=0.04,eq=saturation=1.05',
}
ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '30', '-g', '60', '-an']

def vchain(s, nf, w=1920, h=1080):
    fx = s['fx']; z = fx.get('zoom', 1.0); slow = fx.get('slow', 1.0)
    c = [f'setpts=(PTS-STARTPTS)*{slow}', 'fps=30']
    if fx.get('box'):
        bx, by, bw, bh = fx['box']; c.append(f'crop=iw*{bw}:ih*{bh}:iw*{bx}:ih*{by}')
    c += [f'scale={int(w*z)}:{int(h*z)}:force_original_aspect_ratio=increase', f'crop={w}:{h}']
    if fx.get('push'):
        D = nf / FPS
        c += [f"scale=w='{w}*(1+0.06*t/{D:.3f})':h=-2:eval=frame", f'crop={w}:{h}']
    if fx.get('grade'): c.append(GRADE[fx['grade']])
    c += ['setsar=1', 'format=yuv420p']
    return ','.join(c)

def kenburns(img, nf, kb, out):
    from PIL import Image
    im = Image.open(img).convert('RGB'); iw, ih = im.size
    (c0x, c0y, w0), (c1x, c1y, w1) = kb
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30', '-i', '-'] + ENC + [str(out)], stdin=subprocess.PIPE)
    for f in range(nf):
        u = f / max(1, nf - 1); u = u * u * (3 - 2 * u)
        cx, cy, wf = c0x + (c1x - c0x) * u, c0y + (c1y - c0y) * u, w0 + (w1 - w0) * u
        bw = iw * wf; bh = bw * 9 / 16
        x0 = min(max(cx * iw - bw / 2, 0), iw - bw); y0 = min(max(cy * ih - bh / 2, 0), ih - bh)
        sc = bw / 1920
        fr = im.transform((1920, 1080), Image.AFFINE, (sc, 0, x0, 0, sc, y0), resample=Image.BICUBIC)
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()

def render_shot(n, k, s):
    out = NORM/f'b{int(n):03d}_{k}.mp4'
    if out.exists(): return out
    nf = s['frames']
    if s['src'].startswith('IMG:'):
        kenburns(P/'assets/ai'/s['src'][4:], nf, s['fx'].get('kb', ((0.5, 0.5, 1.0), (0.5, 0.5, 0.88))), out)
        return out
    if s['src'] == 'BLACK':
        cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'color=c=black:s=1920x1080:r=30', '-frames:v', str(nf)] + ENC + [str(out)]
    elif s['src'].startswith('G:'):
        name = s['src'][2:]
        rn = s['fx'].get('reuse', n)
        g = GOUT/f'b{int(rn):03d}_{name}.mp4'
        cmd = ['ffmpeg', '-y', '-v', 'error', '-i', str(g), '-vf', 'fps=30,format=yuv420p', '-frames:v', str(nf)] + ENC + [str(out)]
    elif s['src'] == 'SPLIT':
        (ls, li), (rs, ri) = s['fx']['left'], s['fx']['right']
        l = dict(fx={}); r = dict(fx={'grade': s['fx'].get('rgrade')} if s['fx'].get('rgrade') else {})
        fc = (f"[0:v]{vchain(l, nf, 956, 1080)}[a];[1:v]{vchain(r, nf, 956, 1080)}[b];"
              f"color=c=black:s=1920x1080:r=30[bg];[bg][a]overlay=0:0:shortest=1[x];[x][b]overlay=964:0:shortest=1,format=yuv420p")
        cmd = ['ffmpeg', '-y', '-v', 'error', '-ss', str(li), '-i', str(srcfile(ls)), '-ss', str(ri), '-i', str(srcfile(rs)),
               '-filter_complex', fc, '-frames:v', str(nf)] + ENC + [str(out)]
    else:
        cmd = ['ffmpeg', '-y', '-v', 'error', '-ss', str(s['in']), '-i', str(srcfile(s['src'])), '-vf', vchain(s, nf), '-frames:v', str(nf)] + ENC + [str(out)]
    subprocess.run(cmd, check=True)
    got = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', str(out)], capture_output=True, text=True).stdout.strip())
    if got != nf:  # source ran out: pad by holding the last frame
        tmp = out.with_suffix('.pad.mp4')
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(out), '-vf', f'tpad=stop_mode=clone:stop={nf}', '-frames:v', str(nf)] + ENC + [str(tmp)], check=True)
        os.replace(tmp, out); print(f'  padded b{n}_{k}: {got}->{nf}')
    return out

def render_beat(n):
    pl = json.load(open(P/'artifacts/plan.json'))[str(n)]
    out = BOUT/f'beat_{n:03d}.mp4'
    if out.exists(): return out
    files = [render_shot(n, k, s) for k, s in enumerate(pl['shots'])]
    lst = BOUT/f'beat_{n:03d}.txt'; lst.write_text(''.join(f"file '{f}'\n" for f in files))
    vis, blk = pl['vis'], pl['black']
    prev = BEATS.get(n - 1)
    fade_in = (n == 1) or (prev and prev['pause']) or (prev and prev['chapter_index'] != BEATS[n]['chapter_index'])
    nxt = BEATS.get(n + 1)
    fade_out = blk > 0 or (nxt and nxt['chapter_index'] != BEATS[n]['chapter_index']) or n == 98
    inputs = ['-f', 'concat', '-safe', '0', '-i', str(lst)]
    fc = '[0:v]setpts=PTS-STARTPTS'
    extra = []
    if pl['overlay']:
        name, p, off = pl['overlay']
        extra += ['-itsoffset', str(off), '-i', str(GOUT/f'b{n:03d}_ov_{name}.mov')]
        fc += f"[base];[1:v]format=rgba,fade=t=out:st={vis/FPS - off - 0.6:.3f}:d=0.5:alpha=1[ov];[base][ov]overlay=0:0:eof_action=pass"
    fd = 0.35
    if fade_in: fc += f',fade=t=in:st=0:d={fd}'
    if fade_out: fc += f',fade=t=out:st={vis/FPS - fd:.3f}:d={fd}'
    if blk: fc += f',tpad=stop={blk}:color=black'
    fc += ',format=yuv420p'
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + inputs + extra + ['-filter_complex', fc, '-frames:v', str(vis + blk)] + ENC + [str(out)], check=True)
    return out

def EDL_SHOT_DUR(n):
    pl = json.load(open(P/'artifacts/plan.json'))[str(n)]
    return pl['shots'][0]['frames'] / FPS

def render_card(ci):
    out = BOUT/f'card_{ci:02d}.mp4'
    if not out.exists():
        c = [c for c in TL['chapters'] if c['type'] == 'card' and c['chapter_index'] == ci][0]
        nf = F(c['end']) - F(c['start'])
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(GOUT/f'card_{ci:02d}.mp4'), '-vf', 'fps=30,format=yuv420p', '-frames:v', str(nf)] + ENC + [str(out)], check=True)
    return out

def chunks():
    """One chunk per chapter: [card] + beats; then a list for the final concat."""
    CH = P/'renders/chunks'; CH.mkdir(parents=True, exist_ok=True); allc = []
    for ci in range(1, 15):
        files = ([render_card(ci)] if ci > 1 else []) + [BOUT/f'beat_{n:03d}.mp4' for n in sorted(BEATS) if BEATS[n]['chapter_index'] == ci]
        lst = CH/f'chunk_{ci:02d}.txt'; lst.write_text(''.join(f"file '{f}'\n" for f in files))
        out = CH/f'chunk_{ci:02d}.mp4'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(out)], check=True)
        allc.append(out); print('chunk', ci, out)
    (CH/'all.txt').write_text(''.join(f"file '{f}'\n" for f in allc))

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'plan': plan()
    elif cmd == 'gfxjobs': gfx_jobs()
    elif cmd == 'beats':
        todo = [int(x) for x in sys.argv[2:]] or sorted(BEATS)
        for n in todo:
            render_beat(n); print('beat', n, flush=True)
    elif cmd == 'cards':
        for ci in range(2, 14): render_card(ci)
    elif cmd == 'chunks': chunks()
