# Reel 1080x1920 30fps: cada imagem de assets/ vira fundo em tela cheia por 40 quadros (corte seco),
# enquanto uma faixa de "polaroids" desliza no meio com a imagem atual no centro. Roda as imagens 2x.
# Uso: python3 render.py   (imagens em assets/, ordenadas pelo nome; saída em out/)
import glob, os, subprocess, sys
from PIL import Image, ImageFilter

DIR = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
HOLD = 40          # quadros por imagem (~1,33 s, igual à referência)
LOOPS = 2
CARD_W, CARD_H, BORDER = 200, 268, 11
GAP = 330          # distância entre centros das polaroids
STRIP_Y = 935      # centro vertical da faixa
DRIFT = 80         # deslocamento (px) da faixa durante cada imagem
SLOT_ROT = {-3: 9, -2: -13, -1: 11, 0: -2, 1: -12, 2: 10, 3: -9}  # graus por posição na faixa
SHADOW = 18

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

bgs = [cover(im, W, H) for im in src]

def card(im, rot):
    c = Image.new('RGBA', (CARD_W, CARD_H), (247, 245, 240, 255))
    c.paste(cover(im, CARD_W - 2 * BORDER, CARD_H - 2 * BORDER, 0.45), (BORDER, BORDER))
    pad = SHADOW * 2
    sh = Image.new('RGBA', (CARD_W + 2 * pad, CARD_H + 2 * pad), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 70), (pad, pad + 6, pad + CARD_W, pad + CARD_H + 6))
    sh = sh.filter(ImageFilter.GaussianBlur(SHADOW / 2))
    sh.alpha_composite(c, (pad, pad))
    return sh.rotate(rot, resample=Image.BICUBIC, expand=True)

cards = {(i, s): card(src[i], r) for i in range(n) for s, r in SLOT_ROT.items()}

out = os.path.join(DIR, 'out', 'abanei-carrossel-polaroid.mp4')
os.makedirs(os.path.dirname(out), exist_ok=True)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17',
                       '-movflags', '+faststart', out], stdin=subprocess.PIPE)
for f in range(n * HOLD * LOOPS):
    cur, k = divmod(f, HOLD)
    cur %= n
    drift = -DRIFT / 2 + DRIFT * k / (HOLD - 1)
    fr = bgs[cur].copy().convert('RGBA')
    # a próxima imagem entra pela esquerda e a faixa anda para a direita, como na referência
    for s in sorted(SLOT_ROT, key=abs, reverse=True):
        im = cards[((cur - s) % n, s)]
        cx = W / 2 + s * GAP + drift
        fr.alpha_composite(im, (round(cx - im.width / 2), round(STRIP_Y - im.height / 2)))
    ff.stdin.write(fr.convert('RGB').tobytes())
ff.stdin.close()
ff.wait()
for t, name in [(0.6, 'a'), (2.0, 'b'), (5.0, 'c')]:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', out, '-frames:v', '1',
                    os.path.join(DIR, 'out', f'quadro-{name}.png')])
print(out)
