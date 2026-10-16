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
 'ripado': tema('Ripado e LED', f'{T_}/dna1008.webp', '#121110', '#D9822B',
    V('#121110','#F7F3EE','rgba(236,226,214,.74)','rgba(255,180,100,.07)','rgba(255,215,160,.15)','4,3,2','rgba(16,14,12,.9)','#C2701F','#E08A3A','#FFF2E4'),
    fechadura=True),
 'dente': tema('Dente-de-leão', f'{T_}/blend.webp', '#17110C', '#C98A3A',
    V('#17110C','#FBF4EA','rgba(240,226,206,.74)','rgba(255,200,130,.07)','rgba(255,230,180,.15)','8,5,3','rgba(20,14,10,.9)','#B5752C','#D9964A','#FCF1E2')),
 'cristal': tema('Cristal esmeralda', f'{T_}/cristal.webp', '#0C1418', '#0F7A66',
    V('#0C1418','#F1F7F7','rgba(214,236,236,.74)','rgba(90,220,180,.07)','rgba(200,240,235,.14)','3,10,12','rgba(6,16,20,.9)','#0F7A66','#18A086','#E6F6F2')),
 'imperador': tema('Art déco cobre', f'{T_}/imperador.webp', '#120F0C', '#A8692F',
    V('#120F0C','#FBF5EC','rgba(240,228,210,.74)','rgba(255,190,120,.07)','rgba(255,225,180,.15)','8,6,4','rgba(18,14,10,.9)','#A8692F','#C98A4A','#FBF0E3')),
 'geometrico': tema('Tapete geométrico', f'{T_}/geometrico.webp', '#0B1622', '#2E7FA6',
    V('#0B1622','#F0F6FA','rgba(210,228,240,.74)','rgba(90,190,220,.07)','rgba(200,230,245,.14)','3,8,14','rgba(6,14,22,.9)','#2E7FA6','#3F98C2','#E8F3F9'),
    fechadura=True),
 'palha': tema('Palha e madeira', f'{T_}/palha.webp', '#15110C', '#7A8F4E',
    V('#15110C','#FAF5EC','rgba(238,226,206,.74)','rgba(255,200,130,.07)','rgba(220,235,190,.13)','8,6,3','rgba(20,15,10,.9)','#6F8445','#8CA35C','#F1F5E8'),
    fechadura=True),
 'nogueira': tema('Nogueira e globos', f'{T_}/nogueira.webp', '#14100C', '#C08A3E',
    V('#14100C','#FBF4EA','rgba(240,226,206,.74)','rgba(255,190,110,.08)','rgba(255,225,170,.15)','8,5,3','rgba(18,13,9,.9)','#A8732E','#C98F45','#FCF1E2')),
 'nero': tema('Mármore Nero e ouro', f'{T_}/nero.webp', '#0A0F0C', '#B08A3E',
    V('#0A0F0C','#F7F4EC','rgba(232,226,210,.74)','rgba(255,210,140,.07)','rgba(240,225,190,.14)','2,5,3','rgba(8,12,10,.9)','#0F5A3C','#1A7A52','#E8F4EE')),
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
# visitas proibidas em todos os guias (Pedro): os do QS diziam que visita só não podia pernoitar
QS_VISITAS = [('Visitas não podem pernoitar e precisam ser identificadas na recepção.', 'Visitas não são permitidas: só os hóspedes cadastrados no check-in online sobem à suíte.'),
              ('Visitors cannot stay overnight and must be identified at the front desk.', 'Visitors are not allowed: only the guests registered in the online check-in may go up to the suite.'),
              ('Las visitas no pueden pernoctar y deben identificarse en recepción.', 'No se permiten visitas: solo suben a la suite los huéspedes registrados en el check-in online.')]

# Crystal Place: 14h/11h, manobrista 24h, silêncio 22h–8h; 1113 e 209 têm o economizador HELP Smart
CP_MAPS = 'https://maps.google.com/?cid=1307861366333774887'
CP_RODAPE = {'pt': 'Tomadas 220V · Silêncio das 22h às 8h · Proibido fumar', 'en': '220V outlets · Quiet hours 10 pm–8 am · No smoking',
             'es': 'Enchufes 220V · Silencio de 22 a 8 h · Prohibido fumar'}
CP_ECO = {'pt': 'Economizador HELP Smart, ar e 220V', 'en': 'HELP Smart energy saver, AC and 220V', 'es': 'Ahorrador HELP Smart, aire y 220V'}
def ui_crystal(n, suite):
    tit = {'pt': f'Suíte {n}', 'en': f'Suite {n}', 'es': f'Suite {n}'} if suite else f'Flat {n}'
    sub = {'pt': 'Suíte do Imperador · Crystal Place, Goiânia', 'en': 'Emperor Suite · Crystal Place, Goiânia', 'es': 'Suite del Emperador · Crystal Place, Goiânia'} if suite \
          else 'Crystal Place · Setor Pedro Ludovico, Goiânia'
    ex = {l: {'rodapeRegras': CP_RODAPE[l], 'topicos': {'energia': {'s': CP_ECO[l]}}} for l in CP_RODAPE}
    if suite:
        for l, v in {'pt': ('A suíte', 'Cama, Wi-Fi, TV, banheiro e cozinha', 'Entrar na suíte'), 'en': ('The suite', 'Bed, Wi-Fi, TV, bathroom and kitchen', 'Getting into the suite'),
                     'es': ('La suite', 'Cama, wifi, TV, baño y cocina', 'Entrar a la suite')}.items():
            ex[l]['topicos'].update({'ape': {'t': v[0], 's': v[1]}, 'entrar': {'t': v[2]}})
    return ui_unidade(tit, sub, 14, 11, extra=ex)
def ui_sidney2(n, ala, andar, en_andar):
    lado = {'T': ('esquerda', 'left', 'izquierda'), 'O': ('direita', 'right', 'derecha')}[ala]
    ex = {'pt': {'topicos': {'entrar': {'s': f'{andar}º andar, Ala {ala} · senha da porta'}}},
          'en': {'topicos': {'entrar': {'s': f'{en_andar} floor, wing {ala} · door code'}}},
          'es': {'topicos': {'entrar': {'s': f'Piso {andar}, ala {ala} · clave de la puerta'}}}}
    return ui_unidade({'pt': f'{n} · Ala {ala}', 'en': f'{n} · Wing {ala}', 'es': f'{n} · Ala {ala}'}, 'Metropolitan Sidney · Jardim Goiás, Goiânia', 14, 11, extra=ex)

def cp(n, tema_, suite): return dict(predio='Crystal Place', maps=CP_MAPS, arq=f'guia-crystal-{n}.html', base_ref='2d6f8c2', tema=tema_, ui=ui_crystal(n, suite))

UNIDADES = {
  '501T': dict(predio='Metropolitan Sidney', arq='guia-sidney-501T.html', base_ref='ec0964c^', tema='veludo', ui=ui_sidney('T')),
  '501O': dict(predio='Metropolitan Sidney', arq='guia-sidney-501O.html', base_ref='ff167a0', tema='veludo', ui=ui_sidney('O')),
  '1806A': dict(predio='Metropolitan Barcelona', arq='guia-barcelona-1806A.html', base_ref='978a1cb', tema='seda',
     ui=ui_unidade('1806 A', 'Metropolitan Barcelona · Jardim Goiás, Goiânia', 14, 11,
        vaga_sub={'pt':'Subsolo 2 · cartão do portão no apê','en':'Basement 2 · gate card in the flat','es':'Subsuelo 2 · tarjeta del portón en el depto'},
        extra={'pt':{'vagaVal':'491'},'en':{'vagaVal':'491'},'es':{'vagaVal':'491'}})),
  '1003A': dict(predio='FR Bueno Municipal', arq='guia-fr-bueno-1003A.html', base_ref='978a1cb', tema='agua',
     ui=ui_unidade('Studio 1003A', 'FR Bueno Municipal · Setor Bueno, Goiânia', 15, 12, vaga_sub=FACIAL,
        extra={'pt':{'vagaVal':'093'},'en':{'vagaVal':'093'},'es':{'vagaVal':'093'}})),
  '1701': dict(predio='QS Marista', maps='https://maps.app.goo.gl/cJUTfjhT6uFq1ADb7', arq='guia-marista-1701.html', base_ref='978a1cb', tema='travertino',
     troca_dados=SAIDA_11H + QS_VISITAS, ui=ui_unidade('Suíte 1701', 'QS Marista · Setor Marista, Goiânia', 15, 11, extra=COPA)),
  '402': dict(predio='QS Marista', maps='https://maps.app.goo.gl/cJUTfjhT6uFq1ADb7', arq='guia-marista-402.html', base_ref='978a1cb', tema='travertino',
     troca_dados=SAIDA_11H + QS_VISITAS, ui=ui_unidade('Suíte 402', 'QS Marista · Setor Marista, Goiânia', 15, 11, extra=COPA)),
  '803S': dict(predio='Tai Residências', arq='guia-tai-803S.html', base_ref='978a1cb', tema='carvalho',
     ui=ui_unidade('Flat 803S', 'Tai Residências · Setor Bueno, Goiânia', 15, 12, vaga_sub=FACIAL)),
  '407B': dict(predio='DNA SmartStyle', arq='guia-dna-407B.html', base_ref='978a1cb', tema='marmore',
     ui=ui_unidade({'pt':'Flat 407 · Torre B','en':'Flat 407 · Tower B','es':'Flat 407 · Torre B'}, 'DNA SmartStyle · Setor Bueno, Goiânia', 15, 12,
        vaga_sub={'pt':'Subsolo S2 · controle no apê','en':'Basement S2 · remote in the flat','es':'Subsuelo S2 · control en el depto'})),
  '2003B': dict(predio='DNA SmartStyle', maps='https://maps.app.goo.gl/j8CLV2GZbMLrWVQUA', arq='guia-dna-2003B.html', base_ref='978a1cb', tema='noite', hero='sala-estar-jantar',
     mapa={'entrar': ['ape'], 'ape': ['duplex', 'cozinha']},
     ui=ui_unidade({'pt':'Duplex 2003','en':'Duplex 2003','es':'Dúplex 2003'}, {'pt':'Torre B · DNA SmartStyle · Setor Bueno, Goiânia','en':'Tower B · DNA SmartStyle · Setor Bueno, Goiânia','es':'Torre B · DNA SmartStyle · Setor Bueno, Goiânia'}, 15, 12,
        vaga_sub={'pt':'2º pavimento da garagem','en':'Garage level 2','es':'2º nivel del garaje'})),
  '1008B': dict(predio='DNA SmartStyle', maps='https://maps.app.goo.gl/j8CLV2GZbMLrWVQUA', arq='guia-dna-1008B.html', base_ref='ab7adad', tema='ripado', hero='sala',
     ui=ui_unidade({'pt':'Apartamento 1008','en':'Apartment 1008','es':'Apartamento 1008'}, {'pt':'Torre B · DNA SmartStyle · Setor Bueno, Goiânia','en':'Tower B · DNA SmartStyle · Setor Bueno, Goiânia','es':'Torre B · DNA SmartStyle · Setor Bueno, Goiânia'}, 15, 12,
        vaga_sub={'pt':'2º pavimento da garagem','en':'Garage level 2','es':'2º nivel del garaje'})),
  '757': dict(predio='Blend Smart Style', arq='guia-blend-757.html', base_ref='5bb9d24', tema='dente',
     ui=ui_unidade('Blend 757', 'Blend Smart Style · Setor Marista, Goiânia', 15, 12,
        extra={'pt':{'heroChip':'1 quarto · até 5 hóspedes'},'en':{'heroChip':'1 bedroom · up to 5 guests'},'es':{'heroChip':'1 dormitorio · hasta 5 huéspedes'}})),
  '1113': cp('1113', 'cristal', False), '2413': cp('2413', 'cristal', False), '1313': cp('1313', 'cristal', False),
  '911': cp('911', 'imperador', True), '209': cp('209', 'imperador', True),
  '1310': dict(predio='QS Marista', maps='https://maps.app.goo.gl/cJUTfjhT6uFq1ADb7', arq='guia-marista-1310.html', base_ref='c78e12d', tema='travertino',
     troca_dados=SAIDA_11H + QS_VISITAS, ui=ui_unidade('Suíte 1310', 'QS Marista · Setor Marista, Goiânia', 15, 11, extra={
        'pt': {'topicos': {'ape': {'t': 'A suíte', 's': 'Cama king, escritório, Wi-Fi e banheiro'}, 'entrar': {'t': 'Entrar na suíte'}}},
        'en': {'topicos': {'ape': {'t': 'The suite', 's': 'King bed, office, Wi-Fi and bathroom'}, 'entrar': {'t': 'Getting into the suite'}}},
        'es': {'topicos': {'ape': {'t': 'La suite', 's': 'Cama king, escritorio, wifi y baño'}, 'entrar': {'t': 'Entrar a la suite'}}}})),
  '2903': dict(predio='Walk Bueno', maps='https://maps.app.goo.gl/ce1t5VF6Cp3suEKx9', arq='guia-2903-walk-bueno-v20.html', base_ref='1f3c3e3', tema='nogueira',
     ui=ui_unidade({'pt': 'Duplex 2903', 'en': 'Duplex 2903', 'es': 'Dúplex 2903'}, 'Walk Bueno · Setor Bueno, Goiânia', 15, 12,
        vaga_sub={'pt': 'Térreo · -1 no elevador', 'en': 'Ground floor · -1 in the lift', 'es': 'Planta baja · -1 en el ascensor'},
        extra={'pt': {'rodapeRegras': 'Tomadas 220V · Silêncio depois das 22h · Proibido fumar', 'topicos': {'ape': {'t': 'O duplex', 's': 'Casa inteligente, Wi-Fi, bar e adega'}}},
               'en': {'rodapeRegras': '220V outlets · Quiet after 10 pm · No smoking', 'topicos': {'ape': {'t': 'The duplex', 's': 'Smart home, Wi-Fi, bar and wine fridge'}}},
               'es': {'rodapeRegras': 'Enchufes 220V · Silencio después de las 22 h · Prohibido fumar', 'topicos': {'ape': {'t': 'El dúplex', 's': 'Casa inteligente, wifi, bar y cava'}}}})),
  '503C': dict(predio='Winner Sport Life', arq='guia-winner-503C.html', base_ref='c5a363e', tema='nero',
     ui=ui_unidade({'pt': 'Apto 503', 'en': 'Apt 503', 'es': 'Depto 503'}, {'pt': 'Torre Conquista · Winner Sport Life, Jardim Goiás', 'en': 'Conquista Tower · Winner Sport Life, Jardim Goiás', 'es': 'Torre Conquista · Winner Sport Life, Jardim Goiás'}, 15, 12,
        vaga_sub={'pt': 'Portão G2 · controle na mesa de jantar', 'en': 'Gate G2 · remote on the dining table', 'es': 'Portón G2 · control en la mesa del comedor'},
        extra={'pt': {'topicos': {'ape': {'s': 'Suítes, Alexa, cozinha e bar'}}}, 'en': {'topicos': {'ape': {'s': 'Suites, Alexa, kitchen and bar'}}}, 'es': {'topicos': {'ape': {'s': 'Suites, Alexa, cocina y bar'}}}})),
  '504T': dict(predio='Metropolitan Sidney', arq='guia-sidney-504T.html', base_ref='c78e12d', tema='geometrico', ui=ui_sidney2('504', 'T', 5, '5th')),
  '1202O': dict(predio='Metropolitan Sidney', arq='guia-sidney-1202O.html', base_ref='003997a', tema='palha', ui=ui_sidney2('1202', 'O', 12, '12th')),
}
# 1202O: Wi-Fi por QR Code no modem (sem senha) — o card leva à explicação
for l, v in {'pt': 'Ver como conectar', 'en': 'How to connect', 'es': 'Cómo conectarse'}.items(): UNIDADES['1202O']['ui'][l]['wifiTap'] = v

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
    if U.get('maps'): tema_js['mapsUrl'] = U['maps']
    if U.get('predio'):
        for l in U['ui']: U['ui'][l]['predioNome'] = U['predio']
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
    import glob
    ics_ess = {os.path.basename(p)[4:-5]: b64(p, 'image/webp') for p in glob.glob(f'{P}/icones/ess-*.webp')}
    novo = ('<script>\n/* ícones dos 10 tópicos e do essencial (Gemini) e tema da unidade (Gemini) */\nvar ICS = ' + json.dumps(ics) +
            ';\nvar ICS_ESS = ' + json.dumps(ics_ess) +
            ';\nvar TEMA_TEX = "' + b64(T['tex'], 'image/webp') + '";\nvar TEMA = ' + json.dumps(tema_js) +
            ';\nvar UI_UNIDADE = ' + json.dumps(U['ui'], ensure_ascii=False) + ';\n' + ui + '\n' + render + '\n')
    s = s[:a] + novo + s[b:]
    open(G, 'w', encoding='utf-8').write(s)
    print('ok', chave, orig, len(s))

if __name__ == '__main__':
    for c in sys.argv[1:]: montar(c)
