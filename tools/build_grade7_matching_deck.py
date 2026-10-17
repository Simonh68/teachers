#!/usr/bin/env python3
"""Generate the classroom slide deck accompanying the Grade 7 two-page PDF."""
from pathlib import Path
from html import escape as e
from build_grade7_matching_reading import PAIRS, ORDER, TEXT

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'grade7/exam-matching-reading/index.html'
slides=[]

def speak(text,small=False,evidence=''):
    evidence = evidence if evidence.lower() in text.lower() else ''
    return f'<div class="spoken {"small" if small else ""}"><p class="en" lang="en" data-read data-text="{e(text,quote=True)}" data-evidence="{e(evidence,quote=True)}">{e(text)}</p><button class="speak" type="button" aria-label="הקראת המשפט באנגלית">🔊</button></div>'

def add(section,title,instruction,body,kind='info'):
    slides.append(f'<section class="slide {kind}" data-section="{section}" aria-label="שקף {len(slides)+1}" hidden><div class="frame"><p class="section-label">{section}</p><h1>{title}</h1><p class="instruction">{instruction}</p>{body}</div></section>')

def reveal(body,label='הצג הסבר ותשובה'):
    return f'<button class="reveal-btn" type="button">{label}</button><div class="solution" hidden>{body}</div>'

def options(items):
    # items: text, correct, language, optional printed worksheet number
    out='<div class="choices" data-shuffle>'
    for item in items:
        text,correct,lang,*number=item
        num=f'<b class="printed-number">{number[0]}.</b>' if number else ''
        out+=f'<button class="choice" type="button" lang="{lang}" dir="{"ltr" if lang=="en" else "rtl"}" data-correct="{str(correct).lower()}">{num}<span>{e(text)}</span></button>'
    return out+'</div><p class="feedback" role="status" aria-live="polite">חשבו ובחרו. אפשר לנסות שוב.</p>'

def mc(section,title,instruction,stem,items,explain,hint,refs=(),evidence=''):
    source=''.join(speak(t,True,evidence) for t in refs)
    body=(f'<div class="source"><p class="source-label">מתוך הטקסט</p>{source}</div>' if refs else '')+stem
    body+=options(items)+f'<div class="hint" hidden>{e(hint)}</div>'+reveal(f'<p>{explain}</p>','הצג פתרון')
    add(section,title,instruction,body,'challenge')

def match(i,j,title,hint,explain):
    n=ORDER.index(i)+1; other=ORDER.index(j)+1
    mc('התאמה',title,'איזה תרגום מתאים לכל המשפט? בחרו, ואז כתבו את המספר על הקו בדף.',speak(PAIRS[i][0]),[(PAIRS[i][1],True,'he',n),(PAIRS[j][1],False,'he',other)],f'על הקו כותבים <strong>{n}</strong>. {explain}',hint)

def question(title,q,answer,wrong,ref,explain,hint,evidence=''):
    mc('שאלות',title,'קראו את המשפט מהטקסט, ואז בחרו את התשובה המתאימה לשאלה.',speak(q),[(answer,True,'en'),(wrong,False,'en')],speak(answer)+f'<p>{explain}</p>',hint,ref,evidence)

def openq(title,q,answer,ref,explain,evidence=''):
    body='<div class="source"><p class="source-label">מתוך הטקסט</p>'+''.join(speak(t,True,evidence) for t in ref)+'</div>'+speak(q)
    body+='<p class="write-cue">כתבו תשובה קצרה באנגלית במחברת. אחר כך בדקו.</p>'+reveal(speak(answer)+f'<p>{explain}</p>','הצג תשובה לדוגמה')
    add('שאלות',title,'קודם מנסים בעצמכם. חפשו את המידע הדרוש במשפט שמעל השאלה.',body,'open-question')

def build(title,he,chunks,explain):
    bank=''.join(f'<button type="button" class="tile en" lang="en" data-token="{i}">{e(t)}</button>' for i,t in enumerate(chunks))
    full=' '.join(chunks)
    body=f'<p class="he-target">{e(he)}</p><div class="assembly en" lang="en" aria-label="המשפט שאתם בונים"><span class="assembly-placeholder">המשפט שלכם יופיע כאן</span></div><div class="word-bank" dir="ltr">{bank}</div><div class="build-controls"><button class="check-build" type="button">בדקו את המשפט</button><button class="clear-build" type="button">ניסיון חדש</button></div><p class="feedback" role="status" aria-live="polite">לחצו על החלקים לפי הסדר באנגלית, משמאל לימין.</p>'+reveal(speak(full)+f'<p>{explain}</p>','הצג משפט לדוגמה')
    add('משפט חדש',title,'הרכיבו באנגלית את המשפט שבעברית. אפשר ללחוץ על חלק במשפט כדי להחזיר אותו.',body,'build')

add('התאמה','מתכוננים למבחן','היום נתרגל עם המילים והמשפטים שכבר למדנו.',speak('School Years Around the World')+'<p class="big-note">קוראים משפט, חושבים על המשמעות, ומנסים בעצמנו.</p><a class="resource" href="Grade7-Matching-and-Reading-Practice.pdf">פתיחת דף העבודה: שני עמודים</a><p class="navigation-help">עוברים בעזרת החצים, מקשי החצים או החלקה. לחצו על הרמקול כדי לשמוע אנגלית.</p>','cover')
add('התאמה','כך נראה תרגיל ההתאמה','בטור השמאלי יש משפט באנגלית וקו. בטור הימני יש תרגומים עם מספרים.', '<div class="worksheet-demo" dir="ltr"><div><p class="mini-label">English</p>'+speak('The school year starts in summer.',True)+'<p class="blank en">________</p></div><div dir="rtl"><p class="mini-label">עברית</p><p><b>5.</b> שנת הלימודים מסתיימת באביב.</p><p><b>19.</b> שנת הלימודים מתחילה בקיץ.</p></div></div>'+reveal('<p class="demo-answer">על הקו כותבים <strong>19</strong>.</p><p>המספר שייך לתרגום בעברית. בדקנו גם את הפעולה וגם את העונה.</p>','הצג מה כותבים על הקו'))
add('התאמה','כל המשפט חשוב','איזו מילה משנה את המשמעות?',speak('The school year starts in summer.')+speak('The school year ends in summer.')+reveal('<p><span class="en inline" lang="en">starts</span> = מתחילה</p><p><span class="en inline" lang="en">ends</span> = מסתיימת</p><p>בשני המשפטים כתוב קיץ, אבל הפעולה שונה.</p>'))
add('התאמה','מפת מילים קצרה','קראו את המילים. הן יעזרו לכם לבדוק את כל חלקי המשפט.', '<div class="vocab-grid"><p><span lang="en" class="en inline">spring</span> אביב</p><p><span lang="en" class="en inline">summer</span> קיץ</p><p><span lang="en" class="en inline">autumn</span> סתיו</p><p><span lang="en" class="en inline">late summer</span> סוף הקיץ</p><p><span lang="en" class="en inline">about</span> בערך</p><p><span lang="en" class="en inline">during</span> במהלך</p></div>')
match(1,0,'מה קורה לשנת הלימודים?','חפשו את הפועל ends ואת העונה spring.','ends פירושו מסתיימת, ו־spring פירושו אביב.')
match(2,3,'תחילת חופשה או סוף חופשה?','קראו את הפועל ואת העונה, ולא רק את המילה holiday.','החופשה מתחילה, והעונה היא סתיו.')
match(4,5,'שישה או אחד עשר?','איזה מספר מופיע במשפט באנגלית?','six הוא שישה. המשפט מתאר את אורך חופשת הקיץ.')
match(10,17,'מה כתוב על הילדים?','בדקו אם המשפט באנגלית מציין מדינה.','המשפט אומר שלילדים יש שישה שבועות חופשה. הוא לא מציין מדינה.')
match(18,21,'מקום, פעולה ועונה','חפשו את Alaska ואת late summer.','במשפט הזה הילדים באלסקה מתחילים ללמוד בסוף הקיץ.')
match(26,28,'מי הילדים, ואיפה החופשה?','Japanese מתאר את הילדים. in the USA מציין את מקום החופשה.','הילדים יפנים, ואת חופשת הקיץ הם מבלים בארצות הברית. זהו משפט תרגול דמיוני.')
add('התאמה','כשמשהו מתחיל ומשהו מסתיים','קראו כל חלק בנפרד. שימו לב מה מתחיל ומה מסתיים.',speak('The school year starts when the summer holiday ends.')+reveal('<p><span class="en inline" lang="en">The school year starts</span> שנת הלימודים מתחילה.</p><p><span class="en inline" lang="en">when the summer holiday ends</span> כשחופשת הקיץ מסתיימת.</p><p>בתוך המשפט הזה, when פירושו כש־.</p>'))
match(22,23,'מה מתחיל קודם במשפט?','החלק הראשון הוא The school year starts.','שנת הלימודים מתחילה כשחופשת הקיץ מסתיימת.')
match(24,25,'על מה המשפט מספר?','הנושא בתחילת המשפט הוא The weather.','המשפט מתאר את מזג האוויר במהלך חופשת הקיץ.')
add('התאמה','עכשיו בדף שלכם','בחרו שלושה משפטים שעדיין לא פתרנו. התאימו לכל אחד תרגום וכתבו את המספר.', '<p class="big-note">לפני שמחליטים, בודקים: על מי מדובר? מה קורה? מתי או איפה?</p><p class="write-cue">עבדו לבד שתי דקות, ואז השוו עם חבר.</p>')

add('משפט חדש','בונים משפט מחלקים מוכרים','אפשר להשתמש בחלקים מהטקסט כדי לומר משהו חדש.',speak('Children have a holiday in spring.')+'<div class="chunk-example en" lang="en"><span>Children</span><span>have</span><span>a holiday</span><span>in spring.</span></div>'+reveal('<p>Children אומר על מי מדברים. have אומר שיש להם. אחר כך כתובים מה יש להם ומתי.</p><p>מחליפים חלק אחד ושומרים על משפט בעל משמעות.</p>'))
add('משפט חדש','שינוי קטן, משפט חדש','החליפו את העונה. איזה משפט חדש מתקבל?',speak('Children have a holiday in spring.')+'<p class="he-target">במקום באביב: בקיץ</p>'+reveal(speak('Children have a holiday in summer.')+'<p>החלפנו את spring ב־summer. שאר המשפט נשאר מתאים.</p>','הצג את המשפט החדש'))
build('אתם מרכיבים: לילדים יש חופשה','לילדים יש חופשה באביב.',['Children','have','a holiday','in spring.'],'נושא המשפט הוא Children. אחריו מופיע have, ובסוף הזמן.')
build('אתם מרכיבים: סוף השנה','שנת הלימודים מסתיימת באביב.',['The school year','ends','in spring.'],'The school year הוא נושא המשפט. ends אומר מה קורה.')
build('אתם מרכיבים: שתי מדינות','לילדים ביפן ובאנגליה יש חופשת קיץ.',['Children in Japan and England','have','a summer holiday.'],'כל החלק Children in Japan and England מתאר את הילדים שעליהם מדברים.')
build('אתם מרכיבים: מזג האוויר','מזג האוויר חם במהלך חופשת הקיץ.',['The weather','is hot','during the summer holiday.'],'during פירושו במהלך. הוא עוזר לנו לציין מתי מזג האוויר חם.')

add('שאלות','הטקסט המקוצר שלנו','בעמוד השני עונים רק לפי הטקסט הזה.', '<div class="full-text">'+''.join(speak(t,True) for t in TEXT)+'</div>','text-slide')
add('שאלות','איך מוצאים תשובה?','קראו את השאלה לפני שאתם מחפשים בטקסט.', '<ol class="steps"><li>זהו איזה מידע מבקשים: זמן, מקום, אדם או מספר.</li><li>מצאו את המשפט שמדבר על אותו מקום או אותם ילדים.</li><li>כתבו תשובה קצרה באנגלית.</li></ol><p class="write-cue">יש שורה נפרדת לכל תשובה בדף העבודה.</p>')
mc('שאלות','מה מבקשת המילה When?','השאלה באנגלית מופיעה מתחת. איזה סוג מידע צריך בתשובה?',speak('When does school start in Japan?'),[('זמן או עונה',True,'he'),('מקום',False,'he')],'When פירושו מתי. נחפש זמן, ובטקסט שלנו זו עונה.','חשבו על המשמעות של מתי.')
openq('דוגמה: שאלה על זמן','When does the school year start in Japan?','In spring.',[TEXT[1]],'השאלה מבקשת זמן. In spring היא תשובה קצרה ומדויקת.','in spring')
question('תחילת הלימודים באלסקה','When does school start in Alaska?','In late summer.','In spring.',[TEXT[3]],'השאלה שואלת על ההתחלה. האביב מופיע ליד ends, כלומר הסיום.','חפשו מה כתוב אחרי school starts.','late summer')
openq('ניסיון עצמאי: סוף הלימודים','When does school end in England?','In summer.',[TEXT[6]],'end בשאלה מתאים ל־ends במשפט. שניהם מתייחסים לסיום.','in summer')
mc('שאלות','מה מבקשת המילה Where?','איזה סוג מידע דרוש בתשובה?',speak('Where is Alaska?'),[('מקום',True,'he'),('מספר שבועות',False,'he')],'Where פירושו איפה. התשובה צריכה לציין מקום.','Where היא מילת שאלה על מקום.')
question('איפה נמצאת אלסקה?','Where is Alaska?','In the USA.','In Japan.',[TEXT[3]],'ליד Alaska כתוב in the USA. זהו המקום המבוקש.','קראו את תחילת המשפט.','in the USA')
question('איפה נמצאת פלורידה?','Where is Florida?','In the USA.','In England.',[TEXT[5]],'גם פלורידה נמצאת בארצות הברית לפי הטקסט.','חפשו את המילים שמופיעות מיד אחרי Florida.','in the USA')
mc('שאלות','מה מבקשת המילה Who?','איזה סוג מידע צריך בתשובה?',speak('Who has a summer holiday during the school year?'),[('אדם או אנשים',True,'he'),('עונה',False,'he')],'Who פירושו מי. נחפש על אילו ילדים המשפט מדבר.','מי הם האנשים שעליהם מדברים?')
openq('מי יוצא לחופשה במהלך השנה?','Who has a summer holiday during the school year?','Japanese children.',[TEXT[2]],'התשובה מציינת את הילדים. די בצירוף Japanese children.','Japanese children')
mc('שאלות','מה מבקשות המילים How many?','חשבו מה צריכה התשובה לכלול.',speak('How many weeks is the summer holiday?'),[('מספר שבועות',True,'he'),('שם של מדינה',False,'he')],'How many weeks פירושו כמה שבועות. נחפש מספר ואת המילה weeks.','weeks פירושו שבועות.')
openq('דוגמה: מספר שבועות','How many weeks is the summer holiday in Alaska?','About eleven weeks.',[TEXT[3],TEXT[4]],'there במשפט השני מתייחס לאלסקה שבמשפט הקודם. about פירושו בערך.','about eleven weeks')
question('מספר שבועות באנגליה','How many weeks of summer holiday do children in England have?','About six weeks.','About eleven weeks.',[TEXT[7]],'השאלה היא על אנגליה. בטקסט כתוב about six weeks.','מצאו את המספר במשפט על England.','about six weeks')
question('שאלה על מזג האוויר','What is the weather like when school starts in Florida?','It is hot.','In summer.',[TEXT[5]],'השאלה מבקשת לתאר את מזג האוויר. hot מתאר מזג אוויר; summer היא עונה.','איזו מילה בטקסט מתארת את מזג האוויר?','the weather is hot')
add('שאלות','שאלות כן או לא','גם בשאלת כן או לא צריך לבדוק את המידע בטקסט.',speak('Does school in Japan start in summer?')+'<div class="source">'+speak(TEXT[1],True,'in spring')+'</div>'+reveal(speak('No.')+'<p>השאלה אומרת קיץ, אבל הטקסט אומר אביב. לכן התשובה היא No.</p>','הצג תשובה והסבר'))
question('מה קורה בסוף השנה באלסקה?','Does school in Alaska end in summer?','No.','Yes.',[TEXT[3]],'לפי הטקסט הלימודים באלסקה מסתיימים באביב, ולכן התשובה היא No.','בדקו את העונה שאחרי ends.','ends in spring')
question('החופשה של הילדים ביפן','Do Japanese children have a summer holiday?','Yes.','No.',[TEXT[2]],'הטקסט אומר במפורש שיש לילדים ביפן חופשת קיץ.','קראו מה נאמר אחרי Japanese children.','have a summer holiday')
question('שתי עונות באותו משפט','When does school start in England?','In autumn.','In summer.',[TEXT[6]],'start בשאלה מתאים ל־starts בטקסט. autumn היא עונת ההתחלה.','הבחינו בין starts לבין ends.','starts in autumn')
openq('שני פרטים מהטקסט','Name two places in the USA from the text.','Alaska and Florida.',[TEXT[3],TEXT[5]],'השאלה מבקשת שני מקומות. צריך לכלול את שניהם בתשובה.','in the USA')

add('תרגול עצמאי','עכשיו אתם עונים','כתבו שלוש תשובות קצרות. היעזרו בטקסט שבעמוד השני של דף העבודה.',speak('1. When does school start in Florida?',True)+speak('2. Where is Alaska?',True)+speak('3. How many weeks of summer holiday do children in England have?',True)+'<p class="write-cue">עבדו לבד לפני פתיחת התשובות.</p>'+reveal(speak('1. In summer.',True)+speak('2. In the USA.',True)+speak('3. About six weeks.',True),'בדקו את התשובות שלכם'))
add('תרגול עצמאי','מוכנים להמשיך בדף העבודה','השלימו את ההתאמות ואת שאלות ההבנה שעוד לא פתרתם.', '<ul class="steps"><li>בהתאמה כותבים את מספר התרגום בעברית.</li><li>בשאלות כותבים תשובות קצרות באנגלית, לפי הטקסט.</li><li>במשפט חדש משתמשים בחלקים מוכרים ושומרים על סדר מילים נכון.</li></ul><a class="resource" href="Grade7-Matching-and-Reading-Practice.pdf">פתיחת דף העבודה ב־PDF</a><p class="big-note">לפני שמסיימים, קוראים שוב כל תשובה.</p>','closing')

assert len(slides)==42,len(slides)
slides[0]=slides[0].replace(' hidden>','>',1)
OUT.write_text('''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>כיתה ז׳ | מתאימים, בונים ועונים | הכנה למבחן</title><meta name="description" content="מצגת הכנה לכיתה ז׳: הדגמת דף העבודה, התאמת משפטים, בניית משפטים ושאלות על הטקסט המקוצר."><link rel="stylesheet" href="../../shared/deck/standard.css"><link rel="stylesheet" href="lesson.css?v=1"><script defer src="lesson.js?v=1"></script></head><body>
<header class="topbar"><div class="top-links"><a href="../" aria-label="חזרה לכיתה ז׳">⌂</a><a href="Grade7-Matching-and-Reading-Practice.pdf" aria-label="פתיחת דף העבודה">PDF</a></div><nav class="chapters" aria-label="חלקי המצגת"><button data-chapter="התאמה">התאמה</button><button data-chapter="משפט חדש">משפט חדש</button><button data-chapter="שאלות">שאלות</button><button data-chapter="תרגול עצמאי">תרגול עצמאי</button></nav></header>
<main id="stage" class="stage" aria-live="off">'''+''.join(slides)+'''</main><footer class="controls"><button id="prev" aria-label="השקף הקודם">← <span>הקודם</span></button><span id="counter" role="status" aria-label="מספר השקף"></span><div class="audio-controls"><label for="speed">מהירות</label><select id="speed" aria-label="מהירות הקראה"><option value="0.65">0.65</option><option value="0.8" selected>0.8</option><option value="1">1.0</option></select><button id="stop" aria-label="עצירת הקראה">■</button></div><button id="fullscreen" aria-label="מסך מלא">⛶</button><button id="next"><span>הבא</span> →</button></footer><div class="progress-track"><div id="progress" class="progress-fill"></div></div><p id="audio-status" class="sr-only" role="status"></p><noscript>כדי להשתמש במצגת יש להפעיל JavaScript בדפדפן. דף העבודה זמין בקישור PDF בראש העמוד.</noscript></body></html>''',encoding='utf-8')
print(f'Created {len(slides)} slides: {OUT}')
