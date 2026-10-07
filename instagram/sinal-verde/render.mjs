// Gera o carrossel (png/slide-01..04.png) e a capa piscando (png/sinal-verde-pisca.gif + .mp4). Uso: node render.mjs
import { chromium } from 'playwright'; import { fileURLToPath } from 'url'; import path from 'path'; import { execFileSync } from 'child_process';
const dir = path.dirname(fileURLToPath(import.meta.url)); const out = f => path.join(dir, 'png', f); const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1200,height:1450} });
await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil:'networkidle' }); await p.evaluate(() => document.fonts.ready);
for (const n of [1, 2, 3, 4]) await (await p.$('#s' + n)).screenshot({ path: out(`slide-0${n}.png`) });
await p.evaluate(() => document.body.classList.add('apagado')); await (await p.$('#s1')).screenshot({ path: out('slide-01-apagado.png') }); await b.close();
// pisca como na rua: meio segundo aceso, meio segundo apagado, em loop
const on = out('slide-01.png'), off = out('slide-01-apagado.png');
const ff = (...a) => execFileSync(FFMPEG, ['-y', '-loglevel', 'error', ...a]);
const seq = ['-loop', '1', '-t', '0.5', '-i', on, '-loop', '1', '-t', '0.5', '-i', off];
const cat = '[0][1]concat=n=2:v=1,fps=10';
ff(...seq, '-filter_complex', `${cat},split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a`, '-loop', '0', out('sinal-verde-pisca.gif'));
ff(...seq, '-filter_complex', `${cat},loop=5:10:0`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-r', '30', '-t', '6', '-movflags', '+faststart', out('sinal-verde-pisca.mp4'));
