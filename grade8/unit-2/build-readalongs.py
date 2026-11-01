#!/usr/bin/env python3
"""Build Grade 8 Unit 2: recorded bilingual Read-Alongs using the shared engine.

Only lesson content, aligned timestamps and MP3 files are generated here.
The reusable playback/highlight/translation engine remains in shared/read-along/.
"""
import asyncio
import json
import math
import re
import subprocess
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"lesson-content.json").read_text(encoding="utf-8"))
VOICE="en-US-JennyNeural"
RATE="-10%"

def norm(s):
    return re.sub(r"[^a-z0-9]","",s.lower())

def duration(path):
    out=subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration",
         "-of","default=noprint_wrappers=1:nokey=1",str(path)],text=True)
    value=float(out.strip())
    if value<=0:raise RuntimeError(f"Invalid audio duration: {path}")
    return value

async def synthesize(text,path):
    last_error=None
    for attempt in range(4):
        try:
            chunks=[]
            edges=[]
            stream=edge_tts.Communicate(text,voice=VOICE,rate=RATE,boundary="WordBoundary")
            async for event in stream.stream():
                if event["type"]=="audio":
                    chunks.append(event["data"])
                elif event["type"]=="WordBoundary":
                    edges.append((str(event["text"]),float(event["offset"])/10000000))
            if not chunks:raise RuntimeError("No audio chunks from TTS")
            if len(edges)<2:raise RuntimeError("No precise WordBoundary events")
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(b"".join(chunks))
            return duration(path),edges
        except Exception as exc:
            last_error=exc
            if path.exists():path.unlink()
            await asyncio.sleep(1.5*(attempt+1))
    raise RuntimeError(f"TTS failed for {path}: {last_error}")

def timestamps(text,seconds,edges):
    matches=list(re.finditer(r"\S+",text))
    known=[None]*len(matches)
    pointer=0
    for i,match in enumerate(matches):
        token=norm(match.group())
        for j in range(pointer,min(len(edges),pointer+7)):
            if norm(edges[j][0])==token:
                known[i]=max(0,min(seconds-.08,edges[j][1]))
                pointer=j+1
                break
    number=sum(s is not None for s in known)
    # Neural speech spells numeric tokens as words (e.g. "23" becomes "twenty three").
    # Count those as expected unmatched tokens; retain the actually observed
    # boundaries for ordinary words and interpolate only the numeric span.
    numeric_tokens=sum(norm(m.group()).isdigit() for m in matches)
    if number+numeric_tokens<.72*len(matches) or number<max(2,len(matches)//2):
        raise RuntimeError(f"Word alignment not reliable: {number}/{len(matches)} tokens: {text}")
    for i in range(len(known)):
        if known[i] is not None:continue
        left=next((k for k in range(i-1,-1,-1) if known[k] is not None),None)
        right=next((k for k in range(i+1,len(known)) if known[k] is not None),None)
        if left is None and right is None:raise RuntimeError("No word boundaries")
        if left is None:
            known[i]=max(0,known[right]*(i+1)/(right+1))
        elif right is None:
            known[i]=known[left]+(seconds-known[left])*(i-left)/(len(known)-left)
        else:
            known[i]=known[left]+(known[right]-known[left])*(i-left)/(right-left)
    # Tiny corrections only; large differences should be caught by the coverage gate.
    starts=[]
    for i,s in enumerate(known):
        lo=starts[-1]+.003 if starts else 0
        starts.append(min(seconds-.005,max(lo,s)))
    tokens=[]
    for i,m in enumerate(matches):
        key=norm(m.group())
        gloss=DATA["glossary"].get(key)
        if not gloss:raise RuntimeError(f"Missing Hebrew gloss: {key!r}")
        finish=starts[i+1] if i+1<len(starts) else seconds
        tokens.append({"text":m.group(),"he":gloss,
                       "startChar":m.start(),"endChar":m.end(),
                       "start":round(starts[i],5),"end":round(finish,5)})
    return tokens

def alignment(en,he,tokens):
    hewords=list(re.finditer(r"\S+",he))
    units=[{"indices":[],"text":m.group(),"start":m.start(),"end":m.end()} for m in hewords]
    mapping=[]
    for j in range(len(tokens)):
        index=min(len(units)-1,int(j*len(units)/len(tokens)))
        mapping.append(index)
        units[index]["indices"].append(j)
    return {"plain":en,"he":he,"map":mapping,"units":units}

async def build(slug,source):
    directory=ROOT/slug
    directory.mkdir(exist_ok=True)
    stories=[]
    phrases=[]
    aligned={}
    pages=[]
    for paragraph,rows in enumerate(source["paragraphs"],start=1):
        ids=[]
        for en,he in rows:
            number=len(stories)+1
            path=directory/"audio"/f"story-{number:02d}.mp3"
            sec,edges=await synthesize(en,path)
            tokens=timestamps(en,sec,edges)
            stories.append({"number":number,"paragraph":paragraph,
                            "plain":en,"he":he,"tokens":tokens})
            phrases.append({"number":number,"duration":round(sec,5),
                "parts":[{"index":0,"firstToken":0,"lastToken":len(tokens)-1,
                          "startChar":0,"endChar":len(en),
                          "sourceStart":0,"sourceEnd":round(sec,5),
                          "duration":round(sec,5),"text":en,
                          "src":f"audio/story-{number:02d}.mp3"}]})
            aligned[str(number)]=alignment(en,he,tokens)
            ids.append(number-1)
            print(f"  {slug} sentence {number:02d}: {len(tokens)} timed words, {sec:.1f}s",flush=True)
            await asyncio.sleep(.15)
        pages.append(ids)
    js=lambda name,value:(directory/name).write_text(value,encoding="utf-8")
    js("unit-data.js","window.UNIT_DATA="+json.dumps({
        "story":stories,"pages":pages,"title":source["title"],
        "subtitle":source["subtitle"],"slug":slug
        },ensure_ascii=False,separators=(",",":"))+";\n")
    js("phrase-data.js","window.GRADE8_PHRASES="+json.dumps({
        "pauseMs":1500,"sentences":phrases
        },ensure_ascii=False,separators=(",",":"))+";\n")
    js("alignment.js","window.GRADE8_ALIGNMENT="+json.dumps(
        aligned,ensure_ascii=False,separators=(",",":"))+";\n")
    assert len(stories)==sum(len(p) for p in source["paragraphs"])
    assert len(phrases)==len(aligned)==len(stories)
    assert all(s["tokens"] and all(t["he"] and t["end"]>=t["start"] for t in s["tokens"]) for s in stories)
    print(f"{slug}: complete, {len(stories)} sentences, {sum(len(s['tokens']) for s in stories)} words",flush=True)

async def main():
    for slug,source in DATA["stories"].items():
        await build(slug,source)
    print("Two bilingual readers built successfully",flush=True)
if __name__=="__main__":
    asyncio.run(main())
