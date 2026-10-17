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
  lohn: 0, // Lohn des Bauherrn wird vorerst nicht gerechnet (separates Thema)
  ruecklagen: 0.1, // Anteil an Miete + Pacht
  gastroMargeVorPacht: 0.305, // Anteil vom Umsatz (12.200 € bei 40.000 €)
  umsatz: 40000,
};

const VARIANTEN = {
  sechs: {
    key: "sechs",
    name: "8 Wohnungen, große Gastro im ganzen EG, 540 m² Grundfläche",
    bgf: 1540, // EG 540 + 1. OG 540 + Staffelgeschoss 460 (Holzbau, schmale Terrasse rundum)
    gastroM2: 460, // EG 540 m² abzüglich Treppenhaus, Aufzug und Wohn-Eingang (ca. 80 m²)
    bueroM2: 0,
    wohnungen: 8,
    holzM2: 460, // Staffelgeschoss in Holzbau (Zimmerei), nur 0,8 m zurückgesetzt
    terrasseM2: 72, // schmale umlaufende Dachterrasse (ca. 0,8 m) auf dem 1. OG, zählt nicht zur BGF
    wohnflaeche: 725, // 1. OG 5 x 83 m² + Staffel 3 x 103 m²
    gastroAusbau: 150000, // Annahme des Bauherrn, einfacher Ausbau
    mieteOhnePacht: 725 * (950 / 85), // Wohnen 11,18 €/m²
    pacht: 460 * 12, // 5.520 €
    umsatz: 50000,
  },
  a: {
    key: "a",
    name: "Variante A: 340 m² Grundfläche, 6 Wohnungen, große Gastro im EG",
    bgf: 960, // EG 340 + 1. OG 340 + Staffelgeschoss 280 (Holzbau, schmale Terrasse rundum)
    gastroM2: 290,
    bueroM2: 0,
    wohnungen: 6,
    holzM2: 280, // Staffelgeschoss in Holzbau (Zimmerei)
    terrasseM2: 58, // schmale umlaufende Dachterrasse (ca. 0,8 m) auf dem 1. OG, zählt nicht zur BGF
    wohnflaeche: 444, // 1. OG 3 x 85 m² + Staffel 3 x 63 m²
    gastroAusbau: 150000, // Annahme des Bauherrn, einfacher Ausbau
    mieteOhnePacht: 6 * 950, // 5.700 € Kaltmiete
    pacht: 290 * 12, // 3.480 €
    umsatz: 50000,
  },
  b: {
    key: "b",
    name: "Variante B: 540 m² Grundfläche, Gastro + Büro im EG, OG, Staffel",
    bgf: 1540, // EG 540 + 1. OG 540 + Staffel 460 (Holzbau, schmale Terrasse rundum)
    holzM2: 460,
    terrasseM2: 72,
    gastroM2: 460,
    bueroM2: 0,
    wohnungen: 8,
    wohnflaeche: 725, // 1. OG ca. 415 m² + Staffel ca. 310 m²
    gastroAusbau: 150000,
    mieteOhnePacht: 725 * (950 / 85) , // Wohnen 11,18 €/m² + Büro 10 €/m²
    pacht: 460 * 12,
    umsatz: 50000,
  },
  c: {
    key: "c",
    name: "Variante C: 540 m² Grundfläche, 3 Vollgeschosse plus Holz-Penthouse",
    bgf: 2080, // EG 540 + 1. OG 540 + 2. OG 540 + Staffel 460 (Holzbau, schmale Terrasse rundum)
    holzM2: 460,
    terrasseM2: 72,
    gastroM2: 460,
    bueroM2: 0,
    wohnungen: 13,
    wohnflaeche: 1140, // 1. OG 415 + 2. OG 415 + Staffel 310
    gastroAusbau: 150000,
    mieteOhnePacht: 1140 * (950 / 85) ,
    pacht: 460 * 12,
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

// Umsatz, bei dem der Cashflow (ohne Lohn des Bauherrn) genau 0 ist
function umsatzBreakEven(v, fin, lohn = A.lohn) {
  const miete = v.mieteOhnePacht + v.pacht;
  const need = lohn + fin.rate + miete * A.ruecklagen - miete + v.pacht;
  return need / A.gastroMargeVorPacht;
}

// Verkauf der Einheiten an Einzelne: jede Einheit mit eigenem Kredit, Preis = Selbstkosten
const MIETE_M2 = 950 / 85; // 11,18 €/m² (Annahme des Bauherrn)
const LAYOUTS = {
  A: { EG: 340, OG: 340, ST: 280, terrasse: 58, wfOG: 255, wfST: 189, buero: 0, nOG: 3, nST: 3 },
  B: { EG: 540, OG: 540, ST: 460, terrasse: 72, wfOG: 415, wfST: 310, buero: 0, nOG: 5, nST: 3 },
  C: { EG: 540, OG: 540, OG2: 540, ST: 460, terrasse: 72, wfOG: 415, wfOG2: 415, wfST: 310, buero: 0, nOG: 10, nST: 3 },
};
function teilung(L, zins = A.zinsPlan, opts = {}) {
  const c = opts.bauKostenM2 ?? A.bauKostenM2;
  const aus = opts.gastroAusbau ?? VARIANTEN.sechs.gastroAusbau;
  const f0 = finanz(VARIANTEN.sechs, 0, zins);
  const k = f0.kredit / f0.gesamt; // Zinsen in Bauzeit und Aufschub auf den Kaufpreis
  const N = L.OG + (L.OG2 || 0), wfN = L.wfOG + (L.wfOG2 || 0);
  const B = L.EG + N + L.ST;
  const land = (x) => (A.grundstueck * x) / B;
  const kostenOG = land(N) + N * c * (1 + A.bnk);
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
    ogM2: kostenOG / wfN, stM2: kostenST / L.wfST,
    oG: (m2, miete) => einheit(m2, kostenOG / wfN, miete ?? m2 * MIETE_M2),
    st: (m2, miete) => einheit(m2, kostenST / L.wfST, miete ?? m2 * MIETE_M2),
    gastro: { kosten: kostenEG, kredit: kostenEG * k, rate: g, gewinn: gastroGewinn, buero: bueroMiete, ergebnis: gastroGewinn + bueroMiete - g, beUmsatz: ((opts.lohn ?? A.lohn) + g - bueroMiete) / A.gastroMargeVorPacht },
    preisFuerPlusM2: (MIETE_M2 * (1 - A.ruecklagen) * 12) / (k * (zins + A.tilgung)),
  };
}

// Zielplus: Verkaufspreis je Einheit so, dass der Käufer ohne Eigenkapital und ohne Tilgung genau 'plus' € im Monat übrig behält
function zielplus(L, plus = 250, zins = A.zinsPlan, opts = {}) {
  const t0 = teilung(L, zins, opts);
  const fF = opts.foerderung ?? 0; // Förderung senkt deine Selbstkosten (nicht den Käuferpreis)
  const t = Object.assign({}, t0, { oG: (m2, miete) => ({ ...t0.oG(m2, miete), kosten: t0.oG(m2, miete).kosten * (1 - fF) }), st: (m2, miete) => ({ ...t0.st(m2, miete), kosten: t0.st(m2, miete).kosten * (1 - fF) }), gastro: { ...t0.gastro, kosten: t0.gastro.kosten * (1 - fF) } });
  const til = opts.tilgungKaeufer ?? 0;
  const rate = (kosten) => (kosten * t.k * (zins + til)) / 12;
  const preisFuer = (miete) => Math.round(((miete * (1 - A.ruecklagen) - plus) * 12) / (t.k * (zins + til)));
  const einheit = (e, miete) => {
    const preis = Math.min(e.kosten, preisFuer(miete));
    return { m2: e.m2, kosten: e.kosten, preis, nachlass: e.kosten - preis, preisM2: preis / e.m2, rate: rate(preis), miete, ergebnis: miete * (1 - A.ruecklagen) - rate(preis) };
  };
  const mOG = L.wfOG / L.nOG, mST = L.wfST / L.nST;
  const og = einheit(t.oG(mOG, mOG * MIETE_M2), mOG * MIETE_M2), st = einheit(t.st(mST, mST * MIETE_M2), mST * MIETE_M2);
  const luecke = L.nOG * og.nachlass + L.nST * st.nachlass;
  const tilEG = opts.tilgungBessam ?? A.tilgung;
  const rateEG = (t.gastro.kosten * t.k * (zins + tilEG)) / 12;
  const zinsLuecke = (luecke * t.k * zins) / 12;
  const gewinn = VARIANTEN.sechs.umsatz * A.gastroMargeVorPacht - (opts.lohn ?? A.lohn);
  return { t, og, st, luecke, zinsLuecke, rateEG, bessam: gewinn - rateEG - zinsLuecke, bessamOhneLuecke: gewinn - rateEG };
}

// Verkaufsplan: Zuordnung der Wohnungen an Käufer, Preis = Selbstkosten nach Förderung, Käufer tragen Notar (2 %) und Grunderwerbsteuer (5 %, Verwandte in gerader Linie frei)
const KAEUFER = [
  { name: "Vater", typ: "OG", grest: 0 },
  { name: "Bruder", typ: "OG", grest: 0.05 },
  { name: "Du (Wohnung 1, eigene)", typ: "OG", grest: 0, eigen: true },
  { name: "Du (Wohnung 2, vermietet)", typ: "OG", grest: 0, eigen: true },
  { name: "Du (Wohnung 3, vermietet)", typ: "OG", grest: 0, eigen: true },
  { name: "Onkel 1", typ: "ST", grest: 0.05 },
  { name: "Onkel 2", typ: "ST", grest: 0.05 },
  { name: "Onkel 3", typ: "ST", grest: 0.05 },
];
function verkaufsplan(opts = {}) {
  const f = opts.foerderung ?? 0, c = opts.bauKostenM2 ?? A.bauKostenM2, til = opts.tilgung ?? 0, zins = opts.zins ?? A.zinsPlan;
  const L = LAYOUTS.B, mOG = L.wfOG / L.nOG, mST = L.wfST / L.nST;
  const t = teilung(L, zins, { bauKostenM2: c });
  const rows = KAEUFER.map((b) => {
    const e = b.typ === "OG" ? t.oG(mOG) : t.st(mST);
    const kosten = e.kosten * (1 - f);
    const einnahme0 = e.miete * (1 - A.ruecklagen);
    let preis = kosten;
    if (opts.zielPlus != null && !b.eigen) {
      const maxKredit = ((einnahme0 - opts.zielPlus) * 12) / (t.k * (zins + til) / 1);
      preis = Math.min(kosten, maxKredit / (1 + 0.02 + b.grest) / 1);
    }
    const nk = b.eigen ? 0 : preis * (0.02 + b.grest);
    const kredit = (preis + nk) * t.k;
    const rate = (kredit * (zins + til)) / 12;
    const einnahme = e.miete * (1 - A.ruecklagen);
    return { ...b, m2: e.m2, kosten, preis, nachlass: kosten - preis, nk, kredit, rate, einnahme, ergebnis: einnahme - rate };
  });
  const luecke = rows.reduce((a2, r) => a2 + r.nachlass, 0);
  const zinsLuecke = (luecke * t.k * zins) / 12;
  const rateEG = (t.gastro.kosten * (1 - f) * t.k * (zins + A.tilgung)) / 12;
  const gewinn = VARIANTEN.sechs.umsatz * A.gastroMargeVorPacht - A.lohn;
  const eigen = rows.find((r) => r.eigen);
  return { rows, k: t.k, gastro: t.gastro, luecke, zinsLuecke, rateEG, gewinn, bessam: gewinn - rateEG - zinsLuecke + rows.filter((r) => r.eigen).reduce((a2, r) => a2 + r.ergebnis, 0), eigen };
}


// KfW "Klimafreundlicher Neubau": zinsverbilligter Kredit (kein Zuschuss). Wohnteil Programm 298 (je Wohneinheit), Gastro Programm 299 (je m² Nettogrundfläche).
// Beträge und Zinsen sind Stand der Ratgeber im Oktober 2026 und müssen bei der Hausbank/KfW bestätigt werden (Quellen widersprechen sich).
const KFW = {
  jeWE: { ohneQNG: 100000, mitQNG: 150000 },
  jeM2NGF: { ohneQNG: 1500, mitQNG: 2000 },
  ngfAnteil: 0.85, // Nettogrundfläche der Gastro als Anteil der Fläche (Annahme)
  mehrkostenPct: 0.03, // Mehrkosten Effizienzhaus 40 und QNG-Nachweis in % der Baukosten (Annahme)
};
function kfw(v, { zKfW, qng, mehrPct = KFW.mehrkostenPct, zMarkt = A.zinsAusgang }) {
  const L = LAYOUTS.B;
  const nWE = L.nOG + L.nST;
  const rahmen = nWE * (qng ? KFW.jeWE.mitQNG : KFW.jeWE.ohneQNG) + v.gastroM2 * KFW.ngfAnteil * (qng ? KFW.jeM2NGF.mitQNG : KFW.jeM2NGF.ohneQNG);
  const opts = { bauKostenM2: A.bauKostenM2 * (1 + mehrPct) };
  const f0 = finanz(v, 0, zMarkt, opts);
  const anteil = Math.min(1, rahmen / f0.gesamt);
  const zMix = anteil * zKfW + (1 - anteil) * zMarkt;
  const fin = finanz(v, 0, zMix, opts);
  return { rahmen, anteil, zMix, fin, cf: cashflow(v, fin).cf, mehrkosten: f0.gesamt - finanz(v, 0, zMarkt).gesamt };
}

module.exports = { kfw, KFW, verkaufsplan, KAEUFER, zielplus, teilung, LAYOUTS, MIETE_M2, bauRoh, A, VARIANTEN, finanz, cashflow, umsatzBreakEven };

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
