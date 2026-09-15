const deck=document.getElementById('deck');
const origin=new URL('.',document.currentScript.src);
const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const familyNames={contrast:'ניגוד',addition:'תוספת',cause:'סיבה',result:'תוצאה',example:'הדגמה',sequence:'סדר פעולות',purpose:'מטרה'};
const translation=(s,html)=>`<div class="translation ${s.reveal?'revealed':''}" dir="rtl" aria-hidden="${!s.reveal}">${html}</div>`;
deck.innerHTML=slides.map((s,i)=>{
 const common=`id="s${i+1}" class="slide ${s.kind} ${s.family||''}" ${s.pair?`data-pair="${s.pair}"`:''} hidden aria-label="שקף ${i+1}"`;
 const heading=`<div class="heading"><p class="eyebrow">${familyNames[s.family]||'CONNECTORS'}</p><h2 dir="${s.kind==='example'||s.kind==='practice'?'ltr':'rtl'}">${esc(s.title)}</h2></div>`;
 if(s.kind==='cover')return `<section ${common}><div class="content cover-content"><p class="eyebrow">ENGLISH FOR NOAR</p><h1 lang="en" dir="ltr">Connectors</h1>${translation(s,'<p class="cover-he">מילות קישור</p>')}<div class="cover-words" dir="ltr"><span>BUT</span><span>AND</span><span>BECAUSE</span></div></div></section>`;
 if(s.kind==='idea')return `<section ${common}><img class="idea-image" src="${new URL('assets/'+s.image+'.webp',origin)}" alt="" loading="lazy"><div class="idea-shade"></div><div class="idea-copy"><p class="eyebrow">${familyNames[s.family]}</p><h2 dir="ltr" lang="en">${esc(s.en)}</h2></div></section>`;
 if(s.kind==='explain')return `<section ${common}><div class="content">${heading}<p class="explanation" dir="rtl">${esc(s.body)}</p>${s.formula?`<div class="formula" lang="en" dir="ltr">${s.formula}</div>`:''}${s.note?`<p class="rule">${esc(s.note)}</p>`:''}</div></section>`;
 if(s.kind==='summary')return `<section ${common}><div class="content">${heading}<table><tbody>${s.rows.map(r=>`<tr><th dir="ltr" lang="en">${esc(r[0])}</th><td class="translation ${s.reveal?'revealed':''}" aria-hidden="${!s.reveal}" dir="rtl">${esc(r[1])}</td><td dir="ltr" lang="en">${esc(r[2])}</td></tr>`).join('')}</tbody></table><p class="rule">${esc(s.note)}</p></div></section>`;
 if(s.kind==='practice')return `<section ${common}><div class="content">${heading}<p class="prompt" dir="rtl">${esc(s.prompt)}</p><p class="tense">${esc(s.tense)}</p><div class="sentence question" lang="en" dir="ltr">${esc(s.question)}</div><div class="solution ${s.answerVisible?'revealed':''}" aria-hidden="${!s.answerVisible}"><div class="answer" dir="ltr" lang="en">${s.answer}</div><p class="rule">${esc(s.why)}</p></div>${translation(s,`<p class="meaning">${esc(s.he)}</p>`)}</div></section>`;
 return `<section ${common}><div class="content">${heading}${s.base?`<p class="base" dir="ltr" lang="en">${esc(s.base)}</p>`:''}<p class="tense">${esc(s.tense)}</p><div class="sentence" dir="ltr" lang="en">${s.sentence}</div>${translation(s,`${s.meaning?`<p class="word-meaning">${esc(s.meaning)}</p>`:''}<p class="meaning">${esc(s.he)}</p>`)}</div></section>`;
}).join('');
const all=[...deck.children],jump=document.getElementById('jump'),prev=document.getElementById('prev'),next=document.getElementById('next');
let currentChapter='';
jump.innerHTML=slides.map((s,i)=>{
 let group='';
 if(s.chapter!==currentChapter){group=(i?'</optgroup>':'')+`<optgroup label="${esc(s.chapter)}">`;currentChapter=s.chapter;}
 return group+`<option value="${i}">${i+1} / ${slides.length} · ${esc(s.title||s.en)}</option>`;
}).join('')+'</optgroup>';
let at=0;
function fit(){
 const slide=all[at],content=slide.querySelector('.content');
 if(!content)return;
 content.style.removeProperty('--fit');
 const css=getComputedStyle(slide);
 const available=slide.clientHeight-parseFloat(css.paddingTop)-parseFloat(css.paddingBottom);
 const scale=Math.min(1,available/content.offsetHeight,slide.clientWidth*.9/content.scrollWidth);
 content.style.setProperty('--fit',String(scale));
}
function show(n,write=true){
 n=Math.max(0,Math.min(all.length-1,Number.isFinite(n)?n:0));
 all[at].hidden=true;all[at].querySelectorAll('audio,video').forEach(m=>m.pause());
 at=n;all[at].hidden=false;jump.value=String(at);prev.disabled=at===0;next.disabled=at===all.length-1;
 document.getElementById('progress').style.width=((at+1)/all.length*100)+'%';
 fit();
 if(write)history.replaceState(null,'','#'+(at+1));
}
prev.onclick=()=>show(at-1);next.onclick=()=>show(at+1);jump.onchange=()=>show(Number(jump.value));
window.addEventListener('hashchange',()=>show(parseInt(location.hash.slice(1),10)-1,false));
window.addEventListener('resize',fit);
document.fonts.ready.then(fit);
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
deck.addEventListener('touchend',e=>{if(!touch||!e.changedTouches.length)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;touch=null;if(Math.max(Math.abs(dx),Math.abs(dy))<48)return;show(at+(Math.abs(dy)>Math.abs(dx)?(dy<0?1:-1):(dx<0?1:-1)));},{passive:true});
deck.addEventListener('touchcancel',()=>touch=null,{passive:true});
document.getElementById('full').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{}};
show(parseInt(location.hash.slice(1),10)-1,false);
