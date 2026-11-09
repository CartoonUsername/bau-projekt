"""Baut Ausgabe, Qualitätskontrolle und Präsentations-PDF für das Modell v4 (nach den freigegebenen Korrekturen vom 23.10.2026).
Bilder: renderings/v4/ (Blender-Original und veredelte Fassung). Ältere Dateien bleiben unberührt."""
import os, sys, shutil, csv
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geometrietreue as GT, modell_b3 as MB
HF = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "visualisierungen", "higgsfield")); R = os.path.join(HF, "renderings", "v4")
GEST = "Betonbänder und seitliche Glasbrüstung der Dachterrasse sind konzeptionelle Gestaltung, nicht abschließend planbestätigt."
MOTIVE = [  # nr, ordner, titel, blender, veredelt, kamera, text, status, abweichungen
    ("01", "01_hauptansicht_tag", "Hauptansicht Platzseite (Tag)", "tag/tag_01_front.png", "veredelt/hf_01_front.png", "01_front", "Platzfassade mit großer Gastro-Verglasung im Erdgeschoss, fünf Balkonen am ersten Obergeschoss und zurückgesetztem Staffelgeschoss. Vordach 24 x 3,6 m (Konstruktion offen); Rahmenteilung der Verglasung konzeptionell.", "BESTANDEN",
     "Veredelung lässt Glas leicht Innenraum erkennen; Rahmenteilung konzeptionell; Vordach ohne Konstruktion; Betonbänder nur Gestaltung"),
    ("02", "02_hauptansicht_abend", "Hauptansicht Platzseite (Abend)", "nacht/nacht_01_front.png", "veredelt/hf_02_abend.png", "01_front", "Dieselbe Kamera und Geometrie wie die Tagesansicht, nur Licht und Tageszeit verändert.", "BESTANDEN",
     "Einrichtung hinter der Gastro-Verglasung und Vorhänge frei ergänzt (nicht planverbindlich); Auswahl beleuchteter Fenster ist Gestaltungsannahme"),
    ("03", "03_rueckansicht", "Rückansicht mit überdachten Stellplätzen", "tag/tag_03_rueck.png", "veredelt/hf_03_rueck.png", "03_rueck", "Rückseite mit 3,00 m Auskragung des ersten Obergeschosses über den Stellplätzen (ohne Stützen), zwei Erdgeschosstüren und Dachterrasse mit neutralem Belag. Dachaustritt der Küchenabluft und dritter Bürozugang sind offen und nicht dargestellt.", "BESTANDEN",
     "Stellplatzfläche hypothetisch; Asphalt-Rissbild kosmetisch ergänzt (falls sichtbar); Belag der Dachterrasse neutral"),
    ("04", "04_westseite", "Westseite (Kernseite), plangetreue Fassung", "tag/tag_04_west.png", "veredelt/hf_04_west.png", "04_west", "Seitenfassade des Erschließungskerns ohne Fenster, wie in Blatt 14 gezeichnet. Fenster sind nur als Gestaltungsvorschlag auf Seite 9 dargestellt (Belichtung, Treppenraum und Rettungswege offen).", "BESTANDEN",
     "Seitenfenster nicht Teil der plangetreuen Fassung (C-40 offen)"),
    ("05", "05_ostseite", "Ostseite, plangetreue Fassung", "tag/tag_05_ost.png", "veredelt/hf_05_ost.png", "05_ost", "Seitenfassade mit Erdgeschosstür (Blatt 14), Staffelrücksprung und Dachterrassenbrüstung; keine Fenster, wie in Blatt 14. Gestaltungsvorschlag mit Fenstern auf Seite 9.", "BESTANDEN",
     "Seitenfenster nicht Teil der plangetreuen Fassung (C-40 offen)"),
    ("06", "06_luftbild", "Luftbild / Gesamtansicht", "tag/tag_06_luft.png", "veredelt/hf_06_luft.png", "06_luft", "Baukörper mit Dachterrasse und elf Stellplätzen auf neutralem Grund; keine Nachbarbebauung dargestellt; kein Dachstutzen (Dachaustritt der Abluft offen).", "BESTANDEN", "Umgebung schematisch (Grundstück nicht bestätigt)"),
    ("07", "07_gastro_innenraum", "Gastronomie-Innenraum", "07_gastro_innenraum/tag_07_gastro.png", "veredelt/hf_07_gastro.png", "Innenraum", "Gastraum 28 x 10 m nach Grundriss Blatt 21: Bar am Rückende, Tischreihen, Verglasung zur Platzseite. Möblierung exemplarisch; Innenstützen offen.", "NICHT VERIFIZIERBAR",
     "Raumgeometrie, Tisch- und Barlage aus Blatt 21; Stuhl-/Hockerformen modellhaft; Pfeiler, Stützen und Glas-Stahl-Trennung im Plan B3 nicht vorhanden und nicht dargestellt (Innenstützen in Variante A vorgesehen, offen)"),
]
VORSCHLAG = [("04v", "04_westseite", "Kernseite mit Fenstern (Gestaltungsvorschlag)", "tag/vorschlag_tag_04_west.png", "veredelt/hf_04v_west.png", "04_west"), ("05v", "05_ostseite", "Ostseite mit Fenstern (Gestaltungsvorschlag)", "tag/vorschlag_tag_05_ost.png", "veredelt/hf_05v_ost.png", "05_ost")]
def build():
    rows = []
    for nr, ordner, titel, b, v, kam, text, status, abw in MOTIVE:
        d = os.path.join(R, ordner); os.makedirs(d, exist_ok=True); bn, vn = os.path.basename(b), os.path.basename(v)
        shutil.copy(os.path.join(R, b), os.path.join(d, "blender_" + bn)); shutil.copy(os.path.join(R, v), os.path.join(d, "final_" + vn)); s1, s2 = GT.score(os.path.join(R, b), os.path.join(R, v))
        rows.append(dict(bildnummer=nr, dateiname=f"renderings/v4/{ordner}/final_{vn}", verwendete_modellansicht=f"renderings/v4/{ordner}/blender_{bn} (Kamera {kam}, Modell {MB.MODEL_VERSION} plangetreu)", referenzen="scripts/modell_b3.py; Blatt 14 (Ursprungsansichten), Blatt 25 (Gestaltung), geometry/variant_B3.json" + ("; Blatt 21" if nr == "07" else ""),
                         geometrieprüfung=f"Plan-Ist-Abgleich Blatt 14: 06_pruefpunkte_blatt14.csv; Kantentreue Veredelung: Modellkanten wiedergefunden {s1 * 100:.1f} %, veredelte Kanten im Modell {s2 * 100:.1f} %", materialprüfung="Sichtprüfung gegen Modell: Klinker dunkelrotbraun, Beton, Lärchenholz, Milchglas, Stahlrahmen/Holzfenster Staffel" if nr != "07" else "Sichtprüfung gegen Vorgabe: Olivgrün, Cognac, Bordeaux, Eiche, dunkle Barfront, Messing, Mikrozement",
                         festgestellte_abweichungen=abw, status=status, erforderliche_korrektur="keine" if status == "BESTANDEN" else "Möblierung/Details vom Fachplaner/Bauherrn freigeben lassen; bis dahin konzeptionell kennzeichnen"))
    for nr, ordner, titel, b, v, kam in VORSCHLAG:
        d = os.path.join(R, ordner); bn, vn = os.path.basename(b), os.path.basename(v)
        if not os.path.exists(os.path.join(R, v)): continue
        shutil.copy(os.path.join(R, b), os.path.join(d, "blender_" + bn)); shutil.copy(os.path.join(R, v), os.path.join(d, "final_" + vn)); s1, s2 = GT.score(os.path.join(R, b), os.path.join(R, v))
        rows.append(dict(bildnummer=nr, dateiname=f"renderings/v4/{ordner}/final_{vn}", verwendete_modellansicht=f"renderings/v4/{ordner}/blender_{bn} (Modell {MB.MODEL_VERSION}, Variante 'vorschlag')", referenzen="scripts/modell_b3.py Variante vorschlag; Blatt 25", geometrieprüfung=f"Kantentreue Veredelung: {s1 * 100:.1f} % / {s2 * 100:.1f} %; Fenster nur Blatt 25 (ASSUMED)",
                         materialprüfung="Sichtprüfung", festgestellte_abweichungen="Seitenfenster nicht planbestätigt (Blatt 14 zeigt keine)", status="NICHT VERIFIZIERBAR", erforderliche_korrektur="nur mit Kennzeichnung 'Gestaltungsvorschlag' verwenden; Klärung Belichtung, Treppenraum, Rettungswege (C-40)"))
    rows.append(dict(bildnummer="08", dateiname="-", verwendete_modellansicht="-", referenzen="-", geometrieprüfung="-", materialprüfung="-", festgestellte_abweichungen="Motiv nicht erstellt (optional; Terrassenansicht der früheren Runde war unplausibel)", status="NICHT ERSTELLT", erforderliche_korrektur="optional"))
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
def page(): im = Image.new("RGB", (W, H), "white"); return im, ImageDraw.Draw(im)
def footer(d, n, extra=""):
    d.text((100, H - 70), "Konzeptionelle Visualisierung · Arbeitsstand B3 (Variante B, nicht freigegeben) · Baurecht, Tragwerk und Ausführungsplanung nicht bestätigt" + extra, font=F(21), fill=GREY); d.text((W - 160, H - 70), f"{n}", font=F(22), fill=GREY)
def pdf():
    pages = []; hp = MB.hoehenpruefung()
    im, d = page(); d.text((150, 560), "Neue Mitte Werlte – Baufeld 3", font=F(86, "Bold"), fill=INK); d.text((150, 690), "Konzeptionelle Visualisierungen", font=F(52), fill=INK); d.text((150, 790), "Gesprächsunterlage für die Hümmlinger Volksbank Werlte", font=F(36), fill=GREY)
    d.text((150, 1330), "Alle Ansichten zeigen dasselbe Gebäude (Arbeitsstand B3, Modell v4), erzeugt aus einem gemeinsamen 3D-Modell.", font=F(28), fill=GREY); footer(d, 1); pages.append(im)
    n = 2
    for nr, ordner, titel, b, v, kam, text, status, abw in MOTIVE:
        im, d = page(); src = Image.open(os.path.join(R, v)).convert("RGB"); k = min((W - 200) / src.width, 1170 / src.height); src = src.resize((int(src.width * k), int(src.height * k)), Image.LANCZOS)
        im.paste(src, ((W - src.width) // 2, 70)); y = 70 + src.height + 36; d.text((100, y), titel, font=F(40, "SemiBold"), fill=INK); y += 60
        for ln in wrap(d, text, F(24), W - 200): d.text((100, y), ln, font=F(24), fill="#333"); y += 33
        note = GEST if nr in ("01", "02", "03", "04", "05", "06") else "Konzeptionelles Bild: Möblierung und Details exemplarisch, nicht planverbindlich."
        d.text((100, y + 6), note, font=F(22, "SemiBold"), fill=ACC); footer(d, n); pages.append(im); n += 1
    vs = [(t, v) for nr, o, t, b, v, k in VORSCHLAG if os.path.exists(os.path.join(R, v))]
    if vs:
        im, d = page(); d.text((100, 60), "Gestaltungsvorschlag: Seitenfassaden mit Fenstern (nicht planbestätigt)", font=F(40, "SemiBold"), fill=ACC)
        for i, (t, v) in enumerate(vs):
            src = Image.open(os.path.join(R, v)).convert("RGB"); k = min(1050 / src.width, 650 / src.height); src = src.resize((int(src.width * k), int(src.height * k)), Image.LANCZOS); x0 = 100 + i * 1130; im.paste(src, (x0, 160)); d.text((x0, 170 + src.height), t, font=F(26, "SemiBold"), fill=INK)
        y = 160 + 650 + 120
        for ln in wrap(d, "Die Fenster stammen ausschließlich aus dem Entwurfsvorschlag Blatt 25 (Kernseite: Schlitzfenster im Treppenraum, Ostseite: Fenster am Gangende). Blatt 14 und die Grundrisse zeigen keine Seitenfenster. Ob und wie die Seiten belichtet werden, ist offen: Belichtung und Rauchabzug des Treppenraums sowie der Rettungsweg am Gangende (Brandschutz) sind zu klären (C-40, C-15). Die plangetreue Fassung ohne Fenster steht auf den Seiten 5 und 6.", F(26), W - 200): d.text((100, y), ln, font=F(26), fill="#222"); y += 38
        footer(d, n, " · nur als Gestaltungsvorschlag verwenden"); pages.append(im); n += 1
    im, d = page(); d.text((100, 80), "Planungsstand, Höhe und offene Entscheidungen", font=F(46, "SemiBold"), fill=INK); y = 170
    punkte = ["Arbeitsstand B3 (Variante B, Alternative K), Stand 23.10.2026, vorläufig und nicht freigegeben. Gebäude 32 x 18 m (Erdgeschoss, Breite 32 m ist Arbeitsannahme), 1. Obergeschoss mit 3,00 m Auskragung nach hinten, Staffelgeschoss; 16 Wohnungen (9 + 7), Gastronomie im Erdgeschoss, kompakte Büros hinten.",
              f"Höhe: Attika +{hp['attika_oberkante']:.2f} m über ±0,00 (Oberkante Erdgeschossfußboden), zulässig laut Bestätigung des Auftraggebers 12,00 m, Differenz {hp['differenz']:.2f} m; die Reserve wird nicht ausgenutzt. Höchstens drei Geschosse. Der Bezugspunkt der Höhenmessung der Stadt ist offen (siehe Höhendokument).",
              "Geometrie: ein gemeinsames 3D-Modell, gegen die Ansichten der Ursprungsunterlage Blatt 14 abgeglichen; jeder Prüfpunkt mit Fundstelle in der Prüfdokumentation. Fensterlagen sind dort 'schematisch, Maße offen'.",
              "Offene Planungsentscheidungen: Seitenfenster und Belichtung des Treppenraums (C-40), Rettungswege, Orientierung der Platzfassade und Himmelsrichtung (C-41, C-13), Dachaustritt der Küchenabluft und Belag der Dachterrasse (C-42), Rahmenteilung und Stützen der Glasfront sowie Bürozugang an der Rückseite (C-43, C-16), Tragwerk der Auskragung, des Vordachs und der Stellplatzüberdeckung (C-35).",
              "Als konzeptionell gekennzeichnet: Betonbänder, seitliche Glasbrüstung der Dachterrasse, Rahmenteilung der Verglasung, Vordach (Annahme), Umgebung und Stellplatzfläche (Grundstück nicht belegt), Innenraum.", "Die Wirtschaftlichkeit des Konzepts ist nach dem bisherigen Rechenstand in allen Szenarien nicht tragfähig (siehe separate Unterlage). Baurecht und Förderung sind nicht bestätigt."]
    for p in punkte:
        for j, ln in enumerate(wrap(d, p, F(26), W - 260)): d.text((130 if j else 100, y), ("• " if j == 0 else "") + ln, font=F(26), fill="#222"); y += 38
        y += 16
    footer(d, n); pages.append(im); n += 1
    im, d = page(); d.text((100, 80), "Geometrienachweis: Modell über Planansicht (Blatt 14, M 1:250)", font=F(40, "SemiBold"), fill=INK)
    for i, (k, t) in enumerate([("front", "Platzseite"), ("rear", "Rückseite"), ("west", "Kernseite"), ("east", "Ostseite")]):
        ov = Image.open(os.path.join(R, "00_geometrie_ortho", f"ueberlagerung_blatt14_modell_{k}.png")).convert("RGB"); s = min(1000 / ov.width, 520 / ov.height); ov = ov.resize((int(ov.width * s), int(ov.height * s)), Image.LANCZOS)
        x0 = 120 + (i % 2) * 1100; y0 = 200 + (i // 2) * 620; im.paste(ov, (x0, y0)); d.text((x0, y0 + ov.height + 12), t, font=F(24, "SemiBold"), fill=INK)
    d.text((100, 1480), "Überlagerung 50 % Blatt 14 / 50 % Modell v4: Baukörper, Türen, Fenster, Balkone und Rücksprünge sind deckungsgleich; Betonbänder und seitliche Brüstung zeigt Blatt 14 nicht (Gestaltung).", font=F(22), fill=GREY); footer(d, n); pages.append(im)
    pages[0].save(os.path.join(HF, "05_bildauswahl_volksbank.pdf"), save_all=True, append_images=pages[1:], resolution=200); return len(pages)
if __name__ == "__main__":
    rows = build(); print(len(rows), "Zeilen QC"); print(pdf(), "Seiten PDF")
