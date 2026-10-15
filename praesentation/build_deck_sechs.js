// Deck: Neue Mitte Werlte, Baufeld 3. 6 Wohnungen, EG komplett große Gastro, 930 m² BGF, Flachdach mit Staffelgeschoss in Holzbau
// Aufruf: NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_deck_sechs.js
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");
const { A, VARIANTEN, finanz, cashflow, umsatzBreakEven, bauRoh, teilung, LAYOUTS } = require("./model");
const { execFileSync } = require("child_process");

const IMG = process.env.BILDER || path.join(__dirname, "bilder");
const OUT = process.env.OUT || __dirname;
const v = VARIANTEN.sechs;
const UM = v.umsatz; // Basis-Umsatz 50.000 €
// KI-Bilder (optional): werden automatisch eingebaut, wenn die Dateien in bilder/ liegen
const KI = ["ki_aussen_1.jpg", "ki_aussen_2.jpg", "ki_terrasse.jpg", "ki_innen_1.jpg", "ki_innen_2.jpg"].map((n) => path.join(IMG, n)).filter((f) => fs.existsSync(f));
const KI_AUSSEN = path.join(IMG, "ki_aussen_1.jpg");

// Bild verzerrungsfrei zuschneiden (Mitte), liefert Pfad zum passenden Ausschnitt
function fit(file, w, h) {
  const out = path.join(require("os").tmpdir(), "crop_" + path.basename(file).replace(/\W/g, "_") + "_" + Math.round(w * 100) + "x" + Math.round(h * 100) + ".jpg");
  execFileSync("python3", ["-c", "import sys\nfrom PIL import Image\nim=Image.open(sys.argv[1]).convert('RGB');W,H=im.size;r=float(sys.argv[3])/float(sys.argv[4])\nif W/H>r:\n    nw=int(H*r);x=(W-nw)//2;im=im.crop((x,0,x+nw,H))\nelse:\n    nh=int(W/r);y=(H-nh)//2;im=im.crop((0,y,W,y+nh))\nim.save(sys.argv[2],quality=92)", file, out, String(w), String(h)]);
  return out;
}
const hasKI = (n) => fs.existsSync(path.join(IMG, n));

const THEME = {
  name: "Neue Mitte Werlte",
  headFontFace: "Georgia",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1F2421", lt1: "FFFFFF", dk2: "2F4A3E", lt2: "F1F0EE",
    accent1: "8C3B32", accent2: "2F4A3E", accent3: "C49A45", accent4: "5B6770", accent5: "2E7D5B", accent6: "B3261E",
    hlink: "8C3B32", folHlink: "5B6770",
  },
};

const FOERDERUNG = [0, 0.05, 0.1, 0.15, 0.2, 0.25];
const nf = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
const eur = (n) => `${n < 0 ? "−" : ""}${nf.format(Math.abs(Math.round(n)))} €`;
const eurS = (n) => `${n > 0 ? "+" : n < 0 ? "−" : ""}${nf.format(Math.abs(Math.round(n)))} €`;
const pct = (f) => `${Math.round(f * 100)} %`;
const mio = (n) => `${(n / 1e6).toFixed(2).replace(".", ",")} Mio. €`;
const k = (n) => `${nf.format(n)} €`;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Neue Mitte Werlte – Baufeld 3: Gastro und 6 Wohnungen";
pres.author = "Bessam Hasso";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const W = 13.33;
const H = 7.5;
const MX = 0.6;

pres.defineSlideMaster({ title: "TITEL", background: { color: "2F4A3E" }, objects: [] });
pres.defineSlideMaster({
  title: "INHALT",
  background: { color: "FFFFFF" },
  objects: [
    { rect: { x: MX, y: 1.2, w: 0.9, h: 0.045, fill: { color: C.accent3 }, line: { color: C.accent3, width: 0 } } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.35, w: W - 2 * MX, h: 0.9, fontFace: "Georgia", fontSize: 30, bold: false, color: C.accent1, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: W - 1.1, y: H - 0.45, w: 0.6, h: 0.3, fontSize: 10, color: C.accent4, align: "right" },
});

function content(title, tag, notes) {
  const s = pres.addSlide({ masterName: "INHALT" });
  s.addText(title, { placeholder: "title" });
  if (tag) s.addText(tag, { x: MX, y: H - 0.45, w: 6, h: 0.3, fontSize: 10, color: C.accent4, margin: 0, isTextBox: true, objectName: "Zielgruppe" });
  if (notes) s.addNotes(notes);
  return s;
}
function text(s, t, o) {
  if (o && o.fontSize && o.fontFace !== "Georgia") o = Object.assign({}, o, { fontSize: Math.round(o.fontSize * 1.0 * 2) / 2 });
  s.addText(t, Object.assign({ fontFace: "Arial", fontSize: 13, color: C.text1, margin: 0, isTextBox: true, valign: "top" }, o));
}
function card(s, x, y, w, h, name) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: C.background2 }, line: { color: C.background2, width: 0 }, rectRadius: 0.08, objectName: name || "Karte" });
}
function stat(s, x, y, w, big, label, color) {
  card(s, x, y, w, 1.55, "Kennzahl " + label);
  text(s, big, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.75, fontSize: 30, bold: false, fontFace: "Georgia", color: color || C.accent1, valign: "middle" });
  text(s, label, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: 0.5, fontSize: 14, color: C.accent4 });
}
const hdr = (t, align) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent2 }, align: align || "left", fontSize: 12.5, fontFace: "Arial" } });
const cell = (t, o) => ({ text: t, options: Object.assign({ fontSize: 12.5, fontFace: "Arial" }, o) });
const cfCell = (n, o) => cell(eurS(n), Object.assign({ align: "right", bold: true, color: n >= 0 ? C.accent5 : C.accent6, fill: { color: n >= 0 ? "E3F1EA" : "F8E4E2" } }, o));
const R = (t, o) => cell(t, Object.assign({ align: "right" }, o));
const tblBorder = { type: "solid", color: "FFFFFF", pt: 1 };

const F = {};
for (const f of FOERDERUNG) {
  F[f] = { plan: finanz(v, f, A.zinsPlan), ausgang: finanz(v, f, A.zinsAusgang) };
  F[f].cfPlan = cashflow(v, F[f].plan);
  F[f].cfAusgang = cashflow(v, F[f].ausgang);
}
const f0 = F[0];
const firstPos = FOERDERUNG.find((f) => F[f].cfPlan.cf >= 0);

// ===== 1 Titel =====
{
  const s = pres.addSlide({ masterName: "TITEL" });
  s.addImage({ path: fit(hasKI("ki_aussen_1.jpg") ? KI_AUSSEN : path.join(IMG, "aussen.jpg"), 6.43, H), x: 6.9, y: 0, w: 6.43, h: H, altText: "Außenansicht, modernes Haus mit Klinker und Glas-Erdgeschoss" });
  text(s, "NEUE MITTE WERLTE", { x: MX, y: 1.3, w: 6, h: 0.4, fontSize: 16, bold: true, color: C.accent3, charSpacing: 4 });
  text(s, "Baufeld 3: Große Gastro und 6 Wohnungen", { x: MX, y: 1.85, w: 6, h: 2.2, fontSize: 37, bold: false, fontFace: "Georgia", color: C.background1 });
  text(s, "Baukonzept und Wirtschaftlichkeit", { x: MX, y: 4.3, w: 6, h: 0.6, fontSize: 18, color: C.background1 });
  text(s, "Bessam Hasso, Werlte\nBebauungsplan Nr. 123, 1. Änderung (Entwurf 25.08.2026)\nStand Oktober 2026", { x: MX, y: 5.5, w: 6, h: 1.1, fontSize: 14, color: "CFD8D3" });
  s.addNotes("Titelfolie. Das Bild ist eine Referenzstudie.");
}

// ===== 2 Überblick =====
{
  const s = content("Das Vorhaben auf einen Blick", "Für Stadt und Bank", "Kernaussage: Das Haus trägt sich mit Förderung und einer gut laufenden Gastro.");
  const w = (W - 2 * MX - 0.6) / 4;
  stat(s, MX, 1.5, w, mio(f0.plan.gesamt), "Gesamtkosten (ohne Bauzeitzinsen)");
  stat(s, MX + (w + 0.2), 1.5, w, "6", "Wohnungen und eine Gastro von ca. 290 m² im ganzen EG", C.accent2);
  stat(s, MX + 2 * (w + 0.2), 1.5, w, eur(f0.plan.rate), "Rate pro Monat (3,3 %, ohne Förderung)");
  stat(s, MX + 3 * (w + 0.2), 1.5, w, eurS(f0.cfPlan.cf), `Ergebnis pro Monat bei ${k(UM)} Umsatz`, f0.cfPlan.cf >= 0 ? C.accent5 : C.accent6);
  text(s, `Ergebnis pro Monat (ohne Lohn des Bauherrn) bei ${k(UM)} Gastro-Umsatz (Plan, 3,3 % Zins)`, { x: MX, y: 3.4, w: 10, h: 0.35, fontSize: 16, bold: true, color: C.accent2 });
  s.addTable([[hdr("Förderung"), ...FOERDERUNG.map((f) => hdr(pct(f), "right"))], [cell("Ergebnis"), ...FOERDERUNG.map((f) => cfCell(F[f].cfPlan.cf))]], {
    x: MX, y: 3.85, w: W - 2 * MX, colW: [2.2, ...FOERDERUNG.map(() => (W - 2 * MX - 2.2) / FOERDERUNG.length)], rowH: 0.5, border: tblBorder, objectName: "Tabelle Förderung",
  });
  text(s, [
    { text: firstPos === 0 ? "Schon ohne Förderung im Plus. " : `Mit ${pct(firstPos)} Förderung läuft das Haus erstmals im Plus. `, options: { bold: true } },
    { text: `Break-even-Umsatz ohne Förderung ca. ${k(Math.round(umsatzBreakEven(v, f0.plan) / 100) * 100)} im Monat. Dazu kommt eine Anlaufphase von 12 Monaten ohne Rate (Aufschub).` },
  ], { x: MX, y: 5.0, w: W - 2 * MX, h: 1.2, fontSize: 16 });
}

// ===== 3 Standort =====
{
  const s = content("Ein Eckgrundstück an der neuen Mitte", "Für die Stadt", "Quelle: Konzeptheft Neue Mitte Werlte (Seiten 13, 16 und 24).");
  [["ca. 960 m²", "Baufeld 3, östlich des Rathauses, südlich der Planstraße"], ["Mischgebiet", "Gewerbe im EG erwünscht, Stellplätze auf dem Grundstück"], ["Baureife", "liegt vor, Baubeginn jederzeit möglich"]].forEach((it, i) => {
    card(s, MX, 1.5 + i * 1.4, 5.2, 1.2, "Fakt " + (i + 1));
    text(s, it[0], { x: MX + 0.25, y: 1.6 + i * 1.4, w: 4.7, h: 0.5, fontSize: 22, bold: false, fontFace: "Georgia", color: C.accent1 });
    text(s, it[1], { x: MX + 0.25, y: 2.15 + i * 1.4, w: 4.7, h: 0.5, fontSize: 14 });
  });
  const tl = [["Nov 2026", "Stellplatz alte Grundschule"], ["ab März 2027", "Bau Planstraße (Erschließung)"], ["Mitte 2027", "Unser Baubeginn"], ["ab Juli 2027", "Kreisverkehr Loruper Straße"], ["Ende 2028", "Marktplatz, Rathaus fertig und unsere Eröffnung"]];
  const x0 = 6.7;
  s.addShape(pres.ShapeType.line, { x: x0 + 0.15, y: 1.65, w: 0, h: 4.4, line: { color: C.accent4, width: 2 }, objectName: "Zeitleiste" });
  tl.forEach((t, i) => {
    const y = 1.5 + i * 0.95;
    const hl = i === 2 || i === 4;
    s.addShape(pres.ShapeType.ellipse, { x: x0, y: y + 0.05, w: 0.3, h: 0.3, fill: { color: hl ? C.accent1 : C.accent3 }, line: { color: C.background1, width: 2 }, objectName: "Punkt " + (i + 1) });
    text(s, t[0], { x: x0 + 0.5, y, w: 5.5, h: 0.4, fontSize: 18, bold: true, color: hl ? C.accent1 : C.text1 });
    text(s, t[1], { x: x0 + 0.5, y: y + 0.4, w: 5.5, h: 0.4, fontSize: 14, color: C.accent4 });
  });
}

// ===== 4 B-Plan =====
{
  const s = content("Was der Bebauungsplan vorgibt", "Für die Stadt", "Festsetzungen aus Bebauungsplan Nr. 123 (Entwurf). Zulässigkeit von Staffelgeschoss und Flachdach muss die Stadt schriftlich bestätigen.");
  const rows = [
    [hdr("Festsetzung"), hdr("Wert im B-Plan"), hdr("Unser Entwurf")],
    [cell("Grundflächenzahl (GRZ)"), cell("0,6 → max. 576 m²"), cell("340 m² Grundfläche (35 %)")],
    [cell("Vollgeschosse"), cell("zwei (II im Kreis)"), cell("EG und 1. OG, dazu Staffelgeschoss")],
    [cell("Traufhöhe / Höhe"), cell("6,50 m / 12,00 m"), cell("Hauptbaukörper 6,50 m, gesamt ca. 9,90 m")],
    [cell("Dachform"), cell("laut Konzeptheft Mischgebiet, Details im Plan"), cell("Flachdach mit zurückgesetztem Staffelgeschoss")],
    [cell("Baufenster (geschätzt)"), cell("ca. 27 × 15–17 m = 400–460 m²"), cell("ca. 24 × 14,2 m")],
    [cell("Stellplätze"), cell("auf dem Grundstück, ausreichende Anzahl"), cell("ca. 10–13, Rest siehe Stellplatzfolie")],
  ];
  s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.2, 4.4, 4.53], rowH: 0.52, border: tblBorder, objectName: "Tabelle B-Plan" });
  card(s, MX, 5.4, W - 2 * MX, 1.25, "Klärungsbedarf");
  text(s, [
    { text: "Schriftlich klären: ", options: { bold: true, color: C.accent1 } },
    { text: "Zählt das Staffelgeschoss (ca. 250 m² in Holzbau, das sind 74 % der Fläche darunter) als drittes Vollgeschoss? Ab etwa 2/3 der Fläche darunter wird es meist dazugezählt. Ist die Flachdach-Lösung zulässig?" },
  ], { x: MX + 0.25, y: 5.5, w: W - 2 * MX - 0.5, h: 1.05, fontSize: 15, valign: "middle" });
}

// ===== 4b Holzbau und Terrasse =====
{
  const s = content("Staffelgeschoss in Holzbau mit Terrasse rundum", "Für Bank und Stadt", "Preise sind Annahmen und müssen durch Angebote der Zimmerei und des Bauunternehmens bestätigt werden.");
  const rows = [[hdr("Bauunternehmer-Preisnachlass auf den Bau"), hdr("Gesamtkosten", "right"), hdr("Rate (Plan)", "right"), hdr("Ergebnis/Monat", "right")]];
  [0, 0.05, 0.1].forEach((r) => {
    const fin = finanz(v, 0, A.zinsPlan, { bauRabatt: r });
    rows.push([cell(r === 0 ? "keiner (Annahme in der Rechnung)" : `${Math.round(r * 100)} % (Bekanntenpreis, noch offen)`), R(eur(fin.gesamt)), R(eur(fin.rate)), cfCell(cashflow(v, fin).cf)]);
  });
  s.addTable(rows, { x: MX, y: 1.5, w: 7.6, colW: [3.1, 1.6, 1.3, 1.6], rowH: 0.55, border: tblBorder, objectName: "Tabelle Holzbau Rabatt" });
  const ohne = finanz(Object.assign({}, v, { holzM2: 0, terrasseM2: 0 }), 0, A.zinsPlan);
  text(s, `Ergebnis bei ${k(UM)} Gastro-Umsatz und 3,3 % Zins. Ohne Holzbau und Terrasse wäre der Bau ${eur(bauRoh(Object.assign({}, v, { holzM2: 0, terrasseM2: 0 })) - bauRoh(v))} teurer, die Kosten lägen bei ${eur(ohne.gesamt)}.`, { x: MX, y: 4.0, w: 7.6, h: 1.0, fontSize: 14, color: C.accent4 });
  card(s, 8.6, 1.5, W - 8.6 - MX, 4.6, "Warum Holz oben");
  text(s, [
    { text: "Leichter und schneller: weniger Last auf dem Klinker-Geschoss, kürzere Bauzeit.", options: { bullet: true, breakLine: true } },
    { text: "Zimmerei kennt das Haus von Anfang an und plant das Penthouse mit der Terrasse rundum.", options: { bullet: true, breakLine: true } },
    { text: "Zwei Partner (Bauunternehmen unten, Zimmerei oben) können Preise und Termine gemeinsam angeben.", options: { bullet: true, breakLine: true } },
    { text: "Brandschutz (Holzbau bis Gebäudeklasse 4, Aufzug und Treppenhaus massiv) und Schallschutz muss der Architekt nachweisen.", options: { bullet: true } },
  ], { x: 8.85, y: 1.95, w: W - 8.85 - MX - 0.5, h: 4.0, fontSize: 14, paraSpaceAfter: 8 });
  text(s, "Das Staffelgeschoss springt rundum um ca. 1,3 m zurück: Terrasse ca. 90 m² um die drei Penthouses, kein Teil der BGF.", { x: MX, y: 5.3, w: 7.6, h: 0.9, fontSize: 15, bold: true, color: C.accent2 });
}

// ===== 5 Schnitt =====
{
  const s = content("Zwei Geschosse plus Staffelgeschoss", "Für Stadt und Bank", "Schnitt schematisch. Hauptbaukörper bis 6,50 m, Staffelgeschoss bis ca. 9,60 m, Attika ca. 9,90 m.");
  const sc = 0.34; // Zoll je m
  const x0 = 2.0;
  const yBase = 6.4;
  const z = (m) => yBase - m * sc;
  const w = 14.2 * sc;
  s.addShape(pres.ShapeType.rect, { x: x0 - 0.3, y: yBase, w: w + 0.6, h: 0.06, fill: { color: C.accent4 }, line: { color: C.accent4, width: 0 }, objectName: "Gelände" });
  s.addShape(pres.ShapeType.rect, { x: x0, y: z(3.5), w, h: 3.2 * sc, fill: { color: "F4D58F" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt EG" });
  s.addShape(pres.ShapeType.rect, { x: x0, y: z(6.5), w, h: 3.0 * sc, fill: { color: "9A4034" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt OG" });
  s.addShape(pres.ShapeType.rect, { x: x0, y: z(9.6), w: 13.3 * sc, h: 3.1 * sc, fill: { color: "7A5C3A" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt Staffel" });
  s.addShape(pres.ShapeType.rect, { x: x0 - 0.2, y: z(9.9), w: 13.3 * sc + 0.4, h: 0.3 * sc, fill: { color: "D6D1C8" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt Dach" });
  s.addShape(pres.ShapeType.rect, { x: x0 + 13.3 * sc, y: z(7.6), w: 0.9 * sc, h: 1.1 * sc, fill: { color: "CFE0E8" }, line: { color: C.accent4, width: 1 }, objectName: "Brüstung" });
  text(s, "EG Gastro mit Bar", { x: x0, y: z(3.5), w, h: 3.2 * sc, fontSize: 14, bold: true, align: "center", valign: "middle" });
  text(s, "1. OG · 3 Wohnungen", { x: x0, y: z(6.5), w, h: 3.0 * sc, fontSize: 14, bold: true, align: "center", valign: "middle", color: C.background1 });
  text(s, "Staffelgeschoss · 3 Wohnungen", { x: x0, y: z(9.6), w: 13.3 * sc, h: 3.1 * sc, fontSize: 14, bold: true, align: "center", valign: "middle", color: C.background1 });
  const mark = (zz, label) => {
    s.addShape(pres.ShapeType.line, { x: x0 - 0.5, y: z(zz), w: w + 0.8, h: 0, line: { color: C.accent1, width: 1, dashType: "dash" }, objectName: "Marke " + label });
    text(s, label, { x: MX, y: z(zz) - 0.2, w: 1.1, h: 0.4, fontSize: 12, bold: true, color: C.accent1, align: "right", valign: "middle" });
  };
  mark(9.9, "ca. 9,90 m");
  mark(6.5, "6,50 m");
  text(s, "Süd", { x: x0 + w - 0.5, y: yBase + 0.1, w: 0.6, h: 0.3, fontSize: 12, color: C.accent4, align: "right" });
  text(s, "Nord", { x: x0, y: yBase + 0.1, w: 0.6, h: 0.3, fontSize: 12, color: C.accent4 });
  const rows = [
    [hdr("Ebene"), hdr("Nutzung"), hdr("BGF", "right")],
    [cell("EG"), cell("Gastro ca. 290 m² mit Bar, Treppenhaus, Aufzug, Technik"), R("340 m²")],
    [cell("1. OG"), cell("3 Wohnungen à ca. 85 m²"), R("340 m²")],
    [cell("Staffel"), cell("3 Wohnungen à ca. 56 m², Holzbau, Terrasse rundum"), R("250 m²")],
    [cell("Summe", { bold: true }), cell("6 Wohnungen, ca. 423 m² Wohnfläche", { bold: true }), R("930 m²", { bold: true })],
  ];
  s.addTable(rows, { x: 7.7, y: 1.6, w: W - 7.7 - MX, colW: [0.9, 3.2, 0.93], rowH: 0.6, border: tblBorder, objectName: "Tabelle Flächen" });
  text(s, "BGF = Bruttogrundfläche, alle Geschossflächen zusammen. Das Staffelgeschoss in Holzbau springt rundum um ca. 1,3 m zurück, so entsteht eine Terrasse von ca. 90 m² um die Penthouses.", { x: 7.7, y: 5.4, w: W - 7.7 - MX, h: 1.0, fontSize: 14, color: C.accent4 });
}

// ===== 6 Grundrisse =====
{
  const s = content("Skizzen der Geschosse", "Für die Stadt", "Schematische Skizzen, nicht maßstäblich genau. Aufteilung wird mit dem Architekten verfeinert.");
  const sc = 0.165;
  const pw = 24 * sc;
  const ph = 14.2 * sc;
  const gap = (W - 2 * MX - 3 * pw) / 2;
  const y0 = 2.3;
  const plans = [
    {
      title: "Erdgeschoss",
      rooms: [
        [0, 0, 3.6, 14.2, "Treppe, Aufzug", "8A9199"],
        [3.6, 0, 20.4, 14.2, "", "F2D48C"],
        [4.0, 0.4, 4.2, 1.8, "Bar", "B88652"],
        [12.4, 0, 8, 4.2, "Küche", "7E8A94"],
        [8.4, 0, 4, 4.2, "WC", "A6ADB4"],
        [6, 6.5, 14, 4.5, "Gastraum, ca. 100 Plätze", "E7BE63"],
      ],
    },
    {
      title: "1. Obergeschoss",
      rooms: [
        [0, 0, 3.6, 14.2, "Treppe, Aufzug", "8A9199"],
        [3.6, 0, 6.8, 14.2, "WE 1 · 85 m²", "9A4034"],
        [10.4, 0, 6.8, 14.2, "WE 2 · 85 m²", "9A4034"],
        [17.2, 0, 6.8, 14.2, "WE 3 · 85 m²", "9A4034"],
      ],
    },
    {
      title: "Staffel (Holzbau)",
      rooms: [
        [0, 0, 24, 14.2, "", "C9C4B8"],
        [1.3, 1.3, 3.6, 11.6, "Treppe", "8A9199"],
        [4.9, 1.3, 5.93, 11.6, "WE 4 · 56 m²", "7A5C3A"],
        [10.83, 1.3, 5.93, 11.6, "WE 5 · 56 m²", "7A5C3A"],
        [16.77, 1.3, 5.93, 11.6, "WE 6 · 56 m²", "7A5C3A"],
      ],
    },
  ];
  plans.forEach((p, i) => {
    const x = MX + i * (pw + gap);
    text(s, p.title, { x, y: 1.5, w: pw, h: 0.4, fontSize: 18, bold: true, color: C.accent2 });
    s.addShape(pres.ShapeType.rect, { x, y: y0 - 0.1, w: pw, h: ph + 0.2, fill: { color: "FFFFFF" }, line: { color: C.accent4, width: 1, dashType: "dash" }, objectName: "Baukörper " + p.title });
    p.rooms.forEach((r) => {
      s.addShape(pres.ShapeType.rect, { x: x + r[0] * sc, y: y0 + r[1] * sc, w: r[2] * sc, h: r[3] * sc, fill: { color: r[5] }, line: { color: "FFFFFF", width: 1.5 }, objectName: "Raum " + (r[4] || "Fläche") });
      if (r[4]) text(s, r[4], { x: x + r[0] * sc, y: y0 + r[1] * sc, w: r[2] * sc, h: r[3] * sc, fontSize: 11, bold: true, color: r[5] === "F2D48C" || r[5] === "E7BE63" || r[5] === "C9C4B8" ? "1F2421" : "FFFFFF", align: "center", valign: "middle" });
    });
  });
  card(s, MX, 5.35, W - 2 * MX, 1.2, "Hinweis");
  text(s, "Grundfläche 24 × 14,2 m = 340 m², das passt in das geschätzte Baufenster. Treppenhaus und Aufzug liegen am Westende und erschließen die Wohnungen getrennt von der Gastro. Die Staffel in Holzbau hat ca. 250 m² BGF, die beige Fläche ist die Terrasse (ca. 90 m²) rundum um die Penthouses.", { x: MX + 0.25, y: 5.45, w: W - 2 * MX - 0.5, h: 1.0, fontSize: 15, valign: "middle" });
}

// ===== 7 Außen =====
{
  const s = content("Modern, Klinker, Glas und Staffelgeschoss", "Für die Stadt", "Links Referenzstudie, rechts unsere Eckansicht als Skizze.");
  s.addImage({ path: fit(hasKI("ki_aussen_1.jpg") ? path.join(IMG, "ki_aussen_1.jpg") : path.join(IMG, "aussen.jpg"), 5.9, 3.29), x: MX, y: 1.4, w: 5.9, h: 3.29, altText: "Visualisierung Außenansicht" });
  s.addImage({ path: path.join(IMG, "skizze_aussen_ecke.png"), x: 6.8, y: 1.4, w: 5.9, h: 3.69, sizing: { type: "contain", w: 5.9, h: 3.69 }, altText: "Eckansicht als Skizze: Flachdach mit Staffelgeschoss, Balkone, vollverglastes Erdgeschoss" });
  text(s, hasKI("ki_aussen_1.jpg") ? "KI-Visualisierung" : "Referenzstudie", { x: MX, y: 4.75, w: 5.9, h: 0.3, fontSize: 12, color: C.accent4 });
  text(s, "Unsere Skizze (Eckansicht)", { x: 6.8, y: 5.12, w: 5.9, h: 0.3, fontSize: 12, color: C.accent4 });
  const pts = [["Klinker", "dunkel, Langformat, passend zum Umfeld"], ["Staffelgeschoss", "Holzbau, Terrasse rundum"], ["Balkone", "bodentiefe Fenster mit Glasbrüstung"], ["Glas-EG", "Gastro mit Bar, Terrasse und Vordach"]];
  pts.forEach((p, i) => {
    const x = MX + i * 3.05;
    text(s, p[0], { x, y: 5.6, w: 2.9, h: 0.4, fontSize: 16, bold: false, fontFace: "Georgia", color: C.accent1 });
    text(s, p[1], { x, y: 6.0, w: 2.9, h: 0.6, fontSize: 14 });
  });
}

// ===== 8 Innen =====
{
  const s = content("Große Gastro mit Bar, neu und modern", "Für die Stadt", "Konzeptskizze, Planung folgt mit dem Gastro-Fachplaner.");
  s.addImage({ path: path.join(IMG, "skizze_innen_konzept.png"), x: MX, y: 1.4, w: 8.2, h: 5.125, sizing: { type: "contain", w: 8.2, h: 5.125 }, altText: "Konzeptskizze: Grundriss der Gastro mit Bar, Wandansicht und Materialpalette" });
  s.addImage({ path: fit(hasKI("ki_innen_1.jpg") ? path.join(IMG, "ki_innen_1.jpg") : path.join(IMG, "innen.jpg"), 3.63, 2.43), x: 9.1, y: 1.4, w: 3.63, h: 2.43, altText: "Visualisierung Innenraum" });
  text(s, hasKI("ki_innen_1.jpg") ? "KI-Visualisierung" : "Referenz für Stimmung", { x: 9.1, y: 3.88, w: 3.63, h: 0.3, fontSize: 12, color: C.accent4 });
  [["ca. 100 Plätze", "innen, plus ca. 32 auf der Terrasse"], ["Bar", "10 Barhocker, Polsterbänke, Backbar"], ["Material", "Olivgrün, Cognac-Samt, Bordeaux, Eiche, schwarzer Stahl"]].forEach((p, i) => {
    text(s, p[0], { x: 9.1, y: 4.3 + i * 0.85, w: 3.63, h: 0.35, fontSize: 16, bold: false, fontFace: "Georgia", color: C.accent2 });
    text(s, p[1], { x: 9.1, y: 4.72 + i * 0.75, w: 3.63, h: 0.35, fontSize: 13 });
  });
}

// ===== 8b Visualisierungen (nur wenn KI-Bilder vorliegen) =====
if (KI.length) {
  const s = content("Visualisierungen", "Für die Stadt", "KI-Visualisierungen auf Basis der Skizzen, keine Planung.");
  const n = KI.length;
  const cols = n >= 5 ? 3 : n >= 3 ? 2 : n;
  const rowsN = Math.ceil(n / cols);
  const gw = (W - 2 * MX - (cols - 1) * 0.3) / cols;
  const gh = Math.min(gw * 0.62, (H - 2.65 - (rowsN - 1) * 0.3) / rowsN);
  KI.forEach((f, i) => {
    const x = MX + (i % cols) * (gw + 0.3);
    const y = 1.45 + Math.floor(i / cols) * (gh + 0.3);
    s.addImage({ path: fit(f, gw, gh), x, y, w: gw, h: gh, altText: "Visualisierung " + (i + 1) });
  });
  text(s, "KI-generierte Visualisierungen zur Orientierung, Maße und Details folgen mit dem Architekten.", { x: MX, y: H - 0.95, w: W - 2 * MX, h: 0.4, fontSize: 12, color: C.accent4 });
}

// ===== 9 Stellplätze =====
{
  const s = content("Stellplätze sind der Knackpunkt", "Für die Stadt", "Bedarf nach groben Annahmen (1,5 pro Wohnung, 1 je 10 m² Gastraum bei ca. 200 m²). Die Stellplatzsatzung der Stadt gilt verbindlich.");
  s.addChart(pres.charts.BAR, [{ name: "Stellplätze", labels: ["Bedarf (Annahme)", "Platz auf dem Grundstück"], values: [29, 12] }], {
    x: MX, y: 1.5, w: 5.8, h: 4.6, barDir: "col", chartColors: ["8C3B32", "2F4A3E"], varyColors: true, showValue: true, dataLabelPosition: "outEnd", dataLabelColor: "1F2421", dataLabelFontSize: 16, dataLabelFontFace: "+mn-lt",
    catAxisLabelColor: "1F2421", catAxisLabelFontSize: 14, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, showTitle: false, valAxisMaxVal: 36, valAxisMinVal: 0, objectName: "Diagramm Stellplätze",
  });
  text(s, "Vorschlag für die Stadt", { x: 7.0, y: 1.5, w: 5.7, h: 0.4, fontSize: 19, bold: false, fontFace: "Georgia", color: C.accent1 });
  text(s, [
    { text: "Bedarf ca. 29 Stellplätze, auf dem Grundstück passen ca. 10–13.", options: { bullet: true, breakLine: true } },
    { text: "Restplätze auf der öffentlichen Parkfläche nebenan (im Plan eingezeichnet) per Vereinbarung nutzen, besonders am Abend.", options: { bullet: true, breakLine: true } },
    { text: "Alternativ Ablöse statt Bau, die Höhe muss die Stadt nennen.", options: { bullet: true, breakLine: true } },
    { text: "Klären, ob der 10 m breite Grünstreifen teils befestigt werden darf.", options: { bullet: true } },
  ], { x: 7.0, y: 2.05, w: 5.7, h: 3.8, fontSize: 16, paraSpaceAfter: 10 });
}

// ===== 10 Kosten =====
{
  const s = content("Gesamtkosten ohne Förderung", "Für die Bank", "Baukosten 2.200 €/m² (Holz-Staffel 400 € günstiger) und 15 % Baunebenkosten sind Annahmen des Bauherrn und müssen durch Angebote von Bauunternehmen und Zimmerei bestätigt werden.");
  const fin = f0.plan;
  const rows = [
    [hdr("Posten"), hdr("Rechnung"), hdr("Betrag", "right")],
    [cell("Grundstück inkl. Steuer, Notar"), cell("960 m² × 230 € + ca. 7 %"), R(eur(A.grundstueck))],
    [cell("Bau, Massivbau"), cell("930 m² × 2.200 €"), R(eur(930 * A.bauKostenM2))],
    [cell("Abschlag Holzbau (Staffelgeschoss)"), cell("250 m² × 400 € günstiger"), R("− " + eur(250 * A.holzAbschlag))],
    [cell("Dachterrasse rundum"), cell("90 m² × 450 €"), R(eur(90 * A.terrassePreis))],
    [cell("Baunebenkosten (Architekt, Statik, Gebühren)"), cell("15 % vom Bau"), R(eur(bauRoh(v) * 0.15))],
    [cell("Gastro-Ausbau (Küche, Bar, Möbel, Technik)"), cell("Annahme, Posten im Anhang"), R(eur(v.gastroAusbau))],
    [cell("Gesamtkosten", { bold: true }), cell(""), R(eur(fin.gesamt), { bold: true })],
  ];
  s.addTable(rows, { x: MX, y: 1.5, w: 7.6, colW: [3.5, 2.4, 1.7], rowH: 0.5, border: tblBorder, objectName: "Tabelle Kosten" });
  s.addChart(pres.charts.DOUGHNUT, [{ name: "Kosten", labels: ["Grundstück", "Bau", "Baunebenkosten", "Gastro-Ausbau"], values: [A.grundstueck, bauRoh(v), bauRoh(v) * 0.15, v.gastroAusbau] }], {
    x: 8.5, y: 1.4, w: 4.3, h: 4.4, holeSize: 55, chartColors: ["C49A45", "8C3B32", "5B6770", "2F4A3E"], showPercent: true, showValue: false, dataLabelColor: "FFFFFF", dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt",
    showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: "1F2421", legendFontFace: "+mn-lt", showTitle: false, objectName: "Diagramm Kosten",
  });
  text(s, `Das sind ca. ${nf.format(Math.round(fin.gesamt / 930))} € pro m² BGF.`, { x: MX, y: 5.8, w: 7.6, h: 0.5, fontSize: 16, bold: true, color: C.accent2 });
}

// ===== 11 Finanzierung =====
{
  const s = content("Finanzierung zu 100 % ohne Eigenkapital", "Für die Bank", "Zinsen in der Bauzeit und im Aufschub werden dem Kredit zugeschlagen. Der Aufschub von 12 Monaten muss mit der Bank verhandelt werden.");
  const p = f0.plan;
  const au = f0.ausgang;
  const rows = [
    [hdr(""), hdr("Plan (3,3 %)", "right"), hdr("Ausgang (4,0 %)", "right")],
    [cell("Gesamtkosten"), R(eur(p.gesamt)), R(eur(au.gesamt))],
    [cell("Zinsen in der Bauzeit (15 Monate)"), R(eur(p.zinsenBau)), R(eur(au.zinsenBau))],
    [cell("Bereitstellungszinsen (3 % p. a. ab Monat 7)"), R(eur(p.bereit)), R(eur(au.bereit))],
    [cell("Zinsen im Aufschub-Jahr (keine Rate)"), R(eur(p.aufschubZinsen)), R(eur(au.aufschubZinsen))],
    [cell("Kredit bei Start der Rate", { bold: true }), R(eur(p.kredit), { bold: true }), R(eur(au.kredit), { bold: true })],
    [cell("Rate pro Monat (1 % Tilgung)", { bold: true }), R(eur(p.rate), { bold: true }), R(eur(au.rate), { bold: true })],
    [cell("   davon Zinsen"), R(eur(p.zinsAnteil)), R(eur(au.zinsAnteil))],
    [cell("   davon Tilgung (Rückzahlung der Schuld)"), R(eur(p.tilgAnteil)), R(eur(au.tilgAnteil))],
  ];
  s.addTable(rows, { x: MX, y: 1.5, w: 8.3, colW: [4.5, 1.9, 1.9], rowH: 0.5, border: tblBorder, objectName: "Tabelle Finanzierung" });
  card(s, 9.3, 1.5, W - 9.3 - MX, 4.5, "Hinweise");
  text(s, [
    { text: "Annahmen", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Baubeginn Mitte 2027, 15 Monate Bauzeit, gleichmäßiger Abruf.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Plan: 3,3 % Mischzins aus Förderkrediten (Annahme).", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Ausgang: 4,0 % bei 10 Jahren Zinsbindung (Stand 17.09.2026).", options: {} },
  ], { x: 9.55, y: 1.7, w: W - 9.3 - MX - 0.5, h: 4.0, fontSize: 14 });
}

// ===== 12 Cashflow =====
{
  const s = content("Was pro Monat übrig bleibt", "Für die Bank", "Mieten: 6 Wohnungen zu je 950 € Kaltmiete (Annahme des Bauherrn). Gastro-Marge nach Branchen-Richtwerten.");
  const c = f0.cfPlan;
  const rows = [
    [hdr(`Pro Monat, Plan, ohne Förderung, ${k(UM)} Umsatz`), hdr("Betrag", "right")],
    [cell("6 Wohnungen: je 950 € Kaltmiete"), R(eurS(v.mieteOhnePacht))],
    [cell(`Gastro-Pacht: ${v.gastroM2} m² × 12 €`), R(eurS(v.pacht))],
    [cell("Gastro-Gewinn nach Pacht"), R(eurS(c.gastroNachPacht))],
    [cell("Rate (Zinsen und Tilgung)"), R(eurS(-f0.plan.rate))],
    [cell("Dein Lohn (wird vorerst nicht gerechnet)"), R(eurS(-A.lohn))],
    [cell("Rücklagen (10 % der Miete und Pacht)"), R(eurS(-c.ruecklagen))],
    [cell("Ergebnis pro Monat", { bold: true }), cfCell(c.cf)],
  ];
  s.addTable(rows, { x: MX, y: 1.5, w: 7.2, colW: [5.3, 1.9], rowH: 0.5, border: tblBorder, objectName: "Tabelle Cashflow" });
  s.addChart(pres.charts.BAR, [{ name: "Euro pro Monat", labels: ["Miete", "Gastro", "Rate", "Rücklagen"], values: [c.miete, c.gastroNachPacht, -f0.plan.rate, -(A.lohn + c.ruecklagen)].map(Math.round) }], {
    x: 8.1, y: 1.4, w: 4.7, h: 4.3, barDir: "col", chartColors: ["2E7D5B", "2E7D5B", "B3261E", "B3261E"], varyColors: true, showValue: true, dataLabelFormatCode: "#,##0", dataLabelFontSize: 12, dataLabelColor: "1F2421", dataLabelFontFace: "+mn-lt",
    catAxisLabelColor: "1F2421", catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", catAxisLabelPos: "low", catAxisLabelRotate: 0, valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, showTitle: false, objectName: "Diagramm Cashflow",
  });
  text(s, "Ohne Lohn des Bauherrn. Die ca. 3.100 € Tilgung in der Rate sind Vermögensaufbau (Schuld sinkt), kein Verlust.", { x: MX, y: 6.0, w: 11.5, h: 0.4, fontSize: 14, color: C.accent4 });
}

// ===== 13 Szenarien Förderung x Zins =====
{
  const s = content("Förderung entscheidet über das Ergebnis", "Für Stadt und Bank", `Gastro-Umsatz ${k(UM)}. Förderung als Zuschuss in Prozent der Kosten, der den Kredit von Anfang an verkleinert (Annahme).`);
  const head = [hdr("Förderung"), hdr("Gesamtkosten", "right"), hdr("Rate (3,3 %)", "right"), hdr("Ergebnis (3,3 %)", "right"), hdr("Rate (4,0 %)", "right"), hdr("Ergebnis (4,0 %)", "right")];
  const rows = [head];
  FOERDERUNG.forEach((f) => rows.push([cell(pct(f), { bold: true }), R(eur(F[f].plan.gesamt)), R(eur(F[f].plan.rate)), cfCell(F[f].cfPlan.cf), R(eur(F[f].ausgang.rate)), cfCell(F[f].cfAusgang.cf)]));
  s.addTable(rows, { x: MX, y: 1.45, w: W - 2 * MX, colW: [1.5, 2.3, 2.1, 2.3, 2.1, 1.83], rowH: 0.44, border: tblBorder, objectName: "Tabelle Szenarien" });
  s.addChart(pres.charts.LINE, [
    { name: "Plan (3,3 %)", labels: FOERDERUNG.map(pct), values: FOERDERUNG.map((f) => Math.round(F[f].cfPlan.cf)) },
    { name: "Ausgang (4,0 %)", labels: FOERDERUNG.map(pct), values: FOERDERUNG.map((f) => Math.round(F[f].cfAusgang.cf)) },
  ], {
    x: MX, y: 4.75, w: 7.5, h: 2.15, chartColors: ["2F4A3E", "8C3B32"], lineSize: 3, lineDataSymbolSize: 7, catAxisLabelColor: "1F2421", catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisLabelColor: "1F2421", valAxisLabelFontSize: 11, valAxisLabelFontFace: "+mn-lt", valAxisLabelFormatCode: "#,##0",
    valGridLine: { color: "D9D9D9", size: 0.5 }, catGridLine: { style: "none" }, showLegend: true, legendPos: "r", legendFontSize: 11, legendColor: "1F2421", legendFontFace: "+mn-lt", showTitle: false, catAxisLabelPos: "low", objectName: "Diagramm Förderung",
  });
  text(s, `Pro 5 Prozentpunkte Förderung steigt das Ergebnis um ca. ${nf.format(Math.round(F[0.05].cfPlan.cf - F[0].cfPlan.cf))} € im Monat. Gastro-Umsatz ${k(UM)}, nach Rücklagen, ohne Lohn.`, { x: 8.4, y: 5.0, w: W - 8.4 - MX, h: 1.8, fontSize: 14 });
}

// ===== 14 Szenarien Umsatz =====
{
  const s = content("Wie viel Umsatz braucht die Gastro?", "Für die Bank", "Gastro-Marge vor Pacht 30,5 % vom Umsatz (Branchen-Richtwert, nicht aus Werlte). Break-even = Ergebnis (ohne Lohn des Bauherrn) genau null.");
  const ums = [40000, 45000, 50000, 55000, 60000];
  const fs = [0, 0.1, 0.15, 0.2];
  const rows = [[hdr("Ergebnis pro Monat (Plan 3,3 %)"), ...ums.map((u) => hdr(k(u), "right"))]];
  fs.forEach((f) => rows.push([cell(`Förderung ${pct(f)}`, { bold: true }), ...ums.map((u) => cfCell(cashflow(v, F[f].plan, u).cf))]));
  s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.6, ...ums.map(() => (W - 2 * MX - 3.6) / ums.length)], rowH: 0.55, border: tblBorder, objectName: "Tabelle Umsatz" });
  text(s, "Break-even-Umsatz (Ergebnis = 0, ohne Lohn)", { x: MX, y: 4.5, w: 8, h: 0.4, fontSize: 18, bold: true, color: C.accent2 });
  const be = [[hdr("Förderung"), ...fs.map((f) => hdr(pct(f), "right"))],
    [cell("Plan, 3,3 %"), ...fs.map((f) => R(eur(umsatzBreakEven(v, F[f].plan))))],
    [cell("Ausgang, 4,0 %"), ...fs.map((f) => R(eur(umsatzBreakEven(v, F[f].ausgang))))]];
  s.addTable(be, { x: MX, y: 5.0, w: W - 2 * MX, colW: [3.6, ...fs.map(() => (W - 2 * MX - 3.6) / fs.length)], rowH: 0.5, border: tblBorder, objectName: "Tabelle Break-even" });
}

// ===== 15 Pfad zu Plus =====
{
  const s = content("Der Weg zu Plus: Hebel nacheinander", "Für Stadt und Bank", "Startpunkt ist die vorsichtige Annahme von 40.000 € Umsatz ohne Förderung. Die Hebel sind Ziele für die Verhandlung, keine Zusagen.");
  const steps = [
    ["Ausgangslage (40.000 € Umsatz, keine Förderung)", {}],
    ["+ 15 % Förderung", { f: 0.15 }],
    ["+ Baukosten 2.000 €/m² statt 2.200 € (Bekanntenpreis)", { bau: 2000 }],
    ["+ Gastro-Ausbau nur 100.000 € statt 150.000 €", { ausbau: 100000 }],
    ["+ Gastro-Umsatz 45.000 €", { u: 45000 }],
    ["+ Tilgung 0 % (nur Zinsen) in den ersten Jahren", { til: 0 }],
  ];
  let st = { f: 0, bau: A.bauKostenM2, ausbau: v.gastroAusbau, u: 40000, til: A.tilgung };
  const rows = [[hdr("Schritt"), hdr("Plan (3,3 %)", "right"), hdr("Ausgang (4,0 %)", "right")]];
  const vals = [];
  steps.forEach(([n, d]) => {
    st = Object.assign({}, st, d);
    const row = [n];
    [A.zinsPlan, A.zinsAusgang].forEach((z) => {
      const fin = finanz(v, st.f, z, { bauKostenM2: st.bau, gastroAusbau: st.ausbau, tilgung: st.til });
      row.push(cashflow(v, fin, st.u).cf);
    });
    vals.push(row);
    rows.push([cell(n), cfCell(row[1]), cfCell(row[2])]);
  });
  s.addTable(rows, { x: MX, y: 1.4, w: 8.4, colW: [5.2, 1.6, 1.6], rowH: 0.52, border: tblBorder, objectName: "Tabelle Pfad" });
  card(s, 9.4, 1.4, W - 9.4 - MX, 4.7, "Fazit Pfad");
  text(s, [
    { text: "Mindestpaket", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Ohne Lohn des Bauherrn liegt schon die Ausgangslage mit 40.000 € Umsatz im Plus, Förderung und günstige Preise geben zusätzlichen Puffer.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Nur Konto, kein Gewinn", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Tilgung 0 % verbessert das Konto, nicht das Haus.", options: {} },
  ], { x: 9.65, y: 1.6, w: W - 9.4 - MX - 0.5, h: 4.4, fontSize: 14 });
  text(s, "Verwaltung, Versicherung, Grundsteuer (ca. 300–500 € im Monat) sind noch nicht enthalten.", { x: MX, y: 5.8, w: 8.4, h: 0.5, fontSize: 13, color: C.accent4 });
}

// ===== 15b Verkauf an die Familie =====
{
  const s = content("Verkauf an die Familie: Rechnung je Partei", "Für die Verwandten und die Bank", "Jede Partei bekommt einen eigenen Kredit ohne Eigenkapital. Preis = Selbstkosten, 3,3 % Zins, 1 % Tilgung, Miete 950 €, 10 % Rücklagen.");
  const t = teilung(LAYOUTS.A);
  const o = t.oG(85, 950), st = t.st(56, 950), g = t.gastro;
  const rows = [
    [hdr(""), hdr("1. OG, 85 m² (3×)", "right"), hdr("Staffel, 56 m² (3×)", "right"), hdr("Du: Gastro im EG", "right")],
    [cell("Preis (Selbstkosten)"), R(eur(o.kosten)), R(eur(st.kosten)), R(eur(g.kosten))],
    [cell("Preis je m² Wohnfläche"), R(eur(o.kostenM2)), R(eur(st.kostenM2)), R("")],
    [cell("Rate pro Monat (3,3 % + 1 % Tilgung)"), R(eur(o.rate)), R(eur(st.rate)), R(eur(g.rate))],
    [cell("Einnahme pro Monat (nach 10 % Rücklagen)"), R(eur(o.miete * 0.9)), R(eur(st.miete * 0.9)), R(eur(g.gewinn))],
    [cell("Ergebnis pro Monat", { bold: true }), cfCell(o.ergebnis), cfCell(st.ergebnis), cfCell(g.ergebnis)],
    [cell("Preis, bei dem das Ergebnis 0 € ist"), R(eur(o.preisFuerPlus)), R(eur(st.preisFuerPlus)), R("")],
    [cell("Lücke zum Selbstkostenpreis (ohne Eigenkapital)"), R(eur(o.luecke)), R(eur(st.luecke)), R("")],
    [cell("Ergebnis mit 15 % Förderung"), cfCell(o.ergebnisF15), cfCell(st.ergebnisF15), R("")],
  ];
  s.addTable(rows, { x: MX, y: 1.4, w: W - 2 * MX, colW: [4.4, 2.6, 2.6, 2.53], rowH: 0.44, border: tblBorder, objectName: "Tabelle Verkauf je Partei" });
  text(s, [
    { text: `Die Rechnung für den Gastro-Teil gilt bei ${k(UM)} Umsatz ohne Lohn des Bauherrn, Break-even ab ${k(Math.round(g.beUmsatz / 1000) * 1000)}. Die Wohnungen tragen sich bei 11,18 €/m² Miete erst ab einem Preis von ca. ${eur(Math.round(t.preisFuerPlusM2 / 10) * 10)} je m².`, options: { breakLine: true } },
    { text: `Die Staffel-Wohnung (56 m²) kostet bei 950 € Miete 17 €/m², bei Marktmiete (11,18 €/m²) wären es ${eur(56 * 11.18)} und das Ergebnis ${eurS(t.st(56).ergebnis)}.`, options: {} },
  ], { x: MX, y: 5.65, w: W - 2 * MX, h: 1.1, fontSize: 12.5, color: C.accent4, paraSpaceAfter: 4 });
}

// ===== 15c So rentiert es sich für jede Partei =====
{
  const s = content("So rentiert es sich für jede Partei", "Für die Verwandten und die Bank", "Variante A, 6 Wohnungen, jede mit eigenem Kredit ohne Eigenkapital, Miete 950 €, 50.000 € Gastro-Umsatz. Förderung, Preise und tilgungsfreie Jahre sind Ziele, keine Zusagen.");
  const t0 = teilung(LAYOUTS.A, A.zinsPlan);
  const calc = (o) => {
    const z = o.zins ?? A.zinsPlan, c = o.c ?? A.bauKostenM2, f = o.f ?? 0, til = o.til ?? A.tilgung;
    const t = teilung(LAYOUTS.A, z, { bauKostenM2: c });
    const rate = (kosten) => (kosten * (1 - f) * t.k * (z + til)) / 12;
    const og = 950 * (1 - A.ruecklagen) - rate(t.oG(85, 950).kosten);
    const st = 950 * (1 - A.ruecklagen) - rate(t.st(56, 950).kosten);
    const g = UM * A.gastroMargeVorPacht - A.lohn - rate(t.gastro.kosten);
    return [og, st, g];
  };
  const sc = [
    ["Selbstkostenpreis, 1 % Tilgung (heute)", {}],
    ["+ 15 % Förderung", { f: 0.15 }],
    ["+ Tilgung 0 % (nur Zinsen) in den ersten Jahren", { f: 0.15, til: 0 }],
    ["+ Baukosten 2.000 €/m² statt 2.200 €", { f: 0.15, til: 0, c: 2000 }],
    ["Dasselbe bei 4,0 % Zins", { f: 0.15, til: 0, c: 2000, zins: A.zinsAusgang }],
    ["Alternative: ohne Förderung, Tilgung 0 %, Baukosten 2.000 €/m²", { til: 0, c: 2000 }],
  ];
  const rows = [[hdr("Schritt"), hdr("1. OG, 85 m²", "right"), hdr("Staffel, 56 m²", "right"), hdr("Du: Gastro", "right")]];
  sc.forEach(([n, o]) => {
    const r = calc(o);
    rows.push([cell(n), cfCell(r[0]), cfCell(r[1]), cfCell(r[2])]);
  });
  s.addTable(rows, { x: MX, y: 1.4, w: 8.6, colW: [4.3, 1.4, 1.5, 1.4], rowH: 0.52, border: tblBorder, objectName: "Tabelle Rentiert für alle" });
  card(s, 9.5, 1.4, W - 9.5 - MX, 4.9, "Was das bedeutet");
  text(s, [
    { text: "Plus für alle", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Förderung 15 % und tilgungsfreie Jahre reichen bei 3,3 % Zins für ein Plus bei jeder Partei. Bei 4,0 % Zins fehlt dem OG trotz 2.000 €/m² noch ein kleines Stück, dann braucht es mehr Förderung oder noch günstigere Preise.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Zu beachten", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Ohne Tilgung sinkt die Schuld nicht, der Kredit muss später abgelöst oder verlängert werden.", options: {} },
  ], { x: 9.75, y: 1.6, w: W - 9.5 - MX - 0.5, h: 4.5, fontSize: 12.5 });
  text(s, `Zum Vergleich: Wenn du die Lücke der drei OG-Wohnungen (${eur(3 * -t0.oG(85, 950).ergebnis)} im Monat) selbst trägst, bleiben dir ${eur(t0.gastro.ergebnis + 3 * t0.oG(85, 950).ergebnis)} aus der Gastro.`, { x: MX, y: 5.7, w: 8.6, h: 0.7, fontSize: 12.5, color: C.accent4 });
}

// ===== 16 Risiken =====
{
  const s = content("Risiken und was wir dagegen tun", "Für die Bank", "Die Miete von 950 € je Wohnung ist eine Annahme des Bauherrn, Marktdaten für Werlte liegen darunter.");
  const items = [
    ["Miete", "950 € je Wohnung (ca. 12–15 €/m²) liegt über den Portalwerten für Neubau in Werlte (ca. 11 €/m²). Gegenmaßnahme: Vergleichsangebote, Vorvermietung."],
    ["Gastro-Umsatz", `Die Gastro braucht ab ca. ${k(Math.round(umsatzBreakEven(v, f0.plan) / 1000) * 1000)} Umsatz, bei 4 % Zins ca. ${k(Math.round(umsatzBreakEven(v, f0.ausgang) / 1000) * 1000)}. Gegenmaßnahme: Konzept, Pacht-Staffel, Lohn des Bauherrn bewusst ausgeklammert.`],
    ["Zins", "Nach 10 Jahren Zinsbindung ist der Folgezins offen. Gegenmaßnahme: Förderkredite, Forward-Darlehen, Tilgungsaussetzung."],
    ["Genehmigung", "Staffelgeschoss und Flachdach müssen von der Stadt bestätigt werden. Gegenmaßnahme: Vorabstimmung, Plan B mit Satteldach."],
  ];
  const cw = (W - 2 * MX - 0.4) / 2;
  items.forEach((it, i) => {
    const x = MX + (i % 2) * (cw + 0.4);
    const y = 1.5 + Math.floor(i / 2) * 2.55;
    card(s, x, y, cw, 2.3, "Risiko " + (i + 1));
    text(s, it[0], { x: x + 0.25, y: y + 0.15, w: cw - 0.5, h: 0.45, fontSize: 19, bold: false, fontFace: "Georgia", color: C.accent1 });
    text(s, it[1], { x: x + 0.25, y: y + 0.7, w: cw - 0.5, h: 1.5, fontSize: 14 });
  });
}

// ===== 17 Forderungen an die Stadt =====
{
  const s = content("Was ich von der Stadt brauche", "Für die Stadt", "Wirkungen gerechnet mit dem Modell (Plan 3,3 %, ohne Förderung als Basis).");
  const eff10 = F[0.1].cfPlan.cf - F[0].cfPlan.cf;
  const effLand = f0.plan.rate - finanz(v, 0, A.zinsPlan, { grundstueck: A.grundstueck - 960 * 30 * 1.07 }).rate;
  const effZins = f0.plan.rate - finanz(v, 0, A.zinsPlan - 0.005).rate;
  const items = [
    ["Städtebauförderung", `10 % Förderung bringen ca. ${eurS(eff10)} im Monat`],
    ["Grundstückspreis", `30 € weniger pro m² bringen ca. ${eurS(effLand)} im Monat`],
    ["Pacht oder Mietzuschuss", "1.000 € Zuschuss im Monat sind 1.000 € mehr im Monat"],
    ["Stellplätze", "Mitnutzung der öffentlichen Parkfläche oder faire Ablöse"],
    ["Genehmigung", "Staffelgeschoss, Flachdach und Höhe schriftlich bestätigen"],
    ["Zinsvorteil", `0,5 % weniger Zins bringen ca. ${eurS(effZins)} im Monat`],
  ];
  const cw = (W - 2 * MX - 0.4) / 2;
  items.forEach((it, i) => {
    const x = MX + (i % 2) * (cw + 0.4);
    const y = 1.5 + Math.floor(i / 2) * 1.65;
    card(s, x, y, cw, 1.45, "Forderung " + (i + 1));
    text(s, it[0], { x: x + 0.25, y: y + 0.15, w: cw - 0.5, h: 0.45, fontSize: 19, bold: false, fontFace: "Georgia", color: C.accent1 });
    text(s, it[1], { x: x + 0.25, y: y + 0.65, w: cw - 0.5, h: 0.7, fontSize: 14 });
  });
}

// ===== 18 Nächste Schritte =====
{
  const s = content("Nächste Schritte", "Für Stadt und Bank", "Zeitplan der Stadt aus dem Konzeptheft, Bauantrag und Förderzusagen sind meine Planung.");
  const steps = [
    ["Okt 2026", "Gespräch mit der Stadt: Preis, Förderung, Stellplätze"],
    ["Nov 2026", "Architekt, Baufenster, Höhen und Geschosse schriftlich klären"],
    ["Dez 2026", "Bank: Finanzierung, Aufschub, Förderkredite anfragen"],
    ["Q1 2027", "Städtebaulicher Vertrag, Bauantrag"],
    ["Mitte 2027", "Baubeginn, 15 Monate Bauzeit"],
    ["Ende 2028", "Eröffnung zusammen mit der neuen Mitte"],
  ];
  steps.forEach((t, i) => {
    const y = 1.5 + i * 0.85;
    s.addShape(pres.ShapeType.ellipse, { x: MX, y, w: 0.55, h: 0.55, fill: { color: i === 5 ? C.accent1 : C.accent2 }, line: { color: C.background1, width: 1 }, objectName: "Schritt " + (i + 1) });
    text(s, String(i + 1), { x: MX, y, w: 0.55, h: 0.55, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle" });
    text(s, t[0], { x: MX + 0.85, y: y + 0.02, w: 2.0, h: 0.5, fontSize: 18, bold: true, color: C.accent1, valign: "middle" });
    text(s, t[1], { x: MX + 2.9, y: y + 0.02, w: 9, h: 0.5, fontSize: 16, valign: "middle" });
  });
}

// ===== Anhang =====
{
  const s = pres.addSlide({ masterName: "TITEL" });
  text(s, "Anhang", { x: MX, y: 2.8, w: 10, h: 1.2, fontSize: 41, bold: false, fontFace: "Georgia", color: C.background1 });
  text(s, "Annahmen, Gastro-Kosten, Gastro-Ausbau, Mietdaten, Variante B, Variante mit vier Ebenen", { x: MX, y: 4.1, w: 10, h: 0.6, fontSize: 18, color: "CFD8D3" });
}
{
  const s = content("Rechenannahmen und offene Punkte", "Anhang", "Alle Zahlen sind Planungsannahmen, keine Zusagen.");
  const left = [
    "Grundstück 960 m² × 230 € plus ca. 7 % (5 % Grunderwerbsteuer, ca. 2 % Notar)",
    "Bau 930 m² BGF × 2.200 €, Staffel in Holzbau 400 €/m² günstiger, Terrasse 90 m² × 450 €, Baunebenkosten 15 %",
    "100 % Fremdfinanzierung, 1 % Tilgung, Aufschub 12 Monate",
    "Bauzeit 15 Monate, Bereitstellungszins 3 % p. a. ab Monat 7",
    "Zins Plan 3,3 % (Förderkredite, Annahme), Ausgang 4,0 %",
  ];
  const right = [
    `Gastro-Umsatz ${k(UM)} netto, Marge vor Pacht 30,5 %`,
    "6 Wohnungen zu je 950 € Kaltmiete, Gastro-Pacht 12 €/m²",
    "Lohn des Bauherrn wird vorerst nicht gerechnet, Rücklagen 10 % der Miete und Pacht",
    "Förderung als Zuschuss in % der Gesamtkosten (Annahme)",
    "Nicht enthalten: Hausverwaltung, Versicherung, Grundsteuer (ca. 300–500 €/Monat)",
    "Offen: Baufenster, Staffelgeschoss, Höhen, Stellplatzsatzung, Zins nach 10 Jahren",
  ];
  const cw = (W - 2 * MX - 0.5) / 2;
  [left, right].forEach((arr, kk) => text(s, arr.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < arr.length - 1 } })), { x: MX + kk * (cw + 0.5), y: 1.5, w: cw, h: 4.8, fontSize: 15, paraSpaceAfter: 12 }));
}
{
  const s = content(`Gastro: Kosten pro Monat bei ${k(UM)} Umsatz`, "Anhang", "Prozentwerte sind Branchen-Richtwerte aus meiner Einschätzung, nicht aus Quellen für Werlte.");
  const pctOf = (p) => Math.round(UM * p);
  const base = [
    ["Wareneinsatz (Einkauf Essen und Getränke)", "ca. 28 %", pctOf(0.28)],
    ["Personal (ohne Chef-Lohn)", "ca. 30 %", pctOf(0.3)],
    [`Pacht ans Haus (${v.gastroM2} m² × 12 €)`, "", v.pacht],
    ["Energie, Wasser, Müll", "ca. 3 %", pctOf(0.03)],
    ["Reinigung, Wäsche, Verbrauchsmaterial", "ca. 2 %", pctOf(0.02)],
    ["Werbung und Marketing", "ca. 1,5 %", pctOf(0.015)],
    ["Reparaturen, Wartung, Kassensystem", "ca. 1,5 %", pctOf(0.015)],
    ["Sonstiges", "ca. 1,5 %", pctOf(0.015)],
    ["Versicherungen, GEMA, Gebühren", "ca. 1 %", pctOf(0.01)],
    ["Steuerberater, Buchhaltung", "ca. 1 %", pctOf(0.01)],
  ];
  const sum = base.reduce((a, r) => a + r[2], 0);
  const rows = [[hdr("Posten"), hdr("Richtwert", "right"), hdr("Betrag", "right")], ...base.map((r) => [cell(r[0]), R(r[1]), R(eur(r[2]))]),
    [cell("Summe Kosten", { bold: true }), cell(""), R(eur(sum), { bold: true })],
    [cell("Gewinn nach Pacht, vor Lohn", { bold: true }), cell(""), R(eur(UM - sum), { bold: true })]];
  s.addTable(rows, { x: MX, y: 1.4, w: W - 2 * MX, colW: [7.0, 2.5, 2.63], rowH: 0.405, border: tblBorder, objectName: "Tabelle Gastro-Kosten" });
}
{
  const s = content("Gastro-Ausbau nach Posten", "Anhang", "Zielbudget des Bauherrn für einen einfachen Ausbau, Angebote von Küchen- und Lüftungsbauern müssen es bestätigen.");
  const items = [
    ["Küche (Herd, Kühlräume, Edelstahl, Spülküche)", 30000],
    ["Lüftung und Abluft", 18000],
    ["Theke und Bar (Zapfanlage, Kühlung, Backbar)", 20000],
    ["Möbel (ca. 100 Plätze, Lounge)", 28000],
    ["Beleuchtung und Deko", 8000],
    ["Wand, Boden, Decke, Akustik", 15000],
    ["Gäste-WC Ausstattung", 5000],
    ["Kasse, Technik, Musik, WLAN", 5000],
    ["Terrasse (Holzdeck, Möbel, Heizstrahler)", 6000],
    ["Planung und Genehmigung", 5000],
    ["Eröffnung, Marketing, Warenerstbestückung", 3000],
  ];
  const sumN = items.reduce((a, r) => a + r[1], 0);
  const rows = [[hdr("Posten"), hdr("Betrag", "right")], ...items.map((r) => [cell(r[0]), R(eur(r[1]))]),
    [cell("Puffer 5 %"), R(eur(sumN * 0.05))],
    [cell("Summe (im Modell: 150.000 €)", { bold: true }), R(eur(sumN * 1.05), { bold: true })]];
  s.addTable(rows, { x: MX, y: 1.35, w: 8.0, colW: [6.0, 2.0], rowH: 0.34, border: tblBorder, objectName: "Tabelle Gastro-Ausbau" });
  card(s, 9.0, 1.35, W - 9.0 - MX, 3.2, "Hinweis Ausbau");
  text(s, "Baunebenkosten von 15 % fallen auf Möbel und Geräte nicht an, die Planung steckt als eigener Posten drin. Eine erste Schätzung für einen aufwendigeren Ausbau lag bei ca. 310.000 €, der Unterschied liegt vor allem bei Küche, Möbeln und Theke.", { x: 9.25, y: 1.55, w: W - 9.0 - MX - 0.5, h: 2.8, fontSize: 14 });
}
{
  const s = content("Mietdaten für Werlte", "Anhang", "Es gibt keinen amtlichen Mietspiegel für Werlte, die Portale arbeiten mit kleinen Stichproben.");
  const rows = [
    [hdr("Quelle"), hdr("Wert für Werlte", "right")],
    [cell("ImmoScout24 (Wohnungen, Durchschnitt)"), R("7,78 €/m²")],
    [cell("miete-aktuell.de (Kaltmiete 2026)"), R("8,13 €/m²")],
    [cell("mietpreise.info (14 Inserate, Spanne 6,09–14,48 €)"), R("9,58 €/m²")],
    [cell("mietpreise.info (Neubau)"), R("10,73–11,02 €/m²")],
    [cell("Landkreis Emsland (ImmoScout24, Q2 2026)"), R("8,10 €/m²")],
  ];
  s.addTable(rows, { x: MX, y: 1.5, w: 8.6, colW: [6.0, 2.6], rowH: 0.55, border: tblBorder, objectName: "Tabelle Mieten" });
  card(s, 9.6, 1.5, W - 9.6 - MX, 3.6, "Annahme Miete");
  text(s, [
    { text: "Im Modell", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "6 Wohnungen zu 950 € Kaltmiete (Bauherr, zentrale Lage), das sind bei ca. 75 m² etwa 12,70 €/m². Gastro-Pacht 12 €/m² ohne Marktdaten." },
  ], { x: 9.85, y: 1.7, w: W - 9.6 - MX - 0.5, h: 3.2, fontSize: 14 });
  text(s, "Quellen: mietpreise.info/mietspiegel/werlte, miete-aktuell.de, immobilienscout24.de (Kreis Emsland), Abruf Oktober 2026", { x: MX, y: 5.4, w: W - 2 * MX, h: 0.6, fontSize: 12, color: C.accent4 });
}

// ===== Varianten B und C: 540 m² Grundfläche =====
{
  const s = content("Varianten B und C: 540 m² Grundfläche", "Anhang", "Nur mit Ausnahme der Stadt: Baufenster ca. 400–460 m² geschätzt, im Plan stehen zwei Vollgeschosse und 12 m Höhe, GRZ 0,6 erlaubt max. 576 m².");
  const vb = VARIANTEN.b, vc = VARIANTEN.c;
  const fa = finanz(v, 0, A.zinsPlan), fb = finanz(vb, 0, A.zinsPlan), fc = finanz(vc, 0, A.zinsPlan);
  const ca = cashflow(v, fa), cb = cashflow(vb, fb), cc = cashflow(vc, fc);
  const ta = teilung(LAYOUTS.A), tb = teilung(LAYOUTS.B), tc = teilung(LAYOUTS.C);
  const rows = [
    [hdr(""), hdr("A: 340 m², 2+Staffel", "right"), hdr("B: 540 m², 2+Staffel", "right"), hdr("C: 540 m², 3+Holz-Penthouse", "right")],
    [cell("Bruttofläche"), R("930 m²"), R("1.500 m²"), R("2.040 m²")],
    [cell("Wohnfläche / Wohnungen"), R("423 m² / 6"), R("738 m² / ca. 8–9"), R("1.153 m² / ca. 13")],
    [cell("Gastro / Büro im EG"), R("290 m² / –"), R("290 m² / 150 m²"), R("290 m² / 150 m²")],
    [cell("Gesamtkosten"), R(eur(fa.gesamt)), R(eur(fb.gesamt)), R(eur(fc.gesamt))],
    [cell("Rate pro Monat (ein Kredit)"), R(eur(fa.rate)), R(eur(fb.rate)), R(eur(fc.rate))],
    [cell(`Ergebnis bei ${k(UM)} Umsatz`), cfCell(ca.cf), cfCell(cb.cf), cfCell(cc.cf)],
    [cell("Break-even-Umsatz Gastro"), R(eur(umsatzBreakEven(v, fa))), R(eur(umsatzBreakEven(vb, fb))), R(eur(umsatzBreakEven(vc, fc)))],
    [cell("Ergebnis bei 4,0 % Zins"), cfCell(cashflow(v, finanz(v, 0, A.zinsAusgang)).cf), cfCell(cashflow(vb, finanz(vb, 0, A.zinsAusgang)).cf), cfCell(cashflow(vc, finanz(vc, 0, A.zinsAusgang)).cf)],
    [cell("Kosten je m² Wohnfläche, Regelgeschoss / Staffel"), R(`${eur(ta.ogM2)} / ${eur(ta.stM2)}`), R(`${eur(tb.ogM2)} / ${eur(tb.stM2)}`), R(`${eur(tc.ogM2)} / ${eur(tc.stM2)}`)],
    [cell("85-m²-Wohnung im Regelgeschoss: Ergebnis (eigener Kredit)"), cfCell(ta.oG(85, 950).ergebnis), cfCell(tb.oG(85, 950).ergebnis), cfCell(tc.oG(85, 950).ergebnis)],
    [cell("Preis-Lücke je 85-m²-Wohnung im Regelgeschoss"), R(eur(ta.oG(85, 950).luecke)), R(eur(tb.oG(85, 950).luecke)), R(eur(tc.oG(85, 950).luecke))],
  ];
  s.addTable(rows, { x: MX, y: 1.4, w: 9.0, colW: [3.9, 1.7, 1.7, 1.7], rowH: 0.42, border: tblBorder, objectName: "Tabelle Varianten B und C" });
  card(s, 10.2, 1.4, W - 10.2 - MX, 5.0, "Hinweis B und C");
  text(s, [
    { text: "Annahmen", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "EG 540 m² (Gastro 290 m², Büro 150 m²), Regelgeschosse je 540 m², Staffel 420 m² in Holzbau mit 120 m² Terrasse. Büro 10 €/m², Wohnen 11,18 €/m².", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Zu klären", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Baufenster, zwei Vollgeschosse, bei C drei Vollgeschosse und ca. 13 m Höhe statt 12 m, deutlich mehr Stellplätze.", options: {} },
  ], { x: 10.4, y: 1.6, w: W - 10.2 - MX - 0.4, h: 4.6, fontSize: 12 });
}

// ===== 8c Variante mit zweitem Mittelgeschoss =====
if (hasKI("ki_aussen_4etagen.jpg")) {
  const s = content("Variante: Mittelgeschoss doppelt, vier Ebenen", "Anhang", "Bildmontage aus der KI-Visualisierung: das mittlere Geschoss wurde verdoppelt. Höhe ca. 13 m, der B-Plan erlaubt 12 m.");
  s.addImage({ path: path.join(IMG, "ki_aussen_4etagen.jpg"), x: MX, y: 1.4, w: 7.0, h: 4.46, sizing: { type: "contain", w: 7.0, h: 4.46 }, altText: "Bildmontage: Gebäude mit doppeltem Mittelgeschoss, vier Ebenen" });
  text(s, "Bildmontage, keine neue Planung", { x: MX, y: 5.9, w: 7.0, h: 0.3, fontSize: 12, color: C.accent4 });
  const v4 = Object.assign({}, v, { bgf: 1270, mieteOhnePacht: 9 * 950 });
  const g0 = finanz(v4, 0, A.zinsPlan);
  const g15 = finanz(v4, 0.15, A.zinsPlan);
  const rows = [
    [hdr(""), hdr("3 Ebenen", "right"), hdr("4 Ebenen", "right")],
    [cell("Wohnungen"), R("6"), R("9")],
    [cell("BGF"), R("930 m²"), R("1.270 m²")],
    [cell("Gesamtkosten"), R(eur(f0.plan.gesamt)), R(eur(g0.gesamt))],
    [cell("Rate (Plan)"), R(eur(f0.plan.rate)), R(eur(g0.rate))],
    [cell(`Ergebnis bei ${k(UM)} Umsatz`), cfCell(f0.cfPlan.cf), cfCell(cashflow(v4, g0).cf)],
    [cell("… mit 15 % Förderung"), cfCell(F[0.15].cfPlan.cf), cfCell(cashflow(v4, g15).cf)],
    [cell("Break-even-Umsatz, 15 % Förderung"), R(eur(umsatzBreakEven(v, F[0.15].plan))), R(eur(umsatzBreakEven(v4, g15)))],
  ];
  s.addTable(rows, { x: 7.9, y: 1.5, w: W - 7.9 - MX, colW: [2.2, 1.3, 1.33], rowH: 0.5, border: tblBorder, objectName: "Tabelle Vergleich 3 und 4 Ebenen" });
  text(s, `Das zweite Mittelgeschoss bringt 3 weitere Wohnungen zu 950 €, kostet aber ca. ${((g0.gesamt - f0.plan.gesamt) / 1e6).toFixed(2).replace(".", ",")} Mio. € mehr. Die Höhe von ca. 13 m braucht eine Ausnahme von der Stadt (B-Plan: 12 m).`, { x: 7.9, y: 6.0, w: W - 7.9 - MX, h: 1.0, fontSize: 13, color: C.accent4 });
}

(async () => {
  const file = path.join(OUT, "Neue-Mitte-Werlte_Baufeld3_6-Wohnungen_Gastro-EG.pptx");
  await pres.writeFile({ fileName: file });
  await applyTheme(file, THEME);
  console.log("geschrieben", file);
})();
