// Renderiza as 3 opções de capa (1080x1920) e uma visão geral com a guia da grade 3:4. Uso: node render.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 3440, height: 2000 } });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(dir, 'png', '_visao-geral.png') });
await p.evaluate(() => document.body.classList.remove('guia'));
for (const id of ['a', 'b', 'c']) await (await p.$('#' + id)).screenshot({ path: path.join(dir, 'png', `capa-opcao-${id}.png`) });
await b.close();
