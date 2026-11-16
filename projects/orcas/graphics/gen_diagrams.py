"""Animated diagrams for the orca film. One standalone HyperFrames composition per graphic beat.
Every number shown is spoken in the narration; nothing graphic or violent is depicted."""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_base import page
import shapes as S
from maps import land_path

P = os.path.dirname(HERE)
plan = json.load(open(P + "/shot_plan_retimed.json"))
OUT = HERE + "/compositions"
made = []

def dur(b): return plan[b]["duration"]
def write(name, beat, body, js, css="", d=None):
    d = d or dur(beat)
    html = page(name, d, body, js, css); path = f"{OUT}/{name}.html"
    if not (os.path.exists(path) and open(path).read() == html): open(path, "w").write(html)
    made.append((name, round(d, 2)))

COMMON = """
.h{font-weight:900;letter-spacing:-.03em;line-height:1.02}
.big{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums;font-weight:600}
.cap{font-family:'IBM Plex Mono',monospace;font-size:30px;color:var(--mist);letter-spacing:.06em}
.abs{position:absolute}
svg{overflow:visible}
"""

# ---------------------------------------------------------------- b008 size comparison
M = 92  # px per metre; picture on the left, stats in a column on the right
OW, OH = 9.8 * M, 340 * 9.8 * M / 1000
css = COMMON + f"""
.stage{{position:absolute;left:120px;top:150px;width:1160px;height:800px}}
.orca{{position:absolute;left:0;top:70px;width:{OW:.0f}px}}
.person{{position:absolute;left:{OW+40:.0f}px;top:{70+OH-1.8*M-10:.0f}px;height:{1.8*M:.0f}px}}
.pt{{position:absolute;left:{OW-10:.0f}px;top:{70+OH+4:.0f}px;white-space:nowrap}}
.bus{{position:absolute;left:0;top:{70+OH+150:.0f}px;width:{12*M:.0f}px;opacity:.3}}
.bt{{position:absolute;left:0;top:{70+OH+160+320*12*M/1200:.0f}px}}
.dim{{position:absolute;left:0;top:30px;width:{OW:.0f}px;height:2px;background:var(--amber)}}
.dimt{{position:absolute;left:{OW/2-90:.0f}px;top:-34px;font-size:44px;color:var(--amber)}}
.stats{{position:absolute;left:1380px;top:230px;display:flex;flex-direction:column;gap:64px}}
.st .v{{font-size:72px;color:var(--ice)}} .st .k{{font-size:28px;color:var(--mist);margin-top:6px}}
"""
body = f"""<div class="stage">
  <div class="dim"></div><div class="dimt big">≈ 10 m</div>
  {S.orca(cls='orca')}
  {S.svg(S.PERSON, '0 0 120 340', cls='person')}<div class="pt cap">PERSON · 1.8 M</div>
  {S.svg(S.BUS, '0 0 1200 320', cls='bus')}<div class="bt cap">CITY BUS · 12 M</div>
</div>
<div class="stats">
  <div class="st s1"><div class="v big">up to 10 t</div><div class="k cap">WEIGHT</div></div>
  <div class="st s2"><div class="v big">80–90 yrs</div><div class="k cap">FEMALES · ESTIMATED</div></div>
  <div class="st s3"><div class="v big">50–60 yrs</div><div class="k cap">MALES</div></div>
</div>"""
js = """
tl.from(".orca", { x: -260, opacity: 0, duration: 1.4, ease: "power3.out" }, 0.2);
tl.from(".dim", { scaleX: 0, transformOrigin: "left center", duration: 1.0, ease: "expo.out" }, 0.9);
tl.from(".dimt", { y: 16, opacity: 0, duration: 0.6, ease: "power2.out" }, 1.3);
tl.from(".person,.pt", { y: 30, opacity: 0, duration: 0.7, ease: "back.out(1.6)" }, 1.6);
tl.from(".bus,.bt", { x: 80, opacity: 0, duration: 1.0, ease: "sine.out" }, 2.2);
tl.from(".s1", { x: 30, opacity: 0, duration: 0.6, ease: "power3.out" }, 3.0);
tl.from(".s2", { x: 30, opacity: 0, duration: 0.6, ease: "power3.out" }, 5.4);
tl.from(".s3", { x: 30, opacity: 0, duration: 0.6, ease: "power3.out" }, 7.6);
tl.to(".orca", { x: 14, duration: 8, ease: "sine.inOut" }, 1.6);"""
write("b008_size", 8, body, js, css)

# ---------------------------------------------------------------- b009 world map
W, H = 1700, 760
land, Pw = land_path(HERE + "/data/land-110m.json", -180, 180, -70, 80, W, H)
# points in open ocean in every basin (lon, lat)
ocean = [(-150, 55), (-135, 40), (-125, 49), (-160, 20), (-120, 10), (-150, -20), (-110, -40), (-80, -60),
         (-40, 60), (-20, 40), (-10, 20), (-30, -10), (-20, -40), (-60, -50), (5, 70), (-5, 36), (-65, 30),
         (60, -10), (75, -30), (90, 0), (55, -45), (110, -45), (150, -45), (115, -25), (170, -20), (160, 40),
         (145, 15), (-175, -35), (10, -65), (60, -65), (120, -63), (170, -70), (-150, -70), (-60, -64), (20, -36),
         (-90, 25), (35, 72), (-170, 65)]
dots = "".join(f'<circle class="od" cx="{Pw(lo, la)[0]:.0f}" cy="{Pw(lo, la)[1]:.0f}" r="9" fill="#E9A23B"/>' for lo, la in ocean)
css = COMMON + f""".map{{position:absolute;left:{(1920-W)//2}px;top:90px;width:{W}px;height:{H}px}}
.ttl{{position:absolute;left:0;right:0;bottom:150px;text-align:center;font-size:64px}}
.prey{{position:absolute;left:0;right:0;bottom:80px;text-align:center;font-size:32px;letter-spacing:.12em;color:var(--mist)}}"""
body = f"""<svg class="map" viewBox="0 0 {W} {H}"><path d="{land}" fill="#1D3F4C" stroke="rgba(147,171,177,.35)" stroke-width="1"/>{dots}</svg>
<div class="ttl h">Every ocean on Earth</div><div class="prey">FISH · SEALS · SEA LIONS · SHARKS · WHALES</div>"""
js = """
tl.from(".map path", { opacity: 0, duration: 1.0, ease: "sine.out" }, 0.1);
tl.from(".od", { scale: 0, transformOrigin: "50% 50%", opacity: 0, duration: 0.5, ease: "back.out(2)", stagger: 0.06 }, 0.6);
tl.from(".ttl", { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, 1.0);
tl.from(".prey", { opacity: 0, letterSpacing: "0.4em", duration: 1.2, ease: "expo.out" }, 5.0);
tl.to(".od", { scale: 1.35, transformOrigin: "50% 50%", duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 7, stagger: 0.03 }, 3.0);"""
write("b009_worldmap", 9, body, js, css)

# ---------------------------------------------------------------- dorsal fins
FIN = "M 30 420 C 95 300 150 150 185 10 C 195 140 220 290 290 420 Z"       # tall straight male fin
FIN_F = "M 40 420 C 110 330 160 210 215 70 C 205 170 225 320 290 420 Z"    # falcate female fin
FIN_DROOP = "M 60 420 C 110 330 130 250 115 200 C 100 160 50 135 -40 140 C 40 175 150 230 190 300 C 215 350 245 395 290 420 Z"
def fin(path, nicks="", cls="", style="", fill="#04090C", flip=False, saddle=True):
    tr = ' transform="translate(320,0) scale(-1,1)"' if flip else ""
    sad = '<ellipse cx="160" cy="455" rx="150" ry="26" fill="#93ABB1" opacity=".55"/>' if saddle else ""
    return (f'<svg class="{cls}" viewBox="-60 0 420 490" style="{style}"><g{tr}>{sad}'
            f'<path d="{path}" fill="{fill}" stroke="rgba(238,242,236,.6)" stroke-width="3"/>{nicks}</g></svg>')
def nick(x, y, s=16): return f'<path d="M {x} {y} l {s} {-s*0.4} l 0 {s*0.8} Z" fill="#0A1C24"/>'
fins = [(FIN_F, [(222, 160), (238, 260)]), (FIN, [(204, 120)]), (FIN_F, [(230, 220), (226, 196), (250, 330)])]
css = COMMON + """.row{position:absolute;left:220px;right:220px;top:200px;display:flex;justify-content:space-between}
.f{width:360px;height:420px}.ring{position:absolute;width:64px;height:64px;border:4px solid var(--amber);border-radius:50%}
.t1{position:absolute;left:0;right:0;bottom:170px;text-align:center;font-size:64px}
.t2{position:absolute;left:0;right:0;bottom:110px;text-align:center}"""
rings = ""
for i, (_, ns) in enumerate(fins):
    for (x, y) in ns:
        # fin svg: viewBox -60..360 wide (420) mapped to 360px; height 490 -> 420px
        sc = 360 / 420
        rx = 220 + i * ((1920 - 440 - 360) / 2) + (x + 60) * sc - 32
        ry = 200 + y * sc - 32
        rings += f'<div class="ring r{i}" style="left:{rx:.0f}px;top:{ry:.0f}px"></div>'
body = ('<div class="row">' + "".join(fin(p, "".join(nick(x, y) for x, y in ns), cls=f"f f{i}") for i, (p, ns) in enumerate(fins))
        + f'</div>{rings}<div class="t1 h">Every fin is different</div><div class="t2 cap">MICHAEL BIGG · BRITISH COLUMBIA · 1970s</div>')
js = """
tl.from(".f0", { y: 140, opacity: 0, duration: 1.1, ease: "power3.out" }, 0.2);
tl.from(".f1", { y: 140, opacity: 0, duration: 1.1, ease: "expo.out" }, 0.45);
tl.from(".f2", { y: 140, opacity: 0, duration: 1.1, ease: "power2.out" }, 0.7);
tl.from(".t2", { opacity: 0, duration: 0.8, ease: "sine.out" }, 1.4);
tl.from(".t1", { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, 5.5);
tl.from(".ring", { scale: 0.2, opacity: 0, duration: 0.5, ease: "back.out(2.5)", stagger: 0.35 }, 6.2);"""
write("b016_fin_id", 16, body, js, css)

# ---------------------------------------------------------------- b020 family tree
css = COMMON + """.tree{position:absolute;left:180px;top:160px;width:1560px;height:640px}
.lab{position:absolute;font-size:56px}.lab .cap{display:block;margin-top:8px}
.l1{left:1240px;top:150px}.l2{left:1240px;top:640px}
.yrs{position:absolute;left:260px;top:880px;font-size:40px;color:var(--amber)}"""
body = """<svg class="tree" viewBox="0 0 1560 640">
 <path class="br b0" d="M 0 320 L 260 320" stroke="#EEF2EC" stroke-width="6" fill="none"/>
 <path class="br b1" d="M 260 320 C 420 320 420 60 640 60 L 1020 60" stroke="#EEF2EC" stroke-width="6" fill="none"/>
 <path class="br b2" d="M 260 320 C 420 320 420 580 640 580 L 1020 580" stroke="#EEF2EC" stroke-width="6" fill="none"/>
 <circle class="node" cx="260" cy="320" r="14" fill="#E9A23B"/>
 <path class="span" d="M 260 700 L 1020 700" stroke="#E9A23B" stroke-width="3" stroke-dasharray="10 10" fill="none"/>
</svg>
<div class="lab l1 h">Residents<span class="cap">FISH · MOSTLY SALMON</span></div>
<div class="lab l2 h">Bigg's<span class="cap">SEALS · SEA LIONS · WHALES</span></div>
<div class="yrs big">split more than 300,000 years ago</div>"""
js = """
tl.set(".br", { strokeDasharray: 1400, strokeDashoffset: 1400 }, 0);
tl.to(".b0", { strokeDashoffset: 0, duration: 0.8, ease: "power2.in" }, 0.2);
tl.from(".node", { scale: 0, transformOrigin: "50% 50%", duration: 0.5, ease: "back.out(3)" }, 0.9);
tl.to(".b1", { strokeDashoffset: 0, duration: 1.6, ease: "power3.out" }, 1.0);
tl.to(".b2", { strokeDashoffset: 0, duration: 1.6, ease: "power3.out" }, 1.15);
tl.from(".l1", { x: 40, opacity: 0, duration: 0.7, ease: "expo.out" }, 2.3);
tl.from(".l2", { x: 40, opacity: 0, duration: 0.7, ease: "power3.out" }, 2.5);
tl.from(".span", { scaleX: 0, transformOrigin: "left center", duration: 1.2, ease: "sine.inOut" }, 3.4);
tl.from(".yrs", { y: 20, opacity: 0, duration: 0.8, ease: "power2.out" }, 3.8);"""
write("b020_family_tree", 20, body, js, css)

# ---------------------------------------------------------------- b021 scientific names
css = COMMON + """.cols{position:absolute;left:140px;right:140px;top:360px;display:flex;justify-content:space-between}
.c{width:780px;display:flex;flex-direction:column;gap:18px}.c .n{font-size:84px;font-style:italic;font-weight:300;white-space:nowrap}
.c .w{font-size:34px;color:var(--mist);font-family:'IBM Plex Mono',monospace;letter-spacing:.08em}
.c .bar{width:100%;height:2px;background:var(--mist);opacity:.5}
.yr{position:absolute;left:0;right:0;top:170px;text-align:center}.q{position:absolute;left:0;right:0;bottom:170px;text-align:center;font-size:40px;color:var(--mist)}"""
body = """<div class="yr label amber">PROPOSED IN 2024</div>
<div class="cols"><div class="c c1"><div class="n">Orcinus ater</div><div class="bar"></div><div class="w">RESIDENTS</div></div>
<div class="c c2"><div class="n">Orcinus rectipinnus</div><div class="bar"></div><div class="w">BIGG'S KILLER WHALES</div></div></div>
<div class="q">two species — or two subspecies?</div>"""
js = """
tl.from(".yr", { opacity: 0, letterSpacing: "0.4em", duration: 1.0, ease: "expo.out" }, 0.2);
tl.from(".c1 .n", { y: 40, opacity: 0, duration: 0.9, ease: "power3.out" }, 4.0);
tl.from(".c1 .bar", { scaleX: 0, transformOrigin: "left center", duration: 0.8, ease: "expo.out" }, 4.3);
tl.from(".c1 .w", { opacity: 0, duration: 0.6, ease: "sine.out" }, 4.6);
tl.from(".c2 .n", { y: 40, opacity: 0, duration: 0.9, ease: "power2.out" }, 7.6);
tl.from(".c2 .bar", { scaleX: 0, transformOrigin: "left center", duration: 0.8, ease: "expo.out" }, 7.9);
tl.from(".c2 .w", { opacity: 0, duration: 0.6, ease: "sine.out" }, 8.2);
tl.from(".q", { y: 20, opacity: 0, duration: 0.8, ease: "power2.out" }, 10.6);"""
write("b021_names", 21, body, js, css)

# ---------------------------------------------------------------- b031 15% -> 14 of 15
seal_icon = lambda c: f'<svg class="si {c}" viewBox="0 0 600 200"><path d="{S.SEAL}" fill="currentColor"/></svg>'
grid = "".join(seal_icon("w" if i in {3, 11, 18, 24, 31, 40, 47, 52, 58, 66, 71, 79, 84, 90, 97} else "o") for i in range(100))
kills = "".join(seal_icon("k w" if i != 9 else "k o") for i in range(15))
css = COMMON + """.L{position:absolute;left:140px;top:210px;width:760px}.R{position:absolute;left:1060px;top:210px;width:720px}
.grid{display:grid;grid-template-columns:repeat(10,1fr);gap:14px 10px}.si{width:64px;height:22px}
.o{color:#3B5761}.w{color:var(--amber)}
.kg{display:grid;grid-template-columns:repeat(5,1fr);gap:34px 20px;margin-top:40px}.kg .si{width:120px;height:40px}
.v{font-size:120px;margin-top:40px}.t{font-size:30px;color:var(--mist);margin-top:8px;max-width:620px;font-family:'IBM Plex Mono',monospace;letter-spacing:.06em}
.ar{position:absolute;left:930px;top:470px;font-size:80px;color:var(--mist)}"""
body = f"""<div class="L"><div class="grid">{grid}</div><div class="v big amber vL">≈15%</div><div class="t">OF SEALS RESTING ON THE ICE WERE WEDDELL SEALS</div></div>
<div class="ar">→</div>
<div class="R"><div class="kg">{kills}</div><div class="v big amber vR">14 of 15</div><div class="t">KILLS RECORDED WERE WEDDELL SEALS</div></div>"""
js = """
tl.from(".grid .si", { opacity: 0, scale: 0.6, duration: 0.35, ease: "power2.out", stagger: 0.012 }, 0.3);
tl.from(".grid .w", { color: "#3B5761", duration: 0.6, ease: "sine.inOut" }, 3.4);
tl.from(".L .v, .L .t", { y: 24, opacity: 0, duration: 0.7, ease: "power3.out" }, 3.6);
tl.from(".ar", { x: -30, opacity: 0, duration: 0.6, ease: "expo.out" }, 6.6);
tl.from(".kg .si", { opacity: 0, y: 20, duration: 0.4, ease: "back.out(2)", stagger: 0.08 }, 7.0);
tl.from(".R .v, .R .t", { y: 24, opacity: 0, duration: 0.7, ease: "power3.out" }, 8.8);"""
write("b031_weddell", 31, body, js, css)

# ---------------------------------------------------------------- b048 blue whale, abstract and gore-free
css = COMMON + """.bw{position:absolute;left:180px;top:470px;width:1560px;opacity:.85}
.o{position:absolute;width:330px}.lab1{position:absolute;left:180px;top:790px}.lab2{position:absolute;left:180px;top:230px}
.push{position:absolute;font-size:70px;color:var(--amber)}"""
orcas = [(200, 290), (620, 250), (1080, 270), (1460, 320), (330, 700), (900, 720), (1380, 690),
         (560, 390), (1010, 400)]
body = (S.svg(S.BLUEWHALE, "0 0 2000 300", fill="#5E7F8A", cls="bw")
        + "".join(S.orca(cls=f"o o{i}", style=f"left:{x}px;top:{y}px") for i, (x, y) in enumerate(orcas))
        + '<div class="push p1" style="left:700px;top:500px">↓</div><div class="push p2" style="left:1150px;top:510px">↓</div>'
        + '<div class="lab1 cap">BLUE WHALE · 20 M OR MORE</div><div class="lab2 cap">A DOZEN OR SO ORCAS</div>')
js = """
tl.from(".bw", { x: -120, opacity: 0, duration: 1.4, ease: "sine.out" }, 0.1);
tl.from(".lab1", { opacity: 0, duration: 0.6, ease: "sine.out" }, 0.8);
tl.from(".o", { opacity: 0, x: -160, duration: 1.0, ease: "power3.out", stagger: 0.12 }, 0.5);
tl.from(".lab2", { opacity: 0, duration: 0.6, ease: "sine.out" }, 1.6);
tl.to(".o7,.o8", { y: 50, duration: 1.4, ease: "power2.inOut" }, 3.6);
tl.from(".push", { opacity: 0, y: -20, duration: 0.6, ease: "expo.out", stagger: 0.2 }, 3.6);
tl.to(".bw", { y: 60, duration: 4.0, ease: "sine.inOut" }, 3.8);
tl.to(".o", { x: 26, duration: 6, ease: "sine.inOut" }, 1.5);"""
write("b048_bluewhale", 48, body, js, css)

# ---------------------------------------------------------------- b051 3 kills
css = COMMON + """.n{position:absolute;left:0;right:0;top:170px;text-align:center;font-size:300px;color:var(--amber);line-height:1}
.t{position:absolute;left:0;right:0;top:500px;text-align:center;font-size:64px}
.range{position:absolute;left:460px;right:460px;top:690px;height:2px;background:var(--mist)}
.y1,.y2{position:absolute;top:720px;font-size:40px}.y1{left:400px}.y2{right:400px}
.ws{position:absolute;left:0;right:0;top:600px;display:flex;justify-content:center;gap:60px}.ws svg{width:240px}
.j{position:absolute;left:0;right:0;bottom:120px;text-align:center}"""
body = (f'<div class="n big">3</div><div class="t h">blue whale kills documented</div>'
        f'<div class="ws">{"".join(S.svg(S.BLUEWHALE, "0 0 2000 300", fill="#5E7F8A", cls="wi") for _ in range(3))}</div>'
        f'<div class="range"></div><div class="y1 big">2019</div><div class="y2 big">2021</div>'
        f'<div class="j cap">MARINE MAMMAL SCIENCE</div>')
js = """
tl.from(".n", { scale: 0.6, opacity: 0, duration: 0.9, ease: "back.out(1.8)" }, 0.2);
tl.from(".t", { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.7);
tl.from(".wi", { x: -60, opacity: 0, duration: 0.7, ease: "power2.out", stagger: 0.3 }, 1.4);
tl.from(".range", { scaleX: 0, duration: 1.0, ease: "expo.out" }, 2.6);
tl.from(".y1,.y2", { opacity: 0, y: 14, duration: 0.6, ease: "sine.out", stagger: 0.2 }, 2.9);
tl.from(".j", { opacity: 0, duration: 0.8, ease: "sine.out" }, 5.5);"""
write("b051_three_kills", 51, body, js, css)

# ---------------------------------------------------------------- b056/b057 shark liver
def shark_scene(name, beat, mode):
    css = COMMON + """.sh{position:absolute;left:260px;top:250px;width:1400px}
.lv{position:absolute;left:1330px;top:640px;font-size:44px}.t{position:absolute;left:0;right:0;bottom:120px;text-align:center;font-size:58px}"""
    sh = S.svg(S.SHARK, "0 0 1000 360", fill="#5E7F8A", cls="sh",
               extra=f'<path class="liver" d="{S.SHARK_LIVER}" fill="#E9A23B"/>')
    if mode == "find":
        body = sh + '<div class="lv big amber">LIVER</div><div class="t h">Each one missing the same organ</div>'
        js = """
tl.from(".sh", { x: -200, opacity: 0, duration: 1.4, ease: "power3.out" }, 0.2);
tl.from(".liver", { opacity: 0, duration: 0.8, ease: "sine.inOut" }, D * 0.62);
tl.from(".lv", { opacity: 0, x: 20, duration: 0.6, ease: "expo.out" }, D * 0.62 + 0.3);
tl.from(".t", { y: 24, opacity: 0, duration: 0.7, ease: "power2.out" }, D * 0.55);
tl.to(".sh", { x: 30, duration: D, ease: "sine.inOut" }, 1.6);"""
    else:
        body = sh + '<div class="lv big amber">LIVER</div><div class="t h">Huge, rich in oil: pure energy</div>'
        js = """
tl.from(".sh", { opacity: 0, duration: 0.5, ease: "sine.out" }, 0.1);
tl.fromTo(".liver", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.12, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0.5);
tl.from(".lv", { opacity: 0, duration: 0.5, ease: "expo.out" }, 0.4);
tl.from(".t", { y: 24, opacity: 0, duration: 0.7, ease: "power3.out" }, 0.8);"""
    write(name, beat, body, js, css)
shark_scene("b056_shark_liver", 56, "find")
shark_scene("b057_liver_energy", 57, "energy")

# ---------------------------------------------------------------- b058/b059 Port and Starboard fins
def ps(name, beat, names):
    css = COMMON + """.pair{position:absolute;left:330px;right:330px;top:170px;display:flex;justify-content:space-between}
.pf{width:460px;height:540px}.nm{position:absolute;top:760px;width:600px;text-align:center;font-size:96px;font-weight:900;letter-spacing:.06em}
.n1{left:300px}.n2{right:300px}.dot{position:absolute;left:944px;top:800px;width:32px;height:32px;border-radius:50%;background:var(--amber)}
.ds{position:absolute;top:670px;width:600px;text-align:center}.d1{left:300px}.d2{right:300px}
.meta{position:absolute;left:0;right:0;bottom:90px;text-align:center}"""
    body = (f'<div class="pair">{fin(FIN_DROOP, cls="pf pf1", saddle=False)}{fin(FIN_DROOP, cls="pf pf2", flip=True, saddle=False)}</div>'
            '<div class="ds d1 cap">BENDS LEFT</div><div class="ds d2 cap">BENDS RIGHT</div>')
    if names:
        body += ('<div class="nm n1">PORT</div><div class="dot"></div><div class="nm n2">STARBOARD</div>'
                 '<div class="meta cap amber">FIRST REPORTED 2009 · NAMIBIA</div>')
        js = """
tl.from(".pf", { opacity: 0, duration: 0.5, ease: "sine.out" }, 0.1);
tl.from(".ds", { opacity: 0, duration: 0.5, ease: "sine.out" }, 0.2);
tl.from(".n1", { x: -60, opacity: 0, duration: 0.9, ease: "expo.out" }, 0.9);
tl.from(".n2", { x: 60, opacity: 0, duration: 0.9, ease: "power3.out" }, 1.4);
tl.from(".dot", { scale: 0, duration: 0.5, ease: "back.out(3)" }, 1.9);
tl.from(".meta", { opacity: 0, y: 16, duration: 0.8, ease: "power2.out" }, 4.6);"""
    else:
        js = """
tl.from(".pf1", { y: 160, opacity: 0, duration: 1.2, ease: "power3.out" }, 0.2);
tl.from(".pf2", { y: 160, opacity: 0, duration: 1.2, ease: "expo.out" }, 0.6);
tl.from(".d1", { opacity: 0, duration: 0.6, ease: "sine.out" }, D * 0.62);
tl.from(".d2", { opacity: 0, duration: 0.6, ease: "sine.out" }, D * 0.62 + 0.9);"""
    write(name, beat, body, js, css)
ps("b058_two_fins", 58, False)
ps("b059_port_starboard", 59, True)

# ---------------------------------------------------------------- b060 sightings falling
css = COMMON + """.ch{position:absolute;left:200px;top:260px;width:1300px;height:520px}
.k{position:absolute;left:1540px;top:250px}.k .v{font-size:110px;color:var(--amber)}.k .c{width:260px}
.ttl{position:absolute;left:200px;top:150px;font-size:56px}.z{position:absolute;left:1520px;top:735px;font-size:40px;color:var(--mist)}
.ill{position:absolute;left:200px;top:820px;font-size:22px;color:var(--mist);opacity:.8}"""
body = """<div class="ttl h">Great white sightings</div>
<svg class="ch" viewBox="0 0 1300 520"><path class="ln" d="M 0 60 C 200 50 330 70 420 120 C 560 200 640 360 820 450 C 960 500 1100 505 1300 505" stroke="#EEF2EC" stroke-width="7" fill="none"/>
<line x1="0" y1="515" x2="1300" y2="515" stroke="#93ABB1" stroke-width="2" opacity=".5"/>
<circle class="mk" cx="420" cy="120" r="14" fill="#E9A23B"/></svg>
<div class="k"><div class="v big">7+</div><div class="c cap">DEAD GREAT WHITES FOUND IN 2017 ALONE</div></div>
<div class="z big">≈ 0</div><div class="ill cap">ILLUSTRATIVE TREND, IN THEIR FAVOURITE BAYS</div>"""
js = """
tl.from(".ttl", { y: 20, opacity: 0, duration: 0.7, ease: "power3.out" }, 0.2);
tl.set(".ln", { strokeDasharray: 1600, strokeDashoffset: 1600 }, 0);
tl.to(".ln", { strokeDashoffset: 1100, duration: 1.4, ease: "sine.inOut" }, 0.6);
tl.from(".mk", { scale: 0, transformOrigin: "50% 50%", duration: 0.5, ease: "back.out(3)" }, 1.9);
tl.from(".k", { x: 40, opacity: 0, duration: 0.8, ease: "expo.out" }, 2.0);
tl.to(".ln", { strokeDashoffset: 0, duration: 3.6, ease: "power2.inOut" }, 5.2);
tl.from(".z", { opacity: 0, duration: 0.6, ease: "sine.out" }, 8.6);
tl.from(".ill", { opacity: 0, duration: 0.8, ease: "sine.out" }, 1.0);"""
write("b060_sightings", 60, body, js, css)

# ---------------------------------------------------------------- b067 menopause species
sp = ["Orca", "False killer whale", "Short-finned pilot whale", "Beluga", "Narwhal"]
css = COMMON + """.ttl{position:absolute;left:0;right:0;top:150px;text-align:center;font-size:76px}
.sub{position:absolute;left:0;right:0;top:260px;text-align:center}
.lst{position:absolute;left:300px;right:300px;top:380px;display:flex;flex-direction:column;gap:22px}
.it{display:flex;align-items:center;gap:30px;font-size:52px}.it .d{width:22px;height:22px;border-radius:50%;background:var(--mist)}
.it.o .d{background:var(--amber)}.it.o{color:var(--amber)}.it .n{font-family:'IBM Plex Mono',monospace;font-size:28px;color:var(--mist);width:60px}"""
items = '<div class="it hu"><span class="n">00</span><span class="d" style="background:#EEF2EC"></span>Humans</div>' + "".join(
    f'<div class="it s{i}{" o" if i == 0 else ""}"><span class="n">0{i+1}</span><span class="d"></span>{n}</div>' for i, n in enumerate(sp))
body = f'<div class="ttl h">Menopause</div><div class="sub cap">HUMANS + FIVE TOOTHED WHALES</div><div class="lst">{items}</div>'
js = """
tl.from(".ttl", { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
tl.from(".sub", { opacity: 0, duration: 0.6, ease: "sine.out" }, 0.8);
tl.from(".hu", { x: -40, opacity: 0, duration: 0.6, ease: "expo.out" }, 2.4);
tl.from(".lst .it:not(.hu)", { x: -40, opacity: 0, duration: 0.55, ease: "power3.out", stagger: 0.35 }, 4.6);"""
write("b067_menopause", 67, body, js, css)

# ---------------------------------------------------------------- b072 4.5x
css = COMMON + """.v{position:absolute;left:0;right:0;top:140px;text-align:center;font-size:240px;color:var(--amber);line-height:1}
.rows{position:absolute;left:220px;right:220px;top:470px;display:flex;flex-direction:column;gap:56px}
.r .k{font-size:32px;color:var(--mist);font-family:'IBM Plex Mono',monospace;margin-bottom:14px;letter-spacing:.04em}
.r .b{height:56px;border-radius:4px}.b1{width:300px;background:var(--mist)}.b2{width:1350px;background:var(--amber)}
.ft{position:absolute;left:0;right:0;bottom:90px;text-align:center}"""
body = """<div class="v big"><span class="num">1.0</span>×</div>
<div class="rows"><div class="r r1"><div class="k">CALF MORTALITY · GRANDMOTHER ALIVE</div><div class="b b1"></div></div>
<div class="r r2"><div class="k">GRANDMOTHER DIED IN THE PREVIOUS TWO YEARS</div><div class="b b2"></div></div></div>
<div class="ft cap">2019 STUDY · ALMOST 400 YOUNG ORCAS</div>"""
js = """
tl.from(".ft", { opacity: 0, duration: 0.7, ease: "sine.out" }, 0.3);
tl.from(".r1", { opacity: 0, y: 20, duration: 0.6, ease: "power3.out" }, 1.2);
tl.from(".b1", { scaleX: 0, transformOrigin: "left center", duration: 0.8, ease: "expo.out" }, 1.4);
tl.from(".r2", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 4.0);
tl.from(".b2", { scaleX: 300/1350, transformOrigin: "left center", duration: 2.4, ease: "power2.inOut" }, 4.4);
tl.from(".v", { opacity: 0, scale: 0.8, duration: 0.6, ease: "back.out(2)" }, 4.2);
const v45 = range(1.0, 4.5, 0.1).map(x => x.toFixed(1)); stepper(".num", v45, lin(v45.length, 4.4, 2.4));"""
write("b072_four_point_five", 72, body, js, css)

# ---------------------------------------------------------------- b073 lifespan bars
css = COMMON + """.ttl{position:absolute;left:220px;top:170px;font-size:64px}
.rows{position:absolute;left:220px;right:220px;top:380px;display:flex;flex-direction:column;gap:70px}
.r .k{font-size:32px;color:var(--mist);font-family:'IBM Plex Mono',monospace;margin-bottom:14px;letter-spacing:.04em}
.bar{display:flex;height:60px}.base{width:760px;background:var(--mist);border-radius:4px 0 0 4px}.ext{width:620px;background:var(--amber);border-radius:0 4px 4px 0}
.plus{position:absolute;left:1000px;top:720px;font-size:60px;color:var(--amber)}"""
body = """<div class="ttl h">Female lifespan in toothed whales</div>
<div class="rows"><div class="r r1"><div class="k">SPECIES WITHOUT MENOPAUSE</div><div class="bar"><div class="base"></div></div></div>
<div class="r r2"><div class="k">SPECIES WITH MENOPAUSE</div><div class="bar"><div class="base b2"></div><div class="ext"></div></div></div></div>
<div class="plus big">+ around 40 years</div>"""
js = """
tl.from(".ttl", { y: 24, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
tl.from(".r1", { opacity: 0, duration: 0.5, ease: "sine.out" }, 1.0);
tl.from(".r1 .base", { scaleX: 0, transformOrigin: "left center", duration: 1.2, ease: "power2.out" }, 1.1);
tl.from(".r2", { opacity: 0, duration: 0.5, ease: "sine.out" }, 2.4);
tl.from(".b2", { scaleX: 0, transformOrigin: "left center", duration: 1.2, ease: "power2.out" }, 2.5);
tl.from(".ext", { scaleX: 0, transformOrigin: "left center", duration: 1.6, ease: "expo.out" }, 5.4);
tl.from(".plus", { y: 20, opacity: 0, duration: 0.7, ease: "back.out(2)" }, 6.4);"""
write("b073_lifespan", 73, body, js, css)

# ---------------------------------------------------------------- b080 day counter, b082 day 17
css = COMMON + """.lab{position:absolute;left:0;right:0;top:330px;text-align:center}
.day{position:absolute;left:0;right:0;top:390px;text-align:center;font-size:260px;line-height:1}
.track{position:absolute;left:360px;right:360px;top:760px;height:4px;background:#3B5761}.fill{height:4px;background:var(--amber);width:100%}
.km{position:absolute;left:0;right:0;top:820px;text-align:center;font-size:40px;color:var(--mist)}"""
body = '<div class="lab label">DAY</div><div class="day big"><span class="dn">1</span></div><div class="track"><div class="fill"></div></div>'
js = """
tl.from(".lab", { opacity: 0, duration: 0.5, ease: "sine.out" }, 0.1);
tl.from(".day", { opacity: 0, y: 20, duration: 0.5, ease: "power3.out" }, 0.15);
tl.from(".track", { opacity: 0, duration: 0.5, ease: "sine.out" }, 0.2);
const days = range(1, 14, 1).map(String); stepper(".dn", days, lin(days.length, 0.4, D - 1.4));
tl.fromTo(".fill", { scaleX: 1/17, transformOrigin: "left center" }, { scaleX: 14/17, duration: D - 1.2, ease: "sine.inOut" }, 0.4);"""
write("b080_day_counter", 80, body, js, css)
body = ('<div class="lab label">DAY</div><div class="day big amber">17</div><div class="track"><div class="fill"></div></div>'
        '<div class="km big">≈ 1,600 km</div>')
js = """
tl.from(".lab", { opacity: 0, duration: 0.5, ease: "sine.out" }, 0.1);
tl.from(".day", { opacity: 0, scale: 0.9, duration: 0.8, ease: "power3.out" }, 0.2);
tl.fromTo(".fill", { scaleX: 14/17, transformOrigin: "left center" }, { scaleX: 1, duration: 1.2, ease: "expo.out" }, 0.3);
tl.from(".km", { opacity: 0, y: 16, duration: 0.7, ease: "power2.out" }, 1.4);"""
write("b082_day17", 82, body, js, css)

# ---------------------------------------------------------------- b085 Salish Sea map
W, H = 1600, 900
land, Ps = land_path(HERE + "/data/land-10m.json", -125.6, -121.6, 47.0, 49.7, W, H, min_px=4)
def lab(txt, lo, la, cls="cap", style=""):
    x, y = Ps(lo, la); return f'<div class="ml {cls}" style="left:{160+x:.0f}px;top:{90+y:.0f}px;{style}">{txt}</div>'
css = COMMON + f""".map{{position:absolute;left:160px;top:90px;width:{W}px;height:{H}px;overflow:hidden;
  -webkit-mask-image:radial-gradient(ellipse 52% 52% at 52% 50%,#000 40%,transparent 92%);mask-image:radial-gradient(ellipse 52% 52% at 52% 50%,#000 40%,transparent 92%)}}
.ml{{position:absolute;transform:translate(-50%,-50%);white-space:nowrap}}
.sea{{font-family:'Fraunces',serif;font-size:58px;font-style:italic;font-weight:300;color:var(--amber)}}"""
sx, sy = Ps(-123.1, 48.45)
body = (f'<svg class="map" viewBox="0 0 {W} {H}"><defs><radialGradient id="gl"><stop offset="0" stop-color="#E9A23B" stop-opacity=".26"/><stop offset="1" stop-color="#E9A23B" stop-opacity="0"/></radialGradient></defs><ellipse class="glow" cx="{sx:.0f}" cy="{sy:.0f}" rx="380" ry="260" fill="url(#gl)"/>'
        f'<path d="{land}" fill="#24495A" stroke="rgba(147,171,177,.55)" stroke-width="1.2"/></svg>'
        + lab("BRITISH COLUMBIA", -122.6, 49.45) + lab("VANCOUVER ISLAND", -124.75, 49.15)
        + lab("WASHINGTON STATE", -122.2, 47.35) + lab("Salish Sea", -123.15, 48.62, "sea"))
js = """
tl.from(".map path", { opacity: 0, duration: 1.0, ease: "sine.out" }, 0.1);
tl.from(".glow", { scale: 0.4, transformOrigin: "50% 50%", opacity: 0, duration: 1.6, ease: "power2.out" }, 0.8);
tl.from(".ml.cap", { opacity: 0, y: 10, duration: 0.6, ease: "power3.out", stagger: 0.3 }, 1.4);
tl.from(".sea", { opacity: 0, letterSpacing: "0.3em", duration: 1.2, ease: "expo.out" }, 2.6);"""
write("b085_salish_map", 85, body, js, css)

# ---------------------------------------------------------------- b087 98 -> 73, b089 76 -> 77 (same visual space)
def popgrid():
    return '<div class="pg">' + "".join(f'<div class="pd p{i}"></div>' for i in range(98)) + "</div>"
POPCSS = COMMON + """.pg{position:absolute;left:220px;top:250px;width:780px;display:grid;grid-template-columns:repeat(14,1fr);gap:16px}
.pd{width:38px;height:38px;border-radius:50%;background:var(--ice)}
.num{position:absolute;left:1150px;top:280px;font-size:220px;line-height:1}.yr{position:absolute;left:1150px;top:520px;font-size:44px;color:var(--mist)}
.note{position:absolute;left:1150px;top:620px;width:560px}.ttl{position:absolute;left:220px;top:140px}"""
body = popgrid() + '<div class="ttl label">SOUTHERN RESIDENTS</div><div class="num big"><span class="n">98</span></div><div class="yr big"><span class="y">1995</span></div><div class="note cap">ENDANGERED IN THE UNITED STATES AND CANADA</div>'
lost = list(range(73, 98))
js = f"""
tl.from(".ttl", {{ opacity: 0, duration: 0.6, ease: "sine.out" }}, 0.1);
tl.from(".pd", {{ scale: 0, duration: 0.3, ease: "back.out(2)", stagger: 0.012 }}, 0.2);
tl.from(".num", {{ opacity: 0, y: 20, duration: 0.6, ease: "power3.out" }}, 0.4);
tl.from(".yr", {{ opacity: 0, duration: 0.5, ease: "sine.out" }}, 0.6);
tl.to("{','.join(f'.p{i}' for i in lost)}", {{ opacity: 0.12, duration: 0.25, ease: "sine.in", stagger: 0.09 }}, 3.4);
const pop = range(98, 73, 1).map(String); stepper(".n", pop, lin(pop.length, 3.4, 0.09 * 25));
stepper(".y", ["1995", "2021"], [0, 4.6]);
tl.from(".note", {{ opacity: 0, y: 16, duration: 0.7, ease: "power2.out" }}, 7.8);"""
write("b087_98_to_73", 87, body, js, POPCSS)
body = popgrid() + '<div class="ttl label">SOUTHERN RESIDENTS</div><div class="num big"><span class="n">73</span><span class="up amber"> ↑</span></div><div class="yr big"><span class="y">end of 2021</span></div><div class="note cap nc">2026 CENSUS · SECOND YEAR IN A ROW OF A SMALL INCREASE</div><div class="note cap calf" style="top:740px;color:#E9A23B">OCTOBER 2026 · A NEW CALF</div>'
dim = ",".join(f".p{i}" for i in range(73, 98))
js = f"""
tl.set("{dim}", {{ opacity: 0.12 }}, 0);
tl.from(".ttl,.num,.yr", {{ opacity: 0, duration: 0.5, ease: "sine.out" }}, 0.1);
tl.from(".pd", {{ opacity: 0, duration: 0.5, ease: "sine.out" }}, 0.1);
tl.to(".p73,.p74,.p75", {{ opacity: 1, backgroundColor: "#EEF2EC", duration: 0.5, ease: "back.out(2)", stagger: 0.4 }}, 1.6);
stepper(".n", ["73", "74", "75", "76", "77"], [0, 1.6, 2.0, 2.4, 7.2]);
stepper(".y", ["end of 2021", "2026 census", "October 2026"], [0, 1.6, 7.2]);
tl.from(".up", {{ opacity: 0, y: 20, duration: 0.5, ease: "back.out(2)" }}, 3.0);
tl.from(".nc", {{ opacity: 0, y: 16, duration: 0.7, ease: "power2.out" }}, 3.2);
tl.to(".p76", {{ opacity: 1, backgroundColor: "#E9A23B", scale: 1.25, duration: 0.7, ease: "back.out(3)" }}, 7.2);
tl.set(".n", {{ color: "#E9A23B" }}, 7.2);
tl.from(".calf", {{ opacity: 0, y: 16, duration: 0.7, ease: "power3.out" }}, 7.4);"""
write("b089_76_to_77", 89, body, js, POPCSS)

# ---------------------------------------------------------------- b094 700+ / 8+
css = COMMON + """.two{position:absolute;left:200px;right:200px;top:300px;display:flex;justify-content:space-around}
.k{text-align:center}.k .v{font-size:200px;line-height:1}.k .c{margin-top:20px}"""
body = """<div class="two"><div class="k k1"><div class="v big">700+</div><div class="c cap">INTERACTIONS LOGGED</div></div>
<div class="k k2"><div class="v big amber">8+</div><div class="c cap">BOATS SUNK</div></div></div>"""
js = """
tl.from(".k1", { y: 40, opacity: 0, duration: 0.7, ease: "power3.out" }, 0.2);
tl.from(".k2", { y: 40, opacity: 0, duration: 0.7, ease: "expo.out" }, 2.4);"""
write("b094_700_8", 94, body, js, css)

# ---------------------------------------------------------------- b112 end card
css = COMMON + """.brand{position:absolute;left:0;right:0;top:130px;text-align:center;font-size:84px}
.sub{position:absolute;left:0;right:0;top:250px;text-align:center}
.slots{position:absolute;left:260px;right:260px;top:390px;display:flex;justify-content:space-between}
.sl{width:640px;height:360px;border:2px solid rgba(147,171,177,.6);border-radius:10px;display:flex;align-items:flex-end;padding:24px;box-sizing:border-box;font-size:40px}
.cta{position:absolute;left:0;right:0;bottom:120px;text-align:center;font-size:44px}"""
body = """<div class="brand h">Naturexplore</div><div class="sub cap">A NEW DOCUMENTARY EVERY WEDNESDAY</div>
<div class="slots"><div class="sl s1">The Octopus: An Alien Mind</div><div class="sl s2"></div></div>
<div class="cta">Which orca tradition surprised you most?</div>"""
js = """
tl.from(".brand", { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
tl.from(".sub", { opacity: 0, duration: 0.6, ease: "sine.out" }, 0.6);
tl.from(".s1", { x: -60, opacity: 0, duration: 0.8, ease: "expo.out" }, 1.0);
tl.from(".s2", { x: 60, opacity: 0, duration: 0.8, ease: "power2.out" }, 1.2);
tl.from(".cta", { y: 20, opacity: 0, duration: 0.7, ease: "back.out(1.6)" }, 4.5);"""
write("b112_end_card", 112, body, js, css, d=max(dur(112), 20.0))

for m in made: print(*m)
print(len(made), "diagrams")
