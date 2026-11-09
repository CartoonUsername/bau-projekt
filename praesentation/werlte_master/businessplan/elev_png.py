"""Ansichten (Vorder-/Rück-/West-/Ostansicht) aus dem Geometriemodell als PNG – Vektorzeichnung (revitalyze_pdfs.elevation) mit pdftoppm gerastert."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "scripts", "studie"))
import revitalyze_modelle as RM, revitalyze_pdfs as RP
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
def make(key, s, outdir):
    m = RM.modell_B(key, key, "x.pdf", s); os.makedirs(outdir, exist_ok=True)
    for side in ("front", "rear", "west", "east"):
        name, hf, osd = RP.SIDES[side]; a, b = RP.elev_bbox(m, hf)
        W, H = 500, 205; pdf = os.path.join(outdir, f"_{side}.pdf"); c = canvas.Canvas(pdf, pagesize=(W * mm, H * mm))
        sh = RP.Sheet.__new__(RP.Sheet); sh.c = c; sh.W, sh.H = W, H; sh.m = m; sh.area = (4, 4, W - 4, H - 4); sh.tb = "none"
        sh.fit((a - 2.5, -4.5, b + 13.5, m["zattika"] + 2.6)); RP.elevation(sh, m, side); c.showPage(); c.save()
        subprocess.run(["pdftoppm", "-r", "110", "-png", "-singlefile", pdf, os.path.join(outdir, side)], check=True); os.remove(pdf)
if __name__ == "__main__":
    for k, s in (("R1", 0.0), ("R2", 1.5), ("R3", 3.0)): make(k, s, os.path.join(HERE, "bilder", "ansichten", k))
