"""Generate hosted American English audio; learner browsers never call TTS.

Uses Microsoft Edge TTS with engine word boundaries. Vocabulary source texts
are public curriculum material; reading texts are in the saved project draft.
Run --vocabulary or --reading after their canonical data has been built.
"""
import asyncio,hashlib,html,json,os,re,sys
from pathlib import Path
import edge_tts,edge_tts.communicate
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade7/unit-2'
VOICE='en-US-BrianNeural'
def norm(s):return re.sub(r'[^a-z0-9]','',html.unescape(s).lower())
def align(text,cues):
    tokens=text.split();tn=[norm(t) for t in tokens];cn=[norm(c['word']) for c in cues]
    assert ''.join(tn)==''.join(cn),('Boundary mismatch',tokens,cues)
    cs=[];pos=0
    for n,c in zip(cn,cues):cs.append((pos,pos+len(n),c));pos+=len(n)
    result=[];pos=0
    for token,n in zip(tokens,tn):
        a,b=pos,pos+len(n);parts=[]
        for x,y,c in cs:
            lo,hi=max(a,x),min(b,y)
            if hi>lo:
                d=c['end']-c['start'];parts.append((c['start']+d*(lo-x)/(y-x),c['start']+d*(hi-x)/(y-x)))
        assert parts,token
        result.append(dict(word=token,start=parts[0][0],end=parts[-1][1]));pos=b
    return result
async def record(text,dest):
    digest=hashlib.sha256((VOICE+'|+10Hz|'+text).encode()).hexdigest();cuefile=dest.with_suffix('.cues.json')
    if dest.exists() and cuefile.exists():
        cached=json.loads(cuefile.read_text())
        if cached['sha256Text']==digest:return cached
    dest.parent.mkdir(parents=True,exist_ok=True)
    for attempt in range(3):
        try:
            cues=[];comm=edge_tts.Communicate(text,voice=VOICE,pitch='+10Hz',boundary='WordBoundary',proxy=os.environ.get('HTTPS_PROXY'))
            with dest.with_suffix('.part').open('wb') as f:
                async for c in comm.stream():
                    if c['type']=='audio':f.write(c['data'])
                    elif c['type']=='WordBoundary':cues.append(dict(word=html.unescape(c['text']),start=c['offset']/1e7,end=(c['offset']+c['duration'])/1e7))
            assert dest.with_suffix('.part').stat().st_size>1000
            words=align(text,cues);dest.with_suffix('.part').replace(dest)
            result=dict(text=text,voice=VOICE,pitch='+10Hz',synthetic=True,sha256Text=digest,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),words=words,bytes=dest.stat().st_size)
            cuefile.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');return result
        except Exception:
            if attempt==2:raise
            await asyncio.sleep(1+attempt)
async def main():
    if os.environ.get('CODEX_PROXY_CERT'):edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ['CODEX_PROXY_CERT'])
    if '--vocabulary' in sys.argv:
        records=json.loads((OUT/'vocabulary/entries.json').read_text());manifest=dict(voice=VOICE,synthetic=True,browserSpeechSynthesis=False,files={})
        limit=asyncio.Semaphore(4)
        async def one(r):
            async with limit:
                text=r['en'].rstrip('.!?')+'. '+r['ex_en'];target=OUT/'vocabulary/audio'/(r['id']+'.mp3')
                a=await record(text,target);manifest['files'][r['id']]={k:a[k] for k in ['text','sha256Text','sha256','bytes']};manifest['files'][r['id']].update(src='audio/'+target.name,seconds=a['words'][-1]['end'])
                (OUT/'vocabulary/audio/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
                print('Vocabulary',len(manifest['files']),'/165',r['id'],flush=True)
        await asyncio.gather(*(one(r) for r in records))
        (OUT/'vocabulary/audio-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    if '--reading' in sys.argv:
        data=json.loads((OUT/'reading/content.json').read_text())
        for text in data['texts']:
            ss=[data['sentences'][n] for n in text['ids']];en=' '.join(s['en'] for s in ss)
            target=OUT/'reading/assets'/(text['id']+'.mp3');a=await record(en,target);cursor=0
            for s in ss:
                words=a['words'][cursor:cursor+len(s['words'])];cursor+=len(words);s['audio']='assets/'+target.name;s['start']=words[0]['start'];s['end']=words[-1]['end'];s['timings']=words
            text['audio']='assets/'+target.name;text['sha256']=a['sha256'];print('Reading',text['id'],len(ss),'sentences',flush=True)
        (OUT/'reading/content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        (OUT/'reading/data.js').write_text('window.READING = '+json.dumps(data,ensure_ascii=False)+';\n')
asyncio.run(main())
