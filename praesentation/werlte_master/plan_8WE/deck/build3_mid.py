# 17 Alles auf einer Seite
sl=page(d,SEC[3],"Alles auf einer Seite: Kosten und Gewinn des ganzen Projekts","Realistische Basis: 2.200 €/m² BGF, ohne Eigenkapital, mit KfW. Tilgung ist Vermögensaufbau, kein Verlust. Ohne Steuern und Lohn des Bauherrn.")
tx(sl,0.7,1.85,5.8,0.35,"Was kostet es, und wer zahlt?",size=15,color=GREEN,font=HF)
table(sl,0.7,2.2,5.9,[["Posten","Betrag"],["Grundstück inkl. Steuer, Notar",eur(Z["grund"])],["Bau (Massiv, Holz-Staffel, Terrasse)",eur(Z["bau_roh"]+Z["abschlag"]+Z["terr_k"])],["Baunebenkosten 17 %",eur(Z["bnk_k"])],["Effizienzhaus 40 und QNG 4 %",eur(Z["eh_k"])],["Gastro-Ausbau",eur(150000)],["Außenanlagen, Stellplätze",eur(100000)],["Zinsen in Bau- und Anlaufzeit",eur(Z["fin"])],["Gesamtkosten",eur(Z["gesamt"])],["bezahlt mit KfW-Darlehen",eur(1982000)],["bezahlt mit Hausbank-Darlehen",eur(Z["hb"])]],[3.6,1.6],size=12,rh=0.37,total=(8,))
tx(sl,7.0,1.85,5.6,0.35,"Was kommt rein, was geht raus? (pro Jahr)",size=15,color=GREEN,font=HF)
table(sl,7.0,2.2,5.63,[["Posten","pro Jahr","pro Monat"],["Miete 8 Wohnungen",eur(Z["miete_j"],0,True),eur(Z["miete_j"]/12,0,True)],["Pacht Gastro",eur(Z["pacht_j"],0,True),eur(Z["pacht_j"]/12,0,True)],["Rücklage 15 %",eur(-Z["rueck"]),eur(-Z["rueck"]/12)],["Zinsen",eur(-h[0][1]),eur(-h[0][1]/12)],["Tilgung 1 %",eur(-h[0][2]),eur(-h[0][2]/12)],["Ergebnis im Haus",eur(Z["netto_imm"]-Z["kd_j"],0,True),eur(haus_plus,0,True)],["Gastro-Betrieb (50.000 € Umsatz/Monat)",eur(Z["betrieb"],0,True),eur(Z["betrieb"]/12,0,True)],["Ergebnis gesamt",eur(Z["erg"],0,True),eur(Z["erg"]/12,0,True)]],[3,1.35,1.2],size=12,rh=0.42,total=(6,8),neg=(6,))
tx(sl,0.7,6.15,11.9,0.5,[{"t":[(f"Faktor {f2(Z['dscr_imm'])} allein, {f2(Z['dscr_ges'])} mit Gastro-Gewinn: ",{"bold":True,"color":GREEN}),("Miete und Pacht decken die Raten nicht, erst der Gastro-Gewinn des Betreibers gleicht es aus.",{})]}],size=14)
# 18 Kosten
sl=page(d,SEC[3],f"Das Haus kostet {mio(Z['gesamt'])}, am meisten kostet der Bau",f"Das sind {num(Z['gesamt']/1540)} € je m² BGF. Zusatzszenario Zielpreis 1.450 €/m²: {mio(ZT['gesamt'])}, siehe Folie Szenarien. Zielpreis ist nicht durch Angebote belegt.")
cats=["Bau (inkl. Holz, Terrasse)","Baunebenkosten","Grundstück","Gastro-Ausbau","Zinsen Bauzeit","Außenanlagen","Effizienzhaus, QNG"]; vals=[Z["bau_roh"]+Z["abschlag"]+Z["terr_k"],Z["bnk_k"],Z["grund"],150000,Z["fin"],100000,Z["eh_k"]]
cd=CategoryChartData(); cd.categories=cats; cd.add_series("Kosten",vals)
ch=sl.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(0.7),Inches(1.9),Inches(8),Inches(4.6),cd).chart; style_chart(ch,13)
pl=ch.plots[0]; pl.gap_width=45; pl.has_data_labels=True; pl.data_labels.number_format='#,##0" €"'; pl.data_labels.number_format_is_linked=False; pl.data_labels.position=XL_LABEL_POSITION.OUTSIDE_END; pl.data_labels.font.size=Pt(13)
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb=C(GREEN); ch.value_axis.visible=False; hide_axis_lines(ch.value_axis); ch.category_axis.reverse_order=True; hide_axis_lines(ch.category_axis); ch.value_axis.maximum_scale=3600000
kpi(sl,9.3,2.1,3.3,mio(Z["gesamt"]),"Gesamtkosten inkl. Finanzierung"); kpi(sl,9.3,3.7,3.3,f"{num(Z['gesamt']/1540)} €","je m² Bruttogrundfläche",GREY); kpi(sl,9.3,5.3,3.3,"0 €","Eigenkapital (100 % Fremdkapital)",TERRA)
# 19 Finanzierung
sl=page(d,SEC[3],f"{1982000/Z['gesamt']*100:.0f} % des Geldes kommen von der KfW, der Rest von der Hausbank")
cd=CategoryChartData(); cd.categories=["KfW 298 Wohnen","KfW 299 Gastro","Hausbank"]; cd.add_series("Darlehen",[1200000,782000,Z["hb"]])
ch=sl.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT,Inches(0.7),Inches(1.9),Inches(5.2),Inches(4.6),cd).chart; style_chart(ch,12,True)
for i,c in enumerate((GREEN,GOLD,TERRA)): pt=ch.plots[0].series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=C(c)
ch.plots[0].has_data_labels=True; ch.plots[0].data_labels.number_format='0%'; ch.plots[0].data_labels.show_percentage=True; ch.plots[0].data_labels.show_value=False; ch.plots[0].data_labels.font.size=Pt(13); ch.plots[0].data_labels.font.color.rgb=C(WHITE)
(l1,z1),(l2,z2),(l3,z3)=Z["loans"]
table(sl,6.3,2.1,6.33,[["Darlehen","Betrag","Zins","Rate / Monat"],["KfW 298 Wohnen",eur(l1),pct(z1),eur(l1*(z1+.01)/12)],["KfW 299 Gastro",eur(l2),pct(z2),eur(l2*(z2+.01)/12)],["Hausbank",eur(l3),pct(z3),eur(l3*(z3+.01)/12)],["Summe",eur(Z["gesamt"]),pct(Z["mischzins"],2),eur(Z["kd_m"])]],[2.2,1.6,0.9,1.6],size=13,rh=0.55,total=(4,))
tx(sl,6.3,5.1,6.33,1.5,[f"Bau 15 Monate, danach 12 Monate Anlaufzeit ohne Tilgung. Die Zinsen dieser Zeit ({eur(Z['fin'])}) zahlt die Hausbank vor.","Ohne QNG sinkt der KfW-Rahmen um ca. 600.000 €, die Rate steigt dann um ca. 720 € im Monat."],size=13,color=GREY,space=6)
# 20 Einnahmen gegen Ausgaben
sl=page(d,SEC[3],"Miete und Pacht tragen die Raten nicht allein, mit dem Gastro-Gewinn reicht es","Erstes Jahr nach der Anlaufzeit, pro Jahr. Gastro-Gewinn bei 50.000 € Umsatz pro Monat, vor Lohn des Bauherrn und Steuern.")
cd=CategoryChartData(); cd.categories=["Miete und Pacht (netto)","plus Gastro-Gewinn","Zinsen und Tilgung"]
cd.add_series("Miete und Pacht",[Z["netto_imm"],Z["netto_imm"],None]); cd.add_series("Gastro-Gewinn",[None,Z["betrieb"],None]); cd.add_series("Zinsen",[None,None,h[0][1]]); cd.add_series("Tilgung",[None,None,h[0][2]])
ch=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED,Inches(0.7),Inches(1.9),Inches(8.6),Inches(4.6),cd).chart; style_chart(ch,13,True); pl=ch.plots[0]; pl.gap_width=55; pl.overlap=100
for k,c in enumerate((GREEN,GOLD,TERRA,"D9A79A")):
    s_=pl.series[k]; s_.format.fill.solid(); s_.format.fill.fore_color.rgb=C(c); s_.data_labels.show_value=True; s_.data_labels.number_format='#,##0" €"'; s_.data_labels.number_format_is_linked=False; s_.data_labels.font.size=Pt(12); s_.data_labels.font.color.rgb=C(WHITE if k<3 else INK)
ch.value_axis.visible=False; hide_axis_lines(ch.value_axis); hide_axis_lines(ch.category_axis)
kpi(sl,9.7,2.0,2.9,f"Faktor {f2(Z['dscr_imm'])}","nur Miete und Pacht geteilt durch Zinsen und Tilgung",NEG,vs=30); kpi(sl,9.7,3.65,2.9,f"Faktor {f2(Z['dscr_ges'])}","mit Gastro-Gewinn",POS,vs=30); kpi(sl,9.7,5.3,2.9,eur(Z["kd_m"]),"Zinsen und Tilgung pro Monat",GREY,vs=30)
# 21 Einzel
fl=[x["dscr"] for x in UZ]
sl=page(d,SEC[3],f"Einzeln trägt sich keine Einheit selbst: Faktor {f2(min(fl))} bis {f2(max(fl))}","Plus = Netto-Miete (nach 15 % Rücklage) minus Zins und 1 % Tilgung. Faktor = Netto-Miete geteilt durch Kapitaldienst; über 1,0 trägt sich die Einheit selbst.")
def urow(n,x): return [n,num(x["nf"])+" m²",eur(x["kosten"]),eur(x["kfw"]),eur(x["bank"]),eur(x["netto"]),eur(x["zins"]+x["tilg"]),eur(x["plus"]/12,0,True),f2(x["dscr"])]
tot=lambda k: sum(x[k] for x in UZ)
rows=[["Einheit (je Stück)","Fläche","Kosten","KfW","Hausbank","Netto-Miete/J","Zins+Tilgung/J","Plus/Monat","Faktor"],urow("WE 1–5 (1. OG)",we15),urow("WE 6–8 (Staffel)",we68),urow("Gastro-Fläche",gas),["Gesamtes Haus","1.185 m²",eur(tot("kosten")),eur(tot("kfw")),eur(tot("bank")),eur(tot("netto")),eur(tot("zins")+tot("tilg")),eur(tot("plus")/12,0,True),f2(tot("netto")/(tot("zins")+tot("tilg")))]]
table(sl,0.7,1.95,11.93,rows,[2.3,1,1.4,1.2,1.2,1.4,1.5,1.2,0.9],size=13,rh=0.62,total=(4,),neg=(1,2,3))
tx(sl,0.7,5.4,11.9,1.2,[{"t":[("Warum? ",{"bold":True,"color":GREEN}),("Die Kosten liegen je m² über dem, was Miete und Pacht tragen. Die Gastro-Fläche trägt sich nur, wenn der Betrieb darüber verdient.",{})]}],size=14)
# 22 Beispiel
x=we15; bau_we=2200*x["bgf"]
sl=page(d,SEC[3],"Beispiel: So rechnet sich eine Wohnung im 1. OG")
tx(sl,0.7,1.9,5.8,0.35,"Was kostet sie?",size=16,color=GREEN,font=HF)
table(sl,0.7,2.35,5.8,[["Posten","Betrag"],[f"Bau ({num(x['bgf'])} m² BGF × 2.200 €)",eur(bau_we)],["Baunebenkosten 17 %",eur(bau_we*.17)],["Effizienzhaus, QNG 4 %",eur(bau_we*1.17*.04)],["Grundstück, Außenanlagen, Zinsen (anteilig)",eur(x["kosten"]-bau_we*1.17*1.04)],["Gesamtkosten",eur(x["kosten"])],["je m² Wohnfläche",eur(x["kosten"]/x["nf"])]],[3.6,1.6],size=13,rh=0.5,total=(5,))
tx(sl,7.0,1.9,5.6,0.35,"Wie wird sie bezahlt, was bringt sie?",size=16,color=GREEN,font=HF)
table(sl,7.0,2.35,5.63,[["Posten","Betrag"],["KfW 298 (2,5 %)",eur(x["kfw"])],["Hausbank (4,0 %)",eur(x["bank"])],["Netto-Miete pro Jahr (83 m² × 10,90 € × 12 − 15 %)",eur(x["netto"])],["Zins und Tilgung pro Jahr",eur(-(x["zins"]+x["tilg"]))],["Ergebnis pro Jahr",eur(x["plus"],0,True)],["Ergebnis pro Monat",eur(x["plus"]/12,0,True)]],[3.6,1.6],size=13,rh=0.5,total=(5,),neg=(5,6))
tx(sl,0.7,6.0,11.9,0.6,f"Die Wohnung trägt sich allein nicht (Faktor {f2(x['dscr'])}): Sie kostet ca. {num(x['kosten']/x['nf'])} €/m², Neubauwohnungen werden in Werlte für ca. 3.400 €/m² angeboten.",size=14,color=NEG)
# 23 Gastro Haus Betrieb
g=gas; gp=Z["pacht_j"]/12
sl=page(d,SEC[3],"Gastro: Das Haus bekommt Pacht, der Betrieb verdient zusätzlich","Umsatz 50.000 € und Marge 30,5 % sind Branchen-Richtwerte, keine Werte aus Werlte. Pacht 8 €/m² nach Inseraten in Kleinstädten (6 bis 8 €/m²). Lohn des Bauherrn und Steuern nicht gerechnet.")
tx(sl,0.7,1.9,5.8,0.35,"Haus-GbR/UG: Gastro-Fläche",size=16,color=GREEN,font=HF)
table(sl,0.7,2.35,5.8,[["Posten","Betrag"],["Kosten der Gastro-Fläche (inkl. Ausbau)",eur(g["kosten"])],["davon KfW 299 / Hausbank",f"{eur(g['kfw'])} / {eur(g['bank'])}"],["Pacht pro Jahr (460 m² × 8 €)",eur(g["rent"])],["Netto-Pacht nach 15 % Rücklage",eur(g["netto"])],["Zins und Tilgung pro Jahr",eur(-(g["zins"]+g["tilg"]))],["Ergebnis pro Monat (Faktor "+f2(g["dscr"])+")",eur(g["plus"]/12,0,True)]],[3.7,2.1],size=13,rh=0.55,total=(6,),align=["l","r"],neg=(6,))
tx(sl,7.0,1.9,5.6,0.35,"Betreiber-UG: Gastro-Betrieb pro Monat",size=16,color=GREEN,font=HF)
table(sl,7.0,2.35,5.63,[["Posten","Betrag"],["Umsatz (netto)",eur(50000)],["Wareneinsatz, Personal, Betriebskosten",eur(-34750)],["Gewinn vor Pacht (30,5 %)",eur(15250)],["Pacht an das Haus",eur(-gp)],["Betriebsergebnis vor Lohn und Steuern",eur(15250-gp,0,True)]],[3.7,1.9],size=13,rh=0.55,total=(5,))
# 24 Umsatz
bu=be_um(Z)
sl=page(d,SEC[3],f"Ab {num(round(bu,-2))} € Umsatz im Monat trägt sich das ganze Projekt (±0)",f"Ergebnis = Netto-Miete und -Pacht plus Gastro-Gewinn minus Zinsen und Tilgung (Betreiber = Bauherr). Der Betrieb allein deckt seine Pacht ab {num(round(gp/Z['marge'],-2))} € Umsatz.")
us=[30000,37100,40000,50000,60000,70000]; cd=CategoryChartData(); cd.categories=[num(u) for u in us]; cd.add_series("Ergebnis pro Monat",[erg_um(Z,u) for u in us])
ch=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.7),Inches(1.9),Inches(7.2),Inches(4.6),cd).chart; style_chart(ch,13); pl=ch.plots[0]; pl.gap_width=50
pl.has_data_labels=True; pl.data_labels.number_format='#,##0" €"'; pl.data_labels.number_format_is_linked=False; pl.data_labels.position=XL_LABEL_POSITION.OUTSIDE_END; pl.data_labels.font.size=Pt(12)
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb=C(GREEN); pl.series[0].invert_if_negative=False
for i,u in enumerate(us):
    pt=pl.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=C(NEG if erg_um(Z,u)<-100 else (GOLD if abs(erg_um(Z,u))<=100 else GREEN))
ch.value_axis.visible=False; hide_axis_lines(ch.value_axis); hide_axis_lines(ch.category_axis); ch.category_axis.tick_label_position=XL_TICK_LABEL_POSITION.LOW if False else ch.category_axis.tick_label_position
tx(sl,0.7,6.4,7,0.25,"Gastro-Umsatz pro Monat in €",size=11,color=GREY,align=PP_ALIGN.CENTER)
table(sl,8.3,2.1,4.33,[["Umsatz","Gewinn vor Pacht","Ergebnis gesamt"]]+[[eur(u),eur(u*Z["marge"]),eur(erg_um(Z,u),0,True)] for u in us],[1.2,1.5,1.6],size=12,rh=0.5,hl=(2,))
# 25 Abzahlung
sl=page(d,SEC[3],f"Nach 10 Jahren Zinsbindung bleiben {mio(Z['rest10'])} Restschuld")
cd=CategoryChartData(); cd.categories=[str(y) for y,_,_,_ in h]; cd.add_series("Restschuld",[round(r) for *_,r in h])
ch=sl.shapes.add_chart(XL_CHART_TYPE.LINE,Inches(0.7),Inches(1.9),Inches(7.4),Inches(4.5),cd).chart; style_chart(ch,11)
s_=ch.plots[0].series[0]; s_.format.line.color.rgb=C(GREEN); s_.format.line.width=Pt(3); s_.smooth=False
ch.value_axis.tick_labels.number_format='#,##0'; ch.value_axis.tick_labels.number_format_is_linked=False; hide_axis_lines(ch.value_axis,True)
tx(sl,0.7,6.4,7.4,0.25,"Jahre",size=11,color=GREY,align=PP_ALIGN.CENTER)
yrs=[1,5,10,20,35]; table(sl,8.5,2.1,4.13,[["Jahr","Zinsen","Tilgung","Restschuld"]]+[[("10 (Ende)" if y==10 else str(y)),eur(h[y-1][1]),eur(h[y-1][2]),eur(h[y-1][3])] for y in yrs],[1,1.3,1.3,1.5],size=11,rh=0.5,hl=(3,))
tx(sl,8.5,5.4,4.13,1.2,"Mit 1 % Tilgung sinkt die Schuld langsam, danach muss die Anschlussfinanzierung geplant werden.",size=13,color=GREY)
# 26 Prognose
pg={r[0]:r for r in Z["prog"]}; yy=[1,3,5,7,10]
sl=page(d,SEC[3],f"In zehn Jahren wächst das Ergebnis von {eur(pg[1][6],0,True)} auf {eur(pg[10][6],0,True)} im Jahr","Annahme: Mieten, Pacht und Umsatz steigen 1,5 % pro Jahr, der Kapitaldienst bleibt gleich. Ergebnis inkl. Gastro-Betrieb, vor Steuern und Lohn.")
table(sl,0.7,1.95,11.93,[["Jahr"]+[str(y) for y in yy],["Netto-Ertrag vor Kapitaldienst"]+[eur(pg[y][5]) for y in yy],["Zinsen und Tilgung"]+[eur(-Z["kd_j"])]*5,["Ergebnis pro Jahr"]+[eur(pg[y][6],0,True) for y in yy],["Faktor"]+[f2(pg[y][7]) for y in yy],["Restschuld"]+[eur(pg[y][8]) for y in yy]],[3.2,1.7,1.7,1.7,1.7,1.7],size=14,rh=0.7,total=(3,))
# 27 Belastungstest
sl=page(d,SEC[3],"Was wäre wenn? Der Puffer ist klein","Belastungstest auf das Gesamtergebnis inkl. Gastro-Betrieb (Faktor gesamt). Vereinfachte Rechnung, die Hausbank prüft mit eigenen Annahmen.")
ss=sens(Z); base=ss[0][1]; gf=[s for s in ss if s[0].startswith("Gastro fällt")][0]; ss2=[s for s in ss if not s[0].startswith("Gastro fällt")]
leer=("Eine Wohnung im 1. OG dauerhaft leer",base-we15["netto"]/12,(Z["netto_ges"]-we15["netto"])/Z["kd_j"])
rows=[["Was passiert?","Ergebnis / Monat","Faktor","Änderung"]]+[[n,eur(e,0,True),f2(f_),"" if n=="Plan" else eur(e-base,0,True)] for n,e,f_ in ss2+[leer,gf]]
table(sl,0.7,1.95,11.93,rows,[6,2,1.2,1.7],size=13,rh=0.45,hl=(1,),neg=tuple(i+1 for i,r in enumerate(ss2+[leer,gf]) if r[1]<0))
tx(sl,0.7,6.2,11.9,0.3,"Faktor ab 1,2 gilt bei Banken als üblich, unter 1,0 trägt sich das Haus nicht mehr selbst.",size=10,color=GREY)
# 28 Szenarien
sl=page(d,SEC[3],"Break-even: ab 37.100 € Umsatz ±0, im Stressfall ab 46.500 €","Break-even-Umsatz = Gastro-Umsatz pro Monat, bei dem das Gesamtergebnis (Haus plus Gastro-Betrieb) genau null ist. Einlagensicherung/Zinsaufschlag ist nicht belegt und als +0,5 Prozentpunkte gerechnet.")
def srow(nm,**kw):
    m=model(**{**RK,**kw}); kd=m["zins1"]+m["til"]*m["gesamt"] if "til" in kw else m["kd_j"]
    bu_=(kd-m["netto_imm"]+m["pacht_j"])/m["marge"]/12
    return [nm,eur(m["gesamt"]),eur(kd/12),f2(m["netto_imm"]/kd),eur(bu_),f2((m["netto_imm"]+m["betrieb"])/kd)]
KO=dict(kfw298=800000.0,kfw299=391*1500.0)
rows=[["Szenario (Baupreis 2.200 €/m²)","Gesamtkosten","Kapitaldienst/Monat","Faktor Haus","Break-even-Umsatz","Faktor bei 50.000 €"],srow("Realistische Basis"),srow("Zins +0,5 Prozentpunkte",dz=0.005),srow("KfW ohne QNG",**KO),srow("Zins +0,5 und ohne QNG",dz=0.005,**KO),srow("Tilgung 2 % statt 1 %",til=0.02),srow("Zusatz: Zielpreis 1.450 €/m², Holz −700",bau=1450,holz=700)]
table(sl,0.7,1.95,11.93,rows,[3.6,1.6,1.8,1.3,1.8,1.7],size=13,rh=0.62,hl=(1,),bold=(1,))
tx(sl,0.7,6.35,11.9,0.3,"Faktor Haus = nur Miete und Pacht; Faktor bei 50.000 € = mit Gastro-Gewinn bei 50.000 € Umsatz pro Monat.",size=11,color=GREY)
# 29 Wert
sl=page(d,SEC[3],f"Die Bank wird viel mehr Sicherheit verlangen: Beleihungsauslauf {Z['auslauf']*100:.0f} %","Vereinfachtes Ertragswertverfahren mit Annahmen; ein Gutachter der Bank ermittelt den verbindlichen Wert. Ratgeber 2026 nennen mind. 20 bis 30 % Eigenkapital.")
table(sl,0.7,1.95,5.8,[["Ertragswert","Betrag"],["Rohertrag pro Jahr (Mieten, Pacht)",eur(Z["roh"])],["Reinertrag nach Bewirtschaftung",eur(Z["rein"])],["Bodenwert (960 m² × 230 €)",eur(Z["boden"])],["Gebäudeertragswert",eur(Z["ew_geb"])],["Ertragswert gesamt",eur(Z["ew"])]],[3.6,2.2],size=13,rh=0.55,total=(5,))
table(sl,7.0,1.95,5.63,[["Beleihung","Betrag"],["Beleihungswert (niedrigerer Wert, −10 %)",eur(Z["bel"])],["Gesamtkosten und Darlehen",eur(Z["gesamt"])],["Beleihungsauslauf",f"{Z['auslauf']*100:.0f} %"],["Auslauf nur KfW-Darlehen",f"{Z['auslauf_kfw']*100:.0f} %"],["Über 80 % Auslauf",eur(Z["ek80"])]],[3.6,2.0],size=13,rh=0.55,total=(3,),neg=(3,))
tx(sl,0.7,5.55,11.9,1.1,[{"t":[("Heißt: ",{"bold":True,"color":GREEN}),(f"Der Ertragswert ({mio(Z['ew'])}) liegt weit unter den Kosten ({mio(Z['gesamt'])}). Für 80 % Beleihung braucht die Bank Eigenkapital oder Zusatzsicherheiten (Grundschulden auf weitere Immobilien, Bürgschaft) von ca. {mio(Z['ek80'])}.",{})]}],size=14)
# 30 Airbnb
sl=page(d,SEC[3],"Airbnb lohnt sich nicht: alle 8 Wohnungen bleiben langfristig vermietet","Rechnung aus den Bankunterlagen (Miete 11,18 €/m²); mit 10,90 €/m² ändert sich das Ergebnis nicht.")
table(sl,0.7,1.95,7.4,[["Zwei Apartments à","45 m²","60 m²","83 m²"],["Preis pro Nacht","80 €","95 €","115 €"],["Netto Airbnb je Apartment/Monat","535 €","636 €","770 €"],["Netto langfristige Miete","453 €","604 €","835 €"],["Möblierung (im Kredit)","27.000 €","36.000 €","49.800 €"],["Mehrertrag für 2 Apartments/Monat","−60 €","−236 €","−546 €"]],[3.4,1.3,1.3,1.4],size=13,rh=0.6,neg=(5,))
tx(sl,8.5,2.0,4.1,3.5,["Kein Apartment erreicht den nötigen Mehrertrag von 300 € im Monat.","Dazu kommen Aufwand, Reinigung und ab 12 Betten Sonderbau-Brandschutz."],size=15,space=12)
# 31 Risiken
sl=page(d,SEC[4],"Die größten Risiken und was wir dagegen tun")
rows=[["Risiko","Was passiert?","Was wir tun"],["Baupreis höher als 2.200 €/m²","Je +10 % ca. +"+eur(sens(Z)[5][1]-sens(Z)[0][1]).replace("−","")+" pro Monat Belastung","Angebote einholen, Holz-Staffel, Gewerke aus dem Netzwerk"],["Zins und Bankbedingungen","Zins +0,5 Punkte: Break-even-Umsatz 44.100 €","KfW-Zusage vor Baubeginn, Forward-Darlehen"],["Gastro-Umsatz unter 37.100 €","Gesamtergebnis fällt unter null","Erfahrener Betreiber, Pachtstaffel, Konzept prüfen"],["Genehmigung","Flachdach, Baugrenze (540 m² > ca. 440 m²), Stellplätze offen","Vorabstimmung mit der Stadt, Termin 09.11."],["Sicherheiten","Auslauf "+f"{Z['auslauf']*100:.0f}"+" %: ca. "+mio(Z["ek80"])+" Sicherheiten nötig","Grundschulden, Bürgschaft oder Eigenkapital"]]
table(sl,0.7,1.95,11.93,rows,[3,4.4,4.5],size=13,rh=0.78,align=["l","l","l"])
# 32 Brauche
sl=page(d,SEC[4],"Was ich von Stadt und Bank brauche")
tx(sl,0.7,1.95,5.8,0.4,"Von der Stadt",size=20,color=GREEN,font=HF)
tx(sl,0.7,2.6,5.8,4,[{"t":[("Genehmigung: ",{"bold":True}),("540 m² (Baugrenze), Staffelgeschoss, Flachdach und Höhe schriftlich bestätigen.",{})]},{"t":[("Stellplätze: ",{"bold":True}),("GRZ II mit wasserdurchlässigem Stein, Mitnutzung der Parkfläche oder faire Ablöse.",{})]},{"t":[("Grundstück: ",{"bold":True}),("230 €/m² mit Baureife, Reservierung bis zur Finanzierungszusage.",{})]}],size=15,space=12)
tx(sl,7.0,1.95,5.6,0.4,"Von der Bank",size=20,color=GREEN,font=HF)
tx(sl,7.0,2.6,5.6,4,[{"t":[("Darlehen: ",{"bold":True}),(f"{mio(Z['gesamt'])} mit KfW 298/299 und 12 Monaten Anlaufzeit ohne Tilgung.",{})]},{"t":[("Sicherheiten: ",{"bold":True}),(f"Grundschulden oder Bürgschaft von ca. {mio(Z['ek80'])} wegen des Beleihungsauslaufs.",{})]},{"t":[("KfW-Antrag: ",{"bold":True}),("für 298 und 299 vor Baubeginn über die Hausbank.",{})]}],size=15,space=12)
# 33 Schritte
sl=page(d,SEC[4],"Nächste Schritte bis zur Eröffnung Ende 2028")
st=[("Nov 2026","Termin Bürgermeister 09.11., Fragenliste"),("Nov–Dez 2026","Angebote für Rohbau, Zimmerei, Ausbau, Maler: Baupreis belegen"),("Dez 2026","Hausbank: KfW, Zinsen, Sicherheiten; Steuerberater"),("Q1 2027","Architekt, Energieberater (QNG), Bauantrag, KfW-Antrag"),("Mitte 2027","Baubeginn, 15 Monate Bauzeit"),("Ende 2028","Eröffnung zusammen mit der neuen Mitte")]
for i,(a,b_) in enumerate(st):
    y=1.95+i*0.78; rect(sl,0.7,y,0.5,0.5,TERRA if i==5 else GREEN,shape=MSO_SHAPE.OVAL); tx(sl,0.7,y,0.5,0.5,str(i+1),size=15,color=WHITE,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,font=HF); tx(sl,1.5,y+0.07,2.4,0.4,a,size=17,color=GREEN,font=HF,bold=True); tx(sl,4.0,y+0.09,8.5,0.4,b_,size=15)
