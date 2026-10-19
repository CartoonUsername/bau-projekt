// Deck: Neue Mitte Werlte, Baufeld 3. 6 Wohnungen, große Gastro im ganzen EG, 576 m² Grundfläche, 1.650 m² BGF, 2 Büro-Ankermieter, Flachdach mit Staffelgeschoss in Holzbau
// Aufruf: NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_deck_sechs.js
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");
const { A, VARIANTEN, finanz, cashflow, umsatzBreakEven, bauRoh, teilung, zielplus, verkaufsplan, LAYOUTS, kfw } = require("./model");
const { execFileSync } = require("child_process");

const B = JSON.parse(fs.readFileSync(path.join(__dirname, "bank_values.json"), "utf8"));
const IMG = process.env.BILDER || path.join(__dirname, "bilder");
const OUT = process.env.OUT || __dirname;
const v = VARIANTEN.sechs;
const UM = v.umsatz; // Basis-Umsatz 65.000 €
// KI-Bilder (optional): werden automatisch eingebaut, wenn die Dateien in bilder/ liegen
const KI = ["ki_aussen_1.jpg", "ki_aussen_2.jpg", "ki_terrasse.jpg", "ki_gastro_raum.jpg", "ki_gastro_bar.jpg"].map((n) => path.join(IMG, n)).filter((f) => fs.existsSync(f));
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
const eur2 = (n) => `${new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n)} €`;
const pct2 = (n) => `${(n * 100).toFixed(2).replace(".", ",")} %`;
const fm1 = (n) => new Intl.NumberFormat("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(n);
const mio = (n) => `${(n / 1e6).toFixed(2).replace(".", ",")} Mio. €`;
const k = (n) => `${nf.format(n)} €`;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Neue Mitte Werlte – Baufeld 3: Große Gastro und 6 Wohnungen";
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
  text(s, "Businessplan für die Bank: Konzept, Finanzierung mit KfW-Krediten, Ertragswert und Abzahlungsplan", { x: MX, y: 4.3, w: 6, h: 0.9, fontSize: 17, color: C.background1 });
  text(s, "Bessam Hasso, Werlte\nBebauungsplan Nr. 123, 1. Änderung (Entwurf 25.08.2026)\nStand Oktober 2026", { x: MX, y: 5.5, w: 6, h: 1.1, fontSize: 14, color: "CFD8D3" });
  s.addNotes("Titelfolie. Das Bild ist eine Referenzstudie.");
}

// ===== 2 Überblick =====
{
  const s = content("Das Vorhaben auf einen Blick", "Für Stadt und Bank", "Alle Zahlen stammen aus dem Rechenmodell Bankunterlagen_Baufeld3.xlsx und sind Planungsannahmen.");
  const w = (W - 2 * MX - 0.6) / 4;
  stat(s, MX, 1.5, w, mio(B.k_gesamt), "Gesamtkosten inkl. Finanzierung in Bau- und Anlaufzeit");
  stat(s, MX + (w + 0.2), 1.5, w, pct(B.kredit_kfw_anteil), "des Darlehens über KfW 297, 298, 299 (" + mio(B.kredit_297 + B.kredit_298 + B.kredit_299) + ")", C.accent2);
  stat(s, MX + 2 * (w + 0.2), 1.5, w, eur(B.rate_monat), "Kapitaldienst pro Monat (Mischzins " + (B.mischzins * 100).toFixed(2).replace(".", ",") + " %, 1 % Tilgung)", C.accent4);
  stat(s, MX + 3 * (w + 0.2), 1.5, w, eurS(B.c_ergebnis), "Ergebnis pro Monat nach Kapitaldienst, ohne Lohn", B.c_ergebnis >= 0 ? C.accent5 : C.accent6);
  const rows = [[hdr("Projekt"), hdr("Wert")],
    [cell("Grundstück / Grundfläche / BGF"), cell("960 m² / 576 m² (32 × 18 m, GRZ-Maximum) / 1.650 m² (EG, 1. OG, Staffel)")],
    [cell("Nutzung"), cell("Gastro im ganzen EG (ca. 510 m²), im 1. OG 2 Büro-Ankermieter (100 und 65 m²) und 3 Wohnungen, im Staffelgeschoss in Holzbau 3 Wohnungen")],
    [cell("Finanzierung"), cell("100 % Fremdkapital, kein Eigenkapital, KfW 297/298/299 plus Hausbank")],
    [cell("Kapitaldienstdeckung (DSCR)"), cell(B.dscr.toFixed(2).replace(".", ",") + " gesamt, " + B.dscr_immo.toFixed(2).replace(".", ",") + " nur Immobilie (Miete und Pacht)")],
    [cell("Ertragswert / Beleihungsauslauf"), cell(mio(B.ertragswert) + " / " + pct(B.auslauf) + " (Darlehen zu Beleihungswert)")]];
  s.addTable(rows, { x: MX, y: 3.45, w: W - 2 * MX, colW: [3.6, 8.53], rowH: 0.42, border: tblBorder, objectName: "Tabelle Eckdaten" });
  text(s, "Der Ertrag trägt die Raten nur zusammen mit dem Gastro-Gewinn. Die Bank wird wegen des Ertragswerts zusätzliche Sicherheiten oder Eigenkapital verlangen, siehe Folie Ertragswert.", { x: MX, y: 6.0, w: W - 2 * MX, h: 0.6, fontSize: 14, bold: true, color: C.accent2 });
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
    [cell("Grundflächenzahl (GRZ)"), cell("0,6 → max. 576 m²"), cell("576 m² Grundfläche (60 %, GRZ-Maximum)")],
    [cell("Vollgeschosse"), cell("zwei (II im Kreis)"), cell("EG und 1. OG, dazu Staffelgeschoss")],
    [cell("Traufhöhe / Höhe"), cell("6,50 m / 12,00 m"), cell("Hauptbaukörper 6,50 m, gesamt ca. 9,90 m")],
    [cell("Dachform"), cell("laut Konzeptheft Mischgebiet, Details im Plan"), cell("Flachdach mit zurückgesetztem Staffelgeschoss")],
    [cell("Baufenster (geschätzt)"), cell("im Plan geschätzt ca. 400–460 m², Stadt klären"), cell("ca. 32 × 18 m = 576 m²")],
    [cell("Stellplätze"), cell("auf dem Grundstück, ausreichende Anzahl"), cell("ca. 6–8, Rest siehe Stellplatzfolie")],
  ];
  s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.2, 4.4, 4.53], rowH: 0.52, border: tblBorder, objectName: "Tabelle B-Plan" });
  card(s, MX, 5.4, W - 2 * MX, 1.25, "Klärungsbedarf");
  text(s, [
    { text: "Schriftlich klären: ", options: { bold: true, color: C.accent1 } },
    { text: "Sind 576 m² Grundfläche zulässig (im Plan ist das Baufenster nach meiner Schätzung kleiner)? Zählt das Staffelgeschoss (ca. 498 m² in Holzbau, 86 % der Fläche darunter) als drittes Vollgeschoss? Ist die Flachdach-Lösung zulässig?" },
  ], { x: MX + 0.25, y: 5.5, w: W - 2 * MX - 0.5, h: 1.05, fontSize: 15, valign: "middle" });
}

// ===== 4b Holzbau und Terrasse =====
{
  const s = content("Staffelgeschoss in Holzbau", "Für Bank und Stadt", "Preise sind Annahmen und müssen durch Angebote der Zimmerei und des Bauunternehmens bestätigt werden.");
  const w = (W - 2 * MX - 0.6) / 3;
  stat(s, MX, 1.5, w, "498 m²", "Staffelgeschoss in Holzbau, nur 0,8 m rundum zurückgesetzt", C.accent2);
  stat(s, MX + (w + 0.3), 1.5, w, eur(-B.k_holz), "Ersparnis gegenüber Massivbau (400 € je m², Annahme)", C.accent5);
  stat(s, MX + 2 * (w + 0.3), 1.5, w, "77 m²", "schmale Dachterrasse rundum (ca. 0,8 m), nicht Teil der BGF", C.accent4);
  card(s, MX, 3.4, W - 2 * MX, 2.9, "Warum Holz oben");
  text(s, [
    { text: "Leichter und schneller: weniger Last auf dem Klinker-Geschoss, kürzere Bauzeit.", options: { bullet: true, breakLine: true } },
    { text: "Zwei Partner aus dem Bekanntenkreis (Bauunternehmen unten, Zimmerei oben) können Preise und Termine gemeinsam angeben.", options: { bullet: true, breakLine: true } },
    { text: "Holzbau hilft beim QNG-Nachweis und beim Effizienzhaus-40-Standard (KfW-Voraussetzung).", options: { bullet: true, breakLine: true } },
    { text: "Brandschutz (Holzbau bis Gebäudeklasse 4, Aufzug und Treppenhaus massiv) und Schallschutz muss der Architekt nachweisen.", options: { bullet: true } },
  ], { x: MX + 0.3, y: 3.6, w: W - 2 * MX - 0.6, h: 2.6, fontSize: 15, paraSpaceAfter: 8 });
}

// ===== 5 Schnitt =====
{
  const s = content("Zwei Geschosse plus Staffelgeschoss", "Für Stadt und Bank", "Schnitt schematisch. Hauptbaukörper bis 6,50 m, Staffelgeschoss bis ca. 9,60 m, Attika ca. 9,90 m.");
  const sc = 0.3; // Zoll je m
  const x0 = 1.7;
  const yBase = 6.4;
  const z = (m) => yBase - m * sc;
  const w = 18 * sc, ws = 16.4 * sc;
  s.addShape(pres.ShapeType.rect, { x: x0 - 0.3, y: yBase, w: w + 0.6, h: 0.06, fill: { color: C.accent4 }, line: { color: C.accent4, width: 0 }, objectName: "Gelände" });
  s.addShape(pres.ShapeType.rect, { x: x0, y: z(3.5), w, h: 3.2 * sc, fill: { color: "F4D58F" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt EG" });
  s.addShape(pres.ShapeType.rect, { x: x0, y: z(6.5), w, h: 3.0 * sc, fill: { color: "9A4034" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt OG" });
  s.addShape(pres.ShapeType.rect, { x: x0, y: z(9.6), w: ws, h: 3.1 * sc, fill: { color: "7A5C3A" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt Staffel" });
  s.addShape(pres.ShapeType.rect, { x: x0 - 0.2, y: z(9.9), w: ws + 0.4, h: 0.3 * sc, fill: { color: "D6D1C8" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt Dach" });
  s.addShape(pres.ShapeType.rect, { x: x0 + ws, y: z(7.6), w: 0.9 * sc, h: 1.1 * sc, fill: { color: "CFE0E8" }, line: { color: C.accent4, width: 1 }, objectName: "Brüstung" });
  text(s, "EG große Gastro mit Bar", { x: x0, y: z(3.5), w, h: 3.2 * sc, fontSize: 14, bold: true, align: "center", valign: "middle" });
  text(s, "1. OG · 2 Büros, 3 Wohnungen", { x: x0, y: z(6.5), w, h: 3.0 * sc, fontSize: 14, bold: true, align: "center", valign: "middle", color: C.background1 });
  text(s, "Staffelgeschoss · 3 Wohnungen", { x: x0, y: z(9.6), w: ws, h: 3.1 * sc, fontSize: 14, bold: true, align: "center", valign: "middle", color: C.background1 });
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
    [cell("EG"), cell("Gastro ca. 510 m² mit Bar, Séparée und Küche, dazu Treppenhaus, Aufzug, Eingänge"), R("576 m²")],
    [cell("1. OG"), cell("2 Büro-Ankermieter (100 und 65 m²), 3 Wohnungen à ca. 107 m²"), R("576 m²")],
    [cell("Staffel"), cell("3 Wohnungen à ca. 111 m², Holzbau, schmale Terrasse rundum"), R("498 m²")],
    [cell("Summe", { bold: true }), cell("6 Wohnungen (655 m²), 2 Büros (165 m²)", { bold: true }), R("1.650 m²", { bold: true })],
  ];
  s.addTable(rows, { x: 7.7, y: 1.6, w: W - 7.7 - MX, colW: [0.9, 3.2, 0.93], rowH: 0.6, border: tblBorder, objectName: "Tabelle Flächen" });
  text(s, "BGF = Bruttogrundfläche, alle Geschossflächen zusammen. Das Staffelgeschoss in Holzbau springt rundum nur ca. 0,8 m zurück, so entsteht eine schmale Terrasse von ca. 77 m² um die Wohnungen.", { x: 7.7, y: 5.4, w: W - 7.7 - MX, h: 1.0, fontSize: 14, color: C.accent4 });
}

// ===== 6 Grundrisse =====
{
  const s = content("Skizzen der Geschosse", "Für die Stadt", "Schematische Skizzen, nicht maßstäblich genau. Aufteilung wird mit dem Architekten verfeinert.");
  const sc = 0.1237;
  const pw = 32 * sc;
  const ph = 18 * sc;
  const gap = (W - 2 * MX - 3 * pw) / 2;
  const y0 = 2.3;
  const plans = [
    {
      title: "Erdgeschoss",
      rooms: [
        [0, 0, 4, 18, "Treppe, Aufzug", "8A9199"],
        [4, 0, 28, 18, "", "F2D48C"],
        [6.5, 2.5, 24, 7.5, "Gastraum und Lounge\nca. 160 Plätze", "E7BE63"],
        [12, 11.2, 15, 1.6, "Bar", "3A3F44"],
        [4, 12.5, 7, 5.5, "Séparée\n30 Plätze", "8A6A45"],
        [12, 14, 6.5, 4, "Küche", "7E8A94"],
        [18.5, 14, 5, 4, "Lager", "A6ADB4"],
        [23.5, 14, 8.5, 4, "WC", "A6ADB4"],
      ],
    },
    {
      title: "1. Obergeschoss",
      rooms: [
        [0, 0, 4, 18, "Treppe, Aufzug", "8A9199"],
        [4, 0, 6.2, 18, "Büro 1\n100 m²", "3F6275"],
        [10.2, 0, 4.1, 18, "Büro 2\n65 m²", "5B7D8C"],
        ...[0, 1, 2].map((n) => [14.3 + n * 5.9, 0, 5.9, 18, `WE ${n + 1}\n107 m²`, "9A4034"]),
      ],
    },
    {
      title: "Staffel (Holzbau)",
      rooms: [
        [0, 0, 32, 18, "", "C9C4B8"],
        [0.8, 0.8, 3.4, 16.4, "Treppe", "8A9199"],
        ...[0, 1, 2].map((n) => [4.2 + n * 9.0, 0.8, 9.0, 16.4, `WE ${n + 4}\n111 m²`, "7A5C3A"]),
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
  text(s, "Grundfläche 32 × 18 m = 576 m² (GRZ-Maximum 0,6). Die Gastro nutzt das ganze EG (ca. 510 m²), Treppenhaus und Aufzug liegen am Westende und erschließen Büros und Wohnungen getrennt von der Gastro. Im 1. OG liegen die zwei Büro-Ankermieter und 3 Wohnungen, die Staffel in Holzbau hat ca. 498 m² BGF mit 3 Wohnungen, die beige Fläche ist die schmale Terrasse (ca. 77 m²).", { x: MX + 0.25, y: 5.45, w: W - 2 * MX - 0.5, h: 1.0, fontSize: 15, valign: "middle" });
}

// ===== 7 Außen =====
{
  const s = content("Modern, Klinker, Milchglas und Staffelgeschoss", "Für die Stadt", "Links Referenzstudie, rechts unsere Eckansicht als Skizze.");
  s.addImage({ path: fit(hasKI("ki_aussen_1.jpg") ? path.join(IMG, "ki_aussen_1.jpg") : path.join(IMG, "aussen.jpg"), 5.9, 3.29), x: MX, y: 1.4, w: 5.9, h: 3.29, altText: "Visualisierung Außenansicht" });
  s.addImage({ path: path.join(IMG, "skizze_aussen_ecke.png"), x: 6.8, y: 1.4, w: 5.9, h: 3.69, sizing: { type: "contain", w: 5.9, h: 3.69 }, altText: "Eckansicht als Skizze: Flachdach mit Staffelgeschoss, Balkone, vollverglastes Erdgeschoss" });
  text(s, hasKI("ki_aussen_1.jpg") ? "KI-Visualisierung" : "Referenzstudie", { x: MX, y: 4.75, w: 5.9, h: 0.3, fontSize: 12, color: C.accent4 });
  text(s, "Unsere Skizze (Eckansicht)", { x: 6.8, y: 5.12, w: 5.9, h: 0.3, fontSize: 12, color: C.accent4 });
  const pts = [["Klinker", "dunkel, Langformat, passend zum Umfeld"], ["Staffelgeschoss", "Holzbau, Terrasse rundum"], ["Balkone", "bodentiefe Fenster, Milchglas-Brüstungen"], ["Glas-EG", "Gastro mit Bar, Terrasse und Vordach"]];
  pts.forEach((p, i) => {
    const x = MX + i * 3.05;
    text(s, p[0], { x, y: 5.6, w: 2.9, h: 0.4, fontSize: 16, bold: false, fontFace: "Georgia", color: C.accent1 });
    text(s, p[1], { x, y: 6.0, w: 2.9, h: 0.6, fontSize: 14 });
  });
}

// ===== 8 Innen =====
{
  const s = content("Große Gastro mit Bar, neu und modern", "Für die Stadt", "KI-Visualisierung, Planung folgt mit dem Gastro-Fachplaner. Details im Gastro-Konzept.");
  s.addImage({ path: fit(path.join(IMG, "ki_gastro_raum.jpg"), 8.2, 4.61), x: MX, y: 1.4, w: 8.2, h: 4.61, altText: "Visualisierung Gastraum mit Bar" });
  s.addImage({ path: fit(path.join(IMG, "ki_gastro_bar.jpg"), 3.63, 2.04), x: 9.1, y: 1.4, w: 3.63, h: 2.04, altText: "Visualisierung Bar" });
  [["ca. 190 Plätze", "innen (160 im Gastraum, 30 im Séparée), plus ca. 60 auf der Terrasse"], ["Bar", "12 Barhocker, Polsterbänke, Backbar"], ["Material", "Olivgrün, Cognac-Samt, Bordeaux, Eiche, schwarzer Stahl"]].forEach((p, i) => {
    text(s, p[0], { x: 9.1, y: 3.7 + i * 0.95, w: 3.63, h: 0.35, fontSize: 16, bold: false, fontFace: "Georgia", color: C.accent2 });
    text(s, p[1], { x: 9.1, y: 4.1 + i * 0.95, w: 3.63, h: 0.55, fontSize: 13 });
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
  text(s, "KI-generierte Visualisierungen zur Orientierung, Gestalt und Materialien. Fassadenteilung, Länge (32 m) und Büro-Fenster im 1. OG weichen im Detail von den Skizzen ab, Maße folgen mit dem Architekten.", { x: MX, y: H - 0.95, w: W - 2 * MX, h: 0.4, fontSize: 12, color: C.accent4 });
}

// ===== 9 Stellplätze =====
{
  const s = content("Stellplätze sind der Knackpunkt", "Für die Stadt", "Bedarf nach groben Annahmen (1,5 pro Wohnung, 1 je 10 m² Gastraum bei ca. 370 m², 1 je 30 m² Büro). Die Stellplatzsatzung der Stadt gilt verbindlich.");
  s.addChart(pres.charts.BAR, [{ name: "Stellplätze", labels: ["Bedarf (Annahme)", "Platz auf dem Grundstück"], values: [Math.round(B.stellplatz_bedarf), 7] }], {
    x: MX, y: 1.5, w: 5.8, h: 4.6, barDir: "col", chartColors: ["8C3B32", "2F4A3E"], varyColors: true, showValue: true, dataLabelPosition: "outEnd", dataLabelColor: "1F2421", dataLabelFontSize: 16, dataLabelFontFace: "+mn-lt",
    catAxisLabelColor: "1F2421", catAxisLabelFontSize: 14, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, showTitle: false, valAxisMaxVal: 36, valAxisMinVal: 0, objectName: "Diagramm Stellplätze",
  });
  text(s, "Vorschlag für die Stadt", { x: 7.0, y: 1.5, w: 5.7, h: 0.4, fontSize: 19, bold: false, fontFace: "Georgia", color: C.accent1 });
  text(s, [
    { text: `Bedarf ca. ${Math.round(B.stellplatz_bedarf)} Stellplätze, auf dem Grundstück passen bei 576 m² Gebäude nur ca. 6–8.`, options: { bullet: true, breakLine: true } },
    { text: "Restplätze auf der öffentlichen Parkfläche nebenan (im Plan eingezeichnet) per Vereinbarung nutzen, besonders am Abend.", options: { bullet: true, breakLine: true } },
    { text: "Alternativ Ablöse statt Bau, die Höhe muss die Stadt nennen.", options: { bullet: true, breakLine: true } },
    { text: "Klären, ob der 10 m breite Grünstreifen teils befestigt werden darf.", options: { bullet: true } },
  ], { x: 7.0, y: 2.05, w: 5.7, h: 3.8, fontSize: 16, paraSpaceAfter: 10 });
}

// ===== 11b Flächen und Mieten =====
{
  const s = content("Flächen und Mieten: Wohnungen, Büros und Gastro", "Für die Bank", "Miete 11,18 €/m² (950 € für 85 m², Annahme des Bauherrn). Portale nennen für Neubau in Werlte ca. 10,7–11,0 €/m². Nebenkosten werden umgelegt.");
  const rows = [[hdr("Einheit"), hdr("Geschoss"), hdr("Fläche", "right"), hdr("Miete je m²", "right"), hdr("Kaltmiete / Monat", "right"), hdr("Kaltmiete / Jahr", "right")]];
  B.einheiten.forEach((e) => rows.push([cell(e.nr), cell(e.geschoss), R(e.m2.toFixed(1).replace(".", ",") + " m²"), R(eur2(e.miete_m2)), R(eur(e.miete)), R(eur(e.jahr))]));
  rows.push([cell("Summe Wohnen", { bold: true }), cell(""), R(B.wf.toFixed(1).replace(".", ",") + " m²", { bold: true }), R(""), R(eur(B.miete_voll_monat), { bold: true }), R(eur(B.miete_voll_monat * 12), { bold: true })]);
  rows.push([cell("Gastro (Pacht 10 €/m²)", { bold: true }), cell("EG"), R("510,0 m²", { bold: true }), R(eur2(10)), R(eur(B.pacht_monat), { bold: true }), R(eur(B.pacht_monat * 12), { bold: true })]);
  B.anker.slice(0, 2).forEach((a) => rows.push([cell(a[0].split(":")[0] + " (Ankermieter)", { bold: true }), cell("1. OG"), R(fm1(a[1]) + " m²", { bold: true }), R(eur2(a[2])), R(eur(a[3]), { bold: true }), R(eur(a[4]), { bold: true })]));
  rows.push([cell("Rohertrag gesamt", { bold: true }), cell(""), cell(""), cell(""), R(eur(B.rohertrag_monat), { bold: true }), R(eur(B.rohertrag), { bold: true })]);
  s.addTable(rows, { x: MX, y: 1.45, w: W - 2 * MX, colW: [3.3, 1.5, 1.6, 1.8, 2.0, 1.93], rowH: 0.36, border: tblBorder, objectName: "Tabelle Mieten" });
}

// ===== 11b2 Gewerbe: Gastro-Bedarf und Ankermieter =====
{
  const s = content("Gewerbeflächen: große Gastro und zwei Ankermieter", "Für die Bank", "Gastro-Flächen aus Plätzen und Richtwerten abgeleitet, Büromieten und Laufzeiten sind Annahmen (keine Büromarktdaten für Werlte gefunden).");
  const rows = [[hdr("Gastro-Flächenbedarf"), hdr("Menge", "right"), hdr("Fläche", "right")]];
  B.gastro_bedarf.forEach((r) => rows.push([cell(r[0]), R(r[1] > 1 ? r[1] + " Plätze" : "–"), R(nf.format(Math.round(r[3])) + " m²")]));
  rows.push([cell("Gastro gesamt (ca. 190 Plätze)", { bold: true }), R(""), R(nf.format(Math.round(B.g_bedarf)) + " m²", { bold: true })]);
  s.addTable(rows, { x: MX, y: 1.5, w: 5.9, colW: [3.3, 1.3, 1.3], rowH: 0.4, border: tblBorder, objectName: "Tabelle Gastro Bedarf" });
  const rows2 = [[hdr("Ankermieter Büro (1. OG)"), hdr("Fläche", "right"), hdr("Miete / m²", "right"), hdr("Miete / Jahr", "right")]];
  B.anker.slice(0, 2).forEach((a) => rows2.push([cell(a[0]), R(nf.format(a[1]) + " m²"), R(eur2(a[2])), R(eur(a[4]))]));
  rows2.push([cell("Summe Büro, 10 Jahre fest", { bold: true }), R(nf.format(B.b_m2) + " m²", { bold: true }), R(eur2(B.b_miete_m2), { bold: true }), R(eur(B.b_miete_jahr), { bold: true })]);
  s.addTable(rows2, { x: 6.8, y: 1.5, w: W - 6.8 - MX, colW: [2.6, 1.0, 1.1, 1.23], rowH: 0.5, border: tblBorder, objectName: "Tabelle Ankermieter" });
  card(s, 6.8, 3.7, W - 6.8 - MX, 2.7, "Wirkung");
  text(s, [
    { text: "Ankermieter: ", options: { bold: true, color: C.accent1 } },
    { text: `Die Büros bringen ${eur(B.b_miete_jahr)} im Jahr über 10 Jahre (Indexmiete, zusammen ${mio(B.b_ueber_laufzeit)}) und decken ${pct(B.b_anteil_kd, 0)} des Kapitaldienstes. Zusammen mit den Wohnungen decken die langfristigen Mieten ${pct(B.b_wohn_anteil_kd, 0)}, den Rest tragen Pacht und Gastro-Gewinn.`, options: { breakLine: true } },
    { text: "Gastro: ", options: { bold: true, color: C.accent1 } },
    { text: `${B.g_plaetze} Plätze auf ${nf.format(Math.round(B.g_bedarf))} m² (${B.g_m2_platz.toFixed(1).replace(".", ",")} m² je Platz), Pacht ${pct(B.g_pacht_quote, 1)} vom Umsatz.`, options: {} },
  ], { x: 7.05, y: 3.85, w: W - 6.8 - MX - 0.5, h: 2.5, fontSize: 12.5, paraSpaceAfter: 6 });
  text(s, "Das EG gehört ganz der Gastro, die Büros liegen im 1. OG mit Aufzug und eigenem Eingang (Versicherung, Makler). Die Grundfläche ist auf das Maximum der GRZ (576 m²) vergrößert.", { x: MX, y: 5.45, w: 5.9, h: 1.2, fontSize: 12, color: C.accent4 });
}

// ===== 11c KfW-Programme =====
{
  const s = content("KfW-Kredite 297, 298 und 299", "Für Bank und Stadt", "KfW zahlt im Neubau keinen Zuschuss, sondern verbilligt den Zins. Beträge und Zinsen laut Ratgebern Oktober 2026, bei Hausbank und KfW bestätigen. Antrag über die Hausbank vor Baubeginn.");
  const rows = [[hdr("Programm"), hdr("Wofür"), hdr("Rahmen (mit QNG)"), hdr("Im Projekt", "right"), hdr("Zins (Annahme)", "right")],
    [cell("KfW 297 Klimafreundlicher Neubau", { bold: true }), cell("selbst genutzte Wohnungen"), cell("bis 150.000 € je Wohnung"), R(eur(B.kredit_297)), R("2,50 %")],
    [cell("KfW 298 Klimafreundlicher Neubau", { bold: true }), cell("vermietete Wohnungen"), cell("bis 150.000 € je Wohnung"), R(eur(B.kredit_298)), R("2,50 %")],
    [cell("KfW 299 Klimafreundlicher Neubau", { bold: true }), cell("Gastro und Büros (Nichtwohngebäude)"), cell("bis 2.000 € je m² Nettogrundfläche"), R(eur(B.kredit_299)), R("3,00 %")],
    [cell("Hausbank (Rest)", { bold: true }), cell("Restfinanzierung inkl. Bauzeitzinsen"), cell("–"), R(eur(B.kredit_bank)), R("4,00 %")]];
  s.addTable(rows, { x: MX, y: 1.45, w: W - 2 * MX, colW: [3.3, 2.8, 2.9, 1.7, 1.43], rowH: 0.5, border: tblBorder, objectName: "Tabelle KfW" });
  card(s, MX, 4.15, W - 2 * MX, 2.3, "Voraussetzungen");
  text(s, [
    { text: "Voraussetzungen: ", options: { bold: true, color: C.accent1 } },
    { text: "Effizienzhaus 40 (Gastro: Effizienzgebäude 40), QNG-Zertifikat für den vollen Rahmen, Heizung ohne Öl, Gas und Biomasse (z. B. Wärmepumpe), Energieeffizienz-Experte, Antrag vor Baubeginn über die Hausbank.", options: { breakLine: true } },
    { text: "Gemischte Nutzung: ", options: { bold: true, color: C.accent1 } },
    { text: `Wohnteil (297/298) und Gastro (299) werden getrennt gefördert. Kreditrahmen insgesamt ${eur(B.kfw_rahmen)}, das sind ${pct(B.kredit_kfw_anteil)} des Darlehens. Die KfW-Zinsen schwanken in den Quellen zwischen 0,6 % und 3,05 %. Mehrkosten für den Standard angenommen mit 3 % (${eur(B.k_eh40)}).`, options: {} },
  ], { x: MX + 0.3, y: 4.3, w: W - 2 * MX - 0.6, h: 2.1, fontSize: 13.5, paraSpaceAfter: 6 });
}

// ===== 11d Kosten =====
{
  const s = content("Gesamtkosten", "Für die Bank", "Baukosten 2.200 €/m² (Holz-Staffel 400 € günstiger) und 15 % Baunebenkosten sind Annahmen des Bauherrn und müssen durch Angebote von Bauunternehmen und Zimmerei bestätigt werden.");
  const rows = [[hdr("Posten"), hdr("Rechnung"), hdr("Betrag", "right"), hdr("Anteil", "right")],
    [cell("Grundstück inkl. Steuer und Notar"), cell("960 m² × 230 € + ca. 7 %"), R(eur(B.k_land_ges)), R(pct(B.k_land_ges / B.k_gesamt))],
    [cell("Bau, Massivbau"), cell("1.650 m² × 2.200 €"), R(eur(B.k_bau_massiv)), R(pct(B.k_bau_massiv / B.k_gesamt))],
    [cell("Abschlag Holzbau (Staffelgeschoss)"), cell("498 m² × 400 € günstiger"), R(eur(B.k_holz)), R(pct(B.k_holz / B.k_gesamt))],
    [cell("Dachterrasse rundum (schmal)"), cell("77 m² × 450 €"), R(eur(B.k_terrasse)), R(pct(B.k_terrasse / B.k_gesamt))],
    [cell("Baunebenkosten (Architekt, Statik, Gebühren)"), cell("15 % vom Bau"), R(eur(B.k_bnk)), R(pct(B.k_bnk / B.k_gesamt))],
    [cell("Mehrkosten Effizienzhaus 40 und QNG"), cell("3 % auf Bau inkl. Nebenkosten"), R(eur(B.k_eh40)), R(pct(B.k_eh40 / B.k_gesamt))],
    [cell("Ausbau Gastro (190 Plätze) und Büros"), cell("1.000 € je Platz, Büros 150 €/m²"), R(eur(B.k_ausbau)), R(pct(B.k_ausbau / B.k_gesamt))],
    [cell("Finanzierungskosten (Bauzeit, Bereitstellung, Anlaufzeit)"), cell("27 Monate"), R(eur(B.k_fin)), R(pct(B.k_fin / B.k_gesamt))],
    [cell("Gesamtkosten", { bold: true }), cell(""), R(eur(B.k_gesamt), { bold: true }), R("100 %", { bold: true })]];
  s.addTable(rows, { x: MX, y: 1.5, w: 8.1, colW: [3.7, 2.2, 1.35, 0.85], rowH: 0.46, border: tblBorder, objectName: "Tabelle Kosten" });
  s.addChart(pres.charts.DOUGHNUT, [{ name: "Kosten", labels: ["Grundstück", "Bau", "Baunebenkosten und Standard", "Gastro-Ausbau", "Finanzierung"], values: [B.k_land_ges, B.k_bau, B.k_bnk + B.k_eh40, B.k_ausbau, B.k_fin] }], {
    x: 8.9, y: 1.4, w: 4.0, h: 4.4, holeSize: 55, chartColors: ["C49A45", "8C3B32", "5B6770", "2F4A3E", "A8B0B6"], showPercent: true, showValue: false, dataLabelColor: "FFFFFF", dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt",
    showLegend: true, legendPos: "b", legendFontSize: 11, legendColor: "1F2421", legendFontFace: "+mn-lt", showTitle: false, objectName: "Diagramm Kosten",
  });
  text(s, `Das sind ca. ${nf.format(Math.round(B.kosten_m2_bgf))} € pro m² BGF.`, { x: MX, y: 6.3, w: 8, h: 0.4, fontSize: 15, bold: true, color: C.accent2 });
}

// ===== 11e Finanzierungsplan =====
{
  const s = content("Finanzierungsplan", "Für die Bank", "Kein Eigenkapital. Die Hausbank finanziert den Rest und die Zinsen der Bau- und Anlaufzeit. Tilgungsfreie Anlaufzeit 12 Monate ist mit der Bank zu verhandeln.");
  const rows = [[hdr("Mittelherkunft"), hdr("Betrag", "right"), hdr("Anteil", "right"), hdr("Zins", "right")]];
  B.fin_tab.forEach((r) => rows.push([cell(r[0].replace(" Klimafreundlicher Neubau", "").replace(" (Restfinanzierung inkl. Zinsen der Bauzeit)", "")), R(r[1] ? eur(r[1]) : "–"), R(r[2] ? pct(r[2]) : "–"), R(r[3] ? (r[3] * 100).toFixed(2).replace(".", ",") + " %" : "")]));
  s.addTable(rows, { x: MX, y: 1.5, w: 7.6, colW: [4.0, 1.5, 1.0, 1.1], rowH: 0.5, border: tblBorder, objectName: "Tabelle Herkunft" });
  card(s, 8.5, 1.5, W - 8.5 - MX, 4.2, "Finanzierungskosten");
  text(s, [
    { text: "Mischzins", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: (B.mischzins * 100).toFixed(2).replace(".", ",") + " % über alle Darlehen.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Bau- und Anlaufzeit", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: `15 Monate Bau und 12 Monate Anlaufzeit kosten ${eur(B.k_fin)} an Zinsen und Bereitstellungsgebühr, finanziert von der Hausbank.`, options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Danach", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: `Rate ${eur(B.rate_monat)} pro Monat (Zins plus 1 % Anfangstilgung).`, options: {} },
  ], { x: 8.75, y: 1.7, w: W - 8.5 - MX - 0.5, h: 3.9, fontSize: 13 });
  text(s, `Die Kosten von ${eur(B.k_gesamt)} sind komplett durch Fremdkapital gedeckt.`, { x: MX, y: 5.0, w: 7.6, h: 0.6, fontSize: 14, bold: true, color: C.accent2 });
}

// ===== 11f Zinsen und Rate =====
{
  const s = content("Zinsberechnung und Rate je Darlehen", "Für die Bank", "Annuität: Rate = Darlehen × (Zins + 1 % Tilgung) / 12. Zinsbindung 10 Jahre, danach gleicher Zins angenommen. Die Rate gilt nach der tilgungsfreien Anlaufzeit.");
  const rows = [[hdr("Darlehen"), hdr("Betrag bei Rate-Start", "right"), hdr("Zins", "right"), hdr("Tilgung", "right"), hdr("Rate / Monat", "right"), hdr("Rate / Jahr", "right")],
    [cell("KfW Wohnen (297 und 298)"), R(eur(B.kredit_297 + B.kredit_298)), R("2,50 %"), R("1,00 %"), R(eur(B.rate_w)), R(eur(B.rate_w * 12))],
    [cell("KfW Gastro (299)"), R(eur(B.kredit_299)), R("3,00 %"), R("1,00 %"), R(eur(B.rate_g)), R(eur(B.rate_g * 12))],
    [cell("Hausbank"), R(eur(B.kredit_bank)), R("4,00 %"), R("1,00 %"), R(eur(B.rate_b)), R(eur(B.rate_b * 12))],
    [cell("Summe", { bold: true }), R(eur(B.kredit), { bold: true }), R((B.mischzins * 100).toFixed(2).replace(".", ",") + " %", { bold: true }), R(""), R(eur(B.rate_monat), { bold: true }), R(eur(B.rate_jahr1), { bold: true })]];
  s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.5, 2.2, 1.2, 1.2, 2.0, 2.03], rowH: 0.55, border: tblBorder, objectName: "Tabelle Zinsen" });
  text(s, [
    { text: `Im ersten Jahr nach der Anlaufzeit zahlst du ${eur(B.zins_jahr1)} Zinsen und ${eur(B.tilg_jahr1)} Tilgung.`, options: { breakLine: true } },
    { text: "Zinsänderung nach 10 Jahren: +1 Prozentpunkt auf die Restschuld kostet ca. " + eur(B.rest_10 * 0.01 / 12) + " pro Monat mehr.", options: {} },
  ], { x: MX, y: 4.7, w: W - 2 * MX, h: 1.3, fontSize: 14, paraSpaceAfter: 8 });
}

// ===== 11g Abzahlungsplan =====
{
  const s = content("Abzahlungsplan", "Für die Bank", "Monatlicher Plan über 35 Jahre im Excel-Blatt Tilgungsplan. Hier nach Jahren, Anfangstilgung 1 %, gleicher Zins nach der Zinsbindung angenommen.");
  s.addChart(pres.charts.LINE, [{ name: "Restschuld", labels: B.tilgung.map((t) => String(t.jahr)), values: B.tilgung.map((t) => Math.round(t.rest)) }], {
    x: MX, y: 1.4, w: 6.8, h: 4.8, chartColors: ["8C3B32"], lineSize: 3, lineDataSymbolSize: 4, catAxisLabelColor: "1F2421", catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisLabelColor: "1F2421", valAxisLabelFontSize: 11, valAxisLabelFontFace: "+mn-lt", valAxisLabelFormatCode: "#,##0",
    valGridLine: { color: "D9D9D9", size: 0.5 }, catGridLine: { style: "none" }, showLegend: false, showTitle: true, title: "Restschuld in € nach Jahren", titleFontSize: 13, titleColor: "1F2421", titleFontFace: "+mn-lt", objectName: "Diagramm Restschuld",
  });
  const rows = [[hdr("Jahr"), hdr("Zinsen", "right"), hdr("Tilgung", "right"), hdr("Restschuld", "right")]];
  [1, 2, 3, 5, 10, 15, 20, 25, 30, 35].forEach((y) => { const t = B.tilgung[y - 1]; rows.push([cell(String(y) + (y === 10 ? " (Ende Zinsbindung)" : "")), R(eur(t.zins)), R(eur(t.tilg)), R(eur(t.rest))]); });
  s.addTable(rows, { x: 7.6, y: 1.4, w: W - 7.6 - MX, colW: [1.7, 1.1, 1.1, 1.23], rowH: 0.4, border: tblBorder, objectName: "Tabelle Abzahlungsplan" });
  text(s, `Nach 10 Jahren Zinsbindung beträgt die Restschuld ${eur(B.rest_10)}. Die Anschlussfinanzierung muss eingeplant werden.`, { x: MX, y: 6.25, w: W - 2 * MX, h: 0.5, fontSize: 13.5, bold: true, color: C.accent2 });
}

// ===== 12 Cashflow =====
{
  const s = content("Ertrag und Kapitaldienst pro Monat", "Für die Bank", "Gastro-Betrieb bei 65.000 € Umsatz und 30,5 % Marge vor Pacht, ohne Lohn des Bauherrn. Rücklagen 10 % von Miete und Pacht.");
  const rows = [[hdr("Position", "left"), hdr("pro Monat", "right"), hdr("pro Jahr", "right")],
    [cell("Kaltmiete Wohnen (6 Wohnungen)"), R(eurS(B.c_miete)), R(eurS(B.c_miete * 12))],
    [cell("Büromieten (2 Ankermieter, 10 Jahre fest)"), R(eurS(B.c_buero)), R(eurS(B.c_buero * 12))],
    [cell("Pacht Gastro (510 m² × 10 €)"), R(eurS(B.c_pacht)), R(eurS(B.c_pacht * 12))],
    [cell("Rücklagen (10 % von Miete, Büro, Pacht)"), R(eurS(B.c_rueck)), R(eurS(B.c_rueck * 12))],
    [cell("Nettoertrag Immobilie", { bold: true }), R(eurS(B.c_netto_immo), { bold: true }), R(eurS(B.c_netto_immo * 12), { bold: true })],
    [cell("Betriebsergebnis Gastro nach Pacht"), R(eurS(B.c_gastro)), R(eurS(B.c_gastro * 12))],
    [cell("Nettoertrag vor Kapitaldienst", { bold: true }), R(eurS(B.c_netto), { bold: true }), R(eurS(B.c_netto * 12), { bold: true })],
    [cell("Kapitaldienst (Zinsen und Tilgung)"), R(eurS(B.c_kd)), R(eurS(B.c_kd * 12))],
    [cell("Ergebnis nach Kapitaldienst", { bold: true }), cfCell(B.c_ergebnis), cfCell(B.c_ergebnis * 12)]];
  s.addTable(rows, { x: MX, y: 1.45, w: 7.6, colW: [4.2, 1.7, 1.7], rowH: 0.43, border: tblBorder, objectName: "Tabelle Cashflow" });
  card(s, 8.6, 1.5, W - 8.6 - MX, 4.5, "Kennzahlen");
  text(s, [
    { text: "Kapitaldienstdeckung (DSCR)", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: `Gesamt ${B.dscr.toFixed(2).replace(".", ",")}, nur Immobilie ${B.dscr_immo.toFixed(2).replace(".", ",")}, nur Wohnen und Büro ${B.dscr_lang.toFixed(2).replace(".", ",")}. Banken verlangen meist mindestens 1,2.`, options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Zinsdeckung", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: B.zinsdeckung.toFixed(2).replace(".", ",") + ".", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Anfangsrendite", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: pct2(B.anfangsrendite) + " auf die Gesamtkosten (Nettoertrag Immobilie).", options: {} },
  ], { x: 8.85, y: 1.7, w: W - 8.6 - MX - 0.5, h: 4.2, fontSize: 13 });
  text(s, "Ohne den Gastro-Gewinn deckt die Immobilie allein die Raten nicht. Der Pachtvertrag mit einem tragfähigen Betreiber ist für die Bank entscheidend.", { x: MX, y: 6.3, w: W - 2 * MX, h: 0.5, fontSize: 13.5, bold: true, color: C.accent2 });
}

// ===== 14 Gastro Umsatz =====
{
  const s = content("Wie viel Umsatz braucht die Gastro?", "Für die Bank", "Gastro-Marge vor Pacht 30,5 % vom Umsatz (Branchen-Richtwert, nicht aus Werlte). Bei sehr niedrigem Umsatz drücken Fixkosten stärker, die Rechnung ist dort zu günstig.");
  const rows = [[hdr("Umsatz pro Monat"), hdr("Gewinn vor Pacht", "right"), hdr("Gewinn nach Pacht", "right")]];
  B.gastro_umsatz.forEach((r) => rows.push([cell(eur(r[0]), { bold: r[0] === 65000 }), R(eur(r[1])), cfCell(r[2])]));
  s.addTable(rows, { x: MX, y: 1.5, w: 7.6, colW: [2.8, 2.4, 2.4], rowH: 0.55, border: tblBorder, objectName: "Tabelle Gastro Umsatz" });
  card(s, 8.6, 1.5, W - 8.6 - MX, 3.6, "Break-even");
  text(s, [
    { text: "Betrieb allein", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: `Ab ca. ${eur(Math.round(B.g_breakeven / 100) * 100)} Umsatz deckt der Betrieb seine Pacht.`, options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Haus insgesamt", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: `Ab ca. ${eur(Math.round(B.breakeven_haus / 100) * 100)} Umsatz sind alle Raten bezahlt.`, options: {} },
  ], { x: 8.85, y: 1.7, w: W - 8.6 - MX - 0.5, h: 3.3, fontSize: 13.5 });
  text(s, "Der Umsatz von 65.000 € entspricht nur ca. 4.100 € je Sitzplatz und Jahr (190 Plätze), das ist für 510 m² vorsichtig.", { x: MX, y: 5.4, w: 7.6, h: 0.5, fontSize: 13.5, color: C.accent4 });
}

// ===== 14b Ertragswert =====
{
  const s = content("Ertragswert und Beleihung", "Für die Bank", "Vereinfachtes Ertragswertverfahren nach ImmoWertV, getrennt nach Nutzung: Liegenschaftszins Wohnen 4,0 %, Büro 6,0 %, Gastro 6,5 %. Der verbindliche Beleihungswert kommt vom Gutachter der Bank.");
  const rows = [[hdr("Ertragswert"), hdr("Betrag", "right")],
    [cell("Rohertrag pro Jahr (Mieten und Pacht)"), R(eur(B.rohertrag))],
    [cell("Bewirtschaftungskosten"), R(eur(B.bewirt))],
    [cell("Reinertrag", { bold: true }), R(eur(B.reinertrag), { bold: true })],
    [cell("Bodenwert (960 m² × 230 €)"), R(eur(B.bodenwert))],
    [cell("Gebäudeertragswert (mittl. Vervielfältiger " + B.vervielf.toFixed(1).replace(".", ",") + ")"), R(eur(B.ertragswert_geb))],
    [cell("Ertragswert gesamt", { bold: true }), R(eur(B.ertragswert), { bold: true })],
    [cell("davon Wohnen / Büro / Gastro", { fontSize: 11 }), R(`${(B.ew_wohn / 1e6).toFixed(2).replace(".", ",")} / ${(B.ew_buero / 1e6).toFixed(2).replace(".", ",")} / ${(B.ew_gastro / 1e6).toFixed(2).replace(".", ",")} Mio. €`)]];
  s.addTable(rows, { x: MX, y: 1.5, w: 6.2, colW: [4.4, 1.8], rowH: 0.46, border: tblBorder, objectName: "Tabelle Ertragswert" });
  const rows2 = [[hdr("Beleihung"), hdr("Betrag", "right")],
    [cell("Sachwert (Boden + Herstellungskosten)"), R(eur(B.sachwert))],
    [cell("Beleihungswert (niedrigerer Wert, −10 %)"), R(eur(B.beleihungswert))],
    [cell("Gesamtkosten und Darlehen"), R(eur(B.kredit))],
    [cell("Beleihungsauslauf", { bold: true }), cfCell(0, { text: pct(B.auslauf), fill: { color: "F8E4E2" }, color: C.accent6 })],
    [cell("Ertragswert minus Gesamtkosten"), R(eurS(B.wertluecke))],
    [cell("Betrag über 80 % Auslauf"), R(eur(B.eigenkapital_80))]];
  rows2[4][1] = R(pct(B.auslauf), { bold: true, color: C.accent6, fill: { color: "F8E4E2" } });
  s.addTable(rows2, { x: 7.0, y: 1.5, w: W - 7.0 - MX, colW: [3.9, 1.83], rowH: 0.5, border: tblBorder, objectName: "Tabelle Beleihung" });
  text(s, [
    { text: "Einordnung: ", options: { bold: true, color: C.accent1 } },
    { text: `Die Mieten und die Pacht tragen einen Wert von ${mio(B.ertragswert)}, die Kosten liegen bei ${mio(B.k_gesamt)}. Eine Bank beleiht üblicherweise nur bis ca. 80 % des Beleihungswerts. Für die Finanzierung braucht es deshalb zusätzliche Sicherheiten (Grundschulden auf weitere Immobilien, Bürgschaft) oder Eigenkapital in Höhe von ca. ${mio(B.eigenkapital_80)}.`, options: {} },
  ], { x: MX, y: 5.55, w: W - 2 * MX, h: 1.3, fontSize: 13 });
}

// ===== 14c Prognose und Belastungstest =====
{
  const s = content("Prognose und Belastungstest", "Für die Bank", "Prognose: Miete, Pacht und Umsatz +1,5 % pro Jahr, Kapitaldienst konstant. Belastungstest vereinfacht, Hausbank rechnet mit eigenen Annahmen.");
  const P = B.prognose;
  const yrs = [1, 3, 5, 7, 10];
  const rows = [[hdr("Jahr"), ...yrs.map((y) => hdr(String(y), "right"))],
    [cell("Nettoertrag vor Kapitaldienst"), ...yrs.map((y) => R(eur(P["Nettoertrag vor Kapitaldienst"][y - 1])))],
    [cell("Kapitaldienst"), ...yrs.map((y) => R(eur(P["Kapitaldienst"][y - 1])))],
    [cell("Ergebnis nach Kapitaldienst", { bold: true }), ...yrs.map((y) => cfCell(P["Ergebnis nach Kapitaldienst"][y - 1] / 12, { text: eurS(P["Ergebnis nach Kapitaldienst"][y - 1]) }))],
    [cell("DSCR"), ...yrs.map((y) => R(P["Kapitaldienstdeckung (DSCR)"][y - 1].toFixed(2).replace(".", ",")))],
    [cell("Restschuld Jahresende"), ...yrs.map((y) => R(eur(P["Restschuld Jahresende"][y - 1])))]];
  s.addTable(rows, { x: MX, y: 1.45, w: W - 2 * MX, colW: [3.7, 1.69, 1.69, 1.69, 1.69, 1.67], rowH: 0.37, border: tblBorder, objectName: "Tabelle Prognose" });
  const rows2 = [[hdr("Belastungstest (pro Monat)"), hdr("Ergebnis", "right"), hdr("DSCR", "right"), hdr("zum Plan", "right")]];
  B.sens.forEach((r, i) => rows2.push([cell(r[0], { bold: i === 0 }), cfCell(r[1]), R(r[2].toFixed(2).replace(".", ",")), R(i === 0 ? "" : eurS(r[3]))]));
  s.addTable(rows2, { x: MX, y: 3.85, w: W - 2 * MX, colW: [6.6, 1.9, 1.5, 2.13], rowH: 0.27, fontSize: 11, border: tblBorder, objectName: "Tabelle Belastungstest" });
}

// ===== 14d Airbnb =====
{
  const s = content("Prüfung: zwei Wohnungen als Airbnb", "Für die Bank", "Annahmen: Auslastung 50 % (Emsland laut Quelle ca. 37 %), Möblierung 600 €/m² im Kredit, Kostenquote 56 % vom Umsatz, Mindest-Mehrertrag 300 € pro Monat für den Mehraufwand.");
  const T = B.airbnb_tab;
  const row = (i, f) => T[i];
  const rows = [[hdr("Zwei Apartments à ..."), hdr("45 m²", "right"), hdr("55 m²", "right"), hdr("67 m²", "right")],
    [cell("Preis pro Nacht"), ...[1, 2, 3].map((c) => R(eur(T[2][c])))],
    [cell("Netto Airbnb je Apartment und Monat"), ...[1, 2, 3].map((c) => R(eur(T[4][c])))],
    [cell("Netto langfristige Miete je Apartment und Monat"), ...[1, 2, 3].map((c) => R(eur(T[5][c])))],
    [cell("Möblierung (im Kredit)"), ...[1, 2, 3].map((c) => R(eur(T[6][c])))],
    [cell("Mehrertrag für 2 Apartments pro Monat", { bold: true }), ...[1, 2, 3].map((c) => cfCell(T[9][c], { text: eurS(T[9][c]) }))]];
  s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [5.6, 2.2, 2.2, 2.13], rowH: 0.5, border: tblBorder, objectName: "Tabelle Airbnb" });
  card(s, MX, 4.7, W - 2 * MX, 1.7, "Ergebnis");
  text(s, [
    { text: "Ergebnis: ", options: { bold: true, color: C.accent1 } },
    { text: "Kurzzeitvermietung lohnt sich nicht. Auch kleine Apartments bringen nach Möblierung, Kapitaldienst und Kosten weniger als langfristige Mieter. Dazu kommen Aufwand, Reinigung und bei mehr als 12 Betten Sonderbau-Brandschutz. Deshalb bleiben alle 6 Wohnungen langfristig vermietet." }], { x: MX + 0.3, y: 4.85, w: W - 2 * MX - 0.6, h: 1.4, fontSize: 14, valign: "middle" });
}

// ===== 16 Risiken =====
{
  const s = content("Risiken und was wir dagegen tun", "Für die Bank", "Die Miete von 11,18 €/m² ist eine Annahme des Bauherrn, Marktdaten für Werlte liegen darunter.");
  const items = [
    ["Sicherheiten und Beleihung", `Beleihungsauslauf ${pct(B.auslauf)} bei 100 % Fremdfinanzierung. Gegenmaßnahme: Grundschulden auf weitere Immobilien, Bürgschaft oder Eigenkapital, Pachtvertrag mit Bonitätsnachweis.`],
    ["Gastro-Umsatz", `Haus insgesamt ab ca. ${eur(Math.round(B.breakeven_haus / 1000) * 1000)} Umsatz im Plus, bei Ausfall der Gastro fehlen ca. ${eur(-B.sens[8][3])} pro Monat, bei Auszug des großen Büro-Ankermieters ca. ${eur(-B.sens[6][3])}. Gegenmaßnahme: Konzept, erfahrener Betreiber, Pachtstaffel, Mietverträge über 10 Jahre mit Bonitätsprüfung.`],
    ["Zins", "KfW-Zinsen und Rahmen sind Stand Okt. 2026 unsicher, nach 10 Jahren ist der Folgezins offen. Gegenmaßnahme: Zusage vor Baubeginn, Forward-Darlehen, Tilgungsaussetzung."],
    ["Genehmigung und Standard", "576 m² Grundfläche, Staffelgeschoss und Flachdach müssen bestätigt werden, KfW verlangt Effizienzhaus 40 mit QNG. Gegenmaßnahme: Vorabstimmung, Energieeffizienz-Experte früh einbinden."],
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

// ===== 17 Was ich brauche =====
{
  const s = content("Was ich von Stadt und Bank brauche", "Für Stadt und Bank", "");
  const items = [
    ["Von der Stadt: Genehmigung", "576 m² Grundfläche, Staffelgeschoss, Flachdach und Höhe schriftlich bestätigen"],
    ["Von der Stadt: Stellplätze", "Mitnutzung der öffentlichen Parkfläche oder faire Ablöse"],
    ["Von der Stadt: Grundstück", "Kaufpreis 230 €/m² mit Baureife, Reservierung bis zur Finanzierungszusage"],
    ["Von der Bank: Darlehen", `Finanzierung von ${mio(B.kredit)} mit KfW 297/298/299 und tilgungsfreier Anlaufzeit von 12 Monaten`],
    ["Von der Bank: Sicherheiten", "Gespräch über zusätzliche Grundschulden oder Bürgschaft wegen des Beleihungsauslaufs"],
    ["Von der Bank: KfW-Antrag", "Antrag für 297/298 und 299 vor Baubeginn über die Hausbank"],
  ];
  const cw = (W - 2 * MX - 0.4) / 2;
  items.forEach((it, i) => {
    const x = MX + (i % 2) * (cw + 0.4);
    const y = 1.5 + Math.floor(i / 2) * 1.65;
    card(s, x, y, cw, 1.45, "Bedarf " + (i + 1));
    text(s, it[0], { x: x + 0.25, y: y + 0.15, w: cw - 0.5, h: 0.45, fontSize: 18, bold: false, fontFace: "Georgia", color: C.accent1 });
    text(s, it[1], { x: x + 0.25, y: y + 0.65, w: cw - 0.5, h: 0.7, fontSize: 14 });
  });
}

// ===== 18 Nächste Schritte =====
{
  const s = content("Nächste Schritte", "Für Stadt und Bank", "Zeitplan der Stadt aus dem Konzeptheft, Bauantrag und Förderzusagen sind meine Planung.");
  const steps = [
    ["Okt 2026", "Gespräch mit der Stadt: Preis, Förderung, Stellplätze"],
    ["Nov 2026", "Architekt, Baufenster, Höhen und Geschosse schriftlich klären"],
    ["Dez 2026", "Hausbank: Finanzierung, Anlaufzeit, KfW 297/298/299 und Sicherheiten klären"],
    ["Q1 2027", "Städtebaulicher Vertrag, Bauantrag, KfW-Antrag vor Baubeginn"],
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
  text(s, "Annahmen, Gastro-Kosten, Gastro-Ausbau, Mietdaten", { x: MX, y: 4.1, w: 10, h: 0.6, fontSize: 18, color: "CFD8D3" });
}
{
  const s = content("Rechenannahmen und offene Punkte", "Anhang", "Alle Zahlen sind Planungsannahmen, keine Zusagen.");
  const left = [
    "Grundstück 960 m² × 230 € plus ca. 7 % (5 % Grunderwerbsteuer, ca. 2 % Notar)",
    "Bau 1.650 m² BGF × 2.200 €, Staffel (498 m²) in Holzbau 400 €/m² günstiger, Terrasse 77 m² × 450 €, Baunebenkosten 15 %",
    "100 % Fremdfinanzierung, 1 % Anfangstilgung, tilgungsfreie Anlaufzeit 12 Monate",
    "Bauzeit 15 Monate, Bereitstellungszins 3 % p. a. ab Monat 7",
    "Zins KfW 297/298 2,5 %, KfW 299 3,0 %, Hausbank 4,0 % (Annahmen)",
  ];
  const right = [
    `Gastro-Umsatz ${k(UM)} netto, Marge vor Pacht 30,5 %`,
    "6 Wohnungen (655 m²) zu 11,18 €/m² Kaltmiete, 2 Büros (165 m²) zu 9,50 und 10,00 €/m² (10 Jahre fest), Gastro-Pacht 10 €/m² auf 510 m²",
    "Lohn des Bauherrn wird vorerst nicht gerechnet, Rücklagen 10 % der Miete und Pacht",
    "KfW-Kredite statt Zuschuss, Antrag vor Baubeginn; Mehrkosten Effizienzhaus 40 und QNG 3 %",
    "Nebenkosten (Grundsteuer, Versicherung, Betriebskosten) werden auf die Mieter umgelegt, die Hausverwaltung deckt die Rücklage",
    "Offen: Baufenster, Staffelgeschoss, Höhen, Stellplatzsatzung, Zins nach 10 Jahren, Sicherheiten",
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
    [`Pacht ans Haus (${v.gastroM2} m² × 10 €)`, "", v.pacht],
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
  const s = content("Gastro-Ausbau nach Posten", "Anhang", "Ausgehend vom Zielbudget des Bauherrn (150.000 € für 150 Plätze) hochgerechnet auf 190 Plätze: 1.000 € je Platz. Büros: Vermieter-Ausbau 150 €/m² zusätzlich. Angebote müssen es bestätigen.");
  const items = [
    ["Küche (Herd, Kühlräume, Edelstahl, Spülküche)", 38000],
    ["Lüftung und Abluft", 23000],
    ["Theke und Bar (Zapfanlage, Kühlung, Backbar)", 25000],
    ["Möbel (ca. 190 Plätze, Lounge, Séparée)", 36000],
    ["Beleuchtung und Deko", 10000],
    ["Wand, Boden, Decke, Akustik", 19000],
    ["Gäste-WC Ausstattung", 6000],
    ["Kasse, Technik, Musik, WLAN", 6000],
    ["Terrasse (Holzdeck, Möbel, Heizstrahler, 60 Plätze)", 8000],
    ["Planung und Genehmigung", 6000],
    ["Eröffnung, Marketing, Warenerstbestückung", 4000],
  ];
  const sumN = items.reduce((a, r) => a + r[1], 0);
  const rows = [[hdr("Posten"), hdr("Betrag", "right")], ...items.map((r) => [cell(r[0]), R(eur(r[1]))]),
    [cell("Puffer 5 %"), R(eur(sumN * 0.05))],
    [cell("Summe (im Modell: 190.000 €)", { bold: true }), R(eur(sumN * 1.05), { bold: true })]];
  s.addTable(rows, { x: MX, y: 1.35, w: 8.0, colW: [6.0, 2.0], rowH: 0.34, border: tblBorder, objectName: "Tabelle Gastro-Ausbau" });
  card(s, 9.0, 1.35, W - 9.0 - MX, 3.2, "Hinweis Ausbau");
  text(s, `Baunebenkosten von 15 % fallen auf Möbel und Geräte nicht an, die Planung steckt als eigener Posten drin. Eine erste Schätzung für einen aufwendigeren Ausbau lag bei ca. 310.000 €. Für die große Gastro (510 m², 190 Plätze) sind 190.000 € angesetzt. Bei ${eur(250000)} Ausbau steigt die Rate um ca. ${eur(finanz(v, 0, A.zinsPlan, { gastroAusbau: 250000 }).rate - f0.plan.rate)} im Monat.`, { x: 9.25, y: 1.55, w: W - 9.0 - MX - 0.5, h: 2.8, fontSize: 14 });
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
    { text: "Wohnungen 11,18 €/m² Kaltmiete (950 € für 85 m², Bauherr, zentrale Lage). Büro 9,50–10,00 €/m², Gastro-Pacht 10 €/m², ohne Marktdaten." },
  ], { x: 9.85, y: 1.7, w: W - 9.6 - MX - 0.5, h: 3.2, fontSize: 14 });
  text(s, "Quellen: mietpreise.info/mietspiegel/werlte, miete-aktuell.de, immobilienscout24.de (Kreis Emsland), Abruf Oktober 2026", { x: MX, y: 5.4, w: W - 2 * MX, h: 0.6, fontSize: 12, color: C.accent4 });
}

(async () => {
  const file = path.join(OUT, "Neue-Mitte-Werlte_Baufeld3_6-Wohnungen_Grosse-Gastro-EG.pptx");
  await pres.writeFile({ fileName: file });
  await applyTheme(file, THEME);
  console.log("geschrieben", file);
})();
