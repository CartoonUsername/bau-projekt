"""Businessplan-Präsentation für die Bank je Variante (A Standard B3; B überdachte Stellplätze/größere Wohnungen mit drei Optionen) – im Aufbau und Stil des früheren Bankplans.
Zahlen: finanz.py (Planungsannahmen), Geometrie: studie/vergleichsstudie_ab. Ausgabe: businessplan/Businessplan_Praesentation_<A|B>.pptx"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
import varianten_in as VI, finanz as F
HERE = os.path.dirname(os.path.abspath(__file__)); BILD = os.path.join(HERE, "bilder"); GEO = os.path.join(HERE, "..", "studie_gebaeudeformen")
GREEN = RGBColor(0x2D, 0x4A, 0x3E); BRICK = RGBColor(0x8C, 0x3B, 0x2F); CARD = RGBColor(0xF1, 0xEF, 0xEA); INK = RGBColor(0x22, 0x22, 0x22); GREY = RGBColor(0x66, 0x66, 0x66)
OKC = RGBColor(0xE3, 0xF1, 0xE6); BADC = RGBColor(0xF8, 0xDD, 0xDA); WHITE = RGBColor(255, 255, 255); GOLD = RGBColor(0xC9, 0x9A, 0x3C)
def eur(x, sign=False):
    s = f"{abs(x):,.0f}".replace(",", "."); neg = x < 0
    return ("−" if neg else ("+" if sign else "")) + s + " €"
def num(x, d=0): return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def mio(x): return num(x / 1e6, 2) + " Mio. €"
def pct(x, d=0): return num(x * 100, d) + " %"

class Deck:
    def __init__(self, group, footer_tag):
        self.prs = Presentation(); self.prs.slide_width = Inches(13.333); self.prs.slide_height = Inches(7.5); self.n = 0; self.tag = footer_tag; self.group = group
    def slide(self, title, foot=None, tag=True):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6]); self.n += 1
        if title:
            tb = s.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.8)); p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT; r = p.add_run(); r.text = title; r.font.name = "Georgia"; r.font.size = Pt(28); r.font.color.rgb = BRICK
        if tag:
            self.text(s, 0.5, 7.05, 6, 0.3, foot or self.tag, 9, GREY); self.text(s, 12.2, 7.05, 0.7, 0.3, str(self.n), 9, GREY, align=PP_ALIGN.RIGHT)
        return s
    def text(self, s, x, y, w, h, txt, size=12, color=INK, bold=False, font="Arial", align=None, anchor=None, wrap=True):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = wrap
        if anchor: tf.vertical_anchor = anchor
        lines = txt if isinstance(txt, list) else [txt]
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); r = p.add_run(); r.text = ln; r.font.size = Pt(size); r.font.color.rgb = color; r.font.bold = bold; r.font.name = font
            if align: p.alignment = align
        return tb
    def card(self, s, x, y, w, h, fill=CARD):
        sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)); sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.fill.background(); sh.adjustments[0] = 0.06; sh.shadow.inherit = False; return sh
    def kpi(self, s, x, y, w, big, small, color=BRICK, h=1.25):
        self.card(s, x, y, w, h); self.text(s, x + 0.15, y + 0.08, w - 0.3, 0.55, big, 24, color, font="Georgia"); self.text(s, x + 0.15, y + 0.65, w - 0.3, h - 0.65, small, 10, GREY)
    def note(self, s, x, y, w, h, head, body, size=11):
        self.card(s, x, y, w, h); tb = s.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.1), Inches(w - 0.3), Inches(h - 0.2)); tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        if head:
            r = p.add_run(); r.text = head + "  "; r.font.bold = True; r.font.size = Pt(size); r.font.color.rgb = BRICK; r.font.name = "Arial"
        r = p.add_run(); r.text = body; r.font.size = Pt(size); r.font.color.rgb = INK; r.font.name = "Arial"
    def bullets(self, s, x, y, w, h, items, size=12, fill=True):
        if fill: self.card(s, x, y, w, h)
        tb = s.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.12), Inches(w - 0.4), Inches(h - 0.2)); tf = tb.text_frame; tf.word_wrap = True
        for i, it in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); r = p.add_run(); r.text = "•  " + it; r.font.size = Pt(size); r.font.name = "Arial"; r.font.color.rgb = INK; p.space_after = Pt(5)
    def table(self, s, x, y, w, colw, rows, size=10, bold_rows=(), fills=None, right_from=1, rowh=0.3):
        nr, nc = len(rows), len(rows[0]); tot = sum(colw); sh = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(rowh * nr)); t = sh.table
        tblPr = sh._element.graphic.graphicData.tbl.tblPr; tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
        for j, cw in enumerate(colw): t.columns[j].width = Inches(w * cw / tot)
        for i, row in enumerate(rows):
            t.rows[i].height = Inches(rowh)
            for j, val in enumerate(row):
                c = t.cell(i, j); c.margin_left = c.margin_right = Inches(0.06); c.margin_top = c.margin_bottom = Inches(0.025); c.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf = c.text_frame; tf.word_wrap = True; p = tf.paragraphs[0]; r = p.add_run(); r.text = str(val); r.font.size = Pt(size); r.font.name = "Arial"
                if j >= right_from and i > 0 and isinstance(val, str) and (val[:1] in "+−-0123456789€" or val.endswith(("€", "%", "m²", "×"))): p.alignment = PP_ALIGN.RIGHT
                if i == 0: c.fill.solid(); c.fill.fore_color.rgb = GREEN; r.font.color.rgb = WHITE; r.font.bold = True
                else:
                    c.fill.solid(); c.fill.fore_color.rgb = (fills or {}).get((i, j), WHITE); r.font.color.rgb = INK; r.font.bold = i in bold_rows
        return sh
    def pic(self, s, path, x, y, w=None, h=None):
        from PIL import Image
        iw, ih = Image.open(path).size; ar = iw / ih
        if w and h:
            if w / h > ar: w2 = h * ar; x += (w - w2) / 2; w = w2
            else: h2 = w / ar; y += (h - h2) / 2; h = h2
        elif w: h = w / ar
        else: w = h * ar
        return s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    def save(self, path): self.prs.save(path)

# ---------- Daten ----------
TXT = {"A": dict(titel="Baufeld 3: Standardversion (B3)", sub="Businessplan für die Bank: Konzept, Finanzierung mit KfW-Krediten, Ertragswert und Abzahlungsplan", keys=["A"], names=["A – B3 Standard"],
                 kurz="Gastro im ganzen EG (576 m²), im 1. OG 3 Büro-/Wohn-Einheiten über 3,00 m Anbau, 16 Wohnungen"),
       "B": dict(titel="Baufeld 3: überdachte Stellplätze, größere Wohnungen", sub="Businessplan für die Bank: schmales Erdgeschoss, breitere Obergeschosse, drei Optionen – Finanzierung, Ertragswert, Abzahlungsplan", keys=["F1", "F2", "F3"],
                 names=["B1 bündig", "B2 Staffel 1,50 m", "B3 Staffel 3,00 m"], kurz="schmales EG (18 × 30 m), 1. und 2. OG breiter über Säulen, Stellplätze unter dem Vorbau")}
def optdata(group):
    ks = TXT[group]["keys"]; out = []
    for k in ks:
        v = VI.inp(k); r = F.rechne(v); out.append((k, v, r, VI.D[k]))
    return out
def img(k, name): return os.path.join(GEO, k, "ansichten", name + ".png")
def pln(k, name): return os.path.join(GEO, k, "plaene", name + ".png")
def hf(k, name): return os.path.join(BILD, f"hf_{k}_{name}.jpg")
BK = {"F1": "B1", "F2": "B2", "F3": "B3"}
def neu(k, name): return os.path.join(BILD, "neu", f"{BK[k]}_{name}.jpg")

def build(group):
    T = TXT[group]; O = optdata(group); multi = len(O) > 1; names = T["names"]; foot = "Für Bank und Stadt"
    deck = Deck(group, foot); P = F.P
    r0 = O[0][2]; v0 = O[0][1]
    def cols(fn): return [fn(k, v, r, d) for k, v, r, d in O]
    # 1 Titel
    s = deck.slide(None, tag=False); bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(5.2), Inches(7.5)); bg.fill.solid(); bg.fill.fore_color.rgb = GREEN; bg.line.fill.background()
    deck.text(s, 0.6, 1.0, 4.2, 0.3, "NEUE MITTE WERLTE", 11, GOLD, bold=True); deck.text(s, 0.6, 1.5, 4.2, 2.3, T["titel"], 30 if len(T["titel"]) < 40 else 23, WHITE, font="Georgia")
    deck.text(s, 0.6, 3.9, 4.2, 1.2, T["sub"], 12, WHITE); deck.text(s, 0.6, 5.7, 4.2, 1.0, ["Bessam Hasso, Werlte", "Bebauungsplan Nr. 123 (2023) und 1. Änderung (Entwurf 25.08.2026)", "Stand 27.10.2026 · alle Zahlen Planungsannahmen"], 10, WHITE)
    deck.pic(s, (os.path.join(BILD, "neu", "_title_B.jpg") if multi else hf("A", "persp")), 5.2, 0, w=8.133, h=7.5)
    # 2 Auf einen Blick
    s = deck.slide("Das Vorhaben auf einen Blick", foot)
    mz = [pct(r["mischzins"], 2) for _, _, r, _ in O]
    if multi:
        kf = [(r['kfw_w'] + r['kfw_g']) / r['gesamt'] for _, _, r, _ in O]; rm_ = [r['rate_m'] for _, _, r, _ in O]; cs_ = [r['cash'] / 12 for _, _, r, _ in O]
        big = [f"{num(min(r['gesamt'] for _,_,r,_ in O)/1e6,1)}–{num(max(r['gesamt'] for _,_,r,_ in O)/1e6,1)} Mio. €", f"{num(min(kf)*100)}–{num(max(kf)*100)} %", f"{num(min(rm_)/1000,1)}–{num(max(rm_)/1000,1)} T€", f"{num(min(cs_)/1000,1)} bis {num(max(cs_)/1000,1)} T€"]
    else: big = [mio(r0["gesamt"]), pct((r0["kfw_w"] + r0["kfw_g"]) / r0["gesamt"]), eur(r0["rate_m"]), eur(r0["cash"] / 12, True)]
    small = ["Gesamtkosten inkl. Finanzierung in Bau- und Anlaufzeit", "des Darlehens über KfW 298 und 299", "Kapitaldienst pro Monat (Zins + 1 % Tilgung)", "Ergebnis pro Monat nach Kapitaldienst, ohne Lohn"]
    for i in range(4): deck.kpi(s, 0.5 + i * 3.1, 1.2, 2.95, big[i], small[i], color=BRICK if i != 3 else GREEN)
    rows = [["Projekt"] + (names if multi else ["Wert"])]
    rows += [["Grundstück / EG / BGF gesamt"] + cols(lambda k, v, r, d: f"960 m² / {num(d['flaeche']['eg'])} m² / {num(v['bgf'])} m²"),
             ["Nutzung"] + ([T["kurz"]] if not multi else cols(lambda k, v, r, d: f"Gastro EG, Büro, {d['mix']['standard']['we']} Wohnungen ({num(v['wfl'])} m²)")),
             ["Stellplätze (Hypothese 32 × 30 m)"] + cols(lambda k, v, r, d: "11 rückseitig, teilweise überdacht" if k == "A" else "13, davon 8 voll überdacht"),
             ["Kapitaldienstdeckung (DSCR)"] + cols(lambda k, v, r, d: f"{num(r['dscr_ges'],2)} gesamt, {num(r['dscr_imm'],2)} nur Immobilie"),
             ["Ertragswert / Beleihungsauslauf"] + cols(lambda k, v, r, d: f"{mio(r['ew'])} / {pct(r['auslauf'])}")]
    deck.table(s, 0.5, 2.8, 12.3, [3] + [4] * len(O) if multi else [3, 9], rows, 10, rowh=0.42, right_from=9)
    deck.text(s, 0.5, 5.3, 12.3, 0.8, "Der Ertrag trägt die Raten nur zusammen mit dem Gastro-Gewinn. Die Bank wird wegen des Ertragswerts zusätzliche Sicherheiten oder Eigenkapital verlangen, siehe Folie Ertragswert. Mit 100 % Fremdkapital ist das Ergebnis klein.", 12, GREEN, bold=True)
    # 3 Grundstück / Zeitplan
    s = deck.slide("Ein Eckgrundstück an der neuen Mitte", foot)
    for i, (h, b) in enumerate((("ca. 960 m²", "Baufeld 3, östlich des Rathauses, südlich der Planstraße (Zuordnung und Zuschnitt nicht vermessen)"), ("Mischgebiet", "Gewerbe im EG erwünscht, Stellplätze auf dem Grundstück"), ("Baureife", "laut Stadt vorhanden, Baubeginn jederzeit möglich (zu bestätigen)"))):
        deck.card(s, 0.5, 1.3 + i * 1.5, 5.6, 1.35); deck.text(s, 0.7, 1.4 + i * 1.5, 5.2, 0.5, h, 18, BRICK, font="Georgia"); deck.text(s, 0.7, 1.95 + i * 1.5, 5.2, 0.9, b, 11, GREY)
    for i, (d_, t_) in enumerate((("Nov 2026", "Stellplatz alte Grundschule"), ("ab März 2027", "Bau Planstraße (Erschließung)"), ("Mitte 2027", "Unser Baubeginn"), ("ab Juli 2027", "Kreisverkehr Loruper Straße"), ("Ende 2028", "Marktplatz, Rathaus fertig und unsere Eröffnung"))):
        deck.text(s, 7.0, 1.3 + i * 1.05, 5.5, 0.4, d_, 14, INK, bold=True); deck.text(s, 7.0, 1.7 + i * 1.05, 5.5, 0.4, t_, 11, GREY)
    # 4 B-Plan
    s = deck.slide("Was der Bebauungsplan vorgibt", foot)
    eg = O[0][3]["flaeche"]["eg"]
    rows = [["Festsetzung", "Plan 2023 (rechtskräftig, MI 3)", "Entwurf 2026 (1. Änderung)", "Unser Entwurf"],
            ["Vollgeschosse", "II bis III", "II zwingend (MI 3 nicht erfasst)", "EG, 1. OG und oberstes Geschoss (Holzbau)"],
            ["Traufhöhe / Höhe", "9,80 m / 15,00 m", "6,50 m / 12,00 m", "Attika " + ("+9,90 m" if group == "A" else "+12,00 m (hypothetisches Höhenschema)")],
            ["Grundflächenzahl", "0,6", "–", f"EG {num(eg)} m² = {pct(eg/960)} der Hypothese 960 m²"],
            ["Dachform", "Hauptdach ≥ 38°, Flachdach nur untergeordnet", "Dach ≥ 38°", "Flachdach mit Staffel / Terrasse"],
            ["Baugrenze MI 3", "10 m West, 3 m übrige Seiten; Bezug OK Fahrbahn", "3 m", "Baufenster ≈ 27,7 × 15,9 m (abgeleitet)"],
            ["Stellplätze", "auf dem Grundstück", "63 Plätze im Parkplatz", "siehe Stellplatzfolie"]]
    deck.table(s, 0.5, 1.2, 12.3, [2, 4, 3, 4], rows, 10, rowh=0.5, right_from=9)
    deck.note(s, 0.5, 5.0, 12.3, 1.6, "Schriftlich klären:", "Ist Baufeld 3 tatsächlich MI 3 / Flurstück 59/1? Passt das Gebäude in das Baufenster (EG und Vorbau liegen nach der Schätzung außerhalb)? Sind Flachdach/Staffel, Traufhöhe und Höhenbezug (OK Fahrbahn) befreit oder zulässig? Diese Folien enthalten keine Aussage zur baurechtlichen Zulässigkeit.")
    # 5 Holzbau
    s = deck.slide("Oberstes Geschoss in Holzbau", foot)
    if not multi:
        k, v, r, d = O[0]; deck.kpi(s, 0.5, 1.2, 4.0, f"{num(v['bgf_top'])} m²", "oberstes Geschoss in Holzbau, 0,80 m rundum zurückgesetzt"); deck.kpi(s, 4.65, 1.2, 4.0, eur(v["bgf_top"] * P["holz_abschlag"]), "Ersparnis gegenüber Massivbau (400 € je m², Annahme)", GREEN); deck.kpi(s, 8.8, 1.2, 4.0, f"{num(v['terr'])} m²", "Dachterrasse (nicht in der BGF), Fläche OG1 minus oberstes Geschoss")
    else:
        for i, (k, v, r, d) in enumerate(O): deck.kpi(s, 0.5 + i * 4.15, 1.2, 4.0, f"{num(v['bgf_top'])} m²", f"{names[i]}: oberstes Geschoss, Ersparnis {eur(v['bgf_top']*P['holz_abschlag'])}, Terrasse {num(v['terr'])} m²")
    deck.bullets(s, 0.5, 2.8, 12.3, 3.0, ["Leichter und schneller: weniger Last auf dem Klinker-Geschoss, kürzere Bauzeit.", "Zwei Partner aus dem Bekanntenkreis (Bauunternehmen unten, Zimmerei oben) können Preise und Termine gemeinsam angeben.", "Holzbau hilft beim QNG-Nachweis und beim Effizienzhaus-40-Standard (KfW-Voraussetzung).",
                                           "Brandschutz (Holzbau bis Gebäudeklasse 4, Aufzug und Treppenhaus massiv) und Schallschutz muss der Architekt nachweisen.", "Der Abschlag von 400 €/m² ist eine Annahme aus dem früheren Plan, kein Angebot."], 12)
    # 6 Geschosse
    s = deck.slide("Zwei Geschosse plus oberstes Geschoss" if group == "A" else "Schmales Erdgeschoss, breite Obergeschosse", foot)
    deck.pic(s, pln(O[min(1, len(O) - 1)][0], "schnitt"), 0.4, 1.2, w=7.3, h=4.6)
    rows = [["Ebene", "Nutzung", "BGF"] if not multi else ["Ebene", "Nutzung"] + names]
    nutz = {"A": ["Gastro ca. 440 m² mit Bar, Küche, dazu Büros, Treppenhaus, Aufzug", "Wohnungen, Flur, Kern; Anbau 3,00 m nach hinten", "Wohnungen, oberstes Geschoss in Holzbau"],
            "B": ["Gastro 18 × 30 m (Platzseite 18 m), Büro, Kern; Stellplätze im Osten", "Wohnungen, kragt 1,0 / 1,5 / 5,0 m aus (West / Platz / Ost), Säulen", "Wohnungen, Holzbau, Staffel je Option"]}[group]
    for i, (lab, kk) in enumerate((("EG", "eg"), ("1. OG", "og1"), ("oberstes Geschoss", "st"))):
        rows.append([lab, nutz[i]] + cols(lambda k, v, r, d, kk=kk: f"{num(d['flaeche'][kk], 0)} m²"))
    rows.append(["Summe", ""] + cols(lambda k, v, r, d: f"{num(v['bgf'])} m²"))
    deck.table(s, 7.9, 1.3, 5.0, [1.3, 3.6] + [1.2] * len(O), rows, 9, bold_rows=(4,), rowh=0.75 if not multi else 0.8, right_from=2)
    deck.text(s, 7.9, 5.3, 5.0, 1.0, "BGF = Bruttogrundfläche aller Geschossflächen. Schnitt schematisch aus dem Geometriemodell; Geschosshöhen " + ("aus B3-Modell." if group == "A" else "hypothetisch (Höhenschema 12,00 m), nicht gesichert."), 9, GREY)
    # 7 Skizzen
    s = deck.slide("Skizzen der Geschosse", foot); kk = O[min(1, len(O) - 1)][0]
    for i, (n_, lab) in enumerate((("plan_eg", "Erdgeschoss"), ("plan_og1", "1. Obergeschoss"), ("plan_st", "oberstes Geschoss"))):
        deck.text(s, 0.5 + i * 4.15, 1.15, 4, 0.4, lab + (f" ({names[min(1, len(O)-1)]})" if multi and i == 2 else ""), 13, INK, bold=True); deck.pic(s, pln(kk, n_), 0.5 + i * 4.15, 1.6, w=4.0, h=4.3)
    deck.note(s, 0.5, 6.0, 12.3, 0.9, None, "Schematische Skizzen aus dem Geometriemodell. " + ("Raumaufteilung der Obergeschosse nach Planstand B3." if group == "A" else "Raumaufteilung der Obergeschosse ist NOCH OFFEN (keine Raumdaten); Zonen nur als Annahme."), 10)
    # 8 Visualisierungen (HF)
    s = deck.slide("Modern, Klinker, Glas-EG" + (" und Staffelgeschoss" if group == "A" else ", Vorbau auf Säulen"), foot)
    if not multi:
        deck.pic(s, hf("A", "persp"), 0.5, 1.2, w=6.1, h=3.9); deck.pic(s, hf("A", "aerial"), 6.7, 1.2, w=6.1, h=3.9)
        for i, (h_, b_) in enumerate((("Klinker", "dunkel, Langformat, passend zum Umfeld"), ("Oberstes Geschoss", "Holzbau, Terrasse rundum"), ("Balkone", "bodentiefe Fenster, Milchglas-Brüstungen"), ("Glas-EG", "Gastro mit Bar, Terrasse und Vordach"))):
            deck.text(s, 0.5 + i * 3.1, 5.3, 3.0, 0.3, h_, 13, BRICK, font="Georgia"); deck.text(s, 0.5 + i * 3.1, 5.65, 3.0, 0.7, b_, 10, GREY)
    else:
        for i, (k, v, r, d) in enumerate(O): deck.pic(s, neu(k, "hero"), 0.5 + i * 4.15, 1.3, w=4.0, h=2.45); deck.text(s, 0.5 + i * 4.15, 3.8, 4.0, 0.3, names[i], 13, BRICK, font="Georgia")
        for i, (k, v, r, d) in enumerate(O): deck.pic(s, neu(k, "detail"), 0.5 + i * 4.15, 4.2, w=4.0, h=2.45)
    deck.text(s, 0.5, 6.7, 12.3, 0.3, "KI-Visualisierungen (Nano Banana Pro auf Basis der Geometrie-Renderings) zur Orientierung; Fassadenteilung und Details folgen mit dem Architekten.", 9, GREY)
    if multi:
        s = deck.slide("Vorbau auf Säulen: überdachte Stellplätze und Dachterrasse", foot)
        for i, (k, v, r, d) in enumerate(O): deck.pic(s, neu(k, "east"), 0.5 + i * 4.15, 1.2, w=4.0, h=2.45); deck.text(s, 0.5 + i * 4.15, 3.7, 4.0, 0.3, names[i] + ": Ostseite, Stellplätze unter dem Vorbau", 10, GREY)
        deck.pic(s, neu(O[1][0], "roof"), 0.5, 4.2, w=4.0, h=2.3); deck.text(s, 0.5, 6.55, 4.0, 0.3, "B2: Dachterrasse 1,50 m", 10, GREY)
        deck.pic(s, neu(O[2][0], "roof"), 4.65, 4.2, w=4.0, h=2.3); deck.text(s, 4.65, 6.55, 4.0, 0.3, "B3: Dachterrasse 3,00 m", 10, GREY)
        deck.note(s, 8.8, 4.2, 4.0, 2.3, "B1:", "oberstes Geschoss bündig, keine Dachterrasse. B2 und B3 bekommen eine umlaufende Dachterrasse mit Milchglas-Brüstung; Holzfassade im Staffelgeschoss.", 10)
        deck.text(s, 0.5, 6.85, 12.3, 0.25, "KI-Visualisierungen im Stil der früheren Bilder; Details (Fenster, Brüstungen) folgen mit dem Architekten.", 8, GREY)
    # 9 Gastro
    s = deck.slide("Große Gastro mit Bar, neu und modern" if group == "A" else "Gastro im schmalen Erdgeschoss", foot)
    deck.pic(s, os.path.join(BILD, "gastro_1.jpg"), 0.5, 1.2, w=7.4, h=5.2); deck.pic(s, os.path.join(BILD, "gastro_2.jpg"), 8.1, 1.2, w=4.7, h=2.6)
    pi = [d["stp"]["sitze_innen"] for _, _, _, d in O]; pt = [d["stp"]["sitze_terrasse"] for _, _, _, d in O]
    deck.text(s, 8.1, 4.0, 4.7, 0.5, f"ca. {pi[0]} Plätze innen" if not multi else f"ca. {pi[0]} Plätze innen", 20, BRICK, font="Georgia")
    deck.text(s, 8.1, 4.6, 4.7, 1.8, [f"plus ca. {pt[0]} auf der Terrasse/Arkade (Annahme)", "Bar mit Barhockern, Polsterbänke, Backbar", "Material: Olivgrün, Cognac-Samt, Bordeaux, Eiche, schwarzer Stahl", "Stimmungsbilder aus dem früheren Gastro-Konzept (KI-Visualisierung)."], 11, GREY)
    # 10 Ansichten
    s = deck.slide("Ansichten aus dem Geometriemodell", foot); k1 = O[min(1, len(O) - 1)][0]
    for i, (n_, lab) in enumerate((("front", "Vorderansicht (Platzseite)"), ("rear", "Rückansicht"), ("west", "Westansicht"), ("east", "Ostansicht"))):
        deck.pic(s, img(k1, n_), 0.5 + (i % 2) * 6.2, 1.2 + (i // 2) * 2.9, w=6.0, h=2.5); deck.text(s, 0.5 + (i % 2) * 6.2, 3.65 + (i // 2) * 2.9, 6, 0.3, lab + (f" – {names[min(1, len(O)-1)]}" if multi else ""), 10, GREY)
    # 11 Stellplätze
    s = deck.slide("Stellplätze sind der Knackpunkt", foot)
    cd = CategoryChartData(); cd.categories = ["Bedarf Gastro/Büro (untere Spanne)", "Bedarf (obere Spanne)"] + [f"gezeichnet {n_}" for n_ in names]
    row = [round(r0["gesamt"] * 0 + O[0][3]["stp"]["erf_lo"], 1), round(O[0][3]["stp"]["erf_hi"], 1)] + [11 if k == "A" else 13 for k, *_ in O]
    cd.add_series("Stellplätze", row)
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(1.2), Inches(6.5), Inches(5.4), cd); ch = gf.chart; ch.has_legend = False; ch.plots[0].has_data_labels = True; ch.plots[0].series[0].format.fill.solid(); ch.plots[0].series[0].format.fill.fore_color.rgb = GREEN
    ch.category_axis.tick_labels.font.size = Pt(9); ch.value_axis.tick_labels.font.size = Pt(9)
    deck.text(s, 7.4, 1.2, 5.4, 0.4, "Vorschlag für die Stadt", 15, BRICK, font="Georgia")
    items = (["Gezeichnet sind 11 rückseitige Stellplätze (2,50 × 5,00 m), 10 davon teilweise überdacht; der Nachweis Gastro/Büro nach § 47 NBauO (Richtzahlen) liegt bei " + f"{num(O[0][3]['stp']['erf_lo'],1)}–{num(O[0][3]['stp']['erf_hi'],1)}.", "Wohnen braucht seit 01.07.2024 keine Pflichtstellplätze; optional 0,5–1,5 je Wohnung."] if group == "A" else
             ["Gezeichnet sind 13 Stellplätze auf der Hypothese 32 × 30 m: 8 voll unter dem Vorbau (Ostreihe, Säulenpaare 5,4 m) und 5 Längsparker; Zufahrt von Süden angenommen.", f"Nachweis Gastro/Büro nach Richtzahlen {num(O[0][3]['stp']['erf_lo'],1)}–{num(O[0][3]['stp']['erf_hi'],1)}; Wohnen seit 01.07.2024 ohne Pflicht, optional 0,5–1,5 je Wohnung.", "Offen: Sackgasse/Wendebedarf, Feuerwehrzufahrt unter dem Vorbau."])
    deck.bullets(s, 7.4, 1.7, 5.4, 3.3, items + ["Restplätze alternativ auf der öffentlichen Parkfläche per Vereinbarung oder Ablöse (Höhe nennt die Stadt)."], 11)
    deck.text(s, 7.4, 5.2, 5.4, 1.4, "Auf dem aus den Stadtplänen abgeleiteten Flurstück 59/1 (≈ 42,3 × 22,7 m) sind diese Stellplätze nicht unterzubringen; die Zahlen gelten nur auf der Hypothese.", 10, GREY)
    # 12 Flächen und Mieten
    s = deck.slide("Flächen und Mieten: Wohnungen, Büros und Gastro", foot)
    for oi, (k, v, r, d) in enumerate(O):
        m = d["mix"]["standard"]; areas = [("1. OG", a) for a in m["og1"]["vorn"] + m["og1"]["hinten"]] + [("oberstes Geschoss", a) for a in m["st"]["vorn"] + m["st"]["hinten"]]
        if oi > 0 and multi: continue
    rows = [["Einheit", "Geschoss", "Fläche", "Miete je m²", "Kaltmiete / Monat", "Kaltmiete / Jahr"]]
    k, v, r, d = O[-1] if multi else O[0]
    if multi:
        deck.text(s, 0.5, 1.15, 12.3, 0.3, "Kennwerte je Option (Wohnungen im Standardmix, Größen aus der Geometrie)", 11, GREY)
        rows = [["Position"] + names]
        rows += [["Wohnungen (Anzahl / Fläche)"] + cols(lambda k, v, r, d: f"{d['mix']['standard']['we']} / {num(v['wfl'])} m²"), ["Wohnungsgrößen min–max"] + cols(lambda k, v, r, d: f"{num(d['mix']['standard']['kleinste'])}–{num(d['mix']['standard']['groesste'])} m²"),
                 ["Kaltmiete Wohnen (11,18 €/m²) pro Jahr"] + cols(lambda k, v, r, d: eur(r["wohn"])), ["Büro netto (9,75 €/m²) pro Jahr"] + cols(lambda k, v, r, d: f"{num(v['buero_nf'],1)} m² / {eur(r['buero'])}"),
                 ["Gastro-Pacht (10 €/m²) pro Jahr"] + cols(lambda k, v, r, d: f"{num(v['gastro_nf'])} m² / {eur(r['pacht'])}"), ["Rohertrag gesamt pro Jahr"] + cols(lambda k, v, r, d: eur(r["roh"]))]
        deck.table(s, 0.5, 1.5, 12.3, [4] + [3] * 3, rows, 11, bold_rows=(6,), rowh=0.5)
    else:
        m = d["mix"]["standard"]; ar = [("1. OG", a) for a in m["og1"]["vorn"] + m["og1"]["hinten"]] + [("Staffel", a) for a in m["st"]["vorn"] + m["st"]["hinten"]]
        sc = v["wfl"] / sum(a for _, a in ar)
        for i, (g, a) in enumerate(ar, 1):
            a = a * sc; rows.append([f"WE {i}", g, f"{num(a,1)} m²", "11,18 €", eur(a * 11.18), eur(a * 11.18 * 12)])
        rows.append(["Summe Wohnen", "", f"{num(v['wfl'],1)} m²", "", eur(r["wohn"] / 12), eur(r["wohn"])]); rows.append(["Gastro (Pacht 10 €/m²)", "EG", f"{num(v['gastro_nf'],1)} m²", "10,00 €", eur(r["pacht"] / 12), eur(r["pacht"])]); rows.append(["Büros (2 Ankermieter)", "EG", f"{num(v['buero_nf'],1)} m²", "9,75 €", eur(r["buero"] / 12), eur(r["buero"])]); rows.append(["Rohertrag gesamt", "", "", "", eur(r["roh"] / 12), eur(r["roh"])])
        deck.table(s, 0.5, 1.2, 12.3, [3, 2, 2, 2, 3, 3], rows, 9, bold_rows=(len(ar) + 1, len(rows) - 1), rowh=0.26)
    # 13 Gewerbe
    s = deck.slide("Gewerbeflächen: Gastro und Büros im Erdgeschoss", foot)
    rows = [["Gastro-Flächenbedarf"] + [f"{n_}" for n_ in names]]
    rows += [["Gastraum (Plätze innen)"] + cols(lambda k, v, r, d: f"{d['stp']['sitze_innen']} Plätze / {num(d['stp']['gastro_m2'])} m²"), ["Gastro-Mietfläche gesamt (Gastraum, Bar, Küche, Lager, WC)"] + cols(lambda k, v, r, d: f"{num(v['gastro_nf'])} m²"), ["Terrasse / Arkade"] + cols(lambda k, v, r, d: f"{d['stp']['sitze_terrasse']} Plätze (Annahme)"), ["Büro netto"] + cols(lambda k, v, r, d: f"{num(v['buero_nf'],1)} m², Miete {eur(r['buero'])} / Jahr")]
    deck.table(s, 0.5, 1.3, 7.2, [4] + [2.5] * len(O), rows, 10, rowh=0.62, right_from=9)
    deck.note(s, 8.0, 1.3, 4.8, 3.6, "Gastro:", f"Pacht 10 €/m² und Monat; Umsatz in diesem Plan proportional zu den Innenplätzen (342 € je Platz und Monat wie im früheren Plan, 190 Plätze = 65.010 €). Das ist eine Annahme ohne Marktbeleg." + (" Das Büro (zwei Ankermieter) liegt im EG hinten statt im 1. OG." ))
    deck.text(s, 0.5, 5.2, 7.2, 1.0, "Das EG gehört der Gastro, Büros und Kern liegen rückseitig (Platzdaten aus dem Geometriemodell). Die Büros sind mit 9,50–10,00 €/m² und 10 Jahren Laufzeit angesetzt (Ankermieter, noch nicht vereinbart).", 10, GREY)
    # 14 KfW
    s = deck.slide("KfW-Kredite 298 und 299", foot)
    rows = [["Programm", "Wofür", "Rahmen (mit QNG)"] + [f"Im Projekt {n_}" if multi else "Im Projekt" for n_ in names] + ["Zins (Annahme)"]]
    rows += [["KfW 298 Klimafreundlicher Neubau", "vermietete Wohnungen", "bis 150.000 € je Wohnung"] + cols(lambda k, v, r, d: eur(r["kfw_w"])) + ["2,50 %"], ["KfW 299 Klimafreundlicher Neubau", "Gastro und Büros (Nichtwohngebäude)", "bis 2.000 € je m² Nettogrundfläche"] + cols(lambda k, v, r, d: eur(r["kfw_g"])) + ["3,00 %"], ["Hausbank (Rest)", "Restfinanzierung inkl. Bauzeitzinsen", "–"] + cols(lambda k, v, r, d: eur(r["bank"])) + ["4,00 %"]]
    deck.table(s, 0.5, 1.3, 12.3, [3, 3, 3] + [2] * len(O) + [1.5], rows, 10, rowh=0.55)
    deck.note(s, 0.5, 3.8, 12.3, 1.6, "Voraussetzungen:", "Effizienzhaus 40 (Gastro: Effizienzgebäude 40), QNG-Zertifikat für den vollen Rahmen, Heizung ohne Öl, Gas und Biomasse (z. B. Wärmepumpe), Energieeffizienz-Experte, Antrag vor Baubeginn über die Hausbank. Wohnteil (298) und Gastro/Büro (299) werden getrennt gefördert; die Kreditrahmen sind theoretische Obergrenzen (Nettogrundfläche = 85 % der Gewerbe-Nutzfläche).")
    deck.note(s, 0.5, 5.6, 12.3, 1.0, "Hinweis:", "KfW-Zinsen schwanken in den Quellen zwischen 0,6 % und 3,05 %; die Konditionen sind Stand Oktober 2026 nicht bestätigt. Mehrkosten für Effizienzhaus 40/QNG sind mit 3 % angesetzt.")
    # 15 Gesamtkosten
    s = deck.slide("Gesamtkosten", foot); labels = [p[0] for p in r0["posten"]]
    rows = [["Posten"] + names]
    for i, lab in enumerate(labels): rows.append([lab] + [eur(r["posten"][i][1]) for _, _, r, _ in O])
    rows.append(["Gesamtkosten"] + [eur(r["gesamt"]) for _, _, r, _ in O]); rows.append(["je m² BGF"] + [eur(r["gesamt"] / v["bgf"]) for _, v, r, _ in O])
    deck.table(s, 0.5, 1.2, 8.3 if not multi else 8.8, [4.5] + [2] * len(O), rows, 10, bold_rows=(len(labels) + 1,), rowh=0.42)
    cd = CategoryChartData(); k, v, r, d = O[min(1, len(O) - 1)]; cd.categories = ["Grundstück", "Bau (netto Holz)", "Nebenkosten + Standard", "Ausbau + Außenanlagen", "Finanzierung"]
    p_ = dict(r["posten"]); cd.add_series("Anteil", [p_["Grundstück inkl. Steuer und Notar"], p_["Bau, Massivbau"] + p_["Abschlag Holzbau (oberstes Geschoss)"] + p_["Dachterrassen (nicht in BGF)"], p_["Baunebenkosten"] + p_["Mehrkosten Effizienzhaus 40 und QNG"], p_["Ausbau Gastro und Büros"] + p_["Außenanlagen, Stellplätze (hypothetische Fläche)"], p_["Finanzierungskosten (Bauzeit, Bereitstellung, Anlaufzeit)"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(9.0), Inches(1.2), Inches(3.9), Inches(4.2), cd); ch = gf.chart; ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False; ch.legend.font.size = Pt(8)
    deck.text(s, 9.0, 5.4, 3.9, 0.3, f"Anteile {names[min(1, len(O)-1)]}", 9, GREY)
    deck.text(s, 0.5, 6.4, 12, 0.5, "Rechenregeln wie im früheren Plan: Bau 2.200 €/m² BGF, Holzbau-Abschlag 400 €/m², Terrassen 450 €/m², Nebenkosten 15 %, Effizienzhaus 40/QNG +3 %, Ausbau 1.000 €/Gastro-Platz und 150 €/m² Büro, Außenanlagen 160 €/m² auf der hypothetischen Restfläche.", 9, GREY)
    # 16 Finanzierungsplan
    s = deck.slide("Finanzierungsplan", foot)
    rows = [["Mittelherkunft"] + names + ["Zins"]]
    rows += [["KfW 298 (vermietete Wohnungen)"] + cols(lambda k, v, r, d: f"{eur(r['kfw_w'])} ({pct(r['kfw_w']/r['gesamt'])})") + ["2,50 %"], ["KfW 299 (Gastro und Büros)"] + cols(lambda k, v, r, d: f"{eur(r['kfw_g'])} ({pct(r['kfw_g']/r['gesamt'])})") + ["3,00 %"], ["Hausbank-Darlehen"] + cols(lambda k, v, r, d: f"{eur(r['bank'])} ({pct(r['bank']/r['gesamt'])})") + ["4,00 %"], ["Eigenkapital"] + ["–"] * len(O) + [""],
             ["Summe Finanzierung"] + cols(lambda k, v, r, d: eur(r["gesamt"])) + [""], ["Mischzins"] + cols(lambda k, v, r, d: pct(r["mischzins"], 2)) + [""], ["Rate pro Monat (Zins + 1 % Tilgung)"] + cols(lambda k, v, r, d: eur(r["rate_m"])) + [""]]
    deck.table(s, 0.5, 1.3, 12.3, [4] + [3] * len(O) + [1.2], rows, 10, bold_rows=(5,), rowh=0.5)
    deck.note(s, 0.5, 5.5, 12.3, 1.2, "Bau- und Anlaufzeit:", f"15 Monate Bau und 12 Monate Anlaufzeit kosten {' / '.join(eur(r['fin']) for _,_,r,_ in O)} an Zinsen und Bereitstellungsgebühr, finanziert von der Hausbank. Die Gesamtkosten sind komplett durch Fremdkapital gedeckt (kein Eigenkapital).")
    # 17 Zins & Rate
    s = deck.slide("Zinsberechnung und Rate je Darlehen", foot)
    for oi, (k, v, r, d) in enumerate(O):
        rows = [["Darlehen" + (f" {names[oi]}" if multi else ""), "Betrag", "Zins", "Tilgung", "Rate / Monat", "Rate / Jahr"]]
        for lab, (L, z, rm) in zip(("KfW Wohnen (298)", "KfW Gastro/Büro (299)", "Hausbank"), r["rate_je"]): rows.append([lab, eur(L), pct(z, 2), "1,00 %", eur(rm), eur(rm * 12)])
        rows.append(["Summe", eur(r["gesamt"]), pct(r["mischzins"], 2), "", eur(r["rate_m"]), eur(r["rate_j"])])
        deck.table(s, 0.5, 1.2 + oi * (1.7 if multi else 0), 12.3, [3, 2.5, 1.5, 1.5, 2.5, 2.5], rows, 10, bold_rows=(4,), rowh=0.32)
    deck.text(s, 0.5, 6.55 if multi else 3.2, 12.3, 0.6, f"Im ersten Jahr nach der Anlaufzeit: " + " / ".join(f"{eur(r['zins1'])} Zinsen und {eur(r['tilg1'])} Tilgung" for _, _, r, _ in O) + ".", 11)
    # 18 Abzahlungsplan
    s = deck.slide("Abzahlungsplan", foot)
    cd = CategoryChartData(); cd.categories = [str(y) for y in range(1, 36)]
    for (k, v, r, d), n_ in zip(O, names): cd.add_series(n_, [round(p[3]) for p in r["plan"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(0.5), Inches(1.2), Inches(7.2), Inches(5.0), cd); ch = gf.chart; ch.has_legend = multi
    if multi: ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
    ch.category_axis.tick_labels.font.size = Pt(8); ch.value_axis.tick_labels.font.size = Pt(8); ch.value_axis.tick_labels.number_format = '#,##0'; ch.value_axis.tick_labels.number_format_is_linked = False
    rows = [["Jahr", "Zinsen", "Tilgung", "Restschuld"]]; rp = O[min(1, len(O) - 1)][2]["plan"]
    for y in (1, 2, 3, 5, 10, 15, 20, 25, 30, 35): p = rp[y - 1]; rows.append([f"{y}" + (" (Ende Zinsbindung)" if y == 10 else ""), eur(p[1]), eur(p[2]), eur(p[3])])
    deck.table(s, 8.0, 1.3, 4.9, [2.5, 2, 2, 2.5], rows, 9, rowh=0.36); deck.text(s, 8.0, 5.4, 4.9, 0.6, f"Tabelle: {names[min(1, len(O)-1)]}.", 9, GREY)
    deck.text(s, 0.5, 6.3, 12.3, 0.6, "Nach 10 Jahren Zinsbindung beträgt die Restschuld " + " / ".join(eur(r["plan"][9][3]) for _, _, r, _ in O) + ". Die Anschlussfinanzierung muss eingeplant werden.", 11, bold=True)
    # 19 Ertrag und Kapitaldienst
    s = deck.slide("Ertrag und Kapitaldienst pro Monat", foot)
    rows = [["Position"] + [f"{n_} / Monat" for n_ in names]]
    rows += [["Kaltmiete Wohnen"] + cols(lambda k, v, r, d: eur(r["wohn"] / 12, True)), ["Büromieten (Ankermieter)"] + cols(lambda k, v, r, d: eur(r["buero"] / 12, True)), ["Pacht Gastro (10 €/m²)"] + cols(lambda k, v, r, d: eur(r["pacht"] / 12, True)),
             ["Rücklagen (10 % von Miete, Büro, Pacht)"] + cols(lambda k, v, r, d: eur(-r["rueck"] / 12)), ["Nettoertrag Immobilie"] + cols(lambda k, v, r, d: eur(r["netto_imm"] / 12, True)), ["Betriebsergebnis Gastro nach Pacht"] + cols(lambda k, v, r, d: eur(r["gastro_nach"] / 12, True)),
             ["Nettoertrag vor Kapitaldienst"] + cols(lambda k, v, r, d: eur(r["vor"] / 12, True)), ["Kapitaldienst (Zinsen und Tilgung)"] + cols(lambda k, v, r, d: eur(-r["rate_m"])), ["Ergebnis nach Kapitaldienst"] + cols(lambda k, v, r, d: eur(r["cash"] / 12, True))]
    fl = {(9, j): OKC if O[j - 1][2]["cash"] >= 0 else BADC for j in range(1, len(O) + 1)}
    deck.table(s, 0.5, 1.2, 8.4, [4] + [2.2] * len(O), rows, 10, bold_rows=(5, 7, 9), fills=fl, rowh=0.42)
    deck.note(s, 9.1, 1.2, 3.8, 3.9, "Kennzahlen:", "DSCR gesamt / nur Immobilie: " + " | ".join(f"{num(r['dscr_ges'],2)} / {num(r['dscr_imm'],2)}" for _, _, r, _ in O) + ". Zinsdeckung: " + " | ".join(num(r["zinsdeck"], 2) for _, _, r, _ in O) + ". Anfangsrendite (Immobilie): " + " | ".join(pct(r["rendite_imm"], 2) for _, _, r, _ in O) + ". Banken verlangen meist DSCR ≥ 1,2.", 10)
    deck.text(s, 0.5, 5.6, 12.3, 0.8, "Ohne den Gastro-Gewinn deckt die Immobilie allein die Raten nicht. Der Pachtvertrag mit einem tragfähigen Betreiber ist für die Bank entscheidend. Der Gastro-Umsatz ist proportional zu den Innenplätzen angesetzt (Annahme).", 11, GREEN, bold=True)
    # 20 Gastro-Umsatz Tagesteile
    s = deck.slide("Gastro-Umsatz: Hauptfokus Abend", foot); kk = O[0]; fac = kk[2]["umsatz"] / 65010.0
    teile = [("Frühstück werktags (Di–Fr 08:00–11:00)", 17, 30, 11), ("Brunch am Wochenende (Sa, So 09:00–14:00)", 9, 60, 14), ("Mittag: Bowls, Salate, Suppe (Di–Fr 11:30–14:30)", 17, 40, 13), ("Nachmittag: Kaffee, Kuchen, Snacks (Di–So 14:30–17:00)", 26, 20, 7),
             ("Bar mit Snacks Di–Do, So (ab 17:00)", 17, 35, 20), ("Bar Fr, Sa (bis 01:00)", 9, 90, 26), ("Events: Live-Musik, Feiern (4 pro Monat)", 4, 40, 40)]
    rows = [["Tagesteil", "Tage", "Gäste/Tag (skaliert)", "Ø Bon", "Umsatz/Monat", "Anteil"]]; tot = 0
    for n_, t_, g_, b_ in teile: u = t_ * g_ * b_ * fac; tot += u; rows.append([n_, str(t_), num(g_ * fac), f"{b_} €", eur(u), pct(t_ * g_ * b_ / 65010)])
    rows.append(["Gastro-Umsatz pro Monat", "", "", "", eur(tot), "100 %"])
    deck.table(s, 0.5, 1.2, 8.6, [5, 1, 1.8, 1, 2, 1.2], rows, 9, bold_rows=(8,), rowh=0.4)
    deck.note(s, 9.3, 1.2, 3.6, 3.2, "Annahme:", f"Aufbau und Bon-Werte wie im früheren Plan (190 Plätze, 65.010 €), alle Gästezahlen mit dem Faktor {num(fac,2)} auf {O[0][3]['stp']['sitze_innen']} Plätze skaliert. Das ist eine Rechenannahme, keine Prognose." + (" Für B gilt je Option derselbe Umsatz (gleiche Platzzahl)." if multi else ""), 10)
    deck.text(s, 9.3, 4.6, 3.6, 1.3, f"ca. {eur(tot*12/O[0][3]['stp']['sitze_innen'])} je Platz und Jahr (Branchen-Median Österreich ca. 12.000 €).", 10, GREY)
    # 21 Wie viel Umsatz braucht die Gastro
    s = deck.slide("Wie viel Umsatz braucht die Gastro?", foot)
    rows = [["Umsatz pro Monat", "Gewinn vor Pacht"] + [f"Gewinn nach Pacht {n_}" if multi else "Gewinn nach Pacht" for n_ in names]]; base = O[0][2]["umsatz"]
    for u in (25000, 30000, 40000, 50000, round(base), 65000):
        rows.append([eur(u), eur(u * P["marge"])] + [eur(u * P["marge"] - r["pacht"] / 12, True) for _, _, r, _ in O])
    fl = {(i, j): (OKC if rows[i][j].startswith("+") else BADC) for i in range(1, len(rows)) for j in range(2, len(rows[0]))}
    deck.table(s, 0.5, 1.2, 8.2, [2.5, 2.5] + [3] * len(O), rows, 10, fills=fl, rowh=0.45)
    be_pacht = [r["pacht"] / 12 / P["marge"] for _, _, r, _ in O]; be_haus = [(r["rate_j"] - r["netto_imm"]) / 12 / P["marge"] + r["pacht"] / 12 / P["marge"] * 0 for _, _, r, _ in O]
    be_haus = [max(((r["rate_j"] - r["netto_imm"]) / 12 + r["pacht"] / 12) / P["marge"], 0) for _, _, r, _ in O]
    deck.note(s, 8.9, 1.2, 4.0, 3.4, "Betrieb allein:", "Ab ca. " + " / ".join(eur(x) for x in be_pacht) + " Umsatz deckt der Betrieb seine Pacht.  Haus insgesamt: Ab ca. " + " / ".join(eur(x) for x in be_haus) + " Umsatz sind alle Raten bezahlt (Marge vor Pacht 30,5 %).", 10)
    deck.text(s, 0.5, 5.2, 12.3, 0.8, f"Plan-Umsatz {eur(base)} entspricht ca. {eur(base*12/O[0][3]['stp']['sitze_innen'])} je Sitzplatz und Jahr ({O[0][3]['stp']['sitze_innen']} Plätze).", 10, GREY)
    # 22 Ertragswert
    s = deck.slide("Ertragswert und Beleihung", foot)
    rows = [["Ertragswert"] + names, ["Rohertrag pro Jahr (Mieten und Pacht)"] + cols(lambda k, v, r, d: eur(r["roh"])), ["Bewirtschaftungskosten (13,75 %)"] + cols(lambda k, v, r, d: eur(-r["bew"])), ["Reinertrag"] + cols(lambda k, v, r, d: eur(r["rein"])), ["Bodenwert (960 m² × 230 €)"] + cols(lambda k, v, r, d: eur(r["boden"])),
            ["Gebäudeertragswert"] + cols(lambda k, v, r, d: eur(r["ew_geb"])), ["Ertragswert gesamt"] + cols(lambda k, v, r, d: eur(r["ew"]))]
    deck.table(s, 0.5, 1.2, 6.3, [3.2] + [1.8] * len(O), rows, 9, bold_rows=(6,), rowh=0.42)
    rows = [["Beleihung"] + names, ["Sachwert (Boden + Herstellungskosten)"] + cols(lambda k, v, r, d: eur(r["sach"])), ["Beleihungswert (niedrigerer Wert, −10 %)"] + cols(lambda k, v, r, d: eur(r["beleih"])), ["Gesamtkosten und Darlehen"] + cols(lambda k, v, r, d: eur(r["gesamt"])), ["Beleihungsauslauf"] + cols(lambda k, v, r, d: pct(r["auslauf"])), ["Ertragswert minus Gesamtkosten"] + cols(lambda k, v, r, d: eur(r["ew"] - r["gesamt"])), ["Betrag über 80 % Auslauf"] + cols(lambda k, v, r, d: eur(r["ueber80"]))]
    fl = {(4, j): BADC for j in range(1, len(O) + 1)}
    deck.table(s, 7.0, 1.2, 5.9, [3.2] + [1.8] * len(O), rows, 9, fills=fl, rowh=0.42)
    deck.note(s, 0.5, 4.8, 12.4, 1.7, "Einordnung:", "Die Mieten und die Pacht tragen einen Ertragswert von " + " / ".join(mio(r["ew"]) for _, _, r, _ in O) + ", die Kosten liegen bei " + " / ".join(mio(r["gesamt"]) for _, _, r, _ in O) + ". Eine Bank beleiht üblicherweise nur bis ca. 80 % des Beleihungswerts. Für die Finanzierung braucht es zusätzliche Sicherheiten (Grundschulden auf weitere Immobilien, Bürgschaft) oder Eigenkapital. Vereinfachte Wertermittlung, kein Gutachten (Liegenschaftszins Wohnen 3,85 %, Büro 5,35 %, Gastro 6,35 %, Restnutzungsdauer 60 Jahre).")
    # 23 Prognose & Belastungstest
    s = deck.slide("Prognose und Belastungstest", foot); g = 0.0153
    kp = O[min(1, len(O) - 1)]; rr = kp[2]
    rows = [["Jahr", "1", "3", "5", "7", "10"]]
    yrs = (1, 3, 5, 7, 10); vor = [rr["vor"] * (1 + g) ** (y - 1) for y in yrs]
    rows += [["Nettoertrag vor Kapitaldienst"] + [eur(x) for x in vor], ["Kapitaldienst"] + [eur(-rr["rate_j"])] * 5, ["Ergebnis nach Kapitaldienst"] + [eur(x - rr["rate_j"], True) for x in vor], ["DSCR"] + [num(x / rr["rate_j"], 2) for x in vor], ["Restschuld Jahresende"] + [eur(rr["plan"][y - 1][3]) for y in yrs]]
    deck.table(s, 0.5, 1.2, 12.3, [4, 2, 2, 2, 2, 2], rows, 9, bold_rows=(3,), rowh=0.34)
    deck.text(s, 0.5, 3.3, 12.3, 0.3, f"Prognose für {names[min(1, len(O)-1)]}, Ertragssteigerung 1,53 % p. a. (Annahme wie im früheren Plan)", 9, GREY)
    def stress(r, v):
        base = r["cash"] / 12; rj = r["rate_j"]; mz = r["mischzins"]
        sc = [("Plan", base), ("Anschlusszins nach 10 Jahren +1 Prozentpunkt (auf Restschuld)", base - r["plan"][9][3] * 0.01 / 12), ("Mieten Wohnen −10 %", base - r["wohn"] * 0.1 * 0.9 / 12), ("Gastro-Umsatz −20 %", base - r["gastro_vor"] * 0.2 / 12), ("Gastro-Umsatz −40 %", base - r["gastro_vor"] * 0.4 / 12),
              ("Baukosten +10 % (Kredit steigt entsprechend)", base - 0.1 * (r["gesamt"] - r["fin"]) * (mz + 0.01) / 12), ("Beide Büros leer", base - r["buero"] * 0.9 / 12), ("Gastro fällt ganz aus (keine Pacht, kein Betriebsergebnis)", ((r["wohn"] + r["buero"]) * 0.9 - rj) / 12)]
        return sc
    rows = [["Belastungstest (Ergebnis pro Monat)"] + names]; sts = [stress(r, v) for _, v, r, _ in O]
    for i in range(len(sts[0])): rows.append([sts[0][i][0]] + [eur(st[i][1], True) for st in sts])
    fl = {(i, j): (OKC if sts[j - 1][i - 1][1] >= 0 else BADC) for i in range(1, len(rows)) for j in range(1, len(O) + 1)}
    deck.table(s, 0.5, 3.7, 12.3, [6] + [2] * len(O) if not multi else [6, 2, 2, 2], rows, 9, fills=fl, rowh=0.33)
    # 24 Einfluss Gastro pro Person
    s = deck.slide("Einfluss der Gastro auf das Ergebnis pro Person", foot)
    r1 = O[min(1, len(O) - 1)][2]; names_ = names[min(1, len(O) - 1)]
    sc = [("Gastro fällt ganz aus (ohne Pacht)", ((r1["wohn"] + r1["buero"]) * 0.9 - r1["rate_j"]) / 12)] + [(f"Gastro-Umsatz {eur(u)}", (r1["netto_imm"] + u * 12 * P["marge"] - r1["pacht"] - r1["rate_j"]) / 12) for u in (20000, 30000, 40000, 50000)] + [(f"Plan: {eur(r1['umsatz'])}", r1["cash"] / 12)]
    rows = [["Gastro-Szenario", "Haus gesamt", "1 Person", "2 Personen", "4 Personen", "8 Personen"]]
    for n_, x in sc: rows.append([n_] + [eur(x / p_, True) for p_ in (1, 1, 2, 4, 8)])
    fl = {(i, j): (OKC if sc[i - 1][1] >= 0 else BADC) for i in range(1, len(rows)) for j in range(1, 6)}
    deck.table(s, 0.5, 1.2, 12.3, [4, 2, 2, 2, 2, 2], rows, 10, bold_rows=(len(rows) - 1,), fills=fl, rowh=0.45)
    deck.note(s, 0.5, 4.8, 12.3, 1.2, "Aussage:", f"Gerechnet für {names_}. Ohne Gastro-Gewinn fehlen {eur(-sc[0][1])} pro Monat, die Gastro macht also den Unterschied zwischen negativem und positivem Ergebnis.")
    # 25 Airbnb
    s = deck.slide("Prüfung: ein 60-m²-Apartment als Airbnb", foot)
    rows = [["Apartment 60 m²", "Werlte amtlich", "Emsland-Schnitt", "Optimistisch"], ["Auslastung", "17,4 %", "36,2 %", "60,0 %"], ["Preis pro Nacht", "90 €", "90 €", "90 €"], ["Netto Airbnb pro Monat", "210 €", "436 €", "723 €"], ["Netto langfristige Miete pro Monat (60 m² × 11,18 €)", "604 €", "604 €", "604 €"], ["Möblierung 36.000 € (Kapitaldienst pro Monat)", "−150 €", "−150 €", "−150 €"], ["Mehrertrag gegenüber langfristiger Miete pro Monat", "−544 €", "−318 €", "−31 €"]]
    deck.table(s, 0.5, 1.2, 12.3, [5, 2, 2, 2], rows, 11, rowh=0.5)
    deck.note(s, 0.5, 5.0, 12.3, 1.2, "Ergebnis:", "Airbnb lohnt sich in Werlte nicht. Erst ab ca. 63 % Auslastung wäre es so gut wie die langfristige Miete, in Werlte liegt sie amtlich bei 17 %. Die Wohnungen bleiben langfristig vermietet (Werte aus dem früheren Plan, unverändert).")
    # 26 Risiken
    s = deck.slide("Risiken und was wir dagegen tun", foot)
    ra = [r["auslauf"] for _, _, r, _ in O]
    items = [("Sicherheiten und Beleihung", f"Beleihungsauslauf {' / '.join(pct(x) for x in ra)} bei 100 % Fremdfinanzierung. Gegenmaßnahme: Grundschulden auf weitere Immobilien, Bürgschaft oder Eigenkapital, Pachtvertrag mit Bonitätsnachweis."),
             ("Gastro-Umsatz", f"Bei Ausfall der Gastro fehlen ca. {' / '.join(eur(-st[7][1] + st[0][1]) for st in sts)} pro Monat. Gegenmaßnahme: Konzept, erfahrener Betreiber, Pachtstaffel, Mietverträge über 10 Jahre mit Bonitätsprüfung."),
             ("Zins", "KfW-Zinsen und Rahmen sind Stand Oktober 2026 unsicher, nach 10 Jahren ist der Folgezins offen. Gegenmaßnahme: Zusage vor Baubeginn, Forward-Darlehen, Tilgungsaussetzung."),
             ("Genehmigung und Standard", "Baufenster, Dachform, Höhe und Geschosszahl sind mit der Stadt zu klären; KfW verlangt Effizienzhaus 40 mit QNG. Gegenmaßnahme: Vorabstimmung, Energieeffizienz-Experte früh einbinden."),
             ("Stellplätze" + (" und Statik" if group == "B" else ""), "Stellplätze nur auf der Hypothese nachgewiesen." + (" Kragarme bis 5,0 m über drei Geschosse und Feuerwehrzufahrt unter dem Vorbau sind statisch und brandschutztechnisch zu prüfen." if group == "B" else " Gegenmaßnahme: Vereinbarung über die öffentliche Parkfläche oder Ablöse."))]
    for i, (h_, b_) in enumerate(items): deck.note(s, 0.5 + (i % 2) * 6.2, 1.2 + (i // 2) * 1.85, 6.0, 1.7, h_ + ":", b_, 10)
    # 27 Was ich brauche
    s = deck.slide("Was ich von Stadt und Bank brauche", foot)
    rows = [["", "Anliegen"], ["Von der Stadt: Genehmigung", "Baufenster, Geschosse, Flachdach, Höhe und Höhenbezug schriftlich bestätigen"], ["Von der Stadt: Stellplätze", "Mitnutzung der öffentlichen Parkfläche oder faire Ablöse; Bestätigung der Stellplatzregelung"], ["Von der Stadt: Grundstück", "Kaufpreis 230 €/m² mit Baureife, Reservierung bis zur Finanzierungszusage; Zuschnitt und Baulinie zum Platz"],
            ["Von der Bank: Darlehen", "Finanzierung von " + " / ".join(mio(r["gesamt"]) for _, _, r, _ in O) + " mit KfW 298/299 und tilgungsfreier Anlaufzeit von 12 Monaten"], ["Von der Bank: Sicherheiten", "Gespräch über zusätzliche Grundschulden oder Bürgschaft wegen des Beleihungsauslaufs"], ["Von der Bank: KfW-Antrag", "Antrag für 298 und 299 vor Baubeginn über die Hausbank"]]
    deck.table(s, 0.5, 1.2, 12.3, [3.5, 9], rows, 11, rowh=0.7, right_from=9)
    # 28 Nächste Schritte
    s = deck.slide("Nächste Schritte", foot)
    for i, (d_, t_) in enumerate((("Okt 2026", "Gespräch mit der Stadt: Preis, Förderung, Stellplätze (Termin mit Herrn Keve bereits am 06.10. geführt, Folgetermin anfragen)"), ("Nov 2026", "Architekt, Baufenster, Höhen und Geschosse schriftlich klären"), ("Dez 2026", "Hausbank: Finanzierung, Anlaufzeit, KfW 298/299 und Sicherheiten klären"), ("Q1 2027", "Städtebaulicher Vertrag, Bauantrag, KfW-Antrag vor Baubeginn"), ("Mitte 2027", "Baubeginn, 15 Monate Bauzeit"), ("Ende 2028", "Eröffnung zusammen mit der neuen Mitte"))):
        deck.card(s, 0.5, 1.2 + i * 0.9, 12.3, 0.78); c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), Inches(1.33 + i * 0.9), Inches(0.5), Inches(0.5)); c.fill.solid(); c.fill.fore_color.rgb = BRICK; c.line.fill.background()
        deck.text(s, 0.7, 1.4 + i * 0.9, 0.5, 0.4, str(i + 1), 12, WHITE, bold=True, align=PP_ALIGN.CENTER); deck.text(s, 1.5, 1.3 + i * 0.9, 2.0, 0.5, d_, 13, INK, bold=True); deck.text(s, 3.5, 1.3 + i * 0.9, 9.2, 0.6, t_, 11, GREY)
    # 29 Anhang
    s = deck.slide(None, tag=False); bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)); bg.fill.solid(); bg.fill.fore_color.rgb = GREEN; bg.line.fill.background()
    deck.text(s, 0.8, 2.8, 11, 1, "Anhang", 40, WHITE, font="Georgia"); deck.text(s, 0.8, 3.9, 11, 0.6, "Annahmen, Gastro-Kosten, Gastro-Ausbau, Mietdaten", 16, WHITE)
    # 30 Rechenannahmen
    s = deck.slide("Rechenannahmen und offene Punkte", foot)
    deck.bullets(s, 0.5, 1.2, 12.3, 5.5, ["Grundstück 960 m² × 230 € plus ca. 7 % (5 % Grunderwerbsteuer, ca. 2 % Notar); Zuschnitt 32 × 30 m ist eine Hypothese.", "Bau BGF × 2.200 €, oberstes Geschoss in Holzbau 400 €/m² günstiger, Terrassen 450 €/m², Baunebenkosten 15 %, Effizienzhaus 40/QNG +3 %, Außenanlagen 160 €/m² auf der Restfläche (384 bzw. 420 m², Hypothese).",
        "100 % Fremdfinanzierung, 1 % Anfangstilgung, tilgungsfreie Anlaufzeit 12 Monate; Bauzeit 15 Monate, Bereitstellungszins 3 % p. a. ab Monat 7; Finanzierungskosten vereinfacht nachgerechnet (früherer Plan: 289.674 €, Nachrechnung 279.394 €, Abweichung 0,2 % der Gesamtkosten).",
        "Zins KfW 298 2,5 %, KfW 299 3,0 %, Hausbank 4,0 % (Annahmen); KfW 299 = 2.000 € × 85 % der Gewerbe-Nutzfläche; KfW 298 = 150.000 € je Wohnung.", "Wohnungen 11,18 €/m² Kaltmiete (früherer Planwert), Büro 9,75 €/m², Gastro-Pacht 10 €/m²; Rücklagen 10 % von Miete, Büro und Pacht; Lohn des Bauherrn nicht gerechnet.",
        "Gastro-Umsatz proportional zu den Innenplätzen (342 €/Platz und Monat, Marge vor Pacht 30,5 %) – keine Marktbelege; Steuersatz 35 % und AfA 3 % nur für die Pro-Kopf-Rechnung.", "Geometrie, Flächen und Wohnungen stammen aus dem Geometriemodell (A: B3-Stand v4; B: Entwurfsannahmen), Höhen bei B hypothetisch; Planungsrecht: B-Plan 2023 rechtskräftig, 1. Änderung nur Entwurf, Zuordnung Baufeld 3 unbestätigt.",
        "Offen: Baufenster, Dach, Höhen, Stellplatzsatzung, Zins nach 10 Jahren, Sicherheiten, Betreiber, Bodengutachten."], 11)
    # 31 Gastro Kosten
    s = deck.slide(f"Gastro: Kosten pro Monat bei {eur(O[0][2]['umsatz'])} Umsatz", foot); u = O[0][2]["umsatz"]; pach = O[0][1]["gastro_nf"] * P["pacht"]
    ant = [("Wareneinsatz (Einkauf Essen und Getränke)", "ca. 28 %", 0.28), ("Personal (ohne Chef-Lohn)", "ca. 30 %", 0.30), ("Energie, Wasser, Müll", "ca. 3 %", 0.03), ("Reinigung, Wäsche, Verbrauchsmaterial", "ca. 2 %", 0.02), ("Werbung und Marketing", "ca. 1,5 %", 0.015), ("Reparaturen, Wartung, Kassensystem", "ca. 1,5 %", 0.015), ("Sonstiges", "ca. 1,5 %", 0.015), ("Versicherungen, GEMA, Gebühren", "ca. 1 %", 0.01), ("Steuerberater, Buchhaltung", "ca. 1 %", 0.01)]
    rows = [["Posten", "Richtwert", "Betrag"]] + [[a, b, eur(u * c)] for a, b, c in ant[:2]] + [[f"Pacht ans Haus ({num(O[0][1]['gastro_nf'])} m² × 10 €)", "", eur(pach)]] + [[a, b, eur(u * c)] for a, b, c in ant[2:]]
    ksum = u * sum(c for *_, c in ant) + pach; rows += [["Summe Kosten", "", eur(ksum)], ["Gewinn nach Pacht, vor Lohn", "", eur(u - ksum)]]
    deck.table(s, 0.5, 1.2, 9.0, [5, 2, 2], rows, 10, bold_rows=(len(rows) - 2, len(rows) - 1), rowh=0.38); deck.text(s, 0.5, 6.4, 12, 0.6, "Die Richtwerte der Kostenquoten stammen aus dem früheren Plan; Marge hier ca. " + pct((u - ksum) / u + pach / u, 1) + " vor Pacht (Planwert 30,5 %, Rundung der Richtwerte).", 9, GREY)
    # 32 Gastro Ausbau
    s = deck.slide("Gastro-Ausbau nach Posten", foot); pl = O[0][3]["stp"]["sitze_innen"]; f_ = pl / 190
    base_ = [("Küche (Bowl- und Snackküche, Kühlräume, Spülküche)", 28000), ("Lüftung und Abluft", 23000), ("Theke und Bar (Zapfanlage, Kühlung, Backbar, große Theke)", 35000), (f"Möbel (ca. {pl} Plätze)", 36000), ("Beleuchtung und Deko", 10000), ("Wand, Boden, Decke, Akustik", 19000), ("Gäste-WC Ausstattung", 6000), ("Kasse, Technik, Musik, WLAN", 6000), ("Terrasse/Arkade (Holzdeck, Möbel, Heizstrahler)", 8000), ("Planung und Genehmigung", 6000), ("Eröffnung, Marketing, Warenerstbestückung", 4000)]
    rows = [["Posten", "Betrag (früherer Plan)"] + (["skaliert"] if True else [])] + [[a, eur(b), eur(b * f_)] for a, b in base_]
    sk = sum(b for _, b in base_) * f_; rows.append(["Puffer 5 %", eur(9050), eur(9050 * f_)]); rows.append(["Summe", eur(190050), eur(sk + 9050 * f_)])
    deck.table(s, 0.5, 1.2, 9.5, [5.5, 2, 2], rows, 10, bold_rows=(len(rows) - 1,), rowh=0.36)
    deck.text(s, 0.5, 6.2, 12, 0.7, f"Im Modell angesetzt: 1.000 € je Platz = {eur(pl*1000)} bei {pl} Plätzen. Die Posten sind aus dem früheren Plan proportional umgerechnet, kein Angebot.", 9, GREY)
    # 33 Mietdaten
    s = deck.slide("Mietdaten für Werlte", foot)
    rows = [["Quelle", "Wert für Werlte"], ["ImmoScout24 (Wohnungen, Durchschnitt)", "7,78 €/m²"], ["miete-aktuell.de (Kaltmiete 2026)", "8,13 €/m²"], ["mietpreise.info (14 Inserate, Spanne 6,09–14,48 €)", "9,58 €/m²"], ["mietpreise.info (Neubau)", "10,73–11,02 €/m²"], ["Landkreis Emsland (ImmoScout24, Q2 2026)", "8,10 €/m²"]]
    deck.table(s, 0.5, 1.2, 8.5, [5, 3], rows, 11, rowh=0.5)
    deck.note(s, 0.5, 4.5, 12.3, 1.3, "Im Modell:", "Wohnungen 11,18 €/m² Kaltmiete (Planwert des früheren Plans, zentrale Neubaulage). Büro 9,75 €/m² (9,50–10,00), Gastro-Pacht 10 €/m², ohne Marktdaten. Quellen: mietpreise.info/mietspiegel/werlte, miete-aktuell.de, immobilienscout24.de (Kreis Emsland), Abruf Oktober 2026.")
    out = os.path.join(HERE, f"Businessplan_Praesentation_{group}.pptx"); deck.save(out); return out, deck.n
if __name__ == "__main__":
    for g in ("A", "B"): print(build(g))
