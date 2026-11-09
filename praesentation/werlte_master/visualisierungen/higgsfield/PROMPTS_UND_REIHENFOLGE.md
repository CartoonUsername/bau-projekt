# Higgsfield-Visualisierungen Baufeld 3 (Variante B3) – Prompts und Reihenfolge

Status: Motive 01-07 generiert (Higgsfield, Modell nano_banana_2), Motive 08 (Dachterrasse) und 09 (Wohnung) nicht erstellt.

Alle Bilder: "konzeptionelle Visualisierung", ohne Text/Logos/Schilder, Bildbeschriftung nur im Layout außerhalb des Bildes.

## Gemeinsamer Prompt-Block (an jeden Prompt anhängen)
Photorealistic architectural visualization (conceptual). Use the first reference image (grey clay render) as a strict
geometry guide: keep camera, building outline, number of floors (EG + 1. OG + Staffelgeschoss), floor heights, window and
door positions, five balconies, setbacks, cantilever and proportions exactly. Do not add or remove floors, windows, balconies
or building parts. Materials: dark red-brown clinker brick on the ground floor, timber cladding on upper floors, exposed
concrete bands, glass and frosted-glass railings, large glazing towards the square. No text, no logos, no signs, no people
close-up, no invented neighbouring buildings (neutral surroundings only).

## Reihenfolge, Referenzen, Prompt-Ergänzung
| Nr | Motiv | Geometrie-Referenz (visualisierungen/referenzen) | Stilreferenz (praesentation/bilder) | Plangrundlage | Ergänzung |
|---|---|---|---|---|---|
| 01 | Hauptansicht Tag, Platzseite | ref_01_front.png | ki_aussen_1.jpg | Blatt 23, 31 | overcast daylight, eye level from Marktplatz |
| 02 | Abendansicht | ref_02_abend.png (= Kamera front) | ki_aussen_1.jpg | Blatt 23 | dusk, warm lit Gastro glazing, lit apartments |
| 03 | Rückansicht | ref_03_rueck.png | ki_aussen_2.jpg | Blatt 25, 32 | covered parking, terraces, access visible |
| 04 | West-/Kernseite | ref_04_west.png | ki_aussen_1.jpg | Blatt 24 | side facade, core |
| 05 | Ostseite | ref_05_ost.png | ki_aussen_1.jpg | Blatt 24 | side facade |
| 06 | Luftbild/Gesamtansicht | ref_06_luft.png | ki_aussen_2.jpg | Blatt 21, 32 | 11 covered stalls, neutral ground |
| 07 | Dachterrasse | ref_07_terrasse.png (Deck schlecht sichtbar, neu rendern) | ki_gastro_terrasse.jpg | Blatt 32 | 3 Dachterrassen 9,0 x 2,3 m |
| 08 | Gastro innen | ref_08_gastro.png | ki_gastro_raum.jpg, ki_gastro_bar.jpg | Blatt 22 | Olivgrün/Cognac/Bordeaux, Theke hinten |
| 09 | Wohnung (optional) | – | ki_wohnung_og.jpg, ki_wohnung_balkon.jpg | Blatt 31 | Balkon 2,70 x 1,50 m |

Prüfung je Bild: Geschosszahl, 5 Balkone, Fensterachsen, Auskragung, Staffelrücksprung gegen Referenz; sonst verwerfen.

## Ergebnis der Generierung und Prüfung
Zwei Durchläufe: Durchlauf 1 (Geometrie- plus Stilreferenz) wich ab (Eckperspektive, ca. 8 statt 5 Balkone, auskragendes Dach) und wurde für 01-06 verworfen.
Durchlauf 2 (nur farbcodierte Geometrie-Referenz mit Legende, "exakt fünf Balkone, bündige Attika, keine Zusatzbauteile") ist die Endfassung.
Gastro-Innenraum (07) stammt aus Durchlauf 1 (Referenzen ref_08_gastro + ki_gastro_raum).

Verwendet: 01/02 ref_01_front, 03 ref_03_rueck, 04 ref_04_west, 05 ref_05_ost, 06 ref_06_luft; Rohdaten in `roh/`.

Visuelle Prüfung (gegen Referenzrender, keine Maßprüfung):
- 01/02: Kamera, 3 Ebenen, 5 Balkone, Klinker EG/1. OG, Holz im Staffelgeschoss stimmen; Staffel zeigt eingerückte Loggien.
- 03: Rückflügel mit Auskragung über Stellplätzen plausibel; Anzahl Stellplätze/Balkone nicht exakt kontrolliert; Hintergrund enthält frei erfundene Umgebung (Halle, Felder).
- 04/05/06: Volumen und Materialverteilung stimmen; Fensterzahl im Detail nicht exakt maßgleich.
- 07: Stimmung wie bestehende Innenraumbilder; Möblierung/Pfeilerstellung nicht maßgleich zum Grundriss, im Hintergrund ist ein Platz mit Giebelhäusern erfunden.
Alle Bilder sind konzeptionelle Visualisierungen und keine Planunterlagen.
