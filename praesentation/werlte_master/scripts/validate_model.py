"""Prüft geometry/building_design.json und schreibt validation/validation_report.md. Vergleicht Koordinaten, nicht Bilder."""
import json, hashlib, os
here = os.path.dirname(__file__)
D = json.load(open(os.path.join(here, "..", "geometry", "building_design.json"), encoding="utf-8"))
NET = D["net_factor"]
res = []
def chk(name, ok, detail, level="PASS"):
    res.append((name, "PASS" if ok else level, detail))
def area(r): return round((r["rect"][2] - r["rect"][0]) * (r["rect"][3] - r["rect"][1]), 2)
b = D["building"]
chk("Grundfläche gegen GRZ-Maximum", b["footprint_m2"] <= 0.6 * 960 + 1e-6, f"{b['width']} × {b['depth']} = {b['footprint_m2']} m², Maximum {0.6*960} m²")
chk("Grundfläche gegen Baufenster-Schätzung", False, "576 m² liegen über der geschätzten Baufenster-Größe 400–460 m², Nachweis fehlt (C-01)", "OPEN")
tops = [l["top"] for l in D["levels"]]
chk("Traufhöhe", abs(D["levels"][1]["top"] - 6.5) < 1e-6, f"OG-Oberkante {D['levels'][1]['top']} m gegen 6,50 m")
chk("Gesamthöhe", D["attika_top"] <= 12.0, f"Attika {D['attika_top']} m gegen max. 12,00 m (Messregel unbestätigt)")
# Geschosshöhen lückenlos
ok = all(abs(D["levels"][i]["ffl"] - D["levels"][i-1]["top"]) < 1e-6 for i in range(1, len(D["levels"])))
chk("Geschosse lückenlos", ok, "ffl jedes Geschosses = top des darunter")
# EG
gf = [r for r in D["rooms"] if r["level"] == "GF"]
core = next(r for r in gf if r["type"] == "core")
gastro = round(sum(area(r) for r in gf if r["type"] not in ("core", "lounge", "bar")), 2)  # Lounge und Bar liegen innerhalb des Gastraums DINING-GF
chk("EG vollständig belegt", abs(gastro + area(core) - b["footprint_m2"]) < 0.01, f"Kern {area(core)} + Gastro {gastro} = {gastro+area(core)} m²")
chk("Gastrofläche gegen Ziel 510 m²", abs(gastro - 510) / 510 <= 0.02, f"{gastro} m² (Abweichung {gastro-510:+.1f} m²)", "WARN")
seats = sum(r.get("seats", 0) for r in gf)
chk("Sitzplätze ohne Gastraumtische", True, f"Lounge 20 + Barhocker 12 + Séparée 30 = {seats}; Gastraumtische 116 + Stehtische 12 kommen aus dem Programm, nicht aus Möblierungsplan")
total = seats + D["gf_seats"]["dining_tables"] + D["gf_seats"]["stehtische"]
chk("Innenplätze gegen Ziel 190", total == 190, f"{total} Plätze, {gastro/total:.2f} m² je Platz")
dz = next(r for r in gf if r["id"] == "DINING-GF")
free = area(dz) - sum(area(r) for r in gf if r["id"] in ("LOUNGE-GF", "BAR-GF"))
chk("Fläche Gastraumtische", (free / (116 + 12)) >= 1.9, f"{free:.1f} m² frei für 128 Plätze = {free/128:.2f} m² je Platz (Richtwert 1,9)", "WARN")
chk("Terrasse 60 Plätze", D["terrace"]["area_m2"] / 60 >= 1.4, f"{D['terrace']['area_m2']} m² = {D['terrace']['area_m2']/60:.2f} m² je Platz, Lage auf Grundstück ungeprüft", "WARN")
for name, opt in D["upper_options"].items():
    rs = opt["rooms"]
    apts = [r for r in rs if r["type"] == "apartment"]
    net = sum(area(r) for r in apts) * NET
    offices = {r["id"]: area(r) for r in rs if r["type"] == "office"}
    front = sum(1 for r in apts if r.get("balcony") == "front"); rear = sum(1 for r in apts if r.get("balcony") == "rear")
    chk(f"{name}: Büroflächen", all(abs(offices[k] - t) < 1.0 for k, t in (("OFFICE-1-L1", 100), ("OFFICE-2-L1", 65))), f"{offices}")
    chk(f"{name}: Wohnungen", True, f"{len(apts)} Wohnungen, {sum(area(r) for r in apts):.1f} m² brutto, ca. {net:.0f} m² netto, kleinste {min(area(r) for r in apts)*NET:.0f} m² netto; Balkone vorn {front}, hinten {rear}")
    chk(f"{name}: Balkonbild der Renderings (5 vorn, 0 an Kurzseite)", front == 5, f"vorn {front}", "OPEN")
st = D["staffel"]["rooms"]
apts = [r for r in st if r["type"] == "apartment"]
chk("Staffelgeschoss: Wohnungen", True, f"{len(apts)} Wohnungen, ca. {sum(area(r) for r in apts)*NET:.0f} m² netto (Modell 334 m²)")
front = sum(1 for r in apts if r["rect"][1] < 1.0)
chk("Staffel: 7 Fensterachsen an der Platzfassade", front == 7, f"{front} Wohnungen an der Platzfassade", "OPEN")
sb = D["levels"][2]["setback"]
sa = (b["width"] - 2 * sb) * (b["depth"] - 2 * sb)
chk("Staffel gegen Vollgeschoss-Schwelle", sa / b["footprint_m2"] < 0.75, f"Staffel {sa:.1f} m² = {sa/b['footprint_m2']*100:.0f} % des Geschosses darunter (Schwelle 75 % laut üblicher Regel, Landesrecht prüfen, C-02)", "OPEN")
# Überlappungen im EG
def ov(a, b_):
    return not (a[2] <= b_[0] or b_[2] <= a[0] or a[3] <= b_[1] or b_[3] <= a[1])
bad = [(a["id"], c["id"]) for i, a in enumerate(gf) for c in gf[i+1:] if ov(a["rect"], c["rect"]) and not ({a["id"], c["id"]} & {"DINING-GF"})]
chk("EG ohne Überlappungen (außer Aufenthaltsbereiche im Gastraum)", not bad, f"{bad}")
h = hashlib.sha256(json.dumps(D, sort_keys=True).encode()).hexdigest()
out = ["# Validierungsbericht (Variante A, Entwurf)", "", f"Modell: {D['model']}", f"Geometrie-Hash (SHA-256, gekürzt): `{h[:16]}`", "", "Status: ENTWURF, nicht freigegeben. PASS bedeutet nur, dass die Datei in sich stimmt. OPEN/WARN sind echte Aufgaben.", "", "| Prüfung | Ergebnis | Detail |", "|---|---|---|"]
for n, s, d in res: out.append(f"| {n} | {s} | {d} |")
out += ["", "## Offene Entscheidungen"] + [f"- {x}" for x in D["open_decisions"]]
os.makedirs(os.path.join(here, "..", "validation"), exist_ok=True)
open(os.path.join(here, "..", "validation", "validation_report.md"), "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
