"""Runde 3: Variante B als Arbeitsgrundlage (B3, VORLÄUFIG, nicht festgelegt). Mittelgang bei y 9,5 (ausgeglichene Wohnungstiefen), Büro-Zugang/WC (Alternativen K, F, M), maßstäbliche Möblierung der Gastronomie.
Koordinaten wie building_design.json. Hypothese H1 (Grundstück 32 x 30 m) ist KEINE bestätigte Größe."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NET = 0.88; SL = 0.30; ST = {"A": "ASSUMED", "P": "PROVISIONAL", "H": "HYPOTHETICAL"}
def R(i, t, lv, x0, y0, x1, y1, st="P", **kw):
    d = dict(id=i, type=t, level=lv, rect=[round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)], status=ST[st]); d["area_gross"] = round((x1 - x0) * (y1 - y0), 2); d.update(kw); return d
C0 = 9.5; E1 = 3.0; E2 = 1.5; Y1 = 18 + E1; Y2 = 17.2 + E2

def service(alt):
    """Gastronomie-Service und Büros im hinteren EG. alt: K Kern-Foyer, F Flur zwischen den Büros, M Mitbenutzung Gäste-WC"""
    g = [R("DINING-GF", "dining", "GF", 4, 0, 32, 10, "P", note="Gastraum einschließlich Bar"), R("BAR-GF", "bar", "GF", 5, 8.6, 15, 10, "P", seats=12),
         R("WC-GF", "wc", "GF", 4, 10, 10, 14, "P", note="Gäste-WC, barrierefrei"), R("PERSONAL-GF", "circulation", "GF", 10, 10, 15, 14, "P", note="Umkleide, Personal-WC"),
         R("FLUR-GF", "circulation", "GF", 15, 10, 20, 14, "P", note="Flur, Anrichte, Verbindung Gastraum–Küche, Fluchtweg"),
         R("KITCHEN-GF", "kitchen", "GF", 20, 10, 32, 15, "P"), R("STORE-GF", "storage", "GF", 20, 15, 29, 18, "P"), R("ANLIEF-GF", "storage", "GF", 29, 15, 32, 18, "H", note="Anlieferung, Müll; Tür Ost")]
    if alt in ("K", "M"): o = [R("OFFICE-1-GF", "office", "GF", 4, 14, 12, 18, "A"), R("OFFICE-2-GF", "office", "GF", 12, 14, 20, 18, "A")]
    else: o = [R("OFFICE-1-GF", "office", "GF", 4, 14, 11.2, 18, "A"), R("BUERO-WC-GF", "wc", "GF", 11.2, 14, 13.6, 16, "A", note="Büro-WC barrierefrei"), R("BUERO-FLUR-GF", "foyer", "GF", 11.2, 16, 13.6, 18, "A", note="Büro-Flur mit Rückzugang"), R("OFFICE-2-GF", "office", "GF", 13.6, 14, 20, 18, "A")]
    return g + o

def core(alt, lv):
    c0 = C0
    if lv == "GF":
        r = [R("LOBBY-GF", "core", "GF", 0, 0, 4, c0 - 5, "A"), R("STAIR-GF", "core", "GF", 0, c0 - 5, 4, c0, "A"), R("LANDING-GF", "core", "GF", 0, c0, 4, c0 + 2, "A"),
             R("LIFT-GF", "core", "GF", 0.8, c0 + 2, 3.0, c0 + 4.6, "A"), R("TECH-GF", "core", "GF", 3.0, c0 + 2, 4, c0 + 4.6, "A"), R("WAND-LIFT-GF", "core", "GF", 0, c0 + 2, 0.8, c0 + 4.6, "A")]
        if alt == "K": r += [R("BUERO-WC-GF", "wc", "GF", 0, c0 + 4.6, 2.3, c0 + 6.7, "A", note="Büro-WC barrierefrei"), R("BUERO-FOYER-GF", "foyer", "GF", 2.3, c0 + 4.6, 4, c0 + 6.7, "A"), R("BUERO-FOYER2-GF", "foyer", "GF", 0, c0 + 6.7, 4, 18, "A", note="Büro-Foyer mit Rückzugang")]
        else: r += [R("ABSTELL-GF", "core", "GF", 0, c0 + 4.6, 4, 18, "A", note="Fahrrad/Abstell Wohnen")]
        return r
    x0 = 0 if lv == "L1" else 0.8; xe = 4.0 if lv == "L1" else 4.2; ye = 18 if lv == "L1" else 17.2
    r = [R(f"STAIR-{lv}", "core", lv, x0, c0 - 5, xe, c0, "A"), R(f"LANDING-{lv}", "core", lv, x0, c0, xe, c0 + 2, "A"), R(f"LIFT-{lv}", "core", lv, 0.8, c0 + 2, 3.0, c0 + 4.6, "A"), R(f"TECH-{lv}", "core", lv, 3.0, c0 + 2, xe, c0 + 4.6, "A"),
         R(f"ABSTELL-{lv}", "core", lv, x0, c0 + 4.6, xe, ye, "A", note="Abstell Wohnen")]
    r.append(R(f"VORRAUM-{lv}", "core", lv, x0, 0 if lv == "L1" else 0.8, xe, c0 - 5, "A"))
    if lv == "L1": r.append(R("WAND-LIFT-L1", "core", "L1", 0, c0 + 2, 0.8, c0 + 4.6, "A"))
    return r

def build(alt="K"):
    rooms = core(alt, "GF") + service(alt) + core(alt, "L1") + core(alt, "L2")
    for i in range(5): rooms.append(R(f"WE-L1-V{i+1}", "apartment", "L1", 4 + 5.6 * i, 0, 9.6 + 5.6 * i, C0, "P", balcony="front"))
    rooms.append(R("CORR-L1", "corridor", "L1", 4, C0, 32, C0 + 2, "P"))
    for k in range(4): rooms.append(R(f"WE-L1-H{k+1}", "apartment", "L1", 4 + 7 * k, C0 + 2, 11 + 7 * k, Y1, "P"))
    for i in range(4): rooms.append(R(f"WE-L2-V{i+1}", "apartment", "L2", 4.2 + 6.75 * i, 0.8, 4.2 + 6.75 * (i + 1), C0, "P"))
    rooms.append(R("CORR-L2", "corridor", "L2", 4.2, C0, 31.2, C0 + 2, "P"))
    for k in range(3): rooms.append(R(f"WE-L2-H{k+1}", "apartment", "L2", 4.2 + 9 * k, C0 + 2, 13.2 + 9 * k, Y2, "P"))
    sh = dict(id="SHAFT-KITCHEN", rect=[29.8, C0 + 2.0, 31.0, C0 + 3.2], levels=["GF", "L1", "L2", "ROOF"], status=ST["P"])
    gaps = [(5.0, 6.5), (15.0, 16.5)]; stalls = []; x = 0.0
    while x + 2.5 <= 32 + 1e-9:
        g = next((g for g in gaps if x < g[1] and x + 2.5 > g[0]), None)
        if g: x = g[1]; continue
        stalls.append([round(x, 2), 18.0, round(x + 2.5, 2), 23.0]); x += 2.5
    park = dict(plot_hyp=[0, 0, 32, 30], stalls=stalls, aisle=[0, 23.0, 32, 29.0], aisle_width=6.0, columns=[], walkway_gaps=gaps, covered_depth=min(E1, 5.0), soffit_z=round(3.5 - SL, 2))
    bal = [dict(id=f"BALC-L1-F{i+1}", rect=[round(4 + 5.6 * i + 2.8 - 1.35, 2), -1.5, round(4 + 5.6 * i + 2.8 + 1.35, 2), 0.0]) for i in range(5)]
    outl = dict(GF=[[0, 0], [32, 0], [32, 18], [0, 18]], L1=[[0, 0], [32, 0], [32, Y1], [4, Y1], [4, 18], [0, 18]], L2=[[0.8, 0.8], [31.2, 0.8], [31.2, Y2], [4.2, Y2], [4.2, 17.2], [0.8, 17.2]])
    boxes = [dict(n="EG", x=[0, 32], y=[0, 18], z=[0, 3.5], m="klinker"), dict(n="L1-Haupt", x=[0, 32], y=[0, 18], z=[3.5, 6.5], m="klinker"), dict(n="L1-Anbau", x=[4, 32], y=[18, Y1], z=[3.5, 6.5], m="klinker"),
             dict(n="L2-Haupt", x=[0.8, 31.2], y=[0.8, 17.2], z=[6.5, 9.6], m="laerche"), dict(n="L2-Anbau", x=[4.2, 31.2], y=[17.2, Y2], z=[6.5, 9.6], m="laerche")]
    return dict(key="B3", alt=alt, e1=E1, e2=E2, depth_L1=Y1, y2=Y2, c0=C0, rooms=rooms, shaft=sh, parking=park, balconies=bal, outlines=outl, boxes=boxes, roof_terrace=[4.0, Y2, 32.0, Y1])

# ---------- maßstäbliche Möblierung ----------
TB = (1.2, 0.8); CH = 0.45        # Tisch 1,2 x 0,8 m (4 Plätze), Stuhl 0,45 x 0,45 m  (ASSUMED)
LAYOUTS = {"komfortabel": dict(pitch=2.4, rows=[0.5, 3.6, 6.7], label="komfortabel (Reihenabstand 1,4 m, Tischabstand 1,2 m)"),
           "normal": dict(pitch=2.1, rows=[0.5, 3.4, 6.3], label="normal (Reihenabstand 1,2 m, Tischabstand 0,9 m)"),
           "dicht": dict(pitch=1.7, rows=[0.4, 3.2, 6.0], label="dicht (Reihenabstand 1,1 m, Tischabstand 0,5 m)")}
LANES = [(16.8, 19.2), (29.3, 31.2)]      # freizuhaltende Fluchtwege vor den beiden Platz-Ausgängen
def furnish(layout):
    p = LAYOUTS[layout]; tables = []
    for ri, y in enumerate(p["rows"]):
        x = 4.6
        while x + TB[0] <= 31.8 + 1e-9:
            rect = (x, y, x + TB[0], y + 0.9 + TB[1] + 0.0)  # Tisch mit Stuhlüberstand
            occupied = (x - 0.1, y - 0.05, x + TB[0] + 0.1, y + CH + TB[1] + CH + 0.05)
            bad = any(occupied[0] < l[1] and occupied[2] > l[0] for l in LANES)
            if y + CH + TB[1] + CH > 7.0 and x < 15.8: bad = True      # Barzugang und Stehbereich vor der Bar (y ab 7,0 m, x bis 15,8 m)
            if y + CH + TB[1] + CH > 10 - 0.05: bad = True
            if not bad: tables.append(dict(x=round(x, 2), y=round(y + CH, 2), row=ri))
            x += p["pitch"]
    seats = 4 * len(tables); stools = [[round(5.5 + 0.8 * i, 2), 8.25] for i in range(12)]
    return dict(layout=layout, label=p["label"], tables=tables, seats_tables=seats, stools=stools, seats=seats + 12)
def terrace(layout):
    # Terrasse 24 x 3,6 m: eine Reihe 4er-Tische entlang der Fassade, Stühle beidseitig
    pitch = {"komfortabel": 2.4, "normal": 2.1, "dicht": 1.7}[layout]; ts = []; x = 6.5
    while x + TB[0] <= 29.5 + 1e-9: ts.append(dict(x=round(x, 2), y=round(-3.6 + 0.7 + CH, 2))); x += pitch
    return dict(tables=ts, seats=4 * len(ts))

if __name__ == "__main__":
    out = dict(model="NEUE_MITTE_B3_ARBEITSGRUNDLAGE_001", status="VORLÄUFIG, Variante B nur Arbeitsgrundlage, nicht festgelegt", hypothesis_H1="Grundstück 32 x 30 m ist eine Rechenannahme, keine bestätigte Größe", net_factor=NET,
               variants={alt: build(alt) for alt in ("K", "F", "M")}, furnishing={l: dict(furnish(l), terrace=terrace(l)) for l in LAYOUTS})
    json.dump(out, open(os.path.join(ROOT, "geometry", "variant_B3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print({l: (f["seats_tables"], f["seats"], f["terrace"]["seats"]) for l, f in out["furnishing"].items()})
