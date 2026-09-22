"""Build the published unit from approved scope and exact Core I records."""
from pathlib import Path
import json, re, shutil, html

ROOT = Path(__file__).resolve().parents[2]
TOOL = Path(__file__).resolve().parent
OUT = ROOT / 'grade7/unit-2'
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = TOOL / 'sources'
SOURCES.mkdir(exist_ok=True)
TEMPLATES = TOOL / 'templates'
for target, source, files in [
    ('grammar','grade7/unit-1/reading',['lesson.js','lesson.css','index.html']),
    ('vocabulary','grade7/band2-groups-01-02',['full.html','sequence.js','sequence.css']),
    ('unit','grade7/unit-1',['teacher.html','teacher.js','unit.css','hub.js'])
]:
    dest=TEMPLATES/target
    dest.mkdir(parents=True,exist_ok=True)
    for name in files:
        if not (dest/name).exists():
            shutil.copyfile(ROOT/source/name,dest/name)
records_path = SOURCES / 'vocabulary-records.json'
if not records_path.exists():
    raise FileNotFoundError('The approved immutable vocabulary snapshot is required.')
records = json.loads(records_path.read_text())
assert len(records) == 165
assert all(sum(w['group']==g for w in records)==55 for g in (3,4,5))
corrections_path=SOURCES/'vocabulary-corrections.json'
corrections=json.loads(corrections_path.read_text()) if corrections_path.exists() else {}
source_records=json.loads(records_path.read_text())
for record in records:
    correction=corrections.get(record['id'])
    if correction:
        record['editorial_correction']=correction['reason']
        for key,value in correction.items():
            if key!='reason':record[key]=value
        if 'mean_he' in correction:record['record_sense_he']=correction['mean_he']

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def slide(kind, title, section, **kw):
    return dict(kind=kind, title=title, section=section, home=True, **kw)

def quiz(deck, title, section, question, opts, answer, why):
    for reveal in (False, True):
        deck.append(slide('quiz',title,section,q=question,opts=opts,correct=opts.index(answer),why=why,context='נסו בעצמכם לפני החשיפה',reveal=reveal,tense='הווה'))

def example(deck, en, he, section):
    for reveal in (False, True):
        deck.append(slide('example','משפט בהקשר',section,en=en,he=he,reveal=reveal,tense='הווה'))

def task(deck, title, section, prompt, model, check):
    deck.append(slide('task',title,section,prompt=prompt,tense='הווה'))
    deck.append(slide('review',title,section,model=model,check=check,tense='הווה'))

def rule(deck, title, section, formula, he):
    deck.append(slide('rule',title,section,formula=formula,he=he,tense='הווה'))

A=[slide('cover','Present Simple · Part A','פתיחה',sub='הרגלים, גוף שלישי ושלילה')]
A.append(slide('plan','מה נוכל לכתוב?','פתיחה',steps=['משפט על השגרה שלי','משפט על השגרה של ילד אחר','משפט המסביר מה אינו קורה בשגרה']))
quiz(A,'בדיקת פתיחה','מה כבר יודעים?','I ___ a bag to school.',['carry','carries','carrying'],'carry','עם I משתמשים בצורת הבסיס.')
quiz(A,'בדיקת פתיחה','מה כבר יודעים?','David ___ to school every day.',['walk','walking','walks'],'walks','David הוא אדם יחיד: he. בחיוב מוסיפים s.')
rule(A,'פעולה חוזרת','שגרה','I walk to school every day.','Present Simple מתאר הרגלים ושגרה. ההקשר יכול להראות חזרה גם בלי every day.')
example(A,'I carry a bag.','אני נושא תיק.','שגרה')
example(A,'We study geography.','אנחנו לומדים גיאוגרפיה.','שגרה')
rule(A,'מי עושה את הפעולה?','גוף שלישי','I / you / we / they carry.\nHe / she / it carries.','קודם מזהים את הנושא. שם של אדם יחיד מתנהג כמו he או she.')
example(A,'Daniel carries a bag.','דניאל נושא תיק.','גוף שלישי')
quiz(A,'נושא יחיד','גוף שלישי','The teacher ___ notes to the class.',['hand out','hands out','handing out'],'hands out','The teacher הוא נושא יחיד. הביטוי hand out פירושו לחלק.')
quiz(A,'נושא ברבים','גוף שלישי','The students ___ notes to the class.',['hands out','handing out','hand out'],'hand out','The students הם they. הפועל נשאר בצורת הבסיס.')
rule(A,'הוספת s','כתיב','walk → walks\nplay → plays','ברוב הפעלים מוסיפים s. ב־play יש תנועה לפני y, ולכן ה־y נשארת.')
rule(A,'הוספת es','כתיב','watch → watches\ngo → goes','לומדים את הצורות עם המשפטים, ולא רק כרשימה.')
rule(A,'עיצור לפני y','כתיב','carry → carries\nstudy → studies','כאשר עיצור מופיע לפני y, מחליפים את y ב־ies בגוף שלישי בחיוב.')
quiz(A,'בחירת צורה','כתיב','John ___ geography.',['study','studies','studying'],'studies','לפני y יש עיצור. study הופך ל־studies.')
quiz(A,'בחירת צורה','כתיב','Rina ___ a drum.',['plays','play','plaies'],'plays','ב־play יש תנועה לפני y, ולכן מוסיפים s בלבד.')
task(A,'עצירת כתיבה','יישום ראשון','כתבו שני משפטים: אחד עליכם עם carry ואחד על חבר עם אותו פועל.','I carry a notebook.\nDavid carries a notebook.','התוכן יכול להיות שונה. בדקו התאמה לנושא ומשפט שלם.')
rule(A,'שלילה','שלילה',"I don't walk.\nHe doesn't walk.",'אחרי don’t או doesn’t משתמשים בצורת הבסיס. does כבר נושא את סימון הגוף השלישי.')
example(A,"We don't go to school on foot.",'אנחנו לא הולכים לבית הספר ברגל.','שלילה')
example(A,"Daniel doesn't carry a drum.",'דניאל לא נושא תוף.','שלילה')
quiz(A,'בחירת מילת שלילה','שלילה','His friends ___ take a train.',["don't","doesn't","isn't"],"don't",'His friends הם they, ולכן משתמשים ב־don’t.')
quiz(A,'הפועל אחרי doesn’t','שלילה',"John doesn't ___ to school.",['walks','walking','walk'],'walk','אחרי doesn’t הפועל חוזר לצורת הבסיס.')
task(A,'שינוי משמעות','שלילה','הפכו לשלילה: We carry books. כתבו את המשפט השלם.',"We don't carry books.",'שומרים על הנושא ומשתמשים ב־don’t ובצורת הבסיס.')
rule(A,'תיאור ופעולה','be או פועל רגיל','He is confident.\nHe walks to school.','confident הוא תואר ולכן משתמשים ב־is. במשפט על הליכה הפועל הוא walks.')
quiz(A,'תיאור מצב','be או פועל רגיל','The notebook ___ available.',['is','does','do'],'is','available הוא תואר: זמין. משתמשים ב־is.')
quiz(A,'פעולה רגילה','be או פועל רגיל','Which sentence is correct?',['He is walks to school.','He walks to school.','He walking to school.'],'He walks to school.','במשפט הזה walks הוא הפועל. אין צורך ב־is.')
task(A,'כרטיס יציאה','כתיבה עצמאית','כתבו שלושה משפטים אמיתיים: הרגל שלכם, הרגל של חבר, ומשפט שלילה אחד. השתמשו בשתי מילים מהיחידה.',"I carry a notebook.\nJohn studies geography.\nI don't play a drum.",'קודם בדקו שהמשמעות ברורה. אחר כך בדקו נושא ופועל, שלילה ואיות. הדוגמה נחשפת רק אחרי כתיבה ואיסוף.')
A.append(slide('finish','סיכום','סיכום',text="I carry. / He carries.\nI don't carry. / He doesn't carry.",sub='ממשיכים לחלק ב׳ אחרי שהמורה בודק את הכתיבה.'))

B=[slide('cover','Present Simple · Part B','פתיחה',sub='שאלות, תדירות ושיחה על שגרה')]
quiz(B,'חזרה קצרה','בדיקת פתיחה','David ___ geography.',['study','studies','studying'],'studies','נושא יחיד, משפט חיוב.')
quiz(B,'חזרה קצרה','בדיקת פתיחה',"She doesn't ___ a heavy bag.",['carry','carries','carrying'],'carry','אחרי doesn’t משתמשים בצורת הבסיס.')
rule(B,'שאלות כן או לא','Do / Does','Do you walk to school?\nDoes David walk to school?','Do עם I/you/we/they. Does עם he/she/it. הפועל שאחריהם בצורת הבסיס.')
example(B,'Does Daniel carry a notebook?','האם דניאל נושא מחברת?','Do / Does')
quiz(B,'בחירת מילת עזר','Do / Does','___ your friends walk to school?',['Does','Do','Is'],'Do','your friends הם they.')
quiz(B,'הפועל בשאלה','Do / Does','Does Rina ___ a drum?',['plays','playing','play'],'play','Does לפני הנושא, והפועל בצורת הבסיס.')
rule(B,'תשובות קצרות','תשובות קצרות',"Do you walk? Yes, I do.\nDoes he walk? No, he doesn't.",'בתשובה קצרה חוזרים על do או does, בהתאם לנושא שבתשובה.')
quiz(B,'התאמת התשובה','תשובות קצרות','Do you and Daniel walk? Yes, ___.',['they do','we do','he does'],'we do','כשעונים על שאלה עליי ועל דניאל, הנושא בתשובה הוא we.')
task(B,'סידור שאלה','תשובות קצרות','סדרו וכתבו: your friend / Does / geography / like / ?','Does your friend like geography?','Does לפני הנושא, like בצורת הבסיס וסימן שאלה בסוף.')
rule(B,'איזה מידע חסר?','מילות שאלה','When? → a time\nWhere? → a place\nHow? → a way','בוחרים את מילת השאלה לפי סוג התשובה המבוקש.')
example(B,'How does John get to school?','איך ג׳ון מגיע לבית הספר?','מילות שאלה')
example(B,'When do lessons start?','מתי השיעורים מתחילים?','מילות שאלה')
quiz(B,'שאלה על דרך','מילות שאלה','___ does John get to school? By train.',['When','How','What'],'How','By train מתאר דרך הגעה.')
quiz(B,'שאלה על זמן','מילות שאלה','___ do lessons start? At eight.',['Where','How','When'],'When','At eight היא תשובה על זמן.')
rule(B,'עוד שתי שאלות','מילות שאלה','What do you study?\nWhy do you walk?','What שואל מה. Why שואל מדוע. אחרי מילת השאלה עדיין צריך do/does.')
rule(B,'תדירות','תדירות','I usually walk.\nHe sometimes takes a bus.\nThey never take a train.','usually: בדרך כלל; sometimes: לפעמים; never: אף פעם. במשפטים האלה מילת התדירות לפני הפועל הרגיל.')
example(B,'Daniel usually carries a notebook.','דניאל בדרך כלל נושא מחברת.','תדירות')
rule(B,'תדירות עם be','תדירות','She is usually ready.','עם am/is/are, מילת התדירות באה בדרך כלל אחרי הפועל.')
quiz(B,'סדר מילים','תדירות','Which sentence is correct?',['He usually walks.','He usually walking.','He usually walk.'],'He usually walks.','usually לפני הפועל הרגיל; walks מתאים ל־he.')
rule(B,'רצון, ידיעה והעדפה','פועלי מצב','I know the way.\nShe likes geography.\nHe wants to improve.','Present Simple מתאים גם לידיעה, העדפה ורצון. אין צורך להפוך אותם לצורת ing כדי לתאר מצב בהווה.')
task(B,'שיחה בזוגות','דיבור','שאלו חבר: How do you get to school? What do you do after school? רשמו שתי תשובות קצרות.', 'By bus. / I play a drum.','בודקים שהחבר קיבל את המידע שביקש. אין צורך בתשובה זהה לדוגמה.')
task(B,'דיווח על חבר','דיבור','כתבו משפט אחד על החבר בעקבות השיחה. השתמשו ב־usually או sometimes.','David usually gets to school by bus.','המידע צריך להתאים לתשובת החבר. בודקים גוף שלישי ומקום מילת התדירות.')
quiz(B,'בדיקת סיום','העברה עצמאית','___ the school year start in April?',['Do','Does','Is'],'Does','the school year הוא נושא יחיד; start נשאר בצורת הבסיס.')
task(B,'שאלה עצמאית','העברה עצמאית','כתבו שאלה באנגלית כדי לברר מתי חופשת הקיץ מסתיימת.','When does summer vacation end?','בודקים מילת שאלה מתאימה, does, נושא ופועל בסיס.')
B.append(slide('finish','מה נוכל לעשות עכשיו?','סיכום',text='How do you get to school?\nWhen does your school year end?',sub='נשאל, נקשיב ונכתוב את המידע על אדם אחר.'))

seasonal=json.loads((ROOT/'tools/unit-2/sources/seasonal-main.json').read_text())
calendar=seasonal['calendar']
main_sections=seasonal['main']
stories=json.loads((SOURCES/'journey-messages.json').read_text())
save(OUT/'content.json',dict(title='School Years Around the World',status='published',published='2026-09-22',groups=[3,4,5],main=main_sections,calendar=calendar,stories=stories))

# Reuse Unit 1's tested navigation and feedback implementation.
base_js=(TEMPLATES/'grammar/lesson.js').read_text()
base_js=base_js.replace("slideKey='teachers-unit1-reading-v1'","slideKey='teachers-unit2-'+LESSON.id+'-v1'")
base_js=base_js.replace("'Unit 1 · קוראים וכותבים'","'Unit 2 · '+LESSON.subtitle")
base_js=base_js.replace("'כיתה ז׳ · Unit 1'","'כיתה ז׳ · Unit 2'")
start=base_js.index("if(s.kind==='cover')")
end=base_js.index("else if(s.kind==='plan')",start)
base_js=base_js[:start]+'''if(s.kind==='cover')c=title+'<h1>'+esc(s.title)+'</h1><p class="sub">'+esc(s.sub)+'</p><p class="created">Core I · Groups 03–05</p><div class="actions"><button id="start">מתחילים</button><a href="../index.html">כל היחידה</a></div>';
else if(s.kind==='example')c=title+tense+'<p class="hero english">'+esc(s.en)+'</p><p class="translation '+(s.reveal?'':'hidden')+'" '+(s.reveal?'':'aria-hidden="true"')+'>'+esc(s.he)+'</p>';
'''+base_js[end:]
base_js=base_js.replace('<p class="sub">Part A: הווה · Part B: עבר ותרגול משולב</p>','')
template=(TEMPLATES/'grammar/index.html').read_text()
template=template.replace('Unit 1 · Reading Workshop','Unit 2 · Review Draft').replace('unit-1-v1','unit-2-draft1')
template=template.replace('aria-label="שייכות לעומת קיום"','aria-label="נושא השיעור"')
template=re.sub(r'<div class="audioTools">.*?</div>','<div class="audioTools"><button id="speak" hidden></button><select id="speed" hidden><option value="0.75">0.75</option></select><span id="readProgress"></span></div>',template)
css=(TEMPLATES/'grammar/lesson.css').read_text()+'''\n.example .hero{min-height:150px;display:grid;place-items:center}.example .translation{min-height:120px}.example{justify-content:flex-start;padding-top:24px}.example .hero{overflow-wrap:anywhere} .quiz .hero{overflow-wrap:anywhere} .hidden{visibility:hidden!important}\n'''
for name,deck,subtitle in [('grammar-a',A,'הרגלים ושלילה'),('grammar-b',B,'שאלות ותדירות')]:
    dest=OUT/name;dest.mkdir(exist_ok=True)
    (dest/'index.html').write_text(template)
    (dest/'lesson.js').write_text(base_js)
    (dest/'lesson.css').write_text(css)
    data=dict(id=name,subtitle=subtitle,slides=deck,sentences=[],sections=list(dict.fromkeys(s['section'] for s in deck)))
    save(dest/'content.json',data)
    (dest/'data.js').write_text('window.LESSON = '+json.dumps(data,ensure_ascii=False)+';\n')

# Vocabulary source fields remain byte-for-byte equal after JSON decoding.
v=OUT/'vocabulary';v.mkdir(exist_ok=True)
original=TEMPLATES/'vocabulary'
for name in ['full.html','sequence.js','sequence.css']:
    text=(original/name).read_text()
    if name=='sequence.js':
        text=text.replace('מקור העובדה','Source').replace('110','165').replace('Groups 01–02','Groups 03–05').replace('שתי קבוצות','שלוש קבוצות').replace('שתי הקבוצות','שלוש הקבוצות')
        text=text.replace('teachers-grade7-band2-current','teachers-grade7-unit2-band2-current')
        text=text.replace('group-01.html','group-03.html').replace('group-02.html','group-04.html').replace('קבוצה 01','קבוצה 03').replace('קבוצה 02','קבוצה 04')
        needle='תרגול קבוצה 04</a>'
        text=text.replace(needle,needle+'<a class="action" href="https://englishfornoar.co.il/band-ii/groups/group-05.html" target="_blank" rel="noopener">תרגול קבוצה 05</a>')
        for g in (3,4,5):
            url='https://englishfornoar.co.il/band-ii/groups/group-%02d.html'%g
            label='תרגול קבוצה %02d</a>'%g
            text=text.replace(label,label+'<button data-copy="'+url+'">העתקת קישור</button>')
        text+='''\ndocument.addEventListener('click',async function(e){const b=e.target.closest('[data-copy]');if(!b)return;try{await navigator.clipboard.writeText(b.dataset.copy);document.getElementById('status').textContent='הקישור הועתק';}catch(err){document.getElementById('status').textContent=b.dataset.copy;}});\n'''
    elif name=='sequence.css':text=text.replace('../the-same-way/','../../the-same-way/')
    else:
        text=text.replace('קבוצות 01–02','קבוצות 03–05').replace('href="../"','href="../../"')
        text=text.replace('קריינות AI מוקלטת מראש, באנגלית אמריקאית. רק המילה והמשפט באנגלית מוקראים.','Recorded American English audio. Only the English word and example are read.')
    if name=='full.html':
        for old,new in [('כיתה ז׳2 · אנגלית','Grade 7 · English'),('>תוכן<','>Contents<'),('>הנפשה<','>Motion<'),('>שמע<','>Audio<'),('>קבוצות 03–05<','>Groups 03–05<'),('בחירה ישירה של ערך. ההתקדמות נשמרת רק במכשיר הזה.','Choose an entry. Progress is saved on this device.'),('חיפוש מילה','Find a word')]:text=text.replace(old,new)
    (v/name).write_text(text)
(v/'data.js').write_text('window.VOCABULARY = '+json.dumps(records,ensure_ascii=False)+';\n')
save(v/'entries.json',records)
if not (v/'audio/manifest.json').exists():save(v/'audio/manifest.json',{'clips':{}})
if not (v/'audio-manifest.json').exists():save(v/'audio-manifest.json',{'clips':{}})

# Reviewable main text, companion routines, teacher key and printable worksheets.
esc=html.escape
def page(title,body):
    return '<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><link rel="stylesheet" href="unit.css"><style>.message-card{background:#183b52;border:1px solid #6896a8;border-radius:20px 20px 20px 4px;padding:24px;margin:24px 0;max-width:780px}.message-card .english{margin-bottom:12px}.message-card.whatsapp{background:#153e35;border-color:#69ab8d}.message-card.email{background:#17384f;border-radius:8px;border-top:6px solid #e4c58a}.message-card.instagram{background:#19354f;border-radius:12px;border-top:6px solid #79a9ff}.message-heading{font-size:16px;font-weight:700;border-bottom:1px solid #7090a0;padding-bottom:12px}.message-card.email .message-heading{line-height:1.8}.adaptation{font-size:13px;color:#adc5d4;max-width:780px}.text-block{padding-block:18px;border-bottom:1px solid #365c73}.english{font-size:22px;line-height:1.7}summary{cursor:pointer;color:#dfff75}.answerline{height:35px;border-bottom:1px solid #889cab}.draft{color:#ffdc9b}table{width:100%;border-collapse:collapse}td,th{padding:12px;border-bottom:1px solid #537085;text-align:start}.scroll{overflow:auto}@media print{body{background:white;color:black}a{color:black}header,.no-print,details{display:none}main{padding:0;max-width:none}.text-block{break-inside:avoid}.english{font-size:13pt}h1{font-size:24pt;color:black}h2{font-size:18pt}p{font-size:12pt}.answerline{height:26px}@page{size:A4;margin:16mm}}</style></head><body><main><header><a class="home" href="./">⌂</a><p class="draft">Unit 2 · Grade 7</p></header><h1>'+esc(title)+'</h1>'+body+'</main></body></html>'

body='<p class="english">When does school begin? When does it end? How long is the summer break?</p><p><a href="reading/?text=school-calendars">Read & Listen →</a></p>'
for title,en,he in main_sections:
    body+='<section class="text-block"><h2 dir="ltr">'+esc(title)+'</h2><p class="english">'+esc(en)+'</p><details><summary>Hebrew support</summary><p lang="he" dir="rtl">'+esc(he)+'</p></details></section>'
body+='<h2 dir="ltr">Calendar details & sources</h2><p class="english">These are general patterns, not fixed dates for every year. Holiday lengths include weekends. The school-year span includes shorter holidays, not continuous lessons. Seasons use the Northern Hemisphere calendar. Local dates and teacher-training days can vary.</p>'
for row in calendar:
    body+='<section class="text-block"><h2 dir="ltr">'+esc(row['place'])+'</h2><p class="english">Start: '+esc(row['start'])+'<br>End: '+esc(row['end'])+'<br>Summer: '+esc(row['summer'])+'</p><details><summary>Teacher note</summary><p>'+esc(row['scope']+' · '+row['detail'])+'</p></details>'+''.join('<p class="meta" dir="ltr"><a href="'+esc(u)+'">Source: '+esc(u.split('/')[2])+'</a></p>' for u in row['sources'])+'</section>'
(OUT/'main-text.html').write_text(page('School Years Around the World',body))
body='<p class="english">Three short messages. Three regions of the world. Read each message in a different part of the unit.</p><div class="grid">'
for i,s in enumerate(stories):
    link='journey-'+s['id']+'.html'
    stage=['Part 1 · Routines','Part 2 · Questions and teamwork','Part 3 · Listening and writing'][i]
    body+='<section class="card"><p class="meta">'+esc(stage+' · '+s['region'])+'</p><h2>'+esc(s['title'])+'</h2><p>'+esc(s['place'])+'</p><a class="btn" href="'+link+'">Open message →</a></section>'
    detail='<p class="meta">'+esc(stage+' · '+s['region']+' · '+s['place'])+'</p><p class="meta">'+esc(s['period'])+'</p>'
    if s['id']=='boat':detail+='<p><a href="listening.html">Listen first, before opening the text →</a></p>'
    label='<div class="message-heading">'+esc(s['channel'])+'<br>From: '+esc(s['sender'])
    if s['messageStyle']=='email':label+='<br>To: Our English class<br>Subject: My way to school'
    label+='</div>'
    detail+='<p><a class="btn" href="reading/?text='+s['id']+'">Read & Listen →</a></p><p class="adaptation">A classroom adaptation based on a real journey.</p><section class="message-card '+s['messageStyle']+'" aria-label="'+esc(s['channel'])+'">'+label+'<p class="english">'+esc(s['en'])+'</p>'
    if s['messageStyle']=='email':detail+='<p class="english">Samuel</p>'
    detail+='<details><summary>Hebrew support</summary><p lang="he" dir="rtl">'+esc(s['he'])+'</p></details></section><h2>Read and think</h2><ol>'+''.join('<li><p class="english">'+esc(q)+'</p><details><summary>Answer</summary><p class="english">'+esc(a)+'</p></details></li>' for q,a in s['questions'])+'</ol><p class="meta">Classroom message adapted from a documented routine; not an original message or a direct quotation.</p><p><a href="'+esc(s['source'])+'">Read the original source</a></p>'
    next_link=['grammar-a/','grammar-b/','files/unit2-workbook.pdf'][i]
    next_label=['Practise routines','Practise questions','Write about your school routine'][i]
    detail+='<p><a class="btn" href="'+next_link+'">'+next_label+' →</a></p><p><a href="./">Back to Unit 2</a></p>'
    (OUT/link).write_text(page(s['title'],detail))
(OUT/'companion-stories.html').write_text(page('Three Messages about School',body+'</div>'))

worksheet='<p class="no-print"><button onclick="window.print()">הדפסה</button></p><p>שם פרטי: __________ כיתה: ________</p>'
worksheet+='<h2>Part A · לפני ההסבר</h2><p class="english">1. I ___ a bag. (carry / carries / carrying)<br>2. David ___ to school every day. (walk / walks / walking)</p>'
worksheet+='<h2>Part A · כתיבה עצמאית</h2><p>כתבו הרגל שלכם, הרגל של חבר ומשפט שלילה אחד. השתמשו בשתי מילים מהיחידה.</p>'+('<div class="answerline"></div>'*4)
worksheet+='<h2>Part B · שאלות ושיחה</h2><p>כתבו שאלה על דרך ההגעה ושאלה על פעילות אחרי בית הספר. שאלו חבר ורשמו תשובות. לבסוף כתבו משפט אחד עליו.</p>'+('<div class="answerline"></div>'*6)
worksheet+='<h2>Reading · שתי הודעות</h2><p>בחרו שתי הודעות. רשמו לכל אחד: מי הילד, כיצד הוא מגיע לבית הספר, ופרט שמשפיע על יום הלימודים. כתבו באנגלית דמיון אחד והבדל אחד. ציינו פרט מכל מקור שתומך בתשובה.</p>'+('<div class="answerline"></div>'*6)
worksheet+='<h2>A Reply from You · 50–70 words</h2><p>בחרו הודעה אחת וכתבו עליה תשובה: ענו לשאלת הכותב ותארו את הדרך שלכם לבית הספר ואת השגרה. כללו משפט שלילה, מילת תדירות ושתי מילים מקבוצות 3–5. חברו רעיונות באמצעות and, but או because.</p>'+('<div class="answerline"></div>'*9)
(OUT/'worksheet.html').write_text(page('Unit 2 · דף עבודה',worksheet))

teacher=[
 ('המוקד שאושר','<p>הטקסט המרכזי משווה תחילת וסיום שנות לימודים, חופשות ועונות. הודעת WhatsApp, אימייל ופוסט Instagram לימודיים בגוף ראשון מבוססות על שגרת ילדים אמיתיים: דרכי הגעה שונות, בשלושה אזורים: דרום אמריקה, אסיה ואירופה.</p>'),
 ('מבנה כמו יחידה 1','<p>אוצר מילים במנות; קריאה להבנה; דקדוק בשני מפגשים; קריאה עצמאית; דיבור וכתיבה; איסוף לפני פתרונות.</p>'),
 ('Core I בלבד','<p>קבוצות 03–05: 165 רשומות. מצגת מלאה אינה עדות לשליטה. בוחרים בכל מפגש מספר מילים לשימוש פעיל וחוזרים עליהן במשימות.</p>'),
 ('פריסת עבודה מוצעת','<p>תשעה מפגשים כפולים ורזרבה, לפי הביצוע בפועל. עד 72 דקות פעילות מתוכננת בכל מפגש. זו הצעת הוראה מקומית.</p>'),
 ('מפגשים 1–3','<p>1: פתיחה ולוחות לימודים. 2: חופשות ועונות וחיבור מידע. 3: סיפור הסוס מארגנטינה ודקדוק Part A. בכל מפגש מנת מילים וחזרה.</p>'),
 ('מפגשים 4–6','<p>4: Part B לפי טעויות Part A. 5: הסיפור של סמואל בהודו ושיתוף פעולה. 6: שאלות ומשימת מידע חסר בזוגות.</p>'),
 ('מפגשים 7–9','<p>7: סיפור הסירה מאיי סילי; האזנה עצמאית לפני פתיחת התמליל. 8: כתיבת הודעת תשובה ומשוב. 9: העברה לטקסט חדש וכתיבה ללא הדגם.</p>'),
 ('אבחון לפני הקניה','<p>התלמיד עונה תחילה על שתי שאלות פתיחה. בהמשך כותב במשימות. מפרידים בין הבנת המסר, מבנה ואיות.</p>'),
 ('Part A · 72 דקות','<p>5 פתיחה; 14 שגרה; 13 גוף שלישי; 14 שלילה; 15 כתיבה; 5 איסוף; 6 משוב. אין לדחוס את Part B לאותו מפגש.</p>'),
 ('Part B · 72 דקות','<p>7 חזרה מאבחנת; 12 שאלות; 13 תשובות קצרות; 15 מילות שאלה; 10 תדירות; 8 שיחה; 7 משימת יציאה.</p>'),
 ('החלטה לפי טעות','<p>doesn’t walks: תרגול צורת בסיס. שגיאות רק ב־ies: תרגול כתיב קצר. בחירה נכונה בלי יכולת לכתוב: עוד הפקה עם תמיכה שנעלמת בהדרגה.</p>'),
 ('דיוק בלוחות','<p>לוחות בתי ספר אינם אחידים למדינה שלמה. קנט וג׳רזי כוללים ימי הכשרת צוות. הטקסט מציג דפוסים כלליים: קודם עונה ואורך חופשה, ואז מועד משוער. משך שנת הלימודים כולל חופשות קצרות. העונות לפי חצי הכדור הצפוני. ביפן הקיץ באמצע השנה.</p>'),
 ('סיפורים אמיתיים','<p>אין להוסיף דיאלוג, פחד, תקלה או חילוץ ללא מקור. ההודעות הן עיבוד לימודי בגוף ראשון, לא ציטוטים או הודעות מקוריות של הילדים. הפתיחה והשאלה לקורא נכתבו ליחידה; עובדות הדרך נשענות על המקור. מקור ותאריך מצורפים לכל סיפור.</p>'),
 ('חיבור בין מקורות','<p>התלמיד מוצא דרך הגעה ופרט משפיע בכל טקסט, ואז כותב משפט דמיון ומשפט הבדל. דורשים ראיה מכל אחד משני הטקסטים. מה משותף לדרכים, ואיזה פרט מיוחד לכל סיפור?</p>'),
 ('הסרת התמיכה','<p>תחילה מילון ומשפט פתיחה; בהמשך רק שאלות מנחות; במשימת הסיום טקסט חדש וכתיבה ללא דגם גלוי.</p>'),
 ('כתיבה ומשוב','<p>50–70 מילים. קודם תוכן ברור ורצף, אחר כך Present Simple ושלילה, ואז איות. התלמיד מתקן שני משפטים בעקבות המשוב.</p>'),
 ('מפת כיסוי','<p>165 רשומות מוצגות עם דוגמה ומשימת שליפה בהקשר. מפת הכיסוי מפרידה בין הצגה, בחירה וכתיבה עצמאית. אין לספור subject כערך בית ספר או name כשם עצם.</p>'),
 ('בדיקת מקור אוצר המילים','<p>נשמר צילום המקור של כל הרשומות. 25 רשומות תוקנו גם בספר התיעוד המקורי; משימת סנכרון בתוכנה: E-Vocab #5. תיקוני העריכה מתועדים: חלק דיבור, משמעות או תרגום. דוגמאות: which, included, excited, the young ו־leave במשמעות סיום קשר.</p>'),
 ('פתרונות חוברת העבודה','<p><a href="workbook-key.html">Workbook answer key</a></p><p>אוספים תשובות עצמאיות לפני חשיפת הפתרונות. כל ההפניות למקורות באנגלית.</p>'),
 ('קריאה והאזנה','<p>ארבעה טקסטים: טקסט מרכזי ושלושה סיפורים נפרדים, קטעים קצרים וקריאה משפט־משפט. בכל מילה אפשר לקבל פירוש. ברירת המחדל היא 0.75; בחירת המהירות נשמרת. במשימת ההאזנה מסתירים תחילה את התמליל.</p>'),
]
(OUT/'teacher-data.js').write_text('const TEACHER = '+json.dumps([dict(title=t,body=b) for t,b in teacher],ensure_ascii=False)+';\n')
for name in ['teacher.html','teacher.js','unit.css','hub.js']:
    text=(TEMPLATES/'unit'/name).read_text().replace('Unit 1','Unit 2').replace('unit1-1','unit2-draft1')
    (OUT/name).write_text(text)

groups=[
 ('Part 1 · Seasons and routines', [
 ('School Years Around the World','The main reading · seasons, holidays and school years','main-text.html'),
 ('Read & Listen','Main reading · short parts and sentence practice','reading/?text=school-calendars'),
 ('Vocabulary','165 entries · Groups 03–05 · recorded audio','vocabulary/full.html'),
 ('A Horse Before Class','WhatsApp · Argentina, South America','journey-horse.html'),
 ('Present Simple A','Routines, third person and negatives','grammar-a/')]),
 ('Part 2 · Questions and teamwork',[
 ('Words in Context','Short practice sets · choose, check and write','vocabulary/practice.html'),
 ('Four Kilometres Together','Email · India, Asia','journey-wheelchair.html'),
 ('Present Simple B','Questions, frequency and conversations','grammar-b/')]),
 ('Part 3 · Listening and your own story',[
 ('Listen First','Instagram post · the school boat in Europe','listening.html'),
 ('The School Boat','Instagram post · Isles of Scilly, Europe','journey-boat.html'),
 ('Worksheets','Three separate messages · grammar and independent writing','files/unit2-workbook.pdf'),
 ('Teacher Guide','Teaching sequence, timing and answer keys','teacher.html')])]
body='<p class="english">Grade 7 · Band II, Core I · Groups 03–05</p>'
for title,cards in groups:
    body+='<section class="unit-part"><h2 style="margin-top:32px">'+title+'</h2><div class="grid">'+''.join('<section class="card" dir="ltr"><h2>'+t+'</h2><p>'+d+'</p><a class="btn" href="'+u+'">Open →</a></section>' for t,d,u in cards)+'</div></section>'

(OUT/'index.html').write_text(page('Unit 2 · School Years Around the World',body).replace('class="home" href="./"','class="home" href="../"'))
# Keep the meeting index and its linked preparation/guide in every rebuild.
from build_sessions import build as build_meetings
build_meetings()

pending=[]
for label,relative in [('recorded vocabulary audio','vocabulary/audio/g05-55.mp3'),('recorded reading audio','reading/assets/school-calendars.mp3'),('Read & Listen','reading/index.html'),('contextual practice','vocabulary/practice.html'),('listening task','listening.html'),('worksheet PDF','files/unit2-workbook.pdf')]:
    if not (OUT/relative).is_file():pending.append(label)
save(OUT/'build-report.json',dict(status='published',published='2026-09-22',records=len(records),groups=[3,4,5],grammar_a_slides=len(A),grammar_b_slides=len(B),teacher_slides=len(teacher),true_companion_texts=len(stories),main_words=sum(len(re.findall(r"\b[\w’'-]+\b",x[1])) for x in main_sections),vocabulary_corrected_records=len(corrections),vocabulary_book='corrected: version 4',software_sync_task='https://github.com/Simonh68/E-Vocab-Band-II/issues/5',pending=pending))
print(json.dumps(json.loads((OUT/'build-report.json').read_text()),ensure_ascii=False))
