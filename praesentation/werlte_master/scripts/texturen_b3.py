"""Prozedurale, kachelbare Materialtexturen (numpy/PIL) für das Modell Baufeld 3. Maße der Kachel in Metern stehen im Dateinamen-Dictionary TILE.
Klinker: Läuferverband, Stein 240 x 62,5 mm, Fuge 12 mm (Kachel 1,008 x 0,9 m = 4 Steine x 12 Schichten). Holz: vertikale Lärchenbretter 120 mm mit Fuge. Beton, Pflaster, Asphalt: Rauschen."""
import numpy as np, os
from PIL import Image
TILE = {"klinker": (1.008, 0.9), "holz": (0.6, 1.0), "beton": (2.0, 2.0), "pflaster": (2.0, 2.0), "asphalt": (3.0, 3.0), "mikrozement": (3.0, 3.0), "eiche": (1.0, 1.0)}
rng = np.random.default_rng(7)
def noise(h, w, scales, amps):
    out = np.zeros((h, w))
    for s, a in zip(scales, amps):
        g = rng.random((max(2, h // s), max(2, w // s))); im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC); out += a * (np.asarray(im) / 255.0 - 0.5)
    return out
def save(name, arr, outdir):
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8)).save(os.path.join(outdir, name + ".png"))
def make(outdir):
    os.makedirs(outdir, exist_ok=True)
    # Klinker: 1000 px/m
    ppm = 1000; W, H = 1008, 900; img = np.zeros((H, W, 3)); mortar = np.array([0.50, 0.47, 0.43]); img[:] = mortar
    cols = [np.array(c) for c in ((0.27, 0.10, 0.075), (0.32, 0.12, 0.09), (0.22, 0.085, 0.07), (0.36, 0.15, 0.11), (0.19, 0.08, 0.07), (0.30, 0.13, 0.10))]
    for r in range(12):
        y0 = int(r * 75 + 6); y1 = y0 + 63; off = 126 if r % 2 else 0
        for k in range(-1, 5):
            x0 = int(k * 252 + off + 6); x1 = x0 + 240; c = cols[rng.integers(len(cols))] * (0.9 + 0.2 * rng.random())
            xa, xb = max(0, x0), min(W, x1)
            if xb > xa: img[y0:y1, xa:xb] = c
            if x1 > W: img[y0:y1, 0:x1 - W] = c            # Kachelrand
    img += noise(H, W, (3, 9), (0.06, 0.04))[..., None] * np.array([1, 0.6, 0.5]); save("klinker", img, outdir)
    # Holz: 600 px / 0.6 m, Bretter 120 mm
    W, H = 600, 1000; img = np.zeros((H, W, 3)); base = np.array([0.40, 0.24, 0.12])
    for b in range(5):
        x0, x1 = b * 120 + 2, b * 120 + 118; tone = 0.85 + 0.3 * rng.random(); grain = noise(H, x1 - x0, (400, 60, 12), (0.10, 0.12, 0.08))
        for ch in range(3): img[:, x0:x1, ch] = base[ch] * tone * (1 + grain * 1.2)
        img[:, b * 120:b * 120 + 2] = base * 0.35; img[:, b * 120 + 118:b * 120 + 120] = base * 0.35
    save("holz", img, outdir)
    # Beton: 2 m Kachel, 512 px
    n = noise(512, 512, (4, 16, 64), (0.10, 0.08, 0.06)); img = np.stack([0.58 + n, 0.58 + n, 0.56 + n], -1); save("beton", img, outdir)
    # Pflaster: Läuferverband 200 x 100 mm, 2 m Kachel -> 10 Steine x 20 Reihen, 512 px
    H = W = 1024; img = np.full((H, W, 3), 0.30); step = 51; warm = np.array([1.06, 1.0, 0.92])
    for r in range(20):
        for k in range(-1, 11):
            x0 = int((k * 102.4 + (51 if r % 2 else 0))); y0 = int(r * 51.2); tone = (0.50 + 0.12 * rng.random()) ; xa, xb = max(0, x0 + 2), min(W, x0 + 100)
            if xb > xa: img[y0 + 2:y0 + 49, xa:xb] = tone * warm
    img += noise(H, W, (2, 8), (0.05, 0.04))[..., None]; save("pflaster", img, outdir)
    n = noise(512, 512, (2, 8, 32), (0.10, 0.08, 0.05)); img = np.stack([0.17 + n * 0.8] * 3, -1); save("asphalt", img, outdir)
    n = noise(512, 512, (4, 24, 96), (0.08, 0.10, 0.06)); img = np.stack([0.40 + n, 0.39 + n, 0.38 + n], -1); save("mikrozement", img, outdir)
    W = H = 512; img = np.zeros((H, W, 3)); gr = noise(H, W, (200, 30, 6), (0.12, 0.1, 0.05)); base = np.array([0.55, 0.40, 0.25])
    for ch in range(3): img[..., ch] = base[ch] * (1 + gr * 1.4)
    save("eiche", img, outdir)
if __name__ == "__main__":
    make(os.path.join(os.path.dirname(__file__), "..", "visualisierungen", "higgsfield", "modelle", "texturen"))
