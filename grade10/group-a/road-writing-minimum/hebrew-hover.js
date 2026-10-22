/* Hebrew translations follow the currently displayed English wording.
   Hover, keyboard focus and touch share one tooltip; clicks still change wording. */
(() => {
  'use strict';
  const selector = '.hebrew-hover-target';
  const tip = document.createElement('div');
  tip.id = 'hebrew-hover-tooltip';
  tip.className = 'hebrew-hover-tooltip';
  tip.lang = 'he'; tip.dir = 'rtl'; tip.hidden = true;
  tip.setAttribute('role','tooltip');
  document.body.append(tip);
  let target = null, hovered = null, focused = null, touchTimer = null;
  const targetObserver = new MutationObserver(refresh);
  const findTarget = node => node instanceof Element ? node.closest(selector) : null;

  function sourceFor(el) {
    return el?.matches('.sentence-choice') ? el.querySelector('.sentence-variant.is-current') : el;
  }
  function unlink() {
    if (!target) return;
    const ids = (target.getAttribute('aria-describedby') || '').split(/\s+/).filter(id => id && id !== tip.id);
    if (ids.length) target.setAttribute('aria-describedby',ids.join(' '));
    else target.removeAttribute('aria-describedby');
  }
  function hide() {
    clearTimeout(touchTimer); touchTimer = null;
    targetObserver.disconnect(); unlink(); target = null; tip.hidden = true;
  }
  function refresh() {
    if (!target) return;
    const slide = target.closest('.slide'), source = sourceFor(target);
    if (!slide || slide.hidden || !slide.classList.contains('active') || !source?.dataset.he) { hide(); return; }
    const range = document.createRange(); range.selectNodeContents(source);
    const bounds = slide.getBoundingClientRect();
    const topLimit = Math.max(bounds.top,document.querySelector('.section-nav')?.getBoundingClientRect().bottom || 0) + 8;
    const bottomLimit = Math.min(bounds.bottom,document.querySelector('.nav')?.getBoundingClientRect().top || innerHeight) - 8;
    const lines = [...range.getClientRects()].filter(r => r.width > 0 && r.bottom > topLimit && r.top < bottomLimit);
    if (!lines.length) { hide(); return; }
    tip.textContent = source.dataset.he;
    tip.hidden = false;
    const first = lines[0], last = lines[lines.length-1];
    const box = tip.getBoundingClientRect();
    const center = Math.max(12,first.left) + Math.min(first.width,innerWidth-24)/2;
    const x = Math.max(12,Math.min(innerWidth-box.width-12,center-box.width/2));
    let y = first.top-box.height-12;
    if (y < topLimit) y = last.bottom+12;
    y = Math.max(8,Math.min(innerHeight-box.height-8,y));
    tip.style.left = x+'px'; tip.style.top = y+'px';
  }
  function show(el) {
    if (!el || !sourceFor(el)?.dataset.he) { hide(); return; }
    if (target !== el) {
      hide(); target = el;
      const ids = new Set((el.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean));
      ids.add(tip.id); el.setAttribute('aria-describedby',[...ids].join(' '));
      targetObserver.observe(el,{attributes:true,subtree:true,attributeFilter:['data-choice','class','data-he']});
    }
    refresh();
  }
  document.addEventListener('pointerover',event => {
    if (event.pointerType === 'touch') return;
    const el = findTarget(event.target);
    if (el && !el.contains(event.relatedTarget)) { hovered = el; show(el); }
  });
  document.addEventListener('pointerout',event => {
    if (event.pointerType === 'touch') return;
    const el = findTarget(event.target);
    if (el && !el.contains(event.relatedTarget)) {
      hovered = null;
      if (focused) show(focused); else hide();
    }
  });
  document.addEventListener('focusin',event => {
    const el = findTarget(event.target);
    if (el?.matches(':focus-visible')) { focused = el; show(el); }
  });
  document.addEventListener('focusout',event => {
    if (findTarget(event.target) === focused) {
      focused = null;
      if (hovered) show(hovered); else hide();
    }
  });
  document.addEventListener('pointerdown',event => {
    const el = findTarget(event.target);
    if (!el) { hovered = focused = null; hide(); return; }
    if (event.pointerType === 'touch') {
      show(el); clearTimeout(touchTimer); touchTimer = setTimeout(hide,5000);
    }
  });
  document.addEventListener('keydown',event => {
    if (event.key === 'Escape') { hovered = focused = null; hide(); }
  });
  const slideObserver = new MutationObserver(() => {
    if (target?.closest('.slide')?.hidden) { hovered = focused = null; hide(); }
  });
  document.querySelectorAll('.slide').forEach(slide => slideObserver.observe(slide,{attributes:true,attributeFilter:['hidden']}));
  document.addEventListener('scroll',() => { hovered = focused = null; hide(); },true);
  window.addEventListener('resize',refresh);
  document.fonts?.ready.then(refresh);
  document.addEventListener('visibilitychange',() => { if(document.hidden) hide(); });
  window.addEventListener('pagehide',hide);
})();
