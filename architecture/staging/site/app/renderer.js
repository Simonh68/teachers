import {loadGrade} from './loader.js';
const labels={grade7:'כיתה ז׳',grade8:'כיתה ח׳',grade9:'כיתה ט׳',grade10:'כיתה י׳',grade11:'כיתה י״א',grade12:'כיתה י״ב'};
let controller;
const nav=document.querySelector('#grade-nav');
const root=document.querySelector('#materials');
const status=document.querySelector('#status');
function node(tag,text,cls){const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(cls)el.className=cls;return el;}
async function show(grade){
  controller?.abort();controller=new AbortController();
  status.textContent='טוען חומרי לימוד…';root.replaceChildren();
  try {
    const data=await loadGrade(grade,{signal:controller.signal});
    const fragment=document.createDocumentFragment();
    for(const item of data.materials){
      const card=node('article',undefined,'material');
      const title=node('h2',item.title);
      const unit=node('small',item.unit);
      const link=node('a','פתח חומר לימוד');
      link.href=item.url;
      if(new URL(link.href).origin!==location.origin){link.target='_blank';link.rel='noopener noreferrer';}
      card.append(unit,title);
      if(item.description)card.append(node('p',item.description));
      card.append(link);
      if(item.worksheet){const ws=node('a','דף עבודה');ws.href=item.worksheet;card.append(ws);}
      fragment.append(card);
    }
    root.replaceChildren(fragment);
    status.textContent=labels[grade]+' · '+data.materials.length+' פריטים';
  } catch(error) {
    if(error.name==='AbortError')return;
    status.textContent='לא ניתן לטעון את החומרים. נסו שוב.';
    const retry=node('button','נסה שוב');retry.addEventListener('click',()=>show(grade));root.replaceChildren(retry);
  }
}
for(const grade of Object.keys(labels)){const button=node('button',labels[grade]);button.type='button';button.addEventListener('click',()=>{history.replaceState(null,'','#'+grade);show(grade);});nav.append(button);}
show(Object.hasOwn(labels,location.hash.slice(1))?location.hash.slice(1):'grade7');
window.addEventListener('hashchange',()=>show(Object.hasOwn(labels,location.hash.slice(1))?location.hash.slice(1):'grade7'));
