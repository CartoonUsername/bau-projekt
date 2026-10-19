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
    ("bgf_eg", "BGF Erdgeschoss (m²)", 540, NUM, "Grundfläche 540 m², GRZ 0,6 erlaubt max. 576 m²"),
    ("bgf_og", "BGF 1. Obergeschoss (m²)", 540, NUM, "zweites Vollgeschoss"),
    ("bgf_st", "BGF Staffelgeschoss in Holzbau (m²)", 460, NUM, "0,8 m rundum zurückgesetzt"),
    ("baukosten_m2", "Baukosten je m² BGF (€)", 2200, EUR, "Bauherr (Bekanntenpreis), durch Angebote zu belegen"),
    ("holz_abschlag", "Holzbau günstiger als Massivbau (€/m²)", 400, EUR, "Annahme, Angebot der Zimmerei nötig"),
    ("terrasse_m2", "Umlaufende Dachterrasse (m²)", 72, NUM, "schmal, ca. 0,8 m, zählt nicht zur BGF"),
    ("terrasse_preis", "Dachterrasse Preis (€/m²)", 450, EUR, "Annahme"),
    ("bnk", "Baunebenkosten", 0.15, PCT, "Architekt, Statik, Gebühren; Annahme"),
    ("mehr_eh40", "Mehrkosten Effizienzhaus 40 und QNG", 0.03, PCT, "Annahme, auf Bau inkl. Baunebenkosten; Architekt muss bestätigen"),
    ("gastro_ausbau", "Gastro-Ausbau (€)", 150000, EUR, "Bauherr; für 460 m² knapp, Angebote nötig"),
    ("sec", "Flächen und Nutzung"),
    ("gastro_m2", "Gastrofläche im EG (m²)", 460, NUM, "EG abzüglich Treppenhaus, Aufzug, Wohn-Eingang"),
    ("ngf_anteil", "Nettogrundfläche Anteil der Gastrofläche", 0.85, PCT, "Annahme, für KfW 299"),
    ("wf_og", "Wohnfläche 1. OG (m²)", 415, NUM, "5 Wohnungen"),
    ("n_og", "Wohnungen im 1. OG", 5, NUM, "Bauherr"),
    ("wf_st", "Wohnfläche Staffelgeschoss (m²)", 310, NUM, "3 Penthouses"),
    ("n_st", "Wohnungen im Staffelgeschoss", 3, NUM, "Bauherr"),
    ("eigen", "davon vom Bauherrn selbst genutzt (Anzahl)", 0, NUM, "0 = alle vermietet. Selbstnutzung: KfW 297 statt 298, Miete entfällt"),
    ("sec", "Einnahmen und Gastro"),
    ("miete_m2", "Kaltmiete Wohnen (€/m² Wohnfläche)", "=950/85", EUR2, "Bauherr: 950 € für 85 m²; Portale Neubau Werlte ca. 10,7–11,0 €/m²"),
    ("pacht_m2", "Pacht Gastro (€/m²)", 12, EUR, "Annahme ohne Marktdaten"),
    ("ruecklage", "Rücklagen (Anteil an Miete und Pacht)", 0.10, PCT, "Hausverwaltung, Instandhaltung, Leerstand; Nebenkosten werden umgelegt"),
    ("umsatz", "Gastro-Umsatz pro Monat (€)", 50000, EUR, "Bauherr, netto; vorsichtig für 460 m²"),
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
    ("lzins", "Liegenschaftszins", 0.045, PCT2, "Annahme für gemischt genutztes Gebäude im ländlichen Raum"),
    ("rnd", "Restnutzungsdauer (Jahre)", 80, NUM, "Neubau, Annahme"),
    ("verw_we", "Verwaltungskosten Wohnen je Wohneinheit und Jahr (€)", 360, EUR, "Annahme in Anlehnung an ImmoWertV-Ansätze"),
    ("instand_wohn", "Instandhaltung Wohnen (€/m² Wohnfläche und Jahr)", 12, EUR, "Annahme Neubau"),
    ("maw_wohn", "Mietausfallwagnis Wohnen", 0.02, PCT, "Annahme"),
    ("verw_gew", "Verwaltungskosten Gewerbe (Anteil am Rohertrag)", 0.03, PCT, "Annahme"),
    ("instand_gew", "Instandhaltung Gewerbe (€/m² und Jahr)", 8, EUR, "Annahme"),
    ("maw_gew", "Mietausfallwagnis Gewerbe", 0.04, PCT, "Annahme, Gastro als Mieter riskanter"),
    ("abschlag", "Sicherheitsabschlag Beleihungswert", 0.10, PCT, "Annahme der Bank, üblich 10–20 %"),
    ("sec", "Prognose"),
    ("g_miete", "Mietsteigerung pro Jahr", 0.015, PCT, "Annahme"),
    ("g_umsatz", "Umsatzsteigerung Gastro pro Jahr", 0.015, PCT, "Annahme"),
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
sF = sheet("Flächen und Mieten", "Flächenprogramm und Mietaufstellung", "Gastro im ganzen EG, 8 Wohnungen auf 1. OG und Staffelgeschoss (540 m² Grundfläche).", [46, 14, 14, 16, 16, 18, 18])
header(sF, 4, ["Geschoss", "BGF (m²)", "Nutzung", "Einheiten", "Fläche (m²)", "", ""])
put(sF, "A5", "Erdgeschoss"); put(sF, "B5", f"={A['bgf_eg']}", NUM, link); put(sF, "C5", "Gastro"); put(sF, "D5", 1, NUM); put(sF, "E5", f"={A['gastro_m2']}", NUM, link)
put(sF, "A6", "1. Obergeschoss"); put(sF, "B6", f"={A['bgf_og']}", NUM, link); put(sF, "C6", "Wohnen"); put(sF, "D6", f"={A['n_og']}", NUM, link); put(sF, "E6", f"={A['wf_og']}", NUM, link)
put(sF, "A7", "Staffelgeschoss (Holzbau)"); put(sF, "B7", f"={A['bgf_st']}", NUM, link); put(sF, "C7", "Wohnen"); put(sF, "D7", f"={A['n_st']}", NUM, link); put(sF, "E7", f"={A['wf_st']}", NUM, link)
put(sF, "A8", "Summe", font=bold); put(sF, "B8", "=SUM(B5:B7)", NUM, bold); put(sF, "C8", ""); put(sF, "D8", "=D6+D7", NUM, bold); put(sF, "E8", "=E6+E7", NUM, bold)
reg("bgf", sF, "B8"); reg("n_we", sF, "D8"); reg("wf", sF, "E8")
header(sF, 11, ["Wohneinheit", "Geschoss", "Fläche (m²)", "Nutzung", "Kaltmiete / m²", "Kaltmiete / Monat", "Kaltmiete / Jahr"])
for i in range(8):
    r = 12 + i
    og = i < 5
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
put(sF, "A23", "Rohertrag gesamt (Wohnen vermietet + Pacht)", font=bold); put(sF, "F23", "=F21+F22", EUR, bold); put(sF, "G23", "=G21+G22", EUR, bold)
reg("miete_monat", sF, "F21"); reg("pacht_monat", sF, "F22"); reg("miete_voll_monat", sF, "F20")
put(sF, "A25", "Nebenkosten (Grundsteuer, Versicherung, Betriebskosten) werden auf die Mieter umgelegt und sind hier nicht gerechnet. Mietpreis ist Annahme des Bauherrn.", font=note, border=False)

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
    ("bau_massiv", "Bau, Massivbau (BGF × Baukosten)", f"=({A['bgf_eg']}+{A['bgf_og']}+{A['bgf_st']})*{A['baukosten_m2']}", "1.540 m² × 2.200 €"),
    ("holz", "Abschlag Holzbau Staffelgeschoss", f"=-{A['bgf_st']}*{A['holz_abschlag']}", "460 m² × 400 €"),
    ("terrasse", "Dachterrasse rundum", f"={A['terrasse_m2']}*{A['terrasse_preis']}", "72 m² × 450 €"),
    ("bau", "Bau gesamt", "=SUM(B9:B11)", ""),
    ("bnk", "Baunebenkosten", f"=B12*{A['bnk']}", "15 % vom Bau"),
    ("eh40", "Mehrkosten Effizienzhaus 40 und QNG-Nachweis", f"=(B12+B13)*{A['mehr_eh40']}", "3 % auf Bau inkl. Baunebenkosten"),
    ("ausbau", "Gastro-Ausbau (Küche, Bar, Möbel, Technik)", f"={A['gastro_ausbau']}", "Annahme Bauherr"),
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
put(sK, "A20", "Kosten je Wohneinheit inkl. Anteil Gastro", font=base); put(sK, "B20", "=B18/'Flächen und Mieten'!D8", EUR)

header(sK, 23, ["Mittelherkunft (Finanzierung)", "Betrag bei Rate-Start", "Anteil", "Zins / Programm"])
put(sK, "A24", "KfW 297 Klimafreundlicher Neubau (selbst genutzte Wohnungen)"); put(sK, "A25", "KfW 298 Klimafreundlicher Neubau (vermietete Wohnungen)"); put(sK, "A26", "KfW 299 Klimafreundlicher Neubau (Nichtwohngebäude, Gastro)"); put(sK, "A27", "Hausbank-Darlehen (Restfinanzierung inkl. Zinsen der Bauzeit)"); put(sK, "A28", "Eigenkapital"); put(sK, "A29", "Summe Finanzierung", font=bold)
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
put(sK, "A35", "KfW 299: Rahmen Gastro (Nettogrundfläche × 2.000 €)"); put(sK, "B35", f"={A['gastro_m2']}*{A['ngf_anteil']}*{A['kfw_m2']}", EUR)
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
for i, u in enumerate([30000, 40000, 50000, 60000, 70000]):
    r = 24 + i
    put(sG, f"A{r}", u, EUR, inp); put(sG, f"C{r}", f"=A{r}*$B$16", EUR); put(sG, f"D{r}", f"=C{r}-'Flächen und Mieten'!$F$22-{A['lohn']}", EURS)
put(sG, "A30", "Bei sehr niedrigem Umsatz drücken Fixkosten stärker: die Rechnung ist dort zu günstig.", font=note, border=False)

# =====================================================================================
# Ertrag und Cashflow
# =====================================================================================
sC = sheet("Ertrag und Cashflow", "Ertrag und Kapitaldienst (erstes Jahr nach der Anlaufzeit)", "Für die Bank: reicht der Ertrag für Zinsen und Tilgung? Kapitaldienstdeckung (DSCR) = Ertrag vor Kapitaldienst / Kapitaldienst.", [58, 18, 18, 44])
header(sC, 4, ["Position", "pro Monat", "pro Jahr", "Hinweis"])
lines = [
    ("Kaltmiete Wohnen (vermietete Wohnungen)", "='Flächen und Mieten'!F21", ""),
    ("Pacht Gastro", "='Flächen und Mieten'!F22", "Gastro zahlt an das Haus"),
    ("Rücklagen (Verwaltung, Instandhaltung, Leerstand)", f"=-{A['ruecklage']}*(B5+B6)", "10 % von Miete und Pacht"),
    ("Nettoertrag Immobilie", "=B5+B6+B7", ""),
    ("Betriebsergebnis Gastro nach Pacht", "='Gastro Betrieb'!C19", "Betreiber = Bauherr, ohne Lohn"),
    ("Nettoertrag vor Kapitaldienst", "=B8+B9", ""),
    ("Kapitaldienst (Zinsen und Tilgung aller Darlehen)", "=-'Tilgungsplan'!N3", ""),
    ("Ergebnis pro Monat nach Kapitaldienst", "=B10+B11", "ohne Lohn des Bauherrn"),
]
for i, (lab, fml, h) in enumerate(lines):
    r = 5 + i
    b = i in (3, 5, 7)
    put(sC, f"A{r}", lab, font=bold if b else base)
    put(sC, f"B{r}", fml, EURS if i in (2, 6, 7) else EUR, bold if b else base, fill=key_fill if i == 7 else None)
    put(sC, f"C{r}", f"=B{r}*12", EURS if i in (2, 6, 7) else EUR, bold if b else base)
    put(sC, f"D{r}", h, font=note)
put(sC, "A14", "Kapitaldienstdeckung gesamt (DSCR)", font=bold); put(sC, "B14", "=B10/-B11", X, bold, fill=key_fill); put(sC, "D14", "Bank verlangt meist mindestens 1,2", font=note)
put(sC, "A15", "Kapitaldienstdeckung nur Immobilie (Miete und Pacht)", font=bold); put(sC, "B15", "=B8/-B11", X, bold); put(sC, "D15", "ohne Gastro-Gewinn, Pacht gesichert durch Pachtvertrag", font=note)
put(sC, "A16", "Zinsdeckung (Ertrag vor Kapitaldienst / Zinsen)"); put(sC, "B16", "=B10/('Tilgung Jahre'!B5/12)", X)
put(sC, "A17", "Anfangsrendite auf Gesamtkosten (Nettoertrag Immobilie p. a.)"); put(sC, "B17", "=C8/'Kosten und Finanzierung'!B18", PCT2)
put(sC, "A18", "Break-even Gastro-Umsatz (Haus insgesamt Ergebnis = 0)"); put(sC, "B18", f"=({A['lohn']}-B8-B11-(B9-'Gastro Betrieb'!C19))/{A['marge']}+0*B5", EUR)
sC["B18"].value = f"=(-B8-B11+'Flächen und Mieten'!F22+{A['lohn']})/{A['marge']}"
put(sC, "D18", "Umsatz, ab dem Zinsen und Tilgung aller Darlehen bezahlt sind", font=note)
reg("c_miete", sC, "B5"); reg("c_pacht", sC, "B6"); reg("c_rueck", sC, "B7"); reg("c_netto_immo", sC, "B8"); reg("c_gastro", sC, "B9"); reg("c_netto", sC, "B10"); reg("c_kd", sC, "B11"); reg("c_ergebnis", sC, "B12")
reg("dscr", sC, "B14"); reg("dscr_immo", sC, "B15"); reg("zinsdeckung", sC, "B16"); reg("anfangsrendite", sC, "B17"); reg("breakeven_haus", sC, "B18")

# =====================================================================================
# Ertragswert
# =====================================================================================
sE = sheet("Ertragswert", "Ertragswert und Beleihung", "Ertragswertverfahren nach ImmoWertV (vereinfacht) mit Annahmen. Ein Gutachter der Bank ermittelt den verbindlichen Beleihungswert.", [58, 18, 44])
header(sE, 4, ["Ertragswertberechnung", "Betrag", "Rechnung"])
E = [
    ("Rohertrag Wohnen pro Jahr (alle Wohnungen, marktüblich)", "='Flächen und Mieten'!G20", EUR, ""),
    ("Rohertrag Gewerbe (Pacht Gastro) pro Jahr", "='Flächen und Mieten'!G22", EUR, ""),
    ("Rohertrag gesamt", "=B5+B6", EUR, ""),
    ("Verwaltungskosten Wohnen", f"=-({A['n_og']}+{A['n_st']})*{A['verw_we']}", EUR, "Wohneinheiten × Satz"),
    ("Instandhaltung Wohnen", f"=-({A['wf_og']}+{A['wf_st']})*{A['instand_wohn']}", EUR, "Wohnfläche × Satz"),
    ("Mietausfallwagnis Wohnen", f"=-B5*{A['maw_wohn']}", EUR, ""),
    ("Verwaltungskosten Gewerbe", f"=-B6*{A['verw_gew']}", EUR, ""),
    ("Instandhaltung Gewerbe", f"=-{A['gastro_m2']}*{A['instand_gew']}", EUR, ""),
    ("Mietausfallwagnis Gewerbe", f"=-B6*{A['maw_gew']}", EUR, ""),
    ("Bewirtschaftungskosten gesamt", "=SUM(B8:B13)", EUR, ""),
    ("Reinertrag des Grundstücks", "=B7+B14", EUR, ""),
    ("Bodenwert (Grundstück ohne Nebenkosten)", f"={A['grund_m2']}*{A['preis_m2']}", EUR, "960 m² × 230 €"),
    ("Bodenwertverzinsung", f"=-B16*{A['lzins']}", EUR, "Bodenwert × Liegenschaftszins"),
    ("Reinertragsanteil der Gebäude", "=B15+B17", EUR, ""),
    ("Vervielfältiger", f"=((1+{A['lzins']})^{A['rnd']}-1)/({A['lzins']}*(1+{A['lzins']})^{A['rnd']})", "0.00", "Liegenschaftszins und Restnutzungsdauer"),
    ("Ertragswert der Gebäude", "=B18*B19", EUR, ""),
    ("Ertragswert (Gebäude plus Bodenwert)", "=B20+B16", EUR, ""),
]
for i, (lab, fml, fmt, rc) in enumerate(E):
    r = 5 + i
    b = i in (2, 9, 10, 16)
    put(sE, f"A{r}", lab, font=bold if b else base)
    put(sE, f"B{r}", fml, fmt, bold if b else base, fill=key_fill if i == 16 else None)
    put(sE, f"C{r}", rc, font=note)
header(sE, 24, ["Beleihung", "Betrag", "Rechnung"])
Bl = [
    ("Sachwert (Bodenwert plus Herstellungskosten Gebäude)", "=B16+'Kosten und Finanzierung'!B12+'Kosten und Finanzierung'!B13+'Kosten und Finanzierung'!B14", EUR, "ohne Gastro-Einrichtung"),
    ("Ertragswert", "=B21", EUR, ""),
    ("Marktwert-Schätzung (niedrigerer Wert)", "=MIN(B25,B26)", EUR, "bei Ertragsimmobilien zählt der Ertragswert"),
    ("Beleihungswert nach Sicherheitsabschlag", f"=B27*(1-{A['abschlag']})", EUR, "Abschlag der Bank"),
    ("Gesamtkosten des Vorhabens", "='Kosten und Finanzierung'!B18", EUR, ""),
    ("Darlehensbedarf (100 % Fremdfinanzierung)", "='Kosten und Finanzierung'!B29", EUR, ""),
    ("Beleihungsauslauf (Darlehen / Beleihungswert)", "=B30/B28", PCT, "Banken verlangen meist unter 80–90 %"),
    ("Beleihungsauslauf KfW-Darlehen allein", "=('Kosten und Finanzierung'!B24+'Kosten und Finanzierung'!B25+'Kosten und Finanzierung'!B26)/B28", PCT, ""),
    ("Ertragswert minus Gesamtkosten", "=B21-B29", EURS, "Wertlücke, die über Zusatzsicherheiten oder Eigenkapital zu decken ist"),
    ("Fehlendes Eigenkapital/Sicherheit für Auslauf 80 %", "=MAX(0,B30-0.8*B28)", EUR, "Rechnerischer Betrag über der 80-%-Grenze"),
    ("Kaufpreisfaktor (Ertragswert / Rohertrag)", "=B21/B7", "0.0", "Vervielfältiger auf die Jahresmiete"),
    ("Kosten-Faktor (Gesamtkosten / Rohertrag)", "=B29/B7", "0.0", ""),
]
for i, (lab, fml, fmt, rc) in enumerate(Bl):
    r = 25 + i
    b = i in (3, 6, 8)
    put(sE, f"A{r}", lab, font=bold if b else base)
    put(sE, f"B{r}", fml, fmt, bold if b else base, fill=key_fill if i in (3, 6) else None)
    put(sE, f"C{r}", rc, font=note)
put(sE, "A38", "Die Gastro wird hier nur mit der Pacht bewertet. Der Gewinn des Betriebs (Bauherr) und die Hilfe durch Bürgschaft, Eigenkapital oder weitere Grundstücke sind Verhandlungsgegenstand mit der Bank.", font=note, border=False)
reg("rohertrag", sE, "B7"); reg("reinertrag", sE, "B15"); reg("bewirt", sE, "B14"); reg("bodenwert", sE, "B16"); reg("vervielf", sE, "B19"); reg("ertragswert", sE, "B21"); reg("sachwert", sE, "B25"); reg("beleihungswert", sE, "B28"); reg("auslauf", sE, "B31"); reg("wertluecke", sE, "B33"); reg("eigenkapital_80", sE, "B34"); reg("ertragswert_geb", sE, "B20")

# =====================================================================================
# Prognose 10 Jahre
# =====================================================================================
sP = sheet("Prognose", "Prognose über 10 Jahre", "Miete, Pacht und Umsatz steigen, der Kapitaldienst bleibt konstant (Annuität). Restschuld nach Tilgungsplan.", [44] + [13] * 10)
header(sP, 4, ["Jahr"] + [str(y) for y in range(1, 11)])
pl = [
    ("Kaltmiete Wohnen", lambda c, y: f"='Flächen und Mieten'!$G$21*(1+{A['g_miete']})^({y}-1)"),
    ("Pacht Gastro", lambda c, y: f"='Flächen und Mieten'!$G$22*(1+{A['g_miete']})^({y}-1)"),
    ("Rücklagen", lambda c, y: f"=-{A['ruecklage']}*({c}5+{c}6)"),
    ("Betriebsergebnis Gastro nach Pacht", lambda c, y: f"=('Gastro Betrieb'!$C$16*12*(1+{A['g_umsatz']})^({y}-1))-{c}6-{A['lohn']}*12"),
    ("Nettoertrag vor Kapitaldienst", lambda c, y: f"=SUM({c}5:{c}8)"),
    ("Kapitaldienst", lambda c, y: f"=-'Tilgung Jahre'!D{4 + y}"),
    ("Ergebnis nach Kapitaldienst", lambda c, y: f"={c}9+{c}10"),
    ("Kapitaldienstdeckung (DSCR)", lambda c, y: f"={c}9/-{c}10"),
    ("Restschuld Jahresende", lambda c, y: f"='Tilgung Jahre'!E{4 + y}"),
]
for i, (lab, f) in enumerate(pl):
    r = 5 + i
    put(sP, f"A{r}", lab, font=bold if i in (4, 6, 7) else base)
    for y in range(1, 11):
        col = get_column_letter(1 + y)
        put(sP, f"{col}{r}", f(col, y), X if i == 7 else (EURS if i in (2, 5, 6) else EUR), bold if i in (4, 6, 7) else base)
reg("dscr_y5", sP, "F12"); reg("dscr_y10", sP, "K12"); reg("ergebnis_y10", sP, "K11")
put(sP, "A15", "Gastro-Gewinn vor Pacht mit der Umsatzsteigerung fortgeschrieben, Lohn des Bauherrn nicht gerechnet.", font=note, border=False)

# =====================================================================================
# Airbnb Prüfung
# =====================================================================================
sX = sheet("Airbnb Prüfung", "Prüfung: 2 Wohnungen als Airbnb-Apartments", "Lohnt sich Kurzzeitvermietung gegenüber langfristiger Vermietung? Zwei Apartments, Möblierung im Kredit (Hausbank-Zins + Tilgung).", [52, 16, 16, 16, 40])
put(sX, "A3", "Eingaben", font=bold, border=False)
inputs = [("Auslastung Airbnb", 0.50, PCT, "Annahme; Emsland laut Quelle ca. 37 % (2016/17)"), ("Möblierung je m² (€)", 600, EUR, "Möbel, Küche, Wäsche, Technik; Annahme"), ("Kostenquote vom Umsatz (Plattform, Reinigung, Nebenkosten, Material, Versicherung, Rücklage)", 0.56, PCT, "15 + 20 + 8 + 2 + 3 + 8 %"), ("Mindest-Mehrertrag je Monat für den Mehraufwand (€)", 300, EUR, "Annahme: Gäste, Schlüssel, Preise kosten Zeit")]
for i, (lab, v, fmt, nt) in enumerate(inputs):
    r = 4 + i
    put(sX, f"A{r}", lab); put(sX, f"B{r}", v, fmt, inp); put(sX, f"E{r}", nt, font=note)
header(sX, 9, ["Apartmentgröße (2 Apartments)", "45 m²", "60 m²", "83 m²", "Hinweis"])
sizes = [45, 60, 83]
guests = [2, 3, 4]
prices = [80, 95, 115]
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
sS = sheet("Sensitivität", "Belastungstest: Was passiert, wenn es schlechter läuft?", "Veränderung des Ergebnisses pro Monat und der Kapitaldienstdeckung gegenüber dem Plan.", [56, 18, 18, 20])
header(sS, 4, ["Szenario", "Ergebnis / Monat", "DSCR", "Änderung zum Plan"])
dbau = "0.1*'Kosten und Finanzierung'!B12*(1+" + A["bnk"] + ")*('Kosten und Finanzierung'!B31+" + A["tilgung"] + ")/12"
dz = "'Tilgung Jahre'!E14*0.01/12"
EC = "'Ertrag und Cashflow'!"
sens = [
    ("Plan", f"={EC}B12", f"={EC}B10/'Tilgungsplan'!N3"),
    ("Anschlusszins nach 10 Jahren +1 Prozentpunkt (auf Restschuld)", f"={EC}B12-{dz}", f"={EC}B10/('Tilgungsplan'!N3+{dz})"),
    ("Mieten Wohnen −10 %", f"={EC}B12-0.1*{EC}B5*(1-{A['ruecklage']})", f"=({EC}B10-0.1*{EC}B5*(1-{A['ruecklage']}))/'Tilgungsplan'!N3"),
    ("Gastro-Umsatz −20 %", f"={EC}B12-0.2*{A['umsatz']}*{A['marge']}", f"=({EC}B10-0.2*{A['umsatz']}*{A['marge']})/'Tilgungsplan'!N3"),
    ("Gastro-Umsatz −40 %", f"={EC}B12-0.4*{A['umsatz']}*{A['marge']}", f"=({EC}B10-0.4*{A['umsatz']}*{A['marge']})/'Tilgungsplan'!N3"),
    ("Baukosten +10 % (Kredit steigt entsprechend)", f"={EC}B12-{dbau}", f"={EC}B10/('Tilgungsplan'!N3+{dbau})"),
    ("Gastro fällt ganz aus (keine Pacht, kein Betriebsergebnis)", f"={EC}B8-{EC}B6*(1-{A['ruecklage']})+{EC}B11", f"=({EC}B10-{EC}B9-{EC}B6*(1-{A['ruecklage']}))/'Tilgungsplan'!N3"),
]
for i, (lab, e, d) in enumerate(sens):
    r = 5 + i
    put(sS, f"A{r}", lab, font=bold if i == 0 else base)
    put(sS, f"B{r}", e, EURS)
    put(sS, f"C{r}", d, X)
    put(sS, f"D{r}", "" if i == 0 else f"=B{r}-$B$5", EURS)
put(sS, "A13", "Vereinfachte Rechnung, Hausbank prüft mit eigenen Annahmen.", font=note, border=False)
reg("sens_zins", sS, "B6"); reg("sens_miete", sS, "B7"); reg("sens_umsatz20", sS, "B8"); reg("sens_umsatz40", sS, "B9"); reg("sens_bau", sS, "B10"); reg("sens_pacht", sS, "B11")
reg("sens_zins_dscr", sS, "C6"); reg("sens_miete_dscr", sS, "C7"); reg("sens_umsatz20_dscr", sS, "C8"); reg("sens_umsatz40_dscr", sS, "C9")

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
    ("Einnahmen", "Mietaufstellung und Mietkalkulation", "8 Wohnungen, Flächen, Miete je m².", "vorhanden"),
    ("Einnahmen", "Pachtvertrag Gastro (Entwurf)", "Laufzeit, Pacht 12 €/m², Staffel, Sicherheiten.", "offen"),
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
sO["A2"] = "Gastro im ganzen EG (ca. 460 m²) und 8 Wohnungen auf 1. OG und Staffelgeschoss in Holzbau. Bauherr: Bessam Hasso. Stand Oktober 2026."
sO["A2"].font = sub_font
header(sO, 4, ["Kennzahl", "Wert", "Erläuterung"])
over = [
    ("Projekt", None, None, None),
    ("Grundstück (m²)", f"={A['grund_m2']}", NUM, "Baufeld 3, Neue Mitte Werlte"),
    ("Grundfläche Gebäude (m²)", f"={A['bgf_eg']}", NUM, "GRZ 0,6 erlaubt max. 576 m²"),
    ("Bruttogrundfläche gesamt (m²)", "='Flächen und Mieten'!B8", NUM, "EG 540, 1. OG 540, Staffel 460"),
    ("Wohneinheiten", "='Flächen und Mieten'!D8", NUM, "5 im 1. OG, 3 im Staffelgeschoss (Holzbau)"),
    ("Wohnfläche gesamt (m²)", "='Flächen und Mieten'!E8", NUM, ""),
    ("Gastrofläche (m²)", f"={A['gastro_m2']}", NUM, "ca. 150 Plätze innen, ca. 40 Terrasse"),
    ("Kosten und Finanzierung", None, None, None),
    ("Gesamtkosten", "='Kosten und Finanzierung'!B18", EUR, "inkl. Finanzierungskosten der Bau- und Anlaufzeit"),
    ("Darlehen gesamt (100 % Fremdkapital)", "='Kosten und Finanzierung'!B29", EUR, "kein Eigenkapital"),
    ("davon KfW 297/298/299", "=SUM('Kosten und Finanzierung'!B24:B26)", EUR, "zinsverbilligt"),
    ("Anteil KfW", "='Kosten und Finanzierung'!B30", PCT, ""),
    ("Mischzins", "='Kosten und Finanzierung'!B31", PCT2, "KfW 2,5 % / 3,0 %, Hausbank 4,0 % (Annahmen)"),
    ("Kapitaldienst pro Monat (Anfangstilgung 1 %)", "='Tilgungsplan'!N3", EUR, "nach 12 Monaten tilgungsfreier Anlaufzeit"),
    ("Restschuld nach 10 Jahren Zinsbindung", "='Tilgung Jahre'!E14", EUR, ""),
    ("Ertrag und Wert", None, None, None),
    ("Nettoertrag Immobilie pro Monat (Miete + Pacht − Rücklagen)", "='Ertrag und Cashflow'!B8", EUR, ""),
    ("Betriebsergebnis Gastro nach Pacht pro Monat", "='Ertrag und Cashflow'!B9", EUR, "bei 50.000 € Umsatz, ohne Lohn des Bauherrn"),
    ("Ergebnis pro Monat nach Kapitaldienst", "='Ertrag und Cashflow'!B12", EURS, ""),
    ("Kapitaldienstdeckung gesamt (DSCR)", "='Ertrag und Cashflow'!B14", X, "Bank verlangt meist mindestens 1,2"),
    ("Kapitaldienstdeckung nur Immobilie", "='Ertrag und Cashflow'!B15", X, "ohne Gastro-Gewinn"),
    ("Ertragswert", "='Ertragswert'!B21", EUR, "vereinfachtes Ertragswertverfahren"),
    ("Beleihungswert nach Abschlag", "='Ertragswert'!B28", EUR, ""),
    ("Beleihungsauslauf", "='Ertragswert'!B31", PCT, "Darlehen / Beleihungswert"),
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

order = ["Übersicht", "Annahmen", "Flächen und Mieten", "Kosten und Finanzierung", "Bauphase", "Tilgung Jahre", "Tilgungsplan", "Ertrag und Cashflow", "Gastro Betrieb", "Ertragswert", "Prognose", "Sensitivität", "Airbnb Prüfung", "Bankunterlagen"]
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
