"""Geometrische Untersuchung Neue Planungsrichtung: Varianten A, B, C (HYPOTHETISCH, nicht festgelegt).
Koordinaten wie building_design.json: x West->Ost, y Platzfassade (0) -> Rückseite. Erdgeschoss in allen Varianten 32 x 18 m.
Rechenhypothese H1 (keine Realdaten!): Grundstück 32 x 30 m = 960 m², Platzfassade bei y = 0, Rückseite bei y = 30."""
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NET = 0.88; SL = 0.30
S = {"A": "ASSUMED", "P": "PROVISIONAL", "H": "HYPOTHETICAL", "R": "REQUIRES-APPROVAL"}
def R(i, t, lv, x0, y0, x1, y1, st="P", **kw):
    d = dict(id=i, type=t, level=lv, rect=[round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)], status=S[st]); d["area_gross"] = round((x1 - x0) * (y1 - y0), 2); d.update(kw); return d

def eg(c0):
    """Erdgeschoss 32 x 18 m, in allen Varianten gleich außer der Lage des Kerns (c0 = y des Mittelgangs in den Wohngeschossen)."""
    core = [R("LOBBY-GF", "core", "GF", 0, 0, 4, c0 - 5, "A", name="Eingangshalle Wohnen"), R("STAIR-GF", "core", "GF", 0, c0 - 5, 4, c0, "A"), R("LANDING-GF", "core", "GF", 0, c0, 4, c0 + 2, "A"),
            R("LIFT-GF", "core", "GF", 0.8, c0 + 2, 3.0, c0 + 4.6, "A"), R("TECH-GF", "core", "GF", 3.0, c0 + 2, 4, c0 + 4.6, "A"), R("ABSTELL-GF", "core", "GF", 0, c0 + 4.6, 4, 18, "A", note="Fahrrad/Abstell Wohnen, Zweck offen"), R("WAND-LIFT-GF", "core", "GF", 0, c0 + 2, 0.8, c0 + 4.6, "A", note="Wand/Installationsstreifen")]
    g = [R("DINING-GF", "dining", "GF", 4, 0, 32, 6.3, "P", note="Gastraum einschließlich Bar"), R("BAR-GF", "bar", "GF", 13, 4.9, 23, 6.3, "P", seats=12),
         R("PERSONAL-GF", "circulation", "GF", 4, 6.3, 9, 11.3, "P", note="Umkleide, Personal-WC, Aufenthalt"), R("WC-GF", "wc", "GF", 9, 6.3, 15, 11.3, "P", note="Gäste-WC, barrierefrei"),
         R("STORE-GF", "storage", "GF", 15, 6.3, 22, 11.3, "P", note="Lager, Kühlung"), R("KITCHEN-GF", "kitchen", "GF", 22, 6.3, 32, 11.3, "P")]
    o = [R("OFFICE-1-GF", "office", "GF", 4, 11.3, 20.96, 18, "A", target_net=100), R("OFFICE-2-GF", "office", "GF", 20.96, 11.3, 32, 18, "A", target_net=65)]
    return core + g + o

def variant(key, L, c0, rear_flat_w, drear):
    """L = Auskragung der Wohngeschosse über die Rückwand (m); c0 = y-Beginn des Mittelgangs; drear = Wohnungstiefe hinten"""
    D1 = 18 + L; rooms = eg(c0)
    # Kern in den Wohngeschossen (übereinander)
    def core(lv, x0):
        d = [R(f"STAIR-{lv}", "core", lv, x0, c0 - 5, 4, c0, "A"), R(f"LANDING-{lv}", "core", lv, x0, c0, 4, c0 + 2, "A"), R(f"LIFT-{lv}", "core", lv, 0.8, c0 + 2, 3.0, c0 + 4.6, "A")]
        if lv == "L1": d += [R("TECH-L1", "core", "L1", 3.0, c0 + 2, 4, c0 + 4.6, "A"), R("ABSTELL-L1", "core", "L1", 0, c0 + 4.6, 4, D1, "A", note="Abstell/Fahrrad, Zweck offen"), R("VORRAUM-L1", "core", "L1", 0, 0, 4, c0 - 5, "A", note="Treppenauge/Reserve"), R("WAND-LIFT-L1", "core", "L1", 0, c0 + 2, 0.8, c0 + 4.6, "A")]
        return d
    rooms += core("L1", 0)
    for i in range(5): rooms.append(R(f"WE-L1-V{i+1}", "apartment", "L1", 4 + 5.6 * i, 0, 9.6 + 5.6 * i, c0, "P", balcony="front"))
    rooms.append(R("CORR-L1", "corridor", "L1", 4, c0, 32, c0 + 2, "P"))
    x = 4.0
    for k, w in enumerate(rear_flat_w): rooms.append(R(f"WE-L1-H{k+1}", "apartment", "L1", x, c0 + 2, x + w, D1, "P")); x += w
    assert abs(x - 32) < 1e-6, x
    # Staffel (3. Geschoss), 0,8 m Rücksprung umlaufend
    yf0, yf1, yr0, yr1 = 0.8, c0, c0 + 2, D1 - 0.8
    rooms += [R("VORRAUM-L2", "core", "L2", 0.8, 0.8, 4.2, c0 - 5, "A", note="Treppenauge/Reserve"), R("STAIR-L2", "core", "L2", 0.8, c0 - 5, 4.2, c0, "A"), R("LANDING-L2", "core", "L2", 0.8, c0, 4.2, c0 + 2, "A"),
              R("LIFT-L2", "core", "L2", 0.8, c0 + 2, 3.0, c0 + 4.6, "A"), R("TECH-L2", "core", "L2", 3.0, c0 + 2, 4.2, c0 + 4.6, "A"), R("ABSTELL-L2", "core", "L2", 0.8, c0 + 4.6, 4.2, yr1, "A", note="Abstell/Technik, Zweck offen")]
    for i in range(4): rooms.append(R(f"WE-L2-V{i+1}", "apartment", "L2", 4.2 + 6.75 * i, yf0, 4.2 + 6.75 * (i + 1), yf1, "P"))
    rooms.append(R("CORR-L2", "corridor", "L2", 4.2, c0, 31.2, c0 + 2, "P"))
    nr = 3 if key == "A" else 4; w2 = 27.0 / nr
    for k in range(nr): rooms.append(R(f"WE-L2-H{k+1}", "apartment", "L2", 4.2 + w2 * k, yr0, 4.2 + w2 * (k + 1), yr1, "P"))
    # Küchenschacht über alle Ebenen
    shaft = dict(id="SHAFT-KITCHEN", rect=[29.8, 10.0, 31.0, 11.2], levels=["GF", "L1", "L2", "ROOF"], status=S["P"])
    # Stellplätze (H1)
    gaps = [(10.0, 11.5), (25.0, 26.5)]; stalls = []; x = 0.0
    while x + 2.5 <= 32 + 1e-9:
        g = next((g for g in gaps if x < g[1] and x + 2.5 > g[0]), None)
        if g: x = g[1]; continue
        stalls.append([round(x, 2), 18.0, round(x + 2.5, 2), 23.0]); x += 2.5
    edges = sorted({s[0] for s in stalls} | {s[2] for s in stalls})
    cols = []
    if L >= 5:
        last = None
        for e in edges:
            if last is None or e - last >= 4.5:
                if not any(g[0] <= e <= g[1] for g in gaps) and 1.0 <= e <= 31.0: cols.append([e, 23.0]); last = e
    park = dict(plot_hyp=[0, 0, 32, 30], stalls=stalls, stall_size=[2.5, 5.0], aisle=[0, 23.0, 32, 29.0], aisle_width=6.0, columns=cols, column_size=0.4,
                walkway_gaps=gaps, covered_depth=min(L, 5.0), soffit_z=round(3.5 - SL, 2), note="Stellplatzmaße, Fahrgassenbreite und Höhenanforderung ASSUMED")
    bal = [dict(id=f"BALC-L1-F{i+1}", rect=[round(4 + 5.6 * i + 2.8 - 1.35, 2), -1.5, round(4 + 5.6 * i + 2.8 + 1.35, 2), 0.0], slab_underside_z=3.2) for i in range(5)]
    return dict(key=key, rear_cantilever=L, depth_upper=D1, corridor_y=c0, rooms=rooms, shaft=shaft, parking=park, balconies=bal)

V = {"A": variant("A", 0.0, 8.0, [5.6, 11.2, 11.2], 8), "B": variant("B", 3.0, 8.0, [7.0] * 4, 11), "C": variant("C", 6.0, 11.0, [7.0] * 4, 11)}
OUT = dict(model="NEUE_MITTE_VARIANTEN_ABC_001", status="HYPOTHETISCH, keine Variante festgelegt", hypothesis_H1="Grundstück 32 x 30 m (nur Rechenannahme für 960 m², keine Realdaten), Platzfassade y=0", net_factor=NET,
           ground_floor_common=True, variants=V)
json.dump(OUT, open(os.path.join(ROOT, "geometry", "variants_ABC.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", {k: len(v["rooms"]) for k, v in V.items()}, {k: (len(v["parking"]["stalls"]), len(v["parking"]["columns"])) for k, v in V.items()})
