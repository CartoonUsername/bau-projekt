# 01 Prüfung des bisherigen Workflows und Fehlerliste

Stand 22.10.2026. Geprüft wurden `scripts/render_ref.py` (erster Tonmodell-Renderer), `scripts/blender_model.py` (erstes Blender-Modell), die damit erzeugten Referenzbilder, die Higgsfield-Bilder der `Bildauswahl_Volksbank_Baufeld3.pdf` und die Planunterlagen (Geometriedatei `geometry/variant_B3.json`, Blatt 25 SVG, Blatt 21/23/26).

## A. War das bisherige Modell aus den Plänen aufgebaut?
**Teilweise.** Die Baukörper (Grundriss-Konturen, Geschosshöhen, Rücksprünge 0,80 m, Auskragung 3,00 m, Staffel-Anbau, Attika, fünf Balkone, Dachterrasse, 11 Stellplätze) wurden direkt aus `variant_B3.json` gelesen und sind maßgleich. **Die Öffnungen (Fenster, Türen) und Details wurden dagegen von Hand aus dem Programmcode von Blatt 25 abgeschrieben, nicht aus einer gemeinsamen Datenquelle übernommen, und es gab keine maßliche Prüfung gegen den Plan.** Genau dabei sind Fehler entstanden. Zusätzlich war die Darstellung (Beleuchtung, Gelände, Material) unbrauchbar, und die Higgsfield-Bilder wurden nur nach Augenschein mit der Referenz verglichen.

## B. Konkrete Abweichungen des bisherigen Modells gegenüber den Plänen
| Nr | Bauteil | Bisheriges Modell | Plan (Blatt 25 / Geometriedatei) | Wirkung |
|---|---|---|---|---|
| M1 | Ostseite Fenster 1. OG und Staffel | y 11,5–13,5 | y 9,5–11,5 (Gangende des Mittelgangs, aus `elev3` der Ostansicht) | Fenster lag in der Wohnungszone statt am Gang |
| M2 | Ostseite Tür EG | y 16,7–17,9 | y 15,5–16,7 | falsche Lage um 1,2 m |
| M3 | Abluftstutzen (C-22) | fehlte | in Ostansicht gezeichnet, 0,75 x 0,75 m, +9,90 bis +10,80 m, Mitte x 30,4 / y 12,1 | Dachaufbau fehlte |
| M4 | Betonbänder | 4 cm Überstand über die Wand | bündig mit der Wand | Kanten nicht deckungsgleich |
| M5 | Fensterfelder Platzseite 1. OG | 3 Felder (erste Blender-Fassung) | 2 Felder | Fensterteilung falsch |
| M6 | Rahmenfarbe Staffelfenster | dunkel (erste Fassungen) | helles Holzfenster | Materialwechsel falsch |
| M7 | Vordach Platzseite | enthalten | nicht in der Ansicht Blatt 25 und nicht in der Geometriedatei, nur Blatt 21 / C-18 (Annahme) | Plan-interne Unstimmigkeit, nicht entscheidbar → Frage offen |
| M8 | EG-Verglasung Platzseite | Pfosten alle 1,40 m | Blatt 25 zeigt eine Glasfläche ohne Pfosten | Pfostenraster stammt aus dem eingefrorenen Platzfassaden-Design, im Plan nicht gezeichnet → offen |
| M9 | Abluftstutzen in der Platzansicht | – | Blatt 25 zeigt ihn nur in der Ostansicht, nicht vorn | Plan-interne Unstimmigkeit (in 3D sichtbar) |
| M10 | Stützen unter der Auskragung | 0 (richtig) | 0 (`stuetzen: 0`) | Modell richtig, aber die Higgsfield-Rückansicht zeigte Stützen |

## C. Darstellungsfehler (keine Geometriefehler)
- D1: Himmel/Sonne überbelichtet, Fassaden weiß ausgebrannt; Sonne stand auf der falschen Seite.
- D2: Endliche Bodenfläche mit sichtbarer Kante im Luftbild, keine Horizontlinie.
- D3: Materialien nur als Tonfarben, Prozedural-Texturen mit falscher Skalierung (Klinker als große Streifen), Glas ohne Innenraum schwarz.
- D4: Terrassenkamera sah nur auf die Brüstung.

## D. Fehler der Higgsfield-Bilder (Bildauswahl, Stand 22.10.)
Prüfung nach Augenschein gegen Modell und Blatt 25; **keines der Bilder ist maßlich verifiziert**.
| Bild | Befund | Status |
|---|---|---|
| 01 Tag | Staffel mit eingerückten Loggien/Holzlaibungen statt bündiger Fenster; Anzahl Balkone 5 stimmt | KORREKTUR ERFORDERLICH |
| 02 Abend | Staffelwand ohne Fenster (laut Plan vier Fenster); Fensterläden an 1. OG erfunden; Kameraposition weicht von 01 ab | KORREKTUR ERFORDERLICH |
| 03 Rück | vier bis fünf Stützen erfunden (Plan: keine); tiefe Loggien statt flacher Fenster; Umgebung (Halle, Felder) erfunden | KORREKTUR ERFORDERLICH |
| 04 West | Fenster plausibel, Vordach-Ausleger links abweichend, Dachterrasse nur angedeutet | NICHT VERIFIZIERBAR |
| 05 Ost | Fensterlagen und -größen weichen vom Plan ab | KORREKTUR ERFORDERLICH |
| 06 Luft | Dachterrassenfläche und Staffelkontur nicht eindeutig, Stellplätze nicht deckungsgleich | NICHT VERIFIZIERBAR |
| 07 Gastro | Klinkerpfeiler (im Grundriss Blatt 21 nicht vorhanden), Bankreihen und Bar nicht lagetreu, erfundener Stadtplatz mit Giebelhäusern | KORREKTUR ERFORDERLICH |

## E. Ursachen
1. Keine gemeinsame Datenquelle für Öffnungen (M1–M3).
2. Keine automatische Prüfung der 3D-Geometrie gegen den Plan.
3. Ein Bildmodell ist keine Konstruktionssoftware: es hält Geometrie nicht verlässlich ein, auch nicht bei strengen Prompts.
4. Referenzen wurden nur per Augenmaß verglichen.

## F. Gegenmaßnahmen (umgesetzt)
- Neue Datenquelle `scripts/modell_b3.py` (Baukörper aus der Geometriedatei, Öffnungen nach der Regel von Blatt 25); ein Blender-Aufbau und die Prüfung lesen dieselbe Quelle.
- `scripts/pruefe_modell_gegen_plan.py` vergleicht Modell und SVG von Blatt 25 maßlich (Toleranz 0,015 m): 83 von 83 Prüfpunkten bestanden; der Test erkennt nachweislich die alten Fehler M1/M2 (4 Abweichungen bei Wiedereinbau der alten Werte).
- Ortho-Ansichten des Modells im Maßstab 1:250 über das Planblatt gelegt (`renderings/00_geometrie_ortho/ueberlagerung_plan_modell_*.png`): Kanten deckungsgleich.
- Außenansichten werden mit Blender/Cycles aus diesem Modell gerendert; Higgsfield nur noch optional zur Veredelung mit Geometrie-Kontrolle.
