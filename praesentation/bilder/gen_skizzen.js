// SVG-Skizzen Baufeld 3 (modern, Flachdach mit Staffelgeschoss, EG komplett Gastro, 6 Wohnungen, 930 m² BGF)
// Maße: Baukörper 24 x 14,2 m, Hauptbaukörper bis 6,50 m, Staffelgeschoss (ca. 250 m², Holzbau) bis ca. 9,60 m, Attika ca. 9,90 m
const fs = require("fs");
const path = require("path");
const OUT = process.env.OUT || __dirname;

const COL = {
  klinker: "#7C3A32",
  klinkerHell: "#8E453B",
  fuge: "#B9A895",
  zink: "#8A6A45",
  zinkHell: "#9C7B53",
  glas: "#BCD3DE",
  stahl: "#1E2326",
  holz: "#B88652",
  beton: "#D6D1C8",
  gruen: "#2F4A3E",
  gold: "#C49A45",
  pflaster: "#C9B09E",
  text: "#1F2421",
  grau: "#5B6770",
  pflanze: "#5E8C4B",
};

const head = (w, h, defs = "") =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" font-family="Calibri, Carlito, Arial, sans-serif">
<defs>${defs}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFD9EA"/><stop offset="1" stop-color="#EAF2F7"/></linearGradient>
<linearGradient id="glow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7D58B"/><stop offset="1" stop-color="#E8A94F"/></linearGradient>
<radialGradient id="lamp"><stop offset="0" stop-color="#FFE6A8" stop-opacity="0.95"/><stop offset="1" stop-color="#FFE6A8" stop-opacity="0"/></radialGradient>
</defs>`;

// Langformat-Klinker (lange Steine, dünne Fuge)
const brick = (id, skew = 0) =>
  `<pattern id="${id}" width="36" height="12" patternUnits="userSpaceOnUse" ${skew ? `patternTransform="skewY(${skew})"` : ""}>
  <rect width="36" height="12" fill="${COL.klinker}"/>
  <rect y="5.4" width="36" height="1.2" fill="${COL.fuge}" opacity="0.5"/>
  <rect y="11.4" width="36" height="0.6" fill="${COL.fuge}" opacity="0.5"/>
  <rect x="8" y="0" width="1" height="5.4" fill="${COL.fuge}" opacity="0.5"/>
  <rect x="26" y="6.6" width="1" height="4.8" fill="${COL.fuge}" opacity="0.5"/>
</pattern>`;

const T = (x, y, s, size = 16, opt = "") => `<text x="${x}" y="${y}" font-size="${size}" fill="${COL.text}" ${opt}>${s}</text>`;

// ---------------------------------------------------------------- Ansichten
function ansichten() {
  const W = 1600;
  const H = 910;
  const s = 30;
  const ox = 200;
  const gy = 780;
  const X = (x) => ox + x * s;
  const Z = (z) => gy - z * s;
  const R = (x0, z0, x1, z1, fill, extra = "") => `<rect x="${X(x0)}" y="${Z(z1)}" width="${(x1 - x0) * s}" height="${(z1 - z0) * s}" fill="${fill}" ${extra}/>`;
  const L = (x0, z0, x1, z1, st = COL.stahl, w = 2) => `<line x1="${X(x0)}" y1="${Z(z0)}" x2="${X(x1)}" y2="${Z(z1)}" stroke="${st}" stroke-width="${w}"/>`;
  let o = head(W, H, brick("b1"));
  o += `<rect width="${W}" height="${H}" fill="url(#sky)"/>`;
  o += T(40, 52, "Baufeld 3, Neue Mitte Werlte: Ansichten (Skizze)", 28, 'font-weight="bold"');
  o += T(40, 80, "Modern, Flachdach mit Staffelgeschoss: Klinker, bodentiefe Fenster, EG komplett verglast (große Gastro mit Bar)", 16, `fill="${COL.grau}"`);
  o += T(ox, 140, "Südansicht (Längsseite, 24 m)", 20, 'font-weight="bold"');
  o += `<rect x="0" y="${gy}" width="${W}" height="${H - gy}" fill="${COL.pflaster}"/>`;

  // ---- Süd
  // Sockel
  o += R(-0.2, 0, 24.2, 0.3, "#5E564F");
  // Treppenhausblock West (bis Attika)
  o += R(0, 0.3, 3.6, 9.6, "url(#b1)");
  o += R(0.7, 0.4, 2.7, 3.3, COL.stahl) + R(0.85, 0.55, 2.55, 3.3, COL.glas, 'opacity="0.85"'); // Wohn-Eingang
  o += R(1.0, 4.2, 2.4, 6.0, COL.glas, `stroke="${COL.beton}" stroke-width="4"`); // Treppenhausfenster
  o += R(1.0, 7.2, 2.4, 9.0, COL.glas, `stroke="${COL.beton}" stroke-width="4"`);
  // EG Gastro
  o += R(3.6, 0.3, 24, 3.5, "url(#glow)");
  for (let i = 0; i <= 12; i++) o += L(3.6 + i * (20.4 / 12), 0.3, 3.6 + i * (20.4 / 12), 3.5, COL.stahl, 2.5);
  o += L(3.6, 2.6, 24, 2.6, COL.stahl, 2.5);
  for (let i = 0; i < 6; i++) o += `<circle cx="${X(5 + i * 3.3)}" cy="${Z(3.0)}" r="${0.2 * s}" fill="#FFF3D1"/>`;
  o += R(10.4, 0.3, 11.8, 3.5, COL.stahl, 'opacity="0.18"'); // Eingangstür
  // Bar-Silhouette im Fenster
  o += R(15, 0.3, 21, 1.1, COL.holz, 'opacity="0.8"');
  // Deckenband
  o += R(-0.2, 3.5, 24.2, 3.8, COL.beton);
  // OG: drei Achsen
  o += R(3.6, 3.8, 24, 6.5, "url(#b1)");
  for (let k = 0; k < 3; k++) {
    const bx = 3.6 + k * 6.8;
    o += R(bx + 0.5, 3.9, bx + 3.2, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="3"`);
    o += L(bx + 1.85, 3.9, bx + 1.85, 6.3, COL.stahl, 2.5);
    o += R(bx + 4.4, 3.9, bx + 6.2, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="3"`);
    // Balkon (Platte + Glasbrüstung)
    o += R(bx + 0.3, 3.62, bx + 3.4, 3.8, COL.beton);
    o += R(bx + 0.3, 3.8, bx + 3.4, 4.8, COL.glas, 'opacity="0.35" stroke="#1E2326" stroke-width="2"');
  }
  // Attika/Dachrand Hauptbaukörper mit Glasgeländer und Pflanzen
  o += R(-0.2, 6.5, 24.2, 6.8, COL.beton);
  o += R(3.6, 6.8, 24, 7.6, COL.glas, 'opacity="0.3" stroke="#1E2326" stroke-width="1.5"');
  for (let i = 0; i < 9; i++) o += `<ellipse cx="${X(4 + i * 2.1)}" cy="${Z(7.0)}" rx="${0.5 * s}" ry="${0.35 * s}" fill="${COL.pflanze}"/>`;
  // Staffelgeschoss in Holzbau (x 1,3..22,7, rundum zurückgesetzt, Terrasse ringsum)
  o += R(1.3, 6.8, 22.7, 9.6, COL.zink);
  for (let k = 0; k < 3; k++) {
    const bx = 4.9 + k * 5.93;
    o += R(bx + 0.4, 6.9, bx + 5.5, 9.5, COL.glas, `stroke="${COL.stahl}" stroke-width="3"`);
    o += L(bx + 2.95, 6.9, bx + 2.95, 9.5, COL.stahl, 2.5);
    o += L(bx + 0.4, 8.3, bx + 5.5, 8.3, COL.stahl, 1.5);
  }
  o += R(0.8, 9.6, 23.2, 9.9, COL.beton); // Flachdach mit Überstand
  // Terrasse (Holzdeck) + Vordach-Stützen
  o += `<rect x="${X(3.6) - 15}" y="${gy - 0.4 * s}" width="${20.4 * s + 30}" height="${0.4 * s}" fill="${COL.holz}"/>`;
  for (let i = 0; i < 6; i++) {
    const tx = X(4.3 + i * 3.3);
    o += `<rect x="${tx}" y="${gy - 1.1 * s}" width="${0.9 * s}" height="4" fill="${COL.stahl}"/><rect x="${tx + 0.42 * s}" y="${gy - 1.1 * s}" width="3" height="${0.7 * s}" fill="${COL.stahl}"/>`;
  }
  // Maße
  const dimV = (x, z0, z1, label) =>
    `<line x1="${X(x)}" y1="${Z(z0)}" x2="${X(x)}" y2="${Z(z1)}" stroke="${COL.text}" stroke-width="1.5"/><line x1="${X(x) - 6}" y1="${Z(z0)}" x2="${X(x) + 6}" y2="${Z(z0)}" stroke="${COL.text}" stroke-width="1.5"/><line x1="${X(x) - 6}" y1="${Z(z1)}" x2="${X(x) + 6}" y2="${Z(z1)}" stroke="${COL.text}" stroke-width="1.5"/>` +
    T(X(x) - 10, (Z(z0) + Z(z1)) / 2 + 5, label, 15, 'font-weight="bold" text-anchor="end"');
  o += dimV(-1.0, 0, 6.5, "6,50 m");
  o += dimV(-3.6, 0, 9.9, "ca. 9,90 m");
  o += `<line x1="${X(0)}" y1="${gy + 28}" x2="${X(24)}" y2="${gy + 28}" stroke="${COL.text}" stroke-width="1.5"/>` + T(X(11), gy + 22, "24,0 m", 15, 'font-weight="bold"');
  o += T(X(0), gy + 62, "Eingang", 16, 'font-weight="bold"');
  o += T(X(3.6), gy + 62, "EG: Gastro ca. 290 m² mit Bar und Terrasse", 16, 'font-weight="bold"');
  o += T(X(16.4), gy + 62, "OG und Holz-Staffel mit Terrasse: 6 Wohnungen", 16, 'font-weight="bold"');

  // ---- Ost
  const ox2 = 1010;
  const X2 = (y) => ox2 + y * s;
  const R2 = (y0, z0, y1, z1, fill, extra = "") => `<rect x="${X2(y0)}" y="${Z(z1)}" width="${(y1 - y0) * s}" height="${(z1 - z0) * s}" fill="${fill}" ${extra}/>`;
  o += T(ox2, 140, "Ostansicht (Schmalseite, 14,2 m)", 20, 'font-weight="bold"');
  o += R2(-0.2, 0, 14.4, 0.3, "#5E564F");
  o += R2(0, 0.3, 14.2, 3.5, "url(#glow)");
  for (let i = 0; i <= 7; i++) o += `<line x1="${X2(i * 2.03)}" y1="${Z(0.3)}" x2="${X2(i * 2.03)}" y2="${Z(3.5)}" stroke="${COL.stahl}" stroke-width="2.5"/>`;
  o += R2(-0.2, 3.5, 14.4, 3.8, COL.beton);
  o += R2(0, 3.8, 14.2, 6.5, "url(#b1)");
  [[1.0, 4.4], [9.8, 13.2]].forEach(([a, b]) => (o += R2(a, 3.9, b, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="3"`)));
  o += R2(5.4, 3.9, 8.6, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="3"`);
  o += R2(-0.2, 6.5, 14.4, 6.8, COL.beton);
  o += R2(0, 6.8, 14.2, 7.6, COL.glas, 'opacity="0.3" stroke="#1E2326" stroke-width="1.5"');
  // Staffel zurückgesetzt (heller, entfernter)
  o += R2(1.3, 6.8, 12.9, 9.6, COL.zinkHell);
  for (let k = 0; k < 3; k++) o += R2(1.9 + k * 3.6, 6.9, 4.9 + k * 3.6, 9.5, COL.glas, `stroke="${COL.stahl}" stroke-width="3"`);
  o += R2(0.8, 9.6, 13.4, 9.9, COL.beton);
  o += `<line x1="${X2(0)}" y1="${gy + 28}" x2="${X2(14.2)}" y2="${gy + 28}" stroke="${COL.text}" stroke-width="1.5"/>` + T(X2(5.4), gy + 22, "14,2 m", 15, 'font-weight="bold"');
  o += T(40, 888, "Skizze, nicht maßstäblich genau. Staffelgeschoss in Holzbau mit ca. 250 m², Terrasse ca. 90 m² ringsum, und Gesamthöhe ca. 9,90 m (B-Plan: TH 6,50 m, H 12,00 m): Zulässigkeit mit der Stadt klären. Stand Oktober 2026.", 14);
  o += "</svg>";
  return o;
}

// ---------------------------------------------------------------- Eckansicht (Isometrie)
function ecke() {
  const W = 1600;
  const H = 1000;
  const s = 26;
  const c30 = Math.cos(Math.PI / 6);
  const ox = 533;
  const oy = 360;
  const P = (x, y, z) => [ox + (x - y) * c30 * s, oy + ((x + y) / 2) * s - z * s];
  const poly = (pts, fill, extra = "") => `<polygon points="${pts.map((p) => p.map((v) => v.toFixed(1)).join(",")).join(" ")}" fill="${fill}" ${extra}/>`;
  const A = (Y0) => (u, v) => P(u, Y0, v);
  const B = (X0) => (u, v) => P(X0, u, v);
  const rect = (pl, u0, v0, u1, v1, fill, extra = "") => poly([pl(u0, v0), pl(u1, v0), pl(u1, v1), pl(u0, v1)], fill, extra);
  const line = (a, b, st = COL.stahl, w = 2) => `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}" stroke="${st}" stroke-width="${w}"/>`;

  let o = head(W, H, brick("bs", 30) + brick("bo", -30));
  o += `<rect width="${W}" height="${H}" fill="url(#sky)"/>`;
  o += T(40, 52, "Baufeld 3: Eckansicht modern (Skizze)", 28, 'font-weight="bold"');
  o += T(40, 80, "Flachdach, Staffelgeschoss in Holzbau mit Terrasse rundum, Klinker, Balkone, EG komplett verglast mit Bar-Gastro", 16, `fill="${COL.grau}"`);
  o += poly([P(-2, -2, 0), P(28, -2, 0), P(28, 20.5, 0), P(-2, 20.5, 0)], COL.pflaster);
  for (let i = 0; i < 5; i++) {
    const a = P(26.2, 0.5 + i * 2.7, 0);
    const b = P(27.8, 0.5 + i * 2.7, 0);
    o += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="#F2F2F2" stroke-width="2"/>`;
  }
  o += poly([P(26, -1, 0), P(28, -1, 0), P(28, 15, 0), P(26, 15, 0)], "#6E7378", 'opacity="0.55"');
  // Terrasse
  o += poly([P(3.6, 14.2, 0), P(24.6, 14.2, 0), P(24.6, 19, 0), P(3.6, 19, 0)], COL.holz);
  const Y = 14.2;
  const X = 24;
  const SA = A(Y);
  const SB = B(X);
  // Hauptbaukörper bis 6,5
  o += rect(SA, 0, 0.3, 24, 6.5, "url(#bs)");
  o += rect(SB, 0, 0.3, Y, 6.5, "url(#bo)");
  o += rect(SA, 0, 0, 24, 0.3, "#5E564F") + rect(SB, 0, 0, Y, 0.3, "#4E4740");
  // Eingang Wohnen
  o += rect(SA, 0.7, 0.3, 2.7, 3.3, COL.stahl) + rect(SA, 0.85, 0.5, 2.55, 3.3, COL.glas, 'opacity="0.85"');
  // Gastro-Glas Süd (x 3.6..24) und Ost (y 0..14.2)
  o += rect(SA, 3.6, 0.3, 24, 3.5, "url(#glow)");
  for (let i = 0; i <= 12; i++) o += line(SA(3.6 + i * (20.4 / 12), 0.3), SA(3.6 + i * (20.4 / 12), 3.5), COL.stahl, 2.5);
  o += line(SA(3.6, 2.6), SA(24, 2.6), COL.stahl, 2);
  o += rect(SB, 0, 0.3, Y, 3.5, "url(#glow)");
  for (let i = 0; i <= 7; i++) o += line(SB(i * 2.03, 0.3), SB(i * 2.03, 3.5), COL.stahl, 2.5);
  // Deckenbänder
  o += rect(SA, -0.2, 3.5, 24.2, 3.8, COL.beton) + rect(SB, -0.2, 3.5, Y + 0.2, 3.8, COL.beton);
  // OG Süd: 3 Achsen, Balkone
  for (let k = 0; k < 3; k++) {
    const bx = 3.6 + k * 6.8;
    o += rect(SA, bx + 0.5, 3.9, bx + 3.2, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="2.5"`);
    o += line(SA(bx + 1.85, 3.9), SA(bx + 1.85, 6.3), COL.stahl, 2);
    o += rect(SA, bx + 4.4, 3.9, bx + 6.2, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="2.5"`);
  }
  // OG Ost
  [[1.0, 4.4], [9.8, 13.2]].forEach(([a, b]) => (o += rect(SB, a, 3.9, b, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="2.5"`)));
  o += rect(SB, 5.4, 3.9, 8.6, 6.3, COL.glas, `stroke="${COL.stahl}" stroke-width="2.5"`);
  // Balkone Süd (Platten und Glasbrüstung)
  for (let k = 0; k < 3; k++) {
    const bx = 3.6 + k * 6.8 + 0.3;
    o += poly([P(bx, Y, 3.62), P(bx + 3.1, Y, 3.62), P(bx + 3.1, Y + 1.5, 3.62), P(bx, Y + 1.5, 3.62)], COL.beton);
    o += poly([P(bx, Y + 1.5, 3.62), P(bx + 3.1, Y + 1.5, 3.62), P(bx + 3.1, Y + 1.5, 4.7), P(bx, Y + 1.5, 4.7)], COL.glas, 'opacity="0.4" stroke="#1E2326" stroke-width="2"');
  }
  // Dachterrasse OG-Dach (Ost-Streifen x 21..24 und Süd-Streifen)
  const roofZ = 6.5;
  o += poly([P(22.7, 0, roofZ), P(24, 0, roofZ), P(24, Y, roofZ), P(22.7, Y, roofZ)], "#B9B3A6");
  o += poly([P(0, 12.9, roofZ), P(22.7, 12.9, roofZ), P(22.7, Y, roofZ), P(0, Y, roofZ)], "#B9B3A6");
  // Pflanzkästen
  for (let i = 0; i < 6; i++) {
    const g = P(21.8 + (i % 2) * 1.2, 1 + i * 2.2, roofZ + 0.3);
    o += `<ellipse cx="${g[0]}" cy="${g[1]}" rx="14" ry="9" fill="${COL.pflanze}"/>`;
  }
  // Attika und Glasgeländer
  o += poly([P(21, 0, roofZ), P(24, 0, roofZ + 1.0), P(24, Y, roofZ + 1.0), P(24, Y, roofZ)], "#FFF", 'opacity="0"');
  o += poly([P(24, 0, roofZ), P(24, Y, roofZ), P(24, Y, roofZ + 1.0), P(24, 0, roofZ + 1.0)], COL.glas, 'opacity="0.3" stroke="#1E2326" stroke-width="1.5"');
  o += poly([P(0, Y, roofZ), P(24, Y, roofZ), P(24, Y, roofZ + 1.0), P(0, Y, roofZ + 1.0)], COL.glas, 'opacity="0.3" stroke="#1E2326" stroke-width="1.5"');
  o += rect(SA, -0.2, 6.5, 24.2, 6.8, COL.beton) + rect(SB, -0.2, 6.5, Y + 0.2, 6.8, COL.beton);
  // Treppenhausblock bis 9,9 (Süd, flach mit Fassade)
  // Staffelgeschoss Süd (y=13.3) und Ost (x=21)
  const SS = A(12.9);
  const SO = B(22.7);
  o += rect(SS, 1.3, 6.5, 22.7, 9.6, COL.zink);
  for (let k = 0; k < 3; k++) {
    const bx = 4.9 + k * 5.93;
    o += rect(SS, bx + 0.4, 6.7, bx + 5.5, 9.5, COL.glas, `stroke="${COL.stahl}" stroke-width="2.5"`);
    o += line(SS(bx + 2.95, 6.7), SS(bx + 2.95, 9.5), COL.stahl, 2);
  }
  o += rect(SO, 1.3, 6.5, 12.9, 9.6, COL.zinkHell);
  [[2.0, 5.0], [5.6, 8.6], [9.2, 12.2]].forEach(([a, b]) => (o += rect(SO, a, 6.7, b, 9.5, COL.glas, `stroke="${COL.stahl}" stroke-width="2.5"`)));
  // Flachdach-Platte Staffel (Oberseite + Kante)
  o += poly([P(0.8, 0.8, 9.9), P(23.2, 0.8, 9.9), P(23.2, 13.4, 9.9), P(0.8, 13.4, 9.9)], "#B4BAC0");
  o += poly([P(0.8, 13.4, 9.6), P(23.2, 13.4, 9.6), P(23.2, 13.4, 9.9), P(0.8, 13.4, 9.9)], COL.beton);
  o += poly([P(23.2, 0.8, 9.6), P(23.2, 13.4, 9.6), P(23.2, 13.4, 9.9), P(23.2, 0.8, 9.9)], "#C4BFB5");
  // Terrassenstützen und Vordach
  [3.6, 7.0, 10.4, 13.8, 17.2, 20.6, 24.6].forEach((u) => (o += line(P(u, 19, 0), P(u, 19, 3.5), COL.stahl, 4)));
  [19, 16.6, 14.2].forEach((y) => (o += line(P(24.6, y, 0), P(24.6, y, 3.5), COL.stahl, 4)));
  o += poly([P(3.6, 14.2, 3.55), P(24.6, 14.2, 3.55), P(24.6, 19, 3.55), P(3.6, 19, 3.55)], COL.stahl, 'opacity="0.28"');
  // Bäume
  const tree = (x, y) => {
    const g = P(x, y, 0);
    return `<rect x="${g[0] - 4}" y="${g[1] - 110}" width="8" height="110" fill="#5A4A3A"/><ellipse cx="${g[0]}" cy="${g[1] - 150}" rx="62" ry="80" fill="#5E8C4B"/><ellipse cx="${g[0] - 14}" cy="${g[1] - 166}" rx="38" ry="48" fill="#76A45F" opacity="0.8"/>`;
  };
  o += tree(-1.5, 18.5);
  o += tree(27.5, -0.5);
  // Legende
  const leg = [
    ["Staffelgeschoss", "3 Penthouses in Holzbau, Terrasse rundum, Attika ca. 9,90 m"],
    ["1. Obergeschoss", "3 Wohnungen mit Balkon, Klinker, bodentiefe Fenster"],
    ["Erdgeschoss", "Gastro ca. 290 m² mit Bar, vollverglast, Terrasse mit Vordach"],
    ["Eingang Wohnen", "Treppenhaus mit Aufzug am Westende, ruhig getrennt"],
    ["Stellplätze", "ca. 10–13 auf dem Grundstück, Rest über die Parkfläche"],
  ];
  leg.forEach((l, i) => {
    o += `<rect x="1230" y="${150 + i * 120}" width="330" height="100" rx="10" fill="#FFFFFF" opacity="0.85"/>`;
    o += T(1246, 182 + i * 120, l[0], 19, 'font-weight="bold"');
    o += `<foreignObject x="1246" y="${192 + i * 120}" width="300" height="56"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:15px;color:#5B6770;line-height:1.25">${l[1]}</div></foreignObject>`;
  });
  o += T(40, 968, "Skizze, nicht maßstäblich genau. Staffelgeschoss und Gesamthöhe ca. 9,90 m müssen mit der Stadt abgestimmt werden. Stand Oktober 2026.", 14);
  o += "</svg>";
  return o;
}

// ---------------------------------------------------------------- Innen
function innen() {
  const W = 1600;
  const H = 1000;
  let o = head(W, H);
  o += `<rect width="${W}" height="${H}" fill="#FFFFFF"/>`;
  o += T(40, 52, "Gastro innen 2026: Grundriss mit Bar, Wandansicht und Materialien (Konzeptskizze)", 28, 'font-weight="bold"');
  const s = 30;
  const ox = 50;
  const oy = 150;
  const m = (v) => v * s;
  const wBlock = 3.6;
  const rw = 20.4;
  const rh = 14.2;
  o += T(ox, oy - 14, "Grundriss Erdgeschoss: Gastro ca. 290 m² mit Bar, Terrasse davor", 20, 'font-weight="bold"');
  // Treppenblock
  o += `<rect x="${ox}" y="${oy}" width="${m(wBlock)}" height="${m(rh)}" fill="#E1DDD6" stroke="${COL.stahl}" stroke-width="5"/>`;
  o += T(ox + 8, oy + m(6.5), "Treppe", 14, 'font-weight="bold"') + T(ox + 8, oy + m(7.2), "Aufzug", 14, 'font-weight="bold"') + T(ox + 8, oy + m(8.4), "Technik", 14);
  o += `<rect x="${ox + 4}" y="${oy + m(rh) - 10}" width="${m(2)}" height="12" fill="#fff" stroke="${COL.stahl}" stroke-width="2"/>` + T(ox + 4, oy + m(rh) - 16, "Eingang Wohnen", 12, 'font-weight="bold"');
  // Gastroraum
  const gx = ox + m(wBlock);
  o += `<rect x="${gx}" y="${oy}" width="${m(rw)}" height="${m(rh)}" fill="#F7F4EF" stroke="${COL.stahl}" stroke-width="5"/>`;
  // Küche, WC, Lager (Nordseite)
  o += `<rect x="${gx + m(12.4)}" y="${oy}" width="${m(8)}" height="${m(4.2)}" fill="#D9DEE2" stroke="${COL.stahl}" stroke-width="3"/>` + T(gx + m(14.6), oy + m(2.4), "Küche", 18, 'font-weight="bold"');
  o += `<rect x="${gx + m(8.4)}" y="${oy}" width="${m(4)}" height="${m(4.2)}" fill="#E6E2DC" stroke="${COL.stahl}" stroke-width="3"/>` + T(gx + m(9.0), oy + m(2.4), "WC, Lager", 15, 'font-weight="bold"');
  // Bar (Nordwest)
  o += `<rect x="${gx + m(0.4)}" y="${oy + m(0.2)}" width="${m(7.6)}" height="${m(0.5)}" fill="#E8C879" opacity="0.7"/>`;
  o += `<rect x="${gx + m(0.4)}" y="${oy + m(0.7)}" width="${m(7.6)}" height="${m(0.9)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="2"/>` + T(gx + m(2.8), oy + m(1.35), "Bar", 16, 'font-weight="bold" fill="#fff"');
  let seats = 0;
  for (let i = 0; i < 10; i++) {
    o += `<circle cx="${gx + m(0.9 + i * 0.72)}" cy="${oy + m(2.1)}" r="${m(0.2)}" fill="${COL.gruen}"/>`;
    seats++;
  }
  // Lounge
  o += `<rect x="${gx + m(0.4)}" y="${oy + m(3.0)}" width="${m(2.0)}" height="${m(0.8)}" fill="#E7DCC8" stroke="${COL.stahl}" stroke-width="1.5"/>` + `<rect x="${gx + m(3.4)}" y="${oy + m(3.0)}" width="${m(2.0)}" height="${m(0.8)}" fill="#E7DCC8" stroke="${COL.stahl}" stroke-width="1.5"/>`;
  o += `<rect x="${gx + m(2.7)}" y="${oy + m(3.6)}" width="${m(0.5)}" height="${m(0.5)}" fill="${COL.holz}"/>`;
  seats += 8;
  const t4 = (x, y) => {
    o += `<rect x="${gx + m(x)}" y="${oy + m(y)}" width="${m(1.1)}" height="${m(0.9)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="1.5"/>`;
    [[-0.3, 0.05], [-0.3, 0.55], [1.1, 0.05], [1.1, 0.55]].forEach(([dx, dy]) => (o += `<rect x="${gx + m(x + dx)}" y="${oy + m(y + dy)}" width="${m(0.3)}" height="${m(0.3)}" fill="${COL.gruen}" rx="4"/>`));
    seats += 4;
  };
  const t2 = (x, y) => {
    o += `<rect x="${gx + m(x)}" y="${oy + m(y)}" width="${m(0.8)}" height="${m(0.8)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="1.5"/>`;
    [[-0.3, 0.25], [0.8, 0.25]].forEach(([dx, dy]) => (o += `<rect x="${gx + m(x + dx)}" y="${oy + m(y + dy)}" width="${m(0.3)}" height="${m(0.3)}" fill="${COL.gruen}" rx="4"/>`));
    seats += 2;
  };
  [5.6, 7.8, 10.0].forEach((y) => [1.4, 4.7, 8.0, 11.3, 14.6, 17.9].forEach((x) => t4(x, y)));
  [1.4, 4.7, 8.0, 11.3, 14.6, 17.9].forEach((x) => t2(x, 12.2));
  // Glasfront Süd
  o += `<rect x="${gx}" y="${oy + m(rh) - 8}" width="${m(rw)}" height="10" fill="${COL.glas}"/>`;
  for (let i = 0; i <= 12; i++) o += `<rect x="${gx + m((rw / 12) * i) - 2}" y="${oy + m(rh) - 10}" width="4" height="14" fill="${COL.stahl}"/>`;
  o += `<rect x="${gx + m(9)}" y="${oy + m(rh) - 12}" width="${m(1.6)}" height="14" fill="#FFFFFF" stroke="${COL.stahl}" stroke-width="2"/>` + T(gx + m(8.6), oy + m(rh) - 20, "Eingang Gastro", 13, 'font-weight="bold"');
  // Terrasse
  o += `<rect x="${gx - m(0.4)}" y="${oy + m(rh) + 8}" width="${m(rw) + m(0.8)}" height="${m(4.4)}" fill="#D6B98F" stroke="${COL.stahl}" stroke-width="2" stroke-dasharray="8 6"/>`;
  let ts = 0;
  for (let i = 0; i < 8; i++) {
    const x = gx + m(0.7 + i * 2.5);
    o += `<circle cx="${x + m(0.5)}" cy="${oy + m(rh) + m(1.4)}" r="${m(0.5)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="1.5"/>`;
    ts += 4;
  }
  o += T(gx + m(0.4), oy + m(rh) + m(3.6), `Terrasse (Holzdeck unter Vordach), ca. ${ts} Plätze`, 15, 'font-weight="bold"');
  o += T(ox, oy + m(rh) + m(5.4), `Plätze innen in der Skizze: ${seats} (inkl. 10 Barhocker und Lounge), also ca. 100 Plätze. Möblierung ist Entwurf.`, 14, `fill="${COL.grau}"`);

  // ---- Wandansicht
  const wx = 820;
  const wy = 150;
  const ww = 730;
  const wh = 440;
  o += T(wx, wy - 14, "Wandansicht Bar (Stimmung, modern)", 20, 'font-weight="bold"');
  o += `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="${COL.gruen}"/>`;
  o += `<rect x="${wx}" y="${wy}" width="${ww}" height="14" fill="#F5D590"/>`;
  // Backbar beleuchtet
  o += `<rect x="${wx + 40}" y="${wy + 60}" width="420" height="190" fill="#2A1F1A" stroke="${COL.gold}" stroke-width="5"/>`;
  o += `<rect x="${wx + 46}" y="${wy + 66}" width="408" height="178" fill="url(#lamp)" opacity="0.9"/>`;
  [0, 1].forEach((r) => {
    o += `<rect x="${wx + 40}" y="${wy + 60 + 95 * r + 88}" width="420" height="5" fill="${COL.gold}"/>`;
    for (let i = 0; i < 16; i++) o += `<rect x="${wx + 56 + i * 25}" y="${wy + 60 + 95 * r + 38}" width="11" height="50" rx="4" fill="${["#3C6E47", "#C49A45", "#222", "#7A3A2C"][i % 4]}"/>`;
  });
  // Terrazzo-Bartheke
  o += `<rect x="${wx + 20}" y="${wy + 290}" width="460" height="46" fill="#D8D2C6"/>`;
  for (let i = 0; i < 60; i++) o += `<circle cx="${wx + 24 + ((i * 53) % 450)}" cy="${wy + 294 + ((i * 17) % 38)}" r="${1.5 + (i % 3)}" fill="${["#8E7C66", "#B9A58A", "#6E7C70"][i % 3]}" opacity="0.7"/>`;
  o += `<rect x="${wx + 20}" y="${wy + 336}" width="460" height="104" fill="#243A31"/>`;
  for (let i = 0; i < 12; i++) o += `<line x1="${wx + 20 + i * 38.4}" y1="${wy + 340}" x2="${wx + 20 + i * 38.4}" y2="${wy + 440}" stroke="#355247" stroke-width="3"/>`;
  [90, 210, 330, 440].forEach((x) => (o += `<circle cx="${wx + x}" cy="${wy + 270}" r="22" fill="#F1E8D8" stroke="#2B2B2B" stroke-width="3"/><rect x="${wx + x - 3}" y="${wy + 292}" width="6" height="${wh - 292}" fill="${COL.stahl}"/>`));
  // Pendelleuchten
  [[110, 30], [260, 20], [410, 30]].forEach(([x, y]) => {
    o += `<line x1="${wx + x}" y1="${wy + 14}" x2="${wx + x}" y2="${wy + 36 + y}" stroke="#E8C879" stroke-width="2"/><circle cx="${wx + x}" cy="${wy + 50 + y}" r="14" fill="#FFF3D1" stroke="${COL.gold}" stroke-width="3"/><circle cx="${wx + x}" cy="${wy + 50 + y}" r="60" fill="url(#lamp)"/>`;
  });
  // Stahl-Glas-Wand
  o += `<rect x="${wx + 520}" y="${wy + 40}" width="190" height="300" fill="#C7D8DE" opacity="0.55" stroke="${COL.stahl}" stroke-width="6"/>`;
  for (let i = 1; i < 3; i++) o += `<line x1="${wx + 520 + (190 / 3) * i}" y1="${wy + 40}" x2="${wx + 520 + (190 / 3) * i}" y2="${wy + 340}" stroke="${COL.stahl}" stroke-width="4"/>`;
  for (let i = 1; i < 5; i++) o += `<line x1="${wx + 520}" y1="${wy + 40 + 60 * i}" x2="${wx + 710}" y2="${wy + 40 + 60 * i}" stroke="${COL.stahl}" stroke-width="4"/>`;
  // Bouclé-Lounge
  o += `<rect x="${wx + 520}" y="${wy + 350}" width="190" height="70" rx="26" fill="#EDE5D6"/><rect x="${wx + 540}" y="${wy + 318}" width="150" height="46" rx="18" fill="#F4EEE2"/>`;
  // Pflanze
  o += `<rect x="${wx + 492}" y="${wy + 360}" width="22" height="70" fill="#7A5A38"/><ellipse cx="${wx + 503}" cy="${wy + 345}" rx="30" ry="40" fill="${COL.pflanze}"/>`;
  // Materialpalette
  const py = 650;
  o += T(wx, py - 20, "Materialpalette 2026", 20, 'font-weight="bold"');
  [["Dunkelgrün", COL.gruen, "Wände, Nischen"], ["Klinker dunkel", COL.klinker, "Fassade, Pfeiler"], ["Eiche warm", COL.holz, "Theke, Tische"], ["Terrazzo hell", "#D8D2C6", "Bartheke, Boden"], ["Bouclé creme", "#EDE5D6", "Sitzmöbel"], ["Messing", COL.gold, "Leuchten, Regale"], ["Stahl schwarz", COL.stahl, "Glaswand, Rahmen"]].forEach(([n, c, u], i) => {
    const x = wx + (i % 4) * 185;
    const y = py + Math.floor(i / 4) * 130;
    o += `<rect x="${x}" y="${y}" width="165" height="70" rx="10" fill="${c}" stroke="#ccc"/>`;
    o += T(x, y + 92, n, 16, 'font-weight="bold"') + T(x, y + 112, u, 14, `fill="${COL.grau}"`);
  });
  o += T(40, 968, "Konzeptskizze nach dem Referenzbild (Innenraum), neu und modern gedacht. Planung folgt mit dem Gastro-Fachplaner.", 14);
  o += "</svg>";
  return o;
}

fs.writeFileSync(path.join(OUT, "skizze_aussen_ansichten.svg"), ansichten());
fs.writeFileSync(path.join(OUT, "skizze_aussen_ecke.svg"), ecke());
fs.writeFileSync(path.join(OUT, "skizze_innen_konzept.svg"), innen());
console.log("SVG geschrieben");
