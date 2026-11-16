"""Chapter title cards and the opening title."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_base import page
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plan = json.load(open(P + "/shot_plan_retimed.json"))
OUT = os.path.dirname(os.path.abspath(__file__)) + "/compositions"
CSS = """
.num{font-family:'IBM Plex Mono',monospace;font-size:44px;letter-spacing:.3em;color:var(--amber)}
.rule{width:120px;height:2px;background:var(--amber)}
.ttl{font-size:150px;font-weight:900;letter-spacing:-.03em;line-height:1;text-align:center}
"""
cards = {15: ("1", "Two worlds, one sea"), 25: ("2", "The wave makers"), 34: ("3", "The beach raiders"),
         44: ("4", "Hunting a giant"), 54: ("5", "Port and Starboard"), 66: ("6", "The grandmothers"),
         76: ("7", "Seventeen days"), 92: ("8", "The rudder raiders")}
made = []
for beat, (n, title) in cards.items():
    dur = plan[beat]["duration"]
    body = f'<div class="scene"><div class="num">CHAPTER {n}</div><div class="rule"></div><div class="ttl">{title}</div></div>'
    js = """
tl.from(".num", { y: 24, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
tl.from(".rule", { scaleX: 0, duration: 0.7, ease: "expo.out" }, 0.3);
tl.from(".ttl", { y: 40, opacity: 0, duration: 0.9, ease: "power2.out" }, 0.35);"""
    name = f"b{beat:03d}_card{n}"
    open(f"{OUT}/{name}.html", "w").write(page(name, dur, body, js, CSS)); made.append((name, dur))
# opening title (beat 6): narration line, then the title rises during the 3 s music swell
b = plan[6]; dur = b["duration"]; t_title = b["speech_end"] - b["start"]
body = """<div class="scene"><div class="sub label">Naturexplore</div>
<div class="ttl big">ORCAS</div><div class="rule"></div><div class="tag">The Ocean's Wolf Packs</div></div>"""
css = CSS + ".big{font-size:260px;letter-spacing:.04em}.tag{font-size:72px;font-weight:300;font-style:italic}"
js = f"""
tl.from(".sub", {{ opacity: 0, duration: 0.8, ease: "sine.out" }}, {t_title - 1.2:.2f});
tl.from(".big", {{ y: 60, opacity: 0, scale: 0.96, duration: 1.4, ease: "power3.out" }}, {t_title - 0.9:.2f});
tl.from(".rule", {{ scaleX: 0, duration: 0.9, ease: "expo.out" }}, {t_title - 0.2:.2f});
tl.from(".tag", {{ y: 30, opacity: 0, duration: 1.0, ease: "power2.out" }}, {t_title:.2f});"""
open(f"{OUT}/b006_title.html", "w").write(page("b006_title", dur, body, js, css)); made.append(("b006_title", dur))
for m in made: print(m[0], round(m[1], 2))
