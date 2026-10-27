# Varianten Version 2 (Gastronomie groß, Büros kompakt, abgestufte Wohngeschosse), hypothetisch
Blätter 11–16: je Variante Grundrisse EG, 1. OG, 3. Geschoss, Schnitt (M 1:250) und schematische Ansichten Platzseite, Rückseite, Kernseite, Ostseite. Blatt 17: Vergleich. SVG, PDF (Vektor), PNG (300 dpi), Gesamt-PDF `Varianten_v2_ABC_Gesamt.pdf`.
Ersetzt `varianten/` (erste Fassung, bürolastig). Beschreibung: `documentation/varianten_v2_ABC.md`.
Neu erzeugen: `python3 scripts/variants2/build_variants2.py && python3 scripts/variants2/metrics2.py && cd scripts/present && python3 variants2_sheets.py pA vA pB vB pC vC table`, danach `node export.js ../../varianten_v2/*.svg`.
