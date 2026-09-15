"""Build the shared, progressively revealed Connectors lesson."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade9/connectors'
S=[]
chapter='פתיחה'
connectors=[]

def slide(kind='explain', **kw):
    S.append(dict(kind=kind,chapter=chapter,**kw))

def pair(kind='example', **kw):
    # Identical data, including reserved translation space. Only visibility changes.
    key=f'p{len(S)+1}'
    slide(kind,pair=key,reveal=False,**kw)
    slide(kind,pair=key,reveal=True,**kw)

def explain(title,body,formula='',family='',note=''):
    slide('explain',title=title,body=body,formula=formula,family=family,note=note)

def idea(family,caption):
    groups={'result':'cause','purpose':'cause','example':'addition','sequence':'addition'}
    image_family=groups.get(family,family)
    suffix='a' if sum(s['kind']=='idea' for s in S)%2==0 else 'b'
    slide('idea',family=family,image=image_family+'-'+suffix,en=caption)

def example(family,title,sentence,he,meaning='',base='',tense='הווה'):
    pair(family=family,title=title,sentence=sentence,he=he,meaning=meaning,base=base,tense=tense)

def teach(family,title,sentence,he,meaning,base='',caption='',tense='הווה'):
    if connectors: idea(family,caption or {'contrast':'Still playing.','addition':'One more idea.','cause':'No power.','result':'No call.','example':'One example.','sequence':'What comes next?','purpose':'Time to charge.'}[family])
    connectors.append(title)
    example(family,title,sentence,he,meaning,base,tense)

def practice(family,prompt,question,answer,he,why,tense='הווה'):
    common=dict(family=family,title='Your turn',prompt=prompt,question=question,answer=answer,he=he,why=why,tense=tense)
    slide('practice',answerVisible=False,reveal=False,**common)
    pair('practice',answerVisible=True,**common)

def recap(title,family,rows,note=''):
    pair('summary',title=title,family=family,rows=rows,note=note)

pair('cover',title='Connectors',he='מילות קישור')
explain('מה נלמד לעשות?','נחבר שני רעיונות, נבחר מילת קישור מתאימה, ונבדוק את המבנה ואת הפיסוק.')
explain('בכל דוגמה','קראו את האנגלית ונסו להבין לפי ההקשר. עצרו לפני המעבר הבא; אחריו יתווסף התרגום בלבד.')
explain('שלוש בדיקות לפני שכותבים','מה הקשר בין הרעיונות? מה צריך לבוא אחרי מילת הקישור? איזה סימן פיסוק צריך?')

chapter='ניגוד · הבסיס'
B='The cat is tired, but it keeps playing.'
explain('שני רעיונות שלא מסתדרים כצפוי','החתול עייף. מה היינו מצפים שהוא יעשה? ומה הוא עושה בפועל?',family='contrast')
teach('contrast','But','The cat is tired<em>,</em> <b>but</b> it keeps playing.','החתול עייף, אבל הוא ממשיך לשחק.','אבל')
explain('מזהים שני חלקים שלמים','לכל חלק יש נושא ופועל. כאן מחברים אותם בתוך משפט אחד.','The cat is tired <em>│</em> it keeps playing.',family='contrast')
teach('contrast','However','The cat is tired<em>.</em> <b>However</b><em>,</em> it keeps playing.','החתול עייף. עם זאת, הוא ממשיך לשחק.','עם זאת / אולם',B)
explain('שלב 1 · מפרידים','מוציאים את but והופכים את שני החלקים לשני משפטים.','The cat is tired<em>.</em> It keeps playing.',family='contrast')
explain('שלב 2 · מוסיפים בתחילת המשפט השני','כותבים However ואחריו פסיק. בדוגמה הזו it ממשיך באות קטנה.','The cat is tired<em>.</em> <b>However</b><em>,</em> it keeps playing.',family='contrast')
explain('שלב 3 · בודקים מה נשאר','החתול עדיין עייף ועדיין משחק. השינוי הוא בדרך שבה מחברים את הרעיונות.','A<em>,</em> <b>but</b> B.  →  A<em>.</em> <b>However</b><em>,</em> B.',family='contrast')
practice('contrast','החליפו את but ב־However. שימו לב לפיסוק.','Dan is tired, but he studies.','Dan is tired<em>.</em> <b>However</b><em>,</em> he studies.','דן עייף. עם זאת, הוא לומד.','במבנה הזה: נקודה לפני However ופסיק אחריו.')
recap('סיכום ביניים · אותו קשר, מבנה אחר','contrast',[
 ['but','אבל','A, but B.'],['however','עם זאת','A. However, B.']],
 'במבנה המתורגל כאן, לא מחליפים רק מילה: משנים גם את הפיסוק.')

chapter='ניגוד · משנים את המבנה'
teach('contrast','Although','<b>Although</b> the cat is tired<em>,</em> it keeps playing.','אף שהחתול עייף, הוא ממשיך לשחק.','אף ש־ / למרות ש־',B)
explain('אחרי Although · נושא ופועל','בחלק הראשון יש נושא ופועל. כשהחלק הזה פותח את המשפט, מפרידים אחריו בפסיק.','<b>Although</b> the cat <u>is</u> tired<em>,</em> it keeps playing.',family='contrast')
explain('לא מוסיפים but לאותו חיבור','בחרו אחד משני המבנים. אחרי פתיחה ב־Although, ממשיכים ישר לרעיון השני.','<b>Although</b> A<em>,</em> B.',family='contrast')
teach('contrast','Even though','<b>Even though</b> the cat is tired<em>,</em> it keeps playing.','אף שהחתול עייף, הוא בכל זאת ממשיך לשחק.','אף ש־, בהדגשה',B)
explain('מבנה מוכר · הדגשה חזקה יותר','Even though משתמש באותו מבנה כמו Although ומדגיש את הפער בין הציפייה למציאות.','<b>Even though</b> A<em>,</em> B.',family='contrast')
teach('contrast','Despite','<b>Despite</b> <u>its tiredness</u><em>,</em> the cat keeps playing.','למרות עייפותו, החתול ממשיך לשחק.','למרות',B)
explain('שלב 1 · מצמצמים לצירוף שמני','במבנה הזה לא כותבים אחרי Despite את המשפט the cat is tired. הופכים אותו לצירוף שמני.','the cat is tired  →  <u>its tiredness</u>',family='contrast')
explain('שלב 2 · מחברים מחדש','אחרי Despite מופיע כאן צירוף שמני. לא מוסיפים of.','<b>Despite</b> <u>its tiredness</u><em>,</em> the cat keeps playing.',family='contrast')
practice('contrast','חברו בעזרת Although. התחילו במילה Although.','It is raining. We play outside.','<b>Although</b> it is raining<em>,</em> we play outside.','אף שיורד גשם, אנחנו משחקים בחוץ.','פסיק אחרי החלק הפותח; ללא but.')
practice('contrast','כתבו את אותו רעיון בעזרת Despite.','Although it is raining, we play outside.','<b>Despite</b> <u>the rain</u><em>,</em> we play outside.','למרות הגשם, אנחנו משחקים בחוץ.','it is raining הפך לצירוף השמני the rain.')
recap('סיכום ביניים · מה בא אחרי הביטוי?','contrast',[
 ['although / even though','אף ש־','Although it is raining, …'],['despite','למרות','Despite the rain, …']],
 'Although ו־Even though: נושא ופועל. Despite: כאן צירוף שמני; אפשר גם צורת ing.')

chapter='ניגוד · חלופות והבדלי משמעות'
for word,meaning,he in [
 ('Nevertheless','אף על פי כן','החתול עייף. אף על פי כן, הוא ממשיך לשחק.'),
 ('Nonetheless','אף על פי כן','החתול עייף. אף על פי כן, הוא ממשיך לשחק.'),
 ('Even so','למרות זאת','החתול עייף. למרות זאת, הוא ממשיך לשחק.')]:
    teach('contrast',word,f'The cat is tired<em>.</em> <b>{word}</b><em>,</em> it keeps playing.',he,meaning,B)
explain('המשמעות קודמת למילה המרשימה','Nevertheless ו־Nonetheless רשמיים יותר. אין צורך להחליף However בכל משפט; בוחרים ביטוי שמתאים להקשר.',family='contrast')
teach('contrast','On the contrary','The cat isn’t lazy<em>.</em> <b>On the contrary</b><em>,</em> it is full of energy.','החתול אינו עצלן. להפך, הוא מלא אנרגיה.','להפך','The cat isn’t lazy; it is full of energy.',caption='Lazy? Look again.')
explain('כאן מתקנים רושם שגוי','On the contrary דוחה טענה או רושם ומציג את ההפך. עייפות ומשחק יכולים להתקיים יחד; עצלנות ומרץ מוצגים כאן כהפכים.',family='contrast')
practice('contrast','איזה ביטוי מתאים: However או On the contrary?','This task isn’t boring. ____, it is exciting.','This task isn’t boring<em>.</em> <b>On the contrary</b><em>,</em> it is exciting.','המשימה הזאת אינה משעממת. להפך, היא מרגשת.','המשפט השני מציג את ההפך מהרושם שנדחה.')
recap('סיכום ביניים · שלושה סוגי ניגוד','contrast',[
 ['however / even so','עם זאת / למרות זאת','A. However, B.'],['nevertheless / nonetheless','אף על פי כן','A. Nevertheless, B.'],['on the contrary','להפך','Not A. On the contrary, B.']],
 'לא כל ביטוי מתאים לכל ניגוד. שאלו אם מדובר בפער מהציפייה או בתיקון טענה.')

chapter='תוספת · עוד פרט ועוד נימוק'
A='The app has games, and it has stories.'
explain('מוסיפים לרעיון הקיים','במשפחה הבאה מצרפים פרט נוסף. לא מחפשים ניגוד ולא מסבירים סיבה.',family='addition')
teach('addition','And','The app has games<em>,</em> <b>and</b> it has stories.','באפליקציה יש משחקים, ויש בה סיפורים.','ו־')
teach('addition','Also','The app has games<em>.</em> It <b>also</b> has stories.','באפליקציה יש משחקים. יש בה גם סיפורים.','גם',A)
explain('Also · שמים לב למיקום','בדוגמה הזאת also בא לפני הפועל העיקרי has. אחרי be הוא בדרך כלל בא אחרי הפועל.','It <b>also</b> has stories.  /  It is <b>also</b> free.',family='addition')
teach('addition','Too','The app has games<em>.</em> It has stories <b>too</b>.','באפליקציה יש משחקים. יש בה גם סיפורים.','גם',A)
explain('אותו רעיון · מיקום אחר','במשפטים האלה also בא באמצע ו־too בסוף. לא משאירים את המילה באותו מקום באופן אוטומטי.','It <b>also</b> has stories.  →  It has stories <b>too</b>.',family='addition')
teach('addition','In addition','The app has games<em>.</em> <b>In addition</b><em>,</em> it has stories.','באפליקציה יש משחקים. בנוסף, יש בה סיפורים.','בנוסף',A)
explain('חוזרים למבנה שכבר הכרנו','מסיימים את המשפט הראשון. פותחים את השני בביטוי ובפסיק.','A<em>.</em> <b>In addition</b><em>,</em> B.',family='addition')
practice('addition','החליפו את and ב־In addition.','The app has music, and it has games.','The app has music<em>.</em> <b>In addition</b><em>,</em> it has games.','באפליקציה יש מוזיקה. בנוסף, יש בה משחקים.','שני משפטים שלמים; פסיק אחרי הביטוי.')
for word,meaning in [('Moreover','יתרה מזאת'),('Furthermore','יתר על כן'),('Additionally','בנוסף')]:
    teach('addition',word,f'The app has games<em>.</em> <b>{word}</b><em>,</em> it has stories.',f'באפליקציה יש משחקים. {meaning}, יש בה סיפורים.',meaning,A)
explain('מתי התוספת גם מחזקת טענה?','אם אנחנו מסבירים למה האפליקציה שימושית, סיפורים הם יתרון נוסף. Moreover ו־Furthermore מתאימים במיוחד להוספת נימוק מחזק.',family='addition')
teach('addition','Not to mention','The app has games<em>,</em> <b>not to mention</b> <u>stories</u>.','באפליקציה יש משחקים, שלא לדבר על סיפורים.','שלא לדבר על',A)
explain('כאן מוסיפים שם עצם','בדוגמה הזאת הביטוי מוביל ישירות ל־stories. לא מעתיקים אחריו את כל המשפט it has stories.','games<em>,</em> <b>not to mention</b> <u>stories</u>',family='addition')
recap('סיכום ביניים · תוספת ומיקום','addition',[
 ['also / too','גם','It also has stories. / It has stories too.'],['in addition / additionally','בנוסף','A. In addition, B.'],['moreover / furthermore','יתרה מזאת / יתר על כן','A. Moreover, B.']],
 'בחרו חלופה אחת מתאימה; אין צורך לצרף כמה מילות קישור לאותה תוספת.')
practice('addition','סדרו את המילים למשפט עם also.','It / stories / also / has','It <b>also</b> has stories.','יש בה גם סיפורים.','במשפט הזה also בא לפני has.')

chapter='סיבה · משפט או צירוף שמני'
C='My phone is off because the battery is dead.'
explain('שואלים למה','הטלפון כבוי. הסוללה ריקה. נזהה איזה פרט מסביר את האחר.',family='cause')
teach('cause','Because','My phone is off <b>because</b> the battery is dead.','הטלפון שלי כבוי כי הסוללה ריקה.','כי / מפני ש־')
explain('אחרי Because · הסיבה במשפט','הסיבה כוללת נושא ופועל: the battery + is.','My phone is off <b>because</b> the battery <u>is</u> dead.',family='cause')
teach('cause','Since','My phone is off <b>since</b> the battery is dead.','הטלפון שלי כבוי מכיוון שהסוללה ריקה.','מכיוון ש־',C)
explain('Since · בודקים את ההקשר','כאן Since מציין סיבה. במקומות אחרים הוא מציין זמן; לא בוחרים פירוש בלי לקרוא את המשפט.',family='cause')
teach('cause','Given that','<b>Given that</b> the battery is dead<em>,</em> my phone is off.','בהתחשב בכך שהסוללה ריקה, הטלפון שלי כבוי.','בהתחשב בכך ש־',C)
explain('פותחים בעובדה שעליה נשענים','אחרי Given that באים נושא ופועל. כשהחלק הזה פותח את המשפט, שמים אחריו פסיק.','<b>Given that</b> the battery is dead<em>,</em> my phone is off.',family='cause')
teach('cause','Because of','My phone is off <b>because of</b> <u>the dead battery</u>.','הטלפון שלי כבוי בגלל הסוללה הריקה.','בגלל',C)
explain('שלב 1 · מזהים את שינוי המבנה','תוספת of משנה את מה שמגיע אחריה. כאן הופכים משפט לצירוף שמני.','the battery is dead  →  <u>the dead battery</u>',family='cause')
explain('שלב 2 · בודקים את ההמשך','שימו לב להבדל בין שתי התבניות.','<b>because</b> the battery <u>is</u> dead<br><b>because of</b> <u>the dead battery</u>',family='cause')
teach('cause','Due to','My phone is off <b>due to</b> <u>the dead battery</u>.','הטלפון שלי כבוי עקב הסוללה הריקה.','עקב / בגלל',C)
teach('cause','As a result of','My phone is off <b>as a result of</b> <u>the dead battery</u>.','הטלפון שלי כבוי כתוצאה מהסוללה הריקה.','כתוצאה מ־',C)
practice('cause','החליפו את because ב־Due to. התאימו גם את ההמשך.','We stay home because it is raining.','We stay home <b>due to</b> <u>the rain</u>.','אנחנו נשארים בבית עקב הגשם.','it is raining הפך לצירוף השמני the rain.')
recap('סיכום ביניים · שתי תבניות לסיבה','cause',[
 ['because / since','כי / מכיוון ש־','because the battery is dead'],['because of / due to','בגלל / עקב','due to the dead battery'],['as a result of','כתוצאה מ־','as a result of the dead battery']],
 'לא מחליפים רק את מילת הקישור: בודקים אם צריך לשנות גם את הסיבה שאחריה.')
teach('cause','In light of','<b>In light of</b> <u>the dead battery</u><em>,</em> I charge my phone.','לאור הסוללה הריקה, אני מטעין את הטלפון שלי.','לאור / בהתחשב ב־','I charge my phone because the battery is dead.',caption='A reason to act.')
explain('מהמידע להחלטה','In light of מציג מידע שנלקח בחשבון. לכן בדוגמה הזאת מופיעה החלטה לפעול: להטעין את הטלפון.',family='cause')

chapter='תוצאה · כיוון הקשר'
R='The battery is dead, so my phone is off.'
explain('אותם פרטים · כיוון אחר','עד עכשיו הסברנו למה הטלפון כבוי. עכשיו נתחיל בסוללה ונאמר מה נובע מכך.',family='result')
teach('result','So','The battery is dead<em>,</em> <b>so</b> my phone is off.','הסוללה ריקה, ולכן הטלפון שלי כבוי.','לכן / אז')
explain('בודקים את הכיוון','אחרי because באה הסיבה. אחרי so באה התוצאה.','result <b>because</b> reason<br>reason<em>,</em> <b>so</b> result',family='result')
teach('result','Therefore','The battery is dead<em>.</em> <b>Therefore</b><em>,</em> my phone is off.','הסוללה ריקה. לכן, הטלפון שלי כבוי.','לכן',R)
explain('מבנה מוכר · קשר אחר','הפיסוק דומה לזה של However, אבל כאן הרעיון השני הוא תוצאה ולא ניגוד.','A<em>.</em> <b>Therefore</b><em>,</em> B.',family='result')
teach('result','As a result','The battery is dead<em>.</em> <b>As a result</b><em>,</em> my phone is off.','הסוללה ריקה. כתוצאה מכך, הטלפון שלי כבוי.','כתוצאה מכך',R)
explain('מילה קטנה משנה את המבנה','עם of מציגים את הסיבה בצירוף שמני. בלי of עוברים לתוצאה במשפט חדש.','<b>As a result of</b> the dead battery, …<br>The battery is dead. <b>As a result</b>, …',family='result')
practice('result','חברו בעזרת Therefore. התחילו בסיבה.','It is raining. We stay home.','It is raining<em>.</em> <b>Therefore</b><em>,</em> we stay home.','יורד גשם. לכן, אנחנו נשארים בבית.','קודם הסיבה, אחר כך התוצאה; פסיק אחרי Therefore.')
recap('סיכום ביניים · סיבה ותוצאה','result',[
 ['because','כי','We stay home because it is raining.'],['so','לכן','It is raining, so we stay home.'],['therefore / as a result','לכן / כתוצאה מכך','It is raining. Therefore, we stay home.']],
 'העובדות נשארות זהות. בודקים מאיזה רעיון מתחילים ולאן מילת הקישור מובילה.')

chapter='הדגמה · מהכלל לפרט'
explain('מוסיפים דוגמה','נציג רעיון כללי, ואז פרט שממחיש אותו. דוגמה היא מקרה אחד שמתאים לרעיון הכללי.',family='example')
teach('example','For example','I enjoy sports<em>.</em> <b>For example</b><em>,</em> I play football.','אני אוהב ספורט. למשל, אני משחק כדורגל.','למשל / לדוגמה','I enjoy sports. I play football.',caption='One clear example.')
explain('דוגמה בתוך משפט שלם','בדגם הזה הדוגמה היא משפט עם נושא ופועל.','A<em>.</em> <b>For example</b><em>,</em> B.',family='example')
teach('example','Such as','I enjoy sports <b>such as</b> <u>football</u>.','אני אוהב ענפי ספורט כגון כדורגל.','כגון','I enjoy sports. For example, I play football.')
explain('דוגמה בתוך צירוף','אחרי such as מופיע כאן שם של ענף ספורט. לא מעתיקים את כל המשפט I play football.','sports <b>such as</b> <u>football</u>',family='example')
practice('example','חברו למשפט אחד בעזרת Such as.','I like fruit. For example, I like apples.','I like fruit <b>such as</b> <u>apples</u>.','אני אוהב פירות כגון תפוחים.','אחרי such as בא כאן שם עצם: apples.')
recap('סיכום ביניים · שתי דרכים להדגים','example',[
 ['for example','לדוגמה','For example, I play football.'],['such as','כגון','sports such as football']],
 'הדוגמה נשארת קשורה לאותה קבוצה כללית; המבנה משתנה.')

chapter='סדר ותכלית · בונים רצף'
explain('מסדרים פעולות ברצף','נתאר הכנה למשימה: קוראים, מתכננים, ואז כותבים.',family='sequence')
teach('sequence','First','<b>First</b><em>,</em> I read the question.','תחילה, אני קורא את השאלה.','תחילה / ראשית',tense='הווה')
teach('sequence','Then','<b>Then</b><em>,</em> I plan my answer.','לאחר מכן, אני מתכנן את התשובה שלי.','לאחר מכן',caption='The next step.')
teach('sequence','Finally','<b>Finally</b><em>,</em> I write my answer.','לבסוף, אני כותב את התשובה שלי.','לבסוף',caption='Ready to write.')
recap('סיכום ביניים · שלושה שלבים','sequence',[
 ['first','תחילה','First, I read the question.'],['then','לאחר מכן','Then, I plan my answer.'],['finally','לבסוף','Finally, I write my answer.']],
 'בחרו פעולה אחרת בכל שלב. סדר הפעולות צריך להיות הגיוני.')
explain('לא רק למה · גם לשם מה','נסיים בשתי דרכים להציג מטרה: מה רוצים להשיג באמצעות הפעולה?',family='purpose')
teach('purpose','To','I charge my phone <b>to</b> <u>call</u> Dan.','אני מטעין את הטלפון כדי להתקשר לדן.','כדי','I charge my phone. I want to call Dan.')
explain('אותו מבצע · פעולה ומטרה','במבנה הזה to מציג מטרה ואחריו הפועל בצורת הבסיס.','I charge my phone <b>to</b> <u>call</u> Dan.',family='purpose')
teach('purpose','So that','I charge my phone <b>so that</b> I can call Dan.','אני מטעין את הטלפון כדי שאוכל להתקשר לדן.','כדי ש־','I charge my phone to call Dan.')
explain('אחרי So that · נושא ופועל','כאן ממשיכים עם I can call. אל תבלבלו בין so שמציג תוצאה לבין so that שמציג כאן מטרה.','<b>to</b> call Dan  →  <b>so that</b> I can call Dan',family='purpose')
practice('purpose','החליפו את to ב־so that והשלימו את המבנה.','I save money to buy a bike.','I save money <b>so that</b> I can buy a bike.','אני חוסך כסף כדי שאוכל לקנות אופניים.','to buy הפך ל־so that I can buy.')

chapter='תרגול מסכם'
explain('עכשיו אתם בוחרים','קודם קובעים את הקשר. אחר כך בוחרים ביטוי ובודקים מבנה ופיסוק.')
practice('contrast','השלימו: However / Therefore / In addition.','The game is difficult. ____, I enjoy it.','The game is difficult<em>.</em> <b>However</b><em>,</em> I enjoy it.','המשחק קשה. עם זאת, אני נהנה ממנו.','יש ניגוד בין הקושי לבין ההנאה.')
practice('cause','תקנו את המבנה. אפשר לשנות את הביטוי או את המשכו.','We stay home because of it is raining.','We stay home <b>because of</b> <u>the rain</u>.','אנחנו נשארים בבית בגלל הגשם.','אפשר גם: We stay home because it is raining.')
practice('contrast','תקנו את החיבור הכפול. שמרו על Although.','Although Dan is tired, but he studies.','<b>Although</b> Dan is tired<em>,</em> he studies.','אף שדן עייף, הוא לומד.','מסירים את but; Although כבר מבצע את החיבור.')
practice('result','החליפו את so ב־Therefore.','The bus is late, so we wait.','The bus is late<em>.</em> <b>Therefore</b><em>,</em> we wait.','האוטובוס מאחר. לכן, אנחנו מחכים.','שומרים על הסיבה ועל התוצאה ומשנים את הפיסוק.')
explain('מחברים לפסקה · בוחרים קשרים','חברו את שלושת המשפטים. הוסיפו מילת קישור מתאימה לפני המשפט השני ולפני השלישי.','The app is useful.<br>It has stories.<br>Some games are difficult.')
example('addition','One possible answer','The app is useful. <b>In addition</b>, it has stories. <b>However</b>, some games are difficult.','האפליקציה שימושית. בנוסף, יש בה סיפורים. עם זאת, חלק מהמשחקים קשים.','',tense='הווה')
explain('בודקים את הבחירה','הסיפורים הם יתרון נוסף. הקושי במשחקים מוצג כהסתייגות. אפשר לבחור חלופות אחרות ששומרות על הקשרים האלה.')
recap('סיכום · בוחרים לפי הקשר','',[
 ['but / however','ניגוד','A, but B.'],['and / in addition','תוספת','A. In addition, B.'],['because / therefore','סיבה / תוצאה','A because B. / A. Therefore, B.']],
 'עוד קשרים שלמדנו: הדגמה, סדר פעולות ומטרה.')
explain('משימת סיום','כתבו ארבעה משפטים על אפליקציה, משחק או פעילות. שלבו תוספת, ניגוד וסיבה או תוצאה. סמנו את מילות הקישור שבחרתם.')
explain('בדיקה עצמית לפני שמסיימים','האם הקשר מתאים? האם ההמשך בנוי נכון? האם הפיסוק תקין? קראו את המשפט בקול ובדקו שהוא אומר את מה שהתכוונתם.')

# Files and all entry points share the same lesson, without pupil-facing grade labels.
(OUT/'lesson.json').write_text(json.dumps(S,ensure_ascii=False,indent=2)+'\n')
shell='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#050b14"><title>Connectors</title><link rel="stylesheet" href="../../grade9/connectors/lesson.css?v=20260916-reveal"><script defer src="../../grade9/connectors/lesson.js?v=20260916-reveal"></script></head><body><a class="home" href="../../#gradeGRADE" aria-label="חזרה לדף הכיתה" title="חזרה לדף הכיתה">⌂</a><button class="full" id="full" aria-label="מסך מלא" title="מסך מלא"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5" fill="none" stroke="currentColor" stroke-width="2"/></svg></button><main id="deck" aria-live="polite"></main><nav class="controls" aria-label="ניווט בשקפים" dir="ltr"><button id="prev" aria-label="השקף הקודם">←</button><select id="jump" aria-label="מעבר לשקף"></select><button id="next" aria-label="השקף הבא">→</button></nav><div class="progress"><i id="progress"></i></div><noscript>יש להפעיל JavaScript כדי להציג את המצגת.</noscript></body></html>'''
for grade in (9,10,11):
    (ROOT/f'grade{grade}/connectors/index.html').write_text(shell.replace('GRADE',str(grade)))
js=(ROOT/'tools/connectors/player.js').read_text()
(OUT/'lesson.js').write_text('const slides = '+json.dumps(S,ensure_ascii=False)+';\n'+js)
starts={}
for i,s in enumerate(S,1): starts.setdefault(s['chapter'],i)
notes='''# Connectors — תסריט למורה

מצגת אחת משותפת, ללא שיוך לשכבת גיל על גבי השקפים. שלוש הכניסות הקיימות מפעילות אותו תוכן.

## אופן ההפעלה

- כל זוג חשיפה מציג את אותו שקף בדיוק. בשקף השני מתווסף התרגום בלבד; כל המיקומים נשמרים.
- לפני החשיפה: קראו, בקשו פירוש מההקשר, המתינו, ורק אז התקדמו. הוראות ותרגום הם שדות נפרדים.
- בתרגול יש שלושה שלבים: שאלה; תשובה באנגלית; אותו שקף תשובה בתוספת תרגום. ההסבר מתגלה עם התשובה.
- שקפי ההסבר מפורקים לפעולה אחת. אחרי כמה ביטויים יש תרגול וסיכום ביניים.
- שקפי התמונות נשמרו בין מילות הקישור. הכיתוב קצר באנגלית בלבד; התמונות חוזרות כדי לשמר את האסוציאציות המקוריות.
- זו יחידת לימוד למספר מפגשים. בחרו את נקודת העצירה לפי קצב הכיתה, ללא הצגת תווית רמה לתלמידים.
- תפריט המעבר כולל את הפרקים ואת מספרי השקפים. Home / End עוברים להתחלה ולסוף; חצים, גלילה והחלקה מעבירים צעד אחד.

## דגשים פדגוגיים

- לא מציגים ביטויים כמילים נרדפות שאפשר להחליף בלי לשנות דבר. משווים קשר לוגי, מבנה ומשלב.
- However / Therefore / In addition מתורגלים כאן בתחילת משפט חדש עם פסיק. זהו דגם להקניה, לא רשימה ממצה של כל מיקומיהם האפשריים.
- Although / Even though דורשים פסוקית; Despite מתורגל עם צירוף שמני. אפשר גם ing; קיימים מבנים מורכבים נוספים שלא נדרשים כאן.
- On the contrary מתקן טענה או רושם ומציג את ההפך, ולכן מקבל דוגמה נפרדת.
- Also בדרך כלל לפני הפועל העיקרי ואחרי be; Too מתורגל בסוף.
- Moreover / Furthermore מוסיפים נימוק מחזק; בהסבר קושרים את הדוגמה להמלצה על האפליקציה.
- Because / Since / Given that מקדימים פסוקית. Since עשוי לציין זמן בהקשרים אחרים.
- Because of / Due to / As a result of מקדימים כאן צירוף שמני. In light of מציג מידע שנלקח בחשבון בהחלטה.
- So / Therefore / As a result מציגים תוצאה. As a result of מציג את הסיבה.
- For example מתורגל עם משפט שלם; Such as עם שם עצם. To מציג כאן מטרה, ו־So that בא לפני פסוקית.
- Then יכול להופיע גם ללא פסיק; הפסיק בדוגמה מסייע להראות את פתיחת שלב הרצף.
- בתרגילי כתיבה פתוחים, קבלו חלופות שמביעות את הקשר המתאים ובנויות נכון. הפסקה המסכמת היא אפשרות אחת.

## פרקים

'''
notes+='\n'.join(f'- שקף {i}: {name}' for name,i in starts.items())
notes+='\n\n## מקורות עזר לשימוש\n\n- https://dictionary.cambridge.org/grammar/british-grammar/word-choice-on-the-contrary-or-by-in-contrast\n- https://dictionary.cambridge.org/us/dictionary/english/as-a-result-of\n- https://dictionary.cambridge.org/dictionary/english/in-the-light-of\n- https://www.collinsdictionary.com/us/dictionary/english/not-to-mention\n\nמשפטי הדוגמה מקוריים. נשמרו כל הביטויים מהמצגת המקורית, ונוספו ביטויים להקניה מדורגת.\n'
notes+=f'\n{len(S)} שקפים; {len(connectors)} מילות קישור וביטויים; {sum(s["kind"]=="summary" and s.get("reveal") for s in S)} סיכומים; {sum(s["kind"]=="practice" and not s.get("answerVisible") for s in S)} תרגילים מדורגים.\n'
(OUT/'teacher.md').write_text(notes)
print(json.dumps({'slides':len(S),'connectors':len(connectors),'idea_slides':sum(s['kind']=='idea' for s in S),'translation_pairs':sum(s.get('reveal') is True for s in S),'chapters':starts},ensure_ascii=False))
