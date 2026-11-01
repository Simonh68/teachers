/* Universal Teachers QR / phone remote. This is a controller, NOT a URL-only QR.
   Shared across grade 7–12 and seminar presentations; independent of Firebase.
   Existing Sentence Detective remote modules are intentionally excluded. */
(() => {
"use strict";
if (window.teachersPhoneRemote || document.querySelector("#remoteToggle,#pairDialog")) return;
const params=new URLSearchParams(location.search), pairing=params.get("teacherRemote");
const controller=pairing!==null;
const ctx={role:controller?"controller":"presenter",connected:false,peer:null,channel:null,pending:null,authorized:null,version:0,lastStatus:"",timer:0,lastAction:0,lastSnapshot:""};
window.teachersPhoneRemote=ctx;
const host=document.createElement("div");host.id="teachers-qr-remote-host";host.style.cssText="all:initial";
const root=host.attachShadow({mode:"open"});
root.innerHTML=`<style>
:host{font-family:Arial,sans-serif;direction:rtl;color:white}*,*:before,*:after{box-sizing:border-box}[hidden]{display:none!important}
button,input{font-family:Arial,sans-serif}button{cursor:pointer}
#launch{position:fixed;right:12px;top:12px;z-index:2147482000;background:#103e5a!important;border:2px solid #8ee2f2!important;border-radius:999px!important;color:white!important;box-shadow:0 5px 18px #0019!important;padding:9px 13px!important;font:800 14px Arial!important;cursor:pointer}
#overlay{position:fixed;inset:0;z-index:2147483000;background:#000b;overflow:auto;display:flex;align-items:center;justify-content:center;padding:12px}
.panel{max-width:520px;width:100%;background:#102c42;color:#f4fbff;border:2px solid #5586a1;border-radius:20px;padding:clamp(15px,3vw,27px);box-shadow:0 25px 70px #0009;line-height:1.45;direction:rtl;text-align:right}
h1{font:900 clamp(25px,4vw,32px) Arial;margin:0 0 14px;color:#fff2bd}p{font-size:16px;margin:7px 0 12px}.en{direction:ltr;text-align:left;font-size:14px;color:#c1e6f5}
.row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:10px}.row button,.controls button,#reconnect{border:1px solid #a1d6ef;border-radius:10px;background:#1d5c7a;color:#fff;padding:10px 13px;font:800 16px Arial;min-height:44px}.row button.approve{background:#ffe291;border-color:#ffe291;color:#19334a}.row button:disabled,.controls button:disabled{opacity:.35;cursor:default}
.status{padding:11px;border-radius:9px;border:1px solid #74a3bb;background:#193a51;min-height:40px;margin:12px 0;font-size:15px}.status.ok{color:#cbffdf;border-color:#9be0b7}.status.error{border-color:#eeb0a8;color:#ffe2df}
#qr{width:238px;height:238px;max-width:100%;background:white;color:#112c3a;margin:14px auto;border-radius:13px;padding:8px;display:grid;place-items:center;font-size:14px;text-align:center}#qr img,#qr canvas{max-width:100%;height:auto}
#link{width:100%;font:13px Arial;padding:10px;background:#081c2b;color:#e7ffff;border:1px solid #769bb1;border-radius:7px;direction:ltr;text-align:left}
.counter{font:900 clamp(30px,9vw,48px) Arial,sans-serif;text-align:center;color:#ffe28e;margin:12px 0}.controls{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin:13px 0}.controls button{font-size:27px;min-height:85px}.controls .wide{grid-column:1/-1;min-height:58px;font-size:18px}
.help{font-size:13px;opacity:.92}.title{font-size:15px;text-align:center;overflow-wrap:anywhere}#remote [data-conn]{text-align:center}.close{margin-inline-start:auto}
@media(max-width:560px){.panel{padding:17px}#qr{height:201px;width:201px}.controls button{min-height:95px}}
</style>
<button id="launch" type="button" title="שלט טלפון QR / QR phone controller">📱 QR / שלט</button>
<div id="overlay" hidden role="dialog" aria-label="שלט למצגת / Presentation remote" aria-modal="true">
 <section id="presenter" class="panel" hidden>
  <h1>📱 חיבור טלפון כשלט למצגת</h1>
  <p><strong>מה עושים עם הקוד?</strong> סורקים בטלפון את קוד ה־QR. במחשב מאשרים את בקשת החיבור. לאחר האישור הטלפון שולט בשקפים המוצגים במקרן.</p>
  <p class="en"><strong>What is this code for?</strong> Scan the QR with your phone. Approve the connection on the computer. Then use the phone as a remote for the projected slides.</p>
  <div id="qr" role="img" aria-label="קוד QR זמני לחיבור טלפון כשלט">יוצר קוד QR…</div>
  <label for="link">העתקת קישור / Copy pairing link</label><input id="link" type="text" readonly>
  <div class="row"><button id="copy">העתקה / Copy</button><button id="approve" class="approve" hidden>✓ אישור הטלפון / Approve</button></div>
  <div class="status" id="status" role="status" aria-live="polite">מכין חיבור…</div>
  <div class="row"><button id="reset">↻ קוד חדש / New QR</button><button id="close" class="close">סגור / Close</button></div>
  <p class="help">אין הרשמה או שמירת שם/דוא״ל. רק טלפון שאושר במחשב יכול לשלוט.<span class="en" style="display:block">No sign-up or names/emails saved. Only an approved phone may control the presentation.</span></p>
 </section>
 <section id="remote" class="panel" hidden>
  <h1 style="text-align:center">📱 שלט למצגת / Remote</h1>
  <div class="status" id="remote-status" role="status" data-conn>מחכה לאישור / Waiting for approval</div>
  <div class="counter" id="counter" dir="ltr">—</div><div class="title" id="deck-title"></div>
  <div class="controls">
   <button id="previous" disabled>←<div style="font-size:15px">הקודם / Previous</div></button>
   <button id="next" disabled>→<div style="font-size:15px">הבא / Next</div></button>
   <button id="reveal" class="wide" disabled>✨ חשיפת רמז / Reveal</button>
   <button id="audio" class="wide" disabled>🔊 הפעלה / השהיה — Play / Pause</button>
  </div>
  <p class="help" style="text-align:center">החליקו שמאלה/למעלה כדי להתקדם, ימינה/למטה כדי לחזור.<span class="en" style="display:block;text-align:center">Swipe left/up for next; right/down for previous.</span></p>
  <div class="row"><button id="reconnect">↻ התחבר שוב / Reconnect</button></div>
 </section>
</div>`;
const $=id=>root.getElementById(id), overlay=$("overlay");
function mount(){if(document.body&&!host.isConnected)document.body.append(host);}
mount();
// Several Read-Along engines replace body.innerHTML while initializing.
new MutationObserver(()=>{if(!host.isConnected)mount();}).observe(document.body,{childList:true});
let libs=null,expiry=null;
function status(text,tone=""){const el=$(controller?"remote-status":"status");el.textContent=text;el.className="status "+tone;ctx.lastStatus=text;}
function panel(){overlay.hidden=false;$("launch").hidden=true;$("remote").hidden=!controller;$("presenter").hidden=controller;}
function hide(){if(controller)return;overlay.hidden=true;$("launch").hidden=false;}
function inject(url,check){
 if(check())return Promise.resolve();
 return new Promise((resolve,reject)=>{
  const el=document.createElement("script");el.src=url;el.async=true;
  const timer=setTimeout(()=>{el.remove();reject(Error("Loading library timed out"));},15000);
  el.onload=()=>{clearTimeout(timer);check()?resolve():reject(Error("Library missing"))};
  el.onerror=()=>{clearTimeout(timer);reject(Error("Library unavailable"))};
  document.head.append(el);
 });
}
async function libraries(){
 if(!libs)libs=(async()=>{
  await inject("https://cdn.jsdelivr.net/npm/peerjs@1.5.5/dist/peerjs.min.js",()=>typeof window.Peer==="function");
  if(!controller)try{await inject("https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js",()=>typeof window.QRCode==="function");}catch(e){console.warn("QR unavailable; link works",e);}
 })().catch(e=>{libs=null;throw e});
 return libs;
}
function send(conn,data){if(conn?.open)try{conn.send(data);}catch(e){console.error("QR remote send:",e);}}
function setButtons(ready){for(const name of ["next","previous","reveal","audio"])$(name).disabled=!ready;}
function reset(){
 ctx.connected=false;ctx.authorized=null;ctx.lastSnapshot="";
 clearInterval(ctx.timer);ctx.timer=0;clearTimeout(expiry);
 try{ctx.channel?.close()}catch(e){}ctx.channel=null;
 try{ctx.pending?.close()}catch(e){}ctx.pending=null;
 try{ctx.peer?.destroy()}catch(e){}ctx.peer=null;
 setButtons(false);$("approve").hidden=true;
}
function link(id){
 const url=new URL(location.href);url.hash="";url.searchParams.delete("remote");url.searchParams.delete("sync");
 url.searchParams.set("teacherRemote",id);return url.href;
}
function showQR(id){
 const url=link(id);$("link").value=url;$("qr").replaceChildren();
 if(typeof window.QRCode==="function")try{
  new QRCode($("qr"),{text:url,width:219,height:219,colorDark:"#0b2031",colorLight:"#ffffff",correctLevel:QRCode.CorrectLevel.M});
 }catch(e){$("qr").textContent="QR לא זמין. השתמשו בקישור להעתקה.";}
 else $("qr").textContent="קוד QR לא נטען. העתיקו את הקישור מתחתיו.";
}
function snapshot(){
 let count="";
 if(window.__grade8Bilingual?.ready){
  const d=window.__grade8Bilingual;count=(d.page+1)+(d.reveal?" + תרגום":"")+" / "+d.pages.length;
 }else{
  for(const selector of ["#counter","#slide-counter","#slideCounter","#count",".counter",".page-number","#step-counter"]){
   const el=document.querySelector(selector);
   if(el){const value=el.textContent.trim().replace(/\s+/g," ");if(value.length>0&&value.length<55){count=value;break;}}
  }
  if(!count){
   const slides=[...document.querySelectorAll(".slide")],index=slides.findIndex(e=>e.classList.contains("active")&&!e.hidden);
   if(index>=0)count=(index+1)+" / "+slides.length;
  }
 }
 return {type:"state",counter:count||"מחובר / Connected",title:document.title.slice(0,100)};
}
function update(force=false){
 if(controller||!ctx.connected||!ctx.channel?.open)return;
 const data=snapshot(),sig=JSON.stringify(data);
 if(!force&&sig===ctx.lastSnapshot)return;
 ctx.lastSnapshot=sig;send(ctx.channel,data);
}
function clickFirst(selectors){
 for(const selector of selectors){
  const matches=[...document.querySelectorAll(selector)];
  const el=matches.find(e=>{
   if(host.contains(e)||e.disabled||e.hidden||e.getAttribute("aria-disabled")==="true")return false;
   const cs=getComputedStyle(e),r=e.getBoundingClientRect();
   return cs.display!=="none"&&cs.visibility!=="hidden"&&r.width>0;
  });
  if(el){el.click();return true;}
 }
 return false;
}
function nav(forward){
 const s=forward?[
  ".navigation [data-step='1']",".nav [data-step='1']","[data-step='1']","#deck-next","#deck-down","#next","#down","#nextBtn","#nextSlide"
 ]:[
  ".navigation [data-step='-1']",".nav [data-step='-1']","[data-step='-1']","#deck-prev","#deck-up","#prev","#up","#prevBtn","#previousSlide"
 ];
 if(clickFirst(s))return;
 document.dispatchEvent(new KeyboardEvent("keydown",{key:forward?"ArrowRight":"ArrowLeft",bubbles:true,cancelable:true}));
}
function execute(cmd){
 if(cmd==="next")nav(true);
 else if(cmd==="previous")nav(false);
 else if(cmd==="reveal"){
  if(!clickFirst(["[data-reveal='answer']","#reveal","#why","#showAnswer","#show-answer","#hintToggle","#translate",".reveal-btn","[aria-label*='חשיפה']","[aria-label*='Reveal']"]))nav(true);
 }else if(cmd==="audio")clickFirst(["#play","#playBtn","#audioPlay","#audioBtn","#play-pause",".audio-play-button","[data-audio-action='toggle']"]);
 setTimeout(()=>update(true),120);
}
function connected(){
 ctx.connected=true;status(controller?"✓ מחובר לשקפים / Connected":"✓ הטלפון אושר ומחובר / Phone approved","ok");
 if(controller)setButtons(true);
 else{update(true);clearInterval(ctx.timer);ctx.timer=setInterval(()=>update(false),500);}
}
async function startHost(){
 reset();panel();ctx.version++;const version=ctx.version;
 $("qr").textContent="מכין QR…";$("link").value="";
 status("📱 מכין חיבור זמני… / Preparing pairing");
 try{
  await libraries();if(ctx.version!==version)return;
  ctx.peer=new Peer();
  ctx.peer.on("open",id=>{
   if(ctx.version!==version)return;
   showQR(id);status("📱 סרקו בטלפון ואז אשרו במחשב / Scan and approve on computer");
   expiry=setTimeout(()=>{reset();status("הקוד פג תוקף — צרו קוד חדש / Code expired; reset");},4*60*60*1000);
  });
  ctx.peer.on("connection",conn=>{
   conn.on("open",()=>{
    if(ctx.authorized&&ctx.authorized===conn.peer){ctx.channel=conn;send(conn,{type:"approved"});connected();return;}
    if(ctx.authorized){send(conn,{type:"denied"});conn.close();return;}
    if(ctx.pending&&ctx.pending!==conn){send(conn,{type:"busy"});conn.close();return;}
    ctx.pending=conn;$("approve").hidden=false;panel();
    status("בקשת חיבור התקבלה — אשרו במחשב / Approve this phone");
   });
   conn.on("data",data=>{
    if(conn!==ctx.channel||!ctx.connected||!data)return;
    if(data.type==="command"&&["next","previous","reveal","audio"].includes(data.action)){
     // Every deliberate tap must be honored, including immediate next/previous.
     // Authorization is already checked above; never silently drop navigation.
     ctx.lastAction=Date.now();execute(data.action);
    }else if(data.type==="ping")update(true);
   });
   conn.on("close",()=>{
    if(conn===ctx.channel){ctx.channel=null;ctx.connected=false;clearInterval(ctx.timer);status("הטלפון נותק / Remote disconnected");}
    if(conn===ctx.pending){ctx.pending=null;$("approve").hidden=true;}
   });
  });
  ctx.peer.on("disconnected",()=>{try{ctx.peer.reconnect()}catch(e){}});
  ctx.peer.on("error",e=>status("שגיאה בחיבור / Connection error: "+(e.type||"network"),"error"));
 }catch(e){console.error("Phone remote:",e);status("השלט אינו זמין. אפשר להמשיך במצגת / Remote unavailable; slides still work.","error");}
}
async function startPhone(){
 reset();panel();ctx.version++;const version=ctx.version;
 status("📱 מתחבר למחשב… / Connecting to projector");
 if(!/^[a-zA-Z0-9_-]{6,128}$/.test(pairing||"")){status("קישור לא תקין / Invalid code","error");return;}
 try{
  await libraries();if(ctx.version!==version)return;
  ctx.peer=new Peer();
  ctx.peer.on("open",()=>{
   if(ctx.version!==version)return;
   const conn=ctx.peer.connect(pairing,{serialization:"json"});ctx.channel=conn;
   const watchdog=setTimeout(()=>{if(!ctx.connected){status("לא ניתן להתחבר. נסו שוב / Computer unavailable","error");conn.close();}},15000);
   conn.on("open",()=>{clearTimeout(watchdog);status("בקשה נשלחה. אשרו במחשב / Waiting for computer approval");send(conn,{type:"ping"});});
   conn.on("data",data=>{
    if(conn!==ctx.channel||!data)return;
    if(data.type==="approved"){connected();send(conn,{type:"ping"});}
    else if(data.type==="state"&&ctx.connected){$("counter").textContent=String(data.counter||"—").slice(0,75);$("deck-title").textContent=String(data.title||"").slice(0,100);}
    else if(data.type==="denied"||data.type==="busy"){ctx.connected=false;setButtons(false);status("לא אושר. סרקו קוד חדש / Not approved","error");}
   });
   conn.on("close",()=>{clearTimeout(watchdog);ctx.connected=false;setButtons(false);status("החיבור נותק. התחברו שוב / Disconnected","error");});
  });
  ctx.peer.on("error",e=>status("שגיאת רשת / Connection error: "+(e.type||"network"),"error"));
 }catch(e){console.error("Phone remote:",e);status("לא ניתן לחבר שלט / Remote connection unavailable","error");}
}
$("launch").onclick=startHost;
$("close").onclick=hide;
$("reset").onclick=startHost;
$("approve").onclick=()=>{
 const conn=ctx.pending;
 if(!conn?.open||ctx.authorized)return;
 ctx.pending=null;ctx.authorized=conn.peer;ctx.channel=conn;
 $("approve").hidden=true;send(conn,{type:"approved"});connected();hide();
};
$("copy").onclick=async()=>{
 if(!$("link").value)return;
 try{await navigator.clipboard.writeText($("link").value);$("copy").textContent="✓ הועתק / Copied";}
 catch(e){$("link").focus();$("link").select();$("copy").textContent="בחרו והעתיקו / Select and copy";}
};
for(const [id,action] of [["next","next"],["previous","previous"],["reveal","reveal"],["audio","audio"]])
 $(id).onclick=()=>{if(ctx.connected)send(ctx.channel,{type:"command",action});};
$("reconnect").onclick=startPhone;
let swipe=null;
$("remote").addEventListener("touchstart",e=>{
 if(e.touches.length!==1||e.target.closest("button,input,a")){swipe=null;return;}
 swipe={x:e.touches[0].clientX,y:e.touches[0].clientY};
},{passive:true});
$("remote").addEventListener("touchend",e=>{
 if(!swipe||e.changedTouches.length!==1)return;
 const dx=e.changedTouches[0].clientX-swipe.x,dy=e.changedTouches[0].clientY-swipe.y;swipe=null;
 if(ctx.connected&&Math.max(Math.abs(dx),Math.abs(dy))>=55)
  send(ctx.channel,{type:"command",action:(Math.abs(dx)>Math.abs(dy)?dx:dy)<0?"next":"previous"});
},{passive:true});
$("deck-title").textContent=document.title.slice(0,95);
if(controller)startPhone();
window.addEventListener("pagehide",reset);
})();