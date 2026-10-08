// Renderiza os quadros gráficos (1080x1920) em out/quadros/<id>.png. Uso: node render-quadros.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs';
const dir = path.dirname(fileURLToPath(import.meta.url)); const out = path.join(dir, 'out', 'quadros'); fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 2000 } });
await p.goto('file://' + path.join(dir, 'quadros.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
for (const el of await p.$$('section.q')) await el.screenshot({ path: path.join(out, (await el.getAttribute('id')) + '.png') });
await b.close();
