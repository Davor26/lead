"""TopoJSON (Natural Earth via world-atlas, public domain) -> SVG path strings for the maps."""
import json
def decode(topo, obj):
    tr = topo.get('transform'); arcs = []
    for a in topo['arcs']:
        x = y = 0; pts = []
        for p in a:
            if tr: x += p[0]; y += p[1]; pts.append((x*tr['scale'][0]+tr['translate'][0], y*tr['scale'][1]+tr['translate'][1]))
            else: pts.append(tuple(p))
        arcs.append(pts)
    def ring(r):
        out = []
        for i in r:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            out += seg if not out else seg[1:]
        return out
    polys = []
    def geom(g):
        if g['type'] == 'GeometryCollection':
            for gg in g['geometries']: geom(gg)
        elif g['type'] == 'Polygon': polys.append([ring(r) for r in g['arcs']])
        elif g['type'] == 'MultiPolygon':
            for p in g['arcs']: polys.append([ring(r) for r in p])
    geom(topo['objects'][obj]); return polys
def path(polys, lon0, lon1, lat0, lat1, W, H, minpix=0.6):
    sx = W/(lon1-lon0); sy = H/(lat1-lat0); d = []
    for poly in polys:
        for r in poly:
            xs = [p[0] for p in r]; ys = [p[1] for p in r]
            if False and max(xs) < lon0-5 or min(xs) > lon1+5 or max(ys) < lat0-5 or min(ys) > lat1+5: continue
            pts = []; last = None
            # unwrap rings that cross the antimeridian
            ur = [r[0]]
            for lon, lat in r[1:]:
                pl = ur[-1][0]
                while lon - pl > 180: lon -= 360
                while lon - pl < -180: lon += 360
                ur.append((lon, lat))
            mean = sum(p[0] for p in ur) / len(ur)
            if mean > 180: ur = [(a - 360, b) for a, b in ur]
            if mean < -180: ur = [(a + 360, b) for a, b in ur]
            copies = [ur]
            if max(p[0] for p in ur) > 180: copies.append([(a - 360, b) for a, b in ur])
            if min(p[0] for p in ur) < -180: copies.append([(a + 360, b) for a, b in ur])
            for cp in copies:
              cx_ = [p[0] for p in cp]; cy_ = [p[1] for p in cp]
              if max(cx_) < lon0-2 or min(cx_) > lon1+2 or max(cy_) < lat0-2 or min(cy_) > lat1+2: continue
              pts = []; last = None
              for lon, lat in cp:
                q = ((lon-lon0)*sx, (lat1-lat)*sy)
                if last is None or abs(q[0]-last[0])+abs(q[1]-last[1]) > minpix: pts.append(q); last = q
              if len(pts) >= 3: d.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z')
            continue
            for lon, lat in ur:
                q = ((lon-lon0)*sx, (lat1-lat)*sy)
                if last is None or abs(q[0]-last[0])+abs(q[1]-last[1]) > minpix: pts.append(q); last = q
            if len(pts) < 3: continue
            d.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z')
    return ''.join(d)
w50 = decode(json.load(open('data/land-50m.json')), 'land')
w10 = decode(json.load(open('data/land-10m.json')), 'land')
maps = {
  'world': {'bbox': [-180, 180, -62, 84], 'size': [1600, 647], 'd': path(w50, -180, 180, -62, 84, 1600, 647, 0.8)},
  'iberia': {'bbox': [-13, 1, 34, 45], 'size': [1600, 1257], 'd': path(w10, -13, 1, 34, 45, 1600, 1257, 2.5)},
}
open('maps.js', 'w').write('window.MAPS=' + json.dumps(maps) + ';')
print({k: len(v['d']) for k, v in maps.items()})
