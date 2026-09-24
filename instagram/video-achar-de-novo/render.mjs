// Renderiza o loop de 5 s em MP4 1080x1350 30fps. Uso: FFMPEG=/caminho/ffmpeg node render.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url)); const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const fps = 30, dur = 5, tmp = fs.mkdtempSync(path.join(dir, '.frames-'));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
await p.addInitScript(() => { window.__render = true; });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
const el = await p.$('#v');
for (let f = 0; f < fps * dur; f++) { await p.evaluate(t => setT(t), f / fps); await el.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.png`) }); }
await b.close();
const out = path.join(dir, 'out', 'como-o-cliente-vai-te-achar-de-novo.mp4');
execFileSync(FFMPEG, ['-y', '-framerate', String(fps), '-i', path.join(tmp, 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', out], { stdio: 'ignore' });
for (const [t, n] of [[1.5, 'a'], [3.9, 'b']]) execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-ss', String(t), '-i', out, '-frames:v', '1', path.join(dir, 'out', `quadro-${n}.png`)]);
fs.rmSync(tmp, { recursive: true }); console.log(out);
