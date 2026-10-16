# Reel "Precisa de…? A Way Brand faz para você. / Deixa com a Way Brand." (1080×1920, 28,8 s, loop)

Cópia da referência (pêndulo com a tag da marca que funciona como cortina): à esquerda do fio aparece a pergunta, à direita a resposta.

- Fundo: `#18614D` com brilho radial no centro.
- Pergunta em verde-escuro `#0A2E24`, resposta em branco.
- Logo e símbolo ❋ em verde-menta `#9BEFCB`.

Para trocar as frases, edite `PERGUNTAS` e `RESPOSTAS` no `index.html` e rode `node render.mjs`. Cada pergunta dura uma ida e volta do pêndulo (2,4 s). Com 12 perguntas, o vídeo tem 28,8 s. Se você mudar a quantidade de perguntas, a duração muda junto. O texto diminui sozinho quando a linha fica comprida.

## Frases usadas no vídeo

| # | Pergunta |
|---|---|
| 1 | PRECISA DE / A+ PREMIUM? |
| 2 | PRECISA DE / UMA MARCA? |
| 3 | PRECISA DE / IMAGENS? |
| 4 | PRECISA DE / AMAZON ADS? |
| 5 | PRECISA DE / UMA VITRINE? |
| 6 | PRECISA / VENDER MAIS? |
| 7 | PRECISA DE / UM VÍDEO? |
| 8 | PRECISA DE / ESTRATÉGIA? |
| 9 | PRECISA DE / MAIS CLIQUES? |
| 10 | PRECISA / APARECER? |
| 11 | PRECISA DE / CONTEÚDO? |
| 12 | PRECISA / CRESCER? |

Respostas, alternando a cada pergunta (a 1ª pergunta recebe a 1ª resposta):

1. **A WAY BRAND / FAZ PARA VOCÊ.**
2. **DEIXA COM / A WAY BRAND.**

A resposta troca quando o fio está na ponta direita, com ela escondida.

## Mais opções de pergunta

Até umas 12 letras na segunda linha, o texto fica no tamanho cheio.

**Serviços**
- PRECISA DE / FOTOS NOVAS?
- PRECISA DE / UM LOGO?
- PRECISA DE / UM BRANDING?
- PRECISA DE / EMBALAGEM?
- PRECISA DE / UMA LOJA?
- PRECISA DE / UM CATÁLOGO?
- PRECISA DE / UM REGISTRO? (registro de marca)
- PRECISA DE / INFOGRÁFICOS?
- PRECISA DE / UM ANÚNCIO?
- PRECISA DE / UMA GESTÃO?

**Resultado**
- PRECISA / VENDER MAIS?
- PRECISA DE / MAIS VENDAS?
- PRECISA / CONVERTER?
- PRECISA / SE DESTACAR?
- PRECISA / SER VISTO?
- PRECISA / ESCALAR?
- PRECISA DE / MAIS MARGEM?
- PRECISA / SAIR DO PREÇO? (marca × genérico)
- PRECISA / VIRAR MARCA?
- PRECISA DE / UM EMPURRÃO?

**Amazon**
- QUER VENDER / NA AMAZON?
- PRECISA DO / BUY BOX?
- QUER O / A+ PREMIUM?
- QUER UMA / BRAND STORE?
- QUER SAIR DA / PÁGINA 5?

## Opções de resposta

- **A WAY BRAND / FAZ PARA VOCÊ.** (usada)
- **DEIXA COM / A WAY BRAND.** (usada)
- DEIXA COM / A GENTE.
- A GENTE / RESOLVE.
- CONTA / COM A GENTE.
- A GENTE / FAZ.
- TAMO / JUNTO.
- É COM / A GENTE.
- CHAMA A / WAYBRAND.
- A WAYBRAND / RESOLVE.

## Rodapé

O rodapé "DESIGN · AMAZON · CRESCIMENTO" saiu. No `index.html` há 4 variantes, escolhidas em `RODAPE` (ou com `?rodape=x` na URL):

- `cta`: "Comente **MARCA** que a gente te chama." + @waybrand.co
- `botao`: botão amarelo estilo Amazon "Quero vender mais na Amazon →" + @waybrand.co
- `letreiro` (usada): faixa rolando com os serviços (A+ PREMIUM ❋ AMAZON ADS ❋ …) + @waybrand.co
- `frase`: "Sua marca **pronta pra vender** na Amazon." + @waybrand.co

## Som

Batida trap a 100 BPM, sintetizada do zero em `som/gerar_som.py` (versão `trap`). Um compasso dura uma ida e volta do pêndulo:

- bumbo e baixo 808 quando o pêndulo chega nas pontas;
- caixa quando o fio passa pelo meio;
- chimbal feito com o tique de um relógio de pêndulo, em colcheias;
- rufo de chimbal a cada 2 compassos.

O gerador também tem as versões `relogio` e `metal` (só som de pêndulo) e `house` (outra batida). Para usar outra: `python3 som/gerar_som.py house`.

Volume no padrão do Instagram (-14 LUFS). Para mexer no som: edite `som/gerar_som.py`, rode `python3 som/gerar_som.py` e depois `node render.mjs --som` (só troca o áudio, sem renderizar os quadros de novo).

## Legenda sugerida

> Precisa de A+ Premium? Imagem que vende? Amazon Ads? Uma vitrine que faz o cliente ficar?
> A Way Brand faz para você.
>
> Manda "MARCA" aqui nos comentários que a gente te mostra por onde começar.
