
// Only the two-choice activity lives locally; the central deck owns all navigation.
(() => {
 const pairs=new Map();
 document.querySelectorAll('[data-pair]').forEach(s=>{let a=pairs.get(s.dataset.pair)||[];a.push(s);pairs.set(s.dataset.pair,a)});
 // Balance A/B across the whole lesson, then shuffle; avoid long same-letter runs.
 const randomIndex=n=>{const limit=256-256%n;let x;do{x=crypto.getRandomValues(new Uint8Array(1))[0]}while(x>=limit);return x%n};
 let positions;
 do {
   positions=Array.from({length:pairs.size},(_,i)=>i<Math.ceil(pairs.size/2)?0:1);
   for(let i=positions.length-1;i>0;i--){const j=randomIndex(i+1);[positions[i],positions[j]]=[positions[j],positions[i]];}
 } while(positions.some((x,i)=>i>=2&&x===positions[i-1]&&x===positions[i-2]));
 let questionIndex=0;
 pairs.forEach(members=>{
   const flip=positions[questionIndex++];
   members.forEach(slide=>{const box=slide.querySelector('.choices');if(flip)box.append(box.firstElementChild);[...box.children].forEach((b,i)=>b.querySelector('.letter').textContent=i?'B':'A')});
   const question=members.find(s=>!s.classList.contains('reveal'));
   question.querySelectorAll('.choice').forEach(button=>button.addEventListener('click',()=>{
     members.forEach(slide=>slide.querySelectorAll('.choice').forEach(b=>{const chosen=b.dataset.option===button.dataset.option;b.classList.toggle('selected',chosen);if(!b.disabled)b.setAttribute('aria-pressed',String(chosen))}));
     question.querySelector('.status').textContent='הבחירה סומנה. הסבירו מדוע; עברו לשקף הבא לתשובה לדוגמה.';
   }));
 });
})();
