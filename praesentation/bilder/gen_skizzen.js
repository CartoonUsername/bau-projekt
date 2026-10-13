// Erzeugt SVG-Skizzen zu Baufeld 3 (Außenansichten, Perspektive, Innenkonzept)
// Maße: Gebäude 24 x 14,2 m, Sockel 0,30 m, Traufe 6,50 m, First 12,00 m, Satteldach ca. 38°
const fs = require("fs");
const path = require("path");
const OUT = process.env.OUT || __dirname;

const COL = {
  klinker: "#9A4034",
  klinkerDunkel: "#7C3228",
  fuge: "#C9B8A6",
  dach: "#3B4148",
  dachHell: "#4A525A",
  glas: "#C9DCE6",
  glasWarm: "#F2C879",
  stahl: "#23282C",
  holz: "#B88652",
  beton: "#D8D3CA",
  himmel1: "#BFD9EA",
  himmel2: "#EAF2F7",
  gruen: "#2F4A3E",
  gold: "#C49A45",
  pflaster: "#B0675A",
  text: "#1F2421",
  grau: "#5B6770",
};

const head = (w, h, defs = "") =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" font-family="Calibri, Carlito, Arial, sans-serif">
<defs>${defs}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${COL.himmel1}"/><stop offset="1" stop-color="${COL.himmel2}"/></linearGradient>
<linearGradient id="glow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7D58B"/><stop offset="1" stop-color="#E8A94F"/></linearGradient>
</defs>`;

const brick = (id, skew = 0, size = 1) =>
  `<pattern id="${id}" width="${24 * size}" height="${16 * size}" patternUnits="userSpaceOnUse" ${skew ? `patternTransform="skewY(${skew})"` : ""}>
  <rect width="${24 * size}" height="${16 * size}" fill="${COL.klinker}"/>
  <rect y="${7.2 * size}" width="${24 * size}" height="${1.6 * size}" fill="${COL.fuge}" opacity="0.55"/>
  <rect y="${15.2 * size}" width="${24 * size}" height="${0.8 * size}" fill="${COL.fuge}" opacity="0.55"/>
  <rect x="${5 * size}" y="0" width="${1.4 * size}" height="${7.2 * size}" fill="${COL.fuge}" opacity="0.55"/>
  <rect x="${17 * size}" y="${8.8 * size}" width="${1.4 * size}" height="${6.4 * size}" fill="${COL.fuge}" opacity="0.55"/>
</pattern>`;

const T = (x, y, s, size = 16, opt = "") =>
  `<text x="${x}" y="${y}" font-size="${size}" fill="${COL.text}" ${opt}>${s}</text>`;

// ---------------------------------------------------------------- Außenansichten
function ansichten() {
  const W = 1600;
  const H = 910;
  const s = 30; // px je m
  let o = head(W, H, brick("b1") + brick("b2", 0, 1));
  o += `<rect width="${W}" height="${H}" fill="url(#sky)"/>`;
  o += T(40, 52, "Baufeld 3, Neue Mitte Werlte: Ansichten (Skizze)", 28, 'font-weight="bold"');
  o += T(40, 80, "Satteldach ca. 38°, Traufe 6,50 m, First 12,00 m, drei Ebenen, Klinker rot, Glasfront im Erdgeschoss", 16, `fill="${COL.grau}"`);

  // ---- Südansicht (Traufseite), Gastro am rechten Ende
  const ox = 200;
  const gy = 780; // Geländelinie
  const bw = 24 * s;
  const m = (v) => v * s;
  o += T(ox, 140, "Südansicht (Traufseite, 24 m)", 20, 'font-weight="bold"');
  o += `<rect x="0" y="${gy}" width="${W}" height="${H - gy}" fill="${COL.pflaster}" opacity="0.9"/>`;
  const yEG = gy - m(0.3) - m(3.5);
  const yOG = yEG - m(3.0);
  const yFirst = gy - m(0.3) - m(12);
  // Dach (Traufseite: Rechteck zwischen Traufe und First)
  o += `<polygon points="${ox - 10},${yOG} ${ox + bw + 10},${yOG} ${ox + bw + 10},${yFirst} ${ox - 10},${yFirst}" fill="${COL.dach}"/>`;
  for (let i = 1; i < 12; i++) o += `<line x1="${ox - 10}" y1="${yFirst + ((yOG - yFirst) / 12) * i}" x2="${ox + bw + 10}" y2="${yFirst + ((yOG - yFirst) / 12) * i}" stroke="${COL.dachHell}" stroke-width="1"/>`;
  // Gauben (Penthouses): 2 je Penthouse
  [3.2, 7.2, 14.2, 18.2].forEach((gx) => {
    const x = ox + m(gx);
    o += `<rect x="${x}" y="${yFirst + m(1.3)}" width="${m(2.4)}" height="${m(2.4)}" fill="${COL.beton}"/>`;
    o += `<rect x="${x + m(0.2)}" y="${yFirst + m(1.5)}" width="${m(2.0)}" height="${m(1.9)}" fill="${COL.glas}" stroke="${COL.stahl}" stroke-width="3"/>`;
    o += `<line x1="${x + m(1.2)}" y1="${yFirst + m(1.5)}" x2="${x + m(1.2)}" y2="${yFirst + m(3.4)}" stroke="${COL.stahl}" stroke-width="3"/>`;
    o += `<rect x="${x - m(0.15)}" y="${yFirst + m(1.15)}" width="${m(2.7)}" height="${m(0.2)}" fill="${COL.dach}"/>`;
  });
  // Dachloggien (Dachterrasse) mittig je Penthouse
  [[10.8, 4.4], [21.2, 4.4]].forEach(([gx]) => {});
  // OG
  o += `<rect x="${ox}" y="${yOG}" width="${bw}" height="${m(3.0)}" fill="url(#b1)"/>`;
  o += `<rect x="${ox - 6}" y="${yOG - 6}" width="${bw + 12}" height="8" fill="${COL.beton}"/>`; // Traufbalken
  // Fenster und Loggien OG (3 Wohnungen, je 8 m)
  for (let k = 0; k < 3; k++) {
    const bx = ox + m(k * 8);
    // zwei Fenster
    [1.0, 3.2].forEach((fx) => {
      o += `<rect x="${bx + m(fx)}" y="${yOG + m(0.5)}" width="${m(1.3)}" height="${m(2.2)}" fill="${COL.glas}" stroke="${COL.beton}" stroke-width="5"/>`;
      o += `<line x1="${bx + m(fx + 0.65)}" y1="${yOG + m(0.5)}" x2="${bx + m(fx + 0.65)}" y2="${yOG + m(2.7)}" stroke="${COL.stahl}" stroke-width="2"/>`;
    });
    // Loggia
    const lx = bx + m(5.4);
    o += `<rect x="${lx}" y="${yOG + m(0.35)}" width="${m(2.3)}" height="${m(2.5)}" fill="#3A2B28"/>`;
    o += `<rect x="${lx + m(0.35)}" y="${yOG + m(0.6)}" width="${m(1.6)}" height="${m(2.2)}" fill="${COL.glas}" opacity="0.85"/>`;
    for (let r = 0; r < 12; r++) o += `<line x1="${lx + m(0.1) + r * m(0.18)}" y1="${yOG + m(1.9)}" x2="${lx + m(0.1) + r * m(0.18)}" y2="${yOG + m(2.85)}" stroke="${COL.stahl}" stroke-width="2"/>`;
    o += `<rect x="${lx}" y="${yOG + m(1.85)}" width="${m(2.3)}" height="3" fill="${COL.stahl}"/>`;
  }
  // Deckenband über EG
  o += `<rect x="${ox - 6}" y="${yEG - 8}" width="${bw + 12}" height="14" fill="${COL.beton}"/>`;
  // EG: links Treppe/Technik + Büro (Klinker, Eingang), rechts Gastro (Glas)
  o += `<rect x="${ox}" y="${yEG}" width="${m(10.6)}" height="${m(3.5)}" fill="url(#b1)"/>`;
  // Büro-Fenster
  o += `<rect x="${ox + m(0.8)}" y="${yEG + m(0.6)}" width="${m(2.2)}" height="${m(2.4)}" fill="${COL.glas}" stroke="${COL.beton}" stroke-width="5"/>`;
  o += `<rect x="${ox + m(3.4)}" y="${yEG + m(0.6)}" width="${m(2.2)}" height="${m(2.4)}" fill="${COL.glas}" stroke="${COL.beton}" stroke-width="5"/>`;
  // Wohnungseingang
  o += `<rect x="${ox + m(7.2)}" y="${yEG + m(0.5)}" width="${m(2.2)}" height="${m(3.0)}" fill="${COL.stahl}"/>`;
  o += `<rect x="${ox + m(7.4)}" y="${yEG + m(0.7)}" width="${m(1.8)}" height="${m(2.8)}" fill="${COL.glas}" opacity="0.8"/>`;
  // Glasfront Gastro
  const gx0 = ox + m(10.6);
  o += `<rect x="${gx0}" y="${yEG}" width="${m(13.4)}" height="${m(3.5)}" fill="url(#glow)"/>`;
  for (let i = 0; i <= 13; i++) o += `<line x1="${gx0 + m(i * (13.4 / 13))}" y1="${yEG}" x2="${gx0 + m(i * (13.4 / 13))}" y2="${yEG + m(3.5)}" stroke="${COL.stahl}" stroke-width="3"/>`;
  o += `<line x1="${gx0}" y1="${yEG + m(2.6)}" x2="${gx0 + m(13.4)}" y2="${yEG + m(2.6)}" stroke="${COL.stahl}" stroke-width="3"/>`;
  o += `<rect x="${gx0 + m(5.4)}" y="${yEG + m(0.6)}" width="${m(1.5)}" height="${m(2.9)}" fill="${COL.stahl}" opacity="0.25"/>`; // Tür
  // Pendelleuchten Silhouetten
  for (let i = 0; i < 6; i++) o += `<circle cx="${gx0 + m(1.5 + i * 2.2)}" cy="${yEG + m(0.8)}" r="${m(0.22)}" fill="#FFF3D1"/>`;
  // Terrasse davor (Holz) mit Stahlstützen
  o += `<rect x="${gx0 - m(0.6)}" y="${gy - m(0.45)}" width="${m(14.6)}" height="${m(0.45)}" fill="${COL.holz}"/>`;
  [0, 3, 6, 9, 12, 13.4].forEach((px) => {
    o += `<rect x="${gx0 + m(px) - 3}" y="${yEG - 4}" width="6" height="${gy - yEG - m(0.3)}" fill="${COL.stahl}"/>`;
  });
  // Tische auf Terrasse
  for (let i = 0; i < 6; i++) {
    const tx = gx0 + m(0.8 + i * 2.2);
    o += `<rect x="${tx}" y="${gy - m(1.15)}" width="${m(0.9)}" height="4" fill="${COL.stahl}"/><rect x="${tx + m(0.42)}" y="${gy - m(1.15)}" width="3" height="${m(0.7)}" fill="${COL.stahl}"/>`;
    o += `<rect x="${tx - m(0.3)}" y="${gy - m(0.85)}" width="${m(0.3)}" height="${m(0.4)}" fill="${COL.holz}"/><rect x="${tx + m(0.95)}" y="${gy - m(0.85)}" width="${m(0.3)}" height="${m(0.4)}" fill="${COL.holz}"/>`;
  }
  // Sockel
  o += `<rect x="${ox - 6}" y="${gy - m(0.3)}" width="${bw + 12}" height="${m(0.3)}" fill="#6B625A"/>`;
  // Maße
  const dim = (x1, y1, x2, y2, label, vertical = false) => {
    let r = `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${COL.text}" stroke-width="1.5"/>`;
    r += `<line x1="${x1 - (vertical ? 6 : 0)}" y1="${y1 - (vertical ? 0 : 6)}" x2="${x1 + (vertical ? 6 : 0)}" y2="${y1 + (vertical ? 0 : 6)}" stroke="${COL.text}" stroke-width="1.5"/>`;
    r += `<line x1="${x2 - (vertical ? 6 : 0)}" y1="${y2 - (vertical ? 0 : 6)}" x2="${x2 + (vertical ? 6 : 0)}" y2="${y2 + (vertical ? 0 : 6)}" stroke="${COL.text}" stroke-width="1.5"/>`;
    r += vertical ? T(x1 - 10, (y1 + y2) / 2 + 5, label, 15, 'font-weight="bold" text-anchor="end"') : T((x1 + x2) / 2 - 14, y1 - 8, label, 15, 'font-weight="bold"');
    return r;
  };
  o += dim(ox - 120, gy - m(0.3), ox - 120, yFirst, "12,00 m", true);
  o += dim(ox - 40, gy - m(0.3), ox - 40, yOG, "6,50 m", true);
  o += dim(ox, gy + 28, ox + bw, gy + 28, "24,0 m");
  o += T(ox + m(0.5), yEG + m(3.5) + 22, "", 1);
  o += T(ox + m(10.6), gy + 62, "Gastro 190 m²: Glasfront mit Stahlstützen, Terrasse", 16, 'font-weight="bold"');
  o += T(ox, gy + 62, "Büro 70 m², Eingang Wohnen", 16, 'font-weight="bold"');

  // ---- Ostansicht (Giebelseite)
  const ox2 = 1010;
  const gw = 14 * s; // 14 m
  o += T(ox2, 140, "Ostansicht (Giebelseite, 14 m)", 20, 'font-weight="bold"');
  const yE2 = gy - m(0.3) - m(3.5);
  const yO2 = yE2 - m(3.0);
  const yF2 = gy - m(0.3) - m(12);
  // Giebel
  o += `<polygon points="${ox2 - 10},${yO2} ${ox2 + gw + 10},${yO2} ${ox2 + gw / 2},${yF2}" fill="${COL.dach}"/>`;
  o += `<polygon points="${ox2 + 2},${yO2 - 4} ${ox2 + gw - 2},${yO2 - 4} ${ox2 + gw / 2},${yF2 + 12}" fill="url(#b1)"/>`;
  // Giebelfenster Penthouse
  o += `<rect x="${ox2 + m(4.8)}" y="${yO2 - m(2.3)}" width="${m(1.7)}" height="${m(1.9)}" fill="${COL.glas}" stroke="${COL.beton}" stroke-width="5"/>`;
  o += `<rect x="${ox2 + m(7.5)}" y="${yO2 - m(2.3)}" width="${m(1.7)}" height="${m(1.9)}" fill="${COL.glas}" stroke="${COL.beton}" stroke-width="5"/>`;
  o += `<rect x="${ox2}" y="${yO2}" width="${gw}" height="${m(3.0)}" fill="url(#b1)"/>`;
  o += `<rect x="${ox2 - 6}" y="${yO2 - 6}" width="${gw + 12}" height="8" fill="${COL.beton}"/>`;
  [1.2, 8.6].forEach((fx) => {
    o += `<rect x="${ox2 + m(fx)}" y="${yO2 + m(0.5)}" width="${m(1.3)}" height="${m(2.2)}" fill="${COL.glas}" stroke="${COL.beton}" stroke-width="5"/>`;
  });
  const lx2 = ox2 + m(4.7);
  o += `<rect x="${lx2}" y="${yO2 + m(0.35)}" width="${m(2.6)}" height="${m(2.5)}" fill="#3A2B28"/>`;
  o += `<rect x="${lx2 + m(0.35)}" y="${yO2 + m(0.6)}" width="${m(1.9)}" height="${m(2.2)}" fill="${COL.glas}" opacity="0.85"/>`;
  o += `<rect x="${ox2 - 6}" y="${yE2 - 8}" width="${gw + 12}" height="14" fill="${COL.beton}"/>`;
  o += `<rect x="${ox2}" y="${yE2}" width="${gw}" height="${m(3.5)}" fill="url(#b1)"/>`;
  // Glasfront wrap (Ecke): Gastro greift um die Ecke
  o += `<rect x="${ox2}" y="${yE2}" width="${m(9.5)}" height="${m(3.5)}" fill="url(#glow)"/>`;
  for (let i = 0; i <= 5; i++) o += `<line x1="${ox2 + m(i * 1.9)}" y1="${yE2}" x2="${ox2 + m(i * 1.9)}" y2="${yE2 + m(3.5)}" stroke="${COL.stahl}" stroke-width="3"/>`;
  o += `<rect x="${ox2 + m(11)}" y="${yE2 + m(0.5)}" width="${m(2.2)}" height="${m(2.4)}" fill="${COL.glas}" stroke="${COL.beton}" stroke-width="5"/>`;
  o += `<rect x="${ox2 - 6}" y="${gy - m(0.3)}" width="${gw + 12}" height="${m(0.3)}" fill="#6B625A"/>`;
  o += `<rect x="${ox2 - m(0.6)}" y="${gy - m(0.45)}" width="${m(10.2)}" height="${m(0.45)}" fill="${COL.holz}"/>`;
  o += dim(ox2, gy + 28, ox2 + gw, gy + 28, "14,2 m");
  o += `<line x1="${ox2 + gw + 40}" y1="${yO2}" x2="${ox2 + gw + 40}" y2="${yF2}" stroke="${COL.text}" stroke-width="1.5"/>` + T(ox2 + gw + 50, (yO2 + yF2) / 2 + 5, "Dach 38°", 15, 'font-weight="bold"');
  o += T(40, 888, "Skizze, nicht maßstäblich genau. Aufteilung und Details werden mit dem Architekten festgelegt. Stand Oktober 2026.", 14, `fill="${COL.text}"`);
  o += "</svg>";
  return o;
}

// ---------------------------------------------------------------- Isometrie
function perspektive() {
  const W = 1600;
  const H = 1000;
  const s = 26;
  const c30 = Math.cos(Math.PI / 6);
  const ox = 533;
  const oy = 337;
  const P = (x, y, z) => [ox + (x - y) * c30 * s, oy + ((x + y) / 2) * s - z * s];
  const poly = (pts, fill, extra = "") => `<polygon points="${pts.map((p) => p.map((v) => v.toFixed(1)).join(",")).join(" ")}" fill="${fill}" ${extra}/>`;
  // Ebene A: y=Y0 (Südfläche, u = x), Ebene B: x=X0 (Ostfläche, u = y)
  const A = (Y0) => (u, v) => P(u, Y0, v);
  const B = (X0) => (u, v) => P(X0, u, v);
  const rect = (pl, u0, v0, u1, v1, fill, extra = "") => poly([pl(u0, v0), pl(u1, v0), pl(u1, v1), pl(u0, v1)], fill, extra);
  const line = (a, b, st = COL.stahl, w = 2) => `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}" stroke="${st}" stroke-width="${w}"/>`;

  let o = head(W, H, brick("bs", 30) + brick("bo", -30));
  o += `<rect width="${W}" height="${H}" fill="url(#sky)"/>`;
  o += T(40, 52, "Baufeld 3: Eckansicht mit Satteldach (Skizze)", 28, 'font-weight="bold"');
  o += T(40, 80, "Südfassade mit Gastro-Glasfront und Terrasse, Giebelseite nach Osten", 16, `fill="${COL.grau}"`);
  // Boden
  o += poly([P(-2, -2, 0), P(28, -2, 0), P(28, 20.5, 0), P(-2, 20.5, 0)], "#C9B09E");
  // Parkflächen rechts (Ost)
  for (let i = 0; i < 5; i++) {
    const a = P(26.2, 0.5 + i * 2.7, 0);
    const b = P(27.8, 0.5 + i * 2.7, 0);
    o += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="#F2F2F2" stroke-width="2"/>`;
  }
  o += poly([P(26, -1, 0), P(28, -1, 0), P(28, 15, 0), P(26, 15, 0)], "#6E7378", 'opacity="0.55"');
  // Terrasse (Holz) vor der Südseite, Gastro Ost-Ende x 10.6..24
  o += poly([P(10, 14.2, 0), P(24.6, 14.2, 0), P(24.6, 19, 0), P(10, 19, 0)], COL.holz);
  // Baukörper: Süd (y=14.2) und Ost (x=24)
  const Y = 14.2;
  const X = 24;
  const SA = A(Y);
  const SB = B(X);
  o += rect(SA, 0, 0.3, 24, 6.5, "url(#bs)");
  o += rect(SB, 0, 0.3, Y, 6.5, "url(#bo)");
  o += rect(SA, 0, 0.3, 24, 6.5, "#000", 'opacity="0.0"');
  // Sockel
  o += rect(SA, 0, 0, 24, 0.3, "#6B625A");
  o += rect(SB, 0, 0, Y, 0.3, "#5A524B");
  // Deckenbänder
  o += rect(SA, -0.2, 3.7, 24.2, 4.0, COL.beton);
  o += rect(SB, -0.2, 3.7, Y + 0.2, 4.0, COL.beton);
  // Südfassade EG: links Klinker-Teil mit Eingang, Gastro-Glas x 10.6..24
  o += rect(SA, 10.6, 0.3, 24, 3.7, "url(#glow)");
  for (let i = 0; i <= 13; i++) {
    const u = 10.6 + i * (13.4 / 13);
    o += line(SA(u, 0.3), SA(u, 3.7), COL.stahl, 2.5);
  }
  o += line(SA(10.6, 2.9), SA(24, 2.9), COL.stahl, 2.5);
  // Ostfassade EG: Glas der Gastro greift um die Ecke (y 4.7..14.2)
  o += rect(SB, 4.7, 0.3, Y, 3.7, "url(#glow)");
  for (let i = 0; i <= 5; i++) {
    const u = 4.7 + i * (9.5 / 5);
    o += line(SB(u, 0.3), SB(u, 3.7), COL.stahl, 2.5);
  }
  // Eingangstür Wohnen (Süd, x 7.2..9.4)
  o += rect(SA, 7.2, 0.3, 9.4, 3.3, COL.stahl);
  o += rect(SA, 7.4, 0.5, 9.2, 3.2, COL.glas, 'opacity="0.8"');
  // Büro-Fenster
  [[1, 3.3], [3.8, 6.1]].forEach(([a, b]) => (o += rect(SA, a, 1.0, b, 3.3, COL.glas, `stroke="${COL.beton}" stroke-width="3"`)));
  // OG Süd: 3 Bays, Fenster + Loggia
  for (let k = 0; k < 3; k++) {
    const bx = k * 8;
    [[1.0, 2.3], [3.2, 4.5]].forEach(([a, b]) => (o += rect(SA, bx + a, 4.5, bx + b, 6.7 - 0.2, COL.glas, `stroke="${COL.beton}" stroke-width="3"`)));
    o += rect(SA, bx + 5.4, 4.3, bx + 7.7, 6.8 - 0.3, "#3A2B28");
    o += rect(SA, bx + 5.75, 4.6, bx + 7.35, 6.6 - 0.3, COL.glas, 'opacity="0.85"');
    o += rect(SA, bx + 5.4, 4.3, bx + 7.7, 5.2, COL.stahl, 'opacity="0.0"');
    for (let r = 0; r < 12; r++) o += line(SA(bx + 5.5 + r * 0.18, 4.3), SA(bx + 5.5 + r * 0.18, 5.2), COL.stahl, 1.5);
  }
  // OG Ost
  [[1.0, 2.3], [11.6, 12.9]].forEach(([a, b]) => (o += rect(SB, a, 4.5, b, 6.5, COL.glas, `stroke="${COL.beton}" stroke-width="3"`)));
  o += rect(SB, 5.0, 4.3, 7.6, 6.5, "#3A2B28");
  o += rect(SB, 5.3, 4.6, 7.3, 6.4, COL.glas, 'opacity="0.85"');
  // Terrassenstützen
  [10.6, 13.6, 16.6, 19.6, 22.6, 24.6].forEach((u) => {
    const a = P(u, 19, 0);
    const b = P(u, 19, 3.7);
    o += line(a, b, COL.stahl, 4);
  });
  [19, 16.5, 14.2].forEach((y) => {
    const a = P(24.6, y, 0);
    const b = P(24.6, y, 3.7);
    o += line(a, b, COL.stahl, 4);
  });
  // Terrassendach (Auskragung 4,8 m, flaches Vordach)
  o += poly([P(10, 14.2, 3.9), P(24.6, 14.2, 3.9), P(24.6, 19, 3.9), P(10, 19, 3.9)], COL.beton, 'opacity="0.35"');
  // Dachflächen (Satteldach, First parallel zur Südseite bei y=7.1, z=12)
  const eaveZ = 6.5;
  const ridgeZ = 12;
  const yR = Y / 2;
  // Südseite: von (x,Y,eaveZ) bis (x,yR,ridgeZ)
  o += poly([P(-0.5, Y + 0.5, eaveZ - 0.2), P(24.5, Y + 0.5, eaveZ - 0.2), P(24.5, yR, ridgeZ), P(-0.5, yR, ridgeZ)], COL.dach);
  for (let i = 1; i < 14; i++) {
    const t = i / 14;
    const yy = Y + 0.5 + (yR - (Y + 0.5)) * t;
    const zz = eaveZ - 0.2 + (ridgeZ - (eaveZ - 0.2)) * t;
    o += line(P(-0.5, yy, zz), P(24.5, yy, zz), COL.dachHell, 1);
  }
  // Giebel Ost
  o += poly([P(X, 0, eaveZ), P(X, Y, eaveZ), P(X, yR, ridgeZ)], "url(#bo)");
  // Dachüberstand Ost (Ortgang)
  o += line(P(X + 0.3, 0 - 0.3, eaveZ - 0.2), P(X + 0.3, yR, ridgeZ + 0.1), COL.beton, 5);
  o += line(P(X + 0.3, Y + 0.3, eaveZ - 0.2), P(X + 0.3, yR, ridgeZ + 0.1), COL.beton, 5);
  // Gauben auf der Südseite (Penthouses)
  [3.2, 7.2, 14.2, 18.2].forEach((gx) => {
    const yy = Y - 2.2; // 12.0
    const t = (Y + 0.5 - yy) / (Y + 0.5 - yR);
    const zBase = eaveZ - 0.2 + (ridgeZ - (eaveZ - 0.2)) * t;
    const zTop = zBase + 2.3;
    o += poly([P(gx, yy, zBase), P(gx + 2.4, yy, zBase), P(gx + 2.4, yy, zTop), P(gx, yy, zTop)], COL.beton);
    o += poly([P(gx + 0.25, yy, zBase + 0.2), P(gx + 2.15, yy, zBase + 0.2), P(gx + 2.15, yy, zTop - 0.25), P(gx + 0.25, yy, zTop - 0.25)], COL.glas, `stroke="${COL.stahl}" stroke-width="2.5"`);
    o += line(P(gx + 1.2, yy, zBase + 0.2), P(gx + 1.2, yy, zTop - 0.25), COL.stahl, 2.5);
    o += poly([P(gx - 0.2, yy + 0.1, zTop), P(gx + 2.6, yy + 0.1, zTop), P(gx + 2.6, yy - 0.8, zTop + 0.45), P(gx - 0.2, yy - 0.8, zTop + 0.45)], COL.dach);
  });
  // Giebelfenster
  rect(SB, 5.5, 7, 6.5, 9, COL.glas);
  o += rect(SB, 5.4, 7.4, 6.6, 9.2, COL.glas, `stroke="${COL.beton}" stroke-width="3"`);
  o += rect(SB, 7.6, 7.4, 8.8, 9.2, COL.glas, `stroke="${COL.beton}" stroke-width="3"`);
  // Bäume
  const tree = (x, y) => {
    const g = P(x, y, 0);
    return `<rect x="${g[0] - 4}" y="${g[1] - 110}" width="8" height="110" fill="#5A4A3A"/><ellipse cx="${g[0]}" cy="${g[1] - 150}" rx="62" ry="80" fill="#5E8C4B"/><ellipse cx="${g[0] - 14}" cy="${g[1] - 166}" rx="38" ry="48" fill="#76A45F" opacity="0.8"/>`;
  };
  o += tree(-1, 12);
  o += tree(27.5, -0.5);
  // Legende rechts
  const leg = [
    ["Satteldach ca. 38°", "First 12,00 m, Traufe 6,50 m, 4 Gauben für 2 Penthouses"],
    ["1. Obergeschoss", "6 Wohnungen mit Loggien, Klinker rot, Betonbänder"],
    ["Erdgeschoss", "Gastro 190 m² mit Glasfront, Stahlstützen und Terrasse"],
    ["Büro und Eingang", "Büro 70 m², Treppenhaus mit Aufzug, Technik"],
    ["Stellplätze", "ca. 10–13 auf dem Grundstück, Rest über die Parkfläche"],
  ];
  leg.forEach((l, i) => {
    o += `<rect x="1230" y="${150 + i * 120}" width="330" height="100" rx="10" fill="#FFFFFF" opacity="0.85"/>`;
    o += T(1246, 182 + i * 120, l[0], 19, 'font-weight="bold"');
    o += `<foreignObject x="1246" y="${192 + i * 120}" width="300" height="56"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:15px;color:#5B6770;line-height:1.25">${l[1]}</div></foreignObject>`;
  });
  o += T(40, 968, "Skizze, nicht maßstäblich genau. Das Referenzbild der Stadt-Studie hat ein Flachdach, dieser Entwurf hat ein Satteldach. Stand Oktober 2026.", 14);
  o += "</svg>";
  return o;
}

// ---------------------------------------------------------------- Innenkonzept
function innen() {
  const W = 1600;
  const H = 1000;
  let o = head(W, H);
  o += `<rect width="${W}" height="${H}" fill="#FFFFFF"/>`;
  o += T(40, 52, "Gastro innen: Grundriss, Wandansicht und Materialien (Konzeptskizze)", 28, 'font-weight="bold"');
  o += T(40, 80, "Gastro 190 m² (Gastraum ca. 120 m², Küche, WC, Lager), ca. 65 Plätze innen, ca. 30 auf der Terrasse", 16, `fill="${COL.grau}"`);
  // ---- Grundriss links
  const s = 40;
  const ox = 60;
  const oy = 140;
  const rw = 13.4 * s;
  const rh = 14.2 * s;
  const m = (v) => v * s;
  o += T(ox, oy - 14, "Grundriss Erdgeschoss, Gastro", 20, 'font-weight="bold"');
  o += `<rect x="${ox}" y="${oy}" width="${rw}" height="${rh}" fill="#F7F4EF" stroke="${COL.stahl}" stroke-width="6"/>`;
  // Küche NE (oben rechts) + WC + Lager
  o += `<rect x="${ox + m(8.4)}" y="${oy}" width="${m(5)}" height="${m(4.2)}" fill="#D9DEE2" stroke="${COL.stahl}" stroke-width="3"/>` + T(ox + m(9.1), oy + m(2.3), "Küche", 18, 'font-weight="bold"');
  o += `<rect x="${ox + m(5.6)}" y="${oy}" width="${m(2.8)}" height="${m(4.2)}" fill="#E6E2DC" stroke="${COL.stahl}" stroke-width="3"/>` + T(ox + m(5.95), oy + m(1.9), "WC", 18, 'font-weight="bold"') + T(ox + m(5.95), oy + m(2.5), "Lager", 14);
  // Theke links oben
  o += `<rect x="${ox + m(0.5)}" y="${oy + m(0.5)}" width="${m(4.8)}" height="${m(0.8)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="2"/>` + T(ox + m(1.0), oy + m(1.05), "Theke", 15, 'font-weight="bold" fill="#fff"');
  [0.9, 1.9, 2.9, 3.9].forEach((x) => (o += `<circle cx="${ox + m(0.5 + x)}" cy="${oy + m(1.8)}" r="${m(0.22)}" fill="${COL.gruen}"/>`));
  // Tische
  let seats = 0;
  const table4 = (x, y) => {
    o += `<rect x="${ox + m(x)}" y="${oy + m(y)}" width="${m(1.1)}" height="${m(0.9)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="1.5"/>`;
    [[-0.3, 0.05], [-0.3, 0.55], [1.1, 0.05], [1.1, 0.55]].forEach(([dx, dy]) => (o += `<rect x="${ox + m(x + dx)}" y="${oy + m(y + dy)}" width="${m(0.3)}" height="${m(0.3)}" fill="${COL.gruen}" rx="4"/>`));
    seats += 4;
  };
  const table2 = (x, y) => {
    o += `<rect x="${ox + m(x)}" y="${oy + m(y)}" width="${m(0.8)}" height="${m(0.8)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="1.5"/>`;
    [[-0.3, 0.25], [0.8, 0.25]].forEach(([dx, dy]) => (o += `<rect x="${ox + m(x + dx)}" y="${oy + m(y + dy)}" width="${m(0.3)}" height="${m(0.3)}" fill="${COL.gruen}" rx="4"/>`));
    seats += 2;
  };
  // Reihen im Gastraum (y 5 bis 12.5)
  [[1.5, 5.2], [4.1, 5.2], [6.7, 5.2], [9.3, 5.2], [11.4, 5.2]].forEach(([x, y]) => (x < 11 ? table4(x, y) : table2(x, y)));
  [[1.5, 7.4], [4.1, 7.4], [6.7, 7.4], [9.3, 7.4]].forEach(([x, y]) => table4(x, y));
  [[1.5, 9.6], [4.1, 9.6], [6.7, 9.6], [9.3, 9.6]].forEach(([x, y]) => table4(x, y));
  // Banquette an der Westwand
  o += `<rect x="${ox + m(0.05)}" y="${oy + m(5.0)}" width="${m(0.6)}" height="${m(6.6)}" fill="#A5673F" stroke="${COL.stahl}" stroke-width="1.5"/>`;
  // Banquette an der Glasfront
  o += `<rect x="${ox + m(0.9)}" y="${oy + m(12.4)}" width="${m(9)}" height="${m(0.6)}" fill="#A5673F" stroke="${COL.stahl}" stroke-width="1.5"/>`;
  [[1.5, 11.6], [4.7, 11.6], [7.9, 11.6]].forEach(([x, y]) => {
    o += `<rect x="${ox + m(x)}" y="${oy + m(y)}" width="${m(1.1)}" height="${m(0.7)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="1.5"/>`;
    seats += 3;
  });
  // Glasfront unten
  o += `<rect x="${ox}" y="${oy + rh - 8}" width="${rw}" height="10" fill="${COL.glas}"/>`;
  for (let i = 0; i <= 13; i++) o += `<rect x="${ox + (rw / 13) * i - 2}" y="${oy + rh - 10}" width="4" height="14" fill="${COL.stahl}"/>`;
  o += T(ox + m(4.2), oy + rh - 18, "Glasfront nach Süden", 14, 'font-weight="bold" fill="#3A4046"');
  o += `<rect x="${ox + m(10.4)}" y="${oy + rh - 12}" width="${m(1.5)}" height="14" fill="#FFFFFF" stroke="${COL.stahl}" stroke-width="2"/>`;
  o += T(ox + m(10.2), oy + rh - 20, "Eingang", 13, 'font-weight="bold" fill="#3A4046"');
  // Terrasse
  o += `<rect x="${ox - m(0.5)}" y="${oy + rh + 6}" width="${rw + m(1)}" height="${m(3.6)}" fill="#D6B98F" stroke="${COL.stahl}" stroke-width="2" stroke-dasharray="8 6"/>`;
  for (let i = 0; i < 7; i++) {
    const x = ox + m(0.4 + i * 1.9);
    o += `<circle cx="${x + m(0.45)}" cy="${oy + rh + m(1.7)}" r="${m(0.5)}" fill="${COL.holz}" stroke="${COL.stahl}" stroke-width="1.5"/>`;
  }
  o += T(ox + m(0.5), oy + rh + m(3.3), "Terrasse (Holzdeck unter Vordach), ca. 30 Plätze", 15, 'font-weight="bold"');
  o += T(ox, oy + rh + m(4.9), `Plätze innen in der Skizze: ${seats + 8} (inkl. 8 Barhocker). Plan für ca. 65, bleibt Entwurf.`, 14, `fill="${COL.grau}"`);
  // ---- Wandansicht rechts
  const wx = 760;
  const wy = 140;
  const ww = 780;
  const wh = 470;
  o += T(wx, wy - 14, "Wandansicht Bar und Sitznische (Stimmung)", 20, 'font-weight="bold"');
  o += `<defs><radialGradient id="lamp"><stop offset="0" stop-color="#FFE6A8" stop-opacity="0.95"/><stop offset="1" stop-color="#FFE6A8" stop-opacity="0"/></radialGradient></defs>`;
  o += `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="${COL.gruen}"/>`;
  // Lichtvoute
  o += `<rect x="${wx}" y="${wy}" width="${ww}" height="16" fill="#F5D590"/>`;
  // Wandvertäfelung unten
  o += `<rect x="${wx}" y="${wy + 290}" width="${ww}" height="${wh - 290}" fill="#243A31"/>`;
  for (let i = 0; i < 9; i++) o += `<rect x="${wx + 20 + i * 86}" y="${wy + 305}" width="70" height="140" fill="none" stroke="#3B5A4C" stroke-width="3"/>`;
  // Spiegel (Bogenform)
  o += `<path d="M${wx + 60},${wy + 250} v-130 a40,40 0 0 1 80,0 v130 z" fill="#C9D6D6" opacity="0.75" stroke="#B88652" stroke-width="5"/>`;
  // Nische rot mit Flaschen
  o += `<rect x="${wx + 190}" y="${wy + 80}" width="170" height="170" fill="${COL.klinker}" stroke="#B88652" stroke-width="5"/>`;
  [0, 1].forEach((r) => {
    o += `<rect x="${wx + 190}" y="${wy + 80 + 85 * r + 82}" width="170" height="6" fill="#B88652"/>`;
    for (let i = 0; i < 7; i++) o += `<rect x="${wx + 202 + i * 23}" y="${wy + 80 + 85 * r + 38}" width="12" height="44" rx="4" fill="${["#3C6E47", "#C49A45", "#2B2B2B"][i % 3]}"/>`;
  });
  // Pampasgras-Deko
  o += `<g transform="translate(${wx + 470},${wy + 110})"><ellipse cx="0" cy="0" rx="62" ry="78" fill="#F3E3C3"/><ellipse cx="-10" cy="-10" rx="40" ry="56" fill="#FBF3DE"/><rect x="-3" y="60" width="6" height="90" fill="#7A5A38"/></g>`;
  // Stahl-Glas-Trennwand rechts
  o += `<rect x="${wx + 590}" y="${wy + 40}" width="170" height="260" fill="#C7D8DE" opacity="0.55" stroke="${COL.stahl}" stroke-width="6"/>`;
  for (let i = 1; i < 3; i++) o += `<line x1="${wx + 590 + (170 / 3) * i}" y1="${wy + 40}" x2="${wx + 590 + (170 / 3) * i}" y2="${wy + 300}" stroke="${COL.stahl}" stroke-width="4"/>`;
  for (let i = 1; i < 5; i++) o += `<line x1="${wx + 590}" y1="${wy + 40 + (260 / 5) * i}" x2="${wx + 760}" y2="${wy + 40 + (260 / 5) * i}" stroke="${COL.stahl}" stroke-width="4"/>`;
  // Pendelleuchten
  [[120, 120], [400, 90], [690, 100]].forEach(([x, y]) => {
    o += `<circle cx="${wx + x}" cy="${wy + y + 40}" r="70" fill="url(#lamp)"/>`;
    o += `<line x1="${wx + x}" y1="${wy + 16}" x2="${wx + x}" y2="${wy + y + 20}" stroke="#E8C879" stroke-width="2"/>`;
    o += `<ellipse cx="${wx + x}" cy="${wy + y + 32}" rx="16" ry="20" fill="#FFF3D1" stroke="#C49A45" stroke-width="3"/>`;
  });
  // Banquette (Samt) mit Kissen
  o += `<rect x="${wx + 30}" y="${wy + 300}" width="460" height="100" rx="14" fill="#A5673F"/>`;
  for (let i = 0; i < 17; i++) o += `<line x1="${wx + 50 + i * 26}" y1="${wy + 306}" x2="${wx + 50 + i * 26}" y2="${wy + 394}" stroke="#8A5530" stroke-width="3"/>`;
  [90, 210, 330].forEach((x) => (o += `<rect x="${wx + x}" y="${wy + 262}" width="70" height="62" rx="12" fill="#6D2E46"/>`));
  // Tisch mit Laterne
  o += `<rect x="${wx + 120}" y="${wy + 400}" width="300" height="16" fill="${COL.holz}"/><rect x="${wx + 262}" y="${wy + 416}" width="14" height="52" fill="${COL.stahl}"/>`;
  o += `<rect x="${wx + 246}" y="${wy + 362}" width="46" height="38" rx="8" fill="#F5E9D0" stroke="#C49A45" stroke-width="3"/><ellipse cx="${wx + 269}" cy="${wy + 374}" rx="9" ry="12" fill="#FFB84D"/>`;
  // Theke (Bar) rechts unten
  o += `<rect x="${wx + 520}" y="${wy + 340}" width="250" height="40" fill="${COL.holz}"/><rect x="${wx + 520}" y="${wy + 380}" width="250" height="90" fill="#243A31"/>`;
  [560, 640, 720].forEach((x) => (o += `<circle cx="${wx + x}" cy="${wy + 318}" r="20" fill="#2B2B2B"/><rect x="${wx + x - 3}" y="${wy + 338}" width="6" height="${wh - 338 + 0}" fill="${COL.stahl}"/>`));
  // Materialpalette
  const py = 650;
  o += T(wx, py - 20, "Materialpalette", 20, 'font-weight="bold"');
  [["Dunkelgrün", COL.gruen, "Wände"], ["Klinkerrot", COL.klinker, "Nischen, Fassade"], ["Eiche warm", COL.holz, "Theke, Tische"], ["Samt braun", "#A5673F", "Banquetten"], ["Bordeaux", "#6D2E46", "Kissen"], ["Messing", COL.gold, "Leuchten, Rahmen"], ["Stahl schwarz", COL.stahl, "Glaswand"]].forEach(([n, c, u], i) => {
    const x = wx + (i % 4) * 195;
    const y = py + Math.floor(i / 4) * 130;
    o += `<rect x="${x}" y="${y}" width="170" height="70" rx="10" fill="${c}"/>`;
    o += T(x, y + 92, n, 16, 'font-weight="bold"') + T(x, y + 112, u, 14, `fill="${COL.grau}"`);
  });
  o += T(40, 968, "Konzeptskizze nach dem Referenzbild (Innenraum). Möblierung nur zur Orientierung, Planung folgt mit dem Gastro-Fachplaner.", 14);
  o += "</svg>";
  return o;
}

fs.writeFileSync(path.join(OUT, "skizze_aussen_ansichten.svg"), ansichten());
fs.writeFileSync(path.join(OUT, "skizze_aussen_ecke.svg"), perspektive());
fs.writeFileSync(path.join(OUT, "skizze_innen_konzept.svg"), innen());
console.log("SVG geschrieben");
