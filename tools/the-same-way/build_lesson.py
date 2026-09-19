from pathlib import Path
import json,html,re,shutil
R=Path(__file__).resolve().parents[2] / 'grade7/the-same-way'
d=json.loads((R/'story.json').read_text()); slides=[]
def add(kind,title,**kw): slides.append(dict(kind=kind,title=title,**kw))
def quiz(title,q,opts,correct,why,progress=0,tense=''):
    common=dict(q=q,opts=opts,correct=correct,why=why,progress=progress,tense=tense)
    add('quiz',title,reveal=False,**common);add('quiz',title,reveal=True,**common)
add('cover','The Same Way',sub='כיתה ז׳ · אנגלית · סיפור ותרגול')
add('whole','The Same Way',sub='קריאה ראשונה: מה מדאיג את דן, ומה משתנה בסוף?',progress=0)
quiz('הרעיון המרכזי','What changes for Dan?', ['His school is closer.','He finds boys who feel like him.','The rain stops.'],1,'הדרך אינה מתקצרת. דן מגלה שהוא אינו היחיד שמרגיש כך.')
add('bridge','מה כבר מוכר לנו?',text='To Be: I am · The school is · The boys are',sub='נשתמש במה שלמדנו כדי להבין את הדמויות ואת הרגשות שלהן.',tense='הווה')
quiz('חזרה: To Be','Dan ___ in Grade 7.', ['am','is','are'],1,'Dan = he → is. גם כשבעברית אין פועל, באנגלית צריך is.',tense='הווה')
add('bridge','מילים מקבוצה 01',text='lift · take something out · then · break · meet · join',sub='חלק מהמילים כבר פגשנו. נזהה אותן בתוך הסיפור; מילה שעדיין לא נלמדה נקרא יחד.')
add('bridge','תמיכה בקריאה',text='chose = בחרתי / בחר\njourney = דרך / מסע\nworry = לדאוג · wet = רטוב',sub='chose מספר על בחירה שכבר נעשתה. רוב הסיפור מתאר את הדרך ואת היום בבית הספר.')
questions={
4:('הבחירה של דן','Why did Dan choose this school?', ['It is near his home.','He loves its science lessons.','His brother studies there.'],1,'חפשו את הסיבה בפסקה A: because I love its science lessons.'),
10:('הילדים בדרך','Do the boys talk on the way?', ['Yes, about school.','No, they do not talk.','The story does not say.'],1,'בפסקה B כתוב במפורש: we do not talk. בשלב זה הוא עדיין לא יודע שהם בכיתה שלו.'),
15:('עכשיו או בעתיד?','Are Dan’s books wet now?', ['Yes, it is raining now.','No, he is thinking about winter.','He has no books.'],1,'Today the sky is blue. הספרים הרטובים הם חשש לעתיד, לא עובדה בהווה.'),
18:('הרמזים מתחברים','Why does Dan stop at the door?', ['He sees the boys from the journey.','His brother is there.','The door is locked.'],0,'התיק הירוק והכובע האדום חוזרים בפסקה D ומאפשרים לדן לזהות את הבנים.'),
23:('רגשות משותפים','What do Dan and Ben both worry about?', ['The science test.','The rain.','A red cap.'],1,'דן שואל מה יקרה בגשם; בן אומר: I worry about the rain.'),
28:('מה נפתר ומה נשאר?','Which sentence is true at the end?', ['The journey is short now.','They know exactly what to do in the rain.','Dan can travel with new friends.'],2,'נוצר קשר עם חברים. הסיפור אומר במפורש שהגשם עדיין בעיה.')}
for s in d['sentences']:
    for reveal in [False,True]: add('sentence','קריאה מקרוב',**s,reveal=reveal,progress=s['n'],tense=('עתיד' if s['n'] in [13,28] else 'הווה' if s['n'] in [1,3,4,5,6,7,8,9,10,11,14,15,16,17,18,19,20,21,22,23,24,25,26,27] else ''))
    n=s['n']
    if n in questions:
        t,q,opts,c,w=questions[n];quiz(t,q,opts,c,w,progress=n)
    if n==7:
        for rev in [False,True]:add('route','מסדרים את הדרך',reveal=rev,progress=n)
    if n==10:
        add('grammar','To Be בתוך הסיפור',text='The bag is green.\nThe boys are quiet.',sub='שם עצם יחיד → is. רבים → are. חזרו למצגת To Be: הפועל מתאר מצב.',progress=n,tense='הווה')
        quiz('מתרגלים את ההתאמה','The boys ___ near Dan.', ['am','is','are'],2,'The boys = they → are.',progress=n,tense='הווה')
    if n==15:
        add('pause','Rain plan?',sub='התנחתא קצרה · חוזרים כשמוכנים',progress=n)
        add('grammar','הווה ועתיד עם To Be',text='Now: The sky is blue.\nWinter: My books will be wet.',sub='is מתאר את המצב עכשיו. will be מתאר את המצב שדן חושש ממנו בעתיד.',progress=n)
    if n==23:
        quiz('כינויי גוף','“Are you tired too?” — Who is “you”?', ['Dan’s brother','Ben and Noam','Dan’s books'],1,'דן פונה לשני הבנים. you יכול להיות גם אתם.',progress=n)
add('pair','הסיפור שלכם',text='I am ___ on the way to school.\nMy journey is ___.',sub='חשבו לבד, ואז שתפו בן זוג. אפשר לבחור: tired / happy / worried · short / long.',progress=28)
add('review','בודקים את הסיפור שלכם',heading='האם המשפטים מתאימים למה שרציתם לומר?',answers=[{'label': '1. רגש בדרך לבית הספר', 'en': 'I am tired on the way to school.', 'he': 'זו דוגמה בלבד. גם happy או worried מתאימים אם כך אתם מרגישים. בדקו: I + am + רגש.'}, {'label': '2. תיאור הדרך', 'en': 'My journey is long.', 'he': 'אפשר גם short, בהתאם לדרך שלכם. בדקו: My journey + is + תיאור. אם שני המשפטים מביעים את כוונתכם והשתמשתם ב־am וב־is נכון — הצלחתם.'}],progress=28)
add('work','עבודה בדף המודפס',text='Read → Find evidence → Answer',sub='עבדו לבד 8 דקות. חזרו לפסקה המתאימה לפני כל תשובה. לאחר מכן השוו בזוגות.',progress=28)
add('review','בודקים את דף העבודה',heading='משווים, מתקנים ומוצאים ראיה',answers=[{'label': '1. הבחירה בבית הספר', 'en': 'He loves its science lessons.', 'he': 'מצאתם את שיעורי המדעים כסיבה? נכון. בדקו בפסקה A.'}, {'label': '2. סדר הדרך', 'en': '1. Walk to the bus stop\n2. First bus\n3. Train\n4. Second bus\n5. Walk to school', 'he': 'בדף, לפי סדר הפריטים המודפסים: 3, 2, 5, 4, 1. תקנו כל מספר שונה ובדקו בפסקה B.'}, {'label': '3. האם דן ידע מראש?', 'en': 'False. “The boys from the journey are in my class.”', 'he': 'דן מגלה שהם בכיתתו רק כשהוא מגיע. אפשר לצטט גם את העצירה בפתח הכיתה. we do not talk לבדו אינו מראה בבירור שהוא לא ידע.'}, {'label': '4. הדאגה המשותפת', 'en': 'The rain / What will happen when it rains.', 'he': 'אם ציינתם את הגשם — נכון. הספרים אינם רטובים עכשיו: זהו החשש לחורף.'}, {'label': '5. To Be', 'en': 'Dan is tired. The boys are in his class.', 'he': 'Dan = he → is; The boys = they → are. סמנו ותקנו כל התאמה שונה.'}, {'label': '6. מה השתנה ומה נשאר?', 'en': 'Dan has new friends to travel with. The rain is still a problem.', 'he': 'בתשובה מלאה מופיעים שני הדברים: חברים חדשים, ובעיית הגשם שנותרה. אם חסר חלק — הוסיפו אותו.'}],progress=28)
add('exit','לפני שיוצאים',text='1. Dan is ___. The boys are ___.\n2. What is still a problem?\n3. Which sentence helped you understand?',sub='ענו בעל פה או במחברת. תשובה + פרט מן הסיפור.',progress=28)
add('review','בודקים לפני שיוצאים',heading='שלוש תשובות — בדיקה עצמית',answers=[{'label': '1. משפטים עם To Be — דוגמה', 'en': 'Dan is tired. The boys are in his class.', 'he': 'גם השלמות אחרות נכונות מתקבלות אם הן מתאימות לסיפור. בדקו: Dan + is, The boys + are.'}, {'label': '2. מה עדיין בעיה?', 'en': 'The rain is still a problem.', 'he': 'גשם או הדרך בגשם הם התשובה. אם כתבתם שהדרך התקצרה או שהגשם נפתר — תקנו לפי פסקה E.'}, {'label': '3. משפט שעזר להבין — דוגמה', 'en': '“The boys from the journey are in my class.”', 'he': 'למשל: המשפט מראה שהילדים מהדרך הם חבריו לכיתה. בחרתם משפט אחר וציינתם מה הבנתם ממנו? גם זו תשובה מתאימה. ודאו שיש ציטוט והסבר, והשלימו אם חסר.'}],progress=28)
add('links','חזרה קצרה בבית',sub='קראו שוב את הסיפור ותרגלו את המילים שבחרנו מתוך קבוצה 01.',progress=28)
# Retain the approved ten-page Read Alone Text addition on rebuild.
reading=json.loads((R/'reading.json').read_text())
slides[2:2]=[dict(kind='readalong',title='Read Alone Text',page=n,progress=max(i+1 for i,x in enumerate(reading['sentences']) if x['paragraph']==n)) for n in range(len(reading['pages']))]
(R/'slides.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2))
(R/'data.js').write_text('const STORY='+json.dumps(d,ensure_ascii=False)+';\nconst SLIDES='+json.dumps(slides,ensure_ascii=False)+';\n')
print('Slides',len(slides))
# One A4 page: text and tasks continue on the SAME page.
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
normal=ParagraphStyle('normal',fontName='DejaVu',fontSize=11.3,leading=15,spaceAfter=5)
small=ParagraphStyle('small',parent=normal,fontSize=9,leading=12)
head=ParagraphStyle('head',parent=normal,fontName='DejaVuB',fontSize=20,leading=25,spaceAfter=5)
sub=ParagraphStyle('sub',parent=normal,fontName='DejaVuB',fontSize=11.3,spaceBefore=6,spaceAfter=5)
P=lambda x,style=normal:Paragraph(x,style)
items=[P('The Same Way',head),P('Grade 7 · Reading practice     Name: ____________________',small),Spacer(1,7)]
for i,p in enumerate(d['paragraphs']):items.append(P(f'<b>{chr(65+i)}</b>  '+html.escape(p)))
items.extend([P('Word help: chose = picked / selected; journey = the way from one place to another.',small),P('Read, think and answer',sub)])
tasks=[
'<b>1.</b> Why does Dan like his new school? (A)<br/>_________________________________________________________________',
'<b>2.</b> Number the journey: train ___  first bus ___  walk to school ___<br/>second bus ___  walk to the bus stop ___  (B)',
'<b>3.</b> Dan knows the boys are in his class before he reaches school. (B, D)<br/>Circle: True / False. Copy a clue: __________________________________',
'<b>4.</b> What do Dan and Ben both worry about? (C, D)<br/>_________________________________________________________________',
'<b>5.</b> Circle: Dan <b>am / is / are</b> tired. The boys <b>am / is / are</b> in his class.',
'<b>6.</b> What changes at the end? What is still a problem? (E)<br/>_________________________________________________________________<br/>_________________________________________________________________'
]
for task in tasks:items.extend([P(task,ParagraphStyle('task',parent=normal,fontSize=10,leading=14,spaceAfter=7))])
doc=SimpleDocTemplate(str(R/'files/the-same-way-worksheet.pdf'),pagesize=(595.28,841.89),leftMargin=40,rightMargin=40,topMargin=30,bottomMargin=28)
doc.build(items)
# Teacher notes: no private exam text or answer-key link in the student navigation.
notes='''# The Same Way — תסריט מורה

קהל: כיתה ז׳ בתחילת השנה, ברמת הקבצה א׳ לפי הבקשה. השיוך ביומן נשאר ז׳2; אין כאן שינוי שיבוץ.

## קשר לחומר קודם
מצגת הפתיחה To Be: התאמת am/is/are לכינויי גוף, משפטי מצב, will be. מצגת הקבוצה 01: lift, take something out, then, break, meet, join. רק תחילת הקבוצה תועדה כנלמדת; אין להציג את ששת הערכים כולם כמילים שכבר הוקנו. שואלים מי מזהה, ומשלימים הוראה קצרה לפי הצורך.
הסיפור מקורי ונכתב במיוחד. הדקדוק בהווה פשוט בעיקרו; chose מוצג כפריט להבנה בלבד. משפטי will/when מובנים בעזרת ההקשר, ללא הוראת כללי תנאי חדשים. אין לערבב את יעד כתיבת מודול G של י״א בשיעור ז׳.

## בסיס להשוואת אורך
נמצא ב־Drive בתיקיית ז/OCT צילום הקטע On the Way to School ודף Questions.docx. זוהי נקודת ייחוס מוקדמת בארכיון שנת תשפ״ו; לא ניתן לאמת מהקבצים לבדם שזה היה המבחן הראשון בפועל. מחברת ז׳ תשפ״ו קושרת את המבחן בנובמבר ל־Got Talent, עמ׳ 46; נמצא גם TEST DEC.docx שעודכן בנובמבר ובו אותו קטע. הסיפור החדש הוא 268 מילים, בסדר גודל דומה לקטע הדרך לבית הספר, עם משפטים קצרים יותר וקריאה מתווכת. אין לצרף לאתר צילום של מבחן הארכיון.

## תכנון 72 דקות בתוך מפגש של 80 דקות
0–4 פתיחה והפעלת ידע קודם בעל פה: מה אתם רואים בדרך? אין לחשוף את הסיום.
4–9 הסיפור המלא: קריאה שקטה לחיפוש דאגה ושינוי. אין צורך להבין כל מילה. בוחרים תשובה לשאלת הרעיון המרכזי.
9–16 גשר ל־To Be ותמיכת מילים; תלמידים מנסים לפני הסבר. אם מילה אינה מוכרת — מדגימים ולא בוחנים עליה כידע קודם.
16–29 פסקאות A–B: משפט באנגלית, ניסיון להבין, ואז שקף תרגום. מסדרים את הנסיעה ובודקים עם הטקסט. שני תרגילי To Be קצרים.
29–39 פסקה C: הבחנה בין עובדה עכשיו לחשש לעתיד. התנחתת התמונה 30–45 שניות, ללא מעבר אוטומטי.
39–53 פסקאות D–E: איתור הרמזים, זיהוי הדוברים, רגשות משותפים. מדגישים שהקשר החברתי השתנה אך לא נפתרה בעיית הגשם.
53–56 משפטים בזוגות על הדרך שלהם, עם מסגרת ותמיכה.
56–64 עבודה עצמאית בדף.
64–69 בדיקה בזוגות ודיון בראיות מן הטקסט.
69–72 בדיקת יציאה. שמונה הדקות הנותרות שמורות להפרעות ולמעברים.

## הוראה ומשוב
בכל שאלה: 5–10 שניות לחשיבה אישית; בחירה בלחיצה אינה מסמנת נכונות. רק בשקף הבא מופיעים הפתרון והנימוק. אם תלמיד טועה, מבקשים לחפש רמז בפסקה, ולא נותנים רק ציון. זוגות: אחד קורא ואחד מוצא ראיה, ואז מתחלפים.
סימון התקדמות הקריאה מראה משפט מתוך 28 ופסקה A–E. במעבר לשקף תרגום האנגלית נשארת באותו מקום. בתפריט ניתן לחזור לסיפור המלא ולכל פסקה.
תמיכה: דף מודפס פתוח, קריאה בהד של משפטים, תשובות קצרות, הצבעה על הרמז. אתגר: להסביר כיצד התיק הירוק והכובע האדום עוזרים לקורא ולדן. אין לבקש כתובות בית או מסלולים אישיים מדויקים.

## מפתח לדף
1. He loves its science lessons.
2. train 3; first bus 2; walk to school 5; second bus 4; walk to the bus stop 1.
3. False. Accept: “At school, I open the classroom door and stop”; “The boys from the journey are in my class.” The surprise is an inference from D; “we do not talk” alone is weaker evidence.
4. The rain / what will happen when it rains.
5. is; are.
6. He has new friends / can travel with Ben and Noam. The rain is still a problem.
מקבלים ניסוחים חלופיים נכונים. בשאלות תוכן מתקנים תחילה הבנה; לא פוסלים תשובה מובנת בשל שגיאת כתיב קלה.

## שימוש
חצים ימינה/למטה: קדימה; שמאלה/למעלה: אחורה. גם כפתורים, גלילת עכבר והחלקה. עשרת דפי Read Alone Text נוספו לאחר הסיפור המלא, בלי למחוק אף שקף. ההקראה המוקלטת מתחילה בלחיצה ומעבירה דפים אוטומטית; מעבר ידני משהה. אין הקראת דפדפן. אפשר לבחור בהאזנה במקום חלק מן הקריאה בהד, תוך שמירה על מסגרת 72 הדקות. הפעילויות והבחירות נשמרות בזיכרון ההפעלה בלבד; מספר השקף נשמר מקומית במכשיר.
'''
(R/'teacher-notes.md').write_text(notes)
