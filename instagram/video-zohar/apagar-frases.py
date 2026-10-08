# Apaga as frases pequenas impressas nos mockups (tagline, "EST. 2024 · SÃO PAULO" etc.).
# Lê assets/fotos-com-texto/*.jpg e grava em assets/fotos/*.jpg. Uso: python3 apagar-frases.py
import cv2, numpy as np
K = 1080 / 941  # caixas medidas nas fotos originais (941x1672)
CAIXAS = {
    'pasta':   [(235, 925, 630, 957), (298, 968, 562, 997), (118, 578, 238, 662)],
    'capinha': [(288, 826, 668, 857), (346, 871, 606, 902)],
    'vinil':   [(92, 1102, 298, 1188), (638, 1126, 850, 1188)],
}
for nome, caixas in CAIXAS.items():
    im = cv2.imread(f'assets/fotos-com-texto/{nome}.jpg')
    lum = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(int)
    mask = np.zeros(lum.shape, np.uint8)
    for x0, y0, x1, y1 in caixas:
        x0, y0, x1, y1 = (round(v * K) for v in (x0, y0, x1, y1))
        reg = lum[y0:y1, x0:x1]
        mask[y0:y1, x0:x1] = (reg > np.median(reg) + 25) * 255  # letras e fios claros sobre o fundo
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
    out = cv2.inpaint(im, mask, 6, cv2.INPAINT_TELEA).astype(float)
    # devolve o granulado do papel/tecido onde a letra foi apagada (o preenchimento sai liso)
    fundo = im.astype(float); ruido = fundo - cv2.GaussianBlur(fundo, (0, 0), 3)
    sigma = ruido[mask == 0].std()
    m = cv2.GaussianBlur(mask, (0, 0), 2)[..., None] / 255
    out = np.clip(out + m * np.random.default_rng(1).normal(0, sigma, out.shape), 0, 255).astype(np.uint8)
    cv2.imwrite(f'assets/fotos/{nome}.jpg', out, [cv2.IMWRITE_JPEG_QUALITY, 93])
