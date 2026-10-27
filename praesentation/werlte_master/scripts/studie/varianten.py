"""Entwurfsstudie Gebäudekonzepte Baufeld 3: Variantendefinitionen und abgeleitete Kennzahlen (gemeinsames Modell je Variante).
Alle Ansichten, Grundrisse und der Schnitt einer Variante werden aus den Daten dieser Datei erzeugt (blender_studie.py, zeichne_plaene.py). KEINE Variante ist festgelegt; alle Werte vorläufig.
Koordinaten in m: x West->Ost (Kern bei x 0–4), y Platzfassade (0) -> Rückseite, z oben; ±0,00 = Oberkante Erdgeschossfußboden. Grundstück 32 x 30 m = Hypothese H1 (960 m², Zuschnitt unbestätigt).
Wohnflächenmethode (kalibriert an B3): Wohnfläche netto = 0,88 x Brutto der Wohnstreifen; Wohnstreifen = Geschossfläche östlich des Kerns (x ab 4) abzüglich 2,0 m Mittelgang, je zur Hälfte vorn/hinten. Dieselbe Methode ergibt für B3 exakt 468,2 m² (1. OG) und 377,8 m² (Staffel)
und 9 + 7 Wohnungen mit Modul 5,6 m (vorn) / 7,0 m (hinten). Alles Flächenwerte sind VORLÄUFIG, bis Grundrisse ausgearbeitet sind."""
import json, os, math
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
B3 = json.load(open(os.path.join(ROOT, "geometry", "variant_B3.json")))["variants"]["K"]
B3M = json.load(open(os.path.join(ROOT, "geometry", "variants3_metrics.json")))["K"]
PLOT = (0.0, 0.0, 32.0, 30.0); PLOT_AREA = 960.0
Z = {"EG": (0.0, 3.5), "OG1": (3.5, 6.5), "ST": (6.5, 9.6), "ATT": (9.6, 9.9)}
HOEHE_MAX = 12.0; GRZ_THEOR = 0.6; NETTO = 0.88; GANG = 2.0
V = {
 "A": dict(name="A – Referenz B3 (rückwärtige Erweiterung)", kurz="Referenz B3", farbe="#1F6F8B",
   idee="Bisheriger Entwurf B3: 1. OG 3,00 m nach hinten ausgekragt (ohne Stützen), Staffelgeschoss 0,80 m zurückgesetzt, fünf Balkone zum Platz.",
   eg=[(0, 0, 32, 18)], og1=[(0, 0, 32, 18), (4, 18, 32, 21)], st=[(0.8, 0.8, 31.2, 17.2), (4.2, 17.2, 31.2, 18.7)], wohn={"og1": (4, 0, 32, 21), "st": (4.2, 0.8, 31.2, 18.7)}, saeulen="keine", balkone="front", vordach=True, bruestung=[(4, 21, 32, 21), (32, 18.7, 32, 21), (4, 18.7, 4, 21)]),
 "B": dict(name="B – Umlaufender Vorbau mit Säulen", kurz="Umlaufender Vorbau", farbe="#B45309",
   idee="1. OG kragt rundum 1,50 m (vorn, Seiten) bzw. 3,00 m (hinten) über das Erdgeschoss aus; Säulenreihe am Rand der Auskragung (Arkade), Staffelgeschoss 1,50 m hinter der Kante des 1. OG, rundum Dachterrasse.",
   eg=[(0, 0, 32, 18)], og1=[(-1.5, -1.5, 33.5, 21)], st=[(0, 0, 32, 19.5)], wohn={"og1": (4, -1.5, 33.5, 21), "st": (4, 0, 32, 19.5)}, saeulen="rand_og1", balkone="keine", vordach=False, bruestung=[(-1.5, -1.5, 33.5, -1.5), (-1.5, 21, 33.5, 21), (-1.5, -1.5, -1.5, 21), (33.5, -1.5, 33.5, 21)]),
 "C": dict(name="C – Maximierung der Wohnfläche", kurz="Maximale Wohnfläche", farbe="#7C3AED",
   idee="1. OG kragt vorn/seitlich 1,50 m und hinten 6,00 m aus (Stellplätze vollständig überdeckt), Säulen am Rand; Staffelgeschoss nur 0,80 m zurückgesetzt und damit fast so groß wie das 1. OG.",
   eg=[(0, 0, 32, 18)], og1=[(-1.5, -1.5, 33.5, 24)], st=[(-0.7, -0.7, 32.7, 23.2)], wohn={"og1": (4, -1.5, 33.5, 24), "st": (4.2, -0.7, 32.7, 23.2)}, saeulen="rand_og1", balkone="keine", vordach=False, bruestung=[(-1.5, -1.5, 33.5, -1.5), (-1.5, 24, 33.5, 24), (-1.5, -1.5, -1.5, 24), (33.5, -1.5, 33.5, 24)]),
 "D": dict(name="D – Kompakt ohne Auskragung (Vergleichsbasis)", kurz="Kompakt", farbe="#4D7C0F",
   idee="Ergänzende Variante: Erdgeschoss und 1. OG deckungsgleich 32 x 18 m, Staffelgeschoss 0,80 m zurückgesetzt, keine Auskragung, keine Säulen; Vergleichsbasis nahe der theoretischen GRZ-Fläche.",
   eg=[(0, 0, 32, 18)], og1=[(0, 0, 32, 18)], st=[(0.8, 0.8, 31.2, 17.2)], wohn={"og1": (4, 0, 32, 18), "st": (4.2, 0.8, 31.2, 17.2)}, saeulen="keine", balkone="front", vordach=True, bruestung=[]),
}
def rects_area(rs): return sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in rs)
def bbox(rs): return (min(r[0] for r in rs), min(r[1] for r in rs), max(r[2] for r in rs), max(r[3] for r in rs))
def saeulen(v):
    if "saeulen_pts" in v: return v["saeulen_pts"]
    if v["saeulen"] != "rand_og1": return []
    x0, y0, x1, y1 = bbox(v["og1"]); pts = []
    def edge(a, b, n):
        for i in range(n + 1): pts.append((round(a[0] + (b[0] - a[0]) * i / n, 3), round(a[1] + (b[1] - a[1]) * i / n, 3)))
    nx = math.ceil((x1 - x0) / 5.6); ny = math.ceil((y1 - y0) / 5.6)
    edge((x0, y0), (x1, y0), nx); edge((x0, y1), (x1, y1), nx)
    for i in range(1, ny): pts.append((x0, round(y0 + (y1 - y0) * i / ny, 3))); pts.append((x1, round(y0 + (y1 - y0) * i / ny, 3)))
    return pts
MIX = {"standard": (5.6, 7.0, "Standard (Modul 5,6 m vorn / 7,0 m hinten, wie B3)"), "klein": (4.9, 5.6, "mehr kleinere Wohnungen (4,9 / 5,6 m)"), "gross": (7.0, 8.4, "größere Wohnungen (7,0 / 8,4 m)")}
def _wz(v, lvl):
    w = v["wohn"][lvl]; return (w[1], w[0], w[3], w[2]) if v.get("wohn_orient") == "y" else w
def stp_neu(gastro_m2, terr_m2, buero_m2, we_by_mix):
    """Stellplätze getrennt: (1) rechtlich erforderlich nach § 47 NBauO (Wohnen seit 01.07.2024 nicht mehr; Gastro/Büro nach Richtzahlen des Erlasses, Spanne), (2) optional (Komfort/Markt/Vermietung)."""
    seats = gastro_m2 / (280 / 120); tseats = terr_m2 / (64.4 / 44)
    r = dict(sitze_innen=round(seats), sitze_terrasse=round(tseats), buero_m2=round(buero_m2, 1), gastro_m2=round(gastro_m2, 1), terrasse_m2=round(terr_m2, 1),
             gastro_lo=seats / 12, gastro_mid=seats / 10, gastro_hi=seats / 8, buero_lo=buero_m2 / 40, buero_mid=buero_m2 / 35, buero_hi=buero_m2 / 30)
    r["erf_lo"] = r["gastro_lo"] + r["buero_lo"]; r["erf_mid"] = r["gastro_mid"] + r["buero_mid"]; r["erf_hi"] = r["gastro_hi"] + r["buero_hi"]
    r["erf_mit_terrasse_mid"] = (seats + tseats) / 10 + r["buero_mid"]; r["erf_mit_terrasse_hi"] = (seats + tseats) / 8 + r["buero_hi"]; r["wohnen_erforderlich"] = 0
    r["optional"] = {m: dict(lo=0.5 * w, mid=1.0 * w, hi=1.5 * w) for m, w in we_by_mix.items()}
    r["komfort_ziel"] = {m: r["erf_mid"] + 1.0 * w for m, w in we_by_mix.items()}
    return r
def wohnstreifen(w, mv, mh):
    xs, y0, x1, y1 = w; L = x1 - xs; D = y1 - y0; d = (D - GANG) / 2; nf = int(L // mv); nr = int(L // mh)
    f = [round((L / nf) * d * NETTO, 1) for _ in range(nf)] if nf else []; r = [round((L / nr) * d * NETTO, 1) for _ in range(nr)] if nr else []
    return dict(laenge=L, tiefe=D, streifentiefe=round(d, 2), vorn=f, hinten=r, brutto=round(L * (D - GANG), 1), netto=round(L * (D - GANG) * NETTO, 1), tiefe_breite_max=round(max([d / (L / nf) if nf else 0, d / (L / nr) if nr else 0]), 2))
def kennzahlen(key):
    v = V[key]; k = dict(key=key, name=v["name"], idee=v["idee"], farbe=v["farbe"])
    k["flaeche"] = {l: round(rects_area(v[l]), 1) for l in ("eg", "og1", "st")}
    for l in ("eg", "og1", "st"): b = bbox(v[l]); k.setdefault("aussenmasse", {})[l] = [round(b[2] - b[0], 2), round(b[3] - b[1], 2)]
    allr = v["eg"] + v["og1"] + v["st"]; bb = bbox(allr)
    # Grundfläche: Projektion der Vereinigung aller Geschosse (grob: Summe der Rechtecke EG/OG1, ohne Überdeckungsabzug – nur wo sie sich nicht überlappen)
    proj = rects_area(v["og1"]) if v["og1"] != v["eg"] else rects_area(v["eg"])
    proj = max(proj, rects_area(v["eg"])); k["projektion_m2"] = round(proj, 1); k["grz_eg"] = round(rects_area(v["eg"]) / PLOT_AREA, 3); k["grz_projektion"] = round(proj / PLOT_AREA, 3)
    k["ueber_grundstueck"] = dict(west=round(max(0, PLOT[0] - bb[0]), 2), ost=round(max(0, bb[2] - PLOT[2]), 2), platz=round(max(0, PLOT[1] - bb[1]), 2), rueck=round(max(0, bb[3] - PLOT[3]), 2))
    k["saeulen"] = saeulen(v); k["anzahl_saeulen"] = len(k["saeulen"])
    k["mix"] = {}
    for m, (mv, mh, lab) in MIX.items():
        o = wohnstreifen(_wz(v, "og1"), mv, mh); s = wohnstreifen(_wz(v, "st"), mv, mh); alle = o["vorn"] + o["hinten"] + s["vorn"] + s["hinten"]
        k["mix"][m] = dict(label=lab, og1=o, st=s, we=len(alle), we_og1=len(o["vorn"]) + len(o["hinten"]), we_st=len(s["vorn"]) + len(s["hinten"]), wfl=round(o["netto"] + s["netto"], 1), kleinste=min(alle) if alle else 0, groesste=max(alle) if alle else 0, mittel=round(sum(alle) / len(alle), 1) if alle else 0)
    s = k["mix"]["standard"]; k["wfl"] = s["wfl"]; k["we"] = s["we"]
    vv = V[key]; k["stp"] = stp_neu(vv.get("gastro_m2", 280.0), vv.get("terr_m2", 64.4), vv.get("buero_m2", B3M["buero_netto"]), {m: k["mix"][m]["we"] for m in MIX}); k["stp_nachweisbar_H1"] = 11
    k["stp_bedarf"] = k["stp"]["komfort_ziel"]  # nur Rückwärtskompatibilität: Komfortziel = erforderlich (Mittel) + 1,0/WE, KEINE gesetzliche Pflicht
    k["bgf"] = round(k["flaeche"]["eg"] + k["flaeche"]["og1"] + k["flaeche"]["st"], 1)
    za = V[key].get("Z", Z)["ATT"][1]; k["hoehe"] = dict(attika=za, zulaessig=HOEHE_MAX, differenz=round(HOEHE_MAX - za, 2), geschosse=3)
    k["staffel_anteil"] = round(rects_area(v["st"]) / rects_area(v["og1"]), 3)
    return k
def alle(): return {key: kennzahlen(key) for key in V}
if __name__ == "__main__":
    d = alle(); json.dump(d, open(os.path.join(ROOT, "studie_gebaeudeformen", "varianten_daten.json"), "w"), indent=1, ensure_ascii=False)
    for key, k in d.items():
        s = k["mix"]["standard"]; print(key, "BGF", k["bgf"], "Wfl", s["wfl"], "WE", s["we"], (s["we_og1"], s["we_st"]), "Säulen", k["anzahl_saeulen"], "GRZ_proj", k["grz_projektion"], "stp", k["stp_bedarf"]["standard"], "über", k["ueber_grundstueck"], "kl/gr/mittel", s["kleinste"], s["groesste"], s["mittel"], "Tiefe/Breite", s["og1"]["tiefe_breite_max"], "Staffel%", k["staffel_anteil"])
        for m in ("klein", "gross"): mm = k["mix"][m]; print("   ", m, mm["we"], mm["wfl"], mm["kleinste"], mm["groesste"])
    print("B3 Referenz:", B3M["wfl_L1"], B3M["wfl_L2"], B3M["we"])

import varianten_e  # registriert E1–E4 in V
import varianten_f  # registriert F1–F4 in V
import varianten_g  # registriert G1–G3 (Baufeld 3 / MI 3)
import varianten_r  # registriert R1–R3 (EG 540 m², Vorbau ringsum)
