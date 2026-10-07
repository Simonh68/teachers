/* Approved Grade 8 reading standard. Text, punctuation and timing are source data. */
'use strict';
window.initGrade8Bilingual=async({D,base,view,store,speedStore,deck=null})=>{
const $=id=>document.getElementById(id),stage=$('stage'),sheet=$('sheet'),deckSheet=$('deck-sheet'),menu=$('reading-menu');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const A=window.GRADE8_ALIGNMENT,records=JSON.parse(JSON.stringify(window.GRADE8_PHRASES.sentences));
if(D.story.length!==records.length||D.story.length!==Object.keys(A).length)throw Error('Incomplete reading coverage');
records.forEach(r=>r.parts.forEach(p=>p.src=new URL(p.src,base).href));
let state={read:{},last:null};try{const s=JSON.parse(localStorage.getItem(store)||'null');if(s&&typeof s==='object')state={...state,...s};}catch(_){}
if(!state.read||typeof state.read!=='object')state.read={};
const save=()=>{try{localStorage.setItem(store,JSON.stringify(state));}catch(_){}};
const STANDARD=window.TEACHERS_READALONG_STANDARD||{pauseMs:1500,defaultSpeed:.75,speeds:[.25,.5,.75,1,1.25],speedStore:'teachers-read-alone-speed-v1'};let rate=STANDARD.defaultSpeed;try{const x=Number(localStorage.getItem(speedStore||STANDARD.speedStore));if(STANDARD.speeds.includes(x))rate=x;}catch(_){}
$('speed').value=String(rate);
let pages=[],page=0,reveal=false,breakIndex=-1,pairKey='',auto=false,scheduled=null,narrator=null,lastEn=null,lastHe=null,lastStatus='',ready=false,resizeTimer=null;
let enNodes={},heNodes={},savedLocation=state.bilingualPosition?.[view]||null;
function status(t){if(t!==lastStatus){lastStatus=t;$('status').textContent=t;}}
function clearMarker(){lastEn?.classList.remove('marker');lastHe?.classList.remove('marker');lastEn=null;lastHe=null;}
function hideTip(){$('reading-tip').hidden=true;}
function stop(){clearTimeout(scheduled);scheduled=null;narrator?.stop();clearMarker();hideTip();}
const enHTML=[],heHTML=[];
for(let i=0;i<D.story.length;i++){
 const s=D.story[i],a=A[s.number];
 if(!a||a.plain!==s.plain||a.he!==s.he||a.map.length!==s.tokens.length)throw Error('Source changed: alignment review required, sentence '+s.number);
 let cursor=0,h='';s.tokens.forEach((t,j)=>{h+=esc(s.plain.slice(cursor,t.startChar))+`<span data-en="${i}:${j}" role="button" tabindex="0" aria-label="${esc(t.text+': '+t.he)}">${esc(s.plain.slice(t.startChar,t.endChar))}</span>`;cursor=t.endChar;});h+=esc(s.plain.slice(cursor));enHTML[i]=`<span class="paragraph-line" data-sentence="${i}">${h}</span>`;
 cursor=0;h='';a.units.forEach((u,j)=>{h+=esc(s.he.slice(cursor,u.start))+`<span data-he="${i}:${j}">${esc(s.he.slice(u.start,u.end))}</span>`;cursor=u.end;});h+=esc(s.he.slice(cursor));heHTML[i]=`<span class="paragraph-line" data-translation="${i}">${h}</span>`;
}
function setText(ids){$('english').innerHTML=ids.map(i=>enHTML[i]).join(' ');$('hebrew').innerHTML=ids.map(i=>heHTML[i]).join(' ');}
function hasRoom(){return ['english','hebrew'].every(id=>{const e=$(id);return e.scrollHeight<=e.parentElement.clientHeight-6&&e.scrollWidth<=e.clientWidth+1;});}
function resetSize(){for(const id of ['english','hebrew'])$(id).style.fontSize='';}
function fit(){resetSize();for(const id of ['english','hebrew']){const e=$(id),slot=e.parentElement;let px=parseFloat(getComputedStyle(e).fontSize);while((e.scrollHeight>slot.clientHeight-6||e.scrollWidth>slot.clientWidth+1)&&px>17){px-=.5;e.style.fontSize=px+'px';}}}
function deckSlidesFor(sentenceIndex){return deck?.after?.[String(sentenceIndex+1)]||deck?.after?.[sentenceIndex+1]||[];}
function renderDeckSlide(slide,sentenceIndex,idx){
 stop();breakIndex=idx;sheet.hidden=true;deckSheet.hidden=false;document.body.classList.add('readalong-break');$('play').disabled=true;$('replay').disabled=true;
 const q=esc(slide.q||''),a=esc(slide.a||''),why=esc(slide.why||''),formula=esc(slide.formula||''),ex=esc(slide.ex||''),pq=esc(slide.pq||'');
 let body='';
 if(slide.type==='question')body=`<div class="deck-kicker">SENTENCE ${sentenceIndex+1} · QUESTION</div><h1 class="deck-title">שאלה על המשפט</h1><p class="deck-question en">${q}</p>`;
 else if(slide.type==='answer')body=`<div class="deck-kicker">SENTENCE ${sentenceIndex+1} · ANSWER</div><p class="deck-question en">${q}</p><div class="deck-card"><p class="deck-answer en">${a}</p><p class="deck-note">${why}</p></div>`;
 else if(slide.type==='grammar')body=`<div class="deck-kicker">SENTENCE ${sentenceIndex+1} · GRAMMAR</div><h1 class="deck-title">איך בנינו את השאלה?</h1><div class="deck-formula en">${formula}</div><p class="deck-note">${why}</p>`;
 else if(slide.type==='practice'){const choices=(slide.choices||[]).map(x=>`<button class="deck-choice en" data-choice="${esc(x)}">${esc(x)}</button>`).join('');body=`<div class="deck-kicker">SENTENCE ${sentenceIndex+1} · PRACTICE</div><p class="deck-example en">${ex}</p><p class="deck-question en">${pq}</p><div class="deck-choices">${choices}</div><p class="deck-note" id="deck-feedback" hidden>התשובה: <b class="en">${esc(slide.good||'')}</b></p>`;}
 else body=`<div class="deck-card"><p class="deck-note">${esc(slide.text||'')}</p></div>`;
 deckSheet.innerHTML=`<div class="deck-meta"><span>${esc(deck?.title||'')}</span><span>שקף ${idx+1} / ${deckSlidesFor(sentenceIndex).length}</span></div><div class="deck-body">${body}</div>`;
 deckSheet.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{const good=b.dataset.choice===String(slide.good||'');b.classList.add(good?'good':'bad');const fb=$('deck-feedback');if(fb)fb.hidden=false;});
 $('counter').textContent='משפט '+(sentenceIndex+1)+' · דקדוק '+(idx+1)+'/'+deckSlidesFor(sentenceIndex).length;
 $('status').textContent='שקף רגיל · ממשיכים בחיצים או בהחלקה.';
 $('progress').style.width='0%';
}
function leaveDeck(){breakIndex=-1;deckSheet.hidden=true;sheet.hidden=false;document.body.classList.remove('readalong-break');if(ready){$('play').disabled=false;$('replay').disabled=false;}}
function makePages(){
 pages=[];pairKey='';
 if(view==='sentences'){D.story.forEach((s,i)=>pages.push({ids:[i],source:D.pages.findIndex(ids=>ids.includes(i)),sub:0}));return;}
 D.pages.forEach((ids,source)=>{let group=[],sub=0;for(const i of ids){const candidate=[...group,i];setText(candidate);resetSize();if(group.length&&!hasRoom()){pages.push({ids:group,source,sub:sub++});group=[i];}else group=candidate;}if(group.length)pages.push({ids:group,source,sub});});
}
function refreshTabs(){const source=pages[page].source;$('reading-tabs').innerHTML=D.pages.map((ids,p)=>`<button role="tab" aria-selected="${p===source}" aria-controls="sheet" id="reading-tab-${p}" class="${state.read['page'+p]?'done':''}" data-source="${p}" title="פסקה ${D.story[ids[0]].paragraph} · קטע ${p+1}">${D.story[ids[0]].paragraph} · ${p+1}</button>`).join('');sheet.setAttribute('aria-labelledby','reading-tab-'+source);}
function syncURL(){const p=new URLSearchParams(location.search);p.set('view',view);p.delete('break');if(view==='sentences'){p.set('p',String(page*2+Number(reveal)));p.delete('sub');p.delete('reveal');}else{p.set('p',String(pages[page].source));p.set('sub',String(pages[page].sub));p.set('reveal',String(Number(reveal)));}history.replaceState(null,'','?'+p+location.hash);state.last='?'+p;state.bilingualPosition={...state.bilingualPosition,[view]:{sentence:pages[page].ids[0],reveal}};save();}
function show(n,r=false,{persist=true,schedule=true}={}){
 stop();leaveDeck();page=Math.max(0,Math.min(pages.length-1,n));reveal=!!r;
 const ids=pages[page].ids,key=ids.join(',');
 if(pairKey!==key){setText(ids);pairKey=key;enNodes=Object.fromEntries([...stage.querySelectorAll('[data-en]')].map(e=>[e.dataset.en,e]));heNodes=Object.fromEntries([...stage.querySelectorAll('[data-he]')].map(e=>[e.dataset.he,e]));fit();}
 sheet.classList.toggle('with-translation',reveal);$('translation-slot').setAttribute('aria-hidden',String(!reveal));$('step-label').textContent=reveal?'אנגלית + עברית':'אנגלית';
 const numbered=ids.map(i=>D.story[i].number),loc=numbered.length===1?'משפט '+numbered[0]:'משפטים '+numbered[0]+'–'+numbered.at(-1);
 $('hint').textContent=loc+' · '+(reveal?'התרגום נשאר גלוי לאורך כל ההקראה.':'בשקופית הבאה מתווסף התרגום.');
 $('counter').textContent=(page*2+Number(reveal)+1)+' / '+pages.length*2;
 document.querySelectorAll('[data-step]').forEach(b=>b.disabled=Number(b.dataset.step)<0?page===0&&!reveal:page===pages.length-1&&reveal);
 refreshTabs();if(persist)syncURL();
 narrator.sentence=ids[0];narrator.part=0;narrator.offset=0;narrator.queue=[...ids];
 status(reveal?'לחצו על הקראה לעקיבה בשתי השפות.':'ההפסקות בשמע בלבד — 1.5 שניות.');
 ids.forEach(i=>records[i].parts.forEach((_,p)=>narrator.prepare(i,p).catch(()=>{})));
 if(auto&&schedule)scheduled=setTimeout(()=>{scheduled=null;if(!document.hidden&&!menu.open)narrator.playFrom(ids[0],0,ids);},2000);
}
function step(d){
 if(menu.open)return;
 const sentenceIndex=pages[page]?.ids?.[0]??0,breaks=deckSlidesFor(sentenceIndex);
 if(breakIndex>=0){
  const nextBreak=breakIndex+d;
  if(nextBreak>=0&&nextBreak<breaks.length){renderDeckSlide(breaks[nextBreak],sentenceIndex,nextBreak);return;}
  if(d<0){show(page,true);return;}
  if(page<pages.length-1){show(page+1,false);return;}
  return;
 }
 if(view==='sentences'&&deck){
  if(d>0){
   if(!reveal){show(page,true);return;}
   if(breaks.length){renderDeckSlide(breaks[0],sentenceIndex,0);return;}
   if(page<pages.length-1)show(page+1,false);
   return;
  }
  if(reveal){show(page,false);return;}
  if(page>0){const prev=page-1,prevSentence=pages[prev]?.ids?.[0]??0,prevBreaks=deckSlidesFor(prevSentence);if(prevBreaks.length){page=prev;renderDeckSlide(prevBreaks.at(-1),prevSentence,prevBreaks.length-1);}else show(prev,true);}
  return;
 }
 const index=page*2+Number(reveal),next=Math.max(0,Math.min(pages.length*2-1,index+d));if(next===index)return;show(Math.floor(next/2),!!(next%2));
}
function mark(s,i){const a=A[D.story[s].number],en=enNodes[`${s}:${i}`],he=heNodes[`${s}:${a.map[i]}`];if(en!==lastEn){lastEn?.classList.remove('marker');en?.classList.add('marker');lastEn=en;}if(he!==lastHe){lastHe?.classList.remove('marker');he?.classList.add('marker');lastHe=he;}}
function paint(p){
 $('footer').dataset.phase=p.phase;$('play').setAttribute('aria-pressed',String(p.isActive));
 if(ready)$('play').textContent=p.isActive?'❚❚ השהיה':['paused','pausedGap'].includes(p.phase)?'▶ המשך':'▶ הקראה';
 if(p.phase==='idle'){clearMarker();$('progress').style.width='0%';return;}
 if(p.phase==='loading'){status('טוען הקלטה…');return;}
 if(p.phase==='error'){clearMarker();status('ההקלטה לא נטענה. לחצו על הקראה לניסיון נוסף.');return;}
 const s=D.story[p.sentence],part=p.segment,time=p.sourceTime;let i=-1;
 if(['gap','pausedGap','ended'].includes(p.phase))i=part.lastToken;
 else{i=s.tokens.findIndex((t,n)=>n>=part.firstToken&&n<=part.lastToken&&time>=t.start&&time<t.end);if(i<0){for(let n=part.firstToken;n<=part.lastToken;n++)if(time>=s.tokens[n].start)i=n;}}
 if(i>=0)mark(p.sentence,i);
 const queue=p.queue||[p.sentence],before=queue.slice(0,queue.indexOf(p.sentence)).reduce((a,n)=>a+records[n].duration,0),total=queue.reduce((a,n)=>a+records[n].duration,0);
 $('progress').style.width=Math.min(100,(before+time)/total*100)+'%';
 status(p.phase==='gap'?'הפסקה של 1.5 שניות…':['paused','pausedGap'].includes(p.phase)?'ההקראה מושהית — לחצו על המשך.':p.phase==='ended'?'סוף '+(queue.length===1?'המשפט':'הקטע')+'. ממשיכים כשמוכנים.':reveal?'המרקר עוקב באנגלית ובעברית.':'הקראה באנגלית.');
}
narrator=new TeacherPhrasePlayer(records,{pauseMs:STANDARD.pauseMs,onUpdate:paint,onComplete:()=>{narrator.queue.forEach(i=>state.read['sentence-'+i]=true);D.pages.forEach((ids,p)=>{if(ids.every(i=>state.read['sentence-'+i]))state.read['page'+p]=true;});save();refreshTabs();}});narrator.setRate(rate);
function play(restart=false){clearTimeout(scheduled);scheduled=null;auto=true;hideTip();if(!restart&&narrator.isActive)narrator.pause();else if(!restart&&['paused','pausedGap'].includes(narrator.phase))narrator.resume();else{const ids=pages[page].ids;narrator.playFrom(ids[0],0,ids);}}
$('play').onclick=()=>play();$('replay').onclick=()=>play(true);$('speed').onchange=()=>{rate=Number($('speed').value);narrator.setRate(rate);try{localStorage.setItem(speedStore||STANDARD.speedStore,String(rate));}catch(_){}};
$('contents').onclick=()=>{stop();menu.showModal();};$('close-menu').onclick=()=>menu.close();
menu.querySelector(`[data-mode="${view}"]`).setAttribute('aria-current','page');
$('sentence-list').innerHTML=D.story.map((s,i)=>`<button data-jump="${i}"><small>${s.paragraph} · ${s.number}</small>${esc(s.plain)}</button>`).join('');
function jump(i){menu.close();show(pages.findIndex(p=>p.ids.includes(i)),false);}
$('sentence-list').onclick=e=>{const b=e.target.closest('[data-jump]');if(b)jump(Number(b.dataset.jump));};
$('start-over').onclick=()=>{menu.close();show(0,false);};$('resume-reading').onclick=()=>{menu.close();if(savedLocation){const p=pages.findIndex(p=>p.ids.includes(savedLocation.sentence));show(Math.max(0,p),savedLocation.reveal);}else show(page,reveal);};
$('reading-tabs').onclick=e=>{const b=e.target.closest('[data-source]');if(b)show(pages.findIndex(p=>p.source===Number(b.dataset.source)),false);};
$('reading-tabs').onkeydown=e=>{const b=e.target.closest('[data-source]');if(!b||!['ArrowLeft','ArrowRight'].includes(e.key))return;e.stopPropagation();e.preventDefault();const target=Math.max(0,Math.min(D.pages.length-1,Number(b.dataset.source)+(e.key==='ArrowRight'?1:-1)));show(pages.findIndex(p=>p.source===target),false);$('reading-tab-'+target).focus();};
function tip(node){if(!node)return;const [s,i]=node.dataset.en.split(':').map(Number),t=D.story[s].tokens[i],el=$('reading-tip');el.textContent=t.he;el.hidden=false;el.style.left='10px';el.style.top='0px';const r=node.getBoundingClientRect(),h=el.offsetHeight,w=el.offsetWidth;el.style.left=Math.max(10,Math.min(innerWidth-w-10,r.x+r.width/2-w/2))+'px';el.style.top=(r.bottom+h+8<innerHeight-75?r.bottom+7:Math.max(64,r.top-h-7))+'px';}
let ignoreClick=0;stage.addEventListener('click',e=>{if(performance.now()<ignoreClick){e.preventDefault();return;}const n=e.target.closest('[data-en]');if(n)tip(n);else hideTip();});stage.addEventListener('pointerover',e=>{if(e.pointerType==='mouse')tip(e.target.closest('[data-en]'));});stage.addEventListener('pointerout',e=>{if(e.pointerType==='mouse')hideTip();});stage.addEventListener('focusin',e=>tip(e.target.closest('[data-en]')));
document.addEventListener('click',e=>{if(e.target.closest('a'))stop();});
window.addEventListener('keydown',e=>{if(menu.open||e.altKey||e.ctrlKey||e.metaKey||e.target.closest('select,input,textarea'))return;if(e.key==='Escape'){hideTip();if(narrator.isActive)narrator.pause();return;}if((e.key==='Enter'||e.key===' ')&&e.target.matches('[data-en]')){e.preventDefault();tip(e.target);return;}if(['ArrowDown','ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();step(1);}else if(['ArrowUp','ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();step(-1);}else if(e.key==='Home'){e.preventDefault();show(0,false);}else if(e.key==='End'){e.preventDefault();show(pages.length-1,true);}});
let gesture=null,touches=new Set(),touchGesture=null,lastSwipeAt=0;
function swipeTargetBlocked(target){return !!target.closest?.('button,a,select,input,textarea,[data-en]');}
function runSwipe(dx,dy,startedAt){
 const now=performance.now();if(now-lastSwipeAt<350)return false;
 if(Math.max(Math.abs(dx),Math.abs(dy))<44||now-startedAt>=1800)return false;
 lastSwipeAt=now;ignoreClick=now+500;hideTip();
 step((Math.abs(dx)>Math.abs(dy)?dx:dy)<0?1:-1);return true;
}
stage.addEventListener('pointerdown',e=>{touches.add(e.pointerId);if(touches.size>1){gesture=null;return;}if(e.pointerType==='mouse'&&e.button!==0)return;if(swipeTargetBlocked(e.target)||(window.visualViewport?.scale||1)>1)return;gesture={id:e.pointerId,x:e.clientX,y:e.clientY,t:performance.now()};try{stage.setPointerCapture(e.pointerId);}catch(_){}});
stage.addEventListener('pointerup',e=>{const g=gesture;gesture=null;touches.delete(e.pointerId);if(!g||g.id!==e.pointerId||touches.size)return;runSwipe(e.clientX-g.x,e.clientY-g.y,g.t);});
stage.addEventListener('pointercancel',e=>{touches.delete(e.pointerId);gesture=null;});
/* Touch fallback keeps swipe navigation available during native deck/interlude slides too. */
stage.addEventListener('touchstart',e=>{if(e.touches.length!==1||swipeTargetBlocked(e.target)||(window.visualViewport?.scale||1)>1){touchGesture=null;return;}const t=e.touches[0];touchGesture={x:t.clientX,y:t.clientY,t:performance.now()};},{passive:true});
stage.addEventListener('touchend',e=>{const g=touchGesture;touchGesture=null;if(!g||e.changedTouches.length!==1)return;const t=e.changedTouches[0];runSwipe(t.clientX-g.x,t.clientY-g.y,g.t);},{passive:true});
stage.addEventListener('touchcancel',()=>{touchGesture=null;},{passive:true});
let totalWheel=0,lock=0,previous=0;stage.addEventListener('wheel',e=>{if(e.ctrlKey||e.metaKey||menu.open||e.target.closest('.tabstrip'))return;e.preventDefault();const now=performance.now();if(now<lock)return;if(now-previous>160)totalWheel=0;previous=now;totalWheel+=(Math.abs(e.deltaY)>=Math.abs(e.deltaX)?e.deltaY:e.deltaX)*(e.deltaMode===1?16:e.deltaMode===2?500:1);if(Math.abs(totalWheel)>55){step(totalWheel>0?1:-1);totalWheel=0;lock=now+500;}},{passive:false});
window.addEventListener('pagehide',stop);window.addEventListener('blur',()=>{if(narrator.isActive||scheduled)stop();});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
window.addEventListener('resize',()=>{gesture=null;clearTimeout(resizeTimer);const sentence=pages[page]?.ids[0]||0,r=reveal;resizeTimer=setTimeout(()=>{stop();makePages();show(Math.max(0,pages.findIndex(p=>p.ids.includes(sentence))),r,{schedule:false});},120);});
await document.fonts.ready;
makePages();const qs=new URLSearchParams(location.search),old=Math.max(0,Number(qs.get('p'))||0),sub=Math.max(0,Number(qs.get('sub'))||0);
const start=view==='sentences'?Math.floor(old/2):pages.findIndex(p=>p.source===Math.min(old,D.pages.length-1)&&p.sub===sub);
show(Math.max(0,start),view==='sentences'?!!(old%2):qs.get('reveal')==='1',{persist:false,schedule:false});
ready=true;$('play').disabled=false;$('replay').disabled=false;$('play').textContent='▶ הקראה';
window.__grade8Bilingual={D,records,alignment:A,player:narrator,view,deck,show,step,stop,get pages(){return pages;},get page(){return page;},get reveal(){return reveal;},get breakIndex(){return breakIndex;},get ready(){return ready;},get marker(){return{en:lastEn?.dataset.en||null,he:lastHe?.dataset.he||null};},get auto(){return auto;}};
};
