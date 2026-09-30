# Waybrand services, post estático (1080×1350)

A referência é o post "Our services" com fundo verde quadriculado, título gigante e serviços em pílulas.

Adaptação para a paleta da Way:
- Fundo escuro `#0C1818` com a grade em verde `#00B490`, bem fraca.
- Título em creme `#F0EDE4`.
- Pílulas, CTA e rodapé em verde. As pílulas alternam entre cheias e só com contorno.
- Fonte Inter Black e ExtraBold.

Para renderizar: `node render.mjs`. O título se ajusta sozinho à largura, e as pílulas ficam em `.pills` no `index.html`.

## Versão clara

`png/waybrand-services-claro.png`, gerada a partir de `index.html#claro`. O fundo é branco, a grade continua verde e um pouco mais visível, e os textos e o título ficam no escuro `#0C1818`. O `render.mjs` gera as duas versões.

## Carrossel (capa clara + 6 slides + contato)

Os slides ficam em `slides.html` e são gerados com `node render-slides.mjs`, que salva em `png/slide-0N-*.png`. A capa é `png/slide-01-capa.png`, cópia da versão clara.

Cada slide de serviço usa a cor do botão correspondente na capa clara:
- Botão cheio vira slide verde com texto branco: Identidade visual, Store oficial e Brand registry.
- Botão de contorno vira slide branco com detalhes verdes e texto escuro: Conteúdo A+, Ads e escala e Suporte.

Estrutura dos slides de serviço:
- Só o contador "0N / 06" no topo, sem logo, site, @ ou seta.
- Número gigante vazado no fundo.
- O botão da capa ampliado, com um cursor "clicando" nele.
- Frase de efeito, texto curto e chips com o que está incluído.
- O bloco fica centralizado na altura do slide.

O slide 08 é o de contato, em verde:
- Logo, símbolo da Way grande e "Quer saber mais?".
- Chamada para DM e comentários.
- Site e @ no rodapé.

Para mudar os textos, edite o array `S` e o bloco `.fim` em `slides.html`.
