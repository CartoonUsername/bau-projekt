// Eine Präsentation mit allen Nutzungsoptionen für Variante B (540 m²): Dauermiete, Airbnb/Apartments, Hotel
// Aufruf: NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_deck_optionen.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { execFileSync } = require("child_process");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");
const { A, VARIANTEN } = require("./model");
const { AIRBNB, HOTEL, airbnb, hotel, dauermiete, gastroNetto, bueroNetto, gleichauf, verkauf, mOG, mST } = require("./model_alt");

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
const a45 = airbnb(0.45), h52 = hotel(0.52), h52p = hotel(0.52, { verpachtet: true });
const gleichAirbnb = gleichauf((x) => airbnb(x).cf, dm.cf), gleichHotel = gleichauf((x) => hotel(x).cf, dm.cf);

async function deck() {
  const t = makeDeck("Neue Mitte Werlte – Baufeld 3: Nutzungsoptionen im Vergleich", "Neue-Mitte-Werlte_Baufeld3_Optionen-Dauermiete-Airbnb-Hotel.pptx");
  const { C, content, text, card, stat, hdr, cell, R, cf, border } = t;
  t.title("", "Baufeld 3: Drei Nutzungsoptionen im Vergleich", "Dauermiete, Airbnb-Apartments oder Hotel über der Gastro (540 m² Grundfläche)");
  const TAG = "Optionen";

  // ---- 2 Überblick
  { const s = content("Die drei Optionen auf einen Blick", "Für Stadt und Bank", "Variante B: 540 m² Grundfläche, 1.540 m² BGF. Die Gastro (460 m²) im ganzen EG ist in allen Optionen gleich. 3,3 % Zins, 1 % Tilgung, ohne Förderung, ohne Lohn des Bauherrn.");
    const rows = [[hdr("Option"), hdr("Einheiten"), hdr("Zusatzkosten", "right"), hdr("Rate pro Monat", "right"), hdr("Ergebnis Haus pro Monat", "right"), hdr("Aufwand")],
      [cell("1. Dauermiete", { bold: true }), cell("8 Wohnungen"), R("–"), R(eur(dm.fin.rate)), cf(dm.cf), cell("gering")],
      [cell("2. Airbnb-Apartments", { bold: true }), cell("8 Apartments (45 % Auslastung)"), R(eur(a45.einrichtung)), R(eur(a45.fin.rate)), cf(a45.cf), cell("hoch")],
      [cell("3a. Hotel, Eigenbetrieb", { bold: true }), cell(`${HOTEL.zimmer} Zimmer (52 % Auslastung)`), R(eur(h52.einrichtung)), R(eur(h52.fin.rate)), cf(h52.cf), cell("sehr hoch")],
      [cell("3b. Hotel, verpachtet", { bold: true }), cell(`${HOTEL.zimmer} Zimmer (22 % Pacht)`), R(eur(h52p.einrichtung)), R(eur(h52p.fin.rate)), cf(h52p.cf), cell("gering, Betreiber nötig")]];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [2.6, 2.9, 1.7, 1.7, 2.1, 1.13], rowH: 0.62, border, objectName: "Tabelle Optionen" });
    text(s, [
      { text: "Dauermiete ist die beste Option: das Hotel bringt bei gutem Betrieb nur ähnlich viel, bei viel mehr Aufwand.", options: { bold: true, breakLine: true } },
      { text: `Airbnb erreicht die Dauermiete erst ab ca. ${pct(gleichAirbnb)} Auslastung, das Hotel (Eigenbetrieb) ab ca. ${pct(gleichHotel)}, beides mit viel mehr Arbeit, Zusatzkredit und Risiko. Verpachtet liegt das Hotel ${eur(dm.cf - h52p.cf)} im Monat unter der Dauermiete.`, options: {} },
    ], { x: MX, y: 4.9, w: W - 2 * MX, h: 1.5, fontSize: 15, paraSpaceAfter: 8 });
  }

  // ---- 3 Option 1 Dauermiete
  { const s = content("Option 1: Dauermiete (Basis)", "Für Stadt und Bank", "Ausführliche Rechnung steht in der Hauptpräsentation (8 Wohnungen, Gastro im EG).");
    const w = (W - 2 * MX - 3 * 0.25) / 4;
    stat(s, MX, 1.5, w, "8", `Wohnungen: 5 × ${Math.round(mOG)} m² (1. OG), 3 × ${Math.round(mST)} m² (Penthouse)`);
    stat(s, MX + (w + 0.25), 1.5, w, eur(base.mieteOhnePacht), "Kaltmiete pro Monat (11,18 €/m²)", C.accent2);
    stat(s, MX + 2 * (w + 0.25), 1.5, w, eur(dm.fin.rate), "Rate pro Monat bei einem Kredit", C.accent4);
    stat(s, MX + 3 * (w + 0.25), 1.5, w, eurS(dm.cf), "Ergebnis Haus pro Monat", dm.cf >= 0 ? C.accent5 : C.accent6);
    text(s, [
      { text: "Warum die Basis stark ist", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Ein langfristiger Mieter zahlt jeden Monat gleich, es gibt keine Auslastungsschwankung und keine Möblierung im Kredit.", options: { bullet: true, breakLine: true } },
      { text: "Wohnungen lassen sich einzeln an Verwandte verkaufen (eigener Kredit je Wohnung), siehe Verkaufsfolie.", options: { bullet: true, breakLine: true } },
      { text: "Nebenkosten werden auf die Mieter umgelegt, Rücklage 10 % deckt Verwaltung und Instandhaltung.", options: { bullet: true } },
    ], { x: MX, y: 3.5, w: W - 2 * MX, h: 2.8, fontSize: 15, paraSpaceAfter: 8 });
  }

  // ---- Airbnb
  { const s = content("Option 2: Airbnb-Apartments, Konzept", "Für Stadt und Bank", "Quellen: ferienhausmiete.de, ferienwohnungen.de (Werlte, Abruf Oktober 2026), Emsland Touristik Geschäftsbericht 2016/2017.");
    const rows = [[hdr("Kennzahl"), hdr("Wert"), hdr("Aussagekraft")],
      [cell("Ferienwohnung Werlte, 3 bis 6 Gäste"), cell("ab ca. 70 bis 80 € pro Nacht"), cell("Einzelangebote, günstigste Preise")],
      [cell("Saisonspanne laut Portalen"), cell("ca. 119 bis 205 € pro Nacht"), cell("widersprüchlich, nicht belegt")],
      [cell("Auslastung Emsland (Papenburg, Lingen)"), cell("ca. 37 % (2016/2017)"), cell("fast 10 Jahre alt")],
      [cell("Angebot in Werlte"), cell("über 60 Unterkünfte auf Portalen"), cell("Konkurrenz vorhanden")],
      [cell("Unsere Annahme", { bold: true }), cell(`${eur(100)} (5 × ${Math.round(mOG)} m², 4 Gäste), ${eur(125)} (3 × ${Math.round(mST)} m², 6 Gäste), ${pct(0.45)}`, { bold: true }), cell("vorsichtig, mit Daten prüfen", { bold: true })]];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [4.2, 5.0, 2.93], rowH: 0.55, border, objectName: "Tabelle Markt Airbnb" });
    text(s, `8 Apartments mit ca. ${nf.format(a45.wfl)} m² Wohnfläche, Möblierung ${eur(AIRBNB.einrichtungM2)} je m² = ${eur(a45.einrichtung)} mehr im Kredit. Belastbare Zahlen liefern das Landesamt für Statistik Niedersachsen, Emsland Touristik und Datenanbieter wie AirDNA, die sollten wir vor einer Entscheidung abfragen.`, { x: MX, y: 5.2, w: W - 2 * MX, h: 1.0, fontSize: 13, color: C.accent4 });
  }

  { const s = content("Option 2: Airbnb, Kosten und Ergebnis", "Für Bank", "Anteile am Umsatz sind Annahmen. Plattformgebühr laut Portalen je nach Modell ca. 3 % (geteilte Provision) oder 14 bis 16 % (nur Gastgeber).");
    const k = AIRBNB.kosten;
    const rows = [[hdr("Kostenposten"), hdr("Anteil", "right")],
      [cell("Plattformgebühr (Airbnb, Booking)"), R(pct(k.plattform))],
      [cell("Reinigung und Wäsche"), R(pct(k.reinigung))],
      [cell("Strom, Wasser, Heizung, Internet"), R(pct(k.nebenkosten))],
      [cell("Verbrauchsmaterial"), R(pct(k.material))],
      [cell("Versicherung, Software, Steuerberater"), R(pct(k.versicherungSoftware))],
      [cell("Rücklage für Reparaturen und Ersatz"), R(pct(k.ruecklage))],
      [cell("Bleibt vom Umsatz", { bold: true }), R(pct(1 - a45.quote), { bold: true })]];
    s.addTable(rows, { x: MX, y: 1.5, w: 4.8, colW: [3.5, 1.3], rowH: 0.5, border, objectName: "Tabelle Kosten Airbnb" });
    const rows2 = [[hdr("Auslastung"), hdr("Netto Apartments", "right"), hdr("Ergebnis Haus", "right"), hdr("gg. Dauermiete", "right")]];
    [0.35, 0.45, 0.55, 0.65, 0.75, 0.85].forEach((x) => { const r = airbnb(x); rows2.push([cell(pct(x)), R(eur(r.netto)), cf(r.cf), R(eurS(r.cf - dm.cf))]); });
    s.addTable(rows2, { x: 5.7, y: 1.5, w: W - 5.7 - MX, colW: [1.5, 1.9, 1.9, 1.63], rowH: 0.5, border, objectName: "Tabelle Auslastung Airbnb" });
    text(s, `Rate mit Möblierung ${eur(a45.fin.rate)} statt ${eur(dm.fin.rate)}. Dein Aufwand (Gäste, Schlüssel, Preise) ist nicht bezahlt, eine Verwaltungsfirma kostet zusätzlich ca. 15 bis 25 % vom Umsatz. Gleichauf mit der Dauermiete ab ca. ${pct(gleichAirbnb)} Auslastung.`, { x: MX, y: 5.6, w: W - 2 * MX, h: 0.9, fontSize: 13, color: C.accent4 });
  }

  { const s = content("Option 2: Airbnb, Ergebnis je Preis", "Für Bank", `Bei ${pct(0.45)} Auslastung. Faktor auf unsere Annahme von ${eur(100)} und ${eur(125)} pro Nacht.`);
    const rows = [[hdr("Preis"), hdr(`${Math.round(mOG)} m², 4 Gäste`, "right"), hdr(`${Math.round(mST)} m², 6 Gäste`, "right"), hdr("Ergebnis Haus", "right"), hdr("gegenüber Dauermiete", "right")]];
    [0.8, 1.0, 1.2, 1.4].forEach((f) => { const r = airbnb(0.45, { preisFaktor: f }); rows.push([cell(f === 1 ? "Annahme" : `${f > 1 ? "+" : "−"}${Math.round(Math.abs(f - 1) * 100)} %`), R(eur(100 * f)), R(eur(125 * f)), cf(r.cf), R(eurS(r.cf - dm.cf))]); });
    s.addTable(rows, { x: MX, y: 1.5, w: 9.2, colW: [1.8, 1.8, 1.8, 1.9, 1.9], rowH: 0.55, border, objectName: "Tabelle Preis Airbnb" });
    text(s, "Der Vorteil von Airbnb liegt nur in Zeiten und Orten mit hoher Nachfrage, etwa Messen oder Monteure unter der Woche. Zahlen dafür fehlen für Werlte.", { x: MX, y: 4.9, w: 9.2, h: 1.0, fontSize: 13, color: C.accent4 });
  }

  // ---- Hotel
  { const s = content("Option 3: Hotel, Annahmen", "Für Stadt und Bank", "Alles Annahmen, es gibt keine belastbaren Hoteldaten für Werlte. Kostenanteile und Pachtquote müssen mit einem Hotelbetreiber oder DEHOGA-Zahlen geprüft werden.");
    const k = HOTEL.kosten;
    const rows = [[hdr("Annahme"), hdr("Wert", "right")],
      [cell("Zimmer (ca. 14 im 1. OG, ca. 10 in der Staffel)"), R(`${HOTEL.zimmer}`)],
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
      { text: "Zusatzkosten", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Zimmerausstattung ${eur(HOTEL.einrichtungJeZimmer)} je Zimmer = ${eur(h52.einrichtung)} mehr im Kredit.`, options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Frühstück und Synergie", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Das Frühstück läuft über die Gastro im EG. Das zusätzliche Gastro-Geschäft ist nicht eingerechnet.", options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Verpachtung", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Ein Betreiber zahlt etwa ${pct(HOTEL.pachtQuote)} vom Umsatz als Pacht (Annahme).`, options: {} },
    ], { x: 8.85, y: 1.7, w: W - 8.6 - MX - 0.5, h: 4.2, fontSize: 13 });
  }

  { const s = content("Option 3: Hotel, Ergebnis", "Für Bank", `Ergebnis des ganzen Hauses pro Monat: Gastro plus Hotel minus Rate (${eur(h52.fin.rate)}). Gleichauf mit der Dauermiete ab ca. ${pct(gleichHotel)} Auslastung (Eigenbetrieb).`);
    const rows = [[hdr("Auslastung"), hdr("Umsatz Hotel", "right"), hdr("Hotel nach Kosten", "right"), hdr("Haus: Eigenbetrieb", "right"), hdr("Pacht (22 %)", "right"), hdr("Haus: verpachtet", "right")]];
    [0.4, 0.5, 0.6, 0.7].forEach((x) => { const r = hotel(x), p = hotel(x, { verpachtet: true }); rows.push([cell(pct(x)), R(eur(r.umsatzMonat)), R(eur(r.gopMonat)), cf(r.cf), R(eur(r.pachtMonat)), cf(p.cf)]); });
    rows.push([cell("Dauermiete (Vergleich)", { bold: true }), R(""), R(eur(dm.nettoMiete)), cf(dm.cf), R(""), R("")]);
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [2.0, 1.9, 2.1, 2.2, 1.9, 2.03], rowH: 0.55, border, objectName: "Tabelle Auslastung Hotel" });
    const rows2 = [[hdr("Preis je Zimmer"), hdr("Umsatz pro Monat", "right"), hdr("Haus (52 %, Eigenbetrieb)", "right"), hdr("gegenüber Dauermiete", "right")]];
    [75, 85, 95, 105].forEach((p) => { const r = hotel(0.52, { preis: p }); rows2.push([cell(eur(p)), R(eur(r.umsatzMonat)), cf(r.cf), R(eurS(r.cf - dm.cf))]); });
    s.addTable(rows2, { x: MX, y: 4.9, w: 8.6, colW: [2.2, 2.0, 2.3, 2.1], rowH: 0.35, border, objectName: "Tabelle Preis Hotel" });
  }

  // ---- Verkauf
  { const s = content("Verkauf an die Verwandten: Optionen im Vergleich", "Für Verwandte und Bank", "Jede Einheit mit eigenem Kredit ohne Eigenkapital, 3,3 % Zins, 1 % Tilgung. Preis für +250 € im Monat: nur Zinsen. Airbnb bei 45 %, Hotel bei 52 % Auslastung, Hotel als Pachtanlage (Betreiber zahlt 22 % vom Umsatz).");
    const rows = [[hdr("Einheit"), hdr("Anzahl", "right"), hdr("Selbstkosten", "right"), hdr("Einnahme / Monat", "right"), hdr("Ergebnis", "right"), hdr("Preis für +250 €", "right"), hdr("Differenz je Einheit", "right")]];
    const add = (name, r) => r.einheiten.forEach((e) => rows.push([cell(`${name}: ${e.name}`), R(String(e.n)), R(eur(e.kosten)), R(eur(e.einnahme)), cf(e.ergebnis), R(e.preisPlus > 0 ? eur(e.preisPlus) : "nicht erreichbar"), R(eur(Math.max(0, e.kosten - e.preisPlus)))]));
    const vm = verkauf("miete", 0.45), va = verkauf("airbnb", 0.45), vh = verkauf("hotel", 0.52);
    add("Miete", vm); add("Airbnb", va); add("Hotel", vh);
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [4.0, 0.9, 1.5, 1.5, 1.3, 1.6, 1.33], rowH: 0.5, border, objectName: "Tabelle Verkauf Optionen" });
    text(s, [
      { text: `Nur bei Dauermiete liegt der Preis für +250 € nahe an den Selbstkosten, die Differenz von ${eur(vm.luecke)} trägst du (Dein Ergebnis dann ${eurS(vm.bessam)} pro Monat). Bei Airbnb wären es ${eur(va.luecke)} und beim Hotel ${eur(vh.luecke)}.`, options: { breakLine: true } },
      { text: "Möblierte Apartments und Hotelzimmer sind als Anlage für Verwandte deutlich schlechter geeignet, und eine Bank finanziert eine so hohe Differenz kaum.", options: {} },
    ], { x: MX, y: 5.35, w: W - 2 * MX, h: 1.4, fontSize: 13, color: C.accent4, paraSpaceAfter: 6 });
  }

  // ---- Recht und Risiken
  { const s = content("Recht und Risiken je Option", "Für Stadt und Bank", "Bitte mit Bauamt und Brandschutz klären, die Hinweise sind keine Rechtsberatung.");
    const items = [
      ["Sonderbau Beherbergung", `Bei mehr als 12 Gästebetten gelten meist Sonderbau-Regeln (Brandschutz, Fluchtwege). Airbnb (ca. ${AIRBNB.apartments.reduce((a, x) => a + x.n * x.gaeste, 0)} Betten) und Hotel (${HOTEL.zimmer} Zimmer) betrifft das auch für das Holz-Staffelgeschoss, Dauermiete nicht.`],
      ["Nutzung im B-Plan", "Im Mischgebiet sind Wohnen, Beherbergung und Gastro meist zulässig, die Stadt muss es für Baufeld 3 und die 540 m² Grundfläche bestätigen."],
      ["Stellplätze", "Hotelgäste und Gastro brauchen deutlich mehr Plätze als Wohnungen (ca. 0,5 bis 1 je Zimmer). Auf dem Grundstück passen nur ca. 8–10."],
      ["Betrieb und Markt", "Airbnb und Hotel sind ein zweiter Betrieb mit Personal oder Aufwand. Für Werlte fehlen belastbare Zahlen zu Preis und Auslastung."],
    ];
    items.forEach((it, i) => { const x = MX + (i % 2) * 6.2, y = 1.5 + Math.floor(i / 2) * 2.4; card(s, x, y, 5.9, 2.2, it[0]); text(s, it[0], { x: x + 0.25, y: y + 0.15, w: 5.4, h: 0.4, fontSize: 17, fontFace: "Georgia", color: C.accent1 }); text(s, it[1], { x: x + 0.25, y: y + 0.65, w: 5.4, h: 1.4, fontSize: 13 }); });
  }

  // ---- Empfehlung
  { const s = content("Empfehlung und nächste Schritte", "Für Stadt und Bank", "");
    text(s, [
      { text: "Empfehlung", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Dauermiete (${eurS(dm.cf)} pro Monat) ist die beste Option: Airbnb (${eurS(a45.cf)}) liegt klar darunter, das Hotel (${eurS(h52.cf)} bei 52 % Auslastung, Eigenbetrieb) nur gleichauf, dafür mit viel mehr Aufwand, Zusatzkredit und Brandschutzauflagen.`, options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Nächste Schritte", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Echte Preise und Auslastung für Werlte holen (LSN, Emsland Touristik, AirDNA) und Hotelbetreiber befragen.", options: { bullet: true, breakLine: true } },
      { text: "Nachfrage durch Betriebe und Monteure in der Umgebung prüfen.", options: { bullet: true, breakLine: true } },
      { text: "Brandschutz, Sonderbau und Stellplätze mit dem Bauamt klären.", options: { bullet: true } },
    ], { x: MX, y: 1.6, w: W - 2 * MX, h: 4.5, fontSize: 16, paraSpaceAfter: 8 });
  }
  await t.save();
}

deck();
