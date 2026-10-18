/* Local practice interactions only. shared/deck/standard.js owns navigation. */
document.querySelectorAll('.match-options').forEach(group=>{
  group.addEventListener('click',event=>{
    const button=event.target.closest('.match-option');
    if(!button)return;
    group.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  });
});
document.querySelectorAll('details').forEach(details=>details.addEventListener('toggle',()=>window.dispatchEvent(new Event('resize'))));
