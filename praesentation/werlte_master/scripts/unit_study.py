"""Nutzbarkeitsstudie WE-L1-S (ca. 39 m2 netto): Möblierungs- und Bewegungsflächenprobe, KEINE Grundrissoptimierung auf Wohnungszahl.
Innenmaße ASSUMED: Fassade 0,45 m, Wohnungstrennwand 0,25 m (halb 0,125 je Seite), Flurwand 0,20 m.
Koordinaten: x West->Ost, y von der Platzfassade (0) zur Flurwand (D). Richtwerte der Möbel und Bewegungsflächen sind übliche Planungswerte (ASSUMED), keine NBauO-Zitate."""
import json, os
here = os.path.dirname(__file__)
W, D = 5.6 - 0.25, 8.0 - 0.45 - 0.20          # Innenmaße
F = {  # Möbel / Ausstattung  (x0, y0, x1, y1)
 "Bett 1,4x2,0": (3.35, 0.35, 5.35, 1.75), "Kleiderschrank 1,2x0,6": (4.15, 3.85, 5.35, 4.45),
 "Sofa 2,0x0,9": (0.0, 0.9, 0.9, 2.9), "Tisch 0,8x0,8": (1.35, 2.6, 2.15, 3.4),
 "Küchenzeile 2,4x0,6": (0.0, 4.65, 0.6, 7.05), "Dusche 1,0x1,0": (4.35, 6.35, 5.35, 7.35),
 "WC 0,5x0,7": (4.85, 5.2, 5.35, 5.9), "Waschtisch 0,6x0,55": (3.1, 6.8, 3.7, 7.35), "Waschmaschine 0,6x0,6": (3.1, 4.55, 3.7, 5.15)}
Z = {  # freizuhaltende Bewegungsflächen
 "Balkontür 1,2x1,2": (2.075, 0.0, 3.275, 1.2), "vor Bett (Seite) 0,6": (3.35, 1.75, 5.35, 2.35),
 "vor Küche 1,2x1,2": (0.6, 5.1, 1.8, 6.3), "Eingang 1,2x1,2": (1.6, 6.15, 2.8, 7.35),
 "vor Schrank 0,6": (4.15, 3.25, 5.35, 3.85), "vor WC 1,2x1,2": (3.75, 5.15, 4.85, 6.35)}
R = {"Wohnen/Schlafen (vorn)": (0, 0, W, 4.45), "Flur/Küche": (0, 4.45, 3.0, D), "Bad": (3.0, 4.45, W, D)}
doors = {"Balkontür": (2.075, 3.275, "front"), "Wohnungstür": (1.9, 2.8, "rear"), "Bad (Schiebetür)": (3.0, "west wall y 5.3-6.2")}
ov = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
res = []
inb = lambda r: r[0] >= -1e-9 and r[1] >= -1e-9 and r[2] <= W + 1e-9 and r[3] <= D + 1e-9
for n, r in {**F, **Z}.items():
    if not inb(r): res.append(("FAIL", f"{n} außerhalb der Wohnung"))
names = list(F)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        if ov(F[names[i]], F[names[j]]): res.append(("FAIL", f"Möbel überlappen: {names[i]} / {names[j]}"))
for zn, zr in Z.items():
    for fn, fr in F.items():
        if ov(zr, fr): res.append(("FAIL", f"Bewegungsfläche '{zn}' durch '{fn}' blockiert"))
area = {k: round((v[2] - v[0]) * (v[3] - v[1]), 1) for k, v in R.items()}
fa = 0.25 * 3.2 * 2.2  # Balkon-Fenstertür grob (1,2 x 2,2) – Fensterfläche nur Näherung
res.append(("INFO", f"Innenmaß {W:.2f} x {D:.2f} m = {W*D:.1f} m² (Modell netto 39,4 m²); Raumflächen {area}"))
res.append(("INFO", "Alle Aufenthaltsbereiche liegen an der Platzfassade; Tiefe 7,35 m, Bad und Küchenzeile innenliegend (mechanische Lüftung nötig)"))
res.append(("INFO", f"Fassadenbreite des Wohn-/Schlafraums {W:.2f} m: eine Fenster-/Balkontür-Achse (Balkon 2,7 m), keine Querlüftung"))
fails = [r for r in res if r[0] == "FAIL"]
# ---- SVG
K = 80; ox = 60; oy = 150
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(ox*2+W*K+520)}" height="{int(oy+D*K+110)}" font-family="Arial"><rect width="100%" height="100%" fill="white"/>',
     '<text x="20" y="28" font-size="18" font-weight="bold">Nutzbarkeitsprobe WE-L1-S (39 m² netto) – Arbeitsstand, keine Freigabe</text>',
     '<text x="20" y="48" font-size="11" fill="#a00">Möblierungsprobe zur Prüfung der Eigenständigkeit. Keine Grundrisse zur Maximierung der Wohnungszahl. Maße ASSUMED.</text>',
     f'<text x="{ox}" y="{oy-12}" font-size="11">Platzfassade (Fenster/Balkon) – y = 0</text>']
col = {"Wohnen/Schlafen (vorn)": "#F7E9D0", "Flur/Küche": "#EEE6DA", "Bad": "#D6E6EC"}
for n, r in R.items():
    o.append(f'<rect x="{ox+r[0]*K}" y="{oy+r[1]*K}" width="{(r[2]-r[0])*K}" height="{(r[3]-r[1])*K}" fill="{col[n]}" stroke="#999"/><text x="{ox+(r[0]+r[2])/2*K}" y="{oy+r[1]*K+14}" font-size="10" text-anchor="middle" fill="#555">{n} {area[n]} m²</text>')
for n, r in Z.items():
    o.append(f'<rect x="{ox+r[0]*K}" y="{oy+r[1]*K}" width="{(r[2]-r[0])*K}" height="{(r[3]-r[1])*K}" fill="#9bd" opacity="0.3" stroke="#46a" stroke-dasharray="3 3"/>')
for n, r in F.items():
    o.append(f'<rect x="{ox+r[0]*K}" y="{oy+r[1]*K}" width="{(r[2]-r[0])*K}" height="{(r[3]-r[1])*K}" fill="#B08968" stroke="#333"/><text x="{ox+(r[0]+r[2])/2*K}" y="{oy+(r[1]+r[3])/2*K+3}" font-size="8" text-anchor="middle" fill="#fff">{n.split()[0]}</text>')
o.append(f'<rect x="{ox}" y="{oy}" width="{W*K}" height="{D*K}" fill="none" stroke="#111" stroke-width="4"/>')
o.append(f'<rect x="{ox+2.075*K}" y="{oy-4}" width="{1.2*K}" height="8" fill="#1F9" stroke="#111"/><rect x="{ox+1.9*K}" y="{oy+D*K-4}" width="{0.9*K}" height="8" fill="#e90" stroke="#111"/>')
o.append(f'<rect x="{ox+1.325*K}" y="{oy-1.5*K}" width="{2.7*K}" height="{1.5*K}" fill="#CFD3D6" stroke="#333" stroke-dasharray="4 3" opacity="0.7"/><text x="{ox+2.675*K}" y="{oy-0.6*K}" font-size="10" text-anchor="middle">Balkon 2,7 x 1,5</text>')
for i, (st, t) in enumerate(res):
    o.append(f'<text x="{ox+W*K+20}" y="{oy+16+i*15}" font-size="10" fill="{"#a00" if st=="FAIL" else "#333"}">{st}: {t[:130]}</text>')
o.append(f'<text x="{ox}" y="{oy+D*K+30}" font-size="10" fill="#333">blau gestrichelt = Bewegungsflächen, grün = Balkontür (Balkon 2,7 m, Mitte x 2,675), orange = Wohnungstür vom Mittelgang</text></svg>')
open(os.path.join(here, "..", "plans", "unit_WE-L1-S_nutzbarkeit.svg"), "w", encoding="utf-8").write("\n".join(o))
print(len(fails), "FAIL")
for s in res: print(s)
