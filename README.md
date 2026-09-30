# Guias aluGO

Este é o repositório principal com os guias interativos e o check-in online de todas as unidades da aluGO.

- **Endereço público:** https://pedpaz.github.io/Guias-alugo/
- **Quem usa:** a área do hóspede do loftcare-os (a Ajuda lê o texto dos guias) e as mensagens automáticas da Stays, do Airbnb e do Booking.

## Como está organizado

| Arquivo | O que é |
|---|---|
| `guia-<prédio>-<unidade>.html` | Guia da unidade. Um arquivo só, com as fotos embutidas. |
| `termo.html` | **Formulário único** de check-in. Abre como `termo.html?u=CÓDIGO`. |
| `termo-config.js` | Tabela com o que muda de uma unidade para outra: prédio, endereço, capacidade, horários, acesso, cláusulas e link do guia. |
| `termo-<prédio>-<unidade>.html` | Atalho que redireciona para `termo.html?u=CÓDIGO`. Mantém válidos os links antigos das mensagens automáticas. |
| `assets/` | Arquivos compartilhados (logo aluGO, animação da fechadura) e uma subpasta por unidade quando ela tem mídia própria (`assets/privilege-i07/`, `assets/ykutiba/`). |

O código da unidade é o mesmo da Stays e do loftcare-os (ex.: `TR-803S`, `IP-I07`). O termo grava no loftcare-os (`/api/public/checkin`) com esse código.

## Como adicionar uma unidade nova

1. Suba o guia como `guia-<prédio>-<unidade>.html`. Se ele tiver vídeo ou ícones próprios, coloque em `assets/<unidade>/`.
2. No `termo-config.js`, dentro de `window.UNIDADES`, crie a entrada com o código. Copie uma unidade parecida e ajuste.
   - Se o acesso ou as áreas comuns forem novos, crie um item em `ACESSO` / `AREAS` e reaproveite nas outras unidades do mesmo prédio.
3. Crie o atalho `termo-<prédio>-<unidade>.html`: copie um existente e troque o código.
4. Confira se a unidade existe no loftcare-os com **o mesmo código**. Sem isso, o termo não é registrado.
5. Teste: abra `termo.html?u=CÓDIGO`, envie um termo de teste e confirme que chegou no sistema.

## Unidades fora de Goiânia

| Código | Unidade | Guia | Termo |
|---|---|---|---|
| `IP-I07` | Imbassaí Privilege · Village I07 (Imbassaí/BA) | `guia-privilege-I07.html` | `termo.html?u=IP-I07` |
| `YK-Q03` | Residencial Ykutiba · Casa Q003 (Imbassaí/BA) | `guia-ykutiba-Q003.html` | `termo-ykutiba-Q003.html` (formulário próprio, que gera o PDF exigido pela portaria do Ykutiba) |
| `ADL-*` | Flat Aldeia do Lago (Caldas Novas/GO) | `guia-aldeia-*.html` | `termo.html?u=ADL-…` |

## Domínio (futuro)

O domínio da aluGO é **alugo.net.br**. O plano é:

- `alugo.net.br` apontar para o loftcare-os (Vercel), onde fica a área do hóspede.
- Os guias passarem a abrir de dentro desse domínio.

Antes de mudar o endereço dos guias, é preciso liberar o novo domínio no CORS de `/api/public/checkin` no loftcare-os. Hoje só `https://pedpaz.github.io` é aceito.

Também será preciso trocar a constante `BASE` no `termo.html`, que hoje é `https://pedpaz.github.io/Guias-alugo/`.
