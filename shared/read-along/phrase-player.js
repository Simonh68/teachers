/* Recorded audio only. Pauses run on the wall clock, never the slowed audio clock. */
(()=>{'use strict';
class TeacherPhrasePlayer{
 constructor(records,{pauseMs=1500,onUpdate=()=>{},onComplete=()=>{}}={}){
  this.records=records;this.pauseMs=pauseMs;this.onUpdate=onUpdate;this.onComplete=onComplete;
  this.audio=new Audio();this.audio.preload='auto';this.audio.preservesPitch=true;
  this.rate=(window.TEACHERS_READALONG_STANDARD?.defaultSpeed??.75);this.sentence=0;this.part=0;this.offset=0;this.queue=[];this.phase='idle';this.intent=false;this.unlocked=false;
  this.generation=0;this.timer=null;this.raf=null;this.gap=null;this.cache=new Map();this.events=[];
  this.audio.onended=()=>{if(!this.intent||this.phase!=='playing')return;this.log('part:end');cancelAnimationFrame(this.raf);const next=this.next();if(next){this.gap={...next,remaining:this.pauseMs};this.scheduleGap();}else{this.intent=false;this.phase='ended';this.gap=null;this.update();this.log('page:end');this.onComplete(this.sentence);}};
  this.audio.onerror=()=>{if(this.intent){this.intent=false;this.phase='error';this.clearTimers();this.log('audio:error');this.update();}};
 }
 log(type,detail={}){this.events.push({type,sentence:this.sentence,part:this.part,at:performance.now(),...detail});if(this.events.length>500)this.events.shift();}
 update(){this.onUpdate(this);}
 clearTimers(){clearTimeout(this.timer);cancelAnimationFrame(this.raf);this.timer=null;this.raf=null;}
 get record(){return this.records[this.sentence];}
 get segment(){return this.record?.parts[this.part];}
 get sourceTime(){if(!this.segment)return 0;if(['gap','pausedGap','ended'].includes(this.phase))return this.segment.sourceEnd;const t=this.phase==='paused'?this.offset:this.audio.currentTime;return Math.min(this.segment.sourceEnd,this.segment.sourceStart+(t||0));}
 get isActive(){return this.intent&&['loading','playing','gap'].includes(this.phase);}
 next(){if(this.part+1<this.record.parts.length)return{sentence:this.sentence,part:this.part+1};const i=this.queue.indexOf(this.sentence);return i>=0&&i+1<this.queue.length?{sentence:this.queue[i+1],part:0}:null;}
 prepare(s,p){const path=this.records[s]?.parts[p]?.src;if(!path)return Promise.reject(Error('Missing phrase recording'));
  if(!this.cache.has(path)){const promise=fetch(path).then(r=>{if(!r.ok)throw Error('Audio HTTP '+r.status);return r.blob();}).then(blob=>URL.createObjectURL(blob)).catch(e=>{this.cache.delete(path);throw e;});this.cache.set(path,promise);}return this.cache.get(path);
 }
 prefetch(){const next=this.next();if(next)this.prepare(next.sentence,next.part).catch(()=>{});}
 async loadAndPlay(s,p,offset=0){
  this.clearTimers();this.audio.pause();const version=++this.generation;
  this.sentence=s;this.part=p;this.offset=offset;this.phase='loading';this.intent=true;this.gap=null;this.update();
  try{const url=await this.prepare(s,p);if(version!==this.generation||!this.intent)return;
   this.audio.src=url;this.audio.playbackRate=this.rate;this.audio.preservesPitch=true;this.audio.currentTime=Math.max(0,Math.min(offset,this.segment.duration-.01));
   await this.audio.play();if(version!==this.generation)return;if(!this.intent){this.audio.pause();return;}
   this.phase='playing';this.log('part:playing');this.update();this.prefetch();this.tick();
  }catch(error){if(version!==this.generation)return;this.intent=false;this.phase='error';this.log('audio:error',{message:error.message});this.update();}
 }
 tick(){if(this.phase!=='playing'||!this.intent)return;this.update();this.raf=requestAnimationFrame(()=>this.tick());}
 playFrom(s,p=0,queue=[s]){this.stop();this.queue=[...queue];this.unlocked=true;this.loadAndPlay(s,p);}
 scheduleGap(){
  this.clearTimers();if(!this.gap||!this.intent)return;const duration=Math.max(0,this.gap.remaining),version=++this.generation;
  this.phase='gap';this.gap.deadline=performance.now()+duration;this.log('gap:start',{remainingMs:duration});this.update();
  this.prepare(this.gap.sentence,this.gap.part).catch(()=>{});
  this.timer=setTimeout(()=>{if(version!==this.generation||!this.intent||this.phase!=='gap')return;const next={...this.gap};this.log('gap:end');this.loadAndPlay(next.sentence,next.part);},duration);
 }
 pause(){
  if(!this.isActive)return;
  if(this.phase==='gap'){this.gap.remaining=Math.max(0,this.gap.deadline-performance.now());this.phase='pausedGap';}
  else{this.offset=this.phase==='playing'?this.audio.currentTime:this.offset;this.phase='paused';}
  this.intent=false;this.generation++;this.clearTimers();this.audio.pause();this.log('user:pause');this.update();
 }
 resume(){
  if(this.phase==='pausedGap'&&this.gap){this.intent=true;this.scheduleGap();}
  else if(this.phase==='paused'){this.intent=true;this.loadAndPlay(this.sentence,this.part,this.offset);}
  else this.playFrom(this.sentence,0,this.queue.length?this.queue:[this.sentence]);
 }
 stop(){this.intent=false;this.generation++;this.clearTimers();this.audio.pause();this.gap=null;this.offset=0;this.phase='idle';this.update();}
 seekFraction(fraction){
  if(!this.record)return;const target=Math.max(0,Math.min(.999999,Number(fraction)))*this.record.duration;
  const s=this.sentence,q=[...this.queue],wasActive=this.isActive;
  const p=Math.max(0,this.record.parts.findIndex(x=>target<x.sourceEnd));const offset=Math.max(0,target-this.record.parts[p].sourceStart);
  this.stop();this.sentence=s;this.part=p;this.offset=offset;this.queue=q;this.log('user:seek',{sourceTime:target});
  if(wasActive)this.loadAndPlay(s,p,offset);else{this.phase='paused';this.update();}
 }
 setRate(value){if(!(window.TEACHERS_READALONG_STANDARD?.speeds||[.25,.5,.75,1,1.25]).includes(Number(value)))return;this.rate=Number(value);this.audio.playbackRate=this.rate;this.audio.preservesPitch=true;this.update();}
}
window.TeacherPhrasePlayer=TeacherPhrasePlayer;
})();
