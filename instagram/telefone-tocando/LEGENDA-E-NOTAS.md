# Telefone tocando (loop 4 s, 1080×1350)

Referência: `referencia.jpg` (mão segurando fone no fundo amarelo). Recorte em `assets/mao-telefone.png` gerado por `recortar.py`
(rembg + reforço por cor; reflexos amarelos do fone viram verde #00B490).

- Fundo verde sólido #00A884 com raios #6CC6B4 girando; fone toca duas vezes (trim-trim), traços de toque piscam, card "WayBrand · chamada recebida" com botão verde pulsando.
- `out/telefone-tocando-{a,b,c}.mp4` para postar (Instagram não aceita GIF; o MP4 tem o loop repetido 3x, 12 s). `.gif` 720px para prévia.
- Gerar de novo: `node render.mjs [a|b|c]` (precisa do Playwright e do ffmpeg). Textos em `TEXTOS` no `index.html`.

| Versão | Apoio | Título |
|---|---|---|
| a | Alô, é da **WayBrand?** | Minha marca quer *escalar.* |
| b | Atende, é a **sua marca** ligando. | Ela quer *jogar grande.* |
| c | Do outro lado da linha: | a marca que a gente vai *construir junto.* |
