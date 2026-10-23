"""Unabhängiger Plan-Ist-Abgleich: Modell (scripts/modell_b3.py) gegen die Ursprungsunterlage Blatt 14 (varianten_v2/14_Variante_B_Ansichten.svg, PDF-Seite 4 von Varianten_v2_ABC_Gesamt.pdf).
Blatt 14 entsteht aus einem anderen Skript (variants2_sheets.py) als Blatt 25, ist also kein Zirkelschluss. Jedes Rechteck der SVG wird in Meter (a = Koordinate entlang der Ansicht, z = Höhe) zurückgerechnet und mit dem Modell verglichen.
Ausgabe: visualisierungen/higgsfield/06_pruefpunkte_blatt14.csv"""
import re, os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
import modell_b3 as MB
ROOT = MB.ROOT; M = 4.0; DR = MB.Y1; TOL = 0.03   # 3 cm
S = open(os.path.join(ROOT, "varianten_v2", "14_Variante_B_Ansichten.svg"), encoding="utf-8").read()
def attr(m, k):
    r = re.search(r' %s="([^"]*)"' % k, m); return r.group(1) if r else None
RECT = []
for m in re.findall(r"<rect [^>]*>", S):
    try: RECT.append(dict(x=float(attr(m, "x")), y=float(attr(m, "y")), w=float(attr(m, "width")), h=float(attr(m, "height")), fill=attr(m, "fill"), dash=attr(m, "stroke-dasharray")))
    except TypeError: pass
VIEWS = {"front": (34.0, 100.0, 32.0, "-y", "Platzseite"), "rear": (174.0, 100.0, 32.0, "+y", "Rückseite"), "west": (34.0, 215.0, DR, "-x", "Kernseite"), "east": (174.0, 215.0, DR, "+x", "Ostseite")}
def to_m(view, r):
    ox, gy, w, _, _ = VIEWS[view]; a0 = (r["x"] - ox) / M; a1 = a0 + r["w"] / M; z1 = (gy - r["y"]) / M; z0 = z1 - r["h"] / M
    if view == "front": a0, a1 = 32 - a1, 32 - a0
    if view == "east": a0, a1 = DR - a1, DR - a0
    return (a0, a1, z0, z1)
def model_span(view, x, y):
    if view == "front": return (x[0], x[1])
    if view == "rear": return (x[0], x[1])
    if view == "west": return (y[0], y[1])
    return (y[0], y[1])
def in_view(view, r):
    ox, gy, w, _, _ = VIEWS[view]; return ox - 8 <= r["x"] <= ox + w * M + 8 and gy - 50 <= r["y"] <= gy + 1 and r["w"] <= w * M + 2
def close(a, b): return all(abs(p - q) <= TOL for p, q in zip(a, b))
SRC = "varianten_v2/14_Variante_B_Ansichten.svg (PDF Varianten_v2_ABC_Gesamt.pdf S. 4 = Blatt 14)"
rows = []
def row(view, bauteil, modell, plan, status, hinweis=""): rows.append(dict(ansicht=VIEWS[view][4], bauteil=bauteil, modell_m=modell, blatt14_m=plan, status=status, hinweis=hinweis))
fmt = lambda t: "a %.2f–%.2f / z %.2f–%.2f" % t if t else "-"
for view in VIEWS:
    plan = [(to_m(view, r), r) for r in RECT if in_view(view, r)]
    used = set()
    def find(t):
        for i, (pt, r) in enumerate(plan):
            if close(pt, t): used.add(i); return pt
        return None
    # Baukörper
    for b in MB.boxes():
        a = model_span(view, b["x"], b["y"]); t = (a[0], a[1], b["z"][0], b["z"][1])
        p = find(t); row(view, "Baukörper " + b["name"], fmt(t), fmt(p), "bestätigt" if p else "ungeklärt", "" if p else "Rechteck in Blatt 14 nicht gefunden")
    # Öffnungen dieser Ansicht
    for o in MB.openings():
        if o["side"] != VIEWS[view][3]: continue
        a = o["a"]; t = (a[0], a[1], *o["z"])
        p = find(t)
        if p: row(view, f"Öffnung {o['tag']} ({o['kind']})", fmt(t), fmt(p), "bestätigt", "Lage in Blatt 14 als schematisch/Maße offen gekennzeichnet" if o["kind"] == "glas" and "EG-V" not in o["tag"] else "")
        else: row(view, f"Öffnung {o['tag']} ({o['kind']})", fmt(t), "-", "Abweichung", "im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung)")
    if view == "front":
        for b in MB.balconies():
            for nm, z in (("Balkonplatte", (3.2, 3.5)), ("Balkonbrüstung", (3.5, 4.6))):
                t = (b["x"][0], b["x"][1], *z); p = find(t); row(view, f"{nm} {b['name']}", fmt(t), fmt(p), "bestätigt" if p else "ungeklärt", "" if p else "in Blatt 14 nicht als eigenes Rechteck (Platte) gezeichnet")
        v = MB.vordach(); t = (v["x"][0], v["x"][1], *v["z"]); p = find(t); row(view, "Stahlvordach", fmt(t), fmt(p), "bestätigt" if p else "Abweichung", "Blatt 14 zeichnet das Vordach (24 m x 3,6 m, Unterkante +3,00 m) – Blatt 25 nicht")
    if view == "rear":
        tt = MB.roof_terrace(); t = (tt["x"][0], tt["x"][1], 6.5, 7.6); p = find(t); row(view, "Brüstung Dachterrasse hinten", fmt(t), fmt(p), "bestätigt" if p else "ungeklärt")
    if view in ("west", "east"):
        row(view, "Brüstung Dachterrasse seitlich", "y 18,7–21,0 / z 6,50–7,60", "-", "Abweichung", "Blatt 14 zeichnet keine seitliche Brüstung; Blatt 25 schon")
    if view == "east": row(view, "Abluftstutzen", "y 11,73–12,48 / z 9,90–10,80", "-", "Abweichung", "Blatt 14: 'Abluftführung über Dach (Austritt) ist nicht dargestellt' (C-22)")
    if view in ("front", "rear", "west", "east"):
        for m_ in [b for b in MB.bands()][:1]: row(view, "Betonbänder 0,30 m an den Geschossdecken", "z 3,20–3,50 und 6,20–6,50 umlaufend", "-", "Abweichung", "in Blatt 14 nicht gezeichnet; in Blatt 25, Blatt 4 (Balkonplatten) und Referenzbild ki_aussen vorhanden")
    # Plan -> Modell
    for i, (pt, r) in enumerate(plan):
        if i in used or r["fill"] in ("#FFFFFF",) and r["w"] > 120: continue
        if r["dash"] or (r["fill"] in ("#CFE0E8", "#FFFFFF") and r["w"] < 40):
            row(view, "Plan-Element ohne Modell", "-", fmt(pt), "Abweichung", "in Blatt 14, aber nicht im Modell")
out = os.path.join(ROOT, "visualisierungen", "higgsfield", "06_pruefpunkte_blatt14.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";"); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), "Prüfpunkte", dict(Counter(r["status"] for r in rows)))
for r in rows:
    if r["status"] != "bestätigt": print(r["ansicht"], "|", r["bauteil"], "|", r["status"], "|", r["hinweis"])
