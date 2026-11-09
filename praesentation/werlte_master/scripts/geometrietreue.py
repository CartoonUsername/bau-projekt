"""Misst, wie genau ein veredeltes (Higgsfield-) Bild die Kanten des zugehörigen Blender-Renderings behält.
Kanten (Sobel, 90. Perzentil der Gradienten) beider Bilder; Anteil der Kanten des Blender-Bilds, zu denen das veredelte Bild innerhalb r Pixeln (Standard 6 px bei 2400 px Breite = ca. 0,10 m an der Fassade) eine Kante hat, und umgekehrt."""
import sys, numpy as np
from PIL import Image, ImageFilter
def edges(img, size=(2400, 1350)):
    g = np.asarray(img.convert("L").resize(size, Image.LANCZOS)).astype(float)
    gx = np.zeros_like(g); gy = np.zeros_like(g); gx[:, 1:-1] = g[:, 2:] - g[:, :-2]; gy[1:-1] = g[2:] - g[:-2]; m = np.hypot(gx, gy)
    return m > np.percentile(m, 90)
def dilate(e, r):
    im = Image.fromarray((e * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * r + 1)); return np.asarray(im) > 0
def score(a, b, r=6):
    ea, eb = edges(Image.open(a)), edges(Image.open(b)); return (dilate(eb, r)[ea]).mean(), (dilate(ea, r)[eb]).mean()
if __name__ == "__main__":
    s1, s2 = score(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6); print("Blender-Kanten im veredelten Bild wiedergefunden: %.1f %%; veredelte Kanten im Blender-Bild: %.1f %%" % (s1 * 100, s2 * 100))
