"""Gera a base v2 (TELAS/TXT/SINONIMOS) do WB-2903 (Walk Bueno, duplex 2903) a partir do guia antigo
(guia-2903-walk-bueno-v20.html, HTML por seções, só em português), reescrito nos 3 idiomas.
Esqueleto: guia v2 do DS-407B (978a1cb). Tela extra 'bar' (adega e cervejeira por confiança, com Pix).
uso: python3 montar-base-WB2903.py → reescreve guia-2903-walk-bueno-v20.html (mesmo nome: os links já configurados continuam valendo) (depois: montar.py 2903)"""
import base64, json, os, re, subprocess
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(P))
def git(ref, arq): return subprocess.run(['git', '-C', R, 'show', f'{ref}:{arq}'], capture_output=True, check=True).stdout.decode()
base = git('978a1cb', 'guia-dna-407B.html')
velho = git('55340a4', 'guia-2903-walk-bueno-v20.html')   # guia antigo, antes da conversão
LS = ['pt', 'en', 'es']
MAPS = 'https://maps.app.goo.gl/ce1t5VF6Cp3suEKx9'
WAZE = 'https://waze.com/ul?ll=-16.70551,-49.27124&navigate=yes'
PIX_CC = re.search(r"000201[0-9A-Za-z .]*?6304[0-9A-F]{4}", velho).group(0)
PIX_QR = 'https://drive.google.com/file/d/1E1YEKr9xmS78Xo55ykhih4DstgwGdIAk/view?usp=sharing'
SENHA = '2255'; REDE = 'Macedo Paz'; WSENHA = 'rotas1234'; VAGA = '106'; CAP = 4
SM = {'pt': '1 (um) salário mínimo vigente', 'en': 'one Brazilian minimum monthly wage', 'es': '1 (un) salario mínimo vigente en Brasil'}

def conteudo(L):
    x = lambda pt, en, es: {'pt': pt, 'en': en, 'es': es}[L]
    sm = SM[L]; T = {}
    T['checkin'] = dict(titulo=x('Check-in online e vistoria', 'Online check-in and inspection', 'Check-in online e inspección'),
      sub=x('Dois minutos, e a sua entrada está liberada', 'Two minutes, and your entry is cleared', 'Dos minutos y tu entrada queda liberada'),
      lead=x('O check-in online é obrigatório: é dele que sai o cadastro dos hóspedes e a liberação da biometria na portaria.',
             'The online check-in is mandatory: it registers the guests and clears your biometric access at the front desk.',
             'El check-in online es obligatorio: de él sale el registro de los huéspedes y la liberación de la biometría en la portería.'),
      btnTermo=x('Preencher o check-in online', 'Fill in the online check-in', 'Completar el check-in online'),
      vistH=x('Vistoria de chegada', 'Arrival inspection', 'Inspección de llegada'),
      vistP=x('Encontrou alguma coisa fora do lugar? Marque aqui nas primeiras horas. É isso que protege você de ser cobrado por um dano que já existia. <b>Não enviar nada significa que estava tudo conforme.</b>',
              'Found something out of place? Tick it here in the first few hours. That protects you from being charged for damage that was already there. <b>Sending nothing means everything was fine.</b>',
              '¿Encontraste algo fuera de lugar? Márcalo aquí en las primeras horas. Eso te protege de cobros por daños que ya existían. <b>No enviar nada significa que todo estaba conforme.</b>'),
      vistItens=[x('Cama, colchão e roupa de cama', 'Bed, mattress and bedding', 'Cama, colchón y ropa de cama'), x('Sofá, estofados e decoração', 'Sofa, upholstery and décor', 'Sofá, tapizados y decoración'),
                 x('TV, Alexa e cortinas elétricas', 'TV, Alexa and electric curtains', 'TV, Alexa y cortinas eléctricas'), x('Cozinha: cooktop, micro-ondas e geladeira', 'Kitchen: cooktop, microwave and fridge', 'Cocina: anafe, microondas y heladera'),
                 x('Adega e cervejeira', 'Wine and beer fridges', 'Cava y cervecera'), x('Banheiros e chuveiros', 'Bathrooms and showers', 'Baños y duchas'),
                 x('Ar-condicionado e iluminação', 'Air conditioning and lighting', 'Aire acondicionado e iluminación'), x('Limpeza geral', 'General cleanliness', 'Limpieza general')],
      vistPh=x('Descreva o que encontrou (opcional)', 'Describe what you found (optional)', 'Describe lo que encontraste (opcional)'),
      vistBtn=x('Enviar a vistoria pelo WhatsApp', 'Send the inspection on WhatsApp', 'Enviar la inspección por WhatsApp'),
      vistNota=x('Reforce com fotos pelo WhatsApp logo depois de enviar — o horário fica registrado e garante a sua proteção.',
                 'Add photos on WhatsApp right after sending — the time is recorded and protects you.', 'Refuerza con fotos por WhatsApp justo después de enviar: el horario queda registrado y te protege.'),
      blocos=[dict(dest=True, pill=x('faça agora', 'do it now', 'hazlo ahora'), h=x('Por que é obrigatório', 'Why it is mandatory', 'Por qué es obligatorio'),
        p=[x('A portaria cadastra a biometria e o reconhecimento facial a partir da lista de hóspedes, que vem do check-in online. Sem ela, <b>a entrada não é liberada</b>.',
             'The front desk registers your biometrics and face ID from the guest list, which comes from the online check-in. Without it, <b>entry is not cleared</b>.',
             'La portería registra la biometría y el reconocimiento facial a partir de la lista de huéspedes, que sale del check-in online. Sin ella, <b>la entrada no se libera</b>.'),
           x('<b>Todos os hóspedes</b> precisam constar, inclusive quem chegar depois do titular.', '<b>Every guest</b> must be listed, including anyone arriving later.', '<b>Todos los huéspedes</b> deben figurar, incluso quien llegue después.')])])
    T['chegar'] = dict(titulo=x('Como chegar', 'Getting here', 'Cómo llegar'), sub=x('Walk Bueno · Setor Bueno', 'Walk Bueno · Setor Bueno', 'Walk Bueno · Setor Bueno'),
      lead=x('O Walk Bueno fica no Setor Bueno, de frente para o Parque Vaca Brava — o bairro mais completo de Goiânia para comer e caminhar.',
             'Walk Bueno is in Setor Bueno, facing Parque Vaca Brava — the best neighbourhood in Goiânia to eat out and walk around.',
             'El Walk Bueno está en el Setor Bueno, frente al Parque Vaca Brava: el barrio más completo de Goiânia para comer y caminar.'),
      btnMapa=x('Abrir no Google Maps', 'Open in Google Maps', 'Abrir en Google Maps'),
      blocos=[dict(foto='predio-fachada', h=x('O edifício', 'The building', 'El edificio'), p=[x('<b>Edifício Walk Bueno</b> — Setor Bueno, Goiânia/GO. Apartamento <b>2903</b>, no 29º andar.',
                 '<b>Walk Bueno building</b> — Setor Bueno, Goiânia/GO. Apartment <b>2903</b>, on the 29th floor.', '<b>Edificio Walk Bueno</b> — Setor Bueno, Goiânia/GO. Departamento <b>2903</b>, en el piso 29.')]),
              dict(h=x('De aplicativo', 'By ride app', 'En aplicación'), p=[x('Uber e 99 encontram o Walk Bueno pelo nome. Prefere Waze? <a href="%s" target="_blank" rel="noopener"><b>Abrir no Waze</b></a>' % WAZE,
                 'Uber and 99 find Walk Bueno by name. Prefer Waze? <a href="%s" target="_blank" rel="noopener"><b>Open in Waze</b></a>' % WAZE,
                 'Uber y 99 encuentran el Walk Bueno por el nombre. ¿Prefieres Waze? <a href="%s" target="_blank" rel="noopener"><b>Abrir en Waze</b></a>' % WAZE)])])
    T['predio'] = dict(titulo=x('Entrar no prédio', 'Entering the building', 'Entrar al edificio'), sub=x('Portaria, biometria e reconhecimento facial', 'Front desk, biometrics and face ID', 'Portería, biometría y reconocimiento facial'),
      lead=x('Na chegada, informe o seu nome na recepção. Depois do cadastro, a biometria e o reconhecimento facial liberam o elevador.',
             'On arrival, give your name at the front desk. Once registered, biometrics and face ID release the lift.',
             'Al llegar, da tu nombre en la recepción. Después del registro, la biometría y el reconocimiento facial liberan el ascensor.'),
      blocos=[dict(pill=x('Na chegada', 'On arrival', 'Al llegar'), h=x('Documento com foto', 'Photo ID', 'Documento con foto'),
                   p=[x('A portaria confere o seu nome na lista que vem do check-in online e cadastra a sua biometria na hora.', 'The front desk checks your name against the list from the online check-in and registers your biometrics on the spot.',
                        'La portería confirma tu nombre en la lista del check-in online y registra tu biometría en el momento.')]),
              dict(dest=True, h=x('Visitas não são permitidas', 'No visitors', 'No se permiten visitas'),
                   p=[x('Só entram os hóspedes cadastrados no check-in online.', 'Only guests registered in the online check-in may enter.', 'Solo entran los huéspedes registrados en el check-in online.')])])
    T['porta'] = dict(titulo=x('Entrar no apartamento', 'Getting into the apartment', 'Entrar al departamento'), sub=x('29º andar · senha da porta', '29th floor · door code', 'Piso 29 · clave de la puerta'),
      lead=x('Suba pelo elevador até o 29º andar. O apartamento é o duplex <b>2903</b>.', 'Take the lift to the 29th floor. The apartment is duplex <b>2903</b>.', 'Sube en ascensor al piso 29. El departamento es el dúplex <b>2903</b>.'),
      blocos=[dict(dest=True, h=x('A senha da porta', 'The door code', 'La clave de la puerta'), chave=SENHA, p=[x('A porta tem fechadura digital.', 'The door has a digital lock.', 'La puerta tiene cerradura digital.')]),
              dict(h=x('Ao sair', 'When you leave', 'Al salir'), p=[x('<b>Segure a porta até ela travar por completo.</b> Só então solte — assim ela não fica encostada.',
                   '<b>Hold the door until it locks completely.</b> Only then let go — so it is not left ajar.', '<b>Sostén la puerta hasta que se trabe por completo.</b> Recién entonces suéltala, así no queda entreabierta.')]),
              dict(h=x('Nada a retirar, nada a devolver', 'Nothing to collect or return', 'Nada que retirar ni devolver'), p=[x('Não há chave para buscar na portaria.', 'There is no key to pick up at the front desk.', 'No hay llave que retirar en la portería.')])])
    T['ape'] = dict(titulo=x('O duplex', 'The duplex', 'El dúplex'), sub=x('Duplex · até 4 hóspedes · 220V', 'Duplex · up to 4 guests · 220V', 'Dúplex · hasta 4 huéspedes · 220V'),
      lead=x('Um duplex no 29º andar, com o Parque Vaca Brava na janela, o lustre de globos na sala e casa inteligente.',
             'A duplex on the 29th floor, with Parque Vaca Brava out the window, the glass-globe chandelier in the living room and a smart home.',
             'Un dúplex en el piso 29, con el Parque Vaca Brava en la ventana, la lámpara de globos en la sala y casa inteligente.'),
      blocos=[dict(foto='ape-sala', h=x('A sala', 'The living room', 'La sala'), p=[x('À noite, brinque com o jogo de luzes da sala: o lustre de globos muda o clima do ambiente.',
                   'At night, play with the living-room lighting: the globe chandelier changes the whole mood.', 'De noche, juega con las luces de la sala: la lámpara de globos cambia el clima del ambiente.')]),
              dict(foto='ape-suite', h=x('A suíte', 'The suite', 'La suite'), p=[x('Roupa de cama e toalhas limpas na chegada.', 'Clean bedding and towels on arrival.', 'Ropa de cama y toallas limpias a la llegada.')]),
              dict(foto='ape-lavabo', h=x('O lavabo', 'The powder room', 'El toilette'), p=[x('Lavabo social, além do banheiro da suíte.', 'A guest powder room, besides the suite bathroom.', 'Un toilette social, además del baño de la suite.')]),
              dict(h=x('Casa inteligente', 'Smart home', 'Casa inteligente'),
                   ul=[x('<b>Alexa na sala e no quarto</b> — peça música, ligue a TV ou o ar da sala: “Alexa, liga o ar-condicionado”.', '<b>Alexa in the living room and bedroom</b> — ask for music, or to switch on the TV or the living-room air conditioning.',
                         '<b>Alexa en la sala y el dormitorio</b>: pide música, o que encienda la TV o el aire de la sala.'),
                       x('<b>Cortinas elétricas</b> — use o controle branco ou puxe levemente a cortina para ela começar a correr sozinha.', '<b>Electric curtains</b> — use the white remote, or give the curtain a gentle pull to start it moving.',
                         '<b>Cortinas eléctricas</b>: usa el control blanco o tira suavemente de la cortina para que empiece a moverse sola.')]),
              dict(h=x('Cozinha', 'Kitchen', 'Cocina'), ul=[x('<b>Cooktop</b>', '<b>Cooktop</b>', '<b>Anafe</b>'), x('<b>Micro-ondas</b>', '<b>Microwave</b>', '<b>Microondas</b>'), x('<b>Geladeira</b>', '<b>Fridge</b>', '<b>Heladera</b>'),
                   x('A cristaleira é só decorativa: os utensílios para uso estão nos armários da cozinha.', 'The glass cabinet is decorative only: the utensils to use are in the kitchen cupboards.', 'La cristalería es solo decorativa: los utensilios para usar están en los armarios de la cocina.')]),
              dict(dest=True, pill=x('atenção', 'heads-up', 'atención'), h=x('Guitarras e peças decorativas', 'Guitars and decorative pieces', 'Guitarras y piezas decorativas'),
                   p=[x('As guitarras e as peças de decoração são itens pessoais do proprietário. <b>Por favor, não manuseie.</b>', 'The guitars and decorative pieces are the owner’s personal items. <b>Please do not handle them.</b>',
                        'Las guitarras y las piezas decorativas son objetos personales del propietario. <b>Por favor, no las manipules.</b>')]),
              dict(dest=True, h='Wi-Fi', p=[x(f'Rede <b>{REDE}</b> · senha <b>{WSENHA}</b>. Também está no cartão do topo do guia — toque para copiar.', f'Network <b>{REDE}</b> · password <b>{WSENHA}</b>. It is also on the card at the top of the guide — tap to copy.',
                                            f'Red <b>{REDE}</b> · clave <b>{WSENHA}</b>. También está en la tarjeta del inicio de la guía: toca para copiar.')]),
              dict(h='220V', p=[x('Confira a voltagem dos seus aparelhos e carregadores antes de ligar.', 'Check your devices and chargers before plugging in.', 'Revisa el voltaje de tus aparatos y cargadores antes de enchufar.')]),
              dict(foto='alavie', pill=x('parceria', 'partner', 'alianza'), h=x('Aromatização Alavie', 'Scented by Alavie', 'Aromatización Alavie'),
                   p=[x('A assinatura olfativa do duplex é da <b>Alavie</b>, casa goiana de perfumaria autoral. A composição <b>VIE</b>, de bambu e chá branco, foi escolhida para criar memória afetiva da sua estadia. Gostou? <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.',
                        'The duplex’s signature scent is by <b>Alavie</b>, an independent perfume house from Goiânia. The <b>VIE</b> blend, bamboo and white tea, was chosen to make your stay memorable. Liked it? <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.',
                        'La firma olfativa del dúplex es de <b>Alavie</b>, casa de perfumería de autor de Goiânia. La composición <b>VIE</b>, de bambú y té blanco, fue elegida para crear memoria afectiva de tu estadía. ¿Te gustó? <a href="https://www.instagram.com/alaviebr/" target="_blank" rel="noopener"><b>@alaviebr</b></a>.')])])
    T['bar'] = dict(titulo=x('Bar e adega', 'Bar and wine fridge', 'Bar y cava'), sub=x('Consumo por confiança, pago por Pix', 'Honesty bar, paid by Pix', 'Consumo por confianza, pago por Pix'),
      lead=x('A adega e a cervejeira climatizadas ficam à sua disposição. Funciona por confiança: anote o que consumir e, no fim da estadia, envie o valor por Pix.',
             'The wine and beer fridges are at your disposal. It works on trust: note what you have and, at the end of your stay, send the amount by Pix.',
             'La cava y la cervecera climatizadas están a tu disposición. Funciona por confianza: anota lo que consumas y, al final de la estadía, envía el valor por Pix.'),
      pixH=x('Pagamento via Pix', 'Payment by Pix', 'Pago por Pix'), pixNome='Pedro Henrique Macedo Paz',
      pixQr=x('Abrir o QR Code', 'Open the QR code', 'Abrir el código QR'), pixCopiar=x('Copiar Pix copia e cola', 'Copy the Pix code', 'Copiar el código Pix'),
      blocos=[dict(foto='ape-adega', h=x('Cervejas', 'Beers', 'Cervezas'), ul=['Budweiser long neck — R$ 7,00', 'Heineken long neck — R$ 8,00', 'Eisenbahn long neck — R$ 7,00', 'Baden Baden IPA — R$ 18,00']),
              dict(h=x('Vinhos', 'Wines', 'Vinos'), ul=['Foye — R$ 65,00', 'Porta 6 — R$ 75,00', 'Três Medalhas — R$ 80,00', 'Barefoot — R$ 90,00']),
              dict(h=x('Sem álcool', 'Non-alcoholic', 'Sin alcohol'), ul=[x('Coca-Cola lata — R$ 5,00', 'Coca-Cola can — R$ 5.00', 'Coca-Cola lata — R$ 5,00'), x('Guaraná lata — R$ 5,00', 'Guaraná can — R$ 5.00', 'Guaraná lata — R$ 5,00'),
                   x('Água sem gás — R$ 3,50', 'Still water — R$ 3.50', 'Agua sin gas — R$ 3,50'), x('Água com gás — R$ 4,00', 'Sparkling water — R$ 4.00', 'Agua con gas — R$ 4,00')]),
              dict(h=x('A adega e a cervejeira ficam no lugar', 'The fridges stay where they are', 'La cava y la cervecera se quedan en su lugar'),
                   p=[x('Uso livre, mas não retire os aparelhos do lugar.', 'Use them freely, but do not move the appliances.', 'Uso libre, pero no retires los aparatos de su lugar.')])])
    T['garagem'] = dict(titulo=x('A garagem', 'Parking', 'El garaje'), sub=x('Vaga 106 · térreo (-1 no elevador)', 'Space 106 · ground floor (-1 in the lift)', 'Cochera 106 · planta baja (-1 en el ascensor)'),
      lead=x('O apartamento tem vaga privativa e identificada.', 'The apartment has its own marked parking space.', 'El departamento tiene una cochera privada e identificada.'),
      blocos=[dict(dest=True, h=x('A sua vaga', 'Your space', 'Tu cochera'), chave=VAGA, p=[x('Vaga <b>106</b>, no <b>térreo</b> da garagem.', 'Space <b>106</b>, on the garage <b>ground floor</b>.', 'Cochera <b>106</b>, en la <b>planta baja</b> del garaje.')]),
              dict(dest=True, pill=x('atenção', 'heads-up', 'atención'), h=x('Térreo é o -1 no elevador', 'Ground floor is -1 in the lift', 'La planta baja es el -1 del ascensor'),
                   p=[x('No Walk Bueno, o térreo da garagem corresponde ao botão <b>-1</b> do elevador.', 'At Walk Bueno, the garage ground floor is button <b>-1</b> in the lift.', 'En el Walk Bueno, la planta baja del garaje es el botón <b>-1</b> del ascensor.')]),
              dict(h=x('O controle do portão', 'The gate remote', 'El control del portón'), p=[x('Fica sobre a <b>mesa de espelhos, no hall de entrada</b> do apartamento. Devolva sempre no mesmo lugar.',
                   'It is on the <b>mirrored table in the entrance hall</b> of the apartment. Always put it back there.', 'Está sobre la <b>mesa de espejos, en el hall de entrada</b> del departamento. Devuélvelo siempre al mismo lugar.')])])
    T['lazer'] = dict(titulo=x('Lazer no 31º andar', 'Leisure on the 31st floor', 'Ocio en el piso 31'), sub=x('Aberto 24 horas', 'Open 24 hours', 'Abierto las 24 horas'),
      lead=x('O lazer fica no 31º andar, com o céu de Goiânia na janela. Depois do cadastro na portaria, a biometria ou o reconhecimento facial liberam o acesso.',
             'The leisure floor is the 31st, with the Goiânia sky out the window. Once registered at the front desk, biometrics or face ID give you access.',
             'El ocio está en el piso 31, con el cielo de Goiânia en la ventana. Después del registro en la portería, la biometría o el reconocimiento facial liberan el acceso.'),
      blocos=[dict(foto='predio-vista', h=x('Disponível 24 horas', 'Available 24 hours', 'Disponible las 24 horas'),
                   ul=[x('Piscina', 'Pool', 'Piscina'), x('Jacuzzi', 'Jacuzzi', 'Jacuzzi'), x('Sauna', 'Sauna', 'Sauna'), x('Academia', 'Gym', 'Gimnasio'),
                       x('Sala de jogos', 'Games room', 'Sala de juegos'), x('Lavanderia', 'Laundry', 'Lavandería'), x('Mini mercado', 'Mini-market', 'Minimercado')]),
              dict(duo=['predio-academia', 'predio-jacuzzi'], h=x('Academia e jacuzzi', 'Gym and jacuzzi', 'Gimnasio y jacuzzi'), p=[x('De frente para a cidade.', 'Facing the city.', 'Frente a la ciudad.')]),
              dict(foto='predio-jogos', h=x('Sala de jogos', 'Games room', 'Sala de juegos'), p=[x('Mesa de sinuca e mesas de jogos.', 'Pool table and game tables.', 'Mesa de pool y mesas de juegos.')])])
    T['regras'] = dict(titulo=x('Regras da casa', 'House rules', 'Reglas de la casa'), sub=x('Curtas, e todas por um motivo', 'Short, and each one for a reason', 'Cortas, y cada una por un motivo'),
      lead=x('São as mesmas que você aceitou no check-in online. Estão aqui para consulta.', 'They are the same ones you accepted in the online check-in, here for reference.', 'Son las mismas que aceptaste en el check-in online. Están aquí para consulta.'),
      blocos=[dict(dest=True, pill=x('proibido', 'not allowed', 'prohibido'), h=x('🚭 Proibido fumar', '🚭 No smoking', '🚭 Prohibido fumar'),
                   p=[x('Em <b>nenhum ambiente</b> do apartamento, inclusive na varanda. Vale para cigarro comum, eletrônico (vape) e narguilé.', '<b>Anywhere</b> in the apartment, including the balcony. This covers cigarettes, vapes and hookah.',
                        'En <b>ningún ambiente</b> del departamento, incluso en el balcón. Vale para cigarrillo común, electrónico (vape) y narguile.'),
                      x(f'Multa de <b>{sm}</b> mais o custo da higienização.', f'Fine of <b>{sm}</b> plus the cleaning cost.', f'Multa de <b>{sm}</b> más el costo de la higienización.')]),
              dict(dest=True, h=x('Visitas não são permitidas', 'No visitors', 'No se permiten visitas'), p=[x('O espaço é exclusivo dos hóspedes cadastrados no check-in online.', 'The space is exclusively for the guests registered in the online check-in.', 'El espacio es exclusivo de los huéspedes registrados en el check-in online.')]),
              dict(h=x('Sem festas ou eventos', 'No parties or events', 'Sin fiestas ni eventos'), p=[x(f'Multa de <b>{sm}</b>, além dos danos ao imóvel, ao mobiliário ou à decoração.', f'Fine of <b>{sm}</b>, plus any damage to the property, furniture or décor.',
                   f'Multa de <b>{sm}</b>, además de los daños al inmueble, al mobiliario o a la decoración.')]),
              dict(h=x(f'Capacidade: {CAP} pessoas', f'Capacity: {CAP} guests', f'Capacidad: {CAP} personas'), p=[x(f'Máximo de <b>{CAP} hóspedes</b>. Hóspede excedente: <b>R$ 200,00</b> por pessoa.', f'Maximum <b>{CAP} guests</b>. Each extra guest: <b>R$ 200.00</b>.', f'Máximo de <b>{CAP} huéspedes</b>. Huésped excedente: <b>R$ 200,00</b> por persona.')]),
              dict(h=x('Silêncio depois das 22h', 'Quiet after 10 pm', 'Silencio después de las 22 h'), p=[x('Principalmente na varanda, em respeito aos vizinhos.', 'Especially on the balcony, out of respect for the neighbours.', 'Sobre todo en el balcón, por respeto a los vecinos.')]),
              dict(h=x('Não manusear a decoração', 'Do not handle the décor', 'No manipular la decoración'), p=[x('Guitarras e peças decorativas são itens pessoais do proprietário.', 'Guitars and decorative pieces are the owner’s personal items.', 'Las guitarras y las piezas decorativas son objetos personales del propietario.')]),
              dict(h=x('Horários', 'Times', 'Horarios'), p=[x('Check-in a partir das <b>15h</b>, check-out até as <b>12h</b>. Não realizamos early check-in nem late check-out. Permanência além do horário: <b>R$ 200,00</b> por hora.',
                   'Check-in from <b>3 pm</b>, check-out by <b>12 pm</b>. We do not offer early check-in or late check-out. Staying past check-out: <b>R$ 200.00</b> per hour.',
                   'Check-in desde las <b>15 h</b>, check-out hasta las <b>12 h</b>. No hacemos early check-in ni late check-out. Permanencia fuera de horario: <b>R$ 200,00</b> por hora.')])])
    T['saida'] = dict(titulo=x('Ir embora', 'Leaving', 'Irse'), sub=x('Check-out até as 12h', 'Check-out by 12 pm', 'Check-out hasta las 12 h'),
      lead=x('Temos uma nova reserva chegando logo depois, e a equipe de limpeza entra pontualmente às 12h.', 'A new booking arrives right after you, and the cleaning team comes in at 12 pm sharp.', 'Llega una nueva reserva enseguida, y el equipo de limpieza entra puntualmente a las 12 h.'),
      coSelo=x('⚠ Antes de ir embora', '⚠ Before you leave', '⚠ Antes de irte'), coH=x('Confirme seu check-out', 'Confirm your check-out', 'Confirma tu check-out'),
      coP=x('É um toque só. É esse aviso que registra o encerramento da sua estadia e libera a nossa equipe de limpeza.', 'One tap. This is what closes your stay and releases our cleaning team.', 'Es un solo toque. Este aviso cierra tu estadía y libera a nuestro equipo de limpieza.'),
      coBtn=x('Avisar meu check-out', 'Confirm my check-out', 'Avisar mi check-out'),
      blocos=[dict(h=x('Antes de sair', 'Before you go', 'Antes de salir'),
                   ul=[x('Controle da garagem de volta na mesa de espelhos do hall', 'Garage remote back on the mirrored table in the hall', 'Control del garaje de vuelta en la mesa de espejos del hall'),
                       x('Ar-condicionado desligado em todos os ambientes', 'Air conditioning off in every room', 'Aire acondicionado apagado en todos los ambientes'),
                       x('Janelas e portas da varanda fechadas', 'Windows and balcony doors closed', 'Ventanas y puertas del balcón cerradas'), x('Luzes apagadas', 'Lights off', 'Luces apagadas'),
                       x('Torneiras e chuveiros fechados', 'Taps and showers off', 'Canillas y duchas cerradas'),
                       x('Consumo do bar anotado e Pix enviado', 'Bar consumption noted and Pix sent', 'Consumo del bar anotado y Pix enviado'),
                       x('Lixo nas lixeiras do corredor', 'Rubbish in the corridor bins', 'Basura en los cestos del pasillo'),
                       x('Porta segurada até travar por completo', 'Door held until it locks completely', 'Puerta sostenida hasta que se trabe por completo')]),
              dict(h=x('O check-out termina quando você sai do prédio', 'Check-out ends when you leave the building', 'El check-out termina cuando sales del edificio'),
                   p=[x('Pedimos que o grupo não permaneça nas áreas comuns depois do horário de saída.', 'Please do not stay on in the common areas after check-out time.', 'Pedimos que el grupo no permanezca en las áreas comunes después del horario de salida.')])])
    T['bairro'] = dict(titulo=x('Setor Bueno', 'Setor Bueno', 'Setor Bueno'), sub=x('Parque Vaca Brava em frente', 'Parque Vaca Brava across the street', 'Parque Vaca Brava enfrente'),
      lead=x('O coração gastronômico e noturno de Goiânia, com o Parque Vaca Brava aos pés do prédio.', 'The food and nightlife heart of Goiânia, with Parque Vaca Brava right below the building.', 'El corazón gastronómico y nocturno de Goiânia, con el Parque Vaca Brava a los pies del edificio.'),
      blocos=[dict(foto='vista', h=x('A pé', 'On foot', 'A pie'), ul=[x('<b>Parque Vaca Brava</b> — corrida, lago e fim de tarde', '<b>Parque Vaca Brava</b> — running, the lake and sunset', '<b>Parque Vaca Brava</b>: correr, el lago y el atardecer'),
                   x('<b>Goiânia Shopping</b> — compras, cinema e restaurantes, numa caminhada curta', '<b>Goiânia Shopping</b> — shops, cinema and restaurants, a short walk away', '<b>Goiânia Shopping</b>: compras, cine y restaurantes, a una corta caminata')]),
              dict(h=x('Para comer', 'Where to eat', 'Dónde comer'), ul=[x('<a href="https://maps.app.goo.gl/1bBjsDeMDSRnY5up6" target="_blank" rel="noopener"><b>Cateretê</b></a> (almoço) — cozinha goiana de referência há 25 anos',
                        '<a href="https://maps.app.goo.gl/1bBjsDeMDSRnY5up6" target="_blank" rel="noopener"><b>Cateretê</b></a> (lunch) — classic Goiás cooking for 25 years',
                        '<a href="https://maps.app.goo.gl/1bBjsDeMDSRnY5up6" target="_blank" rel="noopener"><b>Cateretê</b></a> (almuerzo): cocina goiana de referencia hace 25 años'),
                   x('<a href="https://maps.app.goo.gl/yv2U5xvpiLhtXEv59" target="_blank" rel="noopener"><b>Nino Cucina & Vino</b></a> (jantar) — italiano em frente ao Vaca Brava',
                     '<a href="https://maps.app.goo.gl/yv2U5xvpiLhtXEv59" target="_blank" rel="noopener"><b>Nino Cucina & Vino</b></a> (dinner) — Italian facing Vaca Brava',
                     '<a href="https://maps.app.goo.gl/yv2U5xvpiLhtXEv59" target="_blank" rel="noopener"><b>Nino Cucina & Vino</b></a> (cena): italiano frente al Vaca Brava')])])
    T['problema'] = dict(titulo=x('Deu problema?', 'Something wrong?', '¿Algún problema?'), sub=x('Resolva em 30 segundos', 'Fix it in 30 seconds', 'Resuélvelo en 30 segundos'),
      lead=x('Quase tudo aqui se resolve sem esperar. Se não resolver, o WhatsApp está no fim desta tela e a gente responde rápido.', 'Most things here can be fixed straight away. If not, WhatsApp is at the end of this screen and we reply fast.',
             'Casi todo aquí se resuelve sin esperar. Si no, el WhatsApp está al final de esta pantalla y respondemos rápido.'),
      btnZap=x('Falar com a gente no WhatsApp', 'Message us on WhatsApp', 'Hablar con nosotros por WhatsApp'), blocos=[],
      ac=[dict(q=x('A porta não abre', 'The door will not open', 'La puerta no abre'), r=[x(f'Digite <b>{SENHA}</b> com calma. Se o teclado não acender, a pilha pode estar fraca — chame a gente. Não force a porta.',
                f'Type <b>{SENHA}</b> calmly. If the keypad does not light up, the battery may be low — message us. Do not force the door.', f'Marca <b>{SENHA}</b> con calma. Si el teclado no se enciende, la pila puede estar baja: escríbenos. No fuerces la puerta.')]),
          dict(q=x('O elevador não vai para o meu andar', 'The lift will not go to my floor', 'El ascensor no va a mi piso'), r=[x('O elevador é liberado pela biometria ou pelo reconhecimento facial, cadastrados na portaria. Se ainda não cadastrou, é isso que falta.',
                'The lift is released by the biometrics or face ID registered at the front desk. If you have not registered yet, that is what is missing.', 'El ascensor se libera con la biometría o el reconocimiento facial registrados en la portería. Si aún no te registraste, es eso lo que falta.')]),
          dict(q=x('A cortina não fecha', 'The curtain will not close', 'La cortina no cierra'), r=[x('Use o controle branco ou puxe a cortina de leve para ela começar a correr sozinha.', 'Use the white remote, or give the curtain a gentle pull to start it moving.', 'Usa el control blanco o tira suavemente de la cortina para que empiece a moverse sola.')]),
          dict(q=x('O Wi-Fi caiu', 'The Wi-Fi is down', 'Se cayó el wifi'), r=[x(f'A rede é a <b>{REDE}</b>. Tire o roteador da tomada, espere 30 segundos e ligue de novo.', f'The network is <b>{REDE}</b>. Unplug the router, wait 30 seconds and plug it back in.', f'La red es <b>{REDE}</b>. Desenchufa el router, espera 30 segundos y vuelve a enchufarlo.')]),
          dict(q=x('O ar-condicionado não está gelando', 'The air conditioning is not cooling', 'El aire acondicionado no enfría'), r=[x('Confira se está no modo <b>refrigerar</b> (o floco de neve), com a temperatura abaixo de 23°C, e feche janela e cortina.',
                'Check it is on <b>cool</b> mode (the snowflake), set below 23°C, and close the window and curtain.', 'Verifica que esté en modo <b>frío</b> (el copo de nieve), por debajo de 23 °C, y cierra ventana y cortina.')])])
    return T

def gerais(L):
    x = lambda pt, en, es: {'pt': pt, 'en': en, 'es': es}[L]
    rot = 'Walk Bueno 2903'
    return dict(apeNome=x('Duplex 2903', 'Duplex 2903', 'Dúplex 2903'), heroRot=x('Guia da estadia', 'Your stay guide', 'Guía de la estadía'), heroDesce=x('role para começar', 'scroll to start', 'desliza para empezar'),
      secaoMenu=x('O que você precisa saber', 'What you need to know', 'Lo que necesitas saber'), apeSub='Walk Bueno · Setor Bueno, Goiânia',
      cSenha=x('Senha da porta', 'Door code', 'Clave de la puerta'), cSenhaSub=x('fechadura digital', 'digital lock', 'cerradura digital'), cAcesso=x('Seu acesso', 'Your access', 'Tu acceso'),
      cAcessoVal=x('Fechadura digital', 'Digital lock', 'Cerradura digital'), cAcessoSub=x('a senha chega junto com este guia', 'the code comes with this guide', 'la clave llega junto con esta guía'),
      cAcessoTap=x('toque para ver o passo a passo', 'tap for the steps', 'toca para ver el paso a paso'), cWifi=x('Senha do Wi-Fi', 'Wi-Fi password', 'Clave del Wi-Fi'),
      cWifiRede=x('rede:', 'network:', 'red:'), cWifiPend=x('peça pelo WhatsApp', 'ask us on WhatsApp', 'pídela por WhatsApp'), cHoras=x('Horários', 'Times', 'Horarios'),
      cHorasVal=x('15h / 12h', '3pm / 12pm', '15h / 12h'), cHorasSub=x('entrada a partir das 15h · saída até as 12h', 'check-in from 3pm · check-out by 12pm', 'entrada desde las 15h · salida hasta las 12h'),
      cTap=x('toque para copiar', 'tap to copy', 'toca para copiar'), copiado=x('copiado ✓', 'copied ✓', 'copiado ✓'),
      buscaPh=x('O que você procura? (wi-fi, garagem, piscina…)', 'What are you looking for? (wi-fi, parking, pool…)', '¿Qué buscas? (wifi, cochera, piscina…)'),
      buscaVazio=x('Não achamos essa palavra. Toque no WhatsApp na barra de baixo que a gente responde.', "We couldn't find that. Tap WhatsApp in the bar below and we'll answer.", 'No encontramos esa palabra. Toca WhatsApp en la barra de abajo y te respondemos.'),
      bMenu=x('Menu', 'Menu', 'Menú'), bCheckout='CHECK-OUT', bVoltar=x('Voltar ao menu', 'Back to menu', 'Volver al menú'), rodape=x('Gestão de imóveis para temporada', 'Short-stay property management', 'Gestión de inmuebles de temporada'),
      zapOi=x(f'Olá! Sou hóspede do {rot} e preciso de ajuda.', f"Hi! I'm a guest at {rot} and I need some help.", f'¡Hola! Soy huésped del {rot} y necesito ayuda.'),
      zapCheckout=x(f'Olá! Estou fazendo o check-out do {rot}. Já deixei o apartamento.', f"Hi! I'm checking out of {rot}. I've already left the apartment.", f'¡Hola! Estoy haciendo el check-out del {rot}. Ya dejé el departamento.'),
      vistVazio=x('Marque um item ou escreva uma observação antes de enviar.', 'Tick an item or write a note before sending.', 'Marca un ítem o escribe una observación antes de enviar.'),
      vistMsg=x(f'Vistoria de chegada — {rot}. Encontrei:', f'Arrival inspection — {rot}. I found:', f'Inspección de llegada — {rot}. Encontré:'), vistObs=x('Observações', 'Notes', 'Observaciones'))

SIN = {'pt': {'chegar': ['endereco', 'onde fica', 'mapa', 'uber', 'waze', 'localizacao'], 'predio': ['portaria', 'recepcao', 'biometria', 'facial', 'documento', 'visita'],
              'porta': ['senha', 'senha da porta', 'fechadura', 'codigo', 'abrir a porta', 'nao abre', '2903', '29 andar'],
              'ape': ['wifi', 'wi-fi', 'rede', 'internet', 'alexa', 'cortina', 'guitarra', 'cristaleira', 'cozinha', 'tv', '220v', 'alavie', 'lavabo', 'suite'],
              'bar': ['bar', 'adega', 'cervejeira', 'cerveja', 'vinho', 'pix', 'consumo', 'bebida', 'agua', 'refrigerante'],
              'garagem': ['garagem', 'vaga', '106', 'estacionamento', 'carro', 'controle', 'terreo', '-1'],
              'lazer': ['piscina', 'jacuzzi', 'sauna', 'academia', 'jogos', 'sinuca', 'lavanderia', 'mercado', '31'],
              'regras': ['regras', 'fumar', 'vape', 'festa', 'silencio', 'barulho', 'visita', 'multa', 'salario minimo'],
              'problema': ['problema', 'nao funciona', 'quebrou', 'ajuda', 'elevador'], 'bairro': ['restaurante', 'parque', 'vaca brava', 'shopping', 'caterete', 'nino'],
              'checkin': ['check-in', 'checkin', 'termo', 'cadastro', 'vistoria'], 'saida': ['check-out', 'checkout', 'saida', 'ir embora', '12h']},
       'en': {'chegar': ['address', 'map', 'uber', 'waze'], 'predio': ['front desk', 'biometrics', 'face id', 'visitor'], 'porta': ['code', 'door', 'lock', '2903'],
              'ape': ['wifi', 'password', 'alexa', 'curtain', 'guitar', 'kitchen', 'tv', '220v'], 'bar': ['bar', 'wine', 'beer', 'pix', 'drinks'],
              'garagem': ['parking', 'garage', 'car', 'remote', '106'], 'lazer': ['pool', 'jacuzzi', 'sauna', 'gym', 'games', 'laundry'],
              'regras': ['rules', 'smoking', 'party', 'quiet', 'visitor', 'fine'], 'problema': ['problem', 'help', 'lift'], 'bairro': ['restaurant', 'park', 'shopping'],
              'checkin': ['check-in', 'form', 'inspection'], 'saida': ['check-out', 'leave']},
       'es': {'chegar': ['direccion', 'mapa', 'uber', 'waze'], 'predio': ['porteria', 'recepcion', 'biometria', 'facial', 'visita'], 'porta': ['clave', 'puerta', 'cerradura', '2903'],
              'ape': ['wifi', 'clave', 'alexa', 'cortina', 'guitarra', 'cocina', 'tv', '220v'], 'bar': ['bar', 'vino', 'cerveza', 'pix', 'bebida'],
              'garagem': ['cochera', 'garaje', 'auto', 'control', '106'], 'lazer': ['piscina', 'jacuzzi', 'sauna', 'gimnasio', 'juegos', 'lavanderia'],
              'regras': ['reglas', 'fumar', 'fiesta', 'silencio', 'visita', 'multa'], 'problema': ['problema', 'ayuda', 'ascensor'], 'bairro': ['restaurante', 'parque', 'shopping'],
              'checkin': ['check-in', 'formulario', 'inspeccion'], 'saida': ['check-out', 'salida']}}

TXT = {}
for L in LS:
    T = gerais(L)
    for tid, d in conteudo(L).items(): T['tela_' + tid] = d
    TXT[L] = T

telas_js = open(f'{P}/telas-v2-padrao.js').read()
telas_js = re.sub(r"\n  \{id:'(roupas|cozinha)',[^\n]*", '', telas_js)
telas_js = telas_js.replace("  {id:'garagem',", "  {id:'bar', corpo:function(d){ return blocos(d)+'<div class=\"bloco dest\"><h3>'+d.pixH+'</h3><p>'+d.pixNome+'</p>'+\n"
    "     '<a class=\"btn linha\" target=\"_blank\" rel=\"noopener\" href=\"'+PIX_QR+'\" style=\"margin-top:10px\">'+d.pixQr+'</a>'+\n"
    "     '<a class=\"btn laranja\" href=\"#\" onclick=\"copiarTexto(PIX_CC);aviso(t(\\'copiado\\'));return false\" style=\"margin-top:10px\">'+d.pixCopiar+'</a></div>'; }},\n  {id:'garagem',", 1)
assert "'bar'" in telas_js and "'roupas'" not in telas_js

bd = base[base.index('<script id="dados">'):]; bd = bd[:bd.index('</script>')]
rend = bd[:bd.index('var MAPA_URL')].replace('DS-407B · DNA SmartStyle', 'WB-2903 · Walk Bueno')
s = base.replace(bd, rend + 'var MAPA_URL = %s;\n\n' % json.dumps(MAPS) + telas_js + '\n\nvar SINONIMOS = ' + json.dumps(SIN, ensure_ascii=False, indent=1) +
                 ';\n\nvar TXT = ' + json.dumps(TXT, ensure_ascii=False, indent=1) + ';\n')
def troca_var(s, nome, valor):
    s2, k = re.subn(r'^var %s\s*=.*$' % nome, lambda m: f'var {nome} = {valor};', s, count=1, flags=re.M); assert k == 1, nome; return s2
fotos = {k: 'data:image/webp;base64,' + base64.b64encode(open(f'{P}/walk-fotos/{k}.webp', 'rb').read()).decode() for k in
         ['hero', 'ape-sala', 'ape-suite', 'ape-lavabo', 'alavie', 'ape-adega', 'predio-fachada', 'predio-vista', 'predio-academia', 'predio-jacuzzi', 'predio-jogos', 'vista']}
s = troca_var(s, 'UNIDADE', '"WB-2903"'); s = troca_var(s, 'TERMO_URL', '"https://pedpaz.github.io/Guias-alugo/termo.html?u=WB-2903"')
s = troca_var(s, 'SENHA', json.dumps(SENHA)); s = troca_var(s, 'WIFI_REDE', json.dumps(REDE)); s = troca_var(s, 'WIFI_SENHA', json.dumps(WSENHA))
s = troca_var(s, 'MARCA_PREDIO', '""'); s = troca_var(s, 'FOTOS', json.dumps(fotos)); s = troca_var(s, 'CARDS', '{}')
s = s.replace('var CARDS = {};', 'var CARDS = {};\nvar PIX_CC = %s;\nvar PIX_QR = %s;' % (json.dumps(PIX_CC), json.dumps(PIX_QR)), 1)
s = re.sub(r'<title>[^<]*</title>', '<title>Walk Bueno · Duplex 2903 · Guia da estadia</title>', s, 1)
cfg = re.sub(r'data:[^"]+', '', s.split('<script id="dados">')[0]); assert '407' not in cfg
dd = s[s.index('<script id="dados">'):]; dd = dd[:dd.index('</script>')]
for proib in ['407', 'DNA', '5562981771013', '98177']: assert proib not in dd, proib
open(f'{R}/guia-2903-walk-bueno-v20.html', 'w', encoding='utf-8').write(s)
print('ok', len(s), PIX_CC[-8:], [k[5:] for k in TXT['pt'] if k.startswith('tela_')])
