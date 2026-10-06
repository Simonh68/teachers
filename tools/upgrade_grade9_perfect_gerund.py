"""Upgrade the existing 46-sentence story and regenerate aligned narration."""
import json, re, subprocess, hashlib, html, asyncio, tempfile
from pathlib import Path
from bs4 import BeautifulSoup
R = Path(__file__).resolve().parents[1]
O = R/'grade9/unit-1/read-alone'
changes = {
 2: ("His class had already planned a book sale for a community library.", "כיתתו כבר תכננה מכירת ספרים למען ספרייה קהילתית.", "כיתתו|כיתה|כבר — עם had לציון עבר מושלם|כבר|תכננה|מכירת|ספרים|מכירה|למען|ספרייה|קהילתית|ספרייה"),
 9: ("Instead of asking for an explanation, he started writing an angry answer, then stopped.", "במקום לבקש הסבר, הוא התחיל לכתוב תשובה כועסת, ואז עצר.", "במקום|של — בצירוף instead of|לבקש|ל־|הסבר|הסבר|הוא|התחיל|לכתוב|תשובה|כועסת|תשובה|אז|עצר"),
 27: ("He and his father had finished making it late the night before.", "הוא ואביו סיימו להכין אותו בשעה מאוחרת בלילה הקודם.", "הוא|ו־|שלו|אבא|כבר — עם finished לציון עבר מושלם|סיימו|להכין|אותו|מאוחר|ה־|לילה|הקודם"),
 28: ("Suddenly, Noam understood why Eitan had answered so quickly.", "פתאום נועם הבין מדוע איתן ענה מהר כל כך קודם לכן.", "פתאום|נועם|הבין|מדוע|איתן|כבר — עם answered לציון עבר מושלם|ענה|כל כך|במהירות"),
 29: ("“I have never felt so embarrassed about assuming the worst,” Noam said.", "״מעולם לא הרגשתי נבוך כל כך בגלל ההנחה שהכול לרעה,״ אמר נועם.", "אני|עם felt לציון ניסיון עד עכשיו|מעולם לא|הרגשתי|כל כך|נבוך|בגלל|הנחת|ה־|הגרוע ביותר|נועם|אמר"),
 33: ("I have learned that explaining things clearly matters.”", "למדתי שחשוב להסביר דברים בצורה ברורה.״", "אני|עם learned לציון לקח התקף עכשיו|למדתי|ש־|להסביר|דברים|בבירור|חשוב"),
 40: ("“Helping your brother was important, and I appreciate your coming today,” Noam said.", "״העזרה לאחיך הייתה חשובה, ואני מעריך את זה שבאת היום,״ אמר נועם.", "לעזור|שלך|אח|הייתה|חשובה|ו־|אני|מעריך|שלך|ההגעה|היום|נועם|אמר"),
}
async def narrate(data):
 import edge_tts
 sem=asyncio.Semaphore(4)
 norm=lambda s:re.sub('[^a-z0-9]','',html.unescape(s).lower())
 with tempfile.TemporaryDirectory() as tmp:
  folder=Path(tmp)
  async def one(i,row):
   async with sem:
    p=folder/f'{i:02}.mp3';cues=[]
    for attempt in range(3):
     try:
      cues=[]
      with p.open('wb') as f:
       async for c in edge_tts.Communicate(row['en'],voice='en-US-BrianNeural',pitch='+10Hz',boundary='WordBoundary').stream():
        if c['type']=='audio':f.write(c['data'])
        elif c['type']=='WordBoundary':cues.append(dict(word=html.unescape(c['text']),start=c['offset']/1e7,end=(c['offset']+c['duration'])/1e7))
      assert cues
      break
     except Exception:
      if attempt==2:raise
      await asyncio.sleep(2)
    assert ''.join(norm(w['word']) for w in row['words'])==''.join(norm(c['word']) for c in cues)
    wav=folder/f'{i:02}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-ar','24000','-ac','1',str(wav)],check=True)
    import wave
    with wave.open(str(wav)) as w:duration=w.getnframes()/w.getframerate()
    spans=[];pos=0
    for c in cues:
     n=len(norm(c['word']));spans.append((pos,pos+n,c));pos+=n
    words=[];pos=0
    for w in row['words']:
     a=pos;b=a+len(norm(w['word']));pos=b;hits=[]
     for x,y,c in spans:
      l=max(a,x);r=min(b,y)
      if l<r:hits.append((c['start']+(c['end']-c['start'])*(l-x)/(y-x),c['start']+(c['end']-c['start'])*(r-x)/(y-x)))
     assert hits
     words.append(dict(word=w['word'],start=hits[0][0],end=hits[-1][1]))
    # The service occasionally emits a zero duration for a short pronoun.
    # Bound that word by the next measured onset, rather than distributing timings.
    for j,w in enumerate(words):
     if w['end']==w['start']:
      w['end']=words[j+1]['start'] if j+1<len(words) else duration
    assert duration>=words[-1]['end']-.15 and all(w['end']>w['start'] for w in words),(i+1,duration,words)
    print('Verified sentence',i+1,flush=True)
    return duration,words
  pieces=await asyncio.gather(*(one(i,r) for i,r in enumerate(data['sentences'])))
  import wave
  with wave.open(str(folder/'all.wav'),'wb') as out:
   out.setparams((1,2,24000,0,'NONE','not compressed'))
   for i in range(46):
    with wave.open(str(folder/f'{i:02}.wav')) as w:out.writeframes(w.readframes(w.getnframes()))
  dest=O/'assets/story.mp3'
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(folder/'all.wav'),'-codec:a','libmp3lame','-b:a','96k',str(dest)],check=True)
  rows=[];offset=0
  for row,(duration,words) in zip(data['sentences'],pieces):
   for w in words:w.update(start=round(w['start']+offset,5),end=round(w['end']+offset,5))
   rows.append(dict(id=row['id'],en=row['en'],start=words[0]['start'],end=words[-1]['end'],words=words));offset+=duration
  source_hash=hashlib.sha256(' '.join(r['en'] for r in data['sentences']).encode()).hexdigest()
  return dict(version='20261006-perfect-gerund',voice='en-US-BrianNeural',pitch='+10Hz',synthetic=True,timing='Measured WordBoundary timings per sentence; concatenated PCM sample offsets',source_sha256=source_hash,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),duration=offset,audio='assets/story.mp3?v='+source_hash[:12],word_count=sum(len(r['words']) for r in rows),sentences=rows)
def main():
 data=json.loads((O/'content.json').read_text())
 assert len(data['sentences'])==46
 # Preserve sentence IDs and paragraph/page relationships.
 for sid,(en,he,gloss) in changes.items():
  row=data['sentences'][sid-1]; row.update(en=en,he=he)
  toks=list(re.finditer(r"[A-Za-z]+(?:['’][A-Za-z]+)*|[0-9]+",en)); gs=gloss.split('|')
  assert len(toks)==len(gs),(sid,len(toks),len(gs))
  row['words']=[]; pos=0
  for m,g in zip(toks,gs):
   row['words'].append(dict(word=m.group(),he=g,prefix=en[pos:m.start()]));pos=m.end()
  row['suffix']=en[pos:]
  row['units']=[dict(en=w['word'],he=w['he'],first=i,last=i) for i,w in enumerate(row['words'])]
 # Update the reading page before the existing audio builder reads its source.
 path=R/'grade9/unit-1/reading.html'; soup=BeautifulSoup(path.read_text(),'html.parser')
 nodes=soup.select('.story .sentence'); assert len(nodes)==46
 for sid,(en,_,_) in changes.items():
  n=nodes[sid-1]; label=n.select_one('.sid').extract(); n.clear(); n.append(label);n.append(en)
 path.write_text(str(soup))
 audio=asyncio.run(narrate(data));idx=0
 for row,a in zip(data['sentences'],audio['sentences']):
  assert row['en']==a['en'] and len(row['words'])==len(a['words'])
  for w,t in zip(row['words'],a['words']):
   assert w['word'].lower()==t['word'].lower()
   w.update(start=t['start'],end=t['end'],index=idx);t['index']=idx;idx+=1
 data.update(version='20261006-perfect-gerund',wordCount=idx,source_sha256=audio['source_sha256'])
 (O/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (O/'audio.json').write_text(json.dumps(audio,ensure_ascii=False,indent=2)+'\n')
 # Keep the complete teaching deck and its translation slides in sync.
 path=R/'grade9/the-message-without-a-voice/index.html';soup=BeautifulSoup(path.read_text(),'html.parser')
 for node in soup.select('[data-ra-sentence]'):
  sid=int(node['data-ra-sentence'])+1
  target=node.select_one('.story-sentence')
  if target:
   target.clear()
   row=data['sentences'][sid-1]
   markup=''.join(html.escape(w['prefix'])+'<span class="ra-word ra-hit" role="button" tabindex="0" data-w="'+str(w['index'])+'" data-he="'+html.escape(w['he'],quote=True)+'">'+html.escape(w['word'])+'</span>' for w in row['words'])+html.escape(row['suffix'])
   target.append(BeautifulSoup(markup,'html.parser'))
  tr=node.select_one('.translation')
  if tr:tr.string=data['sentences'][sid-1]['he']
 path.write_text(str(soup))
 path=O/'index.html';s=path.read_text();s=re.sub(r'kind:"grade9",(?:assetVersion:"[^"]*",)*','kind:"grade9",assetVersion:"20261006-perfect-gerund",',s);path.write_text(s)
 assert hashlib.sha256((O/'assets/story.mp3').read_bytes()).hexdigest()==audio['sha256']
 report={'version':data['version'],'sentences':46,'updatedSentenceIds':list(changes),'words':idx,'audioSeconds':audio['duration'],'audioMatchesText':True,'grammar':['Past Perfect','Present Perfect','gerund after preposition','gerund as subject','gerund after finish/appreciate']}
 (O/'grammar-upgrade-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report),flush=True)
if __name__=='__main__':main()
