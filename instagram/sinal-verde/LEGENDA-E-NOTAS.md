# Carrossel "Sinal verde pra sua marca"

## Slides
1. Capa: SINAL VERDE PRA SUA MARCA · rótulos 01 Branding / 02 Posicionamento / 03 Anúncios / 04 Resultado · AGORA É SUA VEZ. (versão com o bonequinho piscando no GIF/MP4)
2. Se você já tem a marca **registrada**,
3. produto **validado**,
4. por que sua marca ainda não está **bem posicionada** dentro da Amazon?

Slides 2 a 4 usam a mesma foto do semáforo, inteira, com 22% de opacidade.

## Fonte
RF Dewi Extended Light + Regular + Semibold (Russian Fonts, paga). O arquivo **não vai pro git** porque o repositório é público
(`.gitignore` ignora `assets/fonts/RFDewi*`). Pra renderizar de novo, coloque `RFDewiExtended-Light.ttf`, `-Regular.ttf` e `-Semibold.ttf`
em `assets/fonts` e rode `node render.mjs`. Sem ele, a arte sai com a Onest.
Texto em Light; palavras em destaque em Semibold.

# Texto da capa

## Texto na arte
- Título: **SINAL VERDE / PRA SUA MARCA** (fino, com "MARCA" em negrito)
- Rótulos soltos: ▪ BRANDING · ▪ POSICIONAMENTO · ▪ ANÚNCIOS · ▪ RESULTADO
- Fecho: **AGORA É / SUA VEZ.** (ponto em verde #00B490)

Outras opções para o fecho: "PODE / ATRAVESSAR." · "LIBERADO / PRA CRESCER." · "SUA MARCA / PODE PASSAR."

## Legenda sugerida
Tem marca parada no vermelho há meses na Amazon.
Esperando o momento certo, o orçamento certo, a coragem certa.

O sinal abriu.

Branding, posicionamento e anúncios trabalhando juntos pra sua marca atravessar de vez: sair do meio da multidão e chegar no clique, na venda, no resultado.

A vez agora é sua.
Chama a gente no direct.

## Notas
- Foto: semáforo de referência, esfumada pra esquerda e pra cima num degradê que imita o céu, pra abrir espaço pro título.
- Versão animada: o bonequinho pisca como na rua (0,5 s aceso / 0,5 s apagado, em loop).
  - `png/sinal-verde-pisca.gif` (GIF em loop) e `png/sinal-verde-pisca.mp4` (6 s, pro Instagram, que não aceita GIF).
  - A foto com o bonequinho apagado (`assets/semaforo-apagado.jpg`) sai de `python3 apagar-bonequinho.py`.
- Gerar tudo: `node render.mjs` (slides 1080x1350, quadro apagado, GIF e MP4).
