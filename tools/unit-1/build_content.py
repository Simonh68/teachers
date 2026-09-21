from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2]/'grade7/unit-1/reading'
texts=[dict(title='Rainy Morning? Come Inside!',label='הודעה',lines=[
('A message for Grade 7 students.','הודעה לתלמידי כיתה ז׳.'),
('On rainy mornings, Room 4 is open from 7:30.','בבקרים גשומים חדר 4 פתוח משעה 7:30.'),
('There are chairs and tables in the room.','יש כיסאות ושולחנות בחדר.'),
('There is a place for wet umbrellas near the door.','יש מקום למטריות רטובות ליד הדלת.'),
('You can wait here with your friends.','אתם יכולים לחכות כאן עם החברים שלכם.'),
('Please put your bags under the tables.','בבקשה הניחו את התיקים שלכם מתחת לשולחנות.'),
('Lessons start at 8:00.','השיעורים מתחילים בשעה 8:00.')]),
dict(title='Different Ways to School',label='קטע מידע',lines=[
('Children get to school in different ways.','ילדים מגיעים לבית הספר בדרכים שונות.'),
('Some walk.','חלקם הולכים ברגל.'),
('Some take a bus or a train.','חלקם נוסעים באוטובוס או ברכבת.'),
('A school near home is easy to get to.','קל להגיע לבית ספר שנמצא קרוב לבית.'),
('But some children choose a school far away.','אבל חלק מהילדים בוחרים בבית ספר רחוק.'),
('They want to study music, science or another subject they like.','הם רוצים ללמוד מוזיקה, מדעים או מקצוע אחר שהם אוהבים.'),
('A long journey takes time.','נסיעה ארוכה דורשת זמן.'),
('On rainy days, the journey can be harder.','בימים גשומים הנסיעה יכולה להיות קשה יותר.'),
('Some children travel with friends.','חלק מהילדים נוסעים עם חברים.'),
('They talk on the way.','הם מדברים בדרך.'),
('They are tired when they arrive, but they are happy to be together.','הם עייפים כשהם מגיעים, אבל הם שמחים להיות יחד.')])]
G={'a':'אחד / אחת; לפני שם עצם לא מיודע','message':'הודעה','for':'ל־ / עבור','grade':'כיתה','7':'שבע; כיתה ז׳','students':'תלמידים','on':'ב־; כאן לפני זמן','rainy':'גשומים','mornings':'בקרים','room':'חדר','4':'ארבע','is':'הוא / פתוח; פועל קישור','open':'פתוח','from':'מ־ / החל ב־','7:30':'שבע וחצי','there':'חלק מהמבנה: יש','are':'יש ברבים / הם, לפי המשפט','chairs':'כיסאות','and':'ו־','tables':'שולחנות','in':'ב־ / בתוך','the':'ה־','place':'מקום','wet':'רטובות','umbrellas':'מטריות','near':'ליד / קרוב','door':'דלת','you':'אתם','can':'יכולים / יכול','wait':'לחכות','here':'כאן','with':'עם','your':'שלכם','friends':'חברים','please':'בבקשה','put':'הניחו','bags':'תיקים','under':'מתחת ל־','lessons':'שיעורים','start':'מתחילים','at':'בשעה','8:00':'שמונה','children':'ילדים','get':'מגיעים; חלק מ־get to','to':'ל־; או חלק מצורת הפועל','school':'בית ספר','different':'שונות','ways':'דרכים','some':'חלק / חלקם','walk':'הולכים ברגל','take':'נוסעים ב־; כאן עם אוטובוס ורכבת','bus':'אוטובוס','or':'או','train':'רכבת','home':'בית','easy':'קל','but':'אבל','choose':'בוחרים','far':'רחוק; חלק מ־far away','away':'חלק מהביטוי far away: רחוק','they':'הם','want':'רוצים','study':'ללמוד','music':'מוזיקה','science':'מדעים','another':'אחר','subject':'מקצוע לימוד','like':'אוהבים','long':'ארוכה','journey':'נסיעה / מסע','takes':'דורשת / לוקחת','time':'זמן','days':'ימים','be':'להיות','harder':'קשה יותר','travel':'נוסעים','talk':'מדברים','way':'דרך','tired':'עייפים','when':'כאשר','arrive':'מגיעים','happy':'שמחים','together':'יחד'}
sentences=[]
for t in texts:
 t['ids']=[]
 for en,he in t['lines']:
  words=[]
  for w in en.split():
   k=re.sub(r'[^a-z0-9:]','',w.lower());assert k in G,k
   meaning=G[k]
   if k=='is' and en.startswith('There is'):meaning='יש ביחיד; חלק מ־there is'
   if k=='on' and 'on the way' in en:meaning='חלק מהביטוי on the way: בדרך'
   if k=='are':meaning='יש ברבים' if en.startswith('There are') else 'הם; פועל קישור'
   words.append(dict(word=w,he=meaning))
  t['ids'].append(len(sentences));sentences.append(dict(en=en,he=he,words=words))
qs=[
 dict(id='1',title='למי ההודעה?',q='למי מיועדת ההודעה?',opts=['לתלמידי כיתה ז׳','לנהגי האוטובוס','להורים בלבד'],correct=0,evidence='A message for Grade 7 students.',why='הכותרת המשנית מציינת במפורש את קהל היעד.'),
 dict(id='2',title='משתמשים בזמן ובמקום',q='הגעתם ביום גשום בשעה 7:40. לאן תוכלו להיכנס?',opts=['לחדר 8','לחדר 4','אין חדר פתוח'],correct=1,evidence='On rainy mornings, Room 4 is open from 7:30.',why='7:40 מאוחר מ־7:30, ולכן החדר כבר פתוח. 8:00 היא שעת תחילת השיעורים.'),
 dict(id='3',title='קוראים כדי לפעול',q='היכן מניחים את התיקים?',opts=['ליד הדלת','על השולחנות','מתחת לשולחנות'],correct=2,evidence='Please put your bags under the tables.',why='under פירושו מתחת. ליד הדלת נמצא המקום למטריות, לא לתיקים.'),
 dict(id='5',title='הרעיון המרכזי',q='מה הנושא המרכזי בקטע המידע?',opts=['דרכים להגיע לבית הספר','שיעורי מוזיקה בלבד','משחקים ברכבת'],correct=0,evidence='Children get to school in different ways.',why='המשפט הראשון מציג את הנושא. מוזיקה היא רק דוגמה לסיבה לבחירת בית ספר.'),
 dict(id='6',title='מוצאים סיבה',q='מדוע חלק מהילדים בוחרים בית ספר רחוק?',opts=['כדי לחכות בגשם','כדי ללמוד מקצוע שהם אוהבים','כדי להגיע עייפים'],correct=1,evidence='They want to study music, science or another subject they like.',why='המשפט מסביר את הסיבה לבחירה. עייפות היא קושי בדרך ולא מטרת הבחירה.'),
 dict(id='7',title='למי הכוונה?',q='למי מתייחסת They במשפט They talk on the way?',opts=['למורים','לנהגים','לילדים שנוסעים עם חברים'],correct=2,evidence='Some children travel with friends. They talk on the way.',why='חוזרים למשפט הקודם כדי לזהות על מי מדובר.'),
 dict(id='8',title='מחברים בין טקסטים',q='מה משותף לקטע המידע ולסיפור The Same Way?',opts=['הדרך לבית ספר רחוק והחברים בדרך','כל הילדים לומדים מוזיקה','כל הילדים הולכים רק ברגל'],correct=0,evidence='Some children travel with friends.',why='גם בסיפור וגם בקטע יש נסיעה לבית הספר וחברות. דרכי הנסיעה והפרטים אינם זהים בהכרח.')]
exitText='A message for Grade 7 students. On Tuesday, Room 6 is open from 7:20. Please put your bags near the door. Lessons start at 8:00.'
exitQs=[dict(id='9',title='הודעה חדשה',q='ביום שלישי הגעתם בשעה 7:25. איזה חדר פתוח?',opts=['Room 4','Room 6','Room 8'],correct=1,evidence='On Tuesday, Room 6 is open from 7:20.',why='זו הודעה חדשה: החדר הוא 6, ושעת ההגעה אחרי 7:20.'),dict(id='10',title='פרט חדש',q='לפי ההודעה החדשה, היכן מניחים תיקים?',opts=['מתחת לשולחנות','ליד הדלת','מחוץ לבית הספר'],correct=1,evidence='Please put your bags near the door.',why='קוראים את ההודעה החדשה. המיקום השתנה ביחס להודעה הראשונה.')]
slides=[]
def add(kind,title,section='מתחילים',**kw):slides.append(dict(kind=kind,title=title,section=section,**kw))
def quiz(q,section,home=True):
 for reveal in [False,True]:
  add('quiz',q['title'],section,**{k:v for k,v in q.items() if k!='title'},reveal=reveal,context='דף העבודה · שאלה '+q['id'],home=home)
add('cover','קוראים כדי להבין ולפעול',home=True)
add('task','הדף מוביל את השיעור',prompt='פתחו את דף העבודה. עמוד 1: הודעה ומשימות 1–4. עמוד 2: קטע מידע ומשימות 5–8. פתרו תחילה לבד וסמנו ראיות בטקסט. המורה יסביר מילים לפי הצורך. את משימות 9–10 פותרים רק בסיום.',home=False)
for q in qs:quiz(q,'בדיקת דף העבודה',home=False)
add('review','משימה 4 · הודעה שכתבתם','בדיקת דף העבודה',model='Room 5 is open from 7:30.\nThere are chairs in the room.\nPlease put your bags under the tables.',check='זו דוגמה. בדקו שהודעתכם כוללת חדר ושעה, מה יש בחדר והוראה היכן להניח תיקים. גם נתונים אחרים מתקבלים אם ההודעה ברורה.',home=False)
add('task','לפני שקפי הפתרון הבאים','יישום חדש',prompt='פתרו בדף רק את משימות 9–10 לפי ההודעה החדשה בשקף הבא. עבדו לבד. המורה אוסף את הדפים לפני חשיפת הפתרונות.',home=False)
add('reading','A New Message','יישום חדש',text=exitText,sub='משימות 9–10 בדף: איזה חדר פתוח ב־7:25? איפה מניחים תיקים? Tuesday = יום שלישי; near = ליד; from = החל ב־.',home=False)
add('collect','אוספים את הדפים','יישום חדש',sub='מסרו את הדפים לפני הבדיקה. במשימות 9–10 בודקים שימוש במידע חדש, ולא זיכרון של ההודעה הקודמת.',home=False)
for q in exitQs:quiz(q,'יישום חדש',False)
for t in texts:
 sec=t['label']+' · קריאה'
 add('reading',t['title'],sec,text=' '.join(x[0] for x in t['lines']),sub='קראו תחילה את הטקסט המלא. בהמשך: קריאה מלווה בחלקים. טקסט מקורי לתרגול; אינו הודעה של בית הספר.',home=True)
 chunks=[];chunk=[]
 for sid in t['ids']:
  if chunk and sum(len(sentences[x]['words']) for x in chunk)+len(sentences[sid]['words'])>13:chunks.append(chunk);chunk=[]
  chunk.append(sid)
 if chunk:chunks.append(chunk)
 for n,ids in enumerate(chunks):add('reader',t['title'],sec,ids=ids,tab=n,tabs=len(chunks),home=True)
 for sid in t['ids']:
  for reveal in [False,True]:add('sentence',t['title'],sec,n=sid,en=sentences[sid]['en'],he=sentences[sid]['he'],reveal=reveal,home=False)
 for q in (qs[:3] if t is texts[0] else qs[3:6]):quiz(q,sec+' · בודקים',True)
add('reading','A New Message','חזרה בבית · יישום',text=exitText,sub='הודעה חדשה. נסו לענות לפי הפרטים שבה. Tuesday = יום שלישי; near = ליד; from = החל ב־.',home=True)
for q in exitQs:quiz(q,'חזרה בבית · יישום',True)
add('finish','מה עוזר לנו לקרוא?',text='Notice → What should I do?\nInformation → What can I learn?',sub='הודעה: מחפשים למי, מתי, איפה ומה לעשות. קטע מידע: מזהים נושא, סיבה ופרטים. חזרו לשאלה שהייתה קשה ומצאו את הראיה.',section='מסיימים',home=True)
data=dict(title='Unit 1 · Reading Workshop',created='יום שני, י׳ בתשרי תשפ״ז (21.9.2026)',sentences=sentences,slides=slides,sections=list(dict.fromkeys(s['section'] for s in slides)),texts=texts,questions=qs,exitText=exitText,exitQuestions=exitQs)
(R/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(R/'data.js').write_text('const LESSON='+json.dumps(data,ensure_ascii=False)+';\n')
print('slides',len(slides),'sentences',len(sentences))
