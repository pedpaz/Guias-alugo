"""Gera a base v2 do guia BLE-757 (Blend Smart Style) a partir do guia antigo (formato CFG + TXT.telas).
Esqueleto: guia v2 do DS-407B (978a1cb). Conteúdo: o próprio Blend, blocos convertidos para o formato v2.
uso: python3 montar-base-BLE757.py   → reescreve guia-blend-757.html (depois: montar.py 757)"""
import json, os, re, subprocess
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(P))
TMP = '/tmp/conv-757'; os.makedirs(TMP, exist_ok=True)
def git(ref, arq): return subprocess.run(['git', '-C', R, 'show', f'{ref}:{arq}'], capture_output=True, check=True).stdout.decode()
velho = git('3aff36d', 'guia-blend-757.html'); base = git('978a1cb', 'guia-dna-407B.html')

# conteúdo do guia antigo
a = velho.index('var CFG = {'); e = velho.index('</script>', a)
b = velho.index('var SINONIMOS = {'); c = velho.index('</script>', b)
js = velho[a:e] + '\n' + (velho[b:c] if b > e else '')
js = js[:js.index('var L = ')] if 'var L = ' in js else js
open(f'{TMP}/fonte.js', 'w').write(js)
dump = subprocess.run(['node', '-e', "const fs=require('fs'),vm=require('vm');const x={};vm.createContext(x);"
    f"vm.runInContext(fs.readFileSync('{TMP}/fonte.js','utf8').replace(/^var /gm,'this.'),x);"
    "process.stdout.write(JSON.stringify({CFG:x.CFG,TELAS:x.TELAS,TXT:x.TXT,SIN:x.SINONIMOS}))"], capture_output=True, check=True).stdout.decode()
V = json.loads(dump); CFG = V['CFG']
fotos = json.loads(re.search(r'^var FOTOS = (\{.*\});\s*$', velho, re.M).group(1))
marca = re.search(r'^var MARCA_BLEND = ("[^"]*");', velho, re.M).group(1)

IDS = {'ape': 'porta', 'interior': 'ape', 'trabalhar': 'roupas'}
LS = ['pt', 'en', 'es']
ATENCAO = {'pt': 'atenção', 'en': 'heads-up', 'es': 'atención'}
foto_tela = {t['id']: t.get('foto') for t in V['TELAS'] if t.get('foto') and not t.get('ilu')}

def converte(tid_velho, d, L):
    out = {'titulo': d['titulo'], 'sub': d['sub'], 'lead': d['lead'], 'blocos': []}
    bl = out['blocos']; h_pend = None; extra = {}
    def novo(b):
        nonlocal h_pend
        if h_pend and 'h' not in b: b = {'h': h_pend, **b}
        h_pend = None; bl.append(b)
    for b in d['blocos']:
        if 'h' in b and len(b) == 1:
            if h_pend: bl.append({'h': h_pend})
            h_pend = b['h']; continue
        if 'p' in b and len(b) == 1:
            if bl and h_pend is None and bl[-1].get('_aberto'): bl[-1]['p'] += b['p']
            else: novo({'p': list(b['p']), '_aberto': True})
        elif 'ul' in b: novo({'p': list(b['ul']), '_aberto': True})
        elif 'chave' in b: novo({'p': ['<b>%s</b> — %s' % (x['k'], x['v']) for x in b['chave']]})
        elif 'passos' in b: novo({'p': ['%d. %s' % (i + 1, x) for i, x in enumerate(b['passos'])]})
        elif 'pill' in b: novo({'p': [' · '.join(b['pill'])]})
        elif 'dest' in b:
            x = b['dest']; nb = {'h': x['t'], 'p': [x['p']]}
            if x.get('tipo') in ('aviso', 'proibido'): nb.update(dest=True, pill=ATENCAO[L])
            if h_pend: bl.append({'h': h_pend}); h_pend = None
            bl.append(nb)
        elif 'chaveGrande' in b:
            novo({'dest': True, 'h': b['chaveGrande']['k'], 'chave': CFG[b['chaveGrande']['vKey']]})
        elif 'sanfona' in b: out['ac'] = [{'q': x['q'], 'r': [x['a']]} for x in b['sanfona']]
        elif 'checklist' in b: novo({'h': {'pt': 'Antes de ir', 'en': 'Before you go', 'es': 'Antes de irte'}[L], 'p': list(b['checklist'])})
        elif 'botaoWpp' in b: extra['btnZap'] = b['botaoWpp']
        elif 'botaoTermo' in b: extra['btnTermo'] = b['botaoTermo']
        elif 'vistoria' in b: extra.update(vistPh=b['vistoria']['ph'], vistBtn=b['vistoria']['botao'])
        elif 'checkout' in b:
            x = b['checkout']; extra.update(coSelo=x['selo'], coH=x['t'], coP=x['p'] + ' ' + x.get('rodape', ''), coBtn=x['botao'])
        elif 'mapa' in b: pass
        else: raise SystemExit('bloco desconhecido: %r' % b)
    if h_pend: bl.append({'h': h_pend})
    for x in bl: x.pop('_aberto', None)
    f = foto_tela.get(tid_velho)
    if f and bl: bl[0] = {'foto': f, **bl[0]}
    out.update(extra)
    return out

TXT = {}
base_dados = base[base.index('<script id="dados">'):]; base_dados = base_dados[:base_dados.index('</script>')]
txt_base = json.loads(re.search(r'var TXT = (\{.*\});?\s*$', base_dados, re.S).group(1).rstrip().rstrip(';'))
for L in LS:
    VT = V['TXT'][L]
    T = {k: v for k, v in txt_base[L].items() if not k.startswith('tela_')}
    for k, v in list(T.items()):
        if isinstance(v, str): T[k] = v.replace('DNA SmartStyle 407B', 'Blend Smart Style 757').replace('Flat 407 · Torre B', 'Blend 757')
    T['apeNome'] = 'Blend 757'
    T['apeSub'] = CFG['predio'] + ' · Setor Marista, Goiânia'
    for tid_velho, d in VT['telas'].items():
        tid = IDS.get(tid_velho, tid_velho)
        T['tela_' + tid] = converte(tid_velho, d, L)
    ck = T['tela_checkin']
    # o "Vistoria de chegada" e o texto dele viram os campos da vistoria do formato v2
    vb = [i for i, x in enumerate(ck['blocos']) if x.get('h') in ('Vistoria de chegada', 'Arrival inspection', 'Inspección de llegada')]
    if vb:
        x = ck['blocos'].pop(vb[0]); ck['vistH'] = x['h']; ck['vistP'] = ' '.join(x.get('p', []))
    else:
        ck['vistH'] = {'pt': 'Vistoria de chegada', 'en': 'Arrival inspection', 'es': 'Inspección de llegada'}[L]; ck['vistP'] = ''
    ok = [x for x in ck['blocos'] if not x.get('dest') and x.get('h') and x.get('p')]
    ck['vistItens'] = []; ck['vistNota'] = (ok[-1]['h'] + ' — ' + ok[-1]['p'][0]) if ok else ''
    if ok: ck['blocos'].remove(ok[-1])
    ck.setdefault('btnTermo', {'pt': 'Preencher o check-in online', 'en': 'Complete online check-in', 'es': 'Completar el check-in online'}[L])
    T['tela_chegar']['btnMapa'] = {'pt': 'Abrir no Google Maps', 'en': 'Open in Google Maps', 'es': 'Abrir en Google Maps'}[L]
    T['tela_problema'].setdefault('btnZap', {'pt': 'Falar com a aluGO', 'en': 'Message aluGO', 'es': 'Hablar con aluGO'}[L])
    # garagem: no guia antigo era um aviso dentro de "Como chegar"; vira tela própria (o card da vaga lê daqui)
    g = [x for x in T['tela_chegar']['blocos'] if x.get('dest') and 'aragem' in x.get('h', '') + x.get('p', [''])[0] or 'arking' in x.get('h', '')]
    T['tela_garagem'] = {'titulo': {'pt': 'A garagem', 'en': 'Parking', 'es': 'El garaje'}[L],
        'sub': {'pt': 'Rotativa · sujeita a disponibilidade', 'en': 'No fixed space · subject to availability', 'es': 'Rotativa · sujeta a disponibilidad'}[L],
        'lead': {'pt': 'Não existe vaga fixa da unidade.', 'en': 'The unit has no fixed parking space.', 'es': 'La unidad no tiene plaza fija.'}[L],
        'blocos': [dict(g[0])] if g else []}
    TXT[L] = T

SIN = {L: {IDS.get(k, k): v for k, v in (V['SIN'] or {}).get(L, {}).items()} for L in LS}
for L in LS: SIN[L]['garagem'] = {'pt': ['garagem', 'vaga', 'estacionamento', 'carro', 'rotativa'], 'en': ['parking', 'garage', 'car', 'space'], 'es': ['cochera', 'garaje', 'estacionamiento', 'plaza']}[L]

TELAS = open(f'{P}/telas-v2-padrao.js').read()
rend = base_dados[:base_dados.index('var MAPA_URL')].replace('DS-407B · DNA SmartStyle', 'BLE-757 · Blend Smart Style')
dados = (rend + 'var MAPA_URL = %s;\n\n' % json.dumps(CFG['maps']) + TELAS + '\n\nvar SINONIMOS = ' + json.dumps(SIN, ensure_ascii=False, indent=1) +
         ';\n\nvar TXT = ' + json.dumps(TXT, ensure_ascii=False, indent=1) + ';\n')
s = base.replace(base_dados, dados)
fotos['hero'] = fotos[CFG['fotoHero']]
def troca_var(s, nome, valor):
    s2, n = re.subn(r'^var %s\s*=.*$' % nome, lambda m: f'var {nome} = {valor};', s, count=1, flags=re.M); assert n == 1, nome; return s2
s = troca_var(s, 'UNIDADE', json.dumps(CFG['unidade'])); s = troca_var(s, 'TERMO_URL', json.dumps(CFG['termo']))
s = troca_var(s, 'SENHA', json.dumps(CFG['senhaPorta'])); s = troca_var(s, 'WIFI_REDE', json.dumps(CFG['wifiRede']))
s = troca_var(s, 'WIFI_SENHA', json.dumps(CFG['wifiSenha'])); s = troca_var(s, 'MARCA_PREDIO', marca)
s = troca_var(s, 'FOTOS', json.dumps(fotos)); s = troca_var(s, 'CARDS', '{}')
s = re.sub(r'<title>[^<]*</title>', '<title>Blend Smart Style 757 · Guia da estadia</title>', s, 1)
assert '407' not in re.sub(r'data:[^"]+', '', s.split('<script id="dados">')[0]), 'sobrou 407 na config'
open(f'{R}/guia-blend-757.html', 'w', encoding='utf-8').write(s)
print('ok', len(s), [k for k in TXT['pt'] if k.startswith('tela_')])
