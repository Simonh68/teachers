import asyncio,os,json,re,html,hashlib,subprocess
from pathlib import Path
import edge_tts,edge_tts.communicate as c
if os.environ.get('SSL_CERT_FILE'): c._SSL_CTX.load_verify_locations(os.environ['SSL_CERT_FILE'])
root=Path(__file__).resolve().parents[1]/'grade12/four-units/module-e-food-sharing'
d=json.loads((root/'pilot.json').read_text()); texts=[p['text'] for p in d['paragraphs']]+[q['stem'] for q in d['questions']]
def norm(s): return re.sub('[^a-z0-9]','',html.unescape(s).lower())
async def main():
 cues=[]
 with (root/'audio/narration.mp3').open('wb') as f:
  async for m in edge_tts.Communicate(' '.join(texts),voice='en-US-AriaNeural',boundary='WordBoundary').stream():
   if m['type']=='audio': f.write(m['data'])
   elif m['type']=='WordBoundary': cues.append({'word':html.unescape(m['text']),'start':m['offset']/1e7,'end':(m['offset']+m['duration'])/1e7})
 assert norm(' '.join(texts))==norm(' '.join(c['word'] for c in cues)), 'word alignment mismatch'
 spans=[]; pos=0
 for c in cues:
  end=pos+len(norm(c['word']));spans.append((pos,end,c));pos=end
 pos=0;rows=[];last=0
 for text in texts:
  ws=[]
  for token in text.split():
   a=pos;b=a+len(norm(token));pos=b
   matches=[]
   for x,y,c in spans:
    l=max(a,x);r=min(b,y)
    if l<r:
     dur=c['end']-c['start'];matches.append((c['start']+dur*(l-x)/(y-x),c['start']+dur*(r-x)/(y-x)))
   start,end=(matches[0][0],matches[-1][1]) if matches else (last,last)
   ws.append({'start':round(start,4),'end':round(end,4)});last=end
  rows.append(ws)
 subprocess.run(['ffmpeg','-v','error','-i',str(root/'audio/narration.mp3'),'-f','null','-'],check=True)
 sha=hashlib.sha256((root/'audio/narration.mp3').read_bytes()).hexdigest()
 out={'src':'audio/narration.mp3?v='+sha[:12],'voice':'en-US-AriaNeural','paragraphs':rows[:5],'questions':rows[5:]}
 (root/'audio.js').write_text('window.E_AUDIO='+json.dumps(out,separators=(',',':'))+';\n')
 print('Verified narration:',len(cues),'word cues;',len(rows),'text sections;', (root/'audio/narration.mp3').stat().st_size,'bytes',flush=True)
asyncio.run(main())
