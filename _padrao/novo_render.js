/* ================= RENDER — padrão aluGO 2026 (10 tópicos) ================= */
var L = 'pt';
function t(k){ return (TXT[L]&&TXT[L][k]!=null)?TXT[L][k]:(TXT.pt[k]||''); }
/* textos próprios da unidade (UI_UNIDADE) por cima do padrão */
(function mesclar(a,b){ for(var k in b){ if(b[k]&&typeof b[k]==='object'&&!Array.isArray(b[k])&&a[k]&&typeof a[k]==='object') mesclar(a[k],b[k]); else a[k]=b[k]; } })(UI, (typeof UI_UNIDADE!=='undefined')?UI_UNIDADE:{});
function u(k){ return (UI[L]&&UI[L][k]!=null)?UI[L][k]:(UI.pt[k]!=null?UI.pt[k]:''); }
function foto(k,alt){ return FOTOS[k] ? '<div class="foto"><img loading="lazy" src="'+FOTOS[k]+'" alt="'+(alt||'')+'"></div>' : ''; }
function duo(a,b){ if(!FOTOS[a]||!FOTOS[b]) return foto(a)+foto(b);
  return '<div class="duo"><div class="foto"><img loading="lazy" src="'+FOTOS[a]+'" alt=""></div><div class="foto"><img loading="lazy" src="'+FOTOS[b]+'" alt=""></div></div>'; }

/* vaga da unidade: vem do bloco em destaque da tela "garagem" (fonte única) */
function acharVaga(){ var d=(TXT.pt&&TXT.pt.tela_garagem)||{}, b=(d.blocos||[]).filter(function(x){return x&&x.chave;})[0]; return b?String(b.chave):''; }
var VAGA = acharVaga();

/* Os 10 tópicos — mesma ordem, ícone e cor em TODOS os guias aluGO.
   Cada tópico junta uma ou mais telas do bloco de dados (TELAS/TXT), que
   continuam sendo a fonte da área do hóspede e da IA do atendimento. */
var TOPICOS = [
  {id:'checkin',    c:'#5B5BD6', b:'#ECECFB', telas:['checkin']},
  {id:'chegar',     c:'#2F6FDB', b:'#E6EEFB', telas:['chegar','predio','garagem']},
  {id:'entrar',     c:'#0A7A32', b:'#E3F3E8', telas:['porta','suite']},
  {id:'energia',    c:'#C97A00', b:'#FCF0D6', telas:['luz']},
  {id:'ape',        c:'#7A4FC2', b:'#EFE8FA', telas:['ape','duplex','cozinha','copa']},
  {id:'condominio', c:'#11867E', b:'#E0F3F1', telas:['lazer','murano','roupas']},
  {id:'regras',     c:'#4F5B57', b:'#E9EDEB', telas:['regras']},
  {id:'arredores',  c:'#C2457C', b:'#FBE6EF', telas:['bairro']},
  {id:'checkout',   c:'#D9631A', b:'#FCE9DC', telas:['saida']},
  {id:'ajuda',      c:'#0B2B22', b:'#E1E8E4', telas:['problema']}
];
/* guia com telas organizadas de outro jeito: TEMA.mapa troca as telas de um tópico */
if(TEMA.mapa) TOPICOS.forEach(function(tp){ if(TEMA.mapa[tp.id]) tp.telas=TEMA.mapa[tp.id].slice(); });
if(typeof MARCA_PREDIO==='undefined' || !MARCA_PREDIO) var MARCA_PREDIO = (typeof MARCA_DNA!=='undefined') ? MARCA_DNA : '';
if(typeof aviso!=='function') window.aviso=function(msg){
  var el=document.getElementById('aviso'); if(!el) return;
  el.textContent=msg; el.classList.add('on'); clearTimeout(window._avisoT2);
  window._avisoT2=setTimeout(function(){ el.classList.remove('on'); },4200);
};
/* cada guia só mostra as telas que tem; tópico sem tela some do menu */
TOPICOS.forEach(function(tp){ tp.telas=tp.telas.filter(function(tid){ return TELAS.some(function(x){return x.id===tid;}); }); });
TOPICOS=TOPICOS.filter(function(tp){ return tp.telas.length; });
function topico(id){ for(var i=0;i<TOPICOS.length;i++) if(TOPICOS[i].id===id) return TOPICOS[i]; return null; }
function topicoDaTela(tid){ for(var i=0;i<TOPICOS.length;i++) if(TOPICOS[i].telas.indexOf(tid)>=0) return TOPICOS[i]; return null; }
function telaDef(tid){ for(var i=0;i<TELAS.length;i++) if(TELAS[i].id===tid) return TELAS[i]; return null; }
/* subtítulo do tópico: o da unidade (UI_UNIDADE) ou, com TEMA.autoSub, o da tela principal */
var SUB_AUTO={entrar:'sub',condominio:'titulo',arredores:'sub',checkout:'sub'};
function subTopico(tp){
  var uu=(typeof UI_UNIDADE!=='undefined')&&UI_UNIDADE[L]&&UI_UNIDADE[L].topicos&&UI_UNIDADE[L].topicos[tp.id];
  if(uu&&uu.s) return uu.s;
  if(TEMA.autoSub&&SUB_AUTO[tp.id]){ var d=t('tela_'+tp.telas[0]); if(d&&d[SUB_AUTO[tp.id]]) return d[SUB_AUTO[tp.id]]; }
  return (u('topicos')[tp.id]||{}).s||'';
}
var CHEV='<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>';

/* ---------- TELA INICIAL ---------- */
function montarHome(){
  if(TEMA.autoSub&&topico('ape')){ var ap=t('tela_'+topico('ape').telas[0])||{}; if(ap.sub) document.getElementById('heroChip').textContent=ap.sub.replace(/\s*·\s*220V/i,''); }
  var pv=document.getElementById('cPortaVal');
  pv.textContent = SENHA || t('cAcessoVal'); pv.classList.toggle('longo', !SENHA);
  pv.classList.toggle('med', !!SENHA && SENHA.length>=8);
  if(!SENHA){ document.getElementById('cPortaRot').textContent=u('acessoRot'); document.getElementById('cPortaTap').textContent=u('verComo'); }
  document.getElementById('cWifiVal').textContent = WIFI_SENHA || t('cWifiPend');
  var wl=(WIFI_SENHA||'').length, wv=document.getElementById('cWifiVal');
  wv.classList.toggle('med', wl>=10 && wl<14); wv.classList.toggle('longo', wl>=14);
  document.getElementById('cWifiRede').textContent = WIFI_REDE ? (u('wifiRede')+' '+WIFI_REDE) : '';
  // energia: cartão "Sem luz?" só onde existe a tela do cartão de energia; senão, 220V
  // "Sem luz?" só onde existe o cartão de energia (faixa larga abaixo do essencial)
  document.querySelector('.e-luz').classList.toggle('esconde', !telaDef('luz'));
  // localização: endereço curto + abre o mapa
  var mapa=TEMA.mapsUrl||((typeof MAPA_URL!=='undefined')?MAPA_URL:''), cl=document.getElementById('cLocal');
  document.getElementById('cLocalNome').textContent=u('predioNome')||'';
  // ícones 3D do essencial (Gemini)
  [['icPorta','porta'],['icWifi','wifi'],['icLocal','local'],['icVaga','vaga']].forEach(function(p){
    var im=document.getElementById(p[0]); if(typeof ICS_ESS!=='undefined'&&ICS_ESS[p[1]]) im.src=ICS_ESS[p[1]]; else im.style.display='none'; });
  if(mapa){ cl.href=mapa; cl.onclick=null; } else { cl.removeAttribute('target'); cl.onclick=function(){ abrir('chegar'); return false; }; }
  // vaga: número em destaque; sem número, o resumo da tela da garagem
  var vv=document.getElementById('cVagaVal'), gar=t('tela_garagem')||{};
  var vagaVal=u('vagaVal')||VAGA;
  vv.textContent = vagaVal || gar.sub || ''; vv.classList.toggle('longo', !vagaVal);
  if(!vagaVal){ document.getElementById('cVagaRot').textContent=u('garagem'); document.getElementById('cVagaSub').textContent=''; }
  document.querySelector('.e-vaga').classList.toggle('esconde', !telaDef('garagem'));
  var nt=document.querySelector('[data-u="nTopicos"]'); if(nt) nt.textContent=u('nTopicos').replace('{n}',TOPICOS.length);
  var h='';
  TOPICOS.forEach(function(tp){
    var tx=u('topicos')[tp.id]||{};
    h+='<button onclick="abrir(\''+tp.id+'\')"><img class="ic" src="'+ICS[tp.id]+'" alt="">'+
       '<span class="tx"><b>'+(tx.t||'')+'</b><small>'+subTopico(tp)+'</small></span>'+CHEV+'</button>';
  });
  document.getElementById('lista').innerHTML=h;
  var chips=u('chips').slice(); if(!telaDef('luz')) chips[0]=u('chipAr');
  document.getElementById('chips').innerHTML = chips.map(function(c){
    return '<button onclick="perguntar(\''+c.replace(/'/g,"\\'")+'\')">'+c+'</button>'; }).join('');
}

/* ---------- TELAS DE TÓPICO ---------- */
function corpoTela(tid, comTitulo){
  var s=telaDef(tid); if(!s) return '';
  var d=t('tela_'+tid)||{};
  return '<div class="sec" id="sec-'+tid+'">'+
    (comTitulo?'<h2 class="sec-h">'+(d.titulo||'')+'</h2>'+(d.sub?'<p class="sec-s">'+d.sub+'</p>':''):'')+
    (d.lead?'<p class="lead">'+d.lead+'</p>':'')+
    (s.corpo?s.corpo(d):'')+'</div>';
}
function montarTelas(){
  var c=document.getElementById('telas'), h='';
  TOPICOS.forEach(function(tp,i){
    var tx=u('topicos')[tp.id]||{}, varias=tp.telas.length>1;
    var atalhos = varias ? '<div class="atalhos">'+tp.telas.map(function(tid){
        var d=t('tela_'+tid)||{}; return '<button onclick="irSec(\''+tid+'\')">'+(d.titulo||tid)+'</button>'; }).join('')+'</div>' : '';
    var prox=TOPICOS[i+1], pt=prox?(u('topicos')[prox.id]||{}):null;
    h+='<section class="tela" id="tela-'+tp.id+'" style="--tc:'+tp.c+';--tcb:'+tp.b+'">'+
      '<div class="ttopo"><div class="nav"><button class="voltar" onclick="irMenu()"><svg viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg>'+u('bGuia')+'</button>'+
      '<span class="pos">'+(i+1)+' '+u('de')+' '+TOPICOS.length+'</span></div>'+
      '<div class="tit"><img class="ic" src="'+ICS[tp.id]+'" alt=""><div><span class="k">'+u('topico')+' '+(i+1)+'</span><h1>'+(tx.t||'')+'</h1></div></div>'+
      atalhos+'</div>'+
      '<div class="tcorpo">'+tp.telas.map(function(tid){ return corpoTela(tid, varias); }).join('')+
      (prox?'<div class="prox"><small>'+u('proximo')+'</small><button onclick="abrir(\''+prox.id+'\')"><img class="ic" src="'+ICS[prox.id]+'" alt="">'+
        '<span class="tx"><b>'+(i+2)+' · '+(pt.t||'')+'</b><span>'+subTopico(prox)+'</span></span>'+CHEV+'</button></div>' : '')+
      '</div></section>';
  });
  c.innerHTML=h;
  // vistoria ganha âncora própria (#vistoria) para o atalho da tela inicial
  var vi=c.querySelector('#sec-checkin .vist'); if(vi){ var vb=vi.closest('.bloco'); if(vb) vb.id='vistoria'; }
  // tutorial animado da fechadura (Intelbras FR 101), o mesmo dos outros guias
  var tpE=topico('entrar'), sp=tpE?c.querySelector('#sec-'+tpE.telas[0]):null;
  if(sp && SENHA && TEMA.fechadura && !sp.querySelector('fechadura-anim')){
    var bl=sp.querySelectorAll('.bloco'), ref=bl[2]||bl[bl.length-1];
    var w=document.createElement('div'); w.className='anim-porta';
    w.innerHTML='<fechadura-anim senha="'+SENHA+'" cor="'+TEMA.cor+'" lang="'+L+'"></fechadura-anim>';
    if(ref) ref.parentNode.insertBefore(w, ref.nextSibling); else sp.appendChild(w);
  }
  // a senha em destaque dentro do tópico também copia ao tocar
  [].forEach.call(c.querySelectorAll('.chave'),function(el){
    var v=el.textContent.replace(/\s+/g,'').replace(/✱/g,'*');
    if(SENHA && v===SENHA){ el.setAttribute('role','button'); el.onclick=function(){ copiarTexto(SENHA); aviso(t('copiado')+' · '+SENHA); }; }
  });
}
function copiarTexto(txt){
  if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(txt).catch(function(){}); return; }
  var x=document.createElement('textarea'); x.value=txt; document.body.appendChild(x); x.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(x);
}

function marcarBarra(qual){
  ['bGuia','bConc','bSaida'].forEach(function(id){ document.getElementById(id).classList.toggle('on', id===qual); });
}
/* abrir(id): id de tópico (#energia) ou de tela antiga (#luz, #porta…) —
   os links diretos antigos continuam funcionando. */
function abrir(id){
  if(id==='vistoria'){ abrir('checkin'); setTimeout(function(){ var v=document.getElementById('vistoria'); if(v) v.scrollIntoView({behavior:'smooth',block:'start'}); },120); try{ history.replaceState(null,'','#vistoria'); }catch(e){} return; }
  var tp=topico(id), sec=null;
  if(!tp){ tp=topicoDaTela(id); if(tp && tp.telas[0]!==id) sec=id; }
  if(!tp){ irMenu(); return; }
  document.getElementById('menu').classList.add('hide');
  [].forEach.call(document.querySelectorAll('.tela'),function(e){e.classList.remove('on');});
  var el=document.getElementById('tela-'+tp.id); if(el) el.classList.add('on');
  marcarBarra(tp.id==='checkout'?'bSaida':'');
  window.scrollTo(0,0);
  if(sec) setTimeout(function(){ irSec(sec); },60);
  try{ history.replaceState(null,'','#'+id); }catch(e){}
}
function irSec(tid){ var s=document.getElementById('sec-'+tid); if(s) s.scrollIntoView({behavior:'smooth',block:'start'}); }
function irMenu(){
  [].forEach.call(document.querySelectorAll('.tela'),function(e){e.classList.remove('on');});
  document.getElementById('menu').classList.remove('hide');
  marcarBarra('bGuia'); window.scrollTo(0,0);
  try{ history.replaceState(null,'',location.pathname+location.search); }catch(e){}
}
function irConcierge(){
  irMenu(); marcarBarra('bConc');
  setTimeout(function(){
    document.getElementById('concierge').scrollIntoView({behavior:'smooth',block:'start'});
    try{ document.getElementById('q').focus({preventScroll:true}); }catch(e){}
  },60);
}
function ac(el){ el.parentNode.classList.toggle('on'); }

/* ================= CONCIERGE (busca no guia, sem IA) ================= */
var INDICE=[];
function semTags(s){ return String(s||'').replace(/<svg[\s\S]*?<\/svg>/g,' ').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim(); }
function montarIndice(){
  INDICE=[];
  TELAS.forEach(function(s){
    var d=t('tela_'+s.id)||{};
    var corpo=semTags(s.corpo?s.corpo(d):'');
    INDICE.push({id:s.id,titulo:d.titulo||'',sub:d.sub||'',lead:semTags(d.lead||''),
      texto:((d.titulo||'')+' '+(d.sub||'')+' '+(d.lead||'')+' '+corpo).toLowerCase(),
      sin:(SINONIMOS[L]&&SINONIMOS[L][s.id]||[]).join(' ').toLowerCase()});
  });
}
function normal(s){ return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,''); }
var VAZIAS={pt:['estou','esta','como','onde','qual','quero','para','com','sem','que','nao','tem','uma','um','a','o','e','de','do','da','no','na','meu','minha'],
            en:['i','am','is','the','a','an','how','where','what','my','to','of','in','do','does','wont','not'],
            es:['estoy','esta','como','donde','cual','quiero','para','con','que','no','una','un','el','la','de','del','en','mi']};
function perguntar(txt){ var q=document.getElementById('q'); q.value=txt; buscar(txt); }
function buscar(v){
  var box=document.getElementById('res');
  v=normal(v.trim());
  if(v.length<2){ box.classList.remove('on'); box.innerHTML=''; return; }
  var vaz=VAZIAS[L]||VAZIAS.pt;
  var termos=v.split(/\s+/).filter(function(x){ return x.length>1 && vaz.indexOf(x)<0; });
  if(!termos.length) termos=v.split(/\s+/);
  var r=INDICE.map(function(it){
    var p=0;
    termos.forEach(function(tm){
      if(normal(it.titulo).indexOf(tm)>=0) p+=50;
      if(normal(it.sub).indexOf(tm)>=0) p+=20;
      if(normal(it.sin).indexOf(tm)>=0) p+=40;
      var m=normal(it.texto).split(tm).length-1; p+=Math.min(m,6)*8;
    });
    return {id:it.id,titulo:it.titulo,sub:it.sub,lead:it.lead,p:p};
  }).filter(function(x){return x.p>0;}).sort(function(a,b){return b.p-a.p;}).slice(0,3);
  box.classList.add('on');
  box.innerHTML = r.length
    ? r.map(function(x){
        var res=x.lead.length>170?x.lead.slice(0,167).replace(/\s\S*$/,'')+'…':x.lead;
        return '<div class="resp"><b>'+x.titulo+'</b>'+(res?'<p>'+res+'</p>':'')+
          '<button class="ab" onclick="abrir(\''+x.id+'\')">'+u('abrir')+' →</button></div>'; }).join('')
    : '<div class="vazio"><span>'+u('concVazio')+'</span><a href="#" onclick="zap(TXT[L].zapOi);return false">'+u('concZap')+'</a></div>';
}

/* ================= IDIOMA ================= */
function aplicarIdioma(){
  document.documentElement.lang = L==='pt'?'pt-BR':L;
  [].forEach.call(document.querySelectorAll('[data-t]'),function(e){ var v=t(e.dataset.t); if(typeof v==='string') e.innerHTML=v; });
  [].forEach.call(document.querySelectorAll('[data-u]'),function(e){ var v=u(e.dataset.u); if(typeof v==='string') e.innerHTML=v; });
  document.getElementById('q').placeholder=u('concPh');
  montarHome(); montarTelas(); montarIndice();
  var q=document.getElementById('q'); if(q.value) buscar(q.value);
  [].forEach.call(document.querySelectorAll('.lang button'),function(b){ b.classList.toggle('on', b.dataset.l===L); });
}
[].forEach.call(document.querySelectorAll('.lang button'),function(b){
  b.onclick=function(){ L=b.dataset.l; try{localStorage.setItem('alugo_lang',L);}catch(e){} aplicarIdioma(); };
});
(function init(){
  var mp=document.getElementById('marcaPredio'); if(MARCA_PREDIO) mp.src=MARCA_PREDIO; else mp.style.display='none';
  document.getElementById('marcaAlugo').src = MARCA_ALUGO;
  var fh=FOTOS['hero']||FOTOS[TEMA.hero]||FOTOS[Object.keys(FOTOS)[0]]; document.getElementById('heroBg').style.backgroundImage = 'url('+fh+')';
  document.getElementById('icConc').src = ICS.ajuda;
  document.getElementById('lnkTermo').href = TERMO_URL;
  // tema da unidade: textura de veludo + leve paralaxe ao rolar
  document.getElementById('temaTex').style.backgroundImage = 'url('+TEMA_TEX+')';
  var fundo=document.querySelector('.fundo'), pend=false;
  window.addEventListener('scroll',function(){ if(pend) return; pend=true;
    requestAnimationFrame(function(){ fundo.style.setProperty('--sy', Math.round(window.scrollY*0.06)); pend=false; }); },{passive:true});
  var s=null; try{ s=localStorage.getItem('alugo_lang'); }catch(e){}
  if(!s){ var n=(navigator.language||'pt').slice(0,2); s=(n==='en'||n==='es')?n:'pt'; }
  L=s; aplicarIdioma();
  document.getElementById('q').addEventListener('input',function(){ buscar(this.value); });
  var h=(location.hash||'').replace('#',''); if(h) abrir(h);
})();
