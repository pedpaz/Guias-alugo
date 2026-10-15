"""Gera a base v2 (TELAS/TXT/SINONIMOS) dos 5 guias do Crystal Place a partir do conteúdo dos guias
antigos (HTML por seções, só em português), já com as regras atuais da aluGO e nos 3 idiomas.
Esqueleto: guia v2 do DS-407B (978a1cb). O tutorial do HELP Smart (1113 e 209) é o bloco original,
guardado em crystal-hs/hs-<unidade>.html e mostrado em português; em inglês e espanhol vira texto.
uso: python3 montar-base-crystal.py [1113 1313 2413 911 209]   → reescreve guia-crystal-<n>.html
     (depois: montar.py <n>)"""
import base64, json, os, re, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(P))
FOT = f'{P}/crystal-fotos'
def git(ref, arq): return subprocess.run(['git', '-C', R, 'show', f'{ref}:{arq}'], capture_output=True, check=True).stdout.decode()
base = git('978a1cb', 'guia-dna-407B.html')
LS = ['pt', 'en', 'es']
MAPS = 'https://maps.google.com/?cid=1307861366333774887'

def X(pt, en, es): return {'pt': pt, 'en': en, 'es': es}

# ---------------------------------------------------------------- unidades
UN = {
 '1113': dict(tipo='flat', andar=11, acesso='cartao', rede='Ap-1113', senha_wifi='flat1113', cap=4, help=True,
              camas=X('1 cama de casal + 1 sofá-cama', '1 double bed + 1 sofa bed', '1 cama doble + 1 sofá cama'),
              fotos={'hero': 'f1113-hero', 'sala': 'f1113-a1', 'quarto': 'f1113-a2', 'cozinha': 'f1113-coz'}),
 '2413': dict(tipo='flat', andar=24, acesso='cartao', rede='Ap-2413', senha_wifi='flat2413', cap=4, help=False,
              camas=X('1 cama de casal + 2 camas de solteiro', '1 double bed + 2 single beds', '1 cama doble + 2 camas individuales'),
              fotos={'hero': 'f2413-hero', 'sala': 'f2413-a1', 'quarto': 'f2413-a2', 'cozinha': 'f2413-coz'}),
 '1313': dict(tipo='flat', andar=13, acesso='chave', rede='cristal', senha_wifi='crystal@2022', cap=4, help=False,
              camas=X('1 cama de casal + 2 camas de solteiro', '1 double bed + 2 single beds', '1 cama doble + 2 camas individuales'),
              fotos={'hero': 'f2413-hero', 'sala': 'f2413-a1', 'quarto': 'f2413-a2', 'cozinha': 'f2413-coz'}),
 '911':  dict(tipo='suite', andar=9, acesso='senha', senha='121345*', rede='Flat0911', senha_wifi='flat0911', cap=3, help=False,
              camas=X('1 cama queen + 1 sofá-cama', '1 queen bed + 1 sofa bed', '1 cama queen + 1 sofá cama'),
              fotos={'hero': 's911-hero', 'quarto': 's911-a1', 'sala': 's911-a2', 'banheiro': 's911-ban', 'cozinha': 's911-coz'}),
 '209':  dict(tipo='suite', andar=2, acesso='senha', senha='2209*', rede='AP-209', senha_wifi='flat0209', cap=3, help=True,
              camas=X('1 cama queen + 1 sofá-cama', '1 queen bed + 1 sofa bed', '1 cama queen + 1 sofá cama'),
              fotos={'hero': 's209-hero', 'sala': 's209-a1', 'sofa': 's209-a2', 'banheiro': 's209-ban', 'cozinha': 's209-coz', 'alavie': 's209-alavie'}),
}
PREDIO_FOTOS = {'fachada': 'fachada', 'lobby': 'lobby', 'piscina': 'piscina', 'academia': 'academia', 'mercado': 'mercado'}

def ordinal(n, L): return {'pt': f'{n}º andar', 'en': f'{n}{"st" if n % 10 == 1 and n != 11 else "nd" if n % 10 == 2 and n != 12 else "rd" if n % 10 == 3 and n != 13 else "th"} floor', 'es': f'piso {n}'}[L]

def conteudo(n, U, L):
    sui = U['tipo'] == 'suite'
    x = lambda pt, en, es: {'pt': pt, 'en': en, 'es': es}[L]
    nome = x(f'Suíte do Imperador {n}', f'Emperor Suite {n}', f'Suite del Emperador {n}') if sui else x(f'Flat {n}', f'Flat {n}', f'Flat {n}')
    ape = x('a suíte', 'the suite', 'la suite') if sui else x('o apartamento', 'the flat', 'el departamento')
    Ape = ape[0].upper() + ape[1:]
    andar = ordinal(U['andar'], L)
    cap = U['cap']; camas = U['camas'][L]
    T = {}

    # ---------- check-in
    T['checkin'] = dict(titulo=x('Check-in online e vistoria', 'Online check-in and inspection', 'Check-in online e inspección'),
      sub=x('Dois minutos, e a sua entrada está liberada', 'Two minutes, and your entry is cleared', 'Dos minutos y tu entrada queda liberada'),
      lead=x('O check-in online é obrigatório: é dele que sai o cadastro dos hóspedes na recepção do Crystal Place.',
             'The online check-in is mandatory: it is what registers the guests at the Crystal Place front desk.',
             'El check-in online es obligatorio: de él sale el registro de los huéspedes en la recepción del Crystal Place.'),
      btnTermo=x('Preencher o check-in online', 'Fill in the online check-in', 'Completar el check-in online'),
      vistH=x('Vistoria de chegada', 'Arrival inspection', 'Inspección de llegada'),
      vistP=x('Encontrou alguma coisa fora do lugar? Marque aqui nas primeiras horas. É isso que protege você de ser cobrado por um dano que já existia. <b>Não enviar nada significa que estava tudo conforme.</b>',
              'Found something out of place? Tick it here in the first few hours. That protects you from being charged for damage that was already there. <b>Sending nothing means everything was fine.</b>',
              '¿Encontraste algo fuera de lugar? Márcalo aquí en las primeras horas. Eso te protege de cobros por daños que ya existían. <b>No enviar nada significa que todo estaba conforme.</b>'),
      vistItens=([x('Sala, sofá e móveis', 'Living area, sofa and furniture', 'Sala, sofá y muebles'),
                  x('Cama, roupa de cama e travesseiros', 'Bed, bedding and pillows', 'Cama, ropa de cama y almohadas'),
                  x('Toalhas e amenities', 'Towels and toiletries', 'Toallas y amenities')] if sui else
                 [x('Sala e móveis', 'Living area and furniture', 'Sala y muebles'),
                  x('Camas, roupa de cama e armários', 'Beds, bedding and wardrobes', 'Camas, ropa de cama y armarios')]) +
                [x('Banheiro, chuveiro e descarga', 'Bathroom, shower and flush', 'Baño, ducha y descarga'),
                 x('Cozinha, eletros e utensílios', 'Kitchen, appliances and utensils', 'Cocina, electrodomésticos y utensilios')] +
                ([x('Taças, talheres e louças', 'Glasses, cutlery and dishes', 'Copas, cubiertos y vajilla')] if sui else []) +
                [x('TV, ar-condicionado e Wi-Fi', 'TV, air conditioning and Wi-Fi', 'TV, aire acondicionado y wifi'),
                 x('Janelas, portas e maçanetas', 'Windows, doors and handles', 'Ventanas, puertas y manijas')],
      vistPh=x('Descreva o que encontrou (opcional)', 'Describe what you found (optional)', 'Describe lo que encontraste (opcional)'),
      vistBtn=x('Enviar a vistoria pelo WhatsApp', 'Send the inspection on WhatsApp', 'Enviar la inspección por WhatsApp'),
      vistNota=x('Reforce com fotos pelo WhatsApp logo depois de enviar — o horário fica registrado e garante a sua proteção.',
                 'Add photos on WhatsApp right after sending — the time is recorded and protects you.',
                 'Refuerza con fotos por WhatsApp justo después de enviar: el horario queda registrado y te protege.'),
      blocos=[dict(dest=True, pill=x('faça agora', 'do it now', 'hazlo ahora'), h=x('Por que é obrigatório', 'Why it is mandatory', 'Por qué es obligatorio'),
        p=[x('A recepção confere o seu nome na lista de hóspedes, que vem do check-in online. Sem esse cadastro, <b>a entrada não é liberada</b>. É também exigência legal para hospedagem por temporada.',
             'The front desk checks your name against the guest list, which comes from the online check-in. Without it, <b>entry is not cleared</b>. It is also a legal requirement for short-term stays.',
             'La recepción confirma tu nombre en la lista de huéspedes, que sale del check-in online. Sin ese registro, <b>la entrada no se libera</b>. También es exigencia legal para alquileres temporarios.'),
           x('<b>Todos os hóspedes</b> precisam constar, inclusive quem chegar depois do titular.',
             '<b>Every guest</b> must be listed, including anyone arriving after the main guest.',
             '<b>Todos los huéspedes</b> deben figurar, incluso quien llegue después del titular.')])])

    # ---------- chegar
    T['chegar'] = dict(titulo=x('Como chegar', 'Getting here', 'Cómo llegar'),
      sub=x('Endereço, mapa e manobrista', 'Address, map and valet', 'Dirección, mapa y valet'),
      lead=x('O Crystal Place fica no Setor Pedro Ludovico, em frente ao Parque Areião e a poucos minutos do Setor Marista.',
             'Crystal Place is in Setor Pedro Ludovico, across from Parque Areião and a few minutes from Setor Marista.',
             'El Crystal Place está en el Setor Pedro Ludovico, frente al Parque Areião y a pocos minutos del Setor Marista.'),
      btnMapa=x('Abrir no Google Maps', 'Open in Google Maps', 'Abrir en Google Maps'),
      blocos=[dict(foto='fachada', h=x('Endereço', 'Address', 'Dirección'),
                   p=['<b>Condomínio Crystal Place</b><br>Av. Edmundo P. de Abreu, 31 — Setor Pedro Ludovico<br>Goiânia / GO']),
              dict(h=x('Do aeroporto', 'From the airport', 'Desde el aeropuerto'),
                   p=[x('Cerca de <b>20 minutos</b> de carro (9 km), pela Av. 85 ou pela Av. T-7, sentido Setor Marista.',
                        'About <b>20 minutes</b> by car (9 km), via Av. 85 or Av. T-7 towards Setor Marista.',
                        'Unos <b>20 minutos</b> en auto (9 km), por la Av. 85 o la Av. T-7, sentido Setor Marista.')]),
              dict(h=x('Do Centro', 'From downtown', 'Desde el centro'),
                   p=[x('Cerca de <b>15 minutos</b> (7 km), sentido sul pela Av. Anhanguera ou pela Marginal Botafogo.',
                        'About <b>15 minutes</b> (7 km), heading south on Av. Anhanguera or Marginal Botafogo.',
                        'Unos <b>15 minutos</b> (7 km), hacia el sur por la Av. Anhanguera o la Marginal Botafogo.')]),
              dict(h=x('De aplicativo', 'By ride app', 'En aplicación'),
                   p=[x('Uber e 99 encontram o Crystal Place pelo nome. A recepção funciona <b>24 horas</b>.',
                        'Uber and 99 find Crystal Place by name. The front desk is open <b>24 hours</b>.',
                        'Uber y 99 encuentran el Crystal Place por el nombre. La recepción funciona <b>las 24 horas</b>.')])])

    # ---------- prédio
    acessa = {'cartao': x('o seu cartão magnético', 'your key card', 'tu tarjeta magnética'),
              'chave': x('a chave do apartamento', 'the flat key', 'la llave del departamento'),
              'senha': None}[U['acesso']]
    T['predio'] = dict(titulo=x('Entrar no prédio', 'Entering the building', 'Entrar al edificio'),
      sub=x('Recepção 24h', '24-hour front desk', 'Recepción 24 h'),
      lead=x(f'A recepção do Crystal Place funciona dia e noite. Ao chegar, identifique-se como <b>hóspede da unidade {n}</b>.',
             f'The Crystal Place front desk is open day and night. When you arrive, say you are a <b>guest of unit {n}</b>.',
             f'La recepción del Crystal Place funciona día y noche. Al llegar, identifícate como <b>huésped de la unidad {n}</b>.'),
      blocos=[dict(pill=x('Na chegada', 'On arrival', 'Al llegar'), h=x('Documento com foto', 'Photo ID', 'Documento con foto'),
                   p=[x('Apresente um <b>documento com foto</b>. A recepção confere o seu nome na lista que vem do check-in online.',
                        'Show a <b>photo ID</b>. The front desk checks your name against the list from the online check-in.',
                        'Presenta un <b>documento con foto</b>. La recepción confirma tu nombre en la lista que viene del check-in online.')] +
                     ([x(f'É ali mesmo que você recebe {acessa}.', f'That is where you get {acessa}.', f'Ahí mismo recibes {acessa}.')] if acessa else
                      [x('O acesso à suíte é por senha — você sobe direto, sem nada para retirar.', 'The suite opens with a code — you go straight up, with nothing to pick up.',
                         'La suite se abre con clave: subes directo, sin nada que retirar.')])),
              dict(foto='lobby', h=x('A recepção', 'The front desk', 'La recepción'),
                   p=[x('Equipe disponível 24 horas para o que você precisar durante a estadia.', 'Staff available 24 hours for anything you need during your stay.',
                        'Equipo disponible las 24 horas para lo que necesites durante la estadía.')]),
              dict(dest=True, h=x('Visitas não são permitidas', 'No visitors', 'No se permiten visitas'),
                   p=[x('Só entram no prédio os hóspedes cadastrados no check-in online.', 'Only guests registered in the online check-in may enter the building.',
                        'Solo entran al edificio los huéspedes registrados en el check-in online.')])])

    # ---------- porta
    if U['acesso'] == 'senha':
        s = U['senha']; dig = s.rstrip('*')
        dica911 = n == '911'
        T['porta'] = dict(titulo=x('Entrar na suíte', 'Getting into the suite', 'Entrar a la suite'),
          sub=x(f'{andar} · senha da porta', f'{andar} · door code', f'{andar} · clave de la puerta'),
          lead=x(f'Do lobby, suba pelo elevador até o {andar}. A suíte {n} fica <b>à direita do elevador</b>.',
                 f'From the lobby, take the lift to the {andar}. Suite {n} is <b>to the right of the lift</b>.',
                 f'Desde el lobby, sube en ascensor al {andar}. La suite {n} está <b>a la derecha del ascensor</b>.'),
          blocos=[dict(dest=True, h=x('A senha da porta', 'The door code', 'La clave de la puerta'),
                       p=[x('A porta tem fechadura digital.', 'The door has a digital lock.', 'La puerta tiene cerradura digital.')], chave=s),
                  dict(h=x('O asterisco faz parte', 'The asterisk is part of it', 'El asterisco es parte de la clave'),
                       p=[x(f'Toque no teclado para acendê-lo, digite <b>{dig}</b> e finalize com o <b>asterisco (*)</b> — é ele que confirma.',
                            f'Touch the keypad to wake it, type <b>{dig}</b> and finish with the <b>asterisk (*)</b> — that is what confirms it.',
                            f'Toca el teclado para encenderlo, marca <b>{dig}</b> y termina con el <b>asterisco (*)</b>: es lo que confirma.'),
                          x('Se errar, espere alguns segundos e comece de novo, do zero.', 'If you get it wrong, wait a few seconds and start again from the beginning.',
                            'Si te equivocas, espera unos segundos y empieza de nuevo desde cero.')])] +
                 ([dict(dest=True, pill=x('atenção', 'heads-up', 'atención'), h=x('Puxe a porta enquanto digita', 'Pull the door while you type', 'Tira de la puerta mientras marcas'),
                        p=[x('A porta é pesada: <b>puxe-a para o seu lado enquanto digita</b> a senha. Você vai ouvir a fechadura rodando. Sem puxar, o trinco não gira por causa do peso da porta.',
                             'The door is heavy: <b>pull it towards you while you type</b> the code. You will hear the lock turn. Without pulling, the bolt cannot turn because of the weight of the door.',
                             'La puerta es pesada: <b>tírala hacia ti mientras marcas</b> la clave. Vas a oír girar la cerradura. Sin tirar, el pestillo no gira por el peso de la puerta.')])] if dica911 else []) +
                 [dict(h=x('Ao sair', 'When you go out', 'Al salir'),
                       p=[x('A porta trava ao ser fechada. Confira se ficou bem fechada sempre que sair.', 'The door locks when closed. Make sure it is properly shut every time you leave.',
                            'La puerta se traba al cerrarse. Verifica que quedó bien cerrada cada vez que salgas.')])])
    else:
        cartao = U['acesso'] == 'cartao'
        obj = x('cartão magnético', 'key card', 'tarjeta magnética') if cartao else x('chave', 'key', 'llave')
        T['porta'] = dict(titulo=x('Entrar no apartamento', 'Getting into the flat', 'Entrar al departamento'),
          sub=x(f'{andar} · {obj}', f'{andar} · {obj}', f'{andar} · {obj}'),
          lead=x(f'Do lobby, suba pelo elevador até o {andar}. O apartamento é o {n}.',
                 f'From the lobby, take the lift to the {andar}. The flat is number {n}.',
                 f'Desde el lobby, sube en ascensor al {andar}. El departamento es el {n}.'),
          blocos=[dict(dest=True, h=(x('Cartão magnético na recepção', 'Key card at the front desk', 'Tarjeta magnética en la recepción') if cartao else
                                     x('Chave na recepção', 'Key at the front desk', 'Llave en la recepción')),
                       p=[x(f'O acesso é feito com {"cartão magnético, confeccionado" if cartao else "chave, retirada"} na recepção (24h), depois do check-in online. Identifique-se como hóspede da unidade <b>{n}</b>.',
                            f'Access is by {"key card, issued" if cartao else "key, collected"} at the front desk (24h) after the online check-in. Say you are a guest of unit <b>{n}</b>.',
                            f'El acceso es con {"tarjeta magnética, hecha" if cartao else "llave, retirada"} en la recepción (24 h), después del check-in online. Identifícate como huésped de la unidad <b>{n}</b>.')]),
                  dict(h=x('Cuide bem dele' if cartao else 'Cuide bem dela', 'Keep it safe', 'Cuídala bien'),
                       p=[x(f'{"O cartão" if cartao else "A chave"} fica com você durante toda a estadia e é devolvid{"o" if cartao else "a"} na recepção no check-out. Em caso de perda, há custo de reposição.',
                            f'The {obj} stays with you for the whole stay and goes back to the front desk at check-out. If it is lost, there is a replacement cost.',
                            f'La {obj} queda contigo toda la estadía y se devuelve en la recepción en el check-out. En caso de pérdida, hay costo de reposición.')])])

    # ---------- o apê
    if sui:
        fotos_ape = [dict(foto='quarto' if 'quarto' in U['fotos'] else 'sala', h=x('O ambiente', 'The space', 'El ambiente'),
                          p=[x('Uma suíte Super Luxo pensada nos detalhes: o conforto de um hotel cinco estrelas com a privacidade de casa.',
                               'A Super Luxury suite designed down to the details: five-star comfort with the privacy of home.',
                               'Una suite Súper Lujo pensada en los detalles: el confort de un hotel cinco estrellas con la privacidad de casa.')]),
                     dict(foto='sala' if 'quarto' in U['fotos'] else 'sofa', h=x('Onde dormir', 'Sleeping', 'Dónde dormir'),
                          p=[x(f'<b>{camas}</b> — até <b>{cap} pessoas</b>.', f'<b>{camas}</b> — up to <b>{cap} guests</b>.', f'<b>{camas}</b>: hasta <b>{cap} personas</b>.')])]
        inclui = [x('<b>Roupa de cama premium</b> — jogo completo, travesseiros, edredom e fronhas', '<b>Premium bedding</b> — full set, pillows, duvet and pillowcases', '<b>Ropa de cama premium</b>: juego completo, almohadas, edredón y fundas'),
                  x('<b>Enxoval de banho</b> para toda a estadia', '<b>Bath towels</b> for the whole stay', '<b>Toallas de baño</b> para toda la estadía'),
                  x('<b>Amenities</b> — shampoo, condicionador e sabonete líquido', '<b>Toiletries</b> — shampoo, conditioner and liquid soap', '<b>Amenities</b>: champú, acondicionador y jabón líquido'),
                  x('<b>Smart TV</b> com aplicativos de streaming e Wi-Fi', '<b>Smart TV</b> with streaming apps and Wi-Fi', '<b>Smart TV</b> con aplicaciones de streaming y wifi'),
                  x('<b>Ar-condicionado</b>, com controle na suíte', '<b>Air conditioning</b>, remote in the suite', '<b>Aire acondicionado</b>, con control en la suite')]
    else:
        fotos_ape = [dict(foto='sala', h=x('O ambiente', 'The space', 'El ambiente'),
                          p=[x('Um flat completo, para uma estadia confortável — a trabalho, em família ou a passeio.',
                               'A complete flat for a comfortable stay — for work, with family or on holiday.',
                               'Un flat completo para una estadía cómoda: por trabajo, en familia o de paseo.')]),
                     dict(foto='quarto', h=x('Onde dormir', 'Sleeping', 'Dónde dormir'),
                          p=[x(f'<b>{camas}</b> — até <b>{cap} pessoas</b>.', f'<b>{camas}</b> — up to <b>{cap} guests</b>.', f'<b>{camas}</b>: hasta <b>{cap} personas</b>.')])]
        inclui = [x('<b>Roupa de cama e banho</b> — jogo de cama, travesseiros e toalhas', '<b>Bed and bath linen</b> — bedding, pillows and towels', '<b>Ropa de cama y baño</b>: juego de cama, almohadas y toallas'),
                  x('<b>Smart TV</b> e Wi-Fi durante toda a estadia', '<b>Smart TV</b> and Wi-Fi throughout your stay', '<b>Smart TV</b> y wifi durante toda la estadía'),
                  x('<b>Ar-condicionado</b> nos ambientes principais', '<b>Air conditioning</b> in the main rooms', '<b>Aire acondicionado</b> en los ambientes principales'),
                  x('<b>Itens de cortesia</b> — sabonete, shampoo e água', '<b>Courtesy items</b> — soap, shampoo and water', '<b>Artículos de cortesía</b>: jabón, champú y agua')]
    T['ape'] = dict(titulo=Ape,
      sub=(x('Suíte Super Luxo', 'Super Luxury suite', 'Suite Súper Lujo') if sui else x('1 quarto', '1 bedroom', '1 dormitorio')) + ' · ' +
          x(f'até {cap} hóspedes', f'up to {cap} guests', f'hasta {cap} huéspedes') + ' · 220V',
      lead=x(f'{"A suíte" if sui else "O apartamento"} chega pront{"a" if sui else "o"} para morar: não precisa trazer nada além das malas.',
             f'The {"suite" if sui else "flat"} is ready to live in: bring nothing but your luggage.',
             f'{"La suite llega lista" if sui else "El departamento llega listo"} para vivir: no hace falta traer nada más que las valijas.'),
      blocos=fotos_ape + [
        dict(h=x('O que já está incluído', 'Already included', 'Lo que ya está incluido'), ul=inclui),
        dict(dest=True, h=x('Não fornecemos', 'Not provided', 'No proveemos'),
             p=[x('<b>Café, açúcar, sal e óleo</b> não estão incluídos. O mercadinho do mezanino resolve os esquecidos de última hora.',
                  '<b>Coffee, sugar, salt and cooking oil</b> are not included. The mini-market on the mezzanine covers last-minute needs.',
                  '<b>Café, azúcar, sal y aceite</b> no están incluidos. El minimercado del entrepiso resuelve lo de último momento.')]),
        dict(h=x('Wi-Fi', 'Wi-Fi', 'Wifi'),
             p=[x(f'Rede <b>{U["rede"]}</b> · senha <b>{U["senha_wifi"]}</b>. A senha também está no cartão do topo do guia — toque para copiar.',
                  f'Network <b>{U["rede"]}</b> · password <b>{U["senha_wifi"]}</b>. It is also on the card at the top of the guide — tap to copy.',
                  f'Red <b>{U["rede"]}</b> · clave <b>{U["senha_wifi"]}</b>. También está en la tarjeta del inicio de la guía: toca para copiar.')]),
        dict(h=x('Tomadas', 'Outlets', 'Enchufes'),
             p=[x('<b>220V</b> — confira a voltagem dos seus aparelhos antes de ligar.', '<b>220V</b> — check your devices before plugging in.',
                  '<b>220 V</b>: revisa el voltaje de tus aparatos antes de enchufar.')])])
    if sui:
        T['ape']['blocos'].append(dict(**({'foto': 'alavie'} if 'alavie' in U['fotos'] else {}),
          pill=x('parceria', 'partner', 'alianza'), h=x('Aromatização Alavie', 'Scented by Alavie', 'Aromatización Alavie'),
          p=[x('A assinatura olfativa da suíte é da <b>Alavie</b>, casa goiana de perfumaria autoral. A composição <b>VIE</b>, com notas de bambu e chá branco, foi escolhida para criar memória afetiva da sua estadia.',
               'The suite’s signature scent is by <b>Alavie</b>, an independent perfume house from Goiânia. The <b>VIE</b> blend, with notes of bamboo and white tea, was chosen to make your stay memorable.',
               'La firma olfativa de la suite es de <b>Alavie</b>, casa de perfumería de autor de Goiânia. La composición <b>VIE</b>, con notas de bambú y té blanco, fue elegida para crear memoria afectiva de tu estadía.'),
             x('Gostou? A fragrância está à venda direto com a marca: <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.',
               'Liked it? The fragrance is sold directly by the brand: <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.',
               '¿Te gustó? La fragancia se vende directo con la marca: <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.')]))

    # ---------- cozinha
    T['cozinha'] = dict(titulo=x('A cozinha', 'The kitchen', 'La cocina'), sub=x('Equipada para cozinhar', 'Equipped for cooking', 'Equipada para cocinar'),
      lead=x('Dá para preparar as refeições do dia a dia sem sair de casa.', 'You can cook your everyday meals without going out.', 'Puedes preparar las comidas del día sin salir.'),
      blocos=[dict(foto='cozinha', h=x('O que tem', 'What there is', 'Qué hay'),
                   ul=[x('<b>Geladeira</b>', '<b>Fridge</b>', '<b>Heladera</b>'), x('<b>Fogão / cooktop</b>', '<b>Stove / cooktop</b>', '<b>Cocina / anafe</b>'),
                       x('<b>Micro-ondas</b>', '<b>Microwave</b>', '<b>Microondas</b>'),
                       x('Utensílios básicos para preparo e refeições', 'Basic utensils for cooking and eating', 'Utensilios básicos para cocinar y comer')] +
                      ([x('Talheres, copos, <b>taças de vinho</b> e pratos — do café da manhã ao jantar a dois', 'Cutlery, glasses, <b>wine glasses</b> and plates — from breakfast to dinner for two',
                          'Cubiertos, vasos, <b>copas de vino</b> y platos: del desayuno a la cena para dos')] if sui else [])),
              dict(h=x('O lixo', 'Rubbish', 'La basura'),
                   p=[x('Descarte o lixo ensacado conforme a orientação da recepção. Não deixe sacos no corredor.',
                        'Bag your rubbish and dispose of it as the front desk advises. Do not leave bags in the corridor.',
                        'Desecha la basura en bolsas según indique la recepción. No dejes bolsas en el pasillo.')])])

    # ---------- economizador HELP Smart
    if U['help']:
        lugar = x('a suíte', 'the suite', 'la suite') if sui else x('o apartamento', 'the flat', 'el departamento')
        T['economia'] = dict(titulo=x('Economizador de energia', 'Energy saver', 'Ahorrador de energía'),
          sub=x('Entrou? Toque na botoeira', 'Came in? Tap the button', '¿Entraste? Toca el botón'),
          lead=x(f'{lugar[0].upper()+lugar[1:]} tem o <b>HELP Smart</b>: desliga sozinho o ar-condicionado e as luzes quando fica vazi{"a" if sui else "o"}.',
                 f'{lugar[0].upper()+lugar[1:]} has <b>HELP Smart</b>: it switches the air conditioning and lights off on its own when nobody is in.',
                 f'{lugar[0].upper()+lugar[1:]} tiene <b>HELP Smart</b>: apaga solo el aire acondicionado y las luces cuando queda vací{"a" if sui else "o"}.'),
          blocos=[dict(dest=True, h=x('Entrou e fechou a porta? Toque na botoeira', 'Closed the door? Tap a button', '¿Cerraste la puerta? Toca un botón'),
                       p=[x('A botoeira é um <b>botão redondo branco</b> na parede. Ao tocar, o anel acende em <b>azul</b> — pronto, o sistema sabe que tem gente em casa.',
                            'The button is a <b>round white button</b> on the wall. When you tap it, its ring lights up <b>blue</b> — the system now knows someone is home.',
                            'El botón es <b>redondo y blanco</b>, en la pared. Al tocarlo, el anillo se enciende en <b>azul</b>: el sistema sabe que hay alguien.')]),
                  dict(h=x('Passo a passo', 'Step by step', 'Paso a paso'),
                       ul=[x('<b>Entre e feche a porta</b> — o sensor da porta avisa o sistema.', '<b>Come in and close the door</b> — the door sensor tells the system.', '<b>Entra y cierra la puerta</b>: el sensor de la puerta avisa al sistema.'),
                           x('<b>Toque em qualquer botoeira</b> — o anel acende em azul.', '<b>Tap any button</b> — the ring lights up blue.', '<b>Toca cualquier botón</b>: el anillo se enciende en azul.'),
                           x('<b>Aproveite</b> — ar e luzes funcionam normalmente.', '<b>Enjoy</b> — air and lights work as usual.', '<b>Disfruta</b>: el aire y las luces funcionan normalmente.'),
                           x('<b>Saiu e voltou? Toque de novo</b> — a cada abre-e-fecha da porta o sistema pede um novo toque.', '<b>Went out and came back? Tap again</b> — every time the door opens and closes, it asks for a new tap.', '<b>¿Saliste y volviste? Toca de nuevo</b>: cada vez que la puerta se abre y se cierra, pide otro toque.'),
                           x('<b>Ao ir embora, só feche a porta</b> — sem toque, o sistema desliga tudo sozinho.', '<b>When you leave, just close the door</b> — with no tap, it switches everything off.', '<b>Al irte, solo cierra la puerta</b>: sin toque, el sistema apaga todo solo.')]),
                  dict(h=x('Onde ficam as 3 botoeiras', 'Where the 3 buttons are', 'Dónde están los 3 botones'),
                       p=[x('Perto da porta de entrada, ao lado da cama e no banheiro. Qualquer uma serve — a dica é tocar na da entrada logo depois de fechar a porta.',
                            'Near the front door, next to the bed and in the bathroom. Any of them works — tip: tap the one by the door right after closing it.',
                            'Cerca de la puerta de entrada, al lado de la cama y en el baño. Cualquiera sirve: el consejo es tocar el de la entrada apenas cierres la puerta.')]),
                  dict(h=x('O ar ou as luzes desligaram sozinhos?', 'Air or lights switched off by themselves?', '¿El aire o las luces se apagaron solos?'),
                       p=[x('Não é defeito: provavelmente a botoeira não foi tocada depois de fechar a porta. Toque em qualquer uma e veja o anel acender em azul. Se o ar não voltar, ligue de novo pelo controle remoto.',
                            'It is not a fault: most likely no button was tapped after the door closed. Tap any one and watch the ring light up blue. If the air does not come back, switch it on again with the remote.',
                            'No es una falla: probablemente no se tocó el botón después de cerrar la puerta. Toca cualquiera y mira cómo se enciende el anillo azul. Si el aire no vuelve, enciéndelo de nuevo con el control.'),
                          x('Por que isso existe? Para o ar nunca ficar ligado com o imóvel vazio — economiza energia, sem mudar nada no seu conforto.',
                            'Why? So the air conditioning is never left running in an empty unit — it saves energy without changing your comfort.',
                            '¿Por qué existe? Para que el aire nunca quede encendido con la unidad vacía: ahorra energía sin cambiar tu confort.')])])

    # ---------- garagem (manobrista)
    T['garagem'] = dict(titulo=x('Estacionamento', 'Parking', 'Estacionamiento'),
      sub=x('Manobrista 24h · incluso', '24h valet · included', 'Valet 24 h · incluido'),
      lead=x('O Crystal Place tem manobrista bilíngue 24 horas, já incluído na sua hospedagem — você não paga nada a mais.',
             'Crystal Place has a bilingual valet 24 hours a day, included in your stay — nothing extra to pay.',
             'El Crystal Place tiene valet bilingüe las 24 horas, incluido en tu estadía: no pagas nada extra.'),
      blocos=[dict(dest=True, h=x('Sem vaga numerada', 'No numbered space', 'Sin plaza numerada'),
                   p=[x('É só entregar o carro na entrada do prédio. O manobrista cuida de estacionar e de trazer o veículo de volta quando você pedir.',
                        'Just hand over the car at the building entrance. The valet parks it and brings it back whenever you ask.',
                        'Solo entrega el auto en la entrada del edificio. El valet lo estaciona y lo trae de vuelta cuando lo pidas.')]),
              dict(h=x('No dia da saída', 'On departure day', 'El día de la salida'),
                   p=[x('Peça o carro ao manobrista com alguns minutos de antecedência.', 'Ask the valet for your car a few minutes ahead.', 'Pide el auto al valet con algunos minutos de anticipación.')])])

    # ---------- lazer
    T['lazer'] = dict(titulo=x('Lazer no mezanino', 'Leisure on the mezzanine', 'Ocio en el entrepiso'),
      sub=x('Piscina aquecida, sauna e academia', 'Heated pool, sauna and gym', 'Piscina climatizada, sauna y gimnasio'),
      lead=x('O Crystal Place tem estrutura de lazer e serviços no mezanino, com acesso mediante cadastro na recepção.',
             'Crystal Place has leisure facilities and services on the mezzanine, accessed through registration at the front desk.',
             'El Crystal Place tiene áreas de ocio y servicios en el entrepiso, con acceso mediante registro en la recepción.'),
      blocos=[dict(foto='piscina', h=x('Piscina aquecida', 'Heated pool', 'Piscina climatizada'),
                   p=[x('Climatizada, aberta no horário de funcionamento do lazer.', 'Heated, open during leisure-area hours.', 'Climatizada, abierta en el horario del área de ocio.')]),
              dict(foto='academia', h=x('Academia e sauna', 'Gym and sauna', 'Gimnasio y sauna'),
                   p=[x('Equipamentos para o treino durante a estadia, e a sauna para relaxar depois do dia.', 'Equipment for your workout during the stay, and the sauna to unwind after the day.',
                        'Equipos para entrenar durante la estadía y la sauna para relajarte después del día.')]),
              dict(foto='mercado', h=x('Mercadinho e salão de beleza', 'Mini-market and beauty salon', 'Minimercado y salón de belleza'),
                   p=[x('O mercadinho de conveniência resolve os esquecidos de última hora. O salão de beleza atende com hora marcada.',
                        'The convenience mini-market covers last-minute needs. The beauty salon works by appointment.',
                        'El minimercado resuelve lo de último momento. El salón de belleza atiende con turno.')]),
              dict(h=x('Horários', 'Opening hours', 'Horarios'),
                   p=[x('Os horários e regras de uso de cada espaço estão afixados na recepção — em caso de dúvida, é só perguntar.',
                        'Hours and rules for each area are posted at the front desk — just ask if in doubt.',
                        'Los horarios y reglas de cada espacio están en la recepción: ante cualquier duda, pregunta.')])])

    # ---------- regras
    T['regras'] = dict(titulo=x('Regras da casa', 'House rules', 'Reglas de la casa'),
      sub=x('Curtas, e todas por um motivo', 'Short, and each one for a reason', 'Cortas, y cada una por un motivo'),
      lead=x('São as mesmas que você aceitou no check-in online. Estão aqui para consulta.', 'They are the same ones you accepted in the online check-in, here for reference.',
             'Son las mismas que aceptaste en el check-in online. Están aquí para consulta.'),
      blocos=[dict(dest=True, pill=x('proibido', 'not allowed', 'prohibido'), h=x('🚭 Proibido fumar', '🚭 No smoking', '🚭 Prohibido fumar'),
                   p=[x(f'Em <b>nenhum ambiente</b> d{"a suíte" if sui else "o apartamento"} — inclusive na janela e no banheiro. Vale para cigarro comum, eletrônico (vape) e narguilé.',
                        f'<b>Anywhere</b> in the {"suite" if sui else "flat"} — including at the window and in the bathroom. This covers cigarettes, e-cigarettes (vapes) and hookah.',
                        f'En <b>ningún ambiente</b> de{"la suite" if sui else "l departamento"}, incluso en la ventana y en el baño. Vale para cigarrillo común, electrónico (vape) y narguile.'),
                      x('Multa de <b>R$ 300,00</b> mais o custo da higienização — o cheiro fica nos tecidos e prejudica o próximo hóspede.',
                        'Fine of <b>R$ 300.00</b> plus the cleaning cost — the smell stays in the fabrics and affects the next guest.',
                        'Multa de <b>R$ 300,00</b> más el costo de la higienización: el olor queda en las telas y perjudica al próximo huésped.')]),
              dict(dest=True, h=x('Visitas não são permitidas', 'No visitors', 'No se permiten visitas'),
                   p=[x('Só os hóspedes cadastrados no check-in online entram no prédio e no apartamento.', 'Only the guests registered in the online check-in may enter the building and the unit.',
                        'Solo los huéspedes registrados en el check-in online entran al edificio y a la unidad.')]),
              dict(h=x('Sem festas ou eventos', 'No parties or events', 'Sin fiestas ni eventos'),
                   p=[x('Multa de <b>R$ 500,00</b>, além dos danos que houver.', 'Fine of <b>R$ 500.00</b>, plus any damage.', 'Multa de <b>R$ 500,00</b>, además de los daños.')]),
              dict(h=x(f'Capacidade: {cap} pessoas', f'Capacity: {cap} guests', f'Capacidad: {cap} personas'),
                   p=[x(f'A capacidade máxima é de <b>{cap} hóspedes</b>. Hóspede excedente: <b>R$ 200,00</b> por pessoa.', f'Maximum <b>{cap} guests</b>. Each extra guest: <b>R$ 200.00</b>.',
                        f'La capacidad máxima es de <b>{cap} huéspedes</b>. Huésped excedente: <b>R$ 200,00</b> por persona.')]),
              dict(h=x('Silêncio das 22h às 8h', 'Quiet hours 10 pm to 8 am', 'Silencio de 22 h a 8 h'),
                   p=[x('Volume baixo em TV e conversas depois desse horário, também nas áreas comuns.', 'Keep TV and voices low after that time, in the common areas too.',
                        'Volumen bajo de TV y conversaciones después de ese horario, también en las áreas comunes.')]),
              dict(h=x('Animais de estimação', 'Pets', 'Mascotas'),
                   p=[x('Sob consulta — combine com a aluGO antes da reserva.', 'On request — check with aluGO before booking.', 'A consultar: coordina con aluGO antes de reservar.')]),
              dict(h=x('Horários', 'Times', 'Horarios'),
                   p=[x('Check-in a partir das <b>14h</b>, check-out até as <b>11h</b>. Não realizamos early check-in nem late check-out. Permanência além do horário: <b>R$ 200,00</b> por hora.',
                        'Check-in from <b>2 pm</b>, check-out by <b>11 am</b>. We do not offer early check-in or late check-out. Staying past check-out: <b>R$ 200.00</b> per hour.',
                        'Check-in desde las <b>14 h</b>, check-out hasta las <b>11 h</b>. No hacemos early check-in ni late check-out. Permanencia fuera de horario: <b>R$ 200,00</b> por hora.')]),
              dict(h=x('Eventuais danos', 'Accidental damage', 'Daños eventuales'),
                   p=[x('Aconteceu alguma coisa? Avise a aluGO o quanto antes — resolvemos juntos.', 'Something happened? Let aluGO know as soon as possible — we will sort it out together.',
                        '¿Pasó algo? Avisa a aluGO lo antes posible: lo resolvemos juntos.')])])

    # ---------- saída
    if U['acesso'] == 'senha':
        devol = dict(dest=True, h=x('Nada a devolver', 'Nothing to return', 'Nada que devolver'),
                     p=[x('O acesso é por senha: não há chave nem cartão para entregar na recepção. Só confira se a porta ficou bem fechada.',
                          'Access is by code: there is no key or card to hand in. Just make sure the door is properly shut.',
                          'El acceso es con clave: no hay llave ni tarjeta que entregar. Solo verifica que la puerta quedó bien cerrada.')])
    else:
        cartao = U['acesso'] == 'cartao'
        devol = dict(dest=True, h=(x('Devolva o cartão na recepção', 'Return the key card at the front desk', 'Devuelve la tarjeta en la recepción') if cartao else
                                   x('Devolva a chave na recepção', 'Return the key at the front desk', 'Devuelve la llave en la recepción')),
                     p=[x(f'A estadia só se encerra com {"o cartão" if cartao else "a chave"} de volta na recepção.', f'Your stay only ends once the {"key card" if cartao else "key"} is back at the front desk.',
                          f'La estadía solo termina con la {"tarjeta" if cartao else "llave"} de vuelta en la recepción.')])
    T['saida'] = dict(titulo=x('Ir embora', 'Leaving', 'Irse'), sub=x('Check-out até as 11h', 'Check-out by 11 am', 'Check-out hasta las 11 h'),
      lead=x('Temos uma nova reserva chegando logo depois, e a equipe de limpeza entra pontualmente às 11h.',
             'A new booking arrives right after you, and the cleaning team comes in at 11 am sharp.',
             'Llega una nueva reserva enseguida, y el equipo de limpieza entra puntualmente a las 11 h.'),
      coSelo=x('⚠ Antes de ir embora', '⚠ Before you leave', '⚠ Antes de irte'), coH=x('Confirme seu check-out', 'Confirm your check-out', 'Confirma tu check-out'),
      coP=x('É um toque só. É esse aviso que registra o encerramento da sua estadia e libera a nossa equipe de limpeza.',
            'One tap. This is what closes your stay and releases our cleaning team.', 'Es un solo toque. Este aviso cierra tu estadía y libera a nuestro equipo de limpieza.'),
      coBtn=x('Avisar meu check-out', 'Confirm my check-out', 'Avisar mi check-out'),
      blocos=[dict(h=x('Antes de sair', 'Before you go', 'Antes de salir'),
                   ul=[x('Desligar o ar-condicionado e as luzes', 'Switch off the air conditioning and lights', 'Apagar el aire acondicionado y las luces'),
                       x('Fechar bem janelas e portas', 'Close windows and doors properly', 'Cerrar bien ventanas y puertas'),
                       x('Conferir gavetas, banheiro, geladeira e tomadas — carregador some fácil', 'Check drawers, bathroom, fridge and sockets — chargers are easy to forget',
                         'Revisar cajones, baño, heladera y enchufes: el cargador se olvida fácil'),
                       x('Deixar a louça usada na pia (não precisa lavar)', 'Leave used dishes in the sink (no need to wash)', 'Dejar la vajilla usada en la pileta (no hace falta lavarla)'),
                       x('Descartar o lixo, se houver', 'Throw away any rubbish', 'Desechar la basura, si hay'),
                       x('Pedir o carro ao manobrista, se for o caso', 'Ask the valet for your car, if needed', 'Pedir el auto al valet, si corresponde')]),
              devol,
              dict(h=x('A recepção guarda as suas malas', 'The front desk keeps your bags', 'La recepción guarda tus valijas'),
                   p=[x('Vai embora mais tarde? Depois do check-out, deixe a bagagem com a recepção do Crystal Place e aproveite o resto do dia.',
                        'Leaving later? After check-out, leave your luggage with the Crystal Place front desk and enjoy the rest of the day.',
                        '¿Te vas más tarde? Después del check-out, deja el equipaje en la recepción del Crystal Place y aprovecha el resto del día.')]),
              dict(h=x('O check-out termina quando você sai do prédio', 'Check-out ends when you leave the building', 'El check-out termina cuando sales del edificio'),
                   p=[x('Pedimos que o grupo não permaneça nas áreas comuns depois do horário de saída.', 'Please do not stay on in the common areas after check-out time.',
                        'Pedimos que el grupo no permanezca en las áreas comunes después del horario de salida.')])])

    # ---------- bairro
    T['bairro'] = dict(titulo=x('Pedro Ludovico e Marista', 'Pedro Ludovico and Marista', 'Pedro Ludovico y Marista'),
      sub=x('Parque Areião em frente', 'Parque Areião across the street', 'Parque Areião enfrente'),
      lead=x('Uma das regiões mais bem servidas de Goiânia: em frente ao Parque Areião e a poucos minutos do Marista.',
             'One of the best-served areas of Goiânia: across from Parque Areião and a few minutes from Marista.',
             'Una de las zonas mejor servidas de Goiânia: frente al Parque Areião y a pocos minutos del Marista.'),
      blocos=[dict(h=x('Parque Areião · em frente ao prédio', 'Parque Areião · across the street', 'Parque Areião · enfrente del edificio'),
                   p=[x('250 mil m² de mata nativa, lago, pista de caminhada e ciclovia. Aberto todos os dias.', '250,000 m² of native woodland, a lake, walking track and cycle path. Open every day.',
                        '250 mil m² de bosque nativo, lago, pista para caminar y ciclovía. Abierto todos los días.')]),
              dict(h=x('Setor Marista · gastronomia', 'Setor Marista · food', 'Setor Marista · gastronomía'),
                   p=[x('Bistrôs autorais, casas de carnes, sushis e bares de boa cerveja. À noite, vale explorar a Rua T-25 e arredores.',
                        'Chef-led bistros, steakhouses, sushi and craft-beer bars. At night, Rua T-25 and around are worth exploring.',
                        'Bistrós de autor, parrillas, sushi y bares de buena cerveza. De noche vale recorrer la Rua T-25 y alrededores.')]),
              dict(h=x('Compras', 'Shopping', 'Compras'),
                   ul=[x('<b>Goiânia Shopping</b> — cerca de 8 min', '<b>Goiânia Shopping</b> — about 8 min', '<b>Goiânia Shopping</b>: unos 8 min'),
                       x('<b>Flamboyant Shopping</b> — cerca de 10 min', '<b>Flamboyant Shopping</b> — about 10 min', '<b>Flamboyant Shopping</b>: unos 10 min'),
                       x('Supermercados grandes a 5 minutos de carro', 'Large supermarkets 5 minutes away by car', 'Supermercados grandes a 5 minutos en auto')])])
    if not sui:
        T['bairro']['blocos'].append(dict(pill=x('indicação aluGO', 'aluGO pick', 'recomendación aluGO'), h='Alavie',
          p=[x('Casa goiana de perfumaria autoral, com fragrâncias que transformam um ambiente em atmosfera. A composição <b>VIE</b>, de bambu e chá branco, é um bom começo: <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.',
               'An independent perfume house from Goiânia, with fragrances that turn a room into an atmosphere. The <b>VIE</b> blend, bamboo and white tea, is a good place to start: <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.',
               'Casa de perfumería de autor de Goiânia, con fragancias que convierten un ambiente en atmósfera. La composición <b>VIE</b>, de bambú y té blanco, es un buen comienzo: <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.')]))

    # ---------- deu problema
    ac = []
    if U['acesso'] == 'senha':
        s = U['senha']; dig = s.rstrip('*')
        r = [x(f'Toque no teclado para acendê-lo, digite <b>{dig}</b> e finalize com o <b>asterisco (*)</b>.', f'Touch the keypad to wake it, type <b>{dig}</b> and finish with the <b>asterisk (*)</b>.',
               f'Toca el teclado para encenderlo, marca <b>{dig}</b> y termina con el <b>asterisco (*)</b>.')]
        if n == '911':
            r.append(x('<b>Puxe a porta para o seu lado enquanto digita</b> — sem puxar, o trinco não gira por causa do peso da porta.',
                       '<b>Pull the door towards you while you type</b> — without pulling, the bolt cannot turn because of the weight of the door.',
                       '<b>Tira de la puerta hacia ti mientras marcas</b>: sin tirar, el pestillo no gira por el peso de la puerta.'))
        r.append(x('Se o teclado não acender, a pilha pode estar fraca. Chame a gente — resolvemos na hora. Não force a porta.',
                   'If the keypad does not light up, the battery may be low. Message us — we will fix it right away. Do not force the door.',
                   'Si el teclado no se enciende, la pila puede estar baja. Escríbenos: lo resolvemos enseguida. No fuerces la puerta.'))
        ac.append(dict(q=x('A porta não abre', 'The door will not open', 'La puerta no abre'), r=r))
    else:
        cartao = U['acesso'] == 'cartao'
        ac.append(dict(q=x('O cartão não abre a porta' if cartao else 'A chave não gira', 'The key card does not open the door' if cartao else 'The key will not turn',
                           'La tarjeta no abre la puerta' if cartao else 'La llave no gira'),
                       r=[x('Desça à recepção (24h): a equipe confere e resolve na hora.', 'Go down to the front desk (24h): the team will check it and sort it out.',
                            'Baja a la recepción (24 h): el equipo lo revisa y lo resuelve enseguida.'),
                          x('Se não resolver, chame a gente no WhatsApp.', 'If that does not solve it, message us on WhatsApp.', 'Si no se resuelve, escríbenos por WhatsApp.')]))
    if U['help']:
        ac.append(dict(q=x('O ar ou as luzes desligaram sozinhos', 'The air or lights switched off by themselves', 'El aire o las luces se apagaron solos'),
                       r=[x('É o economizador HELP Smart: a botoeira não foi tocada depois de fechar a porta. Toque em qualquer botoeira e veja o anel acender em azul.',
                            'It is the HELP Smart energy saver: no button was tapped after the door closed. Tap any button and watch the ring light up blue.',
                            'Es el ahorrador HELP Smart: no se tocó el botón después de cerrar la puerta. Toca cualquier botón y mira cómo se enciende el anillo azul.'),
                          x('Se o ar não voltar sozinho, ligue de novo pelo controle remoto.', 'If the air does not come back, switch it on again with the remote.',
                            'Si el aire no vuelve solo, enciéndelo de nuevo con el control.')]))
    ac += [dict(q=x('O Wi-Fi caiu', 'The Wi-Fi is down', 'Se cayó el wifi'),
                r=[x(f'A rede é a <b>{U["rede"]}</b> e a senha está no cartão do topo do guia — toque nele para copiar.', f'The network is <b>{U["rede"]}</b> and the password is on the card at the top of the guide — tap it to copy.',
                     f'La red es <b>{U["rede"]}</b> y la clave está en la tarjeta del inicio de la guía: tócala para copiar.'),
                   x('Se não conectar, tire o roteador da tomada, espere 30 segundos e ligue de novo. Ele leva cerca de 2 minutos para voltar.',
                     'If it will not connect, unplug the router, wait 30 seconds and plug it back in. It takes about 2 minutes to come back.',
                     'Si no conecta, desenchufa el router, espera 30 segundos y vuelve a enchufarlo. Tarda unos 2 minutos en volver.')]),
           dict(q=x('O ar-condicionado não está gelando', 'The air conditioning is not cooling', 'El aire acondicionado no enfría'),
                r=[x('Confira se está no modo <b>refrigerar</b> (o floco de neve), com a temperatura abaixo de 23°C, e feche janela e cortina.',
                     'Check it is on <b>cool</b> mode (the snowflake), set below 23°C, and close the window and curtain.',
                     'Verifica que esté en modo <b>frío</b> (el copo de nieve), por debajo de 23 °C, y cierra ventana y cortina.'),
                   x('Se continuar, avise a gente.', 'If it still does not cool, let us know.', 'Si sigue igual, avísanos.')]),
           dict(q=x('Faltou alguma coisa', 'Something is missing', 'Falta algo'),
                r=[x('Chame a aluGO no WhatsApp — fazemos o possível para resolver na hora.', 'Message aluGO on WhatsApp — we will do our best to sort it out right away.',
                     'Escribe a aluGO por WhatsApp: hacemos lo posible para resolverlo enseguida.')])]
    T['problema'] = dict(titulo=x('Deu problema?', 'Something wrong?', '¿Algún problema?'), sub=x('Resolva em 30 segundos', 'Fix it in 30 seconds', 'Resuélvelo en 30 segundos'),
      lead=x('Quase tudo aqui se resolve sem esperar. Se não resolver, o WhatsApp está no fim desta tela e a gente responde rápido.',
             'Most things here can be fixed straight away. If not, WhatsApp is at the end of this screen and we reply fast.',
             'Casi todo aquí se resuelve sin esperar. Si no, el WhatsApp está al final de esta pantalla y respondemos rápido.'),
      btnZap=x('Falar com a gente no WhatsApp', 'Message us on WhatsApp', 'Hablar con nosotros por WhatsApp'), blocos=[], ac=ac)
    return T, nome

# ---------------------------------------------------------------- textos gerais (fora das telas)
def gerais(n, U, nome, L):
    x = lambda pt, en, es: {'pt': pt, 'en': en, 'es': es}[L]
    sui = U['tipo'] == 'suite'
    rot = f'Crystal Place {n}'
    G = dict(apeNome=nome, heroRot=x('Guia da estadia', 'Your stay guide', 'Guía de la estadía'), heroDesce=x('role para começar', 'scroll to start', 'desliza para empezar'),
      secaoMenu=x('O que você precisa saber', 'What you need to know', 'Lo que necesitas saber'),
      apeSub=x('Crystal Place · Setor Pedro Ludovico, Goiânia', 'Crystal Place · Setor Pedro Ludovico, Goiânia', 'Crystal Place · Setor Pedro Ludovico, Goiânia'),
      cSenha=x('Senha da porta', 'Door code', 'Clave de la puerta'),
      cSenhaSub=x('fechadura digital · o asterisco no final confirma', 'digital lock · the asterisk at the end confirms', 'cerradura digital · el asterisco al final confirma'),
      cAcesso=x('Seu acesso', 'Your access', 'Tu acceso'),
      cAcessoVal={'senha': x('Fechadura digital', 'Digital lock', 'Cerradura digital'), 'cartao': x('Cartão na recepção', 'Key card at reception', 'Tarjeta en recepción'),
                  'chave': x('Chave na recepção', 'Key at reception', 'Llave en recepción')}[U['acesso']],
      cAcessoSub=x('retire na recepção 24h', 'collect it at the 24h front desk', 'retírala en la recepción 24 h') if U['acesso'] != 'senha' else x('a senha chega junto com este guia', 'the code comes with this guide', 'la clave llega junto con esta guía'),
      cAcessoTap=x('toque para ver o passo a passo', 'tap for the steps', 'toca para ver el paso a paso'),
      cWifi=x('Senha do Wi-Fi', 'Wi-Fi password', 'Clave del Wi-Fi'), cWifiRede=x('rede:', 'network:', 'red:'), cWifiPend=x('peça pelo WhatsApp', 'ask us on WhatsApp', 'pídela por WhatsApp'),
      cHoras=x('Horários', 'Times', 'Horarios'), cHorasVal=x('14h / 11h', '2pm / 11am', '14h / 11h'),
      cHorasSub=x('entrada a partir das 14h · saída até as 11h', 'check-in from 2pm · check-out by 11am', 'entrada desde las 14h · salida hasta las 11h'),
      cTap=x('toque para copiar', 'tap to copy', 'toca para copiar'), copiado=x('copiado ✓', 'copied ✓', 'copiado ✓'),
      buscaPh=x('O que você procura? (wi-fi, piscina, manobrista…)', 'What are you looking for? (wi-fi, pool, valet…)', '¿Qué buscas? (wifi, piscina, valet…)'),
      buscaVazio=x('Não achamos essa palavra. Toque no WhatsApp na barra de baixo que a gente responde.', "We couldn't find that. Tap WhatsApp in the bar below and we'll answer.",
                   'No encontramos esa palabra. Toca WhatsApp en la barra de abajo y te respondemos.'),
      bMenu=x('Menu', 'Menu', 'Menú'), bCheckout='CHECK-OUT', bVoltar=x('Voltar ao menu', 'Back to menu', 'Volver al menú'),
      rodape=x('Gestão de imóveis para temporada', 'Short-stay property management', 'Gestión de inmuebles de temporada'),
      zapOi=x(f'Olá! Sou hóspede do {rot} e preciso de ajuda.', f"Hi! I'm a guest at {rot} and I need some help.", f'¡Hola! Soy huésped del {rot} y necesito ayuda.'),
      zapCheckout=x(f'Olá! Estou fazendo o check-out do {rot}. Já deixei {"a suíte" if sui else "o apartamento"}.', f"Hi! I'm checking out of {rot}. I've already left the {'suite' if sui else 'flat'}.",
                    f'¡Hola! Estoy haciendo el check-out del {rot}. Ya dejé {"la suite" if sui else "el departamento"}.'),
      vistVazio=x('Marque um item ou escreva uma observação antes de enviar.', 'Tick an item or write a note before sending.', 'Marca un ítem o escribe una observación antes de enviar.'),
      vistMsg=x(f'Vistoria de chegada — {rot}. Encontrei:', f'Arrival inspection — {rot}. I found:', f'Inspección de llegada — {rot}. Encontré:'),
      vistObs=x('Observações', 'Notes', 'Observaciones'))
    return G

SIN_BASE = {
 'pt': {'chegar': ['endereco', 'onde fica', 'mapa', 'uber', 'taxi', '99', 'localizacao', 'aeroporto', 'rodoviaria', 'edmundo', 'pedro ludovico', 'areiao'],
        'predio': ['portaria', 'recepcao', 'documento', 'rg', 'identidade', 'chegada', 'cadastro', 'visita', 'visitas', '24h'],
        'porta': ['senha', 'senha da porta', 'fechadura', 'asterisco', 'codigo', 'abrir a porta', 'como entro', 'cartao', 'chave', 'nao abre', 'andar', 'elevador'],
        'ape': ['wifi', 'wi-fi', 'rede', 'internet', 'senha do wifi', 'cama', 'sofa cama', 'toalha', 'enxoval', 'tv', 'ar condicionado', '220v', 'voltagem', 'tomada', 'cafe', 'acucar', 'alavie', 'perfume', 'aroma'],
        'cozinha': ['cozinha', 'geladeira', 'fogao', 'cooktop', 'micro-ondas', 'microondas', 'panela', 'prato', 'talher', 'taca', 'lixo'],
        'economia': ['economizador', 'help smart', 'botoeira', 'botao', 'ar desligou', 'luz apagou', 'desligou sozinho', 'energia', 'sensor'],
        'garagem': ['garagem', 'vaga', 'estacionamento', 'carro', 'manobrista', 'valet', 'estacionar'],
        'lazer': ['piscina', 'sauna', 'academia', 'mercadinho', 'mercado', 'salao de beleza', 'lazer', 'mezanino', 'horario da piscina'],
        'regras': ['regras', 'fumar', 'cigarro', 'vape', 'narguile', 'festa', 'barulho', 'silencio', 'pet', 'cachorro', 'gato', 'visita', 'multa', 'late checkout', 'early checkin'],
        'problema': ['problema', 'nao funciona', 'quebrou', 'defeito', 'ajuda', 'wifi caiu', 'ar nao gela'],
        'bairro': ['restaurante', 'bar', 'parque', 'areiao', 'marista', 'shopping', 'supermercado', 'farmacia', 'passeio', 'comer'],
        'checkin': ['check-in', 'checkin', 'termo', 'cadastro', 'vistoria', 'formulario', 'documento'],
        'saida': ['check-out', 'checkout', 'saida', 'ir embora', 'devolver', 'cartao', 'chave', 'malas', 'bagagem', 'guardar malas', '11h']},
 'en': {'chegar': ['address', 'where', 'map', 'uber', 'taxi', 'location', 'airport'], 'predio': ['front desk', 'reception', 'id', 'arrival', 'visitor', '24h'],
        'porta': ['code', 'door code', 'lock', 'asterisk', 'key card', 'key', 'open the door', 'floor', 'lift', 'elevator'],
        'ape': ['wifi', 'wi-fi', 'network', 'internet', 'password', 'bed', 'sofa bed', 'towel', 'tv', 'air conditioning', '220v', 'voltage', 'outlet', 'coffee', 'alavie', 'scent'],
        'cozinha': ['kitchen', 'fridge', 'stove', 'microwave', 'pan', 'plates', 'rubbish', 'trash'],
        'economia': ['energy saver', 'help smart', 'button', 'air switched off', 'lights off', 'sensor'],
        'garagem': ['parking', 'garage', 'car', 'valet'], 'lazer': ['pool', 'sauna', 'gym', 'market', 'salon', 'leisure'],
        'regras': ['rules', 'smoking', 'vape', 'party', 'noise', 'quiet', 'pet', 'dog', 'visitor', 'fine', 'late checkout'],
        'problema': ['problem', 'not working', 'broken', 'help'], 'bairro': ['restaurant', 'bar', 'park', 'shopping', 'supermarket', 'pharmacy'],
        'checkin': ['check-in', 'checkin', 'form', 'registration', 'inspection'], 'saida': ['check-out', 'checkout', 'leave', 'return', 'luggage', 'bags']},
 'es': {'chegar': ['direccion', 'donde', 'mapa', 'uber', 'taxi', 'ubicacion', 'aeropuerto'], 'predio': ['recepcion', 'porteria', 'documento', 'llegada', 'visita', '24 h'],
        'porta': ['clave', 'clave de la puerta', 'cerradura', 'asterisco', 'tarjeta', 'llave', 'abrir la puerta', 'piso', 'ascensor'],
        'ape': ['wifi', 'red', 'internet', 'cama', 'sofa cama', 'toalla', 'tv', 'aire acondicionado', '220v', 'voltaje', 'enchufe', 'cafe', 'alavie', 'aroma'],
        'cozinha': ['cocina', 'heladera', 'microondas', 'olla', 'platos', 'basura'],
        'economia': ['ahorrador', 'help smart', 'boton', 'se apago el aire', 'luces apagadas', 'sensor'],
        'garagem': ['cochera', 'garaje', 'estacionamiento', 'auto', 'valet'], 'lazer': ['piscina', 'sauna', 'gimnasio', 'minimercado', 'salon de belleza'],
        'regras': ['reglas', 'fumar', 'vape', 'fiesta', 'ruido', 'silencio', 'mascota', 'perro', 'visita', 'multa'],
        'problema': ['problema', 'no funciona', 'roto', 'ayuda'], 'bairro': ['restaurante', 'bar', 'parque', 'shopping', 'supermercado', 'farmacia'],
        'checkin': ['check-in', 'checkin', 'formulario', 'registro', 'inspeccion'], 'saida': ['check-out', 'checkout', 'salida', 'devolver', 'valijas', 'equipaje']},
}

ECO_TELA = ("  {id:'economia', corpo:function(d){ return (L==='pt' && typeof HS_HTML==='string' && HS_HTML) ? "
            "'<div class=\"hs-wrap\">'+HS_HTML+'</div>' : blocos(d); }},\n")

def gerar(n):
    U = UN[n]
    TXT = {}; nome_pt = None
    for L in LS:
        telas, nome = conteudo(n, U, L)
        T = gerais(n, U, nome, L)
        for tid, d in telas.items(): T['tela_' + tid] = d
        TXT[L] = T
    ids = list(TXT['pt'].keys())
    SIN = {L: {k: v for k, v in SIN_BASE[L].items() if ('tela_' + k) in TXT[L]} for L in LS}
    for L in LS:
        extra = [n] + ([U['rede'].lower()] if U['rede'] else [])
        SIN[L]['porta'] = SIN[L]['porta'] + [n]
        SIN[L]['ape'] = SIN[L]['ape'] + [U['rede'].lower()]

    telas_js = open(f'{P}/telas-v2-padrao.js').read()
    telas_js = re.sub(r"\n  \{id:'roupas',[^\n]*", '', telas_js)
    if U['help']:
        telas_js = telas_js.replace("  {id:'garagem',", ECO_TELA + "  {id:'garagem',", 1)
    assert ("'economia'" in telas_js) == U['help'] and "'roupas'" not in telas_js

    base_dados = base[base.index('<script id="dados">'):]; base_dados = base_dados[:base_dados.index('</script>')]
    rend = base_dados[:base_dados.index('var MAPA_URL')].replace('DS-407B · DNA SmartStyle', f'CP-{n} · Crystal Place')
    dados = (rend + 'var MAPA_URL = %s;\n\n' % json.dumps(MAPS) + telas_js + '\n\nvar SINONIMOS = ' + json.dumps(SIN, ensure_ascii=False, indent=1) +
             ';\n\nvar TXT = ' + json.dumps(TXT, ensure_ascii=False, indent=1) + ';\n')
    s = base.replace(base_dados, dados)

    def troca_var(s, nome, valor):
        s2, k = re.subn(r'^var %s\s*=.*$' % nome, lambda m: f'var {nome} = {valor};', s, count=1, flags=re.M); assert k == 1, nome; return s2
    b64 = lambda p: 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    fotos = {k: b64(f'{FOT}/{v}.webp') for k, v in U['fotos'].items()}
    fotos.update({k: b64(f'{FOT}/{v}.webp') for k, v in PREDIO_FOTOS.items()})
    s = troca_var(s, 'UNIDADE', json.dumps(f'CP-{n}'))
    s = troca_var(s, 'TERMO_URL', json.dumps(f'https://pedpaz.github.io/Guias-alugo/termo.html?u=CP-{n}'))
    s = troca_var(s, 'SENHA', json.dumps(U.get('senha', '')))
    s = troca_var(s, 'WIFI_REDE', json.dumps(U['rede'])); s = troca_var(s, 'WIFI_SENHA', json.dumps(U['senha_wifi']))
    s = troca_var(s, 'MARCA_PREDIO', '""')
    s = troca_var(s, 'FOTOS', json.dumps(fotos)); s = troca_var(s, 'CARDS', '{}')
    if U['help']:
        hs = open(f'{P}/crystal-hs/hs-{n}.html', encoding='utf-8').read()
        assert '</script' not in hs.lower()
        s = s.replace('var CARDS = {};', 'var CARDS = {};\n/* tutorial original do economizador HELP Smart (mostrado em português; nos outros idiomas, o texto de tela_economia) */\nvar HS_HTML = ' + json.dumps(hs, ensure_ascii=False) + ';', 1)
    titulo = TXT['pt']['apeNome']
    s = re.sub(r'<title>[^<]*</title>', f'<title>Crystal Place · {titulo} · Guia da estadia</title>', s, 1)
    cfg = re.sub(r'data:[^"]+', '', s.split('<script id="dados">')[0])
    assert '407' not in cfg and 'Apartamento407b' not in cfg, 'sobrou 407 na config'
    dd = s[s.index('<script id="dados">'):]; dd = dd[:dd.index('</script>')]
    for proib in ['407', 'DNA', 'T-37', '5562981771013', 'café e itens', 'Frigobar abastecido']:
        assert proib not in dd, proib
    arq = f'{R}/guia-crystal-{n}.html'
    open(arq, 'w', encoding='utf-8').write(s)
    print('ok', n, len(s), [k[5:] for k in TXT['pt'] if k.startswith('tela_')])

if __name__ == '__main__':
    for n in (sys.argv[1:] or list(UN)): gerar(n)
