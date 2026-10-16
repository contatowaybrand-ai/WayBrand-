# Gera som/som.wav (28,8 s, 48 kHz, estéreo) sincronizado com o pêndulo do index.html.
# Cópia da trilha da referência, sintetizada do zero:
#   - whoosh grave em cada balanço, quando o fio passa pelo meio (panorâmico acompanha o lado);
#   - clique duplo agudo em cada ponta;
#   - "pop" com subida de tom na ponta direita, a cada 4 idas e voltas.
# Uso: python3 som/gerar_som.py   (depois: node render.mjs --som)
import numpy as np, wave, os
SR, T, N = 48000, 2.4, 12            # mesmo T e quantidade de perguntas do index.html
DUR = T * N
rng = np.random.default_rng(7)
L = int(DUR * SR); out = np.zeros((L, 2))

def banda(x, lo, hi, incl=0.0):
    """Filtro passa-banda por FFT, com inclinação de incl dB/oitava acima de lo."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = ((f >= lo) & (f <= hi)).astype(float)
    g[f > lo] *= (f[f > lo] / lo) ** (incl / 6.02)
    return np.fft.irfft(X * g, len(x))

def suave(n, corte):
    return banda(rng.standard_normal(n), 0.5, corte)

def por(sinal, t0, pan=0.0, ganho=1.0):
    """Mixa o sinal em t0 (s) com loop: o que passa do fim volta no começo."""
    i = int(t0 * SR) % L; n = len(sinal)
    esq, dir_ = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    idx = (np.arange(n) + i) % L
    out[idx, 0] += sinal * ganho * esq * 1.41; out[idx, 1] += sinal * ganho * dir_ * 1.41

def whoosh():
    d = 0.58; n = int(d * SR); t = np.arange(n) / SR
    x = banda(rng.standard_normal(n), 35, 9000, incl=-4.5)      # ruído escuro, grave forte
    flutter = 1 + 0.45 * suave(n, 28) / (np.abs(suave(n, 28)).max() + 1e-9)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.8 * (0.55 + 0.45 * np.sin(np.pi * t / d))
    return x * env * flutter / (np.abs(x).max() + 1e-9)

def clique():
    n = int(0.12 * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for t0, a in ((0.0, 1.0), (0.032, 0.7)):
        m = t >= t0; tt = t[m] - t0
        s[m] += a * banda(rng.standard_normal(m.sum()), 1400, 9000) * np.exp(-tt / 0.012)
        s[m] += 0.5 * a * np.sin(2 * np.pi * 140 * tt) * np.exp(-tt / 0.02)
    return s / np.abs(s).max()

def pop():
    n = int(0.42 * SR); t = np.arange(n) / SR; s = np.zeros(n)
    def tom(f, t0, d, harm=(1, .5, .3)):
        m = (t >= t0) & (t < t0 + d); tt = t[m] - t0
        fase = 2 * np.pi * np.cumsum(f(tt)) / SR
        env = np.minimum(1, tt / 0.004) * np.minimum(1, (d - tt) / 0.008) * np.exp(-tt / (d * 0.6))
        s[m] += env * sum(a * np.sin(k * fase) for k, a in enumerate(harm, 1))
    tom(lambda tt: 600 + 0 * tt, 0.00, 0.05)                    # blip 1
    tom(lambda tt: 300 + 0 * tt, 0.04, 0.07)                    # blip 2
    tom(lambda tt: 300 + 320 * (tt / 0.16) ** 0.8, 0.18, 0.18, (1, .55, .35, .2))  # subida
    return s / np.abs(s).max()

for k in range(N):
    base = k * T
    # ida (esq → dir): meio em T/4, ponta direita em T/2; volta: meio em 3T/4, ponta esquerda em T
    por(whoosh(), base + T / 4 - 0.2, pan=-0.1, ganho=0.9)
    por(whoosh(), base + 3 * T / 4 - 0.2, pan=0.1, ganho=0.9)
    por(clique(), base + T / 2 - 0.02, pan=0.55, ganho=0.35)
    por(clique(), base + T - 0.02, pan=-0.55, ganho=0.35)
    if k % 4 == 0:
        por(pop(), base + T / 2 - 0.18, pan=0.3, ganho=0.55)

out *= 10 ** (-1 / 20) / np.abs(out).max()                      # pico em -1 dBFS
pcm = (out * 32767).astype('<i2')
cam = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'som.wav')
with wave.open(cam, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(cam)
