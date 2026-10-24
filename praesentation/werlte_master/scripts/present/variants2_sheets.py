"""Blätter Version 2: Gastronomie groß, Büros kompakt, Wohngeschosse abgestuft. Je Variante ein Blatt Grundrisse/Schnitt und ein Blatt Ansichten, dazu die Vergleichstabelle. HYPOTHETISCH."""
import sys, os, json
from lib import *
VD = json.load(open(os.path.join(ROOT, "geometry", "variants2_ABC.json"), encoding="utf-8")); MET = json.load(open(os.path.join(ROOT, "geometry", "variants2_metrics.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "varianten_v2"); os.makedirs(OUT, exist_ok=True)
NET = VD["net_factor"]; M = 1000 / 250
CLK, LARCH, GLASS, CONC = "#C9ADA3", "#DCC7A4", "#CFE0E8", "#D9DADC"
CORE_NAME = {"LOBBY": "Halle", "STAIR": "Treppe", "LANDING": "Flur", "LIFT": "AZ", "TECH": "T", "ABSTELL": "Abstell", "VORRAUM": None, "WAND": None}
VNAME = {"A": "Variante A", "B": "Variante B", "C": "Variante C"}
VTITLE = {"A": "Variante A – Obergeschosse moderat vergrößert (1,50 m)", "B": "Variante B – nach hinten erweitert und abgestuft (3,00 m / 1,50 m)", "C": "Variante C – maximal sinnvoll erweitert, abgestuft (4,50 m / 2,00 m)"}
def short(x): return f"{x:.0f}"
def hatch(s):
    if not any('id="hatch"' in d for d in s.defs):
        s.defs.append('<pattern id="hatch" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="#8A8F98" stroke-width="0.25"/></pattern>')
        s.defs.append('<pattern id="terr" width="1.8" height="1.8" patternUnits="userSpaceOnUse"><line x1="0" y1="0.9" x2="1.8" y2="0.9" stroke="#B49A72" stroke-width="0.3"/></pattern>')
def flat_labels(rs):
    out = {}
    for lv, p in (("L1", "1"), ("L2", "3")):
        fl = sorted([r for r in rs if r["level"] == lv and r["type"] == "apartment"], key=lambda r: (round(r["rect"][1]), r["rect"][0]))
        for i, r in enumerate(fl): out[r["id"]] = f"{p}.{i + 1:02d}"
    return out
def fit(s, cx, cy, w, h, l1, l2=None, fs=2.6, bold=True):
    need = max(tw(l1, fs, bold), tw(l2, fs) if l2 else 0) + 1.2
    if need <= w and h >= (6.2 if l2 else 3.4):
        if l2: s.text(cx, cy - 0.5, l1, fs, "middle", 600 if bold else 400); s.text(cx, cy + 2.9, l2, fs, "middle", 400, GREY)
        else: s.text(cx, cy + 0.9, l1, fs, "middle", 600 if bold else 400)
    elif l2 and tw(l1, fs, bold) + 1.2 <= w and h >= 3.4: s.text(cx, cy + 0.9, l1, fs, "middle", 600 if bold else 400)
    elif tw(l1, fs, bold) + 1.2 <= h and h > w: s.text(cx + 0.9, cy, l1, fs, "middle", 600, rot=-90)
    else: raise AssertionError(f"Label passt nicht: {l1} ({w:.1f}×{h:.1f} mm)")

def draw_plan(s, v, level, ox, oy, extras=True):
    rs = [r for r in v["rooms"] if r["level"] == level]; X = lambda x: ox + x * M; Y = lambda y: oy + y * M; m = MET[v["key"]]; fl = flat_labels(v["rooms"])
    for r in rs: s.rect(X(r["rect"][0]), Y(r["rect"][1]), (r["rect"][2] - r["rect"][0]) * M, (r["rect"][3] - r["rect"][1]) * M, FILL.get(r["type"], "#EEE"), None, 0)
    for r in rs: s.rect(X(r["rect"][0]), Y(r["rect"][1]), (r["rect"][2] - r["rect"][0]) * M, (r["rect"][3] - r["rect"][1]) * M, "none", GREY, 0.2)
    hatch(s); Y1 = v["depth_L1"]; y2 = v["y2"]
    if level == "L1": s.rect(X(4), Y(18), 28 * M, (Y1 - 18) * M, "url(#hatch)", None, 0)
    if level == "L2":
        t = v["roof_terrace"]; s.rect(X(t[0]), Y(t[1]), (t[2] - t[0]) * M, (t[3] - t[1]) * M, "url(#terr)", "#B49A72", 0.3)
        s.rect(X(0), Y(0), 32 * M, 18 * M, "none", LGREY, 0.3, "2 1.2")
        if Y1 > 18: s.rect(X(4), Y(18), 28 * M, (Y1 - 18) * M, "none", LGREY, 0.3, "2 1.2")
    o = v["outlines"][level]; s.poly([(X(a), Y(b)) for a, b in o], "none", INK, 0.6)
    sh = v["shaft"]["rect"]; s.rect(X(sh[0]), Y(sh[1]), (sh[2] - sh[0]) * M, (sh[3] - sh[1]) * M, "#F3D98B", INK, 0.3)
    if level == "L1":
        for b in v["balconies"]: s.rect(X(b["rect"][0]), Y(b["rect"][1]), 2.7 * M, 1.5 * M, "#F1F2F3", INK, 0.35)
    for r in rs:
        x0, y0, x1, y1 = r["rect"]; t = r["type"]; i = r["id"]; a = r["area_gross"]
        if t == "apartment" and level == "L1" and y1 > 18 and y0 < 18: y1e = 18.0 if False else y1
        w, h = (x1 - x0) * M, (y1 - y0) * M; cx, cy = X((x0 + x1) / 2), Y((y0 + y1) / 2)
        if t == "apartment": fit(s, cx, cy, w, h, fl[i], f"{short(a * NET)} m²")
        elif t == "office": fit(s, cx, cy, w, h, "Büro " + i.split("-")[1], f"ca. {short(a * NET)} m²")
        elif t == "corridor": fit(s, cx, cy, w, h, "Gang", None, bold=False)
        elif i == "DINING-GF": fit(s, cx, cy - 4, w, h, "Gastraum", f"ca. {short(m['dining'])} m² · ca. {m['seats']} Plätze")
        elif i == "BAR-GF": fit(s, cx, cy, w, h, "Bar", None)
        elif i == "PERSONAL-GF": fit(s, cx, cy, w, h, "Personal", f"{short(a)} m²")
        elif i == "WC-GF": fit(s, cx, cy, w, h, "WC", f"{short(a)} m²")
        elif i == "FLUR-GF": fit(s, cx, cy, w, h, "Flur", f"{short(a)} m²")
        elif i == "STORE-GF": fit(s, cx, cy, w, h, "Lager", f"{short(a)} m²")
        elif i == "KITCHEN-GF": fit(s, cx, cy, w, h, "Küche", f"{short(a)} m²")
        elif i == "ANLIEF-GF": fit(s, cx, cy, w, h, "Anlief.", f"{short(a)} m²")
        elif t == "core":
            nm = CORE_NAME.get(i.split("-")[0])
            if nm: fit(s, cx, cy, w, h, nm, None, 2.6, False)
    if level == "L2" and True:
        t = v["roof_terrace"]; s.text(X((t[0] + t[2]) / 2), Y((t[1] + t[3]) / 2) + 0.9, f"Dachterrasse {de(t[3] - t[1], 1)} m (Vorschlag)", 2.6, "middle", 600, "#6B5A3A", halo=True)
    if level == "GF":
        s.line(X(4), Y(0), X(32), Y(0), 1.2, "#7FA6BA")
        for a, b in ((17, 19), (29.5, 31), (1, 2.5)): s.line(X(a), Y(0), X(b), Y(0), 1.8, "#FFFFFF"); s.line(X(a), Y(0) - 0.9, X(a), Y(0) + 0.9, 0.4); s.line(X(b), Y(0) - 0.9, X(b), Y(0) + 0.9, 0.4)
        for a, b in v["parking"]["walkway_gaps"]: s.line(X(a), Y(18), X(b), Y(18), 1.8, "#FFFFFF")
        s.line(X(32), Y(15.5), X(32), Y(16.7), 1.8, "#FFFFFF")
        t = (6.0, -3.6, 30.0, 0.0); s.rect(X(t[0]), Y(t[1]), (t[2] - t[0]) * M, (t[3] - t[1]) * M, "#F3EBDD", GREY, 0.25, "1.4 0.9"); s.text(X(18), Y(-1.8) + 0.9, "Terrasse mit Stahlvordach", 2.6, "middle", 400, GREY)
        pk = v["parking"]
        s.rect(X(0), Y(0), 32 * M, 30 * M, "none", ACC, 0.35, "3 1 0.8 1"); s.rect(X(0), Y(23), 32 * M, 6 * M, "#F1F1EF", None, 0)
        for st in pk["stalls"]: s.rect(X(st[0]), Y(st[1]), 2.5 * M, 5 * M, "#E9EAEC", GREY, 0.2)
        if Y1 > 18:
            s.rect(X(4), Y(18), 28 * M, (Y1 - 18) * M, "url(#hatch)", None, 0, op=0.7); s.rect(X(4), Y(18), 28 * M, (Y1 - 18) * M, "none", INK, 0.3, "1.5 1")
        for cx_, cy_ in pk["columns"]: s.rect(X(cx_) - 0.7, Y(cy_) - 0.7, 1.4, 1.4, INK, INK, 0.1)
        ov = f"Auskragung 1. OG {de(v['e1'])} m (schraffiert)"
        s.text(X(16), Y(24.3) + 0.9, f"{len(pk['stalls'])} Stellplätze 2,50 × 5,00 m, {de(pk['covered_depth'], 1)} m von 5,00 m überdeckt", 2.6, "middle", 600)
        s.text(X(16), Y(26.6) + 0.9, "Fahrgasse 6,00 m (Annahme)", 2.6, "middle", 400, GREY)
        s.text(X(16), Y(28.6) + 0.9, "Hypothetische Grundstücksgrenze (Annahme 32 × 30 m)", 2.6, "middle", 400, ACC)

def draw_section(s, v, ox, gy):
    XC = 17.0; Y = lambda y: ox + (y + 3.6) * M; Z = lambda z: gy - z * M; Y1 = v["depth_L1"]; y2 = v["y2"]; rs = v["rooms"]; lab = flat_labels(rs); m = MET[v["key"]]
    zs = {"GF": (0.0, 3.2), "L1": (3.5, 6.2), "L2": (6.5, 9.3)}
    for lv, (z0, z1) in zs.items():
        for r in [r for r in rs if r["level"] == lv and r["rect"][0] < XC < r["rect"][2] and r["type"] != "bar"]:
            y0, y1 = r["rect"][1], r["rect"][3]
            s.rect(Y(y0), Z(z1), (y1 - y0) * M, (z1 - z0) * M, FILL.get(r["type"], "#EEE"), GREY, 0.2)
            i = r["id"]; nm = lab.get(i) or {"DINING-GF": "Gastraum", "FLUR-GF": "Flur", "STORE-GF": "Lager", "KITCHEN-GF": "Küche"}.get(i) or ("Büro " + i.split("-")[1] if r["type"] == "office" else "Gang")
            if tw(nm, 2.6, True) + 1 <= (y1 - y0) * M: s.text(Y((y0 + y1) / 2), Z((z0 + z1) / 2) + 0.9, nm, 2.6, "middle", 600)
    for z, a, b in ((3.5, 0, Y1), (6.5, 0, Y1), (9.6, 0.8, y2)): s.rect(Y(a), Z(z), (b - a) * M, 0.3 * M, INK, INK, 0.1)
    s.rect(Y(0.8), Z(9.9), 0.3 * M, 0.3 * M, INK, INK, 0.1); s.rect(Y(y2) - 0.3 * M, Z(9.9), 0.3 * M, 0.3 * M, INK, INK, 0.1)
    s.rect(Y(Y1) - 0.1 * M, Z(7.6), 0.1 * M, 1.1 * M, "#EAF1F3", INK, 0.3)                       # Terrassenbrüstung
    s.rect(Y(-1.5), Z(3.5), 1.5 * M, 0.3 * M, INK, INK, 0.1); s.rect(Y(-3.6), Z(3.1), 3.6 * M, 0.1 * M, INK, INK, 0.1)
    s.line(Y(-4.5), Z(0), Y(31.5), Z(0), 0.8, INK); s.rect(Y(18), Z(0.05), 5 * M, 0.05 * M, "#C8CBD0", GREY, 0.2)
    s.line(Y(30), Z(0), Y(30), Z(13), 0.35, ACC, "3 1 0.8 1"); s.text(Y(30) - 1.5, Z(12.2), "Grundstücksgrenze", 2.6, "end", 400, ACC); s.text(Y(30) - 1.5, Z(12.2) + 3.2, "(Annahme)", 2.6, "end", 400, ACC)
    for cx_, cy_ in v["parking"]["columns"][:1]: s.rect(Y(cy_) - 0.7, Z(3.2), 1.4, 3.2 * M, INK, INK, 0.1)
    xk = Y(-3.6) - 8
    for z, tx in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60")): s.line(xk - 1.2, Z(z), Y(-3.6) - 1, Z(z), 0.2, GREY, "1.4 1"); s.text(xk - 2, Z(z) + 0.9, tx, 2.6, "end", 600)
    dim_h(s, Y(18), Y(Y1), Z(11.2), f"{de(v['e1'])}") if v["e1"] > 0 else None
    s.text(Y(17.6), Z(11.2) + 0.9, "Auskragung 1. OG", 2.6, "end", 400, GREY)
    s.text(Y(y2) + 1.2, Z(10.4) + 0.9, f"Rücksprung Staffel", 2.6, "start", 400, GREY) if False else None
    s.text(Y(Y1) + 2.0, Z(6.5) - 1.8, f"Dachterrasse {de(m['terrasse_tiefe'], 1)} m", 2.6, "start", 400, "#6B5A3A")
    s.text(Y(18.4), Z(1.0) + 0.9, "h 3,20 m", 2.6, "start", 600)
    yb = gy + 11; dim_h(s, Y(0), Y(18), yb, "18,00"); dim_h(s, Y(18), Y(30), yb, "12,00 Rückbereich (Annahme)")
    s.text(Y(-1.8), Z(0) - 1.2, "Terrasse", 2.6, "middle", 400, GREY); s.text(Y(-3.6), 196.0, "Platzfassade links, Rückbereich rechts", 2.6, "start", 400, GREY)

def kenn(key):
    m = MET[key]
    return [("Außenmaß EG / 1. OG / 3. Geschoss", f"32×18 / 32×{de(m['depth_L1'], 1)} / 30,4×{de(m['y2'] - 0.8, 1)} m"), ("Auskragung 1. OG / Überstand Staffel", f"{de(m['e1'])} / {de(m['e2'])} m"),
            ("Gastronomie brutto, Innenplätze", f"ca. {short(m['gastro_brutto'])} m², ca. {m['seats']}"), ("Büros hinten, netto", f"ca. {short(m['buero_netto'])} m²"), ("Wohnungen, Wohnfläche netto", f"{m['we']}, ca. {short(m['wfl'])} m²"),
            ("Stellplätze, überdeckt", f"{m['stellplaetze']}, {de(m['ueberdacht'], 1)} von 5,0 m Tiefe")]
OFFEN = lambda key: [("C-30", f"Baufenster, GRZ und Zählung von Auskragungen unbekannt; Projektion {short(MET[key]['projektion'])} m² gegen theoretisch 576 m²: nicht nachweisbar zulässig."), ("C-28", "Stellplatzbedarf 61 laut Excel, hier 11 nachweisbar (Annahme)."),
                     ("C-29", "Grundstückszuschnitt, Zufahrt und Anlieferung unbekannt (hier 32 × 30 m angenommen)."), ("C-37", "Büros 56 m² statt 165 m²: Mieteinnahmen und Gastro-Pacht nicht neu gerechnet."), ("C-35", "Tragwerk der Auskragung" + (" und der 5 Stützen." if key == "C" else "."))]

def sheet_plans(key):
    v = VD["variants"][key]; m = MET[key]; s = Sheet(); no = {"A": 11, "B": 13, "C": 15}[key]
    drawing_title(s, VTITLE[key], "Grundrisse und Schnitt M 1:250 · HYPOTHETISCH: Grundstücksform, Baufenster und Rechtsfragen sind nicht belegt")
    ox1, ox2 = 22.0, 180.0
    s.text(ox1, 41, "Erdgeschoss 32 × 18 m mit Stellplätzen", 3.6, weight=600); s.text(ox2, 41, "1. Obergeschoss (nur Wohnungen)", 3.6, weight=600)
    draw_plan(s, v, "GF", ox1, 60.0); draw_plan(s, v, "L1", ox2, 54.0)
    s.text(ox2, 168, "3. Geschoss, Staffel (nur Wohnungen)", 3.6, weight=600); s.text(ox1, 190, "Schnitt bei x = 17,00 m", 3.6, weight=600)
    draw_plan(s, v, "L2", ox2, 176.0); draw_section(s, v, 36.0, 246.0)
    legend = [(lambda s, x, y: s.rect(x, y, 8, 4, FILL["apartment"], GREY, 0.2), "Wohnung, Nummer nach Geschoss (1.xx, 3.xx), Wohnfläche netto"), (lambda s, x, y: s.rect(x, y, 8, 4, FILL["office"], GREY, 0.2), "Büro (EG, hinten)"),
              (lambda s, x, y: s.rect(x, y, 8, 4, FILL["dining"], GREY, 0.2), "Gastraum und Bar"), (lambda s, x, y: s.rect(x, y, 8, 4, FILL["kitchen"], GREY, 0.2), "Küche, Lager, WC, Personal, Anlieferung (Anlief.)"),
              (lambda s, x, y: s.rect(x, y, 8, 4, FILL["core"], GREY, 0.2), "Kern: Halle, Treppe, Flur, Abstell (AZ Aufzug, T Technik)"), (lambda s, x, y: (hatch(s), s.rect(x, y, 8, 4, "url(#hatch)", GREY, 0.2, "1.5 1")), "Auskragung über Stellplätzen (hypothetisch)"),
              (lambda s, x, y: (hatch(s), s.rect(x, y, 8, 4, "url(#terr)", "#B49A72", 0.3)), "Dachterrasse auf dem 1. OG (Vorschlag)"),
              (lambda s, x, y: s.rect(x + 2, y + 0.5, 4, 3, "#F3D98B", INK, 0.3), "Küchenabluft-Schacht, alle Geschosse")]
    hint = ["Erdgeschoss in allen Varianten gleich. Der Anbau ist abgestuft: 1. OG weiter ausgekragt als die Staffel, dazwischen eine Dachterrasse.", "Flächen netto = Brutto × 0,88 (Annahme). Fenster, Türen und Wandstärken sind nicht festgelegt. Keine Variante ist festgelegt."]
    frame(s, f"{VNAME[key]} – Grundrisse und Schnitt", "Maßstab 1:250 (A3)", kenn(key), legend, OFFEN(key), hint, no)
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, f"{no}_Variante_{key}_Grundrisse.svg"), "w", encoding="utf-8").write(s.svg()); print("geschrieben", no)

# ---------- Ansichten ----------
def shade(hexc, f):
    c = hexc.lstrip("#"); r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4)); return "#%02X%02X%02X" % tuple(max(0, min(255, int(x * f))) for x in (r, g, b))
MAT = {"klinker": CLK, "laerche": LARCH}
def elevation_view(s, v, view, ox, gy, title, depth_ref):
    boxes = v["boxes"]; Y1 = v["depth_L1"]; y2 = v["y2"]; Z = lambda z: gy - z * M
    if view == "front": P = lambda x, y: ox + (32 - x) * M; key = lambda b: -b["y"][0]; face = lambda b: ("y", b["y"][0], b["x"]); span = lambda b: (32 - b["x"][1], 32 - b["x"][0]); shd = 1.0
    if view == "rear": P = lambda x, y: ox + x * M; key = lambda b: b["y"][1]; face = lambda b: ("y", b["y"][1], b["x"]); span = lambda b: (b["x"][0], b["x"][1]); shd = 1.0
    if view == "west": P = lambda x, y: ox + y * M; key = lambda b: -b["x"][0]; face = lambda b: ("x", b["x"][0], b["y"]); span = lambda b: (b["y"][0], b["y"][1]); shd = 0.93
    if view == "east": P = lambda x, y: ox + (depth_ref - y) * M; key = lambda b: b["x"][1]; face = lambda b: ("x", b["x"][1], b["y"]); span = lambda b: (depth_ref - b["y"][1], depth_ref - b["y"][0]); shd = 0.93
    s.text(ox - 10, gy - 52, title, 3.4, weight=600)
    for b in sorted(boxes, key=key):
        a0, a1 = span(b); s.rect(ox + a0 * M, Z(b["z"][1]), (a1 - a0) * M, (b["z"][1] - b["z"][0]) * M, shade(MAT[b["m"]], shd), INK, 0.4)
    # Attika
    ys = [b for b in boxes if b["n"].startswith("L2")]
    for b in ys:
        a0, a1 = span(b); s.rect(ox + a0 * M, Z(9.9), (a1 - a0) * M, 0.3 * M, "#8E9399", None, 0); s.line(ox + a0 * M, Z(9.9), ox + a1 * M, Z(9.9), 0.4, INK)
    # Platzseite: Glasfront, Türen, Balkone, Fenster schematisch
    def win(x0, x1, z0, z1, a=None):
        s.rect(a if a is not None else x0, Z(z1), x1 - x0, (z1 - z0) * M, "#F5F6F7", GREY, 0.25, "1.2 0.8")
    rooms = v["rooms"]
    if view == "front":
        px = lambda x: ox + (32 - x) * M
        s.rect(px(32), Z(3.1), 28 * M, 3.1 * M, GLASS, INK, 0.4)
        for a, b, hh in ((17, 19, 2.4), (29.5, 31, 2.4), (1, 2.5, 2.4)): s.rect(px(b), Z(hh), (b - a) * M, hh * M, "#FFFFFF" if a != 1 else GLASS, INK, 0.4)
        for i in range(5):
            x0 = 4 + 5.6 * i; s.rect(px(x0 + 4.7), Z(6.1), 3.8 * M, 2.2 * M, "#F5F6F7", GREY, 0.25, "1.2 0.8")
            bx = v["balconies"][i]["rect"]; s.rect(px(bx[2]), Z(3.5), 2.7 * M, 0.3 * M, CONC, INK, 0.4); s.rect(px(bx[2]), Z(4.6), 2.7 * M, 1.1 * M, "#EAF1F3", INK, 0.35, op=0.85)
        for r in rooms:
            if r["id"].startswith("WE-L2-V"): x0, x1 = r["rect"][0], r["rect"][2]; s.rect(px(x1 - 1.0), Z(9.0), (x1 - x0 - 2.0) * M, 2.1 * M, "#F5F6F7", GREY, 0.25, "1.2 0.8")
        c = (6.0, 30.0); s.rect(px(30), Z(3.1), 24 * M, 0.1 * M, INK, INK, 0.2)
    if view == "rear":
        px = lambda x: ox + x * M
        for r in rooms:
            if r["id"].startswith("WE-L1-H"):
                x0, x1 = r["rect"][0], r["rect"][2]; s.rect(px(x0 + 1.6), Z(6.1), 3.8 * M, 2.2 * M, "#F5F6F7", GREY, 0.25, "1.2 0.8")
            if r["id"].startswith("WE-L2-H"):
                x0, x1 = r["rect"][0], r["rect"][2]; s.rect(px(x0 + 1.6), Z(9.0), 5.8 * M, 2.1 * M, "#F5F6F7", GREY, 0.25, "1.2 0.8")
        for a, b in v["parking"]["walkway_gaps"]: s.rect(px(a), Z(2.4), (b - a) * M, 2.4 * M, GLASS, INK, 0.4)
        s.rect(px(4), Z(7.6), 28 * M, 1.1 * M, "#EAF1F3", INK, 0.35, op=0.85)       # Terrassenbrüstung
        for cx_, cy_ in v["parking"]["columns"]: s.rect(px(cx_) - 0.7, Z(3.2), 1.4, 3.2 * M, INK, INK, 0.1)
        for a, b in [(2.5, 5.0)]: pass
    if view == "west":
        for r in rooms: pass
    if view == "east":
        px = lambda y: ox + (depth_ref - y) * M
        s.rect(px(16.7), Z(2.4), 1.2 * M, 2.4 * M, "#FFFFFF", INK, 0.4)
    wmax = (32 if view in ("front", "rear") else depth_ref)
    s.line(ox - 3, Z(0), ox + wmax * M + 3, Z(0), 0.9, INK)
    if view in ("front", "west"):
        for z, tx in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60")):
            s.line(ox - 9, Z(z), ox - 5, Z(z), 0.4, INK); s.text(ox - 10, Z(z) + 0.9, tx, 2.6, "end", 600)
    dim_h(s, ox, ox + wmax * M, gy + 9, de(wmax) if view in ("front", "rear") else f"{de(depth_ref)} (1. OG)")

def sheet_views(key):
    v = VD["variants"][key]; m = MET[key]; s = Sheet(); no = {"A": 12, "B": 14, "C": 16}[key]; dr = v["depth_L1"]
    drawing_title(s, VTITLE[key].replace("Variante", "Ansichten Variante", 1), "Schematische Ansichten M 1:250 · Fenster- und Türlage schematisch, Maße nicht definiert · Material und Farbe unverändert")
    elevation_view(s, v, "front", 34.0, 100.0, "Ansicht Platzseite", dr); elevation_view(s, v, "rear", 174.0, 100.0, "Ansicht Rückseite", dr)
    elevation_view(s, v, "west", 34.0, 215.0, "Seitenansicht Kernseite (x = 0)", dr); elevation_view(s, v, "east", 174.0, 215.0, "Seitenansicht Ostseite (x = 32)", dr)
    for (ox, gy) in ((24.0, 100.0), (180.0, 100.0)):
        for z, tx in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60")): pass
    s.text(24.0, 130.0, "Höhen: ±0,00 Oberkante Erdgeschoss, +3,50 1. OG, +6,50 Traufe nach B-Plan und Staffel, +9,60 Staffeldecke, +9,90 Attika", 2.6, fill=GREY)
    s.text(24.0, 245.0, "Kernseite: Platzfassade links, Rückseite rechts. Ostseite: Platzfassade rechts, Rückseite links. Himmelsrichtung unbekannt (C-13).", 2.6, fill=GREY)
    legend = [(lambda s, x, y: s.rect(x, y, 8, 4, CLK, GREY, 0.2), "Klinker, dunkelrotbraun (hier aufgehellt)"), (lambda s, x, y: s.rect(x, y, 8, 4, LARCH, GREY, 0.2), "Lärchenholz im Staffelgeschoss"), (lambda s, x, y: s.rect(x, y, 8, 4, CONC, GREY, 0.2), "Betonbalkonplatte"),
              (lambda s, x, y: s.rect(x, y, 8, 4, "#EAF1F3", GREY, 0.2), "Milchglas-Brüstung, 1,10 m"), (lambda s, x, y: s.rect(x, y, 8, 4, GLASS, GREY, 0.2), "Glas und Türen"), (lambda s, x, y: s.rect(x, y, 8, 4, "#F5F6F7", GREY, 0.25, "1.2 0.8"), "Fensterlage schematisch (Maße offen)")]
    offen = [("C-13", "Himmelsrichtung und Platzseite unbekannt; Seiten sind nach dem Kern benannt."), ("C-19", "Rückfassade, Seitenfassaden und Dachterrasse sind nicht Teil des eingefrorenen Designs."), ("C-30", f"Auskragung und Staffelung: Baufenster, GRZ und Abstände unbekannt."),
             ("C-35", "Tragwerk der Auskragung" + (" und der Stützen." if key == "C" else ".")), ("C-22", "Abluftführung über Dach (Austritt) ist nicht dargestellt.")]
    hint = ["Der Anbau ist abgestuft: 1. OG weiter ausgekragt als die Staffel, dazwischen eine Dachterrasse. Die Rückseite folgt dem Material der Platzfassade (Klinker, Lärchenholz).", "Die Seitenfassaden zeigen die Stufung von Erdgeschoss, 1. OG und Staffel.",
            "Die bestehende Platzfassade (dunkler Klinker, Holz, fünf Balkone) bleibt die Grundlage."]
    kk = [("Gebäudetiefe Erdgeschoss", "18,00 m"), ("Tiefe 1. OG / Staffel", f"{de(m['depth_L1'])} / {de(m['y2'] - 0.8)} m"), ("Höhe Attika", "9,90 m"), ("Dachterrasse hinten", f"{de(m['terrasse_tiefe'], 1)} m tief")]
    frame(s, f"Ansichten {VNAME[key]}", "Maßstab 1:250 (A3)", kk, legend, offen, hint, no)
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, f"{no}_Variante_{key}_Ansichten.svg"), "w", encoding="utf-8").write(s.svg()); print("geschrieben", no)

def table():
    s = Sheet(); A, B, C = (MET[k] for k in "ABC"); K = "ABC"
    drawing_title(s, "Vergleich der Varianten A, B und C (Version 2)", "Gastronomie großzügig, Büros kompakt, Wohngeschosse abgestuft. Alle Werte hypothetisch und aus der Geometrie berechnet; keine Variante ist festgelegt.")
    x0 = 14.0; cw = [62, 79, 79, 80]; xs = [x0, x0 + 62, x0 + 141, x0 + 220]; y = 38.0
    for j, h in enumerate(["Kriterium", "A: moderat vergrößert", "B: erweitert und abgestuft", "C: maximal sinnvoll, abgestuft"]): s.text(xs[j] + 1.5, y, h, 3.0, weight=600)
    s.line(x0, y + 2, x0 + 300, y + 2, 0.5, INK); y += 7
    de0 = lambda x: f"{x:,.0f}".replace(",", ".")
    rows = [("Gebäudeform", ["Anbau 1,50 m; Staffel bündig mit EG-Rückwand; Dachterrasse 2,3 m", "Anbau 3,00 m; Staffel 1,50 m kürzer; Treppenform mit Dachterrasse 2,3 m", "Anbau 4,50 m; Staffel 2,00 m; Treppenform mit Dachterrasse 3,3 m; 5 Stützen"]),
            ("Außenmaße EG / 1. OG / 3. Geschoss", [f"32 × 18 / 32 × {de(MET[k]['depth_L1'], 1)} / 30,4 × {de(MET[k]['y2'] - 0.8, 1)} m" for k in K]),
            ("Projizierte Fläche (1. OG), GRZ-Zahl", [f"{de0(MET[k]['projektion'])} m², {de(MET[k]['grz'])} (Grenze theoretisch 576 m²)" for k in K]),
            ("Geschossfläche gesamt, Kubatur (Näherung)", [f"BGF {de0(MET[k]['bgf'])} m², BRI ca. {de0(MET[k]['bri'])} m³" for k in K]),
            ("Gastronomie brutto (Erdgeschoss)", [f"ca. {de0(MET[k]['gastro_brutto'])} m², davon Gastraum mit Bar {de0(MET[k]['dining'])} m²" for k in K]),
            ("Innenplätze (geschätzt) und Terrasse", [f"ca. {MET[k]['seats']} innen (2,1 m² je Platz + 12 Barhocker), 60 Terrasse" for k in K]),
            ("Büros hinten im EG", [f"2 Büros, ca. {de0(MET[k]['buero_netto'])} m² netto ({de0(MET[k]['buero_brutto'])} m² brutto)" for k in K]),
            ("Wohnungen (1. OG + 3. Geschoss)", [f"{MET[k]['we_L1']} + {MET[k]['we_L2']} = {MET[k]['we']}" for k in K]),
            ("Wohnungsgrößen netto (m²)", [", ".join(de0(x) for x in MET[k]["groessen"]) for k in K]),
            ("Wohnfläche netto gesamt", [f"ca. {de0(MET[k]['wfl'])} m² (Excel-Stand 655 m²)" for k in K]),
            ("Zusätzliche Wohnfläche gegenüber A", ["–", f"+{de0(B['wfl'] - A['wfl'])} m² (+{de0((B['wfl'] / A['wfl'] - 1) * 100)} %)", f"+{de0(C['wfl'] - A['wfl'])} m² (+{de0((C['wfl'] / A['wfl'] - 1) * 100)} %)"]),
            ("Überdachte Stellplätze", [f"{MET[k]['stellplaetze']} Plätze, {de(MET[k]['ueberdacht'], 1)} von 5,0 m Tiefe überdeckt" for k in K]),
            ("Stützen, Rangierfläche, Durchfahrt", ["keine Stütze; Fahrgasse 6,00 m (192 m²); h 3,20 m", "keine Stütze; Fahrgasse 6,00 m (192 m²); h 3,20 m", "5 Stützen an der Auskragungskante; Fahrgasse 6,00 m; h 3,20 m"]),
            ("Wohnqualität", ["Vorn 5 Studios mit Balkon, hinten 4 Wohnungen 58 m²; Terrasse nur 2,3 m", "Vorn wie A, hinten 4 Wohnungen 68 m², Staffel hinten 69 m²", "Vorn 5 Wohnungen 44 m², hinten 71 m², Staffel 49 und 65 m²; Tiefe/Breite höchstens 1,64"]),
            ("Nachweisstatus", ["Projektion über 576 m²: nicht nachweisbar", "Projektion über 576 m²: nicht nachweisbar", "Projektion über 576 m²: nicht nachweisbar"])]
    def lines(t, w, fs=3.0, b=False):
        ws, line, n = t.split(), "", 1
        for wd in ws:
            tt = (line + " " + wd).strip()
            if tw(tt, fs, b) <= w or not line: line = tt
            else: n += 1; line = wd
        return n
    for k, vals in rows:
        n = max([lines(k, cw[0] - 3, 3.0, True)] + [lines(v, cw[j + 1] - 3) for j, v in enumerate(vals)])
        for j, t in enumerate([k] + vals): s.wrap(xs[j] + 1.5, y, t, cw[j] - 3, 3.0, 1.35, 600 if j == 0 else 400)
        y += n * 3.0 * 1.35 + 3.6; s.line(x0, y - 1.8, x0 + 300, y - 1.8, 0.15, LGREY)
    assert y < 276, y
    offen = [("C-30", "Baufenster, GRZ und Zählung von Auskragungen sind unbekannt: alle drei Varianten übersteigen die theoretische GRZ-Fläche."), ("C-28", "Stellplätze: Bedarf 61, nachweisbar nur 11 (Annahme)."), ("C-29", "Grundstückszuschnitt (hier 32 × 30 m angenommen), Zufahrt, Anlieferung unbekannt."),
             ("C-37", "Büros 56 m² statt 165 m²: Mieteinnahmen und Gastro-Pacht nicht neu gerechnet."), ("C-35", "Tragwerk der Auskragungen offen.")]
    hint = ["Erdgeschoss in allen Varianten gleich. Gastronomie: Gastraum 280 m², Küche 60, Lager 27, WC 24, Personal 20, Flur 20, Anlieferung 9.", "Wohnungsgrößen netto = Brutto × 0,88 (Annahme).", "Keine Renderings, keine Förderthemen."]
    frame(s, "Vergleich der Varianten A, B und C", "Tabelle", [("Erdgeschoss", "in allen Varianten 32 × 18 m")], None, offen, hint, 17)
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, "17_Vergleich_ABC.svg"), "w", encoding="utf-8").write(s.svg()); print("geschrieben Vergleich")

if __name__ == "__main__":
    for a in sys.argv[1:]:
        table() if a == "table" else (sheet_plans if a[0] == "p" else sheet_views)(a[1:])
