# 03 Referenzregister

## Verbindlich (aktuelle Serie)
| Referenz | Datei | Inhalt |
|---|---|---|
| Modell (Quelle der Wahrheit) | `../../scripts/modell_b3.py`, `modelle/baufeld3_B3_v3.blend` | B3/K, Planprüfung 83/83 |
| Ortho-Ansichten (Front, Rück, West, Ost) | `renderings/00_geometrie_ortho/ortho_*.png` | Maßstab 1:250 wie Blatt 25 |
| Überlagerung Plan/Modell | `renderings/00_geometrie_ortho/ueberlagerung_plan_modell_*.png` | Geometrienachweis |
| Neutrale Perspektiven | `renderings/00_geometrie_neutral/einfach_*.png` | Farbcode wie Blatt 25 |
| Blender-Renderings (Veredelungsbasis) | `renderings/tag/`, `renderings/nacht/`, `renderings/07_gastro_innenraum/` | texturiert, Kamera-JSON daneben |
| Veredelte Endbilder | `renderings/0x_*/final_*.png` | je Motiv, daneben `blender_*.png` |
| Materialtexturen | `modelle/texturen/` | prozedural erzeugt (Klinker, Holz, Beton, Pflaster, Asphalt, Mikrozement, Eiche) |
| Innenraumreferenz | Blatt 21 `varianten_v3/21_Gastronomie_Moeblierung`, `scripts/blender_interior.py` | Gastraum 28 x 10 m, Möblierung ‚normal‘ |

## Nicht verbindlich (veraltet, bleiben zur Nachvollziehbarkeit erhalten)
| Datei | Grund |
|---|---|
| `Bildauswahl_Volksbank_Baufeld3.pdf`, `Bilder_Baufeld3_Zwischenstand.pdf` | Higgsfield-Bilder mit freier Interpretation (siehe `01_fehlerliste.md`, Abschnitt D) |
| `01_Hauptansicht_Tag_Platzseite.png` … `07_Gastro_Innenraum.png` (im Hauptordner) | dieselben veralteten Bilder |
| `roh/` | erste Higgsfield-Läufe, verworfen |
| `referenzen/ref_*.png`, `referenzen/clay_*.png`, `referenzen/mat_*.png` (und `../referenzen/ref_*.png`) | frühere Tonmodelle mit den Fehlern M1–M3 bzw. Darstellungsfehlern |
| `modelle/baufeld3_B3.blend/.glb` | erstes Blender-Modell (Fehler M1–M3) |
| `PROMPTS_UND_REIHENFOLGE.md` | Promptplan des ersten Durchlaufs |
| `renderings/veredelt/runde1/`, `renderings/veredelt_test/` | verworfene Veredelungsläufe (Farbdrift, Terrasse unplausibel) |
