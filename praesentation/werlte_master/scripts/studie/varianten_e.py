"""Variante E – 12 m und umlaufender Vorbau mit Parken (Teilvarianten E1–E4). Registriert sich in varianten.V.
Annahmen (alle vorläufig): Grundstück H1 32 x 30 m (PLOT_POLY austauschbar, sobald der Zuschnitt aus den städtischen Unterlagen vorliegt); Platzseite y = 0;
Zufahrt von Osten (x = 32) in die rückwärtige Fahrgasse (Lage der Straße unbekannt); Stellplatz 2,50 x 5,00 m, Fahrgasse 6,00 m, Säule Ø 0,40 m.
Höhenschema H12: EG 4,30 m, 1. OG 3,60 m, 2. OG 3,60 m, Attika +12,00 m (Höhenbezug ±0,00 = OK Fertigfußboden EG, Bezugspunkt der Stadt unbelegt)."""
import math, varianten as VA
ZE = {"EG": (0.0, 4.3), "OG1": (4.3, 7.9), "ST": (7.9, 11.5), "ATT": (11.5, 12.0)}
DECKE = 0.45; ST_L, ST_T, GASSE, SAEULE_D = 2.5, 5.0, 6.0, 0.4
PLOT_POLY = [(0, 0), (32, 0), (32, 30), (0, 30)]  # H1 – hypothetisch
def rear_columns(x0, x1, y):
    xs = [x0] + [float(x) for x in range(5, 31, 5)] + [x1]; return [(round(x, 3), y) for x in xs]
def columns(D):
    ins = 0.35; x0, x1, y0, y1 = ins, 32 - ins, ins, D - ins; pts = []
    nf = 6; pts += [(round(x0 + (x1 - x0) * i / nf, 3), y0) for i in range(nf + 1)]
    pts += rear_columns(x0, x1, y1)
    ny = math.ceil((y1 - y0) / 5.0)
    for i in range(1, ny): y = round(y0 + (y1 - y0) * i / ny, 3); pts += [(x0, y), (x1, y)]
    return pts
def stalls_row(y0, xs0, n, skip=()):
    return [(round(xs0 + ST_L * i, 3), y0, round(xs0 + ST_L * (i + 1), 3), y0 + ST_T) for i in range(n) if i not in skip]
def mk(key, s, D, d, name, idee, p2=False):
    og1 = [(0, 0, 32, D)]; st = [(s, s, 32 - s, D - s)]
    eg = [(2.5, 1.5, 29.5, d), (0, 1.5, 2.5, 9.5)]
    stalls = stalls_row(d, 2.5, 11, skip=(7,))  # Platz 7 entfällt: Hintereingang Gewerbe/Anlieferung (x 17,5–20,0)
    row2 = []
    if p2: row2 = stalls_row(25.0, 1.0, 12)
    gf = (VA.rects_area(eg) / 576.0)
    return dict(name=name, kurz=name.split(" – ")[0], farbe="#0F766E", idee=idee, Z=ZE, eg=eg, og1=og1, st=st,
                wohn={"og1": (4, 0, 32, D), "st": (s + 4, s, 32 - s, D - s)}, saeulen="x", saeulen_pts=columns(D), balkone="keine", vordach=False,
                bruestung=([] if s == 0 else [(0, 0, 32, 0), (0, D, 32, D), (0, 0, 0, D), (32, 0, 32, D)]), st_mat=("klinker" if s == 0 else "holz"),
                stalls=stalls + row2, stalls_row1=stalls, stalls_row2=row2, asphalt=(0, d, 32, 30), glas_front=(2.5, 29.5, 1.5), gewerbe_faktor=round(gf, 3),
                zufahrt=(32.0, d + ST_T, 32.0, 30.0), fahrgasse=(0, d + ST_T, 32, d + ST_T + GASSE) if not p2 else (0, d + ST_T, 32, d + ST_T + GASSE), plot=PLOT_POLY, staffel_ruecksprung=s)
VA.V["E1"] = mk("E1", 0.0, 24.0, 19.0, "E1 – Vorbau bis Attika (Staffel deckungsgleich)", "12,00 m Gesamthöhe, drei Geschosse; 1. und 2. OG kragen auf allen vier Seiten über das Erdgeschoss (vorn 1,50 m Arkade, seitlich 2,50 m, hinten 5,00 m über der Stellplatzreihe) und sind deckungsgleich bis zur Attika; Säulen am Rand.")
VA.V["E2"] = mk("E2", 1.5, 24.0, 19.0, "E2 – Staffel 1,50 m zurück", "Wie E1, das 2. OG springt rundum 1,50 m hinter die Kante des 1. OG zurück (umlaufende Dachterrasse).")
VA.V["E3"] = mk("E3", 3.0, 24.0, 19.0, "E3 – Staffel 3,00 m zurück", "Wie E1, das 2. OG springt rundum 3,00 m zurück (breite umlaufende Dachterrasse, kleineres Staffelgeschoss).")
VA.V["E4"] = mk("E4", 1.5, 19.0, 14.0, "E4 – zweireihiges Parken, kleineres EG", "Wie E2, aber Erdgeschoss nur 14 m tief: zwei Stellplatzreihen (eine unter dem 5-m-Vorbau hinten, eine frei) mit 6-m-Fahrgasse dazwischen; dafür weniger Gewerbefläche.", p2=True)
