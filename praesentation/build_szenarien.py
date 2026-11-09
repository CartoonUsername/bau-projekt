"""Rechnet die Szenarien 8 und 12 Wohnungen (je ohne und mit Eigenkapital) mit dem unabhängigen Rechenkern
und schreibt szenarien.json. Das Excel-Blatt 'Szenarien' und die Dokumente lesen diese Datei."""
import json
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_CEILING
from rechenkern import run

UMSATZ = D(95635)
STEUER = D("0.35")
WOHNFL = D(655); BUERO = D(165); GASTRO = D(510)

def q(x):
    return float(D(x).quantize(D("0.01"), ROUND_HALF_UP))

def kennzahlen(n, ek, name):
    r = run(n_we=n, umsatz=UMSATZ, eigenkapital=D(ek))
    kfw = r["Lw"] + r["Lg"]
    dscr = r["netto_immo"] / r["rate"]
    cash = 12 * r["ergebnis"]
    geb = r["gesamt"] - r["land_ges"] - r["fin"]
    afa = D("0.03") * geb
    gewinn = 12 * r["netto_immo"] - r["zins1"] - afa
    wa = WOHNFL / (WOHNFL + BUERO + GASTRO)
    afa_opt = geb * (wa * (D("0.05") + D("0.05")) + (1 - wa) * D("0.03"))
    gewinn_opt = 12 * r["netto_immo"] - r["zins1"] - afa_opt
    zinsvorteil = r["Lw"] * (D("0.04") - D("0.025")) + r["Lg"] * (D("0.04") - D("0.03"))
    mischzins = (r["Lw"] * D("0.025") + r["Lg"] * D("0.03") + r["Lb"] * D("0.04")) / (r["Lw"] + r["Lg"] + r["Lb"])
    out = dict(name=name, we=n, ek=q(ek), gesamt=q(r["gesamt"]), fin=q(r["fin"]), kfw=q(kfw), kfw298=q(r["Lw"]), kfw299=q(r["Lg"]), bank=q(r["Lb"]),
               mischzins=float(mischzins), zinsvorteil=q(zinsvorteil), rate=q(r["rate"]), netto_immo=q(r["netto_immo"]), pacht=q(r["pacht"]),
               ergebnis_m=q(r["ergebnis"]), ergebnis_j=q(cash), dscr=float(dscr), betreiber_m=q(r["gastro"]), gesamt_bauherr_m=q(r["gesamt_bauherr"]),
               zins1=q(r["zins1"]), tilg1=q(r["tilg1"]), afa=q(afa), gewinn=q(gewinn), afa_opt=q(afa_opt), gewinn_opt=q(gewinn_opt))
    kopf = {}
    for k in (1, 2, 4, 8):
        steuer = STEUER * gewinn / k
        steuer_opt = STEUER * gewinn_opt / k
        kopf[str(k)] = dict(ek=q(D(ek) / k), cash_m=q(cash / 12 / k), cash_j=q(cash / k), cash_steuer_m=q((cash / k - steuer) / 12),
                            cash_steuer_j=q(cash / k - steuer), cash_opt_m=q((cash / k - steuer_opt) / 12), cash_opt_j=q(cash / k - steuer_opt), tilg_j=q(r["tilg1"] / k))
    out["kopf"] = kopf
    out["faktor"] = q(r["gesamt"] / cash) if cash > 0 else None
    out["vervielf"] = q(r["gesamt"] / (12 * r["netto_immo"]))
    out["faktor_bauherr"] = q(r["gesamt"] / (12 * r["gesamt_bauherr"]))
    out["ek_rendite"] = float(cash / D(ek)) if D(ek) > 0 else None
    return out

def ek_fuer_dscr(n, ziel=D("1.2")):
    lo, hi = D(0), D(4000000)
    for _ in range(100):
        mid = (lo + hi) / 2
        r = run(n_we=n, umsatz=UMSATZ, eigenkapital=mid)
        if r["netto_immo"] / r["rate"] >= ziel:
            hi = mid
        else:
            lo = mid
    return (hi / 1000).to_integral_value(ROUND_CEILING) * 1000

if __name__ == "__main__":
    res = []
    for n in (12, 8):
        res.append(kennzahlen(n, 0, f"{n} Wohnungen, kein Eigenkapital"))
    for n in (12, 8):
        ek = ek_fuer_dscr(n)
        res.append(kennzahlen(n, ek, f"{n} Wohnungen, Eigenkapital für Deckung 1,2"))
    json.dump(res, open("szenarien.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for r in res:
        print(r["name"], "| EK", r["ek"], "| Gesamt", r["gesamt"], "| Rate", r["rate"], "| Erg/M", r["ergebnis_m"], "| DSCR %.4f" % r["dscr"], "| Vervielf.", r["vervielf"], "| Faktor Bauherr", r["faktor_bauherr"])
