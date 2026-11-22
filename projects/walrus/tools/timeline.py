"""Master timeline, re-timed on the real narration durations (narration is the master track)."""
import json, re, subprocess
from pathlib import Path
P = Path(__file__).resolve().parents[1]
T = json.load(open(P/'artifacts/narration_timing.json'))
beats = json.load(open(P/'shot_plan.json'))
LEAD = 1.0          # black lead-in before the first word
CARD = 4.5          # chapter title card (music only) before chapters 2..13
TAIL_END = 9.0      # end card hold after the last word
FADE = 0.35
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)],capture_output=True,text=True).stdout)
chapters, t = [], LEAD
for ci in range(1, 15):
    if ci > 1:
        chapters.append({'type': 'card', 'chapter_index': ci, 'start': round(t, 3), 'end': round(t + CARD, 3)}); t += CARD
    d = dur(P/f'assets/audio/chapters/ch{ci:02d}.wav')
    chapters.append({'type': 'chapter_audio', 'chapter_index': ci, 'start': round(t, 3), 'end': round(t + d, 3), 'file': f'assets/audio/chapters/ch{ci:02d}.wav'})
    t += d
total = t
out = []
starts = {c['chapter_index']: c['start'] for c in chapters if c['type'] == 'chapter_audio'}
for b in T['beats']:
    i = b['beat'] - 1
    s = starts[b['chapter_index']] + b['start_in_chapter']
    e_speech = s + b['speech_dur']
    pause = b['pause_after']
    seg_end = e_speech + T['beat_gap'] + pause
    m = re.match(r'(\d+) — (.*)', beats[i]['chapter'])
    out.append({'beat': b['beat'], 'chapter_index': b['chapter_index'], 'chapter': beats[i]['chapter'],
                'plan_time': beats[i]['time'], 'speech_start': round(s, 3), 'speech_end': round(e_speech, 3),
                'pause': pause, 'visual_start': round(s, 3),
                'black_start': round(e_speech + T['beat_gap'], 3) if pause else None,
                'segment_end': round(seg_end, 3), 'voice_over': beats[i]['voice_over'], 'visual_plan': beats[i]['visual']})
# first beat visual starts at 0 (lead-in), each beat's visual runs to the next beat's speech start (or a chapter card)
out[0]['visual_start'] = 0.0
last = out[-1]
last['segment_end'] = round(last['speech_end'] + TAIL_END, 3)
total = last['segment_end']
json.dump({'lead': LEAD, 'card': CARD, 'fade': FADE, 'total': round(total, 3), 'chapters': chapters, 'beats': out},
          open(P/'artifacts/timeline.json', 'w'), indent=1)
def tc(x): return f'{int(x//60)}:{x%60:05.2f}'
print('total', tc(total))
for b in out: print(b['beat'], b['plan_time'], '->', tc(b['speech_start']), round(b['segment_end']-b['visual_start'],1), b['pause'])
