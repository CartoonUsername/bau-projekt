"""Unabhängige Python-Rechnung der Wirtschaftlichkeit (Gegenprobe zur Excel). Alle Beträge in Euro."""
import json
from params import PARAMS
P = {}
for r in PARAMS:
    if r[0] == "sec": continue
    P[r[0]] = r[3:6]
SC = {"V": 0, "R": 1, "G": 2}
def run(sc="R", q=0.2, bau_f=1.0, dz=0.0, dv=0.0, mf=1.0, tilg=None, kfw=False):
    i = SC[sc]; g = lambda k: P[k][i]
    grund = g("gr_m2") * g("gr_preis"); neben = grund * (g("grest") + g("notar")) / 100; kg100 = grund + neben
    bgf = g("bgf_eg") + g("bgf_l1") + g("bgf_l2")
    kg300 = bgf * g("bau_m2") * bau_f * (1 + g("eh40") / 100); ausbau = g("gew_bgf") * g("ausbau"); kg500 = g("kg500_fl") * g("kg500_m2") + g("kg500_terr")
    basis = kg300 + ausbau + kg500
    bnk = basis * (g("bnk_arch") + g("bnk_fach") + g("bnk_gen") + g("bnk_son")) / 100
    res = (g("kg200") + basis) * g("reserve") / 100
    S = kg100 + g("kg200") + basis + bnk + res
    zb = g("z_bank") + dz; t = (g("tilg") if tilg is None else tilg)
    a = zb / 100 * (g("bauzeit") / 12 * g("abruf") / 100 + g("anlauf") / 12) + g("bearb") / 100
    T = S / (1 - (1 - q) * a); F = T - S; D = (1 - q) * T; EK = q * T
    soll_w = g("wfl") * g("m_wohn") * mf * 12; soll_g = g("gastro_nf") * g("m_gastro") * mf * 12; soll_b = g("buero_nf") * g("m_buero") * mf * 12
    eff_w = soll_w * (1 - (g("v_wohn") + dv) / 100); eff_g = soll_g * (1 - (g("v_gastro") + dv) / 100); eff_b = soll_b * (1 - (g("v_buero") + dv) / 100)
    kosten_w = g("wfl") * g("ih_wohn") + g("we") * g("vw_wohn") + g("wfl") * g("nu_wohn")
    kosten_g = (g("gastro_nf") + g("buero_nf")) * (g("ih_gew") + g("nu_gew")) + (soll_g + soll_b) * g("vw_gew") / 100
    noi = eff_w + eff_g + eff_b - kosten_w - kosten_g
    ds = D * (zb + t) / 100
    out = dict(sc=sc, q=q, grund=grund, neben=neben, kg100=kg100, kg200=g("kg200"), kg300=kg300, ausbau=ausbau, kg500=kg500, bnk=bnk, reserve=res, S=S, F=F, T=T, EK=EK, D=D,
               zins_j=D * zb / 100, tilg_j=D * t / 100, ds=ds, rate_m=ds / 12, zins_m=D * zb / 100 / 12, soll=soll_w + soll_g + soll_b, soll_w=soll_w, soll_g=soll_g, soll_b=soll_b, eff=eff_w + eff_g + eff_b, kosten=kosten_w + kosten_g, noi=noi, dscr=noi / ds, cf=noi - ds, rendite=noi / T, bgf=bgf)
    # Break-even
    out["be_wohn_1"] = (1.0 * ds - (noi - eff_w)) / (g("wfl") * 12 * (1 - (g("v_wohn") + dv) / 100))
    out["be_wohn_12"] = (1.2 * ds - (noi - eff_w)) / (g("wfl") * 12 * (1 - (g("v_wohn") + dv) / 100))
    effs = eff_w + eff_g + eff_b; fix = kosten_w + (g("gastro_nf") + g("buero_nf")) * (g("ih_gew") + g("nu_gew")); vw = g("vw_gew") / 100 * (soll_g + soll_b)
    out["be_faktor_1"] = (1.0 * ds + fix) / (effs - vw); out["be_faktor_12"] = (1.2 * ds + fix) / (effs - vw)
    dmax = noi / (1.2 * (zb + t) / 100); x = dmax / (S + dmax * a); q_need = 1 - x; T_need = S / (1 - x * a)
    out.update(dmax=dmax, q_need=q_need, ek_need=T_need - dmax, a=a)
    # KfW (theoretisch)
    wohn_share = (g("bgf_l1") + g("bgf_l2") + g("bgf_eg") - g("gew_bgf")) / bgf
    k297 = min(g("we") * g("kfw297_we"), wohn_share * D); k299 = min(g("gew_bgf") * g("kfw299_m2"), (1 - wohn_share) * D); bank = D - k297 - k299
    ds_k = k297 * (g("z_297") + t) / 100 + k299 * (g("z_299") + t) / 100 + bank * (zb + t) / 100
    out.update(wohn_share=wohn_share, k297=k297, k299=k299, bank_rest=bank, ds_kfw=ds_k, dscr_kfw=noi / ds_k, cf_kfw=noi - ds_k, zins_kfw_j=k297 * g("z_297") / 100 + k299 * g("z_299") / 100 + bank * zb / 100)
    # NBank theoretisch
    z = g("nb_zusch") / 100 * min(wohn_share * S, g("nb_cap") * g("wfl")); D2 = D - z
    noi2 = noi - eff_w + g("wfl") * g("nb_miete") * 12 * (1 - g("v_wohn") / 100)
    ds2 = D2 * (zb + t) / 100
    out.update(nb_zuschuss=z, nb_D=D2, nb_noi=noi2, nb_ds=ds2, nb_dscr=noi2 / ds2)
    return out
if __name__ == "__main__":
    for sc in "VRG":
        for q in (0, 0.1, 0.2, 0.3):
            r = run(sc, q); print(sc, q, f"T={r['T']:,.0f} D={r['D']:,.0f} NOI={r['noi']:,.0f} DS={r['ds']:,.0f} DSCR={r['dscr']:.2f} CF={r['cf']:,.0f} KfW-DSCR={r['dscr_kfw']:.2f}")
    r = run("R", 0.2); print({k: round(v, 3) if isinstance(v, float) else v for k, v in r.items() if k.startswith(("be_", "nb_", "k29", "wohn_", "rendite", "kg", "ausbau", "bnk", "reserve", "S", "F", "grund", "neben"))})
