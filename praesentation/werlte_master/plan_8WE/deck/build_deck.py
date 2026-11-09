import sys, copy
sys.path.insert(0,"/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/einzel")
from model import model, sens, BASE
from einheiten import units, P as UP
from lib import *
from pptx import Presentation
from pptx.chart.data import CategoryChartData
SRC="/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/Neue-Mitte-Werlte_Baufeld3_8-Wohnungen_Grosse-Gastro-EG_Rev-GRZ-II.pptx"
OUT="/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/deck/Neue-Mitte-Werlte_Baufeld3_8-Wohnungen_Gastro-EG_Einzelrechnung_2026-11.pptx"
ZB,ZH=1450.0,700.0
Z=model(bau=ZB,holz=ZH); B=model()
def unitcalc(**kw):
    m=model(**kw); p=dict(UP); p.update(bau=m["bau"] if False else kw.get("bau",2200.0),holz=kw.get("holz",400.0),fin=m["fin"],z298=m["z298"],z299=m["z299"],zbank=m["zb"],bnk=m["bnk"],eh=m["eh"])
    u,_=units(p)
    for x in u:
        z=p["z299"] if x["typ"]=="Gastro" else p["z298"]
        x["zins"]=x["kfw"]*z+x["bank"]*p["zbank"]; x["tilg"]=(x["kfw"]+x["bank"])*p["til"]; x["plus"]=x["netto"]-x["zins"]-x["tilg"]
    return m,u
mz,UZ=unitcalc(bau=ZB,holz=ZH)
we15=UZ[0]; we68=UZ[5]; gas=UZ[8]; WEs=UZ[:8]
prs=Presentation(SRC); sl=list(prs.slides)
sh={i:list(s.shapes) for i,s in enumerate(sl,1)}
# ---- Klone vor Änderung ----
cl_cards=dup(prs,sl[23])      # Karten-Vorlage (Slide 24)
cl={k:dup(prs,sl[23]) for k in ("gbr","qng","kfwb","zins")}
cl["einzel"]=dup(prs,sl[11]); cl["bsp"]=dup(prs,sl[20]); cl["gas2"]=dup(prs,sl[20]); cl["szen"]=dup(prs,sl[21]); cl["quellen"]=dup(prs,sl[30])
# entferne die überzählige Karten-Dublette
prs.slides._sldIdLst.remove(list(prs.slides._sldIdLst)[len(sl)]); 
def title(s,t,zg=None):
    L=list(s.shapes); T(L[0],t)
    if zg: T(L[1],zg)
# ---- 1 Titel ----
S=sh[1]; T(S[3],"Businessplan für die Bank: Konzept, KfW-Finanzierung, Einzelrechnung je Wohnung und Gastro, Ertrag und Abzahlungsplan")
T(S[4],"Bessam Hasso, Werlte","Bebauungsplan Nr. 123 (Plan 2023, rechtskräftig)","Stand November 2026 · Entwurf, alle Werte Annahmen")
# ---- 2 Auf einen Blick ----
S=sh[2]; haus_plus=(Z["netto_imm"]-Z["kd_j"])/12
T(S[3],num(Z["gesamt"]/1e6,2)+" Mio. €"); T(S[4],"Gesamtkosten inkl. Finanzierung (Zielpreis 1.450 € je m² BGF)")
T(S[6],f"{(1200000+782000)/Z['gesamt']*100:.0f} %"); T(S[7],"des Darlehens über KfW 298 und 299 (1,98 Mio. €)")
T(S[9],eur(Z["kd_m"])); T(S[10],f"Kapitaldienst pro Monat (Mischzins {pct(Z['mischzins'],2)}, 1 % Tilgung)")
T(S[12],eur(haus_plus,0,True)); T(S[13],"Plus pro Monat im Haus nach Kapitaldienst, ohne Gastro-Betrieb")
table_set(S[14],[["Projekt","Wert"],
 ["Grundstück / Grundfläche / BGF","960 m² / 540 m² (GRZ 0,6 erlaubt max. 576 m²) / 1.540 m² (EG, 1. OG, Staffel)"],
 ["Nutzung","Gastro im ganzen EG (460 m², ca. 150 Plätze), im 1. OG 5 Wohnungen (je 83 m²), im Staffelgeschoss in Holzbau 3 Wohnungen (je 103 m²)"],
 ["Finanzierung","100 % Fremdkapital, kein Eigenkapital, KfW 298/299 plus Hausbank"],
 ["Kapitaldienstdeckung (DSCR)",f"{f2(Z['dscr_ges'])} gesamt, {f2(Z['dscr_imm'])} nur Immobilie (Miete und Pacht)"],
 ["Ertragswert / Beleihungsauslauf",f"{num(Z['ew']/1e6,2)} Mio. € / {Z['auslauf']*100:.0f} % (Darlehen zu Beleihungswert)"]])
T(S[15],f"Die Mieten und die Pacht tragen die Raten allein (Faktor {f2(Z['dscr_imm'])} ohne Gastro-Gewinn), wenn der Zielpreis von 1.450 € je m² BGF erreicht wird. Der Zielpreis ist noch durch Angebote zu belegen; bei 2.200 € je m² (Bankunterlagen 19.10.2026) liegt der Faktor bei {f2(B['dscr_imm'])}, siehe Folie Szenarien.")
# ---- 4 B-Plan ----
S=sh[4]; t=S[2].table
cell(t.cell(1,1),"0,6 → max. 576 m² für Gebäude (GRZ I); Stellplätze, Zufahrten, Nebenanlagen zählen zur GRZ II (§ 19 Abs. 4 BauNVO): bis 0,8 = 768 m²")
cell(t.cell(1,2),"540 m² Gebäude (56 %); Stellplätze und Zufahrt zusätzlich bis ca. 228 m² (GRZ II), mit wasserdurchlässigem Stein")
cell(t.cell(5,2),"540 m² Grundfläche, Lage im Baufenster noch zu prüfen")
cell(t.cell(6,2),"ca. 8–10 in der GRZ II (228 m²); mehr mit Ausnahme (wasserdurchlässig)")
T(S[4],"Schriftlich klären: Ist Baufeld 3 tatsächlich MI 3 / Flurstück 59/1 (Plan 2023, rechtskräftig; die 1. Änderung ist nur Entwurf und erfasst MI 3 nicht)? Sind 540 m² Grundfläche zulässig (das Baufenster ist nach meiner Schätzung kleiner)? Sind Staffelgeschoss und Flachdach zulässig oder befreibar? Dürfen Stellplätze und Zufahrten mit wasserdurchlässigem Stein über die GRZ II von 0,8 hinausgehen (§ 19 Abs. 4 Satz 4 Nr. 1 BauNVO)? Das Staffelgeschoss ist als Nicht-Vollgeschoss zu bestätigen.")
# ---- 5 Staffel ----
S=sh[5]; T(S[3],"460 m²"); T(S[4],"Staffelgeschoss in Holzbau (BGF), nur 0,8 m rundum zurückgesetzt, kein Vollgeschoss")
T(S[6],eur(460*ZH)); T(S[7],"Ersparnis gegenüber Massivbau (700 € je m², Annahme, Zimmerei-Angebot nötig)")
T(S[9],"72 m²"); T(S[10],"schmale Dachterrasse rundum (ca. 0,8 m), nicht Teil der BGF")
T(S[12],"Leichter und schneller: weniger Last auf dem Klinker-Geschoss, kürzere Bauzeit.","Zwei Partner aus dem Bekanntenkreis (Bauunternehmen unten, Zimmerei oben) können Preise und Termine gemeinsam angeben.","Holzbau hilft beim QNG-Nachweis und beim Effizienzhaus-40-Standard (KfW-Voraussetzung).","Brandschutz (Holzbau bis Gebäudeklasse 4, Aufzug und Treppenhaus massiv) und Schallschutz muss der Architekt nachweisen.")
# ---- 6 Geschosse ----
S=sh[6]; T(S[9],"1. OG · 5 Wohnungen"); T(S[10],"Staffelgeschoss · 3 Wohnungen")
table_set(S[17],[["Ebene","Nutzung","BGF"],["EG","Gastro 460 m² mit Bar, Séparée und Küche, dazu Treppenhaus, Aufzug, Eingänge","540 m²"],["1. OG","5 Wohnungen à ca. 83 m²","540 m²"],["Staffel","3 Wohnungen à ca. 103 m², Holzbau, schmale Terrasse rundum","460 m²"],["Summe","8 Wohnungen (725 m²), Gastro 460 m²","1.540 m²"]])
T(S[18],"BGF = Bruttogrundfläche, alle Geschossflächen zusammen. Das Staffelgeschoss in Holzbau springt rundum nur ca. 0,8 m zurück, so entsteht eine schmale Terrasse von ca. 72 m² um die Wohnungen. Höhenangaben sind Annahmen.")
# ---- 7 Skizzen ----
S=sh[7]
T(S[8],"Gastraum und Lounge","ca. 130 Plätze"); T(S[12],"Séparée","20 Plätze")
for i in (23,24,25,26): delshape(S[i])
for (a,b),n in zip(((27,28),(29,30),(31,32)),(1,2,3)): pass
left0,w5=5.18,3.46/5
def place(sh_,x,w): sh_.left=Emu(int(x*914400)); sh_.width=Emu(int(w*914400))
newpairs=[]
for k,(a,b) in enumerate(((27,28),(29,30),(31,32))):
    place(S[a],left0+k*w5,w5); place(S[b],left0+k*w5,w5)
for k in (3,4):
    ea=copy.deepcopy(S[31]._element); eb=copy.deepcopy(S[32]._element)
    S[32]._element.addnext(ea); ea.addnext(eb)
sl7=list(sl[6].shapes)
# Neue Shapes finden: nach Namen
og=[x for x in sl7 if x.name.startswith("Raum WE") and abs(x.top/914400-2.3)<0.01]
og_t=[x for x in sl7 if x.has_text_frame and x.text_frame.text.startswith("WE") and abs(x.top/914400-2.3)<0.01]
og.sort(key=lambda x:x.left); og_t.sort(key=lambda x:x.left)
# Der geklonte Satz hat identische Position -> neu verteilen
cands=[x for x in sl7 if abs(x.top/914400-2.3)<0.01 and x.left/914400>5.1]
cands.sort(key=lambda x:(round(x.left/914400,2)))
shapes_og=[x for x in cands if x.name.startswith("Raum")]; texts_og=[x for x in cands if not x.name.startswith("Raum")]
for k,x in enumerate(shapes_og): place(x,left0+k*w5,w5); 
for k,x in enumerate(texts_og): place(x,left0+k*w5,w5)
for k,x in enumerate(texts_og): T(x,f"WE {k+1}",f"{we15['nf']:.0f} m²")
for i in (44,45,46,47): delshape(S[i])
w3=(12.63-9.29)/3
for k,(a,b) in enumerate(((38,39),(40,41),(42,43))):
    place(S[a],9.29+k*w3,w3); place(S[b],9.29+k*w3,w3); T(S[b],f"WE {6+k}",f"{we68['nf']:.0f} m²")
T(S[49],"Grundfläche 540 m² (GRZ-Maximum 576 m²). Die Gastro nutzt das ganze EG (460 m²), Treppenhaus und Aufzug liegen am Westende und erschließen die Wohnungen getrennt von der Gastro. Im 1. OG liegen 5 Wohnungen, die Staffel in Holzbau hat 460 m² BGF mit 3 Wohnungen, die beige Fläche ist die schmale Terrasse (ca. 72 m²).")
# ---- 9, 10 ----
T(sh[9][4],"ca. 150 Plätze"); T(sh[9][5],"innen (130 im Gastraum, 20 im Séparée), plus ca. 40 auf der Terrasse"); T(sh[9][7],"10 Barhocker, Polsterbänke, Backbar")
T(sh[10][7],"KI-generierte Visualisierungen zur Orientierung, Gestalt und Materialien. Fassadenteilung und Länge weichen im Detail von den Skizzen ab, Maße folgen mit dem Architekten.")
# ---- 11 Stellplätze ----
S=sh[11]
cd=CategoryChartData(); cd.categories=["Bedarf (Annahme)","Platz in GRZ II","Mit Ausnahme (wasserdurchlässig)"]; cd.add_series("Stellplätze",[41,8,12]); S[2].chart.replace_data(cd)
T(S[4],"Bedarf ca. 41 Stellplätze (Annahme: ca. 33 für die Gastro laut Gastro-Konzept, plus 1 je Wohnung; Satzung der Stadt maßgeblich). Die 540 m² Gebäude liegen unter der GRZ I von 0,6 (576 m²); Stellplätze und Zufahrten zählen zur GRZ II (bis 0,8, also ca. 228 m² zusätzlich): dort passen ca. 8 Plätze.","Mit wasserdurchlässigem Stein (keine versiegelte Fläche) Ausnahme beantragen: gesamte Restfläche (ca. 420 m²) nutzbar, hochgerechnet ca. 12 Plätze.","Restplätze auf der öffentlichen Parkfläche nebenan per Vereinbarung nutzen, besonders am Abend; alternativ Ablöse (Höhe nennt die Stadt).","Klären, ob der 10 m breite Grünstreifen teils befestigt werden darf.")
# ---- 12 Flächen und Mieten ----
S=sh[12]; T(S[0],"Flächen und Mieten: Wohnungen und Gastro")
rows=[["Einheit","Geschoss","Fläche","Miete je m²","Kaltmiete / Monat","Kaltmiete / Jahr"]]
for x in WEs: rows.append([x["name"],x["geschoss"],num(x["nf"],1)+" m²","11,18 €",eur(x["rent"]/12),eur(x["rent"])])
rows+= [["Summe Wohnen","","725,0 m²","",eur(Z["miete_j"]/12),eur(Z["miete_j"])],["Gastro (Pacht 12 €/m²)","EG","460,0 m²","12,00 €",eur(Z["pacht_j"]/12),eur(Z["pacht_j"])],["Rohertrag gesamt","","","",eur(Z["roh"]/12),eur(Z["roh"])]]
table_set(S[2],rows,remove=(12,13))
# ---- 13 Gastro ----
S=sh[13]; T(S[0],"Gastro: Flächen, Plätze und Pacht")
table_set(S[2],[["Gastro-Flächenbedarf","Menge","Fläche"],["Gastraum mit Tischen und Gängen","ca. 80 Plätze","280 m²"],["Lounge in der Ecke","14 Plätze","35 m²"],["Bar und Backbar","10 Barhocker","30 m²"],["Séparée (Feiern)","20 Plätze","34 m²"],["Küche, Lager, WC, Eingang","–","80 m²"],["Gastro gesamt (ca. 150 Plätze)","","460 m²"]],remove=(2,))
pn=Z["pacht_j"]*0.9
table_set(S[3],[["Pacht der Gastro (an das Haus)","Fläche","Pacht / m²","Pacht / Jahr"],["Gastro im EG, Pacht an das Haus","460 m²","12,00 €",eur(Z["pacht_j"])],["Rücklage 10 %","","",eur(-Z["pacht_j"]*0.1)],["Netto-Pacht für den Kapitaldienst","460 m²","10,80 €",eur(pn)]])
T(S[5],f"Pacht: Die Gastro-Pacht von {eur(Z['pacht_j'])} im Jahr (nach Rücklage {eur(pn)}) deckt {pn/Z['kd_j']*100:.0f} % des Kapitaldienstes, die Wohnungen ({eur(Z['miete_j']*0.9)} netto) {Z['miete_j']*0.9/Z['kd_j']*100:.0f} %. Zusammen {Z['dscr_imm']*100:.0f} %: Die Immobilie trägt die Raten ohne Gastro-Gewinn.","Gastro: 150 Plätze auf 460 m² (3,1 m² je Platz), Pacht 12 €/m² (Annahme, ohne Marktdaten).")
T(S[6],"Das EG gehört ganz der Gastro, Treppenhaus und Aufzug liegen am Westende und erschließen die Wohnungen getrennt von der Gastro. Die Grundfläche beträgt 540 m².")
# ---- 14 KfW ----
S=sh[14]; T(S[0],"KfW-Kredite 298 und 299")
table_set(S[2],[["Programm","Wofür","Rahmen (mit QNG)","Im Projekt","Zins (Annahme)"],["KfW 298 Klimafreundlicher Neubau","vermietete Wohnungen","bis 150.000 € je Wohnung",eur(1200000),pct(Z["z298"],2)],["KfW 299 Klimafreundlicher Neubau","Gastro (Nichtwohngebäude)","bis 2.000 € je m² Nettogrundfläche",eur(782000),pct(Z["z299"],2)],["Hausbank (Rest)","Restfinanzierung inkl. Bauzeitzinsen","–",eur(Z["hb"]),pct(Z["zb"],2)]],remove=(1,))
T(S[4],"Voraussetzungen: Effizienzhaus 40 (Gastro: Effizienzgebäude 40), QNG-Zertifikat für den vollen Rahmen, Heizung ohne fossile Brennstoffe (z. B. Wärmepumpe), Energieeffizienz-Experte, Antrag vor Baubeginn über die Hausbank.",f"Gemischte Nutzung: Wohnteil (298) und Gastro (299) werden getrennt gefördert. Kreditrahmen insgesamt 1.982.000 €, das sind {1982000/Z['gesamt']*100:.0f} % des Darlehens. Die KfW-Zinsen schwanken in den Quellen zwischen 0,6 % und 3,05 %. Mehrkosten für den Standard angenommen mit 3 % ({eur(Z['eh_k'])}).")
# ---- 15 Gesamtkosten ----
S=sh[15]; bau_net=Z["bau_roh"]+Z["abschlag"]+Z["terr_k"]
table_set(S[2],[["Posten","Rechnung","Betrag","Anteil"],
 ["Grundstück inkl. Steuer und Notar","960 m² × 230 € + ca. 7 %",eur(Z["grund"]),pct(Z["grund"]/Z["gesamt"],0)],
 ["Bau, Massivbau","1.540 m² × 1.450 € (Zielpreis)",eur(Z["bau_roh"]),pct(Z["bau_roh"]/Z["gesamt"],0)],
 ["Abschlag Holzbau (Staffelgeschoss)","460 m² × 700 € günstiger",eur(Z["abschlag"]),pct(Z["abschlag"]/Z["gesamt"],0)],
 ["Dachterrasse rundum (schmal)","72 m² × 450 €",eur(Z["terr_k"]),pct(Z["terr_k"]/Z["gesamt"],0)],
 ["Baunebenkosten (Architekt, Statik, Gebühren)","15 % vom Bau",eur(Z["bnk_k"]),pct(Z["bnk_k"]/Z["gesamt"],0)],
 ["Mehrkosten Effizienzhaus 40 und QNG","3 % auf Bau inkl. Nebenkosten",eur(Z["eh_k"]),pct(Z["eh_k"]/Z["gesamt"],0)],
 ["Ausbau Gastro (ca. 150 Plätze)","Annahme Bauherr, Angebote nötig",eur(150000),pct(150000/Z["gesamt"],0)],
 ["Finanzierungskosten (Bauzeit, Bereitstellung, Anlaufzeit)","27 Monate",eur(Z["fin"]),pct(Z["fin"]/Z["gesamt"],0)],
 ["Gesamtkosten","",eur(Z["gesamt"]),"100 %"]])
cd=CategoryChartData(); cd.categories=["Grundstück","Bau","Baunebenkosten und Standard","Gastro-Ausbau","Finanzierung"]
cd.add_series("Kosten",[Z["grund"],bau_net,Z["bnk_k"]+Z["eh_k"],150000,Z["fin"]]); S[3].chart.replace_data(cd)
T(S[4],f"Das sind ca. {num(Z['gesamt']/1540)} € pro m² BGF (bei 2.200 € Bau: {num(B['gesamt']/1540)} €).")
# ---- 16 Finanzierungsplan ----
S=sh[16]
table_set(S[2],[["Mittelherkunft","Betrag","Anteil","Zins"],["KfW 298 (vermietete Wohnungen)",eur(1200000),pct(1200000/Z["gesamt"],0),pct(Z["z298"],2)],["KfW 299 (Nichtwohngebäude: Gastro)",eur(782000),pct(782000/Z["gesamt"],0),pct(Z["z299"],2)],["Hausbank-Darlehen",eur(Z["hb"]),pct(Z["hb"]/Z["gesamt"],0),pct(Z["zb"],2)],["Eigenkapital","–","–",""],["Summe Finanzierung",eur(Z["gesamt"]),"100 %",""]],remove=(1,))
T(S[4],"Mischzins",f"{pct(Z['mischzins'],2)} über alle Darlehen."," ","Bau- und Anlaufzeit",f"15 Monate Bau und 12 Monate Anlaufzeit kosten {eur(Z['fin'])} an Zinsen und Bereitstellungsgebühr, finanziert von der Hausbank."," ","Danach",f"Rate {eur(Z['kd_m'])} pro Monat (Zins plus 1 % Anfangstilgung).")
T(S[5],f"Die Kosten von {eur(Z['gesamt'])} sind komplett durch Fremdkapital gedeckt.")
# ---- 17 Zinsberechnung ----
S=sh[17]; (l1,z1),(l2,z2),(l3,z3)=Z["loans"]
table_set(S[2],[["Darlehen","Betrag bei Rate-Start","Zins","Tilgung","Rate / Monat","Rate / Jahr"],
 ["KfW Wohnen (298)",eur(l1),pct(z1,2),"1,00 %",eur(l1*(z1+.01)/12),eur(l1*(z1+.01))],
 ["KfW Gastro (299)",eur(l2),pct(z2,2),"1,00 %",eur(l2*(z2+.01)/12),eur(l2*(z2+.01))],
 ["Hausbank",eur(l3),pct(z3,2),"1,00 %",eur(l3*(z3+.01)/12),eur(l3*(z3+.01))],
 ["Summe",eur(Z["gesamt"]),pct(Z["mischzins"],2),"",eur(Z["kd_m"]),eur(Z["kd_j"])]])
h=Z["tilg"]; T(S[3],f"Im ersten Jahr nach der Anlaufzeit zahlst du {eur(h[0][1])} Zinsen und {eur(h[0][2])} Tilgung.",f"Zinsänderung nach 10 Jahren: +1 Prozentpunkt auf die Restschuld kostet ca. {eur(Z['rest10']*0.01/12)} pro Monat mehr.")
# ---- 18 Abzahlungsplan ----
S=sh[18]; cd=CategoryChartData(); cd.categories=[str(y) for y,_,_,_ in h]; cd.add_series("Restschuld",[round(r) for _,_,_,r in h]); S[2].chart.replace_data(cd)
yrs=[1,2,3,5,10,15,20,25,30,35]; lab={10:"10 (Ende Zinsbindung)"}
table_set(S[3],[["Jahr","Zinsen","Tilgung","Restschuld"]]+[[lab.get(y,str(y)),eur(h[y-1][1]),eur(h[y-1][2]),eur(h[y-1][3])] for y in yrs])
T(S[4],f"Nach 10 Jahren Zinsbindung beträgt die Restschuld {eur(Z['rest10'])}. Die Anschlussfinanzierung muss eingeplant werden.")
# ---- 19 Ertrag ----
S=sh[19]; ex=Z["erg"]
table_set(S[2],[["Position","pro Monat","pro Jahr"],
 ["Kaltmiete Wohnen (8 Wohnungen)",eur(Z["miete_j"]/12,0,True),eur(Z["miete_j"],0,True)],
 ["Pacht Gastro (460 m² × 12 €)",eur(Z["pacht_j"]/12,0,True),eur(Z["pacht_j"],0,True)],
 ["Rücklagen (10 % von Miete und Pacht)",eur(-Z["rueck"]/12),eur(-Z["rueck"])],
 ["Nettoertrag Immobilie",eur(Z["netto_imm"]/12,0,True),eur(Z["netto_imm"],0,True)],
 ["Betriebsergebnis Gastro nach Pacht",eur(Z["betrieb"]/12,0,True),eur(Z["betrieb"],0,True)],
 ["Nettoertrag vor Kapitaldienst",eur(Z["netto_ges"]/12,0,True),eur(Z["netto_ges"],0,True)],
 ["Kapitaldienst (Zinsen und Tilgung)",eur(-Z["kd_m"]),eur(-Z["kd_j"])],
 ["Ergebnis nach Kapitaldienst",eur(ex/12,0,True),eur(ex,0,True)]],remove=())
T(S[4],"Kapitaldienstdeckung (DSCR)",f"Gesamt {f2(Z['dscr_ges'])}, nur Immobilie {f2(Z['dscr_imm'])}, nur Wohnen {f2(Z['dscr_wohn'])}. Banken verlangen meist mindestens 1,2."," ","Zinsdeckung",f"{f2(Z['zinsdeckung'])}."," ","Anfangsrendite",f"{pct(Z['rendite'],2)} auf die Gesamtkosten (Nettoertrag Immobilie).")
T(S[5],f"Die Immobilie deckt die Raten allein: Plus im Haus {eur(haus_plus,0,True)} pro Monat ohne den Gastro-Gewinn. Voraussetzung ist der Zielpreis; der Pachtvertrag mit einem tragfähigen Betreiber bleibt für die Bank entscheidend.")
# ---- 20 Gastro Umsatz ----
S=sh[20]; mg=Z["marge"]; pj=Z["pacht_j"]/12
table_set(S[2],[["Umsatz pro Monat","Gewinn vor Pacht","Gewinn nach Pacht"]]+[[eur(u),eur(u*mg),eur(u*mg-pj,0,True)] for u in (30000,40000,50000,60000,70000)])
T(S[4],"Betrieb allein",f"Ab ca. {num(round(pj/mg,-2))} € Umsatz deckt der Betrieb seine Pacht."," ","Haus insgesamt",f"Ab ca. {num(round(Z["be_umsatz"],-2))} € Umsatz sind alle Raten bezahlt (Betreiber = Bauherr).")
T(S[5],f"Der Umsatz von 50.000 € entspricht ca. {num(50000*12/150)} € je Sitzplatz und Jahr (150 Plätze), das ist für 460 m² vorsichtig.")
# ---- 21 Ertragswert ----
S=sh[21]
table_set(S[2],[["Ertragswert","Betrag"],["Rohertrag pro Jahr (Mieten und Pacht)",eur(Z["roh"])],["Bewirtschaftungskosten",eur(-Z["bew"])],["Reinertrag",eur(Z["rein"])],["Bodenwert (960 m² × 230 €)",eur(Z["boden"])],[f"Gebäudeertragswert (Vervielfältiger {num(Z['vf'],1)})",eur(Z["ew_geb"])],["Ertragswert gesamt",eur(Z["ew"])],["davon Wohnen / Gastro",f"{num(Z['ew']*Z['miete_j']/Z['roh']/1e6,2)} / {num(Z['ew']*Z['pacht_j']/Z['roh']/1e6,2)} Mio. €"]])
table_set(S[3],[["Beleihung","Betrag"],["Sachwert (Boden + Herstellungskosten)",eur(Z["sach"])],["Beleihungswert (niedrigerer Wert, −10 %)",eur(Z["bel"])],["Gesamtkosten und Darlehen",eur(Z["gesamt"])],["Beleihungsauslauf",f"{Z['auslauf']*100:.0f} %"],["Ertragswert minus Gesamtkosten",eur(Z["ew_luecke"],0,True)],["Betrag über 80 % Auslauf",eur(Z["ek80"])]])
T(S[4],f"Einordnung: Die Mieten und die Pacht tragen einen Wert von {num(Z['ew']/1e6,2)} Mio. €, die Kosten liegen bei {num(Z['gesamt']/1e6,2)} Mio. €. Eine Bank beleiht üblicherweise nur bis ca. 80 % des Beleihungswerts. Für den Rest braucht es zusätzliche Sicherheiten (Grundschulden auf weitere Immobilien, Bürgschaft) oder Eigenkapital in Höhe von ca. {num(Z['ek80']/1e6,2)} Mio. €. Die KfW-Darlehen allein liegen bei {Z['auslauf_kfw']*100:.0f} % Auslauf.")
# ---- 22 Prognose / Belastungstest ----
S=sh[22]; pg={r[0]:r for r in Z["prog"]}
yy=[1,3,5,7,10]
table_set(S[2],[["Jahr"]+[str(y) for y in yy],["Nettoertrag vor Kapitaldienst"]+[eur(pg[y][5]+Z["betrieb"]*0+0) if False else eur(pg[y][5]) for y in yy],["Kapitaldienst"]+[eur(-Z["kd_j"])]*5,["Ergebnis nach Kapitaldienst"]+[eur(pg[y][6],0,True) for y in yy],["DSCR"]+[f2(pg[y][7]) for y in yy],["Restschuld Jahresende"]+[eur(pg[y][8]) for y in yy]])
ss=sens(Z); base=ss[0][1]
one_we=we15["netto"]/12
ss2=[s for s in ss if not s[0].startswith("Gastro fällt")]; gf=[s for s in ss if s[0].startswith("Gastro fällt")][0]
leer=("Eine Wohnung im 1. OG dauerhaft leer",base-one_we,(Z["netto_ges"]-we15["netto"])/Z["kd_j"])
rows=[["Belastungstest (pro Monat)","Ergebnis","DSCR","zum Plan"]]
for nme,e,d in ss2+[leer,gf]: rows.append([nme,eur(e,0,True),f2(d),"" if nme=="Plan" else eur(e-base,0,True)])
table_set(S[3],rows)
# ---- 23 Airbnb ----
S=sh[23]
table_set(S[2],[["Zwei Apartments à ...","45 m²","60 m²","83 m²"],["Preis pro Nacht","80 €","95 €","115 €"],["Netto Airbnb je Apartment und Monat","535 €","636 €","770 €"],["Netto langfristige Miete je Apartment und Monat","453 €","604 €","835 €"],["Möblierung (im Kredit)","27.000 €","36.000 €","49.800 €"],["Mehrertrag für 2 Apartments pro Monat","−60 €","−236 €","−546 €"]])
# ---- 24 Risiken ----
S=sh[24]
T(S[4],f"Beleihungsauslauf {Z['auslauf']*100:.0f} % bei 100 % Fremdfinanzierung. Gegenmaßnahme: Grundschulden auf weitere Immobilien, Bürgschaft oder Eigenkapital, Pachtvertrag mit Bonitätsnachweis.")
T(S[7],f"Die Immobilie trägt die Raten auch ohne Gastro-Gewinn (Faktor {f2(Z['dscr_imm'])}). Fällt die Gastro ganz aus, fehlen im Monat ca. {eur((Z['pacht_j']*0.9+Z['betrieb'])/12)} Pacht und Betriebsergebnis; Faktor dann {f2(gf[2])}. Gegenmaßnahme: Konzept, erfahrener Betreiber, Pachtstaffel, Mietverträge mit Bonitätsprüfung.")
T(S[10],"Der Zielpreis von 1.450 € je m² BGF ist noch nicht durch Angebote belegt; bei 1.800 € trägt das 1. OG die Raten nicht allein. KfW-Zinsen und Rahmen sind Stand Nov. 2026 unsicher. Gegenmaßnahme: Angebote einholen, KfW-Zusage vor Baubeginn, Forward-Darlehen.")
T(S[13],"540 m² Grundfläche, Staffelgeschoss (Nicht-Vollgeschoss) und Flachdach müssen bestätigt werden, KfW verlangt Effizienzhaus 40 mit QNG. Gegenmaßnahme: Vorabstimmung, Energieeffizienz-Experte früh einbinden.")
T(S[9],"Preise und Zins")
# ---- 25 Was ich brauche ----
S=sh[25]
T(S[4],"540 m² Grundfläche, Staffelgeschoss als Nicht-Vollgeschoss, Flachdach und Höhe schriftlich bestätigen")
T(S[13],f"Finanzierung von {num(Z['gesamt']/1e6,2)} Mio. € mit KfW 298/299 und tilgungsfreier Anlaufzeit von 12 Monaten")
T(S[19],"Antrag für 298 und 299 vor Baubeginn über die Hausbank")
# ---- 26 Nächste Schritte ----
S=sh[26]
T(S[4],"Nov 2026"); T(S[5],"Termin Bürgermeister 09.11.: Stellplätze, Baufenster, Staffelgeschoss, Fragenliste")
T(S[8],"Nov bis Dez 2026"); T(S[9],"Angebote für Rohbau, Zimmerei, Ausbau, Maler: Zielpreis 1.450 € je m² belegen")
T(S[12],"Dez 2026"); T(S[13],"Hausbank: KfW 298/299, Zinsen, Sicherheiten; Steuerberater: Umsatzsteuer, GbR/UG")
T(S[16],"Q1 2027"); T(S[17],"Architekt, Energieberater (QNG), Bauantrag, KfW-Antrag vor Baubeginn")
# ---- 27 Anhang ----
T(sh[27][1],"Annahmen, Gastro-Kosten, Gastro-Ausbau, Mietdaten, Quellen")
# ---- 28 Annahmen ----
S=sh[28]
T(S[2],"Grundstück 960 m² × 230 € plus ca. 7 % (5 % Grunderwerbsteuer, ca. 2 % Notar)","Bau 1.540 m² BGF × 1.450 € (Zielpreis, Basis Bankunterlagen 2.200 €), Staffel (460 m²) in Holzbau 700 €/m² günstiger, Terrasse 72 m² × 450 €, Baunebenkosten 15 %","100 % Fremdfinanzierung, 1 % Anfangstilgung, tilgungsfreie Anlaufzeit 12 Monate","Bauzeit 15 Monate, Bereitstellungszins 3 % p. a. ab Monat 7","Zins KfW 298 2,5 %, KfW 299 3,0 %, Hausbank 4,0 % (Annahmen)")
T(S[3],"Gastro-Umsatz 50.000 € netto, Marge vor Pacht 30,5 %","8 Wohnungen (725 m²) zu 11,18 €/m² Kaltmiete, Gastro-Pacht 12 €/m² auf 460 m²","Lohn des Bauherrn wird vorerst nicht gerechnet, Rücklagen 10 % der Miete und Pacht","KfW-Kredite statt Zuschuss, Antrag vor Baubeginn; Mehrkosten Effizienzhaus 40 und QNG 3 %","Nebenkosten werden auf die Mieter umgelegt, die Hausverwaltung deckt die Rücklage","Offen: Baufenster, Staffelgeschoss, Höhen, Stellplatzsatzung, Zins nach 10 Jahren, Sicherheiten, Steuer (Umsatzsteuer-Option, AfA)")
# ---- 29 Gastro Kosten ----
S=sh[29]; T(S[0],"Gastro: Kosten pro Monat bei 50.000 € Umsatz")
posten=[("Wareneinsatz (Einkauf Essen und Getränke)","ca. 28 %",14000),("Personal (ohne Chef-Lohn)","ca. 30 %",15000),("Pacht ans Haus (460 m² × 12 €)","",5520),("Energie, Wasser, Müll","ca. 3 %",1500),("Reinigung, Wäsche, Verbrauchsmaterial","ca. 2 %",1000),("Werbung und Marketing","ca. 1,5 %",750),("Reparaturen, Wartung, Kassensystem","ca. 1,5 %",750),("Sonstiges","ca. 1,5 %",750),("Versicherungen, GEMA, Gebühren","ca. 1 %",500),("Steuerberater, Buchhaltung","ca. 1 %",500)]
tot=sum(x[2] for x in posten)
table_set(S[2],[["Posten","Richtwert","Betrag"]]+[[a,b,eur(c)] for a,b,c in posten]+[["Summe Kosten","",eur(tot)],["Gewinn nach Pacht, vor Lohn","",eur(50000-tot)]])
# ---- 30 Gastro Ausbau ----
S=sh[30]
ausb=[("Küche (Herd, Kühlräume, Edelstahl, Spülküche)",30000),("Lüftung und Abluft",18000),("Theke und Bar (Zapfanlage, Kühlung, Backbar)",20000),("Möbel (ca. 150 Plätze, Lounge, Séparée)",28000),("Beleuchtung und Deko",8000),("Wand, Boden, Decke, Akustik",15000),("Gäste-WC Ausstattung",5000),("Kasse, Technik, Musik, WLAN",5000),("Terrasse (Holzdeck, Möbel, Heizstrahler, 40 Plätze)",6000),("Planung und Genehmigung",5000),("Eröffnung, Marketing, Warenerstbestückung",3000),("Puffer 5 %",7150)]
table_set(S[2],[["Posten","Betrag"]]+[[a,eur(b)] for a,b in ausb]+[["Summe (im Modell: 150.000 €)",eur(sum(b for _,b in ausb))]])
T(S[4],"Baunebenkosten von 15 % fallen auf Möbel und Geräte nicht an, die Planung steckt als eigener Posten drin. Für die Gastro (460 m², ca. 150 Plätze) sind 150.000 € angesetzt, das ist knapp; Angebote sind nötig. Bei 200.000 € Ausbau steigt die Rate um ca. 190 € im Monat.")
# ---- 31 Mietdaten ----
T(sh[31][4],"Im Modell","Wohnungen 11,18 €/m² Kaltmiete (950 € für 85 m², Bauherr, zentrale Lage). Gastro-Pacht 12 €/m², ohne Marktdaten.")
# ================= NEUE FOLIEN =================
def cards(s,t,zg,items):
    L=list(s.shapes); T(L[0],t); T(L[1],zg)
    for (h,b),(i,j) in zip(items,((3,4),(6,7),(9,10),(12,13))): T(L[i],h); T(L[j],b)
cards(cl["gbr"],"Aufbau: Haus-GbR/UG und Betreiber-UG","Für die Bank",[
 ("Haus-GbR/UG (Eigentümer)","Das Gebäude gehört einer eigenen Gesellschaft. Einnahmen: Kaltmiete der 8 Wohnungen und Pacht der Gastro. Ausgaben: Zins, Tilgung und 10 % Rücklage."),
 ("Betreiber-UG (Gastro-Betrieb)","Der Betrieb zahlt Pacht an das Haus (460 m² × 12 €). Umsatz, Wareneinsatz, Personal und Gewinn bleiben im Betrieb und belasten das Haus nicht."),
 ("Einzelrechnung je Einheit","Jede Wohnung und die Gastro-Fläche werden wie ein eigenes Objekt gerechnet: Kosten nach Bruttogrundfläche (Kern anteilig), eigene KfW-Tranche, eigene Miete, eigener Faktor."),
 ("Umsatzsteuer","Wohnungen: Vermietung steuerfrei (§ 4 Nr. 12 UStG), kein Vorsteuerabzug, Baupreise brutto. Gastro: Option zur Umsatzsteuer (§ 9 UStG) möglich, dann Gastro-Baukosten netto, hier nicht eingerechnet. Steuerberater klärt.")])
cards(cl["qng"],"QNG: das Qualitätssiegel Nachhaltiges Gebäude","Für Bank und Stadt",[
 ("Was ist QNG?","Staatliches Siegel für Gebäude, die über die Energie hinaus Nachhaltigkeitsanforderungen erfüllen. Es öffnet den höheren KfW-Kreditrahmen."),
 ("Was wird nachgewiesen?","Ökobilanz (Treibhausgase und nicht erneuerbare Primärenergie über den Lebenszyklus), Schadstoffvermeidung, nachhaltige Materialgewinnung (z. B. zertifiziertes Holz), Zertifizierung durch eine zugelassene Stelle. Grenzwerte im QNG-Handbuch prüfen."),
 ("Was bringt es?","KfW 298: 150.000 € statt 100.000 € je Wohnung, im Projekt 400.000 € mehr. KfW 299: bis 2.000 € statt ca. 1.500 € je m² Nettogrundfläche, im Projekt rund 195.000 € mehr."),
 ("Was heißt das für uns?",f"Von Anfang an mit Energie- und Nachhaltigkeitsberater planen. Mehrkosten im Modell: 3 % ({eur(Z['eh_k'])}), vom Architekten zu bestätigen. Der Holzbau im Staffelgeschoss hilft bei der Ökobilanz (Annahme).")])
cards(cl["kfwb"],"KfW-Förderung: Was gilt?","Für Bank und Stadt",[
 ("Was ist das?","Zinsgünstige Kredite der KfW für klimafreundlichen Neubau, beantragt über die Hausbank. Kein Zuschuss. Kein Rechtsanspruch, die Mittel sind begrenzt."),
 ("Voraussetzungen","Effizienzhaus 40 (Gastro: Effizienzgebäude 40), QNG für den vollen Rahmen, Heizung ohne fossile Brennstoffe, Nachweis durch Energieeffizienz-Experten (Programmvorgaben, im Merkblatt prüfen)."),
 ("Antrag und Ablauf","Antrag vor Vorhabenbeginn, sonst keine Förderung. Zinsbindung 10 Jahre, danach Anschlusskonditionen. Kombination mit den Programmen 296/596 für dieselbe Einheit ist ausgeschlossen."),
 ("Unser Ansatz","KfW 298: 8 × 150.000 € = 1.200.000 € zu 2,5 %. KfW 299: 460 m² × 85 % × 2.000 € = 782.000 € zu 3,0 %. Rest Hausbank zu 4,0 %. Quellen nennen 0,6 % bis 3,05 %, wir rechnen vorsichtig.")])
cards(cl["zins"],"Zinsen und Einlagensicherung","Für die Bank",[
 ("Zinsen im Modell","KfW 298: 2,5 %, KfW 299: 3,0 %, Hausbank: 4,0 %, jeweils 10 Jahre fest, 1 % Tilgung. Stand Bauzinsen Okt. 2026, bei Bank und KfW zu bestätigen."),
 ("Sinken die Zinsen?","Weiter fallende Zinsen sind eine Erwartung und nicht belegt. Wir rechnen Szenarien: −0,5 und +1,0 Prozentpunkte. Fällt der Zins nach Vertragsabschluss, hilft das erst bei der Anschlussfinanzierung."),
 ("Einlagensicherung","Gesetzlich 100.000 € je Kunde und Bank. Die freiwillige Sicherung der Privatbanken wird laut Presse bis 2030 schrittweise gesenkt. Ein Wegfall ab 2027 ist nicht belegt (EU-Frist 11.05.2027 nur fragmentarisch)."),
 ("Was heißt das für uns?","Es betrifft nur Guthaben (Rücklagen, Mietkautionen, Eigenkapital), nicht die Darlehen. Größere Beträge auf mehrere Banken verteilen oder bei Sparkasse oder Volksbank mit Institutssicherung halten.")])
# Einzelrechnung Wohnungen (Klon von Slide 12)
s=cl["einzel"]; L=list(s.shapes); T(L[0],"Einzelrechnung je Wohnung und Gastro"); T(L[1],"Für die Bank")
def urow(nm,x,mult=1):
    return [nm,num(x["nf"],0)+" m²",eur(x["kosten"]),eur(x["kfw"]),eur(x["bank"]),eur(x["netto"]),eur(x["zins"]+x["tilg"]),eur(x["plus"],0,True),eur(x["plus"]/12,0,True),f2(x["dscr"])]
sumrow=["Summe Haus",num(725+460)+" m²",eur(sum(x["kosten"] for x in UZ)),eur(sum(x["kfw"] for x in UZ)),eur(sum(x["bank"] for x in UZ)),eur(sum(x["netto"] for x in UZ)),eur(sum(x["zins"]+x["tilg"] for x in UZ)),eur(sum(x["plus"] for x in UZ),0,True),eur(sum(x["plus"] for x in UZ)/12,0,True),f2(sum(x["netto"] for x in UZ)/sum(x["zins"]+x["tilg"] for x in UZ))]
w=[2.05,0.85,1.3,1.1,1.1,1.1,1.2,1.1,1.1,0.75]; sc=12.13/sum(w); w=[x*sc for x in w]
table_set(L[2],[["Einheit (je Stück)","Fläche","Kosten gesamt","KfW","Hausbank","Netto-Miete / Jahr","Kapitaldienst / Jahr","Plus / Jahr","Plus / Monat","DSCR"],
 urow("WE 1 bis 5 (1. OG), je Wohnung",we15),urow("WE 6 bis 8 (Staffel), je Wohnung",we68),urow("Gastro-Fläche (Haus-Sicht)",gas),sumrow],ncols=10,widths=w)
# Texte unter Tabelle ergänzen
from pptx.util import Pt
tb=L[2]; top=Emu(tb.top+Emu(int(2.6*914400)))
note=copy.deepcopy(sh[19][5]._element); s.shapes._spTree.append(note); nshape=list(s.shapes)[-1]
nshape.left=Emu(int(0.6*914400)); nshape.top=Emu(int(4.7*914400)); nshape.width=Emu(int(12.13*914400)); nshape.height=Emu(int(1.6*914400))
T(nshape,"Lesehilfe: Plus = Netto-Miete (nach 10 % Rücklage) minus Zins und 1 % Tilgung, ohne Eigenkapital. DSCR = Netto-Miete geteilt durch Kapitaldienst; über 1,0 trägt sich die Einheit selbst.",f"Die Wohnungen im 1. OG sind der Engpass ({f2(we15['dscr'])}): Massivbau und anteiliger Kern im EG. Die Staffel-Wohnungen profitieren vom Holzabschlag ({f2(we68['dscr'])}), die Gastro-Fläche liegt bei {f2(gas['dscr'])}.","Alle Werte gelten nur beim Zielpreis von 1.450 € je m² BGF; Eigenkapital ist 0 €.")
# Beispiel WE1 (Klon von Slide 21: zwei Tabellen)
s=cl["bsp"]; L=list(s.shapes); T(L[0],"Beispiel WE 1 (1. OG): Kosten, Finanzierung, Miete"); T(L[1],"Für die Bank")
x=we15
bau_we=ZB*x["bgf"]
table_set(L[2],[["Kosten WE 1","Betrag"],[f"Bau ({num(x['bgf'],0)} m² BGF inkl. Kern × 1.450 €)",eur(bau_we)],["Baunebenkosten 15 %",eur(bau_we*0.15)],["Bau inkl. Nebenkosten",eur(bau_we*1.15)],["Mehrkosten EH 40 und QNG 3 %",eur(bau_we*1.15*0.03)],["Grundstücksanteil und Finanzierungskosten (anteilig)",eur(x["kosten"]-bau_we*1.15*1.03)],["Gesamtkosten WE 1",eur(x["kosten"])],["Kosten je m² Wohnfläche",eur(x["kosten"]/x["nf"])]])
table_set(L[3],[["Finanzierung und Ertrag","Betrag"],["KfW 298 (2,5 %, 1 % Tilgung)",eur(x["kfw"])],["Hausbank (4,0 %, 1 % Tilgung)",eur(x["bank"])],["Netto-Miete (83 m² × 11,18 € × 12, minus 10 %)",eur(x["netto"])],["Zins + Tilgung im 1. Jahr",eur(-(x["zins"]+x["tilg"]))],["Plus pro Jahr",eur(x["plus"],0,True)],["Plus pro Monat / DSCR",f"{eur(x['plus']/12,0,True)} / {f2(x['dscr'])}"]])
T(L[4],f"Das Plus ist klein ({f2(x['dscr'])}). Schon 5 % höhere Baukosten oder 1 Prozentpunkt mehr Zins drehen es ins Minus. Deshalb sind Angebote und die Zinszusage vor Baubeginn entscheidend.")
# Gastro Haus + Betrieb (Klon von Slide 21)
s=cl["gas2"]; L=list(s.shapes); T(L[0],"Gastro: Haus-Sicht und Betreiber-Sicht"); T(L[1],"Für die Bank")
g=gas
table_set(L[2],[["Haus-GbR/UG: Gastro-Fläche","Betrag"],["Gesamtkosten Gastro-Fläche (inkl. Ausbau)",eur(g["kosten"])],["davon KfW 299 / Hausbank",f"{eur(g['kfw'])} / {eur(g['bank'])}"],[f"Netto-Pacht nach Rücklage (Pacht {eur(g['rent'])})",eur(g["netto"])],["Zins (1. Jahr)",eur(-g["zins"])],["Tilgung 1 % (1. Jahr)",eur(-g["tilg"])],["Plus pro Jahr",eur(g["plus"],0,True)],["Plus pro Monat / DSCR",f"{eur(g['plus']/12,0,True)} / {f2(g['dscr'])}"]])
table_set(L[3],[["Betreiber-UG (pro Monat)","Betrag"],["Umsatz (netto)",eur(50000)],["Wareneinsatz, Personal, Betriebskosten",eur(-(50000*0.305*0+50000-15250))],["Gewinn vor Pacht (30,5 %)",eur(15250)],["Pacht an das Haus",eur(-5520)],["Betriebsergebnis nach Pacht, vor Lohn",eur(9730,0,True)],["Break-even-Umsatz des Betriebs","ca. 18.100 €"]])
T(L[4],"Haus und Betrieb sind getrennt: Das Haus verdient die Pacht und trägt den Kapitaldienst der Gastro-Fläche, der Betrieb zahlt die Pacht aus dem Umsatz. Umsatz 50.000 € und Marge 30,5 % sind Richtwerte, keine Werte aus Werlte; Lohn des Bauherrn und Steuern sind nicht gerechnet.")
# Szenarien (Klon von Slide 22)
s=cl["szen"]; L=list(s.shapes); T(L[0],"Szenarien: Baupreis und Zins"); T(L[1],"Für die Bank")
def srow(nm,**kw):
    m,u=unitcalc(**kw); d=lambda x:f2(x["dscr"])
    return [nm,eur(m["gesamt"]),d(u[0]),d(u[5]),d(u[8]),eur((m["netto_imm"]-m["kd_j"])/12,0,True)]
table_set(L[2],[["Szenario","Gesamtkosten","WE 1–5 (DSCR)","WE 6–8 (DSCR)","Gastro (DSCR)","Plus Haus / Monat"],
 srow("Bankunterlagen: 2.200 €/m², Holz −400",bau=2200,holz=400),srow("1.800 €/m², Holz −700",bau=1800,holz=700),
 srow("Zielpreis: 1.450 €/m², Holz −700",bau=1450,holz=700),srow("Zielpreis, Zins −0,5 Prozentpunkte",bau=1450,holz=700,dz=-0.005),srow("Zielpreis, Zins +1,0 Prozentpunkt",bau=1450,holz=700,dz=0.01)])
delshape(L[3])
T(L[4] if len(L)>4 and L[4].has_text_frame else L[3],"") if False else None
# ---- Quellen ----
s=cl["quellen"]; L=list(s.shapes); T(L[0],"Quellen und Stand der Recherche"); T(L[1],"Anhang")
table_set(L[2],[["Quelle (Suchtreffer, nicht im Volltext geprüft)","Aussage"],["Verbraucherzentrale, Interhyp (07.11.2026)","KfW 298: 100.000 € je Wohneinheit, mit QNG 150.000 €"],["KfW, co2online (07.11.2026)","KfW 299: bis 2.000 € je m² Nettogrundfläche mit QNG, max. 10 Mio. €; Rahmen im Merkblatt prüfen"],["vergleich.de (22.06.2026), WIBank","KfW 298 effektiv ca. 2,60 %, andere Quellen 0,6 bis 1,5 %; Zins bei der Bank bestätigen"],["Börsen-Zeitung, mobiflip, PwC-Blog","Einlagensicherung Privatbanken bis 2030 gesenkt; EU-Frist 11.05.2027 fragmentarisch; Wegfall 2027 nicht belegt"],["Thüringer Landesamt für Statistik (PR 094/25, 120/25)","Veranschlagte Baukosten Mehrfamilienhäuser 1.908 bis 2.366 €/m² Wohnfläche (Genehmigungsdaten)"]])
from pptx.enum.text import PP_ALIGN
for r_ in L[2].table.rows:
    for c_ in r_.cells:
        for p_ in c_.text_frame.paragraphs: p_.alignment=PP_ALIGN.LEFT
Ls=[x for x in L[3:] if x.has_text_frame and x.text_frame.text.strip()]
for x in Ls:
    if "Im Modell" in x.text_frame.text or "Wohnungen 11,18" in x.text_frame.text: T(x,"Hinweis","Alle Preise, Zinsen und Umsätze sind Annahmen und durch Angebote, Bank, KfW und Steuerberater zu belegen. Keine Aussage zur baurechtlichen Zulässigkeit.")
    elif "Quellen:" in x.text_frame.text: delshape(x)
# ---- Reihenfolge ----
S_=lambda i: sl[i-1]
order=[S_(i) for i in range(1,15)]+[cl["gbr"],cl["qng"],cl["kfwb"],cl["zins"]]+[S_(i) for i in (15,16,17,18,19)]+[cl["einzel"],cl["bsp"],cl["gas2"]]+[S_(20),S_(21),S_(22),cl["szen"],S_(23),S_(24),S_(25),S_(26),S_(27),S_(28),S_(29),S_(30),S_(31),cl["quellen"]]
reorder(prs,order)
prs.save(OUT); print("saved",len(prs.slides))
