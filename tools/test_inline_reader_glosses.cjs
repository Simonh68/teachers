/* Regression: the prerecorded reader resolves data-gloss as a numeric unit index.
   Runs the real hover handlers against a small DOM/clock substitute; not browser QA. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const {install}=require(path.join(root,'shared/read-along/inline-reader.js'));
global.Audio=class{addEventListener(){} pause(){}};
function fixture(){
 const events={},timers=new Map(),nodes=[],bubbles=[];let serial=0;
 class Node{
  constructor(gloss){this.dataset=gloss===undefined?{}:{gloss:String(gloss)};this.attrs={};this.style={};this.isConnected=true;this.classes=new Set();this.classList={add:n=>this.classes.add(n),remove:n=>this.classes.delete(n),contains:n=>this.classes.has(n)};nodes.push(this)}
  closest(selector){if(selector==='[data-gloss]')return this.dataset.gloss===undefined?null:this;if(selector==='dialog')return this.dialog||null;return null}
  contains(other){return this===other}
  getBoundingClientRect(){return {left:300,top:300,width:100,height:24,right:400,bottom:324}}
  setAttribute(k,v){this.attrs[k]=v}removeAttribute(k){delete this.attrs[k]}
  append(node){node.parent=this;bubbles.push(node)}
  remove(){this.isConnected=false;const i=bubbles.indexOf(this);if(i>=0)bubbles.splice(i,1)}
 }
 const body=new Node();const win={innerWidth:1200,innerHeight:900,setTimeout(fn,ms){timers.set(++serial,{fn,ms});return serial},clearTimeout(id){timers.delete(id)},requestAnimationFrame(){return ++serial},addEventListener(){}};
 const doc={defaultView:win,body,addEventListener(name,fn){events[name]=fn},createElement(){return new Node()},querySelectorAll(selector){return selector==='[data-gloss-toggle]'?[toggle]:selector.startsWith('.')?nodes.filter(n=>n.isConnected&&n.classes.has(selector.slice(1))):[]}};
 const toggle={checked:true,matches:s=>s==='[data-gloss-toggle]'};
 return {doc,Node,events,timers,bubbles,toggle};
}
for(const folder of ['grade12/four-units/module-c-school-radio','grade11/module-e-museum-bag','grade11/module-e-time-bank']){
 const file=name=>path.join(root,folder,name),gloss=JSON.parse(fs.readFileSync(file('glossary.json'))),html=fs.readFileSync(file('index.html'),'utf8');
 const embedded=JSON.parse(html.match(/<script id="gloss-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);assert.deepEqual(embedded,gloss);
 const f=fixture(),reader=install({document:f.doc,records:[],glosses:embedded.units});
 // Check real bubble creation for every word, not just data coverage.
 for(const w of embedded.words){
  const node=new f.Node(w.gloss);f.events.pointerover({target:node,pointerType:'mouse',relatedTarget:null});
  assert.equal(f.bubbles.length,1,`${folder}: no hover bubble for word ${w.id} (${w.text})`);
  assert.equal(f.bubbles[0].textContent,embedded.units[Number(w.gloss)].he);
  assert.equal(f.bubbles[0].attrs.role,'tooltip');assert.equal(f.bubbles[0].dir,'rtl');
  assert(f.timers.size===1&&[...f.timers.values()][0].ms===3500);reader.clear();assert.equal(f.bubbles.length,0);
 }
 const word=new f.Node(embedded.words[0].gloss);
 f.events.click({target:word});assert.equal(f.bubbles.length,1,'phone tap');
 const fade=[...f.timers.values()][0];fade.fn();assert(f.bubbles[0].classes.has('ra-fading'));assert([...f.timers.values()].some(t=>t.ms===1000));reader.clear();
 f.events.focusin({target:word});assert.equal(f.bubbles.length,1,'keyboard focus');reader.clear();
 f.events.keydown({target:word,key:'Enter',preventDefault(){}});assert.equal(f.bubbles.length,1,'keyboard activation');reader.clear();
 const dialog=new f.Node();word.dialog=dialog;f.events.pointerover({target:word,pointerType:'mouse',relatedTarget:null});assert.equal(f.bubbles[0].parent,dialog,'dialog top layer');reader.clear();
 f.toggle.checked=false;f.events.change({target:f.toggle});f.events.click({target:word});assert.equal(f.bubbles.length,0,'disabled toggle');
 f.toggle.checked=true;f.events.change({target:f.toggle});f.events.click({target:word});assert.equal(f.bubbles.length,1,'re-enabled toggle');reader.clear();
 console.log(`PASS ${folder}: ${embedded.words.length} word hover bubbles, Hebrew content, tap/focus/Enter, fade timing, full-text dialog and toggle.`);
}
