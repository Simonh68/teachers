from pathlib import Path
import json, html, re, shutil

ROOT=Path(__file__).resolve().parents[2]
(ROOT/'tools/grammar-in-an-essay/build').mkdir(parents=True,exist_ok=True)
OUT=ROOT/'grade11/grammar-in-an-essay'
E=html.escape
S=[]
SOURCE='https://meyda.education.gov.il/sheeloney_bagrut/pitronot_bagrut/2026/6/016582-8-HEB-1400-1600.pdf'
TOPIC = 'Should every student have a chance to take part in class sports games, regardless of ability?'
SENTENCES = [
'School sports often raise questions about ability and participation in class games.',
'I claim that every student should have a chance to participate, regardless of ability.',
'On the one hand, including beginners may reduce a team’s chances of winning competitive matches.',
'If teams include inexperienced players, they will sometimes lose matches because of simple mistakes.',
'On the other hand, playing together can improve confidence and develop useful social skills.',
'Some students have felt excluded, so joining a team can be especially beneficial.',
'In conclusion, participation has significant educational value despite the challenges it creates.',
'Therefore, class games should be organized fairly to give everyone a meaningful role.',
'For example, repeated mistakes can frustrate teammates who hope to win.',
'Moreover, sharing responsibility can assist quieter classmates and build friendships.'
]
# Sentence numbers are drafting steps. Steps 9 and 10 expand the body,
# so the final reading order is 1,2 / 3,4,9 / 5,6,10 / 7,8.
PARAGRAPH_STEPS = [[0,1],[2,3,8],[4,5,9],[6,7]]
P = [' '.join(SENTENCES[i] for i in ids) for ids in PARAGRAPH_STEPS]
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

add('cover','ברוכים הבאים','כיתה י״א · 5 יח״ל','ישיבת בני עקיבא קריית הרצוג','שיעור המשך לאחר השלמת Advanced Grammar. כעת מיישמים בכתיבה.')
info('Advanced Grammar in an Essay','נבנה חיבור דעה שלם, צעד אחר צעד.','A clear opinion. Developed reasons. Accurate language.','הסבירו: כל מבנה נכנס לחיבור משום שהוא מועיל לרעיון. אין צורך לדחוס את כל המבנים לכל משפט.')
info('The writing task','כתבו את דעתכם ותמכו בה בנימוקים ובדוגמאות.','Should every student have a chance to take part in class sports games, even if they are not good at sports?','נושא תרגול מקורי. אין כאן התחייבות לשאלה שתופיע במבחן.')
info('מסגרת התרגול','120–140 מילים. היום נתאמן בארבע פסקאות.','Introduction / Reason 1 / Reason 2 / Conclusion','האורך תואם למשימות G שפורסמו ב־2026. ארבע פסקאות הן מסגרת ההוראה שנבחרה לשיעור; יש לקרוא תמיד את הוראות המשימה בפועל.',source=SOURCE)
info('מה בדיוק מבקשים?','עמדה על שיתוף במשחקי הכיתה, גם כשהיכולת שונה.','Our focus: participation in class games.','הבחינו בין השתתפות במשחק כיתתי לבין בחירת נבחרת תחרותית. הימנעו מחיבור כללי על יתרונות הספורט.')
timer('תכנון קצר','Write your opinion and two different reasons.',90,'רק שלוש הערות קצרות. עדיין לא כותבים חיבור.','תנו 90 שניות. בקשו מתלמיד אחד להסביר מה ההבדל בין שני הנימוקים.',section='plan')
info('תוכנית לדוגמה','עמדה: לשתף את כולם. נימוק ראשון: חברות. נימוק שני: ביטחון עצמי.','Include everyone. Build friendships. Improve confidence.','זו תוכנית אפשרית. אפשר לבחור עמדה אחרת ולנמק אותה היטב.')
anim(1,'plan')
info('עמדה במשפט ברור','נושא, פועל והמשך שמביעים עמדה.','Every student should have a chance to join class games.','התחילו במשפט נקי. אין צורך לפתוח בקלישאה כללית כגון Nowadays everything is important.',section='intro')
pair('פסקת פתיחה',P[0],'יש תלמידים שנהנים מספורט בבית הספר, ואחרים חוששים לטעות. לדעתי, לכל תלמיד צריכה להיות הזדמנות להשתתף במשחקי הכיתה, בלי קשר ליכולת.','הפתיחה מציגה את הנושא ואת העמדה. while מציג ניגוד בתוך המשפט הראשון.',section='intro',highlights=['while','In my opinion'])
choice('עמדה ממוקדת','Which sentence directly answers the task?',['Sport is very popular around the world.','Every classmate should have a chance to join the game.','There are many different kinds of sports.'],1,'האפשרות השנייה עונה לשאלה על שיתוף תלמידים במשחק. משפט כללי על ספורט אינו מספיק.',section='intro')
anim(2,'intro')
info('פסקת נימוק','כל פסקת גוף מפתחת רעיון אחד: נימוק, הסבר ואז דוגמה.','Reason + explanation + example','אין חובה שכל פסקה תהיה באותו אורך. הדוגמה חייבת להראות איך הנימוק פועל.',section='gerund')
pair('Gerund כנושא המשפט','Playing together helps students build friendships.','משחק משותף עוזר לתלמידים ליצור חברויות.','Playing together היא הפעילות שעליה מדברים. כל הצירוף משמש נושא יחיד, ולכן helps.',section='gerund',tense='הווה',highlights=['Playing together','helps'])
info('שם של פעילות','Gerund הוא פועל עם ing שמתפקד כשם עצם. כאן הוא נושא המשפט.','Playing together helps students.','הבחינו בין Playing helps לבין They are playing. בשני יש פעולה בזמן מתמשך; בשיעור משתמשים בפעילות כשם עצם.',section='gerund')
gap('Gerund והסכמה עם הפועל','',' together helps students build friendships.',['Play','Playing','Played'],1,'Playing together משמש נושא יחיד. לכן נכתוב helps.','התלמידים אומרים אות ומסבירים לפני החשיפה.',section='gerund',tense='הווה')
gap('אחרי מילת יחס','Students learn teamwork by ',' together.',['work','worked','working'],2,'אחרי מילת היחס by משתמשים ב־gerund: by working.','הדגישו: מבנה נוסף שאפשר להשתמש בו לפי הצורך, ולא תוספת חובה לחיבור שלנו.',section='gerund',tense='הווה')
info('נימוק עם הסבר','הנימוק מציג חברות. ההסבר מראה מה התלמידים עושים יחד.','First, playing together helps students build friendships. When classmates support one another, they learn to work as a team.','שאלו: האם המשפט השני מוסיף מידע, או רק חוזר על הראשון?',section='gerund')
anim(3,'gerund')
gap('סיבה','Students feel included ',' their classmates pass them the ball.',['therefore','because','however'],1,'Because מחבר סיבה למשפט. אחריו מופיע משפט עם נושא ופועל.',section='connectors',tense='הווה')
gap('תוצאה','Classmates encourage beginners. ', ', beginners feel more confident.',['However','For example','Therefore'],2,'Therefore מציג תוצאה. כאן הוא פותח משפט חדש ואחריו פסיק.',section='connectors',tense='הווה')
gap('ניגוד','Winning is exciting. ', ', participation also matters.',['However','Because','For example'],0,'However מציג ניגוד או הסתייגות. הוא אינו מציג סיבה.',section='connectors',tense='הווה')
info('מילות קישור ומשמעות','בחרו קשר שמתאים לרעיון, ושמרו על פיסוק מתאים.','because + reason\nFor example, + example\nHowever, + contrast\nTherefore, + result','דוגמאות הפיסוק כאן מראות דרך בטוחה לתלמידים: However ו־Therefore בתחילת משפט חדש. קיימים גם מבנים תקינים נוספים.',section='connectors')
anim(4,'connectors')
info('פסקת הגוף הראשונה','נימוק, הסבר ודוגמה שממחישה שיתוף. ',P[1],'קראו את הפסקה כמכלול. First מסמן נימוק ראשון; For example מציג את הדוגמה. playing ו־passing משמשים gerunds.',section='connectors',highlights=['First','playing together','For example','passing the ball'])
pair('Active: מי עושה את הפעולה?','Teachers should organize games fairly.','המורים צריכים לארגן את המשחקים בהוגנות.','משפט פעיל. המוקד הוא במורים שמארגנים.',section='passive',highlights=['Teachers','should organize'])
pair('Passive: המוקד במשחקים','Games should be organized fairly.','המשחקים צריכים להיות מאורגנים בהוגנות.','המשמעות נשמרת. שינינו את מוקד המשפט למשחקים. אין צורך ב־by teachers כשהמבצע מובן מההקשר.',section='passive',highlights=['Games','should be organized'])
info('מבנה הסביל אחרי should','הנושא מקבל את הפעולה. אחרי should מוסיפים be ואת צורת V3.','subject + should + be + V3','למשל: games should be organized; every student should be included. המילה should אינה משתנה לפי הנושא.',section='passive')
gap('השלמת Passive','Games should ',' so that everyone can take part.',['be organized','organize','be organizing'],0,'should be organized הוא מבנה סביל תקין: should + be + V3.',section='passive')
choice('איזה משפט תקין?','The focus is on including every student.',['Every student should included.','Every student should be included.','Every student should be include.'],1,'צריך גם be וגם V3: should be included. אין להשמיט אחד מהם.',section='passive')
anim(5,'passive')
info('Present Perfect והקשר להווה','מתארים ניסיון או מצב מן העבר שיש לו משמעות עכשיו.','Some students have felt excluded from games.','הרגשת ההדרה מהעבר מסבירה למה צריך לפעול כעת. לא מציינים כאן זמן עבר מסוים כגון yesterday.',section='perfect')
pair('ניסיון קודם, משמעות עכשיו','Some students have felt excluded from games.','יש תלמידים שהרגישו מודרים ממשחקים.','זהו ניסיון קודם שרלוונטי לטיעון בהווה. הפועל feel מופיע בצורת V3: felt.',section='perfect',highlights=['have felt'])
info('מבנה Present Perfect','עם I / you / we / they משתמשים ב־have. עם he / she / it משתמשים ב־has.','have / has + V3','אל תוסיפו תווית הווה/עבר בודדת למשפט הזה: המבנה מחבר ניסיון קודם להווה.',section='perfect')
gap('צורת V3','Some students have ',' excluded from games.',['feel','feeling','felt'],2,'V3 של feel הוא felt. לכן: have felt.',section='perfect')
choice('זמן עבר מוגדר','Which sentence fits the time expression yesterday?',['Yesterday, Tom has felt left out.','Yesterday, Tom felt left out.','Yesterday, Tom have felt left out.'],1,'Yesterday מציין זמן עבר שהסתיים. כאן משתמשים ב־Past Simple: felt.',section='perfect')
anim(6,'perfect')
info('Second Conditional','מדמיינים שינוי במצב ומסבירים מה הייתה התוצאה שלו.','More encouragement could change how students feel.','זו דרך לפתח טיעון, לא רק להדגים נוסחה דקדוקית.',section='conditionals')
info('מבנה תנאי שני','בחלק של if משתמשים ב־Past Simple. בחלק השני: would והפועל הבסיסי.','If + Past Simple, would + base verb','צורת העבר מסמנת כאן מצב היפותטי בהווה או בעתיד, ולא אירוע שהתרחש בעבר. לכן אין תווית עבר צהובה.',section='conditionals')
pair('השינוי והתוצאה','If they received more encouragement, they would feel safer trying again.','אם הם היו מקבלים יותר עידוד, הם היו מרגישים בטוחים יותר לנסות שוב.','they מתייחס לתלמידים שהרגישו מודרים. תנו לתלמידים לזהות את השינוי ואת התוצאה לפני התרגום.',section='conditionals',highlights=['If','received','would feel'])
gap('תוצאה היפותטית','If they received more encouragement, they ',' safer trying again.',['will feel','would feel','felt'],1,'עם If + Past Simple משתמשים כאן ב־would + base verb. הכוונה לתוצאה היפותטית.',section='conditionals')
info('First Conditional','מתארים אפשרות ממשית בעתיד ואת התוצאה הצפויה שלה.','If we include every classmate tomorrow, more students will enjoy the game.','זהו משפט חלופי למסר עתידי. לא חייבים להכניס לחיבור גם תנאי ראשון וגם תנאי שני.',section='conditionals',tense='עתיד')
gap('אפשרות ממשית בעתיד','If we include every classmate tomorrow, more students ',' the game.',['would enjoy','will enjoy','enjoyed'],1,'First Conditional: בחלק של if יש Present Simple; בחלק התוצאה will + base verb.',section='conditionals',tense='עתיד')
anim(7,'conditionals')
info('בחירת סוג התנאי','תנאי ראשון: תוצאה צפויה של אפשרות ממשית. תנאי שני: תוצאה של מצב היפותטי.','If we include them, they will enjoy the game.\nIf they received more encouragement, they would feel safer.','בפסקת הדוגמה נבחר בתנאי השני כדי לדמיין שינוי. שימוש מדויק אחד מועיל יותר מרשימת מבנים.',section='conditionals')
info('פסקת הגוף השנייה','הנימוק הוא ביטחון עצמי. שאר המשפטים מפתחים אותו.',P[2],'הקריאו ברצף. Some students מציג ניסיון קודם; If מראה שינוי אפשרי; Therefore מציג מסקנה מעשית: לארגן את המשחק כך שכולם יוכלו להשתתף.',section='body2',highlights=['Moreover','have felt','If','would feel','Therefore','should be organized'])
info('לכל מבנה יש תפקיד','Perfect: ניסיון קודם. Conditional: שינוי אפשרי. Passive: ארגון המשחקים.','experience / imagined change / focus on the action','אין צורך להוסיף שמות מבנים בתוך החיבור המוגש. בתרגול נסמן אותם אחרי שהכתיבה הושלמה.',section='body2')
choice('Although בחיבור','Which sentence connects the ideas correctly?',['Although winning is exciting, but learning to support others matters more.','Although winning is exciting, learning to support others matters more.','Although winning is exciting, so learning to support others matters more.'],1,'Although כבר מציג ניגוד. לא מוסיפים but או so באותו מבנה.',section='conclusion')
pair('פסקת סיום',P[3],'לסיכום, על בתי הספר להעריך השתתפות לצד הישגים. אף שניצחון מרגש, למידה לתמוך באחרים חשובה יותר. לכן, על המורים לעודד שיתוף של כל חבר לכיתה.','הסיום חוזר לעמדה ומסיק מסקנה. אין לפתוח בו נימוק חדש שלא פותח קודם.',section='conclusion',highlights=['In conclusion','Although','Therefore'])
anim(8,'conclusion')
add('essay','החיבור השלם','\n\n'.join(P),f'{WC} מילים · ארבע פסקאות','קראו את החיבור ברצף לפני שמסמנים מבנים. שאלו אם העמדה נשארת עקבית.',section='essay',paragraphs=P,source=SOURCE)
info('הפתיחה מחזיקה את העמדה','הנושא מוצג, ויש תשובה ברורה לשאלה.',P[0],'שאלו: איזה משפט מבטא את העמדה? זהו שיתוף קצר ולא בוחן.',section='essay',highlights=['In my opinion','every student should have a chance'])
info('הנימוק הראשון מתפתח','חברות, עבודת צוות ודוגמה מהמשחק.',P[1],'הצביעו על המעבר מטענה כללית לפעולה ממשית: מסירה לתלמיד מתחיל.',section='essay',highlights=['playing together','For example','passing the ball'])
info('הנימוק השני מתפתח','ניסיון קודם, שינוי אפשרי והתארגנות מעשית.',P[2],'זהו אותו טקסט. כעת הצבע מדגיש את תרומת המבנים לטיעון.',section='essay',highlights=['have felt','received','would feel','should be organized'])
info('הסיום סוגר את הטיעון','מסקנה שנובעת משני הנימוקים.',P[3],'Although משלב רעיון מנוגד, אבל העמדה המקורית נשמרת.',section='essay',highlights=['In conclusion','Although','Therefore'])
anim(9,'essay')
timer('העברה לנושא חדש','Should students work with different partners in class?',120,'תכננו עמדה ושני נימוקים. אפשר לבחור חברות וביטחון, או רעיונות אחרים.','התלמידים מיישמים את אותה דרך כתיבה על נושא קרוב אך חדש. אל תציגו עדיין את תשובת הדוגמה.',section='practice')
info('תוכנית אפשרית','עמדה: כדאי להחליף שותפים. נימוק אחד: ללמוד מאנשים שונים. נימוק שני: להכיר תלמידים חדשים.','Changing partners can help students learn from one another.','אפשר לקבל גם התנגדות מנומקת, למשל חשש מתחלופה מהירה מדי. העמדה אינה חלק מהציון.',section='practice')
timer('משפט אחד משודרג','Write one sentence using a structure that supports your reason.',90,'בחרו gerund, passive, perfect או conditional.','תנו לכל תלמיד לבחור מבנה שהוא מבין. בקשו משפט עם משמעות ברורה, לא דוגמה מנותקת.',section='practice')
pair('דוגמה אפשרית','Working with different classmates can help students discover new ideas.','עבודה עם תלמידים שונים יכולה לעזור לגלות רעיונות חדשים.','הדוגמה משתמשת ב־gerund. משפט תקין עם מבנה אחר מתקבל באותה מידה.',section='practice',highlights=['Working with different classmates'])
anim(10,'practice')
choice('עריכה: נושא ופועל','Which sentence is correct?',['Playing together help students.','Playing together helps students.','Playing together helping students.'],1,'הצירוף Playing together הוא נושא יחיד; הפועל הוא helps.',section='edit')
choice('עריכה: משפט תנאי','Which sentence correctly describes an imaginary change?',['If students received support, they would try again.','If students would receive support, they tried again.','If students received support, they will tried again.'],0,'If + Past Simple, would + base verb. קראו גם את המשמעות ולא רק את הנוסחה.',section='edit')
info('בדיקת חיבור','האם עניתי למשימה? האם לכל נימוק יש הסבר? האם הדוגמאות קשורות אליו?','Task / clear paragraphs / developed ideas','בסבב הראשון בודקים תוכן וארגון. רק אחר כך בודקים דקדוק ומכניקה.',section='edit')
info('בדיקת שפה','בדקו נושא ופועל, V3, מילות קישור, אות גדולה ופיסוק.','Check meaning first. Then check form.','בכיתה אפשר להדגיש את המבנים לצורך משוב. הסימון ושמות המבנים אינם חלק מהחיבור עצמו.',section='edit')
anim(11,'edit')
timer('כתיבה עצמאית','Write 120–140 words about working with different partners in class.',720,'ארבע פסקאות. דעה, שני נימוקים מפותחים וסיום.','12 דקות כתיבה אחרי התכנון שכבר נעשה. יעד התרגול הכיתתי: ארבעה מבנים שונים שנלמדו, במקומות המתאימים למשמעות. תנו תמיכה נקודתית בלי לכתוב במקום התלמידים.',section='write')
timer('בדיקה עצמית','Read your essay and improve two things.',120,'בדיקה אחת של התוכן ובדיקה אחת של השפה.','השעון אינו מעביר שקף אוטומטית. אפשר להאריך זמן לפי קצב הכיתה.',section='write')
info('סימון לצורך משוב','היעד הכיתתי: ארבעה מבנים מתאימים. סמנו אותם והקיפו את מילות הקישור.','gerund / passive / perfect / conditional','זהו כלי כיתתי לבדיקה. אין להציג מספר מסוים של מבנים או ספירה כפולה של Although ככלל ניקוד רשמי.',section='write')
anim(12,'write')
choice('כרטיס יציאה','Which improvement makes the essay stronger?',['Adding a difficult structure to every sentence.','Using clear reasons and grammar that fits the meaning.','Writing as many connectors as possible.'],1,'החיבור מתחזק כשהטיעון ברור והשפה מדויקת ומתאימה למשמעות.',section='end')
info('להמשך התרגול','סיימו את החיבור, תקנו אותו ושמרו את שתי הגרסאות להשוואה.','One clear opinion. Two developed reasons. A relevant conclusion.','בקשו להביא גם את הטיוטה. בהמשך בוחרים פסקה אחת למשוב ומפתחים אותה, בלי לעבור על כל שגיאה במליאה.',section='end')

# September 2026 revision: the requested for-and-against structure.
def edit(n, **fields):
    S[n-1].update(fields)
edit(2, text='A for-and-against essay with a clear opinion.', he='ארבע פסקאות: פתיחה ודעה, טענה נגדית, חזרה לעמדה וסיכום.')
edit(3, text=TOPIC, he='הציגו את עמדתכם, בחנו טענה נגדית וחזרו לתמוך בעמדה שלכם.')
edit(4, text='Introduction\nOn the one hand, ...\nOn the other hand, ...\nIn conclusion, ...', he='120–140 מילים. בדיוק ארבע פסקאות. ההרחבות נכנסות לפסקאות הגוף.', note='פסקה 1: משפטים 1–2. פסקה 2: 3–4 והרחבה 9. פסקה 3: 5–6 והרחבה 10. פסקה 4: 7–8. המספרים מציינים שלבי כתיבה, לא סדר סופי.')
edit(6, text='Plan your opinion, an opposing idea and a supporting idea.', he='קודם העמדה שלכם. אחר כך חשבו על טענה נגדה ועל תשובה שתומכת בה.', note='תנו זמן לתכנון. בקשו טענה נגדית אמיתית, לא נימוק נוסף לאותה עמדה.')
edit(7, text='Include everyone.\nAgainst: fewer chances to win.\nFor: confidence and social skills.', he='העמדה: לשתף את כולם. נגד: פגיעה בתחרותיות. בעד: ביטחון וכישורים חברתיים.', note='במודל שלנו פסקת On the one hand מתנגדת לעמדה. פסקת On the other hand חוזרת לתמוך בה.')
edit(9, text='Opening: introduce the issue.\nOpinion: I claim that ...', he='משפט 1 מציג את הנושא בלי דעה. משפט 2 מביע דעה וכולל I claim that.', note='בקשו שני משפטים נפרדים. אל תכניסו עמדה במשפט הראשון.', highlights=['I claim that'])
for n in [10,11]:
    edit(n, text=P[0], highlights=['I claim that'], note='משפט פתיחה ניטרלי ואחריו דעה מפורשת. מתקנים רק מה שנחוץ ושומרים על הרעיון של התלמיד.')
edit(11, he='ספורט בבית הספר מעורר שאלות על יכולת והשתתפות במשחקי הכיתה. אני טוען שלכל תלמיד צריכה להיות הזדמנות להשתתף, בלי קשר ליכולת.')
for n in [12,13]:
    edit(n, options=['Sport is very popular around the world.', SENTENCES[1], 'There are many different kinds of sports.'])
edit(13, he='האפשרות השנייה מביעה עמדה שעונה למשימה וכוללת I claim that.')
edit(15, title='פיתוח פסקאות הגוף', text='Opposing idea + consequence\nSupporting idea + experience', he='פסקה 2 מפתחת את הטענה הנגדית. פסקה 3 חוזרת לעמדה שלנו ותומכת בה.', note='לפני משפט 3: חשבו הפוך. לפני משפט 5: חזרו לעמדה. תוספת דוגמה בכל פסקת גוף מפתחת את הטיעון.')
edit(23, title='טענה שתומכת בעמדה', text=SENTENCES[4], he='בפסקה השלישית חוזרים לעמדה: משחק משותף מפתח ביטחון וכישורים חברתיים.', note='On the other hand מתחיל את פסקה 3, והוא משיב לטענה הנגדית שבפסקה 2.', highlights=['On the other hand','playing together'])
edit(33, title='פסקה 2: הטענה הנגדית', text=P[1], he='קודם חושבים הפוך: מה המחיר של שיתוף כולם? תנאי ראשון ודוגמה מפתחים את החשש.', note='הפתיח המדויק: On the one hand,. הטענה נגדית לעמדת I claim that. משפט If הוא תנאי ראשון. משפט For example הוא הרחבה 9 בתוך אותה פסקה.', highlights=['On the one hand','If','will','For example'])
edit(54, title='Second Conditional: הרחבה', note='השוואה למבנה שלמדנו בעבר. בחיבור הנוכחי משפט 4 חייב להיות First Conditional.')
edit(63, he='בחיבור שלנו משתמשים בתנאי ראשון במשפט 4. תנאי שני מוצג להשוואה בלבד.', note='בחיבור: If teams include inexperienced players, they will sometimes lose matches because of simple mistakes.')
edit(64, title='פסקה 3: חזרה לעמדה', text=P[2], he='כעת חוזרים לעמדה שלנו: כישורים חברתיים, ניסיון קודם ויתרון נוסף.', note='On the other hand מתחיל פסקה חדשה. משפט 5 תומך בעמדה, משפט 6 משתמש ב־Present Perfect, ומשפט 10 מרחיב בתוך הפסקה.', highlights=['On the other hand','playing together','have felt','Moreover'])
edit(65, text='First Conditional: a possible consequence\nPresent Perfect: relevant experience\nPassive: how games should be organized', he='משפט 4: תנאי ראשון. משפט 6: Present Perfect. משפט 8: סביל.', note='הסדר נקבע לפי ההנחיות. Gerund משתלב באופן טבעי במשפט התמיכה ובהרחבה.')
for n in [68,69]:
    edit(n, text=P[3], highlights=['In conclusion','should be organized'], note='משפט 7 מסכם את העמדה. משפט 8 מוסיף המלצה בסביל. שני המשפטים באותה פסקת סיום.')
edit(69, he='לסיכום, להשתתפות יש ערך חינוכי משמעותי למרות הקשיים שהיא יוצרת. לכן יש לארגן את משחקי הכיתה בהוגנות, כך שלכל אחד יהיה תפקיד בעל משמעות.')
edit(71, title='החיבור השלם: בעד ונגד', text='\n\n'.join(P), paragraphs=P, he=f'{WC} מילים · ארבע פסקאות', note='הנושא: '+TOPIC+'\nסדר הקריאה הסופי: 1,2 / 3,4,9 / 5,6,10 / 7,8. עשרת המספרים מציינים שלבי כתיבה. סופרים מילים בלי הכותרת והנושא.')
edit(72, text=P[0], he='משפט 1 מציג נושא בלי דעה. משפט 2 מביע עמדה באמצעות I claim that.', highlights=['I claim that'], note='בדקו שהפתיחה והדעה הם שני משפטים נפרדים.')
edit(73, title='הטענה הנגדית מתפתחת', text=P[1], he='פסקה 2: טענה נגדית, תנאי ראשון ודוגמה. כל המשפטים מפתחים את אותו חשש.', highlights=['On the one hand','If','will','For example'], note='משפט ההרחבה 9 נכנס אחרי משפט 4 בפסקה השנייה. אין פסקה חמישית.')
edit(74, title='התמיכה בעמדה מתפתחת', text=P[2], he='פסקה 3: חזרה לעמדה, ניסיון קודם והרחבה. כאן מופיע Present Perfect.', highlights=['On the other hand','have felt','Moreover'], note='משפט ההרחבה 10 נכנס אחרי משפט 6 בפסקה השלישית.')
edit(75, text=P[3], he='פסקה 4: מסקנה והמלצה בסביל, בלי נימוק חדש.', highlights=['In conclusion','should be organized'], note='מסקנה שנובעת מהדיון בשני הצדדים וחוזרת לעמדה המקורית.')
edit(77, text='Should teenagers have an after-school job?', he='תכננו עמדה, טענה נגדית ותמיכה בעמדתכם. נשתמש באותו מבנה של ארבע פסקאות.', note='זהו נושא מתוך הרשימה שסיימון מסר. אין לתת חיבור מוכן על נושא התלמיד.')
edit(78, title='תכנון לפני כתיבה', text='I claim that ...\nOn the one hand, ...\nOn the other hand, ...', he='חומר למחשבה: זמן ללימודים, הכנסה וניסיון. בחרו עמדה משלכם.', note='אלה פתיחים ניטרליים. התלמיד קובע את הטענה ואת הרעיונות. הדוגמאות הבאות משתמשות בנושא קבוע אחר: גיל לקבלת טלפון.')
for n in [80,81]:
    edit(n, title='משפט לדוגמה ללמוד ממנו את התבנית', text='Using a cellphone responsibly can assist children in becoming more independent.', highlights=['Using a cellphone'], note='נושא הדוגמה הקבוע: From what age should children have their own cellphone? הנושא של התלמיד הוא Should teenagers have an after-school job? אל תחליפו את נושא הדוגמה בזמן התרגול.')
edit(81, he='שימוש אחראי בטלפון יכול לסייע לילדים להיות עצמאיים יותר. אני מזכיר לך: הנושא שלך הוא עבודה אחרי הלימודים.')
for n in [85,86]:
    edit(n, text='Which sentence uses the first conditional correctly?', options=['If students receive support, they will try again.','If students will receive support, they try again.','If students receive support, they will tried again.'], note='First Conditional: If + Present Simple, will + base verb. בחיבור זהו משפט 4.')
edit(86, he='If + Present Simple, will + base verb. משפט 4 בחיבור מתאר תנאי אפשרי ותוצאה צפויה.')
edit(87, text='Four paragraphs. An opposing idea. A supported opinion.', he='האם פסקה 2 מתחילה ב־On the one hand ופסקה 3 ב־On the other hand? האם חזרתי לעמדה שלי?', note='ודאו שגם הטענה הנגדית מפותחת. סופרים מילים אחרי כל תוספת. אין לסיים מתחת ל־120 מילים.')
edit(88, text='meaningful / significant / central\nbeneficial / useful / practical\nassist / improve', he='בחרו מילה שמתאימה למשמעות. הימנעו מחזרה על אותה מילה ובדקו את הדקדוק.', note='לפי הנחיות התרגול, לא משתמשים ב־good או ב־important. אין צורך לדחוס את כל החלופות לחיבור אחד.')
edit(90, text='Should teenagers have an after-school job?\nWrite 120–140 words.', he='ארבע פסקאות. כתבו משפט אחד בכל פעם: פתיחה, עמדה, נגד, בעד וסיכום.', note='תנו משוב מינימלי אחרי כל משפט. הציגו החיבור עד עכשיו וספירת מילים. משפטים 9–10 נכנסים לגוף, לא לפסקאות חדשות. אין לסיים מתחת ל־120 מילים.')
edit(91, he='ספרו מילים. אם חסרות מילים, הוסיפו הסבר או דוגמה בתוך פסקאות הגוף.', note='הטווח: 120–140. לא מוסיפים פסקה חמישית ולא מסיימים מתחת ל־120. מתקנים תחילה תוכן ואז שפה.')
edit(92, text='I claim that\nFirst Conditional / Present Perfect / Passive', he='בדקו גם Gerund ומילות קישור. המבנים צריכים לשרת את הטיעון.', note='משפט 2: I claim that. משפט 4: תנאי ראשון. משפט 6: Present Perfect. משפט 8: סביל. אלה הוראות התרגול של סיימון.')
edit(96, text='An opinion. An opposing view. A return to your opinion.', he='ארבע פסקאות, 120–140 מילים. ההרחבות נשארות בתוך פסקאות הגוף.', note='סיום רק לאחר שהחיבור עומד באורך ובמבנה. שמרו טיוטה וגרסה מתוקנת להשוואה.')

# Show the drafting order separately from the final reading order.
old_slides = S[:]
S = []
info('מפת המשפטים: פתיחה וגוף', 'מספרי המשפטים מציינים את סדר העבודה.', '1 Opening · 2 I claim that\n3 Opposing idea · 4 First Conditional\n5 Support · 6 Present Perfect', section='essay')
info('מפת המשפטים: סיום והרחבה', 'בסיום עדיין לא מגישים. משלימים את הגוף עד 120–140 מילים.', '7 Conclusion · 8 Passive\n9 Expansion in paragraph 2\n10 Expansion in paragraph 3', section='essay')
roles=['משפט פתיחה בלי דעה','משפט דעה: I claim that','טענה נגדית: חשבו הפוך','תנאי ראשון שמפתח את הטענה הנגדית','תמיכה: חוזרים לעמדה שלנו','ניסיון קודם ב־Present Perfect','מסקנה','המלצה בסביל','הרחבה בתוך פסקה 2','הרחבה בתוך פסקה 3']
for step,role in enumerate(roles,1):
    paras=[' '.join(SENTENCES[i] for i in ids if i<step) for ids in PARAGRAPH_STEPS]
    words=len(' '.join(paras).split())
    add('essay','החיבור עד עכשיו', '\n\n'.join(paras), f'שלב {step}/10 · {words} מילים'+(' · דרושה הרחבה' if step==8 or step==9 else ''), role+'\nסופרים רק את הטקסט שנכתב. הפסקאות הריקות הן מקומות שמורים, ולא פסקאות נוספות. '+('לפני משפט 3 חושבים הפוך.' if step==3 else 'לפני משפט 5 חוזרים לעמדה שלנו.' if step==5 else ''), section='essay',paragraphs=paras)
progression=S[:]
S=old_slides[:70]+progression+old_slides[70:]
for n,s in enumerate(S,1):s['n']=n

assert len(S)>=65
assert sum(s['kind']=='animation' for s in S)==12
for a,b in zip(S,S[1:]):
    if a.get('pair') and not a.get('reveal'):
        assert b.get('pair')==a['pair'] and b['reveal']
        assert a['text']==b['text'] and a.get('options')==b.get('options')
data=dict(title='Advanced Grammar in an Essay',grade='י״א · 5 יח״ל',durationMinutes=90,wordCount=WC,topic=TOPIC,sentences=SENTENCES,paragraphSteps=PARAGRAPH_STEPS,paragraphs=P,slides=S,source=SOURCE)
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
nav=''.join(f'<a href="#slide-{next(s["n"] for s in S if s["section"]==sec)}">{label}</a>' for sec,label in [('plan','תכנון'),('gerund','דקדוק'),('essay','חיבור'),('write','כתיבה')])
index=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>י״א · Advanced Grammar in an Essay</title><link rel="stylesheet" href="../../assets/lesson-decks/deck.css"><link rel="stylesheet" href="lesson.css?v=20260919-for-against"></head><body><a class="home" href="../five-units/" aria-label="חזרה לכיתה י״א 5 יח״ל">⌂</a><nav class="lesson-sections">{nav}</nav><main class="stage">{sections}</main><nav class="nav"><div class="nav-group"><button data-step="-1" aria-label="לשקף הקודם">←</button><button data-step="1" aria-label="לשקף הבא">→</button></div><div class="progress" id="counter" aria-live="polite"></div><a class="download" href="files/grammar-in-an-essay.pptx?v=20260919-for-against">PPTX</a></nav><div class="progress-track"><div class="progress-fill"></div></div><script src="../../assets/lesson-decks/deck.js"></script><script src="lesson.js"></script></body></html>'''
(OUT/'index.html').write_text(index)
timeline=[('0–8','plan','הצגת המשימה ותכנון קצר'),('8–14','intro','בניית פתיחה'),('14–27','gerund','gerunds, פיתוח נימוק ומילות קישור'),('27–37','passive','סביל ומוקד המשפט'),('37–46','perfect','ניסיון קודם ו־Present Perfect'),('46–58','conditionals','תנאי ראשון ושני בתוך טיעון'),('58–67','body2','חזרה לעמדה, סיום ובניית החיבור בעשרה שלבים'),('67–74','practice','תרגול המבנה בנושא עבודה אחרי הלימודים'),('74–86','write','כתיבה עצמאית'),('86–90','end','בדיקה וכרטיס יציאה')]
rows=''.join(f'<tr><td dir="ltr">{a}</td><td>{next(s["n"] for s in S if s["section"]==b)}</td><td>{c}</td></tr>' for a,b,c in timeline)
script=''.join(f'<details><summary>שקף {s["n"]}: {E(s["title"])}</summary><p>{E(s["note"])}</p><p class="en">{E(s["text"])}</p><a href="index.html#slide-{s["n"]}">פתיחת השקף</a></details>' for s in S)
teacher=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>תסריט למורה · Advanced Grammar in an Essay</title><style>body{{margin:0;background:#07111f;color:#f7f7f2;font:19px/1.7 Arial}}main{{max-width:960px;margin:auto;padding:32px 24px}}h1,h2{{color:#4ee5ff}}a{{color:#dfff5b}}.en{{direction:ltr;text-align:left;white-space:pre-line}}details{{border-bottom:1px solid #ffffff30;padding:14px 0}}summary{{cursor:pointer;font-weight:bold}}table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #ffffff30;text-align:right}}@media print{{body{{background:white;color:black}}a,h1,h2{{color:black}}}}</style></head><body><main><a href="../five-units/">כיתה י״א 5 יח״ל</a><h1>Advanced Grammar in an Essay</h1><p>{len(S)} שקפים, 12 הפוגות מונפשות, תרגול מדורג ושעונים. שיעור המשך לאחר השלמת Advanced Grammar.</p><p><a href="index.html">מצגת</a> · <a href="files/grammar-in-an-essay.pptx?v=20260919-for-against">PPTX</a></p><h2>מה ילמדו</h2><p>בניית חיבור בעד ונגד עם עמדה ברורה: פתיחה ניטרלית, I claim that, טענה נגדית ב־On the one hand, חזרה לעמדה ב־On the other hand וסיום; שימוש משמעותי ב־gerunds, בסביל, ב־Present Perfect, בתנאי ראשון ובמילות קישור. תנאי שני נשאר להשוואה בלבד. התלמידים מיישמים את הדרך בנושא קרוב ומפיקים טיוטה עצמאית.</p><h2>היקף וזמן</h2><p>המסלול המלא מיועד לכ־90 דקות. בשיעור של 80 דקות: קצרו את קריאת הפסקאות החוזרת בשלב החיבור השלם ואת שיתוף התשובות. שמרו על 12 דקות כתיבה ו־2 דקות עריכה. בכיתה שצריכה זמן נוסף, סיימו אחרי בניית הפסקה השנייה והמשיכו בחיבור השלם ובכתיבה במפגש הבא.</p><table><tr><th>דקות מתחילת השיעור</th><th>שקף פתיחה</th><th>עבודה</th></tr>{rows}</table><h2>הפעלת שעונים והנפשות</h2><p>ב־HTML השעונים מתחילים בלחיצה, ניתנים לעצירה, לאיפוס ולהוספת 30 שניות. יציאה משקף עוצרת את השעון. כשהזמן נגמר, השקף נשאר במקומו. ההפוגות שקטות, נמשכות כ־11 שניות וניתנות להשהיה ולהפעלה חוזרת. כיבוד העדפת צמצום תנועה מובנה במצגת.</p><p>ב־PPTX זמני הפעילות מוצגים כהנחיות קבועות. ההפוגות כוללות GIF משובץ; ההפעלה תלויה בתמיכת תוכנת המצגות. לשליטה מלאה בשעונים ובהנפשות השתמשו בגרסת האתר.</p><h2>הדגשים להוראה</h2><p>הצגת ארבע פסקאות ויעד של ארבעה מבנים שונים היא מסגרת תרגול כיתתית. אין ללמד זאת כרשימת תנאי סף רשמית לכל חיבור. אין להציג ספירה כפולה של Although כהוראת ניקוד רשמית. שמות מבנים, הדגשות ורשימות בדיקה משמשים למשוב כיתתי ואינם חלק מהחיבור המוגש. מועד בחינה מסוים אינו חלק משיעור זה.</p><p>האורך 120–140 מילים תואם למשימות G משנת 2026. תמיד קוראים את הוראות המשימה העדכניות. נושאי החיבורים והדוגמאות כאן מקוריים לצורך התרגול.</p><h2>סדר הכתיבה</h2><p>1 פתיחה בלי דעה; 2 דעה הכוללת I claim that; 3 טענה נגדית; 4 תנאי ראשון; 5 תמיכה בעמדה; 6 Present Perfect; 7 מסקנה; 8 סביל. לאחר מכן מוסיפים את הרחבה 9 לפסקה השנייה ואת הרחבה 10 לשלישית. סדר הקריאה הסופי: 1,2 / 3,4,9 / 5,6,10 / 7,8. הטיוטה בת שמונת המשפטים מכילה 107 מילים ולכן עדיין אינה מוכנה להגשה. אחרי ההרחבות: 128 מילים.</p><p>בתרגול העצמאי: הנושא הוא Should teenagers have an after-school job? הדוגמאות להמחשת תבניות ניתנות בנושא הקבוע From what age should children have their own cellphone? מבקשים משפט אחד בכל פעם, נותנים פתיח ניטרלי וחומר למחשבה, מתקנים רק מה שנחוץ, ומציגים את החיבור עד עכשיו עם ספירת מילים. לא מסיימים מתחת ל־120 מילים. נמנעים מ־good ו־important ומשתמשים בחלופות לפי ההקשר.</p><h2>Topic</h2><p class="en">{E(TOPIC)}</p><h2>חיבור לדוגמה: {WC} מילים</h2><div class="en">{''.join('<p>'+E(p)+'</p>' for p in P)}</div><h2>תסריט לפי שקף</h2>{script}<h2>מקורות</h2><ul><li><a href="{SOURCE}">משרד החינוך: שאלון G, קיץ 2026, משימת כתיבה</a></li><li><a href="https://meyda.education.gov.il/files/Pop/0files/english/Chativa-Elyona/Bagrut/FGExternalInternal2020.pdf">מחוון הכתיבה של G</a></li><li><a href="../five-units/advanced-grammar/">מצגת Advanced Grammar של הכיתה</a></li><li><a href="https://github.com/Simonh68/teachers/blob/main/PROJECT_CHARTER.md">אמנת Teachers</a></li></ul><p>איורי החתולים נוצרו עבור שיעורי Teachers. כאן כל אחד משמש פעם אחת, עם משפט מקורי המותאם לכתיבת חיבור.</p></main></body></html>'''
(OUT/'teacher.html').write_text(teacher)
manifest=[dict(n=s['n'],kind=s['kind'],title=s['title'],section=s['section']) for s in S]
(ROOT/'tools/grammar-in-an-essay/build/slide-list.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(f'{len(S)} slides, {WC} words, 12 animations. '+str(OUT))
