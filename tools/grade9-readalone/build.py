"""Build Grade 9 Read Alone 1+2 from the unchanged original story.
The only speech-service payload is the already-public English fictional story.
No student answers, identifiers, credentials or Hebrew translations are sent.
"""
from __future__ import annotations
import asyncio, copy, hashlib, html, json, re, shutil, subprocess, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import edge_tts
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
UNIT = ROOT / 'grade9/unit-1'
OUT = UNIT / 'read-alone'
DECK = ROOT / 'grade9/the-message-without-a-voice/index.html'
BACKUP = HERE / 'source-original.html'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'assets').mkdir(exist_ok=True)
TOKEN = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*")
def norm(text): return re.sub('[^a-z0-9]', '', html.unescape(text).lower())
def dump(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
current = DECK.read_text(encoding='utf-8')
if 'data-ra-deck=' not in current:
    BACKUP.write_text(current, encoding='utf-8')
assert BACKUP.exists(), 'Original presentation backup is required'
source = BACKUP.read_text(encoding='utf-8')
soup = BeautifulSoup(source, 'html.parser')
original_ids = [s['id'] for s in soup.select('section.slide')]
paragraphs = soup.select('p.story-sentence')
translations = json.loads((HERE / 'translations.json').read_text(encoding='utf-8'))
assert len(paragraphs) == len(translations) == 46, (len(paragraphs), len(translations))
sentences, global_words = [], []
for number, (p, entry) in enumerate(zip(paragraphs, translations)):
    text = p.get_text()
    matches = list(TOKEN.finditer(text))
    authored = [w for unit in entry['u'] for w in TOKEN.findall(unit[0])]
    assert [norm(m.group()) for m in matches] == [norm(w) for w in authored], (number+1, text, authored)
    words, units, cursor, previous_end = [], [], 0, 0
    for item in entry['u']:
        english, hebrew = item[:2]
        expected = TOKEN.findall(english)
        glosses = item[2].split('|') if len(item) > 2 else [hebrew]
        assert len(glosses) == len(expected), (number+1, item, len(expected))
        first = cursor
        for meaning in glosses:
            m = matches[cursor]
            word = {'word':m.group(), 'he':meaning, 'prefix':text[previous_end:m.start()], 'index':len(global_words)}
            words.append(word); global_words.append(word)
            previous_end = m.end(); cursor += 1
        units.append({'en':english, 'he':hebrew, 'first':first, 'last':cursor-1})
    sentences.append({'en':text, 'he':entry['he'], 'words':words, 'units':units, 'suffix':text[previous_end:]})
    rebuilt = ''.join(w['prefix']+w['word'] for w in words)+text[previous_end:]
    assert rebuilt == text, ('English changed', number+1)
pages = []
for start, end in [(0,10),(10,24),(24,36),(36,46)]:
    group, count = [], 0
    for i in range(start,end):
        n = len(sentences[i]['words'])
        if group and (count+n > 30 or len(group) == 3): pages.append(group); group, count = [], 0
        group.append(i); count += n
    if group: pages.append(group)
assert [i for page in pages for i in page] == list(range(46))
data = {'title':'The Message Without a Voice','grade':9,'groups':[21,22,23],'sentences':sentences,'pages':pages,'image':'assets/library.webp','source_sha256':hashlib.sha256(source.encode()).hexdigest()}
dump(OUT/'content.json',data)
text = ' '.join(s['en'] for s in sentences)
text_hash = hashlib.sha256(text.encode()).hexdigest()
async def build_audio():
    cached = OUT/'audio.json'
    if cached.exists():
        old = json.loads(cached.read_text())
        if old.get('text_sha256') == text_hash and (OUT/old['audio']).exists():
            print('Reusing verified unchanged narration', flush=True)
            return old
    cues=[]
    dest = OUT/'assets/narration.mp3'
    for attempt in range(3):
        cues=[]
        try:
            comm=edge_tts.Communicate(text,voice='en-US-BrianNeural',pitch='+10Hz',boundary='WordBoundary')
            with dest.open('wb') as f:
                async for chunk in comm.stream():
                    if chunk['type']=='audio': f.write(chunk['data'])
                    elif chunk['type']=='WordBoundary': cues.append({'word':html.unescape(chunk['text']),'start':chunk['offset']/1e7,'end':(chunk['offset']+chunk['duration'])/1e7})
            assert dest.stat().st_size > 10000 and cues
            break
        except Exception:
            if attempt==2: raise
            await asyncio.sleep(3*(attempt+1))
    assert ''.join(norm(w['word']) for w in global_words)==''.join(norm(c['word']) for c in cues), 'Speech boundaries do not match source words'
    cue_spans=[]; pos=0
    for c in cues:
        length=len(norm(c['word']))
        if length: cue_spans.append((pos,pos+length,c)); pos+=length
    aligned=[]; pos=0
    for index,w in enumerate(global_words):
        a,b=pos,pos+len(norm(w['word'])); pos=b; parts=[]
        for x,y,c in cue_spans:
            left,right=max(a,x),min(b,y)
            if left < right:
                duration=c['end']-c['start']
                parts.append((c['start']+duration*(left-x)/(y-x),c['start']+duration*(right-x)/(y-x)))
        assert parts, w
        aligned.append({'word':w['word'],'index':index,'start':parts[0][0],'end':parts[-1][1]})
    clips=[]; cursor=0
    for s in sentences:
        words=aligned[cursor:cursor+len(s['words'])]; cursor+=len(words)
        clips.append({'start':words[0]['start'],'end':words[-1]['end'],'words':words})
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(dest)],text=True).strip())
    assert clips[-1]['end'] <= duration+.2 and duration>60, (duration,clips[-1]['end'])
    for a,b in zip(aligned,aligned[1:]): assert a['start']<=a['end']<=b['start']+.01, (a,b)
    out={'audio':'assets/narration.mp3','voice':'en-US-BrianNeural','pitch':'+10Hz','synthetic':True,'duration':duration,'text_sha256':text_hash,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'timing_source':'Microsoft speech-engine measured WordBoundary events; merged boundaries aligned by normalized source characters','sentences':clips}
    dump(cached,out)
    print('Recorded',len(clips),'sentences,',len(aligned),'words,',round(duration,2),'seconds',flush=True)
    return out
audio=asyncio.run(build_audio())
image_url='https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=900&q=85'
image_path=OUT/'assets/library.webp'
if not image_path.exists():
    req=urllib.request.Request(image_url,headers={'User-Agent':'Teachers educational website media builder'})
    with urllib.request.urlopen(req,timeout=60) as response:
        raw=OUT/'assets/library-source.jpg'; raw.write_bytes(response.read())
    with Image.open(raw) as im:
        im=im.convert('RGB'); im.thumbnail((1000,1000)); im.save(image_path,'WEBP',quality=83)
    raw.unlink()
for name in ['player.js','reader.css']: shutil.copyfile(HERE/name,OUT/name)
(OUT/'index.html').write_text('''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#081423"><title>The Message Without a Voice — Read Alone · כיתה ט׳</title><link rel="stylesheet" href="reader.css?v=20260922-ra1"><script defer src="player.js?v=20260922-ra1"></script></head>
<body class="ra-page"><main id="raApp"><header class="ra-header"><a class="ra-home" href="../../../#grade9" aria-label="חזרה לכיתה ט׳">⌂</a><a href="../">כיתה ט׳ · Unit 1</a><a href="../../the-message-without-a-voice/">המצגת המלאה</a></header><h1 class="ra-title" lang="en">The Message Without a Voice</h1><p class="ra-subtitle">תקשורת וקשרים · קריאה מלווה · הטקסט המקורי במלואו</p><nav class="ra-modes" aria-label="בחירת מסלול קריאה"><button class="ra-mode" data-mode="text" aria-pressed="true">Read Alone Text · קטעים</button><button class="ra-mode" data-mode="sentences" aria-pressed="false">Read Alone · משפטים</button></nav><div id="raTabs" role="tablist" aria-label="קטעי הסיפור"></div><section id="raPanel" aria-label="אזור קריאה"><p>טוען את הסיפור…</p></section><div id="raControls"></div><nav class="ra-nav" aria-label="ניווט בקריאה"><button id="raPrev">→ הקודם</button><output id="raCounter" aria-live="polite"></output><button id="raNext">המשך ←</button></nav><progress id="raProgress" value="0" max="1" aria-label="התקדמות בקריאה"></progress><div class="ra-meta"><button id="raReveal">תרגום הקטע</button><small>קריינות סינתטית מוקלטת · ההעדפות נשמרות במכשיר בלבד · <a href="https://unsplash.com/license" target="_blank" rel="noopener">תצלום: Unsplash</a></small></div><div id="raFullTranslation" hidden></div><noscript>יש להפעיל JavaScript לקריאה המלווה. <a href="../reading.html">פתיחת הטקסט להדפסה</a></noscript></main></body></html>
''',encoding='utf-8')
# Preserve every original slide and its stable URL. Add only translation partners.
for n,p in enumerate(paragraphs):
    s=sentences[n]
    rendered=''.join(html.escape(w['prefix'])+'<span class="ra-word ra-hit" data-w="'+str(w['index'])+'" data-he="'+html.escape(w['he'],quote=True)+'" tabindex="0" role="button" aria-label="'+html.escape(w['word']+' — פירוש',quote=True)+'">'+html.escape(w['word'])+'</span>' for w in s['words'])+html.escape(s['suffix'])
    p.clear()
    fragment=BeautifulSoup(rendered,'html.parser')
    for node in list(fragment.contents): p.append(node)
    assert p.get_text()==s['en']
    section=p.find_parent('section'); section['data-ra-sentence']=str(n); section['data-pair']='ra-sentence-'+str(n)
    slot=soup.new_tag('div',attrs={'class':'translation-slot','style':'visibility:hidden','aria-hidden':'true'})
    he=soup.new_tag('p',attrs={'class':'translation','lang':'he','dir':'rtl'}); he.string=s['he']; slot.append(he); section.select_one('.frame').append(slot)
    clone=copy.deepcopy(section); clone['id']=section['id']+'-translation'; clone['hidden']=''; clone['class']=[c for c in clone.get('class',[]) if c!='active']+['reveal']
    partner=clone.select_one('.translation-slot'); partner.attrs.pop('style',None); partner.attrs.pop('aria-hidden',None)
    section.insert_after(clone)
soup.body['data-ra-deck']='grade9-unit1'
style=soup.new_tag('link',rel='stylesheet',href='../unit-1/read-alone/reader.css?v=20260922-ra1'); soup.head.append(style)
script=soup.new_tag('script',src='../unit-1/read-alone/player.js?v=20260922-ra1',defer=''); soup.head.append(script)
for script in soup.find_all('script'):
    if not script.string or 'const slides = ' not in script.string: continue
    js=script.string
    old="history.replaceState(null, '', '#slide-' + (current + 1));"
    assert old in js
    js=js.replace(old,"history.replaceState(null, '', '#' + slide.id);")
    old='    fit();\n  }\n  navButtons'
    assert old in js
    js=js.replace(old,"    fit();\n    document.dispatchEvent(new CustomEvent('teachers:slidechange', {detail:{id:slide.id}}));\n  }\n  navButtons")
    old="function fromHash() { const match = location.hash.match(/^#slide-(\\d+)$/); show(match ? Number(match[1])-1 : 0, false); }"
    assert old in js
    js=js.replace(old,"function fromHash() { let id = location.hash.slice(1); if (/^\\d+$/.test(id)) id = 'slide-' + id; const index = slides.findIndex(s => s.id === id); show(Math.max(0,index), false); }")
    script.string=js
all_slides=soup.select('section.slide')
assert len(all_slides)==len(original_ids)+46
assert [s['id'] for s in all_slides if not s['id'].endswith('-translation')]==original_ids
for n,s in enumerate(all_slides): s['aria-label']=f'{n+1} מתוך {len(all_slides)}'
links='<div class="ra-inline-links"><a href="../unit-1/read-alone/">Read Alone Text · קריאה בקטעים</a><a href="../unit-1/">כל חומרי היחידה</a></div>'
for target in [soup.select_one('.cover .frame'),soup.select_one('.transition[data-section="reading"] .frame')]:
    if target: target.append(BeautifulSoup(links,'html.parser'))
DECK.write_text(str(soup),encoding='utf-8')
# Add both routes to existing unit pages without removing text or exercises.
block='''<section class="panel" id="read-alone-paths"><p class="eyebrow">קריאה מלווה · שני מסלולים</p><h2>Read Alone — The Message Without a Voice</h2><p>הסיפור המלא, קריינות מוקלטת והדגשה צהובה של כל מילה. בחרו קריאה בקטעים עם תרגום ביטויים, או משפט אחד בכל שקף עם תרגום מילה וחשיפת תרגום המשפט בשקף הבא.</p><div class="actions"><a class="button primary" data-track href="read-alone/">Read Alone Text · קטעים</a><a class="button" data-track href="read-alone/?mode=sentences">Read Alone · משפטים</a><a class="button" data-track href="../the-message-without-a-voice/#slide-36">המצגת המלאה · המשך משקף 36</a></div><p>מהירות התחלתית: איטית (0.75). אפשר להאט עד רבע מהמהירות; הבחירה נשמרת גם במעבר בין המסלולים.</p></section>'''
for name in ['index.html','resources.html','reading.html','student-preparation.html','teacher.html']:
    path=UNIT/name; document=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    for old in document.select('#read-alone-paths'): old.decompose()
    target=document.select_one('section.hero')
    frag=BeautifulSoup(block,'html.parser')
    if target: target.insert_after(frag)
    else:
        main=document.select_one('main') or document.body
        main.insert(0,frag)
    path.write_text(str(document),encoding='utf-8')
manifest_path=UNIT/'manifest.json'
manifest=json.loads(manifest_path.read_text())
manifest['readAlone']={'status':'implemented','text':'read-alone/','sentences':'read-alone/?mode=sentences','fullPresentation':'../the-message-without-a-voice/','sentenceCount':46,'pageCount':len(pages),'wordCount':len(global_words),'prerecorded':True,'defaultRate':.75,'speedStorageKey':'teachers-read-alone-speed-v1'}
dump(manifest_path,manifest)
report={'status':'built-awaiting-browser-verification','sourceEnglishUnchanged':True,'source_sha256':data['source_sha256'],'sentences':46,'words':len(global_words),'meaningUnits':sum(len(s['units']) for s in sentences),'textPages':len(pages),'sentenceSlides':92,'originalSlidesPreserved':len(original_ids),'fullPresentationSlides':len(all_slides),'voice':audio['voice'],'pitch':audio['pitch'],'audioDurationSeconds':audio['duration'],'audioSha256':audio['sha256'],'photoSource':image_url,'groups':[21,22,23],'testDatesChanged':False}
dump(OUT/'completion-report.json',report)
(OUT/'README.md').write_text('# Grade 9 Unit 1 — Read Alone 1+2\n\nBoth routes use the complete original story, the same prerecorded synthetic Brian +10Hz narration and measured word boundaries.\n\nEnglish: 46 sentences; no source words or punctuation changed. Original lesson slides and stable slide IDs preserved. Translation partner slides were added. User answers and progress remain local. No browser speech synthesis.\n\nBuild sources: tools/grade9-readalone/. QA report: qa-report.json.\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
