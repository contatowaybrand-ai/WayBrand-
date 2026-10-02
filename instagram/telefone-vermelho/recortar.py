# Recorta a referência (fundo azul-piscina) e gera duas camadas 2x maiores, no mesmo enquadramento:
#   assets/mao-fone.png  manga + mão + fone + fio      assets/base.png  corpo do telefone (é ele que treme)
# Telefone vermelho -> verde WayBrand #00B490. Manga listrada -> preta (mantém as dobras, some com as listras).
# Uso: pip install "rembg[cpu]" pillow numpy && python3 recortar.py
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove, new_session
import numpy as np
src = Image.open('referencia.jpg').convert('RGB')
W, H = src.size
mask = np.asarray(remove(src, session=new_session('isnet-general-use'), only_mask=True)) / 255
a = np.asarray(src).astype(float)
d = np.sqrt(((a - np.array([75, 183, 186.]))**2).sum(-1))
alpha = np.maximum(mask, np.clip((d - 70) / 30, 0, 1))      # reforço por cor: segura o fio fino

def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=255); return np.asarray(m) > 0

hsv = np.asarray(src.convert('HSV')).astype(float); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
redh = (h <= 8) | (h >= 238)
hand_box = poly([(372, 192), (470, 196), (520, 232), (515, 300), (470, 345), (395, 350), (360, 300)])
red = redh & np.where(hand_box, s > 170, s > 25)            # perto da mão só o vermelho bem saturado (pele fica)
# manga: polígono até o punho, menos a pele (pele = laranja pouco saturado)
sleeve_area = poly([(0, 0), (225, 0), (428, 188), (402, 224), (376, 266), (346, 292), (318, 311), (298, 318), (0, 185)])
skin = (h > 8) & (h < 40) & (s > 40)
sleeve = sleeve_area & ~(skin & (np.arange(W)[None, :] > 370))
# telefone: vermelho fora da manga
phone = red & ~sleeve
teal = (h > 115) & (h < 145) & (s > 60) & ~sleeve           # sobra do fundo (sombra azul): fora
alpha = alpha * ~teal
out = a.copy()
hsv2 = hsv.copy(); hsv2[..., 0] = np.where(phone, 119, h); hsv2[..., 2] = np.where(phone, v * .74, v)
g = np.asarray(Image.fromarray(hsv2.astype(np.uint8), 'HSV').convert('RGB')).astype(float)
out = np.where(phone[..., None], g, out)
# manga preta: luminância bem borrada (some a listra, ficam as dobras)
lum = np.asarray(Image.fromarray(v.astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(float) / 255   # V: listra branca e vermelha têm brilho parecido
black = (8 + 30 * lum)[..., None] * np.array([1, 1.03, 1.02])
soft = np.asarray(Image.fromarray((sleeve * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(float)[..., None] / 255
out = out * (1 - soft) + black * soft
S = 2
img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA').resize((W*S, H*S), Image.LANCZOS)
al = Image.fromarray((alpha * 255).astype(np.uint8)).resize((W*S, H*S), Image.LANCZOS).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
base_m = Image.new('L', (W*S, H*S), 0); ImageDraw.Draw(base_m).rectangle([416*S, 640*S, 700*S, 985*S], fill=255)
bm = np.asarray(base_m) / 255; A = np.asarray(al) / 255
for name, m in [('mao-fone', 1 - bm), ('base', bm)]:
    o = img.copy(); o.putalpha(Image.fromarray((A * m * 255).astype(np.uint8))); o.save(f'assets/{name}.png')
print(img.size)
