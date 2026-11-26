(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const controllerMode = new URLSearchParams(location.search).has('teacherRemote');
  const ui = {
    en: {classLabel:'Class materials',worksheet:'Worksheet PDF',menu:'Menu',menuTitle:'Lesson menu',menuHelp:'Press Down Arrow to reveal the answer, see the explanation and continue. No answer selection is required.',worksheetFull:'Worksheet PDF · 2 pages',key:'Worksheet answer key',copy:'Copy link',copied:'Link copied',copyFail:'Copy this page address from your browser.',full:'Full screen',previous:'Previous step',restart:'Start again',classMaterials:'Grade 8 materials',school:'All classes',rounds:'Choose a round',footnote:'30 multiple-choice questions · 40 open questions · 35 translations in each direction. Other natural translations may also be correct.',round:'ROUND',question:'Challenge',step:'Step',toEn:'Translate into English',toHe:'Translate into Hebrew',choice:'Choose a translation',open:'Your translation',think:'Say your translation aloud.',answer:'One possible answer',correct:'Correct translation',notice:'Notice',next:['Reveal answer','See why','Next challenge'],done:'Completed',completion:'All 70 challenges completed. Well done!',keyHelp:'One key. Every step.',easy:'Warm-up',core:'Core practice',challenge:'Stretch',remote:'Optional QR phone remote',remoteError:'The phone remote is unavailable. Down Arrow still works.'},
    he: {classLabel:'חומרי כיתה ח׳',worksheet:'דף עבודה PDF',menu:'תפריט',menuTitle:'תפריט השיעור',menuHelp:'לוחצים על חץ למטה לחשיפת התשובה, לשורת ההסבר ולהמשך. אין צורך לבחור תשובה או להשתמש בעכבר.',worksheetFull:'דף עבודה PDF · שני עמודים',key:'מפתח תשובות לדף העבודה',copy:'העתקת קישור',copied:'הקישור הועתק',copyFail:'אפשר להעתיק את כתובת העמוד משורת הכתובת.',full:'מסך מלא',previous:'השלב הקודם',restart:'מההתחלה',classMaterials:'חומרי כיתה ח׳',school:'תפריט הכיתות',rounds:'בחירת סבב',footnote:'30 שאלות רב־ברירה · 40 שאלות פתוחות · 35 תרגומים בכל כיוון. גם תרגומים טבעיים אחרים עשויים להיות נכונים.',round:'סבב',question:'אתגר',step:'שלב',toEn:'תרגמו לאנגלית',toHe:'תרגמו לעברית',choice:'בחרו את התרגום',open:'תרגמו בעצמכם',think:'אמרו את התרגום בקול.',answer:'תשובה אפשרית',correct:'התרגום הנכון',notice:'שימו לב',next:['חשיפת תשובה','הסבר קצר','האתגר הבא'],done:'התרגול הושלם',completion:'סיימתם את כל 70 האתגרים. כל הכבוד!',keyHelp:'חץ למטה, לאורך כל הדרך.',easy:'קל',core:'מתאים',challenge:'קשה',remote:'שלט טלפון QR לבחירה',remoteError:'שלט הטלפון אינו זמין. חץ למטה ממשיך לפעול.'}
  };
  let lang = 'en';
  try { lang = localStorage.getItem('teachers.translation.ui') === 'he' ? 'he' : 'en'; } catch (_) {}
  let rounds = [], items = [], index = 0, stage = 0, loaded = false, remotePromise, toastTimer, touchStart = null;
  const translations = () => ui[lang];
  const item = () => items[index];
  const stateNumber = () => index * 3 + stage + 1;

  function toast(message) {
    clearTimeout(toastTimer); $('toast').textContent = message; $('toast').hidden = false;
    toastTimer = setTimeout(() => { $('toast').hidden = true; }, 2500);
  }
  function setText(id, value) { $(id).textContent = value; }
  function setLanguage(el, code) { el.lang = code; el.dir = code === 'he' ? 'rtl' : 'ltr'; }
  function readHash() {
    const values = new URLSearchParams(location.hash.replace(/^#/, ''));
    index = Math.max(0, Math.min(items.length - 1, (Number(values.get('q')) || 1) - 1));
    stage = Math.max(0, Math.min(2, Number(values.get('s')) || 0));
    index = Math.floor(index); stage = Math.floor(stage);
  }
  function writeHash() { history.replaceState(null, '', '#q=' + item().id + '&s=' + stage); }
  function setLabels() {
    const t = translations();
    document.documentElement.lang = lang;
    document.body.classList.toggle('ui-he', lang === 'he');
    $('language').setAttribute('aria-pressed', String(lang === 'he'));
    $('language').textContent = lang === 'he' ? 'English' : 'עברית';
    const labels = {'class-label':t.classLabel,'worksheet-link':t.worksheet,'menu-open':t.menu,'menu-title':t.menuTitle,'menu-help':t.menuHelp,'menu-worksheet':t.worksheetFull,'menu-key':t.key,'copy-link':t.copy,'fullscreen':t.full,'prev':t.previous,'restart':t.restart,'menu-class':t.classMaterials,'menu-school':t.school,'rounds-label':t.rounds,'menu-footnote':t.footnote,'step-label':t.step,'key-help':t.keyHelp,'explanation-label':t.notice,'completion':t.completion};
    for (const [id, text] of Object.entries(labels)) setText(id, text);
    $('phone-remote').title = t.remote;
    $('menu-close').setAttribute('aria-label', lang === 'he' ? 'סגירת התפריט' : 'Close menu');
    $('round-picker').replaceChildren(...rounds.map(round => {
      const button = document.createElement('button'); button.type = 'button';
      button.classList.toggle('active', round.id === item()?.round.id);
      const number = document.createElement('b'); number.textContent = String(round.id).padStart(2, '0');
      const title = document.createElement('span'); title.textContent = lang === 'he' ? round.titleHe : round.titleEn;
      button.append(number, title); button.addEventListener('click', () => { index = items.findIndex(q => q.round.id === round.id); stage = 0; closeMenu(); render(true); });
      return button;
    }));
  }
  function render(newQuestion = false) {
    if (!loaded) return;
    const q = item(), t = translations(), targetLang = q.sourceLang === 'he' ? 'en' : 'he';
    setText('round-number', t.round + ' ' + String(q.round.id).padStart(2, '0') + ' / 10');
    setText('round-title', lang === 'he' ? q.round.titleHe : q.round.titleEn);
    $('level').className = 'level ' + q.level; setText('level', t[q.level]);
    $('cycle').replaceChildren(...Array.from({length:7}, (_, pos) => { const el = document.createElement('span'); el.className = pos === q.roundIndex ? 'current' : pos < q.roundIndex ? 'done' : ''; return el; }));
    $('cycle').setAttribute('aria-label', lang === 'he' ? 'קל, מתאים, קל, מתאים, קל, מתאים, קשה' : 'Easy, core, easy, core, easy, core, stretch');
    setText('direction', q.sourceLang === 'he' ? t.toEn : t.toHe);
    setText('task-type', q.type === 'choice' ? t.choice : t.open);
    setText('prompt', q.prompt); setLanguage($('prompt'), q.sourceLang);
    $('prompt').classList.toggle('long', q.prompt.length > 86);
    const cue = lang === 'he' ? q.cueHe : q.cueEn;
    setText('cue', cue || ''); $('cue').hidden = !cue; setLanguage($('cue'), lang);
    $('choices').hidden = q.type !== 'choice';
    $('choices').replaceChildren(...(q.options || []).map((option, n) => {
      const li = document.createElement('li'); li.className = 'choice'; setLanguage(li, targetLang);
      if (stage >= 1) li.classList.add(option.correct ? 'correct' : 'wrong');
      const marker = document.createElement('span'); marker.className = 'choice-number'; marker.textContent = stage >= 1 && option.correct ? '✓' : String(n + 1);
      const text = document.createElement('span'); text.className = 'choice-text'; text.textContent = option.text;
      li.append(marker, text); return li;
    }));
    $('think').hidden = q.type !== 'open'; setText('think', t.think);
    setText('answer-label', q.type === 'choice' ? t.correct : t.answer);
    setText('answer', q.answer); setLanguage($('answer'), targetLang);
    setText('explanation', lang === 'he' ? q.explanationHe : q.explanationEn); setLanguage($('explanation'), lang);
    for (const [id, visible] of [['answer-row', stage >= 1], ['explanation-row', stage >= 2]]) { $(id).classList.toggle('shown', visible); $(id).setAttribute('aria-hidden', String(!visible)); }
    const finished = index === items.length - 1 && stage === 2;
    $('completion').hidden = !finished;
    setText('question-count', t.question + ' ' + q.id + ' / ' + items.length);
    setText('counter', stateNumber() + ' / ' + (items.length * 3));
    setText('next-label', finished ? t.done : t.next[stage]);
    $('next').disabled = finished;
    $('prev').disabled = index === 0 && stage === 0;
    $('progress-fill').style.width = (stateNumber() / (items.length * 3) * 100) + '%';
    $('progress').setAttribute('aria-valuenow', String(stateNumber()));
    $('phone-remote').hidden = index !== 0;
    $('challenge').dataset.question = String(q.id); $('challenge').dataset.stage = String(stage);
    $('challenge').setAttribute('aria-busy', 'false');
    writeHash();
    if (newQuestion) window.scrollTo({top:0, behavior:'instant'});
    else if (stage > 0) {
      requestAnimationFrame(() => {
        const el = $(stage === 1 ? 'answer-row' : 'explanation-row');
        const rect = el.getBoundingClientRect(), bottom = innerHeight - $('next').closest('footer').offsetHeight - 12;
        if (rect.bottom > bottom) window.scrollBy({top:rect.bottom - bottom, behavior:'instant'});
      });
    }
    document.dispatchEvent(new CustomEvent('translation-step', {detail:{question:q.id, stage, step:stateNumber(), total:items.length * 3}}));
  }
  function closeMenu() { if ($('menu').open) $('menu').close(); $('lesson').focus({preventScroll:true}); }
  function next() {
    if (!loaded || controllerMode) return;
    if ($('menu').open) closeMenu();
    if (stage < 2) { stage++; render(); }
    else if (index < items.length - 1) { index++; stage = 0; render(true); }
  }
  function previous() {
    if (!loaded || controllerMode) return;
    if (stage > 0) { stage--; render(); }
    else if (index > 0) { index--; stage = 2; render(true); }
  }
  window.next = next; window.prev = previous;
  window.grade8Translation = {next,previous,get state(){return {ready:loaded,index,question:item()?.id,stage,step:stateNumber(),total:items.length*3};}};
  $('next').addEventListener('click', next);
  $('prev').addEventListener('click', () => { closeMenu(); previous(); });
  document.addEventListener('keydown', e => {
    if (controllerMode || e.ctrlKey || e.altKey || e.metaKey || e.key !== 'ArrowDown') return;
    e.preventDefault(); e.stopImmediatePropagation();
    if (e.repeat) return;
    const remote = document.getElementById('teachers-qr-remote-host')?.shadowRoot;
    if (remote && !remote.getElementById('overlay')?.hidden) remote.getElementById('close')?.click();
    next();
  }, true);
  $('menu-open').addEventListener('click', () => { setLabels(); $('menu').showModal(); });
  $('menu-close').addEventListener('click', closeMenu);
  $('menu').addEventListener('click', e => { if(e.target === $('menu')) { const r=$('menu').getBoundingClientRect(); if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeMenu(); } });
  $('language').addEventListener('click', () => { lang = lang === 'en' ? 'he' : 'en'; try {localStorage.setItem('teachers.translation.ui',lang);} catch (_) {} setLabels(); render(); $('lesson').focus({preventScroll:true}); });
  $('restart').addEventListener('click', () => { index = 0; stage = 0; closeMenu(); render(true); });
  $('copy-link').addEventListener('click', async () => { try { await navigator.clipboard.writeText(location.href); toast(translations().copied); } catch (_) { toast(translations().copyFail); } });
  $('fullscreen').addEventListener('click', async () => { closeMenu(); try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); } catch (_) {} });
  window.addEventListener('hashchange', () => { if(loaded){readHash();render(true);} });

  // A local swipe is the same single-step action as Down Arrow. No answers are entered.
  $('lesson').addEventListener('touchstart', e => { if(e.touches.length===1)touchStart={x:e.touches[0].clientX,y:e.touches[0].clientY}; else touchStart=null; }, {passive:true});
  $('lesson').addEventListener('touchend', e => {
    if (!touchStart || e.changedTouches.length !== 1) return;
    const dx=e.changedTouches[0].clientX-touchStart.x, dy=e.changedTouches[0].clientY-touchStart.y; touchStart=null;
    if(Math.abs(dy)>=65&&Math.abs(dy)>Math.abs(dx)*1.3){if(dy<0)next();else previous();}
  }, {passive:true});
  $('lesson').addEventListener('touchcancel', () => {touchStart=null;}, {passive:true});

  // Load the existing shared remote only on request. Its automatic opening panel
  // must never interrupt the teacher's Down-Arrow-only lesson.
  function loadPhoneRemote() {
    if (remotePromise) return remotePromise;
    remotePromise = new Promise((resolve,reject) => {
      const script=document.createElement('script'); script.src='../../shared/phone-remote/remote.js'; script.dataset.teacherPhoneRemote='shared';
      script.onload=()=>{
        const shadow=document.getElementById('teachers-qr-remote-host')?.shadowRoot;
        if(!shadow){reject(new Error('Phone remote did not initialize'));return;}
        if(!controllerMode){const style=document.createElement('style');style.textContent='#launch{display:none!important}';shadow.append(style);}
        resolve(shadow);
      };
      script.onerror=()=>{remotePromise=null;reject(new Error('Phone remote could not load'));}; document.body.append(script);
    });
    return remotePromise;
  }
  $('phone-remote').addEventListener('click', async () => {try{const shadow=await loadPhoneRemote();shadow.getElementById('launch').click();}catch(_){toast(translations().remoteError);} });
  if(controllerMode)loadPhoneRemote().catch(()=>toast(translations().remoteError));

  fetch('data.json').then(r=>{if(!r.ok)throw new Error('Lesson data unavailable');return r.json();}).then(data=>{
    rounds=data.rounds;
    items=rounds.flatMap(round=>round.items.map((q,roundIndex)=>({...q,round,roundIndex})));
    if(items.length!==70||rounds.length!==10)throw new Error('Incomplete lesson data');
    loaded=true;readHash();setLabels();render(true);
    if(!controllerMode)$('lesson').focus({preventScroll:true});
  }).catch(error=>{
    console.error(error); $('load-error').hidden=false;
    $('load-error').textContent='The lesson could not load. Please refresh, or use the worksheet PDF. לא ניתן לטעון את המצגת. אפשר לרענן או לפתוח את דף העבודה.';
    $('next').disabled=true;
  });
})();
