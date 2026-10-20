
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

/* Teaching-first essay alternatives: clearly show what changed. */
(() => {
  const PAUSE_MS = 3600;
  const stopped = new WeakSet();
  let currentSlide = null, timer = null, pending = null, oldTarget = null;
  const active = () => document.querySelector('.slide.active:not([hidden])');
  const overlay = document.createElement('div');
  overlay.className = 'essay-change-guide';
  overlay.setAttribute('aria-live','off');
  overlay.innerHTML = '<div class="essay-change-title">✦ Another way to say it</div><div class="essay-change-before"></div><div class="essay-change-arrow">↓</div><div class="essay-change-after"></div><div class="essay-change-help">Tap a highlighted phrase to choose your own wording</div>';
  const style = document.createElement('style');
  style.textContent = `
    .essay-change-guide {position:fixed;left:50%;bottom:calc(92px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:8000;width:min(88vw,570px);padding:13px 18px 15px;border:2px solid #ffe174;border-radius:18px;background:rgba(8,24,38,.97);box-shadow:0 14px 36px #0009;text-align:center;direction:ltr;pointer-events:none;color:#f5f7fb;font-family:system-ui,sans-serif;transition:opacity .3s ease}
    .essay-change-guide[hidden]{display:none!important}
    .essay-change-title{color:#ffe174;font-size:13px;font-weight:800;letter-spacing:.04em;margin-bottom:5px}
    .essay-change-before{color:#b8c4d0;font-size:clamp(15px,3vw,21px);text-decoration:line-through;text-decoration-thickness:1px}
    .essay-change-arrow{color:#ffe174;font-size:21px;line-height:1.1}
    .essay-change-after{display:inline-block;background:#ffe174;color:#13202b;font-weight:850;border-radius:8px;padding:4px 9px;font-size:clamp(18px,4vw,27px)}
    .essay-change-help{font-size:11px;color:#b4c5d7;margin-top:7px}
    .word-switch.essay-live-target{background:#ffe174!important;color:#112236!important;border-radius:5px;outline:3px solid #ffedaa!important;outline-offset:3px;box-shadow:0 0 15px #ffe1748c!important}
    @media(max-height:650px){.essay-change-guide{bottom:67px;padding:8px 12px}.essay-change-help{display:none}}
    @media(prefers-reduced-motion:reduce){.essay-change-guide{transition:none}}
  `;
  document.head.append(style); document.body.append(overlay); overlay.hidden = true;
  const before = overlay.querySelector('.essay-change-before');
  const after = overlay.querySelector('.essay-change-after');
  function clear() {
    clearTimeout(timer); clearTimeout(pending);
    timer = pending = null;
    document.querySelectorAll('.essay-live-target').forEach(el=>el.classList.remove('essay-live-target'));
    overlay.hidden = true;
  }
  function run() {
    const slide = currentSlide;
    if (!slide || active() !== slide || stopped.has(slide) || document.hidden) {clear();return;}
    const choices=[...slide.querySelectorAll('.word-switch[data-options]')].filter(el=>{
      try{return JSON.parse(el.dataset.options).length>1;}catch{return false;}
    });
    if (!choices.length){clear();return;}
    const pool=choices.length>1?choices.filter(el=>el!==oldTarget):choices;
    const el=pool[Math.floor(Math.random()*pool.length)];
    oldTarget=el;
    const options=JSON.parse(el.dataset.options);
    const index=Number(el.dataset.choice||0);
    const next=(index+1+Math.floor(Math.random()*(options.length-1)))%options.length;
    const prior=options[index];
    const future=options[next];
    const punctuation=el.dataset.punctuation||'';
    before.textContent=prior+punctuation;
    after.textContent=future+punctuation;
    overlay.hidden=false;
    el.classList.add('essay-live-target');
    // Give students time to spot the selected words before switching.
    pending=setTimeout(()=>{
      if (currentSlide!==slide||stopped.has(slide)||document.hidden){clear();return;}
      el.dataset.choice=String(next);
      el.textContent=future+punctuation;
      el.setAttribute('aria-label',future+' — לחצו לניסוח אחר');
      const count=slide.querySelector('.count');
      if(count){
        const regions=[...slide.querySelectorAll('.essay.en p,.main-copy.en')];
        count.textContent=regions.reduce((n,p)=>n+(p.textContent.match(/[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*/g)||[]).length,0)+' words';
      }
      window.dispatchEvent(new Event('resize'));
    },650);
    timer=setTimeout(()=>{
      el.classList.remove('essay-live-target');
      overlay.hidden=true;
      run();
    },PAUSE_MS);
  }
  function setSlide(slide){
    clear();currentSlide=slide;oldTarget=null;
    if (!slide||stopped.has(slide)||!slide.querySelector('.essay,.main-copy.en'))return;
    run();
  }
  const sync=()=>{const slide=active();if(slide!==currentSlide)setSlide(slide);};
  const watcher=new MutationObserver(sync);
  document.querySelectorAll('.slide').forEach(el=>watcher.observe(el,{attributes:true,attributeFilter:['class','hidden']}));
  const stop=e=>{
    if(!e.isTrusted)return;
    const node=e.target instanceof Element?e.target.closest('.word-switch[data-options]'):null;
    const slide=active();
    if(!node||!slide||!slide.contains(node))return;
    stopped.add(slide);clear();
  };
  document.addEventListener('pointerdown',stop,true);
  document.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ')stop(e);},true);
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden)clear();
    else if(currentSlide&&!stopped.has(currentSlide))run();
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
  if (!destination || document.querySelector('.final-draft-shortcut, .final-draft-top-link')) return;
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
