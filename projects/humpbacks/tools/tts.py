"""Narration: piper_tts en_GB-cori-high, one WAV per beat, then one WAV per chapter."""
import json, re, wave, sys
import numpy as np
from pathlib import Path
from piper import PiperVoice, SynthesisConfig

P = Path(__file__).resolve().parents[1]
LS = float(sys.argv[1]) if len(sys.argv) > 1 else 1.05
voice = PiperVoice.load(str(P/'assets/voice/en_GB-cori-high.onnx'))
SR = voice.config.sample_rate
cfg = SynthesisConfig(length_scale=LS, noise_scale=0.6, noise_w_scale=0.8)
# TTS-only pronunciation aids: the spoken words stay the same, only spelling for the phonemizer changes.
SAY = {'Schulman-Janiger': 'Shulman Janiger', 'Megaptera': 'Mega-ptera', "Bigg's": 'Biggs'}
SENT_GAP = 0.45   # silence between sentences inside a beat
BEAT_GAP = 0.8   # silence between beats (pauses from the shot plan are added on top)

beats = json.load(open(P/'shot_plan.json'))
def synth(text):
    for k, v in SAY.items(): text = text.replace(k, v)
    sents = re.split(r'(?<=[.!?:])\s+(?=[A-Z0-9"])', text)
    out = []
    for s in sents:
        a = np.concatenate([c.audio_int16_array for c in voice.synthesize(s, syn_config=cfg)])
        out += [a, np.zeros(int(SENT_GAP*SR), np.int16)]
    return np.concatenate(out[:-1])

def write(path, a):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())

timing = []
chapters = {}
for i, b in enumerate(beats):
    a = synth(b['voice_over'])
    write(P/f'assets/audio/beats/beat_{i+1:03d}.wav', a)
    m = re.search(r'\[(\d+(?:\.\d+)?) s — pause\]', b['visual'])
    pause = float(m.group(1)) if m else 0.0
    chapters.setdefault(b['chapter'], []).append((i, a, pause))
    print(i+1, round(len(a)/SR, 2), pause, flush=True)

for ci, (ch, items) in enumerate(chapters.items(), 1):
    parts, t = [], 0.0
    for i, a, pause in items:
        dur = len(a)/SR
        timing.append({'beat': i+1, 'chapter': ch, 'chapter_index': ci, 'start_in_chapter': round(t, 3),
                       'speech_dur': round(dur, 3), 'pause_after': pause})
        tail = BEAT_GAP + pause
        parts += [a, np.zeros(int(round(tail*SR)), np.int16)]
        t += dur + tail
    write(P/f'assets/audio/chapters/ch{ci:02d}.wav', np.concatenate(parts))
json.dump({'length_scale': LS, 'sample_rate': SR, 'beat_gap': BEAT_GAP, 'sentence_gap': SENT_GAP,
           'tts_pronunciation_aids': SAY, 'beats': timing},
          open(P/'artifacts/narration_timing.json', 'w'), indent=1)
print('done')
