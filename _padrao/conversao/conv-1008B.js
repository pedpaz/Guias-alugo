/* Converte o guia DS-1008B (formato próprio) para o formato de dados v2 (TELAS/TXT/SINONIMOS).
   Roda as próprias funções de tela do guia com "ajudantes" falsos que devolvem marcadores,
   e transforma os marcadores em blocos v2. Uso: node conv-1008B.js <arquivo-js-extraido> */
const fs=require('fs'), vm=require('vm');
const code=fs.readFileSync(process.argv[2],'utf8');
const MK=s=>'\u0001'+JSON.stringify(s)+'\u0002';
const ctx={console};
vm.createContext(ctx);
vm.runInContext(code.replace(/^var /gm,'this.'),ctx);
const out={};
for(const L of ['pt','en','es']){
  const I=ctx.I18N[L]||{}, P=ctx.I18N.pt;
  const t=k=>(I[k]!==undefined?I[k]:(P[k]||''));
  Object.assign(ctx,{L,t,
    _head:id=>MK({k:'head',h:t(id+'_h'),lead:t(id+'_lead')}),
    _ph:k=>MK({k:'foto',f:k}),
    _card:(ic,tit,inner)=>MK({k:'card',h:tit,inner}),
    _row:(ic,h,b)=>MK({k:'row',h,b}),
    _note:(cls,ic,txt)=>MK({k:'note',cls,txt}),
    _steps:a=>MK({k:'steps',a}),
    _chips:a=>MK({k:'chips',a}),
    _check:a=>MK({k:'check',a}),
    _acc:a=>MK({k:'acc',a}),
    _L:(id,n)=>{const a=[];for(let i=1;i<=n;i++)a.push(t(id+'_'+i));return a;},
  });
  const tok=s=>{const r=[];let i=0;while(i<s.length){const a=s.indexOf('\u0001',i);if(a<0){if(s.slice(i).trim())r.push({k:'html',v:s.slice(i)});break;}
      if(s.slice(i,a).trim())r.push({k:'html',v:s.slice(i,a)});
      // marcador pode conter marcadores aninhados (card > row)
      let d=0,j=a;for(;j<s.length;j++){if(s[j]=='\u0001')d++;else if(s[j]=='\u0002'){d--;if(!d)break;}}
      const raw=s.slice(a+1,j); r.push(JSON.parse(raw.replace(/\u0001[\s\S]*?\u0002/g,m=>'"__"'))&&parseNested(raw)); i=j+1;}
    return r;};
  function parseNested(raw){ // JSON com strings que contêm marcadores
    return JSON.parse(raw);
  }
  const telas={};
  for(const tl of ctx.TELAS){
    const html=tl.corpo();
    const itens=tok(html);
    const d={titulo:'',sub:'',lead:'',blocos:[]};
    let fotoPend=null;
    const push=b=>{ if(fotoPend){b.foto=fotoPend;fotoPend=null;} d.blocos.push(b); };
    for(const it of itens){
      if(it.k==='head'){d.titulo=it.h;d.lead=it.lead;}
      else if(it.k==='foto'){ if(fotoPend) d.blocos.push({foto:fotoPend}); fotoPend=it.f; }
      else if(it.k==='card'){
        const sub=tok(it.inner), b={h:it.h,p:[]};
        for(const x of sub){
          if(x.k==='row') b.p.push((x.h?'<b>'+x.h+'</b> — ':'')+x.b);
          else if(x.k==='steps') b.ul=(b.ul||[]).concat(x.a.map((s,i)=>(i+1)+'. '+s));
          else if(x.k==='chips') b.p.push(x.a.join(' · '));
          else if(x.k==='check') b.ul=(b.ul||[]).concat(x.a);
          else if(x.k==='html'){ const txt=x.v.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim(); if(txt) b.p.push(txt); }
        }
        if(b.ul){ b.p=b.p.concat(b.ul); delete b.ul; }
        push(b);
      }
      else if(it.k==='note'){ const b={p:[it.txt]}; if(it.cls==='danger'){b.dest=true;b.pill=({pt:'atenção',en:'heads-up',es:'atención'})[L];} push(b); }
      else if(it.k==='acc'){ d.ac=it.a.map(x=>({q:x[0],r:[x[1]]})); }
      else if(it.k==='check'){ d.blocos.push({p:it.a}); }
      else if(it.k==='html'){
        const v=it.v;
        const big=v.match(/big-k">([^<]*)<\/div><div class="big-v">([^<]*)<\/div><div class="big-s">([^<]*)</);
        if(big){ push({dest:true,h:big[1],chave:big[2],p:[big[3]]}); continue; }
        const yn=v.match(/<div class="si"><h4>([^<]*)<\/h4><ul>([\s\S]*?)<\/ul><\/div><div class="nao"><h4>([^<]*)<\/h4><ul>([\s\S]*?)<\/ul>/);
        if(yn){ const li=s=>[...s.matchAll(/<li>([\s\S]*?)<\/li>/g)].map(m=>m[1]);
          push({h:yn[1],p:li(yn[2])}); push({h:yn[3],p:li(yn[4])}); continue; }
        // botões, fechadura, bloco de check-out: o render v2 refaz
      }
    }
    if(fotoPend) d.blocos.push({foto:fotoPend});
    telas[tl.id]=d;
  }
  out[L]={telas,I};
}
fs.writeFileSync(process.argv[3],JSON.stringify(out,null,1));
console.log('ok', Object.keys(out.pt.telas).join(' '));
