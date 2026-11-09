# Businessplan-Pakete Baufeld 3 (27.10.2026)
Zwei getrennte Pakete im Aufbau des früheren Bankplans (33 Folien, Businessplan-DOCX, Kosten-Nutzen pro Kopf):
- **A – Standardversion (B3):** `Businessplan_Praesentation_A.pptx`, `Businessplan_A.docx`, `Kosten_Nutzen_pro_Kopf_A.pdf`
- **B – überdachte Stellplätze, schmales EG, breitere Obergeschosse (3 Optionen B1/B2/B3):** `Businessplan_Praesentation_B.pptx`, `Businessplan_B.docx`, `Kosten_Nutzen_pro_Kopf_B.pdf`
- `bilder/hf_*`: KI-Visualisierungen (Higgsfield, Modell nano_banana_pro, Referenz = Geometrie-Renderings aus `studie_gebaeudeformen/*/ansichten`); `gastro_*.jpg` aus dem früheren Gastro-Konzept.
- Code: `finanz.py` (Rechenmodell, an den früheren Plan angelehnt: Nachrechnung Gesamtkosten −0,2 %), `varianten_in.py`, `build_deck.py`, `build_docs.py`.
Alle Zahlen sind Planungsannahmen; Gastro-Umsatz proportional zu den Innenplätzen; Höhen bei B hypothetisch; keine Aussage zur Zulässigkeit, keine Variante festgelegt.

## Bilder Variante B im Stil der früheren Bilder (27.10.2026)
`bilder/neu/B1|B2|B3_{hero,detail,east}.jpg`, `B2|B3_roof.jpg` (Higgsfield, nano_banana_pro): Geometrie-Referenz = korrigierte Hero-Renderings, Stil-Referenz = Bilder aus dem früheren Bankplan (Eckansicht, Arkadendetail, Dachterrasse). Alternativen in `bilder/neu/alt/`. Gastro-Innenansichten bleiben die früheren Bilder (`gastro_*.jpg`).

## Umstellung auf Variante R (Vorbau ringsum, EG 540 m²)
Businessplan B (Deck, DOCX, Kosten-Nutzen) rechnet mit R1–R3 (`scripts/studie/varianten_r.py`); Bilder in `bilder/neu_r/` (Tonmodell-Referenz `clay.py` → Higgsfield-Luftbild → Augenhöhen-Ansichten; Ansichten als Vektor→PNG `elev_png.py`). `bilder/neu/` (F-Modelle) ist überholt.
