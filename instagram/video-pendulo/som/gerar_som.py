# Gera som/som.wav (28,8 s, 48 kHz, estéreo) sincronizado com o pêndulo do index.html.
# "Relógio de pêndulo musical", calmo e em loop:
#   - tique-taque de madeira em cada ponta (tique na direita, taque na esquerda);
#   - nota de marimba em cada ponta, formando uma melodia sobre os acordes;
#   - acorde suave de fundo + grave, trocando a cada 3 idas e voltas (C, Am, F, G);
#   - whoosh bem baixo quando o fio passa pelo meio;
#   - reverb circular: a cauda do fim cai no começo, então o loop não tem emenda.
# Uso: python3 som/gerar_som.py   (depois: node render.mjs --som)
import numpy as np, wave, os
SR, T, N = 48000, 2.4, 12            # mesmo T e quantidade de perguntas do index.html
DUR = T * N
L = int(DUR * SR)
rng = np.random.default_rng(11)
out = np.zeros((L, 2))

def hz(nota):
    """'C5', 'F#4'… → Hz."""
    nomes = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    n = nomes[nota[0]] + (1 if '#' in nota else 0); o = int(nota[-1])
    return 440 * 2 ** ((n + 12 * (o + 1) - 69) / 12)

def banda(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * ((f >= lo) & (f <= hi)), len(x))

def por(sinal, t0, pan=0.0, ganho=1.0):
    """Mixa em t0 (s) com loop: o que passa do fim volta no começo."""
    i = int(round(t0 * SR)) % L; idx = (np.arange(len(sinal)) + i) % L
    out[idx, 0] += sinal * ganho * np.cos((pan + 1) * np.pi / 4) * 1.41
    out[idx, 1] += sinal * ganho * np.sin((pan + 1) * np.pi / 4) * 1.41

def marimba(f, d=2.0):
    t = np.arange(int(d * SR)) / SR
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.55)
         + 0.35 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t / 0.09)
         + 0.12 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t / 0.03)
         + 0.25 * np.sin(2 * np.pi * f * 2.0 * t + 0.3) * np.exp(-t / 0.3))   # leve brilho de kalimba
    return s * np.minimum(1, t / 0.002) * np.minimum(1, (d - t) / 0.4)   # fecha sem estalo

def madeira(f0, d=0.12):
    t = np.arange(int(d * SR)) / SR
    s = banda(rng.standard_normal(len(t)), f0 * 1.4, f0 * 5) * np.exp(-t / 0.006)
    s = s / np.abs(s).max() * 0.6
    s += np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.035) + 0.4 * np.sin(2 * np.pi * f0 * 2.7 * t) * np.exp(-t / 0.015)
    return s * np.minimum(1, t / 0.0008)

def whoosh(d=0.6):
    t = np.arange(int(d * SR)) / SR
    x = banda(rng.standard_normal(len(t)), 120, 2500)
    return x / np.sqrt(np.mean(x ** 2)) * np.sin(np.pi * t / d) ** 2

def pad(freqs, d):
    t = np.arange(int(d * SR)) / SR; s = np.zeros_like(t)
    for f in freqs:
        for k, a in ((1, 1), (2, .35), (3, .15)):
            for det in (-0.12, 0.12):                                  # leve coro
                s += a * np.sin(2 * np.pi * (f * k + det) * t + rng.uniform(0, 6.3))
    env = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.2)       # entra e sai devagar
    return s * env / len(freqs)

# acordes (3 idas e voltas cada) e notas da melodia (uma por ponta: 6 por acorde)
ACORDES = [
    (['C3'], ['E4', 'G4', 'B4', 'D5'], ['G5', 'B5', 'D6', 'B5', 'G5', 'E5']),
    (['A2'], ['C4', 'E4', 'G4', 'B4'], ['E5', 'G5', 'B5', 'C6', 'B5', 'G5']),
    (['F2'], ['A3', 'C4', 'E4', 'G4'], ['C5', 'E5', 'G5', 'A5', 'G5', 'E5']),
    (['G2'], ['B3', 'D4', 'E4', 'A4'], ['D5', 'G5', 'B5', 'A5', 'G5', 'D5']),
]
DC = 3 * T
for c, (baixo, notas, melodia) in enumerate(ACORDES):
    t0 = c * DC
    por(pad([hz(n) for n in notas], DC + 1.2), t0 - 0.6, ganho=0.05)
    tb = np.arange(int(DC * SR)) / SR
    grave = np.sin(2 * np.pi * hz(baixo[0]) * tb) * np.exp(-tb / 1.2) * np.minimum(1, tb / 0.01) * np.minimum(1, (DC - tb) / 0.3)
    por(grave, t0, ganho=0.07)
    for j, n in enumerate(melodia):
        tp = t0 + j * T / 2                       # pontas: esquerda em k·T, direita em k·T + T/2
        lado = -0.45 if j % 2 == 0 else 0.45
        por(marimba(hz(n)), tp, pan=lado * 0.6, ganho=0.30)

for k in range(2 * N):
    tp = k * T / 2
    direita = k % 2 == 1
    por(madeira(1250 if direita else 900), tp - 0.005, pan=0.5 if direita else -0.5, ganho=0.34)   # tique / taque
    por(whoosh(), tp + T / 4 - 0.3, pan=0.0, ganho=0.035)

# reverb circular (cauda de 1,4 s), 22% molhado
ti = np.arange(int(1.4 * SR)) / SR
for ch in range(2):
    ir = np.zeros(L); ir[:len(ti)] = rng.standard_normal(len(ti)) * np.exp(-ti / 0.35)
    ir = banda(ir, 200, 7000); ir /= np.sqrt(np.sum(ir ** 2))
    molhado = np.fft.irfft(np.fft.rfft(out[:, ch]) * np.fft.rfft(ir), L)
    out[:, ch] = out[:, ch] + 0.22 * molhado * (np.std(out[:, ch]) / (np.std(molhado) + 1e-9))

out *= 10 ** (-1 / 20) / np.abs(out).max()                      # pico em -1 dBFS
cam = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'som.wav')
with wave.open(cam, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes())
print(cam)
