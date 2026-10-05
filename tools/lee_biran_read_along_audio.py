"""Generate prerecorded narration + word timings for the standalone Lee Birron Read Along."""
import asyncio, hashlib, html, json, re, subprocess
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'standalone/lee-biran-read-along'
WORD=re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*|[0-9]+")
def norm(x): return re.sub('[^a-z0-9]','',html.unescape(x).lower())

async def main():
    data=json.loads((OUT/'content.json').read_text())
    sentences=[s['en'] for s in data['sentences']]
    spoken_sentences=[s.replace('Lee Birron','Lee Biran').replace('Birron','Biran') for s in sentences]
    text=' '.join(spoken_sentences)
    source_hash=hashlib.sha256(text.encode()).hexdigest()
    (OUT/'assets').mkdir(parents=True,exist_ok=True)
    dest=OUT/'assets/story.mp3'; meta=OUT/'audio.json'; tmp=OUT/'assets/story.tmp.mp3'
    cues=[]
    comm=edge_tts.Communicate(text,voice='en-US-BrianNeural',pitch='+10Hz',boundary='WordBoundary')
    with tmp.open('wb') as f:
        async for c in comm.stream():
            if c['type']=='audio': f.write(c['data'])
            elif c['type']=='WordBoundary':
                cues.append({'word':html.unescape(c['text']),'start':c['offset']/1e7,'end':(c['offset']+c['duration'])/1e7})
    tokens=[m.group() for s in sentences for m in WORD.finditer(s)]
    spoken_tokens=[m.group() for s in spoken_sentences for m in WORD.finditer(s)]
    assert len(tokens)==len(spoken_tokens), 'Display/spoken token count mismatch'
    assert ''.join(map(norm,spoken_tokens))==''.join(norm(c['word']) for c in cues)
    spans=[];p=0
    for c in cues:
        n=len(norm(c['word']));spans.append((p,p+n,c));p+=n
    aligned=[];p=0
    for word,spoken_word in zip(tokens,spoken_tokens):
        a=p;b=p+len(norm(spoken_word));p=b;matches=[]
        for x,y,c in spans:
            l=max(a,x);r=min(b,y)
            if l<r:
                d=c['end']-c['start']
                matches.append((c['start']+d*(l-x)/(y-x),c['start']+d*(r-x)/(y-x)))
        assert matches,word
        aligned.append({'word':word,'start':round(matches[0][0],5),'end':round(matches[-1][1],5)})
    rows=[];k=0
    for i,s in enumerate(sentences):
        count=len(list(WORD.finditer(s)));w=aligned[k:k+count];k+=count
        assert len(data['sentences'][i]['words'])==count
        rows.append({'id':i+1,'en':s,'start':w[0]['start'],'end':w[-1]['end'],'words':w})
    subprocess.run(['ffmpeg','-v','error','-i',str(tmp),'-f','null','-'],check=True)
    tmp.replace(dest)
    result={'version':'20261005-lee-biran-ra1','voice':'en-US-BrianNeural','pitch':'+10Hz','synthetic':True,'source_sha256':source_hash,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'audio':'assets/story.mp3?v='+source_hash[:12],'word_count':len(aligned),'sentences':rows}
    meta.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('generated',len(rows),'sentences',len(aligned),'words')

if __name__=='__main__':
    asyncio.run(main())
