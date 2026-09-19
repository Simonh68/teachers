(()=>{'use strict';
const $=s=>document.querySelector(s),esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const state={choices:{},route:[]};let i=0;const key='teachers-the-same-way-slide-v1';
const fromHash=parseInt(location.hash.slice(1),10);if(fromHash>0)i=Math.min(SLIDES.length-1,fromHash-1);
const pmap=['A','B','C','D','E'];let lastWheel=0;
const routeItems=['walk to school','train','walk to the bus stop','second bus','first bus'];
const correctRoute=['walk to the bus stop','first bus','train','second bus','walk to school'];
function isReview(s){return s.kind==='review'||(['quiz','route'].includes(s.kind)&&s.reveal);}
function outcome(s){
 if(s.kind==='quiz'){const pick=state.choices[i-1];return pick===undefined?{tone:'unanswered',text:'לא נבחרה תשובה — נבדוק יחד'}:pick===s.correct?{tone:'success',text:'✓ נכון! כל הכבוד.'}:{tone:'needs-work',text:'✗ התשובה שבחרתם אינה נכונה — הנה התיקון'};}
 const count=state.route.filter((x,n)=>x===correctRoute[n]).length;
 return !state.route.length?{tone:'unanswered',text:'לא נבחר סדר — נבדוק יחד'}:state.route.length<5?{tone:'needs-work',text:`הסדר לא הושלם: נבחרו ${state.route.length} מתוך 5 תחנות`}:count===5?{tone:'success',text:'✓ נכון! כל 5 התחנות בסדר הנכון.'}:{tone:'needs-work',text:`✗ צריך לתקן את הסדר: ${count} מתוך 5 תחנות במקום הנכון`};
}
function banner(s){const o=s.reveal?outcome(s):{tone:'pending',text:s.kind==='quiz'?'בחרו תשובה, ואז לחצו על בדיקה':'סדרו את כל 5 התחנות, ואז לחצו על בדיקה'};return `<div class="assessmentBanner ${o.tone}" role="status">${esc(o.text)}</div>`;}
function reviewActions(){return `<div class="reviewActions"><button id="retryAnswer">↶ ניסיון נוסף</button><button id="reviewContinue">המשך ←</button></div>`;}
function quizFeedback(s,pick){return `<section class="answerFeedback" tabindex="-1" aria-label="משוב לתשובה"><p>התשובה שלכם: <bdi dir="ltr">${pick===undefined?'לא נבחרה תשובה':esc(s.opts[pick])}</bdi></p><p class="rightAnswer">✓ התשובה הנכונה: <bdi dir="ltr">${esc(s.opts[s.correct])}</bdi></p><p class="explanation">${esc(s.why)}</p>${reviewActions()}</section>`;}
function routeFeedback(s){return `<div class="routeComparison"><div class="routeHead">שלב</div><div class="routeHead">הסדר שלכם</div><div class="routeHead ${s.reveal?'':'hidden'}">הסדר הנכון</div>${correctRoute.map((x,n)=>{const picked=state.route[n],same=picked===x;return `<div class="routeStep">${n+1}</div><div class="routeCell ${s.reveal?(same?'match':'mismatch'):''}"><bdi dir="ltr">${esc(picked||'—')}</bdi><span class="routeVerdict ${s.reveal?'':'hidden'}">${!picked?'חסר':same?'✓ במקום הנכון':'✗ לא במקום הנכון'}</span></div><div class="routeCell rightAnswer ${s.reveal?'':'hidden'}"><bdi dir="ltr">${esc(x)}</bdi></div>`;}).join('')}</div>`;}
const wordTooltip=document.createElement('div');wordTooltip.id='sentenceWordTooltip';wordTooltip.role='tooltip';wordTooltip.dir='rtl';wordTooltip.hidden=true;document.body.append(wordTooltip);let tooltipWord=null;
function hideWordTooltip(){tooltipWord?.removeAttribute('aria-describedby');tooltipWord=null;wordTooltip.hidden=true;}
function showWordTooltip(word){hideWordTooltip();tooltipWord=word;wordTooltip.textContent=word.dataset.translation;wordTooltip.hidden=false;word.setAttribute('aria-describedby',wordTooltip.id);const r=word.getBoundingClientRect(),b=wordTooltip.getBoundingClientRect();wordTooltip.style.left=Math.max(8,Math.min(innerWidth-b.width-8,r.left+(r.width-b.width)/2))+'px';wordTooltip.style.top=(r.top-b.height-10>=8?r.top-b.height-10:r.bottom+10)+'px';}
document.addEventListener('pointerdown',e=>{if(!e.target.closest('.sentenceWord'))hideWordTooltip();});document.addEventListener('keydown',e=>{if(e.key==='Escape')hideWordTooltip();});window.addEventListener('resize',hideWordTooltip);$('#stage').addEventListener('scroll',hideWordTooltip,{passive:true});
const sentenceAudio=new Audio();sentenceAudio.id='sentenceAudio';sentenceAudio.preload='auto';document.body.append(sentenceAudio);
let sentenceTimer=0,sentenceFrame=0,sentenceRun=0,sentenceEnd=0,sentenceCues=[],spokenIndex=-1;
const narrationData=fetch('reading.json?v=word-hover-9').then(r=>{if(!r.ok)throw Error('audio data');return r.json()});narrationData.catch(()=>{});
function clearSentenceHighlight(){document.querySelectorAll('.sentenceWord.spoken').forEach(w=>w.classList.remove('spoken'));spokenIndex=-1;}
function syncSentenceHighlight(){const t=sentenceAudio.currentTime;const index=sentenceAudio.paused?-1:sentenceCues.findIndex(w=>t>=w.start&&t<w.end);if(index===spokenIndex)return;clearSentenceHighlight();if(index>=0){const word=document.querySelector(`[data-sentence-word="${index}"]`);if(word){word.classList.add('spoken');spokenIndex=index;}}}
function stopSentence(){clearSentenceHighlight();sentenceRun++;clearTimeout(sentenceTimer);cancelAnimationFrame(sentenceFrame);sentenceAudio.pause();}
async function speakSentence(s){stopSentence();const run=sentenceRun;
 try{const data=await narrationData;if(run!==sentenceRun||document.hidden||$('#menu').open)return;const clip=data.sentences[s.n-1];sentenceCues=clip.words;if(!sentenceAudio.src)sentenceAudio.src=data.audio;
 let rate=.75;try{const saved=Number(localStorage.getItem('teachers-read-alone-speed-v1'));if([1,.75,.5,.35,.25].includes(saved))rate=saved;}catch(e){}
 sentenceAudio.playbackRate=rate;sentenceAudio.preservesPitch=true;sentenceAudio.currentTime=Math.max(0,clip.start-.03);sentenceEnd=clip.end+.025;
 await sentenceAudio.play();if(run!==sentenceRun){sentenceAudio.pause();return;}if($('#sentenceSpeak'))$('#sentenceSpeak').textContent='❚❚ עצירה';
 const watch=()=>{if(run!==sentenceRun)return;syncSentenceHighlight();if(sentenceAudio.currentTime>=sentenceEnd){sentenceAudio.pause();if($('#sentenceSpeak'))$('#sentenceSpeak').textContent='▶ שוב';return;}sentenceFrame=requestAnimationFrame(watch);};watch();
 }catch(e){if(run===sentenceRun&&$('#sentenceSpeak'))$('#sentenceSpeak').textContent='▶ לחצו להקראה';}}
sentenceAudio.addEventListener('timeupdate',()=>{syncSentenceHighlight();if(sentenceAudio.currentTime>=sentenceEnd)sentenceAudio.pause();});
sentenceAudio.addEventListener('seeked',syncSentenceHighlight);sentenceAudio.addEventListener('pause',clearSentenceHighlight);sentenceAudio.addEventListener('ended',clearSentenceHighlight);
window.addEventListener('pagehide',stopSentence);document.addEventListener('visibilitychange',()=>{if(document.hidden)stopSentence();});
// Use the same gesture rules in the outer deck and inside the reading frame.
function installSwipe(surface,navigate){
 let gesture=null,suppressClickUntil=0;
 const scrolls=(node,dy)=>{for(let el=node;el&&el.nodeType===1;el=el.parentElement){const style=el.ownerDocument.defaultView.getComputedStyle(el);if(/auto|scroll/.test(style.overflowY)&&el.scrollHeight>el.clientHeight+3){if(dy<0&&el.scrollTop+el.clientHeight<el.scrollHeight-3)return true;if(dy>0&&el.scrollTop>3)return true;}}return false;};
 surface.addEventListener('touchstart',e=>{gesture=null;if(e.touches.length!==1||e.target.closest('input,select,textarea'))return;const t=e.touches[0];gesture={x:t.clientX,y:t.clientY,target:e.target,scroll:false};},{capture:true,passive:true});
 surface.addEventListener('touchmove',e=>{if(!gesture||e.touches.length!==1){gesture=null;return;}const t=e.touches[0],dx=t.clientX-gesture.x,dy=t.clientY-gesture.y;if(Math.max(Math.abs(dx),Math.abs(dy))<10)return;const horizontal=Math.abs(dx)>Math.abs(dy)*1.15;if(!horizontal&&scrolls(gesture.target,dy)){gesture.scroll=true;return;}if(!gesture.scroll&&e.cancelable)e.preventDefault();},{capture:true,passive:false});
 surface.addEventListener('touchend',e=>{if(!gesture)return;const g=gesture;gesture=null;const t=e.changedTouches[0],dx=t.clientX-g.x,dy=t.clientY-g.y;if(g.scroll||Math.max(Math.abs(dx),Math.abs(dy))<45)return;const horizontal=Math.abs(dx)>Math.abs(dy)*1.15;if(!horizontal&&(Math.abs(dy)<=Math.abs(dx)*1.15||scrolls(g.target,dy)))return;if(e.cancelable)e.preventDefault();e.stopImmediatePropagation();suppressClickUntil=Date.now()+450;navigate((horizontal?dx:dy)<0?1:-1);},{capture:true,passive:false});
 surface.addEventListener('touchcancel',()=>{gesture=null;},{capture:true,passive:true});
 surface.addEventListener('click',e=>{if(Date.now()<suppressClickUntil){e.preventDefault();e.stopImmediatePropagation();}},{capture:true});
}
let readerFrame=null,readerReady=false,readerAutomatic=false;
function readingChrome(s){$('#next').textContent='→';$('#next').setAttribute('aria-label','השקף הבא');$('#counter').textContent=`${i+1} / ${SLIDES.length}`;$('#prev').disabled=i===0;$('#next').disabled=i===SLIDES.length-1;$('#readLabel').textContent=`Read Alone Text · דף ${s.page+1} / 10`;$('#readBar').style.width=((s.page+1)/10*100)+'%';history.replaceState(null,'','#'+(i+1));try{localStorage.setItem(key,i)}catch(e){}}
function render(){hideWordTooltip();stopSentence();const s=SLIDES[i];
if(s.kind==='readalong'){
 $('#stage').classList.add('reader-stage');readingChrome(s);
 if(!readerFrame){readerReady=false;readerFrame=document.createElement('iframe');readerFrame.title='Read Alone Text — קריאה מלווה של הסיפור המלא';readerFrame.src='read-along.html?v=word-hover-9';$('#stage').replaceChildren(readerFrame);
 readerFrame.onload=()=>{const w=readerFrame.contentWindow;const ready=()=>{readerReady=true;if(w.readAlong?.data)w.readAlong.setPage(SLIDES[i].page);};w.addEventListener('reader-complete',()=>go(SLIDES.findLastIndex(x=>x.kind==='readalong')+1));w.addEventListener('reader-ready',ready);if(w.readAlong?.data)ready();w.addEventListener('reader-page',e=>{const target=SLIDES.findIndex(x=>x.kind==='readalong'&&x.page===e.detail.page);if(target!==i){readerAutomatic=true;go(target);readerAutomatic=false;}});w.document.addEventListener('keydown',e=>{if(e.target.closest('button,input,select,.unit')||!['ArrowRight','ArrowDown','ArrowLeft','ArrowUp'].includes(e.key))return;e.preventDefault();e.stopImmediatePropagation();go(i+(['ArrowRight','ArrowDown'].includes(e.key)?1:-1));},true);
 installSwipe(w.document,delta=>go(i+delta));};
 }else if(readerReady&&!readerAutomatic)readerFrame.contentWindow.readAlong.setPage(s.page);
 return;
}
if(readerFrame){readerFrame.contentWindow.readAlong?.pause();readerFrame.remove();readerFrame=null;readerReady=false;}
$('#stage').classList.remove('reader-stage');$('#stage').scrollTop=0;let c='';
const title=`<p class="eyebrow">${esc(s.title)}</p>`;const tense=`<div class="tense ${s.tense==='הווה'?'present':s.tense==='עתיד'?'future':''}">${esc(s.tense)}</div>`;
if(s.kind==='cover')c=`<p class="eyebrow">ברוכים הבאים</p><h1>The Same Way</h1><p class="sub">${esc(s.sub)}</p><p class="sub" style="font-size:16px">נוצר: מוצאי שבת, ט׳ בתשרי תשפ״ז (19.9.2026)</p><div class="linkrow"><button id="startNow">פתיחת המצגת</button><button id="resume">המשך מהמקום האחרון</button></div>`;
else if(s.kind==='whole')c=`<h2 dir="ltr">The Same Way</h2><p class="sub">${esc(s.sub)}</p><div class="story">${STORY.paragraphs.map((p,n)=>`<p><span class="para">${pmap[n]}</span>${esc(p)}</p>`).join('')}</div><span class="wordcount">${STORY.wordcount} words</span>`;
else if(s.kind==='sentence')c=`<h2>פסקה ${s.part} · משפט ${s.n} מתוך ${STORY.sentences.length} <button id="sentenceSpeak" aria-label="הקראת המשפט באנגלית">▶ הקראה</button></h2>${tense}<p class="hero english"><span class="sentenceWords">${s.en.split(' ').map((word,n)=>`<span class="sentenceWord" data-sentence-word="${n}" tabindex="0" role="button" aria-label="${esc(word)} — תרגום לעברית" data-translation="${esc(SENTENCE_WORD_TRANSLATIONS[s.n-1][n].he)}">${esc(word)}</span>`).join(' ')}</span></p><div class="translation ${s.reveal?'':'hidden'}" ${s.reveal?'':'aria-hidden="true"'}>${esc(s.he)}</div>`;
else if(s.kind==='quiz'){const qid=s.reveal?i-1:i,pick=state.choices[qid];c=`${banner(s)}${title}${tense}<p class="hero english">${esc(s.q)}</p><div class="options">${s.opts.map((o,n)=>`<button class="option ${pick===n?'selected':''} ${s.reveal&&s.correct===n?'correct':''} ${s.reveal&&pick===n&&n!==s.correct?'incorrect':''}" data-choice="${n}" ${s.reveal?'disabled':''} aria-pressed="${pick===n}"><span>${esc(o)}</span><span class="choiceLabel">${s.reveal?(s.correct===n?(pick===n?'✓ בחרתם נכון':'✓ התשובה הנכונה'):pick===n?'✗ הבחירה שלכם':''):pick===n?'הבחירה שלכם':' '}</span></button>`).join('')}</div>${s.reveal?quizFeedback(s,pick):`<p class="questionHint" role="status">${pick===undefined?'אפשר לבחור תשובה או לפתוח פתרון לבדיקה משותפת.':'הבחירה נשמרה. עכשיו נבדוק אותה.'}</p><button id="checkAnswer">${pick===undefined?'הצגת פתרון לבדיקה משותפת':'בדיקת התשובה ←'}</button>`}`;}
else if(s.kind==='route')c=`${banner(s)}${title}<h2>לחצו על התחנות לפי סדר הנסיעה</h2><div class="options">${routeItems.map((x,n)=>`<button class="option" data-route="${n}" ${s.reveal||state.route.includes(x)?'disabled':''}>${esc(x)}</button>`).join('')}</div>${routeFeedback(s)}${s.reveal?`<section class="answerFeedback" tabindex="-1" aria-label="משוב לסדר הנסיעה"><p>השוו כל שורה: הבחירה שלכם נשארת בצד הסדר הנכון.</p><p class="explanation">פסקה B: הליכה לתחנה → אוטובוס ראשון → רכבת → אוטובוס שני → הליכה לבית הספר.</p>${reviewActions()}</section>`:`<p class="questionHint" role="status">נבחרו ${state.route.length} מתוך 5 תחנות. הפתרון יופיע רק בשקף הבא.</p><div class="reviewActions"><button id="resetRoute">איפוס הבחירה</button><button id="checkAnswer">${state.route.length===5?'בדיקת הסדר ←':'הצגת פתרון לבדיקה משותפת'}</button></div>`}`;
else if(s.kind==='review')c=`${title}<h2>${esc(s.heading)}</h2><p class="questionHint">אלו תשובות לדוגמה וכללי בדיקה. השוו לתשובות שכתבתם או אמרתם; אפשר לקבל ניסוח אחר שמשמעותו נכונה.</p><section class="answerFeedback" tabindex="-1" aria-label="משוב לבדיקה עצמית">${s.answers.map(a=>`<div class="modelAnswer"><h3>${esc(a.label)}</h3><p class="english">${esc(a.en)}</p><p>${esc(a.he)}</p></div>`).join('')}${reviewActions()}</section>`;
else if(s.kind==='pause')c=`<h2 dir="ltr">${esc(s.title)}</h2><img src="assets/train-umbrella.png" alt="איור משעשע: מטרייה ענקית מגינה על רכבת בגשם"><p class="sub">${esc(s.sub)}</p>`;
else if(s.kind==='links')c=`${title}<h2>${esc(s.sub)}</h2><div class="linkrow"><a href="https://englishfornoar.co.il/band-ii/groups/group-01.html" target="_blank" rel="noopener">תרגול קבוצה 01</a><a href="files/the-same-way-worksheet.pdf" target="_blank" rel="noopener">הסיפור והמשימות</a><a href="../../to-be/" target="_blank" rel="noopener">חזרה על To Be</a></div>`;
else c=`${title}${tense}<p class="hero english">${esc(s.text)}</p><p class="sub">${esc(s.sub)}</p>`;
$('#stage').innerHTML=`<article class="${s.kind}">${c}</article>`;$('#counter').textContent=`${i+1} / ${SLIDES.length}`;$('#prev').disabled=i===0;$('#next').disabled=i===SLIDES.length-1;
const progress=s.progress||0;$('#readLabel').innerHTML=progress?`התקדמות בקריאה: <bdi dir="ltr">${progress} / 28</bdi>`:'לפני הקריאה המודרכת';$('#readBar').style.width=(progress/28*100)+'%';
history.replaceState(null,'','#'+(i+1));try{if(i>0)localStorage.setItem(key,i)}catch(e){}
document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{state.choices[i]=Number(b.dataset.choice);render();document.querySelector(`[data-choice="${b.dataset.choice}"]`)?.focus({preventScroll:true});});
document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{const scroll=$('#stage').scrollTop;state.route.push(routeItems[Number(b.dataset.route)]);render();$('#stage').scrollTop=scroll});
if(s.kind==='sentence'){document.querySelectorAll('.sentenceWord').forEach(w=>{w.onpointerenter=e=>{if(e.pointerType!=='touch')showWordTooltip(w);};w.onpointerleave=e=>{if(e.pointerType!=='touch')hideWordTooltip();};w.onfocus=()=>showWordTooltip(w);w.onblur=hideWordTooltip;w.onclick=()=>showWordTooltip(w);w.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();showWordTooltip(w);}};});$('#sentenceSpeak').onclick=()=>{if(!sentenceAudio.paused){stopSentence();$('#sentenceSpeak').textContent='▶ שוב';}else speakSentence(s);};sentenceTimer=setTimeout(()=>speakSentence(s),2000);}
if($('#checkAnswer'))$('#checkAnswer').onclick=()=>go(i+1);
$('#next').textContent='→';$('#next').setAttribute('aria-label','השקף הבא');
if(isReview(s)){$('#reviewContinue').onclick=()=>go(i+1);$('#retryAnswer').onclick=()=>{if(s.kind==='quiz')delete state.choices[i-1];if(s.kind==='route')state.route=[];go(i-1);};}
if($('#resetRoute'))$('#resetRoute').onclick=()=>{state.route=[];render()};
if($('#startNow'))$('#startNow').onclick=()=>go(1);
if($('#resume'))$('#resume').onclick=()=>{let n=1;try{n=Number(localStorage.getItem(key))||1}catch(e){}go(n)};
}
function go(n){i=Math.max(0,Math.min(SLIDES.length-1,n));render()}
$('#prev').onclick=()=>go(i-1);$('#next').onclick=()=>go(i+1);
document.addEventListener('keydown',e=>{if($('#menu').open)return;if(e.target.closest('button,a,.sentenceWord')&&(e.key===' '||e.key==='Enter'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}if(e.key==='Home')go(0);if(e.key==='End')go(SLIDES.length-1)});
$('#stage').addEventListener('wheel',e=>{const el=$('#stage');if(el.scrollHeight>el.clientHeight+4){if(e.deltaY>0&&el.scrollTop+el.clientHeight<el.scrollHeight-3)return;if(e.deltaY<0&&el.scrollTop>3)return;}e.preventDefault();if(Date.now()-lastWheel<500)return;lastWheel=Date.now();go(i+(e.deltaY>0?1:-1))},{passive:false});
installSwipe($('#stage'),delta=>go(i+delta));
$('#menuBtn').onclick=()=>{stopSentence();readerFrame?.contentWindow.readAlong?.pause();$('#menu').showModal();};$('#closeMenu').onclick=()=>$('#menu').close();$('#restart').onclick=()=>{state.route=[];state.choices={};$('#menu').close();go(0)};
$('#fullBtn').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.();
const stops=[{label:'פתיחה',n:0},{label:'הסיפור המלא',n:1},{label:'Read Alone Text · קריאה והאזנה',n:SLIDES.findIndex(s=>s.kind==='readalong')},{label:'חיבור ל־To Be ולאוצר המילים',n:SLIDES.findIndex(s=>s.kind==='bridge')}];for(const p of pmap){stops.push({label:`פסקה ${p}`,n:SLIDES.findIndex(s=>s.kind==='sentence'&&s.part===p)})}stops.push({label:'משימת הדף',n:SLIDES.findIndex(s=>s.kind==='work')},{label:'בדיקת יציאה',n:SLIDES.findIndex(s=>s.kind==='exit')});
$('#contents').innerHTML=stops.map(x=>`<button data-go="${x.n}">${x.label}</button>`).join('');document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{$('#menu').close();go(Number(b.dataset.go))});
window.lesson={go,slides:SLIDES,state};render();
})();
