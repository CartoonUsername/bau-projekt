# 02 Higgsfield-Prompts (Veredelung der Blender-Renderings)

**Workflow:** Architektur und Kamera kommen ausschließlich aus dem Blender-Modell (`scripts/modell_b3.py`, `scripts/blender_modell_v3.py`). Higgsfield (Modell nano_banana_pro, vom Server als nano_banana_2 gemeldet) bekommt das Blender-Rendering als einzige Bildreferenz und darf nur Materialtextur, Spiegelungen und Lichtstimmung veredeln. Freie Generierung der Architektur findet nicht mehr statt. Die ersten Prompts aus der Auftragsbeschreibung (freie Gebäudebeschreibung) wurden bewusst nicht verwendet, weil frühere Läufe die Geometrie verändert haben (siehe 01_fehlerliste.md).

Seitenverhältnis: 16:9. Negativ-/Ausschlusskriterien stehen im Prompt (keine Personen, Fahrzeuge, Bäume, Texte, Logos, keine zusätzlichen Bauteile). Zeitlicher Verlauf: Runde 1 (Prompt ohne Farbsperre) lieferte abweichende Holzfarben (blond/grau) und wurde für 01–06 verworfen (`renderings/veredelt/runde1/`); Runde 2 mit Farbsperre ist final.

Prüfung je Bild: Kantenvergleich (`scripts/geometrietreue.py`) und Sichtprüfung, Ergebnis in `04_qualitaetskontrolle.csv`.

## 01_hauptansicht_tag
- Higgsfield-Job: da2b9839 (Runde 1, verworfen: Farbdrift) / a025bb77-0cb6-4329-a982-89de10f015a3 (final)
- Referenzbild (hochgeladen): Blender-Rendering, Media-ID 1fb40fe7-3e3c-476e-8db5-763f7a54f7de
- Prompt (auch in `prompts/01_hauptansicht_tag.txt`):

> Make this 3D render photorealistic, changing NOTHING about geometry and NOTHING about the colour palette. Same camera, same edges, same windows, doors, mullions, balconies, canopy, bands and chimney at identical pixel positions. COLOURS ARE LOCKED to the input: the top-floor cladding stays the same warm medium reddish-brown vertical timber (do not lighten to blond, do not grey it), the lower walls stay the same dark red-brown clinker brick, bands stay light grey concrete, the ground stays the same light warm-grey paving. The balcony railings stay frosted pale grey-green glass, not concrete. Add only fine material texture, natural glass reflections and soft natural daylight shadows. Empty neutral surroundings, no people, cars, trees, text or logos.

## 02_hauptansicht_abend
- Higgsfield-Job: c2cdd18d-0ad1-4c3f-beea-c42a6f01c7f7
- Referenzbild (hochgeladen): Blender-Rendering, Media-ID d7301a04-a573-4287-aa52-ae0743ad9ed3
- Prompt (auch in `prompts/02_hauptansicht_abend.txt`):

> Make this 3D dusk render photorealistic as a blue-hour photograph, changing NOTHING about geometry. Same camera, same edges, windows, doors, mullions, balconies, canopy, bands and chimney at identical pixel positions; add nothing (no shutters, lamps or light strips). COLOURS ARE LOCKED to the input: top-floor cladding warm medium reddish-brown vertical timber, lower walls dark red-brown clinker brick, light grey concrete bands, balcony railings frosted pale grey-green glass (not concrete). The glowing ground-floor glazing becomes a warm restaurant interior glow with faint tables; the few lit apartment windows show a subtle warm light, the other windows stay dark. Natural blue evening sky, empty paved square, no people, cars, text or logos.

## 03_rueckansicht
- Higgsfield-Job: 39fc8740-1f1c-404e-86ee-5a6e81539fcd
- Referenzbild (hochgeladen): Blender-Rendering, Media-ID 56c3cf83-90db-43f2-8572-a7984784380b
- Prompt (auch in `prompts/03_rueckansicht.txt`):

> Make this 3D render of the rear facade photorealistic, changing NOTHING about geometry and NOTHING about the colour palette. Same camera, same edges, windows, doors, bands, the 3 m cantilever over the parking bays, roof terrace with frosted-glass parapet and setback top floor at identical pixel positions; NO columns or posts under the cantilever, nothing added. COLOURS ARE LOCKED to the input: top-floor cladding warm medium reddish-brown vertical timber (same tone on every part, not grey, not blond), walls dark red-brown clinker brick, light grey concrete bands, parapet frosted pale grey-green glass, asphalt with white bay lines, light warm-grey paving. Fine material texture, natural reflections, soft daylight. Empty neutral surroundings, no cars, people, text.

## 04_westseite
- Higgsfield-Job: f78153a4-5537-4f14-a75a-3dbf2c170045
- Referenzbild (hochgeladen): Blender-Rendering, Media-ID 3c1ee498-38d5-4b4c-8dc8-f4f9c061845b
- Prompt (auch in `prompts/04_westseite.txt`):

> Make this 3D render of the west (core) side photorealistic, changing NOTHING about geometry and NOTHING about the colour palette. Same camera, same edges, the three narrow windows, bands, parapet and canopy at identical pixel positions; nothing added. COLOURS ARE LOCKED to the input: top-floor cladding warm medium reddish-brown vertical timber (not grey, not blond), walls dark red-brown clinker brick, light grey concrete bands, light warm-grey paving. Fine material texture, soft natural daylight. Empty neutral surroundings, no people, cars, text.

## 05_ostseite
- Higgsfield-Job: b0915447-9160-4df1-a778-a681661c786e
- Referenzbild (hochgeladen): Blender-Rendering, Media-ID 84af253b-81c3-47ac-aadf-c49799b711d1
- Prompt (auch in `prompts/05_ostseite.txt`):

> Make this 3D render of the east side photorealistic, changing NOTHING about geometry and NOTHING about the colour palette. Same camera, same edges, the two windows, the ground-floor door, the roof chimney, the setback and the frosted-glass parapet at identical pixel positions; nothing added. COLOURS ARE LOCKED to the input: top-floor cladding warm medium reddish-brown vertical timber (not grey, not blond), walls dark red-brown clinker brick, light grey concrete bands, light warm-grey paving. Fine material texture, soft natural daylight. Empty neutral surroundings, no people, cars, text.

## 06_luftbild
- Higgsfield-Job: 684a069e-f648-4401-9656-e2c903cff729
- Referenzbild (hochgeladen): Blender-Rendering, Media-ID a73c1339-6eb6-4d37-9522-814bec876a0d
- Prompt (auch in `prompts/06_luftbild.txt`):

> Make this 3D aerial render photorealistic, changing NOTHING about geometry and NOTHING about the colour palette. Same camera, same roof outline, roof terrace with frosted-glass parapet, setback, windows, chimney, 11 parking bays with white markings on the asphalt patch at identical pixel positions; nothing added. COLOURS ARE LOCKED to the input: top-floor cladding warm medium reddish-brown vertical timber (not grey, not blond), walls dark red-brown clinker brick, light grey concrete bands and roof, light warm-grey paving ground. Fine material texture, soft natural daylight. Strictly neutral plain ground, no neighbouring buildings, trees, cars, roads, people, text.

## 07_gastro_innenraum
- Higgsfield-Job: 03f3b426-68a9-498e-930f-a1e2d7014588
- Referenzbild (hochgeladen): Blender-Rendering, Media-ID af28b47c-74f7-47bb-867b-9924d122c75b
- Prompt (auch in `prompts/07_gastro_innenraum.txt`):

> Retouch this 3D interior render of a restaurant hall into a photorealistic interior photograph WITHOUT changing the layout. Keep the exact camera, room proportions, the floor-to-ceiling glazing with its slim dark steel mullions on the right, the bar at the far end, the positions and counts of tables, chairs, bar stools and pendant lamps, ceiling and walls at exactly the same positions; do not add or remove furniture, columns, pillars, partitions, benches or windows. Materials: olive green wall panelling with fine dark joints, cognac velvet chairs, bordeaux bar stools, oak tables and bar top, dark fluted bar front with a brass foot rail and brass shelf details, cream textiles, warm pendant lamps with soft warm indirect light, polished micro-cement concrete floor. Outside the glazing only a plain neutral paved square and soft daylight, no buildings. Realistic furniture proportions, elegant but understated. No text, no logos, no menus, no people.

## 08 Wohnraum/Terrasse
Nicht erstellt (optional). Eine Terrassen-Modellansicht (`renderings/tag/tag_08_terrasse.png`) wurde gerendert und zur Veredelung gegeben (Runde 1, Job 13b8a17f); das Ergebnis zeigte das Holzdeck durch die Fenster des Staffelgeschosses und wurde verworfen.
