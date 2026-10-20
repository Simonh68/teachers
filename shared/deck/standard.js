
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

/* Gentle independent variation, without changing fixed linking phrases. */
(() => {
  const fixed=/^\s*(on the one hand|on the other hand)[,.:;!?\s]*$/i;
  const states=new Map(),stopped=new WeakSet();
  let slideNow=null;
  const current=()=>document.querySelector('.slide.active:not([hidden])');
  const style=document.createElement('style');
  style.textContent=`
    .word-switch.essay-soft-focus{transition:color .35s ease,text-shadow .35s ease}
    @media(prefers-reduced-motion:reduce){.word-switch.essay-soft-focus{transition:none}}
  `;
  document.head.append(style);
  function visible(el){
    const s=current();if(!s||!s.contains(el))return false;
    const r=el.getBoundingClientRect(),v=s.getBoundingClientRect();
    return Math.min(r.bottom,v.bottom,innerHeight)-Math.max(r.top,v.top,0)>Math.min(15,r.height*.5)
      && Math.min(r.right,v.right,innerWidth)-Math.max(r.left,v.left,0)>Math.min(20,r.width*.35);
  }
  function optionsFor(el){
    try {
      const all=JSON.parse(el.dataset.options);
      if(!Array.isArray(all)||all.length<2||all.some(x=>fixed.test(x)))return null;
      return all;
    }catch{return null;}
  }
  function stop(state){
    clearTimeout(state.timer);
    state.animation?.cancel();
    state.el?.classList.remove('essay-soft-focus');
    state.el?.style.removeProperty('color');
    state.el?.style.removeProperty('text-shadow');
    states.delete(state.region);
  }
  function tick(state){
    const region=state.region;
    if(document.hidden||!visible(region)||stopped.has(region)){stop(state);return;}
    const els=[...region.querySelectorAll('.word-switch[data-options]')].filter(el=>visible(el)&&optionsFor(el));
    if(!els.length){state.timer=setTimeout(()=>tick(state),900);return;}
    const pool=els.length>1?els.filter(e=>e!==state.el):els;
    const el=pool[Math.floor(Math.random()*pool.length)];
    const opts=optionsFor(el);
    const i=Number(el.dataset.choice||0);
    const next=(i+1+Math.floor(Math.random()*(opts.length-1)))%opts.length;
    state.el=el;
    el.classList.add('essay-soft-focus');
    // Repeated low-amplitude luminous pulses attract attention before the change.
    if(el.animate){
      state.animation=el.animate([
        {color:'inherit',textShadow:'0 0 0 transparent',opacity:1,offset:0},
        {color:'#ffe5a0',textShadow:'0 0 7px rgba(255,223,120,.35)',opacity:.85,offset:.17},
        {color:'inherit',textShadow:'0 0 0 transparent',opacity:1,offset:.34},
        {color:'#ffe5a0',textShadow:'0 0 7px rgba(255,223,120,.35)',opacity:.85,offset:.51},
        {color:'inherit',textShadow:'0 0 0 transparent',opacity:1,offset:.68},
        {color:'#ffe5a0',textShadow:'0 0 7px rgba(255,223,120,.35)',opacity:.85,offset:.85},
        {color:'inherit',textShadow:'0 0 0 transparent',opacity:1,offset:1}
      ],{duration:1650,easing:'ease-in-out'});
    }
    state.timer=setTimeout(()=>{
      if(!visible(el)||stopped.has(region)){stop(state);return;}
      el.dataset.choice=String(next);
      el.textContent=opts[next]+(el.dataset.punctuation||'');
      el.setAttribute('aria-label',opts[next]+' — לחצו לניסוח אחר');
      state.animation?.cancel();
      if(el.animate)state.animation=el.animate([
        {opacity:.72,color:'#ffe9ae',textShadow:'0 0 9px rgba(255,223,120,.45)'},
        {opacity:1,color:'inherit',textShadow:'0 0 0 transparent'}
      ],{duration:1250,easing:'ease-out'});
      const slide=current(),count=slide?.querySelector('.count');
      if(count){
        const ps=[...slide.querySelectorAll('.essay.en p,.main-copy.en')];
        count.textContent=ps.reduce((n,p)=>n+(p.textContent.match(/[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*/g)||[]).length,0)+' words';
      }
      window.dispatchEvent(new Event('resize'));
      state.timer=setTimeout(()=>{el.classList.remove('essay-soft-focus');tick(state);},2450);
    },1650);
  }
  function refresh(){
    const s=current();
    if(s!==slideNow){[...states.values()].forEach(stop);slideNow=s;}
    if(!s||document.hidden)return;
    [...s.querySelectorAll('.essay.en > p,.main-copy.en')].forEach(region=>{
      if(!visible(region)){if(states.has(region))stop(states.get(region));return;}
      if(stopped.has(region)||states.has(region))return;
      if(![...region.querySelectorAll('.word-switch[data-options]')].some(optionsFor))return;
      const state={region,timer:null,animation:null,el:null};
      states.set(region,state);tick(state);
    });
  }
  const observer=new MutationObserver(refresh);
  document.querySelectorAll('.slide').forEach(s=>observer.observe(s,{attributes:true,attributeFilter:['class','hidden']}));
  document.addEventListener('scroll',refresh,true);
  window.addEventListener('resize',refresh);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)[...states.values()].forEach(stop);else refresh();});
  const halt=e=>{
    if(!e.isTrusted)return;
    const el=e.target instanceof Element?e.target.closest('.word-switch[data-options]'):null;
    const region=el?.closest('.essay.en > p,.main-copy.en');
    if(!region)return;
    stopped.add(region);
    if(states.has(region))stop(states.get(region));
  };
  document.addEventListener('pointerdown',halt,true);
  document.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ')halt(e);},true);
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
