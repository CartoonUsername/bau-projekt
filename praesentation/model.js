// Rechenmodell Baufeld 3 – Neue Mitte Werlte (Variante B, 960 m² BGF)
// Alle Annahmen stehen hier an einer Stelle; build_deck.js liest nur von hier.

const A = {
  grundstueck: 236256, // 960 m² x 230 € + 5 % GrESt + ca. 2 % Notar/Grundbuch
  bgf: 960,
  bauKostenM2: 2700,
  bnk: 0.15,
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

function finanz(v, foerderung, zins, opts = {}) {
  const f = foerderung;
  const land = (opts.grundstueck ?? A.grundstueck) * (1 - f);
  const bauKosten = A.bgf * A.bauKostenM2;
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
  const rate = (D * (zins + A.tilgung)) / 12;
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
    tilgAnteil: (D * A.tilgung) / 12,
  };
}

function cashflow(v, fin, umsatz = A.umsatz) {
  const miete = v.mieteOhnePacht + v.pacht;
  const gastroNachPacht = umsatz * A.gastroMargeVorPacht - v.pacht;
  const ruecklagen = miete * A.ruecklagen;
  const cf = miete - ruecklagen - fin.rate + gastroNachPacht - A.lohn;
  return { miete, gastroNachPacht, ruecklagen, cf, hausErgebnis: miete - ruecklagen - fin.rate };
}

// Umsatz, bei dem der Cashflow nach Lohn genau 0 ist
function umsatzBreakEven(v, fin) {
  const miete = v.mieteOhnePacht + v.pacht;
  const need = A.lohn + fin.rate + miete * A.ruecklagen - miete + v.pacht;
  return need / A.gastroMargeVorPacht;
}

module.exports = { A, VARIANTEN, finanz, cashflow, umsatzBreakEven };

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
