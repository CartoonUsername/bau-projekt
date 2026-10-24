# Phase 1: Quellenprüfung (A bis H), Stand 22.10.2026

Nichts davon ist geometrisch geprüft. Es gibt noch kein Gebäudemodell. Es wurden in dieser Phase keine neuen Bilder erzeugt.

## A. Audit des Designkonzepts
- Das Konzept ist in den Renderings und der Präsentation „Gastro-Konzept“ (16 Folien, 8 mit Bildern/Skizzen) klar beschrieben: dunkler Klinker, Beton, Lärchen-Staffel, Milchglas, Stahl-Glas-EG, Restaurant in Olivgrün/Cognac/Bordeaux/Eiche/Messing.
- Das Konzept ist KEIN geometrischer Entwurf. Die Zahlen (32 × 18 m, 5 Balkone, 7 Staffelachsen, 5 + 7 Wohnungen) stammen aus einem Flächenmodell für die Wirtschaftlichkeit und aus Skizzen, nicht aus Grundrissen.
- Die Originalplanungsunterlagen (B-Plan, Konzeptheft, Lageplan) liegen nicht im Projekt.

## B. Konsistenzmatrix
Siehe `reference_image_analysis.md`. Kurz: Materialien sind stimmig, Geometrie nicht (Balkone, Fensterachsen, Raumbreiten, Eingänge).

## C. Fehlende Maße und Widersprüche
Fehlend: Baufenster-Koordinaten, Lageplan mit Straßen/Rathaus/Himmelsrichtung, geprüfte Zeichnungen, Fenster-/Türmaße, Balkonmaße, Raster, Treppen-/Aufzugsmaße, Schächte, Rettungswege.
Widersprüche: 15 Einträge in `source_conflict_register.md`, davon nicht aus den Unterlagen lösbar: C-01 (Grundfläche), C-02 (Geschosse), C-03 (Dach/Höhe), C-13 (Orientierung).

## D. Vorschlag koordinierte Baumasse und Geschossanordnung (PROVISIONAL)
Beide Varianten laufen als Parameter im selben Modell, keine ist freigegeben.

| Größe | Variante A (Bestand) | Variante B (Baufenster-konform) |
|---|---|---|
| Grundfläche | 32,0 × 18,0 = 576 m² (nur mit Befreiung) | ca. 28,7 × 15,0 = 430 m² (Annahme in der Mitte von 400 bis 460) |
| Geschosse | EG, OG, Staffel (Rücksprung 0,8 m) | gleich |
| Höhen (ASSUMED) | Decke EG 3,50 / OG 6,50 (Traufe) / Staffel 9,60 / Attika 9,90 m | gleich |
| Kern West (Treppe, Aufzug, Wohnungseingang) | 4,0 × 18,0 = 72 m² | 4,0 × 15,0 = 60 m² |
| EG Gastro (brutto) | ca. 504 (Programm 510) | ca. 370 |
| OG | 2 Büros 165 m² + Wohnflächen aus Mittelgang-Grundriss | 2 Büros 165 m² + ca. 175 m² Wohnfläche |
| Staffel | ca. 498 m² BGF | ca. 363 m² BGF, ca. 255 m² Wohnfläche |
| Raster (Vorschlag) | 6,4 × 6,0 m (5 × 3 Felder) | 5,7 × 5,0 m (5 × 3 Felder) |
Die Zahl der Wohnungen ergibt sich erst aus dem Grundriss (Konflikt C-07), 12 ist nicht gesetzt. Wohnfläche gesamt in Variante B ca. 430 m² statt 655 m², das ändert die Wirtschaftlichkeit und muss danach neu gerechnet werden.
Grundrissprinzip (Vorschlag): Mittelgang mit Wohnungen an der Süd- und Nordfassade, Balkone ergeben sich aus den Wohnungen, Büros am Kern.

## E. Restaurant gegen Gebäude
- Flächenrichtwert im Modell 2,7 m² je Platz. Variante A: 510 m² ergibt 190 Plätze (konsistent). Variante B: 370 m² ergibt ca. 137 Plätze, bei 400 m² Grundfläche ca. 126, bei 460 m² ca. 148.
- Das Konzept zählt 12 Barhocker und 12 Stehtischplätze in die 190 Plätze. Rettungswege, Barrierefreiheit, Küchengröße und Abluft sind nicht berechnet.
- Die Innenbilder zeigen einen langen schmalen Raum mit Eingang am Ende, Folie 7 eine breite Fläche. Ein einziger EG-Plan muss das festlegen (Konflikt C-05, C-12).
- Nicht still vergrößern: Wenn Variante B gilt, werden Plätze und Küchenfläche reduziert, nicht das Gebäude.

## F. Verifizierter Workflow (3D/BIM und Higgsfield)
Geprüft in dieser Sitzung (Tool-Definitionen und Anleitung `/3d-jutsu`):
- Higgsfield „3D Jutsu“ ist ein gehostetes, versioniertes Blender-5.2-System (headless `bpy`). Es erlaubt eigenen Python-Code, Renders mit EEVEE oder Cycles als PNG/JPEG, Export als GLB und .blend, ca. 5 Minuten je Operation, kein Netzwerk, Code max. 256 KiB. Eigene Dateien lassen sich NICHT importieren (nur Katalog-Assets). Das Gebäude muss deshalb komplett prozedural in `bpy` gebaut werden.
- `scene_builder_3d_generate_angles` erzeugt per KI ein Bild aus einem Render und kostet Credits. Dabei kann sich die Geometrie ändern, jedes Ergebnis braucht einen Abgleich.
- Lokal in dieser Sitzung: kein Blender, kein bpy, kein trimesh/ifcopenshell, aber Python mit numpy, python-pptx und Chromium (Playwright). Pläne, Ansichten und Prüfungen lassen sich lokal aus derselben JSON-Datei erzeugen.
Nicht verifiziert: ob sich ein Blender-Render direkt als Referenzbild an die normale Bildgenerierung (nano_banana) übergeben lässt, und wie fotorealistisch EEVEE-Innenräume mit den vorhandenen Materialien werden.
Empfehlung: Das Modell (JSON) ist die Wahrheit. Pläne/Ansichten lokal aus der JSON, 3D-Renders in Higgsfield 3D Jutsu aus derselben JSON, KI-Veredelung nur optional mit Geometrie-Abgleich und Verwerfen bei Abweichung.

## G. Umsetzungsplan (Dateien und Skripte unter `praesentation/werlte_master/`)
1. `geometry/building_design.json`: Parameter, stabile IDs (WALL-GF-001, WINDOW-L1-004, BALCONY-L1-002, STAIR-RES-001, RESTAURANT-FRONT-001), Status je Wert.
2. `documentation/dimension_register.csv`: alle Maße mit Status (angelegt).
3. `geometry/restaurant_layout.json`: EG-Programm mit Plätzen, Raumgrößen, Wegen.
4. `scripts/generate_plans.py`: SVG-Grundrisse, Schnitte, Ansichten aus der JSON.
5. `scripts/build_model_bpy.py`: erzeugt aus der JSON ein einziges Blender-Skript für 3D Jutsu, Wände/Decken/Fenster/Balkone/Möbel nach ID, Material-Bibliothek.
6. `materials/material_manifest.json`: MAT-BRICK-DARK-01, MAT-TIMBER-NATURAL-01 usw.
7. `cameras/camera_manifest.json`: CAM-EXT-01 bis CAM-AXO-01 mit Position, Blickrichtung, Objektiv, Modellrevision.
8. `scripts/validate_model.py`: prüft Grundfläche gegen GRZ/Baufenster, Höhen, Fenster- und Balkonkoordinaten, schreibt `validation/validation_report.md` und einen Geometrie-Hash.
9. `renders/<Revision>/CAM-*.png` mit Begleitdatei (Revision, Hash, Kamera).
10. Phasenreihenfolge wie im Auftrag: Quellenprüfung (jetzt), Baufenster, Konzept, Master-Geometrie, Validierung, Freeze (`NEUE_MITTE_MASTER_v001`), Renders, Higgsfield-Veredelung, Abgabe.

## H. Mindestinformationen zum Einfrieren der Geometrie
1. B-Plan Nr. 123 mit Baufenster-Koordinaten (oder schriftliche Bestätigung der nutzbaren Grundfläche).
2. Lageplan mit Himmelsrichtung, Straßen, Platzseite, Rathaus, Nachbargebäuden.
3. Entscheidung Variante A oder B (Konflikt C-01).
4. Antwort der Stadt zu Staffelgeschoss/Vollgeschoss und Flachdach (C-02, C-03).
5. Bestätigung: Renderings (dunkler Klinker, Lärche, Milchglas) sind verbindlich, `aussen.jpg` ist nur Stilstudie (C-04).
6. Entscheidung, ob die Wohnungsgrundrisse neu geplant werden dürfen (C-07) und ob die Wohnungszahl 12 dabei als Ziel oder als Ergebnis gilt.
7. Programmentscheidung Restaurant: Plätze folgen der Fläche (C-06).
8. Standardmaße als Freigabe: Fenster-/Türbreiten, Balkonbreite und -tiefe, Umlaufbreite, Geschosshöhen.
9. Grundangaben Brandschutz/Rettungswege (zweiter Ausgang, Treppenhaus-Konzept) von einem Fachplaner.
