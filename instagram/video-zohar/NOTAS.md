# Vídeo identidade Zohar (reels 1080x1920)

Ritmo copiado do vídeo de referência (Miria): cortes calmos, pisca-pisca, desacelera; duas vezes; fecha parado no logo.
17 s, 30 fps, **sem áudio** (música a escolher depois).

- `quadros.html`: quadros gráficos (tipografia + paleta, ícones, logo na luz, monograma, O com estrela, estrela cruzando o nome, fecho).
  O logo é refeito em Bodoni Moda com a estrela de 4 pontas.
- `assets/fotos/`: mockups (boné, chaveiro, ecobag, pasta, skate, capinha, vinil), cortados em 1080x1920.
- Gerar: `node render-quadros.mjs && python3 montar.py` → `out/zohar-identidade.mp4`.
- A ordem das imagens e o tempo de cada corte estão no topo de `montar.py` (`NORMAIS`, `PISCA`, `CORTES`, `FECHO`).
