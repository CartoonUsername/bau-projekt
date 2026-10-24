"""Unabhängiger Plan-Ist-Abgleich: Modell (scripts/modell_b3.py, Variante 'plangetreu') gegen die Ursprungsunterlage Blatt 14 (varianten_v2/14_Variante_B_Ansichten.svg = PDF-Seite 4 von Varianten_v2_ABC_Gesamt.pdf).
Blatt 14 entsteht aus einem anderen Skript (variants2_sheets.py) als Blatt 25, ist also kein Zirkelschluss. Jedes Rechteck der SVG wird in Meter (a = Koordinate entlang der Ansicht, z = Höhe) zurückgerechnet und gegen das Modell verglichen (Toleranz 3 cm).
Jede Zeile trägt die ID des Punkts der Plan-Ist-Prüfliste (06_plan_ist_pruefliste.*) und die Behandlung. Zusätzlich Zeilen für Elemente, die ein Rechtevergleich nicht sieht (Rahmenteilung, Belag, Dachaustritt, Höhe).
Ausgabe: visualisierungen/higgsfield/06_pruefpunkte_blatt14.csv (Modell v4); die Läufe gegen das alte Modell v3 stehen in 06_pruefpunkte_blatt14_modell_v3.csv."""
import re, os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
import modell_b3 as MB
ROOT = MB.ROOT; M = 4.0; DR = MB.Y1; TOL = 0.03
SVGF = "varianten_v2/14_Variante_B_Ansichten.svg"
S = open(os.path.join(ROOT, SVGF), encoding="utf-8").read()
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
def in_view(view, r):
    ox, gy, w, _, _ = VIEWS[view]; return ox - 8 <= r["x"] <= ox + w * M + 8 and gy - 50 <= r["y"] <= gy + 1 and r["w"] <= w * M + 2
def close(a, b): return all(abs(p - q) <= TOL for p, q in zip(a, b))
def pid(b):
    t = b
    for k, v in (("Rahmenteilung", "P6"), ("Betonbänd", "S9"), ("Brüstung Dachterrasse", "S7"), ("Kern-EG", "S1"), ("Kern-OG1", "S2"), ("Kern-Staffel", "S3"), ("Ost-Tür", "S4"), ("Ost-OG1", "S5"), ("Ost-Staffel", "S6"), ("EG-hinten", "P11"), ("Staffel-hinten", "P10"),
                 ("Abluft", "P14"), ("Dachaustritt", "P14"), ("Vordach", "P8"), ("OG1-Fenster", "P3"), ("Staffel-WE", "P4"), ("EG-Verglasung", "P5"), ("Doppeltür", "P7"), ("Tür Gastro", "P7"), ("Eingang Kern", "P7"), ("OG1-hinten", "P9"),
                 ("Baukörper", "P1"), ("Balkon", "P2"), ("Belag", "P13"), ("Höhe", "H1"), ("Plan-Element ohne Modell", "?")):
        if k in t: return v
    return "?"
BEHANDLUNG = {"S9": "als konzeptionelle Gestaltung gekennzeichnet (nicht abschließend planbestätigt)", "S7": "hinten bestätigt; seitlich als konzeptionelle Gestaltung gekennzeichnet", "P6": "Korrektur 1 umgesetzt: konzeptionelle Rahmenteilung ohne Rastermaß, gekennzeichnet",
              "S1": "Seitenfenster aus plangetreuer Fassung entfernt; nur als Gestaltungsvorschlag (offene Entscheidung)", "S2": "wie S1", "S3": "wie S1", "S5": "wie S1", "S6": "wie S1", "S4": "bestätigt", "P10": "Korrektur 2 umgesetzt (z 6,90–9,00)",
              "P11": "Korrektur 3 umgesetzt (dritte Tür entfernt, Bürozugang offen)", "P14": "Korrektur 5 umgesetzt: Stutzen entfernt, Dachaustritt offene Planungsentscheidung", "P8": "Korrektur 6: Vordach beibehalten, Konstruktion offen",
              "P13": "Korrektur 4 umgesetzt: neutral grau", "H1": "dokumentiert (07_gebaeudehoehe.md)"}
SRC = "B14 = " + SVGF + " (PDF Varianten_v2_ABC_Gesamt.pdf S. 4)"
rows = []
def row(view, bauteil, modell, plan, status, hinweis="", rect=None, quelle=None):
    i = pid(bauteil); beh = BEHANDLUNG.get(i, "bestätigt" if status == "bestätigt" else "offen")
    if status == "bestätigt" and i in ("S4",): beh = "bestätigt"
    rows.append(dict(ansicht=VIEWS[view][4] if view in VIEWS else view, bauteil=bauteil, modell_m=modell, blatt14_m=plan, status=status, hinweis=hinweis, pruefliste_id=i, behandlung=beh,
                     fundstelle=(f"B14 SVG-Rechteck x={rect['x']:.2f} y={rect['y']:.2f} b={rect['w']:.2f} h={rect['h']:.2f} (mm Blattkoordinaten)" if rect else (quelle or "B14 (kein Rechteck)"))))
fmt = lambda t: "a %.2f–%.2f / z %.2f–%.2f" % t if t else "-"
for view in VIEWS:
    plan = [(to_m(view, r), r) for r in RECT if in_view(view, r)]; used = set()
    def find(t):
        for i, (pt, r) in enumerate(plan):
            if close(pt, t): used.add(i); return pt, r
        return None, None
    for b in MB.boxes():
        t = (*(b["x"] if view in ("front", "rear") else b["y"]), b["z"][0], b["z"][1]); p, r = find(t)
        row(view, "Baukörper " + b["name"], fmt(t), fmt(p), "bestätigt" if p else "ungeklärt", "" if p else "Rechteck nicht gefunden", r)
    for o in MB.openings("plangetreu"):
        if o["side"] != VIEWS[view][3]: continue
        t = (o["a"][0], o["a"][1], *o["z"]); p, r = find(t)
        if p: row(view, f"Öffnung {o['tag']} ({o['kind']})", fmt(t), fmt(p), "bestätigt", "Lage bestätigt; Maße in B14 'schematisch/offen'" if o["kind"] == "glas" and "EG-V" not in o["tag"] else "", r)
        else: row(view, f"Öffnung {o['tag']} ({o['kind']})", fmt(t), "-", "Abweichung", "im Modell, aber nicht in Blatt 14")
    if view == "front":
        for b in MB.balconies():
            for nm, z in (("Balkonplatte", (3.2, 3.5)), ("Balkonbrüstung", (3.5, 4.6))):
                t = (b["x"][0], b["x"][1], *z); p, r = find(t); row(view, f"{nm} {b['name']}", fmt(t), fmt(p), "bestätigt" if p else "ungeklärt", "" if p else "Platte nicht als Rechteck gezeichnet", r)
        v = MB.vordach(); t = (v["x"][0], v["x"][1], *v["z"]); p, r = find(t); row(view, "Stahlvordach", fmt(t), fmt(p), "bestätigt" if p else "Abweichung", "24 m x 3,6 m, Unterkante +3,00 m; Konstruktion offen", r)
        rt = MB.rahmenteilung(); row(view, "Rahmenteilung EG-Verglasung (konzeptionell, %d Stege, ungleiche Abstände)" % len(rt["x"]), "x " + ", ".join(f"{x:.1f}" for x in rt["x"]), "-", "Abweichung", "Blatt 14 zeigt eine glatte Glasfläche; freigegeben als konzeptionelle Gestaltung ohne Rastermaß", None, "B14 (kein Rechteck)")
    if view == "rear":
        tt = MB.roof_terrace(); t = (tt["x"][0], tt["x"][1], 6.5, 7.6); p, r = find(t); row(view, "Brüstung Dachterrasse hinten", fmt(t), fmt(p), "bestätigt" if p else "ungeklärt", "", r)
        row(view, "Dachterrasse Belag", "neutral grau", "-", "ungeklärt", "Belag in keinem Plan festgelegt; Holz entfernt", None, "B13/B23/B14 (kein Belag angegeben)")
    if view in ("west", "east"):
        row(view, "Brüstung Dachterrasse seitlich", "y 18,7–21,0 / z 6,50–7,60", "-", "Abweichung", "Blatt 14 zeichnet keine seitliche Brüstung; Blatt 25 schon (konzeptionell)", None, "B14 (kein Rechteck), B25")
    if view == "east": row(view, "Dachaustritt Abluft (Stutzen)", "nicht gebaut", "nicht dargestellt", "bestätigt", "Blatt 14: 'Abluftführung über Dach (Austritt) ist nicht dargestellt' (C-22); Modell stimmt jetzt überein", None, "B14 Legende C-22")
    row(view, "Betonbänder 0,30 m an den Geschossdecken", "z 3,20–3,50 und 6,20–6,50 umlaufend", "-", "Abweichung", "in Blatt 14 nicht gezeichnet; in Blatt 25 und Referenzbild ki_aussen vorhanden", None, "B14 (kein Rechteck), B25, KI")
    for i, (pt, r) in enumerate(plan):
        if i in used or (r["fill"] == "#FFFFFF" and r["w"] > 120): continue
        if r["dash"] or (r["fill"] in ("#CFE0E8", "#FFFFFF") and r["w"] < 40): row(view, "Plan-Element ohne Modell", "-", fmt(pt), "Abweichung", "in Blatt 14, aber nicht im Modell", r)
hp = MB.hoehenpruefung()
rows.append(dict(ansicht="alle", bauteil="Höhe: Attika +9,90 m gegen zulässig 12,00 m, 3 Geschosse", modell_m=f"Attika {hp['attika_oberkante']:.2f}, Differenz {hp['differenz']:.2f} m", blatt14_m="B14 Kennzahl 'Höhe Attika 9,90 m'", status="bestätigt" if hp["eingehalten"] else "Abweichung",
                 hinweis="Zulässige Höhe 12,00 m laut Bestätigung des Auftraggebers; Bezugspunkt/Messregel unbestätigt (C-03)", pruefliste_id="H1", behandlung=BEHANDLUNG["H1"], fundstelle="B14 Kennzahlen; B14 Höhenkoten +3,50/+6,50/+9,60/+9,90"))
out = os.path.join(ROOT, "visualisierungen", "higgsfield", "06_pruefpunkte_blatt14.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";"); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), "Prüfpunkte", dict(Counter(r["status"] for r in rows)))
for r in rows:
    if r["status"] != "bestätigt": print(r["pruefliste_id"], "|", r["ansicht"], "|", r["bauteil"], "|", r["status"], "|", r["behandlung"])
