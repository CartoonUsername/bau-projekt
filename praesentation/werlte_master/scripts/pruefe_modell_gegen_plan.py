"""Prüft das verbindliche Modell (scripts/modell_b3.py) maßlich gegen Blatt 25 (SVG, Ansichten M 1:250) und die Geometriedatei.
Jedes erwartete Rechteck aus dem Modell wird in Blattkoordinaten umgerechnet und gegen die Rechtecke der SVG gematcht (Toleranz 0,06 mm = 0,015 m).
Umgekehrt wird jedes Öffnungsrechteck der SVG gegen das Modell gematcht. Ergebnis: Liste Treffer/Abweichungen als Markdown und CSV."""
import re, os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
import modell_b3 as MB
ROOT = MB.ROOT; M = 4.0; TOL = 0.06
SVG = open(os.path.join(ROOT, "varianten_v3", "25_Fassadenkonzept_Ansichten.svg"), encoding="utf-8").read()
RECT = [dict(x=float(m[0]), y=float(m[1]), w=float(m[2]), h=float(m[3]), fill=m[4]) for m in re.findall(r'<rect x="([\d.\-]+)" y="([\d.\-]+)" width="([\d.\-]+)" height="([\d.\-]+)" fill="(#[0-9A-Fa-f]{6})"', SVG)]
DR = MB.Y1
VIEWS = {"front": dict(ox=34.0, gy=100.0, wmax=32.0), "rear": dict(ox=174.0, gy=100.0, wmax=32.0), "west": dict(ox=34.0, gy=215.0, wmax=DR), "east": dict(ox=174.0, gy=215.0, wmax=DR)}
SIDE = {"front": "-y", "rear": "+y", "west": "-x", "east": "+x"}
def span(view, x, y):
    """Modellspanne -> Spanne a entlang der Blickrichtung (wie elev3)"""
    if view == "front": return (32 - x[1], 32 - x[0])
    if view == "rear": return x
    if view == "west": return y
    return (DR - y[1], DR - y[0])
def sheet_rect(view, a, z):
    v = VIEWS[view]; return (v["ox"] + a[0] * M, v["gy"] - z[1] * M, (a[1] - a[0]) * M, (z[1] - z[0]) * M)
def match(r, cand):
    return [c for c in cand if abs(c["x"] - r[0]) < TOL and abs(c["y"] - r[1]) < TOL and abs(c["w"] - r[2]) < TOL and abs(c["h"] - r[3]) < TOL]
OPEN_COL = {"#2B3036", "#E6D9BE", "#CFE0E8", "#FFFFFF"}
rows = []
FREIGEGEBEN = {"Staffel-hinten": "Korrektur 2 (23.10.2026): Höhe z 6,90–9,00 wie Blatt 14 statt Blatt 25 (6,60–9,10)", "EG-hinten": "Korrektur 3: dritte Tür x 1–2,5 entfernt (Bürozugang offen)", "Abluftstutzen": "Korrektur 5: Stutzen entfernt (Dachaustritt offen, C-22)", "Plan-Öffnung ohne Modell": "freigegebene Abweichung Blatt 25 ↔ Modell (Korrekturen 2, 3, 5)"}
def log(view, element, expected, found, note=""): rows.append(dict(ansicht=view, element=element, modell="%.2f/%.2f %.2fx%.2f mm" % expected, plan=("ja" if found else "NEIN"), anmerkung=note))
for view, v in VIEWS.items():
    region = [r for r in RECT if v["ox"] - 6 <= r["x"] <= v["ox"] + v["wmax"] * M + 6 and v["gy"] - 48 <= r["y"] <= v["gy"] + 1 and r["w"] < 140 and r["fill"] != "#FFFFFF" or (v["ox"] - 6 <= r["x"] <= v["ox"] + v["wmax"] * M + 6 and v["gy"] - 48 <= r["y"] <= v["gy"] + 1 and r["fill"] == "#FFFFFF" and r["w"] < 20)]
    expected = []
    for b in MB.boxes(): expected.append((f"Baukörper {b['name']}", sheet_rect(view, span(view, b["x"], b["y"]), b["z"])))
    for b in MB.bands(): expected.append((f"Betonband {b['name']}", sheet_rect(view, span(view, b["x"], b["y"]), b["z"])))
    for b in MB.attika(): expected.append((f"Attika {b['name']}", sheet_rect(view, span(view, b["x"], b["y"]), b["z"])))
    if view == "front":
        for b in MB.balconies(): expected.append((f"Balkonplatte {b['name']}", sheet_rect(view, span(view, b["x"], (0, 0)), (3.2, 3.5)))); expected.append((f"Balkonbrüstung {b['name']}", sheet_rect(view, span(view, b["x"], (0, 0)), (3.5, 4.6))))
    if view == "rear": t = MB.roof_terrace(); expected.append(("Brüstung Dachterrasse", sheet_rect(view, span(view, t["x"], (0, 0)), (6.5, 7.6))))
    if view in ("west", "east"): t = MB.roof_terrace(); expected.append(("Brüstung Dachterrasse seitlich", sheet_rect(view, span(view, (0, 0), (MB.Y2 if MB.Y2 > 18 else 18.0, MB.Y1)), (6.5, 7.6))))
    opens = [o for o in MB.openings("vorschlag") if o["side"] == SIDE[view]]
    open_exp = []
    for o in opens:
        if o["tag"] == "EG-Verglasung": r = sheet_rect(view, span(view, o["a"], o["a"]) if False else ((32 - o["a"][1], 32 - o["a"][0]) if view == "front" else o["a"]), o["z"])
        else:
            a = o["a"]; sp = {"front": (32 - a[1], 32 - a[0]), "rear": a, "west": a, "east": (DR - a[1], DR - a[0])}[view]; r = sheet_rect(view, sp, o["z"])
        open_exp.append((o, r))
    for name, r in expected:
        m = match(r, RECT); log(view, name, r, bool(m))
    for o, r in open_exp:
        m = match(r, RECT); log(view, f"Öffnung {o['tag']} ({o['kind']}, {o['frame']})", r, bool(m), "" if m else "im Plan nicht gefunden")
    # Plan -> Modell: Öffnungsrechtecke der SVG ohne Modellentsprechung
    for c in region:
        if c["fill"] in OPEN_COL and c["w"] < 40:
            if not any(abs(c["x"] - r[0]) < TOL and abs(c["y"] - r[1]) < TOL and abs(c["w"] - r[2]) < TOL and abs(c["h"] - r[3]) < TOL for _, r in open_exp):
                if c["fill"] == "#FFFFFF" and c["h"] < 2: continue
                rows.append(dict(ansicht=view, element="Plan-Öffnung ohne Modell", modell="-", plan="%.2f/%.2f %.2fx%.2f %s" % (c["x"], c["y"], c["w"], c["h"], c["fill"]), anmerkung="FEHLT im Modell: " + FREIGEGEBEN["Plan-Öffnung ohne Modell"]))
bad = [r for r in rows if r["plan"] == "NEIN" or "FEHLT" in r["anmerkung"]]
out = os.path.join(ROOT, "visualisierungen", "higgsfield")
with open(os.path.join(out, "01_modellpruefung_blatt25_v4.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"{len(rows)} Prüfpunkte, {len(rows) - len(bad)} bestanden, {len(bad)} Abweichungen")
for r in bad:
    k = next((k for k in FREIGEGEBEN if k in r["element"]), None); r["anmerkung"] = (r["anmerkung"] + " " + FREIGEGEBEN[k]).strip() if k else r["anmerkung"]; print(r["ansicht"], "|", r["element"], "|", r["modell"], "|", r["plan"], "|", r["anmerkung"])
