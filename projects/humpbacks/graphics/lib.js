// Naturexplore "Why Orcas Don't Kill Humans" — graphics library.
// Deterministic: every frame is a pure function of t (seconds). No CSS animation.
const W = 1920, H = 1080;
const C = {
  ink: '#eef4f8', dim: '#9fb3c4', faint: '#5b7287',
  ice: '#7fd3ff', iceDeep: '#2f8fc4', warm: '#f2b866', red: '#e2583e',
  navy0: '#020b15', navy1: '#06192b', navy2: '#0c2b45',
  paper: '#d9cdb2', paperInk: '#3b3125',
};
const FONT = "'Inter Display', 'Inter', sans-serif";
const MONO = "'JetBrains Mono', monospace";

const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, k) => a + (b - a) * k;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const easeOut = k => 1 - Math.pow(1 - k, 3);
const easeIn = k => k * k * k;
const easeIO = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const eo = (t, a, b) => easeOut(seg(t, a, b));
const eio = (t, a, b) => easeIO(seg(t, a, b));
// global fade in at start and out at end of a clip of duration D
const envelope = (t, D, fi = 0.5, fo = 0.5) => Math.min(seg(t, 0, fi), 1 - seg(t, D - fo, D));
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function txt(x, y, s, o = {}) {
  const size = o.size || 48, w = o.weight || 700, fill = o.fill || C.ink, a = o.anchor || 'middle';
  const op = o.opacity === undefined ? 1 : o.opacity, ls = o.ls === undefined ? 0 : o.ls;
  const fam = o.mono ? MONO : FONT;
  const tr = o.transform ? ` transform="${o.transform}"` : '';
  return `<text x="${x}" y="${y}" font-family="${fam}" font-size="${size}" font-weight="${w}" fill="${fill}" text-anchor="${a}" opacity="${op}" letter-spacing="${ls}"${tr}${o.extra || ''}>${esc(s)}</text>`;
}
// text that rises and fades in at time a
function rise(t, a, x, y, s, o = {}) {
  const k = eo(t, a, a + (o.dur || 0.7));
  return txt(x, y + (1 - k) * (o.dy === undefined ? 24 : o.dy), s, Object.assign({}, o, { opacity: k * (o.opacity === undefined ? 1 : o.opacity) }));
}
const fmt = n => Math.round(n).toLocaleString('en-US');

// --- background: deep water, slow light shafts, vignette -------------------
function defs() {
  return `<defs>
  <radialGradient id="bgG" cx="50%" cy="30%" r="85%"><stop offset="0" stop-color="${C.navy2}"/><stop offset="0.55" stop-color="${C.navy1}"/><stop offset="1" stop-color="${C.navy0}"/></radialGradient>
  <linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd8ff" stop-opacity="0.11"/><stop offset="1" stop-color="#9fd8ff" stop-opacity="0"/></linearGradient>
  <radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.65"/></radialGradient>
  <linearGradient id="iceBar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${C.iceDeep}"/><stop offset="1" stop-color="${C.ice}"/></linearGradient>
  <linearGradient id="warmBar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b9782f"/><stop offset="1" stop-color="${C.warm}"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="SEED"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"/></filter>
  </defs>`;
}
function bg(t, o = {}) {
  let s = `<rect width="${W}" height="${H}" fill="url(#bgG)"/>`;
  const shafts = [[300, 160, 0.9], [760, 120, 1.3], [1180, 200, 0.7], [1600, 140, 1.1]];
  shafts.forEach(([x, w, sp], i) => {
    const dx = Math.sin(t * 0.12 * sp + i * 1.7) * 60;
    const op = 0.6 + 0.4 * Math.sin(t * 0.3 * sp + i);
    s += `<polygon points="${x + dx - w / 2},0 ${x + dx + w / 2},0 ${x + dx * 2.2 + w * 1.6},${H} ${x + dx * 2.2 - w * 0.4},${H}" fill="url(#shaft)" opacity="${op.toFixed(3)}"/>`;
  });
  // drifting particles (marine snow)
  for (let i = 0; i < 70; i++) {
    const px = (i * 739.3 % W + t * (6 + i % 5)) % W, py = (i * 397.7 % H - t * (3 + i % 7) * 2 + H * 4) % H;
    s += `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="${1 + i % 3 * 0.6}" fill="#cfe9ff" opacity="${0.06 + (i % 4) * 0.03}"/>`;
  }
  if (!o.noVig) s += `<rect width="${W}" height="${H}" fill="url(#vig)"/>`;
  return s;
}
function grain(t) { return `<rect width="${W}" height="${H}" filter="url(#grain)" opacity="0.9"/>`.replace('SEED', ''); }

// --- silhouettes (unit boxes; use transform to place) -----------------------
// Orca, side view, facing right, ~ 200 x 70 box (fin up to y=-40)
const ORCA_SIDE = 'M200,34 C196,24 182,17 160,15 C140,13 128,13 120,14 C116,3 110,-26 103,-40 C100,-22 96,-4 88,14 C66,16 46,20 30,26 C20,29 14,30 10,30 C6,24 2,18 -6,14 C-4,22 0,28 2,34 C0,40 -4,46 -6,54 C2,50 6,44 10,38 C16,38 22,39 30,41 C52,47 74,52 96,52 C104,52 108,53 112,55 C110,62 104,70 98,76 C110,72 122,62 128,54 C150,52 170,48 184,43 C194,40 199,37 200,34 Z';
const ORCA_EYE = 'M150,26 C158,21 170,22 176,25 C168,28 158,29 150,26 Z';
const ORCA_BELLY = 'M120,50 C140,49 165,46 182,42 C170,47 150,51 128,53 Z';
const ORCA_SADDLE = 'M84,16 C76,17 70,18 64,19 C70,22 80,21 88,18 Z';
function orca(x, y, sc = 1, o = {}) {
  const flip = o.flip ? -1 : 1, rot = o.rot || 0, fill = o.fill || '#0b0f14', op = o.opacity === undefined ? 1 : o.opacity;
  const cx = 100;
  const tr = `translate(${x},${y}) rotate(${rot}) scale(${sc * flip},${sc}) translate(${-cx},-30)`;
  let s = `<g transform="${tr}" opacity="${op}"><path d="${o.finPath || ORCA_SIDE}" fill="${fill}" stroke="${o.stroke || 'none'}" stroke-width="${o.sw || 0}"/>`;
  if (!o.plain) s += `<path d="${ORCA_EYE}" fill="#e9eef2"/><path d="${ORCA_BELLY}" fill="#e9eef2" opacity="0.9"/><path d="${ORCA_SADDLE}" fill="#6f7c88" opacity="0.8"/>`;
  return s + '</g>';
}
// Orca, top view (aerial), heading right, ~ 160 x 60
const ORCA_TOP = 'M160,30 C156,20 140,14 118,13 C112,4 100,0 96,2 C100,6 102,10 100,13 C80,14 50,18 28,24 C20,26 14,27 8,27 C4,20 -6,12 -14,12 C-8,20 -4,26 -4,30 C-4,34 -8,40 -14,48 C-6,48 4,40 8,33 C14,33 20,34 28,36 C50,42 80,46 100,47 C102,50 100,54 96,58 C100,60 112,56 118,47 C140,46 156,40 160,30 Z';
function orcaTop(x, y, sc = 1, o = {}) {
  const tr = `translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc}) translate(-80,-30)`;
  return `<g transform="${tr}" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="${ORCA_TOP}" fill="${o.fill || '#0b0f14'}" stroke="${o.stroke || '#cfe6f5'}" stroke-width="${o.sw === undefined ? 1.5 : o.sw}" stroke-opacity="0.5"/></g>`;
}
const DOLPHIN = 'M200,36 C206,33 210,34 214,35 C210,38 204,39 198,39 C180,44 150,48 120,47 C116,54 110,58 102,60 C104,54 106,50 104,46 C80,44 56,40 36,36 C26,34 18,33 12,33 C8,28 2,22 -6,20 C-2,28 0,32 2,35 C0,40 -4,46 -6,50 C2,48 8,42 12,38 C30,36 50,28 80,22 C88,12 96,4 104,0 C104,8 102,14 102,20 C140,20 176,26 200,36 Z';
function dolphin(x, y, sc = 1, o = {}) {
  const flip = o.flip ? -1 : 1;
  return `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc * flip},${sc}) translate(-105,-30)" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="${DOLPHIN}" fill="${o.fill || '#56708a'}"/></g>`;
}
const PORPOISE = 'M150,30 C146,20 128,14 100,14 C96,8 90,4 84,4 C86,8 86,12 84,15 C62,17 40,22 22,26 C16,27 10,28 6,28 C2,22 -2,18 -8,16 C-4,24 -2,28 -2,31 C-2,34 -4,38 -8,46 C-2,44 2,40 6,34 C14,34 22,35 30,37 C60,43 100,46 130,42 C144,40 150,35 150,30 Z';
function porpoise(x, y, sc = 1, o = {}) {
  const flip = o.flip ? -1 : 1;
  return `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc * flip},${sc}) translate(-75,-28)" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="${PORPOISE}" fill="${o.fill || '#8aa0b4'}"/></g>`;
}
const SHARK = 'M210,40 C200,30 180,26 150,25 C138,14 124,0 112,-8 C114,6 116,16 114,24 C90,25 60,28 40,32 C30,30 20,18 8,2 C10,18 14,32 16,40 C12,50 6,62 0,74 C14,64 26,54 38,48 C60,52 90,56 120,56 C124,64 126,70 124,78 C134,70 140,62 142,55 C170,54 196,50 210,40 Z';
function shark(x, y, sc = 1, o = {}) {
  const flip = o.flip ? -1 : 1;
  return `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc * flip},${sc}) translate(-105,-35)" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="${SHARK}" fill="${o.fill || '#1a2430'}"/></g>`;
}
const SEAL = 'M120,30 C118,20 106,14 92,15 C80,15 66,18 50,22 C34,26 18,28 6,26 C0,24 -4,22 -8,22 C-6,28 -4,32 0,34 C-4,38 -8,40 -10,44 C0,44 8,40 14,38 C40,42 70,44 96,42 C110,41 120,38 120,30 Z';
function seal(x, y, sc = 1, o = {}) {
  const flip = o.flip ? -1 : 1;
  return `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc * flip},${sc}) translate(-60,-30)" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="${SEAL}" fill="${o.fill || '#7a8792'}"/><circle cx="112" cy="22" r="13" fill="${o.fill || '#7a8792'}"/><circle cx="116" cy="19" r="2" fill="#111"/><path d="M80,40 L92,50 L70,44 Z" fill="${o.fill || '#7a8792'}"/></g>`;
}
const BLUEWHALE = 'M600,40 C590,28 560,22 520,21 C440,19 330,20 220,24 C214,18 208,14 204,14 C204,18 204,22 202,25 C140,28 80,32 40,36 C30,30 18,20 4,12 C8,24 12,34 14,40 C12,46 8,56 4,68 C18,60 30,50 40,44 C120,50 260,56 400,58 C420,64 430,70 440,76 C438,68 436,62 436,58 C490,56 560,52 590,48 C597,46 600,43 600,40 Z';
function bluewhale(x, y, sc = 1, o = {}) {
  const flip = o.flip ? -1 : 1;
  return `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc * flip},${sc}) translate(-300,-40)" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="${BLUEWHALE}" fill="${o.fill || '#3e5f7c'}"/></g>`;
}
// human swimmer (from below / side), ~ 100 long
function swimmer(x, y, sc = 1, o = {}) {
  const f = o.fill || '#0b0f14';
  return `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc})" opacity="${o.opacity === undefined ? 1 : o.opacity}">
   <circle cx="44" cy="0" r="8" fill="${f}"/><path d="M36,-5 L-6,-4 L-34,-2 L-36,3 L-6,4 L36,5 Z" fill="${f}"/>
   <path d="M30,-4 L62,-14 L64,-10 L32,0 Z M30,4 L58,16 L56,20 L28,8 Z" fill="${f}"/></g>`;
}
// standing diver silhouette, 1 unit = 1 px, height ~ 180 at sc 1
function diver(x, y, sc = 1, o = {}) {
  const f = o.fill || C.ice;
  return `<g transform="translate(${x},${y}) scale(${sc})" opacity="${o.opacity === undefined ? 1 : o.opacity}">
   <circle cx="0" cy="-166" r="13" fill="${f}"/><rect x="-16" y="-150" width="32" height="70" rx="12" fill="${f}"/>
   <rect x="-14" y="-84" width="12" height="74" rx="5" fill="${f}"/><rect x="2" y="-84" width="12" height="74" rx="5" fill="${f}"/>
   <path d="M-16,-12 L-2,-12 L4,0 L-24,0 Z M2,-12 L16,-12 L26,0 L0,0 Z" fill="${f}"/>
   <rect x="-26" y="-146" width="10" height="52" rx="5" fill="${f}"/><rect x="16" y="-146" width="10" height="52" rx="5" fill="${f}"/></g>`;
}
function bus(x, y, w, h, o = {}) {
  const f = o.fill || 'none', st = o.stroke || C.dim;
  let s = `<g opacity="${o.opacity === undefined ? 1 : o.opacity}"><rect x="${x}" y="${y - h}" width="${w}" height="${h * 0.82}" rx="${h * 0.08}" fill="${f}" stroke="${st}" stroke-width="3"/>`;
  for (let i = 0; i < 6; i++) s += `<rect x="${x + w * 0.05 + i * w * 0.155}" y="${y - h * 0.9}" width="${w * 0.12}" height="${h * 0.3}" rx="4" fill="none" stroke="${st}" stroke-width="2" opacity="0.7"/>`;
  s += `<circle cx="${x + w * 0.18}" cy="${y - h * 0.16}" r="${h * 0.14}" fill="${C.navy0}" stroke="${st}" stroke-width="3"/><circle cx="${x + w * 0.8}" cy="${y - h * 0.16}" r="${h * 0.14}" fill="${C.navy0}" stroke="${st}" stroke-width="3"/>`;
  return s + '</g>';
}
// small label chip
function chip(x, y, label, value, t, a, o = {}) {
  const k = eo(t, a, a + 0.6);
  const w = o.w || 320;
  return `<g opacity="${k}" transform="translate(0,${(1 - k) * 18})">
   <rect x="${x}" y="${y}" width="${w}" height="104" rx="14" fill="#0e2942" fill-opacity="0.75" stroke="${o.color || C.ice}" stroke-opacity="0.35"/>
   ${txt(x + 24, y + 38, label, { size: 22, weight: 600, fill: C.dim, anchor: 'start', ls: 3 })}
   ${txt(x + 24, y + 84, value, { size: 40, weight: 800, fill: o.color || C.ink, anchor: 'start' })}</g>`;
}
function kicker(t, a, s, y = 150, o = {}) {
  const k = eo(t, a, a + 0.8);
  return `<g opacity="${k}">${txt(W / 2, y, s, { size: o.size || 26, weight: 700, fill: o.fill || C.ice, ls: 8 })}
   <rect x="${W / 2 - 40 * k}" y="${y + 22}" width="${80 * k}" height="3" fill="${o.fill || C.ice}"/></g>`;
}
function svgWrap(inner, t, o = {}) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${defs()}${inner}</svg>`;
}
