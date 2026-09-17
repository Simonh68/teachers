"""Build the approved H8 exam lesson; leave the complete Monkey Festival unchanged."""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib, html, json, re, shutil, subprocess, time
ROOT=Path(__file__).resolve().parents[2]
SRC=Path(__file__).resolve().parent
OUT=ROOT/'grade8/exam-01-preparation'
V=ROOT/'grade7/band2-groups-01-02'
VERSION='20260917-approved1'

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def jsjson(path): return json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('=',1)[1].lstrip())[0]
def write_json(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def get(url):
    for attempt in range(4):
        try:
            with urlopen(Request(url,headers={'User-Agent':'Teachers-H8-Lesson-Builder/1.0'}),timeout=120) as r: return r.read()
        except Exception:
            if attempt==3: raise
            time.sleep(2**attempt)

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    old_story=ROOT/'grade8/monkey-festival/lesson-data-v2.js'
    preserved={str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'grade8/monkey-festival').rglob('*') if p.is_file()}
    words=[dict(w) for w in jsjson(V/'data.js') if w['group']==1]
    assert len(words)==55 and [w['number'] for w in words]==list(range(1,56))
    corrections=[]
    for w in words:
        # A demonstrable source translation mismatch, documented without changing the assigned word or English sentence.
        if w['en']=='Bible' and w['ex_en']=='The boy reads the Bible at home.' and w['ex_he']=='דן קורא בתנ״ך בבית.':
            corrections.append({'id':w['id'],'field':'ex_he','before':w['ex_he'],'after':'הילד קורא בתנ״ך בבית.','reason':'The source English says the boy, not Dan.'})
            w['ex_he']='הילד קורא בתנ״ך בבית.'
    original=[s for s in jsjson(old_story)['story'] if s['eyebrow'].startswith('PART ONE')]
    assert len(original)==18
    story=[]
    for i,s in enumerate(original,1):
        paragraph=re.search(r'PART ONE · ([A-F]) ·',s['eyebrow']).group(1)
        story.append({'id':f'story-{i:02d}','number':i,'paragraph':paragraph,'enHtml':s['en'],'plain':html.unescape(re.sub('<[^>]+>','',s['en'])),'he':s['he']})
    qraw=[
      (2,'basic','WHERE does the Monkey Festival take place?','היכן מתקיים פסטיבל הקופים?','It takes place in Lopburi, Thailand.','הוא מתקיים בלופבורי, תאילנד.','A'),
      (4,'basic','WHAT are many people dressed like?','כמו מה לבושים אנשים רבים?','They are dressed like monkeys.','הם לבושים כמו קופים.','B'),
      (11,'basic','WHICH two valuable things do the monkeys take?','אילו שני דברים יקרי ערך הקופים לוקחים?','They take handbags and sunglasses.','הם לוקחים תיקים ומשקפי שמש.','D'),
      (11,'comp','WHY must people be careful even though the monkeys may look cute?','מדוע צריך להיזהר אף שהקופים עשויים להיראות חמודים?','Because the monkeys can cause trouble and take things from people.','כי הקופים יכולים לגרום לצרות ולקחת דברים מאנשים.','D'),
      (13,'basic','WHEN do people prepare huge plates of fruit?','מתי אנשים מכינים צלחות ענקיות של פירות?','They prepare them early in the morning.','הם מכינים אותן מוקדם בבוקר.','E'),
      (15,'comp','WHY will the beautiful tables not stay that way?','מדוע השולחנות היפים לא יישארו כך?','Because thousands of monkeys jump on the tables and eat the fruit.','כי אלפי קופים קופצים על השולחנות ואוכלים את הפירות.','E–F'),
      (18,'comp','HOW does the writer feel about a possible food fight? Explain.','מה מרגיש הכותב כלפי האפשרות של מלחמת אוכל? הסבירו.','He seems excited because he hopes the monkeys have a food fight today.','נראה שהוא נרגש, כי הוא מקווה שהקופים יערכו מלחמת אוכל היום.','F')]
    questions=[dict(zip(('after','level','en','he','answer','answerHe','evidence'),q),number=i) for i,q in enumerate(qraw,1)]
    traw=[
      ('אנחנו מסתכלים מסביב לעיר.','We look around the town.','look · around · town',True),
      ('אנשים רבים נראים כמו קופים.','Many people look like monkeys.','many people · look like · monkeys',True),
      ('הקופים מסוגלים לקחת דברים מאנשים.','The monkeys are able to take things from people.','are able to · take things · from people',True),
      ('הקופים נראים חמודים. עם זאת, צריך להיזהר.','The monkeys look cute. However, you have to be careful.','look cute · however · have to be careful',True),
      ('אנשים מכינים צלחות ענקיות של פירות.','People prepare huge plates of fruit.','prepare · huge plates · fruit',False),
      ('הקופים לוקחים דברים יקרי ערך.','The monkeys take valuable things.','monkeys · take · valuable things',False)]
    translations=[dict(zip(('he','en','hint','overlap'),t),number=i) for i,t in enumerate(traw,1)]
    payload={'version':VERSION,'exam':'2026-10-08','examHebrew':'יום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026)','scopeApproved':'Full Group 01 only; Part One A–F only','words':words,'story':story,'questions':questions,'translations':translations}
    write_json(OUT/'lesson.json',payload)
    shutil.copyfile(SRC/'index.template.html',OUT/'index.html')
    for name in ['exam.js','exam.css']: shutil.copyfile(SRC/name,OUT/name)
    with (OUT/'exam.css').open('a',encoding='utf-8') as f: f.write('\n@media(max-height:520px){.intro h1{font-size:30px}.intro h2{font-size:24px}.intro p{font-size:16px;line-height:1.35}.intro .pad{gap:6px}.intro .small{font-size:12px}}\n')
    shutil.copyfile(V/'visuals.js',OUT/'visuals.js')
    audio(words,story)
    provenance={'sourceWords':str((V/'data.js').relative_to(ROOT)),'sourceWordSHA256':digest(V/'data.js'),'sourceStory':str(old_story.relative_to(ROOT)),'sourceStorySHA256':digest(old_story),'vocabularyCount':55,'storySentences':18,'basicQuestions':4,'comprehensionQuestions':3,'translationExercises':6,'vocabularyBrainBreaks':18,'readingBrainBreaks':3,'documentedTranslationCorrections':corrections,'sourceStoryFolderUnchanged':all(digest(ROOT/p)==d for p,d in preserved.items())}
    assert provenance['sourceStoryFolderUnchanged']
    write_json(OUT/'source-report.json',provenance)
    teacher(words,story,questions)
    card=ROOT/'grade8/index.html';text=card.read_text(encoding='utf-8')
    pattern=r'<a class="card" href="exam-01-preparation/[^\"]*">[\s\S]*?</a>'
    match=re.search(pattern,text);assert match,'Existing exam card not found; refusing navigation rewrite'
    replacement='<a class="card" href="exam-01-preparation/?v='+VERSION+'"><span class="index">01</span><span class="type">הכנה למבחן הראשון · אודיו AI</span><h2>קבוצה 01 במלואה והחלק הראשון של הסיפור</h2><p>יום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026). כל 55 ערכי Band II · Core I · Group 01 בלבד; The Monkey Festival, Part One A–F בלבד. משפט־משפט עם תרגום, 7 שאלות, 6 תרגילי תרגום, התנחתות ואודיו מוקלט מהאתר. קבוצה 02 והחלק השני אינם כלולים.</p><div class="created"><b>נוצר:</b> יום חמישי, ו׳ בתשרי תשפ״ז <time datetime="2026-09-17">(17.9.2026)</time></div><div class="open">פתיחת מצגת ההכנה <span>←</span></div></a>'
    card.write_text(text[:match.start()]+replacement+text[match.end():],encoding='utf-8')
    print('BUILT: 55 words, 18 original sentences, 7 questions, 6 translations, 73 MP3 files',flush=True)

def audio(words,story):
    jobs=[(w['id'],w['en'].rstrip('.!?')+'. '+w['ex_en']) for w in words]+[(s['id'],s['plain']) for s in story]
    folder=OUT/'audio';folder.mkdir(exist_ok=True)
    candidates=[]
    for p in [V/'audio/manifest.json',V/'audio-manifest.json']:
        if p.exists():
            m=json.loads(p.read_text(encoding='utf-8'));candidates.extend((V,c) for c in (m.get('files') or m.get('clips') or {}).values() if isinstance(c,dict))
    model=None;clips={};cache=ROOT/'.cache/kokoro-v1';cache.mkdir(parents=True,exist_ok=True)
    for ident,text in jobs:
        fp=hashlib.sha256(text.encode()).hexdigest()[:12];mp3=folder/f'{ident}-{fp}.mp3'
        if not mp3.exists():
            source=next((base/c['src'] for base,c in candidates if c.get('text')==text and (base/c['src']).is_file()),None)
            if source:shutil.copyfile(source,mp3)
            else:
                import numpy as np
                import soundfile as sf
                from kokoro_onnx import Kokoro
                if model is None:
                    for name in ['kokoro-v1.0.onnx','voices-v1.0.bin']:
                        path=cache/name
                        if not path.exists():path.write_bytes(get('https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'+name))
                    model=Kokoro(str(cache/'kokoro-v1.0.onnx'),str(cache/'voices-v1.0.bin'))
                samples,sr=model.create(text,voice='af_heart',speed=.88,lang='en-us')
                samples=np.asarray(samples,dtype=np.float32)
                assert np.isfinite(samples).all() and len(samples)>sr*.25 and np.max(np.abs(samples))>.005,ident
                wav=folder/f'{ident}.wav';sf.write(wav,samples,sr)
                subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(wav),'-codec:a','libmp3lame','-b:a','128k',str(mp3)],check=True);wav.unlink()
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(mp3)],text=True))
        assert .25<duration<50 and mp3.stat().st_size>1000,(ident,duration)
        clips[ident]={'src':'audio/'+mp3.name,'text':text,'duration':round(duration,3),'sha256':digest(mp3)}
        print('MP3',ident,round(duration,2),flush=True)
    write_json(OUT/'audio-manifest.json',{'engine':'Kokoro v1.0','voice':'af_heart','language':'en-US','synthetic':True,'browserTTS':False,'count':len(clips),'clips':clips})
    assert len(clips)==73
    (OUT/'AUDIO-NOTICE.txt').write_text('Prerecorded AI narration, Kokoro v1.0 / af_heart, US English. Vocabulary + original English examples, and original Part One sentences only. No browser TTS. Model: https://huggingface.co/hexgrad/Kokoro-82M (Apache-2.0). Runtime: https://github.com/thewh1teagle/kokoro-onnx (MIT). Existing source narration reused only when the full transcript matches.\n',encoding='utf-8')

def teacher(words,story,questions):
    rows=''.join('<p><b>'+html.escape(s['paragraph']+' · '+str(s['number']))+'</b> — <span dir="ltr">'+html.escape(s['plain'])+'</span></p>' for s in story)
    qs=''.join('<p><b>'+str(q['number'])+' · '+('בסיסית' if q['level']=='basic' else 'הבנה')+'</b> <span dir="ltr">'+html.escape(q['en'])+'</span><br><span dir="ltr">'+html.escape(q['answer'])+'</span><br>'+q['answerHe']+'</p>' for q in questions)
    page='<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ח׳2 — תסריט ומפתח</title><style>body{font:20px/1.6 Arial,sans-serif;max-width:1000px;margin:auto;padding:28px;background:#071526;color:#edf8ff}a{color:#7ce8ff}h1,h2{color:#e0ff85}span[dir=ltr]{display:inline-block;text-align:left}p{margin:18px 0}</style><a href="./">למצגת</a><h1>ח׳2 — הכנה למבחן הראשון</h1><p>יום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026), בכפוף לשינויי בית הספר.</p><p>כל 55 ערכי קבוצה 01 בלבד + כל 18 משפטי Part One A–F. זהו מאגר הכנה מלא, ולא יעד להקניית 55 מילים חדשות בשעה אחת.</p><h2>מסלול שיעור מוצע — 60 דקות</h2><p>0–12: חזרה ממוקדת על מילים נבחרות, לא כל הקבוצה. 12–50: קריאת החלק הראשון והשאלות המשולבות. 50–58: תרגום שניים–שלושה משפטים. 58–60: בדיקת יציאה. יתר המילים והתרגילים זמינים לחזרה בבית או במפגש נוסף.</p><h2>חשיפה ושמע</h2><p>מילה ומשפט → הוספת פירוש ותרגום, בלי הזזת המקור. אחרי שלושה ערכים התנחתא. בשאלה: אנגלית → עברית → תשובה אפשרית באנגלית → תרגום התשובה. אין חשיפת תשובה לפני ניסיון תלמיד. קריינות 73 הקלטות מקור: 55 מילים ודוגמאות + 18 משפטי סיפור. אין אודיו בשאלות או בתרגומים.</p><h2>משפטי הקריאה לפי המקור</h2>'+rows+'<h2>שאלות ומפתח</h2>'+qs+'<h2>הערת מקור</h2><p>המצגת המלאה המקורית לא שונתה. בקבוצה 01 תוקן רק אי־התאמה מפורש: The boy תורגם הילד במקום דן. התיקון מתועד ב־source-report.json; המילה והמשפט באנגלית נשמרו.</p></html>'
    (OUT/'teacher.html').write_text(page,encoding='utf-8')

if __name__=='__main__':build()
