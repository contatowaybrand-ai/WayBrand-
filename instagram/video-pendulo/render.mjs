// Renderiza o reel 1080x1920 30fps (28,8 s). Uso: node render.mjs  (--stills: só os quadros de conferência; --som: só troca o áudio)
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url)); const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const stills = process.argv.includes('--stills');
const mudo = path.join(dir, 'out', 'video-sem-som.mp4'), out = path.join(dir, 'out', 'a-way-brand-faz-para-voce.mp4');
// junta o vídeo com som/som.wav (gerado por som/gerar_som.py), volume no padrão do Instagram (-14 LUFS)
const comSom = () => execFileSync(FFMPEG, ['-y', '-i', mudo, '-i', path.join(dir, 'som', 'som.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
  '-af', 'loudnorm=I=-14:TP=-1:LRA=11,alimiter=limit=0.85:level=false', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], { stdio: 'ignore' });
if (process.argv.includes('--som')) {   // reaproveita o vídeo já renderizado, sem refazer os quadros
  execFileSync(FFMPEG, ['-y', '-i', out, '-map', '0:v', '-c', 'copy', mudo], { stdio: 'ignore' }); comSom(); fs.rmSync(mudo); console.log(out); process.exit(0);
}
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
execFileSync(FFMPEG, ['-y', '-framerate', String(fps), '-i', path.join(tmp, 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', mudo], { stdio: 'ignore' });
fs.rmSync(tmp, { recursive: true }); comSom(); fs.rmSync(mudo); console.log(out);
