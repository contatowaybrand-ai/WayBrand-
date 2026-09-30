import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs';
const dir = path.dirname(fileURLToPath(import.meta.url)); fs.mkdirSync(path.join(dir, 'png'), { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1200,height:1450} });
await p.goto('file://' + path.join(dir, 'slides.html'), { waitUntil:'networkidle' }); await p.waitForSelector('body[data-ready]');
const names = ['identidade-visual','conteudo-a-plus','ads-e-escala','store-oficial','brand-registry','suporte','contato'];
for (let i = 0; i < names.length; i++)
  await (await p.$('#s' + (i + 2))).screenshot({ path: path.join(dir, 'png', `slide-0${i + 2}-${names[i]}.png`) });
await b.close();
