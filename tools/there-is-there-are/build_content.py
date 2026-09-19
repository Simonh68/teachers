"""Canonical lesson content. Run from any directory; does not rebuild audio."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2]/'grade7/there-is-there-are'
vocabulary=json.loads((R.parent/'band2-groups-01-02/entries.json').read_text());vmap={e['id']:e for e in vocabulary}
slides=[];sentences=[];section='שייכות ומקום'
def add(kind,title,**kw):slides.append(dict(kind=kind,title=title,section=section,**kw))
def rule(title,formula,he,tense='הווה',rows=None):add('rule',title,formula=formula,he=he,tense=tense,rows=rows)
def ex(en,he,title='קוראים ומבינים',tense='הווה'):
 n=len(sentences);sentences.append(dict(en=en,he=he))
 for reveal in (False,True):add('sentence',title,n=n,en=en,he=he,tense=tense,reveal=reveal)
def quiz(title,q,opts,correct,why,tense='הווה',context=''):
 for reveal in (False,True):add('quiz',title,q=q,opts=opts,correct=correct,why=why,tense=tense,context=context,reveal=reveal)
def task(title,prompt,model,check,tense=''):
 add('task',title,prompt=prompt,tense=tense)
 add('review',title+' · בודקים',model=model,check=check,tense=tense)
def pause(name,image):add('pause',name,image=image)
add('cover','There is · There are',sub='כיתה ז׳ · אנגלית')
add('plan','מה נוכל לעשות בסוף?',steps=['להבחין בין מה שיש למישהו לבין מה שנמצא במקום.','לתאר יחיד ורבים, עכשיו ואתמול.','לומר מה אין ולשאול מה יש.','לקרוא, לבדוק רמזים ולנסח משפטים משלנו.'])
add('vocab','מילים שיעזרו לנו',entries=['g01-20','g02-03','g02-27','g02-01'],sub='מילים מקבוצות 01–02. מילה שעדיין לא פגשנו נלמד יחד לפני התרגול.')
rule('שייכות או מה נמצא במקום?','I have a bag.\nThere is a bag on the chair.','have מספר מה יש לי. there is מציג משהו שנמצא במקום. אותו תיק, שתי משמעויות שונות.')
ex('I have a soccer ball.','יש לי כדורגל.','מה יש לי?')
ex('There is a soccer ball on the chair.','יש כדורגל על הכיסא.','מה נמצא במקום?')
rule('have או has?','I / you / we / they → have\nhe / she / it → has','מסתכלים על מי שיש לו משהו, ולא על מספר החפצים. גם לחדר יכול להיות משהו: The room has two windows.')
ex('Ben has two history books.','לבן יש שני ספרי היסטוריה.','בעל החפצים הוא יחיד')
ex('We have one ball.','יש לנו כדור אחד.','בעלי החפץ הם רבים')
quiz('בודקים את המשמעות','יש כדור על השולחן.',['I have a ball.','There is a ball on the table.','He has a ball.'],1,'המשפט מתאר מה נמצא על השולחן. הוא אינו אומר למי הכדור שייך.')
quiz('שימו לב למי, לא לכמה','Ben ___ three pencils.',['have','are','has'],2,'Ben = he, ולכן has. שלושת העפרונות אינם משנים את הפועל שמתאים לבן.')
rule('there בתחילת המבנה','There is a bag here.','כאן there הוא חלק מהמבנה שמשמעותו „יש”. הוא אינו חייב לציין „שם”. אפשר לתאר גם משהו שנמצא כאן.')
pause('Northern Lights','../../grade9/assets/northern-lights.webp')
section='הווה: יש ואין'
rule('חיוב בהווה','There is + one thing\nThere are + two or more things','בודקים את שם העצם שמציגים: דבר אחד או כמה דברים?',rows=[['יחיד','There is a chair.'],['רבים','There are two chairs.']])
ex('There is a piano in the classroom.','יש פסנתר בכיתה.','יחיד')
ex('There are two windows in the classroom.','יש שני חלונות בכיתה.','רבים')
ex('There is a drawer under the table.','יש מגירה מתחת לשולחן.','המיקום בסוף המשפט')
ex('There is a Bible on the shelf.','יש תנ״ך על המדף.','מילה מקבוצה 01')
quiz('מה קובע את הפועל?','There ___ one book on the desks.',['are','is','have'],1,'one book הוא הדבר שמציגים, ולכן is. המילה desks מופיעה כחלק מתיאור המקום ואינה קובעת את הפועל.')
quiz('איתור טעות','איזה משפט תקין?',['There is three chairs.','There are three chairs.','There have three chairs.'],1,'three chairs הם רבים. המבנה הוא There are + רבים.')
quiz('חוזרים למשמעות','There are two books on the table. מה ידוע?',['הספרים שייכים לבן.','הספרים נמצאים על השולחן.','יש לי שני ספרים.'],1,'there are מציג מה נמצא במקום. כדי לומר שלבן יש ספרים נשתמש ב־Ben has.')
rule('שלילה בהווה','is not = isn’t\nare not = aren’t','מוסיפים not אחרי is או are. הקיצור אינו משנה את המשמעות.')
ex('There is not a computer in this room.','אין מחשב בחדר הזה.','שלילה מלאה')
ex("There isn't a computer in this room.",'אין מחשב בחדר הזה.','אותה משמעות בקיצור')
rule('אין אפילו אחד','There aren’t any + plural noun','בשלילה עם שם עצם ברבים משתמשים כאן ב־any: אין כאלה בכלל. בשאלה any עוזר לשאול אם יש כאלה.')
ex("There aren't any bags on the floor.",'אין תיקים על הרצפה.','שלילה ברבים')
quiz('מה נכון כשאין ספרים?','על המדף אין ספרים.',['There are books on the shelf.',"There isn't any books on the shelf.","There aren't any books on the shelf."],2,'books הם רבים, ולכן aren’t. any מתאים לשלילה: אין ספרים בכלל.',context='בחרו משפט בשלילה עם books ברבים.')
# Concrete non-illustrative evidence for subsequent judgments.
add('inventory','מה יש בחדר?',items=[['piano','1'],['windows','2'],['computer','0'],['bags on the floor','0']],sub='זהו חדר לדוגמה. קראו את הנתונים ואז תארו אותו באנגלית.',tense='הווה')
task('מתארים חדר בזוגות','לפי הנתונים: פסנתר אחד, שני חלונות, אין מחשב. אמרו שני משפטי חיוב ומשפט שלילה. בן הזוג בודק את שם העצם ואת הפועל.','There is a piano.\nThere are two windows.\nThere isn’t a computer.','בדקו: piano עם is; windows עם are; שלילה עם isn’t. אם המבנה והמשמעות מתאימים — הצלחתם. החליפו תפקידים.','הווה')
pause('Mount Everest','../../grade9/assets/mount-everest.webp')
section='הווה: שאלות'
add('vocab','מילים נוספות מהקבוצות',entries=['g01-14','g01-52','g02-07','g02-16'],sub='הפירושים כאן לקוחים מהמאגר. נשתמש במשמעות שמתאימה למשפט.')
ex('There is a short break after the exercise.','יש הפסקה קצרה אחרי התרגיל.','יש גם בזמן, לא רק במקום')
ex('There is an explanation on the board.','יש הסבר על הלוח.','מתארים מה יש')
ex('There is a mouse next to the computer.','יש עכבר מחשב ליד המחשב.','mouse בהקשר של מחשב')
rule('שאלה: הפועל עובר להתחלה','There is a piano. → Is there a piano?\nThere are bags. → Are there any bags?','מקדימים is או are ל־there. אין צורך להוסיף do או does.')
ex('Is there a piano in the classroom?','האם יש פסנתר בכיתה?','שאלה ביחיד')
ex('Yes, there is.','כן, יש.','תשובה קצרה ביחיד')
ex('Are there any bags on the floor?','האם יש תיקים על הרצפה?','שאלה ברבים')
ex("No, there aren't.",'לא, אין.','תשובה קצרה ברבים')
rule('התשובה שומרת על הפועל','Is there …? → Yes, there is. / No, there isn’t.\nAre there …? → Yes, there are. / No, there aren’t.','בתשובה קצרה משתמשים ב־there. בסוף תשובה חיובית קצרה אומרים Yes, there is. ולא Yes, there’s.')
quiz('סדר המילים בשאלה','בחרו שאלה תקינה.',['Do there are two windows?','Are there two windows?','There are two windows?'],1,'בשאלה מהסוג שלמדנו are עובר לפני there. אין מוסיפים do.')
quiz('מקשיבים למספר','Is there a computer?',['No, there aren’t.',"No, there isn't.",'No, it has.'],1,'השאלה מתחילה ב־Is there ולכן התשובה היא No, there isn’t.',context='נתון: אין מחשב בחדר.')
quiz('כן, ברבים','Are there two windows?',['Yes, there is.','Yes, they have.','Yes, there are.'],2,'השאלה עם are ולכן גם התשובה עם are.',context='נתון: בחדר יש שני חלונות.')
task('שאלות על הכיתה שלנו','בן זוג א׳ שואל על פסנתר. בן זוג ב׳ שואל על חלונות. ענו לפי הכיתה האמיתית, ואחר כך החליפו תפקידים.','Is there a piano?\nAre there any windows?','התשובה תלויה בכיתה. בדקו התאמה: Is → is / isn’t; Are → are / aren’t. תשובה שלילית נכונה חשובה כמו תשובה חיובית.','הווה')
rule('עוצרים ומחזירים מהזיכרון','יש → There …\nאין → There … not\nהאם יש? → … there?','בלי לחזור אחורה: אמרו מה משתנה בין יחיד לרבים ובין חיוב, שלילה ושאלה. לאחר מכן בדקו בשקף הסיכום.',tense='הווה')
add('summary','הווה במבט אחד',tense='הווה',rows=[['חיוב','There is a book.','There are books.'],['שלילה','There isn’t a book.','There aren’t any books.'],['שאלה','Is there a book?','Are there any books?'],['כן','Yes, there is.','Yes, there are.'],['לא','No, there isn’t.','No, there aren’t.']])
pause('Petra','../../grade9/assets/petra.webp')
add('checkpoint','סיום מפגש 1',sub='אמרו משפט חיובי, משפט שלילי ושאלה על הכיתה. הסבירו למה there is אינו אומר למי החפץ שייך. אפשר לעצור כאן ולהמשיך במפגש הבא.')
section='עבר: היה והיו'
add('restart','מפגש 2 · חוזרים בלי להציץ',sub='כתבו מהזיכרון משפט אחד עם There is, משפט עם There aren’t ושאלה עם Are there. בדקו בסיכום ההווה, ואז המשיכו.')
quiz('חזרה קצרה: שייכות או מקום?','There is a piano in the room. מה אפשר להסיק?',['יש פסנתר בחדר.','הפסנתר שייך לי.','לבן יש פסנתר.'],0,'מיקום אינו שייכות. לשייכות נאמר I have או Ben has. מבנה there נשאר הנושא המרכזי שלנו.')
add('vocab','עוד מילה לפני הקריאה',entries=['g02-28'],sub='נשתמש ב־lock כדי לתאר מה היה ומה לא היה בחדר.')
rule('אתמול: מחליפים רק את הפועל','is → was\nare → were','there נשאר. יחיד בעבר: was. רבים בעבר: were. חפשו רמזי זמן, למשל yesterday או last week.',tense='עבר')
ex('There was a drawer in the classroom yesterday.','הייתה מגירה בכיתה אתמול.','יחיד בעבר','עבר')
ex('There were three books in the drawer.','היו שלושה ספרים במגירה.','רבים בעבר','עבר')
quiz('רמז הזמן קובע','Yesterday, there ___ two balls in the room.',['are','was','were'],2,'Yesterday מציין עבר; two balls הם רבים. לכן were.','עבר')
rule('שלילה בעבר','was not = wasn’t\nwere not = weren’t','מוסיפים not אחרי was או were, בדיוק כמו בהווה. אין מוסיפים didn’t לפני was או were.',tense='עבר')
ex("There wasn't a ball in the drawer.",'לא היה כדור במגירה.','שלילה ביחיד בעבר','עבר')
ex("There weren't any pencils on the table.",'לא היו עפרונות על השולחן.','שלילה ברבים בעבר','עבר')
ex("There wasn't a lock on the drawer.",'לא היה מנעול על המגירה.','מילה מקבוצה 02','עבר')
quiz('תיקון טעות בעבר','איזה משפט שלילה תקין?',["There didn't were any bags.","There weren't any bags.","There wasn't any bags."],1,'bags הם רבים. בשלילה בעבר אומרים weren’t. אין לשלב didn’t עם were.','עבר')
rule('שאלות בעבר','There was a drawer. → Was there a drawer?\nThere were books. → Were there any books?','was או were עוברים לפני there. אין צורך ב־did.',tense='עבר')
ex('Was there a ball in the drawer?','האם היה כדור במגירה?','שאלה ביחיד בעבר','עבר')
ex("No, there wasn't.",'לא, לא היה.','תשובה קצרה ביחיד בעבר','עבר')
ex('Were there any books in the drawer?','האם היו ספרים במגירה?','שאלה ברבים בעבר','עבר')
ex('Yes, there were.','כן, היו.','תשובה קצרה ברבים בעבר','עבר')
quiz('לא מחליפים זמן באמצע','Were there any pencils?',['No, there aren’t.',"No, there weren't.","No, there wasn't."],1,'Were מציין רבים בעבר, ולכן weren’t. aren’t היה עונה על ההווה.','עבר',context='נתון: אתמול לא היו עפרונות על השולחן.')
add('summary','עבר במבט אחד',tense='עבר',rows=[['חיוב','There was a book.','There were books.'],['שלילה','There wasn’t a book.','There weren’t any books.'],['שאלה','Was there a book?','Were there any books?'],['כן','Yes, there was.','Yes, there were.'],['לא','No, there wasn’t.','No, there weren’t.']])
rule('גם שייכות יכולה להיות בעבר','Ben has a bag now.\nBen had a bag yesterday.','לשייכות בעבר משתמשים ב־had. כדי לומר שהיה משהו במקום משתמשים ב־there was או there were.',tense='')
quiz('משמעות לפני צורה','אתמול היה לבן תיק.',['There was a bag in the room.','Ben had a bag yesterday.','There were bags yesterday.'],1,'המשפט בעברית מספר מה היה לבן. לכן had. שאר האפשרויות מתארות מה היה במקום.','עבר')
task('עכשיו ואתמול','עבדו בזוגות. היום: שני ספרים ואין כדור. אתמול: ספר אחד וכדור אחד. אמרו משפט על היום, שני משפטים על אתמול ושאלה על אתמול.','There are two books today.\nThere was one book yesterday.\nThere was a ball yesterday.\nWas there a ball yesterday?','בדקו זמן, יחיד/רבים, והקדמת was בשאלה. אפשר גם משפט שלילה נכון על היום: There isn’t a ball today.')
pause('Northern Lights · A quiet moment','../../grade9/assets/northern-lights.webp')
section='קוראים ובודקים'
passage=[('Yesterday, there was a drawer in our classroom.','אתמול הייתה מגירה בכיתה שלנו.','עבר'),('There were three books in the drawer.','היו שלושה ספרים במגירה.','עבר'),("There wasn't a ball in the drawer.",'לא היה כדור במגירה.','עבר'),('Today, there is a ball on the table.','היום יש כדור על השולחן.','הווה'),('There are three books on the shelf.','יש שלושה ספרים על המדף.','הווה'),("There aren't any books in the drawer now.",'אין ספרים במגירה עכשיו.','הווה')]
add('reading','The Classroom Drawer',text=' '.join(x[0] for x in passage),sub='קראו פעם אחת: מה השתנה? לאחר מכן נבדוק כל משפט ונחפש ראיות.')
for en,he,t in passage:ex(en,he,'The Classroom Drawer',t)
quiz('שאלת קשב: המיקום השתנה','Where are the books now?',['In the drawer.','On the shelf.','Under the table.'],1,'עכשיו הספרים על המדף. במגירה היו ספרים אתמול. חזרו למשפט שמתחיל There are.')
quiz('שאלת קשב: מה באמת ידוע?','Who owns the ball?',['Ben.','The teacher.','The text does not say.'],2,'הטקסט מספר איפה הכדור נמצא. הוא אינו אומר למי הכדור שייך. there is אינו מוכיח שייכות.')
quiz('עבר מול הווה','Was there a ball in the drawer yesterday?',['Yes, there was.',"No, there wasn't.","No, there isn't."],1,'אתמול לא היה כדור במגירה. היום יש כדור על השולחן; זה אינו משנה את התשובה על אתמול.','עבר')
section='תרגול עצמאי'
rule('מקרה נוסף: מים','There is some water.\nThere isn’t any water.','water הוא שם עצם שאינו נספר ביחידות במבנה הזה, ולכן משתמשים ב־is. bottles הם בקבוקים שאפשר לספור: There are two bottles.')
ex('There is some water in the bottle.','יש מעט מים בבקבוק.','לא כל שם עצם מקבל מספר')
quiz('אתגר קצר','There ___ two bottles on the desk.',['is','are','has'],1,'סופרים bottles, ולכן are. מים בתוך הבקבוקים אינם משנים את ההתאמה.')
task('תיאור עצמאי: לפני ואחרי','בחרו חדר דמיוני. כתבו ארבעה משפטים: חיוב ושלילה על היום, חיוב על אתמול ושאלה על אתמול. אין צורך לציין פרטים אישיים.','There is a desk in the room.\nThere aren’t any bags on the floor.\nThere were two chairs yesterday.\nWas there a piano yesterday?','זו דוגמה, לא התשובה היחידה. סמנו בכל משפט: זמן, שם העצם והפועל. תקנו משפט אחד בעזרת בן הזוג. בדקו שהשלילה כוללת not או קיצור, ושהשאלה מתחילה בפועל.')
quiz('בדיקת יציאה: יחיד בהווה','There ___ a pencil on the books.',['are','is','has'],1,'a pencil הוא יחיד. books הוא חלק מתיאור המקום.')
quiz('בדיקת יציאה: שלילה בעבר','Yesterday, there ___ any chairs.',['aren’t',"wasn't","weren't"],2,'chairs הם רבים ו־Yesterday מציין עבר. לכן weren’t.','עבר')
quiz('בדיקת יציאה: שאלה','שאלו אם יש חלונות בחדר.',['Are there any windows in the room?','Is there any windows in the room?','Do there have windows in the room?'],0,'windows הם רבים. are עובר להתחלה ואין צורך ב־do.')
add('finish','לפני שסוגרים',text='מי? → have / has / had\nמה נמצא? → there is / are / was / were',sub='אמרו משפט אחד חדש בלי להסתכל. אחר כך חזרו לסיכום ובדקו את הזמן, המספר וסדר המילים.')
# Every displayed sentence token gets an individually accessible contextual Hebrew gloss.
gloss={'i':'אני','have':'יש ל־; שייכות','has':'יש לו / לה; שייכות ביחיד','had':'היה ל־; שייכות בעבר','a':'פריט אחד, לא מיודע','blue':'כחול','bag':'תיק','there':'חלק ממבנה יש / היה; בשאלה האם יש / היה','is':'יש ביחיד, כחלק מ־there is','are':'יש ברבים, כחלק מ־there are','was':'היה / הייתה ביחיד','were':'היו ברבים','on':'על','the':'ה־','chair':'כיסא','ben':'בן (שם)','two':'שניים / שתי','books':'ספרים','we':'אנחנו','one':'אחד / אחת','ball':'כדור','piano':'פסנתר','in':'ב־ / בתוך','classroom':'כיתה','windows':'חלונות','drawer':'מגירה','under':'מתחת ל־','table':'שולחן','not':'לא; יוצר שלילה','computer':'מחשב','this':'הזה / הזאת','room':'חדר',"isn't":'is not; אין ביחיד',"aren't":'are not; אין ברבים','any':'בשאלה: כלשהם; בשלילה: אין בכלל','bags':'תיקים','floor':'רצפה','yes':'כן','no':'לא','yesterday':'אתמול','three':'שלושה / שלוש',"wasn't":'was not; לא היה / הייתה',"weren't":'were not; לא היו','pencils':'עפרונות','our':'שלנו','today':'היום','shelf':'מדף','now':'עכשיו','some':'כמות כלשהי / מעט','water':'מים','bottle':'בקבוק'}
gloss.update({'soccer':'כדורגל','history':'היסטוריה','bible':'התנ״ך; כתבי הקודש','short':'קצר / קצרה','break':'הפסקה; חופשה','after':'אחרי','exercise':'תרגיל; פעילות גופנית','an':'פריט אחד, לא מיודע','explanation':'הסבר','board':'לוח','mouse':'עכבר מחשב','next':'חלק מהביטוי next to: ליד','to':'חלק מהביטוי next to: ליד','lock':'מנעול'})
for x in sentences:
 x['words']=[]
 for word in x['en'].split():
  key=re.sub(r"[^a-z']",'',word.lower());assert key in gloss,(key,x)
  meaning=gloss[key]
  if key in ['is','are'] and x['en'].startswith(('Is ','Are ')):meaning='פועל בתחילת שאלה: האם יש?'
  if key in ['was','were'] and x['en'].startswith(('Was ','Were ')):meaning='פועל בתחילת שאלה: האם היה / היו?'
  x['words'].append(dict(word=word,he=meaning))
for sl in slides:
 if sl['kind']=='vocab':sl['entries']=[{k:vmap[e][k] for k in ['id','group','word','meaning']} for e in sl['entries']]
data=dict(vocabularySource='../band2-groups-01-02/entries.json',title='There is · There are',created='יום ראשון, ט׳ בתשרי תשפ״ז (20.9.2026)',sections=list(dict.fromkeys(s['section'] for s in slides)),sentences=sentences,slides=slides)
R.mkdir(parents=True,exist_ok=True)
(R/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(R/'data.js').write_text('const LESSON='+json.dumps(data,ensure_ascii=False)+';\n')
print(json.dumps({'slides':len(slides),'sentences':len(sentences),'questions':sum(s['kind']=='quiz' and not s['reveal'] for s in slides),'words':sum(len(s['words']) for s in sentences)},ensure_ascii=False))
