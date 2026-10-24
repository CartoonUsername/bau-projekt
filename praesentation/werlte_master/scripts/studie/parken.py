"""Parkplatzprüfung (Geometrie) für alle Varianten mit Stellplatzkonzept (E1–E4, F1–F4).
Annahmen: Stellplatz 90° 2,50 × 5,00 m, Parallelparker 2,00 × 5,50 m, Fahrgasse 6,00 m, Säule Ø 0,40 m, Nutzbreite ≥ 2,30 m (eingeschränkt < 2,40 m).
Prüft je Stellplatz: im Grundstück, nicht im EG, nicht in Eingangszonen, Nutzbreite zwischen Säulen, 6-m-Freiraum vor dem Platz frei von Säulen/EG/anderen Plätzen, Anschluss der Fahrgasse an die Zufahrt.
KEINE Schleppkurvensimulation."""
import math, varianten as VA
GASSE = 6.0; PLOT = (0.0, 0.0, 32.0, 30.0); R = 0.2
def hit_circle_rect(c, rect):
    cx, cy = c; x0, y0, x1, y1 = rect; nx, ny = min(max(cx, x0), x1), min(max(cy, y0), y1); return math.hypot(cx - nx, cy - ny) < R - 1e-9
def overlap(a, b, eps=1e-6): return not (a[2] <= b[0] + eps or a[0] >= b[2] - eps or a[3] <= b[1] + eps or a[1] >= b[3] - eps)
def intrusion(st, cols):
    x0, y0, x1, y1 = st; horiz = (x1 - x0) <= (y1 - y0); best = 0.0   # horiz: Breite liegt in x-Richtung (kürzere Seite)
    a0, a1, b0, b1 = (x0, x1, y0, y1) if horiz else (y0, y1, x0, x1)
    for bb in [b0 + (b1 - b0) * i / 20 for i in range(21)]:
        tot = 0.0
        for (cx, cy) in cols:
            ca, cb = (cx, cy) if horiz else (cy, cx)
            if abs(cb - bb) < R:
                h = math.sqrt(max(0, R * R - (cb - bb) ** 2)); lo, hi = max(ca - h, a0), min(ca + h, a1)
                if hi > lo: tot += hi - lo
        best = max(best, tot)
    return best
def band(st, face):
    x0, y0, x1, y1 = st
    return {"E": (x1, y0, x1 + GASSE, y1), "W": (x0 - GASSE, y0, x0, y1), "S": (x0, y1, x1, y1 + GASSE), "N": (x0, y0 - GASSE, x1, y0)}[face]
def stall_list(v):
    out = []
    f = v.get("stall_face", {})
    for key in ("row1", "row2", "par"):
        rows = v.get({"row1": "stalls_row1", "row2": "stalls_row2", "par": "stalls_par"}[key], [])
        for r in rows: out.append(dict(rect=tuple(r), art=("par" if key == "par" else "90"), face=f.get(key, "S")))
    return out
def pruefe(key):
    v = VA.V[key]; cols = v["saeulen_pts"]; res = dict(stalls=[], gesamt=0, voll=0, eingeschraenkt=0, konflikt=0, hinweise=[])
    fg = v["fahrgasse"]; zu = v["zufahrt"]
    # Fahrgasse frei?
    fg_probleme = []
    for c in cols:
        if hit_circle_rect(c, fg): fg_probleme.append("Säule in Fahrgasse")
    for e in v["eg"]:
        if overlap(e, fg): fg_probleme.append("Erdgeschoss in Fahrgasse")
    breite = min(fg[2] - fg[0], fg[3] - fg[1])
    if breite < GASSE - 1e-6: fg_probleme.append(f"Fahrgasse nur {breite:.2f} m")
    anschluss = (abs(fg[2] - zu[0]) < 1e-6 and zu[1] >= fg[1] - 1e-6 and zu[3] <= fg[3] + 1e-6) if v.get("zufahrt_dir") == "E" else (abs(fg[3] - zu[1]) < 1e-6 and zu[0] >= fg[0] - 1e-6 and zu[2] <= fg[2] + 1e-6)
    if not anschluss: fg_probleme.append("Fahrgasse ohne Anschluss an die Zufahrt")
    res["fahrgasse_probleme"] = sorted(set(fg_probleme)); res["fahrgasse_breite"] = breite
    for i, sd in enumerate(stall_list(v), 1):
        r = sd["rect"]; g = []; w_ = []
        if r[0] < PLOT[0] - 1e-6 or r[2] > PLOT[2] + 1e-6 or r[3] > PLOT[3] + 1e-6 or r[1] < PLOT[1] - 1e-6: g.append("außerhalb Grundstück")
        if any(overlap(r, e) for e in v["eg"]): g.append("im Erdgeschoss")
        for n, z in v.get("eingaenge", []):
            if overlap(r, z): g.append("Eingangszone " + n)
        wd = min(r[2] - r[0], r[3] - r[1]) - intrusion(r, cols)
        if wd < 2.30 - 1e-6 and sd["art"] == "90": g.append(f"Nutzbreite {wd:.2f} m < 2,30 m")
        if sd["art"] == "90":
            b = band(r, sd["face"])
            if not (b[0] >= fg[0] - 1e-6 and b[2] <= fg[2] + 1e-6 and b[1] >= fg[1] - 1e-6 and b[3] <= fg[3] + 1e-6): g.append("6-m-Fahrgasse vor dem Platz nicht vollständig vorhanden")
            for c in cols:
                if hit_circle_rect(c, b): g.append("Säule im Ausparkbereich")
            for o in stall_list(v):
                if o["rect"] != r and overlap(b, o["rect"]): g.append("anderer Stellplatz im Ausparkbereich"); break
        else:
            if not (abs(r[0] - fg[2]) < 1e-6 or abs(r[2] - fg[0]) < 1e-6): g.append("Parallelparker nicht an Fahrgasse")
        if g: status = "konflikt"
        elif sd["art"] == "90" and wd < 2.40: status = "eingeschraenkt"; w_.append(f"Säule an der Platzgrenze, Nutzbreite {wd:.2f} m")
        elif sd["art"] == "par": status = "eingeschraenkt"; w_.append("Parallelparker 2,00 × 5,50 m (Annahme), Randlage")
        else: status = "voll"
        res["stalls"].append(dict(nr=i, rect=r, art=sd["art"], face=sd["face"], status=status, gruende=g, hinweise=w_, nutzbreite=round(wd, 2)))
    res["gesamt"] = len(res["stalls"]); res["voll"] = sum(1 for s in res["stalls"] if s["status"] == "voll"); res["eingeschraenkt"] = sum(1 for s in res["stalls"] if s["status"] == "eingeschraenkt"); res["konflikt"] = sum(1 for s in res["stalls"] if s["status"] == "konflikt")
    res["nutzbar"] = res["voll"] + res["eingeschraenkt"]; res["min_nutzbreite"] = min([s["nutzbreite"] for s in res["stalls"] if s["art"] == "90"] or [0])
    if res["fahrgasse_probleme"]: res["nutzbar"] = 0
    # Sackgasse: Fahrgasse endet an Grundstücksgrenze/Platz?
    if v.get("zufahrt_dir") == "S": res["hinweise"].append("Fahrgasse ist Sackgasse zum Platz hin: Wenden im Gassenende (Dreipunktwende) nötig – Schleppkurve prüfen")
    res["hinweise"] += ["Geometrische Prüfung ohne Schleppkurven; 90°-Stellplätze 2,50 × 5,00 m und Fahrgasse 6,00 m sind Planungsannahmen", "Zufahrt (Lage der Straße) ist Annahme", "Feuerwehrzufahrt/Aufstellflächen unter dem Vorbau nicht nachgewiesen (Prüfbedarf)"]
    return res
def flaechenbilanz(key, step=0.25):
    """Aufteilung der Grundstücksfläche (H1 32 × 30 m = 960 m²) in EG, nutzbare Stellplätze, Fahrgasse, Eingangs-/Zugangszonen und nur rechnerisch verbleibende Restfläche."""
    v = VA.V[key]; pk = pruefe(key); cnt = dict(eg=0.0, stall=0.0, par=0.0, fahr=0.0, zone=0.0, rest=0.0); n = int(32 / step); m = int(30 / step); a = step * step
    st = [(s["rect"], s["art"], s["status"]) for s in pk["stalls"]]
    for i in range(n):
        for j in range(m):
            x, y = (i + 0.5) * step, (j + 0.5) * step; p = (x, y, x, y)
            def inside(r): return r[0] <= x < r[2] and r[1] <= y < r[3]
            if any(inside(e) for e in v["eg"]): cnt["eg"] += a
            elif any(inside(r) and stt != "konflikt" and art == "90" for r, art, stt in st): cnt["stall"] += a
            elif any(inside(r) and stt != "konflikt" and art == "par" for r, art, stt in st): cnt["par"] += a
            elif inside(v["fahrgasse"]): cnt["fahr"] += a
            elif any(inside(z) for nme, z in v.get("eingaenge", [])): cnt["zone"] += a
            else: cnt["rest"] += a
    return {k: round(x, 1) for k, x in cnt.items()}
if __name__ == "__main__":
    import sys
    for k in sys.argv[1:] or ["E1", "E4", "F1", "F4"]:
        r = pruefe(k); print(k, r["gesamt"], "voll", r["voll"], "eingeschr.", r["eingeschraenkt"], "Konflikt", r["konflikt"], r["fahrgasse_probleme"], r["min_nutzbreite"], flaechenbilanz(k))
        for s in r["stalls"]:
            if s["gruende"]: print("   ", s["nr"], s["gruende"])
