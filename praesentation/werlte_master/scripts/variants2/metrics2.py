"""Prüfung und Kennzahlen der Varianten (Version 2) -> validation/variants2_validation.md, geometry/variants2_metrics.json"""
import json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
D = json.load(open(os.path.join(ROOT, "geometry", "variants2_ABC.json"), encoding="utf-8")); NET = D["net_factor"]; H = {"GF": 3.5, "L1": 3.0, "L2": 3.1}
def mask(rects, W, Hh, step=0.05):
    xs = np.arange(0, W, step) + step / 2; ys = np.arange(0, Hh, step) + step / 2; G = np.zeros((len(ys), len(xs)), int)
    for r in rects:
        a = (xs >= r[0]) & (xs < r[2]); b = (ys >= r[1]) & (ys < r[3]); G[np.ix_(b, a)] += 1
    return G
def poly_rects(o):  # Außenkontur aus zwei Rechtecken (Haupt + Anbau)
    xs = sorted({p[0] for p in o}); ys = sorted({p[1] for p in o})
    if len(o) == 4: return [[min(xs), min(ys), max(xs), max(ys)]]
    # L-förmig: Haupt = bis zur y-Kante des Rücksprungs, Anbau = x ab Rücksprung
    yb = sorted({p[1] for p in o})[1] if False else None
    x0 = min(p[0] for p in o); x1 = max(p[0] for p in o); y0 = min(p[1] for p in o); yin = sorted({p[1] for p in o})[-2]; yout = max(p[1] for p in o); xin = sorted({p[0] for p in o})[1]
    return [[x0, y0, x1, yin], [xin, yin, x1, yout]]
checks, M = [], {}
for k, v in D["variants"].items():
    rs = v["rooms"]; c0 = v["c0"]; lv = lambda l: [r for r in rs if r["level"] == l]; byid = {r["id"]: r for r in rs}
    for l in ("GF", "L1", "L2"):
        env = poly_rects(v["outlines"][l]); rects = [r["rect"] for r in lv(l) if r["id"] != "BAR-GF"]
        G = mask(rects, 32.5, v["depth_L1"] + 1); E = mask(env, 32.5, v["depth_L1"] + 1)
        over = int((G > 1).sum()) * 0.0025; gap = int(((E > 0) & (G == 0)).sum()) * 0.0025; out = int(((G > 0) & (E == 0)).sum()) * 0.0025
        checks.append((k, f"Geschoss {l}: lückenlos, ohne Überlappung, innerhalb der Außenkontur", "PASS" if over < 0.01 and gap < 0.01 and out < 0.01 else "FAIL", f"Überlappung {over:.2f}, Lücke {gap:.2f}, außerhalb {out:.2f} m²"))
    st = lambda p: [byid[f"{p}-{l}"]["rect"] for l in ("GF", "L1", "L2")]
    lif = st("LIFT"); sta = st("STAIR"); lan = st("LANDING")
    checks.append((k, "Aufzug, Treppe, Flur übereinander", "PASS" if all(x == lif[0] for x in lif) and all(x[1] == sta[0][1] and x[3] == sta[0][3] for x in sta) and all(x[1] == lan[0][1] and x[3] == lan[0][3] for x in lan) else "FAIL", f"Aufzug {lif[0]}, Treppe y {sta[0][1]}–{sta[0][3]}, Flur y {lan[0][1]}–{lan[0][3]}"))
    c1, c2 = byid["CORR-L1"]["rect"], byid["CORR-L2"]["rect"]
    checks.append((k, "Mittelgang stößt an den Flur des Kerns (1. OG, 3. Geschoss)", "PASS" if c1[0] == lan[1][2] and c1[1] == lan[1][1] and c1[3] == lan[1][3] and abs(c2[0] - lan[2][2]) < 0.01 and c2[1] == lan[2][1] else "FAIL", f"Gang y {c1[1]}–{c1[3]}"))
    sh = v["shaft"]["rect"]; c = ((sh[0] + sh[2]) / 2, (sh[1] + sh[3]) / 2); inr = lambda r: r["rect"][0] <= c[0] <= r["rect"][2] and r["rect"][1] <= c[1] <= r["rect"][3]
    where = {l: [r["id"] for r in lv(l) if inr(r) and r["id"] != "BAR-GF"] for l in ("GF", "L1", "L2")}
    checks.append((k, "Küchenschacht in allen Geschossen innerhalb eines Raums", "PASS" if all(len(w) == 1 for w in where.values()) and where["L1"][0].startswith("WE") and where["L2"][0].startswith("WE") else "FAIL", f"{where}; läuft durch Wohnungen (C-22)"))
    fl = [r for r in lv("L1") if r["id"].startswith("WE-L1-V")]
    checks.append((k, "5 Balkone mittig vor den 5 vorderen Wohnungen", "PASS" if len(fl) == 5 and all(abs((r["rect"][0] + r["rect"][2]) / 2 - (b["rect"][0] + b["rect"][2]) / 2) < 1e-6 for r, b in zip(fl, v["balconies"])) else "FAIL", "Balkone 2,70 × 1,50 m Platzseite"))
    ap = {l: [r for r in lv(l) if r["type"] == "apartment"] for l in ("L1", "L2")}; allap = ap["L1"] + ap["L2"]
    net = lambda rr: [round(r["area_gross"] * NET, 1) for r in rr]; dw = lambda r: (r["rect"][3] - r["rect"][1]) / (r["rect"][2] - r["rect"][0])
    gser = [byid[i] for i in ("DINING-GF", "WC-GF", "PERSONAL-GF", "FLUR-GF", "KITCHEN-GF", "STORE-GF", "ANLIEF-GF")]
    gg = sum(r["area_gross"] for r in gser); din = byid["DINING-GF"]["area_gross"]; bar = byid["BAR-GF"]["area_gross"]; seats = int((din - bar) / 2.1) + 12
    off = [r for r in lv("GF") if r["type"] == "office"]
    ar = lambda o: 0.5 * abs(sum(o[i][0] * o[(i + 1) % len(o)][1] - o[(i + 1) % len(o)][0] * o[i][1] for i in range(len(o))))
    fp = {l: ar(v["outlines"][l]) for l in ("GF", "L1", "L2")}; bgf = sum(fp.values()); bri = sum(fp[l] * H[l] for l in fp)
    terr = v["roof_terrace"]; terr_a = (terr[2] - terr[0]) * (terr[3] - terr[1])
    M[k] = dict(e1=v["e1"], e2=v["e2"], depth_L1=v["depth_L1"], y2=v["y2"], flaeche=fp, bgf=round(bgf, 1), bri=round(bri), projektion=round(fp["L1"], 1), grz=round(fp["L1"] / 960, 3),
                gastro_brutto=round(gg, 1), dining=din, seats=seats, buero_brutto=round(sum(r["area_gross"] for r in off), 1), buero_netto=round(sum(r["area_gross"] for r in off) * NET, 1),
                we_L1=len(ap["L1"]), we_L2=len(ap["L2"]), we=len(allap), wfl_L1=round(sum(net(ap["L1"])), 1), wfl_L2=round(sum(net(ap["L2"])), 1), wfl=round(sum(net(allap)), 1),
                groessen=sorted(set(net(allap))), tiefe_breite_max=round(max(dw(r) for r in allap), 2), stellplaetze=len(v["parking"]["stalls"]), ueberdacht=v["parking"]["covered_depth"], stuetzen=len(v["parking"]["columns"]),
                soffit=v["parking"]["soffit_z"], terrasse_tiefe=round(terr[3] - terr[1], 2), terrasse_m2=round(terr_a, 1), stp_bedarf=60.6)
md = ["# Prüfung der Varianten A, B, C (Version 2, hypothetisch, nicht festgelegt)", "", "| Variante | Prüfung | Ergebnis | Detail |", "|---|---|---|---|"] + [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in checks]
open(os.path.join(ROOT, "validation", "variants2_validation.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
json.dump(M, open(os.path.join(ROOT, "geometry", "variants2_metrics.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(f"{a} {b[:55]}: {c} {d[:80]}" for a, b, c, d in checks if c != "PASS" or "Geschoss L2" in b)); print(sum(1 for c in checks if c[2] == "FAIL"), "FAIL")
for k, m in M.items(): print(k, {x: m[x] for x in ("gastro_brutto", "seats", "buero_netto", "we", "wfl", "bgf", "projektion", "grz", "stellplaetze", "ueberdacht", "stuetzen", "terrasse_tiefe", "tiefe_breite_max", "groessen")})
