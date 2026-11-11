'use strict';
const $ = id => document.getElementById(id);
const main = $('main');
const page = $('page');
const slides = lessons.flatMap((lesson, topic) => [
  ...lesson.units.flatMap(unit => ['phrase','noun','read','structure','question','answer'].map(phase => ({topic,unit,phase}))),
  {topic,phase:'transfer'}, {topic,phase:'solution'}
]);
let index = -1;
let muted = false;
let timer;
let reading = '';
const isRemote = new URLSearchParams(location.search).has('teacherRemote');
function escapeText(value) {
  return value.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
}
function mark(text, target, style) {
  const at = text.indexOf(target);
  if (at < 0) return escapeText(text);
  return escapeText(text.slice(0,at)) + '<strong class="'+style+'">'+escapeText(target)+'</strong>'+escapeText(text.slice(at+target.length));
}
function hebrew(text) { return '<p class="he" lang="he" dir="rtl">'+text+'</p>'; }
function card(text) { return '<p class="sentence">'+text+'</p>'; }
function line(unit) { return [unit.subject,unit.verb,unit.detail,unit.ending].join(' '); }
function stopReading() {
  clearTimeout(timer);
  window.speechSynthesis?.cancel();
}
function scheduleReading(text) {
  reading = text;
  if (!text || muted || isRemote || !window.speechSynthesis) return;
  timer = setTimeout(() => {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'en-US';
    speech.rate = 0.7;
    speechSynthesis.speak(speech);
  },4000);
}
function renderQuestion(unit, solved) {
  let html = '<p class="reference">'+escapeText(line(unit))+'</p><h2 class="question">'+escapeText(unit.question)+'</h2>';
  if (unit.choices) return html+'<ol class="choices" type="A">'+unit.choices.map(choice =>
    '<li'+(solved && choice===unit.answer?' class="correct"':'')+'>'+escapeText(choice)+(solved && choice===unit.answer?' ✓':'')+'</li>').join('')+'</ol>';
  if (solved) html+='<p class="answer">'+escapeText(unit.type==='complete'?unit.question.replace('___',unit.answer):unit.answer)+'</p>';
  return html;
}
function render(){
  stopReading();
  let body, label, spoken='';
  if(index<0){
    label='Grade 12 · Four units · Module C';
    body='<h1 class="lead">Sentence Detective<span>Part B</span></h1><div>'+lessons.map((lesson,n)=>'<button class="topic" data-topic="'+n+'">'+escapeText(lesson.name)+' →</button>').join('')+'</div><div class="coverlinks"><a href="../sentence-detective/">Part A</a></div>';
  }else{
    const {topic,unit,phase}=slides[index];
    const lesson=lessons[topic];
    label=lesson.name;
    switch(phase){
      case 'phrase':
        body=card(escapeText(unit.subject))+hebrew('מהו שם העצם המרכזי בצירוף?');
        spoken=unit.subject; break;
      case 'noun':
        body=card(mark(unit.subject,unit.head,'head'))+'<div class="words">'+unit.words.map(([en,he])=>'<div>'+escapeText(en)+' <span lang="he" dir="rtl">'+escapeText(he)+'</span></div>').join('')+'</div>';
        break;
      case 'read':
        body=card(escapeText(line(unit)))+hebrew('מה עושה הנושא, ואיזה פרט מוסיף המשך המשפט?');
        spoken=line(unit); break;
      case 'structure':
        body=card('<span class="subject">'+mark(unit.subject,unit.head,'head')+'</span> <strong class="verb">'+escapeText(unit.verb)+'</strong> '+mark(unit.detail+' '+unit.ending,unit.link,'logic'))+hebrew('<span class="subject">נושא</span> · <span class="verb">פועל מרכזי</span> · <span class="logic">'+escapeText(unit.link)+'</span> — '+escapeText(unit.meaning));
        break;
      case 'question': case 'answer':
        body=renderQuestion(unit,phase==='answer');
        spoken=phase==='question'?(unit.type==='complete'?'':unit.question):(unit.type==='complete'?unit.question.replace('___',unit.answer):unit.answer);break;
      case 'transfer': case 'solution':
        label+=' · Independent reading';
        body='<p class="passage">'+(phase==='solution'?mark(lesson.passage,lesson.evidence,'logic'):escapeText(lesson.passage))+'</p><h2 class="question">'+escapeText(lesson.prompt)+'</h2>';
        if(phase==='solution')body+='<p class="answer">'+escapeText(lesson.prompt.includes('___')?lesson.prompt.replace('___',lesson.response):lesson.response)+'</p>';
        spoken=phase==='transfer'?lesson.passage:(lesson.prompt.includes('___')?lesson.prompt.replace('___',lesson.response):lesson.response);break;
    }
  }
  page.innerHTML='<p class="kicker">'+escapeText(label)+'</p>'+body;
  $('counter').textContent=index<0?'Part B':(index+1)+' / '+slides.length;
  $('prev').disabled=index<0;
  $('next').disabled=index===slides.length-1;
  $('progress').style.width=(index+1)/slides.length*100+'%';
  main.scrollTop=0;
  scheduleReading(spoken);
}
function show(destination){
  if(destination < -1 || destination >= slides.length || destination===index)return;
  index=destination;render();
}
$('next').onclick=()=>show(index+1);
$('prev').onclick=()=>show(index-1);
page.onclick=e=>{
  const button=e.target.closest('[data-topic]');
  if(button)show(slides.findIndex(s=>s.topic===Number(button.dataset.topic)));
};
$('audio').onclick=()=>{
  muted=!muted;
  $('audio').setAttribute('aria-pressed',String(muted));
  $('audio').setAttribute('aria-label',muted?'Enable reading':'Mute reading');
  $('audio').textContent=muted?'🔇':'🔊';
  stopReading();if(!muted)scheduleReading(reading);
};
$('full').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.();
document.addEventListener('keydown',e=>{
  if(e.defaultPrevented||e.altKey||e.metaKey||e.ctrlKey||e.target.closest?.('#teachers-qr-remote-host,input,textarea,select'))return;
  let delta=0;
  if(['ArrowRight','ArrowDown','PageDown'].includes(e.key))delta=1;
  if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key))delta=-1;
  if(delta){e.preventDefault();show(index+delta);}
});
function atEdge(delta){
  return delta>0?main.scrollTop+main.clientHeight>=main.scrollHeight-3:main.scrollTop<=3;
}
let touch;
main.addEventListener('touchstart',e=>{
  touch=null;
  if(e.touches.length!==1||e.target.closest('a,button'))return;
  const point=e.touches[0];
  touch={x:point.clientX,y:point.clientY,top:atEdge(-1),bottom:atEdge(1)};
},{passive:true});
main.addEventListener('touchmove',e=>{if(e.touches.length!==1)touch=null;},{passive:true});
main.addEventListener('touchend',e=>{
  const start=touch;touch=null;
  if(!start||e.changedTouches.length!==1)return;
  const dx=e.changedTouches[0].clientX-start.x,dy=e.changedTouches[0].clientY-start.y;
  if(Math.max(Math.abs(dx),Math.abs(dy))<45)return;
  if(Math.abs(dx)>Math.abs(dy)*1.2)show(index+(dx<0?1:-1));
  else if(Math.abs(dy)>Math.abs(dx)*1.2 && (dy<0?start.bottom:start.top))show(index+(dy<0?1:-1));
},{passive:true});
main.addEventListener('touchcancel',()=>{touch=null;});
let lastWheel=0;
main.addEventListener('wheel',e=>{
  if(e.ctrlKey||!e.deltaY||Math.abs(e.deltaX)>Math.abs(e.deltaY))return;
  const delta=Math.sign(e.deltaY);
  if(!atEdge(delta))return;
  e.preventDefault();
  const now=performance.now();const elapsed=now-lastWheel;lastWheel=now;
  if(elapsed>220)show(index+delta);
},{passive:false});
window.addEventListener('pagehide',stopReading);
render();
