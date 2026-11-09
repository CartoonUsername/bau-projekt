# Fördervergleich OG-1 / OG-2 / OG-3 (Entwurf, nichts zugesichert, nichts festgeschrieben)

Rechnung: `scripts/foerder_vergleich.py` → `foerderung/vergleich.json`. Basis: Excel-Werte (Kredit 4.894.879 €, 3,21 % Mischzins, Miete frei 11,18 €/m², Wohnanteil an Kosten 49,2 %, Mehrkosten 15.000 € je WE).

## Quellenlage (Stand 22.10.2026)
| Aussage | Quelle | Status |
|---|---|---|
| Neue Richtlinien Niedersachsen seit 01.07.2026; Zuschuss bis 40 % der förderfähigen Kosten, Gesamtförderquote bis 80 % bei Haushalten mit niedrigem Einkommen | NBank/Ministerium (Pressemeldung, über Websuche) | Pressestand, Obergrenze |
| Neubau-Produkt: mind. KfW-Effizienzhaus 40, mind. 3 WE, Maßnahme darf nicht begonnen sein, Bindung 35 Jahre ab Bezugsfertigkeit | NBank Produktinformation Stand 10.07.2026 (Suchtreffer) | nicht im Volltext geprüft |
| Angemessene Wohnfläche: 1 Pers. 50 m², 2 Pers. 60, 3 Pers. 75, 4 Pers. 85, +10 je weitere; +10 % im Einzelfall; Wohnung soll ≥ 30 m²; rollstuhlgerecht +12 m² (+15 m² mit Freisitz) | NBank Produktinformation 10.07.2026 (Suchtreffer) | Suchtreffer |
| Darlehens-Kostengrenze 5.330 €/m² (Mietstufe I–III) / 5.550 (IV–VII) | NBank Stand 01.04.2026 | vor der Reform, evtl. überholt |
| Mieten 6,30 €/m² (niedrige) / 7,80 €/m² (mittlere Einkommen), Mietstufe I–III | NBank Stand 01.04.2026 | vor der Reform, evtl. überholt |
| „bis 45.000 € je WE" | Drittquelle | ungeprüft, nicht verwendet |
| Mietstufe Werlte, Einkommensgrenzen in €, Zuschusshöhe je WE, Barrierefreiheits-Quote | NICHT gefunden (NBank-Server aus der Umgebung gesperrt, Volltexte nicht abrufbar) | OFFEN – bei Wohnraumförderstelle Landkreis Emsland erfragen |

## Annahmen (alle gekennzeichnet)
A1 alle Wohnungen werden gefördert; A2 Zuschuss 20 % (vorsichtig) bzw. 40 % (Obergrenze) der förderfähigen Wohnkosten, begrenzt auf 5.330 €/m²; A3 Miete 7,80 bzw. 6,30 €/m² statt 11,18; A4 Zuschuss mindert Darlehen, Ersparnis = Zuschuss × 4,21 % (Annuität); A5 10 % Rückstellung auf Mietänderungen; A6 Gewerbe (Gastro, Büros) nicht förderfähig; A7 Kosten Büro-Ausbau bei OG-3 unverändert (konservativ).

## Vergleich
| | Excel-Basis | OG-1 | OG-2 | OG-3 (Büros → Wohnungen) |
|---|---|---|---|---|
| Wohnungen (OG + Staffel) | 12 | 12 (5+7) | 13 (6+7) | 15 (8+7) |
| Wohnfläche netto | 655 m² | 591 m² | 591 m² | 736 m² |
| Wohnungsgrößen | 47,7 / 64,2 | OG 46,7–54,6; Staffel 42,8 / 57,0 | OG 5×39,4 + 52,1; Staffel wie OG-1 | OG 5×39,4 + 3×65,7; Staffel wie OG-1 |
| Förderfähig (Größe) | – | alle 12; 54,6 m² nur für 2 Pers. (>50 m²) | alle 13; 39 m² für 1 Pers. ideal | alle 15; 65,7 m² für 3 Pers. |
| Gesamtkosten | 4.894.879 € | 4.894.879 € | 4.909.879 € | 4.939.879 € |
| Förderfähige Wohnkosten | 2,41 Mio € | 2,41 Mio € | 2,42 Mio € | 2,43 Mio € |
| Zuschuss 20 % / 40 % (ANNAHME) | 482 / 964 Tsd € | 482 / 964 Tsd € | 484 / 967 Tsd € | 487 / 973 Tsd € |
| GbR-Ergebnis/Monat ohne Förderung | −553 € | −1.197 € | −1.250 € | −1.337 € |
| mit 20 % + 7,80 € Miete | −851 € | −1.300 € | −1.348 € | −1.865 € |
| mit 40 % + 7,80 € Miete | +842 € | +393 € | +351 € | −156 € |
| mit 40 % + 6,30 € Miete | −42 € | −405 € | −447 € | −1.150 € |

## Ergebnis
- Die Gesamtförderung (Annahme je m²) unterscheidet sich zwischen OG-1 und OG-2 kaum (±3 Tsd €), weil beide 591 m² haben; nur eine Förderung je Wohnung würde OG-2 (+1 WE) begünstigen, diese ist nicht belegt.
- OG-1 ist wirtschaftlich minimal besser (+49 €/Monat), OG-2 erfüllt das 5-Balkone-Bild und hat die für Förderung gut passenden 39-m²-Einpersonenwohnungen.
- OG-3 (Büros zu Wohnungen) erzeugt zwar die meiste Fläche und 15 WE, ist aber wegen entfallender Büro-Mieten (1.600 €/Monat) und Ankermieter-Konzept schlechter und braucht Freigabe.
- Alle Varianten liegen mit 591 m² unter den 655 m² der Excel; das senkt das Ergebnis um ca. 644 €/Monat unabhängig von Förderung.
- Empfehlung (vorläufig): OG-2 weiterverfolgen, sobald die Förderfähigkeit (Zuschusshöhe je m² oder je WE, Mietstufe, Mietbindung) bei der Wohnraumförderstelle bestätigt ist; keine Festschreibung.
