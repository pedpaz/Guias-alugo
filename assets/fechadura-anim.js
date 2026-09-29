/* ============================================================================
   aluGO · <fechadura-anim> — Intelbras FR 101 e o "modo de senha aleatória"
   ----------------------------------------------------------------------------
   Fechaduras do Sidney Metropolitan e do DNA SmartStyle (Intelbras FR 101).
   Com o modo de senha aleatória ligado, o hóspede digita a senha + ✱, a porta
   NÃO abre e o teclado acende só alguns números sorteados. É preciso tocar
   nesses números e confirmar de novo com ✱ — aí destrava.
   Fonte: FAQ Intelbras FR 101 ("o teclado acende uma linha aleatória…
   pressione os 3 dígitos exibidos e depois pressione *"; desativar: manual §7.3).

   Uso (qualquer guia):
     <script src="assets/fechadura-anim.js" defer></script>
     <fechadura-anim senha="1213*" cor="#E0761A"></fechadura-anim>

   Idioma: atributo lang, senão <html lang>, senão localStorage 'alugo_lang'.
   Um único arquivo para todos os guias: corrigiu aqui, corrigiu em todos.
   ========================================================================== */
(function(){
  if (!window.customElements || customElements.get('fechadura-anim')) return;

  var TXT = {
    pt: {
      tit: 'Digitou a senha e acenderam outros números?',
      sub: 'Não é erro — é a proteção da fechadura. Veja o que fazer:',
      p: ['Toque na tela para acender o teclado',
          'Digite a senha <b>{senha}</b> e confirme com <b>{ok}</b>',
          'A porta não abriu e acenderam só 2 ou 3 números? Toque neles',
          'Confirme de novo com <b>{ok}</b> — ouviu o bip, é só abrir'],
      nota: 'Se os números sorteados aparecerem logo que você toca a tela, é o mesmo caso: toque neles, depois digite a senha e confirme.',
      por: 'Por que isso acontece? Os números sorteados mudam a cada vez e espalham as marcas de dedo na tela — assim ninguém descobre a senha pelas teclas mais tocadas.',
      erro: 'Errou 5 vezes seguidas? A fechadura apita e bloqueia por 1 minuto. Espere e tente de novo, com calma.',
      tecla: 'A tecla de confirmar fica no canto de baixo, à esquerda do 0.',
      rep: '↻ ver de novo', ok: 'destravou', nao: 'não abriu…'
    },
    en: {
      tit: 'Entered the code and other numbers lit up?',
      sub: 'It isn\'t an error — it\'s the lock\'s protection. Here\'s what to do:',
      p: ['Touch the screen to light up the keypad',
          'Enter the code <b>{senha}</b> and confirm with <b>{ok}</b>',
          'The door didn\'t open and only 2 or 3 numbers lit up? Tap them',
          'Confirm again with <b>{ok}</b> — once it beeps, just open'],
      nota: 'If the random numbers show up as soon as you touch the screen, it\'s the same thing: tap them, then enter the code and confirm.',
      por: 'Why? The random numbers change every time and spread fingerprints across the screen, so nobody can guess the code from the most-touched keys.',
      erro: 'Wrong 5 times in a row? The lock beeps and blocks for 1 minute. Wait and try again calmly.',
      tecla: 'The confirm key is at the bottom, to the left of the 0.',
      rep: '↻ watch again', ok: 'unlocked', nao: 'didn\'t open…'
    },
    es: {
      tit: '¿Marcaste la clave y se encendieron otros números?',
      sub: 'No es un error — es la protección de la cerradura. Qué hacer:',
      p: ['Toca la pantalla para encender el teclado',
          'Marca la clave <b>{senha}</b> y confirma con <b>{ok}</b>',
          '¿La puerta no abrió y se encendieron solo 2 o 3 números? Tócalos',
          'Confirma de nuevo con <b>{ok}</b> — cuando suene el bip, abre'],
      nota: 'Si los números sorteados aparecen apenas tocas la pantalla, es lo mismo: tócalos, después marca la clave y confirma.',
      por: '¿Por qué? Los números sorteados cambian cada vez y reparten las marcas de dedo en la pantalla, así nadie descubre la clave por las teclas más tocadas.',
      erro: '¿Te equivocaste 5 veces seguidas? La cerradura pita y se bloquea 1 minuto. Espera y vuelve a intentar con calma.',
      tecla: 'La tecla de confirmar está abajo, a la izquierda del 0.',
      rep: '↻ ver de nuevo', ok: 'abierta', nao: 'no abrió…'
    }
  };

  // teclado da FR 101: 1–9, [confirmar] 0 [engrenagem]
  var TECLAS = ['1','2','3','4','5','6','7','8','9','ok','0','cfg'];
  var ENGRENAGEM = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>';
  var CADEADO = '<svg viewBox="0 0 24 24" width="15" height="15" fill="#2ED573"><rect x="5" y="10.5" width="14" height="10.5" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0" fill="none" stroke="#2ED573" stroke-width="2.4"/></svg>';

  function idioma(el){
    var l = (el.getAttribute('lang') || document.documentElement.lang || '').slice(0,2).toLowerCase();
    if (!TXT[l]) { try { l = (localStorage.getItem('alugo_lang') || 'pt').slice(0,2); } catch(e) { l = 'pt'; } }
    return TXT[l] ? l : 'pt';
  }

  var CSS = function(cor){ return '\
:host{display:block;margin:0 0 14px;font-family:Manrope,system-ui,-apple-system,sans-serif;color:#221E1B}\
*{box-sizing:border-box}\
.box{background:#FFFDFA;border:1px solid #E9E0D5;border-radius:20px;padding:18px 16px 16px;\
  box-shadow:0 2px 6px rgba(34,30,27,.05),0 10px 26px rgba(34,30,27,.06)}\
.tit{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:18px;line-height:1.2;margin:0 0 4px}\
.sub{font-size:13.5px;color:#6B615A;margin:0 0 16px}\
.palco{display:flex;gap:18px;align-items:center;justify-content:center;flex-wrap:wrap}\
.corpo{position:relative;width:138px;height:292px;border-radius:30px;flex:none;padding:7px;\
  background:linear-gradient(90deg,#9a9a9a,#f2f2f2 18%,#8c8c8c 40%,#e6e6e6 62%,#7d7d7d 86%,#cfcfcf);\
  box-shadow:0 12px 26px rgba(0,0,0,.28)}\
.painel{position:relative;height:100%;border-radius:24px;background:linear-gradient(170deg,#1c1c1d,#0b0b0c 60%,#151516);\
  padding:34px 14px 18px;overflow:hidden}\
.painel::after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.07) 0%,rgba(255,255,255,0) 38%);pointer-events:none}\
.cad{position:absolute;top:15px;left:16px;opacity:.95}\
.tela{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-rows:44px;gap:4px 6px;margin-top:4px}\
.k{display:flex;align-items:center;justify-content:center;font-weight:500;font-size:19px;\
  color:rgba(255,255,255,.06);transition:color .25s,text-shadow .25s,background .2s,transform .12s;border-radius:50%}\
.k.on{color:#fff;text-shadow:0 0 6px rgba(255,255,255,.75)}\
.k.hit{background:rgba(255,255,255,.2);transform:scale(.86)}\
.base{position:absolute;left:18px;right:18px;bottom:10px;height:3px;border-radius:3px;background:rgba(255,255,255,.08)}\
.dedo{position:absolute;width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.26);\
  border:2px solid rgba(255,255,255,.9);box-shadow:0 2px 8px rgba(0,0,0,.4);pointer-events:none;\
  transition:left .36s cubic-bezier(.3,.7,.3,1),top .36s cubic-bezier(.3,.7,.3,1),opacity .3s;opacity:0;z-index:3}\
.dedo.tap{animation:tap .3s ease}\
@keyframes tap{50%{transform:scale(.7)}}\
.balao{position:absolute;left:50%;top:-12px;transform:translateX(-50%);font-size:11px;font-weight:800;\
  letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:5px 12px;white-space:nowrap;\
  opacity:0;transition:opacity .3s;z-index:4}\
.balao.nao{background:#C4441B;color:#fff}\
.balao.sim{background:#1FAA53;color:#fff}\
.balao.on{opacity:1}\
.lista{flex:1;min-width:190px;margin:0;padding:0;list-style:none;counter-reset:n}\
.lista li{position:relative;padding:7px 0 7px 32px;font-size:14px;line-height:1.42;color:#9A9089;transition:color .25s}\
.lista li::before{counter-increment:n;content:counter(n);position:absolute;left:0;top:6px;width:22px;height:22px;\
  border-radius:50%;border:1.5px solid #E9E0D5;display:flex;align-items:center;justify-content:center;\
  font-size:11px;font-weight:800;color:#9A9089;transition:.25s}\
.lista li.at{color:#221E1B;font-weight:700}\
.lista li.at::before{background:'+cor+';border-color:'+cor+';color:#fff}\
.lista li.feito::before{border-color:'+cor+';color:'+cor+'}\
.lista b{color:'+cor+'}\
.miud{font-size:13px;color:#6B615A;margin:10px 0 0;line-height:1.55}\
.por{border-top:1px solid #E9E0D5;padding-top:12px;margin-top:16px}\
.rep{margin-top:12px;background:none;border:1.5px solid #221E1B;border-radius:12px;padding:9px 14px;\
  font:800 12.5px Manrope,system-ui,sans-serif;letter-spacing:.04em;color:#221E1B;cursor:pointer}\
@media (prefers-reduced-motion:reduce){.dedo{display:none}.lista li{color:#221E1B}}\
'; };

  function Fechadura(){ return Reflect.construct(HTMLElement, [], Fechadura); }
  Fechadura.prototype = Object.create(HTMLElement.prototype);
  Fechadura.prototype.constructor = Fechadura;
  Object.setPrototypeOf(Fechadura, HTMLElement);

  Fechadura.prototype.connectedCallback = function(){
    if (this._pronto) return; this._pronto = true;
    var senha = (this.getAttribute('senha') || '1234*').trim();
    var digitos = senha.replace(/[*#✱✓]+$/, '').split('');
    var okSimb = /#$/.test(senha) ? '#' : '✱';
    var cor = this.getAttribute('cor') || '#E0761A';
    var T = TXT[idioma(this)];
    var passos = T.p.map(function(x){ return x.replace('{senha}', digitos.join('')).split('{ok}').join(okSimb); });

    var root = this.attachShadow ? this.attachShadow({mode:'open'}) : this;
    root.innerHTML = '<style>' + CSS(cor) + '</style>' +
      '<div class="box" role="group" aria-label="' + T.tit + '">' +
      '<p class="tit">' + T.tit + '</p><p class="sub">' + T.sub + '</p>' +
      '<div class="palco"><div class="corpo" aria-hidden="true"><div class="painel"><span class="cad">' + CADEADO + '</span><div class="tela">' +
        TECLAS.map(function(k){
          var rot = k === 'ok' ? okSimb : (k === 'cfg' ? ENGRENAGEM : k);
          return '<span class="k" data-k="' + k + '">' + rot + '</span>';
        }).join('') +
      '</div><span class="base"></span><div class="dedo"></div></div>' +
      '<div class="balao nao">' + T.nao + '</div><div class="balao sim">✓ ' + T.ok + '</div></div>' +
      '<ol class="lista">' + passos.map(function(x){ return '<li>' + x + '</li>'; }).join('') + '</ol></div>' +
      '<p class="miud">' + T.nota + '</p>' +
      '<p class="miud">' + T.tecla + '</p>' +
      '<p class="miud por">' + T.por + '</p><p class="miud">' + T.erro + '</p>' +
      '<button class="rep" type="button">' + T.rep + '</button></div>';

    var $ = function(s){ return root.querySelector(s); }, $$ = function(s){ return [].slice.call(root.querySelectorAll(s)); };
    var painel = $('.painel'), dedo = $('.dedo'), nao = $('.balao.nao'), sim = $('.balao.sim'), itens = $$('.lista li');
    var timers = [];
    function limpa(){ timers.forEach(clearTimeout); timers = []; }
    function em(ms, fn){ timers.push(setTimeout(fn, ms)); }
    function tecla(k){ return root.querySelector('.k[data-k="' + k + '"]'); }
    function todas(on){ $$('.k').forEach(function(k){ k.classList.toggle('on', on); }); }
    function passo(i){ itens.forEach(function(li, j){ li.classList.toggle('at', j === i); li.classList.toggle('feito', j < i); }); }
    function aponta(k){
      var el = tecla(k); if (!el) return;
      var r = el.getBoundingClientRect(), f = painel.getBoundingClientRect();
      dedo.style.left = (r.left - f.left + r.width/2 - 16) + 'px';
      dedo.style.top = (r.top - f.top + r.height/2 - 16) + 'px';
    }
    function toca(k){
      var el = tecla(k); if (!el) return;
      dedo.classList.remove('tap'); void dedo.offsetWidth; dedo.classList.add('tap');
      el.classList.add('hit'); setTimeout(function(){ el.classList.remove('hit'); }, 260);
    }
    function digita(seq, t0, passoMs){
      seq.forEach(function(k, i){
        em(t0 + i*passoMs, function(){ aponta(k); });
        em(t0 + i*passoMs + 280, function(){ toca(k); });
      });
      return t0 + seq.length*passoMs;
    }
    function sorteia(){
      var pool = ['1','2','3','4','5','6','7','8','9','0'], n = Math.random() < .5 ? 2 : 3, out = [];
      while (out.length < n) out.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
      return out;
    }
    function roda(){
      limpa(); todas(false); nao.classList.remove('on'); sim.classList.remove('on');
      dedo.style.opacity = 0; passo(-1);
      var t = 400;
      // 1. toca a tela: o teclado acende
      em(t, function(){ passo(0); aponta('5'); dedo.style.opacity = 1; });
      em(t + 450, function(){ toca('5'); todas(true); });
      t += 1300;
      // 2. senha + confirmar
      em(t, function(){ passo(1); });
      t = digita(digitos.concat(['ok']), t + 200, 520);
      // 3. não abriu: só os sorteados acendem
      var sorte = sorteia();
      em(t + 150, function(){ dedo.style.opacity = 0; todas(false); nao.classList.add('on'); });
      em(t + 1100, function(){ passo(2); sorte.forEach(function(k){ tecla(k).classList.add('on'); }); });
      t += 2400;
      em(t, function(){ nao.classList.remove('on'); aponta(sorte[0]); dedo.style.opacity = 1; });
      sorte.forEach(function(k, i){
        em(t + 350 + i*650, function(){ aponta(k); });
        em(t + 650 + i*650, function(){ toca(k); tecla(k).classList.remove('on'); });
      });
      t += 500 + sorte.length*650;
      // 4. confirma de novo: destrava
      em(t, function(){ passo(3); tecla('ok').classList.add('on'); aponta('ok'); });
      em(t + 400, function(){ toca('ok'); });
      t += 900;
      em(t, function(){ dedo.style.opacity = 0; todas(false); sim.classList.add('on'); passo(4); });
      em(t + 3400, roda);
    }
    $('.rep').addEventListener('click', roda);
    this._limpa = limpa;

    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) {
      itens.forEach(function(li){ li.classList.add('at'); }); todas(true); return;
    }
    if ('IntersectionObserver' in window) {
      var visto = false, self = this;
      var io = new IntersectionObserver(function(es){
        es.forEach(function(e){
          if (e.isIntersecting && !visto) { visto = true; roda(); }
          else if (!e.isIntersecting && visto) { visto = false; limpa(); }
        });
      }, {threshold: .35});
      io.observe(this); this._io = io;
    } else { roda(); }
  };
  Fechadura.prototype.disconnectedCallback = function(){ if (this._limpa) this._limpa(); if (this._io) this._io.disconnect(); };

  customElements.define('fechadura-anim', Fechadura);
})();
