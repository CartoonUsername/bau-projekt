# Higgsfield-Visualisierungen Baufeld 3 (Variante B3) – Prompts und Reihenfolge

Status: NICHT generiert. Der Upload der Referenzbilder zu Higgsfield scheitert, weil die Netzwerkrichtlinie
der Umgebung den Host `upload.higgsfield.ai` blockiert (HTTP 403 vom Proxy). Es wurden keine Bilder erfunden.

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
