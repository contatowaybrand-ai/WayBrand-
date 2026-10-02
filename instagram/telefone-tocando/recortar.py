# Recorta a mão + telefone da referência e gera assets/mao-telefone.png (transparente, 3x maior).
# Máscara: rembg (modelo isnet-general-use). Reflexos amarelos do fundo no telefone viram verde WayBrand.
# Uso: pip install "rembg[cpu]" pillow numpy && python3 recortar.py
from PIL import Image, ImageFilter
from rembg import remove, new_session
import numpy as np
src = Image.open('referencia.jpg').convert('RGB')
mask = remove(src, session=new_session('isnet-general-use'), only_mask=True)
S = 3
im = src.resize((src.width*S, src.height*S), Image.LANCZOS)
a = np.asarray(im).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
# o modelo deixa o antebraço translúcido: soma com a distância de cor até o amarelo do fundo
d = np.sqrt(((a - np.array([242, 226, 141.]))**2).sum(-1))
m = np.maximum(np.asarray(mask.resize(im.size, Image.LANCZOS)) / 255, np.clip((d - 10) / 18, 0, 1))
al = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.4))
mx, mn = a.max(-1), a.min(-1); sat = (mx - mn) / np.maximum(mx, 1)
spill = (sat > 0.6) & ((g - b) > 30) & ((r - g) < 80)              # amarelo/ocre saturado, não pele
lum = (0.3*r + 0.59*g + 0.11*b)[..., None]
green = np.array([0, 180, 144.]) / (0.59*180 + 0.11*144)
rgb = np.where(spill[..., None], np.clip(lum * green, 0, 255), a)
out = Image.fromarray(rgb.astype(np.uint8)).convert('RGBA'); out.putalpha(al)
out.save('assets/mao-telefone.png'); print(out.size)
