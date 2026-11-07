import sys
sys.path.insert(0,"/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/einzel")
from model import model, sens
from einheiten import units, P as UP
from lib import eur, num, pct, f2
from ui import *
OUT="/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/deck/Neue-Mitte-Werlte_Baufeld3_Bankpraesentation_2026-11.pptx"
IM="/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/deck/bilder/"
def unitcalc(**kw):
    m=model(**kw); p=dict(UP); p.update(bau=kw.get("bau",2200.0),holz=kw.get("holz",400.0),fin=m["fin"],z298=m["z298"],z299=m["z299"],zbank=m["zb"],bnk=m["bnk"],eh=m["eh"])
    u,_=units(p)
    for x in u:
        z=p["z299"] if x["typ"]=="Gastro" else p["z298"]
        x["zins"]=x["kfw"]*z+x["bank"]*p["zbank"]; x["tilg"]=(x["kfw"]+x["bank"])*p["til"]; x["plus"]=x["netto"]-x["zins"]-x["tilg"]
    return m,u
Z,UZ=unitcalc(bau=1450,holz=700); B=model()
we15,we68,gas=UZ[0],UZ[5],UZ[8]; haus_plus=(Z["netto_imm"]-Z["kd_j"])/12; h=Z["tilg"]; ss=sens(Z)
d=Deck(); mio=lambda v: num(v/1e6,2)+" Mio. €"
SEC=["1 · Das Projekt","2 · Baurecht","3 · Förderung und Zinsen","4 · Rechnung","5 · Risiken und nächste Schritte","Anhang"]
# 1 Titel
sl=d.blank(CREAM); rect(sl,-1.5,-1.5,5.0,5.0,SAGE,shape=MSO_SHAPE.OVAL); rect(sl,3.2,5.6,3.4,3.4,BLUSH,shape=MSO_SHAPE.OVAL); img(sl,IM+"hero.jpg",6.6,0.6,6.1,6.3)
tx(sl,0.8,0.9,5,0.3,"NEUE MITTE WERLTE",size=12,color=GOLD,bold=True)
tx(sl,0.8,2.0,5.4,2.4,"Baufeld 3: Acht Wohnungen und eine große Gastro",size=38,color=INK,font=HF,line=0.95)
tx(sl,0.8,4.5,5.1,0.9,"Bankpräsentation: Konzept, Förderung, Kosten, Ertrag und Abzahlung",size=16,color=GREY)
tx(sl,0.8,6.2,5.1,0.8,["Bessam Hasso, Werlte","Bebauungsplan Nr. 123 (Plan 2023, rechtskräftig)","Stand November 2026, Entwurf, alle Werte Annahmen"],size=11,color=GREY,space=2)
# 2 Inhalt
sl=page(d,"Überblick","Fünf Fragen, fünf Kapitel")
items=[("1","Was wird gebaut?","Haus, Gastro, Wohnungen, Bilder"),("2","Was sagt die Stadt?","Bebauungsplan, Stellplätze, offene Fragen"),("3","Welche Förderung gibt es?","KfW, QNG, Zinsen, Einlagensicherung"),("4","Was kostet es, und trägt es sich?","Kosten, Finanzierung, Ertrag, Gewinn je Einheit"),("5","Was kann schiefgehen, wie geht es weiter?","Risiken, Bedarf an Stadt und Bank, Termine")]
for i,(n,q,s_) in enumerate(items):
    y=1.95+i*0.95; tx(sl,0.9,y,0.7,0.7,n,size=34,color=GOLD,font=HF); tx(sl,1.8,y+0.02,10,0.4,q,size=20,color=GREEN,font=HF); tx(sl,1.8,y+0.42,10,0.3,s_,size=13,color=GREY)
# 3
sl=page(d,SEC[0],"Acht Wohnungen über einer großen Gastro am neuen Marktplatz")
kpi(sl,0.7,2.0,2.9,"8 Wohnungen","725 m² Wohnfläche, alle vermietet")
kpi(sl,3.9,2.0,2.9,"460 m² Gastro","ca. 150 Plätze, ganzes Erdgeschoss",TERRA)
kpi(sl,0.7,3.5,2.9,"1.540 m² BGF","EG, 1. OG und Staffelgeschoss")
kpi(sl,3.9,3.5,2.9,"960 m²","Grundstück, davon 540 m² bebaut (GRZ 0,6 = max. 576 m²)",GREY)
tx(sl,0.7,5.1,6.2,1.4,["Unten die Gastro für den ganzen Tag, darüber fünf Wohnungen im 1. OG und drei Penthouse-Wohnungen im Staffelgeschoss aus Holz."],size=15)
img(sl,IM+"ecke.jpg",7.3,1.95,5.33,4.4); tx(sl,7.3,6.4,5.3,0.25,"Visualisierung, Eckansicht",size=9,color=GREY)
# 4
sl=page(d,SEC[0],"So soll das Haus aussehen: Klinker, bodentiefe Fenster, Holz oben")
img(sl,IM+"hero.jpg",0.7,1.9,7.4,4.4); img(sl,IM+"terrasse.jpg",8.35,1.9,4.28,4.4)
tx(sl,0.7,6.38,7.4,0.3,"Platzseite mit Glas-EG für die Gastro",size=10,color=GREY); tx(sl,8.35,6.38,4.3,0.3,"Dachterrasse am Staffelgeschoss",size=10,color=GREY)
tx(sl,0.7,6.68,12,0.25,"KI-Visualisierungen zur Orientierung; Fassade und Maße folgen mit dem Architekten.",size=9,color=GREY)
# 5
sl=page(d,SEC[0],"Drei Geschosse: Gastro unten, Wohnen darüber")
rect(sl,0.9,4.7,5.2,1.3,"E7D9A8"); tx(sl,0.9,4.7,5.2,1.3,["Erdgeschoss","Gastro mit Bar"],size=15,color=INK,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
rect(sl,0.9,3.4,5.2,1.3,TERRA); tx(sl,0.9,3.4,5.2,1.3,["1. Obergeschoss","5 Wohnungen"],size=15,color=WHITE,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
rect(sl,1.2,2.2,4.6,1.2,"7A5A3A"); tx(sl,1.2,2.2,4.6,1.2,["Staffelgeschoss (Holz)","3 Wohnungen"],size=15,color=WHITE,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
rect(sl,0.7,6.0,5.6,0.05,GREY)
table(sl,6.9,2.2,5.7,[["Ebene","Nutzung","BGF"],["Staffel","3 Wohnungen à ca. 103 m²","460 m²"],["1. OG","5 Wohnungen à 83 m²","540 m²"],["EG","Gastro 460 m², Treppenhaus, Aufzug","540 m²"],["Summe","8 Wohnungen, 1 Gastro","1.540 m²"]],[1,3.2,1.2],size=13,rh=0.5,total=(4,),align=["l","l","r"])
tx(sl,6.9,5.0,5.7,1.2,["BGF = Bruttogrundfläche, alle Geschosse zusammen.","Das Staffelgeschoss springt rundum 0,8 m zurück, so entsteht eine schmale Terrasse (ca. 72 m²). Höhen sind Annahmen."],size=12,color=GREY)
# 6 Skizzen
sl=page(d,SEC[0],"So sind die Geschosse aufgeteilt")
cols=[("Erdgeschoss",0.7),("1. Obergeschoss",4.85),("Staffelgeschoss",9.0)]
for t,x in cols: tx(sl,x,1.95,3.9,0.3,t,size=14,color=GREEN,bold=True)
rect(sl,0.7,2.4,3.9,2.6,LIGHT,LINE); rect(sl,0.7,2.4,0.55,2.6,"BFC5C2"); tx(sl,0.7,2.4,0.55,2.6,"Treppe Aufzug",size=8,color=INK,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
rect(sl,1.3,2.5,3.2,1.25,"E7D9A8"); tx(sl,1.3,2.5,3.2,1.25,["Gastraum und Lounge","ca. 130 Plätze"],size=11,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
for xx,tt in ((1.3,"Séparée 20"),(2.45,"Bar"),(3.4,"Küche, WC")): rect(sl,xx,3.85,1.05 if tt!="Küche, WC" else 1.1,1.05,"EFE6C8"); tx(sl,xx,3.85,1.05,1.05,tt,size=10,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
rect(sl,4.85,2.4,3.9,2.6,LIGHT,LINE); rect(sl,4.85,2.4,0.55,2.6,"BFC5C2"); tx(sl,4.85,2.4,0.55,2.6,"Treppe Aufzug",size=8,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
w5=(3.9-0.6)/5
for i in range(5): rect(sl,5.45+i*w5,2.5,w5-0.04,2.4,"D9A79A"); tx(sl,5.45+i*w5,2.5,w5-0.04,2.4,[f"WE {i+1}","83 m²"],size=10,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
rect(sl,9.0,2.4,3.63,2.6,LIGHT,LINE); w3=(3.63-0.2)/3
for i in range(3): rect(sl,9.1+i*w3,2.5,w3-0.05,2.4,"CDB28F"); tx(sl,9.1+i*w3,2.5,w3-0.05,2.4,[f"WE {6+i}","103 m²"],size=10,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
tx(sl,0.7,5.3,11.9,1.2,["Treppenhaus und Aufzug liegen am Westende und erschließen die Wohnungen getrennt von der Gastro.","Schematische Skizze, keine Bauzeichnung; Aufteilung der Gastro nach Gastro-Konzept."],size=13,color=GREY)
# 7 Gastro
sl=page(d,SEC[0],"Die Gastro: ein Bar-Restaurant für den ganzen Tag")
img(sl,IM+"gastro1.jpg",0.7,1.9,4.0,2.5); img(sl,IM+"gastro2.jpg",4.85,1.9,4.0,2.5); img(sl,IM+"gastro3.jpg",9.0,1.9,3.63,2.5)
kpi(sl,0.7,4.75,2.9,"150 Plätze","innen (130 Gastraum, 20 Séparée)",vs=30); kpi(sl,3.8,4.75,2.9,"+ 40 Plätze","auf der Terrasse",vs=30); kpi(sl,6.9,4.75,2.9,"460 m²","ganzes Erdgeschoss",vs=30); kpi(sl,10.0,4.75,2.6,"12 €/m²","Pacht ans Haus (Annahme)",TERRA,vs=30)
# 8 Staffel
sl=page(d,SEC[0],"Das Staffelgeschoss aus Holz spart Baukosten")
kpi(sl,0.7,2.0,3.6,"460 m²","Staffelgeschoss, kein Vollgeschoss"); kpi(sl,4.7,2.0,3.6,eur(460*700),"Ersparnis gegenüber Massivbau (700 €/m², Annahme)",POS); kpi(sl,8.9,2.0,3.6,"72 m²","schmale Dachterrasse rundum",GREY)
tx(sl,0.7,3.9,7.4,2.5,[{"t":"Leichter und schneller gebaut, kürzere Bauzeit."},{"t":"Zwei Partner aus dem Bekanntenkreis: Bauunternehmen unten, Zimmerei oben."},{"t":"Hilft beim QNG-Nachweis und beim Effizienzhaus-40-Standard."},{"t":"Brandschutz (Gebäudeklasse 4) und Schallschutz muss der Architekt nachweisen."}],size=15,space=10)
img(sl,IM+"terrasse.jpg",8.5,3.8,4.13,2.6)
# 9 Lage
sl=page(d,SEC[0],"Die neue Mitte entsteht rundum, wir eröffnen mit ihr Ende 2028")
tl=[("Nov 2026","Stellplatz alte Grundschule"),("ab März 2027","Bau Planstraße (Erschließung)"),("Mitte 2027","Unser Baubeginn"),("ab Juli 2027","Kreisverkehr Loruper Straße"),("Ende 2028","Marktplatz, Rathaus und unsere Eröffnung")]
ln=sl.shapes.add_connector(1,Inches(1.0),Inches(3.55),Inches(12.3),Inches(3.55)); ln.line.color.rgb=C(GREEN); ln.line.width=Pt(2)
for i,(a,b) in enumerate(tl):
    x=1.0+i*2.8; dot(sl,x-0.1,3.45,TERRA if "Unser" in b or "Ende" in a else GOLD,0.22)
    tx(sl,x-0.3,2.7,2.6,0.4,a,size=16,color=GREEN,font=HF,bold=True); tx(sl,x-0.3,3.95,2.5,1,b,size=13,color=INK)
tx(sl,0.7,5.6,11.9,0.9,["Grundstück: ca. 960 m², Baufeld 3 östlich des Rathauses, südlich der Planstraße. Mischgebiet, Gewerbe im EG erwünscht, Baureife liegt vor."],size=14,color=GREY)
# 10 B-Plan
sl=page(d,SEC[1],"Der Bebauungsplan passt weitgehend, drei Punkte sind offen","Plan 2023, rechtskräftig, Gebiet MI 3. Zum Vergleich Entwurf 1. Änderung (gilt nicht für MI 3): First 12,00 m, dann noch 2,10 m Luft. Zuordnung Baufeld 3 = MI 3 / Flurstück 59/1 ist noch nicht bestätigt. Keine Aussage zur Zulässigkeit.")
rows=[["Thema","Vorgabe im B-Plan","Unser Entwurf","Stand"],["Grundfläche (GRZ)","0,6 = max. 576 m²","540 m²","  passt"],["Geschosse","II bis III Vollgeschosse","EG, 1. OG, Staffel (Nicht-Vollgeschoss)","  klären"],["Höhe","Traufe 9,80 m, First 15,00 m (ab OK Fahrbahn)","gesamt ca. 9,90 m (Annahme), 5,10 m Luft","  klären"],["Dach","geneigt, mind. 38°","Flachdach mit Staffelgeschoss","  Befreiung nötig"],["Baufenster","10 m West, 3 m übrige Seiten","540 m², Lage zu prüfen","  klären"],["Stellplätze","auf dem Grundstück","ca. 8 in der GRZ II","  knapp"]]
table(sl,0.7,1.95,11.93,rows,[2,3.6,3.6,1.7],size=13,rh=0.55,align=["l","l","l","l"])
cl={"passt":POS,"klären":GOLD,"knapp":GOLD,"Befreiung nötig":NEG}
for i,r in enumerate(rows[1:]): dot(sl,10.88,1.95+0.55*(i+1)+0.2,cl[r[3].strip(" ")])
# 11 Stellplätze
sl=page(d,SEC[1],"Stellplätze sind der Engpass: es fehlen ca. 30 Plätze auf dem Grundstück")
cd=CategoryChartData(); cd.categories=["Bedarf (Annahme)","Platz in GRZ II","Mit Ausnahme"]; cd.add_series("Stellplätze",[41,8,12])
ch=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.7),Inches(1.9),Inches(5.6),Inches(4.5),cd).chart; style_chart(ch,12)
pl=ch.plots[0]; pl.gap_width=60; pl.has_data_labels=True; pl.data_labels.font.size=Pt(16); pl.data_labels.position=XL_LABEL_POSITION.OUTSIDE_END
for i,c in enumerate((TERRA,GREEN,GOLD)): pt=pl.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=C(c)
ch.value_axis.visible=False; hide_axis_lines(ch.value_axis); hide_axis_lines(ch.category_axis)
tx(sl,6.8,2.0,5.8,4.4,[{"t":"Bedarf ca. 41 Plätze","bold":True,"size":16,"color":GREEN},"Annahme: 33 für die Gastro (Gastro-Konzept) plus 1 je Wohnung. Maßgeblich ist die Satzung der Stadt.",{"t":"Freifläche: 420 m² (960 − 540)","bold":True,"size":16,"color":GREEN},"Hier liegen Stellplätze, Zufahrt und Terrasse. Befestigt zählen sie zur GRZ II (bis 0,8 = 228 m²), dort passen ca. 8 Plätze. Terrasse und Wintergarten im 10-m-Streifen West sind zu klären.",{"t":"Vorschlag an die Stadt","bold":True,"size":16,"color":GREEN},"Wasserdurchlässiger Stein und Ausnahme über 0,8 hinaus (ca. 12 Plätze), Rest auf der öffentlichen Parkfläche per Vereinbarung oder Ablöse."],size=13,space=7)
# 12 Fragen
sl=page(d,SEC[1],"Das fragen wir die Stadt am Montag, 09.11.2026")
qs=["Ist Baufeld 3 tatsächlich MI 3 (Flurstück 59/1) im rechtskräftigen Plan 2023?","Sind 540 m² Grundfläche im Baufenster zulässig?","Gilt das Staffelgeschoss als Nicht-Vollgeschoss, und ist ein Flachdach befreibar?","Dürfen Stellplätze mit wasserdurchlässigem Stein über GRZ 0,8 hinausgehen (§ 19 Abs. 4 Satz 4 Nr. 1 BauNVO)?","Mitnutzung der öffentlichen Parkfläche oder Höhe der Ablöse?","Dürfen Terrasse und Wintergarten in den 10-m-Streifen West (Baugrenze) und zählen sie zur GRZ II?","Kaufpreis 230 €/m² und Reservierung bis zur Finanzierungszusage?"]
for i,q in enumerate(qs):
    y=1.9+i*0.67; rect(sl,0.7,y,0.46,0.46,GREEN,shape=MSO_SHAPE.OVAL); tx(sl,0.7,y,0.46,0.46,str(i+1),size=15,color=WHITE,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,font=HF); tx(sl,1.45,y+0.07,11,0.5,q,size=15)
tx(sl,0.7,6.65,11.9,0.3,"Die vollständige Fragenliste (34 Punkte) liegt separat als Word-Datei vor.",size=10,color=GREY)
# 13 KfW
sl=page(d,SEC[2],"Die KfW gibt günstige Kredite für 70 % der Kosten, aber nur mit Bedingungen","Zinsen sind Annahmen (Quellen nennen 0,6 % bis 3,05 %). Rahmen laut Ratgebern, im aktuellen Merkblatt zu prüfen.")
for x,t,v,rows_ in ((0.7,"KfW 298 · Wohnungen","1.200.000 €",[("Rahmen","150.000 € je Wohnung (mit QNG)"),("Anzahl","8 Wohnungen"),("Zins (Annahme)","2,5 %, 10 Jahre fest")]),(6.9,"KfW 299 · Gastro","782.000 €",[("Rahmen","2.000 € je m² Nettogrundfläche (mit QNG)"),("Fläche","460 m² × 85 % = 391 m²"),("Zins (Annahme)","3,0 %, 10 Jahre fest")])):
    rect(sl,x,1.95,5.7,3.4,LIGHT,shape=MSO_SHAPE.ROUNDED_RECTANGLE); tx(sl,x+0.35,2.15,5,0.4,t,size=15,color=GREEN,bold=True); tx(sl,x+0.35,2.6,5,0.8,v,size=36,color=GREEN,font=HF)
    for i,(a,b) in enumerate(rows_): tx(sl,x+0.35,3.65+i*0.5,1.7,0.4,a,size=12,color=GREY); tx(sl,x+2.05,3.65+i*0.5,3.5,0.4,b,size=13)
tx(sl,0.7,5.65,11.9,0.9,[{"t":[("Zusammen 1,98 Mio. €, ",{"bold":True,"color":GREEN}),("der Rest von 0,86 Mio. € kommt von der Hausbank (4,0 %). Eigenkapital: 0 €.",{})]}],size=16)
# 14 QNG
sl=page(d,SEC[2],"QNG: das Siegel, das den höheren Kreditrahmen freischaltet")
cols_=[("Was ist das?","Qualitätssiegel Nachhaltiges Gebäude: ein staatliches Siegel für Gebäude, die mehr als nur Energie sparen."),("Was wird geprüft?","Ökobilanz (Treibhausgase, Primärenergie), Schadstoffe in Baustoffen, nachhaltige Materialien wie zertifiziertes Holz. Prüfung durch eine zugelassene Stelle."),("Was bringt es uns?","Mehr günstiges Darlehen: 8 × 50.000 € = 400.000 € bei den Wohnungen und rund 195.000 € bei der Gastro.")]
for i,(a,b) in enumerate(cols_):
    x=0.7+i*4.1; rect(sl,x,1.95,3.8,0.06,GOLD); tx(sl,x,2.2,3.7,0.4,a,size=18,color=GREEN,font=HF); tx(sl,x,2.8,3.7,2.5,b,size=14)
rect(sl,0.7,5.35,11.93,1.1,LIGHT); tx(sl,1.0,5.5,11.3,0.9,[{"t":[("Für uns heißt das: ",{"bold":True,"color":GREEN}),(f"Energie- und Nachhaltigkeitsberater von Anfang an einbinden. Im Modell sind 3 % Mehrkosten ({eur(Z['eh_k'])}) für Effizienzhaus 40 und QNG eingerechnet. Der Holzbau im Staffelgeschoss hilft (Annahme). Grenzwerte im QNG-Handbuch prüfen.",{})]}],size=13)
# 15 Checkliste
sl=page(d,SEC[2],"Checkliste: Das verlangt die KfW, und so stehen wir","Quellen: Verbraucherzentrale, Interhyp, KfW-Programmseiten (Suchtreffer 07.11.2026), im Merkblatt zu prüfen.")
rows=[["Bedingung","Stand bei uns"],["Effizienzhaus 40 bzw. Effizienzgebäude 40","  geplant, Nachweis durch Energieeffizienz-Experten"],["QNG-Siegel für den vollen Rahmen","  geplant, Berater noch zu beauftragen"],["Heizung ohne fossile Brennstoffe","  geplant (z. B. Wärmepumpe)"],["Antrag vor Baubeginn über die Hausbank","  Termin: Q1 2027, vor dem Baubeginn"],["Kein Rechtsanspruch, Mittel begrenzt","  Risiko, siehe Risiken"],["Kombination mit Programmen 296/596 ausgeschlossen","  nicht vorgesehen"]]
table(sl,0.7,1.95,11.93,rows,[5,5.5],size=14,rh=0.62,align=["l","l"])
for i,c in enumerate((GOLD,GOLD,GOLD,GOLD,NEG,POS)): dot(sl,6.55,1.95+0.62*(i+1)+0.23,c)
# 16 Zinsen
sl=page(d,SEC[2],"Zinsen: wir rechnen vorsichtig und prüfen Szenarien","Quellen: Börsen-Zeitung, mobiflip, PwC-Blog (Suchtreffer 07.11.2026, nicht im Volltext geprüft).")
tx(sl,0.7,1.95,5.8,0.4,"Zinsen im Modell (Annahme, 10 Jahre fest)",size=16,color=GREEN,font=HF)
table(sl,0.7,2.5,5.8,[["Darlehen","Zins","Tilgung"],["KfW 298 Wohnen","2,5 %","1 %"],["KfW 299 Gastro","3,0 %","1 %"],["Hausbank","4,0 %","1 %"],["Mischzins",pct(Z["mischzins"],2),"1 %"]],[3,1.2,1.2],size=14,rh=0.5,total=(4,))
tx(sl,0.7,5.2,5.8,1.4,"Weiter fallende Zinsen sind eine Erwartung und nicht belegt. Wir rechnen Szenarien mit −0,5 und +1,0 Prozentpunkten (Folie Szenarien).",size=13,color=GREY)
tx(sl,7.0,1.95,5.6,0.4,"Einlagensicherung",size=16,color=GREEN,font=HF)
tx(sl,7.0,2.5,5.6,4,[{"t":[("Gesetzlich: ",{"bold":True}),("100.000 € je Kunde und Bank.",{})]},{"t":[("Freiwillig (Privatbanken): ",{"bold":True}),("wird laut Presse bis 2030 schrittweise gesenkt.",{})]},{"t":[("Wegfall ab 2027? ",{"bold":True}),("nicht belegt, eine EU-Frist am 11.05.2027 ist nur fragmentarisch belegt.",{})]},{"t":[("Für uns: ",{"bold":True,"color":GREEN}),("betrifft nur Guthaben (Rücklagen, Kautionen), nicht die Darlehen. Größere Beträge auf mehrere Banken verteilen.",{})]}],size=14,space=11)
# 17 Alles auf einer Seite
sl=page(d,SEC[3],"Alles auf einer Seite: Kosten und Gewinn des ganzen Projekts","Zielpreis 1.450 € je m² BGF, ohne Eigenkapital, mit KfW. Tilgung ist Vermögensaufbau, kein Verlust. Ohne Steuern und Lohn des Bauherrn.")
tx(sl,0.7,1.85,5.8,0.35,"Was kostet es, und wer zahlt?",size=15,color=GREEN,font=HF)
table(sl,0.7,2.25,5.9,[["Posten","Betrag"],["Grundstück inkl. Steuer, Notar",eur(Z["grund"])],["Bau (Massiv, Holz-Staffel, Terrasse)",eur(Z["bau_roh"]+Z["abschlag"]+Z["terr_k"])],["Baunebenkosten 15 %",eur(Z["bnk_k"])],["Effizienzhaus 40 und QNG 3 %",eur(Z["eh_k"])],["Gastro-Ausbau",eur(150000)],["Zinsen in Bau- und Anlaufzeit",eur(Z["fin"])],["Gesamtkosten",eur(Z["gesamt"])],["bezahlt mit KfW-Darlehen",eur(1982000)],["bezahlt mit Hausbank-Darlehen",eur(Z["hb"])]],[3.6,1.6],size=12,rh=0.38,total=(7,))
tx(sl,7.0,1.85,5.6,0.35,"Was kommt rein, was geht raus? (pro Jahr)",size=15,color=GREEN,font=HF)
table(sl,7.0,2.25,5.63,[["Posten","pro Jahr","pro Monat"],["Miete 8 Wohnungen",eur(Z["miete_j"],0,True),eur(Z["miete_j"]/12,0,True)],["Pacht Gastro",eur(Z["pacht_j"],0,True),eur(Z["pacht_j"]/12,0,True)],["Rücklage 10 %",eur(-Z["rueck"]),eur(-Z["rueck"]/12)],["Zinsen",eur(-h[0][1]),eur(-h[0][1]/12)],["Tilgung 1 %",eur(-h[0][2]),eur(-h[0][2]/12)],["Plus im Haus",eur(Z["netto_imm"]-Z["kd_j"],0,True),eur(haus_plus,0,True)],["Gastro-Betrieb (50.000 € Umsatz/Monat)",eur(Z["betrieb"],0,True),eur(Z["betrieb"]/12,0,True)],["Plus gesamt",eur(Z["erg"],0,True),eur(Z["erg"]/12,0,True)]],[3,1.35,1.2],size=12,rh=0.42,total=(6,8))
tx(sl,0.7,6.15,11.9,0.5,[{"t":[(f"Faktor {f2(Z['dscr_imm'])}: ",{"bold":True,"color":GREEN}),("Miete und Pacht decken Zinsen und Tilgung allein, der Gastro-Gewinn kommt obendrauf.",{})]}],size=14)
# 18 Kosten
sl=page(d,SEC[3],f"Das Haus kostet {mio(Z['gesamt'])}, am meisten kostet der Bau",f"Das sind {num(Z['gesamt']/1540)} € je m² BGF (bei 2.200 € Baupreis: {num(B['gesamt']/1540)} €). Zielpreis noch nicht durch Angebote belegt.")
cats=["Bau (inkl. Holz, Terrasse)","Baunebenkosten","Grundstück","Gastro-Ausbau","Zinsen Bauzeit","Effizienzhaus, QNG"]; vals=[Z["bau_roh"]+Z["abschlag"]+Z["terr_k"],Z["bnk_k"],Z["grund"],150000,Z["fin"],Z["eh_k"]]
cd=CategoryChartData(); cd.categories=cats; cd.add_series("Kosten",vals)
ch=sl.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(0.7),Inches(1.9),Inches(8),Inches(4.6),cd).chart; style_chart(ch,13)
pl=ch.plots[0]; pl.gap_width=45; pl.has_data_labels=True; pl.data_labels.number_format='#,##0" €"'; pl.data_labels.number_format_is_linked=False; pl.data_labels.position=XL_LABEL_POSITION.OUTSIDE_END; pl.data_labels.font.size=Pt(13)
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb=C(GREEN); ch.value_axis.visible=False; hide_axis_lines(ch.value_axis); ch.category_axis.reverse_order=True; hide_axis_lines(ch.category_axis); ch.value_axis.maximum_scale=2800000
kpi(sl,9.3,2.1,3.3,mio(Z["gesamt"]),"Gesamtkosten inkl. Finanzierung"); kpi(sl,9.3,3.7,3.3,f"{num(Z['gesamt']/1540)} €","je m² Bruttogrundfläche",GREY); kpi(sl,9.3,5.3,3.3,"0 €","Eigenkapital (100 % Fremdkapital)",TERRA)
# 19 Finanzierung
sl=page(d,SEC[3],"70 % des Geldes kommen von der KfW, der Rest von der Hausbank")
cd=CategoryChartData(); cd.categories=["KfW 298 Wohnen","KfW 299 Gastro","Hausbank"]; cd.add_series("Darlehen",[1200000,782000,Z["hb"]])
ch=sl.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT,Inches(0.7),Inches(1.9),Inches(5.2),Inches(4.6),cd).chart; style_chart(ch,12,True)
for i,c in enumerate((GREEN,GOLD,TERRA)): pt=ch.plots[0].series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=C(c)
ch.plots[0].has_data_labels=True; ch.plots[0].data_labels.number_format='0%'; ch.plots[0].data_labels.show_percentage=True; ch.plots[0].data_labels.show_value=False; ch.plots[0].data_labels.font.size=Pt(13); ch.plots[0].data_labels.font.color.rgb=C(WHITE)
(l1,z1),(l2,z2),(l3,z3)=Z["loans"]
table(sl,6.3,2.1,6.33,[["Darlehen","Betrag","Zins","Rate / Monat"],["KfW 298 Wohnen",eur(l1),pct(z1),eur(l1*(z1+.01)/12)],["KfW 299 Gastro",eur(l2),pct(z2),eur(l2*(z2+.01)/12)],["Hausbank",eur(l3),pct(z3),eur(l3*(z3+.01)/12)],["Summe",eur(Z["gesamt"]),pct(Z["mischzins"],2),eur(Z["kd_m"])]],[2.2,1.6,0.9,1.6],size=13,rh=0.55,total=(4,))
tx(sl,6.3,5.1,6.33,1.5,[f"Bau 15 Monate, danach 12 Monate Anlaufzeit ohne Tilgung. Die Zinsen dieser Zeit ({eur(Z['fin'])}) zahlt die Hausbank vor.","Rate danach: Zins plus 1 % Tilgung."],size=13,color=GREY,space=6)
# 20 Waterfall
sl=page(d,SEC[3],f"Miete und Pacht tragen die Raten: {eur(haus_plus,0,True)} Plus im Monat","Erstes Jahr nach der Anlaufzeit, ohne Gastro-Betrieb. Zinsen und Tilgung aus dem Tilgungsplan.")
steps=[("Miete",0,Z["miete_j"],"up"),("Pacht",Z["miete_j"],Z["pacht_j"],"up"),("Rücklage",Z["roh"]-Z["rueck"],Z["rueck"],"down"),("Zinsen",Z["netto_imm"]-h[0][1],h[0][1],"down"),("Tilgung",Z["netto_imm"]-h[0][1]-h[0][2],h[0][2],"down"),("Plus",0,Z["netto_imm"]-Z["kd_j"],"up")]
cd=CategoryChartData(); cd.categories=[s[0] for s in steps]
cd.add_series("Basis",[s[1] for s in steps]); cd.add_series("Plus",[s[2] if s[3]=="up" else None for s in steps]); cd.add_series("Minus",[s[2] if s[3]=="down" else None for s in steps])
ch=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED,Inches(0.7),Inches(1.9),Inches(8.6),Inches(4.6),cd).chart; style_chart(ch,13); pl=ch.plots[0]; pl.gap_width=40; pl.overlap=100
pl.series[0].format.fill.background(); pl.series[0].format.line.fill.background()
for k,c in ((1,POS),(2,NEG)):
    s_=pl.series[k]; s_.format.fill.solid(); s_.format.fill.fore_color.rgb=C(c); s_.data_labels.show_value=True; s_.data_labels.number_format='#,##0" €"'; s_.data_labels.number_format_is_linked=False; s_.data_labels.font.size=Pt(12); s_.data_labels.font.color.rgb=C(WHITE)
ch.value_axis.visible=False; hide_axis_lines(ch.value_axis); hide_axis_lines(ch.category_axis)
kpi(sl,9.7,2.0,2.9,f"Faktor {f2(Z['dscr_imm'])}","Miete und Pacht geteilt durch Zinsen und Tilgung",POS,vs=30); kpi(sl,9.7,3.65,2.9,eur(Z["netto_imm"]/12),"Netto-Ertrag pro Monat",GREEN,vs=30); kpi(sl,9.7,5.3,2.9,eur(Z["kd_m"]),"Zinsen und Tilgung pro Monat",GREY,vs=30)
# 21 Einzel
sl=page(d,SEC[3],"Jede Einheit trägt sich selbst, die Wohnungen im 1. OG sind am knappsten","Plus = Netto-Miete (nach 10 % Rücklage) minus Zins und 1 % Tilgung. Faktor = Netto-Miete geteilt durch Kapitaldienst; über 1,0 trägt sich die Einheit selbst.")
def urow(n,x): return [n,num(x["nf"])+" m²",eur(x["kosten"]),eur(x["kfw"]),eur(x["bank"]),eur(x["netto"]),eur(x["zins"]+x["tilg"]),eur(x["plus"]/12,0,True),f2(x["dscr"])]
tot=lambda k: sum(x[k] for x in UZ)
rows=[["Einheit (je Stück)","Fläche","Kosten","KfW","Hausbank","Netto-Miete/J","Zins+Tilgung/J","Plus/Monat","Faktor"],urow("WE 1–5 (1. OG)",we15),urow("WE 6–8 (Staffel)",we68),urow("Gastro-Fläche",gas),["Gesamtes Haus","1.185 m²",eur(tot("kosten")),eur(tot("kfw")),eur(tot("bank")),eur(tot("netto")),eur(tot("zins")+tot("tilg")),eur(tot("plus")/12,0,True),f2(tot("netto")/(tot("zins")+tot("tilg")))]]
table(sl,0.7,1.95,11.93,rows,[2.3,1,1.4,1.2,1.2,1.4,1.5,1.2,0.9],size=13,rh=0.62,total=(4,))
for i in range(1,4): pass
tx(sl,0.7,5.4,11.9,1.2,[{"t":[("Warum 1. OG knapper? ",{"bold":True,"color":GREEN}),("Massivbau und je Wohnung ein Anteil am Kern im EG: 83 m² Wohnfläche tragen 118 m² Bruttogrundfläche. Die Staffel-Wohnungen sparen durch Holz.",{})]}],size=14)
# 22 Beispiel
x=we15; bau_we=1450*x["bgf"]
sl=page(d,SEC[3],"Beispiel: So rechnet sich eine Wohnung im 1. OG")
tx(sl,0.7,1.9,5.8,0.35,"Was kostet sie?",size=16,color=GREEN,font=HF)
table(sl,0.7,2.35,5.8,[["Posten","Betrag"],[f"Bau ({num(x['bgf'])} m² BGF × 1.450 €)",eur(bau_we)],["Baunebenkosten 15 %",eur(bau_we*.15)],["Effizienzhaus, QNG 3 %",eur(bau_we*1.15*.03)],["Grundstück und Zinsen (anteilig)",eur(x["kosten"]-bau_we*1.15*1.03)],["Gesamtkosten",eur(x["kosten"])],["je m² Wohnfläche",eur(x["kosten"]/x["nf"])]],[3.6,1.6],size=13,rh=0.5,total=(5,))
tx(sl,7.0,1.9,5.6,0.35,"Wie wird sie bezahlt, was bringt sie?",size=16,color=GREEN,font=HF)
table(sl,7.0,2.35,5.63,[["Posten","Betrag"],["KfW 298 (2,5 %)",eur(x["kfw"])],["Hausbank (4,0 %)",eur(x["bank"])],["Netto-Miete pro Jahr (83 m² × 11,18 € × 12 − 10 %)",eur(x["netto"])],["Zins und Tilgung pro Jahr",eur(-(x["zins"]+x["tilg"]))],["Plus pro Jahr",eur(x["plus"],0,True)],["Plus pro Monat",eur(x["plus"]/12,0,True)]],[3.6,1.6],size=13,rh=0.5,total=(5,))
tx(sl,0.7,6.0,11.9,0.6,f"Das Plus ist klein (Faktor {f2(x['dscr'])}): 5 % höhere Baukosten oder 1 Prozentpunkt mehr Zins drehen es ins Minus.",size=14,color=NEG)
# 23 Gastro Haus Betrieb
g=gas
sl=page(d,SEC[3],"Gastro: Das Haus bekommt Pacht, der Betrieb verdient zusätzlich","Umsatz 50.000 € und Marge 30,5 % sind Branchen-Richtwerte, keine Werte aus Werlte. Lohn des Bauherrn und Steuern nicht gerechnet.")
tx(sl,0.7,1.9,5.8,0.35,"Haus-GbR/UG: Gastro-Fläche",size=16,color=GREEN,font=HF)
table(sl,0.7,2.35,5.8,[["Posten","Betrag"],["Kosten der Gastro-Fläche (inkl. Ausbau)",eur(g["kosten"])],["davon KfW 299 / Hausbank",f"{eur(g['kfw'])} / {eur(g['bank'])}"],["Pacht pro Jahr (460 m² × 12 €)",eur(g["rent"])],["Netto-Pacht nach 10 % Rücklage",eur(g["netto"])],["Zins und Tilgung pro Jahr",eur(-(g["zins"]+g["tilg"]))],["Plus pro Monat (Faktor "+f2(g["dscr"])+")",eur(g["plus"]/12,0,True)]],[3.7,2.1],size=13,rh=0.55,total=(6,),align=["l","r"])
tx(sl,7.0,1.9,5.6,0.35,"Betreiber-UG: Gastro-Betrieb pro Monat",size=16,color=GREEN,font=HF)
table(sl,7.0,2.35,5.63,[["Posten","Betrag"],["Umsatz (netto)",eur(50000)],["Wareneinsatz, Personal, Betriebskosten",eur(-34750)],["Gewinn vor Pacht (30,5 %)",eur(15250)],["Pacht an das Haus",eur(-5520)],["Betriebsergebnis vor Lohn und Steuern",eur(9730,0,True)]],[3.7,1.9],size=13,rh=0.55,total=(5,))
# 24 Umsatz
sl=page(d,SEC[3],"Ab 18.100 € Umsatz im Monat verdient der Betrieb seine Pacht","Haus insgesamt (Betreiber = Bauherr) sind die Raten ab ca. 9.700 € Umsatz bezahlt. 50.000 € Umsatz = ca. 4.000 € je Sitzplatz und Jahr bei 150 Plätzen.")
us=[30000,40000,50000,60000,70000]; cd=CategoryChartData(); cd.categories=[num(u) for u in us]; cd.add_series("Gewinn nach Pacht",[u*.305-5520 for u in us])
ch=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.7),Inches(1.9),Inches(7.2),Inches(4.6),cd).chart; style_chart(ch,13); pl=ch.plots[0]; pl.gap_width=50
pl.has_data_labels=True; pl.data_labels.number_format='#,##0" €"'; pl.data_labels.number_format_is_linked=False; pl.data_labels.position=XL_LABEL_POSITION.OUTSIDE_END; pl.data_labels.font.size=Pt(13)
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb=C(GREEN); ch.value_axis.visible=False; hide_axis_lines(ch.value_axis); hide_axis_lines(ch.category_axis)
tx(sl,0.7,6.4,7,0.25,"Umsatz pro Monat in €",size=11,color=GREY,align=PP_ALIGN.CENTER)
table(sl,8.3,2.1,4.33,[["Umsatz","Gewinn vor Pacht","nach Pacht"]]+[[eur(u),eur(u*.305),eur(u*.305-5520,0,True)] for u in us],[1.2,1.5,1.3],size=12,rh=0.5,hl=(3,))
# 25 Abzahlung
sl=page(d,SEC[3],f"Nach 10 Jahren Zinsbindung bleiben {mio(Z['rest10'])} Restschuld")
cd=CategoryChartData(); cd.categories=[str(y) for y,_,_,_ in h]; cd.add_series("Restschuld",[round(r) for *_,r in h])
ch=sl.shapes.add_chart(XL_CHART_TYPE.LINE,Inches(0.7),Inches(1.9),Inches(7.4),Inches(4.5),cd).chart; style_chart(ch,11)
s_=ch.plots[0].series[0]; s_.format.line.color.rgb=C(GREEN); s_.format.line.width=Pt(3); s_.smooth=False
ch.value_axis.tick_labels.number_format='#,##0'; ch.value_axis.tick_labels.number_format_is_linked=False; hide_axis_lines(ch.value_axis,True); ch.category_axis.tick_label_position  # noqa
tx(sl,0.7,6.4,7.4,0.25,"Jahre",size=11,color=GREY,align=PP_ALIGN.CENTER)
yrs=[1,5,10,20,35]; table(sl,8.5,2.1,4.13,[["Jahr","Zinsen","Tilgung","Restschuld"]]+[[("10 (Ende)" if y==10 else str(y)),eur(h[y-1][1]),eur(h[y-1][2]),eur(h[y-1][3])] for y in yrs],[1,1.3,1.3,1.5],size=11,rh=0.5,hl=(3,))
tx(sl,8.5,5.4,4.13,1.2,"Danach muss die Anschlussfinanzierung geplant werden.",size=13,color=GREY)
# 26 Prognose
sl=page(d,SEC[3],"In zehn Jahren wächst das Plus auf knapp 190.000 € im Jahr","Annahme: Mieten, Pacht und Umsatz steigen 1,5 % pro Jahr, der Kapitaldienst bleibt gleich. Ergebnis inkl. Gastro-Betrieb, vor Steuern und Lohn.")
pg={r[0]:r for r in Z["prog"]}; yy=[1,3,5,7,10]
table(sl,0.7,1.95,11.93,[["Jahr"]+[str(y) for y in yy],["Netto-Ertrag vor Kapitaldienst"]+[eur(pg[y][5]) for y in yy],["Zinsen und Tilgung"]+[eur(-Z["kd_j"])]*5,["Plus pro Jahr"]+[eur(pg[y][6],0,True) for y in yy],["Faktor"]+[f2(pg[y][7]) for y in yy],["Restschuld"]+[eur(pg[y][8]) for y in yy]],[3.2,1.7,1.7,1.7,1.7,1.7],size=14,rh=0.7,total=(3,))
# 27 Belastungstest
sl=page(d,SEC[3],"Was wäre wenn? Das Haus bleibt in fast allen Fällen im Plus","Belastungstest auf das Gesamtergebnis inkl. Gastro-Betrieb (Faktor gesamt). Vereinfachte Rechnung, die Hausbank prüft mit eigenen Annahmen.")
base=ss[0][1]; gf=[s for s in ss if s[0].startswith("Gastro fällt")][0]; ss2=[s for s in ss if not s[0].startswith("Gastro fällt")]
leer=("Eine Wohnung im 1. OG dauerhaft leer",base-we15["netto"]/12,(Z["netto_ges"]-we15["netto"])/Z["kd_j"])
rows=[["Was passiert?","Ergebnis / Monat","Faktor","Änderung"]]+[[n,eur(e,0,True),f2(f_),"" if n=="Plan" else eur(e-base,0,True)] for n,e,f_ in ss2+[leer,gf]]
table(sl,0.7,1.95,11.93,rows,[6,2,1.2,1.7],size=13,rh=0.45,hl=(1,))
for i,r in enumerate(rows[1:]): dot(sl,0.72-0.0,1.95+0.5*(i+1)+0.17,POS if float(r[2].replace(",","."))>=1.2 else (GOLD if float(r[2].replace(",","."))>=1.0 else NEG)) if False else None
tx(sl,0.7,6.2,11.9,0.3,"Faktor ab 1,2 gilt bei Banken als üblich, unter 1,0 trägt sich das Haus nicht mehr selbst.",size=10,color=GREY)
# 28 Szenarien
sl=page(d,SEC[3],"Der Baupreis entscheidet: Erst beim Zielpreis tragen sich alle Einheiten","DSCR je Einheit (mit KfW). Zielpreis 1.450 €/m² ist noch nicht durch Angebote belegt, deshalb die Vergleichszeilen.")
def srow(nm,**kw):
    m,u=unitcalc(**kw); return [nm,eur(m["gesamt"]),f2(u[0]["dscr"]),f2(u[5]["dscr"]),f2(u[8]["dscr"]),eur((m["netto_imm"]-m["kd_j"])/12,0,True)]
rows=[["Szenario","Gesamtkosten","WE 1–5","WE 6–8","Gastro","Plus Haus / Monat"],srow("Bankunterlagen: 2.200 €/m², Holz −400",bau=2200,holz=400),srow("1.800 €/m², Holz −700",bau=1800,holz=700),srow("Zielpreis: 1.450 €/m², Holz −700",bau=1450,holz=700),srow("Zielpreis, Zins −0,5 Prozentpunkte",bau=1450,holz=700,dz=-0.005),srow("Zielpreis, Zins +1,0 Prozentpunkt",bau=1450,holz=700,dz=0.01)]
table(sl,0.7,1.95,11.93,rows,[4.2,1.9,1.2,1.2,1.2,2.2],size=14,rh=0.62,hl=(3,),bold=(3,))
tx(sl,0.7,6.0,11.9,0.6,"Lesehilfe: Faktor unter 1,0 = die Einheit muss zugezahlt werden, über 1,0 = sie trägt sich selbst.",size=13,color=GREY)
# 29 Wert
sl=page(d,SEC[3],"Die Bank wird mehr Sicherheit verlangen: Wert und Beleihung","Vereinfachtes Ertragswertverfahren mit Annahmen; ein Gutachter der Bank ermittelt den verbindlichen Wert.")
table(sl,0.7,1.95,5.8,[["Ertragswert","Betrag"],["Rohertrag pro Jahr (Mieten, Pacht)",eur(Z["roh"])],["Reinertrag nach Bewirtschaftung",eur(Z["rein"])],["Bodenwert (960 m² × 230 €)",eur(Z["boden"])],["Gebäudeertragswert",eur(Z["ew_geb"])],["Ertragswert gesamt",eur(Z["ew"])]],[3.6,2.2],size=13,rh=0.55,total=(5,))
table(sl,7.0,1.95,5.63,[["Beleihung","Betrag"],["Beleihungswert (niedrigerer Wert, −10 %)",eur(Z["bel"])],["Gesamtkosten und Darlehen",eur(Z["gesamt"])],["Beleihungsauslauf",f"{Z['auslauf']*100:.0f} %"],["Auslauf nur KfW-Darlehen",f"{Z['auslauf_kfw']*100:.0f} %"],["Über 80 % Auslauf",eur(Z["ek80"])]],[3.6,2.0],size=13,rh=0.55,total=(3,))
tx(sl,0.7,5.55,11.9,1.1,[{"t":[("Heißt: ",{"bold":True,"color":GREEN}),(f"Über 80 % Beleihung braucht die Bank zusätzliche Sicherheiten (Grundschulden auf weitere Immobilien, Bürgschaft) oder Eigenkapital von ca. {mio(Z['ek80'])}. Der Ertragswert ({mio(Z['ew'])}) liegt über den Kosten ({mio(Z['gesamt'])}).",{})]}],size=14)
# 30 Airbnb
sl=page(d,SEC[3],"Airbnb lohnt sich nicht: alle 8 Wohnungen bleiben langfristig vermietet")
table(sl,0.7,1.95,7.4,[["Zwei Apartments à","45 m²","60 m²","83 m²"],["Preis pro Nacht","80 €","95 €","115 €"],["Netto Airbnb je Apartment/Monat","535 €","636 €","770 €"],["Netto langfristige Miete","453 €","604 €","835 €"],["Möblierung (im Kredit)","27.000 €","36.000 €","49.800 €"],["Mehrertrag für 2 Apartments/Monat","−60 €","−236 €","−546 €"]],[3.4,1.3,1.3,1.4],size=13,rh=0.6,neg=(5,))
tx(sl,8.5,2.0,4.1,3.5,["Kein Apartment erreicht den nötigen Mehrertrag von 300 € im Monat.","Dazu kommen Aufwand, Reinigung und ab 12 Betten Sonderbau-Brandschutz."],size=15,space=12)
# 31 Risiken
sl=page(d,SEC[4],"Die größten Risiken und was wir dagegen tun")
rows=[["Risiko","Was passiert?","Was wir tun"],["Baupreis höher als 1.450 €/m²","1. OG trägt die Raten nicht allein (bei 1.800 €: Faktor 0,83)","Angebote einholen, Holz-Staffel, Gewerke aus dem Netzwerk"],["Zins nach Bindung höher","+1 Prozentpunkt: ca. 2.100 € mehr pro Monat","KfW-Zusage vor Baubeginn, Forward-Darlehen"],["Gastro fällt aus","Faktor sinkt auf "+f2(gf[2]),"Erfahrener Betreiber, Pachtstaffel, Bonitätsprüfung"],["Genehmigung","Staffel, Flachdach, Stellplätze offen","Vorabstimmung mit der Stadt, Termin 09.11."],["Sicherheiten","Auslauf "+f"{Z['auslauf']*100:.0f}"+" %","Zusatzsicherheiten, Bürgschaft oder Eigenkapital"]]
table(sl,0.7,1.95,11.93,rows,[3,4.4,4.5],size=13,rh=0.78,align=["l","l","l"])
# 32 Brauche
sl=page(d,SEC[4],"Was ich von Stadt und Bank brauche")
tx(sl,0.7,1.95,5.8,0.4,"Von der Stadt",size=20,color=GREEN,font=HF)
tx(sl,0.7,2.6,5.8,4,[{"t":[("Genehmigung: ",{"bold":True}),("540 m², Staffel als Nicht-Vollgeschoss, Flachdach und Höhe schriftlich bestätigen.",{})]},{"t":[("Stellplätze: ",{"bold":True}),("GRZ II mit wasserdurchlässigem Stein, Mitnutzung der Parkfläche oder faire Ablöse.",{})]},{"t":[("Grundstück: ",{"bold":True}),("230 €/m² mit Baureife, Reservierung bis zur Finanzierungszusage.",{})]}],size=15,space=12)
tx(sl,7.0,1.95,5.6,0.4,"Von der Bank",size=20,color=GREEN,font=HF)
tx(sl,7.0,2.6,5.6,4,[{"t":[("Darlehen: ",{"bold":True}),(f"{mio(Z['gesamt'])} mit KfW 298/299 und 12 Monaten Anlaufzeit ohne Tilgung.",{})]},{"t":[("Sicherheiten: ",{"bold":True}),("Gespräch über Grundschulden oder Bürgschaft wegen des Beleihungsauslaufs.",{})]},{"t":[("KfW-Antrag: ",{"bold":True}),("für 298 und 299 vor Baubeginn über die Hausbank.",{})]}],size=15,space=12)
# 33 Schritte
sl=page(d,SEC[4],"Nächste Schritte bis zur Eröffnung Ende 2028")
st=[("Nov 2026","Termin Bürgermeister 09.11., Fragenliste"),("Nov–Dez 2026","Angebote für Rohbau, Zimmerei, Ausbau, Maler"),("Dez 2026","Hausbank: KfW, Zinsen, Sicherheiten; Steuerberater"),("Q1 2027","Architekt, Energieberater (QNG), Bauantrag, KfW-Antrag"),("Mitte 2027","Baubeginn, 15 Monate Bauzeit"),("Ende 2028","Eröffnung zusammen mit der neuen Mitte")]
for i,(a,b) in enumerate(st):
    y=1.95+i*0.78; rect(sl,0.7,y,0.5,0.5,TERRA if i==5 else GREEN,shape=MSO_SHAPE.OVAL); tx(sl,0.7,y,0.5,0.5,str(i+1),size=15,color=WHITE,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,font=HF); tx(sl,1.5,y+0.07,2.4,0.4,a,size=17,color=GREEN,font=HF,bold=True); tx(sl,4.0,y+0.09,8.5,0.4,b,size=15)
# 34 Anhang
sl=d.blank(SAGE); rect(sl,9.5,3.0,5.5,5.5,BLUSH,shape=MSO_SHAPE.OVAL); tx(sl,0.9,2.8,10,1,"Anhang",size=48,color=INK,font=HF); tx(sl,0.9,3.9,8,0.8,"Annahmen, Gastro-Kosten, Gastro-Ausbau, Mietdaten, Quellen",size=18,color=GREY)
# 35 Annahmen
sl=page(d,SEC[5],"Rechenannahmen auf einen Blick")
rows=[["Annahme","Wert","Herkunft"],["Baukosten","1.450 €/m² BGF (Bank-Excel: 2.200 €)","Zielwert, Angebote nötig"],["Holzabschlag Staffel","700 €/m² (Excel: 400 €)","Annahme"],["Baunebenkosten / Effizienzhaus, QNG","15 % / 3 %","Annahme, Architekt bestätigt"],["Grundstück","960 m² × 230 € + 7 % Nebenkosten","Bauherr / Stadt"],["Miete / Pacht","11,18 €/m² / 12 €/m²","Bauherr / Annahme"],["Rücklage","10 % von Miete und Pacht","Annahme"],["Gastro","50.000 € Umsatz/Monat, Marge 30,5 %","Bauherr / Richtwert"],["Zinsen","KfW 2,5 % und 3,0 %, Hausbank 4,0 %, 1 % Tilgung","Annahme"],["Bauzeit / Anlaufzeit","15 Monate / 12 Monate","Annahme"],["Eigenkapital","0 €","Bauherr"]]
table(sl,0.7,1.85,11.93,rows,[3.6,5.2,3],size=12,rh=0.43,align=["l","l","l"])
# 36 Gastro Kosten
sl=page(d,SEC[5],"Gastro: Kosten pro Monat bei 50.000 € Umsatz","Branchen-Richtwerte, keine Werte aus Werlte.")
po=[("Wareneinsatz (Essen, Getränke)","28 %",14000),("Personal (ohne Chef-Lohn)","30 %",15000),("Pacht ans Haus (460 m² × 12 €)","",5520),("Energie, Wasser, Müll","3 %",1500),("Reinigung, Verbrauchsmaterial","2 %",1000),("Werbung","1,5 %",750),("Reparaturen, Wartung, Kasse","1,5 %",750),("Sonstiges","1,5 %",750),("Versicherungen, GEMA","1 %",500),("Steuerberater, Buchhaltung","1 %",500)]
t_=sum(p[2] for p in po)
table(sl,0.7,1.85,8.5,[["Posten","Anteil","Betrag"]]+[[a,b,eur(c)] for a,b,c in po]+[["Summe Kosten","",eur(t_)],["Gewinn nach Pacht, vor Lohn","",eur(50000-t_)]],[4.6,1.2,1.6],size=12,rh=0.36,total=(11,12))
# 37 Ausbau
sl=page(d,SEC[5],"Gastro-Ausbau: 150.000 € sind knapp, Angebote sind nötig","Bei 200.000 € Ausbau steigt die Rate um ca. 190 € im Monat. Baunebenkosten fallen auf Möbel und Geräte nicht an.")
ab=[("Küche (Herd, Kühlräume, Edelstahl, Spülküche)",30000),("Lüftung und Abluft",18000),("Theke und Bar",20000),("Möbel (ca. 150 Plätze, Lounge, Séparée)",28000),("Beleuchtung und Deko",8000),("Wand, Boden, Decke, Akustik",15000),("Gäste-WC Ausstattung",5000),("Kasse, Technik, Musik, WLAN",5000),("Terrasse (Holzdeck, Möbel, Heizstrahler)",6000),("Planung und Genehmigung",5000),("Eröffnung, Marketing, Erstbestückung",3000),("Puffer 5 %",7150)]
table(sl,0.7,1.85,8.5,[["Posten","Betrag"]]+[[a,eur(b)] for a,b in ab]+[["Summe (im Modell: 150.000 €)",eur(sum(b for _,b in ab))]],[6,2],size=12,rh=0.36,total=(13,))
# 38 Mieten
sl=page(d,SEC[5],"Mietdaten: Wir rechnen mit 11,18 €/m², Neubau liegt bei 10,7 bis 11,0 €","Quellen: mietpreise.info/mietspiegel/werlte, miete-aktuell.de, immobilienscout24.de (Kreis Emsland), Abruf Oktober 2026.")
table(sl,0.7,1.95,8.2,[["Quelle","Wert für Werlte"],["ImmoScout24 (Wohnungen, Durchschnitt)","7,78 €/m²"],["miete-aktuell.de (Kaltmiete 2026)","8,13 €/m²"],["mietpreise.info (14 Inserate, Spanne 6,09–14,48 €)","9,58 €/m²"],["mietpreise.info (Neubau)","10,73–11,02 €/m²"],["Landkreis Emsland (ImmoScout24, Q2 2026)","8,10 €/m²"]],[5.6,2.4],size=13,rh=0.6,hl=(4,))
tx(sl,9.3,2.0,3.3,3.5,["Im Modell: 11,18 €/m² Kaltmiete (950 € für 85 m², Bauherr, zentrale Lage).","Gastro-Pacht 12 €/m² ohne Marktdaten."],size=14,space=10)
# 39 Quellen
sl=page(d,SEC[5],"Quellen und Stand der Recherche","Alles Suchtreffer vom 07.11.2026, nicht im Volltext geprüft. Alle Preise, Zinsen und Umsätze sind Annahmen. Keine Aussage zur baurechtlichen Zulässigkeit.")
table(sl,0.7,1.95,11.93,[["Quelle","Aussage"],["Verbraucherzentrale, Interhyp","KfW 298: 100.000 € je Wohneinheit, mit QNG 150.000 €"],["KfW, co2online","KfW 299: bis 2.000 € je m² Nettogrundfläche mit QNG, max. 10 Mio. €"],["vergleich.de (22.06.2026), WIBank","KfW 298 effektiv ca. 2,60 %, andere Quellen 0,6 bis 1,5 %"],["Börsen-Zeitung, mobiflip, PwC-Blog","Einlagensicherung Privatbanken bis 2030 gesenkt; EU-Frist 11.05.2027 fragmentarisch; Wegfall 2027 nicht belegt"],["Thüringer Landesamt für Statistik (PR 094/25, 120/25)","Veranschlagte Baukosten Mehrfamilienhäuser 1.908 bis 2.366 €/m² Wohnfläche (Genehmigungsdaten)"]],[4,8],size=13,rh=0.7,align=["l","l"])
d.prs.save(OUT); print("slides",d.n)
