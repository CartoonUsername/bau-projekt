# 06 Plan-Ist-Prüfliste: Bildauswahl gegen Originalpläne

Vorgehen: Jedes dargestellte Bauteil von `05_bildauswahl_volksbank.pdf` wird einer Fundstelle in den Originalplänen zugeordnet (Quellenkürzel unten). Es wurden **keine Renderings erzeugt und das Modell nicht geändert**; Änderungen erfolgen erst nach Freigabe dieser Liste.

**Wichtig zur früheren Prüfung:** Die Angabe '83 von 83 Prüfpunkten' verglich das Modell mit den Öffnungsregeln von Blatt 25, aus denen es gebaut wurde. Das ist **kein unabhängiger Beleg** dafür, dass die Pläne richtig umgesetzt sind. Der unabhängige Abgleich gegen Blatt 14 steht in `06_pruefpunkte_blatt14.csv` (71 Prüfpunkte, aus SVG-Koordinaten zurückgerechnet): 52 bestätigt, 19 Abweichungen, davon alle erklärt in dieser Liste. Zwei meiner früheren Aussagen waren falsch und sind hier korrigiert (Vordach ist in Blatt 14 gezeichnet; das 1,40-m-Pfostenraster ist in keinem Plan belegt).

Ergebnis: 15 bestätigt, 2 Abweichung, 16 ungeklärt (insgesamt 33 Punkte).

Quellen: B3p/B4 = `praesentation_zeichnungen/03_Grundriss_Erdgeschoss`, `04_Ansicht_Platzfassade` (Arbeitsstand OG-2). B13/B14 = `varianten_v2/13_`, `14_Variante_B_…` (PDF `Varianten_v2_ABC_Gesamt.pdf` S. 3/S. 4). B21–B26 = `varianten_v3/21…26`. BD = `geometry/building_design.json`. VB3 = `geometry/variant_B3.json`. SK = `bilder/skizze_aussen_ansichten`, `bilder/gen_skizzen.js` (Skizze, nicht maßstäblich). KI = `bilder/ki_aussen_1/2.jpg`. CR = `documentation/source_conflict_register.md`.


## Seitenfassaden

| ID | Bauteil | Seite | Fundstelle in der Ursprungsplanung | Status | Erforderliche Korrektur |
|---|---|---|---|---|---|
| S1 | Kernseite EG: Schlitzfenster y 6,5–7,5 m, z 0,9–3,0 m | 5 | B14 Kernseite: keine Öffnung. B13/B23 Grundrisse: Treppenraum x 0–4, y 4,5–9,5 (VB3 STAIR-GF), kein Fenstersymbol, Vermerk 'Fenster, Türen und Wandstärken nicht festgelegt'. B25 Kernseite: Schlitzfenster als 'Vorschlag (ASSUMED), nicht freigegeben'. SK/KI zeigen keine Kernseite. | **ungeklärt** | Nur durch Blatt 25 vorgeschlagen, in Blatt 14 nicht vorhanden. Bis zur Entscheidung aus dem Bild entfernen (Wand geschlossen) oder als Vorschlag kennzeichnen. Belichtung/Rauchabzug Treppenraum ist Sache des Brandschutz-/Fachplaners (C-15). |
| S2 | Kernseite 1. OG: Schlitzfenster y 6,5–7,5 m, z 3,9–6,1 m | 5 | wie S1 (Treppenraum STAIR-L1 y 4,5–9,5) | **ungeklärt** | wie S1 |
| S3 | Kernseite Staffelgeschoss: Schlitzfenster (Holzrahmen) z 6,9–9,1 m | 5 | wie S1 (Treppenraum STAIR-L2 x 0,8–4,2, y 4,5–9,5); helles Holzfenster nur im Legendentext B25 | **ungeklärt** | wie S1 |
| S4 | Ostseite EG: Tür y 15,5–16,7 m, z 0–2,4 m | 6 | B14 Ostseite: weißes Türrechteck an exakt dieser Lage (SVG a 15,50–16,70 / z 0–2,40). B25 gleich. B13/B23 Grundriss: Ostwand im Küchen-/Anlieferbereich ohne beschriftete Tür. | **bestätigt** | Lage bestätigt, Zweck der Tür (Anlieferung/Personal) im Plan nicht beschriftet; keine Korrektur am Bild. |
| S5 | Ostseite 1. OG: Fenster am Gangende y 9,5–11,5 m, z 4,4–6,0 m | 6 | B14 Ostseite: keine Öffnung. B13/B23: Mittelgang CORR-L1 y 9,5–11,5 endet an der Ostwand (x 32), ohne Fenstersymbol. B25: 'Ostseite mit Fenster am Gangende' (ASSUMED). SK (Variante-A-Stand, Skizze, nicht maßstäblich): Schmalseite mit drei großen Fenstern im 1. OG und voll verglastem EG – anderer, älterer Stand. Gang als Sackgasse/Rettungsweg offen (planning/baurechtliche_fragen.md Nr. 7, C-15). | **ungeklärt** | Vorschlag aus Blatt 25, nicht Ursprungsplan. Bis Entscheidung entfernen oder als Vorschlag kennzeichnen. Ob das Gangende ein Fenster oder einen zweiten Rettungsweg braucht, klärt der Brandschutz. |
| S6 | Ostseite Staffelgeschoss: Fenster am Gangende, z 7,4–9,0 m | 6 | wie S5 (CORR-L2 y 9,5–11,5) | **ungeklärt** | wie S5 |
| S7 | Dachterrassenbrüstung seitlich (West und Ost), Milchglas 1,10 m | 5, 6, 7 | B14 Seitenansichten: nicht gezeichnet. B13/B23 Schnitt: Brüstung hinten gezeichnet; B14 Legende 'Milchglas-Brüstung 1,10 m'. B25 zeichnet sie auch seitlich. | **ungeklärt** | Hinten bestätigt (B13/B14), seitlich nur B25. Absturzsicherung an den offenen Seiten ist baulich naheliegend, im Plan aber nicht festgelegt: Vorschlag beibehalten und kennzeichnen. |
| S8 | Staffelrücksprung vorn und seitlich 0,80 m | 2, 3, 5, 6 | B4 Hinweis 'Staffelgeschoss 0,80 m zurückgesetzt'; B14 Seitenansichten (Staffel 0,8 m eingerückt); VB3 outlines L2. | **bestätigt** | keine |
| S9 | Betonbänder an den Geschossdecken, umlaufend, 0,30 m | 2–7 | B14: nicht gezeichnet. B4: nur Balkonplatten. B25: 'Betonbänder laufen um alle vier Seiten' (Gestaltungsregel, abgeleitet aus KI). KI ki_aussen zeigt Betonbänder. | **ungeklärt** | Gestaltungsregel aus Blatt 25 und Referenzbild, nicht in den Ansichten von Blatt 14/4 gezeichnet. Entscheidung: beibehalten (Design) oder entfernen. |
| S10 | Materialgrenzen Klinker (EG, 1. OG) / Lärchenholz (Staffel) | 2–7 | B14 Legende und Flächen; project_brief.md 'Außen'; KI. | **bestätigt** | keine |

## Platz/Rück

| ID | Bauteil | Seite | Fundstelle in der Ursprungsplanung | Status | Erforderliche Korrektur |
|---|---|---|---|---|---|
| P1 | Baukörper: 32 x 18 m (EG), 1. OG 21 m tief, Staffel 17,9 m; Höhen 3,50 / 3,00 / 3,10 m, Attika 9,90 m | 2–7 | B14 Kennzahlen und SVG-Rechtecke (alle Baukörper deckungsgleich); B13 Kennzahlen; B4 Höhenkoten; VB3 boxes/outlines. | **bestätigt** | keine |
| P2 | Fünf Balkone 2,70 x 1,50 m, Plattenunterseite +3,20, Milchglasbrüstung 1,10 m | 2, 3, 7 | B4 und B14: fünf Balkone an der Platzfassade (SVG a 5,45–8,15; 11,05–13,75; 16,65–19,35; 22,25–24,95; 27,85–30,55); BD balconies BALC-L1-F1…F5 (PROVISIONAL); B13/B23 Grundriss 1. OG: fünf Kästen. KI zeigt ungleiche Balkone, teils kurze Seite (C-08). | **bestätigt** | Plan bestätigt fünf gleiche Balkone nur an der Platzseite; KI weicht bewusst ab (C-08 entschieden zugunsten Plan). |
| P3 | OG-Fenster Platzseite: fünf Fenster x0+0,9…x0+4,7 (3,8 m breit), z 3,9–6,1 m | 2, 3 | B14: fünf gestrichelte Rechtecke exakt an dieser Lage ('Fensterlage schematisch, Maße offen'); B4 gleich. | **bestätigt** | Lage bestätigt, Maße im Plan offen: im Bild als Vorschlag kennzeichnen. |
| P4 | Staffelfenster Platzseite: vier Fenster x 5,2–9,95 / 11,95–16,7 / 18,7–23,45 / 25,45–30,2, z 6,9–9,0 m | 2, 3 | B14: vier gestrichelte Rechtecke exakt an dieser Lage; B4 gleich. C-21: Entwurf 4 Achsen, 1. OG 5, Referenzbilder 7 Fenstergruppen. | **bestätigt** | Lage bestätigt, Maße offen; Achszahl-Widerspruch zu KI (C-21) bleibt offen. |
| P5 | EG-Verglasung Platzseite x 4–32 m, Höhe 3,10 m, schwarze Stahlrahmen | 2, 3 | BD RESTAURANT-FRONT-001 (PROVISIONAL, schwarz Stahl); B3p Glasfront (Annahme); B4, B14 Glasfläche x 4–32. | **bestätigt** | keine |
| P6 | Pfostenraster 1,40 m in der EG-Verglasung (20 Felder) | 2, 3, 8 | Nicht belegt: BD und B3p/B4/B14/B25 zeigen eine Glasfläche ohne Pfosten; SK/gen_skizzen.js: Pfosten alle 2,00 m (13 Felder x 4–30). Das 1,40-m-Raster stammt aus meinem ersten Renderskript (scripts/render_ref.py), nicht aus einem Plan. Fassadenstützen R2 (x 4; 9,6; 15,2; 20,8; 26,4; 32) sind in BD 'REQUIRES-APPROVAL, noch nicht eingezeichnet' (C-16). | **Abweichung** | Fehler im Modell/Bild. Pfosten entfernen (glatte Glasfront wie in B4/B14/B25) oder erst nach Entscheidung des Tragwerksplaners/Bauherrn eintragen. Frühere Aussage 'Pfostenraster stammt aus dem eingefrorenen Design' war falsch. |
| P7 | Türen Platzseite: Eingang Kern x 1–2,5; Doppeltür x 17–19; Tür x 29,5–31 (je 2,40 m hoch) | 2, 3 | BD: DOOR-GF-RES-001 (x 1–2,5, ASSUMED), DOOR-GF-REST-001 (x 17–19, ASSUMED). B14: drei Türen an diesen Lagen. B21: Fluchtwegfelder 2,40 m und 1,90 m breit vor den Ausgängen (C-36). | **bestätigt** | Lage bestätigt; Türbreiten im Plan nicht festgelegt (Modell 2,0 / 1,5 m, B21 nennt 2,40 / 1,90 m Fluchtwegbreite): offen. |
| P8 | Stahlvordach Terrasse 24 x 3,6 m (x 6–30), Unterkante +3,00 m, 0,10 m dick | 2, 3, 5 | BD CANOPY-001 (ASSUMED, schwarz, unter allen Balkonplatten, C-18); B3p, B4 (Linie 'Stahlvordach Unterseite +3,00'), B13/B23 ('Terrasse mit Stahlvordach'), B21 (44 Terrassenplätze); B14 Platzansicht: Rechteck x 6–30, z 3,0–3,1 gezeichnet. B25 zeichnet es NICHT. Frühere Aussage 'nicht in Blatt 14' war falsch. | **bestätigt** | Vordach ist in den Planunterlagen belegt (als Annahme) und im Bild richtig. Konstruktion (Stützen, Abhängung) steht nirgends: siehe T3. |
| P9 | Rückseite 1. OG: vier Fenster (5,6–9,4 / 12,6–16,4 / 19,6–23,4 / 26,6–30,4), z 3,9–6,1 m | 4, 7 | B14 Rückseite: vier gestrichelte Rechtecke exakt an dieser Lage; VB3 rooms WE-L1-H1…H4. | **bestätigt** | Lage bestätigt, Maße offen |
| P10 | Rückseite Staffel: drei Fenster x 5,8–11,6 / 14,8–20,6 / 23,8–29,6, Höhe z 6,6–9,1 m | 4, 7 | B14: Lage identisch, Höhe z 6,90–9,00 m (2,1 m). B25 (und Modell): z 6,60–9,10 m (2,5 m, 'raumhohe Holzfenster zur Dachterrasse'). | **Abweichung** | Höhenabweichung zwischen B14 (Ursprung) und B25. Korrektur-Vorschlag: auf B14 setzen (z 6,9–9,0), sofern keine raumhohen Türen gewünscht sind. |
| P11 | Rückseite EG: Öffnungen x 5–6,5 und 15–16,5 sowie x 1–2,5 | 4, 7 | B14 Rückseite: zwei Türen (x 5–6,5 und 15–16,5, z 0–2,4). Die dritte Öffnung x 1–2,5 steht nur in B25 (Büro-Foyer mit Rückzugang, B22/B23 Alternative K, VB3 BUERO-FOYER2-GF), im Grundriss B23 ohne Türsymbol. | **ungeklärt** | Zwei Türen bestätigt; die dritte ist Alternative-K-Vorschlag: entfernen oder kennzeichnen, bis Büro-Zugang entschieden ist (C-32/C-38). |
| P12 | Auskragung 1. OG hinten 3,00 m; Staffel-Anbau 1,50 m; Dachterrasse 2,3 m tief | 4, 6, 7 | B13/B14/B23 Kennzahlen 'Auskragung 3,00 m / Überstand Staffel 1,50 m', B14 'Dachterrasse hinten 2,3 m tief', B13/B23 Schnitt bei x = 17 mit Maß 3,00 und 2,3 m; VB3 depth_L1 21,0, y2 18,7. | **bestätigt** | keine |
| P13 | Dachterrasse: Lage x 4–32, y 18,7–21; Belag Holzdeck | 4, 7 | Lage/Tiefe: B13/B23 Staffelgrundriss 'Dachterrasse 2,3 m (Vorschlag)', B14. Belag: nirgends festgelegt; CR C-09 nennt für den Staffel-Umlauf 'grauer Beton, ASSUMED'; ki_terrasse (Holzdeck) ist als veraltet geführt. | **ungeklärt** | Lage Vorschlag bestätigt; Belag Holz ist im Modell erfunden. Korrektur-Vorschlag: neutral grau (Beton) bis Entscheidung. |
| P14 | Abluftführung: Schacht x 29,8–31,0, y 11,5–12,7 m; Dachaustritt (Stutzen 0,75 m, bis +10,80 m) | 2, 3, 6, 7 | Schacht: B13/B23 gelbes Feld in allen Geschossen, VB3 SHAFT-KITCHEN (PROVISIONAL), C-22. Dachaustritt: B14 'Abluftführung über Dach (Austritt) ist nicht dargestellt' (C-22); nur B25 zeichnet einen Stutzen in der Ostansicht, Position offen. | **ungeklärt** | Schacht bestätigt, Stutzen nicht belegt. Stutzen im Bild entfernen oder als Annahme kennzeichnen. |
| P15 | Stellplätze: 11 x 2,50 x 5,00 m, 3,0 m von 5,0 m überdeckt, Fahrgasse 6,0 m | 4, 7 | B13/B23/B26 und VB3 parking; alle als hypothetisch (Grundstück 32 x 30 m nicht belegt, C-29). | **bestätigt** | Lage der Fläche im Bild als schematisch kennzeichnen (Umgebung bleibt neutral). |
| P16 | Orientierung der Platzfassade: Kern links oder rechts | 2, 3, 4, 5, 6, 7 | B4 (Design-Freeze-Ansicht) und SK: Kern links (x wächst nach rechts). B14/B25 und alle Bilder: Kern rechts (Platzfassade von außen gesehen). B3p-Grundriss: Platz oben, Kern links; von außen am Platz gesehen liegt der Kern damit rechts. Himmelsrichtung/Platzlage unbekannt (C-13). | **ungeklärt** | Plan-interne Spiegelung zwischen B4 und B14/B25. Entscheidung nötig, welche Seite der Kern liegt; bei Änderung alle Ansichten spiegeln. |

## Tragwerk

| ID | Bauteil | Seite | Fundstelle in der Ursprungsplanung | Status | Erforderliche Korrektur |
|---|---|---|---|---|---|
| T1 | 3,00-m-Auskragung 1. OG über den Stellplätzen | 4, 7 | Maß: B13/B14/B23. Tragwerk: C-35 'Tragwerk der Auskragung (3,00 m, Sichtbeton-Untersicht)' offen; Untersicht +3,20 (B13 Schnitt 'h 3,20 m'). | **ungeklärt** | Maß bestätigt, Konstruktion offen: Bild zeigt nur Volumen, keine Konstruktionsdetails (richtig). |
| T2 | Stellplatzüberdeckung ohne Stützen | 4, 7 | B13/B23/B14/VB3: keine Stützen (stuetzen: 0); Variante C hat 5 Stützen (C-35), B nicht. Ob 3 m ohne Stütze ausführbar und für GRZ/Stellplatznachweis zählt, ist offen (C-30, C-35). | **ungeklärt** | Bild ohne Stützen ist plangetreu; Entscheidung des Tragwerksplaners abwarten. |
| T3 | Vordach: Stützen/Abhängung | 2, 3, 5 | Nirgends gezeichnet oder beschrieben (BD CANOPY-001 nur Platte, Unterseite +3,00 Annahme). KI zeigt schlanke Stützen am Vorderrand (Gestaltungsreferenz). | **ungeklärt** | Offene Planungsentscheidung. Bild zeigt Platte ohne Stützen; als 'Konstruktion offen' kennzeichnen. |
| T4 | Fassadenstützen/Träger der 28-m-Glasfront | 2, 3 | C-16, BD facade_support: 'REQUIRES-APPROVAL', Achsen R2 x 4; 9,6; 15,2; 20,8; 26,4; 32 'noch nicht eingezeichnet'. | **ungeklärt** | Offen. Bild zeigt keine Stützen; Hinweis auf Blatt 'Hinweise' ergänzen. |
| T5 | Innenstützen im Gastraum | 8 | BD columns_gf und B3p (Variante A): vier Stützen x 9,6 / 15,2 / 20,8 / 26,4 bei y 8,0 (Raster R2, Annahme). B21/B23/VB3 (B3): keine Stützen eingetragen; Mittelgang liegt bei y 9,5–11,5 statt 8–10 (C-35, 'Abfangung'). | **ungeklärt** | Offen. Innenraumbild ohne Stützen entspricht B21, kann aber statisch falsch sein: als konzeptionell gekennzeichnet lassen. |

## Gastro-Innenraum

| ID | Bauteil | Seite | Fundstelle in der Ursprungsplanung | Status | Erforderliche Korrektur |
|---|---|---|---|---|---|
| G1 | Raum 28 x 10 m, Bar x 5–15 / y 8,6–10, 12 Barhocker, Tischreihen 11/11/5 Tische, Fluchtwegfelder, Verglasung zur Platzseite | 8 | B21 (Layout normal), VB3 furnishing/rooms: Lage der Tische und Bar aus denselben Daten wie das Bild. | **bestätigt** | Layout bestätigt; Stuhl-/Hockerformen sind modellhaft vereinfacht (keine Plangrundlage). |
| G2 | Klinkerpfeiler, Glas-Stahl-Trennung (Séparée), Bänke | 8 | In B21/B23 nicht vorhanden (Séparée nur in Variante A, B3p). Bild enthält keine. | **bestätigt** | keine (bewusst nicht dargestellt) |

## Vorschlag für die Freigabe (Standardannahmen, bitte bestätigen oder ändern)

1. P6: Pfostenraster entfernen (glatte Glasfront wie B4/B14/B25).
2. P10: Rück-Staffelfenster auf z 6,9–9,0 m (Blatt 14).
3. S1–S3, S5, S6: Seitenfenster entfernen (Blatt 14 zeigt keine), bis der Bauherr/Fachplaner sie festlegt.
4. P11: dritte EG-Rücköffnung (x 1–2,5) entfernen.
5. P13: Dachterrassenbelag neutral grau statt Holz.
6. P14: Abluftstutzen entfernen.
7. P8 Vordach bleibt (in B3p/B4/B13/B14/B21/BD belegt); ohne Stützen, im Hinweisblatt als 'Konstruktion offen'.
8. S7 seitliche Brüstung der Dachterrasse bleibt (Absturzsicherung), S9 Betonbänder bleiben als Gestaltung (Blatt 25, KI).
9. P16 Ausrichtung (Kern rechts) bleibt wie in B14/B25, bis Sie entscheiden; Hinweisblatt nennt die Plan-Spiegelung.
10. T1–T5 und alle 'ungeklärt'-Punkte werden im Hinweisblatt der PDF als offene Planungsentscheidungen aufgeführt.

Danach: Modell (`scripts/modell_b3.py`) ändern, Prüfung gegen Blatt 14 und 25 wiederholen, alle betroffenen Ansichten aus demselben Modell neu rendern und veredeln, PDF neu bauen.
