// Graphic specifications. Each: render(t, D, p) -> inner SVG. alpha: overlay with transparent background.
const G = {};
const full = (t, D, inner, o = {}) => bg(t) + `<g opacity="${envelope(t, D, o.fi || 0.5, o.fo || 0.5)}">${inner}</g>`;

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
  s += rise(t, 4.0, W / 2, 1030, 'Would you have guessed the rock? Tell us in the comments.', { size: 28, weight: 600, fill: C.ink });
  return bg(t) + `<g opacity="${envelope(t, D, 0.8, 1.2)}">${s}</g>`;
}};
