"""Gera a base v2 (TELAS/TXT/SINONIMOS) do WIN-503C (Winner Sport Life, 503 Torre Conquista) a partir do
guia antigo (telas HTML `<section class="scr" id="<lang>-<tela>">` nos 3 idiomas). Cada tela vira um bloco
de dados v2 com o mesmo texto; os subtítulos vêm do menu antigo. Esqueleto: guia v2 do DS-407B (978a1cb).
uso: python3 montar-base-WIN503C.py → reescreve guia-winner-503C.html (depois: montar.py 503C)"""
import json, os, re, subprocess
from bs4 import BeautifulSoup, NavigableString
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(P))
def git(ref, arq): return subprocess.run(['git', '-C', R, 'show', f'{ref}:{arq}'], capture_output=True, check=True).stdout.decode()
base = git('978a1cb', 'guia-dna-407B.html')
velho = git('55340a4', 'guia-winner-503C.html')
LS = ['pt', 'en', 'es']
IDS = {'chegar': 'chegar', 'garagem': 'garagem', 'subir': 'porta', 'smart': 'smart', 'apto': 'ape', 'cozinha': 'cozinha', 'lazer': 'lazer',
       'regras': 'regras', 'problema': 'problema', 'bairro': 'bairro', 'checkin': 'checkin', 'saida': 'saida'}

# fotos do guia antigo (mesmas chaves)
i = re.search(r'(?:var|const|let)\s+FOTOS\s*=\s*', velho).end(); j = velho.index('};', i) + 1
FOTOS = json.loads(velho[i:j])
semsvg = re.sub(r'<svg[\s\S]*?</svg>', '', velho)
soup = BeautifulSoup(semsvg, 'html.parser')

def inner(t):
    """HTML interno, só com <b>/<i>/<a>/<br>"""
    h = ''.join(str(c) for c in t.contents).strip()
    h = re.sub(r'<(?!/?(b|i|a|br)\b)[^>]+>', '', h)
    return re.sub(r'\s+', ' ', h).strip()

def converte(sec, L):
    d = {'titulo': '', 'sub': '', 'lead': '', 'blocos': []}; bl = d['blocos']; foto_pend = None; extra = {}
    for ch in sec.find_all(recursive=False):
        cl = ' '.join(ch.get('class', []))
        if ch.name == 'button' and 'back' in cl: continue
        if ch.name == 'h2': d['titulo'] = ch.get_text(' ', strip=True); continue
        if ch.name == 'figure':
            img = ch.find('img'); cap = ch.find('figcaption')
            foto_pend = (img.get('data-p'), cap.get_text(' ', strip=True) if cap else '')
            continue
        b = {}
        if foto_pend:
            b['foto'] = foto_pend[0]
        if ch.name == 'div' and cl.startswith('blk'):
            h3 = ch.find('h3'); dado = ch.find(class_='dado')
            if h3: b['h'] = h3.get_text(' ', strip=True)
            ps = [inner(p) for p in ch.find_all('p')]
            uls = [inner(li) for li in ch.find_all('li')]
            if ps: b['p'] = ps
            if uls: b['ul'] = uls
            if dado: b['chave'] = dado.get_text('', strip=True); b['dest'] = True
            if 'alert' in cl or 'dest' in cl: b['dest'] = True
        elif ch.name == 'ol':
            b['p'] = ['<b>%d.</b> %s' % (k + 1, inner(li)) for k, li in enumerate(ch.find_all('li'))]
        elif ch.name == 'div' and cl == 'warn':
            b.update(dest=True, p=[inner(p) for p in ch.find_all('p')])
        elif ch.name == 'div' and cl == 'big':
            b.update(dest=True, chave=ch.get_text(' ', strip=True))
        elif ch.name == 'div' and cl == 'minigrid':
            b['ul'] = [m.get_text(' ', strip=True) for m in ch.select('.mini')]
        elif ch.name == 'div' and cl == 'cmd-group':
            h3 = ch.find('h3'); b['h'] = h3.get_text(' ', strip=True) if h3 else ''
            b['ul'] = ['<b>%s</b> — %s' % (c.select_one('.cmd-q').get_text(' ', strip=True), c.select_one('.cmd-a').get_text(' ', strip=True)) for c in ch.select('.cmd')]
        elif ch.name == 'details':
            d.setdefault('ac', []).append({'q': ch.find('summary').get_text(' ', strip=True), 'r': [inner(p) for p in ch.find_all('p')] or [inner(ch).split('</summary>')[-1]]})
            continue
        elif ch.name in ('a', 'button') and 'btn' in cl:
            continue   # botões (mapa, copiar endereço) — o v2 tem os próprios
        elif ch.name == 'div' and cl == 'vist':
            extra['vistH'] = ch.find('h3').get_text(' ', strip=True)
            extra['vistP'] = inner(ch.find('p', class_='lead')) + ' ' + ' '.join(inner(p) for p in ch.select('.warn p'))
            extra['vistItens'] = [i.get('data-v') for i in ch.select('input[data-v]')]
            ta = ch.find('textarea'); extra['vistPh'] = ta.get('placeholder', '') if ta else ''
            bt = ch.find('button'); extra['vistBtn'] = bt.get_text(' ', strip=True) if bt else ''
            nota = ch.select('p:not(.lead):not(.lbl)'); extra['vistNota'] = inner(nota[-1]) if nota else ''
            continue
        elif ch.name == 'div' and cl == 'co':
            extra.update(coSelo='⚠ ' + ch.select_one('.co-seal').get_text(' ', strip=True), coH=ch.select_one('.co-title').get_text(' ', strip=True),
                         coP=inner(ch.select_one('.co-text')), coBtn=ch.select_one('.co-btn').get_text(' ', strip=True))
            continue
        else:
            raise SystemExit('elemento não tratado: %s.%s em %s' % (ch.name, cl, sec.get('id')))
        if foto_pend and foto_pend[1] and 'h' not in b: b['h'] = foto_pend[1]
        foto_pend = None
        if len(b) > (1 if 'foto' in b else 0): bl.append(b)
    if foto_pend: bl.append({'foto': foto_pend[0], 'p': [foto_pend[1]]})
    d.update(extra)
    return d

TXT = {}
txt_base = json.loads(re.search(r'var TXT = (\{.*\});?\s*$', base[base.index('<script id="dados">'):base.index('</script>', base.index('<script id="dados">'))], re.S).group(1).rstrip().rstrip(';'))
for L in LS:
    x = lambda pt, en, es: {'pt': pt, 'en': en, 'es': es}[L]
    T = {k: v for k, v in txt_base[L].items() if not k.startswith('tela_')}
    rot = 'Winner 503 · Torre Conquista'
    T.update(apeNome=x('Apartamento 503', 'Apartment 503', 'Apartamento 503'), apeSub='Winner Sport Life Residence · Jardim Goiás, Goiânia',
             cSenhaSub=x('fechadura digital · termine com *', 'digital lock · end with *', 'cerradura digital · termina con *'),
             cHorasVal=x('15h / 12h', '3pm / 12pm', '15h / 12h'), cHorasSub=x('entrada a partir das 15h · saída até as 12h', 'check-in from 3pm · check-out by 12pm', 'entrada desde las 15h · salida hasta las 12h'),
             buscaPh=x('O que você procura? (toalha, vaga, senha…)', 'What are you looking for? (towel, parking, code…)', '¿Qué buscas? (toalla, cochera, clave…)'),
             zapOi=x(f'Olá! Sou hóspede do {rot} e preciso de ajuda.', f"Hi! I'm a guest at {rot} and I need some help.", f'¡Hola! Soy huésped del {rot} y necesito ayuda.'),
             zapCheckout=x(f'Olá! Estou fazendo o check-out do {rot}. Já deixei o apartamento.', f"Hi! I'm checking out of {rot}. I've already left the apartment.", f'¡Hola! Estoy haciendo el check-out del {rot}. Ya dejé el departamento.'),
             vistMsg=x(f'Vistoria de chegada — {rot}. Encontrei:', f'Arrival inspection — {rot}. I found:', f'Inspección de llegada — {rot}. Encontré:'))
    home = soup.select_one(f'#{L}-home')
    subs = {t['data-k']: t.select_one('.ts').get_text(' ', strip=True) for t in home.select('button.tile[data-k]')}
    for velho_id, tid in IDS.items():
        sec = soup.select_one(f'#{L}-{velho_id}')
        d = converte(sec, L)
        s = subs.get(velho_id, ''); d['sub'] = s[:1].upper() + s[1:]
        if tid == 'chegar': d['btnMapa'] = x('Abrir no Google Maps', 'Open in Google Maps', 'Abrir en Google Maps')
        if tid == 'problema':
            d['btnZap'] = x('Falar com a gente no WhatsApp', 'Message us on WhatsApp', 'Hablar con nosotros por WhatsApp')
            d['lead'] = x('Quase tudo aqui se resolve sem esperar. Se não resolver, o WhatsApp está no fim desta tela.', 'Most things here can be fixed straight away. If not, WhatsApp is at the end of this screen.',
                          'Casi todo aquí se resuelve sin esperar. Si no, el WhatsApp está al final de esta pantalla.')
        if tid == 'checkin': d['btnTermo'] = x('Preencher o check-in online', 'Fill in the online check-in', 'Completar el check-in online')
        # 'chave' grande só para senha e vaga; o resto (endereço, capacidade, horário) vira texto
        for b in d['blocos']:
            ch = b.get('chave')
            if not ch: continue
            if tid == 'porta': continue
            if tid == 'garagem': b['chave'] = re.sub(r'\D', '', ch); b.setdefault('h', x('A sua vaga', 'Your space', 'Tu cochera')); continue
            if tid == 'saida': b.pop('chave'); b['h'] = x('Check-out até as 12h', 'Check-out by 12 pm', 'Check-out hasta las 12 h'); continue
            b.pop('chave')
            if 'h' not in b: b['h'] = ch
            else: b.setdefault('p', []).insert(0, '<b>%s</b>' % ch)
        T['tela_' + tid] = d
    # regras: fumo em destaque com título; visitas proibidas; horários 15h/12h (Pedro, 15/10 — o guia antigo dizia 11h na saída)
    rg = T['tela_regras']['blocos']
    for b in rg:
        if b.get('dest') and 'h' not in b and re.search('fumar|smok|fumar', ' '.join(b.get('p', [])), re.I):
            b['h'] = x('🚭 Proibido fumar', '🚭 No smoking', '🚭 Prohibido fumar'); b['pill'] = x('proibido', 'not allowed', 'prohibido')
    rg.insert(1, dict(dest=True, h=x('Visitas não são permitidas', 'No visitors', 'No se permiten visitas'),
                      p=[x('Só os hóspedes cadastrados no check-in online entram no condomínio e no apartamento.', 'Only the guests registered in the online check-in may enter the building and the apartment.',
                           'Solo los huéspedes registrados en el check-in online entran al condominio y al departamento.')]))
    T = json.loads(json.dumps(T, ensure_ascii=False).replace('11h', '12h').replace('11 h', '12 h').replace('11 am', '12 pm').replace('11am', '12pm')
                   .replace('11H', '12H').replace('11 AM', '12 PM'))
    T['tela_problema']['lead'] = ''
    T['tela_ape']['sub'] = x('2 suítes · até 4 hóspedes · 220V', '2 suites · up to 4 guests · 220V', '2 suites · hasta 4 huéspedes · 220V')
    TXT[L] = T

# sinônimos a partir do índice antigo (SYN), quando existir
SIN = {L: {} for L in LS}
m = re.search(r'(?:var|const|let)\s+SYN\s*=\s*', velho)
if m:
    k = m.end(); depth = 0
    for e in range(k, len(velho)):
        depth += {'{': 1, '}': -1}.get(velho[e], 0)
        if depth == 0: break
    try:
        syn = json.loads(velho[k:e + 1])
        for L in LS:
            for vid, lst in (syn.get(L) or syn).items():
                if vid in IDS and isinstance(lst, list): SIN[L][IDS[vid]] = lst
    except Exception as ex:
        print('SYN não aproveitado:', ex)

telas_js = open(f'{P}/telas-v2-padrao.js').read()
telas_js = re.sub(r"\n  \{id:'(roupas|predio)',[^\n]*", '', telas_js)
telas_js = telas_js.replace("  {id:'cozinha',", "  {id:'smart',    corpo:blocos},\n  {id:'cozinha',", 1)
bd = base[base.index('<script id="dados">'):]; bd = bd[:bd.index('</script>')]
rend = bd[:bd.index('var MAPA_URL')].replace('DS-407B · DNA SmartStyle', 'WIN-503C · Winner Sport Life')
MAPS = 'https://www.google.com/maps/search/?api=1&query=Winner+Sport+Life+Residence%2C+Rua+13%2C+45%2C+Jardim+Goi%C3%A1s%2C+Goi%C3%A2nia+-+GO'
s = base.replace(bd, rend + 'var MAPA_URL = %s;\n\n' % json.dumps(MAPS) + telas_js + '\n\nvar SINONIMOS = ' + json.dumps(SIN, ensure_ascii=False, indent=1) +
                 ';\n\nvar TXT = ' + json.dumps(TXT, ensure_ascii=False, indent=1) + ';\n')
def troca_var(s, nome, valor):
    s2, k = re.subn(r'^var %s\s*=.*$' % nome, lambda m: f'var {nome} = {valor};', s, count=1, flags=re.M); assert k == 1, nome; return s2
fotos = dict(FOTOS); fotos['hero'] = FOTOS['sala-01']
s = troca_var(s, 'UNIDADE', '"WIN-503C"'); s = troca_var(s, 'TERMO_URL', '"https://pedpaz.github.io/Guias-alugo/termo.html?u=WIN-503C"')
s = troca_var(s, 'SENHA', '"1001*"'); s = troca_var(s, 'WIFI_REDE', '"Renata Google"'); s = troca_var(s, 'WIFI_SENHA', '"re100984"')
s = troca_var(s, 'MARCA_PREDIO', '""'); s = troca_var(s, 'FOTOS', json.dumps(fotos)); s = troca_var(s, 'CARDS', '{}')
s = re.sub(r'<title>[^<]*</title>', '<title>Winner Sport Life · 503 Torre Conquista · Guia da estadia</title>', s, 1)
cfg = re.sub(r'data:[^"]+', '', s.split('<script id="dados">')[0]); assert '407' not in cfg
dd = s[s.index('<script id="dados">'):]; dd = dd[:dd.index('</script>')]
for proib in ['407', 'DNA Smart', '5562981771013']: assert proib not in dd, proib
open(f'{R}/guia-winner-503C.html', 'w', encoding='utf-8').write(s)
print('ok', len(s), {L: [k[5:] for k in TXT[L] if k.startswith('tela_')] == [k[5:] for k in TXT['pt'] if k.startswith('tela_')] for L in LS})
