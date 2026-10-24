"""Businessplan für die Bank als Word-Datei (Zahlen aus bank_values.json, erzeugt aus Bankunterlagen_Baufeld3.xlsx)."""
import json
import os
import sys

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUT = sys.argv[1] if len(sys.argv) > 1 else "Businessplan_Baufeld3_Neue-Mitte-Werlte.docx"
here = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(here, "bank_values.json"), encoding="utf-8"))

GREEN = RGBColor(0x2F, 0x4A, 0x3E)
RED = RGBColor(0x8C, 0x3B, 0x32)
GREY = RGBColor(0x5B, 0x67, 0x70)


def fmt(n, d=0):
    return f"{n:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def eur(n):
    return ("−" if n < 0 else "") + fmt(abs(n)) + " €"


def eurs(n):
    return ("+" if n > 0 else "−" if n < 0 else "") + fmt(abs(n)) + " €"


def pct(n, d=1):
    return fmt(n * 100, d) + " %"


def mio(n):
    return fmt(n / 1e6, 2) + " Mio. €"


doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.0)

st = doc.styles["Normal"]
st.font.name = "Arial"
st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.paragraph_format.space_after = Pt(6)
st.paragraph_format.line_spacing = 1.15
for name, size, color in (("Heading 1", 18, RED), ("Heading 2", 13, GREEN), ("Title", 30, GREEN)):
    h = doc.styles[name]
    h.font.name = "Georgia"
    h.font.size = Pt(size)
    h.font.bold = False
    h.font.color.rgb = color
    h.element.rPr.rFonts.set(qn("w:ascii"), "Georgia")
    h.element.rPr.rFonts.set(qn("w:hAnsi"), "Georgia")
    h.element.rPr.rFonts.set(qn("w:eastAsia"), "Georgia")
doc.styles["Heading 1"].paragraph_format.space_before = Pt(18)
doc.styles["Heading 1"].paragraph_format.space_after = Pt(8)
doc.styles["Heading 2"].paragraph_format.space_before = Pt(12)
doc.styles["Heading 2"].paragraph_format.space_after = Pt(4)


def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "D0D0D0")
        b.append(e)
    tblPr.append(b)


def para(text="", bold=False, italic=False, color=None, size=None, align=None, after=None, style=None):
    p = doc.add_paragraph(style=style)
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if color is not None:
            r.font.color.rgb = color
        if size:
            r.font.size = Pt(size)
    if align:
        p.alignment = align
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    return p


def bullets(items):
    for t in items:
        p = doc.add_paragraph(style="List Bullet")
        if isinstance(t, tuple):
            r = p.add_run(t[0])
            r.bold = True
            p.add_run(t[1])
        else:
            p.add_run(t)
        p.paragraph_format.space_after = Pt(3)


def table(rows, widths, header=True, right_cols=(), bold_rows=(), font=9.5, shade_rows=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    borders(t)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.width = Cm(widths[j])
            c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            r = p.add_run(str(val))
            r.font.size = Pt(font)
            if j in right_cols and not (header and i == 0 and False):
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if header and i == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                shade(c, "2F4A3E")
            elif i in bold_rows:
                r.bold = True
                shade(c, "E3E8E5")
            if shade_rows and i in shade_rows:
                shade(c, shade_rows[i])
    for j, w in enumerate(widths):
        t.columns[j].width = Cm(w)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(lay)
    for i, row in enumerate(t.rows):
        trPr = row._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit")
        trPr.append(cs)
        if len(rows) <= 16 and i < len(rows) - 1:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.keep_with_next = True
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def add_page_number(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Businessplan Baufeld 3, Neue Mitte Werlte  |  Seite ")
    r.font.size = Pt(8)
    r.font.color.rgb = GREY
    r2 = p.add_run()
    r2.font.size = Pt(8)
    r2.font.color.rgb = GREY
    for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if t:
            f = OxmlElement("w:fldChar")
            f.set(qn("w:fldCharType"), t)
            r2._r.append(f)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = txt
            r2._r.append(it)


add_page_number(sec)
_h = [0]


def H(text):
    _h[0] += 1
    doc.add_heading(f"{_h[0]}  {text}", level=1)


# ------------------------------------------------------------------ Deckblatt
para("NEUE MITTE WERLTE", bold=True, color=RGBColor(0xC4, 0x9A, 0x45), size=11, after=2)
doc.add_paragraph("Businessplan: Restaurant, Bar und 12 Wohnungen", style="Title")
para("Baufeld 3, Neue Mitte Werlte", size=14, color=GREY, after=14)
img = os.path.join(here, "bilder", "ki_aussen_1.jpg")
if os.path.exists(img):
    doc.add_picture(img, width=Cm(16.6))
    para("Rendering zur Orientierung, keine Planung.", italic=True, color=GREY, size=8.5, after=14)
table([
    ["Bauherr", "Bessam Hasso, Werlte"],
    ["Vorhaben", "Neubau eines gemischt genutzten Gebäudes: Restaurant und Bar im Erdgeschoss, 2 Büro-Ankermieter und 5 Wohnungen im 1. Obergeschoss, 7 Wohnungen im Staffelgeschoss in Holzbau"],
    ["Struktur", "Vermietungs-GbR (Eigentümerin, Gesellschafter als Investoren) und eigene Betreiberfirma für die Gastro, die Pacht zahlt"],
    ["Grundstück", "Baufeld 3, ca. 960 m², Bebauungsplan Nr. 123 „Ehemalige Grundschule“, 1. Änderung (Entwurf 25.08.2026)"],
    ["Finanzierungsbedarf", f"{eur(B['kredit'])} (Basis ohne Eigenkapital), davon KfW-Kredite {eur(B['kredit_297'] + B['kredit_298'] + B['kredit_299'])}"],
    ["Stand", "Oktober 2026"],
], [4.0, 12.6], header=False, font=10)
para("Alle Zahlen sind Planungsannahmen auf Basis des beigefügten Rechenmodells (Bankunterlagen_Baufeld3.xlsx). Mieten, Pacht, Umsatz, Baukosten und KfW-Konditionen müssen durch Angebote, Marktdaten und die Zusagen der Banken belegt werden.", italic=True, color=GREY, size=9)
doc.add_page_break()

# ------------------------------------------------------------------ 1 Zusammenfassung
H("Zusammenfassung")
para(f"Auf dem Baufeld 3 der Neuen Mitte Werlte entsteht ein dreigeschossiges Gebäude (zwei Vollgeschosse plus Staffelgeschoss in Holzbau) mit 576 m² Grundfläche (32 × 18 m, das Maximum der Grundflächenzahl 0,6) und 1.650 m² Bruttogrundfläche (BGF, alle Geschossflächen zusammen). Im Erdgeschoss liegen Restaurant und Bar mit ca. 510 m² und ca. 190 Plätzen. Im 1. Obergeschoss mieten zwei Ankermieter Büros (100 m² Versicherungsgesellschaft o. ä., 65 m² Makler o. ä., 10 Jahre fest), dazu kommen 5 Wohnungen. Im Staffelgeschoss in Holzbau liegen 7 Wohnungen. Die 12 Wohnungen haben zusammen 655 m² Wohnfläche und werden langfristig vermietet. Das Gebäude gehört einer Vermietungs-GbR, deren Gesellschafter die Investoren sind. Die Gastro führt eine eigene Betreiberfirma des Bauherrn und zahlt 10 % vom Umsatz als Pacht (mindestens 10 €/m²).")
table([
    ["Kennzahl", "Wert"],
    ["Gesamtkosten inkl. Finanzierung in Bau- und Anlaufzeit", eur(B["k_gesamt"])],
    ["Darlehen insgesamt (Basis ohne Eigenkapital)", eur(B["kredit"])],
    ["davon KfW 297, 298 und 299 (zinsverbilligte Kredite)", f"{eur(B['kredit_297'] + B['kredit_298'] + B['kredit_299'])} ({pct(B['kredit_kfw_anteil'], 0)})"],
    ["Mischzins über alle Darlehen", pct(B["mischzins"], 2)],
    ["Kapitaldienst (Zinsen und Tilgung) pro Monat", eur(B["rate_monat"])],
    ["Zinsvorteil durch KfW-Kredite pro Jahr (gegenüber Hausbank 4 %)", eur(B["foerder_zins_jahr"])],
    ["Nettoertrag der GbR pro Monat", eur(B["c_netto_immo"])],
    ["Ergebnis der GbR pro Monat nach Kapitaldienst", eurs(B["c_ergebnis"])],
    ["Kapitaldienstdeckung der GbR (DSCR, Verhältnis Ertrag zu Raten)", f"{fmt(B['dscr'], 2)}, mit Gastro-Gewinn des Bauherrn {fmt(B['dscr_gesamt'], 2)}"],
    ["Betriebsergebnis der Betreiberfirma nach Pacht pro Monat", eurs(B["c_gastro"])],
    ["Ertragswert (vereinfacht)", eur(B["ertragswert"])],
    ["Beleihungswert nach 10 % Sicherheitsabschlag", eur(B["beleihungswert"])],
    ["Beleihungsauslauf (Darlehen im Verhältnis zum Beleihungswert)", pct(B["auslauf"], 0)],
], [11.0, 5.6], right_cols=(1,), font=9.5)
para("Kernaussagen", bold=True, color=GREEN, after=2)
bullets([
    ("Die GbR trägt die Raten ohne Eigenkapital knapp nicht. ", f"Die Kapitaldienstdeckung der GbR liegt bei {fmt(B['dscr'], 2)}, das Ergebnis bei {eurs(B['c_ergebnis'])} im Monat. Mit Eigenkapital der Gesellschafter (siehe Szenarien) wird die Deckung 1,2 erreicht."),
    ("Die Gastro ist getrennt. ", f"Die Betreiberfirma verdient {eurs(B['c_gastro'])} im Monat nach Pacht, das gehört dem Bauherrn. Die GbR bekommt {eur(B['c_pacht'])} Pacht im Monat."),
    ("Die Büro-Ankermieter sichern einen Teil. ", f"Die zwei Büros bringen {eur(B['b_miete_jahr'])} im Jahr über 10 Jahre fest und decken {pct(B['b_anteil_kd'], 0)} des Kapitaldienstes, zusammen mit den Wohnungen decken die langfristigen Mieten {pct(B['b_wohn_anteil_kd'], 0)}."),
    ("Förderung senkt die Zinslast. ", f"Die drei KfW-Kreditprogramme decken {pct(B['kredit_kfw_anteil'], 0)} des Darlehens zu 2,5 bis 3,0 % ab und sparen {eur(B['foerder_zins_jahr'])} Zinsen im Jahr, der Mischzins liegt bei {pct(B['mischzins'], 2)} statt 4,0 %. Steuerliche Abschreibungen sind eine Option."),
    ("Der Beleihungswert ist die Hürde. ", f"Der Ertragswert von {mio(B['ertragswert'])} liegt unter den Kosten von {mio(B['k_gesamt'])}, der Beleihungsauslauf beträgt {pct(B['auslauf'], 0)}. Die Bank wird zusätzliche Sicherheiten oder Eigenkapital in der Größenordnung von {mio(B['eigenkapital_80'])} verlangen."),
    ("Airbnb lohnt sich nicht. ", "Ein 60-m²-Airbnb-Apartment bringt bei der Werlter Auslastung (17 %, Emsland 36 %) deutlich weniger als eine langfristige Miete, deshalb bleiben alle 12 Wohnungen langfristig vermietet."),
])

# ------------------------------------------------------------------ 2 Vorhaben
H("Vorhaben und Standort")
para("Das Grundstück liegt östlich des Rathauses und südlich der neuen Planstraße zwischen Markt- und Kirchstraße. Der Bebauungsplan Nr. 123 weist ein Mischgebiet mit mindestens zwei und höchstens drei Geschossen aus, gewerbliche Nutzung im Erdgeschoss ist ausdrücklich erwünscht. Die Baureife liegt vor, ein Baubeginn ist jederzeit möglich.")
table([
    ["Festsetzung", "Wert im Bebauungsplan", "Entwurf"],
    ["Grundflächenzahl (GRZ)", "0,6, das sind max. 576 m²", "576 m² (60 %, Maximum)"],
    ["Vollgeschosse", "zwei", "Erdgeschoss und 1. Obergeschoss, dazu Staffelgeschoss"],
    ["Traufhöhe / Höhe", "6,50 m / 12,00 m", "Hauptbaukörper 6,50 m, gesamt ca. 9,90 m"],
    ["Dachform", "Details im Bebauungsplan", "Flachdach, Staffelgeschoss 0,8 m rundum zurückgesetzt"],
    ["Stellplätze", "auf dem Grundstück in ausreichender Zahl", f"ca. 6–8 auf dem Grundstück, Bedarf ca. {round(B['stellplatz_bedarf'])}"],
], [4.3, 5.6, 6.7], font=9)
para("Offene Punkte mit der Stadt: Zulässigkeit der 576 m² Grundfläche (das Baufenster im Plan wirkt nach unserer Schätzung kleiner), Einordnung des Staffelgeschosses (498 m², 86 % der Fläche darunter) und des Flachdachs sowie die Stellplätze (Mitnutzung der öffentlichen Parkfläche oder Ablöse). Diese Punkte sind schriftlich zu klären.", after=4)
para("Zeitplan der Stadt: Stellplatz alte Grundschule ab November 2026, Planstraße ab März 2027, Marktplatz und Rathausumfeld fertig Ende 2028. Unser Baubeginn ist Mitte 2027, die Bauzeit beträgt 15 Monate, die Eröffnung erfolgt gemeinsam mit der neuen Mitte Ende 2028.")

# ------------------------------------------------------------------ 3 Baukonzept
H("Baukonzept und Flächen")
para("Das Gebäude hat eine Grundfläche von 32 × 18 m (576 m², das Maximum der Grundflächenzahl). Das Erdgeschoss ist vollverglast und gehört ganz der Gastro, Treppenhaus und Aufzug liegen am Westende und erschließen Büros und Wohnungen getrennt von der Gastro. Im 1. Obergeschoss liegen die zwei Büros und 5 Wohnungen, im Staffelgeschoss 7 Wohnungen. Das 1. Obergeschoss ist in rotbraunem Klinker mit Balkonen und Milchglas-Brüstungen ausgeführt, das Staffelgeschoss in Holzbau mit schmaler Dachterrasse (ca. 0,8 m, 77 m²) rundum. Holzbau spart ca. 184.000 € gegenüber Massivbau (Annahme, Angebot der Zimmerei nötig) und hilft beim Effizienzhaus-40-Standard.")
table([
    ["Geschoss", "BGF", "Nutzung", "Einheiten", "Fläche"],
    ["Erdgeschoss", "576 m²", "Restaurant und Bar, Séparée, Küche", "1", "ca. 510 m²"],
    ["1. Obergeschoss", "576 m²", "Büro 1, Büro 2, Wohnen", "2 + 5 × 64 m²", "165 m² Büro, 321 m² Wohnen"],
    ["Staffelgeschoss (Holzbau)", "498 m²", "Wohnen", "7 × 48 m²", "334 m²"],
    ["Summe", "1.650 m²", "", "12 Wohnungen, 2 Büros", "655 m² Wohnen, 165 m² Büro"],
], [4.0, 2.2, 4.8, 2.6, 3.0], bold_rows=(4,), font=9)
_w = [os.path.join(here, "bilder", n) for n in ("ki_wohnung_og.jpg", "ki_wohnung_staffel.jpg")]
if all(os.path.exists(p) for p in _w):
    _t = doc.add_table(rows=1, cols=2)
    for _i, _p in enumerate(_w):
        _c = _t.cell(0, _i); _c.paragraphs[0].add_run().add_picture(_p, width=Cm(8.0))
    para("Renderings der Wohnungen: links 1. OG (ca. 64 m², Balkon), rechts Staffelgeschoss in Holzbau (ca. 48 m², Dachterrasse). Zur Orientierung, keine Planung.", italic=True, color=GREY, size=8.5, after=6)
para("Mietaufstellung", bold=True, color=GREEN, after=2)
rows = [["Wohnungen", "Geschoss", "Fläche", "Miete je m²", "Kaltmiete / Monat", "Kaltmiete / Jahr"]]
for e in B["einheiten"]:
    rows.append([e["nr"], e["geschoss"], fmt(e["m2"], 1) + " m²", fmt(e["miete_m2"], 2) + " €", eur(e["miete"]), eur(e["jahr"])])
rows.append(["Summe Wohnen", "", fmt(B["wf"], 1) + " m²", "", eur(B["miete_voll_monat"]), eur(B["miete_voll_monat"] * 12)])
rows.append(["Gastro-Pacht (10 % vom Umsatz)", "EG", "510,0 m²", fmt(B["pacht_monat"] / 510, 2) + " €", eur(B["pacht_monat"]), eur(B["pacht_monat"] * 12)])
for a in B["anker"][:2]:
    rows.append([a[0].split(":")[0] + " (Ankermieter)", "1. OG", fmt(a[1], 1) + " m²", fmt(a[2], 2) + " €", eur(a[3]), eur(a[4])])
rows.append(["Rohertrag gesamt", "", "", "", eur(B["rohertrag_monat"]), eur(B["rohertrag"])])
table(rows, [3.6, 2.0, 2.4, 2.4, 3.2, 3.0], right_cols=(2, 3, 4, 5), bold_rows=(3, 7), font=9)
para("Die Miete von 11,18 €/m² (950 € für 85 m², Annahme des Bauherrn) liegt am oberen Rand der Portalwerte für Neubau in Werlte (ca. 10,7 bis 11,0 €/m²). Nebenkosten (Grundsteuer, Versicherung, Betriebskosten) werden auf die Mieter umgelegt.", italic=True, color=GREY, size=9)


# ------------------------------------------------------------------ Gewerbe
H("Gewerbeflächen: große Gastro und zwei Ankermieter")
para("Die Grundfläche wurde auf das zulässige Maximum von 576 m² (GRZ 0,6 × 960 m²) vergrößert. Das Erdgeschoss gehört vollständig der Gastro, abzüglich Treppenhaus, Aufzug und Eingängen (66 m²) bleiben 510 m². Die Größe ist aus dem Platzbedarf abgeleitet: 160 Plätze im Gastraum und 30 im Séparée brauchen mit Bar, Küche, Lager, WC und Eingang genau diese Fläche. Das sind 2,7 m² je Platz (Richtwert 2,5 bis 3 m²).")
rows = [["Gastro-Flächenbedarf", "Menge", "Fläche"]]
for r_ in B["gastro_bedarf"]:
    rows.append([r_[0], f"{r_[1]} Plätze" if r_[1] > 1 else "–", fmt(r_[3]) + " m²"])
rows.append(["Gastro gesamt (ca. 190 Plätze)", "", fmt(B["g_bedarf"]) + " m²"])
table(rows, [9.0, 3.8, 3.8], right_cols=(1, 2), bold_rows=(8,), font=9)
para(f"Der Gastro-Umsatz von {eur(B['g_umsatz_monat'])} im Monat entspricht ca. {fmt(B['g_umsatz_platz'])} € je Sitzplatz und Jahr. Zum Vergleich: Der Median in Österreich liegt für Betriebe mit weniger als 100 Plätzen bei ca. 12.000 € (Fitness-Check Gastronomie 2026). Die Annahme liegt damit deutlich unter dem Branchen-Median. Die Pacht beträgt {pct(B['g_pacht_quote'], 1)} vom Umsatz (üblich 6 bis 12 %), mindestens aber 10 €/m².", after=4)
para("Ankermieter Büro", bold=True, color=GREEN, after=2)
para("Im 1. Obergeschoss mit Aufzug und eigenem Eingang liegen zwei Büros für langfristige Ankermieter: ein größeres Büro (100 m², Versicherungsgesellschaft oder ähnlicher Mieter mit zentralem Büro) und ein kleineres Büro (65 m², kleiner Makler oder Dienstleister). Beide Mietverträge sollen 10 Jahre fest laufen, mit Indexmiete (Anpassung an die Inflation). Der Vermieter übernimmt einen Grundausbau (Böden, Decken, Elektro) von 150 €/m², der Mieter den Rest.")
rows = [["Ankermieter", "Fläche", "Miete je m²", "Miete pro Monat", "Miete pro Jahr"]]
for a in B["anker"][:2]:
    rows.append([a[0], fmt(a[1]) + " m²", fmt(a[2], 2) + " €", eur(a[3]), eur(a[4])])
rows.append(["Summe Büro, 10 Jahre fest", fmt(B["b_m2"]) + " m²", fmt(B["b_miete_m2"], 2) + " €", eur(B["b_miete_jahr"] / 12), eur(B["b_miete_jahr"])])
table(rows, [6.0, 2.2, 2.4, 3.0, 3.0], right_cols=(1, 2, 3, 4), bold_rows=(3,), font=9)
bullets([
    f"Die Büros bringen über die Vertragslaufzeit von 10 Jahren zusammen ca. {mio(B['b_ueber_laufzeit'])} (mit Indexierung von 2 % pro Jahr) und machen {pct(B['anteil_buero'], 0)} des Rohertrags aus.",
    f"Sie decken {pct(B['b_anteil_kd'], 0)} des Kapitaldienstes. Zusammen mit den Wohnungen decken die langfristigen Mieten {pct(B['b_wohn_anteil_kd'], 0)}, den Rest tragen Pacht und Gastro-Gewinn.",
    "Büromieten sind Annahmen (9,50 und 10,00 €/m²), für Werlte liegen keine Büromarktdaten vor. Vorverträge mit den Ankermietern sollten vor Baubeginn vorliegen, sie sind für die Bank ein wichtiger Nachweis.",
    "Die Büros zählen zum Nichtwohnteil und werden mit der Gastro über das KfW-Programm 299 finanziert.",
])

# ------------------------------------------------------------------ 4 Gastro
H("Gastro-Konzept")
para("Die Gastro nutzt das ganze Erdgeschoss (ca. 510 m²) als Bar-Restaurant für den ganzen Tag mit dem Hauptfokus auf dem Abend. Morgens gibt es Frühstück (am Wochenende Brunch), mittags einen Mittagstisch für Beschäftigte aus Rathaus und Umgebung. Ab dem späten Nachmittag wird das Haus zum Abendrestaurant mit regionaler, moderner Küche, ab 21 Uhr zur Bar mit Cocktails, Wein, Bier und leiser Musik (Fr und Sa bis 01 Uhr). Dazu kommen Feiern, Live-Abende und Themenabende im Séparée (abgetrennter Raum mit 30 Plätzen). Die Gestaltung folgt dem Referenzbild des Bauherrn: olivgrüne Vertäfelung, Cognac-Samtbanketten, Eiche, anthrazitfarbene Theke, Stahl-Glas-Trennwand und warmes Licht.")
table([
    ["Merkmal", "Annahme"],
    ["Plätze", "ca. 190 innen (160 Gastraum, 30 Séparée), ca. 60 auf der Terrasse, 12 Barhocker"],
    ["Öffnungszeiten", "Di–Fr 11:30–23 Uhr, Sa 10–01 Uhr, So 10–21 Uhr, Montag Ruhetag"],
    ["Umsatz", f"{eur(B['g_umsatz_monat'])} pro Monat (netto), davon {pct(B['g_abend_anteil'], 0)} am Abend, ca. {eur(round(B['g_umsatz_platz'], -2))} je Sitzplatz und Jahr"],
    ["Marge vor Pacht", "30,5 % (Branchen-Richtwert, nicht aus Werlte)"],
    ["Pacht an das Haus", f"10 €/m², {eur(B['pacht_monat'])} pro Monat (ca. " + pct(B['g_pacht_quote'], 1) + " vom Umsatz)"],
    ["Ausbau", "190.000 € (1.000 € je Platz nach dem Budget des Bauherrn, Angebote nötig), dazu Büro-Ausbau 150 €/m²"],
], [4.0, 12.6], font=9)
para(f"Der Umsatz setzt sich aus Tagesteilen zusammen. Der Abend (Restaurant, Bar, Feiern) bringt {pct(B['g_abend_anteil'], 0)} des Umsatzes, Frühstück und Mittag füllen das Haus am Tag. Öffnungstage, Gäste und Bon sind Annahmen, es liegen keine Marktdaten für Werlte vor.", after=4)
rows = [["Tagesteil", "Zeit", "Tage", "Gäste/Tag", "Ø Bon", "Umsatz/Monat", "Anteil"]]
for nm, zt, tg, gs, bon, um, an in B["tagesteile"]:
    rows.append([nm, zt, fmt(tg, 0), fmt(gs, 0), eur(bon), eur(um), pct(an, 0)])
rows.append(["Summe", "", "", "", "", eur(B["g_umsatz_monat"]), "100 %"])
table(rows, [4.6, 4.2, 1.2, 1.7, 1.4, 2.2, 1.3], right_cols=(2, 3, 4, 5, 6), bold_rows=(8,), font=8.5)
rows = [["Umsatz pro Monat", "Gewinn vor Pacht", "Gewinn nach Pacht (Betreiber)"]]
for u, g, n in B["gastro_umsatz"]:
    rows.append([eur(u), eur(g), eurs(n)])
table(rows, [5.0, 5.8, 5.8], right_cols=(1, 2), bold_rows=(4,), font=9)
para(f"Die Betreiberfirma deckt die Mindestpacht ab ca. {eur(round(B['g_breakeven'], -2))} Umsatz im Monat. Die Pacht (Maximum aus 10 €/m² und 10 % vom Umsatz) geht an die GbR, das Betriebsergebnis nach Pacht gehört der Betreiberfirma. Der Lohn des Bauherrn ist nicht gerechnet. Ausführliche Gestaltung, Grundriss, Speisekarte und Personalplan stehen im Gastro-Konzept.", after=4)

# ------------------------------------------------------------------ Struktur
H("Struktur: Vermietungs-GbR und Betreiberfirma")
para("Das Gebäude gehört einer Vermietungs-GbR (Gesellschaft bürgerlichen Rechts), deren Gesellschafter die Investoren sind. Sie nimmt die Darlehen auf, vermietet die 12 Wohnungen und die 2 Büros und verpachtet die Gastro. Die Gastro führt eine eigene Betreiberfirma des Bauherrn, sie zahlt Pacht an die GbR (10 % vom Umsatz, mindestens 10 €/m²) und behält das Betriebsergebnis. So bleibt die GbR eine reine Vermietungsgesellschaft, und die Gastro-Risiken liegen beim Betreiber.")
bullets([
    f"GbR: Nettoertrag {eur(B['c_netto_immo'])} im Monat, Kapitaldienst {eur(-B['c_kd'])}, Ergebnis {eurs(B['c_ergebnis'])} im Monat ohne Eigenkapital.",
    f"Betreiberfirma: Betriebsergebnis nach Pacht {eurs(B['c_gastro'])} im Monat bei {eur(B['g_umsatz_monat'])} Umsatz, ohne Lohn des Bauherrn.",
    "Eine GbR haftet mit dem Privatvermögen aller Gesellschafter. Betreibt die GbR selbst die Gastro, wird sie insgesamt gewerblich (Gewerbesteuer), deshalb die Trennung. Rechtsform, Haftung und Steuer mit Anwalt und Steuerberater klären.",
])

# ------------------------------------------------------------------ 5 Kosten
H("Kosten")
rows = [["Posten", "Rechnung", "Betrag", "Anteil"]]
kt = [("Grundstück inkl. Steuer und Notar", "960 m² × 230 € + ca. 7 %", B["k_land_ges"]), ("Bau, Massivbau", "1.650 m² × 2.200 €", B["k_bau_massiv"]), ("Abschlag Holzbau Staffelgeschoss", "498 m² × 400 €", B["k_holz"]), ("Dachterrasse rundum", "77 m² × 450 €", B["k_terrasse"]), ("Baunebenkosten", "15 % vom Bau", B["k_bnk"]), ("Mehrkosten Effizienzhaus 40 und QNG", "3 % auf Bau inkl. Nebenkosten", B["k_eh40"]), ("Ausbau Gastro, Büros und 4 zusätzliche Wohnungen", "Gastro 190.000 €, Büros 150 €/m², je Wohnung über 8: 15.000 €", B["k_ausbau"]), ("Finanzierungskosten", "Bauzeit, Bereitstellung, Anlaufzeit", B["k_fin"])]
for a, b_, c in kt:
    rows.append([a, b_, eur(c), pct(c / B["k_gesamt"], 1)])
rows.append(["Gesamtkosten", "", eur(B["k_gesamt"]), "100 %"])
table(rows, [6.0, 5.2, 3.0, 2.4], right_cols=(2, 3), bold_rows=(9,), font=9)
para(f"Das entspricht {eur(B['kosten_m2_bgf'])} je m² BGF. Baukosten von 2.200 €/m² (Bekanntenpreis des Bauherrn) und die Baunebenkosten sind durch Angebote von Bauunternehmen und Zimmerei zu belegen. QNG steht für das Qualitätssiegel Nachhaltiges Gebäude.", italic=True, color=GREY, size=9)

# ------------------------------------------------------------------ 6 Finanzierung
H("Finanzierung mit KfW-Krediten")
para("Die Basisrechnung geht von 100 % Fremdfinanzierung aus, die Gesellschafter bringen kein Eigenkapital ein (im Blatt Annahmen einstellbar, siehe Szenarien). Die Kosten werden mit den zinsverbilligten KfW-Krediten „Klimafreundlicher Neubau“ und einem Darlehen der Hausbank gedeckt. Die KfW zahlt im Neubau keinen Zuschuss, die Förderung ist der niedrigere Zins.")
table([
    ["Programm", "Wofür", "Rahmen (mit QNG)", "Im Projekt", "Zins"],
    ["KfW 297", "selbst genutzte Wohnungen", "bis 150.000 € je Wohnung", eur(B["kredit_297"]), "2,50 %"],
    ["KfW 298", "vermietete Wohnungen", "bis 150.000 € je Wohnung", eur(B["kredit_298"]), "2,50 %"],
    ["KfW 299", "Gastro und Büros (Nichtwohngebäude)", "bis 2.000 € je m² Nettogrundfläche", eur(B["kredit_299"]), "3,00 %"],
    ["Hausbank", "Rest inkl. Bauzeitzinsen", "–", eur(B["kredit_bank"]), "4,00 %"],
    ["Summe", "", "", eur(B["kredit"]), pct(B["mischzins"], 2)],
], [2.2, 4.0, 4.6, 3.2, 2.6], right_cols=(3, 4), bold_rows=(5,), font=9)
para("Voraussetzungen und Hinweise", bold=True, color=GREEN, after=2)
bullets([
    "Effizienzhaus 40 (Wohnen) bzw. Effizienzgebäude 40 (Gastro) und QNG-Zertifikat für den vollen Kreditrahmen. Mehrkosten angenommen mit 3 % der Baukosten.",
    "Heizung ohne Öl, Gas und Biomasse, zum Beispiel Wärmepumpe oder Fernwärme. Ein Energieeffizienz-Experte plant und bestätigt den Standard.",
    "Antrag über die Hausbank vor Baubeginn (Vorhabenbeginn). Es gibt keinen Rechtsanspruch, der Zins gilt am Tag der Zusage.",
    "Wohnteil (297/298) und Gastro (299) werden bei gemischter Nutzung getrennt gefördert. Das Programm 297 gilt für selbst genutzte Wohnungen, 298 für vermietete, die Konditionen sind gleich. Im Rechenmodell sind alle 12 Wohnungen vermietet (298), eine Selbstnutzung lässt sich im Blatt Annahmen einstellen.",
    "Die KfW-Zinsen in den Quellen (Ratgeber, Oktober 2026) schwanken zwischen 0,6 % und 3,05 %. Angesetzt sind 2,5 % (Wohnen) und 3,0 % (Gastro). Die Hausbank und die KfW müssen die Konditionen bestätigen.",
])
para("Bau- und Anlaufzeit", bold=True, color=GREEN, after=2)
para(f"Das Grundstück wird zu Beginn bezahlt, die Baukosten fließen über 15 Monate. Danach folgen 12 Monate tilgungsfreie Anlaufzeit, in der nur Zinsen anfallen und von der Hausbank mitfinanziert werden (mit der Bank zu verhandeln). Zinsen und Bereitstellungsgebühr (3 % p. a. ab Monat 7 auf die noch nicht abgerufene Bausumme) betragen in dieser Zeit {eur(B['k_fin'])}. Zu Beginn der Rückzahlung stehen {eur(B['kredit'])} Darlehen.")

H("Förderungen im Überblick")
para("In die Rechnung eingebaut sind die KfW-Kredite. Weitere Förderungen sind als Option beschrieben, ihre Fristen und Voraussetzungen müssen Steuerberater und NBank prüfen.")
table([
    ["Förderung", "Inhalt", "Wirkung im Projekt"],
    ["KfW 298 (vermietete Wohnungen)", "bis 150.000 € je Wohnung, Zins 2,5 % statt 4 %", f"{eur(B['kredit_298'])}, spart {eur(B['kredit_298'] * 0.015)} im Jahr"],
    ["KfW 299 (Gastro und Büros)", "bis 2.000 € je m² Nettogrundfläche, Zins 3,0 %", f"{eur(B['kredit_299'])}, spart {eur(B['kredit_299'] * 0.01)} im Jahr"],
    ["Zinsvorteil KfW gesamt", "gegenüber reiner Hausbank-Finanzierung zu 4,0 %", f"{eur(B['foerder_zins_jahr'])} im Jahr"],
    ["Degressive Abschreibung (Option)", "5 % vom Restwert im Wohnteil statt 3 % linear (§ 7 Abs. 5a EStG)", f"Abschreibung {eur(B['gs_afa_opt'])} statt {eur(B['gs_afa'])} im ersten Jahr (mit Sonder-AfA)"],
    ["Sonder-AfA Mietwohnungsneubau (Option)", "zusätzlich 5 % in 4 Jahren, Baukostengrenze 5.200 €/m², 10 Jahre Vermietung (§ 7b EStG)", "im Wohnteil, in der Zahl oben enthalten"],
    ["NBank Mietwohnraumförderung (Option)", "zinsloses Darlehen, Zuschuss 2 bis 3 € je m² Wohnfläche und Monat gegen Mietbindung, Mietobergrenze ca. 6,50 bis 6,80 €/m²", "nicht gerechnet, passt nicht zur angesetzten Miete von 11,18 €/m²"],
], [4.6, 7.0, 5.0], font=8.5)
para("Hinweis: Die Fristen der steuerlichen Förderungen und die aktuellen NBank-Konditionen sind in den Quellen nicht eindeutig und müssen vor einer Entscheidung geprüft werden.", italic=True, color=GREY, size=9)

# ------------------------------------------------------------------ 7 Abzahlungsplan
H("Abzahlungsplan")
para(f"Die Darlehen werden als Annuitätendarlehen (gleichbleibende Rate) mit 1 % Anfangstilgung zurückgezahlt. Rate = Darlehen × (Zins + Tilgung) / 12. Die Zinsbindung beträgt 10 Jahre, danach wird der gleiche Zins angenommen. Der vollständige monatliche Plan über 35 Jahre steht im Excel-Blatt „Tilgungsplan“, eine Jahresübersicht im Blatt „Tilgung Jahre“.")
table([
    ["Darlehen", "Betrag bei Rate-Start", "Zins", "Tilgung", "Rate / Monat", "Rate / Jahr"],
    ["KfW Wohnen (297, 298)", eur(B["kredit_297"] + B["kredit_298"]), "2,50 %", "1,00 %", eur(B["rate_w"]), eur(B["rate_w"] * 12)],
    ["KfW Gastro (299)", eur(B["kredit_299"]), "3,00 %", "1,00 %", eur(B["rate_g"]), eur(B["rate_g"] * 12)],
    ["Hausbank", eur(B["kredit_bank"]), "4,00 %", "1,00 %", eur(B["rate_b"]), eur(B["rate_b"] * 12)],
    ["Summe", eur(B["kredit"]), pct(B["mischzins"], 2), "", eur(B["rate_monat"]), eur(B["rate_jahr1"])],
], [4.0, 3.4, 1.9, 1.9, 2.8, 2.6], right_cols=(1, 2, 3, 4, 5), bold_rows=(4,), font=9)
rows = [["Jahr", "Zinsen", "Tilgung", "Kapitaldienst", "Restschuld Jahresende"]]
for y in (1, 2, 3, 5, 10, 15, 20, 25, 30, 35):
    t = B["tilgung"][y - 1]
    rows.append([str(y) + (" (Ende Zinsbindung)" if y == 10 else ""), eur(t["zins"]), eur(t["tilg"]), eur(t["rate"]), eur(t["rest"])])
table(rows, [4.2, 3.0, 3.0, 3.2, 3.2], right_cols=(1, 2, 3, 4), bold_rows=(5,), font=9)
para(f"Nach 10 Jahren beträgt die Restschuld {eur(B['rest_10'])}. Die Anschlussfinanzierung ist eingeplant, ein Zinsanstieg um einen Prozentpunkt auf die Restschuld kostet ca. {eur(B['rest_10'] * 0.01 / 12)} pro Monat mehr. Die Bank kann eine höhere Tilgung verlangen, im Modell ist sie einstellbar.", after=4)

# ------------------------------------------------------------------ 8 Ertrag
H("Ertrag und Kapitaldienst")
para("Die Tabelle zeigt die Vermietungs-GbR. Das Betriebsergebnis der Gastro gehört der Betreiberfirma des Bauherrn und ist nur zur Information aufgeführt.", italic=True, color=GREY, size=9)
table([
    ["Position", "pro Monat", "pro Jahr"],
    ["Kaltmiete Wohnen (12 Wohnungen)", eurs(B["c_miete"]), eurs(B["c_miete"] * 12)],
    ["Büromieten (2 Ankermieter, 10 Jahre fest)", eurs(B["c_buero"]), eurs(B["c_buero"] * 12)],
    ["Pacht Gastro (10 % vom Umsatz, mindestens 10 €/m²)", eurs(B["c_pacht"]), eurs(B["c_pacht"] * 12)],
    ["Rücklagen (10 % von Miete, Büro und Pacht)", eurs(B["c_rueck"]), eurs(B["c_rueck"] * 12)],
    ["Nettoertrag Immobilie", eurs(B["c_netto_immo"]), eurs(B["c_netto_immo"] * 12)],
    ["Kapitaldienst (Zinsen und Tilgung)", eurs(B["c_kd"]), eurs(B["c_kd"] * 12)],
    ["Ergebnis der GbR nach Kapitaldienst", eurs(B["c_ergebnis"]), eurs(B["c_ergebnis"] * 12)],
    [f"Betriebsergebnis Gastro nach Pacht (Betreiberfirma, {eur(B['g_umsatz_monat'])} Umsatz)", eurs(B["c_gastro"]), eurs(B["c_gastro"] * 12)],
    ["Gesamtergebnis Bauherr (zur Information)", eurs(B["c_gesamt"]), eurs(B["c_gesamt"] * 12)],
], [9.0, 3.8, 3.8], right_cols=(1, 2), bold_rows=(5, 7, 9), font=9)
bullets([
    ("Kapitaldienstdeckung (DSCR) der GbR: ", f"{fmt(B['dscr'], 2)}, nur aus Wohnen und Büro {fmt(B['dscr_lang'], 2)}, mit dem Gastro-Gewinn des Bauherrn {fmt(B['dscr_gesamt'], 2)}. Banken verlangen meist mindestens 1,2."),
    ("Zinsdeckung: ", f"{fmt(B['zinsdeckung'], 2)} (Ertrag der GbR im Verhältnis zu den Zinsen)."),
    ("Anfangsrendite: ", f"{pct(B['anfangsrendite'], 2)} (Nettoertrag der Immobilie auf die Gesamtkosten)."),
    ("Break-even: ", f"Die GbR deckt alle Raten ab ca. {eur(round(B['breakeven_haus'], -2))} Gastro-Umsatz im Monat (Umsatzpacht)."),
])
para("Die Pacht hängt am Umsatz der Gastro und ist für die Bank der unsichere Teil des Ertrags. Ein Pachtvertrag mit Mindestpacht und Bürgschaft des Betreibers und ein überzeugendes Gastro-Konzept sind deshalb entscheidend.", italic=True, color=GREY, size=9)

# ------------------------------------------------------------------ 9 Ertragswert
H("Ertragswert und Beleihung")
para("Der Ertragswert wird vereinfacht nach der Immobilienwertermittlungsverordnung (ImmoWertV) berechnet: Rohertrag minus Bewirtschaftungskosten ergibt den Reinertrag, davon wird die Verzinsung des Bodenwerts abgezogen und der Rest mit einem Vervielfältiger (Barwertfaktor für die Restnutzungsdauer) kapitalisiert. Die Bewertung erfolgt getrennt nach Nutzung: Liegenschaftszins 4,0 % für Wohnen, 6,0 % für die Büros mit Ankermietern und 6,5 % für die Gastro-Pacht, Restnutzungsdauer 80 Jahre (Wohnen) bzw. 60 Jahre (Gewerbe), Bewirtschaftungskosten nach üblichen Sätzen. Den verbindlichen Beleihungswert ermittelt der Gutachter der Bank.")
table([
    ["Ertragswert", "Betrag"],
    ["Rohertrag pro Jahr (Mieten und Pacht)", eur(B["rohertrag"])],
    ["Bewirtschaftungskosten (Verwaltung, Instandhaltung, Mietausfall)", eur(B["bewirt"])],
    ["Reinertrag", eur(B["reinertrag"])],
    ["Bodenwert (960 m² × 230 €)", eur(B["bodenwert"])],
    [f"Gebäudeertragswert (mittlerer Vervielfältiger {fmt(B['vervielf'], 1)})", eur(B["ertragswert_geb"])],
    ["Ertragswert (Gebäude plus Boden)", eur(B["ertragswert"])],
    ["davon Wohnen", eur(B["ew_wohn"])],
    ["davon Büro (Ankermieter)", eur(B["ew_buero"])],
    ["davon Gastro (Pacht)", eur(B["ew_gastro"])],
], [11.0, 5.6], right_cols=(1,), bold_rows=(3, 6), font=9)
table([
    ["Beleihung", "Betrag"],
    ["Sachwert (Bodenwert plus Herstellungskosten des Gebäudes)", eur(B["sachwert"])],
    ["Beleihungswert (niedrigerer Wert, Sicherheitsabschlag 10 %)", eur(B["beleihungswert"])],
    ["Gesamtkosten und Darlehensbedarf", eur(B["kredit"])],
    ["Beleihungsauslauf (Darlehen im Verhältnis zum Beleihungswert)", pct(B["auslauf"], 0)],
    ["Ertragswert minus Gesamtkosten", eurs(B["wertluecke"])],
    ["Darlehen über dem üblichen Auslauf von 80 %", eur(B["eigenkapital_80"])],
], [11.0, 5.6], right_cols=(1,), bold_rows=(4,), font=9)
para("Bewertung", bold=True, color=GREEN, after=2)
para(f"Die Mieten, Büromieten und die Pacht tragen einen Ertragswert von {mio(B['ertragswert'])}, die Kosten liegen bei {mio(B['k_gesamt'])}. Bei 100 % Fremdfinanzierung ergibt sich ein Beleihungsauslauf von {pct(B['auslauf'], 0)}, Banken beleihen üblicherweise nur bis ca. 80 %. Um das Darlehen darstellen zu können, bietet der Bauherr der Bank zusätzliche Sicherheiten an, etwa Grundschulden auf weitere Immobilien, eine Bürgschaft oder Eigenkapital. Rechnerisch geht es um ca. {mio(B['eigenkapital_80'])}. Weitere Hebel sind höhere Mieten durch Vorvermietung, niedrigere Baukosten durch die Angebote der Bekannten-Unternehmen und eine Städtebauförderung (Zuschuss der Stadt, noch offen).")

# ------------------------------------------------------------------ 10 Prognose
H("Prognose und Belastungstest")
P = B["prognose"]
rows = [["Jahr", "1", "3", "5", "7", "10"]]
for lab in ("Nettoertrag Immobilie (GbR)", "Kapitaldienst", "Ergebnis der GbR nach Kapitaldienst"):
    rows.append([lab] + [eur(P[lab][y - 1]) for y in (1, 3, 5, 7, 10)])
rows.append(["Kapitaldienstdeckung (DSCR)"] + [fmt(P["Kapitaldienstdeckung der GbR (DSCR)"][y - 1], 2) for y in (1, 3, 5, 7, 10)])
rows.append(["Restschuld Jahresende"] + [eur(P["Restschuld Jahresende"][y - 1]) for y in (1, 3, 5, 7, 10)])
table(rows, [5.1, 2.3, 2.3, 2.3, 2.3, 2.3], right_cols=(1, 2, 3, 4, 5), font=8.5, bold_rows=(3,))
para(f"Annahme: Miete und Gastro-Umsatz (damit die Pacht) steigen um 1,5 % pro Jahr, Büromieten um 2 % (Indexmiete), der Kapitaldienst bleibt gleich. Die Kapitaldienstdeckung verbessert sich von {fmt(B['dscr'], 2)} auf {fmt(B['dscr_y10'], 2)} in Jahr 10.", italic=True, color=GREY, size=9)
rows = [["Belastungstest (pro Monat)", "Ergebnis", "DSCR", "zum Plan"]]
for i, (lab, e, d, z) in enumerate(B["sens"]):
    rows.append([lab, eurs(e), fmt(d, 2), "" if i == 0 else eurs(z)])
table(rows, [8.6, 2.8, 2.0, 3.2], right_cols=(1, 2, 3), bold_rows=(1,), font=9)
para("Die Tests sind vereinfacht. Das Ergebnis der GbR reagiert am stärksten auf den Gastro-Umsatz (über die Umsatzpacht) und auf den Zins. Die GbR liegt im Plan schon knapp unter 1,0, jeder Rückgang vergrößert die Lücke: bei Umsatz −40 % sinkt die Deckung auf etwa 0,8, bei einem Ausfall der Gastro auf etwa 0,5. Ein Auszug eines Ankermieters kostet rund 855 € im Monat.", after=4)

# ------------------------------------------------------------------ Gesellschafter
H("Ergebnis pro Gesellschafter")
para("Gleiche Anteile an der GbR, Basis ohne Eigenkapital, erstes Jahr nach der Anlaufzeit. Die Steuerwirkung rechnet mit einem Grenzsteuersatz von 35 % (Annahme). Verluste der GbR (Zinsen und Abschreibung übersteigen die Einnahmen) können mit anderen Einkünften verrechnet werden, das Finanzamt prüft dabei die Gewinnerzielungsabsicht.")
G = B["gs_kopf"]
rows = [["Pro Person", "1 Person", "2 Personen", "4 Personen", "8 Personen"]]
for i, lab in ((2, "Cash pro Monat vor Steuern"), (1, "Cash pro Jahr vor Steuern"), (3, "Steuerliches Ergebnis pro Jahr (Verlust negativ)"), (4, "Steuerwirkung pro Jahr"), (6, "Cash pro Monat nach Steuer"), (9, "Mit Förderoption (degressive AfA und Sonder-AfA): Cash pro Monat nach Steuer"), (10, "Tilgung pro Jahr (Vermögensaufbau)")):
    rows.append([lab] + [eurs(G[i][c]) for c in (1, 2, 3, 4)])
table(rows, [6.6, 2.5, 2.5, 2.5, 2.5], right_cols=(1, 2, 3, 4), bold_rows=(5, 6), font=9)
para(f"Ohne Eigenkapital liegt der Cash knapp unter null, die Steuerwirkung des Verlusts macht das Ergebnis nach Steuer positiv. Die Tilgung von {eur(G[10][1])} im Jahr baut zusätzlich Vermögen auf. Die Förderoption (Fristen prüfen) erhöht die Abschreibung im Wohnteil und damit die Steuerersparnis.", after=4)
H("Szenarien: 12 gegen 8 Wohnungen")
para("Zum Vergleich wurde das Vorhaben mit 8 Wohnungen gerechnet (3 im 1. OG, 5 im Staffelgeschoss), jeweils ohne und mit Eigenkapital. Das Eigenkapital ist so bemessen, dass die GbR die Raten mit dem Faktor 1,2 deckt. Die Werte stammen aus einem unabhängigen Nachbau des Modells, die Basis stimmt auf den Cent mit der Excel-Datei überein. Jede zusätzliche Wohnung erhöht den KfW-Rahmen um 150.000 € zu 2,5 % und wiegt die angesetzten Mehrkosten von 15.000 € je Wohnung über 8 auf.")
Z = B["szenarien"]
rows = [["Kennzahl", "12 WE ohne EK", "8 WE ohne EK", "12 WE mit EK", "8 WE mit EK"]]
rows.append(["Gesamtkosten"] + [eur(z["gesamt"]) for z in Z])
rows.append(["KfW-Kredite 297/298/299"] + [eur(z["kfw"]) for z in Z])
rows.append(["Hausbank-Darlehen"] + [eur(z["bank"]) for z in Z])
rows.append(["Eigenkapital"] + [eur(z["ek"]) for z in Z])
rows.append(["Kapitaldienst pro Monat"] + [eur(z["rate"]) for z in Z])
rows.append(["Ergebnis der GbR pro Monat"] + [eurs(z["ergebnis_m"]) for z in Z])
rows.append(["Kapitaldienstdeckung"] + [fmt(z["dscr"], 2) for z in Z])
rows.append(["Cash pro Person nach Steuer, 8 Personen, pro Monat"] + [eurs(z["kopf"]["8"]["cash_steuer_m"]) for z in Z])
rows.append(["Eigenkapital pro Person bei 8 Personen"] + [eur(z["kopf"]["8"]["ek"]) for z in Z])
rows.append(["Betriebsergebnis Gastro (Betreiberfirma)"] + [eurs(z["betreiber_m"]) for z in Z])
table(rows, [6.0, 2.7, 2.7, 2.7, 2.7], right_cols=(1, 2, 3, 4), bold_rows=(6,), font=8.5)
para(f"Mit 12 Wohnungen brauchen die Gesellschafter {eur(Z[2]['ek'])} Eigenkapital für die Deckung 1,2, mit 8 Wohnungen {eur(Z[3]['ek'])}.", bold=True, color=GREEN)

# ------------------------------------------------------------------ 11 Airbnb
H("Prüfung: ein 60-m²-Apartment als Airbnb")
T = B["airbnb_tab"]
para("Marktlage Werlte (49757), Stand Q4 2026: Die Beherbergungsbetriebe der Samtgemeinde Werlte (ab 10 Betten) hatten zuletzt eine Auslastung von 17,4 % bei 2,7 Tagen Aufenthalt, der Emsland-Schnitt liegt bei 36,2 % (Emsland Tourismus, Quelle Landesamt für Statistik). Ferienunterkünfte kosten in Werlte im Schnitt ca. 87 € pro Nacht, 89 % liegen unter 100 €. Belegungsdaten von Airbnb oder AirDNA für Werlte lagen nicht vor, deshalb sind die Szenarien Näherungen. Angesetzt sind 90 € pro Nacht, Möblierung von 600 €/m² (36.000 €) im Kredit, Kosten von 56 % des Umsatzes (Plattform, Reinigung, Nebenkosten, Rücklage) gegenüber einer langfristigen Miete von 11,18 €/m² abzüglich 10 % Rücklagen.")
rows = [["Apartment 60 m²", "Werlte amtlich", "Emsland-Schnitt", "Optimistisch"]]
rows.append(["Auslastung"] + [pct(T[1][c], 1) for c in (1, 2, 3)])
rows.append(["Preis pro Nacht"] + [eur(T[2][c]) for c in (1, 2, 3)])
rows.append(["Netto Airbnb pro Monat"] + [eur(T[4][c]) for c in (1, 2, 3)])
rows.append(["Netto langfristige Miete pro Monat"] + [eur(T[5][c]) for c in (1, 2, 3)])
rows.append(["Kapitaldienst Möblierung pro Monat"] + [eurs(T[7][c]) for c in (1, 2, 3)])
rows.append(["Mehrertrag gegenüber langfristiger Miete pro Monat"] + [eurs(T[8][c]) for c in (1, 2, 3)])
table(rows, [7.6, 3.0, 3.0, 3.0], right_cols=(1, 2, 3), bold_rows=(6,), font=9)
para(f"Ergebnis: Airbnb lohnt sich in Werlte nicht. Erst ab ca. {pct(T[11][1], 0)} Auslastung wäre es so gut wie die langfristige Miete, in Werlte liegt sie amtlich bei 17 %. Dazu kommen Aufwand für Gäste und Reinigung. Die Wohnung bleibt deshalb langfristig vermietet.", bold=True, color=GREEN)

# ------------------------------------------------------------------ 12 Risiken
H("Chancen und Risiken")
table([
    ["Thema", "Risiko", "Gegenmaßnahme"],
    ["Sicherheiten", f"Beleihungsauslauf {pct(B['auslauf'], 0)} und Kapitaldienstdeckung {fmt(B['dscr'], 2)} bei 100 % Fremdfinanzierung", "Eigenkapital der Gesellschafter, zusätzliche Grundschulden, Bürgschaft; Pachtvertrag mit Bonitätsnachweis"],
    ["Gastro-Umsatz und Pacht", f"GbR deckt die Raten erst ab ca. {eur(round(B['breakeven_haus'], -3))} Umsatz (Umsatzpacht); bei Ausfall der Gastro fehlen ca. {eur(-B['sens'][8][3])} pro Monat zusätzlich", "Mindestpacht, Bürgschaft des Betreibers, erfahrener Betreiber, Probebetrieb"],
    ["Miete", "11,18 €/m² liegt am oberen Rand der Marktdaten", "Vorvermietung, Vergleichsangebote, Einrichtungsqualität"],
    ["Zins", "KfW-Zins und Rahmen unsicher, Folgezins nach 10 Jahren offen", "Zusage vor Baubeginn, Forward-Darlehen, höhere Tilgung später"],
    ["Haftung und Steuer", "GbR haftet persönlich, steuerliche Förderungen hängen an Fristen", "Rechtsform mit Anwalt klären, Steuerberater prüft Abschreibungen und Verlustverrechnung"],
    ["Genehmigung", "576 m², Staffelgeschoss, Flachdach, Stellplätze", "Bauvoranfrage, städtebaulicher Vertrag, Plan B mit kleinerer Grundfläche"],
    ["Standard", "KfW verlangt Effizienzhaus 40 mit QNG, Mehrkosten", "Energieeffizienz-Experte früh einbinden, Holzbau nutzen"],
    ["Baukosten", "Preise sind Annahmen (2.200 €/m²); +10 % kosten ca. 1.400 € im Monat", "Festpreisangebote Bauunternehmen und Zimmerei"],
], [3.0, 6.8, 6.8], font=8.5)
para("Chancen: zentrale Lage am neuen Marktplatz, Holzbau und Eigenleistung der Partner aus dem Bekanntenkreis, zinsverbilligte KfW-Kredite, Spielraum beim Gastro-Umsatz (Terrasse, Feiern, Catering sind nicht eingerechnet).")

# ------------------------------------------------------------------ 13 Zeitplan
H("Zeitplan und nächste Schritte")
table([
    ["Zeitpunkt", "Schritt"],
    ["Oktober 2026", "Gespräch mit der Stadt: Preis, Förderung, Stellplätze, Zulässigkeit der 576 m²"],
    ["November 2026", "Architekt beauftragen, Baufenster, Höhen und Geschosse schriftlich klären, Energieeffizienz-Experte für Effizienzhaus 40 und QNG"],
    ["Dezember 2026", "Hausbank: Finanzierung, Anlaufzeit, KfW 297, 298, 299 und Sicherheiten klären"],
    ["Q1 2027", "Städtebaulicher Vertrag, Bauantrag, Festpreisangebote, KfW-Antrag über die Hausbank vor Baubeginn"],
    ["Mitte 2027", "Baubeginn, 15 Monate Bauzeit"],
    ["Ende 2028", "Fertigstellung und Eröffnung zusammen mit der neuen Mitte"],
], [3.6, 13.0], font=9)

# ------------------------------------------------------------------ 14 Anlagen
H("Anlagen und Unterlagen für die Bank")
para("Das Rechenmodell Bankunterlagen_Baufeld3.xlsx enthält Übersicht, Annahmen, Flächen und Mieten, Kosten und Finanzierungsplan mit Förderwirkung, Bauphase, Abzahlungsplan (monatlich und jährlich), Ertrag und Kapitaldienst, Gesellschafter pro Kopf, Szenarien 12 gegen 8 Wohnungen, Gastro-Betrieb, Gastro-Tagesteile, Ertragswert, Prognose, Belastungstest, Airbnb-Prüfung und die vollständige Checkliste der Unterlagen. Die wichtigsten Unterlagen:")
rows = [["Nr.", "Unterlage", "Status"]]
for nr, name, inh, stt in B["unterlagen"]:
    rows.append([str(nr), name, stt])
table(rows, [1.2, 12.4, 3.0], font=8.5)
para("Weitere Anlagen: Präsentation (Neue-Mitte-Werlte_Baufeld3_12-Wohnungen_Restaurant-Bar.pptx), Gastro-Konzept (Neue-Mitte-Werlte_Baufeld3_Gastro-Konzept.pptx).", italic=True, color=GREY, size=9)

doc.save(OUT)
print("gespeichert", OUT)
