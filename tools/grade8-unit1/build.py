"""Build Grade 8 Unit 1 from the existing, approved lesson; never synthesize new audio.
Run from the repository root. Word timings use CTC forced alignment of the actual MP3s.
Only unit files, the class card and the old lesson's exam date are updated.
"""
from pathlib import Path
import json, re, subprocess, tempfile, hashlib
import numpy as np
import torch, torchaudio

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'grade8/exam-01-preparation'
OUT=ROOT/'grade8/unit-1'
OUT.mkdir(parents=True,exist_ok=True)
lesson=json.loads((SRC/'lesson.json').read_text())
manifest=json.loads((SRC/'audio-manifest.json').read_text())
assert len(lesson['words'])==55 and len(lesson['story'])==18
assert ''.join(dict.fromkeys(s['paragraph'] for s in lesson['story']))=='ABCDEF'
lesson['exam']='2026-10-22'
lesson['examHebrew']='יום חמישי, י״א בחשוון תשפ״ז (22.10.2026)'
lesson['version']='20260922-unit1'
G={}
for line in '''a=מילת יידוע בלתי מסוימת: אחד או כלשהו
about=על; אודות
adventures=הרפתקאות
all=כל
am=פועל be עם I: אני נמצא כאן
an=מילת יידוע בלתי מסוימת לפני צליל תנועה
and=ו־
annual=שנתי
are=פועל be ברבים; לעיתים פועל עזר
aren’t=are not: אינם; כאן בשלילת תוכנית לעתיד
around=מסביב; ברחבי
as=כפי; במבנה as ... as: באותה מידה
at=ב־; נמצא במקום
be=להיות
beautiful=יפים
best=הטוב ביותר
but=אבל
can=יכולים; מסוגלים
careful=זהירים
cause=לגרום
corner=פינה
crazy=משוגע; יוצא דופן
a cute=חמוד
cute=חמודים
dances=ריקודים
day=יום
dressed=לבושים
drinks=משקאות
each=כל אחד
early=מוקדם
eat=לאכול
entire=כולו; כל
especially=במיוחד
even=אפילו
everybody=כולם
everywhere=בכל מקום
excited=נרגשים
festival=פסטיבל
festivals=פסטיבלים
few=מעטים; a few: כמה
fights=מריבות; food fights: מלחמות אוכל
finally=סוף סוף
first=ראשון
food=אוכל
for=ל־; עבור
forward=חלק מהביטוי look forward to: מצפים ל־
from=מ־
fruit=פירות
gathered=נאספים; מרוכזים
gets=חלק מהביטוי gets together: מתאסף
getting=חלק מהביטוי getting ready: מתכוננים
goes=נעשה; כאן goes crazy: משתגע
going=חלק מהמבנה going to: עומד לקרות
handbags=תיקים
has=יש; have עם גוף שלישי יחיד
have=יש; בהקשר have to: צריכים
heard=שמעתי
hope=מקווה
huge=ענקיות
i=אני
in=ב־
is=פועל be ביחיד: הוא או זה
it=הוא; כאן הפסטיבל
jump=קופצים
like=כמו; או אוהבים, לפי המשפט
little=מעט; קצת
live=חיות; מתקיימות במקום, לא מוקלטות
long=ארוכים
look=להסתכל; להיראות, לפי ההקשר
lopburi=לופבורי — שם העיר
loud=חזקים; רועשים
major=גדולות; משמעותיות
making=יוצרים; כאן משמיעים
many=רבים
may=עשויים; אולי
monkey=קוף
monkeys=קופים
morning=בוקר
most=ביותר
much=הרבה; כמות רבה
my=שלי
noises=קולות; רעשים
notice=מבחינים
now=עכשיו
of=של; מ־
on=על; בתאריך: ב־
one=אחד; אחת
other=אחר; each other: זה את זה
part=חלק
people=אנשים
performances=הופעות
plates=צלחות
playing=משחקים
possibly=ככל שאפשר
prepare=מכינים
put=מניחים
ready=מוכנים; getting ready: מתכוננים
right=ממש; כאן right now: ממש עכשיו
see=לראות
so=ולכן
some=קצת; כמה
sometimes=לפעמים
stay=להישאר
street=רחוב
sunglasses=משקפי שמש
tables=שולחנות
take=לקחת
thailand=תאילנד
that=כך; ש־, בהתאם למשפט
the=ה״א הידיעה: ה־
them=אותם; מהם לפי ההקשר
these=אלה
they=הם
thing=דבר
things=דברים
this=זה; הזאת
thousands=אלפים
time=זמן
to=ל־; לפני פועל מציין שם פועל
today=היום
together=יחד
town=עיר
trouble=צרות
unusual=יוצאי דופן
valuable=יקרי ערך
way=אופן; צורה
what=איזה; כאן במשפט קריאה
when=כאשר; מתי
with=עם
world=עולם
write=לכתוב
year=שנה
you=אתם; אתה או את'''.splitlines():
    k,v=line.split('=',1);G[k]=v
# Phrase-level translations are selected longest-first and preserve the source characters.
PH=[('at one of','באחד מ־'),('the most unusual festivals','הפסטיבלים יוצאי הדופן ביותר'),('in the world','בעולם'),('the Monkey Festival','פסטיבל הקופים'),('are getting ready','מתכוננים'),('some time','קצת זמן'),('my adventures','ההרפתקאות שלי'),('gets together','מתאספים'),('the entire town','כל העיר'),('goes a little crazy','קצת משתגעת'),('on this day','ביום הזה'),('are dressed like','לבושים כמו'),('live performances','הופעות חיות'),('the first thing','הדבר הראשון'),('look around town','מסתכלים ברחבי העיר'),('a few of them','כמה מהם'),('right now','ממש עכשיו'),('are gathered together','מתאספים יחד'),('on the street corner','בפינת הרחוב'),('with each other','זה עם זה'),('making loud noises','משמיעים קולות חזקים'),('may look cute','אולי נראים חמודים'),('have to be careful','צריכים להיזהר'),('cause major trouble','לגרום לצרות גדולות'),('like to take','אוהבים לקחת'),('food and drinks','אוכל ומשקאות'),('valuable things','דברים יקרי ערך'),('handbags and sunglasses','תיקים ומשקפי שמש'),('an annual festival','פסטיבל שנתי'),('look forward to it','מצפים לו'),('all year','כל השנה'),('Early in the morning','מוקדם בבוקר'),('huge plates of fruit','צלחות ענקיות של פירות'),('long tables','שולחנות ארוכים'),('aren’t going to stay that way','לא יישארו כך'),('the best part','החלק הטוב ביותר'),('thousands of excited monkeys','אלפי קופים נרגשים'),('as much fruit as they possibly can','כמה פירות שהם רק יכולים'),('food fights','מלחמות אוכל'),('have one today','יערכו אחת היום'),('What a crazy festival','איזה פסטיבל משוגע')]
OV={(9,'have'):'חלק מהביטוי have to: צריכים',(9,'to'):'חלק מהביטוי have to: צריכים',(11,'like'):'אוהבים, לפני הפועל to take',(4,'like'):'כמו',(11,'like',2):'כמו; מציג דוגמאות',(12,'look'):'חלק מהביטוי look forward to: מצפים ל־',(12,'to'):'חלק מהביטוי look forward to: מצפים ל־',(17,'one'):'אחת — מלחמת אוכל',(14,'they'):'הם — השולחנות',(14,'that'):'כך; that way: באותה צורה',(16,'that'):'ש־',(3,'on'):'ב־; on this day: ביום הזה',(8,'them'):'אותם — הקופים'}
word_re=re.compile(r"[A-Za-z]+(?:[’'][A-Za-z]+)?")
for s in lesson['story']:
    plain=s['plain'];occ={};tokens=[]
    for m in word_re.finditer(plain):
        key=m.group().lower();occ[key]=occ.get(key,0)+1
        assert key in G,(s['id'],key)
        he=OV.get((s['number'],key,occ[key]),OV.get((s['number'],key),G[key]))
        tokens.append({'text':m.group(),'startChar':m.start(),'endChar':m.end(),'he':he})
    units=[];p=0
    while p<len(tokens):
        best=None
        for phrase,he in sorted(PH,key=lambda x:len(x[0]),reverse=True):
            start=tokens[p]['startChar']
            if plain[start:start+len(phrase)].lower()==phrase.lower():
                end=start+len(phrase)
                if end==len(plain) or not plain[end].isalpha():
                    ids=[i for i in range(p,len(tokens)) if tokens[i]['startChar']<end]
                    best={'indices':ids,'he':he};break
        if best is None:best={'indices':[p],'he':tokens[p]['he']}
        units.append(best);p=best['indices'][-1]+1
    s['tokens']=tokens;s['units']=units
    s['audio']='../exam-01-preparation/'+manifest['clips'][s['id']]['src']
# Infer character boundaries from the recording, not proportional word lengths.
torch.set_num_threads(2)
bundle=torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model=bundle.get_model().eval();labels={c:i for i,c in enumerate(bundle.get_labels())}
cache=ROOT/'.cache/grade8-unit1';cache.mkdir(parents=True,exist_ok=True)
for s in lesson['story']:
    audio_path=SRC/manifest['clips'][s['id']]['src']
    assert audio_path.exists(),audio_path
    digest=hashlib.sha256(audio_path.read_bytes()+s['plain'].encode()).hexdigest()
    cached=cache/(digest+'.json')
    if cached.exists():timings=json.loads(cached.read_text())
    else:
        with tempfile.TemporaryDirectory() as tmp:
            wav=Path(tmp)/'audio.wav'
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(audio_path),'-ac','1','-ar','16000',str(wav)],check=True)
            waveform,sr=torchaudio.load(str(wav))
        transcript='|'.join(t['text'].upper().replace('’',"'") for t in s['tokens'])
        targets=torch.tensor([[labels[c] for c in transcript]],dtype=torch.int32)
        with torch.inference_mode():
            emissions,_=model(waveform);emissions=emissions.log_softmax(-1)
            alignment,scores=torchaudio.functional.forced_align(emissions,targets,blank=0)
        spans=torchaudio.functional.merge_tokens(alignment[0],scores[0].exp())
        assert len(spans)==len(transcript),(s['id'],len(spans),len(transcript))
        ratio=waveform.shape[-1]/sr/emissions.shape[1]
        timings=[];offset=0
        for token in s['tokens']:
            chars=spans[offset:offset+len(token['text'])]
            timings.append({'start':round(chars[0].start*ratio,3),'end':round(chars[-1].end*ratio,3)})
            offset+=len(token['text'])+1
        cached.write_text(json.dumps(timings))
    assert len(timings)==len(s['tokens'])
    for token,timing in zip(s['tokens'],timings):token.update(timing)
    assert all(t['end']>t['start']>=0 for t in s['tokens'])
    assert all(a['end']<=b['start']+.001 for a,b in zip(s['tokens'],s['tokens'][1:]))
    print(s['id'],len(s['tokens']),'aligned words',flush=True)
for w in lesson['words']:
    w['audio']='../exam-01-preparation/'+manifest['clips'][w['id']]['src']
lesson['timingMethod']='CTC forced alignment of the existing MP3 recordings; WAV2VEC2_ASR_BASE_960H'
lesson['voice']=manifest.get('voice','existing recording')
# Small reading pages keep the text legible on small phones; all 18 sentences remain intact.
lesson['pages']=[[0,1],[2,3],[4,5],[6,7],[8,9],[10],[11,12],[13],[14],[15,16,17]]
(OUT/'unit-data.js').write_text('window.UNIT_DATA='+json.dumps(lesson,ensure_ascii=False)+';\n')
(OUT/'index.html').write_text((Path(__file__).parent/'unit.html').read_text())
# Stable direct links for both reader standards and the HTML teacher presentation.
for name,query in [('reading','view=chunks'),('sentences','view=sentences')]:
    d=OUT/name;d.mkdir(exist_ok=True)
    (d/'index.html').write_text('<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Read Alone · Grade 8</title><script>location.replace("../?'+query+'"+(location.search?"&"+location.search.slice(1):"")+location.hash)</script><a href="../?'+query+'">פתיחת הקריאה</a></html>')
(OUT/'teacher.html').write_text('<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><title>מדריך למורה · Unit 1</title><script>location.replace("./?view=teacher"+location.hash)</script><a href="./?view=teacher">מצגת המדריך למורה</a></html>')
# Correct the old date without rebuilding or reordering its existing slides.
p=SRC/'lesson.json';old=json.loads(p.read_text());old['exam']=lesson['exam'];old['examHebrew']=lesson['examHebrew'];p.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
for name in ('teacher.html','index.html'):
    p=SRC/name
    if p.exists():p.write_text(p.read_text().replace('8.10.2026','22.10.2026').replace('2026-10-08','2026-10-22').replace('כ״ז בתשרי תשפ״ז','י״א בחשוון תשפ״ז'))
p=ROOT/'grade8/index.html';html=p.read_text()
card='<section id="grade8-unit1-card" dir="rtl" style="margin:1.2rem 0;padding:1.3rem;border:1px solid #5376ad;border-radius:18px;background:#10223b;color:#edf5ff"><h2><a href="unit-1/" style="color:inherit">Unit 1 · The Monkey Festival</a></h2><p>ח׳2 · חמישה מפגשים לפי תאריכים · מבחן: יום חמישי, י״א בחשוון תשפ״ז — 22.10.2026</p><p>קבוצה 01 בלבד · Part One A–F · שני סוגי Read Alone עם קריינות מוקלטת והדגשת מילים.</p><small>נוצר: י״א בתשרי תשפ״ז · 22.9.2026</small></section>'
if 'id="grade8-unit1-card"' not in html:
    if re.search(r'<main\b[^>]*>',html):html=re.sub(r'(<main\b[^>]*>)',r'\1'+card,html,count=1)
    else:html=re.sub(r'(<body\b[^>]*>)',r'\1'+card,html,count=1)
p.write_text(html)
(OUT/'BUILD-NOTES.md').write_text('# Grade 8 Unit 1\n\nApproved: Group 01 (55 entries), Part One A–F (18 sentences), five meetings before 22 October 2026. No Part Two and no Group 02. Existing source and all existing MP3 recordings reused. Word timing is forced alignment against each actual recording, not estimated pacing. Translation and pupil progress stay in the browser; no personal data is collected by this unit.\n\nBuild: tools/grade8-unit1/build.py. Source UI: tools/grade8-unit1/unit.html. Standards: PROJECT_CHARTER.md, Read Alone 1 and 2.\n')
print('Built',OUT,flush=True)
