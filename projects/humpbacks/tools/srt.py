"""SRT from the real narration: sentence boundaries found as silences inside each beat's audio."""
import json, re, wave
import numpy as np
from pathlib import Path
P = Path(__file__).resolve().parents[1]
TL = json.load(open(P/'artifacts/timeline.json'))
MAXC = 42  # characters per line, 2 lines max

def load(f):
    with wave.open(str(f)) as w:
        sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return sr, a

def speech_spans(sr, a, min_gap=0.24):
    hop = int(sr * 0.01); n = len(a) // hop
    e = np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop] ** 2)) for i in range(n)])
    on = e > max(0.004, e.max() * 0.02)
    spans = []; i = 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            spans.append([i * 0.01, j * 0.01]); i = j
        else: i += 1
    merged = [spans[0]]
    for s in spans[1:]:
        if s[0] - merged[-1][1] < min_gap: merged[-1][1] = s[1]
        else: merged.append(s)
    return merged

def split_sentences(text):
    return re.split(r'(?<=[.!?:])\s+(?=[A-Z0-9"])', text)

def wrap(text):
    """split a sentence into cues of <= 2 lines x MAXC chars, breaking at punctuation when possible"""
    words = text.split(); cues = []; cur = []
    def fits(ws): return len(' '.join(ws)) <= MAXC * 2 - 10
    for w in words:
        if fits(cur + [w]): cur.append(w)
        else: cues.append(cur); cur = [w]
    if cur: cues.append(cur)
    # balance the last two cues
    if len(cues) > 1 and len(' '.join(cues[-1])) < 18:
        allw = cues[-2] + cues[-1]; h = len(allw) // 2; cues[-2:] = [allw[:h], allw[h:]]
    out = []
    for c in cues:
        s = ' '.join(c)
        if len(s) > MAXC:  # two lines, break near the middle
            best = min(range(1, len(c)), key=lambda k: abs(len(' '.join(c[:k])) - len(s) / 2))
            s = ' '.join(c[:best]) + '\n' + ' '.join(c[best:])
        out.append(s)
    return out

def tc(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

cues = []
for b in TL['beats']:
    sr, a = load(P/f"assets/audio/beats/beat_{b['beat']:03d}.wav")
    sents = split_sentences(b['voice_over'])
    sp = speech_spans(sr, a, 0.18)
    t0, t1 = sp[0][0], sp[-1][1]
    cands = [((sp[i][1] + sp[i+1][0]) / 2, sp[i+1][0] - sp[i][1], sp[i][1], sp[i+1][0]) for i in range(len(sp) - 1)]
    tot = sum(len(x) for x in sents); acc = 0; expect = []
    for x in sents[:-1]: acc += len(x) + 1; expect.append(t0 + (t1 - t0) * acc / (tot + len(sents) - 1))
    # monotonic DP: assign each expected boundary to a distinct candidate pause
    m, k = len(expect), len(cands)
    INF = 1e9; cost = [[INF] * (k + 1) for _ in range(m + 1)]; back = {}
    for j in range(k + 1): cost[0][j] = 0
    for i in range(1, m + 1):
        for j in range(i, k + 1):
            best = INF
            for jj in range(i - 1, j):
                c = cost[i-1][jj] + abs(cands[j-1][0] - expect[i-1]) - 0.8 * cands[j-1][1]
                if c < best: best = c; back[(i, j)] = jj
            cost[i][j] = best
    j = min(range(m, k + 1), key=lambda jj: cost[m][jj]) if k >= m else None
    if j is None:
        bnds = [(e, e) for e in expect]
    else:
        bnds = []
        for i in range(m, 0, -1): bnds.append((cands[j-1][2], cands[j-1][3])); j = back[(i, j)]
        bnds = bnds[::-1]
    spans = []; st = t0
    for e_end, n_start in bnds: spans.append([st, e_end]); st = n_start
    spans.append([st, t1])
    for s, (x0, x1) in zip(sents, spans):
        parts = wrap(s); tot = sum(len(p) for p in parts); acc = x0
        for p in parts:
            d = (x1 - x0) * len(p) / tot
            cues.append([b['speech_start'] + acc, b['speech_start'] + acc + d, p]); acc += d
# readability: extend each cue up to 0.6 s into the following silence, never overlapping the next cue
for i, c in enumerate(cues):
    nxt = cues[i + 1][0] - 0.05 if i + 1 < len(cues) else c[1] + 1.0
    c[1] = min(max(c[1], c[0] + 1.0), nxt, c[1] + 0.6) if c[1] < nxt else min(c[1], nxt)
srt = ''.join(f'{i+1}\n{tc(a)} --> {tc(z)}\n{t}\n\n' for i, (a, z, t) in enumerate(cues))
out = P.parents[1]/'output/walrus/why_polar_bears_throw_rocks_at_walruses.srt'
out.write_text(srt, encoding='utf-8')
# verify the subtitles carry the narration word for word
words = lambda s: re.sub(r'\s+', ' ', s).strip()
narr = ' '.join(l.strip() for l in open(P/'narration_en.txt') if l.strip() and not l.startswith('##'))
print(len(cues), 'cues; text matches narration:', words(' '.join(c[2].replace('\n', ' ') for c in cues)) == words(narr))
