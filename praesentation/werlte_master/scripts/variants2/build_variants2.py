"""Neue Planungsrichtung (Gastronomie groß, Büros kompakt, Wohngeschosse abgestuft). HYPOTHETISCH, keine Variante festgelegt.
Koordinaten wie building_design.json: x West->Ost, y Platzfassade (0) -> Rückseite, z ab Oberkante Erdgeschoss-Fußboden. Erdgeschoss in allen Varianten 32 x 18 m.
Rechenhypothese H1 (keine Realdaten): Grundstück 32 x 30 m, Platzfassade bei y = 0."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NET = 0.88; SL = 0.30
ST = {"A": "ASSUMED", "P": "PROVISIONAL", "H": "HYPOTHETICAL"}
def R(i, t, lv, x0, y0, x1, y1, st="P", **kw):
    d = dict(id=i, type=t, level=lv, rect=[round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)], status=ST[st]); d["area_gross"] = round((x1 - x0) * (y1 - y0), 2); d.update(kw); return d

def eg(c0):
    core = [R("LOBBY-GF", "core", "GF", 0, 0, 4, c0 - 5, "A"), R("STAIR-GF", "core", "GF", 0, c0 - 5, 4, c0, "A"), R("LANDING-GF", "core", "GF", 0, c0, 4, c0 + 2, "A"),
            R("LIFT-GF", "core", "GF", 0.8, c0 + 2, 3.0, c0 + 4.6, "A"), R("TECH-GF", "core", "GF", 3.0, c0 + 2, 4, c0 + 4.6, "A"), R("WAND-LIFT-GF", "core", "GF", 0, c0 + 2, 0.8, c0 + 4.6, "A"),
            R("ABSTELL-GF", "core", "GF", 0, c0 + 4.6, 4, 18, "A", note="Fahrrad/Abstell Wohnen, Zweck offen")]
    g = [R("DINING-GF", "dining", "GF", 4, 0, 32, 10, "P", note="Gastraum einschließlich Bar"), R("BAR-GF", "bar", "GF", 5, 8.6, 15, 10, "P", seats=12),
         R("WC-GF", "wc", "GF", 4, 10, 10, 14, "P", note="Gäste-WC, barrierefrei"), R("PERSONAL-GF", "circulation", "GF", 10, 10, 15, 14, "P", note="Umkleide, Personal-WC"),
         R("FLUR-GF", "circulation", "GF", 15, 10, 20, 14, "P", note="Flur, Anrichte, Verbindung Gastraum–Küche, Fluchtweg"),
         R("KITCHEN-GF", "kitchen", "GF", 20, 10, 32, 15, "P"), R("STORE-GF", "storage", "GF", 20, 15, 29, 18, "P", note="Lager, Kühlung"), R("ANLIEF-GF", "storage", "GF", 29, 15, 32, 18, "H", note="Anlieferung, Müll; Tür Ost")]
    o = [R("OFFICE-1-GF", "office", "GF", 4, 14, 12, 18, "A"), R("OFFICE-2-GF", "office", "GF", 12, 14, 20, 18, "A")]
    return core + g + o

def variant(key, e1, e2, c0):
    """e1 = Auskragung 1. OG hinter der EG-Rückwand, e2 = Überstand Staffel hinter y = 17,2; c0 = Beginn des Mittelgangs"""
    Y1 = 18 + e1; y2 = 17.2 + e2; rooms = eg(c0)
    rooms += [R("VORRAUM-L1", "core", "L1", 0, 0, 4, c0 - 5, "A", note="Treppenauge/Reserve"), R("STAIR-L1", "core", "L1", 0, c0 - 5, 4, c0, "A"), R("LANDING-L1", "core", "L1", 0, c0, 4, c0 + 2, "A"),
              R("LIFT-L1", "core", "L1", 0.8, c0 + 2, 3.0, c0 + 4.6, "A"), R("TECH-L1", "core", "L1", 3.0, c0 + 2, 4, c0 + 4.6, "A"), R("WAND-LIFT-L1", "core", "L1", 0, c0 + 2, 0.8, c0 + 4.6, "A"),
              R("ABSTELL-L1", "core", "L1", 0, c0 + 4.6, 4, 18, "A", note="Abstell/Technik, Zweck offen")]
    for i in range(5): rooms.append(R(f"WE-L1-V{i+1}", "apartment", "L1", 4 + 5.6 * i, 0, 9.6 + 5.6 * i, c0, "P", balcony="front"))
    rooms.append(R("CORR-L1", "corridor", "L1", 4, c0, 32, c0 + 2, "P"))
    for k in range(4): rooms.append(R(f"WE-L1-H{k+1}", "apartment", "L1", 4 + 7 * k, c0 + 2, 11 + 7 * k, Y1, "P"))
    rooms += [R("VORRAUM-L2", "core", "L2", 0.8, 0.8, 4.2, c0 - 5, "A"), R("STAIR-L2", "core", "L2", 0.8, c0 - 5, 4.2, c0, "A"), R("LANDING-L2", "core", "L2", 0.8, c0, 4.2, c0 + 2, "A"),
              R("LIFT-L2", "core", "L2", 0.8, c0 + 2, 3.0, c0 + 4.6, "A"), R("TECH-L2", "core", "L2", 3.0, c0 + 2, 4.2, c0 + 4.6, "A"), R("ABSTELL-L2", "core", "L2", 0.8, c0 + 4.6, 4.2, 17.2, "A")]
    for i in range(4): rooms.append(R(f"WE-L2-V{i+1}", "apartment", "L2", 4.2 + 6.75 * i, 0.8, 4.2 + 6.75 * (i + 1), c0, "P"))
    rooms.append(R("CORR-L2", "corridor", "L2", 4.2, c0, 31.2, c0 + 2, "P"))
    for k in range(3): rooms.append(R(f"WE-L2-H{k+1}", "apartment", "L2", 4.2 + 9 * k, c0 + 2, 13.2 + 9 * k, y2, "P"))
    sh = dict(id="SHAFT-KITCHEN", rect=[29.8, c0 + 2.0, 31.0, c0 + 3.2], levels=["GF", "L1", "L2", "ROOF"], status=ST["P"])
    gaps = [(5.0, 6.5), (15.0, 16.5)]; stalls = []; x = 0.0
    while x + 2.5 <= 32 + 1e-9:
        g = next((g for g in gaps if x < g[1] and x + 2.5 > g[0]), None)
        if g: x = g[1]; continue
        stalls.append([round(x, 2), 18.0, round(x + 2.5, 2), 23.0]); x += 2.5
    edges = sorted({s[0] for s in stalls} | {s[2] for s in stalls}); cols = []
    if e1 >= 4:
        last = None
        for e in edges:
            if (last is None or e - last >= 4.5) and not any(g[0] <= e <= g[1] for g in gaps) and 4.0 <= e <= 31.0: cols.append([e, round(Y1 - 0.2, 2)]); last = e
    park = dict(plot_hyp=[0, 0, 32, 30], stalls=stalls, aisle=[0, 23.0, 32, 29.0], aisle_width=6.0, columns=cols, walkway_gaps=gaps, covered_depth=min(e1, 5.0), soffit_z=round(3.5 - SL, 2))
    bal = [dict(id=f"BALC-L1-F{i+1}", rect=[round(4 + 5.6 * i + 2.8 - 1.35, 2), -1.5, round(4 + 5.6 * i + 2.8 + 1.35, 2), 0.0]) for i in range(5)]
    outl = dict(GF=[[0, 0], [32, 0], [32, 18], [0, 18]], L1=[[0, 0], [32, 0], [32, Y1], [4, Y1], [4, 18], [0, 18]],
                L2=[[0.8, 0.8], [31.2, 0.8], [31.2, y2], [4.2, y2], [4.2, 17.2], [0.8, 17.2]] if y2 > 17.2 + 1e-9 else [[0.8, 0.8], [31.2, 0.8], [31.2, 17.2], [0.8, 17.2]])
    boxes = [dict(n="EG", x=[0, 32], y=[0, 18], z=[0, 3.5], m="klinker"), dict(n="L1-Haupt", x=[0, 32], y=[0, 18], z=[3.5, 6.5], m="klinker"), dict(n="L1-Anbau", x=[4, 32], y=[18, Y1], z=[3.5, 6.5], m="klinker"),
             dict(n="L2-Haupt", x=[0.8, 31.2], y=[0.8, 17.2], z=[6.5, 9.6], m="laerche"), dict(n="L2-Anbau", x=[4.2, 31.2], y=[17.2, y2], z=[6.5, 9.6], m="laerche")]
    boxes = [b for b in boxes if b["y"][1] - b["y"][0] > 1e-9]
    terr = [4.0, y2, 32.0, Y1]
    return dict(key=key, e1=e1, e2=e2, depth_L1=Y1, y2=y2, c0=c0, rooms=rooms, shaft=sh, parking=park, balconies=bal, outlines=outl, boxes=boxes, roof_terrace=terr)

V = {"A": variant("A", 1.5, 0.0, 8.0), "B": variant("B", 3.0, 1.5, 8.0), "C": variant("C", 4.5, 2.0, 9.0)}
json.dump(dict(model="NEUE_MITTE_VARIANTEN2_ABC_001", status="HYPOTHETISCH, keine Variante festgelegt", hypothesis_H1="Grundstück 32 x 30 m (nur Rechenannahme)", net_factor=NET, variants=V),
          open(os.path.join(ROOT, "geometry", "variants2_ABC.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", {k: (len(v["rooms"]), len(v["parking"]["stalls"]), len(v["parking"]["columns"])) for k, v in V.items()})
