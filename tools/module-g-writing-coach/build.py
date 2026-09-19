from pathlib import Path
from html import escape
import json, shutil
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade11/module-g-writing-coach'
GEM='https://gemini.google.com/gem/d675ebc8760b'
slides=[]
def en(t,cls='example'): return f'<p class="en {cls}" lang="en" dir="ltr">{t}</p>'
def he(t,cls='instruction'): return f'<p class="{cls}">{t}</p>'
def add(title,body,kind='',pair='',tense=''):
    slides.append(dict(title=title,body=body,kind=kind,pair=pair,tense=tense))
def writepair(title,prompt,starter,answer,pair,tense=''):
    base=he(prompt)+en(starter)
    for reveal in [False,True]:
        slot=en(answer,'possible-answer')
        add(title,base+f'<div class="answer-slot"{("" if reveal else " aria-hidden=\"true\"")}> <div class="reveal-content{("" if reveal else " concealed")}">{slot}</div></div>','writing',pair,tense)
def quiz(title,before,after,choices,correct,pair,hint,tense=''):
    for reveal in [False,True]:
        blank=f'<span class="gap"><span class="{("solved" if reveal else "concealed")}">{correct}</span></span>'
        opts=''.join(f'<span class="choice">{escape(x)}</span>' for x in choices)
        add(title,en(before+blank+after)+f'<div class="choices en" lang="en" dir="ltr">{opts}</div>'+he(hint)+f'<div class="answer-slot mini"><p class="reveal-content{("" if reveal else " concealed")}">התשובה: <b class="en" lang="en" dir="ltr">{correct}</b></p></div>','quiz',pair,tense)
def pause(image,caption):
    add('התנחתא',f'<img class="break-image" src="assets/{image}" alt="חתול מאויר עם מחברת וציוד לימוד"><div class="break-caption en" lang="en" dir="ltr">{caption}</div>','break')
add('כיתה י״א · 5 יחידות',he('ברוכים הבאים','welcome')+'<h1 class="cover-title">מאמן כתיבה<br>למודול G</h1>'+en('Module G Writing Coach','cover-sub'),'cover')
add('איך מתחילים',he('פותחים את המאמן ומקלידים:')+he('מתחילים','command')+he('קוראים את הנושא וכותבים משפט אחד באנגלית.')+he('אם אין גישה, פונים למורה.','note'))
add('מילים מוכרות לתוכן',en('games · help · use · job · learn')+he('בוחרים מילה מוכרת שמתאימה בדיוק לרעיון.')+he('משפט פשוט ותקין נשאר פשוט.','note'))
add('ביטויים שחוזרים בחיבורים',en('I claim that…','possible-answer')+en('On the one hand,… / On the other hand,…','possible-answer')+en('For example,… / In conclusion,…','possible-answer')+he('זוכרים את המבנה; בכל חיבור משלימים רעיון שמתאים לנושא.','note'))
writepair('פתיחה · עבודה אחרי הלימודים','הנושא: Should teenagers have an after-school job? הציגו אותו בלי עמדה.','Many teenagers…','Many teenagers want to work after school.','opening','הווה')
writepair('עמדה','כתבו את דעתכם על עבודה אחרי הלימודים.','I claim that…','I claim that a small job can be useful if students have enough time to study.','opinion')
quiz('since · מציגים סיבה','Students feel tired ',' they do not sleep enough.',['however','since','for example'],'since','reason','בחרו מילת קישור שמציגה סיבה.','הווה')
pause('serious-cat.webp','A short break')
quiz('תיקון קטן','Students ',' time for homework.',['needs','needing','need'],'need','repair','הנושא ברבים. איזו צורת פועל מתאימה?','הווה')
add('ארבע פסקאות','<div class="plan"><div><b>1</b><span>פתיחה ועמדה</span></div><div><b>2</b><span>הצד האחר + הסבר</span></div><div><b>3</b><span>העמדה שלי + דוגמה</span></div><div><b>4</b><span>מסקנה</span></div></div>'+he('120–140 מילים. בנושאי תיאור המאמן מתאים את פסקאות הגוף.','note'))
add('המבנים שכבר למדנו',en('If they work every day, they will have less time for homework.','possible-answer')+en('Some students have learned to save money.','possible-answer')+en('Enough time should be left for sleep.','possible-answer')+he('המאמן מתרגל כל מבנה בנפרד, בתוך רעיון פשוט.','note'))
add('כשצריך עזרה','<div class="commands"><div><b>רמז</b><span>עזרה קטנה למשפט הנוכחי</span></div><div><b>למה</b><span>הסבר קצר לתיקון</span></div><div><b>החיבור שלי</b><span>הטקסט וספירת המילים</span></div></div>'+he('נושא הדוגמה של המאמן שונה מהנושא שלכם. לוקחים את המבנה.','note'))
essay=[
'Many teenagers want to work after school. I claim that a small job can be useful if students have enough time to study.',
'On the one hand, a job takes time. If students work every day, they will have less time for homework. They may also feel tired in class since they do not sleep enough.',
'On the other hand, work can help students learn new skills. Some students have learned to save money from their jobs. For example, they can use this money to buy books or pay for school trips. They also learn to work with other people and arrive at work on time.',
'In conclusion, I think students can work a few hours a week. However, enough time should be left for schoolwork and sleep.']
count=sum(len(p.split()) for p in essay)
assert 120<=count<=140
add('חיבור לדוגמה','<p class="essay-ruler-key">מילים בכל שורה ↓</p><div class="essay essay-counted" lang="en" dir="ltr">'+''.join('<p>'+p+'</p>' for p in essay)+f'</div><p class="essay-total">סך הכול: <bdi data-essay-total>{count}</bdi> מילים</p>','essay-slide')
add('לפני שמסיימים','<div class="checklist"><p>עניתי על הנושא?</p><p>הסברתי את הרעיון והוספתי דוגמה?</p><p>ארבע פסקאות ו־120–140 מילים?</p></div>'+he('מאמתים את הספירה ב־Word או ב־Google Docs.','note'))
add('כתיבה עצמאית',he('35 דקות לכתיבה','command')+he('כותבים במאמן משפט אחד בכל פעם.')+he('אחר כך: 10 דקות לקריאה ולתיקון.','note'))
add('בדיקת יציאה',he('בחרו משפט אחד שתיקנתם.')+he('הסבירו מה השתנה ולמה.')+he('לתרגול חדש מקלידים ״נביא״. טיוטה שטרם הושלמה ממשיכים בפעם הבאה.','note'))
sections=[]
for i,s in enumerate(slides,1):
    meta='' if s['kind']=='break' else f'<header class="slide-meta"><h2 class="eyebrow">{s["title"]}</h2><div class="tense">{s["tense"]}</div></header>'
    sections.append(f'<section class="slide {s["kind"]}" data-pair="{s["pair"]}" aria-label="שקף {i}: {s["title"]}" hidden><div class="frame">{meta}{s["body"]}</div></section>')
html='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>מאמן כתיבה למודול G — כיתה י״א | Teachers</title><link rel="stylesheet" href="assets/deck.css"><link rel="stylesheet" href="lesson.css?v=linewords1"></head><body>
<a class="home" href="../five-units/" aria-label="חזרה לספריית כיתה י״א"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 11 12 3l9 8M5 10v11h5v-7h4v7h5V10"/></svg></a>
<div class="coach-access"><span>לתרגול כתיבה עם משוב</span><a href="GEM" target="_blank" rel="noopener">פתיחת המאמן ↗</a></div>
<main class="stage" tabindex="-1">SLIDES</main>
<nav class="nav" aria-label="ניווט במצגת"><div class="nav-group"><button data-step="-1" aria-label="השקף הקודם">←</button><button data-step="1" aria-label="השקף הבא">→</button></div><div class="progress" id="counter" aria-live="polite"></div><div class="lesson-links"><a href="teacher.html">למורה</a></div></nav><div class="progress-track"><div class="progress-fill"></div></div><script src="assets/deck.js"></script><script src="assets/essay-ruler.js?v=linewords1"></script></body></html>'''.replace('GEM',GEM).replace('SLIDES','\n'.join(sections))
OUT.joinpath('index.html').write_text(html)
OUT.joinpath('lesson-data.json').write_text(json.dumps({'gem':GEM,'slides':slides,'essay':essay,'count':count},ensure_ascii=False,indent=2))
# Pin shared presentation engine and styles so the package is self-contained.
css=(ROOT/'assets/lesson-decks/deck.css').read_text()
css=css[css.index(':root'):]
css='@font-face{font-family:Heebo;src:url(Heebo.ttf);font-weight:100 900;font-display:swap}@font-face{font-family:Nunito;src:url(Nunito.ttf);font-weight:100 900;font-display:swap}\n'+css
OUT.joinpath('assets/deck.css').write_text(css)
shutil.copyfile(ROOT/'assets/lesson-decks/deck.js',OUT/'assets/deck.js')
print(f'Built {len(slides)} slides; essay: {count} words; paragraphs: {[len(p.split()) for p in essay]}')

