# Präsentationszeichnungen (Arbeitsstand OG-2, vorläufig)
Sechs A3-Blätter für die Projektbesprechung. Nur Darstellung; Geometrie und Design unverändert (Quelle: `geometry/building_design.json`, Wohnung: `scripts/unit_study.py`).
Jedes Blatt als SVG und PDF (Vektor, Schrift Inter eingebettet) sowie PNG mit 300 dpi. Gesamt-PDF: `Neue-Mitte-Werlte_Zeichnungen_Arbeitsstand_Gesamt.pdf`.
Neu erzeugen: `cd scripts/present && python3 plan.py og1 staffel eg && python3 views.py elevation section unit`, danach `NODE_PATH=<node_modules> node export.js ../../praesentation_zeichnungen/0*.svg`.
Die Skripte prüfen automatisch auf Texte außerhalb des Blatts und Textüberlagerungen. Fenster-, Tür- und Wandmaße sind nicht festgelegt und daher nicht oder nur als schematische Lage dargestellt. Alle offenen Konflikte stehen auf den Blättern; keiner gilt als gelöst.
Gegenüber den früheren Arbeitsständen korrigiert (nur Darstellung nach Quelldaten): Staffel-Fassade reicht bis zum Kern (x 0,8–31,2); der Schnitt bei x = 18 schneidet Bar und WC, nicht die Küche.
