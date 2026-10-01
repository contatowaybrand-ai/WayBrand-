# Portfolio 2026, post estático (1080×1350)

A referência é a capa "Portfolio" com pastas de arquivo empilhadas. Aqui a composição está espelhada: as abas descem da esquerda para a direita, e o título fica alinhado à direita.

Cores da Way:
- Fundo `#0C1818`.
- Pastas alternando cinza-claro `#E6E8E6` e verde `#00B490`.
- A última aba (2026) tem a cor do fundo.
- Título em branco e símbolo oficial em verde.

Pastas: Pinati, Bevi Pro, Eleve Life, Premium Lindoia e 2026.

## Opções de fonte (`index.html#a` … `#d`)
| Versão | Título "Portfolio" | Abas |
|---|---|---|
| a | Instrument Serif (Port reto + *folio* itálico) | Space Mono Bold |
| b | Syne ExtraBold + Medium | Syne Bold |
| c | Bricolage Grotesque Bold + Light | Bricolage Bold |
| d | Unbounded Medium + ExtraLight | Unbounded SemiBold |

Para renderizar as 4 versões: `node render.mjs`, que salva em `png/portfolio-2026-<letra>-<fonte>.png`.

**Escolhida: B (Syne).** O texto "Compilation Vol. 1" foi removido. O arquivo final é `png/portfolio-2026-final.png`.

## Versão animada

`png/portfolio-2026-animado.mp4` tem 8 s (2 voltas) e é a versão para postar no Instagram. `png/portfolio-2026-animado.gif` tem 1 volta, em 720 px.

As 4 pastas das marcas sobem uma de cada vez e voltam, como se alguém folheasse o arquivo. A volta dura 4 s e emenda sem corte.

Para gerar: `FFMPEG=/caminho/ffmpeg node render-video.mjs`. O ffmpeg pode vir de `pip install imageio-ffmpeg`.
