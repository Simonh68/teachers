/* Plain HTML links and checkboxes; this script saves only in this browser. */
(()=>{'use strict';
const KEY='teachers-unit2-meetings-v1';
const meetingID=s=>typeof s==='string'&&/^(m[1-9]|d[0-9]{8})$/.test(s);
const idOK=s=>typeof s==='string'&&/^((?:m[1-9]|d[0-9]{8})(?:-[a-z0-9-]+)?|unit-(prep|guide))$/.test(s);
const blank=()=>({version:1,opened:{},completed:{},ready:{},lastOpened:'',expanded:'',historyBackup:null});
function flags(value){const out={};if(value&&typeof value==='object')for(const [id,marked] of Object.entries(value))if(idOK(id)&&marked===true)out[id]=true;return out;}
const hasHistory=value=>!!value&&(Object.keys(value.opened).length>0||!!value.lastOpened);
let state=blank(),storageAvailable=true;
function read(){
 if(!storageAvailable)return state;
 let raw;try{raw=localStorage.getItem(KEY);}catch(e){storageAvailable=false;return state;}
 if(!raw)return blank();
 try{const saved=JSON.parse(raw),out=blank();if(!saved||saved.version!==1)return out;
  for(const field of ['opened','completed','ready'])out[field]=flags(saved[field]);
  if(idOK(saved.lastOpened))out.lastOpened=saved.lastOpened;
  if(meetingID(saved.expanded))out.expanded=saved.expanded;
  if(saved.historyBackup&&typeof saved.historyBackup==='object'){const backup={opened:flags(saved.historyBackup.opened),lastOpened:idOK(saved.historyBackup.lastOpened)?saved.historyBackup.lastOpened:''};if(hasHistory(backup))out.historyBackup=backup;}
  return out;
 }catch(e){return blank();}
}
state=read();
function persist(){try{localStorage.setItem(KEY,JSON.stringify(state));storageAvailable=true;}catch(e){storageAvailable=false;}render();}
function update(fn){state=read();fn(state);persist();}
function completedFor(meeting){const scope=meeting.querySelector('[data-classwork]')||meeting;const boxes=[...scope.querySelectorAll('[data-complete]')];return {boxes,done:boxes.filter(b=>state.completed[b.dataset.complete]).length};}
function render(){
 document.documentElement.classList.add('history-tracked');
 for(const box of document.querySelectorAll('[data-complete]')){box.checked=!!state.completed[box.dataset.complete];box.closest('.activity').classList.toggle('is-completed',box.checked);}
 for(const box of document.querySelectorAll('[data-ready]')){box.checked=!!state.ready[box.dataset.ready];box.closest('.prep-card').classList.toggle('is-ready',box.checked);}
 for(const link of document.querySelectorAll('[data-open-id]')){const id=link.dataset.openId,opened=!!state.opened[id];link.classList.toggle('was-opened',opened);const badge=document.querySelector('[data-open-status="'+id+'"]');if(badge){badge.hidden=!opened;badge.textContent=id===state.lastOpened?'Last opened':'Opened';}link.closest('.activity')?.classList.toggle('last-opened',id===state.lastOpened);}
 let completeMeetings=0;
 const meetings=[...document.querySelectorAll('[data-meeting]')];
 for(const meeting of meetings){const {boxes,done}=completedFor(meeting),finished=boxes.length>0&&done===boxes.length,opened=boxes.filter(b=>[...b.closest('.activity').querySelectorAll('[data-open-id]')].some(a=>state.opened[a.dataset.openId])).length;completeMeetings+=Number(finished);meeting.classList.toggle('is-completed',finished);meeting.querySelector('[data-meeting-summary]').textContent=done+' of '+boxes.length+(meeting.querySelector('[data-classwork]')?' class activities completed':' activities completed');meeting.querySelector('[data-meeting-state]').textContent=finished?'Completed':done?'In progress':opened?'Opened '+opened+' of '+boxes.length:'Not started';const all=meeting.querySelector('[data-complete-meeting]');all.checked=finished;all.indeterminate=done>0&&!finished;const home=[...meeting.querySelectorAll('[data-homework] [data-complete]')],summary=meeting.querySelector('[data-home-summary]');if(summary)summary.textContent=home.filter(b=>state.completed[b.dataset.complete]).length+' of '+home.length+' home rounds completed';}
 const overall=document.querySelector('#overall-progress');if(overall){overall.textContent=completeMeetings+' of '+meetings.length+' meetings completed';document.querySelector('#overall-meter').value=completeMeetings;document.querySelector('#overall-meter').max=meetings.length;document.querySelector('#continue-meeting').textContent=completeMeetings===meetings.length?'Review meetings':'Continue';}
 const last=document.querySelector('#last-opened');if(last){const id=state.lastOpened,link=document.querySelector('[data-open-id="'+id+'"]')||document.querySelector('[data-open-id="'+id.replace('-prep-vocab','-vocab')+'"]'),meeting=link?.closest('[data-meeting],[data-prep-meeting]'),prefix=meeting?(meeting.querySelector('time')?.textContent||'Meeting '+(meeting.dataset.number||meeting.id.slice(1)))+' · ':'';last.textContent=link?'Last opened: '+prefix+link.textContent:id?'Last opened on another checklist page.':'No activity opened yet.';}
 const status=document.querySelector('#save-status');if(status){status.textContent=storageAvailable?'Saved only in this browser on this device.':'Saving is unavailable in this browser. Your ticks work only while this page stays open.';status.classList.toggle('storage-error',!storageAvailable);}
 const reset=document.querySelector('#reset-history'),restore=document.querySelector('#restore-history');if(reset)reset.disabled=!hasHistory(state);if(restore)restore.disabled=!hasHistory(state.historyBackup);
 const historyStatus=document.querySelector('#history-status');if(historyStatus)historyStatus.textContent=hasHistory(state.historyBackup)?'Cleared history is ready to restore. Links opened since the reset will also be kept.':'No cleared history to restore.';
}
function activateMeeting(id,scroll){const meeting=document.getElementById(id);if(!meeting?.matches('[data-meeting]'))return;meeting.open=true;if(scroll){meeting.scrollIntoView({block:'start',behavior:'auto'});meeting.querySelector('summary').focus({preventScroll:true});}}
function initialMeeting(){const exists=id=>meetingID(id)&&document.getElementById(id)?.matches('[data-meeting]');const hash=location.hash.slice(1);if(exists(hash))return hash;if(exists(state.expanded))return state.expanded;const meetings=[...document.querySelectorAll('[data-meeting]')];return meetings.find(m=>{const p=completedFor(m);return p.done<p.boxes.length;})?.id||meetings[0]?.id||'';}
document.addEventListener('change',e=>{const box=e.target;if(box.matches('[data-complete]'))update(s=>{s.completed[box.dataset.complete]=box.checked;});else if(box.matches('[data-ready]'))update(s=>{s.ready[box.dataset.ready]=box.checked;});else if(box.matches('[data-complete-meeting]')){const checked=box.checked,meeting=box.closest('[data-meeting]');update(s=>{for(const child of completedFor(meeting).boxes)s.completed[child.dataset.complete]=checked;});}});
function track(e){if(e.type==='auxclick'&&e.button!==1)return;const link=e.target.closest('a[data-open-id]');if(!link)return;const id=link.dataset.openId;if(!idOK(id))return;update(s=>{s.opened[id]=true;s.lastOpened=id;const meeting=id.match(/^(m[1-9]|d[0-9]{8})/)?.[0];if(meeting)s.expanded=meeting;});}
document.addEventListener('click',track);document.addEventListener('auxclick',track);
document.querySelector('#reset-history')?.addEventListener('click',()=>update(s=>{
 if(!hasHistory(s))return;
 s.historyBackup={opened:{...s.historyBackup?.opened,...s.opened},lastOpened:s.lastOpened||s.historyBackup?.lastOpened||''};
 s.opened={};s.lastOpened='';
}));
document.querySelector('#restore-history')?.addEventListener('click',()=>update(s=>{
 if(!hasHistory(s.historyBackup))return;
 s.opened={...s.historyBackup.opened,...s.opened};s.lastOpened=s.lastOpened||s.historyBackup.lastOpened;s.historyBackup=null;
}));
for(const meeting of document.querySelectorAll('[data-meeting]'))meeting.addEventListener('toggle',()=>{if(meeting.open&&state.expanded!==meeting.id)update(s=>{s.expanded=meeting.id;});});
document.querySelector('#continue-meeting')?.addEventListener('click',()=>{const next=[...document.querySelectorAll('[data-meeting]')].find(m=>{const p=completedFor(m);return p.done<p.boxes.length;})||document.querySelector('[data-meeting]');if(next){activateMeeting(next.id,true);history.replaceState(null,'','#'+next.id);}});
window.addEventListener('hashchange',()=>activateMeeting(location.hash.slice(1),true));
window.addEventListener('pageshow',()=>{state=read();render();activateMeeting(initialMeeting(),false);});
window.addEventListener('storage',e=>{if(e.key===KEY||e.key===null){state=read();render();}});
for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{const status=button.parentElement.querySelector('.copy-status');try{await navigator.clipboard.writeText(button.dataset.copy);status.textContent='Link copied.';}catch(e){status.textContent='Select and copy this link: ';const input=document.createElement('input');input.value=button.dataset.copy;input.readOnly=true;input.setAttribute('aria-label','Group link to copy');status.append(input);input.focus();input.select();}});
render();activateMeeting(initialMeeting(),false);
})();
