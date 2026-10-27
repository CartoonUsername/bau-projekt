"""Variante R (Ring) – Erdgeschoss 540 m² (GRZ-Obergrenze, 60 %), die Obergeschosse überragen das EG RINGSUM (West 1,0 / Platz 1,5 / Rück 1,5 / Ost 5,0 m über der Stellplatzreihe). Planungsvorgabe 27.10.2026.
Unterschied zu F: das EG ist 20 × 27 m (statt 18 × 30 m) und steht in der Grundstückstiefe zurückgesetzt, damit der Vorbau auch rückseitig und zum Platz INNERHALB der Hypothese 32 × 30 m bleibt (F: rückseitig 0 m, Platzseite 1,5 m über die Grenze).
Alles Annahme: Grundstück H1 32 × 30 m, Zufahrt von Süden (y = 30), Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m, Säule Ø 0,40 m, Höhenschema aus varianten_e.py (hypothetisch). R1/R2/R3: oberstes Geschoss bündig / 1,50 m / 3,00 m hinter der OG1-Kante."""
import varianten as VA, varianten_e as VE
ZE = VE.ZE
EG = (1.0, 1.5, 21.0, 28.5); OG = (0.0, 0.0, 26.0, 30.0)
def cols_ring():
    x0, x1, y0, y1 = 0.35, 25.65, 0.35, 29.65; pts = []
    pts += [(round(x0 + (x1 - x0) * i / 5, 3), y0) for i in range(6)] + [(round(x0 + (x1 - x0) * i / 5, 3), y1) for i in range(6)]
    pts += [(x0, round(y0 + (y1 - y0) * i / 6, 3)) for i in range(1, 6)]
    pts += [(x1, round(1.5 + 5.2 + VE.PAAR * j, 3)) for j in range(5)]
    return pts
def mk_ring(s, name, idee):
    og1 = [OG]; st = [(s, s, 26.0 - s, 30.0 - s)]; eg = [EG]
    rooms = [("Kern", (1.0, 1.5, 5.0, 11.0), "core"), ("Gastraum", (5.0, 1.5, 21.0, 15.0), "dining"), ("Gastraum", (1.0, 11.0, 5.0, 15.0), "dining"), ("Küche / Lager / WC", (1.0, 15.0, 21.0, 22.0), "kitchen"), ("Büro / Technik", (1.0, 22.0, 21.0, 28.5), "office")]
    gastro = sum((r[2] - r[0]) * (r[3] - r[1]) for n, r, c in rooms if c == "dining")
    skip = (5, 8); stalls = [(21.0, round(1.5 + VE.PAAR * (k // 2) + 2.5 * (k % 2), 3), 26.0, round(4.0 + VE.PAAR * (k // 2) + 2.5 * (k % 2), 3)) for k in range(10) if k not in skip]
    return dict(name=name, kurz=name.split(" – ")[0], farbe="#0F766E", idee=idee, Z=ZE, eg=eg, og1=og1, st=st, eg_raeume=rooms, wohn_orient="y",
                wohn={"og1": (0.0, 4.0, 26.0, 30.0), "st": (s, 4.0 + s, 26.0 - s, 30.0 - s)}, saeulen="x", saeulen_pts=cols_ring(), balkone="keine", vordach=False,
                bruestung=([] if s == 0 else [(0.0, 0.0, 26.0, 0.0), (0.0, 30.0, 26.0, 30.0), (0.0, 0.0, 0.0, 30.0), (26.0, 0.0, 26.0, 30.0)]), st_mat=("klinker" if s == 0 else "holz"),
                stalls=stalls, stalls_row1=stalls, stalls_row2=[], stalls_par=[], stall_face={"row1": "E"}, asphalt=(21.0, 0.0, 32.0, 30.0), glas_front=(5.0, 21.0, 1.5),
                gastro_m2=gastro, terr_m2=21.0 * 1.5, zufahrt=(26.0, 30.0, 32.0, 30.0), zufahrt_dir="S", fahrgasse=(26.0, 0.0, 32.0, 30.0), plot=VE.PLOT_POLY, staffel_ruecksprung=s, schnitt_achse="x", schnitt_pos=15.0, ortho_cy=14.0, ortho_w=36.0,
                eingaenge=[("Hintereingang/Anlieferung", (21.0, 15.2, 23.5, 17.7)), ("Büro-Eingang", (21.0, 22.9, 23.5, 25.4)), ("Gastro-Eingang (Platz)", (8.0, 0.0, 14.0, 1.5)), ("Kern/Wohnzugang (Platz)", (1.0, 0.0, 5.0, 1.5))], wohn_kern="Kern-Streifen y 0…4 m (4 m über die volle Breite)")
VA.V["R1"] = mk_ring(0.0, "R1 – EG 540 m², Vorbau ringsum, oberstes Geschoss bündig", "EG 20 × 27 m = 540 m² (60 % der Hypothese 960 m²); 1. und 2. OG 26 × 30 m kragen ringsum aus (West 1,0 / Platz 1,5 / Rück 1,5 / Ost 5,0 m über der Stellplatzreihe) und sind deckungsgleich bis zur Attika.")
VA.V["R2"] = mk_ring(1.5, "R2 – EG 540 m², Vorbau ringsum, Staffel 1,50 m", "Wie R1, das oberste Geschoss springt rundum 1,50 m hinter die Kante des 1. OG zurück (umlaufende Dachterrasse).")
VA.V["R3"] = mk_ring(3.0, "R3 – EG 540 m², Vorbau ringsum, Staffel 3,00 m", "Wie R1, das oberste Geschoss springt rundum 3,00 m hinter die Kante des 1. OG zurück (breite Dachterrasse).")
