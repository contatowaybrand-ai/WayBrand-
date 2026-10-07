# Gera a foto com o bonequinho verde apagado (quadro "off" do pisca).
# Uso: python3 apagar-bonequinho.py
import numpy as np
from PIL import Image, ImageFilter
src = Image.open('assets/semaforo-ref.jpg').convert('RGB')
a = np.asarray(src).astype(float)
h, w, _ = a.shape
# máscara: pixels verdes acesos na área do bonequinho (com o brilho em volta), borda suave
lum = a[..., 1]
m = np.clip((lum - 25) / 90, 0, 1)
box = np.zeros((h, w)); box[535:785, 425:588] = 1
box = np.asarray(Image.fromarray((box * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(10))) / 255
m = np.asarray(Image.fromarray((m * box * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(2))) / 255
# LED apagado: fundo escuro do semáforo com o desenho do bonequinho bem fraco, puxado pro cinza
dark = np.array([8, 13, 11.0])
gray = a.mean(axis=2, keepdims=True)
off = dark + (0.55 * gray + 0.45 * a - dark) * 0.12
out = a * (1 - m[..., None]) + off * m[..., None]
Image.fromarray(np.clip(out, 0, 255).astype('uint8')).save('assets/semaforo-apagado.jpg', quality=95)
