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
add('איך מתחילים',he('פותחים את המאמן ומקלידים:')+he('מתחילים','command')+he('קוראים את הנושא שנבחר וכותבים משפט אחד באנגלית.')+he('אם אין גישה, פונים למורה לפני התרגול.','note'))
add('מה עושים בכל תור','<div class="steps"><div><b>1</b> קוראים את המשימה</div><div><b>2</b> כותבים משפט באנגלית</div><div><b>3</b> קוראים משוב ומתקנים</div></div>'+he('המאמן מסביר בעברית; הרעיונות והניסוח שלכם.','note'))
add('ארבע פסקאות בחיבור דעה','<div class="plan"><div><b>1</b><span>פתיחה ניטרלית + עמדה</span></div><div><b>2</b><span>הצד האחר + הסבר ודוגמה</span></div><div><b>3</b><span>העמדה שלי + הסבר ודוגמה</span></div><div><b>4</b><span>מסקנה</span></div></div>'+he('יעד התרגול: 120–140 מילים. הרחבות נכנסות לפסקאות הגוף.','note'))
add('נושא ההדגמה',en('Should teenagers have an after-school job?')+he('חשבו על יתרון אחד ועל קושי אחד.')+he('זו הדגמה כיתתית. במאמן עשוי להיבחר נושא אחר.','note'))
add('לומדים תבנית מנושא אחר',he('נושא הדוגמאות של המאמן: גיל קבלת טלפון')+en('Many parents discuss when children should get their first cellphone.')+he('לוקחים את המבנה וכותבים רעיון על עבודה אחרי הלימודים.','note'))
writepair('משפט פתיחה','מציגים את הנושא בלי להביע עמדה. כתבו משפט משלכם.','Many teenagers…','Many teenagers consider getting a job while they are still at school.','opening','הווה')
writepair('משפט עמדה','בחרו: בעד, נגד, או בעד בתנאים מסוימים. נסחו את עמדתכם.','I claim that…','I claim that limited working hours can help students prepare for adult life.','opinion','הווה')
pause('serious-cat.webp','A short break')
quiz('משוב שמאפשר לתקן','I claim that teenagers ',' time for homework.',['needs','need','needing'],'need','repair','הנושא ברבים. איזו צורת פועל מתאימה?','הווה')
writepair('פסקה שנייה: הצד האחר','אנחנו בעד עבודה מוגבלת. איזה קושי מי שחושב אחרת עשוי להציג?','On the one hand,','On the one hand, working after school can leave teenagers tired.','opposite')
quiz('תנאי ראשון','If they ',' every evening, they will have less time for homework.',['will work','working','work'],'work','conditional','מה מתאים אחרי If בתנאי ראשון?')
writepair('פסקה שלישית: העמדה שלי','כעת חוזרים לעמדה שלנו. איזה יתרון מצדיק עבודה מוגבלת?','On the other hand,','On the other hand, a small job can teach practical skills.','support')
quiz('ניסיון שמשפיע על ההווה','Many students have ',' to manage money through work.',['learn','learned','learning'],'learned','perfect','אחרי have או has נשתמש בצורת V3.','הווה')
pause('however-cat.webp','Another point of view')
writepair('הרחבה שמוסיפה משמעות','הטענה: עבודה מלמדת לנהל כסף. במה זה מועיל בחיי היום־יום?','For example,…','Saving part of their pay can help them understand the difference between needs and wishes.','expand')
add('תקועים באמצע','<div class="commands"><div><b>רמז</b><span>מקבלים מעט עזרה ומנסים שוב</span></div><div><b>למה</b><span>מבקשים הסבר לתיקון</span></div><div><b>החיבור שלי</b><span>רואים את הטקסט ואת הספירה</span></div><div><b>איפה אני</b><span>מזכירים מה הצעד הבא</span></div></div>'+he('אלה פקודות שמקלידים בשיחה.','note'))
writepair('פסקה רביעית: מסקנה','חוזרים לעמדה ומסיימים בלי טיעון חדש. כתבו מסקנה.','In conclusion,…','In conclusion, an after-school job can be beneficial when school remains the main priority.','conclusion')
quiz('מסיימים במשפט סביל','Working hours should ',' during the school year.',['limit','be limited','be limiting'],'be limited','passive','המבנה: should be + V3. מה מתאים?')
add('החיבור עד עכשיו',en('119 words','word-count')+he('איזה הסבר או איזו דוגמה חסרים בפסקת הגוף?')+he('מוסיפים תוכן בעל משמעות עד 120–140 מילים, ונשארים בארבע פסקאות.','note')+he('בסיום מאמתים את הספירה גם ב־Word או ב־Google Docs.','note'))
essay=[
'Many teenagers consider getting a job while they are still at school. I claim that limited working hours can help students prepare for adult life.',
'On the one hand, working after school can leave teenagers tired. If they work every evening, they will have less time for homework. For example, a late shift may make preparing for a test difficult.',
'On the other hand, a small job can teach practical skills. Many students have learned to manage money through work. Saving part of their pay can also help them understand the difference between needs and wishes. In this way, they may become more independent.',
'In conclusion, an after-school job can be beneficial when school remains the main priority. Working hours should be limited during the school year.']
assert sum(len(p.split()) for p in essay)==127
add('החיבור שהשלמנו · 127 מילים','<div class="essay" lang="en" dir="ltr">'+''.join('<p>'+p+'</p>' for p in essay)+'</div>','essay-slide')
add('גם נושא תיאורי',en('Describe someone who had a great influence on your life.')+he('בוחרים אדם, מתארים את ההשפעה ומוסיפים דוגמה.')+he('המאמן מתאים את פסקאות הגוף למשימה. מציגים צדדים מנוגדים רק כשיש ניגוד אמיתי.','note'))
add('בדיקה עצמית לפני סיום','<div class="checklist"><p>עניתי על הנושא והדוגמאות תומכות ברעיון?</p><p>יש ארבע פסקאות ו־120–140 מילים?</p><p>המבנים הדקדוקיים מתאימים למשמעות?</p><p>אני יכול להסביר מה תיקנתי ולמה?</p></div>'+he('זהו מבנה תרגול של הכיתה; המאמן אינו נותן ציון בגרות רשמי.','note'))
add('עכשיו תורכם',he('פתחו את המאמן וכתבו:','instruction')+he('מתחילים','command')+he('כתבו פתיחה ועמדה. תקנו משפט אחד בעקבות המשוב.')+he('בסיום: הסבירו במילים שלכם מה השתפר.','note')+he('לתרגול בנושא חדש מקלידים ״נביא״ או ״נושא חדש״.','note'))
sections=[]
for i,s in enumerate(slides,1):
    meta='' if s['kind']=='break' else f'<header class="slide-meta"><h2 class="eyebrow">{s["title"]}</h2><div class="tense">{s["tense"]}</div></header>'
    sections.append(f'<section class="slide {s["kind"]}" data-pair="{s["pair"]}" aria-label="שקף {i}: {s["title"]}" hidden><div class="frame">{meta}{s["body"]}</div></section>')
html='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>מאמן כתיבה למודול G — כיתה י״א | Teachers</title><link rel="stylesheet" href="assets/deck.css"><link rel="stylesheet" href="lesson.css"></head><body>
<a class="home" href="../five-units/" aria-label="חזרה לספריית כיתה י״א"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 11 12 3l9 8M5 10v11h5v-7h4v7h5V10"/></svg></a>
<div class="coach-access"><span>לתרגול כתיבה עם משוב</span><a href="GEM" target="_blank" rel="noopener">פתיחת המאמן ↗</a></div>
<main class="stage" tabindex="-1">SLIDES</main>
<nav class="nav" aria-label="ניווט במצגת"><div class="nav-group"><button data-step="-1" aria-label="השקף הקודם">←</button><button data-step="1" aria-label="השקף הבא">→</button></div><div class="progress" id="counter" aria-live="polite"></div><div class="lesson-links"><a href="teacher.html">למורה</a><a href="files/writing-coach.pptx">PPTX</a></div></nav><div class="progress-track"><div class="progress-fill"></div></div><script src="assets/deck.js"></script></body></html>'''.replace('GEM',GEM).replace('SLIDES','\n'.join(sections))
OUT.joinpath('index.html').write_text(html)
OUT.joinpath('lesson-data.json').write_text(json.dumps({'gem':GEM,'slides':slides,'essay':essay,'count':127},ensure_ascii=False,indent=2))
# Pin shared presentation engine and styles so the package is self-contained.
css=(ROOT/'assets/lesson-decks/deck.css').read_text()
css=css[css.index(':root'):]
css='@font-face{font-family:Heebo;src:url(Heebo.ttf);font-weight:100 900;font-display:swap}@font-face{font-family:Nunito;src:url(Nunito.ttf);font-weight:100 900;font-display:swap}\n'+css
OUT.joinpath('assets/deck.css').write_text(css)
shutil.copyfile(ROOT/'assets/lesson-decks/deck.js',OUT/'assets/deck.js')
original=ROOT/'grade11/five-units/index.remote.html'
if original.exists():
    card=f'''<a class="material" href="../module-g-writing-coach/"><div><span class="tag">מודול G · מאמן כתיבה ב־Gemini</span><h2>מאמן כתיבה למודול G</h2><p>{len(slides)} שקפים: הפעלת המאמן, כתיבה משפט־משפט, משוב ותיקון. קישור למאמן בכל שקף.</p><div class="created"><b>נוצר:</b> יום שבת, ח׳ בתשרי תשפ״ז (<time datetime="2026-09-19">19.9.2026</time>)</div></div><span class="arrow">←</span></a>
<a class="pptx" href="../module-g-writing-coach/teacher.html">תסריט למורה וחומרי השיעור</a>
<a class="pptx" href="../module-g-writing-coach/files/writing-coach.pptx">PPTX</a>
'''
    (ROOT/'grade11/five-units/index.html').write_text(original.read_text().replace('<section class="materials">','<section class="materials">\n'+card,1))
print(f'Built {len(slides)} slides; essay: 127 words; paragraph counts: {[len(p.split()) for p in essay]}')
