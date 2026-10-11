
// Only the two-choice activity lives locally; the central deck owns all navigation.
(() => {
 const pairs=new Map();
 document.querySelectorAll('[data-pair]').forEach(s=>{let a=pairs.get(s.dataset.pair)||[];a.push(s);pairs.set(s.dataset.pair,a)});
 pairs.forEach(members=>{
   const flip=crypto.getRandomValues(new Uint8Array(1))[0]%2;
   members.forEach(slide=>{const box=slide.querySelector('.choices');if(flip)box.append(box.firstElementChild);[...box.children].forEach((b,i)=>b.querySelector('.letter').textContent=i?'B':'A')});
   const question=members.find(s=>!s.classList.contains('reveal'));
   question.querySelectorAll('.choice').forEach(button=>button.addEventListener('click',()=>{
     members.forEach(slide=>slide.querySelectorAll('.choice').forEach(b=>{const chosen=b.dataset.option===button.dataset.option;b.classList.toggle('selected',chosen);if(!b.disabled)b.setAttribute('aria-pressed',String(chosen))}));
     question.querySelector('.status').textContent='הבחירה סומנה. הסבירו מדוע; עברו לשקף הבא לתשובה לדוגמה.';
   }));
 });
})();
