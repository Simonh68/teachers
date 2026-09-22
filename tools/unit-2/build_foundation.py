"""Build the review draft from approved scope and exact Core I records.

The rejected poster story is never imported. Recorded audio and complete
Read Alone playback remain separate completion gates, explicitly labelled.
"""
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

calendar=[
 dict(place='Japan',scope='דפוס כללי בבתי ספר; התאריכים משתנים',start='April',end='Late March',summer='About six weeks',detail='בקירוב 20 ביולי–31 באוגוסט. חופשת הקיץ בתוך שנת הלימודים.',sources=['https://web-japan.org/kidsweb/explore/schools/q4.html','https://web-japan.org/kidsweb/explore/calendar/april/schoolyear.html']),
 dict(place='Alaska, USA',scope='Anchorage, grades 7–8, 2026–27',start='20 August 2026',end='28 May 2027',summer='76 days in 2027',detail='29 במאי–12 באוגוסט; שנת 2027–28 מתחילה לכיתות 7–8 ב־13 באוגוסט. כ־11 שבועות; מחושב בין ימי הלימוד.',sources=['https://www.asdk12.org/calendar','https://resources.finalsite.net/images/v1775748418/asdk12org/zar08maexobk2er6upcg/27-28_Accessible.pdf']),
 dict(place='Florida, USA',scope='Miami-Dade: school year 2026–27; summer example 2026',start='13 August 2026',end='3 June 2027',summer='69 days in summer 2026',detail='דוגמת חופשה מאומתת: 5 ביוני–12 באוגוסט 2026, בין 4 ביוני ל־13 באוגוסט. אין להציג נתון זה כאורך קיץ 2027.',sources=['https://api.dadeschools.net/WMSFiles/392/calendars/25-26/School-Calendars-2026-2027-Elementary.pdf','https://api.dadeschools.net/WMSFiles/392/calendars/26-25/School-Calendars-2025-2026-Elementary-Secondary.pdf']),
 dict(place='England',scope='Kent council term calendar, 2026–27; INSET days vary',start='1 September 2026',end='21 July 2027',summer='41 days in 2027',detail='22 ביולי–31 באוגוסט: כמעט שישה שבועות. אלו מועדי הרשות; בית הספר עשוי להוסיף ימי הכשרת צוות.',sources=['https://www.kent.gov.uk/education-and-children/schools/term-dates']),
 dict(place='United Arab Emirates',scope='בתי ספר ציבוריים לפי לוח משרד החינוך, 2026–27',start='31 August 2026',end='2 July 2027',summer='58 days in 2027',detail='3 ביולי–29 באוגוסט; חזרה ב־30 באוגוסט. מעט יותר משמונה שבועות.',sources=['https://moe.gov.ae/en/mediacenter/news/Pages/MOE-announces-the-academic-calendar-for-the-next-3-years.aspx']),
 dict(place='Jersey',scope='דוגמת אי מוצעת; לוח ממשלתי 2026–27, לפני התאמות INSET',start='7 September 2026',end='20 July 2027',summer='47 days in 2027',detail='21 ביולי–5 בספטמבר, לפי תחילת סמסטר ב־6 בספטמבר. ימי INSET עשויים להאריך את חופשת התלמידים. אנגלית היא השפה העיקרית באי.',sources=['https://www.gov.je/Education/Schools/SchoolLife/pages/termdates.aspx','https://www.gov.je/Leisure/Jersey/pages/profile.aspx'])
]
main_sections=[
 ('One World, Different School Years', 'Does every school year start in September? No. School calendars are different. The country, the school and the season all matter.', 'האם כל שנת לימודים מתחילה בספטמבר? לא. לוחות הלימודים שונים. למדינה, לבית הספר ולעונה יש חשיבות.'),
 ('Japan', 'In Japan, the school year starts in April, in spring. It ends in late March. Summer vacation is in the middle of the school year. At many schools, it lasts approximately six weeks, from late July to the end of August.', 'ביפן שנת הלימודים מתחילה באפריל, באביב, ומסתיימת בסוף מרץ. חופשת הקיץ נמצאת באמצע שנת הלימודים. בבתי ספר רבים היא נמשכת בערך שישה שבועות, מסוף יולי עד סוף אוגוסט.'),
 ('Alaska and Florida', 'Even in one country, schools follow different calendars. In Anchorage, Alaska, Grade 7 starts on August 20 in 2026 and finishes on May 28 in 2027. Its next summer vacation is about eleven weeks. In Miami-Dade, Florida, school starts on August 13 in 2026 and ends on June 3 in 2027. For a summer example, the 2026 vacation is about ten weeks.', 'גם באותה מדינה בתי ספר פועלים לפי לוחות שונים. באנקורג׳ שבאלסקה כיתה ז׳ מתחילה ב־20 באוגוסט 2026 ומסיימת ב־28 במאי 2027. חופשת הקיץ שאחריה נמשכת כ־11 שבועות. במיאמי־דייד שבפלורידה הלימודים מתחילים ב־13 באוגוסט 2026 ומסתיימים ב־3 ביוני 2027. כדוגמה לחופשת קיץ, החופשה בשנת 2026 נמשכת כעשרה שבועות.'),
 ('England', 'According to the Kent calendar, the 2026 school year starts in September and ends in July 2027. The summer holiday lasts almost six weeks. Individual schools also have days for teacher training.', 'לפי לוח מחוז קנט, שנת הלימודים מתחילה בספטמבר 2026 ומסתיימת ביולי 2027. חופשת הקיץ נמשכת כמעט שישה שבועות. לבתי ספר יש גם ימי הכשרת מורים.'),
 ('The United Arab Emirates', 'In UAE public schools, the year starts on August 31 in 2026 and ends on July 2 in 2027. Summer vacation lasts a little more than eight weeks. Students return on August 30.', 'בבתי הספר הציבוריים באיחוד האמירויות השנה מתחילה ב־31 באוגוסט 2026 ומסתיימת ב־2 ביולי 2027. חופשת הקיץ נמשכת מעט יותר משמונה שבועות. התלמידים חוזרים ב־30 באוגוסט.'),
 ('A Small Island', 'Jersey is a small island where English is the main language. Its 2026–27 calendar runs from September to July. The summer break is nearly seven weeks, before extra teacher-training days. A small island has its own school calendar, too.', 'ג׳רזי הוא אי קטן שבו אנגלית היא השפה העיקרית. לוח הלימודים שלו לשנת 2026–27 נמשך מספטמבר עד יולי. חופשת הקיץ היא כמעט שבעה שבועות, לפני ימי הכשרת צוות נוספים. גם לאי קטן יש לוח לימודים משלו.'),
 ('Seasons and School', 'April brings a new school year in Japan. In the other examples, students begin in August or September. Summer vacation and the end of a school year are not always the same event.', 'אפריל מביא שנת לימודים חדשה ביפן. בדוגמאות האחרות מתחילים באוגוסט או בספטמבר. חופשת הקיץ וסיום שנת הלימודים לא תמיד חלים יחד.')
]
stories=[
 dict(title='A Snow Day, a Screen and a Shovel',place='Anchorage, Alaska, USA',period='9 November 2023; reported by KTUU on 10 November',mode='school journey cancelled',
 en='It is November 9, 2023. A snowstorm makes the roads in Anchorage dangerous. Kali cannot go to school today. Her teacher reads a story to the class online, from his couch. The book is about a snowy day! Kali misses school and finds online learning harder. She also goes outside to clear snow from the driveway. She wants to earn some money.',
 he='9 בנובמבר 2023. סופת שלג הופכת את הכבישים באנקורג׳ למסוכנים. קאלי אינה יכולה להגיע היום לבית הספר. המורה שלה מקריא לכיתה סיפור באינטרנט, מהספה שלו. הספר עוסק ביום מושלג! קאלי מתגעגעת לבית הספר וקשה לה יותר ללמוד מרחוק. היא גם יוצאת החוצה לפנות שלג משביל הגישה. היא רוצה להרוויח קצת כסף.',
 source='https://www.alaskasnewssource.com/2023/11/10/traditional-snow-day-is-now-remote-learning-day/',
 questions=[['Why does Kali stay home?','The storm makes the roads dangerous.'],['Where does her teacher read?','On his couch, online.'],['Why does Kali clear the snow?','She wants to earn money.']],
 targets=[],note='אירוע מתועד המסופר בהווה סיפורי. אין להסיק שקאלי בדרך כלל נוסעת באוטובוס או שכך פועלים כיום בכל יום שלג.'),
 dict(title='A Horse Before Class',place='Argentina',period='On the Way to School, documentary, 2013',mode='horse',
 en='Carlito lives in Patagonia, Argentina. His school is eighteen kilometres from home. Every school day, he rides a horse through the mountains. His little sister Micaela goes with him. Their horse is called Chiverito. The weather can make the journey difficult. Carlito wants to become a vet.',
 he='קרליטו גר בפטגוניה שבארגנטינה. בית הספר שלו נמצא שמונה־עשר קילומטרים מהבית. בכל יום לימודים הוא רוכב על סוס דרך ההרים. אחותו הקטנה מיקאלה נוסעת איתו. לסוס שלהם קוראים צ׳יבריטו. מזג האוויר עלול להקשות על הדרך. קרליטו רוצה להיות וטרינר.',
 source='https://medias.unifrance.org/medias/199/173/110023/presse/on-the-way-to-school-presskit-english.pdf',
 questions=[['Who travels with Carlito?','His sister Micaela.'],['How far is his school?','Eighteen kilometres.'],['Which detail connects his journey with his dream?','He rides a horse and wants to become a vet.']],
 targets=[],note='תיאור שגרת התיעוד, ללא דיאלוג או רגשות שהומצאו. הגילים מתייחסים למועד התיעוד; אין לטעון שהוא תלמיד כיום.'),
 dict(title='Four Kilometres Together',place='India',period='On the Way to School, documentary, 2013',mode='wheelchair',
 en='Samuel lives in India. He uses a wheelchair to get to school. His two younger brothers help him along the way. They push and pull the chair for four kilometres. The route includes sand, rivers and palm trees. A wheelchair journey is part of their school routine. Samuel and his brothers make this long journey together.',
 he='סמואל גר בהודו. הוא משתמש בכיסא גלגלים כדי להגיע לבית הספר. שני אחיו הצעירים עוזרים לו בדרך. הם דוחפים ומושכים את הכיסא לאורך ארבעה קילומטרים. המסלול כולל חול, נהרות ועצי דקל. נסיעה בכיסא גלגלים היא חלק משגרת בית הספר שלהם. סמואל ואחיו עושים את הדרך הארוכה הזאת יחד.',
 source='https://www.fondation-beatrice-schonberg.org/sur-le-chemin-de-l-ecole/',
 questions=[['Who helps Samuel?','His two younger brothers.'],['Name one feature of the route.','Sand, rivers or palm trees.'],['Why is this journey a shared task?','His brothers help push and pull the chair.']],
 targets=['push','along'],note='תיאור שגרת התיעוד. אין להוסיף פציעה, חילוץ או דיאלוג שלא תועדו. אין להסיק שזה מסלול אופייני לכל ילדי הודו.'),
 dict(title='The School Boat',place='Bryher and Tresco, England',period='BBC Teach, source copyright 2024',mode='boat',
 en='Zoe and Isaac live on Bryher, a small island. Their school is on nearby Tresco. Every morning, they meet the other children at the place where the boat stops. The boat journey takes only five minutes. Sometimes they see dolphins. After the boat arrives, they walk to school. For these children, going to class means crossing the sea.',
 he='זואי ואייזק גרים בברייר, אי קטן. בית הספר שלהם נמצא בטרסקו הסמוך. בכל בוקר הם פוגשים את הילדים האחרים במקום שבו הסירה עוצרת. השיט נמשך רק חמש דקות. לפעמים הם רואים דולפינים. לאחר שהסירה מגיעה הם הולכים לבית הספר. עבור הילדים האלה, ההגעה לכיתה כוללת חציית ים.',
 source='https://teach.files.bbci.co.uk/teach/geography/ks1_uk_locations/life_on_the_isles_of_scilly.pdf',
 questions=[['Why do they need a boat?','Their school is on another island.'],['How long is the boat journey?','Five minutes.'],['Do they always see dolphins?','No. Sometimes.']],
 targets=['nearby'],note='מקור BBC משלב מנחה בדיוני בדמות עכבר. העיבוד משתמש רק בפרטי השגרה של הילדים ובמקומות הממשיים, ומשמיט את עלילת המנחה.'),
 dict(title='A Bus Without a Bus',place='Barcelona, Spain',period='NPR report, 22 October 2021',mode='bicycle',
 en='On Fridays, some children in Barcelona ride to school together. Parents go with them. This group is called a bike bus. It has stops where more families join. The full ride takes approximately twenty-five minutes. Police help protect the group on the busy road. One mother rides with her five-year-old son. The regular Friday journey gives them company on the way to school.',
 he='בימי שישי חלק מהילדים בברצלונה רוכבים יחד לבית הספר. ההורים מצטרפים. לקבוצה קוראים אוטובוס אופניים. יש לה תחנות שבהן מצטרפות משפחות נוספות. המסלול המלא נמשך בערך עשרים וחמש דקות. המשטרה עוזרת להגן על הקבוצה בכביש העמוס. אֵם אחת רוכבת עם בנה בן החמש. הדרך הקבועה ביום שישי מספקת להם חברה בדרך לבית הספר.',
 source='https://www.gpb.org/news/2021/10/22/hundreds-of-kids-and-their-families-are-riding-bicycle-bus-school-in-barcelona',
 questions=[['When does the group ride?','On Fridays.'],['Why does it have stops?','More families join there.'],['How does the group make the journey different?','Children travel with other families and police help protect them.']],
 targets=['approximately','protect'],note='שגרת יום שישי שתועדה ב־2021, לא טענה שכל הילדים רוכבים כך בכל יום. שמו של הילד לא פורסם ואין להמציאו.'),
]
photos={
 'A Snow Day, a Screen and a Shovel':dict(file='assets/snow-report.jpg',alt='A snow-covered school-area sign in the KTUU report',caption='A school-area sign in the snow. Kali is not pictured. Source: KTUU / Alaska’s News Source, November 2023.',credit='KTUU / Alaska’s News Source'),
 'A Bus Without a Bus':dict(file='assets/barcelona-bike-bus.jpg',alt='Children cycle together to school in Barcelona',caption='The school bike bus in Eixample, Barcelona, 2021. Photo: Bicibús Eixample, via NPR / GPB. Individual riders are not identified by the source.',credit='Bicibús Eixample, via NPR / Georgia Public Broadcasting')
}
for story in stories:
    if story['title'] in photos:
        story['photo']=photos[story['title']]
save(OUT/'content.json',dict(title='School Years Around the World',status='teacher_review_draft',groups=[3,4,5],main=main_sections,calendar=calendar,stories=stories))

# Reuse Unit 1's tested navigation and feedback implementation.
base_js=(TEMPLATES/'grammar/lesson.js').read_text()
base_js=base_js.replace("slideKey='teachers-unit1-reading-v1'","slideKey='teachers-unit2-'+LESSON.id+'-v1'")
base_js=base_js.replace("'Unit 1 · קוראים וכותבים'","'Unit 2 · '+LESSON.subtitle")
base_js=base_js.replace("'כיתה ז׳ · Unit 1'","'כיתה ז׳ · Unit 2'")
start=base_js.index("if(s.kind==='cover')")
end=base_js.index("else if(s.kind==='plan')",start)
base_js=base_js[:start]+'''if(s.kind==='cover')c=title+'<h1>'+esc(s.title)+'</h1><p class="sub">'+esc(s.sub)+'</p><p class="created">טיוטה לעיון המורה · Core I · קבוצות 03–05</p><div class="actions"><button id="start">מתחילים</button><a href="../index.html">כל היחידה</a></div>';
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
        text=text.replace('110','165').replace('Groups 01–02','Groups 03–05').replace('שתי קבוצות','שלוש קבוצות').replace('שתי הקבוצות','שלוש הקבוצות')
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
    return '<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><link rel="stylesheet" href="unit.css"><style>.text-block{padding-block:18px;border-bottom:1px solid #365c73}.english{font-size:22px;line-height:1.7}summary{cursor:pointer;color:#dfff75}.answerline{height:35px;border-bottom:1px solid #889cab}.draft{color:#ffdc9b}table{width:100%;border-collapse:collapse}td,th{padding:12px;border-bottom:1px solid #537085;text-align:start}.scroll{overflow:auto}@media print{body{background:white;color:black}a{color:black}header,.no-print,details{display:none}main{padding:0;max-width:none}.text-block{break-inside:avoid}.english{font-size:13pt}h1{font-size:24pt;color:black}h2{font-size:18pt}p{font-size:12pt}.answerline{height:26px}@page{size:A4;margin:16mm}}</style></head><body><main><header><a class="home" href="./">⌂</a><p class="draft">Unit 2 · Teacher review edition</p></header><h1>'+esc(title)+'</h1>'+body+'</main></body></html>'

body='<p class="english">When does school begin? When does it end? How long is the summer break?</p><p><a href="reading/?text=school-calendars">Read & Listen →</a></p>'
for title,en,he in main_sections:
    body+='<section class="text-block"><h2 dir="ltr">'+esc(title)+'</h2><p class="english">'+esc(en)+'</p><details><summary>Hebrew support</summary><p lang="he" dir="rtl">'+esc(he)+'</p></details></section>'
body+='<h2 dir="ltr">Calendar details & sources</h2><p class="english">Holiday lengths include weekends. Florida uses a summer 2026 example; the other dated summer examples refer to 2027. Local school calendars and teacher-training days can vary.</p>'
for row in calendar:
    body+='<section class="text-block"><h2 dir="ltr">'+esc(row['place'])+'</h2><p class="english">Start: '+esc(row['start'])+'<br>End: '+esc(row['end'])+'<br>Summer: '+esc(row['summer'])+'</p><details><summary>Teacher note</summary><p lang="he" dir="rtl">'+esc(row['scope']+' · '+row['detail'])+'</p></details>'+''.join('<p class="meta" dir="ltr"><a href="'+esc(u)+'">Source: '+esc(u.split('/')[2])+'</a></p>' for u in row['sources'])+'</section>'
(OUT/'main-text.html').write_text(page('School Years Around the World',body))
body='<p class="english">Real children. Different journeys. Sometimes, a very different school day.</p><p class="meta english">Adapted from published reports and documentary sources. Events and routines refer to the dates shown.</p>'
for s in stories:
    photo=s.get('photo')
    figure=('<figure style="margin:20px 0"><a href="'+esc(s['source'])+'"><img src="'+esc(photo['file'])+'" alt="'+esc(photo['alt'])+'" loading="lazy" style="display:block;width:100%;max-width:720px;height:auto;border-radius:12px" '+('width="1200" height="600"' if 'snow-report' in photo['file'] else 'width="958" height="719"')+'></a><figcaption class="meta" dir="ltr">'+esc(photo['caption'])+'</figcaption></figure>') if photo else ''
    body+='<section class="text-block"><h2 dir="ltr">'+esc(s['title'])+'</h2><p class="meta" dir="ltr">'+esc(s['place']+' · '+s['period'])+'</p><p class="english">'+esc(s['en'])+'</p>'+figure+'<details><summary>Hebrew support & teacher notes</summary><p lang="he" dir="rtl">'+esc(s['he'])+'</p><p lang="he" dir="rtl">'+esc(s['note'])+'</p></details><ol>'+''.join('<li><p class="english">'+esc(q)+'</p><details><summary>Answer</summary><p class="english">'+esc(a)+'</p></details></li>' for q,a in s['questions'])+'</ol><p dir="ltr"><a href="'+esc(s['source'])+'">Read the original source</a></p></section>'
(OUT/'companion-stories.html').write_text(page('Real Journeys to School',body))

worksheet='<p class="no-print"><button onclick="window.print()">הדפסה</button></p><p>שם פרטי: __________ כיתה: ________</p>'
worksheet+='<h2>Part A · לפני ההסבר</h2><p class="english">1. I ___ a bag. (carry / carries / carrying)<br>2. David ___ to school every day. (walk / walks / walking)</p>'
worksheet+='<h2>Part A · כתיבה עצמאית</h2><p>כתבו הרגל שלכם, הרגל של חבר ומשפט שלילה אחד. השתמשו בשתי מילים מהיחידה.</p>'+('<div class="answerline"></div>'*4)
worksheet+='<h2>Part B · שאלות ושיחה</h2><p>כתבו שאלה על דרך ההגעה ושאלה על פעילות אחרי בית הספר. שאלו חבר ורשמו תשובות. לבסוף כתבו משפט אחד עליו.</p>'+('<div class="answerline"></div>'*6)
worksheet+='<h2>Reading · שני סיפורים</h2><p>בחרו שני סיפורים. רשמו לכל אחד: מי הילד, כיצד הוא מגיע לבית הספר או מדוע אינו יכול להגיע, ופרט שמשפיע על יום הלימודים. כתבו באנגלית דמיון אחד והבדל אחד. ציינו פרט מכל מקור שתומך בתשובה.</p>'+('<div class="answerline"></div>'*6)
worksheet+='<h2>My School Routine · 50–70 words</h2><p>תארו את הדרך שלכם לבית הספר ואת השגרה. כללו משפט שלילה, מילת תדירות ושתי מילים מקבוצות 3–5. חברו רעיונות באמצעות and, but או because.</p>'+('<div class="answerline"></div>'*9)
(OUT/'worksheet.html').write_text(page('Unit 2 · דף עבודה',worksheet))

teacher=[
 ('המוקד שאושר','<p>הטקסט המרכזי משווה תחילת וסיום שנות לימודים, חופשות ועונות. הסיפורים הקצרים עוסקים בשגרת ילדים אמיתיים: דרכי הגעה שונות, וגם אירוע מתועד כמו שלג שמשנה את יום הלימודים.</p>'),
 ('מבנה כמו יחידה 1','<p>אוצר מילים במנות; קריאה להבנה; דקדוק בשני מפגשים; קריאה עצמאית; דיבור וכתיבה; איסוף לפני פתרונות.</p>'),
 ('Core I בלבד','<p>קבוצות 03–05: 165 רשומות. מצגת מלאה אינה עדות לשליטה. בוחרים בכל מפגש מספר מילים לשימוש פעיל וחוזרים עליהן במשימות.</p>'),
 ('פריסת עבודה מוצעת','<p>תשעה מפגשים כפולים ורזרבה, לפי הביצוע בפועל. עד 72 דקות פעילות מתוכננת בכל מפגש. זו הצעת הוראה מקומית.</p>'),
 ('מפגשים 1–3','<p>1: פתיחה ולוחות לימודים. 2: חופשות ועונות וחיבור מידע. 3: דקדוק Part A. בכל מפגש מנת מילים וחזרה.</p>'),
 ('מפגשים 4–6','<p>4: Part B לפי טעויות Part A. 5: שני סיפורי שגרה והשוואה. 6: שני סיפורים נוספים ומשימת מידע חסר בזוגות.</p>'),
 ('מפגשים 7–9','<p>7: האזנה עצמאית לפני פתיחת התמליל. 8: My School Routine ומשוב. 9: העברה לטקסט חדש וכתיבה ללא הדגם.</p>'),
 ('אבחון לפני הקניה','<p>התלמיד עונה תחילה על שתי שאלות פתיחה. בהמשך כותב במשימות. מפרידים בין הבנת המסר, מבנה ואיות.</p>'),
 ('Part A · 72 דקות','<p>5 פתיחה; 14 שגרה; 13 גוף שלישי; 14 שלילה; 15 כתיבה; 5 איסוף; 6 משוב. אין לדחוס את Part B לאותו מפגש.</p>'),
 ('Part B · 72 דקות','<p>7 חזרה מאבחנת; 12 שאלות; 13 תשובות קצרות; 15 מילות שאלה; 10 תדירות; 8 שיחה; 7 משימת יציאה.</p>'),
 ('החלטה לפי טעות','<p>doesn’t walks: תרגול צורת בסיס. שגיאות רק ב־ies: תרגול כתיב קצר. בחירה נכונה בלי יכולת לכתוב: עוד הפקה עם תמיכה שנעלמת בהדרגה.</p>'),
 ('דיוק בלוחות','<p>לוחות בתי ספר אינם אחידים למדינה שלמה. קנט וג׳רזי כוללים ימי הכשרת צוות. אורך קיץ פלורידה מתייחס ל־2026. ביפן הקיץ באמצע השנה.</p>'),
 ('סיפורים אמיתיים','<p>אין להוסיף דיאלוג, פחד, תקלה או חילוץ ללא מקור. ההווה הלימודי מתאר שגרה מתועדת. מקור ותאריך מצורפים לכל סיפור.</p>'),
 ('חיבור בין מקורות','<p>התלמיד מוצא דרך הגעה או סיבה להישאר בבית ופרט משפיע בכל טקסט, ואז כותב משפט דמיון ומשפט הבדל. דורשים ראיה מכל אחד משני הטקסטים. מה ידוע על השגרה, ומה השתנה באותו יום?</p>'),
 ('הסרת התמיכה','<p>תחילה מילון ומשפט פתיחה; בהמשך רק שאלות מנחות; במשימת הסיום טקסט חדש וכתיבה ללא דגם גלוי.</p>'),
 ('כתיבה ומשוב','<p>50–70 מילים. קודם תוכן ברור ורצף, אחר כך Present Simple ושלילה, ואז איות. התלמיד מתקן שני משפטים בעקבות המשוב.</p>'),
 ('מפת כיסוי','<p>165 רשומות מוצגות עם דוגמה ומשימת שליפה בהקשר. מפת הכיסוי מפרידה בין הצגה, בחירה וכתיבה עצמאית. אין לספור subject כערך בית ספר או name כשם עצם. misses בסיפור קאלי אינו ערך miss במשמעות להחמיץ.</p>'),
 ('בדיקת מקור אוצר המילים','<p>נשמר צילום המקור של כל הרשומות. 25 רשומות תוקנו גם בספר התיעוד המקורי; משימת סנכרון בתוכנה: E-Vocab #5. תיקוני העריכה מתועדים: חלק דיבור, משמעות או תרגום. דוגמאות: which, included, excited, the young ו־leave במשמעות סיום קשר.</p>'),
 ('פתרונות חוברת העבודה','<p><a href="workbook-key.html">Workbook answer key</a></p><p>אוספים תשובות עצמאיות לפני חשיפת הפתרונות. כל ההפניות למקורות באנגלית.</p>'),
 ('קריאה והאזנה','<p>שישה טקסטים, קטעים קצרים וקריאה משפט־משפט. בכל מילה אפשר לקבל פירוש. ברירת המחדל היא 0.75; בחירת המהירות נשמרת. במשימת ההאזנה מסתירים תחילה את התמליל.</p>'),
]
(OUT/'teacher-data.js').write_text('const TEACHER = '+json.dumps([dict(title=t,body=b) for t,b in teacher],ensure_ascii=False)+';\n')
for name in ['teacher.html','teacher.js','unit.css','hub.js']:
    text=(TEMPLATES/'unit'/name).read_text().replace('Unit 1','Unit 2').replace('unit1-1','unit2-draft1')
    (OUT/name).write_text(text)

cards=[('Read & Listen','Six texts · short parts · sentence practice','reading/'),('Vocabulary','165 entries · Groups 03–05 · recorded audio','vocabulary/full.html'),('Words in Context','Short practice sets · choose, check and write','vocabulary/practice.html'),('Present Simple A','Routines, third person and negatives','grammar-a/'),('Present Simple B','Questions, frequency and conversations','grammar-b/'),('School Calendars','School years, holidays and seasons','main-text.html'),('Real Journeys','Different journeys — and a day changed by snow','companion-stories.html'),('Listen First','Listen, take notes and check the evidence','listening.html'),('Worksheets','Reading, grammar and independent writing','files/unit2-workbook.pdf'),('Teacher Guide','Teaching sequence, timing and answer keys','teacher.html')]
body='<p class="english">Grade 7 · Band II, Core I · Groups 03–05</p><p class="draft english">Teacher review edition</p><div class="grid">'+''.join('<section class="card" dir="ltr"><h2>'+t+'</h2><p>'+d+'</p><a class="btn" href="'+u+'">Open →</a></section>' for t,d,u in cards)+'</div>'
body+='<h2 style="margin-top:30px">Vocabulary practice</h2><p>Use the corrected examples in <a href="vocabulary/practice.html">Words in Context</a>.</p>'

(OUT/'index.html').write_text(page('Unit 2 · School Years Around the World',body))
pending=[]
for label,relative in [('recorded vocabulary audio','vocabulary/audio/g05-55.mp3'),('recorded reading audio','reading/assets/school-calendars.mp3'),('Read & Listen','reading/index.html'),('contextual practice','vocabulary/practice.html'),('listening task','listening.html'),('worksheet PDF','files/unit2-workbook.pdf')]:
    if not (OUT/relative).is_file():pending.append(label)
pending += ['teacher review of complete draft','student publication']
save(OUT/'build-report.json',dict(status='teacher_review_draft',records=len(records),groups=[3,4,5],grammar_a_slides=len(A),grammar_b_slides=len(B),teacher_slides=len(teacher),true_companion_texts=len(stories),main_words=sum(len(re.findall(r"\b[\w’'-]+\b",x[1])) for x in main_sections),vocabulary_corrected_records=len(corrections),vocabulary_book='corrected: version 4',software_sync_task='https://github.com/Simonh68/E-Vocab-Band-II/issues/5',pending=pending))
print(json.dumps(json.loads((OUT/'build-report.json').read_text()),ensure_ascii=False))
