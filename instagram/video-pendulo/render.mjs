// Renderiza o reel 1080x1920 30fps (28,8 s). Uso: node render.mjs  (ou: node render.mjs --stills para só os quadros de conferência)
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url)); const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const stills = process.argv.includes('--stills');
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.addInitScript(() => { window.__render = true; });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
const el = await p.$('#v'); const dur = await p.evaluate(() => DUR); const fps = 30;
if (stills) {
  for (const [t, n] of [[0, 'a'], [0.6, 'b'], [1.2, 'c'], [1.8, 'd'], [3.6, 'e'], [13.2, 'f']]) { await p.evaluate(t => setT(t), t); await el.screenshot({ path: path.join(dir, 'out', `quadro-${n}.png`) }); }
  await b.close(); process.exit(0);
}
const tmp = fs.mkdtempSync(path.join(dir, '.frames-'));
const n = Math.round(fps * dur);
for (let f = 0; f < n; f++) { await p.evaluate(t => setT(t), f / fps); await el.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.png`) }); }
await b.close();
const out = path.join(dir, 'out', 'precisa-de-deixa-com-a-gente.mp4');
execFileSync(FFMPEG, ['-y', '-framerate', String(fps), '-i', path.join(tmp, 'f%04d.png'), '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-c:a', 'aac', '-movflags', '+faststart', out], { stdio: 'ignore' });
fs.rmSync(tmp, { recursive: true }); console.log(out);
