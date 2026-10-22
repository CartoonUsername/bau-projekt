"""Baut die Ausgabestruktur visualisierungen/higgsfield/ (Renderings je Motiv, Qualitätskontrolle als CSV, Präsentations-PDF).
Quelle der Bilder: Blender-Renderings (renderings/tag, nacht, 07_gastro_innenraum) und die daraus veredelten Higgsfield-Bilder (renderings/veredelt). Bestehende Dateien werden nicht gelöscht."""
import os, sys, shutil, csv
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geometrietreue as GT
HF = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "visualisierungen", "higgsfield")); R = os.path.join(HF, "renderings")
MOTIVE = [  # nr, ordner, titel, blender, veredelt, kamera, text, status, abweichung
    ("01", "01_hauptansicht_tag", "Hauptansicht Platzseite (Tag)", "tag/tag_01_front.png", "veredelt/hf_01_front.png", "01_front", "Platzfassade mit großer Gastro-Verglasung im Erdgeschoss, fünf Balkonen am ersten Obergeschoss und zurückgesetztem Staffelgeschoss.", "BESTANDEN",
     "Veredelung lässt Fensterglas leicht Innenraum erkennen; Himmelsrichtung/Platz neutral (C-13); Vordach und Pfostenraster aus dem Platzfassaden-Design, in Blatt 25 nicht gezeichnet (offen)"),
    ("02", "02_hauptansicht_abend", "Hauptansicht Platzseite (Abend)", "nacht/nacht_01_front.png", "veredelt/hf_02_abend.png", "01_front", "Dieselbe Kamera und Geometrie wie die Tagesansicht, nur Licht und Tageszeit verändert.", "BESTANDEN",
     "Einrichtung hinter der Gastro-Verglasung und Vorhänge sind frei ergänzt (nicht planverbindlich); Auswahl der beleuchteten Wohnungsfenster ist Gestaltungsannahme"),
    ("03", "03_rueckansicht", "Rückansicht mit überdachten Stellplätzen", "tag/tag_03_rueck.png", "veredelt/hf_03_rueck.png", "03_rueck", "Rückseite mit 3,00 m Auskragung des ersten Obergeschosses über den Stellplätzen (ohne Stützen) und Dachterrasse vor dem Staffelgeschoss.", "BESTANDEN",
     "Rissbild im Asphalt (kosmetisch) ergänzt; Türen zeigen Innenraum; Stellplatzfläche H1 ist hypothetisch"),
    ("04", "04_westseite", "Westseite (Kernseite)", "tag/tag_04_west.png", "veredelt/hf_04_west.png", "04_west", "Seitenfassade mit Erschließungskern und drei Treppenhausfenstern übereinander.", "BESTANDEN", "keine"),
    ("05", "05_ostseite", "Ostseite", "tag/tag_05_ost.png", "veredelt/hf_05_ost.png", "05_ost", "Seitenfassade mit Fenstern am Gangende, Staffelrücksprung, Dachterrassenbrüstung und Abluftstutzen.", "BESTANDEN", "Abluftstutzen-Lage offen (C-22); Kantentreue der Veredelung etwas geringer (94,6 %), Abweichung nur in Materialtextur"),
    ("06", "06_luftbild", "Luftbild / Gesamtansicht", "tag/tag_06_luft.png", "veredelt/hf_06_luft.png", "06_luft", "Baukörper mit Dachterrasse und elf Stellplätzen auf neutralem Grund; keine Nachbarbebauung dargestellt.", "BESTANDEN", "Umgebung schematisch (Grundstück nicht bestätigt)"),
    ("07", "07_gastro_innenraum", "Gastronomie-Innenraum", "07_gastro_innenraum/tag_07_gastro.png", "veredelt/hf_07_gastro.png", "Innenraum", "Gastraum 28 x 10 m nach Grundriss Blatt 21: Bar am Rückende, Tischreihen, Verglasung zur Platzseite. Möblierung exemplarisch.", "NICHT VERIFIZIERBAR",
     "Raumgeometrie, Tisch- und Barlage stammen aus Blatt 21, Stuhl-/Hockerformen und Details sind modellhaft vereinfacht und von Higgsfield ausgearbeitet; Pfeiler und Glas-Stahl-Trennung sind im Plan nicht vorhanden und fehlen bewusst; nur als konzeptionelles Bild verwenden"),
]
def build():
    rows = []
    for nr, ordner, titel, b, v, kam, text, status, abw in MOTIVE:
        d = os.path.join(R, ordner); os.makedirs(d, exist_ok=True)
        bn = os.path.basename(b); vn = os.path.basename(v)
        shutil.copy(os.path.join(R, b), os.path.join(d, "blender_" + bn)); shutil.copy(os.path.join(R, v), os.path.join(d, "final_" + vn))
        s1, s2 = GT.score(os.path.join(R, b), os.path.join(R, v))
        rows.append(dict(bildnummer=nr, dateiname=f"renderings/{ordner}/final_{vn}", verwendete_modellansicht=f"renderings/{ordner}/blender_{bn} (Kamera {kam})",
                         referenzen="Blender-Modell scripts/modell_b3.py + blender_modell_v3.py; geometry/variant_B3.json; Blatt 25" + ("; Blatt 21 (Möblierung)" if nr == "07" else ""),
                         geometrieprüfung=f"Planprüfung 83/83 Prüfpunkte (Blatt 25); Kantentreue Veredelung: Modellkanten wiedergefunden {s1 * 100:.1f} %, veredelte Kanten im Modell {s2 * 100:.1f} %",
                         materialprüfung="Klinker dunkelrotbraun, Beton, Lärchenholz warmbraun, Milchglas, Stahlrahmen/Holzfenster Staffel: Sichtprüfung gegen Modell bestanden" if nr != "07" else "Olivgrün, Cognac, Bordeaux, Eiche, dunkle Barfront, Messing, Mikrozement: Sichtprüfung gegen Vorgabe",
                         festgestellte_abweichungen=abw, status=status, erforderliche_korrektur="keine" if status == "BESTANDEN" else "Möblierung und Detailformen vom Fachplaner/Bauherrn freigeben lassen; bis dahin als konzeptionell kennzeichnen"))
    rows.append(dict(bildnummer="08", dateiname="-", verwendete_modellansicht="renderings/tag/tag_08_terrasse.png (Modellansicht)", referenzen="Blender-Modell", geometrieprüfung="Modellansicht vorhanden, Veredelung geprüft: Higgsfield zeigte das Deck durch die Fenster der Staffel (unplausibel)",
                     materialprüfung="-", festgestellte_abweichungen="Veredeltes Bild unplausibel, Motiv liefert keinen Mehrwert (Dachterrasse hinter 1,10 m Brüstung kaum sichtbar)", status="NICHT ERSTELLT", erforderliche_korrektur="optional: Terrassenansicht aus anderem Blickwinkel, bei Bedarf"))
    with open(os.path.join(HF, "04_qualitaetskontrolle.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";"); w.writeheader(); w.writerows(rows)
    return rows
W, H = 2339, 1654
F = lambda s, w="Regular": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)
INK, GREY, ACC = "#1B1F24", "#6B7280", "#9A3412"
def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines
def page():
    im = Image.new("RGB", (W, H), "white"); return im, ImageDraw.Draw(im)
def footer(d, n):
    d.text((100, H - 70), "Konzeptionelle Visualisierung · Arbeitsstand B3 (Variante B, nicht freigegeben) · baurechtliche Zulässigkeit und Ausführungsplanung nicht bestätigt", font=F(22), fill=GREY); d.text((W - 160, H - 70), f"{n}", font=F(22), fill=GREY)
def pdf():
    pages = []
    im, d = page(); d.text((150, 560), "Neue Mitte Werlte – Baufeld 3", font=F(86, "Bold"), fill=INK); d.text((150, 690), "Konzeptionelle Visualisierungen", font=F(52), fill=INK); d.text((150, 790), "Gesprächsunterlage für die Hümmlinger Volksbank Werlte", font=F(36), fill=GREY)
    d.text((150, 1330), "Alle Ansichten zeigen dasselbe Gebäude (Arbeitsstand B3), erzeugt aus einem gemeinsamen 3D-Modell.", font=F(28), fill=GREY); footer(d, 1); pages.append(im)
    for i, (nr, ordner, titel, b, v, kam, text, status, abw) in enumerate(MOTIVE):
        im, d = page(); src = Image.open(os.path.join(R, v)).convert("RGB"); k = min((W - 200) / src.width, 1190 / src.height); src = src.resize((int(src.width * k), int(src.height * k)), Image.LANCZOS)
        im.paste(src, ((W - src.width) // 2, 80)); y = 80 + src.height + 40
        d.text((100, y), titel, font=F(40, "SemiBold"), fill=INK); y += 62
        for ln in wrap(d, text, F(25), W - 200): d.text((100, y), ln, font=F(25), fill="#333"); y += 36
        if status != "BESTANDEN": d.text((100, y + 6), "Konzeptionelles Bild: Möblierung und Details exemplarisch, nicht planverbindlich.", font=F(24, "SemiBold"), fill=ACC)
        footer(d, i + 2); pages.append(im)
    im, d = page(); d.text((100, 90), "Planungsstand und Hinweise", font=F(48, "SemiBold"), fill=INK); y = 190
    punkte = ["Arbeitsstand B3 (Variante B, Alternative K), Stand 22.10.2026, vorläufig und nicht freigegeben.",
              "Gebäude 32 x 18 m (EG), 1. Obergeschoss mit 3,00 m Auskragung nach hinten, Staffelgeschoss; Attika +9,90 m. Breite 32 m ist Arbeitsannahme.",
              "16 Wohnungen (9 im 1. Obergeschoss, 7 im Staffelgeschoss), Gastronomie im Erdgeschoss, kompakte Büros hinten.",
              "Geometrie: ein gemeinsames 3D-Modell, maßlich gegen die Ansichten der Planunterlage geprüft (83 von 83 Prüfpunkten). Die Fensterformate der Pläne sind Vorschläge.",
              "Die Bilder wurden aus dem Modell gerendert und anschließend zur Materialdarstellung veredelt; die Veredelung wurde per Kantenvergleich gegen das Modell kontrolliert.",
              "Umgebung und Stellplatzfläche sind schematisch; Grundstück, Himmelsrichtung, Vordach (Blatt 21) und Pfostenraster der Verglasung sind offen. Baurecht, Tragwerk und Förderung sind nicht bestätigt.",
              "Die Wirtschaftlichkeit des Konzepts ist nach dem bisherigen Rechenstand in allen Szenarien nicht tragfähig (siehe separate Unterlage)."]
    for p in punkte:
        for j, ln in enumerate(wrap(d, p, F(28), W - 260)): d.text((130 if j else 100, y), ("• " if j == 0 else "") + ln, font=F(28), fill="#222"); y += 42
        y += 18
    footer(d, 9); pages.append(im)
    im, d = page(); d.text((100, 80), "Geometrienachweis: Modell über Planansicht (Blatt 25, M 1:250)", font=F(40, "SemiBold"), fill=INK)
    names = [("front", "Platzseite"), ("rear", "Rückseite"), ("west", "Kernseite"), ("east", "Ostseite")]
    for i, (k, t) in enumerate(names):
        ov = Image.open(os.path.join(R, "00_geometrie_ortho", f"ueberlagerung_plan_modell_{k}.png")).convert("RGB"); s = min(1000 / ov.width, 520 / ov.height); ov = ov.resize((int(ov.width * s), int(ov.height * s)), Image.LANCZOS)
        x0 = 120 + (i % 2) * 1100; y0 = 200 + (i // 2) * 620; im.paste(ov, (x0, y0)); d.text((x0, y0 + ov.height + 12), t, font=F(24, "SemiBold"), fill=INK)
    d.text((100, 1480), "Überlagerung 50 % Planansicht / 50 % Modellansicht: Kanten, Fenster, Balkone und Rücksprünge sind deckungsgleich.", font=F(24), fill=GREY); footer(d, 10); pages.append(im)
    pages[0].save(os.path.join(HF, "05_bildauswahl_volksbank.pdf"), save_all=True, append_images=pages[1:], resolution=200); return len(pages)
if __name__ == "__main__":
    rows = build(); print(len(rows), "Zeilen QC"); print(pdf(), "Seiten PDF")
