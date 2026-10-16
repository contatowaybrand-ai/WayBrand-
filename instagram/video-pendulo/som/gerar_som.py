# Gera a trilha do reel (28,8 s, 48 kHz, estéreo) sincronizada com o pêndulo do index.html.
# Uso: python3 som/gerar_som.py [versão] [saída.wav]     (padrão: cinema → som/som.wav)
#      depois: node render.mjs --som
# Versões:
#   cinema  – baque grave e encorpado em cada ponta (pêndulo pesado), tique metálico fino de relógio,
#             whoosh que acompanha a velocidade e o lado do pêndulo, fundo grave escuro (Lá menor).
#   groove  – batida lo-fi a 100 BPM casada com o pêndulo: bumbo nas pontas, palma no meio do balanço,
#             chimbal em colcheias, piano elétrico (Am9, Fmaj9, Cmaj9, G6) e baixo.
#   marimba – 1ª versão (tique-taque de madeira + melodia de marimba).
# Pontas do pêndulo: esquerda em k·T, direita em k·T + T/2. Meio do balanço: T/4 e 3T/4.
import numpy as np, wave, os, sys
SR, T, N = 48000, 2.4, 12            # mesmo T e quantidade de perguntas do index.html
DUR = T * N
L = int(DUR * SR)
rng = np.random.default_rng(11)
out = np.zeros((L, 2))
tt = np.arange(L) / SR

def hz(nota):
    """'C5', 'F#4'… → Hz."""
    nomes = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    n = nomes[nota[0]] + (1 if '#' in nota else 0); o = int(nota[-1])
    return 440 * 2 ** ((n + 12 * (o + 1) - 69) / 12)

def banda(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * ((f >= lo) & (f <= hi)), len(x))

def por(sinal, t0, pan=0.0, ganho=1.0):
    """Mixa em t0 (s) com loop: o que passa do fim volta no começo. Sinal mono (pan) ou estéreo (n, 2)."""
    i = int(round(t0 * SR)) % L; idx = (np.arange(len(sinal)) + i) % L
    if sinal.ndim == 2:
        out[idx] += sinal * ganho; return
    out[idx, 0] += sinal * ganho * np.cos((pan + 1) * np.pi / 4) * 1.41
    out[idx, 1] += sinal * ganho * np.sin((pan + 1) * np.pi / 4) * 1.41

def fade(s, d, ini=0.002, fim=0.05):
    t = np.arange(len(s)) / SR
    return s * np.minimum(1, t / ini) * np.minimum(1, (d - t) / fim)

def ruido(d):
    return rng.standard_normal(int(d * SR))

def reverb(cauda=1.6, tempo=0.4, molhado=0.25, lo=150, hi=8000):
    """Reverb circular: a cauda do fim cai no começo, então o loop não tem emenda."""
    ti = np.arange(int(cauda * SR)) / SR
    for ch in range(2):
        ir = np.zeros(L); ir[:len(ti)] = rng.standard_normal(len(ti)) * np.exp(-ti / tempo)
        ir = banda(ir, lo, hi)
        w = np.fft.irfft(np.fft.rfft(out[:, ch]) * np.fft.rfft(ir), L)
        out[:, ch] += molhado * w * (np.std(out[:, ch]) / (np.std(w) + 1e-9))

def pan_pendulo(t):
    """Lado do pêndulo em t: -1 esquerda … +1 direita."""
    return -np.cos(2 * np.pi * t / T)

# ── versão cinema ────────────────────────────────────────────────────
def cinema():
    def baque(d=0.9):
        t = np.arange(int(d * SR)) / SR
        f = 44 + 30 * np.exp(-t / 0.05)                            # queda de afinação: peso
        corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28)
        toc = banda(ruido(d), 180, 2200) * np.exp(-t / 0.012)       # contato, abafado
        toc /= np.abs(toc).max()
        return fade(corpo + 0.35 * toc + 0.25 * np.tanh(3 * corpo), d, fim=0.2)
    def tique(d=0.08):
        t = np.arange(int(d * SR)) / SR
        s = banda(ruido(d), 3500, 11000) * np.exp(-t / 0.0035)
        s = s / np.abs(s).max() + 0.4 * np.sin(2 * np.pi * 3150 * t) * np.exp(-t / 0.012)
        return fade(s, d, ini=0.0003, fim=0.01)
    def whoosh(t0, d=1.0, dir_=1):
        n = int(d * SR); t = np.arange(n) / SR
        x = ruido(d)
        # filtro que abre no meio (maior velocidade) e fecha nas pontas, em 3 faixas somadas
        env = np.sin(np.pi * t / d) ** 2
        s = (banda(x, 80, 400) * 1.0 * env ** 0.8 + banda(x, 400, 1500) * 0.6 * env ** 1.6
             + banda(x, 1500, 5000) * 0.18 * env ** 3)
        s /= np.sqrt(np.mean(s ** 2)) + 1e-9
        pan = pan_pendulo(t0 + t)                                    # acompanha o lado do pêndulo
        st = np.stack([s * np.cos((pan + 1) * np.pi / 4), s * np.sin((pan + 1) * np.pi / 4)], 1) * 1.41
        return st
    for k in range(2 * N):
        tp = k * T / 2; direita = k % 2 == 1
        por(baque(), tp, pan=0.25 if direita else -0.25, ganho=0.55)
        por(tique(), tp - 0.004, pan=0.6 if direita else -0.6, ganho=0.12)
        por(whoosh(tp + T / 4 - 0.35, d=0.7), tp + T / 4 - 0.35, ganho=0.06)
    # fundo: Lá menor escuro, respirando no tempo do loop inteiro (fecha sem emenda)
    resp = 0.6 + 0.4 * np.sin(2 * np.pi * tt / DUR * 2) ** 2
    for f, a in ((hz('A1'), 1.0), (hz('E2'), .55), (hz('A2'), .45), (hz('C3'), .30), (hz('E3'), .18)):
        fq = round(f * DUR) / DUR                    # nº inteiro de ciclos por loop: sem emenda
        out[:, 0] += 0.03 * a * resp * np.sin(2 * np.pi * fq * tt + 1.1)
        out[:, 1] += 0.03 * a * resp * np.sin(2 * np.pi * (fq + 2 / DUR) * tt)   # leve batimento estéreo
    reverb(cauda=2.0, tempo=0.5, molhado=0.16)

# ── versão groove (100 BPM: 1 compasso = 1 ida e volta) ──────────────
def groove():
    B = T / 4                                                         # 1 tempo = 0,6 s
    def bumbo(d=0.5):
        t = np.arange(int(d * SR)) / SR
        f = 50 + 90 * np.exp(-t / 0.03)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)
        return fade(np.tanh(1.8 * s), d, ini=0.001, fim=0.08)
    def palma(d=0.35):
        t = np.arange(int(d * SR)) / SR; s = np.zeros_like(t)
        for o in (0, 0.011, 0.022):                                   # 3 batidas rápidas = palma
            m = t >= o; s[m] += np.exp(-(t[m] - o) / (0.008 if o < 0.02 else 0.09))
        s *= banda(ruido(d), 900, 7000); s /= np.abs(s).max()
        return fade(s, d, ini=0.0005)
    def chimbal(d=0.07, aberto=False):
        d = 0.22 if aberto else d
        t = np.arange(int(d * SR)) / SR
        s = banda(ruido(d), 7000, 16000) * np.exp(-t / (0.06 if aberto else 0.012))
        return fade(s / np.abs(s).max(), d, ini=0.0005, fim=0.01)
    def rhodes(f, d):
        t = np.arange(int(d * SR)) / SR
        trem = 1 + 0.18 * np.sin(2 * np.pi * 4.2 * t)
        s = (np.sin(2 * np.pi * f * t) * np.exp(-t / 1.6)
             + 0.22 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.5)
             + 0.12 * np.sin(2 * np.pi * f * 7.1 * t) * np.exp(-t / 0.05))   # "sino" do ataque
        return fade(s * trem, d, ini=0.003, fim=0.3)
    def baixo(f, d):
        t = np.arange(int(d * SR)) / SR
        s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
        return fade(np.tanh(1.5 * s) * np.exp(-t / 0.9), d, ini=0.004, fim=0.06)
    ACORDES = [('A1', ['C4', 'E4', 'G4', 'B4']),        # Am9
               ('F1', ['A3', 'C4', 'E4', 'G4']),        # Fmaj9
               ('C2', ['E3', 'G3', 'B3', 'D4']),        # Cmaj9
               ('G1', ['B3', 'D4', 'E4', 'A4'])]        # G6/9
    for c in range(N):
        t0 = c * T
        raiz, notas = ACORDES[c % 4]
        por(bumbo(), t0, ganho=0.75); por(bumbo(), t0 + 2 * B, ganho=0.65)          # pontas
        por(bumbo(), t0 + 3.5 * B, ganho=0.35)                                       # contratempo
        por(palma(), t0 + B, pan=0.1, ganho=0.30); por(palma(), t0 + 3 * B, pan=0.1, ganho=0.30)  # meio do balanço
        for h in range(8):
            sw = 0.03 if h % 2 else 0                                                # leve swing
            por(chimbal(aberto=(h == 7)), t0 + h * B / 2 + sw, pan=0.35, ganho=0.10 if h % 2 else 0.16)
        for j, n in enumerate(notas):                                                 # acorde dedilhado
            por(rhodes(hz(n), T + 0.6), t0 + j * 0.018, pan=-0.3 + 0.2 * j, ganho=0.11)
        por(rhodes(hz(notas[-1]) * 2, 1.0), t0 + 2.5 * B, pan=0.3, ganho=0.05)        # resposta no tempo 3
        por(baixo(hz(raiz), 1.1), t0, ganho=0.42); por(baixo(hz(raiz) * 1.5, 0.5), t0 + 2.5 * B, ganho=0.28)
    reverb(cauda=1.2, tempo=0.3, molhado=0.16)
    for ch in range(2):                                               # lo-fi: tira o brilho de cima
        out[:, ch] = banda(out[:, ch], 25, 11000)

# ── versão marimba (1ª versão) ───────────────────────────────────────
def marimba_v():
    def marimba(f, d=2.0):
        t = np.arange(int(d * SR)) / SR
        s = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.55)
             + 0.35 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t / 0.09)
             + 0.12 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t / 0.03)
             + 0.25 * np.sin(2 * np.pi * f * 2.0 * t + 0.3) * np.exp(-t / 0.3))
        return fade(s, d, fim=0.4)
    def madeira(f0, d=0.12):
        t = np.arange(int(d * SR)) / SR
        s = banda(ruido(d), f0 * 1.4, f0 * 5) * np.exp(-t / 0.006); s = s / np.abs(s).max() * 0.6
        s += np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.035) + 0.4 * np.sin(2 * np.pi * f0 * 2.7 * t) * np.exp(-t / 0.015)
        return fade(s, d, ini=0.0008, fim=0.01)
    MEL = [['G5', 'B5', 'D6', 'B5', 'G5', 'E5'], ['E5', 'G5', 'B5', 'C6', 'B5', 'G5'],
           ['C5', 'E5', 'G5', 'A5', 'G5', 'E5'], ['D5', 'G5', 'B5', 'A5', 'G5', 'D5']]
    for c, mel in enumerate(MEL):
        for j, n in enumerate(mel):
            por(marimba(hz(n)), c * 3 * T + j * T / 2, pan=-0.27 if j % 2 == 0 else 0.27, ganho=0.30)
    for k in range(2 * N):
        direita = k % 2 == 1
        por(madeira(1250 if direita else 900), k * T / 2 - 0.005, pan=0.5 if direita else -0.5, ganho=0.34)
    reverb(cauda=1.4, tempo=0.35, molhado=0.22)

versao = sys.argv[1] if len(sys.argv) > 1 else 'cinema'
{'cinema': cinema, 'groove': groove, 'marimba': marimba_v}[versao]()
out *= 10 ** (-1 / 20) / np.abs(out).max()                      # pico em -1 dBFS
cam = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'som.wav')
with wave.open(cam, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes())
print(versao, '→', cam)
