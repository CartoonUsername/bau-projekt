"""Zeichnet SVG-Grundrisse (EG, OG-1, OG-2, Staffel) aus geometry/building_design.json. Maßstab 1 m = 30 px."""
import json, os
here = os.path.dirname(__file__)
D = json.load(open(os.path.join(here, "..", "geometry", "building_design.json"), encoding="utf-8"))
K = 30; OX = 60; OY = 70
COL = {"core": "#8A9199", "dining": "#F2D48C", "lounge": "#B07A4A", "bar": "#3A3F44", "private_dining": "#7A5C3A", "circulation": "#D9D3C8", "wc": "#A6ADB4", "storage": "#A6ADB4", "kitchen": "#7E8A94", "office": "#3F6275", "apartment": "#9A4034", "corridor": "#D9D3C8"}
def svg(title, rooms, extra=""):
    W = int(OX * 2 + 32 * K + 120); H = int(OY + 18 * K + 120)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Arial">', f'<rect width="{W}" height="{H}" fill="white"/>', f'<text x="{OX}" y="36" font-size="22" font-weight="bold">{title}</text>',
         f'<text x="{OX}" y="58" font-size="12" fill="#555">Entwurf Variante A, nicht freigegeben. x: West nach Ost, y: Platzfassade (oben) nach hinten. Maße in m.</text>']
    for r in rooms:
        x0, y0, x1, y1 = r["rect"]
        o.append(f'<rect x="{OX+x0*K}" y="{OY+y0*K}" width="{(x1-x0)*K}" height="{(y1-y0)*K}" fill="{COL.get(r["type"], "#ddd")}" stroke="white" stroke-width="2" opacity="0.92"/>')
        lab = r["id"] + (f"\\n{r['area_gross']:.0f} m²" if r.get("area_gross") else "")
        for i, t in enumerate(lab.split("\\n")):
            o.append(f'<text x="{OX+(x0+x1)/2*K}" y="{OY+(y0+y1)/2*K+i*14-4}" font-size="11" text-anchor="middle" fill="{"#111" if r["type"] in ("dining","corridor","circulation") else "white"}">{t}</text>')
        if r.get("balcony"):
            bw, bd = 2.7, 1.5; cx = (x0 + x1) / 2
            by = y0 - bd if r["balcony"] == "front" else y1
            o.append(f'<rect x="{OX+(cx-bw/2)*K}" y="{OY+by*K}" width="{bw*K}" height="{bd*K}" fill="#CFD3D6" stroke="#333" stroke-dasharray="4 3"/>')
    o.append(f'<rect x="{OX}" y="{OY}" width="{32*K}" height="{18*K}" fill="none" stroke="#111" stroke-width="3"/>')
    o.append(extra); o.append("</svg>")
    return "\n".join(o)
os.makedirs(os.path.join(here, "..", "plans"), exist_ok=True)
gf = [r for r in D["rooms"] if r["level"] == "GF"]
ter = D["terrace"]["rect"]
extra = f'<rect x="{OX+ter[0]*K}" y="{OY+ter[1]*K}" width="{(ter[2]-ter[0])*K}" height="{(ter[3]-ter[1])*K}" fill="#D6B98F" stroke="#333" stroke-dasharray="6 4"/><text x="{OX+18*K}" y="{OY+ter[1]*K+60}" font-size="12" text-anchor="middle">Terrasse ca. 60 Plätze</text>'
for r in D["openings"]:
    x0, x1 = r["x"]; extra += f'<rect x="{OX+x0*K}" y="{OY-3}" width="{(x1-x0)*K}" height="6" fill="#1F9" stroke="#111"/>'
# Terrasse liegt bei negativem y: Kopfzeile verschieben
import re
def write(name, title, rooms, ex=""):
    s = svg(title, rooms, ex).replace(f'y="{OY}"', f'y="{OY}"')
    open(os.path.join(here, "..", "plans", name), "w", encoding="utf-8").write(s)
OY = 70 + 4 * K
write("plan_EG.svg", "Erdgeschoss (Variante A, Entwurf)", gf, extra)
write("plan_OG1.svg", "1. OG Option OG-1: " + D["upper_options"]["OG-1"]["name"], D["upper_options"]["OG-1"]["rooms"])
write("plan_OG2.svg", "1. OG Option OG-2: " + D["upper_options"]["OG-2"]["name"], D["upper_options"]["OG-2"]["rooms"])
write("plan_Staffel.svg", "Staffelgeschoss: " + D["staffel"]["name"], D["staffel"]["rooms"])
print("Pläne geschrieben")
