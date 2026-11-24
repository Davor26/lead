// Humpback film graphics (cards, maps, diagrams). Same library and look as the orca and walrus films.
// ---------- silhouettes ----------
const HUMP = 'M300,44 C298,34 286,26 266,24 C230,20 190,20 150,22 C120,23 96,24 80,26 L74,18 C72,16 70,16 68,20 L64,28 C46,32 30,36 18,40 C14,36 8,28 -4,22 C0,32 4,38 6,42 C4,46 0,52 -4,62 C8,56 14,48 18,46 C40,50 80,58 130,62 C180,64 230,62 262,58 C282,56 296,52 300,44 Z';
const HFLIP = 'M0,0 C-8,22 -36,62 -88,90 C-96,95 -94,100 -86,97 C-36,74 -6,38 12,4 Z';
// humpback, side view facing right, ~300 x 80 (origin centre). o.flipRot rotates the flipper (deg), o.belly = upside down
function hump(x, y, sc = 1, o = {}) {
  const f = o.fill || '#2c3e4f', flip = o.flip ? -1 : 1, vy = o.belly ? -1 : 1;
  let s = `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc * flip},${sc * vy}) translate(-150,-42)" opacity="${o.opacity === undefined ? 1 : o.opacity}">`;
  s += `<g transform="translate(226,54) rotate(${(o.flipRot || 0) + 22}) scale(0.8)"><path d="${HFLIP}" fill="${o.finFill || '#cfd9e0'}" stroke="${f}" stroke-width="3"/></g>`;
  s += `<path d="${HUMP}" fill="${f}"/>`;
  s += `<path d="M300,44 C296,52 282,56 262,58 C230,62 190,64 160,62 C190,58 236,54 270,50 C286,48 296,46 300,44 Z" fill="#dfe6ea" opacity="0.85"/>`;
  for (let i = 0; i < 6; i++) s += `<path d="M${292 - i * 14},${50 + i * 1.6} L${200 - i * 6},${58 + i * 0.6}" stroke="#9aa9b4" stroke-width="1.2" opacity="0.6"/>`;
  [[288, 30], [278, 27], [268, 26], [284, 36], [272, 33]].forEach(([a, b]) => s += `<circle cx="${a}" cy="${b}" r="2.2" fill="#56697a"/>`);
  s += `<circle cx="262" cy="44" r="2.6" fill="#0b0f14"/>`;
  if (o.rakes) [0, 1, 2, 3].forEach(i => s += `<path d="M${6 + i * 3},${30 + i * 6} L${14 + i * 3},${30 + i * 6}" stroke="#eef" stroke-width="1.5"/>`);
  return s + '</g>';
}
// humpback, top view heading right, ~170 x 60 plus flippers
function humpTop(x, y, sc = 1, o = {}) {
  const f = o.fill || '#2c3e4f';
  return `<g transform="translate(${x},${y}) rotate(${o.rot || 0}) scale(${sc}) translate(-75,-30)" opacity="${o.opacity === undefined ? 1 : o.opacity}">
   <path d="M108,16 C98,-2 80,-34 64,-52 C80,-44 104,-12 120,14 Z M108,44 C98,62 80,94 64,112 C80,104 104,72 120,46 Z" fill="#cfd9e0" stroke="${f}" stroke-width="3"/>
   <path d="M160,30 C158,18 140,12 110,12 C80,12 50,16 26,22 L6,30 L26,38 C50,44 80,48 110,48 C140,48 158,42 160,30 Z" fill="${f}" stroke="#cfe6f5" stroke-width="1.5" stroke-opacity="0.5"/>
   <path d="M10,30 L-22,2 C-16,16 -14,26 -16,30 C-14,34 -16,44 -22,58 Z" fill="${f}"/></g>`;
}
const SUNFISH = 'M60,30 C60,10 46,0 30,0 C14,0 0,12 0,30 C0,48 14,60 30,60 C46,60 60,50 60,30 Z';
function sunfish(x, y, sc = 1, o = {}) {
  return `<g transform="translate(${x},${y}) scale(${sc}) translate(-30,-30)" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="${SUNFISH}" fill="${o.fill || '#8fa3b3'}"/><path d="M22,2 L18,-34 L34,0 Z M22,58 L18,94 L34,60 Z" fill="${o.fill || '#8fa3b3'}"/><path d="M0,24 C-8,26 -8,34 0,36 Z" fill="${o.fill || '#8fa3b3'}"/><circle cx="46" cy="24" r="3" fill="#111"/></g>`;
}
function floe(x, y, w, o = {}) {
  const h = w * 0.16;
  return `<g opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="M${x - w / 2},${y} L${x - w * 0.44},${y - h} L${x - w * 0.1},${y - h * 1.15} L${x + w * 0.3},${y - h * 1.05} L${x + w / 2},${y - h * 0.3} L${x + w * 0.48},${y} Z" fill="#e9f3f8"/>
   <path d="M${x - w / 2},${y} L${x + w * 0.48},${y} L${x + w * 0.44},${y + h * 0.9} L${x - w * 0.42},${y + h * 0.8} Z" fill="#7fb6d3" opacity="0.55"/></g>`;
}
function waterline(t, y, o = {}) {
  let d = `M0,${y}`;
  for (let x = 0; x <= W; x += 40) d += ` L${x},${(y + Math.sin(x / 90 + t * 1.6) * (o.amp || 5)).toFixed(1)}`;
  return `<path d="${d} L${W},${H} L0,${H} Z" fill="${o.fill || '#0b2a44'}" opacity="${o.op || 0.85}"/><path d="${d}" fill="none" stroke="#9fd8ff" stroke-width="2" opacity="0.5"/>`;
}
function fin(x, y, sc = 1, o = {}) { // orca dorsal fin above the waterline
  return `<path transform="translate(${x},${y}) scale(${sc * (o.flip ? -1 : 1)},${sc})" d="M-18,0 C-14,-20 -6,-50 2,-80 C6,-50 12,-20 22,0 Z" fill="#0b0f14" opacity="${o.opacity === undefined ? 1 : o.opacity}"/>`;
}
function rings(x, y, t, a, o = {}) {
  let s = '';
  for (let i = 0; i < (o.n || 4); i++) {
    const ph = ((t - a) / (o.period || 1.6) + i / (o.n || 4)) % 1;
    if (t < a) continue;
    s += `<circle cx="${x}" cy="${y}" r="${(o.r0 || 30) + ph * (o.r1 || 260)}" fill="none" stroke="${o.color || C.ice}" stroke-width="${o.sw || 3}" opacity="${(1 - ph) * (o.op || 0.7)}"/>`;
  }
  return s;
}
function bigCard(t, D, kick, big, small, o = {}) {
  let s = kicker(t, 0.1, kick, 300, { fill: o.kfill || C.ice });
  const k = eo(t, 0.5, 1.4);
  s += `<g opacity="${k}" transform="translate(0,${(1 - k) * 20})">${txt(W / 2, 560, big, { size: o.size || 120, weight: 800, fill: o.color || C.ink, ls: 2 })}</g>`;
  if (small) s += rise(t, 1.4, W / 2, 660, small, { size: 36, weight: 600, fill: C.dim, ls: 3 });
  return s;
}
G.card = { render(t, D, p) { return full(t, D, bigCard(t, D, p.kick, p.big, p.small, { size: p.size, color: p.color, kfill: p.kfill })); } };

// ---------- 1: the wave-wash rescue (stage 1: fins circle; 2: wave; 3: seal in the water) ----------
G.wash = { render(t, D, p) {
  const st = p.stage || 1, wy = 640;
  let s = `<rect width="${W}" height="${H}" fill="#0a1f33"/><rect width="${W}" height="${wy}" fill="#5b7387" opacity="0.55"/>`;
  s += `<rect x="0" y="${wy - 90}" width="${W}" height="90" fill="#8ea3b2" opacity="0.25"/>`;
  const fx = 960, k2 = st === 2 ? eio(t, 2.0, 5.0) : st > 2 ? 1 : 0;
  // floe tilts under the wave
  const tilt = st === 2 ? Math.sin(Math.PI * seg(t, 3.2, 6.0)) * -7 : 0;
  s += `<g transform="rotate(${tilt},${fx},${wy})">${floe(fx, wy, 520)}`;
  if (st < 2 || (st === 2 && t < 4.0)) s += seal(fx + (st === 2 ? lerp(0, -150, eio(t, 3.4, 4.0)) : 0), wy - 96, 1.2, { fill: '#6f7c87' });
  s += '</g>';
  // wave
  if (st === 2) {
    const wx = lerp(W + 300, -400, eio(t, 2.4, 6.2)), amp = 120 * Math.sin(Math.PI * seg(t, 2.4, 6.2));
    s += `<path d="M${wx - 500},${wy} C${wx - 250},${wy} ${wx - 120},${wy - amp} ${wx},${wy - amp} C${wx + 160},${wy - amp} ${wx + 260},${wy} ${wx + 500},${wy} L${wx + 500},${H} L${wx - 500},${H} Z" fill="#123b5c" opacity="0.95"/>`;
    s += `<path d="M${wx - 80},${wy - amp} C${wx - 20},${wy - amp - 20} ${wx + 40},${wy - amp - 10} ${wx + 80},${wy - amp + 10}" stroke="#e9f3f8" stroke-width="6" fill="none" opacity="${seg(amp, 20, 100)}"/>`;
  }
  s += waterline(t, wy);
  // orca fins
  const n = 4;
  for (let i = 0; i < n; i++) {
    let x, y = wy + 4, op = 1;
    if (st === 1) { const a = t * 0.35 + i * (Math.PI * 2 / n); x = fx + Math.cos(a) * 620; op = 0.55 + 0.45 * Math.sin(a + 1.2); }
    else if (st === 2) { x = lerp(1500 + i * 70, 1300 + i * 70, eio(t, 0, 2.0)); y = wy + 4 + 90 * eio(t, 1.8, 2.6); }
    else { x = 300 + i * 180 + Math.sin(t * 0.5 + i) * 30; op = 0.9; }
    s += fin(x, y, 1.1, { opacity: op, flip: st === 1 && Math.sin(t * 0.35 + i * (Math.PI * 2 / n)) > 0 });
  }
  if (st === 3) s += seal(fx - 160 + t * 12, wy + 120, 1.2, { fill: '#6f7c87', rot: -8, opacity: eo(t, 0, 0.6) });
  if (st === 1) s += rise(t, 1.2, W / 2, 150, 'ANTARCTICA · 2009', { size: 40, weight: 800, ls: 10, fill: C.ink });
  if (st === 2) s += rise(t, 0.5, W / 2, 150, 'THE WAVE WASH', { size: 34, weight: 800, ls: 10, fill: C.ice });
  return full(t, D, s);
}};
// ---------- 4/5/36: humpback on its back, seal on its chest ----------
G.chest = { render(t, D, p) {
  const st = p.stage || 1, wy = 600, z = p.wide ? 1.0 : 1.25;
  let s = `<rect width="${W}" height="${H}" fill="#0a1f33"/><rect width="${W}" height="${wy}" fill="#5b7387" opacity="0.55"/>`;
  s += `<g transform="translate(${W / 2},${wy}) scale(${z}) translate(${-W / 2},${-wy})">`;
  s += floe(1620, wy + 4, 300, { opacity: 0.95 });
  const bob = Math.sin(t * 1.1) * 4;
  // flipper nudge in stage 2
  const nudge = st === 2 ? Math.sin(Math.PI * seg(t, 1.0, 2.6)) * 28 : 0;
  s += hump(900, wy + 70 + bob, 2.6, { belly: true, flipRot: -nudge, fill: '#2c3e4f' });
  // seal on the chest; in stage 2 it slips, is lifted back, then swims to the floe
  let sx = 1070, sy = wy - 22 + bob, sr = 0, sop = 1;
  if (st === 2) {
    const slip = Math.sin(Math.PI * seg(t, 0.2, 2.6));
    sx += slip * 50; sy += slip * 20; sr = slip * 14;
    const go = eio(t, 3.2, 6.0); sx = lerp(sx, 1600, go); sy = lerp(sy, wy - 70, go) + Math.sin(Math.PI * go) * 60;
  }
  s += seal(sx, sy, 1.6, { fill: '#8a97a2', rot: sr, opacity: sop });
  s += '</g>';
  s += waterline(t, wy + 24, { op: 0.42 });
  if (st === 3) s += rings(900, wy - 10, t, 0.4, { color: C.ice, r1: 420, op: 0.5 });
  if (st === 1) s += rise(t, 0.8, W / 2, 150, 'A HUMPBACK ROLLS ONTO ITS BACK', { size: 32, weight: 800, ls: 8, fill: C.ice });
  if (st === 2) s += rise(t, 3.4, W / 2, 150, 'THE SEAL ESCAPES', { size: 32, weight: 800, ls: 8, fill: C.ice });
  return full(t, D, s);
}};
// ---------- 9: title overlay ----------
G.htitle = { alpha: true, render(t, D) {
  const k = eo(t, 0.2, 1.4);
  let s = `<rect width="${W}" height="${H}" fill="#000" opacity="${0.45 * k}"/>`;
  s += `<g opacity="${k}">${txt(W / 2, 470, 'WHY HUMPBACK WHALES', { size: 104, weight: 800, ls: 4 })}${txt(W / 2, 600, 'SAVE OTHER ANIMALS FROM ORCAS', { size: 84, weight: 800, ls: 3, fill: C.ice })}</g>`;
  s += `<rect x="${W / 2 - 120 * k}" y="650" width="${240 * k}" height="4" fill="${C.ice}"/>`;
  return s;
}};
// ---------- 11: size comparison ----------
G.hsize = { render(t, D) {
  let s = kicker(t, 0.1, 'SIZE MATTERS', 130);
  const base = 780, px = 92, x0 = 150, k0 = eo(t, 0.3, 1.2);
  s += `<line x1="${x0}" y1="${base + 20}" x2="${x0 + 17 * px * k0}" y2="${base + 20}" stroke="${C.faint}" stroke-width="2"/>`;
  for (let m = 0; m <= 17; m++) if (m / 17 <= k0) s += `<line x1="${x0 + m * px}" y1="${base + 12}" x2="${x0 + m * px}" y2="${base + 28}" stroke="${C.faint}" stroke-width="2"/>` + (m % 2 === 0 ? txt(x0 + m * px, base + 62, m + ' m', { size: 22, weight: 500, fill: C.faint }) : '');
  s += hump(x0 + 7.5 * px, base - 0.9 * px, 15 * px / 300, { opacity: eo(t, 0.8, 1.6) });
  s += txt(x0 + 7.5 * px, base - 2.9 * px, 'HUMPBACK · ~15 m · 30+ t', { size: 30, weight: 800, fill: C.ice, ls: 4, opacity: eo(t, 1.0, 1.8) });
  s += orca(x0 + 4.5 * px, base - 4.9 * px, 8 * px / 200, { opacity: eo(t, 2.0, 2.8) });
  s += txt(x0 + 9.2 * px, base - 4.7 * px, 'ORCA · up to ~9 m · ~6 t', { size: 28, weight: 800, anchor: 'start', fill: C.ink, ls: 4, opacity: eo(t, 2.2, 3.0) });
  s += diver(x0 + 16.4 * px, base, 1.8 * px / 180, { fill: C.warm, opacity: eo(t, 3.0, 3.8) });
  s += txt(x0 + 16.4 * px, base - 2.2 * px, 'HUMAN', { size: 26, weight: 800, fill: C.warm, ls: 4, opacity: eo(t, 3.2, 4.0) });
  return full(t, D, s);
}};
// ---------- 12: the flipper ----------
G.flipper = { render(t, D) {
  let s = kicker(t, 0.1, 'MEGAPTERA · "BIG WINGS"', 130);
  s += hump(960, 520, 4.4, { opacity: eo(t, 0.3, 1.2), flipRot: Math.sin(t * 0.8) * 4 });
  const k = eo(t, 1.6, 2.6);
  // highlight the flipper: approx from shoulder (226,54) to tip (-90,95) in local coords
  const X = v => 960 + (v - 150) * 4.4, Y = v => 520 + (v - 42) * 4.4;
  s += `<line x1="${X(226)}" y1="${Y(54) + 40}" x2="${lerp(X(226), X(126), k)}" y2="${lerp(Y(54) + 40, Y(100) + 40, k)}" stroke="${C.warm}" stroke-width="5" stroke-dasharray="14 10"/>`;
  s += rise(t, 2.6, X(150), Y(100) + 120, 'FLIPPER: UP TO ~5 m', { size: 40, weight: 800, fill: C.warm, ls: 3 });
  s += rise(t, 3.4, X(150), Y(100) + 170, 'almost a third of its body', { size: 30, weight: 500, fill: C.dim });
  return full(t, D, s);
}};
// ---------- 22: echolocation ----------
G.echo = { render(t, D) {
  let s = kicker(t, 0.1, 'ECHOLOCATION', 130);
  s += orca(560, 560, 3.2, { opacity: eo(t, 0.2, 1.0) });
  for (let i = 0; i < 6; i++) {
    const ph = ((t - 1.0) / 1.4 + i / 6) % 1; if (t < 1.0) continue;
    const r = 60 + ph * 900;
    s += `<path d="M${880 + r * 0.2},${470 - r * 0.45} A${r} ${r} 0 0 1 ${880 + r * 0.2},${470 + r * 0.45}" fill="none" stroke="${C.ice}" stroke-width="4" opacity="${(1 - ph) * 0.8}"/>`;
  }
  s += seal(1560, 480, 1.4, { fill: '#6f7c87', opacity: eo(t, 2.0, 2.8) });
  for (let i = 0; i < 4; i++) {
    const ph = ((t - 2.6) / 1.4 + i / 4) % 1; if (t < 2.6) continue;
    const r = 30 + ph * 500;
    s += `<path d="M${1500 - r * 0.2},${470 - r * 0.4} A${r} ${r} 0 0 0 ${1500 - r * 0.2},${470 + r * 0.4}" fill="none" stroke="${C.warm}" stroke-width="3" opacity="${(1 - ph) * 0.6}"/>`;
  }
  s += rise(t, 3.0, W / 2, 940, 'clicks out · echoes back', { size: 34, weight: 600, fill: C.dim });
  return full(t, D, s);
}};
// ---------- maps ----------
function rmap(name, o = {}) {
  const m = MAPS[name], sc = o.sc || 1, ox = o.x || 0, oy = o.y || 0;
  return `<g transform="translate(${ox},${oy}) scale(${sc})"><path d="${m.d}" fill="${o.land || '#24384a'}" stroke="#7aa6c4" stroke-width="${1.2 / sc}" stroke-opacity=".7"/></g>`;
}
function rp(name, lon, lat, o = {}) {
  const m = MAPS[name], sc = o.sc || 1, ox = o.x || 0, oy = o.y || 0;
  return [ox + (lon - m.bbox[0]) / (m.bbox[1] - m.bbox[0]) * m.size[0] * sc, oy + (m.bbox[3] - lat) / (m.bbox[3] - m.bbox[2]) * m.size[1] * sc];
}
function pin(x, y, t, a, label, o = {}) {
  const k = eo(t, a, a + 0.6);
  let s = `<circle cx="${x}" cy="${y}" r="${10 * k}" fill="${o.color || C.warm}"/>`;
  if (t > a) { const ph = ((t - a) / 2) % 1; s += `<circle cx="${x}" cy="${y}" r="${10 + 30 * ph}" fill="none" stroke="${o.color || C.warm}" stroke-width="2" opacity="${(1 - ph) * k}"/>`; }
  if (label) s += txt(x + (o.dx === undefined ? 24 : o.dx), y + (o.dy || 10), label, { size: o.size || 34, weight: 800, anchor: o.anchor || 'start', fill: C.ink, opacity: k, ls: 2 });
  return s;
}
function mapFrame(t, D, name, o, inner) {
  const m = MAPS[name], sc = o.sc, z = 1 + 0.06 * eio(t, 0, D);
  let s = `<rect width="${W}" height="${H}" fill="#061a2b"/>`;
  s += `<g transform="translate(${W / 2},${H / 2}) scale(${z}) translate(${-W / 2},${-H / 2})">${rmap(name, o)}${inner}</g>`;
  return s;
}
G.npac = { render(t, D) {
  const o = { sc: 1.1, x: 80, y: -330 };
  let inner = '';
  const P1 = rp('npac', -123, 48.5, o), P2 = rp('npac', -152, 58.5, o), P3 = rp('npac', -122, 36.8, o);
  inner += pin(P1[0], P1[1], t, 1.0, 'FISH-EATERS', { color: C.ice, dx: 28 });
  inner += pin(P2[0], P2[1], t, 2.2, 'MAMMAL HUNTERS', { color: C.warm, dx: -28, anchor: 'end' });
  inner += pin(P3[0], P3[1], t, 3.2, 'MAMMAL HUNTERS', { color: C.warm, dx: 28 });
  let s = mapFrame(t, D, 'npac', o, inner);
  s += kicker(t, 0.1, 'NORTH PACIFIC · TWO KINDS OF KILLER WHALE', 110);
  return full(t, D, s);
}};
G.antpen = { render(t, D) {
  const o = { sc: 0.62, x: 460, y: -20 };
  const [x, y] = rp('antpen', -64.0, -64.8, o);
  let s = mapFrame(t, D, 'antpen', o, pin(x, y, t, 1.0, 'ANTARCTIC PENINSULA · 2009', { dx: 28 }));
  s += kicker(t, 0.1, 'SOUTHERN OCEAN', 110);
  return full(t, D, s);
}};
G.monterey = { render(t, D, p) {
  const o = { sc: 1.0, x: 160, y: -60 };
  let inner = '';
  if (p.canyon) {
    // Monterey Canyon (approx. axis) and the migration route along the coast
    const pts = [[-121.84, 36.80], [-121.95, 36.78], [-122.05, 36.74], [-122.15, 36.70], [-122.30, 36.66], [-122.50, 36.60], [-122.75, 36.55]].map(([a, b]) => rp('monterey', a, b, o));
    const k = eo(t, 0.6, 2.4), n = Math.max(2, Math.ceil(pts.length * k));
    inner += `<polyline points="${pts.slice(0, n).map(q => q.join(',')).join(' ')}" fill="none" stroke="#123b5c" stroke-width="46" stroke-linecap="round" opacity="0.9"/>`;
    inner += `<polyline points="${pts.slice(0, n).map(q => q.join(',')).join(' ')}" fill="none" stroke="${C.ice}" stroke-width="3" stroke-dasharray="10 8"/>`;
    const [cx, cy] = rp('monterey', -122.35, 36.55, o);
    inner += txt(cx, cy + 70, 'MONTEREY CANYON', { size: 30, weight: 800, fill: C.ice, ls: 6, opacity: eo(t, 2.0, 2.8) });
    const r = [[-122.95, 36.35], [-122.4, 36.62], [-122.2, 36.9], [-122.6, 37.18]].map(([a, b]) => rp('monterey', a, b, o));
    const k2 = eo(t, 2.6, 4.6);
    inner += `<path d="M${r[0]} C${r[1]} ${r[2]} ${r[3]}" fill="none" stroke="${C.warm}" stroke-width="6" stroke-dasharray="${1400 * k2} 2000" marker-end="none"/>`;
    inner += txt(r[0][0] + 20, r[0][1] - 30, 'GRAY WHALES HEADING NORTH', { size: 26, weight: 800, fill: C.warm, anchor: 'start', ls: 3, opacity: eo(t, 3.0, 3.8) });
  } else {
    const [x, y] = rp('monterey', -121.95, 36.8, o);
    inner += pin(x, y, t, 1.0, 'MONTEREY BAY', { dx: -28, anchor: 'end' });
  }
  let s = mapFrame(t, D, 'monterey', o, inner);
  s += kicker(t, 0.1, p.canyon ? 'A DEEP CANYON CLOSE TO SHORE' : 'CALIFORNIA · MAY 2012', 110);
  return full(t, D, s);
}};
G.wa = { render(t, D) {
  const o = { sc: 0.62, x: 520, y: 40 };
  const r = [[112.5, -34.5], [111.8, -30], [112.6, -25], [114.5, -20.5], [121.5, -16]].map(([a, b]) => rp('wa', a, b, o));
  const k = eo(t, 0.8, 3.4), n = Math.max(2, Math.ceil(r.length * k));
  let inner = `<polyline points="${r.slice(0, n).map(q => q.join(',')).join(' ')}" fill="none" stroke="${C.warm}" stroke-width="6" stroke-dasharray="14 10"/>`;
  inner += txt(r[1][0] - 30, r[1][1], 'HUMPBACK MIGRATION', { size: 28, weight: 800, anchor: 'end', fill: C.warm, ls: 3, opacity: eo(t, 1.6, 2.4) });
  const [bx, by] = rp('wa', 114.2, -21.8, o);
  inner += pin(bx, by, t, 3.0, '', { color: C.red }) + txt(bx - 30, by + 60, 'ORCAS FOLLOW MOTHERS AND CALVES', { size: 26, weight: 800, anchor: 'end', fill: C.ink, opacity: eo(t, 3.2, 4.0), ls: 2 });
  let s = mapFrame(t, D, 'wa', o, inner);
  s += kicker(t, 0.1, 'WESTERN AUSTRALIA', 110);
  return full(t, D, s);
}};
// world map with report points: p.mode = 'fill' | 'oceans' | 'new'
const REPORTS = [[-122, 37], [-124, 48], [-135, 57], [-150, 59], [-160, 55], [-117, 32], [-110, 23], [-106, 20], [-70, 42], [-66, 44], [-20, 65], [-64, -64], [-62, -63], [-60, -66], [-75, -68], [150, -36], [115, -22], [114, -32], [-80, 0], [-30, -20], [20, -34], [-155, 20], [140, 35]];
G.reports = { render(t, D, p) {
  const m = MAPS.world, sc = 1600 / m.size[0], ox = 160, oy = 230;
  const P = (lon, lat) => [ox + (lon - m.bbox[0]) / (m.bbox[1] - m.bbox[0]) * 1600, oy + (m.bbox[3] - lat) / (m.bbox[3] - m.bbox[2]) * m.size[1] * sc];
  let s = `<g transform="translate(${ox},${oy}) scale(${sc})"><path d="${m.d}" fill="#1d3a52" stroke="#5d86a6" stroke-width="0.8" stroke-opacity="0.6"/></g>`;
  const mode = p.mode || 'fill';
  REPORTS.forEach(([lo, la], i) => {
    const [x, y] = P(lo, la), a = mode === 'new' ? 0.3 : 0.8 + i * 0.22, k = eo(t, a, a + 0.5);
    s += `<circle cx="${x}" cy="${y}" r="${8 * k}" fill="${mode === 'new' ? C.faint : C.warm}" opacity="${k}"/>`;
  });
  if (mode === 'oceans') [['PACIFIC', -150, 15, 1.0], ['ATLANTIC', -40, 30, 1.8], ['SOUTHERN OCEAN', 0, -60, 2.6]].forEach(([n, lo, la, a]) => { const [x, y] = P(lo, la); s += rise(t, a, x, y, n, { size: 30, weight: 800, ls: 8, fill: C.ice }); });
  if (mode === 'new') [[-140, 58], [-128, 51], [-112, 25], [-58, -62], [-66, -65], [-158, 57], [-120, 34], [152, -30]].forEach(([lo, la], i) => {
    const [x, y] = P(lo, la), a = 1.0 + i * 0.5, k = eo(t, a, a + 0.5);
    s += `<circle cx="${x}" cy="${y}" r="${9 * k}" fill="${C.warm}"/>` + (t > a ? `<circle cx="${x}" cy="${y}" r="${9 + 26 * (((t - a) / 2) % 1)}" fill="none" stroke="${C.warm}" opacity="${1 - (((t - a) / 2) % 1)}"/>` : '');
  });
  s += kicker(t, 0.1, mode === 'new' ? 'NEW REPORTS SINCE 2017' : mode === 'oceans' ? 'THREE OCEANS · AT LEAST TEN PREY SPECIES' : 'REPORTS FROM AROUND THE WORLD', 140);
  return full(t, D, s);
}};
// ---------- 29: two types of orca ----------
G.types = { render(t, D) {
  let s = kicker(t, 0.1, 'SAME SPECIES · DIFFERENT MENUS', 130);
  s += `<line x1="${W / 2}" y1="260" x2="${W / 2}" y2="${260 + 600 * eo(t, 0.3, 1.2)}" stroke="${C.faint}" stroke-width="2"/>`;
  s += orca(480, 420, 2.2, { opacity: eo(t, 0.5, 1.3) }) + orca(1440, 420, 2.2, { opacity: eo(t, 1.6, 2.4) });
  s += rise(t, 0.8, 480, 620, 'FISH-EATERS', { size: 44, weight: 800, fill: C.ice, ls: 4 });
  s += rise(t, 1.9, 1440, 620, 'MAMMAL HUNTERS', { size: 44, weight: 800, fill: C.warm, ls: 4 });
  s += rise(t, 1.1, 480, 680, 'salmon · big noisy families', { size: 28, weight: 500, fill: C.dim });
  s += rise(t, 2.2, 1440, 680, 'seals · sea lions · porpoises · whale calves', { size: 28, weight: 500, fill: C.dim });
  s += rise(t, 2.6, 1440, 730, 'small groups · hunt in silence', { size: 28, weight: 500, fill: C.dim });
  [0, 1, 2].forEach(i => s += `<path transform="translate(${380 + i * 90},${800}) scale(1.2)" d="M0,0 C10,-12 40,-12 52,0 L64,-8 L64,8 L52,0 C40,12 10,12 0,0 Z" fill="#c9a07a" opacity="${eo(t, 1.3 + i * 0.2, 1.8 + i * 0.2)}"/>`);
  s += seal(1300, 810, 0.9, { opacity: eo(t, 2.8, 3.3) }) + seal(1440, 810, 0.9, { fill: '#8a6a50', opacity: eo(t, 3.0, 3.5) }) + porpoise(1590, 810, 0.8, { opacity: eo(t, 3.2, 3.7) });
  return full(t, D, s);
}};
// ---------- top-view hunt scenes ----------
function seaTop(t) {
  let s = `<rect width="${W}" height="${H}" fill="#0b3350"/>`;
  for (let i = 0; i < 26; i++) { const y = (i * 53 + t * 8) % H; s += `<path d="M0,${y} Q${W / 4},${y + 10 * Math.sin(t + i)} ${W / 2},${y} T${W},${y}" stroke="#2b6a92" stroke-width="2" fill="none" opacity="0.35"/>`; }
  return s;
}
G.converge = { render(t, D, p) {
  let s = seaTop(t);
  const cx = 1100, cy = 560;
  s += seal(cx, cy, 0.9, { fill: '#7a8792' });
  for (let i = 0; i < 4; i++) { const a = t * 0.6 + i * Math.PI / 2; s += orcaTop(cx + Math.cos(a) * 200, cy + Math.sin(a) * 140, 0.9, { rot: a * 180 / Math.PI + 90 }); }
  s += rings(cx, cy, t, 0.3, { color: C.warm, r1: 600, op: 0.35, n: 3 });
  const hs = p.n || 3;
  for (let i = 0; i < hs; i++) {
    const k = eio(t, 1.0 + i * 0.6, 4.6 + i * 0.6), sx = [-200, -150, 300][i % 3], sy = [180, 960, -160][i % 3];
    const ex = cx - 420 + i * 160, ey = cy + [-260, 300, -300][i % 3] * 0.8;
    const x = lerp(sx, ex, k), y = lerp(sy, ey, k), rot = Math.atan2(ey - sy, ex - sx) * 180 / Math.PI;
    s += humpTop(x, y, 1.1, { rot });
    if (k < 1) s += `<line x1="${x}" y1="${y}" x2="${ex}" y2="${ey}" stroke="${C.ice}" stroke-width="3" stroke-dasharray="10 10" opacity="0.6"/>`;
  }
  s += kicker(t, 0.1, p.kick || 'HUMPBACKS COME TO THE HUNT', 110);
  return full(t, D, s);
}};
G.mob = { render(t, D) {
  let s = seaTop(t);
  const cx = 960, cy = 580;
  s += `<circle cx="${cx}" cy="${cy}" r="70" fill="#1d4a6a" opacity="0.8"/>`;
  for (let i = 0; i < 5; i++) { const a = i * Math.PI * 2 / 5 + Math.sin(t * 0.4 + i) * 0.1, k = eo(t, 0.6 + i * 0.7, 1.6 + i * 0.7);
    s += humpTop(cx + Math.cos(a) * lerp(900, 230, k), cy + Math.sin(a) * lerp(700, 190, k), 1.0, { rot: a * 180 / Math.PI + 180, opacity: k }); }
  for (let i = 0; i < 3; i++) { const a = -0.6 + i * 0.5, r = 430 + 120 * eio(t, 3.5, 7); s += orcaTop(cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.7, 0.85, { rot: a * 180 / Math.PI }); }
  s += rings(cx - 200, cy - 120, t, 2.0, { color: C.ice, r1: 300, op: 0.45, n: 3 }) + rings(cx + 180, cy + 160, t, 2.8, { color: C.ice, r1: 300, op: 0.45, n: 3 });
  s += kicker(t, 0.1, 'MONTEREY BAY · THE HUMPBACKS ARRIVE', 110);
  return full(t, D, s);
}};
G.escort = { render(t, D) {
  let s = seaTop(t);
  const cx = 860 + t * 14, cy = 560;
  s += humpTop(cx, cy, 1.4, { rot: 0 }) + humpTop(cx + 40, cy - 90, 0.7, { rot: 0 });
  const k = eio(t, 1.0, 4.0);
  s += humpTop(lerp(-300, cx - 60, k), lerp(900, cy + 150, k), 1.4, { rot: lerp(-30, 0, k) });
  for (let i = 0; i < 4; i++) { const a = t * 0.5 + i * Math.PI / 2; s += orcaTop(cx + Math.cos(a) * 470, cy + Math.sin(a) * 330, 0.8, { rot: a * 180 / Math.PI + 90 }); }
  s += txt(cx + 40, cy - 150, 'CALF', { size: 24, weight: 800, fill: C.ink, ls: 4, opacity: eo(t, 0.5, 1.2) });
  s += txt(lerp(-300, cx - 60, k), lerp(900, cy + 150, k) + 110, 'ESCORT', { size: 24, weight: 800, fill: C.ice, ls: 4, opacity: eo(t, 2.5, 3.2) });
  s += kicker(t, 0.1, 'HELP ARRIVES', 110);
  return full(t, D, s);
}};
// ---------- 7: 115 encounters / approach / bars ----------
G.approach = { render(t, D) {
  let s = kicker(t, 0.1, 'WHO APPROACHED WHOM?', 130);
  s += orca(1300, 560, 1.6) + orca(1420, 640, 1.3) + orca(1250, 690, 1.2);
  const k = eio(t, 0.8, 4.0);
  s += hump(lerp(300, 800, k), 600, 1.3);
  s += `<path d="M${lerp(500, 980, k)},600 L${lerp(500, 980, k) + 60},600" stroke="${C.ice}" stroke-width="8"/><path d="M${lerp(500, 980, k) + 60},584 L${lerp(500, 980, k) + 90},600 L${lerp(500, 980, k) + 60},616 Z" fill="${C.ice}"/>`;
  s += rise(t, 3.0, W / 2, 900, 'In most cases: the humpbacks went to the orcas', { size: 36, weight: 700, fill: C.ink });
  return full(t, D, s);
}};
G.bars = { render(t, D) {
  let s = kicker(t, 0.1, 'WHICH ORCAS?  (where the type was known)', 130);
  const k = eio(t, 0.8, 2.6);
  s += txt(320, 460, 'MAMMAL HUNTERS', { size: 34, weight: 800, anchor: 'start', fill: C.warm, ls: 3 });
  s += `<rect x="320" y="490" width="${1200 * 0.95 * k}" height="70" rx="8" fill="url(#warmBar)"/>`;
  s += txt(320, 700, 'FISH-EATERS', { size: 34, weight: 800, anchor: 'start', fill: C.ice, ls: 3 });
  s += `<rect x="320" y="730" width="${1200 * 0.05 * k}" height="70" rx="8" fill="url(#iceBar)"/>`;
  s += rise(t, 2.8, 320 + 1200 * 0.95 + 30, 540, 'almost all', { size: 32, weight: 700, anchor: 'start', fill: C.ink });
  s += rise(t, 3.2, 320 + 1200 * 0.05 + 30, 780, 'very few', { size: 32, weight: 700, anchor: 'start', fill: C.dim });
  return full(t, D, s);
}};
// ---------- 8: prey ----------
G.ninety = { render(t, D) {
  let s = kicker(t, 0.1, 'WHO WAS BEING HUNTED?', 160);
  for (let i = 0; i < 10; i++) {
    const x = 330 + i * 140, y = 520, k = eo(t, 0.6 + i * 0.18, 1.0 + i * 0.18);
    s += i < 9 ? seal(x, y, 0.85, { fill: C.warm, opacity: k }) : hump(x, y, 0.36, { fill: C.ice, opacity: k });
  }
  s += rise(t, 2.8, W / 2, 760, '~9 OUT OF 10', { size: 110, weight: 800, fill: C.warm, ls: 4 });
  s += rise(t, 3.4, W / 2, 840, 'another species', { size: 40, weight: 600, fill: C.ink });
  return full(t, D, s);
}};
G.prey = { render(t, D, p) {
  let s = kicker(t, 0.1, p.kick || 'THE PREY HUMPBACKS DEFENDED', 130);
  const items = [
    [(x, y, k) => seal(x, y, 1.4, { opacity: k }), 'HARBOUR SEAL'],
    [(x, y, k) => seal(x, y, 1.6, { fill: '#8a6a50', opacity: k }), 'SEA LION'],
    [(x, y, k) => seal(x, y, 1.4, { fill: '#5f6a72', opacity: k }), 'WEDDELL SEAL'],
    [(x, y, k) => bluewhale(x, y, 0.42, { fill: '#7a8a96', opacity: k }), 'GRAY WHALE CALF'],
    [(x, y, k) => porpoise(x, y, 1.3, { opacity: k }), 'PORPOISE'],
    [(x, y, k) => sunfish(x, y, 1.3, { opacity: k }), 'OCEAN SUNFISH'],
  ];
  items.forEach(([f, n], i) => {
    const x = 400 + (i % 3) * 560, y = 400 + Math.floor(i / 3) * 330, a = 0.5 + i * (p.fast ? 0.35 : 0.8), k = eo(t, a, a + 0.6);
    s += f(x, y, k) + txt(x, y + 120, n, { size: 28, weight: 800, fill: C.ink, ls: 4, opacity: k });
  });
  return full(t, D, s);
}};
// ---------- 9: scars ----------
G.rake = { render(t, D) {
  let s = kicker(t, 0.1, 'RAKE MARKS', 130);
  // big fluke seen from below
  const k = eo(t, 0.3, 1.3);
  s += `<g opacity="${k}" transform="translate(960,560) scale(3.2)"><path d="M0,60 C-20,30 -80,0 -200,-20 C-190,10 -170,40 -120,60 C-80,72 -30,80 0,110 C30,80 80,72 120,60 C170,40 190,10 200,-20 C80,0 20,30 0,60 Z" fill="#20303e"/>
   <path d="M-180,-6 C-120,14 -60,30 -20,60 C-60,48 -120,40 -160,20 Z" fill="#e9eef2" opacity="0.9"/><path d="M180,-6 C120,14 60,30 20,60 C60,48 120,40 160,20 Z" fill="#e9eef2" opacity="0.9"/></g>`;
  const kr = eo(t, 1.6, 3.0);
  [[560, 520], [1260, 560]].forEach(([x0, y0], j) => { for (let i = 0; i < 4; i++) s += `<line x1="${x0 + i * 26}" y1="${y0 + i * 10}" x2="${x0 + i * 26 + 130 * kr}" y2="${y0 + i * 10 + 60 * kr}" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="${0.9 * kr}"/>`; });
  s += rise(t, 3.2, W / 2, 960, 'parallel scars left by killer whale teeth', { size: 34, weight: 600, fill: C.dim });
  return full(t, D, s);
}};
G.shield = { render(t, D) {
  const wy = 230;
  let s = `<rect width="${W}" height="${H}" fill="#0a3352"/><rect width="${W}" height="${wy}" fill="#5b7387" opacity="0.4"/>`;
  s += waterline(t, wy, { fill: '#0e3d60', op: 0.4 });
  const bob = Math.sin(t * 0.9) * 6;
  s += hump(900, 620 + bob, 2.4, { fill: '#2c3e4f' });
  s += hump(960, 430 + bob, 0.95, { fill: '#3b5266' });
  for (let i = 0; i < 3; i++) { const x = 1580 + Math.sin(t * 0.6 + i * 2) * 60 - i * 40, y = 420 + i * 170; s += orca(x, y, 1.1, { flip: true, opacity: 0.9 }); }
  s += rise(t, 1.0, 960, 140, 'THE CALF STAYS CLOSE, ABOVE ITS MOTHER', { size: 32, weight: 800, fill: C.ink, ls: 6 });
  return full(t, D, s);
}};
// ---------- 10: weapons ----------
G.swing = { render(t, D) {
  let s = kicker(t, 0.1, 'WEAPON 1 · THE FLIPPERS', 130);
  const r = Math.sin(t * 1.4) * 32;
  s += hump(900, 500, 3.6, { flipRot: r });
    // barnacle close-up circle
  const k = eo(t, 2.0, 2.8);
  s += `<g opacity="${k}"><circle cx="1520" cy="740" r="150" fill="#1b2a36" stroke="${C.ice}" stroke-width="3"/>`;
  for (let i = 0; i < 9; i++) { const a = i * 0.7, rr = 30 + (i % 3) * 36; s += `<circle cx="${1520 + Math.cos(a) * rr}" cy="${740 + Math.sin(a) * rr}" r="${16 - (i % 3) * 3}" fill="#d9d2c0" stroke="#8d8676" stroke-width="3"/><circle cx="${1520 + Math.cos(a) * rr}" cy="${740 + Math.sin(a) * rr}" r="5" fill="#57524a"/>`; }
  s += txt(1520, 940, 'BARNACLES', { size: 28, weight: 800, fill: C.ice, ls: 4 }) + '</g>';
  return full(t, D, s);
}};
G.calls = { render(t, D, p) {
  let s = kicker(t, 0.1, p.kick || 'WEAPON 3 · NOISE', 130);
  s += hump(700, 580, 2.2);
  s += rings(720, 560, t, 0.6, { color: C.ice, r1: 900, op: 0.55, n: 5 });
  [[1500, 360], [1650, 760], [200, 880]].forEach(([x, y], i) => { const k = eio(t, 2.4 + i * 0.4, 5.0 + i * 0.4); s += hump(lerp(x + (x > 900 ? 500 : -500), x, k), y, 0.9, { flip: x > 900, opacity: k }); });
  s += rise(t, 1.4, W / 2, 1000, 'trumpeting · bellowing · slapping', { size: 34, weight: 600, fill: C.dim });
  return full(t, D, s);
}};
G.silent = { render(t, D) {
  let s = kicker(t, 0.1, 'MAMMAL HUNTERS: SILENT, THEN LOUD', 130);
  const atk = 3.0;
  for (let i = 0; i < 3; i++) s += orca(600 + i * 200, 520 + (i % 2) * 90, 1.3, { opacity: 1 });
  s += txt(800, 380, t < atk ? '. . .' : 'ATTACK', { size: 46, weight: 800, fill: t < atk ? C.faint : C.red, ls: 8 });
  s += rings(800, 560, t, atk, { color: C.red, r1: 1100, op: 0.6, n: 5 });
  const k = eo(t, atk + 1.2, atk + 2.2);
  s += hump(1640, 620, 1.1, { flip: true, opacity: 0.9 });
  s += txt(1640, 760, 'a humpback hears it', { size: 28, weight: 700, fill: C.ice, opacity: k });
  return full(t, D, s);
}};
G.decide = { render(t, D) {
  let s = kicker(t, 0.1, 'A SIMPLE RULE', 130);
  const box = (x, y, w, h, tt, col, a) => { const k = eo(t, a, a + 0.6); return `<g opacity="${k}"><rect x="${x - w / 2}" y="${y - h / 2}" width="${w}" height="${h}" rx="16" fill="#0e2942" fill-opacity="0.8" stroke="${col}" stroke-width="3"/>${txt(x, y + 12, tt, { size: 32, weight: 800, fill: col, ls: 2 })}</g>`; };
  s += box(960, 290, 640, 100, 'ORCAS ATTACKING NEARBY', C.ink, 0.3);
  s += box(540, 560, 520, 100, 'GO AND INTERFERE', C.ice, 1.2) + box(1380, 560, 520, 100, 'STAY AWAY', C.warm, 2.2);
  const l = (x1, y1, x2, y2, a) => `<line x1="${x1}" y1="${y1}" x2="${lerp(x1, x2, eo(t, a, a + 0.5))}" y2="${lerp(y1, y2, eo(t, a, a + 0.5))}" stroke="${C.faint}" stroke-width="3"/>`;
  s += l(860, 340, 600, 510, 1.0) + l(1060, 340, 1320, 510, 2.0);
  s += rise(t, 3.2, 540, 700, 'cost: a little energy', { size: 30, weight: 600, fill: C.ice });
  s += rise(t, 4.2, 1380, 700, 'risk: losing a calf', { size: 30, weight: 600, fill: C.warm });
  s += rise(t, 5.4, 960, 900, 'the safest bet: go every time', { size: 40, weight: 800, fill: C.ink });
  return full(t, D, s);
}};
// ---------- 12: song spectrogram ----------
G.song = { render(t, D) {
  let s = kicker(t, 0.1, 'HUMPBACK SONG', 130);
  s += `<rect x="160" y="260" width="1600" height="560" rx="10" fill="#04101c" stroke="${C.faint}"/>`;
  for (let i = 0; i < 120; i++) {
    const x = 160 + i * 13.3, ph = i + t * 9, u = Math.floor(ph / 14) % 4, j = ph % 14;
    const f0 = [600, 420, 700, 520][u] - j * [12, -8, 18, 4][u], amp = 0.4 + 0.6 * Math.abs(Math.sin(ph * 0.35));
    if ((ph % 14) > 11) continue;
    s += `<rect x="${x}" y="${f0}" width="10" height="${30 + 40 * amp}" rx="4" fill="${C.ice}" opacity="${0.25 + 0.6 * amp}"/>`;
    s += `<rect x="${x}" y="${f0 + 140}" width="10" height="${12 + 16 * amp}" rx="3" fill="${C.ice}" opacity="${0.15 + 0.3 * amp}"/>`;
  }
  s += txt(140, 290, 'pitch', { size: 22, weight: 500, fill: C.faint, anchor: 'end' }) + txt(1760, 860, 'time →', { size: 22, weight: 500, fill: C.faint, anchor: 'end' });
  s += rise(t, 1.2, W / 2, 960, 'songs change from year to year, and spread between populations', { size: 32, weight: 600, fill: C.dim });
  return full(t, D, s);
}};
// ---------- 13: whaling and recovery ----------
G.popcurve = { render(t, D, p) {
  let s = kicker(t, 0.1, p.rise ? 'THE RETURN' : 'THE WHALING YEARS', 130);
  const x0 = 260, x1 = 1660, y0 = 840, y1 = 280, yr = v => x0 + (v - 1900) / 125 * (x1 - x0);
  s += `<line x1="${x0}" y1="${y0}" x2="${x1}" y2="${y0}" stroke="${C.faint}" stroke-width="2"/>`;
  [1900, 1925, 1950, 1975, 2000, 2025].forEach(v => s += txt(yr(v), y0 + 46, v, { size: 24, weight: 500, fill: C.faint }));
  const curve = v => v < 1966 ? 1 - 0.92 * Math.pow(seg(v, 1905, 1966), 1.3) : 0.08 + 0.75 * Math.pow(seg(v, 1975, 2025), 1.4);
  const endY = p.rise ? 2025 : 1966, start = p.rise ? 1966 : 1900;
  const k = eio(t, 0.5, 4.0);
  let d = '';
  for (let v = 1900; v <= lerp(start, endY, k); v += 1) d += (d ? ' L' : 'M') + `${yr(v)},${y0 - curve(v) * (y0 - y1)}`;
  if (p.rise) { let d0 = ''; for (let v = 1900; v <= 1966; v++) d0 += (d0 ? ' L' : 'M') + `${yr(v)},${y0 - curve(v) * (y0 - y1)}`; s += `<path d="${d0}" fill="none" stroke="${C.red}" stroke-width="5" opacity="0.5"/>`; }
  s += `<path d="${d}" fill="none" stroke="${p.rise ? C.ice : C.red}" stroke-width="6"/>`;
  s += `<line x1="${yr(1966)}" y1="${y1 - 20}" x2="${yr(1966)}" y2="${y0}" stroke="${C.ink}" stroke-dasharray="8 8" opacity="${eo(t, p.rise ? 0.2 : 3.6, p.rise ? 0.8 : 4.2)}"/>`;
  s += txt(yr(1966) + 14, y1, '1966: PROTECTED', { size: 26, weight: 800, anchor: 'start', fill: C.ink, opacity: eo(t, p.rise ? 0.2 : 3.6, p.rise ? 0.8 : 4.2) });
  s += txt(x0 - 20, y1 + 10, 'humpbacks', { size: 22, weight: 500, fill: C.faint, anchor: 'end' });
  if (p.rise) s += chip(1240, 860, 'IUCN', 'LEAST CONCERN', t, 4.0, { w: 420 });
  s += rise(t, 1.0, x1, 220, p.rise ? 'illustrative trend' : 'illustrative trend', { size: 20, weight: 500, anchor: 'end', fill: C.faint });
  return full(t, D, s);
}};
G.photoid = { render(t, D) {
  let s = kicker(t, 0.1, 'EVERY TAIL IS A FINGERPRINT', 130);
  for (let i = 0; i < 8; i++) {
    const x = 300 + (i % 4) * 440, y = 380 + Math.floor(i / 4) * 330, k = eo(t, 0.4 + i * 0.25, 1.0 + i * 0.25);
    s += `<g opacity="${k}" transform="translate(${x},${y}) scale(0.95)"><rect x="-200" y="-120" width="400" height="260" rx="12" fill="#0e2942" stroke="${C.faint}"/>
     <path d="M0,40 C-14,20 -60,0 -150,-14 C-142,8 -126,28 -90,40 C-60,50 -22,56 0,80 C22,56 60,50 90,40 C126,28 142,8 150,-14 C60,0 14,20 0,40 Z" fill="#20303e"/>`;
    for (let j = 0; j < 6; j++) { const sx = Math.sin(i * 7.1 + j * 3.3), sy = Math.cos(i * 4.7 + j * 2.1); s += `<ellipse cx="${sx * 90}" cy="${20 + sy * 16}" rx="${14 + (j % 3) * 8}" ry="${6 + (j % 2) * 4}" fill="#e9eef2" opacity="0.85"/>`; }
    s += txt(-180, 120, `ID ${1040 + i * 37}`, { size: 20, weight: 700, anchor: 'start', fill: C.dim, mono: true }) + '</g>';
  }
  return full(t, D, s);
}};
// ---------- end card ----------
G.endcard = { render(t, D) {
  let s = txt(W / 2, 210, 'NATUREXPLORE', { size: 64, weight: 800, ls: 14, opacity: eo(t, 0.2, 1.2) });
  s += rise(t, 0.8, W / 2, 275, 'A new wildlife documentary every week', { size: 30, weight: 500, fill: C.dim });
  [[300, 'WATCH NEXT'], [1020, 'WATCH NEXT']].forEach(([x, l], i) => {
    const k = eo(t, 1.4 + i * 0.3, 2.2 + i * 0.3);
    s += `<g opacity="${k}"><rect x="${x}" y="380" width="600" height="338" rx="16" fill="#0e2942" fill-opacity="0.55" stroke="${C.ice}" stroke-opacity="0.5" stroke-width="2"/>${txt(x + 300, 560, l, { size: 28, weight: 700, ls: 8, fill: C.dim })}</g>`;
  });
  const k = eo(t, 2.6, 3.4);
  s += `<g opacity="${k}"><circle cx="${W / 2}" cy="880" r="88" fill="none" stroke="${C.ink}" stroke-width="3"/>${txt(W / 2, 892, 'SUBSCRIBE', { size: 24, weight: 800, ls: 4 })}</g>`;
  s += rise(t, 4.0, W / 2, 1030, 'Do the humpbacks know what they are doing? Tell us in the comments.', { size: 28, weight: 600, fill: C.ink });
  return bg(t) + `<g opacity="${envelope(t, D, 0.8, 1.2)}">${s}</g>`;
}};
