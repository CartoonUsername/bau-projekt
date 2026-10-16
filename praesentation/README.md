# Neue Mitte Werlte, Baufeld 3: Konzept mit 3 Ebenen

Große Gastro mit Bar im ganzen Erdgeschoss, darüber 6 Wohnungen (1. OG und Staffelgeschoss in Holzbau mit Terrasse rundum), 930 m² BGF, Flachdach.

| Datei | Inhalt |
|---|---|
| `Neue-Mitte-Werlte_Baufeld3_6-Wohnungen_Gastro-EG.pptx` | Präsentation für Stadt und Bank, 25 Folien |
| `Neue-Mitte-Werlte_Baufeld3_6-Wohnungen_Gastro-EG.pdf` | dieselbe Präsentation als PDF zum Versenden |
| `Rechenmodell_Baufeld3.xlsx` | Rechenmodell mit Formeln (Annahmen, Kosten, Kredit, Cashflow), dazu Szenarien |
| `bilder/` | KI-Visualisierungen (`ki_*.jpg`), Skizzen (`skizze_*`), Referenzbilder, `BILDPROMPTS.md` |
| `model.js` | Rechenmodell im Code (Quelle der Zahlen in der Präsentation) |
| `build_deck_sechs.js` | erzeugt die Präsentation (`NODE_PATH=<node_modules> APPLY_THEME=<pfad> node build_deck_sechs.js`) |
| `build_modell_xlsx.py`, `dump_szenarien.js` | erzeugen die Excel-Datei |

Alle Zahlen sind Planungsannahmen: Baukosten 2.700 €/m², Förderung als Zuschuss, Miete 950 € je Wohnung, Gastro-Marge nach Branchen-Richtwerten.

## Stand Oktober 2026: Baukosten und Verkauf an die Familie
- Grundlage jetzt: Baukosten 2.200 €/m² BGF (Annahme des Bauherrn), Gastro-Ausbau 150.000 €, Staffelgeschoss in Holzbau mit Terrasse rundum, 930 m² BGF.
- Folie "Verkauf an die Familie": Rechnung je Partei mit eigenem Kredit ohne Eigenkapital (auch Blatt "Verkauf je Partei" in der Excel-Datei).
- Folie "Variante B" im Anhang: 540 m² Grundfläche, 1.500 m² BGF (nur mit Ausnahme der Stadt).

## Alternativen (separate Ausarbeitungen)
- `Neue-Mitte-Werlte_Baufeld3_Airbnb-Apartments.pptx`: 6 Apartments (Kurzzeitvermietung) statt Dauermiete, Gastro im EG.
- `Neue-Mitte-Werlte_Baufeld3_Hotel-und-Gastro.pptx`: Hotel mit 15 Zimmern über der Gastro.
- Rechnung in `model_alt.js`, Gastro-Konzept in `build_deck_gastro.js`, Folien in `build_deck_optionen.js` (eine Präsentation für Dauermiete, Airbnb und Hotel auf Basis Variante B). Preise, Auslastung und Kostenquoten sind Annahmen, belastbare Werte für Werlte fehlen.

## Finale Präsentation (Variante A, ohne Förderung)
- Basis: 340 m² Grundfläche, EG Gastro, 6 Dauermietwohnungen, 2.200 €/m², Gastro-Ausbau 150.000 €, ohne Förderung, ohne Lohn des Bauherrn.
- Verkaufsplan an Verwandte (Folie 20) und im Excel-Blatt "Verkauf je Partei": Staffel zum Selbstkostenpreis, OG-Wohnungen von Vater und Bruder mit Nachlass, Käufer tilgungsfrei.
- Bilder: `bilder/ki_*.jpg` (Theke `ki_innen_2.jpg` farblich nachbearbeitet, Original in `bilder/alt/`).

- Bilder (16.10.): alle fünf KI-Bilder (`bilder/ki_*.jpg`) mit Higgsfield neu erzeugt (Milchglas-Brüstungen, Holz-Penthouse, anthrazitfarbene Theke); die retuschierten Vorversionen liegen in `bilder/alt/retusche/`.
- `package.json` in `praesentation/` setzt CommonJS, weil das Hauptverzeichnis ein TypeScript-Modulprojekt (Higgsfield-SDK) ist.
