# Opções de toque (12 s = 3 loops de 4 s), todas sintetizadas aqui:
#   nokia.wav     melodia "Nokia tune" (Gran Vals, Francisco Tárrega, 1902, domínio público) em bipe monofônico
#   tuuu.wav      tom de chamada do telefone fixo brasileiro (425 Hz), soa nos dois toques da animação
#   sem-fio.wav   trinado eletrônico de telefone sem fio dos anos 90, nos dois toques da animação
# Uso: python3 gerar-opcoes.py
import numpy as np, wave
SR, DUR, LOOPS = 44100, 4.0, 3
BURSTS = [(0.15, 1.0), (1.35, 2.2)]
n = int(SR*DUR*LOOPS); t = np.arange(n)/SR
f = np.fft.rfftfreq(n, 1/SR)
def band(x, lo, hi):
    X = np.fft.rfft(x); X *= 1/np.sqrt(1+(lo/np.maximum(f, 1))**4)/np.sqrt(1+(f/hi)**4); return np.fft.irfft(X, n)
def save(name, x):
    x = x/np.abs(x).max()*10**(-1/20); st = np.stack([x, x], 1)
    with wave.open(name, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
    print(name)
def gate(a, b, fade=.008):
    m = np.zeros(n)
    for L in range(LOOPS):
        for x0, x1 in BURSTS:
            s, e = L*DUR+x0, L*DUR+x1
            m = np.maximum(m, np.clip(np.minimum((t-s)/fade, (e-t)/fade), 0, 1))
    return m

# 1) Nokia: 13 notas, 180 bpm, onda quadrada suavizada (cara de celular 3310)
N = {'E5':659.25,'D5':587.33,'F#4':369.99,'G#4':415.30,'C#5':554.37,'B4':493.88,'D4':293.66,'E4':329.63,'A4':440.0,'C#4':277.18}
mel = [('E5',.5),('D5',.5),('F#4',1),('G#4',1),('C#5',.5),('B4',.5),('D4',1),('E4',1),('B4',.5),('A4',.5),('C#4',1),('E4',1),('A4',2)]
beat = 60/180; x = np.zeros(n)
for L in range(LOOPS):
    pos = L*DUR + .15
    for note, d in mel:
        s = int(SR*pos); dur = d*beat; m = int(SR*dur*.92); tt = np.arange(m)/SR
        env = np.minimum(1, np.minimum(tt/.004, (dur*.92-tt)/.01))
        x[s:s+m] += np.sign(np.sin(2*np.pi*N[note]*tt)) * env * .8
        pos += dur
save('nokia.wav', band(x, 250, 5000))

# 2) Tuuu: 425 Hz com leve distorção de linha, banda de telefone 300–3400 Hz
x = (np.sin(2*np.pi*425*t) + .18*np.sin(2*np.pi*850*t) + .08*np.sin(2*np.pi*1275*t)) * gate(0, 0, .02)
x += .004*np.random.default_rng(1).standard_normal(n)      # chiado da linha
save('tuuu.wav', band(x, 300, 3400))

# 3) Sem fio anos 90: alterna 1100/1450 Hz a 16 trocas por segundo, timbre de buzzer
sw = (np.floor(t*16) % 2).astype(bool); fr = np.where(sw, 1450, 1100)
ph = 2*np.pi*np.cumsum(fr)/SR
x = np.tanh(3*np.sin(ph)) * gate(0, 0, .004)
save('sem-fio.wav', band(x, 400, 6000))
