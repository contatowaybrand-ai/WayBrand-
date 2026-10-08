// Renderiza a tela da Store (1600x1200) em assets/tela.png, para encaixar no tablet. Uso: node render-tela.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1700, height: 1300 } });
await p.goto('file://' + path.join(dir, 'tela.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
await (await p.$('#tela')).screenshot({ path: path.join(dir, 'assets', 'tela.png') }); await b.close();
