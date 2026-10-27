"""Zwei getrennte Gesamtpräsentationen Baufeld 3: (A) Standardversion = bisheriger B3-Entwurf, unverändert; (B) Version mit überdachten Stellplätzen und größeren/mehr Wohnflächen (neue Idee, drei Rücksprung-Optionen).
Nutzt die Seitenbausteine von vergleichsstudie_ab.py (gleiche Geometrie, gleiche Renderer); nichts wird festgelegt, bestehende Dateien werden nicht überschrieben.
Ausgabe: studie_gebaeudeformen/Praesentation_A_Standard_B3.pdf und Praesentation_B_Ueberdachte_Stellplaetze_Mehr_Wohnflaeche.pdf"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import vergleichsstudie_ab as VS
from vergleichsstudie_ab import *
TA = "VARIANTE A · STANDARD B3"; TB = "VARIANTE B · MEHR WOHNFLÄCHE"
def planstand_tab():
    return [["Planstand / Quelle", "Inhalt", "Status"], ["B-Plan Nr. 123 „Ehemalige Grundschule“ (2023)", "MI 3 / Flurstück 59/1 (vermutetes Baufeld 3): II–III, GRZ 0,6, TH 9,80 m, H 15,00 m, Dach ≥ 38°, Baugrenze 10 m W / 3 m übrige; Bezug OK Fahrbahn, SH 0,30 m", "RECHTSKRÄFTIG seit 14.04.2023"],
        ["1. Änderung (Planzeichnung 25.08.2026)", "betrifft MI 3 nicht; II zwingend, TH 6,50 m, H 12,00 m, Dach ≥ 38°", "ENTWURF, nicht beschlossen"],
        ["Grundstück", "ca. 960 m² (Projektangabe); Flurstück 59/1 ≈ 42,3 × 22,7 m geschätzt; Baufenster ≈ 27,7 × 15,9 m abgeleitet", "GESCHÄTZT, nicht vermessen"],
        ["Entwurfsgrundlage", "Hypothese 32 × 30 m (960 m²), nur zum Darstellen der Entwurfsidee", "HYPOTHESE"], ["Fotos Seiten 13/15/16", "nicht angekommen; Zuordnung Baufeld 3 = MI 3 unbestätigt", "FEHLT"]]
def titel(n, tag, t, sub, aufbau):
    im, d = pg(t, sub, n, tag); table(d, 120, 290, [900, 1700, 600], planstand_tab(), 28); text_block(d, 120, 1250, 3260, aufbau, 32); return [im]
def fussabdruck(n, tag, labs):
    im, d = pg("Baufeld 3 real: Baufenster und Fußabdruck", "Flurstück 59/1 (vermutetes Baufeld 3, MI 3): ≈ 42,3 × 22,7 m geschätzt · Baufenster ≈ 27,7 × 15,9 m abgeleitet", n, tag)
    BF = ED.BF; allf = {"A: EG 32×18 (B3)": ((BF[0], BF[1], BF[0] + 32, BF[1] + 18), (180, 30, 30), (0, 0, 32, 18)), "A: 1. OG 32×21": ((BF[0], BF[1], BF[0] + 32, BF[1] + 21), (225, 120, 120), (0, 0, 32, 21)),
            "B: EG 18×30 (30 tief)": ((BF[0] + 2, 0.4, BF[0] + 20, 22.7), (140, 60, 160), (0, 0, 18, 30)), "B-Vorbau: 1. OG 24×31,5": (None, None, (0, 0, 24, 31.5))}
    foot = [(k, v[0], v[1]) for k, v in allf.items() if k in labs and v[0]]
    im2 = ED.plan_p59(2300, 1900, foot=foot); im.paste(im2, (120, 280))
    rows = [["Fußabdruck", "Baufenster 27,7 × 15,9"]] + [[k, ("passt" if ED.fits(*ED.dims([allf[k][2]])) else "passt NICHT")] for k in labs]
    cl = {(i, 1): (OK if r[1] == "passt" else BAD) for i, r in enumerate(rows) if i}; y = table(d, 2480, 300, [560, 380], rows, 24, colors=cl)
    text_block(d, 2480, y + 40, 900, "Gebäudeteile (Vorbau) dürfen die Baugrenze nicht überschreiten; für die Realisierung wären Befreiung/Planänderung oder ein anderes Baufeld nötig. Alle Maße sind Schätzungen aus dem Plan, keine Vermessung.", 25, GREY); return [im]
def auswirkung(n, tag, keys, names):
    COL = {"ok": OK, "pruef": WARN, "kritisch": BAD}
    im, d = pg("Auswirkungen nach Planstand", "Planstand 1 = rechtskräftiger Plan 2023 (MI 3) · Planstand 2 = Änderungsentwurf 2026 (für Baufeld 3 nicht einschlägig, hier als Annahme) · kein Ergebnis bedeutet baurechtliche Zulässigkeit", n, tag)
    crit = ["EG im Baufenster", "Vorbau/OG im Baufenster", "Höhe", "Vollgeschosse", "Dachform", "GRZ 0,6", "Stellplätze"]
    for bi, lab in enumerate(("PLANSTAND 1 – rechtskräftig 2023, MI 3: II–III, TH 9,80 m, H 15,00 m, Dach ≥ 38°, Baugrenze 10 m W / 3 m übrige", "PLANSTAND 2 – Entwurf 2026 (hypothetisch): II zwingend, TH 6,50 m, H 12,00 m, Dach ≥ 38°, Baugrenze 3 m")):
        rows = [["Kriterium"] + names]; cl = {}
        for ci, c in enumerate(crit, 1):
            row = [c]
            for kj, k in enumerate(keys, 1):
                s = ED.status(k)[bi][c]; txt = s[1]
                if c == "Stellplätze": txt = "11 rückseitig auf 32×30-Hypothese; auf Flurstück 59/1 nicht unterzubringen" if k == "A" else "13 auf 32×30-Hypothese; auf 59/1 nicht übertragbar"
                row.append(txt); cl[(ci, kj)] = COL[s[0]]
            rows.append(row)
        d.text((120, 290 + bi * 1000), lab, font=F(28, "SemiBold"), fill=INK); table(d, 120, 340 + bi * 1000, [520] + [(3268 - 520) // len(keys)] * len(keys), rows, 21, colors=cl)
    return [im]
def kennzahlen(n, tag, ks, names):
    im, d = pg("Kennzahlen (vorläufig)", "Wohnfläche, Wohnungen, Gewerbe, Stellplätze · Schätzungen auf Hypothese 32 × 30 m", n, tag)
    def stp_row(k): pk = PRK["AL"] if k == "A" else PRK[k]; return f"{pk['gesamt']} gez. / {pk['nutzbar']} nutzbar"
    rows = [["Kennzahl"] + names, ["Höhe Attika"] + ["+9,90 m" if k == "A" else "+12,00 m (Bezug offen)" for k in ks], ["Grundfläche EG (m²)"] + [fm(D[k]["flaeche"]["eg"]) for k in ks], ["Grundfläche 1. OG (m²)"] + [fm(D[k]["flaeche"]["og1"]) for k in ks], ["Grundfläche oberstes Geschoss (m²)"] + [fm(D[k]["flaeche"]["st"]) for k in ks],
        ["Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in ks], ["Wohnungen (Standardmix)"] + [str(D[k]["mix"]["standard"]["we"]) for k in ks], ["Wohnungsgrößen min–max / Ø (m²)"] + [f"{fm(D[k]['mix']['standard']['kleinste'])}–{fm(D[k]['mix']['standard']['groesste'])} / {fm(D[k]['mix']['standard']['mittel'])}" for k in ks],
        ["Wohnungen kleiner / größerer Mix"] + [f"{D[k]['mix']['klein']['we']} / {D[k]['mix']['gross']['we']}" for k in ks], ["Größenklassen ≤50/50–60/60–75/75–85/>85 m²"] + [classes(k) for k in ks],
        ["Gastraum (m²) ≈ Plätze innen"] + [f"{fm(VA.V[k].get('gastro_m2', 280))} ≈ {D[k]['stp']['sitze_innen']}" for k in ks], ["Terrasse/Arkade ≈ Plätze"] + [str(D[k]["stp"]["sitze_terrasse"]) for k in ks], ["Büro netto (m², Programmannahme)"] + [fm(D[k]["stp"]["buero_m2"]) for k in ks],
        ["Stellplätze gezeichnet / nutzbar"] + [stp_row(k) for k in ks], ["davon überdacht (Anteil)"] + [f"≈ {covered('AL' if k == 'A' else k)*100:.0f} %" for k in ks], ["erforderlich § 47 (Gastro+Büro; Wohnen 0)"] + [f"{fm(D[k]['stp']['erf_lo'],1)}–{fm(D[k]['stp']['erf_hi'],1)}" for k in ks],
        ["optional Wohnen 0,5–1,5 je WE"] + [f"{fm(D[k]['stp']['optional']['standard']['lo'])}–{fm(D[k]['stp']['optional']['standard']['hi'])}" for k in ks], ["Säulen"] + [("0" if k == "A" else str(D[k]["anzahl_saeulen"])) for k in ks]]
    table(d, 120, 290, [820] + [(3268 - 820) // len(ks)] * len(ks), rows, 26); return [im]
def pruef(n, tag, col):
    im, d = pg("Offene Prüfbedarfe und vorläufige Förderhinweise", "Wohnflächen, Stellplätze und Förderung sind vorläufig, bis Geometrie, Grundstück und Rechtslage geprüft sind", n, tag)
    A = col == "A"
    rows = [["Thema", "Stand / offener Punkt"],
      ["Baufenster / Baugrenzen", "EG 32 × 18 m und 1. OG 32 × 21 m passen nicht in das Baufenster von MI 3 (≈ 27,7 × 15,9 m)" if A else "EG 18 × 30 m, Vorbau und 1. OG passen nicht in das Baufenster; Vorbau über Baugrenze unzulässig"],
      ["Dachform / Traufe", "Flachdach + Staffel: Dach ≥ 38° vorgeschrieben, TH 9,80 m (Befreiung nötig)" if A else "wie bei B3: Flachdach/Staffel gegen Dach ≥ 38°; zusätzlich Wandhöhe +11,5 m > TH 9,80 m"],
      ["Höhe", "Attika +9,90 m (Bezug OK Fahrbahn unbekannt)" if A else "+12,00 m über FFB; Plan 2023 H 15,00 m, Entwurf 2026 H 12,00 m (Bezug offen)"],
      ["Stellplätze", "11 rückseitig (teilüberdacht); Nachweis Gastro/Büro 11,4–16,9 knapp" if A else "13 (8 voll überdacht, 5 Längsparker); Sackgasse, Wendebedarf; Zufahrt von Süden angenommen"],
      ["Fahrwege/Säulen", "Fahrgasse 6 m, keine Säulen" if A else "Säulenpaare 5,4 m auf Stellplatzgrenzen; Feuerwehrzufahrt unter dem Vorbau ungeklärt; zwei Säulen rückseitig nur 0,35 m auseinander"],
      ["Statik/Brandschutz", "Kragarm 3,0 m" if A else "Kragarme 1,0 / 1,5 / 5,0 m, 3 Geschosse über Stellplätzen"],
      ["Förderung (vorläufig)", f"{D['A']['mix']['standard']['we']} WE, Größenklassen {classes('A')}; NBank/KfW-Voraussetzungen offen" if A else f"{D['F1']['mix']['standard']['we']} WE, überwiegend große Wohnungen, Klassen {classes('F1')}; kleinerer Mix bei Bedarf; Mietenstufe, Gewerbeanteil offen"],
      ["Grundstück", "Hypothese 32 × 30 m; real Flurstück 59/1 ≈ 42,3 × 22,7 m (geschätzt)"]]
    table(d, 120, 290, [620, 2640], rows, 26)
    text_block(d, 120, 1450, 3260, "Fehlt: Foto Seite 13 bzw. Bestätigung, dass Baufeld 3 = MI 3 / Flurstück 59/1; amtlicher Lageplan/Vermessung; Fahrbahnhöhe der Planstraße; Auskunft der Stadt zu Befreiungen (Dach, Baugrenze, Traufhöhe), Stellplatzregelung und Stand der 1. Änderung (Entwurf).", 30, INK); return [im]
def baue_A():
    pages = []; n = 1
    def add(ps):
        nonlocal n; pages.extend(ps); n += len(ps)
    aufb = "Aufbau: 1) Kernaussagen · 2) Variante A mit 3D, Ansichten, Grundrissen, Schnitt, Lageplan mit Stellplätzen · 3) Kennzahlen · 4) Baufeld 3 real, Planstände, Prüfbedarfe. Variante A ist der bisherige B3-Entwurf, unverändert; keine Festlegung, alle Werte vorläufig."
    add(titel(n, TA, "Baufeld 3 – Variante A: Standardversion (B3)", "Präsentation 27.10.2026 · bisheriger Entwurf, unverändert · keine Festlegung · alle Werte vorläufig", aufb))
    a = D["A"]; pk = PRK["AL"]
    im, d = pg("Kernaussagen Variante A", "vorläufig · Hypothese 32 × 30 m", n, TA)
    text_block(d, 120, 300, 3260, f"• EG 32 × 18 m = 576 m²: Gastronomie (Gastraum ≈ 280 m², ≈ 120 Plätze) vorn, Büros und Kern hinten.\n• 1. OG mit 3,00 m Anbau nach hinten (ohne Stützen), zurückgesetztes Staffelgeschoss, fünf Balkone zum Platz.\n• Wohnfläche netto {fm(a['wfl'])} m², {a['mix']['standard']['we']} Wohnungen ({fm(a['mix']['standard']['kleinste'])}–{fm(a['mix']['standard']['groesste'])} m²).\n• Stellplätze: {pk['gesamt']} rückseitig, teilweise überdacht (≈ {covered('AL')*100:.0f} %); Anforderung Gastro/Büro {fm(a['stp']['erf_lo'],1)}–{fm(a['stp']['erf_hi'],1)}.\n• Attika +9,90 m über FFB EG (Höhenbezug der Stadt offen).\n• Keine Aussage zur baurechtlichen Zulässigkeit; Baufenster und Dachform sind offene Punkte.", 34); pages.append(im); n += 1
    add(page_A(n)); add(kennzahlen(n, TA, ["A"], ["A – B3 (Standard)"])); add(fussabdruck(n, TA, ["A: EG 32×18 (B3)", "A: 1. OG 32×21"])); add(auswirkung(n, TA, ["A"], ["A (B3)"])); add(pruef(n, TA, "A"))
    p = os.path.join(OUT, "Praesentation_A_Standard_B3.pdf"); save(pages, p); return p, len(pages)
def baue_B():
    pages = []; n = 1
    def add(ps):
        nonlocal n; pages.extend(ps); n += len(ps)
    aufb = "Aufbau: 1) Kernaussagen · 2) Konzept B und seine drei Rücksprung-Optionen · 3) je Option Steckbrief, Lageplan mit überdachten Stellplätzen, Grundrisse, Fassaden, Schnitt, 3D · 4) Kennzahlen, Baufeld 3 real, Planstände, Prüfbedarfe. Keine Option ist gewählt; alle Werte vorläufig."
    add(titel(n, TB, "Baufeld 3 – Variante B: überdachte Stellplätze, größere Wohnungen", "Präsentation 27.10.2026 · neue Idee EG 540 m² mit umlaufendem Vorbau · drei Optionen, keine Festlegung · alle Werte vorläufig", aufb))
    a, b0, b1, b3 = D["A"], D["F1"], D["F2"], D["F3"]
    im, d = pg("Kernaussagen Variante B", "vorläufig · Hypothese 32 × 30 m", n, TB)
    text_block(d, 120, 300, 3260, f"• EG 18 × 30 m = 540 m²; 1. OG kragt 1,0 m West, 1,5 m zum Platz und 5,0 m nach Osten aus (über die Stellplatzreihe), rückseitig kein Vorbau (Grundstücksgrenze der Hypothese).\n• Wohnfläche netto: bündig {fm(b0['wfl'])} m², Staffel 1,5 m {fm(b1['wfl'])} m², Staffel 3,0 m {fm(b3['wfl'])} m² (Referenz B3: {fm(a['wfl'])} m²).\n• Wohnungen: {b0['mix']['standard']['we']} / {b1['mix']['standard']['we']} / {b3['mix']['standard']['we']} im Standardmix, deutlich größer (bis {fm(b0['mix']['standard']['groesste'])} m²); ein kleinerer Mix ergibt mehr Wohnungen.\n• Stellplätze: 13 (8 voll überdacht, 5 Längsparker) auf der Hypothese; Zufahrt von Süden angenommen.\n• Gastraum rund 17 % kleiner als bei B3 (≈ 232 m², ≈ 99 Plätze).\n• Attika +12,00 m über FFB (hypothetisches Höhenschema, Bezug offen).\n• Offene Konflikte: Vorbau ragt 1,5 m über die Hypothese-Grenze zum Platz; zwei Säulen rückseitig nur 0,35 m auseinander; keine Aussage zur Zulässigkeit.", 34); pages.append(im); n += 1
    add(page_B_intro(n))
    for k, lab in BK: add(page_B_variant(k, lab, n))
    names = ["B bündig bis Attika", "B Staffel 1,50 m", "B Staffel 3,00 m"]
    add(kennzahlen(n, TB, ["F1", "F2", "F3"], names)); add(fussabdruck(n, TB, ["B: EG 18×30 (30 tief)", "B-Vorbau: 1. OG 24×31,5"])); add(auswirkung(n, TB, ["F1", "F2", "F3"], names)); add(pruef(n, TB, "B"))
    p = os.path.join(OUT, "Praesentation_B_Ueberdachte_Stellplaetze_Mehr_Wohnflaeche.pdf"); save(pages, p); return p, len(pages)
if __name__ == "__main__": print(baue_A()); print(baue_B())
