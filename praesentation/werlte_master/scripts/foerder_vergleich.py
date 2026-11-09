"""Vergleich OG-1 / OG-2 / OG-3 unter Foerderaspekten. Alle Foerderparameter sind ANNAHMEN (Quelle siehe Bericht)."""
import json
b = json.load(open('../../bank_values.json'))
K0, RATE_J = b['kredit'], b['rate_monat'] * 12
ANNUI = RATE_J / K0                      # Jahresannuitaet je Euro Darlehen (3,21 % + 1 % Tilgung)
MIETE_FREI = b['miete_monat'] / b['wf']  # 11,18 EUR/m2 (Excel)
WOHN_ANTEIL = b['gs_wohnanteil']         # 49,2 % der Gesamtkosten (Excel-Annahme)
BASIS_ERG_M = b['c_ergebnis']            # GbR-Ergebnis/Monat bei 655 m2, 12 WE
V = {  # WE, Wohnflaeche netto (Modell), Buerofaeche Excel-Vermietung entfaellt?
 'Excel-Basis (Vergleich)': dict(we=12, w=655, buero=True),
 'OG-1': dict(we=12, w=591, buero=True),
 'OG-2': dict(we=13, w=591, buero=True),
 'OG-3 (optimiert, Bueros -> Wohnungen)': dict(we=15, w=736, buero=False),
}
RENT = {'frei': MIETE_FREI, 'Mietstufe I-III mittlere Einkommen 7,80': 7.80, 'niedrige Einkommen 6,30': 6.30}
res = {}
for n, v in V.items():
    gk = K0 + (v['we'] - 12) * 15000                  # Mehrkosten je WE ueber 8 (Excel: 15.000)
    kosten_wohn = gk * WOHN_ANTEIL
    foerderfaehig = min(kosten_wohn, 5330 * v['w'])   # Darlehens-Kostengrenze 5.330 EUR/m2 (Stand 04/2026)
    d_rent = (v['w'] - 655) * MIETE_FREI * 0.9        # netto nach 10 % Rueckstellung, je Monat
    d_buero = 0 if v['buero'] else -1600 * 0.9
    d_kap = -(gk - K0) * ANNUI / 12
    ergebnis = BASIS_ERG_M + d_rent + d_buero + d_kap
    r = dict(we=v['we'], wf=v['w'], gesamtkosten=round(gk), foerderfaehig=round(foerderfaehig),
             ergebnis_ohne_foerderung_monat=round(ergebnis))
    for zq in (0.20, 0.40):
        Z = zq * foerderfaehig
        ersp = Z * ANNUI / 12
        for rn, rm in RENT.items():
            if rn == 'frei': continue
            verlust = (MIETE_FREI - rm) * v['w'] * 12 / 12 * 0.9
            r[f'Z{int(zq*100)}_{rm}'] = dict(zuschuss=round(Z), ersparnis_kapitaldienst=round(ersp),
                                            mietverlust=round(verlust), saldo_monat=round(ersp - verlust),
                                            ergebnis_monat=round(ergebnis + ersp - verlust))
    r['Z45k_je_WE_(Dritt-Quelle,ungeprueft)'] = 45000 * v['we']
    res[n] = r
json.dump(res, open('../foerderung/vergleich.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
