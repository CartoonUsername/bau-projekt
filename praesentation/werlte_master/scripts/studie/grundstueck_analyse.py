"""Grundstücks- und Planungsrechtsanalyse Baufeld 3 aus den amtlichen Unterlagen der Stadt Werlte (B-Plan 123, 1. Änderung, Entwurf 25.09.2026; B-Plan 122 Entwurf).
GESICHERT = amtlicher Text/Maßzahl in den Unterlagen. ABGELEITET = aus der Abbildung (Nutzungskonzept M 1:1000) abgegriffen, Genauigkeit ca. ±2 m. ANNAHME/UNBEKANNT = nicht in den Unterlagen.
Ausgabe: studie_gebaeudeformen/Grundstuecksanalyse_Baufeld3.pdf; seiten() liefert die Seiten auch für das Vergleichs-PDF."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from pdflib import *
import varianten as VA
ROOT = VA.ROOT; OUT = os.path.join(ROOT, "studie_gebaeudeformen"); SRC = os.path.join(ROOT, "quellen_stadt", "amtliche_unterlagen_sgwerlte")
TAG = "GRUNDSTÜCK · TEILWEISE ABGELEITET"
GRN = OK; ORG = WARN
# Kandidaten (Näherung aus Abb. 3): Rechteck-Näherungen in m, Ursprung SW-Ecke, x Ost, y Nord; Planstraße im Süden (y < 0), öffentlicher Parkplatz im Norden (y > D)
KAND = {"K1": dict(name="Kandidat K1 „Mitte“ (Baufeld zwischen Stichstraße und Fuß-/Radweg)", b=33.0, d=25.0), "K2": dict(name="Kandidat K2 „Ost“ (Trapez, Rechteck-Näherung)", b=35.0, d=27.0)}
ABST = 3.0  # Baugrenzabstand zu Planstraße und Parkplatz (Begründung 3.3, gesichert); W/O ebenfalls 3,0 m ANGENOMMEN
def baufenster(k): c = KAND[k]; return (c["b"] - 2 * ABST, c["d"] - 2 * ABST)
FOOT = [("B3 / A, B, C, D: EG 32 × 18 m", 32.0, 18.0), ("E1–E3: EG 27 × 17,5 m", 27.0, 17.5), ("E4: EG 27 × 12,5 m", 27.0, 12.5), ("F1–F3: EG 18 × 30 m (30 m tief)", 18.0, 30.0), ("F4: EG 30 × 18 m", 30.0, 18.0), ("Nutzungskonzept (Abb. 3): ca. 26 × 11,5 m", 26.0, 11.5)]
def passt(bw, bd, w, dd): return w <= bw + 0.01 and dd <= bd + 0.01
def p_title(n):
    im, d = page(); header(d, "Grundstück Baufeld 3: Quellen, Planungsrecht, Zuschnitt", "Auswertung der amtlichen Unterlagen der Stadt Werlte · Stand 24.10.2026", TAG); footer(d, n)
    t = ("Wichtig vorab: Die ZIP-Datei mit den Fotos der Seiten 13/15/16 ist in dieser Sitzung nicht angekommen (kein Anhang, Upload-Ordner leer, nichts im Repository). Der Ordner fotos_stadt_unterlagen/ ist leer.\n\n"
         "Stattdessen habe ich die amtlichen Planunterlagen von der Website der Samtgemeinde Werlte geladen: B-Plan Nr. 123 „Ehemalige Grundschule“, 1. Änderung (Entwurf 25.09.2026, mit Begründung, Planzeichnung, Nutzungskonzept, Schallgutachten) und B-Plan Nr. 122 „Neue Mitte“ (Entwurf, Offenlage 02.10.–02.11.2026). Sie liegen in quellen_stadt/amtliche_unterlagen_sgwerlte/.\n\n"
         "Kernergebnisse:\n• Die 12,00 m sind NUR im Entwurf der 1. Änderung festgesetzt (H = 12,00 m); Rechtskraft liegt nur für den Ursprungsplan 123 vor (14.04.2023), dessen Text nicht vorliegt.\n• Bezugspunkt: Oberkante Fahrbahn der nächstgelegenen ausgebauten Erschließungsstraße in der Mitte vor dem Baukörper; EG-Fußboden max. 0,30 m darüber. Bei SH 0,30 m bleiben nur +11,70 m über FFB; die in E/F gezeichneten +12,00 m über FFB sind zu hoch bzw. nicht nachgewiesen.\n• Im Entwurf gilt für den Änderungsbereich: Mischgebiet, GRZ 0,6, zwingend zwei Vollgeschosse, Traufhöhe 6,50 m, geneigtes Dach mind. 38°, Baugrenze 3,0 m zu Planstraße und Parkplatz. Das passt nicht zu dreigeschossigen Flachdachbauten mit Vorbau über die Baugrenze.\n• Welches Baufeld „Baufeld 3“ ist, lässt sich ohne Seite 13 nicht sicher bestimmen. Aus dem Nutzungskonzept habe ich zwei Kandidaten abgegriffen (ca. 33 × 25 m und 35 × 27 m, Näherung ±2 m). Auf beiden passt weder B3 (EG 32 × 18 m) noch F (540 m²) in das Baufenster.")
    text_block(d, 120, 300, 3260, t, 33); return im
def p_status(n):
    im, d = page(); header(d, "Gesicherte Maße, Ableitungen, Annahmen", "Trennung nach Herkunft", TAG); footer(d, n)
    rows = [["Angabe", "Wert", "Status", "Fundstelle / Bemerkung"],
        ["Plangebiet 1. Änderung", "ca. 3.874 m² (0,39 ha)", "GESICHERT", "Begründung Nr. 1; Bekanntmachung 24.09.2026"], ["Baugrenze zu Planstraße und Parkplatz", "3,0 m", "GESICHERT", "Begründung Nr. 3.3"], ["Planstraße Querschnitt", "16,0 m", "GESICHERT", "Begründung Nr. 3.3; Abb. 2 (15,8 m)"],
        ["Parkplatz öffentlich", "63 Einstellplätze", "GESICHERT", "Begründung 2.5, Schallgutachten (Nutzungskonzept)"], ["Höhen (SH 0,30 / TH 6,50 / H 12,00 m), II zwingend, GRZ 0,6, MI", "siehe Planzeichnung", "GESICHERT (Entwurf)", "Planzeichnung, Textliche Festsetzungen 1.2; nicht rechtskräftig"],
        ["Flurstücks- und Baufeldgrenzen der Baufelder", "nicht dargestellt", "UNBEKANNT", "Abb. 3 zeigt keine Grundstücksgrenzen, nur Nutzungen"], ["Kandidat K1: 33 × 25 m (≈ 830 m²)", "Näherung", "ABGELEITET (±2 m)", "aus Abb. 3, Maßstab 1:1000, Straßen-/Wegkanten"], ["Kandidat K2: 35 × 27 m (≈ 900 m²)", "Näherung", "ABGELEITET (±2 m)", "wie oben; Trapezform vereinfacht"],
        ["Fläche Baufeld 3 ≈ 960 m²", "ca. 960 m²", "Projektangabe, nicht am Plan belegt", "weder K1 (−12 %) noch K2 (−6 %) deckungsgleich"], ["Baufenster W/O (Abstand 3 m)", "27 × 19 m (K1)", "ANNAHME", "nur N/S aus Begründung; Ost/West nicht belegt"], ["Ursprungsplan 123 (rechtskräftig seit 14.04.2023)", "–", "UNBEKANNT", "Text/Plan liegt nicht vor; „2–3 Geschosse“ (Seite 13) ungeprüft"], ["Lage der Platzseite / Zufahrt", "–", "UNBEKANNT", "Planstraße im Süden, Parkplatz im Norden der Kandidaten; Zufahrt Annahme"]]
    cl = {(i, 2): (OK if r[2].startswith("GESICHERT") else (WARN if r[2].startswith("ABGELEITET") or "Projekt" in r[2] or r[2].startswith("ANNAHME") else BAD)) for i, r in enumerate(rows) if i}
    table(d, 120, 290, [1050, 650, 560, 1000], rows, 26, colors=cl); return im
def p_recht(n):
    im, d = page(); header(d, "Planungsrecht: Höhe 12,00 m und ihr Bezugspunkt", "B-Plan Nr. 123, 1. Änderung, Entwurf (Textliche Festsetzung 1.2) · Antwort auf: verbindlich festgesetzt? von wo gemessen?", TAG); footer(d, n)
    # Schema
    base, sc = 2050, 120; x0 = 220
    d.line([(x0 - 100, base), (x0 + 900, base)], fill=INK, width=4); d.text((x0 - 100, base + 12), "OK Fahrbahn der nächstgelegenen Erschließungsstraße (unterer Bezugspunkt, ±0,00)", font=F(26), fill=INK)
    def box(z0, z1, lab, fill):
        d.rectangle([x0 + 300, base - z1 * sc, x0 + 760, base - z0 * sc], fill=fill, outline=INK, width=3); d.text((x0 + 315, base - (z0 + z1) / 2 * sc - 14), lab, font=F(24), fill=INK)
    box(0.0, 0.30, "", (200, 200, 205)); box(0.30, 4.6, "EG (FFB = +0,30 = SH max.)", (245, 245, 245)); box(4.6, 8.2, "1. OG", (252, 240, 232)); box(8.2, 11.4, "2. OG / Dachgeschoss", (252, 246, 236)); box(11.4, 11.7, "Attika", (130, 130, 135))
    d.line([(x0 + 100, base - 12 * sc), (x0 + 900, base - 12 * sc)], fill=GRN, width=5); d.text((x0 + 100, base - 12 * sc - 40), "H = 12,00 m (max., Entwurf)", font=F(28, "SemiBold"), fill=GRN)
    d.line([(x0 + 100, base - 6.5 * sc), (x0 + 900, base - 6.5 * sc)], fill=BAD, width=5); d.text((x0 + 770, base - 6.5 * sc - 36), "TH 6,50 m", font=F(26, "SemiBold"), fill=BAD)
    d.line([(x0 + 100, base - 0.3 * sc), (x0 + 300, base - 0.3 * sc)], fill=INK, width=2); d.text((x0 - 50, base - 0.3 * sc - 34), "SH max. 0,30 m", font=F(24), fill=INK)
    d.text((x0 + 100, base - 11.7 * sc - 40), "+11,70 m über FFB bei SH 0,30 m", font=F(24), fill=WARN)
    rows = [["Frage", "Antwort"], ["Ist 12 m verbindlich festgesetzt?", "Im ENTWURF der 1. Änderung (H = 12,00 m). Satzungsbeschluss steht aus; der rechtskräftige Ursprungsplan 123 (14.04.2023) liegt nicht vor. → Nicht als verbindlich nachgewiesen."],
        ["Von wo gemessen?", "Unterer Bezugspunkt: Oberkante Fahrbahn der nächstgelegenen ausgebauten Erschließungsstraße in der Mitte vor dem Baukörper (Höhe beim Bauamt erfragbar). Oberer Punkt: Oberkante Baukörper (First, Hauptgesims); untergeordnete Teile (Antennen, Schornsteine) zählen nicht."],
        ["Verhältnis zu FFB EG", "FFB EG max. 0,30 m über dem Bezugspunkt (SH). Bei SH 0,30 m: Baukörper max. +11,70 m über FFB; E/F zeichnen +12,00 m über FFB → bei SH > 0 überschritten, nur bei FFB = Fahrbahnhöhe möglich."],
        ["Traufhöhe", "max. 6,50 m (Schnittkante Mauerwerk/Dachhaut): Oberkante 1. OG der Entwürfe (+7,90 / +8,20 m) liegt darüber."],
        ["Vollgeschosse / Dach", "II zwingend; Hauptdach geneigt ≥ 38° (Flachdach nur Verbindungsbauten, ≥ 1,0 m unter First, bzw. untergeordnete Teile ≤ 70 m²). Dreigeschossige Flachdachbauten (B3, B, C, E, F) passen nicht zum Entwurf."],
        ["Fazit", "Die 12,00 m bleiben Planungsziel, gelten aber erst als eingehalten, wenn (1) Ursprungsplan/Satzung für Baufeld 3 vorliegt, (2) Fahrbahnhöhe vor dem Baukörper bekannt ist, (3) Traufe/Dachform/Vollgeschosse geklärt sind."]]
    table(d, 1480, 290, [420, 1500], rows, 26); return im
def p_plaene(n):
    im, d = page(); header(d, "Planauszüge der Stadt (Entwurf 1. Änderung)", "links Entwurfszeichnung (Abb. 2, Stand 25.08.2026), rechts Nutzungskonzept (Abb. 3, Stand 14.08.2026) · Quelle: Schallgutachten Bericht 476-26-a-hi, Büro Gieselmann und Müller", TAG); footer(d, n)
    w = (W - 240 - 60) // 2; paste(im, os.path.join(SRC, "Abb2_Entwurfszeichnung_BPlan123_1Aend.jpg"), 120, 280, w, 2000); paste(im, os.path.join(SRC, "Abb3_Nutzungskonzept_BPlan123_1Aend.jpg"), 120 + w + 60, 280, w, 2000); return im
def kandidaten_bild():
    im = Image.open(os.path.join(SRC, "Abb3_Nutzungskonzept_BPlan123_1Aend.jpg")).convert("RGB"); x0, y0, x1, y1 = 300, 280, 900, 660; c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 3, (y1 - y0) * 3), Image.LANCZOS); d = ImageDraw.Draw(c); k = 3 / 2
    def P(pts): return [(int(a * k), int(b * k)) for a, b in pts]
    K1 = [(280, 90), (640, 90), (640, 365), (280, 365)]; K2 = [(720, 90), (1105, 90), (1105, 200), (985, 380), (720, 380)]
    for pts, col in ((K1, (0, 90, 255)), (K2, (0, 150, 80))): d.line(P(pts) + [P(pts)[0]], fill=col, width=6)
    bf = [(312, 122), (607, 122), (607, 332), (312, 332)]; d.line(P(bf) + [P(bf)[0]], fill=(255, 140, 0), width=5)
    d.text((int(300 * k), int(100 * k)), "K1", font=F(48, "SemiBold"), fill=(0, 90, 255)); d.text((int(740 * k), int(100 * k)), "K2", font=F(48, "SemiBold"), fill=(0, 150, 80))
    return c
def p_kand(n):
    im, d = page(); header(d, "Abgeleitete Grundstückskonturen (Näherung aus dem Nutzungskonzept)", "Blau: Kandidat K1, grün: Kandidat K2, orange: Baufenster K1 (3 m Abstand) · Maßstabsabgriff aus Abb. 3, ±2 m · KEINE vermessenen Grenzen", TAG); footer(d, n)
    c = kandidaten_bild(); tmp = os.path.join(OUT, "_kand.png"); c.save(tmp); paste(im, tmp, 120, 280, 2300, 1500); os.remove(tmp)
    t = ("Ableitung: Maßstab 1:1000 der Abbildung; Straßenbreite Planstraße 16 m und Stichstraße/Parkplatz-Arm 11 m dienten als Kontrolle. Die grünen Flächen zwischen Planstraße (Süden), Parkplatz (Norden), Stichstraße (Westen) und Fuß-/Radweg (Osten) sind als Baufelder abgegrenzt; Parzellengrenzen sind in der Abbildung nicht eingezeichnet.\n\n"
         "K1: ca. 33 × 25 m ≈ 830 m². K2: ca. 35 × 27 m ≈ 900 m² (Trapez). Die Projektangabe 960 m² passt zu keinem der beiden genau; Baufeld 3 kann also ein anderes Baufeld sein oder Teile der angrenzenden Wege einschließen. Die Zuordnung erfordert Seite 13/15/16 des Auftraggebers.\n\n"
         "Baugrenzen (Entwurf): 3,0 m Abstand zu Planstraße und Parkplatz (gesichert); Ost/West angenommen. Baufenster K1 ≈ 27 × 19 m = 513 m².")
    text_block(d, 2480, 300, 920, t, 26); return im
def p_lageplan(n):
    im, d = page(); header(d, "Lageplan Kandidat K1: Baufenster und Gebäudefußabdrücke", "Maße in m, Näherung ±2 m · Baugrenze N/S 3,0 m gesichert, W/O 3,0 m angenommen · Parken auf eigener Fläche nach Fußabdruck", TAG); footer(d, n)
    S_ = 34; ox, oy = 240, 300; c = KAND["K1"]; bw, bd = baufenster("K1")
    X = lambda x: int(ox + (x + 12) * S_); Y = lambda y: int(oy + (37 - y) * S_)   # y nach oben (Norden)
    # Umfeld
    d.rectangle([X(-12), Y(0), X(48), Y(-16)], fill=(220, 222, 226)); d.text((X(2), Y(-9)), "Planstraße 16 m (öffentlich, Süden)", font=F(26, "SemiBold"), fill=GREY)
    d.rectangle([X(-12), Y(c["d"] + 12), X(48), Y(c["d"])], fill=(226, 229, 234)); d.text((X(2), Y(c["d"] + 6)), "öffentlicher Parkplatz (63 Plätze, auch für Gewerbe) – Norden", font=F(26, "SemiBold"), fill=GREY)
    d.rectangle([X(-11), Y(c["d"]), X(0), Y(0)], fill=(226, 229, 234)); d.text((X(-11) + 6, Y(12)), "Stichstr./\nParkplatz-\narm 11 m", font=F(22), fill=GREY)
    d.rectangle([X(c["b"]), Y(c["d"]), X(c["b"] + 6), Y(0)], fill=(246, 214, 214)); d.text((X(c["b"]) + 4, Y(12)), "Fuß-/\nRadweg", font=F(22), fill=GREY)
    d.rectangle([X(0), Y(c["d"]), X(c["b"]), Y(0)], fill=(222, 235, 190), outline=INK, width=4); d.text((X(0.5), Y(c["d"]) + 6), f"Kandidat K1 ≈ {c['b']:.0f} × {c['d']:.0f} m = {c['b']*c['d']:.0f} m² (abgeleitet)", font=F(24, "SemiBold"), fill=INK)
    dashed = lambda box, col, w=3: [d.line([(box[0] + i, box[1]), (box[0] + i + 14, box[1])], fill=col, width=w) or d.line([(box[0] + i, box[3]), (box[0] + i + 14, box[3])], fill=col, width=w) for i in range(0, box[2] - box[0], 28)] + [d.line([(box[0], box[1] + j), (box[0], box[1] + j + 14)], fill=col, width=w) or d.line([(box[2], box[1] + j), (box[2], box[1] + j + 14)], fill=col, width=w) for j in range(0, box[3] - box[1], 28)]
    bf = (X(ABST), Y(c["d"] - ABST), X(c["b"] - ABST), Y(ABST)); dashed(bf, (255, 140, 0), 4); d.text((bf[0] + 8, bf[1] + 6), f"Baufenster ≈ {bw:.0f} × {bd:.0f} m (3 m Abstand)", font=F(24, "SemiBold"), fill=(200, 100, 0))
    cols = [(180, 30, 30), (30, 90, 200), (30, 140, 90), (140, 60, 160)]
    foot = [("B3 EG 32 × 18", 32, 18, cols[0]), ("F4 EG 30 × 18", 30, 18, cols[1]), ("E1–E3 EG 27 × 17,5", 27, 17.5, cols[2]), ("Nutzungskonzept 26 × 11,5", 26, 11.5, cols[3])]
    for i, (lab, w, dd, col) in enumerate(foot):
        x = ABST; y = ABST + (i * 0.0); b = (X(x), Y(y + dd), X(x + w), Y(y)); dashed(b, col, 5); d.text((b[0] + 8, b[3] - 36 - i * 30), lab + (" – passt" if passt(bw, bd, w, dd) else " – ragt aus dem Baufenster"), font=F(22, "SemiBold"), fill=col)
    # Hinweis Parken
    d.text((X(-12), Y(-18)), "Parken auf K1: nach Abzug von Baufenster und Baugrenzstreifen (3 m) bleiben ≤ 3–4,5 m Tiefe → keine 5-m-Stellplätze mit Fahrgasse; allenfalls Längsparker im Südstreifen (Ausfahrt über Gehweg ungeklärt).", font=F(26), fill=BAD)
    rows = [["Fußabdruck", "Baufenster K1 27 × 19", "Baufenster K2 ≈ 29 × 21"]] + [[lab, ("passt" if passt(bw, bd, w, dd) else "passt NICHT"), ("passt" if passt(baufenster('K2')[0], baufenster('K2')[1], w, dd) else "passt NICHT")] for lab, w, dd in [(a, b, c_) for a, b, c_ in FOOT]]
    cl = {(i, j): (OK if r[j] == "passt" else BAD) for i, r in enumerate(rows) if i for j in (1, 2)}
    table(d, 2320, 330, [520, 290, 290], rows, 22, colors=cl)
    text_block(d, 2320, 1000, 1080, "Befund (unter dem Vorbehalt der Kandidatenwahl): Der Entwurf B3 (EG 32 × 18 m, 576 m²) passt in keines der beiden Baufenster. F mit 540 m² passt nur in der gedrehten Lesart (30 × 18 m) und nur bei breiterem Baufenster; die wörtliche Lesart 18 × 30 m (30 m tief) passt nicht. Umlaufender Vorbau über die Baugrenze und Parken unter dem Vorbau auf eigener Fläche sind auf den abgeleiteten Grundstücken nicht möglich. Stellplätze für Gastro/Büro müssten über den öffentlichen Parkplatz (63 Plätze, Baulast/Mitnutzung ungeklärt) oder die vom Nutzungskonzept vorgesehenen privaten Stellplätze neben den Gebäuden nachgewiesen werden.", 26); return im
def p_offen(n):
    im, d = page(); header(d, "Konsequenzen und was für eine belastbare Aussage fehlt", "Offene Punkte", TAG); footer(d, n)
    t = ("Fehlt: (1) die Fotos der Seiten 13, 15, 16 (oder der Hinweis, welches Baufeld im Nutzungskonzept „Baufeld 3“ ist); (2) der rechtskräftige Ursprungsplan Nr. 123 (14.04.2023) mit Festsetzungen zu Vollgeschossen/Höhen/Baugrenzen des Baufelds; (3) Katasterauszug/Vermessung für die Grenzen; (4) Fahrbahnhöhe der Erschließungsstraße vor dem Baukörper (Bauamt); (5) städtebaulicher Vertrag/Kaufvertrag mit Stellplatzregelung; (6) Zusage zur Mitnutzung des öffentlichen Parkplatzes/Baulast.\n\n"
         "Folgerungen für die Variantenstudie: Die Varianten E/F auf dem hypothetischen Rechteck 32 × 30 m zeigen Obergrenzen. Auf den aus den amtlichen Plänen abgeleiteten Baufeldern (ca. 830–900 m², Baufenster ca. 27 × 19 m) bleiben nur kleinere Gebäude möglich (Nutzungskonzept: ca. 26 × 11,5 m); die Wohnflächen der Varianten sind dann nicht realisierbar. Erst nach Klärung der Punkte (1)–(6) lässt sich eine Variante dimensionieren.\n\n"
         "Keine Variante wurde festgelegt; bestehende Modelle und B3 sind unverändert.")
    text_block(d, 120, 300, 3260, t, 34); return im
def seiten(n0=1, nur_kern=False):
    fs = [p_title, p_status, p_recht, p_plaene, p_kand, p_lageplan, p_offen]
    if nur_kern: fs = [p_recht, p_kand, p_lageplan]
    return [f(n0 + i) for i, f in enumerate(fs)]
if __name__ == "__main__":
    pages = seiten(); p = os.path.join(OUT, "Grundstuecksanalyse_Baufeld3.pdf"); save(pages, p); print(p)
