/* Grade 8 bilingual reading standard adapted to existing prerecorded narration. */
(()=>{'use strict';
const cfg=window.READALONG8_CONFIG||{}, $=id=>document.getElementById(id), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const STANDARD=window.TEACHERS_READALONG_STANDARD||{pauseMs:1500,defaultSpeed:.75,speeds:[.25,.5,.75,1,1.25],speedStore:'teachers-read-alone-speed-v1'},rates=STANDARD.speeds,pauseMs=STANDARD.pauseMs;
const initialQuery=new URLSearchParams(location.search);
let story=[], sourcePages=[], audioMeta=null, audioUrl='', view=(initialQuery.get('view')==='sentences'||initialQuery.get('mode')==='sentences')?'sentences':'chunks';
let pages=[],page=0,reveal=false,playing=false,paused=false,queue=[],qpos=0,timer=0,raf=0,activeWord=-1,activeSentence=-1,wordTrail=[],auto=false,ignoreClick=0,tipNode=null;
let state={read:{},position:{}};try{const x=JSON.parse(localStorage.getItem(cfg.store)||'null');if(x&&typeof x==='object')state={...state,...x};}catch(_){}
if(!state.read||typeof state.read!=='object')state.read={};if(!state.position||typeof state.position!=='object')state.position={};
const save=()=>{try{localStorage.setItem(cfg.store,JSON.stringify(state));}catch(_){}};
let rate=STANDARD.defaultSpeed;try{const x=Number(localStorage.getItem(cfg.speedStore||STANDARD.speedStore));if(rates.includes(x))rate=x;}catch(_){}
const audio=new Audio();audio.preload='auto';audio.preservesPitch=true;document.body.append(audio);
function ui(){
 document.querySelectorAll('style,link[rel="stylesheet"]').forEach(n=>n.remove());
 const css=document.createElement('link');css.rel='stylesheet';css.href=cfg.css;document.head.append(css);
 document.body.className='grade8-bilingual';document.body.dataset.readingStandard='grade8-bilingual-v1';document.title='Read Along · '+cfg.title+' · '+cfg.grade;
 document.body.innerHTML=`<header class="toolbar"><a class="home" href="${cfg.home}" aria-label="חזרה">⌂</a><div class="brand">${cfg.grade}</div><button id="contents" aria-haspopup="dialog">תוכן</button><div class="audio-controls"><button id="play" disabled aria-pressed="false">טוען שמע…</button><button id="replay" disabled aria-label="הקראה מחדש" title="הקראה מחדש">↺</button><label for="speed">מהירות</label><select id="speed" dir="ltr"><option value=".25">0.25×</option><option value=".5">0.5×</option><option value=".75">0.75×</option><option value="1">1×</option><option value="1.25">1.25×</option></select></div></header>
 <main id="stage"><article class="sheet" id="sheet" role="tabpanel"><div class="meta"><nav id="reading-tabs" class="tabstrip" role="tablist"></nav><span id="step-label" class="step-label"></span></div><div class="text-slot english-slot"><p id="english" class="reading en" lang="en" dir="ltr"></p></div><div class="text-slot hebrew-slot" id="translation-slot" aria-hidden="true"><p id="hebrew" class="reading he" lang="he" dir="rtl"></p></div><p id="hint"></p></article></main><div id="gloss-layer" aria-hidden="true"></div>
 <footer class="footer" id="footer"><nav class="navigation"><button data-step="-1">←</button><button data-step="-1">↑</button><output id="counter"></output><button data-step="1">↓</button><button data-step="1">→</button></nav><p id="status" role="status">ההפסקות בשמע בלבד — 1.5 שניות.</p></footer><div class="progress"><div id="progress"></div></div>
 <dialog id="reading-menu"><div class="menu-heading"><h2>קריאה · ${cfg.title}</h2><button id="close-menu">×</button></div><nav class="menu-modes"><a href="?view=chunks" data-mode="chunks">קריאה בקטעים</a><a href="?view=sentences" data-mode="sentences">משפט בשקף</a><a href="${cfg.home}">מפגשי היחידה</a></nav><div class="jump-row"><button id="start-over">מההתחלה</button><button id="resume-reading">המשך הקריאה</button></div><p class="menu-note">אנגלית תחילה; בשקופית הבאה התרגום נשאר גלוי והמרקר עוקב בשתי השפות. ההקראה באנגלית בלבד.</p><div id="sentence-list"></div></dialog><div id="reading-tip" role="tooltip" hidden></div>`;
 $('speed').value=String(rate);
}
function normalizeGrade7(){
 story=LESSON.sentences.map((s,i)=>({number:i+1,paragraph:i<7?'A':'B',plain:s.en,he:s.he,words:s.words.map((w,j)=>({text:w.word.replace(/[.,!?;:“”"]+$/,''),he:w.he,start:audioMeta.sentences[i].words[j]?.start??audioMeta.sentences[i].start,end:audioMeta.sentences[i].words[j]?.end??audioMeta.sentences[i].end}))}));
 sourcePages=LESSON.texts.map(t=>t.ids.slice());
}
function normalizeGrade9(data){
 story=data.sentences.map((s,i)=>({number:s.id||i+1,paragraph:s.paragraph||String.fromCharCode(65+Math.min(25,Math.floor(i/10))),plain:s.en,he:s.he,image:s.image||null,imageAlt:s.imageAlt||'',imageCredit:s.imageCredit||'',words:s.words.map((w,j)=>({text:w.word,he:w.he,start:audioMeta?.sentences?.[i]?.words?.[j]?.start??w.start??0,end:audioMeta?.sentences?.[i]?.words?.[j]?.end??w.end??0}))}));
 sourcePages=Array.isArray(data.pages)&&data.pages.length?data.pages.map(x=>x.slice()):Array.from({length:Math.ceil(story.length/8)},(_,p)=>story.map((_,i)=>i).slice(p*8,p*8+8));
}
function englishHTML(i){const s=story[i], parts=s.plain.match(/\S+|\s+/g)||[];let wi=0;return parts.map(x=>{if(/\s+/.test(x))return x;const n=wi++,he=s.words[n]?.he||'';return `<span data-en="${i}:${n}" role="button" tabindex="0" aria-label="${esc((s.words[n]?.text||x)+': '+he)}">${esc(x)}</span>`;}).join('');}
function hebrewHTML(i){const toks=(story[i].he.match(/\S+|\s+/g)||[]);let hi=0;return toks.map(x=>/\s+/.test(x)?x:`<span data-he="${i}:${hi++}">${esc(x)}</span>`).join('');}
function setText(ids){
 $('english').innerHTML=ids.map(i=>`<span class="paragraph-line" data-sentence="${i}">${englishHTML(i)}</span>`).join(' ');
 $('hebrew').innerHTML=ids.map(i=>`<span class="paragraph-line" data-translation="${i}">${hebrewHTML(i)}</span>`).join(' ');
 const existing=$('reading-photo');if(existing)existing.remove();
 const item=story[ids[0]];
 if(ids.length===1&&item?.image){
   const figure=document.createElement('figure');figure.id='reading-photo';figure.className='reading-photo';
   figure.innerHTML=`<img src="${esc(item.image)}" alt="${esc(item.imageAlt||'')}" loading="eager" referrerpolicy="no-referrer"><figcaption>${esc(item.imageCredit||'')}</figcaption>`;
   $('sheet').append(figure);
 }else $('sheet').classList.remove('with-photo');
 $('sheet').classList.toggle('with-photo',!!(ids.length===1&&item?.image));
}
function fit(){for(const id of ['english','hebrew']){const e=$(id),slot=e.parentElement;e.style.fontSize='';let px=parseFloat(getComputedStyle(e).fontSize);while((e.scrollHeight>slot.clientHeight-5||e.scrollWidth>slot.clientWidth+1)&&px>17){px-=.5;e.style.fontSize=px+'px';}}}
function makePages(){
 pages=[];
 if(view==='sentences'){story.forEach((_,i)=>pages.push({ids:[i],source:sourcePages.findIndex(x=>x.includes(i)),sub:0}));return;}
 sourcePages.forEach((ids,source)=>{let group=[],sub=0;for(const i of ids){group.push(i);if(group.length>=3){pages.push({ids:group,source,sub:sub++});group=[];}}if(group.length)pages.push({ids:group,source,sub});});
}
function current(){return pages[page]||{ids:[0],source:0,sub:0};}
function refreshTabs(){const src=current().source;$('reading-tabs').innerHTML=sourcePages.map((ids,p)=>`<button role="tab" aria-selected="${p===src}" id="reading-tab-${p}" class="${state.read['page'+p]?'done':''}" data-source="${p}">${story[ids[0]]?.paragraph||''} · ${p+1}</button>`).join('');}
function syncURL(){const q=new URLSearchParams(location.search);q.set('view',view);q.delete('mode');if(view==='sentences'){q.set('p',String(page*2+Number(reveal)));q.delete('sub');q.delete('reveal');}else{q.set('p',String(current().source));q.set('sub',String(current().sub));q.set('reveal',String(Number(reveal)));}history.replaceState(null,'','?'+q);state.position[view]={sentence:current().ids[0],reveal};save();}
function clearMarker(){
 document.querySelectorAll('.marker').forEach(x=>x.classList.remove('marker'));
 activeWord=-1;activeSentence=-1;wordTrail=[];
 const layer=$('gloss-layer');if(layer)layer.innerHTML='';
}
function stop(reset=false){clearTimeout(timer);cancelAnimationFrame(raf);timer=0;raf=0;audio.pause();playing=false;if(reset){paused=false;queue=[];qpos=0;}clearMarker();$('play')&&($('play').textContent=paused?'▶ המשך':'▶ הקראה');$('play')?.setAttribute('aria-pressed','false');}
function mapHe(si,wi){const h=[...document.querySelectorAll(`[data-he^="${si}:"]`)];if(!h.length)return null;const n=Math.max(0,story[si].words.length-1),k=n?Math.round(wi/n*(h.length-1)):0;return h[k];}
function renderGlossTrail(){
 const layer=$('gloss-layer');if(!layer)return;
 layer.innerHTML='';
 if(!reveal||activeSentence<0||activeWord<0)return;
 const states=new Map();
 const completed=wordTrail.slice(-6),full=completed.slice(-3),fading=completed.slice(0,Math.max(0,completed.length-3));
 full.forEach(k=>states.set(k,'full'));
 if(fading.length>=1)states.set(fading.at(-1),'fade1');
 if(fading.length>=2)states.set(fading.at(-2),'fade2');
 if(fading.length>=3)states.set(fading.at(-3),'fade3');
 states.set(activeSentence+':'+activeWord,'full');
 for(const [key,cls] of states){
  const [si,wi]=key.split(':').map(Number),he=(story[si]?.words?.[wi]?.he||'').trim();
  if(!he)continue;
  const word=document.querySelector(`[data-en="${si}:${wi}"]`);if(!word)continue;
  const r=word.getBoundingClientRect(),g=document.createElement('div');
  g.className='trail-gloss '+cls;g.textContent=he;
  g.style.left=(r.left-sheetRect.left+r.width/2)+'px';
  g.style.top=(r.top-sheetRect.top-2)+'px';
  layer.appendChild(g);
 }
}
function paint(){
 if(!playing)return;const si=queue[qpos],s=story[si];if(!s)return;
 let wi=s.words.findIndex(w=>audio.currentTime>=w.start&&audio.currentTime<w.end);if(wi<0)wi=s.words.findLastIndex(w=>audio.currentTime>=w.start);
 if(wi!==activeWord||si!==activeSentence){
 if(activeSentence>=0&&activeWord>=0){wordTrail.push(activeSentence+':'+activeWord);if(wordTrail.length>6)wordTrail.shift();}
 document.querySelectorAll('.marker').forEach(x=>x.classList.remove('marker'));
 activeSentence=si;activeWord=wi;
 document.querySelector(`[data-en="${si}:${wi}"]`)?.classList.add('marker');
 if(reveal)mapHe(si,wi)?.classList.add('marker');
 renderGlossTrail();
}
 const total=queue.reduce((a,i)=>a+(story[i].words.at(-1)?.end-story[i].words[0]?.start||0),0),before=queue.slice(0,qpos).reduce((a,i)=>a+(story[i].words.at(-1)?.end-story[i].words[0]?.start||0),0),cur=Math.max(0,audio.currentTime-(s.words[0]?.start||0));$('progress').style.width=Math.min(100,(before+cur)/Math.max(.01,total)*100)+'%';
 const end=s.words.at(-1)?.end||0;if(audio.currentTime>=end-.01){audio.pause();clearMarker();if(qpos<queue.length-1){playing=false;$('footer').dataset.phase='gap';$('status').textContent='הפסקה של 1.5 שניות…';timer=setTimeout(()=>{qpos++;startQueue(false);},pauseMs);return;}playing=false;paused=false;$('play').textContent='▶ הקראה';$('play').setAttribute('aria-pressed','false');$('status').textContent='סוף '+(queue.length===1?'המשפט':'הקטע')+'. ממשיכים כשמוכנים.';queue.forEach(i=>state.read['sentence-'+i]=true);sourcePages.forEach((ids,p)=>{if(ids.every(i=>state.read['sentence-'+i]))state.read['page'+p]=true;});save();refreshTabs();return;}
 raf=requestAnimationFrame(paint);
}
async function startQueue(restart=true){clearTimeout(timer);const ids=current().ids;if(restart||!queue.length){queue=[...ids];qpos=0;}const si=queue[qpos],s=story[si],start=s.words[0]?.start??0;audio.playbackRate=rate;audio.preservesPitch=true;if(restart||audio.currentTime<start||audio.currentTime>=(s.words.at(-1)?.end??start))audio.currentTime=Math.max(0,start-.01);try{await audio.play();playing=true;paused=false;$('footer').dataset.phase='playing';$('play').textContent='❚❚ השהיה';$('play').setAttribute('aria-pressed','true');$('status').textContent=reveal?'המרקר עוקב באנגלית ובעברית.':'הקראה באנגלית.';paint();}catch(_){playing=false;$('status').textContent='לחצו על הקראה לניסיון נוסף.';}}
function play(restart=false){auto=true;if(playing){paused=true;audio.pause();playing=false;cancelAnimationFrame(raf);$('play').textContent='▶ המשך';$('play').setAttribute('aria-pressed','false');$('status').textContent='ההקראה מושהית — לחצו על המשך.';return;}if(restart){queue=[];qpos=0;}startQueue(!paused||restart);}
function show(n,r=false,{persist=true,schedule=true}={}){stop(true);page=Math.max(0,Math.min(pages.length-1,n));reveal=!!r;setText(current().ids);$('sheet').classList.toggle('with-translation',reveal);$('translation-slot').setAttribute('aria-hidden',String(!reveal));$('step-label').textContent=reveal?'אנגלית + עברית':'אנגלית';const nums=current().ids.map(i=>story[i].number);$('hint').textContent=(nums.length===1?'משפט '+nums[0]:'משפטים '+nums[0]+'–'+nums.at(-1))+' · '+(reveal?'התרגום נשאר גלוי לאורך כל ההקראה.':'בשקופית הבאה מתווסף התרגום.');$('counter').textContent=(page*2+Number(reveal)+1)+' / '+pages.length*2;document.querySelectorAll('[data-step]').forEach(b=>b.disabled=Number(b.dataset.step)<0?page===0&&!reveal:page===pages.length-1&&reveal);refreshTabs();fit();renderGlossTrail();if(persist)syncURL();$('status').textContent=reveal?'לחצו על הקראה לעקיבה בשתי השפות.':'ההפסקות בשמע בלבד — 1.5 שניות.';if(auto&&schedule)timer=setTimeout(()=>{if(!document.hidden&&!$('reading-menu').open)startQueue(true);},2000);}
function step(d){if($('reading-menu').open)return;const idx=page*2+Number(reveal),next=Math.max(0,Math.min(pages.length*2-1,idx+d));if(next!==idx)show(Math.floor(next/2),!!(next%2));}
function tip(n){if(!n)return;const [s,w]=n.dataset.en.split(':').map(Number),el=$('reading-tip');el.textContent=story[s].words[w]?.he||'';el.hidden=false;const r=n.getBoundingClientRect();el.style.left='10px';el.style.top='0';const h=el.offsetHeight,ww=el.offsetWidth;el.style.left=Math.max(10,Math.min(innerWidth-ww-10,r.x+r.width/2-ww/2))+'px';el.style.top=(r.bottom+h+8<innerHeight-75?r.bottom+7:Math.max(64,r.top-h-7))+'px';tipNode=n;}
function bind(){
 $('play').onclick=()=>play(false);$('replay').onclick=()=>play(true);$('speed').onchange=()=>{rate=Number($('speed').value);audio.playbackRate=rate;try{localStorage.setItem(cfg.speedStore||STANDARD.speedStore,String(rate));}catch(_){}};
 $('contents').onclick=()=>{stop(true);$('reading-menu').showModal();};$('close-menu').onclick=()=>$('reading-menu').close();$('reading-menu').querySelector('[data-mode="'+view+'"]').setAttribute('aria-current','page');
 $('sentence-list').innerHTML=story.map((s,i)=>`<button data-jump="${i}"><small>${s.paragraph} · ${s.number}</small>${esc(s.plain)}</button>`).join('');
 $('sentence-list').onclick=e=>{const b=e.target.closest('[data-jump]');if(b){$('reading-menu').close();show(pages.findIndex(p=>p.ids.includes(Number(b.dataset.jump))),false);}};
 $('start-over').onclick=()=>{$('reading-menu').close();show(0,false);};$('resume-reading').onclick=()=>{const p=state.position[view];$('reading-menu').close();if(p){const n=pages.findIndex(x=>x.ids.includes(p.sentence));show(Math.max(0,n),p.reveal);}else show(page,reveal);};
 $('reading-tabs').onclick=e=>{const b=e.target.closest('[data-source]');if(b)show(pages.findIndex(p=>p.source===Number(b.dataset.source)),false);};
 document.querySelectorAll('[data-step]').forEach(b=>b.onclick=()=>step(Number(b.dataset.step)));
 $('stage').addEventListener('click',e=>{if(performance.now()<ignoreClick)return;const n=e.target.closest('[data-en]');if(n)tip(n);else $('reading-tip').hidden=true;});
 $('stage').addEventListener('pointerover',e=>{if(e.pointerType==='mouse')tip(e.target.closest('[data-en]'));});$('stage').addEventListener('pointerout',e=>{if(e.pointerType==='mouse')$('reading-tip').hidden=true;});
 window.addEventListener('keydown',e=>{if($('reading-menu').open||e.altKey||e.ctrlKey||e.metaKey||e.target.closest('select,input,textarea'))return;if(e.key==='Escape'){stop(false);$('reading-tip').hidden=true;return;}if((e.key==='Enter'||e.key===' ')&&e.target.matches('[data-en]')){e.preventDefault();tip(e.target);return;}if(['ArrowDown','ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();step(1);}else if(['ArrowUp','ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();step(-1);}});
 let g=null;$('stage').addEventListener('pointerdown',e=>{if((e.pointerType==='mouse'&&e.button!==0)||e.target.closest('button,a,select'))return;g={id:e.pointerId,x:e.clientX,y:e.clientY,t:performance.now()};});
 $('stage').addEventListener('pointerup',e=>{if(!g||g.id!==e.pointerId)return;const dx=e.clientX-g.x,dy=e.clientY-g.y;if(Math.max(Math.abs(dx),Math.abs(dy))>=44&&performance.now()-g.t<1800){ignoreClick=performance.now()+500;step((Math.abs(dx)>Math.abs(dy)?dx:dy)<0?1:-1);}g=null;});
 window.addEventListener('pagehide',()=>stop(true));document.addEventListener('visibilitychange',()=>{if(document.hidden)stop(true);});window.addEventListener('blur',()=>{if(document.hidden)stop(true);});window.addEventListener('resize',()=>{clearTimeout(timer);fit();renderGlossTrail();});
}
async function init(){
 ui();let data=null;
 if(cfg.kind==='grade7'){audioMeta=await fetch('audio.json?v=20261005-g8standard1').then(r=>r.json());normalizeGrade7();}
 else{const assetVersion=encodeURIComponent(cfg.assetVersion||'20261005-g8standard1');[data,audioMeta]=await Promise.all(['content.json','audio.json'].map(async x=>{const r=await fetch(x+'?v='+assetVersion,{cache:'no-store'});if(!r.ok)throw new Error(x+' HTTP '+r.status);return r.json();}));normalizeGrade9(data);}
 audioUrl=new URL(audioMeta.audio,location.href).href;audio.src=audioUrl;audio.playbackRate=rate;makePages();bind();$('play').disabled=false;$('replay').disabled=false;$('play').textContent='▶ הקראה';
 const qs=new URLSearchParams(location.search),old=Math.max(0,Number(qs.get('p'))||0),sub=Math.max(0,Number(qs.get('sub'))||0);let start=0,r=false;
 if(view==='sentences'){start=Math.floor(old/2);r=!!(old%2);}else{start=pages.findIndex(p=>p.source===Math.min(old,sourcePages.length-1)&&p.sub===sub);r=qs.get('reveal')==='1';}
 show(Math.max(0,start),r,{persist:false,schedule:false});
 if(cfg.autoStart){
   const delayMs=Number.isFinite(Number(cfg.autoStartDelayMs))?Number(cfg.autoStartDelayMs):2000;
   timer=setTimeout(async()=>{
     if(document.hidden||$('reading-menu')?.open)return;
     try{await startQueue(true);}
     catch(_){$('status').textContent='לחצו על ▶ הקראה להפעלת האודיו.';}
   },Math.max(0,delayMs));
 }
}
init().catch(e=>{console.error(e);document.body.innerHTML='<main style="padding:25px;font:20px Arial;direction:rtl"><h1>לא ניתן לטעון את הקריאה כרגע.</h1><p>רעננו את העמוד.</p></main>';});
})();