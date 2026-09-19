/* Count actual displayed lines; keep counts outside the four prose paragraphs. */
(() => {
  'use strict';
  const essays = [...document.querySelectorAll('.essay-counted')];
  let pending = false;
  const isWord = text => /[\p{L}\p{N}]/u.test(text);
  for (const essay of essays) {
    for (const paragraph of essay.querySelectorAll(':scope > p')) {
      const text = paragraph.textContent;
      paragraph.replaceChildren();
      for (const token of text.match(/\S+|\s+/g) || []) {
        if (/^\s+$/.test(token)) paragraph.append(document.createTextNode(token));
        else {
          const word = document.createElement('span');
          word.className = 'essay-token';
          word.textContent = token;
          word.dataset.word = String(Number(isWord(token)));
          paragraph.append(word);
        }
      }
    }
  }
  function update() {
    pending = false;
    for (const essay of essays) {
      if (!essay.getClientRects().length || essay.closest('[hidden]')) continue;
      let total = 0;
      for (const paragraph of essay.querySelectorAll(':scope > p')) {
        paragraph.querySelectorAll('.essay-line-count').forEach(label => label.remove());
        const lines = [];
        for (const token of paragraph.querySelectorAll('.essay-token')) {
          const top = token.offsetTop;
          let line = lines.find(row => Math.abs(row.top - top) < 2);
          if (!line) { line = {top, count:0}; lines.push(line); }
          line.count += Number(token.dataset.word);
        }
        for (const line of lines) {
          const label = document.createElement('span');
          label.className = 'essay-line-count';
          label.style.top = line.top + 'px';
          label.textContent = String(line.count);
          label.setAttribute('aria-hidden','true');
          label.title = line.count + ' words in this line';
          paragraph.append(label);
          total += line.count;
        }
      }
      const totalElement = essay.parentElement.querySelector('[data-essay-total]');
      if (totalElement) totalElement.textContent = String(total);
    }
  }
  function schedule() {
    if (!pending) { pending = true; requestAnimationFrame(update); }
  }
  const resize = new ResizeObserver(schedule);
  const changes = new MutationObserver(schedule);
  for (const essay of essays) {
    resize.observe(essay);
    changes.observe(essay.closest('.slide'),{attributes:true,attributeFilter:['class','hidden']});
    changes.observe(essay.closest('.frame'),{attributes:true,attributeFilter:['style']});
  }
  window.addEventListener('resize', schedule);
  document.fonts.ready.then(schedule);
  schedule();
})();
