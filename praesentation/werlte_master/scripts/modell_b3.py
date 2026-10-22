"""Verbindliches Gebäudemodell Baufeld 3, B3 / Alternative K – reine Python-Geometrie (ohne Blender), eine Quelle für
 * scripts/blender_modell_v3.py (3D-Modell und Renderings) und
 * scripts/pruefe_modell_gegen_plan.py (Prüfung gegen Blatt 25 und die Geometriedatei).
Quellen: geometry/variant_B3.json (Baukörper, Balkone, Dachterrasse, Stellplätze, Räume) und die Öffnungsregeln der Ansichten von Blatt 25
(scripts/present/variants3_sheets.py, elev3). Koordinaten in Metern: x West->Ost (Kernseite x=0), y Platzfassade->Rückseite, z oben.
Alle Öffnungsmaße sind laut Blatt 25 'Vorschlag (ASSUMED), nicht freigegeben'."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = json.load(open(os.path.join(ROOT, "geometry", "variant_B3.json"))); V = D["variants"]["K"]
Y1, Y2 = V["depth_L1"], V["y2"]
def boxes():
    """Baukörper aus der Geometriedatei: (name, material, x0, x1, y0, y1, z0, z1)"""
    out = []
    for b in V["boxes"]: out.append(dict(name=b["n"], mat=b["m"], x=tuple(b["x"]), y=tuple(b["y"]), z=tuple(b["z"])))
    return out
def bands():
    """Betonband 0,30 m an der Oberkante jedes Klinkerkörpers (Blatt 25: Betonband auf allen Seiten, bündig mit der Wand)"""
    return [dict(name="Band-" + b["name"], mat="beton", x=b["x"], y=b["y"], z=(b["z"][1] - 0.3, b["z"][1])) for b in boxes() if b["mat"] == "klinker"]
def attika():
    return [dict(name="Attika-" + b["name"], mat="attika", x=b["x"], y=b["y"], z=(9.6, 9.9)) for b in boxes() if b["name"].startswith("L2")]
def openings():
    """Öffnungen: side ('-y' Platz, '+y' Rückseite, '-x' Kernseite, '+x' Ostseite), a = Koordinate entlang der Fassade (x bzw. y), pos = Lage der Wandebene, kind: glas|tuer, frame: stahl|holz, div = Felder"""
    O = []
    def op(side, a0, a1, z0, z1, pos, kind="glas", frame="stahl", div=1, tag=""): O.append(dict(side=side, a=(a0, a1), z=(z0, z1), pos=pos, kind=kind, frame=frame, div=div, tag=tag))
    # Platzseite (y = 0): EG-Verglasung x 4–32 bis 3,10 m, zwei Türen, Eingang Kern
    op("-y", 4.0, 32.0, 0.0, 3.1, 0.0, "glas", "stahl", 20, "EG-Verglasung")
    op("-y", 17.0, 19.0, 0.0, 2.4, 0.0, "tuer", "stahl", 1, "Doppeltür Gastro")
    op("-y", 29.5, 31.0, 0.0, 2.4, 0.0, "tuer", "stahl", 1, "Tür Gastro Ost")
    op("-y", 1.0, 2.5, 0.0, 2.4, 0.0, "glas", "stahl", 1, "Eingang Kern")
    for i in range(5): x0 = 4 + 5.6 * i; op("-y", x0 + 0.9, x0 + 4.7, 3.9, 6.1, 0.0, "glas", "stahl", 2, f"OG1-Fenster-{i + 1}")
    for r in V["rooms"]:
        if r["id"].startswith("WE-L2-V"): x0, x1 = r["rect"][0], r["rect"][2]; op("-y", x0 + 1.0, x1 - 1.0, 6.9, 9.0, 0.8, "glas", "holz", 2, "Staffel-" + r["id"])
    # Rückseite
    for a, b in ((5.0, 6.5), (15.0, 16.5), (1.0, 2.5)): op("+y", a, b, 0.0, 2.4, 18.0, "glas", "stahl", 1, "EG-hinten")
    for r in V["rooms"]:
        if r["id"].startswith("WE-L1-H"): x0 = r["rect"][0]; op("+y", x0 + 1.6, x0 + 5.4, 3.9, 6.1, Y1, "glas", "stahl", 2, "OG1-hinten-" + r["id"])
        if r["id"].startswith("WE-L2-H"): x0 = r["rect"][0]; op("+y", x0 + 1.6, x0 + 7.4, 6.6, 9.1, Y2, "glas", "holz", 2, "Staffel-hinten-" + r["id"])
    # Kernseite (x = 0): Schlitzfenster Treppenhaus
    op("-x", 6.5, 7.5, 0.9, 3.0, 0.0, "glas", "stahl", 1, "Kern-EG"); op("-x", 6.5, 7.5, 3.9, 6.1, 0.0, "glas", "stahl", 1, "Kern-OG1"); op("-x", 6.5, 7.5, 6.9, 9.1, 0.8, "glas", "holz", 1, "Kern-Staffel")
    # Ostseite (x = 32): Fenster am Gangende (Mittelgang y 9,5–11,5), Tür EG y 15,5–16,7 (so in Blatt 25 gezeichnet)
    op("+x", 9.5, 11.5, 4.4, 6.0, 32.0, "glas", "stahl", 1, "Ost-OG1"); op("+x", 9.5, 11.5, 7.4, 9.0, 31.2, "glas", "holz", 1, "Ost-Staffel"); op("+x", 15.5, 16.7, 0.0, 2.4, 32.0, "tuer", "stahl", 1, "Ost-Tür-EG")
    return O
def balconies():
    return [dict(name=b["id"], x=(b["rect"][0], b["rect"][2]), y=(-1.5, 0.0)) for b in V["balconies"]]   # Platte z 3,20–3,50; Milchglasbrüstung z 3,50–4,60
def roof_terrace():
    x0, y0, x1, y1 = V["roof_terrace"]; return dict(x=(x0, x1), y=(y0, y1), z=6.5)    # Brüstung Milchglas 1,10 m an Rück-, Ost- und Westkante
def flue():
    return dict(name="Abluftstutzen (C-22, Lage offen)", x=(30.025, 30.775), y=(11.725, 12.475), z=(9.9, 10.8))
def vordach():
    return dict(name="Stahlvordach Terrasse (C-18, nicht in Blatt-25-Ansicht)", x=(6.0, 30.0), y=(-3.6, 0.0), z=(3.0, 3.1))
def stalls():
    return V["parking"]["stalls"]
