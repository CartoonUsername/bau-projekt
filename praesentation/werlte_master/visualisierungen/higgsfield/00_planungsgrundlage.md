# 00 Planungsgrundlage für die Visualisierungen – Neue Mitte Werlte, Baufeld 3

Status-Kennzeichnung je Angabe: **[B]** bestätigt (aus der Geometriedatei bzw. dem Planblatt belegt) · **[A]** angenommener Arbeitsstand (ASSUMED/PROVISIONAL im Plan) · **[U]** ungeklärt.
„Bestätigt“ heißt hier nur: in den Projektplänen eindeutig festgelegt. Nichts davon ist baurechtlich oder vom Bauherrn freigegeben (Design Freeze gilt nur für die Platzfassade).

## 1. Variante und Planrevision
- Variante **B3**, Alternative **K** (Büro-Alternative, Abstell/Fahrrad im EG entfällt) – Arbeitsgrundlage Runde 3 vom 22.10.2026 **[B]**.
- Quelle der Wahrheit: `geometry/variant_B3.json` (Schlüssel `variants.K`) und `geometry/variants3_metrics.json` **[B]**.
- Zugeordnete Planblätter (geprüft, Blattinhalt gesehen): Blatt 23 Grundrisse/Schnitt, Blatt 25 Fassadenkonzept/Ansichten, Blatt 21 Gastro-Möblierung, Blatt 22 Büro/Zugang, Blatt 24 Wohnungsstudien, Blatt 26 Stellplätze, Blatt 31 Flächen/Wohnungen, Blatt 32 Dachaufsicht/Schnitt B-B **[B]**.
- Die früheren Bilder (`Bildauswahl_Volksbank_Baufeld3.pdf`, Ordner `roh/`, `referenzen/ref_*.png`, `PROMPTS_UND_REIHENFOLGE.md`) sind **nicht verbindlich** (siehe `03_referenzregister.md`).

## 2. Gebäudeabmessungen
| Größe | Wert | Status |
|---|---|---|
| Breite | 32,00 m | [A] Arbeitsannahme (Grundstück H1 32 x 30 m nicht bestätigt) |
| Tiefe EG | 18,00 m | [B] |
| Tiefe 1. OG | 21,00 m (Anbau hinten x 4–32, y 18–21) | [B] |
| Tiefe Staffel | 17,90 m (y 0,8–18,7) | [B] |
| Höhen | EG 3,50 / 1. OG 3,00 / Staffel 3,10 / Attika 9,90 m ab ±0,00 | [B] |
| Auskragung 1. OG hinten | 3,00 m (y 18→21) | [B], bestätigt mit der Nutzervorgabe |
| Staffel hinten | Rand y 18,7 = 0,70 m über die EG-Flucht, 2,30 m hinter der 1.-OG-Kante; Anbau-Tiefe 1,50 m (e2) | [B] – weicht von der Kurzformel „Staffel 1,5 m Vorsprung“ ab, Geometrie gilt (Konflikt unten) |
| Staffel vorn/seitlich | Rücksprung 0,80 m (Front, West, Ost) | [B] |
| Wohnungen | 16 (9 im 1. OG, 7 im Staffelgeschoss), Wohnfläche 845,9 m² | [B] |
| Gastro | 440 m² brutto, 120 Plätze (normal), Büros 2 x ~28 m² hinten | [A] |

## 3. Orientierung der Fassaden
- Platzfassade: y = 0 (vorn, Marktplatz) **[B]**. Rückseite y = 18/21/18,7 **[B]**.
- Kernseite: x = 0, Ostseite: x = 32 **[B]** (Modellachsen). Himmelsrichtungen **[U]** (C-13).
- Darstellungskonvention der Pläne und der Bilder: Plan als Karte gelesen, Blick von der Platzseite → der Kern (x = 0) liegt **rechts**; Ansicht „Westseite“ = Kernseite (x = 0), „Ostseite“ = x = 32. Die Bezeichnungen West/Ost sind Arbeitsnamen, keine belegten Himmelsrichtungen.

## 4. Geschosskonturen (Grundriss)
- EG: Rechteck 32 x 18 m **[B]**.
- 1. OG: 32 x 18 plus Anbau hinten x 4–32 / y 18–21 (Rücksprung links vom Kern: x 0–4 bleibt auf y 18) **[B]**.
- Staffel: Polygon (0,8/0,8) (31,2/0,8) (31,2/18,7) (4,2/18,7) (4,2/17,2) (0,8/17,2) **[B]**.
- Geschossdecken: Betonbänder 0,30 m (Oberkante Decken bei +3,50 und +6,50 mit Band ab +3,20 bzw. +6,20) umlaufend **[A]** (Dicke angenommen).

## 5. Fenster und Türen (Modell, Positionen ASSUMED – Blatt 25 „Fensterformate Vorschlag, nicht freigegeben“)
| Fassade | Öffnung | x/y-Lage (m) | z (m) | Status |
|---|---|---|---|---|
| Platz EG | durchgehende Verglasung, Pfosten 1,4 m, Oberlicht-Band | x 4–32 | 0–3,1 | [A] |
| Platz EG | Doppeltür / Tür | x 17–19; 29,5–31; Kernfenster/Tür x 1–2,5 | 0–2,4 | [A] |
| Platz 1. OG | 5 Fenster, 2 Felder, schwarzer Stahlrahmen | x0+0,9…x0+4,7, x0 = 4 + 5,6·i | 3,9–6,1 | [A] |
| Platz Staffel | 4 Holzfenster, 2 Felder | je Wohnung (WE-L2-V) x+1,0…−1,0 | 6,9–9,0 | [A] |
| Rückseite EG | 3 Öffnungen | x 1–2,5; 5–6,5; 15–16,5 | 0–2,4 | [A] |
| Rückseite 1. OG | Fenster je Wohnung WE-L1-H | x0+1,6…x0+5,4 | 3,9–6,1 | [A] |
| Rückseite Staffel | Holzfenster je Wohnung WE-L2-H | x0+1,6…x0+7,4 | 6,6–9,1 | [A] |
| Kernseite x=0 | Schlitzfenster (Treppenhaus) EG/1. OG/Staffel | y 6,5–7,5 | 0,9–3,0 / 3,9–6,1 / 6,9–9,1 | [A] |
| Ostseite x=32 | Fenster Gang 1. OG, Staffel, Tür EG | y 11,5–13,5; y 16,7–17,9 (Tür) | 4,4–6,0; 7,4–9,0; 0–2,4 | [A] |

## 6. Balkone und Terrassen
- Platzseite: **5 Balkone**, je 2,70 x 1,50 m, Mitte auf den 5,6-m-Achsen (x 5,45–8,15; 11,05–13,75; 16,65–19,35; 22,25–24,95; 27,85–30,55), Betonplatte Unterseite +3,20, Milchglasbrüstung 1,10 m **[B]**.
- Rückseite 1. OG: keine Balkone **[B]** (Dachterrasse statt Balkon).
- Dachterrasse: 28,0 x 2,3 m (x 4–32, y 18,7–21), in drei Abschnitte à 9,0 x 2,3 m geteilt (64,4 m²), Milchglasbrüstung 1,10 m an Rück-, Ost- und West-Kante **[B]**; Belag Holzdeck **[A]**.
- Vordach Platzseite (EG-Eingang/Terrasse): 24 x 3,6 m, Unterkante +3,0 m, dunkler Stahl **[A]**; Konflikt C-18 (Überlappung mit Balkonplatten) offen.

## 7. Dach und Staffel
Flachdach, Attika +9,90 m, umlaufend 0,30 m hoch, ohne Überstand **[B]**. Staffelgeschoss-Holz: Lärche vertikal **[B]**. Abluftstutzen (C-22) und Aufzugsüberfahrt (C-25) in den Ansichten nicht modelliert **[U]**.

## 8. Überdachte Stellplätze und Stützen
- 11 Stellplätze 2,50 x 5,00 m, y 18–23, Fahrgasse 6,00 m (y 23–29) auf hypothetischer Fläche H1 **[A]**.
- Überdachung = die 3,00 m tiefe Auskragung des 1. OG (y 18–21), **keine Stützen** (`stuetzen: 0`), Untersicht Sichtbeton auf +3,20 m **[B]** (Tragwerk C-35 offen).
- Frühere Higgsfield-Bilder mit Stützen sind damit falsch.

## 9. Materialien und Farben
Dunkel rotbrauner Klinker (EG und 1. OG), Betonbänder hellgrau, Lärchenholz vertikal (Staffel), Milchglasgeländer, schwarze Stahlfenster EG/1. OG, helle Holzfenster in der Staffel, Attika grau. Platz: neutraler Pflasterbelag, Rückbereich Asphalt, keine Nachbarbebauung **[A]**.

## 10. Ungeklärt
C-13 Himmelsrichtung/Platzlage · C-19 Grenzabstände Rückseite · C-30/35 Auskragung, GRZ, Tragwerk · C-18 Vordach · C-22 Küchenabluft · C-25 Aufzugsüberfahrt · C-39 Dachterrasse (Brand/Schall) · Grundstück H1 · tatsächliche Fensterformate (Blatt 25: Vorschlag) · Staffelgeschoss als Vollgeschoss (C-23) · Gastro-Möblierung (Blatt 21).

## Konflikte Nutzervorgabe ↔ Planstand
- „Staffel hinten ca. 1,5 m Vorsprung“ → Plan: Staffel-Anbau 1,50 m tief (e2), Rand 0,70 m hinter … vor der EG-Flucht; es gilt die Geometrie.
- „9 + 7 Wohnungen“ ✓, „Auskragung 3,0 m“ ✓, „Stützen/Kern übereinander“ → Kern x 0–4 übereinander ✓, Stützen keine.
