// Gera os PNGs do post (1080x1350). Uso: node render.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1200,height:1450} });
for (const [html, png] of [['index.html', 'store-amazon.png'], ['ceu.html', 'store-amazon-ceu.png'], ['sacola.html', 'store-amazon-sacola.png']]) {
  await p.goto('file://' + path.join(dir, html), { waitUntil:'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await (await p.$('#post')).screenshot({ path: path.join(dir, 'png', png) });
}
await b.close();
