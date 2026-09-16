(() => {
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.animation').forEach(slide=>{
    const sprite=slide.querySelector('.sprite');
    const toggle=slide.querySelector('[data-anim-toggle]');
    const replay=slide.querySelector('[data-anim-replay]');
    let ended=false;
    function label(){
      const paused=slide.classList.contains('is-paused') || (reduced && !slide.classList.contains('manual-play'));
      toggle.textContent=ended?'↻':paused?'▶':'Ⅱ';
      toggle.setAttribute('aria-label',ended?'הפעלה מחדש':paused?'הפעלת ההנפשה':'השהיית ההנפשה');
    }
    function restart(){
      ended=false;slide.classList.add('manual-play');slide.classList.remove('is-paused');
      sprite.style.animationName='none';
      requestAnimationFrame(()=>requestAnimationFrame(()=>{sprite.style.removeProperty('animation-name');label();}));
    }
    toggle.addEventListener('click',()=>{
      if(ended){restart();return;}
      if(reduced && !slide.classList.contains('manual-play')) slide.classList.add('manual-play');
      else slide.classList.toggle('is-paused');
      label();
    });
    replay.addEventListener('click',restart);
    sprite.addEventListener('animationend',()=>{ended=true;label();});
    new MutationObserver(()=>{
      if(!slide.classList.contains('active')){ended=false;slide.classList.remove('is-paused','manual-play');}
      label();
    }).observe(slide,{attributes:true,attributeFilter:['hidden']});
    label();
  });
})();
