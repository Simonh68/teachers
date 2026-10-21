/* Opt-in prerecorded vocabulary audio. Navigation remains in standard.js. */
(() => {
  'use strict';
  const player = new Audio();
  player.preload = 'none';
  let activeButton = null, generation = 0;
  const status = document.querySelector('[data-audio-status]');
  const speed = document.querySelector('[data-audio-speed]');
  const tell = text => { if (status) status.textContent = text; };
  function stop() {
    generation++; player.pause(); player.currentTime = 0;
    if (activeButton) { activeButton.setAttribute('aria-pressed','false'); activeButton.classList.remove('playing'); }
    activeButton = null; tell('');
  }
  document.addEventListener('click', async event => {
    const button = event.target.closest('[data-vocab-audio]');
    if (!button) return;
    if (button === activeButton && !player.paused) { stop(); return; }
    stop(); const token = generation; activeButton = button;
    player.src = button.dataset.vocabAudio;
    player.playbackRate = Number(speed?.value || 1); player.preservesPitch = true;
    button.setAttribute('aria-pressed','true'); button.classList.add('playing');
    tell('טוען הקלטה…');
    try { await player.play(); if (token === generation) tell(button.dataset.audioKind === 'word' ? 'משמיע את הערך' : 'משמיע את משפט הדוגמה'); }
    catch { if (token === generation) { stop(); tell('ההקלטה לא נטענה. לחצו שוב כדי לנסות.'); } }
  });
  player.addEventListener('ended', stop);
  player.addEventListener('error', () => { if (activeButton) { stop(); tell('ההקלטה לא נטענה. בדקו את החיבור ונסו שוב.'); } });
  speed?.addEventListener('change', () => { player.playbackRate = Number(speed.value); });
  let slide = document.querySelector('.slide.active');
  new MutationObserver(() => { const next = document.querySelector('.slide.active'); if(next !== slide) { stop(); slide=next; } }).observe(document.querySelector('.stage'), {subtree:true,attributes:true,attributeFilter:['hidden','class']});
  document.addEventListener('visibilitychange', () => { if(document.hidden) stop(); });
  window.addEventListener('pagehide',stop);
  const dialog = document.querySelector('[data-vocab-index]');
  document.querySelector('[data-open-index]')?.addEventListener('click',()=> { stop(); dialog.showModal(); });
  document.querySelector('[data-close-index]')?.addEventListener('click',()=>dialog.close());
  dialog?.addEventListener('click',event=> { if(event.target.closest('a[href^="#slide-"]')) dialog.close(); });
  document.querySelectorAll('[data-copy-url]').forEach(button=>button.addEventListener('click',async()=> {
    try { await navigator.clipboard.writeText(button.dataset.copyUrl); tell('הקישור הועתק'); }
    catch { const input=document.createElement('input');input.value=button.dataset.copyUrl;input.readOnly=true;input.setAttribute('aria-label','קישור להעתקה ידנית');button.after(input);input.select();tell('בחרו והעתיקו את הקישור המוצג'); }
  }));
})();
