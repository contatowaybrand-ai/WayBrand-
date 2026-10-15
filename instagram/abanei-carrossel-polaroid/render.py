# Reel 1080x1920 30fps, recriando o vídeo de referência:
# - cada imagem de assets/ vira fundo em tela cheia por 40 quadros (corte seco) com zoom out leve;
# - as miniaturas ficam numa circunferência (roda com centro abaixo da tela) que gira uma posição
#   por imagem com speed ramp: rápida no corte, quase parada com a imagem atual no centro.
# Uso: python3 render.py   (imagens em assets/, ordenadas pelo nome; saída em out/)
import glob, math, os, subprocess, sys
from PIL import Image

DIR = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
HOLD = 40                 # quadros por imagem (~1,33 s, medido na referência)
LOOPS = 2
ZOOM_IN = 1.045           # escala do fundo no corte; termina em 1.0
CARD_W, CARD_H = 199, 249 # miniaturas 4:5, sem borda
CARD_Y = 933              # centro da miniatura do meio
RADIUS = 880              # raio da roda (centro em CARD_Y + RADIUS)
STEP = math.radians(20.6) # ângulo entre miniaturas vizinhas
MID_SPEED = 0.34          # velocidade no meio (posições por imagem) -> speed ramp
RAMP_POW = 5              # quanto mais alto, mais o movimento se concentra perto do corte
SLOTS = range(-4, 5)

paths = sorted(p for p in glob.glob(os.path.join(DIR, 'assets', '*')) if p.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')))
if not paths:
    sys.exit('sem imagens em assets/')
src = [Image.open(p).convert('RGB') for p in paths]
n = len(src)

def cover(im, w, h, bias=0.5):
    s = max(w / im.width, h / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = round((r.height - h) * bias)
    return r.crop((x, y, x + w, y + h))

# fundo guardado já na escala máxima, para o zoom out só reduzir (sem perder nitidez)
BW, BH = round(W * ZOOM_IN), round(H * ZOOM_IN)
bgs = [cover(im, BW, BH) for im in src]
# miniatura 2x maior e reduzida na rotação, para bordas suaves
thumbs = [cover(im, CARD_W * 2, CARD_H * 2, 0.3).convert('RGBA') for im in src]

def ramp(u):
    """posição da roda dentro de uma imagem, de -0.5 a +0.5: rápida nas pontas, lenta no meio."""
    s = u - 0.5
    return MID_SPEED * s + (0.5 - MID_SPEED / 2) * (2 * s) ** RAMP_POW  # RAMP_POW ímpar

def bg_frame(i, u):
    z = 1 + (ZOOM_IN - 1) * (1 - u) ** 1.2
    w, h = W * ZOOM_IN / z, H * ZOOM_IN / z   # janela recortada do fundo guardado
    x, y = (BW - w) / 2, (BH - h) / 2
    return bgs[i].resize((W, H), Image.BICUBIC, box=(x, y, x + w, y + h)).convert('RGBA')

out = os.path.join(DIR, 'out', 'abanei-carrossel-polaroid.mp4')
os.makedirs(os.path.dirname(out), exist_ok=True)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17',
                       '-movflags', '+faststart', out], stdin=subprocess.PIPE)
cx0, cy0 = W / 2, CARD_Y + RADIUS
for f in range(n * HOLD * LOOPS):
    seg, k = divmod(f, HOLD)
    cur = seg % n
    u = (k + 0.5) / HOLD
    fr = bg_frame(cur, u)
    p = ramp(u)  # a roda gira no sentido horário: a próxima imagem entra pela esquerda
    for s in sorted(SLOTS, key=abs, reverse=True):
        a = (s + p) * STEP
        x, y = cx0 + RADIUS * math.sin(a), cy0 - RADIUS * math.cos(a)
        if not -CARD_H < x < W + CARD_H:
            continue
        t = thumbs[(cur - s) % n].rotate(-math.degrees(a), resample=Image.BICUBIC, expand=True)
        t = t.resize((t.width // 2, t.height // 2), Image.LANCZOS)
        fr.alpha_composite(t, (round(x - t.width / 2), round(y - t.height / 2)))
    ff.stdin.write(fr.convert('RGB').tobytes())
ff.stdin.close()
ff.wait()

# "tique" sintetizado em cada corte: estalo agudo curto + um toque grave leve
import numpy as np, wave
SR = 48000
tt = np.arange(int(SR * 0.06)) / SR
rng = np.random.default_rng(7)
click = rng.standard_normal(tt.size) * np.exp(-tt / 0.0025)
click = np.convolve(click, [1, -1], 'same')                     # tira o grave do ruído: estalo mais seco
tone = np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt / 0.012)      # corpo do "tic"
knock = np.sin(2 * np.pi * 180 * tt) * np.exp(-tt / 0.008)      # peso
tick = 0.35 * click / np.abs(click).max() + 0.5 * tone + 0.3 * knock
tick *= 0.7 / np.abs(tick).max()
total = n * HOLD * LOOPS / FPS
audio = np.zeros(int(SR * total) + tick.size)
for seg in range(n * LOOPS):
    i = round(seg * HOLD / FPS * SR)
    audio[i:i + tick.size] += tick
audio = audio[:int(SR * total)]
wav = os.path.join(DIR, 'out', '.tiques.wav')
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())
muted = out + '.mudo.mp4'
os.replace(out, muted)
# trilha ambiente opcional (assets/trilha-ambiente.*): fica por baixo dos tiques, com fade no fim
bed = sorted(glob.glob(os.path.join(DIR, 'assets', 'trilha-ambiente.*')))
inputs = ['-i', muted, '-i', wav]
if bed:
    inputs += ['-i', bed[0]]
    # trilha comprimida à parte (mais corpo sem picos) e tique ~6 dB acima dela em cada corte; total ~-18 LUFS
    mix = (f'[2:a]atrim=0:{total},asetpts=N/SR/TB,volume=7dB,alimiter=limit=0.3:attack=5:release=120:level=false,'
           f'afade=t=in:d=0.4,afade=t=out:st={total - 1.5}:d=1.5[b];'
           '[1:a]aformat=channel_layouts=stereo,volume=2.0[t];'
           '[b][t]amix=inputs=2:normalize=0,alimiter=limit=0.8:attack=1:release=60:level=false[a]')
    amap = ['-filter_complex', mix, '-map', '0:v', '-map', '[a]']
else:
    amap = ['-map', '0:v', '-map', '1:a']
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, *amap, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-ac', '2', '-ar', '48000', '-t', str(total), '-movflags', '+faststart', out], check=True)
os.remove(muted); os.remove(wav)
for t, name in [(0.65, 'a'), (2.0, 'b'), (5.0, 'c')]:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', out, '-frames:v', '1',
                    os.path.join(DIR, 'out', f'quadro-{name}.png')])
print(out)
