"""Build the shared Connectors lesson and its three class entry points."""
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade9/connectors'
S=[]
def slide(kind='example', **kw):
    S.append(dict(kind=kind, **kw))
def idea(family, image, en, he):
    slide('idea', family=family, image=image, en=en, he=he)
def example(family, title, sentence, he, rule='', base='', tense='הווה'):
    slide(family=family,title=title,sentence=sentence,he=he,rule=rule,base=base,tense=tense)
B='The cat is tired, but it keeps playing.'
A='The app has games, and it has stories.'
C='My phone is off because the battery is dead.'
slide('cover',title='Connectors',he='מילות קישור',sub='ט׳ · י׳ · י״א')
example('contrast','BUT', 'The cat is tired, <b>but</b> it keeps playing.', 'החתול עייף, אבל הוא ממשיך לשחק.', 'ניגוד בין שני רעיונות')
for i,(word,he,rule) in enumerate([
    ('However','אולם / עם זאת','משפט חדש. אחר כך מילת הקישור ופסיק.'),
    ('Nevertheless','אף על פי כן','הוא ממשיך למרות העייפות. ביטוי רשמי יותר.'),
    ('Nonetheless','אף על פי כן','משמעות דומה ל־Nevertheless.'),
    ('Even so','למרות זאת','גם במצב הזה הוא ממשיך לשחק.')]):
    idea('contrast','contrast-'+('a' if i%2==0 else 'b'),'Tired. Still playing.','עייף, ובכל זאת משחק')
    example('contrast',word,'The cat is tired<em>.</em> <b>'+word+'</b><em>,</em> it keeps playing.',he,rule,B)
idea('contrast','contrast-b','Lazy? Full of energy.','אולי הוא דווקא מלא אנרגיה?')
example('contrast','BUT · משפט חדש','The cat isn’t lazy, <b>but</b> it is full of energy.','החתול אינו עצלן, אלא מלא אנרגיה.','כאן מתקנים רושם שגוי: עצלן או מלא אנרגיה?')
example('contrast','On the contrary','The cat isn’t lazy<em>.</em> <b>On the contrary</b><em>,</em> it is full of energy.','להפך','מתקנים טענה או רושם ומציגים את ההפך.','The cat isn’t lazy, but it is full of energy.')
idea('addition','addition-a','A book. A new idea.','קריאה שמוסיפה רעיון')
example('addition','AND','The app has games, <b>and</b> it has stories.','באפליקציה יש משחקים, ויש בה סיפורים.','מוסיפים עוד פרט')
for i,(word,rule) in enumerate([
    ('Moreover','מוסיפים פרט שמחזק את הנקודה. ביטוי רשמי יותר.'),
    ('Furthermore','מוסיפים עוד פרט או נימוק. ביטוי רשמי יותר.'),
    ('In addition','מוסיפים מידע. משפט חדש ופסיק אחרי הביטוי.'),
    ('Additionally','מוסיפים מידע. משפט חדש ופסיק אחרי המילה.')]):
    idea('addition','addition-'+('b' if i%2==0 else 'a'),'One idea. One more.','מוסיפים משהו קשור')
    example('addition',word,'The app has games<em>.</em> <b>'+word+'</b><em>,</em> it has stories.','בנוסף / יתרה מזאת',rule,A)
idea('addition','addition-b','And there is more.','עוד פרט שמחזק את הרעיון')
example('addition','Not to mention','The app has games<em>,</em> <b>not to mention</b> <u>stories</u>.','שלא לדבר על','בדוגמה הזו הביטוי בא לפני שם עצם: stories.',A)
idea('cause','cause-a','An empty battery.','מה קורה לטלפון עכשיו?')
example('cause','BECAUSE','My phone is off <b>because</b> the battery is dead.','הטלפון שלי כבוי כי הסוללה ריקה.','אחרי because מופיע משפט עם נושא ופועל.')
idea('cause','cause-b','A silent phone.','הסוללה מסבירה את התוצאה')
example('cause','Since','My phone is off <b>since</b> the battery is dead.','מכיוון ש־','כאן Since מציין סיבה. בהקשרים אחרים הוא מציין זמן.',C)
idea('cause','cause-a','The reason is clear.','הסיבה ידועה')
example('cause','Given that','<b>Given that</b> the battery is dead<em>,</em> my phone is off.','בהתחשב בכך ש־','מציגים עובדה שעליה מבוסס ההסבר.',C)
idea('cause','cause-b','A battery. A result.','סיבה ותוצאה')
example('cause','Due to','My phone is off <b>due to</b> <u>the dead battery</u>.','בגלל / עקב','כאן צריך צירוף שמני: the dead battery.',C)
idea('cause','cause-a','No power. No call.','הסיבה נשארת אותה סיבה')
example('cause','As a result of','My phone is off <b>as a result of</b> <u>the dead battery</u>.','כתוצאה מ־','אחרי of מופיע כאן צירוף שמני.',C)
idea('cause','cause-b','Time to charge it.','המידע מוביל להחלטה')
example('cause','BECAUSE · החלטה','I charge my phone <b>because</b> the battery is dead.','אני מטעין את הטלפון כי הסוללה ריקה.','עכשיו מתארים החלטה בעקבות המידע.')
example('cause','In light of','<b>In light of</b> <u>the dead battery</u><em>,</em> I charge my phone.','לאור / בהתחשב ב־','לאור המצב אני מחליט לפעול. ביטוי רשמי.','I charge my phone because the battery is dead.')
slide('comparison',family='cause',title='As a result of / As a result',sentence='<b>As a result of</b> the dead battery, my phone is off.',second='The battery is dead. <b>As a result</b>, my phone is off.',he='עם of מציגים את הסיבה; בלי of מציגים את התוצאה.',tense='הווה')
for family,prompt,base,answer,he,rule in [
    ('contrast','החליפו את but ב־However','Dan is tired, but he studies.','Dan is tired<em>.</em> <b>However</b><em>,</em> he studies.','דן עייף. עם זאת, הוא לומד.','נקודה לפני However ופסיק אחריו.'),
    ('addition','החליפו את and ב־In addition','The app has music, and it has games.','The app has music<em>.</em> <b>In addition</b><em>,</em> it has games.','באפליקציה יש מוזיקה. בנוסף, יש בה משחקים.','שני משפטים שלמים.'),
    ('cause','החליפו את because ב־Due to','We stay home because it is raining.','We stay home <b>due to</b> <u>the rain</u>.','אנחנו נשארים בבית בגלל הגשם.','it is raining משתנה לצירוף השמני the rain.')]:
    slide('practice',family=family,title='Your turn',sentence=base,he=prompt,rule='',base='',tense='הווה')
    slide('practice',family=family,title='Your turn',sentence=base,he=prompt,rule=rule,answer=answer,base='',tense='הווה')
slide('summary',title='Connectors',he='בוחרים לפי הקשר, המבנה והפיסוק',rows=[['BUT','ניגוד','However, it keeps playing.'],['AND','תוספת','In addition, it has stories.'],['BECAUSE','סיבה','due to the dead battery']])
(OUT/'lesson.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
shell='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#050b14"><title>Connectors</title><link rel="stylesheet" href="../../grade9/connectors/lesson.css?v=20260914"><script defer src="../../grade9/connectors/lesson.js?v=20260914"></script></head><body><a class="home" href="../../#gradeGRADE" aria-label="חזרה לדף הכיתה" title="חזרה לדף הכיתה">⌂</a><button class="full" id="full" aria-label="מסך מלא" title="מסך מלא">⛶</button><main id="deck" aria-live="polite"></main><nav class="controls" aria-label="ניווט בשקפים" dir="ltr"><button id="prev" aria-label="השקף הקודם">←</button><select id="jump" aria-label="מעבר לשקף"></select><button id="next" aria-label="השקף הבא">→</button></nav><div class="progress"><i id="progress"></i></div><noscript>יש להפעיל JavaScript כדי להציג את המצגת.</noscript></body></html>'''
for grade in (9,10,11):
    (ROOT/f'grade{grade}/connectors/index.html').write_text(shell.replace('GRADE',str(grade)))
js=(ROOT/'tools/connectors/player.js').read_text()
(OUT/'lesson.js').write_text('const slides = '+json.dumps(S,ensure_ascii=False)+';\n'+js)
print(json.dumps({'slides':len(S),'idea_slides':sum(s['kind']=='idea' for s in S)},ensure_ascii=False))
