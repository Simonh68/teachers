/* Shared Read-Along browser speech fallback.
   Word-boundary events are not reliable on Android; estimated progress is used when absent.
   For sample-accurate sync use recorded audio plus word timestamps. */
(()=>{'use strict';
window.TeacherReadAlongSpeech=class {
 constructor(button,deck){this.button=button;this.deck=deck;this.synth=window.speechSynthesis;this.token=0;this.parts=[];this.index=0;this.paused=false;this.timer=null;this.progressTimer=null;this.active=null;this.utterance=null;this.wordIndex=0;this.boundarySeen=false;this.elapsed=0;this.started=0;this.duration=0;
  button.addEventListener('click',()=>this.toggle());
  new MutationObserver(changes=>{if(changes.some(x=>x.target.classList?.contains('slide')))this.stop();}).observe(deck,{subtree:true,attributes:true,attributeFilter:['class']});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)this.stop()});
 }
 mark(word){this.active?.classList.remove('readalong-current');this.active=word||null;this.active?.classList.add('readalong-current');}
 stop(){this.token++;clearTimeout(this.timer);clearInterval(this.progressTimer);this.timer=null;this.progressTimer=null;this.synth?.cancel();this.parts=[];this.index=0;this.paused=false;this.mark(null);this.button.textContent='🔊 Read';}
 prepare(el){if(!el.dataset.raWords){const walk=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),nodes=[];while(walk.nextNode())nodes.push(walk.currentNode);for(const node of nodes){const f=document.createDocumentFragment();for(const t of node.textContent.match(/\s+|[^\s]+/g)||[]){if(/^\s+$/.test(t))f.append(document.createTextNode(t));else{const s=document.createElement('span');s.className='readalong-word';s.textContent=t;f.append(s)}}node.replaceWith(f)}el.dataset.raWords='1'}
 const words=[...el.querySelectorAll('.readalong-word')],groups=[];let g=[];
 for(const w of words){g.push(w);if(/[.!?;:]$/.test(w.textContent)){groups.push(g);g=[]}}if(g.length)groups.push(g);
 return groups.map(words=>({words,text:words.map(w=>w.textContent).join(' '),pause:/[.!?]$/.test(words.at(-1).textContent)?1000:450}));
 }
 play(){if(this.index>=this.parts.length){this.stop();return}const id=this.token,p=this.parts[this.index],u=new SpeechSynthesisUtterance(p.text);this.utterance=u;u.lang='en-US';u.rate=.75;this.wordIndex=0;this.boundarySeen=false;this.elapsed=0;this.started=performance.now();this.mark(p.words[0]);
 const offsets=[];let at=0;for(const w of p.words){offsets.push(at);at+=w.textContent.length+1}
 const weights=p.words.map(w=>Math.max(1.5,w.textContent.replace(/[^a-z]/gi,'').length*.52));const total=weights.reduce((a,b)=>a+b,0);
 this.duration=Math.max(850,p.words.length*330,total*125)/u.rate;
 u.onboundary=e=>{if(id!==this.token||e.name!=='word')return;this.boundarySeen=true;let n=0;for(let i=0;i<offsets.length;i++)if(offsets[i]<=e.charIndex)n=i;this.wordIndex=n;this.mark(p.words[n])};
 this.progressTimer=setInterval(()=>{if(id!==this.token||this.paused||this.boundarySeen)return;const t=Math.min(1,(this.elapsed+performance.now()-this.started)/this.duration);let target=t*total,acc=0,n=0;for(let i=0;i<weights.length;i++){acc+=weights[i];if(target<acc){n=i;break}n=i}if(n!==this.wordIndex){this.wordIndex=n;this.mark(p.words[n])}},65);
 u.onend=()=>{if(id!==this.token)return;clearInterval(this.progressTimer);this.progressTimer=null;this.mark(null);this.index++;if(this.index>=this.parts.length){this.stop();return}this.timer=setTimeout(()=>{this.timer=null;if(id===this.token&&!this.paused)this.play()},p.pause)};
 u.onerror=()=>{if(id===this.token)this.stop()};
 this.synth.speak(u);this.button.textContent='⏸ Pause';
 }
 toggle(){if(!this.synth)return;if(this.paused){this.paused=false;this.started=performance.now();if(this.synth.paused)this.synth.resume();else if(this.timer===null)this.play();else{clearTimeout(this.timer);this.timer=null;this.play()}this.button.textContent='⏸ Pause';return}
 if(this.synth.speaking||this.timer!==null){this.paused=true;this.elapsed+=performance.now()-this.started;if(this.synth.speaking)this.synth.pause();if(this.timer!==null){clearTimeout(this.timer);this.timer=null}this.button.textContent='▶ Resume';return}
 this.stop();const el=this.deck.querySelector('.slide.active .reading, .slide.active .quote, .slide.active .question, .slide.active .model-answer, .slide.active .text-en');if(!el){this.button.textContent='No text';return}this.parts=this.prepare(el);if(this.parts.length)this.play();
 }
};
})();