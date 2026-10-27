"""Legt die Ortho-Ansichten des Modells v4 (plangetreu, Maßstab 1:250) 50 % über die Ansichten von Blatt 14 (varianten_v2/14_Variante_B_Ansichten.png).
Die Ortho-Ansicht enthält die Farbcodes von Blatt 25; sichtbar sind Abweichungen als Doppelkanten."""
import os
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
P, M = 11.811, 4.0
plan = Image.open(os.path.join(ROOT, "varianten_v2", "14_Variante_B_Ansichten.png")).convert("RGB")
D = os.path.join(ROOT, "visualisierungen", "higgsfield", "renderings", "v4", "00_geometrie_ortho")
for v, (ox, gy, a0, a1) in {"front": (34, 100, -1, 33), "rear": (174, 100, -1, 33), "west": (34, 215, -1, 22), "east": (174, 215, -1, 22)}.items():
    box = (round((ox + a0 * M) * P), round((gy - 10.5 * M) * P), round((ox + a1 * M) * P), round((gy + 0.3 * M) * P)); c = plan.crop(box)
    m = Image.open(os.path.join(D, f"ortho_{v}.png")).convert("RGB").resize(c.size); Image.blend(c, m, 0.5).save(os.path.join(D, f"ueberlagerung_blatt14_modell_{v}.png")); print("ok", v)
