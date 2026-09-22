"""Small reproducible refinements after build.py and before acceptance tests."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'grade8/unit-1/index.html'
s=p.read_text()
s=s.replace("if(e.key==='Escape'){hideTip();stop();return}","if(e.key==='Escape'){if(!$('#tip').hidden)hideTip();else stop();return}")
# Remember only the position, never a claim that reading equals mastery.
s=s.replace("function mark(){state.read['page'+pos]=true;save();renderTabs()}","function mark(){state.read['page'+pos]=true;save();renderTabs()}")
p.write_text(s)
p=root/'grade8/index.html';s=p.read_text().replace('8.10.2026','22.10.2026').replace('כ״ז בתשרי תשפ״ז','י״א בחשוון תשפ״ז');p.write_text(s)
print('Refined tooltip dismissal and class-card exam date',flush=True)
