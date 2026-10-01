// Gera o post animado (versão B, Syne): MP4 1080x1350 30fps com 2 voltas do loop e um GIF de 1 volta.
// Uso: FFMPEG=/caminho/ffmpeg node render-video.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url)); const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const fps = 30, loop = 4, tmp = fs.mkdtempSync(path.join(dir, '.frames-'));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 1450 } });
await p.addInitScript(() => { window.__render = true; });
await p.goto('file://' + path.join(dir, 'index.html') + '#b', { waitUntil: 'networkidle' }); await p.waitForSelector('body[data-ready]');
const el = await p.$('#post');
for (let f = 0; f < fps * loop; f++) { await p.evaluate(t => setT(t), f / fps); await el.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.png`) }); }
await b.close();
const mp4 = path.join(dir, 'png', 'portfolio-2026-animado.mp4'), gif = path.join(dir, 'png', 'portfolio-2026-animado.gif');
execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-stream_loop', '1', '-framerate', String(fps), '-i', path.join(tmp, 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-movflags', '+faststart', mp4]);
execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', path.join(tmp, 'f%04d.png'),
  '-vf', 'fps=20,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4', '-loop', '0', gif]);
fs.rmSync(tmp, { recursive: true }); console.log(mp4, gif);
