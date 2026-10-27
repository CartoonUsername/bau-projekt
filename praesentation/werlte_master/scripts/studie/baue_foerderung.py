"""Förder-Orientierung je Variante (getrennt von der geometrischen Bewertung). Keine Zusage, keine Berechnung eines Anspruchs."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pdflib import *
import varianten as VA
OUT = os.path.join(VA.ROOT, "studie_gebaeudeformen"); D = VA.alle(); KEYS = list("ABCD")
fm = lambda x, n=0: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def units(k, m):
    x = D[k]["mix"][m]; return x["og1"]["vorn"] + x["og1"]["hinten"] + x["st"]["vorn"] + x["st"]["hinten"]
def klassen(u): return (sum(1 for a in u if a <= 50), sum(1 for a in u if 50 < a <= 60), sum(1 for a in u if 60 < a <= 75), sum(1 for a in u if 75 < a <= 85), sum(1 for a in u if a > 85))
TAG = "FÖRDERUNG · KEINE ZUSAGE"
QUELLEN = [
 "NBank, Allgemeine Mietwohnraumförderung / Produktinformationen Neubau Mietwohnungen (Stand 01.04.2026 bzw. Produktinformation 10.07.2026; neue Richtlinie ab 01.07.2026): nbank.de",
 "KfW 297/298 Klimafreundlicher Neubau Wohngebäude (Stand 30.07.2026), KfW 296 Merkblatt (06/2026), Technische FAQ zu Mischnutzung (Wohngebäude, wenn > 50 % Wohnnutzung): kfw.de",
 "Pressemeldung Land Niedersachsen/NBank zur Neuaufstellung der sozialen Wohnraumförderung (01.07.2026)"]
def baue():
    pages = []; im, d = page(); header(d, "Förderung im Variantenvergleich – Orientierung", "Getrennt von der geometrischen Bewertung · Stand der Recherche Oktober 2026 · keine Zusage, kein Anspruch", TAG); footer(d, 1)
    y = text_block(d, 120, 280, 3260, "Wichtig: Eine größere Wohnfläche garantiert keine höhere Förderung. Maßgeblich sind Förderprogramm, Mietstufe, Einkommensgruppe, angemessene Wohnungsgrößen, Energiestandard, Mietbindung und Antragszeitpunkt. Alle Tabellen zeigen nur, welche Obergrenzen je Variante überhaupt relevant werden könnten.", 34, INK, "SemiBold")
    rows = [["Baustein", "Regel laut Quelle (vor Antrag erneut prüfen)", "Quelle / Stand", "Status"],
     ["NBank Mietwohnraumförderung Neubau", "mind. 3 WE; Effizienzhaus 40; Maßnahme darf noch nicht begonnen sein; Bindung 35 Jahre ab Bezugsfertigkeit; Zuschuss bis 40 %, Gesamtförderung bis 80 % bei niedrigem Einkommen", "NBank 07/2026, Pressemeldung", "Rahmen bekannt, Zahlen für Werlte offen"],
     ["Angemessene Wohnungsgrößen", "1 Pers. 50 m², 2 Pers. 60, 3 Pers. 75, 4 Pers. 85, je weitere +10 m²; Überschreitung im Einzelfall begrenzt (Quellen nennen 2 % bzw. 10 % – klären); Wohnung ≥ 30 m²", "NBank Produktinformation", "zu bestätigen"],
     ["NBank-Darlehen Kostengrenze", "75 % von max. 5.330 €/m² (Mietenstufe I–III) bzw. 5.550 €/m² (IV–VII) Wohnfläche; gebundene Miete, Einkommensgruppen", "NBank Stand 01.04.2026", "Mietenstufe Werlte unbestätigt"],
     ["Barrierefreiheit", "Zuschuss 5.000 € je barrierefreier/rollstuhlgerechter WE (laut NBank-Unterlage)", "NBank", "Voraussetzung je WE prüfen"],
     ["KfW 297/298 (296 mit QNG)", "Kredit bis 100.000 €/WE (298) bzw. 150.000 €/WE mit QNG (296); Effizienzhaus 40; keine Öl-/Gasheizung; Baugenehmigung zum Antrag", "KfW Merkblätter 06–07/2026", "Zinssatz/Tilgungszuschuss tagesaktuell"],
     ["Mischnutzung (Gewerbe im EG)", "Gebäude gilt als Wohngebäude, wenn > 50 % der Fläche Wohnen; Nichtwohnteil getrennt bilanzieren (> 10 % der Nutzfläche)", "KfW Technische FAQ", "Wohnanteil je Variante unten"]]
    table(d, 120, y + 50, [520, 1560, 700, 480], rows, 30)
    pages.append(im)
    im, d = page(); header(d, "Variantenvergleich unter Förderaspekten", "Standardmix; Obergrenzen als Orientierung – kein Förderbetrag berechnet", TAG); footer(d, 2)
    h = ["Kennzahl"] + [D[k]["name"].split(" (")[0] for k in KEYS]; cw = [1000] + [567] * 4
    rows = [h, ["Wohnungen (Standardmix)"] + [str(D[k]["we"]) for k in KEYS], ["Wohnfläche netto (m²)"] + [fm(D[k]["wfl"]) for k in KEYS], ["Wohnanteil an der Geschossfläche (BGF ohne EG)"] + [f"{(D[k]['flaeche']['og1']+D[k]['flaeche']['st'])/D[k]['bgf']*100:.0f} % (Wohnen > 50 % je Variante, EG-Gewerbe beachten)" for k in KEYS]]
    for lab, m in (("Standardmix", "standard"), ("kleinerer Mix", "klein"), ("größerer Mix", "gross")):
        rows.append([f"Größenklassen {lab}: ≤50 / 50–60 / 60–75 / 75–85 / >85 m²"] + [" / ".join(map(str, klassen(units(k, m)))) for k in KEYS])
    rows.append(["Obergrenze NBank-Darlehen: 75 % × 5.330 € × Wohnfläche (T€)"] + [fm(0.75 * 5330 * D[k]["wfl"] / 1000) for k in KEYS])
    rows.append(["KfW 298: WE × 100.000 € (T€) / KfW 296: WE × 150.000 € (T€)"] + [f"{D[k]['we']*100:,} / {D[k]['we']*150:,}".replace(",", ".") for k in KEYS])
    rows.append(["Barrierefreiheits-Zuschuss bis (€), falls alle WE erfüllen"] + [fm(5000 * D[k]["we"]) for k in KEYS])
    rows.append(["Stellplätze erforderlich (Gastro+Büro; Wohnen keine Pflicht) vs. 11 nachweisbar"] + [f"{fm(D[k]['stp']['erf_lo'],1)}–{fm(D[k]['stp']['erf_hi'],1)} vs. 11" for k in KEYS])
    table(d, 120, 290, [1000,567,567,567,567], rows, 32)
    text_block(d, 120, 1900, 3260, "Lesehilfe: Die Obergrenzen wachsen mit Wohnfläche bzw. Wohnungszahl – ob sie ausgeschöpft werden, hängt von den tatsächlich förderfähigen Kosten (Kostengrenze je m²), der Mietbindung (gebundene Miete statt Marktmiete) und der Einkommensgruppe der Mieter ab. Größere Wohnungen können die Einpersonen-/Zweipersonen-Grenzen (50/60 m²) überschreiten und damit nicht angemessen sein; der kleinere Mix passt besser zu 50/60 m², bringt aber höhere Kosten je m² (Küchen/Bäder) und mehr Stellplatzbedarf. Variante C mit hoher Ausnutzung hat die größte Wohnfläche, aber die größten baurechtlichen Risiken (siehe Vergleichs-PDF).", 30, GREY)
    pages.append(im)
    im, d = page(); header(d, "Offene Voraussetzungen und Quellen", "vor jedem Antrag bei Wohnraumförderstelle Landkreis Emsland / NBank und KfW bestätigen", TAG); footer(d, 3)
    t = ("Offen: Mietenstufe Werlte; Einkommensgrenzen und gebundene Miete (€/m²) für 2026; ob die Förderung für Gebäude mit Gewerbeanteil im EG (Gastro/Büro) gilt und wie der Wohnanteil bewertet wird; Zuschusshöhe je WE vs. je m²; Eigenleistung/Eigenmittel (z. B. 25 %); Beginn der Maßnahme (Baubeginn vor Bewilligung schädlich); Baugenehmigung; EH40/QNG-Nachweis; Heizung ohne Öl/Gas; Zinssätze noch zu bestätigen; Barrierefreiheit/Rollstuhlgerechtigkeit (Quote); Kombinierbarkeit NBank + KfW.\n\n"
         "Keine Zusage: Es wurde kein Förderantrag gestellt, keine Förderzusage liegt vor, und kein Betrag in diesem Dokument ist ein Anspruch.\n\nQuellen:\n• " + "\n• ".join(QUELLEN))
    text_block(d, 120, 300, 3260, t, 34); pages.append(im)
    p = f"{OUT}/Foerderung_Variantenvergleich.pdf"; save(pages, p); print(p)
baue()
