// Exportiert A3-SVG-Blätter als PDF (Vektor, eingebettete Schrift) und PNG (300 dpi). Aufruf: NODE_PATH=... node export.js datei.svg ...
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  for (const f of process.argv.slice(2)) {
    const p = path.resolve(f);
    const pg = await b.newPage({ viewport: { width: 1588, height: 1123 }, deviceScaleFactor: 3.125 });
    await pg.goto('file://' + p);
    await pg.evaluate(() => document.fonts.ready);
    await pg.screenshot({ path: p.replace(/\.svg$/, '.png'), clip: { x: 0, y: 0, width: 1587.4, height: 1122.5 } });
    await pg.pdf({ path: p.replace(/\.svg$/, '.pdf'), width: '420mm', height: '297mm', printBackground: true, pageRanges: '1' });
    await pg.close();
  }
  await b.close();
})();
