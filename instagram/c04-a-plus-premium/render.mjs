// Renderiza cada <section class="slide"> do index.html em PNG 1080x1350.
// Uso: node render.mjs   (requer playwright)
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 1 });
await page.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const slides = await page.$$('section.slide');
for (let i = 0; i < slides.length; i++) {
  const out = path.join(dir, 'png', `c04-slide-${String(i + 1).padStart(2, '0')}.png`);
  await slides[i].screenshot({ path: out });
  console.log(out);
}
await browser.close();
