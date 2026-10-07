(()=>{'use strict';
const english=document.documentElement.lang==='en';
const L=(he,en)=>english?en:he;
const games=location.pathname.includes('grammar-in-an-essay');
const labels=[L('פתיחה','Opening'),L('נגד','Against'),L('בעד','For'),L('סיכום','Conclusion')];
const parks=location.pathname.includes('for-and-against-parks');
const demo=games?['School games have helped many students make friends. I believe that giving everyone a chance to play is important.','On the one hand, including every student can make winning harder. Some teams have lost because inexperienced players have made mistakes.']:parks?['Local parks have become important places for families. I believe that spending time outdoors can improve our health.','On the one hand, building parks can be expensive. Some towns have spent more money than they had planned.']:['Using AI at school has become common. I believe that using it responsibly can help students learn.','On the one hand, relying on AI can reduce independent thinking. Some students have stopped checking their own answers.'];
const oldSlides=[...document.querySelectorAll('.slide')];
const instruction=document.createElement('section');instruction.className='slide info paragraph-layout';instruction.hidden=true;instruction.dataset.completed='0';instruction.dataset.words='0';instruction.dataset.writingStep='0';
instruction.innerHTML=`<div class="frame"><div class="slide-meta"><div class="eyebrow">${L('ארבע פסקאות — ארבעה ריבועי מעקב','Four paragraphs — four tracking squares')}</div></div><h2>${L('סוף פסקה ← רווח ברור ← פסקה חדשה','END A PARAGRAPH · LEAVE A GAP · START A NEW ONE')}</h2><p class="paragraph-gap-caption">${L('מיישרים את האנגלית לשמאל. בין פסקאות משאירים רווח ברור. כאן הרווח מדגים שלוש שורות ריקות.','Align English to the left. Leave a clear gap between paragraphs. This display shows a gap of three blank lines.')}</p><div class="essay en" lang="en"><p>${demo[0]}</p><p>${demo[1]}</p></div></div>`;
oldSlides[games?3:2].after(instruction);
const slides=[...document.querySelectorAll('.slide')];
document.querySelectorAll('.lesson-sections a[href^="#slide-"]').forEach(a=>{const old=Number(a.hash.replace('#slide-',''));if(old>(games?4:3))a.hash='slide-'+(old+1);});
const map=games?[0,1,1,2,2,3,3,4,4,2,3]:[0,1,1,2,2,2,3,3,3,4,4];
slides.forEach((slide,i)=>{
slide.dataset.slide=String(i+1);slide.id='slide-'+(i+1);slide.setAttribute('aria-label',L('שקף','Slide')+' '+(i+1)+' / '+slides.length);
let step=Number(slide.dataset.writingStep)||Number(slide.dataset.completed)||0;
// Short prompts with a completed count introduce the next model sentence.
if(!games&&slide.querySelector('.short')&&!slide.querySelector('.answer-slot .main-copy'))step=Math.min(10,step+1);
const current=slide===instruction?2:map[step]||0;slide.dataset.activeParagraph=String(current);
const tracker=document.createElement('div');tracker.className='paragraph-tracker';tracker.setAttribute('aria-label',L('מעקב ארבע פסקאות','Four paragraph progress'));
labels.forEach((label,n)=>{const square=document.createElement('div');square.className='paragraph-square'+(current===n+1?' current':'');square.dataset.paragraph=String(n+1);square.dataset.now=L('כותבים עכשיו','Writing now');square.innerHTML='<b>'+(n+1)+'</b><span>'+label+'</span>';if(current===n+1)square.setAttribute('aria-current','step');tracker.append(square);});
const frame=slide.querySelector('.frame');if(frame)frame.prepend(tracker);
slide.querySelectorAll('.essay.en').forEach(essay=>{[...essay.children].filter(p=>p.tagName==='P').forEach((p,n)=>{if(!p.textContent.trim())return;p.classList.add('essay-paragraph');p.dataset.start='▶ '+L('תחילת פסקה','PARAGRAPH START')+' '+(n+1);p.dataset.end='■ '+L('סוף פסקה','PARAGRAPH END')+' '+(n+1);});});
});
})();
