/* Paired pages share their original DOM: revealing Hebrew cannot move the English. */
(() => {
'use strict';
const $=id=>document.getElementById(id),stage=$('stage'),storageKey='teachers-grade7-band2-01-02-neutral-v1';
const accents=['#53e4ff','#ffad52','#df8dff','#65edbd','#ff81b3','#e4ed65'];
let pages=[],words=[],index=0,activeKey='',manifest={},soundOn=false,audioTimer=null,playToken=0,gesture=null,wheelTotal=0,lastWheel=0;
const player=new Audio();player.preload='auto';
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function highlight(text,word){const parts=word.replace(/[.!?]/g,'').split(/\s+/).filter(p=>p.length>2&&!/^(something|someone|somebody|one|your|the|with)$/i.test(p));let out=escape(text);for(const p of [...new Set(parts)].sort((a,b)=>b.length-a.length)){const r=new RegExp(`\\b(${p.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})\\b`,'gi');out=out.replace(r,'<mark>$1</mark>');}return out;}
function pair(item){pages.push({...item,reveal:false},{...item,reveal:true});}
function build(){
 pair({kind:'cover',key:'cover',meta:'GRADE 7 · BAND II · CORE I',title:'Groups <em>01–02</em>',en:'New words. Clear examples. One step at a time.',he:'מילים חדשות, דוגמאות ברורות — שלב אחרי שלב.'});
 pair({kind:'goals',key:'goals',meta:'איך עובדים?',title:'Read · Think · Use',en:'Read the word and its example. Guess the meaning before the next slide.',he:'קראו את המילה ואת הדוגמה. נסו להבין את המשמעות לפני המעבר לשקף הבא.'});
 let breaks=0;
 for(const group of [1,2]){
 pair({kind:'section',key:`group-${group}`,meta:`GROUP ${String(group).padStart(2,'0')} · 55 ENTRIES`,title:`Group <em>${String(group).padStart(2,'0')}</em>`,en:'Three words, then a short visual break.',he:'שלושה ערכים, ואז התנחתא חזותית קצרה.'});
 const groupWords=words.filter(w=>w.group===group);
 groupWords.forEach((w,j)=>{
 w.page=pages.length;
 pair({kind:'word',key:w.id,word:w,accent:accents[j%accents.length]});
 if((j+1)%3===0)pair({kind:'brain',key:`break-${breaks}`,scene:TeachersScenes.get(breaks),number:++breaks});
 });
 }
 pair({kind:'goals',key:'finish',meta:'סיכום',title:'Use the words',en:'Choose three words. Say one sentence with each word.',he:'בחרו שלוש מילים. אמרו משפט אחד עם כל מילה.'});
 const opts=words.map(w=>`<option value="${w.page}">קבוצה ${String(w.group).padStart(2,'0')} · ${escape(w.en)}</option>`).join('');$('wordSelect').innerHTML=opts;
}
function html(s){
 if(s.kind==='word'){
 const w=s.word;return `<article class="sheet word-slide" style="--accent:${s.accent}" data-key="${s.key}"><div class="ribbon"></div><div class="meta"><span>GROUP ${String(w.group).padStart(2,'0')} · ${w.position} / 55</span><span class="pos">${escape(w.pos)}</span></div><h1 class="headword ${w.en.length>18?'long':''}">${escape(w.en)}</h1><div class="source"><p>${highlight(w.ex_en,w.en)}</p></div><div class="translation" aria-hidden="true"><p class="meaning">${escape(w.mean_he)}</p><p class="he-example">${escape(w.ex_he)}</p></div><div class="entry-number" aria-hidden="true">${String(w.position).padStart(2,'0')}</div><div class="stage-note">קראו, נסו להבין, ואז עברו לשקף הבא.</div></article>`;
 }
 if(s.kind==='brain'){
 const x=s.scene;return `<article class="sheet brain ${['circles','colors','lines','parallel','triangles','stars'].includes(x.kind)?'diagram':''}" data-key="${s.key}"><div class="scene">${x.svg}</div><div class="meta"><span>BRAIN BREAK · ${s.number} / 36</span><span>30–45 שניות</span></div><div class="title-tag">${escape(x.title)}</div><div class="source"><p>${escape(x.en)}</p></div><div class="translation" aria-hidden="true"><p>${escape(x.he)}</p>${x.answer?`<p class="solution">${escape(x.answer)}</p><p>${escape(x.answerHe)}</p>`:''}</div><div class="source-label">${x.source?`<a href="${x.source}" target="_blank" rel="noopener">מקור העובדה</a> · `:''}איור מקורי · ללא צילום של מקום מסוים</div></article>`;
 }
 return `<article class="sheet ${s.kind}" data-key="${s.key}"><div class="ribbon"></div><div class="decor" aria-hidden="true"></div><div class="meta"><span>${escape(s.meta)}</span><span>110 ערכים · 2 קבוצות</span></div><h1 class="headword">${s.title}</h1><div class="source"><p>${escape(s.en)}</p></div><div class="translation" aria-hidden="true"><p class="he-example">${escape(s.he)}</p></div><div class="stage-note">חצים / גלילה / סווייפ: שמאלה או למעלה — קדימה; ימינה או למטה — אחורה.</div></article>`;
}
function stop(){clearTimeout(audioTimer);playToken++;player.pause();try{player.currentTime=0;}catch(_){}}
function available(s){return s&&s.kind==='word'&&manifest[s.word.id];}
function sound(s,immediate=false){stop();if(!soundOn||!available(s)||s.reveal)return;const token=playToken;const run=()=>{if(token!==playToken||document.hidden)return;player.src=manifest[s.word.id];player.play().then(()=>{$('audioStatus').textContent='';}).catch(()=>{$('audioStatus').textContent='לחצו ↻ להשמעה במכשיר הזה.';});};if(immediate)run();else audioTimer=setTimeout(run,2000);}
function fit(){for(const box of stage.querySelectorAll('.headword,.source p,.translation p')){box.style.removeProperty('font-size');const parent=box.classList.contains('headword')?box:box.parentElement;let px=parseFloat(getComputedStyle(box).fontSize);let tries=0;while((box.scrollWidth>box.clientWidth+1||parent.scrollHeight>parent.clientHeight+1)&&px>13&&tries++<35){px-=1;box.style.fontSize=px+'px';}}}
function show(n,save=true){
 index=Math.max(0,Math.min(pages.length-1,Number(n)||0));const s=pages[index];
 if(activeKey!==s.key){stage.innerHTML=html(s);activeKey=s.key;fit();}
 const sheet=stage.querySelector('.sheet');sheet.classList.toggle('revealed',s.reveal);const translation=sheet.querySelector('.translation');translation.setAttribute('aria-hidden',String(!s.reveal));
 stage.setAttribute('aria-label',`שקף ${index+1} מתוך ${pages.length}`);$('counter').textContent=`${index+1} / ${pages.length}`;$('progressFill').style.width=`${100*(index+1)/pages.length}%`;
 $('prev').disabled=index===0;$('next').disabled=index===pages.length-1;$('replayBtn').disabled=!available(s);
 if(save)try{localStorage.setItem(storageKey,String(index));history.replaceState(null,'',`#slide-${index+1}`);}catch(_){}
 sound(s);if(s.kind==='word')$('wordSelect').value=String(s.word.page);
}
function move(step){show(index+step);}
function close(){ $('toc').close();stage.focus({preventScroll:true});}
$('prev').onclick=()=>move(-1);$('next').onclick=()=>move(1);
$('menuBtn').onclick=()=>{stop();$('toc').showModal();};$('closeMenu').onclick=close;
$('restart').onclick=()=>{close();show(0);};$('group1').onclick=()=>{close();show(pages.findIndex(p=>p.key==='group-1'));};$('group2').onclick=()=>{close();show(pages.findIndex(p=>p.key==='group-2'));};$('jumpWord').onclick=()=>{const n=$('wordSelect').value;close();show(n);};
$('fullBtn').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch(_){$('audioStatus').textContent='אפשר לסובב את המכשיר לתצוגה רחבה.';}};
$('audioBtn').onclick=()=>{soundOn=!soundOn;$('audioBtn').setAttribute('aria-pressed',String(soundOn));$('audioBtn').textContent=soundOn?'שמע פועל':'שמע כבוי';if(soundOn)sound({...pages[index],reveal:false},true);else stop();};
$('replayBtn').onclick=()=>{soundOn=true;$('audioBtn').setAttribute('aria-pressed','true');$('audioBtn').textContent='שמע פועל';sound({...pages[index],reveal:false},true);};
window.addEventListener('keydown',e=>{if($('toc').open||e.altKey||e.ctrlKey||e.metaKey)return;const t=e.target;if(t.matches('input,textarea,select'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();move(1);}else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();move(-1);}else if(e.key==='Home'){e.preventDefault();show(0);}else if(e.key==='End'){e.preventDefault();show(pages.length-1);}else if(e.key.toLowerCase()==='r'&&!$('replayBtn').disabled)$('replayBtn').click();});
/* One touch gesture produces one step, in either axis; pinch zoom stays available. */
if('PointerEvent'in window){
 stage.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'||e.target.closest('a,button,select'))return;if(!e.isPrimary){gesture=null;return;}gesture={id:e.pointerId,x:e.clientX,y:e.clientY};try{stage.setPointerCapture(e.pointerId);}catch(_){}});
 stage.addEventListener('pointerup',e=>{if(!gesture||gesture.id!==e.pointerId)return;const dx=e.clientX-gesture.x,dy=e.clientY-gesture.y;gesture=null;if(Math.max(Math.abs(dx),Math.abs(dy))<45)return;move((Math.abs(dx)>Math.abs(dy)?dx:dy)<0?1:-1);});
 stage.addEventListener('pointercancel',()=>gesture=null);
}else{
 stage.addEventListener('touchstart',e=>{gesture=e.touches.length===1?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null;},{passive:true});
 stage.addEventListener('touchmove',e=>{if(gesture&&e.touches.length===1)e.preventDefault();},{passive:false});
 stage.addEventListener('touchend',e=>{if(!gesture||!e.changedTouches.length)return;const dx=e.changedTouches[0].clientX-gesture.x,dy=e.changedTouches[0].clientY-gesture.y;gesture=null;if(Math.max(Math.abs(dx),Math.abs(dy))>=45)move((Math.abs(dx)>Math.abs(dy)?dx:dy)<0?1:-1);},{passive:true});
 stage.addEventListener('touchcancel',()=>gesture=null);
}
stage.addEventListener('wheel',e=>{if(e.ctrlKey||e.metaKey)return;e.preventDefault();const now=performance.now();if(now-lastWheel<420)return;wheelTotal+=Math.abs(e.deltaY)>=Math.abs(e.deltaX)?e.deltaY:e.deltaX;if(Math.abs(wheelTotal)>45){move(wheelTotal>0?1:-1);wheelTotal=0;lastWheel=now;}},{passive:false});
window.addEventListener('resize',()=>{gesture=null;fit();});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);
async function load(){
 try{
 const r=await fetch('words.json?v=20260916-neutral1');if(!r.ok)throw new Error('word-data-unavailable');const data=await r.json();words=data.words;
 if(!Array.isArray(words)||words.length!==110||words.some(w=>!w.en||!w.ex_en||!w.ex_he||!w.mean_he))throw new Error('word-data-invalid');
 build();let saved=0;try{saved=Number(localStorage.getItem(storageKey))||0;}catch(_){}const hash=location.hash.match(/^#slide-(\d+)$/);show(hash?Number(hash[1])-1:saved,false);if(document.fonts)document.fonts.ready.then(fit);
 try{const a=await fetch('audio/manifest.json?v=20260916-neutral1');if(a.ok){const m=await a.json();manifest=m.files||{};}}catch(_){}
 $('audioBtn').disabled=Object.keys(manifest).length===0;$('replayBtn').disabled=!available(pages[index]);if(!Object.keys(manifest).length)$('audioStatus').textContent='הקלטות MP3 אינן זמינות כרגע; המצגת פועלת ללא קריינות.';
 }catch(error){stage.innerHTML='<div class="loading" role="alert">לא ניתן לטעון את קבוצות המילים כרגע.<button id="retry">נסו שוב</button></div>';$('retry').onclick=load;console.error(error);}
}
load();
})();
