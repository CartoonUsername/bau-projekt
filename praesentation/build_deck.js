// Baut zwei Decks: Neue Mitte Werlte – Baufeld 3 (mit Büro / ohne Büro)
// Aufruf: NODE_PATH=<pfad zu node_modules> node build_deck.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");
const { A, VARIANTEN, finanz, cashflow, umsatzBreakEven } = require("./model");

const IMG = process.env.BILDER || path.join(__dirname, "bilder");
const OUT = process.env.OUT || __dirname;

const THEME = {
  name: "Neue Mitte Werlte",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2421",
    lt1: "FFFFFF",
    dk2: "2F4A3E", // Dunkelgrün (Innenraum)
    lt2: "F1F0EE",
    accent1: "8C3B32", // Klinkerrot
    accent2: "2F4A3E",
    accent3: "C49A45", // Messing/Gold
    accent4: "5B6770", // Schiefer
    accent5: "2E7D5B", // positiv
    accent6: "B3261E", // negativ
    hlink: "8C3B32",
    folHlink: "5B6770",
  },
};

const FOERDERUNG = [0, 0.05, 0.1, 0.15, 0.2, 0.25];
const FOERDERUNG_KURZ = [0, 0.1, 0.15, 0.2];

const nf = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
const eur = (n) => `${n < 0 ? "−" : ""}${nf.format(Math.abs(Math.round(n)))} €`;
const eurS = (n) => `${n > 0 ? "+" : n < 0 ? "−" : ""}${nf.format(Math.abs(Math.round(n)))} €`;
const pct = (f) => `${Math.round(f * 100)} %`;
const mio = (n) => `${(n / 1e6).toFixed(2).replace(".", ",")} Mio. €`;

function buildDeck(v, other) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
  pres.title = `Neue Mitte Werlte – Baufeld 3 (${v.name})`;
  pres.author = "Bessam Hasso";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const W = 13.33;
  const H = 7.5;
  const MX = 0.6;

  // ---------- Layouts ----------
  pres.defineSlideMaster({
    title: "TITEL",
    background: { color: "2F4A3E" },
    objects: [],
  });
  pres.defineSlideMaster({
    title: "INHALT",
    background: { color: "FFFFFF" },
    objects: [
      {
        placeholder: {
          options: {
            name: "title",
            type: "title",
            x: MX,
            y: 0.35,
            w: W - 2 * MX,
            h: 0.9,
            fontFace: "Cambria",
            fontSize: 32,
            bold: true,
            color: C.accent1,
            valign: "middle",
            align: "left",
            margin: 0,
          },
          text: "",
        },
      },
    ],
    slideNumber: { x: W - 1.1, y: H - 0.45, w: 0.6, h: 0.3, fontSize: 10, color: C.accent4, align: "right" },
  });

  // ---------- Helfer ----------
  let slideCount = 0;
  function content(title, tag, notes) {
    const s = pres.addSlide({ masterName: "INHALT" });
    slideCount++;
    s.addText(title, { placeholder: "title" });
    if (tag) {
      s.addText(tag, {
        x: MX,
        y: H - 0.45,
        w: 6,
        h: 0.3,
        fontSize: 10,
        color: C.accent4,
        margin: 0,
        isTextBox: true,
        objectName: "Zielgruppe",
      });
    }
    if (notes) s.addNotes(notes);
    return s;
  }
  function text(s, t, o) {
    s.addText(t, Object.assign({ fontFace: "Calibri", fontSize: 14, color: C.text1, margin: 0, isTextBox: true, valign: "top" }, o));
  }
  function card(s, x, y, w, h, name) {
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w, h,
      fill: { color: C.background2 },
      line: { color: C.background2, width: 0 },
      rectRadius: 0.08,
      objectName: name || "Karte",
    });
  }
  function stat(s, x, y, w, big, label, color) {
    card(s, x, y, w, 1.55, "Kennzahl " + label);
    text(s, big, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.75, fontSize: 32, bold: true, fontFace: "Cambria", color: color || C.accent1, valign: "middle" });
    text(s, label, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: 0.5, fontSize: 14, color: C.accent4 });
  }
  const hdr = (t, align) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent2 }, align: align || "left", fontSize: 13 } });
  const cell = (t, o) => ({ text: t, options: Object.assign({ fontSize: 13 }, o) });
  function cfCell(n, o) {
    return cell(eurS(n), Object.assign({ align: "right", bold: true, color: n >= 0 ? C.accent5 : C.accent6, fill: { color: n >= 0 ? "E3F1EA" : "F8E4E2" } }, o));
  }

  const F = {}; // Finanzen je Förderung/Zins
  for (const f of FOERDERUNG) {
    F[f] = { plan: finanz(v, f, A.zinsPlan), ausgang: finanz(v, f, A.zinsAusgang) };
    F[f].cfPlan = cashflow(v, F[f].plan);
    F[f].cfAusgang = cashflow(v, F[f].ausgang);
  }
  const f0 = F[0];
  const firstPositive = FOERDERUNG.find((f) => F[f].cfPlan.cf >= 0);

  // ===== 1 Titel =====
  {
    const s = pres.addSlide({ masterName: "TITEL" });
    slideCount++;
    s.addImage({ path: path.join(IMG, "aussen.jpg"), x: 6.9, y: 0, w: 6.43, h: H, sizing: { type: "cover", w: 6.43, h: H }, altText: "Referenzstudie Außenansicht" });
    text(s, "NEUE MITTE WERLTE", { x: MX, y: 1.3, w: 6, h: 0.4, fontSize: 16, bold: true, color: C.accent3, charSpacing: 4 });
    text(s, "Baufeld 3: Gastro und Wohnen am Rathaus", { x: MX, y: 1.85, w: 6, h: 2.2, fontSize: 40, bold: true, fontFace: "Cambria", color: C.background1, valign: "top" });
    text(s, `Baukonzept und Wirtschaftlichkeit, Variante ${v.name}`, { x: MX, y: 4.3, w: 6, h: 0.6, fontSize: 18, color: C.background1 });
    text(s, "Bessam Hasso, Werlte\nBebauungsplan Nr. 123, 1. Änderung (Entwurf 25.08.2026)\nStand Oktober 2026", { x: MX, y: 5.5, w: 6, h: 1.1, fontSize: 14, color: "CFD8D3" });
    s.addNotes("Titelfolie. Das Bild ist eine Referenzstudie mit Flachdach, der Entwurf wird mit Satteldach angepasst.");
  }

  // ===== 2 Überblick =====
  {
    const s = content("Das Vorhaben auf einen Blick", "Für Stadt und Bank", "Kernaussage: Das Haus trägt sich erst mit Förderung und günstigem Zins, die Gastro muss den Rest tragen.");
    const w = (W - 2 * MX - 0.6) / 4;
    stat(s, MX, 1.5, w, mio(f0.plan.gesamt), "Gesamtkosten (ohne Bauzeitzinsen)");
    stat(s, MX + (w + 0.2), 1.5, w, "8", `Wohnungen auf 960 m² BGF, Gastro ${v.gastroM2} m²${v.bueroM2 ? ", Büro " + v.bueroM2 + " m²" : ""}`, C.accent2);
    stat(s, MX + 2 * (w + 0.2), 1.5, w, eur(f0.plan.rate), "Rate pro Monat (3,3 %, ohne Förderung)");
    stat(s, MX + 3 * (w + 0.2), 1.5, w, eurS(f0.cfPlan.cf), "Ergebnis pro Monat nach Lohn, ohne Förderung", f0.cfPlan.cf >= 0 ? C.accent5 : C.accent6);
    text(s, "Ergebnis pro Monat nach Lohn bei 40.000 € Gastro-Umsatz (Plan, 3,3 % Zins)", { x: MX, y: 3.4, w: 9, h: 0.35, fontSize: 16, bold: true, color: C.accent2 });
    const rows = [[hdr("Förderung"), ...FOERDERUNG.map((f) => hdr(pct(f), "right"))], [cell("Ergebnis"), ...FOERDERUNG.map((f) => cfCell(F[f].cfPlan.cf))]];
    s.addTable(rows, { x: MX, y: 3.85, w: W - 2 * MX, colW: [2.2, ...FOERDERUNG.map(() => (W - 2 * MX - 2.2) / FOERDERUNG.length)], rowH: 0.5, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Förderung" });
    text(s,
      [
        { text: firstPositive !== undefined ? `Mit ${pct(firstPositive)} Förderung läuft das Haus erstmals im Plus. ` : "Im Plan bleibt das Ergebnis ohne höhere Förderung negativ. ", options: { bold: true } },
        { text: "Bei 4,0 % Zins braucht es deutlich mehr: siehe Szenarien. Dazu kommt eine Anlaufphase von 12 Monaten ohne Rate (Aufschub)." },
      ],
      { x: MX, y: 5.0, w: W - 2 * MX, h: 1.2, fontSize: 16 });
  }

  // ===== 3 Standort und Zeitplan =====
  {
    const s = content("Ein Eckgrundstück an der neuen Mitte", "Für die Stadt", "Quelle: Konzeptheft Neue Mitte Werlte (Seiten 13, 16 und 24).");
    const items = [
      ["ca. 960 m²", "Baufeld 3, östlich des Rathauses, südlich der Planstraße"],
      ["Mischgebiet", "Gewerbe im EG erwünscht, Stellplätze auf dem Grundstück"],
      ["Baureife", "liegt vor, Baubeginn jederzeit möglich"],
    ];
    items.forEach((it, i) => {
      card(s, MX, 1.5 + i * 1.4, 5.2, 1.2, "Fakt " + (i + 1));
      text(s, it[0], { x: MX + 0.25, y: 1.6 + i * 1.4, w: 4.7, h: 0.5, fontSize: 24, bold: true, fontFace: "Cambria", color: C.accent1 });
      text(s, it[1], { x: MX + 0.25, y: 2.15 + i * 1.4, w: 4.7, h: 0.5, fontSize: 14 });
    });
    // Zeitleiste
    const tl = [
      ["Nov 2026", "Stellplatz alte Grundschule"],
      ["ab März 2027", "Bau Planstraße (Erschließung)"],
      ["Mitte 2027", "Unser Baubeginn"],
      ["ab Juli 2027", "Kreisverkehr Loruper Straße"],
      ["Ende 2028", "Marktplatz, Rathaus fertig und unsere Eröffnung"],
    ];
    const x0 = 6.7;
    s.addShape(pres.ShapeType.line, { x: x0 + 0.15, y: 1.65, w: 0, h: 4.4, line: { color: C.accent4, width: 2 }, objectName: "Zeitleiste" });
    tl.forEach((t, i) => {
      const y = 1.5 + i * 0.95;
      s.addShape(pres.ShapeType.ellipse, { x: x0, y: y + 0.05, w: 0.3, h: 0.3, fill: { color: i === 2 || i === 4 ? C.accent1 : C.accent3 }, line: { color: C.background1, width: 2 }, objectName: "Punkt " + (i + 1) });
      text(s, t[0], { x: x0 + 0.5, y, w: 5.5, h: 0.4, fontSize: 18, bold: true, color: i === 2 || i === 4 ? C.accent1 : C.text1 });
      text(s, t[1], { x: x0 + 0.5, y: y + 0.4, w: 5.5, h: 0.4, fontSize: 14, color: C.accent4 });
    });
  }

  // ===== 4 B-Plan =====
  {
    const s = content("Was der Bebauungsplan vorgibt", "Für die Stadt", "Grundstückskennwerte aus Bebauungsplan Nr. 123 (Entwurf). Baufenster aus dem Planfoto geschätzt, Bauamt muss bestätigen.");
    const rows = [
      [hdr("Festsetzung"), hdr("Wert"), hdr("Unser Entwurf")],
      [cell("Grundflächenzahl (GRZ)"), cell("0,6 → max. 576 m²"), cell("340 m² Grundfläche (35 %)")],
      [cell("Geschosse"), cell("zwei (II im Kreis), laut Konzeptheft 2 bis 3"), cell("EG, 1. OG, Dachgeschoss")],
      [cell("Traufhöhe / Höhe"), cell("6,50 m / 12,00 m"), cell("Satteldach, ca. 38° Neigung")],
      [cell("Bauweise"), cell("offen (o), Sockelhöhe 0,30 m"), cell("freistehendes Gebäude")],
      [cell("Baufenster (geschätzt)"), cell("ca. 27 × 15–17 m = 400–460 m²"), cell("ca. 24 × 14 m")],
      [cell("Stellplätze"), cell("auf dem Grundstück, ausreichende Anzahl"), cell("ca. 10–13, Rest siehe Stellplatzfolie")],
    ];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.2, 4.8, 4.13], rowH: 0.52, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle B-Plan" });
    card(s, MX, 5.4, W - 2 * MX, 1.15, "Klärungsbedarf");
    text(s, [
      { text: "Schriftlich klären: ", options: { bold: true, color: C.accent1 } },
      { text: "Zählt das Dachgeschoss als drittes Geschoss? Bleibt es bei TH 6,50 m / H 12 m? Darf auf dem 10 m breiten Streifen zur Marktstraße geparkt werden?" },
    ], { x: MX + 0.25, y: 5.5, w: W - 2 * MX - 0.5, h: 0.95, fontSize: 15, valign: "middle" });
  }

  // ===== 5 Schnitt und Flächen =====
  {
    const s = content("Drei Ebenen unter dem Satteldach", "Für Stadt und Bank", "Schnitt schematisch, Maße aus dem B-Plan (TH 6,50 m, H 12 m).");
    const sc = 0.34; // Zoll je m
    const bw = 14 * sc; // Gebäudetiefe 14 m
    const x0 = 2.4;
    const yBase = 6.55; // Oberkante Gelände
    const hSock = 0.3 * sc;
    const hEG = 3.5 * sc;
    const hOG = 3.0 * sc;
    const hRoof = 5.5 * sc;
    const yEG = yBase - hSock - hEG;
    const yOG = yEG - hOG;
    const yFirst = yOG - hRoof;
    s.addShape(pres.ShapeType.rect, { x: x0, y: yEG, w: bw, h: hEG, fill: { color: "D9C9A8" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt EG" });
    s.addShape(pres.ShapeType.rect, { x: x0, y: yOG, w: bw, h: hOG, fill: { color: "B5594D" }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt OG" });
    s.addShape(pres.ShapeType.triangle, { x: x0 - 0.15, y: yFirst, w: bw + 0.3, h: hRoof, fill: { color: C.accent4 }, line: { color: C.accent4, width: 1 }, objectName: "Schnitt Dach" });
    text(s, "EG", { x: x0, y: yEG, w: bw, h: hEG, fontSize: 14, bold: true, align: "center", valign: "middle", color: C.text1 });
    text(s, "1. OG", { x: x0, y: yOG, w: bw, h: hOG, fontSize: 14, bold: true, align: "center", valign: "middle", color: C.background1 });
    text(s, "Dachgeschoss", { x: x0, y: yFirst + hRoof * 0.45, w: bw, h: 0.5, fontSize: 14, bold: true, align: "center", valign: "middle", color: C.background1 });
    // Höhenmarken
    const mark = (y, label) => {
      s.addShape(pres.ShapeType.line, { x: x0 - 0.4, y, w: bw + 0.8, h: 0, line: { color: C.accent1, width: 1, dashType: "dash" }, objectName: "Marke " + label });
      text(s, label, { x: MX, y: y - 0.2, w: 1.4, h: 0.4, fontSize: 12, bold: true, color: C.accent1, valign: "middle", align: "right" });
    };
    mark(yFirst, "First 12,00 m");
    mark(yOG, "Traufe 6,50 m");
    // Flächentabelle
    const rows = [
      [hdr("Ebene"), hdr("Nutzung"), hdr("BGF", "right")],
      [cell("EG"), cell(v.bueroM2 ? `Gastro ${v.gastroM2} m², Büro ${v.bueroM2} m², Technik und Treppenhaus` : `Gastro ${v.gastroM2} m², Technik und Treppenhaus`), cell("340 m²", { align: "right" })],
      [cell("1. OG"), cell("6 Wohnungen à ca. 43 m²"), cell("340 m²", { align: "right" })],
      [cell("Dach"), cell("2 Penthouses à ca. 90 m²"), cell("280 m²", { align: "right" })],
      [cell("Summe", { bold: true }), cell("8 Wohnungen, ca. 440 m² Wohnfläche", { bold: true }), cell("960 m²", { bold: true, align: "right" })],
    ];
    s.addTable(rows, { x: 7.7, y: 1.6, w: W - 7.7 - MX, colW: [0.9, 3.2, 0.93], rowH: 0.6, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Flächen" });
    text(s, "BGF = Bruttogrundfläche, alle Geschossflächen zusammen. Die Penthouses liegen im Dachgeschoss mit Dachterrasse.", { x: 7.7, y: 5.4, w: W - 7.7 - MX, h: 0.9, fontSize: 14, color: C.accent4 });
  }

  // ===== 6 Grundrisse =====
  {
    const s = content("Skizzen der Geschosse", "Für die Stadt", "Schematische Skizzen, nicht maßstäblich genau. Aufteilung wird mit dem Architekten verfeinert.");
    const sc = 0.165; // Zoll je m
    const pw = 24 * sc;
    const ph = 14.2 * sc;
    const gap = (W - 2 * MX - 3 * pw) / 2;
    const y0 = 2.3;
    const plans = [
      {
        title: "Erdgeschoss",
        rooms: v.bueroM2
          ? [
              [0, 0, 13.4, 14.2, `Gastro ${v.gastroM2} m²`, "C49A45"],
              [13.4, 0, 4.9, 14.2, `Büro ${v.bueroM2} m²`, "5B6770"],
              [18.3, 0, 5.7, 14.2, "Treppe, Technik", "8A9199"],
            ]
          : [
              [0, 0, 18.3, 14.2, `Gastro ${v.gastroM2} m²`, "C49A45"],
              [18.3, 0, 5.7, 14.2, "Treppe, Technik", "8A9199"],
            ],
      },
      {
        title: "1. Obergeschoss",
        rooms: [
          [0, 0, 8, 5.4, "WE 1 · 43 m²", "B5594D"], [8, 0, 8, 5.4, "WE 2 · 43 m²", "B5594D"], [16, 0, 8, 5.4, "WE 3 · 43 m²", "B5594D"],
          [0, 5.4, 24, 3.4, "Flur, Treppe, Aufzug", "8A9199"],
          [0, 8.8, 8, 5.4, "WE 4 · 43 m²", "B5594D"], [8, 8.8, 8, 5.4, "WE 5 · 43 m²", "B5594D"], [16, 8.8, 8, 5.4, "WE 6 · 43 m²", "B5594D"],
        ],
      },
      {
        title: "Dachgeschoss",
        rooms: [
          [2, 0, 10, 9, "Penthouse 1 · 90 m²", "8C3B32"], [12, 0, 10, 9, "Penthouse 2 · 90 m²", "8C3B32"],
          [2, 9, 20, 5.2, "Dachterrassen, Treppe", "8A9199"],
        ],
      },
    ];
    plans.forEach((p, i) => {
      const x = MX + i * (pw + gap);
      text(s, p.title, { x, y: 1.5, w: pw, h: 0.4, fontSize: 18, bold: true, color: C.accent2 });
      s.addShape(pres.ShapeType.rect, { x, y: y0 - 0.1, w: pw, h: ph + 0.2, fill: { color: "FFFFFF" }, line: { color: C.accent4, width: 1, dashType: "dash" }, objectName: "Baukörper " + p.title });
      p.rooms.forEach((r) => {
        s.addShape(pres.ShapeType.rect, { x: x + r[0] * sc, y: y0 - 0.1 + 0.1 + r[1] * sc, w: r[2] * sc, h: r[3] * sc, fill: { color: r[5] }, line: { color: "FFFFFF", width: 1.5 }, objectName: "Raum " + r[4] });
        text(s, r[4], { x: x + r[0] * sc, y: y0 + r[1] * sc, w: r[2] * sc, h: r[3] * sc, fontSize: 11, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
      });
    });
    card(s, MX, 5.35, W - 2 * MX, 1.2, "Hinweis");
    text(s, "Grundfläche 24 × 14,2 m = 340 m², das passt in das geschätzte Baufenster von ca. 27 × 15–17 m. Das Dachgeschoss ist wegen der Schräge kleiner (ca. 280 m² BGF).", { x: MX + 0.25, y: 5.45, w: W - 2 * MX - 0.5, h: 1.0, fontSize: 15, valign: "middle" });
  }

  // ===== 7 Außen =====
  {
    const s = content("Rotes Klinker, Glas im Erdgeschoss", "Für die Stadt", "Das Referenzbild zeigt ein Flachdach. Im Entwurf kommt ein Satteldach (TH 6,50 m, H 12 m), Materialien und Gliederung bleiben.");
    s.addImage({ path: path.join(IMG, "aussen.jpg"), x: MX, y: 1.5, w: 7.6, h: 4.24, sizing: { type: "cover", w: 7.6, h: 4.24 }, altText: "Referenzstudie Außenansicht mit Klinkerfassade, Balkonen und Glasfront im Erdgeschoss" });
    text(s, "Referenzstudie, im Entwurf mit Satteldach statt Flachdach", { x: MX, y: 5.8, w: 7.6, h: 0.4, fontSize: 12, color: C.accent4 });
    const pts = [
      ["Klinker", "rot, passend zum Umfeld und zum Rathaus"],
      ["Satteldach", "ca. 38°, Traufe 6,50 m, First 12 m"],
      ["Balkone", "Loggien in den Obergeschossen"],
      ["Glasfront", "Gastro mit Terrasse und Stahlstützen"],
    ];
    pts.forEach((p, i) => {
      text(s, p[0], { x: 8.6, y: 1.5 + i * 1.1, w: 4.1, h: 0.4, fontSize: 20, bold: true, fontFace: "Cambria", color: C.accent1 });
      text(s, p[1], { x: 8.6, y: 1.95 + i * 1.1, w: 4.1, h: 0.6, fontSize: 14 });
    });
  }

  // ===== 8 Innen =====
  {
    const s = content("Bar und Restaurant mit Charakter", "Für die Stadt", "Referenzbild für Stimmung und Materialien, keine Planung.");
    s.addImage({ path: path.join(IMG, "innen.jpg"), x: MX, y: 1.5, w: 6.4, h: 4.29, sizing: { type: "cover", w: 6.4, h: 4.29 }, altText: "Referenz Innenraum: Samt-Banquetten, dunkelgrüne Wände, Stahl-Glas-Trennwand" });
    text(s, "Referenz für Stimmung und Materialien", { x: MX, y: 5.85, w: 6.4, h: 0.4, fontSize: 12, color: C.accent4 });
    const pts = [
      ["Materialien", "dunkelgrüne Wände, Holz, Samt, schwarze Stahl-Glas-Elemente"],
      ["Licht", "warme Pendelleuchten und Lichtvouten, Kerzenlicht"],
      [`Plätze`, v.bueroM2 ? "ca. 65 Plätze innen plus Terrasse auf 190 m²" : "ca. 95 Plätze innen plus Terrasse auf 260 m²"],
      ["Konzept", "Restaurant am Tag und Bar am Abend, mit Blick auf den Platz"],
    ];
    pts.forEach((p, i) => {
      text(s, p[0], { x: 7.4, y: 1.5 + i * 1.1, w: 5.3, h: 0.4, fontSize: 20, bold: true, fontFace: "Cambria", color: C.accent2 });
      text(s, p[1], { x: 7.4, y: 1.95 + i * 1.1, w: 5.3, h: 0.7, fontSize: 14 });
    });
  }

  // ===== 9 Stellplätze =====
  {
    const s = content("Stellplätze sind der Knackpunkt", "Für die Stadt", "Bedarf nach groben Annahmen (1,5 pro Wohnung, 1 je 35 m² Büro, 1 je 10 m² Gastraum). Die Stellplatzsatzung der Stadt gilt verbindlich.");
    const need = v.bueroM2 ? 21 : 24;
    s.addChart(pres.charts.BAR, [{ name: "Stellplätze", labels: ["Bedarf (Annahme)", "Platz auf dem Grundstück"], values: [need, 12] }], {
      x: MX, y: 1.5, w: 5.8, h: 4.6, barDir: "col", chartColors: ["8C3B32", "2F4A3E"], varyColors: true,
      showValue: true, dataLabelPosition: "outEnd", dataLabelColor: "1F2421", dataLabelFontSize: 16, dataLabelFontFace: "+mn-lt",
      catAxisLabelColor: "1F2421", catAxisLabelFontSize: 14, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true,
      valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, showTitle: false, valAxisMaxVal: 30, valAxisMinVal: 0, objectName: "Diagramm Stellplätze",
    });
    text(s, "Vorschlag für die Stadt", { x: 7.0, y: 1.5, w: 5.7, h: 0.4, fontSize: 20, bold: true, fontFace: "Cambria", color: C.accent1 });
    text(s, [
      { text: `Bedarf ca. ${need} Stellplätze, auf dem Grundstück passen ca. 10–13.`, options: { bullet: true, breakLine: true } },
      { text: "Restplätze auf der öffentlichen Parkfläche nebenan (im Plan eingezeichnet) per Vereinbarung nutzen.", options: { bullet: true, breakLine: true } },
      { text: "Alternativ Ablöse statt Bau, die Höhe muss die Stadt nennen.", options: { bullet: true, breakLine: true } },
      { text: "Klären, ob der 10 m breite Grünstreifen teils befestigt werden darf.", options: { bullet: true } },
    ], { x: 7.0, y: 2.05, w: 5.7, h: 3.8, fontSize: 16, paraSpaceAfter: 10 });
  }

  // ===== 10 Kosten =====
  {
    const s = content("Gesamtkosten ohne Förderung", "Für die Bank", "Baukosten 2.700 €/m² BGF und 15 % Baunebenkosten sind Annahmen und müssen durch Architekt und Angebote bestätigt werden.");
    const fin = f0.plan;
    const rows = [
      [hdr("Posten"), hdr("Rechnung"), hdr("Betrag", "right")],
      [cell("Grundstück inkl. Steuer, Notar"), cell("960 m² × 230 € + ca. 7 %"), cell(eur(A.grundstueck), { align: "right" })],
      [cell("Bau"), cell("960 m² × 2.700 €"), cell(eur(960 * 2700), { align: "right" })],
      [cell("Baunebenkosten (Architekt, Statik, Gebühren)"), cell("15 % vom Bau"), cell(eur(960 * 2700 * 0.15), { align: "right" })],
      [cell("Gastro-Ausbau (Küche, Theke, Möbel, Technik)"), cell(v.key === "mit" ? "Posten im Anhang" : "inkl. 70 m² Zusatzfläche"), cell(eur(v.gastroAusbau), { align: "right" })],
      [cell("Gesamtkosten", { bold: true }), cell(""), cell(eur(fin.gesamt), { bold: true, align: "right" })],
    ];
    s.addTable(rows, { x: MX, y: 1.5, w: 7.6, colW: [3.5, 2.4, 1.7], rowH: 0.62, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Kosten" });
    s.addChart(pres.charts.DOUGHNUT, [{ name: "Kosten", labels: ["Grundstück", "Bau", "Baunebenkosten", "Gastro-Ausbau"], values: [A.grundstueck, 960 * 2700, 960 * 2700 * 0.15, v.gastroAusbau] }], {
      x: 8.5, y: 1.4, w: 4.3, h: 4.4, holeSize: 55, chartColors: ["C49A45", "8C3B32", "5B6770", "2F4A3E"],
      showPercent: true, showValue: false, dataLabelColor: "FFFFFF", dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt",
      showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: "1F2421", legendFontFace: "+mn-lt", showTitle: false, objectName: "Diagramm Kosten",
    });
    text(s, `Das sind ca. ${nf.format(Math.round(fin.gesamt / 960))} € pro m² BGF.`, { x: MX, y: 5.6, w: 7.6, h: 0.5, fontSize: 16, bold: true, color: C.accent2 });
  }

  // ===== 11 Finanzierung =====
  {
    const s = content("Finanzierung zu 100 % ohne Eigenkapital", "Für die Bank", "Zinsen in der Bauzeit und im Aufschub werden dem Kredit zugeschlagen. Der Aufschub von 12 Monaten muss mit der Bank verhandelt werden.");
    const p = f0.plan;
    const au = f0.ausgang;
    const rows = [
      [hdr(""), hdr("Plan (3,3 %)", "right"), hdr("Ausgang (4,0 %)", "right")],
      [cell("Gesamtkosten"), cell(eur(p.gesamt), { align: "right" }), cell(eur(au.gesamt), { align: "right" })],
      [cell("Zinsen in der Bauzeit (15 Monate)"), cell(eur(p.zinsenBau), { align: "right" }), cell(eur(au.zinsenBau), { align: "right" })],
      [cell("Bereitstellungszinsen (3 % p. a. ab Monat 7)"), cell(eur(p.bereit), { align: "right" }), cell(eur(au.bereit), { align: "right" })],
      [cell("Zinsen im Aufschub-Jahr (keine Rate)"), cell(eur(p.aufschubZinsen), { align: "right" }), cell(eur(au.aufschubZinsen), { align: "right" })],
      [cell("Kredit bei Start der Rate", { bold: true }), cell(eur(p.kredit), { bold: true, align: "right" }), cell(eur(au.kredit), { bold: true, align: "right" })],
      [cell("Rate pro Monat (1 % Tilgung)", { bold: true }), cell(eur(p.rate), { bold: true, align: "right" }), cell(eur(au.rate), { bold: true, align: "right" })],
      [cell("   davon Zinsen"), cell(eur(p.zinsAnteil), { align: "right" }), cell(eur(au.zinsAnteil), { align: "right" })],
      [cell("   davon Tilgung (Rückzahlung der Schuld)"), cell(eur(p.tilgAnteil), { align: "right" }), cell(eur(au.tilgAnteil), { align: "right" })],
    ];
    s.addTable(rows, { x: MX, y: 1.5, w: 8.3, colW: [4.5, 1.9, 1.9], rowH: 0.5, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Finanzierung" });
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

  // ===== 12 Einnahmen und Cashflow =====
  {
    const s = content("Was pro Monat übrig bleibt", "Für die Bank", "Mieten nach Marktdaten für Werlte (Neubau ca. 10,7 bis 11 €/m²). Gastro-Margen nach Branchen-Richtwerten.");
    const c = f0.cfPlan;
    const rows = [
      [hdr("Pro Monat, Plan, ohne Förderung"), hdr("Betrag", "right")],
      [cell("6 Wohnungen: 260 m² × 11 €"), cell(eurS(2860), { align: "right" })],
      [cell("2 Penthouses: 180 m² × 12 €"), cell(eurS(2160), { align: "right" })],
    ];
    if (v.bueroM2) rows.push([cell("Büro: 70 m² × 10 €"), cell(eurS(700), { align: "right" })]);
    rows.push(
      [cell(`Gastro-Pacht: ${v.gastroM2} m² × 12 €`), cell(eurS(v.pacht), { align: "right" })],
      [cell("Gastro-Gewinn nach Pacht (40.000 € Umsatz)"), cell(eurS(c.gastroNachPacht), { align: "right" })],
      [cell("Rate (Zinsen und Tilgung)"), cell(eurS(-f0.plan.rate), { align: "right" })],
      [cell("Dein Lohn"), cell(eurS(-A.lohn), { align: "right" })],
      [cell("Rücklagen (10 % der Miete und Pacht)"), cell(eurS(-c.ruecklagen), { align: "right" })],
      [cell("Ergebnis pro Monat", { bold: true }), cfCell(c.cf)]
    );
    s.addTable(rows, { x: MX, y: 1.5, w: 7.2, colW: [5.3, 1.9], rowH: 0.43, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Cashflow" });
    const labels = ["Miete", "Gastro", "Rate", "Lohn"];
    const vals = [c.miete, c.gastroNachPacht, -f0.plan.rate, -(A.lohn + c.ruecklagen)];
    s.addChart(pres.charts.BAR, [{ name: "Euro pro Monat", labels, values: vals.map(Math.round) }], {
      x: 8.1, y: 1.4, w: 4.7, h: 4.3, barDir: "col", chartColors: ["2E7D5B", "2E7D5B", "B3261E", "B3261E"], varyColors: true,
      showValue: true, dataLabelFormatCode: "#,##0", dataLabelFontSize: 12, dataLabelColor: "1F2421", dataLabelFontFace: "+mn-lt",
      catAxisLabelColor: "1F2421", catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", catAxisLabelPos: "low", catAxisLabelRotate: 0, valAxisHidden: true,
      valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, showTitle: false, objectName: "Diagramm Cashflow",
    });
    text(s, "Lohn im Diagramm inkl. Rücklagen. Die ca. 3.100 € Tilgung in der Rate sind Vermögensaufbau (Schuld sinkt), kein Verlust.", { x: MX, y: 6.55, w: 11.5, h: 0.4, fontSize: 14, color: C.accent4 });
  }

  // ===== 13 Szenarien Förderung x Zins =====
  {
    const s = content("Förderung entscheidet über das Ergebnis", "Für Stadt und Bank", "Förderung als Zuschuss in Prozent der Kosten, der den Kredit von Anfang an verkleinert (Annahme). Höhe und Zweck der Städtebauförderung sind offen.");
    const head = [hdr("Förderung"), hdr("Gesamtkosten", "right"), hdr("Rate (3,3 %)", "right"), hdr("Ergebnis (3,3 %)", "right"), hdr("Rate (4,0 %)", "right"), hdr("Ergebnis (4,0 %)", "right")];
    const rows = [head];
    FOERDERUNG.forEach((f) => {
      rows.push([
        cell(pct(f), { bold: true }),
        cell(eur(F[f].plan.gesamt), { align: "right" }),
        cell(eur(F[f].plan.rate), { align: "right" }),
        cfCell(F[f].cfPlan.cf),
        cell(eur(F[f].ausgang.rate), { align: "right" }),
        cfCell(F[f].cfAusgang.cf),
      ]);
    });
    s.addTable(rows, { x: MX, y: 1.45, w: W - 2 * MX, colW: [1.5, 2.3, 2.1, 2.3, 2.1, 1.83], rowH: 0.44, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Szenarien" });
    s.addChart(pres.charts.LINE, [
      { name: "Plan (3,3 %)", labels: FOERDERUNG.map(pct), values: FOERDERUNG.map((f) => Math.round(F[f].cfPlan.cf)) },
      { name: "Ausgang (4,0 %)", labels: FOERDERUNG.map(pct), values: FOERDERUNG.map((f) => Math.round(F[f].cfAusgang.cf)) },
    ], {
      x: MX, y: 4.75, w: 7.5, h: 2.15, chartColors: ["2F4A3E", "8C3B32"], lineSize: 3, lineDataSymbolSize: 7,
      catAxisLabelColor: "1F2421", catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisLabelColor: "1F2421", valAxisLabelFontSize: 11, valAxisLabelFontFace: "+mn-lt", valAxisLabelFormatCode: "#,##0",
      valGridLine: { color: "D9D9D9", size: 0.5 }, catGridLine: { style: "none" }, showLegend: true, legendPos: "r", legendFontSize: 11, legendColor: "1F2421", legendFontFace: "+mn-lt", showTitle: false, catAxisLabelPos: "low", objectName: "Diagramm Förderung",
    });
    text(s, `Pro 5 Prozentpunkte Förderung steigt das Ergebnis um ca. ${nf.format(Math.round(F[0.05].cfPlan.cf - F[0].cfPlan.cf))} € im Monat. Gastro-Umsatz 40.000 €, nach Lohn und Rücklagen.`, { x: 8.4, y: 5.0, w: W - 8.4 - MX, h: 1.8, fontSize: 14 });
  }

  // ===== 14 Szenarien Umsatz =====
  {
    const s = content("Wie viel Umsatz braucht die Gastro?", "Für die Bank", "Gastro-Marge vor Pacht 30,5 % vom Umsatz (Branchen-Richtwert, nicht aus Werlte). Break-even = Ergebnis nach Lohn genau null.");
    const umsaetze = [36000, 40000, 44000, 48000, 52000];
    const fs = [0, 0.1, 0.15, 0.2];
    const rows = [[hdr("Ergebnis pro Monat (Plan 3,3 %)"), ...umsaetze.map((u) => hdr(`${nf.format(u)} €`, "right"))]];
    fs.forEach((f) => {
      rows.push([cell(`Förderung ${pct(f)}`, { bold: true }), ...umsaetze.map((u) => cfCell(cashflow(v, F[f].plan, u).cf))]);
    });
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.6, ...umsaetze.map(() => (W - 2 * MX - 3.6) / umsaetze.length)], rowH: 0.55, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Umsatz" });
    text(s, "Break-even-Umsatz (Ergebnis nach Lohn = 0)", { x: MX, y: 4.5, w: 8, h: 0.4, fontSize: 18, bold: true, color: C.accent2 });
    const be = [[hdr("Förderung"), ...fs.map((f) => hdr(pct(f), "right"))],
      [cell("Plan, 3,3 %"), ...fs.map((f) => cell(eur(umsatzBreakEven(v, F[f].plan)), { align: "right" }))],
      [cell("Ausgang, 4,0 %"), ...fs.map((f) => cell(eur(umsatzBreakEven(v, F[f].ausgang)), { align: "right" }))]];
    s.addTable(be, { x: MX, y: 5.0, w: W - 2 * MX, colW: [3.6, ...fs.map(() => (W - 2 * MX - 3.6) / fs.length)], rowH: 0.5, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Break-even" });
  }

  // ===== 15 Vergleich Büro =====
  {
    const s = content("Vergleich: mit und ohne Büro", "Für die Bank", "Ohne Büro wächst die Gastro um 70 m² (ca. 30 Plätze), die Büro-Miete von 700 € fällt weg, die Pacht steigt um 840 €.");
    const m = VARIANTEN.mit;
    const o = VARIANTEN.ohne;
    const fm = (f, z) => finanz(m, f, z);
    const fo = (f, z) => finanz(o, f, z);
    const rows = [
      [hdr(""), hdr("Mit Büro", "right"), hdr("Ohne Büro", "right")],
      [cell("Gastrofläche"), cell("190 m²", { align: "right" }), cell("260 m²", { align: "right" })],
      [cell("Gesamtkosten (ohne Förderung)"), cell(eur(fm(0, A.zinsPlan).gesamt), { align: "right" }), cell(eur(fo(0, A.zinsPlan).gesamt), { align: "right" })],
      [cell("Miete + Pacht pro Monat"), cell(eur(m.mieteOhnePacht + m.pacht), { align: "right" }), cell(eur(o.mieteOhnePacht + o.pacht), { align: "right" })],
      [cell("Rate Plan, ohne Förderung"), cell(eur(fm(0, A.zinsPlan).rate), { align: "right" }), cell(eur(fo(0, A.zinsPlan).rate), { align: "right" })],
    ];
    [0, 0.1, 0.15, 0.2].forEach((f) => {
      rows.push([
        cell(`Ergebnis bei ${pct(f)} Förderung (40.000 €)`),
        cfCell(cashflow(m, fm(f, A.zinsPlan)).cf),
        cfCell(cashflow(o, fo(f, A.zinsPlan)).cf),
      ]);
    });
    const cm = cashflow(m, fm(0, A.zinsPlan)).cf;
    const co = cashflow(o, fo(0, A.zinsPlan), 40000).cf;
    const gleich = 40000 + (cm - co) / A.gastroMargeVorPacht;
    s.addTable(rows, { x: MX, y: 1.5, w: 8.2, colW: [4.4, 1.9, 1.9], rowH: 0.5, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Vergleich" });
    card(s, 9.2, 1.5, W - 9.2 - MX, 4.5, "Fazit Vergleich");
    text(s, [
      { text: "Gleichstand", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: `Ohne Büro ist die Variante erst ab ca. ${nf.format(Math.round(gleich / 100) * 100)} € Umsatz (+7 %) so gut wie mit Büro.`, options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Risiko", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Ohne Büro hängt das ganze Erdgeschoss an der Gastro, eine feste Büro-Miete ist für die Bank sicherer." },
    ], { x: 9.45, y: 1.7, w: W - 9.2 - MX - 0.5, h: 4.0, fontSize: 14 });
  }

  // ===== 16 Forderungen an die Stadt =====
  {
    const s = content("Was ich von der Stadt brauche", "Für die Stadt", "Wirkungen gerechnet mit dem Modell (Plan 3,3 %, ohne Förderung als Basis).");
    const base = F[0].plan;
    const eff10 = F[0.1].cfPlan.cf - F[0].cfPlan.cf;
    const finLand = finanz(v, 0, A.zinsPlan, { grundstueck: A.grundstueck - 960 * 30 * 1.07 });
    const effLand = base.rate - finLand.rate;
    const finZins = finanz(v, 0, A.zinsPlan - 0.005);
    const effZins = base.rate - finZins.rate;
    const items = [
      ["Städtebauförderung", `10 % Förderung bringen ca. ${eurS(eff10)} im Monat`],
      ["Grundstückspreis", `30 € weniger pro m² bringen ca. ${eurS(effLand)} im Monat`],
      ["Pacht oder Mietzuschuss", "1.000 € Zuschuss im Monat sind 1.000 € mehr im Monat"],
      ["Stellplätze", "Mitnutzung der öffentlichen Parkfläche oder faire Ablöse"],
      ["Fristen", "Erschließung (Planstraße ab März 2027) und Baubeginn Mitte 2027 abstimmen"],
      ["Zinsvorteil", `0,5 % weniger Zins bringen ca. ${eurS(effZins)} im Monat`],
    ];
    const cw = (W - 2 * MX - 0.4) / 2;
    items.forEach((it, i) => {
      const x = MX + (i % 2) * (cw + 0.4);
      const y = 1.5 + Math.floor(i / 2) * 1.65;
      card(s, x, y, cw, 1.45, "Forderung " + (i + 1));
      text(s, it[0], { x: x + 0.25, y: y + 0.15, w: cw - 0.5, h: 0.45, fontSize: 20, bold: true, fontFace: "Cambria", color: C.accent1 });
      text(s, it[1], { x: x + 0.25, y: y + 0.65, w: cw - 0.5, h: 0.7, fontSize: 14 });
    });
  }

  // ===== 17 Nächste Schritte =====
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
    slideCount++;
    text(s, "Anhang", { x: MX, y: 2.8, w: 10, h: 1.2, fontSize: 44, bold: true, fontFace: "Cambria", color: C.background1 });
    text(s, "Annahmen, Gastro-Kosten, Gastro-Ausbau, Mietdaten", { x: MX, y: 4.1, w: 10, h: 0.6, fontSize: 18, color: "CFD8D3" });
  }

  // A1 Annahmen
  {
    const s = content("Rechenannahmen und offene Punkte", "Anhang", "Alle Zahlen sind Planungsannahmen, keine Zusagen.");
    const left = [
      "Grundstück 960 m² × 230 € plus ca. 7 % (5 % Grunderwerbsteuer, ca. 2 % Notar)",
      "Bau 960 m² BGF × 2.700 €, Baunebenkosten 15 %",
      "100 % Fremdfinanzierung, 1 % Tilgung, Aufschub 12 Monate",
      "Bauzeit 15 Monate, Bereitstellungszins 3 % p. a. ab Monat 7",
      "Zins Plan 3,3 % (Förderkredite, Annahme), Ausgang 4,0 %",
    ];
    const right = [
      "Gastro-Umsatz 40.000 € netto, Marge vor Pacht 30,5 %",
      "Lohn Bessam 6.000 €, Rücklagen 10 % der Miete und Pacht",
      "Förderung als Zuschuss in % der Gesamtkosten (Annahme)",
      "Nicht enthalten: Hausverwaltung, Versicherung, Grundsteuer (ca. 300–500 €/Monat)",
      "Offen: Baufenster, Geschosse, Höhen, Stellplatzsatzung, Zins nach 10 Jahren",
    ];
    const cw = (W - 2 * MX - 0.5) / 2;
    [left, right].forEach((arr, k) => {
      text(s, arr.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < arr.length - 1 } })), { x: MX + k * (cw + 0.5), y: 1.5, w: cw, h: 4.8, fontSize: 15, paraSpaceAfter: 12 });
    });
  }

  // A2 Gastro-Betriebskosten
  {
    const s = content("Gastro: Kosten pro Monat bei 40.000 € Umsatz", "Anhang", "Prozentwerte sind Branchen-Richtwerte aus meiner Einschätzung, nicht aus Quellen für Werlte.");
    const base = [
      ["Wareneinsatz (Einkauf Essen und Getränke)", "ca. 28 %", 11200],
      ["Personal (ohne Chef-Lohn)", "ca. 30 %", 12000],
      [`Pacht ans Haus (${v.gastroM2} m² × 12 €)`, "", v.pacht],
      ["Energie, Wasser, Müll", "ca. 3 %", 1200],
      ["Reinigung, Wäsche, Verbrauchsmaterial", "ca. 2 %", 800],
      ["Werbung und Marketing", "ca. 1,5 %", 600],
      ["Reparaturen, Wartung, Kassensystem", "ca. 1,5 %", 600],
      ["Sonstiges", "ca. 1,5 %", 600],
      ["Versicherungen, GEMA, Gebühren", "ca. 1 %", 400],
      ["Steuerberater, Buchhaltung", "ca. 1 %", 400],
    ];
    const sum = base.reduce((a, r) => a + r[2], 0);
    const rows = [[hdr("Posten"), hdr("Richtwert", "right"), hdr("Betrag", "right")], ...base.map((r) => [cell(r[0]), cell(r[1], { align: "right" }), cell(eur(r[2]), { align: "right" })]),
      [cell("Summe Kosten", { bold: true }), cell(""), cell(eur(sum), { bold: true, align: "right" })],
      [cell("Gewinn nach Pacht, vor Lohn", { bold: true }), cell(""), cell(eur(40000 - sum), { bold: true, align: "right" })]];
    s.addTable(rows, { x: MX, y: 1.4, w: W - 2 * MX, colW: [7.0, 2.5, 2.63], rowH: 0.405, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Gastro-Kosten" });
  }

  // A3 Gastro-Ausbau
  {
    const s = content("Gastro-Ausbau nach Posten", "Anhang", "Preise sind eigene Schätzungen, ein Gastro-Fachplaner und Angebote von Küchen- und Lüftungsbauern müssen sie bestätigen.");
    const items = [
      ["Küche (Herd, Kühlräume, Edelstahl, Spülküche)", 55000, 40000],
      ["Lüftung und Abluft", 30000, 25000],
      ["Theke und Bar (Zapfanlage, Kühlung)", 28000, 20000],
      ["Möbel (ca. 65 Plätze, Banquetten)", 30000, 22000],
      ["Beleuchtung und Deko", 15000, 10000],
      ["Wand, Boden, Decke, Akustik", 25000, 18000],
      ["Gäste-WC Ausstattung", 10000, 8000],
      ["Kasse, Technik, Musik, WLAN", 8000, 6000],
      ["Terrasse (Holzdeck, Möbel, Heizstrahler)", 20000, 12000],
      ["Planung und Genehmigung", 8000, 6000],
      ["Geschirr, Gläser, Besteck, Textilien", 10000, 7000],
      ["Eröffnung, Marketing, Warenerstbestückung", 6000, 5000],
    ];
    const sumN = items.reduce((a, r) => a + r[1], 0);
    const sumS = items.reduce((a, r) => a + r[2], 0);
    const rows = [[hdr("Posten"), hdr("Normal", "right"), hdr("Sparsam", "right")], ...items.map((r) => [cell(r[0]), cell(eur(r[1]), { align: "right" }), cell(eur(r[2]), { align: "right" })]),
      [cell("Puffer 5 %"), cell(eur(sumN * 0.05), { align: "right" }), cell(eur(sumS * 0.05), { align: "right" })],
      [cell("Summe", { bold: true }), cell(eur(sumN * 1.05), { bold: true, align: "right" }), cell(eur(sumS * 1.05), { bold: true, align: "right" })]];
    s.addTable(rows, { x: MX, y: 1.35, w: 8.4, colW: [5.0, 1.7, 1.7], rowH: 0.34, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Gastro-Ausbau" });
    card(s, 9.4, 1.35, W - 9.4 - MX, 3.2, "Hinweis Ausbau");
    text(s, v.key === "mit"
      ? "Im Modell steht „Normal“ (257.250 €). Baunebenkosten von 15 % fallen auf Möbel und Geräte nicht an, die Planung steckt als eigener Posten drin."
      : "Im Modell steht „Normal“ plus 30.000 € für die zusätzlichen 70 m² (Möbel, Boden, Deko, Geschirr), zusammen 287.250 €.",
      { x: 9.65, y: 1.55, w: W - 9.4 - MX - 0.5, h: 2.8, fontSize: 14 });
  }

  // A4 Mietdaten
  {
    const s = content("Mietdaten für Werlte", "Anhang", "Es gibt keinen amtlichen Mietspiegel für Werlte, die Portale arbeiten mit kleinen Stichproben.");
    const rows = [
      [hdr("Quelle"), hdr("Wert für Werlte", "right")],
      [cell("ImmoScout24 (Wohnungen, Durchschnitt)"), cell("7,78 €/m²", { align: "right" })],
      [cell("miete-aktuell.de (Kaltmiete 2026)"), cell("8,13 €/m²", { align: "right" })],
      [cell("mietpreise.info (14 Inserate, Spanne 6,09–14,48 €)"), cell("9,58 €/m²", { align: "right" })],
      [cell("mietpreise.info (Neubau)"), cell("10,73–11,02 €/m²", { align: "right" })],
      [cell("Landkreis Emsland (ImmoScout24, Q2 2026)"), cell("8,10 €/m²", { align: "right" })],
    ];
    s.addTable(rows, { x: MX, y: 1.5, w: 8.6, colW: [6.0, 2.6], rowH: 0.55, border: { type: "solid", color: "FFFFFF", pt: 1 }, objectName: "Tabelle Mieten" });
    card(s, 9.6, 1.5, W - 9.6 - MX, 3.3, "Annahme Miete");
    text(s, [
      { text: "Im Modell", options: { bold: true, color: C.accent1, breakLine: true } },
      { text: "Wohnungen 11 €, Penthouses 12 €, Büro 10 €, Gastro-Pacht 12 €/m². Büro und Gastro sind ohne Marktdaten angesetzt." },
    ], { x: 9.85, y: 1.7, w: W - 9.6 - MX - 0.5, h: 2.9, fontSize: 14 });
    text(s, "Quellen: mietpreise.info/mietspiegel/werlte, miete-aktuell.de, immobilienscout24.de (Kreis Emsland), Abruf Oktober 2026", { x: MX, y: 5.2, w: W - 2 * MX, h: 0.6, fontSize: 12, color: C.accent4 });
  }

  return { pres, count: slideCount };
}

(async () => {
  for (const key of ["mit", "ohne"]) {
    const v = VARIANTEN[key];
    const { pres, count } = buildDeck(v);
    const file = path.join(OUT, `Neue-Mitte-Werlte_Baufeld3_${key === "mit" ? "MIT-Buero" : "OHNE-Buero"}.pptx`);
    await pres.writeFile({ fileName: file });
    await applyTheme(file, THEME);
    console.log("geschrieben", file, count, "Folien");
  }
})();
