/* Module E: challenging translation slides, hints and reveal feedback. */
(() => {
  'use strict';
  /* A phone controller is not another player session on this origin. */
  if (new URLSearchParams(location.search).has('teacherRemote')) {
    const shell = document.querySelector('.app-shell');
    if (shell) shell.hidden = true;
    return;
  }
  const DATA = window.TRANSLATION_E_DATA;
  if (!DATA || !Array.isArray(DATA.rounds)) {
    console.error('Translation Challenge: content did not load.');
    return;
  }
  const rounds = DATA.rounds;
  const items = rounds.flatMap(round => round.items);
  const byId = new Map(items.map(item => [item.id, item]));
  const roundById = new Map(rounds.map(round => [round.id, round]));
  const itemRound = new Map(rounds.flatMap(round => round.items.map(item => [item.id, round])));
  const STORAGE_KEY = 'teachers.module-e.translation-challenge.slides.v2';
  const LANGUAGE_KEY = 'teachers.module-e.translation-challenge.language';
  const $ = id => document.getElementById(id);

  const I18N = {
    en: {
      eyebrow: 'GRADE 11 · MODULE E', title: 'Translation Challenge',
      subtitle: '70 sentences. Two languages. One focus at a time.',
      start: 'Start the challenge', resume: 'Continue where I stopped', rounds: 'Choose a round',
      backToClass: 'Grade 11 materials', copyLink: 'Copy link', fullscreen: 'Full screen',
      howToTitle: 'How to play',
      howToText: 'Think of a translation or say it aloud. Use a hint when you need one, then reveal a possible answer.',
      howToStep1: 'Translate the sentence in your own words.',
      howToStep2: 'Use a hint or word help when you need it.',
      howToStep3: 'Reveal an answer and explore the highlighted focus.',
      translationNote: 'There is more than one correct translation. Explore the meaning and the focus.',
      progressNote: 'Your place and the slides you explore stay on this device.',
      chooseRound: 'Choose a focus', close: 'Close',
      hint: 'Hint', hideHint: 'Hide hint', vocabulary: 'Word help', hideVocabulary: 'Hide word help',
      reveal: 'Reveal an answer', answerRevealed: 'Answer revealed', flag: 'Practise again',
      flagged: 'Marked for another look', previous: 'Previous', next: 'Next sentence',
      finishRound: 'Finish this round', continueRound: 'Next round',
      repeatRound: 'Repeat this round in a new order', reviewDifficult: 'Revisit marked sentences',
      summaryChooseRound: 'Choose another focus', restart: 'Reset slide progress',
      modelAnswer: 'One possible translation', explanation: 'The focus',
      roundsTitle: 'Ten focused rounds', emptyProgress: 'Ready when you are',
      footerHelp: 'Arrow keys or swipe up / down when the page does not need scrolling.',
      round: 'Round', sentences: 'sentences', intoEnglish: 'Translate into English', intoHebrew: 'Translate into Hebrew',
      copied: 'Link copied.', copyFailed: 'Copy the link from your address bar.',
      fullscreenUnavailable: 'Full screen is not available in this browser.',
      roundSummary: 'End of the round', roundComplete: 'Round explored', gameSummary: 'You reached the final slide',
      summaryRoundText: 'Continue to a new focus, or explore these seven sentences again.',
      summaryGameText: 'Choose a focus to revisit any sentences you want to explore again.',
      revealedCount: 'Answers revealed', of: 'of', noneMarked: 'No sentences are marked in this round yet.',
      practiceStarted: 'The same focus, with the answers hidden again.',
      resetConfirm: 'Reset the saved place and slide progress for this game on this device?',
      resetDone: 'Slide progress reset.', sessionOnly: 'Progress is available for this visit only.',
      language: 'Show explanations in Hebrew', languageEnglish: 'Show explanations in English',
      vocabularyHelp: 'English and Hebrew word help',
      challenges: 'challenges', roundsLabel: 'focused rounds', bothDirections: 'both directions',
      roundsDescription: 'Seven sentences in every round.', teacherGuide: 'How to play & controls',
      keyboardNote: 'Use Up / Down or Page Up / Page Down to move. Space reveals an answer. Swipe up or down when the page does not need scrolling.',
      remoteNote: 'Open the QR button to connect a phone remote. Scan the QR and approve the connection on the computer.',
      currentFocus: 'CURRENT FOCUS', reflection: 'ROUND COMPLETE',
      smallPrint: '70 original challenges · One focus at a time', challengeProgress: 'Challenge position',
      ready: 'Ready to translate', explored: 'answers explored'
    },
    he: {
      eyebrow: 'כיתה י״א · שאלון E', title: 'אתגר התרגום',
      subtitle: '70 משפטים. שתי שפות. מוקד אחד בכל פעם.',
      start: 'מתחילים באתגר', resume: 'המשך מהמקום שעצרתי', rounds: 'בחירת סבב',
      backToClass: 'חומרי הלמידה של כיתה י״א', copyLink: 'העתקת קישור', fullscreen: 'מסך מלא',
      howToTitle: 'איך משחקים',
      howToText: 'חושבים על תרגום או אומרים אותו בקול. נעזרים ברמז לפי הצורך, ואז חושפים תשובה אפשרית.',
      howToStep1: 'מתרגמים את המשפט במילים שלכם.',
      howToStep2: 'נעזרים ברמז או במילות העזר לפי הצורך.',
      howToStep3: 'חושפים תשובה ומתבוננים במוקד המודגש.',
      translationNote: 'יש יותר מתרגום נכון אחד. שימו לב למשמעות ולמוקד התרגול.',
      progressNote: 'המיקום והשקפים שפתחתם נשמרים במכשיר הזה.',
      chooseRound: 'בחירת מוקד לתרגול', close: 'סגירה',
      hint: 'רמז', hideHint: 'הסתרת הרמז', vocabulary: 'מילות עזר', hideVocabulary: 'הסתרת מילות העזר',
      reveal: 'חשיפת תשובה', answerRevealed: 'התשובה נחשפה', flag: 'לחזור למשפט',
      flagged: 'סומן לעיון חוזר', previous: 'הקודם', next: 'המשפט הבא',
      finishRound: 'סיום הסבב', continueRound: 'לסבב הבא',
      repeatRound: 'אותו סבב בסדר חדש', reviewDifficult: 'חזרה למשפטים שסומנו',
      summaryChooseRound: 'בחירת מוקד אחר', restart: 'איפוס ההתקדמות בשקפים',
      modelAnswer: 'תרגום אפשרי', explanation: 'מוקד התרגול',
      roundsTitle: 'עשרה סבבים ממוקדים', emptyProgress: 'אפשר להתחיל',
      footerHelp: 'חיצי המקלדת או החלקה מעלה ומטה כאשר אין צורך בגלילת העמוד.',
      round: 'סבב', sentences: 'משפטים', intoEnglish: 'תרגמו לאנגלית', intoHebrew: 'תרגמו לעברית',
      copied: 'הקישור הועתק.', copyFailed: 'אפשר להעתיק את הקישור משורת הכתובת.',
      fullscreenUnavailable: 'מסך מלא אינו זמין בדפדפן הזה.',
      roundSummary: 'הגעתם לסוף הסבב', roundComplete: 'כל תשובות הסבב נחשפו', gameSummary: 'הגעתם לשקף האחרון',
      summaryRoundText: 'אפשר להמשיך למוקד חדש או לחזור לשבעת המשפטים האלה.',
      summaryGameText: 'בחרו מוקד כדי לחזור למשפטים שתרצו לתרגל שוב.',
      revealedCount: 'תשובות שנחשפו', of: 'מתוך', noneMarked: 'עדיין לא סומנו משפטים לחזרה בסבב הזה.',
      practiceStarted: 'אותו מוקד, כשהתשובות שוב מוסתרות.',
      resetConfirm: 'לאפס את המיקום וההתקדמות בשקפים במשחק הזה במכשיר הזה?',
      resetDone: 'ההתקדמות בשקפים אופסה.', sessionOnly: 'ההתקדמות זמינה לביקור הנוכחי בלבד.',
      language: 'הצגת ההסברים בעברית', languageEnglish: 'הצגת ההסברים באנגלית',
      vocabularyHelp: 'מילות עזר באנגלית ובעברית',
      challenges: 'אתגרים', roundsLabel: 'סבבים ממוקדים', bothDirections: 'בשני הכיוונים',
      roundsDescription: 'שבעה משפטים בכל סבב.', teacherGuide: 'איך משחקים ודרכי שליטה',
      keyboardNote: 'חיצי מעלה ומטה או Page Up ו־Page Down משנים משפט. רווח חושף תשובה. אפשר להחליק מעלה ומטה כאשר אין צורך בגלילת העמוד.',
      remoteNote: 'פותחים את כפתור ה־QR לחיבור שלט בטלפון. סורקים את הקוד ומאשרים את החיבור במחשב.',
      currentFocus: 'מוקד הסבב', reflection: 'סוף הסבב',
      smallPrint: '70 אתגרים מקוריים · מוקד אחד בכל פעם', challengeProgress: 'המיקום במשחק',
      ready: 'מוכנים לתרגום', explored: 'תשובות נחשפו'
    }
  };
  window.TRANSLATION_GAME_I18N = I18N;
  const freshState = () => ({ schema: 2, language: 'en', answers: {}, lastId: 1,
    queue: items.map(item => item.id), position: 0, mode: 'full', screen: 'home', resumeScreen: 'game', summaryRound: 1 });
  let state = freshState();
  let toastTimer = 0;
  let storageWarningShown = false;
  function loadState() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (saved && saved.schema === 2) {
        state.language = saved.language === 'he' ? 'he' : 'en';
        state.lastId = byId.has(saved.lastId) ? saved.lastId : 1;
        if (saved.answers && typeof saved.answers === 'object') {
          for (const item of items) {
            const value = saved.answers[item.id];
            if (!value || typeof value !== 'object') continue;
            state.answers[item.id] = { revealed: value.revealed === true, explored: value.explored === true,
              hint: value.hint === true, vocabulary: value.vocabulary === true,
              flagged: value.flagged === true, visited: value.visited === true };
          }
        }
        const validQueue = Array.isArray(saved.queue) && saved.queue.length > 0 && saved.queue.length <= items.length &&
          saved.queue.every(id => byId.has(id)) && new Set(saved.queue).size === saved.queue.length;
        if (validQueue) {
          state.queue = saved.queue;
          state.position = Math.max(0, Math.min(Number.isInteger(saved.position) ? saved.position : 0, saved.queue.length - 1));
        }
        state.mode = ['full', 'round', 'shuffle', 'review'].includes(saved.mode) ? saved.mode : 'full';
        if (state.mode !== 'full' && new Set(state.queue.map(id => itemRound.get(id).id)).size > 1) {
          state.queue = itemRound.get(state.lastId).items.map(item => item.id);
          state.position = Math.max(0, state.queue.indexOf(state.lastId)); state.mode = 'round';
        }
        state.screen = ['home', 'game', 'summary'].includes(saved.screen) ? saved.screen : 'home';
        state.resumeScreen = saved.resumeScreen === 'summary' || saved.screen === 'summary' ? 'summary' : 'game';
        state.summaryRound = roundById.has(saved.summaryRound) ? saved.summaryRound : 1;
      }
      const language = localStorage.getItem(LANGUAGE_KEY);
      if (language === 'he' || language === 'en') state.language = language;
    } catch (_) { /* Slides remain usable when browser storage is disabled. */ }
  }
  const t = key => I18N[state.language][key] || I18N.en[key] || key;
  const local = (object, field) => object[field + (state.language === 'he' ? 'He' : 'En')] || object[field + 'He'] || '';
  function entry(id) {
    if (!state.answers[id]) state.answers[id] = { revealed: false, explored: false, hint: false,
      vocabulary: false, flagged: false, visited: false };
    return state.answers[id];
  }
  function currentItem() { return byId.get(state.queue[state.position]) || byId.get(state.lastId) || items[0]; }
  function currentRound() { return itemRound.get(currentItem().id); }
  function hasProgress() { return Object.values(state.answers).some(value => value.visited || value.explored || value.flagged); }
  function persist() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      localStorage.setItem(LANGUAGE_KEY, state.language);
    } catch (_) {
      if (!storageWarningShown) { storageWarningShown = true; toast(t('sessionOnly')); }
    }
  }
  function toast(message) {
    const element = $('toast'); if (!element) return;
    clearTimeout(toastTimer); element.textContent = message; element.hidden = false; element.classList.add('visible');
    toastTimer = setTimeout(() => { element.classList.remove('visible'); element.hidden = true; }, 3200);
  }
  function show(element, visible) {
    if (element) { element.hidden = !visible; element.classList.toggle('hidden', !visible); }
  }
  function syncRemoteLauncher() {
    const host = $('teachers-qr-remote-host');
    if (!host || !host.shadowRoot) return false;
    if (!host.shadowRoot.getElementById('translation-launcher-rule')) {
      const style = document.createElement('style');
      style.id = 'translation-launcher-rule';
      style.textContent = ':host([data-translation-hide-launch]) #launch { display: none !important; }';
      host.shadowRoot.append(style);
    }
    host.toggleAttribute('data-translation-hide-launch', state.screen !== 'home');
    return true;
  }
  function setScreen(screen) {
    state.screen = screen; if (screen !== 'home') state.resumeScreen = screen;
    for (const name of ['home', 'game', 'summary']) show($(name + 'Screen'), name === screen);
    document.body.dataset.screen = screen;
    if ($('counter')) $('counter').textContent = screen === 'home' ? '1 / 72' : screen === 'summary' ? '72 / 72' : (currentItem().id + 1) + ' / 72';
    syncRemoteLauncher();
  }
  function exploredCount(list = items) { return list.filter(item => state.answers[item.id] && state.answers[item.id].explored).length; }
  function updateResume() {
    show($('resumeGame'), hasProgress());
    if ($('restartButton')) $('restartButton').disabled = !hasProgress();
  }
  function applyLanguage() {
    document.documentElement.lang = state.language; document.documentElement.dir = state.language === 'he' ? 'rtl' : 'ltr';
    document.body.classList.toggle('hebrew-ui', state.language === 'he');
    for (const element of document.querySelectorAll('[data-i18n]')) {
      if (I18N[state.language][element.dataset.i18n]) element.textContent = t(element.dataset.i18n);
    }
    if ($('languageToggle')) {
      $('languageToggle').textContent = state.language === 'en' ? 'עברית' : 'English';
      $('languageToggle').setAttribute('aria-pressed', String(state.language === 'he'));
      $('languageToggle').setAttribute('aria-label', t(state.language === 'en' ? 'language' : 'languageEnglish'));
    }
    if ($('roundDialog')) $('roundDialog').setAttribute('aria-label', t('chooseRound'));
    updateResume();
  }
  function makeRoundCard(round) {
    const button = document.createElement('button'); button.type = 'button'; button.className = 'round-card'; button.dataset.round = String(round.id);
    const count = exploredCount(round.items);
    const meta = document.createElement('span'); meta.className = 'round-meta'; meta.textContent = t('round') + ' ' + round.id + ' · ' + round.items.length + ' ' + t('sentences');
    const name = document.createElement('span'); name.className = 'round-name'; name.textContent = local(round, 'title');
    const bar = document.createElement('span'); bar.className = 'round-progress'; bar.setAttribute('aria-hidden', 'true');
    const fill = document.createElement('span'); fill.style.width = (count / round.items.length * 100) + '%'; bar.append(fill);
    button.append(meta, name, bar);
    button.setAttribute('aria-label', local(round, 'title') + '. ' + meta.textContent + '. ' + count + ' ' + t('explored'));
    button.classList.toggle('is-complete', count === round.items.length);
    if (state.screen !== 'home' && currentRound().id === round.id) { button.classList.add('is-current'); button.setAttribute('aria-current', 'step'); }
    button.addEventListener('click', () => { closeRoundDialog(); startRound(round.id); });
    return button;
  }
  function renderRoundGrids() {
    for (const id of ['roundGrid', 'dialogRoundGrid']) if ($(id)) $(id).replaceChildren(...rounds.map(makeRoundCard));
  }
  function updateHash(id) {
    const url = new URL(location.href); url.hash = id ? 'q=' + id : ''; history.replaceState(null, '', url);
  }
  function highlightAnswer(element, text, highlights) {
    element.replaceChildren();
    const ranges = [];
    for (const phrase of highlights || []) {
      if (typeof phrase !== 'string' || !phrase) continue;
      let start = text.indexOf(phrase);
      while (start >= 0) { ranges.push({ start, end: start + phrase.length }); start = text.indexOf(phrase, start + phrase.length); }
    }
    ranges.sort((a, b) => a.start - b.start || b.end - a.end);
    let cursor = 0;
    for (const range of ranges) {
      if (range.start < cursor) continue;
      element.append(document.createTextNode(text.slice(cursor, range.start)));
      const mark = document.createElement('mark'); mark.textContent = text.slice(range.start, range.end); element.append(mark); cursor = range.end;
    }
    element.append(document.createTextNode(text.slice(cursor)));
  }
  function renderVocabulary(round) {
    const panel = $('vocabPanel'); if (!panel) return;
    const list = document.createElement('dl'); list.className = 'vocabulary-list'; list.setAttribute('aria-label', t('vocabularyHelp'));
    for (const word of round.glossary || []) {
      const row = document.createElement('div'); row.className = 'vocabulary-row';
      const term = document.createElement('dt'); term.lang = 'en'; term.dir = 'ltr'; term.textContent = word.en; row.append(term);
      if (word.he) { const meaning = document.createElement('dd'); meaning.lang = 'he'; meaning.dir = 'rtl'; meaning.textContent = word.he; row.append(meaning); }
      list.append(row);
    }
    panel.replaceChildren(list);
  }
  function updateFeedback() {
    const revealed = entry(currentItem().id).revealed;
    $('stage').classList.toggle('is-revealed', revealed);
    $('stage').dataset.phase = revealed ? 'revealed' : 'challenge';
    if ($('challengeStatus')) {
      $('challengeStatus').textContent = t(revealed ? 'answerRevealed' : 'ready');
      $('challengeStatus').classList.toggle('is-revealed', revealed);
    }
  }
  function atRoundEnd() {
    const nextId = state.queue[state.position + 1];
    return !nextId || itemRound.get(nextId).id !== currentRound().id;
  }
  function renderGame(focus = false) {
    const item = currentItem(), round = itemRound.get(item.id), value = entry(item.id);
    state.lastId = item.id; value.visited = true; setScreen('game');
    $('roundTitle').textContent = local(round, 'title'); $('roundFocus').textContent = local(round, 'focus');
    const instruction = local(round, 'instruction'); $('roundInstruction').textContent = instruction; show($('roundInstruction'), Boolean(instruction));
    $('directionLabel').textContent = t(item.direction === 'he-en' ? 'intoEnglish' : 'intoHebrew'); $('directionLabel').dataset.direction = item.direction;
    $('promptText').textContent = item.source; $('promptText').lang = item.direction === 'he-en' ? 'he' : 'en';
    $('promptText').dir = item.direction === 'he-en' ? 'rtl' : 'ltr'; $('promptText').tabIndex = -1;
    $('hintPanel').textContent = local(round, 'hint'); show($('hintPanel'), value.hint);
    $('hintButton').textContent = t(value.hint ? 'hideHint' : 'hint'); $('hintButton').setAttribute('aria-expanded', String(value.hint));
    renderVocabulary(round); show($('vocabPanel'), value.vocabulary);
    $('vocabButton').textContent = t(value.vocabulary ? 'hideVocabulary' : 'vocabulary'); $('vocabButton').setAttribute('aria-expanded', String(value.vocabulary));
    $('vocabButton').disabled = !round.glossary || !round.glossary.length;
    highlightAnswer($('answerText'), item.answer, item.answerHighlights);
    $('answerText').lang = item.direction === 'he-en' ? 'en' : 'he'; $('answerText').dir = item.direction === 'he-en' ? 'ltr' : 'rtl';
    $('explanationText').textContent = local(round, 'explanation'); show($('answerPanel'), value.revealed);
    const explanation = $('answerPanel').querySelector('details'); if (explanation) explanation.open = false;
    $('reveal').textContent = t(value.revealed ? 'answerRevealed' : 'reveal'); $('reveal').setAttribute('aria-expanded', String(value.revealed)); $('reveal').disabled = value.revealed;
    $('flagButton').textContent = t(value.flagged ? 'flagged' : 'flag'); $('flagButton').setAttribute('aria-pressed', String(value.flagged)); $('flagButton').classList.toggle('is-flagged', value.flagged);
    $('prev').disabled = state.position === 0; $('prev').textContent = t('previous'); $('next').textContent = t(atRoundEnd() ? 'finishRound' : 'next');
    $('progressText').textContent = item.id + ' / ' + items.length;
    $('progressText').setAttribute('aria-label', t('round') + ' ' + round.id + ', ' + (round.items.findIndex(candidate => candidate.id === item.id) + 1) + ' / ' + round.items.length);
    $('progressBar').max = items.length; $('progressBar').value = item.id;
    $('progressBar').setAttribute('aria-label', t('challengeProgress')); $('progressBar').setAttribute('aria-valuetext', item.id + ' / ' + items.length);
    updateFeedback(); updateResume(); updateHash(item.id); persist();
    if (focus) $('promptText').focus({ preventScroll: true });
  }
  function showHome() { setScreen('home'); updateHash(null); applyLanguage(); renderRoundGrids(); persist(); }
  function startGame() { state.queue = items.map(item => item.id); state.position = 0; state.mode = 'full'; renderGame(true); }
  function startRound(id, mode = 'round', queue = null) {
    const round = roundById.get(id); if (!round) return;
    state.queue = queue || round.items.map(item => item.id); state.position = 0; state.mode = mode; renderGame(true);
  }
  function reveal() {
    if (state.screen !== 'game') return;
    const value = entry(currentItem().id); if (value.revealed) return;
    value.revealed = true; value.explored = true; show($('answerPanel'), true);
    $('reveal').textContent = t('answerRevealed'); $('reveal').setAttribute('aria-expanded', 'true'); $('reveal').disabled = true;
    updateFeedback(); persist();
  }
  function renderSummary() {
    setScreen('summary');
    const round = roundById.get(state.summaryRound) || currentRound();
    const full = state.mode === 'full' && state.position === state.queue.length - 1;
    const set = full ? items : round.items; const count = exploredCount(set);
    $('summaryTitle').textContent = full ? t('gameSummary') : t(count === round.items.length ? 'roundComplete' : 'roundSummary') + ': ' + local(round, 'title');
    $('summaryText').textContent = t(full ? 'summaryGameText' : 'summaryRoundText');
    if ($('summaryStats')) {
      const caption = document.createElement('p'); caption.className = 'summary-caption';
      caption.textContent = t('revealedCount') + ': ' + count + ' ' + t('of') + ' ' + set.length;
      $('summaryStats').replaceChildren(caption);
    }
    show($('summaryContinue'), Boolean(rounds.find(candidate => candidate.id > round.id)));
    $('summaryContinue').textContent = t('continueRound'); $('repeatRound').textContent = t('repeatRound');
    const marked = round.items.filter(item => entry(item.id).flagged).length;
    $('reviewDifficult').textContent = t('reviewDifficult') + (marked ? ' (' + marked + ')' : '');
    $('reviewDifficult').disabled = marked === 0; $('reviewDifficult').title = marked ? '' : t('noneMarked');
    updateResume(); renderRoundGrids(); persist(); $('summaryTitle').tabIndex = -1; $('summaryTitle').focus({ preventScroll: true });
  }
  function next() {
    if (state.screen === 'home') { startGame(); return; }
    if (state.screen === 'summary') { continueRound(); return; }
    if (atRoundEnd()) { state.summaryRound = currentRound().id; renderSummary(); return; }
    state.position++; renderGame(true);
  }
  function previous() {
    if (state.screen === 'summary') { renderGame(true); return; }
    if (state.screen !== 'game' || state.position === 0) return;
    state.position--; renderGame(true);
  }
  function continueRound() {
    const round = roundById.get(state.summaryRound) || currentRound(); const nextRound = rounds.find(candidate => candidate.id > round.id);
    if (!nextRound) { openRoundDialog(); return; }
    if (state.mode === 'full') {
      state.position = state.queue.findIndex(id => itemRound.get(id).id === nextRound.id);
      if (state.position >= 0) { renderGame(true); return; }
    }
    startRound(nextRound.id);
  }
  function freshAttempt(ids) { for (const id of ids) Object.assign(entry(id), { revealed: false, hint: false, vocabulary: false }); }
  function repeatRound() {
    const round = roundById.get(state.summaryRound) || currentRound(); const queue = round.items.map(item => item.id);
    for (let index = queue.length - 1; index > 0; index--) { const other = Math.floor(Math.random() * (index + 1)); [queue[index], queue[other]] = [queue[other], queue[index]]; }
    freshAttempt(queue); startRound(round.id, 'shuffle', queue); toast(t('practiceStarted'));
  }
  function reviewDifficult() {
    const round = roundById.get(state.summaryRound) || currentRound(); const queue = round.items.filter(item => entry(item.id).flagged).map(item => item.id);
    if (!queue.length) { toast(t('noneMarked')); return; }
    freshAttempt(queue); startRound(round.id, 'review', queue); toast(t('practiceStarted'));
  }
  function openRoundDialog() {
    const dialog = $('roundDialog'); renderRoundGrids();
    if (typeof dialog.showModal === 'function') { if (!dialog.open) dialog.showModal(); }
    else { dialog.setAttribute('open', ''); show(dialog, true); }
    const first = dialog.querySelector('.is-current') || dialog.querySelector('button[data-round]'); if (first) first.focus();
  }
  function closeRoundDialog() {
    const dialog = $('roundDialog'); if (typeof dialog.close === 'function') dialog.close();
    else { dialog.removeAttribute('open'); show(dialog, false); }
  }
  async function copyLink() {
    const url = new URL(location.href); url.searchParams.delete('teacherRemote'); if (state.screen === 'game') url.hash = 'q=' + currentItem().id;
    try {
      if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(url.href);
      else {
        const field = document.createElement('textarea'); field.value = url.href; field.style.position = 'fixed'; field.style.opacity = '0';
        document.body.append(field); field.select(); const copied = document.execCommand('copy'); field.remove();
        if (!copied) throw new Error('Copy not available');
      }
      toast(t('copied'));
    } catch (_) { toast(t('copyFailed')); }
  }
  function inputTarget(event) { return event.composedPath().some(node => node instanceof Element && (node.matches('input, textarea, select') || node.isContentEditable)); }
  function overlayOpen() {
    if ($('roundDialog').open || $('roundDialog').hasAttribute('open')) return true;
    const remote = $('teachers-qr-remote-host'); const panel = remote && remote.shadowRoot && remote.shadowRoot.getElementById('overlay');
    return Boolean(panel && !panel.hidden);
  }
  function bind(id, event, fn) { if ($(id)) $(id).addEventListener(event, fn); }
  bind('startGame', 'click', startGame);
  bind('resumeGame', 'click', () => { if (state.resumeScreen === 'summary') renderSummary(); else renderGame(true); });
  bind('roundsButton', 'click', openRoundDialog); bind('summaryChooseRound', 'click', openRoundDialog);
  bind('closeRoundDialog', 'click', closeRoundDialog); bind('roundDialog', 'click', event => { if (event.target === $('roundDialog')) closeRoundDialog(); });
  bind('languageToggle', 'click', () => {
    state.language = state.language === 'en' ? 'he' : 'en'; applyLanguage(); renderRoundGrids();
    if (state.screen === 'game') renderGame(); else if (state.screen === 'summary') renderSummary(); persist();
  });
  bind('copyLink', 'click', copyLink);
  bind('fullscreenToggle', 'click', async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen(); else throw new Error('Unavailable');
    } catch (_) { toast(t('fullscreenUnavailable')); }
  });
  document.addEventListener('fullscreenchange', () => { if ($('fullscreenToggle')) $('fullscreenToggle').setAttribute('aria-pressed', String(Boolean(document.fullscreenElement))); });
  bind('hintButton', 'click', () => {
    const value = entry(currentItem().id); value.hint = !value.hint; show($('hintPanel'), value.hint);
    $('hintButton').textContent = t(value.hint ? 'hideHint' : 'hint'); $('hintButton').setAttribute('aria-expanded', String(value.hint)); persist();
  });
  bind('vocabButton', 'click', () => {
    const value = entry(currentItem().id); value.vocabulary = !value.vocabulary; show($('vocabPanel'), value.vocabulary);
    $('vocabButton').textContent = t(value.vocabulary ? 'hideVocabulary' : 'vocabulary'); $('vocabButton').setAttribute('aria-expanded', String(value.vocabulary)); persist();
  });
  bind('reveal', 'click', reveal);
  bind('flagButton', 'click', () => {
    const value = entry(currentItem().id); value.flagged = !value.flagged;
    $('flagButton').textContent = t(value.flagged ? 'flagged' : 'flag'); $('flagButton').setAttribute('aria-pressed', String(value.flagged));
    $('flagButton').classList.toggle('is-flagged', value.flagged); persist();
  });
  bind('prev', 'click', previous); bind('next', 'click', next); bind('summaryContinue', 'click', continueRound);
  bind('repeatRound', 'click', repeatRound); bind('reviewDifficult', 'click', reviewDifficult);
  bind('restartButton', 'click', () => {
    if (hasProgress() && !window.confirm(t('resetConfirm'))) return;
    const language = state.language; state = freshState(); state.language = language; showHome(); toast(t('resetDone'));
  });
  document.addEventListener('keydown', event => {
    if (event.defaultPrevented || overlayOpen() || inputTarget(event) || event.altKey || event.ctrlKey || event.metaKey) return;
    const focus = document.activeElement;
    if ((event.key === ' ' || event.key === 'Enter') && focus && focus.matches('button, a, summary')) return;
    if (['ArrowDown', 'ArrowRight', 'PageDown'].includes(event.key)) { event.preventDefault(); next(); }
    else if (['ArrowUp', 'ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); previous(); }
    else if (event.key === ' ' && state.screen === 'game') { event.preventDefault(); reveal(); }
  });
  let swipeStart = null;
  function canSwipe(target) {
    if (state.screen !== 'game' || overlayOpen() || target.closest('button, a, textarea, input, select, summary, [contenteditable]')) return false;
    for (let element = target; element && element !== document.body; element = element.parentElement) {
      const style = getComputedStyle(element); if (/(auto|scroll)/.test(style.overflowY) && element.scrollHeight > element.clientHeight + 3) return false;
    }
    const scrolling = document.scrollingElement; return !scrolling || scrolling.scrollHeight <= window.innerHeight + 6;
  }
  bind('stage', 'touchstart', event => {
    if (event.touches.length !== 1 || !canSwipe(event.target)) { swipeStart = null; return; }
    const point = event.touches[0]; swipeStart = { x: point.clientX, y: point.clientY, time: Date.now() };
  });
  if ($('stage')) $('stage').addEventListener('touchmove', event => {
    if (!swipeStart || event.touches.length !== 1) return;
    const point = event.touches[0], dx = point.clientX - swipeStart.x, dy = point.clientY - swipeStart.y;
    if (Math.abs(dy) > 15 && Math.abs(dy) > Math.abs(dx) * 1.3 && event.cancelable) event.preventDefault();
  }, { passive: false });
  if ($('stage')) $('stage').addEventListener('touchend', event => {
    const start = swipeStart; swipeStart = null; if (!start || event.changedTouches.length !== 1 || Date.now() - start.time > 1100) return;
    const point = event.changedTouches[0], dx = point.clientX - start.x, dy = point.clientY - start.y;
    if (Math.abs(dy) < 60 || Math.abs(dy) < Math.abs(dx) * 1.3) return;
    if (event.cancelable) event.preventDefault(); if (dy < 0) next(); else previous();
  }, { passive: false });
  bind('stage', 'touchcancel', () => { swipeStart = null; });
  function routeFromHash() {
    const value = new URLSearchParams(location.hash.slice(1)).get('q'); const id = value && /^\d+$/.test(value) ? Number(value) : NaN;
    if (!byId.has(id)) return false;
    state.queue = items.map(item => item.id); state.position = state.queue.indexOf(id); state.mode = 'full'; renderGame(); return true;
  }
  window.addEventListener('hashchange', () => { if (!routeFromHash()) showHome(); }); window.addEventListener('pagehide', persist);
  window.next = next; window.prev = previous;
  window.translationChallenge = Object.freeze({ getState: () => JSON.parse(JSON.stringify(state)), goToRound: id => startRound(Number(id)), next, previous, reveal });
  loadState(); applyLanguage(); renderRoundGrids();
  const savedScreen = state.screen;
  const initialValue = new URLSearchParams(location.hash.slice(1)).get('q'); const initialId = initialValue && /^\d+$/.test(initialValue) ? Number(initialValue) : NaN;
  const sameSavedItem = byId.has(initialId) && initialId === state.lastId && state.queue[state.position] === initialId && hasProgress();
  if (sameSavedItem && savedScreen !== 'home') { if (savedScreen === 'summary') renderSummary(); else renderGame(); }
  else if (!routeFromHash()) { setScreen('home'); updateResume(); }
  /* The shared remote loads after this file and mounts its own shadow root. */
  if (!syncRemoteLauncher()) {
    const remoteObserver = new MutationObserver(() => {
      if (syncRemoteLauncher()) remoteObserver.disconnect();
    });
    remoteObserver.observe(document.body, { childList: true });
  }
})();
