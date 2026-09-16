from pathlib import Path
import json, html, shutil

ROOT=Path(__file__).resolve().parents[2]
REPO=ROOT
OUT=REPO/'grade9/message-exam-practice'
(OUT/'assets').mkdir(parents=True,exist_ok=True)
(OUT/'files').mkdir(exist_ok=True)
esc=html.escape
slides=[]
def add(kind,body,note,section='start',pair=None,title=''):
    slides.append(dict(n=len(slides)+1,kind=kind,body=body,note=note,section=section,pair=pair,title=title))
def meta(label,tense=''):
    return f'<div class="slide-meta"><div class="eyebrow">{label}</div><div class="tense">{tense}</div></div>'
def info(title,body,note,section='start',kind='info'):
    add(kind,meta({'start':'מתכוננים למבחן','read':'חוזרים לטקסט','write':'כותבים בעצמנו','end':'מסיימים וממשיכים'}[section])+f'<h2 class="part-title">{title}</h2>'+body,note,section,title=title)
def en(text,cls='instruction'):
    return f'<p class="en {cls}" lang="en">{text}</p>'
def he(text,cls='instruction'):
    return f'<p class="{cls}">{text}</p>'
def qa(q,a,note,section='read',pair=None,extra='',source=''):
    pair=pair or f'qa-{len(slides)+1}'
    tense='עבר' if any(x in q for x in ['went wrong','was the class','did Noam','wanted to help']) else ('הווה' if 'does Noam move' in q else '')
    core=meta('קוראים · חושבים · מוצאים הוכחה',tense)+f'<div><h2 class="en question" lang="en">{q}</h2>{extra}</div>'
    add('qa',core+'<div class="answer-slot"></div>',note,section,pair,q)
    add('qa reveal',core+f'<div class="answer-slot"><p class="answer-label">תשובה אפשרית</p><p class="en possible-answer" lang="en">{a}</p><p class="evidence">{source}</p></div>',f'אפשר לקבל ניסוחים אחרים שמבוססים על הטקסט. {note}',section,pair,q)
def gap(before,after,opts,correct,explain,note,section='vocab'):
    pair=f'gap-{len(slides)+1}'
    width=max(len(x) for x in opts)+1
    for reveal in [False,True]:
        choices=''.join(f'<div class="choice {"correct" if reveal and i==correct else ""}"><b>{chr(65+i)}</b><span>{esc(x)}</span></div>' for i,x in enumerate(opts))
        answer=esc(opts[correct]) if reveal else '&nbsp;'
        sentence=f'{before}<span class="gap {"filled" if reveal else ""}" style="--gap-ch:{width}">{answer}</span>{after}'
        body=meta('בוחרים תשובה · מסבירים למה','הווה' if before=='I ' else 'עבר')+f'<h2 class="en question" lang="en">{sentence}</h2><div class="choices en" lang="en">{choices}</div><div class="answer-slot">'+(f'<p class="explanation">{explain}</p>' if reveal else '')+'</div>'
        add('gap-slide'+(' reveal' if reveal else ''),body,note if not reveal else 'חשפו רק עכשיו את התשובה. '+explain,section,pair,before+'___'+after)

animations=[
('half-message','The message loaded. The meaning didn’t.','חתול קורא הודעה בטלפון, נבהל ואז מגלה את ההמשך.', 'לפני שמסיקים מסקנה: האם קראנו את כל ההודעה?'),
('wrong-envelope','Right message. Wrong human.','חתול רודף אחרי מעטפה שנוחתת על ראשו.', 'הפוגה קצרה. מילה אחת: mistake.'),
('serious-cat','Very serious. Slightly blurry.','חתול רציני עם משקפיים ענקיים שמחליקים.', 'אפשר לשאול: Is he angry, or just trying to see?'),
('however-cat','Tiny book. Huge adventure.','חתול קופץ מעל ספר קטן במאמץ מוגזם.', 'בקול: It was a tiny book. However, the jump was huge.'),
('missing-piece','The answer was behind his ear.','חתול מחפש חלק של פאזל שנמצא מאחורי אוזנו.', 'הפוגה של שמונה שניות; חוזרים למילה understanding.'),
('so-far','So far… three books.','חתול מטפס על שלושה ספרים כאילו הם הר.', 'So far — מה כבר הספקנו? תשובת מילה אחת.'),
('tiny-goal','New goal: aim at the bin.','כדור נייר נוחת על ראשו של חתול במקום בסל.', 'גם כשהניסיון הראשון נכשל, אפשר לנסות להשיג את המטרה.'),
('two-friends','Friendship: a work in progress.','שני חתולים מנסים כיף, מפספסים ולבסוף מצליחים.', 'היחסים משתפרים גם בלי הצלחה מושלמת בכל ניסיון.'),
('certain-cat','Case closed. It’s my tail.','חתול בלש מגלה שהדבר החשוד הוא הזנב שלו.', 'Are you certain? חכו לבדיקה לפני מסקנה.'),
('helpful-bag','A small stand. A very big bag.','חתול מוציא מעמד עץ קטן מתיק כחול ענק.', 'רמז חזותי למעמד שאיתן מביא בסיפור.'),
('word-order','Everything is under control. Almost.','חתול מאזן ספרים שלבסוף נוחתים על ראשו.', 'הפוגה קצרה לפני סידור האירועים.'),
('chair-friend','Making room for a friend. Literally.','חתול מזיז כיסא לחבר, דוחף רחוק מדי ולבסוף שניהם יושבים יחד.', 'מקום ליד השולחן יכול להראות שייכות וחברות.')]
def anim(idx,section):
    ident,caption,alt,note=animations[idx-1]
    body=meta(f'הפוגה קצרה · {idx} / 12')+f'<div class="sprite" role="img" aria-label="{esc(alt)}" style="background-image:url(assets/{ident}.webp)"></div><p class="en caption" lang="en">{caption}</p><div class="animation-controls"><button type="button" data-anim-toggle aria-label="השהיית ההנפשה">Ⅱ</button><button type="button" data-anim-replay aria-label="הפעלה מחדש">↻</button></div>'
    add('animation',body,'8–12 שניות בלבד, ללא קול. '+note,section,title=caption)

add('cover',meta('כיתה ט׳1')+'<h1 class="cover-title">ברוכים הבאים</h1><p class="cover-sub">ישיבת בני עקיבא קריית הרצוג</p>', 'פתחו את דף העבודה. היום משלבים אוצר מילים, קריאה וכתיבה לקראת המבחן.',title='ברוכים הבאים')
info('יש לנו מבחן באנגלית',he('יום ראשון, ל׳ בתשרי תשפ״ז<br><span class="gregorian" dir="ltr">(11.10.2026)</span>','date-main')+he('מתכוננים באוצר מילים, בהבנת הנקרא ובכתיבה.')+he('המועד פורסם בלוח בית הספר ועשוי להשתנות.','small-note'),'הציגו את מועד המבחן. הבהירו שהטקסט המוכר משמש לתרגול מיומנויות; לא הובטח שזה הטקסט שיופיע במבחן.')
info('נשארו 3 מפגשים כפולים', '<div class="meeting-list"><p><b>היום</b> · יום רביעי, ה׳ בתשרי תשפ״ז <span dir="ltr">(16.9.2026)</span></p><p>יום ראשון, כ״ג בתשרי תשפ״ז <span dir="ltr">(4.10.2026)</span></p><p>יום רביעי, כ״ו בתשרי תשפ״ז <span dir="ltr">(7.10.2026)</span></p></div>'+he('כולל המפגש היום · לפי המערכת המתוכננת','small-note'),'אמרו: We have three double lessons left before the test, including today. Today we will practise vocabulary, answer reading questions and write a short paragraph.')
info('בסוף השיעור נוכל…','<div class="goal-grid"><p><b>01</b> להשתמש ב־8 מילים וביטויים</p><p><b>02</b> לבסס תשובה על הטקסט</p><p><b>03</b> לכתוב פסקה ברורה</p></div>','הזכירו: המילים לבוחן הראשון הן קבוצות 01–02 ב־Band II, Core I. שמונה המילים היום הן מדגם מתוך הרשימה, לא כל הרשימה.')
anim(1,'start')
qa('What went wrong between Noam and Eitan?','Noam read only part of Eitan’s message and thought Eitan did not want to help.','אספו תשובה אחת מהזיכרון; אל תקראו שוב את כל הסיפור בשלב זה.','start',source='נבדוק את הפרטים בקריאה החוזרת.')
anim(2,'start')
vocab=[
('by mistake','phrase','בטעות','I took the wrong umbrella by mistake.','לקחתי בטעות את המטרייה הלא נכונה.','עבר',1,3),
('however','adverb','עם זאת','It was cold. However, we went out.','היה קר. עם זאת, יצאנו.','עבר',1,4),
('understanding','noun','הבנה; ידע','Thank you for your patience and understanding.','תודה על הסבלנות וההבנה.','',1,5),
('so far','idiom','עד כה','So far, everything is fine.','עד כה הכול בסדר.','הווה',1,6),
('achieve','verb','להשיג','She worked hard to achieve her goal.','היא עבדה קשה כדי להשיג את מטרתה.','עבר',2,7),
('relations','noun','יחסים','Canada has diplomatic relations with China.','לקנדה יחסים דיפלומטיים עם סין.','הווה',2,8),
('certain','adjective','בטוח','I am certain he will come.','אני בטוח שהוא יבוא.','',2,9),
('be responsible for something','phrase','להיות אחראי למשהו','I will not be responsible for my actions.','אני לא אהיה אחראי למעשיי.','עתיד',2,10)]
for idx,(word,pos,meaning,example,translation,tense,group,breakid) in enumerate(vocab):
    core=meta(f'Band II · Core I · Group {group:02d}',tense)+f'<h2 class="en word" lang="en">{word}<span class="qualifier">{pos}</span></h2><p class="en example" lang="en">{example}</p>'
    for reveal in [False,True]:
        slot=f'<p class="meaning">{meaning}</p><p class="translation">{translation}</p>' if reveal else ''
        add('vocab'+(' reveal' if reveal else ''),core+f'<div class="translation-slot">{slot}</div>',('קראו את המילה והמשפט; בקשו פירוש לפני המעבר.' if not reveal else 'חשפו את הפירוש. תלמיד אחד קורא שוב את המשפט.')+(' המובן כאן: certain = בטוח.' if word=='certain' else ''),'vocab',f'word-{idx}',word)
    anim(breakid,'vocab')
gap('I took your book ','. I thought it was mine.',['on purpose','by mistake','at last'],1,'חשבתי שזה הספר שלי — לכן לקחתי אותו בטעות.','כולם בוחרים A, B או C, ואז מסבירים איזו ראיה במשפט עזרה להם.')
info('The Message Without a Voice',en('Read the story again. Underline one misunderstanding and one action that helps the friendship.')+he('עובדים בדף: פסקאות A–K. קראו בשקט במשך 4 דקות.')+'<div class="resource-links"><a href="files/message-exam-practice.pdf" target="_blank">פתיחת דף העבודה · PDF</a></div>','חלקו את הדף או פתחו את הקובץ. ארבע דקות קריאה שקטה. התמקדו בחוסר ההבנה ובפעולה מתקנת.','read')
qa('What was the class preparing?','The class was preparing a book sale for a community library.','בקשו לציין פסקה ולהבחין בין הפעילות לבין המטרה.',source='הוכחה: פסקה A.')
qa('What did Noam think Eitan meant?<br>What did Eitan actually mean?','Noam thought Eitan did not want to help. Eitan meant: start for now; I can bring the stand tomorrow.','בזוגות: תלמיד אחד מסביר את המחשבה של נועם, השני את הכוונה של איתן. שתי דקות לפני החשיפה.',source='הוכחה: פסקאות B ו־D.')
qa('Which two details show that Eitan wanted to help?','He and his father finished the stand late at night. He brought the stand to school.','הבדילו בין דעה לבין שתי פעולות מפורשות בסיפור.',source='הוכחה: פסקה E, ובפסקה D מופיע תכנון הבאת המעמד.')
anim(11,'read')
qa('Put the events in the correct order.','B → D → A → C','תנו דקה עצמאית ועוד דקה להשוואה בזוגות.',pair='event-order',extra='<ol class="en events" lang="en" type="A"><li>Eitan explains the missing message.</li><li>Noam reads the short message.</li><li>The boys welcome the first visitors.</li><li>Eitan brings a wooden stand.</li></ol>',source='קוראים לפי רצף הסיפור, לא לפי סדר הצגת האפשרויות.')
qa('Why does Noam move his chair at the end?','He wants Eitan to feel welcome and included. His action suggests that their friendship is beginning to recover.','זו הסקה: יש יותר מניסוח מוצלח אחד, אבל חייבים להסביר כיצד הפעולה תומכת בו.',source='הוכחה: פסקה K — נועם מזיז את כיסאו ומציע לאיתן לשבת.')
anim(12,'read')
gap('I ',' with you.',['agree','am agreeing','agrees'],0,'כאן agree מבטא דעה או הסכמה. משתמשים ב־Present Simple.','חזרו לאמירה של איתן: I agree. בקשו לזהות את הנושא I.','language')
gap('Noam was still hurt. ', ', he thanked Eitan for the stand.',['Because','However','For example'],1,'However מציג ניגוד: הוא עדיין נפגע, ובכל זאת הודה לחברו.','הצביעו גם על הנקודה לפני However ועל הפסיק אחריו.','language')
gap('Noam misunderstood Eitan ', ' part of the message was missing.',['however','although','because'],2,'Because מציג סיבה: חלק מההודעה היה חסר.','בקשו להשלים בקול ולזהות את הסיבה.','language')
info('Your turn: a misunderstanding',en('Write 70–100 words about a misunderstanding between two friends. Explain what happened and how they solved it.')+he('אפשר להמציא סיפור. אין צורך לשתף אירוע אישי.'),'תנו שמונה דקות לכתיבה עצמאית ועוד זמן לתכנון ולבדיקה. מסגרת האורך היא משימת התרגול היום; לא דרישה מאומתת של המבחן.','write')
info('Plan before you write','<div class="writing-plan en" lang="en"><p><b>1</b> What happened?</p><p><b>2</b> What did each friend think?</p><p><b>3</b> How did they solve the problem?</p></div>'+he('כתבו תחילה שלוש הערות קצרות — לא פסקה שלמה.'),'שתי דקות תכנון. הסתובבו בין התלמידים ועזרו רק בבחירת אירוע וקשר סיבתי.','write')
info('Need a first sentence?',en('“Last week, I sent my friend the wrong message by mistake…”','writing-starter')+he('המשיכו בכיוון שלכם. אפשר גם להתחיל בדרך אחרת.'),'משפט הפתיחה הוא תמיכה, לא תשובה להעתקה. את השאר התלמידים מפתחים בעצמם. לתלמידים מתקדמים: הוסיפו דיאלוג קצר.','write')
info('Check your paragraph','<div class="checklist en" lang="en"><p>□ 70–100 words</p><p>□ Three target words or phrases</p><p>□ Mainly Past Simple</p><p>□ because and however</p><p>□ A clear problem and solution</p></div>','בשתי דקות הסיום: סמנו שלוש מילות יעד, בדקו זמן עבר ושימוש נכון במילות הקישור. תלמידים הזקוקים לתמיכה יכולים להיעזר ברשימת המילים בדף.','write')
qa('What should you do when a message sounds unfriendly?','Ask the person what they meant before you assume. Read the whole message.','כרטיס יציאה: משפט אחד במחברת. בקשו גם לתקן דבר אחד בפסקה שכתבו.','end',source='יותר מניסוח אחד יכול להתאים.')
info('לקראת המפגש הבא',he('סיימו ותקנו את הפסקה שלכם.<br>תרגלו את כל המילים בקבוצות 01–02 ב־Band II, Core I.')+'<div class="resource-links"><a href="https://englishfornoar.co.il/band-ii/groups/group-01.html?preview=20260902" target="_blank">קבוצה 01 · תרגול</a><a href="https://englishfornoar.co.il/band-ii/groups/group-02.html?preview=20260902" target="_blank">קבוצה 02 · תרגול</a></div>'+he('פירוש · הגייה · איות · שימוש במשפט','small-note'),'הזכירו שהתרגול היום כלל שמונה ערכים בלבד מתוך שתי הקבוצות. יש לתרגל את שתי הקבוצות בשלמותן.','end')
assert len(slides)==60, len(slides)
assert sum(s['kind']=='animation' for s in slides)==12

sections=''.join(f'<section class="slide {s["kind"]}" data-slide="{s["n"]}" data-section="{s["section"]}"'+(f' data-pair="{s["pair"]}"' if s['pair'] else '')+f' aria-label="שקף {s["n"]} מתוך 60" hidden><div class="frame">{s["body"]}</div></section>' for s in slides)
nav=''.join(f'<a href="#slide-{n}">{label}</a>' for n,label in [(2,'מבחן'),(9,'מילים'),(35,'קריאה'),(48,'שפה'),(54,'כתיבה')])
index=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>ט׳ · The Message Without a Voice · הכנה למבחן</title><link rel="stylesheet" href="../../assets/lesson-decks/deck.css"><link rel="stylesheet" href="lesson.css?v=20260916b"></head><body><a class="home" href="../../#grade9" aria-label="חזרה לחוצץ כיתה ט׳"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 11 9-8 9 8M5 9v12h14V9M9 21v-8h6v8"/></svg></a><nav class="lesson-sections" aria-label="חלקי השיעור">{nav}</nav><main class="stage">{sections}</main><nav class="nav" aria-label="ניווט במצגת"><div class="nav-group"><button data-step="-1" aria-label="לשקף הקודם">←</button><button data-step="1" aria-label="לשקף הבא">→</button></div><div class="progress" id="counter" aria-live="polite"></div><a class="download" href="files/message-exam-practice.pdf" target="_blank">דף עבודה PDF</a></nav><div class="progress-track"><div class="progress-fill"></div></div><script src="../../assets/lesson-decks/deck.js"></script><script src="lesson.js"></script></body></html>'''
(OUT/'index.html').write_text(index)
(OUT/'lesson.json').write_text(json.dumps({'title':'The Message Without a Voice · Exam practice','grade':'ט׳1','date':'2026-09-16','durationMinutes':80,'slides':slides,'vocabulary':[dict(zip(['word','partOfSpeech','meaning','example','translation','tense','group','animation'],v)) for v in vocab],'animations':[dict(zip(['id','caption','alt','note'],x)) for x in animations]},ensure_ascii=False,indent=2))
timeline=[('10:25–10:32','1–8','פתיחה, תאריך המבחן, שלושת המפגשים שנותרו ושחזור קצר.'),('10:32–10:50','9–34','שמונה מילים וביטויים מקבוצות 01–02; פירוש נחשף בשקף נפרד; תרגיל בחירה.'),('10:50–11:15','35–47','ארבע דקות קריאה חוזרת, איתור ראיות, עבודה בזוגות, רצף והסקה.'),('11:15–11:23','48–53','I agree; שימוש ב־however וב־because.'),('11:23–11:38','54–57','תכנון 2 דקות, כתיבה 8 דקות ובדיקה/שיתוף 5 דקות.'),('11:38–11:45','58–60','כרטיס יציאה, תיקון אחד בפסקה ושיעורי בית.')]
rows=''.join(f'<tr><td dir="ltr">{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in timeline)
script=''.join(f'<details><summary>שקף {s["n"]} · {esc(s["title"] or s["kind"])}</summary><p>{esc(s["note"])}</p><a href="index.html#slide-{s["n"]}">פתיחת השקף</a></details>' for s in slides)
teacher=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>תסריט ומפתח · ט׳ · הכנה למבחן</title><style>@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;800&display=swap');*{{box-sizing:border-box}}body{{background:#07111f;color:#f7f7f2;font:18px/1.75 Heebo,Arial;margin:0}}main{{max-width:960px;margin:auto;padding:35px 24px 80px}}h1,h2{{line-height:1.3}}h1{{color:#dfff5b}}h2{{margin-top:40px;color:#4ee5ff}}a{{color:#4ee5ff}}.lead{{font-size:21px}}.links{{display:flex;gap:20px;flex-wrap:wrap}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ffffff30;padding:12px;text-align:right;vertical-align:top}}td:first-child{{white-space:nowrap}}details{{border:1px solid #ffffff25;border-radius:10px;margin:10px 0;padding:12px 18px}}summary{{cursor:pointer;font-weight:800}}.en{{direction:ltr;text-align:left;font-family:Arial;line-height:1.7}}.note{{background:#ffc85715;border-right:4px solid #ffc857;padding:16px}}@media(max-width:600px){{body{{font-size:16px}}td,th{{padding:6px}}}}@media print{{body{{background:white;color:black}}a,h1,h2{{color:black}}details{{break-inside:avoid}}}}</style></head><body><main><p><a href="../../#grade9">← חוצץ כיתה ט׳</a></p><h1>ט׳1 · תסריט ומפתח תשובות</h1><p class="lead">יום רביעי, ה׳ בתשרי תשפ״ז (16.9.2026) · 10:25–11:45<br>60 שקפים · 12 הפוגות מונפשות ושקטות</p><div class="links"><a href="index.html">פתיחת המצגת</a><a href="files/message-exam-practice.pdf">דף העבודה לתלמידים</a></div><h2>מטרות והכנה</h2><p>להשתמש בשמונה ערכים מקבוצות 01–02 ב־Band II, Core I, לבסס תשובות על ראיות בטקסט, ולהפיק פסקה בת 70–100 מילים על אי־הבנה בין חברים.</p><p>הכינו דף עבודה לכל תלמיד. בזום: שלחו את קישור ה־PDF לפני השיעור; התלמידים יכולים לענות במחברת. שקפי ההפוגה פועלים ללא קול כ־11 שניות ונעצרים; אין מעבר שקף אוטומטי.</p><div class="note"><b>דיוק לקראת המבחן:</b> המועד שפורסם הוא יום ראשון, ל׳ בתשרי תשפ״ז (11.10.2026), ועשוי להשתנות. לא נמצא פירוט מלא מאומת של מבנה המבחן. הטקסט המוכר והפסקה משמשים לתרגול; אין להציג אותם כהבטחה לשאלות או לטקסט שיופיעו במבחן. קבוצות 01–02 הן הרשימה לבוחן הראשון לפי מצגת הפתיחה והודעת המורה. מילות Core II שבסיפור הישן אינן מחליפות רשימה זו.</div><h2>חלוקת הזמן</h2><table><thead><tr><th>שעה</th><th>שקפים</th><th>מה עושים</th></tr></thead><tbody>{rows}</tbody></table><h2>פתיחה מוצעת</h2><p class="en" lang="en">We have three double lessons left before the test, including today. Today we will practise vocabulary, answer reading questions and write a short paragraph.</p><h2>מפתח לדף העבודה</h2><ol class="en" lang="en"><li>A book sale for a community library. Paragraph A.</li><li>Noam thought Eitan did not want to help; Eitan meant that Noam should start for now and he would bring the stand the next day. B and D.</li><li>Eitan and his father finished a stand late at night; Eitan brought it. E.</li><li>B → D → A → C.</li><li>Noam wants Eitan to feel included; moving the chair and offering a seat suggest a repaired friendship. K. Accept other supported interpretations.</li><li>He still feels hurt, but the stand shows that Eitan cares. I.</li></ol><p class="en" lang="en"><b>Vocabulary and language:</b> 1 B (by mistake); 2 A (achieve); 3 C (certain); 4 A (agree); 5 B (However); 6 C (because).</p><p><b>כתיבה:</b> בדקו תוכן וקשר בין הבעיה לפתרון, שלוש מילות יעד בשימוש נכון, שימוש סביר בעבר פשוט, because לסיבה ו־however לניגוד. אין צורך שכל תלמיד ישתמש באותן שלוש מילים. אפשר לקבל שגיאות קלות שאינן פוגעות בהבנה ולתת תיקון ממוקד אחד.</p><h2>התאמה לרמות ולקצב</h2><p>לתלמידים הזקוקים לתמיכה: אפשר לסמן מראש את פסקאות B, D, E ו־K, לתת תכנון בעל־פה ולעזור לבחור שלוש מילים. למתקדמים: בקשו להבחין בין כוונה להשפעה ולהוסיף דיאלוג קצר בכתיבה. אם הקריאה אורכת יותר: קצרו שיתוף מליאה והשלימו עריכת פסקה בבית; שמרו על זמן כתיבה עצמאי.</p><h2>תסריט לפי שקף</h2>{script}<h2>מקורות</h2><ul><li><a href="https://simonh68.github.io/teachers/grade9/">מצגת פתיחת השנה — קבוצות 01–02 ודוגמאות המילים</a></li><li><a href="https://simonh68.github.io/teachers/grade9/the-message-without-a-voice/">המצגת המקורית של הסיפור</a></li><li><a href="https://docs.google.com/document/d/1WOUZ24kb3trJTgNhYegvD1n-YbAL4cG66D3_koVQfI0/edit?tab=t.ehc41uhvf745">הטקסט ומעקב כיתה ט׳ במחברת</a></li><li><a href="https://drive.google.com/file/d/1D5qZ4kQdHzX4Nz0o1eFwlE7gmvTNsHIY/view">לוח המבחנים של ט׳ — מועד שפורסם ועשוי להשתנות</a></li><li><a href="https://github.com/Simonh68/teachers/blob/main/PROJECT_CHARTER.md">אמנת Teachers</a></li></ul></main></body></html>'''
(OUT/'teacher.html').write_text(teacher)
print(f'Authored {len(slides)} slides at {OUT}')
