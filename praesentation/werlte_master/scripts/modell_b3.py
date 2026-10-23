"""Verbindliches Gebäudemodell Baufeld 3, B3 / Alternative K, Version v4 (nach Freigabe der Korrekturen vom 23.10.2026) – reine Python-Geometrie (ohne Blender), eine Quelle für
 * scripts/blender_modell_v3.py (3D-Modell und Renderings, liest dieses Modul),
 * scripts/pruefe_modell_gegen_blatt14.py und scripts/pruefe_modell_gegen_plan.py (Plan-Ist-Abgleich).
Koordinaten in Metern: x West->Ost (Kernseite x = 0), y Platzfassade->Rückseite, z oben (±0,00 = Oberkante Erdgeschossfußboden, Höhenbezug laut Blatt 14).
Jede Öffnung trägt ein Feld `status` und `quelle`:
   plan     = in Blatt 14 (Ursprungsansicht Variante B, varianten_v2/14_Variante_B_Ansichten, PDF Varianten_v2_ABC_Gesamt.pdf S. 4) an dieser Stelle gezeichnet (Lage; Maße dort 'schematisch, offen')
   vorschlag= nur im Entwurfsvorschlag Blatt 25 (varianten_v3/25_Fassadenkonzept_Ansichten), nicht in Blatt 14, nicht in den Grundrissen; wird in der plangetreuen Fassung NICHT gebaut
   konzept  = konzeptionelle Gestaltung ohne Planmaß
Variante 'plangetreu' (Standard) baut nur plan + konzept; Variante 'vorschlag' ergänzt die Blatt-25-Seitenfenster und ist in allen Bildern als Gestaltungsvorschlag zu kennzeichnen."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = json.load(open(os.path.join(ROOT, "geometry", "variant_B3.json"))); V = D["variants"]["K"]
Y1, Y2 = V["depth_L1"], V["y2"]
MODEL_VERSION = "v4"
HOEHE_MAX_ZULAESSIG = 12.0     # Bestätigung des Auftraggebers 23.10.2026; Höhenbezug/Messregel der Stadt unbestätigt (C-03)
MAX_GESCHOSSE = 3              # EG, 1. OG, Staffelgeschoss (Bestätigung des Auftraggebers 23.10.2026)
def boxes():
    """Baukörper aus der Geometriedatei (VB3 boxes)"""
    return [dict(name=b["n"], mat=b["m"], x=tuple(b["x"]), y=tuple(b["y"]), z=tuple(b["z"])) for b in V["boxes"]]
def bands():
    """Betonband 0,30 m an der Oberkante jedes Klinkerkörpers. Status: konzeptionelle Gestaltung (Blatt 25, Referenzbild ki_aussen), in Blatt 14 nicht gezeichnet"""
    return [dict(name="Band-" + b["name"], mat="beton", x=b["x"], y=b["y"], z=(b["z"][1] - 0.3, b["z"][1]), status="gestaltung") for b in boxes() if b["mat"] == "klinker"]
def attika():
    return [dict(name="Attika-" + b["name"], mat="attika", x=b["x"], y=b["y"], z=(9.6, 9.9)) for b in boxes() if b["name"].startswith("L2")]
def openings(variante="plangetreu"):
    """Öffnungen: side ('-y' Platz, '+y' Rückseite, '-x' Kernseite, '+x' Ostseite), a = Koordinate entlang der Fassade (x bzw. y), pos = Wandebene, kind glas|tuer, frame stahl|holz, div = gleichmäßige Felder (nur Fenster, nie bei der EG-Verglasung)"""
    O = []
    def op(side, a0, a1, z0, z1, pos, kind, frame, div, tag, status, quelle):
        O.append(dict(side=side, a=(a0, a1), z=(z0, z1), pos=pos, kind=kind, frame=frame, div=div, tag=tag, status=status, quelle=quelle))
    # Platzseite (y = 0)
    op("-y", 4.0, 32.0, 0.0, 3.1, 0.0, "glas", "stahl", 1, "EG-Verglasung", "plan", "B14 Glasfläche x 4–32; BD RESTAURANT-FRONT-001; Rahmenteilung siehe rahmenteilung()")
    op("-y", 17.0, 19.0, 0.0, 2.4, 0.0, "tuer", "stahl", 1, "Doppeltür Gastro", "plan", "B14, BD DOOR-GF-REST-001, B3p")
    op("-y", 29.5, 31.0, 0.0, 2.4, 0.0, "tuer", "stahl", 1, "Tür Gastro Ost", "plan", "B14, B21 (Fluchtweg)")
    op("-y", 1.0, 2.5, 0.0, 2.4, 0.0, "glas", "stahl", 1, "Eingang Kern", "plan", "B14, BD DOOR-GF-RES-001")
    for i in range(5): x0 = 4 + 5.6 * i; op("-y", x0 + 0.9, x0 + 4.7, 3.9, 6.1, 0.0, "glas", "stahl", 2, f"OG1-Fenster-{i + 1}", "plan", "B14, B4 (Lage; Maße offen)")
    for r in V["rooms"]:
        if r["id"].startswith("WE-L2-V"): x0, x1 = r["rect"][0], r["rect"][2]; op("-y", x0 + 1.0, x1 - 1.0, 6.9, 9.0, 0.8, "glas", "holz", 2, "Staffel-" + r["id"], "plan", "B14, B4 (Lage; Maße offen)")
    # Rückseite (Korrektur 2 und 3): Staffelfenster z 6,90–9,00 wie Blatt 14; dritte EG-Tür x 1–2,5 entfernt (offen bis Bürozugang entschieden)
    for a, b in ((5.0, 6.5), (15.0, 16.5)): op("+y", a, b, 0.0, 2.4, 18.0, "glas", "stahl", 1, "EG-hinten", "plan", "B14 Rückseite")
    for r in V["rooms"]:
        if r["id"].startswith("WE-L1-H"): x0 = r["rect"][0]; op("+y", x0 + 1.6, x0 + 5.4, 3.9, 6.1, Y1, "glas", "stahl", 2, "OG1-hinten-" + r["id"], "plan", "B14 Rückseite")
        if r["id"].startswith("WE-L2-H"): x0 = r["rect"][0]; op("+y", x0 + 1.6, x0 + 7.4, 6.9, 9.0, Y2, "glas", "holz", 2, "Staffel-hinten-" + r["id"], "plan", "B14 Rückseite (z 6,90–9,00)")
    # Ostseite: Tür EG ist in Blatt 14 gezeichnet
    op("+x", 15.5, 16.7, 0.0, 2.4, 32.0, "tuer", "stahl", 1, "Ost-Tür-EG", "plan", "B14 Ostseite")
    # Seitenfenster: nur Gestaltungsvorschlag Blatt 25 (Kernseite: Schlitze im Treppenraum y 4,5–9,5; Ostseite: Gangende y 9,5–11,5)
    if variante == "vorschlag":
        op("-x", 6.5, 7.5, 0.9, 3.0, 0.0, "glas", "stahl", 1, "Kern-EG", "vorschlag", "nur B25 (ASSUMED)")
        op("-x", 6.5, 7.5, 3.9, 6.1, 0.0, "glas", "stahl", 1, "Kern-OG1", "vorschlag", "nur B25 (ASSUMED)")
        op("-x", 6.5, 7.5, 6.9, 9.1, 0.8, "glas", "holz", 1, "Kern-Staffel", "vorschlag", "nur B25 (ASSUMED)")
        op("+x", 9.5, 11.5, 4.4, 6.0, 32.0, "glas", "stahl", 1, "Ost-OG1", "vorschlag", "nur B25 (ASSUMED)")
        op("+x", 9.5, 11.5, 7.4, 9.0, 31.2, "glas", "holz", 1, "Ost-Staffel", "vorschlag", "nur B25 (ASSUMED)")
    return O
def rahmenteilung():
    """Konzeptionelle dunkle Rahmenteilung der EG-Verglasung (Korrektur 1): bewusst UNREGELMÄSSIG, kein Rastermaß, keine Planangabe (Blatt 14/4/25 zeigen eine glatte Glasfläche; Tragwerk/Fassadenstützen C-16 offen)."""
    return dict(x=[6.3, 9.1, 11.2, 14.6, 21.9, 24.3, 27.4], status="konzept", hinweis="konzeptionelle Rahmenteilung, ohne festes Rastermaß, nicht planbestätigt")
def balconies():
    return [dict(name=b["id"], x=(b["rect"][0], b["rect"][2]), y=(-1.5, 0.0)) for b in V["balconies"]]   # Platte z 3,20–3,50; Milchglasbrüstung z 3,50–4,60
def roof_terrace():
    x0, y0, x1, y1 = V["roof_terrace"]
    return dict(x=(x0, x1), y=(y0, y1), z=6.5, belag="neutral grau (Belag im Plan nicht festgelegt, Korrektur 4)", bruestung_hinten="plan (B13/B14: Milchglas 1,10 m)", bruestung_seitlich="gestaltung (nur B25, nicht abschließend planbestätigt)")
def shaft():
    """Küchenabluftschacht laut Grundrissen (B13/B23, VB3 SHAFT-KITCHEN) – bleibt im Modell; der Dachaustritt ist offen (C-22) und wird nicht gebaut."""
    s = V["shaft"]; return dict(id=s["id"], rect=tuple(s["rect"]), levels=s["levels"], dachaustritt="OFFEN: in Blatt 14 'nicht dargestellt' (C-22); nur B25 skizziert einen Stutzen, Lage/Höhe unbelegt")
def vordach():
    return dict(name="Stahlvordach Terrasse", x=(6.0, 30.0), y=(-3.6, 0.0), z=(3.0, 3.1), status="ASSUMED", quelle="BD CANOPY-001 (6,0/−3,6/30,0/0,0, Unterseite +3,00), B3p, B4, B13/B23, B14, B21; Konstruktion (Stützen/Abhängung) nicht belegt – keine ergänzt")
def stalls():
    return V["parking"]["stalls"]
def hoehenpruefung():
    """Gebäudehöhe gegen die zulässige Höhe (Auftraggeber: max. 12,00 m) und Geschosszahl; nutzt die Geometriedatei"""
    attika_top = max(a["z"][1] for a in attika()); zmax = max(attika_top, max(b["z"][1] for b in boxes())); traufe = 6.5
    geschosse = 3
    return dict(attika_oberkante=attika_top, hoechster_bauteilpunkt_ohne_aufbauten=zmax, traufe=traufe, zulaessig=HOEHE_MAX_ZULAESSIG, differenz=round(HOEHE_MAX_ZULAESSIG - attika_top, 2), geschosse=geschosse, geschosse_max=MAX_GESCHOSSE,
                eingehalten=attika_top <= HOEHE_MAX_ZULAESSIG and geschosse <= MAX_GESCHOSSE)
