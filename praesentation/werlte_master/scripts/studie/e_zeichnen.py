"""Variante E: Parkprüfung, Lageplan, Grundrisse (EG, 1. OG, 2. OG) und Schnitt mit Höhen – alles aus varianten.py / varianten_e.py.
Maße sind Planungsannahmen: Stellplatz 2,50 x 5,00 m, Fahrgasse 6,00 m, Säule Ø 0,40 m; Grundstück H1 32 x 30 m (hypothetisch); Zufahrt von Osten (Annahme).
Aufruf: python3 e_zeichnen.py [E1 E2 E3 E4]  ->  studie_gebaeudeformen/<Key>/plaene/{lageplan,plan_eg,plan_og1,plan_st,schnitt}.png + parken_<Key>.json"""
import os, sys, math, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import varianten as VA, varianten_e as VE, zeichne_plaene as ZP
from zeichne_plaene import F, INK, GREY, S, tx, ty, draw_rect, dashed, hatch, canvas, legend, strips, COL
RED = (190, 30, 30); GRN = (30, 110, 50)
def seg_circle_hits_rect(c, r, rect):
    cx, cy = c; x0, y0, x1, y1 = rect; nx, ny = min(max(cx, x0), x1), min(max(cy, y0), y1); return math.hypot(cx - nx, cy - ny) < r - 1e-9
def intrusion(stall, cols):
    x0, y0, x1, y1 = stall; best = 0.0
    for yy in [y0 + (y1 - y0) * i / 20 for i in range(21)]:
        tot = 0.0
        for (cx, cy) in cols:
            if abs(cy - yy) < 0.2:
                h = math.sqrt(max(0, 0.04 - (cy - yy) ** 2)); a, b = max(cx - h, x0), min(cx + h, x1)
                if b > a: tot += b - a
        best = max(best, tot)
    return best
def pruefe_parken(key):
    v = VA.V[key]; cols = v["saeulen_pts"]; eg = v["eg"]; res = dict(stellplaetze=len(v["stalls"]), reihe1=len(v["stalls_row1"]), reihe2=len(v["stalls_row2"]), fehler=[], hinweise=[], min_nutzbreite=9.9)
    plot = (0, 0, 32, 30)
    for i, st in enumerate(v["stalls"], 1):
        x0, y0, x1, y1 = st; fehler = []
        if x0 < plot[0] - 1e-6 or x1 > plot[2] + 1e-6 or y1 > plot[3] + 1e-6 or y0 < 0: fehler.append("außerhalb Grundstück")
        if any(not (x1 <= e[0] or x0 >= e[2] or y1 <= e[1] or y0 >= e[3]) for e in eg): fehler.append("im Erdgeschoss")
        w = (x1 - x0) - intrusion(st, cols); res["min_nutzbreite"] = min(res["min_nutzbreite"], w)
        if w < 2.30: fehler.append(f"Nutzbreite {w:.2f} m < 2,30 m")
        # Fahrgasse vor dem Stellplatz (6,0 m) und Weg zur Zufahrt (Ost)
        if st in v["stalls_row2"]: a = (x0, y0 - VE.GASSE, x1, y0); band = (x0, y0 - VE.GASSE, 32, y0)
        else: a = (x0, y1, x1, y1 + VE.GASSE); band = (x0, y1, 32, y1 + VE.GASSE)
        if band[3] > 30 + 1e-6 or band[1] < 0: fehler.append("Fahrgasse außerhalb Grundstück")
        for c in cols:
            if seg_circle_hits_rect(c, 0.2, band): fehler.append("Säule in Fahrgasse/Ausfahrt")
        for e in eg:
            if not (band[2] <= e[0] or band[0] >= e[2] or band[3] <= e[1] or band[1] >= e[3]): fehler.append("Erdgeschoss in Fahrgasse")
        for o in v["stalls"]:
            if o is not st and not (band[2] <= o[0] or band[0] >= o[2] or band[3] <= o[1] or band[1] >= o[3]): fehler.append("Stellplatz in Fahrgasse"); break
        if fehler: res["fehler"].append((i, sorted(set(fehler))))
    res["fahrgasse_m"] = VE.GASSE; res["ok"] = not res["fehler"]
    res["hinweise"] = ["vereinfachte Geometrieprüfung (Rechteckfreiraum 6,00 m vor 5,00 m tiefen 90°-Stellplätzen), keine Schleppkurven-Simulation", "Säulen (Ø 0,40 m) auf der Stellplatzgrenze: Nutzbreite 2,50 − 0,20 = 2,30 m je Platz (Mindestmaß/Stellplatzverordnung prüfen)", "Zufahrt von Osten ist Annahme (Lage der Erschließungsstraße unbekannt)", "Lücke zwischen Platz 7 und 8 (x 20,0–22,5): Stellplatz entfällt für Hintereingang/Anlieferung Gewerbe; Fußweg zum Kern an der Westseite (x 0–2,5) unter dem Vorbau"]
    return res
def over_plot(key):
    v = VA.V[key]; bb = VA.bbox(v["og1"] + v["eg"] + v["st"]); p = VE.PLOT_POLY; px0, py0, px1, py1 = min(a for a, b in p), min(b for a, b in p), max(a for a, b in p), max(b for a, b in p)
    return dict(west=round(max(0, px0 - bb[0]), 2), ost=round(max(0, bb[2] - px1), 2), platz=round(max(0, py0 - bb[1]), 2), rueck=round(max(0, bb[3] - py1), 2))
def abstand_szenario(key, a):
    v = VA.V[key]; inner = (a, a, 32 - a, 30 - a); r = v["og1"][0]; ov = 0.0
    ix0, iy0, ix1, iy1 = max(r[0], inner[0]), max(r[1], inner[1]), min(r[2], inner[2]), min(r[3], inner[3]); inside = max(0, ix1 - ix0) * max(0, iy1 - iy0)
    return round((r[2] - r[0]) * (r[3] - r[1]) - inside, 1)
def car(d, st, col=(150, 158, 170)):
    x0, y0, x1, y1 = st; cx0, cx1 = x0 + 0.35, x1 - 0.35; cy0, cy1 = y0 + 0.25, y1 - 0.25
    d.rounded_rectangle([tx(cx0), ty(cy0), tx(cx1), ty(cy1)], radius=6, fill=col, outline=(110, 116, 126), width=1)
def lageplan(key):
    v = VA.V[key]; k = VA.kennzahlen(key); pk = pruefe_parken(key)
    im, d = canvas(f"Lageplan {v['kurz']} – Gebäude, Säulen, Zufahrt und Stellplätze", "Grundstück H1 32 × 30 m HYPOTHETISCH (tatsächlicher Zuschnitt Baufeld 3 liegt nicht vor) · Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m = Planungsannahmen · Zufahrt von Osten = Annahme")
    # Abstandsszenarien
    for a, lab in ((3.0, "Szenario Abstand 3,0 m (ungeprüft)"), (6.0, "Szenario 0,5 H = 6,0 m bei 12 m Höhe (ungeprüft)")):
        dashed(d, [tx(a), ty(a), tx(32 - a), ty(30 - a)], (160, 170, 190), 1, 6); d.text((tx(a) + 4, ty(a) + (4 if a == 3 else 22)), lab, font=F(14), fill=(120, 130, 150))
    # Fahrgasse
    fg = v["fahrgasse"]; draw_rect(d, fg, (232, 234, 238), None, 0); d.text((tx(8), ty((fg[1] + fg[3]) / 2) - 10), "Fahrgasse 6,00 m (Annahme)", font=F(18, "SemiBold"), fill=GREY)
    ay = (fg[1] + fg[3]) / 2
    d.line([(tx(30), ty(ay)), (tx(36), ty(ay))], fill=GRN, width=4); d.polygon([(tx(36), ty(ay)), (tx(35), ty(ay) - 7), (tx(35), ty(ay) + 7)], fill=GRN); d.text((tx(32.3), ty(ay) - 34), "Zufahrt (Annahme)", font=F(16, "SemiBold"), fill=GRN)
    # Stellplätze
    bad = {i for i, _ in pk["fehler"]}
    for i, st in enumerate(v["stalls"], 1):
        draw_rect(d, st, (246, 247, 249) if i not in bad else (250, 215, 215), (110, 116, 126), 1); car(d, st); d.text((tx(st[0]) + 8, ty(st[1]) + 5), str(i), font=F(14, "SemiBold"), fill=INK)
    # EG, OG, Staffel
    for r in v["og1"]:
        draw_rect(d, (r[0] + 0.12, r[1] + 0.12, r[2] - 0.12, r[3] - 0.12), None, (170, 110, 80), 3, True)
    for r in v["eg"]: draw_rect(d, r, (238, 232, 226), INK, 4)
    for r in v["og1"]:
        for ov in ZP.subtract([r], (v["eg"][0][0], v["eg"][0][1], v["eg"][0][2], v["eg"][0][3])): pass
    for r in v["st"]: draw_rect(d, r, None, (90, 60, 40), 2)
    d.text((tx(6), ty(3)), "Erdgeschoss (Gewerbe)", font=F(20, "SemiBold"), fill=INK); d.text((tx(6), ty(5.0)), f"{VA.rects_area(v['eg']):.0f} m²", font=F(18), fill=INK)
    for (x, y) in k["saeulen"]: d.ellipse([tx(x) - 7, ty(y) - 7, tx(x) + 7, ty(y) + 7], fill=(30, 30, 30), outline=INK)
    # Grundstück
    p = VE.PLOT_POLY; dashed(d, [tx(0), ty(0), tx(32), ty(30)], RED, 3, 14); d.text((tx(0) + 6, ty(30) + 6), "Grundstücksgrenze H1 (hypothetisch)", font=F(18, "SemiBold"), fill=RED)
    d.text((tx(8), ty(-3.2)), "Platz / öffentliche Fläche (Fußgänger)", font=F(18), fill=GREY)
    # Eingänge
    d.polygon([(tx(1), ty(1.5)), (tx(3), ty(1.5)), (tx(2), ty(0.3))], fill=(40, 90, 160)); d.text((tx(3.2), ty(0.2)), "Eingang Kern/Wohnen (Platz)", font=F(14), fill=(40, 90, 160))
    d.text((tx(12), ty(0.2)), "Gastro-Eingang unter Arkade", font=F(14), fill=(40, 90, 160))
    hx = 20.0; d.rectangle([tx(hx), ty(v["eg"][0][3]) - 5, tx(hx + 2.5), ty(v["eg"][0][3]) + 5], fill=(40, 90, 160)); d.text((tx(hx - 1), ty(v["eg"][0][3]) - 24), "Hintereingang/Anlieferung", font=F(14), fill=(40, 90, 160))
    d.line([(tx(1.2), ty(9.5)), (tx(1.2), ty(v["stalls"][0][3] if False else v["eg"][0][3] + 5))], fill=(40, 90, 160), width=3); d.text((tx(-5.3), ty(14)), "Fußweg zum\nKern unter\nVorbau", font=F(14), fill=(40, 90, 160))
    # Maße
    s0 = v["stalls_row1"][7]; ZP.dim(d, (s0[0] - 2.5, s0[1] + 2.3), (s0[0], s0[1] + 2.3), "2,50"); ZP.dim(d, (s0[0] - 1.25, s0[1]), (s0[0] - 1.25, s0[3]), "5,00") if False else ZP.dim(d, (s0[0] + 0.3, s0[1] + 0.3), (s0[0] + 0.3, s0[3] - 0.3), "5,00")
    ZP.dim(d, (-2.5, fg[1]), (-2.5, fg[3]), "6,00")
    ov = over_plot(key)
    rows = [f"Stellplätze: {pk['stellplaetze']} (Reihe 1: {pk['reihe1']}, Reihe 2: {pk['reihe2']})", f"Prüfung Ein-/Ausfahren: {'alle Plätze frei erreichbar' if pk['ok'] else 'Konflikte an Platz ' + ', '.join(str(i) for i, _ in pk['fehler'])}", f"Min. Nutzbreite mit Säule: {pk['min_nutzbreite']:.2f} m", f"Überstand über Grundstück: {max(ov.values()):.2f} m", f"OG-Fläche im 3-m-Randstreifen: {abstand_szenario(key, 3.0):.0f} m²", f"OG-Fläche im 6-m-Randstreifen: {abstand_szenario(key, 6.0):.0f} m²"]
    for i, t in enumerate(rows): d.text((int(38 * S), ty(1) + i * 28), t, font=F(18, "SemiBold" if i < 2 else "Regular"), fill=INK)
    legend(d, int(44 * S) + 25, [("Erdgeschoss", (238, 232, 226)), ("Fahrgasse", (232, 234, 238)), ("Stellplatz (mit Pkw)", (246, 247, 249))])
    d.text((int(36 * S), int(42.2 * S) + 70), "gestrichelt braun: 1./2. OG über dem EG (Vorbau)", font=F(16), fill=(170, 110, 80)); return im
def plan(key, level):
    v = VA.V[key]; k = VA.kennzahlen(key); lab = {"eg": "Erdgeschoss", "og1": "1. Obergeschoss", "st": "2. Obergeschoss (Staffel)" if v["staffel_ruecksprung"] else "2. Obergeschoss"}[level]
    im, d = canvas(f"{v['kurz']}: {lab} (schematisch)", "Grundriss schematisch · Wohnungsaufteilung = Streifenmodell (Mittelgang 2,0 m), netto = 0,88 × brutto · Säulen Ø 0,40 m · Grundstück H1 hypothetisch")
    dashed(d, [tx(0), ty(0), tx(32), ty(30)], RED, 3, 14)
    rects = v[level]
    if level == "eg":
        eg = v["eg"][0]; dd = eg[3]; gy = 1.5 + (dd - 1.5) * 0.62
        draw_rect(d, (2.5, 1.5, 29.5, gy), COL["dining"], (120, 126, 134), 1); d.text((tx(6), ty(5)), f"Gastraum ca. {27*(gy-1.5):.0f} m²", font=F(20, "SemiBold"), fill=INK)
        draw_rect(d, (4, gy, 17.5, dd), COL["kitchen"], (120, 126, 134), 1); d.text((tx(5), ty(gy) // S + 0 if False else ty(gy + 0.5)), "Küche / Lager / WC", font=F(17), fill=INK)
        draw_rect(d, (20, gy, 29.5, dd), COL["office"], (120, 126, 134), 1); d.text((tx(20.3), ty(gy + 0.5)), "Büro / Technik", font=F(17), fill=INK)
        draw_rect(d, (0, 1.5, 4, 9.5), COL["core"], (110, 116, 124), 2); d.text((tx(0.2), ty(2.0)), "Kern", font=F(16, "SemiBold"), fill=INK)
        for r in v["eg"]: draw_rect(d, r, None, INK, 4)
        for i, st in enumerate(v["stalls"], 1): draw_rect(d, st, None, (170, 175, 185), 1); car(d, st, (205, 210, 218))
        draw_rect(d, v["fahrgasse"], (238, 240, 243), None, 0)
        for r in v["og1"]:
            draw_rect(d, r, None, (170, 110, 80), 2, True)
        d.text((tx(6), ty(-0.9) if False else ty(0.5)), "Arkade unter dem Vorbau (1,50 m)", font=F(15), fill=GREY)
    else:
        for r in rects: draw_rect(d, r, (252, 247, 240), INK, 4)
        if level == "st":
            for ov in ZP.subtract(v["og1"], v["st"][0]): draw_rect(d, ov, (222, 224, 228), None, 0); hatch(d, ov, (170, 170, 180), 12)
        xs, y0, x1, y1 = v["wohn"][level]; mv, mh, _ = VA.MIX["standard"]; apt, corr = strips(v["wohn"][level], mv, mh)
        bx = VA.bbox(rects); core = (bx[0], y0, xs, y1); draw_rect(d, core, COL["core"], (110, 116, 124), 2); d.text((tx(core[0]) + 4, ty(core[1]) + 8), "Kern + Nebenräume", font=F(16, "SemiBold"), fill=INK)
        draw_rect(d, corr, (244, 244, 246), (150, 150, 160), 1); d.text((tx(corr[0]) + 20, ty((corr[1] + corr[3]) / 2) - 10), "Mittelgang 2,0 m", font=F(16), fill=GREY)
        for n, (f, ax0, ay0, ax1, ay1) in enumerate(apt, 1):
            area = round((ax1 - ax0) * (ay1 - ay0) * VA.NETTO, 1); draw_rect(d, (ax0, ay0, ax1, ay1), (242, 222, 212), (110, 80, 70), 2)
            d.text((tx(ax0) + 6, ty(ay0) + 8), f"WE {n}", font=F(17, "SemiBold"), fill=INK); d.text((tx(ax0) + 6, ty(ay0) + 28), f"{area:.0f} m²", font=F(16), fill=INK)
        for r in rects: draw_rect(d, r, None, INK, 4)
    if level != "st":
        for (x, y) in k["saeulen"]: d.ellipse([tx(x) - 7, ty(y) - 7, tx(x) + 7, ty(y) + 7], fill=(30, 30, 30) if level == "eg" else (150, 150, 155), outline=INK)
    bx = VA.bbox(rects); ZP.dim(d, (bx[0], bx[1] - 1.8), (bx[2], bx[1] - 1.8), f"{bx[2]-bx[0]:.1f} m"); ZP.dim(d, (bx[2] + 1.8, bx[1]), (bx[2] + 1.8, bx[3]), f"{bx[3]-bx[1]:.1f} m")
    d.text((int(36 * S), int(41 * S) + 70), f"Fläche Geschoss {VA.rects_area(rects):.0f} m²", font=F(20, "SemiBold"), fill=INK)
    legend(d, int(44 * S) + 25, [("Wohnung (schematisch)", (242, 222, 212)), ("Kern", COL["core"]), ("Gastronomie", COL["dining"]), ("Terrasse/Dach schraffiert", (222, 224, 228))]); return im
def schnitt(key):
    v = VA.V[key]; k = VA.kennzahlen(key); Zv = v["Z"]; xc = 16.25
    s = 34; W, H = int(44 * s) + 330, int(14.5 * s) + 190; im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    X = lambda y: int((y + 4) * s) + 250; Zp = lambda z: int(H - 90 - (z + 0.6) * s)
    d.text((30, 14), f"{v['kurz']}: Schnitt bei x = {xc:.2f} m mit Geschosshöhen (schematisch)", font=F(30, "SemiBold"), fill=INK); d.text((30, 52), "Platzseite links, Rückseite rechts · Höhenbezug ±0,00 = OK Fertigfußboden EG (Planbezug Blatt 14) – Bezugspunkt der Stadt für die 12,00 m ist NICHT belegt", font=F(18), fill=GREY)
    d.line([(X(-4), Zp(0)), (X(34), Zp(0))], fill=INK, width=3)
    def span(rs):
        ys = sorted((r[1], r[3]) for r in rs if r[0] <= xc <= r[2]); a, b = ys[0]
        for c0, c1 in ys[1:]: b = max(b, c1) if c0 <= b + 0.01 else b
        return (a, b)
    se, s1, s2 = span(v["eg"]), span(v["og1"]), span(v["st"])
    d.rectangle([X(se[0]), Zp(Zv["EG"][1]), X(se[1]), Zp(0)], fill=(252, 252, 252), outline=INK, width=2); d.text((X(6.3), Zp(2.6)), "Gastronomie / Büro  lichte Höhe ≈ 3,85 m", font=F(17), fill=INK)
    d.rectangle([X(s1[0]), Zp(Zv["OG1"][1]), X(s1[1]), Zp(Zv["OG1"][0])], fill=(252, 245, 240), outline=INK, width=2); d.text((X(5), Zp(6.0)), "1. OG Wohnungen  lichte Höhe ≈ 3,15 m", font=F(17), fill=INK)
    d.rectangle([X(s2[0]), Zp(Zv["ST"][1]), X(s2[1]), Zp(Zv["ST"][0])], fill=(252, 247, 238), outline=INK, width=2); d.text((X(5 + v["staffel_ruecksprung"]), Zp(9.6)), "2. OG Wohnungen  lichte Höhe ≈ 3,15 m", font=F(17), fill=INK)
    for (a, b, z0, z1) in ((se[0], se[1], 3.85, 4.3), (s1[0], s1[1], 4.3 - 0.0, 4.3 + 0.45), (s1[0], s1[1], 7.9, 7.9 + 0.0), (s2[0], s2[1], 11.5 - 0.0, 11.5)):
        pass
    for (a, b, z) in ((s1[0], s1[1], 4.3), (s2[0], s2[1], 7.9), (s2[0], s2[1], 11.5)): d.rectangle([X(a - 0.04), Zp(z), X(b + 0.04), Zp(z - 0.45)], fill=(150, 150, 150), outline=INK)
    d.rectangle([X(s2[0] - 0.04), Zp(12.0), X(s2[1] + 0.04), Zp(11.5)], fill=(110, 110, 115), outline=INK)
    # Auto im Schnitt (hinterer Stellplatz)
    for st in v["stalls"]:
        if st[0] <= xc <= st[2]: d.rounded_rectangle([X(st[1] + 0.25), Zp(1.5), X(st[3] - 0.25), Zp(0.0)], radius=8, fill=(170, 176, 186), outline=(100, 106, 116)); d.text((X(st[1]) + 6, Zp(2.0)), "Pkw", font=F(14), fill=INK)
    for (x, y) in k["saeulen"]:
        if abs(x - xc) < 0.9 or True: pass
    for y in sorted({round(p[1], 2) for p in k["saeulen"] if abs(p[0] - 15.0) < 0.01 or abs(p[0] - 20.0) < 0.01 or abs(p[0] - 0.35) < 0.01}): d.rectangle([X(y) - 7, Zp(Zv["OG1"][0] - 0.45), X(y) + 7, Zp(0)], fill=(60, 60, 64), outline=INK)
    # Vorbau-Maße
    def ann(y0, y1, z, text, col=(180, 60, 20)):
        d.line([(X(y0), Zp(z)), (X(y1), Zp(z))], fill=col, width=2); d.text((X((y0 + y1) / 2) - 40, Zp(z) - 24), text, font=F(17, "SemiBold"), fill=col)
    ann(s1[0], se[0], 3.45, f"{se[0]-s1[0]:.2f} m vorn"); ann(se[1], s1[1], 3.45, f"{s1[1]-se[1]:.2f} m hinten")
    if v["staffel_ruecksprung"]: ann(s1[0], s2[0], 9.0, f"Rücksprung {s2[0]-s1[0]:.2f} m"); ann(s2[1], s1[1], 9.0, f"Terrasse {s1[1]-s2[1]:.2f} m")
    # Höhenkoten links + 12-m-Grenze
    for z, t in ((0, "±0,00 OK FFB EG"), (4.3, "+4,30 OK FFB 1. OG"), (7.9, "+7,90 OK FFB 2. OG"), (11.5, "+11,50 Dachfläche"), (12.0, "+12,00 Attika = zulässige Höhe")):
        d.line([(X(-3.9), Zp(z)), (X(34), Zp(z))], fill=(205, 208, 214), width=1); d.text((6, Zp(z) - 10 + (-12 if z == 12 else (10 if z == 11.5 else 0))), t, font=F(15, "SemiBold" if z in (0, 12) else "Regular"), fill=GRN if z == 12 else INK)
    d.line([(X(0), Zp(-0.3)), (X(0), Zp(12.6))], fill=RED, width=2); d.line([(X(30), Zp(-0.3)), (X(30), Zp(12.6))], fill=RED, width=2)
    d.text((X(0) + 4, Zp(12.5)), "Grundstücksgrenze Platz (H1)", font=F(15), fill=RED); d.text((X(30) - 250, Zp(12.5)), "Grundstücksgrenze hinten (H1)", font=F(15), fill=RED)
    d.text((30, H - 70), "Geschosshöhen: EG 4,30 m · 1. OG 3,60 m · 2. OG 3,60 m · Dach/Attika 0,50 m = 12,00 m. Reserve 0,00 m: Aufzugsüberfahrt, Dachaufbauten und Messtoleranz wären zusätzlich zu klären.", font=F(19), fill=INK)
    d.text((30, H - 40), f"Säulen im Schnitt: {sum(1 for p in k['saeulen'] if abs(p[0]-15.0)<0.01)+0} (Achse x ≈ 15 m) · Säulen insgesamt: {k['anzahl_saeulen']} · Stellplatz-Decke Vorbau-Unterkante +3,85 m", font=F(19), fill=INK); return im
if __name__ == "__main__":
    for key in sys.argv[1:] or ["E1", "E2", "E3", "E4"]:
        out = os.path.join(VA.ROOT, "studie_gebaeudeformen", key, "plaene"); os.makedirs(out, exist_ok=True)
        lageplan(key).save(os.path.join(out, "lageplan.png"))
        for lv, nm in (("eg", "plan_eg"), ("og1", "plan_og1"), ("st", "plan_st")): plan(key, lv).save(os.path.join(out, nm + ".png"))
        schnitt(key).save(os.path.join(out, "schnitt.png")); json.dump(dict(parken=pruefe_parken(key), ueber=over_plot(key), abstand3=abstand_szenario(key, 3.0), abstand6=abstand_szenario(key, 6.0)), open(os.path.join(VA.ROOT, "studie_gebaeudeformen", key, "parken.json"), "w"), indent=1, ensure_ascii=False, default=str); print("ok", key)
