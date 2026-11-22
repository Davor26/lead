// Walrus film graphics (cards and diagrams). Same library and look as the orca film.
const WALRUS = 'M300,70 C298,52 284,40 266,38 C250,36 236,42 226,50 C200,34 160,24 120,26 C80,28 46,40 24,58 C10,70 2,84 0,96 C-2,104 6,108 14,104 C24,100 34,100 42,104 C70,116 120,122 170,120 C200,119 222,116 240,110 C252,106 262,100 270,96 C286,92 300,84 300,70 Z';
function walrus(x, y, sc = 1, o = {}) {
  const f = o.fill || '#8a5a40', flip = o.flip ? -1 : 1;
  return `<g transform="translate(${x},${y}) scale(${sc * flip},${sc}) translate(-150,-75)" opacity="${o.opacity === undefined ? 1 : o.opacity}">
   <path d="M206,104 C214,122 210,136 200,146 L222,146 C230,132 232,118 226,106 Z" fill="${f}" opacity=".9"/>
   <path d="${WALRUS}" fill="${f}" stroke="${o.stroke || 'none'}" stroke-width="${o.sw || 0}"/>
   <path d="M268,90 L272,${o.short ? 118 : 146} L279,${o.short ? 118 : 146} L281,90 Z M283,88 L289,${o.short ? 114 : 140} L295,${o.short ? 114 : 138} L293,86 Z" fill="#f2ead8"/>
   <circle cx="276" cy="56" r="2.6" fill="#1a0f0a"/>
   <path d="M282,74 C290,76 298,78 302,76" stroke="#e9dcc4" stroke-width="2" fill="none"/></g>`;
}
const BEAR = 'M0,58 C2,50 12,44 24,42 L34,34 C40,30 46,32 46,38 C56,34 70,32 84,34 C120,26 170,24 210,32 C236,38 254,52 260,70 C264,84 262,100 256,112 L254,150 L236,150 L234,120 C220,124 200,126 186,124 L182,150 L164,150 L164,124 C140,126 120,124 106,120 L102,150 L84,150 L84,114 C76,108 70,100 66,90 C54,88 42,84 32,80 C22,78 10,72 4,66 C0,64 -2,62 0,58 Z';
function bear(x, y, sc = 1, o = {}) {
  const flip = o.flip ? -1 : 1;
  return `<g transform="translate(${x},${y}) scale(${sc * flip},${sc}) translate(-130,-90)" opacity="${o.opacity === undefined ? 1 : o.opacity}">
   <path d="${BEAR}" fill="${o.fill || '#ece6d6'}" stroke="${o.stroke || 'none'}" stroke-width="${o.sw || 0}"/>
   <circle cx="20" cy="50" r="2.4" fill="#111"/><circle cx="2" cy="60" r="3" fill="#111"/></g>`;
}
function clam(x, y, sc = 1, o = {}) {
  return `<g transform="translate(${x},${y}) scale(${sc})" opacity="${o.opacity === undefined ? 1 : o.opacity}"><path d="M-14,4 C-14,-8 -6,-14 0,-14 C6,-14 14,-8 14,4 Z" fill="${o.fill || '#d8cbb2'}"/><path d="M-10,2 L-4,-11 M0,2 L0,-13 M10,2 L4,-11" stroke="#a89a80" stroke-width="1.4"/></g>`;
}
function bigCard(t, D, kick, big, small, o = {}) {
  let s = kicker(t, 0.1, kick, 300, { fill: o.kfill || C.ice });
  const k = eo(t, 0.5, 1.4);
  s += `<g opacity="${k}" transform="translate(0,${(1 - k) * 20})">${txt(W / 2, 560, big, { size: o.size || 120, weight: 800, fill: o.color || C.ink, ls: 2 })}</g>`;
  if (small) s += rise(t, 1.4, W / 2, 660, small, { size: 36, weight: 600, fill: C.dim, ls: 3 });
  return s;
}
// 1 the study
G.study = { render(t, D) { return full(t, D, bigCard(t, D, 'THE STUDY', 'STIRLING, LAIDRE & BORN', 'ARCTIC · 2021', { size: 96 })); } };
// 2 size comparison
G.wsize = { render(t, D) {
  let s = kicker(t, 0.1, 'SIZE MATTERS', 130);
  const base = 760, px = 150, x0 = 200, k0 = eo(t, 0.3, 1.2);
  s += `<line x1="${x0}" y1="${base + 20}" x2="${x0 + 10 * px * k0}" y2="${base + 20}" stroke="${C.faint}" stroke-width="2"/>`;
  for (let m = 0; m <= 10; m++) if (m / 10 <= k0) s += `<line x1="${x0 + m * px}" y1="${base + 12}" x2="${x0 + m * px}" y2="${base + 28}" stroke="${C.faint}" stroke-width="2"/>` + (m % 2 === 0 ? txt(x0 + m * px, base + 62, m + ' m', { size: 22, weight: 500, fill: C.faint }) : '');
  s += walrus(x0 + 1.75 * px, base - 0.58 * px, 3.5 * px / 300, { opacity: eo(t, 0.8, 1.6) });
  s += txt(x0 + 1.75 * px, base - 1.4 * px, 'WALRUS', { size: 30, weight: 800, fill: C.warm, ls: 4, opacity: eo(t, 1.0, 1.8) });
  s += bear(x0 + 5.6 * px, base - 0.62 * px, 2.5 * px / 260, { opacity: eo(t, 1.8, 2.6), flip: true });
  s += txt(x0 + 5.6 * px, base - 1.75 * px, 'POLAR BEAR', { size: 30, weight: 800, fill: C.ink, ls: 4, opacity: eo(t, 2.0, 2.8) });
  s += diver(x0 + 8.4 * px, base, 1.8 * px / 180, { fill: C.ice, opacity: eo(t, 2.8, 3.6) });
  s += txt(x0 + 8.4 * px, base - 1.8 * px - 26, 'HUMAN', { size: 30, weight: 800, fill: C.ice, ls: 4, opacity: eo(t, 3.0, 3.8) });
  return full(t, D, s);
}};
// 3 skin / blubber / muscle cutaway
G.cutaway = { render(t, D) {
  let s = kicker(t, 0.1, 'ARMOUR UNDER THE SKIN', 130);
  const x0 = 360, x1 = 1560, layers = [['SKIN', 70, '#7a4a33'], ['BLUBBER', 220, '#e9d6a8'], ['MUSCLE', 220, '#9a3b32']];
  let y = 300;
  layers.forEach(([n, h, c], i) => { const k = eo(t, 0.6 + i * 0.7, 1.4 + i * 0.7);
    s += `<rect x="${x0}" y="${y}" width="${(x1 - x0) * k}" height="${h}" fill="${c}" opacity="${i === 2 ? 0.85 : 1}"/>`;
    s += txt(x0 - 30, y + h / 2 + 12, n, { size: 34, weight: 800, anchor: 'end', fill: C.ink, opacity: k, ls: 3 }); y += h; });
  // a claw strike that stops in the blubber
  const kc = eo(t, 3.0, 4.2), cy = lerp(160, 470, kc);
  [0, 40, 80].forEach(d => s += `<line x1="${980 + d}" y1="160" x2="${960 + d}" y2="${cy}" stroke="${C.ink}" stroke-width="6" stroke-linecap="round" opacity="${eo(t, 2.8, 3.2)}"/>`);
  s += rise(t, 4.4, 1150, 250, 'claws and teeth stop in the blubber', { size: 30, weight: 600, anchor: 'start', fill: C.warm });
  return full(t, D, s);
}};
// 4 walrus skull
G.skull = { render(t, D) {
  let s = kicker(t, 0.1, 'THE WALRUS SKULL', 130);
  const k = eo(t, 0.4, 1.6);
  s += `<g opacity="${k}" transform="translate(560,300) scale(2.2)">
   <path d="M0,60 C10,20 60,0 130,4 C190,8 240,26 262,56 C276,76 276,100 262,116 C240,132 200,138 160,136 L120,136 C80,134 30,120 10,100 C2,90 -2,76 0,60 Z" fill="#e6dcc6" stroke="#b9ad94" stroke-width="2"/>
   <ellipse cx="200" cy="62" rx="20" ry="16" fill="#2a2420"/><path d="M60,40 C90,30 130,30 160,44" stroke="#b9ad94" stroke-width="3" fill="none"/>
   <path d="M228,112 L240,${112 + 160 * eo(t, 1.4, 2.6)} L256,${112 + 160 * eo(t, 1.4, 2.6)} L254,110 Z" fill="#f4ecd8" stroke="#c8bca2"/></g>`;
  s += rise(t, 2.8, 1260, 820, 'TUSKS: elongated canine teeth', { size: 34, weight: 700, anchor: 'start', fill: C.warm });
  s += rise(t, 3.4, 1260, 870, 'up to a metre long', { size: 28, weight: 500, anchor: 'start', fill: C.dim });
  return full(t, D, s);
}};
// 5 map: Wrangel Island and Point Lay
function regionMap(t, name, o = {}) {
  const m = MAPS[name], sc = o.sc || 1, ox = o.x || 160, oy = o.y || 100;
  return `<g transform="translate(${ox},${oy}) scale(${sc})"><path d="${m.d}" fill="${o.land || '#24384a'}" stroke="#7aa6c4" stroke-width="${1.2 / sc}" stroke-opacity=".7"/></g>`;
}
function mp(name, lon, lat, o = {}) { const m = MAPS[name], sc = o.sc || 1, ox = o.x || 160, oy = o.y || 100;
  return [ox + (lon - m.bbox[0]) / (m.bbox[1] - m.bbox[0]) * m.size[0] * sc, oy + (m.bbox[3] - lat) / (m.bbox[3] - m.bbox[2]) * m.size[1] * sc]; }
G.wrangel = { render(t, D) {
  const z = 1 + 0.08 * eio(t, 0, D);
  let s = `<rect width="${W}" height="${H}" fill="#061a2b"/>`;
  s += `<g transform="translate(${W / 2},${H / 2}) scale(${z}) translate(${-W / 2},${-H / 2})">` + regionMap(t, 'wrangel', { x: 160, y: 150 });
  const [bx, by] = mp('wrangel', 180.55, 70.95, { x: 160, y: 150 });
  s += `<circle cx="${bx}" cy="${by}" r="${10 + 8 * Math.sin(t * 2) ** 2}" fill="none" stroke="${C.warm}" stroke-width="3" opacity="${eo(t, 1.6, 2.4)}"/><circle cx="${bx}" cy="${by}" r="6" fill="${C.warm}" opacity="${eo(t, 1.6, 2.4)}"/></g>`;
  s += `<rect width="${W}" height="${H}" fill="url(#vig)"/>`;
  s += rise(t, 0.5, 140, 140, 'WRANGEL ISLAND', { size: 44, weight: 800, anchor: 'start', ls: 6 });
  s += rise(t, 0.9, 140, 190, 'Russian Arctic · Chukchi Sea', { size: 28, weight: 500, anchor: 'start', fill: C.dim });
  s += rise(t, 2.2, bx + 24, by + 60, 'walrus haul-out beach', { size: 26, weight: 700, anchor: 'start', fill: C.warm });
  return `<g opacity="${envelope(t, D)}">${s}</g>`;
}};
G.chukchi = { render(t, D, p) {
  let s = `<rect width="${W}" height="${H}" fill="#061a2b"/>` + regionMap(t, 'chukchi', { x: 320, y: -60, sc: 0.8 });
  const pts = [[180.6, 71.2, 'Wrangel Island', 0.8], [197.0, 69.74, 'Point Lay, Alaska', 1.6]];
  pts.forEach(([lo, la, n, a]) => { const [x, y] = mp('chukchi', lo, la, { x: 320, y: -60, sc: 0.8 }), k = eo(t, a, a + 0.6), hl = p && p.focus && n.startsWith(p.focus);
    s += `<g opacity="${k * (p && p.focus && !hl ? 0.45 : 1)}"><circle cx="${x}" cy="${y}" r="9" fill="${hl ? C.warm : C.ink}"/>${txt(x + 18, y + 9, n, { size: hl ? 34 : 28, weight: 700, anchor: 'start', fill: hl ? C.warm : C.ink })}</g>`; });
  const [sx, sy] = mp('chukchi', 189, 69.5, { x: 320, y: -60, sc: 0.8 });
  s += txt(sx, sy, 'CHUKCHI SEA', { size: 26, weight: 700, ls: 8, fill: C.dim, opacity: eo(t, 0.4, 1.0) });
  s += `<rect width="${W}" height="${H}" fill="url(#vig)"/>`;
  if (p && p.title) s += rise(t, 2.2, W / 2, 1000, p.title, { size: 44, weight: 800, ls: 3 });
  return `<g opacity="${envelope(t, D)}">${s}</g>`;
}};
// 6 25 attempts -> 2 kills -> both calves
G.attempts = { render(t, D) {
  let s = kicker(t, 0.1, 'ONE SEASON OF OBSERVATIONS', 140);
  for (let i = 0; i < 25; i++) { const r = Math.floor(i / 5), c = i % 5, k = eo(t, 0.4 + i * 0.06, 0.8 + i * 0.06), kill = i === 7 || i === 18;
    const x = 260 + c * 86, y = 330 + r * 86, hl = kill && t > 3.6;
    s += `<circle cx="${x}" cy="${y}" r="30" fill="${hl ? C.red : 'none'}" stroke="${hl ? C.red : C.dim}" stroke-width="3" opacity="${k * (t > 3.6 && !kill ? 0.35 : 1)}"/>`; }
  s += rise(t, 0.6, 470, 800, '25 ATTEMPTS', { size: 54, weight: 800 });
  s += rise(t, 3.6, 1040, 560, '→', { size: 90, weight: 700, fill: C.dim });
  s += rise(t, 3.8, 1330, 470, '2 KILLS', { size: 90, weight: 800, fill: C.red });
  s += rise(t, 6.2, 1330, 620, 'BOTH CALVES', { size: 70, weight: 800, fill: C.warm });
  [0, 1].forEach(i => s += walrus(1240 + i * 180, 720, 0.45, { opacity: eo(t, 6.6 + i * 0.2, 7.2 + i * 0.2), short: true }));
  return full(t, D, s);
}};
// 7 adults 0 / 11
G.adults = { render(t, D) {
  let s = kicker(t, 0.1, 'ADULT WALRUSES KILLED', 160);
  s += `<g opacity="${eo(t, 0.5, 1.4)}">${txt(W / 2, 470, 'ADULTS', { size: 60, weight: 800, ls: 10, fill: C.dim })}${txt(W / 2, 680, '0 / 11', { size: 220, weight: 800 })}</g>`;
  for (let i = 0; i < 11; i++) s += walrus(230 + i * 133, 880, 0.36, { opacity: eo(t, 2.0 + i * 0.1, 2.5 + i * 0.1) });
  s += rise(t, 3.6, W / 2, 1010, 'every adult that was attacked survived', { size: 30, weight: 600, fill: C.ink });
  return full(t, D, s);
}};
// 8 bear wound diagram (no blood: marked zones only)
G.wound = { render(t, D) {
  let s = kicker(t, 0.1, 'WHAT A WALRUS CAN DO TO A BEAR', 140);
  s += bear(W / 2, 560, 3.0, { opacity: eo(t, 0.3, 1.2), flip: true, fill: '#e8e2d2' });
  const zones = [[W / 2 - 240, 470, 'neck'], [W / 2 - 120, 520, 'shoulder'], [W / 2 + 60, 500, 'chest']];
  zones.forEach(([x, y, n], i) => { const k = eo(t, 1.6 + i * 0.6, 2.2 + i * 0.6);
    s += `<circle cx="${x}" cy="${y}" r="${34 * k}" fill="none" stroke="${C.warm}" stroke-width="4" stroke-dasharray="8 6"/>${txt(x, y - 52, n.toUpperCase(), { size: 26, weight: 800, fill: C.warm, opacity: k, ls: 3 })}`; });
  s += rise(t, 3.8, W / 2, 900, 'Tusk wounds can be deep enough to kill the bear', { size: 34, weight: 600 });
  return full(t, D, s);
}};
// 9 ~43% of carcasses = calves
G.carcasses = { render(t, D) {
  let s = kicker(t, 0.1, 'WALRUSES EATEN BY BEARS', 140);
  const k = eio(t, 0.6, 2.6), a = 0.43 * k * Math.PI * 2, cx = 620, cy = 560, r = 250;
  s += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#13324d"/>`;
  s += `<path d="M${cx},${cy} L${cx},${cy - r} A${r},${r} 0 ${a > Math.PI ? 1 : 0},1 ${cx + r * Math.sin(a)},${cy - r * Math.cos(a)} Z" fill="url(#warmBar)"/>`;
  s += `<g opacity="${eo(t, 2.4, 3.2)}">${txt(1180, 560, '~43%', { size: 170, weight: 800, fill: C.warm, anchor: 'start' })}${txt(1190, 630, 'OF CARCASSES WERE CALVES', { size: 32, weight: 700, fill: C.dim, ls: 3, anchor: 'start' })}</g>`;
  return full(t, D, s);
}};
// 10 tongue as a piston (suction feeding)
G.tongue = { render(t, D) {
  let s = kicker(t, 0.1, 'SUCTION FEEDING', 130);
  s += `<rect x="0" y="760" width="${W}" height="320" fill="#5a4a36" opacity=".6"/>`;
  s += `<g transform="translate(520,520) scale(1.9)"><path d="M0,0 C40,-60 160,-70 260,-30 C300,-10 320,20 316,60 C300,90 250,100 200,96 L60,90 C20,80 -6,50 0,0 Z" fill="#8a5a40"/>
    <path d="M240,40 L310,40 L310,72 L240,72 Z" fill="#2b1a14"/></g>`;
  const ph = (t * 1.4) % 2, back = ph < 1 ? easeIO(ph) : 1 - easeIO(ph - 1);
  const tx = 1000 + 60 * (1 - back);
  s += `<rect x="${tx - 140}" y="606" width="140" height="44" rx="20" fill="#d77b7b"/>`;
  s += txt(tx - 70, 590, 'TONGUE', { size: 22, weight: 800, fill: '#ffd3d3', ls: 2 });
  s += `<path d="M${1100},640 L${1180},640" stroke="${C.ice}" stroke-width="6" marker-end="url(#ar)" opacity="${back}"/>`;
  const cx = lerp(1300, 1160, back), cyy = lerp(800, 650, back);
  s += clam(cx, cyy, 2.2);
  s += `<path d="M1220,${700 + 20 * Math.sin(t * 6)} q30,10 60,0" stroke="${C.ice}" stroke-width="4" fill="none" opacity="${back}"/>`;
  s += rise(t, 1.0, 200, 300, 'The tongue pulls back like a piston', { size: 34, weight: 700, anchor: 'start' });
  s += rise(t, 2.0, 200, 350, 'and sucks the clam out of its shell', { size: 34, weight: 700, anchor: 'start', fill: C.ice });
  return full(t, D, s);
}};
// 11 3,000-6,000 clams in one meal
G.clams = { render(t, D) {
  let s = kicker(t, 0.1, 'ONE MEAL', 150);
  const n = Math.round(lerp(0, 6000, eo(t, 0.6, 3.2)));
  s += `<g opacity="${eo(t, 0.4, 1.0)}">${txt(W / 2, 420, '3,000–6,000', { size: 170, weight: 800, fill: C.warm })}${txt(W / 2, 500, 'CLAMS IN ONE MEAL', { size: 40, weight: 800, ls: 8 })}</g>`;
  for (let i = 0; i < 160; i++) { const c = i % 20, r = Math.floor(i / 20); if (i / 160 > n / 6000) break;
    s += clam(240 + c * 76, 600 + r * 50, 1.1, { opacity: 0.85 }); }
  return full(t, D, s);
}};
// 12 ice edge retreating past the shelf
G.iceedge = { render(t, D) {
  let s = kicker(t, 0.1, 'WHERE THE ICE GOES', 120);
  // seabed: shallow shelf on the left, drop-off to the deep basin
  s += `<path d="M0,620 L900,640 C960,650 1000,800 1060,960 L1920,980 L1920,1080 L0,1080 Z" fill="#3e3424"/>`;
  s += `<rect x="0" y="300" width="${W}" height="320" fill="#0b3a5a" opacity=".55"/><rect x="0" y="620" width="${W}" height="460" fill="#06243b" opacity=".6"/>`;
  s += txt(420, 700, 'SHALLOW SHELF · CLAMS', { size: 28, weight: 800, fill: C.warm, ls: 4 });
  s += txt(1450, 1040, 'DEEP BASIN', { size: 28, weight: 800, fill: C.dim, ls: 6 });
  s += `<line x1="960" y1="300" x2="960" y2="660" stroke="${C.dim}" stroke-dasharray="8 8" opacity=".6"/>${txt(960, 290, 'SHELF BREAK', { size: 22, weight: 700, fill: C.dim, ls: 4 })}`;
  // ice edge moves from over the shelf to past the shelf break
  const k = eio(t, 1.5, D - 2.5), edge = lerp(760, 1700, k);
  s += `<path d="M${edge},290 L${W},290 L${W},320 L${edge + 30},322 Z" fill="#e8f3fa"/>`;
  s += txt(edge + 40, 270, 'ICE EDGE', { size: 26, weight: 800, fill: C.ink, ls: 4, anchor: 'start' });
  s += walrus(Math.min(edge + 120, 1820), 270, 0.35, { flip: true, opacity: 0.95 });
  s += rise(t, D - 2.2, W / 2, 210, 'too deep to reach the food', { size: 34, weight: 700, fill: C.warm });
  return full(t, D, s);
}};
// 13-16 statement cards
G.pointlay = { render(t, D) { return full(t, D, bigCard(t, D, 'SEPTEMBER HAUL-OUT', 'POINT LAY, ALASKA', '~35,000 WALRUSES ON ONE BEACH', { size: 110 })); } };
G.trampled = { render(t, D) { return full(t, D, bigCard(t, D, 'WRANGEL ISLAND · 1991', '104 TRAMPLED', 'in a single stampede', { size: 150, color: C.warm })); } };
G.population = { render(t, D) { return full(t, D, bigCard(t, D, 'PACIFIC WALRUS', '~250,000', 'estimated population', { size: 180 })); } };
G.iucn = { render(t, D) {
  let s = kicker(t, 0.1, 'IUCN RED LIST', 220);
  const cats = [['LC', '#4f8a5b'], ['NT', '#8fa64a'], ['VU', '#e0a63a'], ['EN', '#d9672f'], ['CR', '#c0392b']];
  cats.forEach(([c, col], i) => { const x = 560 + i * 170, k = eo(t, 0.4 + i * 0.15, 0.9 + i * 0.15), hl = c === 'VU' && t > 1.8;
    s += `<circle cx="${x}" cy="520" r="${hl ? 74 : 56}" fill="${col}" opacity="${k * (hl ? 1 : 0.45)}" ${hl ? 'filter="url(#glow)"' : ''}/>${txt(x, 538, c, { size: hl ? 52 : 40, weight: 800, opacity: k })}`; });
  s += rise(t, 2.0, W / 2, 740, 'VULNERABLE', { size: 110, weight: 800, fill: '#e0a63a', ls: 8 });
  return full(t, D, s);
}};
// rare scene: a bear throwing a block of ice / a stone
G.throwice = { render(t, D, p) {
  let s = kicker(t, 0.1, p && p.kick || 'A WEAPON', 120);
  s += `<path d="M0,900 L560,900 L700,520 L860,520 L980,900 L1920,900 L1920,1080 L0,1080 Z" fill="#cfdde6"/>`;
  s += bear(780, 430, 1.1, { fill: '#f2ede0' });
  s += walrus(1460, 840, 1.25, { flip: true });
  const k = seg(t, 1.8, 3.6), x = lerp(760, 1420, k), y = lerp(330, 760, k) - Math.sin(k * Math.PI) * 260;
  const lift = eio(t, 0.4, 1.6);
  const bx = k > 0 ? x : 760, by = k > 0 ? y : lerp(420, 300, lift);
  s += `<path d="M${bx - 34},${by - 24} L${bx + 30},${by - 30} L${bx + 38},${by + 22} L${bx - 26},${by + 30} Z" fill="${p && p.stone ? '#7d7a74' : '#e8f6ff'}" stroke="#9cc3da" stroke-width="2"/>`;
  if (k > 0) { let tr = ''; for (let u = 0; u <= k; u += 0.04) { const xx = lerp(760, 1420, u), yy = lerp(330, 760, u) - Math.sin(u * Math.PI) * 260; tr += `${xx},${yy} `; }
    s += `<polyline points="${tr}" fill="none" stroke="${C.warm}" stroke-width="4" stroke-dasharray="10 10" opacity=".8"/>`; }
  s += rise(t, 3.8, W / 2, 1010, p && p.caption || 'aimed at the head', { size: 34, weight: 700 });
  return full(t, D, s);
}};
// film title overlay
G.wtitle = { alpha: true, render(t, D) {
  const k = eo(t, 0.2, 1.8), e = envelope(t, D, 0.01, 0.6);
  let s = `<rect width="${W}" height="${H}" fill="#020a12" opacity="${0.5 * e}"/><g opacity="${e}">`;
  s += txt(W / 2, 400, 'NATUREXPLORE', { size: 26, weight: 700, fill: C.ice, ls: 14, opacity: eo(t, 0.2, 1.2) });
  s += `<g opacity="${k}">` + txt(W / 2, 540, 'WHY POLAR BEARS', { size: 120, weight: 800, ls: 2 + 8 * (1 - k) }) + txt(W / 2, 670, 'THROW ROCKS AT WALRUSES', { size: 92, weight: 800, ls: 2 + 8 * (1 - k) }) + '</g>';
  s += `<rect x="${W / 2 - 160 * eo(t, 1.2, 2.4)}" y="716" width="${320 * eo(t, 1.2, 2.4)}" height="3" fill="${C.ice}"/>`;
  return s + '</g>';
}};
// top-view walrus (oval with tusks) for herd diagrams
function walrusTop(x, y, sc = 1, rot = 0, o = {}) {
  return `<g transform="translate(${x},${y}) rotate(${rot}) scale(${sc})" opacity="${o.opacity === undefined ? 1 : o.opacity}"><ellipse cx="0" cy="0" rx="46" ry="22" fill="${o.fill || '#8a5a40'}"/><circle cx="44" cy="0" r="13" fill="${o.fill || '#8a5a40'}"/>
   <path d="M52,-5 L64,-4 M52,5 L64,4" stroke="#f2ead8" stroke-width="3" stroke-linecap="round"/><path d="M-46,0 L-64,-10 L-62,10 Z" fill="${o.fill || '#7a4c35'}"/></g>`;
}
function bearTop(x, y, sc = 1, rot = 0, o = {}) {
  return `<g transform="translate(${x},${y}) rotate(${rot}) scale(${sc})" opacity="${o.opacity === undefined ? 1 : o.opacity}"><ellipse cx="0" cy="0" rx="40" ry="20" fill="#f0ebde"/><ellipse cx="38" cy="0" rx="16" ry="11" fill="#f0ebde"/><circle cx="52" cy="0" r="3" fill="#111"/>
   <ellipse cx="22" cy="-20" rx="7" ry="5" fill="#e6e0d2"/><ellipse cx="22" cy="20" rx="7" ry="5" fill="#e6e0d2"/><ellipse cx="-24" cy="-20" rx="7" ry="5" fill="#e6e0d2"/><ellipse cx="-24" cy="20" rx="7" ry="5" fill="#e6e0d2"/></g>`;
}
// Svalbard 2015: bear weaving through a sleeping herd (top view); p.touch = paw touch stage
G.svalbard = { render(t, D, p) {
  let s = kicker(t, 0.1, p && p.touch ? 'ONE TOUCH' : 'SVALBARD · JULY 2015', 120);
  s += `<rect x="0" y="220" width="${W}" height="860" fill="#4a4a46" opacity=".55"/>`;
  const herd = [[520, 420, 10], [700, 470, -20], [880, 430, 5], [1060, 500, 30], [1240, 440, -10], [1420, 520, 15], [620, 640, -5], [820, 680, 25], [1010, 700, -15], [1210, 660, 10], [1400, 720, -25], [760, 860, 5], [980, 880, -10], [1180, 860, 20]];
  herd.forEach(([x, y, r], i) => s += walrusTop(x, y, 1.1, r, { opacity: eo(t, 0.2 + i * 0.04, 0.6 + i * 0.04) }));
  if (!(p && p.touch)) {
    const path = [[240, 960], [440, 560], [620, 560], [760, 580], [930, 600], [1110, 590], [1310, 600], [1500, 620], [1700, 520]];
    const k = eio(t, 0.8, D - 1.0) * (path.length - 1), i = Math.min(path.length - 2, Math.floor(k)), f = k - i;
    const bx = lerp(path[i][0], path[i + 1][0], f), by = lerp(path[i][1], path[i + 1][1], f);
    const ang = Math.atan2(path[i + 1][1] - path[i][1], path[i + 1][0] - path[i][0]) * 180 / Math.PI;
    s += `<polyline points="${path.slice(0, i + 1).map(q => q.join(',')).join(' ')} ${bx},${by}" fill="none" stroke="${C.ice}" stroke-width="4" stroke-dasharray="10 10" opacity=".7"/>`;
    s += bearTop(bx, by, 1.3, ang);
    s += bearTop(bx - 70 * Math.cos(ang * Math.PI / 180), by - 70 * Math.sin(ang * Math.PI / 180), 0.75, ang);
    s += rise(t, 1.0, W / 2, 1020, 'sniffing one walrus after another', { size: 32, weight: 600 });
  } else {
    const k = eo(t, 0.6, 1.6), wake = eo(t, 1.8, 2.4), back = eio(t, 2.4, 4.0);
    s += bearTop(820 - 140 * back, 600 + 10 * back, 1.4, 0);
    s += `<circle cx="${905 - 140 * back}" cy="600" r="${22 * k * (1 - back)}" fill="none" stroke="${C.warm}" stroke-width="4"/>`;
    s += txt(1010, 520, '!', { size: 80, weight: 800, fill: C.warm, opacity: wake });
    s += rise(t, 2.6, W / 2, 1020, 'the walrus wakes, the bear backs away', { size: 32, weight: 600 });
  }
  return full(t, D, s);
}};
// GoGo: food hung out of reach, stick thrown
G.gogo = { render(t, D, p) {
  let s = kicker(t, 0.1, 'GOGO · OSAKA, JAPAN', 120);
  s += `<rect x="200" y="880" width="1520" height="20" fill="#9fb3c4" opacity=".6"/><rect x="200" y="300" width="20" height="600" fill="#9fb3c4" opacity=".4"/><rect x="1700" y="300" width="20" height="600" fill="#9fb3c4" opacity=".4"/>`;
  s += `<line x1="1100" y1="220" x2="1100" y2="${p && p.drop ? lerp(380, 380, 0) : 380}" stroke="${C.dim}" stroke-width="3"/>`;
  const drop = p && p.drop ? eio(t, 3.0, 4.0) : 0;
  s += `<g transform="translate(1100,${lerp(410, 840, drop)})"><ellipse cx="0" cy="0" rx="46" ry="30" fill="${C.warm}"/>${txt(0, 10, 'FOOD', { size: 20, weight: 800, fill: '#3a2410' })}</g>`;
  s += bear(760, 790, 1.2, { flip: true });
  if (p && p.drop) {
    const k = seg(t, 1.0, 2.8), x = lerp(820, 1090, k), y = lerp(660, 420, k) - Math.sin(k * Math.PI) * 120;
    s += `<g transform="translate(${x},${y}) rotate(${k * 720})"><rect x="-60" y="-6" width="120" height="12" rx="6" fill="#8a6a44"/></g>`;
    s += rise(t, 0.4, W / 2, 1010, 'he threw sticks and other objects until the food fell', { size: 32, weight: 600 });
  } else s += rise(t, 0.8, W / 2, 1010, 'food hung out of his reach', { size: 32, weight: 600 });
  return full(t, D, s);
}};
// tool users card
G.toolusers = { render(t, D) {
  let s = kicker(t, 0.1, 'ANIMALS THAT USE TOOLS', 150);
  const items = [['CHIMPANZEES', 'sticks to fish for termites'], ['SEA OTTERS', 'stones to crack shells'], ['NEW CALEDONIAN CROWS', 'twigs bent into hooks'], ['POLAR BEARS?', 'ice and stones, against walruses']];
  items.forEach(([a, b], i) => { const y = 330 + i * 150, k = eo(t, 0.6 + i * 0.9, 1.2 + i * 0.9), last = i === 3;
    s += `<g opacity="${k}" transform="translate(${(1 - k) * -30},0)"><rect x="460" y="${y}" width="1000" height="110" rx="14" fill="#0e2942" fill-opacity=".8" stroke="${last ? C.warm : C.faint}" stroke-width="${last ? 3 : 1.5}"/>
     ${txt(500, y + 50, a, { size: 34, weight: 800, anchor: 'start', fill: last ? C.warm : C.ink, ls: 3 })}${txt(500, y + 90, b, { size: 26, weight: 500, anchor: 'start', fill: C.dim })}</g>`; });
  return full(t, D, s);
}};
