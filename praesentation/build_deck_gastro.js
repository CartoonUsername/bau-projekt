// Gastro-Konzept und Gestaltung (EG: ca. 510 m², ca. 190 Plätze)
// Aufruf: NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_deck_gastro.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { execFileSync } = require("child_process");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");
const { A, VARIANTEN, umsatzBreakEven } = require("./model");
const { teilung, LAYOUTS, finanz, cashflow } = require("./model");

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

const v = VARIANTEN.sechs;
const BV = JSON.parse(require("fs").readFileSync(path.join(__dirname, "bank_values.json"), "utf8"));
const UM = BV.g_umsatz_monat;
const img = (n) => path.join(IMG, n);

// Umsatzaufbau nach Tagesteilen aus der Excel (Blatt Gastro Tagesteile): Name, Zeit, Tage/Monat, Gäste/Tag, Ø Bon, Umsatz, Anteil
const SEG = BV.tagesteile.map((t) => [t[0] + " (" + t[1] + ")", t[2], t[3], t[4]]);
const segSumme = BV.tagesteile.reduce((a, t) => a + t[5], 0);
const gaesteMonat = BV.tagesteile.reduce((a, t) => a + t[2] * t[3], 0);

async function deck() {
  const t = makeDeck("Neue Mitte Werlte – Baufeld 3: Gastro, Gestaltung und Konzept", "Neue-Mitte-Werlte_Baufeld3_Gastro-Konzept.pptx");
  const { C, content, text, card, hdr, cell, R, cf, border } = t;
  const pres = t.pres;

  // ---- 1 Titel
  { const s = pres.addSlide({ masterName: "TITEL" });
    s.addImage({ path: fit(img("ki_gastro_raum.jpg"), 6.43, H), x: 6.9, y: 0, w: 6.43, h: H, altText: "Gastraum mit Vertäfelung, Cognac-Banketten und Bar" });
    text(s, "NEUE MITTE WERLTE", { x: MX, y: 1.3, w: 6, h: 0.4, fontSize: 15, bold: true, color: C.accent3, charSpacing: 4 });
    text(s, "Gastro im Erdgeschoss: Gestaltung und Konzept", { x: MX, y: 1.85, w: 6, h: 2.2, fontSize: 32, fontFace: "Georgia", color: C.background1 });
    text(s, "Frühstück, Bowls und Bar für den ganzen Tag, ca. 510 m² im ganzen EG", { x: MX, y: 4.3, w: 6, h: 0.7, fontSize: 17, color: C.background1 });
    text(s, "Bessam Hasso, Werlte\nBaufeld 3, Bebauungsplan Nr. 123, 1. Änderung\nStand Oktober 2026", { x: MX, y: 5.5, w: 6, h: 1.1, fontSize: 13, color: "CFD8D3" });
  }

  // ---- 2 Idee
  { const s = content("Die Idee: ein Ort für den ganzen Tag", "Für Stadt und Bank", "Alle Zahlen zu Plätzen, Preisen und Gästen sind Planungsannahmen, noch kein Betreiberkonzept.");
    const cols = [
      ["Morgens und mittags", "Frühstück, Brunch am Wochenende und Bowls, Salate und Suppe zum Mittag. Frisch, schnell, fair im Preis für Beschäftigte aus Rathaus und Umgebung."],
      ["Abends: Bar mit Snacks", "Bar mit Snacks in warmer, dunkler Atmosphäre mit Cognac-Banketten und Kerzenlicht, keine große Restaurantküche. Der Abend bringt ca. " + Math.round(BV.g_abend_anteil * 100) + " % vom Umsatz."],
      ["Cocktails und Events", "Cocktails, Wein und Bier an der großen Theke, Fr und Sa bis 01 Uhr. Live-Musik, Séparée mit 30 Plätzen für Feiern."],
    ];
    const cw = (W - 2 * MX - 0.6) / 3;
    cols.forEach((c, i) => { const x = MX + i * (cw + 0.3); card(s, x, 1.5, cw, 2.3, c[0]); text(s, c[0], { x: x + 0.25, y: 1.65, w: cw - 0.5, h: 0.45, fontSize: 20, fontFace: "Georgia", color: C.accent1 }); text(s, c[1], { x: x + 0.25, y: 2.25, w: cw - 0.5, h: 1.5, fontSize: 14 }); });
    const k = [["ca. 510 m²", "Gastro im ganzen EG"], ["ca. 190", "Plätze innen (160 Gastraum, 30 Séparée)"], ["ca. 60", "Plätze auf der Terrasse"], ["12", "Barhocker an der Theke"]];
    const w = (W - 2 * MX - 0.9) / 4;
    k.forEach((it, i) => { const x = MX + i * (w + 0.3); card(s, x, 4.2, w, 1.5, "Kennzahl " + it[1]); text(s, it[0], { x: x + 0.2, y: 4.3, w: w - 0.4, h: 0.7, fontSize: 28, fontFace: "Georgia", color: C.accent2, valign: "middle" }); text(s, it[1], { x: x + 0.2, y: 5.0, w: w - 0.4, h: 0.6, fontSize: 13, color: C.accent4 }); });
    text(s, "Arbeitstitel: Café und Bar am Marktplatz. Ein Name und eine Marke sind noch offen.", { x: MX, y: 6.0, w: W - 2 * MX, h: 0.4, fontSize: 13, color: C.accent4 });
  }

  // ---- 3 Gäste und Lage
  { const s = content("Wer kommt und warum hier", "Für Stadt und Bank", "Zielgruppen sind Annahmen, es gibt keine Marktstudie für Werlte. Eine Betreiber- und Wettbewerbsanalyse steht noch aus.");
    const rows = [[hdr("Zielgruppe"), hdr("Wann"), hdr("Was sie suchen")],
      [cell("Beschäftigte aus Rathaus und Umgebung"), cell("Mittag, Di–Fr"), cell("schnell, frisch, fair im Preis")],
      [cell("Familien und Senioren"), cell("Brunch am Wochenende"), cell("Platz, Frühstück, Kaffee und Kuchen")],
      [cell("Paare und Freunde"), cell("Abend"), cell("gemütlich essen und trinken am Marktplatz")],
      [cell("Vereine, Firmen, Familienfeiern"), cell("nach Absprache"), cell("Séparée mit Menü, Getränkepaket")],
      [cell("Radtouristen und Besucher aus dem Hümmling"), cell("Sommer, Wochenende"), cell("Terrasse, Kaffee, Bowls")]];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [4.6, 3.1, 4.43], rowH: 0.55, border, objectName: "Tabelle Zielgruppen" });
    card(s, MX, 5.1, W - 2 * MX, 1.3, "Lage");
    text(s, [{ text: "Lage: ", options: { bold: true, color: C.accent1 } }, { text: "am neuen Marktplatz neben dem Rathaus, ab Ende 2028 mit der neuen Mitte fertig. Die Terrasse zum Platz und die vollverglaste Fassade machen die Gastro von außen sichtbar." }], { x: MX + 0.25, y: 5.2, w: W - 2 * MX - 0.5, h: 1.1, fontSize: 15, valign: "middle" });
  }

  // ---- 4 Tagesablauf und Öffnungszeiten
  { const s = content("Ein Tag in der Gastro", "Für Stadt und Bank", "Vorschlag für Öffnungszeiten, Ruhetag Montag. Hauptfokus ist der Abend an der Bar. Snacks bis kurz vor Schluss.");
    const rows = [[hdr("Zeit"), hdr("Angebot"), hdr("Stimmung")],
      [cell("08:00–11:00 (Di–Fr), 09:00–14:00 (Sa, So)"), cell("Frühstück, am Wochenende Brunch, Kaffee"), cell("hell, entspannt, Familien")],
      [cell("11:30–14:30 (Di–Fr)"), cell("Bowls, Salate, Suppe des Tages"), cell("schnell, Tische für zwei und vier")],
      [cell("14:30–17:00"), cell("Kaffee, Kuchen, kleine Snacks"), cell("ruhig, Terrasse im Sommer")],
      [cell("ab 17:00 (Di–Do, So bis 22:00)"), cell("Bar mit Snacks, Wein, Bier, Cocktails"), cell("Kerzenlicht, Banketten, Hauptgeschäft")],
      [cell("Fr, Sa bis 01:00"), cell("Bar, Cocktails, Snacks, Live-Musik"), cell("Theke, Lounge, Séparée")]];
    s.addTable(rows, { x: MX, y: 1.5, w: 7.0, colW: [2.4, 2.5, 2.1], rowH: 0.62, border, objectName: "Tabelle Tagesablauf" });
    s.addImage({ path: fit(img("ki_gastro_fruehstueck.jpg"), 4.9, 3.3), x: W - MX - 4.9, y: 1.5, w: 4.9, h: 3.3, altText: "Frühstück am Fenster" });
    text(s, "Frühstück und Brunch am Morgen", { x: W - MX - 4.9, y: 4.85, w: 4.9, h: 0.3, fontSize: 12, color: C.accent4 });
  }

  // ---- 5 Speisen und Getränke
  { const s = content("Speisen und Getränke (Beispielkarte)", "Für Stadt und Bank", "Gerichte und Preise sind Beispiele für die Kalkulation, kein fertiges Konzept. Küche: regional und modern, kurze Karte, frische Zutaten.");
    const cols = [
      ["Frühstück und Brunch", ["Frühstücksteller 12,90 €", "Avocado-Toast mit Ei 10,90 €", "Pancakes mit Früchten 9,90 €", "Brunch am Sonntag 22,90 €"]],
      ["Bowls und Mittag", ["Bowl mit Huhn und Gemüse 12,90 €", "Vegane Bowl 11,90 €", "Salat mit Topping 10,90 €", "Suppe des Tages 6,50 €"]],
      ["Snacks zur Bar", ["Nachos mit Dip 8,90 €", "Käse- und Wurstplatte 14,90 €", "Flammkuchen 11,90 €", "Bruschetta 7,90 €", "Chicken Wings 9,90 €", "Süßkartoffel-Pommes 6,90 €"]],
      ["Bar und Getränke", ["Cocktails 9,90–12,90 €", "Wein 0,2 l ab 6,50 €", "Bier vom Fass 0,3 l 3,90 €", "Kaffee 3,20 €", "Alkoholfreie Cocktails 6,90 €"]],
    ];
    const cw = (W - 2 * MX - 0.9) / 4;
    cols.forEach((c, i) => { const x = MX + i * (cw + 0.3); card(s, x, 1.5, cw, 4.0, c[0]); text(s, c[0], { x: x + 0.2, y: 1.62, w: cw - 0.4, h: 0.5, fontSize: 17, fontFace: "Georgia", color: C.accent1 }); text(s, c[1].map((t2, j) => ({ text: t2, options: { bullet: true, breakLine: j < c[1].length - 1 } })), { x: x + 0.2, y: 2.2, w: cw - 0.4, h: 3.2, fontSize: 13, paraSpaceAfter: 6 }); });
    text(s, "Durchschnittlicher Bon (Annahme): Frühstück 11 €, Brunch 14 €, Bowls 13 €, Kaffee 7 €, Bar mit Snacks 20–26 €, Events 40 €.", { x: MX, y: 5.8, w: W - 2 * MX, h: 0.4, fontSize: 14, color: C.accent2, bold: true });
  }

  // ---- 5b Abend und Bar
  { const s = content("Hauptfokus Abend: Bar mit Snacks", "Für Stadt und Bank", "Konzeptideen und Zahlen sind Annahmen, keine Betreiberplanung. Der Abend bringt den größten Teil des Umsatzes.");
    const ab = BV.tagesteile.slice(4);
    const abSum = ab.reduce((a, t) => a + t[5], 0);
    s.addImage({ path: fit(img("ki_gastro_bar.jpg"), 4.6, 3.0), x: MX, y: 1.5, w: 4.6, h: 3.0, altText: "Bar am Abend mit beleuchteter Backbar" });
    text(s, [
      { text: "Snacks (kleine Küche)", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Kurze Snackkarte: Platten, Flammkuchen, Nachos, Wings, Bruschetta", options: { bullet: true, breakLine: true } },
      { text: "Gäste teilen und bleiben, dadurch mehr Getränkeumsatz", options: { bullet: true, breakLine: true } },
      { text: "Bar (ab 17:00, Fr und Sa bis 01:00)", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Signature-Cocktails, regionale Weine, Craft-Bier vom Fass, alkoholfreie Drinks", options: { bullet: true, breakLine: true } },
      { text: "After-Work am Donnerstag, Live-Musik oder DJ am Freitag", options: { bullet: true, breakLine: true } },
      { text: "Feiern und Events", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Séparée, Themenabende, Firmen- und Vereinsfeiern, Weihnachtsfeiern", options: { bullet: true } },
    ], { x: 5.5, y: 1.5, w: W - 5.5 - MX, h: 3.4, fontSize: 13, paraSpaceAfter: 3 });
    const rows = [[hdr("Abend-Bereich"), hdr("Tage", "right"), hdr("Gäste/Tag", "right"), hdr("Ø Bon", "right"), hdr("Umsatz/Monat", "right")]];
    ab.forEach((t) => rows.push([cell(t[0]), R(String(t[2])), R(String(t[3])), R(eur(t[4])), R(eur(t[5]))]));
    rows.push([cell("Summe Abend", { bold: true }), R(""), R(""), R(""), R(eur(abSum), { bold: true })]);
    s.addTable(rows, { x: MX, y: 4.65, w: 8.2, colW: [3.8, 0.9, 1.1, 1.0, 1.4], rowH: 0.27, fontSize: 11, border, objectName: "Tabelle Abend" });
    text(s, `${Math.round(BV.g_abend_anteil * 100)} % vom Gastro-Umsatz`, { x: 9.0, y: 5.1, w: W - 9.0 - MX, h: 0.8, fontSize: 24, fontFace: "Georgia", color: C.accent2, valign: "middle" });
  }

  // ---- 6 Grundriss
  { const s = content("Raumkonzept: Grundriss der Gastro", "Für Stadt und Bank", "Schematische Skizze, nicht maßstäblich genau. Aufteilung wird mit Gastro-Fachplaner und Architekt verfeinert. Süden liegt unten.");
    const sc = 0.19, x0 = MX, y0 = 1.5;
    const PX = (x) => x0 + x * sc, PY = (y, h) => y0 + (18 - y - h) * sc + 0.0;
    const rect = (x, y, w, h, fill, name, label, o = {}) => {
      s.addShape(pres.ShapeType.rect, { x: PX(x), y: PY(y, h), w: w * sc, h: h * sc, fill: { color: fill }, line: { color: o.line || "FFFFFF", width: o.lw ?? 1, dashType: o.dash }, objectName: name });
      if (label) text(s, label, { x: PX(x), y: PY(y, h), w: w * sc, h: h * sc, fontSize: o.fs || 10, bold: true, color: o.color || "FFFFFF", align: "center", valign: "middle" });
    };
    rect(0, 0, 28, 18, "F2D48C", "Gastro EG", "", { line: "5B6770", lw: 1.5 });
    rect(3, -2.8, 25, 2.8, "D6B98F", "Terrasse", "Terrasse, ca. 60 Plätze", { color: "1F2421", dash: "dash", line: "5B6770" });
    rect(1.2, 0, 2.6, 1.4, "3A3F44", "Eingang", "Eingang", { fs: 9 });
    for (let r = 0; r < 5; r++) for (let c = 0; c < 5; c++) rect(3.0 + c * 3.9, 2.6 + r * 1.75, 1.7, 0.95, "8A6A45", "Tisch " + (r * 5 + c + 1), "", { lw: 0.5 });
    for (let c = 0; c < 8; c++) rect(2.4 + c * 2.7, 0.55, 0.8, 0.8, "A8723F", "Fenstertisch " + (c + 1), "", { lw: 0.5 });
    rect(22.8, 2, 4.8, 8.4, "B07A4A", "Lounge", "Lounge\n20 Plätze", { fs: 10 });
    rect(8, 11.3, 13, 1.4, "3A3F44", "Bar", "Bar, 12 Barhocker", { fs: 10 });
    rect(8, 13.1, 13, 0.55, "5B4B3A", "Backbar", "", {});
    rect(0.4, 12.5, 7.2, 5.1, "7A5C3A", "Séparée", "Séparée\n30 Plätze\nStahl-Glas-Wand", { fs: 10 });
    rect(8.4, 14.2, 6.4, 3.4, "7E8A94", "Küche", "Küche", { fs: 11 });
    rect(14.9, 14.2, 4.6, 3.4, "A6ADB4", "Lager und Kühlung", "Lager,\nKühlung", { fs: 10 });
    rect(19.6, 14.2, 8, 3.4, "8A9199", "WC", "WC (H, D, barrierefrei)", { fs: 10 });
    const rows = [[hdr("Zone"), hdr("Fläche", "right"), hdr("Plätze", "right")],
      [cell("Gastraum (Tische, Fenster, Gänge)"), R("ca. 304 m²"), R("116")],
      [cell("Lounge in der Ecke"), R("im Gastraum"), R("20")],
      [cell("Große Bar und Theken-Zone"), R("ca. 45 m²"), R("12")],
      [cell("Stehtische an der Bar"), R("im Gastraum"), R("12")],
      [cell("Séparée"), R("ca. 42 m²"), R("30")],
      [cell("Kleine Küche, Lager, WC, Eingang"), R("ca. 119 m²"), R("–")],
      [cell("Summe Gastro", { bold: true }), R("ca. 510 m²", { bold: true }), R("ca. 190", { bold: true })]];
    s.addTable(rows, { x: 6.45, y: 1.5, w: W - 6.45 - MX, colW: [3.1, 1.6, 1.58], rowH: 0.44, border, objectName: "Tabelle Zonen" });
    text(s, "Treppenhaus und Aufzug zu den Wohnungen liegen am Westende des Hauses und sind von der Gastro getrennt.", { x: 6.45, y: 5.6, w: W - 6.45 - MX, h: 0.7, fontSize: 12.5, color: C.accent4 });
  }

  // ---- 7 Gestaltung: Material und Farben
  { const s = content("Gestaltung: warm, dunkel, hochwertig", "Für Stadt und Bank", "Stimmung nach dem Referenzbild des Bauherrn: olivgrüne Wände mit Vertäfelung, Cognac-Samt, schwarzer Stahl und warmes Licht.");
    const sw = [["Olivgrün", "3D4638", "Wände mit Vertäfelung"], ["Cognac", "A9692F", "Samt-Banketten"], ["Bordeaux", "6B1E2E", "Kissen, Akzentlampe"], ["Eiche", "B88652", "Tische, Theke oben"], ["Anthrazit", "2B2E31", "Theke, geriffelte Front"], ["Messing", "B08D57", "Lampen, Details"], ["Creme", "E8DCC4", "Pampas, Textilien"], ["Schwarzstahl", "1E2326", "Glaswand mit Raster"]];
    sw.forEach((c, i) => { const x = MX + (i % 4) * 1.95, y = 1.5 + Math.floor(i / 4) * 1.55; s.addShape(pres.ShapeType.rect, { x, y, w: 1.75, h: 0.8, fill: { color: c[1] }, line: { color: "D9D9D9", width: 0.5 }, objectName: "Farbe " + c[0] }); text(s, c[0], { x, y: y + 0.85, w: 1.75, h: 0.3, fontSize: 12.5, bold: true }); text(s, c[2], { x, y: y + 1.12, w: 1.75, h: 0.3, fontSize: 11, color: C.accent4 }); });
    text(s, [
      { text: "Licht: ", options: { bold: true, color: C.accent1 } }, { text: "indirekte Voutenbeleuchtung an der Decke, Glaspendel mit Messing, geriffelte Tischlichter mit Kerze.", options: { breakLine: true } },
      { text: "Boden und Akustik: ", options: { bold: true, color: C.accent1 } }, { text: "Betonoptik oder Mikrozement, Akustikdecke und Textilien gegen Lärm.", options: { breakLine: true } },
      { text: "Details: ", options: { bold: true, color: C.accent1 } }, { text: "ovale und Bogen-Spiegel, Pampasgras als Wandobjekt, Stahl-Glas-Trennwand zum Séparée.", options: {} },
    ], { x: MX, y: 4.8, w: 7.9, h: 1.9, fontSize: 13, paraSpaceAfter: 6 });
    s.addImage({ path: fit(img("ki_gastro_bar.jpg"), 3.6, 4.9), x: W - MX - 3.6, y: 1.5, w: 3.6, h: 4.9, altText: "Bar mit anthrazitfarbener geriffelter Front" });
  }

  // ---- 8 Bilder Gastraum und Bar
  { const s = content("So kann es aussehen: Gastraum und Bar", "Für Stadt und Bank", "KI-Visualisierungen zur Orientierung, keine Planung.");
    const gw = (W - 2 * MX - 0.3) / 2, gh = gw * 0.5625;
    s.addImage({ path: fit(img("ki_gastro_raum.jpg"), gw, gh), x: MX, y: 1.5, w: gw, h: gh, altText: "Gastraum am Abend" });
    s.addImage({ path: fit(img("ki_gastro_separee.jpg"), gw, gh), x: MX + gw + 0.3, y: 1.5, w: gw, h: gh, altText: "Séparée mit Stahl-Glas-Wand" });
    text(s, "Gastraum am Abend: Banketten, Glaswand, Bar im Hintergrund", { x: MX, y: 1.5 + gh + 0.05, w: gw, h: 0.3, fontSize: 12, color: C.accent4 });
    text(s, "Séparée für Feiern mit 30 Plätzen, hinter Stahl und Glas", { x: MX + gw + 0.3, y: 1.5 + gh + 0.05, w: gw, h: 0.3, fontSize: 12, color: C.accent4 });
  }

  // ---- 9 Terrasse und Außen
  { const s = content("Terrasse und Außenwirkung", "Für Stadt und Bank", "Terrasse mit Vordach zum Marktplatz. Nutzungszeiten und Lärmschutz mit der Stadt abstimmen.");
    const gw = 6.0, gh = gw * 0.5625;
    s.addImage({ path: fit(img("ki_gastro_terrasse.jpg"), gw, gh), x: MX, y: 1.5, w: gw, h: gh, altText: "Terrasse am Abend" });
    s.addImage({ path: fit(img("ki_aussen_1.jpg"), gw, gh), x: MX + gw + 0.3, y: 1.5, w: gw, h: gh, altText: "Haus am Abend" });
    text(s, [
      { text: "ca. 60 Plätze auf Holzdeck unter dunklem Stahl-Vordach, Heizstrahler und Windschutz verlängern die Saison.", options: { bullet: true, breakLine: true } },
      { text: "Die vollverglaste Fassade über die ganze Länge zeigt das Leben im Haus und zieht Gäste an.", options: { bullet: true, breakLine: true } },
      { text: "Die Wohnungen darüber haben eigene Eingänge und Balkone zur anderen Seite, wichtig für Ruhe.", options: { bullet: true } },
    ], { x: MX, y: 1.5 + gh + 0.2, w: W - 2 * MX, h: 1.4, fontSize: 14, paraSpaceAfter: 5 });
  }

  // ---- 10 Umsatzaufbau
  { const s = content(`Wie ${eur(UM)} Umsatz im Monat zusammenkommen`, "Für Bank", `Plausibilitätsrechnung mit Annahmen für Gäste und Bon. Ca. ${eur(Math.round(BV.g_umsatz_platz / 100) * 100)} Umsatz je Sitzplatz und Jahr bei 190 Plätzen, Branchen-Median Österreich ca. 12.000 €.`);
    const rows = [[hdr("Bereich"), hdr("Tage / Monat", "right"), hdr("Gäste pro Tag", "right"), hdr("Ø Bon", "right"), hdr("Umsatz / Monat", "right")]];
    SEG.forEach((g) => rows.push([cell(g[0]), R(String(g[1]).replace(".", ",")), R(String(g[2])), R(eur(g[3])), R(eur(g[1] * g[2] * g[3]))]));
    rows.push([cell("Summe", { bold: true }), R(""), R(""), R(""), R(eur(segSumme), { bold: true })]);
    s.addTable(rows, { x: MX, y: 1.5, w: 8.2, colW: [4.0, 0.9, 1.0, 0.9, 1.4], rowH: 0.5, border, objectName: "Tabelle Umsatzaufbau" });
    card(s, 9.2, 1.5, W - 9.2 - MX, 4.5, "Einordnung");
    text(s, [
      { text: "Was das bedeutet", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Ca. ${nf.format(Math.round(gaesteMonat))} Gäste im Monat, im Schnitt ca. ${Math.round(gaesteMonat / 26)} pro Öffnungstag bei 190 Plätzen. Der Abend (Bar mit Snacks, Events) bringt ${Math.round(BV.g_abend_anteil * 100)} % vom Umsatz.`, options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Nicht eingerechnet", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Terrasse im Sommer, Catering und Weihnachtsfeiern. Das ist Spielraum nach oben.", options: {} },
    ], { x: 9.45, y: 1.7, w: W - 9.2 - MX - 0.5, h: 4.2, fontSize: 13 });
  }

  // ---- 11 Betrieb und Personal
  { const s = content("Betrieb und Personal (Beispiel)", "Für Bank", "Personal ca. 30 % vom Umsatz (Branchen-Richtwert). Der Lohn des Bauherrn ist nicht gerechnet. Beträge sind Arbeitgeber-Brutto, Annahmen.");
    const pers = [["Küchenleitung (Bowls, Snacks)", "1 Vollzeit", 3400], ["Küchenhilfe", "1 Teilzeit", 2400], ["Spülen, Frühstücksservice", "1 Teilzeit", 1400], ["Barchef", "1 Vollzeit", 3200], ["Service und Bar", "ca. 8 Teilzeit und Minijobs", 7600]];
    const sum = pers.reduce((a, p) => a + p[2], 0);
    const rows = [[hdr("Stelle"), hdr("Umfang"), hdr("Kosten / Monat", "right")], ...pers.map((p) => [cell(p[0]), cell(p[1]), R(eur(p[2]))]), [cell("Summe", { bold: true }), cell(`entspricht ${Math.round((sum / UM) * 100)} % vom Umsatz`), R(eur(sum), { bold: true })]];
    s.addTable(rows, { x: MX, y: 1.5, w: 7.6, colW: [2.8, 3.0, 1.8], rowH: 0.55, border, objectName: "Tabelle Personal" });
    card(s, 8.6, 1.5, W - 8.6 - MX, 4.6, "Betrieb");
    text(s, [
      { text: "Betreiber", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Du führst die Gastro selbst oder verpachtest sie. Bei Verpachtung zahlt der Betreiber ca. 10 €/m² Pacht, das sind bei 510 m² ca. 5.100 € im Monat (ca. " + Math.round(BV.g_pacht_quote * 1000) / 10 + " % vom Umsatz).", options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Start", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Barchef und Küchenleitung früh einstellen, 4 bis 6 Wochen vor Eröffnung Probebetrieb.", options: {} },
    ], { x: 8.85, y: 1.7, w: W - 8.6 - MX - 0.5, h: 4.2, fontSize: 13 });
  }

  // ---- 12 Wirtschaftlichkeit
  { const s = content("Wirtschaftlichkeit der Gastro", "Für Bank", "Marge vor Pacht 30,5 % vom Umsatz (Branchen-Richtwert, nicht aus Werlte). Bei sehr niedrigem Umsatz drücken die Fixkosten stärker, die Rechnung ist dort zu günstig.");
    const rows = [[hdr("Umsatz pro Monat"), hdr("Gewinn vor Pacht", "right"), hdr("Pacht ans Haus", "right"), hdr("Gewinn nach Pacht", "right")]];
    [40000, 50000, UM, 80000, 95000].forEach((u) => { const g = u * 0.305; rows.push([cell(eur(u), { bold: u === UM }), R(eur(g)), R(eur(-v.pacht)), cf(g - v.pacht)]); });
    s.addTable(rows, { x: MX, y: 1.5, w: 8.4, colW: [2.4, 2.0, 2.0, 2.0], rowH: 0.55, border, objectName: "Tabelle Gastro Gewinn" });
    const BV = JSON.parse(require("fs").readFileSync(path.join(__dirname, "bank_values.json"), "utf8"));
    card(s, 9.4, 1.5, W - 9.4 - MX, 4.2, "Haus");
    text(s, [
      { text: "Für das ganze Haus", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Mit ${eur(UM)} Umsatz bleiben im ganzen Haus ${eurS(BV.c_ergebnis)} pro Monat nach Zinsen und Tilgung (KfW-Kredite und Hausbank, ohne Lohn). Die Gastro braucht für Break-even im Haus ca. ${eur(Math.round(BV.breakeven_haus / 100) * 100)} Umsatz.`, options: {} },
    ], { x: 9.65, y: 1.7, w: W - 9.4 - MX - 0.5, h: 3.9, fontSize: 13 });
    text(s, "Kosten im Detail (Wareneinsatz, Personal, Energie ...) stehen im Anhang der Hauptpräsentation.", { x: MX, y: 5.0, w: 8.4, h: 0.5, fontSize: 13, color: C.accent4 });
  }

  // ---- 13 Ausbau
  { const s = content("Ausbau: Budget und Posten", "Für Bank", "Hochgerechnet vom Budget des Bauherrn (150.000 € für 150 Plätze): 1.000 € je Platz bei 190 Plätzen. Angebote von Küchen- und Lüftungsbauern müssen es bestätigen.");
    const items = [["Küche (Bowl- und Snackküche, Kühlräume, Spülküche)", 28000], ["Lüftung und Abluft", 23000], ["Theke und Bar (Zapfanlage, Kühlung, Backbar, große Theke)", 35000], ["Möbel (ca. 190 Plätze, Lounge, Séparée)", 36000], ["Beleuchtung und Deko", 10000], ["Wand, Boden, Decke, Akustik", 19000], ["Gäste-WC Ausstattung", 6000], ["Kasse, Technik, Musik, WLAN", 6000], ["Terrasse (Holzdeck, Möbel, Heizstrahler, 60 Plätze)", 8000], ["Planung und Genehmigung", 6000], ["Eröffnung, Marketing, Warenerstbestückung", 4000]];
    const sumN = items.reduce((a, r) => a + r[1], 0);
    const rows = [[hdr("Posten"), hdr("Betrag", "right")], ...items.map((r) => [cell(r[0]), R(eur(r[1]))]), [cell("Puffer 5 %"), R(eur(sumN * 0.05))], [cell("Summe (im Modell: 190.000 €)", { bold: true }), R(eur(sumN * 1.05), { bold: true })]];
    s.addTable(rows, { x: MX, y: 1.4, w: 8.0, colW: [6.0, 2.0], rowH: 0.34, border, objectName: "Tabelle Ausbau" });
    const f0 = finanz(v, 0, A.zinsPlan), f2 = finanz(v, 0, A.zinsPlan, { gastroAusbau: 250000 });
    card(s, 9.0, 1.4, W - 9.0 - MX, 3.2, "Hinweis");
    text(s, `Bei ${eur(250000)} Ausbau steigt die Rate des Hauses um ca. ${eur(f2.rate - f0.rate)} im Monat. Der Schallschutz zur Decke und die Küchenabluft (über Dach, weg von den Wohnungen) gehören unbedingt in die Planung.`, { x: 9.25, y: 1.6, w: W - 9.0 - MX - 0.5, h: 2.8, fontSize: 14 });
  }

  // ---- 14 Genehmigung und Risiken
  { const s = content("Genehmigung, Recht und Risiken", "Für Stadt und Bank", "Hinweise sind keine Rechtsberatung. Bitte mit Bauamt und Ordnungsamt klären.");
    const items = [
      ["Konzession und Hygiene", "Gaststättenerlaubnis beim Ordnungsamt, Hygienekonzept und Lebensmittelaufsicht, Alkoholausschank anmelden."],
      ["Schall und Abluft", "Gastro unter Wohnungen: Schallschutz der Decke, leise Technik, Abluft der kleinen Küche über Dach. Nutzungszeiten der Terrasse klären."],
      ["Stellplätze", "Bedarf der großen Gastro ca. 37 Plätze, mit Büros und Wohnungen ca. 55. Auf dem Grundstück passen nur ca. 6–8, Rest über die öffentliche Parkfläche oder Ablöse."],
      ["Markt und Betreiber", "Keine Marktdaten für Werlte. Erfahrener Betreiber oder Barchef früh gewinnen, Probebetrieb und vorsichtiger Start."],
    ];
    items.forEach((it, i) => { const x = MX + (i % 2) * 6.2, y = 1.5 + Math.floor(i / 2) * 2.4; card(s, x, y, 5.9, 2.2, it[0]); text(s, it[0], { x: x + 0.25, y: y + 0.15, w: 5.4, h: 0.4, fontSize: 17, fontFace: "Georgia", color: C.accent1 }); text(s, it[1], { x: x + 0.25, y: y + 0.65, w: 5.4, h: 1.4, fontSize: 13 }); });
  }

  // ---- 15 Nächste Schritte
  { const s = content("Nächste Schritte für die Gastro", "Für Stadt und Bank", "Zeitplan passend zum Baubeginn Mitte 2027 und zur Eröffnung Ende 2028.");
    const steps = [["Jetzt", "Name, Marke und Zielgruppe festlegen, Betreiber oder Barchef ansprechen"], ["Q4 2026", "Gastro-Fachplaner: Küche, Lüftung, Schallschutz, genaue Plätze"], ["Q1 2027", "Angebote für Ausbau einholen, Budget prüfen (190.000 €)"], ["2027", "Innenarchitektur und Möbel bestellen, Speisekarte und Preise kalkulieren"], ["Mitte 2028", "Personal einstellen, Probebetrieb, Genehmigungen"], ["Ende 2028", "Eröffnung zusammen mit der neuen Mitte"]];
    steps.forEach((st, i) => { const y = 1.5 + i * 0.85; s.addShape(pres.ShapeType.ellipse, { x: MX, y, w: 0.55, h: 0.55, fill: { color: i === 5 ? C.accent1 : C.accent2 }, line: { color: C.background1, width: 1 }, objectName: "Schritt " + (i + 1) }); text(s, String(i + 1), { x: MX, y, w: 0.55, h: 0.55, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle" }); text(s, st[0], { x: MX + 0.85, y: y + 0.02, w: 1.8, h: 0.5, fontSize: 17, bold: true, color: C.accent1, valign: "middle" }); text(s, st[1], { x: MX + 2.7, y: y + 0.02, w: 9, h: 0.5, fontSize: 15, valign: "middle" }); });
  }
  await t.save();
}
deck();
