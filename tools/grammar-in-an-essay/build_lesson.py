from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[2]
(ROOT/'tools/grammar-in-an-essay/build').mkdir(parents=True,exist_ok=True)
OUT=ROOT/'grade11/grammar-in-an-essay'
E=html.escape
S=[]
SOURCE='https://meyda.education.gov.il/sheeloney_bagrut/pitronot_bagrut/2026/6/016582-8-HEB-1400-1600.pdf'
TOPIC='Should every student have a chance to play in class games, even if some students play better than others?'
SENTENCES=[
'School games are part of school life, but some students play better than others.',
'I claim that every student should have a chance to play.',
'On the one hand, some students may make more mistakes during games.',
'If they play, the team will sometimes lose since these mistakes can help the other team.',
'On the other hand, playing together can help students make friends and feel better.',
'Some students have felt alone, so joining a team can help them.',
'In conclusion, I believe that everyone should have a chance to play.',
'Therefore, every student should be included in class games.',
'For example, they may pass the ball to the other team.',
'Moreover, students can learn to help each other when they play together.'
]
PARAGRAPH_STEPS=[[0,1],[2,3,8],[4,5,9],[6,7]]
P=[' '.join(SENTENCES[i] for i in ids) for ids in PARAGRAPH_STEPS]
WC=len(' '.join(P).split())
def add(kind,title='',text='',he='',note='',**kw):
    s=dict(n=len(S)+1,kind=kind,title=title,text=text,he=he,note=note,section=kw.pop('section','plan'),**kw)
    S.append(s)
    return s
def info(title,he,text='',note='',section='plan',**kw):return add('info',title,text,he,note,section=section,**kw)
def pair(title,text,translation,note='',section='grammar',tense='',highlights=None):
    pid='reveal-'+str(len(S)+1)
    for reveal in [False,True]:
        add('example',title,text,translation if reveal else '',note,section=section,pair=pid,reveal=reveal,tense=tense,highlights=highlights or [])
def gap(title,before,after,options,correct,explanation,note='',section='grammar',tense=''):
    pid='gap-'+str(len(S)+1)
    for reveal in [False,True]:
        add('gap',title,before+'___'+after,explanation if reveal else '',note or explanation,section=section,pair=pid,reveal=reveal,before=before,after=after,options=options,correct=correct,tense=tense)
def choice(title,question,options,correct,explanation,section='grammar'):
    pid='choice-'+str(len(S)+1)
    for reveal in [False,True]:
        add('choice',title,question,explanation if reveal else '',explanation,section=section,pair=pid,reveal=reveal,options=options,correct=correct)
def timer(title,text,seconds,he,note,section='practice'):
    add('timer',title,text,he,note,section=section,seconds=seconds)
ANIMS=[
('tiny-goal','Planning is half the game. Aiming helps too.','חתול זורק כדור נייר לסל והוא נוחת על ראשו.','תכנון לפני כתיבה. 10 שניות, בלי משימה נוספת.'),
('half-message','He has read half the message. He has formed a whole opinion.','חתול מסיק מסקנה מוקדם מדי מקריאה בטלפון.','קשר בין קריאת המשימה לגיבוש עמדה. אפשר לחייך ולהמשיך.'),
('word-order','Balancing books is easier in the instructions.','חתול מאזן ספרים והם נוחתים על ראשו.','Balancing הוא נושא המשפט. לא חייבים לענות על שאלה בכל הפוגה.'),
('however-cat','The book is tiny. However, the jump is dramatic.','חתול קופץ מעל ספר זעיר בהגזמה.','הניגוד בין מכשול קטן לתגובה גדולה ממחיש However.'),
('wrong-envelope','The message was delivered. To the wrong head.','מעטפה נוחתת על ראשו של חתול.','הדגמה משעשעת של passive: המוקד במה שקרה להודעה.'),
('so-far','He has climbed three books. He needs a holiday.','חתול מטפס על ספרים כאילו טיפס על הר.','תוצאה עד כה: has climbed. הפוגה קצרה.'),
('serious-cat','If his glasses were smaller, he would look less surprised.','חתול עם משקפיים ענקיים שמחליקים.','משפט תנאי דמיוני הקשור לתמונה.'),
('two-friends','They have tried three times. Teamwork takes practice.','שני חתולים מחטיאים כיף ולבסוף מצליחים.','מחזיר לנושא של שיתוף פעולה ולזמן perfect.'),
('certain-cat','The mystery has been solved. It was his tail.','חתול בלש מגלה את זנבו.','חשיפה קצרה של present perfect passive. אין צורך ללמד מבנה חדש כעת.'),
('missing-piece','He has found the missing piece. Behind his ear.','חתול מוצא חלק פאזל מאחורי האוזן.','כמו בדיקת חיבור: לפעמים הפרט החסר קרוב.'),
('helpful-bag','A small idea. An unnecessarily large bag.','חתול שולף מעמד קטן מתיק גדול.','זוכרים להרחיב רעיון באמצעות דוגמה, בלי להעמיס מילים.'),
('chair-friend','Everyone should be included. Even the chair needs practice.','חתול מזיז כיסא לחבר ומנסה שוב לאחר טעות.','חזרה לנושא החיבור: הכללה, חברות ומתן הזדמנות.')]
def anim(i,section):
    asset,caption,alt,note=ANIMS[i-1]
    add('animation','הפוגה קצרה',caption,'',note,section=section,asset=asset,alt=alt,seconds=10.8)

# Reuse the established visuals, reveal pairs and player; shorten the teaching route.
add('cover','ברוכים הבאים','כיתה י״א · 5 יח״ל','ישיבת בני עקיבא קריית הרצוג','שיעור המשך: יישום מבנים שנלמדו, ולא לימוד הדקדוק מחדש.')
info('חיבור ברור, צעד אחר צעד','נשתמש במילים מוכרות ובמבנים קבועים.','Simple words. Clear ideas.','מטרת המפגש: חיבור מפותח וברור עם שפה שהתלמיד מסוגל לכתוב בעצמו. אין הבטחת ציון.')
info('The writing task','האם כל תלמיד צריך לקבל הזדמנות לשחק במשחקי הכיתה?','Should every student have a chance to play in class games, even if some students play better than others?','הבחינו בין משחקי הכיתה לבין בחירה לנבחרת. זו משימת תרגול.')
info('ארבע פסקאות','פתיחה ודעה; טענה נגדית; תמיכה בדעה; סיום.','Introduction\nOn the one hand, ...\nOn the other hand, ...\nIn conclusion, ...','יעד התרגול: 120–140 מילים. במבחן פועלים לפי הוראות המשימה.',source=SOURCE)
info('מילים שניקח לחיבור הבא','משתמשים בכל ביטוי רק כשהוא מתאים לרעיון.','I claim that ...\nsince / For example, / Moreover,\nTherefore, / In conclusion,','since מציג סיבה. moreover מוסיף רעיון. therefore מציג תוצאה. חזרה שימושית על מספר קטן של ביטויים.')
info('מילים לנושא של היום','בחרו מילים שאתם יודעים להשתמש בהן.','games / play / team\nfriends / help / mistakes','אין צורך במילים כגון matches, inexperienced או beneficial. הדיוק והרלוונטיות קודמים למילה קשה.')
timer('תכנון קצר','One idea against. One idea for.',120,'מה הקושי בשיתוף כולם? מה היתרון?','שתי הערות קצרות בעברית או באנגלית. אין כותבים עכשיו חיבור מלא.',section='plan')

def draft(step,title,prompt,he,section):
    timer(title,prompt,45,he,'ניסיון עצמאי קצר. קבלו ניסוחים פשוטים ותקינים. חשפו את הדוגמה רק אחריו.',section=section)
    S[-1]['draftStep']=step
    paras=[' '.join(SENTENCES[i] for i in ids if i<step) for ids in PARAGRAPH_STEPS]
    words=len(' '.join(paras).split())
    add('essay','החיבור עד עכשיו', '\n\n'.join(paras),f'שלב {step}/10 · {words} מילים'+(' · נוסיף דוגמה בגוף' if step in (8,9) else ''),'קראו רק את המשפט החדש; אין לקרוא שוב את כל החיבור. משפט חדש: '+SENTENCES[step-1]+' ההרחבות 9–10 נשארות בפסקאות הגוף.',section=section,paragraphs=paras,step=step)

draft(1,'1 · פתיחה בלי דעה','School games ...','הציגו את הנושא. עדיין בלי לומר מה דעתכם.','intro')
draft(2,'2 · הדעה שלי','I claim that ...','האם צריך לתת לכל תלמיד הזדמנות לשחק?','intro')
anim(1,'intro')
draft(3,'3 · חושבים על הקושי','On the one hand, ...','מה עלול לקרות לקבוצה כשמשתפים שחקנים פחות מנוסים?','intro')
info('First Conditional','תנאי אפשרי ותוצאה: בחלק של if אין will.','If + Present Simple, will + verb','חזרה קצרה על מבנה שכבר נלמד. תנאי שני אינו חלק מהשיעור הזה.',section='conditionals')
gap('תנאי אפשרי','If students practise, they ',' better.',['play','will play','played'],1,'If + Present Simple, will + verb.','שאלו מה התנאי ומה התוצאה. אל תלמדו כעת מבנים נוספים.',section='conditionals')
gap('since מציג סיבה','Students learn faster ',' they practise every day.',['since','although','therefore'],0,'since = מכיוון ש־. אחריו נושא ופועל.','בתרגול הזה נבחר since כדי ליצור הרגל קבוע. אין הבדל ניקוד אוטומטי רק בגלל החלפת מילת קישור.',section='conditionals')
draft(4,'4 · תנאי וסיבה','If they play, the team will ... since ...','תארו תוצאה אפשרית והסבירו את הסיבה.','conditionals')
draft(5,'5 · חוזרים לעמדה שלנו','On the other hand, ...','איך משחק משותף יכול לעזור לתלמידים?','perfect')
anim(8,'perfect')
info('Present Perfect','ניסיון קודם שקשור לרעיון שלנו.','have / has + V3\nfeel → felt → felt','דוגמה לצורך בנימוק: תלמידים הרגישו לבד, והקבוצה יכולה לעזור. לא מוסיפים זמן עבר מסוים כגון yesterday.',section='perfect')
gap('ניסיון קודם','Some students ',' alone.',['has felt','have felt','have feel'],1,'students הוא רבים: have felt.','מזהים את הנושא ובוחרים have ואת צורת V3.',section='perfect')
draft(6,'6 · ניסיון קודם','Some students have felt ... , so ...','חברו את הניסיון הקודם ליתרון של משחק משותף.','perfect')
draft(7,'7 · סיכום הדעה','In conclusion, I believe that ...','חזרו לעמדה בקצרה. אל תוסיפו טענה חדשה.','passive')
info('Passive','המלצה על מה שצריך לקרות לתלמידים.','should be + V3\ninclude → included','שומרים על מבנה קבוע ועל פועל פשוט. התלמידים מקבלים הזדמנות להשתתף.',section='passive')
gap('סביל בהמלצה','Every student should ',' in class games.',['include','be included','be include'],1,'should be + V3: should be included.','הקפידו על be ועל צורת הפועל. אין צורך בפועל ארוך יותר.',section='passive')
draft(8,'8 · המלצה בסביל','Therefore, every student should be ...','סיימו בהמלצה שתומכת בעמדה.','passive')
info('הטיוטה עדיין קצרה','יש לנו 100 מילים. נוסיף דוגמה בפסקה 2 ורעיון בפסקה 3.','100 words\nAdd an example. Add one more idea.','לא מוסיפים פסקה חמישית ולא ממלאים במילים ריקות. מרחיבים את ההסבר.',section='expand')
draft(9,'9 · דוגמה לקושי','For example, they may ...','תנו דוגמה פשוטה לטעות במשחק. היא נכנסת לפסקה 2.','expand')
draft(10,'10 · עוד יתרון','Moreover, students can ...','מה עוד לומדים ממשחק משותף? ההרחבה נכנסת לפסקה 3.','expand')
anim(12,'expand')
info('תבניות לחיבור הבא','מחליפים את הרעיון ואת מילות הנושא, ושומרים על מבנה שמתאים למשמעות.','If ..., ... will ...\nSome ... have ...\n... should be ...','אין לכפות תבנית שאינה מתאימה לנושא. playing ו־joining במודל מדגימים גם gerund, בלי להוסיף יחידת לימוד נפרדת.',section='expand')
info('נושא לתרגול עצמאי','עכשיו אתם בוחרים עמדה ומפתחים את הרעיונות.','Should teenagers have an after-school job?','שומרים על ארבע פסקאות. אין להציג חיבור מוכן לנושא זה לפני ניסיון התלמיד.',section='practice')
timer('תכנון החיבור שלכם','My opinion / An idea against / An idea for',180,'כתבו שלוש הערות קצרות. אפשר להתחיל בעברית.','עברו בין התלמידים ועזרו ברעיון אחד בלבד. מילים זמינות: work, money, time, school, tired, help.',section='practice')
timer('כתיבה עצמאית','Write 120–140 words.',840,'ארבע פסקאות. משפט אחד בכל פעם.','14 דקות כתיבה. אל תעצרו את כולם לכל שגיאה. תנו עד שני תיקונים עיקריים לתלמיד. מי שלא סיים שומר טיוטה ומסיים בהמשך.',section='write')
info('לפני העריכה','בדקו קודם את הרעיון ואת ארבע הפסקאות. אחר כך את המבנים והכתיב.','Task / reasons / examples\nIf ... will / have + V3 / should be + V3','סופרים מילים ומרחיבים בתוך הגוף אם צריך. אין לצמצם רעיון נחוץ רק כדי לפשט שפה.',section='edit')
timer('עריכה עצמית','Read your essay. Improve two things.',180,'תיקון אחד בתוכן או בהסבר, ותיקון אחד בשפה.','שלוש דקות מוגנות לעריכה. אפשר להיעזר בביטויים הקבועים, בלי להחליף אוטומטית מילים נכונות.',section='edit')
choice('כרטיס יציאה','Which sentence explains how games help?',['Games help students.','Games help students make friends since they spend time together.','Games help students since games help students.'],1,'משפט פשוט שמסביר את הרעיון עדיף על משפט שקשה להבין או להשתמש בו.',section='end')
assert len(S)==50, len(S)
assert WC==123
assert sum(s['kind']=='animation' for s in S)==3
for a,b in zip(S,S[1:]):
    if a.get('pair') and not a.get('reveal'):
        assert b.get('pair')==a['pair'] and b['reveal']
        assert a['text']==b['text'] and a.get('options')==b.get('options')
data=dict(title='Advanced Grammar in an Essay',grade='י״א · 5 יח״ל',durationMinutes=72,wordCount=WC,topic=TOPIC,sentences=SENTENCES,paragraphSteps=PARAGRAPH_STEPS,paragraphs=P,slides=S,source=SOURCE)
(OUT/'lesson.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
def mark(text,highlights):
    txt=E(text)
    for x in sorted(highlights or [],key=len,reverse=True):
        txt=txt.replace(E(x),'<em>'+E(x)+'</em>')
    return txt.replace('\n','<br>')
def body(s):
    title=E(s['title']);text=s['text'];rev=s.get('reveal',False)
    m=f'<div class="slide-meta"><div class="eyebrow">{title}</div><div class="tense">{E(s.get("tense",""))}</div></div>'
    if s['kind']=='cover':return '<div class="slide-meta"><div class="eyebrow">כיתה י״א · 5 יח״ל</div></div><h1 class="cover-title">ברוכים הבאים</h1><p class="cover-sub">ישיבת בני עקיבא קריית הרצוג</p>'
    if s['kind']=='animation':return m+f'<div class="sprite" role="img" aria-label="{E(s["alt"])}" style="background-image:url(assets/{s["asset"]}.webp)"></div><p class="en caption" lang="en">{E(text)}</p><div class="animation-controls"><button type="button" data-anim-toggle aria-label="השהיית ההנפשה">Ⅱ</button><button type="button" data-anim-replay aria-label="הפעלה מחדש">↻</button></div>'
    if s['kind']=='essay':return m+'<div class="essay en" lang="en">'+''.join('<p>'+E(p)+'</p>' for p in s['paragraphs'])+'</div><p class="he count">'+E(s['he'])+'</p>'
    if s['kind'] in ('gap','choice'):
        if s['kind']=='gap':
            w=max(len(x) for x in s['options'])+1
            ans=E(s['options'][s['correct']]) if rev else '&nbsp;'
            q=E(s['before'])+f'<span class="gap {"filled" if rev else ""}" style="--gap-ch:{w}">{ans}</span>'+E(s['after'])
        else:q=E(text)
        opts=''.join(f'<div class="choice {"correct" if rev and i==s["correct"] else ""}"><b>{chr(65+i)}</b><span>{E(x)}</span></div>' for i,x in enumerate(s['options']))
        return m+f'<h2 class="en question" lang="en">{q}</h2><div class="choices en" lang="en">{opts}</div><div class="answer-slot"><p class="he explanation">{E(s["he"])}</p></div>'
    if s['kind']=='timer':return m+f'<h2 class="en question" lang="en">{E(text)}</h2><p class="he support">{E(s["he"])}</p><div class="clock" data-seconds="{s["seconds"]}"><output aria-label="זמן שנותר">{s["seconds"]//60:02}:{s["seconds"]%60:02}</output><div class="clock-controls"><button data-timer-toggle>התחלה</button><button data-timer-reset>איפוס</button><button data-timer-add>+30 שניות</button></div></div>'
    if s['kind']=='example':return m+f'<h2 class="en example-main" lang="en">{mark(text,s.get("highlights"))}</h2><div class="answer-slot"><p class="he translation">{E(s["he"])}</p></div>'
    return m+f'<h2 class="en main-copy" lang="en">{mark(text,s.get("highlights"))}</h2><p class="he support">{E(s["he"])}</p>'
sections=''.join(f'<section class="slide {s["kind"]}{" reveal" if s.get("reveal") else ""}" data-slide="{s["n"]}" data-section="{s["section"]}"'+(f' data-pair="{s["pair"]}"' if s.get('pair') else '')+f' aria-label="שקף {s["n"]} מתוך {len(S)}" hidden><div class="frame">{body(s)}</div></section>' for s in S)
nav=''.join(f'<a href="#slide-{next(s["n"] for s in S if s["section"]==sec)}">{label}</a>' for sec,label in [('plan','תכנון'),('conditionals','דקדוק'),('intro','חיבור'),('write','כתיבה')])
index=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>י״א · Advanced Grammar in an Essay</title><link rel="stylesheet" href="../../assets/lesson-decks/deck.css"><link rel="stylesheet" href="lesson.css?v=20260919-simple72"></head><body><a class="home" href="../five-units/" aria-label="חזרה לכיתה י״א 5 יח״ל">⌂</a><nav class="lesson-sections">{nav}</nav><main class="stage">{sections}</main><nav class="nav"><div class="nav-group"><button data-step="-1" aria-label="לשקף הקודם">←</button><button data-step="1" aria-label="לשקף הבא">→</button></div><div class="progress" id="counter" aria-live="polite"></div><a class="download" href="files/grammar-in-an-essay.pptx?v=20260919-simple72">PPTX</a></nav><div class="progress-track"><div class="progress-fill"></div></div><script src="../../assets/lesson-decks/deck.js"></script><script src="lesson.js"></script></body></html>'''
(OUT/'index.html').write_text(index)
timeline=[('0–7','plan','משימה, מסגרת ומילים מוכרות'),('7–16','intro','פתיחה, דעה וטענה נגדית'),('16–25','conditionals','תנאי ראשון, since ומשפט 4'),('25–34','perfect','הטענה בעד ומשפט Present Perfect'),('34–43','passive','סיום והמלצה בסביל'),('43–50','expand','שתי הרחבות בתוך הגוף וסיכום התבניות'),('50–53','practice','תכנון בנושא עבודה אחרי הלימודים'),('53–67','write','14 דקות כתיבה עצמאית'),('67–71','edit','בדיקה ו־3 דקות עריכה'),('71–72','end','כרטיס יציאה')]
rows=''.join(f'<tr><td dir="ltr">{a}</td><td>{next(s["n"] for s in S if s["section"]==b)}</td><td>{c}</td></tr>' for a,b,c in timeline)
script=''.join(f'<details><summary>שקף {s["n"]}: {E(s["title"])}</summary><p>{E(s["note"])}</p><p class="en">{E(s["text"])}</p><a href="index.html#slide-{s["n"]}">פתיחת השקף</a></details>' for s in S)
teacher=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>תסריט למורה · Advanced Grammar in an Essay</title><style>body{{margin:0;background:#07111f;color:#f7f7f2;font:19px/1.7 Arial}}main{{max-width:960px;margin:auto;padding:32px 24px}}h1,h2{{color:#4ee5ff}}a{{color:#dfff5b}}.en{{direction:ltr;text-align:left;white-space:pre-line}}details{{border-bottom:1px solid #ffffff30;padding:14px 0}}summary{{cursor:pointer;font-weight:bold}}table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #ffffff30;text-align:right}}@media print{{body{{background:white;color:black}}a,h1,h2{{color:black}}}}</style></head><body><main><a href="../five-units/">כיתה י״א 5 יח״ל</a><h1>Advanced Grammar in an Essay</h1><p>50 שקפים, 72 דקות מתוכננות וחיבור בן 123 מילים. שלוש הפוגות מונפשות קצרות כלולות בזמנים.</p><p><a href="index.html">מצגת</a> · <a href="files/grammar-in-an-essay.pptx?v=20260919-simple72">PPTX</a></p><h2>עיקרון ההוראה</h2><p>מבנים ומילות קישור חוזרים משמשים בסיס קבוע. אוצר המילים המשתנה עם הנושא נשאר פשוט ומוכר: games, play, team, friends, help, mistakes. אין לבקש מילים קשות כשמילה מוכרת מביעה את הרעיון במדויק. מרחיבים את ההסבר ואת הדוגמה, ולא את אורך המילה.</p><p>בתרגול בוחרים since להבעת סיבה כדי ליצור הרגל שימוש. הוא אינו מזכה אוטומטית ביותר נקודות מ־because. הניקוד תלוי גם במענה למשימה, פיתוח רעיונות, ארגון, מגוון מתאים ודיוק. החיבור הוא דוגמה להוראה, ולא הבטחת ציון.</p><h2>היקף וזמן</h2><p>השיעור מתוכנן ל־72 דקות עבודה, כדי להשאיר 18 דקות מתוך מפגש של 90 דקות להפוגות בלתי מתוכננות ולמעברים. לא מלמדים מחדש את יחידת Advanced Grammar.</p><p>בכל שלב נותנים ניסיון קצר של משפט אחד ואחריו חושפים דוגמה. בשקפי החיבור המצטבר קוראים רק את המשפט שנוסף. אין לקרוא שוב את כל החיבור בכל שלב. שלוש ההפוגות הקצרות כלולות בשלבי ההוראה ואינן תוספת לזמן.</p><p>שומרים על 14 דקות כתיבה ועל 3 דקות עריכה. אם נוצר עיכוב, מקצרים שיתוף במליאה. מי שלא סיים שומר את הטיוטה להמשך; אין להציג טיוטה חלקית כחיבור שהושלם.</p><table><tr><th>דקות מתחילת השיעור</th><th>שקף פתיחה</th><th>עבודה</th></tr>{rows}</table><h2>המבנים</h2><p>First Conditional: If + Present Simple, will + verb. Present Perfect: have + V3. Passive: should be + V3. Gerund מופיע באופן טבעי ב־playing וב־joining. אין בשיעור יחידה נפרדת על תנאי שני. ארבע הפסקאות והבחירה במבנים אלה הן מסגרת תרגול; במבחן קוראים את הוראות המשימה.</p><h2>סדר הכתיבה</h2><p>1 פתיחה; 2 דעה; 3 טענה נגדית; 4 תנאי וסיבה; 5 תמיכה בדעה; 6 ניסיון קודם; 7 מסקנה; 8 סביל. אחר כך מוסיפים את משפט 9 לפסקה השנייה ואת משפט 10 לשלישית. סדר הקריאה הסופי: 1,2 / 3,4,9 / 5,6,10 / 7,8. לפני ההרחבות: 100 מילים; אחרי הראשונה: 111; בסיום: 123. אין פסקה חמישית.</p><h2>תרגול עצמאי</h2><p class="en">Should teenagers have an after-school job?</p><p>התלמיד בוחר עמדה, כותב משפט אחד בכל פעם ומשתמש במילים מוכרות כגון work, money, time, school, tired, help. משוב על התוכן קודם לשפה, עד שני תיקונים עיקריים. אין להכתיב חיבור מוכן או להבטיח ציון.</p><h2>שעונים והפוגות</h2><p>באתר השעונים מתחילים בלחיצה, ניתנים לעצירה ולהארכה ונעצרים ביציאה מהשקף. אין מעבר שקפים אוטומטי. ב־PPTX הזמן מוצג כהקצאה קבועה עם קישור לשעון באתר; הפעלת GIF תלויה בתוכנת המצגות.</p><h2>Topic</h2><p class="en">{E(TOPIC)}</p><h2>חיבור לדוגמה: {WC} מילים</h2><div class="en">{''.join('<p>'+E(p)+'</p>' for p in P)}</div><h2>תסריט לפי שקף</h2>{script}<h2>מקור משימת הכתיבה</h2><p><a href="{SOURCE}">שאלון G, קיץ 2026</a></p></main></body></html>'''
(OUT/'teacher.html').write_text(teacher)
manifest=[dict(n=s['n'],kind=s['kind'],title=s['title'],section=s['section']) for s in S]
(ROOT/'tools/grammar-in-an-essay/build/slide-list.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(f'{len(S)} slides, {WC} words, 72 minutes. '+str(OUT))

from versions import build_versions
build_versions(globals())
