"""Padroniza o horário de silêncio em 22h–8h (Pedro, 06/11/2026)."""
import re, sys
R = [
 # pt
 (r'22h às 0?7h', '22h às 8h'), (r'22h e 0?7h', '22h e 8h'),
 (r'Silêncio depois das 22h', 'Silêncio das 22h às 8h'),
 (r'Silêncio a partir das 22h', 'Silêncio das 22h às 8h'),
 (r'silêncio é obrigatório a partir das <b>22h</b>', 'silêncio é obrigatório das <b>22h às 8h</b>'),
 (r'([Ss])ilêncio após as 22h', r'\1ilêncio das 22h às 8h'),
 (r'Após as 22h, pedimos silêncio', 'Das 22h às 8h, pedimos silêncio'),
 (r'Barulho após as 22h', 'Barulho entre 22h e 8h'),
 (r'<b>Silêncio\.</b> Dom–qui 22h→8h · vésperas/sex/sáb 24h→9h · Natal e Ano Novo 3h→9h\.', '<b>Silêncio.</b> Das 22h às 8h.'),
 # en
 (r'10 pm–7 am', '10 pm–8 am'), (r'10pm–7am', '10pm–8am'),
 (r'10 ?pm to 7 ?am', lambda m: m.group(0).replace('7', '8')),
 (r'10pm and 7am', '10pm and 8am'),
 (r'Quiet after 10 pm', 'Quiet hours 10 pm–8 am'),
 (r'Quiet is mandatory from <b>10 pm</b>', 'Quiet is mandatory from <b>10 pm to 8 am</b>'),
 (r'Quiet from 10 pm"', 'Quiet from 10 pm to 8 am"'),
 (r'Quiet hours after 10 pm', 'Quiet hours 10 pm to 8 am'),
 (r'Noise after 10 pm', 'Noise between 10 pm and 8 am'),
 # es
 (r'de 22 a 7 h', 'de 22 a 8 h'), (r'22h a 0?7h', '22h a 8h'),
 (r'de las 22h a las 7h', 'de las 22h a las 8h'),
 (r'Silencio después de las 22 h', 'Silencio de 22 h a 8 h'),
 (r'Silencio a partir de las 22 h', 'Silencio de 22 h a 8 h'),
 (r'silencio es obligatorio a partir de las <b>22 h</b>', 'silencio es obligatorio de <b>22 h a 8 h</b>'),
 (r'El silencio después de las 22h', 'El silencio de 22h a 8h'),
 (r'Ruido después de las 22h', 'Ruido entre las 22h y las 8h'),
]
def silencio(s):
    for a, b in R: s = re.sub(a, b, s)
    return s
if __name__ == '__main__':
    tot = 0
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read(); n = silencio(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n); tot += 1; print('mudou', f)
    print(tot, 'arquivos')
