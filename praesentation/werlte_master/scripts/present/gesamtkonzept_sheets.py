"""Gesamtkonzept B3: Flächen- und Wohnungsübersicht (Blatt 31), Dachaufsicht und Schnitt B–B (Blatt 32). Quelle: geometry/variant_B3.json."""
import sys, os, json
from lib import *
import variants3_sheets as V3
import variants2_sheets as V2
D3 = V3.D3; VK = V3.VK; MK = V3.MK; NET = D3["net_factor"]
OUT = os.path.join(ROOT, "gesamtkonzept"); os.makedirs(OUT, exist_ok=True)
def save(s, name):
    err = s.check(); assert not err, "\n".join(err)
    open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(s.svg().replace("Stand 22.10.2026 · Modell NEUE_MITTE_MASTER_DRAFT_A_003", V3.STAMP)); print("geschrieben", name)

def sheet31():
    s = Sheet(); drawing_title(s, "Flächen- und Wohnungsübersicht", "Gesamtkonzept B3 (Variante B, Büro-Alternative K) · Brutto aus der Geometrie, Netto = Brutto × 0,88 (Annahme) · alle Flächen hypothetisch")
    rooms = sorted([r for r in VK["rooms"] if r["type"] == "apartment"], key=lambda r: (r["level"], round(r["rect"][1]), r["rect"][0])); n = {"L1": 0, "L2": 0}; rows = [("Nr.", "Geschoss", "Typ", "Brutto m²", "Netto m²", "Außenraum")]; tot_b = tot_n = 0
    TYP = {"WE-L1-V": ("1. OG vorn", "Studio", "Balkon 2,70 × 1,50 m"), "WE-L1-H": ("1. OG hinten", "Zweizimmer", "–"), "WE-L2-V": ("Staffel vorn", "Zweizimmer", "Umlauf 0,80 m"), "WE-L2-H": ("Staffel hinten", "Zweizimmer", "Dachterrasse 20,7 m²")}
    for r in rooms:
        n[r["level"]] += 1; nr = f"{'1' if r['level'] == 'L1' else '3'}.{n[r['level']]:02d}"; g, t, e = TYP[r["id"][:7]]; b = r["area_gross"]; tot_b += b; tot_n += b * NET
        rows.append((nr, g, t, f"{b:.2f}".replace(".", ","), f"{b * NET:.2f}".replace(".", ","), e))
    rows.append(("Summe", "16 Wohnungen", "", f"{tot_b:.2f}".replace(".", ","), f"{tot_n:.2f}".replace(".", ","), ""))
    y = V3.table_block(s, 14, 40.0, [14, 28, 26, 24, 24, 44], rows, 2.9)
    x2 = 190.0; y2 = 40.0
    rows2 = [("Flächenbilanz", "Brutto m²", "Netto m²"), ("EG Gastronomie (Gastraum und Bar 280)", "440,0", "440,0"), ("EG Büros 1 und 2", "64,0", "56,3"), ("EG Büro-Foyer und Büro-WC", "15,6", "–"), ("EG Wohnkern (Halle, Treppe, Flur, Aufzug)", "56,4", "–"), ("Erdgeschoss gesamt", "576,0", ""),
             ("1. Obergeschoss (Wohnen, Kern, Gang)", "660,0", "468,0"), ("Staffelgeschoss (Wohnen, Kern, Gang)", "539,1", "377,9"), ("Bruttogrundfläche gesamt", "1.775,1", ""), ("Wohnfläche gesamt (ohne Balkon und Terrassen)", "", "845,9"), ("Wohnfläche je BGF", "", "47,7 %"),
             ("Brutto-Rauminhalt (Näherung)", "5.667 m³", ""), ("Außenmaß EG / 1. OG / Staffel", "32,0×18,0 / 32,0×21,0 / 30,4×17,9 m", "")]
    y2 = V3.table_block(s, x2, 40.0, [70, 28, 24], rows2, 2.9)
    s.text(x2, y2 + 4, "Gastronomie: Gastraum 280, Küche 60, Lager 27, WC 24, Personal 20, Flur 20, Anlieferung 9 m².", 2.7, fill=GREY)
    s.text(x2, y2 + 8.5, "Innenplätze realistisch ca. 120 (88–128), Terrasse ca. 44 (40–52).", 2.7, fill=GREY)
    assert y < 282 and y2 < 270
    kenn = [("Wohnungen", "16"), ("Wohnfläche netto", "ca. 846 m²"), ("Gastronomie brutto", "440 m²"), ("Büros netto", "ca. 56 m²"), ("BGF", "1.775 m²")]
    offen = [("C-30", "Geschossflächen mit Auskragung hypothetisch: Baufenster, GRZ, Abstände offen."), ("C-38", "Fahrrad- und Abstellraum Wohnen: neuer Ort offen."), ("C-27", "Rollstuhlgerechte Wohnung: Zahl und Lage nicht nachgewiesen.")]
    V3.frame3(s, "Flächen- und Wohnungsübersicht", "Tabelle", kenn, None, offen, ["Die Flächenbilanz ist mit der Wirtschaftlichkeitsrechnung (Excel, Blatt Flächen) identisch.", "Wohnflächen nach Brutto × 0,88; eine Berechnung nach Wohnflächenverordnung (Balkone, Terrassen, Schrägen) steht aus."], 31) if False else frame(s, "Flächen- und Wohnungsübersicht", "Tabelle", kenn, None, offen, ["Die Flächenbilanz ist mit der Wirtschaftlichkeitsrechnung (Excel, Blatt Flächen) identisch.", "Wohnflächen nach Brutto × 0,88; eine Berechnung nach Wohnflächenverordnung (Balkone, Terrassen) steht aus."], 31)
    save(s, "31_Flaechen_Wohnungsuebersicht")

def sheet32():
    s = Sheet(); M = V2.M; v = VK
    drawing_title(s, "Dachaufsicht und Schnitt B–B", "Gesamtkonzept B3 · M 1:250 · Dachterrassen, Abluft und Aufzug schematisch · HYPOTHETISCH, Rechtsfragen offen")
    ox, oy = 24.0, 60.0; X = lambda x: ox + x * M; Y = lambda y: oy + y * M; Y1 = v["depth_L1"]; y2 = v["y2"]
    s.text(ox, 41, "Dachaufsicht", 3.6, weight=600); V2.hatch(s)
    s.poly([(X(a), Y(b)) for a, b in v["outlines"]["L1"]], "#E7E3DA", INK, 0.5)
    t = v["roof_terrace"]; s.rect(X(t[0]), Y(t[1]), (t[2] - t[0]) * M, (t[3] - t[1]) * M, "url(#terr)", "#B49A72", 0.3)
    s.poly([(X(a), Y(b)) for a, b in v["outlines"]["L2"]], "#CDB89A", INK, 0.6)
    for k in (1, 2): s.line(X(4.2 + 9 * k), Y(y2), X(4.2 + 9 * k), Y(Y1), 0.5, "#6B5A3A")
    s.text(X(8.7), Y((y2 + Y1) / 2) + 0.9, "Terrasse 3.05", 2.6, "middle", 600, "#6B5A3A", halo=True); s.text(X(17.7), Y((y2 + Y1) / 2) + 0.9, "Terrasse 3.06", 2.6, "middle", 600, "#6B5A3A", halo=True); s.text(X(26.7), Y((y2 + Y1) / 2) + 0.9, "Terrasse 3.07", 2.6, "middle", 600, "#6B5A3A", halo=True)
    s.line(X(0), Y(0), X(32), Y(0), 1.0, INK)
    sh = v["shaft"]["rect"]; s.rect(X(sh[0]), Y(sh[1]), (sh[2] - sh[0]) * M, (sh[3] - sh[1]) * M, "#F3D98B", INK, 0.3)
    s.text(X(sh[0]) - 1.5, Y(sh[1]) + 1.0, "Abluft", 2.6, "end", 600)
    s.rect(X(0.8), Y(11.5), 2.2 * M, 2.6 * M, "none", INK, 0.4, "1.5 1"); s.text(X(1.9), Y(12.8) + 0.9, "AZ", 2.6, "middle", 600)
    s.text(X(16), Y(6.5) + 0.9, "Dach Staffelgeschoss (Attika 9,90 m)", 2.8, "middle", 600, INK, halo=True)
    s.text(X(16), Y(Y1) + 5, f"Dachterrassen 9,0 × {de(Y1 - y2, 1)} m = 20,7 m² je Wohnung, Milchglas-Brüstung 1,10 m", 2.6, "middle", 400, GREY)
    s.text(X(0.8), Y(11.5) - 2.0, "Aufzugsüberfahrt: Aufbau offen (C-25)", 2.6, "start", 400, GREY)
    # Schnitt B-B
    ox2 = 176.0; s.text(ox2, 41, "Schnitt B–B bei y = 5,00 m (Blick zur Rückseite)", 3.6, weight=600)
    gy = 150.0; Xb = lambda x: ox2 + x * M; Z = lambda z: gy - z * M; YC = 5.0
    zs = {"GF": (0, 3.2), "L1": (3.5, 6.2), "L2": (6.5, 9.3)}; fl = V2.flat_labels(v["rooms"])
    for lv, (z0, z1) in zs.items():
        for r in [r for r in v["rooms"] if r["level"] == lv and r["rect"][1] < YC < r["rect"][3] and r["type"] != "bar"]:
            x0, _, x1, _ = r["rect"]; s.rect(Xb(x0), Z(z1), (x1 - x0) * M, (z1 - z0) * M, FILL.get(r["type"], "#EEE"), GREY, 0.2)
            nm = fl.get(r["id"]) or {"DINING-GF": "Gastraum", "STAIR-GF": "Treppe", "STAIR-L1": "Treppe", "STAIR-L2": "Treppe", "LOBBY-GF": "Halle"}.get(r["id"])
            if nm and tw(nm, 2.6, True) + 1 <= (x1 - x0) * M: s.text(Xb((x0 + x1) / 2), Z((z0 + z1) / 2) + 0.9, nm, 2.6, "middle", 600)
    for z, a, b in ((3.5, 0, 32), (6.5, 0, 32), (9.6, 0.8, 31.2)): s.rect(Xb(a), Z(z), (b - a) * M, 0.3 * M, INK, INK, 0.1)
    s.rect(Xb(0.8), Z(9.9), 0.3 * M, 0.3 * M, INK, INK, 0.1); s.rect(Xb(31.2) - 0.3 * M, Z(9.9), 0.3 * M, 0.3 * M, INK, INK, 0.1)
    s.line(Xb(-1), Z(0), Xb(33), Z(0), 0.9, INK)
    for z, tx in ((0, "±0,00"), (3.5, "+3,50"), (6.5, "+6,50"), (9.6, "+9,60")): s.line(Xb(0) - 9, Z(z), Xb(0) - 3, Z(z), 0.2, GREY, "1.4 1"); s.text(Xb(0) - 10, Z(z) + 0.9, tx, 2.6, "end", 600)
    dim_h(s, Xb(0), Xb(32), gy + 9, "32,00")
    s.text(ox2, gy + 18, "Schnittebene durch Gastraum, Treppe und die vorderen Wohnungen;", 2.6, fill=GREY); s.text(ox2, gy + 22, "die Balkone liegen vor der Ebene.", 2.6, fill=GREY)
    legend = [(V3.sw(FILL["apartment"]), "Wohnung"), (V3.sw(FILL["dining"]), "Gastraum"), (V3.sw(FILL["core"]), "Kern, Treppe"), (lambda s, x, y: (V2.hatch(s), s.rect(x, y, 8, 4, "url(#terr)", "#B49A72", 0.3)), "Dachterrasse (Vorschlag)"), (V3.sw("#F3D98B", INK, 4, 3), "Küchenabluft-Schacht")]
    frame(s, "Dachaufsicht und Schnitt B–B", "Maßstab 1:250 (A3)", [("Dachterrassen", "3 × 20,7 m²"), ("Höhe Attika", "9,90 m")], legend, [("C-39", "Dachterrassen: Brüstung, Dachaufbau, Brand- und Schallschutz offen."), ("C-25", "Aufzugsüberfahrt und Abluftaustritt über Dach offen."), ("C-22", "Abluft-Schacht läuft durch Wohnungen.")], ["Die Terrassen gehören den hinteren Staffelwohnungen 3.05 bis 3.07.", "Keine Rettungsfunktion der Dachterrassen nachgewiesen."], 32)
    save(s, "32_Dachaufsicht_Schnitt_BB")
if __name__ == "__main__":
    for a in sys.argv[1:]: globals()["sheet" + a]()
