# Monta out/zohar-identidade.mp4 (1080x1920, 30 fps, sem áudio) no ritmo do vídeo de referência:
# cortes calmos -> acelera até piscar -> desacelera, duas vezes, e fecha no logo.
# Cada imagem tem movimento (entra com zoom e assenta devagar); cortes longos ganham uma fusão curta.
# Uso: node render-quadros.mjs && python3 montar.py
import subprocess
from PIL import Image

FPS, W, H = 30, 1080, 1920
Q = lambda n: f'out/quadros/{n}.png'
F = lambda n: f'assets/fotos/{n}.jpg'

ABERTURA = [(Q('tipo-bodoni'), 14), (Q('icones'), 14), (F('bone'), 16), (F('pasta'), 18), (Q('logo-luz'), 20)]
# rodízio do miolo: fotos e quadros intercalados; o logo na luz fica de fora pra não repetir
RODIZIO = [F('capinha'), Q('monograma'), F('vinil'), F('chaveiro'), Q('o-estrela'), F('ecobag'), Q('tipo-inter'),
           F('skate'), Q('estrela-nome'), F('bone'), Q('icones'), F('pasta'), Q('tipo-bodoni')]
# duração (em quadros) de cada corte: acelera, pisca, desacelera, acelera de novo, desacelera
RITMO = ([6, 5, 4, 4, 3, 3] + [2] * 14 + [3, 3, 4, 4, 5, 6, 7, 9, 11, 14, 17] +
         [5, 4, 3, 3] + [2] * 14 + [3, 4, 5, 6, 8, 10, 13, 16])
FECHO = [(Q('logo-luz'), 16), (Q('fim'), 45)]

cortes = list(ABERTURA)
for i, q in enumerate(RITMO):
    img = RODIZIO[i % len(RODIZIO)]
    if img == cortes[-1][0]: img = RODIZIO[(i + 1) % len(RODIZIO)]
    cortes.append((img, q))
cortes += FECHO
assert all(a[0] != b[0] for a, b in zip(cortes, cortes[1:])), 'imagem repetida em sequência'

cache = {}
def carregar(p):
    if p not in cache: cache[p] = Image.open(p).convert('RGB').resize((W, H))
    return cache[p]

def ease(x): return 1 - (1 - min(max(x, 0), 1)) ** 3

def quadro(p, f, n):
    """imagem p no quadro f de um corte de n quadros: entra com zoom e assenta, depois aproxima devagar."""
    foto = p.endswith('.jpg')
    deriva = (0.05 if foto else 0.02) * f / max(n, 1)
    entrada = (0.07 if foto else 0.03) * (1 - ease(f / 7)) if n >= 6 else 0
    s = 1 + deriva + entrada + (0.02 if foto and n < 6 else 0)
    im = carregar(p); w, h = round(W * s), round(H * s)
    big = im.resize((w, h), Image.BILINEAR)
    x, y = (w - W) // 2, (h - H) // 2
    return big.crop((x, y, x + W, y + H))

ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow',
                       '-pix_fmt', 'yuv420p', '-movflags', '+faststart', 'out/zohar-identidade.mp4'], stdin=subprocess.PIPE)
FUSAO = 4  # quadros de fusão nos cortes de 10 quadros ou mais
total = 0
for k, (p, n) in enumerate(cortes):
    for f in range(n):
        im = quadro(p, f, n)
        if k and n >= 10 and f < FUSAO:  # fusão: a imagem anterior continua o movimento e some
            pp, pn = cortes[k - 1]
            im = Image.blend(quadro(pp, pn + f, pn), im, (f + 1) / (FUSAO + 1))
        ff.stdin.write(im.tobytes()); total += 1
ff.stdin.close(); ff.wait()
print(len(cortes), 'cortes,', round(total / FPS, 2), 's')
