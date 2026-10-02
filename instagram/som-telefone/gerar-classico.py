# Campainha clássica de telefone de disco (estilo Western Electric 500 / telefone de filme):
# corrente de toque de 20 Hz faz o martelo bater nos dois gongos de aço alternadamente → 40 batidas/s.
# Gongos brilhantes com parciais inarmônicos e sustentação longa; sala pequena.
#   classico-longo.wav  "trrrriiiim… trrrriiiim…"  (um toque em cada rajada da animação: 0,15–1,0 s e 1,35–2,2 s)
#   classico-duplo.wav  "trim-trim… trim-trim…"    (cada rajada vira dois toques curtos: 0,35 s + pausa 0,15 s + 0,35 s)
# Uso: python3 gerar-classico.py
import numpy as np, wave
SR, DUR, LOOPS = 44100, 4.0, 3
n = int(SR*DUR*LOOPS); f = np.fft.rfftfreq(n, 1/SR)
rng = np.random.default_rng(11)
ring = int(SR*1.6); tt = np.arange(ring)/SR
RAT = [1, 2.76, 5.40, 8.93]                       # modos de um gongo em forma de cúpula
GONGS = [(1180, [1, .8, .5, .25], [1.3, .55, .25, .12]),
         (1390, [1, .75, .45, .22], [1.2, .5, .22, .11])]
def gong(f0, amps, decs):
    return sum(a*np.sin(2*np.pi*f0*r*(1+rng.uniform(-.003, .003))*tt + rng.uniform(0, 6.3))*np.exp(-tt/d)
               for r, a, d in zip(RAT, amps, decs))
G = [gong(*g) for g in GONGS]
tick = rng.standard_normal(int(SR*.003))*np.exp(-np.arange(int(SR*.003))/(SR*.0008))
def make(segments, name):
    x = np.zeros(n)
    for L in range(LOOPS):
        for a, b in segments:
            for k, t0 in enumerate(np.arange(a, b, 1/40)):
                i = int(SR*(L*DUR+t0)); e = min(n, i+ring)
                s = G[k % 2].copy(); s[:len(tick)] += .6*tick
                amp = (.8+.2*rng.random()) * min(1, (t0-a)/.03+.5)
                x[i:e] += s[:e-i]*amp
    # amortecimento natural quando a corrente para: o gongo continua soando (já está no decaimento)
    irn = int(SR*.35); ir = rng.standard_normal(irn)*np.exp(-np.arange(irn)/(SR*.07)); ir[0] = 10
    w = np.fft.irfft(np.fft.rfft(x, n+irn)*np.fft.rfft(ir, n+irn))[:n]
    y = .8*x/np.abs(x).max() + .2*w/np.abs(w).max()
    Y = np.fft.rfft(y); Y *= 1/np.sqrt(1+(180/np.maximum(f, 1))**4)/np.sqrt(1+(f/9000)**4); y = np.fft.irfft(Y, n)
    y = np.tanh(y/np.abs(y).max()*1.6); y = y/np.abs(y).max()*10**(-1/20)
    st = np.stack([y, np.roll(y, int(SR*.0005))], 1)
    with wave.open(name, 'wb') as wv:
        wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((st*32767).astype('<i2').tobytes())
    print(name)
make([(0.15, 1.0), (1.35, 2.2)], 'classico-longo.wav')
make([(0.15, .50), (.65, 1.0), (1.35, 1.70), (1.85, 2.2)], 'classico-duplo.wav')
