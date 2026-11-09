"""Lageplan (mit Stellplatzprüfung), Grundrisse (EG, 1. OG, 2. OG) und Schnitt mit Höhen für die Varianten E1–E4 und F1–F4.
Alle Maße sind Planungsannahmen: Stellplatz 2,50 × 5,00 m (Paare + Säule 0,40 m), Fahrgasse 6,00 m, Parallelparker 2,00 × 5,50 m, Säule Ø 0,40 m; Grundstück H1 32 × 30 m (hypothetisch).
Aufruf: python3 e_zeichnen.py [E1 .. F4]  ->  studie_gebaeudeformen/<Key>/plaene/{lageplan,plan_eg,plan_og1,plan_st,schnitt}.png + parken.json"""
import os, sys, math, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import varianten as VA, varianten_e as VE, parken as PK, zeichne_plaene as ZP
from zeichne_plaene import F, INK, GREY, S, tx, ty, draw_rect, dashed, hatch, canvas, legend, COL
RED = (190, 30, 30); GRN = (30, 110, 50); BLUE = (40, 90, 160); ORG = (200, 120, 20)
STAT_COL = {"voll": (214, 238, 218), "eingeschraenkt": (253, 236, 200), "konflikt": (250, 205, 205)}
def over_plot(key):
    v = VA.V[key]; bb = VA.bbox(v["og1"] + v["eg"] + v["st"])
    return dict(west=round(max(0, 0 - bb[0]), 2), ost=round(max(0, bb[2] - 32), 2), platz=round(max(0, 0 - bb[1]), 2), rueck=round(max(0, bb[3] - 30), 2))
def abstand_szenario(key, a):
    v = VA.V[key]; r = v["og1"][0]; ix0, iy0, ix1, iy1 = max(r[0], a), max(r[1], a), min(r[2], 32 - a), min(r[3], 30 - a)
    return round((r[2] - r[0]) * (r[3] - r[1]) - max(0, ix1 - ix0) * max(0, iy1 - iy0), 1)
def car(d, st, col=(150, 158, 170)):
    x0, y0, x1, y1 = st; wx = (x1 - x0) <= (y1 - y0); mx, my = (0.35, 0.25) if wx else (0.25, 0.35)
    d.rounded_rectangle([tx(x0 + mx), ty(y0 + my), tx(x1 - mx), ty(y1 - my)], radius=6, fill=col, outline=(110, 116, 126), width=1)
def lageplan(key):
    v = VA.V[key]; k = VA.kennzahlen(key); pk = PK.pruefe(key); bil = PK.flaechenbilanz(key)
    im, d = canvas(f"Lageplan {v['kurz']} – Gebäude, Säulen, Zufahrt, Stellplätze", "Grundstück H1 32 × 30 m HYPOTHETISCH (Zuschnitt/Baugrenzen nicht belegt) · Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m = Planungsannahmen · Zufahrt = Annahme")
    # nur rechnerisch verbleibende Fläche (nicht nutzbar) schraffieren
    st_ok = [(s["rect"]) for s in pk["stalls"]]
    step = 0.5
    for i in range(int(32 / step)):
        for j in range(int(30 / step)):
            x, y = (i + 0.5) * step, (j + 0.5) * step; ins = lambda r: r[0] <= x < r[2] and r[1] <= y < r[3]
            if any(ins(e) for e in v["eg"]) or any(ins(r) for r in st_ok) or ins(v["fahrgasse"]) or any(ins(z) for n, z in v.get("eingaenge", [])): continue
            d.rectangle([tx(i * step), ty(j * step), tx((i + 1) * step), ty((j + 1) * step)], fill=(247, 232, 232))
    for a, lab in ((3.0, "Szenario Abstand 3,0 m (ungeprüft)"), (6.0, "Szenario 0,5 H = 6,0 m bei 12 m Höhe (ungeprüft)")):
        dashed(d, [tx(a), ty(a), tx(32 - a), ty(30 - a)], (160, 170, 190), 1, 6); d.text((tx(a) + 4, ty(a) + (4 if a == 3 else 22)), lab, font=F(13), fill=(120, 130, 150))
    fg = v["fahrgasse"]; draw_rect(d, fg, (226, 229, 234), None, 0)
    cx, cy = (fg[0] + fg[2]) / 2, (fg[1] + fg[3]) / 2; d.text((tx(fg[0]) + 8, ty(cy) - 10) if v.get("zufahrt_dir") == "E" else (tx(fg[0]) + 6, ty(cy) - 30), "Fahrgasse 6,00 m\n(Annahme)", font=F(17, "SemiBold"), fill=GREY)
    # Zufahrt
    if v.get("zufahrt_dir") == "E": a0 = (tx(30), ty(cy)); a1 = (tx(36), ty(cy)); tri = [a1, (a1[0] - 10, a1[1] - 7), (a1[0] - 10, a1[1] + 7)]; lab = (tx(32.3), ty(cy) - 34)
    else: a0 = (tx(cx), ty(28)); a1 = (tx(cx), ty(33)); tri = [a1, (a1[0] - 7, a1[1] - 10), (a1[0] + 7, a1[1] - 10)]; lab = (tx(cx) + 12, ty(31.6))
    d.line([a0, a1], fill=GRN, width=4); d.polygon(tri, fill=GRN); d.text(lab, "Zufahrt (Annahme)", font=F(16, "SemiBold"), fill=GRN)
    # Gebäude: OG über EG
    for r in v["og1"]: draw_rect(d, (r[0] + 0.12, r[1] + 0.12, r[2] - 0.12, r[3] - 0.12), None, (170, 110, 80), 3, True)
    for r in v["eg"]: draw_rect(d, r, (238, 232, 226), INK, 4)
    for r in v["st"]: draw_rect(d, (r[0] + 0.05, r[1] + 0.05, r[2] - 0.05, r[3] - 0.05), None, (90, 60, 40), 2)
    # Stellplätze nach Status
    for s in pk["stalls"]:
        draw_rect(d, s["rect"], STAT_COL[s["status"]], (110, 116, 126), 1); car(d, s["rect"], (170, 176, 188)); d.text((tx(s["rect"][0]) + 6, ty(s["rect"][1]) + 4), str(s["nr"]), font=F(13, "SemiBold"), fill=INK)
    # Eingänge
    for nme, z in v.get("eingaenge", []): draw_rect(d, z, None, BLUE, 2, True); d.text((tx(z[0]) + 3, ty(z[1]) + 3), nme, font=F(12), fill=BLUE)
    for (x, y) in k["saeulen"]: d.ellipse([tx(x) - 6, ty(y) - 6, tx(x) + 6, ty(y) + 6], fill=(30, 30, 30), outline=INK)
    dashed(d, [tx(0), ty(0), tx(32), ty(30)], RED, 3, 14); d.text((tx(0) + 6, ty(30) + 6), "Grundstücksgrenze H1 (hypothetisch)", font=F(17, "SemiBold"), fill=RED)
    ov = over_plot(key)
    if ov["platz"] > 0: d.text((tx(8), ty(-3.4)), f"Vorbau ragt {ov['platz']:.1f} m über die Grundstücksgrenze in den Platz (ROT = Überstand)", font=F(17, "SemiBold"), fill=RED); d.rectangle([tx(0), ty(-1.5), tx(max(r[2] for r in v['og1'])), ty(0)], outline=RED, width=2)
    else: d.text((tx(8), ty(-3.2)), "Platz / öffentliche Fläche (Fußgänger)", font=F(17), fill=GREY)
    # Maße
    r1 = pk["stalls"][0]["rect"]; wx = (r1[2] - r1[0]) <= (r1[3] - r1[1])
    ZP.dim(d, (fg[0] - 2.2, fg[1]), (fg[0] - 2.2, fg[3]), "6,00") if v.get("zufahrt_dir") == "E" else ZP.dim(d, (fg[0], fg[1] + 1.2), (fg[2], fg[1] + 1.2), "6,00")
    tbl = [f"Stellplätze gezeichnet: {pk['gesamt']}", f"  funktionieren voll: {pk['voll']}", f"  eingeschränkt: {pk['eingeschraenkt']}", f"  Konflikt: {pk['konflikt']}", f"Fläche (960 m²): EG {bil['eg']:.0f} · Stellpl. {bil['stall'] + bil['par']:.0f} · Fahrgasse {bil['fahr']:.0f} · Zugänge {bil['zone']:.0f}", f"  nur rechnerisch (nicht nutzbar): {bil['rest']:.0f} m²", f"Überstand über H1: {max(ov.values()):.2f} m", f"OG im 3-m-/6-m-Randstreifen: {abstand_szenario(key, 3.0):.0f} / {abstand_szenario(key, 6.0):.0f} m²"]
    for i, t in enumerate(tbl): d.text((int(38.5 * S), ty(1) + i * 26), t, font=F(17, "SemiBold" if i in (0, 5) else "Regular"), fill=INK)
    legend(d, int(44 * S) + 25, [("Stellplatz funktioniert", STAT_COL["voll"]), ("eingeschränkt", STAT_COL["eingeschraenkt"]), ("Konflikt", STAT_COL["konflikt"]), ("Fahrgasse", (226, 229, 234)), ("nur rechnerisch verbleibend", (247, 232, 232))])
    d.text((int(30 * S), int(42.2 * S) + 70), "braun gestrichelt: 1./2. OG über dem EG (Vorbau) · blau gestrichelt: Eingangszonen", font=F(15), fill=(170, 110, 80)); return im
def strips_y(w, mv, mh):
    xs, ys, x1, y1 = w; apt, corr = ZP.strips((ys, xs, y1, x1), mv, mh)   # transponiert rechnen
    return [(f, B0, A0, B1, A1) for (f, A0, B0, A1, B1) in apt], (corr[1], corr[0], corr[3], corr[2])
def plan(key, level):
    v = VA.V[key]; k = VA.kennzahlen(key); lab = {"eg": "Erdgeschoss", "og1": "1. Obergeschoss", "st": "2. Obergeschoss (Staffel)" if v["staffel_ruecksprung"] else "2. Obergeschoss"}[level]
    im, d = canvas(f"{v['kurz']}: {lab} (schematisch)", "Grundriss schematisch · Wohnungsaufteilung = Streifenmodell (Mittelgang 2,0 m), netto = 0,88 × brutto · Säulen Ø 0,40 m · Grundstück H1 hypothetisch")
    dashed(d, [tx(0), ty(0), tx(32), ty(30)], RED, 3, 14); rects = v[level]
    if level == "eg":
        for nme, r, t in v["eg_raeume"]: draw_rect(d, r, COL.get(t, COL["other"]), (120, 126, 134), 1)
        done = set()
        for nme, r, t in v["eg_raeume"]:
            if nme in done and t == "dining": continue
            done.add(nme); d.text((tx(r[0]) + 6, ty(r[1]) + 6), nme + (f" ca. {v['gastro_m2']:.0f} m²" if t == "dining" else ""), font=F(18, "SemiBold" if t == "dining" else "Regular"), fill=INK)
        for r in v["eg"]: draw_rect(d, r, None, INK, 4)
        pk = PK.pruefe(key); draw_rect(d, v["fahrgasse"], (238, 240, 243), None, 0)
        for s in pk["stalls"]: draw_rect(d, s["rect"], None, (170, 175, 185), 1); car(d, s["rect"], (205, 210, 218))
        for r in v["og1"]: draw_rect(d, (r[0] + 0.12, r[1] + 0.12, r[2] - 0.12, r[3] - 0.12), None, (170, 110, 80), 2, True)
        for nme, z in v.get("eingaenge", []): draw_rect(d, z, None, BLUE, 2, True)
    else:
        for r in rects: draw_rect(d, r, (252, 247, 240), INK, 4)
        if level == "st":
            for ov in ZP.subtract(v["og1"], v["st"][0]): draw_rect(d, ov, (222, 224, 228), None, 0); hatch(d, ov, (170, 170, 180), 12)
        w = v["wohn"][level]; mv, mh, _ = VA.MIX["standard"]
        if v.get("wohn_orient") == "y":
            apt, corr = strips_y(w, mv, mh); core = (w[0], VA.bbox(rects)[1], w[2], w[1])
        else:
            apt, corr = ZP.strips(w, mv, mh); core = (VA.bbox(rects)[0], w[1], w[0], w[3])
        draw_rect(d, core, COL["core"], (110, 116, 124), 2); d.text((tx(core[0]) + 4, ty(core[1]) + 6), "Kern + Nebenräume", font=F(16, "SemiBold"), fill=INK)
        draw_rect(d, corr, (244, 244, 246), (150, 150, 160), 1)
        for n, (f, ax0, ay0, ax1, ay1) in enumerate(apt, 1):
            area = round((ax1 - ax0) * (ay1 - ay0) * VA.NETTO, 1); draw_rect(d, (ax0, ay0, ax1, ay1), (242, 222, 212), (110, 80, 70), 2)
            d.text((tx(ax0) + 6, ty(ay0) + 6), f"WE {n}", font=F(17, "SemiBold"), fill=INK); d.text((tx(ax0) + 6, ty(ay0) + 26), f"{area:.0f} m²", font=F(16), fill=INK)
        for r in rects: draw_rect(d, r, None, INK, 4)
    if level != "st":
        for (x, y) in k["saeulen"]: d.ellipse([tx(x) - 6, ty(y) - 6, tx(x) + 6, ty(y) + 6], fill=(30, 30, 30) if level == "eg" else (150, 150, 155), outline=INK)
    bx = VA.bbox(rects); ZP.dim(d, (bx[0], bx[1] - 1.8), (bx[2], bx[1] - 1.8), f"{bx[2]-bx[0]:.1f} m"); ZP.dim(d, (bx[2] + 1.8, bx[1]), (bx[2] + 1.8, bx[3]), f"{bx[3]-bx[1]:.1f} m")
    d.text((int(36 * S), int(41 * S) + 70), f"Fläche Geschoss {VA.rects_area(rects):.0f} m²", font=F(20, "SemiBold"), fill=INK)
    legend(d, int(44 * S) + 25, [("Wohnung (schematisch)", (242, 222, 212)), ("Kern", COL["core"]), ("Gastronomie", COL["dining"]), ("Terrasse/Dach schraffiert", (222, 224, 228))]); return im
def schnitt(key):
    v = VA.V[key]; k = VA.kennzahlen(key); Zv = v["Z"]; a = 0 if v.get("schnitt_achse") == "x" else 1; c = v.get("schnitt_pos", 16.25)   # a: Achse der Zeichnung (0 = x, 1 = y)
    s = 34; W, H = int(44 * s) + 330, int(14.5 * s) + 190; im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    X = lambda t: int((t + 4) * s) + 250; Zp = lambda z: int(H - 90 - (z + 0.6) * s)
    ax = ("Westseite links, Ostseite rechts · Schnitt bei y = %.1f m" % c) if a == 0 else ("Platzseite links, Rückseite rechts · Schnitt bei x = %.2f m" % c)
    d.text((30, 14), f"{v['kurz']}: Gebäudeschnitt mit Geschosshöhen (schematisch)", font=F(30, "SemiBold"), fill=INK); d.text((30, 52), ax + " · Höhenbezug ±0,00 = OK Fertigfußboden EG (Planbezug Blatt 14) – Bezugspunkt der Stadt für die 12,00 m ist NICHT belegt", font=F(18), fill=GREY)
    d.line([(X(-4), Zp(0)), (X(36), Zp(0))], fill=INK, width=3)
    def span(rs):
        ys = sorted((r[a], r[a + 2]) for r in rs if r[1 - a] <= c <= r[3 - a]); lo, hi = ys[0]
        for c0, c1 in ys[1:]: hi = max(hi, c1) if c0 <= hi + 0.01 else hi
        return (lo, hi)
    se, s1, s2 = span(v["eg"]), span(v["og1"]), span(v["st"])
    for (lo, hi), z0, z1, fill, txt in ((se, 0, Zv["EG"][1], (252, 252, 252), "Gastronomie / Büro  lichte Höhe ≈ 3,85 m"), (s1, Zv["OG1"][0], Zv["OG1"][1], (252, 245, 240), "1. OG Wohnungen  lichte Höhe ≈ 3,15 m"), (s2, Zv["ST"][0], Zv["ST"][1], (252, 247, 238), "2. OG Wohnungen  lichte Höhe ≈ 3,15 m")):
        d.rectangle([X(lo), Zp(z1), X(hi), Zp(z0)], fill=fill, outline=INK, width=2); d.text((X(lo) + 60, Zp((z0 + z1) / 2) - 10 + (0 if z0 else -30)), txt, font=F(17), fill=INK)
    for (lo, hi, z) in ((s1[0], s1[1], Zv["OG1"][0]), (s2[0], s2[1], Zv["ST"][0]), (s2[0], s2[1], Zv["ATT"][0])): d.rectangle([X(lo - 0.04), Zp(z), X(hi + 0.04), Zp(z - 0.45)], fill=(150, 150, 150), outline=INK)
    d.rectangle([X(s2[0] - 0.04), Zp(Zv["ATT"][1]), X(s2[1] + 0.04), Zp(Zv["ATT"][0])], fill=(110, 110, 115), outline=INK)
    for sd in PK.stall_list(v):
        r = sd["rect"]
        if r[1 - a] <= c <= r[3 - a]: d.rounded_rectangle([X(r[a] + 0.25), Zp(1.5), X(r[a + 2] - 0.25), Zp(0.0)], radius=8, fill=(170, 176, 186), outline=(100, 106, 116)); d.text((X(r[a]) + 4, Zp(2.0)), "Pkw", font=F(13), fill=INK)
    near = [p for p in k["saeulen"] if abs(p[1 - a] - c) <= 2.9]; seen = set()
    for p in near:
        t = round(p[a], 1)
        if t not in seen: seen.add(t); d.rectangle([X(t) - 7, Zp(Zv["OG1"][0] - 0.45), X(t) + 7, Zp(0)], fill=(60, 60, 64), outline=INK)
    def ann(y0, y1, z, text, col=(180, 60, 20)): d.line([(X(y0), Zp(z)), (X(y1), Zp(z))], fill=col, width=2); d.text((X((y0 + y1) / 2) - 40, Zp(z) - 24), text, font=F(17, "SemiBold"), fill=col)
    n1, n2 = ("vorn", "hinten") if a == 1 else ("West", "Ost")
    if se[0] - s1[0] > 0.01: ann(s1[0], se[0], 3.45, f"{se[0]-s1[0]:.2f} m {n1}")
    if s1[1] - se[1] > 0.01: ann(se[1], s1[1], 3.45, f"{s1[1]-se[1]:.2f} m {n2}")
    if s2[0] - s1[0] > 0.01: ann(s1[0], s2[0], 9.0, f"Rücksprung {s2[0]-s1[0]:.2f} m")
    if s1[1] - s2[1] > 0.01: ann(s2[1], s1[1], 9.0, f"Terrasse {s1[1]-s2[1]:.2f} m")
    for z, t in ((0, "±0,00 OK FFB EG"), (Zv["OG1"][0], "+4,30 OK FFB 1. OG"), (Zv["ST"][0], "+7,90 OK FFB 2. OG"), (Zv["ATT"][0], "+11,50 Dachfläche"), (Zv["ATT"][1], "+12,00 Attika = zulässige Höhe")):
        d.line([(X(-3.9), Zp(z)), (X(36), Zp(z))], fill=(205, 208, 214), width=1); d.text((6, Zp(z) - 10 + (-12 if z == 12 else (10 if z == 11.5 else 0))), t, font=F(15, "SemiBold" if z in (0, 12) else "Regular"), fill=GRN if z == 12 else INK)
    lim = (0, 30) if a == 1 else (0, 32); nm = ("Platz", "hinten") if a == 1 else ("West", "Ost")
    for t, tt, off in ((lim[0], nm[0], 4), (lim[1], nm[1], -250)): d.line([(X(t), Zp(-0.3)), (X(t), Zp(12.6))], fill=RED, width=2); d.text((X(t) + off, Zp(12.5)), f"Grundstücksgrenze {tt} (H1)", font=F(15), fill=RED)
    d.text((30, H - 70), "Geschosshöhen: EG 4,30 m · 1. OG 3,60 m · 2. OG 3,60 m · Dach/Attika 0,50 m = 12,00 m. Reserve 0,00 m. Die 12,00 m gelten erst als eingehalten, wenn der baurechtliche Höhenbezug geklärt ist.", font=F(19), fill=INK)
    d.text((30, H - 40), f"Säulen im Schnittbereich: {len(seen)} · Säulen insgesamt: {k['anzahl_saeulen']} · Vorbau-Unterkante +4,00 m (Decke 0,30 m)", font=F(19), fill=INK); return im
def speichern(key):
    out = os.path.join(VA.ROOT, "studie_gebaeudeformen", key, "plaene"); os.makedirs(out, exist_ok=True)
    lageplan(key).save(os.path.join(out, "lageplan.png"))
    for lv, nm in (("eg", "plan_eg"), ("og1", "plan_og1"), ("st", "plan_st")): plan(key, lv).save(os.path.join(out, nm + ".png"))
    schnitt(key).save(os.path.join(out, "schnitt.png"))
    json.dump(dict(parken=PK.pruefe(key), flaeche=PK.flaechenbilanz(key), ueber=over_plot(key), abstand3=abstand_szenario(key, 3.0), abstand6=abstand_szenario(key, 6.0)), open(os.path.join(VA.ROOT, "studie_gebaeudeformen", key, "parken.json"), "w"), indent=1, ensure_ascii=False, default=str); print("ok", key)
if __name__ == "__main__":
    for key in sys.argv[1:] or ["E1", "E2", "E3", "E4", "F1", "F2", "F3", "F4"]: speichern(key)
