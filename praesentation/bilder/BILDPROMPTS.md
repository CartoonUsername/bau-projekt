# Bildprompts Baufeld 3, Neue Mitte Werlte (für Nano Banana Pro / Higgsfield)

Die Higgsfield-Verbindung in der Sitzung kann nur Modelle und fertige Ergebnisse anzeigen, nicht erzeugen.
Die Prompts sind deshalb zum Einfügen in Higgsfield (Nano Banana Pro) gedacht.

**Referenzbilder mit hochladen:**
- `aussen.jpg` (Stil: Klinker, Balkone, Glas-EG) und `innen.jpg` (Stimmung, Materialien)
- `skizze_aussen_ecke.png` und `skizze_aussen_ansichten.png` als Geometrie-Vorgabe (Staffelgeschoss, Fensterachsen)
- Hinweis im Prompt: "Use image 1 for style, use the sketch for the exact massing and proportions"

**Feste Faktoren (in jedem Prompt enthalten):**
Gebäude ca. 24 × 14,2 m (Staffel ca. 21,4 × 11,6 m, rundum 1,3 m zurück), EG komplett große Gastro mit Bar und vollverglaster Fassade, darüber 1. OG mit drei Wohnungen
und ein zurückgesetztes Staffelgeschoss mit drei Wohnungen (insgesamt 6), Flachdach, Hauptbaukörper 6,50 m, Gesamthöhe ca. 9,90 m,
dunkles Langformat-Klinker, schwarze Stahlrahmen, Milchglas-Brüstungen (satiniertes Glas), Holzbau-Staffelgeschoss mit Lärchenfassade und Terrasse rundum, Holzterrasse mit Vordach,
Stellplätze und rotes Pflaster rechts, norddeutsche Kleinstadt (Werlte, Emsland), Stil 2026, kein Landhaus, keine Satteldach.

---

## 1. Außen, Eckansicht, Abendstimmung

```
Photorealistic architectural visualization of a new contemporary mixed-use corner building in a small north-German
town centre (Werlte, Emsland), 2026. Three levels: a fully glazed ground floor with black slim steel frames (large
restaurant and bar, warm interior light, wooden terrace with outdoor tables under a flat steel canopy), one upper
floor in dark long-format red-brown clinker brick with floor-to-ceiling windows, concrete bands and projecting
balconies with frosted (milk) glass balustrades, and a set-back top floor of timber construction clad in warm larch wood and glass, set back evenly on all four sides with a continuous wraparound roof terrace with frosted (milk) glass balustrade and planters.
Flat roof with a slim concrete fascia, total height about 10 metres, no pitched roof, not a farmhouse style.
Red brick paving, young street trees, public car parking on the right. Blue hour, soft clouds, glowing windows.
Wide angle, eye level, from the south-east corner. Architectural photography, high detail, no text.
```

## 2. Außen, Tag, Straßenansicht

```
Photorealistic daytime street view of a modern three-level mixed-use building with a set-back top floor, dark clinker
brick facade, large black-framed windows, balconies with frosted (milk) glass railings, fully glazed restaurant ground floor with
a wooden terrace and café tables, flat roof, town hall square in Werlte (Emsland) with red paving, trees and parking
spaces, partly cloudy sky, soft natural light. Frontal elevation-like view, 35 mm lens. No pitched roof, no extra
storey, no text.
```

## 3. Innen, Restaurant mit Bar (Stil wie Referenzbild innen.jpg)

```
Photorealistic interior of a new modern restaurant with a bar, evening mood, warm and cosy but contemporary (2026).
Dark olive-green walls with elegant wainscot panelling, cognac-coloured channel-tufted velvet banquettes along the
walls with burgundy velvet cushions, solid oak tables with black pedestal bases, velvet chairs in taupe, ribbed glass
table lamps with candles, glass pendant lamps with brass caps, oval and arched mirrors, a large dried pampas grass
wall arrangement, dark red accent lamp, a black steel-framed glass partition with grid pattern, indirect cove lighting
along the ceiling, floor-to-ceiling windows to a town square with red brick paving at blue hour, a long oak bar with
a dark green fluted front and a lit back bar in the background, guests softly blurred. Use image 1 as the exact style
reference (colours, materials, mood). Wide-angle interior photography, high detail, no text, no logos.
```

## 4. Innen, Theke und Sitzecke (Stil wie Referenzbild)

```
Photorealistic close-up of a bar counter in solid oak with a dark green fluted front and black bar stools, behind it
dark olive-green panelled wall with an arched mirror, a small lit niche with a red back wall and bottles, glass
pendant lamps, in front of it cognac velvet banquettes with burgundy cushions and oak tables with ribbed glass
candle lamps, black steel-glass partition in the background, evening mood, shallow depth of field, use image 1 as
the exact style reference, high detail, no text, no logos.
```

## 5. Dachterrasse im Staffelgeschoss (optional)

```
Photorealistic view of a roof terrace of a set-back top-floor apartment, floor-to-ceiling glazing with black frames,
warm larch timber cladding, wooden decking, frosted (milk) glass balustrade, planters, view over the red-brown roofs of a small north-German
town and the church tower, golden hour. Flat roof, no pitched roof, no text.
```

---

## Hinweise
- Die Zahlen stehen als Faktoren im Prompt, KI-Bilder sind keine Planung: Sie halten Maße nur ungefähr ein.
- Wenn die Form abweicht: Skizze `skizze_aussen_ecke.png` als erstes Bild setzen und "keep exactly the massing of image 1" ergänzen.
- **Dateinamen für den Einbau** (in `praesentation/bilder/` speichern, dann `build_deck_sechs.js` neu laufen lassen, die Folie "Visualisierungen" und das Titelbild entstehen automatisch):
  - `ki_aussen_1.jpg` (Prompt 1, wird auch Titelbild), `ki_aussen_2.jpg` (Prompt 2)
  - `ki_innen_1.jpg` (Prompt 3), `ki_innen_2.jpg` (Prompt 4)
