# Design de som sincronizado com os cortes do vídeo (gerado do zero, sem música de terceiros).
# Lê a linha do tempo de montar.py, grava out/zohar-som.wav e junta com o vídeo mudo em out/zohar-identidade.mp4.
# Uso: python3 montar.py && python3 som.py
import subprocess, wave
import numpy as np
from montar import cortes, FPS, Q

SR = 48000
rng = np.random.default_rng(7)
quadros = sum(n for _, n in cortes)
N = int(quadros / FPS * SR)
mix = np.zeros((N, 2)); verb = np.zeros((N, 2))  # verb: o que passa pelo reverb
t_all = np.arange(N) / SR

def soma(buf, s, sinal, pan=0.0, ganho=1.0):
    """coloca um som mono em s (amostra) com pan -1..1."""
    e = min(N, s + len(sinal))
    if s >= N: return
    seg = sinal[:e - s] * ganho
    buf[s:e, 0] += seg * np.sqrt((1 - pan) / 2); buf[s:e, 1] += seg * np.sqrt((1 + pan) / 2)

def env(n, ataque, queda):
    t = np.arange(n) / SR
    return np.minimum(t / max(ataque, 1e-4), 1) * np.exp(-t / queda)

def passa_baixa(x, corte):
    """filtro de um polo; corte pode variar no tempo (array)."""
    corte = np.broadcast_to(corte, x.shape)
    a = np.exp(-2 * np.pi * corte / SR); y = np.empty_like(x); v = 0.0
    for i in range(len(x)): v = (1 - a[i]) * x[i] + a[i] * v; y[i] = v
    return y

def grave(dur, f0, f1, queda):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.05)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, queda)

def clique(dur=.012):
    n = int(dur * SR); ruido = np.diff(rng.standard_normal(n + 1))  # agudo
    tom = np.sin(2 * np.pi * 3200 * np.arange(n) / SR)
    return (0.6 * ruido + 0.4 * tom) * env(n, .0005, dur / 4)

# ---- onde cada corte começa
inicio, f = [], 0
for img, n in cortes: inicio.append(f); f += n
amostra = lambda q: int(q / FPS * SR)

# ---- pad: acorde de Ré suave (D3 A3 E4 F#4 C#5), levemente desafinado entre L e R
pad = np.zeros((N, 2))
for fr in (146.83, 220.0, 329.63, 369.99, 554.37):
    for c, det in ((0, -0.6), (1, 0.6)):
        for k in range(1, 5):
            pad[:, c] += np.sin(2 * np.pi * (fr + det) * k * t_all + k) / k ** 1.6
curva = np.minimum(t_all / 1.2, 1) * (0.75 + 0.25 * np.sin(2 * np.pi * t_all / 6))

# ---- cortes
piscas = []
for k, ((img, n), q) in enumerate(zip(cortes, inicio)):
    s = amostra(q)
    if img == Q('fim'):
        fim_s = s; continue
    if n >= 10:      # corte longo: grave macio + clique leve
        soma(mix, s, grave(.5, 110, 46, .28), ganho=.9)
        soma(verb, s, clique(.02), pan=.2 * (-1) ** k, ganho=.25)
    elif n >= 4:     # corte médio: grave curto
        soma(mix, s, grave(.25, 140, 60, .12), ganho=.55)
        soma(mix, s, clique(), pan=.3 * (-1) ** k, ganho=.35)
        soma(verb, s, clique(), ganho=.15)
    else:            # pisca: clique seco
        soma(mix, s, clique(.008), pan=.45 * (-1) ** k, ganho=1.1)
        piscas.append(s)

# ---- subida (ruído que abre + tom que sobe) em cada bloco de pisca
blocos, atual = [], [piscas[0]]
for s in piscas[1:]:
    if s - atual[-1] < amostra(5): atual.append(s)
    else: blocos.append(atual); atual = [s]
blocos.append(atual)
for b in blocos:
    a0, a1 = b[0] - amostra(10), b[-1] + amostra(2)
    n = a1 - a0; x = np.linspace(0, 1, n)
    ruido = passa_baixa(rng.standard_normal(n), 300 + 7000 * x ** 2) * x ** 1.5
    tom = np.sin(2 * np.pi * np.cumsum(220 + 900 * x ** 2) / SR) * x ** 2
    sobe = (ruido * 1.4 + tom * .18); sobe[-int(.01 * SR):] *= np.linspace(1, 0, int(.01 * SR))
    soma(mix, a0, sobe, ganho=.22); soma(verb, a0, sobe, ganho=.06)
    curva[a0:a1] *= 1 - .45 * x  # o pad abaixa enquanto pisca
    curva[a1:a1 + amostra(8)] *= np.linspace(.55, 1, len(curva[a1:a1 + amostra(8)]))

# ---- fecho: whoosh entrando no logo, impacto e brilho da estrela
w0 = fim_s - amostra(16); n = fim_s - w0; x = np.linspace(0, 1, n)
soma(mix, w0, passa_baixa(rng.standard_normal(n), 200 + 5000 * x ** 3) * x ** 2, ganho=.45)
soma(mix, fim_s, grave(2.0, 90, 34, .7), ganho=.85)
choque = passa_baixa(rng.standard_normal(int(1.5 * SR)), 2500) * env(int(1.5 * SR), .001, .35)
soma(verb, fim_s, choque, ganho=.3)
for i, fr in enumerate((1174.66, 1760.0, 2349.32, 2637.02)):  # D6 A6 D7 E7, um atrás do outro
    n = int(2.2 * SR); t = np.arange(n) / SR
    sino = np.sin(2 * np.pi * fr * t + .3 * np.sin(2 * np.pi * 5 * t)) * env(n, .003, .7)
    sino += .3 * np.sin(2 * np.pi * fr * 2.76 * t) * env(n, .001, .2)
    soma(verb, fim_s + amostra(2 + 3 * i), sino, pan=(-.4, .4, -.2, .2)[i], ganho=.22)
curva[fim_s:] *= 1.15  # o pad abre no logo

mix += pad * curva[:, None] * .022

# ---- reverb: cauda de ruído com queda exponencial (convolução por FFT)
ir_n = int(1.6 * SR); ir_t = np.arange(ir_n) / SR
for c in range(2):
    ir = rng.standard_normal(ir_n) * np.exp(-ir_t / .45); ir[0] = 0
    L = 1 << int(np.ceil(np.log2(N + ir_n)))
    molhado = np.fft.irfft(np.fft.rfft(verb[:, c], L) * np.fft.rfft(ir, L), L)[:N]
    mix[:, c] += verb[:, c] + molhado * .06

# ---- master: fade de saída, compressão suave, pico em -1 dB
mix[-int(.6 * SR):] *= np.linspace(1, 0, int(.6 * SR))[:, None] ** 1.5
mix = np.tanh(mix / np.percentile(np.abs(mix), 99.7) * 1.3)  # compressão suave: sobe o volume geral sem estourar o fecho
mix *= 10 ** (-1 / 20) / np.abs(mix).max()
with wave.open('out/zohar-som.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/zohar-identidade-mudo.mp4', '-i', 'out/zohar-som.wav',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                'out/zohar-identidade.mp4'], check=True)
print(f'{len(cortes)} cortes, {len(piscas)} cliques de pisca, {len(blocos)} subidas, {N / SR:.2f} s')
