"""Modelle und Konsistenzprüfung für die Revitalyze-Import-PDFs (Baufeld 3).
Je Variante EIN Modell-Dict; Grundrisse, Ansichten, Schnitt und Lageplan werden ausschließlich daraus gezeichnet (revitalyze_pdfs.py).
Variante A = bisheriger B3-Stand (geometry/variant_B3.json + scripts/modell_b3.py, unverändert gelesen).
Varianten B1–B3 = neue Idee (EG 18 × 30 m = 540 m², Daten aus varianten_f.py F1–F3, nur gelesen).
Koordinaten in m: x West -> Ost, y von der Platzseite (0) zur Rückseite, z ab OK Fertigfußboden EG (±0,00).
Nichts wird erfunden: Unbekanntes steht in 'offen' und wird im PDF als ANNAHME bzw. NOCH OFFEN ausgewiesen."""
import os, sys, math
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER); sys.path.insert(0, os.path.join(HIER, ".."))
import varianten as VA, varianten_f  # noqa: F401  (registriert F1–F3)
import modell_b3 as M3

WAND = 0.30          # ANNAHME Außenwandstärke (nur Darstellung der Doppellinie)
SAEULE_D = 0.40      # aus parken.py/varianten_e.py (Annahme des Entwurfs)
PLOT = [(0, 0), (32, 0), (32, 30), (0, 30)]   # Hypothese H1 – 960 m², Zuschnitt NICHT bestätigt

def poly_area(p): return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2
def rect_poly(r): return [(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])]
def bb(p): return (min(x for x, y in p), min(y for x, y in p), max(x for x, y in p), max(y for x, y in p))

def modell_A():
    v = M3.V; o = v["outlines"]; Z = {"EG": 0.0, "OG1": 3.5, "ST": 6.5}
    L = lambda k: [tuple(p) for p in o[k]]
    name = {"STAIR": "Treppenhaus", "LIFT": "Aufzug", "LOBBY": "Eingang/Lobby", "LANDING": "Podest", "TECH": "Technik", "WAND": "Wandscheibe", "BUERO": "Büro-Zugang",
            "ABSTELL": "Abstell", "VORRAUM": "Vorraum", "DINING": "Gastraum", "BAR": "Bar", "WC": "WC", "PERSONAL": "Personal", "FLUR": "Flur", "KITCHEN": "Küche",
            "STORE": "Lager", "ANLIEF": "Anlieferung", "OFFICE": "Büro", "CORR": "Flur", "WE": "Wohnung"}
    def rn(r):
        k = r["id"].split("-")[0]; n = name.get(k, k)
        if r["id"].startswith("BUERO-WC"): n = "WC (Büro)"
        if r["id"].startswith("BUERO-FOYER"): n = "Foyer (Büro)"
        return n
    lv = {}
    for key, lid in (("EG", "GF"), ("OG1", "L1"), ("ST", "L2")):
        rooms = [dict(id=r["id"], name=rn(r), rect=tuple(r["rect"]), typ=r["type"], status=r["status"]) for r in v["rooms"] if r["level"] == lid]
        lv[key] = dict(poly=L(lid), rooms=rooms)
    ops = [dict(o_, a0=o_["a"][0], a1=o_["a"][1]) for o_ in M3.openings("plangetreu")]
    bal = [tuple(b["rect"]) for b in v["balconies"]]
    stalls = [tuple(s) for s in v["parking"]["stalls"]]
    return dict(key="A", dat="A_B3_Referenz_Import.pdf", titel="Variante A – B3-Referenz (unverändert)", kurz="A B3-Referenz", gruppe="A", s=None,
                beschr="EG 32,00 × 18,00 m = 576 m² (Gastro EG, Büros rückseitig); 1. OG mit 3,00 m rückseitigem Anbau (ohne Stützen); Staffelgeschoss; fünf Balkone zum Platz; rückseitig teilweise überdeckte Stellplätze. Daten aus dem bestehenden B3-Modell (v4, Planstand Blatt 14), nicht neu gezeichnet.",
                hoehenstatus="aus B3-Modell v4 (Planstand B14); Höhenbezug zur Stadt NOCH OFFEN", quelle="geometry/variant_B3.json (Alt. K), scripts/modell_b3.py v4",
                levels=lv, zfloor=Z, ztop_st=9.6, zattika=9.9, slab=0.30, slab_status="ANNAHME 0,30 m (B3: Unterseite überdeckte Stellplätze +3,20 bei OK 3,50)",
                saeulen=[], openings=ops, balkone=bal, vordach=M3.vordach(), terrasse=tuple(v["roof_terrace"]), schacht=tuple(v["shaft"]["rect"]),
                plot=PLOT, stalls=stalls, aisle=tuple(v["parking"]["aisle"]), walkways=[tuple(w) for w in v["parking"]["walkway_gaps"]], zufahrt=None, eingaenge=[],
                schnitt_x=14.0, rest_hyp=960 - 576, eg_ziel=(32.0, 18.0), ziel_m2=576.0, setback=None,
                offen=["Wandstärken (Darstellung 0,30 m ist ANNAHME)", "Deckenstärken (0,30 m ANNAHME)", "Innentüren und Türanschläge (nicht im Datenbestand) – nicht gezeichnet",
                       "Treppenlauf/Stufen und Aufzugsgröße (nur Raumrechteck vorhanden)", "Fenstermaße OG/Staffel: Lage laut B14/B4, Brüstungs- und Sturzhöhen NOCH OFFEN",
                       "Zufahrt/Fahrgasse-Anbindung an öffentliche Straße", "Grundstückszuschnitt (32 × 30 m = Hypothese H1)", "Höhenbezug (OK Fahrbahn) der Stadt"])

def modell_B(key, titel, dat, s):
    v = VA.V[key]; Z = v["Z"]; eg = v["eg"][0]; og = v["og1"][0]; st = v["st"][0]
    zf = {"EG": 0.0, "OG1": Z["OG1"][0], "ST": Z["ST"][0]}
    rooms = [dict(id=f"EG-{i + 1}", name=n, rect=tuple(r), typ=c, status="ANNAHME") for i, (n, r, c) in enumerate(v["eg_raeume"])]
    lv = {"EG": dict(poly=rect_poly(eg), rooms=rooms), "OG1": dict(poly=rect_poly(og), rooms=[]), "ST": dict(poly=rect_poly(st), rooms=[])}
    stalls = [tuple(x) for x in v["stalls"]]
    return dict(key=key, dat=dat, titel=titel, kurz=key, gruppe="B", s=s,
                beschr=("Neue Idee: EG 18,00 m (Platzseite) × 30,00 m = 540 m² (Hypothese, Grundstück 32 × 30 m = 960 m² unbestätigt, Rest 420 m²); OG1 kragt 1,00 m West, 1,50 m Platzseite, 5,00 m Ost (über Stellplätze) aus, rückseitig bündig (Grundstücksgrenze der Hypothese); "
                        + {0.0: "oberstes Geschoss bündig mit der Außenkante des 1. OG.", 1.5: "oberstes Geschoss 1,50 m hinter der Außenkante des 1. OG zurückgesetzt (rundum).", 3.0: "oberstes Geschoss 3,00 m hinter der Außenkante des 1. OG zurückgesetzt (rundum)."}[s]),
                hoehenstatus="HYPOTHETISCH (Höhenschema EG 4,30 / 1. OG 3,60 / oberstes Geschoss 3,60 / Attika 0,50 = 12,00 m aus varianten_e.py) – NICHT gesichert, nicht verbindlich",
                quelle="studie/varianten_f.py " + key + " (Planungsziel 24.10.2026)",
                levels=lv, zfloor=zf, ztop_st=Z["ST"][1], zattika=Z["ATT"][1], slab=0.45, slab_status="ANNAHME 0,45 m (Wert aus varianten_e.py DECKE)",
                saeulen=[tuple(p) for p in v["saeulen_pts"]], openings=[], balkone=[], vordach=None, terrasse=None, schacht=None,
                plot=PLOT, stalls=stalls, aisle=tuple(v["fahrgasse"]), walkways=[], zufahrt=tuple(v["zufahrt"]), eingaenge=[(n, tuple(r)) for n, r in v["eingaenge"]],
                glasfront=v["glas_front"], schnitt_x=15.0, rest_hyp=960 - 540, eg_ziel=(18.0, 30.0), ziel_m2=540.0, setback=s,
                offen=["Wandstärken (0,30 m Darstellung ANNAHME)", "Deckenstärken (0,45 m ANNAHME)", "Fenster, Türen, Brüstungen: keine Daten – nicht gezeichnet (nur Glasfront-Lage Gastro aus dem Entwurf als ANNAHME)",
                       "Innenaufteilung 1. OG und oberstes Geschoss (Wohnen/Kern) – keine Raumdaten", "Treppen-/Aufzugslage im OG (Kern-Streifen laut Entwurf widerspricht der EG-Kernlage, siehe Konsistenzprotokoll)",
                       "Geschosshöhen (hypothetisch) und Höhenbezug", "Grundstückszuschnitt (Hypothese 32 × 30 m), Lage von Zufahrt/Straße", "Rückseitiger Vorbau: auf der Hypothese-Grenze nicht möglich (0,00 m)",
                       "Stellplatzmaß 2,50 × 5,00 m und Fahrgasse 6,00 m sind Annahmen"])

def alle():
    return [modell_A(),
            modell_B("F1", "Variante B1 – 540 m² EG, Vorbau bündig (oberstes Geschoss bündig zum 1. OG)", "B1_540m2_Vorbau_Buendig_Import.pdf", 0.0),
            modell_B("F2", "Variante B2 – 540 m² EG, Vorbau, Staffel 1,50 m", "B2_540m2_Vorbau_Staffel_150cm_Import.pdf", 1.5),
            modell_B("F3", "Variante B3neu – 540 m² EG, Vorbau, Staffel 3,00 m", "B3_540m2_Vorbau_Staffel_300cm_Import.pdf", 3.0)]

# ---------- Konsistenzprüfung ----------
def pip(p, pt):
    x, y = pt; n = len(p); inside = False
    for i in range(n):
        (x0, y0), (x1, y1) = p[i], p[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0: inside = not inside
    return inside
def rect_ov(a, b, eps=1e-6): return a[0] < b[2] - eps and b[0] < a[2] - eps and a[1] < b[3] - eps and b[1] < a[3] - eps
def col_rect(c): h = SAEULE_D / 2; return (c[0] - h, c[1] - h, c[0] + h, c[1] + h)
def c2(x): return f"{x:.2f}".replace(".", ",")

def pruefe(m):
    F = []  # (Status, Text)  Status: OK / KONFLIKT / HINWEIS
    add = lambda s, t: F.append((s, t))
    eg = m["levels"]["EG"]["poly"]; b = bb(eg); w, d = b[2] - b[0], b[3] - b[1]; fl = poly_area(eg)
    add("OK" if abs(fl - m["ziel_m2"]) < 0.01 and (round(w, 2), round(d, 2)) == m["eg_ziel"] else "KONFLIKT",
        f"EG-Außenmaß {c2(w)} × {c2(d)} m = {fl:.0f} m² (Vorgabe {m['eg_ziel'][0]:.0f} × {m['eg_ziel'][1]:.0f} = {m['ziel_m2']:.0f} m²)")
    add("HINWEIS", f"Restfläche Grundstück (Hypothese 960 m²): {960 - fl:.0f} m² – 960 m² Grundstück ist NICHT bestätigt")
    for k, lv in m["levels"].items():
        ba = bb(lv["poly"])
        if ba[0] < 0 or ba[1] < 0 or ba[2] > 32 or ba[3] > 30:
            add("KONFLIKT", f"{k}: Geschoss ragt über die Hypothese-Grundstücksgrenze 32 × 30 m hinaus (x {c2(ba[0])}…{c2(ba[2])}, y {c2(ba[1])}…{c2(ba[3])}) – Grenze zum Platz/Baulinie NOCH OFFEN")
    z = m["zfloor"]; hs = [z["EG"], z["OG1"], z["ST"], m["ztop_st"], m["zattika"]]
    add("OK" if all(hs[i] < hs[i + 1] for i in range(4)) else "KONFLIKT", "Höhenfolge " + " < ".join(f"{h:+.2f}" for h in hs).replace(".", ",") + " m")
    add("HINWEIS", f"Gesamthöhe Attika-OK {c2(m['zattika'])} m über ±0,00 (OK FFB EG); Bezug zur Stadt (OK Fahrbahn) NOCH OFFEN – keine Aussage zur Zulässigkeit")
    if m["setback"] is not None:
        og, st = bb(m["levels"]["OG1"]["poly"]), bb(m["levels"]["ST"]["poly"]); s = m["setback"]
        ins = (st[0] - og[0], st[1] - og[1], og[2] - st[2], og[3] - st[3])
        add("OK" if all(abs(i - s) < 1e-6 for i in ins) else "KONFLIKT",
            f"Rücksprung oberstes Geschoss zur Außenkante des 1. OG West/Platz/Ost/Rück = {c2(ins[0])} / {c2(ins[1])} / {c2(ins[2])} / {c2(ins[3])} m (Soll {c2(s)} rundum)")
        e = bb(eg); vor = (e[0] - og[0], e[1] - og[1], og[2] - e[2], og[3] - e[3])
        add("KONFLIKT" if min(vor) <= 0 else "OK",
            f"Vorbau (OG1-Kante minus EG-Wand) West/Platz/Ost/Rück = {c2(vor[0])} / {c2(vor[1])} / {c2(vor[2])} / {c2(vor[3])} m – Vorgabe 'umlaufend auf allen vier Seiten' ist rückseitig NICHT erfüllt (Grundstücksgrenze der Hypothese bei y = 30)")
    cs = m["saeulen"]
    if cs:
        og = m["levels"]["OG1"]["poly"]; ob = bb(og)
        add("OK" if len(cs) == len(set(cs)) else "KONFLIKT", f"{len(cs)} Säulen Ø {c2(SAEULE_D)} m, Lage am Rand der Auskragung des 1. OG")
        bad = [c for c in cs if not pip(og, c)]
        add("OK" if not bad else "KONFLIKT", "alle Säulenachsen liegen innerhalb des OG1-Umrisses" if not bad else f"Säulen außerhalb OG1: {bad}")
        near = [(a, c) for i, a in enumerate(cs) for c in cs[i + 1:] if math.dist(a, c) < SAEULE_D + 0.3]
        for a, c in near: add("KONFLIKT", f"Säulen {a} und {c} liegen nur {c2(math.dist(a, c))} m auseinander (Ø 0,40 m, Säulen berühren/überschneiden sich)")
        outg = [c for c in cs if c[1] < 0 or c[0] < 0]
        if outg: add("KONFLIKT", f"{len(outg)} Säulen stehen außerhalb der Hypothese-Grundstücksgrenze (y < 0 bzw. x < 0), z. B. {outg[0]}")
        stall_hit = [(c, s) for c in cs for s in m["stalls"] if rect_ov(col_rect(c), s)]
        add("OK" if not stall_hit else "KONFLIKT", "keine Säule überschneidet einen Stellplatz" if not stall_hit else f"{len(stall_hit)} Säule(n) überschneiden Stellplätze, z. B. Säule {stall_hit[0][0]}")
        inEG = [c for c in cs if rect_ov(col_rect(c), bb(eg))]
        add("OK" if not inEG else "KONFLIKT", "keine Säule steht im EG-Gebäude" if not inEG else f"{len(inEG)} Säule(n) im EG-Grundriss")
        ysx = sorted({round(c[1], 3) for c in cs if abs(c[0] - ob[2] + 0.35) < 1e-6})
        gaps = [round(ysx[i + 1] - ysx[i], 2) for i in range(len(ysx) - 1)]
        add("HINWEIS", "Achsabstände Ostreihe: " + ", ".join(c2(g) for g in gaps) + " m (Raster 5,40 m aus Stellplatzpaaren, unregelmäßig am Ende)")
        rear = [c for c in cs if abs(c[1] - ob[3] + 0.35) < 1e-6]
        add("HINWEIS", f"Rückseite (y = {c2(ob[3] - 0.35)} m): {len(rear)} Säulen – Rückfassade des 1. OG ist zwischen den Ecken ohne Säulen")
    ops = m["openings"]
    if ops:
        lvk = lambda zz: "EG" if zz < m["zfloor"]["OG1"] else ("OG1" if zz < m["zfloor"]["ST"] else "ST")
        bad = []
        for o in ops:
            p = m["levels"][lvk(o["z"][0])]["poly"]; sd = o["side"]; pos = o["pos"]; ok = False
            for i in range(len(p)):
                (x0, y0), (x1, y1) = p[i], p[(i + 1) % len(p)]
                if sd in ("-y", "+y") and y0 == y1 and abs(y0 - pos) < 0.05 and min(x0, x1) - 1e-6 <= o["a0"] and o["a1"] <= max(x0, x1) + 1e-6: ok = True
                if sd in ("-x", "+x") and x0 == x1 and abs(x0 - pos) < 0.05 and min(y0, y1) - 1e-6 <= o["a0"] and o["a1"] <= max(y0, y1) + 1e-6: ok = True
            if not ok: bad.append(o)
        add("OK" if not bad else "KONFLIKT", f"{len(ops) - len(bad)} von {len(ops)} Öffnungen liegen auf einer Fassadenlinie des zugehörigen Geschosses" + ("" if not bad else "; nicht auf Fassade: " + "; ".join(f"{o['tag']} ({o['side']} pos {o['pos']})" for o in bad)))
    for nm, rs in (("Balkon", m["balkone"]), ("Vordach", [(m["vordach"]["x"][0], m["vordach"]["y"][0], m["vordach"]["x"][1], m["vordach"]["y"][1])] if m["vordach"] else [])):
        outb = [r for r in rs if r[1] < 0]
        if outb: add("KONFLIKT", f"{nm}: {len(outb)} Bauteil(e) ragen über die Hypothese-Grenze zum Platz (y < 0) bis y = {c2(min(r[1] for r in outb))} m – Grenze/Baulinie NOCH OFFEN")
    if m["vordach"]: add("HINWEIS", "Stahlvordach Terrasse (Unterseite +3,00 m): Stützen/Abhängung nicht belegt – keine ergänzt")
    for k, lv in m["levels"].items():
        rr = lv["rooms"]
        if not rr: continue
        rect_of = {r["id"]: r["rect"] for r in rr}
        inside = lambda a, c: a[0] >= c[0] and a[1] >= c[1] and a[2] <= c[2] and a[3] <= c[3]
        ov = [(a["id"], c["id"]) for i, a in enumerate(rr) for c in rr[i + 1:] if rect_ov(a["rect"], c["rect"])]
        nest = [(a, c) for a, c in ov if inside(rect_of[a], rect_of[c]) or inside(rect_of[c], rect_of[a])]
        real = [x for x in ov if x not in nest]
        add("OK" if not ov else ("KONFLIKT" if real else "HINWEIS"), f"{k}: {len(rr)} Räume, keine Überschneidungen" if not ov else (f"{k}: Raumüberschneidungen {real}" if real else f"{k}: {len(rr)} Räume; verschachtelt (Raum liegt im Rechteck eines anderen): {nest} – Flächensumme dadurch größer als Geschossfläche"))
        ra = sum((r["rect"][2] - r["rect"][0]) * (r["rect"][3] - r["rect"][1]) for r in rr)
        add("OK" if abs(ra - poly_area(lv["poly"])) < 0.05 else "HINWEIS", f"{k}: Raumflächensumme {ra:.1f} m² (brutto) gegen Geschossumriss {poly_area(lv['poly']):.1f} m²".replace(".", ","))
    if m["gruppe"] == "B":
        add("KONFLIKT", "Kern: EG-Kern x 1–5 / y 0–9,5 m; Entwurf nennt für die Obergeschosse einen Kern-Streifen y −1,5…2,5 m über die volle Breite – Treppe/Aufzug im OG liegen nicht über dem EG-Kern; Lage NOCH OFFEN, im OG-Plan nicht gezeichnet")
        add("HINWEIS", "Fenster, Türen, Brüstungen und Geschossraumaufteilung für B1–B3 liegen nicht vor – Ansichten ohne Öffnungen, OG ohne Räume (bewusst nicht erfunden)")
    st = m["stalls"]
    dims = {(round(s[2] - s[0], 2), round(s[3] - s[1], 2)) for s in st}
    add("HINWEIS", f"{len(st)} Stellplätze; Rechteckmaße in x × y {sorted(dims)} – 2,50 × 5,00 m und 6,00 m Fahrgasse sind ANNAHMEN")
    ov = [(a, c) for i, a in enumerate(st) for c in st[i + 1:] if rect_ov(a, c)]
    add("OK" if not ov else "KONFLIKT", "Stellplätze überschneiden sich nicht" if not ov else f"{len(ov)} Stellplatz-Überschneidungen")
    hit = [s for s in st if rect_ov(s, bb(eg))]
    add("OK" if not hit else "KONFLIKT", "kein Stellplatz liegt im EG-Gebäude" if not hit else f"{len(hit)} Stellplätze im EG-Gebäude")
    pl = bb(m["plot"]); outp = [s for s in st if s[0] < pl[0] or s[1] < pl[1] or s[2] > pl[2] or s[3] > pl[3]]
    add("OK" if not outp else "KONFLIKT", "alle Stellplätze innerhalb der Hypothese-Grundstücksgrenze" if not outp else f"{len(outp)} Stellplätze außerhalb des Grundstücks")
    ogb = bb(m["levels"]["OG1"]["poly"])
    if m["gruppe"] == "A":
        cov = [s for s in st if rect_ov(s, (4, 18, 32, 21))]
        add("HINWEIS", f"{len(cov)} von {len(st)} Stellplätzen teilweise überdeckt (OG1-Anbau y 18–21, Stellplatztiefe y 18–23, ca. 3,00 m von 5,00 m); Stellplätze x 0–4 unbedeckt")
    else:
        full = [s for s in st if s[0] >= ogb[0] and s[2] <= ogb[2] and s[1] >= ogb[1] and s[3] <= ogb[3]]
        add("HINWEIS", f"{len(full)} von {len(st)} Stellplätzen vollständig vom 1. OG überdeckt (Ostauskragung 5,00 m über der Stellplatzreihe); Parallelparker außerhalb")
    a = m["aisle"]
    add("HINWEIS", f"Fahrgasse {c2(a[2] - a[0])} × {c2(a[3] - a[1])} m (Annahme)")
    return F

if __name__ == "__main__":
    for m in alle():
        print("==", m["key"], m["titel"])
        for s, t in pruefe(m): print(f"  [{s}] {t}")
