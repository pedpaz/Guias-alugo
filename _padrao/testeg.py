import asyncio,sys
from playwright.async_api import async_playwright
ARQ=sys.argv[1]; import os; G='file://'+os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'+ARQ
import tempfile; D=tempfile.gettempdir()+'/guia-shots/'
import os; os.makedirs(D,exist_ok=True); tag=ARQ.replace('guia-','').replace('.html','')
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,locale='pt-BR')
        pg=await ctx.new_page(); erros=[]
        pg.on('pageerror',lambda e: erros.append(str(e)))
        pg.on('console',lambda m: erros.append('console:'+m.text) if m.type=='error' else None)
        await pg.goto(G); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=D+tag+'-home.png',full_page=True)
        info=await pg.evaluate("""({senha:document.getElementById('cPortaVal').textContent, wifi:document.getElementById('cWifiVal').textContent,
          rede:document.getElementById('cWifiRede').textContent, vaga:document.getElementById('cVagaVal').textContent,
          termo:document.getElementById('lnkTermo').href, tit:document.querySelector('.hero h1').textContent,
          n:document.querySelector('[data-u=nTopicos]').textContent, topicos:TOPICOS.map(t=>t.id+':'+t.telas.join('+')).join(' '),
          orfas:TELAS.filter(x=>!TOPICOS.some(t=>t.telas.indexOf(x.id)>=0)).map(x=>x.id),
          fech:!!document.querySelector('fechadura-anim'), vist:!!document.getElementById('vistoria')})""")
        for k,v in info.items(): print(' ',k,':',v)
        await pg.fill('#q','senha wifi'); await pg.wait_for_timeout(300)
        print('  busca:', (await pg.inner_text('#res'))[:100].replace('\n',' | '))
        for tid in [t.split(':')[0] for t in info['topicos'].split()]:
            await pg.evaluate(f"abrir('{tid}')"); await pg.wait_for_timeout(200)
        await pg.evaluate("abrir('entrar')"); await pg.wait_for_timeout(800)
        await pg.screenshot(path=D+tag+'-entrar.png',full_page=True)
        await pg.evaluate("irMenu()"); await pg.click('.lang button[data-l=en]'); await pg.wait_for_timeout(300)
        print('  en tit:', await pg.evaluate("document.querySelector('.hero h1').textContent"))
        print('  erros:', erros)
        await b.close()
asyncio.run(main())
