# Vídeo identidade Zohar (reels 1080x1920)

Ritmo inspirado no vídeo de referência (Miria): cortes calmos, acelera até piscar, desacelera; duas vezes; fecha no logo.
O pisca percorre imagens diferentes (sem repetir em sequência) e o logo na luz aparece só na abertura e no fecho.
Cada imagem entra com zoom e assenta; cortes de 10+ quadros têm fusão de 4 quadros.
~13 s, 30 fps, **sem áudio** (música a escolher depois).

- `quadros.html`: quadros gráficos (tipografia + paleta, ícones, logo na luz, monograma, O com estrela, estrela cruzando o nome, fecho).
  O logo é refeito em Bodoni Moda com a estrela de 4 pontas.
- `assets/fotos/`: mockups (boné, chaveiro, ecobag, pasta, skate, capinha, vinil), cortados em 1080x1920.
- Gerar: `node render-quadros.mjs && python3 montar.py` → `out/zohar-identidade.mp4`.
- A ordem das imagens e o tempo de cada corte estão no topo de `montar.py` (`ABERTURA`, `RODIZIO`, `RITMO`, `FECHO`).
