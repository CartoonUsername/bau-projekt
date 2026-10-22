"""Bericht Wirtschaftlichkeit und Finanzierung (docx -> pdf) und Kurzzusammenfassung für das Bankgespräch. Zahlen aus ergebnisse.json (Gegenprobe Excel/Python bestanden)."""
import json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
R = json.load(open("ergebnisse.json"))
from params import PARAMS
P = {p[0]: p[3:6] for p in PARAMS if p[0] != "sec"}
def e(x, d=0): return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"
def n(x, d=0): return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def pc(x, d=1): return n(x * 100, d) + " %"
GREEN = RGBColor(0x2F, 0x4A, 0x3E)
def setup():
    d = Document(); s = d.sections[0]; s.page_width = Cm(21); s.page_height = Cm(29.7); s.left_margin = s.right_margin = Cm(2.0); s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)
    st = d.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(9.5); st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    for nm, sz in (("Heading 1", 15), ("Heading 2", 12), ("Heading 3", 10.5)):
        h = d.styles[nm]; h.font.name = "Georgia"; h.font.size = Pt(sz); h.font.bold = True; h.font.color.rgb = GREEN; rf = h.element.rPr.rFonts; [rf.set(qn(a), "Georgia") for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs")]
    return d
def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), color); tcPr.append(sh)
def table(d, rows, widths=None, head=True, size=8.5, bold_rows=()):
    t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.text = ""; p = c.paragraphs[0]; r = p.add_run(str(v)); r.font.size = Pt(size)
            if (head and i == 0) or i in bold_rows: r.bold = True
            if head and i == 0: shade(c, "E3E8E5")
            if j > 0 and i > 0 and isinstance(v, str) and v[:1].isdigit() or (isinstance(v, str) and v[:1] in "-–+" and len(v) > 1 and v[1].isdigit()): p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if widths:
        t.autofit = False
        for j, w in enumerate(widths): t.columns[j].width = Cm(w)
        for row in t.rows:
            for j, w in enumerate(widths): row.cells[j].width = Cm(w)
    d.add_paragraph(); return t
def para(d, text, bold=False, italic=False, size=None):
    p = d.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    return p
def bullets(d, items):
    for t in items: p = d.add_paragraph(style="List Bullet"); p.add_run(t)
V, Rr, G = R["V 20 %"], R["R 20 %"], R["G 20 %"]
def bericht():
    d = setup()
    t = d.add_paragraph(); r = t.add_run("Neue Mitte Werlte, Baufeld 3"); r.font.name = "Georgia"; r.font.size = Pt(20); r.bold = True; r.font.color.rgb = GREEN
    para(d, "Wirtschaftlichkeit und Finanzierung des Gesamtkonzepts (Arbeitsgrundlage B3)", bold=True, size=12)
    para(d, "Stand 22.10.2026 · vorläufig · alle Zahlen sind begründete Annahmen · keine Förderzusage · Architektur, Wirtschaftlichkeit und baurechtliche Machbarkeit werden getrennt bewertet", italic=True, size=8.5)
    d.add_heading("1. Ergebnis in Kürze", 1)
    para(d, f"Nach den hier begründeten Annahmen trägt sich das Gesamtkonzept in keinem der drei Szenarien aus den Mieten. Bei 20 % Eigenkapital liegt der Kapitaldienstdeckungsgrad bei {n(V['dscr'], 2)} (vorsichtig), {n(Rr['dscr'], 2)} (realistisch) und {n(G['dscr'], 2)} (günstig); üblich wäre mindestens 1,2. Die Finanzierung ist damit nicht tragfähig. Auch die theoretisch höchstmögliche Förderung ändert daran nichts (Deckungsgrad realistisch mit KfW {n(Rr['dscr_kfw'], 2)}, mit NBank-Zuschuss {n(Rr['nb_dscr'], 2)}).")
    rows = [["Eigenkapital 20 %", "vorsichtig", "realistisch", "günstig"]]
    for lab, k, f in (("Gesamtkosten", "T", e), ("Eigenkapital", "EK", e), ("Fremdkapital", "D", e), ("Zinsen monatlich (Jahr 1)", "zins_m", e), ("Kreditrate monatlich (Zins + 2 % Tilgung)", "rate_m", e), ("Kapitaldienst jährlich", "ds", e), ("Netto-Mietertrag jährlich", "noi", e), ("Cashflow nach Kapitaldienst jährlich", "cf", e)):
        rows.append([lab] + [f(R[c][k]) for c in ("V 20 %", "R 20 %", "G 20 %")])
    rows.append(["Kapitaldienstdeckungsgrad"] + [n(R[c]["dscr"], 2) for c in ("V 20 %", "R 20 %", "G 20 %")]); rows.append(["Nettoanfangsrendite"] + [pc(R[c]["rendite"]) for c in ("V 20 %", "R 20 %", "G 20 %")])
    table(d, rows, [7, 3.3, 3.3, 3.3], bold_rows=(9,))
    para(d, f"Was sich ändern müsste: Alle Mieten müssten im realistischen Szenario um den Faktor {n(Rr['be_faktor_1'], 2)} steigen, damit der Deckungsgrad 1,0 erreicht (Wohnmiete {n(Rr['be_wohn_1'], 1)} €/m² bei unveränderten Gewerbemieten); für einen Deckungsgrad von 1,2 mit 20 % Fremdkapital-Anteil wären ca. {e(Rr['ek_need'])} Eigenkapital nötig ({pc(Rr['q_need'], 0)} der Gesamtkosten). Die Spanne der Kostenannahmen ist groß; entscheidend ist die Prüfung durch einen Kostenplaner.")
    d.add_heading("2. Gesamtkonzept und Flächen", 1)
    para(d, "Gebäude 32 × 18 m im Erdgeschoss, drei Geschosse (EG, 1. OG, zurückgesetztes Staffelgeschoss). Erdgeschoss: großzügige Gastronomie vorn und in der Mitte (440 m² brutto, Gastraum und Bar 280 m², ca. 120 Innenplätze möbliert, ca. 44 Terrassenplätze), kompakte Büros hinten (2 × 28 m² netto), Wohnkern im Westen. 1. OG und Staffel nur Wohnungen: 16 Wohnungen mit 846 m² Wohnfläche netto; fünf Balkone zur Platzseite, Staffel 0,80 m zurückgesetzt, hinten 3 m Auskragung des 1. OG über überdachten Stellplätzen und drei Dachterrassen (20,7 m²) vor den hinteren Staffelwohnungen. Pläne: Ordner varianten_v3 und gesamtkonzept (Blätter 21–27, 31, 32).")
    table(d, [["Fläche", "Brutto m²", "Netto / Miet m²"], ["Gastronomie (Mietfläche)", "440,0", "440,0"], ["Büros 1 und 2", "64,0", "56,3"], ["Wohnungen 1. OG (9)", "660,0 (Geschoss)", "468,0"], ["Wohnungen Staffelgeschoss (7)", "539,1 (Geschoss)", "377,9"], ["Bruttogrundfläche gesamt", "1.775,1", ""], ["Wohnfläche gesamt (16 Wohnungen)", "", "845,9"]], [8, 4, 4])
    para(d, "Netto = Brutto × 0,88 (Annahme). Balkone und Dachterrassen sind nicht in der Wohnfläche angesetzt. Alle Geschossflächen mit Auskragung sind hypothetisch (Baufenster, GRZ und Abstände offen).", italic=True, size=8.5)
    d.add_heading("3. Einnahmen (getrennt nach Bereichen)", 1)
    rows = [["Bereich", "Annahme (vorsichtig / realistisch / günstig)", "Jahresmiete realistisch", "nach Leerstand"]]
    rows.append(["A. Gastronomie, Vermietung an einen Betreiber", f"440 m² × {n(P['m_gastro'][0], 0)} / {n(P['m_gastro'][1], 0)} / {n(P['m_gastro'][2], 0)} €/m² Monat, Ausfall {n(P['v_gastro'][0], 0)} / {n(P['v_gastro'][1], 0)} / {n(P['v_gastro'][2], 0)} %", e(Rr["soll_g"]), e(Rr["eff"] - Rr["eff"] + (Rr["soll_g"] * (1 - P['v_gastro'][1] / 100)))])
    rows.append(["B. 16 Wohnungen", f"846 m² × {n(P['m_wohn'][0], 1)} / {n(P['m_wohn'][1], 1)} / {n(P['m_wohn'][2], 1)} €/m² Monat, Leerstand {n(P['v_wohn'][0], 1)} / {n(P['v_wohn'][1], 1)} / {n(P['v_wohn'][2], 1)} %", e(Rr["soll_w"]), e(Rr["soll_w"] * (1 - P['v_wohn'][1] / 100))])
    rows.append(["C. Büros (2)", f"56,3 m² netto × {n(P['m_buero'][0], 1)} / {n(P['m_buero'][1], 1)} / {n(P['m_buero'][2], 1)} €/m² Monat, Leerstand {n(P['v_buero'][0], 0)} / {n(P['v_buero'][1], 0)} / {n(P['v_buero'][2], 0)} %", e(Rr["soll_b"]), e(Rr["soll_b"] * (1 - P['v_buero'][1] / 100))])
    rows.append(["Gesamt Sollmiete / nach Leerstand", "", e(Rr["soll"]), e(Rr["eff"])]); rows.append(["laufende nicht umlagefähige Kosten", "Instandhaltung, Verwaltung, sonstige (Wohnen 10 €/m², 300 €/Wohnung, 4 €/m²; Gewerbe 6 + 3 €/m², 3 % Miete)", "", e(-Rr["kosten"])]); rows.append(["Netto-Mietertrag", f"monatlich {e(Rr['noi'] / 12)}", "", e(Rr["noi"])])
    table(d, rows, [4.5, 7.2, 2.7, 2.7], bold_rows=(4, 6))
    bullets(d, ["Wohnungen: Angebote in Werlte und Umgebung 2026 liegen bei 9,5–12,5 €/m² (Neubau), der Durchschnitt in Werlte bei 7,8–8,4 €/m² (ImmoScout24, miet-check, miete-aktuell). Die Stichprobe ist klein, es sind Angebotsmieten. Die vorsichtigen, realistischen und günstigen Annahmen 9,5 / 10,5 / 11,5 €/m² liegen im oberen Bereich dieser Spanne, weil Neubau.",
                "Büros: Angebote Werlte 9,6–12 €/m² (kleine Einheiten), Meppen 9–9,5, Sögel 6,3–7,8 €/m². Vermietbar sind nur die beiden Büros (56,3 m²); Foyer und WC (15,6 m²) sind keine Mietfläche. Vermietbarkeit kleiner Büros in Werlte ist nicht belegt.",
                "Gastronomie: Keine regionale Flächenmiete gefunden; die Annahme 8/10/12 €/m² wird über die Pachtquote geprüft (Richtwert 8–12 % des Nettoumsatzes, Ratgeber): bei 164 Plätzen und 5.500 € Umsatz je Platz entspräche die realistische Miete etwa 7 % des Umsatzes. Der Umsatz je Platz ist nicht belegt. Es wird keine Eigenbewirtschaftung unterstellt."])
    d.add_heading("4. Gesamtinvestition (Kostenschätzung nach DIN 276)", 1)
    rows = [["Kostengruppe", "vorsichtig", "realistisch", "günstig"]]
    for lab, k in (("KG 100 Grundstück (960 m² × 230 €)", "grund"), ("Erwerbsnebenkosten (5 % + 2 %)", "neben"), ("KG 200 Herrichten, Erschließen", "kg200"), ("KG 300+400 Bauwerk inkl. EH-40-Aufschlag", "kg300"), ("Gewerbe-Ausbau durch Vermieter", "ausbau"), ("KG 500 Außenanlagen, Stellplätze, Terrasse", "kg500"), ("KG 700 Baunebenkosten (Planung, Fachplaner, Genehmigung, Sonstiges)", "bnk"), ("Reserve", "reserve"), ("Zwischensumme", "S"), ("Finanzierungskosten", "F"), ("GESAMTKOSTEN", "T")):
        rows.append([lab] + [e(R[c][k]) for c in ("V 20 %", "R 20 %", "G 20 %")])
    table(d, rows, [8, 3, 3, 3], bold_rows=(9, 11))
    para(d, f"Bauwerk: {n(P['bau_m2'][0])} / {n(P['bau_m2'][1])} / {n(P['bau_m2'][2])} €/m² Bruttogrundfläche (1.775 m²); Baunebenkosten 22,5 / 20 / 17,5 % von KG 300–500; Reserve 8 / 6 / 4 %. Alle Preise brutto inklusive 19 % Mehrwertsteuer, ein Vorsteuerabzug ist nicht angesetzt (Wohnungsvermietung ist umsatzsteuerfrei; Option beim Gewerbeteil steuerlich zu prüfen). Die Baukosten sind Orientierungswerte aus Ratgeberseiten (2.500–3.500 €/m² Wohnfläche), nicht aus BKI; Bodengutachten, Lageplan und Planungsstand fehlen. Der günstige Fall entspricht der bisherigen Projektannahme von 2.200 €/m². Die Außenanlagen beruhen auf der unbestätigten Annahme 32 × 30 m Grundstück.", size=8.5)
    d.add_heading("5. Finanzierung bei unterschiedlichen Eigenkapitalquoten (ohne Förderung)", 1)
    for sc, nm in (("R", "Realistisches Szenario"), ("V", "Vorsichtiges Szenario"), ("G", "Günstiges Szenario")):
        d.add_heading(nm, 3)
        rows = [["Eigenkapitalquote", "0 %", "10 %", "20 %", "30 %"]]; cs = [f"{sc} 0 %", f"{sc} 10 %", f"{sc} 20 %", f"{sc} 30 %"]
        for lab, k, f in (("Eigenkapital", "EK", e), ("Fremdkapital", "D", e), ("Zinsen monatlich (Jahr 1)", "zins_m", e), ("Kreditrate monatlich", "rate_m", e), ("Kapitaldienst jährlich", "ds", e), ("Netto-Mietertrag jährlich", "noi", e), ("Cashflow nach Kapitaldienst jährlich", "cf", e)):
            rows.append([lab] + [f(R[c][k]) for c in cs])
        rows.append(["Kapitaldienstdeckungsgrad"] + [n(R[c]["dscr"], 2) for c in cs]); table(d, rows, [6, 2.7, 2.7, 2.7, 2.7], bold_rows=(8,), size=8)
    para(d, f"Zinssatz Hausbank: {n(P['z_bank'][0], 1)} / {n(P['z_bank'][1], 1)} / {n(P['z_bank'][2], 1)} % (10 Jahre fest; Bauzinsen 10/2026 ca. 4,0–4,5 %, Dr. Klein 22.10.2026: 4,13 % effektiv; Aufschlag gewerblich), anfängliche Tilgung 2 % (bei 1 % Tilgung sinkt der Kapitaldienst im realistischen Fall auf {e(R['R 20 %, Tilgung 1 %']['ds'])}, der Deckungsgrad steigt auf {n(R['R 20 %, Tilgung 1 %']['dscr'], 2)}). Finanzierungskosten: Bauzeitzinsen (15 Monate, 50 % mittlere Inanspruchnahme), Anlaufzinsen (9 / 6 / 3 Monate), Bearbeitung 1 %.", size=8.5)
    d.add_heading("6. Break-even und Sensitivität (realistisch, 20 % Eigenkapital)", 1)
    cs = ["R 20 %", "R Baukosten +10 %", "R Baukosten +20 %", "R Zins +1 pp", "R Zins +2 pp", "R Leerstand +5 pp", "R Leerstand +10 pp", "R Miete −10 %"]
    rows = [["Fall", "Gesamtkosten", "Kapitaldienst", "Netto-Mietertrag", "Cashflow", "DSCR"]]
    for c in cs: rows.append([c.replace("R ", "", 1) if c != "R 20 %" else "Basis", e(R[c]["T"]), e(R[c]["ds"]), e(R[c]["noi"]), e(R[c]["cf"]), n(R[c]["dscr"], 2)])
    table(d, rows, [4.2, 3, 3, 3, 3, 1.6], size=8)
    bullets(d, [f"Break-even-Wohnmiete für Deckungsgrad 1,0: {n(Rr['be_wohn_1'], 1)} €/m² (vorsichtig {n(V['be_wohn_1'], 1)}, günstig {n(G['be_wohn_1'], 1)}); für 1,2: {n(Rr['be_wohn_12'], 1)} €/m².", f"Break-even-Faktor aller Mieten für 1,0: {n(Rr['be_faktor_1'], 2)} (günstig {n(G['be_faktor_1'], 2)}).", "Der Deckungsgrad liegt in allen Sensitivitätsfällen unter 1,0; die Aussage hängt nicht an einer einzelnen Annahme."])
    d.add_heading("7. Fördermöglichkeiten (Abruf 22.10.2026)", 1)
    para(d, "Offizielle Seiten von KfW und NBank waren aus der Arbeitsumgebung nicht direkt abrufbar; die Angaben stammen aus Suchtreffern (KfW-Merkblattlinks, Beratungs- und Ratgeberseiten, NBank-Pressemeldung) und sind vor einer Antragstellung gegen die Originalmerkblätter und die Konditionsübersicht zu prüfen. Förderzinsen sind zeitabhängig und widersprüchlich angegeben; sie sind noch zu bestätigen.", italic=True, size=8.5)
    rows = [["Programm", "theoretisch möglich (Höhe)", "fachlich plausibel", "bestätigt"], ["KfW 297/298 Wohngebäude", f"bis 100.000 € je WE, mit QNG-PLUS/-PREMIUM 150.000 € (16 WE: bis 2,4 Mio €); Zinsverbilligung, kein Zuschuss; Laufzeit bis 35 J., Zinsbindung bis 10 J.; im Modell {e(Rr['k297'])}", "plausibel bei Effizienzhaus 40 mit QNG; Mischnutzung (Wohnanteil ca. 72 % der BGF) prüfen; EH-55-Stufe nur bis 31.12.2026", "nein"],
            ["KfW 296 Niedrigpreissegment", "bis 100.000 € je WE (16 WE: 1,6 Mio €); EH 55, Wohnflächenoptimierung, Kostengrenzen; nicht mit 297/298/299 je Einheit kombinierbar", "unwahrscheinlich (Programmkriterien, Gewerbeanteil, Dachterrassen)", "nein"],
            ["KfW 299 Nichtwohngebäude (Gewerbeteil)", f"laut Drittseiten 1.000–2.000 €/m², Bezugsfläche ungeklärt; im Modell {e(Rr['k299'])} (1.500 €/m² × 504 m²); Merkblatt 07/2026", "unklar (Abgrenzung zum Wohnteil, Mischnutzung)", "nein"],
            ["NBank Mietwohnraumförderung (seit 01.07.2026)", f"Zuschuss bis 40 % der förderfähigen Kosten (Obergrenze, im Modell {e(Rr['nb_zuschuss'])}), Mietbindung 35 Jahre, gebundene Miete 6,30–7,80 €/m² (Stand 04/2026)", "nicht plausibel mit Marktmieten; Mietstufe Werlte unbekannt", "nein"],
            ["Kommunale Programme", "nicht ermittelt", "nicht beurteilbar", "nein"]]
    table(d, rows, [3.5, 6.5, 4.8, 1.6], size=8)
    rows = [["Einfluss (realistisch, 20 % EK)", "ohne Förderung", "KfW 297 + 299 theoretisch", "NBank theoretisch"], ["Fremdkapital", e(Rr["D"]), e(Rr["D"]), e(Rr["nb_D"])], ["Kapitaldienst jährlich", e(Rr["ds"]), e(Rr["ds_kfw"]), e(Rr["nb_ds"])], ["Netto-Mietertrag jährlich", e(Rr["noi"]), e(Rr["noi"]), e(Rr["nb_noi"])], ["Deckungsgrad", n(Rr["dscr"], 2), n(Rr["dscr_kfw"], 2), n(Rr["nb_dscr"], 2)]]
    table(d, rows, [5, 3.5, 4, 3.5], size=8, bold_rows=(4,))
    para(d, f"KfW-Zinssätze im Modell: 297/298 {n(P['z_297'][1], 1)} % und 299 {n(P['z_299'][1], 1)} % (realistisch, noch zu bestätigen; Quellenspanne 0,6–3,05 %). Auch mit den theoretischen Höchstbeträgen bleibt der Deckungsgrad unter 1,0. Förderung ist hier keine zugesagte Größe und wird nicht zur Begründung der Tragfähigkeit verwendet.", size=8.5)
    d.add_heading("8. Risikoanalyse", 1)
    table(d, [["Risiko", "Wirkung", "Einschätzung / Gegenmaßnahme"], ["Baukosten höher als angenommen", "+10 % Baukosten: DSCR " + n(R['R Baukosten +10 %']['dscr'], 2), "hoch; Kostenplanung nach BKI, Ausschreibung, Festpreis"], ["Zinsen steigen", "+2 pp: DSCR " + n(R['R Zins +2 pp']['dscr'], 2), "mittel; Zinsbindung, Sondertilgung, Förderzins sichern"], ["Mieten niedriger / Leerstand", "−10 % Miete: " + n(R['R Miete −10 %']['dscr'], 2), "hoch; Marktprüfung, Vorvermietung"], ["Gastronomie: Betreiber und Pacht", "Pacht und Betreiberwechsel nicht belegt", "hoch; Letter of Intent, Mindestpacht, Sicherheiten"], ["Büros: Vermietbarkeit", "nur 56 m², kleine Einheiten", "mittel; Mietinteressenten vorab"],
            ["Baurecht (GRZ, Baufenster, Auskragung, Höhen)", "alle Varianten über der theoretischen GRZ-Fläche", "hoch; Bauvoranfrage bei der Stadt"], ["Stellplätze", "Bedarf ca. 54 (Annahme), nachweislich 0, hypothetisch 11", "hoch; Satzung, Nachweis, Ablöse klären"], ["Förderung", "keine Zusage, Konditionen zeitabhängig", "nicht einplanen; Antrag vor Baubeginn"], ["Lage und Schall", "Wohnungen über Gastro-Terrasse und Bar", "mittel; Schallgutachten, Betriebszeiten"], ["Tragwerk, Brandschutz", "Auskragung, Dachterrassen, Gastro unter Wohnungen", "mittel; Fachplaner früh einbinden"]], [4.5, 5.5, 6.4], size=8)
    d.add_heading("9. Getrennte Bewertung", 1)
    bullets(d, ["Architektur: Das Gesamtkonzept ist als Arbeitsgrundlage geometrisch konsistent (Pläne, Schnitte, Ansichten, Flächenübersicht); keine Freigabe, keine Detailplanung.", "Wirtschaftlichkeit: Nach den hier begründeten Annahmen nicht tragfähig, auch nicht mit theoretischer Förderung.", "Baurechtliche Machbarkeit: nicht nachgewiesen (Baufenster, GRZ, Auskragung, Höhen, Stellplätze, Brandschutz sind offene Prüfpunkte); keine Zulässigkeit behauptet."])
    d.add_heading("10. Offene Entscheidungen", 1)
    bullets(d, ["Grundrichtung: Soll die Planung an die Wirtschaftlichkeit angepasst werden (z. B. weniger Aufwand bei Staffel, Auskragung, Außenanlagen), oder soll mit deutlich höherem Eigenkapital oder anderen Mitteln geplant werden?", "Kostenprüfung der Baukosten durch Kostenplaner/Architekt (BKI) und Vergleich mit realen Angeboten.", "Bauvoranfrage zu Baufenster, GRZ, Auskragung, Staffel als Vollgeschoss, Stellplätzen.", "Gastronomie: Betreiber und Pacht klären (Absichtserklärung).", "Förderberatung bei Hausbank/KfW und Wohnraumförderstelle (Mietstufe, Konditionen), vor Baubeginn.", "Büro-Alternative K, F oder M und Ort für Fahrrad-/Abstellraum.", "Steuerliche Beratung (Umsatzsteuer-Option, Abschreibung, GbR)."])
    d.add_heading("Anhang: Quellen (Abruf 22.10.2026)", 1)
    for t in ["KfW 297/298: baukostenplan.de/ratgeber/kfw-297-298-klimafreundlicher-neubau-2026; baumentor.de; hausbaujournal.com (Zinsangaben widersprüchlich)", "KfW 296: kfw.de Merkblatt 6000005195_M_296; baukostenplan.de/ratgeber/kfw-296-klimafreundlicher-neubau-niedrigpreissegment", "KfW 299: kfw.de Merkblatt 6000005052_M_299 (Fassung 07/2026, nicht gelesen); fensterversand.com/foerderung/kfw/299.php", "NBank: nbank.de Pressemeldung ‚Niedersachsen stellt soziale Wohnraumförderung neu auf‘; Produktinformation Energetisch hochwertiger Mietwohnungsneubau (Stand 07/2026, nicht gelesen)", "Mieten: kleinanzeigen.de, immowelt.de, meinestadt.de (Werlte), ImmoScout24 Mietspiegel Landkreis Emsland Q2 2026, miet-check.de, miete-aktuell.de", "Büro: immowelt.de, immobilienscout24.de (Gewerbe) Werlte, Meppen, Sögel", "Pacht: gastro-master.de, kanzlei-herfurtner.de", "Zinsen: baufi24.de Zinskommentar 10/2026, sparkasse.de, interhyp.de, drklein.de", "Baukosten: baukostenplan.de (Mehrfamilienhaus, Niedersachsen)", "Rechenmodell: Wirtschaftlichkeit_Gesamtkonzept_B3.xlsx (Formeln, Gegenprobe gegen unabhängige Python-Rechnung mit Abweichung unter 1e-9)"]:
        p = d.add_paragraph(style="List Bullet"); r = p.add_run(t); r.font.size = Pt(8)
    d.save("Wirtschaftlichkeit_und_Finanzierung_Baufeld3_B3.docx")
def kurz():
    d = setup()
    t = d.add_paragraph(); r = t.add_run("Neue Mitte Werlte, Baufeld 3 – Kurzzusammenfassung für das Finanzierungsgespräch"); r.font.name = "Georgia"; r.font.size = Pt(15); r.bold = True; r.font.color.rgb = GREEN
    para(d, "Hümmlinger Volksbank, Werlte · Stand 22.10.2026 · vorläufig · alle Zahlen Annahmen · keine Förderzusage", italic=True, size=8.5)
    d.add_heading("Vorhaben", 2)
    para(d, "Mischgenutztes Gebäude auf 960 m² (230 €/m²): Erdgeschoss mit großzügiger Gastronomie (440 m², ca. 120 Innenplätze) und zwei kompakten Büros (56 m² netto), 16 Wohnungen (846 m² Wohnfläche) im 1. Obergeschoss und im zurückgesetzten Staffelgeschoss, Dachterrassen und überdachte Stellplätze. Gastronomie wird vermietet, nicht selbst betrieben. Baufenster, GRZ, Abstände und Stellplatznachweis sind noch nicht geklärt.")
    d.add_heading("Zahlen (Eigenkapital 20 %)", 2)
    rows = [["", "vorsichtig", "realistisch", "günstig"], ["Gesamtkosten (inkl. Grundstück, Nebenkosten, Finanzierung)"] + [e(R[c]["T"]) for c in ("V 20 %", "R 20 %", "G 20 %")], ["Fremdkapital"] + [e(R[c]["D"]) for c in ("V 20 %", "R 20 %", "G 20 %")], ["Zinsen monatlich / Rate monatlich (2 % Tilgung)"] + [f"{e(R[c]['zins_m'])} / {e(R[c]['rate_m'])}" for c in ("V 20 %", "R 20 %", "G 20 %")],
            ["Netto-Mietertrag jährlich"] + [e(R[c]["noi"]) for c in ("V 20 %", "R 20 %", "G 20 %")], ["Kapitaldienst jährlich"] + [e(R[c]["ds"]) for c in ("V 20 %", "R 20 %", "G 20 %")], ["Cashflow nach Kapitaldienst jährlich"] + [e(R[c]["cf"]) for c in ("V 20 %", "R 20 %", "G 20 %")], ["Kapitaldienstdeckungsgrad"] + [n(R[c]["dscr"], 2) for c in ("V 20 %", "R 20 %", "G 20 %")]]
    table(d, rows, [7.4, 3.2, 3.2, 3.2], bold_rows=(7,), size=8.5)
    d.add_heading("Einordnung", 2)
    bullets(d, [f"Die Finanzierung ist nach diesen Annahmen nicht tragfähig: Deckungsgrad {n(V['dscr'], 2)} / {n(Rr['dscr'], 2)} / {n(G['dscr'], 2)}, Cashflow negativ in allen Szenarien.", f"Break-even: Wohnmiete {n(Rr['be_wohn_1'], 1)} €/m² (realistisch) bzw. alle Mieten × {n(Rr['be_faktor_1'], 2)}; ein tragbarer Deckungsgrad von 1,2 bräuchte ca. {e(Rr['ek_need'])} Eigenkapital.", f"Mit theoretisch höchster KfW-Förderung (297 + 299) steigt der Deckungsgrad nur auf {n(Rr['dscr_kfw'], 2)}; mit NBank-Zuschuss und gebundener Miete {n(Rr['nb_dscr'], 2)}. Keine Förderung ist zugesagt, Förderzinsen sind noch zu bestätigen.", "Mieten: Neubauangebote in Werlte und Umgebung 9,5–12,5 €/m² (Durchschnitt 7,8–8,4); Büros 9–12 €/m²; Gastronomie nur als Pachtquote (8–12 % vom Umsatz) plausibilisiert.", "Baukosten: Orientierung 2.200–3.000 €/m² BGF (günstig bis vorsichtig), noch nicht durch Kostenplanung belegt."])
    d.add_heading("Fragen und Bitten an die Bank", 2)
    bullets(d, ["Welcher Deckungsgrad und welche Eigenkapitalquote werden für gemischt genutzte Objekte dieser Größe gefordert?", "Welche Beleihungsauslauf- und Mietansätze legt die Bank an (Wohnen, Büro, Gastronomie)?", "Wie wird Gastronomie als Vermietung bewertet (Betreiberbonität, Sicherheiten)?", "Konditionen KfW 297/298/299 über die Hausbank: aktuelle Zinsen, Eignung bei Mischnutzung, Antragszeitpunkt vor Baubeginn.", "Gewünschte Unterlagen für den nächsten Schritt (Kostenermittlung, Bauvoranfrage, Mietbestätigungen)."])
    d.add_heading("Offene Punkte (ehrlich)", 2)
    bullets(d, ["Baurecht nicht nachgewiesen (Baufenster, GRZ, Auskragung, Höhen, Staffel als Vollgeschoss, Stellplätze).", "Kosten und Mieten sind Annahmen; Bodengutachten, Lageplan, Kostenplanung und Mietinteressenten fehlen.", "Grundrichtung (Anpassung des Konzepts an die Wirtschaftlichkeit) ist noch zu entscheiden."])
    d.save("Kurzzusammenfassung_Finanzierungsgespraech.docx")
bericht(); kurz(); print("ok")
