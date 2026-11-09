"""Runde 3: Arbeitsgrundlage B3 (Variante B, nur vorläufig). Blätter 21–27. Alle Werte hypothetisch oder ASSUMED, nichts freigegeben."""
import sys, os, json
from lib import *
import variants2_sheets as V2
D3 = json.load(open(os.path.join(ROOT, "geometry", "variant_B3.json"), encoding="utf-8")); MT = json.load(open(os.path.join(ROOT, "geometry", "variants3_metrics.json"), encoding="utf-8")); M2 = json.load(open(os.path.join(ROOT, "geometry", "variants2_metrics.json"), encoding="utf-8"))
FURN = D3["furnishing"]; OUT = os.path.join(ROOT, "varianten_v3"); os.makedirs(OUT, exist_ok=True); NET = D3["net_factor"]
VK = D3["variants"]["K"]; MK = MT["K"]
STAMP = "Stand 22.10.2026 · Arbeitsgrundlage B3 (Variante B, nicht festgelegt)"
sw = lambda fill, stroke=GREY, w=8, h=4, dash=None: (lambda s, x, y: s.rect(x, y, w, h, fill, stroke, 0.25, dash))
def save(s, name):
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(s.svg().replace("Stand 22.10.2026 · Modell NEUE_MITTE_MASTER_DRAFT_A_003", STAMP)); print("geschrieben", name)
def frame3(s, *a, **k):
    frame(s, *a, **k)
    # Schriftfeld-Zeile mit Modellstand ersetzen (Text im SVG wird beim Speichern ersetzt)

# ---------- Blatt 21: Gastronomie mit maßstäblicher Möblierung (1:100) ----------
def chairs(s, X, Y, t, fill="#D9D4CA"):
    x, y = t["x"], t["y"]
    for cx in (x + 0.15, x + 0.60):
        s.rect(X(cx), Y(y - 0.45), 0.45 * 10, 4.5, fill, GREY, 0.15); s.rect(X(cx), Y(y + 0.8), 0.45 * 10, 4.5, fill, GREY, 0.15)
def sheet21():
    s = Sheet(); M = 10.0; ox, oy = 20.0, 70.0
    X = lambda x: ox + (x - 4) * M; Y = lambda y: oy + y * M; fz = FURN["normal"]
    drawing_title(s, "Gastronomie – maßstäbliche Möblierung, Layout normal", "Grundriss M 1:100 · Tische 1,20 × 0,80 m (4 Plätze), Stühle 0,45 × 0,45 m, 12 Barhocker · Maße ASSUMED")
    rs = [r for r in VK["rooms"] if r["level"] == "GF" and r["id"] in ("DINING-GF", "BAR-GF", "WC-GF", "PERSONAL-GF", "FLUR-GF", "KITCHEN-GF", "STORE-GF", "ANLIEF-GF", "OFFICE-1-GF", "OFFICE-2-GF")]
    for r in rs: s.rect(X(r["rect"][0]), Y(r["rect"][1]), (r["rect"][2] - r["rect"][0]) * M, (r["rect"][3] - r["rect"][1]) * M, FILL.get(r["type"], "#EEE"), GREY, 0.25)
    s.rect(X(4), Y(0), 28 * M, 18 * M, "none", INK, 0.8)
    # Terrasse
    t = (6.0, -3.6, 30.0, 0.0); s.rect(X(t[0]), Y(t[1]), 24 * M, 3.6 * M, "#F3EBDD", GREY, 0.3, "2 1.2")
    for tt in fz["terrace"]["tables"]:
        s.rect(X(tt["x"]), Y(tt["y"]), 12, 8, "#FFFFFF", INK, 0.25); chairs(s, X, Y, tt)
    s.text(X(18), Y(-3.6) - 2.0, f"Terrasse mit Stahlvordach: {fz['terrace']['seats']} Plätze (Annahme der Planung: 60)", 2.8, "middle", 600, GREY)
    # Tische und Stühle
    for tt in fz["tables"]: chairs(s, X, Y, tt); s.rect(X(tt["x"]), Y(tt["y"]), 12, 8, "#FFFFFF", INK, 0.3)
    s.rect(X(5), Y(8.6), 10 * M, 1.4 * M, "#CFC8BB", INK, 0.4); s.text(X(10), Y(9.5) + 1.0, "Bartheke", 2.8, "middle", 600)
    for sx, sy in fz["stools"]: s.circle(X(sx), Y(sy), 2.0, "#FFFFFF", INK, 0.3)
    s.text(X(10), Y(7.45) + 1.0, "Barhocker 12", 2.6, "middle", 400, GREY)
    # Fluchtwege vor den Ausgängen
    for a, b in ((16.8, 19.2), (29.3, 31.2)):
        s.rect(X(a), Y(0), (b - a) * M, 10 * M, "#DDEFE0", None, 0, op=0.55); s.line(X(a), Y(0), X(a), Y(10), 0.2, "#4C9A5E", "2 1.2"); s.line(X(b), Y(0), X(b), Y(10), 0.2, "#4C9A5E", "2 1.2")
    s.text(X(18), Y(5.0), "Fluchtweg", 2.6, "middle", 600, "#2F7A44", rot=-90); s.text(X(30.25), Y(5.0), "Fluchtweg", 2.6, "middle", 600, "#2F7A44", rot=-90)
    # Fassade
    s.line(X(4), Y(0), X(32), Y(0), 1.6, "#7FA6BA")
    for a, b in ((17, 19), (29.5, 31)): s.line(X(a), Y(0), X(b), Y(0), 2.4, "#FFFFFF"); s.line(X(a), Y(0) - 1, X(a), Y(0) + 1, 0.5); s.line(X(b), Y(0) - 1, X(b), Y(0) + 1, 0.5)
    # Service-Bereich
    lab = {"WC-GF": ("WC", 24), "PERSONAL-GF": ("Personal", 20), "FLUR-GF": ("Flur, Anrichte", 20), "KITCHEN-GF": ("Küche", 60), "STORE-GF": ("Lager, Kühlung", 27), "ANLIEF-GF": ("Anlief.", 9), "OFFICE-1-GF": ("Büro 1", None), "OFFICE-2-GF": ("Büro 2", None)}
    for r in rs:
        i = r["id"]
        if i in lab:
            x0, y0, x1, y1 = r["rect"]; nm, a = lab[i]; cx, cy = X((x0 + x1) / 2), Y((y0 + y1) / 2)
            if a: s.text(cx, cy - 0.6, nm, 2.8, "middle", 600); s.text(cx, cy + 3.2, f"{a} m²", 2.8, "middle", 400, GREY)
            else: s.text(cx, cy - 0.6, nm, 2.8, "middle", 600); s.text(cx, cy + 3.2, f"ca. {r['area_gross'] * NET:.0f} m²", 2.8, "middle", 400, GREY)
    s.text(X(4) + 1.5, Y(0) + 5.0, "Gastraum und Bar 280 m²", 2.8, "start", 600) if False else None
    dim_h(s, X(4), X(32), Y(18) + 8, "28,00"); dim_v(s, X(4) - 8, Y(0), Y(10), "10,00"); dim_v(s, X(4) - 8, Y(10), Y(18), "8,00")
    # Plätze je Reihe
    rows = {}
    for tt in fz["tables"]: rows[tt["row"]] = rows.get(tt["row"], 0) + 1
    scale_bar(s, 14, 273, 100, 5)
    km = MK
    kenn = [("Gastraum und Bar", "280 m²"), ("Innenplätze realistisch (normal)", f"{km['seats']}"), ("  davon Barhocker", "12"), ("komfortabel / dicht", f"{km['seats_komf']} / {km['seats_dicht']}"), ("Flächenregel der letzten Fassung", f"{km['seats_regel']}"), ("Terrasse (normal)", f"{km['terrasse_plaetze']}"),
            ("Fläche je Platz (normal)", f"{280 / km['seats']:.1f} m²".replace(".", ","))]
    legend = [(sw("#FFFFFF", INK, 8, 4), "Tisch 1,20 × 0,80 m, 4 Plätze"), (sw("#D9D4CA", GREY, 8, 4), "Stuhl 0,45 × 0,45 m"), (lambda s, x, y: s.circle(x + 4, y + 2, 2.0, "#FFFFFF", INK, 0.3), "Barhocker"),
              (sw("#DDEFE0", "#4C9A5E", 8, 4, "2 1.2"), "Fluchtweg vor den Ausgängen, 2,40 und 1,90 m breit"), (sw("#F3EBDD", GREY, 8, 4, "2 1.2"), "Terrasse")]
    offen = [("C-20", "Gaststätte mit über 120 + 44 Plätzen: Einstufung als Sonderbau, Zahl der Ausgänge und Rettungsbreiten offen."), ("C-36", "Fluchtwege nur als Annahme; Küche und Personal über Flur und Anlieferung Ost."), ("C-38", "Barrierefreie Plätze und Fahrbahn für Rollstühle noch nicht nachgewiesen.")]
    hint = ["Die 138 Plätze der letzten Fassung waren eine Flächenregel (2,1 m² je Platz). Die Möblierung zeigt: realistisch sind etwa 120, komfortabel 88, sehr dicht 128. Die Gastronomie wird nicht weiter verkleinert.",
            f"Reihen im Layout normal: " + ", ".join(f"Reihe {k + 1}: {v} Tische" for k, v in sorted(rows.items())) + "."]
    frame(s, "Gastronomie – Möblierung", "Maßstab 1:100 (A3)", kenn, legend, offen, hint, 21)
    save(s, "21_Gastronomie_Moeblierung")

# ---------- Blatt 22: Büro-Zugang, WC und Flur (Alternativen) ----------
def sheet22():
    s = Sheet(); M = 1000 / 150; s.defs = []; XM = 21.5
    drawing_title(s, "Büros hinten – Zugang, Büro-WC und Flur (drei Alternativen)", "Grundrisse hinterer Erdgeschoss-Bereich M 1:150 · unabhängige Erreichbarkeit nur über die Rückseite, Fußweg vom Platz ungeklärt (C-29)")
    cells = {"K": (14.0, 40.0), "F": (162.0, 40.0), "M": (14.0, 160.0)}
    TITLES = {"K": "Alternative K: Büro-Foyer im Kern", "F": "Alternative F: Flur und WC zwischen den Büros", "M": "Alternative M: Mitbenutzung des Gäste-WC"}
    for alt, (cx, cy) in cells.items():
        v = D3["variants"][alt]; ox = cx; oy = cy + 12 - 11 * M * 0 - 9.5 * 0
        X = lambda x: ox + x * M; Y = lambda y: cy + 8 + (y - 10.5) * M
        s.text(cx, cy, TITLES[alt], 3.4, weight=600)
        rs = [r for r in v["rooms"] if r["level"] == "GF" and r["rect"][3] > 10.5 and r["rect"][1] < 18.5 and r["id"] not in ("DINING-GF", "BAR-GF")]
        for r in rs:
            x0, y0, x1, y1 = r["rect"]; y0 = max(y0, 10.5); x1 = min(x1, XM)
            if x0 >= XM: continue
            s.rect(X(x0), Y(y0), (x1 - x0) * M, (y1 - y0) * M, FILL.get(r["type"], "#EEE"), GREY, 0.25)
        for st in v["parking"]["stalls"]:
            if st[2] <= XM: s.rect(X(st[0]), Y(st[1]), 2.5 * M, 5 * M, "#EEEFF1", LGREY, 0.2)
        s.line(X(0), Y(18), X(XM), Y(18), 0.9, INK); s.line(X(0), Y(10.5), X(0), Y(18), 0.9, INK)
        for r in rs:
            x0, y0, x1, y1 = r["rect"]; i = r["id"]; w = (min(x1, XM) - x0) * M; h = (y1 - max(y0, 10.5)) * M; ccx, ccy = X((x0 + min(x1, XM)) / 2), Y((max(y0, 10.5) + y1) / 2)
            nm = {"OFFICE-1-GF": "Büro 1", "OFFICE-2-GF": "Büro 2", "BUERO-WC-GF": "WC", "BUERO-FOYER-GF": None, "BUERO-FOYER2-GF": "Foyer", "BUERO-FLUR-GF": "Flur", "WC-GF": "Gäste-WC", "PERSONAL-GF": "Personal", "FLUR-GF": "Flur", "STORE-GF": "Lager", "KITCHEN-GF": "Küche",
                  "LIFT-GF": "AZ", "ABSTELL-GF": "Abstell", "STAIR-GF": None, "LANDING-GF": "Flur", "TECH-GF": None, "WAND-LIFT-GF": None, "LOBBY-GF": None}.get(i)
            if x1 > XM and i not in ("OFFICE-1-GF", "OFFICE-2-GF"): continue
            if i in ("OFFICE-1-GF", "OFFICE-2-GF"):
                a = r["area_gross"] * NET; V2.fit(s, ccx, ccy, w, h, nm, f"{a:.0f} m²".replace(".", ","))
            elif nm and w >= tw(nm, 2.6, True) + 1.2 and h >= 3.4: s.text(ccx, ccy + 0.9, nm, 2.6, "middle", 600 if i.startswith(("OFFICE", "BUERO")) else 400, INK if i.startswith(("OFFICE", "BUERO")) else GREY)
        # Türen und Wege
        if alt == "K":
            doors = [(1.0, 2.5), (5.0, 6.5), (15.0, 16.5)]; inner = [(4.0, 16.4, 17.4)]
        elif alt == "F":
            doors = [(11.4, 13.4), (15.0, 16.5)]; inner = []
        else:
            doors = [(5.0, 6.5), (15.0, 16.5)]; inner = []
        for a, b in doors: s.line(X(a), Y(18), X(b), Y(18), 2.0, "#FFFFFF"); s.line(X(a), Y(18) - 1, X(a), Y(18) + 1, 0.5); s.line(X(b), Y(18) - 1, X(b), Y(18) + 1, 0.5)
        for a, b in [(5.0, 6.5)] if alt == "F" else []: pass
        # Weg von außen (grün) bzw. durch das Restaurant (rot)
        py = Y(19.6)
        if alt in ("K", "F"):
            s.line(X(1.5 if alt == "K" else 12.4), py, X(15.7), py, 0.5, "#4C9A5E", "2 1.2"); s.line(X(1.5 if alt == "K" else 12.4), py, X(1.5 if alt == "K" else 12.4), Y(18.3), 0.5, "#4C9A5E", "2 1.2")
            s.text(X(8), py + 3.6, "Zugang von der Rückseite", 2.6, "middle", 600, "#2F7A44")
        else:
            s.line(X(5.75), py, X(15.7), py, 0.5, "#4C9A5E", "2 1.2"); s.text(X(10), py + 3.6, "Zugang von der Rückseite", 2.6, "middle", 600, "#2F7A44")
            s.line(X(7), Y(10.5), X(7), Y(10.5) - 7, 0.6, "#B03A2E", "2 1.2"); s.text(X(7.6), Y(10.5) - 3.0, "WC-Weg durch das Restaurant", 2.6, "start", 600, "#B03A2E")
    # vierte Zelle: Vergleich
    x0, y = 162.0, 160.0; w0 = 138.0
    s.text(x0, y, "Vergleich der Alternativen", 3.4, weight=600); y += 7
    rowsT = [("", "K", "F", "M"), ("Gastronomie", "440 m²", "440 m²", "440 m²"), ("Büros netto", "56 m²", "48 m²", "56 m²"), ("Büro-WC", "im Foyer, 5 m²", "zwischen Büros, 5 m²", "Gäste-WC"), ("WC von beiden Büros erreichbar", "nur über außen", "ja, innen", "nur durch Restaurant"), ("unabhängig vom Restaurant", "ja (Rückseite)", "ja (Rückseite)", "nein (WC)"),
             ("Barrierefreier Zugang", "ja, eben", "ja, eben", "ja, eben"), ("Verlust", "Abstell Wohnen 16 m²", "Bürofläche −8 m²", "keiner")]
    cwid = [48, 30, 30, 30]; xs = [x0, x0 + 48, x0 + 78, x0 + 108]
    for ri, row in enumerate(rowsT):
        nl = 1
        for j, t in enumerate(row):
            nl = max(nl, len(s.__class__.wrap.__doc__ and [0] or [0]))
        hts = []
        for j, t in enumerate(row):
            ws, line, n = t.split(), "", 1
            for wd in ws:
                tt = (line + " " + wd).strip()
                if tw(tt, 2.7, ri == 0 or j == 0) <= cwid[j] - 2 or not line: line = tt
                else: n += 1; line = wd
            hts.append(n)
        for j, t in enumerate(row): s.wrap(xs[j], y, t, cwid[j] - 2, 2.7, 1.3, 600 if (ri == 0 or j == 0) else 400)
        y += max(hts) * 2.7 * 1.3 + 2.2; s.line(x0, y - 1.4, x0 + w0, y - 1.4, 0.15, LGREY)
    y += 2; y = s.wrap(x0, y, "Arbeitsstand: Alternative K (Büros bleiben je 28 m², Gastronomie unverändert). Sie kostet den Abstellraum Wohnen im Erdgeschoss; ein neuer Ort für Fahrrad und Abstell ist offen (C-38). Alternative F löst die Wege innen, verkleinert die Büros auf 25 und 22 m².", w0, 2.8, 1.35)
    assert y < 280, y
    legend = [(sw(FILL["office"]), "Büro"), (sw(FILL["foyer"]), "Büro-Foyer, Büro-Flur"), (sw(FILL["wc"]), "WC"), (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 0.5, "#4C9A5E", "2 1.2"), "Weg von der Rückseite"), (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 0.6, "#B03A2E", "2 1.2"), "Weg durch das Restaurant")]
    offen = [("C-32", "Büros nur rückseitig belichtet und erschlossen; Büro-WC jetzt in drei Alternativen geprüft."), ("C-29", "Fußweg vom Platz zur Rückseite und Grundstückszuschnitt unbekannt: unabhängige Erreichbarkeit nur unter dieser Voraussetzung."), ("C-38", "Abstell- und Fahrradraum Wohnen: neuer Ort offen."), ("C-36", "Fluchtwege der Büros: Rücktüren, nicht geprüft.")]
    frame(s, "Büros – Zugang, WC und Flur", "Maßstab 1:150 (A3)", [("Büro 1 und 2 (K)", "je ca. 28 m² netto"), ("Foyer mit Büro-WC (K)", "ca. 16 m² brutto")], legend, offen, ["Gastronomie bleibt bei 440 m²; keine Fläche wird ohne Alternativen abgegeben.", "Flächen netto = Brutto × 0,88 (Annahme). Türen und Wandstärken nicht festgelegt."], 22)
    save(s, "22_Bueros_Zugang_Alternativen")


# ---------- Blatt 23: Arbeitsgrundlage B3, Grundrisse und Schnitt ----------
def sheet23():
    v = VK; s = Sheet(); V2.MET["B3"] = dict(MK); m = MK
    drawing_title(s, "Arbeitsgrundlage B3 – Grundrisse und Schnitt (Variante B, nicht festgelegt)", "M 1:250 · Mittelgang bei y 9,50 m für ausgeglichene Wohnungstiefen · HYPOTHETISCH: Grundstücksform, Baufenster und Rechtsfragen nicht belegt")
    ox1, ox2 = 22.0, 180.0
    s.text(ox1, 41, "Erdgeschoss 32 × 18 m (Alternative K, Büro-Foyer im Kern)", 3.6, weight=600); s.text(ox2, 41, "1. Obergeschoss (nur Wohnungen)", 3.6, weight=600)
    V2.draw_plan(s, v, "GF", ox1, 60.0); V2.draw_plan(s, v, "L1", ox2, 54.0)
    X = lambda x: ox1 + x * V2.M; Y = lambda y: 60.0 + y * V2.M
    for r in v["rooms"]:
        if r["level"] == "GF" and r["id"] in ("BUERO-WC-GF", "BUERO-FOYER2-GF"):
            x0, y0, x1, y1 = r["rect"]; V2.fit(s, X((x0 + x1) / 2), Y((y0 + y1) / 2), (x1 - x0) * V2.M, (y1 - y0) * V2.M, "WC" if "WC" in r["id"] else "Foyer", None, 2.6, False)
    s.text(ox2, 168, "3. Geschoss, Staffel (nur Wohnungen)", 3.6, weight=600); s.text(ox1, 190, "Schnitt bei x = 17,00 m", 3.6, weight=600)
    V2.draw_plan(s, v, "L2", ox2, 176.0); V2.draw_section(s, v, 36.0, 246.0)
    kenn = [("Außenmaß EG / 1. OG / 3. Geschoss", "32×18 / 32×21,0 / 30,4×17,9 m"), ("Anbau 1. OG / Überstand Staffel", "3,00 / 1,50 m"), ("Gastronomie, Innenplätze realistisch", f"440 m², {m['seats']}"), ("Büros, netto", f"2 × 28 = {m['buero_netto']:.0f} m²".replace(".", ",")),
            ("Wohnungen, Wohnfläche netto", f"{m['we']}, ca. {m['wfl']:.0f} m²"), ("Dachterrasse hinten", "2,3 m tief")]
    legend = [(sw(FILL["apartment"]), "Wohnung, Nummer nach Geschoss, Wohnfläche netto"), (sw(FILL["office"]), "Büro"), (sw(FILL["dining"]), "Gastraum und Bar"), (sw(FILL["kitchen"]), "Küche, Lager, WC, Personal, Anlieferung"), (sw(FILL["foyer"]), "Büro-Foyer"),
              (sw(FILL["core"]), "Kern (AZ Aufzug, T Technik)"), (lambda s, x, y: (V2.hatch(s), s.rect(x, y, 8, 4, "url(#hatch)", GREY, 0.2, "1.5 1")), "Auskragung 1. OG über Stellplätzen"), (lambda s, x, y: (V2.hatch(s), s.rect(x, y, 8, 4, "url(#terr)", "#B49A72", 0.3)), "Dachterrasse (Vorschlag)"),
              (sw("#F3D98B", INK, 4, 3), "Küchenabluft-Schacht")]
    offen = [("C-30", "Baufenster, GRZ, Abstände, Zählung der Auskragung unbekannt; Projektion 660 m² gegen theoretisch 576 m²."), ("C-28", "Stellplatzbedarf und nachweisbare Stellplätze getrennt: siehe Blatt 26."), ("C-38", "Abstell- und Fahrradraum Wohnen im EG entfällt (Alternative K)."), ("C-22", "Küchenabluft-Schacht läuft durch Wohnungen.")]
    hint = ["Variante B ist nur Arbeitsgrundlage, nicht festgelegt. Gegenüber Version 2 liegt der Mittelgang bei y 9,50 m; die Wohnfläche ist unverändert.", "Flächen netto = Brutto × 0,88 (Annahme). Fenster, Türen und Wandstärken nicht festgelegt."]
    frame(s, "Arbeitsgrundlage B3 – Grundrisse und Schnitt", "Maßstab 1:250 (A3)", kenn, legend, offen, hint, 23)
    save(s, "23_B3_Grundrisse_Schnitt")

# ---------- Blatt 24: Wohnungsstudien ----------
W_T = {
 "T1": dict(title="Wohnung 1.01–1.05 (1. OG vorn)", gross=(5.6, 9.5), face="top", rooms=[("Wohnen / Schlafen", 0, 0, 5.35, 4.6, True), ("Küche (offen)", 0, 4.6, 2.7, 6.8, False), ("Abstell", 2.7, 4.6, 5.35, 6.0, False), ("Bad", 2.7, 6.0, 5.35, 8.85, False), ("Flur", 0, 6.8, 2.7, 8.85, False)], door=(0.8, 1.7), ext="Balkon 2,70 × 1,50 m zum Platz", net=46.8),
 "T2": dict(title="Wohnung 1.06–1.09 (1. OG hinten)", gross=(7.0, 9.5), face="top", rooms=[("Wohnen / Essen", 0, 0, 3.9, 4.6, True), ("Schlafen", 3.9, 0, 6.75, 4.6, True), ("Küche (offen)", 0, 4.6, 3.9, 7.2, False), ("Bad", 3.9, 4.6, 6.75, 7.0, False), ("Flur", 0, 7.2, 3.9, 8.85, False), ("Abstell", 3.9, 7.0, 6.75, 8.85, False)], door=(1.2, 2.1), ext="kein Außenraum", net=58.5),
 "T3": dict(title="Wohnung 3.01–3.04 (Staffel vorn)", gross=(6.75, 8.7), face="top", rooms=[("Wohnen / Essen", 0, 0, 3.6, 4.4, True), ("Schlafen", 3.6, 0, 6.5, 4.4, True), ("Küche (offen)", 0, 4.4, 3.6, 6.4, False), ("Bad", 3.6, 4.4, 6.5, 6.6, False), ("Flur", 0, 6.4, 3.6, 8.05, False), ("Abstell", 3.6, 6.6, 6.5, 8.05, False)], door=(1.0, 1.9), ext="Umlauf 0,80 m, kein nutzbarer Außenraum", net=51.7),
 "T4": dict(title="Wohnung 3.05–3.07 (Staffel hinten)", gross=(9.0, 7.2), face="top", rooms=[("Wohnen / Essen", 0, 0, 4.8, 3.9, True), ("Schlafen", 4.8, 0, 8.75, 3.9, True), ("Küche (offen)", 0, 3.9, 3.4, 6.55, False), ("Bad", 3.4, 3.9, 5.8, 6.55, False), ("Flur", 5.8, 3.9, 8.75, 6.55, False)], door=(6.6, 7.5), ext="Dachterrasse 9,0 × 2,3 m = 20,7 m²", net=57.0, terrace=2.3)}
def sheet24():
    s = Sheet(); M = 10.0; drawing_title(s, "Wohnungsstudien – Grundrisse, Belichtung, Belüftung, Erschließung", "Studien M 1:100 zur Prüfung der Nutzbarkeit (Variante B als Arbeitsgrundlage), keine Planung · Innenmaße mit Wandstärken ASSUMED")
    pos = {"T1": (22.0, 40.0), "T2": (166.0, 40.0), "T3": (22.0, 168.0), "T4": (166.0, 168.0)}
    COL = {True: "#F7F0E8", False: "#EDEAE4"}
    for k, t in W_T.items():
        cx, cy = pos[k]; wi = t["gross"][0] - 0.25; di = t["gross"][1] - 0.65; off = {"T1": 22, "T2": 22, "T3": 8, "T4": 8 + 23}[k]; X = lambda x: cx + x * M; Y = lambda y: cy + off + y * M
        s.text(cx, cy, t["title"], 3.2, weight=600)
        tot = 0.0
        for nm, x0, y0, x1, y1, win in t["rooms"]:
            s.rect(X(x0), Y(y0), (x1 - x0) * M, (y1 - y0) * M, COL[win], GREY, 0.25); a = (x1 - x0) * (y1 - y0); tot += a
            ccx, ccy = X((x0 + x1) / 2), Y((y0 + y1) / 2); w, h = (x1 - x0) * M, (y1 - y0) * M
            V2.fit(s, ccx, ccy, w, h, nm, f"{a:.1f} m²".replace(".", ","), 2.6, win)
        assert abs(tot - wi * di) < 0.15, (k, tot, wi * di)
        s.rect(X(0), Y(0), wi * M, di * M, "none", INK, 1.0)
        # Fenster (an der Fassade oben), Tür (unten)
        for nm, x0, y0, x1, y1, win in t["rooms"]:
            if win: s.rect(X(x0 + 0.5), Y(0) - 0.7, (x1 - x0 - 1.0) * M, 1.4, "#FFFFFF", INK, 0.4)
        a, b = t["door"]; s.rect(X(a), Y(di) - 0.7, (b - a) * M, 1.4, "#FFFFFF", INK, 0.4)
        if k == "T1": s.rect(X(1.325), Y(-1.5), 2.7 * M, 1.5 * M, "#F1F2F3", INK, 0.45); s.text(X(2.675), Y(-0.75) + 0.9, "Balkon", 2.6, "middle", 400, GREY)
        if k == "T4": V2.hatch(s); s.rect(X(0), Y(-2.3), 8.75 * M, 2.3 * M, "url(#terr)", "#B49A72", 0.3); s.text(X(4.4), Y(-1.15) + 0.9, "Dachterrasse 2,3 m", 2.6, "middle", 600, "#6B5A3A", halo=True)
        s.text(X(0), Y(di) + 4.2, "Eingang vom Mittelgang", 2.6, "start", 400, GREY)
        # Prüfzeilen rechts
        tx = cx + wi * M + 6; ty = Y(0) + 2.0; tw_ = min(56.0, 308 - tx)
        win_rooms = [r for r in t["rooms"] if r[5]]; depth = max(r[4] - r[2 - 1 if False else 1] for r in win_rooms)
        wide = sum(r[3] - r[1] for r in win_rooms)
        glaz = sum(min(r[3] - r[1] - 0.9, 3.2) * 2.2 for r in win_rooms); wohn = sum((r[3] - r[1]) * (r[4] - r[2]) for r in win_rooms)
        inside = [r[0] for r in t["rooms"] if not r[5]]
        bullets = [f"Wohnfläche netto ca. {t['net']:.1f} m² (Modell)".replace(".", ","), f"Wohnräume an der Fassade: {len(win_rooms)}, Raumtiefe {depth:.1f} m".replace(".", ","), f"Glasfläche (Annahme) ca. {glaz:.1f} m² = {glaz / wohn * 100:.0f} % der Wohnraumfläche".replace(".", ","),
                   "Innenliegend: " + ", ".join(i.replace(" (offen)", "") for i in inside) + " (mechanische Lüftung)", "Einseitig belichtet, keine Querlüftung", "Außenraum: " + t["ext"], "Stufenlos über Aufzug und Mittelgang"]
        for b in bullets: s.text(tx, ty, "•", 2.7); ty = s.wrap(tx + 3, ty, b, tw_ - 3, 2.7, 1.3) + 1.4
        assert ty < Y(di) + 20, (k, ty)
    scale_bar(s, 14, 280, 100, 2)
    legend = [(sw("#F7F0E8"), "Raum mit Fenster (Aufenthaltsraum)"), (sw("#EDEAE4"), "innenliegender Raum, mechanische Lüftung"), (sw("#FFFFFF", INK, 8, 2), "Fenster / Wohnungstür (Lage Annahme)"), (lambda s, x, y: (V2.hatch(s), s.rect(x, y, 8, 4, "url(#terr)", "#B49A72", 0.3)), "Dachterrasse")]
    offen = [("C-26", "Einseitig belichtete Wohnungen, Lage über der Gastro-Terrasse: Schall und Betriebszeiten nicht geprüft."), ("C-33", "Hintere Wohnungen im 1. OG ohne Außenraum (Loggien nur als Option, nicht geplant)."), ("C-39", "Dachterrasse: Brüstung, Brand- und Schallschutz, Dachaufbau über Wohnungen und Zugang offen; keine Rettungsfunktion nachgewiesen."),
             ("C-27", "Rollstuhlgerechte Wohnung: Kandidaten sind T2 und T4, nicht nachgewiesen.")]
    frame(s, "Wohnungsstudien", "Maßstab 1:100 (A3)", [("Typen", "4"), ("Wohnungen im Modell", "16")], legend, offen, ["Wohnungsgrößen sind Ergebnis der Gebäudetiefe (Mittelgang bei y 9,50 m: vorn 9,5 m, hinten 9,5 m), nicht der Flächenmaximierung. Küche und Bad liegen innen.", "Glasfläche = 2,2 m Höhe × (Raumbreite − 0,9 m, höchstens 3,2 m); Regeln zu Tageslicht und Lüftung sind nicht geprüft."], 24)
    save(s, "24_Wohnungsstudien")


# ---------- Blatt 25: Fassadenkonzept rundum (schematische Ansichten) ----------
CLK, LARCH, GLASS, CONC = V2.CLK, V2.LARCH, V2.GLASS, V2.CONC
def window(s, x, y, w, h, frame="#2B3036", glass="#C9DCE6", mull=True):
    s.rect(x, y, w, h, frame, None, 0); s.rect(x + 0.5, y + 0.5, w - 1.0, h - 1.0, glass, None, 0)
    if mull and w > 12: s.line(x + w / 2, y + 0.5, x + w / 2, y + h - 0.5, 0.3, frame)
def elev3(s, v, view, ox, gy, title, dr):
    M = V2.M; Z = lambda z: gy - z * M; Y1 = v["depth_L1"]; y2 = v["y2"]; boxes = v["boxes"]
    if view == "front": P = lambda x, y: ox + (32 - x) * M; key = lambda b: -b["y"][0]; span = lambda b: (32 - b["x"][1], 32 - b["x"][0]); shd = 1.0
    if view == "rear": P = lambda x, y: ox + x * M; key = lambda b: b["y"][1]; span = lambda b: (b["x"][0], b["x"][1]); shd = 1.0
    if view == "west": P = lambda x, y: ox + y * M; key = lambda b: -b["x"][0]; span = lambda b: (b["y"][0], b["y"][1]); shd = 0.93
    if view == "east": P = lambda x, y: ox + (dr - y) * M; key = lambda b: b["x"][1]; span = lambda b: (dr - b["y"][1], dr - b["y"][0]); shd = 0.93
    s.text(ox - 10, gy - 52, title, 3.4, weight=600)
    # Platzhalter für Koordinaten entlang der Blickachse
    px = lambda t: P(t, t)  # nicht verwendet
    def H(a): return ox + a * M          # horizontale Position aus Spannen-Koordinate
    for b in sorted(boxes, key=key):
        a0, a1 = span(b); fill = V2.shade(V2.MAT[b["m"]], shd); s.rect(H(a0), Z(b["z"][1]), (a1 - a0) * M, (b["z"][1] - b["z"][0]) * M, fill, INK, 0.4)
        if b["m"] == "klinker": s.rect(H(a0), Z(b["z"][1]), (a1 - a0) * M, 0.3 * M, CONC, INK, 0.2)           # Betonband (Geschossdecke) auf allen Seiten
        n = b["n"]
        if view == "front":
            hx = lambda x: ox + (32 - x) * M
            if n == "EG":
                s.rect(hx(32), Z(3.1), 28 * M, 3.1 * M, GLASS, INK, 0.4)
                for a, bb, hh in ((17, 19, 2.4), (29.5, 31, 2.4)): s.rect(hx(bb), Z(hh), (bb - a) * M, hh * M, "#FFFFFF", INK, 0.4)
                s.rect(hx(2.5), Z(2.4), 1.5 * M, 2.4 * M, GLASS, INK, 0.4)
            if n == "L1-Haupt":
                for i in range(5):
                    x0 = 4 + 5.6 * i; window(s, hx(x0 + 4.7), Z(6.1), 3.8 * M, 2.2 * M)
                    bx = v["balconies"][i]["rect"]; s.rect(hx(bx[2]), Z(3.5), 2.7 * M, 0.3 * M, CONC, INK, 0.4); s.rect(hx(bx[2]), Z(4.6), 2.7 * M, 1.1 * M, "#EAF1F3", INK, 0.35, op=0.9)
            if n == "L2-Haupt":
                for r in v["rooms"]:
                    if r["id"].startswith("WE-L2-V"): x0, x1 = r["rect"][0], r["rect"][2]; window(s, hx(x1 - 1.0), Z(9.0), (x1 - x0 - 2.0) * M, 2.1 * M, "#E6D9BE", "#C9DCE6")
        if view == "rear":
            hx = lambda x: ox + x * M
            if n == "EG":
                for a, bb in [(5.0, 6.5), (15.0, 16.5), (1.0, 2.5)]: window(s, hx(a), Z(2.4), (bb - a) * M, 2.4 * M, "#2B3036", "#C9DCE6", False)
            if n == "L1-Anbau":
                for r in v["rooms"]:
                    if r["id"].startswith("WE-L1-H"): x0 = r["rect"][0]; window(s, hx(x0 + 1.6), Z(6.1), 3.8 * M, 2.2 * M)
            if n == "L2-Anbau":
                for r in v["rooms"]:
                    if r["id"].startswith("WE-L2-H"): x0 = r["rect"][0]; window(s, hx(x0 + 1.6), Z(9.1), 5.8 * M, 2.5 * M, "#E6D9BE", "#C9DCE6")
            if n == "L1-Anbau": s.rect(hx(4), Z(7.6), 28 * M, 1.1 * M, "#EAF1F3", INK, 0.35, op=0.9)       # Brüstung Dachterrasse
        if view == "west" and n == "L1-Haupt":
            for z0, z1 in ((0.9, 3.0), (3.9, 6.1), (6.9, 9.1)): pass
        if view == "west" and n == "EG":
            for z0, z1 in ((0.9, 3.0),): window(s, H(6.5), Z(z1), 1.0 * M, (z1 - z0) * M, "#2B3036", "#C9DCE6", False)
        if view == "west" and n == "L1-Haupt": window(s, H(6.5), Z(6.1), 1.0 * M, 2.2 * M, "#2B3036", "#C9DCE6", False)
        if view == "west" and n == "L2-Haupt": window(s, H(6.5), Z(9.1), 1.0 * M, 2.2 * M, "#E6D9BE", "#C9DCE6", False)
        if view == "east":
            hy = lambda y: ox + (dr - y) * M
            if n == "EG": s.rect(hy(16.7), Z(2.4), 1.2 * M, 2.4 * M, "#2B3036", INK, 0.4)
            if n == "L1-Haupt": window(s, hy(11.5), Z(6.0), 2.0 * M, 1.6 * M, "#2B3036", "#C9DCE6", False)
            if n == "L2-Haupt": window(s, hy(11.5), Z(9.0), 2.0 * M, 1.6 * M, "#E6D9BE", "#C9DCE6", False)
    # Attika und Brüstungen an den Seiten
    for b in [b for b in boxes if b["n"].startswith("L2")]:
        a0, a1 = span(b); s.rect(H(a0), Z(9.9), (a1 - a0) * M, 0.3 * M, "#8E9399", None, 0); s.line(H(a0), Z(9.9), H(a1), Z(9.9), 0.4, INK)
    if view in ("west", "east"):
        a0, a1 = ((y2 if False else 17.2 + 0.0), Y1) if False else (18.0 + (y2 - 17.2 - 0.0) * 0 , Y1)
        yy0, yy1 = y2 if y2 > 18 else 18.0, Y1
        sa, sb = (yy0, yy1) if view == "west" else (dr - yy1, dr - yy0)
        s.rect(H(sa), Z(7.6), (sb - sa) * M, 1.1 * M, "#EAF1F3", INK, 0.35, op=0.9)
    if view == "east": s.rect(H(dr - 12.1) - 1.5, Z(10.8), 3.0, 0.9 * M, "#4A4F57", INK, 0.3)
    wmax = (32 if view in ("front", "rear") else dr)
    s.line(ox - 3, Z(0), ox + wmax * M + 3, Z(0), 0.9, INK)
    if view in ("front", "west"):
        for z, tx in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60")): s.line(ox - 9, Z(z), ox - 5, Z(z), 0.4, INK); s.text(ox - 10, Z(z) + 0.9, tx, 2.6, "end", 600)
    dim_h(s, ox, ox + wmax * M, gy + 9, de(wmax) if view in ("front", "rear") else f"{de(dr)} (1. OG)")

def sheet25():
    v = VK; s = Sheet(); dr = v["depth_L1"]
    drawing_title(s, "Fassadenkonzept rundum – schematische Ansichten, Arbeitsgrundlage B3", "Ansichten M 1:250 · Material und Farbe der Platzfassade unverändert · Fensterformate Vorschlag (ASSUMED), nicht freigegeben")
    elev3(s, v, "front", 34.0, 100.0, "Ansicht Platzseite (unverändert)", dr); elev3(s, v, "rear", 174.0, 100.0, "Ansicht Rückseite", dr)
    elev3(s, v, "west", 34.0, 215.0, "Seitenansicht Kernseite (x = 0)", dr); elev3(s, v, "east", 174.0, 215.0, "Seitenansicht Ostseite (x = 32)", dr)
    s.text(24.0, 130.0, "Höhen: ±0,00 Oberkante Erdgeschoss, +3,50 1. OG, +6,50 Traufe nach B-Plan und Staffel, +9,60 Staffeldecke, +9,90 Attika", 2.6, fill=GREY)
    s.text(24.0, 245.0, "Kernseite: Platzfassade links, Rückseite rechts. Ostseite: Platzfassade rechts, Rückseite links. Himmelsrichtung unbekannt (C-13).", 2.6, fill=GREY)
    legend = [(sw(CLK), "Klinker, dunkelrotbraun (hier aufgehellt)"), (sw(CONC), "Betonbänder und Balkonplatten"), (sw(LARCH), "Lärchenholz Staffelgeschoss"), (sw("#EAF1F3"), "Milchglas-Brüstung, 1,10 m"), (sw(GLASS), "Glas, Türen"),
              (lambda s, x, y: s.rect(x, y, 8, 4, "#2B3036", None, 0), "schwarzer Stahlrahmen (Wohngeschoss, EG)"), (lambda s, x, y: s.rect(x, y, 8, 4, "#E6D9BE", GREY, 0.2), "helles Holzfenster (Staffel)")]
    offen = [("C-13", "Himmelsrichtung und Platzseite unbekannt."), ("C-19", "Rückseite, Seiten und Dachterrasse sind nicht Teil des eingefrorenen Designs; hier ein Entwurfsvorschlag."), ("C-30", "Auskragung und Stufung: Baufenster, GRZ, Abstände und Höhen offen."), ("C-35", "Tragwerk der Auskragung (3,00 m, Sichtbeton-Untersicht)."),
             ("C-22", "Abluftstutzen über dem Dach (Position offen).")]
    hint = ["Gestaltungsregeln: Die Betonbänder der Platzfassade laufen um alle vier Seiten. Fensterachsen der Rückseite folgen den Wohnungsachsen, die Staffel hinten öffnet sich mit raumhohen Holzfenstern zur Dachterrasse.",
            "Die Stufung ist ausgebildet: Auskragung mit Betonband, Dachterrasse mit Milchglas-Brüstung, Staffel in Lärchenholz. Kernseite mit Treppenhausschlitz, Ostseite mit Fenster am Gangende."]
    frame(s, "Fassadenkonzept rundum", "Maßstab 1:250 (A3)", [("Tiefe EG / 1. OG / Staffel", "18,00 / 21,00 / 17,90 m"), ("Höhe Attika", "9,90 m"), ("Dachterrasse hinten", "2,3 m tief")], legend, offen, hint, 25)
    save(s, "25_Fassadenkonzept_Ansichten")


def table_block(s, x0, y, cw, rows, fs=2.9, head=True):
    xs = [x0]; [xs.append(xs[-1] + w) for w in cw[:-1]]
    def nl(t, w, b=False):
        n, line = 1, ""
        for wd in t.split():
            tt = (line + " " + wd).strip()
            if tw(tt, fs, b) <= w - 2 or not line: line = tt
            else: n += 1; line = wd
        return n
    for ri, row in enumerate(rows):
        hb = head and ri == 0
        n = max(nl(t, cw[j], hb or j == 0) for j, t in enumerate(row))
        for j, t in enumerate(row): s.wrap(xs[j] + 1.0, y, t, cw[j] - 2, fs, 1.3, 600 if (hb or j == 0) else 400)
        yl = y + (n - 1) * fs * 1.3 + 1.9; s.line(x0, yl, x0 + sum(cw), yl, 0.5 if hb else 0.15, INK if hb else LGREY); y = yl + 1.9 + fs * 0.85
    return y

# ---------- Blatt 26: Stellplätze und baurechtliche Prüfpunkte ----------
def sheet26():
    s = Sheet(); m = MK
    drawing_title(s, "Stellplätze und baurechtliche Prüfpunkte – Bedarf, Nachweis und offene Fragen getrennt", "Alle Werte hypothetisch oder Annahme; es wird keine Zulässigkeit behauptet. Die 32 × 30 m sind keine bestätigte Grundstücksgröße.")
    y = 38.0
    s.text(14, y, "1. Stellplätze: Bedarf und Nachweis getrennt", 3.6, weight=600); y += 6
    rows = [("", "Bedarf (grobe Annahme der Excel, nicht Satzung)", "Nachweislich möglich", "Hypothese H1 (32 × 30 m, nicht bestätigt)"),
            ("Wohnungen", f"{m['we']} × 1,5 = {m['we'] * 1.5:.0f}".replace(".", ","), "0 (kein Lageplan, keine Grundstücksmaße)", "–"),
            ("Gastronomie", f"Gastraum und Bar 280 m² / 10 = {280 / 10:.0f}".replace(".", ","), "0", "–"), ("Büros", f"{m['buero_netto']:.0f} m² / 30 = {m['buero_netto'] / 30:.1f}".replace(".", ","), "0", "–"),
            ("Summe", f"{m['stp_bedarf_neu']:.0f} (Excel-Stand mit 12 Wohnungen und 165 m² Büro: 61)", "0", "11 Stellplätze 2,50 × 5,00 m"),
            ("Fehlbetrag", "–", "gegenüber dem Bedarf: nicht bestimmbar", f"rechnerisch {m['stp_bedarf_neu'] - 11:.0f} Stellplätze".replace(".", ",")),
            ("Überdeckung", "–", "–", "3,0 von 5,0 m Tiefe durch die Auskragung; Durchfahrtshöhe 3,20 m (Annahme)")]
    y = table_block(s, 14, y, [28, 100, 78, 94], rows) + 3
    y = s.wrap(14, y, "Die Stellplatzsatzung der Stadt ist nicht bekannt; der Bedarf folgt den groben Annahmen der Excel. Mögliche Lösungen (Stellplätze außerhalb des Grundstücks, Ablöse, Gemeinschaftsanlage, Fahrradstellplätze) sind mit der Stadt zu klären und nicht Teil dieser Geometrie. Die Überdachung erzeugt keine zusätzlichen Stellplätze.", 300, 2.9, 1.35) + 5
    s.text(14, y, "2. Baurechtliche Prüfpunkte (alle offen)", 3.6, weight=600); y += 6
    rows2 = [("Thema", "Wert im Modell (hypothetisch)", "Status", "Nötige Unterlage"),
             ("GRZ", "Grundfläche EG 576 m² = 0,60 × 960 m²; Projektion 1. OG 660 m² = 0,69", "OFFEN: Zählung von Auskragungen, Terrassen, Stellplätzen unbekannt; Variante nicht nachweisbar zulässig", "B-Plan Nr. 123, Auslegung der GRZ"),
             ("Baufenster", "Gebäude 32 × 18 m; Sichtschätzung des Baufensters nur 400–460 m²", "OFFEN (C-01): Nachweis fehlt", "Baufenster-Koordinaten, Lageplan"),
             ("Auskragung", "3,00 m hinten über Stellplätzen, Staffel 1,50 m kürzer", "OFFEN: Baugrenze und Überbauung der Stellplatzfläche", "B-Plan, Stadt"),
             ("Abstände", "Rückbereich 12 m (aus 32 × 30 m angenommen)", "OFFEN: Grenzabstand und Abstandsflächen unbekannt", "Lageplan mit Grenzen, NBauO"),
             ("Höhen", "Traufe 6,50 m, Staffeldecke 9,60 m, Attika 9,90 m, Maximum 12,00 m", "OFFEN (C-03): Messregel unbestätigt", "B-Plan, Stadt"),
             ("Geschosse", "EG, 1. OG, Staffel (Staffel 87 % des Geschosses darunter)", "OFFEN (C-02): Vollgeschoss und Zahl zulässig?", "B-Plan, Stadt"),
             ("Brandschutz und Rettungswege", "Gaststätte 120 + 44 Plätze, Büros, 16 Wohnungen, ein Treppenraum, Dachterrasse", "OFFEN (C-15, C-20, C-36, C-39)", "Brandschutzkonzept"),
             ("Terrasse und Vordach am Platz", "24 × 3,6 m, Vordach, Balkone 1,50 m über der Fassade", "OFFEN: Eigentum und Sondernutzung des Platzes", "Lageplan, Stadt")]
    y = table_block(s, 14, y, [38, 100, 100, 62], rows2, 2.8)
    assert y < 282, y
    legend = None
    frame(s, "Stellplätze und Prüfpunkte", "Tabelle", [("Bedarf (Annahme)", f"ca. {m['stp_bedarf_neu']:.0f}"), ("nachweislich möglich", "0"), ("Hypothese H1", "11")], legend, [("C-28", "Stellplätze: Bedarf und Nachweis getrennt, Fehlbetrag offen."), ("C-29", "Grundstückszuschnitt, Zufahrt, Anlieferung unbekannt."), ("C-30", "Baurechtliche Zulässigkeit nicht nachgewiesen.")], ["Keine Variante gilt als zulässig, solange die Nachweise fehlen."], 26)
    save(s, "26_Stellplaetze_und_Pruefpunkte")

# ---------- Blatt 27: Vergleich ----------
def sheet27():
    s = Sheet(); m = MK; a, b, c = M2["A"], M2["B"], M2["C"]
    drawing_title(s, "Vergleichstabelle – Arbeitsgrundlage B3 gegenüber A, B und C (Version 2)", "Spalte B3 ist die Arbeitsgrundlage dieser Runde (Variante B, nicht festgelegt). Alle Werte hypothetisch.")
    de0 = lambda x: f"{x:,.0f}".replace(",", ".")
    rows = [("Kriterium", "A (v2)", "B (v2)", "B3 Arbeitsgrundlage", "C (v2)"),
            ("Anbau 1. OG / Überstand Staffel", "1,5 / 0 m", "3,0 / 1,5 m", "3,0 / 1,5 m", "4,5 / 2,0 m"),
            ("Mittelgang", "y 8,0", "y 8,0", "y 9,5 (Tiefen 9,5 / 9,5 m)", "y 9,0"),
            ("Projizierte Fläche, GRZ-Zahl", f"{de0(a['projektion'])} m², {de(a['grz'])}", f"{de0(b['projektion'])} m², {de(b['grz'])}", f"{de0(m['projektion'])} m², {de(m['grz'])}", f"{de0(c['projektion'])} m², {de(c['grz'])}"),
            ("Gastronomie brutto", "440 m²", "440 m²", "440 m²", "440 m²"),
            ("Innenplätze", "138 (Flächenregel)", "138 (Flächenregel)", f"{m['seats']} realistisch; {m['seats_komf']} komfortabel; {m['seats_dicht']} dicht", "138 (Flächenregel)"),
            ("Terrassenplätze", "60 (Annahme)", "60 (Annahme)", f"{m['terrasse_plaetze']} (komfortabel {m['terr_komf']}, dicht {m['terr_dicht']})", "60 (Annahme)"),
            ("Büros netto, Zugang und WC", "56 m², WC fehlt", "56 m², WC fehlt", "56 m² (Alt. K), WC im Foyer, Zugang rückseitig", "56 m², WC fehlt"),
            ("Wohnungen, Wohnfläche netto", f"{a['we']}, {de0(a['wfl'])} m²", f"{b['we']}, {de0(b['wfl'])} m²", f"{m['we']}, {de0(m['wfl'])} m²", f"{c['we']}, {de0(c['wfl'])} m²"),
            ("Wohnungsgrößen netto", "39, 43, 57, 58 m²", "39, 43, 68, 69 m²", "47, 52, 57, 59 m²", "44, 49, 65, 71 m²"),
            ("Tiefe/Breite höchstens", f"{a['tiefe_breite_max']}".replace(".", ","), f"{b['tiefe_breite_max']}".replace(".", ","), f"{m['tiefe_breite_max']}".replace(".", ","), f"{c['tiefe_breite_max']}".replace(".", ",")),
            ("Dachterrasse", "2,3 m", "2,3 m", "2,3 m, 3 Terrassen à 20,7 m²", "3,3 m"),
            ("Stellplätze: Bedarf / nachweislich / Hypothese", "54 / 0 / 11", "54 / 0 / 11", f"{m['stp_bedarf_neu']:.0f} / 0 / 11".replace(".", ","), "54 / 0 / 11"),
            ("Überdeckt, Stützen", "1,5 m, keine", "3,0 m, keine", "3,0 m, keine", "4,5 m, 5 Stützen"),
            ("Nachweisstatus", "nicht nachweisbar", "nicht nachweisbar", "nicht nachweisbar", "nicht nachweisbar")]
    y = table_block(s, 14, 40.0, [62, 50, 50, 88, 50], rows, 3.0)
    assert y < 278, y
    kenn = [("Zusätzliche Wohnfläche B3 gegen A", f"+{m['wfl'] - a['wfl']:.0f} m²"), ("Innenplätze B3 gegen Flächenregel", f"{m['seats']} statt {m['seats_regel']}")]
    frame(s, "Vergleichstabelle", "Tabelle", kenn, None, [("C-30", "Zulässigkeit nicht nachgewiesen."), ("C-28", "Stellplatznachweis offen."), ("C-37", "Büros und Gastronomie kleiner als in der Excel: Wirtschaftlichkeit nicht neu gerechnet."), ("C-29", "Grundstücksgröße 32 × 30 m ist Annahme.")],
          ["A, B, C (v2) unverändert aus der letzten Runde; die Innenplätze dort sind eine Flächenregel (2,1 m² je Platz), nur B3 wurde möbliert.", "Der Bedarf von 54 Stellplätzen folgt den groben Excel-Annahmen mit den neuen Flächen (Excel-Stand 61)."], 27)
    save(s, "27_Vergleich_B3")

if __name__ == "__main__":
    for a in sys.argv[1:]: globals()["sheet" + a]()
