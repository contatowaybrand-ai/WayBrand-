# Gera o toque de telefone antigo (campainha de dois sinos) sincronizado com as animações:
# toques em 0,15–1,0 s e 1,35–2,2 s de cada loop de 4 s. Saída: toque-12s.wav (3 loops, igual ao MP4).
# Uso: python3 gerar.py
import numpy as np, wave
SR, DUR, LOOPS = 44100, 4.0, 3
BURSTS = [(0.15, 1.0), (1.35, 2.2)]
RATE = 26                                            # batidas do martelo por segundo (alterna os dois sinos)
BELLS = [  # (frequências, amplitudes, decaimento s) — parciais inarmônicos de sino
    ([1046, 2380, 3710, 5240], [1, .55, .32, .18], [.32, .16, .09, .05]),
    ([1175, 2675, 4170, 5890], [1, .55, .30, .16], [.30, .15, .08, .05]),
]
n = int(SR * DUR * LOOPS); out = np.zeros((n, 2))
ring = int(SR * .45); tt = np.arange(ring) / SR
strikes = [np.sum([a * np.sin(2*np.pi*f*tt) * np.exp(-tt/d) for f, a, d in zip(*b)], axis=0) for b in BELLS]
rng = np.random.default_rng(7)
click = rng.standard_normal(int(SR*.004)) * np.exp(-np.arange(int(SR*.004))/(SR*.0012))
pan = [(.85, .5), (.5, .85)]
for L in range(LOOPS):
    for a, b in BURSTS:
        k = 0
        for t0 in np.arange(a, b, 1/RATE):
            i = int(SR*(L*DUR + t0)); s = strikes[k % 2].copy(); s[:len(click)] += .35*click
            e = min(n, i+ring); seg = s[:e-i]
            env = min(1, (t0-a)/.04 + .3)            # ataque rápido no começo da rajada
            out[i:e, 0] += seg*env*pan[k%2][0]; out[i:e, 1] += seg*env*pan[k%2][1]; k += 1
out = np.tanh(out / np.abs(out).max() * 2.2)          # saturação leve: mais presença no celular
out = out / np.abs(out).max() * 10**(-1/20)           # -1 dBFS
with wave.open('toque-12s.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes())
print('toque-12s.wav', n/SR, 's')
