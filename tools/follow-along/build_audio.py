"""Build full-story narration without changing the canonical story text.
Install edge-tts==7.2.8. Run: python tools/follow-along/build_audio.py
Audio is generated during authoring; browsers only play the hosted MP3.
"""
import asyncio,hashlib,html,json,os,re
from pathlib import Path
import edge_tts,edge_tts.communicate
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade7/follow-along'
SOURCE=ROOT/'grade7/the-same-way/story.json'
VOICE='en-US-AnaNeural' # Synthetic child voice, not an adult narrator.
PAGE_GROUPS=[[0,1],[2,3],[4,5,6],[7,8,9],[10,11,12],[13,14],[15,16,17],[18,19,20],[21,22,23],[24,25,26,27]]
PAGE_TITLES=['בית ספר חדש','יוצאים מהבית','אוטובוסים ורכבת','שני בנים בדרך','מה יהיה בחורף?','הטלפון נשאר שקט','הפתעה בכיתה','גם אתם עייפים?','אותן תחושות','מחר נגיד שלום']
IMAGE_KEYS=['departure','departure','journey','journey','winter','winter','classroom','friends','friends','friends']
def norm(s):
 s=re.sub(r'[^a-z0-9]','',html.unescape(s).lower())
 return '7' if s=='seven' else s
async def main():
 if os.environ.get('CODEX_PROXY_CERT'):edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ['CODEX_PROXY_CERT'])
 source=json.loads(SOURCE.read_text());units=json.loads((OUT/'units.json').read_text())
 text=' '.join(source['paragraphs']);assert text==' '.join(s['en'] for s in source['sentences'])
 for s,u in zip(source['sentences'],units,strict=True):assert ' '.join(g[0] for g in u)==s['en'],s
 c=edge_tts.Communicate(text,voice=VOICE,rate='+0%',boundary='WordBoundary',proxy=os.environ.get('HTTPS_PROXY'))
 cues=[];dest=OUT/'assets/narration-full.mp3'
 with dest.open('wb') as f:
  async for x in c.stream():
   if x['type']=='audio':f.write(x['data'])
   elif x['type']=='WordBoundary':cues.append({'word':html.unescape(x['text']),'start':round(x['offset']/1e7,4),'end':round((x['offset']+x['duration'])/1e7,4)})
 tokens=text.split();assert len(cues)==len(tokens),(len(cues),len(tokens))
 for cue,token in zip(cues,tokens):
  assert norm(cue['word'])==norm(token),(cue,token)
  cue['word']=token
 sentences=[];cursor=0
 for i,s in enumerate(source['sentences']):
  count=len(s['en'].split());words=cues[cursor:cursor+count];cursor+=count
  sentences.append({'text':s['en'],'translation':s['he'],'sourceParagraph':s['part'],'paragraph':next(p for p,g in enumerate(PAGE_GROUPS) if i in g),'start':words[0]['start'],'end':words[-1]['end'],'words':words,'units':[{'text':en,'translation':he} for en,he in units[i]]})
 data={'title':source['title'],'audio':'assets/narration-full.mp3','voice':VOICE,'rate':'+0%','synthetic':True,'voiceDescription':'Synthetic child voice, American English','timing':'Engine word boundaries on the audio timeline, seconds','wordCount':len(tokens),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':'../the-same-way/story.json','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'pages':[{'title':title,'image':'assets/'+image+'.webp'} for title,image in zip(PAGE_TITLES,IMAGE_KEYS)],'sentences':sentences}
 (OUT/'reading.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'words':len(tokens),'sentences':len(sentences),'pages':len(PAGE_GROUPS),'lastCue':cues[-1]['end'],'audioBytes':dest.stat().st_size}),flush=True)
if __name__=='__main__':asyncio.run(main())
