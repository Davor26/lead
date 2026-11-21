// Graphic specifications. Each: render(t, D, p) -> inner SVG. alpha: overlay with transparent background.
const G = {};
const full = (t, D, inner, o = {}) => bg(t) + `<g opacity="${envelope(t, D, o.fi || 0.5, o.fo || 0.5)}">${inner}</g>`;

// ---------- 6: 0 CONFIRMED HUMAN DEATHS IN THE WILD ----------
G.zero = { render(t, D) {
  const k = eo(t, 0.3, 1.6);
  let s = `<g opacity="${k}" transform="translate(${W / 2},500) scale(${1.08 - 0.08 * k})">${txt(0, 0, '0', { size: 380, weight: 800, fill: C.ink, extra: ' filter="url(#glow)"' })}</g>`;
  s += rise(t, 1.4, W / 2, 640, 'CONFIRMED HUMAN DEATHS', { size: 64, weight: 800, ls: 6 });
  s += rise(t, 1.9, W / 2, 720, 'IN THE WILD', { size: 64, weight: 800, ls: 6, fill: C.ice });
  s += rise(t, 3.0, W / 2, 820, 'across all of recorded history', { size: 30, weight: 500, fill: C.dim, ls: 1 });
  return full(t, D, s);
}};

// ---------- 7: title (overlay) ----------
G.title = { alpha: true, render(t, D) {
  const k = eo(t, 0.2, 1.8), e = envelope(t, D, 0.01, 0.6);
  let s = `<rect width="${W}" height="${H}" fill="#020a12" opacity="${0.45 * e}"/>`;
  s += `<g opacity="${e}">`;
  s += txt(W / 2, 420, 'NATUREXPLORE', { size: 26, weight: 700, fill: C.ice, ls: 14, opacity: eo(t, 0.2, 1.2) });
  s += `<g opacity="${k}">` + txt(W / 2, 560, 'WHY ORCAS', { size: 150, weight: 800, ls: 4 + 10 * (1 - k) }) + txt(W / 2, 700, "DON'T KILL HUMANS", { size: 104, weight: 800, ls: 4 + 10 * (1 - k), fill: C.ink }) + '</g>';
  s += `<rect x="${W / 2 - 160 * eo(t, 1.2, 2.4)}" y="748" width="${320 * eo(t, 1.2, 2.4)}" height="3" fill="${C.ice}"/>`;
  return s + '</g>';
}};

// ---------- 9: family tree (oceanic dolphins) ----------
G.family = { render(t, D) {
  let s = kicker(t, 0.1, 'THE OCEANIC DOLPHIN FAMILY', 140);
  const rootX = W / 2, rootY = 250;
  s += `<circle cx="${rootX}" cy="${rootY}" r="${8 * eo(t, 0.4, 0.9)}" fill="${C.ice}"/>`;
  const sp = [
    { n: 'Common dolphin', len: 2.2, x: 330 }, { n: 'Bottlenose dolphin', len: 3.2, x: 720 },
    { n: 'Pilot whale', len: 6.5, x: 1140 }, { n: 'ORCA', len: 9.8, x: 1600, hl: true },
  ];
  sp.forEach((q, i) => {
    const a = 0.8 + i * 0.7, k = eo(t, a, a + 0.8);
    const y = 560;
    s += `<path d="M${rootX},${rootY} C${rootX},${rootY + 140} ${q.x},${rootY + 100} ${q.x},${y - 150}" fill="none" stroke="${q.hl ? C.ice : C.faint}" stroke-width="${q.hl ? 4 : 2.5}" stroke-dasharray="1200" stroke-dashoffset="${1200 * (1 - k)}"/>`;
    const sc = q.len / 9.8 * 1.75;
    if (q.hl) s += orca(q.x, y + 20, sc, { opacity: k, fill: '#05080c', stroke: C.ice, sw: 1.2 / sc });
    else s += dolphin(q.x, y + 20, sc * 0.95, { opacity: k, fill: '#5f7a94' });
    s += txt(q.x, y + 190, q.n, { size: q.hl ? 52 : 34, weight: q.hl ? 800 : 600, fill: q.hl ? C.ice : C.ink, opacity: k });
    s += txt(q.x, y + 240, `up to ~${q.len} m`, { size: 26, weight: 500, fill: C.dim, opacity: k });
  });
  s += rise(t, 4.4, W / 2, 960, 'The orca is the largest member of the family', { size: 34, weight: 600, fill: C.ink });
  return full(t, D, s);
}};

// ---------- 10: size ----------
G.size = { render(t, D) {
  let s = kicker(t, 0.1, 'HOW BIG IS AN ORCA?', 130);
  const base = 640, px = 92; // 92 px per metre
  const x0 = 180;
  // scale ruler
  const k0 = eo(t, 0.3, 1.2);
  s += `<line x1="${x0}" y1="${base + 30}" x2="${x0 + 12 * px * k0}" y2="${base + 30}" stroke="${C.faint}" stroke-width="2"/>`;
  for (let m = 0; m <= 12; m++) if (m / 12 <= k0) s += `<line x1="${x0 + m * px}" y1="${base + 22}" x2="${x0 + m * px}" y2="${base + 38}" stroke="${C.faint}" stroke-width="2"/>` + (m % 2 === 0 ? txt(x0 + m * px, base + 70, m + ' m', { size: 22, weight: 500, fill: C.faint }) : '');
  // bus (12 m)
  const kb = eo(t, 0.8, 1.6);
  s += bus(x0, base, 12 * px, 330, { opacity: 0.45 * kb, stroke: C.faint });
  s += txt(x0 + 12 * px - 10, base - 350, 'CITY BUS · 12 m', { size: 22, weight: 600, fill: C.faint, anchor: 'end', opacity: kb, ls: 2 });
  // orca 9.8 m: ORCA_SIDE spans -6..200 (206 units)
  const ko = eo(t, 1.4, 2.4), sc = 9.8 * px / 206;
  s += orca(x0 + 103 * sc + 6 * sc, base - 46 * sc, sc, { opacity: ko, fill: '#05080c', stroke: C.ice, sw: 1.5 / sc });
  // diver 1.8 m
  const kd = eo(t, 2.2, 3.0);
  s += diver(x0 + 11 * px, base, 1.8 * px / 180, { opacity: kd, fill: C.ice });
  s += txt(x0 + 11 * px, base - 1.8 * px - 30, 'DIVER · 1.8 m', { size: 22, weight: 600, fill: C.ice, opacity: kd, ls: 2 });
  s += chip(1440, 280, 'LENGTH', 'up to ~10 m', t, 3.2);
  s += chip(1440, 400, 'WEIGHT', 'up to 10 tonnes', t, 4.2);
  s += chip(180, 820, 'FEMALES LIVE', '80–90 years', t, 5.6, { w: 380 });
  s += chip(600, 820, 'MALES LIVE', '50–60 years', t, 7.2, { w: 380 });
  return full(t, D, s);
}};

// ---------- 11: world map, every ocean ----------
function worldMap(t, o = {}) {
  const m = MAPS.world, sx = o.w || 1600, ox = o.x === undefined ? 160 : o.x, oy = o.y === undefined ? 230 : o.y, sc = sx / m.size[0];
  return `<clipPath id="wclip"><rect x="${ox}" y="${oy}" width="${sx}" height="${m.size[1] * sc}"/></clipPath><g clip-path="url(#wclip)"><g transform="translate(${ox},${oy}) scale(${sc})"><path d="${m.d}" fill="${o.land || '#1d3a52'}" stroke="${o.stroke || '#5d86a6'}" stroke-width="${o.sw || 0.8}" stroke-opacity="${o.so === undefined ? 0.6 : o.so}"/></g></g>`;
}
function ll(lon, lat, o = {}) { // project lon/lat to the world map placement
  const m = MAPS.world, sx = (o.w || 1600) / m.size[0], ox = o.x === undefined ? 160 : o.x, oy = o.y === undefined ? 230 : o.y;
  const [l0, l1, a0, a1] = m.bbox;
  return [ox + (lon - l0) / (l1 - l0) * m.size[0] * sx, oy + (a1 - lat) / (a1 - a0) * m.size[1] * sx];
}
G.world = { render(t, D) {
  let s = kicker(t, 0.1, 'ORCAS LIVE IN EVERY OCEAN', 140);
  // ocean glow sweeping from the poles to the tropics
  const oceans = [['ARCTIC', 0, 78, 1.0], ['SOUTHERN', 20, -55, 1.6], ['PACIFIC', -150, 8, 2.3], ['ATLANTIC', -35, 18, 3.0], ['INDIAN', 78, -18, 3.6], ['PACIFIC', 165, -12, 2.6]];
  let glow = '';
  oceans.forEach(([n, lo, la, a]) => {
    const [x, y] = ll(lo, la), k = eo(t, a, a + 1.4);
    glow += `<circle cx="${x}" cy="${y}" r="${200 * k}" fill="${C.ice}" opacity="${0.13 * k}" filter="url(#soft)"/>`;
  });
  s += `<g opacity="1">${glow}</g>` + worldMap(t);
  oceans.slice(0, 5).forEach(([n, lo, la, a]) => { const [x, y] = ll(lo, la); s += rise(t, a + 0.4, x, y, n, { size: 26, weight: 700, ls: 6, fill: C.ice }); });
  // scattered orca sightings
  const pts = [[-125, 49], [-150, 58], [-63, -42], [18, -34], [114, -34], [174, -40], [-16, 66], [10, 64], [-60, -64], [30, -68], [160, -70], [-8, 36], [-80, 25], [140, 40], [56, 20], [-110, 20], [-30, -30], [80, -50]];
  pts.forEach(([lo, la], i) => { const [x, y] = ll(lo, la), k = eo(t, 4.2 + i * 0.12, 4.6 + i * 0.12); s += `<circle cx="${x}" cy="${y}" r="${7 * k}" fill="${C.ink}" opacity="${k}"/><circle cx="${x}" cy="${y}" r="${7 + 16 * seg((t - 4.2 - i * 0.12) % 2.4, 0, 2.4)}" fill="none" stroke="${C.ink}" opacity="${0.5 * k * (1 - seg((t - 4.2 - i * 0.12) % 2.4, 0, 2.4))}"/>`; });
  s += rise(t, 6.4, W / 2, 1000, 'No natural predators', { size: 34, weight: 600, fill: C.ink });
  return full(t, D, s);
}};

// ---------- 17b: wave-washing diagram ----------
G.wavewash = { render(t, D) {
  let s = kicker(t, 0.1, 'WAVE-WASHING · ANTARCTIC PENINSULA', 130);
  const sea = 600;
  // floe
  const tilt = Math.sin(seg(t, 4.2, 7.5) * Math.PI * 3) * 4 * seg(t, 4.0, 4.6);
  s += `<g transform="rotate(${tilt},1450,${sea})"><path d="M1180,${sea - 30} L1720,${sea - 40} L1740,${sea + 20} L1170,${sea + 26} Z" fill="#dfeef7"/><path d="M1170,${sea + 26} L1740,${sea + 20} L1700,${sea + 90} L1210,${sea + 96} Z" fill="#9cc6df" opacity="0.6"/>`;
  const slide = eio(t, 6.0, 7.6) * 120;
  s += seal(1440 + slide, sea - 52, 1.1, { fill: '#5b6873', flip: true }) + '</g>';
  // water
  s += `<rect x="0" y="${sea}" width="${W}" height="${H - sea}" fill="#0a3657" opacity="0.55"/>`;
  // wave rising and travelling toward the floe
  const wk = seg(t, 3.0, 6.4), wx = lerp(500, 1500, easeIn(wk)), wh = 130 * Math.sin(Math.PI * clamp(wk * 1.05));
  let path = `M0,${sea}`;
  for (let x = 0; x <= W; x += 20) { const d = (x - wx) / 140; path += ` L${x},${(sea - wh * Math.exp(-d * d)).toFixed(1)}`; }
  path += ` L${W},${H} L0,${H} Z`;
  s += `<path d="${path}" fill="#0c4a74" opacity="0.85"/>`;
  s += `<path d="${path.split(' L' + W + ',' + H)[0]}" fill="none" stroke="${C.ice}" stroke-width="3" opacity="0.8"/>`;
  // orcas: line up and charge side by side, then dive
  for (let i = 0; i < 4; i++) {
    const k = seg(t, 1.2, 3.6), dive = eio(t, 3.2, 4.0);
    const x = lerp(160, 900, easeIO(k)) - i * 120, y = sea + 70 + (i % 2) * 34 + dive * 90;
    s += orca(x, y, 0.55, { opacity: eo(t, 0.6 + i * 0.15, 1.2 + i * 0.15), rot: dive * 18, fill: '#06090d', stroke: C.ice, sw: 1 });
  }
  s += rise(t, 0.6, 300, 260, '1   Line up', { size: 34, weight: 700, anchor: 'start', fill: C.ink });
  s += rise(t, 2.0, 300, 310, '2   Charge together', { size: 34, weight: 700, anchor: 'start', fill: C.ink });
  s += rise(t, 3.3, 300, 360, '3   Dive just before impact', { size: 34, weight: 700, anchor: 'start', fill: C.ink });
  s += rise(t, 4.6, 300, 410, '4   The wave keeps going', { size: 34, weight: 700, anchor: 'start', fill: C.ice });
  return full(t, D, s);
}};

// ---------- 18: 15% -> 14 of 15 ----------
G.weddell = { render(t, D) {
  let s = kicker(t, 0.1, 'SEALS ON THE ICE', 120);
  // 100 seals grid, 15 Weddell
  const gx = 170, gy = 240, cw = 76, ch = 56;
  const isW = i => [3, 11, 17, 24, 30, 38, 45, 51, 57, 63, 70, 76, 84, 91, 97].includes(i);
  const k1 = seg(t, 0.6, 2.2), hl = eo(t, 2.6, 3.4);
  for (let i = 0; i < 100; i++) {
    const r = Math.floor(i / 10), c = i % 10, ki = clamp(k1 * 100 - i);
    const w = isW(i);
    s += seal(gx + c * cw + 30, gy + r * ch + 20, 0.42, { fill: w ? (hl > 0 ? `rgba(127,211,255,${0.35 + 0.65 * hl})` : '#6f7f8c') : '#3c4c5a', opacity: ki * (w ? 1 : 1 - 0.45 * hl), flip: r % 2 === 1 });
  }
  s += txt(gx + 5 * cw, gy + 10 * ch + 70, 'Weddell seals: ~15% of seals on the ice', { size: 32, weight: 600, fill: C.ice, opacity: hl });
  // big numbers
  const k2 = eo(t, 5.6, 6.4);
  s += `<g opacity="${eo(t, 2.8, 3.6)}">${txt(1240, 440, '15%', { size: 170, weight: 800, fill: C.ice, anchor: 'start' })}${txt(1250, 500, 'OF THE SEALS', { size: 28, weight: 700, ls: 4, fill: C.dim, anchor: 'start' })}</g>`;
  s += `<g opacity="${k2}">${txt(1240, 560 + 120, '→', { size: 80, weight: 700, fill: C.dim, anchor: 'start' })}${txt(1240, 820, '14 of 15', { size: 150, weight: 800, fill: C.ink, anchor: 'start' })}${txt(1250, 880, 'OF THE KILLS', { size: 28, weight: 700, ls: 4, fill: C.dim, anchor: 'start' })}</g>`;
  // kill dots
  for (let i = 0; i < 15; i++) { const k = eo(t, 6.4 + i * 0.12, 6.8 + i * 0.12); s += `<circle cx="${1250 + i * 34}" cy="920" r="12" fill="${i < 14 ? C.ice : C.faint}" opacity="${k}"/>`; }
  s += rise(t, 9.5, 1250, 990, 'They were choosing.', { size: 36, weight: 700, anchor: 'start', fill: C.ink });
  return full(t, D, s);
}};

// ---------- 20b: beach hunting diagram ----------
G.beach = { render(t, D) {
  let s = kicker(t, 0.1, 'INTENTIONAL STRANDING · PATAGONIA', 130);
  // beach slope
  s += `<path d="M0,820 L760,820 L1920,560 L1920,1080 L0,1080 Z" fill="#c9b48b" opacity="0.85"/>`;
  s += `<path d="M0,820 L760,820 L1920,560" fill="none" stroke="#e6d6b4" stroke-width="3"/>`;
  // sea (left), wave surge
  const surge = Math.sin(Math.PI * seg(t, 1.4, 6.0));
  const wl = 760 + 520 * surge;
  s += `<path d="M0,700 L${wl},${820 - (wl - 760) * 0.224} L${wl},${840} L0,1080 Z" fill="#0c4a74" opacity="0.8"/>`;
  s += `<path d="M0,700 L${wl},${820 - (wl - 760) * 0.224}" stroke="${C.ice}" stroke-width="3" opacity="0.8"/>`;
  // sea lion pups on the shore
  [[1380, 0], [1500, 1], [1610, 0], [1720, 1]].forEach(([x, f], i) => { const y = 820 - (x - 760) * 0.224 - 22; s += seal(x, y, 0.55, { fill: '#6b5440', flip: !!f, opacity: i === 0 ? 1 - seg(t, 4.0, 4.4) : 1 }); });
  // orca rides the wave in, grabs, twists back
  const k = seg(t, 1.6, 7.2), x = k < .5 ? lerp(300, 1330, easeOut(k * 2)) : lerp(1330, 300, easeIn((k - .5) * 2));
  const y = 820 - Math.max(0, x - 760) * 0.224 - 6 + (x < 760 ? 40 : 0);
  s += orca(x, y, 0.95, { flip: k >= .5, rot: k < .5 ? -12 : 12, fill: '#06090d', stroke: C.ice, sw: 1, opacity: eo(t, 0.8, 1.6) });
  s += rise(t, 1.0, 120, 330, 'Ride the wave onto the beach', { size: 34, weight: 700, anchor: 'start' });
  s += rise(t, 3.6, 120, 385, 'Grab a sea lion pup', { size: 34, weight: 700, anchor: 'start' });
  s += rise(t, 5.4, 120, 440, 'Twist back into the sea', { size: 34, weight: 700, anchor: 'start' });
  s += rise(t, 8.0, 120, 520, 'Misjudge the wave, and the orca can be stranded.', { size: 30, weight: 600, anchor: 'start', fill: C.warm });
  return full(t, D, s);
}};

// ---------- 22b: blue whale ----------
G.bluewhale = { render(t, D) {
  let s = kicker(t, 0.1, 'WESTERN AUSTRALIA · 2019–2021', 130);
  s += bluewhale(W / 2, 560, 2.2, { fill: '#365a78', opacity: eo(t, 0.4, 1.4) });
  s += txt(W / 2, 700, 'BLUE WHALE · up to ~30 m', { size: 24, weight: 600, fill: C.dim, ls: 3, opacity: eo(t, 0.8, 1.6) });
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * Math.PI * 2 + t * 0.25, k = eo(t, 1.6 + i * 0.12, 2.4 + i * 0.12);
    const rx = 760, ry = 230, x = W / 2 + Math.cos(a) * rx * (1.4 - 0.4 * k), y = 560 + Math.sin(a) * ry * (1.4 - 0.4 * k);
    s += orca(x, y, 0.42, { flip: Math.cos(a + Math.PI / 2) < 0, fill: '#05080c', stroke: C.ice, sw: 2, opacity: k });
  }
  s += rise(t, 3.6, W / 2, 860, 'A dozen or so orcas hunted it down', { size: 34, weight: 600 });
  const k3 = eo(t, 6.0, 7.0);
  s += `<g opacity="${k3}">${txt(W / 2, 980, '3 BLUE WHALES', { size: 72, weight: 800, fill: C.ice, ls: 6 })}</g>`;
  return full(t, D, s);
}};

// ---------- 23: Port and Starboard ----------
function collapsedFin(x, y, side, k, label) {
  // side: -1 folds left (Port), +1 folds right (Starboard)
  const f = 1 - 0.0 * k;
  const tipX = x + side * 120 * k, tipY = y - 260 + 120 * k;
  return `<path d="M${x - 60},${y} C${x - 40},${y - 120} ${x - 10 * side + side * 40 * k},${y - 220 + 120 * k} ${tipX},${tipY} C${x + side * 40},${y - 150 + 80 * k} ${x + 50},${y - 80} ${x + 70},${y} Z" fill="#06090d" stroke="${C.ice}" stroke-width="2"/>
  <path d="M${x - 200},${y} Q${x},${y - 30} ${x + 200},${y}" fill="#06090d" stroke="${C.ice}" stroke-width="2"/>` + txt(x, y + 80, label, { size: 54, weight: 800, ls: 6 });
}
G.portstar = { render(t, D) {
  let s = kicker(t, 0.1, 'SOUTH AFRICA · TWO MALE ORCAS', 130);
  const k = eio(t, 1.2, 2.8);
  s += `<g opacity="${eo(t, 0.4, 1.2)}">` + collapsedFin(620, 640, -1, k, 'PORT') + '</g>';
  s += `<g opacity="${eo(t, 0.8, 1.6)}">` + collapsedFin(1300, 640, 1, k, 'STARBOARD') + '</g>';
  s += rise(t, 3.0, W / 2, 790, 'Named for their collapsed dorsal fins, one bent to the left, one to the right', { size: 30, weight: 500, fill: C.dim });
  const ks = eo(t, 5.0, 6.4), sx = lerp(W + 300, W / 2 + 120, ks) - seg(t, 9.0, 14) * 900;
  s += shark(sx, 940, 1.4, { fill: '#121a23', flip: true, opacity: ks * (1 - seg(t, 12.5, 14.5)) });
  s += rise(t, 7.2, W / 2, 1010, 'Great white sharks left some of their favourite bays', { size: 32, weight: 600 });
  return full(t, D, s);
}};

// ---------- 27 / 33: archive-style incident map ----------
G.incidents = { render(t, D, p) {
  const all = p && p.all;
  let s = `<rect width="${W}" height="${H}" fill="${C.paper}"/>`;
  // paper texture: subtle stripes + vignette
  for (let i = 0; i < 40; i++) s += `<rect x="0" y="${i * 27}" width="${W}" height="1" fill="#000" opacity="0.025"/>`;
  s += worldMap(t, { land: '#b9a782', stroke: '#6b5a40', so: 0.7, sw: 1 });
  s += `<rect width="${W}" height="${H}" fill="url(#vig)" opacity="0.8"/>`;
  s += txt(W / 2, 150, all ? 'A HANDFUL OF BITES, BUMPS AND CLOSE CALLS' : 'EVERY KNOWN ENCOUNTER · WILD ORCAS AND PEOPLE', { size: 30, weight: 800, fill: C.paperInk, ls: 6, opacity: eo(t, 0.1, 0.8) });
  const pins = [[-121.9, 36.3, '1972', 'Point Sur, California'], [-63.8, -42.6, '1989', 'Patagonia, Argentina'], [-131.6, 55.3, '2005', 'Ketchikan, Alaska'], [174.8, -36.8, '2014', 'New Zealand']];
  pins.forEach(([lo, la, y, n], i) => {
    const a = all ? 0.2 + i * 0.15 : 0.8 + i * 1.1, k = eo(t, a, a + 0.5), [x, yy] = ll(lo, la);
    const drop = (1 - k) * -40;
    s += `<g opacity="${k}" transform="translate(0,${drop})"><circle cx="${x}" cy="${yy}" r="11" fill="#a23b26" stroke="#3b1a10" stroke-width="2"/><line x1="${x}" y1="${yy}" x2="${x}" y2="${yy - 60}" stroke="#3b1a10" stroke-width="2"/>
      ${txt(x + (lo > 100 ? -14 : 14), yy - 64, y, { size: 40, weight: 800, fill: '#3b1a10', anchor: lo > 100 ? 'end' : 'start' })}
      ${txt(x + (lo > 100 ? -14 : 14), yy - 36, n, { size: 20, weight: 600, fill: C.paperInk, anchor: lo > 100 ? 'end' : 'start' })}</g>`;
  });
  if (all) s += rise(t, 1.6, W / 2, 1010, 'Over many decades, that is about all the evidence there is.', { size: 30, weight: 600, fill: C.paperInk });
  return `<g opacity="${envelope(t, D)}">${s}</g>`;
}};

// ---------- overlays: year / location lower-thirds and statement texts ----------
G.lower = { alpha: true, render(t, D, p) {
  const k = eo(t, 0, 0.8);
  let s = `<rect x="0" y="${H - 330}" width="${W}" height="330" fill="url(#lowG)"/>`;
  s = `<defs><linearGradient id="lowG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.6"/></linearGradient></defs>` + s;
  s += `<g opacity="${k}" transform="translate(${(1 - k) * -30},0)">${txt(140, H - 150, p.big, { size: p.size || 120, weight: 800, anchor: 'start', fill: p.color || C.ink, ls: 2 })}`;
  if (p.small) s += txt(146, H - 96, p.small, { size: 32, weight: 600, anchor: 'start', fill: C.dim, ls: 4 });
  s += `<rect x="146" y="${H - 132 - (p.size || 120)}" width="${90 * k}" height="4" fill="${p.color || C.ice}"/></g>`;
  return s;
}};
G.statement = { alpha: true, render(t, D, p) {
  const k = eo(t, 0, 1.0);
  let s = `<rect width="${W}" height="${H}" fill="#000" opacity="${0.35 * k}"/>`;
  s += `<g opacity="${k}">${txt(W / 2, H / 2 + 20, p.big, { size: p.size || 110, weight: 800, fill: p.color || C.ink, ls: 6 + 6 * (1 - k) })}`;
  if (p.small) s += txt(W / 2, H / 2 + 100, p.small, { size: 34, weight: 600, fill: C.dim, ls: 4 });
  return s + '</g>';
}};

// ---------- 35: shark comparison ----------
G.sharks = { render(t, D) {
  let s = kicker(t, 0.1, 'INTERNATIONAL SHARK ATTACK FILE', 150);
  s += rise(t, 0.6, W / 2, 300, '2025', { size: 70, weight: 800, fill: C.dim, ls: 8 });
  const n = Math.round(65 * eo(t, 1.2, 3.2)), d = Math.round(9 * eo(t, 2.6, 4.0));
  s += `<g opacity="${eo(t, 1.0, 1.6)}">${txt(640, 560, String(n), { size: 230, weight: 800, fill: C.ink })}${txt(640, 640, 'UNPROVOKED SHARK BITES', { size: 30, weight: 700, fill: C.dim, ls: 4 })}</g>`;
  s += `<g opacity="${eo(t, 2.4, 3.0)}">${txt(1280, 560, String(d), { size: 230, weight: 800, fill: C.red })}${txt(1280, 640, 'DEATHS', { size: 30, weight: 700, fill: C.dim, ls: 4 })}</g>`;
  s += `<line x1="${W / 2}" y1="380" x2="${W / 2}" y2="660" stroke="${C.faint}" stroke-width="2" opacity="${eo(t, 1.0, 1.6)}"/>`;
  const k = eo(t, 6.0, 7.0);
  s += `<g opacity="${k}"><rect x="560" y="760" width="800" height="130" rx="16" fill="#0e2942" fill-opacity="0.8" stroke="${C.ice}" stroke-opacity="0.4"/>
    ${txt(660, 845, '0', { size: 90, weight: 800, fill: C.ice })}${txt(730, 815, 'WILD ORCAS', { size: 30, weight: 800, anchor: 'start', ls: 4 })}${txt(730, 860, 'confirmed human deaths, ever', { size: 28, weight: 500, anchor: 'start', fill: C.dim })}</g>`;
  return full(t, D, s);
}};

// ---------- 41: range vs tank ----------
G.range = { render(t, D) {
  let s = kicker(t, 0.1, 'WHAT CAPTIVITY TAKES AWAY', 130);
  // winding path of a day's travel
  const pts = [];
  for (let i = 0; i <= 200; i++) { const u = i / 200; pts.push([160 + u * 1180 + Math.sin(u * 9) * 40, 560 + Math.sin(u * 5.3) * 190 + Math.cos(u * 13) * 30]); }
  const k = eio(t, 0.6, 6.0), n = Math.max(2, Math.floor(k * pts.length));
  s += `<polyline points="${pts.slice(0, n).map(p => p.join(',')).join(' ')}" fill="none" stroke="${C.ice}" stroke-width="5" stroke-linecap="round" opacity="0.9"/>`;
  const [hx, hy] = pts[n - 1], [px2, py2] = pts[Math.max(0, n - 4)];
  s += orcaTop(hx, hy, 0.5, { rot: Math.atan2(hy - py2, hx - px2) * 180 / Math.PI, fill: '#05080c' });
  // family members following
  [1, 2, 3].forEach(j => { const q = pts[Math.max(0, n - 1 - j * 12)], q2 = pts[Math.max(0, n - 5 - j * 12)]; s += orcaTop(q[0] + j * 6, q[1] + (j % 2 ? 26 : -26), 0.36, { rot: Math.atan2(q[1] - q2[1], q[0] - q2[0]) * 180 / Math.PI, fill: '#05080c', opacity: 0.85 }); });
  s += rise(t, 1.0, 160, 330, 'IN THE WILD', { size: 30, weight: 800, anchor: 'start', ls: 6, fill: C.ice });
  s += rise(t, 1.6, 160, 380, 'dozens of kilometres a day, with family', { size: 32, weight: 500, anchor: 'start', fill: C.ink });
  // tank
  const kt = eo(t, 6.6, 7.6);
  s += `<g opacity="${kt}"><rect x="1540" y="520" width="110" height="70" fill="none" stroke="${C.dim}" stroke-width="4"/>${orcaTop(1595, 555, 0.4, { fill: '#05080c', rot: (t * 40) % 360 })}
    ${txt(1595, 470, 'IN A TANK', { size: 30, weight: 800, ls: 6, fill: C.dim })}${txt(1595, 650, 'no space, no family', { size: 28, weight: 500, fill: C.dim })}</g>`;
  return full(t, D, s);
}};

// ---------- 49: resident vs Bigg's tree ----------
G.tree = { render(t, D) {
  let s = kicker(t, 0.1, 'TWO KINDS OF ORCA · SAME WATERS', 120);
  const rx = 260, ry = 560, k = eio(t, 0.6, 2.4);
  s += `<line x1="${rx - 120}" y1="${ry}" x2="${rx}" y2="${ry}" stroke="${C.dim}" stroke-width="5"/>`;
  s += `<path d="M${rx},${ry} C${rx + 260},${ry} ${rx + 260},${ry - 210} ${rx + 620},${ry - 210} L${rx + 1000},${ry - 210}" fill="none" stroke="${C.ice}" stroke-width="5" stroke-dasharray="1400" stroke-dashoffset="${1400 * (1 - k)}"/>`;
  s += `<path d="M${rx},${ry} C${rx + 260},${ry} ${rx + 260},${ry + 210} ${rx + 620},${ry + 210} L${rx + 1000},${ry + 210}" fill="none" stroke="${C.warm}" stroke-width="5" stroke-dasharray="1400" stroke-dashoffset="${1400 * (1 - k)}"/>`;
  s += `<circle cx="${rx}" cy="${ry}" r="12" fill="${C.ink}" opacity="${eo(t, 0.3, 0.8)}"/>`;
  s += rise(t, 2.6, rx, ry + 60, 'split > 300,000', { size: 28, weight: 700, fill: C.ink });
  s += rise(t, 2.8, rx, ry + 96, 'years ago', { size: 28, weight: 500, fill: C.dim });
  // tips
  s += orca(rx + 1140, ry - 230, 0.8, { fill: '#05080c', stroke: C.ice, sw: 1.5, opacity: eo(t, 2.4, 3.2) });
  s += orca(rx + 1140, ry + 190, 0.7, { fill: '#05080c', stroke: C.warm, sw: 1.5, opacity: eo(t, 2.6, 3.4) });
  s += rise(t, 3.2, rx + 640, ry - 250, 'RESIDENTS', { size: 46, weight: 800, anchor: 'start', fill: C.ice, ls: 4 });
  s += rise(t, 3.6, rx + 640, ry - 160, 'large family groups · fish, mostly salmon', { size: 28, weight: 500, anchor: 'start' });
  s += rise(t, 4.0, rx + 640, ry + 170, "BIGG'S", { size: 46, weight: 800, anchor: 'start', fill: C.warm, ls: 4 });
  s += rise(t, 4.4, rx + 640, ry + 260, 'small groups · seals, sea lions, whales', { size: 28, weight: 500, anchor: 'start' });
  const kq = eo(t, 9.5, 10.5);
  s += `<g opacity="${kq}"><rect x="560" y="900" width="800" height="96" rx="14" fill="#0e2942" fill-opacity="0.8" stroke="${C.faint}"/>${txt(W / 2, 942, '2024: proposed as two separate species', { size: 30, weight: 700 })}${txt(W / 2, 980, 'not yet fully accepted by the scientific community', { size: 24, weight: 500, fill: C.dim })}</g>`;
  return full(t, D, s);
}};

// ---------- 54/55: porpoises ----------
G.porpoise1 = { render(t, D) {
  let s = kicker(t, 0.1, 'HARBOUR PORPOISE', 150);
  const sea = 620;
  const arc = seg(t, 0.6, 4.2), x = lerp(500, 1420, arc), y = sea + 30 - Math.sin(arc * Math.PI) * 90;
  s += porpoise(x, y, 2.2, { rot: lerp(-24, 24, arc), fill: '#8da3b6' });
  s += `<rect x="0" y="${sea}" width="${W}" height="${H - sea}" fill="#06243b" opacity="0.85"/><line x1="0" y1="${sea}" x2="${W}" y2="${sea}" stroke="${C.ice}" stroke-width="2" opacity="0.6"/>`;
  s += rise(t, 1.4, W / 2, 860, 'about 1.5 metres long', { size: 32, weight: 500, fill: C.dim });
  return full(t, D, s);
}};
G.porpoise2 = { render(t, D) {
  let s = kicker(t, 0.1, 'SOUTHERN RESIDENTS AND PORPOISES', 130);
  const cx = W / 2, cy = 560;
  const px = cx + Math.sin(t * 1.3) * 60, py = cy + Math.cos(t * 1.7) * 40;
  s += porpoise(px, py, 0.9, { rot: Math.sin(t * 2) * 30, fill: '#9fb3c4' });
  for (let i = 0; i < 4; i++) {
    const a = t * 0.9 + i * Math.PI / 2, r = 230 + Math.sin(t * 1.4 + i) * 30;
    s += orcaTop(cx + Math.cos(a) * r * 1.4, cy + Math.sin(a) * r * 0.8, 0.85, { rot: a * 180 / Math.PI + 90, fill: '#05080c', opacity: eo(t, 0.5 + i * 0.2, 1.2 + i * 0.2) });
  }
  s += `<ellipse cx="${cx}" cy="${cy}" rx="420" ry="250" fill="none" stroke="${C.faint}" stroke-dasharray="6 10" opacity="0.6"/>`;
  s += rise(t, 1.2, 240, 920, 'CHASE', { size: 44, weight: 800, anchor: 'start', fill: C.ice, ls: 6 });
  s += rise(t, 2.0, 800, 920, 'PUSH', { size: 44, weight: 800, fill: C.ice, ls: 6 });
  s += rise(t, 2.8, 1680, 920, 'TOSS', { size: 44, weight: 800, anchor: 'end', fill: C.ice, ls: 6 });
  s += rise(t, 4.2, W / 2, 1000, 'sometimes for hours', { size: 30, weight: 500, fill: C.dim });
  return full(t, D, s);
}};

// ---------- 56: 78 incidents ----------
G.g78 = { render(t, D) {
  let s = kicker(t, 0.1, 'GILES, TEMAN ET AL. · MARINE MAMMAL SCIENCE · 2023', 140, { size: 22 });
  const n = Math.round(78 * eo(t, 1.0, 4.5));
  s += `<g opacity="${eo(t, 0.6, 1.2)}">${txt(W / 2, 420, String(n), { size: 240, weight: 800 })}${txt(W / 2, 500, 'DOCUMENTED INCIDENTS', { size: 34, weight: 800, ls: 6, fill: C.ice })}</g>`;
  // timeline 1962 -> 2020 with 78 ticks
  const x0 = 260, x1 = 1660, y = 720, kk = eo(t, 1.0, 1.8);
  s += `<line x1="${x0}" y1="${y}" x2="${lerp(x0, x1, kk)}" y2="${y}" stroke="${C.dim}" stroke-width="3"/>`;
  s += txt(x0, y + 60, '1962', { size: 34, weight: 700, opacity: kk }) + txt(x1, y + 60, '2020', { size: 34, weight: 700, opacity: kk });
  for (let i = 0; i < 78; i++) {
    const u = Math.pow((i + 0.5) / 78, 0.55), x = lerp(x0, x1, u), k = clamp(n - i);
    s += `<circle cx="${x}" cy="${y - 26 - (i % 3) * 18}" r="6" fill="${C.ice}" opacity="${k}"/>`;
  }
  s += rise(t, 6.0, W / 2, 900, 'more than sixty years of records', { size: 32, weight: 500, fill: C.dim });
  s += rise(t, 12.0, W / 2, 980, 'Porpoises are never eaten.', { size: 40, weight: 700, fill: C.ink });
  return full(t, D, s);
}};

// ---------- 58: three explanations ----------
G.three = { render(t, D) {
  let s = kicker(t, 0.1, 'THREE POSSIBLE EXPLANATIONS', 150);
  const cards = [['PLAY', 'social play that helps the group bond', 1.6], ['PRACTICE', 'a porpoise standing in for a fast salmon', 6.0], ['MISPLACED CARE', 'trying to look after a small, weak animal', 10.5]];
  cards.forEach(([h, d, a], i) => {
    const x = 210 + i * 520, k = eo(t, a, a + 0.8), active = t > a;
    s += `<g opacity="${0.25 + 0.75 * k}" transform="translate(0,${(1 - k) * 30})"><rect x="${x}" y="330" width="460" height="500" rx="20" fill="#0e2942" fill-opacity="0.8" stroke="${active ? C.ice : C.faint}" stroke-width="${active ? 3 : 1.5}"/>
      ${txt(x + 230, 450, String(i + 1), { size: 100, weight: 800, fill: active ? C.ice : C.faint })}
      ${txt(x + 230, 580, h, { size: i === 2 ? 42 : 52, weight: 800, ls: 4 })}
      <foreignObject x="${x + 40}" y="620" width="380" height="180"><div xmlns="http://www.w3.org/1999/xhtml" style="font-family:${FONT};font-size:30px;font-weight:500;color:${C.dim};text-align:center;line-height:1.3">${esc(d)}</div></foreignObject></g>`;
  });
  return full(t, D, s);
}};

// ---------- 62: life timeline ----------
G.life = { render(t, D) {
  let s = kicker(t, 0.1, "A FEMALE ORCA'S LIFE", 150);
  const x0 = 200, x1 = 1720, y = 560, px = (x1 - x0) / 90, k = eio(t, 0.4, 2.0);
  s += `<rect x="${x0}" y="${y - 26}" width="${(x1 - x0) * k}" height="52" rx="26" fill="#13324d"/>`;
  s += `<rect x="${x0 + 12 * px}" y="${y - 26}" width="${(40 - 12) * px * eo(t, 1.2, 2.4)}" height="52" fill="url(#iceBar)"/>`;
  s += `<rect x="${x0 + 40 * px}" y="${y - 26}" width="${(85 - 40) * px * eo(t, 3.0, 4.6)}" height="52" fill="url(#warmBar)"/>`;
  [0, 20, 40, 60, 80].forEach(a => s += txt(x0 + a * px, y + 80, a + ' yrs', { size: 24, weight: 600, fill: C.faint, opacity: k }));
  s += rise(t, 1.6, x0 + 26 * px, y - 60, 'CALVES', { size: 34, weight: 800, fill: C.ice, ls: 4 });
  s += rise(t, 3.4, x0 + 62 * px, y - 60, 'DECADES AFTER MENOPAUSE', { size: 34, weight: 800, fill: C.warm, ls: 4 });
  s += rise(t, 4.4, W / 2, 800, 'Only humans and a few toothed whales live like this', { size: 30, weight: 500, fill: C.dim });
  return full(t, D, s);
}};

// ---------- 65: 4.5x ----------
G.grand = { render(t, D) {
  let s = kicker(t, 0.1, 'NEARLY 400 YOUNG ORCAS · 2019 STUDY', 140, { fill: C.warm });
  const base = 820;
  const h1 = 90, h2 = h1 * 4.5, k1 = eo(t, 1.0, 2.2), k2 = eo(t, 3.0, 5.0);
  s += `<rect x="520" y="${base - h1 * k1}" width="260" height="${h1 * k1}" rx="8" fill="${C.faint}"/>`;
  s += `<rect x="1140" y="${base - h2 * k2}" width="260" height="${h2 * k2}" rx="8" fill="url(#warmBar)"/>`;
  s += `<line x1="400" y1="${base}" x2="1520" y2="${base}" stroke="${C.dim}" stroke-width="2"/>`;
  s += rise(t, 1.0, 650, base + 60, 'Grandmother alive', { size: 30, weight: 700 });
  s += rise(t, 3.0, 1270, base + 60, 'Grandmother died', { size: 30, weight: 700 });
  s += rise(t, 3.2, 1270, base + 100, 'in the previous two years', { size: 24, weight: 500, fill: C.dim });
  s += `<g opacity="${eo(t, 4.6, 5.6)}">${txt(1270, base - h2 - 40, '4.5×', { size: 150, weight: 800, fill: C.warm })}</g>`;
  s += rise(t, 5.4, 650, base - h1 - 30, 'calf mortality', { size: 26, weight: 500, fill: C.dim });
  return full(t, D, s);
}};

// ---------- 70: brain ----------
G.brain = { render(t, D) {
  let s = kicker(t, 0.1, 'ONE OF THE LARGEST BRAINS IN THE OCEAN', 150);
  const k = eo(t, 0.4, 1.6);
  s += orca(W / 2 - 40, 560, 3.6, { opacity: k, fill: '#05080c', stroke: C.ice, sw: 0.5, plain: true });
  // brain glow near the head
  const pulse = 0.6 + 0.4 * Math.sin(t * 2.2);
  const bx = W / 2 - 40 + (150 - 100) * 3.6, by = 560 + (24 - 30) * 3.6;
  s += `<ellipse cx="${bx}" cy="${by}" rx="${70 * eo(t, 1.4, 2.4)}" ry="${48 * eo(t, 1.4, 2.4)}" fill="${C.ice}" opacity="${0.55 * pulse}" filter="url(#glow)"/>`;
  s += `<path d="M${bx - 40},${by} C${bx - 30},${by - 30} ${bx},${by - 34} ${bx + 20},${by - 20} C${bx + 46},${by - 26} ${bx + 56},${by + 4} ${bx + 36},${by + 20} C${bx + 10},${by + 34} ${bx - 30},${by + 26} ${bx - 40},${by} Z" fill="none" stroke="${C.ink}" stroke-width="3" opacity="${eo(t, 1.8, 2.6)}"/>`;
  s += rise(t, 3.2, W / 2, 900, 'Complex societies · family bonds that can last a lifetime', { size: 32, weight: 600 });
  return full(t, D, s);
}};

// ---------- 72: DAY 17 counter (overlay) ----------
G.day17 = { alpha: true, render(t, D) {
  const k = eo(t, 0, 0.8), day = Math.min(17, 1 + Math.floor(seg(t, 0.8, D - 2.4) * 16.999));
  const km = Math.round(1600 * seg(t, 0.8, D - 2.4));
  let s = `<rect x="0" y="0" width="${W}" height="${H}" fill="#000" opacity="${0.25 * k}"/>`;
  s += `<g opacity="${k}">${txt(140, 230, 'DAY', { size: 44, weight: 800, anchor: 'start', fill: C.warm, ls: 10 })}${txt(132, 400, String(day), { size: 200, weight: 800, anchor: 'start', mono: false })}`;
  s += txt(146, 470, `${fmt(km)} km`, { size: 44, weight: 700, anchor: 'start', fill: C.dim, mono: true });
  s += `<rect x="146" y="500" width="${380 * seg(t, 0.8, D - 2.4)}" height="4" fill="${C.warm}"/></g>`;
  return s;
}};

// ---------- 78: carved wooden orca (procedural, warm firelight) ----------
G.carving = { render(t, D) {
  const fl = 0.75 + 0.12 * Math.sin(t * 7.3) + 0.08 * Math.sin(t * 13.1 + 1) + 0.05 * Math.sin(t * 23.7);
  let s = `<defs><radialGradient id="fire" cx="50%" cy="85%" r="70%"><stop offset="0" stop-color="#ffb25e" stop-opacity="${0.55 * fl}"/><stop offset="0.5" stop-color="#7a3512" stop-opacity="${0.35 * fl}"/><stop offset="1" stop-color="#000" stop-opacity="1"/></radialGradient>
  <pattern id="grainP" width="400" height="60" patternUnits="userSpaceOnUse"><rect width="400" height="60" fill="#6b4223"/>${Array.from({ length: 14 }, (_, i) => `<path d="M0,${i * 4.5} C100,${i * 4.5 + 3} 300,${i * 4.5 - 3} 400,${i * 4.5}" stroke="#3e2410" stroke-width="${1 + i % 3}" fill="none" opacity="0.6"/>`).join('')}</pattern>
  <linearGradient id="woodShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffcf8a" stop-opacity="${0.45 * fl}"/><stop offset="1" stop-color="#000" stop-opacity="0.55"/></linearGradient></defs>`;
  s += `<rect width="${W}" height="${H}" fill="#050302"/><rect width="${W}" height="${H}" fill="url(#fire)"/>`;
  const k = eo(t, 0.2, 2.0), drift = t * 6;
  const tr = `translate(${W / 2 - 20 + drift},${560}) scale(4.4) translate(-100,-30)`;
  s += `<g transform="${tr}" opacity="${k}"><path d="${ORCA_SIDE}" fill="url(#grainP)"/><path d="${ORCA_SIDE}" fill="url(#woodShade)"/><path d="${ORCA_SIDE}" fill="none" stroke="#2a170a" stroke-width="0.8"/>
     <path d="${ORCA_EYE}" fill="#2a170a" opacity="0.8"/><path d="M150,26 C140,30 130,33 120,34" stroke="#2a170a" stroke-width="0.6" fill="none"/></g>`;
  // embers
  for (let i = 0; i < 40; i++) { const x = (i * 211.7 + t * 30 * (1 + i % 3)) % W, y = H - ((t * (40 + i * 3) + i * 97) % H); s += `<circle cx="${x}" cy="${y}" r="${1.2 + i % 3}" fill="#ffb25e" opacity="${0.15 + 0.25 * ((i * 7) % 5) / 5}"/>`; }
  s += rise(t, 1.4, W / 2, 940, 'NATSILANE · A TLINGIT STORY', { size: 28, weight: 700, fill: '#e9b77a', ls: 8 });
  return `<g opacity="${envelope(t, D, 0.6, 0.01)}">${s}</g>`;
}};

// ---------- 82b / 85: rudder diagram ----------
G.rudder = { render(t, D, p) {
  let s = kicker(t, 0.1, p && p.short ? 'THE TARGET' : 'IBERIAN ORCAS · SINCE 2020', 110);
  const sea = 560;
  // hull + keel + rudder, side view
  s += `<path d="M380,${sea - 60} L1560,${sea - 60} C1500,${sea + 40} 1400,${sea + 70} 1240,${sea + 80} L560,${sea + 80} C470,${sea + 60} 420,${sea + 20} 380,${sea - 60} Z" fill="#dfe7ee"/>`;
  s += `<line x1="1000" y1="${sea - 60}" x2="1000" y2="${sea - 330}" stroke="#dfe7ee" stroke-width="10"/><path d="M1010,${sea - 320} L1010,${sea - 70} L1300,${sea - 70} Z" fill="#dfe7ee" opacity="0.85"/>`;
  s += `<path d="M880,${sea + 80} L1080,${sea + 80} L1050,${sea + 280} L920,${sea + 280} Z" fill="#9fb0bf"/>`;
  const wig = Math.sin(t * 5) * 10 * seg(t, 2.2, 3.0);
  s += `<g transform="rotate(${wig},630,${sea + 80})"><path d="M600,${sea + 80} L660,${sea + 80} L670,${sea + 260} L590,${sea + 250} Z" fill="${C.warm}" stroke="#fff" stroke-width="2"/></g>`;
  s += `<rect x="0" y="${sea}" width="${W}" height="${H - sea}" fill="#06243b" opacity="0.55"/><line x1="0" y1="${sea}" x2="${W}" y2="${sea}" stroke="${C.ice}" opacity="0.6" stroke-width="2"/>`;
  const k = seg(t, 0.6, 2.4);
  s += orca(lerp(80, 470, easeOut(k)), sea + 230, 1.1, { fill: '#05080c', stroke: C.ice, sw: 1, rot: -8 });
  s += orca(lerp(-200, 300, easeOut(seg(t, 1.0, 2.8))), sea + 380, 0.8, { fill: '#05080c', stroke: C.ice, sw: 1, opacity: 0.85 });
  s += rise(t, 2.4, 760, sea + 360, 'THE RUDDER', { size: 46, weight: 800, fill: C.warm, ls: 4, anchor: 'start' });
  // people on deck
  [1380, 1440].forEach((x, i) => s += diver(x, sea - 60, 0.42, { fill: C.ink, opacity: eo(t, 3.0 + i * 0.2, 3.6 + i * 0.2) }));
  s += rise(t, 3.6, 1490, sea - 100, 'NOT THE PEOPLE', { size: 34, weight: 800, fill: C.ink, ls: 4, anchor: 'start' });
  return full(t, D, s);
}};

// ---------- 83: 700+ / 8+ ----------
G.iberia = { render(t, D) {
  let s = kicker(t, 0.1, 'SPAIN AND PORTUGAL · SINCE 2020', 160);
  s += `<g opacity="${eo(t, 0.4, 1.2)}">${txt(620, 560, '700+', { size: 220, weight: 800 })}${txt(620, 640, 'INTERACTIONS LOGGED', { size: 30, weight: 700, fill: C.dim, ls: 4 })}</g>`;
  s += `<g opacity="${eo(t, 2.2, 3.0)}">${txt(1300, 560, '8+', { size: 220, weight: 800, fill: C.warm })}${txt(1300, 640, 'BOATS SUNK', { size: 30, weight: 700, fill: C.dim, ls: 4 })}</g>`;
  s += `<line x1="${W / 2 + 20}" y1="380" x2="${W / 2 + 20}" y2="660" stroke="${C.faint}" stroke-width="2" opacity="${eo(t, 1.0, 1.6)}"/>`;
  return full(t, D, s);
}};

// ---------- 84: Strait of Gibraltar map ----------
G.gibraltar = { render(t, D) {
  const m = MAPS.iberia;
  const z = 1 + 0.9 * eio(t, 1.0, 9.0);
  // focus around the strait (-5.6, 36.0)
  const fx = (-5.6 - m.bbox[0]) / (m.bbox[1] - m.bbox[0]) * m.size[0], fy = (m.bbox[3] - 36.0) / (m.bbox[3] - m.bbox[2]) * m.size[1];
  const base = 1.0, cx = lerp(W / 2 + 120, W / 2, eio(t, 1, 9)), cy = lerp(H / 2 + 260, H / 2 + 60, eio(t, 1, 9));
  let s = `<rect width="${W}" height="${H}" fill="#061a2b"/>`;
  s += `<g transform="translate(${cx},${cy}) scale(${base * z}) translate(${-fx},${-fy})"><path d="${m.d}" fill="#1f3b2f" stroke="#7fa08a" stroke-width="${1.2 / z}"/>`;
  // interaction zone along the coasts
  const proj = (lo, la) => [(lo - m.bbox[0]) / (m.bbox[1] - m.bbox[0]) * m.size[0], (m.bbox[3] - la) / (m.bbox[3] - m.bbox[2]) * m.size[1]];
  const zone = [[-9.6, 43.6], [-9.4, 41.5], [-9.5, 39.0], [-9.3, 37.0], [-8.0, 36.7], [-6.4, 36.5], [-5.6, 35.9], [-5.0, 36.1]];
  const zk = eo(t, 2.0, 4.0);
  s += `<polyline points="${zone.map(q => proj(...q).join(',')).join(' ')}" fill="none" stroke="${C.warm}" stroke-width="${26 / z}" stroke-linecap="round" stroke-linejoin="round" opacity="${0.45 * zk}"/>`;
  const [gx, gy] = proj(-5.6, 35.95);
  s += `<circle cx="${gx}" cy="${gy}" r="${(10 + 12 * Math.sin(t * 2) ** 2) / z}" fill="none" stroke="${C.ink}" stroke-width="${2 / z}" opacity="${eo(t, 3, 4)}"/></g>`;
  s += `<rect width="${W}" height="${H}" fill="url(#vig)"/>`;
  s += rise(t, 0.6, 140, 160, 'SPAIN · PORTUGAL', { size: 30, weight: 800, anchor: 'start', fill: C.ink, ls: 8 });
  s += rise(t, 3.6, 140, 210, 'Strait of Gibraltar', { size: 30, weight: 500, anchor: 'start', fill: C.dim });
  s += rise(t, 4.4, 140, 980, 'Interaction zone', { size: 28, weight: 700, anchor: 'start', fill: C.warm });
  s += rise(t, 7.0, W - 140, 980, 'A game spreading through a playground?', { size: 30, weight: 600, anchor: 'end', fill: C.ink });
  return `<g opacity="${envelope(t, D)}">${s}</g>`;
}};

// ---------- 91: 98 -> 73 -> 77 ----------
G.srkw = { render(t, D) {
  let s = kicker(t, 0.1, 'SOUTHERN RESIDENT KILLER WHALES', 140);
  const x0 = 280, x1 = 1640, y0 = 860, y1 = 300; // years 1995..2026, count 60..105
  const X = yr => lerp(x0, x1, (yr - 1995) / 31), Y = n => lerp(y0, y1, (n - 60) / 45);
  const pts = [[1995, 98], [2021, 73], [2026, 76], [2026.8, 77]];
  s += `<line x1="${x0}" y1="${y0}" x2="${x1}" y2="${y0}" stroke="${C.faint}" stroke-width="2"/>`;
  [1995, 2005, 2015, 2026].forEach(yr => s += txt(X(yr), y0 + 50, String(yr), { size: 26, weight: 600, fill: C.faint }));
  const k = eio(t, 1.0, 9.0);
  // path 1995 -> 2021 -> 2026
  const segs = [[pts[0], pts[1], 1.0, 6.0], [pts[1], pts[2], 9.0, 11.0], [pts[2], pts[3], 13.0, 14.0]];
  segs.forEach(([a, b, s0, s1]) => { const kk = eio(t, s0, s1); s += `<line x1="${X(a[0])}" y1="${Y(a[1])}" x2="${lerp(X(a[0]), X(b[0]), kk)}" y2="${lerp(Y(a[1]), Y(b[1]), kk)}" stroke="${C.ice}" stroke-width="5" stroke-linecap="round"/>`; });
  const lab = [[pts[0], 0.6, '98', '1995'], [pts[1], 6.0, '73', 'end of 2021'], [pts[3], 14.0, '77', 'Oct 2026']];
  lab.forEach(([p, a, n, d], i) => { const kk = eo(t, a, a + 0.6); s += `<circle cx="${X(p[0])}" cy="${Y(p[1])}" r="12" fill="${i === 2 ? C.warm : C.ice}" opacity="${kk}"/>` + txt(X(p[0]) + (i === 2 ? -10 : 0), Y(p[1]) - (i === 2 ? 70 : 40), n, { size: 80, weight: 800, opacity: kk, anchor: i === 2 ? 'end' : 'middle', fill: i === 2 ? C.warm : C.ink }) + txt(X(p[0]) + (i === 2 ? -10 : 0), Y(p[1]) + (i === 2 ? -40 : 54), d, { size: 24, weight: 600, fill: C.dim, opacity: kk, anchor: i === 2 ? 'end' : 'middle' }); });
  s += `<circle cx="${X(2026)}" cy="${Y(76)}" r="8" fill="${C.ice}" opacity="${eo(t, 11, 11.5)}"/>` + rise(t, 11.0, X(2026) + 30, Y(76) + 8, '76', { size: 34, weight: 800, anchor: 'start', fill: C.ink }) + rise(t, 11.2, X(2026) + 30, Y(76) + 40, '2026 census', { size: 22, weight: 600, anchor: 'start', fill: C.dim });
  s += rise(t, 2.0, x0, 250, 'Chinook salmon have declined', { size: 28, weight: 600, anchor: 'start', fill: C.dim });
  return full(t, D, s);
}};

// ---------- chapter cards ----------
G.chapter = { render(t, D, p) {
  const k = eo(t, 0.2, 1.2);
  let s = txt(W / 2, 430, p.kicker, { size: 30, weight: 700, fill: C.ice, ls: 12, opacity: eo(t, 0.1, 0.9) });
  s += `<rect x="${W / 2 - 60 * k}" y="462" width="${120 * k}" height="3" fill="${C.ice}"/>`;
  s += `<g opacity="${k}">` + txt(W / 2, 600 + (1 - k) * 20, p.title, { size: p.title.length > 22 ? 84 : 104, weight: 800, ls: 2 }) + '</g>';
  return bg(t) + `<g opacity="${envelope(t, D, 0.4, 0.5)}">${s}</g>`;
}};

// ---------- end card ----------
G.endcard = { render(t, D) {
  let s = txt(W / 2, 210, 'NATUREXPLORE', { size: 64, weight: 800, ls: 14, opacity: eo(t, 0.2, 1.2) });
  s += rise(t, 0.8, W / 2, 275, 'A new wildlife documentary every week', { size: 30, weight: 500, fill: C.dim });
  // two end-screen slots (YouTube end-screen elements go here)
  [[300, 'WATCH NEXT'], [1020, 'WATCH NEXT']].forEach(([x, l], i) => {
    const k = eo(t, 1.4 + i * 0.3, 2.2 + i * 0.3);
    s += `<g opacity="${k}"><rect x="${x}" y="380" width="600" height="338" rx="16" fill="#0e2942" fill-opacity="0.55" stroke="${C.ice}" stroke-opacity="0.5" stroke-width="2"/>${txt(x + 300, 560, l, { size: 28, weight: 700, ls: 8, fill: C.dim })}</g>`;
  });
  const k = eo(t, 2.6, 3.4);
  s += `<g opacity="${k}"><circle cx="${W / 2}" cy="880" r="88" fill="none" stroke="${C.ink}" stroke-width="3"/>${txt(W / 2, 892, 'SUBSCRIBE', { size: 24, weight: 800, ls: 4 })}</g>`;
  s += rise(t, 4.0, W / 2, 1030, 'Why do you think orcas leave us alone? Tell us in the comments.', { size: 28, weight: 600, fill: C.ink });
  return bg(t) + `<g opacity="${envelope(t, D, 0.8, 1.2)}">${s}</g>`;
}};
