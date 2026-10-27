# 06 Zusammenhang der beiden Prüfungen und Zuordnung der 19 Abweichungen

**Zwei Prüfungen mit unterschiedlicher Zähleinheit:**

| Prüfung | Zähleinheit | Ergebnis |
|---|---|---|
| Blatt-14-Abgleich (`scripts/pruefe_modell_gegen_blatt14.py`) | ein Prüfpunkt = ein Bauteil in einer Ansicht (zurückgerechnetes SVG-Rechteck gegen Modellelement, Toleranz 3 cm); dasselbe Bauteil zählt in jeder Ansicht, in der es vorkommt, und eine Abweichung kann mehrere Zeilen erzeugen | Modell v3: 71 Prüfpunkte, 52 bestätigt, 19 Abweichungen |
| Plan-Ist-Prüfliste (`06_plan_ist_pruefliste.*`) | ein Punkt = ein Bauteil bzw. eine Planfrage mit Bezug auf Bildseiten, auch solche ohne Rechteck in der Ansicht (Tragwerk, Orientierung, Belag, Pfostenraster, Türbreiten) | 33 Punkte: 15 bestätigt, 2 Abweichung, 16 ungeklärt |

**Warum die Zahlen nicht übereinstimmen:** (1) Die Prüfliste zählt Bauteile, nicht Zeilen: z. B. ergeben die drei Rück-Staffelfenster sechs Zeilen im Abgleich (drei Modellelemente ohne Plan-Gegenstück und dieselben drei Plan-Rechtecke ohne Modell-Gegenstück) und einen Punkt (P10). (2) Die Prüfliste klassifiziert nach Plangrundlage: 'Abweichung' nur dort, wo der Plan eindeutig etwas anderes sagt (P6, P10); wo die Pläne nichts festlegen, steht 'ungeklärt', während der Abgleich jedes Element, das in Blatt 14 nicht gezeichnet ist, als 'Abweichung zu Blatt 14' zählt. (3) Der Abgleich sieht nur gezeichnete Rechtecke: Pfostenraster (P6), Belag (P13), Orientierung (P16), Türbreiten (P7), Tragwerk (T1–T5) und Innenraum (G1, G2) fehlen deshalb im Abgleich und wurden ab jetzt als eigene Zeilen ergänzt (Modell v4, siehe `06_pruefpunkte_blatt14.csv`).

## Die 19 Abweichungen (Modell v3) und ihre Zuordnung

| Nr | Ansicht | Prüfpunkt | Befund | Prüflistenpunkt | Stand Modell v4 |
|---|---|---|---|---|---|
| 1 | Platzseite | Betonbänder 0,30 m an den Geschossdecken | in Blatt 14 nicht gezeichnet; in Blatt 25, Blatt 4 (Balkonplatten) und Referenzbild ki_aussen vorhanden | S9 | bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen, nicht planbestätigt) |
| 2 | Rückseite | Öffnung EG-hinten (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | P11 | behoben (Korrektur 3: dritte Tür entfernt) |
| 3 | Rückseite | Öffnung Staffel-hinten-WE-L2-H1 (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | P10 | behoben (Korrektur 2: z 6,90–9,00 wie Blatt 14); die 3 'Plan-Elemente ohne Modell' sind dieselben Fenster in der Plan-Sicht |
| 4 | Rückseite | Öffnung Staffel-hinten-WE-L2-H2 (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | P10 | behoben (Korrektur 2: z 6,90–9,00 wie Blatt 14); die 3 'Plan-Elemente ohne Modell' sind dieselben Fenster in der Plan-Sicht |
| 5 | Rückseite | Öffnung Staffel-hinten-WE-L2-H3 (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | P10 | behoben (Korrektur 2: z 6,90–9,00 wie Blatt 14); die 3 'Plan-Elemente ohne Modell' sind dieselben Fenster in der Plan-Sicht |
| 6 | Rückseite | Betonbänder 0,30 m an den Geschossdecken | in Blatt 14 nicht gezeichnet; in Blatt 25, Blatt 4 (Balkonplatten) und Referenzbild ki_aussen vorhanden | S9 | bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen, nicht planbestätigt) |
| 7 | Rückseite | Plan-Element ohne Modell | in Blatt 14, aber nicht im Modell | P10 | behoben (Korrektur 2: z 6,90–9,00 wie Blatt 14); die 3 'Plan-Elemente ohne Modell' sind dieselben Fenster in der Plan-Sicht |
| 8 | Rückseite | Plan-Element ohne Modell | in Blatt 14, aber nicht im Modell | P10 | behoben (Korrektur 2: z 6,90–9,00 wie Blatt 14); die 3 'Plan-Elemente ohne Modell' sind dieselben Fenster in der Plan-Sicht |
| 9 | Rückseite | Plan-Element ohne Modell | in Blatt 14, aber nicht im Modell | P10 | behoben (Korrektur 2: z 6,90–9,00 wie Blatt 14); die 3 'Plan-Elemente ohne Modell' sind dieselben Fenster in der Plan-Sicht |
| 10 | Kernseite | Öffnung Kern-EG (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | S1 | behoben durch Herausnahme aus der plangetreuen Fassung; nur noch als Gestaltungsvorschlag (offene Entscheidung) |
| 11 | Kernseite | Öffnung Kern-OG1 (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | S2 | wie S1 |
| 12 | Kernseite | Öffnung Kern-Staffel (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | S3 | wie S1 |
| 13 | Kernseite | Brüstung Dachterrasse seitlich | Blatt 14 zeichnet keine seitliche Brüstung; Blatt 25 schon | S7 | bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen) |
| 14 | Kernseite | Betonbänder 0,30 m an den Geschossdecken | in Blatt 14 nicht gezeichnet; in Blatt 25, Blatt 4 (Balkonplatten) und Referenzbild ki_aussen vorhanden | S9 | bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen, nicht planbestätigt) |
| 15 | Ostseite | Öffnung Ost-OG1 (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | S5 | wie S1 |
| 16 | Ostseite | Öffnung Ost-Staffel (glas) | im Modell, aber NICHT in Blatt 14 (nur Vorschlag Blatt 25 bzw. Gestaltung) | S6 | wie S1 |
| 17 | Ostseite | Brüstung Dachterrasse seitlich | Blatt 14 zeichnet keine seitliche Brüstung; Blatt 25 schon | S7 | bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen) |
| 18 | Ostseite | Abluftstutzen | Blatt 14: 'Abluftführung über Dach (Austritt) ist nicht dargestellt' (C-22) | P14 | behoben (Korrektur 5: Stutzen entfernt; Dachaustritt offene Planungsentscheidung C-22) |
| 19 | Ostseite | Betonbänder 0,30 m an den Geschossdecken | in Blatt 14 nicht gezeichnet; in Blatt 25, Blatt 4 (Balkonplatten) und Referenzbild ki_aussen vorhanden | S9 | bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen, nicht planbestätigt) |

Summe je Prüflistenpunkt: P10: 6, P11: 1, P14: 1, S1: 1, S2: 1, S3: 1, S5: 1, S6: 1, S7: 2, S9: 4 = 19.

Alle 19 sind einem Punkt der Prüfliste zugeordnet (keine Zeile mit '?'): ja

## Prüflistenpunkte ohne Zeile in den 19 Abweichungen

| Punkt | Warum nicht im Abgleich sichtbar |
|---|---|
| P6 Pfostenraster | Blatt 14 zeichnet die Glasfläche als ein Rechteck; das Modell passte darauf (Rechteck x 4–32) und der Abgleich sah die 1,40-m-Stege nicht. Jetzt eigene Zeile. |
| P13 Belag Dachterrasse | Blatt 14 zeichnet keinen Belag. Jetzt eigene Zeile. |
| P7 Türbreiten, P16 Orientierung, P15 Stellplätze, T1–T5 Tragwerk, G1/G2 Innenraum | keine Rechtecke in den Ansichten von Blatt 14; Quellen sind andere Blätter (siehe Prüfliste). |
| P8 Vordach | im Abgleich 'bestätigt' (Blatt 14 zeichnet es); Prüflistenpunkt betrifft nur die offene Konstruktion. |
