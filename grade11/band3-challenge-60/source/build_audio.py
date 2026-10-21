"""Generate 120 independent prerecorded MP3s. Requires edge-tts and ffmpeg."""
import asyncio,hashlib,json,os,re,subprocess,html
from pathlib import Path
import edge_tts
import edge_tts.communicate as speech
if os.environ.get('SSL_CERT_FILE'):speech._SSL_CTX.load_verify_locations(os.environ['SSL_CERT_FILE'])
ROOT=Path(__file__).resolve().parents[1]
VOICE='en-US-AriaNeural'
entries=json.loads((ROOT/'entries.json').read_text())
sem=asyncio.Semaphore(4)
def norm(t):return re.sub(r'[^a-z0-9]','',html.unescape(t).lower())
async def make(e,kind):
 text=e['en'].replace(' sth',' something') if kind=='word' else e['ex_en']
 path=ROOT/'audio'/f"{e['number']:02d}-{kind}.mp3"
 async with sem:
  cues=[]
  for attempt in range(4):
   try:
    temp=path.with_suffix('.tmp');temp.unlink(missing_ok=True)
    with temp.open('wb') as f:
     async for part in edge_tts.Communicate(text,voice=VOICE,rate='-10%',boundary='WordBoundary').stream():
      if part['type']=='audio':f.write(part['data'])
      elif part['type']=='WordBoundary':cues.append(html.unescape(part['text']))
    assert norm(text)==norm(' '.join(cues)),(text,cues)
    subprocess.run(['ffmpeg','-v','error','-i',str(temp),'-f','null','-'],check=True)
    temp.rename(path);break
   except Exception:
    if attempt==3:raise
    cues=[];await asyncio.sleep(1+attempt)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True))
  print(f"{e['number']:02d} {kind} OK {duration:.2f}s",flush=True)
  return {'entry':e['source_entry_id'],'number':e['number'],'kind':kind,'text':text,'src':str(path.relative_to(ROOT)),'duration':duration,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'spoken_words':cues}
async def main():
 results=await asyncio.gather(*(make(e,kind) for e in entries for kind in ['word','sentence']))
 (ROOT/'audio-manifest.json').write_text(json.dumps({'voice':VOICE,'rate':'-10%','prerecorded':True,'clips':results},ensure_ascii=False,indent=2)+'\n')
 print('COMPLETE',len(results),flush=True)
asyncio.run(main())
