"""Natural Earth land (world-atlas TopoJSON, public domain) to SVG paths, equirectangular projection."""
import json
def _decode(topo):
    sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]; arcs = []
    for arc in topo["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc: x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs
def _ring(arcs, idx):
    pts = []
    for i in idx:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a[1:] if pts else a)
    return pts
def land_path(file, lon0, lon1, lat0, lat1, W, H, min_px=0.0):
    """Path for land inside [lon0,lon1]x[lat0,lat1] fitted to W x H (equirectangular, cos-lat corrected)."""
    import math
    topo = json.load(open(file)); arcs = _decode(topo)
    geom = topo["objects"]["land"]["geometries"]
    k = math.cos(math.radians((lat0 + lat1) / 2))
    sx = W / ((lon1 - lon0) * k); sy = H / (lat1 - lat0); s = min(sx, sy)
    ox = (W - (lon1 - lon0) * k * s) / 2; oy = (H - (lat1 - lat0) * s) / 2
    def P(lon, lat): return (ox + (lon - lon0) * k * s, oy + (lat1 - lat) * s)
    out = []
    for g in geom:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in polys:
            for ring in poly:
                pts = _ring(arcs, ring)
                if not any(lon0 - 5 <= lo <= lon1 + 5 and lat0 - 5 <= la <= lat1 + 5 for lo, la in pts): continue
                xy = [P(lo, la) for lo, la in pts]
                xs = [p[0] for p in xy]; ys = [p[1] for p in xy]
                if max(xs) - min(xs) < min_px and max(ys) - min(ys) < min_px: continue
                simp = [xy[0]]
                for p in xy[1:]:
                    if abs(p[0] - simp[-1][0]) + abs(p[1] - simp[-1][1]) > 0.8: simp.append(p)
                # split where the ring wraps across the antimeridian, so no line crosses the whole map
                segs, cur = [], [simp[0]]
                for a, b2 in zip(simp, simp[1:]):
                    if abs(b2[0] - a[0]) > W / 2: segs.append(cur); cur = [b2]
                    else: cur.append(b2)
                segs.append(cur)
                close = "Z" if len(segs) == 1 else ""
                for sg in segs:
                    if len(sg) > 1: out.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in sg) + close)
    return " ".join(out), P
