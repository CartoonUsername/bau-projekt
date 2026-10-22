"""Erzeugt geometry/building_design.json (Variante A, VORLÄUFIG). Einzige Quelle für Pläne, Prüfung und das spätere Blender-Skript.
Koordinaten: x entlang der langen Seite von West (0) nach Ost (32), y von der Platzfassade (0) nach hinten (18), z Höhe über Erdgeschoss-Fußboden.
Die Himmelsrichtung ist NICHT bekannt (Konflikt C-13)."""
import json, hashlib, os
S = {"V": "VERIFIED", "S": "SOURCE-DEFINED", "A": "ASSUMED", "P": "PROVISIONAL", "R": "REQUIRES-APPROVAL"}
NET = 0.88  # Netto/Brutto Wohnfläche, ASSUMED

def room(id_, typ, level, x0, y0, x1, y1, status="P", **kw):
    d = dict(id=id_, type=typ, level=level, rect=[x0, y0, x1, y1], area_gross=round((x1 - x0) * (y1 - y0), 2), status=S[status])
    d.update(kw)
    return d

D = {
    "model": "NEUE_MITTE_MASTER_DRAFT_A_003",
    "decision": "Variante A verbindlich (Auftraggeber, 22.10.2026). Nachweis der Grundfläche 576 m² steht aus (Konflikt C-01).",
    "units": "m", "origin": "SW-Ecke Gebäude, x West nach Ost, y Platzfassade nach hinten",
    "site": {"area_m2": 960, "grz": 0.6, "footprint_max_theoretical_m2": 576, "envelope_estimate_m2": "400-460 (PROVISIONAL, nicht gemessen)"},
    "building": {"width": 32.0, "depth": 18.0, "footprint_m2": 576.0, "status": S["R"]},
    "levels": [
        {"id": "GF", "name": "Erdgeschoss", "ffl": 0.0, "top": 3.5, "status": S["A"]},
        {"id": "L1", "name": "1. Obergeschoss", "ffl": 3.5, "top": 6.5, "status": S["A"], "note": "Traufhöhe B-Plan 6,50 m"},
        {"id": "L2", "name": "Staffelgeschoss", "ffl": 6.5, "top": 9.6, "status": S["A"], "setback": 0.8},
    ],
    "attika_top": 9.9, "slab_thickness": 0.30,
    "grid": {"x": [4.0, 11.0, 18.0, 25.0, 32.0], "y": [0.0, 8.0, 18.0],
             "note": "Raster 7,0 m in x, 8,0 und 10,0 m in y. Wohngeschoss-Mittelgang bei y 8–10 liegt nicht auf dem Raster: Unterzug/Abfangung, Statik prüfen (PROVISIONAL)"},
    "columns_gf": [[11.0, 8.0], [18.0, 8.0], [25.0, 8.0]],
    "rooms": [],
}
R = D["rooms"]
# ---- Erdgeschoss
R.append(room("CORE-RES-GF", "core", "GF", 0, 0, 4, 18, "A", note="Treppe, Aufzug, Technik, Wohnungseingang"))
R.append(room("DINING-GF", "dining", "GF", 4, 0, 32, 12, "P", seats_note="Gastraum + Lounge + Stehtische + Bar zusammen"))
R.append(room("LOUNGE-GF", "lounge", "GF", 26.0, 0.8, 32, 8.2, "P", seats=20))
R.append(room("BAR-GF", "bar", "GF", 14.5, 9.6, 23.5, 12, "P", seats=12, note="Hocker, Theke 0,7 m, Servicegang 0,8 m, Backbar 0,6 m"))
R.append(room("SEPAREE-GF", "private_dining", "GF", 4, 12, 11, 18, "P", seats=30, partition="Stahl-Glas-Wand an x=11 und y=12"))
R.append(room("SERVICE-GF", "circulation", "GF", 11, 12, 14.5, 18, "P", note="Garderobe/Servicegang"))
R.append(room("WC-GF", "wc", "GF", 14.5, 12, 18.5, 18, "P", note="H, D, barrierefrei, Fachplaner prüft"))
R.append(room("STORE-GF", "storage", "GF", 18.5, 12, 23.5, 18, "P", note="Lager, Kühlung"))
R.append(room("KITCHEN-GF", "kitchen", "GF", 23.5, 12, 32, 18, "P", note="Abluft über Dach, Schacht nötig (C-14)"))
D["gf_seats"] = {"dining_tables": 116, "stehtische": 12, "lounge": 20, "barhocker": 12, "separee": 30, "total_indoor": 190, "terrace": 60}
D["openings"] = [
    {"id": "RESTAURANT-FRONT-001", "type": "glazing", "level": "GF", "wall": "y=0", "x": [4.0, 32.0], "height": 3.1, "status": S["P"], "frame": "schwarz Stahl"},
    {"id": "DOOR-GF-REST-001", "type": "door_double", "level": "GF", "wall": "y=0", "x": [17.0, 19.0], "height": 2.4, "status": S["A"]},
    {"id": "DOOR-GF-RES-001", "type": "door", "level": "GF", "wall": "y=0", "x": [1.0, 2.5], "height": 2.4, "status": S["A"], "note": "Wohnungseingang West"},
]
D["terrace"] = {"id": "TERRACE-001", "rect": [6.0, -3.6, 30.0, 0.0], "area_m2": 86.4, "seats": 60, "status": S["R"], "note": "Lage auf dem Grundstück ungeprüft; Stahlvordach CANOPY-001 schwarz"}
# ---- Obergeschoss: zwei Untersuchungsvarianten (Entscheidung offen)
og1 = []
og1.append(room("OFFICE-1-L1", "office", "L1", 4, 0, 16.5, 8, "A", target=100))
og1.append(room("OFFICE-2-L1", "office", "L1", 4, 10, 12.1, 18, "A", target=65))
for i, (a, b) in enumerate([(16.5, 24.25), (24.25, 32)], 1):
    og1.append(room(f"WE-L1-S{i}", "apartment", "L1", a, 0, b, 8, "P", balcony="front"))
for i, (a, b) in enumerate([(12.1, 18.73), (18.73, 25.37), (25.37, 32)], 1):
    og1.append(room(f"WE-L1-N{i}", "apartment", "L1", a, 10, b, 18, "P", balcony="rear"))
og1.append(room("CORR-L1", "corridor", "L1", 4, 8, 32, 10, "P"))
og2 = []
for i in range(5):
    a = 4 + 5.6 * i
    og2.append(room(f"WE-L1-S{i+1}", "apartment", "L1", round(a, 2), 0, round(a + 5.6, 2), 8, "P", balcony="front"))
og2.append(room("OFFICE-1-L1", "office", "L1", 4, 10, 16.5, 18, "A", target=100))
og2.append(room("OFFICE-2-L1", "office", "L1", 16.5, 10, 24.6, 18, "A", target=65))
og2.append(room("WE-L1-N1", "apartment", "L1", 24.6, 10, 32, 18, "P", balcony="rear"))
og2.append(room("CORR-L1", "corridor", "L1", 4, 8, 32, 10, "P"))
st = []
for i in range(4):
    a = 4.2 + 6.75 * i
    st.append(room(f"WE-L2-S{i+1}", "apartment", "L2", round(a, 2), 0.8, round(a + 6.75, 2), 8.0, "P"))
for i in range(3):
    a = 4.2 + 9.0 * i
    st.append(room(f"WE-L2-N{i+1}", "apartment", "L2", round(a, 2), 10.0, round(a + 9.0, 2), 17.2, "P"))
st.append(room("CORR-L2", "corridor", "L2", 4.2, 8, 31.2, 10, "P"))
st.append(room("CORE-RES-L2", "core", "L2", 0.8, 0.8, 4.2, 17.2, "A"))
D["upper_options"] = {
    "OG-1": {"name": "Mittelgang, Balkone vorn und hinten (2 + 3)", "rooms": og1, "note": "Wohnungen mit realistischen Räumen, Balkonbild der Renderings (5 an der Platzfassade) nicht erfüllt"},
    "OG-2": {"name": "5 kleine Wohnungen vorn mit 5 Balkonen, Büros hinten", "rooms": og2, "note": "Balkonbild der Renderings erfüllt, Wohnungen nur ca. 39 m² netto"},
}
D["staffel"] = {"name": "Staffel S-1: 4 Wohnungen vorn, 3 hinten, Mittelgang", "rooms": st, "note": "Die Renderings zeigen 7 Fensterachsen an der Platzfassade, das lässt sich nur mit 7 Mikrowohnungen von 3,9 m Breite erfüllen"}
D["net_factor"] = NET
D["open_decisions"] = ["Variante OG-1 oder OG-2", "Baufenster/Grundfläche 576 m² nachweisen (C-01)", "Staffelgeschoss als Vollgeschoss (C-02)", "Himmelsrichtung/Platzseite (C-13)", "Statik Abfangung Mittelgang (Raster)", "Rettungswege (C-15)"]
# ---- Arbeitsbasis OG-2 (VORLÄUFIG, keine Festschreibung) und Koordination
D["working_basis"] = {"upper_option": "OG-2", "status": "VORLÄUFIG – geometrische Arbeitsgrundlage, keine endgültige Entscheidung (Auftraggeber 22.10.2026)",
    "separation": "Förderprüfung (Mietstufe, Förderhöhe, Wohnungsanforderungen) ist getrennt in ../foerderung/ und fließt NICHT in die Geometrie ein"}
D["grid_options"] = {
    "R1": {"x": [4.0, 11.0, 18.0, 25.0, 32.0], "note": "7,0-m-Raster der ersten Entwurfsfassung; Mitte (x 18) liegt auf einer Stütze und kollidiert mit der Doppeltür x 17–19; Balkon- und Wohnungsachsen (5,6 m) liegen nicht auf dem Raster"},
    "R2": {"x": [4.0, 9.6, 15.2, 20.8, 26.4, 32.0], "note": "5,6-m-Raster = 5 Felder gleich den 5 Wohnungen/Balkonen des OG-2; x 18 liegt in Feldmitte (Tür frei). VORSCHLAG, REQUIRES-APPROVAL (Tragwerksplaner)"}}
D["grid_working"] = "R2"
D["grid"] = {"x": D["grid_options"]["R2"]["x"], "y": [0.0, 8.0, 18.0], "note": "Arbeitsraster R2 (vorläufig); Mittelgang y 8–10 liegt nicht auf dem y-Raster: Unterzug/Abfangung, Statik prüfen"}
D["columns_gf"] = [[x, 8.0] for x in (9.6, 15.2, 20.8, 26.4)]
D["facade_support"] = {"status": S["R"], "note": "Die OG-Last der Platzfassade (28 m Glasfront) braucht Fassadenstützen oder einen Träger; vollverglaste Front ohne Stützen ist nicht nachgewiesen (C-16). Annahme im Modell: Stützen 0,3 m in Rasterachsen R2 an y=0, noch nicht eingezeichnet.", "candidate_axes_x": D["grid_options"]["R2"]["x"]}
D["core"] = {
    "GF": [{"id": "LOBBY-GF", "rect": [0, 0, 4, 3], "status": S["A"], "note": "Eingang x 1–2,5, Briefkästen"}, {"id": "STAIR-GF", "rect": [0, 3, 4, 8], "status": S["A"]}, {"id": "LANDING-GF", "rect": [0, 8, 4, 10], "status": S["A"], "note": "Aufzugsvorraum, liegt auf Höhe des Mittelgangs"}, {"id": "LIFT-GF", "rect": [0.8, 10, 3.0, 12.6], "status": S["A"]}, {"id": "TECH-GF", "rect": [3.0, 10, 4, 12.6], "status": S["A"]}, {"id": "ABSTELL-GF", "rect": [0, 12.6, 4, 18], "status": S["A"], "note": "Fahrrad/Müll/Abstellräume, Zweck offen"}],
    "L1": [{"id": "RESERVE-L1", "rect": [0, 0, 4, 3], "status": S["A"], "note": "Zweck offen"}, {"id": "STAIR-L1", "rect": [0, 3, 4, 8], "status": S["A"]}, {"id": "LANDING-L1", "rect": [0, 8, 4, 10], "status": S["A"]}, {"id": "LIFT-L1", "rect": [0.8, 10, 3.0, 12.6], "status": S["A"]}, {"id": "TECH-L1", "rect": [3.0, 10, 4, 12.6], "status": S["A"]}, {"id": "ABSTELL-L1", "rect": [0, 12.6, 4, 18], "status": S["A"]}],
    "L2": [{"id": "STAIR-L2", "rect": [0.8, 3, 4.0, 8], "status": S["A"]}, {"id": "LANDING-L2", "rect": [0.8, 8, 4.0, 10], "status": S["A"]}, {"id": "LIFT-L2", "rect": [0.8, 10, 3.0, 12.6], "status": S["A"], "note": "Schacht auf allen Ebenen x 0,8–3,0: Westwand liegt auf der Staffel-Rückversatzlinie; Überfahrt über Attika offen (C-25)"}]}
D["shafts"] = [{"id": "SHAFT-KITCHEN", "rect": [30.0, 16.0, 31.2, 17.2], "levels": ["GF", "L1", "L2", "ROOF"], "status": S["P"], "note": "Küchenabluft; durchläuft Büro/Wohnung N1 (L1) und Staffel-N3 (L2): Geruch, Schall, Brandschutz (C-14)"}]
BW, BD = 2.7, 1.5
bal = []
for i in range(5):
    cx = 4 + 5.6 * i + 2.8
    bal.append({"id": f"BALC-L1-F{i+1}", "level": "L1", "side": "front", "rect": [round(cx - BW / 2, 2), -BD, round(cx + BW / 2, 2), 0.0], "slab_underside_z": 3.2, "railing": "Milchglas 1,1 m", "status": S["P"]})
bal.append({"id": "BALC-L1-R1", "level": "L1", "side": "rear", "rect": [27.35, 18.0, 30.05, 19.5], "slab_underside_z": 3.2, "status": S["P"], "note": "Rückseite nicht im eingefrorenen Design, ragt über 18 m (C-19)"})
D["balconies"] = bal
D["canopy"] = {"id": "CANOPY-001", "rect": [6.0, -3.6, 30.0, 0.0], "underside_z": 3.0, "status": S["A"], "note": "Stahlvordach; liegt unter allen fünf Balkonplatten (Unterseite 3,2 m) und überlappt sie in der Projektion (C-18)"}
D["staffel_alt"] = {"S-2": "5 Wohnungen vorn auf Raster R2 (5,4–5,6 m) + 3 hinten = 8 Staffel-Wohnungen, Gesamt 14 WE; NICHT gewählt, ändert Wohnungszahl, nur Vorschlag (C-09)"}
D["open_decisions"] = ["OG-2 bleibt VORLÄUFIG (nicht festgeschrieben)", "Raster R1 oder R2 (Tragwerk, C-16)", "Staffel S-1 (4 vorn) oder S-2 (5 vorn, +1 WE) (C-09)", "Baufenster/Grundfläche 576 m² nachweisen (C-01)", "Staffelgeschoss als Vollgeschoss (C-02)", "Himmelsrichtung/Platzseite (C-13)", "Rettungswege und Anleiterbarkeit (C-15)", "Küchenschacht (C-14)", "Vordach gegen Balkone (C-18)", "Rückseitiger Balkon / Grenzabstand (C-19)", "Gaststätte als Sonderbau ab ca. 190 + 60 Plätzen (C-20)"]
os.makedirs("../geometry", exist_ok=True)
out = os.path.join(os.path.dirname(__file__), "..", "geometry", "building_design.json")
json.dump(D, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("geschrieben", os.path.abspath(out), hashlib.sha256(json.dumps(D, sort_keys=True).encode()).hexdigest()[:16])
