// SVG -> PNG über Playwright/Chromium
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const dir = __dirname;
(async () => {
  const browser = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter((n) => n.startsWith("skizze_") && n.endsWith(".svg"))) {
    const svg = fs.readFileSync(path.join(dir, f), "utf8");
    const m = svg.match(/width="(\d+)" height="(\d+)"/);
    const page = await browser.newPage({ viewport: { width: +m[1], height: +m[2] }, deviceScaleFactor: 1.5 });
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    await page.screenshot({ path: path.join(dir, f.replace(".svg", ".png")) });
    await page.close();
    console.log("PNG", f);
  }
  await browser.close();
})();
