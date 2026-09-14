from pathlib import Path
import json,html,shutil,re
R=Path(__file__).parent
repo=R.parents[1]
out=repo/'grade8/monkey-festival'
d=json.loads((out/'lesson.json').read_text())
e=html.escape
def inline(text):
    value=e(text).replace('\n','<br>')
    value=re.sub(r'\d{1,2}:\d{2}[–-]\d{1,2}:\d{2}', lambda m: '<bdi dir="ltr">'+m.group()+'</bdi>', value)
    return re.sub(r'\(\d{1,2}\.\d{1,2}\.\d{4}\)', lambda m: '<bdi dir="ltr" class="gregorian">'+m.group()+'</bdi>', value)
def texttag(tag,cls,text):
    if not text:return ''
    english=not any('\u0590'<=c<='\u05ff' for c in text)
    return f'<{tag} class="{cls}'+(' en' if english else '')+'"'+(' lang="en" dir="ltr"' if english else ' lang="he" dir="rtl"')+'>'+inline(text)+f'</{tag}>'
sections=[]
for s in d['slides']:
    kind=s['kind']; n=s['n']
    cl={'notice':'transition notice','schedule':'transition schedule','question':'transition','reading':'reading','vocab':'vocab','qa':'qa','cover':'cover','break':'break'}[kind]
    if n==3:cl+=' dated-schedule'
    if s.get('answer') or s.get('meaning'):cl+=' reveal'
    attrs=f'id="slide-{n}" class="slide {cl}'+(' active' if n==1 else '')+f'" data-section="{s["section"]}" role="group" aria-roledescription="שקף" aria-label="{n} מתוך 70"'+(' hidden' if n>1 else '')
    if s.get('pair'):attrs+=f' data-pair="{s["pair"]}"'
    meta='<div class="slide-meta">'+texttag('p','eyebrow',s.get('label') or {'reading':s['title'],'vocab':'אוצר מילים','qa':'תרגול','break':''}.get(kind,'כיתה ח׳ · הכנה למבחן'))+texttag('p','tense',s.get('tense',''))+'</div>'
    b=meta
    if kind=='break':b=f'<img class="break-image" src="assets/{s["asset"]}.jpg" alt="איור משעשע של קוף בפסטיבל" width="1672" height="941">'
    elif kind=='vocab':
        b+=texttag('h1','word',s['title'])+texttag('p','example',s['body'])+'<div class="translation-slot">'+texttag('p','meaning',s.get('meaning',''))+texttag('p','translation',s.get('translation',''))+'</div>'
    elif kind=='qa':
        b+=texttag('h1','question',s['title'])+texttag('p','clue',s.get('hint',''))+'<div class="answer-slot">'+texttag('p','possible-answer',s.get('answer',''))+'</div>'
    elif kind=='reading':b+=texttag('p','story-sentence',s['body'])
    else:
        b+=texttag('h1','cover-title' if kind=='cover' else 'part-title',s['title'])
        b+=texttag('p','part-he',s.get('body',''))+texttag('p','part-he',s.get('sub',''))
        if s.get('items'):b+='<div class="lesson-items">'+''.join(texttag('p','lesson-item',t) for t in s['items'])+'</div>'
        b+=texttag('p','instruction',s.get('hint',''))
        if s.get('links'):b+='<div class="resource-links">'+''.join(f'<a href="{e(l["href"])}" target="_blank" rel="noopener">{e(l["label"])}</a>' for l in s['links'])+'</div>'
    sections.append('<section '+attrs+'><div class="frame">'+b+'</div></section>')
page='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>The Monkey Festival · כיתה ח׳ · Teacher</title><link rel="stylesheet" href="../../assets/lesson-decks/deck.css?v=20260910f"><link rel="stylesheet" href="lesson.css?v=20260914b"></head><body>
<a class="home" href="../" aria-label="חזרה לחומרי כיתה ח׳"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5M5.5 9v11h13V9M9 20v-6h6v6"/></svg></a>
<nav class="lesson-shortcuts" aria-label="קיצורי דרך"><a href="#slide-2">המבחן</a><a href="#slide-8">מילים</a><a href="#slide-32">קריאה</a><a href="#slide-60">עבודה</a><a href="#slide-62">12:25</a><a href="files/monkey-festival.pptx" download>PPTX</a></nav>
<main class="stage" aria-label="The Monkey Festival">'''+''.join(sections)+'''</main>
<nav class="nav" aria-label="ניווט שקפים"><div class="nav-group"><button data-step="-1" aria-label="השקף הקודם">↑</button><button data-step="-1" aria-label="השקף הקודם">←</button><button data-step="1" aria-label="השקף הבא">→</button><button data-step="1" aria-label="השקף הבא">↓</button></div><output id="counter" class="progress" aria-live="polite"></output></nav><div class="progress-track" aria-hidden="true"><div class="progress-fill"></div></div><script src="../../assets/lesson-decks/deck.js?v=20260910f"></script></body></html>'''
(out/'index.html').write_text(page)
(out/'lesson.css').write_text('''
.lesson-shortcuts{position:fixed;top:19px;right:20px;left:86px;z-index:12;display:flex;gap:14px;align-items:center;justify-content:flex-start;flex-wrap:wrap}
.lesson-shortcuts a{color:var(--cyan);font-size:14px;font-weight:800;text-decoration:none;background:#07111fec;padding:6px 3px}.lesson-shortcuts a:hover{text-decoration:underline}
.clue{font-size:21px;color:var(--cyan);text-align:left;direction:ltr;font-family:Nunito,Arial,sans-serif}
.qa .frame{grid-template-rows:auto auto auto minmax(140px,auto)}.qa .question{font-size:clamp(29px,3.7vw,52px)}.qa .possible-answer{font-size:clamp(26px,3.2vw,42px)}
.reading .story-sentence{font-size:clamp(27px,3.1vw,43px);line-height:1.5;font-weight:700;text-wrap:pretty}
.reading .slide-meta{margin-bottom:20px}.reading .frame:before{margin-bottom:18px}
.notice .part-title,.schedule .part-title{font-size:clamp(34px,5.2vw,68px)}.part-title:not(.en){font-family:Heebo,Arial,sans-serif}.cover-title:not(.en){font-family:Heebo,Arial,sans-serif}
.lesson-items{margin:25px auto 0;max-width:1000px}.lesson-item{font-size:clamp(23px,2.7vw,35px);line-height:1.45;margin:12px 0;text-wrap:balance}.instruction{font-size:clamp(19px,2vw,26px)}
.break .frame{height:100%}.resource-links{margin:12px auto}.resource-links a{font-size:22px}.cover:after{display:none}
@media(max-width:760px){.lesson-shortcuts{top:15px;right:12px;left:65px;gap:10px}.lesson-shortcuts a{font-size:11px;padding:6px 1px}.reading .story-sentence{font-size:clamp(24px,6vw,34px)}.qa .question{font-size:clamp(26px,6.7vw,37px)}.qa .possible-answer{font-size:clamp(23px,5.6vw,32px)}.lesson-item{font-size:24px}.clue{font-size:18px}}
@media(max-height:570px){.reading .story-sentence{font-size:clamp(23px,4.6vh,32px);line-height:1.36}.lesson-items{margin-top:15px}.lesson-item{font-size:23px;margin:8px 0}.notice .part-title,.schedule .part-title{font-size:40px}.qa .frame{grid-template-rows:auto auto auto minmax(110px,auto);gap:8px}.qa .question{font-size:32px}.qa .possible-answer{font-size:27px}.clue{font-size:18px}.lesson-shortcuts{top:12px}.instruction{font-size:20px;margin-top:14px}}
.gregorian{white-space:nowrap;unicode-bidi:isolate}
.dated-schedule .lesson-items{margin-top:18px}
.dated-schedule .lesson-item{font-size:clamp(23px,2.35vw,31px);line-height:1.4;margin:14px 0}
.dated-schedule .instruction{font-size:clamp(18px,1.8vw,24px);margin-top:16px}
@media(max-width:760px){.dated-schedule .part-title{font-size:36px}.dated-schedule .lesson-item{font-size:23px;margin:12px 0}}
@media(max-height:570px){.dated-schedule .part-title{font-size:34px}.dated-schedule .lesson-item{font-size:23px;margin:8px 0}.dated-schedule .instruction{font-size:19px}}
@media print{.lesson-shortcuts{display:none}}
''')
home=(repo/'grade8/index.html').read_text()
card='''
    <a class="card" href="monkey-festival/?v=20260914b">
      <span class="index">03</span><span class="type">EXAM PREPARATION</span>
      <h2 lang="en" dir="ltr">The Monkey Festival</h2>
      <p>שיעור הכנה בזום ביום שני, ג׳ בתשרי תשפ״ז (14.9.2026): טקסט מהארכיון, אוצר מילים ושאלות. המבחן ביום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026).</p>
      <div class="open">פתיחת המצגת <span>←</span></div>
    </a>
    <div class="downloads"><a href="monkey-festival/files/monkey-festival.pptx" download>PPTX</a><a href="monkey-festival/files/monkey-festival-practice.pdf" target="_blank" rel="noopener">טקסט ודף תרגול · PDF</a><a href="monkey-festival/teacher.html" target="_blank" rel="noopener">תסריט ומפתח תשובות למורה</a></div>
'''
if 'monkey-festival/' in home:
    home,count=re.subn(r'<a class="card" href="monkey-festival/.*?</a>\s*<div class="downloads">.*?</div>',card.strip(),home,flags=re.S)
    assert count==1,count
else:
    home=home.replace('  </main>',card+'  </main>')
(repo/'grade8/index.html').write_text(home)
key='''<h1>The Monkey Festival · תסריט למורה</h1><p>יום שני, ג׳ בתשרי תשפ״ז (14.9.2026) · כיתה ח׳2</p>
<p>המצגת כוללת 70 שקפים. שקפים 1–59 מיועדים לזום הראשון, 60–61 לעבודה העצמאית, 62–70 לסיכום. לא מקריאים כל שקף: חשיפת מילים היא מהירה, והפסקות התמונה אורכות 15–20 שניות.</p>
<h2>הפתיחה לתלמידים</h2><p>המבחן יהיה ביום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026).</p><p lang="en" dir="ltr"> We have three double lessons planned before the test, including today. The second lesson may change because of a school event. Today we will practise with a reading text from an earlier Grade 8 test. We will also review vocabulary. Please keep your text and a notebook ready.</p>
<h2>זמנים מוצעים</h2><ul><li>11:10–11:14 · שקפים 1–7: מועד המבחן, מפגשים ומטרת השיעור.</li><li>11:14–11:24 · שקפים 8–30: שמונה מילות קריאה ושלוש מילים מקבוצה 01.</li><li>11:24–11:46 · שקפים 31–56: קריאה מודרכת, שאלות, תשובות והתנחתות.</li><li>11:46–11:50 · שקפים 57–59: בדיקה והוראות לעבודה.</li><li>11:50–12:00 · הפסקה.</li><li>12:00–12:25 · שקפים 60–61: עבודה עצמאית.</li><li>12:25–12:32 לכל היותר · שקפים 62–70: קושי אחד מהכיתה, תיקון משפט ותזכורת.</li><li>עד 12:40 · תיקון והגשה בערוץ הכיתתי הרגיל.</li></ul>
<p>אם הקריאה דורשת יותר זמן, מדלגים על תרגול ההרחבה בשקפים 55–56 ומשתמשים בשקף 57 לסגירת המפגש. המטרה היא התנסות בהבנה ובתשובה, ולא הספק מכני של שקפים.</p>
<h2>מה מאומת ומהו תכנון הוראה</h2><p>לפי הלוח שפורסם, המבחן ביום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026). שלושת המפגשים המתוכננים הם: יום שני, ג׳ בתשרי תשפ״ז (14.9.2026), יום חמישי, ו׳ בתשרי תשפ״ז (17.9.2026), יום שני, כ״ד בתשרי תשפ״ז (5.10.2026). המפגש השני טעון בדיקה בגלל מופע סליחות. מצגת הפתיחה מגדירה התחלה בקבוצה 01. לא נמצא מפרט מלא למבחן הראשון. אין להסיק שהטקסט הזה יופיע במבחן הקרוב או שכל המילים בטקסט שייכות לקבוצה 01.</p>
<p>המבחן נמצא בתיקיית התשפו / ח / מבחן אקטובר. תאריך השינוי של קובץ המקור הוא 21.10.2024. זהו הקובץ שבתיקיית השנה שעברה, אך אין בכך לבדו תיעוד של העברתו בפועל בתאריך מסוים.</p>
<h2>מפתח העבודה העצמאית</h2><p dir="ltr">A1. They are on the street corner. [C]<br>A2. Many people are dressed like monkeys. [B]<br>A3. The writer hopes to see a food fight. [F]<br>A4. The monkeys can cause trouble and take people’s things. [D, also G]<br>A5. Monkeys helped Prince Rama in the story, so people believe they can bring good luck. [H–I]</p>
<p dir="ltr">B1. I am at the festival.<br>B2. I like the festival.<br>B3. I can be at the festival.</p>
<p dir="ltr">C1. However<br>C2. care</p><p>הרחבה D: תשובות שונות אפשריות. לקבל הסבר קצר עם פרט מהטקסט. הבדיקה היא של קשר בין הדעה לראיה, לא של הבחירה כן/לא.</p>
<h2>בדיקה מהירה</h2><p>שאלות A: נקודה לתוכן ונקודה לפסקה מתאימה, 10 נקודות. B: שתי נקודות למשפט מובן ותקין, 6 נקודות. C: נקודה לכל השלמה, 2 נקודות. סך הכול 18 נקודות לתרגול אבחוני; אין חובה לתת ציון. טעויות באיות אינן מוחקות תוכן נכון בחלק A. אין זה מחוון המבחן הקרוב.</p>
<h2>התאמות</h2><p>למי שמתקשה: להפנות לאותיות הפסקאות, להשתמש בבנק המילים שבחלק C ולתת בעל פה התחלות משפטים לפי הצורך. להתחיל בשלוש שאלות A הראשונות ובמשפט B1. להוסיף בהדרגה. למתקדמים: לענות ללא הסתכלות בשקפי הפתרונות ולהוסיף את D. לא ללמד נושא דקדוקי חדש רק כדי למלא זמן.</p>
<h2>הערות על המקור</h2><p>נוסח הקריאה נשמר. שורת ניווט לאתר והערות שוליים חסרות הוסרו. נוספו אותיות פסקאות, ופסקה ארוכה חולקה לשתיים. בשאלת האוכל במבחן המקורי הופיעה הפניה לשורות שאינה מתאימה לתשובה; במצגת ההפניה היא לפסקה F. חלק משאלות ההבנה נוסחו מחדש באנגלית טבעית תוך שמירה על המיומנות. התיאורים על Prince Rama מוצגים כסיפור וכאמונת תושבים לפי הטקסט.</p>
<h2>מקורות</h2>'''
key+='<ul>'+''.join(f'<li><a href="{e(v)}">{e(k)}</a></li>' for k,v in d['sources'].items())+'</ul><h2>תסריט לפי שקף</h2>'
for s in d['slides']:
    key+=f'<h3>{s["n"]}. {e(s["title"] or "התנחתות חזותית")}</h3><p>{e(s.get("notes",""))}</p>'
    if s.get('answer'):key+=f'<p dir="ltr">{e(s["answer"])}</p>'
key=re.sub(r'\d{1,2}:\d{2}[–-]\d{1,2}:\d{2}', lambda m: '<bdi dir="ltr">'+m.group()+'</bdi>', key)
(out/'teacher.html').write_text('<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>תסריט למורה · The Monkey Festival</title><style>body{font:18px/1.7 Arial,sans-serif;max-width:900px;margin:auto;padding:32px;background:#f7f7f2;color:#07111f}a{color:#075873}h1,h2{line-height:1.3}h2{margin-top:2em}p[dir=ltr]{text-align:left}li{margin:.5em 0}bdi{white-space:nowrap}</style><a href="./">פתיחת המצגת</a>'+key+'</html>')
print('HTML slides:',len(sections))
