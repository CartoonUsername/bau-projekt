import json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

B = json.load(open("bank_values.json"))
GREEN = RGBColor(0x2E, 0x4A, 0x3E); RED = RGBColor(0x8B, 0x3A, 0x2F); GREY = RGBColor(0x5A, 0x5F, 0x66)
def n(x, d=0): return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def eur(x): return n(x) + " €"

kosten = B["k_gesamt"]; land = B["k_land_ges"]; fin = B["k_fin"]
roh = B["rohertrag"]; rueck = -B["c_rueck"] * 12
gastro = B["c_gastro"] * 12
zins = B["zins_jahr1"]; tilg = B["tilg_jahr1"]; rate = B["rate_jahr1"]
afa = 0.03 * (kosten - land - fin)
vor_kd = roh - rueck + gastro
cash = vor_kd - rate
gewinn = vor_kd - zins - afa
immo_cash = roh - rueck - rate

doc = Document()
sec = doc.sections[0]; sec.page_width = Cm(21); sec.page_height = Cm(29.7)
for a in ("left_margin", "right_margin"): setattr(sec, a, Cm(2))
sec.top_margin = Cm(1.8); sec.bottom_margin = Cm(1.6)
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

def para(t, bold=False, size=None, color=None, after=4, italic=False, font=None):
    p = doc.add_paragraph(); r = p.add_run(t); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    if font: r.font.name = font
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(0)
    return p
def head(t): 
    p = para(t, size=14, color=RED, after=3, font="Georgia"); p.paragraph_format.space_before = Pt(8); p.paragraph_format.keep_with_next = True
def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hexc); tcPr.append(s)
def table(rows, widths, right=(), boldrows=()):
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"; t.autofit = False
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.width = Cm(widths[j]); c.text = ""
            p = c.paragraphs[0]; r = p.add_run(str(v)); r.font.size = Pt(9.5)
            p.paragraph_format.space_after = Pt(1)
            if j in right: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if i == 0: r.bold = True; r.font.color.rgb = RGBColor(255, 255, 255); shade(c, "2E4A3E")
            elif i in boldrows: r.bold = True; shade(c, "E4EDE6")
    for j, w in enumerate(widths): t.columns[j].width = Cm(w)
    tblPr = t._tbl.tblPr; lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

para("NEUE MITTE WERLTE · BAUFELD 3", bold=True, size=9, color=RGBColor(0xB8, 0x8A, 0x2E), after=0)
para("Kosten, Nutzen und Gewinn pro Kopf", size=22, color=GREEN, after=2, font="Georgia")
para("Kurze Erklärung für die Gesellschafter einer GbR. Basis: Excel-Rechenmodell (8 Wohnungen, 2 Büros, Gastro 510 m²), Jahr 1 nach der Anlaufzeit. Alle Zahlen sind Planungsannahmen, Stand Oktober 2026.", italic=True, color=GREY, size=9.5, after=6)

head("1 Was kostet das Projekt?")
para(f"Die Gesamtkosten liegen bei {eur(kosten)} (Grundstück {eur(land)}, Bau, Nebenkosten, Gastro- und Büro-Ausbau, Finanzierungskosten in der Bauzeit). Sie werden zu 100 % über KfW-Kredite und Hausbank finanziert, die Gesellschafter zahlen kein Eigenkapital ein. Die Rate für Zins und 1 % Tilgung beträgt {eur(rate / 12)} im Monat ({eur(rate)} im Jahr).")

head("2 Was kommt rein? (pro Jahr)")
table([
    ["Position", "pro Jahr"],
    ["Mieten Wohnen (8 Wohnungen, 655 m²) + Büros (2 Ankermieter) + Gastro-Pacht", eur(roh)],
    ["abzüglich Rücklagen (10 %: Verwaltung, Instandhaltung, Leerstand)", "−" + eur(rueck)],
    ["Gastro-Betriebsergebnis nach Pacht (Umsatz 65.010 € im Monat, ohne Lohn)", eur(gastro)],
    ["Ertrag vor Kapitaldienst", eur(vor_kd)],
    ["Zins und Tilgung an die Banken", "−" + eur(rate)],
    ["Cash für die Gesellschafter", eur(cash)],
], [13.2, 3.8], right=(1,), boldrows=(4, 6))
para(f"Nutzen-Faktor: Der Ertrag vor Kapitaldienst entspricht {n(vor_kd / kosten * 100, 1)} % der Gesamtkosten (Anfangsrendite), die Kosten sind also das {n(kosten / vor_kd, 1)}-Fache des Jahresertrags. Nur aus Mieten und Pacht wären es {n((roh - rueck) / kosten * 100, 1)} %, das reicht nicht für die Raten.", after=4)

head("3 Was bekommt jeder? (gleiche Anteile)")
rows = [["Personen", "Cash pro Person / Monat", "Cash pro Person / Jahr", "Gewinn zu versteuern / Jahr", "Nach Steuer / Monat", "Tilgung pro Person / Jahr"]]
for k in (1, 2, 4, 8):
    steuer = 0.35 * gewinn / k
    rows.append([str(k), eur(cash / 12 / k), eur(cash / k), eur(gewinn / k), eur((cash / k - steuer) / 12), eur(tilg / k)])
table(rows, [2.0, 3.2, 3.2, 3.2, 3.0, 2.4], right=(1, 2, 3, 4, 5))
para(f"Steuerlich ist der Gewinn nur {eur(gewinn)} im Jahr: Zinsen ({eur(zins)}) und Gebäudeabschreibung 3 % ({eur(afa)}) mindern ihn, die Tilgung ({eur(tilg)}) nicht. Die Tilgung ist aber Vermögensaufbau, denn sie senkt die Schulden. Der Steuersatz von 35 % ist eine Annahme und hängt vom persönlichen Einkommen ab.", after=4)

head("4 Wo liegt das Risiko?")
for t in [
    f"Ohne Gastro-Gewinn fehlen {eur(-immo_cash)} im Jahr (Kapitaldienstdeckung nur {n(B['dscr_immo'], 2)}), der Gewinn hängt also an einer gut laufenden Gastro.",
    f"Der Beleihungsauslauf liegt bei {n(B['auslauf'] * 100, 0)} %: Die Bank verlangt zusätzliche Sicherheiten (Grundschulden, Bürgschaften oder Eigenkapital), die Lücke zur 80-%-Grenze beträgt etwa 2,77 Mio € insgesamt.",
    "Eine GbR haftet mit dem persönlichen Vermögen aller Gesellschafter. Betreibt die GbR auch die Gastro, ist sie komplett gewerblich (Gewerbesteuer), besser ist eine getrennte Betreiberfirma, die Pacht zahlt.",
    "Der Lohn des Bauherrn, mögliche Sonderabschreibungen und Gewerbesteuer sind nicht gerechnet. Steuerberater und Bank müssen das prüfen.",
]:
    p = doc.add_paragraph(style="List Bullet"); r = p.add_run(t); r.font.size = Pt(10); p.paragraph_format.space_after = Pt(2)

para("Quelle: Bankunterlagen_Baufeld3.xlsx (Blätter Ertrag und Cashflow, Tilgungsplan, Gastro Tagesteile).", italic=True, color=GREY, size=8.5, after=0)
doc.save("Kosten-Nutzen_pro-Kopf_Baufeld3.docx")
print(cash, gewinn, vor_kd/kosten)
