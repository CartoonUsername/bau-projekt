# Varianten A, B, C (hypothetisch, keine Variante festgelegt)
Blatt 7–9: je Variante Erdgeschoss mit Stellplätzen, 1. Obergeschoss, 3. Geschoss und Schnitt (M 1:250). Blatt 10: Vergleichstabelle. SVG, PDF (Vektor) und PNG (300 dpi); Gesamt-PDF `Varianten_ABC_Gesamt.pdf`.
Neu erzeugen: `python3 scripts/variants/build_variants.py && python3 scripts/variants/metrics_variants.py && cd scripts/present && python3 variants_sheets.py A B C table`, danach `node export.js ../../varianten/*.svg`.
Beschreibung, Annahmen und Konflikte: `documentation/varianten_ABC.md`.
