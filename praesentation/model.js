// Rechenmodell Baufeld 3 – Neue Mitte Werlte (Variante B, 960 m² BGF)
// Alle Annahmen stehen hier an einer Stelle; build_deck.js liest nur von hier.

const A = {
  grundstueck: 236256, // 960 m² x 230 € + 5 % GrESt + ca. 2 % Notar/Grundbuch
  bgf: 960,
  bauKostenM2: 2200, // Annahme des Bauherrn (Bekanntenpreis), durch Angebot zu belegen
  bnk: 0.15,
  holzAbschlag: 400, // €/m² günstiger als Massivbau beim Staffelgeschoss in Holzbau (Annahme, Angebot der Zimmerei nötig)
  terrassePreis: 450, // €/m² Dachterrasse (Abdichtung, Holzrost, Geländer, Annahme)
  bauRabatt: 0, // Preisnachlass durch Bauunternehmer/Zimmerei aus dem Bekanntenkreis (Annahme 0 %)
  bauMonate: 15,
  bereitstellung: 0.03, // p. a., ab Monat 7 auf noch nicht abgerufenen Betrag
  aufschubMonate: 12, // Rate ausgesetzt, Zinsen werden aufgeschlagen
  tilgung: 0.01,
  zinsPlan: 0.033,
  zinsAusgang: 0.04,
  lohn: 6000,
  ruecklagen: 0.1, // Anteil an Miete + Pacht
  gastroMargeVorPacht: 0.305, // Anteil vom Umsatz (12.200 € bei 40.000 €)
  umsatz: 40000,
};

const VARIANTEN = {
  sechs: {
    key: "sechs",
    name: "6 Wohnungen, große Gastro im EG",
    bgf: 930, // EG 340 + 1. OG 340 + Staffelgeschoss 250 (Holzbau, mit umlaufender Terrasse)
    gastroM2: 290,
    bueroM2: 0,
    wohnungen: 6,
    holzM2: 250, // Staffelgeschoss in Holzbau (Zimmerei)
    terrasseM2: 90, // umlaufende Dachterrasse auf dem 1. OG, zählt nicht zur BGF
    wohnflaeche: 423, // 1. OG 3 x 85 m² + Staffel 3 x 56 m²
    gastroAusbau: 150000, // Annahme des Bauherrn, einfacher Ausbau
    mieteOhnePacht: 6 * 950, // 5.700 € Kaltmiete
    pacht: 290 * 12, // 3.480 €
    umsatz: 50000,
  },
  b: {
    key: "b",
    name: "Variante B: 540 m² Grundfläche, Gastro + Büro im EG, OG, Staffel",
    bgf: 1500, // EG 540 + 1. OG 540 + Staffel 420 (Holzbau, Terrasse rundum)
    holzM2: 420,
    terrasseM2: 120,
    gastroM2: 290,
    bueroM2: 150,
    wohnungen: 8,
    wohnflaeche: 738, // 1. OG ca. 415 m² + Staffel ca. 323 m²
    gastroAusbau: 150000,
    mieteOhnePacht: 738 * (950 / 85) + 150 * 10, // Wohnen 11,18 €/m² + Büro 10 €/m²
    pacht: 290 * 12,
    umsatz: 50000,
  },
  flach: {
    key: "flach",
    name: "EG Gastro, 8 Wohnungen in 2 Obergeschossen, Flachdach",
    bgf: 1020, // 3 Geschosse x 340 m²
    gastroM2: 290,
    bueroM2: 0,
    gastroAusbau: 310000,
    mieteOhnePacht: 8 * 950, // 8 Wohnungen à 950 € Kaltmiete = 7.600 €
    pacht: 290 * 12, // 3.480 €
  },
  dach950: {
    key: "dach950",
    name: "EG Gastro, 8 Wohnungen in OG und Dach, 960 m² BGF",
    bgf: 960,
    gastroM2: 290,
    bueroM2: 0,
    gastroAusbau: 310000,
    mieteOhnePacht: 8 * 950,
    pacht: 290 * 12,
  },
  gross: {
    key: "gross",
    name: "große Gastro im ganzen EG",
    gastroM2: 290,
    bueroM2: 0,
    gastroAusbau: 310000, // normal 257.250 € bei 190 m² + 100 m² Gastraum + modernere Bar
    mieteOhnePacht: 260 * 11 + 190 * 12, // 4 WE im 1. OG (260 m²) + 4 WE im DG (190 m²) = 5.140 €
    pacht: 290 * 12, // 3.480 €
  },
  mit: {
    key: "mit",
    name: "mit Büro",
    gastroM2: 190,
    bueroM2: 70,
    gastroAusbau: 257250,
    mieteOhnePacht: 260 * 11 + 180 * 12 + 70 * 10, // 5.720 €
    pacht: 190 * 12, // 2.280 €
  },
  ohne: {
    key: "ohne",
    name: "ohne Büro",
    gastroM2: 260,
    bueroM2: 0,
    gastroAusbau: 287250,
    mieteOhnePacht: 260 * 11 + 180 * 12, // 5.020 €
    pacht: 260 * 12, // 3.120 €
  },
};

// Reine Baukosten (ohne Baunebenkosten): Massivbau, Holz-Abschlag, Terrasse, Rabatt
function bauRoh(v, opts = {}) {
  const massiv = (v.bgf ?? A.bgf) * (opts.bauKostenM2 ?? A.bauKostenM2);
  const holz = (v.holzM2 ?? 0) * (opts.holzAbschlag ?? A.holzAbschlag);
  const terr = (v.terrasseM2 ?? 0) * A.terrassePreis;
  return (massiv - holz + terr) * (1 - (opts.bauRabatt ?? A.bauRabatt));
}

function finanz(v, foerderung, zins, opts = {}) {
  const f = foerderung;
  const land = (opts.grundstueck ?? A.grundstueck) * (1 - f);
  const bauKosten = bauRoh(v, opts);
  const bau = bauKosten * (1 + A.bnk);
  const gastro = (opts.gastroAusbau ?? v.gastroAusbau) * (1 - f);
  const build = bau * (1 - f) + gastro;
  const gesamt = land + build;
  let bal = land;
  let und = build;
  let zinsenBau = 0;
  let bereit = 0;
  for (let m = 1; m <= A.bauMonate; m++) {
    const i = (bal * zins) / 12;
    const b = m > 6 ? (und * A.bereitstellung) / 12 : 0;
    zinsenBau += i;
    bereit += b;
    bal += i + b + build / A.bauMonate;
    und -= build / A.bauMonate;
  }
  const kreditNachBau = bal;
  let D = bal;
  for (let m = 0; m < A.aufschubMonate; m++) D += (D * zins) / 12;
  const aufschubZinsen = D - kreditNachBau;
  const til = opts.tilgung ?? A.tilgung;
  const rate = (D * (zins + til)) / 12;
  return {
    gesamt,
    land,
    bau: bau * (1 - f),
    gastro,
    zinsenBau,
    bereit,
    aufschubZinsen,
    kredit: D,
    rate,
    zinsAnteil: (D * zins) / 12,
    tilgAnteil: (D * til) / 12,
  };
}

function cashflow(v, fin, umsatz = v.umsatz ?? A.umsatz, opts = {}) {
  const miete = v.mieteOhnePacht * (opts.mieteFaktor ?? 1) + v.pacht;
  const gastroNachPacht = umsatz * A.gastroMargeVorPacht - v.pacht;
  const ruecklagen = miete * A.ruecklagen;
  const cf = miete - ruecklagen - fin.rate + gastroNachPacht - (opts.lohn ?? A.lohn);
  return { miete, gastroNachPacht, ruecklagen, cf, hausErgebnis: miete - ruecklagen - fin.rate };
}

// Umsatz, bei dem der Cashflow nach Lohn genau 0 ist
function umsatzBreakEven(v, fin, lohn = A.lohn) {
  const miete = v.mieteOhnePacht + v.pacht;
  const need = lohn + fin.rate + miete * A.ruecklagen - miete + v.pacht;
  return need / A.gastroMargeVorPacht;
}

// Verkauf der Einheiten an Einzelne: jede Einheit mit eigenem Kredit, Preis = Selbstkosten
const MIETE_M2 = 950 / 85; // 11,18 €/m² (Annahme des Bauherrn)
const LAYOUTS = {
  A: { EG: 340, OG: 340, ST: 250, terrasse: 90, wfOG: 255, wfST: 168, buero: 0 },
  B: { EG: 540, OG: 540, ST: 420, terrasse: 120, wfOG: 415, wfST: 323, buero: 150 },
};
function teilung(L, zins = A.zinsPlan, opts = {}) {
  const c = opts.bauKostenM2 ?? A.bauKostenM2;
  const aus = opts.gastroAusbau ?? VARIANTEN.sechs.gastroAusbau;
  const f0 = finanz(VARIANTEN.sechs, 0, zins);
  const k = f0.kredit / f0.gesamt; // Zinsen in Bauzeit und Aufschub auf den Kaufpreis
  const B = L.EG + L.OG + L.ST;
  const land = (x) => (A.grundstueck * x) / B;
  const kostenOG = land(L.OG) + L.OG * c * (1 + A.bnk);
  const kostenST = land(L.ST) + (L.ST * (c - A.holzAbschlag) + L.terrasse * A.terrassePreis) * (1 + A.bnk);
  const kostenEG = land(L.EG) + L.EG * c * (1 + A.bnk) + aus;
  const rate = (kosten, eigenkapital = 0, f = 0, til = A.tilgung) => ((kosten * (1 - f) - eigenkapital) * k * (zins + til)) / 12;
  const einheit = (m2, kostenM2, miete) => {
    const kosten = m2 * kostenM2;
    const r = rate(kosten);
    const ergebnis = miete * (1 - A.ruecklagen) - r;
    const maxKredit = (miete * (1 - A.ruecklagen) * 12) / (k * (zins + A.tilgung));
    return { m2, kosten, kostenM2, kredit: kosten * k, preisFuerPlus: maxKredit / k, luecke: Math.max(0, kosten - maxKredit / k), rate: r, miete, ergebnis, ekFuerPlus: Math.max(0, kosten - maxKredit), ekProzent: Math.max(0, 1 - maxKredit / kosten), ergebnisF15: miete * (1 - A.ruecklagen) - rate(kosten, 0, 0.15) };
  };
  const g = rate(kostenEG);
  const gastroGewinn = VARIANTEN.sechs.umsatz * A.gastroMargeVorPacht - (opts.lohn ?? A.lohn);
  const bueroMiete = L.buero * 10 * (1 - A.ruecklagen);
  return {
    L, k, kostenOG, kostenST, kostenEG, BGF: B,
    ogM2: kostenOG / L.wfOG, stM2: kostenST / L.wfST,
    oG: (m2, miete) => einheit(m2, kostenOG / L.wfOG, miete ?? m2 * MIETE_M2),
    st: (m2, miete) => einheit(m2, kostenST / L.wfST, miete ?? m2 * MIETE_M2),
    gastro: { kosten: kostenEG, kredit: kostenEG * k, rate: g, gewinn: gastroGewinn, buero: bueroMiete, ergebnis: gastroGewinn + bueroMiete - g, beUmsatz: ((opts.lohn ?? A.lohn) + g - bueroMiete) / A.gastroMargeVorPacht },
    preisFuerPlusM2: (MIETE_M2 * (1 - A.ruecklagen) * 12) / (k * (zins + A.tilgung)),
  };
}

module.exports = { teilung, LAYOUTS, MIETE_M2, bauRoh, A, VARIANTEN, finanz, cashflow, umsatzBreakEven };

if (require.main === module) {
  for (const v of Object.values(VARIANTEN)) {
    console.log("==", v.name);
    for (const z of [A.zinsPlan, A.zinsAusgang]) {
      for (const f of [0, 0.05, 0.1, 0.15, 0.2, 0.25]) {
        const fin = finanz(v, f, z);
        const c = cashflow(v, fin);
        console.log(
          z, f, Math.round(fin.gesamt), Math.round(fin.kredit), Math.round(fin.rate),
          Math.round(c.cf), Math.round(umsatzBreakEven(v, fin))
        );
      }
    }
  }
}
