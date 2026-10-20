(() => {
const D=window.REWARDS_ESSAY;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const support=s=>`<p class="support">${esc(s)}</p>`;
const starts=[4,9,14,19];
function tracker(p){return `<nav class="paragraph-tracker" aria-label="Essay paragraphs">${D.names.map((n,i)=>`<a class="paragraph-square ${i===p?'current':''}" href="#slide-${starts[i]}" data-now="Writing now" ${i===p?'aria-current="step"':''}><b>${i+1}</b><span>${n}</span></a>`).join('')}</nav>`;}
function sentence(p,s){return D.parts[p][s].map((x,i)=>typeof x==='string'?esc(x):`<span class="word-switch" role="button" tabindex="0" data-phrase="${p}-${s}-${i}" data-options="${esc(JSON.stringify(x))}" data-choice="0" title="Click for another wording">${esc(x[0])}</span>`).join('');}
const paragraph=p=>`<p>${sentence(p,0)} ${sentence(p,1)}</p>`;
const slides=[];
function add(title,body,{p=-1,essay=false,topic=false}={}){slides.push({title,html:`<div class="frame">${p>=0?tracker(p):''}<div class="slide-meta"><div class="eyebrow">${esc(title)}</div>${topic?`<div class="essay-topic-compact en">${D.topic}</div>`:''}</div>${body}</div>`,essay});}
add('Write an essay on the following topic:',`<h1 class="main-copy en">${D.topic}</h1><p class="support en">State your opinion. Support it with reasons and examples.</p>`+support('Module G, Winter 2023, Question 10. Write 120–140 words.')+`<p class="small">${esc(D.format)} · Base model: ${D.baseWords} words</p>`);
add('Four paragraphs',tracker(-1)+support(D.structure)+support('Phrases change with yellow and orange highlighting. Click to change a phrase yourself, adjust the speed or pause.'));
add('Both parts of the task',`<p class="main-copy en"><mark>Rewards</mark> for <mark>helping at home</mark></p>`+support(D.focus)+support('This is one possible position. You can choose and support another view.'));
for(let p=0;p<4;p++){
 for(let s=0;s<2;s++){
  const c=D.coaching[p*2+s],n=p*2+s+1;
  add(`Sentence ${n} · Your idea`,`<h2 class="main-copy">${esc(c.prompt)}</h2><details class="starting-point"><summary>A simple starting point</summary><p class="short en">${esc(c.simple)}</p></details>`,{p});
  add(`Sentence ${n} · Develop and vary`,`<p class="main-copy en">${sentence(p,s)}</p>`+support(c.note)+`<p class="count en" aria-live="polite"></p>`,{p});
 }
 add(`Paragraph ${p+1} · Check the connection`,`<div class="essay en">${paragraph(p)}</div>`+support(D.paragraphNotes[p])+`<p class="count en" aria-live="polite"></p>`,{p,essay:true});
}
add('Final Draft',`<div class="essay en">${[0,1,2,3].map(paragraph).join('')}</div><p class="count en" aria-live="polite" data-full-count></p>`,{essay:true,topic:true});
function grammarSlides(){
 for(const g of D.grammar)add(g.title,`${g.location?`<p class="small">${esc(g.location)}</p>`:''}<p class="main-copy en"><mark class="${g.color}">${esc(g.example)}</mark></p><p class="short en">${esc(g.pattern)}</p>`+support(g.note));
 add(D.grammarSummaryTitle||'Grammar in the base essay',`<div class="grammar-summary en">${D.grammar.map(g=>`<p><strong>${esc(g.title)}</strong><br><mark class="${g.color}">${esc(g.pattern)}</mark>${g.summaryExample?`<br><span class="small">${esc(g.summaryExample)}</span>`:''}</p>`).join('')}</div>`+support(D.grammarSummaryNote||'These structures occur in the base essay. Choose a structure that fits the idea you want to express.'));
}
if(!D.grammarAtEnd)grammarSlides();
add('Choose a useful connector',`<div class="connector-guide en">${D.connectors.map(c=>`<p><strong>${esc(c.job)}</strong><br><mark>${esc(c.phrase)}</mark><br><span>${esc(c.example)}</span></p>`).join('')}</div>`+support('Choose a connector for its purpose. A clear reason and a concrete example matter more than a long opening phrase.'));
add('Your own essay',`<p class="short en">${D.topic}</p>`+support('Write four paragraphs. Address rewards and help at home, and keep your position consistent.')+`<label class="draft-label" for="own-draft">Draft in English</label><textarea id="own-draft" dir="ltr" aria-label="Draft in English"></textarea><p id="draft-count" class="count en" aria-live="polite"></p>`+support('Before finishing, check your household example, verb forms, spelling and 120–140 words.'));
if(D.grammarAtEnd)grammarSlides();
document.getElementById('stage').innerHTML=slides.map((s,i)=>`<section class="slide ${s.essay?'essay':'info'}" hidden id="slide-${i+1}" data-slide="${i+1}" aria-label="${esc(s.title)}">${s.html}</section>`).join('');
document.getElementById('slide-menu').innerHTML=slides.map((s,i)=>`<option value="${i+1}">${i+1}. ${esc(s.title)}</option>`).join('');
window.REWARDS_UI={esc,slides:slides.map(s=>s.title),starts};
})();
