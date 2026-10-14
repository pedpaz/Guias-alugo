var TELAS = [
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
];