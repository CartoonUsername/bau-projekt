import sys, os
sys.path.insert(0, "/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/einzel")
from einheiten import units, P
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
F="/usr/share/fonts/truetype/crosextra/"
for n,f in [("Cal","Caladea-Regular"),("Cal-B","Caladea-Bold"),("Cal-I","Caladea-Italic"),("Car","Carlito-Regular"),("Car-B","Carlito-Bold"),("Car-I","Carlito-Italic")]:
    pdfmetrics.registerFont(TTFont(n,F+f+".ttf"))
pdfmetrics.registerFontFamily("Car",normal="Car",bold="Car-B",italic="Car-I",boldItalic="Car-B")
pdfmetrics.registerFontFamily("Cal",normal="Cal",bold="Cal-B",italic="Cal-I",boldItalic="Cal-B")

R="/home/user/bau-projekt/praesentation/werlte_master/"
M="/tmp/claude-0/-home-user-bau-projekt/34dd8d0f-0f8e-569d-be22-0f852263e127/scratchpad/m/ppt/media/"
IMG=dict(hero=M+"image-10-1.jpg",corner=M+"image-8-1.jpg",terr=M+"image-10-3.jpg",g1=M+"image-9-1.jpg",g2=M+"image-10-4.jpg",g3=M+"image-10-5.jpg",skizze=M+"image-8-2.png",
         bplan=R+"quellen_stadt/amtliche_unterlagen_sgwerlte/Ausschnitt_MI3_Flurstueck_59-1_BPlan123_2023-01.png")

# ---------------- Rechenmodell ----------------
FIN=271065.9/4219771.8
def rechne(bau=1450.0, holz=700.0, dz=0.0, bnk=0.15, eh=0.03, umsatz=50000.0):
    p=dict(P); p.update(bau=bau,holz=holz,bnk=bnk,eh=eh,fin=0.0)
    p["z298"]+=dz; p["z299"]+=dz; p["zbank"]+=dz
    u,_=units(p); p["fin"]=FIN*sum(x["invest"] for x in u); u,_=units(p)
    for x in u:
        z=p["z299"] if x["typ"]=="Gastro" else p["z298"]
        x["zins"]=x["kfw"]*z+x["bank"]*p["zbank"]; x["tilg"]=x["kosten"]*0+x["kfw"]*p["til"]+x["bank"]*p["til"]
        x["plus"]=x["netto"]-x["zins"]-x["tilg"]; x["ruecklage"]=x["rent"]-x["netto"]
    return u
def eur(v,d=0): 
    s=f"{v:,.{d}f}".replace(",","X").replace(".",",").replace("X","."); return s
def f2(v): return f"{v:.2f}".replace(".",",")

# ---------------- Layout ----------------
NAVY=colors.HexColor("#1f3a4d"); GREY=colors.HexColor("#5b6670"); LIGHT=colors.HexColor("#eef2f5"); GREEN=colors.HexColor("#2e6b4a"); RED=colors.HexColor("#9b2c2c")
H1=ParagraphStyle("h1",fontName="Cal-B",fontSize=19,leading=23,textColor=NAVY,spaceAfter=6)
H2=ParagraphStyle("h2",fontName="Cal-B",fontSize=13,leading=16,textColor=NAVY,spaceBefore=8,spaceAfter=3)
B=ParagraphStyle("b",fontName="Car",fontSize=10,leading=13.2,textColor=colors.HexColor("#222222"),spaceAfter=3)
BS=ParagraphStyle("bs",parent=B,fontSize=8.5,leading=11,textColor=GREY)
BL=ParagraphStyle("bl",parent=B,leftIndent=10,bulletIndent=0)
CELL=ParagraphStyle("c",fontName="Car",fontSize=8.6,leading=10.5)
CELLB=ParagraphStyle("cb",parent=CELL,fontName="Car-B")
def P_(t,s=B): return Paragraph(t,s)
def bl(items): return [Paragraph(t,BL,bulletText="•") for t in items]
def tbl(rows,widths,head=True,align_right_from=1,zebra=True,fs=8.6,bold_last=False):
    data=[[Paragraph(str(c),CELLB if (head and i==0) else CELL) if isinstance(c,str) and not c.startswith("\0") else c for c in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=widths,repeatRows=1 if head else 0)
    st=[("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LINEBELOW",(0,0),(-1,-1),0.25,colors.HexColor("#c9d1d8")),("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5)]
    if head: st+=[("BACKGROUND",(0,0),(-1,0),LIGHT),("LINEBELOW",(0,0),(-1,0),0.8,NAVY)]
    if bold_last: st+=[("BACKGROUND",(0,len(rows)-1),(-1,len(rows)-1),LIGHT)]
    t.setStyle(TableStyle(st)); return t
def num(v,bold=False,color=None):
    s=ParagraphStyle("n",parent=CELLB if bold else CELL,alignment=2,textColor=color or colors.black); return Paragraph(v,s)
def img(path,w,maxh=None):
    from PIL import Image as PI
    iw,ih=PI.open(path).size; h=w*ih/iw
    if maxh and h>maxh: w=w*maxh/h; h=maxh
    return Image(path,width=w,height=h)
def cap(t): return Paragraph(t,ParagraphStyle("cap",parent=BS,fontName="Car-I",spaceAfter=6))

def footer(c,d):
    c.saveState(); c.setFont("Car",8); c.setFillColor(GREY)
    c.drawString(20*mm,10*mm,"Neue Mitte Werlte – Baufeld 3 · 8 Wohnungen + Gastro im EG · Entwurf Stand 07.11.2026 · alle Werte Annahmen, keine Zusage")
    c.drawRightString(190*mm,10*mm,f"Seite {d.page}"); c.restoreState()
doc=BaseDocTemplate("Neue-Mitte-Werlte_Baufeld3_Gesamtkonzept_Einzelrechnung_Stand-2026-11-07.pdf",pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=18*mm,
    title="Neue Mitte Werlte – Baufeld 3: Gesamtkonzept mit Einzelrechnung",author="Bessam Hasso")
doc.addPageTemplates([PageTemplate(id="p",frames=[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id="f")],onPage=footer)])
W=doc.width
S=[]

# ---------------- Rechnungen ----------------
Z=rechne(1450,700)          # Zielszenario
A=rechne(1800,700); Bm=rechne(1600,700); Cc=rechne(2200,400)
Zm=rechne(1450,700,-0.005); Zp=rechne(1450,700,+0.01)
we=[x for x in Z if x["typ"]=="WE"]; g=Z[-1]
def row(x): return x
tot=lambda L,k: sum(x[k] for x in L)

# ---------- Seite 1 Titel ----------
S+= [img(IMG["hero"],W), Spacer(1,8),
     P_("Neue Mitte Werlte – Baufeld 3",ParagraphStyle("t",parent=H1,fontSize=26,leading=30)),
     P_("8 Wohnungen und große Gastro im Erdgeschoss",ParagraphStyle("t2",parent=H2,fontSize=15,leading=19,textColor=GREY)),
     Spacer(1,6),
     P_("Gesamtkonzept mit Einzelrechnung je Wohnung und Gastro (Haus-GbR und Betreiber-UG getrennt), Erklärung von QNG und KfW-Förderung, Zinsumfeld und Einlagensicherung."),
     P_("Bauherr: Bessam Hasso · Stand 07.11.2026 · Entwurf zur Besprechung, nichts zugesichert. Bildmaterial sind Visualisierungen, keine Bauantragsunterlagen.",BS),
     P_("Keine Aussage zur baurechtlichen Zulässigkeit. Alle Preise, Zinsen und Umsätze sind ANNAHMEN und durch Angebote, Bank, KfW und Steuerberater zu belegen.",BS),
     PageBreak()]

# ---------- Seite 2 Projekt auf einen Blick ----------
S+= [P_("1. Das Projekt auf einen Blick",H1),
     P_("Ein Eckgebäude am Platz in der Neuen Mitte Werlte: unten eine große Gastronomie, darüber acht Mietwohnungen, das oberste Geschoss als zurückgesetztes Staffelgeschoss in Holzbau mit umlaufender schmaler Dachterrasse."),
     tbl([["Merkmal","Wert","Hinweis"],
          ["Grundstück","960 m² (Hypothese), Flurstück 59/1","Zuordnung Baufeld 3 = MI 3 noch nicht amtlich bestätigt"],
          ["Grundfläche Gebäude","540 m²","GRZ 0,6 erlaubt max. 576 m² (Gebäude)"],
          ["Erdgeschoss","Gastro 460 m² Nutzfläche","Rest: Treppenhaus, Aufzug, Wohn-Eingang"],
          ["1. Obergeschoss (Vollgeschoss)","5 Wohnungen je 83 m² = 415 m²","Massivbau"],
          ["Staffelgeschoss (kein Vollgeschoss)","3 Wohnungen je 103,3 m² = 310 m²","Holzbau, 0,8 m rundum zurückgesetzt"],
          ["Bruttogrundfläche gesamt","1.540 m²","540 + 540 + 460"],
          ["Wohnfläche gesamt","725 m²","8 Wohnungen, alle vermietet"]],
         [48*mm,52*mm,W-100*mm]),
     Spacer(1,6),
     img(IMG["corner"],W*0.8),
     cap("Außenansicht Eckgebäude, Platzseite (Visualisierung)"),
     PageBreak()]

# ---------- Seite 3 Bilder ----------
S+= [P_("2. Bilder",H1),
     Table([[img(IMG["hero"],W/2-3*mm),img(IMG["terr"],W/2-3*mm)],
            [cap("Platzseite mit Gastro im EG, Wohnungen im 1. OG, Staffelgeschoss mit Dachterrasse"),cap("Umlaufende schmale Dachterrasse am Staffelgeschoss (Holz)")]],colWidths=[W/2]*2),
     Table([[img(IMG["g1"],W/2-3*mm),img(IMG["g2"],W/2-3*mm)],[cap("Gastro innen: Fensterfront zum Platz"),cap("Gastro innen: Sitzbereich und Bar")]],colWidths=[W/2]*2),
     Table([[img(IMG["g3"],W/2-3*mm),img(IMG["skizze"],W/2-3*mm)],[cap("Gastro: Barbereich"),cap("Skizze der Geschosse: Staffelgeschoss, 1. OG, Gastro-EG")]],colWidths=[W/2]*2),
     P_("Die Grundrisse in den Planunterlagen stammen teils aus früheren Varianten (z. B. 12 Wohnungen) und sind hier nicht aufgenommen, bis sie auf den Plan mit 8 Wohnungen nachgezogen sind.",BS),
     PageBreak()]

# ---------- Seite 4 Baurecht ----------
S+= [P_("3. Baurecht in Kürze",H1),
     Table([[img(IMG["bplan"],W*0.5),
             [P_("Bebauungsplan Nr. 123 (Plan 2023, rechtskräftig), Gebiet MI 3:"),
              *bl(["Zwei bis drei Vollgeschosse (II–III)","GRZ 0,6, Traufhöhe 9,80 m, Gesamthöhe 15,00 m","Hauptdach mindestens 38° Neigung","Baugrenze 10 m zur Westseite, 3 m zu den übrigen Seiten","Höhenbezug: Oberkante Fahrbahn"]),
              P_("Die 1. Änderung des Plans (Entwurf) erfasst MI 3 nicht; dort gelten II zwingend, Traufhöhe 6,50 m und Gesamthöhe 12,00 m.",BS)]]],colWidths=[W*0.52,W*0.48]),
     P_("GRZ II (Stellplätze, Zufahrten, Nebenanlagen)",H2),
     P_("Nach §19 Abs. 4 BauNVO darf die zulässige Grundfläche durch Stellplätze, Zufahrten und Nebenanlagen bis zu 50 % überschritten werden, höchstens bis GRZ 0,8. Das Gebäude (GRZ I) bleibt bei 0,6. Wasserdurchlässige Beläge ändern nichts an der Berechnung, können aber für die Ausnahme bei geringfügigen Bodenauswirkungen (Satz 4 Nr. 1) relevant sein; das entscheidet die Stadt."),
     P_("Noch offen und am Montag, 09.11.2026, beim Bürgermeister zu klären: Zuordnung Baufeld 3 zu MI 3, Behandlung des Staffelgeschosses als Nicht-Vollgeschoss, Stellplatznachweis, GRZ-II-Ausnahme. Die vollständige Fragenliste liegt separat vor.",B),
     PageBreak()]

# ---------- Seite 5 GbR/UG ----------
S+= [P_("4. Aufbau: Haus-GbR/UG und Betreiber-UG",H1),
     P_("Das Gebäude wird als eigene Gesellschaft (GbR oder UG) geführt. Jede Wohnung und die Gastro-Fläche werden darin einzeln gerechnet, so als wären es eigene Objekte: eigene Kosten, eigene Finanzierung, eigene Miete."),
     tbl([["Gesellschaft","Einnahmen","Ausgaben","Ziel"],
          ["Haus-GbR/UG (Eigentümer)","Kaltmiete der 8 Wohnungen, Pacht von der Gastro","Zins und Tilgung, 10 % Rücklage (Verwaltung, Instandhaltung, Leerstand)","Jede Einheit trägt ihren Kapitaldienst selbst, mit leichtem Plus"],
          ["Betreiber-UG (Gastro-Betrieb)","Umsatz Restaurant und Bar","Wareneinsatz, Personal, Energie, Pacht an das Haus","Betriebsergebnis nach Pacht positiv, Pacht marktüblich"]],
         [38*mm,42*mm,55*mm,W-135*mm]),
     Spacer(1,4),
     P_("Aufteilung der Kosten auf die Einheiten (Annahme): nach Bruttogrundfläche. Der Kern im Erdgeschoss (Treppenhaus, Aufzug, Eingang, 80 m²) wird anteilig auf die Wohnungen umgelegt, das Grundstück nach Bruttogrundfläche, die Finanzierungskosten nach Investition."),
     P_("Umsatzsteuer",H2),
     *bl(["Wohnungen: Vermietung zu Wohnzwecken ist umsatzsteuerfrei (§4 Nr. 12 UStG), die 19 % Vorsteuer auf die Baukosten sind nicht abziehbar, die Baupreise werden brutto gerechnet.",
          "Gastro: Bei Pacht mit Umsatzsteuer (Option nach §9 UStG, Betreiber muss vorsteuerabzugsberechtigt sein) wären die Gastro-Baukosten netto zu rechnen, das wären bei den Zielwerten rund "+eur((g["invest"]-236256*460/1540)*0.19/1.19/1000)+" Tsd. € weniger. Das ist NICHT eingerechnet (Upside, Steuerberater klären).",
          "Gemeinsame Bauteile (Dach, Kern) sind nach Nutzung aufzuteilen, auch das klärt der Steuerberater."]),
     PageBreak()]

# ---------- Seite 6 QNG ----------
S+= [P_("5. QNG: Was bedeutet das?",H1),
     P_("<b>QNG = Qualitätssiegel Nachhaltiges Gebäude.</b> Es ist ein staatliches Siegel für Gebäude, die über die Energie hinaus bestimmte Nachhaltigkeitsanforderungen erfüllen. Es ist die Eintrittskarte für den höheren KfW-Kreditrahmen."),
     P_("Wofür brauchen wir es?",H2),
     *bl(["KfW 298 (Wohngebäude): Kreditrahmen 150.000 € je Wohneinheit mit QNG, ohne QNG 100.000 €.","KfW 299 (Nichtwohngebäude, Gastro): Kreditrahmen mit QNG bis 2.000 € je m² Nettogrundfläche, ohne QNG niedriger (Annahme 1.500 €/m²)."]),
     P_("Was wird nachgewiesen? (Überblick, Einzelwerte im aktuellen QNG-Handbuch prüfen)",H2),
     *bl(["Ökobilanz über den Lebenszyklus: Treibhausgas-Emissionen und nicht erneuerbarer Primärenergiebedarf bleiben unter festgelegten Grenzwerten.",
          "Schadstoffvermeidung: Baustoffe ohne bestimmte Schadstoffe, dokumentiert.",
          "Nachhaltige Materialgewinnung: zum Beispiel Holz aus zertifizierter Forstwirtschaft (FSC/PEFC).",
          "Zertifizierung durch eine dafür zugelassene Stelle; geprüft werden Planung und fertiges Gebäude."]),
     P_("Was bedeutet das praktisch?",H2),
     *bl(["Von Anfang an mit einem Energie- und Nachhaltigkeitsberater planen, nicht nachträglich.","Zusätzliche Kosten für Berater, Zertifizierung und Dokumentation: im Modell pauschal 3 % Mehrkosten für Effizienzhaus 40 und QNG, vom Architekten zu bestätigen.","Der Holzbau im Staffelgeschoss hilft bei der Ökobilanz (ANNAHME, rechnerisch nachzuweisen).","Ohne QNG sinkt der Kreditrahmen, und das Modell verliert bis zu 50.000 € günstiges Darlehen je Wohnung."]),
     P_("Quellen: Verbraucherzentrale, Interhyp, KfW-Programmseiten (Suchtreffer 07.11.2026); QNG-Grenzwerte im Volltext nicht geprüft.",BS),
     PageBreak()]

# ---------- Seite 7 KfW ----------
S+= [P_("6. KfW-Förderung: Was ist das und welche Bedingungen gelten?",H1),
     P_("Die KfW (staatliche Förderbank) vergibt zinsgünstige Kredite für klimafreundlichen Neubau. Der Antrag läuft über die Hausbank. Es gibt keinen Zuschuss, sondern einen Kredit mit verbessertem Zins."),
     tbl([["","KfW 298 Wohngebäude","KfW 299 Nichtwohngebäude"],
          ["Für uns","8 Wohnungen (Vermietung)","Gastro-Fläche im EG"],
          ["Standard","Effizienzhaus 40 (Klimafreundliches Wohngebäude)","Effizienzgebäude 40 (Klimafreundliches Nichtwohngebäude)"],
          ["Kreditrahmen mit QNG","150.000 € je Wohneinheit","bis 2.000 €/m² Nettogrundfläche, max. 10 Mio. €"],
          ["Ohne QNG","100.000 € je Wohneinheit","niedriger (Annahme 1.500 €/m²)"],
          ["Zins im Modell","2,5 % (10 Jahre fest, ANNAHME)","3,0 % (10 Jahre fest, ANNAHME)"],
          ["Im Modell abgerufen","8 × 150.000 € = 1.200.000 €","460 m² × 85 % × 2.000 € = 782.000 €"]],
         [34*mm,(W-34*mm)/2,(W-34*mm)/2]),
     P_("Bedingungen (aus Programmbeschreibungen, im aktuellen Merkblatt zu prüfen)",H2),
     *bl(["Antrag muss vor Beginn des Vorhabens bei der Hausbank gestellt werden, die Bank leitet ihn an die KfW weiter. Ein Baubeginn vor Antrag gefährdet die Förderung.",
          "Förderung gilt nach verfügbarem Budget, es gibt keinen Rechtsanspruch.",
          "Nachweis durch Energieeffizienz-Experten; mit QNG zusätzlich Zertifizierung. Heizung ohne fossile Brennstoffe (Programmvorgabe, prüfen).",
          "Zinsbindung 10 Jahre, danach Anschlusskonditionen. Die Zinsen schwanken: Quellen nennen zwischen 0,6 % und 3,05 %, das Modell rechnet vorsichtig mit 2,5 % / 3,0 %.",
          "Kombination mit den Programmen für das Niedrigpreissegment (296/596) ist für dieselbe Einheit ausgeschlossen.",
          "Die Bank prüft zusätzlich die Bonität und braucht Sicherheiten (Grundschuld auf das Grundstück). Der Rest der Finanzierung kommt von der Hausbank."]),
     P_("Weitere Förderung: Niedersachsen (NBank) fördert sozialen Wohnungsbau mit Mietbindung. Das ist hier NICHT eingerechnet, weil dann die Mieten gedeckelt wären; Wohnraumförderstelle Landkreis Emsland wäre zu fragen.",BS),
     PageBreak()]

# ---------- Seite 8 Zinsen / Einlagensicherung ----------
S+= [P_("7. Zinsen und Einlagensicherung",H1),
     P_("Einlagensicherung",H2),
     P_("Die Einlagensicherung schützt Sparer: Geld auf Konten bei einer Bank. Sie betrifft uns als Kreditnehmer nur indirekt, zum Beispiel bei der Frage, wo wir Eigenkapital, Mietkautionen und Rücklagen parken."),
     *bl(["Die gesetzliche Einlagensicherung (EU-weit) schützt 100.000 € je Kunde und Bank. Laut einer Quelle ist sie von der Reform der privaten Banken nicht betroffen.",
          "Die freiwillige Sicherung der privaten Banken wird laut Presse bis 2030 schrittweise gesenkt, auf höchstens 1 Mio. € je Institut; für Kommunen wurde sie gestrichen.",
          "Eine Änderung, die 2027 wirksam wird, konnte ich NICHT belegen. Ein PwC-Blog vom Mai 2026 nennt für eine EU-Reform der Einlagensicherungsrichtlinie den 11. Mai 2027 als Frist, die Quelle ist aber fragmentarisch. Bitte bei Bank oder Bundesverband deutscher Banken bestätigen lassen."]),
     P_("Konsequenz für uns: Größere Guthaben (Rücklagen, Kautionen) auf mehrere Banken verteilen oder bei einer Bank mit Institutssicherung (Sparkasse, Volksbank) halten. Das gilt unabhängig von der Reform.",B),
     P_("Zinsen",H2),
     *bl(["Das Modell rechnet mit 2,5 % KfW 298, 3,0 % KfW 299 und 4,0 % Hausbank bei 1 % Tilgung, alles 10 Jahre fest. Das ist eine Annahme, Stand Bauzinsen Sept./Okt. 2026.",
          "Dass die Zinsen weiter fallen, ist eine Erwartung und NICHT belegt. Deshalb rechnen wir Szenarien: Zins −0,5 Prozentpunkte und +1,0 Prozentpunkte (siehe Seite 12).",
          "Wichtig: Bei Baubeginn legen wir die Zinsbindung fest; fällt der Zins danach, hilft das erst bei der Anschlussfinanzierung."]),
     P_("Quellen: Börsen-Zeitung, mobiflip, PwC-Blog, Verbraucherzentrale (Suchtreffer 07.11.2026, ohne Volltextprüfung).",BS),
     PageBreak()]

# ---------- Seite 9 Annahmen ----------
S+= [P_("8. Annahmen der Rechnung",H1),
     P_("Die Rechnung wird in zwei Fassungen gezeigt: der bisherigen Basis (2.200 €/m² BGF) und dem <b>Zielwert (1.450 €/m² BGF)</b>, bei dem jede Einheit ein leichtes Plus erreicht. Der Zielwert ist keine Erwartung, sondern der Preis, den dein Netzwerk aus Bau, Maler und weiteren Gewerken erreichen muss."),
     tbl([["Posten","Basis","Zielwert","Hinweis"],
          ["Baukosten €/m² BGF (brutto)","2.200","1.450","Zielwert = ca. 1.885 €/m² Wohnfläche; Thüringen: veranschlagt 1.900–2.400 €/m² Wohnfläche"],
          ["Holzabschlag Staffelgeschoss €/m²","400","700","ANNAHME, Angebot der Zimmerei nötig"],
          ["Baunebenkosten","15 %","15 %","Ratgeber 15–20 %, daher nicht gesenkt"],
          ["Mehrkosten EH 40 + QNG","3 %","3 %","Quellen 3–8 %, unteres Ende"],
          ["Grundstück inkl. Nebenkosten","236.256 €","236.256 €","960 m² × 230 € + 5 % GrESt + 2 % Notar"],
          ["Gastro-Ausbau","150.000 €","150.000 €","für 460 m² knapp, Angebote nötig"],
          ["Finanzierungskosten","6,4 % der Investition","6,4 %","Bauzeit-Zinsen, Bereitstellung"],
          ["Kaltmiete Wohnen","11,18 €/m²","11,18 €/m²","Bauherr; Portale Neubau Werlte 10,7–11,0 €/m²"],
          ["Pacht Gastro","12 €/m²","12 €/m²","ANNAHME ohne Marktdaten"],
          ["Rücklage","10 %","10 %","Verwaltung, Instandhaltung, Leerstand"],
          ["Zinsen KfW 298 / 299 / Hausbank","2,5 / 3,0 / 4,0 %","2,5 / 3,0 / 4,0 %","1 % Tilgung, 10 Jahre fest"]],
         [52*mm,26*mm,26*mm,W-104*mm]),
     Spacer(1,4),
     P_("Nicht gerechnet: Einkommensteuer / Körperschaftsteuer, Abschreibung (AfA), Eigenleistung, Förderung durch das Land, Umsatzsteuer-Option Gastro. Eigenkapital: 0 €, 100 % Fremdfinanzierung."),
     PageBreak()]

# ---------- Seite 10 Einzelrechnung Wohnungen ----------
def r(v,b=False,c=None): return num(eur(v),b,c)
rows=[["Einheit","m²","Kosten gesamt €","KfW 298 €","Haus- bank €","Miete pro Jahr €","Rück- lage €","Zins €/J","Til- gung €/J","Plus €/J","Plus €/ Monat","DSCR"]]
for x in Z:
    if x["typ"]!="WE": continue
    rows.append([f"{x['name']} ({x['geschoss']})",num(eur(x["nf"],1)),r(x["kosten"]),r(x["kfw"]),r(x["bank"]),r(x["rent"]),r(x["ruecklage"]),r(x["zins"]),r(x["tilg"]),r(x["plus"],True,GREEN),r(x["plus"]/12,True,GREEN),num(f2(x["dscr"]),True)])
wsum=[x for x in Z if x["typ"]=="WE"]
rows.append(["Summe 8 WE",num(eur(sum(x["nf"] for x in wsum),1)),r(tot(wsum,"kosten")),r(tot(wsum,"kfw")),r(tot(wsum,"bank")),r(tot(wsum,"rent")),r(tot(wsum,"ruecklage")),r(tot(wsum,"zins")),r(tot(wsum,"tilg")),r(tot(wsum,"plus"),True,GREEN),r(tot(wsum,"plus")/12,True,GREEN),num(f2(tot(wsum,"netto")/(tot(wsum,"zins")+tot(wsum,"tilg"))),True)])
cw=[19*mm,12*mm,17*mm,17*mm,14*mm,14*mm,12*mm,13*mm,13*mm,16*mm,14*mm,13*mm]
sc=W/sum(cw); cw=[c*sc for c in cw]
S+= [P_("9. Einzelrechnung je Wohnung (Zielwerte, 1. Jahr)",H1),
     P_("Jede Wohnung wird wie ein eigenes Objekt gerechnet. <b>Plus</b> = Netto-Miete (nach 10 % Rücklage) minus Zins minus 1 % Tilgung, ohne Eigenkapital. <b>DSCR</b> = Netto-Miete ÷ (Zins + Tilgung); über 1,0 trägt sich die Einheit selbst.",B),
     tbl(rows,cw,bold_last=True),
     Spacer(1,5),
     P_("Wie die Zahl entsteht (Beispiel WE 1, 1. OG)",H2),
     P_(f"Gesamtkosten {eur(Z[0]['kosten'])} € bestehen aus Bau ({eur(1450*Z[0]['bgf'])} €), Baunebenkosten 15 %, EH-40-/QNG-Mehrkosten 3 %, Grundstücksanteil und Finanzierungskosten. Davon übernimmt die KfW 150.000 € zu 2,5 %, die Hausbank den Rest zu 4,0 %. Die Miete beträgt {eur(Z[0]['rent'])} € im Jahr, nach Rücklage bleiben {eur(Z[0]['netto'])} €."),
     P_("Die Wohnungen im 1. OG sind knapper als die Staffel, weil sie in Massivbau gebaut werden und jede ihren Anteil am Kern im EG trägt. Die Staffel-Wohnungen profitieren vom Holzabschlag und von größeren Flächen.",B),
     P_("Ergebnis: Jede Wohnung hat ein leichtes Plus ohne Eigenkapital, wenn der Zielpreis erreicht wird. Die Wohnungen im 1. OG sind der Engpass.",B),
     PageBreak()]

# ---------- Seite 11 Gastro ----------
gr=g
S+= [P_("10. Gastro: Haus-Sicht und Betrieb",H1),
     P_("Haus-GbR/UG: Pacht und Kapitaldienst der Gastro-Fläche",H2),
     tbl([["Posten","€ pro Jahr","€ pro Monat"],
          ["Gesamtkosten Gastro-Fläche (inkl. Ausbau 150.000 €)",eur(gr["kosten"]),""],
          ["davon KfW 299 (460 m² × 85 % × 2.000 € = 782.000 €)",eur(gr["kfw"]),""],
          ["davon Hausbank",eur(gr["bank"]),""],
          ["Pacht 460 m² × 12 €/m²",eur(gr["rent"]),eur(gr["rent"]/12)],
          ["− Rücklage 10 %",eur(-gr["ruecklage"]),eur(-gr["ruecklage"]/12)],
          ["= Netto-Pacht",eur(gr["netto"]),eur(gr["netto"]/12)],
          ["− Zins",eur(-gr["zins"]),eur(-gr["zins"]/12)],
          ["− Tilgung 1 %",eur(-gr["tilg"]),eur(-gr["tilg"]/12)],
          [f"<b>= Plus Haus (DSCR {f2(gr['dscr'])})</b>",f"<b>{eur(gr['plus'])}</b>",f"<b>{eur(gr['plus']/12)}</b>"]],
         [W-60*mm,30*mm,30*mm],bold_last=True),
     P_("Betreiber-UG: Umsatz, Kosten, Gewinn (Branchenrichtwerte, keine Werte aus Werlte)",H2),
     tbl([["Posten","Anteil","€ pro Monat"],
          ["Umsatz (netto)","100 %","50.000"],
          ["Wareneinsatz","28 %","−14.000"],["Personal (ohne Lohn des Bauherrn)","30 %","−15.000"],
          ["Energie, Wasser, Müll","3 %","−1.500"],["Reinigung, Verbrauchsmaterial","2 %","−1.000"],
          ["Werbung, Reparaturen, Sonstiges","4,5 %","−2.250"],["Versicherung, GEMA, Steuerberater","2 %","−1.000"],
          ["<b>Gewinn vor Pacht</b>","30,5 %","<b>15.250</b>"],
          ["Pacht an das Haus",f"{gr['rent']/12/500:.1f} %".replace(".",","),eur(-gr["rent"]/12)],
          ["<b>Betriebsergebnis nach Pacht</b>","","<b>"+eur(15250-gr["rent"]/12)+"</b>"]],
         [W-60*mm,30*mm,30*mm],bold_last=True),
     Spacer(1,4),
     tbl([["Umsatz €/Monat","30.000","40.000","50.000","60.000","70.000"],
          ["Gewinn nach Pacht €/Monat","3.630","6.680","9.730","12.780","15.830"]],[W-5*22*mm]+[22*mm]*5),
     P_("Break-even-Umsatz des Betriebs: etwa 18.100 € pro Monat. Der Lohn des Bauherrn und Steuern sind nicht gerechnet. Bei niedrigem Umsatz sind Fixkosten stärker, die Tabelle ist dort zu günstig.",BS),
     PageBreak()]

# ---------- Seite 12 Gesamt + Szenarien ----------
def dsc(L,i): return f2(L[i]["dscr"])
def pl(L,i): return eur(L[i]["plus"]/12)
S+= [P_("11. Gesamtübersicht und Szenarien",H1),
     P_("Haus-GbR/UG gesamt (Zielwerte)",H2),
     tbl([["Posten","€ pro Jahr","€ pro Monat"],
          ["Mieten 8 Wohnungen",eur(tot(wsum,"rent")),eur(tot(wsum,"rent")/12)],
          ["Pacht Gastro",eur(g["rent"]),eur(g["rent"]/12)],
          ["Rohertrag",eur(tot(Z,"rent")),eur(tot(Z,"rent")/12)],
          ["− Rücklage 10 %",eur(-tot(Z,"ruecklage")),eur(-tot(Z,"ruecklage")/12)],
          ["− Zins",eur(-tot(Z,"zins")),eur(-tot(Z,"zins")/12)],
          ["− Tilgung 1 %",eur(-tot(Z,"tilg")),eur(-tot(Z,"tilg")/12)],
          [f"<b>= Plus Haus gesamt (DSCR {f2(tot(Z,'netto')/(tot(Z,'zins')+tot(Z,'tilg')))})</b>",f"<b>{eur(tot(Z,'plus'))}</b>",f"<b>{eur(tot(Z,'plus')/12)}</b>"]],
         [W-60*mm,30*mm,30*mm],bold_last=True),
     P_(f"Gesamtkosten: {eur(tot(Z,'kosten'))} € (Basis 2.200 €/m²: {eur(tot(Cc,'kosten'))} €). Darlehen: KfW {eur(tot(Z,'kfw'))} €, Hausbank {eur(tot(Z,'bank'))} €. Eigenkapital: 0 €. Zusätzlich der Betrieb der Gastro-UG: {eur(15250-g['rent']/12)} € pro Monat vor Lohn des Bauherrn und Steuern.",B),
     P_("Wie reagiert das Plus auf Preise und Zinsen?",H2)]
hdr=["Szenario","Gesamt-kosten €","WE 1–5 DSCR","WE 6–8 DSCR","Gastro DSCR","Plus Haus €/Mon."]
def line(name,L): return [name,num(eur(tot(L,'kosten'))),num(dsc(L,0)),num(dsc(L,5)),num(dsc(L,8)),num(eur(tot(L,'plus')/12))]
S+= [tbl([hdr,line("Basis 2.200 €/m², Holz −400",Cc),line("1.800 €/m², Holz −700",A),line("1.600 €/m², Holz −700",Bm),line("<b>Zielwert 1.450 €/m², Holz −700</b>",Z),
          line("Ziel, Zins −0,5 Prozentpunkte",Zm),line("Ziel, Zins +1,0 Prozentpunkte",Zp)],
         [48*mm,26*mm,22*mm,22*mm,22*mm,W-140*mm]),
     Spacer(1,4),
     P_("Lesehilfe: DSCR unter 1,0 = die Einheit muss zugezahlt werden, über 1,0 = sie trägt sich selbst. Bei 1.800 €/m² reicht es für Staffel und Gastro, aber nicht für das 1. OG; dafür bräuchte es dann Eigenkapital oder Preise nahe dem Zielwert. Bei Zins +1 Punkt wird das Plus der Wohnungen im 1. OG negativ, dort ist der Puffer klein.",B),
     PageBreak()]

# ---------- Seite 13 Risiken ----------
S+= [P_("12. Offene Punkte, Risiken, nächste Schritte",H1),
     P_("Was noch belegt werden muss",H2),
     *bl(["Baupreis: Angebote für Rohbau, Zimmerei (Staffel), Ausbau, Maler und weitere Gewerke; erst dann ist der Zielwert von 1.450 €/m² belastbar.",
          "KfW: Zins, Kreditrahmen, Bedingungen mit Hausbank und Energieberater; Antrag vor Baubeginn.",
          "QNG: Berater beauftragen, Kosten und machbare Zertifizierungsstufe klären.",
          "Steuer: Umsatzsteuer-Option für Gastro, Aufteilung gemeinsamer Bauteile, Abschreibung; mit Steuerberater.",
          "Baurecht: Zuordnung MI 3, Staffelgeschoss als Nicht-Vollgeschoss, Stellplätze, GRZ II (Termin Bürgermeister 09.11.2026).",
          "Gastro: Betreiber, Pachtvertrag, Pachthöhe (12 €/m² ist Annahme), Umsatz 50.000 €/Monat (Bauherrenvorgabe) und Konzept.",
          "Zinsen und Einlagensicherung: Erwartungen (fallende Zinsen, Änderung 2027) sind nicht belegt; Szenarien statt Annahmen."]),
     P_("Hauptrisiken",H2),
     *bl(["Das Plus der Wohnungen im 1. OG ist klein: Baupreise 3–5 % höher oder Zinsen 1 Punkt höher drehen es ins Minus.",
          "Die Gastro-Pacht hängt am Betreiber; fällt er aus, fehlen 66.240 € Pacht im Jahr.",
          "Förderung ist budgetabhängig, keine Zusage."]),
     P_("Empfehlung",H2),
     P_("Zuerst die Baupreise per Angebot belegen, dann KfW-Konditionen mit der Hausbank und die Steuerfragen klären, bevor Verträge unterschrieben oder Aufträge vergeben werden. Alle Zahlen in diesem Dokument sind ein Rechenstand und keine Zusage."),
     P_("Rechenmodell: Einzelrechnung_Einheiten_Ziel1800.xlsx (mit Formeln) und einheiten.py im Projektordner; die Excel wird für die Zielwerte 1.450 €/m² noch angepasst.",BS)]
doc.build(S)
print("ok")
