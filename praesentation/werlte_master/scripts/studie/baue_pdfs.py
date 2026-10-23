"""Baut die vier Varianten-PDFs und das Vergleichs-PDF der Entwurfsstudie (alles aus varianten.py + vorhandenen Bildern)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pdflib import *
import varianten as VA
OUT = os.path.join(VA.ROOT, "studie_gebaeudeformen"); D = VA.alle()
KEYS = [k for k in "ABCD" if os.path.exists(f"{OUT}/{k}/ansichten/aerial.png")]
IMG = lambda k, n: f"{OUT}/{k}/ansichten/{n}.png"; PLN = lambda k, n: f"{OUT}/{k}/plaene/{n}.png"
fm = lambda x, n=0: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
TAG = "ENTWURFSSTUDIE · NICHT FESTGELEGT"

# Baurecht-Bewertung je Variante: (Kriterium, Status ok/pruef/kritisch, Text)
def baurecht(k):
    d = D[k]; u = d["ueber_grundstueck"]; ue = max(u.values()); r = []
    r.append(("Gebäudehöhe max. 12,00 m", "ok", f"Attika +{fm(d['hoehe']['attika'],2)} m, Reserve {fm(d['hoehe']['differenz'],2)} m nicht ausgenutzt (Bezugspunkt der Höhe noch offen)."))
    r.append(("Geschosse (2–3)", "pruef", f"3 Geschosse inkl. Staffel; Staffel = {fm(d['staffel_anteil']*100)} % des 1. OG – ob Vollgeschoss (B-Plan, NBauO), ist zu klären."))
    g = d["grz_projektion"]; r.append(("GRZ / überbaute Fläche", "ok" if g <= 0.6 else ("pruef" if g <= 0.8 else "kritisch"), f"EG {fm(d['flaeche']['eg'])} m² = {fm(d['grz_eg']*100)} %; größte Geschossprojektion {fm(d['projektion_m2'])} m² = {fm(g*100)} % von 960 m². Theoretische GRZ 0,6 ist eine Annahme, keine Festsetzung."))
    r.append(("Baugrenzen / Grenzen", "ok" if ue == 0 else "kritisch", "Alle Geschosse innerhalb des hypothetischen Grundstücks 32 × 30 m." if ue == 0 else f"Obergeschoss ragt bis {fm(ue,2)} m über das hypothetische Grundstück (W/O/Platz) – Überbauung Platzfläche/Nachbargrenze, Baulast/Genehmigung erforderlich."))
    n = d["stp_bedarf"]["standard"]; r.append(("Stellplätze", "kritisch", f"Bedarf nach Ansatz ca. {fm(n,1)} (Wohnen 1,5/WE, Gastro 1/10 m², Büro 1/30 m²) gegenüber 11 nachweisbaren – Stellplatzsatzung/Ablöse klären."))
    r.append(("Gewerbe im EG", "ok", "EG-Nutzung Gastronomie/Büro wie B3 unverändert (32 × 18 m)."))
    r.append(("Brandschutz / Rettungswege", "pruef", "Staffel/OG-Auskragung, Gebäudeklasse 4/5, Rettungswege, Feuerwehrzufahrt: Konzept erforderlich."))
    return r
COL = {"ok": OK, "pruef": WARN, "kritisch": BAD}; LBL = {"ok": "voraussichtlich ok", "pruef": "zu prüfen", "kritisch": "kritisch / Abweichung"}

KONSTR = {
 "A": ("keine Stützen; 3,00 m Auskragung nach hinten (Rückseite), Staffel 0,80 m zurück", "Referenz; Auskragung rückseitig ist statisch bereits Sonderlösung (Unterzug/Kragplatte, Wärmebrücke).", "Geringste Wohnfläche der Auskragungsvarianten; Stellplätze nur teilweise überdeckt.", "Statik der Kragplatte (3,0 m), Brandschutz über Stellplätzen."),
 "B": ("24 Säulen am Rand der 1,50/3,00 m Auskragung (≈5,0 m Achsabstand, Raster R2 5,6 m passt nicht deckungsgleich)", "Umlaufende Arkade: geschützter Gehweg, klare Gestalt, Säulen reduzieren Kragarmlängen, Auskragung als Wetterschutz/Beschattung.", "Überbauung der Platzfläche und der seitlichen Grenzen um 1,5 m; Säulen im Stellplatz-/Gehwegbereich; mehr Fassaden-/Fundamentaufwand.", "Baugrenzen, Überbauung öffentlicher Raum, Fundamente Säulen, Abstandsflächen, Stützenstellung ↔ Stellplätze/Gastro."),
 "C": ("24 Säulen wie B, hinten 6,00 m Auskragung mit Mittelstützen/Unterzug erforderlich", "Größte Wohnfläche, Stellplätze vollständig überdeckt (Carport-Wirkung), mehr Wohnungen.", "Sehr hohe Ausnutzung (Projektion 93 % von 960 m²), Staffel fast so groß wie 1. OG (Baumasse, Verschattung/Nachbarn), höchster Konstruktions- und Brandschutzaufwand.", "GRZ/Überbauung, Abstandsflächen (Höhe × Tiefe), Vollgeschoss-Definition, Schallschutz, Statik 6 m Kragarm, Stellplatz-Nachweis."),
 "D": ("keine Stützen, keine Auskragung (einfaches Tragwerk)", "Einfachste, wirtschaftlichste Konstruktion; GRZ-neutral; alle Geschosse innerhalb 32 × 18 m.", "Geringste Wohnfläche; weniger attraktive Wohnungsgrößen; keine Vordach-/Arkadenwirkung.", "Vergleichsbasis; Förderlogik und Mindestgrößen."),
}

def steckbrief(k):
    d = D[k]; m = d["mix"]["standard"]
    return [["Kennzahl", "Wert (vorläufig)"],
            ["Außenmaße EG / 1. OG / Staffel", f"{d['aussenmasse']['eg'][0]:.1f} × {d['aussenmasse']['eg'][1]:.1f} / {d['aussenmasse']['og1'][0]:.1f} × {d['aussenmasse']['og1'][1]:.1f} / {d['aussenmasse']['st'][0]:.1f} × {d['aussenmasse']['st'][1]:.1f} m"],
            ["Grundfläche EG / 1. OG / Staffel", f"{fm(d['flaeche']['eg'])} / {fm(d['flaeche']['og1'])} / {fm(d['flaeche']['st'])} m²"],
            ["Summe Geschossflächen (BGF)", f"{fm(d['bgf'])} m²"],
            ["Geschätzte Wohnfläche (netto)", f"{fm(d['wfl'])} m² (1. OG {fm(m['og1']['netto'])} + Staffel {fm(m['st']['netto'])})"],
            ["Wohnungen (Standardmix)", f"{m['we']} ({m['we_og1']} im 1. OG, {m['we_st']} in der Staffel); Größen {fm(m['kleinste'])}–{fm(m['groesste'])} m², Ø {fm(m['mittel'])} m²"],
            ["Wohnungen alternativer Mix", f"klein: {d['mix']['klein']['we']} WE (Ø {fm(d['mix']['klein']['mittel'])} m²) · groß: {d['mix']['gross']['we']} WE (Ø {fm(d['mix']['gross']['mittel'])} m²)"],
            ["Säulen / Tragwerk", f"{d['anzahl_saeulen']} Säulen · {KONSTR[k][0]}"],
            ["Höhe", f"Attika +9,90 m, zulässig 12,00 m (Auftraggeber), 3 Geschosse"]]

def seite_bild(titel, sub, bilder, n, tag=TAG):
    im, d = page(); header(d, titel, sub, tag); footer(d, n)
    nb = len(bilder); gap = 60
    if nb == 4:
        w = (W - 240 - gap) // 2; h = (H - 330 - 200 - 120) // 2
        for i, (p, cap) in enumerate(bilder):
            x = 120 + (i % 2) * (w + gap); y = 300 + (i // 2) * (h + 100); d.text((x, y), cap, font=F(36, "SemiBold"), fill=INK); paste(im, p, x, y + 55, w, h)
        return im
    w = (W - 240 - gap * (nb - 1)) // nb
    for i, (p, cap) in enumerate(bilder):
        x = 120 + i * (w + gap); d.text((x, 270), cap, font=F(36, "SemiBold"), fill=INK); paste(im, p, x, 330, w, H - 330 - 260)
    return im

def variante_pdf(k):
    d = D[k]; pages = []; n = 1; nm = d["name"]; tag = f"VARIANTE {k} · NICHT FESTGELEGT"
    im, dr = page(); header(dr, nm, "Entwurfsstudie Neue Mitte Werlte – Baufeld 3 · Konzeptvariante, keine Genehmigungsplanung", tag); footer(dr, n)
    paste(im, IMG(k, "aerial"), 120, 270, 1950, 1100); dr.text((120, 1390), "Erhöhte Schrägansicht (aus dem gemeinsamen Modell der Variante)", font=F(28), fill=GREY)
    y = text_block(dr, 2130, 280, 1260, d["idee"], 34, INK, "SemiBold")
    table(dr, 2130, y + 40, [430, 830], steckbrief(k), 28)
    text_block(dr, 120, 1450, 1950, "Status: Diese Variante ist ein Vorschlag zum Vergleich. Sie ist nicht genehmigt, nicht statisch bemessen und nicht mit Behörden abgestimmt. Alle Flächen sind schematisch aus den Geschosskonturen abgeleitet (Netto = 0,88 × Bruttowohnstreifen, kalibriert an B3 = 846 m² / 16 WE), Wohnungsaufteilung ist rein schematisch.", 30, GREY)
    pages.append(im); n += 1
    pages.append(seite_bild("3D-Gesamtansicht und erhöhte Schrägansicht", nm, [(IMG(k, "persp"), "3D-Gesamtansicht (Platzseite)"), (IMG(k, "aerial"), "Erhöhte Schrägansicht")], n, tag)); n += 1
    pages.append(seite_bild("Vorder- und Rückfassade", nm + " · Ansichten orthogonal aus dem Modell", [(IMG(k, "front"), "Vorderfassade (Platzseite)"), (IMG(k, "rear"), "Rückfassade")], n, tag)); n += 1
    pages.append(seite_bild("Seitenfassaden West und Ost", nm + " · Ansichten orthogonal aus dem Modell", [(IMG(k, "west"), "Seitenfassade West"), (IMG(k, "east"), "Seitenfassade Ost")], n, tag)); n += 1
    pages.append(seite_bild("Schematische Grundrisse", nm + " · EG, 1. OG, Staffelgeschoss · Aufteilung schematisch, Himmelsrichtung unbekannt", [(PLN(k, "plan_eg"), "Erdgeschoss"), (PLN(k, "plan_og1"), "1. Obergeschoss"), (PLN(k, "plan_st"), "Staffelgeschoss")], n, tag)); n += 1
    im, dr = page(); header(dr, "Gebäudeschnitt, Konstruktion und Baurecht", nm, tag); footer(dr, n)
    paste(im, PLN(k, "schnitt"), 120, 270, 1900, 800)
    rows = [["Konstruktion / Besonderheit", KONSTR[k][0]], ["Vorteil", KONSTR[k][1]], ["Nachteil / Risiko", KONSTR[k][2]], ["Prüfbedarf Statik/Baurecht", KONSTR[k][3]]]
    table(dr, 2060, 290, [380, 950], rows, 28)
    br = [["Baurechtlicher Punkt", "Einschätzung", "Begründung (vorläufig)"]] + [[a, LBL[b], c] for a, b, c in baurecht(k)]
    col = {(i + 1, 1): COL[b] for i, (a, b, c) in enumerate(baurecht(k))}
    table(dr, 120, 1150, [520, 360, 2388], br, 26, colors=col)
    pages.append(im)
    p = f"{OUT}/Variante_{k}_{d['name'].split('–')[1].strip().split(' (')[0].replace(' ', '_').replace('ä','ae')}.pdf"; save(pages, p); return p

def vergleich_pdf():
    pages = []; n = 1; ks = KEYS
    im, d = page(); header(d, "Vergleich der Gebäudekonzepte", "Entwurfsstudie Neue Mitte Werlte – Baufeld 3 · Entscheidungsgrundlage, keine Festlegung", TAG); footer(d, n)
    y = text_block(d, 120, 280, 3200, "Zweck: Gegenüberstellung mehrerer Baukörper bei unverändertem Erdgeschoss (32 × 18 m, Gastronomie/Büro). Das bestehende Modell B3 bleibt unverändert als Referenz (Variante A). Keine Variante ist gewählt, genehmigt oder statisch geprüft.", 36)
    rows = [["", "Bestätigt (Quelle: Projektunterlagen / Auftraggeber)", "Annahme / unbestätigt (Grundstück, Baurecht)"],
            ["Grundstück", "ca. 960 m², B-Plan Nr. 123, Baufeld 3 Werlte", "Zuschnitt 32 × 30 m (Hypothese H1), Baugrenzen, Grenzabstände, Erschließung"],
            ["Höhe / Geschosse", "max. 12,00 m, 2–3 Geschosse (Bestätigung Auftraggeber); B3-Attika +9,90 m", "Bezugspunkt der Höhe; ob Staffel als Vollgeschoss zählt"],
            ["Nutzung", "Gewerbe (Gastro/Büro) im EG, Wohnen in den OG", "Stellplatznachweis (11 nachweisbar), Mischnutzungsanteil"],
            ["Flächen", "B3: 468,2 + 377,8 = 846 m² Wohnfläche, 16 WE (Planwerte)", "Alle Werte B/C/D sind aus Geschosskonturen geschätzt (0,88 × Wohnstreifen), Wohnungsaufteilung schematisch"],
            ["Idee Vorbau", "Anregung Auftraggeber/Chat: umlaufender Vorbau mit tragenden Säulen, ggf. größere Obergeschosse", "Weder Zulässigkeit noch Tragfähigkeit geprüft; ChatGPT-Chat ist reiner Kontext, kein Beleg"]]
    table(d, 120, y + 60, [480, 1350, 1370], rows, 36)
    pages.append(im); n += 1
    # Luftbilder 2x2
    im, d = page(); header(d, "Erhöhte Schrägansichten im Vergleich", "gleiche Kamera, gleiche Darstellung · Erdgeschoss in allen Varianten unverändert", TAG); footer(d, n)
    for i, k in enumerate(ks):
        x, y = 120 + (i % 2) * 1650, 270 + (i // 2) * 1000; d.text((x, y), D[k]["name"], font=F(34, "SemiBold"), fill=INK); paste(im, IMG(k, "aerial"), x, y + 55, 1600, 880)
    pages.append(im); n += 1
    pages.append(seite_bild("Grundrisse 1. Obergeschoss im Vergleich", "schematisch, gleicher Zeichenmaßstab je Plan nicht garantiert (Maße in den Plänen)", [(PLN(k, "plan_og1"), D[k]["name"].split("(")[0]) for k in ks], n)); n += 1
    pages.append(seite_bild("Gebäudeschnitte im Vergleich", "Auskragungen, Staffelung, Säulen · schematisch", [(PLN(k, "schnitt"), D[k]["name"].split("(")[0]) for k in ks], n)); n += 1
    # Tabelle Maße
    im, d = page(); header(d, "Vergleichstabelle 1: Außenmaße und Flächen", "alle Werte vorläufig (Methodik auf der letzten Seite)", TAG); footer(d, n)
    h = ["Kennzahl"] + [D[k]["name"].split(" (")[0] for k in ks]
    rows = [h,
        ["Außenmaß EG (m)"] + [f"{D[k]['aussenmasse']['eg'][0]:.1f} × {D[k]['aussenmasse']['eg'][1]:.1f}" for k in ks],
        ["Außenmaß 1. OG (m)"] + [f"{D[k]['aussenmasse']['og1'][0]:.1f} × {D[k]['aussenmasse']['og1'][1]:.1f}" for k in ks],
        ["Außenmaß Staffel (m)"] + [f"{D[k]['aussenmasse']['st'][0]:.1f} × {D[k]['aussenmasse']['st'][1]:.1f}" for k in ks],
        ["Grundfläche EG (m²)"] + [fm(D[k]["flaeche"]["eg"]) for k in ks],
        ["Grundfläche 1. OG (m²)"] + [fm(D[k]["flaeche"]["og1"]) for k in ks],
        ["Grundfläche Staffel (m²)"] + [fm(D[k]["flaeche"]["st"]) for k in ks],
        ["Summe Geschossflächen BGF (m²)"] + [fm(D[k]["bgf"]) for k in ks],
        ["Geschätzte Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in ks],
        ["Δ Wohnfläche gegenüber A"] + [("±0" if k == "A" else f"{D[k]['wfl']-D['A']['wfl']:+.0f} m² ({(D[k]['wfl']/D['A']['wfl']-1)*100:+.0f} %)") for k in ks],
        ["Größte Geschossprojektion / GRZ-Wert (Annahme 0,6)"] + [f"{fm(D[k]['projektion_m2'])} m² / {D[k]['grz_projektion']:.2f}" for k in ks],
        ["Staffelanteil am 1. OG"] + [f"{D[k]['staffel_anteil']*100:.0f} %" for k in ks],
        ["Überstand über hypoth. Grundstück (W/O/Platz/Rück)"] + [("keiner" if max(D[k]["ueber_grundstueck"].values()) == 0 else "/".join(fm(D[k]["ueber_grundstueck"][s], 1) for s in ("west", "ost", "platz", "rueck")) + " m") for k in ks]]
    cw = [1000] + [(3268 - 1000) // len(ks)] * len(ks); table(d, 120, 290, cw, rows, 38)
    pages.append(im); n += 1
    # Tabelle Wohnungen
    im, d = page(); header(d, "Vergleichstabelle 2: Wohnungen, Größen, Stützen", "Wohnungsmix schematisch; 16 WE sind in keiner Variante ein Maximum, sondern ein Ergebnis des Rasters", TAG); footer(d, n)
    rows = [h]
    for m, lab in (("standard", "Standardmix (5,6 / 7,0 m Modul, wie B3)"), ("klein", "Mix kleinere Wohnungen (4,9 / 5,6 m)"), ("gross", "Mix größere Wohnungen (7,0 / 8,4 m)")):
        rows.append([lab + " – Anzahl WE"] + [str(D[k]["mix"][m]["we"]) for k in ks])
        rows.append(["   Größen min – max (Ø), m²"] + [f"{fm(D[k]['mix'][m]['kleinste'])} – {fm(D[k]['mix'][m]['groesste'])} (Ø {fm(D[k]['mix'][m]['mittel'])})" for k in ks])
    rows.append(["Beispiel-Wohnungsgrößen (Standard)"] + [f"{fm(D[k]['mix']['standard']['kleinste'])} m² (vorn) und {fm(D[k]['mix']['standard']['groesste'])} m² (hinten)" for k in ks])
    rows.append(["Mehr als 16 WE möglich?"] + [("Ja: " + str(max(D[k]['mix'][m]['we'] for m in D[k]['mix'])) + " WE bei kleinerem Mix" if max(D[k]['mix'][m]['we'] for m in D[k]['mix']) > 16 else "nein (16 nur im Standardmix)") for k in ks])
    rows.append(["Anzahl Stützen / Besonderheit"] + [(f"{D[k]['anzahl_saeulen']} Säulen" if D[k]['anzahl_saeulen'] else "keine Stützen") for k in ks])
    rows.append(["Stellplatzbedarf (Ansatz) vs. 11 nachweisbar"] + [f"{fm(D[k]['stp_bedarf']['standard'],1)} vs. 11" for k in ks])
    table(d, 120, 290, cw, rows, 34)
    text_block(d, 120, 2000, 3200, "Hinweis: Die Wohnungszahl hängt vom Raster (Modulbreite) ab. Mehr WE heißt kleinere Wohnungen; ob kleinere oder größere Wohnungen förderlich/vermietbar sind, ist in der separaten Förder- und Marktbetrachtung zu klären (Foerderung_Variantenvergleich.pdf). Größere Wohnfläche allein garantiert keine höhere Förderung.", 30, GREY)
    pages.append(im); n += 1
    # Baurecht Ampel
    im, d = page(); header(d, "Vergleichstabelle 3: Baurechtliche Ampel (vorläufig)", "Einschätzung der Geometrie gegen die angegebenen Randbedingungen – keine rechtliche Prüfung, nichts genehmigt", TAG); footer(d, n)
    crit = [a for a, b, c in baurecht(ks[0])]; rows = [["Kriterium"] + [D[k]["name"].split(" (")[0] for k in ks]]; col = {}
    for i, cr in enumerate(crit):
        row = [cr]
        for j, k in enumerate(ks):
            a, b, c = baurecht(k)[i]; row.append(LBL[b] + ": " + c); col[(i + 1, j + 1)] = COL[b]
        rows.append(row)
    table(d, 120, 290, cw, rows, 28, colors=col)
    pages.append(im); n += 1
    # Konstruktion / Vor-Nachteile
    im, d = page(); header(d, "Konstruktion, Vor- und Nachteile, Prüfbedarf", "Statik nicht bemessen · Säulen/Kragarme sind Konzeptannahmen", TAG); footer(d, n)
    rows = [["", *[D[k]["name"].split(" (")[0] for k in ks]], ["Konstruktion"] + [KONSTR[k][0] for k in ks], ["Vorteile"] + [KONSTR[k][1] for k in ks], ["Nachteile / Risiken"] + [KONSTR[k][2] for k in ks], ["Prüfbedarf Baurecht / Statik"] + [KONSTR[k][3] for k in ks]]
    table(d, 120, 290, cw, rows, 34)
    pages.append(im); n += 1
    # indikativ Wirtschaft
    im, d = page(); header(d, "Orientierung Flächen-/Ertragswirkung (keine Wirtschaftlichkeitsrechnung)", "Annahmen aus wirtschaft/params.py (mittleres Szenario): Bauwerk 2.500 €/m² BGF, Wohnmiete 10,50 €/m² · Monat – beide unbestätigte Annahmen", TAG); footer(d, n)
    rows = [h, ["Δ BGF gegenüber A (m²)"] + [f"{D[k]['bgf']-D['A']['bgf']:+.0f}" for k in ks], ["Indikative Mehr-/Minderbaukosten Bauwerk (T€)"] + [f"{(D[k]['bgf']-D['A']['bgf'])*2.5:+.0f}" for k in ks],
            ["Δ Wohnfläche gegenüber A (m²)"] + [f"{D[k]['wfl']-D['A']['wfl']:+.0f}" for k in ks], ["Indikative Mehr-/Minderkaltmiete (€/Monat)"] + [f"{(D[k]['wfl']-D['A']['wfl'])*10.5:+,.0f}".replace(",", ".") for k in ks]]
    table(d, 120, 290, cw, rows, 38)
    text_block(d, 120, 900, 3200, "Nicht enthalten: Säulen, Kragarme, Fundamente, Außenanlagen, Brandschutz, Stellplatz-Ablöse, Förderbedingungen, Mietbindungen. Ob eine größere Fläche wirtschaftlich besser ist, entscheidet erst eine gesonderte Rechnung mit bestätigten Baukosten.", 32, GREY)
    pages.append(im); n += 1
    # Methodik / offen
    im, d = page(); header(d, "Methodik, Annahmen und offene Fragen", "Was bestätigt ist, was nur Annahme ist, was noch fehlt", TAG); footer(d, n)
    t = ("Methodik: Jede Variante ist als Rechteckvereinigung je Geschoss in scripts/studie/varianten.py definiert; Ansichten (Blender), Grundrisse, Schnitt und Kennzahlen entstehen aus diesen Daten. Wohnfläche netto = 0,88 × Bruttofläche der Wohnstreifen (Geschoss ab x = 4 m abzüglich 2,0 m Mittelgang); die Methode reproduziert B3 exakt (468,2 + 377,8 m²; 9 + 7 WE).\n\n"
         "Offene Fragen: (1) tatsächlicher Grundstückszuschnitt, Baugrenzen, Grenzabstände, Erschließung und GRZ/GFZ laut B-Plan Nr. 123; (2) Bezugspunkt der 12-m-Höhe und Definition Vollgeschoss/Staffel; (3) Zulässigkeit der Überbauung der Platzfläche/Nachbargrenzen (Vorbau/Arkade); (4) Stellplatznachweis und Ablöse; (5) Statik Kragarme und Säulenstellung, Brandschutz; (6) Himmelsrichtung/Besonnung (Orientierung Blatt 4 vs. 14/25 nicht geklärt); (7) Förderbedingungen je Variante (separate Betrachtung).\n\n"
         "Nächster Schritt: Auswahl bzw. Kombination einer oder mehrerer Varianten durch den Auftraggeber; erst danach Vertiefung (Detailmodell, Plan-Ist-Prüfung, Visualisierung). Keine Variante wurde als Standard gesetzt.")
    text_block(d, 120, 300, 3200, t, 42)
    pages.append(im)
    p = f"{OUT}/Vergleich_Gebaeudekonzepte.pdf"; save(pages, p); return p

if __name__ == "__main__":
    for k in KEYS: print(variante_pdf(k))
    print(vergleich_pdf())
