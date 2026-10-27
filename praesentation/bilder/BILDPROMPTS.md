# Bildprompts Baufeld 3, Neue Mitte Werlte (für Nano Banana Pro / Higgsfield)

Die Higgsfield-Verbindung in der Sitzung kann nur Modelle und fertige Ergebnisse anzeigen, nicht erzeugen.
Die Prompts sind deshalb zum Einfügen in Higgsfield (Nano Banana Pro) gedacht.

**Referenzbilder mit hochladen:**
- `aussen.jpg` (Stil: Klinker, Balkone, Glas-EG) und `innen.jpg` (Stimmung, Materialien)
- `skizze_aussen_ecke.png` und `skizze_aussen_ansichten.png` als Geometrie-Vorgabe (Staffelgeschoss, Fensterachsen)
- Hinweis im Prompt: "Use image 1 for style, use the sketch for the exact massing and proportions"

**Feste Faktoren (in jedem Prompt enthalten):**
Gebäude ca. 24 × 14,2 m (Staffel ca. 22,4 × 12,6 m, rundum nur 0,8 m zurück, also fast so groß wie das Geschoss darunter), EG komplett große Gastro mit Bar und vollverglaster Fassade, darüber 1. OG mit drei Wohnungen
und ein zurückgesetztes Staffelgeschoss mit drei Wohnungen (insgesamt 6), Flachdach, Hauptbaukörper 6,50 m, Gesamthöhe ca. 9,90 m,
dunkles Langformat-Klinker, schwarze Stahlrahmen, Milchglas-Brüstungen (satiniertes Glas), großes Holzbau-Staffelgeschoss mit Lärchenfassade und nur schmalem Terrassenumlauf (ca. 0,8 m), Holzterrasse mit Vordach,
Stellplätze und rotes Pflaster rechts, norddeutsche Kleinstadt (Werlte, Emsland), Stil 2026, kein Landhaus, keine Satteldach.

---

## 1. Außen, Eckansicht, Abendstimmung

```
Photorealistic architectural visualization of a new contemporary mixed-use corner building in a small north-German
town centre (Werlte, Emsland), 2026. Three levels: a fully glazed ground floor with black slim steel frames (large
restaurant and bar, warm interior light, wooden terrace with outdoor tables under a flat steel canopy), one upper
floor in dark long-format red-brown clinker brick with floor-to-ceiling windows, concrete bands and projecting
balconies with frosted (milk) glass balustrades, and a large top floor of timber construction clad in warm larch wood and glass, set back only 0.8 m on all four sides so it covers about 82% of the floor below, with just a very narrow walkway (0.8 m) around it behind a frosted (milk) glass balustrade, no furniture, no large terrace.
Flat roof with a slim concrete fascia, total height about 10 metres, no pitched roof, not a farmhouse style.
Red brick paving, young street trees, public car parking on the right. Blue hour, soft clouds, glowing windows.
Wide angle, eye level, from the south-east corner. Architectural photography, high detail, no text.
```

## 2. Außen, Tag, Straßenansicht

```
Photorealistic daytime street view of a modern three-level mixed-use building with a large top floor of timber construction clad in warm larch wood, set back only 0.8 m with a narrow walkway and no garden furniture, dark clinker
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
an anthracite (charcoal) fluted front and a lit back bar in the background, guests softly blurred. Use image 1 as the exact style
reference (colours, materials, mood). Wide-angle interior photography, high detail, no text, no logos.
```

## 4. Innen, Theke und Sitzecke (Stil wie Referenzbild)

```
Photorealistic close-up of a bar counter in solid oak with an anthracite (charcoal) fluted front and black bar stools, behind it
dark olive-green panelled wall with an arched mirror, a small lit niche with a red back wall and bottles, glass
pendant lamps, in front of it cognac velvet banquettes with burgundy cushions and oak tables with ribbed glass
candle lamps, black steel-glass partition in the background, evening mood, shallow depth of field, use image 1 as
the exact style reference, high detail, no text, no logos.
```

## 5. Schmaler Terrassenumlauf am Holzgeschoss (optional)

```
Photorealistic close view of the narrow 0.8 m walkway around a large timber top-floor apartment: floor-to-ceiling
glazing with black frames, warm larch timber cladding, simple wooden decking, frosted (milk) glass balustrade, at most
one small planter and no furniture, no loungers, no wellness look, view over the red-brown roofs of a small
north-German town, soft daylight. Flat roof, no pitched roof, no text.
```

---

## Hinweise
- Die Zahlen stehen als Faktoren im Prompt, KI-Bilder sind keine Planung: Sie halten Maße nur ungefähr ein.
- Wenn die Form abweicht: Skizze `skizze_aussen_ecke.png` als erstes Bild setzen und "keep exactly the massing of image 1" ergänzen.
- **Dateinamen für den Einbau** (in `praesentation/bilder/` speichern, dann `build_deck_sechs.js` neu laufen lassen, die Folie "Visualisierungen" und das Titelbild entstehen automatisch):
  - `ki_aussen_1.jpg` (Prompt 1, wird auch Titelbild), `ki_aussen_2.jpg` (Prompt 2)
  - `ki_innen_1.jpg` (Prompt 3), `ki_innen_2.jpg` (Prompt 4)

---

## Stand Oktober 2026: 12 Wohnungen (Renderings Außen und Wohnungen)

Feste Details für alle Bilder (Gebäude muss überall gleich aussehen):
- 1. OG: dunkler braun-violetter Langformat-Klinker, graue Betonbänder, schwarze Stahlfenster, 5 auskragende Balkone aus grauem Beton mit Milchglas-Brüstung (Betonboden, kein Holzdeck)
- Staffelgeschoss: Lärchenholz, Fenster mit hellen Holzrahmen, 7 schmale Fensterachsen, nur ca. 0,8 m breiter Umlauf mit grauem Boden hinter durchgehender Milchglas-Brüstung
- EG: vollverglaste Gastro mit schwarzem Stahlvordach und Holzterrasse
- Außenbilder: `ki_aussen_1.jpg` (Blaue Stunde), `ki_aussen_2.jpg` (Tag); Wohnungen: `ki_wohnung_og.jpg` (ca. 64 m²), `ki_wohnung_staffel.jpg` und `ki_wohnung_schlafen.jpg` (ca. 48 m²), `ki_wohnung_balkon.jpg`
- Die Wohnungsbilder wurden mit der Tagesansicht als Referenzbild (image_references) erzeugt.
