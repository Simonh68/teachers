/* Runs after the copied Unit 1 application; all overrides are confined to this copy. */
(()=>{'use strict';
const cfg=window.PILOT_PHRASES;
if(!cfg||cfg.sentences.length!==D.story.length)throw Error('Incomplete phrase snapshot');
const isReading=()=>['chunks','sentences'].includes(view),st=$('#stage');
const oldStop=stop,oldRender=render,oldText=textHTML,oldMove=move;
let narrator=null,lastWord=null,lastPart=null,lastScroll=0,lastStatus='';
let visibleIds=[],pageGroups=[],activeTab=-1,subIndex=Math.max(0,Number(qs.get('sub'))||0),reversePage=false;
const setStatus=text=>{if(lastStatus!==text){$('#audioStatus').textContent=text;lastStatus=text;}};
const queueFor=idx=>{const ids=visibleIds.length?visibleIds:(D.pages[pos]||[idx]);return view==='chunks'?ids.slice(Math.max(0,ids.indexOf(idx))):[idx];};
function paint(p){
 if(!isReading())return;
 const active=p.isActive;
 $('#play').textContent=active?'❚❚ השהיה':(['paused','pausedGap'].includes(p.phase)?'▶ המשך':'▶ הקראה');
 $('#play').setAttribute('aria-pressed',String(active));st.dataset.audioPhase=p.phase;
 if(p.phase==='idle'){$$('.word.playing,.sense-part.current-part,.sentence-unit.reading-now').forEach(x=>x.classList.remove('playing','current-part','reading-now'));lastWord=null;lastPart=null;return;}
 sentenceIndex=p.sentence;
 const record=p.record,part=p.segment;
 if(!record||!part)return;
 const partNode=st.querySelector(`[data-phrase-sentence="${p.sentence}"][data-phrase="${p.part}"]`);
 if(partNode!==lastPart){lastPart?.classList.remove('current-part');lastPart=partNode;partNode?.classList.add('current-part');
  $$('.sentence-unit.reading-now').forEach(x=>x.classList.remove('reading-now'));partNode?.closest('.sentence-unit')?.classList.add('reading-now');
  if(partNode&&performance.now()-lastScroll>1800){const r=partNode.getBoundingClientRect(),box=st.getBoundingClientRect();if(r.bottom>box.bottom-18||r.top<box.top+10)st.scrollTo({top:st.scrollTop+r.top-box.top-28,behavior:'auto'});}
 }
 const s=D.story[p.sentence],time=p.sourceTime;
 const i=p.phase==='playing'?s.tokens.findIndex(t=>time>=t.start&&time<t.end):-1;
 const word=i>=0?st.querySelector(`[data-sentence="${p.sentence}"][data-word="${i}"]`):null;
 if(word!==lastWord){lastWord?.classList.remove('playing');lastWord=word;word?.classList.add('playing');}
 $('#seek').value=Math.min(100,time/record.duration*100);
 const label=`משפט ${s.number} · חלק ${p.part+1} מתוך ${record.parts.length}`;
 if(p.phase==='gap')setStatus(label+' · הפסקה של 1.5 שניות…');
 else if(p.phase==='pausedGap')setStatus(label+' · מושהה; ההמשך ממתין ללחיצה');
 else if(p.phase==='paused')setStatus(label+' · מושהה');
 else if(p.phase==='loading')setStatus(label+' · טוען הקלטה');
 else if(p.phase==='playing')setStatus(label);
 else if(p.phase==='error')setStatus('לא ניתן להפעיל את ההקלטה כרגע. לחצו על הקראה לניסיון נוסף.');
}
narrator=new TeacherPhrasePlayer(cfg.sentences,{pauseMs:cfg.pauseMs,onUpdate:paint,onComplete:()=>{
 if(view==='chunks'){
  narrator.queue.forEach(i=>state.read['sentence-'+i]=true);save();
  if(D.pages[pos].every(i=>state.read['sentence-'+i]))mark();
  $('#next').textContent=subIndex+1<pageGroups.length?'המשך הפסקה ←':'המשך לקטע הבא ←';
  setStatus('סוף קטע הקריאה. ההקראה נעצרה; המשיכו כשתהיו מוכנים.');
 }else setStatus('סוף המשפט. בשקף הבא נחשף התרגום.');
}});
narrator.setRate(speed);
stop=function(){oldStop();narrator.stop();};
textHTML=function(s,units=false){
 if(!isReading())return oldText(s,units);
 const record=cfg.sentences[s.number-1];
 return record.parts.map(p=>{
  let html='',cursor=p.startChar;
  for(let i=p.firstToken;i<=p.lastToken;i++){
   const t=s.tokens[i],unit=s.units.find(u=>u.indices.includes(i));const gloss=units?(unit?.he||t.he):t.he;
   html+=esc(s.plain.slice(cursor,t.startChar));
   html+=`<span class="word ${units?'phrase':''}" role="button" tabindex="0" data-sentence="${s.number-1}" data-word="${i}" data-gloss="${esc(gloss)}" aria-label="${esc(t.text)}: ${esc(gloss)}">${esc(s.plain.slice(t.startChar,t.endChar))}</span>`;
   cursor=t.endChar;
  }
  html+=esc(s.plain.slice(cursor,p.endChar));
  return `<span class="sense-part ${p.index+1<record.parts.length?'has-breath':''}" data-phrase-sentence="${s.number-1}" data-phrase="${p.index}">${html}</span>`;
 }).join('');
};
playSentence=async function(idx,resume=false){
 clearTimeout(delay);delay=null;audio.pause();cancelAnimationFrame(frame);
 if(!isReading()||(view==='sentences'&&pos%2))return;
 if(resume&&narrator.sentence===idx&&['paused','pausedGap'].includes(narrator.phase))narrator.resume();
 else narrator.playFrom(idx,0,queueFor(idx));
};
function paginate(){
 visibleIds=[];pageGroups=[];if(view!=='chunks')return;
 const ids=D.pages[pos],cards=[...st.querySelectorAll('.sentence-unit')];
 const outer=el=>{if(!el)return 0;const c=getComputedStyle(el);return el.getBoundingClientRect().height+parseFloat(c.marginTop||0)+parseFloat(c.marginBottom||0);};
 const c=getComputedStyle(st),details=st.querySelector(':scope > details');
 const available=st.clientHeight-parseFloat(c.paddingTop)-parseFloat(c.paddingBottom)-outer(st.querySelector('.reader-heading'))-outer(details)-8;
 let group=[],height=0;
 cards.forEach((card,i)=>{
  const text=card.querySelector('.reading-text');let size=parseFloat(getComputedStyle(text).fontSize);
  while(outer(card)>available&&size>18){size--;text.style.fontSize=size+'px';text.style.lineHeight='1.6';}
  const h=outer(card);
  if(group.length&&height+h>available){pageGroups.push(group);group=[];height=0;}
  group.push(ids[i]);height+=h;
 });
 if(group.length)pageGroups.push(group);
 if(activeTab>=0&&activeTab!==pos)subIndex=reversePage?pageGroups.length-1:0;
 if(reversePage)subIndex=pageGroups.length-1;
 activeTab=pos;reversePage=false;subIndex=Math.max(0,Math.min(pageGroups.length-1,subIndex));visibleIds=pageGroups[subIndex]||ids;
 cards.forEach((card,i)=>card.hidden=!visibleIds.includes(ids[i]));
 if(details){const tr=details.querySelector('.he-translation');if(tr)tr.textContent=visibleIds.map(i=>D.story[i].he).join(' ');}
 sentenceIndex=visibleIds[0];
 $('#prev').disabled=pos===0&&subIndex===0;
 $('#next').disabled=pos===D.pages.length-1&&subIndex===pageGroups.length-1;
 $('#counter').textContent=`${pos+1} / ${D.pages.length}`+(pageGroups.length>1?` · ${subIndex+1} / ${pageGroups.length}`:'');
 const subtitle=st.querySelector('.reader-location');if(subtitle)subtitle.textContent='פסקה '+D.story[sentenceIndex].paragraph+(pageGroups.length>1?` · חלק ${subIndex+1}/${pageGroups.length}`:'');
 const params=new URLSearchParams(location.search);params.set('view',view);params.set('p',String(pos));if(subIndex)params.set('sub',String(subIndex));else params.delete('sub');
 state.last='?'+params.toString();save();history.replaceState(null,'',state.last);
}
function enhance(){
 document.body.classList.toggle('reading-pilot',isReading());$('#counter').dir='ltr';
 if(!isReading())return;
 const s=D.story[sentenceIndex],first=st.querySelector('p.small');
 if(first){first.className='reader-heading';first.innerHTML=`<span class="reader-name" lang="en">Read Along</span><span class="reader-location">פסקה ${esc(s.paragraph)}${view==='sentences'?' · משפט '+s.number:''}</span><span class="breath-badge">1.5 שנ׳ בין חלקים</span>`;}
 $('#repeat').title='חזרה על המשפט כולו';
 if(!$('#repeatPart')){const b=document.createElement('button');b.id='repeatPart';b.textContent='↺ חלק';b.title='השמעת חלק המשפט הנוכחי שוב';b.setAttribute('aria-label','השמעת חלק המשפט הנוכחי שוב');$('#repeat').after(b);}
 $('#repeatPart').onclick=()=>{clearTimeout(delay);const same=narrator.sentence===sentenceIndex&&narrator.phase!=='idle';narrator.playFrom(sentenceIndex,same?narrator.part:0,queueFor(sentenceIndex));};
 $('#seek').setAttribute('aria-label','מיקום בתוך המשפט, כולל כל חלקיו');
 $('#play').setAttribute('aria-pressed','false');
 paginate();
 setStatus(view==='sentences'&&pos%2?'התרגום נחשף; האנגלית נשארת במקומה.':'לחצו על הקראה. בכל גבול מסומן תישמע הפסקה של 1.5 שניות.');
 narrator.sentence=sentenceIndex;narrator.part=0;narrator.offset=0;narrator.queue=queueFor(sentenceIndex);
 narrator.prepare(sentenceIndex,0).catch(()=>{});
 syncTouchMode();
}
render=function(){
 oldRender();clearTimeout(delay);delay=null;lastStatus='';enhance();
 if(isReading()&&narrator.unlocked&&(view==='chunks'||pos%2===0)){
  const currentEpoch=epoch;delay=setTimeout(()=>{if(currentEpoch===epoch&&!document.hidden)playSentence(sentenceIndex);},2000);
 }
};
move=function(delta){
 if(view==='chunks'&&subIndex+delta>=0&&subIndex+delta<pageGroups.length){subIndex+=delta;render();return;}
 reversePage=view==='chunks'&&delta<0;oldMove(delta);reversePage=false;
};
$('#tabs').addEventListener('click',()=>{subIndex=0;},true);
$('#play').onclick=()=>{
 clearTimeout(delay);delay=null;
 if(!isReading()){playVocab();return;}
 if(narrator.isActive){narrator.pause();return;}
 if(['paused','pausedGap'].includes(narrator.phase)&&narrator.sentence===sentenceIndex){narrator.resume();return;}
 narrator.playFrom(sentenceIndex,0,queueFor(sentenceIndex));
};
$('#repeat').onclick=()=>{clearTimeout(delay);if(!isReading()){playVocab();return;}narrator.playFrom(sentenceIndex,0,queueFor(sentenceIndex));};
$('#seek').oninput=()=>{clearTimeout(delay);if(isReading())narrator.seekFraction(Number($('#seek').value)/100);else if(Number.isFinite(audio.duration))audio.currentTime=Number($('#seek').value)/100*audio.duration;};
const oldSpeed=$('#speed').onchange;
$('#speed').onchange=()=>{oldSpeed();narrator.setRate(speed);};
st.addEventListener('wheel',()=>lastScroll=performance.now(),{passive:true});
st.addEventListener('touchstart',()=>lastScroll=performance.now(),{passive:true});
document.addEventListener('click',e=>{if(e.target.closest('a'))stop();},true);
window.addEventListener('blur',()=>{if(narrator.isActive||delay)stop();});
let resizeTimer;
window.addEventListener('resize',()=>{if(view==='chunks'){clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>render(),150);}});
if(isReading())render();else{
 const hero=$('#home .hero');if(hero)hero.insertAdjacentHTML('beforeend','<p class="pilot-note">עותק קריאה נפרד · הקראה בחלקי משפט עם הפסקות של 1.5 שניות. התוכנית והתוכן נשמרו מהיחידה המקורית.</p>');
}
window.__readingPilot={player:narrator,data:cfg,get view(){return view;},get position(){return pos;},get sentence(){return sentenceIndex;},get subpage(){return subIndex;},get groups(){return pageGroups;},get visibleSentences(){return visibleIds;},show(n){pos=n;subIndex=0;activeTab=-1;render();},get originalAudio(){return audio;}};
})();
