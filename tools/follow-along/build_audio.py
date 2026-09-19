"""Pre-generate narration and word timing cues; never run TTS in the browser.
Install: pip install edge-tts==7.2.8
Run from any directory: python tools/follow-along/build_audio.py
"""
import asyncio, hashlib, html, json, os, re
from pathlib import Path
import edge_tts
import edge_tts.communicate
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'grade7/follow-along'
VOICE = 'en-US-GuyNeural'
SENTENCES = [
    ('My name is Dan, and I am in Grade seven.', 'קוראים לי דן, ואני בכיתה ז׳.', 0),
    ('My new school is far from home.', 'בית הספר החדש שלי רחוק מהבית.', 0),
    ('Every morning, I walk, take a bus, and then take a train.', 'בכל בוקר אני הולך ברגל, נוסע באוטובוס ואז נוסע ברכבת.', 0),
    ('Two boys are on the train too.', 'גם שני ילדים נמצאים ברכבת.', 1),
    ('One has a green bag.', 'לאחד מהם יש תיק ירוק.', 1),
    ('We do not talk.', 'אנחנו לא מדברים.', 1),
    ('I look at the sky.', 'אני מביט בשמיים.', 1),
    ('What will I do when it rains?', 'מה אעשה כשירד גשם?', 1),
    ('At school, I open the classroom door.', 'בבית הספר אני פותח את דלת הכיתה.', 2),
    ('The green bag is there!', 'התיק הירוק נמצא שם!', 2),
    ('The boys are in my class.', 'הילדים בכיתה שלי.', 2),
    ('I smile and say hello.', 'אני מחייך ואומר שלום.', 2),
]
def norm(s): return re.sub(r'[^a-z0-9]', '', html.unescape(s).lower())
async def main():
    if os.environ.get('CODEX_PROXY_CERT'):
        edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ['CODEX_PROXY_CERT'])
    text = ' '.join(s[0] for s in SENTENCES)
    stream = edge_tts.Communicate(text, voice=VOICE, rate='-15%', boundary='WordBoundary', proxy=os.environ.get('HTTPS_PROXY'))
    cues=[]
    dest=OUT/'assets/narration.mp3'
    with dest.open('wb') as f:
        async for item in stream.stream():
            if item['type']=='audio': f.write(item['data'])
            elif item['type']=='WordBoundary':
                cues.append({'word':html.unescape(item['text']), 'start':round(item['offset']/1e7,4), 'end':round((item['offset']+item['duration'])/1e7,4)})
    tokens=[w for s,_,_ in SENTENCES for w in s.split()]
    assert len(cues)==len(tokens), (len(cues),len(tokens))
    for cue,word in zip(cues,tokens):
        assert norm(cue['word'])==norm(word), (cue,word)
        cue['word']=word
    cursor=0; sentences=[]
    for en,he,p in SENTENCES:
        words=cues[cursor:cursor+len(en.split())]
        sentences.append({'text':en,'translation':he,'paragraph':p,'start':words[0]['start'],'end':words[-1]['end'],'words':words})
        cursor+=len(words)
    units=json.loads((OUT/'units.json').read_text())
    for sentence, groups in zip(sentences, units, strict=True):
        assert ' '.join(g[0] for g in groups)==sentence['text']
        sentence['units']=[{'text':en, 'translation':he} for en,he in groups]
    data={'title':'The Green Bag','audio':'assets/narration.mp3','voice':VOICE,'rate':'-15%','synthetic':True,'timing':'Speech engine word boundary events, seconds on the audio timeline','wordCount':len(cues),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'sentences':sentences}
    (OUT/'reading.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(f'Generated {dest.stat().st_size} bytes, {len(cues)} word cues, last cue {cues[-1]["end"]}s')
if __name__=='__main__': asyncio.run(main())
