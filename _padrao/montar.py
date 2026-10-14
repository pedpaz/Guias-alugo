"""Monta um guia no padrão aluGO 2026 (10 tópicos + tema da unidade).
uso: python3 montar.py <chave>   (chaves em UNIDADES)
Parte SEMPRE do HTML publicado antes da conversão (base_ref) e troca só a
camada visual: fonte, CSS, corpo e o script RENDER. O <script id="dados">
(TELAS/TXT/SINONIMOS) fica intacto — a área do hóspede e a IA leem dele."""
import base64, re, sys, json, subprocess
import os
P = os.path.dirname(os.path.abspath(__file__))      # _padrao/
R = os.path.dirname(P)                               # raiz do repositório Guias-alugo

def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode()

T_ = f'{P}/temas'
def tema(nome, tex, theme, cor, vars_, fechadura=False, autoSub=True):
    return dict(nome=nome, tex=tex, theme=theme, cor=cor, vars=vars_, fechadura=fechadura, autoSub=autoSub)
def V(bg, tx, tx2, luzA, luzB, veu, barra, assin, assin2, assinBg):
    return {'--tema-bg':bg,'--tema-tx':tx,'--tema-tx2':tx2,'--tema-luz-a':luzA,'--tema-luz-b':luzB,'--tema-veu':veu,
            '--tema-barra':barra,'--assin':assin,'--assin2':assin2,'--assin-bg':assinBg}

TEMAS = {
 'veludo': tema('Veludo vivo', f'{T_}/veludo.webp', '#2B050B', '#B8121F',
    V('#2B050B','#FFF4F5','rgba(255,228,232,.72)','rgba(255,120,135,.10)','rgba(255,200,206,.20)','18,0,4','rgba(34,4,10,.88)','#B8121F','#E0303E','#FFF0F1'),
    fechadura=True, autoSub=False),
 'seda': tema('Seda petróleo', f'{T_}/barcelona.webp', '#0A2328', '#0E6B73',
    V('#0A2328','#F1FAFA','rgba(214,240,240,.74)','rgba(120,200,205,.08)','rgba(235,205,140,.16)','2,14,16','rgba(4,22,26,.9)','#0E6B73','#1A8C95','#E8F5F5')),
 'agua': tema('Água ao entardecer', f'{T_}/frbueno.webp', '#0D1B2A', '#C26A1E',
    V('#0D1B2A','#F2F6FB','rgba(214,226,240,.74)','rgba(255,170,90,.07)','rgba(255,205,150,.15)','4,10,18','rgba(8,18,30,.9)','#C26A1E','#E08A3A','#FFF3E6')),
 'carvalho': tema('Carvalho', f'{T_}/tai.webp', '#1C140D', '#A8692A',
    V('#1C140D','#FBF5EE','rgba(240,226,210,.74)','rgba(255,210,150,.07)','rgba(255,230,190,.15)','12,8,4','rgba(24,17,10,.9)','#A8692A','#C98A45','#FBF1E4')),
 'marmore': tema('Mármore grafite', f'{T_}/dna.webp', '#121314', '#E0761A',
    V('#121314','#F5F5F4','rgba(228,228,226,.72)','rgba(255,255,255,.05)','rgba(255,255,255,.12)','0,0,0','rgba(14,14,15,.9)','#D2691A','#F08C32','#FFF2E6'),
    fechadura=True),
 'noite': tema('Cidade à noite', f'{T_}/dna2003.webp', '#0B1020', '#C8743A',
    V('#0B1020','#F1F4FB','rgba(214,222,240,.74)','rgba(255,170,110,.06)','rgba(200,220,255,.13)','3,5,12','rgba(8,12,24,.9)','#B8632A','#D9833F','#FDF0E6'),
    fechadura=True),
 'travertino': tema('Travertino', f'{T_}/marista.webp', '#1A1410', '#B0243F',
    V('#1A1410','#FAF4EE','rgba(236,222,208,.74)','rgba(255,200,150,.06)','rgba(255,225,190,.14)','10,6,3','rgba(22,16,12,.9)','#B0243F','#D0385A','#FCEBEF')),
}

def ui_sidney(ala):
    return {
      'pt': {'heroTit': f'501 · Ala {ala}', 'heroSub': 'Metropolitan Sidney · Jardim Goiás, Goiânia',
             'topicos': {'entrar': {'s': f'5º andar, Ala {ala} · senha da porta'}}},
      'en': {'heroTit': f'501 · Wing {ala}', 'heroSub': 'Metropolitan Sidney · Jardim Goiás, Goiânia',
             'topicos': {'entrar': {'s': f'5th floor, wing {ala} · door code'}}},
      'es': {'heroTit': f'501 · Ala {ala}', 'heroSub': 'Metropolitan Sidney · Jardim Goiás, Goiânia',
             'topicos': {'entrar': {'s': f'Piso 5, ala {ala} · clave de la puerta'}}},
    }

def ui_unidade(tit, sub, ent, sai, vaga_sub=None, extra=None):
    """tit/sub: str ou dict por idioma; ent/sai: horas inteiras."""
    def L(x, l): return x[l] if isinstance(x, dict) else x
    am = lambda h: f'{h} am' if h < 12 else ('12 pm' if h == 12 else f'{h-12} pm')
    d = {
      'pt': {'heroTit': L(tit,'pt'), 'heroSub': L(sub,'pt'), 'hEnt': f'das {ent}h', 'hSai': f'até as {sai}h',
             'p3s': f'Até {sai}h · avise sua saída com um toque'},
      'en': {'heroTit': L(tit,'en'), 'heroSub': L(sub,'en'), 'hEnt': am(ent), 'hSai': f'by {am(sai)}',
             'p3s': f'By {am(sai)} · let us know with one tap'},
      'es': {'heroTit': L(tit,'es'), 'heroSub': L(sub,'es'), 'hEnt': f'{ent} h', 'hSai': f'hasta las {sai} h',
             'p3s': f'Hasta las {sai} h · avisa tu salida con un toque'},
    }
    if vaga_sub:
        for l in d: d[l]['vagaSub'] = L(vaga_sub, l)
    for l, kv in (extra or {}).items():
        for k, v in kv.items():
            if isinstance(v, dict) and isinstance(d[l].get(k), dict): d[l][k].update(v)
            else: d[l][k] = v
    return d

FACIAL = {'pt': 'Portão por reconhecimento facial', 'en': 'Gate opens by face ID', 'es': 'Portón por reconocimiento facial'}
COPA = {'pt': {'topicos': {'ape': {'t': 'A suíte', 's': 'Cama, Wi-Fi, TV, banheiro e copa'}, 'entrar': {'t': 'Entrar na suíte'}}},
        'en': {'topicos': {'ape': {'t': 'The suite', 's': 'Bed, Wi-Fi, TV, bathroom and pantry'}, 'entrar': {'t': 'Getting into the suite'}}},
        'es': {'topicos': {'ape': {'t': 'La suite', 's': 'Cama, wifi, TV, baño y office'}, 'entrar': {'t': 'Entrar a la suite'}}}}

# QS Marista: a saída é às 11h (Pedro, out/2026) — os guias diziam 12h
SAIDA_11H = [('12h', '11h'), ('12 pm', '11 am')]

UNIDADES = {
  '501T': dict(arq='guia-sidney-501T.html', base_ref='ec0964c^', tema='veludo', ui=ui_sidney('T')),
  '501O': dict(arq='guia-sidney-501O.html', base_ref='e9bacd1', tema='veludo', ui=ui_sidney('O')),
  '1806A': dict(arq='guia-barcelona-1806A.html', base_ref='978a1cb', tema='seda',
     ui=ui_unidade('1806 A', 'Metropolitan Barcelona · Jardim Goiás, Goiânia', 14, 11,
        vaga_sub={'pt':'Subsolo 2 · cartão do portão no apê','en':'Basement 2 · gate card in the flat','es':'Subsuelo 2 · tarjeta del portón en el depto'},
        extra={'pt':{'vagaVal':'491'},'en':{'vagaVal':'491'},'es':{'vagaVal':'491'}})),
  '1003A': dict(arq='guia-fr-bueno-1003A.html', base_ref='978a1cb', tema='agua',
     ui=ui_unidade('Studio 1003A', 'FR Bueno Municipal · Setor Bueno, Goiânia', 15, 12, vaga_sub=FACIAL,
        extra={'pt':{'vagaVal':'093'},'en':{'vagaVal':'093'},'es':{'vagaVal':'093'}})),
  '1701': dict(arq='guia-marista-1701.html', base_ref='978a1cb', tema='travertino',
     troca_dados=SAIDA_11H, ui=ui_unidade('Suíte 1701', 'QS Marista · Setor Marista, Goiânia', 15, 11, extra=COPA)),
  '402': dict(arq='guia-marista-402.html', base_ref='978a1cb', tema='travertino',
     troca_dados=SAIDA_11H, ui=ui_unidade('Suíte 402', 'QS Marista · Setor Marista, Goiânia', 15, 11, extra=COPA)),
  '803S': dict(arq='guia-tai-803S.html', base_ref='978a1cb', tema='carvalho',
     ui=ui_unidade('Flat 803S', 'Tai Residências · Setor Bueno, Goiânia', 15, 12, vaga_sub=FACIAL)),
  '407B': dict(arq='guia-dna-407B.html', base_ref='978a1cb', tema='marmore',
     ui=ui_unidade({'pt':'Flat 407 · Torre B','en':'Flat 407 · Tower B','es':'Flat 407 · Torre B'}, 'DNA SmartStyle · Setor Bueno, Goiânia', 15, 12,
        vaga_sub={'pt':'Subsolo S2 · controle no apê','en':'Basement S2 · remote in the flat','es':'Subsuelo S2 · control en el depto'})),
  '2003B': dict(arq='guia-dna-2003B.html', base_ref='978a1cb', tema='noite', hero='sala-estar-jantar',
     mapa={'entrar': ['ape'], 'ape': ['duplex', 'cozinha']},
     ui=ui_unidade({'pt':'Duplex 2003','en':'Duplex 2003','es':'Dúplex 2003'}, {'pt':'Torre B · DNA SmartStyle · Setor Bueno, Goiânia','en':'Tower B · DNA SmartStyle · Setor Bueno, Goiânia','es':'Torre B · DNA SmartStyle · Setor Bueno, Goiânia'}, 15, 12,
        vaga_sub={'pt':'2º pavimento da garagem','en':'Garage level 2','es':'2º nivel del garaje'})),
}

def montar(chave):
    U = UNIDADES[chave]; T = TEMAS[U['tema']]
    G = f"{R}/{U['arq']}"
    s = subprocess.run(['git', '-C', R, 'show', f"{U['base_ref']}:{U['arq']}"], capture_output=True, check=True).stdout.decode('utf-8')
    orig = len(s)
    ids = ['checkin','chegar','entrar','energia','ape','predio','regras','arredores','checkout','ajuda']
    ics = {(k if k != 'predio' else 'condominio'): b64(f'{P}/icones/ic-{k}.webp', 'image/webp') for k in ids}
    raiz = ':root{' + ';'.join(f'{k}:{v}' for k, v in T['vars'].items()) + '}\n'
    css = open(f'{P}/novo_css.css').read() + raiz + open(f'{P}/tema.css').read()
    body = open(f'{P}/novo_body.html').read()
    ui = open(f'{P}/novo_ui.js').read()
    render = open(f'{P}/novo_render.js').read()
    tema_js = {'nome': T['nome'], 'cor': T['cor'], 'fechadura': T['fechadura'], 'autoSub': T['autoSub']}
    if U.get('mapa'): tema_js['mapa'] = U['mapa']
    if U.get('hero'): tema_js['hero'] = U['hero']
    # correções de conteúdo pedidas pelo Pedro (só dentro do bloco de dados)
    if U.get('troca_dados'):
        a = s.index('<script id="dados"'); b = s.index('</script>', a); d = s[a:b]
        for velho, novo in U['troca_dados']:
            assert velho in d, velho
            d = d.replace(velho, novo)
        s = s[:a] + d + s[b:]
    # nunca o alert nativo (trava o webview): vistoria vazia vira aviso
    s = s.replace('alert(TXT[L].vistVazio)', 'aviso(TXT[L].vistVazio)')

    s, n = re.subn(r'<link href="https://fonts\.googleapis\.com/css2\?family=Fraunces[^"]*" rel="stylesheet">',
      '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@500;600;700&display=swap" rel="stylesheet">', s, 1)
    assert n == 1, 'fonte'
    s, n = re.subn(r'<meta name="theme-color" content="[^"]*">', f'<meta name="theme-color" content="{T["theme"]}">', s, 1)
    assert n == 1, 'theme-color'
    if T['fechadura'] and 'fechadura-anim.js' not in s:
        s = s.replace('</head>', '<script src="assets/fechadura-anim.js" defer></script>\n</head>', 1)
    a = s.index('<style>'); b = s.index('</style>', a)
    s = s[:a] + '<style>\n' + css + '\n' + s[b:]
    a = s.find('<div id="aviso"')
    if a < 0: a = s.index('<body>') + len('<body>\n')
    b = s.index('<script>', a)
    s = s[:a] + body + s[b:]
    a = s.index('<script>\n/* ================= RENDER ================= */'); b = s.index('</script>', a)
    novo = ('<script>\n/* ícones dos 10 tópicos (Gemini) e tema da unidade (Gemini) */\nvar ICS = ' + json.dumps(ics) +
            ';\nvar TEMA_TEX = "' + b64(T['tex'], 'image/webp') + '";\nvar TEMA = ' + json.dumps(tema_js) +
            ';\nvar UI_UNIDADE = ' + json.dumps(U['ui'], ensure_ascii=False) + ';\n' + ui + '\n' + render + '\n')
    s = s[:a] + novo + s[b:]
    open(G, 'w', encoding='utf-8').write(s)
    print('ok', chave, orig, len(s))

if __name__ == '__main__':
    for c in sys.argv[1:]: montar(c)
