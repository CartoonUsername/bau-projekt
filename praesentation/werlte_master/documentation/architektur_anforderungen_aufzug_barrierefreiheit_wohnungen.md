# Architektonische Anforderungen: Aufzug, Barrierefreiheit, Nutzbarkeit der ca. 39-m²-Wohnungen
Arbeitsstand OG-2 (VORLÄUFIG, 22.10.2026). Keine Förderthemen, keine Designänderung, keine Renderings. **Es wird keine baurechtliche Zulässigkeit behauptet.** Alle Aussagen zum Recht stammen aus Suchtreffern, nicht aus dem amtlichen Volltext (NI-VORIS und NBank-Seiten konnten von der Umgebung nicht abgerufen werden).

## 1. Aufzug und barrierefreie Erschließung
### 1.1 Quellenlage (Status je Aussage)
| Aussage | Quelle | Status |
|---|---|---|
| Wird ein Gebäude mit mehr als vier Wohnungen errichtet, müssen die Wohnungen barrierefrei sein (§ 49 Abs. 1 NBauO); Neubau mit 13 Wohnungen fällt in diesen Bereich | [§ 49 NBauO, VORIS](https://voris.wolterskluwer-online.de/browse/document/c84955d0-4e6b-36bc-a242-7e40f3107d02); [Haufe](https://www.haufe.de/id/norm/bauordnung-niedersachsen-49-barrierefreie-zugaenglichkeit-und-benutzbarkeit-baulicher-anlagen-HI3049642_p49.html); [nullbarriere](https://nullbarriere.de/bauordnung-niedersachsen.htm) | Suchtreffer, Wortlaut nicht geprüft |
| Aufzugspflicht nach § 38 Abs. 2 NBauO erst bei Aufenthaltsräumen mit Fußboden mehr als 12,25 m über der Eingangsebene; Staffel-FFL liegt bei 6,5 m | [MW Niedersachsen FAQ NBauO](https://www.mw.niedersachsen.de/download/209290), [Aufzugspflicht 2026](https://www.personenaufzuege.com/ratgeber/aufzugspflicht/) | Suchtreffer; daraus folgt voraussichtlich KEINE Pflicht zur Herstellung, aber ungeklärt |
| Stufenlose Erreichbarkeit höherer Geschosse muss im Entwurf nachweisbar dargestellt sein, auch wo kein Aufzug gebaut werden muss | [bfb Aufzüge Niedersachsen](https://www.bfb-barrierefrei-bauen.de/aufzuege-niedersachsen) | Suchtreffer, ab welchem Geschoss ist unklar (Formulierung „ab dem zweiten oberirdischen Geschoss") |
| Jede achte Wohnung rollstuhlgerecht; Rundung bei 13 Wohnungen (1,6) nicht geklärt | [nullbarriere](https://nullbarriere.de/bauordnung-niedersachsen.htm), [TÜV SÜD Barrierefreiheit im Wohnungsbau](https://www.tuvsud.com/de-de/-/media/de/industry-service/pdf/netinform/bautechnik-2024/barrierefreiheit-im-wohnungsbau.pdf) | Suchtreffer |
| Novelle: Kabinettsentwurf sieht u. a. Streichung eines Satzes in § 49 Abs. 1 (Aufzug zu barrierefreien Wohnungen) vor; Stand der Verabschiedung unbekannt | [Staatskanzlei](https://www.stk.niedersachsen.de/startseite/presseinformationen/kabinett-gibt-entwurf-der-novelle-der-niedersachsischen-bauordnung-zur-verbandsbeteiligung-frei-bauen-soll-leichter-schneller-und-gunstiger-werden-227757.html), [Synopse](https://www.mw.niedersachsen.de/download/202157/Synopse_NBauO_GE-NBauO_Auszug.pdf) | UNBESTÄTIGT, aktueller Wortlaut prüfen |
| Technische Ausführung: DIN 18040-2 (Wohnungen), Arbeitshilfe des Landes | [NLBL Arbeitshilfe](https://www.nlbl.niedersachsen.de/download/156579/Arbeitshilfe_fuer_das_barrierefreie_Bauen.pdf), [bfb Eingeführte Technische Baubestimmungen](https://www.bfb-barrierefrei-bauen.de/niedersachsen) | Einführung als technische Baubestimmung zu prüfen |
| Gastro und Büros (öffentlich zugänglich) unterliegen eigenen Anforderungen des § 49 | nicht abgerufen | OFFEN, nicht bewertet |

### 1.2 Entscheidung für den Entwurf
Der Aufzug bleibt bis zur fachlichen Klärung im Entwurf (Auftraggeber). Rechtliche Notwendigkeit ist NICHT belegt; er dient der stufenlosen Erreichbarkeit aller Wohnungen, Büros und des Staffelgeschosses.

### 1.3 Geometrische Prüfung am Arbeitsstand (v003, siehe `validation/consistency_OG2.md`)
- **Mangel im Arbeitsstand v002 (selbst verursacht, nun korrigiert, C-24):** Der Aufzug lag hinter dem Treppenraum und war vom Mittelgang nicht direkt erreichbar. Kern in v003 neu geordnet: Lobby (y 0–3), Treppenraum (y 3–8), Aufzugsvorraum (y 8–10, stößt an den Mittelgang), Aufzug x 0,8–3,0 / y 10–12,6, dahinter Technik und Abstellraum. Alle ASSUMED.
- Aufzug liegt auf GF, 1. OG und Staffel übereinander; Schacht 2,2 × 2,6 m ist großzügig. Fahrkorbgröße und -typ (z. B. 1,1 × 1,4 m) sind fachlich offen.
- **C-25:** Schacht ab x 0,8, damit die Westwand mit der Staffel-Rückversatzlinie fluchtet. Überfahrt über Attika (9,9 m) kann einen sichtbaren Aufbau erzeugen, das wäre eine Designfrage und wird nicht still gelöst.
- Mittelgang 2,0 m breit; Vorraum 4,0 × 2,0 m. Eingang West x 1–2,5 m (1,5 m breit); Gelände-/Platzhöhen unbekannt, daher stufenloser Zugang nicht nachgewiesen.
- Balkone: Schwellenfreiheit der Balkontüren bei Betonbalkon nicht geklärt.
- **Rollstuhlgerechte Wohnung (R):** mindestens eine, evtl. zwei; die 39-m²-Wohnungen kommen nach heutiger Einschätzung dafür kaum in Frage. Kandidaten wären WE-L1-N1 (ca. 52 m²) oder eine Staffel-Nordwohnung (ca. 57 m², Aufzug erreichbar). Nicht nachgewiesen, Fachplaner prüft Bewegungsflächen.
- Offene Punkte: Aufzug im Brandfall (Treppenraum und Aufzug getrennt?), Feuerwehraufzug nicht angenommen, Gastro-WC barrierefrei.

## 2. Nutzbarkeit der Wohnungen ca. 39 m² netto (WE-L1-S1…S5)
Datei: `plans/unit_WE-L1-S_nutzbarkeit.png`, Skript `scripts/unit_study.py`. Innenmaß ca. 5,35 × 7,35 m (ASSUMED Wandstärken). Probe mit Bett 1,4 × 2,0, Sofa, Tisch, Küchenzeile 2,4 m, Schrank, Dusche, WC, Waschtisch, Waschmaschine und freien Bewegungsflächen: **keine Überlappungen, keine blockierten Bewegungsflächen**.

**Befund (kein Rechtsurteil):**
- Sinnvoll und eigenständig nutzbar als **Studio-Wohnung (Einzimmer mit Schlafbereich, Küche, Bad)** für 1 Person, mit Einschränkung 2 Personen. Kein separates Schlafzimmer möglich: ein zweiter Raum würde zwei ca. 2,6 m breite Räume an der Fassade ergeben.
- Wohn-/Schlafraum 23,8 m², Flur/Küche 8,7 m², Bad 6,8 m² (großzügig, kann um ca. 1 m² zugunsten Abstellnische verkleinert werden).
- Einseitige Belichtung: nur eine Fassadenachse zum Platz (Balkontür); Küche und Bad innenliegend, mechanische Lüftung nötig, keine Querlüftung.
- Lage: alle Aufenthaltsbereiche und Balkone liegen über der Gastro-Terrasse (60 Plätze) und der Bar. Lärm am Schlafplatz bis in die Nacht ist ein Nutzungsrisiko (Schallschutz, Betriebszeiten, Himmelsrichtung C-13), nicht geprüft.
- Kein Abstellraum in der Wohnung, nur Kern-Abstellflächen (ABSTELL-GF/L1, 21,6 m² je Ebene, Zweck offen).
- Wohnungstür liegt am Mittelgang; Brüstungshöhe, Fensterflächen und Tageslichtnachweis nicht geprüft.
- Das Ergebnis begründet keine Erhöhung der Wohnungszahl; die Zahl bleibt eine Folge des Entwurfs (5 Balkonachsen).
- Größere Typen: WE-L1-N1 (52 m²) gut als 2-Zimmer, Staffel hinten (57 m²) als 2-Zimmer mit Möglichkeit R; Staffel vorn (ca. 43 m²) wie Studio. Nicht einzeln durchgeplant.

## 3. Offene Anforderungen, die vor Freigabe geklärt werden müssen
1. Aktueller Wortlaut § 49 und § 38 NBauO (VORIS) einschließlich Novelle; Zahl der R-Wohnungen (Rundung).
2. Fahrkorbgröße und Aufzugstyp; Überfahrt/Aufbau (C-25).
3. Stufenloser Zugang (Gelände/Platzhöhen), Balkonschwellen.
4. Brandschutz Aufzug/Treppenraum; Rettungsweg im Mittelgang (C-15).
5. Mindestanforderungen an Wohnungen (Fensterflächen, Belüftung innenliegender Räume, lichte Höhen) nach NBauO/DVO und DIN 18040-2 prüfen und gegenzeichnen lassen.
6. Schallschutz und Betriebskonzept Gastro gegenüber den Wohnungen.
