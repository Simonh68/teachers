(()=>{'use strict';
const $=s=>document.querySelector(s),esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const state={choices:{},route:[]};let i=0;const key='teachers-the-same-way-slide-v1';
const fromHash=parseInt(location.hash.slice(1),10);if(fromHash>0)i=Math.min(SLIDES.length-1,fromHash-1);
const pmap=['A','B','C','D','E'];let lastWheel=0;
const routeItems=['walk to school','train','walk to the bus stop','second bus','first bus'];
const correctRoute=['walk to the bus stop','first bus','train','second bus','walk to school'];
let readerFrame=null,readerReady=false,readerAutomatic=false;
function readingChrome(s){$('#counter').textContent=`${i+1} / ${SLIDES.length}`;$('#prev').disabled=i===0;$('#next').disabled=i===SLIDES.length-1;$('#readLabel').textContent=`Read Alone Text · דף ${s.page+1} / 10`;$('#readBar').style.width=((s.page+1)/10*100)+'%';history.replaceState(null,'','#'+(i+1));try{localStorage.setItem(key,i)}catch(e){}}
function render(){const s=SLIDES[i];
if(s.kind==='readalong'){
 $('#stage').classList.add('reader-stage');readingChrome(s);
 if(!readerFrame){readerReady=false;readerFrame=document.createElement('iframe');readerFrame.title='Read Alone Text — קריאה מלווה של הסיפור המלא';readerFrame.src='read-along.html?v=integrated-mobile-2';$('#stage').replaceChildren(readerFrame);
 readerFrame.onload=()=>{const w=readerFrame.contentWindow;const ready=()=>{readerReady=true;if(w.readAlong?.data)w.readAlong.setPage(SLIDES[i].page);};w.addEventListener('reader-ready',ready);if(w.readAlong?.data)ready();w.addEventListener('reader-page',e=>{const target=SLIDES.findIndex(x=>x.kind==='readalong'&&x.page===e.detail.page);if(target!==i){readerAutomatic=true;go(target);readerAutomatic=false;}});w.document.addEventListener('keydown',e=>{if(e.target.closest('button,input,select,.unit')||!['ArrowRight','ArrowDown','ArrowLeft','ArrowUp'].includes(e.key))return;e.preventDefault();e.stopImmediatePropagation();go(i+(['ArrowRight','ArrowDown'].includes(e.key)?1:-1));},true);
 w.document.addEventListener('touchstart',e=>{if(e.target.closest('button,input,select,.unit'))return;touch={x:e.touches[0].clientX,y:e.touches[0].clientY};},{passive:true,capture:true});w.document.addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;touch=null;if(Math.abs(dx)>70&&Math.abs(dx)>Math.abs(dy)){e.stopImmediatePropagation();go(i+(dx<0?1:-1));}},{capture:true});};
 }else if(readerReady&&!readerAutomatic)readerFrame.contentWindow.readAlong.setPage(s.page);
 return;
}
if(readerFrame){readerFrame.contentWindow.readAlong?.pause();readerFrame.remove();readerFrame=null;readerReady=false;}
$('#stage').classList.remove('reader-stage');$('#stage').scrollTop=0;let c='';
const title=`<p class="eyebrow">${esc(s.title)}</p>`;const tense=`<div class="tense ${s.tense==='הווה'?'present':s.tense==='עתיד'?'future':''}">${esc(s.tense)}</div>`;
if(s.kind==='cover')c=`<p class="eyebrow">ברוכים הבאים</p><h1>The Same Way</h1><p class="sub">${esc(s.sub)}</p><p class="sub" style="font-size:16px">נוצר: מוצאי שבת, ט׳ בתשרי תשפ״ז (19.9.2026)</p><div class="linkrow"><button id="startNow">פתיחת המצגת</button><button id="resume">המשך מהמקום האחרון</button></div>`;
else if(s.kind==='whole')c=`<h2 dir="ltr">The Same Way</h2><p class="sub">${esc(s.sub)}</p><div class="story">${STORY.paragraphs.map((p,n)=>`<p><span class="para">${pmap[n]}</span>${esc(p)}</p>`).join('')}</div><span class="wordcount">${STORY.wordcount} words</span>`;
else if(s.kind==='sentence')c=`<h2>פסקה ${s.part} · משפט ${s.n} מתוך ${STORY.sentences.length}</h2>${tense}<p class="hero english">${esc(s.en)}</p><div class="translation ${s.reveal?'':'hidden'}" ${s.reveal?'':'aria-hidden="true"'}>${esc(s.he)}</div>`;
else if(s.kind==='quiz'){let qid=s.reveal?i-1:i;c=`${title}${tense}<p class="hero english">${esc(s.q)}</p><div class="options">${s.opts.map((o,n)=>`<button class="option ${state.choices[qid]===n?'selected':''} ${s.reveal&&s.correct===n?'correct':''}" data-choice="${n}" ${s.reveal?'disabled':''} aria-pressed="${state.choices[qid]===n}">${esc(o)}</button>`).join('')}</div><div class="response ${s.reveal?'':'neutral'}" aria-live="polite">${s.reveal?esc(s.why):state.choices[qid]!==undefined?'הבחירה נשמרה. בדקו את הנימוק בשקף הבא.':'בחרו תשובה ונמקו. הפתרון בשקף הבא.'}</div>`;}
else if(s.kind==='route')c=`${title}<h2>לחצו על התחנות לפי סדר הנסיעה</h2><div class="options">${routeItems.map((x,n)=>`<button class="option" data-route="${n}" ${s.reveal||state.route.includes(x)?'disabled':''}>${esc(x)}</button>`).join('')}</div><div class="routeOutput"><span class="routeSizer" aria-hidden="true">${correctRoute.map((x,n)=>`${n+1}. ${esc(x)}`).join(' → ')}</span><span class="routeValue">${(s.reveal?correctRoute:state.route).map((x,n)=>`${n+1}. ${esc(x)}`).join(' → ')||'1. …'}</span></div><div class="response ${s.reveal?'':'neutral'}">${s.reveal?'First → Then → Finally · חזרו לפסקה B ובדקו.':'הסדר שבחרתם יופיע כאן. הפתרון בשקף הבא.'}</div><button id="resetRoute" ${s.reveal?'disabled':''}>איפוס הבחירה</button>`;
else if(s.kind==='pause')c=`<h2 dir="ltr">${esc(s.title)}</h2><img src="assets/train-umbrella.png" alt="איור משעשע: מטרייה ענקית מגינה על רכבת בגשם"><p class="sub">${esc(s.sub)}</p>`;
else if(s.kind==='links')c=`${title}<h2>${esc(s.sub)}</h2><div class="linkrow"><a href="https://englishfornoar.co.il/band-ii/groups/group-01.html" target="_blank" rel="noopener">תרגול קבוצה 01</a><a href="files/the-same-way-worksheet.pdf" target="_blank" rel="noopener">הסיפור והמשימות</a><a href="../../to-be/" target="_blank" rel="noopener">חזרה על To Be</a></div>`;
else c=`${title}${tense}<p class="hero english">${esc(s.text)}</p><p class="sub">${esc(s.sub)}</p>`;
$('#stage').innerHTML=`<article class="${s.kind}">${c}</article>`;$('#counter').textContent=`${i+1} / ${SLIDES.length}`;$('#prev').disabled=i===0;$('#next').disabled=i===SLIDES.length-1;
const progress=s.progress||0;$('#readLabel').innerHTML=progress?`התקדמות בקריאה: <bdi dir="ltr">${progress} / 28</bdi>`:'לפני הקריאה המודרכת';$('#readBar').style.width=(progress/28*100)+'%';
history.replaceState(null,'','#'+(i+1));try{if(i>0)localStorage.setItem(key,i)}catch(e){}
document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{state.choices[i]=Number(b.dataset.choice);render()});
document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{state.route.push(routeItems[Number(b.dataset.route)]);render()});
if($('#resetRoute'))$('#resetRoute').onclick=()=>{state.route=[];render()};
if($('#startNow'))$('#startNow').onclick=()=>go(1);
if($('#resume'))$('#resume').onclick=()=>{let n=1;try{n=Number(localStorage.getItem(key))||1}catch(e){}go(n)};
}
function go(n){i=Math.max(0,Math.min(SLIDES.length-1,n));render()}
$('#prev').onclick=()=>go(i-1);$('#next').onclick=()=>go(i+1);
document.addEventListener('keydown',e=>{if($('#menu').open)return;if(e.target.closest('button,a')&&(e.key===' '||e.key==='Enter'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}if(e.key==='Home')go(0);if(e.key==='End')go(SLIDES.length-1)});
$('#stage').addEventListener('wheel',e=>{const el=$('#stage');if(el.scrollHeight>el.clientHeight+4){if(e.deltaY>0&&el.scrollTop+el.clientHeight<el.scrollHeight-3)return;if(e.deltaY<0&&el.scrollTop>3)return;}e.preventDefault();if(Date.now()-lastWheel<500)return;lastWheel=Date.now();go(i+(e.deltaY>0?1:-1))},{passive:false});
let touch=null;$('#stage').addEventListener('touchstart',e=>{if(e.target.closest('button,a'))return;touch={x:e.touches[0].clientX,y:e.touches[0].clientY}},{passive:true});$('#stage').addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;touch=null;if(Math.max(Math.abs(dx),Math.abs(dy))<70)return;if(Math.abs(dx)>Math.abs(dy))go(i+(dx<0?1:-1));else if($('#stage').scrollHeight<=$('#stage').clientHeight+4)go(i+(dy<0?1:-1))},{passive:true});
$('#menuBtn').onclick=()=>{readerFrame?.contentWindow.readAlong?.pause();$('#menu').showModal();};$('#closeMenu').onclick=()=>$('#menu').close();$('#restart').onclick=()=>{state.route=[];state.choices={};$('#menu').close();go(0)};
$('#fullBtn').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.();
const stops=[{label:'פתיחה',n:0},{label:'הסיפור המלא',n:1},{label:'Read Alone Text · קריאה והאזנה',n:SLIDES.findIndex(s=>s.kind==='readalong')},{label:'חיבור ל־To Be ולאוצר המילים',n:SLIDES.findIndex(s=>s.kind==='bridge')}];for(const p of pmap){stops.push({label:`פסקה ${p}`,n:SLIDES.findIndex(s=>s.kind==='sentence'&&s.part===p)})}stops.push({label:'משימת הדף',n:SLIDES.findIndex(s=>s.kind==='work')},{label:'בדיקת יציאה',n:SLIDES.findIndex(s=>s.kind==='exit')});
$('#contents').innerHTML=stops.map(x=>`<button data-go="${x.n}">${x.label}</button>`).join('');document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{$('#menu').close();go(Number(b.dataset.go))});
window.lesson={go,slides:SLIDES,state};render();
})();
