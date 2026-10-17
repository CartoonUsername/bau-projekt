// KfW-Förderung (Klimafreundlicher Neubau) für Variante B
// Aufruf: NODE_PATH=<node_modules> APPLY_THEME=<pfad>/apply_theme.js node build_deck_kfw.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { execFileSync } = require("child_process");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");
const { A, VARIANTEN, finanz, cashflow, kfw, KFW, teilung, LAYOUTS } = require("./model");

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
const L = LAYOUTS.B;
const base = finanz(v, 0, A.zinsAusgang), cb = cashflow(v, base).cf;
const plan = finanz(v, 0, A.zinsPlan), cp = cashflow(v, plan).cf;
const sz = [];
for (const q of [false, true]) for (const z of [0.03, 0.02, 0.01]) sz.push({ q, z, r: kfw(v, { zKfW: z, qng: q }) });

async function deck() {
  const t = makeDeck("Neue Mitte Werlte – Baufeld 3: KfW-Förderung", "Neue-Mitte-Werlte_Baufeld3_KfW-Foerderung.pptx");
  const { C, content, text, card, hdr, cell, R, cf, border } = t;
  const pres = t.pres;

  { const s = pres.addSlide({ masterName: "TITEL" });
    s.addImage({ path: fit(path.join(IMG, "ki_aussen_1.jpg"), 6.43, H), x: 6.9, y: 0, w: 6.43, h: H, altText: "Außenansicht am Abend" });
    text(s, "NEUE MITTE WERLTE", { x: MX, y: 1.3, w: 6, h: 0.4, fontSize: 15, bold: true, color: C.accent3, charSpacing: 4 });
    text(s, "KfW-Förderung für Baufeld 3", { x: MX, y: 1.85, w: 6, h: 2.2, fontSize: 34, fontFace: "Georgia", color: C.background1 });
    text(s, "Günstiger Kredit für 8 Wohnungen und die große Gastro", { x: MX, y: 4.3, w: 6, h: 0.7, fontSize: 17, color: C.background1 });
    text(s, "Bessam Hasso, Werlte\nStand Oktober 2026\nKonditionen müssen bei Hausbank und KfW bestätigt werden", { x: MX, y: 5.5, w: 6, h: 1.1, fontSize: 13, color: "CFD8D3" });
  }

  // 2 Kurzfassung
  { const s = content("Kurzfassung: ein günstiger Kredit, kein Zuschuss", "Für Stadt und Bank", "Quellen: KfW-Infoblatt Klimafreundlicher Neubau und Ratgeberseiten (Oktober 2026). Die KfW-Seiten selbst waren nicht abrufbar, die Ratgeber widersprechen sich bei den Zinsen.");
    const k0 = sz[0].r, k1 = sz[3].r;
    const w = (W - 2 * MX - 0.9) / 4;
    const st = [[eur(Math.round(k0.rahmen / 1000) * 1000), "KfW-Kreditrahmen ohne QNG-Zertifikat", C.accent2], [eur(Math.round(k1.rahmen / 1000) * 1000), "KfW-Kreditrahmen mit QNG-Zertifikat", C.accent2], [`${Math.round(k0.anteil * 100)} bis ${Math.round(k1.anteil * 100)} %`, "der Gesamtkosten sind so günstig finanzierbar", C.accent1], [eurS(sz[4].r.cf - cb), "pro Monat mehr als ohne KfW (QNG, 2 % KfW-Zins)", C.accent5]];
    st.forEach((it, i) => { const x = MX + i * (w + 0.3); card(s, x, 1.5, w, 1.6, "Kennzahl " + i); text(s, it[0], { x: x + 0.2, y: 1.6, w: w - 0.4, h: 0.75, fontSize: 24, fontFace: "Georgia", color: it[2], valign: "middle" }); text(s, it[1], { x: x + 0.2, y: 2.4, w: w - 0.4, h: 0.65, fontSize: 12.5, color: C.accent4 }); });
    const rows = [[hdr("Programm"), hdr("Wofür"), hdr("Betrag (Stand Ratgeber)")],
      [cell("KfW 298 Klimafreundlicher Neubau (Wohngebäude)"), cell("8 Wohnungen, auch für Vermieter und Käufer als Anlage"), cell("bis 100.000 € je Wohnung, mit QNG bis 150.000 €")],
      [cell("KfW 299 Klimafreundlicher Neubau (Nichtwohngebäude)"), cell("Gastro im EG (ca. 460 m²)"), cell("ca. 1.500 € je m² Nettogrundfläche, mit QNG ca. 2.000 €")],
      [cell("KfW 300 Wohneigentum für Familien"), cell("nur Selbstnutzer mit Kindern und Einkommensgrenze"), cell("passt nicht für vermietete Wohnungen")]];
    s.addTable(rows, { x: MX, y: 3.4, w: W - 2 * MX, colW: [4.4, 4.0, 3.73], rowH: 0.55, border, objectName: "Tabelle Programme" });
    text(s, "Die KfW zahlt im Neubau keinen Zuschuss mehr: Der Vorteil ist der niedrigere Zins auf einen Teil des Kredits.", { x: MX, y: 5.8, w: W - 2 * MX, h: 0.5, fontSize: 15, bold: true, color: C.accent2 });
  }

  // 3 Voraussetzungen
  { const s = content("Voraussetzungen und Mehrkosten", "Für Stadt und Bank", `Mehrkosten für Effizienzhaus 40 und QNG-Nachweis angenommen mit ${Math.round(KFW.mehrkostenPct * 100)} % der Baukosten, das sind ca. ${eur(sz[0].r.mehrkosten)}. Das ist eine Annahme, der Architekt muss sie bestätigen.`);
    const items = [
      ["Effizienzhaus 40", "Das Haus muss mindestens den Standard Effizienzhaus 40 (Wohnen) bzw. Effizienzgebäude 40 (Gastro) erreichen. Ein Energieeffizienz-Experte plant und bestätigt das."],
      ["QNG-Zertifikat", "Das Qualitätssiegel Nachhaltiges Gebäude erhöht den Kreditrahmen auf 150.000 € je Wohnung. Für die Gastro ist QNG-PLUS oder -PREMIUM nötig. Holzbau im Staffelgeschoss kann dabei helfen."],
      ["Heizung", "Keine Öl-, Gas- oder Biomasseheizung, zum Beispiel Wärmepumpe oder Fernwärme. Das gilt für das ganze Haus mit Gastro-Küche."],
      ["Antrag vor Baubeginn", "Der Antrag läuft über die Hausbank und muss vor dem Vorhabenbeginn gestellt sein. Verträge mit aufschiebender Bedingung sind erlaubt, Bauarbeiten erst nach dem Antrag. Kein Rechtsanspruch, es zählt der Zins am Tag der Zusage."],
    ];
    items.forEach((it, i) => { const x = MX + (i % 2) * 6.2, y = 1.5 + Math.floor(i / 2) * 2.5; card(s, x, y, 5.9, 2.3, it[0]); text(s, it[0], { x: x + 0.25, y: y + 0.15, w: 5.4, h: 0.4, fontSize: 17, fontFace: "Georgia", color: C.accent1 }); text(s, it[1], { x: x + 0.25, y: y + 0.65, w: 5.4, h: 1.55, fontSize: 13 }); });
  }

  // 4 Rechnung
  { const s = content("Was KfW dem Haus bringt", "Für Bank", "Zinsen für KfW laut Ratgebern ca. 0,6 bis 3,05 %, einer nennt 1,94 % für EH40 (10 Jahre, 2 tilgungsfreie Jahre). Hier gerechnet mit 1, 2 und 3 %. Rest des Kredits zu 4,0 %. Ohne Förderung, 1 % Tilgung, 50.000 € Umsatz.");
    const rows = [[hdr("Szenario"), hdr("KfW-Rahmen", "right"), hdr("Anteil am Kredit", "right"), hdr("Mischzins", "right"), hdr("Rate / Monat", "right"), hdr("Ergebnis / Monat", "right"), hdr("gg. ohne KfW", "right")],
      [cell("Ohne KfW (Markt 4,0 %)", { bold: true }), R("–"), R("–"), R("4,00 %"), R(eur(base.rate)), cf(cb), R("")],
      ...sz.map((x) => [cell(`${x.q ? "mit" : "ohne"} QNG, KfW ${String(Math.round(x.z * 1000) / 10).replace(".", ",")} %`), R(eur(Math.round(x.r.rahmen / 1000) * 1000)), R(`${Math.round(x.r.anteil * 100)} %`), R(`${(x.r.zMix * 100).toFixed(2).replace(".", ",")} %`), R(eur(x.r.fin.rate)), cf(x.r.cf), R(eurS(x.r.cf - cb))]),
      [cell("Annahme Hauptpräsentation (3,3 %)", { color: C.accent4 }), R(""), R(""), R("3,30 %"), R(eur(plan.rate)), cf(cp), R(eurS(cp - cb))]];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.9, 1.4, 1.5, 1.2, 1.4, 1.5, 1.23], rowH: 0.42, border, objectName: "Tabelle KfW Szenarien" });
    text(s, `Fazit: Mit QNG und einem KfW-Zins von ca. 2 % sinkt der Mischzins auf ca. ${(sz[4].r.zMix * 100).toFixed(1).replace(".", ",")} %. Das passt zur Annahme von 3,3 % in der Hauptpräsentation, die damit realistisch ist, aber nur mit KfW-Zusage.`, { x: MX, y: 5.95, w: W - 2 * MX, h: 0.8, fontSize: 14, bold: true, color: C.accent2 });
  }

  // 5 Käufer
  { const s = content("Auch für die Käufer in der Familie", "Für Verwandte und Bank", "Jeder Käufer einer Wohnung kann den KfW-Kredit 298 für seine Wohnung beantragen, wenn er sie vermietet. Selbstkosten-Preis, Miete 11,18 €/m², 1 % Tilgung, Rest zu 4,0 %.");
    const mOG = L.wfOG / L.nOG, mST = L.wfST / L.nST;
    const rows = [[hdr("Wohnung"), hdr("Preis", "right"), hdr("Ergebnis ohne KfW", "right"), hdr("KfW 100.000 € zu 2 %", "right"), hdr("KfW 150.000 € (QNG) zu 2 %", "right")]];
    [["1. OG", mOG, "oG"], ["Penthouse", mST, "st"]].forEach(([n, m, k]) => {
      const t0 = teilung(L, A.zinsAusgang);
      const e0 = t0[k](m);
      const res = (kfwBetrag) => { const kosten = e0.kosten; const anteil = Math.min(1, kfwBetrag / kosten); const zMix = anteil * 0.02 + (1 - anteil) * A.zinsAusgang; return teilung(L, zMix)[k](m).ergebnis; };
      rows.push([cell(`${n}, ${Math.round(m)} m²`), R(eur(e0.kosten)), cf(e0.ergebnis), cf(res(100000)), cf(res(150000))]);
    });
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [3.0, 1.9, 2.4, 2.4, 2.43], rowH: 0.6, border, objectName: "Tabelle KfW Käufer" });
    text(s, [
      { text: "Auch mit KfW bleibt die Wohnung bei Selbstkostenpreis und 1 % Tilgung noch leicht im Minus. Erst mit tilgungsfreien Jahren und einem Nachlass im Verkaufsplan wird ein Plus je Wohnung erreichbar.", options: { breakLine: true } },
      { text: "Jeder Käufer braucht eine eigene Zusage von seiner Hausbank, das Wohneigentum-Programm für Familien (300) passt nicht, weil die Wohnungen vermietet werden.", options: {} },
    ], { x: MX, y: 3.4, w: W - 2 * MX, h: 1.8, fontSize: 14, paraSpaceAfter: 8 });
  }

  // 6 Zuschuss vs. Kredit
  { const s = content("Kredit statt Zuschuss: Einordnung", "Für Stadt und Bank", "Die Hauptpräsentation rechnet die Förderung als Zuschuss in Prozent der Kosten. Die KfW bietet im Neubau keinen Zuschuss.");
    const z5 = finanz(v, 0.05, A.zinsAusgang);
    const rows = [[hdr("Förderart"), hdr("Was passiert", "right"), hdr("Ergebnis / Monat", "right"), hdr("gg. ohne Förderung", "right")],
      [cell("Ohne Förderung (Zins 4,0 %)"), R("–"), cf(cb), R("")],
      [cell("5 % Zuschuss der Stadt (Städtebauförderung, offen)"), R(`Kosten ${eur(z5.gesamt)}`), cf(cashflow(v, z5).cf), R(eurS(cashflow(v, z5).cf - cb))],
      [cell("KfW ohne QNG, 2 % auf Teilkredit"), R(`Mischzins ${(sz[1].r.zMix * 100).toFixed(2).replace(".", ",")} %`), cf(sz[1].r.cf), R(eurS(sz[1].r.cf - cb))],
      [cell("KfW mit QNG, 2 % auf Teilkredit"), R(`Mischzins ${(sz[4].r.zMix * 100).toFixed(2).replace(".", ",")} %`), cf(sz[4].r.cf), R(eurS(sz[4].r.cf - cb))]];
    s.addTable(rows, { x: MX, y: 1.5, w: W - 2 * MX, colW: [5.2, 2.5, 2.2, 2.23], rowH: 0.6, border, objectName: "Tabelle Zuschuss gegen Kredit" });
    text(s, "KfW und ein Zuschuss der Stadt lassen sich kombinieren, die Stadt muss aber zusagen. Weitere Programme, etwa Landesmittel oder Wohnraumförderung Niedersachsen (NBank) für geförderte Mieten, sind noch nicht geprüft.", { x: MX, y: 4.7, w: W - 2 * MX, h: 1.2, fontSize: 14, color: C.accent4 });
  }

  // 7 Nächste Schritte
  { const s = content("Nächste Schritte zur KfW-Zusage", "Für Stadt und Bank", "Verbindlich sind nur die Konditionen von KfW und Hausbank am Tag der Zusage.");
    const steps = [["Jetzt", "Energieeffizienz-Experten beauftragen: Effizienzhaus 40 und QNG für Wohnen und Gastro prüfen"], ["Q4 2026", "Heizkonzept ohne Gas und Öl (Wärmepumpe, Fernwärme) und Abluft der Gastro-Küche klären"], ["Q1 2027", "Hausbank fragt KfW-Zinsen und Rahmen für 298 und 299 an, QNG-Zertifizierer wählen"], ["vor Baubeginn", "KfW-Antrag über die Hausbank stellen (Mitte 2027), erst danach mit dem Bau beginnen"], ["nach Fertigstellung", "Nachweis und Bestätigung durch den Experten, Auszahlung abschließen"], ["parallel", "Käufer in der Familie: eigene Kreditzusage mit KfW 298 bei ihrer Hausbank"]];
    steps.forEach((st, i) => { const y = 1.5 + i * 0.85; s.addShape(pres.ShapeType.ellipse, { x: MX, y, w: 0.55, h: 0.55, fill: { color: C.accent2 }, line: { color: C.background1, width: 1 }, objectName: "Schritt " + (i + 1) }); text(s, String(i + 1), { x: MX, y, w: 0.55, h: 0.55, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle" }); text(s, st[0], { x: MX + 0.85, y: y + 0.02, w: 2.2, h: 0.5, fontSize: 16, bold: true, color: C.accent1, valign: "middle" }); text(s, st[1], { x: MX + 3.1, y: y + 0.02, w: 9, h: 0.5, fontSize: 14, valign: "middle" }); });
  }
  await t.save();
}
deck();
