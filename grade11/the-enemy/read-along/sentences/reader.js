'use strict';
const app=document.querySelector('#app');
const audio=new Audio();
audio.preload='metadata';
const $=s=>app.querySelector(s);
const escapeText=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const label=i=>String(i+1).padStart(2,'0');
const state={page:'menu',part:0,index:0,translated:false};
const languageButton=document.querySelector('#hebrew-mode');
const languageKey='teachers.the-enemy.hebrew';
let savedLanguage=null;
try{savedLanguage=localStorage.getItem(languageKey)}catch{}
const initialLink=new URLSearchParams(location.search);
let hebrewEnabled=savedLanguage==='on' ||
  (savedLanguage===null && initialLink.get('he')==='1' && initialLink.has('sentence'));

function rememberLanguage(){
  try{localStorage.setItem(languageKey,hebrewEnabled?'on':'off')}catch{}
}
if(savedLanguage===null && hebrewEnabled)rememberLanguage();
languageButton.setAttribute('aria-pressed',String(hebrewEnabled));
languageButton.addEventListener('click',()=>{
  hebrewEnabled=!hebrewEnabled;
  rememberLanguage();
  languageButton.setAttribute('aria-pressed',String(hebrewEnabled));
  if(state.page==='prep')prep();
  if(state.page!=='read'||!$('.sentence'))return;
  if(!hebrewEnabled){
    state.translated=false;
    $('.translation').textContent='';
    $('.meaning').textContent='';
    const url=new URL(location.href);
    url.searchParams.delete('he');
    history.replaceState(null,'',url);
  }
  updateGlosses();
});

const chapters=new Map();
const pendingChapters=new Map();
let data, activeTrack='', requested=false, engaged=false, speed=.75, automatic=true;
let timer=0,frame=0,epoch=0,lastWord=-1,wordNodes=[];
function loadText(part){
  if(!pendingChapters.has(part)){
    const request=fetch('sentences/part-'+(part+1)+'.json')
      .then(response=>{
        if(!response.ok)throw Error('Could not load chapter');
        return response.json();
      })
      .then(chapter=>{chapters.set(part,chapter);return chapter})
      .finally(()=>pendingChapters.delete(part));
    pendingChapters.set(part,request);
  }
  return pendingChapters.get(part);
}
function currentChecks(){return state.part===0?checks:data.checks}
function partHeading(){return 'Part '+label(state.part)+' · '+parts[state.part].title}
function action(name,content,cls='',more=''){
  const remoteStep={next:1,back:-1}[name] || (name==='begin'&&state.page==='prep' || state.page==='finish'&&['next-part','parts'].includes(name) ? 1 : 0);
  if(remoteStep)more+=' data-step="'+remoteStep+'"';
  if(name==='hint')more+=' data-reveal="answer"';
  return '<button type="button" class="'+cls+'" data-action="'+name+'" '+more+'>'+content+'</button>'}
function stop(){
  epoch++;requested=false;clearTimeout(timer);cancelAnimationFrame(frame);audio.pause();
}
function go(page,part=state.part,index=state.index,translated=false,historyMode='pushState'){
  stop();Object.assign(state,{page,part,index,translated});const u=new URL(location.href);u.hash='';u.search='';
  if(page!=='menu')u.searchParams.set('part',part+1);
  if(['read','check'].includes(page))u.searchParams.set('sentence',index+1);
  if(page==='check'||page==='finish')u.searchParams.set('view',page);
  if(page==='read'&&translated)u.searchParams.set('he','1');
  if(historyMode)history[historyMode](null,'',u);
  render();window.scrollTo(0,0);app.focus({preventScroll:true});
}
function readLocation(){
  const q=new URLSearchParams(location.search);
  const p=Number(q.get('part'))-1,idx=Number(q.get('sentence'))-1;
  if(!Number.isInteger(p)||p<0||p>4)return go('menu',0,0,false,null);
  if(q.get('view')==='finish')return go('finish',p,0,false,null);
  if(q.has('sentence')&&Number.isInteger(idx)&&idx>=0)return go(q.get('view')==='check'?'check':'read',p,idx,hebrewEnabled && q.get('he')==='1',null);
  go('prep',p,0,false,null);
}
function schedule(){
  clearTimeout(timer);
  if(engaged&&automatic&&state.page==='read')timer=setTimeout(()=>startAudio(),4000);
}
function menu(){
  app.innerHTML='<div class="intro"><div><div class="eyebrow">Pearl S. Buck</div><h1>The Enemy</h1><p class="subtitle">Five-part Read-Along</p></div><figure class="photo"><img src="sentences/media/shore.jpg" alt="Pine-covered rocks along the Japanese coast at Jōdogahama"><figcaption>Jōdogahama · <a href="https://commons.wikimedia.org/wiki/File:Jyoudogahama.jpg">Junpei Satoh</a> · <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a></figcaption></figure></div><div class="menu">'+parts.map((p,i)=>action('part','<span class="part-number">'+label(i)+'</span><span><span class="part-title">'+p.title+'</span><span class="part-status">'+('Preparation &amp; sentence-by-sentence reading')+'</span></span><span aria-hidden="true">↗</span>','part-row','data-part="'+i+'"')).join('')+'</div>';
}
function prep(){
  const p=parts[state.part];
  app.innerHTML='<section class="prep"><div class="eyebrow">Part '+label(state.part)+' · Listening preparation</div><h2>'+p.title+'</h2><p class="lead">'+p.intro+'</p><div class="group"><h3>Words to listen for</h3><div class="chips">'+p.words.map(([w,h],i)=>hebrewEnabled?action('vocab',w+'<small dir="rtl" lang="he" hidden>'+h+'</small>','chip','aria-expanded="false" data-word="'+i+'"'):'<span class="vocab-label">'+escapeText(w)+'</span>').join('')+'</div></div><div class="group"><h3>Listen for this</h3><p class="prompt">'+p.focus+'</p></div><div class="reveal prep-cards" id="prep-he" lang="he" dir="rtl" '+(hebrewEnabled?'':'hidden')+'><strong>'+p.he+'</strong><p>'+p.introHe+'</p><p>'+p.focusHe+'</p></div><div class="footnav">'+action('begin','Start reading · Part '+(state.part+1),'primary')+(state.part<4?action('next-part','Prepare Part '+(state.part+2)+' →','minor'):'')+'</div></section>';
}
function reader(){
  state.index=Math.min(state.index,data.rows.length-1);
  const s=data.rows[state.index],num=state.index+1;

  const options=data.rows.map((_,i)=>'<option value="'+i+'" '+(i===state.index?'selected':'')+'>Sentence '+(i+1)+'</option>').join('');
  app.innerHTML='<section class="reader"><div class="bar"><span class="eyebrow">'+partHeading()+'</span><label class="control-label"><select class="picker" id="jump" aria-label="Go to sentence">'+options+'</select> / '+data.rows.length+'</label></div><div class="progress"><i style="width:'+num/data.rows.length*100+'%"></i></div><p class="sentence '+(s.words.length>25?'long':'')+'" lang="en" dir="ltr">'+s.words.map(([word],i)=>'<span class="word" data-i="'+i+'">'+escapeText(word)+'</span>').join(' ')+'</p><div class="meaning" lang="he" dir="rtl" aria-live="polite"></div><div class="translation" lang="he" dir="rtl">'+(state.translated?escapeText(s.he):'')+'</div><div class="controls">'+action('play','▶ Play','primary','id="play"')+action('replay','↺ Replay','minor')+action('rewind','−15 s','minor','aria-label="Back fifteen seconds"')+'<label class="control-label"><select id="rate" aria-label="Playback speed">'+[.6,.75,1].map(r=>'<option value="'+r+'" '+(r===speed?'selected':'')+'>'+r+'×</option>').join('')+'</select></label><label class="control-label"><input id="auto" type="checkbox" '+(automatic?'checked':'')+'>Auto · 4 s</label></div><p class="status" role="status"></p><div class="footnav">'+action('back','← Back','minor')+action('next','Next →','primary')+'</div></section>';
  wordNodes=[...app.querySelectorAll('.word')];lastWord=-1;
  updateGlosses();
  const file=data.tracks[s.track].file;
  if(activeTrack!==file){activeTrack=file;audio.src='sentences/'+file;audio.load()}
  audio.playbackRate=speed;schedule();
}
function updateGlosses(){
  for(const el of wordNodes){
    const word=el.textContent;
    const key=word.toLowerCase().replace(/^[^a-z]+|[^a-z]+$/g,'');
    const meaning=hebrewEnabled && Object.hasOwn(glossary,key) && glossary[key];
    el.classList.toggle('known',Boolean(meaning));
    if(meaning){
      el.tabIndex=0;
      el.setAttribute('role','button');
      el.dataset.gloss=meaning;
      el.setAttribute('aria-label',word+' — '+meaning);
    }else{
      for(const attr of ['tabindex','role','data-gloss','aria-label'])el.removeAttribute(attr);
    }
  }
}
function checkpoint(){
  const [question,hint,answer]=currentChecks()[state.index+1];
  app.innerHTML='<section class="prep"><div class="eyebrow">Part '+label(state.part)+' · Reading check</div><h2 class="question">'+question+'</h2><div class="actionrow">'+action('hint','⭐','minor','aria-label="Show a hint" aria-expanded="false"')+action('answer','Show answer','minor','aria-expanded="false"')+'</div><p id="hint" class="hint" hidden>'+hint+'</p><p id="answer" class="answer" hidden>'+answer+'</p><div class="footnav">'+action('back','← Back','minor')+action('next',state.index===data.rows.length-1?'Finish Part '+(state.part+1):'Continue reading →','primary')+'</div></section>';
}
function render(){
  window.cur=state.page==='menu'?0:1;
  document.body.dataset.page=state.page;
  document.querySelector('#home').hidden=state.page==='menu';
  if(state.page==='menu')return menu();
  if(state.page==='prep')return prep();
  data=chapters.get(state.part);
  if(!data){
    const part=state.part,key=epoch;
    app.innerHTML='<p role="status">Loading Part '+(part+1)+'…</p>';
    loadText(part).then(()=>{if(key===epoch)render()}).catch(()=>{
      if(key===epoch)app.innerHTML='<p role="alert">The reading could not load.</p>'+action('retry','Try again');
    });
    return;
  }
  state.index=Math.min(state.index,data.rows.length-1);
  if(state.page==='finish'){
    const next=state.part<parts.length-1?action('next-part','Prepare Part '+(state.part+2)+' →','primary'):action('parts','All five parts','primary');
    app.innerHTML='<section class="prep"><div class="eyebrow">Part '+label(state.part)+' · Complete</div><h2>'+parts[state.part].title+'</h2><div class="footnav">'+action('back','← Back','minor')+action('begin','Read Part '+(state.part+1)+' again','minor')+next+'</div></section>';return;
  }
  if(state.page==='check'&&currentChecks()[state.index+1])return checkpoint();
  state.page='read';reader();
}
function syncWords(){
  if(!requested||state.page!=='read')return;
  const s=data.rows[state.index],time=audio.currentTime;
  if(time>=s.end-.012){stop();$('#play').textContent='▶ Play';if(lastWord>=0)wordNodes[lastWord]?.classList.remove('on');lastWord=-1;return}
  const i=s.words.findIndex(([,a,b])=>time>=a&&time<b);
  if(i!==lastWord){if(lastWord>=0)wordNodes[lastWord]?.classList.remove('on');if(i>=0)wordNodes[i].classList.add('on');lastWord=i}
}
function tick(){syncWords();if(requested)frame=requestAnimationFrame(tick)}
async function startAudio(at=null){
  if(state.page!=='read'||!data)return;
  stop();const key=epoch,s=data.rows[state.index];
  requested=true;const play=$('#play');play.textContent='Ⅱ Pause';
  try{
    if(audio.readyState<1)await new Promise((ok,fail)=>{const done=()=>{clean();ok()},bad=()=>{clean();fail(Error('audio'))};function clean(){audio.removeEventListener('loadedmetadata',done);audio.removeEventListener('error',bad)}if(audio.error)return bad();audio.addEventListener('loadedmetadata',done);audio.addEventListener('error',bad)});
    if(key!==epoch)return;
    if(at!==null||audio.currentTime<s.start||audio.currentTime>=s.end-.08||!play.dataset.paused)audio.currentTime=at??s.start;
    delete play.dataset.paused;audio.playbackRate=speed;await audio.play();if(key!==epoch)return;
    $('.status').textContent='';tick();
  }catch(e){if(key===epoch){stop();play.textContent='▶ Play';$('.status').textContent=e.name==='NotAllowedError'?'Tap Play to start the recording.':'Audio could not play. Tap Play to retry.'}}
}
function move(dir){
  const n=state.index;
  const part=state.part;
  if(state.page==='menu'){if(dir>0)go('prep',0);return}
  if(state.page==='prep'){if(dir>0)go('read',part,0);else go('menu');return}
  if(!data)return;
  if(state.page==='finish'){
    if(dir<0)go('check',part,data.rows.length-1);
    else if(part<parts.length-1)go('prep',part+1);
    else go('menu');
    return;
  }
  if(state.page==='check'){
    if(dir<0)go('read',part,n,hebrewEnabled,'replaceState');
    else if(n+1<data.rows.length)go('read',part,n+1,false,'replaceState');
    else go('finish',part);
    return;
  }
  if(state.page!=='read')return;
  if(dir>0){
    if(hebrewEnabled&&!state.translated)go('read',part,n,true,'replaceState');
    else if(currentChecks()[n+1])go('check',part,n,false,'replaceState');
    else if(n+1<data.rows.length)go('read',part,n+1,false,'replaceState');
    else go('finish',part);
  }else if(state.translated)go('read',part,n,false,'replaceState');
  else if(n===0)go('prep',part);
  else if(currentChecks()[n])go('check',part,n-1,false,'replaceState');
  else go('read',part,n-1,hebrewEnabled,'replaceState');
}
function toggle(btn,el){el.hidden=!el.hidden;btn.setAttribute('aria-expanded',String(!el.hidden))}
function showGloss(el){const box=$('.meaning');if(el&&box)box.textContent=el.textContent+' · '+el.dataset.gloss}
app.addEventListener('pointerover',e=>{if(e.pointerType!=='touch')showGloss(e.target.closest('[data-gloss]'))});
app.addEventListener('focusin',e=>showGloss(e.target.closest('[data-gloss]')));
app.addEventListener('click',e=>{
  engaged=true;const word=e.target.closest('[data-gloss]');if(word){showGloss(word);return}
  const b=e.target.closest('[data-action]');if(!b)return;
  switch(b.dataset.action){
    case 'parts':go('menu');break;
    case 'part':go('prep',+b.dataset.part,0);break;
    case 'next-part':go('prep',state.part+1,0);break;
    case 'begin':go('read',state.part,0);break;
    case 'retry':render();break;
    case 'vocab':toggle(b,b.querySelector('small'));break;
    case 'hint':toggle(b,$('#hint'));break;
    case 'answer':toggle(b,$('#answer'));b.textContent=$('#answer').hidden?'Show answer':'Hide answer';break;
    case 'next':move(1);break;
    case 'back':move(-1);break;
    case 'play':if(requested){const wasPlaying=!audio.paused;stop();if(wasPlaying)b.dataset.paused='1';b.textContent='▶ Play'}else startAudio();break;
    case 'replay':startAudio(data.rows[state.index].start);break;
    case 'rewind':{
      const s=data.rows[state.index];const local=(requested||$('#play').dataset.paused)?audio.currentTime:s.start;
      const absolute=Math.max(0,data.tracks[s.track].offset+local-15);
      let i=data.rows.findLastIndex(r=>data.tracks[r.track].offset+r.start<=absolute);i=Math.max(i,0);
      const target=data.rows[i];go('read',state.part,i,state.translated,'replaceState');
      startAudio(Math.min(target.end-.08,Math.max(target.start,absolute-data.tracks[target.track].offset)));break;
    }
  }
});
app.addEventListener('change',e=>{engaged=true;if(e.target.id==='jump')go('read',state.part,Number(e.target.value),false,'replaceState');if(e.target.id==='rate'){speed=Number(e.target.value);audio.playbackRate=speed}if(e.target.id==='auto'){automatic=e.target.checked;clearTimeout(timer);if(automatic&&!requested)schedule()}});
let touch=null;
app.addEventListener('touchstart',e=>{const t=e.touches[0];touch=e.touches.length===1?[t.clientX,t.clientY,scrollY<3,scrollY+innerHeight>=document.documentElement.scrollHeight-3]:null},{passive:true});
app.addEventListener('touchend',e=>{if(!touch)return;const t=e.changedTouches[0],dx=t.clientX-touch[0],dy=t.clientY-touch[1],atTop=touch[2],atBottom=touch[3];touch=null;const vertical=Math.abs(dy)>Math.abs(dx);if(vertical&&document.documentElement.scrollHeight>innerHeight+12){if((dy>0&&!atTop)||(dy<0&&!atBottom))return;}const delta=vertical?dy:dx;if(Math.abs(delta)>65){engaged=true;move(delta<0?1:-1)}},{passive:true});
document.addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||['SELECT','INPUT'].includes(e.target.tagName))return;if(e.target.matches?.('[data-gloss]')&&[' ','Enter'].includes(e.key)){e.preventDefault();showGloss(e.target);return}if(e.target.closest?.('#teachers-qr-remote-host'))return;if(['ArrowDown','ArrowRight','ArrowUp','ArrowLeft'].includes(e.key)){engaged=true;e.preventDefault();move(['ArrowDown','ArrowRight'].includes(e.key)?1:-1)}});
audio.addEventListener('timeupdate',syncWords);
audio.addEventListener('ended',()=>{if(requested){stop();const p=$('#play');if(p)p.textContent='▶ Play'}});
document.querySelector('#home').onclick=()=>{engaged=true;go('menu')};
document.addEventListener('visibilitychange',()=>{if(document.hidden){const p=$('#play');if(requested&&p){p.dataset.paused='1';p.textContent='▶ Play'}stop()}});
window.addEventListener('pagehide',stop);window.addEventListener('popstate',readLocation);
readLocation();
