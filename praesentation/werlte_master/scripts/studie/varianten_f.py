"""Variante F – Erdgeschoss 540 m² (Planungsziel 24.10.2026): 18 m breit × 30 m lang, Restfläche 420 m² für Zufahrt, Fahrgasse, Stellplätze.
F1–F3: wörtliche Lesart (18 m an der Platzseite × 30 m Tiefe), Staffelrücksprung 0 / 1,5 / 3,0 m. F4: gedrehte Lesart (30 m an der Platzseite × 18 m Tiefe), Staffel 1,5 m.
ABWEICHUNG: Bei 30 m Länge füllt das EG die Grundstückstiefe (H1 32 × 30 m) vollständig; Vorbau vorn ragt 1,5 m über die Grundstücksgrenze zum Platz, hinten ist KEIN Vorbau möglich (Grenze).
Alles Annahme: Grundstück H1, Zufahrt von hinten (Süden) bzw. Osten, Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m, Parallelparker 2,00 × 5,50 m, Säule Ø 0,40 m."""
import math, varianten as VA, varianten_e as VE
ZE = VE.ZE
def cols_literal():
    pts = []; x0, x1, y0, y1 = 0.35, 23.65, -1.15, 29.65
    pts += [(round(x0 + (x1 - x0) * i / 5, 3), y0) for i in range(6)]
    pts += [(x0, round(y0 + (y1 - y0) * i / 6, 3)) for i in range(1, 7)]
    pts += [(x1, y) for y in VE.pair_cols(2.5) + [29.65]]
    return pts
def mk_literal(s, name, idee):
    og1 = [(0.0, -1.5, 24.0, 30.0)]; st = [(s, -1.5 + s, 24.0 - s, 30.0 - s)]; eg = [(1.0, 0.0, 19.0, 30.0)]
    rooms = [("Kern", (1.0, 0.0, 5.0, 9.5), "core"), ("Gastraum", (5.0, 0.0, 19.0, 15.0), "dining"), ("Gastraum", (1.0, 9.5, 5.0, 15.0), "dining"), ("Küche / Lager / WC", (1.0, 15.0, 19.0, 23.0), "kitchen"), ("Büro / Technik", (1.0, 23.0, 19.0, 30.0), "office")]
    gastro = sum((r[2] - r[0]) * (r[3] - r[1]) for n, r, c in rooms if c == "dining")
    skip = (5, 8); stalls = [(19.0, round(2.5 + VE.PAAR * (k // 2) + 2.5 * (k % 2), 3), 24.0, round(5.0 + VE.PAAR * (k // 2) + 2.5 * (k % 2), 3)) for k in range(10) if k not in skip]
    par = [(30.0, round(1.0 + 5.5 * k, 3), 32.0, round(6.5 + 5.5 * k, 3)) for k in range(5)]
    return dict(name=name, kurz=name.split(" – ")[0], farbe="#B91C1C", idee=idee, Z=ZE, eg=eg, og1=og1, st=st, eg_raeume=rooms, wohn_orient="y",
                wohn={"og1": (0.0, 2.5, 24.0, 30.0), "st": (s, 2.5 + (s if s else 0), 24.0 - s, 30.0 - s)}, saeulen="x", saeulen_pts=cols_literal(), balkone="keine", vordach=False,
                bruestung=([] if s == 0 else [(s - s, -1.5, 24.0, -1.5), (0.0, 30.0, 24.0, 30.0), (0.0, -1.5, 0.0, 30.0), (24.0, -1.5, 24.0, 30.0)]), st_mat=("klinker" if s == 0 else "holz"),
                stalls=stalls + par, stalls_row1=stalls, stalls_row2=[], stalls_par=par, stall_face={"row1": "E", "par": "W"}, asphalt=(19.0, 0.0, 32.0, 30.0), glas_front=(5.0, 19.0, 0.0),
                gastro_m2=gastro, terr_m2=24.0 * 1.5, zufahrt=(24.0, 30.0, 30.0, 30.0), zufahrt_dir="S", fahrgasse=(24.0, 0.0, 30.0, 30.0), plot=VE.PLOT_POLY, staffel_ruecksprung=s, schnitt_achse="x", schnitt_pos=15.0, ortho_cy=14.0, ortho_w=36.0,
                eingaenge=[("Hintereingang/Anlieferung", (19.0, 15.8, 21.5, 18.3)), ("Büro-Eingang", (19.0, 24.1, 21.5, 26.6)), ("Gastro-Eingang (Platz)", (8.0, -1.5, 14.0, 0.0)), ("Kern/Wohnzugang (Platz)", (1.0, -1.5, 5.0, 0.0))], wohn_kern="Kern-Streifen y −1,5…2,5 (4 m über volle Breite)")
def mk_gedreht(s, name, idee):
    D = 24.0; og1 = [(0.0, 0.0, 32.0, D)]; st = [(s, s, 32.0 - s, D - s)]; eg = [(1.0, 1.0, 31.0, 19.0)]
    rooms = [("Kern", (1.0, 1.0, 5.0, 10.5), "core"), ("Gastraum", (5.0, 1.0, 31.0, 12.5), "dining"), ("Gastraum", (1.0, 10.5, 5.0, 12.5), "dining"), ("Küche / Lager / WC", (5.0, 12.5, 18.0, 19.0), "kitchen"), ("Büro / Technik", (18.0, 12.5, 31.0, 19.0), "office")]
    gastro = sum((r[2] - r[0]) * (r[3] - r[1]) for n, r, c in rooms if c == "dining")
    stalls = VE.stalls_row(19.0, 2.5, 10, skip=(5,))
    return dict(name=name, kurz=name.split(" – ")[0], farbe="#B91C1C", idee=idee, Z=ZE, eg=eg, og1=og1, st=st, eg_raeume=rooms,
                wohn={"og1": (4, 0, 32, D), "st": (s + 4, s, 32 - s, D - s)}, saeulen="x", saeulen_pts=VE.columns(D), balkone="keine", vordach=False,
                bruestung=([] if s == 0 else [(0, 0, 32, 0), (0, D, 32, D), (0, 0, 0, D), (32, 0, 32, D)]), st_mat=("klinker" if s == 0 else "holz"),
                stalls=stalls, stalls_row1=stalls, stalls_row2=[], stalls_par=[], stall_face={"row1": "S"}, asphalt=(0, 19, 32, 30), glas_front=(5.0, 31.0, 1.0),
                gastro_m2=gastro, terr_m2=30.0, zufahrt=(32.0, 24.0, 32.0, 30.0), zufahrt_dir="E", fahrgasse=(0, 24.0, 32, 30.0), plot=VE.PLOT_POLY, staffel_ruecksprung=s,
                eingaenge=[("Hintereingang/Anlieferung", (15.8, 19.0, 18.3, 21.5)), ("Gastro-Eingang (Arkade)", (8.0, 0.0, 14.0, 1.0)), ("Kern/Wohnzugang", (1.0, 0.0, 5.0, 1.0))])
VA.V["F1"] = mk_literal(0.0, "F1 – EG 18×30 m, Vorbau bis Attika", "Erdgeschoss 18 × 30 m = 540 m² (Platzseite 18 m, Tiefe 30 m = volle Grundstückstiefe); 1. und 2. OG kragen 1,0 m nach Westen, 5,0 m nach Osten (über die Stellplatzreihe) und 1,5 m zum Platz aus und sind deckungsgleich bis zur Attika +12,00 m. Rückseite ohne Vorbau (Grundstücksgrenze).")
VA.V["F2"] = mk_literal(1.5, "F2 – EG 18×30 m, Staffel 1,50 m", "Wie F1, das 2. OG springt rundum 1,50 m zurück (umlaufende Dachterrasse).")
VA.V["F3"] = mk_literal(3.0, "F3 – EG 18×30 m, Staffel 3,00 m", "Wie F1, das 2. OG springt rundum 3,00 m zurück (breite Dachterrasse, kleineres 2. OG).")
VA.V["F4"] = mk_gedreht(1.5, "F4 – EG 30×18 m (gedreht), Staffel 1,50 m", "Gedrehte Lesart der 540 m²: 30 m Platzseite × 18 m Tiefe, Vorbau rundum (vorn 1,0 / seitlich 1,0 / hinten 5,0 m über der Stellplatzreihe), Staffel 1,50 m; wie E2, aber EG 540 statt 492 m².")
