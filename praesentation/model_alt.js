// Nutzungsoptionen für Variante B (540 m² Grundfläche, 1.540 m² BGF): Dauermiete, Airbnb/Apartments, Hotel (je mit Gastro und Büro im EG)
const { A, VARIANTEN, finanz, cashflow, teilung, LAYOUTS } = require("./model");
const v = VARIANTEN.sechs;
const L = LAYOUTS.B;
const mOG = L.wfOG / L.nOG; // 83 m²
const mST = L.wfST / L.nST; // 103 m²
const gastroNetto = v.umsatz * A.gastroMargeVorPacht - v.pacht * A.ruecklagen; // Gastro-Gewinn, Rücklage auf die Pacht wie im Hausmodell
const bueroNetto = v.bueroM2 * 10 * (1 - A.ruecklagen); // Büro 10 €/m², nach Rücklage

// Airbnb / Apartments
const AIRBNB = {
  apartments: [{ typ: "OG", n: L.nOG, m2: mOG, gaeste: 4, preis: 100 }, { typ: "ST", n: L.nST, m2: mST, gaeste: 6, preis: 125 }],
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
  const cf = gastroNetto + bueroNetto + netto - fin.rate;
  return { ausl, einrichtung, umsatzMonat: umsatzJahr / 12, quote, netto, fin, cf, wfl };
}

// Hotel (Eigenbetrieb oder Verpachtung), Zimmer im 1. OG und in der Staffel
const HOTEL = {
  zimmer: 24, // OG ca. 14 + Staffel ca. 10 (ca. 38–42 m² BGF je Zimmer inkl. Flur)
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
  const cf = gastroNetto + bueroNetto + hotelErtrag - fin.rate;
  return { ausl, einrichtung, umsatzMonat: umsatzJahr / 12, quote, gopMonat, pachtMonat, fin, cf, zimmer: HOTEL.zimmer };
}

const dauermiete = () => {
  const fin = finanz(v, 0, A.zinsPlan);
  return { fin, cf: cashflow(v, fin).cf, nettoMiete: v.mieteOhnePacht * (1 - A.ruecklagen) };
};

// Auslastung, bei der ein Konzept so viel bringt wie die Dauermiete (Bisektion)
function gleichauf(fn, ziel) {
  let lo = 0.05, hi = 1.5;
  for (let i = 0; i < 50; i++) { const mid = (lo + hi) / 2; if (fn(mid) < ziel) lo = mid; else hi = mid; }
  return (lo + hi) / 2;
}

// Verkauf der Einheiten an Verwandte (je Einheit ein Kredit, kein Eigenkapital, Preis = Selbstkosten oder Zielpreis für plus €)
function verkauf(konzept, ausl, plus = 250, zins = A.zinsPlan) {
  const t = teilung(L, zins);
  const k = t.k;
  const preisFuer = (einnahme, til) => Math.max(0, ((einnahme - plus) * 12) / (k * (zins + til)));
  const rate = (preis, til) => (preis * k * (zins + til)) / 12;
  const einheiten = [];
  const mk = (name, n, kosten, einnahme) => einheiten.push({ name, n, kosten, einnahme, rate: rate(kosten, A.tilgung), ergebnis: einnahme - rate(kosten, A.tilgung), preisPlus: preisFuer(einnahme, 0) });
  if (konzept === "miete") {
    mk(`Wohnung ${Math.round(mOG)} m² (1. OG)`, L.nOG, t.oG(mOG).kosten, mOG * 950 / 85 * (1 - A.ruecklagen));
    mk(`Penthouse ${Math.round(mST)} m² (Staffel)`, L.nST, t.st(mST).kosten, mST * 950 / 85 * (1 - A.ruecklagen));
  } else if (konzept === "airbnb") {
    const quote = Object.values(AIRBNB.kosten).reduce((a, b) => a + b, 0);
    for (const ap of AIRBNB.apartments) {
      const bau = (ap.typ === "OG" ? t.oG(ap.m2) : t.st(ap.m2)).kosten;
      const moebel = ap.m2 * AIRBNB.einrichtungM2;
      mk(`Apartment ${Math.round(ap.m2)} m²`, ap.n, bau + moebel, (ap.preis * 365 * ausl * (1 - quote)) / 12);
    }
  } else {
    const einricht = HOTEL.zimmer * HOTEL.einrichtungJeZimmer;
    const proZimmer = (t.kostenOG + t.kostenST + einricht) / HOTEL.zimmer;
    mk("Hotelzimmer", HOTEL.zimmer, proZimmer, (HOTEL.preis * 365 * ausl * HOTEL.pachtQuote * (1 - A.ruecklagen)) / 12); // Pacht je Zimmer nach Rücklage
  }
  const luecke = einheiten.reduce((a, e) => a + e.n * Math.max(0, e.kosten - e.preisPlus), 0);
  const gewinn = v.umsatz * A.gastroMargeVorPacht - A.lohn;
  const rateEG = (t.gastro.kosten * k * (zins + A.tilgung)) / 12;
  const zinsLuecke = (luecke * k * zins) / 12;
  return { einheiten, luecke, rateEG, zinsLuecke, bessam: gewinn - rateEG - zinsLuecke + t.gastro.buero, gewinn };
}

module.exports = { AIRBNB, HOTEL, airbnb, hotel, dauermiete, gastroNetto, bueroNetto, gleichauf, verkauf, mOG, mST };
