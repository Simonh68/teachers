/* Opt-in alternating full-sentence variants. Shared with short-answer decks.
   Exactly one sentence changes at each interval; hand cues never add changes. */
(() => {
  'use strict';
  const decks = [...document.querySelectorAll('.slide:has(.sentence-answer)')];
  if (!decks.length) return;
  const groups = new Map();
  const states = new WeakMap();
  const everyChange = document.documentElement.dataset.sequenceHand === 'every-change';
  const cueLead = everyChange ? 600 : 1200;
  let active = null, paused = false, timer = null, cueTimer = null;
  let manualTimer = null, hideTimer = null, handTarget = null;
  const hand = document.createElement('div');
  hand.className = 'sequence-hand'; hand.setAttribute('aria-hidden', 'true');
  hand.innerHTML = '<svg viewBox="0 0 55 65"><path d="M19 56 9 39c-4-8 2-12 7-7l5 5V9c0-8 10-8 10 0v22-8c0-7 9-7 9 0v11-6c0-6 8-6 8 0v13c0 11-6 19-16 19H25z" fill="#f4cfac" stroke="#5e4335" stroke-width="2" stroke-linejoin="round"/></svg>';
  document.body.append(hand);

  function hideHand() {
    clearTimeout(hideTimer); hideTimer = null; handTarget = null;
    hand.classList.remove('show');
  }
  function cancel(keepHand=false) {
    clearTimeout(timer); clearTimeout(cueTimer); clearTimeout(manualTimer);
    timer = cueTimer = manualTimer = null;
    if (!keepHand) hideHand();
  }
  function stateFor(slide) {
    if (!states.has(slide)) states.set(slide, {next:0, cycles:0});
    return states.get(slide);
  }
  function selections(slide) {
    const group = slide.querySelector('.sentence-answer').dataset.answerGroup;
    if (!groups.has(group)) groups.set(group, [0,0]);
    return groups.get(group);
  }
  function render(slide, pulse=-1) {
    const choices = selections(slide);
    slide.querySelectorAll('.sentence-choice').forEach((el,n) => {
      const options = [...el.querySelectorAll('.sentence-variant')];
      options.forEach((option,i) => {
        option.classList.toggle('is-current', i===choices[n]);
        option.setAttribute('aria-hidden', String(i!==choices[n]));
      });
      el.dataset.choice = String(choices[n]);
      el.setAttribute('aria-label', options[choices[n]].textContent+' — לחצו לניסוח אחר');
      el.closest('.sentence-row').querySelector('.variant-count').textContent = `${choices[n]+1} / ${options.length}`;
      el.classList.remove('changing');
      if (n===pulse) { void el.offsetWidth; el.classList.add('changing',`changed-${n}`); }
    });
  }
  function blocked() {
    return !active || paused || document.hidden || !!active.querySelector('details[open]');
  }
  function updateButtons() {
    document.querySelectorAll('.sequence-toggle').forEach(b => {
      b.textContent = paused ? '▶ המשך ההחלפות' : 'Ⅱ השהיית ההחלפות';
      b.setAttribute('aria-pressed', String(!paused));
    });
  }
  function positionHand(el) {
    if (!active || !active.contains(el)) return false;
    // Measure the visible text, not the grid space reserved for longer variants.
    const range = document.createRange();
    range.selectNodeContents(el.querySelector('.is-current'));
    const parent = active.getBoundingClientRect();
    const top = Math.max(parent.top, document.querySelector('.section-nav')?.getBoundingClientRect().bottom || 0) + 8;
    const bottom = Math.min(parent.bottom, document.querySelector('.nav')?.getBoundingClientRect().top || innerHeight) - 8;
    const rect = [...range.getClientRects()].find(r => r.width > 0 && r.bottom > top && r.top < bottom && r.right > 8 && r.left < innerWidth-8);
    if (!rect) return false;
    const left = Math.max(8,rect.left), right = Math.min(innerWidth-8,rect.right);
    const x = left + Math.min(120,(right-left)*.5);
    const y = (Math.max(top,rect.top)+Math.min(bottom,rect.bottom))*.5;
    // The SVG fingertip is 23px from the left and 3px from the top.
    hand.style.left = (x-23)+'px';
    hand.style.top = (y-3)+'px';
    return true;
  }
  function showHand(el) {
    hideHand();
    if (!positionHand(el)) return;
    handTarget = el;
    hand.classList.remove('show'); void hand.offsetWidth; hand.classList.add('show');
    hideTimer = setTimeout(hideHand, everyChange ? 1200 : 1500);
  }
  function change(slide,n,automatic) {
    const state = stateFor(slide), selected = selections(slide);
    const count = slide.querySelectorAll('.sentence-choice')[n].querySelectorAll('.sentence-variant').length;
    selected[n] = (selected[n]+1)%count;
    state.next = (n+1)%2;
    if (automatic) state.cycles++;
    slide.dataset.lastChangedSentence = String(n+1);
    slide.dataset.automaticCycles = String(state.cycles);
    render(slide,n);
  }
  function schedule(keepHand=false) {
    cancel(keepHand);
    if (blocked()) return;
    const owner = active, state = stateFor(owner);
    const interval = Number(owner.querySelector('.sentence-answer').dataset.interval)||10000;
    const cycle = state.cycles+1;
    if (everyChange || cycle<=2 || cycle%5===0) cueTimer = setTimeout(() => {
      if (active===owner && !blocked()) showHand(owner.querySelectorAll('.sentence-choice')[state.next]);
    }, Math.max(0,interval-cueLead));
    timer = setTimeout(() => {
      if (active!==owner || blocked()) return;
      change(owner,state.next,true);
      schedule(everyChange);
    },interval);
  }
  function refresh() {
    const next = decks.find(s=>s.classList.contains('active')&&!s.hidden)||null;
    if (next===active) return;
    cancel(); active = next;
    if (active) { render(active); schedule(); }
  }
  decks.forEach(slide => {
    slide.querySelectorAll('.sentence-choice').forEach((el,n) => {
      el.addEventListener('click', () => {
        if (slide!==active) return;
        if (!everyChange) { change(slide,n,false); schedule(); return; }
        cancel(); showHand(el);
        manualTimer = setTimeout(() => {
          if (slide!==active || document.hidden) return;
          change(slide,n,false); schedule(true);
        },cueLead);
      });
      el.addEventListener('keydown', e => {
        if (e.key==='Enter'||e.key===' ') { e.preventDefault();e.stopPropagation();el.click(); }
      });
    });
    slide.querySelectorAll('details').forEach(el=>el.addEventListener('toggle',()=>{
      if (slide===active) schedule();
    }));
  });
  document.querySelectorAll('.sequence-toggle').forEach(b=>b.addEventListener('click',()=>{
    paused=!paused;updateButtons();schedule();
  }));
  const observer = new MutationObserver(refresh);
  document.querySelectorAll('.slide').forEach(s=>observer.observe(s,{attributes:true,attributeFilter:['class','hidden']}));
  document.addEventListener('visibilitychange',()=>{cancel();if(!document.hidden)schedule();});
  window.addEventListener('pagehide',()=>cancel());
  const repositionHand = () => {
    if (handTarget && !positionHand(handTarget)) hideHand();
  };
  document.addEventListener('scroll',repositionHand,true);
  window.addEventListener('resize',repositionHand);
  refresh();
})();

