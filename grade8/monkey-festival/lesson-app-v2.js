(()=>{
const D=window.MONKEY_DATA, stage=document.getElementById('stage'), player=document.getElementById('narration');
const slides=[];
const add=s=>slides.push(s);
add({type:'cover',eyebrow:'GRADE 8 · 60 MINUTES',title:'The Monkey Festival',sub:'Complete story · Part One + Part Two · sentence by sentence'});
add({type:'plan',eyebrow:'TODAY · 60 MINUTES',title:'מה נעשה בשיעור?',plan:[['0–10','Vocabulary'],['10–37','Part One'],['37–52','Part Two'],['52–60','Translation + exit']]});
add({type:'visual',...D.visuals[0]}); add({type:'visualReveal',...D.visuals[0]});
add({type:'section',eyebrow:'VOCABULARY',title:'Words before the story',sub:'Look → listen → guess → reveal'});
D.vocab.forEach(v=>{add({type:'vocab',...v});add({type:'vocabReveal',...v,audio:null})});
add({type:'visual',...D.visuals[1]}); add({type:'visualReveal',...D.visuals[1]});
add({type:'section',eyebrow:'PART ONE · A–F',title:'Part One',sub:'Every sentence. Nothing skipped.'});
const qByAfter=Object.fromEntries(D.questions.map(q=>[q.after,q]));
D.story.forEach((st,i)=>{
 if(i===18){add({type:'visual',...D.visuals[2]});add({type:'visualReveal',...D.visuals[2]});add({type:'section',eyebrow:'PART TWO · G–I',title:'Part Two',sub:'Why do the people care about the monkeys?'});}
 add({type:'story',...st});add({type:'storyReveal',...st,audio:null});
 const q=qByAfter[i+1]; if(q){add({type:'question',...q});add({type:'questionReveal',...q});add({type:'answer',...q});add({type:'answerReveal',...q});}
});
add({type:'section',eyebrow:'TEST LANGUAGE',title:'עברית → English',sub:'Use the story vocabulary.'});
D.translations.forEach(t=>{add({type:'translation',...t});add({type:'translationAnswer',...t})});
add({type:'exit',eyebrow:'EXIT · 2 MINUTES',title:'Before you leave…',items:['Name 3 vocabulary words.','Answer one BASIC question.','Answer one COMPREHENSION question.','Translate one sentence.','Tell me what Part Two explains.']});
function render(s,i){let x='';
 if(s.type==='cover')x=`<div class="frame"><p class="eyebrow">${s.eyebrow}</p><h1 class="title en">${s.title}</h1><p class="subtitle en">${s.sub}</p><button class="start" id="startLesson">Start lesson</button><p class="smallnote">Swipe left / up = next · right / down = previous.</p></div>`;
 else if(s.type==='plan')x=`<div class="frame"><p class="eyebrow">${s.eyebrow}</p><h1 class="sectionTitle">${s.title}</h1><div class="plan">${s.plan.map(a=>`<div><b>${a[0]}</b><span>${a[1]}</span></div>`).join('')}</div></div>`;
 else if(s.type==='visual'||s.type==='visualReveal')x=`<div class="frame"><img src="${s.img}" alt=""><div class="caption"><h2 class="en">${s.title}</h2><p class="en">${s.en}</p></div>${s.type==='visualReveal'?`<p class="visualHe"><span class="translationLabel">תרגום</span>${s.he}</p>`:''}<span class="credit">${s.credit}</span></div>`;
 else if(s.type==='section')x=`<div class="frame"><p class="eyebrow">${s.eyebrow}</p><h1 class="sectionTitle en">${s.title}</h1><p class="sectionSub en">${s.sub}</p></div>`;
 else if(s.type==='vocab')x=`<div class="frame"><div class="vocabAnchor"><p class="eyebrow">VOCABULARY · LISTEN FIRST</p><h1 class="word">${s.word}</h1><p class="example">${s.en}</p></div></div>`;
 else if(s.type==='vocabReveal')x=`<div class="frame"><div class="vocabAnchor"><p class="eyebrow">VOCABULARY · REVEAL</p><h1 class="word">${s.word}</h1><p class="example">${s.en}</p></div><div class="vocabRevealBottom"><p class="meaning">${s.meaning}</p><p class="exampleHe">${s.he}</p></div></div>`;
 else if(s.type==='story')x=`<div class="frame"><div class="storyAnchor"><p class="eyebrow">${s.eyebrow}</p><p class="story">${s.en}</p></div></div>`;
 else if(s.type==='storyReveal')x=`<div class="frame"><div class="storyAnchor"><p class="eyebrow">${s.eyebrow}</p><p class="story">${s.en}</p></div><p class="storyHe"><span class="translationLabel">תרגום</span>${s.he}</p></div>`;
 else if(s.type==='question'||s.type==='questionReveal')x=`<div class="frame"><div class="qaAnchor"><span class="pill ${s.level}">${s.label}</span><h1 class="question">${s.en}</h1><p class="subtitle en">Answer before moving on.</p></div>${s.type==='questionReveal'?`<p class="qaHe"><span class="translationLabel">תרגום השאלה</span>${s.he}</p>`:''}</div>`;
 else if(s.type==='answer'||s.type==='answerReveal')x=`<div class="frame"><div class="qaAnchor"><span class="pill answer">ANSWER</span><h1 class="question">${s.en}</h1><p class="answerText">${s.answer}</p></div>${s.type==='answerReveal'?`<p class="answerHe"><span class="translationLabel">תרגום התשובה</span>${s.answerHe}</p>`:''}</div>`;
 else if(s.type==='translation')x=`<div class="frame"><p class="eyebrow">TRANSLATE · HEBREW → ENGLISH</p><h1 class="translationPrompt">${s.he}</h1><p class="hint">Help: ${s.hint}</p></div>`;
 else if(s.type==='translationAnswer')x=`<div class="frame"><span class="pill answer">ANSWER</span><h1 class="translationPrompt">${s.he}</h1><p class="answerText">${s.answer}</p></div>`;
 else if(s.type==='exit')x=`<div class="frame"><p class="eyebrow">${s.eyebrow}</p><h1 class="sectionTitle en">${s.title}</h1><div class="plan" style="grid-template-columns:1fr 1fr">${s.items.map((a,j)=>`<div><b>${j+1}</b><span class="en">${a}</span></div>`).join('')}</div></div>`;
 return `<section class="slide ${(s.type==='visual'||s.type==='visualReveal')?'visual':''}" data-audio-file="${s.audio||''}" aria-label="Slide ${i+1} of ${slides.length}">${x}</section>`;
}
stage.innerHTML=slides.map(render).join('');
const nodes=[...document.querySelectorAll('.slide')], counter=document.getElementById('counter'), progress=document.getElementById('progress'), audioBtn=document.getElementById('audioBtn'), replayBtn=document.getElementById('replayBtn');
let index=0,audioOn=true,audioUnlocked=false,timer=null;
if(D.audioReady){audioBtn.hidden=false;replayBtn.hidden=false;audioBtn.classList.add('on')}
function stopAudio(){clearTimeout(timer);player.pause();player.removeAttribute('src');player.load()}
function playCurrent(force=false){stopAudio();if(!D.audioReady||!audioOn||(!audioUnlocked&&!force))return;const file=nodes[index].dataset.audioFile;if(!file)return;timer=setTimeout(()=>{player.src=file;player.currentTime=0;player.play().catch(()=>{})},2000)}
function show(n){index=Math.max(0,Math.min(nodes.length-1,n));nodes.forEach((x,j)=>x.classList.toggle('active',j===index));counter.textContent=`${index+1} / ${nodes.length}`;progress.style.width=`${(index+1)/nodes.length*100}%`;playCurrent();const b=document.getElementById('startLesson');if(b)b.onclick=()=>{audioUnlocked=true;show(1)}}
document.getElementById('next').onclick=()=>{audioUnlocked=true;show(index+1)};document.getElementById('prev').onclick=()=>{audioUnlocked=true;show(index-1)};replayBtn.onclick=()=>{audioUnlocked=true;playCurrent(true)};audioBtn.onclick=()=>{audioOn=!audioOn;audioBtn.classList.toggle('on',audioOn);audioBtn.textContent=audioOn?'🔊 AUDIO':'🔇 MUTED';if(!audioOn)stopAudio();else{audioUnlocked=true;playCurrent(true)}};
window.addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(index+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(index-1)}if(e.key.toLowerCase()==='r')playCurrent(true)});
let gesture=null;stage.addEventListener('pointerdown',e=>{if(e.target.closest('button,a'))return;gesture={x:e.clientX,y:e.clientY,id:e.pointerId};audioUnlocked=true;try{stage.setPointerCapture(e.pointerId)}catch(_){}});stage.addEventListener('pointerup',e=>{if(!gesture||gesture.id!==e.pointerId)return;const dx=e.clientX-gesture.x,dy=e.clientY-gesture.y;gesture=null;const ax=Math.abs(dx),ay=Math.abs(dy);if(Math.max(ax,ay)<55)return;if(ax>ay){dx<0?show(index+1):show(index-1)}else{dy<0?show(index+1):show(index-1)}});stage.addEventListener('pointercancel',()=>gesture=null);
show(0);
})();
