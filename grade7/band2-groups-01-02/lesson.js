/* Complete Teachers lesson. Only site-hosted prerecorded MP3 narration. */
(async()=>{
'use strict';
const $=id=>document.getElementById(id),stage=$('stage'),dialog=$('contents');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let entries=[],slides=[],index=0,breakReveal=false,audioEnabled=false,manifest=null,timer=0,token=0,lastEntry='',wordNode=null;
const player=new Audio();player.preload='auto';
const getJSON=async(url)=>{const r=await fetch(url);if(!r.ok)throw Error('HTTP '+r.status);return r.json()};
function stopAudio(){clearTimeout(timer);token++;player.pause();try{player.currentTime=0}catch(_){}$('audioStatus').textContent=''}
function audioForCurrent(){const s=slides[index];return s?.type==='word'&&!s.reveal&&manifest?.clips?.[s.entry.id]}
function updateAudioUI(){const has=!!audioForCurrent();$('replay').disabled=!has;$('audioToggle').disabled=!manifest;$('audioToggle').textContent=manifest?(audioEnabled?'אודיו פועל':'הפעל אודיו'):'אודיו לא זמין';$('audioToggle').setAttribute('aria-pressed',String(audioEnabled));}
function playCurrent(delay=0){stopAudio();const clip=audioForCurrent();if(!clip)return;const runToken=token;timer=setTimeout(async()=>{if(runToken!==token)return;try{player.src=new URL(clip.src,location.href).href;await player.play();if(runToken===token)$('audioStatus').textContent='קריינות AI · המילה והמשפט'}catch(err){if(runToken===token&&err.name!=='AbortError')$('audioStatus').textContent='לחצו ▶ להשמעה'}},delay)}
player.addEventListener('ended',()=>{$('audioStatus').textContent=''});
function fit(){stage.querySelectorAll('[data-fit]').forEach(el=>{el.style.fontSize='';let size=parseFloat(getComputedStyle(el).fontSize),min=stage.clientHeight<330?13:17;for(let j=0;j<45&&(el.scrollHeight>el.clientHeight+1||el.scrollWidth>el.clientWidth+1)&&size>min;j++){size-=1;el.style.fontSize=size+'px'}})}
function tense(text){if(/\b(will)\b/i.test(text))return'עתיד';if(/\b(was|were|went|walked|won|called|saw|fell|listened|stayed|worked|had|took|brought|broke|felt)\b/i.test(text))return'עבר';if(/\b(is|are|am|needs|moves|spreads|buy|walk|study|has|can|feel|meet)\b/i.test(text))return'הווה';return''}
function originalWord(e){return `<section class="page word-page"><div class="frame word-frame" data-entry="${esc(e.id)}"><div class="meta"><p class="eyebrow">BAND II · CORE I · GROUP ${String(e.group).padStart(2,'0')} · ${e.number}/55</p><span class="part">${tense(e.sentence)}</span></div><h1 class="word-line" data-fit lang="en"><span>${esc(e.word)}</span></h1><p class="meaning-line" data-fit lang="he" dir="rtl" aria-hidden="true">${esc(e.meaning)}</p><p class="sentence-line" data-fit lang="en"><span>${esc(e.sentence)}</span></p><p class="translation-line" data-fit lang="he" dir="rtl" aria-hidden="true">${esc(e.translation)}</p></div></section>`}
function render(s){
 if(s.type==='word'){
  if(lastEntry!==s.entry.id||!wordNode){stage.innerHTML=originalWord(s.entry);wordNode=stage.querySelector('.word-frame');lastEntry=s.entry.id}
  wordNode.classList.toggle('show-translation',s.reveal);wordNode.querySelectorAll('.meaning-line,.translation-line').forEach(x=>x.setAttribute('aria-hidden',String(!s.reveal)));
 }else{
  wordNode=null;lastEntry='';
  if(s.type==='cover')stage.innerHTML=`<section class="page cover"><div class="frame"><p class="eyebrow">TEACHERS · כיתה ז׳2</p><h1 lang="en" dir="ltr">Band II · Core I<br>Groups 01–02</h1><div class="accent-rule"></div><p class="he-title">ברוכים הבאים</p><p class="scope">שתי קבוצות מלאות · 110 ערכים<br>אנגלית תחילה, תרגום בשקף הבא.</p><button class="primary" id="begin">מתחילים</button><span class="cover-number" aria-hidden="true">01<br>02</span></div></section>`;
  else if(s.type==='goals')stage.innerHTML=`<section class="page goals"><div class="frame"><p class="eyebrow">סדר העבודה</p><h1>מילה, משפט, תרגום</h1><div class="goal-grid"><article><b>1</b><p>קוראים מילה ומשפט באנגלית.</p></article><article><b>2</b><p>מנסים להבין, ואז חושפים תרגום.</p></article><article><b>3</b><p>אחרי שלושה ערכים עוצרים להתנחתא חזותית.</p></article></div><p class="help">שני שקפים לכל ערך. האנגלית אינה זזה בזמן החשיפה.<br>החלקה שמאלה או למעלה: קדימה. ימינה או למטה: אחורה.<br>אפשר לעצור ולחזור לאותה נקודה דרך תפריט התוכן.</p></div></section>`;
  else if(s.type==='break'){
   const v=BreakVisuals.get(s.number);stage.innerHTML=`<section class="page break-page"><div class="break-frame"><div class="art">${v.art}</div><span class="break-tag">התנחתא ${s.number+1}</span><h1 class="break-title" lang="en">${esc(v.title)}</h1><span class="art-note">${esc(v.note)}</span>${v.puzzle?`<button class="break-control" id="inspect" aria-pressed="false">${esc(v.button)}</button>`:''}<div class="break-caption"><p class="break-en" data-fit lang="en">${esc(v.english)}</p><p class="break-he" data-fit lang="he" aria-hidden="true">${esc(v.hebrew)}</p></div></div></section>`;
   if($('inspect'))$('inspect').onclick=()=>{const f=stage.querySelector('.break-frame'),on=f.classList.toggle('inspect');$('inspect').setAttribute('aria-pressed',String(on))};
  }else stage.innerHTML=`<section class="page end"><div class="frame"><p class="eyebrow">סיום שתי הקבוצות</p><h1>חוזרים למילים שעדיין צריכות תרגול</h1><p class="scope">עברנו על 110 ערכים. בתפריט התוכן אפשר לבחור כל מילה ולחזור אל המשפט שלה.<br>לקראת המבחן: פירוש המילים ותרגום משפטים מעברית לאנגלית.</p><div class="end-links"><a href="https://englishfornoar.co.il/band-ii/groups/group-01.html" target="_blank" rel="noopener">תרגול קבוצה 01 באתר</a><a href="https://englishfornoar.co.il/band-ii/groups/group-02.html" target="_blank" rel="noopener">תרגול קבוצה 02 באתר</a></div></div></section>`;
 }
 $('begin')?.addEventListener('click',()=>navigate(1),{once:true});
}
function setBreakReveal(value){breakReveal=value;const frame=stage.querySelector('.break-frame');frame?.classList.toggle('break-revealed',value);frame?.querySelector('.break-he')?.setAttribute('aria-hidden',String(!value));$('stepHint').textContent=value?'קדימה: הערך הבא':'קדימה: חשיפת התרגום';}
function show(n,save=true){
 stopAudio();index=Math.max(0,Math.min(slides.length-1,n));breakReveal=false;const s=slides[index];render(s);
 $('counter').textContent=`${index+1} / ${slides.length}`;$('progressFill').style.width=((index+1)/slides.length*100)+'%';
 $('stepHint').textContent=s.type==='word'?(s.reveal?'התרגום נחשף; האנגלית נשארת במקום':'קדימה: חשיפת התרגום'):'החליקו שמאלה או למעלה כדי להתקדם';
 if(s.type==='break')setBreakReveal(false);
 document.querySelectorAll('[data-nav]').forEach(b=>b.disabled=Number(b.dataset.nav)<0?index===0:index===slides.length-1);
 if(save){try{localStorage.setItem('teachers-grade7-groups-01-02-v1',String(index))}catch(_){}history.replaceState(null,'','#slide-'+(index+1))}
 fit();updateAudioUI();if(audioEnabled&&audioForCurrent())playCurrent(2000);
}
function navigate(delta){if(dialog.open)return;if(slides[index]?.type==='break'){if(delta>0&&!breakReveal){setBreakReveal(true);return}if(delta<0&&breakReveal){setBreakReveal(false);return}}show(index+delta)}
document.querySelectorAll('[data-nav]').forEach(b=>b.onclick=()=>navigate(Number(b.dataset.nav)));
$('audioToggle').onclick=()=>{audioEnabled=!audioEnabled;updateAudioUI();if(audioEnabled)playCurrent(0);else stopAudio()};$('replay').onclick=()=>playCurrent(0);
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(_){}};
$('menuButton').onclick=()=>{stopAudio();dialog.showModal();$('search').focus()};$('closeMenu').onclick=()=>dialog.close();
function jump(entryIndex){dialog.close();show(slides.findIndex(s=>s.type==='word'&&!s.reveal&&s.entry===entries[entryIndex]))}
$('reset').onclick=()=>{dialog.close();show(0)};document.querySelectorAll('[data-group]').forEach(b=>b.onclick=()=>jump(entries.findIndex(e=>e.group===Number(b.dataset.group))));
function listWords(){let term=$('search').value.toLowerCase().trim();$('wordList').innerHTML=entries.map((e,n)=>({e,n})).filter(({e})=>(e.word+' '+e.meaning).toLowerCase().includes(term)).map(({e,n})=>`<button data-entry-index="${n}"><small>${e.group}.${String(e.number).padStart(2,'0')}</small>${esc(e.word)}</button>`).join('');}
$('search').oninput=listWords;$('wordList').onclick=e=>{let b=e.target.closest('[data-entry-index]');if(b)jump(Number(b.dataset.entryIndex))};
window.addEventListener('keydown',e=>{if(dialog.open||e.target.closest('input,textarea,select,[contenteditable]'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();navigate(1)}else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();navigate(-1)}else if(e.key==='Home'){e.preventDefault();show(0)}else if(e.key==='End'){e.preventDefault();show(slides.length-1)}else if(e.key.toLowerCase()==='r')playCurrent(0)});
// One deliberate single-finger gesture moves one step. A pinch never advances slides.
let gesture=null,pointers=new Set();const interactive=t=>t.closest('button,a,input,select,textarea,[contenteditable]');
function beginPointer(e){pointers.add(e.pointerId);if(pointers.size>1){gesture=null;return}if(interactive(e.target)||e.pointerType==='mouse'&&e.button!==0)return;gesture={id:e.pointerId,x:e.clientX,y:e.clientY,time:performance.now()};try{stage.setPointerCapture(e.pointerId)}catch(_){}}
function endPointer(e){const g=gesture;pointers.delete(e.pointerId);gesture=null;if(!g||g.id!==e.pointerId||pointers.size)return;const dx=e.clientX-g.x,dy=e.clientY-g.y;if(Math.max(Math.abs(dx),Math.abs(dy))<42||performance.now()-g.time>1800)return;navigate((Math.abs(dx)>Math.abs(dy)?dx:dy)<0?1:-1)}
if('PointerEvent'in window){stage.addEventListener('pointerdown',beginPointer);stage.addEventListener('pointerup',endPointer);stage.addEventListener('pointercancel',e=>{gesture=null;pointers.delete(e.pointerId)});}else{stage.addEventListener('touchstart',e=>{if(e.touches.length!==1||interactive(e.target)){gesture=null;return}const t=e.touches[0];gesture={x:t.clientX,y:t.clientY,time:performance.now()}},{passive:true});stage.addEventListener('touchmove',e=>{if(e.touches.length!==1){gesture=null;return}if(gesture)e.preventDefault()},{passive:false});stage.addEventListener('touchend',e=>{let g=gesture;gesture=null;if(!g||e.touches.length)return;let t=e.changedTouches[0],dx=t.clientX-g.x,dy=t.clientY-g.y;if(Math.max(Math.abs(dx),Math.abs(dy))>=42&&performance.now()-g.time<1800)navigate((Math.abs(dx)>Math.abs(dy)?dx:dy)<0?1:-1)},{passive:true});stage.addEventListener('touchcancel',()=>gesture=null,{passive:true})}
let wheelSum=0,wheelTime=0,lockUntil=0;stage.addEventListener('wheel',e=>{if(e.ctrlKey||dialog.open)return;e.preventDefault();const now=performance.now();if(now<lockUntil)return;if(now-wheelTime>160)wheelSum=0;wheelTime=now;let d=Math.abs(e.deltaY)>Math.abs(e.deltaX)?e.deltaY:e.deltaX;wheelSum+=d*(e.deltaMode===1?16:e.deltaMode===2?400:1);if(Math.abs(wheelSum)>55){navigate(wheelSum>0?1:-1);wheelSum=0;lockUntil=now+450}},{passive:false});
window.addEventListener('resize',fit);window.addEventListener('pagehide',stopAudio);window.addEventListener('blur',stopAudio);document.addEventListener('visibilitychange',()=>{if(document.hidden)stopAudio()});document.addEventListener('click',e=>{if(e.target.closest('a'))stopAudio()});
try{
 entries=await getJSON('entries.json?v=20260916-full1');if(entries.length!==110||entries.filter(e=>e.group===1).length!==55||entries.filter(e=>e.group===2).length!==55)throw Error('Unexpected vocabulary snapshot');
 slides=[{type:'cover'},{type:'goals'}];let count=0;entries.forEach((entry,n)=>{slides.push({type:'word',entry,reveal:false},{type:'word',entry,reveal:true});if((n+1)%3===0)slides.push({type:'break',number:count++})});slides.push({type:'end'});
 listWords();let initial=Number(location.hash.match(/^#slide-(\d+)$/)?.[1]||1)-1;show(initial,false);document.fonts?.ready.then(fit);
 getJSON('audio-manifest.json?v=20260916-full1').then(m=>{if(m.count!==110||!entries.every(e=>m.clips?.[e.id]?.src))throw Error('Incomplete audio');manifest=m;updateAudioUI()}).catch(()=>{manifest=null;updateAudioUI()});
 window.__lessonTest={get entries(){return entries},get slides(){return slides},get index(){return index},show,navigate,get breakReveal(){return breakReveal},get audio(){return{ready:!!manifest,enabled:audioEnabled,paused:player.paused,src:player.src}}};
}catch(err){stage.innerHTML='<div class="loading"><h1>המצגת לא נטענה</h1><p>יש לרענן את העמוד ולבדוק את החיבור.</p><button onclick="location.reload()">ניסיון נוסף</button></div>';console.error(err)}
})();
