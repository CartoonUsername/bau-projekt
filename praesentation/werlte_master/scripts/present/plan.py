"""Grundrissblätter (EG, 1. OG, Staffelgeschoss) im Präsentationsstil. Geometrie ausschließlich aus geometry/building_design.json."""
import sys, os
from lib import *
M = 8.0   # mm je m  -> Maßstab 1:125
NAMES = {"LOBBY-GF": "Eingangshalle", "STAIR": "Treppenraum", "LANDING": "Aufzugsvorraum", "LIFT": "Aufzug", "TECH": "Technik", "ABSTELL": "Abstellräume", "RESERVE": "Reserve",
         "DINING-GF": "Gastraum", "LOUNGE-GF": "Lounge", "BAR-GF": "Bar", "SEPAREE-GF": "Séparée", "SERVICE-GF": "Service / Garderobe", "WC-GF": "WC", "STORE-GF": "Lager / Kühlung", "KITCHEN-GF": "Küche"}
NET = D["net_factor"]
def name(i):
    if i in NAMES: return NAMES[i]
    for k in ("STAIR", "LANDING", "LIFT", "TECH", "ABSTELL", "RESERVE"):
        if i.startswith(k): return NAMES[k]
    if i.startswith("OFFICE-"): return "Büro " + i.split("-")[1]
    if i.startswith("CORR"): return "Mittelgang"
    return i
def lab(r):
    """(Zeile 1, Zeile 2) – Flächen netto = brutto × Faktor, nur für Wohnungen/Büros"""
    t, i, a = r["type"], r["id"], r.get("area_gross")
    if t == "apartment": return i, f"ca. {de(a * NET, 1)} m²"
    if t == "office": return name(i), f"ca. {de(a * NET, 1)} m²"
    if t == "corridor": return "Mittelgang", "2,00 m breit"
    if i == "DINING-GF": return "Gastraum", f"ca. {de(a, 0)} m² einschl. Lounge und Bar"
    if i == "LOUNGE-GF": return "Lounge", f"{r['seats']} Plätze"
    if i == "BAR-GF": return "Bar", f"{r['seats']} Hocker"
    if i == "SEPAREE-GF": return "Séparée", f"{r['seats']} Plätze · {de(a, 0)} m²"
    if i in ("SERVICE-GF", "WC-GF", "STORE-GF", "KITCHEN-GF"): return name(i), f"{de(a, 0)} m²"
    return name(i), None
def room_label(s, r, X, Y, rect, fs=2.8, dark=False):
    x0, y0, x1, y1 = rect; l1, l2 = lab(r) if "type" in r else (name(r["id"]), ("Zweck offen" if r["id"].startswith(("RESERVE", "ABSTELL")) else None))
    w, h = (x1 - x0) * M, (y1 - y0) * M
    cx, cy = X((x0 + x1) / 2), Y((y0 + y1) / 2)
    need = max(tw(l1, fs, True), tw(l2, fs - 0.2) if l2 else 0)
    if need + 2 > w and h > w:      # schmaler hoher Raum: Text drehen
        s.text(cx + 1.0, cy, l1, fs, "middle", 600, rot=-90)
        if l2: s.text(cx - 2.0, cy, l2, fs - 0.2, "middle", 400, GREY, rot=-90)
        return
    assert need + 1.5 <= w, f"Beschriftung '{l1}' passt nicht in den Raum ({need:.1f} > {w:.1f} mm)"
    if l2: s.text(cx, cy - 0.6, l1, fs, "middle", 600); s.text(cx, cy + 3.0, l2, fs - 0.2, "middle", 400, GREY)
    else: s.text(cx, cy + 1.0, l1, fs, "middle", 600)

def plan_sheet(level, title, sub, fname, sheet_no, rooms, extra_kenn, offen, hinweise, flags=(), env=None, terrace=False, balc=True, ox=52.0, oy=84.0, legend_extra=None, unit_chain=None):
    s = Sheet()
    X = lambda x: ox + x * M; Y = lambda y: oy + y * M
    drawing_title(s, title, sub)
    ex0, ey0, ex1, ey1 = env or (0, 0, 32, 18)
    # Geschoss darunter (nur Staffel): gestrichelte Außenkontur
    if env: s.rect(X(0), Y(0), 32 * M, 18 * M, "none", LGREY, 0.3, "2 1.2")
    # Raumflächen
    for r in rooms:
        x0, y0, x1, y1 = r["rect"]
        s.rect(X(x0), Y(y0), (x1 - x0) * M, (y1 - y0) * M, FILL.get(r["type"], "#EEE"), PALE if False else "#FFFFFF", 0.0)
    kx0, ky0, kx1, ky1 = (0, 0, 4, 18) if level in ("GF", "L1") else (0.8, 0.8, 4.0, 17.2)
    s.rect(X(kx0), Y(ky0), (kx1 - kx0) * M, (ky1 - ky0) * M, FILL["core"], None, 0)
    # Innenlinien
    for r in [r for r in rooms if r["type"] != "core"] + D["core"].get(level, []):
        x0, y0, x1, y1 = r["rect"]
        s.rect(X(x0), Y(y0), (x1 - x0) * M, (y1 - y0) * M, "none", GREY, 0.25)
    # Außenwand
    s.rect(X(ex0), Y(ey0), (ex1 - ex0) * M, (ey1 - ey0) * M, "none", INK, 0.8)
    # Aufzugsschacht und Schächte
    for sh in D["shafts"]:
        if level in sh["levels"]:
            x0, y0, x1, y1 = sh["rect"]; s.rect(X(x0), Y(y0), (x1 - x0) * M, (y1 - y0) * M, "#F3D98B", INK, 0.35)
            s.text(X((x0 + x1) / 2), Y((y0 + y1) / 2) + 1.0, "KS", 2.6, "middle", 600)
    for c in D["core"].get(level, []):
        if c["id"].startswith("LIFT"):
            x0, y0, x1, y1 = c["rect"]; s.line(X(x0), Y(y0), X(x1), Y(y1), 0.2, GREY); s.line(X(x0), Y(y1), X(x1), Y(y0), 0.2, GREY)
    # Beschriftungen
    for r in rooms:
        if r["type"] == "core": continue
        room_label(s, r, X, Y, r["rect"])
    for c in D["core"].get(level, []):
        if c["id"].startswith("LIFT"):
            x0, y0, x1, y1 = c["rect"]; s.rect(X(x0) + 1, Y((y0 + y1) / 2) - 3.6, (x1 - x0) * M - 2, 5.6, "#FFFFFF", None, 0, op=0.85)
        room_label(s, {"id": c["id"]}, X, Y, c["rect"], 2.7)
    # Stützen
    if level in ("GF", "L1"):
        for cx, cy in D["columns_gf"]: s.rect(X(cx) - 1.2, Y(cy) - 1.2, 2.4, 2.4, INK, INK, 0.1)
    # Balkone
    if balc and level == "L1":
        for b in D["balconies"]:
            x0, y0, x1, y1 = b["rect"]
            s.rect(X(x0), Y(y0), (x1 - x0) * M, (y1 - y0) * M, "#F1F2F3", INK, 0.45)
            s.rect(X(x0) + 0.5, Y(y0) + 0.5, (x1 - x0) * M - 1.0, (y1 - y0) * M - 1.0, "none", GREY, 0.2)
            s.text(X((x0 + x1) / 2), Y((y0 + y1) / 2) + 1.0, "Balkon", 2.6, "middle", 400, GREY)
    # Terrasse und Vordach, Eingänge (EG)
    if terrace:
        t = D["terrace"]["rect"]
        s.rect(X(t[0]), Y(t[1]), (t[2] - t[0]) * M, (t[3] - t[1]) * M, "#F3EBDD", GREY, 0.3, "1.6 1.0")
        s.text(X((t[0] + t[2]) / 2), Y(t[1]) + 11.5, "Terrasse und Stahlvordach · 60 Plätze · Lage auf dem Grundstück ungeprüft", 2.7, "middle", 400, GREY)
        for o in D["openings"]:
            a, b = o["x"]
            if o["id"].startswith("RESTAURANT"): g = (a, b)
        s.line(X(4), Y(0), X(32), Y(0), 1.6, "#7FA6BA")
        s.line(X(4), Y(0), X(32), Y(0), 0.25, INK)
        for o in D["openings"]:
            if o["type"].startswith("door"):
                a, b = o["x"]; s.line(X(a), Y(0), X(b), Y(0), 2.2, "#FFFFFF"); s.line(X(a), Y(0) - 1.1, X(a), Y(0) + 1.1, 0.5); s.line(X(b), Y(0) - 1.1, X(b), Y(0) + 1.1, 0.5)
        s.text(X(18), Y(0) + 5.2, "Zugang Restaurant", 2.5, "middle", 400, GREY) if False else None
    # Raster und Maße: oben, bei Terrasse (EG) unten
    gx, gy = D["grid"]["x"], D["grid"]["y"]
    bot = terrace
    for i, x in enumerate(gx):
        if bot:
            s.line(X(x), Y(ey1), X(x), Y(18) + 21, 0.18, "#B9615A", "5 1.2 0.8 1.2"); bubble(s, X(x), Y(18) + 24, str(i + 1))
        else:
            s.line(X(x), oy - 31, X(x), Y(ey0), 0.18, "#B9615A", "5 1.2 0.8 1.2")
            s.line(X(x), Y(ey1), X(x), Y(18) + 7, 0.18, "#B9615A", "5 1.2 0.8 1.2"); bubble(s, X(x), oy - 34, str(i + 1))
    for j, y in enumerate(gy):
        s.line(ox - 30, Y(y), X(ex0), Y(y), 0.18, "#B9615A", "5 1.2 0.8 1.2")
        s.line(X(ex1), Y(y), X(32) + 7, Y(y), 0.18, "#B9615A", "5 1.2 0.8 1.2")
        bubble(s, ox - 33, Y(y), "ABC"[j])
    yo, yt = (Y(18) + 10, Y(18) + 17) if bot else (oy - 20, oy - 27)
    dim_h(s, X(0), X(4), yo, "4,00")
    for a, b in zip(gx[:-1], gx[1:]): dim_h(s, X(a), X(b), yo, de(b - a))
    dim_h(s, X(0), X(32), yt, "32,00")
    if unit_chain:
        for a, b in zip(unit_chain[:-1], unit_chain[1:]): dim_h(s, X(a), X(b), oy - 11, de(b - a))
        s.text(X(0) - 2, oy - 10.2, "Wohnungsbreiten", 2.5, "end", 400, GREY)
    xo = ox - 12
    dim_v(s, xo, Y(0), Y(8), "8,00"); dim_v(s, xo, Y(8), Y(10), "2,00"); dim_v(s, xo, Y(10), Y(18), "8,00")
    dim_v(s, ox - 20, Y(0), Y(18), "18,00")
    for fx, fy, cid in flags: flag(s, X(fx), Y(fy), cid)
    scale_bar(s, 14, 268, 125)
    # Informationsbereich
    legend = [
        (lambda s, x, y: s.rect(x, y, 8, 4, FILL["apartment"], GREY, 0.25), "Wohnung (Wohnfläche netto)"),
        (lambda s, x, y: s.rect(x, y, 8, 4, FILL["office"], GREY, 0.25), "Büro (Nutzfläche netto)"),
        (lambda s, x, y: s.rect(x, y, 8, 4, FILL["core"], GREY, 0.25), "Erschließung: Treppenraum, Aufzug, Technik"),
        (lambda s, x, y: s.rect(x, y, 8, 4, FILL["corridor"], GREY, 0.25), "Mittelgang"),
        (lambda s, x, y: s.rect(x + 2.5, y + 0.5, 3, 3, INK, INK, 0.1), "Stütze (Annahme, Raster R2)"),
        (lambda s, x, y: s.rect(x + 2, y + 0.5, 4, 3, "#F3D98B", INK, 0.3), "KS: Küchenabluft-Schacht"),
        (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 0.18, "#B9615A", "5 1.2 0.8 1.2"), "Rasterachse (vorläufig)"),
    ]
    if legend_extra: legend = legend_extra
    if level == "L1": legend.insert(4, (lambda s, x, y: (s.rect(x + 1, y, 6, 4, "#F1F2F3", INK, 0.45)), "Balkon (2,70 × 1,50 m)"))
    kenn = [("Grundfläche Gebäude", "32,00 × 18,00 m = 576 m²")] + extra_kenn
    frame(s, title, "Maßstab 1:125 (A3)", kenn, legend, offen, hinweise, sheet_no)
    err = s.check()
    assert not err, "\n".join(err)
    open(os.path.join(ROOT, "praesentation_zeichnungen", fname + ".svg"), "w", encoding="utf-8").write(s.svg())
    print("geschrieben", fname)

def apts(rs): return [r for r in rs if r["type"] == "apartment"]
if __name__ == "__main__":
    which = sys.argv[1:] or ["og1"]
    HINT_COMMON = ["Flächen netto = Brutto × 0,88 (Annahme).", "Fenster, Türen und Wandstärken sind noch nicht festgelegt und daher nicht dargestellt.", "Himmelsrichtung unbekannt (C-13). Förderthemen sind nicht Gegenstand dieses Blatts."]
    if "og1" in which:
        og = D["upper_options"]["OG-2"]["rooms"]
        a = apts(og); fl = sum(r["area_gross"] * NET for r in a); bu = sum(r["area_gross"] * NET for r in og if r["type"] == "office")
        plan_sheet("L1", "1. Obergeschoss – Arbeitsgrundlage OG-2", "Grundriss M 1:125 · OG-2 ist vorläufige Arbeitsgrundlage, keine endgültige Entscheidung", "01_Grundriss_1OG_OG2", 1, og,
                   [("Wohnungen im 1. OG", f"{len(a)}"), ("Wohnfläche netto", f"ca. {de(fl, 0)} m²"), ("Bürofläche netto", f"ca. {de(bu, 0)} m²")],
                   [("C-01", "Baufenster: Nachweis der 576 m² Grundfläche fehlt."), ("C-15", "Rettungswege: Mittelgang ca. 28 m lang, zweiter Rettungsweg offen."), ("C-16", "Stützen oder Träger in der Platzfassade nicht nachgewiesen."),
                    ("C-19", "Rückseitiger Balkon: Grenzabstand unbekannt."), ("C-22", "Küchenabluft-Schacht läuft durch Wohnung WE-L1-N1."), ("C-25", "Aufzug: Überfahrt über die Attika offen.")],
                   ["OG-2: fünf Wohnungen vorn mit je einem Balkon zum Platz (Platzfassade oben), eine Wohnung und zwei Büros hinten."] + HINT_COMMON,
                   flags=[(24.0, 9.3, "C-16"), (29.2, 9.3, "C-15"), (27.9, 16.6, "C-22"), (27.9, 20.4, "C-19")])

    if "og1" not in which or True:
        pass
    if "staffel" in which:
        st = D["staffel"]["rooms"]; a = apts(st)
        front = sorted({r["rect"][0] for r in a if r["rect"][1] == 0.8} | {r["rect"][2] for r in a if r["rect"][1] == 0.8})
        plan_sheet("L2", "Staffelgeschoss – Arbeitsstand S-1", "Grundriss M 1:125 · Staffel 0,80 m zurückgesetzt, Geschoss darunter gestrichelt", "02_Grundriss_Staffelgeschoss", 2, st,
                   [("Wohnungen im Staffelgeschoss", f"{len(a)}"), ("Wohnfläche netto", f"ca. {de(sum(r['area_gross'] * NET for r in a), 0)} m²"), ("Staffel gegen Geschoss darunter", "87 %")],
                   [("C-02", "Staffel gilt voraussichtlich als Vollgeschoss (87 % der Fläche darunter)."), ("C-21", "Achsen: Entwurf 4, 1. OG 5, Renderings 7 – offen."), ("C-15", "Rettungswege und Anleiterung: offen."),
                    ("C-22", "Küchenabluft-Schacht läuft durch Wohnung WE-L2-N3."), ("C-25", "Aufzug: Überfahrt über die Attika offen.")],
                   ["Rückversatz 0,80 m umlaufend (Umlauf). Die Wohnungstrennwände vorn liegen nicht auf dem Raster R2."] + HINT_COMMON,
                   flags=[(14.0, 9.3, "C-21"), (27.9, 16.6, "C-22")], env=(0.8, 0.8, 31.2, 17.2), balc=False, unit_chain=front)
    if "eg" in which:
        gf = [r for r in D["rooms"] if r["level"] == "GF"]
        leg = [(lambda s, x, y: s.rect(x, y, 8, 4, FILL["dining"], GREY, 0.25), "Gastraum"), (lambda s, x, y: s.rect(x, y, 8, 4, FILL["lounge"], GREY, 0.25), "Lounge, Bar, Séparée"),
               (lambda s, x, y: s.rect(x, y, 8, 4, FILL["kitchen"], GREY, 0.25), "Küche, Lager, WC, Service"), (lambda s, x, y: s.rect(x, y, 8, 4, FILL["core"], GREY, 0.25), "Erschließung Wohnen: Halle, Treppenraum, Aufzug, Technik"),
               (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 1.6, "#7FA6BA"), "Glasfront zum Platz (Annahme)"), (lambda s, x, y: s.rect(x, y, 8, 4, "#F3EBDD", GREY, 0.3, "1.6 1.0"), "Terrasse und Vordach"),
               (lambda s, x, y: s.rect(x + 2.5, y + 0.5, 3, 3, INK, INK, 0.1), "Stütze (Annahme, Raster R2)"), (lambda s, x, y: s.rect(x + 2, y + 0.5, 4, 3, "#F3D98B", INK, 0.3), "KS: Küchenabluft-Schacht"),
               (lambda s, x, y: s.line(x, y + 2, x + 8, y + 2, 0.18, "#B9615A", "5 1.2 0.8 1.2"), "Rasterachse (vorläufig)")]
        plan_sheet("GF", "Erdgeschoss – Restaurant, Bar und Wohnungseingang", "Grundriss M 1:125 · Arbeitsstand der Variante A", "03_Grundriss_Erdgeschoss", 3, gf,
                   [("Gastrofläche ohne Lounge und Bar", "504 m² (Ziel 510 m²)"), ("Innenplätze", "190"), ("Terrassenplätze", "60")],
                   [("C-01", "Baufenster: Nachweis der 576 m² Grundfläche fehlt."), ("C-16", "Platzfassade: 28 m Glasfront ohne nachgewiesene Stützen oder Träger."), ("C-18", "Stahlvordach liegt unter den Balkonplatten des 1. OG."),
                    ("C-20", "Gaststätte mit 190 + 60 Plätzen: Einstufung als Sonderbau offen."), ("C-22", "Küchenabluft-Schacht durchläuft darüberliegende Wohnungen."), ("C-13", "Platzseite und Himmelsrichtung unbekannt.")],
                   ["Wohnungseingang am Westende (Eingangshalle). Zugang Restaurant über die Doppeltür in Feldmitte (x 17–19 m).", "Terrasse 24,0 × 3,6 m: Lage auf dem Grundstück ungeprüft."] + HINT_COMMON,
                   flags=[(27.4, 15.0, "C-22")] if False else [], terrace=True, balc=False, oy=96.0, legend_extra=leg)
