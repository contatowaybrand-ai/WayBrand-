# C04 · A+ Premium, carrossel de 6 slides (1080×1350)

Segue o padrão do feed @waybrand.co, com base na análise post a post de 24/09/2026 (ver `ANALISE-FEED.md`).
Modelo principal: o carrossel "Case 18% → 30%" (11/09/2026).

| Slide | Fundo | Conteúdo |
|---|---|---|
| 01 Capa | escuro + cena de luz | "O A+ Premium não é mais só para Apple, JBL e Red Bull." + faixa verde "Marcas registradas podem vender **até 33% mais.**" |
| 02 O que mudou | verde sólido #00A884 | "O Premium era *clube fechado.*" Antes (✕ só gigantes) × Agora (✓ marcas registradas) |
| 03 A diferença | branco | "Mesmo anúncio. *Outra página.*" Antes/depois com divisor: básico × Premium |
| 04 O que libera | escuro #18241E | "5 recursos que *vendem por você.*" Banner, vídeo, interativo, perguntas e respostas, comparativo |
| 05 Por que vende mais | claro | "O cliente fica. *E a Amazon percebe.*" Notificações "Nova venda na Amazon" |
| 06 Fechamento | claro | ~~"A+ Premium é coisa de marca grande."~~ → "É gratuito pra marca registrada. *E quase ninguém usa.*" + caminho no Seller Central + barra de comentário PREMIUM |

## Legenda

Durante anos, o A+ Premium foi coisa de Apple, JBL e Red Bull.

Hoje ele está disponível pra quem tem marca registrada na Amazon. E quase ninguém no Brasil está usando.

Banner em tela cheia. Vídeo na descrição. Imagem interativa. Perguntas e respostas. Comparativo da sua linha.

O cliente fica mais tempo no seu anúncio. E a Amazon percebe.

É gratuito. A diferença é quem começa primeiro.

Comente PREMIUM e a gente avalia se a sua marca já pode usar.

## Conferir antes de postar

1. **"Até 33%" não tem fonte da Amazon.** A Amazon divulga até 8% (A+ básico) e até 20% (A+ Premium). O 33% vem de uma pesquisa sobre consistência de marca entre canais. Versão segura: "até 20% mais". Pra trocar, é só mudar `.l2` no `index.html` e rodar `node render.mjs`.
2. Confirmar com o André os requisitos atuais do Premium no Brasil.
3. Capa: a cena foi feita em código. Há dois renders 3D gerados no Magnific (corda de veludo aberta + notebook com página verde). Para usar um deles, salve como `assets/capa.png`, descomente a linha `<img class="bgimg">` do slide 1 e renderize de novo.
4. Fonte do render: Inter (Black/ExtraBold + itálico), a grotesca mais próxima do que o feed usa hoje.
