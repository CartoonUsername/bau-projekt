import sys
sys.path.insert(0,"/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/einzel")
from model import model, sens
from einheiten import units, P as UP
from lib import eur, num, pct, f2
from ui import *
OUT="/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/deck/Neue-Mitte-Werlte_Baufeld3_Bankpraesentation_2026-11.pptx"
IM="/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/deck/bilder/"
def unitcalc(**kw):
    m=model(**kw); p=dict(UP); p.update(bau=kw.get("bau",2200.0),holz=kw.get("holz",400.0),fin=m["fin"],z298=m["z298"],z299=m["z299"],zbank=m["zb"],bnk=m["bnk"],eh=m["eh"],aussen=kw.get("aussen",0.0))
    u,_=units(p,pacht=kw.get("pacht",12.0),miete=kw.get("miete",11.176))
    for x in u:
        z=p["z299"] if x["typ"]=="Gastro" else p["z298"]
        x["zins"]=x["kfw"]*z+x["bank"]*p["zbank"]; x["tilg"]=(x["kfw"]+x["bank"])*p["til"]; x["plus"]=x["netto"]-x["zins"]-x["tilg"]
    return m,u
RK=dict(bau=2200,holz=400,bnk=0.17,eh=0.04,pacht=8.0,rl=0.15,miete=10.9,aussen=100000.0)
Z,UZ=unitcalc(**RK); B=model()
ZT=model(**{**RK,"bau":1450,"holz":700})
def be_um(m): return (m["kd_j"]-m["netto_imm"]+m["pacht_j"])/m["marge"]/12
def erg_um(m,u): return (m["netto_imm"]+u*12*m["marge"]-m["pacht_j"]-m["kd_j"])/12
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
kpi(sl,0.7,4.75,2.9,"150 Plätze","innen (130 Gastraum, 20 Séparée)",vs=30); kpi(sl,3.8,4.75,2.9,"+ 40 Plätze","auf der Terrasse",vs=30); kpi(sl,6.9,4.75,2.9,"460 m²","ganzes Erdgeschoss",vs=30); kpi(sl,10.0,4.75,2.6,"8 €/m²","Pacht ans Haus (Annahme)",TERRA,vs=30)
# 8 Staffel
sl=page(d,SEC[0],"Das Staffelgeschoss aus Holz spart Baukosten")
kpi(sl,0.7,2.0,3.6,"460 m²","Staffelgeschoss in Holzbau"); kpi(sl,4.7,2.0,3.6,eur(460*400),"Ersparnis gegenüber Massivbau (400 €/m², Annahme)",POS); kpi(sl,8.9,2.0,3.6,"72 m²","schmale Dachterrasse rundum",GREY)
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
sl=page(d,SEC[1],"Bebauungsplan: Fläche, Geschosse und Höhe passen, zwei Punkte brauchen eine Befreiung","Plan 2023 (rechtskräftig), MI 3: Begründung 3.2, örtliche Bauvorschrift 2.2. Baufenster ca. 440 m² aus dem Plan abgegriffen, nicht vermessen. Zuordnung Baufeld 3 = MI 3 unbestätigt. Keine Aussage zur Zulässigkeit.")
SP="\u2003\u2003"
rows=[["Thema","Vorgabe im B-Plan","Unser Entwurf","Stand"],
["Grundfläche (GRZ)","0,6 = max. 576 m²","540 m²",SP+"passt"],
["Geschosse","II bis III Vollgeschosse","EG, 1. OG, Staffel: auch als 3. Vollgeschoss erlaubt",SP+"passt"],
["Höhe","Traufe max. 9,80 m, First max. 15,00 m","First ca. 9,90 m (5,10 m Luft), Traufe auf 9,80 m auslegen",SP+"passt"],
["Dach","Hauptdach geneigt, mind. 38°","Flachdach mit Staffelgeschoss (Alternative: Satteldach 38°)",SP+"Befreiung nötig"],
["Baufenster","10 m West, 3 m übrige Seiten, ca. 440 m²","540 m²: ca. 100 m² über der Baugrenze",SP+"Befreiung nötig"],
["Stellplätze","auf dem Grundstück","ca. 8 in der GRZ II, 420 m² Freifläche",SP+"knapp"]]
table(sl,0.7,1.95,11.93,rows,[2,3.4,4.3,1.9],size=13,rh=0.58,align=["l","l","l","l"])
cl={"passt":POS,"knapp":GOLD,"Befreiung nötig":NEG}
for i,r in enumerate(rows[1:]): dot(sl,10.62,1.95+0.58*(i+1)+0.21,cl[r[3].strip("\u2003")])
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
qs=["Ist Baufeld 3 tatsächlich MI 3 (Flurstück 59/1) im rechtskräftigen Plan 2023?","Das Baufenster hat ca. 440 m²: Befreiung von der Baugrenze für 540 m²?","Ist das Staffelgeschoss als drittes Vollgeschoss (II–III) erlaubt, und ist das Flachdach befreibar?","Dürfen Stellplätze mit wasserdurchlässigem Stein über GRZ 0,8 hinausgehen (§ 19 Abs. 4 Satz 4 Nr. 1 BauNVO)?","Mitnutzung der öffentlichen Parkfläche oder Höhe der Ablöse?","Dürfen Terrasse und Wintergarten in den 10-m-Streifen West (Baugrenze) und zählen sie zur GRZ II?","Kaufpreis 230 €/m² und Reservierung bis zur Finanzierungszusage?"]
for i,q in enumerate(qs):
    y=1.9+i*0.67; rect(sl,0.7,y,0.46,0.46,GREEN,shape=MSO_SHAPE.OVAL); tx(sl,0.7,y,0.46,0.46,str(i+1),size=15,color=WHITE,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,font=HF); tx(sl,1.45,y+0.07,11,0.5,q,size=15)
tx(sl,0.7,6.65,11.9,0.3,"Die vollständige Fragenliste (34 Punkte) liegt separat als Word-Datei vor.",size=10,color=GREY)
# 13 KfW
sl=page(d,SEC[2],f"Die KfW gibt günstige Kredite für {1982000/Z['gesamt']*100:.0f} % der Kosten, aber nur mit Bedingungen","Zinsen sind Annahmen (Quellen nennen 0,6 % bis 3,05 %). Rahmen laut Ratgebern, im aktuellen Merkblatt zu prüfen.")
for x,t,v,rows_ in ((0.7,"KfW 298 · Wohnungen","1.200.000 €",[("Rahmen","150.000 € je Wohnung (mit QNG)"),("Anzahl","8 Wohnungen"),("Zins (Annahme)","2,5 %, 10 Jahre fest")]),(6.9,"KfW 299 · Gastro","782.000 €",[("Rahmen","2.000 € je m² Nettogrundfläche (mit QNG)"),("Fläche","460 m² × 85 % = 391 m²"),("Zins (Annahme)","3,0 %, 10 Jahre fest")])):
    rect(sl,x,1.95,5.7,3.4,LIGHT,shape=MSO_SHAPE.ROUNDED_RECTANGLE); tx(sl,x+0.35,2.15,5,0.4,t,size=15,color=GREEN,bold=True); tx(sl,x+0.35,2.6,5,0.8,v,size=36,color=GREEN,font=HF)
    for i,(a,b) in enumerate(rows_): tx(sl,x+0.35,3.65+i*0.5,1.7,0.4,a,size=12,color=GREY); tx(sl,x+2.05,3.65+i*0.5,3.5,0.4,b,size=13)
tx(sl,0.7,5.65,11.9,0.9,[{"t":[("Zusammen 1,98 Mio. €, ",{"bold":True,"color":GREEN}),(f"der Rest von {num(Z['hb']/1e6,2)} Mio. € kommt von der Hausbank (4,0 %). Eigenkapital: 0 € (die Bank wird mehr verlangen, siehe Folie Wert und Beleihung).",{})]}],size=16)
# 14 QNG
sl=page(d,SEC[2],"QNG: das Siegel, das den höheren Kreditrahmen freischaltet")
cols_=[("Was ist das?","Qualitätssiegel Nachhaltiges Gebäude: ein staatliches Siegel für Gebäude, die mehr als nur Energie sparen."),("Was wird geprüft?","Ökobilanz (Treibhausgase, Primärenergie), Schadstoffe in Baustoffen, nachhaltige Materialien wie zertifiziertes Holz. Prüfung durch eine zugelassene Stelle."),("Was bringt es uns?","Mehr günstiges Darlehen: 8 × 50.000 € = 400.000 € bei den Wohnungen und rund 195.000 € bei der Gastro.")]
for i,(a,b) in enumerate(cols_):
    x=0.7+i*4.1; rect(sl,x,1.95,3.8,0.06,GOLD); tx(sl,x,2.2,3.7,0.4,a,size=18,color=GREEN,font=HF); tx(sl,x,2.8,3.7,2.5,b,size=14)
rect(sl,0.7,5.35,11.93,1.1,LIGHT); tx(sl,1.0,5.5,11.3,0.9,[{"t":[("Für uns heißt das: ",{"bold":True,"color":GREEN}),(f"Energie- und Nachhaltigkeitsberater von Anfang an einbinden. Im Modell sind 4 % Mehrkosten ({eur(Z['eh_k'])}) für Effizienzhaus 40 und QNG eingerechnet. Der Holzbau im Staffelgeschoss hilft (Annahme). Grenzwerte im QNG-Handbuch prüfen.",{})]}],size=13)
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
