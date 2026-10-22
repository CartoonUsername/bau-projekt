"""Gegenprobe: vergleicht alle Rechenfälle der Excel (nach recalc) mit der unabhängigen Python-Rechnung und schreibt ergebnisse.json."""
import json, openpyxl
from model import run
mp = json.load(open("xlsx_map.json")); FR, COL = mp["FR"], mp["COL"]
ws = openpyxl.load_workbook("Wirtschaftlichkeit_Gesamtkonzept_B3.xlsx", data_only=True)["Rechenkern"]
cases = {"V 20 %": ("V", .2, {}), "R 20 %": ("R", .2, {}), "G 20 %": ("G", .2, {}), "V 0 %": ("V", 0, {}), "V 10 %": ("V", .1, {}), "V 30 %": ("V", .3, {}), "R 0 %": ("R", 0, {}), "R 10 %": ("R", .1, {}), "R 30 %": ("R", .3, {}), "G 0 %": ("G", 0, {}), "G 10 %": ("G", .1, {}), "G 30 %": ("G", .3, {}),
         "R 20 %, Tilgung 1 %": ("R", .2, dict(tilg=1)), "R Baukosten +10 %": ("R", .2, dict(bau_f=1.1)), "R Baukosten +20 %": ("R", .2, dict(bau_f=1.2)), "R Zins +1 pp": ("R", .2, dict(dz=1)), "R Zins +2 pp": ("R", .2, dict(dz=2)),
         "R Leerstand +5 pp": ("R", .2, dict(dv=5)), "R Leerstand +10 pp": ("R", .2, dict(dv=10)), "R Miete −10 %": ("R", .2, dict(mf=.9))}
mapk = {"T": "T", "D": "D", "EK": "EK", "ds": "ds", "noi": "noi", "dscr": "dscr", "cf": "cf", "k297": "k297", "k299": "k299", "ds_kfw": "ds_kfw", "dscr_kfw": "dscr_kfw", "nb_z": "nb_zuschuss", "nb_dscr": "nb_dscr", "be_w1": "be_wohn_1", "be_w12": "be_wohn_12", "be_f1": "be_faktor_1", "ek_need": "ek_need", "dmax": "dmax", "rendite": "rendite", "F": "F", "bnk": "bnk", "kg300": "kg300", "S": "S"}
mx = 0.0; res = {}
for name, (sc, q, ov) in cases.items():
    r = run(sc, q, **ov); col = COL[name]; res[name] = r
    for xk, pk in mapk.items():
        v = ws[f"{col}{FR[xk]}"].value; mx = max(mx, abs(v - r[pk]) / max(1.0, abs(r[pk])))
print("größte relative Abweichung Excel gegen Python:", mx)
assert mx < 1e-9
json.dump(res, open("ergebnisse.json", "w"), ensure_ascii=False, indent=1)
