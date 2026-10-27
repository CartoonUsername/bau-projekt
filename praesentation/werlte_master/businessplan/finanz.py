"""Finanzmodell für den Businessplan je Variante – gleiche Rechenlogik und Annahmen wie der frühere Bankplan (8 Wohnungen / große Gastro, Stand Oktober 2026).
Rechenregeln (aus dem früheren Plan zurückgerechnet und nachgerechnet): Grundstück 230 €/m² + 7 %; Bau 2.200 €/m² BGF; Holzbau-Abschlag 400 €/m² auf das oberste Geschoss; Terrasse 450 €/m²; Baunebenkosten 15 %;
Effizienzhaus-40/QNG +3 % auf Bau + Nebenkosten; Ausbau 1.000 € je Gastro-Platz, Büro 150 €/m²; 100 % Fremdfinanzierung; KfW 298 150.000 € je Wohnung, KfW 299 2.000 € × 0,85 × Gewerbe-Nutzfläche; Rest Hausbank.
Zinsen KfW 297/298 2,5 %, KfW 299 3,0 %, Hausbank 4,0 %; 1 % Tilgung; Bauzeit 15 + Anlauf 12 Monate. ALLES PLANUNGSANNAHMEN, nichts bestätigt."""
import math
P = dict(gr_m2=960.0, gr_preis=230.0, nk_grund=0.07, bau_m2=2200.0, holz_abschlag=400.0, terr_m2=450.0, bnk=0.15, eh40=0.03, platz_ausbau=1000.0, buero_ausbau=150.0,
         kfw298_we=150000.0, kfw299_m2=2000.0, kfw299_f=0.85, z298=0.025, z299=0.030, zbank=0.040, tilg=0.01, bauzeit=15, anlauf=12, bereit=0.03, bereit_ab=7,
         m_wohn=11.18, m_buero=9.75, pacht=10.0, ruecklage=0.10, marge=0.305, umsatz_platz=65010.0 / 190, steuer=0.35, afa=0.03, aussen_m2=160.0, reserve_aussen=True)
def rate_ann(L, z, t): return L * (z + t)
def rechne(v, p=P, umsatz=None, ohne_gastro=False):
    """v: dict(bgf, bgf_top, terr, wfl, we, gastro_nf, buero_nf, plaetze, aussen_m2)"""
    r = {}
    grund = p["gr_m2"] * p["gr_preis"] * (1 + p["nk_grund"])
    bau = v["bgf"] * p["bau_m2"]; abs_ = -v["bgf_top"] * p["holz_abschlag"]; terr = v["terr"] * p["terr_m2"]
    bnk = (bau + abs_ + terr) * p["bnk"]; eh = (bau + abs_ + terr + bnk) * p["eh40"]
    ausb = v["plaetze"] * p["platz_ausbau"] + v["buero_nf"] * p["buero_ausbau"]
    aussen = v.get("aussen_m2", 0) * p["aussen_m2"]
    c0 = grund + bau + abs_ + terr + bnk + eh + ausb + aussen
    r["posten"] = [("Grundstück inkl. Steuer und Notar", grund), ("Bau, Massivbau", bau), ("Abschlag Holzbau (oberstes Geschoss)", abs_), ("Dachterrassen (nicht in BGF)", terr), ("Baunebenkosten", bnk), ("Mehrkosten Effizienzhaus 40 und QNG", eh), ("Ausbau Gastro und Büros", ausb), ("Außenanlagen, Stellplätze (hypothetische Fläche)", aussen)]
    # Finanzierungskosten (Näherung, iterativ): Bauzeitzinsen auf 50 % mittleren Abruf, Bereitstellung ab Monat 7, Vollverzinsung in der Anlaufzeit
    wk = 298
    kfw_w = min(p["kfw298_we"] * v["we"], c0 * 0.6); kfw_g = p["kfw299_m2"] * p["kfw299_f"] * (v["gastro_nf"] + v["buero_nf"])
    fin = 0.0
    for _ in range(50):
        tot = c0 + fin; bank = max(tot - kfw_w - kfw_g, 0); mz = (kfw_w * p["z298"] + kfw_g * p["z299"] + bank * p["zbank"]) / tot
        bauz = c0 * 0.5 * mz * p["bauzeit"] / 12; und = 1 - p["bereit_ab"] / p["bauzeit"]; bere = c0 * (und / 2) * p["bereit"] * (p["bauzeit"] - p["bereit_ab"]) / 12
        anl = (c0 + bauz + bere) * mz * p["anlauf"] / 12; fin_n = bauz + bere + anl
        if abs(fin_n - fin) < 1: break
        fin = fin_n
    tot = c0 + fin; bank = max(tot - kfw_w - kfw_g, 0); mz = (kfw_w * p["z298"] + kfw_g * p["z299"] + bank * p["zbank"]) / tot
    r["posten"].append(("Finanzierungskosten (Bauzeit, Bereitstellung, Anlaufzeit)", fin)); r["gesamt"] = tot; r["fin"] = fin
    r["kfw_w"], r["kfw_g"], r["bank"], r["mischzins"] = kfw_w, kfw_g, bank, mz
    # Kapitaldienst (jährlich) und Tilgungsplan monatlich je Darlehen
    loans = [(kfw_w, p["z298"]), (kfw_g, p["z299"]), (bank, p["zbank"])]
    r["rate_m"] = sum(L * (z + p["tilg"]) / 12 for L, z in loans); r["rate_j"] = r["rate_m"] * 12
    r["rate_je"] = [(L, z, L * (z + p["tilg"]) / 12) for L, z in loans]
    plan = []; bal = [L for L, _ in loans]
    for yr in range(1, 36):
        zi = ti = 0.0
        for m in range(12):
            for i, (L, z) in enumerate(loans):
                pay = L * (z + p["tilg"]) / 12; ii = bal[i] * z / 12; tt = min(pay - ii, bal[i]); bal[i] -= tt; zi += ii; ti += tt
        plan.append((yr, zi, ti, sum(bal)))
    r["plan"] = plan
    # Erträge
    wohn = v["wfl"] * p["m_wohn"] * 12; buero = v["buero_nf"] * p["m_buero"] * 12; pacht = v["gastro_nf"] * p["pacht"] * 12
    roh = wohn + buero + pacht; rueck = roh * p["ruecklage"]; netto_imm = roh - rueck
    um = umsatz if umsatz is not None else v["plaetze"] * p["umsatz_platz"]
    gastro_vor = um * p["marge"] * 12; gastro_nach = gastro_vor - pacht
    if ohne_gastro: gastro_nach = -0.0; gastro_nach = 0.0; netto_imm = roh - rueck - pacht
    vor = netto_imm + gastro_nach; cash = vor - r["rate_j"]
    r.update(wohn=wohn, buero=buero, pacht=pacht, roh=roh, rueck=rueck, netto_imm=netto_imm, umsatz=um, gastro_nach=gastro_nach, gastro_vor=gastro_vor, vor=vor, cash=cash)
    z1 = r["plan"][0][1]; t1 = r["plan"][0][2]
    r.update(zins1=z1, tilg1=t1, dscr_ges=vor / r["rate_j"], dscr_imm=netto_imm / r["rate_j"], dscr_wb=(wohn + buero - (wohn + buero) * p["ruecklage"]) / r["rate_j"], zinsdeck=vor / z1,
             rendite_imm=netto_imm / tot, rendite_ges=vor / tot)
    afa_basis = tot - grund - fin; afa = afa_basis * p["afa"]; gew = vor - z1 - afa
    r.update(afa=afa, gewinn_steuer=gew, steuer=max(gew, 0) * p["steuer"], nach_steuer=cash - max(gew, 0) * p["steuer"])
    # Ertragswert (vereinfacht, Annahmen: Liegenschaftszins Wohnen 3,85 %, Büro 5,35 %, Gastro 6,35 % (an den früheren Plan angeglichen), Restnutzungsdauer 60 Jahre, Bewirtschaftung 13,75 % Rohertrag)
    bew = roh * 0.1375; rein = roh - bew; boden = p["gr_m2"] * p["gr_preis"]
    def vf(z, n=60): return (1 - (1 + z) ** -n) / z
    parts = {"Wohnen": (wohn, 0.0385), "Büro": (buero, 0.0535), "Gastro": (pacht, 0.0635)}; ew_geb = 0.0; ew_part = {}
    for k, (e, z) in parts.items():
        rk = e * (1 - 0.1375); g = max(rk - boden * z * (e / roh if roh else 0), 0) * vf(z); ew_part[k] = g + boden * (e / roh if roh else 0); ew_geb += g
    ew = ew_geb + boden; sach = boden + (tot - grund - fin) ; beleih = min(ew, sach) * 0.9
    r.update(bew=bew, rein=rein, boden=boden, ew_geb=ew_geb, ew=ew, ew_part=ew_part, sach=sach, beleih=beleih, auslauf=tot / beleih, ueber80=tot - 0.8 * beleih)
    return r
if __name__ == "__main__":
    old = dict(bgf=1650, bgf_top=498, terr=77, wfl=655, we=8, gastro_nf=510, buero_nf=165, plaetze=190, aussen_m2=0)
    P2 = dict(P, m_wohn=11.18, m_buero=(100 * 9.5 + 65 * 10) / 165); r = rechne(old, P2, umsatz=65010)
    for k in ("gesamt", "fin", "kfw_w", "kfw_g", "bank", "mischzins", "rate_m", "roh", "netto_imm", "gastro_nach", "vor", "cash", "zins1", "tilg1", "afa", "gewinn_steuer", "ew", "beleih", "auslauf"): print(k, round(r[k], 3))
