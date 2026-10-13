# Bildprompts Baufeld 3, Neue Mitte Werlte (für Nano Banana Pro / Higgsfield)

Die Higgsfield-Verbindung in der Sitzung kann nur Modelle und fertige Ergebnisse anzeigen, nicht erzeugen.
Die Prompts sind deshalb zum Einfügen in Higgsfield (Nano Banana Pro) gedacht.

**Referenzbilder mit hochladen:**
- `aussen.jpg` (Stil: Klinker, Balkone, Glas-EG) und `innen.jpg` (Stimmung, Materialien)
- `skizze_aussen_ecke.png` und `skizze_aussen_ansichten.png` als Geometrie-Vorgabe (Staffelgeschoss, Fensterachsen)
- Hinweis im Prompt: "Use image 1 for style, use the sketch for the exact massing and proportions"

**Feste Faktoren (in jedem Prompt enthalten):**
Gebäude ca. 24 × 14,2 m, EG komplett große Gastro mit Bar und vollverglaster Fassade, darüber 1. OG mit drei Wohnungen
und ein zurückgesetztes Staffelgeschoss mit drei Wohnungen (insgesamt 6), Flachdach, Hauptbaukörper 6,50 m, Gesamthöhe ca. 9,90 m,
dunkles Langformat-Klinker, schwarze Stahlrahmen, Glasbrüstungen, Zink am Staffelgeschoss, Holzterrasse mit Vordach,
Stellplätze und rotes Pflaster rechts, norddeutsche Kleinstadt (Werlte, Emsland), Stil 2026, kein Landhaus, keine Satteldach.

---

## 1. Außen, Eckansicht, Abendstimmung

```
Photorealistic architectural visualization of a new contemporary mixed-use corner building in a small north-German
town centre (Werlte, Emsland), 2026. Three levels: a fully glazed ground floor with black slim steel frames (large
restaurant and bar, warm interior light, wooden terrace with outdoor tables under a flat steel canopy), one upper
floor in dark long-format red-brown clinker brick with floor-to-ceiling windows, concrete bands and projecting
balconies with glass balustrades, and a set-back top floor clad in dark zinc and glass with roof terraces and planters.
Flat roof with a slim concrete fascia, total height about 10 metres, no pitched roof, not a farmhouse style.
Red brick paving, young street trees, public car parking on the right. Blue hour, soft clouds, glowing windows.
Wide angle, eye level, from the south-east corner. Architectural photography, high detail, no text.
```

## 2. Außen, Tag, Straßenansicht

```
Photorealistic daytime street view of a modern three-level mixed-use building with a set-back top floor, dark clinker
brick facade, large black-framed windows, balconies with glass railings, fully glazed restaurant ground floor with
a wooden terrace and café tables, flat roof, town hall square in Werlte (Emsland) with red paving, trees and parking
spaces, partly cloudy sky, soft natural light. Frontal elevation-like view, 35 mm lens. No pitched roof, no extra
storey, no text.
```

## 3. Innen, Bar und Restaurant (modern, 2026)

```
Photorealistic interior of a new modern restaurant and bar, evening mood, about 290 square metres, 100 seats.
Long illuminated back bar with brass shelves and bottles, terrazzo bar counter with oak front and black stools,
dark green walls, brass pendant lamps, cove lighting along the ceiling, cream bouclé lounge seating and cognac
leather banquettes, solid oak tables with ribbed glass lanterns, black steel and glass partition with grid pattern,
floor-to-ceiling windows to a town square at blue hour, lush green plants, guests softly blurred. Use image 1 as
style reference. Wide-angle interior photography, warm and upscale, high detail, no text, no logos.
```

## 4. Innen, Theke

```
Photorealistic close-up of a terrazzo and oak bar counter with black bar stools in front of a lit back bar with
brass shelves and bottles, dark green wall, three brass pendant lamps, arched mirror, warm candle light, restaurant
guests blurred in the background, glass partition with black steel frame. Evening mood, shallow depth of field,
high detail, no text, no logos.
```

## 5. Dachterrasse im Staffelgeschoss (optional)

```
Photorealistic view of a roof terrace of a set-back top-floor apartment, floor-to-ceiling glazing with black frames,
dark zinc cladding, wooden decking, glass balustrade, planters, view over the red-brown roofs of a small north-German
town and the church tower, golden hour. Flat roof, no pitched roof, no text.
```

---

## Hinweise
- Die Zahlen stehen als Faktoren im Prompt, KI-Bilder sind keine Planung: Sie halten Maße nur ungefähr ein.
- Wenn die Form abweicht: Skizze `skizze_aussen_ecke.png` als erstes Bild setzen und "keep exactly the massing of image 1" ergänzen.
- Fertige Bilder bitte in `praesentation/bilder/` speichern, dann baue ich sie in die Präsentation ein.
