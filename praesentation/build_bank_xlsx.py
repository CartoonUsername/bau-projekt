"""Bankunterlagen Baufeld 3 (Neue Mitte Werlte) als Excel-Rechenmodell mit Formeln.

Aufruf: python3 build_bank_xlsx.py Bankunterlagen_Baufeld3.xlsx
Danach: python3 <skill>/scripts/recalc.py Bankunterlagen_Baufeld3.xlsx   (rechnet alle Formeln und prüft auf Fehler)
Alle Eingaben stehen im Blatt 'Annahmen' (blaue Schrift). Alle anderen Blätter rechnen daraus.
"""
import json
import sys
from openpyxl import Workbook
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties

OUT = sys.argv[1] if len(sys.argv) > 1 else "Bankunterlagen_Baufeld3.xlsx"
REG = {}  # Schlüssel -> "Blatt!Zelle" für den Export der Kennzahlen (bank_values.json)

GREEN = "2F4A3E"
GOLD = "C49A45"
LIGHT = "F1F0EE"
F = "Arial"
base = Font(name=F, size=10)
bold = Font(name=F, size=10, bold=True)
inp = Font(name=F, size=10, color="0000FF")
link = Font(name=F, size=10, color="008000")
note = Font(name=F, size=9, italic=True, color="5B6770")
hdr_font = Font(name=F, size=10, bold=True, color="FFFFFF")
title_font = Font(name=F, size=16, bold=True, color=GREEN)
sub_font = Font(name=F, size=10, color="5B6770")
hdr_fill = PatternFill("solid", fgColor=GREEN)
sec_fill = PatternFill("solid", fgColor="E3E8E5")
key_fill = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="D0D0D0")
box = Border(top=thin, bottom=thin, left=thin, right=thin)

EUR = '#,##0 "€";-#,##0 "€";"–"'
EUR2 = '#,##0.00 "€";-#,##0.00 "€";"–"'
EURS = '+#,##0 "€";-#,##0 "€";"–"'
M2 = '#,##0.0 "m²"'
PCT = "0.0%"
PCT2 = "0.00%"
NUM = "#,##0"
X = '0.00"x"'

wb = Workbook()


def q(name):
    return "'" + name + "'"


def sheet(name, title, subtitle="", widths=None, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = name
    ws.sheet_view.showGridLines = False
    ws["A1"] = title
    ws["A1"].font = title_font
    ws["A2"] = subtitle
    ws["A2"].font = sub_font
    for i, w in enumerate(widths or [], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


def put(ws, ref, value, fmt=None, font=None, fill=None, align=None, border=True):
    c = ws[ref]
    c.value = value
    c.font = font or base
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if align:
        c.alignment = align
    if border:
        c.border = box
    return c


def header(ws, row, labels, col=1):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=t)
        c.font = hdr_font
        c.fill = hdr_fill
        c.alignment = Alignment(horizontal="left" if i == 0 else "center", vertical="center", wrap_text=True)
        c.border = box


def section(ws, row, text, cols=6):
    for i in range(cols):
        ws.cell(row=row, column=1 + i).fill = sec_fill
    c = ws.cell(row=row, column=1, value=text)
    c.font = bold


def reg(key, ws, ref):
    REG[key] = f"{ws.title}!{ref}"


# =====================================================================================
# Annahmen
# =====================================================================================
sA = sheet("Annahmen", "Annahmen", "Blaue Zellen sind Eingaben, alle anderen Blätter rechnen daraus. Quelle 'Bauherr' = Vorgabe von Bessam Hasso, 'Annahme' = Planungsannahme ohne Beleg.", [46, 16, 62], first=False)
wb.remove(wb["Sheet"]) if "Sheet" in wb.sheetnames else None
A = {}
row = 4
ASSUME = [
    ("sec", "Grundstück"),
    ("grund_m2", "Grundstücksfläche (m²)", 960, NUM, "Konzeptheft Neue Mitte Werlte, Baufeld 3"),
    ("preis_m2", "Kaufpreis je m² (€)", 230, EUR, "Bauherr / Stadt Werlte"),
    ("grest", "Grunderwerbsteuer", 0.05, PCT, "Niedersachsen 5,0 %"),
    ("notar", "Notar und Grundbuch", 0.02, PCT, "Annahme"),
    ("sec", "Bauwerk"),
    ("bgf_eg", "BGF Erdgeschoss (m²)", 576, NUM, "Grundfläche 32 × 18 m = GRZ-Maximum 0,6 × 960 m² = 576 m²"),
    ("bgf_og", "BGF 1. Obergeschoss (m²)", 576, NUM, "zweites Vollgeschoss: 2 Büros und 3 Wohnungen"),
    ("bgf_st", "BGF Staffelgeschoss in Holzbau (m²)", 498, NUM, "0,8 m rundum zurückgesetzt: 30,4 × 16,4 m, 5 Wohnungen"),
    ("baukosten_m2", "Baukosten je m² BGF (€)", 2200, EUR, "Bauherr (Bekanntenpreis), durch Angebote zu belegen"),
    ("holz_abschlag", "Holzbau günstiger als Massivbau (€/m²)", 400, EUR, "Annahme, Angebot der Zimmerei nötig"),
    ("terrasse_m2", "Umlaufende Dachterrasse (m²)", 77, NUM, "schmal, ca. 0,8 m, zählt nicht zur BGF"),
    ("terrasse_preis", "Dachterrasse Preis (€/m²)", 450, EUR, "Annahme"),
    ("bnk", "Baunebenkosten", 0.15, PCT, "Architekt, Statik, Gebühren; Annahme"),
    ("mehr_eh40", "Mehrkosten Effizienzhaus 40 und QNG", 0.03, PCT, "Annahme, auf Bau inkl. Baunebenkosten; Architekt muss bestätigen"),
    ("gastro_ausbau", "Gastro-Ausbau (€)", 190000, EUR, "Bauherr: 150.000 € für 150 Plätze, hier 1.000 € je Platz bei 190 Plätzen; Angebote nötig"),
    ("sec", "Flächen und Nutzung"),
    ("gastro_m2", "Gastrofläche im EG (m²)", 510, NUM, "EG abzüglich Treppenhaus, Aufzug, Eingänge (66 m²); Bedarf siehe Blatt Gewerbe und Anker"),
    ("ngf_anteil", "Nettogrundfläche Anteil der Gastrofläche", 0.85, PCT, "Annahme, für KfW 299"),
    ("wf_og", "Wohnfläche 1. OG (m²)", 321, NUM, "3 Wohnungen à ca. 107 m² (OG: 576 m² BGF minus Büros, Treppenhaus, Wände)"),
    ("n_og", "Wohnungen im 1. OG", 3, NUM, "Bauherr: 8 Wohnungen insgesamt"),
    ("wf_st", "Wohnfläche Staffelgeschoss (m²)", 334, NUM, "5 Wohnungen à ca. 67 m² (67 % der BGF)"),
    ("n_st", "Wohnungen im Staffelgeschoss", 5, NUM, "Bauherr: 8 Wohnungen insgesamt"),
    ("eigen", "davon vom Bauherrn selbst genutzt (Anzahl)", 0, NUM, "0 = alle vermietet. Selbstnutzung: KfW 297 statt 298, Miete entfällt"),
    ("sec", "Ankermieter Büro (1. OG, mit Aufzug)"),
    ("b1_m2", "Büro 1, Versicherungsgesellschaft o. ä. (m²)", 100, NUM, "Bauherr: größeres Büro, langfristiger Ankermieter"),
    ("b1_miete", "Büro 1: Kaltmiete (€/m²)", 9.5, EUR2, "Annahme: Neubau-Büro im Mittelzentrum ca. 8–11 €/m²; keine Marktdaten für Werlte gefunden"),
    ("b2_m2", "Büro 2, kleiner Makler o. ä. (m²)", 65, NUM, "Bauherr: kleineres Büro"),
    ("b2_miete", "Büro 2: Kaltmiete (€/m²)", 10.0, EUR2, "Annahme, kleine Einheit etwas teurer je m²"),
    ("b_laufzeit", "Mietvertragslaufzeit Ankermieter (Jahre)", 10, NUM, "Annahme: 10 Jahre fest, Indexmiete"),
    ("b_ausbau", "Vermieter-Ausbau der Büros (€/m²)", 150, EUR, "Annahme: Böden, Decken, Elektro-Grundausbau; Rest Mieter"),
    ("sec", "Gastro-Flächenbedarf (Richtwerte)"),
    ("plaetze_gast", "Plätze im Gastraum inkl. Bar und Lounge", 160, NUM, "Planung"),
    ("plaetze_sep", "Plätze im Séparée", 30, NUM, "Planung"),
    ("m2_platz", "Fläche je Platz im Gastraum (m²)", 1.9, "0.0", "Richtwert Gastraum 1,6–2,2 m² je Platz"),
    ("m2_platz_sep", "Fläche je Platz im Séparée (m²)", 1.4, "0.0", "Richtwert Festtafel"),
    ("fl_bar", "Bar- und Theken-Zone (m²)", 25, NUM, "Theke, Backbar, Service"),
    ("fl_kueche", "Küche mit Spülküche (m²)", 55, NUM, "Richtwert ca. 25–30 % der Gastraumfläche"),
    ("fl_lager", "Lager, Kühlung, Anlieferung (m²)", 25, NUM, ""),
    ("fl_wc", "WC (Herren, Damen, barrierefrei) (m²)", 22, NUM, "ca. 1 WC je 25 Plätze"),
    ("fl_eingang", "Eingang, Garderobe, Flure, Technik (m²)", 37, NUM, "Rest bis zur Gastrofläche"),
    ("sec", "Einnahmen und Gastro"),
    ("miete_m2", "Kaltmiete Wohnen (€/m² Wohnfläche)", "=950/85", EUR2, "Bauherr: 950 € für 85 m²; Portale Neubau Werlte ca. 10,7–11,0 €/m²"),
    ("pacht_m2", "Pacht Gastro (€/m²)", 10, EUR, "Annahme: ca. 8 % vom Umsatz (üblich 6–12 %), große Fläche günstiger je m²"),
    ("ruecklage", "Rücklagen (Anteil an Miete und Pacht)", 0.10, PCT, "Hausverwaltung, Instandhaltung, Leerstand; Nebenkosten werden umgelegt"),
    ("umsatz", "Gastro-Umsatz pro Monat (€)", 65000, EUR, "netto; ca. 4.100 € je Sitzplatz und Jahr bei 190 Plätzen (Österreich Median ca. 12.000 €, vorsichtig)"),
    ("marge", "Gastro-Marge vor Pacht", 0.305, PCT, "Branchen-Richtwert"),
    ("lohn", "Lohn des Bauherrn pro Monat (€)", 0, EUR, "Bauherr: wird vorerst nicht gerechnet"),
    ("sec", "Finanzierung (100 % Fremdkapital, kein Eigenkapital)"),
    ("kfw_we", "KfW 297/298: Kreditrahmen je Wohneinheit (€)", 150000, EUR, "mit QNG-Zertifikat, ohne QNG 100.000 € (Stand Ratgeber Okt. 2026)"),
    ("kfw_m2", "KfW 299: Kreditrahmen je m² Nettogrundfläche (€)", 2000, EUR, "mit QNG-PLUS/PREMIUM, ohne QNG 1.500 € (Stand Ratgeber Okt. 2026)"),
    ("z_kfw_wohn", "Zins KfW 297 und 298 (effektiv, 10 Jahre fest)", 0.025, PCT2, "Annahme: Ratgeber nennen 0,6 % bis 3,05 %. Bei Hausbank/KfW bestätigen"),
    ("z_kfw_gewerbe", "Zins KfW 299 (effektiv, 10 Jahre fest)", 0.03, PCT2, "Annahme, Nichtwohngebäude teurer als Wohnen"),
    ("z_bank", "Zins Hausbank (Restdarlehen, 10 Jahre fest)", 0.04, PCT2, "Annahme, Stand Bauzinsen Sept./Okt. 2026"),
    ("tilgung", "Anfangstilgung p. a.", 0.01, PCT, "Bauherr; Restschuld wird nach der Zinsbindung angeschlossen"),
    ("bauzeit", "Bauzeit (Monate)", 15, NUM, "feste Tabelle im Blatt Bauphase (15 Monate)"),
    ("aufschub", "Tilgungsfreie Anlaufzeit nach Bau (Monate)", 12, NUM, "feste Tabelle im Blatt Bauphase (12 Monate), mit Bank zu verhandeln"),
    ("bereit", "Bereitstellungszins p. a.", 0.03, PCT, "ab Monat 7 auf noch nicht abgerufene Bausumme"),
    ("bereit_ab", "Bereitstellungszins ab Monat", 7, NUM, ""),
    ("sec", "Wertermittlung (Ertragswertverfahren nach ImmoWertV)"),
    ("lzins_wohn", "Liegenschaftszins Wohnen", 0.04, PCT2, "Annahme: Mehrfamilienhaus ländlicher Raum ca. 3,5–4,5 %"),
    ("lzins_buero", "Liegenschaftszins Büro", 0.06, PCT2, "Annahme: Büro/Geschäft ca. 5–7 %; Ankermieter-Vertrag 10 Jahre"),
    ("lzins_gastro", "Liegenschaftszins Gastro", 0.065, PCT2, "Annahme: Gastro-Pacht höheres Risiko, ca. 6–7,5 %"),
    ("rnd", "Restnutzungsdauer Wohnen (Jahre)", 80, NUM, "Neubau, Annahme"),
    ("rnd_gew", "Restnutzungsdauer Büro und Gastro (Jahre)", 60, NUM, "Annahme, Ausbau kürzer"),
    ("verw_we", "Verwaltungskosten Wohnen je Wohneinheit und Jahr (€)", 360, EUR, "Annahme in Anlehnung an ImmoWertV-Ansätze"),
    ("instand_wohn", "Instandhaltung Wohnen (€/m² Wohnfläche und Jahr)", 12, EUR, "Annahme Neubau"),
    ("maw_wohn", "Mietausfallwagnis Wohnen", 0.02, PCT, "Annahme"),
    ("verw_gew", "Verwaltungskosten Gewerbe (Anteil am Rohertrag)", 0.03, PCT, "Annahme"),
    ("instand_gew", "Instandhaltung Gewerbe (€/m² und Jahr)", 8, EUR, "Annahme"),
    ("maw_gew", "Mietausfallwagnis Gewerbe", 0.04, PCT, "Annahme, Gastro als Mieter riskanter"),
    ("maw_buero", "Mietausfallwagnis Büro (Ankermieter)", 0.02, PCT, "Annahme: bonitätsstarker Mieter mit 10-Jahres-Vertrag"),
    ("abschlag", "Sicherheitsabschlag Beleihungswert", 0.10, PCT, "Annahme der Bank, üblich 10–20 %"),
    ("sec", "Prognose"),
    ("g_miete", "Mietsteigerung pro Jahr", 0.015, PCT, "Annahme"),
    ("g_umsatz", "Umsatzsteigerung Gastro pro Jahr", 0.015, PCT, "Annahme"),
    ("g_index", "Indexierung Büromieten pro Jahr", 0.02, PCT, "Annahme: Indexmiete, zieht Inflation nach"),
]
put(sA, "A3", "Annahme", font=hdr_font, fill=hdr_fill)
put(sA, "B3", "Wert", font=hdr_font, fill=hdr_fill)
put(sA, "C3", "Quelle / Hinweis", font=hdr_font, fill=hdr_fill)
for it in ASSUME:
    if it[0] == "sec":
        section(sA, row, it[1], 3)
        row += 1
        continue
    key, label, val, fmt, nt = it
    put(sA, f"A{row}", label)
    c = put(sA, f"B{row}", val, fmt, font=inp, fill=key_fill if key in ("z_kfw_wohn", "z_kfw_gewerbe", "z_bank", "tilgung", "miete_m2", "umsatz", "gastro_ausbau") else None)
    put(sA, f"C{row}", nt, font=note)
    A[key] = f"Annahmen!$B${row}"
    row += 1
sA.freeze_panes = "A4"
put(sA, f"A{row + 1}", "Gelb hinterlegt: wichtigste Stellschrauben für die Bankverhandlung.", font=note, border=False)

# =====================================================================================
# Flächen und Mieten
# =====================================================================================
sF = sheet("Flächen und Mieten", "Flächenprogramm und Mietaufstellung", "Grundfläche 32 × 18 m (GRZ-Maximum): Gastro im EG, 2 Ankermieter-Büros und 3 Wohnungen im 1. OG, 5 Wohnungen im Staffelgeschoss.", [46, 14, 14, 16, 16, 18, 18])
header(sF, 4, ["Geschoss", "BGF (m²)", "Nutzung", "Einheiten", "Fläche (m²)", "", ""])
put(sF, "A5", "Erdgeschoss"); put(sF, "B5", f"={A['bgf_eg']}", NUM, link); put(sF, "C5", "Gastro"); put(sF, "D5", 1, NUM); put(sF, "E5", f"={A['gastro_m2']}", NUM, link)
put(sF, "A6", "1. Obergeschoss"); put(sF, "B6", f"={A['bgf_og']}", NUM, link); put(sF, "C6", "Büro + Wohnen"); put(sF, "D6", f"=2+{A['n_og']}", NUM); put(sF, "E6", f"={A['wf_og']}+{A['b1_m2']}+{A['b2_m2']}", NUM)
put(sF, "A7", "Staffelgeschoss (Holzbau)"); put(sF, "B7", f"={A['bgf_st']}", NUM, link); put(sF, "C7", "Wohnen"); put(sF, "D7", f"={A['n_st']}", NUM, link); put(sF, "E7", f"={A['wf_st']}", NUM, link)
put(sF, "A8", "Summe", font=bold); put(sF, "B8", "=SUM(B5:B7)", NUM, bold); put(sF, "C8", ""); put(sF, "D8", "=D5+D6+D7", NUM, bold); put(sF, "E8", "=SUM(E5:E7)", NUM, bold)
put(sF, "A9", "davon Wohneinheiten / Wohnfläche"); put(sF, "D9", f"={A['n_og']}+{A['n_st']}", NUM); put(sF, "E9", f"={A['wf_og']}+{A['wf_st']}", NUM)
reg("bgf", sF, "B8"); reg("n_we", sF, "D9"); reg("wf", sF, "E9")
header(sF, 11, ["Einheit", "Geschoss", "Fläche (m²)", "Nutzung", "Kaltmiete / m²", "Kaltmiete / Monat", "Kaltmiete / Jahr"])
for i in range(8):
    r = 12 + i
    og = i < 3
    put(sF, f"A{r}", f"WE {i + 1}")
    put(sF, f"B{r}", "1. OG" if og else "Staffel")
    put(sF, f"C{r}", f"={A['wf_og']}/{A['n_og']}" if og else f"={A['wf_st']}/{A['n_st']}", "0.0")
    put(sF, f"D{r}", f'=IF({i + 1}>{A["n_og"]}+{A["n_st"]}-{A["eigen"]},"Eigennutzung","vermietet")')
    put(sF, f"E{r}", f"={A['miete_m2']}", EUR2, link)
    put(sF, f"F{r}", f"=C{r}*E{r}", EUR)
    put(sF, f"G{r}", f"=F{r}*12", EUR)
put(sF, "A20", "Summe Wohnen (alle Wohnungen, marktüblich)", font=bold); put(sF, "C20", "=SUM(C12:C19)", "0.0", bold); put(sF, "F20", "=SUM(F12:F19)", EUR, bold); put(sF, "G20", "=SUM(G12:G19)", EUR, bold)
put(sF, "A21", "davon vermietet (Einnahmen)", font=bold); put(sF, "F21", '=SUMIF(D12:D19,"vermietet",F12:F19)', EUR, bold); put(sF, "G21", "=F21*12", EUR, bold)
put(sF, "A22", "Gastro-Pacht (Gastro zahlt an das Haus)", font=bold); put(sF, "C22", f"={A['gastro_m2']}", "0.0"); put(sF, "E22", f"={A['pacht_m2']}", EUR2, link); put(sF, "F22", "=C22*E22", EUR, bold); put(sF, "G22", "=F22*12", EUR, bold)
put(sF, "A23", "Büro 1 (Ankermieter, Versicherung o. ä.)", font=bold); put(sF, "B23", "1. OG"); put(sF, "C23", f"={A['b1_m2']}", "0.0"); put(sF, "D23", f'={A["b_laufzeit"]}&" Jahre fest"'); put(sF, "E23", f"={A['b1_miete']}", EUR2, link); put(sF, "F23", "=C23*E23", EUR, bold); put(sF, "G23", "=F23*12", EUR, bold)
put(sF, "A24", "Büro 2 (Makler o. ä.)", font=bold); put(sF, "B24", "1. OG"); put(sF, "C24", f"={A['b2_m2']}", "0.0"); put(sF, "D24", f'={A["b_laufzeit"]}&" Jahre fest"'); put(sF, "E24", f"={A['b2_miete']}", EUR2, link); put(sF, "F24", "=C24*E24", EUR, bold); put(sF, "G24", "=F24*12", EUR, bold)
put(sF, "A25", "Büromieten gesamt", font=bold); put(sF, "C25", "=C23+C24", "0.0", bold); put(sF, "F25", "=F23+F24", EUR, bold); put(sF, "G25", "=G23+G24", EUR, bold)
put(sF, "A26", "Rohertrag gesamt (Wohnen vermietet + Büro + Pacht)", font=bold); put(sF, "F26", "=F21+F22+F25", EUR, bold); put(sF, "G26", "=G21+G22+G25", EUR, bold)
reg("miete_monat", sF, "F21"); reg("pacht_monat", sF, "F22"); reg("miete_voll_monat", sF, "F20"); reg("buero_monat", sF, "F25"); reg("buero1_monat", sF, "F23"); reg("buero2_monat", sF, "F24"); reg("rohertrag_monat", sF, "F26")
put(sF, "A28", "Nebenkosten (Grundsteuer, Versicherung, Betriebskosten) werden auf die Mieter umgelegt und sind hier nicht gerechnet. Mieten sind Annahmen des Bauherrn bzw. Planungsannahmen.", font=note, border=False)

# =====================================================================================
# Gewerbe und Anker
# =====================================================================================
sW = sheet("Gewerbe und Anker", "Gewerbeflächen: Gastro-Flächenbedarf und Ankermieter Büro", "Gastro im ganzen EG nach Bedarf (aus Plätzen), zwei Büros im 1. OG als langfristige Ankermieter (Aufzug, getrennter Eingang).", [52, 16, 16, 16, 16, 16, 16, 30])
header(sW, 4, ["Gastro-Flächenbedarf", "Menge", "m² je Einheit", "Fläche (m²)", "", "", "", "Hinweis"])
need = [
    ("Gastraum inkl. Lounge", f"={A['plaetze_gast']}", f"={A['m2_platz']}", "=B5*C5", "Plätze × Richtwert"),
    ("Séparée (Feiern)", f"={A['plaetze_sep']}", f"={A['m2_platz_sep']}", "=B6*C6", "Festtafel"),
    ("Bar und Theken-Zone", 1, f"={A['fl_bar']}", "=B7*C7", ""),
    ("Küche mit Spülküche", 1, f"={A['fl_kueche']}", "=B8*C8", ""),
    ("Lager, Kühlung, Anlieferung", 1, f"={A['fl_lager']}", "=B9*C9", ""),
    ("WC (Herren, Damen, barrierefrei)", 1, f"={A['fl_wc']}", "=B10*C10", ""),
    ("Eingang, Garderobe, Flure, Technik", 1, f"={A['fl_eingang']}", "=B11*C11", ""),
]
for i, (lab, m, c, f_, h) in enumerate(need):
    r = 5 + i
    put(sW, f"A{r}", lab); put(sW, f"B{r}", m, NUM, link if isinstance(m, str) else None); put(sW, f"C{r}", c, "0.0", link if isinstance(c, str) else None); put(sW, f"D{r}", f_, NUM); put(sW, f"H{r}", h, font=note)
put(sW, "A12", "Gastrofläche aus Bedarf", font=bold); put(sW, "D12", "=SUM(D5:D11)", NUM, bold, fill=key_fill)
put(sW, "A13", "Gastrofläche im Modell (Annahmen)"); put(sW, "D13", f"={A['gastro_m2']}", NUM, link)
put(sW, "A14", "Abweichung (Bedarf minus Modell)"); put(sW, "D14", "=D12-D13", EURS.replace(' "€"',''))
put(sW, "A15", "Plätze innen gesamt"); put(sW, "D15", "=B5+B6", NUM)
put(sW, "A16", "Bruttofläche je Platz (m²)"); put(sW, "D16", "=D13/D15", "0.00"); put(sW, "H16", "Richtwert Gesamtfläche 2,5–3 m² je Platz", font=note)
put(sW, "A17", "Gastro-Umsatz je Platz und Jahr (€)"); put(sW, "D17", f"={A['umsatz']}*12/D15", EUR); put(sW, "H17", "vorsichtig, Österreich Median ca. 12.000 €", font=note)
put(sW, "A18", "Pacht in % vom Gastro-Umsatz"); put(sW, "D18", f"='Flächen und Mieten'!F22/{A['umsatz']}", PCT); put(sW, "H18", "üblich 6–12 %", font=note)
reg("g_plaetze", sW, "D15"); reg("g_bedarf", sW, "D12"); reg("g_umsatz_platz", sW, "D17"); reg("g_pacht_quote", sW, "D18"); reg("g_m2_platz", sW, "D16")
header(sW, 21, ["Ankermieter Büro", "Fläche (m²)", "Miete €/m²", "Miete / Monat", "Miete / Jahr", "Laufzeit (Jahre)", "Miete über Laufzeit", "Anteil am Rohertrag"])
sW.row_dimensions[21].height = 30
for i, (nm, m2k, mk) in enumerate((("Büro 1: Versicherungsgesellschaft o. ä.", "b1_m2", "b1_miete"), ("Büro 2: Makler o. ä.", "b2_m2", "b2_miete"))):
    r = 22 + i
    put(sW, f"A{r}", nm); put(sW, f"B{r}", f"={A[m2k]}", NUM, link); put(sW, f"C{r}", f"={A[mk]}", EUR2, link)
    put(sW, f"D{r}", f"=B{r}*C{r}", EUR); put(sW, f"E{r}", f"=D{r}*12", EUR); put(sW, f"F{r}", f"={A['b_laufzeit']}", NUM, link)
    put(sW, f"G{r}", f"=E{r}*((1+{A['g_index']})^F{r}-1)/{A['g_index']}", EUR); put(sW, f"H{r}", f"=E{r}/'Flächen und Mieten'!$G$26", PCT)
put(sW, "A24", "Summe Büro", font=bold)
for col, fm in (("B", NUM), ("D", EUR), ("E", EUR), ("G", EUR), ("H", PCT)):
    put(sW, f"{col}24", f"=SUM({col}22:{col}23)", fm, bold)
put(sW, "C24", "=D24/B24", EUR2, bold)
put(sW, "A26", "Deckung des Kapitaldienstes durch langfristige Mieten", font=bold, border=False)
put(sW, "A27", "Kapitaldienst pro Jahr"); put(sW, "D27", "='Tilgungsplan'!N3*12", EUR)
put(sW, "A28", "Büromieten nach Rücklagen pro Jahr"); put(sW, "D28", f"=E24*(1-{A['ruecklage']})", EUR)
put(sW, "A29", "davon gedeckter Anteil des Kapitaldienstes"); put(sW, "D29", "=D28/D27", PCT)
put(sW, "A30", "Wohnen und Büro nach Rücklagen pro Jahr"); put(sW, "D30", f"=('Flächen und Mieten'!G21+E24)*(1-{A['ruecklage']})", EUR)
put(sW, "A31", "davon gedeckter Anteil des Kapitaldienstes (ohne Gastro)"); put(sW, "D31", "=D30/D27", PCT, bold, fill=key_fill)
put(sW, "A32", "Mietdauer-gewichtete Restlaufzeit der Büro-Verträge (Jahre)"); put(sW, "D32", "=SUMPRODUCT(E22:E23,F22:F23)/E24", "0.0")
reg("b_anteil_kd", sW, "D29"); reg("b_wohn_anteil_kd", sW, "D31"); reg("b_miete_jahr", sW, "E24"); reg("b_m2", sW, "B24"); reg("b_miete_m2", sW, "C24"); reg("b_ueber_laufzeit", sW, "G24")
put(sW, "A34", "Stellplatzbedarf (grobe Annahme)", font=bold, border=False)
put(sW, "A35", "Wohnungen: 1,5 je Wohnung"); put(sW, "D35", f"=({A['n_og']}+{A['n_st']})*1.5", "0.0")
put(sW, "A36", "Gastro: 1 je 10 m² Gastraum (Gastraum, Séparée, Bar)"); put(sW, "D36", "=(D5+D6+D7)/10", "0.0")
put(sW, "A37", "Büro: 1 je 30 m²"); put(sW, "D37", "=B24/30", "0.0")
put(sW, "A38", "Stellplatzbedarf gesamt", font=bold); put(sW, "D38", "=SUM(D35:D37)", "0", bold)
put(sW, "H38", "Stellplatzsatzung der Stadt gilt verbindlich", font=note)
reg("stellplatz_bedarf", sW, "D38")
put(sW, "A40", "Hinweis: Büromieten und Laufzeiten sind Annahmen, für Werlte liegen keine Büromarktdaten vor. Anker-Mietverträge (Vorverträge) vor Baubeginn sichern.", font=note, border=False)

# =====================================================================================
# Kosten und Finanzierung
# =====================================================================================
sK = sheet("Kosten und Finanzierung", "Kosten und Finanzierungsplan", "Mittelverwendung und Mittelherkunft. 100 % Fremdfinanzierung, kein Eigenkapital.", [52, 18, 14, 40])
header(sK, 4, ["Mittelverwendung (Kosten)", "Betrag", "Anteil", "Rechnung"])
K = {}
rows = [
    ("land", "Grundstück (Kaufpreis)", f"={A['grund_m2']}*{A['preis_m2']}", "m² × Preis"),
    ("grest", "Grunderwerbsteuer", f"=B5*{A['grest']}", ""),
    ("notar", "Notar und Grundbuch", f"=B5*{A['notar']}", ""),
    ("land_ges", "Grundstück gesamt", "=SUM(B5:B7)", ""),
    ("bau_massiv", "Bau, Massivbau (BGF × Baukosten)", f"=({A['bgf_eg']}+{A['bgf_og']}+{A['bgf_st']})*{A['baukosten_m2']}", f'=TEXT({A["bgf_eg"]}+{A["bgf_og"]}+{A["bgf_st"]},"#,##0")&" m² × "&TEXT({A["baukosten_m2"]},"#,##0")&" €"'),
    ("holz", "Abschlag Holzbau Staffelgeschoss", f"=-{A['bgf_st']}*{A['holz_abschlag']}", f'=TEXT({A["bgf_st"]},"#,##0")&" m² × "&TEXT({A["holz_abschlag"]},"#,##0")&" €"'),
    ("terrasse", "Dachterrasse rundum", f"={A['terrasse_m2']}*{A['terrasse_preis']}", f'=TEXT({A["terrasse_m2"]},"#,##0")&" m² × "&TEXT({A["terrasse_preis"]},"#,##0")&" €"'),
    ("bau", "Bau gesamt", "=SUM(B9:B11)", ""),
    ("bnk", "Baunebenkosten", f"=B12*{A['bnk']}", "15 % vom Bau"),
    ("eh40", "Mehrkosten Effizienzhaus 40 und QNG-Nachweis", f"=(B12+B13)*{A['mehr_eh40']}", "3 % auf Bau inkl. Baunebenkosten"),
    ("ausbau", "Ausbau Gastro (Küche, Bar, Möbel, Technik) und Büros (Vermieter-Ausbau)", f"={A['gastro_ausbau']}+({A['b1_m2']}+{A['b2_m2']})*{A['b_ausbau']}", "Gastro 1.000 € je Platz, Büros 150 €/m²"),
    ("invest", "Investitionskosten ohne Finanzierung", "=B8+B12+B13+B14+B15", ""),
    ("fin", "Finanzierungskosten (Bauzeit, Bereitstellung, Anlaufzeit)", "=0", "aus Blatt Bauphase"),
    ("gesamt", "Gesamtkosten des Vorhabens", "=B16+B17", ""),
]
for i, (k, lab, fml, rc) in enumerate(rows):
    r = 5 + i
    bld = k in ("land_ges", "bau", "invest", "gesamt")
    put(sK, f"A{r}", lab, font=bold if bld else base)
    put(sK, f"B{r}", fml, EUR, bold if bld else base, fill=key_fill if k == "gesamt" else None)
    put(sK, f"C{r}", f"=B{r}/$B$18", PCT)
    put(sK, f"D{r}", rc, font=note)
    K[k] = f"B{r}"
    reg("k_" + k, sK, f"B{r}")
put(sK, "A19", "Kosten je m² BGF", font=base); put(sK, "B19", f"=B18/'Flächen und Mieten'!B8", EUR); reg("kosten_m2_bgf", sK, "B19")
put(sK, "A20", "Kosten je Wohneinheit (Gesamtkosten / 8, inkl. Gewerbe)", font=base); put(sK, "B20", "=B18/'Flächen und Mieten'!D9", EUR)

header(sK, 23, ["Mittelherkunft (Finanzierung)", "Betrag bei Rate-Start", "Anteil", "Zins / Programm"])
put(sK, "A24", "KfW 297 Klimafreundlicher Neubau (selbst genutzte Wohnungen)"); put(sK, "A25", "KfW 298 Klimafreundlicher Neubau (vermietete Wohnungen)"); put(sK, "A26", "KfW 299 Klimafreundlicher Neubau (Nichtwohngebäude: Gastro und Büros)"); put(sK, "A27", "Hausbank-Darlehen (Restfinanzierung inkl. Zinsen der Bauzeit)"); put(sK, "A28", "Eigenkapital"); put(sK, "A29", "Summe Finanzierung", font=bold)
put(sK, "B24", f"='Bauphase'!L33*{A['eigen']}/MAX(1,({A['n_og']}+{A['n_st']}))", EUR)
put(sK, "B25", f"='Bauphase'!L33-B24", EUR)
put(sK, "B26", "='Bauphase'!M33", EUR)
put(sK, "B27", "='Bauphase'!N33", EUR)
put(sK, "B28", 0, EUR, inp)
put(sK, "B29", "=SUM(B24:B28)", EUR, bold, fill=key_fill)
for r in range(24, 30):
    put(sK, f"C{r}", f"=B{r}/$B$29", PCT)
put(sK, "D24", f"={A['z_kfw_wohn']}", PCT2, link); put(sK, "D25", f"={A['z_kfw_wohn']}", PCT2, link); put(sK, "D26", f"={A['z_kfw_gewerbe']}", PCT2, link); put(sK, "D27", f"={A['z_bank']}", PCT2, link); put(sK, "D28", "")
put(sK, "A30", "Anteil KfW-Kredite an der Finanzierung", font=bold); put(sK, "B30", "=(B24+B25+B26)/B29", PCT, bold)
put(sK, "A31", "Mischzins aller Darlehen", font=bold); put(sK, "B31", f"=(B24*{A['z_kfw_wohn']}+B25*{A['z_kfw_wohn']}+B26*{A['z_kfw_gewerbe']}+B27*{A['z_bank']})/B29", PCT2, bold)
reg("kredit", sK, "B29"); reg("kredit_kfw_anteil", sK, "B30"); reg("mischzins", sK, "B31")
reg("kredit_297", sK, "B24"); reg("kredit_298", sK, "B25"); reg("kredit_299", sK, "B26"); reg("kredit_bank", sK, "B27")
put(sK, "A33", "KfW-Rahmen laut Programm (Stand Ratgeber Okt. 2026, bei Hausbank und KfW zu bestätigen):", font=bold, border=False)
put(sK, "A34", "KfW 297/298: Rahmen Wohnen (Wohneinheiten × 150.000 €)"); put(sK, "B34", f"=({A['n_og']}+{A['n_st']})*{A['kfw_we']}", EUR)
put(sK, "A35", "KfW 299: Rahmen Gastro und Büros (Nettogrundfläche × 2.000 €)"); put(sK, "B35", f"=({A['gastro_m2']}+{A['b1_m2']}+{A['b2_m2']})*{A['ngf_anteil']}*{A['kfw_m2']}", EUR)
put(sK, "A36", "KfW-Rahmen gesamt"); put(sK, "B36", "=B34+B35", EUR, bold)
put(sK, "A37", "Antrag nur mit Effizienzhaus 40, QNG-Zertifikat, Heizung ohne Öl, Gas und Biomasse, vor Baubeginn über die Hausbank.", font=note, border=False)
reg("kfw_rahmen", sK, "B36"); reg("kfw_rahmen_wohn", sK, "B34"); reg("kfw_rahmen_gastro", sK, "B35")

# =====================================================================================
# Bauphase
# =====================================================================================
sB = sheet("Bauphase", "Bauphase und Anlaufzeit: Abrufe, Zinsen, Kreditstand", "Monat 0 = Grundstück. Monate 1–15 Bau. Monate 16–27 tilgungsfreie Anlaufzeit. KfW-Darlehen werden anteilig zu den Ausgaben abgerufen, die Hausbank zahlt zusätzlich alle Zinsen.", [8, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 15, 15, 15])
put(sB, "A3", "Anteil KfW Wohnen an den Ausgaben", border=False); put(sB, "E3", f"=MIN(1,'Kosten und Finanzierung'!B34/'Kosten und Finanzierung'!B16)", PCT)
put(sB, "F3", "Anteil KfW Gastro", border=False); put(sB, "I3", f"=MIN(1-E3,'Kosten und Finanzierung'!B35/'Kosten und Finanzierung'!B16)", PCT)
put(sB, "J3", "Anteil Hausbank", border=False); put(sB, "L3", "=1-E3-I3", PCT)
header(sB, 5, ["Monat", "Phase", "Ausgaben (Grundstück, Bau)", "Offene Bausumme", "Abruf KfW Wohnen", "Abruf KfW Gastro", "Zinsen KfW Wohnen", "Zinsen KfW Gastro", "Zinsen Hausbank", "Bereitstellungs-zins", "Abruf Hausbank", "Stand KfW Wohnen", "Stand KfW Gastro", "Stand Hausbank"])
sB.row_dimensions[5].height = 42
bau_sum = "('Kosten und Finanzierung'!B16-'Kosten und Finanzierung'!B8)"
for m in range(0, 28):
    r = 6 + m
    put(sB, f"A{r}", m, NUM)
    put(sB, f"B{r}", "Grundstück" if m == 0 else ("Bau" if m <= 15 else "Anlaufzeit"))
    if m == 0:
        put(sB, f"C{r}", "='Kosten und Finanzierung'!B8", EUR)
        put(sB, f"D{r}", f"={bau_sum}", EUR)
        for col in "GHIJ":
            put(sB, f"{col}{r}", 0, EUR)
    else:
        put(sB, f"C{r}", f"=IF(A{r}<={A['bauzeit']},{bau_sum}/{A['bauzeit']},0)", EUR)
        put(sB, f"D{r}", f"=IF(A{r}<={A['bauzeit']},{bau_sum}*({A['bauzeit']}-(A{r}-1))/{A['bauzeit']},0)", EUR)
        put(sB, f"G{r}", f"=L{r - 1}*{A['z_kfw_wohn']}/12", EUR)
        put(sB, f"H{r}", f"=M{r - 1}*{A['z_kfw_gewerbe']}/12", EUR)
        put(sB, f"I{r}", f"=N{r - 1}*{A['z_bank']}/12", EUR)
        put(sB, f"J{r}", f"=IF(AND(A{r}>={A['bereit_ab']},A{r}<={A['bauzeit']}),D{r}*{A['bereit']}/12,0)", EUR)
    put(sB, f"E{r}", f"=C{r}*$E$3", EUR)
    put(sB, f"F{r}", f"=C{r}*$I$3", EUR)
    put(sB, f"K{r}", f"=C{r}*$L$3+G{r}+H{r}+I{r}+J{r}", EUR)
    put(sB, f"L{r}", f"=E{r}" if m == 0 else f"=L{r - 1}+E{r}", EUR)
    put(sB, f"M{r}", f"=F{r}" if m == 0 else f"=M{r - 1}+F{r}", EUR)
    put(sB, f"N{r}", f"=K{r}" if m == 0 else f"=N{r - 1}+K{r}", EUR)
# Summenzeile 34, Endstände (Rate-Start) stehen in Zeile 33 (Monat 27)
put(sB, "A34", "Summe", font=bold)
for col in "CEFGHIJK":
    put(sB, f"{col}34", f"=SUM({col}6:{col}33)", EUR, bold)
put(sB, "B34", "Summen", font=bold)
put(sB, "B33", "Rate-Start", font=bold)
put(sB, "A36", "Finanzierungskosten gesamt (Zinsen und Bereitstellung):", font=bold, border=False); put(sB, "G36", "=SUM(G34:J34)", EUR, bold)
put(sB, "A37", "Kontrolle: Stand Rate-Start minus Ausgaben minus Finanzierungskosten (muss 0 sein)", border=False); put(sB, "G37", "=ROUND(L33+M33+N33-C34-G36,2)", EUR)
# Zeile 33 enthält die Summen; die Finanzierungskosten stehen in den Spalten G–J
sK["B17"].value = "='Bauphase'!G36"
reg("fin_kosten", sB, "G36")

# =====================================================================================
# Tilgungsplan (monatlich) und Jahresübersicht
# =====================================================================================
sT = sheet("Tilgungsplan", "Abzahlungsplan (Tilgungsplan) monatlich, 35 Jahre", "Annuitätendarlehen: Rate = Darlehen × (Zins + Anfangstilgung) / 12. Nach 10 Jahren Zinsbindung wird der gleiche Zins angenommen.", [8, 8, 14, 14, 15, 14, 14, 15, 14, 14, 15, 14, 14, 14, 16])
put(sT, "A3", "Rate pro Monat", font=bold, border=False)
put(sT, "C3", f"=E6*({A['z_kfw_wohn']}+{A['tilgung']})/12", EUR, bold); put(sT, "F3", f"=H6*({A['z_kfw_gewerbe']}+{A['tilgung']})/12", EUR, bold); put(sT, "I3", f"=K6*({A['z_bank']}+{A['tilgung']})/12", EUR, bold); put(sT, "N3", "=C3+F3+I3", EUR, bold, fill=key_fill)
put(sT, "C2", "KfW Wohnen", font=bold, border=False); put(sT, "F2", "KfW Gastro", font=bold, border=False); put(sT, "I2", "Hausbank", font=bold, border=False); put(sT, "N2", "Summe", font=bold, border=False)
header(sT, 5, ["Monat", "Jahr", "Zins KfW Wohnen", "Tilgung KfW Wohnen", "Rest KfW Wohnen", "Zins KfW Gastro", "Tilgung KfW Gastro", "Rest KfW Gastro", "Zins Hausbank", "Tilgung Hausbank", "Rest Hausbank", "Zinsen gesamt", "Tilgung gesamt", "Rate gesamt", "Restschuld gesamt"])
sT.row_dimensions[5].height = 42
put(sT, "A6", 0, NUM); put(sT, "B6", 0, NUM)
put(sT, "E6", "='Bauphase'!L33", EUR); put(sT, "H6", "='Bauphase'!M33", EUR); put(sT, "K6", "='Bauphase'!N33", EUR); put(sT, "O6", "=E6+H6+K6", EUR)
for m in range(1, 421):
    r = 6 + m
    sT.cell(row=r, column=1, value=m).font = base
    sT.cell(row=r, column=2, value=f"=ROUNDUP(A{r}/12,0)").font = base
    for (zc, tc, rc, zin, rate) in (("C", "D", "E", A["z_kfw_wohn"], "$C$3"), ("F", "G", "H", A["z_kfw_gewerbe"], "$F$3"), ("I", "J", "K", A["z_bank"], "$I$3")):
        sT[f"{zc}{r}"] = f"={rc}{r - 1}*{zin}/12"
        sT[f"{tc}{r}"] = f"=MIN({rate}-{zc}{r},{rc}{r - 1})"
        sT[f"{rc}{r}"] = f"={rc}{r - 1}-{tc}{r}"
    sT[f"L{r}"] = f"=C{r}+F{r}+I{r}"
    sT[f"M{r}"] = f"=D{r}+G{r}+J{r}"
    sT[f"N{r}"] = f"=L{r}+M{r}"
    sT[f"O{r}"] = f"=E{r}+H{r}+K{r}"
    for col in range(3, 16):
        c = sT.cell(row=r, column=col)
        c.number_format = EUR
        c.font = base
sT.freeze_panes = "C6"

sJ = sheet("Tilgung Jahre", "Abzahlungsplan nach Jahren", "Zusammenfassung des monatlichen Tilgungsplans. Zinsbindung 10 Jahre, danach gleicher Zins angenommen.", [8, 16, 16, 16, 18, 18, 14])
header(sJ, 4, ["Jahr", "Zinsen", "Tilgung", "Kapitaldienst (Rate)", "Restschuld Jahresende", "davon KfW", "Zinsbindung"])
sJ.row_dimensions[4].height = 30
for y in range(1, 36):
    r = 4 + y
    put(sJ, f"A{r}", y, NUM)
    put(sJ, f"B{r}", f"=SUMIFS('Tilgungsplan'!$L$7:$L$426,'Tilgungsplan'!$B$7:$B$426,A{r})", EUR)
    put(sJ, f"C{r}", f"=SUMIFS('Tilgungsplan'!$M$7:$M$426,'Tilgungsplan'!$B$7:$B$426,A{r})", EUR)
    put(sJ, f"D{r}", f"=B{r}+C{r}", EUR)
    put(sJ, f"E{r}", f"=INDEX('Tilgungsplan'!$O$7:$O$426,A{r}*12)", EUR)
    put(sJ, f"F{r}", f"=INDEX('Tilgungsplan'!$E$7:$E$426,A{r}*12)+INDEX('Tilgungsplan'!$H$7:$H$426,A{r}*12)", EUR)
    put(sJ, f"G{r}", "bis Jahr 10" if y <= 10 else "Anschluss")
put(sJ, "A41", "Summe", font=bold)
put(sJ, "B41", "=SUM(B5:B39)", EUR, bold); put(sJ, "C41", "=SUM(C5:C39)", EUR, bold); put(sJ, "D41", "=SUM(D5:D39)", EUR, bold)
reg("rate_jahr1", sJ, "D5"); reg("rate_monat", sT, "N3"); reg("rest_10", sJ, "E14"); reg("rest_20", sJ, "E24"); reg("rest_35", sJ, "E39")
reg("zins_jahr1", sJ, "B5"); reg("tilg_jahr1", sJ, "C5"); reg("rate_w", sT, "C3"); reg("rate_g", sT, "F3"); reg("rate_b", sT, "I3")
ch = LineChart()
ch.title = "Restschuld nach Jahren"
ch.y_axis.title = "€"
ch.x_axis.title = "Jahr"
ch.height = 8
ch.width = 18
data = Reference(sJ, min_col=5, min_row=4, max_row=39)
ch.add_data(data, titles_from_data=True)
ch.set_categories(Reference(sJ, min_col=1, min_row=5, max_row=39))
ch.legend = None
sJ.add_chart(ch, "I4")

# =====================================================================================
# Gastro Betrieb
# =====================================================================================
sG = sheet("Gastro Betrieb", "Gastro-Betrieb: Umsatz, Kosten, Ergebnis pro Monat", "Richtwerte aus der Branche, keine Werte aus Werlte. Lohn des Bauherrn ist nicht gerechnet.", [46, 14, 16, 40])
header(sG, 4, ["Posten", "Anteil", "Betrag / Monat", "Hinweis"])
put(sG, "A5", "Umsatz (netto)", font=bold); put(sG, "B5", ""); put(sG, "C5", f"={A['umsatz']}", EUR, link)
costs = [("Wareneinsatz (Einkauf Essen und Getränke)", 0.28), ("Personal (ohne Lohn des Bauherrn)", 0.30), ("Energie, Wasser, Müll", 0.03), ("Reinigung, Wäsche, Verbrauchsmaterial", 0.02), ("Werbung und Marketing", 0.015), ("Reparaturen, Wartung, Kassensystem", 0.015), ("Sonstiges", 0.015), ("Versicherungen, GEMA, Gebühren", 0.01), ("Steuerberater, Buchhaltung", 0.01)]
for i, (lab, p) in enumerate(costs):
    r = 6 + i
    put(sG, f"A{r}", lab); put(sG, f"B{r}", p, PCT, inp); put(sG, f"C{r}", f"=-$C$5*B{r}", EUR)
put(sG, "A15", "Summe Betriebskosten ohne Pacht", font=bold); put(sG, "B15", "=SUM(B6:B14)", PCT, bold); put(sG, "C15", "=SUM(C6:C14)", EUR, bold)
put(sG, "A16", "Gewinn vor Pacht", font=bold); put(sG, "B16", "=1-B15", PCT, bold); put(sG, "C16", "=C5+C15", EUR, bold)
put(sG, "A17", "Pacht an das Haus"); put(sG, "C17", "=-'Flächen und Mieten'!F22", EUR)
put(sG, "A18", "Lohn des Bauherrn"); put(sG, "C18", f"=-{A['lohn']}", EUR, link)
put(sG, "A19", "Betriebsergebnis nach Pacht", font=bold); put(sG, "C19", "=C16+C17+C18", EUR, bold, fill=key_fill)
put(sG, "A20", "Break-even-Umsatz des Betriebs (Ergebnis nach Pacht = 0)"); put(sG, "C20", f"=('Flächen und Mieten'!F22+{A['lohn']})/B16", EUR)
put(sG, "D16", "Marge laut Annahmen muss mit 30,5 % übereinstimmen", font=note)
reg("g_gewinn_vor_pacht", sG, "C16"); reg("g_ergebnis", sG, "C19"); reg("g_breakeven", sG, "C20")
header(sG, 23, ["Umsatz pro Monat", "", "Gewinn vor Pacht", "Gewinn nach Pacht"])
for i, u in enumerate([40000, 50000, 65000, 80000, 90000]):
    r = 24 + i
    put(sG, f"A{r}", u, EUR, inp); put(sG, f"C{r}", f"=A{r}*$B$16", EUR); put(sG, f"D{r}", f"=C{r}-'Flächen und Mieten'!$F$22-{A['lohn']}", EURS)
put(sG, "A30", "Bei sehr niedrigem Umsatz drücken Fixkosten stärker: die Rechnung ist dort zu günstig.", font=note, border=False)

# =====================================================================================
# Ertrag und Cashflow
# =====================================================================================
sC = sheet("Ertrag und Cashflow", "Ertrag und Kapitaldienst (erstes Jahr nach der Anlaufzeit)", "Für die Bank: reicht der Ertrag für Zinsen und Tilgung? Kapitaldienstdeckung (DSCR) = Ertrag vor Kapitaldienst / Kapitaldienst.", [64, 18, 18, 46])
header(sC, 4, ["Position", "pro Monat", "pro Jahr", "Hinweis"])
lines = [
    ("Kaltmiete Wohnen (vermietete Wohnungen)", "='Flächen und Mieten'!F21", ""),
    ("Büromieten (2 Ankermieter)", "='Flächen und Mieten'!F25", "10 Jahre fest, Indexmiete"),
    ("Pacht Gastro", "='Flächen und Mieten'!F22", "Gastro zahlt an das Haus"),
    ("Rücklagen (Verwaltung, Instandhaltung, Leerstand)", f"=-{A['ruecklage']}*(B5+B6+B7)", "10 % von Miete, Büro und Pacht"),
    ("Nettoertrag Immobilie", "=SUM(B5:B8)", ""),
    ("Betriebsergebnis Gastro nach Pacht", "='Gastro Betrieb'!C19", "Betreiber = Bauherr, ohne Lohn"),
    ("Nettoertrag vor Kapitaldienst", "=B9+B10", ""),
    ("Kapitaldienst (Zinsen und Tilgung aller Darlehen)", "=-'Tilgungsplan'!N3", ""),
    ("Ergebnis pro Monat nach Kapitaldienst", "=B11+B12", "ohne Lohn des Bauherrn"),
]
for i, (lab, fml, h) in enumerate(lines):
    r = 5 + i
    b = i in (4, 6, 8)
    sg = i in (3, 7, 8)
    put(sC, f"A{r}", lab, font=bold if b else base)
    put(sC, f"B{r}", fml, EURS if sg else EUR, bold if b else base, fill=key_fill if i == 8 else None)
    put(sC, f"C{r}", f"=B{r}*12", EURS if sg else EUR, bold if b else base)
    put(sC, f"D{r}", h, font=note)
put(sC, "A15", "Kapitaldienstdeckung gesamt (DSCR)", font=bold); put(sC, "B15", "=B11/-B12", X, bold, fill=key_fill); put(sC, "D15", "Bank verlangt meist mindestens 1,2", font=note)
put(sC, "A16", "Kapitaldienstdeckung nur Immobilie (Wohnen, Büro, Pacht)", font=bold); put(sC, "B16", "=B9/-B12", X, bold); put(sC, "D16", "ohne Gastro-Gewinn", font=note)
put(sC, "A17", "Kapitaldienstdeckung nur langfristige Mieten (Wohnen, Büro)", font=bold); put(sC, "B17", f"=(B5+B6)*(1-{A['ruecklage']})/-B12", X, bold); put(sC, "D17", "ohne Pacht und Gastro: Ankermieter helfen hier", font=note)
put(sC, "A18", "Zinsdeckung (Ertrag vor Kapitaldienst / Zinsen)"); put(sC, "B18", "=B11/('Tilgung Jahre'!B5/12)", X)
put(sC, "A19", "Anfangsrendite auf Gesamtkosten (Nettoertrag Immobilie p. a.)"); put(sC, "B19", "=C9/'Kosten und Finanzierung'!B18", PCT2)
put(sC, "A20", "Break-even Gastro-Umsatz (Haus insgesamt Ergebnis = 0)"); put(sC, "B20", f"=(-B9-B12+'Flächen und Mieten'!F22+{A['lohn']})/{A['marge']}", EUR); put(sC, "D20", "Umsatz, ab dem Zinsen und Tilgung aller Darlehen bezahlt sind", font=note)
put(sC, "A21", "Anteil der Büro-Ankermieter am Rohertrag"); put(sC, "B21", "='Flächen und Mieten'!G25/'Flächen und Mieten'!G26", PCT)
for k_, c_ in (("c_miete", "B5"), ("c_buero", "B6"), ("c_pacht", "B7"), ("c_rueck", "B8"), ("c_netto_immo", "B9"), ("c_gastro", "B10"), ("c_netto", "B11"), ("c_kd", "B12"), ("c_ergebnis", "B13"), ("dscr", "B15"), ("dscr_immo", "B16"), ("dscr_lang", "B17"), ("zinsdeckung", "B18"), ("anfangsrendite", "B19"), ("breakeven_haus", "B20"), ("anteil_buero", "B21")):
    reg(k_, sC, c_)

# =====================================================================================
# Ertragswert
# =====================================================================================
sE = sheet("Ertragswert", "Ertragswert und Beleihung", "Ertragswertverfahren nach ImmoWertV (vereinfacht) getrennt nach Wohnen, Büro und Gastro. Ein Gutachter der Bank ermittelt den verbindlichen Beleihungswert.", [58, 16, 16, 16, 18, 40])
header(sE, 4, ["Ertragswert nach Nutzung", "Wohnen", "Büro", "Gastro", "Summe", "Hinweis"])
FM = "'Flächen und Mieten'!"
put(sE, "A5", "Rohertrag pro Jahr", font=bold); put(sE, "B5", f"={FM}G20", EUR); put(sE, "C5", f"={FM}G25", EUR); put(sE, "D5", f"={FM}G22", EUR); put(sE, "E5", "=SUM(B5:D5)", EUR, bold)
put(sE, "A6", "Verwaltungskosten"); put(sE, "B6", f"=-({A['n_og']}+{A['n_st']})*{A['verw_we']}", EUR); put(sE, "C6", f"=-C5*{A['verw_gew']}", EUR); put(sE, "D6", f"=-D5*{A['verw_gew']}", EUR)
put(sE, "A7", "Instandhaltung"); put(sE, "B7", f"=-({A['wf_og']}+{A['wf_st']})*{A['instand_wohn']}", EUR); put(sE, "C7", f"=-({A['b1_m2']}+{A['b2_m2']})*{A['instand_gew']}", EUR); put(sE, "D7", f"=-{A['gastro_m2']}*{A['instand_gew']}", EUR)
put(sE, "A8", "Mietausfallwagnis"); put(sE, "B8", f"=-B5*{A['maw_wohn']}", EUR); put(sE, "C8", f"=-C5*{A['maw_buero']}", EUR); put(sE, "D8", f"=-D5*{A['maw_gew']}", EUR)
put(sE, "A9", "Bewirtschaftungskosten", font=bold)
for col in "BCD":
    put(sE, f"{col}9", f"=SUM({col}6:{col}8)", EUR, bold)
put(sE, "E9", "=SUM(B9:D9)", EUR, bold)
put(sE, "A10", "Reinertrag", font=bold)
for col in "BCD":
    put(sE, f"{col}10", f"={col}5+{col}9", EUR, bold)
put(sE, "E10", "=SUM(B10:D10)", EUR, bold)
put(sE, "A11", "Flächenanteil (für die Verteilung des Bodenwerts)")
put(sE, "B11", f"=({A['wf_og']}+{A['wf_st']})/(({A['wf_og']}+{A['wf_st']})+{A['b1_m2']}+{A['b2_m2']}+{A['gastro_m2']})", PCT)
put(sE, "C11", f"=({A['b1_m2']}+{A['b2_m2']})/(({A['wf_og']}+{A['wf_st']})+{A['b1_m2']}+{A['b2_m2']}+{A['gastro_m2']})", PCT)
put(sE, "D11", "=1-B11-C11", PCT); put(sE, "E11", "=SUM(B11:D11)", PCT)
put(sE, "A12", "Bodenwertanteil (Bodenwert 960 m² × 230 €)"); put(sE, "E12", f"={A['grund_m2']}*{A['preis_m2']}", EUR, bold)
for col in "BCD":
    put(sE, f"{col}12", f"=$E$12*{col}11", EUR)
put(sE, "A13", "Liegenschaftszins"); put(sE, "B13", f"={A['lzins_wohn']}", PCT2, link); put(sE, "C13", f"={A['lzins_buero']}", PCT2, link); put(sE, "D13", f"={A['lzins_gastro']}", PCT2, link)
put(sE, "A14", "Bodenwertverzinsung")
for col in "BCD":
    put(sE, f"{col}14", f"=-{col}12*{col}13", EUR)
put(sE, "A15", "Reinertragsanteil der Gebäude")
for col in "BCD":
    put(sE, f"{col}15", f"={col}10+{col}14", EUR)
put(sE, "E15", "=SUM(B15:D15)", EUR)
put(sE, "A16", "Restnutzungsdauer (Jahre)"); put(sE, "B16", f"={A['rnd']}", NUM, link); put(sE, "C16", f"={A['rnd_gew']}", NUM, link); put(sE, "D16", f"={A['rnd_gew']}", NUM, link)
put(sE, "A17", "Vervielfältiger")
for col in "BCD":
    put(sE, f"{col}17", f"=((1+{col}13)^{col}16-1)/({col}13*(1+{col}13)^{col}16)", "0.00")
put(sE, "E17", "=E18/E15", "0.00"); put(sE, "F17", "Summe: mittlerer Vervielfältiger", font=note)
put(sE, "A18", "Ertragswert der Gebäude", font=bold)
for col in "BCD":
    put(sE, f"{col}18", f"={col}15*{col}17", EUR, bold)
put(sE, "E18", "=SUM(B18:D18)", EUR, bold)
put(sE, "A19", "Ertragswert (Gebäude plus Bodenwert)", font=bold)
for col in "BCD":
    put(sE, f"{col}19", f"={col}18+{col}12", EUR, bold, fill=key_fill)
put(sE, "E19", "=SUM(B19:D19)", EUR, bold, fill=key_fill)
header(sE, 22, ["Beleihung", "Betrag", "", "", "", "Rechnung"])
Bl = [
    ("Sachwert (Bodenwert plus Herstellungskosten Gebäude)", "=E12+'Kosten und Finanzierung'!B12+'Kosten und Finanzierung'!B13+'Kosten und Finanzierung'!B14", EUR, "ohne Gastro-Einrichtung"),
    ("Ertragswert", "=E19", EUR, ""),
    ("Marktwert-Schätzung (niedrigerer Wert)", "=MIN(B23,B24)", EUR, "bei Ertragsimmobilien zählt der Ertragswert"),
    ("Beleihungswert nach Sicherheitsabschlag", f"=B25*(1-{A['abschlag']})", EUR, "Abschlag der Bank"),
    ("Gesamtkosten des Vorhabens", "='Kosten und Finanzierung'!B18", EUR, ""),
    ("Darlehensbedarf (100 % Fremdfinanzierung)", "='Kosten und Finanzierung'!B29", EUR, ""),
    ("Beleihungsauslauf (Darlehen / Beleihungswert)", "=B28/B26", PCT, "Banken verlangen meist unter 80–90 %"),
    ("Beleihungsauslauf KfW-Darlehen allein", "=('Kosten und Finanzierung'!B24+'Kosten und Finanzierung'!B25+'Kosten und Finanzierung'!B26)/B26", PCT, ""),
    ("Ertragswert minus Gesamtkosten", "=E19-B27", EURS, "Wertlücke, über Zusatzsicherheiten oder Eigenkapital zu decken"),
    ("Darlehen über 80 % Beleihungsauslauf", "=MAX(0,B28-0.8*B26)", EUR, "Rechnerischer Betrag über der 80-%-Grenze"),
    ("Kaufpreisfaktor (Ertragswert / Rohertrag)", "=E19/E5", "0.0", "Vervielfältiger auf die Jahresmiete"),
    ("Kosten-Faktor (Gesamtkosten / Rohertrag)", "=B27/E5", "0.0", ""),
]
for i, (lab, fml, fmt, rc) in enumerate(Bl):
    r = 23 + i
    b = i in (3, 6, 8)
    put(sE, f"A{r}", lab, font=bold if b else base)
    put(sE, f"B{r}", fml, fmt, bold if b else base, fill=key_fill if i in (3, 6) else None)
    put(sE, f"F{r}", rc, font=note)
put(sE, "A36", "Die Gastro wird hier nur mit der Pacht bewertet, die Büros mit den Ankermieter-Mieten. Der Gewinn des Betriebs (Bauherr) und Zusatzsicherheiten sind Verhandlungsgegenstand mit der Bank.", font=note, border=False)
for k_, c_ in (("rohertrag", "E5"), ("reinertrag", "E10"), ("bewirt", "E9"), ("bodenwert", "E12"), ("vervielf", "E17"), ("ertragswert", "E19"), ("ertragswert_geb", "E18"), ("sachwert", "B23"), ("beleihungswert", "B26"), ("auslauf", "B29"), ("wertluecke", "B31"), ("eigenkapital_80", "B32"), ("ew_wohn", "B19"), ("ew_buero", "C19"), ("ew_gastro", "D19")):
    reg(k_, sE, c_)

# =====================================================================================
# Prognose 10 Jahre
# =====================================================================================
sP = sheet("Prognose", "Prognose über 10 Jahre", "Mieten, Pacht, Büro-Indexmiete und Umsatz steigen, der Kapitaldienst bleibt konstant (Annuität). Restschuld nach Tilgungsplan.", [44] + [13] * 10)
header(sP, 4, ["Jahr"] + [str(y) for y in range(1, 11)])
pl = [
    ("Kaltmiete Wohnen", lambda c, y: f"='Flächen und Mieten'!$G$21*(1+{A['g_miete']})^({y}-1)"),
    ("Büromieten (Indexmiete)", lambda c, y: f"='Flächen und Mieten'!$G$25*(1+{A['g_index']})^({y}-1)"),
    ("Pacht Gastro", lambda c, y: f"='Flächen und Mieten'!$G$22*(1+{A['g_miete']})^({y}-1)"),
    ("Rücklagen", lambda c, y: f"=-{A['ruecklage']}*({c}5+{c}6+{c}7)"),
    ("Betriebsergebnis Gastro nach Pacht", lambda c, y: f"=('Gastro Betrieb'!$C$16*12*(1+{A['g_umsatz']})^({y}-1))-{c}7-{A['lohn']}*12"),
    ("Nettoertrag vor Kapitaldienst", lambda c, y: f"=SUM({c}5:{c}9)"),
    ("Kapitaldienst", lambda c, y: f"=-'Tilgung Jahre'!D{4 + y}"),
    ("Ergebnis nach Kapitaldienst", lambda c, y: f"={c}10+{c}11"),
    ("Kapitaldienstdeckung (DSCR)", lambda c, y: f"={c}10/-{c}11"),
    ("Restschuld Jahresende", lambda c, y: f"='Tilgung Jahre'!E{4 + y}"),
]
for i, (lab, f) in enumerate(pl):
    r = 5 + i
    b = i in (5, 7, 8)
    put(sP, f"A{r}", lab, font=bold if b else base)
    for y in range(1, 11):
        col = get_column_letter(1 + y)
        put(sP, f"{col}{r}", f(col, y), X if i == 8 else (EURS if i in (3, 6, 7) else EUR), bold if b else base)
reg("dscr_y5", sP, "F13"); reg("dscr_y10", sP, "K13"); reg("ergebnis_y10", sP, "K12")
put(sP, "A16", "Gastro-Gewinn vor Pacht mit der Umsatzsteigerung fortgeschrieben, Lohn des Bauherrn nicht gerechnet.", font=note, border=False)

# =====================================================================================
# Airbnb Prüfung
# =====================================================================================
sX = sheet("Airbnb Prüfung", "Prüfung: 2 Wohnungen als Airbnb-Apartments", "Lohnt sich Kurzzeitvermietung gegenüber langfristiger Vermietung? Zwei Apartments, Möblierung im Kredit (Hausbank-Zins + Tilgung).", [52, 16, 16, 16, 40])
put(sX, "A3", "Eingaben", font=bold, border=False)
inputs = [("Auslastung Airbnb", 0.50, PCT, "Annahme; Emsland laut Quelle ca. 37 % (2016/17)"), ("Möblierung je m² (€)", 600, EUR, "Möbel, Küche, Wäsche, Technik; Annahme"), ("Kostenquote vom Umsatz (Plattform, Reinigung, Nebenkosten, Material, Versicherung, Rücklage)", 0.56, PCT, "15 + 20 + 8 + 2 + 3 + 8 %"), ("Mindest-Mehrertrag je Monat für den Mehraufwand (€)", 300, EUR, "Annahme: Gäste, Schlüssel, Preise kosten Zeit")]
for i, (lab, v, fmt, nt) in enumerate(inputs):
    r = 4 + i
    put(sX, f"A{r}", lab); put(sX, f"B{r}", v, fmt, inp); put(sX, f"E{r}", nt, font=note)
header(sX, 9, ["Apartmentgröße (2 Apartments)", "45 m²", "55 m²", "67 m²", "Hinweis"])
sizes = [45, 55, 67]
guests = [2, 3, 4]
prices = [80, 90, 105]
put(sX, "A10", "Wohnfläche je Apartment (m²)")
put(sX, "A11", "Gäste")
put(sX, "A12", "Preis pro Nacht (€)")
put(sX, "A13", "Umsatz pro Apartment und Monat")
put(sX, "A14", "Netto Airbnb pro Apartment und Monat")
put(sX, "A15", "Netto langfristige Miete pro Apartment und Monat")
put(sX, "A16", "Möblierung (€)")
put(sX, "A17", "Kapitaldienst der Möblierung pro Monat")
put(sX, "A18", "Mehrertrag Airbnb je Apartment pro Monat", font=bold)
put(sX, "A19", "Mehrertrag für 2 Apartments pro Monat", font=bold)
put(sX, "A20", "Ergebnis", font=bold)
for j, col in enumerate("BCD"):
    put(sX, f"{col}10", sizes[j], NUM, inp); put(sX, f"{col}11", guests[j], NUM, inp); put(sX, f"{col}12", prices[j], EUR, inp)
    put(sX, f"{col}13", f"={col}12*365*$B$4/12", EUR)
    put(sX, f"{col}14", f"={col}13*(1-$B$6)", EUR)
    put(sX, f"{col}15", f"={col}10*{A['miete_m2']}*(1-{A['ruecklage']})", EUR)
    put(sX, f"{col}16", f"={col}10*$B$5", EUR)
    put(sX, f"{col}17", f"=-{col}16*({A['z_bank']}+{A['tilgung']})/12", EUR)
    put(sX, f"{col}18", f"={col}14-{col}15+{col}17", EURS, bold)
    put(sX, f"{col}19", f"=2*{col}18", EURS, bold, fill=key_fill)
    put(sX, f"{col}20", f'=IF({col}19>=$B$7,"lohnt sich","lohnt sich nicht")', None, bold)
put(sX, "E12", "Annahme: kleinere Apartments erzielen mehr Umsatz je m²", font=note)
put(sX, "E15", "nach Rücklagen von 10 %, Miete aus 11,18 €/m²", font=note)
put(sX, "A22", "Fazit", font=bold, border=False)
put(sX, "A23", '=IF(MAX(B19:D19)>=B7,"Mindestens eine Größe erreicht den Mindest-Mehrertrag: Airbnb prüfen.","Kein Apartment erreicht den Mindest-Mehrertrag von "&TEXT(B7,"#,##0")&" € pro Monat. Langfristige Vermietung ist besser, Airbnb bleibt aus dem Konzept.")', None, bold, border=False)
put(sX, "A24", "Die Möblierung erhöht den Kredit, Kurzzeitvermietung braucht dazu Aufwand, Reinigung, Gästekommunikation und bei mehr als 12 Betten Sonderbau-Brandschutz.", font=note, border=False)
reg("airbnb_45", sX, "B19"); reg("airbnb_60", sX, "C19"); reg("airbnb_83", sX, "D19"); reg("airbnb_fazit", sX, "A23")
reg("airbnb_netto_45", sX, "B14"); reg("langfrist_45", sX, "B15"); reg("airbnb_netto_83", sX, "D14"); reg("langfrist_83", sX, "D15")

# =====================================================================================
# Sensitivität
# =====================================================================================
sS = sheet("Sensitivität", "Belastungstest: Was passiert, wenn es schlechter läuft?", "Veränderung des Ergebnisses pro Monat und der Kapitaldienstdeckung gegenüber dem Plan.", [60, 18, 18, 20])
header(sS, 4, ["Szenario", "Ergebnis / Monat", "DSCR", "Änderung zum Plan"])
dbau = "0.1*'Kosten und Finanzierung'!B12*(1+" + A["bnk"] + ")*('Kosten und Finanzierung'!B31+" + A["tilgung"] + ")/12"
dz = "'Tilgung Jahre'!E14*0.01/12"
EC = "'Ertrag und Cashflow'!"
KD = "'Tilgungsplan'!N3"
sens = [
    ("Plan", f"={EC}B13", f"={EC}B11/{KD}"),
    ("Anschlusszins nach 10 Jahren +1 Prozentpunkt (auf Restschuld)", f"={EC}B13-{dz}", f"={EC}B11/({KD}+{dz})"),
    ("Mieten Wohnen −10 %", f"={EC}B13-0.1*{EC}B5*(1-{A['ruecklage']})", f"=({EC}B11-0.1*{EC}B5*(1-{A['ruecklage']}))/{KD}"),
    ("Gastro-Umsatz −20 %", f"={EC}B13-0.2*{A['umsatz']}*{A['marge']}", f"=({EC}B11-0.2*{A['umsatz']}*{A['marge']})/{KD}"),
    ("Gastro-Umsatz −40 %", f"={EC}B13-0.4*{A['umsatz']}*{A['marge']}", f"=({EC}B11-0.4*{A['umsatz']}*{A['marge']})/{KD}"),
    ("Baukosten +10 % (Kredit steigt entsprechend)", f"={EC}B13-{dbau}", f"={EC}B11/({KD}+{dbau})"),
    ("Größerer Büro-Ankermieter zieht aus (Leerstand)", f"={EC}B13-'Flächen und Mieten'!F23*(1-{A['ruecklage']})", f"=({EC}B11-'Flächen und Mieten'!F23*(1-{A['ruecklage']}))/{KD}"),
    ("Beide Büros leer", f"={EC}B13-{EC}B6*(1-{A['ruecklage']})", f"=({EC}B11-{EC}B6*(1-{A['ruecklage']}))/{KD}"),
    ("Gastro fällt ganz aus (keine Pacht, kein Betriebsergebnis)", f"={EC}B9-{EC}B7*(1-{A['ruecklage']})+{EC}B12", f"=({EC}B9-{EC}B7*(1-{A['ruecklage']}))/{KD}"),
]
for i, (lab, e, d) in enumerate(sens):
    r = 5 + i
    put(sS, f"A{r}", lab, font=bold if i == 0 else base)
    put(sS, f"B{r}", e, EURS)
    put(sS, f"C{r}", d, X)
    put(sS, f"D{r}", "" if i == 0 else f"=B{r}-$B$5", EURS)
put(sS, "A15", "Vereinfachte Rechnung, Hausbank prüft mit eigenen Annahmen.", font=note, border=False)
for k_, c_ in (("sens_zins", "B6"), ("sens_miete", "B7"), ("sens_umsatz20", "B8"), ("sens_umsatz40", "B9"), ("sens_bau", "B10"), ("sens_buero1", "B11"), ("sens_buero2", "B12"), ("sens_pacht", "B13")):
    reg(k_, sS, c_)

# =====================================================================================
# Bankunterlagen (Checkliste)
# =====================================================================================
sU = sheet("Bankunterlagen", "Unterlagen für die Bank (Checkliste)", "Was die Hausbank für Finanzierung und KfW-Antrag typischerweise braucht. Status bitte pflegen.", [6, 46, 62, 16])
header(sU, 4, ["Nr.", "Unterlage", "Inhalt / Hinweis", "Status"])
docs = [
    ("Projekt", "Businessplan (Word) und Präsentation", "Vorhaben, Konzept, Zahlen, Risiken. Liegt vor.", "vorhanden"),
    ("Projekt", "Rechenmodell mit Finanzierungs- und Tilgungsplan", "Diese Excel-Datei.", "vorhanden"),
    ("Projekt", "Gastro-Konzept mit Gestaltung", "Konzept, Grundriss, Speisekarte, Umsatzaufbau.", "vorhanden"),
    ("Projekt", "Lageplan, Flurkarte, Grundbuchauszug", "Baufeld 3, ca. 960 m². Grundbuchauszug nach Kaufvertrag.", "offen"),
    ("Projekt", "Bebauungsplan Nr. 123, 1. Änderung und Konzeptheft", "Festsetzungen, städtebaulicher Vertrag. Entwurf Stand 25.08.2026.", "teilweise"),
    ("Projekt", "Grundstückskaufvertrag oder Reservierung der Stadt", "Preis 230 €/m², Zuschnitt, Baureife.", "offen"),
    ("Bau", "Entwurfspläne, Flächen- und Wohnflächenberechnung", "Grundrisse, Schnitte, Ansichten vom Architekten.", "offen"),
    ("Bau", "Baubeschreibung", "Konstruktion, Energiestandard, Heizung.", "offen"),
    ("Bau", "Bauvoranfrage oder Baugenehmigung", "Zulässigkeit 540 m², Staffelgeschoss, Flachdach, Höhe, Stellplätze.", "offen"),
    ("Bau", "Kostenberechnung nach DIN 276 und Angebote", "Bauunternehmen und Zimmerei, Festpreis je m².", "offen"),
    ("Bau", "Bauzeitenplan", "Baubeginn Mitte 2027, 15 Monate Bauzeit.", "vorhanden"),
    ("KfW", "Bestätigung Energieeffizienz-Experte (Effizienzhaus 40)", "Antrag KfW 297/298 und 299 über die Hausbank vor Baubeginn.", "offen"),
    ("KfW", "QNG-Zertifizierung (Konzept und Zertifizierer)", "Für den vollen Kreditrahmen erforderlich.", "offen"),
    ("KfW", "Heizkonzept ohne Öl, Gas und Biomasse", "Wärmepumpe oder Fernwärme.", "offen"),
    ("Einnahmen", "Mietaufstellung und Mietkalkulation", "8 Wohnungen und 2 Büros, Flächen, Miete je m².", "vorhanden"),
    ("Einnahmen", "Pachtvertrag Gastro (Entwurf)", "Laufzeit, Pacht 10 €/m², Staffel, Sicherheiten.", "offen"),
    ("Einnahmen", "Vorverträge Ankermieter Büro (2 Mieter)", "Versicherungsgesellschaft (100 m²) und Makler (65 m²), 10 Jahre fest, Indexmiete, Bonitätsauskunft.", "offen"),
    ("Einnahmen", "Vorvermietungsabsichten", "Interessenten für Wohnungen und Gastro.", "offen"),
    ("Betrieb", "Gastro-Kalkulation mit Wareneinsatz, Personal, Umsatz", "Blatt 'Gastro Betrieb'.", "vorhanden"),
    ("Betrieb", "Nachweis Gastro-Erfahrung, Lebenslauf, Konzession", "Gaststättenerlaubnis, Hygiene, Qualifikation.", "offen"),
    ("Person", "Selbstauskunft und Vermögensübersicht", "Einkommen, Verbindlichkeiten, Vermögen.", "offen"),
    ("Person", "Einkommensnachweise, Steuerbescheide, BWA, Schufa", "letzte drei Jahre.", "offen"),
    ("Person", "Nachweis weiterer Sicherheiten", "Bürgschaften, Grundschulden auf weitere Immobilien, bestehende Objekte (letzte zwei Jahre gekauft).", "offen"),
    ("Sicherheit", "Wertermittlung / Beleihungswert", "Gutachten der Bank, Rechenbeispiel im Blatt 'Ertragswert'.", "offen"),
    ("Sicherheit", "Versicherungen", "Bauleistung, Bauherrenhaftpflicht, Gebäude.", "offen"),
]
for i, (kat, name, inh, st) in enumerate(docs):
    r = 5 + i
    put(sU, f"A{r}", i + 1, NUM); put(sU, f"B{r}", f"{kat}: {name}"); put(sU, f"C{r}", inh, font=note); put(sU, f"D{r}", st, font=inp)
    sU[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    sU[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")

# =====================================================================================
# Übersicht (erste Seite)
# =====================================================================================
sO = wb.create_sheet("Übersicht", 0)
sO.sheet_view.showGridLines = False
sO.column_dimensions["A"].width = 54
sO.column_dimensions["B"].width = 20
sO.column_dimensions["C"].width = 60
sO["A1"] = "Neue Mitte Werlte, Baufeld 3: Bankunterlagen"
sO["A1"].font = title_font
sO["A2"] = "Große Gastro im EG (ca. 510 m²), 2 Büro-Ankermieter und 3 Wohnungen im 1. OG, 5 Wohnungen im Staffelgeschoss in Holzbau. Bauherr: Bessam Hasso. Stand Oktober 2026."
sO["A2"].font = sub_font
header(sO, 4, ["Kennzahl", "Wert", "Erläuterung"])
over = [
    ("Projekt", None, None, None),
    ("Grundstück (m²)", f"={A['grund_m2']}", NUM, "Baufeld 3, Neue Mitte Werlte"),
    ("Grundfläche Gebäude (m²)", f"={A['bgf_eg']}", NUM, "32 × 18 m = GRZ-Maximum (0,6 × 960 m²)"),
    ("Bruttogrundfläche gesamt (m²)", "='Flächen und Mieten'!B8", NUM, "EG 576, 1. OG 576, Staffel 498"),
    ("Gastrofläche (m²)", f"={A['gastro_m2']}", NUM, "ca. 190 Plätze innen, ca. 60 Terrasse"),
    ("Büro-Ankermieter (m²)", "='Gewerbe und Anker'!B24", NUM, "100 m² Versicherung o. ä. und 65 m² Makler o. ä., 10 Jahre fest"),
    ("Wohneinheiten", "='Flächen und Mieten'!D9", NUM, "3 im 1. OG (ca. 107 m²), 5 im Staffelgeschoss (ca. 67 m²)"),
    ("Wohnfläche gesamt (m²)", "='Flächen und Mieten'!E9", NUM, ""),
    ("Kosten und Finanzierung", None, None, None),
    ("Gesamtkosten", "='Kosten und Finanzierung'!B18", EUR, "inkl. Finanzierungskosten der Bau- und Anlaufzeit"),
    ("Darlehen gesamt (100 % Fremdkapital)", "='Kosten und Finanzierung'!B29", EUR, "kein Eigenkapital"),
    ("davon KfW 297/298/299", "=SUM('Kosten und Finanzierung'!B24:B26)", EUR, "zinsverbilligt"),
    ("Anteil KfW", "='Kosten und Finanzierung'!B30", PCT, ""),
    ("Mischzins", "='Kosten und Finanzierung'!B31", PCT2, "KfW 2,5 % / 3,0 %, Hausbank 4,0 % (Annahmen)"),
    ("Kapitaldienst pro Monat (Anfangstilgung 1 %)", "='Tilgungsplan'!N3", EUR, "nach 12 Monaten tilgungsfreier Anlaufzeit"),
    ("Restschuld nach 10 Jahren Zinsbindung", "='Tilgung Jahre'!E14", EUR, ""),
    ("Ertrag und Wert", None, None, None),
    ("Mieten Wohnen + Büro + Pacht pro Monat", "='Flächen und Mieten'!F26", EUR, "Rohertrag"),
    ("Nettoertrag Immobilie pro Monat (nach Rücklagen)", "='Ertrag und Cashflow'!B9", EUR, ""),
    ("Betriebsergebnis Gastro nach Pacht pro Monat", "='Ertrag und Cashflow'!B10", EUR, "bei 65.000 € Umsatz, ohne Lohn des Bauherrn"),
    ("Ergebnis pro Monat nach Kapitaldienst", "='Ertrag und Cashflow'!B13", EURS, ""),
    ("Kapitaldienstdeckung gesamt (DSCR)", "='Ertrag und Cashflow'!B15", X, "Bank verlangt meist mindestens 1,2"),
    ("Kapitaldienstdeckung nur Immobilie", "='Ertrag und Cashflow'!B16", X, "ohne Gastro-Gewinn"),
    ("Kapitaldienstdeckung nur Wohnen und Büro", "='Ertrag und Cashflow'!B17", X, "langfristige Mieten ohne Gastro"),
    ("Ertragswert", "='Ertragswert'!E19", EUR, "Ertragswertverfahren nach Nutzung"),
    ("Beleihungswert nach Abschlag", "='Ertragswert'!B26", EUR, ""),
    ("Beleihungsauslauf", "='Ertragswert'!B29", PCT, "Darlehen / Beleihungswert"),
    ("Airbnb für 2 Apartments", "='Airbnb Prüfung'!A23", None, "Prüfung, siehe Blatt 'Airbnb Prüfung'"),
]
r = 5
for lab, f_, fmt, nt in over:
    if f_ is None:
        section(sO, r, lab, 3)
        r += 1
        continue
    put(sO, f"A{r}", lab)
    c = put(sO, f"B{r}", f_, fmt, link)
    if lab.startswith("Airbnb"):
        c.alignment = Alignment(wrap_text=True)
        sO.merge_cells(f"B{r}:C{r}")
        sO.row_dimensions[r].height = 44
    else:
        put(sO, f"C{r}", nt, font=note)
    r += 1
put(sO, f"A{r + 1}", "Alle Beträge sind Planungsannahmen. KfW-Zinsen und Rahmen sind Stand Ratgeber Oktober 2026 und müssen bei Hausbank und KfW bestätigt werden.", font=note, border=False)

order = ["Übersicht", "Annahmen", "Flächen und Mieten", "Gewerbe und Anker", "Kosten und Finanzierung", "Bauphase", "Tilgung Jahre", "Tilgungsplan", "Ertrag und Cashflow", "Gastro Betrieb", "Ertragswert", "Prognose", "Sensitivität", "Airbnb Prüfung", "Bankunterlagen"]
wb._sheets = [wb[n] for n in order]
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = GREEN if ws.title in ("Übersicht", "Annahmen") else GOLD
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
wb.save(OUT)
with open("bank_registry.json", "w", encoding="utf-8") as fh:
    json.dump(REG, fh, ensure_ascii=False, indent=1)
print("gespeichert", OUT, len(REG), "Kennzahlen registriert")
