"""Entwurfs-PDF Variante E (E1–E4) und Vergleich E / B / C. Aus varianten.py, varianten_e.py, e_zeichnen.py und den Blender-Ansichten."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(__file__))
from pdflib import *
import varianten as VA, varianten_e as VE, e_zeichnen as EZ
OUT = os.path.join(VA.ROOT, "studie_gebaeudeformen"); EK = ["E1", "E2", "E3", "E4"]
fm = lambda x, n=0: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
D = {k: VA.kennzahlen(k) for k in ["A", "B", "C", "D"] + EK}
PK = {k: EZ.pruefe_parken(k) for k in EK}
TAG = "VARIANTE E · NICHT FESTGELEGT"
IMG = lambda k, n: f"{OUT}/{k}/ansichten/{n}.png"; PLN = lambda k, n: f"{OUT}/{k}/plaene/{n}.png"
def alt_parken(key):
    """B/C mit den B3-Stellplätzen (11, y 18–23, Fahrgasse dahinter) und den Säulen der Variante: Wie viele Plätze werden durch Säulen/Fahrgassenkonflikt beeinträchtigt?"""
    v = VA.V[key]; cols = D[key]["saeulen"]; st = VA.B3["parking"]["stalls"]; konf = 0; minb = 9.9
    for s in st:
        w = (s[2] - s[0]) - EZ.intrusion(s, cols); minb = min(minb, w); band = (s[0], s[3], 32, s[3] + 6.0)
        if w < 2.30 or any(EZ.seg_circle_hits_rect(c, 0.2, band) for c in cols) or any(s[1] < r[3] and s[3] > r[1] and s[0] < r[2] and s[2] > r[0] for r in v["eg"]): konf += 1
    return len(st), konf, minb
ALT = {k: alt_parken(k) for k in ("B", "C")}
def spacing(key):
    cols = D[key]["saeulen"]
    if not cols: return "–"
    xs = sorted({round(c[0], 2) for c in cols if abs(c[1] - max(c2[1] for c2 in cols)) < 0.01}); gaps = [b - a for a, b in zip(xs, xs[1:])]
    return f"{min(gaps):.1f}–{max(gaps):.1f} m (Rückseite)"
def ampel(k):
    d = D[k]; v = VA.V[k]; r = []
    ov = EZ.over_plot(k); mx = max(ov.values())
    r.append(("Gebäudehöhe max. 12,00 m", "pruef", f"Attika +{fm(d['hoehe']['attika'],2)} m = Grenzwert, Reserve {fm(d['hoehe']['differenz'],2)} m; Höhenbezug der Stadt unbelegt, Aufzugsüberfahrt/Dachaufbauten zusätzlich." if d['hoehe']['differenz'] < 0.5 else f"Attika +{fm(d['hoehe']['attika'],2)} m, Reserve {fm(d['hoehe']['differenz'],2)} m."))
    r.append(("Geschosse (2–3)", "pruef", f"3 Geschosse; 2. OG = {fm(d['staffel_anteil']*100)} % des 1. OG – Vollgeschoss-Frage (NBauO/B-Plan) klären. Traufhöhe 6,50 m (project_brief) bei +7,90 m Vorbau-Oberkante prüfen."))
    g = d["grz_projektion"]; r.append(("GRZ / überdeckte Fläche", "ok" if g <= 0.6 else ("pruef" if g <= 0.8 else "kritisch"), f"Größte Geschossprojektion {fm(d['projektion_m2'])} m² = {fm(g*100)} % von 960 m² (theoretisch GRZ 0,6 = 576 m², Kappung 0,8 angenommen; Anrechnung überdeckter Stellplätze ungeklärt)."))
    r.append(("Baugrenzen / Grundstücksgrenzen", "kritisch" if mx > 0 else "pruef", ("Überstand " + fm(mx, 2) + " m über H1.") if mx > 0 else f"Außenkante der Obergeschosse liegt auf der angenommenen Grenze (0,00 m Überstand), Säulen 0,35 m innen; {EZ.abstand_szenario(k,3.0):.0f} m² (3 m) bzw. {EZ.abstand_szenario(k,6.0):.0f} m² (6 m) des 1. OG lägen im Abstandsszenario – Baugrenze/Abstandsflächen/Grenzbebauung ungeklärt."))
    r.append(("Stellplätze", "kritisch", f"{PK[k]['stellplaetze']} Plätze gezeichnet gegenüber Bedarf ca. {fm(d['stp_bedarf']['standard'],1)} – Defizit {fm(d['stp_bedarf']['standard']-PK[k]['stellplaetze'],1)}; Ablöse/Tiefgarage/Nachbarfläche zu klären."))
    r.append(("Gewerbe im EG", "pruef", f"EG {fm(d['flaeche']['eg'])} m² statt 576 m² bei B3 ({fm(d['flaeche']['eg']-576)} m²); Gastro-/Büro-Programm anpassen."))
    r.append(("Brandschutz / Rettungswege", "pruef", "Vorbau über Stellplätzen/Fahrgasse, Feuerwehrzufahrt und Aufstellflächen, Gebäudeklasse 4/5 – Konzept erforderlich."))
    return r
COL_ = {"ok": OK, "pruef": WARN, "kritisch": BAD}; LBL = {"ok": "voraussichtlich ok", "pruef": "zu prüfen", "kritisch": "kritisch / offen"}
def kenn_rows(k):
    d = D[k]; m = d["mix"]["standard"]; pk = PK[k]; ov = EZ.over_plot(k)
    return [["Kennzahl", "Wert (vorläufig)"],
        ["Höhe", "12,00 m Attika (EG 4,30 · 1. OG 3,60 · 2. OG 3,60 · Dach/Attika 0,50 m), 3 Geschosse"],
        ["Grundfläche EG / 1. OG / 2. OG", f"{fm(d['flaeche']['eg'])} / {fm(d['flaeche']['og1'])} / {fm(d['flaeche']['st'])} m²"],
        ["Außenmaße EG / 1. OG / 2. OG", f"{d['aussenmasse']['eg'][0]:.1f} × {d['aussenmasse']['eg'][1]:.1f} / {d['aussenmasse']['og1'][0]:.1f} × {d['aussenmasse']['og1'][1]:.1f} / {d['aussenmasse']['st'][0]:.1f} × {d['aussenmasse']['st'][1]:.1f} m"],
        ["Wohnfläche netto (geschätzt)", f"{fm(d['wfl'])} m² (1. OG {fm(m['og1']['netto'])} + 2. OG {fm(m['st']['netto'])})"],
        ["Wohnungen (Standardmix)", f"{m['we']} WE ({m['we_og1']} + {m['we_st']}), {fm(m['kleinste'])}–{fm(m['groesste'])} m², Ø {fm(m['mittel'])} m²"],
        ["Wohnungen anderer Mix", f"klein {d['mix']['klein']['we']} WE (Ø {fm(d['mix']['klein']['mittel'])} m²) · groß {d['mix']['gross']['we']} WE (Ø {fm(d['mix']['gross']['mittel'])} m²)"],
        ["Säulen", f"{d['anzahl_saeulen']} Säulen Ø 0,40 m, Raster Rückseite 5,0 m (= 2 Stellplätze)"],
        ["Stellplätze", f"{pk['stellplaetze']} (Reihe 1: {pk['reihe1']}, Reihe 2: {pk['reihe2']}); Bedarf ca. {fm(d['stp_bedarf']['standard'],1)}"],
        ["Ein-/Ausfahren (geometrisch)", "alle Plätze frei erreichbar" if pk["ok"] else "Konflikte: " + str(pk["fehler"])],
        ["Überstand über Grundstück H1", f"{fm(max(ov.values()),2)} m (Außenkante OG auf Grenze)"]]
def page_with(title, sub, n, tag=TAG):
    im, d = page(); header(d, title, sub, tag); footer(d, n); return im, d
def pages_for(k, n):
    d = D[k]; v = VA.V[k]; pages = []
    im, dr = page_with(v["name"], "Entwurfsstudie Baufeld 3 · Konzeptvariante, keine Genehmigungsplanung", n, f"{k} · NICHT FESTGELEGT"); paste(im, IMG(k, "aerial"), 120, 270, 1950, 1100)
    y = text_block(dr, 2130, 280, 1260, v["idee"], 32, INK, "SemiBold"); table(dr, 2130, y + 30, [400, 860], kenn_rows(k), 25)
    text_block(dr, 120, 1420, 1950, "Alle Maße sind Planungsannahmen: Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m, Säule Ø 0,40 m, Grundstück 32 × 30 m (Hypothese, tatsächlicher Zuschnitt unbestätigt), Zufahrt von Osten (Annahme). Wohnfläche = 0,88 × Wohnstreifen, schematisch. Nichts ist genehmigt, bemessen oder abgestimmt.", 28, GREY); pages.append(im); n += 1
    im, dr = page_with(f"{k}: Lageplan mit Gebäude, Säulen, Zufahrt und Stellplätzen", v["name"], n, f"{k} · NICHT FESTGELEGT"); paste(im, PLN(k, "lageplan"), 120, 260, 2300, 2000)
    pk = PK[k]; t = [["Parkprüfung", ""], ["Stellplätze", str(pk["stellplaetze"])], ["Ein-/Ausfahren", "frei" if pk["ok"] else "Konflikte"], ["Fahrgasse", "6,00 m (Annahme)"], ["Min. Nutzbreite mit Säule", f"{pk['min_nutzbreite']:.2f} m"], ["Überstand H1", f"{fm(max(EZ.over_plot(k).values()),2)} m"]]
    y = table(dr, 2480, 300, [520, 400], t, 28); text_block(dr, 2480, y + 30, 900, "\n".join("• " + h for h in pk["hinweise"]), 24, GREY); pages.append(im); n += 1
    pages.append(seite3([(PLN(k, "plan_eg"), "Erdgeschoss"), (PLN(k, "plan_og1"), "1. Obergeschoss"), (PLN(k, "plan_st"), "2. Obergeschoss")], f"{k}: Grundrisse EG, 1. OG, 2. OG", v["name"] + " · schematisch", n, k)); n += 1
    im, dr = page_with(f"{k}: vier Fassaden", v["name"] + " · orthogonale Ansichten aus dem 3D-Modell", n, f"{k} · NICHT FESTGELEGT")
    w = (W - 240 - 60) // 2; h = (H - 330 - 130) // 2
    for i, (nm, cap) in enumerate((("front", "Vorderfassade (Platzseite)"), ("rear", "Rückfassade (Stellplatzseite)"), ("west", "Seitenfassade West"), ("east", "Seitenfassade Ost"))):
        x = 120 + (i % 2) * (w + 60); y = 280 + (i // 2) * (h + 70); dr.text((x, y), cap, font=F(34, "SemiBold"), fill=INK); paste(im, IMG(k, nm), x, y + 50, w, h)
    pages.append(im); n += 1
    im, dr = page_with(f"{k}: Gebäudeschnitt mit Geschosshöhen und 3D-Ansicht", v["name"], n, f"{k} · NICHT FESTGELEGT"); paste(im, PLN(k, "schnitt"), 120, 270, 2250, 1200); paste(im, IMG(k, "persp"), 120, 1520, 1500, 800); paste(im, IMG(k, "aerial"), 1700, 1520, 1500, 800); pages.append(im)
    return pages
def seite3(bilder, titel, sub, n, k):
    im, d = page_with(titel, sub, n, f"{k} · NICHT FESTGELEGT"); gap = 60; w = (W - 240 - gap * 2) // 3
    for i, (p, cap) in enumerate(bilder):
        x = 120 + i * (w + gap); d.text((x, 270), cap, font=F(36, "SemiBold"), fill=INK); paste(im, p, x, 330, w, H - 330 - 200)
    return im
def hoehen_seite(n):
    im, d = page_with("Höhenrahmen: B3 (+9,90 m) gegen 12,00 m", "Schnittschema, Höhenbezug und Raumhöhen · alle Höhen vorläufig", n)
    base = 2000; sc = 135  # px je m
    def col(x, levels, title, note):
        d.text((x, 270), title, font=F(34, "SemiBold"), fill=INK)
        for (z0, z1, lab, c) in levels:
            d.rectangle([x, base - z1 * sc, x + 520, base - z0 * sc], fill=c, outline=INK, width=3); d.text((x + 16, base - (z0 + z1) / 2 * sc - 14), lab, font=F(26), fill=INK)
        d.text((x, base + 20), note, font=F(24), fill=GREY)
    col(150, [(0, 3.5, "EG 3,50 m", (245, 245, 245)), (3.5, 6.5, "1. OG 3,00 m", (252, 240, 232)), (6.5, 9.6, "Staffel 3,10 m", (252, 246, 236)), (9.6, 9.9, "", (130, 130, 135))], "B3 / A–D (bisher)", "Attika +9,90 m · Reserve 2,10 m")
    col(950, [(0, 4.3, "EG 4,30 m (lichte ≈ 3,85)", (245, 245, 245)), (4.3, 7.9, "1. OG 3,60 m (lichte ≈ 3,15)", (252, 240, 232)), (7.9, 11.5, "2. OG 3,60 m (lichte ≈ 3,15)", (252, 246, 236)), (11.5, 12.0, "", (130, 130, 135))], "E1–E4 (Höhenschema H12)", "Attika +12,00 m · Reserve 0,00 m")
    d.line([(100, base - 12 * sc), (1600, base - 12 * sc)], fill=OK, width=4); d.text((130, base - 12 * sc - 40), "+12,00 m zulässige Höhe (Auftraggeber, B-Plan-Entwurf S. 15 laut Unterlagen)", font=F(26, "SemiBold"), fill=OK)
    rows = [["Aspekt", "Aussage / Annahme"], ["Höhenbezug", "±0,00 = OK Fertigfußboden Erdgeschoss (Bezug Blatt 14). Der Bezugspunkt der Stadt für „12,00 m“ (Gelände, Straßenhöhe, OK Platz) ist NICHT belegt – Differenz zwischen FFB und Gelände unbekannt."], ["Nutzung der 2,10 m", "Statt eines vierten Geschosses (nicht angenommen, nach B-Plan max. drei) fließen die 2,10 m in größere Geschosshöhen: EG +0,80 m (Gastro, Stützweite/Technik), je Wohngeschoss +0,60 m (lichte Höhe ≈ 3,15 statt ≈ 2,65 m: großzügigere Räume, Galerie-/Hochbett-Optionen, bessere Belichtung)."], ["Folge für Wohnfläche", "Keine direkte: Fläche entsteht aus der Grundfläche, nicht aus der Höhe. Höhere Geschosse erhöhen Baukosten und Fassadenfläche; Wohnfläche steigt nur über größere Obergeschosse (Vorbau)."], ["Reserve", "Mit Attika = 12,00 m keine Reserve für Aufzugsüberfahrt, Absturzsicherung, Technikaufbauten oder Messtoleranz. Alternative: Attika bei +11,50 m (Geschosse 4,10/3,45/3,45) lässt 0,50 m Reserve."], ["Offen", "Traufhöhe 6,50 m laut project_brief (festgesetzt?) gegen +7,90 m Oberkante 1. OG; Definition Vollgeschoss/Staffelgeschoss; Dachform; ob Attika/Brüstung zur Gebäudehöhe zählt."]]
    table(d, 1750, 300, [330, 1350], rows, 25); return im
def intro(n):
    pages = []
    im, d = page_with("Variante E – 12 m und umlaufender Vorbau mit Parken", "Entwurfsstudie Neue Mitte Werlte – Baufeld 3 · Ergänzung der Variantenstudie · keine Variante festgelegt", n)
    y = text_block(d, 120, 280, 3260, "Ziel: Gebäudehöhe bis 12,00 m planerisch ausnutzen (drei Geschosse, keine zusätzlichen), oberen Geschosse auf allen vier Seiten über das Erdgeschoss auskragen und von Säulen tragen lassen, die Flächen unter und neben dem Vorbau für Zufahrt, Fahrgasse und Stellplätze nutzen. Vier Teilvarianten zeigen unterschiedliche Staffelrücksprünge (E1 bis Attika, E2 1,50 m, E3 3,00 m) und ein zweireihiges Parkkonzept (E4).", 36)
    rows = [["", "Bestätigt (Quelle)", "Annahme / unbestätigt"], ["Grundstück", "ca. 960 m², B-Plan Nr. 123, Baufeld 3, Mischgebiet", "ZUSCHNITT 32 × 30 m = Hypothese H1. Der tatsächliche Zuschnitt aus den städtischen Unterlagen liegt in den Projektdateien NICHT vor (nur Fotos im ChatGPT-Chat). Baugrenzen, Abstände, Erschließungsstraße unbekannt."], ["Höhe / Geschosse", "max. 12,00 m und 2–3 Geschosse (Auftraggeber, B-Plan-Entwurf)", "Höhenbezug; Traufhöhe 6,50 m; Vollgeschoss-Definition"], ["Stellplatz/Gasse", "–", "2,50 × 5,00 m und 6,00 m (Auftraggeber als vorläufige Annahme), Säule Ø 0,40 m, Zufahrt von Osten"], ["Wohnfläche", "B3: 846 m², 16 WE (Plan)", "E: aus Geschosskonturen geschätzt, 0,88 × Wohnstreifen"], ["Realisierbarkeit", "–", "Zusätzliche Flächen gelten erst als realisierbar, wenn Grundstück, Baugrenzen und Baurecht geprüft sind."]]
    table(d, 120, y + 60, [380, 1100, 1780], rows, 30); pages.append(im); n += 1
    pages.append(hoehen_seite(n)); n += 1
    im, d = page_with("Benötigte Unterlagen für das reale Grundstück", "Ohne diese Angaben bleibt der Lageplan eine Annahme", n)
    t = ("1. Planzeichnung des Bebauungsplans Nr. 123 (Seite 15 der städtischen Unterlagen) als PDF oder hochaufgelöstes Bild, mit Maßstab bzw. Maßketten.\n2. Zuschnitt von Baufeld 3: Eckkoordinaten oder Maße der Grenzen (Flurstück/Liegenschaftskarte), Fläche 960 m² verifizieren.\n3. Baugrenzen/Baulinien, Bauweise, Grundflächenzahl, Geschossigkeit, Höhenbezugspunkt, Traufhöhe, Dachform, Festsetzungen zu Stellplätzen.\n4. Lage der Erschließungsstraße(n), Zufahrtsverbote/-bereiche, Verlauf des Platzes (Platzseite), Gehwege, Nachbargrundstücke.\n5. Stellplatzsatzung der Gemeinde (Anzahl je WE/Gewerbe, Ablöse) und ggf. Gestaltungssatzung.\n\nSobald diese Daten vorliegen, wird der Zuschnitt in varianten_e.py (PLOT_POLY) ersetzt; Lageplan, Stellplatzprüfung und Überstandsprüfung rechnen neu.\n\nAbgleich im Projekt: Die B3-Pläne nehmen dieselbe Hypothese (32 × 30 m, 11 Stellplätze y 18–23) an; sie ist nirgends mit einem Originalmaß belegt.")
    text_block(d, 120, 300, 3200, t, 38); pages.append(im); n += 1
    im, d = page_with("Überblick E1–E4", "Standardmix · vorläufige Werte · Referenz B3 (A)", n)
    h = ["Kennzahl", "A Referenz B3"] + [VA.V[k]["name"].split(" – ")[0] + " – " + VA.V[k]["name"].split(" – ")[1] for k in EK]
    ks = ["A"] + EK
    rows = [h, ["Staffelrücksprung", "0,8 m"] + [f"{VA.V[k]['staffel_ruecksprung']:.1f} m" for k in EK],
        ["Grundfläche EG / 1. OG / 2. OG (m²)"] + [f"{fm(D[k]['flaeche']['eg'])} / {fm(D[k]['flaeche']['og1'])} / {fm(D[k]['flaeche']['st'])}" for k in ks],
        ["Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in ks], ["Δ Wohnfläche gg. A"] + ["±0"] + [f"{D[k]['wfl']-D['A']['wfl']:+.0f} m² ({(D[k]['wfl']/D['A']['wfl']-1)*100:+.0f} %)" for k in EK],
        ["Wohnungen (Standardmix)"] + [str(D[k]["we"]) for k in ks], ["Stellplätze gezeichnet"] + ["11"] + [str(PK[k]["stellplaetze"]) for k in EK], ["Stellplatzbedarf (Ansatz)"] + [fm(D[k]["stp_bedarf"]["standard"], 1) for k in ks], ["Säulen"] + ["0"] + [str(D[k]["anzahl_saeulen"]) for k in EK], ["Höhe Attika"] + ["9,90 m"] + ["12,00 m"] * 4]
    cw = [800] + [(3268 - 800) // 5] * 5; table(d, 120, 290, cw, rows, 30)
    text_block(d, 120, 1500, 3260, "Befund: Der umlaufende Vorbau bringt gegenüber B3 bis zu +238 m² Wohnfläche (E1), kostet aber 84 m² Gewerbefläche im EG und erreicht mit dem 32-m-breiten Grundstück nur 10 Stellplätze (E1–E3) bzw. 22 (E4, zweireihig, mit nur 358 m² EG). Der Stellplatzbedarf von rund 50 bleibt in jedem Fall weit unterschritten. Zahlen sind Annahmen auf hypothetischem Grundstück.", 34); pages.append(im)
    return pages
def abschluss(n):
    pages = []
    im, d = page_with("Baurechtliche Ampel E1–E4 (vorläufig)", "Keine Rechtsprüfung · alles bis zur Klärung von Grundstück, Baugrenzen und Satzungen offen", n)
    crit = [a for a, b, c in ampel("E1")]; rows = [["Kriterium"] + EK]; col = {}
    for i, cr in enumerate(crit):
        row = [cr]
        for j, k in enumerate(EK): a, b, c = ampel(k)[i]; row.append(LBL[b] + ": " + c); col[(i + 1, j + 1)] = COL_[b]
        rows.append(row)
    table(d, 120, 290, [600] + [667] * 4, rows, 22, colors=col); pages.append(im); n += 1
    im, d = page_with("Offene Fragen und Prüfbedarf", "Was vor jeder Weiterentwicklung geklärt werden muss", n)
    t = ("• Tatsächlicher Grundstückszuschnitt, Baugrenzen, Abstandsflächen (bei 12 m Höhe: Grundregel 0,5 H = 6 m, ggf. reduziert), Grenzbebauung/Baulast.\n• Höhenbezugspunkt der 12,00 m; Traufhöhe 6,50 m; Dachform; Vollgeschoss-Definition für das 2. OG (E3: 61 % des 1. OG).\n• GRZ und Anrechnung überdeckter Stellplätze/Fahrgasse (Kappungsgrenze 0,8 angenommen); E1–E3 liegen exakt bei 768 m² = 0,80.\n• Stellplatzbedarf ≈ 50 (Ansatz 1,5/WE, Gastro 1/10 m², Büro 1/30 m²) gegenüber 10–22: Satzung, Ablöse, Tiefgarage, Mitbenutzung öffentlicher Parkplätze.\n• Zufahrt: Lage der Straße, Gefälle, Sichtdreiecke, Feuerwehrzufahrt/Aufstellflächen unter dem Vorbau.\n• Statik: Kragarme 1,50 m (Arkade vorn), 2,50 m (Seiten), 5,00 m (hinten), Säulenraster 5,0 m, Fundamente, Auskragung bei drei Geschossen (Lasten aus 2 Wohngeschossen).\n• Brandschutz: Vorbau über Stellplätzen/Fahrgasse, Rettungswege, Geschosshöhen > 7 m OK Fußboden prüfen (Gebäudeklasse).\n• Gewerbe-EG schrumpft (492 bzw. 358 m² statt 576 m²): Gastro-/Büro-Programm und Pachtertrag neu bewerten.\n• Förderung: nicht neu bewertet; Wohnungsgrößen s. Förder-PDF der Variantenstudie.\n\nNächster Schritt: Unterlagen zum Grundstück (siehe Seite „Benötigte Unterlagen“) bereitstellen; danach Auswahl bzw. Kombination der Teilvarianten durch den Auftraggeber. Keine Variante ist ausgewählt.")
    text_block(d, 120, 300, 3200, t, 34); pages.append(im); return pages
def entwurf_pdf():
    pages = intro(1); n = len(pages) + 1
    for k in EK:
        ps = pages_for(k, n); pages += ps; n += len(ps)
    pages += abschluss(n); p = f"{OUT}/Entwurf_E_12m_Umlaufender_Vorbau_mit_Parken.pdf"; save(pages, p); return p
def vergleich_pdf():
    ks = ["B", "C"] + EK; pages = []; n = 1
    im, d = page_with("Vergleich E mit B und C", "Wohnfläche, Wohnungsgrößen, Stellplätze, Säulenraster, offene Fragen · alle Werte vorläufig · Referenz A = B3", n)
    h = ["Kennzahl", "A B3"] + [VA.V[k]["name"].split(" – ")[0] if k in ("B", "C") else VA.V[k]["name"].split(" – ")[0] for k in ks]
    allk = ["A"] + ks
    def stp(k): return str(PK[k]["stellplaetze"]) if k in EK else ("11" if k == "A" else f"{ALT[k][0]} (davon {ALT[k][1]} mit Konflikt)")
    rows = [h,
      ["Höhe Attika"] + ["9,90 m", "9,90 m", "9,90 m"] + ["12,00 m"] * 4,
      ["Auskragung vorn / seitlich / hinten"] + ["0 / 0 / 3,0"] + ["1,5 / 1,5 / 3,0", "1,5 / 1,5 / 6,0"] + ["1,5 / 2,5 / 5,0"] * 3 + ["1,5 / 2,5 / 5,0"],
      ["Grundfläche EG (m²)"] + [fm(D[k]["flaeche"]["eg"]) for k in allk],
      ["Grundfläche 1. OG / 2. OG (m²)"] + [f"{fm(D[k]['flaeche']['og1'])} / {fm(D[k]['flaeche']['st'])}" for k in allk],
      ["Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in allk],
      ["Δ Wohnfläche gg. A"] + ["±0"] + [f"{D[k]['wfl']-D['A']['wfl']:+.0f}" for k in ks],
      ["Wohnungen / Größen min–max (Ø), Standardmix"] + [f"{D[k]['mix']['standard']['we']} WE · {fm(D[k]['mix']['standard']['kleinste'])}–{fm(D[k]['mix']['standard']['groesste'])} (Ø {fm(D[k]['mix']['standard']['mittel'])})" for k in allk],
      ["WE bei kleinerem Mix / größerem Mix"] + [f"{D[k]['mix']['klein']['we']} / {D[k]['mix']['gross']['we']}" for k in allk],
      ["Stellplätze gezeichnet"] + [stp(k) for k in allk],
      ["Stellplatzbedarf (Ansatz)"] + [fm(D[k]["stp_bedarf"]["standard"], 1) for k in allk],
      ["Säulenanzahl / Raster"] + ["0 / –"] + [f"{D[k]['anzahl_saeulen']} / {spacing(k)}" for k in ks],
      ["Säulen im Stellplatzbereich"] + ["–", f"Raster 5,6 m ≠ Stellplatz 2,5 m: {ALT['B'][1]} von {ALT['B'][0]} Plätzen betroffen", f"{ALT['C'][1]} von {ALT['C'][0]} Plätzen betroffen (Säulen in Fahrgasse)"] + ["Säulen auf Stellplatzgrenze (Raster 5,0 m), min. Nutzbreite 2,33 m"] * 4,
      ["Überstand über H1 (W/O/Platz)"] + ["0"] + ["1,5 m", "1,5 m"] + ["0,0 m (Außenkante auf Grenze)"] * 4,
      ["1. OG-Fläche im 3-m-Randstreifen der Hypothese (m², ungeprüft)"] + [fm(EZ.abstand_szenario(k, 3.0)) for k in allk],
      ["Offene baurechtliche Fragen"] + ["Baugrenze hinten (3 m Anbau), Höhenbezug"] + ["Überbauung Platz/Nachbarn 1,5 m, GRZ 0,82, Stellplatz-Raster", "Überbauung 1,5 m, GRZ 0,93, 6 m Kragarm, Abstandsflächen"] + ["Höhe 12,00 m ohne Reserve, Grenzabstand/Baugrenze, GRZ 0,80 (Kappung), Stellplatzdefizit, Gewerbefläche −84 m²"] * 3 + ["Höhe 12,00 m ohne Reserve, Grenzabstand/Baugrenze, Gewerbefläche −219 m², Stellplatzdefizit"]]
    cw = [820] + [(3268 - 820) // 7] * 7; table(d, 120, 280, cw, rows, 22); pages.append(im); n += 1
    im, d = page_with("Einordnung des Vergleichs", "Was die Zahlen zeigen – und was nicht", n)
    t = ("• Wohnfläche: E1 (Vorbau bis Attika) bringt gegenüber B3 +238 m² (+28 %), liegt aber nur 121 m² über B (963 m²) und unter C (1.159 m²). C erreicht seine Fläche über 6 m Kragarm und 93 % Grundstücksausnutzung; E bleibt innerhalb der angenommenen Grenzen. E3/E4 liegen nahe an B3 bzw. darunter.\n• Höhe: Die 12,00 m werden in E in Geschosshöhen (nicht in ein 4. Geschoss) investiert: bessere Raumhöhen, aber höhere Baukosten und keine Reserve.\n• Parken: Der Vorbau bringt keine zusätzlichen Plätze, solange die Fahrgasse (6 m) und eine Reihe (5 m) die Grundstückstiefe belegen: 10 Plätze (E1–E3) liegen unter B3 (11). Zweireihig (E4) sind 22 Plätze möglich, dann schrumpft das EG auf 358 m² und die Wohnfläche auf 727 m² (unter B3).\n• Säulenraster: In B und C passt das Wohnraster (5,6 m) nicht zum Stellplatzraster; in E ist es auf 5,0 m = 2 Stellplätze abgestimmt.\n• Grundstück: Alle Aussagen gelten für das hypothetische Rechteck 32 × 30 m. Die Außenkante der Obergeschosse in E liegt exakt auf der Grenze – mit realen Baugrenzen/Abständen ist das nicht zulässig; die Flächen sind daher Obergrenzen („Hüllkurve“), keine realisierbaren Werte.\n• Wirtschaftlichkeit: nicht gerechnet; zusätzliche Geschossflächen und höhere Geschosse verursachen Mehrkosten (Annahme 2.500 €/m² BGF), Säulen, Kragarme und Stellplatz-Ablöse sind darin nicht enthalten.")
    text_block(d, 120, 300, 3200, t, 34); pages.append(im)
    p = f"{OUT}/Vergleich_E_mit_B_und_C.pdf"; save(pages, p); return p
if __name__ == "__main__": print(entwurf_pdf()); print(vergleich_pdf())
