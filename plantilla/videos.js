(()=>{const D=__D__,K=__K__,SEED=__SEED__;
// Rebajón MX · generador de videos 1080x1920, estilo azul Rebajón (como la portada de Facebook).
// Todo lo importante va entre y=440 y y=1480: es lo que Instagram deja ver en el feed (recorte 4:5/1:1)
// y lo que no tapan los botones de TikTok.
const W=1080,H=1920,C={co:'#2340d9',ro:'#e4006f',so:'#ffcf2e',in:'#141a33',mu:'#5b6385',ok:'#12a150',bg:'#2340d9',tx:'#ffffff',tm:'rgba(255,255,255,.86)'};
const TINTES=['#2340d9','#2a44e0','#1f39c8','#2747e4'];
const cl=t=>Math.min(Math.max(t,0),1),E=t=>1-Math.pow(1-cl(t),3),B=t=>{t=cl(t);return 1+2.70158*Math.pow(t-1,3)+1.70158*Math.pow(t-1,2)};
const money=n=>'$'+n.toLocaleString('es-MX',{minimumFractionDigits:n%1?2:0,maximumFractionDigits:2});
const img=u=>new Promise(r=>{const i=new Image();i.crossOrigin='anonymous';i.onload=()=>r(i);i.onerror=()=>r(null);i.src=u.startsWith('data:')?u:'https://wsrv.nl/?w=700&output=png&url='+encodeURIComponent(u.replace(/^https?:\/\//,''))});
let pre=null;const fotos=async()=>{if(pre)return pre;pre={};for(const d of D)pre[d.img]=await img(d.img);return pre};
async function build(id){const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');await fotos();
const F=(s,w=900)=>`${w} ${s}px "Segoe UI Black","Segoe UI","Noto Sans",Arial,"Segoe UI Emoji","Noto Color Emoji",sans-serif`;
const fit=(s,size,max,w=900)=>{x.font=F(size,w);while(x.measureText(s).width>max&&size>24){size-=2;x.font=F(size,w)}return size};
const T=(s,X,Y,size,col,o={})=>{const {w=900,sc=1,al=1,max=940}=o;size=fit(s,size,max,w);x.save();x.globalAlpha=cl(al);x.translate(X,Y);x.scale(sc,sc);x.font=F(size,w);x.textAlign='center';x.textBaseline='middle';x.fillStyle=col;x.fillText(s,0,0);x.restore()};
const pill=(s,X,Y,size,bg,fg,o={})=>{const {sc=1,rot=0,al=1}=o;size=fit(s,size,860);x.save();x.globalAlpha=cl(al);x.translate(X,Y);x.rotate(rot);x.scale(sc,sc);x.font=F(size);const w=x.measureText(s).width+size*1.3,h=size*1.85;x.shadowColor='rgba(20,26,51,.18)';x.shadowBlur=24;x.shadowOffsetY=8;x.beginPath();x.roundRect(-w/2,-h/2,w,h,h/2);x.fillStyle=bg;x.fill();x.shadowColor='transparent';x.fillStyle=fg;x.textAlign='center';x.textBaseline='middle';x.fillText(s,0,size*.06);x.restore()};
// Fondo azul con un círculo punteado que gira y otro translúcido (como la portada de Facebook)
const bg=(t,tinte=C.bg)=>{x.fillStyle=/^#[12]/.test(tinte)?tinte:C.bg;x.fillRect(0,0,W,H);
 x.save();x.fillStyle='rgba(255,255,255,.07)';x.beginPath();x.arc(-120+Math.sin(t*.6)*30,H-260,620,0,7);x.fill();x.restore();
 x.save();x.translate(W-60,560);x.rotate(t*.25);x.strokeStyle='rgba(255,255,255,.22)';x.lineWidth=7;x.setLineDash([26,22]);x.beginPath();x.arc(0,0,430,0,7);x.stroke();x.restore();
 x.fillStyle=C.so;x.fillRect(0,0,W,16);x.fillRect(0,H-16,W,16)};
const P=[...Array(70)].map((_,i)=>({x:(i*137)%W,y:-((i*311)%H),v:300+(i*53)%420,r:i,s:12+(i*7)%16,c:[C.so,C.ro,'#ffffff',C.so][i%4]}));
const conf=t=>P.forEach(p=>{const y=(p.y+p.v*t)%(H+200)-100;x.save();x.translate(p.x+Math.sin(t*2+p.r)*30,y<-100?y+H+200:y);x.rotate(t*3+p.r);x.fillStyle=p.c;x.fillRect(-p.s/2,-p.s/4,p.s,p.s/2);x.restore()});
const logo=()=>{pill('REBAJÓN',W/2-45,370,44,C.so,C.in,{rot:-.04});pill('MX',W/2+148,388,30,C.ro,'#fff',{rot:.07})};
const shake=(t,k=14)=>t>0&&t<.3?[(Math.sin(t*90)*k*(1-t/.3)),(Math.cos(t*70)*k*(1-t/.3))]:[0,0];
// Tarjeta blanca con sombra y la foto del producto (o un emoji si la foto no carga)
const foto=(d,X,Y,cw,sc=1,al=1)=>{x.save();x.globalAlpha=cl(al);x.translate(X,Y);x.scale(sc,sc);x.shadowColor='rgba(20,26,51,.16)';x.shadowBlur=50;x.shadowOffsetY=18;x.beginPath();x.roundRect(-cw/2,-cw/2,cw,cw,44);x.fillStyle='#fff';x.fill();x.shadowColor='transparent';
 const im=pre[d.img];if(im){const r=Math.min((cw-56)/im.width,(cw-56)/im.height);x.drawImage(im,-im.width*r/2,-im.height*r/2,im.width*r,im.height*r)}else{x.font=F(cw*.42);x.textAlign='center';x.textBaseline='middle';x.fillText(d.e,0,0)}x.restore()};
const precio=(d,t,t0,yN,yP,yA)=>{T(d.n,W/2,yN,60,C.tx,{al:(t-t0)/.15,max:900});
 const cnt=d.was-(d.was-d.now)*E((t-t0-.1)/.55);T(money(t>t0+.7?d.now:Math.round(cnt)),W/2,yP,112,C.so,{al:(t-t0-.05)/.1,sc:B((t-t0-.05)/.3)});
 x.save();x.font=F(50,700);const ws='antes '+money(d.was),ww=x.measureText(ws).width;T(ws,W/2,yA,50,C.tm,{w:700,al:(t-t0-.2)/.15});x.globalAlpha=cl((t-t0-.2)/.15);x.fillStyle=C.ro;x.fillRect(W/2-ww/2,yA-3,ww,5);x.restore();
 pill('🛒 en Mercado Libre',W/2,yA+95,36,'#fff',C.in,{al:(t-t0-.35)/.2})};
const cta=t=>{bg(t);conf(t);logo();
 T('Solo ofertas',W/2,560,104,C.tx,{sc:B(t/.4),al:t/.15});T('REALES ✅',W/2,685,124,C.so,{sc:B((t-.15)/.4),al:(t-.15)/.15});
 T('con link directo a la tienda',W/2,795,48,C.tm,{w:700,al:(t-.4)/.3});
 const pu=1+Math.sin(t*8)*.03;pill('🌐 rebajonmx.netlify.app',W/2,910,54,C.so,C.in,{sc:B((t-.6)/.4)*pu,al:(t-.6)/.15});
 pill('🔔 Alertas gratis en WhatsApp',W/2,1050,48,C.ok,'#fff',{sc:B((t-.9)/.4),al:(t-.9)/.15});
 T('📌 Links en el perfil y en los comentarios',W/2,1185,44,C.tx,{al:(t-1.2)/.3});
 T('Síguenos para más rebajas 🔥',W/2,1290,42,C.tm,{w:700,al:(t-1.5)/.3})};
let S=[];
if(id===1){S=[
 {d:2.4,f:t=>{bg(t);logo();const [a,b]=shake(t,18);x.save();x.translate(a,b);T('ALTO ✋',W/2,640,190,C.so,{sc:B(t/.35)});x.restore();
  T('No compres NADA',W/2,850,88,C.tx,{al:(t-.5)/.15,sc:B((t-.5)/.35)});T('en el Buen Fin',W/2,960,88,C.tx,{al:(t-.85)/.15,sc:B((t-.85)/.35)});
  pill('sin ver esto 👀',W/2,1120,72,C.so,C.in,{al:(t-1.2)/.15,sc:B((t-1.2)/.35),rot:-.04})}},
 {d:2.4,f:t=>{bg(t);logo();T(K.eb,W/2,560,60,C.so,{al:t/.2});
  T(K.l1,W/2,740,200,C.tx,{sc:B((t-.15)/.4),al:(t-.15)/.1});T(K.l2,W/2,905,96,C.tx,{al:(t-.5)/.2,sc:B((t-.5)/.35)});
  pill(K.badge,W/2,1070,70,C.ro,'#fff',{sc:B((t-.85)/.35)*(1+Math.sin(t*10)*.04),al:(t-.85)/.1})}},
 ...[0,1,2,3].map(k=>({d:1.7,f:t=>{const d=D[k];bg(t+k,TINTES[k%4],k%2?C.ro:C.co);logo();foto(d,W/2,720,420,.55+.45*B(t/.3),t/.1);
  const [a,b]=shake(t-.2,20);x.save();x.translate(a,b);pill('-'+d.off+'%',W/2+240,545,80,C.ro,'#fff',{rot:.1,sc:t<.2?0:2-1*E((t-.2)/.2)});x.restore();
  precio(d,t,.3,1010,1120,1220)}})),
 {d:3.4,f:cta}]}
if(id===2){const top=[...D].sort((a,b)=>a.off-b.off).slice(-5);
 S=[{d:2,f:t=>{bg(t);conf(t);logo();T('TOP 5',W/2,700,260,C.so,{sc:B(t/.4),al:t/.1});T('rebajas de HOY',W/2,900,96,C.tx,{al:(t-.4)/.15,sc:B((t-.4)/.35)});pill('en Mercado Libre',W/2,1045,58,C.ro,'#fff',{al:(t-.8)/.15,sc:B((t-.8)/.35)})}},
 ...top.map((d,k)=>({d:2.4,f:t=>{bg(t+k,TINTES[k%4],k%2?C.ro:C.co);logo();foto(d,W/2,720,430,.6+.4*E(t/.35),t/.2);
  pill('#'+(5-k),W/2-250,535,56,C.so,C.in,{rot:-.08,sc:B(t/.3)});pill('-'+d.off+'%',W/2+245,550,78,C.ro,'#fff',{rot:.1,sc:t<.4?0:2-1*E((t-.4)/.2)});
  precio(d,t,.35,1015,1125,1225)}})),
 {d:3.4,f:cta}]}
if(id===3){S=[
 {d:2.6,f:t=>{bg(t);logo();T('¿Ese -50%',W/2,720,160,C.tx,{sc:B(t/.35),al:t/.1});T('es REAL? 🤔',W/2,920,160,C.so,{sc:B((t-.5)/.35),al:(t-.5)/.1})}},
 {d:3.4,f:t=>{bg(t);logo();T('Muchas tiendas SUBEN',W/2,540,76,C.tx,{al:t/.2});T('el precio antes del Buen Fin',W/2,630,54,C.so,{w:800,al:(t-.3)/.2});
  const pts=[[170,1160],[450,1160],[640,860],[910,1160]],k=cl((t-.6)/1.6)*3;x.save();x.lineWidth=16;x.lineCap='round';x.lineJoin='round';x.strokeStyle=C.so;x.beginPath();x.moveTo(...pts[0]);
  for(let i=1;i<=3;i++){const f=cl(k-(i-1));if(f<=0)break;const [ax,ay]=pts[i-1],[bx,by]=pts[i];x.lineTo(ax+(bx-ax)*f,ay+(by-ay)*f)}x.stroke();x.restore();
  if(k>0)T('$999',260,1230,52,C.tx);if(k>1.6)pill('$1,499',640,790,52,C.ro,'#fff',{sc:B((k-1.6)/.6)});if(k>2.6)T('-33% = $999',870,1230,52,C.so);
  T('Mismo precio de antes 🙃',W/2,1360,66,C.tx,{al:(t-2.5)/.2,sc:B((t-2.5)/.35)})}},
 {d:3,f:t=>{bg(t);logo();T('Nosotros revisamos',W/2,560,90,C.tx,{al:t/.15,sc:B(t/.35)});T('antes vs. ahora',W/2,670,90,C.so,{al:(t-.2)/.15,sc:B((t-.2)/.35)});
  ['Precio real de antes','Descuento verificado','Link directo a la tienda'].forEach((s,i)=>{const tt=t-.6-i*.4,Y=830+i*140;x.save();x.globalAlpha=cl(tt/.15);x.translate(-60*(1-E(tt/.3)),0);x.beginPath();x.arc(210,Y,46,0,7);x.fillStyle=C.so;x.fill();x.restore();
   T('✓',210,Y+2,58,C.in,{al:tt/.15});x.save();x.globalAlpha=cl(tt/.15);x.font=F(56,800);x.fillStyle=C.tx;x.textBaseline='middle';x.fillText(s,285,Y+2);x.restore()})}},
 {d:3.4,f:cta}]}
const dur=S.reduce((a,s)=>a+s.d,0);
const draw=t=>{let a=0;for(const s of S){if(t<a+s.d||s===S[S.length-1]){s.f(Math.min(t-a,s.d));break}a+=s.d}};
return {c,x,dur,draw}}
// Música propia (sin derechos): cada video y cada día suena distinto (tempo, tono, bajo y melodía).
function beat(ac,out,dur,id){let s=((SEED*31+id*977)%2147483646)+1;const R=()=>(s=s*16807%2147483647)/2147483647;
 const estilos=[{bpm:128,esc:[0,3,5,7,10],onda:'sawtooth',arp:'square'},{bpm:116,esc:[0,2,4,7,9],onda:'square',arp:'triangle'},{bpm:100,esc:[0,3,5,7,10],onda:'triangle',arp:'sine'},{bpm:122,esc:[0,2,4,7,9],onda:'sawtooth',arp:'triangle'},{bpm:108,esc:[0,2,3,7,8],onda:'square',arp:'sine'}];
 const st=estilos[(id+SEED)%estilos.length],raiz=[55,58.27,61.74,65.41,69.3,73.42][Math.floor(R()*6)],bpm=st.bpm+Math.floor(R()*6)-3,sp=60/bpm,t0=ac.currentTime+.05;
 const g=ac.createGain();g.gain.value=.5;g.connect(out);const nb=ac.createBuffer(1,ac.sampleRate*.2,ac.sampleRate),nd=nb.getChannelData(0);for(let i=0;i<nd.length;i++)nd[i]=Math.random()*2-1;
 const f=n=>raiz*Math.pow(2,n/12),prog=[0,st.esc[3]-12,st.esc[2],st.esc[1]],patB=[...Array(8)].map(()=>R()<.7),patA=[...Array(8)].map(()=>st.esc[Math.floor(R()*5)]+12*(1+Math.floor(R()*2)));
 const nota=(tipo,fr,t,len,vol,lp)=>{const o=ac.createOscillator(),gg=ac.createGain(),fl=ac.createBiquadFilter();o.type=tipo;o.frequency.value=fr;fl.type='lowpass';fl.frequency.value=lp;gg.gain.setValueAtTime(.0001,t);gg.gain.exponentialRampToValueAtTime(vol,t+.015);gg.gain.exponentialRampToValueAtTime(.0005,t+len);o.connect(fl).connect(gg).connect(g);o.start(t);o.stop(t+len+.05)};
 const hats=st.bpm>110?2:1;
 for(let i=0;i*sp<dur;i++){const t=t0+i*sp,raizC=prog[Math.floor(i/4)%4];
  const o=ac.createOscillator(),k=ac.createGain();o.frequency.setValueAtTime(150,t);o.frequency.exponentialRampToValueAtTime(42,t+.22);k.gain.setValueAtTime(st.bpm<105?.8:1,t);k.gain.exponentialRampToValueAtTime(.001,t+.32);o.connect(k).connect(g);o.start(t);o.stop(t+.35);
  if(i%2){const n=ac.createBufferSource(),ng=ac.createGain(),bf=ac.createBiquadFilter();n.buffer=nb;bf.type='bandpass';bf.frequency.value=1800;ng.gain.setValueAtTime(.45,t);ng.gain.exponentialRampToValueAtTime(.001,t+.16);n.connect(bf).connect(ng).connect(g);n.start(t);n.stop(t+.2)}
  for(let h=0;h<hats;h++){const th=t+sp*(h+.5)/hats,n=ac.createBufferSource(),hf=ac.createBiquadFilter(),hg=ac.createGain();n.buffer=nb;hf.type='highpass';hf.frequency.value=7500;hg.gain.setValueAtTime(.25,th);hg.gain.exponentialRampToValueAtTime(.001,th+.05);n.connect(hf).connect(hg).connect(g);n.start(th);n.stop(th+.07)}
  for(let e=0;e<2;e++){const te=t+e*sp/2,paso=(i*2+e)%8;if(patB[paso])nota(st.onda,f(raizC-12),te,sp*.45,.2,600);if(i>=8&&(paso%2===0||R()<.3))nota(st.arp,f(raizC+patA[paso]),te,sp*.4,.07,3200)}}}
const FPS=30,cache={};const get=async id=>cache[id]||(cache[id]=await build(id));
async function audio(id,dur){const sr=48000,ac=new OfflineAudioContext(2,Math.ceil(sr*(dur+.2)),sr);beat(ac,ac.destination,dur,id);return ac.startRendering()}
// Cuántas fotos de producto cargaron (revisar antes de publicar: deben ser todas)
window.RVfotos=async()=>{const p=await fotos();const v=Object.values(p);return {cargadas:v.filter(Boolean).length,total:v.length}};
// Navegador con WebCodecs: arma el MP4 cuadro por cuadro (fluido aunque la ventana esté oculta).
window.RV=async id=>{const v=await get(id),N=Math.round(v.dur*FPS),ab=await audio(id,v.dur);
 const mux=new Mp4Muxer.Muxer({target:new Mp4Muxer.ArrayBufferTarget(),video:{codec:'avc',width:W,height:H,frameRate:FPS},audio:{codec:'aac',numberOfChannels:2,sampleRate:48000},fastStart:'in-memory',firstTimestampBehavior:'offset'});
 let err=null;const ve=new VideoEncoder({output:(c,m)=>mux.addVideoChunk(c,m),error:e=>err=e});ve.configure({codec:'avc1.640028',width:W,height:H,bitrate:7e6,framerate:FPS,avc:{format:'avc'}});
 for(let i=0;i<N;i++){v.draw(i/FPS);const fr=new VideoFrame(v.c,{timestamp:Math.round(i*1e6/FPS),duration:Math.round(1e6/FPS)});ve.encode(fr,{keyFrame:i%(FPS*2)===0});fr.close();while(ve.encodeQueueSize>6)await new Promise(r=>setTimeout(r,4));if(err)throw err}
 await ve.flush();
 const ae=new AudioEncoder({output:(c,m)=>mux.addAudioChunk(c,m),error:e=>err=e});ae.configure({codec:'mp4a.40.2',sampleRate:48000,numberOfChannels:2,bitrate:128000});
 const L=ab.getChannelData(0),R=ab.getChannelData(1),n=Math.min(L.length,Math.round(v.dur*48000));
 for(let o=0;o<n;o+=1024){const k=Math.min(1024,n-o),buf=new Float32Array(k*2);buf.set(L.subarray(o,o+k),0);buf.set(R.subarray(o,o+k),k);const a=new AudioData({format:'f32-planar',sampleRate:48000,numberOfFrames:k,numberOfChannels:2,timestamp:Math.round(o*1e6/48000),data:buf});ae.encode(a);a.close()}
 await ae.flush();if(err)throw err;mux.finalize();
 const f=new File([mux.target.buffer],'rebajonmx-video-'+id+'.mp4',{type:'video/mp4'});window.__vids=window.__vids||{};window.__vids[id]=f;return {name:f.name,mb:+(f.size/1e6).toFixed(2),dur:v.dur,frames:N}};
// Sin WebCodecs (servidor): Python pide cada cuadro en JPG y el audio en WAV; ffmpeg arma el MP4.
window.RVinfo=async id=>{const v=await get(id);return {dur:v.dur,frames:Math.round(v.dur*FPS),fps:FPS}};
window.RVframe=async(id,i)=>{const v=await get(id);v.draw(i/FPS);return v.c.toDataURL('image/jpeg',.92).split(',')[1]};
window.RVwav=async id=>{const v=await get(id),ab=await audio(id,v.dur),n=Math.round(v.dur*48000),b=new DataView(new ArrayBuffer(44+n*4)),w=(o,s)=>[...s].forEach((ch,i)=>b.setUint8(o+i,ch.charCodeAt(0)));
 w(0,'RIFF');b.setUint32(4,36+n*4,true);w(8,'WAVEfmt ');b.setUint32(16,16,true);b.setUint16(20,1,true);b.setUint16(22,2,true);b.setUint32(24,48000,true);b.setUint32(28,192000,true);b.setUint16(32,4,true);b.setUint16(34,16,true);w(36,'data');b.setUint32(40,n*4,true);
 const L=ab.getChannelData(0),R=ab.getChannelData(1);for(let i=0;i<n;i++){b.setInt16(44+i*4,Math.max(-1,Math.min(1,L[i]))*32767,true);b.setInt16(46+i*4,Math.max(-1,Math.min(1,R[i]))*32767,true)}
 const u=new Uint8Array(b.buffer);let s='';for(let i=0;i<u.length;i+=0x8000)s+=String.fromCharCode(...u.subarray(i,i+0x8000));return btoa(s)};
})();
