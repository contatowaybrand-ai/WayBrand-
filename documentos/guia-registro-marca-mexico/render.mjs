// Gera o PDF (A4) e uma prévia PNG de cada página do index.html.
// Uso: node render.mjs   (requer playwright)
import { createRequire } from 'module';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import path from 'path';
// usa o playwright local se existir; senão, o instalado globalmente
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'))); }
const dir = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2 });
await page.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

const pages = await page.$$('section.page');
for (let i = 0; i < pages.length; i++) {
  const out = path.join(dir, 'png', `pagina-${String(i + 1).padStart(2, '0')}.png`);
  await pages[i].screenshot({ path: out });
  console.log(out);
}

await page.emulateMedia({ media: 'print' });
const pdf = path.join(dir, 'Guia-Registro-de-Marca-Mexico-IMPI-WayBrand.pdf');
await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
console.log(pdf);
await browser.close();
