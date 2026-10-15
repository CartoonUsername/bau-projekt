// Alternativen zu Dauermietwohnungen: Airbnb/Apartments und Hotel (je mit Gastro im EG), Variante A (930 m² BGF)
const { A, VARIANTEN, finanz, cashflow } = require("./model");
const v = VARIANTEN.sechs;
const gastroNetto = v.umsatz * A.gastroMargeVorPacht - v.pacht * A.ruecklagen; // Gastro-Gewinn, Rücklage auf die Pacht wie im Hausmodell

// Airbnb / Apartments
const AIRBNB = {
  apartments: [{ n: 3, m2: 85, gaeste: 4, preis: 100 }, { n: 3, m2: 56, gaeste: 2, preis: 85 }],
  einrichtungM2: 600, // € je m² möbliert (Möbel, Küche, Wäsche, Technik), Annahme
  kosten: { plattform: 0.15, reinigung: 0.2, nebenkosten: 0.08, material: 0.02, versicherungSoftware: 0.03, ruecklage: 0.08 }, // in % vom Umsatz, Annahmen
};
function airbnb(ausl = 0.45, opts = {}) {
  const preisFaktor = opts.preisFaktor ?? 1;
  const wfl = AIRBNB.apartments.reduce((a, x) => a + x.n * x.m2, 0);
  const einrichtung = wfl * AIRBNB.einrichtungM2;
  const umsatzJahr = AIRBNB.apartments.reduce((a, x) => a + x.n * x.preis * preisFaktor * 365 * ausl, 0);
  const quote = Object.values(AIRBNB.kosten).reduce((a, b) => a + b, 0);
  const netto = (umsatzJahr * (1 - quote)) / 12;
  const fin = finanz(v, 0, opts.zins ?? A.zinsPlan, { gastroAusbau: v.gastroAusbau + einrichtung });
  const cf = gastroNetto + netto - fin.rate;
  return { ausl, einrichtung, umsatzMonat: umsatzJahr / 12, quote, netto, fin, cf, wfl };
}

// Hotel (Eigenbetrieb oder Verpachtung), Zimmer im 1. OG und in der Staffel
const HOTEL = {
  zimmer: 15, // OG ca. 9 + Staffel ca. 6 (ca. 38 m² BGF je Zimmer inkl. Flur)
  einrichtungJeZimmer: 18000, // Annahme
  preis: 85, // € Zimmer inkl. Frühstück, Annahme
  kosten: { personal: 0.28, fruehstueck: 0.08, energie: 0.06, reinigungWaesche: 0.1, vertrieb: 0.12, verwaltungSonst: 0.08 }, // % vom Umsatz
  pachtQuote: 0.22, // bei Verpachtung, % vom Umsatz (Annahme)
};
function hotel(ausl = 0.52, opts = {}) {
  const einrichtung = HOTEL.zimmer * HOTEL.einrichtungJeZimmer;
  const umsatzJahr = HOTEL.zimmer * (opts.preis ?? HOTEL.preis) * 365 * ausl;
  const quote = Object.values(HOTEL.kosten).reduce((a, b) => a + b, 0);
  const gopMonat = (umsatzJahr * (1 - quote)) / 12; // Eigenbetrieb, vor Rate
  const pachtMonat = (umsatzJahr * HOTEL.pachtQuote) / 12;
  const fin = finanz(v, 0, opts.zins ?? A.zinsPlan, { gastroAusbau: v.gastroAusbau + einrichtung });
  const hotelErtrag = opts.verpachtet ? pachtMonat * (1 - A.ruecklagen) : gopMonat;
  const cf = gastroNetto + hotelErtrag - fin.rate;
  return { ausl, einrichtung, umsatzMonat: umsatzJahr / 12, quote, gopMonat, pachtMonat, fin, cf, zimmer: HOTEL.zimmer };
}

const dauermiete = () => {
  const fin = finanz(v, 0, A.zinsPlan);
  return { fin, cf: cashflow(v, fin).cf, nettoMiete: v.mieteOhnePacht * (1 - A.ruecklagen) };
};

module.exports = { AIRBNB, HOTEL, airbnb, hotel, dauermiete, gastroNetto };
