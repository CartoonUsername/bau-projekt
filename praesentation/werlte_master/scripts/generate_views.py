"""Arbeitsbasis OG-2: Grundrisse mit Raster/Kern/Schacht/Balkonen, Platzfassade (Ansicht) und Schnitt A-A. Schematische Zeichnungen, KEINE Renderings."""
import json, os
here = os.path.dirname(__file__)
D = json.load(open(os.path.join(here, "..", "geometry", "building_design.json"), encoding="utf-8"))
K = 30; OX = 70
COL = {"core": "#8A9199", "dining": "#F2D48C", "lounge": "#B07A4A", "bar": "#3A3F44", "private_dining": "#7A5C3A", "circulation": "#D9D3C8", "wc": "#A6ADB4", "storage": "#A6ADB4", "kitchen": "#7E8A94", "office": "#3F6275", "apartment": "#9A4034", "corridor": "#D9D3C8"}
GX = D["grid"]["x"]
def head(t, sub, W, H):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Arial">', f'<rect width="{W}" height="{H}" fill="white"/>',
            f'<text x="20" y="30" font-size="20" font-weight="bold">{t}</text>', f'<text x="20" y="50" font-size="12" fill="#a00">{sub}</text>']
SUB = "ARBEITSSTAND, VORLÄUFIG (OG-2 als Arbeitsgrundlage, nicht festgeschrieben). Schematische Zeichnung, kein Rendering. Maße in m."
def plan(name, title, rooms, level, extra_rects=()):
    OY = 130; W = int(OX + 32 * K + 110); H = int(OY + 19 * K + 80)
    o = head(title, SUB, W, H)
    for r in rooms:
        x0, y0, x1, y1 = r["rect"]
        o.append(f'<rect x="{OX+x0*K}" y="{OY+y0*K}" width="{(x1-x0)*K}" height="{(y1-y0)*K}" fill="{COL.get(r["type"], "#ddd")}" stroke="white" stroke-width="2" opacity="0.9"/>')
        if r.get("area_gross"):
            net = r["area_gross"] * D["net_factor"] if r["type"] == "apartment" or r["type"] == "office" else r["area_gross"]
            lab = [r["id"], f"{net:.0f} m² {'netto' if r['type'] in ('apartment','office') else ''}"]
            for i, t in enumerate(lab):
                o.append(f'<text x="{OX+(x0+x1)/2*K}" y="{OY+(y0+y1)/2*K+i*13-3}" font-size="10" text-anchor="middle" fill="{"#111" if r["type"] in ("dining","corridor","circulation") else "white"}">{t}</text>')
    for c in D["core"].get(level, []):
        x0, y0, x1, y1 = c["rect"]
        o.append(f'<rect x="{OX+x0*K}" y="{OY+y0*K}" width="{(x1-x0)*K}" height="{(y1-y0)*K}" fill="#B8BEC4" stroke="#fff" stroke-width="2"/><text x="{OX+(x0+x1)/2*K}" y="{OY+(y0+y1)/2*K+3}" font-size="9" text-anchor="middle">{c["id"]}</text>')
    for s in D["shafts"]:
        if level in s["levels"]:
            x0, y0, x1, y1 = s["rect"]; o.append(f'<rect x="{OX+x0*K}" y="{OY+y0*K}" width="{(x1-x0)*K}" height="{(y1-y0)*K}" fill="#E8D44D" stroke="#000"/><text x="{OX+x0*K-4}" y="{OY+y0*K-3}" font-size="9" text-anchor="end">Schacht Küche</text>')
    if level == "L1":
        for b in D["balconies"]:
            x0, y0, x1, y1 = b["rect"]; o.append(f'<rect x="{OX+x0*K}" y="{OY+y0*K}" width="{(x1-x0)*K}" height="{(y1-y0)*K}" fill="#CFD3D6" stroke="#333" stroke-dasharray="4 3"/>')
    if level == "GF":
        t = D["terrace"]["rect"]; o.append(f'<rect x="{OX+t[0]*K}" y="{OY+t[1]*K}" width="{(t[2]-t[0])*K}" height="{(t[3]-t[1])*K}" fill="#D6B98F" stroke="#333" stroke-dasharray="6 4"/><text x="{OX+18*K}" y="{OY+t[1]*K+60}" font-size="11" text-anchor="middle">Terrasse (Lage ungeprüft)</text>')
        for op in D["openings"]:
            a, b = op["x"]; o.append(f'<rect x="{OX+a*K}" y="{OY-3}" width="{(b-a)*K}" height="6" fill="#1F9" stroke="#111"/>')
    for x in GX:
        o.append(f'<line x1="{OX+x*K}" y1="{OY-14}" x2="{OX+x*K}" y2="{OY+18*K+8}" stroke="#c0392b" stroke-width="0.8" stroke-dasharray="8 3 2 3"/><text x="{OX+x*K}" y="{OY-18}" font-size="9" text-anchor="middle" fill="#c0392b">{x:g}</text>')
    for c in D["columns_gf"]:
        if level in ("GF", "L1"): o.append(f'<rect x="{OX+c[0]*K-5}" y="{OY+c[1]*K-5}" width="10" height="10" fill="#000"/>')
    o.append(f'<rect x="{OX}" y="{OY}" width="{32*K}" height="{18*K}" fill="none" stroke="#111" stroke-width="3"/>')
    o.append(f'<text x="{OX}" y="{OY+18*K+30}" font-size="11" fill="#333">Raster R2 (rot, vorläufig), schwarze Quadrate = Stützen, y=0 Platzfassade (oben). Himmelsrichtung unbekannt (C-13).</text></svg>')
    open(os.path.join(here, "..", "plans", name), "w", encoding="utf-8").write("\n".join(o))
gf = [r for r in D["rooms"] if r["level"] == "GF"]
plan("plan_EG_arbeitsstand.svg", "Erdgeschoss – Arbeitsstand OG-2-Koordination", gf, "GF")
plan("plan_OG2_arbeitsstand.svg", "1. OG – Arbeitsgrundlage OG-2", D["upper_options"]["OG-2"]["rooms"], "L1")
plan("plan_Staffel_arbeitsstand.svg", "Staffelgeschoss – Arbeitsstand (S-1)", D["staffel"]["rooms"], "L2")
# ---- Ansicht Platzfassade (Blick von y<0), x nach rechts, z nach oben
S = 40; H0 = 560; W = int(OX + 32 * S + 60); H = 640
o = head("Ansicht Platzfassade – Arbeitsstand (OG-2)", SUB, W, H)
z = lambda v: H0 - v * S
X = lambda v: OX + v * S
o.append(f'<line x1="20" y1="{H0}" x2="{W-20}" y2="{H0}" stroke="#333" stroke-width="2"/>')
o.append(f'<rect x="{X(0)}" y="{z(6.5)}" width="{32*S}" height="{6.5*S}" fill="#6B2E27"/>')           # Klinker EG+OG
o.append(f'<rect x="{X(4.2)}" y="{z(9.6)}" width="{27*S}" height="{3.1*S}" fill="#B88B5A"/>')          # Staffel Lärche
o.append(f'<rect x="{X(4)}" y="{z(9.9)}" width="{27.2*S}" height="{0.3*S}" fill="#555"/>')            # Attika
o.append(f'<rect x="{X(4)}" y="{z(3.1)}" width="{28*S}" height="{3.1*S}" fill="#9FC4D6" opacity="0.7" stroke="#111"/>')  # EG-Glas
a, b = D["openings"][1]["x"]; o.append(f'<rect x="{X(a)}" y="{z(2.4)}" width="{(b-a)*S}" height="{2.4*S}" fill="none" stroke="#111" stroke-width="2"/>')
a, b = D["openings"][2]["x"]; o.append(f'<rect x="{X(a)}" y="{z(2.4)}" width="{(b-a)*S}" height="{2.4*S}" fill="#9FC4D6" stroke="#111"/>')
for i in range(5):                                                                                       # Wohnungen/Balkone OG
    x0 = 4 + 5.6 * i; bx = D["balconies"][i]["rect"]
    o.append(f'<rect x="{X(x0+0.9)}" y="{z(6.1)}" width="{3.8*S}" height="{2.2*S}" fill="#222" opacity="0.85"/>')
    o.append(f'<rect x="{X(bx[0])}" y="{z(3.5)-0.3*S}" width="{2.7*S}" height="{0.3*S}" fill="#C9CCCF" stroke="#111"/>')
    o.append(f'<rect x="{X(bx[0])}" y="{z(4.6)}" width="{2.7*S}" height="{1.1*S}" fill="#E6EEF0" opacity="0.8" stroke="#555"/>')
for i in range(4):                                                                                       # Staffel 4 Achsen
    x0 = 4.2 + 6.75 * i; o.append(f'<rect x="{X(x0+1.0)}" y="{z(9.0)}" width="{4.75*S}" height="{2.1*S}" fill="#222" opacity="0.85"/>')
ca = D["canopy"]["rect"]; o.append(f'<rect x="{X(ca[0])}" y="{z(3.0)-0.1*S}" width="{(ca[2]-ca[0])*S}" height="{0.1*S}" fill="#000"/><text x="{X(18)}" y="{z(3.0)+14}" font-size="9" text-anchor="middle" fill="#000">Vordach UK 3,0 m (C-18)</text>')
for x in GX:
    o.append(f'<line x1="{X(x)}" y1="{z(10.8)}" x2="{X(x)}" y2="{H0+14}" stroke="#c0392b" stroke-width="0.8" stroke-dasharray="8 3 2 3"/><text x="{X(x)}" y="{z(10.8)-3}" font-size="9" text-anchor="middle" fill="#c0392b">{x:g}</text>')
for lab, v in (("OKFF EG ±0,00", 0), ("OKFF 1. OG +3,50", 3.5), ("Traufe +6,50 (B-Plan)", 6.5), ("Attika +9,90", 9.9)):
    o.append(f'<line x1="{X(32)+4}" y1="{z(v)}" x2="{X(32)+26}" y2="{z(v)}" stroke="#333"/><text x="{X(32)+28}" y="{z(v)+3}" font-size="9">{lab}</text>')
o.append(f'<text x="{OX}" y="{H0+40}" font-size="11" fill="#333">Konflikte sichtbar: Staffel 4 Achsen (Rendering 7, C-09); Doppeltür x 17–19 in Feldmitte nur bei Raster R2; Platzfassade ohne Stützen nicht nachgewiesen (C-16).</text></svg>')
open(os.path.join(here, "..", "elevations", "elevation_platz_arbeitsstand.svg"), "w", encoding="utf-8").write("\n".join(o))
# ---- Schnitt A-A bei x = 18: y nach rechts (Platz links), z nach oben
S = 36; OX2 = 150; H0 = 520; W = int(OX2 + 24 * S + 80); H = 600
o = head("Schnitt A–A (x = 18) – Arbeitsstand", SUB, W, H)
Y = lambda v: OX2 + (v + 3.6) * S; z = lambda v: H0 - v * S
o.append(f'<line x1="20" y1="{H0}" x2="{W-20}" y2="{H0}" stroke="#333" stroke-width="2"/>')
def box(y0, y1, z0, z1, fill, st="#111", op=1):
    o.append(f'<rect x="{Y(y0)}" y="{z(z1)}" width="{(y1-y0)*S}" height="{(z1-z0)*S}" fill="{fill}" stroke="{st}" opacity="{op}"/>')
box(0, 18, 0, 3.5, "#F2D48C", op=0.5); box(12, 18, 0, 3.5, "#7E8A94", op=0.5)
box(-3.6, 0, 0, 0.12, "#D6B98F")
for (y0, y1, z0, z1) in ((0, 18, 3.2, 3.5), (0, 18, 6.2, 6.5), (0.8, 17.2, 9.3, 9.6)): box(y0, y1, z0, z1, "#9AA0A6")
box(0, 8, 3.5, 6.2, "#9A4034", op=0.55); box(10, 18, 3.5, 6.2, "#3F6275", op=0.55); box(8, 10, 3.5, 6.2, "#D9D3C8", op=0.8)
box(0.8, 8, 6.5, 9.3, "#B88B5A", op=0.6); box(10, 17.2, 6.5, 9.3, "#B88B5A", op=0.6); box(8, 10, 6.5, 9.3, "#D9D3C8", op=0.8)
box(-1.5, 0, 3.2, 3.5, "#C9CCCF"); box(-3.6, 0, 2.9, 3.0, "#000")
o.append(f'<rect x="{Y(8)-4}" y="{z(6.2)}" width="8" height="{6.2*S}" fill="#000"/><text x="{Y(8)}" y="{z(6.2)-4}" font-size="9" text-anchor="middle">Stütze y=8 (R2: x 15,2/20,8)</text>')
for t, (y, zz) in {"Terrasse": (-1.8, 0.5), "Platzfassade y=0": (0, 10.5), "Gastro EG": (6, 1.7), "Küche": (15, 1.7), "WE-L1-S3 (44,8 m² brutto)": (4, 4.8), "Büro (hinten)": (14, 4.8), "Mittelgang": (9, 4.8), "Staffel vorn": (4.4, 8.0), "Staffel hinten": (13.6, 8.0)}.items():
    o.append(f'<text x="{Y(y)}" y="{z(zz)}" font-size="10" text-anchor="middle">{t}</text>')
for lab, v in (("±0,00", 0), ("+3,50", 3.5), ("+6,50 Traufe", 6.5), ("+9,90 Attika", 9.9)):
    o.append(f'<text x="{Y(18)+6}" y="{z(v)+3}" font-size="9">{lab}</text><line x1="{Y(18)}" y1="{z(v)}" x2="{Y(18)+4}" y2="{z(v)}" stroke="#333"/>')
o.append(f'<text x="20" y="{H0+40}" font-size="11" fill="#333">Schematisch: Geschosshöhen 3,5 / 3,0 / 3,1 m, Decken 0,30 m, Balkon UK 3,2 m schneidet Vordach UK 3,0 m (C-18). Staffel 0,8 m zurückgesetzt. Rückseite: Grundstücksgrenze unbekannt.</text></svg>')
open(os.path.join(here, "..", "sections", "section_AA_arbeitsstand.svg"), "w", encoding="utf-8").write("\n".join(o))
print("ok")
