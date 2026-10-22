// Aufruf: NODE_PATH=... node svg_to_png.js datei.svg ...
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  for (const f of process.argv.slice(2)) {
    const pg = await b.newPage();
    await pg.goto('file://' + path.resolve(f));
    await (await pg.$('svg')).screenshot({ path: f.replace(/\.svg$/, '.png') });
    await pg.close();
  }
  await b.close();
})();
