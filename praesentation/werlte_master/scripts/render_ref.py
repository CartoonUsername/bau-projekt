"""Geometrie-Referenzbilder (Tonmodell) für die Higgsfield-Visualisierungen, direkt aus geometry/variant_B3.json (Alternative K).
Z-Buffer-Rasterizer, keine Materialien, nur Proportionen, Öffnungen und Rücksprünge. x West->Ost, y Platzfassade->Rückseite, z nach oben (Meter)."""
import json, os, sys, numpy as np
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = json.load(open(os.path.join(ROOT, "geometry", "variant_B3.json"))); V = D["variants"]["K"]; FURN = D["furnishing"]["normal"]
KLK, LAR, CON, GLS, DRK, WOOD, ASP, PAV, ATT, MIL = (0.36, 0.20, 0.17), (0.71, 0.55, 0.36), (0.74, 0.74, 0.73), (0.55, 0.72, 0.80), (0.10, 0.11, 0.13), (0.62, 0.48, 0.32), (0.28, 0.28, 0.29), (0.66, 0.65, 0.62), (0.55, 0.56, 0.58), (0.86, 0.91, 0.93)
class Scene:
    def __init__(self): self.f = []
    def quad(self, p, col, bias=0.0): self.f.append((np.array(p, float), col, bias))
    def box(self, x0, x1, y0, y1, z0, z1, col, top=None, skip=()):
        c = lambda x, y, z: (x, y, z)
        faces = {"-y": [c(x0, y0, z0), c(x1, y0, z0), c(x1, y0, z1), c(x0, y0, z1)], "+y": [c(x1, y1, z0), c(x0, y1, z0), c(x0, y1, z1), c(x1, y1, z1)], "-x": [c(x0, y1, z0), c(x0, y0, z0), c(x0, y0, z1), c(x0, y1, z1)],
                 "+x": [c(x1, y0, z0), c(x1, y1, z0), c(x1, y1, z1), c(x1, y0, z1)], "+z": [c(x0, y0, z1), c(x1, y0, z1), c(x1, y1, z1), c(x0, y1, z1)], "-z": [c(x0, y1, z0), c(x1, y1, z0), c(x1, y0, z0), c(x0, y0, z0)]}
        for k, q in faces.items():
            if k in skip: continue
            self.quad(q, top if (k == "+z" and top) else col)
    def face(self, side, a0, a1, z0, z1, pos, col, bias=0.03):
        """Flächenstück auf einer Fassade: side '-y','+y','-x','+x'; a = Koordinate entlang der Fassade, pos = feste Koordinate"""
        if side == "-y": q = [(a0, pos, z0), (a1, pos, z0), (a1, pos, z1), (a0, pos, z1)]
        if side == "+y": q = [(a1, pos, z0), (a0, pos, z0), (a0, pos, z1), (a1, pos, z1)]
        if side == "-x": q = [(pos, a1, z0), (pos, a0, z0), (pos, a0, z1), (pos, a1, z1)]
        if side == "+x": q = [(pos, a0, z0), (pos, a1, z0), (pos, a1, z1), (pos, a0, z1)]
        self.quad(q, col, bias)
def building(S):
    v = V; Y1 = v["depth_L1"]; y2 = v["y2"]
    # Gelände und Platz (Pflaster) – neutrale Flächen, keine Nachbarbebauung
    S.quad([(-60, -60, 0), (100, -60, 0), (100, 0, 0), (-60, 0, 0)], PAV); S.quad([(-60, 0, 0), (-0.001, 0, 0), (-0.001, 60, 0), (-60, 60, 0)], PAV); S.quad([(32, 0, 0), (100, 0, 0), (100, 60, 0), (32, 60, 0)], PAV)
    S.quad([(0, 18, 0), (32, 18, 0), (32, 60, 0), (0, 60, 0)], ASP)
    # Baukörper
    S.box(0, 32, 0, 18, 0, 3.5, KLK); S.box(0, 32, 0, 18, 3.5, 6.5, KLK); S.box(4, 32, 18, Y1, 3.5, 6.5, KLK)
    S.box(0.8, 31.2, 0.8, 17.2, 6.5, 9.6, LAR); S.box(4.2, 31.2, 17.2, y2, 6.5, 9.6, LAR)
    for (x0, x1, y0, y1, z) in ((0, 32, 0, 18, 3.2), (4, 32, 18, Y1, 3.2), (0, 32, 0, 18, 6.2), (4, 32, 18, Y1, 6.2)): S.box(x0 - 0.04, x1 + 0.04, y0 - 0.04, y1 + 0.04, z, z + 0.3, CON, skip=("-z",))
    S.box(0.76, 31.24, 0.76, 17.24, 9.6, 9.9, ATT); S.box(4.16, 31.24, 17.2, y2 + 0.04, 9.6, 9.9, ATT)
    S.quad([(0.8, 0.8, 9.9), (31.2, 0.8, 9.9), (31.2, y2, 9.9), (0.8, y2, 9.9)], (0.45, 0.45, 0.47))
    S.quad([(4, y2, 6.52), (32, y2, 6.52), (32, Y1, 6.52), (4, Y1, 6.52)], WOOD)                      # Dachterrasse
    for x0, x1 in ((4.2, 13.2), (13.2, 22.2), (22.2, 31.2)): pass
    # Brüstungen Dachterrasse (Milchglas 1,10 m)
    S.box(4, 32, Y1 - 0.06, Y1, 6.5, 7.6, MIL); S.box(31.94, 32, y2, Y1, 6.5, 7.6, MIL); S.box(4, 4.06, y2, Y1, 6.5, 7.6, MIL)
    # Platzseite: Glasfront EG, Türen, Fenster, Balkone, Vordach
    S.face("-y", 4, 32, 0, 3.1, -0.02, GLS); 
    for a, b in ((17, 19), (29.5, 31)): S.face("-y", a, b, 0, 2.4, -0.04, (0.85, 0.88, 0.9), 0.05)
    S.face("-y", 1.0, 2.5, 0, 2.4, -0.02, GLS)
    for x in np.arange(5.4, 32, 1.4): S.face("-y", x - 0.03, x + 0.03, 0, 3.1, -0.04, DRK, 0.05)
    S.face("-y", 4, 32, 3.1, 3.2, -0.04, DRK, 0.05)
    for b in v["balconies"]:
        x0, _, x1, _ = b["rect"]; S.box(x0, x1, -1.5, 0, 3.2, 3.5, CON); S.box(x0, x1, -1.5, -1.44, 3.5, 4.6, MIL); S.box(x0, x0 + 0.06, -1.5, 0, 3.5, 4.6, MIL); S.box(x1 - 0.06, x1, -1.5, 0, 3.5, 4.6, MIL)
    for i in range(5): x0 = 4 + 5.6 * i; S.face("-y", x0 + 0.9, x0 + 4.7, 3.9, 6.1, -0.02, DRK)
    for r in v["rooms"]:
        if r["id"].startswith("WE-L2-V"): x0, x1 = r["rect"][0], r["rect"][2]; S.face("-y", x0 + 1.0, x1 - 1.0, 6.9, 9.0, 0.78, (0.84, 0.74, 0.55))
    S.box(6, 30, -3.6, 0, 3.0, 3.1, DRK); S.quad([(6, -3.6, 0.12), (30, -3.6, 0.12), (30, 0, 0.12), (6, 0, 0.12)], WOOD)
    # Rückseite
    for r in v["rooms"]:
        if r["id"].startswith("WE-L1-H"): x0 = r["rect"][0]; S.face("+y", x0 + 1.6, x0 + 5.4, 3.9, 6.1, Y1 + 0.02, DRK)
        if r["id"].startswith("WE-L2-H"): x0 = r["rect"][0]; S.face("+y", x0 + 1.6, x0 + 7.4, 6.6, 9.1, y2 + 0.02, (0.84, 0.74, 0.55))
    for a, b in ((5.0, 6.5), (15.0, 16.5), (1.0, 2.5)): S.face("+y", a, b, 0, 2.4, 18.02, DRK)
    # Seiten
    S.face("-x", 6.5, 7.5, 0.9, 3.0, -0.02, DRK); S.face("-x", 6.5, 7.5, 3.9, 6.1, -0.02, DRK); S.face("-x", 6.5, 7.5, 6.9, 9.1, 0.78, (0.84, 0.74, 0.55))
    S.face("+x", 11.5, 13.5, 4.4, 6.0, 32.02, DRK); S.face("+x", 11.5, 13.5, 7.4, 9.0, 31.22, (0.84, 0.74, 0.55)); S.face("+x", 16.7, 17.9, 0, 2.4, 32.02, DRK)
    # überdachte Stellplätze (hypothetische Fläche, 11 Plätze 2,5 x 5,0 m)
    for st in v["parking"]["stalls"]:
        x0, y0, x1, y1 = st; S.quad([(x0, y0, 0.01), (x0 + 0.08, y0, 0.01), (x0 + 0.08, y1, 0.01), (x0, y1, 0.01)], (0.85, 0.85, 0.85)); S.quad([(x1 - 0.08, y0, 0.01), (x1, y0, 0.01), (x1, y1, 0.01), (x1 - 0.08, y1, 0.01)], (0.85, 0.85, 0.85))
class Cam:
    def __init__(self, pos, target, fov=50, w=1920, h=1280):
        self.p = np.array(pos, float); f = np.array(target, float) - self.p; f /= np.linalg.norm(f); up = np.array([0, 0, 1.0]); r = -np.cross(f, up); r /= np.linalg.norm(r); u = up - np.dot(up, f) * f; u /= np.linalg.norm(u)   # x gespiegelt: Planlage (Platz oben, y nach unten) wie eine Karte gelesen
        self.R = np.stack([r, u, f]); self.w, self.h = w, h; self.fl = (w / 2) / np.tan(np.radians(fov) / 2)
    def proj(self, P):
        q = (P - self.p) @ self.R.T; z = q[:, 2]; return np.stack([self.w / 2 + self.fl * q[:, 0] / z, self.h / 2 - self.fl * q[:, 1] / z], 1), z
def render(S, cam, sky=((0.62, 0.78, 0.93), (0.92, 0.95, 0.98)), light=(-0.4, -0.6, 0.7), ss=2):
    w, h = cam.w * ss, cam.h * ss; img = np.zeros((h, w, 3)); zb = np.full((h, w), 1e9)
    t = np.linspace(0, 1, h)[:, None, None]; img[:] = np.array(sky[0]) * (1 - t) + np.array(sky[1]) * t
    L = np.array(light, float); L /= np.linalg.norm(L)
    fh = np.array([-cam.R[2][0] * 0 + cam.R[2][0], cam.R[2][1], 0.0]); fh /= np.linalg.norm(fh); far = cam.p + fh * 5000.0; far[2] = 0.0
    hp, _ = cam.proj(far[None, :]); hy = int(np.clip(hp[0][1] * ss, 0, h))
    gr = np.linspace(0, 1, max(1, h - hy))[:, None, None]; img[hy:] = np.array((0.70, 0.70, 0.68)) * (1 - gr * 0.25) + np.array((0.60, 0.60, 0.58)) * gr * 0.25
    for P, col, bias in S.f:
        n = np.cross(P[1] - P[0], P[2] - P[0]); ln = np.linalg.norm(n)
        if ln < 1e-9: continue
        n /= ln; c = P.mean(0)
        if getattr(cam, 'cull', True) and np.dot(n, cam.p - c) <= 0: continue
        sh = 0.55 + 0.45 * max(0.0, np.dot(n, L)); colr = np.array(col) * sh
        pts, z = cam.proj(P)
        if (z <= 0.2).any(): continue
        pts = pts * ss
        for tri in ((0, 1, 2), (0, 2, 3)):
            a, b, cc = pts[list(tri)]; za = z[list(tri)]
            x0, x1 = int(max(0, np.floor(min(a[0], b[0], cc[0])))), int(min(w - 1, np.ceil(max(a[0], b[0], cc[0])))); y0, y1 = int(max(0, np.floor(min(a[1], b[1], cc[1])))), int(min(h - 1, np.ceil(max(a[1], b[1], cc[1]))))
            if x1 < x0 or y1 < y0: continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            den = (b[1] - cc[1]) * (a[0] - cc[0]) + (cc[0] - b[0]) * (a[1] - cc[1])
            if abs(den) < 1e-9: continue
            l1 = ((b[1] - cc[1]) * (xs - cc[0]) + (cc[0] - b[0]) * (ys - cc[1])) / den; l2 = ((cc[1] - a[1]) * (xs - cc[0]) + (a[0] - cc[0]) * (ys - cc[1])) / den; l3 = 1 - l1 - l2
            m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
            inv = l1 / za[0] + l2 / za[1] + l3 / za[2]; zz = 1 / np.maximum(inv, 1e-9) - bias
            sub = zb[y0:y1 + 1, x0:x1 + 1]; upd = m & (zz < sub); sub[upd] = zz[upd]; img[y0:y1 + 1, x0:x1 + 1][upd] = colr
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)); return im.resize((cam.w, cam.h), Image.LANCZOS)
VIEWS = {"01_front": ((46, -34, 1.8), (14, 6, 4.8), 52), "02_abend": ((46, -34, 1.8), (14, 6, 4.8), 52), "03_rueck": ((-14, 52, 2.4), (18, 12, 4.8), 54), "04_west": ((-40, -4, 2.2), (4, 10, 4.8), 52), "05_ost": ((72, 24, 2.2), (30, 10, 4.8), 52),
         "06_luft": ((70, 58, 25), (14, 10, 3.0), 50), "07_terrasse": ((17, 41, 19), (17, 19.5, 6.8), 58)}
def interior():
    S = Scene(); x0, x1, y0, y1, h = 4.0, 32.0, 0.0, 10.0, 3.2
    S.quad([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], (0.55, 0.40, 0.27)); S.quad([(x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h)], (0.93, 0.92, 0.88))
    S.quad([(x0, y1, 0), (x1, y1, 0), (x1, y1, h), (x0, y1, h)], (0.42, 0.45, 0.30)); S.quad([(x0, y0, 0), (x0, y1, 0), (x0, y1, h), (x0, y0, h)], (0.42, 0.45, 0.30)); S.quad([(x1, y0, 0), (x1, y1, 0), (x1, y1, h), (x1, y0, h)], (0.42, 0.45, 0.30))
    S.quad([(x0, y0, 0), (x1, y0, 0), (x1, y0, 3.1), (x0, y0, 3.1)], (0.78, 0.88, 0.95)); S.quad([(x0, y0, 3.1), (x1, y0, 3.1), (x1, y0, h), (x0, y0, h)], DRK)
    for x in np.arange(5.4, 32, 1.4): S.quad([(x - 0.03, 0.01, 0), (x + 0.03, 0.01, 0), (x + 0.03, 0.01, 3.1), (x - 0.03, 0.01, 3.1)], DRK)
    for x in (4.0, 11.0, 18.0, 25.0, 31.6): S.box(x, x + 0.4, 0.0, 0.5, 0, 3.1, (0.30, 0.15, 0.12))      # Fensterpfeiler, Klinker (bestehendes Konzept)
    S.box(5, 15, 8.6, 10, 0, 1.1, (0.20, 0.14, 0.10)); S.box(5, 15, 9.6, 10, 1.1, 2.3, (0.25, 0.18, 0.12))
    for sx, sy in FURN["stools"]: S.box(sx - 0.2, sx + 0.2, sy - 0.2, sy + 0.2, 0, 0.75, (0.35, 0.18, 0.14))
    for t in FURN["tables"]:
        S.box(t["x"], t["x"] + 1.2, t["y"], t["y"] + 0.8, 0.72, 0.77, (0.72, 0.58, 0.40)); S.box(t["x"] + 0.55, t["x"] + 0.65, t["y"] + 0.35, t["y"] + 0.45, 0, 0.72, DRK)
        for cx in (t["x"] + 0.15, t["x"] + 0.6):
            S.box(cx, cx + 0.45, t["y"] - 0.45, t["y"], 0, 0.9, (0.45, 0.20, 0.17)); S.box(cx, cx + 0.45, t["y"] + 0.8, t["y"] + 1.25, 0, 0.9, (0.45, 0.20, 0.17))
    return S
if __name__ == "__main__" and "gastro" in sys.argv:
    c = Cam((5.2, 9.3, 1.55), (21, 0.5, 1.2), 74); c.cull = False; render(interior(), c, sky=((0.9, 0.9, 0.88), (0.9, 0.9, 0.88))).save(os.path.join(ROOT, "visualisierungen", "referenzen", "ref_08_gastro.png")); print("ok gastro"); sys.exit()
if __name__ == "__main__":
    outd = os.path.join(ROOT, "visualisierungen", "referenzen"); S = Scene(); building(S)
    for k, (p, t, fov) in VIEWS.items():
        if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
        render(S, Cam(p, t, fov)).save(os.path.join(outd, f"ref_{k}.png")); print("ok", k)
