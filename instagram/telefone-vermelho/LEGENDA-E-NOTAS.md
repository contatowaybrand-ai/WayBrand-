# Telefone tocando 2 (loop 4 s, 1080×1350, fundo branco)

Referência: `referencia.jpg` (telefone de disco vermelho, manga listrada, fundo azul-piscina).
`recortar.py` recorta (rembg + cor), troca o vermelho pelo verde #00B490, deixa a manga preta e separa o corpo do telefone
(`assets/base.png`, que pula quando toca) da mão com o fone (`assets/mao-fone.png`).

- Cena espelhada (braço entra pela direita); o disco é desvirado à parte para os números ficarem legíveis.
- Copy grande no topo: "Chamada de:" (Inter Light) / "sua marca no" (Bricolage Grotesque 800) / "*topo da Amazon.*" (Anton, #00B490). Fontes em `assets/fonts` (Google Fonts, OFL).
- O telefone toca duas vezes (trim-trim), pula e treme com traços verdes dos lados. Símbolo WayBrand (8 raios) girando bem claro no fundo: gira 45° por loop, então o fim encaixa no começo sem salto.
- `out/telefone-tocando-2.mp4` para postar (loop 3x, 12 s), `.gif` 720px, `-quadro.png` estático.
- Gerar de novo: `node render.mjs` (Playwright + ffmpeg).

- **Som:** os MP4 têm toque de telefone antigo sincronizado com os dois toques da animação (`../som-telefone/gerar.py` → `toque-12s.wav`). O GIF não tem som.
