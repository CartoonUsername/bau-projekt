"""Kleine PDF-Hilfsbibliothek (PIL) für die Variantenstudie: A3 quer (3508 x 2480 px = 300 dpi / 2), Inter-Schrift, Tabellen mit Umbruch."""
from PIL import Image, ImageDraw, ImageFont
W, H = 3508, 2480
INK, GREY, LG, ACC, OK, WARN, BAD = (27, 31, 36), (107, 114, 128), (225, 228, 233), (154, 52, 18), (22, 101, 52), (180, 83, 9), (185, 28, 28)
def F(s, w="Regular"): return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)
def page(): im = Image.new("RGB", (W, H), "white"); return im, ImageDraw.Draw(im)
def wrap(d, text, font, maxw):
    lines = []
    for para in str(text).split("\n"):
        cur = ""
        for wd in para.split():
            t = (cur + " " + wd).strip()
            if d.textlength(t, font=font) <= maxw: cur = t
            else:
                if cur: lines.append(cur)
                cur = wd
        lines.append(cur)
    return lines
def header(d, title, sub=None, tag=None):
    d.text((120, 80), title, font=F(66, "SemiBold"), fill=INK)
    if sub: d.text((120, 168), sub, font=F(32), fill=GREY)
    d.line([(120, 225), (W - 120, 225)], fill=LG, width=3)
    if tag: d.rounded_rectangle([W - 120 - 700, 70, W - 120, 140], radius=14, fill=(253, 241, 231), outline=ACC, width=3); d.text((W - 120 - 680, 86), tag, font=F(30, "SemiBold"), fill=ACC)
def footer(d, n, text="Entwurfsstudie Neue Mitte Werlte – Baufeld 3 · alle Werte vorläufig · keine Variante festgelegt · Baurecht, Statik und Förderung nicht bestätigt"):
    d.text((120, H - 90), text, font=F(26), fill=GREY); d.text((W - 220, H - 90), str(n), font=F(26), fill=GREY)
def paste(im, path, x, y, w, h):
    src = Image.open(path).convert("RGB")
    if "/plaene/" in path:
        from PIL import ImageChops; bb = ImageChops.difference(src, Image.new("RGB", src.size, "white")).getbbox()
        if bb: src = src.crop((max(0, bb[0] - 20), max(0, bb[1] - 20), min(src.width, bb[2] + 20), min(src.height, bb[3] + 20)))
    k = min(w / src.width, h / src.height); src = src.resize((int(src.width * k), int(src.height * k)), Image.LANCZOS)
    ox, oy = x + (w - src.width) // 2, y; im.paste(src, (ox, oy)); return (ox, oy, src.width, src.height)
def text_block(d, x, y, w, text, size=34, color=INK, weight="Regular", lh=1.35):
    f = F(size, weight)
    for ln in wrap(d, text, f, w): d.text((x, y), ln, font=f, fill=color); y += int(size * lh)
    return y
def table(d, x, y, colw, rows, size=28, head=True, zebra=True, colors=None):
    """rows: Liste von Listen; colors: dict (zeile, spalte) -> RGB-Textfarbe"""
    fb, fr = F(size, "SemiBold"), F(size); pad = 14; cy = y
    for ri, row in enumerate(rows):
        cells = [wrap(d, str(c), fb if (ri == 0 and head) or ci == 0 else fr, colw[ci] - 2 * pad) for ci, c in enumerate(row)]
        hh = max(len(c) for c in cells) * int(size * 1.3) + 2 * pad
        if ri == 0 and head: d.rectangle([x, cy, x + sum(colw), cy + hh], fill=(229, 232, 236))
        elif zebra and ri % 2 == 0: d.rectangle([x, cy, x + sum(colw), cy + hh], fill=(247, 248, 250))
        cx = x
        for ci, lines in enumerate(cells):
            col = (colors or {}).get((ri, ci), INK); yy = cy + pad
            for ln in lines: d.text((cx + pad, yy), ln, font=fb if (ri == 0 and head) or ci == 0 else fr, fill=col); yy += int(size * 1.3)
            cx += colw[ci]
        d.line([(x, cy + hh), (x + sum(colw), cy + hh)], fill=LG, width=2); cy += hh
    d.rectangle([x, y, x + sum(colw), cy], outline=(190, 195, 203), width=2)
    return cy
def save(pages, path): pages[0].save(path, save_all=True, append_images=pages[1:], resolution=150)
