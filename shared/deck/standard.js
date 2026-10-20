
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
  document.querySelectorAll('[data-play-clip]').forEach(button => {
    const video = button.parentElement.querySelector('video');
    function label() { const playing = !video.paused && !video.ended; button.textContent = playing ? 'Ⅱ' : '▶'; button.setAttribute('aria-label', playing ? 'השהיית הסרטון' : 'הפעלת הסרטון השקט'); }
    button.addEventListener('click', async () => { if (video.paused) { try { await video.play(); } catch { button.setAttribute('aria-label','לא ניתן להפעיל כרגע — נסו שוב'); } } else video.pause(); label(); });
    video.addEventListener('play',label); video.addEventListener('pause',label); video.addEventListener('ended',label);
  });
  function fromHash() { const match = location.hash.match(/^#slide-(\d+)$/); show(match ? Number(match[1])-1 : 0, false); }
  window.addEventListener('hashchange', fromHash);
  window.addEventListener('resize', fit);
  document.fonts.ready.then(fit);
  fromHash();
})();

/* Classroom essay variation demo: continuous until the learner interacts. */
(() => {
  const STEP_MS = 2100;
  const pausedSlides = new WeakSet();
  let timer = null, delayed = null, slideNow = null, lastElement = null;
  let animations = [];
  const activeSlide = () => document.querySelector('.slide.active:not([hidden])');
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function clearEffects() {
    clearInterval(timer); clearTimeout(delayed);
    timer = delayed = null;
    animations.forEach(a => a.cancel()); animations = [];
    document.querySelectorAll('.word-switch.auto-essay-target').forEach(el => {
      el.classList.remove('auto-essay-target');
      el.style.removeProperty('outline-offset');
    });
  }
  function play(el, keyframes, duration) {
    if (reduced() || typeof el.animate !== 'function') return;
    const animation = el.animate(keyframes, {duration, easing:'ease-in-out'});
    animations.push(animation);
    animation.onfinish = () => { animations = animations.filter(a => a !== animation); };
  }
  function rotate() {
    const slide = slideNow;
    if (!slide || activeSlide() !== slide || pausedSlides.has(slide)) { clearEffects(); return; }
    const eligible = [...slide.querySelectorAll('.word-switch[data-options]')].filter(el => {
      try { return JSON.parse(el.dataset.options).length > 1; } catch { return false; }
    });
    if (!eligible.length) return;
    const pool = eligible.length > 1 ? eligible.filter(el => el !== lastElement) : eligible;
    const el = pool[Math.floor(Math.random() * pool.length)];
    lastElement = el;
    const options = JSON.parse(el.dataset.options);
    const current = Number(el.dataset.choice || 0);
    const shift = 1 + Math.floor(Math.random() * (options.length - 1));
    // Identify the phrase first, then reveal a different valid expression.
    el.classList.add('auto-essay-target');
    play(el, [
      {backgroundColor:'rgba(255,224,83,0)',boxShadow:'0 0 0 0 rgba(255,224,83,0)'},
      {backgroundColor:'rgba(255,224,83,.33)',boxShadow:'0 0 0 3px rgba(255,224,83,.12)'}
    ], 340);
    delayed = setTimeout(() => {
      if (slideNow !== slide || activeSlide() !== slide || pausedSlides.has(slide)) return;
      for(let i=0;i<shift;i++) el.click(); // Reuse existing count/punctuation logic.
      el.classList.remove('auto-essay-target');
      play(el, [
        {offset:0,backgroundColor:'rgba(255,224,83,.68)',boxShadow:'0 0 0 3px rgba(255,224,83,.12)',opacity:.90},
        {offset:.20,backgroundColor:'rgba(255,224,83,.45)',boxShadow:'0 0 0 2px rgba(255,224,83,.07)',opacity:1},
        {offset:1,backgroundColor:'rgba(255,224,83,0)',boxShadow:'0 0 0 0 rgba(255,224,83,0)',opacity:1}
      ], 1500);
    }, 340);
  }
  function activate(slide) {
    clearEffects(); slideNow = slide; lastElement = null;
    if (!slide || pausedSlides.has(slide)) return;
    if (!slide.querySelector('.essay, .main-copy.en')) return;
    if (!slide.querySelector('.word-switch[data-options]')) return;
    timer = setInterval(rotate, STEP_MS);
    rotate();
  }
  const sync = () => { const next = activeSlide(); if (slideNow !== next) activate(next); };
  const observer = new MutationObserver(sync);
  document.querySelectorAll('.slide').forEach(slide =>
    observer.observe(slide, {attributes:true,attributeFilter:['class','hidden']})
  );
  function stopOnInteraction(event) {
    if (!event.isTrusted) return;
    const target = event.target instanceof Element ? event.target.closest('.word-switch[data-options]') : null;
    const slide = activeSlide();
    if (!target || !slide || !slide.contains(target)) return;
    pausedSlides.add(slide);
    clearEffects(); // Current alternative stays in place; manual clicks still work.
  }
  document.addEventListener('pointerdown', stopOnInteraction, true);
  document.addEventListener('keydown', event => {
    if (event.key === 'Enter' || event.key === ' ') stopOnInteraction(event);
  }, true);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) clearEffects();
    else if (slideNow && !pausedSlides.has(slideNow)) activate(slideNow);
  });
  sync();
})();

/* Persistent Final Draft shortcut for essay-writing decks. */
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const destination = [...slides].reverse().find(slide =>
    slide.classList.contains('essay') &&
    /החיבור המלא|final draft|full essay/i.test(slide.querySelector('.eyebrow')?.textContent || '')
  );
  if (!destination || document.querySelector('.final-draft-shortcut')) return;
  const link = document.createElement('a');
  link.className = 'final-draft-shortcut';
  link.href = '#' + destination.id;
  link.textContent = 'Final Draft';
  link.title = 'מעבר לחיבור הסופי';
  link.setAttribute('aria-label', 'Final Draft — מעבר לחיבור הסופי');
  document.body.append(link);
  const style = document.createElement('style');
  style.textContent = `
    .final-draft-shortcut {
      position:fixed; top:max(12px,env(safe-area-inset-top));
      right:max(16px,env(safe-area-inset-right)); z-index:200;
      display:inline-flex; align-items:center; justify-content:center;
      min-height:36px; padding:7px 15px;
      border:1px solid rgba(255,230,142,.5); border-radius:999px;
      background:rgba(28,34,46,.94); color:#ffebaa;
      font:700 13px/1.2 system-ui,sans-serif; letter-spacing:.025em;
      text-decoration:none; box-shadow:0 3px 14px rgba(0,0,0,.18);
      transition:background .2s ease,transform .2s ease;
    }
    .final-draft-shortcut:hover,.final-draft-shortcut:focus-visible {
      background:#43402b; color:#fff4cc; transform:translateY(-1px);
      outline-offset:3px;
    }
    @media(max-width:600px) {
      .final-draft-shortcut {top:max(8px,env(safe-area-inset-top));right:10px;padding:7px 11px;font-size:12px}
    }
  `;
  document.head.append(style);
})();
