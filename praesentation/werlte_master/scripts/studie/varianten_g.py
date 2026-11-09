"""Geometrie-Prüfskizzen G1–G3 auf Baufeld 3 (Annahme: MI 3 / Flurstück 59/1 des B-Plans Nr. 123, ca. 42,3 × 22,7 m, Planstraße im Norden, Marktstraße im Westen).
KOORDINATEN: x nach Osten (0 = Westgrenze, Marktstraße), y nach Süden (0 = Nordgrenze an der Planstraße). Baufenster P23 (abgeleitet, Vektorplan 1:1000): x 10,5–38,2, y 3,4–19,3 (≈ 27,7 × 15,9 m).
G1: EG = Baufenster. G2: kleineres EG, Obergeschosse im Baufenster (Vorbau), Stellplatzreihe + Fahrgasse im Osten. G3: EG 540 m² (30 × 18 m) – nur mit Befreiung/Änderung der Baugrenzen.
Alles Planungsannahmen; weder Grundstück noch Baugrenzen sind vermessen; keine Genehmigungsplanung."""
import math, varianten as VA, varianten_e as VE
PLOT_RECT = (0.0, 0.0, 42.3, 22.7); BF = (10.5, 3.4, 38.2, 19.3); ZE = VE.ZE
def perim_cols(r, ins=0.35, step=5.0, east_ys=None):
    x0, y0, x1, y1 = r[0] + ins, r[1] + ins, r[2] - ins, r[3] - ins; pts = []
    nx = max(1, round((x1 - x0) / step)); ny = max(1, round((y1 - y0) / step))
    pts += [(round(x0 + (x1 - x0) * i / nx, 3), y0) for i in range(nx + 1)] + [(round(x0 + (x1 - x0) * i / nx, 3), y1) for i in range(nx + 1)]
    pts += [(x0, round(y0 + (y1 - y0) * j / ny, 3)) for j in range(1, ny)]
    pts += [(x1, y) for y in (east_ys if east_ys is not None else [round(y0 + (y1 - y0) * j / ny, 3) for j in range(1, ny)])]
    return sorted(set(pts))
def base(name, kurz, idee, eg, og1, st, rooms, gastro, terr, **kw):
    d = dict(name=name, kurz=kurz, farbe="#0369A1", idee=idee, Z=ZE, eg=eg, og1=og1, st=st, eg_raeume=rooms, plot_rect=PLOT_RECT, saeulen="x", balkone="keine", vordach=False, bruestung=[], st_mat="klinker",
             wohn={"og1": (og1[0][0] + 4, og1[0][1], og1[0][2], og1[0][3]), "st": (st[0][0] + 4, st[0][1], st[0][2], st[0][3])}, gastro_m2=gastro, terr_m2=terr, staffel_ruecksprung=0.0, stalls_row1=[], stalls_row2=[], stalls_par=[], stalls=[], stall_face={}, eingaenge=[])
    d.update(kw); return d
# G1: volles Baufenster
eg1 = [BF]
VA.V["G1"] = base("G1 – EG im vollen Baufenster (27,7 × 15,9 m)", "G1", "EG, 1. OG und 2. OG im vollen Baufenster des B-Plans 2023 (≈ 440 m²); kein Vorbau (Baugrenze), keine Stellplätze auf dem Grundstück.", eg1, [BF], [BF],
    [("Kern", (BF[0], BF[1], BF[0] + 4, BF[1] + 8), "core"), ("Gastraum", (BF[0] + 4, BF[1], BF[2], BF[1] + 9), "dining"), ("Küche / Lager / WC", (BF[0] + 4, BF[1] + 9, BF[2] - 8, BF[3]), "kitchen"), ("Büro / Technik", (BF[2] - 8, BF[1] + 9, BF[2], BF[3]), "office")], 36 * 6.5, 25.0,
    saeulen_pts=perim_cols(BF), fahrgasse=(0, 0, 0.1, 0.1), zufahrt=(0, 0, 0, 0), zufahrt_dir="E")
# G2: kleineres EG, OG im Baufenster, Stellplätze Ost
EG2 = (12.5, 4.9, 31.0, 17.8)
stalls2 = [(37.3, round(4.0 + VE.PAAR * (k // 2) + 2.5 * (k % 2), 3), 42.3, round(6.5 + VE.PAAR * (k // 2) + 2.5 * (k % 2), 3)) for k in range(5)]
cols2 = [c for c in perim_cols(BF, east_ys=[3.75, 9.2, 14.6, 18.95]) if not (31.2 < c[0] < 37.6 and c[1] in (3.75, 18.95))]  # Fahrgasse (x 31,3–37,3) wird stützenfrei überspannt
VA.V["G2"] = base("G2 – kleineres EG, Obergeschosse im Baufenster, Stellplätze Ost", "G2", "EG 18,5 × 12,9 m (≈ 239 m²); 1./2. OG im vollen Baufenster (Vorbau 2,0 m West, 1,5 m Nord/Süd, 6,2 m Ost über die 6-m-Fahrgasse); Stellplatzreihe an der Ostgrenze; Zufahrt von der Planstraße im Norden.", [EG2], [BF], [BF],
    [("Kern", (12.5, 4.9, 16.5, 12.0), "core"), ("Gastraum", (16.5, 4.9, 31.0, 12.0), "dining"), ("Küche / Lager / WC", (12.5, 12.0, 24.0, 17.8), "kitchen"), ("Büro / Technik", (24.0, 12.0, 31.0, 17.8), "office")], 14.5 * 7.1, 21.0,
    saeulen_pts=cols2, stalls_row1=stalls2, stalls=stalls2, stall_face={"row1": "W"}, asphalt=(31.0, 0.0, 42.3, 22.7), fahrgasse=(31.3, 0.0, 37.3, 22.7), zufahrt=(31.3, 0.0, 37.3, 0.0), zufahrt_dir="N",
    eingaenge=[("Hintereingang/Anlieferung", (31.0, 12.3, 33.5, 14.8)), ("Gastro-Eingang (Planstraße)", (20.0, 3.4, 26.0, 4.9)), ("Kern/Wohnzugang", (12.5, 3.4, 16.5, 4.9))])
# G3: EG 540 m² (Befreiung)
EG3 = (6.0, 2.7, 36.0, 20.7)
VA.V["G3"] = base("G3 – EG 540 m² (30 × 18 m), nur mit Befreiung", "G3", "EG 30 × 18 m = 540 m² (Planungsziel) auf Flurstück 59/1; liegt außerhalb des Baufensters (West 10,0 → 6,0 m, Nord/Süd/Ost < 3 m) – nur mit Befreiung bzw. Änderung der Baugrenzen; keine Stellplätze möglich.", [EG3], [EG3], [(EG3[0] + 1.5, EG3[1] + 1.5, EG3[2] - 1.5, EG3[3] - 1.5)],
    [("Kern", (6.0, 2.7, 10.0, 11.0), "core"), ("Gastraum", (10.0, 2.7, 36.0, 11.5), "dining"), ("Küche / Lager / WC", (10.0, 11.5, 24.0, 20.7), "kitchen"), ("Büro / Technik", (24.0, 11.5, 36.0, 20.7), "office")], 26 * 8.8, 30.0,
    saeulen_pts=perim_cols(EG3), fahrgasse=(0, 0, 0.1, 0.1), zufahrt=(0, 0, 0, 0), zufahrt_dir="E")
for k in ("G1", "G2", "G3"): VA.V[k]["wohn"]["st"] = (VA.V[k]["st"][0][0] + 4, VA.V[k]["st"][0][1], VA.V[k]["st"][0][2], VA.V[k]["st"][0][3])
