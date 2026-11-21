import hashlib, subprocess, json, time
from pathlib import Path
P = Path(__file__).resolve().parents[1]
m = json.load(open(P/'artifacts/search/commons_meta.json'))
picks0 = {'Interloper_(MacLeod,_Kevin)_(ISRC_USUAN1100401).oga':'interloper','Distant_Tension_(ISRC_USUAN1100257).mp3':'distant_tension','Kevin_MacLeod_-_Isolated.ogg':'isolated','Kevin_MacLeod_-_Unanswered_Questions.ogg':'unanswered_questions','Stratosphere,_(MacLeod,_Kevin).oga':'stratosphere','Healing_(Kevin_MacLeod)_(ISRC_USUAN1200048).oga':'healing','Peaceful_Desolation_(Kevin_MacLeod)_(ISRC_USUAN1200017).oga':'peaceful_desolation','Kevin_MacLeod_-_On_the_Passing_of_Time.ogg':'passing_of_time','Kevin_MacLeod_-_Inner_Light.ogg':'inner_light','Kevin_MacLeod_-_Winter_Reflections.ogg':'winter_reflections','Earth_Prelude_(MacLeod,_Kevin)_(ISRC_USUAN1100247).oga':'earth_prelude','The_Voices_(MacLeod,_Kevin)_(ISRC_USUAN1100046).oga':'the_voices','Kevin_MacLeod_-_06_-_Impact_Lento.ogg':'impact_lento','Spc_X2x_(Unseen_Presence)_by_Kevin_MacLeod.ogg':'unseen_presence'}
order = ['interloper','healing','peaceful_desolation','passing_of_time','inner_light','the_voices','isolated','earth_prelude','distant_tension','stratosphere','unanswered_questions','winter_reflections','impact_lento','unseen_presence']
inv = {v: k for k, v in picks0.items()}
picks = {inv[k]: k for k in order}
metaf = P/'assets/music/music_meta.json'
meta = json.load(open(metaf)) if metaf.exists() else {}
for f, k in picks.items():
    ext = f.rsplit('.', 1)[1]; out = P/f'assets/music/{k}.{ext}'
    lic = [l for l in m['File:'+f]['licence'] if l != 'CC BY-SA 4.0'][0]
    meta[k] = {'file': str(out.relative_to(P)), 'title': f.rsplit('.', 1)[0].replace('_', ' '), 'author': 'Kevin MacLeod (incompetech.com)', 'page_url': m['File:'+f]['page_url'], 'licence': lic, 'provider': 'Wikimedia Commons'}
    json.dump(meta, open(metaf, 'w'), indent=1)
    if out.exists() and out.stat().st_size > 100000: continue
    h = hashlib.md5(f.encode()).hexdigest(); url = f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{f}'
    for a in range(12):
        r = subprocess.run(['curl', '-s', '-m', '180', '-A', 'NaturexploreDocBot/1.0 (documentary research; github.com/Davor26/lead)', '-o', str(out), '-w', '%{http_code}', url], capture_output=True, text=True).stdout
        print(time.strftime('%H:%M'), r, k, flush=True)
        if r == '200': break
        time.sleep(660)
    time.sleep(4)
print('done')
