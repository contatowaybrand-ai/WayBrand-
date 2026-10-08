# Monta out/zohar-identidade.mp4 (1080x1920, 30 fps, sem áudio) com o ritmo de cortes do vídeo de referência:
# cortes calmos -> pisca-pisca -> desacelera, duas vezes, e termina parado no logo.
# Uso: node render-quadros.mjs && python3 montar.py
import subprocess, os, shutil
from PIL import Image
FPS = 30
# instantes dos cortes medidos na referência (segundos); o último trecho vira o fecho
CORTES = [0.4, .933, 1.5, 2.3, 2.467, 2.533, 2.6, 2.667, 2.7, 2.833, 2.9, 2.967, 3.033, 3.1, 3.167, 3.233, 3.3, 3.367,
  3.433, 3.5, 3.567, 3.633, 3.7, 3.767, 3.833, 3.9, 4.033, 4.1, 4.167, 4.233, 4.333, 4.4, 4.467, 4.633, 4.7, 4.767, 4.867,
  5.033, 5.233, 5.367, 5.5, 5.7, 5.833, 6.033, 6.233, 6.433, 6.667, 6.867, 7.2, 7.533, 7.9, 8.467, 8.967, 9.6, 10.3,
  10.567, 10.667, 10.733, 10.8, 10.867, 11, 11.067, 11.133, 11.2, 11.267, 11.333, 11.4, 11.467, 11.533, 11.6, 11.667,
  11.733, 11.8, 11.867, 11.967, 12.1, 12.167, 12.233, 12.3, 12.367, 12.5, 12.567, 12.7, 12.767, 12.833, 12.967, 13.033,
  13.267, 13.367, 13.567, 13.7, 13.867, 14.067, 14.267, 14.533, 14.733, 14.933, 15.233]
FECHO = 1.8  # segundos parado no logo no final

Q = lambda n: f'out/quadros/{n}.png'
F = lambda n: f'assets/fotos/{n}.jpg'
# sequência dos trechos "normais" (os de 1 a 3 quadros viram pisca entre uma foto e o logo na luz)
NORMAIS = [Q('tipo-bodoni'), Q('icones'), F('bone'), F('pasta'),
           F('capinha'), Q('monograma'), F('vinil'), F('chaveiro'), Q('o-estrela'), F('ecobag'), Q('tipo-inter'),
           F('skate'), Q('estrela-nome'), F('pasta'), F('bone'), Q('logo-luz'),
           Q('tipo-bodoni'), Q('icones'), F('vinil'),
           F('skate'), Q('o-estrela'), F('capinha'), Q('monograma'), F('chaveiro'), F('ecobag'), Q('estrela-nome'),
           Q('tipo-inter'), F('bone'), F('pasta'), Q('logo-luz')]
PISCA = [(F('pasta'), Q('logo-luz')), (F('skate'), Q('logo-luz'))]

marcas = [0] + [round(t * FPS) for t in CORTES]
trechos = [b - a for a, b in zip(marcas, marcas[1:]) if b > a]
lista, n, ciclo, i = [], 0, -1, 0
while i < len(trechos):
    if trechos[i] <= 3:  # bloco de pisca: alterna entre os dois
        ciclo += 1; a, b = PISCA[min(ciclo, len(PISCA) - 1)]; k = 0
        while i < len(trechos) and trechos[i] <= 3:
            lista.append((a if k % 2 == 0 else b, trechos[i])); k += 1; i += 1
    else:
        lista.append((NORMAIS[n % len(NORMAIS)], trechos[i])); n += 1; i += 1
lista.append((Q('fim'), round(FECHO * FPS)))

# o concat do ffmpeg exige um formato só: as fotos viram PNG numa pasta temporária
tmp = 'out/.tmp'; os.makedirs(tmp, exist_ok=True)
def png(img):
    if img.endswith('.png'): return '../../' + img
    dst = os.path.join(tmp, os.path.basename(img)[:-4] + '.png')
    if not os.path.exists(dst): Image.open(img).convert('RGB').save(dst)
    return os.path.basename(dst)
with open(f'{tmp}/lista.txt', 'w') as f:
    for img, q in lista: f.write(f"file '{png(img)}'\nduration {q / FPS:.6f}\n")
    f.write(f"file '{png(lista[-1][0])}'\n")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/lista.txt',
  '-vf', f'scale=1080:1920,setsar=1,fps={FPS},format=yuv420p', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow',
  '-movflags', '+faststart', '-an', 'out/zohar-identidade.mp4'], check=True)
shutil.rmtree(tmp)
print(len(lista), 'cortes,', sum(q for _, q in lista) / FPS, 's')
