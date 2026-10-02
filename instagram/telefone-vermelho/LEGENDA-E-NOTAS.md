# Telefone tocando 2 (loop 4 s, 1080×1350, fundo branco)

Referência: `referencia.jpg` (telefone de disco vermelho, manga listrada, fundo azul-piscina).
`recortar.py` recorta (rembg + cor), troca o vermelho pelo verde #00B490, deixa a manga preta e separa o corpo do telefone
(`assets/base.png`, que pula quando toca) da mão com o fone (`assets/mao-fone.png`).

- Copy: "Chamada de:" / "sua marca no *topo da Amazon.*" (destaque #00B490).
- O telefone toca duas vezes (trim-trim), pula e treme com traços verdes dos lados. Raios verdes suaves no fundo.
- `out/telefone-tocando-2.mp4` para postar (loop 3x, 12 s), `.gif` 720px, `-quadro.png` estático.
- Gerar de novo: `node render.mjs` (Playwright + ffmpeg).
