"""Gera a base v2 do guia DS-1008B (formato de dados TELAS/TXT/SINONIMOS) a partir do guia antigo.
Esqueleto: guia v2 do DS-407B (mesmo prédio) na versão 978a1cb. Conteúdo: o próprio 1008B,
convertido por conv-1008B.js (as frases são as do guia antigo, nos 3 idiomas).
uso: python3 montar-base-1008B.py   → reescreve guia-dna-1008B.html (depois: montar.py 1008B)"""
import json, os, re, subprocess
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(P))
TMP = '/tmp/conv-1008B'; os.makedirs(TMP, exist_ok=True)

def git(ref, arq): return subprocess.run(['git', '-C', R, 'show', f'{ref}:{arq}'], capture_output=True, check=True).stdout.decode()
velho = git('92c6f60', 'guia-dna-1008B.html')          # guia antigo (formato próprio)
base = git('978a1cb', 'guia-dna-407B.html')             # esqueleto v2 do mesmo prédio

# 1) extrai o script de conteúdo do guia antigo e converte
a = velho.index('var UNIDADE='); b = velho.index('var L = (function')
code = velho[a:b]
fotos_velho = re.search(r'var FOTOS=(\{.*?\});\n', code, re.S).group(1)
code = re.sub(r'var FOTOS=\{.*?\};\n', 'var FOTOS={};\n', code, flags=re.S)
open(f'{TMP}/fonte.js', 'w').write(code)
subprocess.run(['node', f'{P}/conv-1008B.js', f'{TMP}/fonte.js', f'{TMP}/conv.json'], check=True)
conv = json.load(open(f'{TMP}/conv.json'))

SUBS = {
 'chegar':  ('Endereço, mapa e a torre certa', 'Address, map and the right tower', 'Dirección, mapa y la torre correcta'),
 'predio':  ('Portaria 24h e reconhecimento facial', '24h front desk and face ID', 'Portería 24 h y reconocimiento facial'),
 'porta':   ('10º andar · senha da fechadura', '10th floor · door code', 'Piso 10 · clave de la cerradura'),
 'ape':     ('1 quarto · 3 pessoas · 220V', '1 bedroom · 3 guests · 220V', '1 dormitorio · 3 personas · 220V'),
 'cozinha': ('Completa, dá para cozinhar', 'Fully equipped for cooking', 'Completa, para cocinar de verdad'),
 'garagem': ('Vaga 215 · 2º pavimento', 'Space 215 · level 2', 'Plaza 215 · 2º nivel'),
 'lazer':   ('Piscina, academia e jogos', 'Pool, gym and games', 'Piscina, gimnasio y juegos'),
 'roupas':  ('Lava e seca no apartamento', 'Washer-dryer in the flat', 'Lavasecadora en el depto'),
 'regras':  ('Curtas, e todas por um motivo', 'Short, and each one for a reason', 'Cortas, y cada una por un motivo'),
 'problema':('Resolva em 30 segundos', 'Fix it in 30 seconds', 'Resuélvelo en 30 segundos'),
 'bairro':  ('Setor Bueno · tudo a pé', 'Setor Bueno · all within walking distance', 'Setor Bueno · todo a pie'),
 'checkin': ('Dois minutos, e a sua entrada está liberada', 'Two minutes and your entry is cleared', 'Dos minutos y tu entrada queda liberada'),
 'saida':   ('Check-out até as 12h', 'Check-out by 12 pm', 'Check-out hasta las 12 h'),
}
IDS = {'apto': 'porta', 'casa': 'ape', 'lavar': 'roupas'}
LS = ['pt', 'en', 'es']
sem_tag = lambda s: re.sub(r'<[^>]+>', '', s or '').strip()

TXT = {}
base_dados = base[base.index('<script id="dados">'):]
base_dados = base_dados[:base_dados.index('</script>')]
txt_base = json.loads(re.search(r'var TXT = (\{.*\});?\s*$', base_dados, re.S).group(1).rstrip().rstrip(';'))

for i, L in enumerate(LS):
    I = conv[L]['I']; It = lambda k: I.get(k) or conv['pt']['I'].get(k, '')
    T = {k: v for k, v in txt_base[L].items() if not k.startswith('tela_')}
    for k, v in list(T.items()):
        if isinstance(v, str): T[k] = v.replace('407B', '1008B').replace('Flat 407', 'Apartamento 1008').replace('4º andar', '10º andar')
    T['apeNome'] = {'pt': 'Apartamento 1008 · Torre B', 'en': 'Apartment 1008 · Tower B', 'es': 'Apartamento 1008 · Torre B'}[L]
    T['cSenhaSub'] = It('apto_big')
    for velho_id, d in conv[L]['telas'].items():
        tid = IDS.get(velho_id, velho_id)
        d = dict(d); d['titulo'] = sem_tag(d['titulo']); d['sub'] = SUBS[tid][i]
        if tid == 'chegar': d['btnMapa'] = sem_tag(It('chegar_btn'))
        if tid == 'problema': d['btnZap'] = sem_tag(It('problema_btn'))
        if tid == 'checkin':
            d['blocos'] = [b for b in d['blocos'] if b.get('h') != It('c_vistoria')]
            d.update(btnTermo=sem_tag(It('checkin_btn')), vistH=It('c_vistoria'), vistP=It('vist_intro'),
                     vistItens=It('vist_itens').split('|'), vistPh=It('vist_ph'), vistBtn=sem_tag(It('vist_btn')), vistNota=It('vist_n1'))
        if tid == 'saida':
            d.update(coSelo=sem_tag(It('co_selo')), coH=sem_tag(It('co_tit')), coP=It('co_desc'), coBtn=sem_tag(It('co_btn')))
        T['tela_' + tid] = d
    # garagem: no guia antigo era uma linha em "Como chegar"; vira tela própria (o card da vaga lê daqui)
    T['tela_garagem'] = {'titulo': {'pt': 'A garagem', 'en': 'Parking', 'es': 'El garaje'}[L], 'sub': SUBS['garagem'][i],
        'lead': {'pt': 'O apartamento tem vaga própria, sem custo adicional.', 'en': 'The flat has its own parking space, at no extra cost.',
                 'es': 'El departamento tiene su propia plaza, sin costo adicional.'}[L],
        'blocos': [{'dest': True, 'h': {'pt': 'A sua vaga', 'en': 'Your space', 'es': 'Tu plaza'}[L], 'chave': '215', 'p': [It('chegar_gar')]}]}
    TXT[L] = T

# sinônimos do guia antigo, com os ids novos
ctx_sin = subprocess.run(['node', '-e', "const fs=require('fs'),vm=require('vm');const x={};vm.createContext(x);"
    f"vm.runInContext(fs.readFileSync('{TMP}/fonte.js','utf8').replace(/^var /gm,'this.'),x);process.stdout.write(JSON.stringify(x.SINONIMOS))"],
    capture_output=True, check=True).stdout.decode()
sin_velho = json.loads(ctx_sin); SIN = {}
for L in LS:
    SIN[L] = {IDS.get(k, k): v for k, v in sin_velho.get(L, {}).items()}
    SIN[L]['garagem'] = {'pt': ['vaga', 'garagem', 'estacionamento', 'carro', '215', 'onde estaciono'],
                         'en': ['parking', 'space', 'garage', 'car', '215'], 'es': ['cochera', 'garaje', 'estacionamiento', 'plaza', '215']}[L]

TELAS = """var TELAS = [
  {id:'chegar',   corpo:function(d){ return blocos(d)+'<a class="btn laranja" target="_blank" rel="noopener" href="'+MAPA_URL+'">'+d.btnMapa+'</a>'; }},
  {id:'predio',   corpo:blocos},
  {id:'porta',    corpo:blocos},
  {id:'ape',      corpo:blocos},
  {id:'cozinha',  corpo:blocos},
  {id:'garagem',  corpo:blocos},
  {id:'lazer',    corpo:blocos},
  {id:'roupas',   corpo:blocos},
  {id:'regras',   corpo:blocos},
  {id:'problema', tipo:'alerta', corpo:function(d){ return blocos(d)+acordeoes(d)+'<a class="btn laranja" href="#" onclick="zap(TXT[L].zapOi);return false">'+d.btnZap+'</a>'; }},
  {id:'bairro',   corpo:blocos},
  {id:'checkin',  larga:true, corpo:function(d){ return blocos(d)+
     '<a class="btn laranja" target="_blank" rel="noopener" href="'+TERMO_URL+'">'+d.btnTermo+'</a>'+
     '<div class="bloco"><h3>'+d.vistH+'</h3><p>'+d.vistP+'</p><div class="vist">'+
       d.vistItens.map(function(i){return '<label><input type="checkbox" data-item="'+i+'"><span>'+i+'</span></label>';}).join('')+
       '<textarea id="vistObs" placeholder="'+d.vistPh+'"></textarea></div>'+
     '<a class="btn linha" href="#" onclick="enviarVistoria();return false" style="margin-top:13px">'+d.vistBtn+'</a>'+
     '<p style="font-size:13px;color:var(--tinta-2);margin:10px 0 0">'+d.vistNota+'</p></div>'; }},
  {id:'saida',    saida:true, corpo:function(d){ return blocos(d)+
     '<div class="co"><span class="selo">'+d.coSelo+'</span><h3>'+d.coH+'</h3><p>'+d.coP+'</p>'+
     '<button class="co-btn" onclick="avisarCheckout()">'+d.coBtn+'</button></div>'; }}
];"""

# 2) monta o bloco de dados novo a partir do do 407B
rend = base_dados[:base_dados.index('var MAPA_URL')]
rend = rend.replace('DS-407B · DNA SmartStyle', 'DS-1008B · DNA SmartStyle')
dados_novo = (rend + 'var MAPA_URL = "https://maps.app.goo.gl/j8CLV2GZbMLrWVQUA";\n\n' + TELAS + '\n\nvar SINONIMOS = ' +
              json.dumps(SIN, ensure_ascii=False, indent=1) + ';\n\nvar TXT = ' + json.dumps(TXT, ensure_ascii=False, indent=1) + ';\n')
s = base.replace(base_dados, dados_novo)

# 3) configuração da unidade
fotos = json.loads(fotos_velho); fotos['hero'] = fotos['sala']
def troca_var(s, nome, valor):
    s2, n = re.subn(r'^var %s\s*=.*$' % nome, lambda m: f'var {nome} = {valor};', s, count=1, flags=re.M); assert n == 1, nome; return s2
s = troca_var(s, 'UNIDADE  ', '"DS-1008B"') if re.search(r'^var UNIDADE  ', s, re.M) else troca_var(s, 'UNIDADE', '"DS-1008B"')
s = troca_var(s, 'TERMO_URL', '"https://pedpaz.github.io/Guias-alugo/termo-dna-1008B.html"')
s = troca_var(s, 'SENHA', '"134679*"')
s = troca_var(s, 'WIFI_REDE', '"Smart T 5.0"')
s = troca_var(s, 'WIFI_SENHA', '"veiga5300"')
s = troca_var(s, 'FOTOS', json.dumps(fotos))
s = troca_var(s, 'CARDS', '{}')
s = re.sub(r'<title>[^<]*</title>', '<title>DNA SmartStyle 1008B · Guia da estadia</title>', s, 1)
assert '407' not in re.sub(r'data:[^"]+', '', s.split('<script id="dados">')[0]).replace('#E0761A', ''), 'sobrou 407 na config'
open(f'{R}/guia-dna-1008B.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
