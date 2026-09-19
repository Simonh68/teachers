(()=>{'use strict';
const $=s=>document.querySelector(s),audio=$('#audio');
let data,words=[],sentenceNodes=[],wordNodes=[],activeWord=-1,activeSentence=-1,repeatEnd=null,raf=0,tooltipUnit=null,pageIndex=0;
const tooltip=$('#unitTooltip');
$('.reader').append($('.below'));
$('.reader').addEventListener('scroll',hideTooltip,{passive:true});
function notifyPage(){window.dispatchEvent(new CustomEvent('reader-page',{detail:{page:pageIndex}}));}
function hideTooltip(){if(tooltipUnit)tooltipUnit.removeAttribute('aria-describedby');tooltipUnit=null;tooltip.hidden=true;}
function showTooltip(unit){
  if(tooltipUnit&&tooltipUnit!==unit)tooltipUnit.removeAttribute('aria-describedby');
  tooltipUnit=unit;tooltip.textContent=unit.dataset.translation;tooltip.hidden=false;unit.setAttribute('aria-describedby','unitTooltip');
  const rect=unit.getBoundingClientRect(),box=tooltip.getBoundingClientRect();
  const left=Math.max(8,Math.min(innerWidth-box.width-8,rect.left+(rect.width-box.width)/2));
  const top=rect.top-box.height-10>=8?rect.top-box.height-10:rect.bottom+10;
  tooltip.style.left=left+'px';tooltip.style.top=top+'px';
}
document.addEventListener('pointerdown',e=>{if(!e.target.closest('.unit'))hideTooltip();});
document.addEventListener('keydown',e=>{if(e.key==='Escape')hideTooltip();});
window.addEventListener('scroll',()=>{if(tooltipUnit&&tooltipUnit.matches(':hover'))showTooltip(tooltipUnit);else hideTooltip();},{passive:true});window.addEventListener('resize',hideTooltip);

function setPage(n,manual=false){
  if(!data)return;n=Math.max(0,Math.min(data.pages.length-1,n));
  hideTooltip();pageIndex=n;
  document.querySelectorAll('#story > p').forEach((p,i)=>p.hidden=i!==n);
  const image=document.createElement('img');image.src=data.pages[n].image;image.alt=data.pages[n].title+' — תמונה להמחשת הסיפור';image.width=1536;image.height=1024;$('#scene').replaceChildren(image);$('#pageTitle').textContent=data.pages[n].title;$('#pageNumber').textContent=`דף ${n+1} מתוך ${data.pages.length}`;
  $('#previousPage').disabled=n===0;$('#nextPage').disabled=n===data.pages.length-1;
  const t=$('#translation').children;for(let i=0;i<t.length;i++)t[i].hidden=i!==n;
  notifyPage();
  if(manual){audio.pause();repeatEnd=null;audio.currentTime=Math.max(0,data.sentences.find(s=>s.paragraph===n).start-.06);sync();$('#status').textContent='לחצו על הקראה';}
}
$('#previousPage').onclick=()=>setPage(pageIndex-1,true);$('#nextPage').onclick=()=>setPage(pageIndex+1,true);
document.addEventListener('keydown',e=>{if(e.target.closest('button,input,select,.unit'))return;if(['ArrowRight','ArrowDown'].includes(e.key)){e.preventDefault();setPage(pageIndex+1,true);}if(['ArrowLeft','ArrowUp'].includes(e.key)){e.preventDefault();setPage(pageIndex-1,true);}});
let touchStart=null;$('.reader').addEventListener('touchstart',e=>{if(e.target.closest('button,input,select,.unit'))return;touchStart={x:e.touches[0].clientX,y:e.touches[0].clientY};},{passive:true});$('.reader').addEventListener('touchend',e=>{if(!touchStart)return;const dx=e.changedTouches[0].clientX-touchStart.x,dy=e.changedTouches[0].clientY-touchStart.y;touchStart=null;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy))setPage(pageIndex+(dx<0?1:-1),true);},{passive:true});
const clock=t=>`${Math.floor((t||0)/60)}:${String(Math.floor((t||0)%60)).padStart(2,'0')}`;
function sync(){
  const t=audio.currentTime;
  if(repeatEnd!==null&&t>=repeatEnd){audio.pause();repeatEnd=null;}
  let wi=-1,si=-1,read=0;
  for(let i=0;i<words.length;i++){if(t>=words[i].start){read=i+1;si=words[i].sentence;}if(t>=words[i].start&&t<words[i].end)wi=i;}
  if(!audio.paused){let target=0;for(const s of data.sentences)if(t>=s.start-.08)target=s.paragraph;if(target!==pageIndex)setPage(target);}
  if(audio.ended){wi=-1;si=-1;read=words.length;}
  if(wi!==activeWord){if(activeWord>=0)wordNodes[activeWord].classList.remove('current');if(wi>=0)wordNodes[wi].classList.add('current');activeWord=wi;if(wi>=0&&!audio.paused&&$('#followScroll').checked){const r=wordNodes[wi].getBoundingClientRect(),playerTop=$('.player').getBoundingClientRect().top;const bottom=Math.min(innerHeight-20,playerTop-20);if(r.top<20||r.bottom>bottom)wordNodes[wi].scrollIntoView({block:'center',behavior:'instant'});}}
  if(si!==activeSentence){if(activeSentence>=0)sentenceNodes[activeSentence].classList.remove('active');if(si>=0)sentenceNodes[si].classList.add('active');activeSentence=si;}
  $('#elapsed').textContent=clock(t);$('#seek').value=t;
  $('#progress').innerHTML=`<bdi>${read} / ${words.length}</bdi> מילים · <bdi>${Math.round(read/words.length*100)}%</bdi>`;
  $('#seek').setAttribute('aria-valuetext',`${clock(t)} מתוך ${clock(audio.duration)}`);
}
function frame(){sync();if(!audio.paused)raf=requestAnimationFrame(frame);}
async function play(){try{await audio.play();}catch(e){$('#status').textContent='לא ניתן לנגן כרגע. נסו שוב או פתחו את קובץ ההקראה.';}}
function sentenceAt(){return activeSentence>=0&&data.sentences[activeSentence].paragraph===pageIndex?activeSentence:data.sentences.findIndex(s=>s.paragraph===pageIndex);}
async function repeatSentence(i){const s=data.sentences[i];repeatEnd=s.end+.12;audio.currentTime=Math.max(0,s.start-.06);sync();await play();}
$('#play').onclick=()=>{if(!audio.paused)audio.pause();else{repeatEnd=null;if(audio.ended)audio.currentTime=0;play();}};
$('#restart').onclick=()=>{repeatEnd=null;setPage(0);audio.currentTime=0;sync();play();};
$('#repeat').onclick=()=>repeatSentence(sentenceAt());
// One preference shared by Teachers reading presentations on this browser.
const speedKey='teachers-read-alone-speed-v1',allowedSpeeds=[1,.75,.5,.35,.25];
let preferredSpeed=.75;
try{const saved=Number(localStorage.getItem(speedKey));if(allowedSpeeds.includes(saved))preferredSpeed=saved;}catch(e){}
function applySpeed(value){const speed=allowedSpeeds.includes(value)?value:.75;audio.defaultPlaybackRate=speed;audio.playbackRate=speed;audio.preservesPitch=true;$('#speed').value=String(speed);}
applySpeed(preferredSpeed);
$('#speed').onchange=e=>{const speed=Number(e.target.value);applySpeed(speed);try{localStorage.setItem(speedKey,String(audio.playbackRate));}catch(e){}};
$('#seek').oninput=e=>{repeatEnd=null;audio.currentTime=Number(e.target.value);let target=0;for(const s of data.sentences)if(audio.currentTime>=s.start-.08)target=s.paragraph;setPage(target);sync();};
audio.addEventListener('play',()=>{$('#play').textContent='❚❚ השהיה';$('#status').textContent='מקשיבים וקוראים';cancelAnimationFrame(raf);frame();});
audio.addEventListener('pause',()=>{cancelAnimationFrame(raf);$('#play').textContent='▶ המשך';$('#status').textContent=audio.ended?'הקריאה הושלמה':'מושהה';sync();});
audio.addEventListener('ended',()=>{repeatEnd=null;$('#play').textContent='▶ שוב מההתחלה';$('#status').textContent='הקריאה הושלמה';sync();});
audio.addEventListener('timeupdate',sync);audio.addEventListener('seeked',sync);
audio.addEventListener('loadedmetadata',()=>{$('#duration').textContent=clock(audio.duration);$('#seek').max=audio.duration;$('#seek').disabled=false;});
audio.addEventListener('waiting',()=>{$('#status').textContent='טוען אודיו…';});
audio.addEventListener('playing',()=>{$('#status').textContent='מקשיבים וקוראים';});
audio.addEventListener('error',()=>{$('#status').textContent='האודיו לא נטען. רעננו את העמוד ונסו שוב.';});
window.addEventListener('pagehide',()=>audio.pause());
document.addEventListener('visibilitychange',()=>{if(document.hidden)audio.pause();});
$('#translate').onclick=()=>{const open=$('#translation').hidden;$('#translation').hidden=!open;$('#translate').setAttribute('aria-expanded',String(open));$('#translate').textContent=open?'הסתרת התרגום':'הצגת תרגום לעברית';};
$('#check').onclick=()=>{const answer=$('input[name=answer]:checked');$('#feedback').textContent=!answer?'בחרו תשובה לפני הבדיקה.':answer.value==='class'?'נכון. התיק הירוק נמצא בכיתה — והילדים מהרכבת הם חבריו לכיתה.':'קראו שוב את הפסקה האחרונה. היכן דן פותח את הדלת?';};
async function init(){try{
  const response=await fetch('reading.json?v=reading-prefs-4');if(!response.ok)throw Error('Reading unavailable');data=await response.json();
  $('#wordCount').textContent=`${data.wordCount} מילים`;$('#story').textContent='';let paragraph=-1,p;
  data.sentences.forEach((s,i)=>{if(s.paragraph!==paragraph){p=document.createElement('p');$('#story').append(p);paragraph=s.paragraph;}
    const node=document.createElement('span');node.className='sentence';let wordInSentence=0;
    s.units.forEach((u,ui)=>{const unit=document.createElement('span');unit.className='unit';unit.tabIndex=0;unit.setAttribute('role','button');unit.setAttribute('aria-label',`${u.text} — הצגת תרגום`);unit.dataset.translation=u.translation;
      u.text.split(' ').forEach((text,j)=>{const w=s.words[wordInSentence++];if(w.word!==text)throw Error('Translation unit mismatch');const span=document.createElement('span');span.className='word';span.textContent=text;span.dataset.index=words.length;unit.append(span);if(j<u.text.split(' ').length-1)unit.append(' ');words.push({...w,sentence:i});wordNodes.push(span);});
      unit.onpointerenter=e=>{if(e.pointerType!=='touch')showTooltip(unit);};unit.onpointermove=e=>{if(e.pointerType!=='touch'&&tooltip.hidden)showTooltip(unit);};unit.onpointerleave=e=>{if(e.pointerType!=='touch')hideTooltip();};unit.onfocus=()=>showTooltip(unit);unit.onblur=hideTooltip;unit.onclick=()=>showTooltip(unit);unit.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showTooltip(unit);}};
      node.append(unit);if(ui<s.units.length-1)node.append(' ');
    });
    const replay=document.createElement('button');replay.className='sentence-play';replay.textContent='▶';replay.setAttribute('aria-label',`השמעת משפט ${i+1}: ${s.text}`);replay.onclick=()=>{hideTooltip();repeatSentence(i);};node.append(' ',replay);
    p.append(node,' ');sentenceNodes.push(node);
  });
  for(const part of [...new Set(data.sentences.map(s=>s.paragraph))]){const p=document.createElement('p');p.textContent=data.sentences.filter(s=>s.paragraph===part).map(s=>s.translation).join(' ');$('#translation').append(p);}
  audio.preservesPitch=true;audio.src=data.audio;['play','restart','repeat'].forEach(id=>$('#'+id).disabled=false);$('#status').textContent='לחצו על הקראה';setPage(0);sync();
}catch(e){$('#story').textContent='הקטע לא נטען. רעננו את העמוד כדי לנסות שוב.';$('#status').textContent='שגיאה בטעינה';}}
window.readAlong={setPage:(n)=>setPage(n,true),pause:()=>audio.pause(),get page(){return pageIndex;},get data(){return data;}};
init().then(()=>window.dispatchEvent(new Event('reader-ready')));
})();
