# Gera a trilha do reel (28,8 s, 48 kHz, estéreo) sincronizada com o pêndulo do index.html.
# Uso: python3 som/gerar_som.py [versão] [saída.wav]     (padrão: trap → som/som.wav)
#      depois: node render.mjs --som
# Só pêndulo:
#   relogio – tique-taque mecânico de relógio de pêndulo (clique do mecanismo + caixa de madeira).
#   metal   – pêndulo pesado: ar cortado (mais forte no meio do balanço) + tilintar de corrente nas pontas.
# Com batida (100 BPM: 1 compasso = 1 ida e volta, tempos 1 e 3 nas pontas, 2 e 4 no meio do balanço):
#   trap    – bumbo + 808 nas pontas, caixa no meio, chimbal feito com o tique do relógio.
#   house   – bumbo em todo tempo, palma no meio, chimbal aberto no contratempo, baixo pulsante + tique-taque.
import numpy as np, wave, os, sys
SR, T, N = 48000, 2.4, 12            # mesmo T e quantidade de perguntas do index.html
DUR = T * N
B = T / 4                            # 1 tempo = 0,6 s (100 BPM)
L = int(DUR * SR)
rng = np.random.default_rng(5)
out = np.zeros((L, 2))

def hz(nota):
    nomes = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    n = nomes[nota[0]] + (1 if '#' in nota else 0); o = int(nota[-1])
    return 440 * 2 ** ((n + 12 * (o + 1) - 69) / 12)

def banda(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * ((f >= lo) & (f <= hi)), len(x))

def tempo(d):
    return np.arange(int(d * SR)) / SR

def fade(s, ini=0.0005, fim=0.02):
    t = np.arange(len(s)) / SR; d = len(s) / SR
    return s * np.minimum(1, t / ini) * np.minimum(1, (d - t) / fim)

def norm(s):
    return s / (np.abs(s).max() + 1e-12)

def por(sinal, t0, pan=0.0, ganho=1.0):
    """Mixa em t0 (s) com loop: o que passa do fim volta no começo. Mono (com pan) ou estéreo (n, 2)."""
    i = int(round(t0 * SR)) % L; idx = (np.arange(len(sinal)) + i) % L
    if sinal.ndim == 2:
        out[idx] += sinal * ganho; return
    out[idx, 0] += sinal * ganho * np.cos((pan + 1) * np.pi / 4) * 1.41
    out[idx, 1] += sinal * ganho * np.sin((pan + 1) * np.pi / 4) * 1.41

def reverb(cauda=1.2, decai=0.3, molhado=0.2, lo=200, hi=9000):
    """Reverb circular: a cauda do fim cai no começo, então o loop não tem emenda."""
    ti = tempo(cauda)
    for ch in range(2):
        ir = np.zeros(L); ir[:len(ti)] = rng.standard_normal(len(ti)) * np.exp(-ti / decai)
        ir = banda(ir, lo, hi)
        w = np.fft.irfft(np.fft.rfft(out[:, ch]) * np.fft.rfft(ir), L)
        out[:, ch] += molhado * w * (np.std(out[:, ch]) / (np.std(w) + 1e-9))

def modos(t, lista):
    """Soma de ressonâncias amortecidas: (freq, amplitude, decaimento)."""
    return sum(a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.3)) * np.exp(-t / d) for f, a, d in lista)

def comprimir(drive):
    """Segura os picos (som de cliques fica mais presente sem estourar)."""
    global out
    out = np.tanh(drive * out / np.abs(out).max())

# ── sons de pêndulo ──────────────────────────────────────────────────
def tique_relogio(tom=1.0, d=0.35):
    """Escape de relógio: 2 cliques metálicos colados + caixa de madeira ressoando."""
    t = tempo(d); s = np.zeros_like(t)
    for o, a in ((0.0, 1.0), (0.007 * tom, 0.55), (0.019, 0.25)):
        m = t >= o; tt = t[m] - o
        s[m] += a * banda(rng.standard_normal(m.sum()), 1800 * tom, 9000) * np.exp(-tt / 0.0025)
        s[m] += a * 0.5 * modos(tt, [(3100 * tom, 1, .006), (4650 * tom, .6, .004), (6900 * tom, .4, .003)])
    caixa = modos(t, [(190 * tom, 1, .11), (410 * tom, .7, .08), (880 * tom, .45, .05), (1530 * tom, .3, .03)])
    return fade(norm(s) + 0.55 * norm(caixa), fim=0.05)

def ar_pendulo(d):
    """Ar cortado: ruído com filtro que abre na velocidade máxima (meio) e fecha nas pontas."""
    t = tempo(d); x = rng.standard_normal(len(t))
    v = np.sin(np.pi * t / d)                                         # velocidade (0 nas pontas)
    s = banda(x, 60, 300) * v ** 2.5 + banda(x, 300, 900) * 0.7 * v ** 3.5 + banda(x, 900, 3000) * 0.3 * v ** 5
    return s / np.sqrt(np.mean(s ** 2))

def tilintar(d=0.5):
    """Corrente/gancho de metal que encosta na ponta do balanço."""
    t = tempo(d); s = np.zeros_like(t)
    for o, a in ((0.0, 1.0), (0.023, 0.45), (0.051, 0.2)):
        m = t >= o; tt = t[m] - o
        s[m] += a * (modos(tt, [(2330, 1, .09), (3710, .7, .06), (5170, .5, .04), (6890, .3, .025)])
                     + 0.6 * banda(rng.standard_normal(m.sum()), 3000, 12000) * np.exp(-tt / 0.002))
    return fade(norm(s), fim=0.08)

def baque_pendulo(d=0.4):
    t = tempo(d)
    return fade(norm(np.sin(2 * np.pi * (60 + 25 * np.exp(-t / 0.02)) * t) * np.exp(-t / 0.09)), fim=0.05)

# ── bateria ──────────────────────────────────────────────────────────
def bumbo(d=0.45, grave=50):
    t = tempo(d)
    f = grave + 110 * np.exp(-t / 0.025)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)
    clique = banda(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.002)
    return fade(np.tanh(2.2 * s) + 0.15 * norm(clique), fim=0.05)

def oito_o_oito(f, d=1.1, desliza=None):
    t = tempo(d)
    fq = f * (1 + 1.0 * np.exp(-t / 0.018))
    if desliza: fq = fq * (1 + (desliza - 1) * np.clip((t - d * 0.55) / (d * 0.3), 0, 1))
    s = np.sin(2 * np.pi * np.cumsum(fq) / SR) * np.exp(-t / 0.7)
    return fade(np.tanh(2.5 * s), ini=0.001, fim=0.12)

def caixa(d=0.3):
    t = tempo(d)
    s = banda(rng.standard_normal(len(t)), 1200, 9000) * np.exp(-t / 0.07)
    s = norm(s) + 0.6 * np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.04) + 0.3 * np.sin(2 * np.pi * 330 * t) * np.exp(-t / 0.03)
    return fade(norm(s), fim=0.03)

def palma(d=0.3):
    t = tempo(d); env = np.zeros_like(t)
    for o in (0, 0.009, 0.019, 0.028):
        m = t >= o; env[m] += np.exp(-(t[m] - o) / (0.006 if o < 0.025 else 0.08))
    return fade(norm(env * banda(rng.standard_normal(len(t)), 900, 8000)), fim=0.03)

def chimbal(aberto=False):
    d = 0.25 if aberto else 0.06; t = tempo(d)
    s = banda(rng.standard_normal(len(t)), 7000, 17000) + 0.3 * modos(t, [(8200, 1, .02), (10400, .7, .015)])
    return fade(norm(s) * np.exp(-t / (0.07 if aberto else 0.012)), fim=0.01)

# ── versões ──────────────────────────────────────────────────────────
def relogio():
    for k in range(2 * N):
        tique = k % 2 == 1                                   # tique na direita, taque na esquerda
        por(tique_relogio(1.0 if tique else 0.84), k * T / 2, pan=0.35 if tique else -0.35, ganho=0.8)
    reverb(cauda=1.0, decai=0.18, molhado=0.22, lo=150, hi=7000)
    comprimir(5)

def metal():
    for k in range(2 * N):
        tp = k * T / 2; direita = k % 2 == 1; lado = 1 if direita else -1
        s = ar_pendulo(T / 2)                                 # de uma ponta à outra
        t = tempo(T / 2); pan = lado * np.cos(np.pi * t / (T / 2))      # acompanha o lado
        por(np.stack([s * np.cos((pan + 1) * np.pi / 4), s * np.sin((pan + 1) * np.pi / 4)], 1) * 1.41, tp, ganho=0.08)
        por(tilintar(), tp - 0.01, pan=0.6 * lado, ganho=0.22)
        por(baque_pendulo(), tp, pan=0.3 * lado, ganho=0.18)
    reverb(cauda=1.6, decai=0.4, molhado=0.25)

def trap():
    NOTAS = ['A1', 'A1', 'F1', 'G1']                          # 808 por compasso
    for c in range(N):
        t0 = c * T; raiz = hz(NOTAS[c % 4])
        por(bumbo(grave=48), t0, ganho=0.8); por(bumbo(grave=48), t0 + 2 * B, ganho=0.7)
        por(bumbo(grave=48), t0 + 2.75 * B, ganho=0.5)
        por(oito_o_oito(raiz, 1.15), t0, ganho=0.55)
        por(oito_o_oito(raiz, 0.55, desliza=1.5 if c % 2 else None), t0 + 2 * B, ganho=0.45)
        por(caixa(), t0 + B, ganho=0.5); por(caixa(), t0 + 3 * B, ganho=0.5)            # meio do balanço
        for h in range(8):                                    # chimbal = tique do relógio em colcheias
            ponta = h % 4 == 0
            por(tique_relogio(1.0 if h % 2 else 0.9, d=0.12), t0 + h * B / 2, pan=0.3 if h % 2 else -0.3,
                ganho=0.42 if ponta else 0.2)
        if c % 2 == 1:                                        # rufo de chimbal no fim de 2 compassos
            for r in range(6):
                por(chimbal(), t0 + 3.5 * B + r * B / 12, pan=0.4, ganho=0.12 + 0.02 * r)
    reverb(cauda=0.9, decai=0.2, molhado=0.12)

def house():
    NOTAS = ['A1', 'A1', 'F1', 'G1']
    for c in range(N):
        t0 = c * T; raiz = hz(NOTAS[c % 4])
        for b in range(4):
            por(bumbo(d=0.4, grave=52), t0 + b * B, ganho=0.75)
            por(chimbal(aberto=True), t0 + b * B + B / 2, pan=0.25, ganho=0.22)              # contratempo
            tb = tempo(B * 0.45)
            baixo = np.tanh(2 * (np.sin(2 * np.pi * raiz * 2 * tb) + 0.4 * np.sin(2 * np.pi * raiz * 4 * tb)))
            por(fade(baixo * np.exp(-tb / 0.15), ini=0.004, fim=0.03), t0 + b * B + B / 2, ganho=0.30)
        por(palma(), t0 + B, pan=0.1, ganho=0.45); por(palma(), t0 + 3 * B, pan=0.1, ganho=0.45)  # meio do balanço
        for h in range(16):
            if h % 4: por(chimbal(), t0 + h * B / 4, pan=-0.3, ganho=0.07 if h % 2 else 0.1)
        por(tique_relogio(1.0, d=0.2), t0 + 2 * B, pan=0.4, ganho=0.35)                   # tique (direita)
        por(tique_relogio(0.84, d=0.2), t0, pan=-0.4, ganho=0.35)                         # taque (esquerda)
    reverb(cauda=1.0, decai=0.22, molhado=0.14)

versao = sys.argv[1] if len(sys.argv) > 1 else 'trap'
{'relogio': relogio, 'metal': metal, 'trap': trap, 'house': house}[versao]()
out *= 10 ** (-1 / 20) / np.abs(out).max()                      # pico em -1 dBFS
cam = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'som.wav')
with wave.open(cam, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes())
print(versao, '→', cam)
