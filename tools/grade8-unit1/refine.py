"""Reproducible usability refinements after build.py, before acceptance tests."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'grade8/unit-1/index.html'
s=p.read_text()
s=s.replace("if(e.key==='Escape'){hideTip();stop();return}","if(e.key==='Escape'){if(!$('#tip').hidden)hideTip();else stop();return}")
# A tooltip contains text only: it must never intercept the next reading gesture.
s=s.replace('pointer-events:auto}#tip','pointer-events:none}#tip')
# Updating completion must not detach the checkbox while its click is processing.
old="if(e.target.dataset.tick.endsWith('-done')){let open=$$('.meeting[open]').map(x=>x.id);home();open.forEach(id=>{let el=document.getElementById(id);if(el)el.open=true})}"
new="if(e.target.dataset.tick.endsWith('-done')){const count=M.filter((_,i)=>state.ticks['m'+i+'-done']).length;const bar=$('#home progress');if(bar){bar.value=count;bar.previousElementSibling.textContent=count+' מתוך 5 מפגשים סומנו כבוצעו'}}"
assert old in s, 'Completion handler changed; review patch before publishing'
s=s.replace(old,new)
# Explicit touch-action avoids native browser cancellation before touchend.
# Long pages retain ordinary vertical scrolling and pinch zoom.
s=s.replace("$('#stage').innerHTML=html;remember();", "$('#stage').innerHTML=html;syncTouchMode();remember();")
start=s.index("const stage=$('#stage');stage.addEventListener('touchstart'")
end=s.index('let wheelAt=0;',start)
s=s[:start]+r"""const stage=$('#stage');
function syncTouchMode(){
 stage.style.touchAction=stage.scrollHeight>stage.clientHeight+4?'pan-y pinch-zoom':'none';
}
window.addEventListener('resize',syncTouchMode);
function finishSwipe(dx,dy){
 if(!touch||touch.done||Math.max(Math.abs(dx),Math.abs(dy))<45)return;
 const horizontal=Math.abs(dx)>Math.abs(dy);
 const canScroll=dy<0?stage.scrollHeight-stage.clientHeight-touch.top>4:touch.top>4;
 if(!horizontal&&canScroll)return;
 touch.done=true;hideTip();ignoreClickUntil=Date.now()+600;
 move((horizontal?dx:dy)<0?1:-1);
}
stage.addEventListener('touchstart',e=>{
 if(e.touches.length!==1){touch=null;return}
 const t=e.touches[0];touch={x:t.clientX,y:t.clientY,top:stage.scrollTop,done:false};
},{passive:true});
stage.addEventListener('touchmove',e=>{
 if(!touch||e.touches.length!==1)return;
 const t=e.touches[0],dx=t.clientX-touch.x,dy=t.clientY-touch.y;
 const horizontal=Math.abs(dx)>Math.abs(dy);
 if(horizontal&&Math.abs(dx)>8&&e.cancelable)e.preventDefault();
 finishSwipe(dx,dy);
},{passive:false});
stage.addEventListener('touchend',e=>{
 if(!touch)return;
 if(e.changedTouches.length){const t=e.changedTouches[0];finishSwipe(t.clientX-touch.x,t.clientY-touch.y)}
 if(touch&&touch.done){if(e.cancelable)e.preventDefault();ignoreClickUntil=Date.now()+600}
 touch=null;
},{passive:false});
stage.addEventListener('touchcancel',()=>{touch=null},{passive:true});
"""+s[end:]
p.write_text(s)
p=root/'grade8/index.html';s=p.read_text().replace('8.10.2026','22.10.2026').replace('כ״ז בתשרי תשפ״ז','י״א בחשוון תשפ״ז');p.write_text(s)
print('Refined stable progress controls, tooltip hit-testing and mobile touch navigation',flush=True)
