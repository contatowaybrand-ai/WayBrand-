// Gera o slide 3 em MP4 (1080x1350, 30 fps) com o A+ Premium rolando dentro do painel.
// Uso: node render-slide3-video.mjs   (usa assets/jbl-aplus.png; sem ele, usa o placeholder)
import { chromium } from 'playwright';
import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url));
const FFMPEG = process.env.FFMPEG || '/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux';
const fps = 30, hold1 = 1.0, scroll = 7.0, hold2 = 1.2;
const total = Math.round((hold1 + scroll + hold2) * fps);
const tmp = fs.mkdtempSync(path.join(dir, '.frames-'));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 1400 } });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.waitForFunction(() => { const i = document.getElementById('aplus'); return i.complete && i.naturalWidth > 0; });
await p.evaluate(() => { const w = document.querySelector('#s3 .scrollwin'), i = document.getElementById('aplus');
  w.style.setProperty('--winh', w.clientHeight + 'px'); w.style.setProperty('--imgh', i.clientHeight + 'px'); });
const el = await p.$('#s3');
const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
for (let f = 0; f < total; f++) {
  const t = f / fps; const prog = t <= hold1 ? 0 : t >= hold1 + scroll ? 1 : ease((t - hold1) / scroll);
  await p.evaluate(v => document.querySelector('#s3 .scrollwin').style.setProperty('--p', v), prog);
  await el.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.png`) });
}
await b.close();
const out = path.join(dir, 'png', 'c04-slide-03.mp4');
execFileSync(FFMPEG, ['-y', '-framerate', String(fps), '-i', path.join(tmp, 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out], { stdio: 'ignore' });
fs.rmSync(tmp, { recursive: true });
console.log(out);
