"""Prerecorded Brian voice and engine word boundaries. pip install edge-tts==7.2.8."""
import asyncio,html,json,os,re,hashlib
from pathlib import Path
import edge_tts,edge_tts.communicate
R=Path(__file__).resolve().parents[2]/'grade7/unit-1/reading'
def norm(x):return re.sub(r'[^a-z0-9]', '',html.unescape(x).lower())
async def main():
 if os.environ.get('CODEX_PROXY_CERT'):edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ['CODEX_PROXY_CERT'])
 data=json.loads((R/'content.json').read_text());text=' '.join(s['en'] for s in data['sentences']);cues=[]
 dest=R/'assets/narration.mp3'
 comm=edge_tts.Communicate(text,voice='en-US-BrianNeural',pitch='+10Hz',boundary='WordBoundary',proxy=os.environ.get('HTTPS_PROXY'))
 with dest.open('wb') as f:
  async for c in comm.stream():
   if c['type']=='audio':f.write(c['data'])
   if c['type']=='WordBoundary':cues.append(dict(word=html.unescape(c['text']),start=c['offset']/1e7,end=(c['offset']+c['duration'])/1e7))
 tokens=text.split()
 # Edge occasionally returns one boundary for two adjacent written tokens.
 # Align on the normalized character stream and split only that boundary's
 # measured duration between the affected display words.
 token_norm=[norm(t) for t in tokens];cue_norm=[norm(c['word']) for c in cues]
 assert ''.join(token_norm)==''.join(cue_norm),(token_norm,cue_norm)
 token_spans=[];pos=0
 for t,n in zip(tokens,token_norm):
  token_spans.append((pos,pos+len(n),t));pos+=len(n)
 cue_spans=[];pos=0
 for c,n in zip(cues,cue_norm):
  cue_spans.append((pos,pos+len(n),c));pos+=len(n)
 aligned=[]
 for a,b,t in token_spans:
  parts=[]
  for x,y,c in cue_spans:
   left=max(a,x);right=min(b,y)
   if left>=right:continue
   duration=c['end']-c['start']
   parts.append((c['start']+duration*(left-x)/(y-x),c['start']+duration*(right-x)/(y-x)))
  assert parts,t
  aligned.append(dict(word=t,start=parts[0][0],end=parts[-1][1]))
 cues=aligned
 clips=[];cursor=0
 for s in data['sentences']:
  w=cues[cursor:cursor+len(s['words'])];cursor+=len(w);clips.append(dict(start=w[0]['start'],end=w[-1]['end'],words=w))
 out=dict(audio='assets/narration.mp3?v=unit-1-v2',voice='en-US-BrianNeural',pitch='+10Hz',synthetic=True,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),sentences=clips)
 (R/'audio.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Recorded',len(clips),'sentences;',len(cues),'words;',dest.stat().st_size,'bytes',flush=True)
asyncio.run(main())
