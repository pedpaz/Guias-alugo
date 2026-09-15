/* =====================================================================
   aluGO · termo.html — TABELA DE CONFIGURAÇÃO
   Um formulário só (termo.html?u=CÓDIGO). Tudo que muda de um apê pro
   outro mora aqui. Textos podem ser string (vale pros 3 idiomas) ou
   objeto {pt, en, es}. Campos entre {chaves} nas cláusulas são trocados
   pelos dados do apê (ou pelo PADRAO quando o apê não define).
   ===================================================================== */

/* Valores usados quando o apê não diz diferente. */
window.PADRAO = {
  bairro: "Goiânia",
  checkin: "15h",
  checkout: "11h",
  multa_fumar: "R$ 300,00",
  multa_festa: "R$ 500,00",
  multa_atraso: "R$ 200,00 por hora",
  multa_extra: "R$ 200,00 por pessoa",
  silencio: "22h e 7h",
  pos_envio: { pt: "Guarde este link: você recebe a confirmação por WhatsApp.",
               en: "Keep this link: you'll get a confirmation on WhatsApp.",
               es: "Guarda este enlace: recibirás la confirmación por WhatsApp." }
};

/* Cláusulas padrão (mesma ordem pra todos). Um apê pode tirar uma cláusula
   pelo id (sem: ["animais"]) ou acrescentar (clausulas_extra: [...]). */
window.CLAUSULAS = [
  { id: "imovel",
    t: { pt: "Do imóvel", en: "The property", es: "Del inmueble" },
    p: [
      { pt: "A unidade {unidade} do {predio} ({endereco}) é cedida para hospedagem por temporada, mobiliada e equipada, exclusivamente para fins residenciais temporários.",
        en: "Unit {unidade} at {predio} ({endereco}) is provided as a short-term holiday rental, furnished and equipped, exclusively for temporary residential use.",
        es: "La unidad {unidade} del {predio} ({endereco}) se cede para hospedaje temporario, amoblada y equipada, exclusivamente para fines residenciales temporales." },
      { pt: "É vedada a sublocação, a cessão a terceiros e o uso comercial do imóvel.",
        en: "Subletting, transfer to third parties and commercial use are forbidden.",
        es: "Está prohibido el subarriendo, la cesión a terceros y el uso comercial del inmueble." }
    ] },
  { id: "capacidade",
    t: { pt: "Da capacidade", en: "Capacity", es: "De la capacidad" },
    p: [
      { pt: "A unidade comporta no máximo <b>{capacidade} pessoa(s)</b>{camas}.",
        en: "The unit sleeps a maximum of <b>{capacidade} guest(s)</b>{camas}.",
        es: "La unidad admite un máximo de <b>{capacidade} persona(s)</b>{camas}." },
      { pt: "A presença de hóspede não declarado acarreta multa de <b>{multa_extra}</b>, sem prejuízo do encerramento imediato da estadia.",
        en: "An undeclared guest incurs a fine of <b>{multa_extra}</b>, and the stay may be ended immediately.",
        es: "La presencia de un huésped no declarado genera una multa de <b>{multa_extra}</b>, sin perjuicio del cierre inmediato de la estadía." },
      { pt: "Visitantes não podem pernoitar e devem ser identificados na entrada do prédio.",
        en: "Visitors may not stay overnight and must be identified at the building entrance.",
        es: "Las visitas no pueden pernoctar y deben identificarse en la entrada del edificio." }
    ] },
  { id: "horarios",
    t: { pt: "Do check-in e do check-out", en: "Check-in and check-out", es: "Del check-in y del check-out" },
    p: [
      { pt: "Check-in a partir das <b>{checkin}</b>. Check-out até as <b>{checkout}</b>.",
        en: "Check-in from <b>{checkin}</b>. Check-out by <b>{checkout}</b>.",
        es: "Check-in a partir de las <b>{checkin}</b>. Check-out hasta las <b>{checkout}</b>." },
      { pt: "Os horários são fixos e correspondem ao tempo necessário para higienização e troca de enxoval entre estadias. O atraso não autorizado na saída acarreta multa de <b>{multa_atraso}</b>.",
        en: "These times are fixed and match the time needed to clean and change all linen between stays. Unauthorised late departure incurs a fine of <b>{multa_atraso}</b>.",
        es: "Los horarios son fijos y corresponden al tiempo necesario para la higienización y el cambio de ropa de cama entre estadías. El retraso no autorizado genera una multa de <b>{multa_atraso}</b>." }
    ] },
  { id: "fumar",
    t: { pt: "Da proibição de fumar", en: "No smoking", es: "De la prohibición de fumar" },
    p: [
      { pt: "É <b>proibido fumar</b> em qualquer área interna da unidade, incluindo cigarro eletrônico, varanda e banheiro.",
        en: "Smoking is <b>prohibited</b> anywhere inside the unit, including e-cigarettes, balcony and bathroom.",
        es: "Está <b>prohibido fumar</b> en cualquier área interna de la unidad, incluidos el cigarrillo electrónico, el balcón y el baño." },
      { pt: "O descumprimento acarreta multa de <b>{multa_fumar}</b>, acrescida do custo de higienização de enxoval, cortinas e estofados, e das multas que o condomínio venha a aplicar.",
        en: "Breaching this incurs a fine of <b>{multa_fumar}</b>, plus the cost of deep-cleaning linen, curtains and upholstery, and any fine applied by the building.",
        es: "El incumplimiento genera una multa de <b>{multa_fumar}</b>, más el costo de higienización de ropa de cama, cortinas y tapizados, y las multas que aplique el condominio." }
    ] },
  { id: "acesso",
    t: { pt: "Do acesso", en: "Access", es: "Del acceso" },
    p: [ "{acesso}", "{acesso2}" ] },
  { id: "festas",
    t: { pt: "Das festas e eventos", en: "Parties and events", es: "De las fiestas y eventos" },
    p: [
      { pt: "São <b>proibidas</b> festas, eventos, comemorações e reuniões de pessoas não hospedadas na unidade.",
        en: "Parties, events, celebrations and gatherings of people not staying in the unit are <b>forbidden</b>.",
        es: "Están <b>prohibidas</b> las fiestas, eventos, celebraciones y reuniones de personas no hospedadas en la unidad." },
      { pt: "O descumprimento acarreta multa de <b>{multa_festa}</b>, além da reparação integral de eventuais danos e do encerramento imediato da hospedagem.",
        en: "Breaching this incurs a fine of <b>{multa_festa}</b>, plus full repair of any damage and immediate termination of the stay.",
        es: "El incumplimiento genera una multa de <b>{multa_festa}</b>, además de la reparación integral de los daños y del cierre inmediato del hospedaje." }
    ] },
  { id: "trajes",
    t: { pt: "Dos trajes de banho", en: "Swimwear", es: "De los trajes de baño" },
    p: [
      { pt: "É <b>proibido circular em trajes de banho</b> (biquíni, sunga, maiô, sem camisa) nas dependências do condomínio: portaria, recepção, elevadores, corredores e garagem. Da piscina até o apartamento, use uma saída de banho ou camiseta.",
        en: "<b>Walking around in swimwear</b> (bikini, trunks, swimsuit, shirtless) is <b>not allowed</b> in the building's common areas: lobby, front desk, lifts, corridors and garage. Between the pool and the apartment, wear a cover-up or a t-shirt.",
        es: "Está <b>prohibido circular en traje de baño</b> (bikini, bañador, malla, sin camiseta) por las dependencias del condominio: portería, recepción, ascensores, pasillos y cochera. De la piscina al apartamento, usa una salida de baño o una camiseta." },
      { pt: "Multas aplicadas pelo condomínio por descumprimento serão repassadas integralmente ao hóspede.",
        en: "Any fine applied by the building for breaching this will be passed on in full to the guest.",
        es: "Las multas aplicadas por el condominio por incumplimiento se trasladarán íntegramente al huésped." }
    ] },
  { id: "danos",
    t: { pt: "Da conservação e dos danos", en: "Care and damage", es: "De la conservación y los daños" },
    p: [
      { pt: "O hóspede recebe a unidade em perfeitas condições e se compromete a devolvê-la no mesmo estado.",
        en: "The guest receives the unit in perfect condition and undertakes to return it in the same state.",
        es: "El huésped recibe la unidad en perfectas condiciones y se compromete a devolverla en el mismo estado." },
      { pt: "Danos, avarias e itens faltantes serão cobrados pelo valor de reposição. A vistoria de chegada, disponível no guia digital, deve ser enviada em até 3 horas após a entrada; a ausência de envio presume que a unidade foi recebida em conformidade.",
        en: "Damage, breakage and missing items will be charged at replacement value. The arrival inspection, available in the digital guide, must be sent within 3 hours of entry; not sending it means the unit was received in order.",
        es: "Los daños, averías y faltantes se cobrarán por su valor de reposición. La inspección de llegada, disponible en la guía digital, debe enviarse dentro de las 3 horas posteriores al ingreso; su ausencia presume que la unidad fue recibida conforme." }
    ] },
  { id: "silencio",
    t: { pt: "Do silêncio", en: "Quiet hours", es: "Del silencio" },
    p: [
      { pt: "O prédio é residencial. É obrigatório o silêncio entre <b>{silencio}</b>.",
        en: "The building is residential. Quiet is required between <b>{silencio}</b>.",
        es: "El edificio es residencial. Es obligatorio el silencio entre las <b>{silencio}</b>." },
      { pt: "Multas aplicadas pelo condomínio por perturbação do sossego serão repassadas integralmente ao hóspede.",
        en: "Any fine applied by the building for noise disturbance will be passed on in full to the guest.",
        es: "Las multas aplicadas por el condominio por perturbación del descanso se trasladarán íntegramente al huésped." }
    ] },
  { id: "animais",
    t: { pt: "Dos animais", en: "Pets", es: "De los animales" },
    p: [
      { pt: "<b>Não é permitida</b> a permanência de animais de estimação nesta unidade, de qualquer porte ou espécie.",
        en: "Pets of any size or species are <b>not allowed</b> in this unit.",
        es: "<b>No se permite</b> la permanencia de mascotas en esta unidad, de ningún porte ni especie." }
    ] },
  { id: "responsabilidade",
    t: { pt: "Da responsabilidade e das áreas comuns", en: "Liability and common areas", es: "De la responsabilidad y las áreas comunes" },
    p: [
      { pt: "O titular responde por todos os hóspedes declarados e por quaisquer acompanhantes eventuais.",
        en: "The main guest is responsible for all declared guests and any occasional companions.",
        es: "El titular responde por todos los huéspedes declarados y por cualquier acompañante eventual." },
      { pt: "A aluGO não se responsabiliza por objetos pessoais deixados na unidade ou nas áreas comuns, nem por interrupções de serviços públicos ou do condomínio.",
        en: "aluGO is not liable for personal belongings left in the unit or the common areas, nor for interruptions to public or building services.",
        es: "aluGO no se responsabiliza por objetos personales dejados en la unidad o en las áreas comunes, ni por interrupciones de servicios públicos o del condominio." },
      "{areas_comuns}",
      "{estacionamento}"
    ] }
];

/* ---------------------------------------------------------------------
   OS APARTAMENTOS. Chave = código no sistema (units.code).
   Campos:
     predio, unidade (rótulo), bairro, endereco, capacidade, camas (" , em 1 cama de casal"),
     checkin, checkout, multas..., silencio, guia (arquivo do guia),
     pede_placa, pede_telefone, acesso / acesso2 (texto da cláusula de acesso),
     areas_comuns, estacionamento, sem: [ids], clausulas_extra: [{t,p}], decl_extra: [texto]
   --------------------------------------------------------------------- */
/* Textos de acesso reutilizados (3 idiomas). */
var ACESSO = {
  fechadura: {
    pt: "O prédio cadastra o reconhecimento facial de cada hóspede na entrada, mediante documento com foto e conferência desta lista. O acesso ao apartamento é por <b>fechadura digital</b> com senha pessoal, enviada após a confirmação do cadastro; a senha é trocada a cada reserva e não deve ser repassada a terceiros.",
    en: "The building registers each guest's facial recognition at the entrance, on presentation of a photo ID and a check against this list. Access to the apartment is by <b>digital lock</b> with a personal code, sent once your registration is confirmed; the code changes every booking and must not be shared.",
    es: "El edificio registra el reconocimiento facial de cada huésped en la entrada, con documento con foto y verificación de esta lista. El acceso al apartamento es por <b>cerradura digital</b> con clave personal, enviada tras confirmar el registro; la clave cambia en cada reserva y no debe compartirse." },
  fechadura2: {
    pt: "Não há chave nem cartão a devolver no check-out.",
    en: "There is no key or card to return at check-out.",
    es: "No hay llave ni tarjeta que devolver al hacer el check-out." },
  cartao: {
    pt: "O acesso ao prédio é pela recepção, que funciona 24 horas, mediante apresentação de documento com foto e conferência desta lista de hóspedes. O acesso ao apartamento é por <b>cartão magnético</b>, retirado na recepção, de uso pessoal e intransferível.",
    en: "Building access is through the front desk, staffed 24 hours, on presentation of a photo ID and a check against this guest list. Access to the apartment is by <b>keycard</b>, collected at the front desk, personal and non-transferable.",
    es: "El acceso al edificio es por la recepción, abierta 24 horas, presentando documento con foto y verificando esta lista de huéspedes. El acceso al apartamento es por <b>tarjeta magnética</b>, retirada en recepción, personal e intransferible." },
  cartao2: {
    pt: "<b>O cartão deve ser devolvido na recepção no check-out.</b> A não devolução acarreta o custo de reposição.",
    en: "<b>The card must be returned to the front desk at check-out.</b> Failure to return it incurs the replacement cost.",
    es: "<b>La tarjeta debe devolverse en recepción al hacer el check-out.</b> La no devolución genera el costo de reposición." },
  chave: {
    pt: "O acesso ao prédio é pela recepção, mediante apresentação de documento com foto e conferência desta lista de hóspedes. O acesso ao apartamento é por <b>chave física</b>, retirada na recepção.",
    en: "Building access is through the front desk, on presentation of a photo ID and a check against this guest list. Access to the apartment is by <b>physical key</b>, collected at the front desk.",
    es: "El acceso al edificio es por la recepción, presentando documento con foto y verificando esta lista de huéspedes. El acceso al apartamento es con <b>llave física</b>, retirada en recepción." },
  chave2: {
    pt: "<b>A chave deve ser devolvida na recepção no check-out.</b> A não devolução acarreta o custo de troca do segredo.",
    en: "<b>The key must be returned to the front desk at check-out.</b> Failure to return it incurs the cost of changing the lock.",
    es: "<b>La llave debe devolverse en recepción al hacer el check-out.</b> La no devolución genera el costo del cambio de cerradura." },
  recepcao: {
    pt: "O prédio cadastra o reconhecimento facial de cada hóspede na recepção, mediante documento com foto e conferência desta lista. Quem não estiver na lista não entra.",
    en: "The building registers each guest's facial recognition at the front desk, on presentation of a photo ID and a check against this list. Anyone not on the list cannot come in.",
    es: "El edificio registra el reconocimiento facial de cada huésped en recepción, con documento con foto y verificación de esta lista. Quien no esté en la lista no entra." }
};

/* Áreas comuns / estacionamento reutilizados. */
var AREAS = {
  dna: {
    pt: "O uso das áreas comuns segue o regimento do condomínio. Piscina e espaço gourmet ficam liberados, de sexta a domingo, apenas para estadias de 3 noites ou mais; o salão de festas não está disponível para hospedagem por temporada.",
    en: "Use of the common areas follows the building's rules. The pool and gourmet area are available, Friday to Sunday, only for stays of 3 nights or more; the party room is not available for short stays.",
    es: "El uso de las áreas comunes sigue el reglamento del condominio. La piscina y el espacio gourmet quedan liberados, de viernes a domingo, solo para estadías de 3 noches o más; el salón de fiestas no está disponible para hospedaje temporario." },
  marista: {
    pt: "O uso das áreas comuns — piscina da cobertura, academia, sauna, salas de reunião e espaço gourmet — segue o regimento interno do condomínio. Horários, necessidade de reserva e eventual custo são confirmados na recepção.",
    en: "Use of the common areas — rooftop pool, gym, sauna, meeting rooms and gourmet space — follows the building's internal rules. Opening hours, booking requirements and any cost are confirmed at the front desk.",
    es: "El uso de las áreas comunes — piscina de la azotea, gimnasio, sauna, salas de reunión y espacio gourmet — sigue el reglamento interno del condominio. Horarios, reserva previa y eventual costo se confirman en recepción." },
  condominio: {
    pt: "O uso das áreas comuns segue o regimento interno do condomínio, inclusive quanto a horários e à proibição de fumar.",
    en: "Use of the common areas follows the building's internal rules, including opening hours and the smoking ban.",
    es: "El uso de las áreas comunes sigue el reglamento interno del condominio, incluidos los horarios y la prohibición de fumar." },
  manobrista: {
    pt: "O estacionamento com manobrista e o café da manhã do restaurante do mezanino são <b>serviços pagos à parte</b>, não inclusos na diária, sujeitos à disponibilidade.",
    en: "Valet parking and breakfast at the mezzanine restaurant are <b>paid services</b>, not included in the nightly rate, subject to availability.",
    es: "El estacionamiento con valet y el desayuno del restaurante del entrepiso son <b>servicios pagos aparte</b>, no incluidos en la tarifa, sujetos a disponibilidad." },
  garagem_winner: {
    pt: "O controle do portão da garagem fica sobre a mesa da sala de jantar e deve ser devolvido no mesmo local no check-out.",
    en: "The garage gate remote is on the dining table and must be left in the same place at check-out.",
    es: "El control del portón de la cochera está sobre la mesa del comedor y debe dejarse en el mismo lugar al hacer el check-out." }
};

var PETS_WINNER = {
  t: { pt: "Dos animais", en: "Pets", es: "De los animales" },
  p: [ { pt: "Animais de estimação <b>dependem de autorização prévia</b> da aluGO, caso a caso. Animal não autorizado acarreta o custo de higienização especial da unidade.",
         en: "Pets <b>require prior authorisation</b> from aluGO, case by case. An unauthorised animal incurs the cost of a special deep clean of the unit.",
         es: "Las mascotas <b>requieren autorización previa</b> de aluGO, caso por caso. Un animal no autorizado genera el costo de una higienización especial de la unidad." } ]
};

function crystal(unidade, tipo){
  return { predio: "Crystal Place", unidade: unidade, bairro: "Setor Oeste",
    endereco: "Av. Edmundo P. de Abreu, 31, Setor Oeste, Goiânia/GO",
    capacidade: 4, checkin: "14h", checkout: "11h",
    acesso: ACESSO[tipo], acesso2: ACESSO[tipo+"2"], areas_comuns: AREAS.condominio,
    guia: "guia-crystal-" + unidade.replace(/\D/g,"") + ".html" };
}

window.UNIDADES = {
  /* ---- Crystal Place (recepção com reconhecimento facial) ---- */
  "CP-911":  Object.assign(crystal("Suíte 911", "fechadura"),  { capacidade: 3 }),
  "CP-209":  Object.assign(crystal("Suíte 209", "fechadura"),  { capacidade: 3 }),
  "CP-2413": crystal("Flat 2413", "cartao"),
  "CP-1313": crystal("Flat 1313", "chave"),
  "CP-1113": crystal("Flat 1113", "cartao"),

  /* ---- Sidney Metropolitan ---- */
  "SM-1202O": { predio: "Metropolitan Sidney", unidade: "Studio 1202O", bairro: "Jardim Goiás",
    endereco: "Edifício Metropolitan Sidney, Jardim Goiás, Goiânia/GO", capacidade: 2,
    checkin: "14h", checkout: "11h", acesso: ACESSO.recepcao, areas_comuns: AREAS.condominio,
    guia: "guia-sidney-1202O.html" },
  "SM-504T": { predio: "Metropolitan Sidney", unidade: "Apto 504T", bairro: "Jardim Goiás",
    endereco: "Edifício Metropolitan Sidney, Jardim Goiás, Goiânia/GO", capacidade: 4,
    checkin: "14h", checkout: "11h", acesso: ACESSO.recepcao, areas_comuns: AREAS.condominio,
    guia: "guia-sidney-504T.html" },

  /* ---- QS Marista (hotel: recepção 24h + cartão) ---- */
  "QS-1701": { predio: "QS Marista", unidade: "Suíte 1701", bairro: "Setor Marista",
    endereco: "Rua 145, nº 120, Setor Marista, Goiânia/GO", capacidade: 2,
    camas: { pt: ", em 1 cama de casal", en: ", in 1 double bed", es: ", en 1 cama de matrimonio" },
    checkin: "15h", checkout: "12h",
    acesso: ACESSO.cartao, acesso2: ACESSO.cartao2, areas_comuns: AREAS.marista, estacionamento: AREAS.manobrista,
    decl_extra: [ { pt: "Estou ciente de que o cartão magnético de acesso deve ser devolvido na recepção no check-out.",
                    en: "I understand the access keycard must be returned to the front desk at check-out.",
                    es: "Sé que la tarjeta magnética de acceso debe devolverse en recepción al hacer el check-out." } ],
    guia: "guia-marista-1701.html" },
  "QS-402": { predio: "QS Marista", unidade: "Suíte 402", bairro: "Setor Marista",
    endereco: "Rua 145, nº 120, Setor Marista, Goiânia/GO", capacidade: 4,
    camas: { pt: ", em 1 cama de casal e 1 de solteiro", en: ", in 1 double and 1 single bed", es: ", en 1 cama de matrimonio y 1 individual" },
    checkin: "15h", checkout: "12h",
    acesso: ACESSO.cartao, acesso2: ACESSO.cartao2, areas_comuns: AREAS.marista, estacionamento: AREAS.manobrista,
    decl_extra: [ { pt: "Estou ciente de que o cartão magnético de acesso deve ser devolvido na recepção no check-out.",
                    en: "I understand the access keycard must be returned to the front desk at check-out.",
                    es: "Sé que la tarjeta magnética de acceso debe devolverse en recepción al hacer el check-out." } ],
    guia: "guia-marista-402.html" },
  "QS-1310": { predio: "QS Marista", unidade: "Suíte 1310", bairro: "Setor Marista",
    endereco: "Rua 145, nº 120, Setor Marista, Goiânia/GO", capacidade: 2,
    camas: { pt: " (2 adultos e 1 bebê)", en: " (2 adults and 1 baby)", es: " (2 adultos y 1 bebé)" },
    checkin: "15h", checkout: "12h",
    acesso: ACESSO.recepcao, areas_comuns: AREAS.marista, estacionamento: AREAS.manobrista,
    guia: "guia-marista-1310.html" },

  /* ---- Walk Bueno ---- */
  "WB-2903": { predio: "Walk Bueno", unidade: "Duplex 2903", bairro: "Setor Bueno",
    endereco: "Edifício Walk Bueno, Setor Bueno, Goiânia/GO", capacidade: 4,
    checkin: "15h", checkout: "12h", acesso: ACESSO.recepcao, areas_comuns: AREAS.condominio,
    clausulas_extra: [ { t: { pt: "Dos objetos pessoais do proprietário", en: "The owner's personal items", es: "De los objetos personales del propietario" },
      p: [ { pt: "As peças de decoração, guitarras e demais objetos pessoais expostos no apartamento <b>não devem ser manuseados</b>. A adega e a cervejeira são de uso livre, mas não devem ser retiradas do local.",
             en: "The decorative pieces, guitars and other personal items displayed in the apartment <b>must not be handled</b>. The wine cooler and beer fridge may be used freely but must not be moved.",
             es: "Las piezas de decoración, guitarras y demás objetos personales expuestos en el apartamento <b>no deben manipularse</b>. La cava y la heladera de cerveza son de uso libre, pero no deben retirarse del lugar." } ] } ],
    decl_extra: [ { pt: "Estou ciente de que não devo manusear as decorações pessoais e de que a adega e a cervejeira não devem ser retiradas do local.",
                    en: "I understand I must not handle the personal decorations and that the wine cooler and beer fridge must not be moved.",
                    es: "Sé que no debo manipular las decoraciones personales y que la cava y la heladera de cerveza no deben retirarse del lugar." } ],
    guia: "guia-2903-walk-bueno-v20.html" },

  /* ---- Dna Smart / DNA SmartStyle (fechadura digital) ---- */
  "DS-407B": { predio: "Dna Smart", unidade: "Flat 407B", bairro: "Setor Bueno",
    endereco: "Edifício Dna Smart, Setor Bueno, Goiânia/GO", capacidade: 4,
    checkin: "15h", checkout: "12h",
    acesso: ACESSO.fechadura, acesso2: ACESSO.fechadura2, areas_comuns: AREAS.condominio },
  "DS-2003B": { predio: "DNA SmartStyle", unidade: "Duplex 2003 · Torre B", bairro: "Setor Bueno",
    endereco: "R. T-37, 2300, Setor Bueno, Goiânia/GO", capacidade: 4,
    camas: { pt: ", em 1 cama queen na suíte e 1 sofá-cama na sala", en: ", in 1 queen bed in the suite and 1 sofa bed in the living room", es: ", en 1 cama queen en la suite y 1 sofá cama en la sala" },
    checkin: "15h", checkout: "12h", silencio: "22h e 8h",
    acesso: ACESSO.fechadura, acesso2: ACESSO.fechadura2, areas_comuns: AREAS.dna,
    guia: "guia-dna-2003B.html" },
  "DS-1008B": { predio: "DNA SmartStyle", unidade: "Apto 1008B", bairro: "Setor Bueno",
    endereco: "R. T-37, 2300, Setor Bueno, Goiânia/GO", capacidade: 3,
    camas: { pt: ", contando crianças", en: ", children included", es: ", contando niños" },
    checkin: "15h", checkout: "12h", pede_telefone: true,
    acesso: ACESSO.fechadura, acesso2: ACESSO.fechadura2, areas_comuns: AREAS.dna,
    decl_extra: [ { pt: "Estou ciente de que não são permitidos animais de estimação na unidade.",
                    en: "I understand pets are not allowed in the unit.",
                    es: "Sé que no se permiten mascotas en la unidad." } ],
    guia: "guia-dna-1008B.html" },

  /* ---- Tai Residencial ---- */
  "TR-803S": { predio: "Tai Residencial", unidade: "Flat 803S", bairro: "Setor Bueno",
    endereco: "Edifício Tai Residencial, Setor Bueno, Goiânia/GO", capacidade: 4,
    checkin: "15h", checkout: "12h",
    acesso: ACESSO.fechadura, acesso2: ACESSO.fechadura2, areas_comuns: AREAS.condominio },

  /* ---- Blend Smart Style ---- */
  "BLE-757": { predio: "Blend Smart Style", unidade: "Apto 757", bairro: "Setor Marista",
    endereco: "R. T-55, 95, Setor Marista, Goiânia/GO", capacidade: 5,
    checkin: "15h", checkout: "12h", silencio: "22h e 8h",
    acesso: ACESSO.fechadura, acesso2: ACESSO.fechadura2, areas_comuns: AREAS.condominio,
    guia: "guia-blend-757.html" },

  /* ---- Winner (telefone do titular obrigatório; pets com autorização) ---- */
  "WIN-503C": { predio: "Winner Sport Life", unidade: "Apto 503 · Torre Conquista", bairro: "Jardim Goiás",
    endereco: "Rua 13, nº 45, Jardim Goiás, Goiânia/GO", capacidade: 4,
    camas: { pt: ", em 1 cama king e 1 cama queen", en: ", in 1 king and 1 queen bed", es: ", en 1 cama king y 1 cama queen" },
    checkin: "14h", checkout: "11h", pede_telefone: true,
    acesso: ACESSO.fechadura, acesso2: AREAS.garagem_winner, areas_comuns: AREAS.condominio,
    sem: ["animais"], clausulas_extra: [ PETS_WINNER ],
    guia: "guia-winner-503C.html" }
};
