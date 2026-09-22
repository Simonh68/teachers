"""Generate recorded English narration; never use browser speech.
Only the already-public story is sent to Microsoft's speech service.
The source text and punctuation are retained in the manifest.
"""
import asyncio, hashlib, html, json, re, subprocess, os
from pathlib import Path
from bs4 import BeautifulSoup
import edge_tts
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'grade9/unit-1/read-alone'
WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*|[0-9]+")
def norm(x): return re.sub('[^a-z0-9]', '', html.unescape(x).lower())
def source():
    soup = BeautifulSoup((ROOT/'grade9/unit-1/reading.html').read_text(), 'html.parser')
    rows=[]
    for node in soup.select('.story .sentence'):
        sid=node.select_one('.sid'); sid.extract()
        rows.append(node.get_text().strip())
    assert len(rows)==46, f'Expected 46 original sentences; got {len(rows)}'
    return rows
async def main():
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'assets').mkdir(exist_ok=True)
    sentences=source(); text=' '.join(sentences)
    source_hash=hashlib.sha256(text.encode()).hexdigest()
    dest=OUT/'assets/story.mp3'; meta=OUT/'audio.json'
    if dest.exists() and meta.exists():
        old=json.loads(meta.read_text())
        if old.get('source_sha256')==source_hash and old.get('sha256')==hashlib.sha256(dest.read_bytes()).hexdigest():
            print('Reuse verified complete narration',len(old['sentences']),flush=True); return
    cues=[]; tmp=dest.with_suffix('.tmp.mp3')
    for attempt in range(3):
        cues=[]
        try:
            comm=edge_tts.Communicate(text, voice='en-US-BrianNeural', pitch='+10Hz', boundary='WordBoundary')
            with tmp.open('wb') as f:
                async for c in comm.stream():
                    if c['type']=='audio': f.write(c['data'])
                    elif c['type']=='WordBoundary': cues.append({'word':html.unescape(c['text']),'start':c['offset']/1e7,'end':(c['offset']+c['duration'])/1e7})
            assert cues and tmp.stat().st_size>10000
            break
        except Exception as e:
            print('Speech attempt',attempt+1,type(e).__name__,str(e)[:240],flush=True)
            if attempt==2: raise
            await asyncio.sleep(3*(attempt+1))
    tokens=[m.group() for s in sentences for m in WORD.finditer(s)]
    assert ''.join(map(norm,tokens))==''.join(norm(c['word']) for c in cues), 'Narration/source alignment mismatch'
    spans=[]; p=0
    for c in cues:
        size=len(norm(c['word'])); spans.append((p,p+size,c)); p+=size
    aligned=[]; p=0
    for word in tokens:
        a=p; b=p+len(norm(word)); p=b; matches=[]
        for x,y,c in spans:
            l=max(a,x); r=min(b,y)
            if l<r:
                d=c['end']-c['start']; matches.append((c['start']+d*(l-x)/(y-x),c['start']+d*(r-x)/(y-x)))
        assert matches,word
        aligned.append({'word':word,'start':round(matches[0][0],5),'end':round(matches[-1][1],5)})
    rows=[]; k=0
    for i,s in enumerate(sentences):
        count=len(list(WORD.finditer(s))); w=aligned[k:k+count]; k+=count
        rows.append({'id':i+1,'en':s,'start':w[0]['start'],'end':w[-1]['end'],'words':w})
    subprocess.run(['ffmpeg','-v','error','-i',str(tmp),'-f','null','-'],check=True)
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(tmp)],text=True).strip())
    assert duration>=aligned[-1]['end']-.15 and all(w['end']>w['start'] for w in aligned)
    tmp.replace(dest)
    result={'version':'g9-read-alone-20260922','voice':'en-US-BrianNeural','pitch':'+10Hz','synthetic':True,'timing':'Microsoft WordBoundary with normalized character alignment for compound boundaries; not evenly timed','source_sha256':source_hash,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'duration':duration,'audio':'assets/story.mp3?v='+source_hash[:12],'word_count':len(aligned),'sentences':rows}
    meta.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Verified',len(rows),'sentences',len(aligned),'timed words',duration,'seconds',dest.stat().st_size,'bytes',flush=True)
if __name__=='__main__': asyncio.run(main())
