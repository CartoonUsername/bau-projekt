# Bildprompts Baufeld 3, Neue Mitte Werlte (für Nano Banana Pro / Higgsfield)

Die Higgsfield-Verbindung in dieser Sitzung kann nur Modelle und fertige Ergebnisse anzeigen, nicht erzeugen.
Die Prompts sind deshalb zum Einfügen in Higgsfield (Nano Banana Pro) gedacht.

**Referenzbilder mit hochladen:**
- `aussen.jpg` (Stil, Klinker, Glas-EG) und `innen.jpg` (Stimmung, Materialien)
- `skizze_aussen_ecke.png` und `skizze_aussen_ansichten.png` als Geometrie-Vorgabe (Dachform, Fenster, Loggien)
- Hinweis im Prompt: "Use image 1 for style, use the sketch for the exact roof shape and proportions"

**Feste Faktoren (in jedem Prompt enthalten):**
Gebäude ca. 24 × 14 m, drei Ebenen (EG, 1. OG, Dachgeschoss), Satteldach ca. 38° Neigung, Traufe 6,50 m,
First 12,00 m, kein Flachdach, kein viertes Geschoss, rotes Klinker, Glasfront im EG mit schwarzen Stahlstützen,
Holzterrasse, Loggien im 1. OG, vier Dachgauben für zwei Penthouses, Stellplätze und Pflaster rechts, norddeutsche Kleinstadt (Werlte, Emsland).

---

## 1. Außen, Eckansicht, Abendstimmung

```
Photorealistic architectural visualization of a new three-storey mixed-use corner building in a small
north-German town centre (Werlte, Emsland). Red clinker brick facade (Hamburg red-brown brick, light mortar),
steep gable roof with about 38 degree pitch in dark anthracite roof tiles, ridge parallel to the street,
eaves height 6.5 m, ridge height 12 m. Exactly three levels: ground floor, one upper floor, and a roof floor
with four dormer windows (two penthouses). Ground floor: floor-to-ceiling glass front with slim black steel
columns, warm interior light, a restaurant and bar with a wooden terrace and outdoor tables under a flat
canopy. First floor: six apartments with recessed loggias and black steel railings, white-grey concrete
bands between floors. Red brick paving, young street trees, public car parking on the right.
Blue hour, soft clouds, warm glowing windows. Wide angle, eye level, slightly from the south-east corner,
architectural photography, high detail. No flat roof, no fourth floor, no text.
```

## 2. Außen, Tag, Straßenansicht (Südseite)

```
Photorealistic daytime street view of a three-storey mixed-use building, red clinker brick, gable roof
38 degrees, dark roof tiles, four small dormers, six apartments with loggias on the first floor, glass
ground floor with black steel columns and a wooden terrace with café tables. Town hall square in Werlte
(Emsland) with red paving, trees and parking spaces, partly cloudy sky, soft natural light.
Elevation-like frontal view, 35 mm lens, architectural photography. No flat roof, no extra storey, no text.
```

## 3. Innen, Bar und Restaurant

```
Photorealistic interior of a stylish restaurant and bar in a new building, evening mood. Dark green painted
walls with wainscoting, arched mirrors, red brick niche with bottle shelf, brass pendant lamps with warm
light, cove lighting along the ceiling, curved velvet booth seating in cognac brown with burgundy cushions,
solid oak tables with ribbed glass candle lanterns, pampas grass wall decoration, black steel and glass
partition with grid pattern, floor-to-ceiling windows with a view of a town square at blue hour, guests
softly blurred. About 120 square metres dining room, 65 seats, bar counter in oak with black stools at the
back. Use image 1 as style reference. Wide-angle interior photography, warm and intimate, high detail, no text.
```

## 4. Innen, Theke und Küchenpass

```
Photorealistic close-up interior of an oak bar counter with black bar stools in front of a dark green wall,
brick niche with bottles and brass shelf edges, three brass pendant lamps, arched mirror, warm candle light,
restaurant guests blurred in the background, glass partition with black steel frame. Evening mood, shallow
depth of field, high detail, no text, no logos.
```

## 5. Dachterrasse der Penthouses (optional)

```
Photorealistic view of a penthouse roof terrace carved into a steep anthracite gable roof, recessed dachloggia
with black steel railing, glass sliding doors, wooden decking, potted plants, view over the red-brown tiled roofs
of a small north-German town and the church tower, golden hour. No flat roof, no text.
```

---

## Hinweise
- Die Zahlen stehen als Faktoren im Prompt, KI-Bilder sind keine Planung: Sie halten Maße nur ungefähr ein.
- Wenn das Dach trotzdem flach wird: Skizze `skizze_aussen_ecke.png` als erstes Bild setzen und "keep exactly the roof shape of image 1" ergänzen.
- Fertige Bilder bitte in `praesentation/bilder/` speichern, dann baue ich sie in beide Präsentationen ein.
