"""Platzfassade, Schnitt A–A und Wohnungsstudie im Präsentationsstil. Geometrie nur aus building_design.json (und unit_study.py für die Wohnung)."""
import sys, os
sys.path.insert(0, os.path.join(HERE := os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import *
from plan import NET, name, lab
OUT = os.path.join(ROOT, "praesentation_zeichnungen")
HINT = ["Flächen netto = Brutto × 0,88 (Annahme).", "Himmelsrichtung unbekannt (C-13). Förderthemen sind nicht Gegenstand dieses Blatts."]
def save(s, fname):
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, fname + ".svg"), "w", encoding="utf-8").write(s.svg()); print("geschrieben", fname)
def sw(fill, stroke=GREY, w=8, h=4, dash=None):
    return lambda s, x, y: s.rect(x, y, w, h, fill, stroke, 0.25, dash)
CLK, LARCH, GLASS, CONC = "#C9ADA3", "#DCC7A4", "#D3E3EA", "#D9DADC"
LV = {l["id"]: l for l in D["levels"]}

def elevation():
    ME = 150; M = 1000 / ME; s = Sheet()
    ox, gy = 78.0, 192.0
    X = lambda x: ox + x * M; Z = lambda z: gy - z * M
    drawing_title(s, "Ansicht Platzfassade – Arbeitsstand OG-2", "Ansicht M 1:150 · Fensterlage schematisch, Fenstermaße sind noch nicht festgelegt")
    st = [r for r in D["staffel"]["rooms"]]
    sx0 = min(r["rect"][0] for r in D["core"]["L2"]); sx1 = max(r["rect"][2] for r in st if r["type"] == "apartment")
    # Baukörper
    s.rect(X(0), Z(6.5), 32 * M, 6.5 * M, CLK, INK, 0.5)
    s.rect(X(sx0), Z(9.6), (sx1 - sx0) * M, 3.1 * M, LARCH, INK, 0.5)
    s.rect(X(sx0), Z(D["attika_top"]), (sx1 - sx0) * M, (D["attika_top"] - 9.6) * M, "#8E9399", INK, 0.35)
    # EG: Glasfront, Türen
    gl = next(o for o in D["openings"] if o["id"].startswith("RESTAURANT"))
    s.rect(X(gl["x"][0]), Z(gl["height"]), (gl["x"][1] - gl["x"][0]) * M, gl["height"] * M, GLASS, INK, 0.4)
    for o in D["openings"][1:]:
        a, b = o["x"]; s.rect(X(a), Z(o["height"]), (b - a) * M, o["height"] * M, "#FFFFFF" if o["id"].endswith("REST-001") else GLASS, INK, 0.5)
        if o["type"] == "door_double": s.line(X((a + b) / 2), Z(o["height"]), X((a + b) / 2), Z(0), 0.3, INK)
    # 1. OG: Fensterlage schematisch und Balkone
    for i, b in enumerate(D["balconies"][:5]):
        x0 = 4 + 5.6 * i
        s.rect(X(x0 + 0.9), Z(6.1), 3.8 * M, 2.2 * M, "#F5F6F7", GREY, 0.3, "1.2 0.8")
        bx0, _, bx1, _ = b["rect"]
        s.rect(X(bx0), Z(3.5), (bx1 - bx0) * M, 0.3 * M, CONC, INK, 0.45)
        s.rect(X(bx0), Z(4.6), (bx1 - bx0) * M, 1.1 * M, "#EAF1F3", INK, 0.35, op=0.8)
    # Staffel: Fensterlage schematisch
    for r in st:
        if r["type"] == "apartment" and r["rect"][1] == 0.8:
            x0, _, x1, _ = r["rect"]; s.rect(X(x0 + 1.0), Z(9.0), (x1 - x0 - 2.0) * M, 2.1 * M, "#F5F6F7", GREY, 0.3, "1.2 0.8")
    # Vordach
    c = D["canopy"]["rect"]; s.rect(X(c[0]), Z(D["canopy"]["underside_z"] + 0.1), (c[2] - c[0]) * M, 0.1 * M, INK, INK, 0.3)
    # Gelände
    s.line(X(-1.5), Z(0), X(33.5), Z(0), 0.9, INK)
    # Raster
    for i, x in enumerate(D["grid"]["x"]):
        s.line(X(x), Z(11.7), X(x), Z(10.2) if False else Z(D["attika_top"]) - 1, 0.18, "#B9615A", "5 1.2 0.8 1.2"); bubble(s, X(x), Z(11.7) - 3.4, str(i + 1))
        s.line(X(x), Z(0) + 1, X(x), Z(0) + 8, 0.18, "#B9615A", "5 1.2 0.8 1.2")
    # Höhenkoten links
    xk = X(0) - 14
    for z, t in ((0, "±0,00  Oberkante Erdgeschoss"), (3.5, "+3,50  Oberkante 1. OG"), (6.5, "+6,50  Traufe (B-Plan), Oberkante Staffel"), (9.6, "+9,60  Oberkante Staffel-Decke"), (D["attika_top"], "+9,90  Oberkante Attika")):
        s.line(xk - 1.5, Z(z), X(0) - 2, Z(z), 0.2, GREY, "1.4 1")
        s.line(xk - 1.5, Z(z), xk + 1.5, Z(z), 0.5, INK)
    # Höhenmarken als Text rechtsbündig links neben der Achse
    for z, t in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60"), (D["attika_top"], "+9,90")):
        s.text(xk - 3, Z(z) + 1.0 + {9.6: 1.9, 9.9: -1.1}.get(z, 0), t, 2.7, "end", 600)
    for (z0, z1, t) in ((0, 3.5, "3,50"), (3.5, 6.5, "3,00"), (6.5, 9.6, "3,10")):
        s.line(X(32) + 8, Z(z0), X(32) + 8, Z(z1), 0.2, INK)
        for z in (z0, z1): s.line(X(32) + 7.1, Z(z) + 0.9, X(32) + 8.9, Z(z) - 0.9, 0.3, INK)
        s.text(X(32) + 6.7, Z((z0 + z1) / 2), t, 2.6, "end", rot=-90, halo=True) if False else s.text(X(32) + 9.8, Z((z0 + z1) / 2) + 1.0, t, 2.6)
    for zc, tx in ((1.75, "Erdgeschoss"), (5.0, "1. Obergeschoss"), (8.05, "Staffelgeschoss")):
        s.text(xk - 17, Z(zc) + 1.0, tx, 2.7, "end", 400, GREY)
    # Maße unten
    gx = D["grid"]["x"]; yd = Z(0) + 13
    dim_h(s, X(0), X(4), yd, "4,00")
    for a, b in zip(gx[:-1], gx[1:]): dim_h(s, X(a), X(b), yd, de(b - a))
    dim_h(s, X(0), X(32), yd + 7, "32,00")
    flag(s, X(18) - 4.5, Z(2.0) - 12.0 if False else Z(3.0) + 6, "C-18") if False else None
    flag(s, X(8) , Z(3.0) + 5.5, "C-18")
    flag(s, X(24.5), Z(3.0) + 5.5, "C-16")
    flag(s, X(2.2) - 3, Z(9.9) - 7, "C-25") if False else flag(s, X(0.9) - 1, Z(9.9) - 6.0, "C-25")
    flag(s, X(14) , Z(9.9) - 6.0, "C-21")
    scale_bar(s, 14, 268, 150, 5)
    legend = [(sw(CLK), "Klinker (dunkelrotbraun, hier aufgehellt dargestellt)"), (sw(CONC), "Betonbalkonplatte"), (sw("#EAF1F3", INK), "Milchglas-Brüstung, 1,10 m"), (sw(GLASS, INK), "Glasfront und Türen im Erdgeschoss"),
              (sw(LARCH), "Lärchenholz Staffelgeschoss"), (sw("#F5F6F7", GREY, dash="1.2 0.8"), "Fensterlage schematisch (Maße offen)"), (lambda s, x, y: s.rect(x, y + 1.5, 8, 1, INK, INK, 0.2), "Stahlvordach (Annahme, Unterseite +3,00)")]
    frame(s, "Ansicht Platzfassade – Arbeitsstand OG-2", "Maßstab 1:150 (A3)", [("Gebäudebreite", "32,00 m"), ("Höhe Attika", "9,90 m"), ("Traufhöhe nach B-Plan", "6,50 m")], legend,
          [("C-16", "Stützen oder Träger in der 28 m langen Glasfront nicht nachgewiesen."), ("C-18", "Stahlvordach liegt unter den Balkonplatten."), ("C-21", "Staffel: Entwurf 4 Achsen, 1. OG 5, Renderings 7."), ("C-25", "Aufzug: Überfahrt über die Attika offen."), ("C-03", "Höhenmessregel der Stadt unbestätigt.")],
          ["Platzfassade mit fünf Balkonen im 1. OG. Staffelgeschoss 0,80 m zurückgesetzt, hier nicht sichtbar."] + HINT, 4)
    save(s, "04_Ansicht_Platzfassade")

def section():
    MS = 100; M = 1000 / MS; s = Sheet()
    ox, gy = 78.0, 188.0
    Y = lambda y: ox + (y + 3.6) * M; Z = lambda z: gy - z * M
    drawing_title(s, "Schnitt A–A bei x = 18,00 m – Arbeitsstand OG-2", "Schnitt M 1:100 · Platzfassade links, Rückseite rechts · Schnittebene schneidet Wohnung WE-L1-S3, Büro 2, Bar und WC")
    XC = 18.0
    cut = lambda r: r["rect"][0] < XC < r["rect"][2]
    zs = {"GF": (0.0, 3.2), "L1": (3.5, 6.2), "L2": (6.5, 9.3)}
    rooms = {"GF": [r for r in D["rooms"] if r["level"] == "GF" and r["type"] != "core"], "L1": D["upper_options"]["OG-2"]["rooms"], "L2": [r for r in D["staffel"]["rooms"] if r["type"] != "core"]}
    for lv, rs in rooms.items():
        z0, z1 = zs[lv]
        for r in rs:
            if cut(r):
                y0, y1 = r["rect"][1], r["rect"][3]
                s.rect(Y(y0), Z(z1), (y1 - y0) * M, (z1 - z0) * M, FILL.get(r["type"], "#EEE"), "#FFFFFF", 0.0)
        for r in rs:
            if cut(r):
                y0, y1 = r["rect"][1], r["rect"][3]; s.rect(Y(y0), Z(z1), (y1 - y0) * M, (z1 - z0) * M, "none", GREY, 0.25)
                l1, l2 = lab(r); wmm = (y1 - y0) * M; cx = Y((y0 + y1) / 2); cy = Z((z0 + z1) / 2)
                if l1 == "Gastraum": l2 = None
                if tw(l1, 2.8, True) + 1.5 > wmm: l1 = {"Bar": "Bar"}.get(l1, l1)
                s.text(cx, cy - 0.6, l1, 2.8, "middle", 600)
                if l2 and tw(l2, 2.6) + 1.5 <= wmm: s.text(cx, cy + 3.0, l2, 2.6, "middle", 400, GREY)
    # Decken (Dicke 0,30 m)
    t = D["slab_thickness"]
    for z, y0, y1 in ((3.5, 0, 18), (6.5, 0, 18), (D["levels"][2]["top"], 0.8, 17.2)):
        s.rect(Y(y0), Z(z), (y1 - y0) * M, t * M, INK, INK, 0.2) if z != 9.6 else s.rect(Y(y0), Z(z), (y1 - y0) * M, t * M, INK, INK, 0.2)
    # Decken liegen unter Fußbodenoberkante: oberhalb zeichnen verschoben
    # Attika
    s.rect(Y(0.8), Z(D["attika_top"]), (17.2 - 0.8) * M, (D["attika_top"] - 9.6) * M, "#8E9399", INK, 0.3) if False else None
    s.rect(Y(0.8) - 0.1, Z(D["attika_top"]), 0.5 * M * 0.0 + 0.3 * M, (D["attika_top"] - 9.6) * M, INK, INK, 0.2)
    s.rect(Y(17.2) - 0.3 * M, Z(D["attika_top"]), 0.3 * M, (D["attika_top"] - 9.6) * M, INK, INK, 0.2)
    # Balkon (Schnitt durch Balkon 3 bei x = 18) und Vordach
    b = D["balconies"][2]["rect"]
    s.rect(Y(b[1]), Z(3.5), (b[3] - b[1]) * M, 0.3 * M, INK, INK, 0.2)
    s.line(Y(b[1]), Z(3.5), Y(b[1]), Z(4.6), 0.7, GREY)
    c = D["canopy"]["rect"]; s.rect(Y(c[1]), Z(D["canopy"]["underside_z"] + 0.1), (c[3] - c[1]) * M, 0.1 * M, INK, INK, 0.3)
    # Terrasse und Gelände
    s.line(Y(-4.5), Z(0), Y(19.5), Z(0), 0.9, INK)
    ter = D["terrace"]["rect"]; s.rect(Y(ter[1]), Z(0.12), (ter[3] - ter[1]) * M, 0.12 * M, "#C9A97C", INK, 0.2)
    # Umlauf
    s.text(Y(0.75), Z(6.5) - 2.2, "Umlauf 0,80", 2.6, "end", 400, GREY)
    s.text(Y(-1.6), Z(4.2), "Balkon", 2.6, "end", 400, GREY)
    s.text(Y(-3.6) - 1.5, Z(3.0) + 1.0, "UK Vordach +3,00", 2.6, "end", 400, GREY)
    for zc, tx in ((1.75, "Erdgeschoss"), (5.0, "1. Obergeschoss"), (8.05, "Staffelgeschoss")):
        s.text(Y(-3.6) - 31, Z(zc) + 1.0, tx, 2.7, "end", 400, GREY)
    # Höhenkoten (links)
    xk = Y(-3.6) - 14
    zl = [(0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60"), (D["attika_top"], "+9,90")]
    for z, tx in zl:
        s.line(xk - 1.5, Z(z), Y(-3.6) - 2, Z(z), 0.2, GREY, "1.4 1"); s.line(xk - 1.5, Z(z), xk + 1.5, Z(z), 0.5, INK); s.text(xk - 3, Z(z) + 1.0 + {9.6: 1.9, 9.9: -1.1}.get(z, 0), tx, 2.7, "end", 600)
    s.text(xk - 3, Z(3.0) + 1.0, "+3,00 Vordach UK", 2.5, "end", 400, GREY) if False else None
    # Geschosshöhen rechts
    xr = Y(18) + 8
    for z0, z1, tx in ((0, 3.5, "3,50"), (3.5, 6.5, "3,00"), (6.5, 9.6, "3,10")):
        s.line(xr, Z(z0), xr, Z(z1), 0.2, INK)
        for z in (z0, z1): s.line(xr - 0.9, Z(z) + 0.9, xr + 0.9, Z(z) - 0.9, 0.3, INK)
        s.text(xr + 2.0, Z((z0 + z1) / 2) + 1.0, tx, 2.6)
    # Beschriftung Bauteile mit Leitlinien
    def lead(px, py, tx, ty, txt, anchor="start"):
        s.line(px, py, tx, ty, 0.2, GREY); s.text(tx + (1.5 if anchor == "start" else -1.5), ty + 1.0, txt, 2.6, anchor, 400)
    # Maße unten
    yd = gy + 12
    ys = [-3.6, 0, 8, 10, 18]
    for a, bb, tx in ((-3.6, 0, "3,60"), (0, 8, "8,00"), (8, 10, "2,00"), (10, 18, "8,00")): dim_h(s, Y(a), Y(bb), yd, tx)
    dim_h(s, Y(0), Y(18), yd + 7, "18,00")
    for lx, tx, a in ((-1.8, "Terrasse", "middle"),):
        s.text(Y(lx), Z(0) - 2.0, tx, 2.6, a, 400, GREY)
    s.text(Y(-1.8), Z(3.0) + 4.6, "Stahlvordach", 2.6, "middle", 400, GREY)
    s.text(Y(-0.75), Z(3.5) - 2.0, "Balkon", 2.5, "middle", 400, GREY) if False else None
    flag(s, Y(-3.4), Z(3.0) + 9.5, "C-18")
    flag(s, Y(8), Z(9.9) - 3.5, "C-02")
    scale_bar(s, 14, 268, 100, 5)
    legend = [(sw(FILL["apartment"]), "Wohnung"), (sw(FILL["office"]), "Büro"), (sw(FILL["dining"]), "Gastraum, Bar (Gastronomie)"), (sw(FILL["kitchen"]), "WC und Nebenräume"), (sw(FILL["corridor"]), "Mittelgang"),
              (lambda s, x, y: s.rect(x, y + 1.2, 8, 1.6, INK, INK, 0.2), "Geschossdecke, Dicke 0,30 m"), (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 0.9, INK), "Gelände")]
    frame(s, "Schnitt A–A bei x = 18,00 m – Arbeitsstand OG-2", "Maßstab 1:100 (A3)", [("Geschosshöhen", "3,50 / 3,00 / 3,10 m"), ("Höhe Attika", "9,90 m"), ("Deckendicke", "0,30 m (Annahme)")], legend,
          [("C-18", "Balkonplatte (Unterseite +3,20) und Vordach (Unterseite +3,00) überlappen."), ("C-02", "Staffelgeschoss gilt voraussichtlich als Vollgeschoss."), ("C-19", "Rückseitiger Balkon liegt nicht in dieser Schnittebene."), ("C-22", "Küchenabluft-Schacht liegt nicht in dieser Schnittebene.")],
          ["Wände sind nur als Raumgrenzen dargestellt, Wandstärken sind noch nicht festgelegt.", "Die Schnittebene liegt auf Balkon 3 (Mitte). Terrasse und Vordach nach Annahme (Lage ungeprüft)."] + HINT, 5)
    save(s, "05_Schnitt_AA")

def unit():
    sys.path.insert(0, os.path.join(HERE, ".."))
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        import unit_study as U
    M = 1000 / 45; s = Sheet(); ox, oy = 48.0, 86.0
    X = lambda x: ox + x * M; Y = lambda y: oy + y * M
    Wi, Di = U.W, U.D
    drawing_title(s, "Wohnung WE-L1-S (1. OG, vorn) – Nutzbarkeitsprobe", "Grundriss M 1:45 · Möblierungsprobe zur Prüfung der Eigenständigkeit, keine Optimierung der Wohnungszahl")
    zc = {"Wohnen/Schlafen (vorn)": "#F7F0E8", "Flur/Küche": "#F1EEE9", "Bad": "#E3ECF0"}
    for n, r in U.R.items(): s.rect(X(r[0]), Y(r[1]), (r[2] - r[0]) * M, (r[3] - r[1]) * M, zc[n], None, 0)
    # Bewegungsflächen
    for n, r in U.Z.items(): s.rect(X(r[0]), Y(r[1]), (r[2] - r[0]) * M, (r[3] - r[1]) * M, "#BBD3E3", "#5B87A6", 0.2, "1.2 0.8", op=0.45)
    # Möbel
    short = {"Bett 1,4x2,0": "Bett", "Kleiderschrank 1,2x0,6": "Schrank", "Sofa 2,0x0,9": "Sofa", "Tisch 0,8x0,8": "Tisch", "Küchenzeile 2,4x0,6": "Küchenzeile", "Dusche 1,0x1,0": "Dusche", "WC 0,5x0,7": "WC", "Waschtisch 0,6x0,55": "WT", "Waschmaschine 0,6x0,6": "WM"}
    for n, r in U.F.items():
        s.rect(X(r[0]), Y(r[1]), (r[2] - r[0]) * M, (r[3] - r[1]) * M, "#EAE3D9", INK, 0.3)
        cx, cy = X((r[0] + r[2]) / 2), Y((r[1] + r[3]) / 2); t = short[n]
        if (r[3] - r[1]) > (r[2] - r[0]) * 1.5 and tw(t, 2.6) > (r[2] - r[0]) * M - 2: s.text(cx + 1.0, cy, t, 2.6, "middle", 400, rot=-90)
        else: s.text(cx, cy + 0.9, t, 2.6, "middle")
    # Wände
    s.rect(X(0), Y(0), Wi * M, Di * M, "none", INK, 1.0)
    s.line(X(3.0), Y(4.45), X(3.0), Y(Di), 0.6, INK); s.line(X(3.0), Y(4.45), X(Wi), Y(4.45), 0.6, INK)
    s.rect(X(3.0) - 0.5, Y(5.3), 1.0, 0.9 * M, "#FFFFFF", None, 0); s.line(X(3.0), Y(5.3), X(3.0), Y(6.2), 0.3, GREY, "1.2 0.8")
    s.rect(X(2.075), Y(0) - 0.7, 1.2 * M, 1.4, "#FFFFFF", None, 0); s.line(X(2.075), Y(0) - 0.35, X(3.275), Y(0) - 0.35, 0.25, INK); s.line(X(2.075), Y(0) + 0.35, X(3.275), Y(0) + 0.35, 0.25, INK)
    s.rect(X(1.9), Y(Di) - 0.7, 0.9 * M, 1.4, "#FFFFFF", None, 0); s.line(X(1.9), Y(Di) - 0.4, X(2.8), Y(Di) - 0.4, 0.25, INK)
    # Balkon
    s.rect(X(1.325), Y(-1.5), 2.7 * M, 1.5 * M, "#F1F2F3", INK, 0.45); s.rect(X(1.325) + 0.5, Y(-1.5) + 0.5, 2.7 * M - 1.0, 1.5 * M - 1.0, "none", GREY, 0.2)
    s.text(X(2.675), Y(-0.75) + 1.0, "Balkon 2,70 × 1,50 m", 2.7, "middle", 400, GREY)
    # Raumbeschriftung
    a = U.area
    s.text(X(3.2), Y(3.05), "Wohnen / Schlafen", 2.8, "middle", 600); s.text(X(3.2), Y(3.05) + 3.4, f"{de(a['Wohnen/Schlafen (vorn)'], 1)} m²", 2.7, "middle", 400, GREY)
    s.text(X(2.45), Y(4.8), "Flur / Küche", 2.8, "middle", 600); s.text(X(2.45), Y(4.8) + 3.4, f"{de(a['Flur/Küche'], 1)} m²", 2.7, "middle", 400, GREY)
    s.text(X(4.3), Y(4.85), f"Bad {de(a['Bad'], 1)} m²", 2.8, "middle", 600)
    s.text(X(2.2), Y(Di) + 4.6, "Wohnungstür vom Mittelgang", 2.6, "middle", 400, GREY)
    # Maße
    yb = Y(Di) + 11
    dim_h(s, X(0), X(Wi), yb, de(Wi)); 
    dim_v(s, X(0) - 8, Y(0), Y(4.45), "4,45"); dim_v(s, X(0) - 8, Y(4.45), Y(Di), "2,90"); dim_v(s, X(0) - 16, Y(0), Y(Di), de(Di))
    dim_h(s, X(1.325), X(4.025), Y(-1.5) - 5, "2,70")
    s.text(X(0), Y(-1.5) - 12, "Platzfassade", 2.7, "start", 600, GREY)
    scale_bar(s, 14, 276, 45, 2)
    # Raumprogramm und Befund (rechts der Zeichnung)
    x0, w0, y = 168.0, 140.0, 44.0
    s.text(x0, y, "RAUMPROGRAMM (INNENMASS)", 2.6, weight=600, fill=GREY); s.line(x0, y + 1.6, x0 + w0, y + 1.6, 0.2, LGREY); y += 7
    for k, v in (("Wohnen / Schlafen (vorn, an der Platzfassade)", a["Wohnen/Schlafen (vorn)"]), ("Flur / Küche (innenliegend)", a["Flur/Küche"]), ("Bad (innenliegend)", a["Bad"])):
        s.text(x0, y, k, 3.0); s.text(x0 + w0, y, f"{de(v, 1)} m²", 3.0, "end", 600); y += 5.2
    s.line(x0, y - 2.8, x0 + w0, y - 2.8, 0.3, INK)
    s.text(x0, y + 0.8, f"Summe Innenmaß {de(Wi, 2)} × {de(Di, 2)} m", 3.0, weight=600); s.text(x0 + w0, y + 0.8, f"{de(Wi * Di, 1)} m²", 3.0, "end", 600); y += 5.2
    s.text(x0, y + 0.8, "Modellwert Wohnfläche netto (Brutto 44,8 m² × 0,88)", 2.8, fill=GREY); s.text(x0 + w0, y + 0.8, "39,4 m²", 2.8, "end", 400, GREY); y += 5.2
    s.text(x0, y + 0.8, "Balkon (nicht in der Wohnfläche)", 2.8, fill=GREY); s.text(x0 + w0, y + 0.8, "4,05 m²", 2.8, "end", 400, GREY); y += 11
    s.text(x0, y, "BEFUND DER NUTZBARKEITSPROBE (KEIN RECHTSURTEIL)", 2.6, weight=600, fill=GREY); s.line(x0, y + 1.6, x0 + w0, y + 1.6, 0.2, LGREY); y += 7
    for t in ("Eigenständig nutzbar als Studio-Wohnung für 1 Person, mit Einschränkung für 2 Personen.",
              "Alle Möbel und Bewegungsflächen der Probe passen ohne Überlappung in den Grundriss.",
              "Ein separates Schlafzimmer ist nicht möglich: zwei Räume an der Fassade wären nur ca. 2,6 m breit.",
              "Einseitige Belichtung über eine Fassadenachse, keine Querlüftung. Küche und Bad liegen innen und brauchen mechanische Lüftung.",
              "Balkon und Schlafplatz liegen über der Gastro-Terrasse: Schall und Betriebszeiten sind nicht geprüft (C-26).",
              "Kein Abstellraum in der Wohnung; Abstellräume nur im Kern, Zweck offen.",
              "Als rollstuhlgerechte Wohnung kommt dieser Typ voraussichtlich nicht in Frage (C-27)."):
        s.text(x0, y, "•", 3.0); y = s.wrap(x0 + 4, y, t, w0 - 4, 3.0, 1.4) + 2.0
    y += 3
    s.text(x0, y, "ANNAHMEN", 2.6, weight=600, fill=GREY); s.line(x0, y + 1.6, x0 + w0, y + 1.6, 0.2, LGREY); y += 7
    y = s.wrap(x0, y, "Wandstärken: Fassade 0,45 m, Wohnungstrennwand 0,25 m, Flurwand 0,20 m. Möbelmaße und Bewegungsflächen sind übliche Planungswerte, keine Rechtsvorgaben.", w0, 2.8, 1.4)
    assert y < 270, y
    legend = [(lambda s, x, y: s.rect(x, y, 8, 4, "#EAE3D9", INK, 0.3), "Möbel (WT Waschtisch, WM Waschmaschine)"), (lambda s, x, y: s.rect(x, y, 8, 4, "#BBD3E3", "#5B87A6", 0.2, "1.2 0.8", op=0.45), "freizuhaltende Bewegungsfläche, 1,20 × 1,20 m bzw. 0,60 m seitlich"),
              (sw("#F1F2F3", INK), "Balkon"), (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 1.0, INK), "Wand (Annahme)"), (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 0.3, GREY, "1.2 0.8"), "Schiebetür Bad")]
    frame(s, "Wohnung WE-L1-S – Nutzbarkeitsprobe", "Maßstab 1:45 (A3)", [("Wohnungen dieses Typs", "WE-L1-S1 bis S5"), ("Wohnfläche netto (Modell)", "ca. 39,4 m²"), ("Innenmaß", "5,35 × 7,35 m")], legend,
          [("C-26", "Einseitig belichtet, Lage über Gastro-Terrasse, kein Abstellraum."), ("C-27", "Rollstuhlgerechte Wohnung: Kandidaten sind nur die größeren Typen."), ("C-07", "Wohnungsgrundrisse sind noch keine Planung, nur Probe.")],
          ["Fenster- und Türmaße sind nicht festgelegt; Balkontür 1,20 m und Wohnungstür 0,90 m sind Annahmen der Probe.", "Himmelsrichtung unbekannt (C-13). Förderthemen sind nicht Gegenstand dieses Blatts."], 6)
    save(s, "06_Wohnung_WE-L1-S")

if __name__ == "__main__":
    for w in sys.argv[1:]: globals()[w]()
