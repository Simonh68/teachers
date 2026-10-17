(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  const stage = document.querySelector('#stage');
  const key = 'grade7-matching-reading-deck-v1';
  let pos = 0, activeUtterance = null, speechRun = 0, touch = null, wheelAt = 0;
  const read = (name, fallback) => { try { return localStorage.getItem(name) ?? fallback; } catch { return fallback; } };
  const save = (name, value) => { try { localStorage.setItem(name, String(value)); } catch {} };
  const shuffle = list => { for (let i=list.length-1;i>0;i--) { const j=Math.floor(Math.random()*(i+1)); [list[i],list[j]]=[list[j],list[i]]; } return list; };
  const groups = [...document.querySelectorAll('[data-shuffle]')];
  let positions;
  // Independent balanced randomization. The correct answer has no fixed side.
  for (let tries=0;tries<100;tries++) {
    positions=shuffle(groups.map((_,i)=>i%2));
    if (!positions.some((x,i)=>i>=3&&positions.slice(i-3,i+1).every(v=>v===x))) break;
  }
  groups.forEach((group,i)=> {
    const buttons=[...group.children];
    const good=buttons.find(b=>b.dataset.correct==='true');
    const bad=buttons.find(b=>b.dataset.correct==='false');
    group.replaceChildren(...(positions[i]===0?[good,bad]:[bad,good]));
  });
  document.querySelectorAll('.word-bank').forEach(bank=> {
    let tiles=shuffle([...bank.children]);
    if (tiles.every((t,i)=>Number(t.dataset.token)===i)) tiles.push(tiles.shift());
    bank.replaceChildren(...tiles);
  });
  document.querySelectorAll('[data-read]').forEach(p=> {
    const text=p.dataset.text;
    p.replaceChildren();
    let i=0;
    text.split(/(\s+)/).forEach(part=> {
      if (/^\s+$/.test(part)) p.append(document.createTextNode(part));
      else if(part) {
        const word=document.createElement('span');word.className='word';word.dataset.start=String(i);word.dataset.end=String(i+part.length);word.textContent=part;p.append(word);
      }
      i+=part.length;
    });
  });
  const speed=document.querySelector('#speed');
  const savedSpeed=read('teachers-read-alone-speed-v1','0.8');
  if ([...speed.options].some(o=>o.value===savedSpeed)) speed.value=savedSpeed;
  speed.addEventListener('change',()=>{save('teachers-read-alone-speed-v1',speed.value);stop();});
  function stop() {
    speechRun++;
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    activeUtterance=null;
    document.querySelectorAll('.current,.speaking').forEach(x=>x.classList.remove('current','speaking'));
    document.querySelectorAll('.speak').forEach(b=>b.setAttribute('aria-pressed','false'));
  }
  function speak(button) {
    const p=button.parentElement.querySelector('[data-read]');
    stop();
    const status=document.querySelector('#audio-status');
    if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) {
      status.classList.remove('sr-only');status.textContent='ההקראה אינה זמינה בדפדפן הזה. אפשר לפתוח בכרום או באדג׳.';return;
    }
    const run=speechRun;
    const utterance=new SpeechSynthesisUtterance(p.dataset.text);
    activeUtterance=utterance;
    utterance.lang='en-US';utterance.rate=Number(speed.value);
    const voices=speechSynthesis.getVoices();
    const voice=voices.find(v=>v.lang==='en-US'&&/Google|Microsoft|Samantha/.test(v.name))||voices.find(v=>v.lang==='en-US')||voices.find(v=>v.lang.startsWith('en'));
    if(voice)utterance.voice=voice;
    utterance.onstart=()=>{if(run!==speechRun)return;p.classList.add('speaking');button.setAttribute('aria-pressed','true');status.classList.add('sr-only');status.textContent='הקראה באנגלית';};
    utterance.onboundary=event=> {
      if(run!==speechRun)return;
      p.querySelectorAll('.word').forEach(w=>w.classList.toggle('current',event.charIndex>=Number(w.dataset.start)&&event.charIndex<Number(w.dataset.end)));
    };
    const finish=()=>{if(run!==speechRun)return;p.classList.remove('speaking');p.querySelectorAll('.current').forEach(w=>w.classList.remove('current'));button.setAttribute('aria-pressed','false');activeUtterance=null;};
    utterance.onend=()=>{finish();status.textContent='';};
    utterance.onerror=event=>{if(run!==speechRun)return;finish();if(!['canceled','interrupted'].includes(event.error)){status.classList.remove('sr-only');status.textContent='ההקראה לא הופעלה. בדקו את עוצמת השמע ונסו שוב.';}};
    speechSynthesis.speak(utterance);
  }
  function evidence(slide) {
    slide.querySelectorAll('[data-evidence]').forEach(p=> {
      const phrase=p.dataset.evidence;if(!phrase)return;
      const start=p.dataset.text.toLowerCase().indexOf(phrase.toLowerCase());
      if(start<0)return;
      const end=start+phrase.length;
      p.querySelectorAll('.word').forEach(w=>w.classList.toggle('evidence',Number(w.dataset.start)<end&&Number(w.dataset.end)>start));
    });
  }
  function reveal(slide) {
    const solution=slide.querySelector('.solution');if(!solution)return;
    solution.hidden=false;
    const b=slide.querySelector('.reveal-btn');b.setAttribute('aria-expanded','true');b.textContent='הסתר תשובה';
    evidence(slide);
  }
  function markChoice(slide,button) {
    const feedback=slide.querySelector('.feedback');
    if(button.dataset.correct==='true') {
      button.classList.add('correct');
      slide.querySelectorAll('.choice').forEach(b=>b.disabled=true);
      feedback.textContent='נכון! בדקו את ההסבר והמידע התומך בתשובה.';feedback.className='feedback good';
      reveal(slide);
    } else {
      button.classList.add('wrong');
      feedback.textContent='נסו שוב. '+(slide.querySelector('.hint')?.textContent||'קראו שוב את המשפט.');feedback.className='feedback bad';
    }
  }
  function clearBuild(slide) {
    slide.querySelectorAll('.tile').forEach(t=>t.disabled=false);
    slide.querySelectorAll('.assembled').forEach(t=>t.remove());
    slide.querySelector('.assembly-placeholder').hidden=false;
    slide.querySelector('.assembly').classList.remove('solved');
    slide.querySelector('.feedback').className='feedback';slide.querySelector('.feedback').textContent='לחצו על החלקים לפי הסדר באנגלית, משמאל לימין.';
    slide.querySelector('.solution').hidden=true;slide.querySelector('.reveal-btn').setAttribute('aria-expanded','false');slide.querySelector('.reveal-btn').textContent='הצג משפט לדוגמה';
  }
  function checkBuild(slide) {
    const chosen=[...slide.querySelectorAll('.assembled')];
    const total=slide.querySelectorAll('.tile').length;
    const feedback=slide.querySelector('.feedback');
    if(chosen.length!==total){feedback.textContent='בחרו את כל חלקי המשפט לפני הבדיקה.';feedback.className='feedback bad';return;}
    if(chosen.every((t,i)=>Number(t.dataset.token)===i)) {
      feedback.textContent='נכון! הרכבתם משפט שלם.';feedback.className='feedback good';slide.querySelector('.assembly').classList.add('solved');reveal(slide);
    } else {feedback.textContent='בדקו את סדר המילים: על מי מדברים? מה קורה? מה מגיע אחר כך? לחצו על חלק כדי להחזיר אותו.';feedback.className='feedback bad';}
  }
  stage.addEventListener('click',event=> {
    const button=event.target.closest('button');if(!button)return;
    const slide=button.closest('.slide');
    if(button.classList.contains('speak')){speak(button);return;}
    if(button.classList.contains('choice')){markChoice(slide,button);return;}
    if(button.classList.contains('reveal-btn')) {
      const solution=slide.querySelector('.solution');
      if(!solution.hidden){solution.hidden=true;button.setAttribute('aria-expanded','false');button.textContent='הצג שוב את התשובה';stop();}
      else {
        reveal(slide);
        if(slide.classList.contains('challenge')) {
          slide.querySelectorAll('.choice').forEach(b=>{b.classList.toggle('correct',b.dataset.correct==='true');b.disabled=true;});
          const feedback=slide.querySelector('.feedback');feedback.textContent='זהו הפתרון. קראו גם את ההסבר.';feedback.className='feedback good';
        }
      }
      return;
    }
    if(button.classList.contains('tile')) {
      button.disabled=true;const area=slide.querySelector('.assembly');area.classList.remove('solved');
      slide.querySelector('.assembly-placeholder').hidden=true;
      const placed=document.createElement('button');placed.className='assembled';placed.type='button';placed.dataset.token=button.dataset.token;placed.textContent=button.textContent;placed.title='לחצו כדי להחזיר למחסן';area.append(placed);return;
    }
    if(button.classList.contains('assembled')) {
      slide.querySelector(`.tile[data-token="${button.dataset.token}"]`).disabled=false;button.remove();
      slide.querySelector('.assembly-placeholder').hidden=!!slide.querySelector('.assembled');slide.querySelector('.assembly').classList.remove('solved');
      slide.querySelector('.feedback').textContent='אפשר לשנות את הסדר ולבדוק שוב.';slide.querySelector('.feedback').className='feedback';return;
    }
    if(button.classList.contains('check-build'))checkBuild(slide);
    if(button.classList.contains('clear-build'))clearBuild(slide);
  });
  function show(index,updateHash=true) {
    stop();pos=Math.max(0,Math.min(slides.length-1,index));
    slides.forEach((s,i)=>{s.hidden=i!==pos;s.classList.toggle('active',i===pos);});
    slides[pos].scrollTop=0;
    document.querySelector('#counter').textContent=`${pos+1} / ${slides.length}`;
    document.querySelector('#progress').style.width=`${100*(pos+1)/slides.length}%`;
    document.querySelector('#prev').disabled=pos===0;document.querySelector('#next').disabled=pos===slides.length-1;
    document.querySelectorAll('[data-chapter]').forEach(b=>b.setAttribute('aria-current',String(b.dataset.chapter===slides[pos].dataset.section)));
    save(key,pos);
    if(updateHash)history.replaceState(null,'',`#slide-${pos+1}`);
  }
  document.querySelector('#prev').onclick=()=>show(pos-1);
  document.querySelector('#next').onclick=()=>show(pos+1);
  document.querySelector('#stop').onclick=stop;
  document.querySelector('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{}};
  document.querySelectorAll('[data-chapter]').forEach(b=>b.onclick=()=>show(slides.findIndex(s=>s.dataset.section===b.dataset.chapter)));
  document.querySelectorAll('.reveal-btn').forEach(b=>b.setAttribute('aria-expanded','false'));
  document.addEventListener('keydown',event=> {
    if(event.altKey||event.ctrlKey||event.metaKey||event.target.closest('input,textarea,select,[contenteditable=true]'))return;
    const forward=['ArrowRight','ArrowDown','PageDown'],back=['ArrowLeft','ArrowUp','PageUp'];
    if(forward.includes(event.key)||back.includes(event.key)){event.preventDefault();show(pos+(forward.includes(event.key)?1:-1));}
    if(event.key==='Home'){event.preventDefault();show(0);}
    if(event.key==='End'){event.preventDefault();show(slides.length-1);}
    if(event.key==='Escape')stop();
  });
  stage.addEventListener('touchstart',event=> {
    if(event.touches.length!==1||event.target.closest('button,a,input,select')){touch=null;return;}
    const s=slides[pos],t=event.touches[0];
    touch={x:t.clientX,y:t.clientY,top:s.scrollTop,bottom:s.scrollTop+s.clientHeight>=s.scrollHeight-4,pos};
  },{passive:true});
  stage.addEventListener('touchmove',event=>{if(event.touches.length!==1)touch=null;},{passive:true});
  stage.addEventListener('touchend',event=> {
    if(!touch||!event.changedTouches.length)return;
    const t=event.changedTouches[0],start=touch;touch=null;
    if(start.pos!==pos)return;
    const dx=t.clientX-start.x,dy=t.clientY-start.y;
    if(Math.max(Math.abs(dx),Math.abs(dy))<70)return;
    if(Math.abs(dx)>Math.abs(dy)*1.3){show(pos+(dx<0?1:-1));return;}
    if(Math.abs(dy)<=Math.abs(dx)*1.3)return;
    const s=slides[pos],long=s.scrollHeight>s.clientHeight+4;
    if(long&&!((dy<0&&start.bottom)||(dy>0&&start.top<=4)))return;
    show(pos+(dy<0?1:-1));
  },{passive:true});
  stage.addEventListener('touchcancel',()=>{touch=null;},{passive:true});
  stage.addEventListener('wheel',event=> {
    if(event.ctrlKey)return;const s=slides[pos];
    if(s.scrollHeight>s.clientHeight+4)return;
    if(Math.abs(event.deltaY)<40)return;event.preventDefault();
    if(Date.now()-wheelAt<650)return;wheelAt=Date.now();show(pos+(event.deltaY>0?1:-1));
  },{passive:false});
  function fromHash(){const match=location.hash.match(/^#slide-(\d+)$/);const index=match?Number(match[1])-1:Number(read(key,'0'));show(Number.isFinite(index)?index:0,false);}
  window.addEventListener('hashchange',fromHash);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  fromHash();
})();
