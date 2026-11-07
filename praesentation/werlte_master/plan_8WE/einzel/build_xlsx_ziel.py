from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
wb=Workbook(); ws=wb.active; ws.title="Einzelrechnung"
blue=Font(color="0000FF"); b=Font(bold=True)
ws["A1"]="Neue Mitte Werlte – Baufeld 3: Einzelrechnung je Einheit (Zielwerte Bau 1.450 €/m², Holz-Staffel)"; ws["A1"].font=Font(bold=True,size=13)
inp=[("Baukosten €/m² BGF (ANNAHME Zielpreis)",1450),("Holzabschlag Staffel €/m² (ANNAHME)",700),("Terrasse Staffel gesamt €",32400),
("Baunebenkosten",0.15),("Effizienzhaus/QNG-Mehrkosten",0.03),("Grundstück gesamt €",236256),("Gastro-Ausbau €",150000),
("Finanzierungskosten (% der Investition)",271065.9/4219771.8),("Zins KfW 298",0.025),("Zins KfW 299",0.03),("Zins Hausbank",0.04),
("Tilgung",0.01),("Rücklage (% der Miete)",0.10),("Miete Wohnung €/m²/Monat",11.176),("Pacht Gastro €/m²/Monat",12.0),
("KfW 298 je Wohnung €",150000),("KfW 299 €/m² Gastro-NF",1700),("Ziel-DSCR",1.0)]
for i,(k,v) in enumerate(inp):
    r=3+i; ws.cell(r,1,k); c=ws.cell(r,2,v); c.font=blue
    c.number_format="0.0%" if isinstance(v,float) and v<1 and "Miete" not in k and "Ziel" not in k else "#,##0.00" if isinstance(v,float) else "#,##0"
ws["B10"].number_format="0.00%"
I={n:f"$B${3+i}" for i,n in enumerate(["bau","holz","terr","bnk","eh","grund","aus","fin","z298","z299","zb","til","rl","miete","pacht","k298","k299","ziel"])}
h=["Einheit","Geschoss","NF m²","BGF m² (inkl. Kern)","Bau €","Terrasse €","Nebenkosten €","EH-Mehrkosten €","Grundstück €","Ausbau €","Investition €","Finanz.-Kosten €","Kosten gesamt €","KfW €","Hausbank €","Kapitaldienst €/J","Miete/Pacht €/J","Netto €/J","DSCR","DSCR nur KfW-Teil","Eigenkapital für Ziel-DSCR €"]
R0=23
for j,t in enumerate(h,1):
    c=ws.cell(R0,j,t); c.font=b; c.fill=PatternFill("solid",fgColor="DDDDDD"); c.alignment=Alignment(wrap_text=True)
rows=[(f"WE {i}","1. OG",83.0,540/5+10) for i in range(1,6)]+[(f"WE {i}","Staffel",310/3,460/3+10) for i in range(6,9)]+[("Gastro","EG",460.0,460.0)]
f,l=R0+1,R0+len(rows)
for k,(n,g,nf,bgf) in enumerate(rows):
    r=R0+1+k; gas=n=="Gastro"; st=g=="Staffel"
    ws.cell(r,1,n); ws.cell(r,2,g); ws.cell(r,3,nf); ws.cell(r,4,bgf)
    ws.cell(r,5,f"={I['bau']}*D{r}"+(f"-{I['holz']}*460/3+{I['terr']}/3" if st else ""))
    ws.cell(r,6,0)
    ws.cell(r,7,f"=E{r}*{I['bnk']}"); ws.cell(r,8,f"=(E{r}+G{r})*{I['eh']}")
    ws.cell(r,9,f"={I['grund']}*D{r}/SUM($D${f}:$D${l})"); ws.cell(r,10,f"={I['aus']}" if gas else 0)
    ws.cell(r,11,f"=E{r}+F{r}+G{r}+H{r}+I{r}+J{r}"); ws.cell(r,12,f"=K{r}*{I['fin']}"); ws.cell(r,13,f"=K{r}+L{r}")
    z=I['z299'] if gas else I['z298']; kf=f"{I['k299']}*C{r}" if gas else I['k298']
    ws.cell(r,14,f"=MIN({kf},M{r})"); ws.cell(r,15,f"=M{r}-N{r}")
    ws.cell(r,16,f"=N{r}*({z}+{I['til']})+O{r}*({I['zb']}+{I['til']})")
    ws.cell(r,17,f"=C{r}*{I['pacht'] if gas else I['miete']}*12"); ws.cell(r,18,f"=Q{r}*(1-{I['rl']})")
    ws.cell(r,19,f"=R{r}/P{r}"); ws.cell(r,20,f"=R{r}/(N{r}*({z}+{I['til']}))")
    ws.cell(r,21,f"=MAX(M{r}-N{r}-MAX(R{r}/{I['ziel']}-N{r}*({z}+{I['til']}),0)/({I['zb']}+{I['til']}),0)")
    for c in range(3,22): ws.cell(r,c).number_format="0.00" if c in (19,20) else "#,##0"
t=l+1; ws.cell(t,1,"Summe").font=b
for c in "CDEFGHIJKLMNOPQRU":
    ws[f"{c}{t}"]=f"=SUM({c}{f}:{c}{l})"; ws[f"{c}{t}"].number_format="#,##0"; ws[f"{c}{t}"].font=b
ws[f"S{t}"]=f"=R{t}/P{t}"; ws[f"S{t}"].number_format="0.00"; ws[f"S{t}"].font=b
ws.cell(t+2,1,"Hinweise: KfW-Förderdarlehen (298: 150.000 € je WE zu 2,5 %; 299: 1.700 €/m² Gastro-NF zu 3,0 %) sind in DSCR bereits enthalten; Rest Hausbank 4,0 %. Blau = Eingaben. Baupreis, Holzabschlag und KfW 299 (1.700 €/m²) sind ANNAHMEN bzw. Zielwerte und noch nicht durch Angebote belegt. DSCR ohne Gastro-Betriebsgewinn. Keine Aussage zur baurechtlichen Zulässigkeit.")
ws.column_dimensions["A"].width=40
for c in range(2,22): ws.column_dimensions[ws.cell(1,c).column_letter].width=14
wb.save("Einzelrechnung_Einheiten_Ziel1450.xlsx")
