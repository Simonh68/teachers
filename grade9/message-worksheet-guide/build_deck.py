"""Build the worksheet companion using the shared Teachers deck runtime."""
from pathlib import Path
from html import escape
import json

BASE=Path(__file__).resolve().parent
PDF='files/Grade9-The-Message-Without-a-Voice-Worksheets.pdf'
CREATED='מוצאי שבת, ז׳ בחשוון תשפ״ז (17.10.2026)'
slides=[]

def slide(section,content,kind='info',pair=None,eyebrow='',tense=''):
    n=len(slides)+1
    attrs=f' data-pair="{pair}"' if pair else ''
    slides.append(f'<section class="slide {kind}" data-section="{section}"{attrs} aria-label="שקף {n}" hidden><div class="frame"><div class="slide-meta"><div class="eyebrow">{eyebrow}</div><div class="tense">{tense}</div></div>{content}</div></section>')

def intro(section,title,body,eyebrow):
    slide(section,f'<h2 class="part-title">{title}</h2><p class="instruction">{body}</p>','transition',eyebrow=eyebrow)

def work(section,title,body,eyebrow):
    slide(section,f'<h2 class="part-title">{title}</h2><p class="instruction">{body}</p><p class="work-note">עובדים בחוברת. חוזרים לטקסט לפי הצורך.</p>',eyebrow=eyebrow)

def qa(section,title,main,answer,pair,eyebrow,tense=''):
    for reveal in [False,True]:
        slot=answer if reveal else ''
        slide(section,f'<h2 class="question">{title}</h2>{main}<div class="answer-slot" aria-label="תשובה">{slot}</div>',
              'qa guide-pair'+(' reveal' if reveal else ''),pair,eyebrow,tense)

slide('start','<h1 class="cover-title">הכנה למבחן</h1><p class="cover-sub">כיתה ט׳ · דפי עבודה</p><p class="story-title en" lang="en">The Message Without a Voice</p>',
      'cover transition',eyebrow='מבחנים ומעקב')
slide('start',f'<h2 class="part-title">פותחים את החוברת</h2><p class="instruction">מתחילים בקריאת הסיפור בעמוד 1.<br>האותיות <bdi>A–D</bdi> מסמנות את הפסקאות.</p><div class="resource-links"><a href="{PDF}" target="_blank" rel="noopener" type="application/pdf">פתיחת החוברת · PDF אחד · 6 עמודים</a></div><p class="work-note">קריאה, סידור עלילה, נכון/לא נכון, התאמה ושאלות פתוחות.</p>',eyebrow='עמוד 1 · קריאה · 5 דקות')

intro('order','מסדרים את העלילה','כותבים בכל ריבוע מספר מ־1 עד 8.<br>המספר מציין מתי האירוע קרה בסיפור.','עמוד 2 · חלק 1')
events=['Noam reads the short message.','Noam asks Eitan to help.','Eitan explains the missing message.']
for reveal in [False,True]:
    rows=''.join(f'<div class="event-row"><span class="number-box {"filled" if reveal else ""}">{[2,1,3][i] if reveal else "?"}</span><span>{escape(s)}</span></div>' for i,s in enumerate(events))
    slide('order',f'<h2 class="question">מה קורה קודם? מספרו את שלושת האירועים.</h2><div class="event-demo en" lang="en">{rows}</div><div class="answer-slot">'+
          ('<p class="explanation">קודם נועם מבקש עזרה, אחר כך קורא את ההודעה, ולבסוף שומע את ההסבר.</p>' if reveal else '')+'</div>',
          'qa guide-pair'+(' reveal' if reveal else ''),'order-demo','הדגמה קצרה · כאן יש שלושה אירועים')
work('order','עכשיו: שמונת האירועים','מלאו את כל הריבועים בעמוד 2.<br>כל מספר מ־1 עד 8 מופיע פעם אחת.','עמוד 2 · חלק 1 · 7 דקות כולל ההדגמה')

intro('facts','בודקים עובדות מהסיפור','הקיפו נכון או לא נכון.<br>אם המשפט שגוי, כתבו בשורה משפט מתוקן באנגלית.','עמוד 2 · חלק 2')
qa('facts','נכון או לא נכון?',
   '<p class="en demo-sentence" lang="en">Noam sent Eitan an angry answer.</p><p class="choice-labels">נכון &nbsp; / &nbsp; לא נכון</p>',
   '<p class="answer-label">לא נכון</p><p class="en possible-answer" lang="en">Noam started writing an angry answer, <mark>but he stopped</mark>.</p><p class="evidence">פסקה A: הוא התחיל לכתוב ועצר. לא נאמר ששלח.</p>',
   'fact-demo','דוגמה מתוך החוברת','עבר')
work('facts','בודקים את כל שמונת המשפטים','השאירו משפט נכון ללא שינוי.<br>במשפט שגוי, תקנו את העובדה בעזרת הטקסט.','עמוד 2 · חלק 2 · 10 דקות כולל ההדגמה')

intro('match','מתאימים משפטים לתרגום','אנגלית בצד שמאל. עברית ממוספרת בצד ימין.<br>כתבו ליד האנגלית את מספר התרגום המתאים.','עמוד 3 · 16 התאמות')
for reveal in [False,True]:
    content=f'''<h2 class="question">איזה מספר כותבים ליד כל משפט?</h2>
    <div class="match-demo" dir="ltr">
      <div class="match-column en" lang="en"><p><span class="number-box {"filled" if reveal else ""}">{'2' if reveal else '?'}</span><span>Noam wanted to make friends.</span></p><p><span class="number-box {"filled" if reveal else ""}">{'1' if reveal else '?'}</span><span>Eitan helped his brother.</span></p></div>
      <div class="match-column" dir="rtl" lang="he"><p><b>1.</b><span>איתן עזר לאחיו.</span></p><p><b>2.</b><span>נועם רצה להתיידד.</span></p></div>
    </div><div class="answer-slot">{('<p class="explanation">התאימו את משמעות המשפט כולו. התרגום המתאים אינו בהכרח באותה שורה.</p>' if reveal else '')}</div>'''
    slide('match',content,'qa guide-pair'+(' reveal' if reveal else ''),'match-demo','דוגמה קצרה · שני משפטים')
work('match','מתאימים את כל 16 המשפטים','כתבו מספר על כל קו בצד האנגלי.<br>השתמשו בכל מספר עברי פעם אחת.','עמוד 3 · 12 דקות כולל ההדגמה')

intro('answers','עונים על שאלות פתוחות','קראו מה בדיוק נשאלתם.<br>מצאו את הפרט בסיפור וכתבו תשובה קצרה באנגלית.','עמודים 4–6 · 18 שאלות')
qa('answers','בשאלת מדוע מסבירים סיבה',
   '<p class="en demo-sentence" lang="en">Why did Noam ask Eitan to help with the display?</p>',
   '<p class="answer-label">תשובה אפשרית</p><p class="en possible-answer" lang="en">He asked Eitan <mark>because</mark> he wanted to make friends with him.</p><p class="evidence">הסיבה מופיעה בפסקה A. אפשר לנסח גם במילים שלכם.</p>',
   'open-demo','דוגמה · שאלה 2 בחוברת','עבר')
work('answers','כותבים תשובות בחוברת','ענו על שאלות 1–18.<br>אם נשאלתם שני דברים, ענו על שניהם.<br>בשאלות 13 ו־18 הסבירו מסקנה בעזרת פרט מהסיפור.','עמודים 4–6 · 26 דקות כולל ההדגמה')

intro('fix','רשות: מתקנים כתיב ודקדוק','בכל משפט יש שגיאה אחת.<br>כתבו את כל המשפט מחדש בצורה נכונה.','עמוד 6 · למי שסיים')
qa('fix','איזו מילה צריך לתקן?',
   '<p class="en demo-sentence" lang="en">Noam did not sent the angry answer.</p>',
   '<p class="en possible-answer" lang="en">Noam did not <mark>send</mark> the angry answer.</p><p class="explanation">אחרי <bdi>did not</bdi> משתמשים בצורת הבסיס של הפועל.</p>',
   'grammar-demo','תרגיל רשות · דקדוק','עבר')
qa('fix','איך מאייתים את הפועל בעבר?',
   '<p class="en demo-sentence" lang="en">Eitan carryed a blue bag.</p>',
   '<p class="en possible-answer" lang="en">Eitan <mark>carried</mark> a blue bag.</p><p class="explanation">בסיום עיצור + <bdi>y</bdi>, משנים את <bdi>y</bdi> ל־<bdi>i</bdi> ומוסיפים <bdi>ed</bdi>.</p>',
   'spelling-demo','תרגיל רשות · כתיב','עבר')
slide('end',f'<h2 class="part-title">בודקים לפני שמסיימים</h2><p class="instruction">עניתי על כל מה שנשאלתי?<br>התשובה מתאימה לפרטים בסיפור?<br>בדקתי כתיב, אות גדולה ונקודה?</p><div class="resource-links"><a href="{PDF}" target="_blank" rel="noopener">חזרה לחוברת העבודה · PDF</a></div>',
      'transition',eyebrow='בדיקה עצמית')

head='''<!doctype html>
<html lang="he" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#07111f">
<meta name="description" content="מצגת הדרכה לחוברת ההכנה למבחן בכיתה ט׳: סדר עלילה, נכון ולא נכון, התאמת משפטים ושאלות פתוחות על The Message Without a Voice.">
<title>כיתה ט׳ · חוברת עבודה והדרכה · The Message Without a Voice</title>
<link rel="stylesheet" href="../../shared/deck/standard.css?v=20261017">
<link rel="stylesheet" href="guide.css?v=20261017">
</head><body>
<a class="home" href="../../#grade9" aria-label="חזרה לחומרי כיתה ט׳">⌂</a>
<nav class="section-nav" aria-label="חלקי המצגת">
<button data-jump="order">עלילה</button><button data-jump="facts">עובדות</button><button data-jump="match">התאמה</button><button data-jump="answers">שאלות</button><button data-jump="fix">תיקון</button>
</nav><main class="stage">'''
foot=f'''</main><nav class="nav" aria-label="ניווט במצגת">
<div class="nav-group"><button data-step="-1" aria-label="השקף הקודם">←</button><button data-step="1" aria-label="השקף הבא">→</button></div>
<span class="progress" id="counter" aria-live="polite"></span>
<a class="pdf-link" href="{PDF}" target="_blank" rel="noopener" type="application/pdf">PDF</a>
</nav><p class="created-meta">נוצר: {CREATED}</p>
<div class="progress-track"><div class="progress-fill"></div></div>
<script src="../../shared/deck/standard.js?v=20261017"></script>
</body></html>'''
(BASE/'index.html').write_text(head+'\n'+'\n'.join(slides)+'\n'+foot)
(BASE/'manifest.json').write_text(json.dumps({'title':'The Message Without a Voice - Worksheet Guide','created':'2026-10-17','created_hebrew':CREATED,'slides':len(slides),'worksheet':PDF,'worksheet_pages':6,'questions':18,'standard':'../../shared/deck/standard.js'},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(slides)} slides')
