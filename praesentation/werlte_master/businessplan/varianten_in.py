"""Eingangswerte je Variante aus dem gemeinsamen Geometriemodell (studie/varianten_daten, vergleichsstudie_ab)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "studie"))
import vergleichsstudie_ab as VS
import finanz as F
D = VS.D
def inp(k):
    d = D[k]; f = d["flaeche"]; a = k == "A"
    return dict(bgf=f["eg"] + f["og1"] + f["st"], bgf_top=f["st"], terr=f["og1"] - f["st"], wfl=d["wfl"], we=d["mix"]["standard"]["we"], gastro_nf=440.0 if a else 376.0,
                buero_nf=d["stp"]["buero_m2"], plaetze=d["stp"]["sitze_innen"], aussen_m2=384.0 if a else 420.0, plaetze_terr=d["stp"]["sitze_terrasse"])
KEYS = {"A": ["A"], "B": ["F1", "F2", "F3"]}
def alle(): return {k: (inp(k), F.rechne(inp(k))) for k in ("A", "F1", "F2", "F3")}
if __name__ == "__main__":
    for k, (v, r) in alle().items():
        print(k, {x: round(y, 1) for x, y in v.items()})
        print("  gesamt", round(r["gesamt"]), "kfw", round(r["kfw_w"]), round(r["kfw_g"]), "bank", round(r["bank"]), "rate/m", round(r["rate_m"]), "roh", round(r["roh"]), "vor", round(r["vor"]), "cash", round(r["cash"]), "dscr", round(r["dscr_ges"], 2), round(r["dscr_imm"], 2), "ew", round(r["ew"]), "ausl", round(r["auslauf"], 2), "umsatz", round(r["umsatz"]))
