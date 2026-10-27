# 01 Geometriefreigabe – verbindliches 3D-Modell Baufeld 3 (B3 / K)

Stand 22.10.2026. Freigabe = **technische Arbeitsfreigabe für die Visualisierung**, keine Freigabe der Planung durch den Auftraggeber.

## Modell
- Quelle der Wahrheit: `scripts/modell_b3.py` (Baukörper, Bänder, Attika, Balkone, Dachterrasse, Stellplätze aus `geometry/variant_B3.json`; Öffnungen nach den Ansichtsregeln von Blatt 25; Abluftstutzen und Vordach als dokumentierte Zusatzelemente).
- 3D-Aufbau und Renderings: `scripts/blender_modell_v3.py` (Blender 5.1 über das Python-Modul bpy, Cycles). Gespeicherte Modelle: `modelle/baufeld3_B3_v3.blend`, früheres Tonmodell `modelle/baufeld3_B3.blend/.glb` (veraltet, enthält die Fehler M1–M3 aus `01_fehlerliste.md`).
- Szene: x' = −x gespiegelt, damit der Blick von der Platzseite den Kern (x = 0) rechts zeigt (Plan als Karte gelesen, wie Blatt 25). Himmelsrichtung unbekannt (C-13).

## Korrektur der früheren Prüfaussage (23.10.2026)
Die Angabe „83 von 83 Prüfpunkten“ verglich das Modell mit den Öffnungsregeln von Blatt 25, aus denen es gebaut war, und ist **kein unabhängiger Beleg**. Maßgeblich ist der Abgleich gegen Blatt 14 (andere Quelle): `06_pruefpunkte_blatt14.csv` mit Fundstelle je Zeile (SVG-Rechteck) und Zuordnung zur Prüfliste. Vordach und Pfostenraster: siehe `06_plan_ist_pruefliste.md` (frühere Aussagen dazu waren falsch). Modell jetzt Version v4.

## Prüfung (Stand Modell v3, historisch)
1. **Maßliche Prüfung gegen Blatt 25** (`scripts/pruefe_modell_gegen_plan.py`, Ergebnis `01_modellpruefung_details.csv`): 83 von 83 Prüfpunkten (Baukörper, Betonbänder, Attika, Balkonplatten und -brüstungen, Dachterrassenbrüstung, Abluftstutzen, alle Fenster und Türen aller vier Ansichten) stimmen mit der SVG von Blatt 25 auf 0,015 m überein; Gegenprobe Plan → Modell ebenfalls ohne fehlende Öffnung. Empfindlichkeitstest: mit den alten (falschen) Ostfenster- und Türwerten meldet die Prüfung 4 Abweichungen.
2. **Überlagerung** Ortho-Ansicht des Modells (Maßstab 1:250) über die Planansicht: `renderings/00_geometrie_ortho/ueberlagerung_plan_modell_{front,rear,west,east}.png`, Kanten deckungsgleich.
3. **Neutrale Ansichten** aus den definierten Kameras: `renderings/00_geometrie_neutral/einfach_*.png` (Farbcode wie Blatt 25).
4. Prüfung gegen die Geometriedatei: Baukörper werden direkt aus ihr gelesen.

## Kameras (Modellkoordinaten in m, Kleinbild 36 mm)
| Ansicht | Position | Ziel | Brennweite | Datei |
|---|---|---|---|---|
| 01 Platzseite Tag und 02 Abend (identisch) | 46 / −34 / 1,8 | 19 / 4 / 4,4 | 38 mm | `renderings/tag/tag_01_front.camera.json`, `renderings/nacht/…` |
| 03 Rückseite | −14 / 52 / 2,4 | 17 / 14 / 4,6 | 36 mm | `renderings/tag/tag_03_rueck.camera.json` |
| 04 Westseite (Kern) | −40 / −4 / 2,2 | 4 / 9 / 4,6 | 36 mm | `renderings/tag/tag_04_west.camera.json` |
| 05 Ostseite | 72 / 24 / 2,2 | 30 / 9 / 4,6 | 36 mm | `renderings/tag/tag_05_ost.camera.json` |
| 06 Luftbild | 70 / 58 / 25 | 14 / 10 / 3,0 | 36 mm | `renderings/tag/tag_06_luft.camera.json` |
Tages- und Abendbild nutzen exakt dieselbe Kamera; geändert sind nur Himmel, Sonne und Fensterbeleuchtung. Die Sonnenrichtung ist Gestaltungswahl (Himmelsrichtung unbekannt).

## Architektur-Freeze ab dieser Freigabe
Keine zusätzlichen oder verschobenen Fenster, Balkone, Stützen, Rücksprünge, Dachformen, Eingänge oder Stellplatzanordnungen. Änderungen nur nach dokumentierter Planprüfung und mit Aktualisierung der gesamten Serie.

## Einschränkungen (ehrlich)
- Die Öffnungsmaße stammen aus Blatt 25 und sind dort „Vorschlag (ASSUMED), nicht freigegeben“; das Modell ist damit so genau wie dieser Plan, nicht genauer.
- Offene Plan-Unstimmigkeiten, die im Modell so gelöst wurden: Vordach Platzseite (Blatt 21/C-18, nicht in Blatt 25) – im Modell enthalten; Pfostenraster 1,40 m der EG-Verglasung (Design Freeze, in Blatt 25 nicht gezeichnet) – im Modell enthalten; Abluftstutzen (nur Ostansicht gezeichnet) – im Modell enthalten, daher auch in der Platzansicht sichtbar. **Frage an den Auftraggeber:** Sollen Vordach, Pfostenraster und Abluftstutzen in den Bildern bleiben?
- Der Gastro-Innenraum ist aus Blatt 21 (Möblierung ‚normal‘) aufgebaut; Stuhl-/Hockerformen sind vereinfacht.
- Die Veredelung durch Higgsfield wurde per Kantenvergleich (nicht per Maßprüfung) kontrolliert.
