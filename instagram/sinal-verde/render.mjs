import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1200,height:1450} });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil:'networkidle' }); await p.evaluate(() => document.fonts.ready);
await (await p.$('#post')).screenshot({ path: path.join(dir, 'png', 'sinal-verde.png') }); await b.close();
