// Gibt die Szenario-Tabellen des Rechenmodells als JSON aus (für den Excel-Export)
const { A, VARIANTEN, finanz, cashflow, umsatzBreakEven } = require("./model");
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
console.log(JSON.stringify(out));
