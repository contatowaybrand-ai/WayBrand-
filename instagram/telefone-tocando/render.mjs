// Renderiza o loop de 4 s: MP4 1080x1350 30fps (para postar) + GIF 720x900 (prévia).
// Uso: node render.mjs [a|b|c|d|d:claro ...]   (sem argumento renderiza a, b e c; ':claro' = fundo branco)
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import fs from 'fs'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url)); const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const fps = 30, dur = 4, vs = process.argv.slice(2).length ? process.argv.slice(2) : ['a', 'b', 'c'];
const b = await chromium.launch();
for (const arg of vs) {
  const [v, tema] = arg.split(':');
  const tmp = fs.mkdtempSync(path.join(dir, '.frames-'));
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.addInitScript(() => { window.__render = true; });
  await p.goto('file://' + path.join(dir, 'index.html') + '?v=' + v + (tema ? '&tema=' + tema : ''), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const el = await p.$('#v');
  for (let f = 0; f < fps * dur; f++) { await p.evaluate(t => setT(t), f / fps); await el.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.png`) }); }
  await p.close();
  const base = path.join(dir, 'out', `telefone-tocando-${v}${tema ? '-' + tema : ''}`), seq = path.join(tmp, 'f%04d.png');
  execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-stream_loop', '2', '-framerate', String(fps), '-i', seq, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', base + '.mp4']);
  execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', seq, '-vf', 'fps=20,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a', '-loop', '0', base + '.gif']);
  fs.copyFileSync(path.join(tmp, 'f0015.png'), base + '-quadro.png');
  fs.rmSync(tmp, { recursive: true }); console.log(base);
}
await b.close();
