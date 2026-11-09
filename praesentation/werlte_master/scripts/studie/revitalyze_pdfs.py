"""Erzeugt die technischen VEKTOR-PDFs für den Revitalyze-Test (PDF -> IFC), je Variante ein Paket, Maßstab 1:100 (A2 quer; Test-PDF A3 quer).
Alle Blätter einer Variante werden aus EINEM Modell (revitalyze_modelle.py) gezeichnet. Keine Rasterbilder, keine Fotos, keine Schattierungen; Text ist echter PDF-Text.
Aufruf: python3 revitalyze_pdfs.py  -> schreibt nach ../../studie_gebaeudeformen/revitalyze_import/ (bestehende Dateien anderer Ordner werden nicht angefasst)."""
import os, math, sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A2, A3, landscape
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import revitalyze_modelle as RM

OUT = os.path.abspath(os.path.join(HIER, "..", "..", "studie_gebaeudeformen", "revitalyze_import"))
DATUM = "27.10.2026"; PROJ = "Neue Mitte Werlte – Baufeld 3"; STEMPEL = "VORLÄUFIGER ENTWURF – NICHT GENEHMIGT"
SC = 10.0   # mm je m  (1:100)
BLACK = (0, 0, 0); GRAY = (0.45, 0.45, 0.45); LGRAY = (0.72, 0.72, 0.72); DIMC = (0.10, 0.25, 0.55); RED = (0.80, 0.10, 0.10); ORANGE = (0.80, 0.42, 0.0); POCHE = (0.86, 0.86, 0.86)
F = "Helvetica"; FB = "Helvetica-Bold"
def n2(v, d=2): return f"{v:.{d}f}".replace(".", ",")
def kote(z): return ("±" if abs(z) < 1e-9 else ("+" if z > 0 else "−")) + n2(abs(z))

def setdash(c, dash):
    c.setDash([d * mm for d in dash]) if dash else c.setDash()

def offset_in(p, t):
    p = list(p); a2 = sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))
    if a2 < 0: p.reverse()
    n = len(p); out = []
    for i in range(n):
        a, b, c = p[i - 1], p[i], p[(i + 1) % n]
        e1 = (b[0] - a[0], b[1] - a[1]); l1 = math.hypot(*e1); e1 = (e1[0] / l1, e1[1] / l1); n1 = (-e1[1], e1[0])
        e2 = (c[0] - b[0], c[1] - b[1]); l2 = math.hypot(*e2); e2 = (e2[0] / l2, e2[1] / l2); n2_ = (-e2[1], e2[0])
        cr = e1[0] * e2[1] - e1[1] * e2[0]
        if abs(cr) < 1e-9: out.append((b[0] + n1[0] * t, b[1] + n1[1] * t)); continue
        p1 = (b[0] + n1[0] * t, b[1] + n1[1] * t); p2 = (b[0] + n2_[0] * t, b[1] + n2_[1] * t)
        # Schnitt der Geraden p1 + s*e1 und p2 + u*e2
        s = ((p2[0] - p1[0]) * e2[1] - (p2[1] - p1[1]) * e2[0]) / cr
        out.append((p1[0] + e1[0] * s, p1[1] + e1[1] * s))
    return out

class Sheet:
    """Ein Blatt: Rahmen, Schriftfeld, Zeichenfläche. (u,v) = Zeichenkoordinaten in m (Grundriss: x,y; Ansicht/Schnitt: h,z)."""
    def __init__(self, c, size, tb, titel_zeile, blatt, nr, nmax, m, anm):
        self.c = c; self.W, self.H = size; self.tb = tb; self.m = m
        self.frame(titel_zeile, blatt, nr, nmax, anm)
    # --- Grundfunktionen ---
    def P(self, u, v): return (self.ox + u * SC) * mm, (self.oy + v * SC) * mm
    def col(self, col, fill=False):
        (self.c.setFillColorRGB if fill else self.c.setStrokeColorRGB)(*col)
    def line(self, u0, v0, u1, v1, w=0.25, dash=None, col=BLACK):
        c = self.c; c.setLineWidth(w * mm); self.col(col); setdash(c, dash); c.line(*self.P(u0, v0), *self.P(u1, v1)); c.setDash()
    def mmline(self, x0, y0, x1, y1, w=0.25, col=BLACK, dash=None):
        c = self.c; c.setLineWidth(w * mm); self.col(col); setdash(c, dash); c.line(x0 * mm, y0 * mm, x1 * mm, y1 * mm); c.setDash()
    def poly(self, pts, w=0.25, close=True, fill=None, dash=None, col=BLACK):
        c = self.c; p = c.beginPath(); q = [self.P(*t) for t in pts]; p.moveTo(*q[0])
        for t in q[1:]: p.lineTo(*t)
        if close: p.close()
        c.setLineWidth(w * mm); self.col(col); setdash(c, dash)
        if fill is not None: self.col(fill, True)
        c.drawPath(p, stroke=1 if w > 0 else 0, fill=1 if fill is not None else 0); c.setDash()
    def rect(self, r, **k): self.poly([(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])], **k)
    def ring(self, outer, inner, w=0.5, fill=POCHE, col=BLACK):
        c = self.c; p = c.beginPath()
        for poly in (outer, inner):
            q = [self.P(*t) for t in poly]; p.moveTo(*q[0])
            for t in q[1:]: p.lineTo(*t)
            p.close()
        c.setLineWidth(w * mm); self.col(col); self.col(fill, True); c.drawPath(p, stroke=1, fill=1, fillMode=0)   # even-odd
    def circle(self, u, v, r, fill=BLACK, w=0.3, col=BLACK):
        c = self.c; c.setLineWidth(w * mm); self.col(col); self.col(fill, True) if fill is not None else None
        x, y = self.P(u, v); c.circle(x, y, r * SC * mm, stroke=1, fill=1 if fill is not None else 0)
    def text(self, u, v, s, size=7, anchor="c", rot=0, col=BLACK, font=F, dx=0, dy=0):
        c = self.c; x, y = self.P(u, v); x += dx * mm; y += dy * mm; c.saveState(); c.translate(x, y); c.rotate(rot); c.setFont(font, size); self.col(col, True)
        {"c": c.drawCentredString, "l": c.drawString, "r": c.drawRightString}[anchor](0, 0, s); c.restoreState()
    def tw(self, s, size=7, font=F): return stringWidth(s, font, size) / mm
    def fit(self, bbox, pad=0.0):
        u0, v0, u1, v1 = bbox; ax0, ay0, ax1, ay1 = self.area; w, h = (u1 - u0) * SC, (v1 - v0) * SC
        if w > ax1 - ax0 + 1e-6 or h > ay1 - ay0 + 1e-6: raise ValueError(f"Zeichnung passt nicht aufs Blatt: {w:.0f}x{h:.0f} mm in {ax1 - ax0:.0f}x{ay1 - ay0:.0f} mm")
        self.ox = ax0 + (ax1 - ax0 - w) / 2 - u0 * SC; self.oy = ay0 + (ay1 - ay0 - h) / 2 - v0 * SC
    # --- Rahmen & Schriftfeld ---
    def frame(self, titel, blatt, nr, nmax, anm):
        W, H = self.W, self.H; mg = 8
        self.mmline(mg, mg, W - mg, mg, 0.5); self.mmline(W - mg, mg, W - mg, H - mg, 0.5); self.mmline(W - mg, H - mg, mg, H - mg, 0.5); self.mmline(mg, H - mg, mg, mg, 0.5)
        m = self.m
        rows = [("Projekt", PROJ), ("Variante", m["titel"]), ("Zeichnung", titel), ("Maßstab", "1:100 (Blattgröße " + ("A2" if W > 500 else "A3") + " quer)"), ("Datum", DATUM), ("Blatt", f"{nr} / {nmax}  –  {blatt}"),
                ("Höhen", m["hoehenstatus"]), ("Status", STEMPEL)]
        if self.tb == "right":
            x0 = W - mg - 66; self.area = (mg + 4, mg + 4, x0 - 4, H - mg - 4); self.mmline(x0, mg, x0, H - mg, 0.5)
            y = H - mg - 6
            for k, v in rows:
                self.c.setFillColorRGB(*GRAY); self.c.setFont(F, 6); self.c.drawString((x0 + 3) * mm, y * mm, k.upper()); y -= 4.2
                lines = wrap(v, FB if k in ("Zeichnung", "Status") else F, 8 if k in ("Zeichnung", "Status") else 7.5, 60)
                for ln in lines:
                    self.c.setFillColorRGB(*(RED if k == "Status" else BLACK)); self.c.setFont(FB if k in ("Zeichnung", "Status") else F, 8 if k in ("Zeichnung", "Status") else 7.5); self.c.drawString((x0 + 3) * mm, y * mm, ln); y -= 4
                y -= 2.5; self.mmline(x0, y + 3.2, W - mg, y + 3.2, 0.15, LGRAY)
            y -= 1; self.c.setFillColorRGB(*GRAY); self.c.setFont(F, 6); self.c.drawString((x0 + 3) * mm, y * mm, "ANMERKUNGEN"); y -= 4
            for a in anm:
                for ln in wrap(a, F, 6.5, 60):
                    self.c.setFillColorRGB(*BLACK); self.c.setFont(F, 6.5); self.c.drawString((x0 + 3) * mm, y * mm, ln); y -= 3.3
                y -= 1.2
            self.tbx = (x0, mg, W - mg, H - mg)
        else:
            h = 34; y0 = mg + h; self.area = (mg + 4, y0 + 4, W - mg - 4, H - mg - 4); self.mmline(mg, y0, W - mg, y0, 0.5)
            cols = [(mg + 3, rows[0:3]), (mg + 3 + 105, rows[3:6]), (mg + 3 + 195, rows[6:8])]
            for x, rr in cols:
                y = y0 - 5
                for k, v in rr:
                    self.c.setFillColorRGB(*GRAY); self.c.setFont(F, 5.5); self.c.drawString(x * mm, y * mm, k.upper()); y -= 3.6
                    for ln in wrap(v, FB if k in ("Zeichnung", "Status") else F, 7.5, 98 if x < mg + 100 else (85 if x < mg + 150 else 92)):
                        self.c.setFillColorRGB(*(RED if k == "Status" else BLACK)); self.c.setFont(FB if k in ("Zeichnung", "Status") else F, 7.5); self.c.drawString(x * mm, y * mm, ln); y -= 3.6
                    y -= 1.2
            y = y0 - 5
            self.c.setFillColorRGB(*GRAY); self.c.setFont(F, 5.5); self.c.drawString((mg + 3 + 292) * mm, y * mm, "ANMERKUNGEN"); y -= 3.6
            for a in anm:
                for ln in wrap(a, F, 6.5, 100): self.c.setFillColorRGB(*BLACK); self.c.setFont(F, 6.5); self.c.drawString((mg + 3 + 292) * mm, y * mm, ln); y -= 3.2
                y -= 0.8

def wrap(s, font, size, wmm):
    out = []; cur = ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) / mm <= wmm: cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out or [""]

# ---------- Bemaßung ----------
def dim_chain(sh, vals, axis, base, off, sign=-1, size=5.5, ext_from=None, label_min=0.55):
    """Maßkette. axis 'h': Kette läuft in u-Richtung auf v = base + sign*off; axis 'v': in v-Richtung auf u = base + sign*off."""
    vals = sorted({round(v, 3) for v in vals}); pos = base + sign * off
    if len(vals) < 2: return
    a, b = vals[0], vals[-1]
    ext0 = base + sign * 0.15 if ext_from is None else ext_from
    for v in vals:
        if axis == "h": sh.line(v, ext0, v, pos + sign * 0.25, 0.1, col=DIMC)
        else: sh.line(ext0, v, pos + sign * 0.25, v, 0.1, col=DIMC)
    if axis == "h": sh.line(a - 0.15, pos, b + 0.15, pos, 0.13, col=DIMC)
    else: sh.line(pos, a - 0.15, pos, b + 0.15, 0.13, col=DIMC)
    for v in vals:      # Schrägstrich-Marken
        if axis == "h": sh.line(v - 0.1, pos - 0.1, v + 0.1, pos + 0.1, 0.35, col=DIMC)
        else: sh.line(pos - 0.1, v - 0.1, pos + 0.1, v + 0.1, 0.35, col=DIMC)
    for i in range(len(vals) - 1):
        l = vals[i + 1] - vals[i]; mid = (vals[i] + vals[i + 1]) / 2; s = n2(l)
        if l < label_min or l * SC < sh.tw(s, size) + 1.2: continue
        if axis == "h": sh.text(mid, pos, s, size, "c", col=DIMC, dy=0.9)
        else: sh.text(pos, mid, s, size, "c", rot=90, col=DIMC, dx=-0.9)

def legend_sample(sh, x, y, kind, label):
    c = sh.c
    if kind == "wall": sh.c.setLineWidth(0.5 * mm); sh.col(BLACK); sh.col(POCHE, True); c.rect(x * mm, (y - 1.2) * mm, 14 * mm, 2.4 * mm, stroke=1, fill=1)
    elif kind == "room": sh.mmline(x, y, x + 14, y, 0.18, GRAY)
    elif kind == "dim": sh.mmline(x, y, x + 14, y, 0.13, DIMC); sh.mmline(x + 1, y - 1, x + 2.5, y + 1, 0.35, DIMC); sh.mmline(x + 11.5, y - 1, x + 13, y + 1, 0.35, DIMC)
    elif kind == "dash": sh.mmline(x, y, x + 14, y, 0.25, GRAY, (3, 1.5))
    elif kind == "dashdot": sh.mmline(x, y, x + 14, y, 0.5, BLACK, (6, 1.5, 1, 1.5))
    elif kind == "plot": sh.mmline(x, y, x + 14, y, 0.35, RED, (5, 2))
    elif kind == "col": sh.c.setFillColorRGB(0, 0, 0); c.circle((x + 7) * mm, y * mm, 2.0 * mm, stroke=1, fill=1)
    elif kind == "glass":
        for dy in (-0.6, 0, 0.6): sh.mmline(x, y + dy, x + 14, y + dy, 0.12, BLACK)
    elif kind == "door": sh.mmline(x, y, x + 14, y, 0.3, BLACK)
    elif kind == "cut": sh.c.setFillColorRGB(0, 0, 0); c.rect(x * mm, (y - 1) * mm, 14 * mm, 2 * mm, stroke=0, fill=1)
    sh.c.setFillColorRGB(*BLACK); sh.c.setFont(F, 7); sh.c.drawString((x + 17) * mm, (y - 0.8) * mm, label)

# ---------- Grundriss ----------
LV_NAME = {"EG": "Erdgeschoss (EG)", "OG1": "1. Obergeschoss (OG1)", "ST": None}
def top_name(m): return "Staffelgeschoss" if m["gruppe"] == "A" else ("2. Obergeschoss (oberstes Geschoss)" + (" – bündig" if m["setback"] == 0 else f" – Staffel {n2(m['setback'])} m"))
def lv_title(m, k): return top_name(m) if k == "ST" else LV_NAME[k]
def level_idx(m, z): return "EG" if z < m["zfloor"]["OG1"] else ("OG1" if z < m["zfloor"]["ST"] else "ST")

def plan_bbox(m, k, with_plot=True):
    pts = list(m["levels"][k]["poly"])
    if with_plot: pts += m["plot"]
    if m["gruppe"] == "A":
        for b in m["balkone"]: pts += [(b[0], b[1]), (b[2], b[3])]
        if m["vordach"]: v = m["vordach"]; pts += [(v["x"][0], v["y"][0]), (v["x"][1], v["y"][1])]
    for c in m["saeulen"]: pts.append((c[0] - 0.2, c[1] - 0.2))
    u = [p[0] for p in pts]; v = [p[1] for p in pts]; return (min(u), min(v), max(u), max(v))

def sect_mark(sh, m, k):
    xc = m["schnitt_x"]; b = plan_bbox(m, k, False); y0, y1 = b[1] - 3.0, RM.bb(m['levels'][k]['poly'])[3] + 0.8
    sh.line(xc, y0, xc, y1, 0.5, (6, 1.5, 1, 1.5))
    for yy, sgn in ((y0, 1), (y1, -1)):
        sh.line(xc, yy, xc - 0.9, yy, 0.5)  # Blickrichtung -x (nach Westen)
        sh.poly([(xc - 0.9, yy), (xc - 0.5, yy + 0.18), (xc - 0.5, yy - 0.18)], 0.2, fill=BLACK)
        sh.circle(xc, yy + (-0.9 if yy == y0 else 0.9), 0.45, fill=(1, 1, 1), w=0.3)
        sh.text(xc, yy + (-0.9 if yy == y0 else 0.9), "A", 8, "c", font=FB, dy=-1.4)

def draw_opening_plan(sh, m, o, t=RM.WAND):
    sd = o["side"]; p = o["pos"]
    if sd == "-y": r = (o["a0"], p, o["a1"], p + t)
    elif sd == "+y": r = (o["a0"], p - t, o["a1"], p)
    elif sd == "-x": r = (p, o["a0"], p + t, o["a1"])
    else: r = (p - t, o["a0"], p, o["a1"])
    sh.rect(r, w=0, fill=(1, 1, 1))
    horiz = sd in ("-y", "+y")
    if o["kind"] == "glas":
        for f in (0.15, 0.5, 0.85):
            if horiz: sh.line(r[0], r[1] + f * t, r[2], r[1] + f * t, 0.15)
            else: sh.line(r[0] + f * t, r[1], r[0] + f * t, r[3], 0.15)
    else:
        if horiz: sh.line(r[0], r[1] + t / 2, r[2], r[1] + t / 2, 0.35)
        else: sh.line(r[0] + t / 2, r[1], r[0] + t / 2, r[3], 0.35)
    # Laibungen
    if horiz: sh.line(r[0], r[1], r[0], r[3], 0.5); sh.line(r[2], r[1], r[2], r[3], 0.5)
    else: sh.line(r[0], r[1], r[2], r[1], 0.5); sh.line(r[0], r[3], r[2], r[3], 0.5)

def room_label(sh, rm, size=6.2):
    r = rm["rect"]; w, h = (r[2] - r[0]) * SC, (r[3] - r[1]) * SC; cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
    name = rm["name"]; sub = rm["id"]
    for sz in (size, 5.5, 4.8):
        if sh.tw(name, sz) + 1.5 <= w and 2.2 * 1.6 <= h:
            two = h >= 7.5 and sh.tw(sub, sz - 1) + 1.5 <= w
            if rm['id'].startswith(('LIFT', 'STAIR')):
                ww = max(sh.tw(name, sz), sh.tw(sub, sz - 1.2) if two else 0) + 1.2; x_, y_ = sh.P(cx, cy); sh.c.setFillColorRGB(1, 1, 1); sh.c.rect(x_ - ww / 2 * mm, y_ - (3.4 if two else 1.6) * mm, ww * mm, (6.2 if two else 3.4) * mm, stroke=0, fill=1)
            sh.text(cx, cy, name, sz, "c", font=FB, dy=1.0 if two else -0.8)
            if two: sh.text(cx, cy, sub, sz - 1.2, "c", col=GRAY, dy=-2.4)
            return True
    return False

def plan(sh, m, k, test=False):
    lv = m["levels"][k]; poly = lv["poly"]; keys = ["EG", "OG1", "ST"]; i = keys.index(k)
    if i > 0 and not test: sh.poly(m["levels"][keys[i - 1]]["poly"], 0.3, dash=(3, 1.5), col=GRAY)
    # Raumgrenzen
    for rm in lv["rooms"]: sh.rect(rm["rect"], w=0.18, col=GRAY)
    # Aufzug / Treppe
    for rm in lv["rooms"]:
        r = rm["rect"]
        if rm["id"].startswith("LIFT"): sh.line(r[0], r[1], r[2], r[3], 0.18, col=GRAY); sh.line(r[0], r[3], r[2], r[1], 0.18, col=GRAY)
        if rm["id"].startswith("STAIR"): sh.line(r[0], r[1], r[2], r[3], 0.18, col=GRAY)
    inner = offset_in(poly, RM.WAND); sh.ring(poly, inner, 0.5)
    for o in m["openings"]:
        if level_idx(m, o["z"][0]) == k: draw_opening_plan(sh, m, o)
    if m["gruppe"] == "B" and k == "EG":
        gx0, gx1, gy = m["glasfront"]
        sh.rect((gx0, gy, gx1, gy + RM.WAND), w=0, fill=(1, 1, 1)); [sh.line(gx0, gy + f * RM.WAND, gx1, gy + f * RM.WAND, 0.15) for f in (0.15, 0.5, 0.85)]
        sh.line(gx0, gy, gx0, gy + RM.WAND, 0.5); sh.line(gx1, gy, gx1, gy + RM.WAND, 0.5)
    for rm in lv["rooms"]:
        if not room_label(sh, rm) and rm["rect"][2] - rm["rect"][0] > 0.5: pass
    # Säulen
    for c_ in m["saeulen"]: sh.circle(c_[0], c_[1], RM.SAEULE_D / 2, fill=BLACK, w=0.2)
    # A: Balkone/Vordach/Terrasse
    if m["gruppe"] == "A":
        if k == "OG1":
            for b in m["balkone"]: sh.rect(b, w=0.35); sh.text((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, "Balkon", 5.2, "c")
        if k == "EG" and m["vordach"] and not test:
            v = m["vordach"]; sh.rect((v["x"][0], v["y"][0], v["x"][1], v["y"][1]), w=0.3, dash=(3, 1.5), col=GRAY); sh.text(10, v["y"][0] + 1.8, "Stahlvordach Terrasse darüber (Unterseite +3,00 m, ANNAHME)", 5.5, "c", col=GRAY)
        if k == "OG1":
            t = m["terrasse"]; sh.rect(t, w=0, fill=None); sh.text((t[0] + t[2]) / 2, (t[1] + t[3]) / 2, "Dachterrasse über Anbau – Belag NOCH OFFEN", 5.5, "c", col=GRAY, dy=-5) if False else None
        if k == "ST":
            t = m["terrasse"]; sh.rect(t, w=0.25, dash=(2, 1.5), col=GRAY); sh.text((t[0] + t[2]) / 2, (t[1] + t[3]) / 2, "Dachterrasse (Dach OG1-Anbau), Belag NOCH OFFEN", 5.5, "c", col=GRAY)
        if k == "EG" and m["schacht"]: sh.rect(m["schacht"], w=0.3); sh.text((m["schacht"][0] + m["schacht"][2]) / 2, m["schacht"][1] - 0.6, "Küchenabluftschacht (vorl.)", 4.8, "c", col=GRAY)
    else:
        if k != "EG" and i == 2 and m["setback"]:
            b = bb_ = RM.bb(m["levels"]["OG1"]["poly"]); sh.text((b[0] + b[2]) / 2, b[1] + 0.8, "Dachterrasse umlaufend (Breite " + n2(m["setback"]) + " m), Belag NOCH OFFEN", 5.2, "c", col=GRAY)
        if k != "EG":
            sh.text((RM.bb(poly)[0] + RM.bb(poly)[2]) / 2, (RM.bb(poly)[1] + RM.bb(poly)[3]) / 2 + 2, "Raumaufteilung NOCH OFFEN (keine Daten)", 7, "c", col=ORANGE, font=FB)
            sh.text((RM.bb(poly)[0] + RM.bb(poly)[2]) / 2, (RM.bb(poly)[1] + RM.bb(poly)[3]) / 2 - 1, "Kern/Treppe/Aufzug im OG NOCH OFFEN", 6, "c", col=ORANGE)
            sh.text((RM.bb(poly)[0] + RM.bb(poly)[2]) / 2, (RM.bb(poly)[1] + RM.bb(poly)[3]) / 2 - 3.5, "Nutzung Wohnen = ANNAHME", 6, "c", col=ORANGE)
        if k == "EG":
            b = RM.bb(poly); sh.text(10.0, -0.9, "Eingänge siehe Blatt Stellplätze/Erschließung", 5, "c", col=GRAY) if False else None
    sect_mark(sh, m, k) if not test else None
    # Bemaßung
    b = RM.bb(poly); xs = {p[0] for p in poly}; ys = {p[1] for p in poly}
    if test: pb = b
    else: pb = plan_bbox(m, k, False)
    xs_c = set(xs); ys_c = set(ys)
    if m["gruppe"] == "B": xs_c |= {c[0] for c in m["saeulen"] if c[1] == min(cc[1] for cc in m["saeulen"])} if m["saeulen"] and k != "EG" else set()
    ybase = pb[1]; first = ybase - 1.0 if not test else b[1] - 1.0
    ox_ = {v for o in m["openings"] if o["side"] == "-y" and level_idx(m, o["z"][0]) == k for v in (o["a0"], o["a1"])}
    c1 = set(xs_c) | ox_
    dim_chain(sh, c1, "h", first, 0.0, -1, ext_from=b[1] - 0.2)
    if len(c1) > 2: dim_chain(sh, [b[0], b[2]], "h", first, 1.0, -1, ext_from=b[1] - 0.2)
    rx = {r["rect"][0] for r in lv["rooms"]} | {r["rect"][2] for r in lv["rooms"]}
    if rx and not test: dim_chain(sh, rx, "h", b[3], 1.2, +1, ext_from=b[3] + 0.2)
    elif rx: dim_chain(sh, rx, "h", b[3], 1.0, +1, ext_from=b[3] + 0.2)
    lx = pb[0] - 1.0 if not test else b[0] - 1.0
    dim_chain(sh, ys_c, "v", lx, 0.0, -1, ext_from=b[0] - 0.2)
    if len(ys_c) > 2: dim_chain(sh, [b[1], b[3]], "v", lx, 1.0, -1, ext_from=b[0] - 0.2)
    ry = {r["rect"][1] for r in lv["rooms"]} | {r["rect"][3] for r in lv["rooms"]}
    if ry: dim_chain(sh, ry, "v", b[2], 1.2, +1, ext_from=b[2] + 0.2)
    # Höhenkote
    if test: sh.text(b[0], b[3] + 2.2, "Testblatt: nur EG-Grundriss, Wandstärke 0,30 m = ANNAHME, Innentüren/Türanschläge NOCH OFFEN (nicht gezeichnet)", 6, "l", col=ORANGE)

WAND_T = RM.WAND

# ---------- Ansichten ----------
SIDES = {"front": ("Vorderansicht (Platzseite, Blick von Platz)", lambda x, y: x, "-y"), "rear": ("Rückansicht (Blick von der Rückseite)", lambda x, y: -x, "+y"),
         "west": ("Westansicht (Seite x = 0; Nordrichtung NOCH OFFEN)", lambda x, y: -y, "-x"), "east": ("Ostansicht (Seite Ost; Nordrichtung NOCH OFFEN)", lambda x, y: y, "+x")}
def extents(m, hf, k):
    hs = [hf(*p) for p in m["levels"][k]["poly"]]; return min(hs), max(hs)
def elev_bbox(m, hf):
    hs = []
    for k in m["levels"]: hs += list(extents(m, hf, k))
    if m["gruppe"] == "A":
        for b in m["balkone"]: hs += [hf(b[0], b[1]), hf(b[2], b[3])]
        v = m["vordach"]; hs += [hf(v["x"][0], v["y"][0]), hf(v["x"][1], v["y"][1])]
    return min(hs), max(hs)
def elev_columns(m, side):
    cs = m["saeulen"]
    if not cs: return []
    if side == "front": r = min(c[1] for c in cs); return [c for c in cs if abs(c[1] - r) < 1e-6]
    if side == "rear": r = max(c[1] for c in cs); return [c for c in cs if abs(c[1] - r) < 1e-6]
    if side == "west": r = min(c[0] for c in cs); return [c for c in cs if abs(c[0] - r) < 1e-6]
    r = max(c[0] for c in cs); return [c for c in cs if abs(c[0] - r) < 1e-6]

def storeys(m):
    z = m["zfloor"]; t = m["slab"]
    return [("EG", 0.0, z["OG1"] - t), ("OG1", z["OG1"], z["ST"] - t), ("ST", z["ST"], m["ztop_st"])]

def elevation(sh, m, side):
    name, hf, osd = SIDES[side]; z = m["zfloor"]; t = m["slab"]; sdir = 1
    # Geschosskörper
    for k, z0, z1 in storeys(m):
        a, b = extents(m, hf, k); sh.rect((a, z0, b, z1), w=0.5, fill=(1, 1, 1))
    for k, zf in (("OG1", z["OG1"]), ("ST", z["ST"])):        # Deckenkanten (Platten) in Umriss des darunterliegenden Geschosses (Auskragung sichtbar)
        a, b = extents(m, hf, "OG1"); sh.rect((a, zf - t, b, zf), w=0.5, fill=POCHE)
    a, b = extents(m, hf, "ST"); sh.rect((a, m["ztop_st"], b, m["zattika"]), w=0.5, fill=POCHE)
    # Öffnungen
    for o in m["openings"]:
        if o["side"] != osd: continue
        h0, h1 = (o["a0"], o["a1"]) if side in ("front", "east") else (-o["a1"], -o["a0"])
        if side == "west": h0, h1 = -o["a1"], -o["a0"]
        if side == "rear": h0, h1 = -o["a1"], -o["a0"]
        sh.rect((h0, o["z"][0], h1, o["z"][1]), w=0.3, fill=(1, 1, 1))
        if o["kind"] == "glas":
            for i in range(1, o["div"]): hh = h0 + (h1 - h0) * i / o["div"]; sh.line(hh, o["z"][0], hh, o["z"][1], 0.2)
        else: sh.line(h0, o["z"][0], h1, o["z"][1], 0.15, col=GRAY); sh.line(h0, o["z"][1], h1, o["z"][0], 0.15, col=GRAY) if False else None
    # Balkone / Vordach (A, nur Vorderansicht sichtbar-relevant; Seitenansichten: Auskragung)
    if m["gruppe"] == "A":
        for bl in m["balkone"]:
            h0, h1 = sorted((hf(bl[0], bl[1]), hf(bl[2], bl[3])))
            if side in ("front",): sh.rect((h0, 3.2, h1, 3.5), w=0.4, fill=POCHE); sh.rect((h0, 3.5, h1, 4.6), w=0.3, fill=(1, 1, 1)); sh.text((h0 + h1) / 2, 4.0, "Brüstung", 4.6, "c", col=GRAY) if (h1 - h0) * SC > 11 else None
            if side in ("west", "east") and False: pass
        v = m["vordach"]; h0, h1 = sorted((hf(v["x"][0], v["y"][0]), hf(v["x"][1], v["y"][1])))
        if side == "front": sh.rect((h0, 3.0, h1, 3.1), w=0.4, fill=POCHE)
    for cc in elev_columns(m, side):
        h = hf(*cc); sh.rect((h - RM.SAEULE_D / 2, 0, h + RM.SAEULE_D / 2, z["OG1"] - t), w=0.3, fill=BLACK)
    # Gelände / Bezugshöhe
    a, b = elev_bbox(m, hf)
    sh.line(a - 1.5, 0, b + 1.5, 0, 0.9)
    sh.text(a - 1.5, 0, "±0,00 = OK Fertigfußboden EG (Gelände ANNAHME bündig)", 5.5, "l", dy=-3.2)
    if m["gruppe"] == "B": sh.text((a + b) / 2, z["ST"] + 1.8, "Fassadenöffnungen NOCH OFFEN – nicht gezeichnet", 6.5, "c", col=ORANGE, font=FB)
    # Höhenkoten rechts
    xr = b + 1.2
    levels = [("OK Fertigfußboden EG", 0.0), ("OK Fertigfußboden 1. OG", z["OG1"]), ("OK Fertigfußboden " + ("Staffelgeschoss" if m["gruppe"] == "A" else "2. OG"), z["ST"]), ("OK Dach/Decke oberstes Geschoss", m["ztop_st"]), ("OK Attika", m["zattika"])]
    for lab, zz in levels:
        sh.line(a - 1.0, zz, xr + 0.6, zz, 0.12, (6, 2), DIMC) if zz > 0 else None
        sh.poly([(xr, zz), (xr + 0.25, zz + 0.4), (xr - 0.25, zz + 0.4)], 0.2, fill=DIMC, col=DIMC)
        sh.text(xr + 0.5, zz, kote(zz) + "  " + lab, 6, "l", col=DIMC, dy=0.7)
    dim_chain(sh, [0.0, z["OG1"], z["ST"], m["ztop_st"], m["zattika"]], "v", b + 0.2, 0.5, +1, ext_from=b + 0.05) if False else None
    dim_chain(sh, [0.0, z["OG1"], z["ST"], m["ztop_st"], m["zattika"]], "v", a, 1.2, -1, ext_from=a - 0.1)
    # Breitenmaße
    xs = set()
    for k in m["levels"]: xs |= set(extents(m, hf, k))
    dim_chain(sh, xs, "h", 0.0, 1.8, -1, ext_from=-0.1)
    dim_chain(sh, [a, b], "h", 0.0, 2.8, -1, ext_from=-0.1)
    ccs = elev_columns(m, side)
    if ccs: dim_chain(sh, [hf(*cc) for cc in ccs], "h", 0.0, 0.9, -1, ext_from=-0.1)
    sh.text(a, m["zattika"] + 1.6, name, 8, "l", font=FB)
    sh.text(a, m["zattika"] + 0.7, "Geschosshöhen: " + m["hoehenstatus"], 5.5, "l", col=ORANGE)

# ---------- Schnitt ----------
def cut_intervals(poly, xc):
    ys = []
    n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if y0 == y1 and min(x0, x1) < xc + 1e-9 < max(x0, x1) + 1e-9 and min(x0, x1) <= xc < max(x0, x1): ys.append(y0)
    ys.sort(); return [(ys[i], ys[i + 1]) for i in range(0, len(ys) - 1, 2)]

def section(sh, m):
    xc = m["schnitt_x"]; z = m["zfloor"]; t = m["slab"]; W_ = RM.WAND
    cuts = {k: cut_intervals(m["levels"][k]["poly"], xc) for k in m["levels"]}
    for cc in m["saeulen"]:
        if cc[0] < xc - 0.2: sh.rect((cc[1] - 0.2, 0, cc[1] + 0.2, z["OG1"] - t), w=0.2, col=GRAY)
    cut_cols = [cc for cc in m["saeulen"] if abs(cc[0] - xc) <= 0.2]
    for cc in cut_cols: sh.rect((cc[1] - 0.2, 0, cc[1] + 0.2, z["OG1"] - t), w=0.3, fill=BLACK)
    # Platten (geschnitten)
    for zf in (z["OG1"], z["ST"]):
        for a, b in cuts["OG1"]: sh.rect((a, zf - t, b, zf), w=0.3, fill=BLACK)
    for a, b in cuts["ST"]:
        sh.rect((a, m["ztop_st"] - t, b, m["ztop_st"]), w=0.3, fill=BLACK)
    # Wände (geschnitten)
    for k, z0, z1 in storeys(m):
        for a, b in cuts[k]:
            z1_ = z1 if k != "ST" else m["ztop_st"] - t
            sh.rect((a, z0, a + W_, z1_), w=0.3, fill=BLACK); sh.rect((b - W_, z0, b, z1_), w=0.3, fill=BLACK)
    for a, b in cuts["ST"]:
        sh.rect((a, m["ztop_st"], a + W_, m["zattika"]), w=0.3, fill=BLACK); sh.rect((b - W_, m["ztop_st"], b, m["zattika"]), w=0.3, fill=BLACK)
    # Räume im Schnitt (nur wo Raumdaten vorliegen)
    for k, z0, z1 in storeys(m):
        for rm in m["levels"][k]["rooms"]:
            r = rm["rect"]
            if r[0] < xc < r[2]:
                zz = (z0 + z1) / 2; w = (r[3] - r[1]) * SC
                if sh.tw(rm["name"], 5.5) + 1.5 < w: sh.text((r[1] + r[3]) / 2, zz, rm["name"], 5.5, "c", col=GRAY)
    if m["gruppe"] == "B":
        for k, z0, z1 in storeys(m): sh.text(cuts[k][0][0] + (cuts[k][0][1] - cuts[k][0][0]) / 2, (z0 + z1) / 2, "Raumaufteilung NOCH OFFEN", 6.5, "c", col=ORANGE)
    a = min(c[0] for k in cuts for c in cuts[k]); b = max(c[1] for k in cuts for c in cuts[k])
    sh.line(a - 1.5, 0, b + 1.5, 0, 0.9); sh.text(a - 1.5, 0, "±0,00 = OK Fertigfußboden EG (Gelände ANNAHME bündig; Bodenplatte NOCH OFFEN)", 5.5, "l", dy=-3.2)
    xr = b + 1.2
    for lab, zz in (("OK Fertigfußboden EG", 0.0), ("OK Fertigfußboden 1. OG", z["OG1"]), ("OK Fertigfußboden " + ("Staffelgeschoss" if m["gruppe"] == "A" else "2. OG"), z["ST"]), ("OK Dach oberstes Geschoss", m["ztop_st"]), ("OK Attika", m["zattika"])):
        sh.line(a - 1.0, zz, xr + 0.6, zz, 0.12, (6, 2), DIMC) if zz > 0 else None
        sh.poly([(xr, zz), (xr + 0.25, zz + 0.4), (xr - 0.25, zz + 0.4)], 0.2, fill=DIMC, col=DIMC)
        sh.text(xr + 0.5, zz, kote(zz) + "  " + lab, 6, "l", col=DIMC, dy=0.7)
    # Deckenstärke
    sh.text(b + 0.4, z["OG1"] - t / 2, "", 5)
    dim_chain(sh, [0.0, z["OG1"], z["ST"], m["ztop_st"], m["zattika"]], "v", a, 1.2, -1, ext_from=a - 0.1)
    ys = {y for k in cuts for c in cuts[k] for y in c}; sh.text(a, -3.0, "", 5)
    dim_chain(sh, ys, "h", 0.0, 1.8, -1, ext_from=-0.1); dim_chain(sh, [a, b], "h", 0.0, 2.8, -1, ext_from=-0.1)
    sh.text(a, m["zattika"] + 1.6, f"Schnitt A–A  (Schnittlinie x = {n2(xc)} m, Blick nach Westen; Platzseite links)", 8, "l", font=FB)
    sh.text(a, m["zattika"] + 0.7, f"Geschossdecken {m['slab_status']}; Höhen: {m['hoehenstatus']}", 5.5, "l", col=ORANGE)
    sh.text(a, -4.0, "Platzseite (y = 0)", 6, "l"); sh.text(b, -4.0, "Rückseite", 6, "r")
    return a, b

# ---------- Lageplan Stellplätze / Erschließung ----------
def erschliessung(sh, m):
    sh.poly(m["plot"], 0.35, dash=(5, 2), col=RED)
    sh.text(0.3, m["plot"][0][1] + 0.35, "Grundstücksgrenze HYPOTHESE 32 × 30 m = 960 m² (nicht bestätigt)", 5.5, "l", col=RED)
    sh.rect(m["aisle"], w=0.25, dash=(1, 1.5), col=GRAY)
    a = m["aisle"]; sh.text((a[0] + a[2]) / 2, (a[1] + a[3]) / 2 + (0 if m["gruppe"] == "A" else 0), f"Fahrgasse {n2(a[2] - a[0] if m['gruppe'] == 'B' else a[3] - a[1])} m (ANNAHME)", 7, "c", col=GRAY, rot=0 if m["gruppe"] == "A" else 90)
    sh.poly(m["levels"]["OG1"]["poly"], 0.35, dash=(3, 1.5), col=GRAY)
    sh.poly(m["levels"]["EG"]["poly"], 0.7, fill=POCHE)
    sh.text(*[(RM.bb(m["levels"]["EG"]["poly"])[0] + RM.bb(m["levels"]["EG"]["poly"])[2]) / 2, RM.bb(m["levels"]["EG"]["poly"])[1] + 3], "Gebäude EG", 8, "c", font=FB) if False else None
    b = RM.bb(m["levels"]["EG"]["poly"]); sh.text((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, f"Gebäude EG ({n2(b[2] - b[0])} × {n2(b[3] - b[1])} m)", 8, "c", font=FB)
    sh.text((b[0] + b[2]) / 2, (b[1] + b[3]) / 2 - 2, "gestrichelt: Umriss 1. OG (überdeckt Stellplätze/Wege)", 6, "c", col=GRAY)
    if m["gruppe"] == "A":
        for i, s in enumerate(m["stalls"]): sh.rect(s, w=0.3); sh.text((s[0] + s[2]) / 2, (s[1] + s[3]) / 2, f"SP{i + 1}", 6, "c")
        for w_ in m["walkways"]: sh.rect((w_[0], 18.0, w_[1], 23.0), w=0.2, dash=(1, 1.5), col=GRAY); sh.text((w_[0] + w_[1]) / 2, 23.35, "Durchgang", 4.6, "c", col=GRAY)
        ein = [(o["tag"], (o["a0"], -0.9, o["a1"], 0.0)) for o in m["openings"] if o["side"] == "-y" and o["kind"] == "tuer"] + [("Eingang Kern", (1.0, -0.9, 2.5, 0.0))] + [("Tür Ost", (32.0, 15.5, 32.9, 16.7))]
        ein += [(f"EG-Tür hinten {i + 1}", (w_[0], 18.0, w_[1], 18.9)) for i, w_ in enumerate(m["walkways"])]
    else:
        for i, s in enumerate(m["stalls"]): sh.rect(s, w=0.3); sh.text((s[0] + s[2]) / 2, (s[1] + s[3]) / 2, f"SP{i + 1}", 5.6, "c")
        z = m["zufahrt"]; sh.line(z[0] + 1, z[1] + 1.5, z[0] + 1, z[1] - 0.2, 0.6, col=DIMC); sh.line(z[2] - 1, z[3] - 0.2, z[2] - 1, z[3] + 1.5, 0.6, col=DIMC)
        sh.text((z[0] + z[2]) / 2, z[3] + 1.0, "Zufahrt (Lage ANNAHME, y = 30 m)", 6.5, "c", col=DIMC, font=FB)
        ein = m["eingaenge"]
    for i, (nm, r) in enumerate(ein):
        sh.rect(r, w=0.3, fill=(0.95, 0.9, 0.7)); sh.text((r[0] + r[2]) / 2, (r[1] + r[3]) / 2, f"E{i + 1}", 5.5, "c", font=FB, dy=-0.9)
    sh.text(33.0, 28.0, "Eingänge (Lage/Breite ANNAHME):", 6.5, "l", font=FB)
    for i, (nm, r) in enumerate(ein): sh.text(33.0, 27.0 - i * 0.8, f"E{i + 1} {nm}", 5.6, "l")
    for c_ in m["saeulen"]: sh.circle(c_[0], c_[1], RM.SAEULE_D / 2, fill=BLACK, w=0.2)
    # Konflikte rot
    cs = m["saeulen"]
    for c1, c2 in [(p, q) for i, p in enumerate(cs) for q in cs[i + 1:] if math.dist(p, q) < RM.SAEULE_D + 0.3]:
        sh.circle((c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2, 0.6, fill=None, w=0.6, col=RED); sh.text((c1[0] + c2[0]) / 2 - 0.9, (c1[1] + c2[1]) / 2, "K-Säulen", 5.2, "r", col=RED, font=FB)
    for c_ in cs:
        if c_[1] < 0 or c_[0] < 0: sh.circle(c_[0], c_[1], 0.45, fill=None, w=0.6, col=RED)
    b1 = RM.bb(m["levels"]["OG1"]["poly"])
    if b1[1] < 0: sh.line(b1[0], b1[1], b1[2], b1[1], 0.8, col=RED); sh.text((b1[0] + b1[2]) / 2, b1[1] - 0.9, "K: 1. OG ragt über Hypothese-Grenze zum Platz (y < 0)", 6, "c", col=RED, font=FB)
    if m["gruppe"] == "A":
        yb = min(r[1] for r in m["balkone"]); sh.line(4.0, yb, 32.0, yb, 0.8, col=RED); sh.text(18.0, -4.7, "K: Balkone (y −1,50) und Vordach (y −3,60) ragen über die Hypothese-Grenze zum Platz", 6, "c", col=RED, font=FB)
    # Maße
    dim_chain(sh, [0, b[0], b[2], 32] if b[0] > 0 else [0, b[2], 32], "h", -1.0 if m["gruppe"] == "B" else -4.0, 1.5, -1, ext_from=-0.2)
    dim_chain(sh, [0, 18, 23, 29, 30] if m["gruppe"] == "A" else [0, 30], "v", 0.0, 1.5, -1, ext_from=-0.2) if m["gruppe"] == "A" else dim_chain(sh, [0, 30], "v", 0.0, 1.8, -1, ext_from=-0.2)
    sh.text(0, 31.3 if m["gruppe"] == "B" else 31.3, "Stellplatz 2,50 × 5,00 m und Fahrgasse 6,00 m = ANNAHMEN (Quelle: parken.py); Gesamtzahl = Zeichnung, kein Stellplatznachweis", 6, "l", col=ORANGE)

# ---------- Textblätter ----------
def textblatt(sh, m, y_top, cols):
    pass

def text_columns(sh, blocks, x0=20, y0=None, colw=135, size=7.5, lead=3.9, gap=8):
    """blocks: Liste (Überschrift, [Zeilen]) – laufen spaltenweise (mm-Koordinaten des Blatts)."""
    top = y0 or (sh.area[3] - 6); x = x0; y = top; bottom = sh.area[1] + 4
    for head, lines in blocks:
        need = (len(lines) + 1) * lead
        if y - need < bottom and y != top: x += colw + gap; y = top
        sh.c.setFillColorRGB(*BLACK); sh.c.setFont(FB, size + 1.5); sh.c.drawString(x * mm, y * mm, head); y -= lead + 1
        for ln in lines:
            for w in wrap(ln, F, size, colw):
                if y < bottom: x += colw + gap; y = top
                sh.c.setFillColorRGB(*(RED if ln.startswith("[KONFLIKT]") else (ORANGE if ln.startswith("[HINWEIS]") or "ANNAHME" in ln[:40] else BLACK))); sh.c.setFont(F, size); sh.c.drawString(x * mm, y * mm, w); y -= lead
        y -= 3

# ---------- Übersichtsblatt ----------
def uebersicht(sh, m, blattliste):
    area = sh.area; x0 = area[0] + 6; top = area[3] - 6; sh.c.setFillColorRGB(0, 0, 0)
    sh.c.setFont(FB, 14); sh.c.drawString(x0 * mm, top * mm, f"{PROJ} – {m['titel']}"); top -= 7
    sh.c.setFont(F, 8); sh.c.setFillColorRGB(*RED); sh.c.drawString(x0 * mm, top * mm, STEMPEL + "  –  technische Zeichnungen für PDF-Import, keine Präsentation, keine Genehmigungsunterlage"); top -= 8
    blocks = []
    b = RM.bb(m["levels"]["EG"]["poly"]); fl = {k: RM.poly_area(m["levels"][k]["poly"]) for k in m["levels"]}
    blocks.append(("Beschreibung", [m["beschr"], "Datenquelle: " + m["quelle"]]))
    kz = [f"EG-Außenmaß {n2(b[2] - b[0])} × {n2(b[3] - b[1])} m = {n2(fl['EG'], 1)} m²"]
    for k in ("OG1", "ST"):
        bb_ = RM.bb(m["levels"][k]["poly"]); kz.append(f"{lv_title(m, k)}: Umriss {n2(bb_[2] - bb_[0])} × {n2(bb_[3] - bb_[1])} m, Fläche {n2(fl[k], 1)} m²")
    z = m["zfloor"]; kz += [f"Höhen über ±0,00: OK FFB 1. OG {kote(z['OG1'])}; OK FFB oberstes Geschoss {kote(z['ST'])}; OK Dach {kote(m['ztop_st'])}; OK Attika {kote(m['zattika'])} m",
                           "Höhenstatus: " + m["hoehenstatus"], "Decken: " + m["slab_status"], f"Außenwand: Darstellung als Doppellinie 0,30 m = ANNAHME (Wandstärke NOCH OFFEN)", f"Säulen: {len(m['saeulen'])} Stück, Ø {n2(RM.SAEULE_D)} m (Annahme des Entwurfs)" if m["saeulen"] else "Säulen: keine (Referenz B3: Auskragung ohne Stützen)"]
    blocks.append(("Maße und Kennwerte", kz))
    blocks.append(("Maßstab / Bezug", ["Alle Blätter 1:100 auf " + ("A2" if sh.W > 500 else "A3") + " quer. Maßstabsbalken unten: 10,00 m = 100 mm auf dem Blatt. Maße in Metern.", "Grundrisse: x = West→Ost, y = von der Platzseite (unten) zur Rückseite (oben). Nordrichtung NOCH OFFEN.", "Bezugshöhe ±0,00 = OK Fertigfußboden Erdgeschoss; Bezug zur OK Fahrbahn der Stadt NOCH OFFEN."]))
    blocks.append(("Blattverzeichnis", blattliste))
    if m["gruppe"] == "A":
        rl = []
        for k in ("EG", "OG1", "ST"):
            for rm in m["levels"][k]["rooms"]: r = rm["rect"]; rl.append(f"{k} {rm['id']}: {rm['name']} x {n2(r[0])}–{n2(r[2])}, y {n2(r[1])}–{n2(r[3])} [{rm['status']}]")
        blocks.append(("Raumliste (Koordinaten m, Status laut B3-Modell)", rl))
    blocks.append(("Konsistenz (Kurzfassung)", [f"[{s}] {t}" for s, t in RM.pruefe(m) if s == "KONFLIKT"][:8] + ["Vollständiges Protokoll: letztes Blatt."]))
    legend_y = area[1] + 40
    text_columns(sh, blocks, x0=x0, y0=top, colw=125, size=7, lead=3.5)
    # Legende
    ly = area[1] + 36; lx = x0; sh.c.setFillColorRGB(0, 0, 0); sh.c.setFont(FB, 9); sh.c.drawString(lx * mm, (ly + 6) * mm, "Legende (Linienarten)")
    items = [("wall", "Außenwand (Doppellinie, grau gefüllt)"), ("room", "Raumgrenze (dünn, grau)"), ("col", "Säule Ø 0,40 m (voll)"), ("glass", "Fenster/Verglasung (3 Linien in der Wand)"), ("door", "Tür (Linie in der Wandöffnung, ohne Anschlag)"),
             ("dim", "Maßlinie mit Schrägstrich (blau)"), ("dash", "Umriss darunterliegendes Geschoss / überdeckend"), ("dashdot", "Schnittlinie A–A"), ("plot", "Grundstücksgrenze HYPOTHESE (rot gestrichelt)"), ("cut", "Geschnittenes Bauteil (Schnitt, schwarz)")]
    for i, (kd, lb) in enumerate(items):
        legend_sample(sh, lx + (i // 5) * 120, ly - (i % 5) * 5.5, kd, lb)
    # Maßstabsbalken 10 m
    bx = lx; by = area[1] + 2
    sh.mmline(bx, by + 2, bx + 100, by + 2, 0.6)
    for i in range(0, 11): sh.mmline(bx + i * 10, by + 2, bx + i * 10, by + (4 if i % 5 == 0 else 3), 0.4)
    for i in (0, 5, 10): sh.c.setFont(F, 6.5); sh.c.setFillColorRGB(0, 0, 0); sh.c.drawCentredString((bx + i * 10) * mm, (by - 1.5) * mm, f"{i} m")
    sh.c.setFont(F, 6.5); sh.c.drawString((bx + 106) * mm, (by + 1.2) * mm, "Maßstabsbalken 1:100 (10 m = 100 mm Blattmaß)")

# ---------- Rechtsebenen & Konsistenz ----------
def rechtsblatt(sh, m):
    blocks = [("Rechtsebenen und Datenstände – getrennt zu lesen (keine Aussage zur Zulässigkeit)", [
        "EBENE 1 – Alter B3-Geometriestand (Modell v4, Planstand Blatt 14): " + ("in DIESEM PDF verwendet, unverändert aus geometry/variant_B3.json." if m["gruppe"] == "A" else "in diesem PDF NICHT verwendet; nur als Vergleich im Paket A."),
        "EBENE 2 – Neue Entwurfsannahmen (Planungsziel 24.10.2026: EG 18 × 30 m = 540 m², Vorbau, Säulen, Zielhöhe 12,00 m nicht bindend): " + ("in diesem PDF nicht verwendet." if m["gruppe"] == "A" else "in DIESEM PDF verwendet (varianten_f.py); alle Werte sind Entwurfsannahmen."),
        "EBENE 3 – B-Plan Nr. 123 (14.04.2023, rechtskräftig, wahrscheinlich MI 3 / Flurstück 59/1): MI 3 – II bis III Vollgeschosse, GRZ 0,6, Traufhöhe 9,80 m, Gebäudehöhe 15,00 m, Sockel 0,30 m; Hauptdach ≥ 38° (Flachdach nur untergeordnet); Höhenbezug OK Fahrbahn. Zuordnung Baufeld 3 = MI 3 ist NICHT bestätigt.",
        "EBENE 4 – Änderungsentwurf 2026 (kein Beschluss, nicht rechtskräftig): II Vollgeschosse zwingend, Traufhöhe 6,50 m, Gebäudehöhe 12,00 m; erfasst MI 3 nach vorliegendem Stand nicht.",
        "EBENE 5 – Offener Höhenbezug: ±0,00 = OK Fertigfußboden EG ist eine Zeichnungsannahme; Anbindung an OK Fahrbahn und Gelände NOCH OFFEN. Geschosshöhen dieses PDFs: " + m["hoehenstatus"] + ".",
        "Die Zeichnungen enthalten KEINE Aussage, ob eine Variante baurechtlich zulässig ist; kein Geschossvergleich mit den Ebenen 3 und 4 wurde als Ergebnis eingetragen."]),
              ("Nicht gesichert / NOCH OFFEN in diesem PDF", ["• " + o for o in m["offen"]])]
    text_columns(sh, blocks, x0=sh.area[0] + 6, colw=150, size=7.5, lead=3.9)

def konsistenzblatt(sh, m):
    fs = RM.pruefe(m); blocks = [("Konsistenzprotokoll (automatisch aus dem gemeinsamen Modell; Widersprüche sind dokumentiert, NICHT stillschweigend korrigiert)", [f"[{s}] {t}" for s, t in fs]),
                                 ("Ableitung", ["Alle Grundrisse, Ansichten, der Schnitt und der Lageplan dieses PDFs werden aus demselben Modell-Dict gezeichnet (Umrisse, Höhen, Säulen, Öffnungen, Stellplätze). Abweichungen zwischen Blättern sind dadurch ausgeschlossen; die Widersprüche liegen in den Eingangsdaten."])]
    text_columns(sh, blocks, x0=sh.area[0] + 6, colw=150, size=7.2, lead=3.7)

# ---------- Paket ----------
def paket(m, pfad):
    c = canvas.Canvas(pfad, pagesize=landscape(A2)); size = (594, 420)
    c.setTitle(f"{PROJ} – {m['titel']} (Revitalyze-Import, Vektor)"); c.setAuthor("Entwurfsstudie – vorläufig"); c.setSubject(STEMPEL)
    kt = lambda k: f"Grundriss {lv_title(m, k)} – OK Fertigfußboden {kote(m['zfloor'][k])} m (Höhenbezug ANNAHME)"
    blaetter = [("Übersicht", "Übersichtsblatt"), ("EG", kt("EG")), ("OG1", kt("OG1")), ("ST", kt("ST")), ("front", "Vorderansicht"), ("rear", "Rückansicht"), ("west", "Westansicht"), ("east", "Ostansicht"),
                ("schnitt", "Schnitt A–A mit Höhenkoten"), ("park", "Stellplätze / Erschließung (getrennt)"), ("recht", "Rechtsebenen und offene Punkte"), ("kons", "Konsistenzprotokoll")]
    N = len(blaetter); liste = [f"Blatt {i + 1}: {b[1]}" for i, b in enumerate(blaetter)] + ["Blätter 1–10 sind Zeichnungen (Vektor); Blätter 11–12 sind reine Textblätter (für den Import-Test entbehrlich)."]
    anm_plan = ["Wandstärke 0,30 m = ANNAHME (Darstellung).", "Innentüren und Türanschläge NOCH OFFEN – nicht gezeichnet.", "Maße in m. Maßketten blau, Bauteilkanten schwarz."]
    for i, (key, titel) in enumerate(blaetter):
        sh = Sheet(c, size, "right", titel, titel, i + 1, N, m, anm_plan if key in ("EG", "OG1", "ST") else ["Maße in m.", "Höhen: " + m["hoehenstatus"]] + (["Fassadenöffnungen von B1–B3: keine Daten – nicht gezeichnet."] if m["gruppe"] == "B" and key in ("front", "rear", "west", "east", "schnitt") else []))
        if key == "Übersicht": uebersicht(sh, m, liste)
        elif key in ("EG", "OG1", "ST"):
            pb = plan_bbox(m, key, False); eb = RM.bb(m['levels'][key]['poly']); sh.fit((pb[0] - 3.4, pb[1] - 4.5, pb[2] + 3.4, max(pb[3], eb[3] + 2.6))); plan(sh, m, key)
        elif key in SIDES:
            a, b = elev_bbox(m, SIDES[key][1]); sh.fit((a - 2.5, -4.5, b + 13.5, m["zattika"] + 2.6)); elevation(sh, m, key)
        elif key == "schnitt":
            cuts_all = [cut_intervals(m["levels"][k]["poly"], m["schnitt_x"]) for k in m["levels"]]; a = min(c_[0] for cc in cuts_all for c_ in cc); b = max(c_[1] for cc in cuts_all for c_ in cc)
            sh.fit((a - 2.5, -5.0, b + 13.5, m["zattika"] + 2.6)); section(sh, m)
        elif key == "park":
            sh.fit((-3.0, -6.8 if m["gruppe"] == "A" else -4.5, 35.0, 32.4)); erschliessung(sh, m)
        elif key == "recht": rechtsblatt(sh, m)
        elif key == "kons": konsistenzblatt(sh, m)
        c.showPage()
    c.save()

def testpaket(m, pfad):
    c = canvas.Canvas(pfad, pagesize=landscape(A3)); size = (420, 297); c.setTitle(f"{PROJ} – Testblatt EG (Revitalyze-Import, Vektor)"); c.setSubject(STEMPEL)
    anm = ["Reduziertes Testblatt: ein Grundriss, kein Plot, keine Stellplätze, keine Säulen.", "Wandstärke 0,30 m = ANNAHME.", "Innentüren/Anschläge NOCH OFFEN.", "Quelle: B3-Modell v4 (Variante A)."]
    sh = Sheet(c, size, "bottom", "Testblatt – Grundriss Erdgeschoss (nur EG) – OK Fertigfußboden ±0,00 m (Höhenbezug ANNAHME)", "Testblatt", 1, 1, m, anm)
    bx = RM.bb(m["levels"]["EG"]["poly"]); sh.fit((bx[0] - 2.4, bx[1] - 2.4, bx[2] + 2.4, bx[3] + 3.4)); plan(sh, m, "EG", test=True)
    sh.mmline(sh.area[0] + 4, sh.area[1] + 1, sh.area[0] + 104, sh.area[1] + 1, 0.6)
    for i in (0, 5, 10): sh.mmline(sh.area[0] + 4 + i * 10, sh.area[1] + 1, sh.area[0] + 4 + i * 10, sh.area[1] + 3.5, 0.4); sh.c.setFont(F, 6); sh.c.setFillColorRGB(0, 0, 0); sh.c.drawCentredString((sh.area[0] + 4 + i * 10) * mm, (sh.area[1] - 2) * mm, f"{i} m")
    sh.c.setFont(F, 6); sh.c.drawString((sh.area[0] + 108) * mm, (sh.area[1] + 0.5) * mm, "Maßstabsbalken 1:100 (10 m = 100 mm)")
    c.showPage(); c.save()

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); ms = RM.alle()
    for m in ms:
        paket(m, os.path.join(OUT, m["dat"])); print("geschrieben", m["dat"])
    testpaket(ms[0], os.path.join(OUT, "Test_EG_Vektor_Import.pdf")); print("geschrieben Test_EG_Vektor_Import.pdf")
