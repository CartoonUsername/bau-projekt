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
