
(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  const counter = document.querySelector('#counter');
  const progress = document.querySelector('.progress-fill');
  const navButtons = [...document.querySelectorAll('[data-step]')];
  const sectionButtons = [...document.querySelectorAll('[data-jump]')];
  let current = -1, wheelTime = 0, wheelSum = 0, touchStart = null;
  function fit() {
    const slide = slides[current];
    if (!slide) return;
    const frame = slide.querySelector('.frame');
    const pair = slide.dataset.pair;
    const candidates = pair ? slides.filter(s => s.dataset.pair === pair) : [slide];
    const available = slide.clientHeight - parseFloat(getComputedStyle(slide).paddingTop) - parseFloat(getComputedStyle(slide).paddingBottom);
    let scale = 1;
    // Reserve the answer's complete height in both members of the pair.
    if (pair) {
      let slotHeight = 0;
      for (const candidate of candidates) {
        const active = candidate === slide;
        if (!active) { candidate.hidden = false; candidate.style.display = 'flex'; candidate.style.visibility = 'hidden'; }
        candidate.querySelector('.frame').style.zoom = '1';
        const slot = candidate.querySelector('.translation-slot, .answer-slot');
        slot.style.height = 'auto';
        slotHeight = Math.max(slotHeight, slot.getBoundingClientRect().height);
        if (!active) { candidate.hidden = true; candidate.style.removeProperty('display'); candidate.style.removeProperty('visibility'); }
      }
      candidates.forEach(candidate => { candidate.querySelector('.translation-slot, .answer-slot').style.height = slotHeight + 'px'; });
    }
    // Measure both members of a pair so the question never jumps on reveal.
    for (const candidate of candidates) {
      const f = candidate.querySelector('.frame');
      const active = candidate === slide;
      if (!active) { candidate.hidden = false; candidate.style.display = 'flex'; candidate.style.visibility = 'hidden'; }
      f.style.zoom = '1';
      scale = Math.min(scale, available / Math.max(f.scrollHeight, 1), f.clientWidth / Math.max(f.scrollWidth, 1));
      if (!active) { candidate.hidden = true; candidate.style.removeProperty('display'); candidate.style.removeProperty('visibility'); }
    }
    const fittingScale = Math.min(1, Math.max(.68, scale));
    for (const candidate of candidates) candidate.querySelector('.frame').style.zoom = String(fittingScale);
    // Ordinary vertical scrolling remains available for browser text enlargement.
    slide.style.alignItems = frame.getBoundingClientRect().height > available + 1 ? 'flex-start' : 'center';
  }
  function show(index, updateHash = true) {
    index = Math.max(0, Math.min(slides.length - 1, index));
    if (current >= 0) { slides[current].querySelectorAll('video').forEach(v => { v.pause(); v.currentTime = 0; }); slides[current].classList.remove('active'); slides[current].hidden = true; }
    current = index;
    const slide = slides[current];
    slide.hidden = false; slide.classList.add('active'); slide.scrollTop = 0;
    counter.textContent = `${current + 1} / ${slides.length}`;
    progress.style.width = `${100 * (current + 1) / slides.length}%`;
    navButtons.forEach(b => { b.disabled = Number(b.dataset.step) < 0 ? current === 0 : current === slides.length - 1; });
    sectionButtons.forEach(b => b.setAttribute('aria-current', String(b.dataset.jump === slide.dataset.section)));
    if (updateHash) history.replaceState(null, '', '#slide-' + (current + 1));
    fit();
  }
  navButtons.forEach(b => b.addEventListener('click', () => show(current + Number(b.dataset.step))));
  sectionButtons.forEach(b => b.addEventListener('click', () => show(slides.findIndex(s => s.dataset.section === b.dataset.jump && s.classList.contains('transition')))));
  document.addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey || e.target.closest('video,input,textarea,select,[contenteditable="true"]')) return;
    const forward = ['ArrowRight','ArrowDown','PageDown'];
    const back = ['ArrowLeft','ArrowUp','PageUp'];
    if (forward.includes(e.key) || back.includes(e.key)) { e.preventDefault(); show(current + (forward.includes(e.key) ? 1 : -1)); }
    else if (e.key === 'Home') { e.preventDefault(); show(0); }
    else if (e.key === 'End') { e.preventDefault(); show(slides.length - 1); }
    else if (e.key === ' ' && !e.target.closest('a,button')) { e.preventDefault(); show(current + (e.shiftKey ? -1 : 1)); }
  });
  const stage = document.querySelector('.stage');
  stage.addEventListener('wheel', e => {
    if (e.ctrlKey) return;
    const slide = slides[current];
    if (slide.scrollHeight > slide.clientHeight + 2) return;
    e.preventDefault();
    const now = Date.now();
    if (now - wheelTime < 400) return;
    const delta = Math.abs(e.deltaY) >= Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
    if (Math.sign(wheelSum) !== Math.sign(delta)) wheelSum = 0;
    wheelSum += delta * (e.deltaMode === 1 ? 16 : 1);
    if (Math.abs(wheelSum) >= 35) { show(current + (wheelSum > 0 ? 1 : -1)); wheelTime = now; wheelSum = 0; }
  }, {passive:false});
  stage.addEventListener('touchstart', e => { if (e.touches.length === 1) touchStart = {x:e.touches[0].clientX,y:e.touches[0].clientY}; else touchStart=null; }, {passive:true});
  stage.addEventListener('touchend', e => {
    if (!touchStart || !e.changedTouches.length) return;
    const dx = e.changedTouches[0].clientX - touchStart.x;
    const dy = e.changedTouches[0].clientY - touchStart.y;
    touchStart = null;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < 55) return;
    if (Math.abs(dx) > Math.abs(dy)) show(current + (dx < 0 ? 1 : -1));
    else if (slides[current].scrollHeight <= slides[current].clientHeight + 2) show(current + (dy < 0 ? 1 : -1));
  }, {passive:true});
  stage.addEventListener('touchcancel', () => {touchStart=null;}, {passive:true});
  function fromHash() { const match = location.hash.match(/^#slide-(\d+)$/); show(match ? Number(match[1])-1 : 0, false); }
  window.addEventListener('hashchange', fromHash);
  window.addEventListener('resize', fit);
  document.fonts.ready.then(fit);
  fromHash();
})();
