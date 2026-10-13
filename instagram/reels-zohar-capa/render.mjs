// Renderiza as opções de capa (1080x1920) e visões gerais com a guia da grade 3:4. Uso: node render.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const ids = ['a', 'b', 'c', 'd', 'e', 'f'];
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 3440, height: 2000 } });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
const mostrar = grupo => p.evaluate(g => document.querySelectorAll('.capa').forEach(c => c.style.display = g.includes(c.id) ? '' : 'none'), grupo);
for (const [nome, grupo] of [['_visao-geral', ['a', 'b', 'c']], ['_visao-geral-2', ['d', 'e', 'f']]]) { await mostrar(grupo); await p.screenshot({ path: path.join(dir, 'png', nome + '.png') }); }
await mostrar(ids); await p.evaluate(() => document.body.classList.remove('guia'));
for (const id of ids) await (await p.$('#' + id)).screenshot({ path: path.join(dir, 'png', `capa-opcao-${id}.png`) });
await b.close();
