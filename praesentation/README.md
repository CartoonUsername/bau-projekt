# Neue Mitte Werlte, Baufeld 3: Businessplan für die Bank

Große Gastro (510 m²) im ganzen Erdgeschoss, darüber im 1. OG zwei Ankermieter-Büros (100 m² und 65 m²) und 3 Wohnungen, im Staffelgeschoss 5 Wohnungen (8 Wohnungen, Holzbau), 576 m² Grundfläche (GRZ-Maximum), 1.650 m² BGF, 100 % Fremdfinanzierung mit KfW 297, 298, 299 und Hausbank (Gesamtkosten 4,85 Mio €, Mischzins 3,39 %, Rate 17.733 €/Monat).

| Datei | Inhalt |
|---|---|
| `Businessplan_Baufeld3_Neue-Mitte-Werlte.docx` (+ `.pdf`) | Businessplan für die Bank (Word, ca. 9 Seiten) |
| `Bankunterlagen_Baufeld3.xlsx` | Rechenmodell mit Formeln: Annahmen, Flächen und Mieten, Kosten und Finanzierung, Bauphase, Abzahlungsplan (monatlich und jährlich), Ertrag und Cashflow, Gastro-Betrieb, Ertragswert, Prognose, Belastungstest, Airbnb-Prüfung, Checkliste Bankunterlagen |
| `Neue-Mitte-Werlte_Baufeld3_8-Wohnungen_Grosse-Gastro-EG.pptx` (+ `.pdf`) | Präsentation für Bank und Stadt |
| `Neue-Mitte-Werlte_Baufeld3_Gastro-Konzept.pptx` (+ `.pdf`) | Gastro: Gestaltung, Grundriss, Speisekarte, Umsatz, Personal |
| `bilder/` | KI-Visualisierungen (`ki_*.jpg`), Skizzen, Referenzbilder, `BILDPROMPTS.md` |

## Erzeugung (Reihenfolge)
1. `python3 build_bank_xlsx.py Bankunterlagen_Baufeld3.xlsx`, danach Formeln berechnen: `python3 <xlsx-skill>/scripts/recalc.py Bankunterlagen_Baufeld3.xlsx`
2. `python3 export_bank_values.py` schreibt `bank_values.json` (alle Zahlen für Präsentation und Word)
3. `NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_deck_sechs.js` (Hauptpräsentation) und `node build_deck_gastro.js`
4. `python3 build_businessplan_docx.py Businessplan_Baufeld3_Neue-Mitte-Werlte.docx`

`model.js` enthält die Geometrie und das frühere Einzelzins-Modell (nur noch für wenige Hilfswerte, z. B. Gastro-Ausbau-Hinweis).

## Annahmen (alle im Blatt "Annahmen", blau)
Baukosten 2.200 €/m², Holz-Staffel 400 €/m² günstiger, Baunebenkosten 15 %, Mehrkosten Effizienzhaus 40/QNG 3 %, Gastro-Ausbau 150.000 €, Miete 11,18 €/m², Pacht 12 €/m², Gastro-Umsatz 50.000 € bei 30,5 % Marge, Rücklagen 10 %, KfW 297/298 2,5 %, KfW 299 3,0 %, Hausbank 4,0 %, Anfangstilgung 1 %, 15 Monate Bau, 12 Monate tilgungsfreie Anlaufzeit. KfW-Zinsen und -Rahmen sind Stand Ratgeber Oktober 2026 und bei Hausbank/KfW zu bestätigen. Ergebnis: Beleihungsauslauf ca. 163 %, die Bank verlangt zusätzliche Sicherheiten oder Eigenkapital.
