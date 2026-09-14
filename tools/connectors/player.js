const deck=document.getElementById('deck');
const origin=new URL('.',document.currentScript.src);
const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const familyNames={contrast:'ניגוד',addition:'תוספת',cause:'סיבה'};
deck.innerHTML=slides.map((s,i)=>{
 const common=`id="s${i+1}" class="slide ${s.kind} ${s.family||''}" hidden aria-label="שקף ${i+1}"`;
 if(s.kind==='cover')return `<section ${common}><div class="cover-content"><p class="eyebrow">ENGLISH FOR NOAR</p><h1 lang="en" dir="ltr">Connectors</h1><p class="cover-he">מילות קישור</p><div class="cover-words" dir="ltr"><span>BUT</span><span>AND</span><span>BECAUSE</span></div><p class="classes">${s.sub}</p></div></section>`;
 if(s.kind==='idea')return `<section ${common}><img class="idea-image" src="${new URL('assets/'+s.image+'.webp',origin)}" alt="${esc(s.he)}"><div class="idea-shade"></div><div class="idea-copy"><p class="eyebrow">${familyNames[s.family]}</p><h2 dir="ltr" lang="en">${s.en}</h2><p dir="rtl">${s.he}</p></div></section>`;
 if(s.kind==='summary')return `<section ${common}><div class="content"><h2 class="summary-title">${s.title}</h2><table><tbody>${s.rows.map(r=>`<tr><th dir="ltr">${r[0]}</th><td>${r[1]}</td><td dir="ltr" lang="en">${r[2]}</td></tr>`).join('')}</tbody></table><p class="meaning">${s.he}</p></div></section>`;
 return `<section ${common}><div class="content"><div class="heading"><p class="eyebrow">${familyNames[s.family]}</p><h2 dir="ltr">${s.title}</h2></div><p class="base ${s.base?'':'empty'}" dir="ltr" lang="en">${esc(s.base||'משפט מקור')}</p><p class="tense">${s.tense||''}</p><div class="sentence" dir="ltr" lang="en">${s.sentence}</div>${s.second?`<div class="second sentence" lang="en" dir="ltr">${s.second}</div>`:''}<p class="meaning" dir="rtl">${s.he||''}</p>${s.kind==='practice'?`<div class="answer ${s.answer?'revealed':''}" dir="ltr" lang="en">${s.answer||'&nbsp;'}</div>`:''}<p class="rule" dir="rtl">${s.rule||'&nbsp;'}</p></div></section>`;
}).join('');
const all=[...deck.children],jump=document.getElementById('jump'),prev=document.getElementById('prev'),next=document.getElementById('next');
jump.innerHTML=slides.map((s,i)=>`<option value="${i}">${i+1} / ${slides.length} · ${esc(s.title||s.en)}</option>`).join('');
let at=0;
function show(n,write=true){
 n=Math.max(0,Math.min(all.length-1,Number.isFinite(n)?n:0));
 all[at].hidden=true;all[at].querySelectorAll('audio,video').forEach(m=>m.pause());
 at=n;all[at].hidden=false;jump.value=String(at);prev.disabled=at===0;next.disabled=at===all.length-1;
 document.getElementById('progress').style.width=((at+1)/all.length*100)+'%';
 if(write)history.replaceState(null,'','#'+(at+1));
}
prev.onclick=()=>show(at-1);next.onclick=()=>show(at+1);jump.onchange=()=>show(Number(jump.value));
window.addEventListener('hashchange',()=>show(parseInt(location.hash.slice(1),10)-1,false));
document.addEventListener('keydown',e=>{
 if(e.target.matches('select,input,textarea'))return;
 let n;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key))n=at+1;
 if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key))n=at-1;
 if(e.key==='Home')n=0;if(e.key==='End')n=all.length-1;
 if(n!==undefined){e.preventDefault();show(n);}
});
let wheel=0,last=0;
document.addEventListener('wheel',e=>{if(e.target.closest('select'))return;e.preventDefault();const now=Date.now();if(now-last<650)return;wheel+=e.deltaY;if(Math.abs(wheel)>45){show(at+Math.sign(wheel));wheel=0;last=now;}},{passive:false});
let touch=null;
deck.addEventListener('touchstart',e=>{if(e.touches.length===1)touch={x:e.touches[0].clientX,y:e.touches[0].clientY};else touch=null;},{passive:true});
deck.addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;touch=null;if(Math.max(Math.abs(dx),Math.abs(dy))<48)return;show(at+(Math.abs(dy)>Math.abs(dx)?(dy<0?1:-1):(dx<0?1:-1)));},{passive:true});
deck.addEventListener('touchcancel',()=>touch=null,{passive:true});
document.getElementById('full').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{}};
show(parseInt(location.hash.slice(1),10)-1,false);
