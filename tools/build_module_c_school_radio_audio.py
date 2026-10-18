"""Generate prerecorded US English MP3 files and real word cues. No runtime TTS."""
import asyncio, hashlib, html, json, os, re, subprocess
from pathlib import Path
import edge_tts
import edge_tts.communicate as speech
if os.environ.get('SSL_CERT_FILE'):
    speech._SSL_CTX.load_verify_locations(os.environ['SSL_CERT_FILE'])
ROOT=Path(__file__).resolve().parents[1]/'grade12/four-units/module-c-school-radio'
AUDIO=ROOT/'audio';AUDIO.mkdir(exist_ok=True)
DATA=json.loads((ROOT/'content.json').read_text())
PHRASES=json.loads((ROOT/'reading-phrases.json').read_text())
def norm(s):return re.sub('[^a-z0-9]','',html.unescape(s).lower())
async def main():
    records=[];global_word=0
    for i,paragraph in enumerate(DATA['paragraphs'],1):
        target=AUDIO/f'paragraph-{i}.mp3';cues=[]
        async for event in edge_tts.Communicate(paragraph,voice='en-US-AriaNeural',boundary='WordBoundary').stream():
            if event['type']=='audio':
                with target.open('ab' if cues or target.exists() else 'wb') as f:f.write(event['data'])
            elif event['type']=='WordBoundary':cues.append({'text':html.unescape(event['text']),'start':event['offset']/1e7,'end':(event['offset']+event['duration'])/1e7})
        assert norm(paragraph)==norm(' '.join(c['text'] for c in cues)),f'Paragraph {i}: spoken word alignment mismatch'
        spans=[];pos=0
        for c in cues:
            end=pos+len(norm(c['text']));spans.append((pos,end,c));pos=end
        pos=0;words=[]
        for token in paragraph.split():
            a=pos;b=a+len(norm(token));pos=b;matches=[]
            for x,y,c in spans:
                lo,hi=max(a,x),min(b,y)
                if lo<hi:
                    duration=c['end']-c['start'];matches.append((c['start']+duration*(lo-x)/(y-x),c['start']+duration*(hi-x)/(y-x)))
            assert matches,(i,token)
            words.append({'id':global_word,'text':token,'start':round(matches[0][0],4),'end':round(matches[-1][1],4)});global_word+=1
        subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(target)],text=True))
        assert 0<words[-1]['end']<=duration+.1
        records.append({'paragraph':i,'src':f'audio/paragraph-{i}.mp3','sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'duration':duration,'words':words,'phrases':[p for p in PHRASES if p['paragraph']==i]})
        print(f'Paragraph {i}: {len(words)} aligned words, {duration:.1f} seconds, {target.stat().st_size} bytes',flush=True)
    (ROOT/'audio.json').write_text(json.dumps({'voice':'en-US-AriaNeural','kind':'prerecorded','paragraphs':records},ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
    # A rebuild must never append new audio to an old recording.
    for i in range(1,len(DATA['paragraphs'])+1):(AUDIO/f'paragraph-{i}.mp3').unlink(missing_ok=True)
    asyncio.run(main())
