"""Schematische Grundrisse (EG, 1. OG, Staffelgeschoss) und Schnitt je Variante, gezeichnet aus denselben Daten wie die Blender-Ansichten (scripts/studie/varianten.py).
Alles schematisch und vorläufig: Wohnungsaufteilung = Streifenmodell (Mittelgang 2,0 m, Modul 5,6 m vorn / 7,0 m hinten), Erdgeschossnutzung wie B3 (Gastro, Küche, Büros, Kern).
Aufruf: python3 zeichne_plaene.py [A B C D]  ->  studie_gebaeudeformen/<Variante>/plaene/{plan_eg,plan_og1,plan_st,schnitt}.png"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import varianten as VA
F = lambda s, w="Regular": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)
INK, GREY, LG = (27, 31, 36), (107, 114, 128), (201, 206, 214)
COL = {"dining": (243, 235, 221), "kitchen": (222, 226, 232), "core": (229, 232, 236), "office": (214, 228, 238), "wc": (229, 232, 236), "bar": (216, 208, 195), "other": (236, 238, 241)}
S = 38  # px je m
def tx(x, ox=0): return int((x + 6) * S)
def ty(y): return int((y + 6) * S) + 70
def draw_rect(d, r, fill=None, outline=INK, w=2, dash=False):
    x0, y0, x1, y1 = r; box = [tx(x0), ty(y0), tx(x1), ty(y1)]
    if fill is not None: d.rectangle(box, fill=fill)
    if dash: dashed(d, box, outline, w)
    elif outline: d.rectangle(box, outline=outline, width=w)
def dashed(d, box, col, w=2, seg=10):
    x0, y0, x1, y1 = box
    for (a, b, c, e) in ((x0, y0, x1, y0), (x0, y1, x1, y1), (x0, y0, x0, y1), (x1, y0, x1, y1)):
        L = math.hypot(c - a, e - b); n = max(1, int(L // seg))
        for i in range(0, n, 2): d.line([(a + (c - a) * i / n, b + (e - b) * i / n), (a + (c - a) * min(i + 1, n) / n, b + (e - b) * min(i + 1, n) / n)], fill=col, width=w)
def hatch(d, r, col=(150, 150, 160), gap=9):
    x0, y0, x1, y1 = [tx(r[0]), ty(r[1]), tx(r[2]), ty(r[3])]
    for k in range(-(y1 - y0), x1 - x0, gap): d.line([(x0 + max(k, 0), y0 + max(-k, 0)), (min(x1, x0 + k + (y1 - y0)), min(y1, y0 + (y1 - y0) - max(0, (k + (y1 - y0)) - (x1 - x0)) if False else y1))], fill=col, width=1) if False else None
    # einfache Schraffur über Linien im Rechteck
    h = y1 - y0; w_ = x1 - x0
    for k in range(-h, w_, gap):
        xa, ya = x0 + max(k, 0), y0 + max(-k, 0); xb, yb = x0 + min(w_, k + h), y0 + min(h, w_ - k)
        if xb > xa: d.line([(xa, ya), (xb, yb)], fill=col, width=1)
def subtract(rects, cut):
    out = []
    for (x0, y0, x1, y1) in rects:
        cx0, cy0, cx1, cy1 = cut
        if cx0 >= x1 or cx1 <= x0 or cy0 >= y1 or cy1 <= y0: out.append((x0, y0, x1, y1)); continue
        if y0 < cy0: out.append((x0, y0, x1, cy0))
        if y1 > cy1: out.append((x0, cy1, x1, y1))
        ym0, ym1 = max(y0, cy0), min(y1, cy1)
        if x0 < cx0: out.append((x0, ym0, cx0, ym1))
        if x1 > cx1: out.append((cx1, ym0, x1, ym1))
    return out
def canvas(title, sub):
    W, H = int(54 * S), int(44 * S) + 70; im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im); d.text((30, 14), title, font=F(34, "SemiBold"), fill=INK); d.text((30, 52), sub, font=F(20), fill=GREY); return im, d
def plot(d):
    x0, y0, x1, y1 = VA.PLOT; dashed(d, [tx(x0), ty(y0), tx(x1), ty(y1)], (190, 30, 30), 3, 14); d.text((tx(x0) + 6, ty(y1) - 28), "Grundstück H1 32 x 30 m (hypothetisch, Zuschnitt unbestätigt)", font=F(18), fill=(190, 30, 30))
def dim(d, a, b, text, side="top"):
    (x0, y0), (x1, y1) = a, b
    d.line([(tx(x0), ty(y0)), (tx(x1), ty(y1))], fill=GREY, width=2); d.text(((tx(x0) + tx(x1)) // 2 - 40, (ty(y0) + ty(y1)) // 2 - 26), text, font=F(18, "SemiBold"), fill=GREY)
def strips(w, mv, mh):
    xs, y0, x1, y1 = w; L = x1 - xs; D = y1 - y0; dd = (D - VA.GANG) / 2; nf = int(L // mv); nr = int(L // mh); res = []
    for i in range(nf): res.append(("v", xs + L / nf * i, y0, xs + L / nf * (i + 1), y0 + dd))
    for i in range(nr): res.append(("h", xs + L / nr * i, y1 - dd, xs + L / nr * (i + 1), y1))
    return res, (xs, y0 + dd, x1, y1 - dd)
def legend(d, y, items):
    x = 40
    for lab, col in items: d.rectangle([x, y, x + 26, y + 18], fill=col, outline=INK); d.text((x + 34, y - 1), lab, font=F(17), fill=INK); x += 44 + int(d.textlength(lab, font=F(17))) + 20
def plan(key, level):
    v = VA.V[key]; k = VA.kennzahlen(key); lab = {"eg": "Erdgeschoss", "og1": "1. Obergeschoss", "st": "Staffelgeschoss"}[level]
    im, d = canvas(f"Variante {key}: {lab} (schematisch)", f"{v['kurz']} · Maßstab schematisch · Wohnungsaufteilung und Nutzung schematisch, Flächen vorläufig (netto = 0,88 x brutto), Himmelsrichtung unbekannt")
    plot(d); rects = v[level]
    # untere Geschosse gestrichelt
    below = {"og1": v["eg"], "st": v["og1"]}.get(level, [])
    for r in below: draw_rect(d, r, None, GREY, 2, True)
    over = subtract(rects, (0, 0, 0, 0)) if False else rects
    if level == "eg":
        for r in rects: draw_rect(d, r, (250, 250, 250), INK, 4)
        for rm in VA.B3["rooms"]:
            if rm["level"] != "GF": continue
            x0, y0, x1, y1 = rm["rect"]; t = rm["type"]; c = COL.get(t, COL["other"]); draw_rect(d, (x0, y0, x1, y1), c, (120, 126, 134), 1)
        for rm in VA.B3["rooms"]:
            if rm["level"] != "GF" or rm["type"] not in ("dining", "kitchen", "bar", "office", "core"): continue
            x0, y0, x1, y1 = rm["rect"]; nm = {"dining": "Gastraum (Möblierung wie B3)", "kitchen": "Küche", "bar": "Bar", "office": rm["id"].replace("-GF", "").replace("OFFICE-", "Büro "), "core": rm["id"].replace("-GF", "")}[rm["type"]]
            if (x1 - x0) * (y1 - y0) > 8: d.text((tx(x0) + 6, ty(y0) + 6), nm, font=F(16), fill=INK)
        for r in rects: draw_rect(d, r, None, INK, 4)
        t = (6, -3.6, 30, 0.0)
        if v["vordach"]: draw_rect(d, t, None, GREY, 2, True); d.text((tx(8), ty(-2.2)), "Terrasse mit Stahlvordach (wie B3)", font=F(17), fill=GREY)
        else: d.text((tx(6), ty(-0.9)), "Terrasse unter dem Vorbau (Anordnung offen)", font=F(17), fill=GREY)
        for r in v["og1"]:
            for ov in subtract([r], (0, 0, 32, 18)): hatch(d, ov, (150, 150, 165))
        legend(d, int(44 * S) + 25, [("Gastronomie", COL["dining"]), ("Küche/Lager/WC", COL["kitchen"]), ("Büro", COL["office"]), ("Kern", COL["core"])])
    else:
        # Dachfläche des unteren Geschosses außerhalb (Terrasse) bei Staffel; bei OG1 die Auskragung schraffiert
        for r in rects: draw_rect(d, r, (252, 247, 240) if level == "st" else (250, 244, 238), INK, 4)
        if level == "st":
            for r in v["og1"]:
                rem = r and [r]
                for s_ in v["st"]: rem = subtract(rem, s_)
                for ov in rem: draw_rect(d, ov, (222, 224, 228), None, 0); hatch(d, ov, (170, 170, 180), 12)
        else:
            for r in rects:
                for ov in subtract([r], (0, 0, 32, 18)): hatch(d, ov, (190, 150, 120), 10)
        xs, y0, x1, y1 = v["wohn"][level]; mv, mh, _ = VA.MIX["standard"]; apt, corr = strips(v["wohn"][level], mv, mh)
        # Kern und Mittelgang
        bx = VA.bbox(rects); core = (bx[0], y0, xs, y1) if level == "og1" else (bx[0], y0, xs, y1); draw_rect(d, core, COL["core"], (110, 116, 124), 2); d.text((tx(core[0]) + 4, ty(core[1]) + 8), "Kern und Nebenräume", font=F(16, "SemiBold"), fill=INK)
        draw_rect(d, corr, (244, 244, 246), (150, 150, 160), 1); d.text((tx(corr[0]) + 20, ty((corr[1] + corr[3]) / 2) - 10), "Mittelgang 2,0 m", font=F(16), fill=GREY)
        n = 0
        for (f, ax0, ay0, ax1, ay1) in apt:
            n += 1; area = round((ax1 - ax0) * (ay1 - ay0) * VA.NETTO, 1); draw_rect(d, (ax0, ay0, ax1, ay1), (242, 222, 212), (110, 80, 70), 2)
            d.text((tx(ax0) + 6, ty(ay0) + 8), f"WE {n}", font=F(18, "SemiBold"), fill=INK); d.text((tx(ax0) + 6, ty(ay0) + 30), f"{area:.0f} m²", font=F(17), fill=INK)
        if v["balkone"] == "front" and level == "og1":
            for b in VA.B3["balconies"]: x0, _, x1, _ = b["rect"]; draw_rect(d, (x0, -1.5, x1, 0), (230, 234, 238), INK, 2)
        for r in rects: draw_rect(d, r, None, INK, 4)
        legend(d, int(44 * S) + 25, [("Wohnung (schematisch)", (242, 222, 212)), ("Kern", COL["core"]), ("Auskragung/Terrasse schraffiert", (222, 224, 228))])
    for (x, y) in k["saeulen"]:
        if level == "eg" or level == "og1": d.ellipse([tx(x) - 8, ty(y) - 8, tx(x) + 8, ty(y) + 8], fill=(20, 20, 20) if level == "eg" else (170, 170, 175), outline=INK)
    bx = VA.bbox(rects); dim(d, (bx[0], bx[1] - 1.8), (bx[2], bx[1] - 1.8), f"{bx[2] - bx[0]:.1f} m"); dim(d, (bx[2] + 1.8, bx[1]), (bx[2] + 1.8, bx[3]), f"{bx[3] - bx[1]:.1f} m")
    d.text((int(36 * S), int(41 * S) + 70), f"Fläche Geschoss {VA.rects_area(rects):.0f} m²", font=F(20, "SemiBold"), fill=INK)
    return im
def schnitt(key):
    v = VA.V[key]; k = VA.kennzahlen(key); sx = [p[0] for p in k["saeulen"]]; xc = min(sx, key=lambda a: abs(a - 16)) if sx else 16.0
    s = 34; W, H = int(44 * s) + 80, int(15 * s) + 150; im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    X = lambda y: int((y + 6) * s) + 40; Zp = lambda z: int(H - 80 - (z + 0.6) * s)
    d.text((30, 14), f"Variante {key}: Schnitt bei x = {xc:.1f} m (schematisch)", font=F(30, "SemiBold"), fill=INK); d.text((30, 52), "Platzseite links, Rückseite rechts · Auskragungen, Staffelung und Säulen · hypothetische Grundstücksgrenzen rot gestrichelt · Konstruktion nicht bemessen", font=F(18), fill=GREY)
    d.line([(X(-6), Zp(0)), (X(36), Zp(0))], fill=INK, width=3)
    def span(rs):
        ys = [(r[1], r[3]) for r in rs if r[0] <= xc <= r[2]]
        if not ys: return None
        ys.sort(); a, b = ys[0]
        for c0, c1 in ys[1:]: b = max(b, c1) if c0 <= b + 0.01 else b
        return (a, b)
    levels = [("EG", v["eg"], 0.0, 3.5, (252, 252, 252), (201, 173, 163)), ("OG1", v["og1"], 3.5, 6.5, (252, 245, 240), (201, 173, 163)), ("ST", v["st"], 6.5, 9.6, (252, 247, 238), (220, 199, 164))]
    for nm, rs, z0, z1, fill, wallc in levels:
        sp = span(rs)
        if not sp: continue
        a, b = sp; d.rectangle([X(a), Zp(z1), X(b), Zp(z0)], fill=fill, outline=INK, width=2); d.rectangle([X(a), Zp(z1), X(a + 0.3), Zp(z0)], fill=wallc); d.rectangle([X(b - 0.3), Zp(z1), X(b), Zp(z0)], fill=wallc)
        lab = {"EG": "Gastronomie / Büros", "OG1": "Wohnungen · Mittelgang", "ST": "Wohnungen · Mittelgang"}[nm]; d.text((X((a + b) / 2) - 90, Zp((z0 + z1) / 2) - 10), lab, font=F(17), fill=INK)
        d.rectangle([X(a - 0.04), Zp(z0 + 0.3), X(b + 0.04), Zp(z0)], fill=(150, 150, 150), outline=INK)
    sp1 = span(v["og1"]); sp2 = span(v["st"]); spe = span(v["eg"])
    d.rectangle([X(sp1[0] - 0.04), Zp(6.5), X(sp1[1] + 0.04), Zp(6.2)], fill=(150, 150, 150), outline=INK); d.rectangle([X(sp2[0] - 0.04), Zp(9.9), X(sp2[1] + 0.04), Zp(9.6)], fill=(110, 110, 115), outline=INK)
    for (x, y) in k["saeulen"]:
        if abs(x - xc) < 0.01: d.rectangle([X(y) - 7, Zp(3.2), X(y) + 7, Zp(0)], fill=(60, 60, 64), outline=INK)
    # Maße Auskragung/Rücksprung
    def ann(y0, y1, z, text, col=(180, 60, 20)):
        d.line([(X(y0), Zp(z)), (X(y1), Zp(z))], fill=col, width=2); d.text((X((y0 + y1) / 2) - 36, Zp(z) - 24), text, font=F(17, "SemiBold"), fill=col)
    if sp1[0] < spe[0] - 0.01: ann(sp1[0], spe[0], 3.0, f"{spe[0] - sp1[0]:.2f} m vorn")
    if sp1[1] > spe[1] + 0.01: ann(spe[1], sp1[1], 3.0, f"{sp1[1] - spe[1]:.2f} m hinten")
    if sp2[0] > sp1[0] + 0.01: ann(sp1[0], sp2[0], 8.0, f"Rücksprung {sp2[0] - sp1[0]:.2f} m")
    if sp1[1] > sp2[1] + 0.01: ann(sp2[1], sp1[1], 8.0, f"Terrasse {sp1[1] - sp2[1]:.2f} m")
    for z, t in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60 Staffeldecke"), (9.9, "+9,90 Attika")): d.line([(X(-5.9), Zp(z)), (X(-5.4), Zp(z))], fill=INK, width=2) if False else None; d.text((6, Zp(z) - 10 + (-14 if z == 9.9 else (8 if z == 9.6 else 0))), t, font=F(15), fill=INK)
    d.line([(X(0), Zp(-0.3)), (X(0), Zp(11))], fill=(190, 30, 30), width=2); d.line([(X(30), Zp(-0.3)), (X(30), Zp(11))], fill=(190, 30, 30), width=2)
    d.text((X(0) + 4, Zp(10.6)), "Grundstücksgrenze Platz (H1)", font=F(15), fill=(190, 30, 30)); d.text((X(30) - 230, Zp(10.6)), "Grundstücksgrenze hinten (H1)", font=F(15), fill=(190, 30, 30))
    d.line([(X(-1), Zp(12.0 - 1.9)), (X(36), Zp(12.0 - 1.9))], fill=(30, 100, 30), width=1) if False else None
    d.text((30, H - 50), f"Gebäudehöhe Attika +9,90 m, zulässig 12,00 m (Bestätigung Auftraggeber), Differenz 2,10 m nicht ausgenutzt · Säulen im Schnitt: {sum(1 for p in k['saeulen'] if abs(p[0] - xc) < 0.01)} · Säulen insgesamt: {k['anzahl_saeulen']}", font=F(19), fill=INK)
    return im
if __name__ == "__main__":
    keys = sys.argv[1:] or list(VA.V)
    for key in keys:
        out = os.path.join(VA.ROOT, "studie_gebaeudeformen", key, "plaene"); os.makedirs(out, exist_ok=True)
        for lv, nm in (("eg", "plan_eg"), ("og1", "plan_og1"), ("st", "plan_st")): plan(key, lv).save(os.path.join(out, nm + ".png"))
        schnitt(key).save(os.path.join(out, "schnitt.png")); print("ok", key)
