# PDF-Import-Checkliste – Revitalyze PDF-zu-IFC-Test (Neue Mitte Werlte – Baufeld 3)

Stand 27.10.2026 · VORLÄUFIGER ENTWURF – NICHT GENEHMIGT · keine Variante ist gewählt, keine ist als „baurechtlich zulässig" bewertet.
Erzeugt mit `scripts/studie/revitalyze_pdfs.py` (reportlab, reine Vektor-PDFs, 0 Rasterbilder, echter Text); Modelle und Prüfungen in `scripts/studie/revitalyze_modelle.py`. Bestehende B3-Modelle und frühere PDFs wurden nicht verändert.

## 1. Dateien

| Datei | Inhalt | Format |
|---|---|---|
| `Test_EG_Vektor_Import.pdf` | **Zuerst hochladen:** nur Grundriss EG der B3-Referenz, ohne Grundstück, Stellplätze, Säulen | 1 Seite A3 quer, 1:100 |
| `A_B3_Referenz_Import.pdf` | B3-Referenz unverändert (aus dem bestehenden Modell v4) | 12 Seiten A2 quer, 1:100 |
| `B1_540m2_Vorbau_Buendig_Import.pdf` | Neue Idee (Ring, Stand 27.10.2026): EG 20 × 27 m = 540 m², Vorbau ringsum, oberstes Geschoss bündig zur Außenkante OG1 | 12 Seiten A2 quer, 1:100 |
| `B2_540m2_Vorbau_Staffel_150cm_Import.pdf` | wie B1, Staffel 1,50 m (rundum, ab Außenkante OG1) | 12 Seiten A2 quer, 1:100 |
| `B3_540m2_Vorbau_Staffel_300cm_Import.pdf` | wie B1, Staffel 3,00 m (nicht die B3-Referenz!) | 12 Seiten A2 quer, 1:100 |

Seiten je Paket: 1 Übersicht (Maße, Maßstabsbalken 10 m, Legende) · 2 EG · 3 OG1 · 4 oberstes Geschoss · 5–8 Vorder-, Rück-, West-, Ostansicht · 9 Schnitt A–A mit Höhenkoten · 10 Stellplätze/Erschließung (getrennt) · 11 Rechtsebenen/offene Punkte · 12 Konsistenzprotokoll. Seiten 11–12 sind reine Textseiten und für den Import-Test entbehrlich; für den Upload einzelne Zeichnungsseiten (z. B. 2, 5, 9) separat exportieren, falls Revitalyze Mehrseiten-PDFs nicht sauber trennt.

## 2. Was Revitalyze öffentlich sagt (Stand Abruf 27.10.2026)

- **Gesichert (Herstellerangabe):** Der KI-Agent erstellt aus PDF-Plänen (Grundrisse, Schnitte, Ansichten) ein IFC-Modell; im IFC „Wände, Decken, Türen und Fenster sowie Räume und Geschosse, soweit erkennbar".
- **Ungeklärt:** akzeptierte Dateitypen und Seitenformate, Größenlimit, ob Vektor-PDFs besser als Scans funktionieren, Einzel- vs. Mehrseiten-PDF, wie Grundriss/Ansicht/Schnitt einander zugeordnet werden, ob echte 3D-Körpergeometrie oder nur Mengen/Elemente entstehen, ob Räume als IfcSpace kommen.
- Der **kostenlose PlanReader-Test** liefert nach öffentlicher Beschreibung Mengen als Excel (kein IFC) und verlangt eine Firmen-E-Mail; der Maßstab wird im Tool gesetzt. → Maßstabsbalken (10 m = 100 mm) und Maßketten liegen auf jedem Blatt bei.
- Es wird **keine erfolgreiche Konvertierung zugesichert.** Die PDFs sind für gute Lesbarkeit gebaut, nicht für ein garantiertes Ergebnis.

## 3. Gesichert / angenommen / ungeklärt

### A (B3-Referenz)
- **Gesichert (aus bestehendem Modell/Planstand B14):** EG 32,00 × 18,00 m = 576 m²; Umrisse OG1 (3,00 m Anbau hinten) und Staffelgeschoss; Raumrechtecke; 23 Öffnungen mit Lage und Höhen (Status „plan"); fünf Balkone; 11 Stellplätze (davon 10 teils überdeckt).
- **Angenommen:** Wandstärke 0,30 m (nur Darstellung), Deckenstärke 0,30 m, Höhenbezug ±0,00 = OK Fertigfußboden EG, Stellplatz 2,50 × 5,00 m, Fahrgasse 6,00 m, Grundstück 32 × 30 m.
- **Ungeklärt:** Innentüren und Türanschläge (nicht gezeichnet), Treppenläufe, Aufzugsgröße, Brüstungs-/Sturzhöhen, Anbindung der Fahrgasse, Höhenbezug zur Stadt.

### B1–B3 (neue Idee, Ring)
- **Gesichert:** nur die Vorgabe selbst (EG 540 m² = 60 % der Hypothese 960 m², Vorbau ringsum, Staffel 0/1,50/3,00 m ab Außenkante OG1, Zielhöhe 12,00 m nicht bindend).
- **Angenommen (Entwurfsannahmen):** EG 20 × 27 m; Vorbau West 1,00 / Platz 1,50 / Rück 1,50 / Ost 5,00 m (über der Stellplatzreihe); 22 Säulen Ø 0,40 m; Höhenschema EG 4,30 / OG1 3,60 / oberstes Geschoss 3,60 / Attika 0,50 = 12,00 m (**hypothetisch**); EG-Raumzonen; Glasfront Gastro x 5–21; Eingangslagen; 8 Stellplätze; Zufahrt von Süden.
- **Ungeklärt:** Fenster, Türen, Brüstungen (nicht gezeichnet), Raumaufteilung und Kern in den Obergeschossen, Geschosshöhen, Deckenstärke (0,45 m Annahme), Grundstückszuschnitt, Lage der Straße/Zufahrt, Feuerwehrzufahrt unter dem Vorbau.

## 4. Dokumentierte Widersprüche (nicht stillschweigend korrigiert)

1. **B1–B3: Kern im EG (x 1–5, y 1,5–11) ≠ Kern-Streifen der Obergeschosse (y 0…4 über die volle Breite).** OG-Kern daher nicht gezeichnet.
2. **A: Balkone (y −1,50) und Vordach (y −3,60) ragen über die Hypothese-Grenze zum Platz.**
3. **A: Bar liegt innerhalb des Gastraum-Rechtecks** (verschachtelt; Raumflächensumme EG 590 m² statt 576 m²). Beide Rechtecke werden wie im Modell gezeichnet.
4. Höhen: A Attika +9,90 m (B3-Modell), B +12,00 m (hypothetisches Schema) – nicht vergleichbar bezogen; Höhenbezug der Stadt (OK Fahrbahn) offen.
5. Rechtsebenen (B-Plan Nr. 123 von 2023, rechtskräftig; Änderungsentwurf 2026 ohne Wirkung für MI 3; Hauptdach-Neigung ≥ 38° bei Flachdach/Staffel) sind auf Seite 11 jedes Pakets getrennt aufgeführt; **es wird keine Zulässigkeit festgestellt**. Dass Baufeld 3 = MI 3 / Flurstück 59/1 ist, ist unbestätigt.
6. Geändert gegenüber der ersten Fassung vom 27.10.2026: Die früheren B-Modelle (EG 18 × 30 m) hatten rückseitig keinen Vorbau, ragten 1,5 m über die Hypothese-Grenze und hatten zwei kollidierende Säulen. Das Ring-Modell (EG 20 × 27 m) erfüllt „Vorbau auf allen vier Seiten innerhalb der Grenze" und hat diese Konflikte nicht mehr.

Vollständige Protokolle: Seite 12 jedes Pakets.

## 5. Fehlende Angaben (bitte nachliefern, wenn verfügbar)

- Vermessener Grundstückszuschnitt und Baulinie zum Platz; Lage der Straße/Zufahrt.
- Höhenbezug (OK Fahrbahn) und Geländehöhe am Gebäude.
- Wand- und Deckenstärken, Konstruktionsraster der Säulen (B).
- Fenster-/Türliste mit Maßen, Türanschläge, Brüstungshöhen (B komplett, A Innentüren).
- Raumprogramm und Kernlage in den Obergeschossen (B); Treppen- und Aufzugsmaße.
- Bestätigung, ob Revitalyze Mehrseiten-/A2-Vektor-PDFs akzeptiert und ob Geschosse über Blattnamen oder Seitenreihenfolge erkannt werden.

## 6. Empfehlung für den Testlauf

1. `Test_EG_Vektor_Import.pdf` hochladen (eine Seite, A3, nur EG von A). Prüfen: Außenwände, Öffnungen (23 gesamt, im EG-Plan die Platz-/Rück-/Ost-Öffnungen), Räume, Maßstab (Maßstabsbalken 10 m = 100 mm).
2. Wenn der EG-Test brauchbar ist: Seite 2 von `A_B3_Referenz_Import.pdf`, danach Mehrseiten-Test (Seiten 2–9).
3. Erst dann B1–B3; deren Ergebnis hängt an den oben genannten Annahmen und fehlenden Öffnungsdaten.
