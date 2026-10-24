"""Entwurfs-PDFs E (E1–E4) und F (F1–F4, EG 540 m²), Stellplatzberechnung und Vergleich E/F/B/C. Aus varianten*.py, parken.py, e_zeichnen.py und den Blender-Ansichten."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(__file__))
from pdflib import *
import varianten as VA, parken as PK, e_zeichnen as EZ, entscheidung_pdf as ED
OUT = os.path.join(VA.ROOT, "studie_gebaeudeformen"); EK = ["E1", "E2", "E3", "E4"]; FK = ["F1", "F2", "F3", "F4"]
fm = lambda x, n=0: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
D = {k: VA.kennzahlen(k) for k in ["A", "B", "C", "D"] + EK + FK}
PRK = {k: PK.pruefe(k) for k in EK + FK}; BIL = {k: PK.flaechenbilanz(k) for k in EK + FK}
# B und C mit den 11 B3-Stellplätzen prüfen (gleiche Annahmen)
for k in ("B", "C"):
    VA.V[k + "P"] = dict(VA.V[k], stalls_row1=[tuple(s) for s in VA.B3["parking"]["stalls"]], stalls_row2=[], stalls_par=[], stall_face={"row1": "S"}, saeulen_pts=D[k]["saeulen"], fahrgasse=(0, 23.0, 32, 29.0), zufahrt=(32.0, 23.0, 32.0, 29.0), zufahrt_dir="E", eingaenge=[])
    PRK[k + "P"] = PK.pruefe(k + "P")
IMG = lambda k, n: f"{OUT}/{k}/ansichten/{n}.png"; PLN = lambda k, n: f"{OUT}/{k}/plaene/{n}.png"
LBL = {"ok": "voraussichtlich ok", "pruef": "zu prüfen", "kritisch": "kritisch / offen", "offen": "offen"}; COLR = {"ok": OK, "pruef": WARN, "kritisch": BAD, "offen": WARN}
def nutz(k): return PRK[k]["nutzbar"] if k in PRK else (11 if k == "A" else PRK[k + "P"]["voll"] + PRK[k + "P"]["eingeschraenkt"])
def stp(k): return D[k]["stp"]
def meets(k):
    n = nutz(k); s = D[k]["stp"]; j = lambda b: "ja" if b else "nein"
    return f"{j(n >= s['erf_lo'] - 0.05)}/{j(n >= s['erf_mid'] - 0.05)}/{j(n >= s['erf_hi'] - 0.05)}"
def stp_status(k):
    n = nutz(k); s = stp(k)
    if n >= s["erf_hi"]: return "ok", f"{n} nutzbar ≥ erforderlich bis {fm(s['erf_hi'],1)}"
    if n >= s["erf_mid"]: return "pruef", f"{n} nutzbar, erforderlich {fm(s['erf_lo'],1)}–{fm(s['erf_hi'],1)} (Mittel {fm(s['erf_mid'],1)}): Spanne der Bauaufsicht entscheidet"
    return "kritisch", f"{n} nutzbar < erforderlich Mittel {fm(s['erf_mid'],1)} ({fm(s['erf_lo'],1)}–{fm(s['erf_hi'],1)}): Ablöse/Mitbenutzung nötig"
def ampel(k):
    d = D[k]; v = VA.V[k]; ov = EZ.over_plot(k); mx = max(ov.values()); r = []
    hh = d["hoehe"]["attika"]
    r.append(("Gebäudehöhe / Traufe", "kritisch", f"Attika +{fm(hh,2)} m über FFB, Wandhöhe ≈ +{fm(hh-0.5,2)} m. Plan A (rechtskräftig 2023, MI 3): H 15,00 m ok, aber TH 9,80 m überschritten. Plan B (Entwurf 2026, nicht einschlägig): H 12,00 m über OK Fahrbahn (FFB max. +0,30 m → Baukörper max. +11,70 m über FFB), TH 6,50 m überschritten. Fahrbahnhöhe unbekannt."))
    r.append(("Geschosse / Dach", "kritisch", f"Plan A: II–III, drei Geschosse zulässig; Plan B: II zwingend (✗). Beide Pläne: Hauptdach geneigt ≥ 38°, Flachdach nur untergeordnet → alle Flachdach-Entwürfe benötigen Befreiung; 2. OG = {fm(d['staffel_anteil']*100)} % des 1. OG."))
    g = d["grz_projektion"]; r.append(("GRZ / Überdeckung", "ok" if g <= 0.6 else ("pruef" if g <= 0.8 else "kritisch"), f"größte Geschossprojektion {fm(d['projektion_m2'])} m² = {fm(g*100)} % von 960 m² (GRZ 0,6 = 576 m² nur Annahme)."))
    if mx > 0: r.append(("Grenzen / Baugrenzen", "kritisch", f"Überstand {fm(mx,2)} m über H1 ({'Platzseite' if ov['platz'] else 'Seite'}); Außenkante sonst auf der Grenze."))
    else: r.append(("Grenzen / Baugrenzen", "kritisch", "Baufenster MI 3 (P23) ≈ 27,7 × 15,9 m (abgeleitet), Baugrenzen 10,0 m West / 3 m übrige Seiten; EG-Fußabdruck und Vorbau über die Baugrenze passen nicht (siehe Entscheidungs-PDF)."))
    a, b = stp_status(k); r.append(("Stellplätze (gesetzlich)", a, b))
    r.append(("Gewerbe im EG", "pruef", f"EG {fm(d['flaeche']['eg'])} m² (B3: 576 m²); Gastraum ca. {fm(VA.V[k].get('gastro_m2',280))} m²."))
    r.append(("Brandschutz / Feuerwehr", "pruef", "Vorbau über Stellplätzen/Fahrgasse, Aufstellflächen und Feuerwehrzufahrt, Rettungswege – Konzept erforderlich."))
    return r
def kenn_rows(k):
    d = D[k]; m = d["mix"]["standard"]; pk = PRK[k]; s = stp(k); ov = EZ.over_plot(k)
    return [["Kennzahl", "Wert (vorläufig)"], ["Höhe", "12,00 m Attika (EG 4,30 · 1. OG 3,60 · 2. OG 3,60 · Dach/Attika 0,50), 3 Geschosse – Höhenbezug offen"],
        ["Grundfläche EG / 1. OG / 2. OG", f"{fm(d['flaeche']['eg'])} / {fm(d['flaeche']['og1'])} / {fm(d['flaeche']['st'])} m²"],
        ["Außenmaße EG / 1. OG / 2. OG", f"{d['aussenmasse']['eg'][0]:.1f} × {d['aussenmasse']['eg'][1]:.1f} / {d['aussenmasse']['og1'][0]:.1f} × {d['aussenmasse']['og1'][1]:.1f} / {d['aussenmasse']['st'][0]:.1f} × {d['aussenmasse']['st'][1]:.1f} m"],
        ["Wohnfläche netto (geschätzt)", f"{fm(d['wfl'])} m²"], ["Wohnungen Standardmix", f"{m['we']} WE ({m['we_og1']} + {m['we_st']}), {fm(m['kleinste'])}–{fm(m['groesste'])} m², Ø {fm(m['mittel'])} m²"],
        ["Gewerbe", f"EG {fm(d['flaeche']['eg'])} m²; Gastraum ca. {fm(VA.V[k]['gastro_m2'])} m² (≈ {s['sitze_innen']} Plätze), Terrasse/Arkade ≈ {s['sitze_terrasse']} Plätze, Büro {fm(s['buero_m2'])} m²"],
        ["Säulen", f"{d['anzahl_saeulen']} Säulen Ø 0,40 m; Paare 5,4 m (zwei Stellplätze + Säule)"],
        ["Stellplätze gezeichnet", f"{pk['gesamt']}: {pk['voll']} voll nutzbar, {pk['eingeschraenkt']} eingeschränkt, {pk['konflikt']} Konflikt"],
        ["Stellplätze erforderlich (§ 47 NBauO)", f"{fm(s['erf_lo'],1)}–{fm(s['erf_hi'],1)}, Mittel {fm(s['erf_mid'],1)} (nur Gastro + Büro; Wohnen 0)"],
        ["Stellplätze optional (Komfort/Markt)", f"Wohnen 0,5–1,5 je WE = {fm(s['optional']['standard']['lo'])}–{fm(s['optional']['standard']['hi'])}; Komfortziel gesamt ≈ {fm(s['komfort_ziel']['standard'])}"],
        ["Überstand über Grundstück H1", f"{fm(max(ov.values()),2)} m"]]
def page_with(title, sub, n, tag):
    im, d = page(); header(d, title, sub, tag); footer(d, n); return im, d
def pages_for(k, n, tag):
    d = D[k]; v = VA.V[k]; pages = []; pk = PRK[k]; bil = BIL[k]
    im, dr = page_with(v["name"], "Entwurfsstudie Baufeld 3 · Konzeptvariante, keine Genehmigungsplanung", n, tag); paste(im, IMG(k, "aerial"), 120, 270, 1900, 1070)
    y = text_block(dr, 2080, 280, 1320, v["idee"], 30, INK, "SemiBold"); table(dr, 2080, y + 20, [430, 890], kenn_rows(k), 24)
    text_block(dr, 120, 1380, 1900, "Alle Maße sind Planungsannahmen: Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m, Säule Ø 0,40 m, Grundstück 32 × 30 m (Hypothese; die städtischen Unterlagen Seite 13/15/16 liegen nur als Beschreibung vor, nicht als Foto), Zufahrt = Annahme. Wohnfläche = 0,88 × Wohnstreifen, schematisch. Nichts ist genehmigt, bemessen oder abgestimmt.", 26, GREY); pages.append(im); n += 1
    im, dr = page_with(f"{k}: Lageplan mit Gebäude, Säulen, Zufahrt und Stellplätzen", v["name"] + " · grün = Stellplatz funktioniert, orange = eingeschränkt, rot = Konflikt, rosa = nur rechnerisch verbleibende Fläche", n, tag); paste(im, PLN(k, "lageplan"), 120, 260, 2300, 2000)
    t = [["Stellplatzprüfung", ""], ["Gezeichnet", str(pk["gesamt"])], ["funktionieren voll", str(pk["voll"])], ["eingeschränkt", str(pk["eingeschraenkt"])], ["Konflikt", str(pk["konflikt"])], ["Min. Nutzbreite 90°", f"{pk['min_nutzbreite']:.2f} m"], ["Fahrgasse", f"{pk['fahrgasse_breite']:.1f} m" + (" – " + "; ".join(pk["fahrgasse_probleme"]) if pk["fahrgasse_probleme"] else " (frei)")],
         ["Flächenbilanz 960 m²", ""], ["Erdgeschoss", f"{fm(bil['eg'],1)} m²"], ["Stellplätze", f"{fm(bil['stall']+bil['par'],1)} m²"], ["Fahrgasse", f"{fm(bil['fahr'],1)} m²"], ["Zugangszonen", f"{fm(bil['zone'],1)} m²"], ["nur rechnerisch", f"{fm(bil['rest'],1)} m²"]]
    yy = table(dr, 2480, 300, [470, 450], t, 25); text_block(dr, 2480, yy + 20, 920, "\n".join("• " + h for h in pk["hinweise"]), 22, GREY); pages.append(im); n += 1
    im, dr = page_with(f"{k}: Grundrisse EG, 1. OG, 2. OG", v["name"] + " · schematisch", n, tag); gap = 60; w = (W - 240 - gap * 2) // 3
    for i, (p, cap) in enumerate(((PLN(k, "plan_eg"), "Erdgeschoss"), (PLN(k, "plan_og1"), "1. Obergeschoss"), (PLN(k, "plan_st"), "2. Obergeschoss"))): x = 120 + i * (w + gap); dr.text((x, 270), cap, font=F(36, "SemiBold"), fill=INK); paste(im, p, x, 330, w, H - 330 - 200)
    pages.append(im); n += 1
    im, dr = page_with(f"{k}: vier Fassaden", v["name"] + " · orthogonale Ansichten aus dem 3D-Modell", n, tag); w = (W - 240 - 60) // 2; h = (H - 330 - 130) // 2
    cap_r = "Rückfassade" ; 
    for i, (nm, cap) in enumerate((("front", "Vorderfassade (Platzseite)"), ("rear", "Rückfassade"), ("west", "Seitenfassade West"), ("east", "Seitenfassade Ost"))):
        x = 120 + (i % 2) * (w + 60); y = 280 + (i // 2) * (h + 70); dr.text((x, y), cap, font=F(34, "SemiBold"), fill=INK); paste(im, IMG(k, nm), x, y + 50, w, h)
    pages.append(im); n += 1
    im, dr = page_with(f"{k}: Gebäudeschnitt mit Geschosshöhen und 3D-Ansichten", v["name"], n, tag); paste(im, PLN(k, "schnitt"), 120, 270, 2250, 1200); paste(im, IMG(k, "persp"), 120, 1520, 1500, 800); paste(im, IMG(k, "aerial"), 1700, 1520, 1500, 800); pages.append(im)
    return pages
def hoehen_seite(n, tag):
    im, d = page_with("Höhenrahmen: B3 (+9,90 m) und E/F (+12,00 m)", "Schnittschema · Plan A (2023): H 15 m/TH 9,80 m · Plan B (Entwurf 2026): H 12 m/TH 6,50 m · Bezugspunkt OK Fahrbahn", n, tag)
    base, sc = 2000, 135
    def col(x, levels, title, note):
        d.text((x, 270), title, font=F(34, "SemiBold"), fill=INK)
        for (z0, z1, lab, c) in levels:
            d.rectangle([x, base - z1 * sc, x + 520, base - z0 * sc], fill=c, outline=INK, width=3); d.text((x + 16, base - (z0 + z1) / 2 * sc - 14), lab, font=F(26), fill=INK)
        d.text((x, base + 20), note, font=F(24), fill=GREY)
    col(150, [(0, 3.5, "EG 3,50 m", (245, 245, 245)), (3.5, 6.5, "1. OG 3,00 m", (252, 240, 232)), (6.5, 9.6, "Staffel 3,10 m", (252, 246, 236)), (9.6, 9.9, "", (130, 130, 135))], "B3 / A–D (bisher)", "Attika +9,90 m über FFB EG")
    col(950, [(0, 4.3, "EG 4,30 m (lichte ≈ 3,85)", (245, 245, 245)), (4.3, 7.9, "1. OG 3,60 m (lichte ≈ 3,15)", (252, 240, 232)), (7.9, 11.5, "2. OG 3,60 m (lichte ≈ 3,15)", (252, 246, 236)), (11.5, 12.0, "", (130, 130, 135))], "E/F (Höhenschema H12)", "Attika +12,00 m über FFB EG")
    d.line([(100, base - 12 * sc), (1600, base - 12 * sc)], fill=OK, width=4); d.text((130, base - 12 * sc - 40), "+12,00 m über FFB (Plan B nur bei SH 0; Plan A: H 15 m)", font=F(26, "SemiBold"), fill=OK)
    d.line([(100, base - 11.7 * sc), (1600, base - 11.7 * sc)], fill=BAD, width=4); d.text((1000, base - 11.7 * sc + 8), "+11,70 m über FFB bei SH 0,30 m", font=F(26, "SemiBold"), fill=BAD)
    rows = [["Aspekt", "Aussage (Quelle: B-Plan Nr. 123 rechtskräftig 2023 und 1. Änderung Entwurf 2026)"],
        ["Bezugspunkt (beide Pläne)", "H über Oberkante Fahrbahn der nächsten ausgebauten Erschließungsstraße in der Mitte vor dem Baukörper (nicht über FFB); FFB EG max. 0,30 m darüber (SH). Fahrbahnhöhe unbekannt."],
        ["Plan A: rechtskräftig 2023 (MI 3 / MI 1)", "II–III, TH max. 9,80 m, H max. 15,00 m. Attika +12,0 m über FFB passt zu H; die Wandhöhe ≈ +11,5 m überschreitet aber TH 9,80 m."],
        ["Plan B: Entwurf 2026 / MI 2", "II zwingend, TH 6,50 m, H 12,00 m (max. +11,70 m über FFB bei SH 0,30 m). Für MI 3 nicht einschlägig; hier hypothetisch."],
        ["Dach (beide Pläne)", "Hauptdach geneigt ≥ 38°; Flachdach nur Verbindungsbauten/≤ 70 m² → dreigeschossige Flachdachbauten brauchen Befreiung."], ["Nutzung der Reserve", "Statt eines vierten Geschosses (nicht angenommen) fließt die Höhe in Geschosshöhen (lichte ≈ 3,15 m); Wohnfläche steigt dadurch nicht."]]
    table(d, 1750, 300, [330, 1350], rows, 25); return im
def quellen_seite(n, tag):
    im, d = page_with("Grundstück, Baugrenzen und Quellenstatus", "Was gesichert ist, was nur aus Beschreibungen stammt und was Hypothese ist", n, tag)
    rows = [["Punkt", "Stand", "Herkunft / Bemerkung"], ["Grundstücksfläche ca. 960 m²", "GESICHERT (Projektangabe)", "Projektunterlagen/Auftraggeber; nicht am Liegenschaftsnachweis geprüft"],
        ["Zuschnitt 32 × 30 m (Variantenstudie E/F)", "HYPOTHESE H1", "nur aus 960 m² und B3-Annahme; widerspricht dem Planausschnitt: Flurstück 59/1 ≈ 42,3 × 22,7 m (geschätzt), Baufenster ≈ 27,7 × 15,9 m (abgeleitet)"],
        ["B-Plan Nr. 123 „Ehemalige Grundschule“, 1. Änderung (Entwurf 25.09.2026): MI, GRZ 0,6, II zwingend, TH 6,50 m, H 12,00 m, SH 0,30 m, Baugrenze 3 m", "GESICHERT (Entwurf)", "amtliche Unterlagen der Stadt Werlte (sgwerlte.de), in quellen_stadt/ abgelegt; nicht rechtskräftig"],
        ["Foto-Seiten 13/15/16 des Auftraggebers („zwei- bis dreigeschossig“)", "FEHLEN", "ZIP nicht angekommen; Seite 15/16 entsprechen vermutlich Abb. 2/3 der 1. Änderung (unbestätigt)"],
        ["Zuordnung „Baufeld 3“ im Nutzungskonzept", "INDIZ: MI 3 / Flurstück 59/1", "Fläche ≈ 960 m² und Z II–III passen; Seite 13 fehlt (unbestätigt)"],
        ["Baugrenzen / Baulinien, GRZ, Abstandsflächen", "UNBEKANNT", "keine Maße am Plan abgelesen; alle Konturen in den Plänen sind Hypothese"],
        ["Erschließungsstraße, Zufahrt, Platzseite", "ANNAHME", "Platz an der Seite y = 0; Zufahrt von Osten (E) bzw. Süden (F) angenommen"],
        ["Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m", "ANNAHME (Auftraggeber, vorläufig)", "Abgleich mit Stellplatzsatzung/Garagenverordnung ausstehend"]]
    cl = {(i, 1): (OK if r[1].startswith("GESICHERT") else (WARN if "BESCHREIBUNG" in r[1] or "ANNAHME" in r[1] else BAD)) for i, r in enumerate(rows) if i}
    y = table(d, 120, 290, [1100, 560, 1520], rows, 28, colors=cl)
    text_block(d, 120, y + 60, 3200, "Die ZIP-Datei mit den Fotos der Seiten 13, 15 und 16 ist in dieser Sitzung nicht angekommen; der Ordner quellen_stadt/fotos_stadt_unterlagen/ ist leer. Grundlage sind die amtlichen Planunterlagen der Stadt (Entwurf B-Plan 123, 1. Änderung). Konturen aus den Plänen sind als ABGELEITET/GESCHÄTZT gekennzeichnet, gesicherte Maße getrennt (siehe Entscheidungs-PDF).", 30)
    return im
def pruefung540(n, tag):
    im, d = page_with("Planungsziel EG 540 m² + 420 m² Restfläche: Prüfung gegen die Hypothese", "18 m × 30 m = 540 m² Gebäude, 960 − 540 = 420 m² für Zufahrt, Fahrgasse, Stellplätze, Freiflächen", n, tag)
    rows = [["Lesart", "Anordnung auf H1 (32 × 30 m)", "Vereinbar?", "Bemerkung"],
        ["F1–F3 wörtlich: 18 m Platzseite × 30 m Tiefe", "EG x 1–19, y 0–30; Restfläche = Streifen 14 × 30 m (+1 m Westrand)", "geometrisch ja, mit Abweichung", "EG füllt die ganze Grundstückstiefe: rückseitig KEIN Vorbau und keine Rückfahrfläche; Vorbau vorn ragt 1,5 m in den Platz (Überstand!); Zufahrt nur von Süden"],
        ["F4 gedreht: 30 m Platzseite × 18 m Tiefe", "EG x 1–31, y 1–19; Restfläche = hinterer Streifen 32 × 11 m + Ränder", "ja", "Vorbau rundum innerhalb H1 (vorn/seitlich 1,0 m, hinten 5,0 m über der Stellplatzreihe); eine Stellplatzreihe + 6-m-Fahrgasse"],
        ["Baugrenzen/Abstände", "unbekannt", "NICHT PRÜFBAR", "Baufenster geschätzt 400–460 m² (project_brief, nicht gemessen) läge unter 540 m²; ohne Planfoto keine Aussage"]]
    y = table(d, 120, 290, [700, 900, 420, 1160], rows, 27)
    rows2 = [["Restfläche 420 m² (EG 540 m²)", "F1–F3", "F4"]] + [[lab] + [fm(BIL[k][key] if key != "sp" else BIL[k]["stall"] + BIL[k]["par"], 1) + " m²" for k in ("F1", "F4")] for lab, key in (("Stellplätze (funktionierend)", "sp"), ("Fahrgasse 6,00 m", "fahr"), ("Zugangszonen (Eingänge)", "zone"), ("nur rechnerisch verbleibend (nicht nutzbar)", "rest"))]
    rows2.append(["Summe Restfläche", fm(960 - BIL["F1"]["eg"], 1) + " m²", fm(960 - BIL["F4"]["eg"], 1) + " m²"])
    table(d, 120, y + 60, [1200, 500, 500], rows2, 30)
    text_block(d, 120, y + 560, 3200, "Ergebnis: Die 420 m² sind nicht vollständig Stellplatzfläche. Nach Abzug von Fahrgasse (180–192 m²), Zugängen und Randstreifen bleiben rund 100–155 m² für Stellplätze = 8–13 Plätze (F1–F3: 8 Plätze 90° + 5 Parallelparker; F4: 9). Der verbleibende Rest ist nur rechnerisch vorhanden.", 32, INK, "SemiBold")
    return im
def intro(n, tag, titel, sub):
    pages = []; im, d = page_with(titel, sub, n, tag)
    y = text_block(d, 120, 280, 3260, "Ziel: Gebäudehöhe bis 12,00 m planerisch ausnutzen (drei Geschosse, keine zusätzlichen), umlaufender säulengestützter Vorbau, Zufahrt und Stellplätze unter und neben dem Vorbau. Keine Variante ist festgelegt; B3 (Variante A) und alle bestehenden Modelle bleiben unverändert. Alle Flächen sind vorläufig, bis Grundstücksgrenzen und Baugrenzen verlässlich geklärt sind.", 34)
    rows = [["", "Bestätigt (Quelle)", "Annahme / unbestätigt"], ["Grundstück", "ca. 960 m²; B-Plan 123 rechtskräftig 2023: Baufeld 3 vermutlich MI 3 / Flurstück 59/1 mit Baugrenzen 10,0 m West, 3 m übrige Seiten", "Zuschnitt 32 × 30 m = Hypothese H1; Planausschnitt: ≈ 42,3 × 22,7 m (geschätzt), Baufenster ≈ 27,7 × 15,9 m (abgeleitet); Foto-Seiten fehlen"], ["Höhe / Geschosse", "Plan A rechtskräftig 2023 (MI 3): II–III, TH 9,80 m, H 15,00 m; Plan B Entwurf 2026 (MI 2/Änderung): II zwingend, TH 6,50 m, H 12,00 m; beide: Dach ≥ 38°, Bezug OK Fahrbahn", "Baufeld 3 nicht bestätigt; Fahrbahnhöhe unbekannt; Befreiungen (Dach, Baugrenze, TH) offen"],
        ["Stellplätze Wohnen", "KEINE gesetzliche Pflicht seit 01.07.2024 (§ 47 Abs. 1 Satz 3 NBauO; FAQ Land Niedersachsen Stand 11.07.2025)", "ob B-Plan/städtebaulicher Vertrag/Kaufvertrag Stellplätze für Wohnungen verlangt: unbekannt"], ["Stellplätze Gastro/Büro", "Pflicht besteht; Bemessung bedarfsorientiert (Richtzahlen Erlass: Gaststätte 1 je 8–12 Sitzplätze, Büro 1 je 30–40 m²)", "Gaststättenart („örtliche Bedeutung“) und Sitzplatzzahl angenommen"],
        ["Maße", "–", "Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m, Säule Ø 0,40 m (Vorgaben/Annahmen), Zufahrtslage"], ["Wohnfläche", "B3: 846 m², 16 WE (Plan)", "übrige Varianten aus Geschosskonturen geschätzt (0,88 × Wohnstreifen)"]]
    table(d, 120, y + 50, [380, 1400, 1480], rows, 28); pages.append(im); return pages
def ueberblick(n, tag, keys, titel):
    im, d = page_with(titel, "Standardmix · alle Werte vorläufig · Referenz B3 (A)", n, tag); ks = ["A"] + keys
    rows = [["Kennzahl"] + [VA.V[k]["name"].split(" – ")[0] + " " + (VA.V[k]["name"].split(" – ")[1][:30] if k != "A" else "B3") for k in ks],
        ["Staffelrücksprung"] + ["0,8 m"] + [f"{VA.V[k]['staffel_ruecksprung']:.1f} m" for k in keys], ["Grundfläche EG / 1. OG / 2. OG (m²)"] + [f"{fm(D[k]['flaeche']['eg'])} / {fm(D[k]['flaeche']['og1'])} / {fm(D[k]['flaeche']['st'])}" for k in ks],
        ["Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in ks], ["Δ Wohnfläche gg. A"] + ["±0"] + [f"{D[k]['wfl']-D['A']['wfl']:+.0f} ({(D[k]['wfl']/D['A']['wfl']-1)*100:+.0f} %)" for k in keys], ["Wohnungen"] + [str(D[k]["we"]) for k in ks],
        ["Gastraum (m²) / Plätze innen"] + [f"{fm(VA.V[k].get('gastro_m2',280))} / {D[k]['stp']['sitze_innen']}" for k in ks],
        ["Stellplätze gezeichnet / nutzbar"] + ["11 / 11"] + [f"{PRK[k]['gesamt']} / {PRK[k]['nutzbar']}" for k in keys],
        ["erforderlich § 47 (Spanne / Mittel)"] + [f"{fm(D[k]['stp']['erf_lo'],1)}–{fm(D[k]['stp']['erf_hi'],1)} / {fm(D[k]['stp']['erf_mid'],1)}" for k in ks], ["optional Wohnen (0,5–1,5 je WE)"] + [f"{fm(D[k]['stp']['optional']['standard']['lo'])}–{fm(D[k]['stp']['optional']['standard']['hi'])}" for k in ks],
        ["Säulen"] + ["0"] + [str(D[k]["anzahl_saeulen"]) for k in keys], ["Höhe Attika"] + ["9,90 m"] + ["12,00 m (Bezug offen)"] * len(keys)]
    cw = [820] + [(3268 - 820) // len(ks)] * len(ks); table(d, 120, 290, cw, rows, 28); return im
def abschluss(n, tag, keys):
    pages = []; im, d = page_with("Baurechtliche Ampel (vorläufig)", "Keine Rechtsprüfung · bis zur Klärung von Grundstück, Baugrenzen und Satzungen offen", n, tag)
    crit = [a for a, b, c in ampel(keys[0])]; rows = [["Kriterium"] + keys]; col = {}
    for i, cr in enumerate(crit):
        row = [cr]
        for j, k in enumerate(keys): a, b, c = ampel(k)[i]; row.append(LBL[b] + ": " + c); col[(i + 1, j + 1)] = COLR[b]
        rows.append(row)
    table(d, 120, 290, [560] + [(3268 - 560) // len(keys)] * len(keys), rows, 21, colors=col); pages.append(im)
    im, d = page_with("Offene Fragen und Prüfbedarf", "Vor jeder Weiterentwicklung zu klären", n + 1, tag)
    t = ("• Fotos der städtischen Unterlagen (S. 13, 15, 16) in den Projektordner; daraus Grundstückszuschnitt, Baugrenzen, GRZ, Höhenbezugspunkt, Traufhöhe, Dachform, Abstände, Festsetzungen zu Stellplätzen/Zufahrten.\n• Bebauungsplan-Stand: Entwurf (S. 15) – rechtskräftige Fassung; örtliche Bauvorschrift/Stellplatzsatzung für Nicht-Wohnungen; städtebaulicher Vertrag/Kaufvertrag (Stellplätze auch für Wohnungen möglich).\n• Einstufung der Gaststätte („örtliche“ oder „überörtliche Bedeutung“), Sitzplatzzahl innen/außen, Büro mit/ohne Besucherverkehr.\n• Höhenbezug der 12,00 m; Vollgeschoss-Definition für das 2. OG; Traufhöhe 6,50 m.\n• Überbauung des Platzes (F1–F3: 1,5 m), Grenz- und Abstandsflächen, GRZ-Anrechnung überdeckter Stellplätze.\n• Zufahrt: Straße, Gefälle, Sichtdreiecke; Feuerwehrzufahrt/Aufstellflächen unter dem Vorbau; Wendemöglichkeit in der Sackgasse (F1–F3).\n• Stellplatzmaße/Garagenverordnung für Stellplätze neben Säulen und Parallelparker; Schleppkurven.\n• Statik: Kragarme 1,0–5,0 m, Säulenraster 5,4 m, Fundamente; Brandschutz Vorbau.\n\nKeine Variante ist ausgewählt.")
    text_block(d, 120, 300, 3200, t, 34); pages.append(im); return pages
def entwurf(keys, name, tag, titel, sub, extra):
    pages = intro(1, tag, titel, sub); n = len(pages) + 1
    pages.append(quellen_seite(n, tag)); n += 1
    ga = [f(n + i) for i, f in enumerate([ED.p_staende, ED.p_zuordnung, ED.p_massrisiko, ED.p_fussabdruck])]; pages += ga; n += len(ga)
    pages.append(hoehen_seite(n, tag)); n += 1
    if extra: pages.append(pruefung540(n, tag)); n += 1
    pages.append(ueberblick(n, tag, keys, "Überblick " + "–".join([keys[0], keys[-1]]))); n += 1
    for k in keys: ps = pages_for(k, n, tag); pages += ps; n += len(ps)
    pages += abschluss(n, tag, keys); p = f"{OUT}/{name}"; save(pages, p); return p
def stellplatz_pdf():
    tag = "STELLPLÄTZE · VORLÄUFIG"; pages = []; n = 1
    im, d = page_with("Stellplatzberechnung nach § 47 NBauO – Pflicht und optionales Ziel getrennt", "Prüfung der geltenden Vorgaben (Quelle: FAQ Land Niedersachsen Stand 11.07.2025; Richtzahlen des Erlasses)", n, tag)
    t = ("1. Wohnungen: Seit 01.07.2024 keine gesetzliche Pflicht mehr für den durch Wohnungen verursachten Bedarf (§ 47 Abs. 1 Satz 3 NBauO, wenn der Bauantrag nach dem 30.06.2024 gestellt wird). Kommunale Stellplatzsatzungen sind für Wohnungen nichtig. Ein Bebauungsplan kann keine Mindestzahl je Wohnung festsetzen; ein städtebaulicher Vertrag kann Stellplätze weiterhin vereinbaren (FAQ 11.1, 11.7–11.9). Freiwillige Stellplätze sind zulässig (11.10).\n"
         "2. Gastronomie und Büro: Pflicht besteht weiter (§ 47 Abs. 1 Satz 1), bedarfsorientiert durch die Bauaufsicht; Richtzahlen: Gaststätte örtlicher Bedeutung 1 je 8–12 Sitzplätze, überörtlicher Bedeutung 1 je 4–8; Büro allgemein 1 je 30–40 m² Nutzfläche, mit Besucherverkehr 1 je 15–25 m² (mind. 5).\n"
         "3. B-Plan 123, 1. Änderung (Entwurf): keine Mindestzahl an Stellplätzen festgesetzt; Stadt plant einen öffentlichen Parkplatz mit 63 Plätzen (auch für angrenzende gewerbliche Nutzungen, nachts gesperrt); Wohn-Stellplätze werden den Wohneinheiten zugeordnet; Überdachung von Stellplätzen in der Parkplatzfläche unzulässig. Städtebaulicher Vertrag/Kaufvertrag und örtliche Bauvorschrift für Nicht-Wohnungen: UNBEKANNT/nicht gefunden.\n"
         "4. Vorbehalt: konsolidierter Gesetzestext in NI-VORIS war nicht abrufbar; Stand der Quelle 11.07.2025, spätere Änderungen sind zu prüfen.")
    y = text_block(d, 120, 290, 3260, t, 30); pages.append(im); n += 1
    im, d = page_with("Ergebnis je Variante: erforderlich (Pflicht) und optional (Ziel) getrennt", "„erforderlich“ = Gastro + Büro nach Richtzahlen (Spanne); „optional“ = freiwillig für Wohnen · „nutzbar“ = gezeichnet und geometrisch geprüft", n, tag)
    ks = ["A", "B", "C"] + EK + FK
    rows = [["Kennzahl"] + ks, ["Sitzplätze Gastro innen"] + [str(D[k]["stp"]["sitze_innen"]) for k in ks], ["Terrassen-/Arkadenplätze"] + [str(D[k]["stp"]["sitze_terrasse"]) for k in ks], ["Büro netto (m²)"] + [fm(D[k]["stp"]["buero_m2"]) for k in ks],
        ["ERFORDERLICH Gastro (1 je 8–12)"] + [f"{fm(D[k]['stp']['gastro_lo'],1)}–{fm(D[k]['stp']['gastro_hi'],1)}" for k in ks], ["ERFORDERLICH Büro (1 je 30–40 m²)"] + [f"{fm(D[k]['stp']['buero_lo'],1)}–{fm(D[k]['stp']['buero_hi'],1)}" for k in ks],
        ["ERFORDERLICH Wohnen"] + ["0"] * len(ks), ["ERFORDERLICH gesamt (Spanne)"] + [f"{fm(D[k]['stp']['erf_lo'],1)}–{fm(D[k]['stp']['erf_hi'],1)}" for k in ks], ["ERFORDERLICH gesamt (Mittel)"] + [fm(D[k]["stp"]["erf_mid"], 1) for k in ks],
        ["mit Terrassenplätzen (Mittel)"] + [fm(D[k]["stp"]["erf_mit_terrasse_mid"], 1) for k in ks], ["OPTIONAL Wohnen 0,5 / 1,0 / 1,5 je WE"] + [f"{fm(D[k]['stp']['optional']['standard']['lo'])} / {fm(D[k]['stp']['optional']['standard']['mid'])} / {fm(D[k]['stp']['optional']['standard']['hi'])}" for k in ks],
        ["Wohnungen (Standardmix)"] + [str(D[k]["we"]) for k in ks], ["NUTZBAR gezeichnet (voll + eingeschr.)"] + [str(nutz(k)) for k in ks], ["nutzbar ≥ Untergrenze / ≥ Mittel / ≥ Obergrenze"] + [meets(k) for k in ks]]
    cl = {(13, j + 1): (OK if nutz(k) >= D[k]["stp"]["erf_mid"] else BAD) for j, k in enumerate(ks)}
    cw = [760] + [(3268 - 760) // len(ks)] * len(ks); y = table(d, 120, 290, cw, rows, 22, colors=cl)
    ok_mid = [k for k in ks if nutz(k) >= D[k]["stp"]["erf_mid"] - 0.05]; no_mid = [k for k in ks if k not in ok_mid]
    text_block(d, 120, y + 40, 3260, "Lesart: Bewertet wird gegen die gesetzliche Pflicht (Gastro + Büro), nicht gegen eine pauschale Wohnungsquote; kein Fahrzeug wird für Wohnungen verlangt. Mittelwert der Richtzahlen erreichen: " + ", ".join(ok_mid) + ". Darunter: " + ", ".join(no_mid) + " (Ablöse nach § 47 Abs. 4 NBauO, Baulast auf Nachbargrundstück oder kleinere Sitzplatzzahl/Richtzahl 12 statt 8–10 als Ausweg, mit der Bauaufsicht zu klären). B3 (A) liegt mit 11 Plätzen knapp unter der Untergrenze 11,4. E4 hat den größten Überhang, aber das kleinste Gewerbe-EG (Gastraum 197 m²); das optionale Komfortziel (z. B. 1,0 Platz je WE zusätzlich) wird nur dort annähernd erreicht.", 28)
    pages.append(im); n += 1
    p = f"{OUT}/Stellplatzberechnung_NBauO47.pdf"; save(pages, p); return p
def vergleich_pdf():
    tag = "VERGLEICH · NICHT FESTGELEGT"; ks = ["A", "B", "C"] + EK + FK; pages = []; n = 1
    pages += intro(n, tag, "Vergleich der Varianten B, C, E1–E4 und F1–F4", "Entwurfsstudie Baufeld 3 · alle Werte vorläufig · keine Variante festgelegt"); n += 1
    pages.append(quellen_seite(n, tag)); n += 1
    ga = [f(n + i) for i, f in enumerate([ED.p_staende, ED.p_zuordnung, ED.p_massrisiko, ED.p_fussabdruck])]; pages += ga; n += len(ga)
    im, d = page_with("Erhöhte Schrägansichten im Vergleich", "gleiche Kamera, gleiche Darstellung", n, tag); kk = ["B", "C", "E1", "E2", "F1", "F2", "F3", "F4"]; w = 780
    for i, k in enumerate(kk): x = 120 + (i % 4) * (w + 30); y = 290 + (i // 4) * 900; d.text((x, y), VA.V[k]["name"].split(" (")[0][:34], font=F(26, "SemiBold"), fill=INK); paste(im, IMG(k, "aerial"), x, y + 40, w, 800)
    pages.append(im); n += 1
    im, d = page_with("Lagepläne im Vergleich (Stellplätze, Säulen, Zufahrt)", "grün = funktioniert, orange = eingeschränkt, rot = Konflikt, rosa = nur rechnerisch verbleibend", n, tag); kk = ["E1", "E4", "F2", "F4"]; w = (W - 240 - 3 * 40) // 4
    for i, k in enumerate(kk): x = 120 + i * (w + 40); d.text((x, 280), VA.V[k]["name"].split(" – ")[0] + " – " + VA.V[k]["name"].split(" – ")[1][:28], font=F(28, "SemiBold"), fill=INK); paste(im, PLN(k, "lageplan"), x, 340, w, 1900)
    pages.append(im); n += 1
    im, d = page_with("Vergleichstabelle 1: Flächen, Gewerbe, Wohnungen", "alle Werte vorläufig; Wohnfläche = 0,88 × Wohnstreifen, schematisch", n, tag)
    h = ["Kennzahl"] + [k for k in ks]; cw = [880] + [(3268 - 880) // len(ks)] * len(ks)
    def mx(k): return f"{D[k]['aussenmasse']['eg'][0]:.0f}×{D[k]['aussenmasse']['eg'][1]:.0f}"
    rows = [h, ["Höhe Attika (Bezug offen)"] + ["9,90"] * 3 + ["12,00"] * 8, ["Außenmaß EG (m)"] + [mx(k) for k in ks], ["Grundfläche EG (m²)"] + [fm(D[k]["flaeche"]["eg"]) for k in ks], ["Grundfläche 1. OG (m²)"] + [fm(D[k]["flaeche"]["og1"]) for k in ks], ["Grundfläche 2. OG / Staffel (m²)"] + [fm(D[k]["flaeche"]["st"]) for k in ks],
        ["Gastraum (m²) / Plätze innen"] + [f"{fm(VA.V[k].get('gastro_m2',280))}/{D[k]['stp']['sitze_innen']}" for k in ks], ["Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in ks], ["Δ Wohnfläche gg. A (m²)"] + [f"{D[k]['wfl']-D['A']['wfl']:+.0f}" for k in ks],
        ["Wohnungen Standardmix"] + [str(D[k]["we"]) for k in ks], ["Größen min–max (m²)"] + [f"{fm(D[k]['mix']['standard']['kleinste'])}–{fm(D[k]['mix']['standard']['groesste'])}" for k in ks], ["Ø Wohnungsgröße (m²)"] + [fm(D[k]["mix"]["standard"]["mittel"]) for k in ks],
        ["WE kleiner / größerer Mix"] + [f"{D[k]['mix']['klein']['we']}/{D[k]['mix']['gross']['we']}" for k in ks], ["Säulen"] + ["0"] + [str(D[k]["anzahl_saeulen"]) for k in ks[1:]], ["Überstand über H1 (m)"] + [fm(max(EZ.over_plot(k).values()), 1) for k in ks]]
    table(d, 120, 290, cw, rows, 24); pages.append(im); n += 1
    im, d = page_with("Vergleichstabelle 2: Stellplätze (Pflicht und Ziel getrennt)", "„nutzbar“ nach geometrischer Prüfung (Säulen, Eingänge, Fahrgasse); B/C mit den 11 B3-Stellplätzen geprüft", n, tag)
    rows = [h, ["Stellplätze gezeichnet"] + ["11"] + [str(PRK[k + "P"]["gesamt"]) for k in ("B", "C")] + [str(PRK[k]["gesamt"]) for k in EK + FK], ["davon voll nutzbar"] + ["11"] + [str(PRK[k + "P"]["voll"]) for k in ("B", "C")] + [str(PRK[k]["voll"]) for k in EK + FK],
        ["eingeschränkt"] + ["0"] + [str(PRK[k + "P"]["eingeschraenkt"]) for k in ("B", "C")] + [str(PRK[k]["eingeschraenkt"]) for k in EK + FK], ["Konflikt (Säule/Eingang/Gasse)"] + ["0"] + [str(PRK[k + "P"]["konflikt"]) for k in ("B", "C")] + [str(PRK[k]["konflikt"]) for k in EK + FK],
        ["erforderlich § 47 (Gastro+Büro, Spanne)"] + [f"{fm(D[k]['stp']['erf_lo'],1)}–{fm(D[k]['stp']['erf_hi'],1)}" for k in ks], ["erforderlich Mittel"] + [fm(D[k]["stp"]["erf_mid"], 1) for k in ks], ["erforderlich Wohnen"] + ["0"] * len(ks),
        ["optional Wohnen 0,5–1,5/WE"] + [f"{fm(D[k]['stp']['optional']['standard']['lo'])}–{fm(D[k]['stp']['optional']['standard']['hi'])}" for k in ks], ["nutzbar ≥ Untergrenze / Mittel / Obergrenze"] + [meets(k) for k in ks],
        ["Bemerkung"] + ["B3: 11 Plätze rückseitig"] + [f"{PRK[k+'P']['konflikt']} von {PRK[k+'P']['gesamt']} Plätzen durch Säulen/Gasse gestört (Raster 5,6 m ≠ Stellplatz)" for k in ("B", "C")] + [("Reihe unter Vorbau, Hintereingang-Lücke" if k != "E4" else "zweireihig, kleines EG") if k in EK else ("Sackgasse, Parallelparker Ostrand" if k != "F4" else "Reihe unter Vorbau") for k in FK] if False else ["Bemerkung"] + ["B3"] + [f"{PRK[k+'P']['konflikt']}/{PRK[k+'P']['gesamt']} gestört" for k in ("B", "C")] + ["1 Reihe", "1 Reihe", "1 Reihe", "2 Reihen"] + ["Sackgasse", "Sackgasse", "Sackgasse", "1 Reihe"]]
    cl = {(8, j + 1): (OK if nutz(k) >= D[k]["stp"]["erf_mid"] else BAD) for j, k in enumerate(ks)}
    y = table(d, 120, 290, cw, rows, 24, colors=cl)
    text_block(d, 120, y + 40, 3260, "Wichtig: Die Bewertung der Stellplätze erfolgt gegen die gesetzliche Pflicht (Gastro + Büro), nicht gegen eine pauschale Wohnungsquote. E4 wird daher nicht wegen fehlender Wohnungsstellplätze abgewertet; es hat den größten Überhang gegenüber der Pflicht, bezahlt dies aber mit 135 m² weniger Gewerbe-EG gegenüber E1–E3. F1–F3 erreichen die Pflicht (Mittel) mit 13 nutzbaren Plätzen knapp; E1–E3 und F4 (9 Plätze) liegen darunter.", 28); pages.append(im); n += 1
    pages += abschluss(n, tag, ["E1", "E2", "E3", "E4", "F1", "F2", "F3", "F4"]); p = f"{OUT}/Vergleich_E_F_B_C.pdf"; save(pages, p); return p
if __name__ == "__main__":
    print(entwurf(EK, "Entwurf_E_12m_Umlaufender_Vorbau_mit_Parken.pdf", "VARIANTE E · NICHT FESTGELEGT", "Variante E – 12 m und umlaufender Vorbau mit Parken (E1–E4)", "Entwurfsstudie Neue Mitte Werlte – Baufeld 3 · überarbeitet 24.10.2026 · keine Variante festgelegt", False))
    print(entwurf(FK, "Entwurf_F_EG540m2_Umlaufender_Vorbau_Parken.pdf", "VARIANTE F · NICHT FESTGELEGT", "Variante F – Erdgeschoss 540 m² (18 × 30 m) mit umlaufendem Vorbau und Parken (F1–F4)", "Entwurfsstudie Neue Mitte Werlte – Baufeld 3 · Planungsziel 540 m² Gebäude + 420 m² Restfläche · keine Variante festgelegt", True))
    print(stellplatz_pdf()); print(vergleich_pdf())
