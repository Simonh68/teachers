"""First exam preparation: source-preserving reading and scaffolded practice."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'grade7/first-exam-preparation'
story=json.loads((ROOT/'grade7/the-same-way/story.json').read_text())
old=json.loads((ROOT/'grade7/there-is-there-are/content.json').read_text())
raw=(ROOT/'grade7/the-same-way/sentence-word-translations.js').read_text()
storywords=json.loads(raw[raw.index('['):].rstrip().rstrip(';'))
slides=[];sentences=[];section='מתכוננים'
def add(kind,title,**kw):slides.append(dict(kind=kind,title=title,section=section,**kw))
def rule(title,formula,he,tense=''):add('rule',title,formula=formula,he=he,tense=tense)
def ex(en,he,title='קוראים ומבינים',tense='',words=None):
 n=len(sentences);sentences.append(dict(en=en,he=he,words=words))
 for reveal in (False,True):add('sentence',title,n=n,en=en,he=he,tense=tense,reveal=reveal)
def quiz(title,q,opts,correct,why,tense='',context=''):
 for reveal in (False,True):add('quiz',title,q=q,opts=opts,correct=correct,why=why,tense=tense,context=context,reveal=reveal)
def task(title,prompt,model,check):
 add('task',title,prompt=prompt);add('review',title+' · בודקים',model=model,check=check)
def pause(n):add('pause',['Northern Lights','Mount Everest','Petra'][n%3],image='../../grade9/assets/'+['northern-lights','mount-everest','petra'][n%3]+'.webp')
add('cover','הכנה למבחן הראשון',sub='כיתה ז׳ · אנגלית')
add('plan','מה נתרגל?',steps=['מזהים מה מילת השאלה מבקשת.','מוצאים בסיפור ראיה לתשובה קצרה.','מבחינים בין יש במקום לבין שייכות.','כותבים ובודקים משפטים שלמים.'])
rule('מבנה המבחן','Read → Find → Answer','עמוד ראשון: הסיפור. עמוד שני: חמש שאלות הבנה, ובחירה של חמישה מתוך שבעה משפטים לכתיבה באנגלית. כאן מתרגלים את הדרך לפתרון.')
section='מילות שאלה'
for word,meaning,q,he,hint in [
 ('Who','מי','Who is in the classroom?','מי נמצא בכיתה?','מחפשים אדם או אנשים.'),
 ('Where','איפה / היכן','Where is the school?','איפה בית הספר?','מחפשים מקום.'),
 ('When','מתי','When is the break?','מתי ההפסקה?','מחפשים זמן.'),
 ('What','מה','What is in the bag?','מה יש בתיק?','מחפשים דבר או מידע שמתאים לשאלה.'),
 ('Why','למה / מדוע','Why is the boy worried?','למה הילד מודאג?','מחפשים סיבה. because עוזר להסביר אותה.'),
 ('How many','כמה','How many boys are there?','כמה בנים יש?','מחפשים מספר. אחרי How many בא כאן שם עצם ברבים.')]:
 rule(word,word,meaning+' — '+hint);ex(q,he,'מזהים מה מבקשים')
 if word=='When':quiz('אדם, מקום או זמן?','התשובה היא: At school. מהי מילת השאלה?',['Who','Where','When'],1,'At school הוא מקום, ולכן Where. אדם היה מתאים ל־Who וזמן ל־When.');pause(0)
quiz('סיבה או מספר?','התשובה היא: Because he is tired. איזו פתיחה מתאימה?',['How many','Where','Why'],2,'Because מציג סיבה. Why מבקש סיבה.')
quiz('בוחרים מילת שאלה','___ books are in the bag?',['How many','Who','When'],0,'books הם דברים שאפשר לספור. How many מבקש את מספר הספרים.')
task('מנסים בלי אפשרויות','כתבו באנגלית את מילת השאלה המתאימה לכל תשובה: Two boys. / Tomorrow. / Ben and Noam.','How many?\nWhen?\nWho?','Two נותן כמות; Tomorrow נותן זמן; Ben and Noam הם אנשים. בדקו כל שורה בנפרד ותקנו אם צריך.')
rule('איך עונים על שאלת הבנה?','Question word → Evidence → Short answer','מסמנים מילת שאלה, מחפשים את הפסקה המתאימה, ואז בוחרים רק את המידע שנשאל. אין צורך להעתיק פסקה שלמה.')
section='משפחת How'
rule('How משנה את סוג השאלה','How + word','How לבדו שואל איך. המילה שמצטרפת אליו משנה את מה שמבקשים: כמות, זמן, מרחק, גיל או תיאור. אל תתרגמו כל How באופן אוטומטי ל״איך״.')
ex('How do you get to school?','איך אתם מגיעים לבית הספר?','How: דרך או אופן')
quiz('How בלי מילה מתארת','How do you get to school?',['By bus.','At seven.','Two buses.'],0,'How כאן מבקש דרך הגעה. By bus מתאים. At seven עונה על When, ו־Two buses נותן כמות.')
rule('How many לעומת How much','How many books?\nHow much water?','many עם דברים שסופרים ביחידות: books, boys, buses. much עם כמות שאינה נספרת כאן ביחידות: water. אפשר לספור בקבוקים, ולכן How many bottles?')
ex('How much water is in the bottle?','כמה מים יש בבקבוק?','How much: כמות')
quiz('סופרים את שם העצם שבשאלה','___ bottles are there?',['How much','How many','How long'],1,'bottles הם בקבוקים שאפשר לספור. בוחרים many גם כשהבקבוקים מכילים מים.')
quiz('מים אינם מספר בקבוקים','___ water is in the bottle?',['How many','How far','How much'],2,'השאלה היא על כמות water, ולא על מספר bottles. לכן much.')
rule('How much גם שואל מחיר','How much is …?','כששואלים על מחיר, How much פירושו כמה זה עולה. התשובה היא סכום כסף. מבדילים לפי ההקשר בין מחיר לכמות.')
ex('How much is this bag?','כמה עולה התיק הזה?','How much: מחיר')
quiz('מה מבקשים בחנות?','How much is this bag?',['Twenty shekels.','Two bags.','Ten minutes.'],0,'בחנות שואלים כאן על מחיר. Twenty shekels הוא סכום כסף; Two bags הוא מספר תיקים.')
pause(1)
rule('How long: משך זמן','How long is the break?','מבקשים כמה זמן ההפסקה נמשכת. תשובה אפשרית היא Ten minutes. לעומת זאת When מבקש מתי היא מתחילה או מתקיימת.')
ex('How long is the break?','כמה זמן נמשכת ההפסקה?','How long: משך')
quiz('מתי לעומת כמה זמן','התשובה היא: Ten minutes. איזו שאלה מתאימה?',['When is the break?','How long is the break?','How many breaks are there?'],1,'Ten minutes הוא משך זמן. At ten הוא זמן בשעון ומתאים ל־When.')
rule('How long: גם אורך','How long is the train?','אותו צירוף יכול לשאול על אורך של חפץ. התשובה כאן תהיה במטרים, למשל. משך נסיעה נמדד בדקות; אורך רכבת נמדד במטרים.')
ex('How long is the train?','מה אורך הרכבת?','How long: אורך')
rule('How far: מרחק','How far is … from …?','שואלים על המרחק בין מקומות. למשל: Two kilometers. אין לבלבל בין מרחק לבין משך הדרך: Twenty minutes עונה על How long.')
ex('How far is the school from home?','מה המרחק מבית הספר לבית?','How far: מרחק')
quiz('מרחק או משך?','התשובה היא: Two kilometers. מה שואלים?',['How long','How far','How old'],1,'kilometers מודד מרחק ולכן How far. אין צורך לדעת את המרחק לבית הספר של דן: זו דוגמה חדשה.')
rule('How good: איכות או רמה','How good is …?','שואלים עד כמה משהו טוב. תשובה מתאימה יכולה להיות Very good. How + תואר מתאר מידה: לא מספר ולא מחיר.')
ex('How good is your English?','עד כמה האנגלית שלך טובה?','How good: רמה')
quiz('תשובה שמתאימה לתיאור','How good is the food?',['Very good.','Three plates.','At school.'],0,'good שואל על איכות האוכל. Very good מתאר איכות; מספר צלחות ומקום אינם עונים לשאלה.')
rule('How small: עד כמה קטן','How small is …?','זו שאלה תקינה על מידת הקוטן, בדרך כלל כשכבר מדברים על משהו קטן. How big שואל באופן כללי מה הגודל. אין מתרגמים How small ל״כמה דברים קטנים״.')
ex('How small is the bag?','עד כמה התיק קטן?','How small: גודל')
quiz('גודל או מספר?','How small is the bag?',['Very small.','Three bags.','Ten shekels.'],0,'Very small מתאר גודל. Three bags נותן מספר ומתאים ל־How many. Ten shekels נותן מחיר ומתאים ל־How much.')
rule('How old: גיל','How old is …?','שואלים בן כמה או בת כמה. למשל: Twelve years old. old בצירוף הזה אינו אומר שהאדם זקן.')
ex('How old is your brother?','בן כמה אחיך?','How old: גיל')
quiz('איזו משפחה של תשובה?','Twelve years old.',['How far','How good','How old'],2,'years old מתאר גיל. זוהי דוגמה חדשה; הסיפור אינו מוסר את גיל האח.')
task('עכשיו בלי אפשרויות','התאימו בעל פה צירוף How לכל תשובה: Three books. / A little water. / Ten minutes. / Very small.','How many?\nHow much?\nHow long?\nHow small?','בדקו כל שורה: מספר פריטים, כמות מים, משך זמן, גודל. אם החלפתם many ו־much, חזרו לשם העצם ושאלו אם סופרים אותו ביחידות.')
add('howSummary','סיכום משפחת How',rows=[['דרך / אופן','How'],['מספר פריטים','How many'],['כמות / מחיר','How much'],['משך זמן / אורך','How long'],['מרחק','How far'],['איכות / רמה','How good'],['מידת הקוטן','How small'],['גיל','How old']])
pause(2)
section='חזרה על הסיפור'
add('whole','The Same Way',paragraphs=story['paragraphs'],sub='קראו וחפשו: מה מדאיג את דן, ומה משתנה בסוף?')
add('readalong','Read Alone Text')
for idx,s in enumerate(story['sentences']):
 ex(s['en'],s['he'],'פסקה '+s['part']+' · משפט '+str(idx+1)+' / 28',words=storywords[idx])
 if idx==3:quiz('מוצאים ראיה בפסקה A','What does Dan carry every morning?',['A heavy blue bag.','A red cap.','A green bag.'],0,'בפסקה A נאמר: a heavy blue bag. התיק הירוק והכובע האדום שייכים לבנים האחרים.')
 if idx==9:
  quiz('קשב לסדר בפסקה B','What does Dan take after the first bus?',['Another bus.','A train.','A car.'],1,'קודם אוטובוס לתחנת הרכבת, אחריו רכבת, ואז אוטובוס נוסף. חפשו First ו־Then.');pause(1)
 if idx==14:quiz('מה קורה עכשיו?','Are Dan’s books wet now?',['Yes, they are.','The story says they will be wet when it rains.','He has no books.'],1,'זהו חשש לעתיד, לא תיאור ספרים רטובים עכשיו. חפשו will be בפסקה C.')
 if idx==22:
  task('תשובה קצרה עם ראיה','Who says “I worry about the rain”? כתבו תשובה קצרה והצביעו על הרמז בפסקה D.','Ben.','שם הדובר מופיע אחרי הציטוט: says Ben. אם כתבתם Dan, הוא אכן מודאג, אך השאלה מבקשת מי אמר את המשפט המסוים.');pause(2)
quiz('מה משתנה בסוף?','What is still a problem?',['The rain.','The classroom door.','A lost phone.'],0,'בפסקה E נאמר שהגשם עדיין בעיה. החברות השתנתה; בעיית הגשם עדיין לא נפתרה.')
section='יש ושייכות'
rule('שתי משמעויות של יש','I have a bag.\nThere is a bag at the bus stop.','have / has מתארים שייכות. there is / there are מתארים מה יש או נמצא במקום. לא מסיקים למי החפץ שייך רק ממיקומו.','הווה')
ex('There is a bag at the bus stop.','יש תיק בתחנת האוטובוס.','יחיד: יש במקום','הווה')
ex('There are two boys at the bus stop.','יש שני בנים בתחנת האוטובוס.','רבים: יש במקום','הווה')
quiz('בוחרים לפי מה שמציגים','There ___ a bag near the boys.',['are','is','has'],1,'a bag הוא יחיד. boys מופיע בתיאור המקום ואינו קובע כאן את הפועל.','הווה')
ex('Daniel has a green bag.','לדניאל יש תיק ירוק.','דוגמה חדשה: שייכות','הווה')
quiz('מי או מה נמצא?','יש לי שני ספרים.',['There are two books.','I have two books.','I has two books.'],1,'יש לי מציין שייכות. I מתאים ל־have גם כשיש יותר מספר אחד.','הווה')
rule('חיוב, שלילה ושאלה','There is → There isn’t → Is there?\nThere are → There aren’t → Are there?','בשלילה מוסיפים not או משתמשים בקיצור. בשאלה מעבירים is / are לפני there.','הווה')
ex("There isn't a train at the station.",'אין רכבת בתחנה.','שלילה ביחיד','הווה')
ex("There aren't any books in the bag.",'אין ספרים בתיק.','שלילה ברבים','הווה')
ex('Are there any books in the bag?','האם יש ספרים בתיק?','שאלה ברבים','הווה')
quiz('התאמה בתשובה','Are there any books in the bag?',['No, there isn’t.',"No, there aren't.",'No, I hasn’t.'],1,'השאלה עם are ולכן התשובה עם aren’t.','הווה','בתרגיל הזה התיק ריק.')
add('summary','סיכום there is / there are',tense='הווה',rows=[['חיוב','There is a bag.','There are books.'],['שלילה','There isn’t a bag.','There aren’t any books.'],['שאלה','Is there a bag?','Are there any books?'],['כן','Yes, there is.','Yes, there are.'],['לא','No, there isn’t.','No, there aren’t.']])
pause(0)
section='כותבים ובודקים'
rule('מ־I אל he','I am → He is\nI have → He has','כשמשנים מי מדבר, בודקים גם את הפועל וגם את מילת השייכות: my → his. בסיפור I הוא דן.','הווה')
task('מתרגמים לפי משמעות','כתבו באנגלית: יש שני ספרים על הכיסא. אחר כך: לדניאל יש שני ספרים.','There are two books on the chair.\nDaniel has two books.','במשפט הראשון מקום ולכן There are. בשני Daniel = he ולכן has. שתי צורות שונות גם כשהכמות זהה.')
task('שלילה עם To Be','כתבו באנגלית: התיק שלי כחול, אבל הספרים שלי אינם רטובים.','My bag is blue, but my books are not wet.','bag ביחיד מקבל is; books ברבים מקבלים are not. גם aren’t תקין. but מחבר בין החלקים.')
task('הופכים משפט לשאלה','The boys are in the classroom. כתבו שאלה שמתחילה ב־Are.','Are the boys in the classroom?','are עובר לפני The boys. אין מוסיפים there כי השאלה היא על הבנים המסוימים, לא האם יש בנים כלשהם.')
task('משפט על מחר','כתבו באנגלית: אנחנו רוצים להצטרף אליכם מחר. היעזרו ב־want to ובפסקה E.','We want to join you tomorrow.','בדקו: We, אחריו want to, אחריו join. you כאן פירושו אליכם. בסוף tomorrow ונקודה.')
section='בדיקת יציאה'
quiz('מילת שאלה','___ is the red cap? — On the chair.',['Who','Where','Why'],1,'On the chair הוא מקום ולכן Where.')
quiz('יש ברבים','There ___ two bags near the door.',['has','is','are'],2,'two bags הם רבים ולכן are.','הווה')
task('ניסיון עצמאי אחרון','בלי אפשרויות: When will Dan say hello at the bus stop? אחר כך כתבו: יש כובע אדום על הכיסא.','Tomorrow.\nThere is a red cap on the chair.','When מבקש זמן: Tomorrow. במשפט הכתיבה מציגים cap ביחיד במקום, ולכן There is. בדקו אות גדולה ונקודה.')
add('finish','לפני המבחן',text='Read → Find evidence → Answer → Check',sub='האם עניתי על מה שנשאל? האם מצאתי ראיה? בכתיבה: מי הנושא, יחיד או רבים, שייכות או יש במקום?')
gloss={}
norm=lambda w:re.sub(r"[^a-z0-9']",'',w.lower().replace('’',"'"))
for sent in old['sentences']:
 for w in sent['words']:gloss[norm(w['word'])]=w['he']
for sent in storywords:
 for w in sent:gloss[norm(w['word'])]=w['he']
gloss.update({'boy':'ילד','do':'פועל עזר בשאלה בהווה','get':'מגיעים; כאן get to: להגיע אל','much':'כמה; כמות או מחיר','long':'ארוך; בצירוף How long: כמה זמן או מה האורך','far':'רחוק; בצירוף How far: מה המרחק','good':'טוב; כאן רמה טובה','your':'שלך / שלכם','english':'אנגלית','small':'קטן','old':'בצירוף How old: בן כמה / בת כמה','who':'מי','where':'איפה / היכן','when':'מתי','why':'למה / מדוע','how':'בביטוי How many: כמה','many':'בביטוי How many: כמה','worried':'מודאג','daniel':'דניאל','any':'כלשהם; בשלילה: אין בכלל',"isn't":'is not; אין ביחיד',"aren't":'are not; אין ברבים'})
for s in sentences:
 if s['words'] is not None:continue
 s['words']=[]
 for w in s['en'].split():
  k=norm(w);assert k in gloss,(w,s)
  meaning=gloss[k]
  if k=='there':meaning='חלק מהמבנה יש / האם יש'
  if k in ('is','are'):meaning='פועל בהווה: התאמה ליחיד / רבים; במבנה there פירושו יש'
  s['words'].append(dict(word=w,he=meaning))
data=dict(title='הכנה למבחן הראשון',created='יום ראשון, ט׳ בתשרי תשפ״ז (20.9.2026)',sections=list(dict.fromkeys(s['section'] for s in slides)),sentences=sentences,slides=slides)
(R/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(R/'data.js').write_text('const LESSON='+json.dumps(data,ensure_ascii=False)+';\n')
print('Slides',len(slides),'sentences',len(sentences))
