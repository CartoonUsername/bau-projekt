# 00 Planungsgrundlage für die Visualisierungen – Neue Mitte Werlte, Baufeld 3

> **Aktualisierung Modell v4 (23.10.2026) – überholt die Angaben weiter unten in folgenden Punkten:**
> 1. EG-Verglasung: **kein Pfostenraster** (das 1,40-m-Raster war nicht belegt). Konzeptionelle, unregelmäßige Rahmenteilung (7 Stege) ohne Rastermaß, nicht planbestätigt.
> 2. Rückseite Staffelfenster: z **6,90–9,00 m** (Blatt 14).
> 3. Rückseite EG: **zwei** Öffnungen (x 5–6,5 und 15–16,5, Blatt 14); die dritte (x 1–2,5) entfällt bis zur Entscheidung über den Bürozugang.
> 4. Dachterrasse: Belag **neutral grau** (im Plan nicht festgelegt).
> 5. Abluft: Schacht im Gebäude bleibt (B13/B23, VB3); **Dachaustritt/Stutzen nicht dargestellt**, offene Planungsentscheidung (C-22).
> 6. Vordach 24 x 3,6 m, Unterkante +3,00 m: **in Blatt 14 gezeichnet** und mit BD CANOPY-001 belegt (Annahme); Konstruktion offen, keine Stützen.
> 7. Seitenfenster Kern-/Ostseite: **nicht Teil der plangetreuen Fassung** (Blatt 14 zeigt keine); nur Ost-Tür EG (Blatt 14). Blatt-25-Fenster nur als gekennzeichneter Gestaltungsvorschlag (C-40).
> 8. Betonbänder und seitliche Dachterrassenbrüstung: konzeptionelle Gestaltung, nicht abschließend planbestätigt.
> 9. Ausrichtung unverändert (Kern rechts von außen gesehen); Plan-Spiegelung Blatt 4 ↔ Blatt 14 offen (C-41).
> 10. Höhe: Attika +9,90 m, zulässig 12,00 m (Bestätigung Auftraggeber), Differenz 2,10 m nicht ausgenutzt; max. 3 Geschosse (`07_gebaeudehoehe.md`).

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
| Staffel hinten | Rand y 18,7 = 0,70 m hinter der EG-Rückwand (y 18), 2,30 m vor der 1.-OG-Kante (y 21); Anbau-Tiefe 1,50 m (e2) | [B] – weicht von der Kurzformel „Staffel 1,5 m Vorsprung“ ab, Geometrie gilt (Konflikt unten) |
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
| Ostseite x=32 | Fenster am Gangende (Mittelgang y 9,5–11,5) 1. OG und Staffel, Tür EG | y 9,5–11,5; Tür y 15,5–16,7 | 4,4–6,0; 7,4–9,0; 0–2,4 | [A] (korrigiert gegenüber früherem Modell, siehe 01_fehlerliste.md) |

## 6. Balkone und Terrassen
- Platzseite: **5 Balkone**, je 2,70 x 1,50 m, Mitte auf den 5,6-m-Achsen (x 5,45–8,15; 11,05–13,75; 16,65–19,35; 22,25–24,95; 27,85–30,55), Betonplatte Unterseite +3,20, Milchglasbrüstung 1,10 m **[B]**.
- Rückseite 1. OG: keine Balkone **[B]** (Dachterrasse statt Balkon).
- Dachterrasse: 28,0 x 2,3 m (x 4–32, y 18,7–21), in drei Abschnitte à 9,0 x 2,3 m geteilt (64,4 m²), Milchglasbrüstung 1,10 m an Rück-, Ost- und West-Kante **[B]**; Belag Holzdeck **[A]**.
- Vordach Platzseite (Terrasse, Blatt 21 und Konflikt C-18): 24 x 3,6 m, Unterkante +3,0 m, dunkler Stahl **[A]**. Es steht **nicht** in der Ansicht Blatt 25 und nicht in der Geometriedatei – Unstimmigkeit im Plan, Frage an den Auftraggeber offen (Modell zeigt es, weil es zum eingefrorenen Platzfassaden-Design gehört).

## 7. Dach und Staffel
Flachdach, Attika +9,90 m, umlaufend 0,30 m hoch, ohne Überstand **[B]**. Staffelgeschoss-Holz: Lärche vertikal **[B]**. Abluftstutzen (C-22) ist in der Ostansicht von Blatt 25 gezeichnet (0,75 x 0,75 m, +9,90 bis +10,80 m, Mitte x 30,4 / y 12,1) und im Modell enthalten, Lage offen **[A]**; Aufzugsüberfahrt (C-25) ist nicht dargestellt **[U]**.

## 8. Überdachte Stellplätze und Stützen
- 11 Stellplätze 2,50 x 5,00 m, y 18–23, Fahrgasse 6,00 m (y 23–29) auf hypothetischer Fläche H1 **[A]**.
- Überdachung = die 3,00 m tiefe Auskragung des 1. OG (y 18–21), **keine Stützen** (`stuetzen: 0`), Untersicht Sichtbeton auf +3,20 m **[B]** (Tragwerk C-35 offen).
- Frühere Higgsfield-Bilder mit Stützen sind damit falsch.

## 9. Materialien und Farben
Dunkel rotbrauner Klinker (EG und 1. OG), Betonbänder hellgrau, Lärchenholz vertikal (Staffel), Milchglasgeländer, schwarze Stahlfenster EG/1. OG, helle Holzfenster in der Staffel, Attika grau. Platz: neutraler Pflasterbelag, Rückbereich Asphalt, keine Nachbarbebauung **[A]**.

## 10. Ungeklärt
C-13 Himmelsrichtung/Platzlage · C-19 Grenzabstände Rückseite · C-30/35 Auskragung, GRZ, Tragwerk · C-18 Vordach · C-22 Küchenabluft · C-25 Aufzugsüberfahrt · C-39 Dachterrasse (Brand/Schall) · Grundstück H1 · tatsächliche Fensterformate (Blatt 25: Vorschlag) · Staffelgeschoss als Vollgeschoss (C-23) · Gastro-Möblierung (Blatt 21).

## Konflikte Nutzervorgabe ↔ Planstand
- „Staffel hinten ca. 1,5 m Vorsprung“ → Plan: Staffel-Anbau 1,50 m tief (e2), Staffelrand 0,70 m hinter der EG-Rückwand und 2,30 m vor der 1.-OG-Kante; es gilt die Geometrie.
- „9 + 7 Wohnungen“ ✓, „Auskragung 3,0 m“ ✓, „Stützen/Kern übereinander“ → Kern x 0–4 übereinander ✓, Stützen keine.
