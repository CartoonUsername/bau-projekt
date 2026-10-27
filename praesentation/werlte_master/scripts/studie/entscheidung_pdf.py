"""Entscheidungs-PDF: zwei Planstände (B-Plan 123 rechtskräftig 2023 / 1. Änderung Entwurf 2026), Baufeld-3-Zuordnung, Grundstücksrisiken, Auswirkungen auf F1–F4 und Prüfgeometrien G1–G3.
KEINE Variante wird als baurechtlich zulässig bezeichnet. Maße: GESICHERT (im Plan genannt) / ABGELEITET (Vektorplan, Maßstabsabgriff) / GESCHÄTZT (aus Abbildung) – siehe quellen_stadt/planungsrecht_baufeld3.md."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from pdflib import *
import varianten as VA, parken as PK
ROOT = VA.ROOT; OUT = os.path.join(ROOT, "studie_gebaeudeformen"); SRC = os.path.join(ROOT, "quellen_stadt", "amtliche_unterlagen_sgwerlte")
TAG = "ENTSCHEIDUNGSGRUNDLAGE · NICHTS FESTGELEGT"
fm = lambda x, n=0: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
BF = (10.5, 3.4, 38.2, 19.3); PL = (0.0, 0.0, 42.3, 22.7); BFW, BFD = BF[2] - BF[0], BF[3] - BF[1]
C_OK, C_W, C_B = OK, WARN, BAD
def D(k): return VA.kennzahlen(k)
def dims(rects): b = VA.bbox(rects); return b[2] - b[0], b[3] - b[1]
def fits(w, d): return (w <= BFW + 0.05 and d <= BFD + 0.05) or (w <= BFD + 0.05 and d <= BFW + 0.05)
def pg(title, sub, n): im, d = page(); header(d, title, sub, TAG); footer(d, n); return im, d
# ---- Zeichnung Flurstück 59/1 ----
def plan_p59(w, h, keys=None, show_stalls=None, foot=None, title=None):
    im = Image.new("RGB", (w, h), "white"); d = ImageDraw.Draw(im); S = (w - 80) / 62.0; ox, oy = 40 + 9 * S, 90
    X = lambda x: int(ox + x * S); Y = lambda y: int(oy + (y + 7) * S)
    d.rectangle([X(-9), Y(-7), X(53), Y(0)], fill=(220, 222, 226)); d.text((X(-8), Y(-5.5)), "Planstraße (öffentlich, 16 m) – Norden", font=F(int(S * 0.9), "SemiBold"), fill=GREY)
    d.rectangle([X(-9), Y(0), X(0), Y(22.7)], fill=(236, 238, 242)); d.text((X(-8.7), Y(8)), "Markt-\nstraße", font=F(int(S * 0.8)), fill=GREY)
    d.rectangle([X(0), Y(0), X(42.3), Y(22.7)], fill=(222, 235, 190), outline=INK, width=4)
    # nicht überbaubare Streifen
    d.rectangle([X(BF[0]), Y(BF[1]), X(BF[2]), Y(BF[3])], fill=(255, 250, 235))
    def dash(box, col, wd=4):
        x0, y0, x1, y1 = box
        for i in range(int(x0), int(x1), 24): d.line([(i, y0), (min(i + 12, x1), y0)], fill=col, width=wd); d.line([(i, y1), (min(i + 12, x1), y1)], fill=col, width=wd)
        for j in range(int(y0), int(y1), 24): d.line([(x0, j), (x0, min(j + 12, y1))], fill=col, width=wd); d.line([(x1, j), (x1, min(j + 12, y1))], fill=col, width=wd)
    dash((X(BF[0]), Y(BF[1]), X(BF[2]), Y(BF[3])), (255, 140, 0), 5); d.text((X(BF[0]) + 8, Y(BF[1]) + 6), f"Baufenster P23 ≈ {BFW:.1f} × {BFD:.1f} m (abgeleitet)", font=F(int(S * 0.85), "SemiBold"), fill=(200, 100, 0))
    d.text((X(0.5), Y(22.7) + 8), "Flurstück 59/1 ≈ 42,3 × 22,7 m ≈ 960 m² (geschätzt)", font=F(int(S * 0.85), "SemiBold"), fill=INK)
    d.text((X(0.5), Y(1.0)), "10,0 m nicht überbaubar (Baumreihe)", font=F(int(S * 0.7)), fill=GREY)
    if foot:
        for lab, (x0, y0, x1, y1), col in foot: dash((X(x0), Y(y0), X(x1), Y(y1)), col, 5); d.text((X(x0) + 8, Y(y1) - int(S * 1.5)), lab, font=F(int(S * 0.8), "SemiBold"), fill=col)
    if keys:
        for k in keys:
            v = VA.V[k]
            for r in v["og1"]: dash((X(r[0]), Y(r[1]), X(r[2]), Y(r[3])), (170, 110, 80), 3)
            for r in v["eg"]: d.rectangle([X(r[0]), Y(r[1]), X(r[2]), Y(r[3])], fill=(238, 232, 226), outline=INK, width=4)
            fg = v.get("fahrgasse")
            if fg and fg[2] - fg[0] > 1: d.rectangle([X(fg[0]), Y(fg[1]), X(fg[2]), Y(fg[3])], fill=(226, 229, 234)); d.text((X(fg[0]) + 6, Y(fg[1]) + 10), "Fahrgasse 6 m", font=F(int(S * 0.7), "SemiBold"), fill=GREY)
            for r in v["eg"]: d.rectangle([X(r[0]), Y(r[1]), X(r[2]), Y(r[3])], outline=INK, width=4)
            d.text((X(v["eg"][0][0]) + 8, Y(v["eg"][0][1]) + 6), f"EG {VA.rects_area(v['eg']):.0f} m²", font=F(int(S * 0.9), "SemiBold"), fill=INK)
            if v.get("stalls_row1"):
                pk = PK.pruefe(k); col = {"voll": (214, 238, 218), "eingeschraenkt": (253, 236, 200), "konflikt": (250, 205, 205)}
                for s in pk["stalls"]: r = s["rect"]; d.rectangle([X(r[0]), Y(r[1]), X(r[2]), Y(r[3])], fill=col[s["status"]], outline=(110, 116, 126), width=2); d.rounded_rectangle([X(r[0] + 0.3), Y(r[1] + 0.25), X(r[2] - 0.3), Y(r[3] - 0.25)], radius=5, fill=(170, 176, 188)); d.text((X(r[0]) + 4, Y(r[1]) + 2), str(s["nr"]), font=F(int(S * 0.6), "SemiBold"), fill=INK)
            for (x, y) in v["saeulen_pts"]: d.ellipse([X(x) - 5, Y(y) - 5, X(x) + 5, Y(y) + 5], fill=(30, 30, 30))
    if title: d.text((40, 20), title, font=F(34, "SemiBold"), fill=INK)
    return im
# ---- Seiten ----
def p_fazit(n):
    im, d = pg("Entscheidungsgrundlage Variante F: zwei Planstände", "B-Plan Nr. 123 „Ehemalige Grundschule“ – rechtskräftig 2023 und 1. Änderung als Entwurf 2026 · Stand 24.10.2026", n)
    t = ("1. Es gibt ZWEI Planstände: den rechtskräftigen Plan (in Kraft seit 14.04.2023, Planunterlage Stand 08.06.2022) und den Entwurf der 1. Änderung (Planzeichnung 25.08.2026, Begründung 25.09.2026, noch ohne Satzungsbeschluss). Beide liegen vor (quellen_stadt/amtliche_unterlagen_sgwerlte/).\n\n"
         "2. Die Aussage der städtischen Seite 13 („mindestens zwei, höchstens drei Geschosse“) ist am Originalplan BESTÄTIGT – aber nur für MI 1 und MI 3 (Z = II–III). Für MI 2 gilt II zwingend. Dort (und im Entwurf 2026) steht die „12,00 m“; für MI 1/MI 3 gilt H = 15,00 m, TH = 9,80 m.\n\n"
         "3. Welches Grundstück Baufeld 3 ist: sehr wahrscheinlich MI 3 / Flurstück 59/1 südlich der Planstraße (≈ 960 m², Z II–III). Das ist ein Indizienschluss; Seite 13 fehlt, die Fotos-ZIP ist nicht angekommen. Die 1. Änderung betrifft MI 3 NICHT – für Baufeld 3 gilt dann ausschließlich der Plan von 2023.\n\n"
         "4. Der Originalplan enthält Festsetzungen, die alle bisherigen Varianten (B3, B, C, D, E, F) betreffen: Hauptdächer geneigt ≥ 38° (Flachdach nur für Verbindungsbauten/≤ 70 m²), Traufhöhe ≤ 9,80 m, Baugrenze 10,0 m West / 3 m übrige Seiten. Das Baufenster von MI 3 misst ≈ 27,7 × 15,9 m (≈ 439 m², abgeleitet) – EG 540 m² und umlaufender Vorbau über die Baugrenze passen dort nicht.\n\n"
         "5. Keine Variante darf als baurechtlich zulässig bezeichnet werden, bevor Baufeld 3, amtliche Grundstücksgrenzen und die Frage von Befreiungen (Dach, Baugrenze) geklärt sind.")
    text_block(d, 120, 300, 3260, t, 34); return im
def p_staende(n):
    im, d = pg("Die zwei Planstände im Vergleich", "Fundstellen: Planzeichnung und textliche Festsetzungen (P23 / E26), Begründung 3.2–3.3", n)
    rows = [["Merkmal", "P23 MI 3 (und MI 1) – RECHTSKRÄFTIG 2023", "P23 MI 2 – rechtskräftig 2023", "E26 – 1. Änderung ENTWURF 2026"],
      ["Rechtsstand", "in Kraft seit 14.04.2023", "in Kraft seit 14.04.2023", "Entwurf, kein Satzungsbeschluss"],
      ["Geltungsbereich", "ganzes Plangebiet (1,27 ha), MI 3 = Flurstück 59/1", "östlicher Block", "ca. 3.874 m²; MI 3 liegt NICHT darin"],
      ["Gebietsart / GRZ", "Mischgebiet / 0,6", "Mischgebiet / 0,6", "Mischgebiet / 0,6"], ["Vollgeschosse", "II–III (Mindest-/Höchstmaß)", "II zwingend", "II zwingend"],
      ["Traufhöhe TH", "max. 9,80 m", "max. 6,50 m", "max. 6,50 m"], ["Gebäudehöhe H", "max. 15,00 m", "max. 12,00 m", "max. 12,00 m"], ["Sockelhöhe SH", "FFB EG ≤ 0,30 m über Bezugspunkt", "wie MI 3", "wie P23"],
      ["Bezugspunkt", "OK Fahrbahn der nächsten ausgebauten Erschließungsstraße, Mitte vor dem Baukörper; oben: OK Baukörper (First/Hauptgesims)", "wie MI 3", "wie P23"],
      ["Dachform", "Hauptdächer geneigt ≥ 38°; Flachdach nur Verbindungsbauten (≥ 1,0 m unter First), Wintergärten/untergeordnete Dachflächen ≤ 70 m²", "wie MI 3", "wie P23 (örtl. Bauvorschrift)"],
      ["Bauweise", "offen (bis 50 m)", "offen", "offen"], ["Baugrenzen (MI 3)", "10,0 m zur Marktstraße (W); 3 m Planstraße (N), 3 m Ost, 3 m Süd", "an Baumstandorte orientiert", "3,0 m zu Planstraße und Parkplatz"],
      ["Stellplätze/Nebenanlagen", "Garagen/Gebäude-Nebenanlagen entlang öffentl. Verkehrsflächen unzulässig; Baumreihe Marktstraße: Kronentraufbereich ohne Versiegelung", "wie MI 3", "öffentlicher Parkplatz 63 Plätze; Überdachung von Stellplätzen dort unzulässig"],
      ["Fassade", "Ziegelsichtmauerwerk nicht glasiert (Rot/Rotbraun), andere Materialien ≤ 1/2", "wie MI 3", "wie P23"]]
    table(d, 120, 290, [560, 1160, 740, 800], rows, 25); return im
def p_zuordnung(n):
    im, d = pg("Welches Grundstück ist Baufeld 3? (Indizien, UNBESTÄTIGT)", "Ausschnitt rechtskräftiger Plan 2023 (links) und Nutzungskonzept 2026 (rechts, Markierung = vermutete Lage)", n)
    a = Image.open(os.path.join(SRC, "Ausschnitt_MI3_Flurstueck_59-1_BPlan123_2023-01.png")).convert("RGB"); tmp = os.path.join(OUT, "_a.png"); a.save(tmp); paste(im, tmp, 120, 290, 1100, 880); os.remove(tmp)
    b = Image.open(os.path.join(SRC, "Abb3_Nutzungskonzept_BPlan123_1Aend.jpg")).convert("RGB"); dd = ImageDraw.Draw(b); dd.rectangle([13, 561, 244, 689], outline=(0, 90, 255), width=6); dd.text((20, 530), "Baufeld 3? (MI 3)", font=F(34, "SemiBold"), fill=(0, 90, 255)); tmp = os.path.join(OUT, "_b.png"); b.save(tmp); paste(im, tmp, 1280, 290, 800, 1130); os.remove(tmp)
    rows = [["Indiz", "Befund"], ["Fläche", "Flurstück 59/1 ≈ 960 m² (aus Planabbildung abgegriffen, ±3 %) = Projektangabe ca. 960 m²"], ["Geschosse", "MI 3: II–III = städtische Seite 13 „mindestens zwei, höchstens drei“ (MI 2: II zwingend – passt nicht)"], ["Plan 2026", "Änderungsbereich enthält MI 3 nicht → die „12,00 m“ der Seite 15 gelten für Baufeld 3 nicht"], ["Gegenindiz", "MI 1 hat ebenfalls II–III, H 15 m; die Baufeldnummern stehen in den geladenen Unterlagen nicht; Seite 13 fehlt"], ["Folge", "Bestätigung durch den Auftraggeber nötig (Foto Seite 13 / Baufeldplan)"]]
    table(d, 2150, 300, [320, 1000], rows, 24); return im
def p_massrisiko(n):
    im, d = pg("Grundstücksmaße und Risiken: gesichert, abgeleitet, geschätzt", "Keine verbindlichen Grundstücksmaße aus einer abgebildeten/fotografierten Plankarte – amtlicher Lageplan erforderlich", n)
    rows = [["Angabe", "Wert", "Status", "Herkunft / Risiko"],
      ["Baugrenzabstände MI 3", "10,0 m W; 3 m N/O/S", "GESICHERT (im Plan bemaßt)", "Planzeichnung P23"], ["Planstraße", "16,0 m Querschnitt", "GESICHERT", "Begründung 3.3"], ["Höhen, Z, GRZ, Dach, Bezugspunkt", "siehe Planstände", "GESICHERT (P23 rechtskräftig)", "Textliche Festsetzungen 1.2, 2.2"],
      ["Baufenster MI 3", "≈ 27,7 × 15,9 m = 439 m²", "ABGELEITET (Vektorplan 1:1000)", "Polygon aus der PDF-Geometrie; Plan leicht gegen Nord gedreht; nicht vermessen"],
      ["Flurstück 59/1", "≈ 42,3 × 22,7 m ≈ 960 m²", "GESCHÄTZT (±3 %)", "aus der Planabbildung gemessen; Grenzen nur grafisch (Liegenschaftskarte Stand 08.06.2022)"],
      ["Fahrbahnhöhe (Bezugspunkt)", "unbekannt", "FEHLT", "Bauamt der Stadt Werlte (laut Festsetzung 1.2 erfragbar)"], ["Amtlicher Lageplan / Vermessung", "–", "FEHLT", "ÖbVI Dipl.-Ing. Jörg Jüngerink (Plan-Az. 22-7003); Gebäude in der Nutzung ist Stand 2022"],
      ["Baumreihe Marktstraße", "Kronen-/Wurzelschutz", "GESICHERT (Festsetzung)", "schränkt Stellplätze/Zufahrt im Westen ein; Kronendurchmesser unbekannt"], ["Zufahrt/Ausfahrt zur Planstraße", "–", "ANNAHME", "Lage, Sichtdreiecke, Gehwege (16 m Querschnitt) ungeklärt"]]
    cl = {(i, 2): (OK if r[2].startswith("GESICHERT") else (WARN if r[2].startswith(("ABGELEITET", "GESCHÄTZT", "ANNAHME")) else BAD)) for i, r in enumerate(rows) if i}
    table(d, 120, 290, [820, 700, 620, 1120], rows, 26, colors=cl); return im
def p_fussabdruck(n):
    im, d = pg("Lageplan Flurstück 59/1: Baufenster und Fußabdrücke der Varianten", "Alle EG-Fußabdrücke aus F, E, B3 passen NICHT in das Baufenster · Umrisse an der Baufensterecke ausgerichtet · Maße abgeleitet/geschätzt", n)
    foot = [("B3 32×18", (BF[0], BF[1], BF[0] + 32, BF[1] + 18), (180, 30, 30)), ("F4 30×18", (BF[0], BF[1], BF[0] + 30, BF[1] + 18), (30, 90, 200)), ("E1–E3 27×17,5", (BF[0], BF[1], BF[0] + 27, BF[1] + 17.5), (30, 140, 90)), ("F1–F3 18×30 (30 tief)", (BF[0] + 4, 0.8, BF[0] + 22, 22.7), (140, 60, 160))]
    im2 = plan_p59(2300, 1900, foot=foot); im.paste(im2, (120, 280))
    rows = [["EG-Fußabdruck", "Baufenster 27,7 × 15,9"]] + [[lab, ("passt" if fits(*dims([r])) else "passt NICHT")] for lab, r in (("B3 / A–D: 32 × 18 m", (0, 0, 32, 18)), ("E1–E3: 27 × 17,5 m", (0, 0, 27, 17.5)), ("E4: 27 × 12,5 m", (0, 0, 27, 12.5)), ("F1–F3: 18 × 30 m", (0, 0, 18, 30)), ("F4: 30 × 18 m", (0, 0, 30, 18)), ("G1: 27,7 × 15,9 m", (0, 0, 27.7, 15.9)))]
    cl = {(i, 1): (OK if r[1] == "passt" else BAD) for i, r in enumerate(rows) if i}
    y = table(d, 2480, 300, [520, 380], rows, 24, colors=cl)
    text_block(d, 2480, y + 40, 900, "Zusätzlich: EG 540 m² übersteigt das Baufenster (439 m²) um 101 m² (+23 %). Die GRZ 0,6 erlaubt rechnerisch 576 m² Grundfläche – begrenzend wirkt die Baugrenze. Ein Vorbau über die Baugrenze hinaus ist unzulässig; ein umlaufender Vorbau müsste innerhalb des Baufensters bleiben.", 25, GREY); return im
def p_geometrien(n):
    im, d = pg("Prüfgeometrien G1–G3 auf Flurstück 59/1 (keine Festlegung)", "G1 volles Baufenster · G2 kleineres EG + Vorbau im Baufenster + Stellplätze Ost · G3 EG 540 m² nur mit Befreiung", n)
    w = (W - 240 - 2 * 40) // 3
    for i, k in enumerate(("G1", "G2", "G3")):
        pim = plan_p59(w, 880, keys=[k]); x = 120 + i * (w + 40); d.text((x, 270), VA.V[k]["name"], font=F(28, "SemiBold"), fill=INK); im.paste(pim, (x, 320))
    ks = ["G1", "G2", "G3"]; rows = [["Kennzahl"] + ks, ["EG (m²)"] + [fm(D(k)["flaeche"]["eg"]) for k in ks], ["1. OG / 2. OG (m²)"] + [f"{fm(D(k)['flaeche']['og1'])} / {fm(D(k)['flaeche']['st'])}" for k in ks], ["Wohnfläche netto (m²)"] + [fm(D(k)["wfl"]) for k in ks],
        ["Wohnungen (Größen m²)"] + [f"{D(k)['mix']['standard']['we']} ({fm(D(k)['mix']['standard']['kleinste'])}–{fm(D(k)['mix']['standard']['groesste'])})" for k in ks], ["Gastraum ≈ Plätze innen"] + [f"{fm(VA.V[k]['gastro_m2'])} m² ≈ {D(k)['stp']['sitze_innen']}" for k in ks],
        ["Stellplätze nutzbar (gezeichnet)"] + [str(PK.pruefe(k)["nutzbar"]) if VA.V[k]["stalls_row1"] else "0" for k in ks], ["erforderlich Gastro+Büro (Spanne)"] + [f"{fm(D(k)['stp']['erf_lo'],1)}–{fm(D(k)['stp']['erf_hi'],1)}" for k in ks],
        ["liegt im Baufenster?"] + ["ja", "ja (OG), EG innen", "NEIN – Befreiung"], ["Dach (≥ 38° Pflicht)", "Flachdach: Befreiung nötig", "Flachdach: Befreiung nötig", "Flachdach: Befreiung nötig"]]
    table(d, 120, 1300, [700, 900, 900, 900], rows, 26)
    text_block(d, 120, 2050, 3200, "Lesart: Auf dem echten Zuschnitt lässt sich nur eine kleine Stellplatzreihe unterbringen (G2: 5 Plätze), und nur mit kleinerem Gewerbe-EG. Wohnfläche und EG 540 m² schließen sich gegenseitig mit Stellplätzen aus. Alle Zahlen sind Prüfskizzen auf geschätztem Zuschnitt.", 26, GREY); return im
def status(k):
    d = D(k); v = VA.V[k]; eg_w, eg_d = dims(v["eg"]); og_w, og_d = dims(v["og1"]); att = d["hoehe"]["attika"]; ov = max(0, VA.rects_area(v["og1"]) - 0)  # Platzhalter
    st = d["staffel_anteil"]
    A = {}; B = {}
    A["EG im Baufenster"] = ("kritisch", "nein") if not fits(eg_w, eg_d) else ("ok", "ja")
    A["Vorbau/OG im Baufenster"] = ("kritisch", "nein (Baugrenze)") if not fits(og_w, og_d) else ("ok", "ja")
    B["EG im Baufenster"] = A["EG im Baufenster"]; B["Vorbau/OG im Baufenster"] = A["Vorbau/OG im Baufenster"]
    if k.startswith(("E", "F")):
        A["Höhe"] = ("pruef", f"+{att:.2f} m über FFB (+≤0,30 SH) ≤ 15,00 m: ok, aber TH 9,80 m überschritten (Wand +11,5 m)")
        B["Höhe"] = ("kritisch", f"+{att:.2f} m über FFB; H 12,00 m über OK Fahrbahn → bei SH > 0 überschritten; TH 6,50 m überschritten")
    else:
        A["Höhe"] = ("pruef", f"+{att:.2f} m: ok gegen 15,00 m; TH 9,80 m prüfen"); B["Höhe"] = ("pruef", f"+{att:.2f} m: ok gegen 12,00 m; TH 6,50 m überschritten")
    A["Vollgeschosse"] = ("ok", "3 Geschosse = II–III zulässig (Staffelanteil %.0f %%)" % (st * 100)); B["Vollgeschosse"] = ("kritisch", "II zwingend – drei Vollgeschosse unzulässig; Staffel < 2/3 (%.0f %%) nur ggf. kein Vollgeschoss" % (st * 100) if st < 2 / 3 else "II zwingend – drei Vollgeschosse unzulässig")
    A["Dachform"] = ("kritisch", "Flachdach: Hauptdach ≥ 38° vorgeschrieben (Befreiung)"); B["Dachform"] = A["Dachform"]
    g = d["projektion_m2"]; A["GRZ 0,6"] = ("pruef", f"EG {VA.rects_area(v['eg']):.0f} m² ≤ 576; größte Projektion {g:.0f} m²"); B["GRZ 0,6"] = A["GRZ 0,6"]
    A["Stellplätze"] = ("pruef", "auf 32×30-Hypothese gerechnet, nicht auf 59/1 übertragbar") if k.startswith(("E", "F")) else ("pruef", "siehe G-Skizzen"); B["Stellplätze"] = A["Stellplätze"]
    return A, B
def p_auswirkung(n):
    im, d = pg("Auswirkungen auf F1–F4 nach Planstand A und B", "A = rechtskräftig 2023 (MI 3), B = Entwurf 2026 hypothetisch auf Baufeld 3 angewandt · grün = voraussichtlich ok, orange = prüfen, rot = widerspricht · kein Ergebnis bedeutet Zulässigkeit", n)
    COL = {"ok": OK, "pruef": WARN, "kritisch": BAD}; keys = ["F1", "F2", "F3", "F4"]
    crit = ["EG im Baufenster", "Vorbau/OG im Baufenster", "Höhe", "Vollgeschosse", "Dachform", "GRZ 0,6", "Stellplätze"]
    for bi, (lab, idx) in enumerate((("PLANSTAND A – P23 rechtskräftig 2023, MI 3: II–III, TH 9,80, H 15,00, Dach ≥ 38°", 0), ("PLANSTAND B – E26 Entwurf 2026 (für Baufeld 3 NICHT einschlägig, hypothetisch): II zwingend, TH 6,50, H 12,00, Dach ≥ 38°", 1))):
        rows = [["Kriterium"] + keys]; cl = {}
        for ci, c in enumerate(crit, 1):
            row = [c]
            for kj, k in enumerate(keys, 1): s = status(k)[idx][c]; row.append(s[1]); cl[(ci, kj)] = COL[s[0]]
            rows.append(row)
        d.text((120, 280 + bi * 1000), lab, font=F(30, "SemiBold"), fill=INK); table(d, 120, 330 + bi * 1000, [520] + [(3268 - 520) // 4] * 4, rows, 22, colors=cl)
    return im
def p_offen(n):
    im, d = pg("Entscheidungsfragen und fehlende Unterlagen", "Bevor die Rechtslage geklärt ist, wird keine Variante als zulässig bezeichnet und kein Modell überschrieben", n)
    t = ("Fehlt/anzufordern:\n• Foto Seite 13 (oder Baufeldplan der Stadt), um MI 3 / Flurstück 59/1 als Baufeld 3 zu bestätigen; die Fotos der Seiten 13/15/16 sind nicht angekommen.\n• Maßstäblicher Originalplan bzw. amtlicher Lageplan/Vermessung des Flurstücks 59/1 (keine verbindlichen Maße aus der Planabbildung).\n• Fahrbahnhöhe der Planstraße vor dem Baukörper (Bauamt) für den Höhenbezug.\n• Auskunft der Stadt: Befreiung von (a) Dachform (≥ 38°), (b) Baugrenzen/Baufenster, (c) Traufhöhe 9,80 m für ein Flachdach-/Staffelkonzept; Stellplatzregelung (städtebaulicher Vertrag/Kaufvertrag), Mitnutzung des öffentlichen Parkplatzes (63 Plätze) für Gastro/Büro; Rechtsstand und Zeitplan der 1. Änderung (Entwurf).\n\n"
         "Entscheidungen für den Auftraggeber:\n• Soll Baufeld 3 als MI 3 angenommen werden? (Dann gelten 15 m/II–III/TH 9,80 m, aber Baufenster ≈ 439 m².)\n• Soll das Konzept an die Festsetzungen angepasst werden (geneigtes Dach ≥ 38°, Baufenster) oder eine Befreiung/Planänderung beantragt werden?\n• Soll EG 540 m² mit Befreiung weiterverfolgt oder auf das Baufenster (G1/G2) reduziert werden?\n\n"
         "Nicht geändert: B3 und alle bestehenden Modelle; keine Variante ist ausgewählt.")
    text_block(d, 120, 300, 3260, t, 33); return im
def baue():
    fs = [p_fazit, p_staende, p_zuordnung, p_massrisiko, p_fussabdruck, p_geometrien, p_auswirkung, p_offen]
    pages = [f(i + 1) for i, f in enumerate(fs)]; p = os.path.join(OUT, "Entscheidung_Planstaende_Baufeld3_Variante_F.pdf"); save(pages, p); return p
if __name__ == "__main__": print(baue())
