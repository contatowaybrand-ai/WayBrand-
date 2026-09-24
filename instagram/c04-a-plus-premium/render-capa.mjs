import { chromium } from 'playwright';
import { fileURLToPath } from 'url'; import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1080,height:1350} });
await p.goto('file://' + path.join(dir, 'capa-texto.html'), { waitUntil:'networkidle' });
await p.evaluate(() => document.fonts.ready);
await (await p.$('#capa')).screenshot({ path: path.join(dir,'png','capa-camada-texto.png'), omitBackground:true });
await b.close();
