# Entwurfsstudie Gebäudekonzepte Baufeld 3 (keine Variante festgelegt)

- `Vergleich_Gebaeudekonzepte.pdf` – Vergleichs-PDF (Maße, Flächen, Wohnungen, Baurecht-Ampel, Konstruktion, Prüfbedarf)
- `Variante_A…D_*.pdf` – je Variante: Steckbrief, 3D, Fassaden, Grundrisse, Schnitt
- `Foerderung_Variantenvergleich.pdf` – Förder-Orientierung (keine Zusage)
- `varianten_daten.json` – gemeinsame Datenbasis; erzeugt mit `scripts/studie/` (varianten.py → blender_studie.py, zeichne_plaene.py → baue_pdfs.py, baue_foerderung.py)
- B3 (`scripts/modell_b3.py`) und die bisherigen PDFs bleiben unverändert; Variante A = B3.
- Alle Werte vorläufig; Grundstück 32 × 30 m ist Hypothese H1.

## Ergänzung: Variante E (12 m, umlaufender Vorbau, Parken)
- `Entwurf_E_12m_Umlaufender_Vorbau_mit_Parken.pdf` – Höhenrahmen, Lageplan, Grundrisse, vier Fassaden, Schnitt für E1–E4
- `Vergleich_E_mit_B_und_C.pdf` – Vergleichstabelle und Einordnung
- Quellen: `scripts/studie/varianten_e.py`, `e_zeichnen.py`, `baue_pdfs_e.py`; Grundstück als `PLOT_POLY` austauschbar (aktuell Hypothese 32 × 30 m)

## Überarbeitung 24.10.2026 (Stellplätze nach § 47 NBauO, Variante F mit EG 540 m²)
- `Entwurf_E_12m_Umlaufender_Vorbau_mit_Parken.pdf` (E1–E4, neu gerechnet) und `Entwurf_F_EG540m2_Umlaufender_Vorbau_Parken.pdf` (F1–F4)
- `Stellplatzberechnung_NBauO47.pdf` – gesetzlich erforderlich (Gastro + Büro) und optional (Wohnen) getrennt
- `Vergleich_E_F_B_C.pdf` ersetzt `Vergleich_E_mit_B_und_C.pdf`
- Quellen: `../quellen_stadt/` (Fotos der städtischen Seiten 13/15/16 fehlen noch)
- Code: `scripts/studie/parken.py` (Parkprüfung), `varianten_f.py`, `e_zeichnen.py`, `baue_pdfs_ef.py`

## Planstände und Baufeld 3 (24.10.2026)
- `Entscheidung_Planstaende_Baufeld3_Variante_F.pdf` – zwei Planstände (rechtskräftig 2023 / Entwurf 2026), Baufeld-3-Zuordnung (MI 3, unbestätigt), Grundstücksrisiken, Auswirkungen auf F1–F4, Prüfgeometrien G1–G3
- Code: `scripts/studie/entscheidung_pdf.py`, `varianten_g.py`; Quellen: `../quellen_stadt/`

## Vergleichsstudie A gegen B (27.10.2026)
- `Vergleichsstudie_A_B3_gegen_B_Neue_Idee.pdf` – Variante A = unveränderter B3-Entwurf, Variante B = neue Idee (EG 540 m², umlaufender Vorbau, drei Rücksprung-Optionen = Modelle F1–F3); je 3D, Ansichten, Grundrisse, Schnitt, Lageplan; Baufeld-3-Prüfung nach Planstand; Vergleichstabelle
- Code: `scripts/studie/vergleichsstudie_ab.py`

## Revitalyze-Import-PDFs (27.10.2026)
- `revitalyze_import/` – technische Vektor-PDFs (1:100, A2 quer; Test-PDF A3) für einen PDF-zu-IFC-Test: A (B3-Referenz), B1–B3 (540 m², Staffel 0/1,50/3,00 m), `Test_EG_Vektor_Import.pdf`, `PDF_Import_Checkliste.md` (gesichert/angenommen/ungeklärt).
- Code: `scripts/studie/revitalyze_modelle.py` (Modelle, Konsistenzprüfung), `revitalyze_pdfs.py` (reportlab).

## Zwei getrennte Gesamtpräsentationen (27.10.2026)
- `Praesentation_A_Standard_B3.pdf` – Standardversion = bisheriger B3-Entwurf, unverändert (13 Seiten).
- `Praesentation_B_Ueberdachte_Stellplaetze_Mehr_Wohnflaeche.pdf` – Version mit überdachten Stellplätzen und größeren/mehr Wohnflächen, drei Rücksprung-Optionen, keine Festlegung (22 Seiten).
- Code: `scripts/studie/praesentation_ab.py` (nutzt die Bausteine von `vergleichsstudie_ab.py`).
