"""Blätter für die Varianten A, B, C (Grundrisse EG, 1. OG, 3. Geschoss, Schnitt) und die Vergleichstabelle. Alle Varianten HYPOTHETISCH."""
import sys, os, json
from lib import *
VD = json.load(open(os.path.join(ROOT, "geometry", "variants_ABC.json"), encoding="utf-8")); MET = json.load(open(os.path.join(ROOT, "geometry", "variants_metrics.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "varianten"); os.makedirs(OUT, exist_ok=True)
NET = VD["net_factor"]; M = 1000 / 250          # Maßstab 1:250
CORE_NAME = {"LOBBY": "Halle", "STAIR": "Treppe", "LANDING": "Flur", "LIFT": "AZ", "TECH": "T", "ABSTELL": "Abstell", "VORRAUM": None, "WAND": None}
VNAME = {"A": "Variante A", "B": "Variante B", "C": "Variante C"}
VTITLE = {"A": "Variante A – Erdgeschoss 32 × 18 m, Obergeschosse wie bisher", "B": "Variante B – Wohngeschosse 3,00 m nach hinten ausgekragt", "C": "Variante C – Wohngeschosse 6,00 m ausgekragt, Stellplätze überdeckt"}
VSUB = {"A": "Erdgeschoss 32 × 18 m, Obergeschosse in der bisherigen Geometrie", "B": "Auskragung der Wohngeschosse nach hinten um 3,00 m", "C": "Auskragung der Wohngeschosse nach hinten um 6,00 m, Stellplätze überdeckt"}
def short(x): return f"{x:.0f}".replace(".", ",")

def flat_labels(rs):
    out = {}
    for lv, p in (("L1", "1"), ("L2", "3")):
        fl = sorted([r for r in rs if r["level"] == lv and r["type"] == "apartment"], key=lambda r: (round(r["rect"][1]), r["rect"][0]))
        for i, r in enumerate(fl): out[r["id"]] = f"{p}.{i + 1:02d}"
    return out

def hatch(s):
    if not any("hatch" in d for d in s.defs):
        s.defs.append('<pattern id="hatch" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="#8A8F98" stroke-width="0.25"/></pattern>')

def fit(s, cx, cy, w, h, l1, l2=None, fs=2.6, bold=True):
    need = max(tw(l1, fs, bold), tw(l2, fs) if l2 else 0) + 1.2
    if need <= w and h >= (6.2 if l2 else 3.4):
        if l2: s.text(cx, cy - 0.5, l1, fs, "middle", 600 if bold else 400); s.text(cx, cy + 2.9, l2, fs, "middle", 400, GREY)
        else: s.text(cx, cy + 0.9, l1, fs, "middle", 600 if bold else 400)
    elif l2 and tw(l1, fs, bold) + 1.2 <= w and h >= 3.4: s.text(cx, cy + 0.9, l1, fs, "middle", 600 if bold else 400)
    elif tw(l1, fs, bold) + 1.2 <= h and h > w: s.text(cx + 0.9, cy, l1, fs, "middle", 600, rot=-90)
    else: raise AssertionError(f"Label passt nicht: {l1} ({w:.1f}×{h:.1f} mm)")

def draw_plan(s, v, level, ox, oy, par=False):
    rs = [r for r in v["rooms"] if r["level"] == level]; X = lambda x: ox + x * M; Y = lambda y: oy + y * M; D1 = v["depth_upper"]; L = v["rear_cantilever"]
    fl = flat_labels(v["rooms"])
    fillmap = dict(FILL)
    for r in rs: s.rect(X(r["rect"][0]), Y(r["rect"][1]), (r["rect"][2] - r["rect"][0]) * M, (r["rect"][3] - r["rect"][1]) * M, fillmap.get(r["type"], "#EEE"), None, 0)
    for r in rs: s.rect(X(r["rect"][0]), Y(r["rect"][1]), (r["rect"][2] - r["rect"][0]) * M, (r["rect"][3] - r["rect"][1]) * M, "none", GREY, 0.2)
    # Außenkontur
    env = {"GF": (0, 0, 32, 18), "L1": (0, 0, 32, D1), "L2": (0.8, 0.8, 31.2, D1 - 0.8)}[level]
    s.rect(X(env[0]), Y(env[1]), (env[2] - env[0]) * M, (env[3] - env[1]) * M, "none", INK, 0.6)
    if L > 0 and level in ("L1", "L2"):
        hatch(s); y0 = 18.0
        s.rect(X(env[0]), Y(y0), (env[2] - env[0]) * M, (env[3] - y0) * M, "url(#hatch)", None, 0)
        s.line(X(env[0]), Y(y0), X(env[2]), Y(y0), 0.3, INK, "1.5 1")
        s.text(X(env[2]), Y(env[3]) + 4.2, f"Auskragung {de(L)} m (hypothetisch, schraffiert)", 2.6, "end", 600, INK)
    if level == "GF": 
        s.rect(X(0), Y(0), 32 * M, 18 * M, "none", INK, 0.6)
        if L > 0: s.rect(X(0), Y(18), 32 * M, L * M, "none", GREY, 0.3, "1.5 1")
    # Schacht
    sh = v["shaft"]["rect"]; s.rect(X(sh[0]), Y(sh[1]), (sh[2] - sh[0]) * M, (sh[3] - sh[1]) * M, "#F3D98B", INK, 0.3)
    # Balkone
    if level == "L1":
        for b in v["balconies"]: s.rect(X(b["rect"][0]), Y(b["rect"][1]), 2.7 * M, 1.5 * M, "#F1F2F3", INK, 0.35)
    # Beschriftung
    for r in rs:
        x0, y0, x1, y1 = r["rect"]
        if L > 0 and level in ("L1", "L2") and y0 < 18 < y1: y1 = 18.0
        w, h = (x1 - x0) * M, (y1 - y0) * M; cx, cy = X((x0 + x1) / 2), Y((y0 + y1) / 2); t = r["type"]; i = r["id"]
        a = r["area_gross"]
        if t == "apartment": fit(s, cx, cy, w, h, fl[i], f"{short(a * NET)} m²")
        elif t == "office": fit(s, cx, cy, w, h, "Büro " + i.split("-")[1], f"ca. {short(a * NET)} m²")
        elif t == "corridor": fit(s, cx, cy, w, h, "Gang", None, bold=False)
        elif i == "DINING-GF": fit(s, cx, cy - 4, w, h, "Gastraum", f"ca. {short(MET[v['key']]['dining_brutto'])} m² · ca. {MET[v['key']]['seats_innen']} Plätze")
        elif i == "BAR-GF": fit(s, cx, cy, w, h, "Bar", None)
        elif i == "PERSONAL-GF": fit(s, cx, cy, w, h, "Personal", f"{short(a)} m²")
        elif i == "WC-GF": fit(s, cx, cy, w, h, "WC", f"{short(a)} m²")
        elif i == "STORE-GF": fit(s, cx, cy, w, h, "Lager", f"{short(a)} m²")
        elif i == "KITCHEN-GF": fit(s, cx, cy, w, h, "Küche", f"{short(a)} m²")
        elif t == "core":
            nm = CORE_NAME.get(i.split("-")[0])
            if nm: fit(s, cx, cy, w, h, nm, None, 2.6, False)
    # Eingänge und Glasfront im EG
    if level == "GF":
        s.line(X(4), Y(0), X(32), Y(0), 1.2, "#7FA6BA")
        for a, b in ((17, 19), (29.5, 31), (1, 2.5)): s.line(X(a), Y(0), X(b), Y(0), 1.8, "#FFFFFF"); s.line(X(a), Y(0) - 0.9, X(a), Y(0) + 0.9, 0.4); s.line(X(b), Y(0) - 0.9, X(b), Y(0) + 0.9, 0.4)
        for a, b in v["parking"]["walkway_gaps"]: s.line(X(a), Y(18), X(b), Y(18), 1.8, "#FFFFFF")
        s.line(X(32), Y(8.0), X(32), Y(9.2), 1.8, "#FFFFFF")
        t = (6.0, -3.6, 30.0, 0.0); s.rect(X(t[0]), Y(t[1]), (t[2] - t[0]) * M, (t[3] - t[1]) * M, "#F3EBDD", GREY, 0.25, "1.4 0.9"); s.text(X(18), Y(-1.8) + 0.9, "Terrasse mit Stahlvordach", 2.6, "middle", 400, GREY)
        pk = v["parking"]
        s.rect(X(0), Y(0), 32 * M, 30 * M, "none", ACC, 0.35, "3 1 0.8 1")
        s.rect(X(0), Y(23), 32 * M, 6 * M, "#F1F1EF", None, 0)
        for st in pk["stalls"]: s.rect(X(st[0]), Y(st[1]), 2.5 * M, 5 * M, "#E9EAEC", GREY, 0.2)
        s.text(X(16), Y(26.6) + 0.9, "Fahrgasse 6,00 m (Annahme)", 2.6, "middle", 400, GREY)
        s.text(X(16), Y(28.6) + 0.9, "Hypothetische Grundstücksgrenze (Annahme 32 × 30 m)", 2.6, "middle", 400, ACC)
        for cx_, cy_ in pk["columns"]: s.rect(X(cx_) - 0.7, Y(cy_) - 0.7, 1.4, 1.4, INK, INK, 0.1)
        s.text(X(16), Y(24.3) + 0.9, f"{len(pk['stalls'])} Stellplätze 2,50 × 5,00 m" + (" überdeckt" if pk["covered_depth"] >= 5 else (" teilweise überdeckt" if pk["covered_depth"] > 0 else "")), 2.6, "middle", 600, INK, halo=True)

def draw_section(s, v, ox, gy):
    XC = 17.0; Y = lambda y: ox + (y + 3.6) * M; Z = lambda z: gy - z * M; D1 = v["depth_upper"]; L = v["rear_cantilever"]; rs = v["rooms"]
    zs = {"GF": (0.0, 3.2), "L1": (3.5, 6.2), "L2": (6.5, 9.3)}
    cut = lambda r: r["rect"][0] < XC < r["rect"][2]
    lab = flat_labels(rs)
    for lv, (z0, z1) in zs.items():
        for r in [r for r in rs if r["level"] == lv and cut(r) and r["type"] != "bar"]:
            y0, y1 = r["rect"][1], r["rect"][3]
            s.rect(Y(y0), Z(z1), (y1 - y0) * M, (z1 - z0) * M, FILL.get(r["type"], "#EEE"), GREY, 0.2)
            t = r["type"]; i = r["id"]; nm = lab.get(i) or {"DINING-GF": "Gastraum", "STORE-GF": "Lager"}.get(i) or ("Büro " + i.split("-")[1] if t == "office" else "Gang")
            w = (y1 - y0) * M; cy = Z((z0 + z1) / 2)
            if tw(nm, 2.6, True) + 1 <= w: s.text(Y((y0 + y1) / 2), cy + 0.9, nm, 2.6, "middle", 600)
    for z, y0, y1 in ((3.5, 0, D1), (6.5, 0, D1), (9.6, 0.8, D1 - 0.8)): s.rect(Y(y0), Z(z), (y1 - y0) * M, 0.3 * M, INK, INK, 0.1)
    s.rect(Y(0.8), Z(9.9), 0.3 * M, 0.3 * M, INK, INK, 0.1); s.rect(Y(D1 - 0.8) - 0.3 * M, Z(9.9), 0.3 * M, 0.3 * M, INK, INK, 0.1)
    s.rect(Y(-1.5), Z(3.5), 1.5 * M, 0.3 * M, INK, INK, 0.1)
    s.rect(Y(-3.6), Z(3.1), 3.6 * M, 0.1 * M, INK, INK, 0.1)
    s.line(Y(-4.5), Z(0), Y(31.5), Z(0), 0.8, INK)
    pk = v["parking"]
    s.rect(Y(18), Z(0.05), 5 * M, 0.05 * M, "#C8CBD0", GREY, 0.2)
    s.line(Y(30), Z(0), Y(30), Z(13), 0.35, ACC, "3 1 0.8 1")
    s.text(Y(30) - 1.5, Z(12.2), "Grundstücksgrenze", 2.6, "end", 400, ACC); s.text(Y(30) - 1.5, Z(12.2) + 3.2, "(Annahme)", 2.6, "end", 400, ACC)
    for cx_, cy_ in pk["columns"][:1]: s.rect(Y(cy_) - 0.7, Z(3.2), 1.4, 3.2 * M, INK, INK, 0.1); s.text(Y(cy_) + 1.8, Z(2.7), "Stütze", 2.6, "start", 400, GREY)
    # Maße: Höhen links, Auskragung, Durchfahrtshöhe
    xk = Y(-3.6) - 8
    for z, tx in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60")):
        s.line(xk - 1.2, Z(z), Y(-3.6) - 1, Z(z), 0.2, GREY, "1.4 1"); s.text(xk - 2, Z(z) + 0.9, tx, 2.6, "end", 600)
    if L > 0:
        dim_h(s, Y(18), Y(18 + L), Z(10.9), f"Auskragung {de(L)}")
        s.line(Y(18 + L), Z(10.9) + 0.5, Y(18 + L), Z(6.5), 0.15, GREY, "1 1")
    yb = gy + 11
    dim_h(s, Y(0), Y(18), yb, "18,00"); dim_h(s, Y(18), Y(30), yb, "12,00 Rückbereich (Annahme)")
    dim_v(s, Y(18) + 3 * M * 0 + 0, Z(3.2), Z(0), "") if False else None
    s.text(Y(18.4), Z(1.0) + 0.9, "h 3,20 m", 2.6, "start", 600) if L >= 3 else None
    s.text(Y(-1.8), Z(0) - 1.2, "Terrasse", 2.6, "middle", 400, GREY)
    s.text(Y(-3.6), 196.0, "Platzfassade links, Rückbereich rechts", 2.6, "start", 400, GREY)

def sheet(key):
    v = VD["variants"][key]; m = MET[key]; s = Sheet(); D1 = v["depth_upper"]
    drawing_title(s, VTITLE[key], "Grundrisse und Schnitt M 1:250 · HYPOTHETISCH: Grundstücksform, Baufenster und Rechtsfragen sind nicht belegt")
    ox1, ox2 = 22.0, 180.0
    s.text(ox1, 41, "Erdgeschoss 32 × 18 m mit Stellplätzen", 3.6, weight=600); s.text(ox2, 41, "1. Obergeschoss (nur Wohnungen)", 3.6, weight=600)
    draw_plan(s, v, "GF", ox1, 60.0)
    draw_plan(s, v, "L1", ox2, 54.0)
    s.text(ox2, 162, "3. Geschoss, Staffel (nur Wohnungen)", 3.6, weight=600); s.text(ox1, 190, "Schnitt bei x = 17,00 m", 3.6, weight=600)
    draw_plan(s, v, "L2", ox2, 170.0)
    draw_section(s, v, 36.0, 246.0)
    ms = m
    kenn = [("Außenmaß Erdgeschoss", "32,00 × 18,00 m"), ("Außenmaß 1. Obergeschoss", f"32,00 × {de(D1)} m"), ("Außenmaß 3. Geschoss", f"30,40 × {de(D1 - 1.6)} m"), ("Auskragung hinten", f"{de(ms['auskragung_hinten_m'])} m"),
            ("Geschossflächen EG/1.OG/3.G", f"576 / {short(ms['flaeche_L1'])} / {short(ms['flaeche_L2'])} m²"), ("Wohnungen (1. OG + 3. Geschoss)", f"{ms['we_L1']} + {ms['we_L2']} = {ms['we_gesamt']}"), ("Wohnfläche netto gesamt", f"ca. {short(ms['wfl_gesamt'])} m²"),
            ("Gastronomie brutto", f"ca. {short(ms['gastro_brutto'])} m²"), ("Innenplätze (geschätzt)", f"ca. {ms['seats_innen']}"), ("Büros hinten im EG, netto", f"ca. {short(ms['buero_netto'])} m²"), ("Stellplätze (Annahme)", f"{ms['stellplaetze']} von 61 Bedarf")]
    legend = [(lambda s, x, y: s.rect(x, y, 8, 4, FILL["apartment"], GREY, 0.2), "Wohnung, Nummer nach Geschoss (1.xx, 3.xx), Wohnfläche netto"), (lambda s, x, y: s.rect(x, y, 8, 4, FILL["office"], GREY, 0.2), "Büro (EG, hinten)"),
              (lambda s, x, y: s.rect(x, y, 8, 4, FILL["dining"], GREY, 0.2), "Gastraum und Bar"), (lambda s, x, y: s.rect(x, y, 8, 4, FILL["kitchen"], GREY, 0.2), "Küche, Lager, WC, Personal"), (lambda s, x, y: s.rect(x, y, 8, 4, FILL["core"], GREY, 0.2), "Kern: Halle, Treppe, Flur, Abstell (AZ Aufzug, T Technik)"),
              (lambda s, x, y: (hatch(s), s.rect(x, y, 8, 4, "url(#hatch)", GREY, 0.2, "1.5 1")), "Auskragung (hypothetisch)"), (lambda s, x, y: s.rect(x + 1, y, 6, 4, "#E9EAEC", GREY, 0.2), "Stellplatz 2,50 × 5,00 m (Annahme)"),
              (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 0.35, ACC, "3 1 0.8 1"), "hypothetische Grundstücksgrenze"), (lambda s, x, y: s.rect(x + 2, y + 0.5, 4, 3, "#F3D98B", INK, 0.3), "Küchenabluft-Schacht, alle Geschosse")]
    offen = [("C-30", "Baufenster, GRZ und Zählung der Auskragungen unbekannt: " + ("Variante ohne Überschreitung der 576 m²." if key == "A" else f"Projektion {short(ms['projektion_gesamt'])} m², nicht nachweisbar zulässig.")),
             ("C-28", "Stellplatzbedarf 61 laut Excel, hier nur 11 Stellplätze nachweisbar."), ("C-29", "Grundstückszuschnitt, Zufahrt und Anlieferung unbekannt."), ("C-31", "Gastro 316 m² statt 504 m²: Umsatz und Pacht nicht neu gerechnet."),
             ("C-22", "Küchenabluft-Schacht läuft durch Wohnungen."), ("C-35", "Tragwerk: " + ("Raster 5,6 m gegen 5,0 m Stützenraster Stellplätze, 6 Stützen." if key == "C" else "Kragarm" if key == "B" else "keine Auskragung.")), ("C-36", "Fluchtwege EG nur als Annahme.")]
    hint = ["Erdgeschoss in allen Varianten gleich; Büros liegen hinter der Gastronomie, Wohnungen nur im 1. Obergeschoss und im 3. Geschoss.", "Flächen netto = Brutto × 0,88 (Annahme). Fenster, Türen und Wandstärken sind nicht festgelegt.", "Keine Variante ist festgelegt, keine Rendering-Erzeugung."]
    if key == "C": hint.insert(0, "Variante C ist die Obergrenze der Untersuchung, kein Vorschlag. Vordere Wohnungen sind 11 m tief bei 5,6 m Breite (Verhältnis 1,96).")
    frame(s, f"{VNAME[key]} – Grundrisse und Schnitt", "Maßstab 1:250 (A3)", kenn, legend, offen, hint, {"A": 7, "B": 8, "C": 9}[key])
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, f"0{ {'A':7,'B':8,'C':9}[key] }_Variante_{key}.svg"), "w", encoding="utf-8").write(s.svg()); print("geschrieben", key)

def table():
    s = Sheet(); A, B, C = (MET[k] for k in "ABC")
    drawing_title(s, "Vergleich der Varianten A, B und C", "Alle Werte hypothetisch und aus der Geometrie berechnet. Keine Variante ist festgelegt.")
    x0 = 14.0; cw = [66, 78, 78, 78]; xs = [x0, x0 + 66, x0 + 144, x0 + 222]; y = 38.0
    for j, h in enumerate(["Kriterium", "A: Obergeschosse wie bisher", "B: Auskragung 3,00 m", "C: Auskragung 6,00 m"]):
        s.text(xs[j] + 1.5, y, h, 2.9, weight=600)
    s.line(x0, y + 2, x0 + 300, y + 2, 0.5, INK); y += 7
    d = lambda k, f: [f(MET[x]) for x in "ABC"]
    rows = [("Außenmaße", [f"EG 32 × 18 · 1. OG 32 × {de(MET[k]['flaeche_L1'] / 32)} · 3. Geschoss 30,4 × {de(MET[k]['flaeche_L2'] / 30.4)} m" for k in "ABC"]),
            ("Auskragung und projizierte Fläche", [f"{de(MET[k]['auskragung_hinten_m'])} m · {short(MET[k]['projektion_gesamt'])} m² = GRZ {de(MET[k]['grz_projektion'])}" for k in "ABC"]),
            ("Geschossflächen und Kubatur (Näherung)", [f"BGF {MET[k]['bgf']:,.0f} m² · BRI ca. {MET[k]['bri_naeherung']:,} m³".replace(",", ".") for k in "ABC"]),
            ("Gastronomie (EG vorn und Mitte)", [f"ca. {short(MET[k]['gastro_brutto'])} m² brutto, Gastraum und Bar {short(MET[k]['dining_brutto'])} m²" for k in "ABC"]),
            ("Sitzplätze (geschätzt)", [f"ca. {MET[k]['seats_innen']} innen (2,1 m² je Platz) + 60 Terrasse" for k in "ABC"]),
            ("Büros im hinteren EG", [f"ca. {short(MET[k]['buero_netto'])} m² netto (100 + 65)" for k in "ABC"]),
            ("Wohnungen (1. OG + 3. Geschoss)", [f"{MET[k]['we_L1']} + {MET[k]['we_L2']} = {MET[k]['we_gesamt']}" for k in "ABC"]),
            ("Wohnungsgrößen netto (m²)", [", ".join(short(x) for x in MET[k]["wohnungsgroessen"]) for k in "ABC"]),
            ("Wohnfläche netto gesamt", [f"ca. {MET[k]['wfl_gesamt']:,.0f} m² (Excel-Stand 655 m²)".replace(",", ".") for k in "ABC"]),
            ("Wohnfläche je Geschossfläche (BGF)", [f"{MET[k]['wfl_gesamt'] / MET[k]['bgf'] * 100:.0f} %" for k in "ABC"]),
            ("Zusätzliche Wohnfläche gegenüber A", ["–", f"+{short(B['wfl_gesamt'] - A['wfl_gesamt'])} m² (+{short((B['wfl_gesamt'] / A['wfl_gesamt'] - 1) * 100)} %)", f"+{short(C['wfl_gesamt'] - A['wfl_gesamt'])} m² (+{short((C['wfl_gesamt'] / A['wfl_gesamt'] - 1) * 100)} %)"]),
            ("Wohnqualität", ["Vorn 5 Studios mit Balkon, hinten 1 Studio und 2 Dreizimmerwohnungen ohne Außenraum", "Vorn wie A, hinten 4 Wohnungen 68 m², Tiefe 11 m, ohne Außenraum", "Vorn 5 Wohnungen 54 m², Tiefe 11 m bei 5,6 m Breite (1,96), hinten wie B"]),
            ("Stellplätze, Rangierfläche (Annahme)", [f"{MET[k]['stellplaetze']} Plätze, Fahrgasse 6,00 m, {MET[k]['rangierflaeche']} m²; Bedarf 61" for k in "ABC"]),
            ("Überdachung und Stützen", ["keine", "3,00 m der 5,00 m Stelltiefe, keine Stützen", "voll überdeckt, 6 Stützen an der Stellplatzvorderkante"]),
            ("Durchfahrtshöhe unter Auskragung", ["–", "3,20 m (Plattenunterseite)", "3,20 m (Plattenunterseite)"]),
            ("Nachweisstatus", ["GRZ-Grenze erreicht, Baufenster ungeklärt", "Projektion 672 m², nicht nachweisbar", "Projektion 768 m², nicht nachweisbar"])]
    for k, vals in rows:
        hs = [s.wrap(xs[0] + 1.5, 0, k, cw[0] - 3, 2.7, 1.35, 600) if False else 0]
        # Höhe der Zeile aus dem längsten Umbruch bestimmen
        def lines(t, w, fs=3.1, b=False):
            ws, line, n = t.split(), "", 1
            for wd in ws:
                tt = (line + " " + wd).strip()
                if tw(tt, fs, b) <= w or not line: line = tt
                else: n += 1; line = wd
            return n
        n = max([lines(k, cw[0] - 3, 3.1, True)] + [lines(v, cw[j + 1] - 3) for j, v in enumerate(vals)])
        for j, t in enumerate([k] + vals):
            s.wrap(xs[j] + 1.5, y, t, cw[j] - 3, 3.1, 1.35, 600 if j == 0 else 400)
        y += n * 3.1 * 1.35 + 4.2
        s.line(x0, y - 2.0, x0 + 300, y - 2.0, 0.15, LGREY)
    assert y < 272, y
    kenn = [("Erdgeschoss", "in allen Varianten 32 × 18 m")]
    legend = None
    offen = [("C-30", "Baufenster, GRZ und Zählung von Auskragungen sind unbekannt: B und C nicht nachweisbar."), ("C-28", "Stellplätze: Bedarf 61, nachweisbar nur 11 (Annahme)."), ("C-29", "Grundstückszuschnitt (hier 32 × 30 m angenommen), Zufahrt, Anlieferung unbekannt."),
             ("C-31", "Gastronomie 316 m² statt 504 m²: Wirtschaftlichkeit nicht neu gerechnet."), ("C-35", "Tragwerk der Auskragungen offen."), ("C-33", "Hintere Wohnungen ohne Außenraum.")]
    hint = ["Gastronomie-Fläche aus Rest nach Kern (72 m²) und Büros (188 m² brutto): 316 m². Plätze: (Gastraum − Bar) / 2,1 m² + 12 Barhocker.", "Wohnungsgrößen netto = Brutto × 0,88 (Annahme).", "Fördertechnische Aspekte und neue Renderings sind nicht Teil dieses Blatts."]
    frame(s, "Vergleich der Varianten A, B und C", "Tabelle", kenn, legend, offen, hint, 10)
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, "10_Vergleich_ABC.svg"), "w", encoding="utf-8").write(s.svg()); print("geschrieben Vergleich")

if __name__ == "__main__":
    for a in sys.argv[1:]:
        table() if a == "table" else sheet(a)
