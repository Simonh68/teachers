/* Plain HTML links and checkboxes; this script saves only in this browser. */
(()=>{'use strict';
const KEY='teachers-unit2-meetings-v1';
const idOK=s=>typeof s==='string'&&/^(m[1-9](?:-[a-z-]+)?|unit-(prep|guide))$/.test(s);
const blank=()=>({version:1,opened:{},completed:{},ready:{},lastOpened:'',expanded:''});
let state=blank(),storageAvailable=true;
function read(){
 if(!storageAvailable)return state;
 let raw;try{raw=localStorage.getItem(KEY);}catch(e){storageAvailable=false;return state;}
 if(!raw)return blank();
 try{const saved=JSON.parse(raw),out=blank();if(!saved||saved.version!==1)return out;
  for(const field of ['opened','completed','ready'])if(saved[field]&&typeof saved[field]==='object')for(const [id,value] of Object.entries(saved[field]))if(idOK(id)&&value===true)out[field][id]=true;
  if(idOK(saved.lastOpened))out.lastOpened=saved.lastOpened;
  if(/^m[1-9]$/.test(saved.expanded||''))out.expanded=saved.expanded;
  return out;
 }catch(e){return blank();}
}
state=read();
function persist(){try{localStorage.setItem(KEY,JSON.stringify(state));storageAvailable=true;}catch(e){storageAvailable=false;}render();}
function update(fn){state=read();fn(state);persist();}
function completedFor(meeting){const boxes=[...meeting.querySelectorAll('[data-complete]')];return {boxes,done:boxes.filter(b=>state.completed[b.dataset.complete]).length};}
function render(){
 for(const box of document.querySelectorAll('[data-complete]')){box.checked=!!state.completed[box.dataset.complete];box.closest('.activity').classList.toggle('is-completed',box.checked);}
 for(const box of document.querySelectorAll('[data-ready]')){box.checked=!!state.ready[box.dataset.ready];box.closest('.prep-card').classList.toggle('is-ready',box.checked);}
 for(const link of document.querySelectorAll('[data-open-id]')){const id=link.dataset.openId,opened=!!state.opened[id];link.classList.toggle('was-opened',opened);const badge=document.querySelector('[data-open-status="'+id+'"]');if(badge){badge.hidden=!opened;badge.textContent=id===state.lastOpened?'Last opened':'Opened';}link.closest('.activity')?.classList.toggle('last-opened',id===state.lastOpened);}
 let completeMeetings=0;
 for(const meeting of document.querySelectorAll('[data-meeting]')){const {boxes,done}=completedFor(meeting),finished=done===boxes.length,opened=boxes.filter(b=>state.opened[b.dataset.complete]).length;completeMeetings+=Number(finished);meeting.classList.toggle('is-completed',finished);meeting.querySelector('[data-meeting-summary]').textContent=done+' of '+boxes.length+' activities completed';meeting.querySelector('[data-meeting-state]').textContent=finished?'Completed':done?'In progress':opened?'Opened '+opened+' of '+boxes.length:'Not started';const all=meeting.querySelector('[data-complete-meeting]');all.checked=finished;all.indeterminate=done>0&&!finished;}
 const overall=document.querySelector('#overall-progress');if(overall){overall.textContent=completeMeetings+' of 9 meetings completed';document.querySelector('#overall-meter').value=completeMeetings;document.querySelector('#continue-meeting').textContent=completeMeetings===9?'Review meetings':'Continue';}
 const last=document.querySelector('#last-opened');if(last){const id=state.lastOpened,link=document.querySelector('[data-open-id="'+id+'"]')||document.querySelector('[data-open-id="'+id.replace('-prep-vocab','-vocab')+'"]'),meeting=id.match(/^m([1-9])/);last.textContent=link?'Last opened: '+(meeting?'Meeting '+meeting[1]+' · ':'')+link.textContent:'No activity opened yet.';}
 const status=document.querySelector('#save-status');if(status){status.textContent=storageAvailable?'Saved only in this browser on this device.':'Saving is unavailable in this browser. Your ticks work only while this page stays open.';status.classList.toggle('storage-error',!storageAvailable);}
}
function activateMeeting(id,scroll){const meeting=document.getElementById(id);if(!meeting?.matches('[data-meeting]'))return;meeting.open=true;if(scroll){meeting.scrollIntoView({block:'start',behavior:'auto'});meeting.querySelector('summary').focus({preventScroll:true});}}
function initialMeeting(){const hash=location.hash.slice(1);if(/^m[1-9]$/.test(hash))return hash;if(state.expanded)return state.expanded;return [...document.querySelectorAll('[data-meeting]')].find(m=>{const p=completedFor(m);return p.done<p.boxes.length;})?.id||'m1';}
document.addEventListener('change',e=>{const box=e.target;if(box.matches('[data-complete]'))update(s=>{s.completed[box.dataset.complete]=box.checked;});else if(box.matches('[data-ready]'))update(s=>{s.ready[box.dataset.ready]=box.checked;});else if(box.matches('[data-complete-meeting]')){const checked=box.checked,meeting=box.closest('[data-meeting]');update(s=>{for(const child of meeting.querySelectorAll('[data-complete]'))s.completed[child.dataset.complete]=checked;});}});
function track(e){if(e.type==='auxclick'&&e.button!==1)return;const link=e.target.closest('a[data-open-id]');if(!link)return;const id=link.dataset.openId;if(!idOK(id))return;update(s=>{s.opened[id]=true;s.lastOpened=id;const meeting=id.match(/^m[1-9]/)?.[0];if(meeting)s.expanded=meeting;});}
document.addEventListener('click',track);document.addEventListener('auxclick',track);
for(const meeting of document.querySelectorAll('[data-meeting]'))meeting.addEventListener('toggle',()=>{if(meeting.open&&state.expanded!==meeting.id)update(s=>{s.expanded=meeting.id;});});
document.querySelector('#continue-meeting')?.addEventListener('click',()=>{const next=[...document.querySelectorAll('[data-meeting]')].find(m=>{const p=completedFor(m);return p.done<p.boxes.length;})||document.querySelector('[data-meeting]');if(next){activateMeeting(next.id,true);history.replaceState(null,'','#'+next.id);}});
window.addEventListener('hashchange',()=>activateMeeting(location.hash.slice(1),true));
window.addEventListener('pageshow',()=>{state=read();render();activateMeeting(initialMeeting(),false);});
window.addEventListener('storage',e=>{if(e.key===KEY||e.key===null){state=read();render();}});
for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{const status=button.parentElement.querySelector('.copy-status');try{await navigator.clipboard.writeText(button.dataset.copy);status.textContent='Link copied.';}catch(e){status.textContent='Select and copy this link: ';const input=document.createElement('input');input.value=button.dataset.copy;input.readOnly=true;input.setAttribute('aria-label','Group link to copy');status.append(input);input.focus();input.select();}});
render();activateMeeting(initialMeeting(),false);
})();
