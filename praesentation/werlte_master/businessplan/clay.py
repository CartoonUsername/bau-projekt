"""Einfaches Tonmodell (Isometrie) einer Variante aus scripts/studie/varianten.V – dient als Geometrie-Referenz für die KI-Visualisierung (kein Entwurfsbild)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "studie"))
import varianten as VA
from PIL import Image, ImageDraw
def render(key, path, view="east", size=(2000, 1125)):
    v = VA.V[key]; Z = v["Z"]; W, H = size; c, s = math.cos(math.radians(30)), math.sin(math.radians(30)); sc = 19.0
    mir = (lambda x, y: (32 - x, y)) if view == "east" else (lambda x, y: (x, y))
    def P(x, y, z):
        x_, y_ = mir(x, y); return (W / 2 + (x_ - y_) * c * sc - 40, H * 0.88 - ((x_ + y_) * s * sc) - z * sc * 1.0 + 0)
    im = Image.new("RGB", size); d = ImageDraw.Draw(im)
    for yy in range(H): t = yy / H; d.line([(0, yy), (W, yy)], fill=(int(190 - 40 * t), int(205 - 30 * t), int(225 - 15 * t)))
    def poly(pts, col): d.polygon([P(*p) for p in pts], fill=col, outline=(70, 70, 76))
    def flat(r, z, col): poly([(r[0], r[1], z), (r[2], r[1], z), (r[2], r[3], z), (r[0], r[3], z)], col)
    def box(r, z0, z1, top=(214, 210, 204), fr=(176, 168, 160), sd=(140, 133, 126)):
        x0, y0, x1, y1 = r
        order = []
        # sichtbare Flächen: Ostseite (x=x1) und Platzseite (y=y0) bei view=east, sonst Westseite (x0) und Platzseite
        if view == "east": poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], sd)
        else: poly([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], sd)
        poly([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], fr); poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top)
    flat((-6, -6, 38, 36), 0, (150, 140, 134)); flat((0, 0, 32, 30), 0.02, (166, 158, 150))
    a = v["asphalt"]; flat(a, 0.04, (120, 122, 128))
    for st in v["stalls"]: flat(st, 0.06, (150, 152, 158)); d.line([P(st[0], st[1], .06), P(st[2], st[1], .06)], fill=(240, 240, 240), width=2); d.line([P(st[0], st[3], .06), P(st[2], st[3], .06)], fill=(240, 240, 240), width=2)
    pieces = []
    eg = v["eg"][0]; og = v["og1"][0]; st_ = v["st"][0]
    cols = v["saeulen_pts"]
    items = [("col", (c_[0] - .2, c_[1] - .2, c_[0] + .2, c_[1] + .2), 0, Z["OG1"][0] - .45) for c_ in cols] + [("eg", eg, 0, Z["OG1"][0] - .45), ("og", og, Z["OG1"][0] - .45, Z["ST"][0]), ("st", st_, Z["ST"][0], Z["ATT"][1])]
    def key_(it): r = it[1]; x_, y_ = mir((r[0] + r[2]) / 2, (r[1] + r[3]) / 2); return -(x_ + y_) - (it[2] + it[3]) * 0.0
    for it in sorted(items, key=lambda it: (it[0] in ("og", "st"), it[0] == "st", key_(it))):
        kind, r, z0, z1 = it
        if kind == "col": box(r, z0, z1, top=(235, 235, 235), fr=(222, 222, 222), sd=(190, 190, 190))
        elif kind == "eg": box(r, z0, z1, top=(226, 214, 190), fr=(120, 160, 190), sd=(96, 130, 156))
        elif kind == "og": box(r, z0, z1, top=(214, 210, 204), fr=(150, 100, 88), sd=(120, 78, 68))
        else: box(r, z0, z1, top=(224, 218, 208), fr=(196, 160, 110), sd=(170, 136, 92))
    im.save(path); return path
if __name__ == "__main__":
    for k in sys.argv[1:] or ["R1", "R2", "R3"]:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder", "ref"); os.makedirs(out, exist_ok=True); print(render(k, os.path.join(out, f"clay_{k}.png")))
