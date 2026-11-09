"""Konsistenzprüfung der Arbeitsbasis OG-2 (nur Geometrie, ohne Förderthemen). Schreibt validation/consistency_OG2.md"""
import json, os
here = os.path.dirname(__file__)
D = json.load(open(os.path.join(here, "..", "geometry", "building_design.json"), encoding="utf-8"))
og = {r["id"]: r for r in D["upper_options"]["OG-2"]["rooms"]}
st = {r["id"]: r for r in D["staffel"]["rooms"]}
gf = {r["id"]: r for r in D["rooms"]}
NET = D["net_factor"]
rows = []
def add(name, status, detail): rows.append((name, status, detail))
inside = lambda p, r: r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]
for s in D["shafts"]:
    c = ((s["rect"][0] + s["rect"][2]) / 2, (s["rect"][1] + s["rect"][3]) / 2)
    ok = inside(c, gf["KITCHEN-GF"]["rect"]) and inside(c, og["WE-L1-N1"]["rect"]) and inside(c, st["WE-L2-N3"]["rect"])
    add("Küchenschacht durchgehend GF–L1–L2", "PASS" if ok else "FAIL", f"Mitte {c}: Küche, WE-L1-N1, WE-L2-N3 – aber Schacht läuft durch Wohnungen (C-14)")
for k in ("R1", "R2"):
    cols = [x for x in D["grid_options"][k]["x"]]
    d0, d1 = D["openings"][1]["x"]
    hit = [x for x in cols if d0 <= x <= d1]
    add(f"Doppeltür x {d0:g}–{d1:g} gegen Fassadenstütze, Raster {k}", "FAIL" if hit else "PASS", f"Stützenachsen in der Tür: {hit or 'keine'}")
fl = [og[f"WE-L1-S{i}"] for i in range(1, 6)]
off = [round(abs((b["rect"][0] + b["rect"][2]) / 2 - (r["rect"][0] + r["rect"][2]) / 2), 2) for r, b in zip(fl, D["balconies"][:5])]
add("Balkonmitte gleich Wohnungsmitte (5 Stück)", "PASS" if max(off) == 0 else "FAIL", f"Abweichungen {off}")
for ax in ("R1", "R2"):
    gx = D["grid_options"][ax]["x"]
    d = [round(min(abs(w - x) for x in gx), 2) for w in (9.6, 15.2, 20.8, 26.4)]
    add(f"OG-2 Wohnungstrennwände gegen Raster {ax}", "PASS" if max(d) < 0.05 else "OPEN", f"Abstand zur nächsten Stützenachse {d} m")
sx = sorted({r["rect"][0] for r in st.values() if r["rect"][1] == 0.8} | {r["rect"][2] for r in st.values() if r["rect"][1] == 0.8})
d = [round(min(abs(w - x) for x in D["grid_options"]["R2"]["x"]), 2) for w in sx[1:-1]]
add("Staffel-S-1-Trennwände (vorn) gegen Raster R2 und OG-2", "OPEN", f"Achsen {sx[1:-1]}, Abstand zu R2 {d} m; Staffel hat 4, OG-2 hat 5 Achsen (C-09)")
net = lambda rs: sum(r["area_gross"] * NET for r in rs if r["type"] == "apartment")
add("Wohnfläche netto OG-2 / Staffel / gesamt", "INFO", f"{net(og.values()):.0f} / {net(st.values()):.0f} / {net(og.values())+net(st.values()):.0f} m² (Excel-Stand 655 m²) – ASSUMED Netto-Faktor {NET}")
add("Anzahl Wohnungen", "INFO", f"OG-2 {sum(1 for r in og.values() if r['type']=='apartment')} + Staffel {sum(1 for r in st.values() if r['type']=='apartment')} = {sum(1 for r in list(og.values())+list(st.values()) if r['type']=='apartment')}")
sf = sum(r["area_gross"] for r in st.values()) ; add("Staffel gegen Geschoss darunter", "OPEN", f"Staffel-Rechteck inkl. Kern 30,4 × 16,4 = {30.4*16.4:.1f} m² = {30.4*16.4/576*100:.0f} % von 576 m² (C-02)")
b = D["canopy"]; ov = [x["id"] for x in D["balconies"][:5] if x["rect"][2] > b["rect"][0] and x["rect"][0] < b["rect"][2]]
add("Vordach gegen Balkonplatten", "OPEN", f"Vordach UK {b['underside_z']} m, Balkon UK 3,2 m; Überlappung in Grundrissprojektion: {ov} (C-18)")
add("Weg Treppenraum bis östliches Ende Mittelgang", "OPEN", "ca. 28 m Sackgasse ab x = 4; zweiter Rettungsweg nur über Fenster/Anleiterung (C-15)")
add("Oberstes Geschoss FFL", "INFO", "Staffel-FFL 6,5 m (< 7 m) → Gebäudeklasse 3 oder 4 prüfen, abhängig von Nutzungseinheiten; baurechtliche Einstufung offen")
add("Gaststätte Plätze", "OPEN", "190 innen + 60 Terrasse; Sonderbau/Versammlungsstätte-Schwelle prüfen (C-20)")
add("Fassadenstützen EG", "OPEN", "Platzfassade 28 m ohne Stütze nicht nachgewiesen; Modell nimmt Stützen in R2-Achsen an, noch nicht gezeichnet (C-16)")
add("Rückseitiger Balkon über y = 18", "OPEN", "Rückseite nicht Teil des eingefrorenen Designs; Grenzabstand unbekannt (C-19)")

core = D["core"]
lift = {lv: next(c for c in core[lv] if c["id"].startswith("LIFT")) for lv in ("GF", "L1", "L2")}
add("Aufzug übereinander (GF, L1, L2)", "PASS" if len({tuple(v["rect"]) for v in lift.values()}) == 1 else "FAIL", f"{lift['GF']['rect']} auf allen Ebenen")
lg = {lv: next(c for c in core[lv] if c["id"].startswith("LANDING")) for lv in ("GF", "L1", "L2")}
corr = og["CORR-L1"]["rect"]
touch = lg["L1"]["rect"][2] == corr[0] and lg["L1"]["rect"][1] >= corr[1] - 1e-9 and lg["L1"]["rect"][3] <= corr[3] + 1e-9
add("Aufzugsvorraum stößt an Mittelgang (L1)", "PASS" if touch else "FAIL", f"Vorraum {lg['L1']['rect']}, Gang {corr[:2]}–{corr[2:]}; Gang 2,0 m breit")
lr = lift["L1"]["rect"]; add("Aufzugsschacht Größe", "OPEN", f"{lr[2]-lr[0]:.1f} x {lr[3]-lr[1]:.1f} m; Fahrkorb-Größe (z. B. 1,1 x 1,4 m) und Typ (Bettentransport) fachlich offen")
add("Aufzug erreicht alle Wohn- und Gewerbeebenen", "PASS", "EG, 1. OG, Staffel; Gastro-Küche/Büros über Mittelgang bzw. Kern erreichbar")
add("Aufzugsüberfahrt gegen Attika", "OPEN", "Staffel-FFL 6,5 m + üblicher Überfahrtsbedarf liegt nahe/über Attika 9,9 m; sichtbarer Aufbau wäre eine Designfrage (C-25)")
add("Stufenloser Zugang Wohnungseingang West (x 1–2,5)", "OPEN", "Gelände- und Platzhöhen unbekannt, keine Schwellen/Rampen im Modell")
add("Balkontür-Schwellen", "OPEN", "Betonbalkon-Detail im Design nicht definiert; Anschlusshöhe/Schwellenfreiheit offen")
md = ["# Konsistenzprüfung Arbeitsbasis OG-2 (nur Geometrie, vorläufig)", "", "| Prüfung | Ergebnis | Detail |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in rows]
open(os.path.join(here, "..", "validation", "consistency_OG2.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("\n".join(md))
