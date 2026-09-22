"""Reproducible usability refinements after build.py, before acceptance tests."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'grade8/unit-1/index.html'
s=p.read_text()
s=s.replace("if(e.key==='Escape'){hideTip();stop();return}","if(e.key==='Escape'){if(!$('#tip').hidden)hideTip();else stop();return}")
# Claim a navigation gesture on touchmove, before the browser cancels it as
# scrolling/selection. Ordinary vertical scrolling remains native when needed.
start=s.index("const stage=$('#stage');stage.addEventListener('touchstart'")
end=s.index('let wheelAt=0;',start)
s=s[:start]+r"""const stage=$('#stage');
stage.style.touchAction='auto';
stage.addEventListener('touchstart',e=>{
 if(e.touches.length!==1){touch=null;return}
 const t=e.touches[0];touch={x:t.clientX,y:t.clientY,top:stage.scrollTop,claimed:false,done:false};
},{passive:true});
stage.addEventListener('touchmove',e=>{
 if(!touch||e.touches.length!==1)return;
 const t=e.touches[0],dx=t.clientX-touch.x,dy=t.clientY-touch.y;
 if(Math.max(Math.abs(dx),Math.abs(dy))<8)return;
 const horizontal=Math.abs(dx)>Math.abs(dy);
 const canScroll=dy<0?stage.scrollHeight-stage.clientHeight-touch.top>4:touch.top>4;
 if(!horizontal&&canScroll&&!touch.claimed){touch=null;return}
 touch.claimed=true;
 if(e.cancelable)e.preventDefault();
 hideTip();ignoreClickUntil=Date.now()+600;
 if(!touch.done&&Math.max(Math.abs(dx),Math.abs(dy))>=45){
  touch.done=true;move((horizontal?dx:dy)<0?1:-1);
 }
},{passive:false});
stage.addEventListener('touchend',e=>{
 if(touch&&touch.claimed){if(e.cancelable)e.preventDefault();ignoreClickUntil=Date.now()+600}
 touch=null;
},{passive:false});
stage.addEventListener('touchcancel',()=>{touch=null},{passive:true});
"""+s[end:]
p.write_text(s)
p=root/'grade8/index.html'
s=p.read_text().replace('8.10.2026','22.10.2026').replace('כ״ז בתשרי תשפ״ז','י״א בחשוון תשפ״ז')
p.write_text(s)
print('Refined touch navigation, tooltip dismissal and class-card exam date',flush=True)
