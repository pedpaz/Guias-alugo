"""Gera a base v2 do QS-1310 (QS Marista, Suíte 1310) a partir do guia v2 do QS-1701 (978a1cb, mesmo prédio,
3 idiomas). O que é da suíte (andar, cama king, escritório, vista, capacidade 2 adultos + 1 bebê, vistoria) vem
do guia antigo do 1310 e é reescrito aqui nos 3 idiomas. A suíte 1310 não tem a tela de copa (o guia antigo não
menciona; tem frigobar — Pedro, 15/10). uso: python3 montar-base-QS1310.py → reescreve guia-marista-1310.html (depois: montar.py 1310)"""
import base64, copy, json, os, re, subprocess
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(P))
def git(ref, arq): return subprocess.run(['git', '-C', R, 'show', f'{ref}:{arq}'], capture_output=True, check=True).stdout.decode()
base = git('978a1cb', 'guia-marista-1701.html')
bd = base[base.index('<script id="dados">'):]; bd = bd[:bd.index('</script>')]
T0 = json.loads(re.search(r'var TXT = (\{.*\});?\s*$', bd, re.S).group(1).rstrip().rstrip(';'))
LS = ['pt', 'en', 'es']

def troca(o, pares):
    if isinstance(o, str):
        for a, b in pares: o = o.replace(a, b)
        return o
    if isinstance(o, list): return [troca(x, pares) for x in o]
    if isinstance(o, dict): return {k: troca(v, pares) for k, v in o.items()}
    return o

TXT = {}
for L in LS:
    x = lambda pt, en, es: {'pt': pt, 'en': en, 'es': es}[L]
    T = copy.deepcopy(T0[L]); T.pop('tela_copa', None)
    T = troca(T, [('1701', '1310'), ('17º andar', '13º andar'), ('Floor 17', 'Floor 13'), ('floor <b>17</b>', 'floor <b>13</b>'),
                  ('Piso 17', 'Piso 13'), ('piso <b>17</b>', 'piso <b>13</b>'), ('<b>17º andar</b>', '<b>13º andar</b>')])
    T['tela_ape'] = dict(titulo=x('A suíte', 'The suite', 'La suite'),
      sub=x('Suíte King · 36 m² · 2 adultos + 1 bebê', 'King suite · 36 m² · 2 adults + 1 baby', 'Suite King · 36 m² · 2 adultos + 1 bebé'),
      lead=x('A maior suíte do prédio: 36 m², decoração assinada, vista panorâmica de Goiânia e escritório integrado.',
             'The largest suite in the building: 36 m², designer décor, a panoramic view of Goiânia and a built-in office.',
             'La suite más grande del edificio: 36 m², decoración de autor, vista panorámica de Goiânia y escritorio integrado.'),
      blocos=[dict(foto='ape-cama', h=x('Onde dormir', 'Sleeping', 'Dónde dormir'),
                   p=[x('<b>Cama king</b> com enxoval hoteleiro — roupa de cama e de banho inclusas.', '<b>King bed</b> with hotel linen — bedding and towels included.',
                        '<b>Cama king</b> con ropa de hotel: ropa de cama y de baño incluidas.'),
                      x('Capacidade: <b>2 adultos + 1 bebê</b>.', 'Capacity: <b>2 adults + 1 baby</b>.', 'Capacidad: <b>2 adultos + 1 bebé</b>.')]),
              dict(foto='ape-escritorio', h=x('Para trabalhar', 'For work', 'Para trabajar'),
                   p=[x('O escritório integrado e a Smart TV fazem da suíte um bom lugar para lazer ou negócios.', 'The built-in office and Smart TV make the suite work for leisure or business.',
                        'El escritorio integrado y la Smart TV hacen de la suite un buen lugar para ocio o negocios.'),
                      x('O Wi-Fi do prédio chega em toda a suíte. A rede e a senha estão no cartão do topo deste guia, com um toque para copiar.',
                        'The building Wi-Fi reaches the whole suite. The network and password are on the card at the top of this guide — tap to copy.',
                        'El wifi del edificio llega a toda la suite. La red y la clave están en la tarjeta del inicio de esta guía: toca para copiar.')]),
              dict(foto='ape-banheiro', h=x('O banheiro', 'The bathroom', 'El baño'),
                   p=[x('Bancada de pedra e <b>amenities</b> — shampoo, condicionador e sabonete.', 'Stone vanity and <b>toiletries</b> — shampoo, conditioner and soap.',
                        'Mesada de piedra y <b>amenities</b>: champú, acondicionador y jabón.'),
                      x('Precisa de toalha extra ou de mais amenities? É só pedir pelo WhatsApp.', 'Need an extra towel or more toiletries? Just ask on WhatsApp.',
                        '¿Necesitas otra toalla o más amenities? Pídelo por WhatsApp.')]),
              dict(h=x('Frigobar', 'Minibar fridge', 'Frigobar'),
                   p=[x('A suíte tem <b>frigobar</b> para as bebidas e o lanche. Ao sair, retire o que sobrou.', 'The suite has a <b>minibar fridge</b> for drinks and snacks. Empty it when you leave.',
                        'La suite tiene <b>frigobar</b> para bebidas y snacks. Al irte, retira lo que quedó.')]),
              dict(h=x('Ar-condicionado e energia', 'Air conditioning and power', 'Aire acondicionado y energía'),
                   p=[x('Use o ar com a janela e as cortinas fechadas: gela mais rápido e mantém melhor.', 'Use the air conditioning with the window and curtains closed: it cools faster and holds better.',
                        'Usa el aire con la ventana y las cortinas cerradas: enfría más rápido y mantiene mejor.'),
                      x('<b>Tomadas 220V.</b> Confira a voltagem dos seus aparelhos antes de ligar.', '<b>220V outlets.</b> Check your devices before plugging in.',
                        '<b>Enchufes de 220 V.</b> Revisa el voltaje de tus aparatos antes de enchufar.')])])
    T['tela_checkin']['vistItens'] = [x('Cama king e enxoval', 'King bed and linen', 'Cama king y ropa de cama'),
        x('TV, ar-condicionado e iluminação', 'TV, air conditioning and lighting', 'TV, aire acondicionado e iluminación'),
        x('Escritório e mobiliário', 'Office and furniture', 'Escritorio y mobiliario'),
        x('Banheiro, louça sanitária e amenities', 'Bathroom, fixtures and toiletries', 'Baño, sanitarios y amenities'),
        x('Limpeza geral', 'General cleanliness', 'Limpieza general'), x('Fechadura ou cartão com problema', 'Lock or card problem', 'Problema con la cerradura o la tarjeta')]
    T['tela_regras'] = troca(T['tela_regras'], [('<b>2 hóspede(s)</b>', '<b>2 adultos + 1 bebê</b>'), ('<b>2 guest(s)</b>', '<b>2 adults + 1 baby</b>'),
                                                ('<b>2 huésped(es)</b>', '<b>2 adultos + 1 bebé</b>')])
    TXT[L] = T
assert '1701' not in json.dumps(TXT) and '17º' not in json.dumps(TXT, ensure_ascii=False)

telas_js = bd[bd.index('var TELAS'):bd.index('var SINONIMOS')]
telas_js = re.sub(r"\n\s*\{id:'copa'[^\n]*", '', telas_js)
sin_js = bd[bd.index('var SINONIMOS'):bd.index('var TXT')].replace('1701', '1310').replace('17 andar', '13 andar')
rend = bd[:bd.index('var TELAS')].replace('1701', '1310')
s = base.replace(bd, rend + telas_js + sin_js + 'var TXT = ' + json.dumps(TXT, ensure_ascii=False, indent=1) + ';\n')
def troca_var(s, nome, valor):
    s2, k = re.subn(r'^var %s\s*=.*$' % nome, lambda m: f'var {nome} = {valor};', s, count=1, flags=re.M); assert k == 1, nome; return s2
fot = json.loads(re.search(r'^var FOTOS\s*=\s*(\{.*\});\s*$', base, re.M).group(1))
b64 = lambda f: 'data:image/webp;base64,' + base64.b64encode(open(f'{P}/marista-fotos/{f}.webp', 'rb').read()).decode()
fotos = {k: v for k, v in fot.items() if k.startswith('predio-')}
fotos.update({'hero': b64('1310-cama'), 'ape-cama': b64('1310-cama'), 'ape-escritorio': b64('1310-escritorio'), 'ape-banheiro': b64('1310-banheiro')})
s = troca_var(s, 'UNIDADE', '"QS-1310"'); s = troca_var(s, 'TERMO_URL', '"https://pedpaz.github.io/Guias-alugo/termo.html?u=QS-1310"')
s = troca_var(s, 'FOTOS', json.dumps(fotos))
if re.search(r'^var CARDS', s, re.M): s = troca_var(s, 'CARDS', '{}')
s = re.sub(r'<title>[^<]*</title>', '<title>QS Marista · Suíte 1310 · Guia da estadia</title>', s, 1)
assert '1701' not in re.sub(r'data:[^"]+', '', s)
open(f'{R}/guia-marista-1310.html', 'w', encoding='utf-8').write(s)
print('ok', len(s), [k[5:] for k in TXT['pt'] if k.startswith('tela_')])
