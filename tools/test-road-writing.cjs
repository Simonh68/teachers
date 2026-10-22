/* Behavioral checks; run with jsdom installed (NODE_PATH may point to it). */
const {JSDOM}=require('jsdom');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
const html=fs.readFileSync(path.join(root,'grade10/group-a/road-writing-minimum/index.html'),'utf8');
const data=JSON.parse(fs.readFileSync(path.join(root,'grade10/group-a/road-writing-minimum/questions.json')));
const dom=new JSDOM(html,{url:'https://example.test/grade10/group-a/road-writing-minimum/',runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window,d=w.document;
Object.defineProperty(d,'fonts',{value:{ready:Promise.resolve()}});
let now=0,nextId=0;const tasks=new Map();
w.setTimeout=(fn,delay=0)=>{const id=++nextId;tasks.set(id,{fn,at:now+delay});return id;};
w.clearTimeout=id=>tasks.delete(id);
w.Date.now=()=>now;
const flush=()=>new Promise(resolve=>setImmediate(resolve));
async function tick(ms){const until=now+ms;while(true){const first=[...tasks].filter(([,v])=>v.at<=until).sort((a,b)=>a[1].at-b[1].at)[0];if(!first)break;now=first[1].at;tasks.delete(first[0]);first[1].fn();await flush();}now=until;await flush();}
const all=[...d.querySelectorAll('.slide')];
all.forEach(s=>{Object.defineProperty(s,'clientHeight',{value:600,configurable:true});Object.defineProperty(s,'scrollHeight',{value:600,configurable:true});});
w.eval(fs.readFileSync(path.join(root,'shared/deck/standard.js'),'utf8'));
w.eval(fs.readFileSync(path.join(root,'shared/deck/sentence-sequence.js'),'utf8'));
const active=()=>d.querySelector('.slide.active');
const choices=()=>[...active().querySelectorAll('.sentence-choice')].map(e=>Number(e.dataset.choice));
const jump=async n=>{w.location.hash=`slide-${n}`;w.dispatchEvent(new w.Event('hashchange'));await flush();};
function touch(el,from,to){const start=new w.Event('touchstart',{bubbles:true});Object.defineProperty(start,'touches',{value:[{clientX:from[0],clientY:from[1]}]});el.dispatchEvent(start);const end=new w.Event('touchend',{bubbles:true});Object.defineProperty(end,'changedTouches',{value:[{clientX:to[0],clientY:to[1]}]});el.dispatchEvent(end);}
(async()=>{
  assert.equal(all.length,36);
  data.forEach((q,i)=>{
    assert.equal(all[i*6].querySelector('.question-en').textContent,q.question);
    assert.equal(all[i*6+1].querySelector('.question-en').outerHTML,all[i*6].querySelector('.question-en').outerHTML);
    assert.ok(all[i*6].querySelector('.question-translation.unrevealed'));
    assert.ok(!all[i*6+1].querySelector('.question-translation.unrevealed'));
    q.sentences.forEach(s=>assert.equal(new Set(s).size,6));
  });
  assert.equal(d.querySelectorAll('input,textarea').length,0);
  assert.equal(all[17].querySelector('blockquote').textContent,'“Had worn them really about the same”');
  assert.equal(all[17].querySelectorAll('.sentence-answer').length,0);
  await jump(5);
  assert.deepEqual(choices(),[0,0]);await tick(9999);assert.deepEqual(choices(),[0,0]);
  await tick(1);assert.deepEqual(choices(),[1,0]);await tick(10000);assert.deepEqual(choices(),[1,1]);
  for(let n=2;n<=6;n++){await tick(10000);assert.deepEqual(choices(),[n%6,(n-1)%6]);await tick(10000);assert.deepEqual(choices(),[n%6,n%6]);}
  active().querySelector('.sequence-toggle').click();const paused=choices();await tick(30000);assert.deepEqual(choices(),paused);
  active().querySelector('.sentence-choice').click();assert.deepEqual(choices(),[1,0]);
  active().querySelector('.sequence-toggle').click();await tick(10000);assert.deepEqual(choices(),[1,1]);
  await jump(6);assert.deepEqual(choices(),[1,1]);await tick(10000);assert.deepEqual(choices(),[2,1]);
  await jump(7);await tick(30000);assert.equal(d.getElementById('slide-6').dataset.automaticCycles,'1');
  await jump(35);assert.deepEqual(choices(),[0,0]);await tick(10000);assert.deepEqual(choices(),[1,0]);await tick(10000);assert.deepEqual(choices(),[1,1]);
  Object.defineProperty(d,'hidden',{value:true,configurable:true});d.dispatchEvent(new w.Event('visibilitychange'));await tick(30000);assert.deepEqual(choices(),[1,1]);
  Object.defineProperty(d,'hidden',{value:false,configurable:true});d.dispatchEvent(new w.Event('visibilitychange'));await tick(10000);assert.deepEqual(choices(),[2,1]);
  await jump(36);await tick(10000);assert.deepEqual(choices(),[3,1]);
  await jump(5);const el=active().querySelector('.sentence-choice');touch(el,[250,250],[120,250]);await flush();assert.equal(active().id,'slide-6');
  touch(active(),[120,250],[250,250]);await flush();assert.equal(active().id,'slide-5');
  touch(active(),[150,350],[150,200]);await flush();assert.equal(active().id,'slide-6');
  touch(active(),[150,200],[150,350]);await flush();assert.equal(active().id,'slide-5');
  // A reading swipe that starts inside a long slide must not turn the page.
  Object.defineProperty(active(),'scrollHeight',{value:1000,configurable:true});active().scrollTop=150;
  touch(active(),[150,350],[150,200]);await flush();assert.equal(active().id,'slide-5');
  active().scrollTop=400;touch(active(),[150,350],[150,200]);await flush();assert.equal(active().id,'slide-6');
  await jump(1);touch(active(),[100,200],[250,200]);await flush();assert.equal(active().id,'slide-1');
  await jump(36);touch(active(),[250,200],[100,200]);await flush();assert.equal(active().id,'slide-36');
  dom.window.close();console.log('PASS: 36 steps, 72 variants, 10-second alternating cadence, all six options, pause/manual/resume, Q6, summary, visibility cancellation, fixed question markup, copy task, swipe directions and scroll boundaries.');
})().catch(e=>{console.error(e);process.exitCode=1;dom.window.close();});
