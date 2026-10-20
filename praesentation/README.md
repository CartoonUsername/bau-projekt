# Neue Mitte Werlte, Baufeld 3: Businessplan für die Bank

Restaurant und Bar (510 m², eigene Betreiberfirma, Pacht 10 % vom Umsatz) im ganzen Erdgeschoss, darüber 2 Ankermieter-Büros und 12 Wohnungen (5 im 1. OG, 7 im Staffelgeschoss in Holzbau), 576 m² Grundfläche (GRZ-Maximum), 1.650 m² BGF. Eigentümerin ist eine Vermietungs-GbR, Finanzierung Basis 100 % Fremdkapital mit KfW 297, 298, 299 und Hausbank. Vergleich mit 8 Wohnungen und mit Eigenkapital im Excel-Blatt Szenarien (`build_szenarien.py`, `rechenkern.py` = unabhängiger Nachbau zur Gegenprüfung).

| Datei | Inhalt |
|---|---|
| `Businessplan_Baufeld3_Neue-Mitte-Werlte.docx` (+ `.pdf`) | Businessplan für die Bank (Word, ca. 9 Seiten) |
| `Bankunterlagen_Baufeld3.xlsx` | Rechenmodell mit Formeln: Annahmen, Flächen und Mieten, Kosten und Finanzierung, Bauphase, Abzahlungsplan (monatlich und jährlich), Ertrag und Cashflow, Gastro-Betrieb, Ertragswert, Prognose, Belastungstest, Airbnb-Prüfung, Checkliste Bankunterlagen |
| `Neue-Mitte-Werlte_Baufeld3_12-Wohnungen_Restaurant-Bar.pptx` (+ `.pdf`) | Präsentation für Bank und Stadt |
| `Neue-Mitte-Werlte_Baufeld3_Gastro-Konzept.pptx` (+ `.pdf`) | Gastro: Gestaltung, Grundriss, Speisekarte, Umsatz, Personal |
| `bilder/` | Renderings (`ki_*.jpg`), Skizzen, Referenzbilder, `BILDPROMPTS.md` |

## Erzeugung (Reihenfolge)
1. `python3 build_bank_xlsx.py Bankunterlagen_Baufeld3.xlsx`, danach Formeln berechnen: `python3 <xlsx-skill>/scripts/recalc.py Bankunterlagen_Baufeld3.xlsx`
2. `python3 export_bank_values.py` schreibt `bank_values.json` (alle Zahlen für Präsentation und Word)
3. `NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_deck_sechs.js` (Hauptpräsentation) und `node build_deck_gastro.js`
4. `python3 build_businessplan_docx.py Businessplan_Baufeld3_Neue-Mitte-Werlte.docx`

`model.js` enthält die Geometrie und das frühere Einzelzins-Modell (nur noch für wenige Hilfswerte, z. B. Gastro-Ausbau-Hinweis).

## Annahmen (alle im Blatt "Annahmen", blau)
Baukosten 2.200 €/m², Holz-Staffel 400 €/m² günstiger, Baunebenkosten 15 %, Mehrkosten Effizienzhaus 40/QNG 3 %, Gastro-Ausbau 150.000 €, Miete 11,18 €/m², Pacht 12 €/m², Gastro-Umsatz 50.000 € bei 30,5 % Marge, Rücklagen 10 %, KfW 297/298 2,5 %, KfW 299 3,0 %, Hausbank 4,0 %, Anfangstilgung 1 %, 15 Monate Bau, 12 Monate tilgungsfreie Anlaufzeit. KfW-Zinsen und -Rahmen sind Stand Ratgeber Oktober 2026 und bei Hausbank/KfW zu bestätigen. Ergebnis: Beleihungsauslauf ca. 163 %, die Bank verlangt zusätzliche Sicherheiten oder Eigenkapital.
