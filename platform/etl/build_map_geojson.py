#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#57/#65 — GERÇEK GeoJSON harita arka planı. Natural Earth 110m (public-domain) land + ülke sınırları
→ haritanın projeksiyonuyla (project: x=0.7517·lon−14.71, y=−1.6949·lat+118.58, viewBox 0..100)
→ bbox-clip + Douglas-Peucker basitleştirme → SVG path (land fill + ince ülke sınırları).
Çıktı: platform/ui/map_geo.py (LAND_PATH + BORDER_PATH). build_map_bg() bunu kullanır.
Dış tile YOK; veri build'e gömülür (statik, hafif). Çalıştırma: python platform/etl/build_map_geojson.py
"""
import json, math, os

HERE = os.path.dirname(__file__)
GEO = os.path.join(HERE, "geo")
# Ekranda görünür alan + kenar payı (viewBox 0..100). Bu kutuyla kesişmeyen poligonlar atılır.
VX0, VY0, VX1, VY1 = -3, -3, 103, 103


def pj(lon, lat):
    return (0.7517 * lon - 14.71, -1.6949 * lat + 118.58)


def _perp(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(x - x1, y - y1)
    t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))


def dp(pts, tol):
    """Douglas-Peucker basitleştirme."""
    if len(pts) < 3:
        return pts
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = _perp(pts[i], pts[0], pts[-1])
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        return dp(pts[:idx + 1], tol)[:-1] + dp(pts[idx:], tol)
    return [pts[0], pts[-1]]


def ring_in_view(ring):
    xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
    return not (max(xs) < VX0 or min(xs) > VX1 or max(ys) < VY0 or min(ys) > VY1)


def rings_from_geom(geom):
    t = geom["type"]; c = geom["coordinates"]
    out = []
    if t == "Polygon":
        out = c
    elif t == "MultiPolygon":
        for poly in c:
            out.extend(poly)
    return out


def path_for(geojson_path, tol, closed):
    data = json.load(open(geojson_path, encoding="utf-8"))
    segs = []
    for feat in data["features"]:
        g = feat.get("geometry")
        if not g:
            continue
        for ring in rings_from_geom(g):
            proj = [pj(lon, lat) for lon, lat, *_ in ring]
            if not ring_in_view(proj):
                continue
            simp = dp(proj, tol)
            if len(simp) < 2:
                continue
            d = "M " + " L ".join(f"{round(x,1)} {round(y,1)}" for x, y in simp)
            if closed:
                d += " Z"
            segs.append(d)
    return " ".join(segs)


def main():
    land = path_for(os.path.join(GEO, "ne_110m_land.geojson"), tol=0.35, closed=True)
    borders = path_for(os.path.join(GEO, "ne_110m_countries.geojson"), tol=0.45, closed=True)
    out = os.path.join(HERE, "..", "ui", "map_geo.py")
    with open(out, "w", encoding="utf-8") as f:
        f.write("# OTOMATİK ÜRETİLDİ — build_map_geojson.py (Natural Earth 110m, public-domain).\n")
        f.write("# project: x=0.7517*lon-14.71, y=-1.6949*lat+118.58 (viewBox 0..100). ELLE DÜZENLEME.\n")
        f.write("LAND_PATH = %r\n" % land)
        f.write("BORDER_PATH = %r\n" % borders)
    print("map_geo.py yazildi: land %d kr, border %d kr (uzunluk land=%d border=%d)" %
          (land.count("M"), borders.count("M"), len(land), len(borders)))


if __name__ == "__main__":
    main()
