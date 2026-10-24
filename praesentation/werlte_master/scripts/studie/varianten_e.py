"""Variante E – 12 m und umlaufender Vorbau mit Parken (Teilvarianten E1–E4). Registriert sich in varianten.V.
Annahmen (alle vorläufig): Grundstück H1 32 x 30 m (PLOT_POLY austauschbar, sobald der Zuschnitt aus den städtischen Unterlagen vorliegt); Platzseite y = 0;
Zufahrt von Osten (x = 32) in die rückwärtige Fahrgasse (Lage der Straße unbekannt); Stellplatz 2,50 x 5,00 m, Fahrgasse 6,00 m, Säule Ø 0,40 m.
Höhenschema H12: EG 4,30 m, 1. OG 3,60 m, 2. OG 3,60 m, Attika +12,00 m (Höhenbezug ±0,00 = OK Fertigfußboden EG, Bezugspunkt der Stadt unbelegt)."""
import math, varianten as VA
ZE = {"EG": (0.0, 4.3), "OG1": (4.3, 7.9), "ST": (7.9, 11.5), "ATT": (11.5, 12.0)}
DECKE = 0.45; ST_L, ST_T, GASSE, SAEULE_D = 2.5, 5.0, 6.0, 0.4
PLOT_POLY = [(0, 0), (32, 0), (32, 30), (0, 30)]  # H1 – hypothetisch
PAAR = 5.4  # zwei Stellplätze 2,50 m + Säule 0,40 m
def pair_cols(start, n=5): return [round(start + 5.0 + 0.2 + PAAR * j, 3) for j in range(n)]
def rear_columns(x0, x1, y):
    xs = [x0] + pair_cols(2.5) + [x1]; return [(round(x, 3), y) for x in xs]
def columns(D):
    ins = 0.35; x0, x1, y0, y1 = ins, 32 - ins, ins, D - ins; pts = []
    nf = 6; pts += [(round(x0 + (x1 - x0) * i / nf, 3), y0) for i in range(nf + 1)]
    pts += rear_columns(x0, x1, y1)
    ny = math.ceil((y1 - y0) / 5.0)
    for i in range(1, ny): y = round(y0 + (y1 - y0) * i / ny, 3); pts += [(x0, y), (x1, y)]
    return pts
def stalls_row(y0, xs0, n, skip=(), paare=True):
    """n Stellplätze; paare=True: je zwei Plätze 2,50 m, dann 0,40 m Säule (Raster 5,4 m)."""
    out = []
    for i in range(n):
        if i in skip: continue
        x = xs0 + (PAAR * (i // 2) + ST_L * (i % 2) if paare else ST_L * i); out.append((round(x, 3), y0, round(x + ST_L, 3), y0 + ST_T))
    return out
def mk(key, s, D, d, name, idee, p2=False):
    og1 = [(0, 0, 32, D)]; st = [(s, s, 32 - s, D - s)]
    eg = [(2.5, 1.5, 29.5, d), (0, 1.5, 2.5, 9.5)]
    stalls = stalls_row(d, 2.5, 10, skip=(5,))  # ein Platz entfällt: Hintereingang Gewerbe/Anlieferung (x 15,8–18,3)
    row2 = []
    if p2: row2 = stalls_row(25.0, 1.0, 12, paare=False)
    gy = 1.5 + (d - 1.5) * 0.62
    rooms = [("Kern", (0.0, 1.5, 4.0, 9.5), "core"), ("Gastraum", (4.0, 1.5, 29.5, gy), "dining"), ("Gastraum", (2.5, 9.5, 4.0, gy), "dining"), ("Küche / Lager / WC", (2.5, gy, 19.0, d), "kitchen"), ("Büro / Technik", (19.0, gy, 29.5, d), "office")]
    rooms = [x for x in rooms if x[1][3] > x[1][1] + 0.01]
    gastro = sum((r[2] - r[0]) * (r[3] - r[1]) for n, r, c in rooms if c == "dining")
    gf = (VA.rects_area(eg) / 576.0)
    return dict(name=name, kurz=name.split(" – ")[0], farbe="#0F766E", idee=idee, Z=ZE, eg=eg, og1=og1, st=st,
                wohn={"og1": (4, 0, 32, D), "st": (s + 4, s, 32 - s, D - s)}, saeulen="x", saeulen_pts=columns(D), balkone="keine", vordach=False,
                bruestung=([] if s == 0 else [(0, 0, 32, 0), (0, D, 32, D), (0, 0, 0, D), (32, 0, 32, D)]), st_mat=("klinker" if s == 0 else "holz"),
                stalls=stalls + row2, stalls_row1=stalls, stalls_row2=row2, asphalt=(0, d, 32, 30), glas_front=(2.5, 29.5, 1.5), gewerbe_faktor=round(gf, 3),
                gastro_m2=round(gastro, 1), eg_raeume=rooms, terr_m2=27 * 1.5, zufahrt=(32.0, d + ST_T, 32.0, d + ST_T + GASSE), zufahrt_dir="E",
                eingaenge=[("Hintereingang/Anlieferung", (15.8, d, 18.3, d + 2.5)), ("Gastro-Eingang (Arkade)", (8.0, 0.0, 14.0, 1.5)), ("Kern/Wohnzugang", (0.0, 0.0, 4.0, 1.5))],
                stall_face={"row1": "S", "row2": "N"}, fahrgasse=(0, d + ST_T, 32, d + ST_T + GASSE) if not p2 else (0, d + ST_T, 32, d + ST_T + GASSE), plot=PLOT_POLY, staffel_ruecksprung=s)
VA.V["E1"] = mk("E1", 0.0, 24.0, 19.0, "E1 – Vorbau bis Attika (Staffel deckungsgleich)", "12,00 m Gesamthöhe, drei Geschosse; 1. und 2. OG kragen auf allen vier Seiten über das Erdgeschoss (vorn 1,50 m Arkade, seitlich 2,50 m, hinten 5,00 m über der Stellplatzreihe) und sind deckungsgleich bis zur Attika; Säulen am Rand.")
VA.V["E2"] = mk("E2", 1.5, 24.0, 19.0, "E2 – Staffel 1,50 m zurück", "Wie E1, das 2. OG springt rundum 1,50 m hinter die Kante des 1. OG zurück (umlaufende Dachterrasse).")
VA.V["E3"] = mk("E3", 3.0, 24.0, 19.0, "E3 – Staffel 3,00 m zurück", "Wie E1, das 2. OG springt rundum 3,00 m zurück (breite umlaufende Dachterrasse, kleineres Staffelgeschoss).")
VA.V["E4"] = mk("E4", 1.5, 19.0, 14.0, "E4 – zweireihiges Parken, kleineres EG", "Wie E2, aber Erdgeschoss nur 14 m tief: zwei Stellplatzreihen (eine unter dem 5-m-Vorbau hinten, eine frei) mit 6-m-Fahrgasse dazwischen; dafür weniger Gewerbefläche.", p2=True)
