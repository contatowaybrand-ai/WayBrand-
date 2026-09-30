import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs';
const dir = path.dirname(fileURLToPath(import.meta.url)); fs.mkdirSync(path.join(dir, 'png'), { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1200,height:1450} });
const opts = { a:'instrument-serif', b:'syne', c:'bricolage', d:'unbounded' };
for (const [k, name] of Object.entries(opts)) {
  await p.goto('file://' + path.join(dir, 'index.html') + '#' + k, { waitUntil:'networkidle' }); await p.reload({ waitUntil:'networkidle' });
  await p.waitForSelector('body[data-ready]');
  await (await p.$('#post')).screenshot({ path: path.join(dir, 'png', `portfolio-2026-${k}-${name}.png`) });
}
await b.close();
