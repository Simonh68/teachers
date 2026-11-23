/* Translation challenge slides: no scores, grading, or answer tracking. */
(() => {
  'use strict';
  if (new URLSearchParams(location.search).has('teacherRemote')) {
    document.body.classList.add('remote-controller');
    return;
  }
  const rounds = window.TRANSLATION_DATA.rounds;
  const items = rounds.flatMap(round => round.items.map(item => ({ ...item, round })));
  const byId = new Map(items.map(item => [item.id, item]));
  const $ = id => document.getElementById(id);
  const LANG_KEY = 'teachers:translate-win:language';
  let language = 'en';
  try { if (localStorage.getItem(LANG_KEY) === 'he') language = 'he'; } catch (_) { /* Language is optional. */ }
  let currentId = Number(new URLSearchParams(location.hash.slice(1)).get('q'));
  if (!byId.has(currentId)) currentId = 1;
  let revealed = false;
  let hintVisible = false;
  let toastTimer;
  const current = () => byId.get(currentId);
  const text = {
    en: {
      courseLabel: 'Grade 12 · 4 units · Module C', backLink: 'Class materials', copyBtn: 'Copy link',
      fullBtn: 'Full screen', menuBtn: 'Rounds', focusLabel: 'Focus', hintBtn: 'Hint', hideHint: 'Hide hint',
      revealBtn: 'Show answer', hideAnswer: 'Hide answer', answerLabel: 'One possible answer',
      answerNote: 'Other natural translations can also be correct.', prevBtn: 'Previous', nextBtn: 'Next',
      startAgain: 'Back to start', roundDialogTitle: 'Choose a round', closeRoundsBtn: 'Close',
      dialogHelp: 'Five short challenges in each round. Choose any round.', shareTitle: 'Copy this link', closeShareBtn: 'Close',
      intoEnglish: 'Translate into English', intoHebrew: 'Translate into Hebrew', round: 'Round', of: 'of',
      challenge: 'Challenge', sentence: 'Sentence', copied: 'Link copied', yourTurn: 'Your turn',
      hintShown: 'Hint opened', answerShown: 'Answer revealed', focusFeedback: 'Notice',
      shortcuts: 'Arrow keys, or swipe the sentence up and down.',
      unavailableFullscreen: 'Full screen is not available in this browser.',
      finalSlide: 'Last challenge. Choose another round or return to the start.'
    },
    he: {
      courseLabel: 'כיתה י״ב · 4 יח״ל · שאלון C', backLink: 'חומרי הלמידה', copyBtn: 'העתקת קישור',
      fullBtn: 'מסך מלא', menuBtn: 'סבבים', focusLabel: 'המוקד', hintBtn: 'רמז', hideHint: 'הסתרת רמז',
      revealBtn: 'חשיפת תשובה', hideAnswer: 'הסתרת תשובה', answerLabel: 'תשובה אפשרית',
      answerNote: 'גם תרגומים טבעיים אחרים יכולים להיות נכונים.', prevBtn: 'הקודם', nextBtn: 'הבא',
      startAgain: 'חזרה להתחלה', roundDialogTitle: 'בחירת סבב', closeRoundsBtn: 'סגירה',
      dialogHelp: 'חמישה אתגרים קצרים בכל סבב. אפשר לבחור כל סבב.', shareTitle: 'העתקת הקישור', closeShareBtn: 'סגירה',
      intoEnglish: 'תרגמו לאנגלית', intoHebrew: 'תרגמו לעברית', round: 'סבב', of: 'מתוך',
      challenge: 'אתגר', sentence: 'משפט', copied: 'הקישור הועתק', yourTurn: 'תורכם לתרגם',
      hintShown: 'הרמז פתוח', answerShown: 'הפתרון נחשף', focusFeedback: 'שימו לב',
      shortcuts: 'חיצי המקלדת, או החלקה מעלה ומטה על המשפט.',
      unavailableFullscreen: 'מסך מלא אינו זמין בדפדפן הזה.',
      finalSlide: 'האתגר האחרון. אפשר לבחור סבב אחר או לחזור להתחלה.'
    }
  };
  const t = key => text[language][key];
  function notify(message) {
    clearTimeout(toastTimer);
    $('toast').textContent = message;
    $('toast').hidden = false;
    toastTimer = setTimeout(() => { $('toast').hidden = true; }, 2400);
  }
  function sentence(element, value, phrases, highlight) {
    element.replaceChildren();
    if (!highlight) { element.textContent = value; return; }
    const spans = phrases.map(phrase => ({ start: value.indexOf(phrase), end: value.indexOf(phrase) + phrase.length }))
      .filter(span => span.start >= 0).sort((a, b) => a.start - b.start);
    let position = 0;
    for (const span of spans) {
      if (span.start < position) continue;
      element.append(document.createTextNode(value.slice(position, span.start)));
      const mark = document.createElement('mark');
      mark.className = 'focus-mark'; mark.textContent = value.slice(span.start, span.end);
      element.append(mark); position = span.end;
    }
    element.append(document.createTextNode(value.slice(position)));
  }
  function renderRounds() {
    $('roundList').replaceChildren();
    for (const round of rounds) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'round-choice' + (round.id === current().round.id ? ' current' : '');
      button.dataset.round = String(round.id);
      button.setAttribute('aria-current', String(round.id === current().round.id));
      const title = document.createElement('span');
      title.textContent = `${round.id}. ${language === 'he' ? round.titleHe : round.titleEn}`;
      button.append(title);
      button.addEventListener('click', () => { $('roundDialog').close(); goTo(round.items[0].id); });
      $('roundList').append(button);
    }
  }
  function render(moveFocus = false) {
    const item = current();
    const sourceEnglish = item.direction === 'en-he';
    document.documentElement.lang = language;
    document.documentElement.dir = language === 'he' ? 'rtl' : 'ltr';
    document.body.classList.toggle('is-rtl', language === 'he');
    ['courseLabel', 'backLink', 'copyBtn', 'fullBtn', 'menuBtn', 'focusLabel', 'answerLabel', 'answerNote',
      'prevBtn', 'roundDialogTitle', 'closeRoundsBtn', 'dialogHelp', 'shareTitle', 'closeShareBtn'].forEach(id => { $(id).textContent = t(id); });
    $('langBtn').textContent = language === 'en' ? 'עברית' : 'English';
    $('langBtn').lang = language === 'en' ? 'he' : 'en';
    $('langBtn').setAttribute('aria-pressed', String(language === 'he'));
    $('langBtn').setAttribute('aria-label', language === 'en' ? 'Show Hebrew instructions' : 'הצגת הוראות באנגלית');
    $('roundMeta').textContent = `${t('round')} ${item.round.id} ${t('of')} ${rounds.length}`;
    $('roundTitle').textContent = language === 'he' ? item.round.titleHe : item.round.titleEn;
    $('focusText').textContent = item.round.focus; $('focusText').dir = 'ltr';
    $('globalProgress').value = currentId;
    $('globalProgress').setAttribute('aria-label', language === 'he' ? 'מיקום בשקפים' : 'Slide position');
    $('progressText').textContent = `${t('sentence')} ${item.round.items.findIndex(row => row.id === item.id) + 1} ${t('of')} 5`;
    $('directionLabel').textContent = t(sourceEnglish ? 'intoHebrew' : 'intoEnglish');
    const source = $('sourceSentence');
    source.dir = sourceEnglish ? 'ltr' : 'rtl'; source.lang = sourceEnglish ? 'en' : 'he';
    sentence(source, sourceEnglish ? item.en : item.he, item.focusEn, sourceEnglish && revealed);
    const answer = $('answerSentence');
    answer.dir = sourceEnglish ? 'rtl' : 'ltr'; answer.lang = sourceEnglish ? 'he' : 'en';
    sentence(answer, sourceEnglish ? item.he : item.en, item.focusEn, !sourceEnglish && revealed);
    $('hintText').textContent = language === 'he' ? item.round.hintHe : item.round.hintEn;
    $('hintText').dir = language === 'he' ? 'rtl' : 'ltr'; $('hintText').hidden = !hintVisible;
    $('hintBtn').textContent = t(hintVisible ? 'hideHint' : 'hintBtn');
    $('hintBtn').setAttribute('aria-expanded', String(hintVisible));
    $('answerPanel').hidden = !revealed;
    $('revealBtn').textContent = t(revealed ? 'hideAnswer' : 'revealBtn');
    $('revealBtn').setAttribute('aria-expanded', String(revealed));
    $('gameState').textContent = t(revealed ? 'answerShown' : hintVisible ? 'hintShown' : 'yourTurn');
    $('gameState').dataset.state = revealed ? 'answer' : hintVisible ? 'hint' : 'challenge';
    $('playScreen').classList.toggle('is-revealed', revealed);
    $('focusFeedback').replaceChildren(document.createTextNode(t('focusFeedback') + ': '));
    const focus = document.createElement('strong'); focus.dir = 'ltr'; focus.textContent = item.round.focus;
    $('focusFeedback').append(focus);
    $('prevBtn').disabled = currentId === 1;
    $('nextBtn').textContent = t(currentId === items.length ? 'startAgain' : 'nextBtn');
    $('questionMeta').replaceChildren(document.createTextNode(t('challenge') + ' '));
    const counter = document.createElement('span');
    counter.id = 'counter'; counter.dir = 'ltr'; counter.textContent = currentId + ' / ' + items.length;
    $('questionMeta').append(counter);
    $('statusMessage').textContent = currentId === items.length ? t('finalSlide') : '';
    $('keyboardHelp').textContent = t('shortcuts');
    try { history.replaceState(null, '', '#q=' + currentId); } catch (_) { /* Local file support. */ }
    renderRounds();
    if (moveFocus) {
      source.focus({ preventScroll: true });
      source.scrollIntoView({ block: 'nearest', behavior: 'instant' });
    }
  }
  function goTo(id) {
    if (!byId.has(id)) return;
    currentId = id; revealed = false; hintVisible = false; render(true);
  }
  function next() { goTo(currentId === items.length ? 1 : currentId + 1); }
  function previous() { if (currentId > 1) goTo(currentId - 1); }
  function reveal() { revealed = !revealed; render(); }
  $('prevBtn').dataset.step = '-1'; $('nextBtn').dataset.step = '1';
  $('revealBtn').dataset.reveal = 'answer';
  $('hintBtn').addEventListener('click', () => { hintVisible = !hintVisible; render(); });
  $('revealBtn').addEventListener('click', reveal);
  $('prevBtn').addEventListener('click', previous);
  $('nextBtn').addEventListener('click', next);
  $('menuBtn').addEventListener('click', () => { renderRounds(); $('roundDialog').showModal(); });
  $('closeRoundsBtn').addEventListener('click', () => $('roundDialog').close());
  $('langBtn').addEventListener('click', () => {
    language = language === 'en' ? 'he' : 'en';
    try { localStorage.setItem(LANG_KEY, language); } catch (_) { /* Keep it for this visit. */ }
    render();
  });
  $('copyBtn').addEventListener('click', async () => {
    const url = location.href.split(/[?#]/)[0];
    try { await navigator.clipboard.writeText(url); notify(t('copied')); }
    catch (_) { $('shareInput').value = url; $('shareDialog').showModal(); $('shareInput').focus(); $('shareInput').select(); }
  });
  $('closeShareBtn').addEventListener('click', () => $('shareDialog').close());
  $('fullBtn').addEventListener('click', async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen();
      else notify(t('unavailableFullscreen'));
    } catch (_) { notify(t('unavailableFullscreen')); }
  });
  window.addEventListener('hashchange', () => {
    const id = Number(new URLSearchParams(location.hash.slice(1)).get('q'));
    if (byId.has(id) && id !== currentId) goTo(id);
  });
  document.addEventListener('keydown', event => {
    if (document.querySelector('dialog[open]') || event.ctrlKey || event.metaKey || event.altKey) return;
    if (document.getElementById('teachers-qr-remote-host')?.shadowRoot?.getElementById('overlay')?.hidden === false) return;
    if (event.target.closest('input,textarea,select,[contenteditable=true]')) return;
    if (event.key === 'ArrowDown' || event.key === 'ArrowRight') { event.preventDefault(); next(); }
    else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') { event.preventDefault(); previous(); }
    else if ((event.key === ' ' || event.key === 'Enter') && !event.target.closest('button,a')) { event.preventDefault(); reveal(); }
  });
  let touch;
  $('sourceSentence').addEventListener('touchstart', event => {
    touch = event.touches.length === 1 ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  $('sourceSentence').addEventListener('touchend', event => {
    if (!touch || !event.changedTouches.length) return;
    const dx = event.changedTouches[0].clientX - touch.x, dy = event.changedTouches[0].clientY - touch.y;
    touch = null;
    if (Math.abs(dy) > 70 && Math.abs(dy) > Math.abs(dx) * 1.3) { if (dy < 0) next(); else previous(); }
  }, { passive: true });
  $('sourceSentence').addEventListener('touchcancel', () => { touch = null; }, { passive: true });
  render();
})();
