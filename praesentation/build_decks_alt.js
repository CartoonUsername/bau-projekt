// Zwei getrennte Ausarbeitungen: (1) Airbnb/Apartments statt Wohnungen, (2) Hotel über der Gastro
// Aufruf: NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_decks_alt.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { execFileSync } = require("child_process");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");
const { A, VARIANTEN } = require("./model");
const { AIRBNB, HOTEL, airbnb, hotel, dauermiete, gastroNetto } = require("./model_alt");

const IMG = process.env.BILDER || path.join(__dirname, "bilder");
const OUT = process.env.OUT || __dirname;
const THEME = {
  name: "Neue Mitte Werlte", headFontFace: "Georgia", bodyFontFace: "Arial",
  colors: { dk1: "1F2421", lt1: "FFFFFF", dk2: "2F4A3E", lt2: "F1F0EE", accent1: "8C3B32", accent2: "2F4A3E", accent3: "C49A45", accent4: "5B6770", accent5: "2E7D5B", accent6: "B3261E", hlink: "8C3B32", folHlink: "5B6770" },
};
const nf = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
const eur = (n) => `${n < 0 ? "−" : ""}${nf.format(Math.abs(Math.round(n)))} €`;
const eurS = (n) => `${n > 0 ? "+" : n < 0 ? "−" : ""}${nf.format(Math.abs(Math.round(n)))} €`;
const pct = (x) => `${Math.round(x * 100)} %`;
const W = 13.33, H = 7.5, MX = 0.6;

function fit(file, w, h) {
  const out = path.join(require("os").tmpdir(), "crop_" + path.basename(file).replace(/\W/g, "_") + "_" + Math.round(w * 100) + "x" + Math.round(h * 100) + ".jpg");
  execFileSync("python3", ["-c", "import sys\nfrom PIL import Image\nim=Image.open(sys.argv[1]).convert('RGB');W,H=im.size;r=float(sys.argv[3])/float(sys.argv[4])\nif W/H>r:\n    nw=int(H*r);x=(W-nw)//2;im=im.crop((x,0,x+nw,H))\nelse:\n    nh=int(W/r);y=(H-nh)//2;im=im.crop((0,y,W,y+nh))\nim.save(sys.argv[2],quality=92)", file, out, String(w), String(h)]);
  return out;
}

function makeDeck(title, fileName) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = title; pres.author = "Bessam Hasso";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  pres.defineSlideMaster({ title: "TITEL", background: { color: "2F4A3E" }, objects: [] });
  pres.defineSlideMaster({ title: "INHALT", background: { color: "FFFFFF" }, objects: [
    { rect: { x: MX, y: 1.2, w: 0.9, h: 0.045, fill: { color: C.accent3 }, line: { color: C.accent3, width: 0 } } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.35, w: W - 2 * MX, h: 0.9, fontFace: "Georgia", fontSize: 27, bold: false, color: C.accent1, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ], slideNumber: { x: W - 1.1, y: H - 0.45, w: 0.6, h: 0.3, fontSize: 10, color: C.accent4, align: "right" } });
  const t = {
    pres, C,
    content(titleText, tag, notes) {
      const s = pres.addSlide({ masterName: "INHALT" });
      s.addText(titleText, { placeholder: "title" });
      if (tag) s.addText(tag, { x: MX, y: H - 0.45, w: 6, h: 0.3, fontSize: 10, color: C.accent4, margin: 0, isTextBox: true, objectName: "Zielgruppe" });
      if (notes) s.addNotes(notes);
      return s;
    },
    text(s, tx, o) { s.addText(tx, Object.assign({ fontFace: "Arial", fontSize: 13, color: C.text1, margin: 0, isTextBox: true, valign: "top" }, o)); },
    card(s, x, y, w, h, name) { s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: C.background2 }, line: { color: C.background2, width: 0 }, rectRadius: 0.08, objectName: name || "Karte" }); },
    stat(s, x, y, w, big, label, color) {
      t.card(s, x, y, w, 1.55, "Kennzahl " + label);
      t.text(s, big, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.75, fontSize: 28, fontFace: "Georgia", color: color || C.accent1, valign: "middle" });
      t.text(s, label, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: 0.5, fontSize: 13, color: C.accent4 });
    },
    hdr: (x, align) => ({ text: x, options: { bold: true, color: C.background1, fill: { color: C.accent2 }, align: align || "left", fontSize: 12.5, fontFace: "Arial" } }),
    cell: (x, o) => ({ text: x, options: Object.assign({ fontSize: 12.5, fontFace: "Arial" }, o) }),
  };
  t.R = (x, o) => t.cell(x, Object.assign({ align: "right" }, o));
  t.cf = (n, o) => t.cell(eurS(n), Object.assign({ align: "right", bold: true, color: n >= 0 ? C.accent5 : C.accent6, fill: { color: n >= 0 ? "E3F1EA" : "F8E4E2" } }, o));
  t.border = { type: "solid", color: "FFFFFF", pt: 1 };
  t.title = (kicker, head, sub) => {
    const s = pres.addSlide({ masterName: "TITEL" });
    s.addImage({ path: fit(path.join(IMG, "ki_aussen_1.jpg"), 6.43, H), x: 6.9, y: 0, w: 6.43, h: H, altText: "Außenansicht" });
    t.text(s, "NEUE MITTE WERLTE", { x: MX, y: 1.3, w: 6, h: 0.4, fontSize: 15, bold: true, color: C.accent3, charSpacing: 4 });
    t.text(s, head, { x: MX, y: 1.85, w: 6, h: 2.2, fontSize: 32, fontFace: "Georgia", color: C.background1 });
    t.text(s, sub, { x: MX, y: 4.3, w: 6, h: 0.7, fontSize: 17, color: C.background1 });
    t.text(s, "Bessam Hasso, Werlte\nBebauungsplan Nr. 123, 1. Änderung (Entwurf 25.08.2026)\nStand Oktober 2026", { x: MX, y: 5.5, w: 6, h: 1.1, fontSize: 13, color: "CFD8D3" });
    return s;
  };
  t.save = async () => { const f = path.join(OUT, fileName); await pres.writeFile({ fileName: f }); await applyTheme(f, THEME); console.log("geschrieben", f); };
  return t;
}

const dm = dauermiete();
const base = VARIANTEN.sechs;

// ===================== Ausarbeitung 1: Airbnb / Apartments =====================
async function deckAirbnb() {
  const t = makeDeck("Neue Mitte Werlte – Baufeld 3: Gastro und 6 Apartments", "Neue-Mitte-Werlte_Baufeld3_Airbnb-Apartments.pptx");
  const { C, content, text, card, stat, hdr, cell, R, cf, border } = t;
  const a45 = airbnb(0.45);
  t.title("", "Baufeld 3: Große Gastro und 6 Apartments", "Kurzzeitvermietung (Airbnb) statt Dauermiete");

  { const s = content("Das Konzept auf einen Blick", "Ausarbeitung 1", "Variante A: 930 m² BGF, EG Gastro 290 m², darüber 6 möblierte Apartments, Staffel in Holzbau.");
    const w = (W - 2 * MX - 3 * 0.25) / 4;
    stat(s, MX, 1.5, w, "6", "Apartments: 3 × 85 m² (4 Gäste), 3 × 56 m² (2 Gäste)");
    stat(s, MX + (w + 0.25), 1.5, w, eur(a45.einrichtung), "Möblierung und Ausstattung, mit im Kredit");
    stat(s, MX + 2 * (w + 0.25), 1.5, w, eurS(a45.cf), `Ergebnis Haus pro Monat bei ${pct(0.45)} Auslastung`, a45.cf >= 0 ? C.accent5 : C.accent6);
    stat(s, MX + 3 * (w + 0.25), 1.5, w, eurS(dm.cf), "zum Vergleich: Dauermiete (950 € je Wohnung)", C.accent4);
    text(s, [
      { text: "Kurzzeitvermietung bringt in Werlte nicht mehr als normale Mieter.", options: { bold: true, breakLine: true } },
      { text: `Bei ${pct(0.45)} Auslastung und ${eur(100)} bzw. ${eur(85)} pro Nacht liegt das Ergebnis des Hauses ${eur(dm.cf - a45.cf)} unter der Dauermiete. Erst bei ca. ${pct(0.82)} Auslastung wäre es gleich.`, options: {} },
    ], { x: MX, y: 3.4, w: W - 2 * MX, h: 1.6, fontSize: 15, paraSpaceAfter: 8 });
  }

  { const s = content("Markt in Werlte: was wir wissen und was nicht", "Ausarbeitung 1", "Quellen: ferienhausmiete.de, ferienwohnungen.de (Werlte, Abruf Oktober 2026), Emsland Touristik Geschäftsbericht 2016/2017.");
    const rows = [[hdr("Kennzahl"), hdr("Wert"), hdr("Aussagekraft")],
      [cell("Ferienwohnung Werlte, 3 bis 6 Gäste"), cell("ab ca. 70 bis 80 € pro Nacht"), cell("Einzelangebote, günstigste Preise")],
      [cell("Saisonspanne laut Portalen"), cell("ca. 119 bis 205 € pro Nacht"), cell("widersprüchlich, nicht belegt")],
      [cell("Auslastung Emsland (Papenburg, Lingen)"), cell("ca. 37 % (2016/2017)"), cell("fast 10 Jahre alt")],
      [cell("Angebot in Werlte"), cell("über 60 Unterkünfte auf Portalen"), cell("Konkurrenz vorhanden")],
      [cell("Unsere Annahme", { bold: true }), cell(`${eur(100)} (85 m²), ${eur(85)} (56 m²), ${pct(0.45)}`, { bold: true }), cell("vorsichtig, mit Daten prüfen", { bold: true })]];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [4.6, 4.0, 3.53], rowH: 0.55, border, objectName: "Tabelle Markt Airbnb" });
    text(s, "Belastbare Zahlen liefern das Landesamt für Statistik Niedersachsen (Beherbergungsstatistik), Emsland Touristik und Datenanbieter für Kurzzeitvermietung (z. B. AirDNA). Das sollten wir vor einer Entscheidung abfragen.", { x: MX, y: 5.2, w: W - 2 * MX, h: 1.0, fontSize: 13, color: C.accent4 });
  }

  { const s = content("Kosten der Kurzzeitvermietung", "Ausarbeitung 1", "Anteile am Umsatz sind Annahmen. Plattformgebühr laut Portalen je nach Modell ca. 3 % (geteilte Provision) oder 14 bis 16 % (nur Gastgeber).");
    const k = AIRBNB.kosten;
    const rows = [[hdr("Posten"), hdr("Anteil am Umsatz", "right")],
      [cell("Plattformgebühr (Airbnb, Booking)"), R(pct(k.plattform))],
      [cell("Reinigung und Wäsche"), R(pct(k.reinigung))],
      [cell("Strom, Wasser, Heizung, Internet"), R(pct(k.nebenkosten))],
      [cell("Verbrauchsmaterial (Seife, Kaffee …)"), R(pct(k.material))],
      [cell("Versicherung, Software, Steuerberater"), R(pct(k.versicherungSoftware))],
      [cell("Rücklage für Reparaturen und Ersatz"), R(pct(k.ruecklage))],
      [cell("Summe", { bold: true }), R(pct(a45.quote), { bold: true })],
      [cell("Bleibt vom Umsatz", { bold: true }), R(pct(1 - a45.quote), { bold: true })]];
    s.addTable(rows, { x: MX, y: 1.5, w: 6.4, colW: [4.4, 2.0], rowH: 0.5, border, objectName: "Tabelle Kosten Airbnb" });
    card(s, 7.4, 1.5, W - 7.4 - MX, 4.6, "Hinweis");
    text(s, [
      { text: "Möblierung", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `ca. ${eur(AIRBNB.einrichtungM2)} je m² (Möbel, Küche, Wäsche, Technik) bei ${nf.format(a45.wfl)} m², das sind ${eur(a45.einrichtung)} mehr im Kredit.`, options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Selbstbetrieb", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Dein Aufwand (Gäste, Schlüssel, Preise) ist nicht bezahlt. Eine Verwaltungsfirma kostet zusätzlich ca. 15 bis 25 % vom Umsatz.", options: {} },
    ], { x: 7.65, y: 1.7, w: W - 7.4 - MX - 0.5, h: 4.2, fontSize: 13 });
  }

  { const s = content("Ergebnis je Auslastung", "Ausarbeitung 1", "Ergebnis des ganzen Hauses pro Monat: Gastro (ohne Lohn) plus Apartments minus Rate. Ein Kredit, 3,3 % Zins, 1 % Tilgung.");
    const rows = [[hdr("Auslastung"), hdr("Umsatz Apartments", "right"), hdr("Netto Apartments", "right"), hdr("Rate", "right"), hdr("Ergebnis Haus", "right"), hdr("gegenüber Dauermiete", "right")]];
    [0.35, 0.45, 0.55, 0.65, 0.75].forEach((x) => { const r = airbnb(x); rows.push([cell(pct(x)), R(eur(r.umsatzMonat)), R(eur(r.netto)), R(eur(r.fin.rate)), cf(r.cf), R(eurS(r.cf - dm.cf))]); });
    rows.push([cell("Dauermiete (Vergleich)", { bold: true }), R(eur(base.mieteOhnePacht)), R(eur(dm.nettoMiete)), R(eur(dm.fin.rate)), cf(dm.cf), R("")]);
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [2.2, 2.0, 2.0, 1.7, 2.0, 2.23], rowH: 0.55, border, objectName: "Tabelle Auslastung Airbnb" });
    text(s, `Ohne Einrichtungskosten läge die Rate bei ${eur(dm.fin.rate)}. Mit der Möblierung steigt sie auf ${eur(a45.fin.rate)}.`, { x: MX, y: 5.7, w: W - 2 * MX, h: 0.5, fontSize: 13, color: C.accent4 });
  }

  { const s = content("Ergebnis je Preis pro Nacht", "Ausarbeitung 1", `Bei ${pct(0.45)} Auslastung. Faktor auf unsere Annahme von 100 € und 85 € pro Nacht.`);
    const rows = [[hdr("Preis"), hdr("85 m², 4 Gäste", "right"), hdr("56 m², 2 Gäste", "right"), hdr("Ergebnis Haus", "right"), hdr("gegenüber Dauermiete", "right")]];
    [0.8, 1.0, 1.2, 1.4].forEach((f) => { const r = airbnb(0.45, { preisFaktor: f }); rows.push([cell(f === 1 ? "Annahme" : `${f > 1 ? "+" : "−"}${Math.round(Math.abs(f - 1) * 100)} %`), R(eur(100 * f)), R(eur(85 * f)), cf(r.cf), R(eurS(r.cf - dm.cf))]); });
    s.addTable(rows, { x: MX, y: 1.5, w: 9.2, colW: [1.8, 1.8, 1.8, 1.9, 1.9], rowH: 0.55, border, objectName: "Tabelle Preis Airbnb" });
    text(s, "Auch bei 40 % höheren Preisen bleibt das Ergebnis unter der Dauermiete. Der Vorteil von Airbnb liegt nur in Zeiten und Orten mit hoher Nachfrage, etwa Messen oder Monteure unter der Woche.", { x: MX, y: 4.9, w: 9.2, h: 1.0, fontSize: 13, color: C.accent4 });
  }

  { const s = content("Recht und Risiken", "Ausarbeitung 1", "Bitte mit Bauamt und Brandschutz klären, die Hinweise sind keine Rechtsberatung.");
    const items = [
      ["Beherbergungsstätte", "Bei mehr als 12 Gästebetten gelten meist Sonderbau-Regeln (Brandschutz, Fluchtwege), hier ca. 18 Betten. Das betrifft auch das Holz-Staffelgeschoss."],
      ["Nutzung im B-Plan", "Im Mischgebiet sind Beherbergung und Ferienwohnungen meist zulässig, die Stadt muss es für Baufeld 3 bestätigen."],
      ["Stellplätze", "Gäste und Gastro brauchen zusammen noch mehr Plätze als heute (Bedarf ca. 29, Platz 10–13)."],
      ["Aufwand und Steuern", "Gäste, Reinigung und Preise kosten Zeit. Einnahmen sind Gewerbe, Verkauf einzelner Apartments an Verwandte passt dazu nicht gut."],
    ];
    items.forEach((it, i) => { const x = MX + (i % 2) * 6.2, y = 1.5 + Math.floor(i / 2) * 2.4; card(s, x, y, 5.9, 2.2, it[0]); text(s, it[0], { x: x + 0.25, y: y + 0.15, w: 5.4, h: 0.4, fontSize: 17, fontFace: "Georgia", color: C.accent1 }); text(s, it[1], { x: x + 0.25, y: y + 0.65, w: 5.4, h: 1.4, fontSize: 13 }); });
  }

  { const s = content("Fazit und nächste Schritte", "Ausarbeitung 1", "");
    text(s, [
      { text: "Fazit", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Apartments sind möglich, aber im Plan ${eur(dm.cf - a45.cf)} im Monat schwächer als normale Mieter, bei mehr Arbeit und Risiko.`, options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Nächste Schritte", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Echte Preise und Auslastung für Werlte holen (LSN, Emsland Touristik, Airbnb-Daten).", options: { bullet: true, breakLine: true } },
      { text: "Nachfrage durch Betriebe und Monteure in der Umgebung prüfen.", options: { bullet: true, breakLine: true } },
      { text: "Brandschutz und Sonderbau mit dem Bauamt klären.", options: { bullet: true } },
    ], { x: MX, y: 1.6, w: W - 2 * MX, h: 4.5, fontSize: 16, paraSpaceAfter: 8 });
  }
  await t.save();
}

// ===================== Ausarbeitung 2: Hotel =====================
async function deckHotel() {
  const t = makeDeck("Neue Mitte Werlte – Baufeld 3: Gastro und Hotel", "Neue-Mitte-Werlte_Baufeld3_Hotel-und-Gastro.pptx");
  const { C, content, text, card, stat, hdr, cell, R, cf, border } = t;
  const h52 = hotel(0.52), h52p = hotel(0.52, { verpachtet: true });
  t.title("", "Baufeld 3: Hotel mit großer Gastro", "15 Zimmer über der Gastro im Erdgeschoss");

  { const s = content("Das Konzept auf einen Blick", "Ausarbeitung 2", "Variante A: 930 m² BGF, EG Gastro 290 m² mit Frühstück, 1. OG und Staffel (Holzbau) als Hotel mit 15 Zimmern.");
    const w = (W - 2 * MX - 3 * 0.25) / 4;
    stat(s, MX, 1.5, w, "15", "Zimmer: ca. 9 im 1. OG, ca. 6 in der Staffel mit Terrasse");
    stat(s, MX + (w + 0.25), 1.5, w, eur(h52.einrichtung), "Zimmerausstattung (18.000 € je Zimmer), mit im Kredit");
    stat(s, MX + 2 * (w + 0.25), 1.5, w, eurS(h52.cf), `Ergebnis Haus pro Monat bei ${pct(0.52)} Auslastung, Eigenbetrieb`, h52.cf >= 0 ? C.accent5 : C.accent6);
    stat(s, MX + 3 * (w + 0.25), 1.5, w, eurS(dm.cf), "zum Vergleich: Dauermiete (950 € je Wohnung)", C.accent4);
    text(s, [
      { text: "Das Hotel bringt bei guter Auslastung etwa so viel wie Dauermiete, mit viel mehr Arbeit.", options: { bold: true, breakLine: true } },
      { text: `Bei ${pct(0.52)} Auslastung und ${eur(HOTEL.preis)} pro Zimmer liegt der Eigenbetrieb ${eur(Math.abs(dm.cf - h52.cf))} ${dm.cf > h52.cf ? "unter" : "über"} der Dauermiete, verpachtet ${eur(dm.cf - h52p.cf)} darunter.`, options: {} },
    ], { x: MX, y: 3.4, w: W - 2 * MX, h: 1.6, fontSize: 15, paraSpaceAfter: 8 });
  }

  { const s = content("Annahmen für das Hotel", "Ausarbeitung 2", "Alles Annahmen, es gibt keine belastbaren Hoteldaten für Werlte. Pachtquote und Kostenanteile sind Richtwerte und müssen mit einem Hotelbetreiber oder DEHOGA-Zahlen geprüft werden.");
    const k = HOTEL.kosten;
    const rows = [[hdr("Annahme"), hdr("Wert", "right")],
      [cell("Zimmer / BGF je Zimmer"), R(`${HOTEL.zimmer} / ca. 38 m²`)],
      [cell("Preis pro Zimmer und Nacht inkl. Frühstück"), R(eur(HOTEL.preis))],
      [cell("Personal"), R(pct(k.personal))],
      [cell("Frühstück und Wareneinsatz"), R(pct(k.fruehstueck))],
      [cell("Energie"), R(pct(k.energie))],
      [cell("Reinigung und Wäsche"), R(pct(k.reinigungWaesche))],
      [cell("Vertrieb und Provisionen (Booking u. a.)"), R(pct(k.vertrieb))],
      [cell("Verwaltung, Versicherung, Sonstiges"), R(pct(k.verwaltungSonst))],
      [cell("Bleibt vom Umsatz (vor Rate)", { bold: true }), R(pct(1 - h52.quote), { bold: true })]];
    s.addTable(rows, { x: MX, y: 1.5, w: 7.6, colW: [5.2, 2.4], rowH: 0.45, border, objectName: "Tabelle Annahmen Hotel" });
    card(s, 8.6, 1.5, W - 8.6 - MX, 4.6, "Hinweis");
    text(s, [
      { text: "Frühstück und Synergie", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Das Frühstück läuft über die Gastro im EG, Hotelgäste können dort auch abends essen. Das zusätzliche Gastro-Geschäft ist nicht eingerechnet.", options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Verpachtung", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Ein Betreiber zahlt etwa ${pct(HOTEL.pachtQuote)} vom Umsatz als Pacht (Annahme).`, options: {} },
    ], { x: 8.85, y: 1.7, w: W - 8.6 - MX - 0.5, h: 4.2, fontSize: 13 });
  }

  { const s = content("Ergebnis je Auslastung", "Ausarbeitung 2", `Ergebnis des ganzen Hauses pro Monat: Gastro (ohne Lohn) plus Hotel minus Rate (${eur(h52.fin.rate)}). Ein Kredit, 3,3 % Zins, 1 % Tilgung.`);
    const rows = [[hdr("Auslastung"), hdr("Umsatz Hotel", "right"), hdr("Hotel nach Kosten", "right"), hdr("Haus: Eigenbetrieb", "right"), hdr("Pacht (22 %)", "right"), hdr("Haus: verpachtet", "right")]];
    [0.4, 0.5, 0.6, 0.7].forEach((x) => { const r = hotel(x), p = hotel(x, { verpachtet: true }); rows.push([cell(pct(x)), R(eur(r.umsatzMonat)), R(eur(r.gopMonat)), cf(r.cf), R(eur(r.pachtMonat)), cf(p.cf)]); });
    rows.push([cell("Dauermiete (Vergleich)", { bold: true }), R(""), R(eur(dm.nettoMiete)), cf(dm.cf), R(""), R("")]);
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [2.0, 1.9, 2.1, 2.2, 1.9, 2.03], rowH: 0.55, border, objectName: "Tabelle Auslastung Hotel" });
  }

  { const s = content("Ergebnis je Preis pro Zimmer", "Ausarbeitung 2", `Bei ${pct(0.52)} Auslastung, Eigenbetrieb.`);
    const rows = [[hdr("Preis je Zimmer"), hdr("Umsatz pro Monat", "right"), hdr("Haus pro Monat", "right"), hdr("gegenüber Dauermiete", "right")]];
    [75, 85, 95, 105].forEach((p) => { const r = hotel(0.52, { preis: p }); rows.push([cell(eur(p)), R(eur(r.umsatzMonat)), cf(r.cf), R(eurS(r.cf - dm.cf))]); });
    s.addTable(rows, { x: MX, y: 1.5, w: 8.6, colW: [2.4, 2.1, 2.0, 2.1], rowH: 0.55, border, objectName: "Tabelle Preis Hotel" });
  }

  { const s = content("Die drei Konzepte im Vergleich", "Ausarbeitung 2", "Variante A, 3,3 % Zins, ohne Lohn des Bauherrn. Airbnb bei 45 %, Hotel bei 52 % Auslastung.");
    const a45 = airbnb(0.45);
    const rows = [[hdr("Konzept"), hdr("Zusatzkosten", "right"), hdr("Rate", "right"), hdr("Ergebnis Haus", "right"), hdr("Aufwand")],
      [cell("Dauermiete (6 Wohnungen)"), R("–"), R(eur(dm.fin.rate)), cf(dm.cf), cell("gering")],
      [cell("Airbnb (6 Apartments)"), R(eur(a45.einrichtung)), R(eur(a45.fin.rate)), cf(a45.cf), cell("hoch (Gäste, Reinigung)")],
      [cell("Hotel, Eigenbetrieb (15 Zimmer)"), R(eur(h52.einrichtung)), R(eur(h52.fin.rate)), cf(h52.cf), cell("sehr hoch (Personal, 24 Stunden)")],
      [cell("Hotel, verpachtet"), R(eur(h52.einrichtung)), R(eur(h52p.fin.rate)), cf(h52p.cf), cell("gering, Betreiber nötig")]];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.8, 1.9, 1.7, 2.0, 2.73], rowH: 0.65, border, objectName: "Tabelle Vergleich Konzepte" });
  }

  { const s = content("Recht und Risiken", "Ausarbeitung 2", "Bitte mit Bauamt und Brandschutz klären, die Hinweise sind keine Rechtsberatung.");
    const items = [
      ["Sonderbau Beherbergung", "Ein Hotel mit 15 Zimmern gilt als Beherbergungsstätte mit strengen Brandschutz- und Fluchtwegauflagen, auch für das Holz-Staffelgeschoss."],
      ["Betrieb und Personal", "Rezeption, Reinigung, Frühstück: Das ist ein zweiter Betrieb neben der Gastro, ohne Erfahrung oder Partner schwer."],
      ["Stellplätze und Lärm", "Hotelgäste brauchen zusätzliche Stellplätze (ca. 0,5 bis 1 je Zimmer), und Gastro und Zimmer liegen übereinander."],
      ["Markt", "Es gibt keine belastbaren Zahlen zur Nachfrage in Werlte. Vor einer Entscheidung sind Betreiber-Gespräche und Marktdaten nötig."],
    ];
    items.forEach((it, i) => { const x = MX + (i % 2) * 6.2, y = 1.5 + Math.floor(i / 2) * 2.4; card(s, x, y, 5.9, 2.2, it[0]); text(s, it[0], { x: x + 0.25, y: y + 0.15, w: 5.4, h: 0.4, fontSize: 17, fontFace: "Georgia", color: C.accent1 }); text(s, it[1], { x: x + 0.25, y: y + 0.65, w: 5.4, h: 1.4, fontSize: 13 }); });
  }

  { const s = content("Fazit und nächste Schritte", "Ausarbeitung 2", "");
    text(s, [
      { text: "Fazit", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Ein Hotel schlägt Dauermiete nur ab etwa ${pct(0.57)} Auslastung und mit viel Aufwand. Verpachtet liegt es dauerhaft unter der Dauermiete.`, options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Nächste Schritte", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Hotelbetreiber oder Hotelberater für Werlte befragen (Preis, Auslastung, Pacht).", options: { bullet: true, breakLine: true } },
      { text: "Beherbergungsstatistik (LSN) und Emsland Touristik anfragen.", options: { bullet: true, breakLine: true } },
      { text: "Brandschutz und Stellplätze mit dem Bauamt klären.", options: { bullet: true } },
    ], { x: MX, y: 1.6, w: W - 2 * MX, h: 4.5, fontSize: 16, paraSpaceAfter: 8 });
  }
  await t.save();
}

(async () => { await deckAirbnb(); await deckHotel(); })();
