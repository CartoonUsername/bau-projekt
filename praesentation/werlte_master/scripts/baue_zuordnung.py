"""Ordnet die 19 Abweichungen des unabhängigen Blatt-14-Abgleichs (Modell v3, 71 Prüfpunkte, 06_pruefpunkte_blatt14_modell_v3.csv) den Punkten der Plan-Ist-Prüfliste (33 Punkte) zu und zeigt den Stand im Modell v4."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
HF = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "visualisierungen", "higgsfield"))
old = list(csv.DictReader(open(os.path.join(HF, "06_pruefpunkte_blatt14_modell_v3.csv"), encoding="utf-8"), delimiter=";"))
def pid(r):
    b = r["bauteil"]
    for k, v in (("Betonbänd", "S9"), ("Brüstung Dachterrasse", "S7"), ("Kern-EG", "S1"), ("Kern-OG1", "S2"), ("Kern-Staffel", "S3"), ("Ost-OG1", "S5"), ("Ost-Staffel", "S6"), ("EG-hinten", "P11"), ("Staffel-hinten", "P10"), ("Abluft", "P14")):
        if k in b: return v
    if b == "Plan-Element ohne Modell" and r["ansicht"] == "Rückseite": return "P10"
    return "?"
NEU = {"S9": "bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen, nicht planbestätigt)", "P11": "behoben (Korrektur 3: dritte Tür entfernt)", "P10": "behoben (Korrektur 2: z 6,90–9,00 wie Blatt 14); die 3 'Plan-Elemente ohne Modell' sind dieselben Fenster in der Plan-Sicht",
       "S1": "behoben durch Herausnahme aus der plangetreuen Fassung; nur noch als Gestaltungsvorschlag (offene Entscheidung)", "S2": "wie S1", "S3": "wie S1", "S5": "wie S1", "S6": "wie S1", "S7": "bleibt, als konzeptionelle Gestaltung gekennzeichnet (offen)", "P14": "behoben (Korrektur 5: Stutzen entfernt; Dachaustritt offene Planungsentscheidung C-22)"}
dev = [r for r in old if r["status"] != "bestätigt"]
rows = [(i + 1, r["ansicht"], r["bauteil"], r["hinweis"], pid(r), NEU.get(pid(r), "?")) for i, r in enumerate(dev)]
with open(os.path.join(HF, "06_zuordnung_19_abweichungen.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["Nr", "Ansicht", "Prüfpunkt Blatt-14-Abgleich (Modell v3)", "Befund", "Punkt der Prüfliste", "Stand Modell v4"]); w.writerows(rows)
from collections import Counter
c = Counter(r[4] for r in rows)
md = ["# 06 Zusammenhang der beiden Prüfungen und Zuordnung der 19 Abweichungen", "",
      "**Zwei Prüfungen mit unterschiedlicher Zähleinheit:**", "",
      "| Prüfung | Zähleinheit | Ergebnis |", "|---|---|---|",
      "| Blatt-14-Abgleich (`scripts/pruefe_modell_gegen_blatt14.py`) | ein Prüfpunkt = ein Bauteil in einer Ansicht (zurückgerechnetes SVG-Rechteck gegen Modellelement, Toleranz 3 cm); dasselbe Bauteil zählt in jeder Ansicht, in der es vorkommt, und eine Abweichung kann mehrere Zeilen erzeugen | Modell v3: 71 Prüfpunkte, 52 bestätigt, 19 Abweichungen |",
      "| Plan-Ist-Prüfliste (`06_plan_ist_pruefliste.*`) | ein Punkt = ein Bauteil bzw. eine Planfrage mit Bezug auf Bildseiten, auch solche ohne Rechteck in der Ansicht (Tragwerk, Orientierung, Belag, Pfostenraster, Türbreiten) | 33 Punkte: 15 bestätigt, 2 Abweichung, 16 ungeklärt |", "",
      "**Warum die Zahlen nicht übereinstimmen:** (1) Die Prüfliste zählt Bauteile, nicht Zeilen: z. B. ergeben die drei Rück-Staffelfenster sechs Zeilen im Abgleich (drei Modellelemente ohne Plan-Gegenstück und dieselben drei Plan-Rechtecke ohne Modell-Gegenstück) und einen Punkt (P10). (2) Die Prüfliste klassifiziert nach Plangrundlage: 'Abweichung' nur dort, wo der Plan eindeutig etwas anderes sagt (P6, P10); wo die Pläne nichts festlegen, steht 'ungeklärt', während der Abgleich jedes Element, das in Blatt 14 nicht gezeichnet ist, als 'Abweichung zu Blatt 14' zählt. (3) Der Abgleich sieht nur gezeichnete Rechtecke: Pfostenraster (P6), Belag (P13), Orientierung (P16), Türbreiten (P7), Tragwerk (T1–T5) und Innenraum (G1, G2) fehlen deshalb im Abgleich und wurden ab jetzt als eigene Zeilen ergänzt (Modell v4, siehe `06_pruefpunkte_blatt14.csv`).", "",
      "## Die 19 Abweichungen (Modell v3) und ihre Zuordnung", "", "| Nr | Ansicht | Prüfpunkt | Befund | Prüflistenpunkt | Stand Modell v4 |", "|---|---|---|---|---|---|"]
for r in rows: md.append("| " + " | ".join(str(x) for x in r) + " |")
md += ["", "Summe je Prüflistenpunkt: " + ", ".join(f"{k}: {v}" for k, v in sorted(c.items())) + f" = {sum(c.values())}.", "",
       "Alle 19 sind einem Punkt der Prüfliste zugeordnet (keine Zeile mit '?'): " + ("ja" if "?" not in c else "NEIN"), "",
       "## Prüflistenpunkte ohne Zeile in den 19 Abweichungen", "",
       "| Punkt | Warum nicht im Abgleich sichtbar |", "|---|---|",
       "| P6 Pfostenraster | Blatt 14 zeichnet die Glasfläche als ein Rechteck; das Modell passte darauf (Rechteck x 4–32) und der Abgleich sah die 1,40-m-Stege nicht. Jetzt eigene Zeile. |",
       "| P13 Belag Dachterrasse | Blatt 14 zeichnet keinen Belag. Jetzt eigene Zeile. |",
       "| P7 Türbreiten, P16 Orientierung, P15 Stellplätze, T1–T5 Tragwerk, G1/G2 Innenraum | keine Rechtecke in den Ansichten von Blatt 14; Quellen sind andere Blätter (siehe Prüfliste). |",
       "| P8 Vordach | im Abgleich 'bestätigt' (Blatt 14 zeichnet es); Prüflistenpunkt betrifft nur die offene Konstruktion. |"]
open(os.path.join(HF, "06_zuordnung_pruefungen.md"), "w", encoding="utf-8").write("\n".join(md) + "\n"); print(len(rows), dict(c))
