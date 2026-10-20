(() => {
'use strict';
const stage=document.querySelector('.stage');
const switches=[...stage.querySelectorAll('.word-switch[data-phrase]')];
const byPhrase=new Map();
for(const el of switches){const key=el.dataset.phrase;if(!byPhrase.has(key))byPhrase.set(key,[]);byPhrase.get(key).push(el);}
const words=s=>(s.match(/[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*/g)||[]).length;
function cleanText(el){const clone=el.cloneNode(true);clone.querySelectorAll('[hidden],.magic-essay-control').forEach(e=>e.remove());return clone.textContent;}
function counts(){
 document.querySelectorAll('.slide .count:not(#draft-count)').forEach(count=>{
  const slide=count.closest('.slide'),regions=[...slide.querySelectorAll('.essay.en > p,.main-copy.en')];
  const n=regions.reduce((sum,p)=>sum+words(cleanText(p)),0);
  let label=`${n} words`;
  if(count.hasAttribute('data-full-count'))label+=n<120||n>140?' · outside the 120–140 exam range':' · exam range: 120–140';
  if(count.textContent!==label)count.textContent=label;
  count.classList.toggle('outside',count.hasAttribute('data-full-count')&&(n<120||n>140));
 });
}
function synchronize(source){
 const choices=JSON.parse(source.dataset.options),index=Number(source.dataset.choice||0)%choices.length;
 for(const el of byPhrase.get(source.dataset.phrase)||[]){
  if(el.dataset.choice!==String(index))el.dataset.choice=String(index);
  if(el.textContent!==choices[index])el.textContent=choices[index];
  el.setAttribute('aria-label',choices[index]+' — click for another wording');
 }
}
const phrasingObserver=new MutationObserver(records=>{
 const changed=new Set();for(const record of records){const el=(record.target.nodeType===1?record.target:record.target.parentElement).closest('.word-switch[data-phrase]');if(el)changed.add(el)}
 changed.forEach(synchronize);counts();
});
for(const el of switches){
 phrasingObserver.observe(el,{subtree:true,childList:true,attributes:true,attributeFilter:['data-choice']});
 el.addEventListener('click',()=>{const options=JSON.parse(el.dataset.options);el.dataset.choice=String((Number(el.dataset.choice||0)+1)%options.length);synchronize(el);counts();});
 el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();el.click();}});
}
// The optional transition appears only with the opening paragraph and full essay.
const choices=[['In the following essay,','In this essay,'],['I will explain','I will show','I will make clear'],['opinion','idea','understanding']];
const positions=[0,0,0],places=[];let enabled=false;
function updateOptional(){for(const {sentence,parts,button} of places){sentence.hidden=!enabled;parts.forEach((part,i)=>part.textContent=choices[i][positions[i]]+(i===2?'.':''));button.setAttribute('aria-pressed',String(enabled));}counts();}
for(const slide of document.querySelectorAll('.slide.essay')){
 const paragraphs=[...slide.querySelectorAll('.essay.en > p')];
 const opening=slide.querySelector('.paragraph-square.current b')?.textContent==='1';
 if(!paragraphs.length||(!opening&&paragraphs.length!==4))continue;
 const sentence=document.createElement('span');sentence.className='magic-essay-sentence';sentence.hidden=true;sentence.append(' ');
 const parts=choices.map((options,i)=>{
  const part=document.createElement('span');part.className='magic-essay-part';part.tabIndex=0;part.setAttribute('role','button');part.title='Click for another wording';
  part.setAttribute('aria-label',['Alternative introduction','Alternative verb phrase','Opinion, idea or understanding'][i]);
  part.addEventListener('click',()=>{positions[i]=(positions[i]+1)%options.length;updateOptional()});
  part.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();part.click()}});return part;
 });
 sentence.append(parts[0],' ',parts[1],' my ',parts[2]);
 const button=document.createElement('button');button.className='magic-essay-control';button.type='button';button.textContent='✨';button.title='Optional sentence';button.setAttribute('aria-label','Optional sentence');button.setAttribute('aria-pressed','false');
 button.addEventListener('click',()=>{enabled=!enabled;updateOptional()});paragraphs[0].append(sentence,button);places.push({sentence,parts,button});
}
const menu=document.querySelector('#slide-menu');
function reflectSlide(){const active=document.querySelector('.slide.active');if(!active)return;menu.value=active.dataset.slide;document.title=`${window.REWARDS_UI.slides[+active.dataset.slide-1]} · ${window.REWARDS_ESSAY.format} · Rewards at Home`;}
menu.addEventListener('change',()=>{location.hash='slide-'+menu.value});
const slideObserver=new MutationObserver(reflectSlide);document.querySelectorAll('.slide').forEach(s=>slideObserver.observe(s,{attributes:true,attributeFilter:['class','hidden']}));
// A reading gesture that reaches the end must not become a navigation gesture.
let start=null;
stage.addEventListener('touchstart',e=>{const slide=document.querySelector('.slide.active');start=e.touches.length===1&&slide&&!e.target.closest('textarea,input,button,a,select,summary,[role="button"]')?{x:e.touches[0].clientX,y:e.touches[0].clientY,scrollable:slide.scrollHeight>slide.clientHeight+2,top:slide.scrollTop<=2,bottom:slide.scrollTop+slide.clientHeight>=slide.scrollHeight-2}:null},{passive:true,capture:true});
stage.addEventListener('touchmove',e=>{if(e.touches.length!==1)start=null},{passive:true,capture:true});
stage.addEventListener('touchend',e=>{
 e.stopImmediatePropagation();if(!start||!e.changedTouches.length)return;const began=start;start=null;
 const dx=e.changedTouches[0].clientX-began.x,dy=e.changedTouches[0].clientY-began.y;
 if(Math.abs(dy)<55||Math.abs(dy)<=Math.abs(dx))return;
 if(!began.scrollable||(dy<0&&began.bottom)||(dy>0&&began.top)){const button=document.querySelector('[data-step="'+(dy<0?'1':'-1')+'"]');if(!button.disabled)button.click();}
},{passive:true,capture:true});
stage.addEventListener('touchcancel',()=>{start=null},{passive:true,capture:true});
stage.addEventListener('wheel',e=>{const slide=document.querySelector('.slide.active');if(!e.ctrlKey&&slide&&slide.scrollHeight>slide.clientHeight+2)e.stopImmediatePropagation()},{passive:true,capture:true});
const draft=document.querySelector('#own-draft'),draftKey='essay-draft:'+location.pathname;
try{draft.value=localStorage.getItem(draftKey)||''}catch{}
function draftCount(){document.querySelector('#draft-count').textContent=`${words(draft.value)} words · exam range: 120–140`;}
draft.addEventListener('input',()=>{draftCount();try{localStorage.setItem(draftKey,draft.value)}catch{}});
updateOptional();reflectSlide();draftCount();
})();
