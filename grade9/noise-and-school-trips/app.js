/* Grade 9: the approved worksheet, taught without changing its text. */
(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = s => String(s || '').toLowerCase().replace(/[’]/g,"'").replace(/[^a-z0-9' ]/g,' ').replace(/\s+/g,' ').trim();
  const countWords = s => (s.match(/[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*/g) || []).length;
  const stage = $('#stage'), slideEl = $('#current-slide'), narration = $('#narration');
  const stored = (key, fallback) => {try{return localStorage.getItem(key) ?? fallback;}catch{return fallback;}};
  const save = (key, value) => {try{localStorage.setItem(key,String(value));}catch{}};
  const S = {data:null, clips:{}, audioByText:new Map(), slides:[], index:0, hebrew:stored('teachers-show-hebrew','false')==='true', rate:Number(stored('teachers-audio-speed','0.75')), auto:false, revealed:new Set(), hinted:new Set(), choices:new Map(), variants:{near:[0,0,0,0,0,0],far:[0,0,0,0,0,0]}, cycling:true, cycles:new Map(), demos:new Map(), queue:[], queueIndex:0, activeClip:null, audioRun:0, autoTimer:0, cycleTimer:0, handTimers:[], animation:0, draft:''};
  if (![0.7,0.75,1,1.25,1.5].includes(S.rate)) S.rate=0.75;
  try {S.draft=sessionStorage.getItem('grade9-noise-writing-draft')||'';}catch{}
  let glossary = {}, chapters = {};
  const current = () => S.slides[S.index];
  const he = (text, cls='translation') => text ? `<p class="he ${cls}" lang="he" dir="rtl">${esc(text)}</p>` : '';
  const b = (action, label, cls='', attrs='') => `<button data-action="${action}" class="${cls}" ${attrs}>${label}</button>`;
  const label = (text) => `<p class="kicker">${esc(text)}</p>`;
  const audioId = text => S.audioByText.get(norm(text)) || null;
  function words(text, id) {
    let n=0;
    return String(text).split(/(\s+)/).map(part=>{
      if(/^\s+$/.test(part))return part;
      if(!part)return '';
      const clean=norm(part),gloss=glossary[clean];
      return `<span class="word${gloss?' has-gloss':''}" data-word="${n++}"${id?` data-clip="${esc(id)}"`:''}${gloss?` data-gloss="${esc(gloss)}"`:''}>${esc(part)}</span>`;
    }).join('');
  }
  const speakText=(text,cls='body-copy')=>`<p class="${cls}" dir="ltr">${words(text,audioId(text))}</p>`;
  function toast(text){const e=$('#toast');e.textContent=text;e.classList.add('visible');setTimeout(()=>e.classList.remove('visible'),2400);}
  function createSlides(){
    const add=s=>S.slides.push(s);
    add({id:'start',type:'cover',chapter:'start',title:'Too Much Noise at School'});
    S.data.warmup.forEach((w,i)=>add({id:`warmup-${i+1}`,type:'warmup',chapter:'start',title:w.title,item:w}));
    S.data.vocabulary.forEach((v,i)=>add({id:`word-${i+1}`,type:'vocab',chapter:'words',title:v.word,item:v,i}));
    S.data.checks.slice(0,2).forEach((c,i)=>add({id:`check-${i+1}`,type:'check',chapter:'words',title:c.title,item:c}));
    S.data.paragraphs.forEach((p,i)=>{
      p.sentences.forEach((s,j)=>add({id:`p${i+1}s${j+1}`,type:'sentence',chapter:'reading',title:`Paragraph ${p.id}: sentence ${j+1}`,p,i,j,item:s}));
      add({id:`paragraph-${p.id}`,type:'paragraph',chapter:'reading',title:`Paragraph ${p.id}: read it together`,p,i});
      if(i>=2){const c=S.data.checks[i];add({id:`check-${i+1}`,type:'check',chapter:'reading',title:c.title,item:c});}
    });
    S.data.questions.forEach(q=>add({id:`question-${q.number}`,type:'question',chapter:'questions',title:`Worksheet question ${q.number}`,q}));
    add({id:'writing-topic',type:'writing-topic',chapter:'writing',title:'School Trips: Near or Far?'});
    add({id:'check-writing',type:'check',chapter:'writing',title:'Opinion and reason',item:S.data.checks[5]});
    add({id:'writing-plan',type:'writing-plan',chapter:'writing',title:'Two possible opinions'});
    for(const model of ['near','far']){
      S.data.writing[model].sentences.forEach((s,n)=>add({id:`${model}-build-${n+1}`,type:'writing-build',chapter:'writing',title:`${model==='near'?'Nearby':'Distant'} trips: ${s.role.toLowerCase()}`,model,n}));
      add({id:`${model}-model`,type:'writing-model',chapter:'writing',title:`${model==='near'?'Nearby':'Distant'} trips: complete model`,model,n:5});
    }
    add({id:'your-writing',type:'your-writing',chapter:'writing',title:'Your own school trip'});
    add({id:'writing-checklist',type:'checklist',chapter:'writing',title:'Check your writing'});
    for(const [i,s] of S.slides.entries())if(chapters[s.chapter]===undefined)chapters[s.chapter]=i;
  }
  const findIndex=id=>S.slides.findIndex(s=>s.id===id);
  function sentenceChoice(model,i){const x=S.data.writing[model].sentences[i],v=S.variants[model][i];return {en:[x.en,...x.variants][v],he:[x.he,...x.variantsHe][v],role:x.role};}
  function modelText(model,until=5){return S.data.writing[model].sentences.slice(0,until+1).map((_,i)=>sentenceChoice(model,i).en).join(' ');}
  function modelHTML(model,until=5,focus=true){
    return S.data.writing[model].paragraphGroups.map(group=>{
      const ids=group.filter(i=>i<=until);if(!ids.length)return '';
      return `<p>${ids.map(i=>{const choice=sentenceChoice(model,i);return `<span class="phrase-switch${focus?(i===until?' newest':' older'):''}" role="button" tabindex="0" data-sentence="${i}" data-model="${model}" aria-label="${esc(choice.en)} Change wording" title="Click for another way to say this">${words(choice.en,audioId(choice.en))}</span>`;}).join(' ')}</p>`;
    }).join('');
  }
  function writingTracker(s){return `<nav class="tracker" aria-label="Parts of the composition">${[['Opinion',0],['Reason + example',1],['Second reason',3],['Ending',5]].map(([name,n])=>b('goto',esc(name),n===s.n?'current':'',`data-id="${s.model}-build-${n+1}"`)).join('')}</nav>`;}
  function writingTools(s){const n=countWords(modelText(s.model,s.n));return `<div class="writing-toolbar">${b('cycle-toggle',S.cycling?'Pause changes':'Resume changes','small-action',`aria-pressed="${S.cycling}"`)}${b('reset-model','Reset wording','small-action',`data-model="${s.model}"`)}<span class="word-count${n>=70&&n<=90?' in-range':''}" aria-live="polite">${n} words${s.type==='writing-model'?' · target 70–90':''}</span></div><p class="tiny">Click a sentence to try another wording. Automatic changes every 8 seconds.</p>${he('לחצו על משפט לניסוח חלופי. הניסוחים מתחלפים אוטומטית כל שמונה שניות. אפשר לעצור את ההחלפה.','note')}`;}
  function choicesHTML(item,id){return `<div class="choices" role="group" aria-label="Answer choices">${item.options.map((opt,i)=>`<button class="choice${S.choices.get(id)===i?(i===item.correctIndex?' correct':' wrong'):''}${S.revealed.has(id)&&i===item.correctIndex?' correct':''}" data-action="choose" data-choice="${i}"><span class="choice-letter">${String.fromCharCode(97+i)}.</span><span>${esc(opt)}${item.optionsHe?.[i]?`<span class="he note" lang="he" dir="rtl">${esc(item.optionsHe[i])}</span>`:''}</span></button>`).join('')}</div>`;}
  function questionHTML(s){
    const q=s.q,shown=S.revealed.has(s.id),hint=S.hinted.has(s.id);
    return label(`Worksheet question ${q.number} of 7`)+`<h2 class="question-prompt">${words(q.prompt,audioId(q.prompt))}</h2>`+he(q.promptHe)+(q.stem?speakText(q.stem+' …','write-space')+he(q.stemHe):'')+
      (q.type==='mcq'?choicesHTML(q,s.id):`<p class="write-space">Think first. Write your answer on the worksheet.</p>${he('חשבו תחילה וכתבו תשובה בדף העבודה.','note')}`)+
      `<div class="question-tools">${b('hint',hint?'Hide hint':'Hint','secondary')}${b('reveal',shown?'Hide answer':'Show answer and evidence','primary','id="show-answer" data-reveal="answer"')}${q.paragraph!=='Whole text'?b('goto',`Read paragraph ${esc(q.paragraph)}`,'secondary',`data-id="paragraph-${q.paragraph}"`):''}</div>`+
      (hint?`<div class="hint-text">${esc(q.hint)}</div>${he(q.hintHe,'note')}`:'')+
      (S.choices.has(s.id)&&!shown?`<p class="feedback">${S.choices.get(s.id)===q.correctIndex?'Correct. Look at the evidence.':'Try again. Find support in the text.'}</p>`:'')+
      (shown?`<div class="answer-panel"><p class="answer-label">A possible answer</p>${speakText(q.completeAnswer||q.answer,'answer-text')}${he(q.answerHe)}${q.evidence.map(e=>`<blockquote class="evidence">“${words(e.quote,audioId(e.quote))}”<small>Paragraph ${esc(e.paragraph)}</small></blockquote>`).join('')}<p class="note">${esc(q.explanation)}</p>${he(q.explanationHe,'note')}${q.number===6?`<details><summary class="note">Other supported answers</summary><ul class="note">${q.answerOptions.map((a,i)=>`<li>${esc(a)}${he(q.answerOptionsHe[i],'note')}</li>`).join('')}</ul></details>`:''}${b('listen-answer','Listen to the answer','small-action')}</div>`:'');
  }
  function renderHTML(s){
    if(s.type==='cover')return `<div class="cover"><div>${label('Grade 9 · Module C practice')}<h1>Too Much Noise<br>at School</h1><p class="subtle">Read carefully.<br>Find evidence.<br>Write your own opinion.</p>${he('קוראים, מוצאים ראיות בטקסט וכותבים דעה משלנו.')}<div class="actions">${b('start-audio','Start with audio','primary')}${b('goto','Start lesson','secondary','data-id="warmup-1"')}</div><p class="lesson-topics">16 words · 5 paragraphs · 7 worksheet questions</p><p class="note">Writing: school trips near or far</p></div><div><img class="cover-photo" src="images/classroom.webp" alt="An empty classroom with desks, windows and ceiling fans"><p class="photo-caption">Which classroom sounds could disturb your reading?</p></div></div>`;
    if(s.type==='warmup')return label('Before reading')+`<h2>${esc(s.item.title)}</h2>`+speakText(s.item.en)+he(s.item.he)+`<p class="note">Tell your partner. Then share one idea with the class.</p>`+he('שוחחו עם חבר ושתפו רעיון אחד עם הכיתה.','note');
    if(s.type==='vocab')return label(`Vocabulary ${s.i+1} of ${S.data.vocabulary.length}`)+`<h1 class="vocab-word${s.item.word.length>14?' long-word':''}">${words(s.item.word,audioId(s.item.word))}</h1>`+he(s.item.he,'vocab-meaning')+speakText(s.item.example,'vocab-example')+he(s.item.exampleHe)+`<p class="note">Say the word. Then use it in a short sentence.</p>`+he('אמרו את המילה ונסו להשתמש בה במשפט קצר.','note');
    if(s.type==='check'){
      const c=s.item,chosen=S.choices.get(s.id),revealed=S.revealed.has(s.id);
      return label('Quick practice · not a worksheet question')+`<h2>${esc(c.title)}</h2><p class="question-prompt">${esc(c.prompt)}</p>`+he(c.promptHe)+choicesHTML(c,s.id)+(chosen!==undefined||revealed?`<p class="feedback">${chosen===c.correctIndex||revealed?'✓ '+esc(c.explanation):'Try again. Read all the choices.'}</p>${chosen===c.correctIndex||revealed?he(c.explanationHe,'note'):''}`:'')+`<div class="actions">${b('reveal',revealed?'Hide explanation':'Show explanation','secondary','data-reveal="answer"')}</div>`;
    }
    if(s.type==='sentence')return label(`Paragraph ${s.p.id} · sentence ${s.j+1} of ${s.p.sentences.length}`)+`<div class="reading" lang="en" dir="ltr">${words(s.item.en,s.id)}</div>`+he(s.item.he)+`<div class="reading-progress"><span id="clip-progress"></span></div><div class="reader-links">${b('goto','Whole paragraph','small-action',`data-id="paragraph-${s.p.id}"`)}</div><p class="tiny">Listen at your own speed. Tap a highlighted vocabulary word for Hebrew help when עברית is on.</p>`;
    if(s.type==='paragraph'){
      const qs=S.data.questions.filter(q=>q.paragraph===s.p.id);
      return label(`Paragraph ${s.p.id} · read it together`)+`<div class="reading paragraph" lang="en" dir="ltr">${s.p.sentences.map((x,j)=>words(x.en,`p${s.i+1}s${j+1}`)).join(' ')}</div>`+he(s.p.sentences.map(x=>x.he).join(' '))+`<p class="paragraph-summary">${esc(s.p.summary.en)}</p>`+he(s.p.summary.he,'note')+`<div class="reader-links">${qs.map(q=>b('goto',`Worksheet question ${q.number}`,'small-action',`data-id="question-${q.number}"`)).join('')}</div>`;
    }
    if(s.type==='question')return questionHTML(s);
    if(s.type==='writing-topic')return label('Writing · 70–90 words')+`<h2>School Trips: Near or Far?</h2><p class="question-prompt">${esc(S.data.writing.prompt)}</p>`+he(S.data.writing.promptHe)+`<p class="body-copy">${esc(S.data.writing.instructions)}</p>`+he(S.data.writing.instructionsHe)+`<img class="trip-photo" src="images/school-bus.webp" alt="A yellow school bus, an illustration of school travel"><p class="note">Both choices are possible. Explain the choice you prefer.</p>`+he('שתי הבחירות אפשריות. הסבירו את הבחירה המועדפת עליכם.','note');
    if(s.type==='writing-plan')return label('Plan your answer')+`<h2>Two possible opinions</h2><div class="contrast"><div><h3>Near our school</h3><img class="trip-photo local-park" src="images/yarkon-park.webp" alt="Yarkon Park, one possible nearby school-trip destination"><p class="photo-caption">A local park is one possible choice.</p><p>Less time on the bus.</p><p>A lower travel cost.</p>${he('פחות זמן בנסיעה. עלות נסיעה נמוכה יותר.','note')}${b('goto','Build the nearby-trip model','primary','data-id="near-build-1"')}</div><div><h3>Far away</h3><p>A chance to visit a new place.</p><p>More time together.</p>${he('הזדמנות לבקר במקום חדש. יותר זמן יחד.','note')}${b('goto','Build the distant-trip model','primary','data-id="far-build-1"')}</div></div><p class="note">Opinion + two different reasons + an example</p>${he('דעה ברורה, שני נימוקים שונים ודוגמה.','note')}`;
    if(s.type==='writing-build'){
      const choice=sentenceChoice(s.model,s.n);
      return label(`Writing together · ${s.model==='near'?'nearby places':'places far away'}`)+`<h2>${esc(choice.role)}</h2>`+writingTracker(s)+`<p class="note">${s.n===0?'How can you state your opinion?':`What would you add for the ${choice.role.toLowerCase()}?`}</p>`+he(s.n===0?'כיצד תציגו את הדעה שלכם?':'הציעו משפט משלכם לפני קריאת הדוגמה.','note')+`<div class="build-copy en" dir="ltr">${modelHTML(s.model,s.n)}</div>`+he(choice.he)+writingTools(s);
    }
    if(s.type==='writing-model')return label('One complete model · 70–90 words')+`<h2>${esc(S.data.writing[s.model].title)}</h2>`+`<div class="model-copy en" dir="ltr">${modelHTML(s.model,5,false)}</div>`+he(S.data.writing[s.model].sentences.map((_,i)=>sentenceChoice(s.model,i).he).join(' '))+writingTools(s)+`<div class="actions">${b('goto','Write your own answer','primary','data-id="your-writing"')}${b('goto',`See the ${s.model==='near'?'distant':'nearby'}-trip model`,'secondary',`data-id="${s.model==='near'?'far':'near'}-model"`)}</div>`;
    if(s.type==='your-writing')return label('Your turn')+`<h2>Your own school trip</h2><p class="question-prompt">${esc(S.data.writing.prompt)}</p>`+he(S.data.writing.promptHe)+`<p class="note">Write 70–90 words. Give two reasons and an example. Use the worksheet or this space.</p>`+he(S.data.writing.independentTask.he,'note')+`<textarea class="draft-input" id="draft" aria-label="Your English composition" placeholder="I prefer school trips to…" spellcheck="true" lang="en">${esc(S.draft)}</textarea><p id="draft-count" class="word-count" aria-live="polite">${countWords(S.draft)} words · target 70–90</p><p class="tiny">Your draft stays in this browser tab. Copy it before closing the tab.</p><div class="actions">${b('copy-draft','Copy my writing','secondary')}${b('goto','Check my writing','primary','data-id="writing-checklist"')}</div>`;
    if(s.type==='checklist')return label('Before you finish')+`<h2>Check your writing</h2><ul class="checklist">${S.data.writing.checklist.map(x=>`<li>${esc(x.en)}${he(x.he,'note')}</li>`).join('')}</ul><div class="actions">${b('goto','Back to my writing','primary','data-id="your-writing"')}<a class="secondary" href="grade9-noise-and-school-trips.pdf" target="_blank" rel="noopener">Open the worksheet PDF</a></div>`;
    return '';
  }
  function applyLanguage(){document.body.classList.toggle('he-on',S.hebrew);$('#hebrew-toggle').setAttribute('aria-pressed',String(S.hebrew));}
  function updateControls(){
    $('#counter').textContent=`${S.index+1} / ${S.slides.length}`;
    $('#prev').disabled=S.index===0;$('#next').disabled=S.index===S.slides.length-1;
    $('#progress-fill').style.width=`${(S.index+1)/S.slides.length*100}%`;
    $$('.chapters button').forEach(x=>x.classList.toggle('current',x.dataset.chapter===current().chapter));
    $('#auto-read').textContent=`Auto-read: ${S.auto?'on':'off'}`;$('#auto-read').setAttribute('aria-pressed',String(S.auto));
    $('#audio-rate').value=String(S.rate);$('#audio-toggle').disabled=getQueue().length===0;
  }
  function render(keepScroll=false){
    const top=stage.scrollTop,s=current();
    slideEl.className=`slide active${['paragraph','question','writing-model','your-writing','checklist','writing-build'].includes(s.type)?' long':''}`;
    slideEl.dataset.slideId=s.id;slideEl.setAttribute('aria-label',`${s.title}, slide ${S.index+1} of ${S.slides.length}`);
    slideEl.innerHTML=renderHTML(s);applyLanguage();updateControls();
    stage.scrollTop=keepScroll?top:0;window.cur=S.index;
  }
  function clearHand(){S.handTimers.forEach(clearTimeout);S.handTimers=[];$('#hand-guide').hidden=true;}
  function stopTimers(){clearTimeout(S.autoTimer);clearInterval(S.cycleTimer);clearHand();}
  function go(n,hash=true){
    if(!S.slides.length)return;
    n=Math.max(0,Math.min(S.slides.length-1,n));stopTimers();stopAudio();hideTip();S.index=n;render();
    if(hash)history.replaceState(null,'',`#${current().id}`);
    scheduleSlide();
  }
  function goId(id){const n=findIndex(id);if(n>=0)go(n);}
  function scheduleSlide(){
    const s=current();
    if(S.auto&&['vocab','sentence','paragraph'].includes(s.type))S.autoTimer=setTimeout(()=>playCurrent(),4000);
    if(['writing-build','writing-model'].includes(s.type)&&S.cycling){
      if((S.demos.get(s.id)||0)<2)demoHand(true);
      S.cycleTimer=setInterval(()=>{
        if(!S.cycling||!['writing-build','writing-model'].includes(current().type))return;
        if(S.activeClip)return;
        const cycles=(S.cycles.get(s.id)||0)+1;S.cycles.set(s.id,cycles);
        if(cycles%5===0)demoHand();else changeSentence(s.model,(cycles-1)%(s.n+1),false);
      },8000);
    }
  }
  function changeSentence(model,i,manual=true){
    stopAudio();S.variants[model][i]=(S.variants[model][i]+1)%3;render(true);
    if(manual)$(`[data-sentence="${i}"][data-model="${model}"]`)?.focus({preventScroll:true});
  }
  function demoHand(initial=false){
    clearHand();const s=current(),ids=s.n>0?[0,1]:[0,0];
    const completed=initial?(S.demos.get(s.id)||0):0;
    ids.slice(completed).forEach((i,k)=>{
      S.handTimers.push(setTimeout(()=>{
        if(current().id!==s.id||!S.cycling||S.activeClip)return;
        const phrase=$(`[data-sentence="${i}"]`,slideEl);if(!phrase)return;
        const box=phrase.getClientRects()[0],stageBox=stage.getBoundingClientRect();
        if(!box||box.top<stageBox.top||box.top>stageBox.bottom-50)return;
        const hand=$('#hand-guide');hand.style.left=`${Math.min(innerWidth-60,box.left+Math.min(110,box.width/2))}px`;hand.style.top=`${box.top+Math.min(box.height,30)}px`;hand.hidden=false;
        S.handTimers.push(setTimeout(()=>{if(current().id===s.id&&S.cycling){hand.classList.add('tap');changeSentence(s.model,i,false);if(initial)S.demos.set(s.id,(S.demos.get(s.id)||0)+1);}},650));
        S.handTimers.push(setTimeout(()=>{hand.classList.remove('tap');hand.hidden=true;},1150));
      },1000+k*2000));
    });
  }
  function getQueue(answer=false){
    const s=current();if(!s)return[];
    let texts=[];
    if(s.type==='vocab')texts=[s.item.word,s.item.example];
    else if(s.type==='sentence')return S.clips[s.id]?[s.id]:[];
    else if(s.type==='paragraph')return s.p.sentences.map((_,j)=>`p${s.i+1}s${j+1}`).filter(id=>S.clips[id]);
    else if(s.type==='question')texts=answer?[s.q.completeAnswer||s.q.answer]:[s.q.prompt,...(s.q.stem?[s.q.stem]:[])];
    else if(['writing-build','writing-model'].includes(s.type))texts=S.data.writing[s.model].sentences.slice(0,s.n+1).map((_,i)=>sentenceChoice(s.model,i).en);
    return texts.map(audioId).filter(Boolean);
  }
  function audioUI(playing){$('#audio-toggle').innerHTML=playing?'❚❚ <span>Pause</span>':'▶ <span>Listen</span>';$('#audio-toggle').classList.toggle('playing',playing);}
  function stopAudio(){S.audioRun++;cancelAnimationFrame(S.animation);narration.pause();narration.removeAttribute('src');S.queue=[];S.activeClip=null;$$('.reading-now',slideEl).forEach(x=>x.classList.remove('reading-now'));audioUI(false);}
  function highlight(){
    const clip=S.clips[S.activeClip];if(!clip||narration.paused)return;
    const t=narration.currentTime;let idx=-1;
    for(let i=0;i<clip.words.length;i++){if(t>=clip.words[i].start&&t<=clip.words[i].end+.08){idx=i;break;}}
    $$('.reading-now',slideEl).forEach(x=>x.classList.remove('reading-now'));
    if(idx>=0){for(const wordIndex of (clip.wordTokens?.[idx]||[idx])){const elements=$$(`[data-clip="${S.activeClip}"][data-word="${wordIndex}"]`,slideEl);elements.forEach(e=>e.classList.add('reading-now'));}}
    const progress=$('#clip-progress');if(progress&&narration.duration)progress.style.width=`${t/narration.duration*100}%`;
    S.animation=requestAnimationFrame(highlight);
  }
  async function startClip(run){
    if(run!==S.audioRun)return;
    const id=S.queue[S.queueIndex];if(!id){audioUI(false);S.activeClip=null;$$('.reading-now',slideEl).forEach(x=>x.classList.remove('reading-now'));return;}
    const clip=S.clips[id];S.activeClip=id;narration.src=clip.file;narration.playbackRate=S.rate;narration.preservesPitch=true;
    try{await narration.play();if(run!==S.audioRun)return;audioUI(true);cancelAnimationFrame(S.animation);highlight();}
    catch(err){if(run===S.audioRun){audioUI(false);toast('Tap Listen to start the recorded audio.');}}
  }
  function playCurrent(answer=false){
    clearTimeout(S.autoTimer);clearHand();const queue=getQueue(answer);if(!queue.length)return;
    stopAudio();S.queue=queue;S.queueIndex=0;const run=S.audioRun;startClip(run);
  }
  function toggleAudio(){
    clearTimeout(S.autoTimer);clearHand();
    if(S.activeClip&&narration.getAttribute('src')){
      if(narration.paused){narration.play().then(()=>{audioUI(true);highlight();}).catch(()=>toast('Tap Listen again to start audio.'));}
      else{narration.pause();cancelAnimationFrame(S.animation);audioUI(false);}
    }else playCurrent();
  }
  narration.addEventListener('ended',()=>{cancelAnimationFrame(S.animation);S.queueIndex++;const run=S.audioRun;setTimeout(()=>startClip(run),230);});
  narration.addEventListener('error',()=>{if(narration.getAttribute('src')){audioUI(false);toast('The recording could not load. Try Listen again.');}});
  async function copy(text,success){
    try{await navigator.clipboard.writeText(text);toast(success);}catch{const field=document.createElement('textarea');field.value=text;field.style.position='fixed';field.style.left='-9999px';document.body.append(field);field.select();const ok=document.execCommand('copy');field.remove();toast(ok?success:'Copy this page address from your browser.');}
  }
  function hideTip(){$('#word-tip').hidden=true;}
  function showTip(word){
    if(!S.hebrew||!word.dataset.gloss)return;
    const tip=$('#word-tip'),rect=word.getBoundingClientRect();tip.textContent=word.dataset.gloss;tip.hidden=false;
    const box=tip.getBoundingClientRect();tip.style.left=`${Math.max(10,Math.min(innerWidth-box.width-10,rect.left))}px`;tip.style.top=`${Math.max(110,rect.top-box.height-8)}px`;
  }
  stage.addEventListener('mouseover',e=>{const w=e.target.closest('.word[data-gloss]');if(w)showTip(w);});
  stage.addEventListener('mouseout',e=>{if(e.target.closest('.word[data-gloss]'))hideTip();});
  stage.addEventListener('scroll',hideTip,{passive:true});
  stage.addEventListener('click',e=>{
    const phrase=e.target.closest('[data-sentence]');if(phrase){changeSentence(phrase.dataset.model,Number(phrase.dataset.sentence));return;}
    const action=e.target.closest('[data-action]');
    if(!action){const w=e.target.closest('.word[data-gloss]');if(w)showTip(w);return;}
    const s=current();switch(action.dataset.action){
      case 'goto':goId(action.dataset.id);break;
      case 'start-audio':S.auto=true;goId('warmup-1');toast('Audio is on. Reading starts after four seconds.');break;
      case 'hint':S.hinted.has(s.id)?S.hinted.delete(s.id):S.hinted.add(s.id);render(true);break;
      case 'reveal':S.revealed.has(s.id)?S.revealed.delete(s.id):S.revealed.add(s.id);stopAudio();render(true);break;
      case 'choose':{const i=Number(action.dataset.choice),item=s.q||s.item;S.choices.set(s.id,i);if(i===item.correctIndex)S.revealed.add(s.id);render(true);break;}
      case 'listen-answer':playCurrent(true);break;
      case 'cycle-toggle':S.cycling=!S.cycling;stopTimers();render(true);scheduleSlide();break;
      case 'reset-model':S.variants[action.dataset.model]=[0,0,0,0,0,0];stopAudio();render(true);break;
      case 'copy-draft':copy(S.draft,'Writing copied');break;
    }
  });
  stage.addEventListener('input',e=>{if(e.target.id==='draft'){S.draft=e.target.value;try{sessionStorage.setItem('grade9-noise-writing-draft',S.draft);}catch{}const n=countWords(S.draft),c=$('#draft-count');c.textContent=`${n} words · target 70–90`;c.classList.toggle('in-range',n>=70&&n<=90);}});
  document.addEventListener('keydown',e=>{
    if($('#contents-dialog').open)return;
    if(e.composedPath().some(x=>x.id==='teachers-qr-remote-host'))return;
    if(e.target.matches('input,textarea,select,[contenteditable="true"]'))return;
    if(e.target.closest('[data-sentence]')&&['Enter',' '].includes(e.key)){e.preventDefault();const x=e.target.closest('[data-sentence]');changeSentence(x.dataset.model,Number(x.dataset.sentence));return;}
    if(e.target.closest('button,a')&&['Enter',' '].includes(e.key))return;
    if(['ArrowRight','ArrowDown','PageDown'].includes(e.key)){e.preventDefault();go(S.index+1);}
    else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(S.index-1);}
    else if(e.key==='Home'){e.preventDefault();go(0);}
    else if(e.key==='End'){e.preventDefault();go(S.slides.length-1);}
    else if(e.key===' '){e.preventDefault();toggleAudio();}
  });
  let touch=null;
  stage.addEventListener('touchstart',e=>{
    if(e.touches.length!==1||e.target.closest('button,a,input,textarea,select,[data-sentence]')){touch=null;return;}
    const t=e.touches[0];touch={x:t.clientX,y:t.clientY,top:stage.scrollTop,bottom:stage.scrollTop+stage.clientHeight>=stage.scrollHeight-3,long:stage.scrollHeight>stage.clientHeight+8};
  },{passive:true});
  stage.addEventListener('touchend',e=>{
    const start=touch;touch=null;if(!start||e.changedTouches.length!==1)return;
    const t=e.changedTouches[0],dx=t.clientX-start.x,dy=t.clientY-start.y;
    if(Math.abs(dy)>65&&Math.abs(dy)>Math.abs(dx)*1.2){if(!start.long||(dy<0&&start.bottom)||(dy>0&&start.top<=3)){go(S.index+(dy<0?1:-1));}}
    else if(Math.abs(dx)>90&&Math.abs(dx)>Math.abs(dy)*1.4)go(S.index+(dx<0?1:-1));
  },{passive:true});
  stage.addEventListener('touchcancel',()=>touch=null,{passive:true});
  stage.addEventListener('touchmove',e=>{if(e.touches.length!==1)touch=null;},{passive:true});
  $('#prev').onclick=()=>go(S.index-1);$('#next').onclick=()=>go(S.index+1);
  $('#hebrew-toggle').onclick=()=>{S.hebrew=!S.hebrew;save('teachers-show-hebrew',S.hebrew);applyLanguage();hideTip();};
  $('#audio-toggle').onclick=toggleAudio;
  $('#audio-rate').onchange=e=>{S.rate=Number(e.target.value);save('teachers-audio-speed',S.rate);narration.playbackRate=S.rate;};
  $('#auto-read').onclick=()=>{S.auto=!S.auto;clearTimeout(S.autoTimer);updateControls();if(S.auto&&['vocab','sentence','paragraph'].includes(current().type))S.autoTimer=setTimeout(playCurrent,4000);};
  $('#copy-link').onclick=()=>{const url=new URL(location.href);url.searchParams.delete('teacherRemote');copy(url.href,'Presentation link copied');};
  $$('.chapters [data-chapter]').forEach(button=>button.onclick=()=>go(chapters[button.dataset.chapter]));
  function openMenu(){stopTimers();narration.pause();audioUI(false);const names={start:'Before reading',words:'Vocabulary',reading:'Read the text',questions:'The seven worksheet questions',writing:'School-trip writing'};$('#contents-list').innerHTML=Object.entries(names).map(([key,title])=>`<h3>${title}</h3>${S.slides.map((s,i)=>s.chapter===key?`<button class="contents-row${i===S.index?' current':''}" data-goto="${i}"><span>${esc(s.title)}</span><span>${i+1}</span></button>`:'').join('')}`).join('');$('#contents-dialog').showModal();}
  $('#counter').onclick=$('#open-menu').onclick=openMenu;
  let menuNavigated=false;
  $('#close-menu').onclick=()=>$('#contents-dialog').close();
  $('#contents-dialog').addEventListener('close',()=>{if(menuNavigated){menuNavigated=false;return;}stopTimers();scheduleSlide();});
  $('#contents-dialog').addEventListener('click',e=>{const row=e.target.closest('[data-goto]');if(row){menuNavigated=true;$('#contents-dialog').close();go(Number(row.dataset.goto));}});
  window.addEventListener('hashchange',()=>{const id=decodeURIComponent(location.hash.slice(1)),i=findIndex(id);if(i>=0&&i!==S.index)go(i,false);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden){stopTimers();narration.pause();audioUI(false);}else scheduleSlide();});
  window.addEventListener('pagehide',()=>{stopTimers();stopAudio();});
  async function init(){
    const results=await Promise.all([fetch('content.json?v=20261118').then(r=>{if(!r.ok)throw Error('content');return r.json();}),fetch('audio/manifest.json?v=20261118').then(r=>r.ok?r.json():{clips:{}}).catch(()=>({clips:{}}))]);
    S.data=results[0];S.clips=results[1].clips||{};for(const [id,clip] of Object.entries(S.clips)){
      S.audioByText.set(norm(clip.text),id);
      let offset=0;const spans=clip.text.split(/\s+/).filter(Boolean).map(word=>{const start=offset;offset+=norm(word).replace(/\s/g,'').length;return {start,end:offset};});
      const joined=norm(clip.text).replace(/\s/g,'');let cursor=0;
      clip.wordTokens=clip.words.map(word=>{const value=norm(word.text).replace(/\s/g,'');const found=joined.indexOf(value,cursor),start=found<0?cursor:found,end=start+value.length;cursor=end;return spans.map((span,i)=>span.end>start&&span.start<end?i:-1).filter(i=>i>=0);});
    }
    for(const [key,value] of Object.entries(S.data.glossary||{}))glossary[norm(key)]=value;
    for(const x of S.data.vocabulary)glossary[norm(x.word)]=x.he;
    createSlides();const hash=decodeURIComponent(location.hash.slice(1));const index=findIndex(hash);go(index>=0?index:0,false);
    window.noiseLesson={ready:true,go:goId,next:()=>go(S.index+1),previous:()=>go(S.index-1),get index(){return S.index;},get slides(){return S.slides.map(({id,type,chapter,title})=>({id,type,chapter,title}));},get audioClips(){return Object.keys(S.clips).length;}};
    fetch('images/attribution.json').then(r=>r.json()).then(data=>{const items=Array.isArray(data)?data:(data.images||data.assets||Object.values(data));$('#photo-credits').innerHTML=items.filter(x=>x&&typeof x==='object').map(x=>{const url=x.sourceURL||x.sourceUrl||x.source_url||x.source||'',license=x.licenseURL||x.licenseUrl||x.license_url||'',name=x.title||x.filename||x.file||'Photograph',author=x.author||'',lic=x.license||'';return `<p>${esc(name)} · ${esc(author)} · ${esc(lic)}${x.changes?' · '+esc(x.changes):''}${/^https:/.test(url)?` <a href="${esc(url)}" target="_blank" rel="noopener">Source</a>`:''}${/^https:/.test(license)?` <a href="${esc(license)}" target="_blank" rel="noopener">License</a>`:''}</p>`;}).join('');}).catch(()=>{$('#photo-credits').textContent='Classroom: CC0. School bus: CC0. Yarkon Park: Ynhockey, CC BY-SA 4.0. Sources are recorded in images/attribution.json.';});
  }
  init().catch(error=>{console.error(error);slideEl.innerHTML=`<h1>The lesson could not load</h1><p>Refresh this page, or open the worksheet below.</p><a href="grade9-noise-and-school-trips.pdf">Open worksheet PDF</a>`;});
})();
