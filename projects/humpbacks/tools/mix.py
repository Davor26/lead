"""Audio: narration master + chapter music bed (ducked ~18 dB under the voice) -> final mix 48 kHz stereo."""
import json, subprocess, wave, re
import numpy as np
from pathlib import Path
P = Path(__file__).resolve().parents[1]
TL = json.load(open(P/'artifacts/timeline.json'))
SR = 48000
TOTAL = TL['total']
N = int(round(TOTAL * SR))
A = P/'assets/audio'; A.mkdir(exist_ok=True)

def decode(f, ss=0.0):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', str(f), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def lufs(x):
    """integrated loudness via ffmpeg ebur128 on a temp wav"""
    tmp = A/'_tmp.wav'; write(tmp, x)
    o = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(tmp), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])

def write(f, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(f), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())

# ---- narration master: chapter files placed at their timeline positions ----
narr = np.zeros((N, 2), np.float32)
for c in TL['chapters']:
    if c['type'] != 'chapter_audio': continue
    x = decode(P/c['file']); s = int(round(c['start'] * SR))
    narr[s:s + len(x)] += x[:max(0, N - s)]
g = 10 ** ((-16.0 - lufs(narr)) / 20); narr *= g
write(A/'narration_master.wav', narr)
print('narration normalised to -16 LUFS')

# ---- music bed ----
meta = json.load(open(P/'assets/music/music_meta.json'))
for i, v in json.load(open(P/'assets/music/mixkit/meta.json')).items():
    meta['mx_' + i] = {'file': f'assets/music/mixkit/mx_{i}.mp3', 'title': v['title'], 'author': v['artist'], 'page_url': f'https://assets.mixkit.co/music/{i}/{i}.mp3',
                       'licence': 'Mixkit Stock Music Free License', 'provider': 'Mixkit'}
json.dump(meta, open(P/'assets/music/music_meta_all.json', 'w'), indent=1)
have = {k for k, v in meta.items() if (P/v['file']).exists() and (P/v['file']).stat().st_size > 100000}
print('music available:', sorted(have))
B = {b['beat']: b for b in TL['beats']}
cards = {c['chapter_index']: c['start'] for c in TL['chapters'] if c['type'] == 'card'}
cstart = lambda ci: cards[ci] if ci in cards else 0.0
# chapter -> preferred tracks (first available wins); (track, offset seconds)
# chapter -> track. Tense under the paradox and the record; warm for the grandmothers and Tahlequah.
PLAN = {1: ['mx_188'], 2: ['mx_612'], 3: ['mx_565'], 4: ['mx_184'], 5: ['mx_188'], 6: ['mx_546'], 7: ['mx_682'], 8: ['mx_148'],
        9: ['mx_565'], 10: ['mx_546'], 11: ['mx_683'], 12: ['mx_614'], 13: ['mx_612'], 14: ['mx_184']}
OFFS = {('mx_188', 5): 60.0, ('mx_565', 9): 150.0, ('mx_546', 10): 50.0, ('mx_612', 13): 60.0, ('mx_184', 14): 90.0, ('mx_612', 2): 20.0}
segs = []  # (track, offset, t_start, t_end, fade_in, fade_out)
t_b5 = B[7]['speech_start'] - 0.15        # 'Because it makes no sense.' -> music stops
t_b7 = B[9]['visual_start']                # title card: music returns
for ci in range(1, 15):
    tr = next((t for t in PLAN[ci] if t in have), None)
    if tr is None: continue
    st = cstart(ci); en = cstart(ci + 1) + 2.0 if ci < 14 else TOTAL
    if ci == 1:
        segs.append((tr, 0.0, 0.0, t_b5, 2.5, 0.25))
        tr2 = next((t for t in PLAN[2] if t in have), tr)
        segs.append((tr2, 0.0, t_b7, cstart(2) + 2.0, 1.5, 2.0)); continue
    if ci == 2: st = cstart(2) - 0.5; segs.append((tr, OFFS.get((tr, ci), 40.0 if tr == segs[-1][0] else 0.0), st, en, 2.0, 2.0)); continue
    segs.append((tr, OFFS.get((tr, ci), 0.0), st, en, 2.0, 2.0 if ci < 14 else 4.0))
music = np.zeros((N, 2), np.float32); cache = {}
for tr, off, t0, t1, fi, fo in segs:
    if tr not in cache:
        x = decode(P/meta[tr]['file']); x *= 10 ** ((-16.0 - lufs(x)) / 20); cache[tr] = x
    x = cache[tr]; need = int((t1 - t0) * SR); o = int(off * SR) % len(x)
    y = np.concatenate([x[o:]] + [x] * (need // len(x) + 2))[:need].copy()
    ramp = np.ones(need, np.float32); a = int(fi * SR); b = int(fo * SR)
    if a: ramp[:a] = np.linspace(0, 1, a) ** 1.5
    if b: ramp[-b:] = np.minimum(ramp[-b:], np.linspace(1, 0, b) ** 1.5)
    s0 = int(t0 * SR); music[s0:s0 + need] += (y * ramp[:, None])[:N - s0]
# ---- ducking envelope: -18 dB under speech, -8 dB in the gaps (cards, pauses) ----
env_db = np.full(N, -8.0, np.float32)
for b in TL['beats']:
    s0 = int((b['speech_start'] - 0.25) * SR); s1 = int((b['speech_end'] + 0.35) * SR)
    env_db[max(0, s0):s1] = -18.0
# a quieter, darker bed under the cold open's first lines
env_db[:int(B[4]['speech_start'] * SR)] = np.minimum(env_db[:int(B[4]['speech_start'] * SR)], -15.0)
# smooth with a 0.4 s moving average so the music breathes rather than pumps
k = int(0.4 * SR); cs = np.concatenate([[0.0], np.cumsum(env_db, dtype=np.float64)]); pad = k // 2
idx = np.arange(N); lo = np.clip(idx - pad, 0, N); hi = np.clip(idx + pad, 0, N)
env_db = ((cs[hi] - cs[lo]) / np.maximum(hi - lo, 1)).astype(np.float32)
music *= (10 ** (env_db / 20))[:, None]
write(A/'music_bed.wav', music)
mix = narr + music
peak = np.abs(mix).max(); print('peak before limiting', round(float(peak), 3))
write(A/'mix_premaster.wav', mix / max(1.0, peak / 0.97))
# final loudness for YouTube: -14 LUFS integrated, true peak -1.5 dBTP (two-pass loudnorm)
o = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(A/'mix_premaster.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(o[o.rindex('{'):o.rindex('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(A/'mix_premaster.wav'), '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,aresample=48000",
                '-ar', '48000', str(A/'final_mix.wav')], check=True)
json.dump({'segments': segs, 'music_available': sorted(have)}, open(P/'artifacts/music_plan.json', 'w'), indent=1)
print('final mix written', TOTAL)
