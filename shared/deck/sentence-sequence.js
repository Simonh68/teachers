/* Opt-in alternating full-sentence variants. Shared with short-answer decks.
   Exactly one sentence changes at each interval; hand cues never add changes. */
(() => {
  'use strict';
  const decks = [...document.querySelectorAll('.slide:has(.sentence-answer)')];
  if (!decks.length) return;
  const groups = new Map();
  const states = new WeakMap();
  let active = null, paused = false, timer = null, cueTimer = null;
  const hand = document.createElement('div');
  hand.className = 'sequence-hand'; hand.setAttribute('aria-hidden', 'true');
  hand.innerHTML = '<svg viewBox="0 0 55 65"><path d="M19 56 9 39c-4-8 2-12 7-7l5 5V9c0-8 10-8 10 0v22-8c0-7 9-7 9 0v11-6c0-6 8-6 8 0v13c0 11-6 19-16 19H25z" fill="#f4cfac" stroke="#5e4335" stroke-width="2" stroke-linejoin="round"/></svg>';
  document.body.append(hand);

  function cancel() {
    clearTimeout(timer); clearTimeout(cueTimer); timer = cueTimer = null;
    hand.classList.remove('show');
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
  function showHand(el) {
    const rect = el.querySelector('.is-current').getBoundingClientRect();
    const parent = active.getBoundingClientRect();
    if (rect.top < parent.top || rect.bottom > innerHeight-85) return;
    hand.style.left = Math.max(8,Math.min(innerWidth-55,rect.left+rect.width*.45))+'px';
    hand.style.top = Math.max(70,Math.min(innerHeight-85,rect.top+rect.height*.5))+'px';
    hand.classList.remove('show'); void hand.offsetWidth; hand.classList.add('show');
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
  function schedule() {
    cancel();
    if (blocked()) return;
    const owner = active, state = stateFor(owner);
    const interval = Number(owner.querySelector('.sentence-answer').dataset.interval)||10000;
    const cycle = state.cycles+1;
    if (cycle<=2 || cycle%5===0) cueTimer = setTimeout(() => {
      if (active===owner && !blocked()) showHand(owner.querySelectorAll('.sentence-choice')[state.next]);
    }, Math.max(0,interval-1200));
    timer = setTimeout(() => {
      if (active!==owner || blocked()) return;
      change(owner,state.next,true);
      schedule();
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
        change(slide,n,false); schedule();
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
  window.addEventListener('pagehide',cancel);
  refresh();
})();
