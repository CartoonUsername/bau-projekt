"""Prüfung und Kennzahlen der Varianten A, B, C -> validation/variants_validation.md und geometry/variants_metrics.json"""
import json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
D = json.load(open(os.path.join(ROOT, "geometry", "variants_ABC.json"), encoding="utf-8")); NET = D["net_factor"]
H = {"GF": 3.5, "L1": 3.0, "L2": 3.1}
def grid(rects, x1, y1, step=0.05):
    xs = np.arange(0, x1, step) + step / 2; ys = np.arange(0, y1, step) + step / 2; G = np.zeros((len(ys), len(xs)), int)
    for r in rects:
        a = (xs >= r[0]) & (xs < r[2]); b = (ys >= r[1]) & (ys < r[3]); G[np.ix_(b, a)] += 1
    return G
def area(r): return (r[2] - r[0]) * (r[3] - r[1])
checks, M = [], {}
for k, v in D["variants"].items():
    rs = v["rooms"]; L = v["rear_cantilever"]; D1 = v["depth_upper"]; c0 = v["corridor_y"]
    lv = lambda l: [r for r in rs if r["level"] == l]
    env = {"GF": [0, 0, 32, 18], "L1": [0, 0, 32, D1], "L2": [0.8, 0.8, 31.2, D1 - 0.8]}
    for l in ("GF", "L1", "L2"):
        rects = [r["rect"] for r in lv(l) if r["id"] != "BAR-GF"]
        G = grid(rects, 32, D1 + 1) if l != "GF" else grid(rects, 32, 19)
        e = env[l]; ys0, ys1 = round(e[1] / 0.05), round(e[3] / 0.05); xs0, xs1 = round(e[0] / 0.05), round(e[2] / 0.05)
        inside = G[ys0:ys1, xs0:xs1]; over = int((G > 1).sum()) * 0.0025; gap = int((inside == 0).sum()) * 0.0025; out = float(G.sum() * 0.0025 - inside.sum() * 0.0025)
        checks.append((k, f"Geschoss {l}: lückenlos und ohne Überlappung", "PASS" if over < 0.01 and gap < 0.01 and out < 0.01 else "FAIL", f"Überlappung {over:.2f} m², Lücke {gap:.2f} m², außerhalb {out:.2f} m²"))
    byid = {r["id"]: r for r in rs}
    st = lambda p: [byid[f"{p}-{l}"]["rect"] for l in ("GF", "L1", "L2")]
    lif = st("LIFT"); ok_l = all(x == lif[0] for x in lif); lan = [byid[f"LANDING-{l}"]["rect"] for l in ("GF", "L1", "L2")]; sta = [byid[f"STAIR-{l}"]["rect"] for l in ("GF", "L1", "L2")]
    ok_s = all(x[1] == sta[0][1] and x[3] == sta[0][3] for x in sta) and all(x[1] == lan[0][1] and x[3] == lan[0][3] for x in lan)
    checks.append((k, "Aufzug, Treppe, Vorraum übereinander", "PASS" if ok_l and ok_s else "FAIL", f"Aufzug {lif[0]}, Treppe y {sta[0][1]}–{sta[0][3]}, Vorraum y {lan[0][1]}–{lan[0][3]}"))
    cl1 = byid["CORR-L1"]["rect"]; cl2 = byid["CORR-L2"]["rect"]
    checks.append((k, "Mittelgang stößt an Aufzugsvorraum (L1, L2)", "PASS" if cl1[0] == lan[1][2] and cl1[1] == lan[1][1] and cl1[3] == lan[1][3] and abs(cl2[0] - lan[2][2]) < 0.01 and cl2[1] == lan[2][1] else "FAIL", f"Gang y {cl1[1]}–{cl1[3]}, Vorraum y {lan[1][1]}–{lan[1][3]}"))
    sh = v["shaft"]["rect"]; c = ((sh[0] + sh[2]) / 2, (sh[1] + sh[3]) / 2); inr = lambda r: r["rect"][0] <= c[0] <= r["rect"][2] and r["rect"][1] <= c[1] <= r["rect"][3]
    where = {l: [r["id"] for r in lv(l) if inr(r) and r["id"] != "BAR-GF"] for l in ("GF", "L1", "L2")}
    checks.append((k, "Küchenschacht in allen Geschossen innerhalb eines Raums", "PASS" if all(len(w) == 1 for w in where.values()) else "FAIL", f"{where}; läuft durch Wohnungen (C-22)"))
    fl = [r for r in lv("L1") if r["id"].startswith("WE-L1-V")]; bc = v["balconies"]
    checks.append((k, "5 Balkone mittig vor den 5 Vorderwohnungen", "PASS" if len(fl) == 5 and all(abs((r["rect"][0] + r["rect"][2]) / 2 - (b["rect"][0] + b["rect"][2]) / 2) < 1e-6 for r, b in zip(fl, bc)) else "FAIL", "Balkone 2,70 × 1,50 m, Platzseite"))
    # Kennzahlen
    ap = {l: [r for r in lv(l) if r["type"] == "apartment"] for l in ("L1", "L2")}
    net = lambda rr: [round(r["area_gross"] * NET, 1) for r in rr]
    dw = lambda r: (r["rect"][3] - r["rect"][1]) / (r["rect"][2] - r["rect"][0])
    allap = ap["L1"] + ap["L2"]; offices = [r for r in lv("GF") if r["type"] == "office"]
    din = byid["DINING-GF"]; bar = byid["BAR-GF"]; gserv = [byid[i] for i in ("PERSONAL-GF", "WC-GF", "STORE-GF", "KITCHEN-GF")]
    ggross = din["area_gross"] + sum(r["area_gross"] for r in gserv); free = din["area_gross"] - bar["area_gross"]
    seats = int(free / 2.1) + 12
    fp = {"GF": 576.0, "L1": 32 * D1, "L2": (31.2 - 0.8) * (D1 - 1.6)}
    bgf = sum(fp.values()); bri = sum(fp[l] * H[l] for l in fp)
    covered = v["parking"]["covered_depth"]; ns = len(v["parking"]["stalls"])
    M[k] = dict(auskragung_hinten_m=L, flaeche_L1=fp["L1"], flaeche_L2=round(fp["L2"], 1), bgf=round(bgf, 1), bri_naeherung=round(bri), projektion_gesamt=max(fp.values()), grz_projektion=round(max(fp.values()) / 960, 3),
                gastro_brutto=round(ggross, 1), dining_brutto=round(din["area_gross"], 1), seats_innen=seats, buero_brutto=round(sum(r["area_gross"] for r in offices), 1), buero_netto=round(sum(r["area_gross"] for r in offices) * NET, 1),
                we_L1=len(ap["L1"]), we_L2=len(ap["L2"]), we_gesamt=len(allap), wfl_L1=round(sum(net(ap["L1"])), 1), wfl_L2=round(sum(net(ap["L2"])), 1), wfl_gesamt=round(sum(net(allap)), 1),
                wohnungsgroessen=sorted(set(net(allap))), tiefe_breite_max=round(max(dw(r) for r in allap), 2), tiefe_breite_tief=[r["id"] for r in allap if dw(r) > 1.8],
                stellplaetze=ns, ueberdacht_tiefe=covered, voll_ueberdacht=covered >= 5.0, stuetzen=len(v["parking"]["columns"]), durchfahrt_hoehe=v["parking"]["soffit_z"],
                rangierflaeche=round(6.0 * 32), stp_bedarf=60.6)
checks_md = ["# Prüfung der Varianten A, B, C (hypothetisch, nicht festgelegt)", "", "| Variante | Prüfung | Ergebnis | Detail |", "|---|---|---|---|"] + [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in checks]
open(os.path.join(ROOT, "validation", "variants_validation.md"), "w", encoding="utf-8").write("\n".join(checks_md) + "\n")
json.dump(M, open(os.path.join(ROOT, "geometry", "variants_metrics.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(f"{a} {b}: {c} {d[:90]}" for a, b, c, d in checks)); print(json.dumps(M, ensure_ascii=False, indent=0)[:3000])
