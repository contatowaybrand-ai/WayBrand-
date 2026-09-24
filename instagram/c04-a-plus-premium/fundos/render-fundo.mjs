import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path';
const dir = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1080,height:1350} });
await p.goto('file://' + path.join(dir, process.argv[2] + '.html')); await p.screenshot({ path: path.join(dir, '..', 'assets', process.argv[2] + '.png') }); await b.close();
