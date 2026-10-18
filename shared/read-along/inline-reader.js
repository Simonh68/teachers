/* Inline Read Along support: recorded audio plus contextual hover/tap glosses.
   The host supplies existing text spans and JSON. No speech service runs in the browser. */
(function(root){
'use strict';
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
function buildSegments(records,first,last){
 return records.flatMap(r=>(r.phrases||[{first:r.words[0].id,last:r.words.at(-1).id,gapMs:2000,pauseKind:'sentence'}]).flatMap(phrase=>{
  const words=r.words.filter(w=>w.id>=Math.max(first,phrase.first)&&w.id<=Math.min(last,phrase.last));
  if(!words.length)return [];
  const next=r.words.find(w=>w.id===words.at(-1).id+1);
  return [{src:r.src,words,start:Math.max(0,words[0].start-.02),end:Math.min(words.at(-1).end+.04,next?next.start-.005:r.duration),gapMs:phrase.gapMs,pauseKind:phrase.pauseKind}];
 }));
}
class RecordedReader{
 constructor(records,{media,onState=()=>{},onWord=()=>{},clock=globalThis}={}){
  this.records=records;this.media=media||new Audio();this.onState=onState;this.onWord=onWord;this.clock=clock;
  this.media.preload='none';this.media.preservesPitch=true;this.rate=.75;this.phase='idle';this.segments=[];this.part=0;this.epoch=0;this.timer=null;this.frame=null;this.lastWord=-1;this.owner=null;
  this.media.addEventListener('ended',()=>{if(this.phase==='playing')this.advance();});
  this.media.addEventListener('error',()=>{if(['loading','playing'].includes(this.phase))this.fail();});
 }
 emit(){this.onState(this);}
 clearTimers(){this.clock.clearTimeout(this.timer);this.clock.cancelAnimationFrame(this.frame);this.timer=null;this.frame=null;}
 stop(){this.epoch++;this.clearTimers();this.media.pause();this.phase='idle';this.segments=[];this.lastWord=-1;this.onWord(-1);this.emit();}
 playRange(first,last,owner){this.stop();this.owner=owner;this.segments=buildSegments(this.records,first,last);this.part=0;if(this.segments.length)this.load(this.part);}
 async load(part){
  this.clearTimers();this.part=part;const s=this.segments[part];if(!s)return;const token=++this.epoch;
  this.media.pause();this.phase='loading';this.emit();
  try{
   if(this.source!==s.src){this.source=s.src;this.media.src=s.src;this.media.load();}this.media.playbackRate=this.rate;
   // Seek once metadata is available on engines that reset currentTime during load().
   if(this.media.readyState<1)await new Promise((resolve,reject)=>{const clean=()=>{this.media.removeEventListener('loadedmetadata',ok);this.media.removeEventListener('error',bad);this.clock.clearTimeout(timeout);};const ok=()=>{clean();resolve();};const bad=()=>{clean();reject(Error('Audio unavailable'));};const timeout=this.clock.setTimeout(bad,15000);this.media.addEventListener('loadedmetadata',ok,{once:true});this.media.addEventListener('error',bad,{once:true});});
   if(token!==this.epoch)return;
   this.media.currentTime=Math.max(0,s.start);await this.media.play();if(token!==this.epoch)return;
   this.phase='playing';this.emit();this.tick();
  }catch(e){if(token===this.epoch)this.fail();}
 }
 fail(){this.epoch++;this.clearTimers();this.media.pause();this.phase='error';this.onWord(-1);this.emit();}
 tick(){
  if(this.phase!=='playing')return;const s=this.segments[this.part];if(!s)return;
  const t=this.media.currentTime;const word=s.words.find(w=>t>=w.start&&t<w.end);
  const id=word?.id??-1;if(id!==this.lastWord){this.lastWord=id;this.onWord(id);}
  if(t>=s.end){this.advance();return;}
  this.frame=this.clock.requestAnimationFrame(()=>this.tick());
 }
 advance(){
  this.clearTimers();this.media.pause();this.onWord(-1);
  if(this.part+1>=this.segments.length){this.phase='ended';this.emit();return;}
  this.phase='gap';this.emit();const token=++this.epoch;
  this.timer=this.clock.setTimeout(()=>{if(token===this.epoch)this.load(this.part+1);},this.segments[this.part].gapMs);
 }
 pause(){if(!['playing','loading','gap'].includes(this.phase))return;const was=this.phase;this.epoch++;this.clearTimers();this.media.pause();this.phase=was==='gap'?'paused-gap':was==='loading'?'paused-loading':'paused';this.emit();}
 async resume(){
  if(this.phase==='paused-gap'){this.load(this.part+1);return;}
  if(this.phase==='paused-loading'){this.load(this.part);return;}
  if(this.phase!=='paused')return;const token=++this.epoch;
  try{await this.media.play();if(token!==this.epoch)return;this.phase='playing';this.emit();this.tick();}catch{if(token===this.epoch)this.fail();}
 }
 setRate(rate){if([.5,.75,1,1.25].includes(Number(rate))){this.rate=Number(rate);this.media.playbackRate=this.rate;}}
}
function install({document:doc=globalThis.document,records,glosses}){
 let serial=0,entries=[],enabled=true,frame=null;const win=doc.defaultView;
 const markWord=id=>{doc.querySelectorAll('.ra-speaking').forEach(n=>n.classList.remove('ra-speaking'));if(id>=0)doc.querySelectorAll(`[data-word="${id}"]`).forEach(n=>n.classList.add('ra-speaking'));};
 const player=new RecordedReader(records,{onWord:markWord,onState:p=>{
  doc.querySelectorAll('[data-reader]').forEach(bar=>{
   const active=bar===p.owner;const playing=active&&['playing','loading','gap'].includes(p.phase),paused=active&&p.phase.startsWith('paused');
   const play=bar.querySelector('[data-read-play]');play.textContent=playing?'❚❚ השהיה':paused?'▶ המשך':'▶ הקראה';play.setAttribute('aria-pressed',String(playing));
   const status=bar.querySelector('[data-read-status]');status.textContent=active?({loading:'טוען הקלטה…',playing:'הקלטה מוכנה מראש',gap:p.segments[p.part]?.pauseKind==='sentence'?'הפסקה בין משפטים…':'הפסקה בין חלקי המשפט…',paused:'מושהה','paused-gap':'מושהה','paused-loading':'מושהה',ended:'סיום הקטע',error:'לא ניתן לטעון את ההקלטה. לחצו לנסות שוב.'}[p.phase]||''):'';
  });
 }});
 function remove(entry){win.clearTimeout(entry.fadeTimer);win.clearTimeout(entry.removeTimer);entry.bubble.remove();if(entry.node.isConnected)entry.node.removeAttribute('aria-describedby');entries=entries.filter(e=>e!==entry);}
 function clear(){entries.slice().forEach(remove);doc.querySelectorAll('.ra-hovered').forEach(n=>n.classList.remove('ra-hovered'));}
 function fade(entry){if(entry.fading)return;entry.fading=true;entry.node.classList.remove('ra-hovered');entry.bubble.classList.add('ra-fading');entry.removeTimer=win.setTimeout(()=>remove(entry),1000);}
 function place(){
  frame=null;const placed=[];
  for(const e of entries.slice().reverse()){
   if(!e.node.isConnected){remove(e);continue;}
   const r=e.node.getBoundingClientRect();const clip=e.node.closest('.excerpt .reading-lines,dialog,main');const c=clip?.getBoundingClientRect();
   if(r.bottom<0||r.top>win.innerHeight||(c&&(r.bottom<c.top||r.top>c.bottom))){e.bubble.hidden=true;continue;}e.bubble.hidden=false;
   const b=e.bubble.getBoundingClientRect(),bounds=e.node.closest('dialog')?.getBoundingClientRect();
   const left=clamp(r.left+r.width/2-b.width/2,Math.max(8,bounds?.left+8||8),Math.min(win.innerWidth-8,bounds?.right-8||win.innerWidth-8)-b.width);
   let top=r.top-b.height-8;
   for(let tries=0;tries<6;tries++){
    const hit=placed.find(p=>left<p.right+4&&left+b.width>p.left-4&&top<p.bottom+3&&top+b.height>p.top-3);
    if(!hit)break;top=hit.top-b.height-5;
   }
   if(top<Math.max(8,bounds?.top+8||8)){if(!placed.length)top=Math.min(r.bottom+8,win.innerHeight-b.height-8);else{e.bubble.hidden=true;continue;}}
   e.bubble.style.left=left+'px';e.bubble.style.top=top+'px';placed.push({left,right:left+b.width,top,bottom:top+b.height});
  }
 }
 function schedulePlace(){if(frame===null)frame=win.requestAnimationFrame(place);}
 function show(node){
  if(!enabled||!node)return;const gloss=glosses[Number(node.dataset.gloss)];if(!gloss)return;
  let e=entries.find(x=>x.node===node);
  if(e){win.clearTimeout(e.fadeTimer);win.clearTimeout(e.removeTimer);e.fading=false;e.bubble.classList.remove('ra-fading');entries=entries.filter(x=>x!==e);entries.push(e);}
  else{
   const bubble=doc.createElement('div');bubble.className='ra-gloss-bubble';bubble.id='ra-gloss-'+(++serial);bubble.lang='he';bubble.dir='rtl';bubble.setAttribute('role','tooltip');bubble.textContent=gloss.he;
   (node.closest('dialog')||doc.body).append(bubble);node.setAttribute('aria-describedby',bubble.id);e={node,bubble,fading:false};entries.push(e);
  }
  doc.querySelectorAll('.ra-hovered').forEach(n=>n.classList.remove('ra-hovered'));node.classList.add('ra-hovered');
  // A bounded trail: up to three full bubbles and three fading predecessors.
  entries.slice(0,-3).forEach(fade);while(entries.length>6)remove(entries[0]);
  e.fadeTimer=win.setTimeout(()=>fade(e),3500);place();
 }
 function target(event){return event.target.closest?.('[data-gloss]');}
 doc.addEventListener('pointerover',e=>{if(e.pointerType==='touch')return;const n=target(e);if(n&&!n.contains(e.relatedTarget))show(n);});
 doc.addEventListener('focusin',e=>{const n=target(e);if(n)show(n);});
 doc.addEventListener('click',e=>{
  const node=target(e);if(node){show(node);return;}
  const button=e.target.closest?.('[data-read-play],[data-read-restart]');if(!button)return;
  const bar=button.closest('[data-reader]');
  if(button.hasAttribute('data-read-restart')){player.playRange(Number(bar.dataset.first),Number(bar.dataset.last),bar);return;}
  if(player.owner===bar&&['playing','loading','gap'].includes(player.phase))player.pause();
  else if(player.owner===bar&&player.phase.startsWith('paused'))player.resume();
  else player.playRange(Number(bar.dataset.first),Number(bar.dataset.last),bar);
 });
 doc.addEventListener('keydown',e=>{if(e.key==='Escape'){clear();return;}const n=target(e);if(n&&['Enter',' '].includes(e.key)){e.preventDefault();show(n);}});
 doc.addEventListener('change',e=>{if(e.target.matches('[data-read-speed]')){player.setRate(e.target.value);doc.querySelectorAll('[data-read-speed]').forEach(s=>s.value=String(player.rate));}if(e.target.matches('[data-gloss-toggle]')){enabled=e.target.checked;doc.querySelectorAll('[data-gloss-toggle]').forEach(s=>s.checked=enabled);if(!enabled)clear();}});
 doc.addEventListener('scroll',schedulePlace,true);win.addEventListener('resize',schedulePlace);
 doc.addEventListener('visibilitychange',()=>{if(doc.hidden){player.pause();clear();}});
 return {player,clear,reset(){player.stop();clear();},sync(){doc.querySelectorAll('[data-read-speed]').forEach(s=>s.value=String(player.rate));doc.querySelectorAll('[data-gloss-toggle]').forEach(s=>s.checked=enabled);},show};
}
const api={buildSegments,RecordedReader,install};
if(typeof module!=='undefined')module.exports=api;else root.TeacherInlineReader=api;
})(typeof window!=='undefined'?window:globalThis);
