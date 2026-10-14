# Padrão de guia aluGO 2026 — montagem

Os guias no padrão novo (10 tópicos, tema da unidade, "Sua estadia em 3 passos") são **montados** por `montar.py`
a partir do HTML publicado antes da conversão (`base_ref` de cada unidade). Só a camada visual é trocada;
o `<script id="dados">` (TELAS/TXT/SINONIMOS) fica intacto, porque a área do hóspede e a IA do atendimento leem dele.

    python3 _padrao/montar.py 501T 1806A ...      # remonta as unidades
    python3 _padrao/testeg.py guia-xxx.html       # teste rápido em 390px (Playwright)

- `novo_body.html`, `novo_css.css`, `novo_ui.js`, `novo_render.js`, `tema.css` — camada visual comum a todos
- `temas/*.webp` — fundos gerados no Gemini (um por unidade/prédio); `icones/` — os 10 ícones (Gemini)
- Para mudar conteúdo de um apê, edite o bloco de dados do guia **e** ajuste o `base_ref` (ou use `troca_dados`).
- Unidade nova no padrão: adicione em `UNIDADES` (tema, títulos, horários, `mapa` se as telas forem diferentes).
