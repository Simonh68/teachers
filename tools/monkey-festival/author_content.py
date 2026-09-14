import json
from pathlib import Path

ROOT=Path(__file__).parent
OUT=ROOT.parents[1]/'grade8/monkey-festival'
OUT.mkdir(parents=True,exist_ok=True)
SOURCE='https://drive.google.com/file/d/1GJz_c1qY3qMb3NidioFReT7V1l2WebFr/view'
READING_SOURCE='https://drive.google.com/file/d/1v5hxzvq6L3lwQonsgvWBEOi9tFcik7v0/view'
CAL='https://drive.google.com/file/d/1MkEy1qZROpufD3z4PVTW5YuP3VSotr6M/view'
OPENING='https://simonh68.github.io/teachers/grade8/opening/'
GROUP='https://englishfornoar.co.il/band-ii/groups/group-01.html'
paragraphs=[
('Part One · A','I am at one of the most unusual festivals in the world – the Monkey Festival in Lopburi, Thailand. People are getting ready for the festival, so I finally have some time to write about my adventures.'),
('Part One · B','Everybody in town gets together and the entire town goes a little crazy on this day! Many people are dressed like monkeys, and the festival has live performances and dances.'),
('Part One · C','The first thing you notice when you look around town are the monkeys. They are everywhere! I can see a few of them right now. They are gathered together on the street corner, playing with each other and making loud noises.'),
('Part One · D','They may look cute, but you have to be careful. These monkeys can cause major trouble. They like to take things from people, especially food and drinks, and even valuable things, like handbags and sunglasses.'),
('Part One · E','This is an annual festival, and people look forward to it all year. Early in the morning, people prepare huge plates of fruit and put them on long tables. The tables look beautiful, but they aren’t going to stay that way.'),
('Part One · F','The best part of the festival is when thousands of excited monkeys jump on the tables and eat as much fruit as they possibly can. I heard that sometimes the monkeys even have food fights! I hope they have one today. What a crazy festival!'),
('Part Two · G','I also noticed the way the people of Lopburi treat the monkeys. They are kind to them and make sure that they are not hungry. In the beginning, I found this attitude a bit strange. Why would these people care so much about the monkeys? After all, they are quite scary and they often steal things.'),
('Part Two · H','I asked my friend Aroon, who owns a small business in the center of town. He explained that the people of Lopburi admire the monkeys because of a famous story that happened many centuries ago. It is about Prince Rama and it tells how monkeys helped him save his wife from a horrible monster.'),
('Part Two · I','They take care of the monkeys and once a year, every November, they honor them by having a monkey festival. They believe that these monkeys will bring them good luck, like they did for Prince Rama.')
]
slides=[]
def add(kind,title='',body='',**kw):
    slides.append(dict(n=len(slides)+1,kind=kind,title=title,body=body,section=kw.pop('section','start'),**kw))
def pair(title,answer,*,hint='',label='שאלת הבנה',section='reading',notes='',tense='',source=SOURCE):
    pid='pair-'+str(len(slides)+1)
    add('qa',title,pair=pid,hint=hint,label=label,section=section,tense=tense,notes=notes,source=source)
    add('qa',title,pair=pid,answer=answer,hint=hint,label=label,section=section,tense=tense,notes=notes,source=source)
def vocab(word,example,meaning,translation,*,group=False,tense=''):
    pid='word-'+str(len(slides)+1)
    label='Band II · Core I · Group 01' if group else 'מילים מתוך טקסט הקריאה'
    src=OPENING if group else SOURCE
    note='להמתין כ־10 שניות לניחוש. לקרוא את הדוגמה ואז לחשוף משמעות. '+('משפט ותרגום נשמרו מהמצגת הקיימת. ' if group else 'הדוגמה נכתבה לצורך התרגול ואינה ציטוט מהטקסט. ')
    for reveal in (False,True):
        add('vocab',word,example,pair=pid,meaning=meaning if reveal else '',translation=translation if reveal else '',label=label,section='words',tense=tense,notes=note,source=src)
def read(i):
    title,body=paragraphs[i]
    add('reading',title,body,section='reading',source=READING_SOURCE,notes='קריאה קצרה עם המורה. אין צורך לתרגם כל מילה. לבקש לאתר את המידע הנדרש. אותיות הפסקאות נוספו לצורך התרגול. הטקסט המקורי נשמר, ופסקה אחת חולקה ל־E ול־F.')
def funny(key,note):
    add('break',asset=key,section='words' if len(slides)<30 else 'reading',notes=note+' הפסקה חזותית של 15–20 שניות. איור הומוריסטי דמיוני, לא תיעוד מהפסטיבל.')

add('cover','ברוכים הבאים','כיתה ח׳2 · אנגלית',notes='11:10. פתיחה קצרה. היום מתכוננים למבחן בעזרת טקסט מבחן מהארכיון.')
add('notice','המבחן הראשון באנגלית','יום חמישי, כ״ז בתשרי תשפ״ז',sub='(8.10.2026)',hint='לפי הלוח שפורסם. המועד עשוי להשתנות.',source=CAL,notes='לומר: המבחן ביום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026). היום מתחילים להתכונן. להבהיר שזהו המועד שפורסם.')
add('schedule','נשארו 3 מפגשים כפולים',items=['יום שני, ג׳ בתשרי תשפ״ז (14.9.2026)\nהיום בזום','יום חמישי, ו׳ בתשרי תשפ״ז (17.9.2026)\nטעון בדיקה בגלל מופע סליחות','יום שני, כ״ד בתשרי תשפ״ז (5.10.2026)\nהמפגש האחרון לפני המבחן'],hint='כולל היום. אם המפגש השני יתבטל, יישארו שני מפגשים כולל היום.',source=CAL,notes='ליום השיעור: שלושה מפגשים מתוכננים כולל היום, שניים אחריו. חופשת החגים מיום ראשון, ט׳ בתשרי תשפ״ז (20.9.2026), עד שבת, כ״ב בתשרי תשפ״ז (3.10.2026). המבחן עצמו אינו נספר כמפגש הכנה. המפגש השני אינו מאושר סופית.')
add('notice','מה מתרגלים היום?','אוצר מילים והבנת הנקרא',items=['קבוצה 01: פירוש, איות ושימוש במשפט','טקסט הקריאה: פרטים, הסבר ותשובה מבוססת'],hint='הטקסט מהארכיון מיועד לתרגול. פירוט החומר למבחן יימסר בנפרד.',source=OPENING,notes='זהו מוקד ההכנה לשיעור. לא נמצא מפרט מלא לבחינה הקרובה, ולכן אין להכריז שהטקסט הזה יופיע שוב בבחינה או שקבוצה 01 היא כל החומר. למורה: יש לפרסם היקף סופי בנפרד.')
add('schedule','השיעור היום',items=['11:10–11:50 · זום ותרגול יחד','12:00–12:25 · עבודה עצמאית','12:25 · סיכום קצר בזום','עד 12:40 · תיקון והגשה'],notes='פורמט מומלץ שסוכם עם המורה. את השקפים הקצרים מחליפים במהירות לפי תגובות הכיתה. אם מתעכבים, מדלגים לחזרה המקוצרת בשקף 57 וחוזרים לתרגול בבית.')
add('question','The Monkey Festival','Who do you think the food is for?',hint='ניחוש קצר בצ׳אט. נבדוק לפי הטקסט.',notes='לשמוע שני ניחושים. זו שאלת חיזוי, לכן התשובה תתברר בקריאה ולא בשקף תשובה מיידי.',source=SOURCE)
funny('banana_guest','מבט קצר על אורח רציני מאוד בשולחן הפירות.')
for row in [
('unusual','This is an unusual festival.','לא רגיל; יוצא דופן','זהו פסטיבל יוצא דופן.'),
('festival','People come to the festival.','פסטיבל; חגיגה','אנשים באים לפסטיבל.'),
('prepare','People prepare plates of fruit.','להכין','אנשים מכינים צלחות של פירות.'),
('valuable','Sunglasses can be valuable.','בעל ערך; יקר ערך','משקפי שמש יכולים להיות בעלי ערך.'),
('annual','The annual festival happens once a year.','שנתי; שמתקיים פעם בשנה','הפסטיבל השנתי מתקיים פעם בשנה.'),
('careful','You have to be careful.','זהיר','צריך להיות זהירים.'),
('take care of','People take care of the monkeys.','לטפל ב־; לדאוג ל־','אנשים דואגים לקופים.'),
('honor','People honor the monkeys with a festival.','לכבד; לחלוק כבוד','אנשים חולקים כבוד לקופים באמצעות פסטיבל.')]:
    vocab(*row,tense='הווה')
funny('banana_safe','בננה אחת זוכה לאבטחה של אוצר יקר. אפשר להצביע על valuable בלי להפוך את התמונה למשימה נוספת.')
vocab('however','It was hard. However, I tried.','עם זאת','זה היה קשה. עם זאת, ניסיתי.',group=True,tense='עבר')
vocab('around','Is anyone around?','בסביבה; מסביב','יש מישהו בסביבה?',group=True,tense='הווה')
vocab('care','The baby needs care.','טיפול; תשומת לב','התינוק צריך טיפול.',group=True,tense='הווה')
add('notice','איך בונים תשובה?','Question → paragraph → answer',items=['מזהים מה שואלים: מי, היכן, מה או למה','מוצאים פרט מתאים בטקסט','כותבים תשובה ובודקים שהיא עונה לשאלה'],section='reading',notes='להדגים בקצרה: Where מצפה למקום. Why מצפה לסיבה. לא צריך להבין כל מילה כדי לענות על פרט מפורש.')
read(0)
pair('Where is the festival?','The festival is in Lopburi, Thailand.',hint='Part One · A',notes='שאלה 1 במבחן הישן. ההפניה עודכנה לאות הפסקה, כי מספרי השורות בצילום אינם מתאימים לכל השאלות.')
read(1)
read(2)
read(3)
pair('Name two valuable things the monkeys take.','They take handbags and sunglasses.',hint='Part One · D',notes='תרגול נוסף, אינו אחת מחמש שאלות המבחן המקורי. לבקש את שני הפריטים ולא רק food.')
funny('monkey_detective','בלש מחפש רמז בתוך קליפת בננה. הפסקה קצרה לפני המשך הקריאה.')
read(4)
read(5)
pair('Who eats the food at the festival?','The monkeys eat the food.',hint='Part One · F',notes='שאלה 2 במבחן הישן בניסוח אנגלי טבעי. במקור הופיעו שורות 6–8, אך התשובה נמצאת בפסקה האחרונה בחלק הראשון. בתרגול משתמשים בהפניה F.')
pair('What do people prepare in the morning?','They prepare huge plates of fruit and put them on long tables.',hint='Part One · E',notes='שאלה 3 במבחן הישן. לשאול מה מכינים, ולא לדרוש פירוט שלא נמצא בטקסט.')
read(6)
pair('Why does the writer find the people’s attitude strange?','They are kind to the monkeys, although the monkeys are scary and often steal things.',hint='Part Two · G',notes='שאלה 4 במבחן הישן בניסוח מפורש יותר. אפשר לקבל שני משפטים קצרים: The monkeys steal things. However, the people are kind to them. זו חזרה על however מהקבוצה.')
funny('banana_calendar','התלמיד שהכין יותר מדי ציוד. הפסקה לפני ההסבר שבחלק השני.')
read(7)
read(8)
pair('How do the people honor the monkeys?','They have a monkey festival every November.',hint='Part Two · I',notes='שאלה 5 במבחן הישן. התשובה היא הפעולה שעושים כדי לכבד. ההסבר התרבותי מתאר את אמונת התושבים לפי הטקסט.')
pair('Why does the writer include the story about Prince Rama?','It helps explain why the people admire the monkeys and hold the festival.',hint='Part Two · H–I',label='שאלת חשיבה על הטקסט',notes='שאלת הרחבה. להסביר שזהו סיפור שמסביר מנהג בטקסט, ולא עובדה היסטורית שאנו מאמתים. אפשר לענות בעברית תחילה ואחר כך לבנות משפט אנגלי.')
add('notice','בדיקה לפני עבודה עצמאית','Where? Who? What? Why? How?',items=['אני יודע היכן למצוא את המידע','אני מבדיל בין תשובה קצרה להסבר עם סיבה','אני בודק אות גדולה, פועל וסימן פיסוק'],section='work',notes='עד 11:47. לשאול מי זקוק לעזרה באיתור פסקאות. אפשר לדלג לכאן מכל שלב אם נגמר זמן הזום הראשון.')
funny('monkey_zoom','משתתף נוסף בזום: בננה עם אוזניות. הפסקה קצרה לפני היציאה לעבודה.')
add('notice','הפסקה עד 12:00','חוזרים לזום ב־12:25',hint='העבודה העצמאית נמצאת בדף התרגול. ההגשה עד 12:40.',section='work',notes='11:50. לסיים את המפגש הראשון. לשלוח בצ׳אט קישור לדף העבודה ולוודא שנפתח. אין צורך להישאר בזום בזמן העבודה העצמאית.')
add('schedule','העבודה העצמאית',items=['A · חמש שאלות קריאה. ציינו אות פסקה בכל תשובה','B · שלושה משפטים לתרגום לאנגלית','C · שתי השלמות מקבוצה 01'],hint='הטקסט פתוח. כתבו תשובות משלכם, בלי להעתיק משקפי הפתרונות.',section='work',notes='12:00–12:25. דף העבודה כולל שאלות חדשות על אותו טקסט, כדי לבדוק הבנה ולא רק זיכרון של הפתרונות. לתלמידים מתקשים: להתחיל ב־A1–A3 ו־B1, ואז להמשיך. למתקדמים: שאלת ההרחבה D.',links=[{'label':'דף תרגול · PDF','href':'files/monkey-festival-practice.pdf'}])
add('notice','מה מגישים?','תשובות מסומנות A, B, C',items=['שם פרטי וכיתה בראש העבודה','תשובות קריאה עם אות הפסקה','צילום ברור או קובץ בערוץ הכיתתי הרגיל'],hint='סמנו בכוכבית שאלה שתרצו לבדוק בזום.',section='work',notes='שקף זה נשאר מוצג אם המורה משאיר שיתוף מסך. אין לאסוף פרטים אישיים נוספים. לא הוגדר בשיחה כלי הגשה מסוים.')
add('notice','12:25 · סיכום בזום','איזו שאלה הייתה קשה?',hint='שלחו בצ׳אט את מספר השאלה בלבד.',section='wrap',notes='סיכום מומלץ של כחמש עד שבע דקות. לבחור קושי אחד או שניים מהצ׳אט. השקפים הבאים קצרים. אם אין זמן, להשתמש רק בזוג הרלוונטי.')
pair('I can _____ at the festival.','I can be at the festival.',hint='be / am / is',label='בדיקת משפט',section='wrap',source='',notes='אחרי can משתמשים בצורת הבסיס be. לא I can am. זו הכנה למשפטי התרגום מהמבחן הישן. אפשר לקבל join רק אם השאלה אינה רב־ברירה, אך כאן האפשרויות קבועות.')
pair('Translate: אני בפסטיבל.','I am at the festival.',label='תרגום לאנגלית',section='wrap',tense='הווה',source=SOURCE,notes='משפט 6 במבחן הישן. להדגיש שנחוץ am גם אם בעברית אין פועל מפורש.')
pair('Why do the people admire the monkeys?','They admire them because, in the story, monkeys helped Prince Rama.',hint='Begin with: They admire them because…',label='תשובה עם סיבה',section='wrap',source=SOURCE,notes='לקבל גם תשובה על האמונה שהקופים מביאים מזל טוב. לבדוק שמוצגת סיבה ושלא הופכים אמונה או אגדה לטענה היסטורית. מתאים לשאלת A5 בעבודה העצמאית.')
add('schedule','תרגול עד המפגש הבא',items=['קבוצה 01: פירוש, איות ומשפט','קריאה חוזרת של The Monkey Festival','תיקון תשובה אחת שלא הייתה מדויקת'],hint='תרגלו 10 דקות בכל יום. אל תחכו לסוף חופשת החגים.',section='wrap',source=OPENING,links=[{'label':'תרגול קבוצה 01','href':GROUP}],notes='זהו תרגול שנקבע במערך הזה. אין להציג את שלוש המילים שהופיעו במצגת כמכלול 55 מילות הקבוצה. המועד שפורסם לבחינה הוא יום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026).')
add('notice','הגשה עד 12:40','One thing I can do better now is…',hint='תקנו בעקבות הסיכום, הוסיפו משפט יציאה והגישו.',section='wrap',notes='לאחר סיכום הזום, התלמידים מסיימים תיקון והגשה עד 12:40. משפט היציאה יכול להיות באנגלית פשוטה או בעברית לפי יכולת. אין להוסיף שיעורי זום מעבר לשעות שנקבעו.')
assert len(slides)==70,len(slides)

data={'title':'The Monkey Festival','date':'2026-09-14','exam_date':'2026-10-08','slides':slides,'paragraphs':[{'label':k,'text':v} for k,v in paragraphs],'display_dates':{'lesson':'יום שני, ג׳ בתשרי תשפ״ז (14.9.2026)','second_lesson':'יום חמישי, ו׳ בתשרי תשפ״ז (17.9.2026)','last_lesson':'יום שני, כ״ד בתשרי תשפ״ז (5.10.2026)','exam':'יום חמישי, כ״ז בתשרי תשפ״ז (8.10.2026)'},'sources':{'reading':READING_SOURCE,'exam_questions':SOURCE,'calendar':CAL,'opening':OPENING,'vocabulary':GROUP},'archive_note':'The source exam is filed under התשפו / ח / מבחן אקטובר. The original file modification date is 21 October 2024. The folder placement identifies the archive context, not independent proof that this exact copy was administered in 2025.','editorial_note':'Original passage wording preserved. The website navigation sentence was omitted. Original footnote markers with missing footnotes were removed. Paragraph letters A–I were added and the last paragraph of Part One was split into E and F. Teaching questions use paragraph references because some original line references are inaccurate.'}
(OUT/'lesson.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('Slides:',len(slides),'Reading words:',sum(len(t.split()) for _,t in paragraphs))
