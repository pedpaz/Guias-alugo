"""Gera a base v2 (TELAS/TXT/SINONIMOS) do SM-504T e do SM-1202O.
Esqueleto e conteúdo do prédio: guia v2 do 501T (ec0964c^) / 501O (e9bacd1), mesmo prédio, nos 3 idiomas.
O que é da unidade (porta, apartamento, cozinha, garagem, vistoria, capacidade, saída, Wi-Fi) vem do
guia antigo de cada uma (formato HTML + KB, só em português) e é reescrito aqui nos 3 idiomas.
uso: python3 montar-base-sidney.py [504T 1202O]   → reescreve guia-sidney-<u>.html (depois: montar.py <u>)"""
import base64, copy, json, os, re, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(P))
FOT = f'{P}/sidney-fotos'
def git(ref, arq): return subprocess.run(['git', '-C', R, 'show', f'{ref}:{arq}'], capture_output=True, check=True).stdout.decode()
LS = ['pt', 'en', 'es']

UN = {
 '504T': dict(base=('ec0964c^', 'guia-sidney-501T.html'), ala='T', andar=5, num='504', senha='1213*', rede='alugo504t', wsenha='apartamento504t',
              cap=4, vaga='194', luz=True, fotos={'hero': '504-hero', 'ape-sala': '504-sala', 'ape-quarto': '504-quarto', 'ape-cozinha': '504-cozinha',
                                                  'ape-banheiro': '504-banheiro', 'ape-mesa': '504-mesa'}),
 '1202O': dict(base=('e9bacd1', 'guia-sidney-501O.html'), ala='O', andar=12, num='1202', senha='3078*', rede='', wsenha='',
               cap=2, vaga='72', luz=False, fotos={'hero': '1202-hero', 'ape-cama': '1202-cama'}),
}
# fotos do prédio e do cartão de energia vêm da base do 501T (mesmas instalações)
FOTOS_PREDIO = ['predio-fachada', 'predio-torre', 'predio-lobby', 'predio-piscina', 'predio-piscina2', 'predio-jacuzzi', 'predio-academia',
                'predio-sauna', 'predio-rooftop', 'predio-lavanderia', 'predio-mall', 'predio-mall-porta', 'vista']
FOTOS_LUZ = ['ape-energia', 'ape-energia-cartao', 'ape-energia-aviso']

def dados_de(html):
    d = html[html.index('<script id="dados">'):]; d = d[:d.index('</script>')]
    return d, json.loads(re.search(r'var TXT = (\{.*\});?\s*$', d, re.S).group(1).rstrip().rstrip(';'))

def ordinal(n, L):
    suf = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return {'pt': f'{n}º andar', 'en': f'{n}{suf} floor', 'es': f'{n}º piso'}[L]

def troca(o, pares):
    """substitui texto em todas as strings de um objeto (dict/list/str)"""
    if isinstance(o, str):
        for a, b in pares: o = o.replace(a, b)
        return o
    if isinstance(o, list): return [troca(x, pares) for x in o]
    if isinstance(o, dict): return {k: troca(v, pares) for k, v in o.items()}
    return o

def gerar(u, cor_tema):
    U = UN[u]; base = git(*U['base']); base_dados, T0 = dados_de(base)
    n, ala, A = U['num'], U['ala'], U['andar']
    lado = {'T': ('esquerda', 'left', 'izquierda'), 'O': ('direita', 'right', 'derecha')}[ala]
    TXT = {}
    for i, L in enumerate(LS):
        x = lambda pt, en, es: {'pt': pt, 'en': en, 'es': es}[L]
        T = copy.deepcopy(T0[L])
        # ---- textos gerais
        nome = x(f'{n} · Ala {ala}', f'{n} · Wing {ala}', f'{n} · Ala {ala}')
        rot = f'Metropolitan Sidney {n}{ala}'
        T.update(apeNome=nome, apeSub=x(f'{n} · Ala {ala} · Metropolitan Sidney, Jardim Goiás', f'{n} · Wing {ala} · Metropolitan Sidney, Jardim Goiás', f'{n} · Ala {ala} · Metropolitan Sidney, Jardim Goiás'),
          zapOi=x(f'Olá! Sou hóspede do {rot} e preciso de ajuda.', f"Hello! I'm staying at {rot} and I need help.", f'¡Hola! Soy huésped del {rot} y necesito ayuda.'),
          zapSenha=x(f'Olá! Sou hóspede do {rot}. Pode me enviar a senha da porta?', f"Hello! I'm staying at {rot}. Could you send me the door code?", f'¡Hola! Soy huésped del {rot}. ¿Me envían la clave de la puerta?'),
          zapWifi=x(f'Olá! Sou hóspede do {rot}. Pode me ajudar com o Wi-Fi?', f"Hello! I'm staying at {rot}. Could you help me with the Wi-Fi?", f'¡Hola! Soy huésped del {rot}. ¿Me ayudan con el wifi?'),
          zapVaga=x(f'Olá! Sou hóspede do {rot} e vou chegar de carro. Qual é a minha vaga?', f"Hello! I'm staying at {rot} and I'm arriving by car. Which parking space is mine?", f'¡Hola! Soy huésped del {rot} y llego en auto. ¿Cuál es mi cochera?'),
          zapCheckout=x(f'Olá! Estou fazendo o check-out do {rot}. Já deixei o apartamento.', f"Hello! I'm checking out of {rot}. I've left the apartment.", f'¡Hola! Estoy haciendo el check-out del {rot}. Ya dejé el departamento.'),
          vistMsg=x(f'Vistoria de chegada — {rot}. Encontrei:', f'Arrival inspection — {rot}. I found:', f'Inspección de llegada — {rot}. Encontré:'))
        if not U['wsenha']:
            T['cWifiPend'] = x('QR Code no modem', 'QR code on the router', 'Código QR en el módem')

        # ---- prédio: só o andar muda
        T['tela_predio'] = troca(T['tela_predio'], [('5º andar', ordinal(A, 'pt')), ('5th floor', ordinal(A, 'en')), ('5º piso', ordinal(A, 'es')), ('5.º piso', ordinal(A, 'es')), ('quinto piso', ordinal(A, 'es'))])

        # ---- porta: a da unidade-base (mesma ala), com o número, o andar e a senha desta unidade
        porta = T['tela_porta']
        pares = [('501', n), ('5010', n + '0'), ('5º andar', ordinal(A, 'pt')), ('5th floor', ordinal(A, 'en')), ('5º piso', ordinal(A, 'es')),
                 ('5.º piso', ordinal(A, 'es')), ('quinto piso', ordinal(A, 'es')), ('#B8121F', cor_tema)]
        porta = troca(porta, pares)
        for b in porta['blocos']:
            if b.get('chave'): b['chave'] = U['senha'].rstrip('*') + ' ✱'
        if not U['luz']:
            porta['blocos'] = [b for b in porta['blocos'] if "abrir('luz')" not in json.dumps(b)]
        porta['blocos'] = [b for b in porta['blocos'] if not (b.get('h', '').startswith(('Nada a', 'Nothing to', 'Nada que')))]
        porta['blocos'].append(dict(h=x('Nada a retirar, nada a devolver', 'Nothing to collect or return', 'Nada que retirar ni devolver'),
            p=[x('Não há chave para buscar na portaria. Ao sair, feche a porta, encoste a mão no teclado e aguarde o bip de travamento.',
                 'There is no key to pick up at the front desk. When you leave, close the door, touch the keypad and wait for the locking beep.',
                 'No hay llave que retirar en la portería. Al salir, cierra la puerta, toca el teclado y espera el pitido de cierre.')]))
        assert '501' not in json.dumps(porta), 'sobrou 501 na porta'
        T['tela_porta'] = porta

        # ---- o apartamento
        if u == '504T':
            T['tela_ape'] = dict(titulo=x('O apartamento', 'The apartment', 'El departamento'),
              sub=x('1 quarto + sofá-cama · até 4 pessoas · 220V', '1 bedroom + sofa bed · up to 4 guests · 220V', '1 dormitorio + sofá cama · hasta 4 personas · 220V'),
              lead=x('Um quarto separado e um living integrado à cozinha, em tons claros de madeira, com o sofá azul e a mesa redonda junto à janela.',
                     'A separate bedroom and a living area open to the kitchen, in light wood tones, with the blue sofa and the round table by the window.',
                     'Un dormitorio aparte y un living integrado a la cocina, en tonos claros de madera, con el sofá azul y la mesa redonda junto a la ventana.'),
              blocos=[dict(foto='ape-sala', h=x('O living', 'The living area', 'El living'),
                           p=[x('<b>Sofá-cama</b>, Smart TV e a cozinha logo ao lado, num ambiente só.', '<b>Sofa bed</b>, Smart TV and the kitchen right beside, all in one space.', '<b>Sofá cama</b>, Smart TV y la cocina al lado, en un solo ambiente.')]),
                      dict(foto='ape-quarto', h=x('O quarto', 'The bedroom', 'El dormitorio'),
                           p=[x('Cama de casal com cabeceira iluminada, ar-condicionado e TV. Com o <b>sofá-cama da sala</b>, a unidade recebe até <b>4 hóspedes</b>.',
                                'Double bed with a lit headboard, air conditioning and TV. With the <b>living-room sofa bed</b>, the unit sleeps up to <b>4 guests</b>.',
                                'Cama doble con cabecera iluminada, aire acondicionado y TV. Con el <b>sofá cama de la sala</b>, la unidad recibe hasta <b>4 huéspedes</b>.')]),
                      dict(foto='ape-mesa', h=x('A mesa com vista', 'The table with a view', 'La mesa con vista'),
                           p=[x('Mesa redonda para quatro, junto ao vidro, de frente para o Jardim Goiás.', 'A round table for four by the glass, facing Jardim Goiás.', 'Mesa redonda para cuatro, junto al vidrio, frente al Jardim Goiás.')]),
                      dict(h=x('Conforto', 'Comfort', 'Confort'),
                           ul=[x('<b>Ar-condicionado split</b>', '<b>Split air conditioning</b>', '<b>Aire acondicionado split</b>'),
                               x('<b>Smart TV</b> com streaming', '<b>Smart TV</b> with streaming', '<b>Smart TV</b> con streaming'),
                               x('Roupa de cama e toalhas limpas na chegada', 'Clean bedding and towels on arrival', 'Ropa de cama y toallas limpias a la llegada')]),
                      dict(foto='ape-banheiro', h=x('O banheiro', 'The bathroom', 'El baño'),
                           p=[x('Bancada com cuba e box de vidro.', 'Vanity with basin and glass shower.', 'Mesada con bacha y box de vidrio.')]),
                      dict(dest=True, h='Wi-Fi', p=[x(f'Rede <b>{U["rede"]}</b> · senha <b>{U["wsenha"]}</b>. Também está no cartão do topo do guia — toque para copiar.',
                                                    f'Network <b>{U["rede"]}</b> · password <b>{U["wsenha"]}</b>. It is also on the card at the top of the guide — tap to copy.',
                                                    f'Red <b>{U["rede"]}</b> · clave <b>{U["wsenha"]}</b>. También está en la tarjeta del inicio de la guía: toca para copiar.')]),
                      dict(dest=True, h='220V', p=[x('Padrão de Goiás. Confira a voltagem dos seus aparelhos antes de ligar.', 'Standard in Goiás. Check your devices before plugging in.', 'Estándar en Goiás. Revisa el voltaje de tus aparatos antes de enchufar.')])])
        else:
            T['tela_ape'] = dict(titulo=x('O apartamento', 'The apartment', 'El departamento'),
              sub=x('Studio · 2 pessoas · 220V', 'Studio · 2 guests · 220V', 'Estudio · 2 personas · 220V'),
              lead=x('Um studio de ambiente integrado, em madeira e tons claros, com estante vazada separando o estar da cama.',
                     'An open-plan studio in wood and light tones, with an open shelf separating the living area from the bed.',
                     'Un estudio integrado, en madera y tonos claros, con un estante calado que separa el estar de la cama.'),
              blocos=[dict(foto='hero', h=x('O estar e a cozinha', 'Living area and kitchen', 'El estar y la cocina'),
                           p=[x('Sofá, tapete e a cozinha com balcão e banquetas logo adiante.', 'Sofa, rug and the kitchen with a counter and stools just beyond.', 'Sofá, alfombra y la cocina con barra y banquetas al fondo.')]),
                      dict(foto='ape-cama', h=x('Onde dormir', 'Sleeping', 'Dónde dormir'),
                           p=[x('Cama de casal para <b>2 pessoas</b>, com a TV na estante e o cantinho de home office ao lado.',
                                'Double bed for <b>2 guests</b>, with the TV on the shelf and a small home-office corner beside it.',
                                'Cama doble para <b>2 personas</b>, con la TV en el estante y un rincón de home office al lado.')]),
                      dict(h=x('Conforto', 'Comfort', 'Confort'),
                           ul=[x('<b>Ar-condicionado split</b>', '<b>Split air conditioning</b>', '<b>Aire acondicionado split</b>'),
                               x('<b>Smart TV</b> com streaming', '<b>Smart TV</b> with streaming', '<b>Smart TV</b> con streaming'),
                               x('Cantinho de <b>home office</b>', 'A <b>home-office</b> corner', 'Rincón de <b>home office</b>'),
                               x('Roupa de cama e toalhas limpas na chegada', 'Clean bedding and towels on arrival', 'Ropa de cama y toallas limpias a la llegada')]),
                      dict(dest=True, h='Wi-Fi', p=[x('Sem senha para digitar: <b>escaneie o QR Code colado no modem</b> com a câmera do celular e a conexão é feita na hora.',
                                                    'No password to type: <b>scan the QR code on the router</b> with your phone camera and you are connected.',
                                                    'Sin clave para escribir: <b>escanea el código QR pegado en el módem</b> con la cámara del celular y te conectas al instante.'),
                                                  x('Não encontrou o QR Code? <a href="#" onclick="zap(TXT[L].zapWifi);return false">Fale com a gente</a>.',
                                                    'Can’t find the QR code? <a href="#" onclick="zap(TXT[L].zapWifi);return false">Message us</a>.',
                                                    '¿No encuentras el código QR? <a href="#" onclick="zap(TXT[L].zapWifi);return false">Escríbenos</a>.')]),
                      dict(dest=True, h='220V', p=[x('Padrão de Goiás. Confira a voltagem dos seus aparelhos antes de ligar.', 'Standard in Goiás. Check your devices before plugging in.', 'Estándar en Goiás. Revisa el voltaje de tus aparatos antes de enchufar.')])])

        # ---- cozinha: o lixo é do prédio (mantém o bloco da base); o resto é da unidade
        lixo = [b for b in T['tela_cozinha']['blocos'] if 'elevador de serviço' in json.dumps(b, ensure_ascii=False) or 'service lift' in json.dumps(b) or 'servicio' in json.dumps(b, ensure_ascii=False)]
        T['tela_cozinha'] = dict(titulo=x('A cozinha', 'The kitchen', 'La cocina'), sub=x('Completa, para cozinhar de verdade', 'Fully equipped for real cooking', 'Completa, para cocinar de verdad'),
          lead=x('Dá para preparar as refeições do dia a dia sem sair de casa.', 'You can cook your everyday meals without going out.', 'Puedes preparar las comidas del día sin salir.'),
          blocos=[dict(**({'foto': 'ape-cozinha'} if 'ape-cozinha' in U['fotos'] else {}), h=x('O que tem', 'What there is', 'Qué hay'),
                       ul=[x('<b>Cooktop</b>', '<b>Cooktop</b>', '<b>Anafe</b>'), x('<b>Micro-ondas</b>', '<b>Microwave</b>', '<b>Microondas</b>'),
                           x('<b>Geladeira</b>', '<b>Fridge</b>', '<b>Heladera</b>'), x('<b>Cafeteira</b>', '<b>Coffee maker</b>', '<b>Cafetera</b>'),
                           x('Louças, panelas e utensílios prontos para uso', 'Dishes, pans and utensils ready to use', 'Vajilla, ollas y utensilios listos para usar')])] + lixo)

        # ---- garagem
        g = T['tela_garagem']
        for b in g['blocos']:
            if b.get('chave'): b['chave'] = U['vaga']
        g['sub'] = x(f'Vaga {U["vaga"]}', f'Space {U["vaga"]}', f'Cochera {U["vaga"]}') + ' · ' + (
            x('Portão 1', 'Gate 1', 'Portón 1') if u == '504T' else x('subsolo', 'basement', 'subsuelo'))
        onde = dict(h=x('Onde fica', 'Where it is', 'Dónde está'),
                    p=[x('Entre pelo <b>Portão 1</b>.', 'Use <b>Gate 1</b>.', 'Entra por el <b>Portón 1</b>.') if u == '504T' else
                       x('A vaga fica no <b>subsolo</b>.', 'The space is in the <b>basement</b>.', 'La cochera está en el <b>subsuelo</b>.')])
        g['blocos'].insert(1, onde)
        assert '190' not in json.dumps(g)
        T['tela_garagem'] = g

        # ---- vistoria
        T['tela_checkin']['vistItens'] = [x('Cama, colchão e roupa de cama', 'Bed, mattress and bedding', 'Cama, colchón y ropa de cama'),
            x('Sofá e estofados', 'Sofa and upholstery', 'Sofá y tapizados'), x('TV e controle remoto', 'TV and remote', 'TV y control remoto'),
            x('Cozinha: cooktop, micro-ondas e geladeira', 'Kitchen: cooktop, microwave and fridge', 'Cocina: anafe, microondas y heladera'),
            x('Louças, panelas e utensílios', 'Dishes, pans and utensils', 'Vajilla, ollas y utensilios'), x('Banheiro e chuveiro', 'Bathroom and shower', 'Baño y ducha'),
            x('Ar-condicionado', 'Air conditioning', 'Aire acondicionado'), x('Paredes, piso e janelas', 'Walls, floor and windows', 'Paredes, piso y ventanas')]

        # ---- regras: capacidade
        cap = U['cap']
        T['tela_regras'] = troca(T['tela_regras'], [('Capacidade: 2 pessoas', f'Capacidade: {cap} pessoas'), ('<b>2 hóspedes</b>', f'<b>{cap} hóspedes</b>'),
            ('Capacity: 2 guests', f'Capacity: {cap} guests'), ('<b>2 guests</b>', f'<b>{cap} guests</b>'),
            ('Capacidad: 2 personas', f'Capacidad: {cap} personas'), ('<b>2 huéspedes</b>', f'<b>{cap} huéspedes</b>')])
        assert f'{cap}' in json.dumps(T['tela_regras'])

        # ---- saída
        s = T['tela_saida']
        for b in s['blocos']:
            if b.get('ul'):
                b['ul'] = [troca(it, [(' e o closet', ' e os armários'), (' and the closet', ' and the wardrobe'), (' y el clóset', ' y los armarios'), (' y el vestidor', ' y los armarios')])
                           for it in b['ul'] if U['luz'] or ('cartão' not in it.lower() and 'card' not in it.lower() and 'tarjeta' not in it.lower())]
        T['tela_saida'] = s

        # ---- deu problema
        pr = T['tela_problema']
        if not U['luz']:
            pr['ac'] = [a for a in pr['ac'] if "abrir('luz')" not in json.dumps(a)]
        for a in pr['ac']:
            if a['q'] in ('O Wi-Fi caiu', 'The Wi-Fi is down', 'The Wi-Fi dropped', 'Se cayó el wifi', 'Se cayó el Wi-Fi'):
                a['r'] = ([x('Escaneie de novo o <b>QR Code do modem</b>.', 'Scan the <b>QR code on the router</b> again.', 'Vuelve a escanear el <b>código QR del módem</b>.')] if not U['wsenha'] else
                          [x(f'A rede é a <b>{U["rede"]}</b> e a senha está no cartão do topo do guia.', f'The network is <b>{U["rede"]}</b> and the password is on the card at the top of the guide.',
                             f'La red es <b>{U["rede"]}</b> y la clave está en la tarjeta del inicio de la guía.')]) + a['r']
        T['tela_problema'] = pr
        if not U['luz']: T.pop('tela_luz', None)
        T['tela_lazer'] = troca(T['tela_lazer'], [])
        TXT[L] = T

    # nada de Red Velvet / 501 nos textos
    tudo = json.dumps(TXT, ensure_ascii=False)
    for proib in ['Red Velvet', '501', '101001', '101002', '190-T', 'Bambola']:
        assert proib not in tudo, proib

    # telas: as da base, sem a do cartão de energia quando a unidade não tem
    telas_js = base_dados[base_dados.index('var TELAS'):base_dados.index('var SINONIMOS')]
    if not U['luz']: telas_js = re.sub(r"\n\s*\{id:'luz'[^\n]*", '', telas_js)
    sin_js = base_dados[base_dados.index('var SINONIMOS'):base_dados.index('var TXT')]
    sin_js = sin_js.replace('501', n).replace('101001', U['senha'].rstrip('*')).replace('101002', U['senha'].rstrip('*'))
    rend = base_dados[:base_dados.index('var TELAS')]
    rend = re.sub(r'SM-501[TO] · [^*\n]*', f'SM-{u} · Metropolitan Sidney', rend)
    dados = rend + telas_js + sin_js + 'var TXT = ' + json.dumps(TXT, ensure_ascii=False, indent=1) + ';\n'
    s = base.replace(base_dados, dados)

    def troca_var(s, nome, valor):
        s2, k = re.subn(r'^var %s\s*=.*$' % nome, lambda m: f'var {nome} = {valor};', s, count=1, flags=re.M); assert k == 1, nome; return s2
    fot_base = json.loads(re.search(r'^var FOTOS\s*=\s*(\{.*\});\s*$', git('ec0964c^', 'guia-sidney-501T.html'), re.M).group(1))
    fotos = {k: fot_base[k] for k in FOTOS_PREDIO + (FOTOS_LUZ if U['luz'] else []) if k in fot_base}
    fotos.update({k: 'data:image/webp;base64,' + base64.b64encode(open(f'{FOT}/{v}.webp', 'rb').read()).decode() for k, v in U['fotos'].items()})
    s = troca_var(s, 'UNIDADE', json.dumps(f'SM-{u}'))
    s = troca_var(s, 'TERMO_URL', json.dumps(f'https://pedpaz.github.io/Guias-alugo/termo.html?u=SM-{u}'))
    s = troca_var(s, 'SENHA', json.dumps(U['senha'])); s = troca_var(s, 'WIFI_REDE', json.dumps(U['rede'])); s = troca_var(s, 'WIFI_SENHA', json.dumps(U['wsenha']))
    s = troca_var(s, 'FOTOS', json.dumps(fotos))
    if re.search(r'^var CARDS', s, re.M): s = troca_var(s, 'CARDS', '{}')
    s = re.sub(r'<title>[^<]*</title>', f'<title>Metropolitan Sidney {n} · Ala {ala} · Guia da estadia</title>', s, 1)
    cfg = re.sub(r'data:[^"]+', '', s.split('<script id="dados">')[0])
    for proib in ['101001', '101002', 'Bambola', 'Red Velvet']:
        assert proib not in cfg, proib
    open(f'{R}/guia-sidney-{u}.html', 'w', encoding='utf-8').write(s)
    print('ok', u, len(s), [k[5:] for k in TXT['pt'] if k.startswith('tela_')])

if __name__ == '__main__':
    COR = {'504T': '#2E7FA6', '1202O': '#7A8F4E'}
    for u in (sys.argv[1:] or list(UN)): gerar(u, COR[u])
