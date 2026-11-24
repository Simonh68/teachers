"""Create prerecorded vocabulary word + listening pause + example clips."""
import argparse
import asyncio
import hashlib
import html
import json
import os
import re
import subprocess
from pathlib import Path

import edge_tts
import edge_tts.communicate as speech

if os.environ.get('SSL_CERT_FILE'):
    speech._SSL_CTX.load_verify_locations(os.environ['SSL_CERT_FILE'])

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parent.parent/'stern_work/lesson_support.json')
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'vocabulary')
args = parser.parse_args()
OUT = args.output
OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT/'parts'
CACHE.mkdir(exist_ok=True)
VOICE = 'en-US-BrianNeural'
RATE = '-5%'

def norm(s):
    return re.sub('[^a-z0-9]', '', html.unescape(s).lower())

async def part(text, name, semaphore):
    path = CACHE/(name+'.mp3')
    meta = CACHE/(name+'.json')
    fingerprint = hashlib.sha256((VOICE+'\n'+RATE+'\n'+text).encode()).hexdigest()
    if path.exists() and meta.exists():
        m = json.loads(meta.read_text())
        if m['source_sha256'] == fingerprint and m['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest():
            return path
    async with semaphore:
        for attempt in range(3):
            chunks = []
            cues = []
            try:
                async for event in edge_tts.Communicate(text, voice=VOICE, rate=RATE, boundary='WordBoundary').stream():
                    if event['type'] == 'audio':
                        chunks.append(event['data'])
                    elif event['type'] == 'WordBoundary':
                        cues.append(html.unescape(event['text']))
                assert norm(text) == norm(' '.join(cues)), (name, text, cues)
                audio = b''.join(chunks)
                assert len(audio) > 1000
                path.write_bytes(audio)
                meta.write_text(json.dumps({'text':text,'voice':VOICE,'rate':RATE,'source_sha256':fingerprint,
                                           'sha256':hashlib.sha256(audio).hexdigest(),'spoken_tokens':cues},indent=2)+'\n')
                return path
            except Exception as error:
                print(f'{name} attempt {attempt+1}: {type(error).__name__}: {str(error)[:120]}',flush=True)
                if attempt == 2:
                    raise
                await asyncio.sleep(attempt+1)

async def card(chapter, index, item, semaphore):
    stem = f'vocab-{chapter}-{index}'
    a,b = await asyncio.gather(part(item['word'], stem+'-word', semaphore),
                               part(item['exampleEnglish'], stem+'-example', semaphore))
    target = OUT/(stem+'.mp3')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(a),'-i',str(b),
                    '-filter_complex','[0:a]apad=pad_dur=0.55[w];[w][1:a]concat=n=2:v=0:a=1[a]',
                    '-map','[a]','-ar','24000','-ac','1','-codec:a','libmp3lame','-b:a','64k',str(target)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration',
                   '-of','default=noprint_wrappers=1:nokey=1',str(target)],text=True))
    row={'chapter':chapter,'index':index,'word':item['word'],'exampleEnglish':item['exampleEnglish'],
         'src':'audio/vocabulary/'+target.name,'duration':duration,
         'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    print(f'{stem}: {item["word"]}, {duration:.2f}s, {target.stat().st_size} bytes',flush=True)
    return row

async def main():
    data=json.loads(args.source.read_text())
    semaphore=asyncio.Semaphore(3)
    jobs=[card(ch['id'],i,v,semaphore) for ch in data['chapters'] for i,v in enumerate(ch['vocabulary'],1)]
    rows=await asyncio.gather(*jobs)
    assert len(rows)==24
    (OUT/'manifest.json').write_text(json.dumps({'voice':VOICE,'rate':RATE,'synthetic':True,
        'pause_seconds':0.55,'source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),'clips':rows},ensure_ascii=False,indent=2)+'\n')
    print('COMPLETE',len(rows),'vocabulary cards',flush=True)

if __name__=='__main__':
    asyncio.run(main())
