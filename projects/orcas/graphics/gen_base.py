"""Shared shell for the orca graphics: each graphic is a standalone HyperFrames composition."""
GSAP = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
CSS = """
@font-face{font-family:'Fraunces';src:url('fonts/fraunces-latin-900-normal.woff2') format('woff2');font-weight:900;font-style:normal}
@font-face{font-family:'Fraunces';src:url('fonts/fraunces-latin-600-normal.woff2') format('woff2');font-weight:600;font-style:normal}
@font-face{font-family:'Fraunces';src:url('fonts/fraunces-latin-300-normal.woff2') format('woff2');font-weight:300;font-style:normal}
@font-face{font-family:'Fraunces';src:url('fonts/fraunces-latin-300-italic.woff2') format('woff2');font-weight:300;font-style:italic}
:root{--deep:#0A1C24;--mid:#12313D;--ice:#EEF2EC;--mist:#93ABB1;--amber:#E9A23B}
html,body{margin:0;background:#0A1C24}
[data-composition-id]{position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--deep);
  color:var(--ice);font-family:'Fraunces',serif}
.light{position:absolute;left:50%;top:-38%;width:2200px;height:1500px;margin-left:-1100px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(18,49,61,.95),rgba(18,49,61,.35) 55%,rgba(10,28,36,0) 100%)}
.caustic{position:absolute;inset:-10%;opacity:.07;
  background:radial-gradient(ellipse 60px 18px at 20% 30%,#EEF2EC,transparent),radial-gradient(ellipse 90px 22px at 70% 20%,#EEF2EC,transparent),
  radial-gradient(ellipse 50px 14px at 45% 55%,#EEF2EC,transparent),radial-gradient(ellipse 80px 20px at 85% 60%,#EEF2EC,transparent),
  radial-gradient(ellipse 70px 16px at 10% 75%,#EEF2EC,transparent)}
.veil{position:absolute;inset:0;background:#0A1C24;z-index:50}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;
  padding:120px 160px;gap:28px;box-sizing:border-box;z-index:10}
.mono{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums}
.label{font-family:'IBM Plex Mono',monospace;font-size:30px;letter-spacing:.08em;color:var(--mist);text-transform:uppercase}
.amber{color:var(--amber)}
.stk{display:inline-grid}.stk>span{grid-area:1/1}
"""
def page(cid, dur, body, js, extra_css=""):
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{cid}</title>
<style>{CSS}{extra_css}</style></head>
<body>
<div id="root" data-composition-id="{cid}" data-start="0" data-duration="{dur:.3f}" data-width="1920" data-height="1080">
  <div class="light"></div><div class="caustic"></div>
  {body}
  <div class="veil"></div>
</div>
<script src="{GSAP}"></script>
<script>
window.__timelines = window.__timelines || {{}};
const D = {dur:.3f};
const tl = gsap.timeline({{ paused: true }});
// Deterministic text stepper: every value is a stacked span toggled by tl.set (seek-safe, no callbacks).
function stepper(sel, vals, times) {{
  const el = document.querySelector(sel); el.classList.add("stk"); el.textContent = "";
  const sp = vals.map((v, i) => {{ const s = document.createElement("span"); s.textContent = v; s.style.opacity = i ? 0 : 1; el.appendChild(s); return s; }});
  for (let i = 1; i < vals.length; i++) {{ tl.set(sp[i - 1], {{ opacity: 0 }}, times[i]); tl.set(sp[i], {{ opacity: 1 }}, times[i]); }}
}}
function lin(n, t0, d) {{ return Array.from({{ length: n }}, (_, i) => t0 + d * i / Math.max(n - 1, 1)); }}
function range(a, b, step) {{ const out = []; const n = Math.round(Math.abs(b - a) / step); for (let i = 0; i <= n; i++) out.push(a + (b > a ? 1 : -1) * step * i); return out; }}
tl.to(".veil", {{ opacity: 0, duration: 0.4, ease: "sine.out" }}, 0);
tl.fromTo(".light", {{ scale: 1 }}, {{ scale: 1.06, duration: D, ease: "sine.inOut" }}, 0);
tl.fromTo(".caustic", {{ x: 0, y: 0 }}, {{ x: 40, y: 18, duration: D, ease: "none" }}, 0);
{js}
tl.to(".veil", {{ opacity: 1, duration: 0.4, ease: "sine.in" }}, D - 0.4);
window.__timelines["{cid}"] = tl;
</script>
</body></html>"""
