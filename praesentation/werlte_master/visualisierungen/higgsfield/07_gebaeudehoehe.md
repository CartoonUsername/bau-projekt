# 07 Gebäudehöhe gegen zulässige Höhe

Stand 23.10.2026, Modell v4 (`scripts/modell_b3.py`, Funktion `hoehenpruefung()`).

| Größe | Wert | Fundstelle |
|---|---|---|
| Zulässige Gesamthöhe | **12,00 m** | Bestätigung des Auftraggebers vom 23.10.2026; deckt sich mit dem B-Plan-Auszug-Stand in `documentation/project_brief.md` ('Gesamthöhe max. 12,00 m') und `source_conflict_register.md` C-03 |
| Traufhöhe nach B-Plan | 6,50 m | B14 Höhenkote '+6,50 Traufe nach B-Plan und Staffel'; Modell: Oberkante 1. OG / Betonband bei +6,50 |
| Staffeldecke | +9,60 m | B14 Höhenkote, VB3 boxes L2 |
| Attika (Oberkante Dach, höchster Bauteilpunkt des Modells) | **+9,90 m** | B14 Kennzahl 'Höhe Attika 9,90 m', B4, VB3 |
| **Differenz zur zulässigen Höhe** | **2,10 m** (12,00 − 9,90) | Rechnung, nur gültig bei Bezug auf ±0,00 |
| Geschosse | 3 (EG, 1. OG, Staffelgeschoss), zulässig höchstens 3 | Bestätigung des Auftraggebers 23.10.2026; Vollgeschossfrage des Staffelgeschosses (C-02/C-23) bleibt offen |

## Höhenbezug
- Im Modell und in allen Plänen ist **±0,00 die Oberkante des Erdgeschossfußbodens** (B14: '±0,00 Oberkante Erdgeschoss'). Die absolute Höhe des Geländes, der Straße oder des Platzes und der **Bezugspunkt der Messregel** der Stadt (Gelände, Straßenoberkante, Attika oder First) sind **nicht belegt** (kein Lageplan, C-13/C-29, C-03 'Messregel unbestätigt').
- Die Differenz von 2,10 m gilt daher nur, wenn der Bezugspunkt der Stadt auf Höhe von ±0,00 liegt. Liegt der Bezugspunkt tiefer (z. B. Straße unter dem Erdgeschossfußboden), verringert sich die Reserve entsprechend. Das ist **offen** und mit der Stadt zu klären.

## Umgang mit der Reserve
- Die restlichen 2,10 m werden **nicht ausgenutzt**: keine Aufstockung, keine höhere Attika, keine zusätzlichen Geschosse, Gebäudehöhe im Modell unverändert 9,90 m.
- Dachaufbauten (Abluft-Austritt C-22, Aufzugsüberfahrt C-25) sind weder dargestellt noch bemessen; ob sie innerhalb der Reserve liegen, ist offen und von der Messregel abhängig.

## Prüfung
`python3 scripts/pruefe_modell_gegen_blatt14.py` enthält die Zeile H1 (Attika 9,90 m gegen 12,00 m, 3 Geschosse): bestätigt. Die Prüfung stützt sich auf die Höhenkoten von Blatt 14, nicht auf einen Lageplan.
