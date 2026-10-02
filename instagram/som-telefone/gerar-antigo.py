# Toque nostálgico de telefone de disco (campainha de gongo metálico, anos 60/70), com cara de gravação antiga:
# gongos graves e longos, martelo batendo a ~20 Hz, sala com eco curto, banda estreita de alto-falante velho,
# chiado e estalos leves de vinil. Sincronizado com os toques da animação (0,15–1,0 s e 1,35–2,2 s de cada loop de 4 s).
# Saída: toque-antigo-12s.wav (3 loops). Uso: python3 gerar-antigo.py
import numpy as np, wave
SR, DUR, LOOPS = 44100, 4.0, 3
BURSTS = [(0.15, 1.0), (1.35, 2.2)]
RATE = 20                                            # batidas por segundo, alternando os dois gongos
RATIOS = [1, 2.32, 4.25, 6.63, 9.38]                 # parciais de gongo/sino
GONGS = [(690, [1, .7, .45, .25, .12], [.9, .45, .25, .14, .08]),
         (820, [1, .65, .4, .22, .10], [.85, .42, .22, .12, .07])]
n = int(SR * DUR * LOOPS); dry = np.zeros(n)
ring = int(SR * 1.2); tt = np.arange(ring) / SR
rng = np.random.default_rng(3)
def gong(f0, amps, decs):
    s = np.zeros(ring)
    for r, a, d in zip(RATIOS, amps, decs):
        det = 1 + rng.uniform(-.004, .004)          # leve desafinação: metal real
        s += a * np.sin(2*np.pi*f0*r*det*tt + rng.uniform(0, 6.28)) * np.exp(-tt/d)
    return s
strikes = [gong(*g) for g in GONGS]
hit = rng.standard_normal(int(SR*.006)) * np.exp(-np.arange(int(SR*.006))/(SR*.0015))   # "tec" do martelo
for L in range(LOOPS):
    for a, b in BURSTS:
        for k, t0 in enumerate(np.arange(a, b, 1/RATE)):
            i = int(SR*(L*DUR + t0)); e = min(n, i+ring)
            s = strikes[k % 2].copy(); s[:len(hit)] += .5*hit
            vel = .75 + .25*rng.random()             # o martelo nunca bate igual
            dry[i:e] += s[:e-i] * vel * min(1, (t0-a)/.05 + .4)
dry /= np.abs(dry).max()
# sala: eco curto (resposta de ruído com decaimento) — dá o "corredor de casa antiga"
irn = int(SR*.7); ir = rng.standard_normal(irn) * np.exp(-np.arange(irn)/(SR*.18)); ir[0] = 6
wet = np.fft.irfft(np.fft.rfft(dry, n+irn) * np.fft.rfft(ir, n+irn))[:n]
x = .75*dry + .25*wet/np.abs(wet).max()
# alto-falante/gravação antiga: banda 350–4200 Hz
X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1/SR)
X *= 1/np.sqrt(1+(350/np.maximum(f, 1))**4) / np.sqrt(1+(f/4200)**4); x = np.fft.irfft(X, n)
x = np.tanh(x/np.abs(x).max()*1.8)                  # saturação de fita
# vinil: chiado bem baixo + estalos esparsos
hiss = rng.standard_normal(n); H = np.fft.rfft(hiss); H *= 1/np.sqrt(1+(f/3000)**2); hiss = np.fft.irfft(H, n)
x += .012*hiss/np.abs(hiss).max()
for p in rng.choice(n-200, 30, replace=False): x[p:p+60] += rng.choice([-1, 1]) * .12 * np.exp(-np.arange(60)/8)
x = x/np.abs(x).max() * 10**(-1/20)
st = np.stack([x, np.roll(x, int(SR*.0004))], 1)     # estéreo bem estreito, como gravação mono antiga
with wave.open('toque-antigo-12s.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
print('toque-antigo-12s.wav', n/SR, 's')
