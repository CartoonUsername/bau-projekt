// Gibt die Szenario-Tabellen des Rechenmodells als JSON aus (für den Excel-Export)
const { A, VARIANTEN, finanz, cashflow, umsatzBreakEven, teilung, zielplus, LAYOUTS } = require("./model");
const v = VARIANTEN.sechs;
const F = [0, 0.05, 0.1, 0.15, 0.2, 0.25];
const out = { foerderung: [], umsatz: [], variante4: null };
for (const f of F) {
  const p = finanz(v, f, A.zinsPlan), a = finanz(v, f, A.zinsAusgang);
  out.foerderung.push({ f, gesamt: p.gesamt, kreditPlan: p.kredit, ratePlan: p.rate, cfPlan: cashflow(v, p).cf, kreditAus: a.kredit, rateAus: a.rate, cfAus: cashflow(v, a).cf, bePlan: umsatzBreakEven(v, p), beAus: umsatzBreakEven(v, a) });
}
for (const f of [0, 0.1, 0.15, 0.2]) {
  const p = finanz(v, f, A.zinsPlan);
  out.umsatz.push({ f, werte: [40000, 45000, 50000, 55000, 60000].map((u) => cashflow(v, p, u).cf) });
}
const v4 = Object.assign({}, v, { bgf: 1270, mieteOhnePacht: 9 * 950 });
const g0 = finanz(v4, 0, A.zinsPlan), g15 = finanz(v4, 0.15, A.zinsPlan);
out.variante4 = { gesamt: g0.gesamt, rate: g0.rate, cf0: cashflow(v4, g0).cf, cf15: cashflow(v4, g15).cf };
const ref = finanz(v, 0, A.zinsPlan);
out.referenz = { gesamt: ref.gesamt, kredit: ref.kredit, rate: ref.rate, cf: cashflow(v, ref).cf, zinsenBau: ref.zinsenBau, bereit: ref.bereit, aufschub: ref.aufschubZinsen };
const vb = VARIANTEN.b;
const vc = VARIANTEN.c;
const fa = finanz(v, 0, A.zinsPlan), fb = finanz(vb, 0, A.zinsPlan), fc = finanz(vc, 0, A.zinsPlan);
const pick = (e) => ({ m2: e.m2, kosten: e.kosten, kostenM2: e.kostenM2, rate: e.rate, miete: e.miete, ergebnis: e.ergebnis, preisFuerPlus: e.preisFuerPlus, luecke: e.luecke, ergebnisF15: e.ergebnisF15 });
out.verkauf = {};
for (const key of ["A", "B", "C"]) {
  const t = teilung(LAYOUTS[key]);
  out.verkauf[key] = { og85: pick(t.oG(85, 950)), st56: pick(t.st(56, 950)), st56Markt: pick(t.st(56)), gastro: t.gastro, ogM2: t.ogM2, stM2: t.stM2, preisFuerPlusM2: t.preisFuerPlusM2 };
}
out.varianteB = { A: { gesamt: fa.gesamt, rate: fa.rate, cf: cashflow(v, fa).cf, be: umsatzBreakEven(v, fa) }, B: { gesamt: fb.gesamt, rate: fb.rate, cf: cashflow(vb, fb).cf, be: umsatzBreakEven(vb, fb) }, C: { gesamt: fc.gesamt, rate: fc.rate, cf: cashflow(vc, fc).cf, be: umsatzBreakEven(vc, fc) } };
out.ziel = {};
for (const [key, z] of [["plan", A.zinsPlan], ["ausgang", A.zinsAusgang]]) {
  const r = zielplus(LAYOUTS.A, 250, z);
  out.ziel[key] = { og: r.og, st: r.st, luecke: r.luecke, zinsLuecke: r.zinsLuecke, rateEG: r.rateEG, bessam: r.bessam };
}
console.log(JSON.stringify(out));
