"""Einzelrechnung je Einheit (GbR/UG-Sicht): jede Wohnung und die Gastro werden mit eigenen Kosten, eigener Finanzierung und eigener Miete gerechnet.
Eingaben aus Bankunterlagen_Baufeld3.xlsx (Stand 19.10.2026, 540 m², Gastro 460 m², 8 Wohnungen). Annahmen wie im Rechenmodell: Bau 2.200 €/m² BGF, Holzabschlag 400 €/m² (Staffel), Terrasse 32.400 € (Staffel), BNK 15 %, EH40/QNG 3 %, Gastro-Ausbau 150.000 €, Rücklage 10 %, KfW 298 150.000 € je WE (2,5 %), KfW 299 2.000 € × 85 % × Gastro-NF (3,0 %), Hausbank 4,0 %, Tilgung 1 %.
Zuordnung (Annahme): Kosten nach BGF; Erschließung/Kern im EG (80 m²) wird auf die Wohnungen umgelegt; Finanzierungskosten anteilig an den Investitionskosten."""
P=dict(bau=2200.0, holz=400.0, terr=32400.0, bnk=0.15, eh=0.03, grund=236256.0, ausbau=150000.0, fin=271065.9, ruecklage=0.10, kfw298=150000.0, z298=0.025, z299=0.030, zbank=0.040, til=0.01, kfw299_m2=2000.0*0.85)
def units(p=P, pacht=12.0, miete=11.176, umsatz=50000.0, marge=0.305):
    WE=[("WE %d"%i,"1. OG",83.0,540/5*(1-80/540)) for i in range(1,6)]+[("WE %d"%i,"Staffel",310/3,460/3) for i in range(6,9)]
    # BGF: OG1 540/5 je WE; Staffel 460/3; Kern 80 m² EG wird auf 8 WE umgelegt
    ue=[]; kern=80.0
    for n,g,nf,bgf in WE:
        bgf_tot = (540/5 if g=="1. OG" else 460/3) + kern/8
        ue.append(dict(name=n,geschoss=g,nf=nf,bgf=bgf_tot,typ="WE"))
    ue.append(dict(name="Gastro",geschoss="EG",nf=460.0,bgf=540.0-kern,typ="Gastro"))
    tot_bgf=sum(u["bgf"] for u in ue)
    for u in ue:
        bau=p["bau"]*u["bgf"]; terr=0.0
        if u["geschoss"]=="Staffel": bau=bau-p["holz"]*(460/3)+p["terr"]/3; terr=0.0
        bnk=bau*p["bnk"]; eh=(bau+bnk)*p["eh"]; grund=p["grund"]*u["bgf"]/tot_bgf; aus=p["ausbau"] if u["typ"]=="Gastro" else 0.0
        u["invest"]=bau+terr+bnk+eh+grund+aus
    ti=sum(u["invest"] for u in ue)
    for u in ue:
        u["fin"]=p["fin"]*u["invest"]/ti; u["kosten"]=u["invest"]+u["fin"]
        if u["typ"]=="WE":
            u["kfw"]=min(p["kfw298"],u["kosten"]); u["z_kfw"]=p["z298"]; u["rent"]=u["nf"]*miete*12
        else:
            u["kfw"]=min(p["kfw299_m2"]*u["nf"],u["kosten"]); u["z_kfw"]=p["z299"]; u["rent"]=u["nf"]*pacht*12
        u["bank"]=u["kosten"]-u["kfw"]
        u["rate"]=u["kfw"]*(u["z_kfw"]+p["til"])+u["bank"]*(p["zbank"]+p["til"])
        u["netto"]=u["rent"]*(1-p["ruecklage"]); u["dscr"]=u["netto"]/u["rate"]
        u["rate_kfw"]=u["kfw"]*(u["z_kfw"]+p["til"]); u["dscr_kfw"]=u["netto"]/u["rate_kfw"]; u["ek"]=u["kosten"]-u["kfw"]
        # Eigenkapital je Einheit, damit DSCR 1,0 bzw. 1,2 mit Hausbank-Rest
        for tgt in (1.0,1.2):
            allowed=u["netto"]/tgt - u["rate_kfw"]; hb=max(allowed,0)/(p["zbank"]+p["til"]); u["ek%s"%tgt]=max(u["kosten"]-u["kfw"]-hb,0)
    g=[u for u in ue if u["typ"]=="Gastro"][0]
    betrieb=umsatz*marge-g["rent"]/12
    return ue, betrieb
if __name__=="__main__":
    ue,bet=units()
    print("%-7s %-8s %6s %7s %9s %9s %9s %9s %6s %9s %9s"%("Einheit","Geschoss","NF","BGF","Kosten","KfW","Hausbank","Rate/J","DSCR","DSCR KfW","EK 1,0"))
    for u in ue: print("%-7s %-8s %6.1f %7.1f %9.0f %9.0f %9.0f %9.0f %6.2f %9.2f %9.0f"%(u["name"],u["geschoss"],u["nf"],u["bgf"],u["kosten"],u["kfw"],u["bank"],u["rate"],u["dscr"],u["dscr_kfw"],u["ek1.0"]))
    print("Summe Kosten",round(sum(u["kosten"] for u in ue)),"Rate",round(sum(u["rate"] for u in ue)),"Netto",round(sum(u["netto"] for u in ue)),"DSCR",round(sum(u["netto"] for u in ue)/sum(u["rate"] for u in ue),2),"Betrieb/Monat",round(bet))
