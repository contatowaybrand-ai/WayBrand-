// Renderiza o loop de 4 s: MP4 1080x1350 30fps (para postar, loop 3x) + GIF 720x900 + um quadro PNG.
// Uso: node render.mjs   (precisa do Playwright e do ffmpeg)
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url)); const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const AUDIO = path.join(dir, '..', 'som-telefone', 'toque-12s.wav');   // toque de telefone (gerado por som-telefone/gerar.py)
const fps = 30, dur = 4, tmp = fs.mkdtempSync(path.join(dir, '.frames-'));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
await p.addInitScript(() => { window.__render = true; });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
const el = await p.$('#v');
for (let f = 0; f < fps * dur; f++) { await p.evaluate(t => setT(t), f / fps); await el.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.png`) }); }
await b.close();
const base = path.join(dir, 'out', 'telefone-tocando-2'), seq = path.join(tmp, 'f%04d.png');
execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-stream_loop', '2', '-framerate', String(fps), '-i', seq, '-i', AUDIO, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', base + '.mp4']);
execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', seq, '-vf', 'fps=20,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a', '-loop', '0', base + '.gif']);
fs.copyFileSync(path.join(tmp, 'f0015.png'), base + '-quadro.png');
fs.rmSync(tmp, { recursive: true }); console.log(base);
