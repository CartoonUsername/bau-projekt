"""Vergleichsstudie Baufeld 3: Variante A (bisheriger B3-Entwurf, unveränderte Referenz) gegen Variante B (neue Idee: EG 540 m², größere Obergeschosse, umlaufender säulengestützter Vorbau mit überdachten Stellplätzen).
Variante B wird mit drei Rücksprung-Optionen gezeigt (bündig bis Attika / Staffel 1,5 m / Staffel 3,0 m) = interne Modelle F1–F3. Nichts wird festgelegt; alle Werte vorläufig.
Ausgabe: studie_gebaeudeformen/Vergleichsstudie_A_B3_gegen_B_Neue_Idee.pdf (neue Datei, keine bestehende PDF wird überschrieben)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pdflib import *
import varianten as VA, parken as PK, e_zeichnen as EZ, entscheidung_pdf as ED, baue_pdfs_ef as EF
OUT = EF.OUT; fm = EF.fm; D = EF.D
BK = [("F1", "B · bündig bis Attika"), ("F2", "B · Staffel 1,50 m"), ("F3", "B · Staffel 3,00 m")]
TAG = "VERGLEICHSSTUDIE · NICHTS FESTGELEGT"; TAGA = "VARIANTE A · BISHERIGER ENTWURF B3 (REFERENZ)"; TAGB = "VARIANTE B · NEUE IDEE"
# Lageplan-Variante für A: B3-Stellplätze (11, rückseitig) auf der Hypothese 32 × 30 m, unveränderte B3-Geometrie
VA.V["AL"] = dict(VA.V["A"], saeulen_pts=[], stalls_row1=[tuple(s) for s in VA.B3["parking"]["stalls"]], stalls_row2=[], stalls_par=[], stall_face={"row1": "S"}, stalls=[tuple(s) for s in VA.B3["parking"]["stalls"]], fahrgasse=(0, 23.0, 32, 29.0), zufahrt=(32.0, 23.0, 32.0, 29.0), zufahrt_dir="E", eingaenge=[("Kern/Wohnzugang", (0.0, 0.0, 4.0, 1.5)), ("Gastro-Eingang (Terrasse)", (8.0, 0.0, 14.0, 1.5))], staffel_ruecksprung=0.8, kurz="A – Referenz B3")
PRK = EF.PRK; PRK["AL"] = PK.pruefe("AL")
def covered(k):
    v = VA.V[k]; ov = v["og1"]; tot = cov = 0.0
    for s in PK.stall_list(v):
        r = s["rect"]; a = (r[2] - r[0]) * (r[3] - r[1]); c = 0.0
        for o in ov: c += max(0, min(r[2], o[2]) - max(r[0], o[0])) * max(0, min(r[3], o[3]) - max(r[1], o[1]))
        tot += a; cov += min(c, a)
    return cov / tot if tot else 0.0
def classes(k):
    m = D[k]["mix"]["standard"]; u = m["og1"]["vorn"] + m["og1"]["hinten"] + m["st"]["vorn"] + m["st"]["hinten"]
    return "/".join(str(x) for x in (sum(a <= 50 for a in u), sum(50 < a <= 60 for a in u), sum(60 < a <= 75 for a in u), sum(75 < a <= 85 for a in u), sum(a > 85 for a in u)))
def pg(t, s, n, tag): im, d = page(); header(d, t, s, tag); footer(d, n); return im, d
def kenn_A():
    d = D["A"]; m = d["mix"]["standard"]; s = d["stp"]; pk = PRK["AL"]
    return [["Kennzahl", "Wert (vorläufig)"], ["Höhe", "Attika +9,90 m über FFB EG, 3 Geschosse (EG 3,50 / 1. OG 3,00 / Staffel 3,10 m)"], ["Grundfläche EG / 1. OG / Staffel", f"{fm(d['flaeche']['eg'])} / {fm(d['flaeche']['og1'])} / {fm(d['flaeche']['st'])} m²"],
        ["Außenmaße EG / 1. OG", "32,0 × 18,0 m / 32,0 × 21,0 m (1. OG 3,00 m nach hinten, ohne Stützen)"], ["Wohnfläche netto", f"{fm(d['wfl'])} m² (Plan B3: 468,2 + 377,8)"], ["Wohnungen", f"{m['we']} WE (9 + 7), {fm(m['kleinste'])}–{fm(m['groesste'])} m², Ø {fm(m['mittel'])} m²"],
        ["Gewerbe", f"EG 576 m²: Gastronomie 440 m² brutto (Gastraum ≈ 280 m², ≈ 120 Plätze), Büro 64 m² brutto/56 m² netto im hinteren Bereich, Terrasse ≈ 44 Plätze"], ["Balkone / Staffel", "5 Balkone zum Platz; Staffelgeschoss 0,80 m zurückgesetzt, Dachterrasse hinten"],
        ["Stellplätze", f"{pk['gesamt']} rückseitig (2,50 × 5,00 m), {pk['voll']} voll nutzbar; davon ≈ {covered('AL')*100:.0f} % überdacht (Auskragung 3,00 m über 5,00 m Tiefe)"], ["erforderlich (§ 47 NBauO)", f"{fm(s['erf_lo'],1)}–{fm(s['erf_hi'],1)} (Gastro + Büro; Wohnen 0)"]]
def page_A(n):
    pages = []
    im, d = pg("Variante A – bisheriger B3-Entwurf (unveränderte Referenz)", "Darstellung aus den B3-Geometriedaten (geometry/variant_B3.json) mit demselben Renderer wie Variante B · Detailmodell v4 bleibt unverändert", n, TAGA); paste(im, EF.IMG("A", "aerial"), 120, 270, 1900, 1070)
    y = text_block(d, 2080, 280, 1320, VA.V["A"]["idee"], 30, INK, "SemiBold"); table(d, 2080, y + 20, [430, 890], kenn_A(), 24)
    text_block(d, 120, 1380, 1900, "Keine neue Geometrie: EG 32 × 18 m, Gastronomie vorn, Kern und Büros hinten, 1. OG +3,00 m nach hinten, zurückgesetztes Staffelgeschoss, fünf Balkone, Vordach, rückwärtige Stellplätze. Wohnfläche und Wohnungen entsprechen den B3-Plänen.", 26, GREY); pages.append(im); n += 1
    im, d = pg("A: 3D-Gesamtansicht und erhöhte Schrägansicht", "gleiche Geometrie wie alle Ansichten von A", n, TAGA); paste(im, EF.IMG("A", "persp"), 120, 300, 1600, 900); paste(im, EF.IMG("A", "aerial"), 1760, 300, 1600, 900); d.text((120, 270), "3D-Gesamtansicht (Platzseite)", font=F(34, "SemiBold"), fill=INK); d.text((1760, 270), "Erhöhte Schrägansicht", font=F(34, "SemiBold"), fill=INK); pages.append(im); n += 1
    for t, items in (("A: Vorder- und Rückansicht", (("front", "Vorderfassade (Platzseite)"), ("rear", "Rückfassade"))), ("A: Seitenansichten West und Ost", (("west", "Seitenfassade West"), ("east", "Seitenfassade Ost")))):
        im, d = pg(t, "orthogonale Ansichten aus dem 3D-Modell", n, TAGA); w = (W - 240 - 60) // 2
        for i, (nm, cap) in enumerate(items): x = 120 + i * (w + 60); d.text((x, 280), cap, font=F(34, "SemiBold"), fill=INK); paste(im, EF.IMG("A", nm), x, 340, w, 1700)
        pages.append(im); n += 1
    im, d = pg("A: Grundrisse EG, 1. OG und Staffelgeschoss", "schematisch, aus den B3-Plänen", n, TAGA); w = (W - 240 - 120) // 3
    for i, (p, cap) in enumerate(((EF.PLN("A", "plan_eg"), "Erdgeschoss"), (EF.PLN("A", "plan_og1"), "1. Obergeschoss"), (EF.PLN("A", "plan_st"), "Staffelgeschoss (oberstes Geschoss)"))): x = 120 + i * (w + 60); d.text((x, 270), cap, font=F(36, "SemiBold"), fill=INK); paste(im, p, x, 330, w, H - 330 - 200)
    pages.append(im); n += 1
    im, d = pg("A: Gebäudeschnitt mit Geschosshöhen und Staffelung", "keine Säulen; Auskragung hinten 3,00 m, Staffel 0,80 m", n, TAGA); paste(im, EF.PLN("A", "schnitt"), 120, 300, 3200, 1500); pages.append(im); n += 1
    im, d = pg("A: Lageplan (Hypothese 32 × 30 m) mit Stellplätzen und Fahrgasse", "maßstäblich · rückwärtig überdachte Stellplätze nach B3 · Grundstück ist HYPOTHESE (siehe Seite zu Baufeld 3)", n, TAGA); os.makedirs(os.path.join(OUT, "AL", "plaene"), exist_ok=True); lp = os.path.join(OUT, "AL", "plaene", "lageplan.png"); EZ.lageplan("AL").save(lp); paste(im, lp, 120, 260, 2300, 2000)
    pk = PRK["AL"]; t = [["Stellplatzprüfung A", ""], ["gezeichnet", str(pk["gesamt"])], ["voll nutzbar", str(pk["voll"])], ["Konflikt", str(pk["konflikt"])], ["überdacht (Anteil)", f"≈ {covered('AL')*100:.0f} %"], ["Fahrgasse", "6,00 m (Annahme)"]]
    table(d, 2480, 300, [520, 400], t, 26); pages.append(im); return pages
def page_B_intro(n):
    im, d = pg("Variante B – neue Idee: EG 540 m², umlaufender Vorbau", "drei Rücksprung-Optionen desselben Konzepts (keine Festlegung) · Darstellung auf der Hypothese 32 × 30 m", n, TAGB)
    rows = [["", "B · bündig bis Attika", "B · Staffel 1,50 m", "B · Staffel 3,00 m"]]
    fl = lambda k: f"{fm(D[k]['flaeche']['eg'])} / {fm(D[k]['flaeche']['og1'])} / {fm(D[k]['flaeche']['st'])}"
    rows += [["Idee", "1. und 2. OG deckungsgleich bis zur Attika (Vorbau setzt sich fort)", "2. OG springt rundum 1,50 m zurück (Dachterrasse)", "2. OG springt rundum 3,00 m zurück (breite Terrasse)"], ["Grundfläche EG / 1. OG / 2. OG (m²)"] + [fl(k) for k, _ in BK],
             ["Auskragung (1. OG)", "1,5 m zum Platz, 1,0 m West, 5,0 m Ost (über die Stellplatzreihe), 0 m Rückseite (Grundstücksende)"] + ["wie links"] * 2, ["Höhe Attika (Bezug offen)"] + ["+12,00 m über FFB"] * 3, ["Säulen"] + [f"{D[k]['anzahl_saeulen']} (Paare 5,4 m: 2 Stellplätze + Säule)" for k, _ in BK],
             ["Wohnfläche netto / Δ gg. A"] + [f"{fm(D[k]['wfl'])} m² / {D[k]['wfl']-D['A']['wfl']:+.0f} m² ({(D[k]['wfl']/D['A']['wfl']-1)*100:+.0f} %)" for k, _ in BK], ["Wohnungen"] + [f"{D[k]['mix']['standard']['we']} WE, {fm(D[k]['mix']['standard']['kleinste'])}–{fm(D[k]['mix']['standard']['groesste'])} m²" for k, _ in BK],
             ["Stellplätze (nutzbar)"] + [f"{PRK[k]['nutzbar']} (davon {PRK[k]['eingeschraenkt']} eingeschränkt)" for k, _ in BK]]
    table(d, 120, 290, [640, 880, 880, 880], rows, 28)
    text_block(d, 120, 1500, 3260, "Wichtig: B ist auf der HYPOTHETISCHEN Grundstücksform 32 × 30 m (aus 960 m²) entwickelt, weil nur dort ein EG von 18 × 30 m = 540 m² und 420 m² Restfläche rechnerisch aufgehen. Auf dem aus den städtischen Plänen abgeleiteten Flurstück 59/1 (≈ 42,3 × 22,7 m, Baufenster ≈ 27,7 × 15,9 m) passt B nicht (siehe Baufeld-3-Seiten). Die Rücksprung-Optionen unterscheiden sich nur im obersten Geschoss; EG, Vorbau, Säulen und Stellplätze sind gleich.", 30, INK); return [im]
def page_B_variant(k, lab, n):
    tag = TAGB + " · " + lab.replace("B · ", "").upper(); pages = []; d0 = D[k]; v = VA.V[k]
    ps = EF.pages_for(k, n, tag)   # Steckbrief, Lageplan, Grundrisse, Fassaden, Schnitt+3D
    return ps
def p_massnahmen_real(n):
    im, d = pg("Baufeld 3 real: Baufenster und Fußabdrücke von A und B", "Flurstück 59/1 (vermutetes Baufeld 3, MI 3): ≈ 42,3 × 22,7 m geschätzt · Baufenster ≈ 27,7 × 15,9 m abgeleitet · Umrisse an der Baufensterecke angelegt", n, TAG)
    BF = ED.BF; foot = [("A: EG 32×18 (B3)", (BF[0], BF[1], BF[0] + 32, BF[1] + 18), (180, 30, 30)), ("A: 1. OG 32×21", (BF[0], BF[1], BF[0] + 32, BF[1] + 21), (225, 120, 120)), ("B: EG 18×30 (30 tief)", (BF[0] + 2, 0.4, BF[0] + 20, 22.7), (140, 60, 160)), ("B gedreht: EG 30×18", (BF[0], BF[1], BF[0] + 30, BF[1] + 18), (30, 90, 200))]
    im2 = ED.plan_p59(2300, 1900, foot=foot); im.paste(im2, (120, 280))
    rows = [["Fußabdruck", "Baufenster 27,7 × 15,9"]] + [[lab, ("passt" if ED.fits(*ED.dims([r])) else "passt NICHT")] for lab, r in (("A: EG 32 × 18 m", (0, 0, 32, 18)), ("A: 1. OG 32 × 21 m", (0, 0, 32, 21)), ("B: EG 18 × 30 m", (0, 0, 18, 30)), ("B gedreht: EG 30 × 18 m", (0, 0, 30, 18)), ("B-Vorbau: 1. OG 24 × 31,5 m", (0, 0, 24, 31.5)))]
    cl = {(i, 1): (OK if r[1] == "passt" else BAD) for i, r in enumerate(rows) if i}; y = table(d, 2480, 300, [560, 380], rows, 24, colors=cl)
    text_block(d, 2480, y + 40, 900, "Weder der B3-Entwurf (A) noch Variante B passen in das Baufenster von MI 3. Gebäudeteile (Vorbau) dürfen die Baugrenze nicht überschreiten. A wie B setzen eine größere Fläche voraus (Befreiung/Planänderung oder anderes Baufeld). Alle Maße sind Schätzungen aus dem Plan, keine Vermessung.", 25, GREY); return [im]
def status_AB(k):
    return ED.status(k)
def p_auswirkung(n):
    COL = {"ok": OK, "pruef": WARN, "kritisch": BAD}; keys = ["A", "F1", "F2", "F3"]; names = ["A (B3)", "B bündig", "B Staffel 1,5", "B Staffel 3,0"]
    im, d = pg("Auswirkungen nach Planstand: A (B3) und B (drei Optionen)", "Planstand 1 = rechtskräftiger Plan 2023 (MI 3) · Planstand 2 = Änderungsentwurf 2026, für Baufeld 3 nicht einschlägig, hier getrennt als Annahme · kein Ergebnis bedeutet baurechtliche Zulässigkeit", n, TAG)
    crit = ["EG im Baufenster", "Vorbau/OG im Baufenster", "Höhe", "Vollgeschosse", "Dachform", "GRZ 0,6", "Stellplätze"]
    for bi, lab in enumerate(("PLANSTAND 1 – rechtskräftig 2023, MI 3: II–III, TH 9,80 m, H 15,00 m, Dach ≥ 38°, Baugrenze 10 m W / 3 m übrige", "PLANSTAND 2 – Entwurf 2026 (hypothetisch): II zwingend, TH 6,50 m, H 12,00 m, Dach ≥ 38°, Baugrenze 3 m")):
        rows = [["Kriterium"] + names]; cl = {}
        for ci, c in enumerate(crit, 1):
            row = [c]
            for kj, k in enumerate(keys, 1):
                s = status_AB(k)[bi][c]; txt = s[1]
                if c == "Stellplätze": txt = "11 rückseitig auf 32×30-Hypothese; auf Flurstück 59/1 nicht unterzubringen (Tiefe 22,7 m < 18 + 5 m)" if k == "A" else "13 auf 32×30-Hypothese; auf 59/1 nicht übertragbar"
                row.append(txt); cl[(ci, kj)] = COL[s[0]]
            rows.append(row)
        d.text((120, 290 + bi * 1000), lab, font=F(28, "SemiBold"), fill=INK); table(d, 120, 340 + bi * 1000, [520] + [(3268 - 520) // 4] * 4, rows, 21, colors=cl)
    return [im]
def p_tabelle(n):
    ks = ["A", "F1", "F2", "F3"]; names = ["A – B3 (Referenz)", "B bündig bis Attika", "B Staffel 1,50 m", "B Staffel 3,00 m"]
    im, d = pg("Vergleichstabelle A gegen B (vorläufig)", "Wohnfläche, Wohnungen, Gewerbe, Stellplätze · alle Werte Schätzungen auf Hypothese 32 × 30 m", n, TAG)
    def stp_row(k): pk = PRK["AL"] if k == "A" else PRK[k]; return f"{pk['gesamt']} gez. / {pk['nutzbar']} nutzbar"
    rows = [["Kennzahl"] + names,
        ["Höhe Attika"] + ["+9,90 m"] + ["+12,00 m (Bezug offen)"] * 3, ["Grundfläche EG (m²)"] + [fm(D[k]["flaeche"]["eg"]) for k in ks], ["Grundfläche 1. OG (m²)"] + [fm(D[k]["flaeche"]["og1"]) for k in ks], ["Grundfläche oberstes Geschoss (m²)"] + [fm(D[k]["flaeche"]["st"]) for k in ks],
        ["Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in ks], ["Δ Wohnfläche gg. A"] + ["±0"] + [f"{D[k]['wfl']-D['A']['wfl']:+.0f} m² ({(D[k]['wfl']/D['A']['wfl']-1)*100:+.0f} %)" for k in ks[1:]],
        ["Wohnungen (Standardmix)"] + [str(D[k]["mix"]["standard"]["we"]) for k in ks], ["Wohnungsgrößen min–max / Ø (m²)"] + [f"{fm(D[k]['mix']['standard']['kleinste'])}–{fm(D[k]['mix']['standard']['groesste'])} / {fm(D[k]['mix']['standard']['mittel'])}" for k in ks],
        ["Wohnungen kleiner / größerer Mix"] + [f"{D[k]['mix']['klein']['we']} / {D[k]['mix']['gross']['we']}" for k in ks], ["Größenklassen ≤50/50–60/60–75/75–85/>85 m²"] + [classes(k) for k in ks],
        ["Gewerbe: EG gesamt (m²)"] + [fm(D[k]["flaeche"]["eg"]) for k in ks], ["Gastraum (m²) ≈ Plätze innen"] + [f"{fm(VA.V[k].get('gastro_m2', 280))} ≈ {D[k]['stp']['sitze_innen']}" for k in ks], ["Terrasse/Arkade ≈ Plätze"] + [str(D[k]["stp"]["sitze_terrasse"]) for k in ks], ["Büro netto (m², Programmannahme)"] + [fm(D[k]["stp"]["buero_m2"]) for k in ks],
        ["Stellplätze gezeichnet / nutzbar"] + [stp_row(k) for k in ks], ["davon überdacht (Anteil)"] + [f"≈ {covered('AL' if k == 'A' else k)*100:.0f} %" for k in ks], ["erforderlich § 47 (Gastro+Büro; Wohnen 0)"] + [f"{fm(D[k]['stp']['erf_lo'],1)}–{fm(D[k]['stp']['erf_hi'],1)}" for k in ks],
        ["optional Wohnen 0,5–1,5 je WE"] + [f"{fm(D[k]['stp']['optional']['standard']['lo'])}–{fm(D[k]['stp']['optional']['standard']['hi'])}" for k in ks], ["Säulen"] + ["0"] + [str(D[k]["anzahl_saeulen"]) for k in ks[1:]], ["Überstand über Grundstücksgrenze (Hyp.)"] + ["0"] + ["1,5 m zum Platz"] * 3]
    table(d, 120, 290, [820] + [(3268 - 820) // 4] * 4, rows, 24); return [im]
def p_pruef(n):
    im, d = pg("Offene Prüfbedarfe und vorläufige Förderhinweise", "Wohnflächen, Stellplätze und Förderung sind vorläufig, bis Geometrie, Grundstück und Rechtslage geprüft sind", n, TAG)
    rows = [["Thema", "Variante A (B3)", "Variante B (neue Idee)"],
      ["Baufenster / Baugrenzen", "EG 32 × 18 m und 1. OG 32 × 21 m passen nicht in das Baufenster von MI 3 (≈ 27,7 × 15,9 m)", "EG 18 × 30 m, Vorbau und 1. OG passen nicht; Vorbau über Baugrenze unzulässig"],
      ["Dachform / Traufe", "Flachdach + Staffel: Dach ≥ 38° vorgeschrieben, TH 9,80 m (Befreiung nötig)", "wie A; zusätzlich Wandhöhe +11,5 m > TH 9,80 m"], ["Höhe", "Attika +9,90 m (Bezug OK Fahrbahn unbekannt)", "+12,00 m über FFB; Plan 2023 H 15,00 m, Entwurf 2026 H 12,00 m (bei SH > 0 überschritten)"],
      ["Stellplätze", "11 rückseitig (teilüberdacht); Nachweis Gastro/Büro 11,4–16,9 knapp", "13 (8 voll überdacht, 5 Längsparker); Sackgasse, Wendebedarf; Zufahrt von Süden angenommen"], ["Fahrwege/Säulen", "Fahrgasse 6 m, keine Säulen", "Säulenpaare 5,4 m auf Stellplatzgrenzen; Feuerwehrzufahrt unter dem Vorbau ungeklärt"],
      ["Statik/Brandschutz", "Kragarm 3,0 m", "Kragarme 1,0 / 1,5 / 5,0 m, 3 Geschosse über Stellplätzen"], ["Förderung (vorläufig)", f"{D['A']['mix']['standard']['we']} WE, Größenklassen {classes('A')}; NBank/KfW-Voraussetzungen offen", f"{D['F1']['mix']['standard']['we']} WE, überwiegend große Wohnungen (66–89 m²), Klassen {classes('F1')}; kleinerer Mix bei Bedarf; Mietenstufe, Gewerbeanteil offen"],
      ["Grundstück", "Hypothese 32 × 30 m", "Hypothese 32 × 30 m; real Flurstück 59/1 ≈ 42,3 × 22,7 m (geschätzt)"]]
    table(d, 120, 290, [620, 1300, 1350], rows, 26)
    text_block(d, 120, 1500, 3260, "Fehlt: Foto Seite 13 bzw. Bestätigung, dass Baufeld 3 = MI 3 / Flurstück 59/1; amtlicher Lageplan/Vermessung; Fahrbahnhöhe der Planstraße; Auskunft der Stadt zu Befreiungen (Dach, Baugrenze, Traufhöhe), Stellplatzregelung und zum Stand der 1. Änderung (Entwurf).", 30, INK); return [im]
def p_fazit(n):
    a, b0, b1, b3 = D["A"], D["F1"], D["F2"], D["F3"]
    im, d = pg("Zwischenergebnis: mehr Wohnfläche ohne Nachteile bei EG und Parken?", "Kein Urteil über Zulässigkeit · Zahlen auf der Hypothese 32 × 30 m, vorläufig", n, TAG)
    t = (f"• Wohnfläche: A {fm(a['wfl'])} m². B bündig {fm(b0['wfl'])} m² ({b0['wfl']-a['wfl']:+.0f} m², {(b0['wfl']/a['wfl']-1)*100:+.0f} %), B Staffel 1,5 m {fm(b1['wfl'])} m² ({b1['wfl']-a['wfl']:+.0f} m², {(b1['wfl']/a['wfl']-1)*100:+.0f} %), B Staffel 3,0 m {fm(b3['wfl'])} m² ({b3['wfl']-a['wfl']:+.0f} m²). Mehrfläche nur, wenn das oberste Geschoss groß bleibt.\n"
         f"• Wohnungen: A 16 WE (47–63 m²); B 13–14 WE, aber deutlich größer (bis 89 m²); mit kleinerem Mix lassen sich mehr WE bilden.\n"
         f"• Gewerbe im EG: A 576 m² (Gastraum ≈ 280 m², ≈ 120 Plätze); B 540 m² (Gastraum ≈ 232 m², ≈ 99 Plätze) – rund 17 % weniger Gastraum bei gleichem Büro.\n"
         f"• Parken: A 11 rückseitige Stellplätze, teilüberdacht; B 13 Plätze, davon 8 voll überdacht und 5 Längsparker; Anforderung für Gastro/Büro: A 11,4–16,9 (11 Plätze = knapp unter der Untergrenze), B 9,7–14,3 (13 Plätze = innerhalb der Spanne, aber Sackgasse und Wendebedarf).\n"
         "• Das EG von B bleibt nutzbar, die Parkmöglichkeiten sind aber nur auf dem hypothetischen Rechteck nachgewiesen.\n"
         "• Auf dem real abgeleiteten Baufeld (MI 3) passen weder A noch B in das Baufenster; für beide wären Befreiungen (Baugrenze, Dach ≥ 38°, Traufhöhe) nötig. Unter dem Änderungsentwurf 2026 (II zwingend, TH 6,50 m, H 12,00 m) widerspricht B zusätzlich der Geschosszahl und Höhe.\n"
         "• Keine Entscheidung getroffen; Variante A und alle bestehenden Modelle sind unverändert.")
    text_block(d, 120, 300, 3260, t, 34); return [im]
def p_titel(n):
    im, d = pg("Baufeld 3: Variante A (B3) gegen Variante B (neue Idee)", "Vergleichsstudie 27.10.2026 · professionelle Entscheidungsgrundlage, keine Festlegung · alle Werte vorläufig", n, TAG)
    rows = [["Planstand / Quelle", "Inhalt", "Status"], ["B-Plan Nr. 123 „Ehemalige Grundschule“ (2023)", "MI 3 / Flurstück 59/1 (vermutetes Baufeld 3): II–III, GRZ 0,6, TH 9,80 m, H 15,00 m, Dach ≥ 38°, Baugrenze 10 m W / 3 m übrige; Bezug OK Fahrbahn, SH 0,30 m", "RECHTSKRÄFTIG seit 14.04.2023"],
        ["1. Änderung (Planzeichnung 25.08.2026)", "betrifft MI 3 nicht; MI, II zwingend, TH 6,50 m, H 12,00 m, Dach ≥ 38°; Parkplatz 63 Plätze", "ENTWURF, nicht beschlossen"],
        ["Grundstück", "Fläche ca. 960 m² (Projektangabe); Flurstück 59/1 ≈ 42,3 × 22,7 m (aus Planabbildung geschätzt); Baufenster ≈ 27,7 × 15,9 m (aus Vektorplan abgeleitet)", "GESCHÄTZT/ABGELEITET, nicht vermessen"],
        ["Entwurfsgrundlage der Varianten", "Hypothese 32 × 30 m (960 m²) – nur zum Vergleich der Entwurfsideen", "HYPOTHESE"], ["Fotos Seiten 13/15/16", "nicht angekommen; Baufeld-3-Zuordnung unbestätigt", "FEHLT"]]
    table(d, 120, 290, [900, 1700, 600], rows, 28)
    text_block(d, 120, 1250, 3260, "Aufbau: 1) Variante A – bisheriger B3-Entwurf (unverändert) mit 3D, Ansichten, Grundrissen, Schnitt, Lageplan · 2) Variante B – neue Idee in drei Rücksprung-Optionen mit denselben Unterlagen · 3) Baufeld 3 real: Baufenster, Planstände, Auswirkungen · 4) Vergleichstabelle, Prüfbedarfe, Zwischenergebnis. Variante A ist die unveränderte Referenz; keine bestehende Datei wurde überschrieben.", 32); return [im]
def baue():
    pages = []; n = 1
    def add(ps): 
        nonlocal n; pages.extend(ps); n += len(ps)
    add(p_titel(n)); add(p_fazit(n)); add(page_A(n)); add(page_B_intro(n))
    for k, lab in BK: add(page_B_variant(k, lab, n))
    add(p_massnahmen_real(n)); add(p_auswirkung(n)); add(p_tabelle(n)); add(p_pruef(n))
    p = os.path.join(OUT, "Vergleichsstudie_A_B3_gegen_B_Neue_Idee.pdf"); save(pages, p); return p, len(pages)
if __name__ == "__main__": print(baue())
