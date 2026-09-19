(() => {
  const english=document.documentElement.lang==='en';
  const L=(he,en)=>english?en:he;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.animation').forEach(slide=>{
    const sprite=slide.querySelector('.sprite'),toggle=slide.querySelector('[data-anim-toggle]'),replay=slide.querySelector('[data-anim-replay]');
    let ended=false;
    function label(){const paused=slide.classList.contains('is-paused')||(reduced&&!slide.classList.contains('manual-play'));toggle.textContent=ended?'↻':paused?'▶':'Ⅱ';toggle.setAttribute('aria-label',ended?L('הפעלה מחדש','Replay'):paused?L('הפעלת ההנפשה','Play animation'):L('השהיית ההנפשה','Pause animation'));}
    function restart(){ended=false;slide.classList.add('manual-play');slide.classList.remove('is-paused');sprite.style.animationName='none';requestAnimationFrame(()=>requestAnimationFrame(()=>{sprite.style.removeProperty('animation-name');label();}));}
    toggle.addEventListener('click',()=>{if(ended){restart();return;}if(reduced&&!slide.classList.contains('manual-play'))slide.classList.add('manual-play');else slide.classList.toggle('is-paused');label();});
    replay.addEventListener('click',restart);sprite.addEventListener('animationend',()=>{ended=true;label();});
    new MutationObserver(()=>{if(!slide.classList.contains('active')){ended=false;slide.classList.remove('is-paused','manual-play');}label();}).observe(slide,{attributes:true,attributeFilter:['hidden']});label();
  });
  document.querySelectorAll('.clock').forEach(clock=>{
    const slide=clock.closest('.slide'),output=clock.querySelector('output'),toggle=clock.querySelector('[data-timer-toggle]');
    let remaining=Number(clock.dataset.seconds)*1000,running=false,started=0,ticker=null;
    function display(){const n=Math.max(0,Math.ceil(remaining/1000));output.textContent=n===0?L('הזמן הסתיים','Time is up'):`${String(Math.floor(n/60)).padStart(2,'0')}:${String(n%60).padStart(2,'0')}`;clock.classList.toggle('done',n===0);toggle.textContent=running?L('השהיה','Pause'):remaining<=0?L('התחלה מחדש','Restart'):L('התחלה / המשך','Start / resume');}
    function tick(){const now=performance.now();remaining=Math.max(0,remaining-(now-started));started=now;if(!remaining){running=false;clearInterval(ticker);ticker=null;}display();}
    function pause(){if(running){tick();running=false;clearInterval(ticker);ticker=null;}display();}
    toggle.addEventListener('click',()=>{if(running){pause();return;}if(remaining<=0)remaining=Number(clock.dataset.seconds)*1000;running=true;started=performance.now();ticker=setInterval(tick,100);display();});
    clock.querySelector('[data-timer-reset]').addEventListener('click',()=>{pause();remaining=Number(clock.dataset.seconds)*1000;display();});
    clock.querySelector('[data-timer-add]').addEventListener('click',()=>{if(running)tick();remaining+=30000;display();});
    new MutationObserver(()=>{if(slide.hidden)pause();}).observe(slide,{attributes:true,attributeFilter:['hidden']});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});display();
  });
  const rail=document.querySelector('.essay-progress');
  const language=document.querySelector('.language-switch');
  function syncProgress(){
    const slide=document.querySelector('.slide.active');
    if(!slide||!rail)return;
    const done=Number(slide.dataset.completed),writing=Number(slide.dataset.writingStep);
    rail.querySelector('[data-sentence-count]').textContent=done;
    rail.querySelector('[data-word-count]').textContent=slide.dataset.words;
    rail.querySelector('progress').value=done;
    rail.querySelectorAll('[data-sentence]').forEach(item=>{
      const n=Number(item.dataset.sentence);
      item.classList.toggle('done',n<=done);
      item.classList.toggle('current',n===writing);
      if(n===writing)item.setAttribute('aria-current','step');else item.removeAttribute('aria-current');
      item.setAttribute('aria-label',`${n}: ${item.querySelector('.sentence-role').textContent}, ${n<=done?'complete':n===writing?'writing now':'planned'}`);
    });
    language.hash='slide-'+slide.dataset.slide;
  }
  new MutationObserver(syncProgress).observe(document.querySelector('.stage'),{subtree:true,attributes:true,attributeFilter:['hidden']});
  syncProgress();
})();
