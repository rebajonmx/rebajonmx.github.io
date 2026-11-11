(()=>{const V=__VIDEO__;
// Rebajón MX · motor de videos 1080x1920 a partir de un "concepto" (lista de escenas).
// No hace falta tocar este archivo para crear videos nuevos: se crean en contenido/conceptos/*.json
// (formato en docs/CONCEPTOS.md). Python resuelve textos y productos y los pasa ya listos en __VIDEO__.
// Zona segura: todo lo importante va entre y=440 y y=1480 (lo que ve el feed de Instagram y lo que no tapa TikTok).
const W=1080,H=1920,FPS=30,TM=V.tema,SEED=V.seed;
const C={bg:TM.fondo,tx:TM.texto,tm:TM.suave,ac:TM.acento,a2:TM.acento2,sa:TM.sobre_acento,dc:TM.decoracion,in:'#141a33',ok:'#12a150',wh:'#ffffff'};
const cl=t=>Math.min(Math.max(t,0),1),E=t=>1-Math.pow(1-cl(t),3),B=t=>{t=cl(t);return 1+2.70158*Math.pow(t-1,3)+1.70158*Math.pow(t-1,2)};
const money=n=>'$'+Number(n).toLocaleString('es-MX',{minimumFractionDigits:n%1?2:0,maximumFractionDigits:2});
const img=u=>new Promise(r=>{if(!u)return r(null);const i=new Image();i.crossOrigin='anonymous';i.onload=()=>r(i);i.onerror=()=>r(null);i.src=u.startsWith('data:')?u:'https://wsrv.nl/?w=700&output=png&url='+encodeURIComponent(u.replace(/^https?:\/\//,''))});
const prods=V.escenas.flatMap(s=>s.productos||(s.producto?[s.producto]:[]));
let pre=null;const fotos=async()=>{if(pre)return pre;pre={};for(const p of prods)if(!(p.img in pre))pre[p.img]=await img(p.img);return pre};
async function build(){const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');await fotos();
const F=(s,w=900)=>`${w} ${s}px "Segoe UI Black","Segoe UI","Noto Sans",Arial,"Segoe UI Emoji","Noto Color Emoji",sans-serif`;
const fit=(s,size,max,w=900)=>{x.font=F(size,w);while(x.measureText(s).width>max&&size>24){size-=2;x.font=F(size,w)}return size};
const T=(s,X,Y,size,col,o={})=>{const {w=900,sc=1,al=1,max=940}=o;size=fit(s,size,max,w);x.save();x.globalAlpha=cl(al);x.translate(X,Y);x.scale(sc,sc);x.font=F(size,w);x.textAlign='center';x.textBaseline='middle';x.fillStyle=col;x.fillText(s,0,0);x.restore()};
// Parte un texto en renglones que quepan en "max" pixeles
const lines=(s,size,max,w=800)=>{x.font=F(size,w);const out=[];let cur='';for(const word of String(s).split(' ')){const t=cur?cur+' '+word:word;if(x.measureText(t).width>max&&cur){out.push(cur);cur=word}else cur=t}if(cur)out.push(cur);return out};
const P=(s,X,Y,size,col,o={})=>{const {w=800,al=1,max=900,lh=1.25}=o;const ls=lines(s,size,max,w);ls.forEach((l,i)=>T(l,X,Y+(i-(ls.length-1)/2)*size*lh,size,col,{w,al:al-i*.15,max}));return ls.length};
const pill=(s,X,Y,size,bg,fg,o={})=>{const {sc=1,rot=0,al=1}=o;size=fit(s,size,860);x.save();x.globalAlpha=cl(al);x.translate(X,Y);x.rotate(rot);x.scale(sc,sc);x.font=F(size);const w=x.measureText(s).width+size*1.3,h=size*1.85;x.shadowColor='rgba(20,26,51,.2)';x.shadowBlur=24;x.shadowOffsetY=8;x.beginPath();x.roundRect(-w/2,-h/2,w,h,h/2);x.fillStyle=bg;x.fill();x.shadowColor='transparent';x.fillStyle=fg;x.textAlign='center';x.textBaseline='middle';x.fillText(s,0,size*.06);x.restore()};
// Fondo del tema: color sólido, círculo punteado que gira, círculo translúcido y franjas arriba/abajo
const bg=t=>{x.fillStyle=C.bg;x.fillRect(0,0,W,H);
 x.save();x.globalAlpha=.55;x.fillStyle=C.dc;x.beginPath();x.arc(-120+Math.sin(t*.6)*30,H-260,620,0,7);x.fill();x.restore();
 x.save();x.translate(W-60,560);x.rotate(t*.25);x.strokeStyle=C.dc;x.lineWidth=7;x.setLineDash([26,22]);x.beginPath();x.arc(0,0,430,0,7);x.stroke();x.restore();
 x.fillStyle=C.ac;x.fillRect(0,0,W,16);x.fillRect(0,H-16,W,16)};
const PT=[...Array(70)].map((_,i)=>({x:(i*137)%W,y:-((i*311)%H),v:300+(i*53)%420,r:i,s:12+(i*7)%16,c:[C.ac,C.a2,C.wh,C.ac][i%4]}));
const conf=t=>PT.forEach(p=>{const y=(p.y+p.v*t)%(H+200)-100;x.save();x.translate(p.x+Math.sin(t*2+p.r)*30,y<-100?y+H+200:y);x.rotate(t*3+p.r);x.fillStyle=p.c;x.fillRect(-p.s/2,-p.s/4,p.s,p.s/2);x.restore()});
const logo=()=>{pill(V.logo[0],W/2-45,370,44,C.ac,C.sa,{rot:-.04});if(V.logo[1])pill(V.logo[1],W/2+148,388,30,C.a2,C.wh,{rot:.07})};
const shake=(t,k=14)=>t>0&&t<.3?[(Math.sin(t*90)*k*(1-t/.3)),(Math.cos(t*70)*k*(1-t/.3))]:[0,0];
const foto=(d,X,Y,cw,sc=1,al=1)=>{x.save();x.globalAlpha=cl(al);x.translate(X,Y);x.scale(sc,sc);x.shadowColor='rgba(20,26,51,.2)';x.shadowBlur=50;x.shadowOffsetY=18;x.beginPath();x.roundRect(-cw/2,-cw/2,cw,cw,44);x.fillStyle='#fff';x.fill();x.shadowColor='transparent';
 const im=pre[d.img];if(im){const r=Math.min((cw-56)/im.width,(cw-56)/im.height);x.drawImage(im,-im.width*r/2,-im.height*r/2,im.width*r,im.height*r)}else{x.font=F(cw*.42);x.textAlign='center';x.textBaseline='middle';x.fillText(d.e||'🛒',0,0)}x.restore()};
const precio=(d,t,t0,yN,yP,yA)=>{T(d.n,W/2,yN,60,C.tx,{al:(t-t0)/.15,max:900});
 const cnt=d.was-(d.was-d.now)*E((t-t0-.1)/.55);T(money(t>t0+.7?d.now:Math.round(cnt)),W/2,yP,112,C.ac,{al:(t-t0-.05)/.1,sc:B((t-t0-.05)/.3)});
 x.save();x.font=F(50,700);const ws='antes '+money(d.was),ww=x.measureText(ws).width;T(ws,W/2,yA,50,C.tm,{w:700,al:(t-t0-.2)/.15});x.globalAlpha=cl((t-t0-.2)/.15);x.fillStyle=C.a2;x.fillRect(W/2-ww/2,yA-3,ww,5);x.restore();
 pill('🛒 en '+V.tienda,W/2,yA+95,36,'#fff',C.in,{al:(t-t0-.35)/.2})};
// ---------- Tipos de escena (ver docs/CONCEPTOS.md) ----------
const ESC={
 gancho:(s,t)=>{bg(t);logo();const [a,b]=shake(t,18);x.save();x.translate(a,b);if(s.emoji)T(s.emoji,W/2,560,150,C.tx,{sc:B(t/.35)});T(s.titulo,W/2,s.emoji?760:700,150,C.ac,{sc:B(t/.35),max:960});x.restore();
  if(s.texto)P(s.texto,W/2,960,74,C.tx,{w:900,al:(t-.5)/.2,max:900});if(s.etiqueta)pill(s.etiqueta,W/2,1180,66,C.a2,C.wh,{al:(t-1)/.15,sc:B((t-1)/.35),rot:-.04})},
 texto:(s,t)=>{bg(t);logo();if(s.titulo)P(s.titulo,W/2,600,84,C.ac,{w:900,al:t/.15,max:920});if(s.texto)P(s.texto,W/2,900,62,C.tx,{w:700,al:(t-.35)/.2,max:900});
  if(s.etiqueta)pill(s.etiqueta,W/2,1200,52,C.a2,C.wh,{al:(t-.9)/.15,sc:B((t-.9)/.35)})},
 numero:(s,t)=>{bg(t);logo();if(s.titulo)P(s.titulo,W/2,560,62,C.tx,{al:t/.15});T(s.numero,W/2,800,260,C.ac,{sc:B((t-.2)/.4),al:(t-.2)/.1,max:980});
  if(s.texto)P(s.texto,W/2,1080,60,C.tx,{w:700,al:(t-.6)/.2})},
 lista:(s,t)=>{bg(t);logo();P(s.titulo,W/2,560,76,C.ac,{w:900,al:t/.15});const n=s.items.length,gap=Math.min(150,700/n);
  s.items.forEach((it,i)=>{const tt=t-.5-i*.45,Y=760+i*gap;x.save();x.globalAlpha=cl(tt/.15);x.translate(-60*(1-E(tt/.3)),0);x.beginPath();x.arc(150,Y,42,0,7);x.fillStyle=C.ac;x.fill();x.restore();
   T(s.marca||'✓',150,Y+2,52,C.sa,{al:tt/.15});x.save();x.globalAlpha=cl(tt/.15);const sz=fit(it,52,780,800);x.font=F(sz,800);x.fillStyle=C.tx;x.textBaseline='middle';x.fillText(it,220,Y+2);x.restore()})},
 comparacion:(s,t)=>{bg(t);logo();P(s.titulo,W/2,560,70,C.tx,{al:t/.15});
  [[s.izq,280,C.a2],[s.der,800,C.ac]].forEach(([c,X,col],i)=>{const tt=t-.4-i*.6;x.save();x.globalAlpha=cl(tt/.2);x.beginPath();x.roundRect(X-230,700,460,420,40);x.fillStyle=col;x.fill();x.restore();
   T(c.titulo,X,770,46,i?C.sa:C.wh,{al:tt/.2,max:420});T(c.valor,X,900,96,i?C.sa:C.wh,{al:tt/.2,sc:B(tt/.4),max:420});P(c.texto||'',X,1040,36,i?C.sa:C.wh,{w:700,al:tt/.2,max:400})});
  if(s.texto)P(s.texto,W/2,1270,58,C.tx,{al:(t-1.6)/.2})},
 producto:(s,t)=>{const d=s.producto;bg(t);logo();foto(d,W/2,720,430,.6+.4*E(t/.35),t/.2);
  if(s.etiqueta)pill(s.etiqueta,W/2-250,535,52,C.ac,C.sa,{rot:-.08,sc:B(t/.3)});const [a,b]=shake(t-.3,18);x.save();x.translate(a,b);pill('-'+d.off+'%',W/2+245,550,78,C.a2,C.wh,{rot:.1,sc:t<.3?0:2-1*E((t-.3)/.2)});x.restore();
  precio(d,t,.35,1015,1125,1225)},
 cierre:(s,t)=>{bg(t);conf(t);logo();
  T(s.titulo||'Solo ofertas',W/2,560,104,C.tx,{sc:B(t/.4),al:t/.15});T(s.titulo2||'REALES ✅',W/2,685,124,C.ac,{sc:B((t-.15)/.4),al:(t-.15)/.15});
  T('con link directo a la tienda',W/2,795,48,C.tm,{w:700,al:(t-.4)/.3});
  pill('🌐 '+V.web,W/2,910,54,C.ac,C.sa,{sc:B((t-.6)/.4)*(1+Math.sin(t*8)*.03),al:(t-.6)/.15});
  pill(V.telegram?'🔔 Alertas gratis: WhatsApp y Telegram':'🔔 Alertas gratis en WhatsApp',W/2,1050,46,C.ok,C.wh,{sc:B((t-.9)/.4),al:(t-.9)/.15});
  T('📌 Links en el perfil y en los comentarios',W/2,1185,44,C.tx,{al:(t-1.2)/.3});
  T('Síguenos para más rebajas 🔥',W/2,1290,42,C.tm,{w:700,al:(t-1.5)/.3})}};
const DUR={gancho:2.6,texto:3.2,numero:2.8,lista:3.8,comparacion:3.8,producto:2.4,cierre:3.4};
const S=V.escenas.map(s=>({s,d:s.seg||DUR[s.tipo]||3}));
const dur=S.reduce((a,e)=>a+e.d,0);
const draw=t=>{let a=0;for(const e of S){if(t<a+e.d||e===S[S.length-1]){(ESC[e.s.tipo]||ESC.texto)(e.s,Math.min(t-a,e.d));break}a+=e.d}};
return {c,x,dur,draw}}
// Música propia sin derechos: cambia con cada video y cada día (tempo, tono, bajo y melodía).
function beat(ac,out,dur){let s=(SEED%2147483646)+1;const R=()=>(s=s*16807%2147483647)/2147483647;
 const estilos=[{bpm:128,esc:[0,3,5,7,10],onda:'sawtooth',arp:'square'},{bpm:116,esc:[0,2,4,7,9],onda:'square',arp:'triangle'},{bpm:100,esc:[0,3,5,7,10],onda:'triangle',arp:'sine'},{bpm:122,esc:[0,2,4,7,9],onda:'sawtooth',arp:'triangle'},{bpm:108,esc:[0,2,3,7,8],onda:'square',arp:'sine'}];
 const st=estilos[SEED%estilos.length],raiz=[55,58.27,61.74,65.41,69.3,73.42][Math.floor(R()*6)],bpm=st.bpm+Math.floor(R()*6)-3,sp=60/bpm,t0=ac.currentTime+.05;
 const g=ac.createGain();g.gain.value=.5;g.connect(out);const nb=ac.createBuffer(1,ac.sampleRate*.2,ac.sampleRate),nd=nb.getChannelData(0);for(let i=0;i<nd.length;i++)nd[i]=R()*2-1;
 const f=n=>raiz*Math.pow(2,n/12),prog=[0,st.esc[3]-12,st.esc[2],st.esc[1]],patB=[...Array(8)].map(()=>R()<.7),patA=[...Array(8)].map(()=>st.esc[Math.floor(R()*5)]+12*(1+Math.floor(R()*2)));
 const nota=(tipo,fr,t,len,vol,lp)=>{const o=ac.createOscillator(),gg=ac.createGain(),fl=ac.createBiquadFilter();o.type=tipo;o.frequency.value=fr;fl.type='lowpass';fl.frequency.value=lp;gg.gain.setValueAtTime(.0001,t);gg.gain.exponentialRampToValueAtTime(vol,t+.015);gg.gain.exponentialRampToValueAtTime(.0005,t+len);o.connect(fl).connect(gg).connect(g);o.start(t);o.stop(t+len+.05)};
 const hats=st.bpm>110?2:1;
 for(let i=0;i*sp<dur;i++){const t=t0+i*sp,raizC=prog[Math.floor(i/4)%4];
  const o=ac.createOscillator(),k=ac.createGain();o.frequency.setValueAtTime(150,t);o.frequency.exponentialRampToValueAtTime(42,t+.22);k.gain.setValueAtTime(st.bpm<105?.8:1,t);k.gain.exponentialRampToValueAtTime(.001,t+.32);o.connect(k).connect(g);o.start(t);o.stop(t+.35);
  if(i%2){const n=ac.createBufferSource(),ng=ac.createGain(),bf=ac.createBiquadFilter();n.buffer=nb;bf.type='bandpass';bf.frequency.value=1800;ng.gain.setValueAtTime(.45,t);ng.gain.exponentialRampToValueAtTime(.001,t+.16);n.connect(bf).connect(ng).connect(g);n.start(t);n.stop(t+.2)}
  for(let h=0;h<hats;h++){const th=t+sp*(h+.5)/hats,n=ac.createBufferSource(),hf=ac.createBiquadFilter(),hg=ac.createGain();n.buffer=nb;hf.type='highpass';hf.frequency.value=7500;hg.gain.setValueAtTime(.25,th);hg.gain.exponentialRampToValueAtTime(.001,th+.05);n.connect(hf).connect(hg).connect(g);n.start(th);n.stop(th+.07)}
  for(let e=0;e<2;e++){const te=t+e*sp/2,paso=(i*2+e)%8;if(patB[paso])nota(st.onda,f(raizC-12),te,sp*.45,.2,600);if(i>=8&&(paso%2===0||R()<.3))nota(st.arp,f(raizC+patA[paso]),te,sp*.4,.07,3200)}}}
let cache=null;const get=async()=>cache||(cache=await build());
async function audio(dur){const sr=48000,ac=new OfflineAudioContext(2,Math.ceil(sr*(dur+.2)),sr);beat(ac,ac.destination,dur);return ac.startRendering()}
// Interfaz para Python (scripts/generar_video.py): cuadros en JPG + audio en WAV; ffmpeg arma el MP4.
window.RVfotos=async()=>{const p=await fotos();const v=Object.values(p);return {cargadas:v.filter(Boolean).length,total:v.length}};
window.RVinfo=async()=>{const v=await get();return {dur:v.dur,frames:Math.round(v.dur*FPS),fps:FPS}};
window.RVframe=async i=>{const v=await get();v.draw(i/FPS);return v.c.toDataURL('image/jpeg',.92).split(',')[1]};
window.RVwav=async()=>{const v=await get(),ab=await audio(v.dur),n=Math.round(v.dur*48000),b=new DataView(new ArrayBuffer(44+n*4)),w=(o,s)=>[...s].forEach((ch,i)=>b.setUint8(o+i,ch.charCodeAt(0)));
 w(0,'RIFF');b.setUint32(4,36+n*4,true);w(8,'WAVEfmt ');b.setUint32(16,16,true);b.setUint16(20,1,true);b.setUint16(22,2,true);b.setUint32(24,48000,true);b.setUint32(28,192000,true);b.setUint16(32,4,true);b.setUint16(34,16,true);w(36,'data');b.setUint32(40,n*4,true);
 const L=ab.getChannelData(0),R=ab.getChannelData(1);for(let i=0;i<n;i++){b.setInt16(44+i*4,Math.max(-1,Math.min(1,L[i]))*32767,true);b.setInt16(46+i*4,Math.max(-1,Math.min(1,R[i]))*32767,true)}
 const u=new Uint8Array(b.buffer);let s='';for(let i=0;i<u.length;i+=0x8000)s+=String.fromCharCode(...u.subarray(i,i+0x8000));return btoa(s)};
})();
