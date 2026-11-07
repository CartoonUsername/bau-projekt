"""Vollmodell Baufeld 3 (540 m², 8 WE + Gastro 460 m²), Nachbau von Bankunterlagen_Baufeld3.xlsx mit Parametern."""
import sys
sys.path.insert(0,"/home/user/bau-projekt/praesentation/werlte_master/plan_8WE/einzel")
BASE=dict(bau=2200.0,holz=400.0,bnk=0.15,eh=0.03,dz=0.0,umsatz=50000.0,marge=0.305,miete=11.176,pacht=12.0,rl=0.10,
          grund=236256.0,ausbau=150000.0,terr=32400.0,kfw298=1200000.0,kfw299=782000.0,z298=0.025,z299=0.030,zb=0.040,til=0.01)
BGF=1540.0; WF=725.0; GNF=460.0
def model(**kw):
    p=dict(BASE); p.update(kw); m=dict(p)
    z298,z299,zb=p["z298"]+p["dz"],p["z299"]+p["dz"],p["zb"]+p["dz"]
    m.update(z298=z298,z299=z299,zb=zb)
    bau_roh=BGF*p["bau"]; abschlag=-460*p["holz"]
    m["bau_roh"]=bau_roh; m["abschlag"]=abschlag; m["terr_k"]=p["terr"]
    m["bau"]=bau_roh+abschlag+p["terr"]
    m["bnk_k"]=m["bau"]*p["bnk"]; m["eh_k"]=(m["bau"]+m["bnk_k"])*p["eh"]
    inv=p["grund"]+m["bau"]+m["bnk_k"]+m["eh_k"]+p["ausbau"]; m["inv"]=inv
    # Bauphase
    k298,k299=p["kfw298"],p["kfw299"]; s1,s2=k298/inv,k299/inv; s3=1-s1-s2
    st1=st2=st3=0.0; fin=0.0; bau_sum=inv-p["grund"]; off=bau_sum
    for mo in range(0,28):
        if mo==0: aus=p["grund"]; offen=bau_sum
        elif mo<=15: aus=bau_sum/15; offen=bau_sum-(mo-1)*bau_sum/15
        else: aus=0.0; offen=0.0
        if mo<=15:
            zi1=st1*z298/12; zi2=st2*z299/12; zi3=st3*zb/12
            bere=0.03/12*offen if mo>=7 else 0.0
            a1=aus*s1;a2=aus*s2
            if mo==15: a1=k298-st1; a2=k299-st2   # Abruf bis Rahmen
            a3=aus*s3+zi1+zi2+zi3+bere
        else:
            zi1=k298*z298/12; zi2=k299*z299/12; zi3=st3*zb/12; bere=0.0; a1=a2=0.0; a3=zi1+zi2+zi3
        fin+=zi1+zi2+zi3+bere
        st1+=a1; st2+=a2; st3+=a3
    m["fin"]=fin; m["gesamt"]=inv+fin; m["hb"]=m["gesamt"]-k298-k299
    # Kapitaldienst
    L=[(k298,z298),(k299,z299),(m["hb"],zb)]; m["loans"]=L
    m["kd_j"]=sum(l*(z+p["til"]) for l,z in L); m["kd_m"]=m["kd_j"]/12
    m["zins1"]=sum(l*z for l,z in L)
    m["mischzins"]=m["zins1"]/m["gesamt"]
    # Ertrag
    m["miete_j"]=WF*p["miete"]*12; m["pacht_j"]=GNF*p["pacht"]*12
    m["roh"]=m["miete_j"]+m["pacht_j"]; m["rueck"]=m["roh"]*p["rl"]; m["netto_imm"]=m["roh"]-m["rueck"]
    m["gewinn_vp"]=p["umsatz"]*12*p["marge"]; m["betrieb"]=m["gewinn_vp"]-m["pacht_j"]
    m["netto_ges"]=m["netto_imm"]+m["betrieb"]; m["erg"]=m["netto_ges"]-m["kd_j"]
    m["dscr_ges"]=m["netto_ges"]/m["kd_j"]; m["dscr_imm"]=m["netto_imm"]/m["kd_j"]
    m["dscr_wohn"]=m["miete_j"]*(1-p["rl"])/m["kd_j"]
    m["zinsdeckung"]=m["netto_ges"]/m["zins1"]; m["rendite"]=m["netto_imm"]/m["gesamt"]
    m["be_umsatz"]=((m["kd_j"]-m["netto_imm"]+m["pacht_j"])/p["marge"])/12
    # Tilgungsplan (monatlich je Darlehen)
    bal=[l for l,z in L]; hist=[]
    for yr in range(1,36):
        zi=ti=0.0
        for mo in range(12):
            for i,(l,z) in enumerate(L):
                pay=l*(z+p["til"])/12; ins=bal[i]*z/12; t=pay-ins; bal[i]-=t; zi+=ins; ti+=t
        hist.append((yr,zi,ti,sum(bal)))
    m["tilg"]=hist; m["rest10"]=hist[9][3]
    # Ertragswert
    verw_w=8*360; inst_w=WF*12; mausf_w=0.02*m["miete_j"]; verw_g=0.03*m["pacht_j"]; inst_g=GNF*8; mausf_g=0.04*m["pacht_j"]
    bew=verw_w+inst_w+mausf_w+verw_g+inst_g+mausf_g; m["bew"]=bew
    rein=m["roh"]-bew; boden=960*230; bv=boden*0.045; q=1.045
    vf=(1-q**-80)/0.045; geb=(rein-bv)*vf; ew=geb+boden
    m.update(rein=rein,boden=boden,vf=vf,ew_geb=geb,ew=ew)
    sach=boden+m["bau"]+m["bnk_k"]+m["eh_k"]; m["sach"]=sach
    bel=min(sach,ew)*0.9; m["bel"]=bel; m["auslauf"]=m["gesamt"]/bel; m["auslauf_kfw"]=(k298+k299)/bel
    m["ew_luecke"]=ew-m["gesamt"]; m["ek80"]=m["gesamt"]-0.8*bel
    # Prognose
    prog=[]
    for t in range(10):
        g=1.015**t; mj=m["miete_j"]*g; pj=m["pacht_j"]*g; rk=(mj+pj)*p["rl"]; bet=(m["gewinn_vp"]*g-pj)
        net=mj+pj-rk+bet; prog.append((t+1,mj,pj,rk,bet,net,net-m["kd_j"],net/m["kd_j"],hist[t][3]))
    m["prog"]=prog
    return m
def sens(m):
    p=m; base=m["erg"]/12; kd=m["kd_j"]; out=[("Plan",base,m["dscr_ges"])]
    d=m["rest10"]*0.01/12; out.append(("Anschlusszins nach 10 Jahren +1 Prozentpunkt (auf Restschuld)",base-d,(m["netto_ges"]-0)/(kd+d*12)))
    d=m["miete_j"]*0.1*(1-m["rl"])/12; out.append(("Mieten Wohnen −10 %",base-d,(m["netto_ges"]-d*12)/kd))
    for pct in (0.2,0.4):
        d=m["umsatz"]*pct*m["marge"]; out.append((f"Gastro-Umsatz −{int(pct*100)} %",base-d,(m["netto_ges"]-d*12)/kd))
    dk=(m["bau"]*0.1)*(1+m["bnk"])*(1+m["eh"])*(1+m["fin"]/m["inv"]); d=dk*(m["zb"]+m["til"])/12
    out.append(("Baukosten +10 % (Kredit steigt entsprechend, Hausbank)",base-d,m["netto_ges"]/(kd+d*12)))
    d=(m["pacht_j"]*(1-m["rl"])+m["betrieb"])/12; out.append(("Gastro fällt ganz aus (keine Pacht, kein Betriebsergebnis)",base-d,(m["netto_ges"]-d*12)/kd))
    return out
if __name__=="__main__":
    m=model()
    for k in ("inv","fin","gesamt","hb","kd_m","mischzins","dscr_ges","dscr_imm","zinsdeckung","rend" if False else "rendite","be_umsatz","rest10","ew","bel","auslauf","ek80"): print(k,round(m[k],4))
