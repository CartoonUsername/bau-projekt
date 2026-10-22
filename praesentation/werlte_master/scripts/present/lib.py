"""Zeichnungsbibliothek für die Präsentationsblätter (A3 quer, Einheit mm). Alle Texte werden als echte Vektortexte gesetzt."""
import json, os, html
from PIL import ImageFont
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
D = json.load(open(os.path.join(ROOT, "geometry", "building_design.json"), encoding="utf-8"))
FONTS = "/usr/share/fonts/opentype/inter/"
_R = ImageFont.truetype(FONTS + "Inter-Regular.otf", 200)
_B = ImageFont.truetype(FONTS + "Inter-SemiBold.otf", 200)
INK = "#1B1F24"; GREY = "#6B7280"; LGREY = "#C9CED6"; PALE = "#E5E8EC"; ACC = "#9A3412"; ACCBG = "#FDF1E7"
FILL = {"apartment": "#F2E4DC", "office": "#DDE7EE", "core": "#E7E9EC", "corridor": "#F8F8F6", "dining": "#F5EEDC", "lounge": "#EBDDC3", "bar": "#D9D2C6",
        "private_dining": "#E8DCC8", "circulation": "#EFEFEC", "wc": "#E3E7EA", "storage": "#E3E7EA", "kitchen": "#DADFE3"}
W, H = 420.0, 297.0

def tw(s, fs, bold=False):
    return (_B if bold else _R).getlength(s) / 200 * fs
def de(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")
def esc(s):
    return html.escape(s, quote=False)

class Sheet:
    def __init__(self):
        self.e = []
        self.defs = []
        self.boxes = []
    def add(self, s):
        self.e.append(s)
    def line(self, x1, y1, x2, y2, w=0.25, c=INK, dash=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{c}" stroke-width="{w}"{d} stroke-linecap="{cap}"/>')
    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=0.25, dash=None, rx=0, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        r = f' rx="{rx}"' if rx else ""
        self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}"{o} stroke="{stroke if stroke else "none"}" stroke-width="{sw}"{d}{r}/>')
    def circle(self, x, y, r, fill="none", stroke=INK, sw=0.25):
        self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def poly(self, pts, fill="none", stroke=INK, sw=0.25, close=True, dash=None):
        p = " ".join(f"{x:.3f},{y:.3f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<{"polygon" if close else "polyline"} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linejoin="round"/>')
    def text(self, x, y, s, fs=2.8, anchor="start", weight=400, fill=INK, rot=None, italic=False, halo=False):
        w_ = tw(s, fs, weight >= 600)
        if rot: bx = (x - fs * 0.8, y - w_ / 2, x + fs * 0.22, y + w_ / 2)
        else:
            x0_ = x - w_ / 2 if anchor == "middle" else (x - w_ if anchor == "end" else x)
            bx = (x0_, y - fs * 0.8, x0_ + w_, y + fs * 0.22)
        self.boxes.append((bx, s))
        t = f' transform="rotate({rot} {x:.3f} {y:.3f})"' if rot else ""
        st = ' font-style="italic"' if italic else ""
        if halo: st += ' stroke="#FFFFFF" stroke-width="0.9" paint-order="stroke" stroke-linejoin="round"'
        self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{fs}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{t}{st}>{esc(s)}</text>')
    def wrap(self, x, y, s, width, fs=2.8, lh=1.4, weight=400, fill=INK, anchor="start"):
        """Zeilenumbruch nach gemessener Textbreite; gibt die y-Koordinate unter dem letzten Text zurück."""
        words, line = s.split(), ""
        out = []
        for w in words:
            t = (line + " " + w).strip()
            if tw(t, fs, weight >= 600) <= width or not line: line = t
            else: out.append(line); line = w
        out.append(line)
        for l in out:
            assert tw(l, fs, weight >= 600) <= width + 0.01, f"Zeile zu breit: {l}"
            self.text(x, y, l, fs, anchor, weight, fill); y += fs * lh
        return y
    def check(self):
        """Prüft: kein Text außerhalb des Blattrahmens und keine Textüberlagerungen. Gibt Fehlerliste zurück."""
        err = []
        for (a, t) in self.boxes:
            if a[0] < 6.5 or a[2] > W - 6.5 or a[1] < 6.5 or a[3] > H - 6.5: err.append(f"außerhalb des Blatts: {t}")
        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                a, ta = self.boxes[i]; b, tb = self.boxes[j]
                if a[0] < b[2] - 0.15 and b[0] < a[2] - 0.15 and a[1] < b[3] - 0.15 and b[1] < a[3] - 0.15: err.append(f"Überlagerung: '{ta}' / '{tb}'")
        return err
    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" '
                f'font-family="Inter, \'Helvetica Neue\', Arial, sans-serif" text-rendering="geometricPrecision">'
                '<defs>' + "".join(self.defs) + f'</defs><rect width="{W}" height="{H}" fill="#FFFFFF"/>')
        return head + "\n".join(self.e) + "</svg>"

# ---------- Blattrahmen, Schriftfeld, Informationsbereich ----------
PX0, PX1 = 318.0, 408.0          # Informationsbereich
TB_Y = 236.0                     # Oberkante Schriftfeld
def frame(s, title, scale_txt, kenn, legend, offen, hinweise, sheet_no, status="VORLÄUFIGER ARBEITSSTAND – nicht freigegeben"):
    s.rect(6, 6, W - 12, H - 12, stroke=INK, sw=0.5)
    s.line(PX0 - 3, 6, PX0 - 3, H - 6, 0.25, GREY)
    x, wid, y = PX0, PX1 - PX0, 14.0
    def head(t):
        nonlocal y
        s.text(x, y, t.upper(), 2.6, weight=600, fill=GREY); y += 1.6
        s.line(x, y, x + wid, y, 0.2, LGREY); y += 4.6
    if kenn:
        head("Kennzahlen")
        for k, v in kenn:
            s.text(x, y, k, 2.8); s.text(x + wid, y, v, 2.8, "end", 600); y += 4.4
        y += 3
    if legend:
        head("Legende")
        for sym, t in legend:
            sym(s, x, y - 2.9)
            y = s.wrap(x + 12, y, t, wid - 12, 2.8) + 0.9
        y += 2
    if offen:
        head("Offene Punkte (nicht gelöst)")
        for cid, t in offen:
            s.rect(x, y - 2.6, 9.0, 3.8, ACCBG, ACC, 0.2, rx=0.8); s.text(x + 4.5, y, cid, 2.4, "middle", 600, ACC)
            y = s.wrap(x + 11.5, y, t, wid - 11.5, 2.8) + 1.0
        y += 2
    if hinweise:
        head("Hinweise")
        for t in hinweise: y = s.wrap(x, y, t, wid, 2.7, 1.38, fill=INK) + 1.2
    assert y < TB_Y - 3, f"Informationsbereich läuft in das Schriftfeld: y={y:.1f}"
    # Schriftfeld
    s.line(PX0 - 3, TB_Y, W - 6, TB_Y, 0.5, INK)
    ty = TB_Y + 7
    s.text(x, ty, "Neue Mitte Werlte · Baufeld 3", 3.4, weight=600); ty += 5.2
    s.text(x, ty, "Bauvorhaben: Restaurant und Bar, Büros, Wohnungen", 2.7, fill=GREY); ty += 8.5
    ty = s.wrap(x, ty, title, wid, 4.2, 1.25, 600) + 1.5
    s.text(x, ty, scale_txt, 2.8); ty += 4.2
    s.text(x, ty, "Stand 22.10.2026 · Modell NEUE_MITTE_MASTER_DRAFT_A_003", 2.5, fill=GREY); ty += 5
    s.rect(x, ty - 3.2, wid, 6.2, ACCBG, ACC, 0.3, rx=0.8)
    s.text(x + wid / 2, ty + 1.0, status, 2.6, "middle", 600, ACC)
    s.text(x + wid, H - 9, f"Blatt {sheet_no}", 2.6, "end", 600)
    assert ty + 6 < H - 7, f"Schriftfeld zu lang: {ty:.1f}"

def drawing_title(s, t, sub=None):
    s.text(14, 20, t, 6.0, weight=600)
    if sub: s.text(14, 27, sub, 3.0, fill=GREY)

def scale_bar(s, x, y, scale, length_m=5):
    mm = length_m * 1000 / scale
    for i in range(length_m):
        s.rect(x + i * mm / length_m, y, mm / length_m, 1.6, INK if i % 2 == 0 else "#FFFFFF", INK, 0.2)
    s.text(x, y + 5, "0", 2.5); s.text(x + mm, y + 5, f"{length_m} m", 2.5, "end"); s.text(x + mm + 4, y + 1.4, f"Maßstab 1:{scale}", 2.7)

def dim_h(s, x0, x1, y, label, off=0.0, fs=2.6):
    """horizontale Maßlinie mit Schrägstrichen; y = Lage der Maßlinie"""
    s.line(x0, y, x1, y, 0.2, INK)
    for x in (x0, x1): s.line(x - 0.9, y + 0.9, x + 0.9, y - 0.9, 0.3, INK)
    s.text((x0 + x1) / 2, y - 1.1, label, fs, "middle", halo=True)
def dim_v(s, x, y0, y1, label, fs=2.6):
    s.line(x, y0, x, y1, 0.2, INK)
    for y in (y0, y1): s.line(x - 0.9, y + 0.9, x + 0.9, y - 0.9, 0.3, INK)
    s.text(x - 1.1, (y0 + y1) / 2, label, fs, "middle", rot=-90, halo=True)
def bubble(s, x, y, t, r=3.0):
    s.circle(x, y, r, "#FFFFFF", INK, 0.3); s.text(x, y + 1.0, t, 2.7, "middle", 600)
def flag(s, x, y, cid):
    s.rect(x, y - 2.5, 9.0, 3.8, ACCBG, ACC, 0.25, rx=0.8); s.text(x + 4.5, y, cid, 2.4, "middle", 600, ACC)
