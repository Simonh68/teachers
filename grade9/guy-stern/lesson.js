/* Guy Stern content adapters. Navigation, gestures, recording and glosses are shared. */
(()=>{'use strict';
const data=window.STERN_LESSON,$=id=>document.getElementById(id),allSlides=[...document.querySelectorAll('.slide')];
const storage={get(k,f=null){try{return localStorage.getItem(k)??f}catch{return f}},set(k,v){try{localStorage.setItem(k,String(v))}catch{}}};
const speedKey='teachers-read-alone-speed-v1',rates=[.25,.35,.5,.75,1,1.25,1.5];
const savedRate=Number(storage.get(speedKey,.75));let rate=rates.includes(savedRate)?savedRate:.75;
const reader=TeacherInlineReader.install({records:data.records,glosses:data.glosses});
const player=reader.player,bar=$('reader-bar'),voice=player.media;voice.id='voice';voice.hidden=true;document.body.append(voice);
const vocabulary=new Audio();vocabulary.preload='none';vocabulary.preservesPitch=true;vocabulary.id='vocabulary-voice';vocabulary.hidden=true;document.body.append(vocabulary);
let active=null,activeInfo=null,pendingPlay=false,vocabButton=null,toastTimer=0,guideTimer=0,guideHide=0,readVisits=0;
let previousPosition=Number(storage.get('guy-stern-position-v1',0)),lastWord=-1;
const completed=new Set(JSON.parse((()=>{try{const s=storage.get('guy-stern-completed-v1','[]');return Array.isArray(JSON.parse(s))?s:'[]'}catch{return '[]'}})()));
const format=t=>{t=Math.max(0,Number(t)||0);return Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0')};
function tell(text){clearTimeout(toastTimer);$('toast').textContent=text;$('toast').classList.add('visible');toastTimer=setTimeout(()=>$('toast').classList.remove('visible'),2800)}
function setRate(n){rate=rates.includes(Number(n))?Number(n):.75;player.rate=rate;voice.playbackRate=rate;voice.preservesPitch=true;vocabulary.playbackRate=rate;$('speed').value=String(rate);storage.set(speedKey,rate)}
setRate(rate);
function setHebrew(show){document.documentElement.dataset.hebrew=String(show);$('hebrew-toggle').setAttribute('aria-pressed',String(show));storage.set('guy-stern-hebrew-v1',show);reader.clear()}
setHebrew(storage.get('guy-stern-hebrew-v1','false')==='true');
function stopVocabulary(){vocabulary.pause();vocabulary.currentTime=0;if(vocabButton){vocabButton.textContent='Listen';vocabButton.setAttribute('aria-pressed','false')}vocabButton=null}
function stopAll(){reader.reset();stopVocabulary();clearTimeout(guideTimer);clearTimeout(guideHide);$('hand-guide').hidden=true}
function goto(n,play=false){n=Math.max(1,Math.min(data.slides.length,Number(n)));pendingPlay=play;closeDialogs();if(activeInfo?.slide===n){if(play)playPassage();return}location.hash='slide-'+n}
function closeDialogs(){document.querySelectorAll('dialog[open]').forEach(d=>d.close())}
function openDialog(id){stopAll();$(id).showModal()}
function range(){if(!activeInfo||activeInfo.kind!=='story-reading')return null;return {first:activeInfo.first,last:activeInfo.last,start:activeInfo.start,end:activeInfo.end}}
function playPassage(){const r=range();if(r){stopVocabulary();player.playRange(r.first,r.last,bar)}}
function updateClock(){const r=range();if(!r)return;const t=Math.min(r.end,Math.max(r.start,voice.currentTime||r.start));$('seek').value=String(Math.max(0,t-r.start));$('elapsed').textContent=format(t-r.start);$('duration').textContent=format(r.end-r.start)}
const originalWord=player.onWord;player.onWord=id=>{originalWord(id);if(id>=0)lastWord=id};
const originalState=player.onState;player.onState=p=>{originalState(p);const on=['playing','loading','gap'].includes(p.phase),paused=p.phase.startsWith('paused');if(paused)originalWord(-1);const r=range(),fullPassage=!!r&&p.segments[0]?.words[0]?.id===r.first&&p.segments.at(-1)?.words.at(-1)?.id===r.last;$('play').textContent=on?'Pause':paused?'Continue':'Listen';$('play').setAttribute('aria-pressed',String(on));bar.querySelector('[data-read-status]').textContent=({loading:'Loading audio…',playing:'Listen and follow the highlighted word.',paused:'Paused','paused-loading':'Paused','paused-gap':'Paused',ended:fullPassage?'Passage complete. Choose Next to continue.':'Sentence complete. Press Listen for the passage.',error:'Audio could not play. Press Listen to retry.'}[p.phase]||'Recorded English narration');if(p.phase==='ended'&&fullPassage){completed.add(activeInfo.slide);storage.set('guy-stern-completed-v1',JSON.stringify([...completed]));$('next').classList.add('ready');refreshTabs()}updateClock()};
function refreshTabs(){for(const tab of document.querySelectorAll('[data-tab-slide]'))tab.classList.toggle('done',completed.has(Number(tab.dataset.tabSlide)))}
data.chapters.forEach(ch=>{document.querySelectorAll(`[data-tabs="${ch.id}"]`).forEach(holder=>{const selected=Number(holder.dataset.page);holder.innerHTML=ch.reading.map((n,i)=>`<button role="tab" aria-selected="${i===selected}" aria-label="Passage ${i+1}" data-tab-slide="${n}" data-jump-slide="${n}" class="${completed.has(n)?'done':''}">${i+1}</button>`).join('')})});
function handGuide(){if(!active||document.hidden||new URLSearchParams(location.search).has('teacherRemote'))return;const word=active.querySelector('[data-gloss]');if(!word)return;const r=word.getBoundingClientRect();if(r.top<90||r.bottom>innerHeight-180)return;const guide=$('hand-guide');guide.style.left=Math.max(8,Math.min(innerWidth-170,r.left+12))+'px';guide.style.top=Math.min(innerHeight-210,r.bottom+9)+'px';guide.hidden=false;guideHide=setTimeout(()=>{guide.hidden=true},3300)}
function changed(){const next=document.querySelector('.slide.active');if(!next||next===active)return;const wantPlay=pendingPlay;pendingPlay=false;stopAll();active=next;activeInfo=data.slides[allSlides.indexOf(active)];lastWord=-1;$('next').classList.remove('ready');const isRead=activeInfo.kind==='story-reading';document.body.classList.toggle('is-reading',isRead);bar.hidden=!isRead;storage.set('guy-stern-position-v1',activeInfo.slide);if(isRead){bar.dataset.first=activeInfo.first;bar.dataset.last=activeInfo.last;$('seek').max=String(activeInfo.end-activeInfo.start);$('seek').value='0';$('elapsed').textContent='0:00';$('duration').textContent=format(activeInfo.end-activeInfo.start);bar.querySelector('[data-read-status]').textContent='Recorded English narration';readVisits++;if(readVisits===1||readVisits%5===0)guideTimer=setTimeout(handGuide,1400);if(wantPlay)playPassage()}document.title=(activeInfo.chapter?data.chapters[activeInfo.chapter-1].title+' · ':'')+'Guy Stern | Grade 9';}
const watcher=new MutationObserver(changed);allSlides.forEach(s=>watcher.observe(s,{attributes:true,attributeFilter:['class','hidden']}));changed();
if(previousPosition>1&&previousPosition<=allSlides.length){$('resume').hidden=false;$('resume').addEventListener('click',()=>goto(previousPosition))}
document.addEventListener('click',async e=>{
 const t=e.target.closest('button,a');if(!t)return;
 if(t.hasAttribute('data-open-menu'))openDialog('chapter-menu');
 else if(t.hasAttribute('data-open-sources'))openDialog('sources');
 else if(t.hasAttribute('data-close-dialog'))t.closest('dialog').close();
 else if(t.hasAttribute('data-jump-slide'))goto(t.dataset.jumpSlide);
 else if(t.hasAttribute('data-start'))goto(data.chapters[0].start);
 else if(t.hasAttribute('data-vocabulary'))goto(data.chapters[Number(t.dataset.vocabulary)-1].vocabulary[0]);
 else if(t.hasAttribute('data-listen-chapter'))goto(data.chapters[Number(t.dataset.listenChapter)-1].reading[0],true);
 else if(t.hasAttribute('data-show-answer'))goto(activeInfo.slide+1);
 else if(t.hasAttribute('data-vocab-reveal')){const content=active.querySelector('.answer-content');const reveal=content.hidden;content.hidden=!reveal;t.textContent=reveal?'Hide the meaning':'Show the meaning';t.setAttribute('aria-expanded',String(reveal));}
 else if(t.hasAttribute('data-vocab-audio')){if(vocabButton===t&&!vocabulary.paused){vocabulary.pause();t.textContent='Continue';t.setAttribute('aria-pressed','false');return}reader.reset();if(vocabButton!==t){stopVocabulary();vocabButton=t;vocabulary.src=t.dataset.vocabAudio;vocabulary.playbackRate=rate}try{await vocabulary.play();t.textContent='Pause';t.setAttribute('aria-pressed','true')}catch{tell('Audio could not play. Press Listen to retry.')}}
});
vocabulary.addEventListener('ended',()=>{if(vocabButton){vocabButton.textContent='Listen';vocabButton.setAttribute('aria-pressed','false')}});
vocabulary.addEventListener('error',()=>{if(vocabButton){vocabButton.textContent='Retry audio';tell('The recording could not load. Check your connection.')}});
$('hebrew-toggle').addEventListener('click',()=>setHebrew(document.documentElement.dataset.hebrew!=='true'));
$('speed').addEventListener('change',e=>setRate(e.target.value));
voice.addEventListener('timeupdate',updateClock);
async function seekTo(seconds){const r=range();if(!r)return;const target=r.start+Math.max(0,Math.min(r.end-r.start,seconds)),resume=['playing','loading','gap'].includes(player.phase);player.stop();const token=player.epoch;player.owner=bar;player.segments=TeacherInlineReader.buildSegments(data.records,r.first,r.last);player.part=0;const source=player.segments[0].src;if(player.source!==source){player.source=source;voice.src=source;voice.load()}player.phase='paused';player.emit();try{if(voice.readyState<1)await new Promise((resolve,reject)=>{const clean=()=>{voice.removeEventListener('loadedmetadata',ok);voice.removeEventListener('error',bad);clearTimeout(timer)};const ok=()=>{clean();resolve()},bad=()=>{clean();reject(Error('Audio unavailable'))};const timer=setTimeout(bad,15000);voice.addEventListener('loadedmetadata',ok,{once:true});voice.addEventListener('error',bad,{once:true})});if(token!==player.epoch)return;voice.playbackRate=rate;voice.currentTime=target;lastWord=-1;reader.clear();updateClock();if(resume)player.resume()}catch{if(token===player.epoch)player.fail()}}
$('seek').addEventListener('input',e=>seekTo(Number(e.target.value)));
$('rewind').addEventListener('click',()=>{const r=range();if(r)seekTo(Math.max(0,voice.currentTime-r.start-15))});
$('replay-sentence').addEventListener('click',()=>{const r=range();if(!r)return;const words=data.records.flatMap(r=>r.words).filter(w=>w.id>=r.first&&w.id<=r.last);let i=Math.max(0,words.findLastIndex(w=>voice.currentTime>=w.start));const sentenceEnd=w=>/[.!?]$/.test(w.text)&&!['St.','U.S.','Dr.','Mr.','Mrs.'].includes(w.text);let first=i,last=i;while(first>0&&!sentenceEnd(words[first-1]))first--;while(last<words.length-1&&!sentenceEnd(words[last]))last++;player.playRange(words[first].id,words[last].id,bar)});
// Keep modal key presses inside the dialog; shared navigation owns deck keys.
document.addEventListener('keydown',e=>{if(document.querySelector('dialog[open]')&&['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','PageUp','PageDown','Home','End',' '].includes(e.key)){e.stopImmediatePropagation();return}if(e.key===' '&&activeInfo?.kind==='story-reading'&&!e.target.closest('a,button,input,select,textarea,[data-gloss]')){e.preventDefault();e.stopImmediatePropagation();$('play').click()}},true);
document.addEventListener('click',e=>{if(!e.target.closest('[data-gloss]'))reader.clear()},true);
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopAll()});window.addEventListener('pagehide',stopAll);
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close()}}));
$('copy-link').addEventListener('click',async()=>{const url=new URL(location.href);url.searchParams.delete('teacherRemote');try{await navigator.clipboard.writeText(url.href);tell('Link copied · הקישור הועתק')}catch{$('manual-link').value=url.href;openDialog('copy-dialog');$('manual-link').focus();$('manual-link').select()}});
$('fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{tell('Use your browser full-screen option.')}});
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen'});
window.GuySternLesson={reader,player,vocabulary,get current(){return activeInfo},chapters:data.chapters};
})();
