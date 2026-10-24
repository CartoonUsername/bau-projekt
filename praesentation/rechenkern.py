"""Unabhängiger Nachbau des Rechenmodells (Decimal, ohne Excel) zum Gegenprüfen jeder Zahl.
Bildet Kosten, Bauphase, KfW-Stapel, Tilgung und Ertrag der Vermietungs-GbR nach (Stand Oktober 2026)."""
from decimal import Decimal as D, getcontext
getcontext().prec = 40

def run(n_we=8, umsatz=D(65010), moeb=D(0), airbnb_net=D(0), airbnb_m2=D(0), eigenkapital=D(0), pacht_m2=D(10), miete_m2=None, mehr_we=D(15000), pacht_quote=D('0.10'), buero_m2=(D(9.5), D(10))):
    miete_m2 = D(950) / D(85) if miete_m2 is None else D(miete_m2)
    # ---- Kosten
    land = D(960) * 230; gres = land * D("0.05"); notar = land * D("0.02"); land_ges = land + gres + notar
    bgf = D(576 + 576 + 498)
    bau = bgf * 2200 - D(498) * 400 + D(77) * 450
    bnk = bau * D("0.15"); eh40 = (bau + bnk) * D("0.03")
    ausbau = D(190000) + (D(100) + D(65)) * 150 + moeb + mehr_we * max(0, n_we - 8)
    invest = land_ges + bau + bnk + eh40 + ausbau
    # ---- KfW-Rahmen und Finanzierungsstapel (Eigenkapital ersetzt zuerst Hausbank, dann KfW 299, dann KfW 298)
    kfw_w_cap = D(n_we) * 150000
    kfw_g_cap = (D(510) + 100 + 65) * D("0.85") * 2000
    Tw = min(invest, kfw_w_cap); Tg = min(invest - Tw, kfw_g_cap); Tb = invest - Tw - Tg
    ek = D(eigenkapital)
    take = min(ek, Tb); Tb -= take; rest = ek - take
    take = min(rest, Tg); Tg -= take; rest -= take
    take = min(rest, Tw); Tw -= take; rest -= take
    sw, sg, sb = Tw / invest, Tg / invest, Tb / invest
    se = ek / invest
    z_w, z_g, z_b = D("0.025"), D("0.03"), D("0.04")
    bau_rest = invest - land_ges
    mon = bau_rest / 15
    Lw = land_ges * sw; Lg = land_ges * sg
    Lb = land_ges * sb
    zins_sum = D(0); bereit_sum = D(0)
    for m in range(1, 28):
        spend = mon if m <= 15 else D(0)
        offen = bau_rest - mon * (m - 1) if m <= 15 else D(0)
        zw = Lw * z_w / 12; zg = Lg * z_g / 12; zb = Lb * z_b / 12
        ber = offen * D("0.03") / 12 if 7 <= m <= 15 else D(0)
        Lw += spend * sw; Lg += spend * sg
        Lb += spend * sb + zw + zg + zb + ber
        zins_sum += zw + zg + zb + ber
    fin_kosten = zins_sum
    gesamt = invest + fin_kosten
    check = (Lw + Lg + Lb + ek) - (invest + fin_kosten)
    # ---- Rate
    rate_w = Lw * (z_w + D("0.01")) / 12; rate_g = Lg * (z_g + D("0.01")) / 12; rate_b = Lb * (z_b + D("0.01")) / 12
    rate = rate_w + rate_g + rate_b
    # Jahr 1 Zinsen/Tilgung und Restschuld nach 120 Monaten
    def sched(L, z, r, months):
        zs = D(0); ts = D(0)
        for i in range(months):
            zi = L * z / 12; ti = r - zi; L -= ti; zs += zi; ts += ti
        return L, zs, ts
    out = {}
    for name, L, z, r in (("w", Lw, z_w, rate_w), ("g", Lg, z_g, rate_g), ("b", Lb, z_b, rate_b)):
        out[name] = [sched(L, z, r, 12), sched(L, z, r, 120)]
    zins1 = sum(out[k][0][1] for k in out); tilg1 = sum(out[k][0][2] for k in out)
    rest10 = sum(out[k][1][0] for k in out)
    # ---- Ertrag (monatlich)
    wohn_m2 = D(655)
    miete_lang = (wohn_m2 - airbnb_m2) * miete_m2
    buero = D(100) * D(buero_m2[0]) + D(65) * D(buero_m2[1])
    pacht = max(D(510) * D(pacht_m2), D(umsatz) * D(pacht_quote))
    rueck = (miete_lang + buero + pacht) * D("0.1")
    netto_immo = miete_lang + buero + pacht - rueck + airbnb_net
    gastro = umsatz * D("0.305") - pacht  # Betreiber-Ergebnis nach Pacht
    kd = rate
    ergebnis = netto_immo - kd  # Ergebnis der Vermietungs-GbR
    return dict(invest=invest, land_ges=land_ges, fin=fin_kosten, gesamt=gesamt, check=check, sw=sw, sg=sg, sb=sb,
                Lw=Lw, Lg=Lg, Lb=Lb, rate=rate, rate_w=rate_w, rate_g=rate_g, rate_b=rate_b, zins1=zins1, tilg1=tilg1, rest10=rest10,
                miete=miete_lang, buero=buero, pacht=pacht, rueck=rueck, netto_immo=netto_immo, gastro=gastro, ergebnis=ergebnis,
                umsatz=umsatz, ek=ek, gesamt_bauherr=netto_immo + gastro - kd, roh=(miete_lang + buero + pacht) * 12)

if __name__ == "__main__":
    r = run()
    for k, v in r.items(): print(k, round(v, 4))
