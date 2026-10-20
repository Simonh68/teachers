
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

/* Paragraph-local essay wording examples: only visible text animates. */
(() => {
  const CYCLE=3900, PREVIEW=950;
  const stopped=new WeakSet(), states=new Map();
  let activeSlide=null;
  const visibleSlide=()=>document.querySelector('.slide.active:not([hidden])');
  const style=document.createElement('style');
  style.textContent=`
    .word-switch.essay-demo-upcoming{outline:3px solid #f6c744!important;outline-offset:3px;border-radius:5px;background:rgba(255,218,93,.28)!important;box-shadow:0 0 0 5px rgba(255,218,93,.12)!important}
    .word-switch.essay-demo-new{outline:3px solid #ffe575!important;outline-offset:3px;border-radius:5px;background:#ffe575!important;color:#142334!important;box-shadow:0 0 14px #ffe57588!important;transition:background 1.6s ease,box-shadow 1.6s ease}
    .essay-demo-note{position:fixed;z-index:7000;max-width:min(82vw,380px);padding:8px 12px;border:1px solid #ffe575;border-radius:12px;background:rgba(10,28,43,.97);color:#fff5cd;font:600 14px/1.4 system-ui,sans-serif;text-align:center;pointer-events:none;box-shadow:0 7px 24px #0008;direction:ltr}
    .essay-demo-note[hidden]{display:none!important}
    .essay-demo-note .old{color:#bccbd5;text-decoration:line-through;font-weight:400}
    .essay-demo-note .new{color:#ffe575;font-weight:800}
    @media(prefers-reduced-motion:reduce){.word-switch.essay-demo-new{transition:none}}
  `;
  document.head.append(style);
  function visible(el){
    if(!el.isConnected||!activeSlide||!activeSlide.contains(el))return false;
    const r=el.getBoundingClientRect(), s=activeSlide.getBoundingClientRect();
    const top=Math.max(r.top,s.top,0),bottom=Math.min(r.bottom,s.bottom,innerHeight);
    const left=Math.max(r.left,s.left,0),right=Math.min(r.right,s.right,innerWidth);
    return bottom-top>Math.min(14,r.height*.5)&&right-left>Math.min(24,r.width*.35);
  }
  function stopState(state){
    clearTimeout(state.timer);clearTimeout(state.next);
    state.el?.classList.remove('essay-demo-upcoming','essay-demo-new');
    state.note.remove();states.delete(state.region);
  }
  function stopAll(){[...states.values()].forEach(stopState);}
  function sequence(state){
    if(visibleSlide()!==activeSlide||!visible(state.region)||stopped.has(state.region)){stopState(state);return;}
    const available=[...state.region.querySelectorAll('.word-switch[data-options]')].filter(el=>{
      try{return visible(el)&&JSON.parse(el.dataset.options).length>1;}catch{return false;}
    });
    if(!available.length){state.timer=setTimeout(()=>sequence(state),1000);return;}
    const pool=available.length>1?available.filter(el=>el!==state.el):available;
    const el=pool[Math.floor(Math.random()*pool.length)], options=JSON.parse(el.dataset.options);
    state.el=el;
    const current=Number(el.dataset.choice||0);
    const next=(current+1+Math.floor(Math.random()*(options.length-1)))%options.length;
    const ending=el.dataset.punctuation||'';
    state.note.replaceChildren();
    const old=document.createElement('span'),fresh=document.createElement('span');
    old.className='old';fresh.className='new';
    old.textContent=options[current]+ending;fresh.textContent=options[next]+ending;
    state.note.append(old,document.createTextNode('  →  '),fresh);
    const r=el.getBoundingClientRect();
    state.note.style.left=Math.max(8,Math.min(innerWidth-260,r.left))+'px';
    state.note.style.top=(r.top>94?Math.max(8,r.top-66):Math.min(innerHeight-74,r.bottom+10))+'px';
    state.note.hidden=false;
    el.classList.add('essay-demo-upcoming');
    state.next=setTimeout(()=>{
      if(!visible(el)||stopped.has(state.region)){stopState(state);return;}
      el.classList.remove('essay-demo-upcoming');el.classList.add('essay-demo-new');
      el.dataset.choice=String(next);el.textContent=options[next]+ending;
      el.setAttribute('aria-label',options[next]+' — לחצו לניסוח אחר');
      const slide=activeSlide;
      const count=slide?.querySelector('.count');
      if(count){
        const regions=[...slide.querySelectorAll('.essay.en p,.main-copy.en')];
        count.textContent=regions.reduce((n,p)=>n+(p.textContent.match(/[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*/g)||[]).length,0)+' words';
      }
      window.dispatchEvent(new Event('resize'));
      state.timer=setTimeout(()=>{
        el.classList.remove('essay-demo-new');state.note.hidden=true;sequence(state);
      },CYCLE-PREVIEW);
    },PREVIEW);
  }
  function refresh(){
    const slide=visibleSlide();
    if(slide!==activeSlide){stopAll();activeSlide=slide;}
    if(!slide||document.hidden)return;
    const paragraphs=[...slide.querySelectorAll('.essay.en > p,.main-copy.en')];
    paragraphs.forEach(region=>{
      if(stopped.has(region)||!region.querySelector('.word-switch[data-options]'))return;
      if(!visible(region)){if(states.has(region))stopState(states.get(region));return;}
      if(states.has(region))return;
      const note=document.createElement('div');note.className='essay-demo-note';note.hidden=true;
      document.body.append(note);
      const state={region,note,el:null,timer:null,next:null};states.set(region,state);
      sequence(state);
    });
  }
  const observer=new MutationObserver(refresh);
  document.querySelectorAll('.slide').forEach(slide=>observer.observe(slide,{attributes:true,attributeFilter:['class','hidden']}));
  document.addEventListener('scroll',refresh,true);
  window.addEventListener('resize',refresh);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stopAll();else refresh();});
  function stopByTouch(e){
    if(!e.isTrusted)return;
    const el=e.target instanceof Element?e.target.closest('.word-switch[data-options]'):null;
    const region=el?.closest('.essay.en > p,.main-copy.en');
    if(!region)return;
    stopped.add(region);if(states.has(region))stopState(states.get(region));
  }
  document.addEventListener('pointerdown',stopByTouch,true);
  document.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ')stopByTouch(e);},true);
  refresh();
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
